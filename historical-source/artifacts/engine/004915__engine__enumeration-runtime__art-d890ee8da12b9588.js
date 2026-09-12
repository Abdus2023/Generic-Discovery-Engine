class EnumerationRuntime {

    async execute(execution, enumerator, context) {
        throw new Error('Not implemented');
    }

    async resume(execution, enumerator, context) {
        throw new Error('Not implemented');
    }

    validateTermination(page, context) {
        return {
            terminated: false,
            evidenceIds: []
        };
    }
}
