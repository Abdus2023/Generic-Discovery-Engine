    class HtmlProvider
        extends Provider {

        matches(observation) {
            return (
                isHtml(
                    observation.http
                        .contentType
                ) ||
                looksHtml(
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
                return [];
            }

            const base =
                observation.http
                    .finalUrl ||
                candidate.target;

            const doc =
                new DOMParser()
                    .parseFromString(
                        observation.body ||
                            '',
                        'text/html'
                    );

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
                          base
                      ) || base
                    : base;

            const discoveries =
                [];

            const links =
                [];

            if (
                CONFIG.discoverLinks
            ) {
                for (
                    const el of
                    doc.querySelectorAll(
                        'a[href], area[href]'
                    )
                ) {
                    const url =
                        canonicalizeUrl(
                            el.getAttribute(
                                'href'
                            ),
                            documentBase
                        );

                    if (
                        url &&
                        allowed(url)
                    ) {
                        links.push(url);
                    }
                }
            }

            const resources =
                [];

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
                    const el of
                    doc.querySelectorAll(
                        selector
                    )
                ) {
                    const raw =
                        el.getAttribute(
                            'src'
                        ) ||
                        el.getAttribute(
                            'href'
                        ) ||
                        el.getAttribute(
                            'data'
                        ) ||
                        el.getAttribute(
                            'xlink:href'
                        );

                    const url =
                        canonicalizeUrl(
                            raw,
                            documentBase
                        );

                    if (
                        url &&
                        allowed(url)
                    ) {
                        const tag =
                            el.tagName
                                .toLowerCase();

                        const rel =
                            (
                                el.getAttribute(
                                    'rel'
                                ) || ''
                            ).toLowerCase();

                        let type =
                            'resource';

                        if (
                            tag ===
                            'script'
                        ) {
                            type =
                                'script';
                        } else if (
                            tag === 'link' &&
                            rel.includes(
                                'stylesheet'
                            )
                        ) {
                            type =
                                'stylesheet';
                        } else if (
                            tag === 'link' &&
                            rel.includes(
                                'manifest'
                            )
                        ) {
                            type =
                                'manifest';
                        } else if (
                            tag === 'img' ||
                            tag === 'video' ||
                            tag === 'audio' ||
                            tag === 'source' ||
                            tag === 'track'
                        ) {
                            type =
                                'media';
                        } else if (
                            tag === 'iframe' ||
                            tag === 'frame'
                        ) {
                            type =
                                'frame';
                        }

                        resources.push({
                            url,
                            type
                        });
                    }
                }
            }

            const forms =
                [];

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
                            documentBase
                        );

                    if (
                        url &&
                        allowed(url)
                    ) {
                        forms.push(
                            url
                        );
                    }
                }
            }

            const metadata =
                [];

            if (
                CONFIG.discoverMetadata
            ) {
                for (
                    const selector of [
                        'link[rel~="canonical"][href]',
                        'link[rel~="manifest"][href]',
                        'link[rel~="sitemap"][href]'
                    ]
                ) {
                    for (
                        const el of
                        doc.querySelectorAll(
                            selector
                        )
                    ) {
                        const url =
                            canonicalizeUrl(
                                el.getAttribute(
                                    'href'
                                ),
                                documentBase
                            );

                        if (
                            url &&
                            allowed(url)
                        ) {
                            metadata.push(
                                url
                            );
                        }
                    }
                }

                for (
                    const el of
                    doc.querySelectorAll(
                        'meta[property="og:url"][content], meta[name="twitter:url"][content]'
                    )
                ) {
                    const url =
                        canonicalizeUrl(
                            el.getAttribute(
                                'content'
                            ),
                            documentBase
                        );

                    if (
                        url &&
                        allowed(url)
                    ) {
                        metadata.push(
                            url
                        );
                    }
                }
            }

            const embedded =
                CONFIG.discoverFromText
                    ? extractUrls(
                          observation.body,
                          documentBase
                      )
                    : [];

            const title =
                doc.querySelector(
                    'title'
                )
                    ?.textContent
                    ?.trim() || '';

            if (links.length) {
                discoveries.push(
                    new Discovery({
                        candidate,
                        observation,
                        kind:
                            'html-links',
                        confidence:
                            0.98,
                        mechanism:
                            'html-link-parser',
                        data: {
                            urls:
                                unique(
                                    links
                                )
                        }
                    })
                );
            }

            if (resources.length) {
                discoveries.push(
                    new Discovery({
                        candidate,
                        observation,
                        kind:
                            'html-resources',
                        confidence:
                            0.97,
                        mechanism:
                            'html-resource-parser',
                        data: {
                            resources,
                            title
                        }
                    })
                );
            }

            if (forms.length) {
                discoveries.push(
                    new Discovery({
                        candidate,
                        observation,
                        kind:
                            'html-forms',
                        confidence:
                            0.94,
                        mechanism:
                            'html-form-parser',
                        data: {
                            urls:
                                unique(
                                    forms
                                )
                        }
                    })
                );
            }

            if (metadata.length) {
                discoveries.push(
                    new Discovery({
                        candidate,
                        observation,
                        kind:
                            'html-metadata',
                        confidence:
                            0.96,
                        mechanism:
                            'html-metadata-parser',
                        data: {
                            urls:
                                unique(
                                    metadata
                                )
                        }
                    })
                );
            }

            if (embedded.length) {
                discoveries.push(
                    new Discovery({
                        candidate,
                        observation,
                        kind:
                            'html-embedded-urls',
                        confidence:
                            0.75,
                        mechanism:
                            'html-text-parser',
                        data: {
                            urls:
                                unique(
                                    embedded
                                )
                        }
                    })
                );
            }

            /*
             * Always produce a document-level discovery so that
             * the resource itself has a graph node even if it
             * contained no outbound resources.
             */
            discoveries.unshift(
                new Discovery({
                    candidate,
                    observation,
                    kind:
                        'html-document',
                    confidence:
                        0.99,
                    mechanism:
                        'html-recognition',
                    data: {
                        url:
                            candidate.target,

                        finalUrl:
                            documentBase,

                        title
                    }
                })
            );

            return discoveries;
        }

        candidates(
            discovery
        ) {
            const depth =
                discovery
                    .provenance
                    .depth + 1;

            const parent =
                discovery.id;

            if (
                discovery.kind ===
                'html-links' ||
                discovery.kind ===
                'html-forms' ||
                discovery.kind ===
                'html-metadata' ||
                discovery.kind ===
                'html-embedded-urls'
            ) {
                return (
                    discovery.data.urls ||
                    []
                ).map(url =>
                    new Candidate({
                        target: url,
                        type:
                            discovery.kind ===
                            'html-forms'
                                ? 'form'
                                : 'url',
                        origin:
                            discovery
                                .provenance
                                .mechanism,
                        parent,
                        depth,
                        priority:
                            discovery.kind ===
                            'html-links'
                                ? 0.82
                                : 0.68
                    })
                );
            }

            if (
                discovery.kind ===
                'html-resources'
            ) {
                return (
                    discovery.data.resources ||
                    []
                ).map(resource =>
                    new Candidate({
                        target:
                            resource.url,

                        type:
                            resource.type,

                        origin:
                            'html-resource-parser',

                        parent,

                        depth,

                        priority:
                            resource.type ===
                            'script'
                                ? 0.60
                                : resource.type ===
                                  'manifest'
                                ? 0.82
                                : resource.type ===
                                  'stylesheet'
                                ? 0.46
                                : resource.type ===
                                  'media'
                                ? 0.25
                                : 0.42
                    })
                );
            }

            return [];
        }
    }
