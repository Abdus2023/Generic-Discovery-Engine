    class NetworkEvent {
        constructor(data = {}) {
            this.id = makeId('network');

            this.requestId = data.requestId || null;
            this.api = data.api || 'unknown';

            this.method = data.method
                ? String(data.method).toUpperCase()
                : null;

            this.url = data.url || null;
            this.finalUrl = data.finalUrl || null;

            this.status = data.status ?? null;
            this.contentType = normalizeContentType(
                data.contentType || ''
            );

            this.initiatorType = data.initiatorType || null;

            this.requestAt = data.requestAt || now();
            this.responseAt = data.responseAt || null;

            this.duration = data.duration ?? null;

            this.phase = data.phase || 'unknown';
            this.error = data.error || null;
        }
    }
