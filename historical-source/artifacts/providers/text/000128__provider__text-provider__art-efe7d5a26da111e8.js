class TextProvider extends ResponseProvider {

    matches(observation) {

        const type =
            observation.http.contentType ||
            '';

        return (
            type.startsWith('text/') ||
            type === ''
        );
    }

    recognize(candidate, observation) {

        if (!this.matches(observation)) {
            return null;
        }

        const text =
            observation.body || '';

        /*
         * Find absolute HTTP(S) URLs in text.
         */
        const matches =
            text.match(
                /https?:\/\/[^\s"'<>]+/gi
            ) || [];

        const urls =
            matches
                .map(canonicalizeUrl)
                .filter(Boolean)
                .filter(isAllowedUrl);

        return new Discovery({
            candidate,
            observation,

            kind: 'text-document',

            confidence: 0.75,

            data: {
                url: candidate.target,
                textLength: text.length,
                urls: [
                    ...new Set(urls)
                ]
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
