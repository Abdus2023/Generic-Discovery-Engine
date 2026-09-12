    class JavaScriptProvider
        extends Provider {

        constructor() {
            super(
                'javascript',
                true
            );
        }

        matches(
            candidate,
            observation
        ) {
            return (
                isJavaScriptContentType(
                    observation.http.contentType
                ) ||
                candidate.type ===
                    'script' ||
                /\.(?:js|mjs|cjs)(?:[?#]|$)/i.test(
                    candidate.target
                )
            );
        }

        recognize(
            candidate,
            observation
        ) {
            const base =
                observation.http.finalUrl ||
                candidate.target;

            const urls =
                extractUrlsFromText(
                    observation.body,
                    base
                );

            const sourceMap =
                observation.body
                    ?.match(
                        /\/\/[#@]\s*sourceMappingURL\s*=\s*(\S+)/i
                    )?.[1] ||
                null;

            if (sourceMap) {
                const sourceMapUrl =
                    canonicalizeUrl(
                        sourceMap,
                        base
                    );

                if (
                    sourceMapUrl &&
                    isAllowedUrl(
                        sourceMapUrl
                    )
                ) {
                    urls.push(
                        sourceMapUrl
                    );
                }
            }

            return [
                new Discovery({
                    candidateId:
                        candidate.id,

                    observationId:
                        observation.id,

                    kind:
                        'javascript-document',

                    confidence:
                        0.82,

                    mechanism:
                        'javascript-text-parser',

                    data: {
                        url:
                            candidate.target,

                        finalUrl:
                            observation.http.finalUrl,

                        urls:
                            unique(urls),

                        sourceMap:
                            sourceMap ||
                            null
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
                discovery.data.urls
            ).map(
                url =>
                    new Candidate({
                        target:
                            url,

                        type:
                            looksLikeApiUrl(
                                url
                            )
                                ? 'api'
                                : /\.js(?:[?#]|$)/i.test(
                                    url
                                )
                                    ? 'script'
                                    : 'url',

                        origin:
                            'javascript-url',

                        parent:
                            discovery.id,

                        priority:
                            looksLikeApiUrl(
                                url
                            )
                                ? 0.93
                                : 0.62,

                        hints: {
                            confidence:
                                discovery.confidence
                        },

                        depth:
                            discovery.provenance
                                .depth + 1
                    })
            );
        }
    }
