class RequestBudget {
    constructor(maxRequests = Infinity) {
        this.maxRequests = maxRequests;
        this.used = 0;
    }

    available() {
        return this.used < this.maxRequests;
    }

    reserve() {
        if (!this.available()) {
            return false;
        }

        this.used++;
        return true;
    }

    remaining() {
        return Math.max(
            0,
            this.maxRequests - this.used
        );
    }

    serialize() {
        return {
            maxRequests: this.maxRequests,
            used: this.used,
            remaining: this.remaining()
        };
    }
}
