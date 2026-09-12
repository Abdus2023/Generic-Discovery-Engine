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

            this.domObserver =
                null;

            this.running =
                false;

            this.paused =
                false;

            this.stopRequested =
                false;

            this.runId =
                0;

            this.stats =
                this.newStats();

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

                passiveDomEvents: 0,

                providerMisses: 0
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
                this.domObserver ||
                typeof MutationObserver ===
                    'undefined'
            ) {
                return;
            }

            const root =
                document.documentElement;

            if (!root) {
                /*
                 * document-start may execute before <html> exists.
                 */
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
                root,
                {
                    subtree:
                        true,

                    childList:
                        true
                }
            );

            log(
                'DOM observer installed'
            );
        }

        inspectDomNode(node) {
            if (
                !node ||
                !node.querySelectorAll
            ) {
                return;
            }

            const selector = [
                'a[href]',
                'area[href]',
                'script[src]',
                'link[href]',
                'img[src]',
                'iframe[src]',
                'frame[src]',
                'source[src]',
                'video[src]',
                'audio[src]',
                'form[action]',
                'object[data]',
                'embed[src]'
            ].join(',');

            const elements =
                [];

            try {
                if (
                    node.matches?.(
                        selector
                    )
                ) {
                    elements.push(
                        node
                    );
                }

                elements.push(
                    ...node.querySelectorAll(
                        selector
                    )
                );
            } catch {
                return;
            }

            for (
                const element of
                elements
            ) {
                this.observeDomElement(
                    element
                );
            }
        }

        observeDomElement(
            element
        ) {
            let raw =
                null;

            let type =
                'dom-resource';

            if (
                element.matches(
                    'a[href],area[href]'
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
                    ) ||
                    element.getAttribute(
                        'data'
                    );
            }

            const url =
                canonicalizeUrl(
                    raw,
                    location.href
                );

            if (
                !url ||
                !isAllowedUrl(
                    url
                )
            ) {
                return;
            }

            const key =
                `dom:${url}`;

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

            this.addCandidate(
                new Candidate({
                    target:
                        url,

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
                            ? 0.68
                            : 0.46,

                    depth: 0
                })
            );
        }

        recordPassiveNetwork({
            url,
            status = null,
            contentType = null,
            mechanism =
                'network'
        }) {
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
                this.passiveObserved
                    .has(key)
            ) {
                return;
            }

            this.passiveObserved
                .add(key);

            this.stats
                .passiveNetworkEvents++;

            const nodeId =
                this.database.graph
                    .addPassiveObservation(
                        {
                            url:
                                canonical,

                            mechanism,

                            status,

                            contentType
                        }
                    );

            const candidate =
                new Candidate({
                    target:
                        canonical,

                    type:
                        'network-resource',

                    origin:
                        `network:${mechanism}`,

                    priority:
                        mechanism.includes(
                            'response'
                        )
                            ? 0.94
                            : 0.88,

                    depth: 0,

                    hints: {
                        observedStatus:
                            status,

                        observedContentType:
                            contentType,

                        mechanism,

                        passiveNodeId:
                            nodeId
                    }
                });

            this.addCandidate(
                candidate
            );
        }

        addCandidate(
            candidate
        ) {
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
            this.startObservers();

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
                            1,

                        depth:
                            0
                    })
                );
            }

            if (
                CONFIG.discoverLinks
            ) {
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
                                    0.7,

                                depth:
                                    0
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
                                    0.5,

                                depth:
                                    0
                            })
                        );
                    }
                }
            }

            if (
                CONFIG.discoverMetadata
            ) {
                for (
                    const element of
                    document.querySelectorAll(
                        'link[rel][href]'
                    )
                ) {
                    const rel =
                        (
                            element.getAttribute(
                                'rel'
                            ) || ''
                        ).toLowerCase();

                    if (
                        !(
                            rel.includes(
                                'manifest'
                            ) ||
                            rel.includes(
                                'sitemap'
                            ) ||
                            rel.includes(
                                'alternate'
                            ) ||
                            rel.includes(
                                'canonical'
                            )
                        )
                    ) {
                        continue;
                    }

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
                                    'metadata',

                                origin:
                                    'initial-dom',

                                priority:
                                    0.78,

                                depth:
                                    0
                            })
                        );
                    }
                }
            }

            /*
             * Standard discovery endpoints.
             */
            if (
                CONFIG.discoverWellKnown
            ) {
                const origin =
                    location.origin;

                const standard =
                    [
                        [
                            `${origin}/robots.txt`,
                            'robots',
                            0.82
                        ],

                        [
                            `${origin}/sitemap.xml`,
                            'sitemap',
                            0.78
                        ],

                        [
                            `${origin}/sitemap_index.xml`,
                            'sitemap',
                            0.72
                        ]
                    ];

                for (
                    const [
                        target,
                        type,
                        priority
                    ] of standard
                ) {
                    this.addCandidate(
                        new Candidate({
                            target,
                            type,
                            origin:
                                'well-known',
                            priority,
                            depth:
                                0
                        })
                    );
                }
            }

            /*
             * Performance entries may have been created before the
             * PerformanceObserver was installed.
             */
            if (
                CONFIG.observePerformance &&
                typeof performance !==
                    'undefined' &&
                typeof performance.getEntriesByType ===
                    'function'
            ) {
                try {
                    for (
                        const entry of
                        performance.getEntriesByType(
                            'resource'
                        )
                    ) {
                        if (
                            entry?.name
                        ) {
                            this.recordPassiveNetwork(
                                {
                                    url:
                                        entry.name,

                                    mechanism:
                                        'performance-initial'
                                }
                            );
                        }
                    }
                } catch {}
            }

            /*
             * MutationObserver may not have been possible at
             * document-start, so install it again after seeding.
             */
            this.installDomObserver();

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
            if (
                this.running
            ) {
                return;
            }

            this.resetStats();

            this.runId++;
            const currentRun =
                this.runId;

            this.stopRequested =
                false;

            this.paused =
                false;

            this.running =
                true;

            this.stats.startedAt =
                now();

            log(
                'Starting discovery',
                {
                    run:
                        currentRun,

                    concurrency:
                        CONFIG.concurrency,

                    maxRequests:
                        CONFIG.maxRequests,

                    maxDepth:
                        CONFIG.maxDepth
                }
            );

            const workers =
                [];

            for (
                let i = 0;
                i <
                    CONFIG.concurrency;
                i++
            ) {
                workers.push(
                    this.worker(
                        i,
                        currentRun
                    )
                );
            }

            await Promise.all(
                workers
            );

            /*
             * Only the active run may finalize itself.
             */
            if (
                currentRun ===
                this.runId
            ) {
                this.stats.finishedAt =
                    now();

                this.running =
                    false;

                this.paused =
                    false;
            }

            log(
                'Discovery complete',
                this.stats
            );

            this.report();
        }

        async worker(
            workerId,
            currentRun
        ) {
            while (
                this.running &&
                !this.stopRequested &&
                currentRun ===
                    this.runId &&
                this.stats.requests <
                    CONFIG.maxRequests
            ) {
                if (
                    this.paused
                ) {
                    await sleep(
                        100
                    );

                    continue;
                }

                const candidate =
                    this.scheduler.claim();

                if (!candidate) {
                    if (
                        this.scheduler.size() >
                        0
                    ) {
                        await sleep(
                            100
                        );

                        continue;
                    }

                    break;
                }

                this.stats.requests++;

                log(
                    `Worker ${workerId} claimed`,
                    candidate.target
                );

                try {
                    const observation =
                        await this.acquisition
                            .acquire(
                                candidate
                            );

                    if (
                        currentRun !==
                        this.runId
                    ) {
                        /*
                         * The run was superseded.
                         */
                        this.scheduler.fail(
                            candidate,
                            false
                        );

                        continue;
                    }

                    this.database
                        .addObservation(
                            observation
                        );

                    if (
                        observation.status !==
                        'acquired'
                    ) {
                        this.handleFailure(
                            candidate
                        );

                        continue;
                    }

                    const result =
                        this.providers
                            .recognize(
                                candidate,
                                observation
                            );

                    if (!result) {
                        this.stats
                            .providerMisses++;

                        this.scheduler
                            .complete(
                                candidate
                            );

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
                        if (
                            next.depth <=
                            CONFIG.maxDepth
                        ) {
                            this.addCandidate(
                                next
                            );
                        }
                    }

                    this.scheduler
                        .complete(
                            candidate
                        );
                } catch (error) {
                    warn(
                        `Worker ${workerId} failed:`,
                        error
                    );

                    this.handleFailure(
                        candidate
                    );
                }
            }
        }

        handleFailure(
            candidate
        ) {
            this.stats.failures++;

            if (
                candidate.attempts <=
                CONFIG.maxRetries
            ) {
                this.stats.retries++;

                this.scheduler.fail(
                    candidate,
                    true
                );

                return;
            }

            this.scheduler.fail(
                candidate,
                false
            );
        }

        pause() {
            if (
                this.running
            ) {
                this.paused =
                    true;
            }
        }

        resume() {
            if (
                this.running
            ) {
                this.paused =
                    false;
            }
        }

        stop() {
            if (
                !this.running
            ) {
                return;
            }

            this.stopRequested =
                true;

            this.running =
                false;

            this.runId++;

            log(
                'Discovery stopped'
            );
        }

        export() {
            return {
                version:
                    5,

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

                    requestTimeout:
                        CONFIG.requestTimeout,

                    maxDepth:
                        CONFIG.maxDepth,

                    sameOriginOnly:
                        CONFIG.sameOriginOnly
                },

                statistics:
                    this.stats,

                queue: {
                    pending:
                        this.scheduler
                            .size(),

                    inFlight:
                        this.scheduler
                            .inFlight()
                },

                discoveries:
                    [
                        ...this.database
                            .discoveries
                            .values()
                    ],

                provenance:
                    this.database.graph
                        .serialize()
            };
        }

        async importState(
            data
        ) {
            if (
                !data ||
                typeof data !==
                    'object'
            ) {
                throw new Error(
                    'Invalid discovery state'
                );
            }

            if (
                data.version >
                5
            ) {
                throw new Error(
                    'State belongs to a newer engine version'
                );
            }

            if (
                this.running
            ) {
                throw new Error(
                    'Stop the current scan before importing'
                );
            }

            this.database.clear();

            for (
                const key of
                data.provenance
                    ?.nodes || []
            ) {
                if (
                    key?.id
                ) {
                    this.database
                        .graph
                        .nodes.set(
                            key.id,
                            key
                        );
                }
            }

            for (
                const edge of
                data.provenance
                    ?.edges || []
            ) {
                if (
                    edge?.id
                ) {
                    this.database
                        .graph
                        .edges.set(
                            edge.id,
                            edge
                        );
                }
            }

            for (
                const discovery of
                data.discoveries ||
                []
            ) {
                if (
                    discovery?.id
                ) {
                    this.database
                        .discoveries
                        .set(
                            discovery.id,
                            discovery
                        );
                }
            }

            this.database
                .persist();
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

                        mechanism:
                            discovery.mechanism,

                        depth:
                            discovery
                                .provenance
                                ?.depth ??
                            '',

                        type:
                            discovery
                                .provenance
                                ?.candidateType ||
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
            if (
                this.running
            ) {
                return false;
            }

            this.database.clear();

            this.passiveObserved
                .clear();

            this.resetStats();

            return true;
        }
    }
