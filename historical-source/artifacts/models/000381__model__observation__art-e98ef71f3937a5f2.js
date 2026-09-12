    class Observation {
        constructor(data = {}) {
            this.id =
                data.id || makeId('obs');

            this.candidateId =
                data.candidateId || null;

            this.planId =
                data.planId || null;

            this.target =
                data.target || '';

            this.requestedUrl =
                data.requestedUrl || this.target;

            this.startedAt =
                data.startedAt || now();

            this.completedAt =
                data.completedAt || null;

            this.status =
                data.status || 'unknown';

            this.reason =
                data.reason || null;

            this.signalPresent =
                Boolean(data.signalPresent);

            this.http =
                data.http || {
                    status: 0,
                    contentType: '',
                    contentLength: null,
                    finalUrl: this.requestedUrl
                };

            this.body =
                data.body || '';

            this.bodyTruncated =
                Boolean(data.bodyTruncated);

            this.errors =
                safeArray(data.errors);

            this.network =
                safeArray(data.network);

            this.fingerprint =
                data.fingerprint || null;
        }

        serialize() {
            return {
                id: this.id,
                candidateId: this.candidateId,
                planId: this.planId,
                target: this.target,
                requestedUrl: this.requestedUrl,
                startedAt: this.startedAt,
                completedAt: this.completedAt,
                status: this.status,
                reason: this.reason,
                signalPresent: this.signalPresent,
                http: this.http,
                bodyTruncated: this.bodyTruncated,
                errors: this.errors,
                network: this.network,
                fingerprint: this.fingerprint
            };
        }
    }
