class SearchWorkKey {
    constructor(data = {}) {
        this.kind = data.kind || 'unknown';

        this.target = data.target || null;

        this.partitionId = data.partitionId || null;

        this.enumeratorId = data.enumeratorId || null;

        this.cursor = data.cursor ?? null;

        this.strategyId = data.strategyId || null;
    }

    serialize() {
        return { ...this };
    }
}
