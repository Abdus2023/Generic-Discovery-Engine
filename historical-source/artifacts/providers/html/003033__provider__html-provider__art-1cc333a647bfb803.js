    class HtmlProvider
        extends ResponseProvider {

        matches(observation) {
            return (
                isHtmlContentType(
                    observation
                        .http
                        .contentType
                ) ||
                looksLikeHtml(
                    observation.body
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

            const doc =
                new DOMParser()
                    .parseFromString(
                        body,
                        'text/html'
                    );

            /*
             * The fetched document does not have the URL
             * of the current page as its base. Therefore all
             * relative URLs must be resolved explicitly.
             */
            const baseUrl =
                observation.http.finalUrl ||
                candidate.target;

            const explicitBase =
                doc.querySelector(
                    'base[href]'
                );

            const documentBase =
                explicitBase
                    ? canonicalizeUrl(
                          explicitBase.getAttribute(
                              'href'
                          ),
                          baseUrl
                      ) ||
                      baseUrl
                    : baseUrl;

            const title =
                doc.querySelector(
                    'title'
                )
                    ?.textContent
                    ?.trim() || '';

            const links = [];

            if (
                CONFIG.discoverLinks
            ) {
                for (
                    const element of
                    doc.querySelectorAll(
                        'a[href], area[href]'
                    )
                ) {
                    const raw =
                        element.getAttribute(
                            'href'
                        );

                    const url =
                        canonicalizeUrl(
                            raw,
                            documentBase
                        );

                    if (
                        url &&
                        isAllowedUrl(url)
                    ) {
                        links.push(
                            url
                        );
                    }
                }
            }

            const resources = [];

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
                    'image[href]',
                    'use[href]',
                    'use[xlink\\:href]'
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
                        ) ||
                        element.getAttribute(
                            'xlink:href'
                        );

                    const url =
                        canonicalizeUrl(
                            raw,
                            documentBase
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

            const forms = [];

            if (
                CONFIG.discoverForms
            ) {
                for (
                    const form of
                    doc.querySelectorAll(
                        'form[action]'
                    )
                ) {
                    const raw =
                        form.getAttribute(
                            'action'
                        );

                    const url =
                        canonicalizeUrl(
                            raw,
                            documentBase
                        );

                    if (
                        url &&
                        isAllowedUrl(url)
                    ) {
                        forms.push(
                            url
                        );
                    }
                }
            }

            const metadata = [];

            if (
                CONFIG.discoverMetadata
            ) {
                const canonical =
                    doc.querySelector(
                        'link[rel~="canonical"][href]'
                    );

                if (canonical) {
                    const url =
                        canonicalizeUrl(
                            canonical.getAttribute(
                                'href'
                            ),
                            documentBase
                        );

                    if (
                        url &&
                        isAllowedUrl(url)
                    ) {
                        metadata.push(
                            url
                        );
                    }
                }

                for (
                    const element of
                    doc.querySelectorAll(
                        'meta[property="og:url"][content], meta[name="twitter:url"][content]'
                    )
                ) {
                    const url =
                        canonicalizeUrl(
                            element.getAttribute(
                                'content'
                            ),
                            documentBase
                        );

                    if (
                        url &&
                        isAllowedUrl(url)
                    ) {
                        metadata.push(
                            url
                        );
                    }
                }

                const manifest =
                    doc.querySelector(
                        'link[rel~="manifest"][href]'
                    );

                if (manifest) {
                    const url =
                        canonicalizeUrl(
                            manifest.getAttribute(
                                'href'
                            ),
                            documentBase
                        );

                    if (
                        url &&
                        isAllowedUrl(url)
                    ) {
                        metadata.push(
                            url
                        );
                    }
                }

                for (
                    const element of
                    doc.querySelectorAll(
                        'link[rel~="sitemap"][href]'
                    )
                ) {
                    const url =
                        canonicalizeUrl(
                            element.getAttribute(
                                'href'
                            ),
                            documentBase
                        );

                    if (
                        url &&
                        isAllowedUrl(url)
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
                    const httpEquiv =
                        element.getAttribute(
                            'http-equiv'
                        );

                    if (
                        !httpEquiv ||
                        httpEquiv.toLowerCase() !==
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
                            documentBase
                        );

                    if (
                        url &&
                        isAllowedUrl(url)
                    ) {
                        metadata.push(
                            url
                        );
                    }
                }
            }

            const embeddedUrls =
                CONFIG.discoverFromText
                    ? extractUrlsFromText(
                          body,
                          documentBase
                      )
                    : [];

            return new Discovery({
                candidate,
                observation,
                kind:
                    'html-document',
                confidence: 0.95,
                mechanism:
                    'html-parser',
                data: {
                    url:
                        candidate.target,

                    finalUrl:
                        documentBase,

                    title,

                    links:
                        unique(
                            links
                        ),

                    resources:
                        unique(
                            resources
                        ),

                    forms:
                        unique(
                            forms
                        ),

                    metadata:
                        unique(
                            metadata
                        ),

                    embeddedUrls:
                        unique(
                            embeddedUrls
                        )
                }
            });
        }

        candidates(discovery) {
            const result = [];

            const depth =
                (
                    discovery
                        .provenance
                        .depth || 0
                ) + 1;

            const parent =
                discovery.id;

            for (
                const url of
                discovery.data.links ||
                []
            ) {
                result.push(
                    new Candidate({
                        target: url,
                        type: 'url',
                        origin:
                            `html:${discovery.id}`,
                        parent,
                        priority: 0.82,
                        depth
                    })
                );
            }

            for (
                const url of
                discovery.data.resources ||
                []
            ) {
                result.push(
                    new Candidate({
                        target: url,
                        type: 'resource',
                        origin:
                            `html:${discovery.id}`,
                        parent,
                        priority: 0.52,
                        depth
                    })
                );
            }

            for (
                const url of
                discovery.data.forms ||
                []
            ) {
                result.push(
                    new Candidate({
                        target: url,
                        type: 'form',
                        origin:
                            `html:${discovery.id}`,
                        parent,
                        priority: 0.62,
                        depth
                    })
                );
            }

            for (
                const url of
                discovery.data.metadata ||
                []
            ) {
                result.push(
                    new Candidate({
                        target: url,
                        type: 'metadata',
                        origin:
                            `html:${discovery.id}`,
                        parent,
                        priority: 0.72,
                        depth
                    })
                );
            }

            for (
                const url of
                discovery.data.embeddedUrls ||
                []
            ) {
                result.push(
                    new Candidate({
                        target: url,
                        type:
                            'embedded-url',
                        origin:
                            `html:${discovery.id}`,
                        parent,
                        priority: 0.42,
                        depth
                    })
                );
            }

            return result;
        }
    }
