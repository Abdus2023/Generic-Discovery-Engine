    class JavaScriptProvider
        extends Provider {

        matches(
            candidate,
            observation
        ) {
            return (
                isJavaScript(
                    observation.http
                        .contentType
                ) ||
                candidate.type ===
                    'script' ||
                /\.(m?js)$/i.test(
                    candidate.target
                )
            );
        }

        recognize(
            candidate,
            observation
        ) {
            const base =
                observation.http
                    .finalUrl ||
                candidate.target;

            const body =
                observation.body ||
                '';

            const urls =
                extractUrls(
                    body,
                    base
                );

            const sourceMaps =
                [];

            const regex =
                /[#@]\s*sourceMappingURL\s*=\s*([^\s]+)/gi;

            let match;

            while (
                (match =
                    regex.exec(body)) !==
                null
            ) {
                const url =
                    canonicalizeUrl(
                        match[1],
                        base
                    );

                if (
                    url &&
                    allowed(url)
                ) {
                    sourceMaps.push(
                        url
                    );
                }
            }

            return [
                new Discovery({
                    candidate,
                    observation,
                    kind:
                        'javascript-document',
                    confidence:
                        0.88,
                    mechanism:
                        'javascript-parser',
                    data: {
                        url:
                            candidate.target,

                        finalUrl:
                            base,

                        textLength:
                            body.length,

                        urls:
                            unique([
                                ...urls,
                                ...sourceMaps
                            ])
                    }
                })
            ];
        }

        candidates(
            discovery
        ) {
            const depth =
                discovery
                    .provenance
                    .depth + 1;

            return (
                discovery.data.urls ||
                []
            ).map(url =>
                new Candidate({
                    target:
                        url,

                    type:
                        /\.map$/i.test(
                            url
                        )
                            ? 'source-map'
                            : classifyUrl(
                                  url
                              ),

                    origin:
                        'javascript-parser',

                    parent:
                        discovery.id,

                    depth,

                    priority:
                        /\.map$/i.test(
                            url
                        )
                            ? 0.53
                            : 0.34,

                    hints: {
                        confidence:
                            discovery.confidence
                    }
                })
            );
        }
    }
