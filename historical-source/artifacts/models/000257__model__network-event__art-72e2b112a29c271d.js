    class NetworkEvent {
        constructor(data = {}) {
            this.id =
                data.id ||
                makeId('network');

            this.requestId =
                data.requestId ||
                null;

            this.api =
                data.api ||
                null;

            this.phase =
                data.phase ||
                null;

            this.method =
                data.method ||
                null;

            this.url =
                data.url ||
                null;

            this.finalUrl =
                data.finalUrl ||
                null;

            this.status =
                data.status ??
                null;

            this.contentType =
                data.contentType ||
                '';

            this.initiatorType =
                data.initiatorType ||
                null;

            this.requestAt =
                data.requestAt ||
                null;

            this.responseAt =
                data.responseAt ||
                null;

            this.duration =
                data.duration ??
                null;

            this.error =
                data.error ||
                null;

            this.candidateCreated =
                Boolean(
                    data.candidateCreated
                );

            this.timestamp =
                data.timestamp ||
                now();
        }

        update(data) {
            if (
                data.api
            ) {
                this.api =
                    data.api;
            }

            if (
                data.method
            ) {
                this.method =
                    data.method;
            }

            if (
                data.url
            ) {
                this.url =
                    data.url;
            }

            if (
                data.finalUrl
            ) {
                this.finalUrl =
                    data.finalUrl;
            }

            if (
                data.status !==
                undefined
            ) {
                this.status =
                    data.status;
            }

            if (
                data.contentType !==
                undefined
            ) {
                this.contentType =
                    data.contentType;
            }

            if (
                data.initiatorType
            ) {
                this.initiatorType =
                    data.initiatorType;
            }

            if (
                data.phase ===
                'request'
            ) {
                this.requestAt =
                    data.timestamp ||
                    now();
            }

            if (
                data.phase ===
                'response' ||
                data.phase ===
                'error'
            ) {
                this.responseAt =
                    data.timestamp ||
                    now();

                if (
                    this.requestAt
                ) {
                    this.duration =
                        this.responseAt -
                        this.requestAt;
                }
            }

            if (
                data.error
            ) {
                this.error =
                    data.error;
            }

            this.phase =
                data.phase ||
                this.phase;

            this.timestamp =
                data.timestamp ||
                now();
        }
    }
