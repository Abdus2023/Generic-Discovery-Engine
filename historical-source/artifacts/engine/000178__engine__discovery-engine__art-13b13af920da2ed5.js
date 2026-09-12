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

            this.networkObserver =
                new NetworkObserver(
                    this
                );

            this.running =
                false;

            this.stats =
                this.newStats();

            /*
             * Passive observations are deduplicated independently from
             * active candidates.
             */
            this.passiveObserved =
                new Set();
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

                passiveNetworkEvents: 0,

                passiveDomEvents: 0
            };
        }

        resetStats() {
            this.stats =
                this.newStats();
        }

        startObservers() {
            this.networkObserver
                .install();

            if (
                CONFIG.observeDomResources
            ) {
                this.installDomObserver();
            }
        }

        installDomObserver() {
            if (
                this.domObserver
            ) {
                return;
            }

            if (
                typeof MutationObserver ===
                'undefined'
            ) {
                return;
            }

            this.domObserver =
                new MutationObserver(
                    mutations => {
                        for (
                            const mutation of
                            mutations
                        ) {
                            for (
                                const node of
                                mutation.addedNodes
                            ) {
                                if (
                                    node.nodeType !==
                                    Node.ELEMENT_NODE
                                ) {
                                    continue;
                                }

                                this.inspectDomNode(
                                    node
                                );
                            }
                        }
                    }
                );

            this.domObserver.observe(
                document.documentElement,
                {
                    subtree: true,
                    childList: true
                }
            );

            log(
                'DOM observer installed'
            );
        }

        inspectDomNode(node) {
            if (
                !node.querySelectorAll
            ) {
                return;
            }

            const selector = [
                'a[href]',
                'script[src]',
                'link[href]',
                'img[src]',
                'iframe[src]',
                'source[src]',
                'video[src]',
                'audio[src]',
                'form[action]'
            ].join(',');

            const elements = [];

            if (
                node.matches?.(
                    selector
                )
            ) {
                elements.push(node);
            }

            elements.push(
                ...node.querySelectorAll(
                    selector
                )
            );

            for (
                const element of
                elements
            ) {
                this.observeDomElement(
                    element
                );
            }
        }

        observeDomElement(element) {
            let raw = null;
            let type = 'dom-resource';

            if (
                element.matches(
                    'a[href]'
                )
            ) {
                raw =
                    element.getAttribute(
                        'href'
                    );

                type =
                    'dom-link';
            } else if (
                element.matches(
                    'form[action]'
                )
            ) {
                raw =
                    element.getAttribute(
                        'action'
                    );

                type =
                    'dom-form';
            } else {
                raw =
                    element.getAttribute(
                        'src'
                    ) ||
                    element.getAttribute(
                        'href'
                    );
            }

            const url =
                canonicalizeUrl(
                    raw,
                    location.href
                );

            if (
                !url ||
                !isAllowedUrl(url)
            ) {
                return;
            }

            const key =
                `${type}:${url}`;

            if (
                this.passiveObserved
                    .has(key)
            ) {
                return;
            }

            this.passiveObserved
                .add(key);

            this.stats
                .passiveDomEvents++;

            /*
             * Passive DOM observations are turned into candidates.
             */
            this.addCandidate(
                new Candidate({
                    target: url,

                    type:
                        type ===
                        'dom-link'
                            ? 'url'
                            : 'resource',

                    origin:
                        'passive-dom',

                    priority:
                        type ===
                        'dom-link'
                            ? 0.65
                            : 0.45,

                    depth: 0
                })
            );
        }

        recordPassiveNetwork({
            url,
            status,
            contentType,
            mechanism
        }) {
            if (
                !url ||
                !isAllowedUrl(url)
            ) {
                return;
            }

            const key =
                `${mechanism}:${url}`;

            if (
                this.passiveObserved
                    .has(key)
            ) {
                return;
            }

            this.passiveObserved
                .add(key);

            this.stats
                .passiveNetworkEvents++;

            /*
             * A network-observed resource is a high-quality candidate
             * because the page itself has already demonstrated that
             * the resource exists or was attempted.
             */
            const candidate =
                new Candidate({
                    target: url,

                    type:
                        'network-resource',

                    origin:
                        `network:${mechanism}`,

                    priority:
                        0.9,

                    depth: 0,

                    hints: {
                        observedStatus:
                            status,

                        observedContentType:
                            contentType,

                        mechanism
                    }
                });

            this.addCandidate(
                candidate
            );

            log(
                'Passive network observation',
                mechanism,
                url
            );
        }

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
             * Start passive observers before scanning the current DOM.
             */
            this.startObservers();

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

                        priority:
                            1.0,

                        depth: 0
                    })
                );
            }

            /*
             * Existing links.
             */
            if (CONFIG.discoverLinks) {
                for (
                    const element of
                    document.querySelectorAll(
                        'a[href],area[href]'
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
                        isAllowedUrl(url)
                    ) {
                        this.addCandidate(
                            new Candidate({
                                target: url,

                                type:
                                    'url',

                                origin:
                                    'initial-dom',

                                priority:
                                    0.7,

                                depth: 0
                            })
                        );
                    }
                }
            }

            /*
             * Existing resources.
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
                    'audio[src]',
                    'track[src]'
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

                                priority:
                                    0.5,

                                depth: 0
                            })
                        );
                    }
                }
            }

            /*
             * Also inspect the initial DOM through the same passive path.
             */
            if (
                this.domObserver
            ) {
                this.inspectDomNode(
                    document.documentElement
                );
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
                        CONFIG.maxDepth
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

        async worker(workerId) {
            while (
                this.running &&
                this.stats.requests <
                    CONFIG.maxRequests
            ) {
                const candidate =
                    this.scheduler.claim();

                if (!candidate) {
                    /*
                     * A queue can temporarily contain only candidates
                     * waiting for retry backoff.
                     *
                     * Give them a chance to become eligible rather than
                     * immediately terminating all workers.
                     */
                    if (
                        this.scheduler.size() >
                        0
                    ) {
                        await this.sleep(
                            100
                        );

                        continue;
                    }

                    break;
                }

                /*
                 * Synchronous reservation.
                 */
                this.stats.requests++;

                log(
                    `Worker ${workerId} claimed`,
                    candidate.target
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
                        this.scheduler
                            .complete(
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

                    const newCandidates =
                        provider.candidates(
                            discovery
                        );

                    for (
                        const next of
                        newCandidates
                    ) {
                        this.addCandidate(
                            next
                        );
                    }

                    this.scheduler
                        .complete(
                            candidate
                        );

                    finalized =
                        true;
                } catch (error) {
                    warn(
                        `Worker ${workerId} error:`,
                        error
                    );

                    this.stats
                        .failures++;

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

                    finalized =
                        true;
                }

                /*
                 * Defensive ownership cleanup.
                 */
                if (
                    !finalized &&
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

        sleep(ms) {
            return new Promise(
                resolve =>
                    setTimeout(
                        resolve,
                        ms
                    )
            );
        }

        export() {
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
                ],

                provenance:
                    this.database.graph
                        .serialize()
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

                        mechanism:
                            discovery.mechanism,

                        depth:
                            discovery.provenance
                                ?.depth ??
                            '',

                        url:
                            discovery.data
                                ?.url ||
                            '',

                        title:
                            discovery.data
                                ?.title ||
                            ''
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
                'Graph nodes:',
                this.database.graph
                    .nodes.size
            );

            console.log(
                'Graph edges:',
                this.database.graph
                    .edges.size
            );

            console.log(
                'Statistics:',
                this.stats
            );

            console.groupEnd();
        }

        clear() {
            this.database.clear();

            this.passiveObserved
                .clear();

            this.resetStats();
        }
    }
