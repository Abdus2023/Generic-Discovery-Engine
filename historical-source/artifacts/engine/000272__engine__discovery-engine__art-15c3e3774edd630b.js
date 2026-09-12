    class DiscoveryEngine {
        constructor() {
            this.db =
                new KnowledgeBase(
                    this
                );

            this.acquisition =
                new HttpAcquisition();

            this.providers =
                new ProviderRegistry();

            this.running =
                false;

            this.stats =
                this.createStats();

            this.networkCandidateKeys =
                new Set();

            new NetworkBridge(
                this
            );

            new PerformanceObserverAdapter(
                this
            );
        }

        createStats() {
            return {
                startedAt:
                    null,

                finishedAt:
                    null,

                requests:
                    0,

                observations:
                    0,

                discoveries:
                    0,

                candidatesCreated:
                    0,

                candidatesMerged:
                    0,

                candidatesRejected:
                    0,

                candidateLimitHits:
                    0,

                maxDepthRejected:
                    0,

                maxDepthSeen:
                    0,

                maxDepthReached:
                    0,

                maxRequestsReached:
                    0,

                failures:
                    0,

                retries:
                    0,

                cacheSkips:
                    0,

                networkEvents:
                    0,

                networkCandidates:
                    0,

                performanceEvents:
                    0
            };
        }

        addCandidate(
            candidate
        ) {
            if (
                !candidate?.target
            ) {
                return false;
            }

            const before =
                this.stats
                    .candidatesCreated;

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

                if (
                    candidate.depth ===
                    CONFIG.maxDepth
                ) {
                    this.stats
                        .maxDepthReached++;
                }
            } else if (
                this.stats
                    .candidatesCreated ===
                before
            ) {
                this.stats
                    .candidatesRejected++;
            }

            return added;
        }

        handleNetworkEvent(
            event
        ) {
            this.stats
                .networkEvents++;

            if (
                event.api ===
                'performance'
            ) {
                this.stats
                    .performanceEvents++;
            }

            const stored =
                this.db.addNetworkEvent(
                    event
                );

            /*
             * Requests themselves are observations, but not yet
             * sufficient to justify an acquisition candidate.
             */
            if (
                stored.phase ===
                'request'
            ) {
                return;
            }

            if (
                stored.phase !==
                    'response' &&
                stored.phase !==
                    'resource'
            ) {
                return;
            }

            const method =
                String(
                    stored.method ||
                        'GET'
                ).toUpperCase();

            const safe =
                method === 'GET' ||
                method === 'HEAD' ||
                !stored.method;

            if (
                !safe &&
                !CONFIG.acquireObservedNonGet
            ) {
                return;
            }

            const target =
                stored.url;

            if (
                !target ||
                !allowed(target)
            ) {
                return;
            }

            const type =
                classifyUrl(
                    target,
                    stored.contentType
                );

            const key =
                `${target}|${type}`;

            if (
                this.networkCandidateKeys.has(
                    key
                )
            ) {
                return;
            }

            this.networkCandidateKeys.add(
                key
            );

            const candidate =
                new Candidate({
                    target,

                    type,

                    origin:
                        stored.api ===
                        'performance'
                            ? 'performance-observer'
                            : `network-${stored.api}`,

                    depth:
                        0,

                    priority:
                        type === 'api'
                            ? 0.98
                            : 0.82,

                    hints: {
                        confidence:
                            stored.api ===
                            'performance'
                                ? 0.76
                                : 0.94,

                        method,

                        status:
                            stored.status,

                        contentType:
                            stored.contentType,

                        requestId:
                            stored.requestId,

                        finalUrl:
                            stored.finalUrl
                    }
                });

            if (
                this.addCandidate(
                    candidate
                )
            ) {
                this.stats
                    .networkCandidates++;

                stored.candidateCreated =
                    true;
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

                        depth:
                            0,

                        priority:
                            1.0
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
                            )
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

                                depth:
                                    1,

                                priority:
                                    0.78
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
                    'embed[src]'
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
                            raw
                        );

                    if (
                        !url ||
                        !allowed(url)
                    ) {
                        continue;
                    }

                    const tag =
                        element.tagName
                            .toLowerCase();

                    let type =
                        classifyUrl(
                            url
                        );

                    if (
                        tag ===
                        'script'
                    ) {
                        type =
                            'script';
                    } else if (
                        tag ===
                        'link'
                    ) {
                        const rel =
                            (
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
                        }
                    } else if (
                        tag ===
                            'iframe' ||
                        tag ===
                            'frame'
                    ) {
                        type =
                            'frame';
                    } else if (
                        [
                            'img',
                            'video',
                            'audio',
                            'source',
                            'track'
                        ].includes(
                            tag
                        )
                    ) {
                        type =
                            'media';
                    }

                    this.addCandidate(
                        new Candidate({
                            target:
                                url,

                            type,

                            origin:
                                'initial-dom',

                            depth:
                                1,

                            priority:
                                TYPE_PRIORITY[
                                    type
                                ] ??
                                0.40
                        })
                    );
                }
            }

            if (
                CONFIG.discoverWellKnown
            ) {
                for (
                    const item of [
                        [
                            '/robots.txt',
                            'robots',
                            0.90
                        ],
                        [
                            '/sitemap.xml',
                            'sitemap',
                            0.86
                        ]
                    ]
                ) {
                    const url =
                        canonicalizeUrl(
                            item[0],
                            location.origin
                        );

                    if (url) {
                        this.addCandidate(
                            new Candidate({
                                target:
                                    url,

                                type:
                                    item[1],

                                origin:
                                    'well-known',

                                depth:
                                    1,

                                priority:
                                    item[2]
                            })
                        );
                    }
                }
            }
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

            if (
                this.stats.requests >=
                CONFIG.maxRequests
            ) {
                this.stats
                    .maxRequestsReached++;
            }

            this.stats.finishedAt =
                now();

            this.running =
                false;

            this.db.persist();
        }

        async worker(
            workerId
        ) {
            while (
                this.running
            ) {
                if (
                    this.stats.requests >=
                    CONFIG.maxRequests
                ) {
                    break;
                }

                const candidate =
                    this.db.claimNext();

                if (!candidate) {
                    if (
                        this.db.queueSize() ===
                        0
                    ) {
                        if (
                            this.db.inFlight() >
                            0
                        ) {
                            await sleep(
                                50
                            );

                            continue;
                        }

                        break;
                    }

                    const delay =
                        this.db.nextDelay();

                    if (
                        delay !== null
                    ) {
                        await sleep(
                            Math.min(
                                Math.max(
                                    25,
                                    delay
                                ),
                                250
                            )
                        );
                    }

                    continue;
                }

                /*
                 * Resource-level reuse check.
                 */
                const resource =
                    this.db.getResource(
                        candidate.target
                    );

                if (
                    resource?.status ===
                        'acquired' &&
                    resource.fingerprint
                ) {
                    this.stats
                        .cacheSkips++;

                    candidate.lifecycle(
                        'observed'
                    );

                    this.db.complete(
                        candidate
                    );

                    continue;
                }

                if (
                    this.stats.requests >=
                    CONFIG.maxRequests
                ) {
                    this.db.fail(
                        candidate,
                        false
                    );

                    break;
                }

                this.stats.requests++;

                candidate.lifecycle(
                    'acquiring'
                );

                resource.status =
                    'acquiring';

                try {
                    const observation =
                        await this.acquisition
                            .acquire(
                                candidate.target
                            );

                    this.stats
                        .observations++;

                    if (
                        observation.body
                    ) {
                        observation.fingerprint =
                            {
                                length:
                                    observation.body
                                        .length,

                                sha256:
                                    await sha256(
                                        observation.body
                                    )
                            };
                    } else {
                        observation.fingerprint =
                            {
                                length:
                                    observation
                                        .http
                                        .contentLength,

                                sha256:
                                    null
                            };
                    }

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

                    candidate.lifecycle(
                        'observed'
                    );

                    const finalUrl =
                        canonicalizeUrl(
                            observation
                                .http
                                .finalUrl
                        );

                    if (
                        finalUrl &&
                        finalUrl !==
                            candidate.target
                    ) {
                        this.recordRedirect(
                            candidate.target,
                            finalUrl,
                            candidate
                        );
                    }

                    const matches =
                        this.providers
                            .recognize(
                                candidate,
                                observation
                            );

                    candidate.lifecycle(
                        'recognized'
                    );

                    for (
                        const match of
                        matches
                    ) {
                        for (
                            const discovery of
                            match.discoveries
                        ) {
                            this.db
                                .addDiscovery(
                                    discovery
                                );

                            this.stats
                                .discoveries++;

                            const generated =
                                match.provider
                                    .candidates(
                                        discovery
                                    ) || [];

                            candidate.lifecycle(
                                'expanded'
                            );

                            for (
                                const next of
                                generated
                            ) {
                                this.addCandidate(
                                    next
                                );
                            }
                        }
                    }

                    resource.status =
                        'acquired';

                    this.db.complete(
                        candidate
                    );

                    log(
                        `worker ${workerId}`,
                        candidate.target,
                        'completed'
                    );
                } catch (error) {
                    await this.handleFailure(
                        candidate,
                        error
                    );
                }
            }
        }

        async handleFailure(
            candidate,
            error
        ) {
            this.stats.failures++;

            candidate.lastError =
                error
                    ? String(error)
                    : 'acquisition failed';

            const retry =
                candidate.attempts <
                CONFIG.maxRetries + 1;

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

        recordRedirect(
            from,
            to,
            candidate
        ) {
            if (
                this.db.edges.size >=
                CONFIG.maxGraphEdges
            ) {
                return;
            }

            const key =
                `redirect|${from}|${to}`;

            if (
                this.db.edges.has(
                    key
                )
            ) {
                return;
            }

            this.db.edges.set(
                key,
                {
                    id:
                        makeId('edge'),

                    fromUrl:
                        from,

                    target:
                        to,

                    relationship:
                        'redirect',

                    mechanism:
                        'http-acquisition',

                    candidateType:
                        candidate.type,

                    createdAt:
                        now()
                }
            );
        }

        buildGraph() {
            const nodes =
                [];

            const edges =
                [];

            const resourceNodeIds =
                new Map();

            nodes.push({
                id:
                    'root',

                kind:
                    'root',

                url:
                    canonicalizeUrl(
                        location.href
                    ),

                title:
                    document.title ||
                    ''
            });

            for (
                const resource of
                this.db.resources.values()
            ) {
                const nodeId =
                    resource.id;

                resourceNodeIds.set(
                    resource.url,
                    nodeId
                );

                nodes.push({
                    id:
                        nodeId,

                    kind:
                        'resource',

                    url:
                        resource.url,

                    finalUrl:
                        resource.finalUrl,

                    types:
                        [
                            ...resource.types
                        ],

                    mechanisms:
                        [
                            ...resource
                                .mechanisms
                        ],

                    status:
                        resource.status,

                    firstSeenAt:
                        resource.firstSeenAt,

                    lastSeenAt:
                        resource.lastSeenAt,

                    acquisitionCount:
                        resource
                            .acquisitionCount,

                    fingerprint:
                        resource.fingerprint
                });
            }

            /*
             * Candidate provenance edges.
             */
            for (
                const edge of
                this.db.edges.values()
            ) {
                if (
                    edge.relationship ===
                    'redirect'
                ) {
                    const fromId =
                        resourceNodeIds.get(
                            edge.fromUrl
                        );

                    const toId =
                        resourceNodeIds.get(
                            edge.target
                        );

                    if (
                        fromId &&
                        toId &&
                        fromId !== toId
                    ) {
                        edges.push({
                            id:
                                edge.id,

                            from:
                                fromId,

                            to:
                                toId,

                            relationship:
                                'redirect',

                            mechanism:
                                edge.mechanism,

                            candidateType:
                                edge.candidateType
                        });
                    }

                    continue;
                }

                let fromId =
                    'root';

                if (
                    edge.fromDiscoveryId
                ) {
                    const discovery =
                        this.db
                            .discoveries
                            .get(
                                edge.fromDiscoveryId
                            );

                    if (
                        discovery
                    ) {
                        const source =
                            discovery
                                .target();

                        fromId =
                            resourceNodeIds.get(
                                source
                            ) ||
                            'root';
                    }
                }

                const toId =
                    resourceNodeIds.get(
                        edge.target
                    );

                if (
                    !toId
                ) {
                    continue;
                }

                if (
                    fromId ===
                    toId
                ) {
                    continue;
                }

                edges.push({
                    id:
                        edge.id,

                    from:
                        fromId,

                    to:
                        toId,

                    relationship:
                        edge.relationship,

                    mechanism:
                        edge.mechanism,

                    candidateType:
                        edge.candidateType,

                    priority:
                        edge.priority,

                    depth:
                        edge.depth
                });
            }

            /*
             * Network observation edges.
             */
            for (
                const event of
                this.db.networkEvents.values()
            ) {
                const toId =
                    resourceNodeIds.get(
                        event.url
                    );

                if (
                    !toId
                ) {
                    continue;
                }

                edges.push({
                    id:
                        makeId('edge'),

                    from:
                        'root',

                    to:
                        toId,

                    relationship:
                        'network-observation',

                    mechanism:
                        event.api,

                    requestId:
                        event.requestId,

                    method:
                        event.method,

                    status:
                        event.status
                });
            }

            return {
                nodes,
                edges:
                    edges.slice(
                        0,
                        CONFIG.maxGraphEdges
                    )
            };
        }

        export() {
            return {
                version:
                    '0.6.0',

                engine:
                    'Generic Discovery Engine',

                scope: {
                    type:
                        'web-resource-discovery',

                    sameOriginOnly:
                        CONFIG.sameOriginOnly,

                    rfScanning:
                        false
                },

                architecture: [
                    'candidate',
                    'scheduler',
                    'acquisition',
                    'observation',
                    'recognition',
                    'discovery',
                    'candidate'
                ],

                timestamp:
                    new Date()
                        .toISOString(),

                page: {
                    url:
                        location.href,

                    title:
                        document.title ||
                        ''
                },

                configuration:
                    {
                        ...CONFIG
                    },

                statistics:
                    {
                        ...this.stats,

                        resources:
                            this.db
                                .resources
                                .size,

                        pending:
                            this.db
                                .queueSize(),

                        inFlight:
                            this.db
                                .inFlight(),

                        graphEdges:
                            this.db
                                .edges
                                .size
                    },

                lifecycle: {
                    discovered:
                        'candidate created',

                    queued:
                        'candidate available to scheduler',

                    claimed:
                        'candidate atomically claimed',

                    acquiring:
                        'acquisition in progress',

                    observed:
                        'acquisition produced observation',

                    recognized:
                        'provider recognized observation',

                    expanded:
                        'provider generated new candidates',

                    completed:
                        'candidate finished',

                    failed:
                        'candidate exhausted retries'
                },

                graph:
                    this.buildGraph(),

                resources:
                    [
                        ...this.db
                            .resources
                            .values()
                    ].map(
                        resource =>
                            resource.toJSON()
                    ),

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
                            id:
                                observation.id,

                            candidateId:
                                observation
                                    .candidateId,

                            target:
                                observation
                                    .target,

                            startedAt:
                                observation
                                    .startedAt,

                            completedAt:
                                observation
                                    .completedAt,

                            status:
                                observation
                                    .status,

                            signalPresent:
                                observation
                                    .signalPresent,

                            http:
                                observation
                                    .http,

                            fingerprint:
                                observation
                                    .fingerprint,

                            errors:
                                observation
                                    .errors
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

            this.networkCandidateKeys.clear();

            this.stats =
                this.createStats();
        }
    }
