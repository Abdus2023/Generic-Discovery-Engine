    class JsonProvider
        extends Provider {

        matches(observation) {
            return (
                isJson(
                    observation.http
                        .contentType
                ) ||
                (
                    !observation.http
                        .contentType &&
                    looksJson(
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
                return [];
            }

            let value;

            try {
                value =
                    JSON.parse(
                        observation.body ||
                            ''
                    );
            } catch {
                return [];
            }

            const base =
                observation.http
                    .finalUrl ||
                candidate.target;

            const urls =
                [];

            const visit =
                value => {
                    if (
                        typeof value ===
                        'string'
                    ) {
                        const direct =
                            canonicalizeUrl(
                                value,
                                base
                            );

                        if (
                            direct &&
                            allowed(direct)
                        ) {
                            urls.push(
                                direct
                            );
                        }

                        urls.push(
                            ...extractUrls(
                                value,
                                base
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
                        const item of
                        Object.values(
                            value
                        )
                    ) {
                        visit(item);
                    }
                };

            visit(value);

            const summary =
                Array.isArray(value)
                    ? {
                          valueType:
                              'array',

                          arrayLength:
                              value.length
                      }
                    : value &&
                      typeof value ===
                          'object'
                    ? {
                          valueType:
                              'object',

                          keys:
                              Object.keys(
                                  value
                              ).slice(
                                  0,
                                  100
                              )
                      }
                    : {
                          valueType:
                              typeof value
                      };

            return [
                new Discovery({
                    candidate,
                    observation,
                    kind:
                        candidate.type ===
                        'manifest'
                            ? 'manifest-json'
                            : 'json-document',
                    confidence:
                        0.98,
                    mechanism:
                        'json-parser',
                    data: {
                        url:
                            candidate.target,

                        finalUrl:
                            base,

                        ...summary,

                        urls:
                            unique(
                                urls
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
                    target: url,
                    type: 'api',
                    origin:
                        'json-parser',
                    parent:
                        discovery.id,
                    depth,
                    priority: 0.74
                })
            );
        }
    }
