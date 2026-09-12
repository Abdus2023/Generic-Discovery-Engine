    class TextProvider extends Provider {
        constructor() {
            super('text');
            this.exclusive = false;
        }

        recognize(observation) {
            if (
                observation.body &&
                observation.body.length
            ) {
                return {
                    recognized: true,
                    confidence: 0.20
                };
            }

            return {
                recognized: false,
                confidence: 0
            };
        }

        discover(observation) {
            return extractUrlsFromText(
                observation.body,
                observation.http.finalUrl ||
                observation.target
            ).map(url =>
                new Discovery({
                    candidateId:
                        observation.candidateId,

                    observationId:
                        observation.id,

                    kind:
                        looksLikeApiUrl(url)
                            ? 'api'
                            : 'url',

                    mechanism:
                        'text-url-extraction',

                    confidence: 0.42,

                    data: { url },

                    provenance: {
                        parent:
                            observation.http.finalUrl ||
                            observation.target,

                        candidateTarget:
                            observation.target,

                        candidateType: 'text',

                        mechanism:
                            'text-url-extraction',

                        depth: 0
                    }
                })
            );
        }
    }
