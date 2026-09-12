    class HtmlProvider
        extends Provider {

        matches(
            candidate,
            observation
        ) {
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

            const baseElement =
                doc.querySelector(
                    'base[href]'
                );

            const documentBase =
                baseElement
                    ? canonicalizeUrl(
                          baseElement
                              .getAttribute(
                                  'href'
                              ),
                          base
                      ) || base
                    : base;

            const references =
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
                            documentBase
                        );

                    if (
                        url &&
                        allowed(url)
                    ) {
                        references.push({
                            url,
                            type:
                                'url',
                            mechanism:
                                'html-link',
                            tag:
                                element.tagName
                                    .toLowerCase()
                        });
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
                    'embed[src]'
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
                            documentBase
                        );

                    if (
                        !url ||
                        !allowed(url)
                    ) {
                        continue;
                    }

                    const tag =
                        element.tagName
                            .toLowerCase();

                    const rel =
                        (
                            element.getAttribute(
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
                        tag === 'iframe' ||
                        tag === 'frame'
                    ) {
                        type =
                            'frame';
                    } else if (
                        tag === 'img' ||
                        tag === 'video' ||
                        tag === 'audio' ||
                        tag === 'source' ||
                        tag === 'track'
                    ) {
                        type =
                            'media';
                    }

                    references.push({
                        url,
                        type,
                        mechanism:
                            'html-resource',
                        tag,
                        rel
                    });
                }
            }

            if (
                CONFIG.discoverMetadata
            ) {
                for (
                    const element of
                    doc.querySelectorAll(
                        'link[href]'
                    )
                ) {
                    const rel =
                        (
                            element.getAttribute(
                                'rel'
                            ) || ''
                        ).toLowerCase();

                    const url =
                        canonicalizeUrl(
                            element.getAttribute(
                                'href'
                            ),
                            documentBase
                        );

                    if (
                        !url ||
                        !allowed(url)
                    ) {
                        continue;
                    }

                    if (
                        rel.includes(
                            'sitemap'
                        )
                    ) {
                        references.push({
                            url,
                            type:
                                'sitemap',
                            mechanism:
                                'html-sitemap',
                            tag:
                                'link',
                            rel
                        });
                    } else if (
                        rel.includes(
                            'alternate'
                        )
                    ) {
                        references.push({
                            url,
                            type:
                                'feed',
                            mechanism:
                                'html-alternate',
                            tag:
                                'link',
                            rel
                        });
                    } else if (
                        rel.includes(
                            'canonical'
                        )
                    ) {
                        references.push({
                            url,
                            type:
                                'metadata',
                            mechanism:
                                'html-canonical',
                            tag:
                                'link',
                            rel
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

            const discoveries = [
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
            ];

            if (
                references.length
            ) {
                discoveries.push(
                    new Discovery({
                        candidate,
                        observation,
                        kind:
                            'html-references',
                        confidence:
                            0.97,
                        mechanism:
                            'html-reference-parser',
                        data: {
                            references
                        }
                    })
                );
            }

            if (
                forms.length
            ) {
                discoveries.push(
                    new Discovery({
                        candidate,
                        observation,
                        kind:
                            'html-forms',
                        confidence:
                            0.92,
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

            if (
                embedded.length
            ) {
                discoveries.push(
                    new Discovery({
                        candidate,
                        observation,
                        kind:
                            'html-embedded-urls',
                        confidence:
                            0.72,
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

            return discoveries;
        }

        candidates(
            discovery
        ) {
            const depth =
                discovery
                    .provenance
                    .depth + 1;

            if (
                discovery.kind ===
                'html-references'
            ) {
                return (
                    discovery.data
                        .references || []
                ).map(
                    reference =>
                        new Candidate({
                            target:
                                reference.url,

                            type:
                                reference.type,

                            origin:
                                reference.mechanism,

                            parent:
                                discovery.id,

                            depth,

                            priority:
                                TYPE_PRIORITY[
                                    reference.type
                                ] ??
                                0.45,

                            hints: {
                                confidence:
                                    discovery.confidence,

                                relation:
                                    reference.rel ||
                                    null
                            }
                        })
                );
            }

            if (
                discovery.kind ===
                'html-forms'
            ) {
                return (
                    discovery.data.urls ||
                    []
                ).map(url =>
                    new Candidate({
                        target:
                            url,

                        type:
                            'form',

                        origin:
                            'html-form-parser',

                        parent:
                            discovery.id,

                        depth,

                        priority:
                            0.36,

                        hints: {
                            confidence:
                                discovery.confidence
                        }
                    })
                );
            }

            if (
                discovery.kind ===
                'html-embedded-urls'
            ) {
                return (
                    discovery.data.urls ||
                    []
                ).map(url =>
                    new Candidate({
                        target:
                            url,

                        type:
                            classifyUrl(
                                url
                            ),

                        origin:
                            'html-text-parser',

                        parent:
                            discovery.id,

                        depth,

                        priority:
                            0.34,

                        hints: {
                            confidence:
                                discovery.confidence
                        }
                    })
                );
            }

            return [];
        }
    }
