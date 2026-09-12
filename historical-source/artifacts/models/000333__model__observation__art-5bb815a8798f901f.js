    class Observation {
        constructor(data = {}) {
            this.id = data.id || makeId('obs');
            this.candidateId = data.candidateId || null;

            this.target = data.target || '';
            this.requestedUrl = data.requestedUrl || this.target;

            this.startedAt = data.startedAt || now();
            this.completedAt = data.completedAt || null;

            this.status = data.status || 'pending';
            this.reason = data.reason || null;

            this.signalPresent = Boolean(data.signalPresent);

            this.http = {
                status: data.http?.status ?? null,
                contentType: data.http?.contentType || '',
                contentLength: data.http?.contentLength ?? null,
                finalUrl: data.http?.finalUrl || this.target
            };

            this.body = data.body || '';

            this.errors = safeArray(data.errors);

            this.network = safeArray(data.network);

            this.fingerprint = data.fingerprint || null;
        }

        serialize(includeBody = false) {
            const result = {
                id: this.id,
                candidateId: this.candidateId,
                target: this.target,
                requestedUrl: this.requestedUrl,
                startedAt: this.startedAt,
                completedAt: this.completedAt,
                status: this.status,
                reason: this.reason,
                signalPresent: this.signalPresent,
                http: this.http,
                errors: this.errors,
                network: this.network,
                fingerprint: this.fingerprint
            };

            if (includeBody) {
                result.body = this.body;
            }

            return result;
        }
    }
