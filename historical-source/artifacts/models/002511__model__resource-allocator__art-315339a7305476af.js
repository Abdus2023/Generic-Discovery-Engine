class ResourceAllocator {
    canAllocate(work, context) {
        return {
            allowed: false,
            reason: 'not-implemented'
        };
    }

    estimate(work, context) {
        return {};
    }

    reserve(work, estimate, context) {
        throw new Error('Not implemented');
    }

    release(reservation, context) {
        throw new Error('Not implemented');
    }
}
