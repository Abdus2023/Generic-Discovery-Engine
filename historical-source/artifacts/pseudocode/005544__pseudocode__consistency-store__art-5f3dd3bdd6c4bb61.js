class ConsistencyStore {
    async read(aggregateId) {
        throw new Error('Not implemented');
    }

    async compareAndSwap(
        aggregateId,
        expectedVersion,
        mutation
    ) {
        throw new Error('Not implemented');
    }
}
