# HTML Provider

> **Status:** CURRENT
>
> **Source:** `Continue Architecture Planning.md`
>
> **Purpose:** The HTML response provider of the prototype, as implemented in the latest prototype script.

## Contents

- **HtmlProvider (v0.7.1)** — code extract from `Continue Architecture Planning.md` L51357–51675

## Related Documents

- [Providers Overview](overview.md)
- [JSON Provider](json.md)
- [Text Provider](text.md)
- [Prototype Overview](../prototype/overview.md)

---

<!-- extracted from Continue Architecture Planning.md L51357–51675 -->
### HtmlProvider (v0.7.1)

Extracted verbatim from `Continue Architecture Planning.md` lines 51357–51675. The complete script is preserved in [prototype/versions/14-v0.7.1.md](../prototype/versions/14-v0.7.1.md).

```
    class HtmlProvider extends Provider {
        constructor() {
            super('html');
        }

        matches(observation) {
            return looksLikeHtml(
                observation.http?.contentType,
                observation.body
            );
        }

        async recognize(candidate, observation) {
            const discoveries = [];

            let doc;

            try {
                const parser =
                    new DOMParser();

                doc =
                    parser.parseFromString(
                        observation.body,
                        'text/html'
                    );
            } catch {
                return discoveries;
            }

            const emit =
                (
                    url,
                    type,
                    mechanism,
                    confidence = 0.7,
                    hints = {}
                ) => {
                    if (!url) return;

                    const canonical =
                        canonicalizeUrl(
                            url
                        );

                    if (!canonical) return;

                    discoveries.push(
                        new Discovery({
                            candidateId:
                                candidate.id,

                            observationId:
                                observation.id,

                            kind: type,

                            confidence,

                            mechanism,

                            data: {
                                url: canonical
                            },

                            provenance: {
                                origin:
                                    candidate.origin,

                                parent:
                                    candidate.target,

                                candidateTarget:
                                    candidate.target,

                                candidateType:
                                    candidate.type,

                                mechanism,

                                depth:
                                    candidate.depth,

                                hints
                            }
                        })
                    );
                };

            for (
                const element of
                doc.querySelectorAll(
                    'a[href], area[href]'
                )
            ) {
                emit(
                    element.href,
                    'url',
                    'html-link',
                    0.85
                );
            }

            for (
                const element of
                doc.querySelectorAll(
                    'script[src]'
                )
            ) {
                emit(
                    element.src,
                    'script',
                    'html-script',
                    0.80
                );
            }

            for (
                const element of
                doc.querySelectorAll(
                    'link[href]'
                )
            ) {
                const rel =
                    String(
                        element.rel || ''
                    ).toLowerCase();

                let type =
                    'resource';

                if (
                    rel.includes('stylesheet')
                ) {
                    type = 'stylesheet';
                } else if (
                    rel.includes('manifest')
                ) {
                    type = 'manifest';
                } else if (
                    rel.includes('alternate')
                ) {
                    type = 'feed';
                } else if (
                    rel.includes('sitemap')
                ) {
                    type = 'sitemap';
                }

                emit(
                    element.href,
                    type,
                    `html-link-rel:${rel || 'none'}`,
                    0.75
                );
            }

            for (
                const element of
                doc.querySelectorAll(
                    'iframe[src], frame[src]'
                )
            ) {
                emit(
                    element.src,
                    'frame',
                    'html-frame',
                    0.65
                );
            }

            for (
                const element of
                doc.querySelectorAll(
                    'img[src], video[src], audio[src], source[src]'
                )
            ) {
                emit(
                    element.src,
                    'media',
                    'html-media',
                    0.50,
                    {
                        binary: true
                    }
                );
            }

            for (
                const element of
                doc.querySelectorAll(
                    'object[data], embed[src]'
                )
            ) {
                emit(
                    element.data ||
                    element.src,
                    'embedded',
                    'html-embedded',
                    0.45,
                    {
                        binary: true
                    }
                );
            }

            for (
                const element of
                doc.querySelectorAll(
                    'form[action]'
                )
            ) {
                emit(
                    element.action,
                    'form',
                    'html-form-action',
                    0.55,
                    {
                        method:
                            String(
                                element.method ||
                                'GET'
                            ).toUpperCase()
                    }
                );
            }

            const base =
                doc.querySelector(
                    'base[href]'
                );

            const baseHref =
                base?.href || null;

            for (
                const meta of
                doc.querySelectorAll(
                    'meta[content]'
                )
            ) {
                const httpEquiv =
                    String(
                        meta.httpEquiv || ''
                    ).toLowerCase();

                if (
                    httpEquiv ===
                    'refresh'
                ) {
                    const match =
                        meta.content.match(
                            /url\s*=\s*(.+)$/i
                        );

                    if (match) {
                        emit(
                            new URL(
                                match[1].trim(),
                                baseHref ||
                                    observation.requestedUrl
                            ).href,
                            'url',
                            'meta-refresh',
                            0.70
                        );
                    }
                }
            }

            for (
                const selector of [
                    'link[rel="canonical"]',
                    'meta[property="og:url"]',
                    'meta[name="twitter:url"]'
                ]
            ) {
                const element =
                    doc.querySelector(
                        selector
                    );

                const value =
                    element?.href ||
                    element?.content;

                if (value) {
                    emit(
                        value,
                        'metadata',
                        'metadata-url',
                        0.90
                    );
                }
            }

            const htmlText =
                doc.documentElement?.outerHTML ||
                observation.body;

            for (
                const raw of
                extractUrlsFromText(
                    htmlText
                )
            ) {
                emit(
                    raw,
                    looksLikeApiUrl(raw)
                        ? 'api'
                        : 'url',
                    'html-embedded-url',
                    0.45
                );
            }

            return discoveries;
        }
    }
```
