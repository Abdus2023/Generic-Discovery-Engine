class StrategyOutcome {
    constructor(data = {}) {
        this.strategyId =
            data.strategyId || null;

        this.partitionId =
            data.partitionId || null;

        this.workItemId =
            data.workItemId || null;

        this.status =
            data.status || 'unknown';

        this.candidates =
            data.candidates || 0;

        this.newResources =
            data.newResources || 0;

        this.newArtifacts =
            data.newArtifacts || 0;

        this.usefulDiscoveries =
            data.usefulDiscoveries || 0;

        this.cost =
            data.cost || {};

        this.failure =
            data.failure || null;

        this.createdAt =
            data.createdAt || now();
    }
}
