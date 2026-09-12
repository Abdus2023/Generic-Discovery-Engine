    class JsonProvider extends Provider {
        constructor() {
            super('json', true);
        }

        matches(candidate, observation) {
            return (
                isJsonContentType(
                    observation.http.contentType
                ) ||
                (
                    (
                        candidate.type === 'api' ||
                        candidate.type === 'manifest'
                    ) &&
                    looksLikeJson(observation.body)
                )
            );
        }

        recognize(candidate, observation) {
            let value = null;

            try {
                value =
                    JSON.parse(
                        observation.body
                    );
            } catch {
                return [];
            }

            const urls = [];

            const visit = node => {
                if (node === null || node === undefined) {
                    return;
                }

                if (typeof node === 'string') {
                    const url =
                        canonicalizeUrl(
                            node,
                            observation.http.finalUrl ||
                            candidate.target
                        );

                    if (
                        url &&
                        isAllowedUrl(url)
                    ) {
                        urls.push(url);
                    }

                    return;
                }

                if (Array.isArray(node)) {
                    for (const item of node) {
                        visit(item);
                    }

                    return;
                }

                if (typeof node === 'object') {
                    for (const key of Object.keys(node)) {
                        visit(node[key]);
                    }
                }
            };

            visit(value);

            const rootType =
                Array.isArray(value)
                    ? 'array'
                    : typeof value;

            const summary = {
                url: candidate.target,

                finalUrl:
                    observation.http.finalUrl,

                valueType: rootType,

                arrayLength:
                    Array.isArray(value)
                        ? value.length
                        : undefined,

                keys:
                    value &&
                    typeof value === 'object' &&
                    !Array.isArray(value)
                        ? Object.keys(value).slice(0, 100)
                        : undefined,

                urls: unique(urls)
            };

            return [
                new Discovery({
                    candidateId: candidate.id,
                    observationId: observation.id,
                    kind:
                        candidate.type === 'manifest'
                            ? 'web-manifest'
                            : 'json-document',

                    confidence:
                        candidate.type === 'manifest'
                            ? 0.98
                            : 0.93,

                    mechanism: 'json-parser',

                    data: summary,

                    provenance: {
                        origin: candidate.origin,
                        parent: candidate.parent,
                        candidateTarget: candidate.target,
                        candidateType: candidate.type,
                        depth: candidate.depth
                    }
                })
            ];
        }

        candidates(discovery) {
            return safeArray(
                discovery.data.urls
            ).map(url =>
                new Candidate({
                    target: url,
                    type: looksLikeApiUrl(url)
                        ? 'api'
                        : 'url',
                    origin: 'json-url',
                    parent: discovery.id,
                    priority:
                        looksLikeApiUrl(url)
                            ? 0.94
                            : 0.78,
                    hints: {
                        confidence:
                            discovery.confidence
                    },
                    depth:
                        discovery.provenance.depth + 1
                })
            );
        }
    }
