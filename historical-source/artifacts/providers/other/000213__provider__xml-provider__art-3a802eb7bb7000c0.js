    class XmlProvider
        extends ResponseProvider {

        matches(observation) {
            const type =
                observation
                    .http
                    .contentType;

            const body =
                observation.body ||
                '';

            return (
                isXmlContentType(
                    type
                ) ||
                (
                    !isHtmlContentType(
                        type
                    ) &&
                    /<loc[\s>]/i.test(
                        body
                    )
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
                return null;
            }

            const baseUrl =
                observation
                    .http
                    .finalUrl ||
                candidate.target;

            const urls =
                extractXmlLocs(
                    observation.body ||
                        '',
                    baseUrl
                );

            return new Discovery({
                candidate,
                observation,
                kind:
                    'xml-document',
                confidence: 0.92,
                mechanism:
                    'xml-parser',
                data: {
                    url:
                        candidate.target,

                    finalUrl:
                        baseUrl,

                    urls,

                    documentType:
                        this.detectType(
                            observation.body ||
                                ''
                        )
                }
            });
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

        candidates(discovery) {
            const depth =
                (
                    discovery
                        .provenance
                        .depth || 0
                ) + 1;

            return (
                discovery.data.urls ||
                []
            ).map(url =>
                new Candidate({
                    target: url,
                    type: 'url',
                    origin:
                        `xml:${discovery.id}`,
                    parent:
                        discovery.id,
                    priority: 0.65,
                    depth
                })
            );
        }
    }
