class OriginController {
    constructor(options = {}) {
        this.maxConcurrent =
            options.maxConcurrent ?? 2;

        this.minInterval =
            options.minInterval ?? 150;

        this.maxRequests =
            options.maxRequests ?? 50;

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
        const state = this.state(origin);

        return (
            state.active < this.maxConcurrent &&
            state.requests < this.maxRequests
        );
    }

    reserve(origin) {
        if (!this.canReserve(origin)) {
            return false;
        }

        const state = this.state(origin);

        state.active++;
        state.requests++;

        return true;
    }

    release(origin) {
        const state = this.state(origin);

        state.active = Math.max(
            0,
            state.active - 1
        );

        state.lastRequestAt = Date.now();
    }
}
