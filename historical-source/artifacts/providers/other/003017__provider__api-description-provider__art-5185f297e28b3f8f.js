    class ApiDescriptionProvider
        extends ResponseProvider {

        score(observation) {
            const type =
                normalizeContentType(
                    observation.http
                        .contentType
                );

            const body =
                observation.body ||
                '';

            if (
                !(
                    type ===
                        'application/json' ||
                    type.endsWith(
                        '+json'
                    ) ||
                    type === ''
                )
            ) {
                return 0;
            }

            if (
                /"openapi"\s*:/i.test(
                    body
                )
            ) {
                return 1;
            }

            if (
                /"swagger"\s*:/i.test(
                    body
                )
            ) {
                return 0.98;
            }

            return 0;
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

            /*
             * servers[].url
             */
            for (
                const server of
                value.servers ||
                []
            ) {
                const url =
                    canonicalizeUrl(
                        server?.url,
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
            }

            /*
             * OpenAPI 2 host/basePath.
             */
            if (
                value.host
            ) {
                const scheme =
                    value.schemes?.[0] ||
                    new URL(
                        baseUrl
                    ).protocol
                        .replace(
                            ':',
                            ''
                        );

                const base =
                    `${scheme}://${value.host}` +
                    (
                        value.basePath ||
                        '/'
                    );

                const url =
                    canonicalizeUrl(
                        base,
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
            }

            /*
             * External documentation and referenced schemas.
             */
            const references =
                extractJsonReferences(
                    value,
                    baseUrl
                );

            urls.push(
                ...references
            );

            return new Discovery({
                candidate,
                observation,

                kind:
                    'api-description',

                confidence:
                    0.99,

                data: {
                    url:
                        candidate.target,

                    finalUrl:
                        baseUrl,

                    specification:
                        value.openapi ||
                        value.swagger ||
                        null,

                    title:
                        value.info?.title ||
                        '',

                    pathCount:
                        value.paths
                            ? Object.keys(
                                  value.paths
                              ).length
                            : 0,

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
                        'api',
                        discovery,
                        0.85,
                        depth
                    )
            );
        }
    }
