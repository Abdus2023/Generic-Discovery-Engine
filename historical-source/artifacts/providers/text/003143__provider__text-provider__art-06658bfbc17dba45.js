    class TextProvider
        extends Provider {

        constructor() {
            super(
                'text',
                true
            );
        }

        matches(
            candidate,
            observation
        ) {
            const type =
                observation.http.contentType;

            if (
                isHtmlContentType(type) ||
                isJsonContentType(type) ||
                isXmlContentType(type) ||
                isCssContentType(type) ||
                isJavaScriptContentType(type)
            ) {
                return false;
            }

            try {
                const path =
                    new URL(
                        candidate.target
                    ).pathname
                        .toLowerCase();

                if (
                    path.endsWith(
                        '/robots.txt'
                    )
                ) {
                    return false;
                }
            } catch {
                // Ignore.
            }

            return (
                isTextContentType(type) ||
                !!observation.body
            );
        }

        recognize(
            candidate,
            observation
        ) {
            const urls =
                extractUrlsFromText(
                    observation.body,
                    observation.http.finalUrl ||
                        candidate.target
                );

            return [
                new Discovery({
                    candidateId:
                        candidate.id,

                    observationId:
                        observation.id,

                    kind:
                        'text-document',

                    confidence:
                        0.55,

                    mechanism:
                        'text-url-parser',

                    data: {
                        url:
                            candidate.target,

                        finalUrl:
                            observation.http.finalUrl,

                        urls
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
                                : 'url',

                        origin:
                            'text-url',

                        parent:
                            discovery.id,

                        priority:
                            looksLikeApiUrl(
                                url
                            )
                                ? 0.90
                                : 0.65,

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
