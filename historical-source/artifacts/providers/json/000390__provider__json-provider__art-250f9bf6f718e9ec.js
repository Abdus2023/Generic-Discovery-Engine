    class JsonProvider extends Provider {
        constructor() {
            super('json');
        }

        matches(observation) {
            return looksLikeJson(
                observation.http?.contentType,
                observation.body
            );
        }

        async recognize(candidate, observation) {
            const discoveries = [];

            let parsed;

            try {
                parsed =
                    JSON.parse(
                        observation.body
                    );
            } catch {
                return discoveries;
            }

            const walk =
                (value, path = '$') => {
                    if (typeof value === 'string') {
                        const canonical =
                            canonicalizeUrl(
                                value
                            );

                        if (
                            canonical &&
                            isAllowedUrl(
                                canonical
                            )
                        ) {
                            discoveries.push(
                                new Discovery({
                                    candidateId:
                                        candidate.id,

                                    observationId:
                                        observation.id,

                                    kind:
                                        looksLikeApiUrl(
                                            canonical
                                        )
                                            ? 'api'
                                            : 'url',

                                    confidence:
                                        0.75,

                                    mechanism:
                                        'json-url',

                                    data: {
                                        url:
                                            canonical,
                                        path
                                    },

                                    provenance: {
                                        origin:
                                            candidate.origin,
                                        parent:
                                            candidate.target,
                                        candidateTarget:
                                            candidate.target,
                                        candidateType:
                                            candidate.type,
                                        mechanism:
                                            'json-url',
                                        depth:
                                            candidate.depth
                                    }
                                })
                            );
                        }

                        return;
                    }

                    if (
                        Array.isArray(value)
                    ) {
                        value.forEach(
                            (item, index) =>
                                walk(
                                    item,
                                    `${path}[${index}]`
                                )
                        );

                        return;
                    }

                    if (
                        value &&
                        typeof value ===
                            'object'
                    ) {
                        for (
                            const [
                                key,
                                child
                            ] of Object.entries(
                                value
                            )
                        ) {
                            walk(
                                child,
                                `${path}.${key}`
                            );
                        }
                    }
                };

            walk(parsed);

            return discoveries;
        }
    }
