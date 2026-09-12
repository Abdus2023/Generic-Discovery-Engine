class JsonProvider extends ResponseProvider {

    matches(observation) {

        const type =
            observation.http.contentType ||
            '';

        return (
            type.includes(
                'application/json'
            ) ||
            type.includes(
                '+json'
            )
        );
    }

    recognize(candidate, observation) {

        if (!this.matches(observation)) {
            return null;
        }

        let value;

        try {

            value =
                JSON.parse(
                    observation.body
                );

        } catch {
            return null;
        }

        const urls =
            this.extractUrls(value);

        return new Discovery({
            candidate,
            observation,

            kind: 'json-document',

            confidence: 0.95,

            data: {
                url: candidate.target,
                value,
                urls
            }
        });
    }

    extractUrls(value) {

        const result = [];

        const visit = value => {

            if (typeof value === 'string') {

                const url =
                    canonicalizeUrl(
                        value
                    );

                if (
                    url &&
                    isAllowedUrl(url)
                ) {
                    result.push(url);
                }

                return;
            }

            if (!value || typeof value !== 'object') {
                return;
            }

            for (
                const child of
                Object.values(value)
            ) {
                visit(child);
            }
        };

        visit(value);

        return [
            ...new Set(result)
        ];
    }

    candidates(discovery) {

        return (
            discovery.data.urls || []
        ).map(url =>
            new Candidate({
                target: url,
                type: 'url',
                origin:
                    `json:${discovery.id}`,
                parent:
                    discovery.id,
                priority: 0.7
            })
        );
    }
}
