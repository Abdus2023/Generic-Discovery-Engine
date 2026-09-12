class TacticCheckpoint {
    constructor(data = {}) {
        this.id = data.id || makeId('checkpoint');

        this.executionId = data.executionId || null;

        this.sequence = data.sequence ?? 0;

        this.cursor = data.cursor ?? null;

        this.stats = data.stats || {};

        this.strategyState = data.strategyState ?? null;

        this.createdAt = data.createdAt || now();
    }

    serialize() {
        return { ...this };
    }
}
