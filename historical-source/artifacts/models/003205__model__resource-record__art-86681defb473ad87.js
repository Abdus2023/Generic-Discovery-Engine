    class ResourceRecord {
        constructor(data = {}) {
            this.url =
                data.url || '';

            this.types =
                safeArray(data.types);

            this.mechanisms =
                safeArray(data.mechanisms);

            this.parents =
                safeArray(data.parents);

            this.candidateIds =
                safeArray(data.candidateIds);

            this.observationIds =
                safeArray(data.observationIds);

            this.discoveryIds =
                safeArray(data.discoveryIds);

            this.networkEventIds =
                safeArray(data.networkEventIds);

            this.createdAt =
                data.createdAt || now();

            this.updatedAt =
                data.updatedAt || now();

            this.status =
                data.status || 'known';

            this.fingerprint =
                data.fingerprint || null;

            this.finalUrl =
                data.finalUrl || null;

            this.skipReason =
                data.skipReason || null;
        }

        merge(data = {}) {
            this.updatedAt = now();

            if (data.type) {
                this.types.push(data.type);
                this.types = unique(this.types);
            }

            if (data.mechanism) {
                this.mechanisms.push(data.mechanism);
                this.mechanisms =
                    unique(this.mechanisms);
            }

            for (const field of [
                'parents',
                'candidateIds',
                'observationIds',
                'discoveryIds',
                'networkEventIds'
            ]) {
                if (data[field]) {
                    this[field] = unique([
                        ...this[field],
                        ...data[field]
                    ]);
                }
            }

            if (data.status) {
                this.status = data.status;
            }

            if (data.fingerprint) {
                this.fingerprint =
                    data.fingerprint;
            }

            if (data.finalUrl) {
                this.finalUrl =
                    data.finalUrl;
            }

            if (data.skipReason) {
                this.skipReason =
                    data.skipReason;
            }
        }

        serialize() {
            return { ...this };
        }
    }
