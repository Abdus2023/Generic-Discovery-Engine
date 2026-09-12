    class TextProvider
        extends Provider {

        matches(
            candidate,
            observation
        ) {
            const type =
                observation.http
                    .contentType;

            if (
                candidate.type ===
                    'robots' ||
                isHtml(type) ||
                isJson(type) ||
                isXml(type) ||
                isCss(type) ||
                isJavaScript(type)
            ) {
                return false;
            }

            return isText(type);
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
                            body.length,

                        preview:
                            body.slice(
                                0,
                                CONFIG.maxTextPreview
                            ),

                        urls:
                            extractUrls(
                                body,
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
                        'text-parser',

                    parent:
                        discovery.id,

                    depth,

                    priority:
                        0.31,

                    hints: {
                        confidence:
                            discovery.confidence
                    }
                })
            );
        }
    }
