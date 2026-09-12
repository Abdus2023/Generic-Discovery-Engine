class KnowledgeBase {

    constructor() {
        this.candidates = new Map();

        this.observations = new Map();

        this.discoveries = new Map();

        /*
         * visited:
         *     candidates permanently completed.
         *
         * claimed:
         *     candidates currently owned by a worker.
         *
         * Keeping claimed separate from visited is important.
         */
        this.visited = new Set();
        this.claimed = new Set();

        this.load();
    }

    candidateKey(candidate) {
        return candidate.key();
    }

    addCandidate(candidate) {

        const key =
            this.candidateKey(candidate);

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
     * JavaScript executes this synchronous section without another
     * worker being able to interleave an await.
     *
     * A worker therefore:
     *
     *     1. asks for the next candidate
     *     2. candidate is immediately removed from the queue
     *     3. candidate is immediately placed in claimed
     *     4. only then does the worker perform async I/O
     *
     * This prevents two concurrent workers from claiming the same
     * candidate.
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
             * Claim is synchronous and happens before returning.
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
        }

        this.persist();
    }

    addObservation(observation) {
        this.observations.set(
            observation.id,
            observation
        );

        this.persist();
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

    serialize() {
        return {
            visited: [...this.visited],

            discoveries: [
                ...this.discoveries.values()
            ]
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
                this.discoveries.set(
                    discovery.id,
                    discovery
                );
            }

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
