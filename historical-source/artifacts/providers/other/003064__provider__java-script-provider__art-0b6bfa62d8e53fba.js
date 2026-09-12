    class JavaScriptProvider
        extends Provider {

        matches(observation) {
            return isJs(
                observation.http
                    .contentType
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

            const text =
                observation.body ||
                '';

            const urls =
                extractUrls(
                    text,
                    base
                );

            const sourceMaps =
                [];

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
                        0.86,
                    mechanism:
                        'javascript-parser',
                    data: {
                        url:
                            candidate.target,

                        finalUrl:
                            base,

                        textLength:
                            text.length,

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
                    target: url,
                    type:
                        url.endsWith(
                            '.map'
                        )
                            ? 'source-map'
                            : 'resource',
                    origin:
                        'javascript-parser',
                    parent:
                        discovery.id,
                    depth,
                    priority:
                        url.endsWith(
                            '.map'
                        )
                            ? 0.58
                            : 0.37
                })
            );
        }
    }
