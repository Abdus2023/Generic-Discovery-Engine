class CandidateExtractor {

    fromDocument(document, origin = 'dom') {

        const result = [];

        if (CONFIG.discoverLinks) {

            for (const element of
                document.querySelectorAll(
                    'a[href]'
                )) {

                const url =
                    canonicalizeUrl(
                        element.href
                    );

                if (!isAllowedUrl(url)) {
                    continue;
                }

                result.push(
                    new Candidate({
                        target: url,
                        type: 'url',
                        origin,
                        priority: 0.6
                    })
                );
            }
        }

        if (CONFIG.discoverResources) {

            for (const element of
                document.querySelectorAll(
                    'script[src],link[href],img[src]'
                )) {

                const url =
                    canonicalizeUrl(
                        element.src ||
                        element.href
                    );

                if (!isAllowedUrl(url)) {
                    continue;
                }

                result.push(
                    new Candidate({
                        target: url,
                        type: 'resource',
                        origin,
                        priority: 0.4
                    })
                );
            }
        }

        return result;
    }

    fromDiscovery(discovery) {

        const result = [];

        for (const url of
            discovery.data.links || []) {

            result.push(
                new Candidate({
                    target: url,
                    type: 'url',
                    origin: `discovery:${discovery.id}`,
                    priority: 0.8,
                    parent: discovery.id
                })
            );
        }

        for (const url of
            discovery.data.resources || []) {

            result.push(
                new Candidate({
                    target: url,
                    type: 'resource',
                    origin: `discovery:${discovery.id}`,
                    priority: 0.5,
                    parent: discovery.id
                })
            );
        }

        return result;
    }
}
