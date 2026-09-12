    class DiscoveryEngine {
        constructor() {
            this.database =
                new KnowledgeBase();

            this.acquisition =
                new HttpAcquisitionAdapter();

            this.policy =
                new AcquisitionPolicy();

            this.providers =
                new ProviderRegistry();

            this.originBudget =
                new OriginBudget();

            this.scheduler =
                new Scheduler(this);

            this.networkEvents =
                new Map();

            this.networkRequestIndex =
                new Map();

            this.diagnostics =
                [];

            this.running =
                false;

            this.paused =
                false;

            this.stopRequested =
                false;

            this.inFlight =
                0;

            this.seeded =
                false;

            this.currentConcurrency =
                CONFIG.concurrency;

            this.consecutiveFailures =
                0;

            this.consecutiveSuccesses =
                0;

            this.networkObserver =
                new NetworkObserver(
                    event =>
                        this.observeNetwork(
                            event
                        )
                );

            if (
                CONFIG.discoverNetwork
            ) {
                this.networkObserver.install();
            }
        }

        diagnostic(
            level,
            message,
            data = null
        ) {
            const entry = {
                id:
                    makeId(
                        'diagnostic'
                    ),

                at:
                    now(),

                level,

                message,

                data
            };

            this.diagnostics.push(
                entry
            );

            if (
                this.diagnostics.length >
                CONFIG.maxDiagnostics
            ) {
                this.diagnostics.splice(
                    0,
                    this.diagnostics.length -
                        CONFIG.maxDiagnostics
                );
            }

            if (
                level === 'error'
            ) {
                warn(
                    message,
                    data
                );
            } else {
                log(
                    message,
                    data
                );
            }
        }

        seed() {
            if (this.seeded) {
                return;
            }

            this.seeded =
                true;

            const current =
                canonicalizeUrl(
                    location.href
                );

            if (current) {
                this.addCandidate(
                    new Candidate({
                        target:
                            current,

                        type:
                            'url',

                        origin:
                            'document',

                        priority:
                            1.0,

                        hints: {
                            confidence:
                                1
                        },

                        depth:
                            0
                    })
                );
            }

            this.seedFromCurrentDom();

            if (
                CONFIG.discoverWellKnown
            ) {
                this.seedWellKnown();
            }
        }

        seedFromCurrentDom() {
            if (!document) {
                return;
            }

            const base =
                location.href;

            if (
                CONFIG.discoverLinks
            ) {
                for (
                    const element of
                    document.querySelectorAll(
                        'a[href], area[href]'
                    )
                ) {
                    const url =
                        canonicalizeUrl(
                            element.getAttribute(
                                'href'
                            ),
                            base
                        );

                    if (
                        !url ||
                        !isAllowedUrl(url)
                    ) {
                        continue;
                    }

                    this.addCandidate(
                        new Candidate({
                            target:
                                url,

                            type:
                                'url',

                            origin:
                                `dom:${element.tagName.toLowerCase()}`,

                            priority:
                                0.80,

                            hints: {
                                confidence:
                                    0.82
                            },

                            depth:
                                1
                        })
                    );
                }
            }

            if (
                CONFIG.discoverResources
            ) {
                const resourceSelectors = [
                    [
                        'script[src]',
                        'src',
                        'script'
                    ],
                    [
                        'link[href]',
                        'href',
                        'resource'
                    ],
                    [
                        'img[src]',
                        'src',
                        'media'
                    ],
                    [
                        'iframe[src], frame[src]',
                        'src',
                        'frame'
                    ],
                    [
                        'video[src], audio[src], source[src]',
                        'src',
                        'media'
                    ]
                ];

                for (
                    const [
                        selector,
                        attribute,
                        defaultType
                    ] of
                    resourceSelectors
                ) {
                    for (
                        const element of
                        document.querySelectorAll(
                            selector
                        )
                    ) {
                        const url =
                            canonicalizeUrl(
                                element.getAttribute(
                                    attribute
                                ),
                                base
                            );

                        if (
                            !url ||
                            !isAllowedUrl(url)
                        ) {
                            continue;
                        }

                        let type =
                            defaultType;

                        if (
                            selector ===
                            'link[href]'
                        ) {
                            const rel =
                                String(
                                    element.getAttribute(
                                        'rel'
                                    ) || ''
                                ).toLowerCase();

                            if (
                                rel.includes(
                                    'stylesheet'
                                )
                            ) {
                                type =
                                    'stylesheet';
                            } else if (
                                rel.includes(
                                    'manifest'
                                )
                            ) {
                                type =
                                    'manifest';
                            } else if (
                                rel.includes(
                                    'sitemap'
                                )
                            ) {
                                type =
                                    'sitemap';
                            }
                        }

                        this.addCandidate(
                            new Candidate({
                                target:
                                    url,

                                type,

                                origin:
                                    `dom:${element.tagName.toLowerCase()}`,

                                priority:
                                    CONFIG.typePriority[
                                        type
                                    ] ??
                                    0.45,

                                hints: {
                                    confidence:
                                        0.82
                                },

                                depth:
                                    1
                            })
                        );
                    }
                }
            }

            if (
                CONFIG.discoverForms
            ) {
                for (
                    const form of
                    document.querySelectorAll(
                        'form[action]'
                    )
                ) {
                    const url =
                        canonicalizeUrl(
                            form.getAttribute(
                                'action'
                            ),
                            base
                        );

                    if (
                        !url ||
                        !isAllowedUrl(url)
                    ) {
                        continue;
                    }

                    this.addCandidate(
                        new Candidate({
                            target:
                                url,

                            type:
                                'form',

                            origin:
                                'dom:form',

                            priority:
                                0.35,

                            hints: {
                                confidence:
                                    0.75,

                                method:
                                    normalizeMethod(
                                        form.getAttribute(
                                            'method'
                                        ) || 'GET'
                                    )
                            },

                            depth:
                                1
                        })
                    );
                }
            }
        }

        seedWellKnown() {
            let origin;

            try {
                origin =
                    new URL(
                        location.href
                    ).origin;
            } catch {
                return;
            }

            const seeds = [
                [
                    '/robots.txt',
                    'robots',
                    0.88
                ],
                [
                    '/sitemap.xml',
                    'sitemap',
                    0.90
                ]
            ];

            for (
                const [
                    path,
                    type,
                    priority
                ] of seeds
            ) {
                const url =
                    canonicalizeUrl(
                        origin + path
                    );

                if (
                    !url ||
                    !isAllowedUrl(url)
                ) {
                    continue;
                }

                this.addCandidate(
                    new Candidate({
                        target:
                            url,

                        type,

                        origin:
                            'well-known',

                        priority,

                        hints: {
                            confidence:
                                0.70
                        },

                        depth:
                            1
                    })
                );
            }
        }

        addCandidate(candidate) {
            return this.database
                .addCandidate(
                    candidate
                );
        }

        observeNetwork(data) {
            if (!data?.url) {
                return;
            }

            if (
                data.event ===
                'performance'
            ) {
                this.handlePerformanceEvent(
                    data
                );

                return;
            }

            const requestId =
                data.requestId ||
                null;

            let event =
                null;

            if (
                data.event ===
                'request'
            ) {
                event =
                    new NetworkEvent({
                        requestId,

                        api:
                            data.api,

                        method:
                            data.method,

                        url:
                            data.url,

                        requestAt:
                            data.requestAt ||
                            now(),

                        phase:
                            'request'
                    });

                this.storeNetworkEvent(
                    event
                );

                if (requestId) {
                    this.networkRequestIndex.set(
                        requestId,
                        event.id
                    );
                }

                return;
            }

            if (
                data.event ===
                    'response' ||
                data.event ===
                    'error'
            ) {
                if (requestId) {
                    const eventId =
                        this.networkRequestIndex.get(
                            requestId
                        );

                    if (eventId) {
                        event =
                            this.networkEvents.get(
                                eventId
                            );
                    }
                }

                if (!event) {
                    event =
                        new NetworkEvent({
                            requestId,

                            api:
                                data.api,

                            method:
                                data.method,

                            url:
                                data.url,

                            requestAt:
                                data.requestAt ||
                                now()
                        });

                    this.storeNetworkEvent(
                        event
                    );
                }

                event.phase =
                    data.event ===
                    'error'
                        ? 'error'
                        : 'response';

                event.finalUrl =
                    canonicalizeUrl(
                        data.finalUrl
                    ) ||
                    event.url;

                event.status =
                    data.status ??
                    null;

                event.contentType =
                    normalizeContentType(
                        data.contentType ||
                        ''
                    );

                event.responseAt =
                    data.responseAt ||
                    now();

                event.duration =
                    data.duration ??
                    (
                        event.requestAt
                            ? event.responseAt -
                              event.requestAt
                            : null
                    );

                event.error =
                    data.error ||
                    null;

                this.storeNetworkEvent(
                    event
                );

                /*
                 * GET-only rule.
                 *
                 * The engine observes POST/etc. but never replays them.
                 */
                if (
                    data.event ===
                        'response' &&
                    this.policy
                        .shouldAcquireAfterObservation(
                            null,
                            event
                        )
                ) {
                    const target =
                        canonicalizeUrl(
                            event.url
                        );

                    if (
                        target &&
                        isAllowedUrl(
                            target
                        )
                    ) {
                        const type =
                            looksLikeApiUrl(
                                target
                            )
                                ? 'api'
                                : 'network';

                        const candidate =
                            new Candidate({
                                target,

                                type,

                                origin:
                                    `network:${event.api}`,

                                priority:
                                    type === 'api'
                                        ? 0.96
                                        : 0.80,

                                hints: {
                                    confidence:
                                        0.94,

                                    networkRequestId:
                                        requestId,

                                    observedStatus:
                                        event.status,

                                    observedContentType:
                                        event.contentType,

                                    observedFinalUrl:
                                        event.finalUrl,

                                    observedNetwork:
                                        true
                                },

                                depth:
                                    0
                            });

                        if (
                            this.addCandidate(
                                candidate
                            )
                        ) {
                            this.database
                                .statistics
                                .networkCandidates++;
                        }
                    }
                }
            }
        }

        handlePerformanceEvent(
            data
        ) {
            const target =
                canonicalizeUrl(
                    data.url
                );

            if (
                !target ||
                !isAllowedUrl(target)
            ) {
                return;
            }

            const type =
                this.classifyPerformanceResource(
                    data
                );

            const candidate =
                new Candidate({
                    target,

                    type,

                    origin:
                        `performance:${data.initiatorType || 'resource'}`,

                    priority:
                        CONFIG.typePriority[
                            type
                        ] ??
                        0.45,

                    hints: {
                        confidence:
                            0.88,

                        initiatorType:
                            data.initiatorType ||
                            null,

                        performanceDuration:
                            data.duration ??
                            null
                    },

                    depth:
                        0
                });

            if (
                this.addCandidate(
                    candidate
                )
            ) {
                this.database
                    .statistics
                    .performanceCandidates++;
            }
        }

        classifyPerformanceResource(
            data
        ) {
            const initiator =
                String(
                    data.initiatorType ||
                    ''
                ).toLowerCase();

            const url =
                String(
                    data.url ||
                    ''
                ).toLowerCase();

            if (
                initiator === 'fetch' ||
                initiator ===
                    'xmlhttprequest'
            ) {
                return looksLikeApiUrl(
                    url
                )
                    ? 'api'
                    : 'network';
            }

            if (
                initiator ===
                    'script' ||
                /\.(?:js|mjs|cjs)(?:[?#]|$)/i
                    .test(url)
            ) {
                return 'script';
            }

            if (
                initiator ===
                    'css' ||
                initiator ===
                    'link' ||
                /\.css(?:[?#]|$)/i.test(
                    url
                )
            ) {
                return 'stylesheet';
            }

            if (
                initiator === 'img' ||
                /\.(?:png|jpe?g|gif|webp|svg|avif|ico)(?:[?#]|$)/i
                    .test(url)
            ) {
                return 'media';
            }

            if (
                initiator === 'iframe' ||
                initiator === 'frame'
            ) {
                return 'frame';
            }

            return 'resource';
        }

        storeNetworkEvent(event) {
            if (!event?.id) {
                return;
            }

            if (
                !this.networkEvents.has(
                    event.id
                )
            ) {
                while (
                    this.networkEvents.size >=
                    CONFIG.maxNetworkEvents
                ) {
                    const oldest =
                        this.networkEvents.keys()
                            .next()
                            .value;

                    if (!oldest) {
                        break;
                    }

                    this.networkEvents.delete(
                        oldest
                    );
                }

                this.networkEvents.set(
                    event.id,
                    event
                );

                this.database
                    .statistics
                    .networkEvents++;
            }
        }

        async run() {
            if (this.running) {
                return;
            }

            this.seed();

            this.running =
                true;

            this.paused =
                false;

            this.stopRequested =
                false;

            const workerCount =
                Math.max(
                    1,
                    CONFIG.concurrency
                );

            const workers = [];

            for (
                let i = 0;
                i < workerCount;
                i++
            ) {
                workers.push(
                    this.worker(i)
                );
            }

            await Promise.all(
                workers
            );

            this.running =
                false;

            this.paused =
                false;

            this.database.persistNow();

            this.diagnostic(
                'info',
                'Scan complete',
                this.report()
            );
        }

        pause() {
            if (
                !this.running ||
                this.paused
            ) {
                return;
            }

            this.paused =
                true;

            this.database
                .statistics
                .pauses++;

            this.diagnostic(
                'info',
                'Scan paused'
            );
        }

        resume() {
            if (
                !this.running ||
                !this.paused
            ) {
                return;
            }

            this.paused =
                false;

            this.database
                .statistics
                .resumes++;

            this.diagnostic(
                'info',
                'Scan resumed'
            );
        }

        stop() {
            if (!this.running) {
                return;
            }

            this.stopRequested =
                true;

            this.paused =
                false;

            this.diagnostic(
                'info',
                'Stop requested'
            );
        }

        async worker(workerId) {
            while (
                this.running &&
                !this.stopRequested
            ) {
                while (
                    this.paused &&
                    !this.stopRequested
                ) {
                    await sleep(100);
                }

                if (
                    this.stopRequested
                ) {
                    break;
                }

                if (
                    this.database
                        .statistics
                        .requests >=
                    CONFIG.maxRequests
                ) {
                    break;
                }

                const candidate =
                    this.scheduler.next();

                if (!candidate) {
                    if (
                        this.inFlight > 0
                    ) {
                        await sleep(50);
                        continue;
                    }

                    const delay =
                        this.scheduler.delay();

                    if (
                        delay === null
                    ) {
                        break;
                    }

                    await sleep(
                        Math.min(
                            Math.max(
                                delay,
                                25
                            ),
                            250
                        )
                    );

                    continue;
                }

                await this.processCandidate(
                    candidate,
                    workerId
                );
            }
        }

        async processCandidate(
            candidate,
            workerId
        ) {
            const decision =
                this.policy.shouldAcquire(
                    candidate
                );

            if (!decision.allowed) {
                const observation =
                    new Observation({
                        candidateId:
                            candidate.id,

                        target:
                            candidate.target,

                        status:
                            'skipped',

                        reason:
                            decision.reason
                    });

                observation.completedAt =
                    now();

                observation.signalPresent =
                    false;

                candidate.transition(
                    'observed'
                );

                this.database.addObservation(
                    observation
                );

                candidate.transition(
                    'recognized'
                );

                candidate.transition(
                    'expanded'
                );

                candidate.transition(
                    'skipped'
                );

                this.database.skipCandidate(
                    candidate,
                    decision.reason
                );

                return;
            }

            /*
             * Resource-level deduplication.
             */
            if (
                this.database
                    .resourceAlreadyAcquired(
                        candidate.target
                    )
            ) {
                const resource =
                    this.database.getResource(
                        candidate.target
                    );

                const observation =
                    new Observation({
                        candidateId:
                            candidate.id,

                        target:
                            candidate.target,

                        status:
                            'reused',

                        reason:
                            'resource-already-acquired'
                    });

                observation.completedAt =
                    now();

                observation.signalPresent =
                    true;

                observation.http = {
                    status:
                        resource?.fingerprint
                            ?.status ??
                        null,

                    contentType:
                        resource?.fingerprint
                            ?.contentType ||
                        '',

                    contentLength:
                        resource?.fingerprint
                            ?.contentLength ??
                        null,

                    finalUrl:
                        resource?.finalUrl ||
                        resource?.fingerprint
                            ?.finalUrl ||
                        candidate.target
                };

                observation.fingerprint =
                    resource?.fingerprint ||
                    null;

                candidate.transition(
                    'observed'
                );

                this.database.addObservation(
                    observation
                );

                candidate.transition(
                    'recognized'
                );

                candidate.transition(
                    'expanded'
                );

                this.database.completeCandidate(
                    candidate
                );

                return;
            }

            /*
             * Global adaptive concurrency.
             */
            const slot =
                await this.scheduler
                    .waitForGlobalSlot();

            if (
                !slot ||
                this.stopRequested
            ) {
                /*
                 * Return the candidate to the queue rather than losing it.
                 */
                candidate.transition(
                    'queued'
                );

                this.database.queue.push(
                    candidate
                );

                this.database.claimed.delete(
                    candidate.key()
                );

                return;
            }

            const origin =
                getOrigin(
                    candidate.target
                );

            const originSlot =
                await this.originBudget
                    .acquireSlot(
                        origin
                    );

            if (
                !originSlot.acquired
            ) {
                candidate.hints.skipReason =
                    originSlot.reason;

                candidate.transition(
                    'skipped'
                );

                this.database
                    .claimed
                    .delete(
                        candidate.key()
                    );

                this.database
                    .visited
                    .add(
                        candidate.key()
                    );

                const resource =
                    this.database
                        .ensureResource(
                            candidate.target
                        );

                resource.status =
                    'skipped';

                this.database
                    .statistics
                    .originBudgetSkips++;

                this.database
                    .statistics
                    .policySkips++;

                this.database
                    .schedulePersist();

                return;
            }

            this.inFlight++;

            this.database
                .statistics
                .requests++;

            candidate.transition(
                'acquiring'
            );

            let successful =
                false;

            try {
                const observation =
                    await this.acquisition
                        .acquire(
                            candidate
                        );

                successful =
                    true;

                candidate.transition(
                    'observed'
                );

                this.database.addObservation(
                    observation
                );

                this.database
                    .markResourceAcquired(
                        candidate.target,
                        observation
                    );

                const discoveries =
                    this.providers
                        .recognizeAll(
                            candidate,
                            observation
                        );

                candidate.transition(
                    'recognized'
                );

                for (
                    const discovery of
                    discoveries
                ) {
                    this.database
                        .addDiscovery(
                            discovery
                        );

                    const nextCandidates =
                        this.providers
                            .candidatesFor(
                                discovery
                            );

                    for (
                        const nextCandidate of
                        nextCandidates
                    ) {
                        this.addCandidate(
                            nextCandidate
                        );
                    }
                }

                candidate.transition(
                    'expanded'
                );

                this.database
                    .completeCandidate(
                        candidate
                    );

                this.recordSuccess();

                log(
                    `Worker ${workerId} completed`,
                    candidate.target,
                    discoveries.length,
                    'discoveries'
                );
            } catch (error) {
                this.recordFailure(
                    error
                );

                this.database
                    .failCandidate(
                        candidate,
                        error
                    );

                this.diagnostic(
                    'error',
                    `Acquisition failed: ${candidate.target}`,
                    {
                        workerId,
                        error:
                            String(
                                error?.message ||
                                error
                            ),
                        attempts:
                            candidate.attempts
                    }
                );
            } finally {
                this.originBudget.release(
                    origin,
                    successful
                );

                this.inFlight--;
            }
        }

        recordSuccess() {
            if (
                !CONFIG.adaptiveConcurrency
            ) {
                return;
            }

            this.consecutiveFailures =
                0;

            this.consecutiveSuccesses++;

            if (
                this.consecutiveSuccesses >=
                CONFIG.adaptiveRecoverySuccesses
            ) {
                this.consecutiveSuccesses =
                    0;

                if (
                    this.currentConcurrency <
                    CONFIG.concurrency
                ) {
                    this.currentConcurrency++;

                    this.database
                        .statistics
                        .adaptiveConcurrencyChanges++;

                    this.diagnostic(
                        'info',
                        'Adaptive concurrency increased',
                        {
                            current:
                                this.currentConcurrency
                        }
                    );
                }
            }
        }

        recordFailure(error) {
            if (
                !CONFIG.adaptiveConcurrency
            ) {
                return;
            }

            this.consecutiveSuccesses =
                0;

            this.consecutiveFailures++;

            if (
                this.consecutiveFailures >=
                CONFIG.adaptiveFailureThreshold
            ) {
                this.consecutiveFailures =
                    0;

                if (
                    this.currentConcurrency >
                    CONFIG.adaptiveMinConcurrency
                ) {
                    this.currentConcurrency =
                        Math.max(
                            CONFIG.adaptiveMinConcurrency,
                            this.currentConcurrency -
                                1
                        );

                    this.database
                        .statistics
                        .adaptiveConcurrencyChanges++;

                    this.diagnostic(
                        'info',
                        'Adaptive concurrency reduced',
                        {
                            current:
                                this.currentConcurrency,

                            error:
                                String(
                                    error?.message ||
                                    error
                                )
                        }
                    );
                }
            }
        }

        report() {
            const stats =
                this.database.statistics;

            return {
                running:
                    this.running,

                paused:
                    this.paused,

                stopRequested:
                    this.stopRequested,

                queue:
                    this.database.queue.length,

                claimed:
                    this.database.claimed.size,

                inFlight:
                    this.inFlight,

                configuredConcurrency:
                    CONFIG.concurrency,

                currentConcurrency:
                    this.currentConcurrency,

                resources:
                    this.database.resources.size,

                observations:
                    this.database.observations.size,

                discoveries:
                    this.database.discoveries.size,

                networkEvents:
                    this.networkEvents.size,

                requests:
                    stats.requests,

                maxRequests:
                    CONFIG.maxRequests,

                retries:
                    stats.retries,

                failures:
                    stats.failures,

                successes:
                    stats.successes,

                cacheSkips:
                    stats.cacheSkips,

                policySkips:
                    stats.policySkips,

                originBudgetSkips:
                    stats.originBudgetSkips,

                duplicateContent:
                    stats.duplicateContent,

                redirects:
                    stats.redirects,

                candidatesCreated:
                    stats.candidatesCreated,

                candidatesMerged:
                    stats.candidatesMerged,

                candidatesRejected:
                    stats.candidatesRejected,

                maxDepthReached:
                    stats.maxDepthReached
            };
        }

        export() {
            const resources =
                [
                    ...this.database
                        .resources
                        .values()
                ];

            const observations =
                [
                    ...this.database
                        .observations
                        .values()
                ];

            const discoveries =
                [
                    ...this.database
                        .discoveries
                        .values()
                ];

            const networkEvents =
                [
                    ...this.networkEvents
                        .values()
                ];

            const graphNodes = [
                {
                    id:
                        'root',

                    kind:
                        'root',

                    url:
                        canonicalizeUrl(
                            location.href
                        ),

                    label:
                        'scan-root'
                }
            ];

            for (
                const resource of
                resources
            ) {
                graphNodes.push({
                    id:
                        resource.id,

                    kind:
                        'resource',

                    url:
                        resource.url,

                    types:
                        [
                            ...resource.types
                        ],

                    mechanisms:
                        [
                            ...resource.mechanisms
                        ],

                    status:
                        resource.status,

                    firstSeenAt:
                        resource.firstSeenAt,

                    lastSeenAt:
                        resource.lastSeenAt,

                    fingerprint:
                        resource.fingerprint,

                    finalUrl:
                        resource.finalUrl,

                    redirectTo:
                        resource.redirectTo,

                    duplicateFingerprint:
                        resource.duplicateFingerprint,

                    candidateIds:
                        [
                            ...resource.candidateIds
                        ],

                    observationIds:
                        [
                            ...resource.observationIds
                        ],

                    discoveryIds:
                        [
                            ...resource.discoveryIds
                        ]
                });
            }

            const graphEdges = [];

            /*
             * Discovery/provenance edges.
             */
            for (
                const edge of
                this.database
                    .edgeRecords
            ) {
                let sourceId =
                    'root';

                if (
                    edge.fromDiscoveryId
                ) {
                    const discovery =
                        this.database
                            .discoveries
                            .get(
                                edge.fromDiscoveryId
                            );

                    const parentTarget =
                        discovery?.targetUrl();

                    if (parentTarget) {
                        const parentResource =
                            this.database
                                .resources
                                .get(
                                    parentTarget
                                );

                        if (parentResource) {
                            sourceId =
                                parentResource.id;
                        }
                    }
                }

                const target =
                    this.database
                        .resources
                        .get(
                            edge.target
                        );

                if (!target) {
                    continue;
                }

                if (
                    sourceId ===
                    target.id
                ) {
                    continue;
                }

                graphEdges.push({
                    id:
                        edge.id,

                    source:
                        sourceId,

                    target:
                        target.id,

                    kind:
                        'discovery',

                    mechanism:
                        edge.mechanism,

                    candidateType:
                        edge.candidateType,

                    confidence:
                        edge.confidence,

                    priority:
                        edge.priority,

                    depth:
                        edge.depth,

                    discoveryId:
                        edge.fromDiscoveryId,

                    createdAt:
                        edge.createdAt
                });
            }

            /*
             * Redirect edges.
             */
            for (
                const resource of
                resources
            ) {
                if (
                    !resource.redirectTo ||
                    resource.redirectTo ===
                        resource.url
                ) {
                    continue;
                }

                const target =
                    this.database
                        .resources
                        .get(
                            resource.redirectTo
                        );

                if (!target) {
                    continue;
                }

                graphEdges.push({
                    id:
                        stableId(
                            'redirect',
                            `${resource.url}->${resource.redirectTo}`
                        ),

                    source:
                        resource.id,

                    target:
                        target.id,

                    kind:
                        'redirect',

                    mechanism:
                        'http-redirect'
                });
            }

            /*
             * Duplicate-content edges.
             */
            if (
                CONFIG.detectDuplicateContent
            ) {
                for (
                    const [
                        fingerprint,
                        urls
                    ] of
                    this.database
                        .fingerprintIndex
                ) {
                    if (
                        urls.size < 2
                    ) {
                        continue;
                    }

                    const list =
                        [
                            ...urls
                        ];

                    const first =
                        this.database
                            .resources
                            .get(
                                list[0]
                            );

                    if (!first) {
                        continue;
                    }

                    for (
                        let i = 1;
                        i < list.length;
                        i++
                    ) {
                        const duplicate =
                            this.database
                                .resources
                                .get(
                                    list[i]
                                );

                        if (!duplicate) {
                            continue;
                        }

                        graphEdges.push({
                            id:
                                stableId(
                                    'duplicate',
                                    `${list[0]}->${list[i]}:${fingerprint}`
                                ),

                            source:
                                first.id,

                            target:
                                duplicate.id,

                            kind:
                                'duplicate-content',

                            fingerprint
                        });
                    }
                }
            }

            /*
             * Network observation edges.
             */
            for (
                const event of
                networkEvents
            ) {
                const target =
                    event.url &&
                    this.database
                        .resources
                        .get(
                            event.url
                        );

                if (!target) {
                    continue;
                }

                graphEdges.push({
                    id:
                        stableId(
                            'network-edge',
                            event.id
                        ),

                    source:
                        'root',

                    target:
                        target.id,

                    kind:
                        event.phase ===
                        'performance'
                            ? 'performance-observation'
                            : 'network-observation',

                    mechanism:
                        event.api,

                    requestId:
                        event.requestId,

                    method:
                        event.method,

                    status:
                        event.status,

                    contentType:
                        event.contentType
                });
            }

            return {
                version:
                    6,

                scope: {
                    type:
                        'web-resource-discovery',

                    architecture:
                        'candidate -> policy -> acquisition -> observation -> recognition -> discovery -> scheduler',

                    inspiredBy:
                        'DVB blind-scan architecture',

                    rfScanning:
                        false
                },

                timestamp:
                    new Date()
                        .toISOString(),

                page: {
                    url:
                        location.href,

                    origin:
                        location.origin,

                    title:
                        document.title ||
                        '',

                    userAgent:
                        navigator.userAgent
                },

                statistics:
                    this.report(),

                configuration:
                    CONFIG,

                scheduler: {
                    configuredConcurrency:
                        CONFIG.concurrency,

                    currentConcurrency:
                        this.currentConcurrency,

                    adaptive:
                        CONFIG.adaptiveConcurrency,

                    paused:
                        this.paused,

                    running:
                        this.running
                },

                policy: {
                    sameOriginOnly:
                        CONFIG.sameOriginOnly,

                    acquireForms:
                        CONFIG.acquireForms,

                    acquireMedia:
                        CONFIG.acquireMedia,

                    acquireBinaryResources:
                        CONFIG.acquireBinaryResources,

                    acquireFrames:
                        CONFIG.acquireFrames,

                    maxRequestsPerOrigin:
                        CONFIG.maxRequestsPerOrigin,

                    minRequestInterval:
                        CONFIG.minRequestInterval,

                    maxConcurrentPerOrigin:
                        CONFIG.maxConcurrentPerOrigin,

                    stripTrackingParams:
                        CONFIG.stripTrackingParams
                },

                origins:
                    this.originBudget.toJSON(),

                queue:
                    this.database.queue
                        .map(
                            candidate => ({
                                id:
                                    candidate.id,

                                target:
                                    candidate.target,

                                type:
                                    candidate.type,

                                origin:
                                    candidate.origin,

                                parent:
                                    candidate.parent,

                                priority:
                                    candidate.priority,

                                effectivePriority:
                                    candidate.effectivePriority(),

                                depth:
                                    candidate.depth,

                                status:
                                    candidate.status,

                                attempts:
                                    candidate.attempts,

                                nextAttemptAt:
                                    candidate.nextAttemptAt
                            })
                        ),

                resources:
                    resources.map(
                        resource =>
                            resource.toJSON()
                    ),

                observations:
                    observations.map(
                        observation => ({
                            id:
                                observation.id,

                            candidateId:
                                observation.candidateId,

                            target:
                                observation.target,

                            startedAt:
                                observation.startedAt,

                            completedAt:
                                observation.completedAt,

                            status:
                                observation.status,

                            reason:
                                observation.reason,

                            signalPresent:
                                observation.signalPresent,

                            http:
                                observation.http,

                            errors:
                                observation.errors,

                            network:
                                observation.network,

                            fingerprint:
                                observation.fingerprint
                        })
                    ),

                discoveries,

                networkEvents,

                duplicateContentGroups:
                    [
                        ...this.database
                            .fingerprintIndex
                    ].map(
                        ([fingerprint, urls]) => ({
                            fingerprint,
                            urls:
                                [
                                    ...urls
                                ]
                        })
                    ),

                diagnostics:
                    this.diagnostics.slice(
                        -CONFIG.maxDiagnostics
                    ),

                graph: {
                    nodes:
                        graphNodes,

                    edges:
                        graphEdges.slice(
                            -CONFIG.maxGraphEdges
                        )
                }
            };
        }

        exportJson() {
            return JSON.stringify(
                this.export(),
                null,
                2
            );
        }

        clear() {
            this.stopRequested =
                true;

            this.running =
                false;

            this.paused =
                false;

            this.database.clear();

            this.networkEvents.clear();

            this.networkRequestIndex.clear();

            this.originBudget =
                new OriginBudget();

            this.diagnostics.length =
                0;

            this.seeded =
                false;

            this.currentConcurrency =
                CONFIG.concurrency;

            this.consecutiveFailures =
                0;

            this.consecutiveSuccesses =
                0;
        }
    }
