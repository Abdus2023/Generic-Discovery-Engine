    class TextProvider extends ResponseProvider {

        matches(observation) {
            const type =
                observation.http.contentType || '';

            /*
             * Do not treat unknown binary responses as arbitrary text.
             *
             * An empty Content-Type is accepted because many simple
             * endpoints omit it.
             */
            return (
                isTextContentType(type) ||
                normalizeContentType(type) === ''
            );
        }

        recognize(candidate, observation) {
            if (!this.matches(observation)) {
                return null;
            }

            const text =
                observation.body || '';

            const urls =
                extractUrlsFromText(
                    text,
                    observation.http.finalUrl ||
                        candidate.target
                );

            return new Discovery({
                candidate,
                observation,

                kind: 'text-document',

                confidence: 0.75,

                data: {
                    url: candidate.target,

                    finalUrl:
                        observation.http.finalUrl ||
                        candidate.target,

                    textLength:
                        text.length,

                    urls
                }
            });
        }

        candidates(discovery) {
            return (
                discovery.data.urls || []
            ).map(url =>
                new Candidate({
                    target: url,
                    type: 'url',
                    origin:
                        `text:${discovery.id}`,
                    parent:
                        discovery.id,
                    priority: 0.4
                })
            );
        }
    }
