    class JsonProvider extends Provider {
        constructor() {
            super('json');
            this.exclusive = true;
        }

        recognize(observation) {
            const type =
                observation.http.contentType || '';

            if (
                isJsonContentType(type) ||
                looksLikeJson(observation.body)
            ) {
                return {
                    recognized: true,
                    confidence: 0.97
                };
            }

            return {
                recognized: false,
                confidence: 0
            };
        }

        discover(observation) {
            let value;

            try {
                value =
                    JSON.parse(observation.body);
            } catch {
                return [];
            }

            const text =
                JSON.stringify(value);

            const urls =
                extractUrlsFromText(
                    text,
                    observation.http.finalUrl ||
                    observation.target
                );

            const discoveries =
                urls.map(url =>
                    new Discovery({
                        candidateId:
                            observation.candidateId,

                        observationId:
                            observation.id,

                        kind:
                            /manifest\.json/i.test(
                                observation.target
                            )
                                ? 'manifest'
                                : 'url',

                        mechanism:
                            'json-url-extraction',

                        confidence:
                            looksLikeApiUrl(
                                observation.target
                            )
                                ? 0.86
                                : 0.72,

                        data: {
                            url
                        },

                        provenance: {
                            parent:
                                observation.http.finalUrl ||
                                observation.target,

                            candidateTarget:
                                observation.target,

                            candidateType:
                                'api',

                            mechanism:
                                'json-url-extraction',

                            depth: 0
                        }
                    })
                );

            return discoveries;
        }
    }
