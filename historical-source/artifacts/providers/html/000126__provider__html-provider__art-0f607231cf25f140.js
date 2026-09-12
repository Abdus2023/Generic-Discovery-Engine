class HtmlProvider extends ResponseProvider {

    matches(observation) {

        const type =
            observation.http.contentType ||
            '';

        const body =
            observation.body || '';

        return (
            type.includes('text/html') ||
            /<html[\s>]/i.test(body) ||
            /<body[\s>]/i.test(body)
        );
    }

    recognize(candidate, observation) {

        if (!this.matches(observation)) {
            return null;
        }

        const body =
            observation.body || '';

        const doc =
            new DOMParser()
                .parseFromString(
                    body,
                    'text/html'
                );

        const title =
            doc.querySelector('title')
                ?.textContent
                ?.trim() || '';

        const links = [
            ...doc.querySelectorAll(
                'a[href]'
            )
        ]
            .map(element =>
                canonicalizeUrl(
                    element.href
                )
            )
            .filter(Boolean)
            .filter(isAllowedUrl);

        const resources = [
            ...doc.querySelectorAll(
                'script[src],' +
                'link[href],' +
                'img[src]'
            )
        ]
            .map(element =>
                canonicalizeUrl(
                    element.src ||
                    element.href
                )
            )
            .filter(Boolean)
            .filter(isAllowedUrl);

        return new Discovery({
            candidate,
            observation,

            kind: 'html-document',

            confidence: 0.95,

            data: {
                url: candidate.target,
                title,
                links,
                resources
            }
        });
    }

    candidates(discovery) {

        const result = [];

        if (CONFIG.discoverLinks) {

            for (
                const url of
                discovery.data.links || []
            ) {

                result.push(
                    new Candidate({
                        target: url,
                        type: 'url',
                        origin:
                            `html:${discovery.id}`,
                        parent:
                            discovery.id,
                        priority: 0.8
                    })
                );
            }
        }

        if (CONFIG.discoverResources) {

            for (
                const url of
                discovery.data.resources || []
            ) {

                result.push(
                    new Candidate({
                        target: url,
                        type: 'resource',
                        origin:
                            `html:${discovery.id}`,
                        parent:
                            discovery.id,
                        priority: 0.5
                    })
                );
            }
        }

        return result;
    }
}
