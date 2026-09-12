    class JsonProvider
        extends ResponseProvider {

        matches(observation) {
            const type =
                normalizeContentType(
                    observation.http
                        .contentType
                );

            return (
                type ===
                    'application/json' ||
                type.endsWith('+json') ||
                (
                    type === '' &&
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

            const urls =
                this.extractUrls(
                    value,
                    observation.http
                        .finalUrl ||
                        candidate.target
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
                        observation.http
                            .finalUrl ||
                        candidate.target,

                    value,

                    urls
                }
            });
        }

        extractUrls(
            value,
            baseUrl
        ) {
            const result = [];

            const visit = value => {
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
                    Object.values(value)
                ) {
                    visit(child);
                }
            };

            visit(value);

            return unique(result);
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
                    'url',
                    discovery,
                    0.7,
                    depth
                )
            );
        }
    }
