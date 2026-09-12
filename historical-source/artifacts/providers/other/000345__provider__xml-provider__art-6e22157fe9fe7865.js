    class XmlProvider extends Provider {
        constructor() {
            super('xml');
            this.exclusive = true;
        }

        recognize(observation) {
            const type =
                observation.http.contentType || '';

            if (
                isXmlContentType(type) ||
                looksLikeXml(observation.body)
            ) {
                return {
                    recognized: true,
                    confidence: 0.94
                };
            }

            return {
                recognized: false,
                confidence: 0
            };
        }

        discover(observation) {
            const urls =
                extractXmlLocs(
                    observation.body,
                    observation.http.finalUrl ||
                    observation.target
                );

            let kind = 'xml';

            if (
                /sitemap/i.test(
                    observation.target
                )
            ) {
                kind = 'sitemap';
            } else if (
                /rss|atom|feed/i.test(
                    observation.http.contentType ||
                    observation.target
                )
            ) {
                kind = 'feed';
            }

            return urls.map(url =>
                new Discovery({
                    candidateId:
                        observation.candidateId,

                    observationId:
                        observation.id,

                    kind,
                    mechanism: 'xml-location',
                    confidence:
                        kind === 'sitemap'
                            ? 0.95
                            : 0.78,

                    data: { url },

                    provenance: {
                        parent:
                            observation.http.finalUrl ||
                            observation.target,

                        candidateTarget:
                            observation.target,

                        candidateType: kind,

                        mechanism: 'xml-location',
                        depth: 0
                    }
                })
            );
        }
    }
