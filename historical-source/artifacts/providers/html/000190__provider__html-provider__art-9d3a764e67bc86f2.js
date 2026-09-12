    class HtmlProvider
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
                'text/html'
            ) {
                return 1;
            }

            if (
                type ===
                'application/xhtml+xml'
            ) {
                return 0.98;
            }

            if (
                looksLikeHtml(body)
            ) {
                return 0.9;
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
                        'text/html'
                    );

            const title =
                doc.querySelector(
                    'title'
                )
                    ?.textContent
                    ?.trim() ||
                '';

            const links =
                [];

            const resources =
                [];

            const forms =
                [];

            const metadata =
                [];

            const cssUrls =
                [];

            if (
                CONFIG.discoverLinks
            ) {
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
                        isAllowedUrl(
                            url
                        )
                    ) {
                        links.push(
                            url
                        );
                    }
                }
            }

            if (
                CONFIG.discoverResources
            ) {
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
                        isAllowedUrl(
                            url
                        )
                    ) {
                        resources.push(
                            url
                        );
                    }
                }

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
                            isAllowedUrl(
                                url
                            )
                        ) {
                            resources.push(
                                url
                            );
                        }
                    }
                }
            }

            if (
                CONFIG.discoverForms
            ) {
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
                        isAllowedUrl(
                            url
                        )
                    ) {
                        forms.push(
                            url
                        );
                    }
                }
            }

            if (
                CONFIG.discoverMetadata
            ) {
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
                                'canonical'
                            ) ||
                            rel.includes(
                                'alternate'
                            ) ||
                            rel.includes(
                                'manifest'
                            ) ||
                            rel.includes(
                                'sitemap'
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
                        isAllowedUrl(
                            url
                        )
                    ) {
                        metadata.push(
                            url
                        );
                    }
                }

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
                        isAllowedUrl(
                            url
                        )
                    ) {
                        metadata.push(
                            url
                        );
                    }
                }

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

                    const url =
                        canonicalizeUrl(
                            match[1]
                                .trim()
                                .replace(
                                    /^['"]|['"]$/g,
                                    ''
                                ),
                            baseUrl
                        );

                    if (
                        url &&
                        isAllowedUrl(
                            url
                        )
                    ) {
                        metadata.push(
                            url
                        );
                    }
                }
            }

            if (
                CONFIG.discoverCss
            ) {
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

            const embeddedUrls =
                CONFIG.discoverFromText
                    ? extractUrlsFromText(
                          body,
                          baseUrl
                      )
                    : [];

            return new Discovery({
                candidate,
                observation,

                kind:
                    'html-document',

                confidence:
                    0.96,

                data: {
                    url:
                        candidate.target,

                    finalUrl:
                        baseUrl,

                    title,

                    links:
                        unique(
                            links
                        ).slice(
                            0,
                            CONFIG.maxUrlsPerDiscovery
                        ),

                    resources:
                        unique(
                            resources
                        ).slice(
                            0,
                            CONFIG.maxUrlsPerDiscovery
                        ),

                    forms:
                        unique(
                            forms
                        ).slice(
                            0,
                            CONFIG.maxUrlsPerDiscovery
                        ),

                    metadata:
                        unique(
                            metadata
                        ).slice(
                            0,
                            CONFIG.maxUrlsPerDiscovery
                        ),

                    embeddedUrls:
                        unique(
                            embeddedUrls
                        ).slice(
                            0,
                            CONFIG.maxUrlsPerDiscovery
                        ),

                    cssUrls:
                        unique(
                            cssUrls
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

            const result = [];

            const add =
                (
                    urls,
                    type,
                    priority
                ) => {
                    for (
                        const url of
                        urls || []
                    ) {
                        result.push(
                            makeDerivedCandidate(
                                url,
                                type,
                                discovery,
                                priority,
                                depth
                            )
                        );
                    }
                };

            if (
                CONFIG.discoverLinks
            ) {
                add(
                    discovery.data.links,
                    'url',
                    0.8
                );
            }

            if (
                CONFIG.discoverResources
            ) {
                add(
                    discovery.data.resources,
                    'resource',
                    0.5
                );
            }

            if (
                CONFIG.discoverForms
            ) {
                add(
                    discovery.data.forms,
                    'form',
                    0.6
                );
            }

            if (
                CONFIG.discoverMetadata
            ) {
                add(
                    discovery.data.metadata,
                    'metadata',
                    0.72
                );
            }

            if (
                CONFIG.discoverFromText
            ) {
                add(
                    discovery.data.embeddedUrls,
                    'embedded-url',
                    0.4
                );
            }

            if (
                CONFIG.discoverCss
            ) {
                add(
                    discovery.data.cssUrls,
                    'stylesheet-url',
                    0.45
                );
            }

            return result;
        }
    }
