// src/engine.js — AcquisitionPlan, AcquisitionPolicy, OriginController, Acquisition, NetworkObserver, GenericDiscoveryEngine

// --- 681-754 ---
    class AcquisitionPlan {
        constructor(data = {}) {
            this.id = data.id || makeId('plan');

            this.candidateId =
                data.candidateId || null;

            this.target =
                data.target || '';

            this.method =
                String(data.method || 'GET').toUpperCase();

            this.allowed =
                Boolean(data.allowed);

            this.reason =
                data.reason || null;

            this.priority =
                Number.isFinite(data.priority)
                    ? data.priority
                    : 0;

            this.origin =
                data.origin || originOf(this.target);

            this.expectedType =
                data.expectedType || 'unknown';

            this.requiresOriginSlot =
                data.requiresOriginSlot !== false;

            this.createdAt =
                data.createdAt || now();

            this.policyVersion =
                data.policyVersion || CONFIG.version;

            this.policyInputs =
                data.policyInputs || {};
        }

        serialize() {
            return {
                id: this.id,
                candidateId: this.candidateId,
                target: this.target,
                method: this.method,
                allowed: this.allowed,
                reason: this.reason,
                priority: this.priority,
                origin: this.origin,
                expectedType: this.expectedType,
                requiresOriginSlot: this.requiresOriginSlot,
                createdAt: this.createdAt,
                policyVersion: this.policyVersion,
                policyInputs: this.policyInputs
            };
        }
    }

    /*
     * ============================================================
     * DETERMINISTIC EVENT LEDGER
     * ============================================================
     *
     * The ledger records decisions and transitions.
     *
     * It does not claim that network execution is deterministic.
     * ============================================================
     */


// --- 2102-2244 ---
    class AcquisitionPolicy {
        plan(candidate) {
            const method =
                String(
                    candidate.hints?.method ||
                    'GET'
                ).toUpperCase();

            const base = {
                candidateId: candidate.id,
                target: candidate.target,
                method,
                priority:
                    candidate.effectivePriority(),
                origin: candidate.origin,
                expectedType: candidate.type,
                policyInputs: {
                    candidateType: candidate.type,
                    hints: {
                        ...candidate.hints
                    }
                }
            };

            if (!isAllowedUrl(candidate.target)) {
                return new AcquisitionPlan({
                    ...base,
                    allowed: false,
                    reason: 'url-not-allowed'
                });
            }

            if (method !== 'GET') {
                return new AcquisitionPlan({
                    ...base,
                    allowed: false,
                    reason: 'non-get-method'
                });
            }

            if (
                candidate.depth >
                CONFIG.maxDepth
            ) {
                return new AcquisitionPlan({
                    ...base,
                    allowed: false,
                    reason: 'max-depth'
                });
            }

            if (
                candidate.type === 'form' &&
                !CONFIG.policy.acquireForms
            ) {
                return new AcquisitionPlan({
                    ...base,
                    allowed: false,
                    reason: 'forms-disabled'
                });
            }

            if (
                candidate.type === 'media' &&
                !CONFIG.policy.acquireMedia
            ) {
                return new AcquisitionPlan({
                    ...base,
                    allowed: false,
                    reason: 'media-disabled'
                });
            }

            if (
                candidate.type === 'frame' &&
                !CONFIG.policy.acquireFrames
            ) {
                return new AcquisitionPlan({
                    ...base,
                    allowed: false,
                    reason: 'frames-disabled'
                });
            }

            if (
                candidate.type === 'stylesheet' &&
                !CONFIG.policy.acquireStylesheets
            ) {
                return new AcquisitionPlan({
                    ...base,
                    allowed: false,
                    reason: 'stylesheets-disabled'
                });
            }

            if (
                candidate.type === 'script' &&
                !CONFIG.policy.acquireScripts
            ) {
                return new AcquisitionPlan({
                    ...base,
                    allowed: false,
                    reason: 'scripts-disabled'
                });
            }

            if (
                candidate.type === 'network' &&
                !CONFIG.policy.acquireNetworkGet
            ) {
                return new AcquisitionPlan({
                    ...base,
                    allowed: false,
                    reason: 'network-get-disabled'
                });
            }

            if (
                candidate.hints?.binary &&
                !CONFIG.policy.acquireBinaryResources
            ) {
                return new AcquisitionPlan({
                    ...base,
                    allowed: false,
                    reason: 'binary-disabled'
                });
            }

            return new AcquisitionPlan({
                ...base,
                allowed: true,
                reason: null
            });
        }
    }

    /*
     * ============================================================
     * ORIGIN CONTROL
     * ============================================================
     */


