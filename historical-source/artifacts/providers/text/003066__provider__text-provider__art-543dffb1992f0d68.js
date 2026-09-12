    class TextProvider
        extends Provider {

        matches(observation) {
            const type =
                observation.http
                    .contentType;

            return (
                String(type).startsWith(
                    'text/'
                ) &&
                !isHtml(type) &&
                !isCss(type) &&
                !isJs(type)
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

            return [
                new Discovery({
                    candidate,
                    observation,
                    kind:
                        'text-document',
                    confidence:
                        0.70,
                    mechanism:
                        'text-parser',
                    data: {
                        url:
                            candidate.target,

                        finalUrl:
                            base,

                        textLength:
                            text.length,

                        preview:
                            text.slice(
                                0,
                                CONFIG.maxTextPreview
                            ),

                        urls:
                            extractUrls(
                                text,
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
                    target: url,
                    type: 'resource',
                    origin:
                        'text-parser',
                    parent:
                        discovery.id,
                    depth,
                    priority: 0.34
                })
            );
        }
    }
