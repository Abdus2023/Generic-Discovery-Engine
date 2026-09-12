class StarvationDetector {
    constructor(limitMs = 30000) {
        this.limitMs = limitMs;
    }

    isStarved(work, nowMs = Date.now()) {
        if (work.status !== 'queued') {
            return false;
        }

        if (!work.queuedAt) {
            return false;
        }

        return (
            nowMs - work.queuedAt >=
            this.limitMs
        );
    }
}
