class PersistenceAdapter {
    async begin() {
        throw new Error('Not implemented');
    }

    async commit(transaction) {
        throw new Error('Not implemented');
    }

    async rollback(transaction) {
        throw new Error('Not implemented');
    }

    async read(key) {
        throw new Error('Not implemented');
    }

    async scan(prefix) {
        throw new Error('Not implemented');
    }

    describe() {
        return {
            id: 'unknown-persistence',
            name: 'Unknown Persistence Adapter'
        };
    }
}
