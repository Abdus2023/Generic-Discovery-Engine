    class XmlProvider extends Provider {
        constructor() {
            super('xml');
        }

        matches(observation) {
            return looksLikeXml(
                observation.http?.contentType,
                observation.body
            );
        }

        async recognize(candidate, observation) {
            const discoveries = [];

            const locs =
                extractXmlLocs(
                    observation.body
                );

            for (const loc of locs) {
                const url =
                    canonicalizeUrl(
                        loc
                    );

                if (!url) continue;

                discoveries.push(
                    new Discovery({
                        candidateId:
                            candidate.id,

                        observationId:
                            observation.id,

                        kind:
                            candidate.type ===
                            'sitemap'
                                ? 'url'
                                : 'xml',

                        confidence:
                            candidate.type ===
                            'sitemap'
                                ? 0.90
                                : 0.70,

                        mechanism:
                            'xml-loc',

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
                                'xml-loc',

                            depth:
                                candidate.depth
                        }
                    })
                );
            }

            return discoveries;
        }
    }
