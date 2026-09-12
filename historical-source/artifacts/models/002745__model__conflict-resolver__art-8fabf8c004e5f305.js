class ConflictResolver {
    canResolve(conflict, context) {
        return false;
    }

    async resolve(conflict, context) {
        throw new Error('Not implemented');
    }

    describe() {
        return {
            id: 'unknown-resolver',
            name: 'Unknown Conflict Resolver'
        };
    }
}
