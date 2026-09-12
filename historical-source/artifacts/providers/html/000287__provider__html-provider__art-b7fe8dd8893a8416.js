    class HtmlProvider extends Provider {
        constructor() {
            super('html', true);
        }

        matches(candidate, observation) {
            const type =
                observation.http.contentType;

            return (
                isHtmlContentType(type) ||
                (
                    !type &&
                    looksLikeHtml(observation.body)
                ) ||
                (
                    candidate.type === 'url' &&
                    looksLikeHtml(observation.body)
                )
            );
        }

        classifyLink(element) {
            const rel =
                String(
                    element.getAttribute('rel') || ''
                )
                .toLowerCase()
                .split(/\s+/)
                .filter(Boolean);

            const href =
                element.getAttribute('href');

            const type =
                String(
                    element.getAttribute('type') || ''
                ).toLowerCase();

            if (rel.includes('stylesheet')) {
                return 'stylesheet';
            }

            if (rel.includes('manifest')) {
                return 'manifest';
            }

            if (rel.includes('sitemap')) {
                return 'sitemap';
            }

            if (
                type.includes('rss') ||
                type.includes('atom') ||
                rel.includes('alternate')
            ) {
                return 'feed';
            }

            if (
                rel.includes('canonical') ||
                rel.includes('shortlink') ||
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

        addReference(references, url, type, meta = {}) {
            if (!url || !isAllowedUrl(url)) {
                return;
            }

            references.push({
                url,
                type,
                ...meta
            });
        }

        recognize(candidate, observation) {
            const parser =
                new DOMParser();

            const baseFetched =
                observation.http.finalUrl ||
                candidate.target;

            const doc =
                parser.parseFromString(
                    observation.body,
                    'text/html'
                );

            const baseElement =
                doc.querySelector('base[href]');

            const baseUrl =
                baseElement
                    ? canonicalizeUrl(
                        baseElement.getAttribute('href'),
                        baseFetched
                    ) || baseFetched
                    : baseFetched;

            const references = [];

            if (CONFIG.discoverLinks) {
                for (const element of doc.querySelectorAll(
                    'a[href], area[href]'
                )) {
                    const raw =
                        element.getAttribute('href');

                    const url =
                        canonicalizeUrl(
                            raw,
                            baseUrl
                        );

                    this.addReference(
                        references,
                        url,
                        'url',
                        {
                            relation:
                                element.getAttribute('rel') || '',
                            tag:
                                element.tagName.toLowerCase(),
                            attribute: 'href'
                        }
                    );
                }
            }

            if (CONFIG.discoverResources) {
                const selectors = [
                    {
                        selector: 'script[src]',
                        attribute: 'src',
                        type: 'script'
                    },
                    {
                        selector: 'link[href]',
                        attribute: 'href',
                        type: 'resource'
                    },
                    {
                        selector: 'img[src]',
                        attribute: 'src',
                        type: 'media'
                    },
                    {
                        selector: 'iframe[src], frame[src]',
                        attribute: 'src',
                        type: 'frame'
                    },
                    {
                        selector:
                            'video[src], audio[src], source[src], track[src]',
                        attribute: 'src',
                        type: 'media'
                    },
                    {
                        selector:
                            'object[data]',
                        attribute: 'data',
                        type: 'resource'
                    },
                    {
                        selector:
                            'embed[src]',
                        attribute: 'src',
                        type: 'resource'
                    }
                ];

                for (const group of selectors) {
                    for (const element of doc.querySelectorAll(
                        group.selector
                    )) {
                        const raw =
                            element.getAttribute(
                                group.attribute
                            );

                        const url =
                            canonicalizeUrl(
                                raw,
                                baseUrl
                            );

                        let type =
                            group.type;

                        if (
                            group.selector === 'link[href]'
                        ) {
                            type =
                                this.classifyLink(element);
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
                                    element.tagName.toLowerCase(),
                                attribute:
                                    group.attribute
                            }
                        );
                    }
                }

                for (const element of doc.querySelectorAll(
                    'img[srcset], source[srcset]'
                )) {
                    const srcset =
                        element.getAttribute('srcset');

                    for (const part of String(
                        srcset || ''
                    ).split(',')) {
                        const raw =
                            part.trim().split(/\s+/)[0];

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
                                    element.tagName.toLowerCase(),
                                attribute: 'srcset'
                            }
                        );
                    }
                }
            }

            if (CONFIG.discoverForms) {
                for (const form of doc.querySelectorAll(
                    'form[action]'
                )) {
                    const url =
                        canonicalizeUrl(
                            form.getAttribute('action'),
                            baseUrl
                        );

                    this.addReference(
                        references,
                        url,
                        'form',
                        {
                            tag: 'form',
                            attribute: 'action',
                            method:
                                (
                                    form.getAttribute(
                                        'method'
                                    ) || 'GET'
                                ).toUpperCase()
                        }
                    );
                }
            }

            if (CONFIG.discoverMetadata) {
                for (const element of doc.querySelectorAll(
                    'meta[content]'
                )) {
                    const property =
                        element.getAttribute('property') ||
                        element.getAttribute('name') ||
                        element.getAttribute('itemprop') ||
                        '';

                    const content =
                        element.getAttribute('content') ||
                        '';

                    const url =
                        canonicalizeUrl(
                            content,
                            baseUrl
                        );

                    if (
                        url &&
                        (
                            /url|image|video|audio|icon|manifest|canonical/i
                        ).test(property)
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

                for (const element of doc.querySelectorAll(
                    'link[rel][href]'
                )) {
                    const rel =
                        String(
                            element.getAttribute('rel') || ''
                        ).toLowerCase();

                    if (
                        rel.includes('canonical') ||
                        rel.includes('alternate') ||
                        rel.includes('manifest') ||
                        rel.includes('sitemap')
                    ) {
                        const url =
                            canonicalizeUrl(
                                element.getAttribute('href'),
                                baseUrl
                            );

                        this.addReference(
                            references,
                            url,
                            this.classifyLink(element),
                            {
                                relation: rel
                            }
                        );
                    }
                }
            }

            const embedded =
                CONFIG.discoverFromText
                    ? extractUrlsFromText(
                        observation.body,
                        baseUrl
                    )
                    : [];

            for (const url of embedded) {
                this.addReference(
                    references,
                    url,
                    'embedded'
                );
            }

            if (CONFIG.discoverWellKnown) {
                const manifest =
                    doc.querySelector(
                        'link[rel~="manifest"][href]'
                    );

                if (manifest) {
                    const url =
                        canonicalizeUrl(
                            manifest.getAttribute('href'),
                            baseUrl
                        );

                    this.addReference(
                        references,
                        url,
                        'manifest',
                        {
                            relation: 'manifest'
                        }
                    );
                }

                const refresh =
                    doc.querySelector(
                        'meta[http-equiv="refresh"][content]'
                    );

                if (refresh) {
                    const match =
                        refresh.getAttribute('content')
                            ?.match(
                                /url\s*=\s*(.+)$/i
                            );

                    if (match) {
                        const url =
                            canonicalizeUrl(
                                match[1].trim()
                                    .replace(/^['"]|['"]$/g, ''),
                                baseUrl
                            );

                        this.addReference(
                            references,
                            url,
                            'url',
                            {
                                relation: 'meta-refresh'
                            }
                        );
                    }
                }
            }

            const deduped = [];

            const seen = new Set();

            for (const reference of references) {
                const key =
                    `${reference.type}:${reference.url}:${reference.relation || ''}`;

                if (seen.has(key)) {
                    continue;
                }

                seen.add(key);
                deduped.push(reference);
            }

            return [
                new Discovery({
                    candidateId: candidate.id,
                    observationId: observation.id,
                    kind: 'html-document',
                    confidence: 0.96,
                    mechanism: 'html-parser',
                    data: {
                        url: candidate.target,
                        finalUrl: baseFetched,
                        baseUrl,
                        title:
                            doc.querySelector('title')
                                ?.textContent
                                ?.trim()
                                ?.slice(
                                    0,
                                    CONFIG.maxStoredTextPreview
                                ) || '',

                        references: deduped,

                        referenceCount:
                            deduped.length
                    },
                    provenance: {
                        origin: candidate.origin,
                        parent: candidate.parent,
                        candidateTarget: candidate.target,
                        candidateType: candidate.type,
                        depth: candidate.depth
                    }
                })
            ];
        }

        candidates(discovery) {
            const result = [];

            for (const reference of safeArray(
                discovery.data.references
            )) {
                if (!reference?.url) {
                    continue;
                }

                const basePriority =
                    CONFIG.typePriority[
                        reference.type
                    ] ??
                    CONFIG.typePriority.resource;

                result.push(
                    new Candidate({
                        target: reference.url,
                        type: reference.type,
                        origin:
                            `html:${reference.tag || 'document'}:${reference.attribute || 'unknown'}`,
                        parent: discovery.id,
                        priority: basePriority,
                        hints: {
                            confidence:
                                discovery.confidence,

                            relation:
                                reference.relation || '',

                            tag:
                                reference.tag || '',

                            attribute:
                                reference.attribute || ''
                        },
                        depth:
                            discovery.provenance.depth + 1
                    })
                );
            }

            return result;
        }
    }
