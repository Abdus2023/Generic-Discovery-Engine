    class NetworkEvent {
        constructor(data = {}) {
            this.id =
                makeId('network');

            this.requestId =
                data.requestId || null;

            this.phase =
                data.phase ||
                data.event ||
                'unknown';

            this.api =
                data.api ||
                'unknown';

            this.method =
                data.method
                    ? normalizeMethod(
                        data.method
                    )
                    : null;

            this.url =
                canonicalizeUrl(
                    data.url
                ) ||
                data.url ||
                null;

            this.finalUrl =
                canonicalizeUrl(
                    data.finalUrl
                ) ||
                data.finalUrl ||
                null;

            this.status =
                data.status ??
                null;

            this.contentType =
                normalizeContentType(
                    data.contentType || ''
                );

            this.initiatorType =
                data.initiatorType ||
                null;

            this.requestAt =
                data.requestAt ||
                now();

            this.responseAt =
                data.responseAt ||
                null;

            this.duration =
                data.duration ??
                null;

            this.error =
                data.error ||
                null;
        }
    }
