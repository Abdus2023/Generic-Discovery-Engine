    class Discovery {
        constructor(data = {}) {
            this.id =
                data.id || makeId('discovery');

            this.candidateId =
                data.candidateId || null;

            this.observationId =
                data.observationId || null;

            this.kind =
                data.kind || 'url';

            this.confidence =
                Number.isFinite(data.confidence)
                    ? data.confidence
                    : 0.5;

            this.mechanism =
                data.mechanism || 'unknown';

            this.data =
                data.data || {};

            this.provenance =
                data.provenance || {};

            this.createdAt =
                data.createdAt || now();
        }

        targetUrl() {
            return (
                this.data.url ||
                this.data.target ||
                this.provenance.candidateTarget ||
                null
            );
        }

        serialize() {
            return { ...this };
        }
    }
