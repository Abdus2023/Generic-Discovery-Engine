    class ManifestProvider
        extends ResponseProvider {

        matches(observation) {
            const type =
                normalizeContentType(
                    observation.http
                        .contentType
                );

            return (
                type ===
                    'application/manifest+json'
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

            let value;

            try {
                value =
                    JSON.parse(
                        observation.body ||
                            ''
                    );
            } catch {
                return null;
            }

            const baseUrl =
                observation.http
                    .finalUrl ||
                candidate.target;

            const urls = [];

            const inspect =
                value => {
                    if (
                        typeof value ===
                        'string'
                    ) {
                        const url =
                            canonicalizeUrl(
                                value,
                                baseUrl
                            );

                        if (
                            url &&
                            isAllowedUrl(
                                url
                            )
                        ) {
                            urls.push(url);
                        }

                        return;
                    }

                    if (
                        !value ||
                        typeof value !==
                            'object'
                    ) {
                        return;
                    }

                    for (
                        const child of
                        Object.values(
                            value
                        )
                    ) {
                        inspect(child);
                    }
                };

            inspect(value);

            return new Discovery({
                candidate,
                observation,

                kind:
                    'web-manifest',

                confidence:
                    0.97,

                data: {
                    url:
                        candidate.target,

                    finalUrl:
                        baseUrl,

                    value,

                    urls:
                        unique(urls)
                }
            });
        }

        candidates(discovery) {
            const depth =
                (
                    discovery
                        .provenance
                        .depth ||
                    0
                ) + 1;

            return (
                discovery.data.urls ||
                []
            ).map(url =>
                makeDerivedCandidate(
                    url,
                    'manifest-resource',
                    discovery,
                    0.55,
                    depth
                )
            );
        }
    }
