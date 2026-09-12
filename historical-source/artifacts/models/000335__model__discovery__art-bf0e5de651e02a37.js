    class Discovery {
        constructor(data = {}) {
            this.id = data.id || makeId('disc');

            this.candidateId = data.candidateId || null;
            this.observationId = data.observationId || null;

            this.kind = data.kind || 'url';

            this.confidence = Number.isFinite(data.confidence)
                ? data.confidence
                : 0.5;

            this.mechanism = data.mechanism || 'unknown';

            this.data = data.data || {};

            this.provenance = {
                origin: data.provenance?.origin || null,
                parent: data.provenance?.parent || null,
                candidateTarget: data.provenance?.candidateTarget || null,
                candidateType: data.provenance?.candidateType || null,
                mechanism: data.provenance?.mechanism || this.mechanism,
                depth: data.provenance?.depth ?? 0
            };

            this.createdAt = data.createdAt || now();
        }

        targetUrl() {
            if (this.data.url) {
                return canonicalizeUrl(
                    this.data.url,
                    this.provenance.parent || location.href
                );
            }

            if (this.data.target) {
                return canonicalizeUrl(
                    this.data.target,
                    this.provenance.parent || location.href
                );
            }

            return this.provenance.candidateTarget || null;
        }

        serialize() {
            return { ...this };
        }
    }
