    class Discovery {
        constructor(options) {
            this.id =
                makeId('discovery');

            this.candidateId =
                options.candidate.id;

            this.observationId =
                options.observation.id;

            this.kind =
                options.kind;

            this.confidence =
                clamp(
                    Number(
                        options.confidence
                    ) || 0
                );

            this.mechanism =
                options.mechanism ||
                'provider';

            this.data =
                options.data ||
                {};

            this.provenance = {
                origin:
                    options.candidate
                        .origin,

                parent:
                    options.candidate
                        .parent,

                candidateTarget:
                    options.candidate
                        .target,

                candidateType:
                    options.candidate
                        .type,

                mechanism:
                    this.mechanism,

                depth:
                    options.candidate
                        .depth
            };

            this.createdAt =
                now();
        }

        target() {
            return (
                this.data.finalUrl ||
                this.data.url ||
                this.provenance
                    .candidateTarget
            );
        }
    }
