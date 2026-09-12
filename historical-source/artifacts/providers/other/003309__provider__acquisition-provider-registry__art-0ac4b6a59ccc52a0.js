class AcquisitionProviderRegistry {
    constructor() {
        this.providers = [];
    }

    register(provider) {
        this.providers.push(provider);
        return this;
    }

    select(plan) {
        return this.providers.find(
            provider =>
                provider.canExecute(plan)
        ) || null;
    }

    describe() {
        return this.providers.map(
            provider => provider.describe()
        );
    }
}