// --- 2244-2337 ---
    class OriginController {
        constructor() {
            this.states = new Map();
        }

        state(origin) {
            if (!this.states.has(origin)) {
                this.states.set(origin, {
                    active: 0,
                    requests: 0,
                    lastRequestAt: 0
                });
            }

            return this.states.get(origin);
        }

        canReserve(origin) {
            const state =
                this.state(origin);

            if (
                state.requests >=
                CONFIG.origin.maxRequestsPerOrigin
            ) {
                return false;
            }

            if (
                state.active >=
                CONFIG.origin.maxConcurrentPerOrigin
            ) {
                return false;
            }

            return true;
        }

        async acquire(origin) {
            while (true) {
                const state =
                    this.state(origin);

                if (
                    state.requests >=
                    CONFIG.origin.maxRequestsPerOrigin
                ) {
                    return false;
                }

                if (
                    state.active <
                    CONFIG.origin.maxConcurrentPerOrigin
                ) {
                    const elapsed =
                        now() -
                        state.lastRequestAt;

                    const wait =
                        CONFIG.origin.minRequestInterval -
                        elapsed;

                    if (wait > 0) {
                        await sleep(wait);
                        continue;
                    }

                    state.active++;
                    state.requests++;
                    state.lastRequestAt = now();

                    return true;
                }

                await sleep(50);
            }
        }

        release(origin) {
            const state =
                this.state(origin);

            state.active =
                Math.max(0, state.active - 1);
        }
    }

    /*
     * ============================================================
     * ACQUISITION
     * ============================================================
     */


