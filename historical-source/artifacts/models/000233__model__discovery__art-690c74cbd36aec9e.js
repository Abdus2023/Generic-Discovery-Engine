    class Discovery {
        constructor({
            candidate,
            observation,
            kind,
            confidence,
            mechanism,
            data
        }) {
            this.id =
                id('discovery');

            this.candidateId =
                candidate.id;

            this.observationId =
                observation.id;

            this.kind =
                kind;

            this.confidence =
                confidence;

            this.data =
                data || {};

            this.provenance = {
                origin:
                    candidate.origin,

                parent:
                    candidate.parent,

                candidateTarget:
                    candidate.target,

                candidateType:
                    candidate.type,

                mechanism:
                    mechanism ||
                    'provider',

                depth:
                    candidate.depth
            };

            this.createdAt =
                now();
        }
    }
