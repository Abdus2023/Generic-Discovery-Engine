class QueryExpansionProvider {
    canExpand(goal, context) {
        return false;
    }

    expand(goal, context) {
        return [];
    }

    describe() {
        return {
            id: 'unknown-expander',
            name: 'Unknown Query Expansion Provider'
        };
    }
}