// --- 2337-2786 ---
    class Acquisition {
        constructor(originController) {
            this.origins =
                originController;
        }

        async execute(plan, ledger) {
            const startedAt = now();

            ledger.recordRequestStarted(plan);

            const originGranted =
                await this.origins.acquire(
                    plan.origin
                );

            if (!originGranted) {
                const observation =
                    new Observation({
                        candidateId:
                            plan.candidateId,
                        planId: plan.id,
                        target: plan.target,
                        requestedUrl:
                            plan.target,
                        startedAt,
                        completedAt: now(),
                        status: 'skipped',
                        reason:
                            'origin-request-budget'
                    });

                ledger.recordRequestCompleted(
                    plan,
                    observation
                );

                return observation;
            }

            try {
                return await this.request(
                    plan,
                    startedAt,
                    ledger
                );
            } finally {
                this.origins.release(
                    plan.origin
                );
            }
        }

        async request(plan, startedAt, ledger) {
            if (
                typeof GM_xmlhttpRequest ===
                'function'
            ) {
                return new Promise(resolve => {
                    let finished = false;

                    const finish =
                        observation => {
                            if (finished) return;

                            finished = true;

                            ledger.recordRequestCompleted(
                                plan,
                                observation
                            );

                            resolve(observation);
                        };

                    const timeoutId =
                        setTimeout(() => {
                            finish(
                                new Observation({
                                    candidateId:
                                        plan.candidateId,
                                    planId: plan.id,
                                    target:
                                        plan.target,
                                    requestedUrl:
                                        plan.target,
                                    startedAt,
                                    completedAt:
                                        now(),
                                    status: 'timeout',
                                    reason:
                                        'request-timeout'
                                })
                            );
                        }, CONFIG.requestTimeout);

                    try {
                        GM_xmlhttpRequest({
                            method: plan.method,
                            url: plan.target,
                            timeout:
                                CONFIG.requestTimeout,

                            onload: response => {
                                clearTimeout(timeoutId);

                                let body =
                                    String(
                                        response.responseText ||
                                        ''
                                    );

                                let bodyTruncated =
                                    false;

                                if (
                                    body.length >
                                    CONFIG.maxBodyChars
                                ) {
                                    body =
                                        body.slice(
                                            0,
                                            CONFIG.maxBodyChars
                                        );

                                    bodyTruncated = true;
                                }

                                const observation =
                                    new Observation({
                                        candidateId:
                                            plan.candidateId,

                                        planId:
                                            plan.id,

                                        target:
                                            plan.target,

                                        requestedUrl:
                                            plan.target,

                                        startedAt,

                                        completedAt:
                                            now(),

                                        status:
                                            response.status >=
                                                200 &&
                                            response.status <
                                                400
                                                ? 'success'
                                                : 'http-error',

                                        http: {
                                            status:
                                                response.status,

                                            contentType:
                                                response.responseHeaders
                                                    ?.match(
                                                        /content-type:\s*([^\r\n]+)/i
                                                    )?.[1]
                                                    ?.trim() ||
                                                '',

                                            contentLength:
                                                response.responseHeaders
                                                    ?.match(
                                                        /content-length:\s*(\d+)/i
                                                    )?.[1] ||
                                                null,

                                            headers: (() => {
                                                const h = {};
                                                for (const line of String(
                                                    response.responseHeaders || ''
                                                ).split(/\r?\n/)) {
                                                    const idx =
                                                        line.indexOf(':');
                                                    if (idx > 0) {
                                                        h[
                                                            line
                                                                .slice(
                                                                    0,
                                                                    idx
                                                                )
                                                                .trim()
                                                                .toLowerCase()
                                                        ] =
                                                            line
                                                                .slice(
                                                                    idx + 1
                                                                )
                                                                .trim();
                                                    }
                                                }
                                                return h;
                                            })(),

                                            finalUrl:
                                                response.finalUrl ||
                                                plan.target
                                        },

                                        body,
                                        bodyTruncated,

                                        fingerprint:
                                            makeFingerprint(
                                                body
                                            )
                                    });

                                finish(observation);
                            },

                            ontimeout: () => {
                                clearTimeout(timeoutId);

                                finish(
                                    new Observation({
                                        candidateId:
                                            plan.candidateId,
                                        planId: plan.id,
                                        target: plan.target,
                                        requestedUrl:
                                            plan.target,
                                        startedAt,
                                        completedAt:
                                            now(),
                                        status: 'timeout',
                                        reason:
                                            'request-timeout'
                                    })
                                );
                            },

                            onerror: error => {
                                clearTimeout(timeoutId);

                                finish(
                                    new Observation({
                                        candidateId:
                                            plan.candidateId,
                                        planId: plan.id,
                                        target: plan.target,
                                        requestedUrl:
                                            plan.target,
                                        startedAt,
                                        completedAt:
                                            now(),
                                        status: 'error',
                                        reason:
                                            'request-error',
                                        errors: [
                                            String(
                                                error?.error ||
                                                'unknown-error'
                                            )
                                        ]
                                    })
                                );
                            }
                        });
                    } catch (error) {
                        clearTimeout(timeoutId);

                        finish(
                            new Observation({
                                candidateId:
                                    plan.candidateId,
                                planId: plan.id,
                                target: plan.target,
                                requestedUrl:
                                    plan.target,
                                startedAt,
                                completedAt:
                                    now(),
                                status: 'error',
                                reason:
                                    'request-exception',
                                errors: [
                                    String(error)
                                ]
                            })
                        );
                    }
                });
            }

            /*
             * Fetch fallback.
             *
             * IMPORTANT:
             * AbortController is used so a timeout does not leave
             * an uncontrolled fetch alive.
             */

            const controller =
                new AbortController();

            const timeoutId =
                setTimeout(
                    () => controller.abort(),
                    CONFIG.requestTimeout
                );

            try {
                const response =
                    await fetch(
                        plan.target,
                        {
                            method: plan.method,
                            credentials: 'same-origin',
                            redirect: CONFIG.sameOriginOnly ? 'error' : 'follow',
                            signal:
                                controller.signal
                        }
                    );

                let body =
                    await response.text();

                let bodyTruncated = false;

                if (
                    body.length >
                    CONFIG.maxBodyChars
                ) {
                    body =
                        body.slice(
                            0,
                            CONFIG.maxBodyChars
                        );

                    bodyTruncated = true;
                }

                const observation =
                    new Observation({
                        candidateId:
                            plan.candidateId,

                        planId:
                            plan.id,

                        target:
                            plan.target,

                        requestedUrl:
                            plan.target,

                        startedAt,

                        completedAt:
                            now(),

                        status:
                            response.ok
                                ? 'success'
                                : 'http-error',

                        http: {
                            status:
                                response.status,

                            contentType:
                                response.headers.get(
                                    'content-type'
                                ) || '',

                            contentLength:
                                response.headers.get(
                                    'content-length'
                                ),

                            headers: Object.fromEntries(
                                [...response.headers.entries()].map(
                                    ([k, v]) => [
                                        k.toLowerCase(),
                                        v
                                    ]
                                )
                            ),

                            finalUrl:
                                response.url ||
                                plan.target
                        },

                        body,
                        bodyTruncated,

                        fingerprint:
                            makeFingerprint(body)
                    });

                ledger.recordRequestCompleted(
                    plan,
                    observation
                );

                return observation;
            } catch (error) {
                const observation =
                    new Observation({
                        candidateId:
                            plan.candidateId,
                        planId: plan.id,
                        target: plan.target,
                        requestedUrl:
                            plan.target,
                        startedAt,
                        completedAt: now(),
                        status:
                            error?.name ===
                            'AbortError'
                                ? 'timeout'
                                : 'error',
                        reason:
                            error?.name ===
                            'AbortError'
                                ? 'request-timeout'
                                : 'request-error',
                        errors: [
                            String(error)
                        ]
                    });

                ledger.recordRequestCompleted(
                    plan,
                    observation
                );

                return observation;
            } finally {
                clearTimeout(timeoutId);
            }
        }
    }

    /*
     * ============================================================
     * PROVIDER BASE
     * ============================================================
     */


