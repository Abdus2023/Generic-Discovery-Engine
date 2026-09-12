    class GenericDiscoveryEngine {
        constructor() {
            this.db =
                new KnowledgeBase();

            this.policy =
                new AcquisitionPolicy();

            this.origins =
                new OriginController();

            this.acquisition =
                new Acquisition(
                    this.origins
                );

            this.providers =
                new ProviderRegistry();

            this.ledger =
                new DecisionLedger();

            this.networkObserver =
                new NetworkObserver(
                    this
                );

            this.networkEvents =
                new Map();

            this.running = false;
            this.paused = false;
            this.stopRequested = false;

            this.activeWorkers = 0;
            this.requestsReserved = 0;

            this.currentConcurrency =
                CONFIG.concurrency;

            this.consecutiveFailures = 0;
            this.consecutiveSuccesses = 0;

            this.persistenceTimer = null;

            this.ui = null;
        }

        async init() {
            this.restore();

            this.ledger.recordDiagnostic(
                'engine-init',
                {
                    version:
                        CONFIG.version
                }
            );

            this.installUI();

            if (
                document.readyState ===
                'loading'
            ) {
                document.addEventListener(
                    'DOMContentLoaded',
                    () => this.bootstrap(),
                    {
                        once: true
                    }
                );
            } else {
                this.bootstrap();
            }
        }

        bootstrap() {
            this.observeCurrentPage();

            this.networkObserver.start();

            if (
                CONFIG.observeDomMutations
            ) {
                this.installMutationObserver();
            }

            this.start();
        }

        /*
         * --------------------------------------------------------
         * DISCOVERY
         * --------------------------------------------------------
         */

        discover(
            target,
            type = 'url',
            options = {}
        ) {
            const canonical =
                canonicalizeUrl(target);

            if (!canonical) {
                return null;
            }

            if (!isAllowedUrl(canonical)) {
                return null;
            }

            const candidate =
                new Candidate({
                    target:
                        canonical,

                    type,

                    origin:
                        originOf(canonical),

                    parent:
                        options.parent ||
                        null,

                    priority:
                        Number.isFinite(
                            options.priority
                        )
                            ? options.priority
                            : 0,

                    hints:
                        options.hints || {},

                    depth:
                        Number.isFinite(
                            options.depth
                        )
                            ? options.depth
                            : 0
                });

            const stored =
                this.db.addCandidate(
                    candidate,
                    options.discovery ||
                        null
                );

            if (!stored) {
                return null;
            }

            this.db.queueCandidate(
                stored
            );

            this.ledger
                .recordCandidateDiscovered(
                    stored,
                    options.discovery ||
                        null
                );

            this.ledger
                .recordCandidateEnqueued(
                    stored
                );

            this.db.ensureResource(
                stored.target
            ).merge({
                type: stored.type,
                mechanism:
                    options.mechanism ||
                    'discovery',
                candidateIds: [
                    stored.id
                ]
            });

            this.schedulePersistence();

            return stored;
        }

        emitDiscovery(discovery) {
            this.db.addDiscovery(
                discovery
            );

            this.ledger.recordDiscovery(
                discovery
            );

            const target =
                discovery.targetUrl();

            if (!target) {
                return null;
            }

            const depth =
                Number.isFinite(
                    discovery.provenance?.depth
                )
                    ? discovery.provenance.depth +
                      1
                    : 1;

            const type =
                discovery.kind === 'api'
                    ? 'api'
                    : discovery.kind;

            const candidate =
                this.discover(
                    target,
                    type,
                    {
                        parent:
                            discovery.candidateId,

                        priority:
                            discovery.confidence,

                        depth,

                        hints:
                            discovery.provenance
                                ?.hints ||
                            {
                                confidence:
                                    discovery.confidence
                            },

                        discovery,

                        mechanism:
                            discovery.mechanism
                    }
                );

            return candidate;
        }

        /*
         * --------------------------------------------------------
         * ACQUISITION PLAN
         * --------------------------------------------------------
         */

        plan(candidate) {
            this.db.markPlanned(
                candidate
            );

            const plan =
                this.policy.plan(
                    candidate
                );

            this.ledger.recordPlan(
                plan
            );

            if (!plan.allowed) {
                this.ledger
                    .recordPolicyDenied(
                        plan
                    );

                this.ledger
                    .recordDiagnostic(
                        'policy-denied',
                        plan.serialize()
                    );
            }

            return plan;
        }

        /*
         * --------------------------------------------------------
         * REQUEST BUDGET
         * --------------------------------------------------------
         *
         * Synchronous reservation prevents several workers from
         * collectively exceeding maxRequests.
         * --------------------------------------------------------
         */

        reserveRequestSlot() {
            if (
                this.requestsReserved >=
                CONFIG.maxRequests
            ) {
                return false;
            }

            this.requestsReserved++;

            return true;
        }

        /*
         * --------------------------------------------------------
         * EXECUTION
         * --------------------------------------------------------
         */

        async executePlan(plan) {
            const candidate =
                this.db.candidates.get(
                    plan.candidateId
                );

            if (!candidate) {
                return;
            }

            if (
                !plan.allowed
            ) {
                this.db.markSkipped(
                    candidate,
                    plan.reason
                );

                this.ledger
                    .recordCandidateSkipped(
                        candidate,
                        plan.reason
                    );

                return;
            }

            if (
                !this.db.shouldAcquireResource(
                    plan.target
                )
            ) {
                this.ledger
                    .recordDiagnostic(
                        'resource-already-acquired',
                        {
                            candidateId:
                                candidate.id,
                            target:
                                plan.target
                        }
                    );

                this.db.markCompleted(
                    candidate
                );

                this.ledger
                    .recordCandidateCompleted(
                        candidate
                    );

                return;
            }

            if (
                !this.reserveRequestSlot()
            ) {
                this.ledger
                    .recordBudgetDenied(
                        candidate,
                        'global-request-budget'
                    );

                this.db.markSkipped(
                    candidate,
                    'global-request-budget'
                );

                this.ledger
                    .recordCandidateSkipped(
                        candidate,
                        'global-request-budget'
                    );

                return;
            }

            this.ledger.recordSlotGranted(
                plan
            );

            this.db.markAcquiring(
                candidate
            );

            const observation =
                await this.acquisition.execute(
                    plan,
                    this.ledger
                );

            this.db.recordObservation(
                observation
            );

            this.ledger
                .recordObservation(
                    observation
                );

            this.db.markObserved(
                candidate
            );

            if (
                observation.status !==
                'success'
            ) {
                const retried =
                    this.db.retryCandidate(
                        candidate,
                        observation.reason ||
                            observation.status
                    );

                if (retried) {
                    this.ledger.recordRetry(
                        candidate,
                        observation.reason ||
                            observation.status
                    );
                }

                this.onFailure();

                return;
            }

            this.onSuccess();

            const providers =
                this.providers.matching(
                    observation
                );

            if (!providers.length) {
                this.db.markCompleted(
                    candidate
                );

                this.ledger
                    .recordCandidateCompleted(
                        candidate
                    );

                return;
            }

            this.db.markRecognized(
                candidate
            );

            for (const provider of providers) {
                this.ledger.recordRecognition(
                    candidate,
                    observation,
                    provider.name
                );

                let discoveries = [];

                try {
                    discoveries =
                        await provider.recognize(
                            candidate,
                            observation
                        );
                } catch (error) {
                    this.ledger
                        .recordDiagnostic(
                            'provider-error',
                            {
                                provider:
                                    provider.name,
                                candidateId:
                                    candidate.id,
                                error:
                                    String(error)
                            }
                        );

                    continue;
                }

                for (
                    const discovery of
                    discoveries
                ) {
                    this.emitDiscovery(
                        discovery
                    );
                }
            }

            this.db.markExpanded(
                candidate
            );

            this.db.markCompleted(
                candidate
            );

            this.ledger
                .recordCandidateCompleted(
                    candidate
                );

            this.schedulePersistence();
        }

        /*
         * --------------------------------------------------------
         * WORKER LOOP
         * --------------------------------------------------------
         */

        async worker() {
            this.activeWorkers++;

            try {
                while (
                    this.running &&
                    !this.stopRequested
                ) {
                    if (this.paused) {
                        await sleep(100);
                        continue;
                    }

                    if (
                        this.requestsReserved >=
                        CONFIG.maxRequests
                    ) {
                        break;
                    }

                    const candidate =
                        this.db.claimNextCandidate();

                    if (!candidate) {
                        break;
                    }

                    this.ledger
                        .recordCandidateClaimed(
                            candidate
                        );

                    const plan =
                        this.plan(candidate);

                    if (!plan.allowed) {
                        this.db.markSkipped(
                            candidate,
                            plan.reason
                        );

                        this.ledger
                            .recordCandidateSkipped(
                                candidate,
                                plan.reason
                            );

                        continue;
                    }

                    await this.executePlan(
                        plan
                    );
                }
            } finally {
                this.activeWorkers--;

                if (
                    this.activeWorkers === 0 &&
                    this.running
                ) {
                    this.updateUI();
                }
            }
        }

        async start() {
            if (this.running) {
                return;
            }

            this.running = true;
            this.paused = false;
            this.stopRequested = false;

            this.ledger.recordDiagnostic(
                'scan-started'
            );

            const workers = [];

            for (
                let i = 0;
                i < this.currentConcurrency;
                i++
            ) {
                workers.push(
                    this.worker()
                );
            }

            await Promise.all(
                workers
            );

            if (
                this.stopRequested ||
                this.requestsReserved >=
                    CONFIG.maxRequests
            ) {
                this.running = false;
            }

            this.ledger.recordDiagnostic(
                'scan-finished',
                {
                    requests:
                        this.requestsReserved,
                    candidates:
                        this.db.candidates.size
                }
            );

            this.persist();
            this.updateUI();
        }

        pause() {
            this.paused = true;

            this.ledger.recordDiagnostic(
                'scan-paused'
            );

            this.updateUI();
        }

        resume() {
            this.paused = false;

            this.ledger.recordDiagnostic(
                'scan-resumed'
            );

            this.updateUI();

            if (
                !this.running
            ) {
                this.start();
            }
        }

        stop() {
            this.stopRequested = true;
            this.running = false;

            this.ledger.recordDiagnostic(
                'scan-stop-requested'
            );

            this.persist();
            this.updateUI();
        }

        /*
         * --------------------------------------------------------
         * ADAPTIVE CONTROL
         * --------------------------------------------------------
         */

        onSuccess() {
            this.consecutiveSuccesses++;
            this.consecutiveFailures = 0;

            if (
                !CONFIG.adaptive.enabled
            ) {
                return;
            }

            if (
                this.consecutiveSuccesses >=
                CONFIG.adaptive.successThreshold
            ) {
                const old =
                    this.currentConcurrency;

                this.currentConcurrency =
                    clamp(
                        this.currentConcurrency + 1,
                        CONFIG.adaptive
                            .minConcurrency,
                        CONFIG.concurrency
                    );

                this.consecutiveSuccesses = 0;

                if (
                    old !==
                    this.currentConcurrency
                ) {
                    this.ledger
                        .recordDiagnostic(
                            'adaptive-increase',
                            {
                                from: old,
                                to:
                                    this.currentConcurrency
                            }
                        );
                }
            }
        }

        onFailure() {
            this.consecutiveFailures++;
            this.consecutiveSuccesses = 0;

            if (
                !CONFIG.adaptive.enabled
            ) {
                return;
            }

            if (
                this.consecutiveFailures >=
                CONFIG.adaptive.failureThreshold
            ) {
                const old =
                    this.currentConcurrency;

                this.currentConcurrency =
                    clamp(
                        this.currentConcurrency - 1,
                        CONFIG.adaptive
                            .minConcurrency,
                        CONFIG.concurrency
                    );

                this.consecutiveFailures = 0;

                if (
                    old !==
                    this.currentConcurrency
                ) {
                    this.ledger
                        .recordDiagnostic(
                            'adaptive-decrease',
                            {
                                from: old,
                                to:
                                    this.currentConcurrency
                            }
                        );
                }
            }
        }

        /*
         * --------------------------------------------------------
         * NETWORK EVIDENCE
         * --------------------------------------------------------
         */

        recordNetworkEvent(event) {
            if (
                this.networkEvents.size >=
                CONFIG.maxNetworkEvents
            ) {
                return;
            }

            this.networkEvents.set(
                event.id,
                event
            );

            this.ledger
                .recordDiagnostic(
                    'network-observed',
                    {
                        eventId:
                            event.id,
                        api:
                            event.api,
                        method:
                            event.method,
                        url:
                            event.url,
                        initiatorType:
                            event.initiatorType ||
                            null
                    }
                );

            const resource =
                this.db.ensureResource(
                    event.url
                );

            if (resource) {
                resource.merge({
                    networkEventIds: [
                        event.id
                    ],
                    mechanism:
                        `network:${event.api}`
                });
            }
        }

        observeNetworkGet(event) {
            if (
                !CONFIG.discovery.network
            ) {
                return;
            }

            if (
                event.method !== 'GET'
            ) {
                return;
            }

            if (!event.url) {
                return;
            }

            const url =
                canonicalizeUrl(
                    event.finalUrl ||
                    event.url
                );

            if (!url) return;

            this.recordNetworkEvent(
                event
            );

            this.discover(
                url,
                looksLikeApiUrl(url)
                    ? 'api'
                    : 'network',
                {
                    priority: 0.65,
                    depth: 0,
                    hints: {
                        confidence: 0.70,
                        method: 'GET',
                        networkObserved: true
                    },
                    mechanism:
                        'network-get'
                }
            );
        }

        /*
         * --------------------------------------------------------
         * CURRENT PAGE
         * --------------------------------------------------------
         */

        observeCurrentPage() {
            this.discover(
                location.href,
                'url',
                {
                    priority: 1,
                    depth: 0,
                    hints: {
                        confidence: 1,
                        method: 'GET',
                        root: true
                    },
                    mechanism:
                        'current-page'
                }
            );
        }

        /*
         * --------------------------------------------------------
         * DOM MUTATION OBSERVER
         * --------------------------------------------------------
         */

        installMutationObserver() {
            if (
                typeof MutationObserver ===
                'undefined'
            ) {
                return;
            }

            let timer = null;

            const observer =
                new MutationObserver(
                    () => {
                        clearTimeout(timer);

                        timer =
                            setTimeout(
                                () =>
                                    this.observeCurrentDom(),
                                CONFIG.mutationDebounce
                            );
                    }
                );

            observer.observe(
                document.documentElement ||
                    document,
                {
                    subtree: true,
                    childList: true,
                    attributes: true,
                    attributeFilter: [
                        'href',
                        'src',
                        'action'
                    ]
                }
            );
        }

        observeCurrentDom() {
            for (
                const element of
                document.querySelectorAll(
                    'a[href], area[href]'
                )
            ) {
                this.discover(
                    element.href,
                    'url',
                    {
                        priority: 0.50,
                        depth: 1,
                        hints: {
                            method: 'GET'
                        },
                        mechanism:
                            'dom-observer-link'
                    }
                );
            }

            for (
                const element of
                document.querySelectorAll(
                    'script[src]'
                )
            ) {
                this.discover(
                    element.src,
                    'script',
                    {
                        priority: 0.45,
                        depth: 1,
                        hints: {
                            method: 'GET'
                        },
                        mechanism:
                            'dom-observer-script'
                    }
                );
            }

            for (
                const element of
                document.querySelectorAll(
                    'link[href]'
                )
            ) {
                this.discover(
                    element.href,
                    'resource',
                    {
                        priority: 0.40,
                        depth: 1,
                        hints: {
                            method: 'GET'
                        },
                        mechanism:
                            'dom-observer-link'
                    }
                );
            }
        }

        /*
         * --------------------------------------------------------
         * PERSISTENCE
         * --------------------------------------------------------
         */

        schedulePersistence() {
            if (!CONFIG.persistence) {
                return;
            }

            clearTimeout(
                this.persistenceTimer
            );

            this.persistenceTimer =
                setTimeout(
                    () => this.persist(),
                    CONFIG.persistenceDebounce
                );
        }

        persist() {
            if (!CONFIG.persistence) {
                return;
            }

            try {
                GM_setValue(
                    STORAGE_KEY,
                    JSON.stringify({
                        engine:
                            this.db.serialize(),

                        ledger:
                            this.ledger.export(),

                        requestsReserved:
                            this.requestsReserved,

                        currentConcurrency:
                            this.currentConcurrency
                    })
                );
            } catch (error) {
                this.db.recordDiagnostic(
                    'persistence-error',
                    {
                        error:
                            String(error)
                    }
                );
            }
        }

        restore() {
            if (!CONFIG.persistence) {
                return;
            }

            try {
                const raw =
                    GM_getValue(
                        STORAGE_KEY,
                        null
                    );

                if (!raw) {
                    return;
                }

                const data =
                    typeof raw === 'string'
                        ? JSON.parse(raw)
                        : raw;

                /*
                 * v6 -> v7 migration is intentionally additive.
                 *
                 * Candidate records are retained.
                 * Existing persistence does not contain a ledger,
                 * so a new ledger begins here.
                 */

                if (
                    data.engine?.version >= 6
                ) {
                    this.db.restore(
                        data.engine
                    );
                }

                if (data.ledger) {
                    this.ledger.restore(
                        data.ledger
                    );
                }

                /*
                 * Do not restore the old request counter blindly.
                 *
                 * A new browser execution gets a fresh execution
                 * budget.
                 */

                this.requestsReserved = 0;

                this.currentConcurrency =
                    clamp(
                        Number(
                            data.currentConcurrency ||
                            CONFIG.concurrency
                        ),
                        CONFIG.adaptive
                            .minConcurrency,
                        CONFIG.concurrency
                    );
            } catch (error) {
                warn(
                    'Restore failed',
                    error
                );
            }
        }

        /*
         * --------------------------------------------------------
         * EXPORT
         * --------------------------------------------------------
         */

        exportData() {
            return {
                schema: 'gde-export-v7.1',

                exportedAt:
                    new Date().toISOString(),

                config: {
                    ...CONFIG
                },

                engine:
                    this.db.serialize(),

                ledger:
                    this.ledger.export(),

                networkEvents:
                    [
                        ...this.networkEvents.values()
                    ],

                diagnostics:
                    this.db.diagnostics.slice()
            };
        }

        /*
         * --------------------------------------------------------
         * UI
         * --------------------------------------------------------
         */

        installUI() {
            if (this.ui) {
                return;
            }

            const panel =
                document.createElement(
                    'div'
                );

            panel.style.cssText = `
                position:fixed;
                right:12px;
                bottom:12px;
                z-index:2147483647;
                background:#111;
                color:#eee;
                border:1px solid #555;
                border-radius:6px;
                padding:10px;
                font:12px/1.4 monospace;
                min-width:230px;
                box-shadow:0 4px 20px rgba(0,0,0,.35);
            `;

            const stats =
                document.createElement(
                    'div'
                );

            stats.style.marginBottom =
                '8px';

            const buttons =
                document.createElement(
                    'div'
                );

            buttons.style.display =
                'flex';

            buttons.style.gap =
                '4px';

            const button =
                (label, handler) => {
                    const el =
                        document.createElement(
                            'button'
                        );

                    el.textContent =
                        label;

                    el.style.cssText = `
                        font:11px monospace;
                        padding:4px 7px;
                        cursor:pointer;
                    `;

                    el.addEventListener(
                        'click',
                        handler
                    );

                    buttons.appendChild(
                        el
                    );

                    return el;
                };

            button(
                'Scan',
                () => this.start()
            );

            button(
                'Pause',
                () => {
                    if (this.paused) {
                        this.resume();
                    } else {
                        this.pause();
                    }
                }
            );

            button(
                'Stop',
                () => this.stop()
            );

            button(
                'Clear',
                () => {
                    if (
                        confirm(
                            'Clear persisted discovery state?'
                        )
                    ) {
                        GM_setValue(
                            STORAGE_KEY,
                            null
                        );

                        location.reload();
                    }
                }
            );

            button(
                'Export',
                () => {
                    const data =
                        this.exportData();

                    const blob =
                        new Blob(
                            [
                                JSON.stringify(
                                    data,
                                    null,
                                    2
                                )
                            ],
                            {
                                type:
                                    'application/json'
                            }
                        );

                    const url =
                        URL.createObjectURL(
                            blob
                        );

                    const anchor =
                        document.createElement(
                            'a'
                        );

                    anchor.href = url;

                    anchor.download =
                        `gde-${Date.now()}.json`;

                    anchor.click();

                    setTimeout(
                        () =>
                            URL.revokeObjectURL(
                                url
                            ),
                        1000
                    );
                }
            );

            panel.appendChild(
                stats
            );

            panel.appendChild(
                buttons
            );

            (
                document.body ||
                document.documentElement
            )?.appendChild(panel);

            this.ui = {
                panel,
                stats
            };

            this.updateUI();
        }

        updateUI() {
            if (!this.ui) {
                return;
            }

            const s =
                this.db.stats;

            this.ui.stats.textContent =
                [
                    `GDE v${CONFIG.version}`,
                    `state=${
                        this.stopRequested
                            ? 'stopped'
                            : this.paused
                                ? 'paused'
                                : this.running
                                    ? 'running'
                                    : 'idle'
                    }`,
                    `candidates=${this.db.candidates.size}`,
                    `queued=${
                        [...this.db.candidates.values()]
                            .filter(
                                c =>
                                    c.status ===
                                    'queued'
                            ).length
                    }`,
                    `active=${this.activeWorkers}`,
                    `requests=${this.requestsReserved}/${CONFIG.maxRequests}`,
                    `concurrency=${this.currentConcurrency}`,
                    `acquired=${s.acquired}`,
                    `recognized=${s.recognized}`,
                    `expanded=${s.expanded}`,
                    `completed=${s.completed}`,
                    `skipped=${s.skipped}`,
                    `failed=${s.failed}`,
                    `ledger=${this.ledger.events.length}`
                ].join('\n');
        }
    }
