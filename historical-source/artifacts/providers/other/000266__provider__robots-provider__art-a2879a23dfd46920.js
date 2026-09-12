    class RobotsProvider
        extends Provider {

        matches(
            candidate
        ) {
            return (
                candidate.type ===
                    'robots' ||
                /\/robots\.txt$/i.test(
                    candidate.target
                )
            );
        }

        recognize(
            candidate,
            observation
        ) {
            const base =
                observation.http
                    .finalUrl ||
                candidate.target;

            const sitemaps =
                [];

            for (
                const line of
                String(
                    observation.body ||
                        ''
                ).split(
                    /\r?\n/
                )
            ) {
                const match =
                    line.match(
                        /^\s*Sitemap\s*:\s*(\S+)/i
                    );

                if (!match) {
                    continue;
                }

                const url =
                    canonicalizeUrl(
                        match[1],
                        base
                    );

                if (
                    url &&
                    allowed(url)
                ) {
                    sitemaps.push(
                        url
                    );
                }
            }

            return [
                new Discovery({
                    candidate,
                    observation,
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
                            base,

                        sitemaps:
                            unique(
                                sitemaps
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
                discovery.data.sitemaps ||
                []
            ).map(url =>
                new Candidate({
                    target:
                        url,

                    type:
                        'sitemap',

                    origin:
                        'robots-parser',

                    parent:
                        discovery.id,

                    depth,

                    priority:
                        0.92,

                    hints: {
                        confidence:
                            discovery.confidence
                    }
                })
            );
        }
    }
