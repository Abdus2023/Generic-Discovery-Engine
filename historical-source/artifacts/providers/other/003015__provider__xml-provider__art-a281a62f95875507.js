    class XmlProvider
        extends ResponseProvider {

        score(observation) {
            const type =
                normalizeContentType(
                    observation.http
                        .contentType
                );

            const body =
                observation.body ||
                '';

            if (
                type ===
                'application/xml' ||
                type ===
                'text/xml'
            ) {
                return 1;
            }

            if (
                type.endsWith(
                    '+xml'
                )
            ) {
                return 0.95;
            }

            if (
                type === '' &&
                looksLikeXml(body)
            ) {
                return 0.82;
            }

            return 0;
        }

        recognize(
            candidate,
            observation
        ) {
            if (
                this.score(
                    observation
                ) <= 0
            ) {
                return null;
            }

            const body =
                observation.body ||
                '';

            const baseUrl =
                observation.http
                    .finalUrl ||
                candidate.target;

            const doc =
                new DOMParser()
                    .parseFromString(
                        body,
                        'application/xml'
                    );

            if (
                doc.querySelector(
                    'parsererror'
                )
            ) {
                return null;
            }

            const urls =
                [];

            for (
                const element of
                doc.querySelectorAll(
                    'loc'
                )
            ) {
                const url =
                    canonicalizeUrl(
                        element
                            .textContent
                            ?.trim(),
                        baseUrl
                    );

                if (
                    url &&
                    isAllowedUrl(
                        url
                    )
                ) {
                    urls.push(
                        url
                    );
                }
            }

            for (
                const element of
                doc.querySelectorAll(
                    'link'
                )
            ) {
                const raw =
                    element.getAttribute(
                        'href'
                    ) ||
                    element.textContent
                        ?.trim();

                const url =
                    canonicalizeUrl(
                        raw,
                        baseUrl
                    );

                if (
                    url &&
                    isAllowedUrl(
                        url
                    )
                ) {
                    urls.push(
                        url
                    );
                }
            }

            const root =
                doc.documentElement
                    ?.localName ||
                '';

            let kind =
                'xml-document';

            if (
                root ===
                'urlset'
            ) {
                kind =
                    'sitemap';
            } else if (
                root ===
                'sitemapindex'
            ) {
                kind =
                    'sitemap-index';
            } else if (
                root ===
                'rss'
            ) {
                kind =
                    'rss-feed';
            } else if (
                root ===
                'feed'
            ) {
                kind =
                    'atom-feed';
            }

            return new Discovery({
                candidate,
                observation,

                kind,

                confidence:
                    kind ===
                        'sitemap' ||
                    kind ===
                        'sitemap-index'
                        ? 0.99
                        : 0.88,

                data: {
                    url:
                        candidate.target,

                    finalUrl:
                        baseUrl,

                    root,

                    urls:
                        unique(
                            urls
                        ).slice(
                            0,
                            CONFIG.maxUrlsPerDiscovery
                        )
                }
            });
        }

        candidates(
            discovery
        ) {
            const depth =
                (
                    discovery
                        .provenance
                        .depth ||
                    0
                ) + 1;

            const type =
                discovery.kind ===
                    'sitemap' ||
                discovery.kind ===
                    'sitemap-index'
                    ? 'sitemap-url'
                    : 'xml-url';

            return (
                discovery.data.urls ||
                []
            ).map(
                url =>
                    makeDerivedCandidate(
                        url,
                        type,
                        discovery,
                        0.68,
                        depth
                    )
            );
        }
    }
