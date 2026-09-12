    class Discovery {
        constructor({
            candidateId,
            observationId,
            kind,
            confidence = 0.5,
            mechanism = 'unknown',
            data = {},
            provenance = {}
        }) {
            this.id =
                makeId('discovery');

            this.candidateId =
                candidateId;

            this.observationId =
                observationId;

            this.kind =
                kind;

            this.confidence =
                clamp(
                    Number(confidence) || 0,
                    0,
                    1
                );

            this.mechanism =
                mechanism;

            this.data =
                data;

            this.provenance = {
                origin:
                    provenance.origin ||
                    null,

                parent:
                    provenance.parent ||
                    null,

                candidateTarget:
                    provenance.candidateTarget ||
                    null,

                candidateType:
                    provenance.candidateType ||
                    null,

                mechanism,
                depth:
                    Number(
                        provenance.depth ||
                        0
                    )
            };

            this.createdAt =
                now();
        }

        targetUrl() {
            const possible = [
                this.data?.url,
                this.data?.finalUrl,
                this.data?.target,
                this.provenance?.candidateTarget
            ];

            for (const value of possible) {
                const url =
                    canonicalizeUrl(value);

                if (url) {
                    return url;
                }
            }

            return null;
        }
    }
