    class DiscoveryEngine {
        constructor() {
            this.database =
                new KnowledgeBase();

            this.scheduler =
                new Scheduler(
                    this.database
                );

            this.acquisition =
                new HttpAcquisitionAdapter();

            this.providers =
                new ProviderRegistry();

            this.running =
                false;

            this.stats =
                this.newStats();

            this.networkSeen =
                new Set();

            this.networkObserver =
                null;

            /*
             * Install the observer as early as possible.
             * Performance entries already present will also
             * be processed.
             */
            if (
                CONFIG.discoverNetwork ||
                CONFIG.discoverPerformance
            ) {
                this.networkObserver =
                    new NetworkObserver(
                        this
                    );
            }
        }

        newStats() {
            return {
                startedAt: null,
                finishedAt: null,

                requests: 0,

                discoveries: 0,

                failures: 0,

                retries: 0,

                candidatesCreated: 0,

                candidatesRejected: 0,

                networkCandidates: 0,

                performanceCandidates: 0
            };
        }

        resetStats() {
            this.stats =
                this.newStats();
        }

        addCandidate(
            candidate
        ) {
            if (
                !candidate ||
                !candidate.target
            ) {
                this.stats
                    .candidatesRejected++;

                return false;
            }

            const added =
                this.scheduler.add(
                    candidate
                );

            if (added) {
                this.stats
                    .candidatesCreated++;
            } else {
                this.stats
                    .candidatesRejected++;
            }

            return added;
        }

        observeNetwork({
            url,
            mechanism =
                'network',
            event = 'request',
            status = null,
            contentType = null
        }) {
            if (
                !CONFIG.discoverNetwork &&
                mechanism !==
                    'performance-resource'
            ) {
                return;
            }

            const canonical =
                canonicalizeUrl(
                    url,
                    location.href
                );

            if (
                !canonical ||
                !isAllowedUrl(
                    canonical
                )
            ) {
                return;
            }

            const key =
                `${mechanism}:${canonical}`;

            if (
                this.networkSeen.has(
                    key
                )
            ) {
                return;
            }

            this.networkSeen.add(
                key
            );

            const candidate =
                new Candidate({
                    target:
                        canonical,

                    type:
                        'network',

                    origin:
                        mechanism,

                    parent:
                        null,

                    priority:
                        mechanism ===
                            'network-fetch' ||
                        mechanism ===
                            'network-xhr'
                            ? 0.95
                            : 0.82,

                    depth: 0,

                    hints: {
                        mechanism,
                        event,
                        status,
                        contentType
                    }
                });

            const added =
                this.addCandidate(
                    candidate
                );

            if (added) {
                if (
                    mechanism ===
                    'performance-resource'
                ) {
                    this.stats
                        .performanceCandidates++;
                } else {
                    this.stats
                        .networkCandidates++;
                }

                log(
                    'Network candidate:',
                    canonical,
                    mechanism
                );
            }
        }

        seed() {
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
                            'initial-page',

                        priority:
                            1.0,

                        depth: 0
                    })
                );
            }

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
                            location.href
                        );

                    if (
                        url &&
                        isAllowedUrl(
                            url
                        )
                    ) {
                        this.addCandidate(
                            new Candidate({
                                target:
                                    url,

                                type:
                                    'url',

                                origin:
                                    'initial-dom',

                                priority:
                                    0.72,

                                depth: 1
                            })
                        );
                    }
                }
            }

            if (
                CONFIG.discoverResources
            ) {
                const selector = [
                    'script[src]',
                    'link[href]',
                    'img[src]',
                    'iframe[src]',
                    'frame[src]',
                    'source[src]',
                    'video[src]',
                    'audio[src]',
                    'track[src]',
                    'object[data]',
                    'embed[src]',
                    'input[src]'
                ].join(',');

                for (
                    const element of
                    document.querySelectorAll(
                        selector
                    )
                ) {
                    const raw =
                        element.getAttribute(
                            'src'
                        ) ||
                        element.getAttribute(
                            'href'
                        ) ||
                        element.getAttribute(
                            'data'
                        );

                    const url =
                        canonicalizeUrl(
                            raw,
                            location.href
                        );

                    if (
                        url &&
                        isAllowedUrl(
                            url
                        )
                    ) {
                        this.addCandidate(
                            new Candidate({
                                target:
                                    url,

                                type:
                                    'resource',

                                origin:
                                    'initial-dom',

                                priority:
                                    0.55,

                                depth: 1
                            })
                        );
                    }
                }
            }

            if (
                CONFIG.discoverMetadata
            ) {
                const manifest =
                    document.querySelector(
                        'link[rel~="manifest"][href]'
                    );

                if (manifest) {
                    const url =
                        canonicalizeUrl(
                            manifest.getAttribute(
                                'href'
                            ),
                            location.href
                        );

                    if (
                        url &&
                        isAllowedUrl(
                            url
                        )
                    ) {
                        this.addCandidate(
                            new Candidate({
                                target:
                                    url,

                                type:
                                    'manifest',

                                origin:
                                    'initial-dom',

                                priority:
                                    0.85,

                                depth: 1
                            })
                        );
                    }
                }
            }

            if (
                CONFIG.discoverWellKnown
            ) {
                const origin =
                    location.origin;

                const wellKnown = [
                    {
                        path:
                            '/robots.txt',

                        type:
                            'robots',

                        priority:
                            0.88
                    },
                    {
                        path:
                            '/sitemap.xml',

                        type:
                            'sitemap',

                        priority:
                            0.86
                    }
                ];

                for (
                    const item of
                    wellKnown
                ) {
                    const url =
                        canonicalizeUrl(
                            item.path,
                            origin
                        );

                    if (
                        url &&
                        isAllowedUrl(
                            url
                        )
                    ) {
                        this.addCandidate(
                            new Candidate({
                                target:
                                    url,

                                type:
                                    item.type,

                                origin:
                                    'well-known',

                                priority:
                                    item.priority,

                                depth: 1
                            })
                        );
                    }
                }
            }

            log(
                'Seed complete',
                {
                    queue:
                        this.scheduler
                            .size(),

                    inFlight:
                        this.scheduler
                            .inFlight()
                }
            );
        }

        async run() {
            if (
                this.running
            ) {
                return;
            }

            this.resetStats();

            this.running =
                true;

            this.stats.startedAt =
                now();

            log(
                'Starting discovery',
                {
                    concurrency:
                        CONFIG.concurrency,

                    maxRequests:
                        CONFIG.maxRequests,

                    maxDepth:
                        CONFIG.maxDepth,

                    queue:
                        this.scheduler
                            .size()
                }
            );

            const workers = [];

            for (
                let i = 0;
                i < CONFIG.concurrency;
                i++
            ) {
                workers.push(
                    this.worker(i)
                );
            }

            await Promise.all(
                workers
            );

            this.stats.finishedAt =
                now();

            this.running =
                false;

            log(
                'Discovery complete',
                this.stats
            );

            this.report();
        }

        async worker(
            workerId
        ) {
            while (
                this.running &&
                this.stats.requests <
                    CONFIG.maxRequests
            ) {
                const candidate =
                    this.scheduler.claim();

                if (
                    !candidate
                ) {
                    const queueSize =
                        this.scheduler
                            .size();

                    const inFlight =
                        this.scheduler
                            .inFlight();

                    if (
                        queueSize === 0
                    ) {
                        break;
                    }

                    /*
                     * There may be queued retry candidates
                     * waiting for backoff.
                     *
                     * Wait rather than terminating the worker.
                     */
                    const delay =
                        this.scheduler
                            .nextReadyDelay();

                    if (
                        delay === null
                    ) {
                        break;
                    }

                    await sleep(
                        Math.min(
                            Math.max(
                                25,
                                delay
                            ),
                            250
                        )
                    );

                    /*
                     * If other workers are still processing
                     * candidates, loop again and see whether
                     * they have produced new work.
                     */
                    if (
                        inFlight > 0
                    ) {
                        continue;
                    }

                    continue;
                }

                this.stats.requests++;

                log(
                    `Worker ${workerId} claimed`,
                    candidate.target,
                    {
                        type:
                            candidate.type,

                        depth:
                            candidate.depth,

                        attempt:
                            candidate.attempts +
                            1
                    }
                );

                let finalized =
                    false;

                try {
                    const observation =
                        await this.acquisition
                            .acquire(
                                candidate
                            );

                    this.database
                        .addObservation(
                            observation
                        );

                    if (
                        observation.status !==
                        'acquired'
                    ) {
                        this.stats
                            .failures++;

                        const retryable =
                            candidate.attempts <=
                            CONFIG.maxRetries;

                        if (
                            retryable
                        ) {
                            this.stats
                                .retries++;

                            this.scheduler.fail(
                                candidate,
                                true
                            );

                            log(
                                `Worker ${workerId} retry scheduled`,
                                candidate.target,
                                candidate.nextAttemptAt
                            );
                        } else {
                            this.scheduler.fail(
                                candidate,
                                false
                            );
                        }

                        finalized =
                            true;

                        continue;
                    }

                    const result =
                        this.providers
                            .recognize(
                                candidate,
                                observation
                            );

                    if (!result) {
                        this.scheduler.complete(
                            candidate
                        );

                        finalized =
                            true;

                        continue;
                    }

                    const {
                        provider,
                        discovery
                    } = result;

                    this.database
                        .addDiscovery(
                            discovery
                        );

                    this.stats
                        .discoveries++;

                    log(
                        `Worker ${workerId} discovered`,
                        discovery.kind,
                        candidate.target
                    );

                    let newCandidates =
                        [];

                    try {
                        newCandidates =
                            provider.candidates(
                                discovery
                            );
                    } catch (error) {
                        warn(
                            'Candidate expansion failed:',
                            error
                        );
                    }

                    for (
                        const next of
                        newCandidates
                    ) {
                        this.addCandidate(
                            next
                        );
                    }

                    this.scheduler.complete(
                        candidate
                    );

                    finalized =
                        true;
                } catch (error) {
                    warn(
                        `Worker ${workerId} failed:`,
                        error
                    );

                    this.stats
                        .failures++;

                    const retryable =
                        candidate.attempts <=
                        CONFIG.maxRetries;

                    if (
                        retryable
                    ) {
                        this.stats
                            .retries++;

                        this.scheduler.fail(
                            candidate,
                            true
                        );
                    } else {
                        this.scheduler.fail(
                            candidate,
                            false
                        );
                    }

                    finalized =
                        true;
                } finally {
                    /*
                     * Defensive cleanup.
                     *
                     * This prevents a candidate from remaining
                     * permanently claimed if an unexpected path
                     * bypassed the normal finalization logic.
                     */
                    if (
                        !finalized &&
                        this.database
                            .claimed
                            .has(
                                candidate.key()
                            )
                    ) {
                        this.scheduler.fail(
                            candidate,
                            false
                        );
                    }
                }
            }
        }

        export() {
            const discoveries =
                [
                    ...this.database
                        .discoveries
                        .values()
                ];

            const edges =
                [];

            for (
                const discovery of
                discoveries
            ) {
                const parent =
                    discovery
                        .provenance
                        .parent;

                if (
                    parent
                ) {
                    edges.push({
                        from:
                            parent,

                        to:
                            discovery.id,

                        candidate:
                            discovery
                                .provenance
                                .candidateTarget,

                        mechanism:
                            discovery
                                .provenance
                                .mechanism
                    });
                }
            }

            return {
                version: 4,

                scope: {
                    type:
                        'web-resource-discovery',

                    inspiredBy:
                        'DVB blind-scan architecture',

                    rfScanning:
                        false
                },

                timestamp:
                    new Date()
                        .toISOString(),

                page:
                    location.href,

                statistics:
                    this.stats,

                configuration: {
                    maxCandidates:
                        CONFIG.maxCandidates,

                    maxRequests:
                        CONFIG.maxRequests,

                    concurrency:
                        CONFIG.concurrency,

                    maxDepth:
                        CONFIG.maxDepth,

                    sameOriginOnly:
                        CONFIG.sameOriginOnly
                },

                queue: {
                    pending:
                        this.scheduler
                            .size(),

                    inFlight:
                        this.scheduler
                            .inFlight()
                },

                graph: {
                    nodes:
                        discoveries,

                    edges
                },

                discoveries
            };
        }

        report() {
            const discoveries =
                [
                    ...this.database
                        .discoveries
                        .values()
                ];

            console.group(
                '[Discovery] Results'
            );

            console.table(
                discoveries.map(
                    discovery => ({
                        kind:
                            discovery.kind,

                        confidence:
                            discovery.confidence,

                        candidate:
                            discovery
                                .provenance
                                .candidateTarget,

                        mechanism:
                            discovery
                                .provenance
                                .mechanism,

                        depth:
                            discovery
                                .provenance
                                .depth,

                        title:
                            discovery.data
                                ?.title ||
                            '',

                        createdAt:
                            discovery.createdAt
                    })
                )
            );

            console.log(
                'Queue:',
                this.scheduler
                    .size()
            );

            console.log(
                'In flight:',
                this.scheduler
                    .inFlight()
            );

            console.log(
                'Statistics:',
                this.stats
            );

            console.groupEnd();
        }

        clear() {
            this.database.clear();

            this.networkSeen.clear();

            this.resetStats();
        }
    }
