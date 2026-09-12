class StateVersion {
    constructor(data = {}) {
        this.aggregateId = data.aggregateId || null;
        this.version = data.version ?? 0;
        this.lastEventId = data.lastEventId || null;
        this.updatedAt = data.updatedAt || now();
    }
}
