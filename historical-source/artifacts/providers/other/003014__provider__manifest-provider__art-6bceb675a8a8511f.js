    class ManifestProvider
        extends ResponseProvider {

        score(observation) {
            const type =
                normalizeContentType(
                    observation.http
                        .contentType
                );

            return type ===
                'application/manifest+json'
                ? 1
                : 0;
        }

        recognize(
            candidate,
            observation
        ) {
            if (
                this.score(
                    observation
                ) <= 0
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

            const urls =
                [];

            const visit =
                current => {
                    if (
                        typeof current ===
                        'string'
                    ) {
                        const url =
                            canonicalizeUrl(
                                current,
                                baseUrl
                            );

                        if (
                            url &&
                            isAllowedUrl(
                                url
                            )
                        ) {
                            urls.push(
                                url
                            );
                        }

                        return;
                    }

                    if (
                        !current ||
                        typeof current !==
                            'object'
                    ) {
                        return;
                    }

                    for (
                        const child of
                        Object.values(
                            current
                        )
                    ) {
                        visit(
                            child
                        );
                    }
                };

            visit(value);

            return new Discovery({
                candidate,
                observation,

                kind:
                    'web-manifest',

                confidence:
                    0.98,

                data: {
                    url:
                        candidate.target,

                    finalUrl:
                        baseUrl,

                    name:
                        typeof value.name ===
                        'string'
                            ? value.name
                            : '',

                    startUrl:
                        canonicalizeUrl(
                            value.start_url,
                            baseUrl
                        ),

                    scope:
                        canonicalizeUrl(
                            value.scope,
                            baseUrl
                        ),

                    urls:
                        unique(
                            urls
                        ).slice(
                            0,
                            CONFIG.maxUrlsPerDiscovery
                        )
                }
            });
        }

        candidates(
            discovery
        ) {
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
            ).map(
                url =>
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
