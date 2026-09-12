    class Discovery {
        constructor({
            candidate,
            observation = null,
            kind,
            confidence = 0.5,
            data = {},
            mechanism = 'active-acquisition'
        }) {
            this.id =
                makeId('discovery');

            this.candidateId =
                candidate.id;

            this.observationId =
                observation
                    ? observation.id
                    : null;

            this.kind =
                kind;

            this.confidence =
                confidence;

            this.mechanism =
                mechanism;

            this.data =
                data;

            this.provenance = {
                origin:
                    candidate.origin,

                parent:
                    candidate.parent,

                depth:
                    candidate.depth
            };

            this.createdAt =
                now();
        }
    }
