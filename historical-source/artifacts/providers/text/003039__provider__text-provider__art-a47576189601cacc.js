    class TextProvider
        extends ResponseProvider {

        matches(observation) {
            const type =
                observation
                    .http
                    .contentType;

            /*
             * Unknown content types are accepted only when
             * the response looks textual. This avoids trying
             * to parse arbitrary binary content as text.
             */
            if (
                isTextContentType(
                    type
                )
            ) {
                return true;
            }

            if (
                !type &&
                observation.body
            ) {
                return (
                    !looksLikeHtml(
                        observation.body
                    ) &&
                    !looksLikeJson(
                        observation.body
                    )
                );
            }

            return false;
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
                observation
                    .http
                    .finalUrl ||
                candidate.target;

            const urls =
                CONFIG.discoverFromText
                    ? extractUrlsFromText(
                          text,
                          baseUrl
                      )
                    : [];

            return new Discovery({
                candidate,
                observation,
                kind:
                    'text-document',
                confidence: 0.72,
                mechanism:
                    'text-url-parser',
                data: {
                    url:
                        candidate.target,

                    finalUrl:
                        baseUrl,

                    textLength:
                        text.length,

                    textPreview:
                        text.slice(
                            0,
                            CONFIG.maxStoredTextPreview
                        ),

                    urls
                }
            });
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
                    type: 'url',
                    origin:
                        `text:${discovery.id}`,
                    parent:
                        discovery.id,
                    priority: 0.38,
                    depth
                })
            );
        }
    }
