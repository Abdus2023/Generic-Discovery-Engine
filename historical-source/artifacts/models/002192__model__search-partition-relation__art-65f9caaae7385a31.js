class SearchPartitionRelation {
    constructor(data = {}) {
        this.id = data.id || makeId('prel');

        this.fromPartitionId = data.fromPartitionId || null;
        this.toPartitionId = data.toPartitionId || null;

        this.relation = data.relation || 'unknown';

        this.scope = data.scope || null;

        this.evidenceIds = data.evidenceIds || [];

        this.confidence = Number.isFinite(data.confidence)
            ? data.confidence
            : 0;

        this.createdAt = data.createdAt || now();
    }

    serialize() {
        return { ...this };
    }
}
