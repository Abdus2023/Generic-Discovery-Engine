    class ResourceRecord {
        constructor(data = {}) {
            this.id = data.id || stableId('res', data.url || makeId());

            this.url = canonicalizeUrl(data.url) || data.url;

            this.types = new Set(safeArray(data.types));
            this.mechanisms = new Set(safeArray(data.mechanisms));
            this.parents = new Set(safeArray(data.parents));

            this.candidateIds = new Set(safeArray(data.candidateIds));
            this.observationIds = new Set(safeArray(data.observationIds));
            this.discoveryIds = new Set(safeArray(data.discoveryIds));
            this.networkEventIds = new Set(safeArray(data.networkEventIds));

            this.firstSeenAt = data.firstSeenAt || now();
            this.lastSeenAt = data.lastSeenAt || this.firstSeenAt;

            this.status = data.status || 'known';

            this.fingerprint = data.fingerprint || null;
            this.finalUrl = data.finalUrl || null;

            this.skipReason = data.skipReason || null;
        }

        addType(type) {
            if (type) this.types.add(type);
        }

        addMechanism(mechanism) {
            if (mechanism) this.mechanisms.add(mechanism);
        }

        serialize() {
            return {
                id: this.id,
                url: this.url,
                types: [...this.types],
                mechanisms: [...this.mechanisms],
                parents: [...this.parents],
                candidateIds: [...this.candidateIds],
                observationIds: [...this.observationIds],
                discoveryIds: [...this.discoveryIds],
                networkEventIds: [...this.networkEventIds],
                firstSeenAt: this.firstSeenAt,
                lastSeenAt: this.lastSeenAt,
                status: this.status,
                fingerprint: this.fingerprint,
                finalUrl: this.finalUrl,
                skipReason: this.skipReason
            };
        }
    }
