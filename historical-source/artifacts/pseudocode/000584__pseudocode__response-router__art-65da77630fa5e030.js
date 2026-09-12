class ResponseRouter {
    constructor() {
        this.providers = [];
    }

    register(provider) {
        this.providers.push(provider);
        return this;
    }

    select(observation) {
        for (const provider of this.providers) {
            try {
                if (provider.canRecognize(observation)) {
                    return provider;
                }
            } catch (_) {
                // Provider routing must not kill the scan.
            }
        }

        return null;
    }
}
