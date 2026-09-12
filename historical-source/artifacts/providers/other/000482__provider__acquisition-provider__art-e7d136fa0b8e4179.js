class AcquisitionProvider {
    capabilities() {
        return [];
    }

    canExecute(plan) {
        return false;
    }

    async execute(plan) {
        throw new Error('Not implemented');
    }

    describe() {
        return {
            id: 'unknown',
            name: 'Unknown Acquisition Provider'
        };
    }
}
