    class KnowledgeBase {
        constructor() {
            this.candidates = new Map();
            this.observations = new Map();
            this.discoveries = new Map();

            /*
             * Permanently completed/failed candidates.
             */
            this.visited = new Set();

            /*
             * Candidates currently owned by workers.
             */
            this.claimed = new Set();

            this.load();
        }

        candidateKey(candidate) {
            return candidate.key();
        }

        addCandidate(candidate) {
            const key = this.candidateKey(candidate);

            if (!candidate.target) {
                return false;
            }

            if (this.visited.has(key)) {
                return false;
            }

            if (this.claimed.has(key)) {
                return false;
            }

            if (this.candidates.has(key)) {
                return false;
            }

            if (
                this.candidates.size >=
                CONFIG.maxCandidates
            ) {
                return false;
            }

            this.candidates.set(key, candidate);

            this.persist();

            return true;
        }

        /*
         * ---------------------------------------------------------------
         * ATOMIC CANDIDATE CLAIM
         * ---------------------------------------------------------------
         *
         * No await occurs during this operation.
         *
         * Therefore concurrent async workers cannot claim the same
         * candidate between selection and removal.
         */
        claimNextCandidate() {
            const candidates = [
                ...this.candidates.entries()
            ];

            if (!candidates.length) {
                return null;
            }

            candidates.sort((a, b) => {
                return (
                    b[1].priority -
                    a[1].priority
                );
            });

            for (const [key, candidate]
                of candidates) {

                if (
                    this.visited.has(key) ||
                    this.claimed.has(key)
                ) {
                    continue;
                }

                /*
                 * Atomic synchronous ownership transfer.
                 */
                this.candidates.delete(key);
                this.claimed.add(key);

                candidate.status = 'claimed';
                candidate.claimedAt = now();

                this.persist();

                return candidate;
            }

            return null;
        }

        completeCandidate(candidate) {
            const key =
                this.candidateKey(candidate);

            this.claimed.delete(key);
            this.visited.add(key);

            candidate.status = 'completed';
            candidate.completedAt = now();

            this.persist();
        }

        failCandidate(candidate, retry = false) {
            const key =
                this.candidateKey(candidate);

            this.claimed.delete(key);

            if (retry) {
                candidate.status = 'queued';

                this.candidates.set(
                    key,
                    candidate
                );
            } else {
                this.visited.add(key);

                candidate.status = 'failed';
                candidate.failedAt = now();
            }

            this.persist();
        }

        addObservation(observation) {
            this.observations.set(
                observation.id,
                observation
            );

            /*
             * Observations can contain complete response bodies and are
             * deliberately not persisted.
             */
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
            const discoveries = [
                ...this.discoveries.values()
            ];

            /*
             * Keep persistence bounded.
             */
            const bounded =
                discoveries.slice(
                    -CONFIG.maxPersistedDiscoveries
                );

            return {
                version: 3,
                visited: [...this.visited],
                discoveries: bounded
            };
        }

        persist() {
            if (!CONFIG.persistState) {
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
                        'discovery-state',
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
                    typeof raw === 'string'
                        ? JSON.parse(raw)
                        : raw;

                /*
                 * Ignore incompatible future state formats.
                 */
                if (
                    data.version &&
                    data.version > 3
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

                log(
                    'Restored state:',
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
