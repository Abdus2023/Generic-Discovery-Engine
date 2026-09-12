    class OriginBudget {
        constructor() {
            this.records =
                new Map();
        }

        get(origin) {
            if (!origin) {
                return null;
            }

            let record =
                this.records.get(
                    origin
                );

            if (!record) {
                record = {
                    origin,

                    requests: 0,

                    active: 0,

                    lastRequestAt: 0,

                    successes: 0,

                    failures: 0
                };

                this.records.set(
                    origin,
                    record
                );
            }

            return record;
        }

        canRequest(origin) {
            const record =
                this.get(origin);

            if (!record) {
                return false;
            }

            if (
                record.requests >=
                CONFIG.maxRequestsPerOrigin
            ) {
                return false;
            }

            if (
                record.active >=
                CONFIG.maxConcurrentPerOrigin
            ) {
                return false;
            }

            return true;
        }

        remainingDelay(origin) {
            const record =
                this.get(origin);

            if (!record) {
                return 0;
            }

            const elapsed =
                now() -
                record.lastRequestAt;

            return Math.max(
                0,
                CONFIG.minRequestInterval -
                elapsed
            );
        }

        async acquireSlot(origin) {
            if (!origin) {
                return {
                    acquired: false,
                    reason: 'invalid-origin'
                };
            }

            const record =
                this.get(origin);

            if (
                record.requests >=
                CONFIG.maxRequestsPerOrigin
            ) {
                return {
                    acquired: false,
                    reason: 'origin-budget'
                };
            }

            while (
                record.active >=
                CONFIG.maxConcurrentPerOrigin
            ) {
                await sleep(25);
            }

            const delay =
                this.remainingDelay(
                    origin
                );

            if (delay > 0) {
                await sleep(delay);
            }

            if (
                record.requests >=
                CONFIG.maxRequestsPerOrigin
            ) {
                return {
                    acquired: false,
                    reason: 'origin-budget'
                };
            }

            record.requests++;
            record.active++;
            record.lastRequestAt =
                now();

            return {
                acquired: true,
                reason: null
            };
        }

        release(
            origin,
            success
        ) {
            const record =
                this.get(origin);

            if (!record) {
                return;
            }

            record.active =
                Math.max(
                    0,
                    record.active - 1
                );

            if (success) {
                record.successes++;
            } else {
                record.failures++;
            }
        }

        toJSON() {
            return [
                ...this.records.values()
            ].map(record => ({
                ...record
            }));
        }
    }
