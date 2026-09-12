class StateMutation {
    constructor(data = {}) {
        this.aggregateId = data.aggregateId;
        this.expectedVersion = data.expectedVersion ?? 0;
        this.operation = data.operation;
        this.payload = data.payload || {};
        this.workerId = data.workerId || null;
        this.claimId = data.claimId || null;
        this.epoch = data.epoch ?? null;
        this.createdAt = data.createdAt || now();
    }
}
