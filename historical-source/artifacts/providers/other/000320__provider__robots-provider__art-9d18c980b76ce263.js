    class RobotsProvider
        extends Provider {

        constructor() {
            super(
                'robots',
                true
            );
        }

        matches(candidate) {
            try {
                const path =
                    new URL(
                        candidate.target
                    ).pathname
                        .toLowerCase();

                return (
                    candidate.type ===
                        'robots' ||
                    path.endsWith(
                        '/robots.txt'
                    )
                );
            } catch {
                return false;
            }
        }

        recognize(
            candidate,
            observation
        ) {
            const urls = [];

            for (
                const line of
                String(
                    observation.body ||
                    ''
                ).split(/\r?\n/)
            ) {
                const match =
                    line.match(
                        /^\s*sitemap\s*:\s*(\S+)/i
                    );

                if (!match) {
                    continue;
                }

                const url =
                    canonicalizeUrl(
                        match[1],
                        observation.http.finalUrl ||
                            candidate.target
                    );

                if (
                    url &&
                    isAllowedUrl(url)
                ) {
                    urls.push(url);
                }
            }

            return [
                new Discovery({
                    candidateId:
                        candidate.id,

                    observationId:
                        observation.id,

                    kind:
                        'robots-document',

                    confidence:
                        0.99,

                    mechanism:
                        'robots-parser',

                    data: {
                        url:
                            candidate.target,

                        finalUrl:
                            observation.http.finalUrl,

                        sitemaps:
                            unique(urls)
                    },

                    provenance: {
                        origin:
                            candidate.origin,

                        parent:
                            candidate.parent,

                        candidateTarget:
                            candidate.target,

                        candidateType:
                            candidate.type,

                        depth:
                            candidate.depth
                    }
                })
            ];
        }

        candidates(discovery) {
            return safeArray(
                discovery.data.sitemaps
            ).map(
                url =>
                    new Candidate({
                        target:
                            url,

                        type:
                            'sitemap',

                        origin:
                            'robots-sitemap',

                        parent:
                            discovery.id,

                        priority:
                            0.90,

                        hints: {
                            confidence:
                                discovery.confidence
                        },

                        depth:
                            discovery.provenance
                                .depth + 1
                    })
            );
        }
    }
