    class TextProvider extends Provider {
        constructor() {
            super('text');
        }

        matches(observation) {
            const type =
                contentTypeBase(
                    observation.http
                        ?.contentType
                );

            return (
                type.startsWith('text/') ||
                type === ''
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
                    canonicalizeUrl(raw);

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

                        confidence: 0.40,

                        mechanism:
                            'text-url',

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
                                'text-url',

                            depth:
                                candidate.depth
                        }
                    })
                );
            }

            return discoveries;
        }
    }
