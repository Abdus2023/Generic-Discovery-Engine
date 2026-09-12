class SearchTactic {

    canExecute(step, context) {
        return false;
    }

    async execute(context) {
        throw new Error('Not implemented');
    }

    describe() {
        return {
            id: 'unknown-tactic',
            name: 'Unknown Search Tactic'
        };
    }
}
