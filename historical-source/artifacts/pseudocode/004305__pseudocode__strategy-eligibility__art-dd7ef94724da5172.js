class StrategyEligibility {
    constructor(data = {}) {
        this.strategyId =
            data.strategyId || null;

        this.allowed =
            data.allowed !== false;

        this.reason =
            data.reason || null;

        this.missingCapabilities =
            data.missingCapabilities || [];

        this.createdAt =
            data.createdAt || now();
    }
}
