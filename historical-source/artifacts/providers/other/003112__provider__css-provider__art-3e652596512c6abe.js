    class CssProvider extends Provider {
        constructor() {
            super('css', true);
        }

        matches(candidate, observation) {
            return (
                isCssContentType(
                    observation.http.contentType
                ) ||
                (
                    candidate.type === 'stylesheet' &&
                    !looksLikeHtml(observation.body)
                ) ||
                /\.css(?:[?#]|$)/i.test(
                    candidate.target
                )
            );
        }

        recognize(candidate, observation) {
            const base =
                observation.http.finalUrl ||
                candidate.target;

            const urls =
                extractCssUrls(
                    observation.body,
                    base
                );

            return [
                new Discovery({
                    candidateId: candidate.id,
                    observationId: observation.id,
                    kind: 'css-document',
                    confidence: 0.90,
                    mechanism: 'css-parser',
                    data: {
                        url: candidate.target,
                        finalUrl:
                            observation.http.finalUrl,
                        urls,
                        count: urls.length
                    },
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
                    type: /\.css(?:[?#]|$)/i.test(url)
                        ? 'stylesheet'
                        : 'media',
                    origin: 'css-url',
                    parent: discovery.id,
                    priority:
                        /\.css(?:[?#]|$)/i.test(url)
                            ? 0.52
                            : 0.25,
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
