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

            this.networkEvents = new Map();

            this.networkRequestIndex =
                new Map();

            this.running = false;

            this.inFlight = 0;

            this.seeded = false;

            this.networkObserver =
                new NetworkObserver(
                    event =>
                        this.observeNetwork(
                            event
                        )
                );

            if (CONFIG.discoverNetwork) {
                this.networkObserver.install();
            }
        }

        seed() {
            if (this.seeded) {
                return;
            }

            this.seeded = true;

            const current =
                canonicalizeUrl(
                    location.href
                );

            if (current) {
                this.addCandidate(
                    new Candidate({
                        target: current,
                        type: 'url',
                        origin: 'document',
                        priority: 1.0,
                        hints: {
                            confidence: 1
                        },
                        depth: 0
                    })
                );
            }

            if (
                CONFIG.discoverLinks ||
                CONFIG.discoverResources
            ) {
                this.seedFromCurrentDom();
            }

            if (CONFIG.discoverWellKnown) {
                this.seedWellKnown();
            }
        }

        seedFromCurrentDom() {
            if (!document) {
                return;
            }

            const base =
                location.href;

            if (CONFIG.discoverLinks) {
                for (const element of document.querySelectorAll(
                    'a[href], area[href]'
                )) {
                    const url =
                        canonicalizeUrl(
                            element.getAttribute(
                                'href'
                            ),
                            base
                        );

                    if (!url || !isAllowedUrl(url)) {
                        continue;
                    }

                    this.addCandidate(
                        new Candidate({
                            target: url,
                            type: 'url',
                            origin:
                                `dom:${element.tagName.toLowerCase()}`,
                            priority: 0.80,
                            hints: {
                                confidence: 0.82
                            },
                            depth: 1
                        })
                    );
                }
            }

            if (CONFIG.discoverResources) {
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

                for (const [
                    selector,
                    attribute,
                    type
                ] of resourceSelectors) {
                    for (const element of document.querySelectorAll(
                        selector
                    )) {
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

                        let candidateType =
                            type;

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
                                candidateType =
                                    'stylesheet';
                            } else if (
                                rel.includes(
                                    'manifest'
                                )
                            ) {
                                candidateType =
                                    'manifest';
                            } else if (
                                rel.includes(
                                    'sitemap'
                                )
                            ) {
                                candidateType =
                                    'sitemap';
                            }
                        }

                        this.addCandidate(
                            new Candidate({
                                target: url,
                                type:
                                    candidateType,
                                origin:
                                    `dom:${element.tagName.toLowerCase()}`,
                                priority:
                                    CONFIG.typePriority[
                                        candidateType
                                    ] ??
                                    0.5,
                                hints: {
                                    confidence: 0.82
                                },
                                depth: 1
                            })
                        );
                    }
                }
            }

            if (
                CONFIG.discoverForms
            ) {
                for (const form of document.querySelectorAll(
                    'form[action]'
                )) {
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
                            target: url,
                            type: 'form',
                            origin: 'dom:form',
                            priority: 0.35,
                            hints: {
                                confidence: 0.75,
                                method:
                                    (
                                        form.getAttribute(
                                            'method'
                                        ) || 'GET'
                                    ).toUpperCase()
                            },
                            depth: 1
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

            const candidates = [
                {
                    path: '/robots.txt',
                    type: 'robots',
                    priority: 0.88
                },
                {
                    path: '/sitemap.xml',
                    type: 'sitemap',
                    priority: 0.90
                }
            ];

            for (const item of candidates) {
                const url =
                    canonicalizeUrl(
                        origin + item.path
                    );

                if (!url || !isAllowedUrl(url)) {
                    continue;
                }

                this.addCandidate(
                    new Candidate({
                        target: url,
                        type: item.type,
                        origin: 'well-known',
                        priority: item.priority,
                        hints: {
                            confidence: 0.70
                        },
                        depth: 1
                    })
                );
            }
        }

        addCandidate(candidate) {
            return this.scheduler.add(
                candidate
            );
        }

        observeNetwork(data) {
            if (!data?.url) {
                return;
            }

            const requestId =
                data.requestId || null;

            let networkEvent =
                requestId
                    ? this.networkRequestIndex.get(
                        requestId
                    )
                    : null;

            if (
                data.event === 'request'
            ) {
                networkEvent =
                    new NetworkEvent({
                        requestId,
                        api: data.api,
                        method: data.method,
                        url:
                            canonicalizeUrl(
                                data.url
                            ) || data.url,
                        requestAt:
                            data.requestAt ||
                            now(),
                        phase: 'request'
                    });

                this.storeNetworkEvent(
                    networkEvent
                );

                if (requestId) {
                    this.networkRequestIndex.set(
                        requestId,
                        networkEvent.id
                    );
                }

                return;
            }

            if (
                data.event === 'response' ||
                data.event === 'error'
            ) {
                if (requestId) {
                    const eventId =
                        this.networkRequestIndex.get(
                            requestId
                        );

                    if (eventId) {
                        networkEvent =
                            this.networkEvents.get(
                                eventId
                            );
                    }
                }

                if (!networkEvent) {
                    networkEvent =
                        new NetworkEvent({
                            requestId,
                            api: data.api,
                            method: data.method,
                            url:
                                canonicalizeUrl(
                                    data.url
                                ) || data.url,
                            requestAt:
                                data.requestAt ||
                                now()
                        });

                    this.storeNetworkEvent(
                        networkEvent
                    );
                }

                networkEvent.phase =
                    data.event === 'error'
                        ? 'error'
                        : 'response';

                networkEvent.finalUrl =
                    canonicalizeUrl(
                        data.finalUrl
                    ) ||
                    networkEvent.url;

                networkEvent.status =
                    data.status ?? null;

                networkEvent.contentType =
                    normalizeContentType(
                        data.contentType || ''
                    );

                networkEvent.responseAt =
                    data.responseAt ||
                    now();

                networkEvent.duration =
                    data.duration ?? (
                        networkEvent.requestAt
                            ? networkEvent.responseAt -
                              networkEvent.requestAt
                            : null
                    );

                networkEvent.error =
                    data.error || null;

                this.storeNetworkEvent(
                    networkEvent
                );

                /*
                 * Do not replay unsafe methods.
                 * Only observed GET requests become acquisition candidates.
                 */
                if (
                    data.event === 'response' &&
                    (
                        !networkEvent.method ||
                        networkEvent.method === 'GET'
                    )
                ) {
                    const type =
                        looksLikeApiUrl(
                            networkEvent.url
                        )
                            ? 'api'
                            : 'network';

                    const priority =
                        type === 'api'
                            ? 0.96
                            : 0.80;

                    const candidate =
                        new Candidate({
                            target:
                                networkEvent.url,
                            type,
                            origin:
                                `network:${networkEvent.api}`,
                            priority,
                            hints: {
                                confidence: 0.94,
                                networkRequestId:
                                    requestId,
                                observedStatus:
                                    networkEvent.status,
                                observedContentType:
                                    networkEvent.contentType,
                                observedFinalUrl:
                                    networkEvent.finalUrl
                            },
                            depth: 0
                        });

                    if (
                        this.addCandidate(
                            candidate
                        )
                    ) {
                        this.database.statistics
                            .networkCandidates++;
                    }
                }

                return;
            }

            if (
                data.event === 'performance'
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
                            ] ?? 0.45,
                        hints: {
                            confidence: 0.88,
                            initiatorType:
                                data.initiatorType ||
                                null,
                            performanceDuration:
                                data.duration ??
                                null
                        },
                        depth: 0
                    });

                if (
                    this.addCandidate(
                        candidate
                    )
                ) {
                    this.database.statistics
                        .performanceCandidates++;
                }
            }
        }

        classifyPerformanceResource(data) {
            const initiator =
                String(
                    data.initiatorType || ''
                ).toLowerCase();

            const url =
                String(
                    data.url || ''
                ).toLowerCase();

            if (
                initiator === 'fetch' ||
                initiator === 'xmlhttprequest'
            ) {
                return looksLikeApiUrl(url)
                    ? 'api'
                    : 'network';
            }

            if (
                initiator === 'script' ||
                /\.(?:js|mjs|cjs)(?:[?#]|$)/i.test(url)
            ) {
                return 'script';
            }

            if (
                initiator === 'css' ||
                initiator === 'link' ||
                /\.(?:css)(?:[?#]|$)/i.test(url)
            ) {
                return 'stylesheet';
            }

            if (
                initiator === 'img' ||
                /\.(?:png|jpe?g|gif|webp|svg|avif|ico)(?:[?#]|$)/i.test(url)
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

                this.database.statistics
                    .networkEvents++;
            }
        }

        async run() {
            if (this.running) {
                return;
            }

            this.running = true;

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

            this.running = false;

            this.database.persistNow();

            log(
                'Scan complete',
                this.report()
            );
        }

        async worker(workerId) {
            while (this.running) {
                if (
                    this.database.statistics.requests >=
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
                            Math.max(delay, 25),
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
            candidate.transition(
                'acquiring'
            );

            /*
             * Resource-level deduplication:
             *
             * Multiple mechanisms may discover the same URL,
             * but only one actual acquisition is necessary.
             */
            if (
                this.database.resourceAlreadyAcquired(
                    candidate.target
                )
            ) {
                const observation =
                    new Observation({
                        candidateId:
                            candidate.id,
                        target:
                            candidate.target,
                        status: 'reused'
                    });

                observation.completedAt =
                    now();

                const resource =
                    this.database.getResource(
                        candidate.target
                    );

                observation.http = {
                    status:
                        resource?.fingerprint
                            ?.status ?? null,

                    contentType:
                        resource?.fingerprint
                            ?.contentType || '',

                    contentLength:
                        resource?.fingerprint
                            ?.contentLength ?? null,

                    finalUrl:
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

                candidate.transition(
                    'completed'
                );

                this.database.completeCandidate(
                    candidate
                );

                return;
            }

            this.inFlight++;

            this.database.statistics.requests++;

            try {
                const observation =
                    await this.acquisition.acquire(
                        candidate
                    );

                candidate.transition(
                    'observed'
                );

                this.database.addObservation(
                    observation
                );

                const resource =
                    this.database.ensureResource(
                        candidate.target
                    );

                resource.status =
                    'acquired';

                resource.fingerprint =
                    observation.fingerprint;

                resource.finalUrl =
                    observation.http.finalUrl;

                /*
                 * Redirects create a first-class resource relationship.
                 */
                if (
                    observation.http.finalUrl &&
                    observation.http.finalUrl !==
                        candidate.target
                ) {
                    this.database.ensureResource(
                        observation.http.finalUrl
                    );
                }

                const discoveries =
                    this.providers.recognizeAll(
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
                    this.database.addDiscovery(
                        discovery
                    );

                    const expanded =
                        this.providers
                            .candidatesFor(
                                discovery
                            );

                    for (
                        const nextCandidate of
                        expanded
                    ) {
                        this.addCandidate(
                            nextCandidate
                        );
                    }
                }

                candidate.transition(
                    'expanded'
                );

                candidate.transition(
                    'completed'
                );

                this.database.completeCandidate(
                    candidate
                );

                log(
                    `Worker ${workerId} completed`,
                    candidate.target,
                    discoveries.length,
                    'discoveries'
                );
            } catch (error) {
                this.database.failCandidate(
                    candidate,
                    error
                );

                warn(
                    `Worker ${workerId} failed`,
                    candidate.target,
                    error
                );
            } finally {
                this.inFlight--;
            }
        }

        report() {
            const stats =
                this.database.statistics;

            return {
                running:
                    this.running,

                queue:
                    this.database.queue.length,

                claimed:
                    this.database.claimed.size,

                inFlight:
                    this.inFlight,

                candidates:
                    this.database.resources.size,

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

                cacheSkips:
                    stats.cacheSkips,

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
            const resources = [
                ...this.database.resources.values()
            ];

            const observations = [
                ...this.database.observations.values()
            ];

            const discoveries = [
                ...this.database.discoveries.values()
            ];

            const networkEvents = [
                ...this.networkEvents.values()
            ];

            const graphNodes = [
                {
                    id: 'root',
                    kind: 'root',
                    url:
                        canonicalizeUrl(
                            location.href
                        ),
                    label: 'scan-root'
                }
            ];

            for (const resource of resources) {
                graphNodes.push({
                    id: resource.id,
                    kind: 'resource',
                    url: resource.url,
                    types: [
                        ...resource.types
                    ],
                    mechanisms: [
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

                    candidateIds:
                        [...resource.candidateIds],

                    observationIds:
                        [...resource.observationIds],

                    discoveryIds:
                        [...resource.discoveryIds]
                });
            }

            const graphEdges = [];

            /*
             * Candidate/discovery edges.
             */
            for (
                const edge of
                this.database.edgeRecords
            ) {
                let sourceId =
                    'root';

                if (
                    edge.fromDiscoveryId
                ) {
                    const parentDiscovery =
                        this.database
                            .discoveries
                            .get(
                                edge.fromDiscoveryId
                            );

                    const parentTarget =
                        parentDiscovery?.targetUrl();

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

                const targetResource =
                    this.database.resources.get(
                        edge.target
                    );

                if (!targetResource) {
                    continue;
                }

                /*
                 * Self-references are usually HTML canonical/self links
                 * and add little graph value.
                 */
                if (
                    sourceId ===
                    targetResource.id
                ) {
                    continue;
                }

                graphEdges.push({
                    id: edge.id,
                    source: sourceId,
                    target:
                        targetResource.id,
                    kind: 'discovery',
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
                    createdAt:
                        edge.createdAt,
                    discoveryId:
                        edge.fromDiscoveryId
                });
            }

            /*
             * Redirect edges.
             */
            for (const resource of resources) {
                if (
                    !resource.finalUrl ||
                    resource.finalUrl ===
                        resource.url
                ) {
                    continue;
                }

                const target =
                    this.database.resources.get(
                        resource.finalUrl
                    );

                if (!target) {
                    continue;
                }

                graphEdges.push({
                    id:
                        stableId(
                            'redirect',
                            `${resource.url}->${resource.finalUrl}`
                        ),
                    source:
                        resource.id,
                    target:
                        target.id,
                    kind: 'redirect',
                    mechanism:
                        'http-redirect'
                });
            }

            /*
             * Network-observation edges.
             *
             * Network events do not always expose their semantic parent,
             * so their default source is the scan root.
             */
            for (const event of networkEvents) {
                const target =
                    event.url &&
                    this.database.resources.get(
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
                    source: 'root',
                    target: target.id,
                    kind:
                        event.phase === 'performance'
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

            const graph = {
                nodes: graphNodes,

                edges: graphEdges.slice(
                    -CONFIG.maxGraphEdges
                )
            };

            return {
                version: 5,

                scope: {
                    type:
                        'web-resource-discovery',

                    architecture:
                        'candidate -> observation -> recognition -> discovery -> candidate',

                    inspiredBy:
                        'DVB blind-scan architecture',

                    rfScanning: false
                },

                timestamp:
                    new Date().toISOString(),

                page: {
                    url:
                        location.href,

                    origin:
                        location.origin,

                    title:
                        document.title || '',

                    userAgent:
                        navigator.userAgent
                },

                statistics:
                    this.report(),

                configuration:
                    CONFIG,

                queue: [
                    ...this.database.queue
                ].map(candidate => ({
                    id: candidate.id,
                    target: candidate.target,
                    type: candidate.type,
                    origin: candidate.origin,
                    parent: candidate.parent,
                    priority: candidate.priority,
                    effectivePriority:
                        candidate.effectivePriority(),
                    depth: candidate.depth,
                    status: candidate.status,
                    attempts: candidate.attempts,
                    nextAttemptAt:
                        candidate.nextAttemptAt
                })),

                lifecycle: {
                    statuses: [
                        'discovered',
                        'queued',
                        'claimed',
                        'acquiring',
                        'observed',
                        'recognized',
                        'expanded',
                        'completed',
                        'failed'
                    ]
                },

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

                networkEvents,

                discoveries,

                graph
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
            this.database.clear();

            this.networkEvents.clear();
            this.networkRequestIndex.clear();

            this.seeded = false;
        }
    }
