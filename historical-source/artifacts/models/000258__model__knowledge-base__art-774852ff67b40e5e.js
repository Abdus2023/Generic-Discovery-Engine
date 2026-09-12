    class KnowledgeBase {
        constructor(engine) {
            this.engine =
                engine;

            this.candidates =
                new Map();

            this.claimed =
                new Set();

            this.visited =
                new Set();

            this.observations =
                new Map();

            this.discoveries =
                new Map();

            this.resources =
                new Map();

            this.edges =
                new Map();

            this.networkEvents =
                new Map();

            this.networkRequests =
                new Map();

            this.persistTimer =
                null;

            this.load();
        }

        getResource(url) {
            const target =
                canonicalizeUrl(
                    url
                );

            if (!target) {
                return null;
            }

            let resource =
                this.resources.get(
                    target
                );

            if (!resource) {
                resource =
                    new ResourceRecord(
                        target
                    );

                this.resources.set(
                    target,
                    resource
                );
            }

            return resource;
        }

        addCandidate(
            candidate
        ) {
            if (
                !candidate.target ||
                !allowed(
                    candidate.target
                )
            ) {
                return false;
            }

            if (
                candidate.depth >
                CONFIG.maxDepth
            ) {
                this.engine.stats
                    .maxDepthRejected++;

                return false;
            }

            const resource =
                this.getResource(
                    candidate.target
                );

            resource.mergeCandidate(
                candidate
            );

            /*
             * Provenance is retained even when the candidate
             * itself is deduplicated.
             */
            this.recordCandidateEdge(
                candidate
            );

            const key =
                candidate.key();

            /*
             * Resource-level acquisition deduplication.
             */
            if (
                resource.status ===
                    'acquired' &&
                resource.fingerprint
            ) {
                this.engine.stats
                    .cacheSkips++;

                return false;
            }

            if (
                this.visited.has(key) ||
                this.claimed.has(key)
            ) {
                return false;
            }

            const existing =
                this.candidates.get(
                    key
                );

            if (existing) {
                this.mergeCandidate(
                    existing,
                    candidate
                );

                this.engine.stats
                    .candidatesMerged++;

                return false;
            }

            if (
                this.candidates.size >=
                CONFIG.maxCandidates
            ) {
                this.engine.stats
                    .candidateLimitHits++;

                return false;
            }

            candidate.lifecycle(
                'queued'
            );

            this.candidates.set(
                key,
                candidate
            );

            this.schedulePersist();

            return true;
        }

        mergeCandidate(
            existing,
            incoming
        ) {
            existing.priority =
                Math.max(
                    existing.priority,
                    incoming.priority
                );

            existing.depth =
                Math.min(
                    existing.depth,
                    incoming.depth
                );

            existing.hints = {
                ...existing.hints,
                ...incoming.hints
            };

            if (
                incoming.parent &&
                !existing.parent
            ) {
                existing.parent =
                    incoming.parent;
            }
        }

        recordCandidateEdge(
            candidate
        ) {
            if (
                this.edges.size >=
                CONFIG.maxGraphEdges
            ) {
                return;
            }

            const from =
                candidate.parent ||
                'root';

            const key =
                [
                    from,
                    candidate.target,
                    candidate.type,
                    candidate.origin
                ].join('|');

            if (
                this.edges.has(key)
            ) {
                return;
            }

            this.edges.set(
                key,
                {
                    id:
                        makeId('edge'),

                    fromDiscoveryId:
                        candidate.parent,

                    target:
                        candidate.target,

                    relationship:
                        'candidate-reference',

                    mechanism:
                        candidate.origin,

                    candidateType:
                        candidate.type,

                    priority:
                        candidate.priority,

                    depth:
                        candidate.depth,

                    createdAt:
                        now()
                }
            );
        }

        claimNext() {
            const current =
                now();

            const ready =
                [
                    ...this.candidates
                        .entries()
                ].filter(
                    ([, candidate]) =>
                        candidate
                            .nextAttemptAt <=
                        current
                );

            if (!ready.length) {
                return null;
            }

            ready.sort(
                (a, b) =>
                    b[1].score() -
                    a[1].score()
            );

            const [
                key,
                candidate
            ] = ready[0];

            this.candidates.delete(
                key
            );

            this.claimed.add(
                key
            );

            candidate.lifecycle(
                'claimed'
            );

            return candidate;
        }

        complete(
            candidate
        ) {
            const key =
                candidate.key();

            this.claimed.delete(
                key
            );

            this.visited.add(
                key
            );

            candidate.lifecycle(
                'completed'
            );

            this.schedulePersist();
        }

        fail(
            candidate,
            retry
        ) {
            const key =
                candidate.key();

            this.claimed.delete(
                key
            );

            if (retry) {
                const exponent =
                    Math.max(
                        0,
                        candidate.attempts -
                            1
                    );

                const delay =
                    Math.min(
                        CONFIG.retryMaxDelay,
                        CONFIG.retryBaseDelay *
                            Math.pow(
                                2,
                                exponent
                            )
                    );

                candidate.status =
                    'retry-wait';

                candidate.nextAttemptAt =
                    now() + delay;

                this.candidates.set(
                    key,
                    candidate
                );
            } else {
                candidate.lifecycle(
                    'failed'
                );

                this.visited.add(
                    key
                );

                const resource =
                    this.getResource(
                        candidate.target
                    );

                resource.status =
                    'failed';
            }

            this.schedulePersist();
        }

        addObservation(
            observation
        ) {
            this.observations.set(
                observation.id,
                observation
            );

            const resource =
                this.getResource(
                    observation.target
                );

            resource.mergeObservation(
                observation
            );

            this.schedulePersist();
        }

        addDiscovery(
            discovery
        ) {
            this.discoveries.set(
                discovery.id,
                discovery
            );

            const resource =
                this.getResource(
                    discovery.provenance
                        .candidateTarget
                );

            resource.mergeDiscovery(
                discovery
            );

            this.schedulePersist();
        }

        addNetworkEvent(
            event
        ) {
            if (
                event.requestId &&
                this.networkRequests.has(
                    event.requestId
                )
            ) {
                const existing =
                    this.networkRequests.get(
                        event.requestId
                    );

                existing.update(
                    event
                );

                this.addNetworkResource(
                    existing
                );

                return existing;
            }

            if (
                this.networkEvents.size >=
                CONFIG.maxNetworkEvents
            ) {
                const oldest =
                    this.networkEvents
                        .keys()
                        .next()
                        .value;

                if (oldest) {
                    this.networkEvents.delete(
                        oldest
                    );
                }
            }

            this.networkEvents.set(
                event.id,
                event
            );

            if (
                event.requestId
            ) {
                this.networkRequests.set(
                    event.requestId,
                    event
                );
            }

            this.addNetworkResource(
                event
            );

            return event;
        }

        addNetworkResource(
            event
        ) {
            if (!event.url) {
                return;
            }

            const resource =
                this.getResource(
                    event.url
                );

            if (!resource) {
                return;
            }

            resource.mechanisms.add(
                `network:${event.api}`
            );

            resource.lastSeenAt =
                now();

            if (
                event.contentType
            ) {
                resource.types.add(
                    classifyUrl(
                        event.url,
                        event.contentType
                    )
                );
            }
        }

        queueSize() {
            return this.candidates.size;
        }

        inFlight() {
            return this.claimed.size;
        }

        nextDelay() {
            if (
                !this.candidates.size
            ) {
                return null;
            }

            const current =
                now();

            return Math.min(
                ...[
                    ...this.candidates
                        .values()
                ].map(
                    candidate =>
                        Math.max(
                            0,
                            candidate
                                .nextAttemptAt -
                                current
                        )
                )
            );
        }

        serialize() {
            return {
                version: 6,

                visited:
                    [
                        ...this.visited
                    ].slice(
                        -CONFIG.maxCandidates
                    ),

                resources:
                    [
                        ...this.resources
                            .values()
                    ]
                        .slice(
                            -CONFIG.maxPersistedResources
                        )
                        .map(
                            resource =>
                                resource.toJSON()
                        ),

                discoveries:
                    [
                        ...this.discoveries
                            .values()
                    ].slice(
                        -CONFIG.maxPersistedDiscoveries
                    ),

                edges:
                    [
                        ...this.edges
                            .values()
                    ].slice(
                        -CONFIG.maxPersistedEdges
                    )
            };
        }

        schedulePersist() {
            if (
                !CONFIG.persistState
            ) {
                return;
            }

            clearTimeout(
                this.persistTimer
            );

            this.persistTimer =
                setTimeout(
                    () => this.persist(),
                    CONFIG.persistDebounceMs
                );
        }

        persist() {
            if (
                !CONFIG.persistState
            ) {
                return;
            }

            clearTimeout(
                this.persistTimer
            );

            this.persistTimer =
                null;

            try {
                GM_setValue(
                    STATE_KEY,
                    JSON.stringify(
                        this.serialize()
                    )
                );
            } catch (error) {
                warn(
                    'Persistence failed',
                    error
                );
            }
        }

        load() {
            if (
                !CONFIG.persistState
            ) {
                return;
            }

            try {
                const raw =
                    GM_getValue(
                        STATE_KEY,
                        null
                    );

                if (!raw) {
                    return;
                }

                const state =
                    typeof raw ===
                    'string'
                        ? JSON.parse(raw)
                        : raw;

                for (
                    const value of
                    state.visited || []
                ) {
                    this.visited.add(
                        value
                    );
                }

                for (
                    const value of
                    state.resources || []
                ) {
                    if (
                        value?.url
                    ) {
                        this.resources.set(
                            value.url,
                            ResourceRecord
                                .fromJSON(
                                    value
                                )
                        );
                    }
                }

                for (
                    const value of
                    state.discoveries || []
                ) {
                    if (
                        value?.id
                    ) {
                        this.discoveries.set(
                            value.id,
                            value
                        );
                    }
                }

                for (
                    const value of
                    state.edges || []
                ) {
                    if (
                        value?.target
                    ) {
                        const key =
                            [
                                value
                                    .fromDiscoveryId ||
                                    'root',
                                value.target,
                                value
                                    .candidateType ||
                                    '',
                                value
                                    .mechanism ||
                                    ''
                            ].join('|');

                        this.edges.set(
                            key,
                            value
                        );
                    }
                }

                log(
                    'Restored persistent state',
                    {
                        version:
                            state.version,

                        resources:
                            this.resources.size,

                        discoveries:
                            this.discoveries.size,

                        edges:
                            this.edges.size
                    }
                );
            } catch (error) {
                warn(
                    'State restoration failed',
                    error
                );
            }
        }

        clear() {
            clearTimeout(
                this.persistTimer
            );

            this.candidates.clear();
            this.claimed.clear();
            this.visited.clear();
            this.observations.clear();
            this.discoveries.clear();
            this.resources.clear();
            this.edges.clear();
            this.networkEvents.clear();
            this.networkRequests.clear();

            this.persist();
        }
    }
