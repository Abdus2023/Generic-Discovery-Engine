    class JsonProvider extends ResponseProvider {

        matches(observation) {
            const type =
                observation.http.contentType || '';

            return (
                isJsonContentType(type) ||
                normalizeContentType(type) ===
                    'application/ld+json'
            );
        }

        recognize(candidate, observation) {
            if (!this.matches(observation)) {
                return null;
            }

            let value;

            try {
                value = JSON.parse(
                    observation.body || ''
                );
            } catch {
                return null;
            }

            const urls =
                this.extractUrls(
                    value,
                    observation.http.finalUrl ||
                        candidate.target
                );

            return new Discovery({
                candidate,
                observation,

                kind: 'json-document',

                confidence: 0.95,

                data: {
                    url: candidate.target,

                    finalUrl:
                        observation.http.finalUrl ||
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
                    /*
                     * First attempt to interpret the complete string
                     * as a URL.
                     */
                    const direct =
                        canonicalizeUrl(
                            value,
                            baseUrl
                        );

                    if (
                        direct &&
                        isAllowedUrl(direct)
                    ) {
                        result.push(direct);
                    }

                    /*
                     * Then look for URLs embedded in larger strings.
                     */
                    const embedded =
                        extractUrlsFromText(
                            value,
                            baseUrl
                        );

                    result.push(
                        ...embedded
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
            return (
                discovery.data.urls || []
            ).map(url =>
                new Candidate({
                    target: url,
                    type: 'url',
                    origin:
                        `json:${discovery.id}`,
                    parent:
                        discovery.id,
                    priority: 0.7
                })
            );
        }
    }
