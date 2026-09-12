    class HtmlProvider
        extends Provider {

        constructor() {
            super(
                'html',
                true
            );
        }

        matches(
            candidate,
            observation
        ) {
            const type =
                observation.http.contentType;

            return (
                isHtmlContentType(type) ||
                (
                    !type &&
                    looksLikeHtml(
                        observation.body
                    )
                ) ||
                (
                    candidate.type === 'url' &&
                    looksLikeHtml(
                        observation.body
                    )
                )
            );
        }

        classifyLink(element) {
            const rel =
                String(
                    element.getAttribute(
                        'rel'
                    ) || ''
                )
                    .toLowerCase()
                    .split(/\s+/)
                    .filter(Boolean);

            const type =
                String(
                    element.getAttribute(
                        'type'
                    ) || ''
                ).toLowerCase();

            if (
                rel.includes(
                    'stylesheet'
                )
            ) {
                return 'stylesheet';
            }

            if (
                rel.includes(
                    'manifest'
                )
            ) {
                return 'manifest';
            }

            if (
                rel.includes(
                    'sitemap'
                )
            ) {
                return 'sitemap';
            }

            if (
                type.includes('rss') ||
                type.includes('atom')
            ) {
                return 'feed';
            }

            if (
                rel.includes('canonical') ||
                rel.includes('alternate') ||
                rel.includes('author')
            ) {
                return 'metadata';
            }

            if (
                rel.includes('preload') ||
                rel.includes('prefetch') ||
                rel.includes('modulepreload')
            ) {
                return 'resource';
            }

            return 'url';
        }

        addReference(
            references,
            url,
            type,
            meta = {}
        ) {
            if (
                !url ||
                !isAllowedUrl(url)
            ) {
                return;
            }

            references.push({
                url,
                type,
                ...meta
            });
        }

        recognize(
            candidate,
            observation
        ) {
            const parser =
                new DOMParser();

            const fetchedUrl =
                observation.http.finalUrl ||
                candidate.target;

            const doc =
                parser.parseFromString(
                    observation.body,
                    'text/html'
                );

            const baseElement =
                doc.querySelector(
                    'base[href]'
                );

            const baseUrl =
                baseElement
                    ? (
                        canonicalizeUrl(
                            baseElement.getAttribute(
                                'href'
                            ),
                            fetchedUrl
                        ) ||
                        fetchedUrl
                    )
                    : fetchedUrl;

            const references = [];

            if (
                CONFIG.discoverLinks
            ) {
                for (
                    const element of
                    doc.querySelectorAll(
                        'a[href], area[href]'
                    )
                ) {
                    const url =
                        canonicalizeUrl(
                            element.getAttribute(
                                'href'
                            ),
                            baseUrl
                        );

                    this.addReference(
                        references,
                        url,
                        'url',
                        {
                            relation:
                                element.getAttribute(
                                    'rel'
                                ) || '',

                            tag:
                                element.tagName
                                    .toLowerCase(),

                            attribute:
                                'href'
                        }
                    );
                }
            }

            if (
                CONFIG.discoverResources
            ) {
                const selectors = [
                    [
                        'script[src]',
                        'src',
                        'script'
                    ],
                    [
                        'link[href]',
                        'href',
                        'resource'
                    ],
                    [
                        'img[src]',
                        'src',
                        'media'
                    ],
                    [
                        'iframe[src], frame[src]',
                        'src',
                        'frame'
                    ],
                    [
                        'video[src], audio[src], source[src], track[src]',
                        'src',
                        'media'
                    ],
                    [
                        'object[data]',
                        'data',
                        'resource'
                    ],
                    [
                        'embed[src]',
                        'src',
                        'resource'
                    ]
                ];

                for (
                    const [
                        selector,
                        attribute,
                        defaultType
                    ] of selectors
                ) {
                    for (
                        const element of
                        doc.querySelectorAll(
                            selector
                        )
                    ) {
                        const url =
                            canonicalizeUrl(
                                element.getAttribute(
                                    attribute
                                ),
                                baseUrl
                            );

                        let type =
                            defaultType;

                        if (
                            selector ===
                            'link[href]'
                        ) {
                            type =
                                this.classifyLink(
                                    element
                                );
                        }

                        this.addReference(
                            references,
                            url,
                            type,
                            {
                                relation:
                                    element.getAttribute(
                                        'rel'
                                    ) || '',

                                tag:
                                    element.tagName
                                        .toLowerCase(),

                                attribute
                            }
                        );
                    }
                }

                for (
                    const element of
                    doc.querySelectorAll(
                        'img[srcset], source[srcset]'
                    )
                ) {
                    const srcset =
                        element.getAttribute(
                            'srcset'
                        );

                    for (
                        const part of
                        String(
                            srcset || ''
                        ).split(',')
                    ) {
                        const raw =
                            part.trim()
                                .split(/\s+/)[0];

                        const url =
                            canonicalizeUrl(
                                raw,
                                baseUrl
                            );

                        this.addReference(
                            references,
                            url,
                            'media',
                            {
                                tag:
                                    element.tagName
                                        .toLowerCase(),

                                attribute:
                                    'srcset'
                            }
                        );
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

                    this.addReference(
                        references,
                        url,
                        'form',
                        {
                            tag: 'form',

                            attribute:
                                'action',

                            method:
                                normalizeMethod(
                                    form.getAttribute(
                                        'method'
                                    ) || 'GET'
                                )
                        }
                    );
                }
            }

            if (
                CONFIG.discoverMetadata
            ) {
                for (
                    const element of
                    doc.querySelectorAll(
                        'meta[content]'
                    )
                ) {
                    const property =
                        element.getAttribute(
                            'property'
                        ) ||
                        element.getAttribute(
                            'name'
                        ) ||
                        element.getAttribute(
                            'itemprop'
                        ) ||
                        '';

                    const content =
                        element.getAttribute(
                            'content'
                        ) || '';

                    const url =
                        canonicalizeUrl(
                            content,
                            baseUrl
                        );

                    if (
                        url &&
                        /url|image|video|audio|icon|manifest|canonical/i
                            .test(property)
                    ) {
                        this.addReference(
                            references,
                            url,
                            'metadata',
                            {
                                property
                            }
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
                        String(
                            element.getAttribute(
                                'rel'
                            ) || ''
                        ).toLowerCase();

                    if (
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
                        )
                    ) {
                        const url =
                            canonicalizeUrl(
                                element.getAttribute(
                                    'href'
                                ),
                                baseUrl
                            );

                        this.addReference(
                            references,
                            url,
                            this.classifyLink(
                                element
                            ),
                            {
                                relation:
                                    rel
                            }
                        );
                    }
                }
            }

            if (
                CONFIG.discoverFromText
            ) {
                for (
                    const url of
                    extractUrlsFromText(
                        observation.body,
                        baseUrl
                    )
                ) {
                    this.addReference(
                        references,
                        url,
                        'embedded'
                    );
                }
            }

            const refresh =
                doc.querySelector(
                    'meta[http-equiv="refresh"][content]'
                );

            if (refresh) {
                const match =
                    refresh.getAttribute(
                        'content'
                    )?.match(
                        /url\s*=\s*(.+)$/i
                    );

                if (match) {
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

                    this.addReference(
                        references,
                        url,
                        'url',
                        {
                            relation:
                                'meta-refresh'
                        }
                    );
                }
            }

            const seen =
                new Set();

            const deduped = [];

            for (
                const reference of
                references
            ) {
                const key =
                    [
                        reference.type,
                        reference.url,
                        reference.relation ||
                            '',
                        reference.tag ||
                            ''
                    ].join('|');

                if (
                    seen.has(key)
                ) {
                    continue;
                }

                seen.add(key);
                deduped.push(
                    reference
                );
            }

            return [
                new Discovery({
                    candidateId:
                        candidate.id,

                    observationId:
                        observation.id,

                    kind:
                        'html-document',

                    confidence:
                        0.96,

                    mechanism:
                        'html-parser',

                    data: {
                        url:
                            candidate.target,

                        finalUrl:
                            fetchedUrl,

                        baseUrl,

                        title:
                            doc.querySelector(
                                'title'
                            )
                                ?.textContent
                                ?.trim()
                                ?.slice(
                                    0,
                                    CONFIG.maxStoredTextPreview
                                ) || '',

                        references:
                            deduped,

                        referenceCount:
                            deduped.length
                    },

                    provenance: {
                        origin:
                            candidate.origin,

                        parent:
                            candidate.parent,

                        candidateTarget:
                            candidate.target,

                        candidateType:
                            candidate.type,

                        depth:
                            candidate.depth
                    }
                })
            ];
        }

        candidates(discovery) {
            return safeArray(
                discovery.data.references
            ).map(
                reference =>
                    new Candidate({
                        target:
                            reference.url,

                        type:
                            reference.type,

                        origin:
                            `html:${reference.tag || 'document'}:${reference.attribute || 'unknown'}`,

                        parent:
                            discovery.id,

                        priority:
                            CONFIG.typePriority[
                                reference.type
                            ] ??
                            0.45,

                        hints: {
                            confidence:
                                discovery.confidence,

                            relation:
                                reference.relation ||
                                '',

                            tag:
                                reference.tag ||
                                '',

                            attribute:
                                reference.attribute ||
                                '',

                            method:
                                reference.method ||
                                null
                        },

                        depth:
                            discovery.provenance
                                .depth + 1
                    })
            );
        }
    }
