    class OriginController {
        constructor() {
            this.states = new Map();
        }

        state(origin) {
            if (!this.states.has(origin)) {
                this.states.set(origin, {
                    active: 0,
                    requests: 0,
                    lastRequestAt: 0
                });
            }

            return this.states.get(origin);
        }

        canReserve(origin) {
            const state =
                this.state(origin);

            if (
                state.requests >=
                CONFIG.origin.maxRequestsPerOrigin
            ) {
                return false;
            }

            if (
                state.active >=
                CONFIG.origin.maxConcurrentPerOrigin
            ) {
                return false;
            }

            return true;
        }

        async acquire(origin) {
            while (true) {
                const state =
                    this.state(origin);

                if (
                    state.requests >=
                    CONFIG.origin.maxRequestsPerOrigin
                ) {
                    return false;
                }

                if (
                    state.active <
                    CONFIG.origin.maxConcurrentPerOrigin
                ) {
                    const elapsed =
                        now() -
                        state.lastRequestAt;

                    const wait =
                        CONFIG.origin.minRequestInterval -
                        elapsed;

                    if (wait > 0) {
                        await sleep(wait);
                        continue;
                    }

                    state.active++;
                    state.requests++;
                    state.lastRequestAt = now();

                    return true;
                }

                await sleep(50);
            }
        }

        release(origin) {
            const state =
                this.state(origin);

            state.active =
                Math.max(0, state.active - 1);
        }
    }
