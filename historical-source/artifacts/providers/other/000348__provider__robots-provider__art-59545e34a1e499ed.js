    class RobotsProvider extends Provider {
        constructor() {
            super('robots');
            this.exclusive = true;
        }

        recognize(observation) {
            if (
                /robots\.txt([?#]|$)/i.test(
                    observation.target
                )
            ) {
                return {
                    recognized: true,
                    confidence: 0.99
                };
            }

            return {
                recognized: false,
                confidence: 0
            };
        }

        discover(observation) {
            const discoveries = [];

            const lines =
                String(observation.body || '')
                    .split(/\r?\n/);

            for (const line of lines) {
                const match =
                    line.match(
                        /^\s*Sitemap\s*:\s*(\S+)/i
                    );

                if (!match) continue;

                const url =
                    canonicalizeUrl(
                        match[1],
                        observation.target
                    );

                if (!url) continue;

                discoveries.push(
                    new Discovery({
                        candidateId:
                            observation.candidateId,

                        observationId:
                            observation.id,

                        kind: 'sitemap',
                        mechanism:
                            'robots-sitemap',

                        confidence: 0.99,

                        data: { url },

                        provenance: {
                            parent:
                                observation.target,

                            candidateTarget:
                                observation.target,

                            candidateType:
                                'robots',

                            mechanism:
                                'robots-sitemap',

                            depth: 0
                        }
                    })
                );
            }

            return discoveries;
        }
    }
