    class DiscoveryEngine {
        constructor() {
            this.db =
                new KnowledgeBase();

            this.acquisition =
                new HttpAcquisition();

            this.providers =
                new ProviderRegistry();

            this.running =
                false;

            this.stats =
                this.createStats();

            this.networkKeys =
                new Set();

            /*
             * Install passive observers immediately.
             */
            if (
                CONFIG.discoverNetwork
            ) {
                new NetworkBridge(
                    this
                );
            }

            if (
                CONFIG.discoverPerformance
            ) {
                new PerformanceNetworkObserver(
                    this
                );
            }
        }

        createStats() {
            return {
                startedAt: null,
                finishedAt: null,

                requests: 0,

                observations: 0,

                discoveries: 0,

                candidatesCreated: 0,

                candidatesRejected: 0,

                failures: 0,

                retries: 0,

                networkEvents: 0,

                networkCandidates: 0,

                performanceEvents: 0,

                maxDepthSeen: 0
            };
        }

        addCandidate(
            candidate
        ) {
            if (
                candidate.depth >
                CONFIG.maxDepth
            ) {
                return false;
            }

            const added =
                this.db.addCandidate(
                    candidate
                );

            if (added) {
                this.stats
                    .candidatesCreated++;

                this.stats.maxDepthSeen =
                    Math.max(
                        this.stats
                            .maxDepthSeen,
                        candidate.depth
                    );
            } else {
                this.stats
                    .candidatesRejected++;
            }

            return added;
        }

        recordNetwork(
            event
        ) {
            if (
                this.stats.networkEvents >=
                CONFIG.maxNetworkEvents
            ) {
                return;
            }

            this.stats.networkEvents++;

            if (
                event.api ===
                'performance'
            ) {
                this.stats
                    .performanceEvents++;
            }

            this.db.addNetworkEvent(
                event
            );

            /*
             * Do not acquire the same URL repeatedly just
             * because both fetch/XHR and PerformanceObserver
             * saw it.
             */
            const key =
                `${event.url}`;

            if (
                this.networkKeys.has(
                    key
                )
            ) {
                return;
            }

            /*
             * A response is more useful than a request because
             * it gives us content-type and status information.
             *
             * Performance resources are also immediately useful.
             */
            const useful =
                event.phase ===
                    'response' ||
                event.phase ===
                    'resource';

            if (!useful) {
                return;
            }

            const method =
                String(
                    event.method ||
                        'GET'
                ).toUpperCase();

            const safeMethod =
                method === 'GET' ||
                method === 'HEAD' ||
                !event.method;

            if (
                !safeMethod &&
                !CONFIG.acquireObservedNonGet
            ) {
                return;
            }

            this.networkKeys.add(
                key
            );

            let type =
                'network';

            const path =
                (() => {
                    try {
                        return new URL(
                            event.url
                        ).pathname
                            .toLowerCase();
                    } catch {
                        return '';
                    }
                })();

            if (
                isJson(
                    event.contentType
                ) ||
                /\/(api|graphql|rpc)(\/|$)/i.test(
                    path
                ) ||
                /\.(json|graphql)$/i.test(
                    path
                )
            ) {
                type =
                    'api';
            }

            const candidate =
                new Candidate({
                    target:
                        event.url,

                    type,

                    origin:
                        event.api ===
                        'performance'
                            ? 'performance-observer'
                            : `network-${event.api}`,

                    parent:
                        null,

                    depth: 0,

                    priority:
                        type === 'api'
                            ? 0.98
                            : 0.86,

                    hints: {
                        method,

                        status:
                            event.status,

                        contentType:
                            event.contentType,

                        networkApi:
                            event.api
                    }
                });

            if (
                this.addCandidate(
                    candidate
                )
            ) {
                this.stats
                    .networkCandidates++;
            }
        }

        seed() {
            const root =
                canonicalizeUrl(
                    location.href
                );

            if (root) {
                this.addCandidate(
                    new Candidate({
                        target:
                            root,

                        type:
                            'page',

                        origin:
                            'root',

                        priority:
                            1.0,

                        depth: 0
                    })
                );
            }

            /*
             * Seed current DOM.
             */
            for (
                const el of
                document.querySelectorAll(
                    'a[href], area[href]'
                )
            ) {
                const url =
                    canonicalizeUrl(
                        el.getAttribute(
                            'href'
                        ),
                        location.href
                    );

                if (
                    url &&
                    allowed(url)
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
                                0.78,

                            depth: 1
                        })
                    );
                }
            }

            const resourceSelector = [
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
                'embed[src]'
            ].join(',');

            for (
                const el of
                document.querySelectorAll(
                    resourceSelector
                )
            ) {
                const raw =
                    el.getAttribute(
                        'src'
                    ) ||
                    el.getAttribute(
                        'href'
                    ) ||
                    el.getAttribute(
                        'data'
                    );

                const url =
                    canonicalizeUrl(
                        raw,
                        location.href
                    );

                if (
                    !url ||
                    !allowed(url)
                ) {
                    continue;
                }

                const tag =
                    el.tagName
                        .toLowerCase();

                const type =
                    tag === 'script'
                        ? 'script'
                        : tag === 'img'
                        ? 'media'
                        : tag === 'iframe' ||
                          tag === 'frame'
                        ? 'frame'
                        : 'resource';

                this.addCandidate(
                    new Candidate({
                        target:
                            url,

                        type,

                        origin:
                            'initial-dom',

                        priority:
                            type ===
                            'script'
                                ? 0.60
                                : 0.42,

                        depth: 1
                    })
                );
            }

            if (
                CONFIG.discoverWellKnown
            ) {
                for (
                    const item of [
                        {
                            path:
                                '/robots.txt',

                            type:
                                'robots',

                            priority:
                                0.90
                        },
                        {
                            path:
                                '/sitemap.xml',

                            type:
                                'sitemap',

                            priority:
                                0.86
                        }
                    ]
                ) {
                    const url =
                        canonicalizeUrl(
                            item.path,
                            location.origin
                        );

                    if (url) {
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
                'Seeded',
                this.db.queueSize(),
                'candidates'
            );
        }

        async run() {
            if (
                this.running
            ) {
                return;
            }

            this.running =
                true;

            this.stats =
                this.createStats();

            this.stats.startedAt =
                now();

            const workers =
                [];

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

            this.db.persist();

            log(
                'Finished',
                this.stats
            );
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
                    this.db.claimNext();

                if (!candidate) {
                    const queue =
                        this.db.queueSize();

                    if (!queue) {
                        break;
                    }

                    const delay =
                        this.db.nextDelay();

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

                    continue;
                }

                this.stats.requests++;

                try {
                    candidate.status =
                        'acquiring';

                    const observation =
                        await this.acquisition
                            .acquire(
                                candidate
                            );

                    this.stats
                        .observations++;

                    this.db.addObservation(
                        observation
                    );

                    if (
                        observation.status !==
                        'observed'
                    ) {
                        await this.handleFailure(
                            candidate
                        );

                        continue;
                    }

                    /*
                     * Calculate the fingerprint after acquisition.
                     */
                    observation.fingerprint
                        .sha256 =
                        await hashText(
                            observation.body
                        );

                    candidate.status =
                        'observed';

                    const result =
                        this.providers
                            .recognize(
                                candidate,
                                observation
                            );

                    if (!result) {
                        this.db.complete(
                            candidate
                        );

                        continue;
                    }

                    candidate.status =
                        'recognized';

                    const {
                        provider,
                        discoveries
                    } = result;

                    for (
                        const discovery of
                        discoveries
                    ) {
                        this.db.addDiscovery(
                            discovery
                        );

                        this.stats
                            .discoveries++;

                        this.expand(
                            provider,
                            discovery
                        );
                    }

                    this.db.complete(
                        candidate
                    );

                    log(
                        `worker ${workerId}`,
                        candidate.target,
                        'completed'
                    );
                } catch (error) {
                    warn(
                        `worker ${workerId}`,
                        error
                    );

                    await this.handleFailure(
                        candidate,
                        error
                    );
                }
            }
        }

        async handleFailure(
            candidate,
            error = null
        ) {
            candidate.lastError =
                error
                    ? String(error)
                    : 'acquisition failed';

            this.stats.failures++;

            const retry =
                candidate.attempts <=
                CONFIG.maxRetries;

            if (retry) {
                this.stats.retries++;

                this.db.fail(
                    candidate,
                    true
                );
            } else {
                this.db.fail(
                    candidate,
                    false
                );
            }
        }

        expand(
            provider,
            discovery
        ) {
            let candidates =
                [];

            try {
                candidates =
                    provider.candidates(
                        discovery
                    ) || [];
            } catch (error) {
                warn(
                    'Expansion error',
                    error
                );

                return;
            }

            for (
                const candidate of
                candidates
            ) {
                if (
                    candidate.depth >
                    CONFIG.maxDepth
                ) {
                    continue;
                }

                this.addCandidate(
                    candidate
                );
            }
        }

        buildGraph() {
            const nodes =
                [];

            const edges =
                [];

            const nodeIds =
                new Set();

            const rootId =
                'root';

            nodes.push({
                id:
                    rootId,

                kind:
                    'root',

                target:
                    location.href,

                depth: 0
            });

            nodeIds.add(
                rootId
            );

            for (
                const discovery of
                this.db.discoveries.values()
            ) {
                const target =
                    discovery.data
                        ?.finalUrl ||
                    discovery.data
                        ?.url ||
                    discovery
                        .provenance
                        .candidateTarget;

                nodes.push({
                    id:
                        discovery.id,

                    kind:
                        discovery.kind,

                    target,

                    confidence:
                        discovery.confidence,

                    mechanism:
                        discovery
                            .provenance
                            .mechanism,

                    depth:
                        discovery
                            .provenance
                            .depth,

                    parent:
                        discovery
                            .provenance
                            .parent
                });

                nodeIds.add(
                    discovery.id
                );

                const parent =
                    discovery
                        .provenance
                        .parent;

                edges.push({
                    id:
                        id('edge'),

                    from:
                        parent &&
                        nodeIds.has(
                            parent
                        )
                            ? parent
                            : rootId,

                    to:
                        discovery.id,

                    relationship:
                        discovery
                            .provenance
                            .mechanism
                });
            }

            /*
             * Network events are represented as separate graph
             * nodes. They intentionally do not contain response
             * bodies.
             */
            for (
                const event of
                this.db.networkEvents.values()
            ) {
                const nodeId =
                    event.id;

                nodes.push({
                    id:
                        nodeId,

                    kind:
                        'network-event',

                    target:
                        event.url,

                    api:
                        event.api,

                    phase:
                        event.phase,

                    method:
                        event.method,

                    status:
                        event.status,

                    contentType:
                        event.contentType,

                    timestamp:
                        event.timestamp
                });

                edges.push({
                    id:
                        id('edge'),

                    from:
                        rootId,

                    to:
                        nodeId,

                    relationship:
                        'network-observation'
                });
            }

            return {
                nodes,
                edges
            };
        }

        export() {
            return {
                version: 5,

                engine:
                    'Generic Discovery Engine',

                architecture:
                    'candidate -> acquisition -> observation -> recognition -> discovery -> candidate',

                timestamp:
                    new Date()
                        .toISOString(),

                page:
                    location.href,

                configuration: {
                    ...CONFIG
                },

                statistics:
                    this.stats,

                queue: {
                    pending:
                        this.db.queueSize(),

                    inFlight:
                        this.db.inFlight()
                },

                graph:
                    this.buildGraph(),

                candidates:
                    [
                        ...this.db
                            .candidates
                            .values()
                    ],

                observations:
                    [
                        ...this.db
                            .observations
                            .values()
                    ].map(
                        observation => ({
                            ...observation,

                            /*
                             * Exported observations do not contain
                             * response bodies.
                             */
                            body:
                                undefined
                        })
                    ),

                discoveries:
                    [
                        ...this.db
                            .discoveries
                            .values()
                    ],

                networkEvents:
                    [
                        ...this.db
                            .networkEvents
                            .values()
                    ]
            };
        }

        clear() {
            this.db.clear();

            this.networkKeys.clear();

            this.stats =
                this.createStats();
        }
    }