// --- 3770-4266 ---
    class NetworkObserver {
        constructor(engine) {
            this.engine = engine;
            this.started = false;
            this.performanceObserver = null;
        }

        start() {
            if (this.started) return;

            this.started = true;

            if (CONFIG.networkBridge) {
                this.installBridge();
            }

            if (
                CONFIG.discovery.performance &&
                typeof PerformanceObserver !==
                    'undefined'
            ) {
                this.installPerformanceObserver();
            }
        }

        installBridge() {
            try {
                const script =
                    document.createElement(
                        'script'
                    );

                const __gdeBridgeSource = `(function () {
    if (window.__GDE_NETWORK_BRIDGE__) return;
    window.__GDE_NETWORK_BRIDGE__ = true;

    function emit(event) {
        window.postMessage({
            source: 'generic-discovery-engine',
            type: 'network',
            event: event
        }, '*');
    }

    const originalFetch = window.fetch;

    if (originalFetch) {
        window.fetch = async function (
            input,
            init
        ) {
            const requestAt =
                Date.now();

            const url =
                typeof input === 'string'
                    ? input
                    : input?.url;

            const method =
                String(
                    init?.method ||
                    input?.method ||
                    'GET'
                ).toUpperCase();

            const requestId =
                'fetch-' +
                requestAt +
                '-' +
                Math.random()
                    .toString(36)
                    .slice(2);

            emit({
                phase: 'request',
                api: 'fetch',
                requestId,
                method,
                url,
                requestAt
            });

            try {
                const response =
                    await originalFetch.apply(
                        this,
                        arguments
                    );

                emit({
                    phase: 'response',
                    api: 'fetch',
                    requestId,
                    method,
                    url,
                    finalUrl:
                        response.url,
                    status:
                        response.status,
                    contentType:
                        response.headers.get(
                            'content-type'
                        ) || '',
                    responseAt:
                        Date.now()
                });

                return response;
            } catch (error) {
                emit({
                    phase: 'error',
                    api: 'fetch',
                    requestId,
                    method,
                    url,
                    error:
                        String(error),
                    responseAt:
                        Date.now()
                });

                throw error;
            }
        };
    }

    const OriginalXHR =
        window.XMLHttpRequest;

    if (OriginalXHR) {
        const open =
            OriginalXHR.prototype.open;

        const send =
            OriginalXHR.prototype.send;

        OriginalXHR.prototype.open =
            function (
                method,
                url
            ) {
                this.__gde = {
                    method:
                        String(
                            method || 'GET'
                        ).toUpperCase(),
                    url,
                    requestId:
                        'xhr-' +
                        Date.now() +
                        '-' +
                        Math.random()
                            .toString(36)
                            .slice(2)
                };

                return open.apply(
                    this,
                    arguments
                );
            };

        OriginalXHR.prototype.send =
            function () {
                const meta =
                    this.__gde;

                if (meta) {
                    emit({
                        phase: 'request',
                        api: 'xhr',
                        requestId:
                            meta.requestId,
                        method:
                            meta.method,
                        url:
                            meta.url,
                        requestAt:
                            Date.now()
                    });

                    this.addEventListener(
                        'load',
                        function () {
                            emit({
                                phase:
                                    'response',
                                api: 'xhr',
                                requestId:
                                    meta.requestId,
                                method:
                                    meta.method,
                                url:
                                    meta.url,
                                finalUrl:
                                    this.responseURL ||
                                    meta.url,
                                status:
                                    this.status,
                                contentType:
                                    this.getResponseHeader(
                                        'content-type'
                                    ) || '',
                                responseAt:
                                    Date.now()
                            });
                        }
                    );

                    this.addEventListener(
                        'error',
                        function () {
                            emit({
                                phase:
                                    'error',
                                api: 'xhr',
                                requestId:
                                    meta.requestId,
                                method:
                                    meta.method,
                                url:
                                    meta.url,
                                error:
                                    'xhr-error',
                                responseAt:
                                    Date.now()
                            });
                        }
                    );
                }

                return send.apply(
                    this,
                    arguments
                );
            };
    }
})();
`;
                // Trusted Types compliance (gde-bridge policy) — S-02 residual
                try {
                    if (window.trustedTypes?.createPolicy) {
                        const __gdePolicy = window.trustedTypes.createPolicy('gde-bridge', {
                            createScript: s => s
                        });
                        // @ts-ignore TrustedScript
                        script.textContent = __gdePolicy.createScript(__gdeBridgeSource);
                    } else {
                        script.textContent = __gdeBridgeSource;
                    }
                } catch {
                    script.textContent = __gdeBridgeSource;
                }

                (
                    document.documentElement ||
                    document.head ||
                    document.body
                )?.appendChild(script);

                script.remove();

                window.addEventListener(
                    'message',
                    event => {
                        if (
                            event.source !== window
                        ) {
                            return;
                        }

                        if (
                            event.data?.source !==
                            'generic-discovery-engine'
                        ) {
                            return;
                        }

                        if (
                            event.data?.type !==
                            'network'
                        ) {
                            return;
                        }

                        this.handleBridgeEvent(
                            event.data.event
                        );
                    }
                );
            } catch (error) {
                const msg = String(error);
                this.engine.ledger
                    .recordDiagnostic(
                        'network-bridge-error',
                        {
                            error: msg
                        }
                    );
                if (
                    /Content[- ]Security[- ]Policy|CSP|Refused to execute/i.test(
                        msg
                    )
                ) {
                    this.engine.ledger.recordDiagnostic(
                        'csp-blocks-bridge',
                        {
                            error: msg,
                            hint: 'page CSP blocks inline script; network bridge disabled, PerformanceObserver remains'
                        }
                    );
                }
            }
        }

        handleBridgeEvent(event) {
            if (!event) return;

            const key =
                event.requestId;

            if (!key) return;

            // Centralize through recordNetworkEvent to enforce maxNetworkEvents cap (P1 hardening)
            const ev = {
                    id:
                        key,
                    requestId:
                        key,
                    api:
                        event.api,
                    method:
                        event.method,
                    url:
                        event.url,
                    finalUrl:
                        event.finalUrl ||
                        null,
                    status:
                        event.status ||
                        0,
                    contentType:
                        event.contentType ||
                        '',
                    requestAt:
                        event.requestAt ||
                        now(),
                    responseAt:
                        event.responseAt ||
                        null,
                    phase:
                        event.phase,
                    error:
                        event.error ||
                        null
                };
            this.engine.recordNetworkEvent(ev);

            const networkEvent =
                this.engine.networkEvents.get(
                    key
                ) || ev;

            if (
                networkEvent.phase ===
                    'response' &&
                networkEvent.method ===
                    'GET' &&
                networkEvent.url
            ) {
                this.engine.observeNetworkGet(
                    networkEvent
                );
            }
        }

        installPerformanceObserver() {
            try {
                this.performanceObserver =
                    new PerformanceObserver(
                        entries => {
                            for (
                                const entry of
                                entries.getEntries()
                            ) {
                                if (
                                    !entry.name
                                ) {
                                    continue;
                                }

                                const initiator =
                                    entry.initiatorType ||
                                    'unknown';

                                /*
                                 * We intentionally do NOT assume
                                 * fetch/xhr == GET here.
                                 *
                                 * They are evidence only unless
                                 * the bridge provides method data.
                                 */
                                const executableGetLike =
                                    ![
                                        'fetch',
                                        'xmlhttprequest'
                                    ].includes(
                                        initiator
                                    );

                                const event = {
                                    id:
                                        makeId(
                                            'perf'
                                        ),

                                    requestId:
                                        makeId(
                                            'perf-request'
                                        ),

                                    api:
                                        'performance',

                                    method:
                                        executableGetLike
                                            ? 'GET'
                                            : null,

                                    url:
                                        entry.name,

                                    finalUrl:
                                        entry.name,

                                    status:
                                        0,

                                    contentType:
                                        '',

                                    initiatorType:
                                        initiator,

                                    requestAt:
                                        now(),

                                    responseAt:
                                        now(),

                                    duration:
                                        entry.duration,

                                    phase:
                                        'performance'
                                };

                                this.engine.recordNetworkEvent(
                                    event
                                );

                                if (
                                    executableGetLike
                                ) {
                                    this.engine.observeNetworkGet(
                                        event
                                    );
                                }
                            }
                        }
                    );

                this.performanceObserver.observe({
                    entryTypes: ['resource']
                });
            } catch (error) {
                this.engine.ledger
                    .recordDiagnostic(
                        'performance-observer-error',
                        {
                            error:
                                String(error)
                        }
                    );
            }
        }
    }

    /*
     * ============================================================
     * ENGINE
     * ============================================================
     */


