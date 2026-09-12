    class TextProvider
        extends ResponseProvider {

        score(observation) {
            const type =
                normalizeContentType(
                    observation.http
                        .contentType
                );

            if (
                type.startsWith(
                    'text/'
                )
            ) {
                return 0.7;
            }

            if (
                type ===
                    'application/javascript' ||
                type ===
                    'application/x-javascript'
            ) {
                return 0.82;
            }

            /*
             * No Content-Type is treated conservatively.
             */
            if (
                type === '' &&
                !looksLikeHtml(
                    observation.body
                ) &&
                !looksLikeJson(
                    observation.body
                ) &&
                !looksLikeXml(
                    observation.body
                )
            ) {
                return 0.3;
            }

            return 0;
        }

        recognize(
            candidate,
            observation
        ) {
            const score =
                this.score(
                    observation
                );

            if (
                score <= 0
            ) {
                return null;
            }

            const text =
                observation.body ||
                '';

            const baseUrl =
                observation.http
                    .finalUrl ||
                candidate.target;

            const urls =
                extractUrlsFromText(
                    text,
                    baseUrl
                );

            const cssUrls =
                CONFIG.discoverCss
                    ? extractCssUrls(
                          text,
                          baseUrl
                      )
                    : [];

            const contentType =
                normalizeContentType(
                    observation.http
                        .contentType
                );

            const isCss =
                contentType ===
                    'text/css' ||
                /\.css(?:[?#]|$)/i.test(
                    candidate.target
                );

            return new Discovery({
                candidate,
                observation,

                kind:
                    isCss
                        ? 'stylesheet'
                        : 'text-document',

                confidence:
                    isCss
                        ? 0.92
                        : 0.72,

                data: {
                    url:
                        candidate.target,

                    finalUrl:
                        baseUrl,

                    contentType,

                    textLength:
                        text.length,

                    urls:
                        unique(
                            urls
                        ),

                    cssUrls:
                        unique(
                            cssUrls
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

            const result =
                [];

            for (
                const url of
                discovery.data.urls ||
                []
            ) {
                result.push(
                    makeDerivedCandidate(
                        url,
                        'url',
                        discovery,
                        0.4,
                        depth
                    )
                );
            }

            for (
                const url of
                discovery.data.cssUrls ||
                []
            ) {
                result.push(
                    makeDerivedCandidate(
                        url,
                        'stylesheet-url',
                        discovery,
                        0.48,
                        depth
                    )
                );
            }

            return result;
        }
    }
