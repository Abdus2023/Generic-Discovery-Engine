    class TextProvider
        extends ResponseProvider {

        matches(observation) {
            const type =
                normalizeContentType(
                    observation.http
                        .contentType
                );

            return (
                type.startsWith(
                    'text/'
                ) ||
                type ===
                    'application/javascript' ||
                type ===
                    'application/x-javascript' ||
                type === ''
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

            return new Discovery({
                candidate,
                observation,

                kind:
                    'text-document',

                confidence:
                    0.75,

                data: {
                    url:
                        candidate.target,

                    finalUrl:
                        baseUrl,

                    textLength:
                        text.length,

                    urls:
                        unique(urls),

                    cssUrls:
                        unique(cssUrls)
                }
            });
        }

        candidates(discovery) {
            const depth =
                (
                    discovery
                        .provenance
                        .depth ||
                    0
                ) + 1;

            const result = [];

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
                        0.45,
                        depth
                    )
                );
            }

            return result;
        }
    }
