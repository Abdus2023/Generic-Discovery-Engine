class EnumerationTermination {
    constructor(data = {}) {
        this.executionId = data.executionId || null;

        this.status = data.status || 'unknown';

        this.reason = data.reason || null;

        this.conditions = data.conditions || [];

        this.evidenceIds = data.evidenceIds || [];

        this.createdAt = data.createdAt || now();
    }
}
