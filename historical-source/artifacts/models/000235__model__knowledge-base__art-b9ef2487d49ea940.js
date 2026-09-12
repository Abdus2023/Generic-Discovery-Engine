    class KnowledgeBase {
        constructor() {
            this.candidates =
                new Map();

            this.observations =
                new Map();

            this.discoveries =
                new Map();

            this.networkEvents =
                new Map();

            this.visited =
                new Set();

            this.claimed =
                new Set();

            this.load();
        }

        addCandidate(candidate) {
            if (
                !candidate ||
                !candidate.target
            ) {
                return false;
            }

            if (
                candidate.depth >
                CONFIG.maxDepth
            ) {
                return false;
            }

            const key =
                candidate.key();

            if (
                this.visited.has(key) ||
                this.claimed.has(key) ||
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

            return true;
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
                        candidate.nextAttemptAt <=
                        current
                );

            if (!ready.length) {
                return null;
            }

            ready.sort(
                (a, b) => {
                    const score =
                        b[1].score() -
                        a[1].score();

                    if (
                        score !== 0
                    ) {
                        return score;
                    }

                    return (
                        a[1].createdAt -
                        b[1].createdAt
                    );
                }
            );

            const [
                key,
                candidate
            ] = ready[0];

            /*
             * Atomic claim.
             */
            this.candidates.delete(
                key
            );

            this.claimed.add(
                key
            );

            candidate.status =
                'claimed';

            return candidate;
        }

        complete(candidate) {
            const key =
                candidate.key();

            this.claimed.delete(
                key
            );

            this.visited.add(
                key
            );

            candidate.status =
                'completed';

            candidate.completedAt =
                now();
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

            if (
                retry
            ) {
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
                candidate.status =
                    'failed';

                this.visited.add(
                    key
                );
            }
        }

        addObservation(
            observation
        ) {
            this.observations.set(
                observation.id,
                observation
            );
        }

        addDiscovery(
            discovery
        ) {
            this.discoveries.set(
                discovery.id,
                discovery
            );
        }

        addNetworkEvent(
            event
        ) {
            if (
                this.networkEvents.size >=
                CONFIG.maxNetworkEvents
            ) {
                const first =
                    this.networkEvents
                        .keys()
                        .next()
                        .value;

                if (first) {
                    this.networkEvents.delete(
                        first
                    );
                }
            }

            this.networkEvents.set(
                event.id,
                event
            );
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
                version: 5,

                visited:
                    [...this.visited]
                        .slice(
                            -CONFIG.maxCandidates
                        ),

                discoveries:
                    [
                        ...this.discoveries
                            .values()
                    ].slice(
                        -CONFIG.maxPersistedDiscoveries
                    )
            };
        }

        persist() {
            if (
                !CONFIG.persistState
            ) {
                return;
            }

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
                    const key of
                    state.visited ||
                    []
                ) {
                    this.visited.add(
                        key
                    );
                }

                for (
                    const discovery of
                    state.discoveries ||
                    []
                ) {
                    if (
                        discovery?.id
                    ) {
                        this.discoveries.set(
                            discovery.id,
                            discovery
                        );
                    }
                }
            } catch (error) {
                warn(
                    'State restoration failed',
                    error
                );
            }
        }

        clear() {
            this.candidates.clear();
            this.observations.clear();
            this.discoveries.clear();
            this.networkEvents.clear();
            this.visited.clear();
            this.claimed.clear();

            this.persist();
        }
    }
