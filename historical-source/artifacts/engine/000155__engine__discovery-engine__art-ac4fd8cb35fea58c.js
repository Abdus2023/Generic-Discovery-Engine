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

            this.running = false;

            this.stats = this.newStats();
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
                candidatesRejected: 0
            };
        }

        resetStats() {
            this.stats =
                this.newStats();
        }

        /*
         * Add a candidate through one central path so statistics remain
         * consistent.
         */
        addCandidate(candidate) {
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

        seed() {
            /*
             * Seed the current document.
             */
            const current =
                canonicalizeUrl(
                    location.href
                );

            if (current) {
                this.addCandidate(
                    new Candidate({
                        target: current,
                        type: 'url',
                        origin:
                            'initial-page',
                        priority: 1.0
                    })
                );
            }

            /*
             * Discover links already present in the loaded DOM.
             *
             * These do not require another request merely to become
             * candidates.
             */
            if (CONFIG.discoverLinks) {
                const elements =
                    document.querySelectorAll(
                        'a[href], area[href]'
                    );

                for (
                    const element of
                    elements
                ) {
                    const raw =
                        element.getAttribute(
                            'href'
                        );

                    const url =
                        canonicalizeUrl(
                            raw,
                            location.href
                        );

                    if (
                        url &&
                        isAllowedUrl(url)
                    ) {
                        this.addCandidate(
                            new Candidate({
                                target: url,
                                type: 'url',
                                origin:
                                    'initial-dom',
                                priority: 0.7
                            })
                        );
                    }
                }
            }

            /*
             * Seed resources already visible in the DOM.
             */
            if (CONFIG.discoverResources) {
                const selector = [
                    'script[src]',
                    'link[href]',
                    'img[src]',
                    'iframe[src]',
                    'frame[src]',
                    'source[src]',
                    'video[src]',
                    'audio[src]'
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
                        );

                    const url =
                        canonicalizeUrl(
                            raw,
                            location.href
                        );

                    if (
                        url &&
                        isAllowedUrl(url)
                    ) {
                        this.addCandidate(
                            new Candidate({
                                target: url,
                                type:
                                    'resource',
                                origin:
                                    'initial-dom',
                                priority: 0.5
                            })
                        );
                    }
                }
            }

            log(
                'Seed complete',
                {
                    queue:
                        this.scheduler.size()
                }
            );
        }

        async run() {
            if (this.running) {
                return;
            }

            /*
             * Each Scan button starts a fresh statistics interval,
             * while the knowledge base remains persistent.
             */
            this.resetStats();

            this.running = true;

            this.stats.startedAt =
                now();

            log(
                'Starting discovery',
                {
                    concurrency:
                        CONFIG.concurrency,

                    maxRequests:
                        CONFIG.maxRequests,

                    queue:
                        this.scheduler.size()
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

            this.running = false;

            log(
                'Discovery complete',
                this.stats
            );

            this.report();
        }

        async worker(workerId) {
            while (
                this.running &&
                this.stats.requests <
                    CONFIG.maxRequests
            ) {
                /*
                 * CLAIM FIRST.
                 *
                 * This is synchronous and establishes worker ownership
                 * before any asynchronous network operation.
                 */
                const candidate =
                    this.scheduler.claim();

                if (!candidate) {
                    break;
                }

                /*
                 * The increment is also synchronous, so two workers
                 * cannot observe and increment the same request count
                 * between awaits.
                 */
                this.stats.requests++;

                log(
                    `Worker ${workerId} claimed`,
                    candidate.target
                );

                let completed = false;

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

                        /*
                         * Retry only while the candidate still has
                         * retry budget.
                         */
                        if (
                            candidate.attempts <=
                            CONFIG.maxRetries
                        ) {
                            this.stats
                                .retries++;

                            this.scheduler.fail(
                                candidate,
                                true
                            );

                            log(
                                `Worker ${workerId} retrying`,
                                candidate.target
                            );
                        } else {
                            this.scheduler.fail(
                                candidate,
                                false
                            );
                        }

                        continue;
                    }

                    const result =
                        this.providers.recognize(
                            candidate,
                            observation
                        );

                    if (!result) {
                        this.scheduler.complete(
                            candidate
                        );

                        completed = true;

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

                    /*
                     * Provider expands the search space.
                     */
                    const newCandidates =
                        provider.candidates(
                            discovery
                        );

                    for (
                        const next
                        of newCandidates
                    ) {
                        this.addCandidate(
                            next
                        );
                    }

                    this.scheduler.complete(
                        candidate
                    );

                    completed = true;
                } catch (error) {
                    warn(
                        `Worker ${workerId} failed:`,
                        error
                    );

                    this.stats
                        .failures++;

                    /*
                     * Retry unexpected failures as well.
                     */
                    if (
                        candidate.attempts <=
                        CONFIG.maxRetries
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
                }

                /*
                 * Defensive cleanup.
                 *
                 * Normally all paths above already complete/fail the
                 * candidate. This prevents an accidental future code
                 * path from leaving it permanently claimed.
                 */
                if (
                    !completed &&
                    this.database.claimed.has(
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

        export() {
            return {
                version: 3,

                scope: {
                    type:
                        'web-resource-discovery',

                    inspiredBy:
                        'DVB blind-scan architecture',

                    rfScanning:
                        false
                },

                timestamp:
                    new Date().toISOString(),

                page:
                    location.href,

                statistics:
                    this.stats,

                queue: {
                    pending:
                        this.scheduler.size(),

                    inFlight:
                        this.scheduler.inFlight()
                },

                discoveries: [
                    ...this.database
                        .discoveries
                        .values()
                ]
            };
        }

        report() {
            const discoveries = [
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

                        url:
                            discovery.data.url ||
                            '',

                        title:
                            discovery.data.title ||
                            '',

                        createdAt:
                            discovery.createdAt
                    })
                )
            );

            console.log(
                'Queue:',
                this.scheduler.size()
            );

            console.log(
                'In flight:',
                this.scheduler.inFlight()
            );

            console.log(
                'Statistics:',
                this.stats
            );

            console.groupEnd();
        }

        clear() {
            this.database.clear();
            this.resetStats();
        }
    }
