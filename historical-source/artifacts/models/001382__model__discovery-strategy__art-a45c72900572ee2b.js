class DiscoveryStrategy {
    canExplore(partition, context) {
        return false;
    }

    async explore(partition, context) {
        throw new Error('Not implemented');
    }

    describe() {
        return {
            id: 'unknown-strategy',
            name: 'Unknown Discovery Strategy'
        };
    }
}
