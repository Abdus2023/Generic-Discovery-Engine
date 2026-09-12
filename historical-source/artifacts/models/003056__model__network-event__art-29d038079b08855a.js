    class NetworkEvent {
        constructor(data) {
            this.id =
                id('network');

            this.timestamp =
                now();

            this.url =
                data.url;

            this.api =
                data.api ||
                null;

            this.phase =
                data.phase ||
                null;

            this.method =
                data.method ||
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

            this.duration =
                data.duration ??
                null;

            this.error =
                data.error ||
                null;
        }
    }
