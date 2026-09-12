class StrategyPerformance {
    constructor(data = {}) {
        this.strategyId =
            data.strategyId || null;

        this.partitionKind =
            data.partitionKind || null;

        this.attempts =
            data.attempts || 0;

        this.successes =
            data.successes || 0;

        this.failures =
            data.failures || 0;

        this.candidates =
            data.candidates || 0;

        this.newResources =
            data.newResources || 0;

        this.newArtifacts =
            data.newArtifacts || 0;

        this.usefulClassifications =
            data.usefulClassifications || 0;

        this.costRequests =
            data.costRequests || 0;

        this.costBytes =
            data.costBytes || 0;

        this.elapsedMs =
            data.elapsedMs || 0;
    }
}
