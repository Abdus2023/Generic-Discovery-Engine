class TacticRuntime {

    canExecute(execution, context) {
        return false;
    }

    async execute(execution, context) {
        throw new Error('Not implemented');
    }

    cancel(execution, reason = 'cancelled') {
        throw new Error('Not implemented');
    }

    checkpoint(execution, state) {
        throw new Error('Not implemented');
    }

    describe() {
        return {
            id: 'unknown-tactic-runtime',
            name: 'Unknown Tactic Runtime'
        };
    }
}
