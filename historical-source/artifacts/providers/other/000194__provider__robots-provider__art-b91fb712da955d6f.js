    class RobotsProvider
        extends ResponseProvider {

        score(observation) {
            const type =
                normalizeContentType(
                    observation.http
                        .contentType
                );

            const target =
                observation.target
                    .toLowerCase();

            const body =
                observation.body ||
                '';

            if (
                target.endsWith(
                    '/robots.txt'
                )
            ) {
                return 1;
            }

            if (
                type.startsWith(
                    'text/plain'
                ) &&
                /^\s*(user-agent|sitemap|allow|disallow)\s*:/im.test(
                    body
                )
            ) {
                return 0.95;
            }

            return 0;
        }

        recognize(
            candidate,
            observation
        ) {
            if (
                this.score(
                    observation
                ) <= 0
            ) {
                return null;
            }

            const body =
                observation.body ||
                '';

            const baseUrl =
                observation.http
                    .finalUrl ||
                candidate.target;

            const sitemaps =
                [];

            const urls =
                [];

            for (
                const line of
                body.split(/\r?\n/)
            ) {
                const match =
                    line.match(
                        /^\s*Sitemap\s*:\s*(\S+)/i
                    );

                if (
                    !match
                ) {
                    continue;
                }

                const url =
                    canonicalizeUrl(
                        match[1],
                        baseUrl
                    );

                if (
                    url &&
                    isAllowedUrl(
                        url
                    )
                ) {
                    sitemaps.push(
                        url
                    );

                    urls.push(
                        url
                    );
                }
            }

            /*
             * Extract absolute HTTP URLs appearing elsewhere in robots.txt.
             */
            urls.push(
                ...extractUrlsFromText(
                    body,
                    baseUrl
                )
            );

            return new Discovery({
                candidate,
                observation,

                kind:
                    'robots-txt',

                confidence:
                    0.99,

                data: {
                    url:
                        candidate.target,

                    finalUrl:
                        baseUrl,

                    sitemaps:
                        unique(
                            sitemaps
                        ),

                    urls:
                        unique(
                            urls
                        ).slice(
                            0,
                            CONFIG.maxUrlsPerDiscovery
                        )
                }
            });
        }

        candidates(
            discovery
        ) {
            const depth =
                (
                    discovery
                        .provenance
                        .depth ||
                    0
                ) + 1;

            return (
                discovery.data.urls ||
                []
            ).map(
                url =>
                    makeDerivedCandidate(
                        url,
                        'sitemap',
                        discovery,
                        0.9,
                        depth
                    )
            );
        }
    }
