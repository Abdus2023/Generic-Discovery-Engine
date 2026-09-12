    class JavaScriptProvider
        extends ResponseProvider {

        matches(observation) {
            return isJavaScriptContentType(
                observation
                    .http
                    .contentType
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

            const baseUrl =
                observation
                    .http
                    .finalUrl ||
                candidate.target;

            const text =
                observation.body ||
                '';

            const urls =
                extractUrlsFromText(
                    text,
                    baseUrl
                );

            const sourceMapUrls =
                this.extractSourceMaps(
                    text,
                    baseUrl
                );

            return new Discovery({
                candidate,
                observation,
                kind:
                    'javascript-document',
                confidence: 0.84,
                mechanism:
                    'javascript-text-parser',
                data: {
                    url:
                        candidate.target,

                    finalUrl:
                        baseUrl,

                    textLength:
                        text.length,

                    urls:
                        unique(
                            [
                                ...urls,
                                ...sourceMapUrls
                            ]
                        )
                }
            });
        }

        extractSourceMaps(
            text,
            baseUrl
        ) {
            const result = [];

            const regex =
                /[#@]\s*sourceMappingURL\s*=\s*([^\s]+)/gi;

            let match;

            while (
                (match =
                    regex.exec(text)) !==
                null
            ) {
                const url =
                    canonicalizeUrl(
                        match[1],
                        baseUrl
                    );

                if (
                    url &&
                    isAllowedUrl(url)
                ) {
                    result.push(
                        url
                    );
                }
            }

            return unique(
                result
            );
        }

        candidates(discovery) {
            const depth =
                (
                    discovery
                        .provenance
                        .depth || 0
                ) + 1;

            return (
                discovery.data.urls ||
                []
            ).map(url =>
                new Candidate({
                    target: url,
                    type:
                        url.endsWith(
                            '.map'
                        )
                            ? 'source-map'
                            : 'url',
                    origin:
                        `javascript:${discovery.id}`,
                    parent:
                        discovery.id,
                    priority:
                        url.endsWith(
                            '.map'
                        )
                            ? 0.6
                            : 0.38,
                    depth
                })
            );
        }
    }