// --- 4266-5864 ---
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
            this._uiRaf = null;
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

            if (!CONFIG.sameOriginOnly) {
                this.ledger.recordDiagnostic(
                    'config-cross-origin-requires-connect-star',
                    {
                        sameOriginOnly: false,
                        hint: 'set @connect * for cross-origin fetch'
                    }
                );
                warn(
                    'sameOriginOnly=false — ensure @connect * is enabled'
                );
            }

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

            // v0.9.1: revisitChanged — re-queue changed resource (opt-in, clears visited)
            if (CONFIG.revisitChanged) {
                try {
                    const revisitUrl = canonicalizeUrl(observation.requestedUrl) || observation.requestedUrl;
                    const res = this.db.resources.get(revisitUrl);
                    if (res && res.status === 'changed') {
                        const revisitKey = `url:${revisitUrl}`;
                        this.db.visited.delete(revisitKey);
                        this.db.candidateKeys.delete(revisitKey);
                        const revisit = this.discover(observation.requestedUrl, 'url', {
                            priority: 0.6,
                            depth: candidate.depth,
                            hints: { confidence: 0.7, revisit: true },
                            mechanism: 'revisit-changed'
                        });
                        if (revisit) {
                            this.ledger.recordDiagnostic('revisit-queued', { target: observation.requestedUrl, candidateId: revisit.id });
                        }
                    }
                } catch {}
            }

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

            // P1-1: per-observation cross-provider dedup (sequential vs concurrent via CONFIG.providers.concurrent)
            const emittedForObservation =
                new Set();
            const processDiscoveries = (discoveries, providerName) => {
                for (const discovery of discoveries) {
                    const dedupKey = discovery.targetUrl();
                    if (dedupKey && emittedForObservation.has(dedupKey)) {
                        this.ledger.recordDiagnostic('discovery-deduped', { url: dedupKey, provider: providerName });
                        continue;
                    }
                    if (dedupKey) emittedForObservation.add(dedupKey);
                    this.emitDiscovery(discovery);
                }
            };
            if (CONFIG.providers?.concurrent) {
                const results = await Promise.all(providers.map(async (provider) => {
                    this.ledger.recordRecognition(candidate, observation, provider.name);
                    try {
                        const discoveries = await provider.recognize(candidate, observation);
                        return { provider: provider.name, discoveries };
                    } catch (error) {
                        this.ledger.recordDiagnostic('provider-error', { provider: provider.name, candidateId: candidate.id, error: String(error) });
                        return { provider: provider.name, discoveries: [] };
                    }
                }));
                for (const { provider: name, discoveries } of results) {
                    processDiscoveries(discoveries, name);
                }
            } else {
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

                    processDiscoveries(discoveries, provider.name);
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

            // v0.9.1: pattern-guided exploration (opt-in, bounded)
            if (CONFIG.patternGuided?.enabled) {
                try {
                    const suggestions = this.db.suggestPatternCandidates();
                    for (const { suggestion, pattern, count } of suggestions) {
                        const pc = this.discover(suggestion, 'url', {
                            priority: 0.55,
                            depth: candidate.depth + 1,
                            hints: { confidence: 0.6, patternGuided: true, pattern },
                            mechanism: 'pattern-guided'
                        });
                        if (pc) {
                            this.ledger.recordDiagnostic('pattern-guided-queued', { pattern, suggestion, count, candidateId: pc.id });
                        }
                    }
                } catch {}
            }

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

        // Adaptive concurrency is a *target* for the next scan's worker pool (not active workers mid-scan)
        // Workers are fixed at scan start; currentConcurrency is clamped and applied on next start()
        get concurrencyTarget() { return this.currentConcurrency; }
        set concurrencyTarget(v) { this.currentConcurrency = clamp(v, CONFIG.adaptive.minConcurrency, CONFIG.concurrency); }

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
                            'adaptive-target-increase',
                            {
                                from: old,
                                to:
                                    this.currentConcurrency,
                                activeWorkers: this.activeWorkers,
                                note: 'target for next scan; active workers unchanged mid-scan'
                            }
                        );
                    // keep legacy name for compat
                    this.ledger.recordDiagnostic('adaptive-increase', { from: old, to: this.currentConcurrency });
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
                            'adaptive-target-decrease',
                            {
                                from: old,
                                to:
                                    this.currentConcurrency,
                                activeWorkers: this.activeWorkers,
                                note: 'target for next scan; active workers unchanged mid-scan'
                            }
                        );
                    this.ledger.recordDiagnostic('adaptive-decrease', { from: old, to: this.currentConcurrency });
                }
            }
        }

        /*
         * --------------------------------------------------------
         * NETWORK EVIDENCE
         * --------------------------------------------------------
         */

        recordNetworkEvent(event) {
            // Enforce cap only for new keys; updates to existing requestId (bridge request→response) must not be dropped at cap
            if (
                !this.networkEvents.has(event.id) &&
                this.networkEvents.size >=
                CONFIG.maxNetworkEvents
            ) {
                // Evict oldest to make room (FIFO) rather than silently drop
                const first = this.networkEvents.keys().next().value;
                if (first) this.networkEvents.delete(first);
                // Also record diagnostic for observability
                this.ledger?.recordDiagnostic?.('network-events-evicted', { max: CONFIG.maxNetworkEvents });
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
            // P1-2: batch dedup within single mutation flush
            const seen = new Set();

            const tryDiscover = (
                target,
                type,
                priority,
                mechanism
            ) => {
                try {
                    const key = `${type}:${canonicalizeUrl(
                        target
                    )}`;
                    if (!key || seen.has(key)) return;
                    seen.add(key);
                } catch {
                    return;
                }

                this.discover(target, type, {
                    priority,
                    depth: 1,
                    hints: { method: 'GET' },
                    mechanism
                });
            };

            for (
                const element of
                document.querySelectorAll(
                    'a[href], area[href]'
                )
            ) {
                tryDiscover(
                    element.href,
                    'url',
                    0.50,
                    'dom-observer-link'
                );
            }

            for (
                const element of
                document.querySelectorAll(
                    'script[src]'
                )
            ) {
                tryDiscover(
                    element.src,
                    'script',
                    0.45,
                    'dom-observer-script'
                );
            }

            for (
                const element of
                document.querySelectorAll(
                    'link[href]'
                )
            ) {
                tryDiscover(
                    element.href,
                    'resource',
                    0.40,
                    'dom-observer-link'
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

        // P2-3: coverage/budget frontier metrics (added v0.7.3)
        getCoverageMetrics() {
            const all = [
                ...this.db.candidates.values()
            ];
            const queued =
                all.filter(
                    c =>
                        c.status ===
                        'queued'
                );
            const queuedByTypeUnsorted = {};
            for (const c of queued) {
                queuedByTypeUnsorted[c.type] =
                    (queuedByTypeUnsorted[c.type] ||
                        0) + 1;
            }
            // deterministic: sorted keys
            const queuedByType = {};
            for (const k of Object.keys(queuedByTypeUnsorted).sort()) {
                queuedByType[k] = queuedByTypeUnsorted[k];
            }
            const live = all.filter(
                c =>
                    ![
                        'completed',
                        'skipped'
                    ].includes(
                        c.status
                    )
            ).length;
            // inference metrics (O(n≤750) via KnowledgeBase, ~0.06ms)
            const patternMetrics = this.db.getPatternMetrics
                ? this.db.getPatternMetrics()
                : { size: 0, total: 0, top: [] };
            const clusterMetrics = this.db.getClusterMetrics
                ? this.db.getClusterMetrics()
                : { size: 0, total: 0, top: [] };
            const providerMetrics = this.getProviderMetrics();
            const providerInstances = this.providers?.getInstanceCount?.() ?? this.providers?.providers?.length ?? 0;
            return {
                frontierSize:
                    queued.length,
                queuedByType,
                liveCount: live,
                visitedSize:
                    this.db.visited.size,
                knownResources:
                    this.db.resources.size,
                totalCandidates:
                    all.length,
                requestsUsed:
                    this.requestsReserved,
                requestsRemaining:
                    Math.max(
                        0,
                        CONFIG.maxRequests -
                            this.requestsReserved
                    ),
                ledgerSize:
                    this.ledger.events.length,
                graphEdges:
                    this.db.graphEdges.length,
                observations:
                    this.db.observations.size,
                patternCount:
                    patternMetrics.size,
                clusterCount:
                    clusterMetrics.size,
                fingerprintUnique:
                    this.db.fingerprintIndex
                        ? this.db.fingerprintIndex.size
                        : 0,
                inferenceEnabled:
                    Boolean(
                        CONFIG.inference &&
                        CONFIG.inference
                            .patternInference
                    ),
                providerInstances,
                providerMetrics
            };
        }

        getProviderMetrics() {
            try {
                if (this.providers?.getMetrics) return this.providers.getMetrics();
                // fallback: synthesize from provider names
                const out = {};
                for (const p of (this.providers?.providers || [])) {
                    out[p.name] = { calls: 0, matches: 0, totalMs: 0, avgMs: 0 };
                }
                return out;
            } catch { return {}; }
        }

        getHealthMetrics() {
            try {
                const cov = this.getCoverageMetrics();
                const providerMetrics = cov.providerMetrics || this.getProviderMetrics();
                const slowThreshold = CONFIG.health?.slowProviderMs ?? 50;
                const slowProviders = Object.entries(providerMetrics)
                    .filter(([_, m]) => (m.avgMs ?? 0) > slowThreshold)
                    .map(([name, m]) => ({ name, avgMs: Number(m.avgMs.toFixed(2)), calls: m.calls, matches: m.matches }))
                    .sort((a,b)=>b.avgMs-a.avgMs);
                const maxErr = CONFIG.health?.maxRecentErrors ?? 20;
                const diagnosticCount = (this.db.diagnostics || []).length;
                const recentDiagnostics = (this.db.diagnostics || []).slice(-maxErr);
                const recentLedgerErrors = (this.ledger.events || []).filter(e => /error|illegal|failed|bridge/i.test(String(e.type||''))).slice(-5);
                const frontierPressure = cov.frontierSize / Math.max(1, CONFIG.maxCandidates);
                const requestPressure = cov.requestsUsed / Math.max(1, CONFIG.maxRequests);
                const ledgerPressure = cov.ledgerSize / 5000;
                let status = 'healthy';
                if (slowProviders.length > 2 || frontierPressure > 0.9 || requestPressure > 0.9 || cov.observations > 750) status = 'degraded';
                if (slowProviders.some(p=>p.avgMs>100) || cov.liveCount >= CONFIG.maxCandidates || diagnosticCount > maxErr) status = 'unhealthy';
                if (!CONFIG.health?.enabled) status = 'disabled';
                const configuredProviders = this.providers?.factories ? Object.keys(this.providers.factories).length : (this.providers?.order?.length ?? Object.keys(providerMetrics).length);
                const instantiatedProviders = Object.keys(providerMetrics).length;
                return {
                    status,
                    timestamp: new Date().toISOString(),
                    coverage: cov,
                    providerHealth: { slowProviders, totalProviders: configuredProviders, configuredProviders, instantiatedProviders, slowThresholdMs: slowThreshold, slowCount: slowProviders.length },
                    system: { frontierPressure: Number(frontierPressure.toFixed(3)), requestPressure: Number(requestPressure.toFixed(3)), ledgerPressure: Number(ledgerPressure.toFixed(3)), concurrency: this.currentConcurrency, adaptive: !!CONFIG.adaptive.enabled, healthEnabled: !!CONFIG.health?.enabled },
                    recentErrors: [...recentLedgerErrors, ...recentDiagnostics.slice(-5)].slice(-5)
                };
            } catch (e) {
                return { status: 'unknown', error: String(e), timestamp: new Date().toISOString() };
            }
        }

        exportData() {
            const coverage =
                this.getCoverageMetrics();
            // inference snapshot (bounded, top 20 already sorted)
            const inference = {
                enabled: Boolean(
                    CONFIG.inference &&
                    CONFIG.inference.patternInference
                ),
                patternMetrics:
                    this.db.getPatternMetrics
                        ? this.db.getPatternMetrics()
                        : {
                            size: 0,
                            total: 0,
                            top: []
                          },
                clusterMetrics:
                    this.db.getClusterMetrics
                        ? this.db.getClusterMetrics()
                        : {
                            size: 0,
                            total: 0,
                            top: []
                          },
                fingerprintStats: {
                    unique:
                        this.db.fingerprintIndex
                            ? this.db.fingerprintIndex.size
                            : 0,
                    total:
                        this.db.fingerprintIndex
                            ? [
                                ...this.db.fingerprintIndex.values()
                              ].reduce(
                                    (a, s) =>
                                        a + s.size,
                                    0
                                )
                            : 0
                }
            };
            const providers = {
                lazy: Boolean(CONFIG.providers?.lazy),
                disabled: [...(CONFIG.providers?.disabled || [])],
                concurrent: Boolean(CONFIG.providers?.concurrent),
                metrics: this.getProviderMetrics(),
                instanceCount: this.providers?.getInstanceCount?.() ?? 0
            };
            const health = this.getHealthMetrics();
            return {
                schema: 'gde-export-v8.0',

                exportedAt:
                    new Date().toISOString(),

                config: {
                    ...CONFIG
                },

                coverage,

                inference,

                providers,

                health,

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
            if (typeof requestAnimationFrame === 'function') {
                if (this._uiRaf) return;
                this._uiRaf = requestAnimationFrame(() => {
                    this._uiRaf = null;
                    this._doUpdateUI();
                });
                return;
            }
            this._doUpdateUI();
        }

        _doUpdateUI() {
            const s =
                this.db.stats;
            const cov =
                this.getCoverageMetrics();

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
                    `candidates=${this.db.candidates.size} (live ${cov.liveCount})`,
                    `queued=${cov.frontierSize} ${JSON.stringify(cov.queuedByType)}`,
                    `active=${this.activeWorkers}`,
                    `requests=${this.requestsReserved}/${CONFIG.maxRequests} (remain ${cov.requestsRemaining})`,
                    `concurrency=${this.currentConcurrency}`,
                    `visited=${cov.visitedSize} resources=${cov.knownResources}`,
                    `acquired=${s.acquired}`,
                    `recognized=${s.recognized}`,
                    `expanded=${s.expanded}`,
                    `completed=${s.completed}`,
                    `skipped=${s.skipped}`,
                    `failed=${s.failed}`,
                    `ledger=${this.ledger.events.length} edges=${cov.graphEdges} obs=${cov.observations}`
                ].join('\n');
        }
    }

    /*
     * ============================================================
     * BOOT
     * ============================================================
     */

    const engine =
        new GenericDiscoveryEngine();

    window.GenericDiscoveryEngine =
        engine;

    engine.init();

})();
