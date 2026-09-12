class PartitionProposal {
    constructor(data = {}) {
        this.id = data.id || makeId('pprop');

        this.domainId = data.domainId || null;
        this.sessionId = data.sessionId || null;

        this.parentPartitionId = data.parentPartitionId || null;

        this.kind = data.kind || 'unknown';
        this.selector = data.selector || null;

        this.reason = data.reason || null;

        this.evidenceIds = data.evidenceIds || [];

        this.confidence = Number.isFinite(data.confidence)
            ? data.confidence
            : 0;

        this.status = data.status || 'proposed';

        this.createdAt = data.createdAt || now();
    }

    serialize() {
        return { ...this };
    }
}
