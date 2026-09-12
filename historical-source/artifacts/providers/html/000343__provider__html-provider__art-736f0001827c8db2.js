    class HtmlProvider extends Provider {
        constructor() {
            super('html');
            this.exclusive = true;
        }

        recognize(observation) {
            const type =
                observation.http.contentType || '';

            if (
                isHtmlContentType(type) ||
                looksLikeHtml(observation.body)
            ) {
                return {
                    recognized: true,
                    confidence: 0.98
                };
            }

            return {
                recognized: false,
                confidence: 0
            };
        }

        discover(observation) {
            const html = observation.body || '';

            if (!html) return [];

            const parser =
                new DOMParser();

            const doc =
                parser.parseFromString(
                    html,
                    'text/html'
                );

            const baseHref =
                doc.querySelector('base[href]')?.href ||
                observation.http.finalUrl ||
                observation.target;

            const discoveries = [];

            const add = (
                url,
                kind,
                mechanism,
                confidence,
                data = {}
            ) => {
                const canonical =
                    canonicalizeUrl(
                        url,
                        baseHref
                    );

                if (!canonical || !isAllowedUrl(canonical)) {
                    return;
                }

                discoveries.push(
                    new Discovery({
                        candidateId:
                            observation.candidateId,

                        observationId:
                            observation.id,

                        kind,
                        mechanism,
                        confidence,

                        data: {
                            ...data,
                            url: canonical
                        },

                        provenance: {
                            parent:
                                observation.http.finalUrl ||
                                observation.target,

                            candidateTarget:
                                observation.target,

                            candidateType:
                                'url',

                            mechanism,
                            depth: 0
                        }
                    })
                );
            };

            if (CONFIG.discovery.links) {
                for (
                    const element of
                    doc.querySelectorAll(
                        'a[href], area[href]'
                    )
                ) {
                    add(
                        element.getAttribute('href'),
                        'url',
                        'html-link',
                        0.85
                    );
                }
            }

            if (CONFIG.discovery.resources) {
                const selectors = [
                    ['script[src]', 'script', 'html-script'],
                    ['link[href]', 'resource', 'html-link'],
                    ['img[src]', 'media', 'html-image'],
                    ['audio[src]', 'media', 'html-audio'],
                    ['video[src]', 'media', 'html-video'],
                    ['source[src]', 'media', 'html-source'],
                    ['iframe[src]', 'frame', 'html-frame'],
                    ['frame[src]', 'frame', 'html-frame'],
                    ['object[data]', 'embedded', 'html-object'],
                    ['embed[src]', 'embedded', 'html-embed']
                ];

                for (
                    const [
                        selector,
                        type,
                        mechanism
                    ] of selectors
                ) {
                    for (
                        const element of
                        doc.querySelectorAll(selector)
                    ) {
                        const attribute =
                            element.hasAttribute('src')
                                ? 'src'
                                : element.hasAttribute('href')
                                    ? 'href'
                                    : 'data';

                        add(
                            element.getAttribute(attribute),
                            type,
                            mechanism,
                            0.78
                        );
                    }
                }

                for (
                    const element of
                    doc.querySelectorAll(
                        'link[rel]'
                    )
                ) {
                    const rel =
                        (element.getAttribute('rel') || '')
                            .toLowerCase();

                    const href =
                        element.getAttribute('href');

                    if (!href) continue;

                    if (
                        rel.includes('manifest')
                    ) {
                        add(
                            href,
                            'manifest',
                            'html-manifest',
                            0.96
                        );
                    }

                    if (
                        rel.includes('alternate') ||
                        rel.includes('feed')
                    ) {
                        add(
                            href,
                            'feed',
                            'html-feed',
                            0.88
                        );
                    }

                    if (
                        rel.includes('sitemap')
                    ) {
                        add(
                            href,
                            'sitemap',
                            'html-sitemap',
                            0.95
                        );
                    }

                    if (
                        rel.includes('preload') ||
                        rel.includes('prefetch') ||
                        rel.includes('modulepreload')
                    ) {
                        add(
                            href,
                            'resource',
                            `html-${rel.split(/\s+/)[0]}`,
                            0.62
                        );
                    }
                }
            }

            if (CONFIG.discovery.forms) {
                for (
                    const form of
                    doc.querySelectorAll('form[action]')
                ) {
                    add(
                        form.getAttribute('action'),
                        'form',
                        'html-form',
                        0.70,
                        {
                            method:
                                (
                                    form.getAttribute('method') ||
                                    'get'
                                ).toUpperCase()
                        }
                    );
                }
            }

            if (CONFIG.discovery.metadata) {
                for (
                    const element of
                    doc.querySelectorAll(
                        'link[rel="canonical"], meta[content]'
                    )
                ) {
                    const property =
                        element.getAttribute('property') ||
                        element.getAttribute('name') ||
                        element.getAttribute('rel') ||
                        '';

                    const value =
                        element.getAttribute('href') ||
                        element.getAttribute('content');

                    if (!value) continue;

                    if (
                        /url|canonical|og:url|twitter:url/i
                            .test(property)
                    ) {
                        add(
                            value,
                            'metadata',
                            'html-metadata',
                            0.82,
                            { property }
                        );
                    }
                }

                for (
                    const meta of
                    doc.querySelectorAll(
                        'meta[http-equiv="refresh"]'
                    )
                ) {
                    const content =
                        meta.getAttribute('content') || '';

                    const match =
                        content.match(
                            /url\s*=\s*(.+)$/i
                        );

                    if (match) {
                        add(
                            match[1].trim(),
                            'url',
                            'meta-refresh',
                            0.80
                        );
                    }
                }
            }

            const embeddedText =
                html.slice(
                    0,
                    CONFIG.fingerprintMaxChars
                );

            for (
                const url of
                extractUrlsFromText(
                    embeddedText,
                    baseHref
                )
            ) {
                add(
                    url,
                    'url',
                    'html-embedded-url',
                    0.52
                );
            }

            discoveries.push(
                new Discovery({
                    candidateId:
                        observation.candidateId,

                    observationId:
                        observation.id,

                    kind: 'html-document',
                    mechanism: 'html-parser',
                    confidence: 0.98,

                    data: {
                        references:
                            discoveries.map(
                                discovery =>
                                    discovery.data.url
                            )
                    },

                    provenance: {
                        parent:
                            observation.http.finalUrl ||
                            observation.target,

                        candidateTarget:
                            observation.target,

                        candidateType: 'url',
                        mechanism: 'html-parser',
                        depth: 0
                    }
                })
            );

            return discoveries;
        }
    }
