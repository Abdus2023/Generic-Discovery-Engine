class ExplorationPlan {
    constructor(data = {}) {
        this.id = data.id || makeId('explore');

        this.partitionId =
            data.partitionId || null;

        this.strategyId =
            data.strategyId || null;

        this.work = data.work || [];

        this.priority =
            Number.isFinite(data.priority)
                ? data.priority
                : 0;

        this.reason =
            data.reason || null;

        this.createdAt =
            data.createdAt || now();
    }
}
