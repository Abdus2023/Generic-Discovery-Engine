class HtmlRecognizer {

    recognize(candidate, observation) {

        if (
            observation.status !== 'acquired' ||
            !observation.features.body
        ) {
            return null;
        }

        const body = observation.features.body;

        const contentType =
            observation.http.contentType || '';

        const looksLikeHtml =
            contentType.includes('text/html') ||
            /<html[\s>]/i.test(body) ||
            /<body[\s>]/i.test(body);

        if (!looksLikeHtml) {
            return null;
        }

        const document =
            new DOMParser().parseFromString(
                body,
                'text/html'
            );

        const title =
            document.querySelector('title')
                ?.textContent
                ?.trim() || '';

        const links = [
            ...document.querySelectorAll(
                'a[href]'
            )
        ]
            .map(a =>
                canonicalizeUrl(a.href)
            )
            .filter(Boolean)
            .filter(isAllowedUrl);

        const resources = [
            ...document.querySelectorAll(
                'script[src],link[href],img[src]'
            )
        ]
            .map(el =>
                el.src ||
                el.href ||
                null
            )
            .filter(Boolean)
            .map(canonicalizeUrl)
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
}
