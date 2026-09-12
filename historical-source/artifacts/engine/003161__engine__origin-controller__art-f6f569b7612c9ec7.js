    class OriginController {
        constructor() {
            this.origins = new Map();
        }

        getState(url) {
            const origin = originOf(url);

            let state = this.origins.get(origin);

            if (!state) {
                state = {
                    origin,
                    requests: 0,
                    active: 0,
                    lastRequestAt: 0,
                    successes: 0,
                    failures: 0
                };

                this.origins.set(origin, state);
            }

            return state;
        }

        async acquire(url) {
            const state = this.getState(url);

            while (true) {
                if (
                    state.requests >=
                    CONFIG.origin.maxRequestsPerOrigin
                ) {
                    return false;
                }

                const elapsed =
                    now() - state.lastRequestAt;

                const waitForInterval =
                    Math.max(
                        0,
                        CONFIG.origin.minRequestInterval -
                        elapsed
                    );

                const available =
                    state.active <
                    CONFIG.origin.maxConcurrentPerOrigin;

                if (available && waitForInterval <= 0) {
                    state.active++;
                    state.requests++;
                    state.lastRequestAt = now();

                    return true;
                }

                await sleep(
                    Math.max(
                        25,
                        Math.min(
                            250,
                            waitForInterval || 50
                        )
                    )
                );

                if (engine.stopRequested) {
                    return false;
                }
            }
        }

        release(url, success) {
            const state = this.getState(url);

            state.active = Math.max(
                0,
                state.active - 1
            );

            if (success) {
                state.successes++;
            } else {
                state.failures++;
            }
        }

        snapshot() {
            return [...this.origins.values()]
                .map(state => ({ ...state }));
        }
    }
