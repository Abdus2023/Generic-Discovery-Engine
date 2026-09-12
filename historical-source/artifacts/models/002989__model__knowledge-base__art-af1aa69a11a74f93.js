    class KnowledgeBase {
        constructor() {
            this.candidates =
                new Map();

            this.observations =
                new Map();

            this.discoveries =
                new Map();

            this.visited =
                new Set();

            this.claimed =
                new Set();

            this.graph =
                new ProvenanceGraph();

            this.load();
        }

        candidateKey(candidate) {
            return candidate.key();
        }

        addCandidate(candidate) {
            const key =
                this.candidateKey(
                    candidate
                );

            if (!candidate.target) {
                return false;
            }

            if (
                candidate.depth >
                CONFIG.maxDepth
            ) {
                return false;
            }

            if (
                this.visited.has(key)
            ) {
                return false;
            }

            if (
                this.claimed.has(key)
            ) {
                return false;
            }

            if (
                this.candidates.has(key)
            ) {
                return false;
            }

            if (
                this.candidates.size >=
                CONFIG.maxCandidates
            ) {
                return false;
            }

            this.candidates.set(
                key,
                candidate
            );

            this.graph.addCandidate(
                candidate
            );

            this.persist();

            return true;
        }

        /*
         * Synchronous atomic claim.
         */
        claimNextCandidate() {
            const candidates = [
                ...this.candidates.entries()
            ];

            if (!candidates.length) {
                return null;
            }

            /*
             * Highest effective score first.
             *
             * Priority is primary.
             * Lower depth receives a small preference.
             * Retry delay is enforced separately.
             */
            candidates.sort(
                (a, b) => {
                    const ca = a[1];
                    const cb = b[1];

                    const scoreA =
                        ca.priority -
                        ca.depth * 0.025;

                    const scoreB =
                        cb.priority -
                        cb.depth * 0.025;

                    return (
                        scoreB -
                        scoreA
                    );
                }
            );

            const timestamp =
                now();

            for (
                const [key, candidate]
                of candidates
            ) {
                if (
                    this.visited.has(key) ||
                    this.claimed.has(key)
                ) {
                    continue;
                }

                /*
                 * Retry backoff.
                 */
                if (
                    candidate.nextAttemptAt >
                    timestamp
                ) {
                    continue;
                }

                /*
                 * Atomic ownership transfer.
                 */
                this.candidates.delete(
                    key
                );

                this.claimed.add(
                    key
                );

                candidate.status =
                    'claimed';

                candidate.claimedAt =
                    timestamp;

                this.persist();

                return candidate;
            }

            return null;
        }

        completeCandidate(candidate) {
            const key =
                this.candidateKey(
                    candidate
                );

            this.claimed.delete(key);
            this.visited.add(key);

            candidate.status =
                'completed';

            candidate.completedAt =
                now();

            this.persist();
        }

        failCandidate(
            candidate,
            retry = false
        ) {
            const key =
                this.candidateKey(
                    candidate
                );

            this.claimed.delete(key);

            if (
                retry &&
                candidate.attempts <=
                    CONFIG.maxRetries
            ) {
                candidate.status =
                    'queued';

                const delay =
                    CONFIG.retryBaseDelay *
                    Math.pow(
                        2,
                        Math.max(
                            0,
                            candidate.attempts - 1
                        )
                    );

                candidate.nextAttemptAt =
                    now() + delay;

                this.candidates.set(
                    key,
                    candidate
                );
            } else {
                this.visited.add(key);

                candidate.status =
                    'failed';

                candidate.failedAt =
                    now();
            }

            this.persist();
        }

        addObservation(observation) {
            /*
             * Observations are kept in memory only.
             *
             * They may contain complete HTTP bodies.
             */
            this.observations.set(
                observation.id,
                observation
            );
        }

        addDiscovery(discovery) {
            this.discoveries.set(
                discovery.id,
                discovery
            );

            this.graph.addDiscovery(
                discovery
            );

            this.persist();
        }

        queueSize() {
            return this.candidates.size;
        }

        claimedSize() {
            return this.claimed.size;
        }

        discoveryCount() {
            return this.discoveries.size;
        }

        serialize() {
            const discoveries = [
                ...this.discoveries.values()
            ];

            const visited = [
                ...this.visited
            ];

            return {
                version: 4,

                visited:
                    visited.slice(
                        -CONFIG.maxPersistedVisited
                    ),

                discoveries:
                    discoveries.slice(
                        -CONFIG.maxPersistedDiscoveries
                    ),

                graph:
                    this.graph.serialize()
            };
        }

        persist() {
            if (!CONFIG.persistState) {
                return;
            }

            try {
                const raw =
                    JSON.stringify(
                        this.serialize()
                    );

                if (
                    typeof GM_setValue ===
                    'function'
                ) {
                    GM_setValue(
                        'discovery-state',
                        raw
                    );
                } else {
                    localStorage.setItem(
                        'generic-discovery-state',
                        raw
                    );
                }
            } catch (error) {
                warn(
                    'Persistence failed:',
                    error
                );
            }
        }

        load() {
            if (!CONFIG.persistState) {
                return;
            }

            try {
                let raw = null;

                if (
                    typeof GM_getValue ===
                    'function'
                ) {
                    raw = GM_getValue(
                        'discovery-state',
                        null
                    );
                } else {
                    raw =
                        localStorage.getItem(
                            'generic-discovery-state'
                        );
                }

                if (!raw) {
                    return;
                }

                const data =
                    typeof raw ===
                    'string'
                        ? JSON.parse(raw)
                        : raw;

                if (
                    data.version &&
                    data.version > 4
                ) {
                    warn(
                        'Stored state belongs to a newer version.'
                    );

                    return;
                }

                for (
                    const key of
                    data.visited || []
                ) {
                    this.visited.add(key);
                }

                for (
                    const discovery of
                    data.discoveries || []
                ) {
                    if (
                        discovery &&
                        discovery.id
                    ) {
                        this.discoveries.set(
                            discovery.id,
                            discovery
                        );
                    }
                }

                /*
                 * Restore graph data if available.
                 */
                for (
                    const node of
                    data.graph?.nodes || []
                ) {
                    if (
                        node &&
                        node.id
                    ) {
                        this.graph.nodes.set(
                            node.id,
                            node
                        );
                    }
                }

                for (
                    const edge of
                    data.graph?.edges || []
                ) {
                    if (
                        edge &&
                        edge.id
                    ) {
                        this.graph.edges.set(
                            edge.id,
                            edge
                        );
                    }
                }

                log(
                    'State restored',
                    {
                        visited:
                            this.visited.size,

                        discoveries:
                            this.discoveries.size,

                        graphNodes:
                            this.graph.nodes.size
                    }
                );
            } catch (error) {
                warn(
                    'Could not restore state:',
                    error
                );
            }
        }

        clear() {
            this.candidates.clear();
            this.observations.clear();
            this.discoveries.clear();

            this.visited.clear();
            this.claimed.clear();

            this.graph.clear();

            this.persist();
        }
    }
