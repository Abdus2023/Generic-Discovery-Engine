class EventMetadata {
    constructor(data = {}) {
        this.eventId = data.eventId;
        this.aggregateId = data.aggregateId;
        this.aggregateType = data.aggregateType;

        this.sequence = data.sequence ?? null;
        this.expectedVersion = data.expectedVersion ?? null;
        this.resultingVersion = data.resultingVersion ?? null;

        this.transactionId = data.transactionId || null;

        this.workerId = data.workerId || null;
        this.claimId = data.claimId || null;
        this.epoch = data.epoch ?? null;

        this.parentEventId = data.parentEventId || null;

        this.createdAt = data.createdAt || now();
    }
}
