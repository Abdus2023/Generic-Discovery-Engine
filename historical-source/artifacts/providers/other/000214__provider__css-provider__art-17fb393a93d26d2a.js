    class CssProvider
        extends ResponseProvider {

        matches(observation) {
            return isCssContentType(
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

            const urls =
                extractCssUrls(
                    observation.body ||
                        '',
                    baseUrl
                );

            return new Discovery({
                candidate,
                observation,
                kind:
                    'css-document',
                confidence: 0.9,
                mechanism:
                    'css-parser',
                data: {
                    url:
                        candidate.target,

                    finalUrl:
                        baseUrl,

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
                    type: 'resource',
                    origin:
                        `css:${discovery.id}`,
                    parent:
                        discovery.id,
                    priority: 0.48,
                    depth
                })
            );
        }
    }
