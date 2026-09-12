    class JavaScriptProvider extends Provider {
        constructor() {
            super('javascript');
            this.exclusive = true;
        }

        recognize(observation) {
            const type =
                observation.http.contentType || '';

            if (
                /javascript|ecmascript/i.test(type) ||
                /\.(?:js|mjs|cjs)([?#]|$)/i.test(
                    observation.target
                )
            ) {
                return {
                    recognized: true,
                    confidence: 0.93
                };
            }

            return {
                recognized: false,
                confidence: 0
            };
        }

        discover(observation) {
            const base =
                observation.http.finalUrl ||
                observation.target;

            const urls =
                extractUrlsFromText(
                    observation.body,
                    base
                );

            const discoveries =
                urls.map(url =>
                    new Discovery({
                        candidateId:
                            observation.candidateId,

                        observationId:
                            observation.id,

                        kind:
                            looksLikeApiUrl(url)
                                ? 'api'
                                : 'url',

                        mechanism:
                            'javascript-url-extraction',

                        confidence:
                            looksLikeApiUrl(url)
                                ? 0.82
                                : 0.50,

                        data: { url },

                        provenance: {
                            parent: base,
                            candidateTarget:
                                observation.target,

                            candidateType:
                                'script',

                            mechanism:
                                'javascript-url-extraction',

                            depth: 0
                        }
                    })
                );

            const sourceMap =
                observation.body.match(
                    /[#@]\s*sourceMappingURL\s*=\s*(\S+)/i
                );

            if (sourceMap) {
                const url =
                    canonicalizeUrl(
                        sourceMap[1],
                        base
                    );

                if (url) {
                    discoveries.push(
                        new Discovery({
                            candidateId:
                                observation.candidateId,

                            observationId:
                                observation.id,

                            kind: 'resource',
                            mechanism:
                                'javascript-sourcemap',

                            confidence: 0.74,

                            data: { url },

                            provenance: {
                                parent: base,
                                candidateTarget:
                                    observation.target,

                                candidateType:
                                    'script',

                                mechanism:
                                    'javascript-sourcemap',

                                depth: 0
                            }
                        })
                    );
                }
            }

            return discoveries;
        }
    }
