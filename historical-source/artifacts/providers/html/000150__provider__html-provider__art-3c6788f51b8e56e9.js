    class HtmlProvider extends ResponseProvider {

        matches(observation) {
            const type =
                observation.http.contentType || '';

            const body =
                observation.body || '';

            return (
                isHtmlContentType(type) ||
                looksLikeHtml(body)
            );
        }

        recognize(candidate, observation) {
            if (!this.matches(observation)) {
                return null;
            }

            const body =
                observation.body || '';

            const doc =
                new DOMParser()
                    .parseFromString(
                        body,
                        'text/html'
                    );

            /*
             * IMPORTANT:
             *
             * DOMParser creates a document whose base URL may not be
             * the URL from which the document was acquired.
             *
             * We therefore resolve every raw attribute explicitly
             * against the acquired document URL.
             */
            const baseUrl =
                observation.http.finalUrl ||
                candidate.target;

            const title =
                doc.querySelector('title')
                    ?.textContent
                    ?.trim() || '';

            const links = [];

            if (CONFIG.discoverLinks) {
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
                    'input[src]'
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
                        resources.push(url);
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
                    const raw =
                        form.getAttribute(
                            'action'
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
                        forms.push(url);
                    }
                }
            }

            const metadata = [];

            if (CONFIG.discoverMetadata) {
                /*
                 * Canonical URL.
                 */
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
                 * OpenGraph URL.
                 */
                for (
                    const element of
                    doc.querySelectorAll(
                        'meta[property="og:url"][content]'
                    )
                ) {
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
                 * Meta refresh.
                 */
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
             * Extract URLs from inline HTML/attributes as a secondary
             * discovery signal.
             */
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

                kind: 'html-document',

                confidence: 0.95,

                data: {
                    url: candidate.target,

                    finalUrl: baseUrl,

                    title,

                    links: unique(links),

                    resources:
                        unique(resources),

                    forms: unique(forms),

                    metadata:
                        unique(metadata),

                    embeddedUrls:
                        unique(embeddedUrls)
                }
            });
        }

        candidates(discovery) {
            const result = [];

            if (CONFIG.discoverLinks) {
                for (
                    const url of
                    discovery.data.links || []
                ) {
                    result.push(
                        new Candidate({
                            target: url,
                            type: 'url',
                            origin:
                                `html:${discovery.id}`,
                            parent:
                                discovery.id,
                            priority: 0.8
                        })
                    );
                }
            }

            if (CONFIG.discoverResources) {
                for (
                    const url of
                    discovery.data.resources || []
                ) {
                    result.push(
                        new Candidate({
                            target: url,
                            type: 'resource',
                            origin:
                                `html:${discovery.id}`,
                            parent:
                                discovery.id,
                            priority: 0.5
                        })
                    );
                }
            }

            if (CONFIG.discoverForms) {
                for (
                    const url of
                    discovery.data.forms || []
                ) {
                    result.push(
                        new Candidate({
                            target: url,
                            type: 'form',
                            origin:
                                `html:${discovery.id}`,
                            parent:
                                discovery.id,
                            priority: 0.6
                        })
                    );
                }
            }

            if (CONFIG.discoverMetadata) {
                for (
                    const url of
                    discovery.data.metadata || []
                ) {
                    result.push(
                        new Candidate({
                            target: url,
                            type: 'metadata',
                            origin:
                                `html:${discovery.id}`,
                            parent:
                                discovery.id,
                            priority: 0.7
                        })
                    );
                }
            }

            if (CONFIG.discoverFromText) {
                for (
                    const url of
                    discovery.data.embeddedUrls || []
                ) {
                    result.push(
                        new Candidate({
                            target: url,
                            type: 'embedded-url',
                            origin:
                                `html:${discovery.id}`,
                            parent:
                                discovery.id,
                            priority: 0.4
                        })
                    );
                }
            }

            return result;
        }
    }
