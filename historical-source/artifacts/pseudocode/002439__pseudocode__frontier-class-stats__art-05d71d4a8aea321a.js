class FrontierClassStats {
    constructor() {
        this.queued = 0;
        this.running = 0;
        this.completed = 0;

        this.waitTimeMs = 0;
        this.maxWaitTimeMs = 0;

        this.selected = 0;
        this.skipped = 0;

        this.starved = 0;
    }
}
