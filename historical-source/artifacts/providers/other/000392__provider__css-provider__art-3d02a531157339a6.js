    class CssProvider extends Provider {
        constructor() {
            super('css');
        }

        matches(observation) {
            return looksLikeCss(
                observation.http?.contentType
            );
        }

        async recognize(candidate, observation) {
            const discoveries = [];

            for (
                const raw of
                extractCssUrls(
                    observation.body
                )
            ) {
                const url =
                    canonicalizeUrl(
                        new URL(
                            raw,
                            observation.requestedUrl
                        ).href
                    );

                if (!url) continue;

                discoveries.push(
                    new Discovery({
                        candidateId:
                            candidate.id,

                        observationId:
                            observation.id,

                        kind: 'resource',

                        confidence: 0.60,

                        mechanism:
                            'css-url',

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
                                'css-url',

                            depth:
                                candidate.depth
                        }
                    })
                );
            }

            return discoveries;
        }
    }
