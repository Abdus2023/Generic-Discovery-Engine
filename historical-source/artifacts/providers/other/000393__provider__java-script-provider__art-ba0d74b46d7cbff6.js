    class JavaScriptProvider extends Provider {
        constructor() {
            super('javascript');
        }

        matches(observation) {
            return looksLikeJavaScript(
                observation.http?.contentType
            );
        }

        async recognize(candidate, observation) {
            const discoveries = [];

            for (
                const raw of
                extractUrlsFromText(
                    observation.body
                )
            ) {
                const url =
                    canonicalizeUrl(
                        raw
                    );

                if (!url) continue;

                discoveries.push(
                    new Discovery({
                        candidateId:
                            candidate.id,

                        observationId:
                            observation.id,

                        kind:
                            looksLikeApiUrl(url)
                                ? 'api'
                                : 'url',

                        confidence:
                            looksLikeApiUrl(url)
                                ? 0.65
                                : 0.45,

                        mechanism:
                            'javascript-url',

                        data: {
                            url
                        },

                        provenance: {
                            origin:
                                candidate.origin,

                            parent:
                                candidate.target,

                            candidateTarget:
                                candidate.target,

                            candidateType:
                                candidate.type,

                            mechanism:
                                'javascript-url',

                            depth:
                                candidate.depth
                        }
                    })
                );
            }

            return discoveries;
        }
    }
