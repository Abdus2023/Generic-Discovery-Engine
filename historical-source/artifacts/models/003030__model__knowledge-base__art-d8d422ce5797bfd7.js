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

            this.load();
        }

        candidateKey(candidate) {
            return candidate.key();
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
                this.candidateKey(
                    candidate
                );

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

            this.persist();

            return true;
        }

        claimNextCandidate() {
            const entries = [
                ...this.candidates.entries()
            ];

            if (!entries.length) {
                return null;
            }

            const current =
                now();

            const ready =
                entries.filter(
                    ([key, candidate]) =>
                        !this.visited.has(key) &&
                        !this.claimed.has(key) &&
                        (
                            !candidate.nextAttemptAt ||
                            candidate.nextAttemptAt <=
                                current
                        )
                );

            if (!ready.length) {
                return null;
            }

            ready.sort(
                (a, b) => {
                    const priorityDifference =
                        b[1].effectivePriority() -
                        a[1].effectivePriority();

                    if (
                        priorityDifference !==
                        0
                    ) {
                        return priorityDifference;
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
             * IMPORTANT:
             *
             * Remove from the queue and mark claimed
             * BEFORE any asynchronous work occurs.
             *
             * This makes candidate claiming atomic from
             * the scheduler's perspective and prevents two
             * workers from acquiring the same candidate.
             */
            this.candidates.delete(key);

            this.claimed.add(key);

            candidate.status =
                'claimed';

            candidate.claimedAt =
                current;

            this.persist();

            return candidate;
        }

        nextReadyDelay() {
            const entries = [
                ...this.candidates.values()
            ];

            if (!entries.length) {
                return null;
            }

            const current =
                now();

            let minimum =
                Infinity;

            for (
                const candidate of
                entries
            ) {
                if (
                    !candidate.nextAttemptAt
                ) {
                    return 0;
                }

                minimum =
                    Math.min(
                        minimum,
                        Math.max(
                            0,
                            candidate.nextAttemptAt -
                                current
                        )
                    );
            }

            return Number.isFinite(
                minimum
            )
                ? minimum
                : null;
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
                    'queued';

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

        addObservation(
            observation
        ) {
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
            const discoveries =
                [
                    ...this.discoveries
                        .values()
                ];

            const bounded =
                discoveries.slice(
                    -CONFIG.maxPersistedDiscoveries
                );

            /*
             * Deliberately do not persist:
             *   - response bodies
             *   - observations
             *   - pending candidates
             *
             * Response bodies can be huge and can also contain
             * sensitive application data.
             */
            return {
                version: 4,

                visited: [
                    ...this.visited
                ],

                discoveries:
                    bounded
            };
        }

        persist() {
            if (
                !CONFIG.persistState
            ) {
                return;
            }

            try {
                const data =
                    JSON.stringify(
                        this.serialize()
                    );

                if (
                    typeof GM_setValue ===
                    'function'
                ) {
                    GM_setValue(
                        STATE_KEY,
                        data
                    );
                } else {
                    localStorage.setItem(
                        'generic-discovery-state',
                        data
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
            if (
                !CONFIG.persistState
            ) {
                return;
            }

            try {
                let raw =
                    null;

                if (
                    typeof GM_getValue ===
                    'function'
                ) {
                    raw =
                        GM_getValue(
                            STATE_KEY,
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
                        'Stored state is from a newer version.'
                    );

                    return;
                }

                for (
                    const key of
                    data.visited || []
                ) {
                    if (
                        typeof key ===
                        'string'
                    ) {
                        this.visited.add(
                            key
                        );
                    }
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

                log(
                    'Restored state',
                    {
                        visited:
                            this.visited.size,

                        discoveries:
                            this.discoveries.size
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

            this.persist();
        }
    }
