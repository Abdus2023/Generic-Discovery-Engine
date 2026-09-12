    class XmlProvider extends Provider {
        constructor() {
            super('xml', true);
        }

        matches(candidate, observation) {
            return (
                isXmlContentType(
                    observation.http.contentType
                ) ||
                (
                    candidate.type === 'sitemap' &&
                    looksLikeXml(observation.body)
                ) ||
                looksLikeXml(observation.body)
            );
        }

        recognize(candidate, observation) {
            const base =
                observation.http.finalUrl ||
                candidate.target;

            const urls =
                extractXmlLocs(
                    observation.body,
                    base
                );

            const body =
                observation.body || '';

            let kind = 'xml-document';

            if (
                /<urlset\b|<sitemapindex\b/i.test(body)
            ) {
                kind = 'sitemap';
            } else if (
                /<rss\b/i.test(body)
            ) {
                kind = 'rss-feed';
            } else if (
                /<feed\b/i.test(body)
            ) {
                kind = 'atom-feed';
            }

            return [
                new Discovery({
                    candidateId: candidate.id,
                    observationId: observation.id,
                    kind,
                    confidence:
                        kind === 'sitemap'
                            ? 0.98
                            : 0.87,
                    mechanism: 'xml-parser',
                    data: {
                        url: candidate.target,
                        finalUrl:
                            observation.http.finalUrl,
                        urls,
                        count: urls.length
                    },
                    provenance: {
                        origin: candidate.origin,
                        parent: candidate.parent,
                        candidateTarget: candidate.target,
                        candidateType: candidate.type,
                        depth: candidate.depth
                    }
                })
            ];
        }

        candidates(discovery) {
            return safeArray(
                discovery.data.urls
            ).map(url =>
                new Candidate({
                    target: url,
                    type: looksLikeApiUrl(url)
                        ? 'api'
                        : 'url',
                    origin: 'xml-loc',
                    parent: discovery.id,
                    priority:
                        discovery.kind === 'sitemap'
                            ? 0.86
                            : 0.72,
                    hints: {
                        confidence:
                            discovery.confidence
                    },
                    depth:
                        discovery.provenance.depth + 1
                })
            );
        }
    }
