class QueryPlanner {
    tactics() {
        return [];
    }

    canPlan(goal, context) {
        return true;
    }

    plan(goal, context) {
        throw new Error('Not implemented');
    }

    describe() {
        return {
            id: 'unknown-planner',
            name: 'Unknown Query Planner'
        };
    }
}
