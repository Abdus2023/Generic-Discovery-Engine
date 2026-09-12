    class CssProvider
        extends Provider {

        matches(
            candidate,
            observation
        ) {
            return (
                isCss(
                    observation.http
                        .contentType
                ) ||
                candidate.type ===
                    'stylesheet'
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

            return [
                new Discovery({
                    candidate,
                    observation,
                    kind:
                        'css-document',
                    confidence:
                        0.94,
                    mechanism:
                        'css-parser',
                    data: {
                        url:
                            candidate.target,

                        finalUrl:
                            base,

                        urls:
                            extractCssUrls(
                                observation.body,
                                base
                            )
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
                        classifyUrl(
                            url
                        ),

                    origin:
                        'css-parser',

                    parent:
                        discovery.id,

                    depth,

                    priority:
                        0.40,

                    hints: {
                        confidence:
                            discovery.confidence
                    }
                })
            );
        }
    }
