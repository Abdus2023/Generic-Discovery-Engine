    class JsonProvider
        extends ResponseProvider {

        score(observation) {
            const type =
                normalizeContentType(
                    observation.http
                        .contentType
                );

            if (
                type ===
                'application/json'
            ) {
                return 1;
            }

            if (
                type.endsWith(
                    '+json'
                )
            ) {
                return 0.98;
            }

            if (
                type === '' &&
                looksLikeJson(
                    observation.body
                )
            ) {
                return 0.82;
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
                this.extractUrls(
                    value,
                    baseUrl
                );

            /*
             * Do not persist the complete JSON object.
             */
            const summary =
                this.summarize(
                    value
                );

            return new Discovery({
                candidate,
                observation,

                kind:
                    'json-document',

                confidence:
                    0.95,

                data: {
                    url:
                        candidate.target,

                    finalUrl:
                        baseUrl,

                    summary,

                    urls
                }
            });
        }

        summarize(value) {
            if (
                Array.isArray(value)
            ) {
                return {
                    type:
                        'array',

                    length:
                        value.length
                };
            }

            if (
                value &&
                typeof value ===
                    'object'
            ) {
                return {
                    type:
                        'object',

                    keys:
                        Object.keys(
                            value
                        ).slice(
                            0,
                            100
                        )
                };
            }

            return {
                type:
                    typeof value
            };
        }

        extractUrls(
            value,
            baseUrl
        ) {
            const result = [];

            const visit =
                current => {
                    if (
                        typeof current ===
                        'string'
                    ) {
                        const direct =
                            canonicalizeUrl(
                                current,
                                baseUrl
                            );

                        if (
                            direct &&
                            isAllowedUrl(
                                direct
                            )
                        ) {
                            result.push(
                                direct
                            );
                        }

                        result.push(
                            ...extractUrlsFromText(
                                current,
                                baseUrl
                            )
                        );

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

                        if (
                            result.length >=
                            CONFIG.maxUrlsPerDiscovery
                        ) {
                            return;
                        }
                    }
                };

            visit(value);

            return unique(
                result
            ).slice(
                0,
                CONFIG.maxUrlsPerDiscovery
            );
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
                        'url',
                        discovery,
                        0.7,
                        depth
                    )
            );
        }
    }
