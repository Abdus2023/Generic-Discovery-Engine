    class XmlProvider
        extends Provider {

        matches(
            candidate,
            observation
        ) {
            return (
                isXml(
                    observation.http
                        .contentType
                ) ||
                candidate.type ===
                    'sitemap' ||
                /<loc[\s>]/i.test(
                    observation.body ||
                        ''
                )
            );
        }

        recognize(
            candidate,
            observation
        ) {
            const base =
                observation.http
                    .finalUrl ||
                candidate.target;

            const body =
                observation.body ||
                '';

            let documentType =
                'xml';

            if (
                /<urlset[\s>]/i.test(
                    body
                )
            ) {
                documentType =
                    'sitemap';
            } else if (
                /<sitemapindex[\s>]/i.test(
                    body
                )
            ) {
                documentType =
                    'sitemap-index';
            } else if (
                /<rss[\s>]/i.test(
                    body
                )
            ) {
                documentType =
                    'rss';
            } else if (
                /<feed[\s>]/i.test(
                    body
                )
            ) {
                documentType =
                    'atom';
            }

            return [
                new Discovery({
                    candidate,
                    observation,
                    kind:
                        'xml-document',
                    confidence:
                        0.95,
                    mechanism:
                        'xml-parser',
                    data: {
                        url:
                            candidate.target,

                        finalUrl:
                            base,

                        documentType,

                        urls:
                            extractXmlLocs(
                                body,
                                base
                            )
                    }
                })
            ];
        }

        candidates(
            discovery
        ) {
            const depth =
                discovery
                    .provenance
                    .depth + 1;

            return (
                discovery.data.urls ||
                []
            ).map(url =>
                new Candidate({
                    target:
                        url,

                    type:
                        discovery.data
                            .documentType ===
                        'sitemap'
                            ? 'url'
                            : 'resource',

                    origin:
                        'xml-parser',

                    parent:
                        discovery.id,

                    depth,

                    priority:
                        discovery.data
                            .documentType ===
                        'sitemap'
                            ? 0.64
                            : 0.42,

                    hints: {
                        confidence:
                            discovery.confidence
                    }
                })
            );
        }
    }
