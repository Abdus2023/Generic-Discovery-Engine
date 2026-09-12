class QueryTactic {
    canPlan(goal, context) {
        return false;
    }

    plan(goal, context) {
        throw new Error('Not implemented');
    }

    describe() {
        return {
            id: 'unknown-tactic',
            name: 'Unknown Query Tactic'
        };
    }
}
