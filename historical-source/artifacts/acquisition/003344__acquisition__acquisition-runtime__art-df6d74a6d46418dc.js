class AcquisitionRuntime {
    constructor(options = {}) {
        this.scheduler = options.scheduler || null;
        this.providerRegistry = options.providerRegistry || null;
        this.budget = options.budget || null;
        this.originController = options.originController || null;
        this.cancellation = options.cancellation || null;
    }

    async execute(plan) {
        throw new Error('Not implemented');
    }

    describe() {
        return {
            id: 'unknown-runtime'
        };
    }
}
