    class CssProvider extends Provider {
        constructor() {
            super('css');
            this.exclusive = true;
        }

        recognize(observation) {
            const type =
                observation.http.contentType || '';

            if (
                isCssContentType(type) ||
                /\.css([?#]|$)/i.test(
                    observation.target
                )
            ) {
                return {
                    recognized: true,
                    confidence: 0.96
                };
            }

            return {
                recognized: false,
                confidence: 0
            };
        }

        discover(observation) {
            return extractCssUrls(
                observation.body,
                observation.http.finalUrl ||
                observation.target
            ).map(url =>
                new Discovery({
                    candidateId:
                        observation.candidateId,

                    observationId:
                        observation.id,

                    kind: 'resource',
                    mechanism: 'css-url',
                    confidence: 0.68,

                    data: { url },

                    provenance: {
                        parent:
                            observation.http.finalUrl ||
                            observation.target,

                        candidateTarget:
                            observation.target,

                        candidateType:
                            'stylesheet',

                        mechanism: 'css-url',
                        depth: 0
                    }
                })
            );
        }
    }
