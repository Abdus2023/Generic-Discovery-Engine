    class XmlProvider
        extends ResponseProvider {

        matches(observation) {
            const type =
                normalizeContentType(
                    observation.http
                        .contentType
                );

            const body =
                observation.body ||
                '';

            return (
                type ===
                    'application/xml' ||
                type ===
                    'text/xml' ||
                type.endsWith(
                    '+xml'
                ) ||
                (
                    type === '' &&
                    looksLikeXml(body)
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

            const parseError =
                doc.querySelector(
                    'parsererror'
                );

            if (parseError) {
                return null;
            }

            const urls = [];

            /*
             * Sitemap:
             *
             * <loc>https://example...</loc>
             */
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
                    isAllowedUrl(url)
                ) {
                    urls.push(url);
                }
            }

            /*
             * RSS/Atom links.
             */
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
                    isAllowedUrl(url)
                ) {
                    urls.push(url);
                }
            }

            /*
             * Generic XML text URL extraction as a secondary signal.
             */
            urls.push(
                ...extractUrlsFromText(
                    body,
                    baseUrl
                )
            );

            const root =
                doc.documentElement
                    ?.localName ||
                '';

            const kind =
                root === 'urlset'
                    ? 'sitemap'
                    : root ===
                        'sitemapindex'
                    ? 'sitemap-index'
                    : root === 'rss'
                    ? 'rss-feed'
                    : root === 'feed'
                    ? 'atom-feed'
                    : 'xml-document';

            return new Discovery({
                candidate,
                observation,

                kind,

                confidence:
                    kind === 'sitemap' ||
                    kind === 'sitemap-index'
                        ? 0.98
                        : 0.85,

                data: {
                    url:
                        candidate.target,

                    finalUrl:
                        baseUrl,

                    root,

                    urls:
                        unique(urls)
                }
            });
        }

        candidates(discovery) {
            const depth =
                (
                    discovery
                        .provenance
                        .depth ||
                    0
                ) + 1;

            return (
                discovery.data.urls ||
                []
            ).map(url =>
                makeDerivedCandidate(
                    url,
                    'xml-url',
                    discovery,
                    0.65,
                    depth
                )
            );
        }
    }
