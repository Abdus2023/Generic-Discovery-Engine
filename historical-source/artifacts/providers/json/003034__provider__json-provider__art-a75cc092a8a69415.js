    class JsonProvider
        extends ResponseProvider {

        matches(observation) {
            const type =
                observation
                    .http
                    .contentType;

            return (
                isJsonContentType(
                    type
                ) ||
                normalizeContentType(
                    type
                ) ===
                    'application/ld+json' ||
                (
                    !type &&
                    looksLikeJson(
                        observation.body
                    )
                )
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
                observation
                    .http
                    .finalUrl ||
                candidate.target;

            const urls =
                this.extractUrls(
                    value,
                    baseUrl
                );

            let summary;

            if (
                Array.isArray(value)
            ) {
                summary = {
                    valueType:
                        'array',

                    arrayLength:
                        value.length
                };
            } else if (
                value &&
                typeof value ===
                    'object'
            ) {
                summary = {
                    valueType:
                        'object',

                    keys:
                        Object.keys(
                            value
                        ).slice(
                            0,
                            100
                        )
                };
            } else {
                summary = {
                    valueType:
                        typeof value
                };
            }

            /*
             * Do not store the complete JSON object.
             * API responses can contain large or sensitive data.
             */
            return new Discovery({
                candidate,
                observation,
                kind:
                    'json-document',
                confidence: 0.95,
                mechanism:
                    'json-parser',
                data: {
                    url:
                        candidate.target,

                    finalUrl:
                        baseUrl,

                    ...summary,

                    urls
                }
            });
        }

        extractUrls(
            value,
            baseUrl
        ) {
            const result = [];

            const visit =
                value => {
                    if (
                        typeof value ===
                        'string'
                    ) {
                        const direct =
                            canonicalizeUrl(
                                value,
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
                                value,
                                baseUrl
                            )
                        );

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
                        visit(child);
                    }
                };

            visit(value);

            return unique(
                result
            );
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
                    type: 'api',
                    origin:
                        `json:${discovery.id}`,
                    parent:
                        discovery.id,
                    priority: 0.72,
                    depth
                })
            );
        }
    }
