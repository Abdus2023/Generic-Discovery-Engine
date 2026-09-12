class CandidateSource {
    describe() {
        return {
            id: 'unknown-source',
            priority: 0
        };
    }

    canDiscover(context) {
        return true;
    }

    discover(context) {
        return {
            proposals: []
        };
    }
}
