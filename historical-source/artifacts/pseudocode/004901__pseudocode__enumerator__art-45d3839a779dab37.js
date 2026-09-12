class Enumerator {

    canEnumerate(target, context) {
        return false;
    }

    async begin(context) {
        throw new Error('Not implemented');
    }

    async next(context, cursor) {
        throw new Error('Not implemented');
    }

    async checkpoint(context, state) {
        return state;
    }

    async validateCursor(context, cursor) {
        return { valid: true };
    }

    describe() {
        return {
            id: 'unknown-enumerator',
            name: 'Unknown Enumerator'
        };
    }
}
