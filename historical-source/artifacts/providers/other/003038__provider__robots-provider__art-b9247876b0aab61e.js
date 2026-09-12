    class RobotsProvider
        extends ResponseProvider {

        matches(observation) {
            const target =
                observation.target ||
                '';

            return (
                /\/robots\.txt$/i.test(
                    target
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
                return null;
            }

            const text =
                observation.body ||
                '';

            const sitemaps = [];

            for (
                const line of
                text.split(/\r?\n/)
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
                        observation
                            .http
                            .finalUrl ||
                            candidate.target
                    );

                if (
                    url &&
                    isAllowedUrl(url)
                ) {
                    sitemaps.push(
                        url
                    );
                }
            }

            return new Discovery({
                candidate,
                observation,
                kind:
                    'robots-document',
                confidence: 0.98,
                mechanism:
                    'robots-parser',
                data: {
                    url:
                        candidate.target,

                    finalUrl:
                        observation
                            .http
                            .finalUrl ||
                        candidate.target,

                    sitemaps:
                        unique(
                            sitemaps
                        ),

                    lineCount:
                        text.split(
                            /\r?\n/
                        ).length
                }
            });
        }

        candidates(discovery) {
            const depth =
                (
                    discovery
                        .provenance
                        .depth || 0
                ) + 1;

            return (
                discovery.data.sitemaps ||
                []
            ).map(url =>
                new Candidate({
                    target: url,
                    type: 'sitemap',
                    origin:
                        `robots:${discovery.id}`,
                    parent:
                        discovery.id,
                    priority: 0.9,
                    depth
                })
            );
        }
    }
