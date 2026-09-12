class KnowledgeBase {
    constructor() {
        this.candidates = new Map();
        this.observations = new Map();
        this.discoveries = new Map();
        this.visited = new Set();

        this.load();
    }

    candidateKey(candidate) {
        return candidate.key();
    }

    hasCandidate(candidate) {
        return this.candidates.has(this.candidateKey(candidate));
    }

    addCandidate(candidate) {
        const key = this.candidateKey(candidate);

        if (this.visited.has(key)) {
            return false;
        }

        if (this.candidates.has(key)) {
            return false;
        }

        if (this.candidates.size >= CONFIG.maxCandidates) {
            return false;
        }

        this.candidates.set(key, candidate);

        this.persist();

        return true;
    }

    markVisited(candidate) {
        const key = this.candidateKey(candidate);

        this.visited.add(key);
        this.candidates.delete(key);

        this.persist();
    }

    addObservation(observation) {
        this.observations.set(observation.id, observation);
        this.persist();
    }

    addDiscovery(discovery) {
        this.discoveries.set(discovery.id, discovery);
        this.persist();
    }

    serialize() {
        return {
            visited: [...this.visited],
            discoveries: [...this.discoveries.values()]
        };
    }

    persist() {
        if (!CONFIG.persistState) {
            return;
        }

        try {
            const data = this.serialize();

            if (typeof GM_setValue === 'function') {
                GM_setValue('discovery-state', JSON.stringify(data));
            } else {
                localStorage.setItem(
                    'generic-discovery-state',
                    JSON.stringify(data)
                );
            }
        } catch (error) {
            warn('Persistence failed:', error);
        }
    }

    load() {
        if (!CONFIG.persistState) {
            return;
        }

        try {
            let raw = null;

            if (typeof GM_getValue === 'function') {
                raw = GM_getValue('discovery-state', null);
            } else {
                raw = localStorage.getItem(
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

            for (const key of data.visited || []) {
                this.visited.add(key);
            }

            for (const discovery of data.discoveries || []) {
                this.discoveries.set(
                    discovery.id,
                    discovery
                );
            }
        } catch (error) {
            warn('Could not restore discovery state:', error);
        }
    }

    clear() {
        this.candidates.clear();
        this.observations.clear();
        this.discoveries.clear();
        this.visited.clear();

        this.persist();
    }
}
