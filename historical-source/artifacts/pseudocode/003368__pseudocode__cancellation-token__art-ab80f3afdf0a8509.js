class CancellationToken {
    constructor() {
        this.cancelled = false;
        this.reason = null;
    }

    cancel(reason = 'cancelled') {
        this.cancelled = true;
        this.reason = reason;
    }

    throwIfCancelled() {
        if (this.cancelled) {
            throw new Error(this.reason);
        }
    }
}
