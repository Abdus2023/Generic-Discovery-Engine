class PartitionProposal {
    constructor(data = {}) {
        this.parentPartitionId =
            data.parentPartitionId || null;

        this.kind =
            data.kind || 'unknown';

        this.selector =
            data.selector || null;

        this.reason =
            data.reason || null;

        this.evidenceIds =
            data.evidenceIds || [];

        this.confidence =
            Number.isFinite(data.confidence)
                ? data.confidence
                : 0;
    }
}
