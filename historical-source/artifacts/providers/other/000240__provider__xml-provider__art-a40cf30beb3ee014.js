    class XmlProvider
        extends Provider {

        matches(observation) {
            return (
                isXml(
                    observation.http
                        .contentType
                ) ||
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
            if (
                !this.matches(
                    observation
                )
            ) {
                return [];
            }

            const base =
                observation.http
                    .finalUrl ||
                candidate.target;

            const urls =
                extractXmlLocs(
                    observation.body ||
                        '',
                    base
                );

            return [
                new Discovery({
                    candidate,
                    observation,
                    kind:
                        'xml-document',
                    confidence:
                        0.94,
                    mechanism:
                        'xml-parser',
                    data: {
                        url:
                            candidate.target,

                        finalUrl:
                            base,

                        documentType:
                            this.detectType(
                                observation.body
                            ),

                        urls
                    }
                })
            ];
        }

        detectType(xml) {
            if (
                /<urlset[\s>]/i.test(
                    xml
                )
            ) {
                return 'sitemap';
            }

            if (
                /<sitemapindex[\s>]/i.test(
                    xml
                )
            ) {
                return 'sitemap-index';
            }

            if (
                /<rss[\s>]/i.test(
                    xml
                )
            ) {
                return 'rss';
            }

            if (
                /<feed[\s>]/i.test(
                    xml
                )
            ) {
                return 'atom';
            }

            return 'xml';
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
                    target: url,
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
                            ? 0.65
                            : 0.48
                })
            );
        }
    }
