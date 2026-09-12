    class GenericDiscoveryEngine {
        constructor() {
            this.db =
                new KnowledgeBase();

            this.policy =
                new AcquisitionPolicy();

            this.origins =
                new OriginController();

            this.scheduler =
                new AdaptiveScheduler();

            this.providers =
                new ProviderRegistry();

            this.networkObserver =
                new NetworkObserver();

            this.running = false;
            this.paused = false;
            this.stopRequested = false;

            this.inFlight = 0;
            this.requestsStarted = 0;

            this.workerPromises = [];

            this.domObserver = null;
            this.mutationTimer = null;

            this.ui = null;
        }

        start() {
            if (this.running) {
                this.resume();
                return;
            }

            this.running = true;
            this.paused = false;
            this.stopRequested = false;

            this.networkObserver.start();

            this.seed();

            if (
                CONFIG.observeDomMutations
            ) {
                this.installDomObserver();
            }

            this.updateUI();

            this.workerPromises =
                Array.from(
                    {
                        length:
                            CONFIG.concurrency
                    },
                    (_, index) =>
                        this.worker(index)
                );

            Promise.allSettled(
                this.workerPromises
            ).then(() => {
                if (
                    this.running &&
                    !this.stopRequested
                ) {
                    this.running = false;
                }

                this.updateUI();
            });
        }

        pause() {
            if (!this.running) {
                return;
            }

            this.paused = true;

            this.db.recordDiagnostic(
                'pause',
                {}
            );

            this.updateUI();
        }

        resume() {
            if (!this.running) {
                this.start();
                return;
            }

            this.paused = false;

            this.db.recordDiagnostic(
                'resume',
                {}
            );

            this.updateUI();
        }

        stop() {
            this.stopRequested = true;
            this.paused = false;

            this.db.recordDiagnostic(
                'stop',
                {}
            );

            this.updateUI();
        }

        async waitUntilRunnable() {
            while (this.paused) {
                if (this.stopRequested) {
                    return false;
                }

                await sleep(100);
            }

            return !this.stopRequested;
        }

        reserveRequestSlot() {
            if (
                this.requestsStarted >=
                CONFIG.maxRequests
            ) {
                return false;
            }

            this.requestsStarted++;
            this.db.stats.requestsStarted++;

            return true;
        }

        enqueue(
            target,
            type = 'url',
            hints = {},
            parent = location.href,
            depth = 0
        ) {
            const canonical =
                canonicalizeUrl(
                    target,
                    parent
                );

            if (!canonical) {
                return null;
            }

            const candidate =
                new Candidate({
                    target: canonical,
                    type,
                    hints,
                    origin: location.href,
                    parent,
                    depth,
                    priority:
                        hints.priority ??
                        (
                            0.40 +
                            (
                                hints.confidence ||
                                0
                            ) * 0.50
                        )
                });

            return this.db.addCandidate(
                candidate
            );
        }

        seed() {
            const current =
                canonicalizeUrl(
                    location.href
                );

            this.enqueue(
                current,
                'url',
                {
                    mechanism: 'page-root',
                    confidence: 1,
                    priority: 1
                },
                null,
                0
            );

            if (
                CONFIG.discovery.wellKnown
            ) {
                this.enqueue(
                    new URL(
                        '/robots.txt',
                        location.origin
                    ).href,
                    'robots',
                    {
                        mechanism:
                            'well-known-robots',
                        confidence: 0.99,
                        priority: 0.96
                    },
                    current,
                    1
                );

                this.enqueue(
                    new URL(
                        '/sitemap.xml',
                        location.origin
                    ).href,
                    'sitemap',
                    {
                        mechanism:
                            'well-known-sitemap',
                        confidence: 0.92,
                        priority: 0.90
                    },
                    current,
                    1
                );
            }

            this.scanDocument(
                document,
                location.href,
                1,
                'initial-dom'
            );
        }

        scanDocument(
            doc,
            baseUrl,
            depth,
            mechanismPrefix
        ) {
            if (!doc) return;

            const enqueueElement =
                (
                    element,
                    attribute,
                    type,
                    mechanism,
                    confidence
                ) => {
                    const value =
                        element.getAttribute(
                            attribute
                        );

                    if (!value) return;

                    this.enqueue(
                        value,
                        type,
                        {
                            mechanism,
                            confidence
                        },
                        baseUrl,
                        depth
                    );
                };

            if (CONFIG.discovery.links) {
                for (
                    const element of
                    doc.querySelectorAll(
                        'a[href],area[href]'
                    )
                ) {
                    enqueueElement(
                        element,
                        'href',
                        'url',
                        `${mechanismPrefix}:link`,
                        0.82
                    );
                }
            }

            if (CONFIG.discovery.resources) {
                const resourceSelectors = [
                    [
                        'script[src]',
                        'src',
                        'script',
                        'script'
                    ],
                    [
                        'link[href]',
                        'href',
                        'stylesheet',
                        'stylesheet'
                    ],
                    [
                        'img[src]',
                        'src',
                        'media',
                        'image'
                    ],
                    [
                        'audio[src]',
                        'src',
                        'media',
                        'audio'
                    ],
                    [
                        'video[src]',
                        'src',
                        'media',
                        'video'
                    ],
                    [
                        'iframe[src]',
                        'src',
                        'frame',
                        'frame'
                    ],
                    [
                        'frame[src]',
                        'src',
                        'frame',
                        'frame'
                    ],
                    [
                        'object[data]',
                        'data',
                        'embedded',
                        'object'
                    ],
                    [
                        'embed[src]',
                        'src',
                        'embedded',
                        'embed'
                    ]
                ];

                for (
                    const [
                        selector,
                        attribute,
                        type,
                        name
                    ] of resourceSelectors
                ) {
                    for (
                        const element of
                        doc.querySelectorAll(
                            selector
                        )
                    ) {
                        enqueueElement(
                            element,
                            attribute,
                            type,
                            `${mechanismPrefix}:${name}`,
                            0.72
                        );
                    }
                }

                for (
                    const element of
                    doc.querySelectorAll(
                        'link[rel][href]'
                    )
                ) {
                    const rel =
                        (
                            element.getAttribute(
                                'rel'
                            ) || ''
                        ).toLowerCase();

                    let type =
                        'resource';

                    if (
                        rel.includes(
                            'manifest'
                        )
                    ) {
                        type = 'manifest';
                    } else if (
                        rel.includes(
                            'sitemap'
                        )
                    ) {
                        type = 'sitemap';
                    } else if (
                        rel.includes(
                            'feed'
                        ) ||
                        rel.includes(
                            'alternate'
                        )
                    ) {
                        type = 'feed';
                    }

                    enqueueElement(
                        element,
                        'href',
                        type,
                        `${mechanismPrefix}:link-rel:${rel}`,
                        0.82
                    );
                }
            }

            if (CONFIG.discovery.forms) {
                for (
                    const form of
                    doc.querySelectorAll(
                        'form[action]'
                    )
                ) {
                    enqueueElement(
                        form,
                        'action',
                        'form',
                        `${mechanismPrefix}:form`,
                        0.68
                    );
                }
            }
        }

        installDomObserver() {
            if (
                this.domObserver ||
                typeof MutationObserver ===
                'undefined'
            ) {
                return;
            }

            const install = () => {
                if (!document.body) {
                    setTimeout(
                        install,
                        250
                    );
                    return;
                }

                this.domObserver =
                    new MutationObserver(
                        mutations => {
                            const added =
                                [];

                            for (
                                const mutation of
                                mutations
                            ) {
                                for (
                                    const node of
                                    mutation.addedNodes
                                ) {
                                    if (
                                        node.nodeType ===
                                        Node.ELEMENT_NODE
                                    ) {
                                        added.push(
                                            node
                                        );
                                    }
                                }
                            }

                            if (!added.length) {
                                return;
                            }

                            clearTimeout(
                                this.mutationTimer
                            );

                            this.mutationTimer =
                                setTimeout(() => {
                                    for (
                                        const node of
                                        added
                                    ) {
                                        this.scanMutationNode(
                                            node
                                        );
                                    }
                                },
                                CONFIG.mutationDebounce
                            );
                        }
                    );

                this.domObserver.observe(
                    document.body,
                    {
                        childList: true,
                        subtree: true
                    }
                );
            };

            install();
        }

        scanMutationNode(node) {
            const base =
                location.href;

            const selectors = [
                [
                    'a[href]',
                    'href',
                    'url',
                    'mutation-link'
                ],
                [
                    'script[src]',
                    'src',
                    'script',
                    'mutation-script'
                ],
                [
                    'link[href]',
                    'href',
                    'stylesheet',
                    'mutation-stylesheet'
                ],
                [
                    'img[src]',
                    'src',
                    'media',
                    'mutation-image'
                ],
                [
                    'iframe[src]',
                    'src',
                    'frame',
                    'mutation-frame'
                ],
                [
                    'form[action]',
                    'action',
                    'form',
                    'mutation-form'
                ]
            ];

            for (
                const [
                    selector,
                    attribute,
                    type,
                    mechanism
                ] of selectors
            ) {
                if (
                    node.matches?.(selector)
                ) {
                    const value =
                        node.getAttribute(
                            attribute
                        );

                    if (value) {
                        this.enqueue(
                            value,
                            type,
                            {
                                mechanism,
                                confidence: 0.76
                            },
                            base,
                            1
                        );
                    }
                }

                for (
                    const child of
                    node.querySelectorAll?.(
                        selector
                    ) || []
                ) {
                    const value =
                        child.getAttribute(
                            attribute
                        );

                    if (value) {
                        this.enqueue(
                            value,
                            type,
                            {
                                mechanism,
                                confidence: 0.76
                            },
                            base,
                            1
                        );
                    }
                }
            }
        }

        async worker(index) {
            log(
                'Worker started',
                index
            );

            while (!this.stopRequested) {
                const runnable =
                    await this.waitUntilRunnable();

                if (!runnable) {
                    break;
                }

                const candidate =
                    this.db.claimNextCandidate();

                if (!candidate) {
                    if (
                        this.inFlight === 0
                    ) {
                        break;
                    }

                    await sleep(100);
                    continue;
                }

                const policy =
                    this.policy.shouldAcquire(
                        candidate
                    );

                if (!policy.acquire) {
                    this.db.markSkipped(
                        candidate,
                        policy.reason
                    );

                    this.updateUI();

                    continue;
                }

                const resource =
                    this.db.resources.get(
                        candidate.target
                    );

                if (
                    resource &&
                    resource.status ===
                    'acquired'
                ) {
                    const observation =
                        new Observation({
                            candidateId:
                                candidate.id,

                            target:
                                candidate.target,

                            requestedUrl:
                                candidate.target,

                            startedAt: now(),
                            completedAt: now(),

                            status: 'success',

                            signalPresent: true,

                            http: {
                                status: null,
                                contentType:
                                    resource.fingerprint
                                        ?.split(':')[0] ||
                                    '',
                                finalUrl:
                                    resource.finalUrl ||
                                    candidate.target
                            },

                            reason:
                                'resource-already-acquired'
                        });

                    this.db.addObservation(
                        observation
                    );

                    candidate.mark(
                        'observed'
                    );

                    candidate.mark(
                        'recognized'
                    );

                    candidate.mark(
                        'expanded'
                    );

                    this.db.completeCandidate(
                        candidate
                    );

                    this.updateUI();

                    continue;
                }

                if (
                    !await this.scheduler
                        .waitForGlobalSlot()
                ) {
                    this.db.requeue(
                        candidate
                    );

                    break;
                }

                const originSlot =
                    await this.origins.acquire(
                        candidate.target
                    );

                if (!originSlot) {
                    this.db.markSkipped(
                        candidate,
                        'origin-budget'
                    );

                    this.updateUI();

                    continue;
                }

                const requestSlot =
                    this.reserveRequestSlot();

                if (!requestSlot) {
                    this.origins.release(
                        candidate.target,
                        true
                    );

                    this.db.requeue(
                        candidate
                    );

                    break;
                }

                this.inFlight++;

                let success = false;

                try {
                    candidate.mark(
                        'acquiring'
                    );

                    const observation =
                        await this.processCandidate(
                            candidate
                        );

                    success =
                        observation.status ===
                        'success' ||
                        observation.status ===
                        'http-error';

                    if (success) {
                        this.scheduler
                            .recordSuccess();

                        this.db.stats
                            .requestsSucceeded++;

                        this.db.completeCandidate(
                            candidate
                        );
                    } else {
                        this.scheduler
                            .recordFailure();

                        this.db.stats
                            .requestsFailed++;

                        this.db.failCandidate(
                            candidate,
                            observation.errors?.join(
                                '; '
                            ) || 'request failed'
                        );
                    }
                } catch (error) {
                    this.scheduler
                        .recordFailure();

                    this.db.stats
                        .requestsFailed++;

                    this.db.failCandidate(
                        candidate,
                        error
                    );
                } finally {
                    this.origins.release(
                        candidate.target,
                        success
                    );

                    this.inFlight--;

                    this.updateUI();
                }
            }

            log(
                'Worker stopped',
                index
            );
        }

        async processCandidate(
            candidate
        ) {
            const startedAt =
                now();

            let response;

            try {
                response =
                    await acquireHttp(
                        candidate.target
                    );
            } catch (error) {
                const observation =
                    new Observation({
                        candidateId:
                            candidate.id,

                        target:
                            candidate.target,

                        requestedUrl:
                            candidate.target,

                        startedAt,

                        completedAt: now(),

                        status: 'error',

                        signalPresent: false,

                        errors: [
                            String(
                                error?.message ||
                                error
                            )
                        ],

                        http: {
                            finalUrl:
                                candidate.target
                        }
                    });

                this.db.addObservation(
                    observation
                );

                return observation;
            }

            const contentType =
                getContentType(
                    response.headers
                );

            const status =
                response.httpStatus >= 200 &&
                response.httpStatus < 400
                    ? 'success'
                    : 'http-error';

            const fingerprint =
                makeFingerprint(
                    response.body,
                    contentType
                );

            const observation =
                new Observation({
                    candidateId:
                        candidate.id,

                    target:
                        candidate.target,

                    requestedUrl:
                        candidate.target,

                    startedAt,

                    completedAt: now(),

                    status,

                    signalPresent:
                        Boolean(
                            response.body ||
                            response.httpStatus
                        ),

                    http: {
                        status:
                            response.httpStatus,

                        contentType,

                        contentLength:
                            response.body?.length ||
                            null,

                        finalUrl:
                            response.finalUrl ||
                            candidate.target
                    },

                    body:
                        response.body || '',

                    fingerprint
                });

            this.db.addObservation(
                observation
            );

            if (
                observation.http.finalUrl &&
                observation.http.finalUrl !==
                candidate.target
            ) {
                this.db.recordRedirect(
                    candidate.target,
                    observation.http.finalUrl
                );
            }

            candidate.hints.contentType =
                contentType;

            candidate.mark(
                'observed'
            );

            const recognition =
                this.providers.recognize(
                    observation
                );

            candidate.mark(
                'recognized'
            );

            if (recognition.length) {
                candidate.hints.provider =
                    recognition[0]
                        .provider.name;

                candidate.hints.confidence =
                    Math.max(
                        Number(
                            candidate.hints
                                .confidence || 0
                        ),
                        recognition[0]
                            .confidence
                    );
            }

            const discoveries =
                this.providers.discover(
                    observation
                );

            for (
                const discovery of
                discoveries
            ) {
                discovery.provenance.depth =
                    candidate.depth + 1;

                this.db.addDiscovery(
                    discovery
                );

                const candidateSpecs =
                    this.providers
                        .candidatesFor(
                            discovery
                        );

                for (
                    const spec of
                    candidateSpecs
                ) {
                    if (
                        candidate.depth + 1 >
                        CONFIG.maxDepth
                    ) {
                        continue;
                    }

                    this.enqueue(
                        spec.target,
                        spec.type,
                        {
                            ...spec.hints,
                            confidence:
                                Math.max(
                                    discovery.confidence,
                                    spec.hints
                                        ?.confidence ||
                                    0
                                )
                        },
                        candidate.target,
                        candidate.depth + 1
                    );
                }
            }

            candidate.mark(
                'expanded'
            );

            return observation;
        }

        clear() {
            this.stop();

            this.db.clear();

            this.running = false;
            this.paused = false;
            this.stopRequested = false;
            this.inFlight = 0;
            this.requestsStarted = 0;

            this.scheduler =
                new AdaptiveScheduler();

            this.origins =
                new OriginController();

            this.updateUI();
        }

        exportData() {
            const graphNodes = [
                {
                    id: 'root',
                    type: 'root',
                    url: location.href
                }
            ];

            for (
                const resource of
                this.db.resources.values()
            ) {
                graphNodes.push({
                    id:
                        resource.id,

                    type:
                        'resource',

                    url:
                        resource.url,

                    resourceTypes:
                        [...resource.types],

                    mechanisms:
                        [...resource.mechanisms],

                    status:
                        resource.status,

                    fingerprint:
                        resource.fingerprint,

                    finalUrl:
                        resource.finalUrl
                });
            }

            const graphEdges = [
                ...this.db.edges
            ];

            for (
                const resource of
                this.db.resources.values()
            ) {
                for (
                    const parent of
                    resource.parents
                ) {
                    const parentResource =
                        this.db.resources.get(
                            parent
                        );

                    graphEdges.push({
                        id:
                            makeId('edge'),

                        from:
                            parentResource?.id ||
                            'root',

                        to:
                            resource.id,

                        kind:
                            'resource-provenance',

                        createdAt:
                            resource.firstSeenAt
                    });
                }
            }

            for (
                const [
                    fingerprint,
                    urls
                ] of
                this.db.fingerprintIndex
            ) {
                const list =
                    [...urls];

                if (list.length < 2) {
                    continue;
                }

                const primary =
                    this.db.resources.get(
                        list[0]
                    );

                for (
                    const duplicateUrl of
                    list.slice(1)
                ) {
                    const duplicate =
                        this.db.resources.get(
                            duplicateUrl
                        );

                    if (
                        primary &&
                        duplicate
                    ) {
                        graphEdges.push({
                            id:
                                makeId('edge'),

                            from:
                                primary.id,

                            to:
                                duplicate.id,

                            kind:
                                'duplicate-content',

                            fingerprint
                        });
                    }
                }
            }

            return {
                version: 6,

                scope:
                    'web-resource-discovery',

                architecture:
                    'candidate → acquisition/observation → recognition/provider → discovery → new candidates → scheduler',

                inspiredBy:
                    'DVB blind scanning architecture',

                rfScanning: false,

                timestamp: new Date().toISOString(),

                page: {
                    url:
                        location.href,

                    title:
                        document.title,

                    origin:
                        location.origin
                },

                statistics: {
                    ...this.db.stats,

                    queue:
                        [...this.db.candidates.values()]
                            .filter(
                                candidate =>
                                    candidate.status ===
                                    'queued'
                            ).length,

                    inFlight:
                        this.inFlight,

                    requestsRemaining:
                        Math.max(
                            0,
                            CONFIG.maxRequests -
                            this.requestsStarted
                        ),

                    resources:
                        this.db.resources.size,

                    candidates:
                        this.db.candidates.size
                },

                configuration:
                    CONFIG,

                policy:
                    CONFIG.policy,

                scheduler: {
                    ...this.scheduler.snapshot(),

                    paused:
                        this.paused,

                    running:
                        this.running,

                    stopRequested:
                        this.stopRequested
                },

                origins:
                    this.origins.snapshot(),

                queue:
                    [...this.db.candidates.values()]
                        .map(candidate =>
                            candidate.serialize()
                        ),

                lifecycle:
                    [...this.db.candidates.values()]
                        .map(candidate => ({
                            id:
                                candidate.id,

                            target:
                                candidate.target,

                            type:
                                candidate.type,

                            status:
                                candidate.status,

                            attempts:
                                candidate.attempts,

                            discoveredAt:
                                candidate.discoveredAt,

                            queuedAt:
                                candidate.queuedAt,

                            claimedAt:
                                candidate.claimedAt,

                            acquiringAt:
                                candidate.acquiringAt,

                            observedAt:
                                candidate.observedAt,

                            recognizedAt:
                                candidate.recognizedAt,

                            expandedAt:
                                candidate.expandedAt,

                            completedAt:
                                candidate.completedAt,

                            failedAt:
                                candidate.failedAt
                        })),

                resources:
                    [...this.db.resources.values()]
                        .map(resource =>
                            resource.serialize()
                        ),

                observations:
                    [...this.db.observations.values()]
                        .map(observation =>
                            observation.serialize(
                                false
                            )
                        ),

                networkEvents:
                    [...this.db.networkEvents.values()]
                        .map(event =>
                            event.serialize()
                        ),

                discoveries:
                    [...this.db.discoveries.values()]
                        .map(discovery =>
                            discovery.serialize()
                        ),

                fingerprints:
                    [...this.db.fingerprintIndex]
                        .map(
                            ([
                                fingerprint,
                                urls
                            ]) => ({
                                fingerprint,
                                urls:
                                    [...urls]
                            })
                        ),

                graph: {
                    nodes:
                        graphNodes,

                    edges:
                        graphEdges.slice(
                            0,
                            CONFIG.maxGraphEdges
                        )
                },

                diagnostics:
                    this.db.diagnostics
            };
        }

        downloadExport() {
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

            document.body.appendChild(
                anchor
            );

            anchor.click();
            anchor.remove();

            setTimeout(
                () =>
                    URL.revokeObjectURL(
                        url
                    ),
                1000
            );
        }

        buildUI() {
            if (this.ui) {
                return;
            }

            const panel =
                document.createElement(
                    'div'
                );

            panel.style.cssText = `
                position: fixed;
                right: 12px;
                bottom: 12px;
                z-index: 2147483647;
                width: 330px;
                padding: 10px;
                background: rgba(20,20,20,.96);
                color: #eee;
                font: 12px/1.4 sans-serif;
                border: 1px solid #555;
                border-radius: 8px;
                box-shadow: 0 4px 18px rgba(0,0,0,.45);
            `;

            panel.innerHTML = `
                <div style="
                    font-weight:bold;
                    font-size:14px;
                    margin-bottom:7px;
                ">
                    Generic Discovery Engine 0.6
                </div>

                <div
                    data-gde-status
                    style="margin-bottom:7px;"
                ></div>

                <div style="
                    display:flex;
                    flex-wrap:wrap;
                    gap:5px;
                    margin-bottom:7px;
                ">
                    <button data-gde-scan>Scan</button>
                    <button data-gde-pause>Pause</button>
                    <button data-gde-stop>Stop</button>
                    <button data-gde-clear>Clear</button>
                    <button data-gde-export>Export</button>
                </div>

                <div
                    data-gde-stats
                    style="
                        white-space:pre-wrap;
                        opacity:.85;
                    "
                ></div>
            `;

            document.documentElement.appendChild(
                panel
            );

            this.ui = panel;

            panel.querySelector(
                '[data-gde-scan]'
            ).addEventListener(
                'click',
                () => this.start()
            );

            panel.querySelector(
                '[data-gde-pause]'
            ).addEventListener(
                'click',
                event => {
                    this.paused
                        ? this.resume()
                        : this.pause();

                    event.currentTarget
                        .textContent =
                        this.paused
                            ? 'Resume'
                            : 'Pause';
                }
            );

            panel.querySelector(
                '[data-gde-stop]'
            ).addEventListener(
                'click',
                () => this.stop()
            );

            panel.querySelector(
                '[data-gde-clear]'
            ).addEventListener(
                'click',
                () => this.clear()
            );

            panel.querySelector(
                '[data-gde-export]'
            ).addEventListener(
                'click',
                () => this.downloadExport()
            );

            this.updateUI();
        }

        updateUI() {
            if (!this.ui) {
                return;
            }

            const status =
                this.ui.querySelector(
                    '[data-gde-status]'
                );

            const stats =
                this.ui.querySelector(
                    '[data-gde-stats]'
                );

            const queued =
                [...this.db.candidates.values()]
                    .filter(
                        candidate =>
                            candidate.status ===
                            'queued'
                    ).length;

            const scheduler =
                this.scheduler.snapshot();

            status.textContent =
                this.stopRequested
                    ? 'Stopped'
                    : this.paused
                        ? 'Paused'
                        : this.running
                            ? 'Running'
                            : 'Idle';

            stats.textContent =
                [
                    `Candidates: ${this.db.candidates.size}`,
                    `Queued: ${queued}`,
                    `Resources: ${this.db.resources.size}`,
                    `Discoveries: ${this.db.stats.discoveries}`,
                    `Requests: ${this.requestsStarted}/${CONFIG.maxRequests}`,
                    `In-flight: ${this.inFlight}`,
                    `Concurrency: ${scheduler.currentConcurrency}/${scheduler.configuredConcurrency}`,
                    `Succeeded: ${this.db.stats.requestsSucceeded}`,
                    `Failed: ${this.db.stats.requestsFailed}`,
                    `Policy skips: ${this.db.stats.policySkips}`,
                    `Origin skips: ${this.db.stats.originBudgetSkips}`,
                    `Duplicates: ${this.db.stats.duplicateContent}`,
                    `Network events: ${this.db.stats.networkEvents}`,
                    `Graph edges: ${this.db.stats.graphEdges}`
                ].join('\n');
        }
    }
