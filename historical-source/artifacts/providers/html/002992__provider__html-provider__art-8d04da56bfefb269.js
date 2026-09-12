    class HtmlProvider
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
                    'text/html' ||
                type ===
                    'application/xhtml+xml' ||
                looksLikeHtml(body)
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
                        'text/html'
                    );

            const title =
                doc.querySelector(
                    'title'
                )
                    ?.textContent
                    ?.trim() ||
                '';

            const links = [];

            if (CONFIG.discoverLinks) {
                for (
                    const element of
                    doc.querySelectorAll(
                        'a[href],area[href]'
                    )
                ) {
                    const url =
                        canonicalizeUrl(
                            element.getAttribute(
                                'href'
                            ),
                            baseUrl
                        );

                    if (
                        url &&
                        isAllowedUrl(url)
                    ) {
                        links.push(url);
                    }
                }
            }

            const resources = [];

            if (CONFIG.discoverResources) {
                const selector = [
                    'script[src]',
                    'link[href]',
                    'img[src]',
                    'iframe[src]',
                    'frame[src]',
                    'source[src]',
                    'video[src]',
                    'audio[src]',
                    'track[src]',
                    'object[data]',
                    'embed[src]',
                    'input[src]',
                    'image[href]'
                ].join(',');

                for (
                    const element of
                    doc.querySelectorAll(
                        selector
                    )
                ) {
                    const raw =
                        element.getAttribute(
                            'src'
                        ) ||
                        element.getAttribute(
                            'href'
                        ) ||
                        element.getAttribute(
                            'data'
                        );

                    const url =
                        canonicalizeUrl(
                            raw,
                            baseUrl
                        );

                    if (
                        url &&
                        isAllowedUrl(url)
                    ) {
                        resources.push(
                            url
                        );
                    }
                }

                /*
                 * srcset can contain multiple URLs.
                 */
                for (
                    const element of
                    doc.querySelectorAll(
                        '[srcset]'
                    )
                ) {
                    const srcset =
                        element.getAttribute(
                            'srcset'
                        ) || '';

                    for (
                        const entry of
                        srcset.split(',')
                    ) {
                        const raw =
                            entry
                                .trim()
                                .split(
                                    /\s+/
                                )[0];

                        const url =
                            canonicalizeUrl(
                                raw,
                                baseUrl
                            );

                        if (
                            url &&
                            isAllowedUrl(url)
                        ) {
                            resources.push(
                                url
                            );
                        }
                    }
                }
            }

            const forms = [];

            if (CONFIG.discoverForms) {
                for (
                    const form of
                    doc.querySelectorAll(
                        'form[action]'
                    )
                ) {
                    const url =
                        canonicalizeUrl(
                            form.getAttribute(
                                'action'
                            ),
                            baseUrl
                        );

                    if (
                        url &&
                        isAllowedUrl(url)
                    ) {
                        forms.push(url);
                    }
                }
            }

            const metadata = [];

            if (CONFIG.discoverMetadata) {
                /*
                 * Canonical.
                 */
                for (
                    const element of
                    doc.querySelectorAll(
                        'link[rel~="canonical"][href]'
                    )
                ) {
                    const url =
                        canonicalizeUrl(
                            element.getAttribute(
                                'href'
                            ),
                            baseUrl
                        );

                    if (
                        url &&
                        isAllowedUrl(url)
                    ) {
                        metadata.push(url);
                    }
                }

                /*
                 * Alternate resources.
                 */
                for (
                    const element of
                    doc.querySelectorAll(
                        'link[rel][href]'
                    )
                ) {
                    const rel =
                        (
                            element.getAttribute(
                                'rel'
                            ) || ''
                        ).toLowerCase();

                    if (
                        !(
                            rel.includes(
                                'alternate'
                            ) ||
                            rel.includes(
                                'manifest'
                            ) ||
                            rel.includes(
                                'preload'
                            ) ||
                            rel.includes(
                                'prefetch'
                            )
                        )
                    ) {
                        continue;
                    }

                    const url =
                        canonicalizeUrl(
                            element.getAttribute(
                                'href'
                            ),
                            baseUrl
                        );

                    if (
                        url &&
                        isAllowedUrl(url)
                    ) {
                        metadata.push(url);
                    }
                }

                /*
                 * OpenGraph and common metadata URL values.
                 */
                for (
                    const element of
                    doc.querySelectorAll(
                        'meta[content]'
                    )
                ) {
                    const property =
                        (
                            element.getAttribute(
                                'property'
                            ) ||
                            element.getAttribute(
                                'name'
                            ) ||
                            ''
                        ).toLowerCase();

                    if (
                        !(
                            property ===
                                'og:url' ||
                            property ===
                                'twitter:url' ||
                            property ===
                                'application-url'
                        )
                    ) {
                        continue;
                    }

                    const url =
                        canonicalizeUrl(
                            element.getAttribute(
                                'content'
                            ),
                            baseUrl
                        );

                    if (
                        url &&
                        isAllowedUrl(url)
                    ) {
                        metadata.push(url);
                    }
                }

                /*
                 * Web App Manifest.
                 */
                for (
                    const element of
                    doc.querySelectorAll(
                        'link[rel~="manifest"][href]'
                    )
                ) {
                    const url =
                        canonicalizeUrl(
                            element.getAttribute(
                                'href'
                            ),
                            baseUrl
                        );

                    if (
                        url &&
                        isAllowedUrl(url)
                    ) {
                        metadata.push(url);
                    }
                }

                /*
                 * Meta refresh.
                 */
                for (
                    const element of
                    doc.querySelectorAll(
                        'meta[http-equiv][content]'
                    )
                ) {
                    const directive =
                        (
                            element.getAttribute(
                                'http-equiv'
                            ) || ''
                        ).toLowerCase();

                    if (
                        directive !==
                        'refresh'
                    ) {
                        continue;
                    }

                    const content =
                        element.getAttribute(
                            'content'
                        ) || '';

                    const match =
                        content.match(
                            /url\s*=\s*(.+)$/i
                        );

                    if (!match) {
                        continue;
                    }

                    const raw =
                        match[1]
                            .trim()
                            .replace(
                                /^['"]|['"]$/g,
                                ''
                            );

                    const url =
                        canonicalizeUrl(
                            raw,
                            baseUrl
                        );

                    if (
                        url &&
                        isAllowedUrl(url)
                    ) {
                        metadata.push(url);
                    }
                }
            }

            /*
             * Embedded URLs.
             */
            const embeddedUrls =
                CONFIG.discoverFromText
                    ? extractUrlsFromText(
                          body,
                          baseUrl
                      )
                    : [];

            /*
             * Stylesheet URL extraction.
             */
            const cssUrls = [];

            if (CONFIG.discoverCss) {
                for (
                    const style of
                    doc.querySelectorAll(
                        'style'
                    )
                ) {
                    cssUrls.push(
                        ...extractCssUrls(
                            style.textContent ||
                                '',
                            baseUrl
                        )
                    );
                }
            }

            return new Discovery({
                candidate,
                observation,

                kind:
                    'html-document',

                confidence:
                    0.95,

                data: {
                    url:
                        candidate.target,

                    finalUrl:
                        baseUrl,

                    title,

                    links:
                        unique(links),

                    resources:
                        unique(resources),

                    forms:
                        unique(forms),

                    metadata:
                        unique(metadata),

                    embeddedUrls:
                        unique(
                            embeddedUrls
                        ),

                    cssUrls:
                        unique(cssUrls)
                }
            });
        }

        candidates(discovery) {
            const result = [];

            const depth =
                (
                    discovery
                        .provenance
                        .depth ||
                    0
                ) + 1;

            if (CONFIG.discoverLinks) {
                for (
                    const url of
                    discovery.data
                        .links || []
                ) {
                    result.push(
                        makeDerivedCandidate(
                            url,
                            'url',
                            discovery,
                            0.8,
                            depth
                        )
                    );
                }
            }

            if (CONFIG.discoverResources) {
                for (
                    const url of
                    discovery.data
                        .resources || []
                ) {
                    result.push(
                        makeDerivedCandidate(
                            url,
                            'resource',
                            discovery,
                            0.5,
                            depth
                        )
                    );
                }
            }

            if (CONFIG.discoverForms) {
                for (
                    const url of
                    discovery.data
                        .forms || []
                ) {
                    result.push(
                        makeDerivedCandidate(
                            url,
                            'form',
                            discovery,
                            0.6,
                            depth
                        )
                    );
                }
            }

            if (CONFIG.discoverMetadata) {
                for (
                    const url of
                    discovery.data
                        .metadata || []
                ) {
                    result.push(
                        makeDerivedCandidate(
                            url,
                            'metadata',
                            discovery,
                            0.7,
                            depth
                        )
                    );
                }
            }

            if (CONFIG.discoverFromText) {
                for (
                    const url of
                    discovery.data
                        .embeddedUrls || []
                ) {
                    result.push(
                        makeDerivedCandidate(
                            url,
                            'embedded-url',
                            discovery,
                            0.4,
                            depth
                        )
                    );
                }
            }

            if (CONFIG.discoverCss) {
                for (
                    const url of
                    discovery.data
                        .cssUrls || []
                ) {
                    result.push(
                        makeDerivedCandidate(
                            url,
                            'stylesheet-url',
                            discovery,
                            0.45,
                            depth
                        )
                    );
                }
            }

            return result;
        }
    }
