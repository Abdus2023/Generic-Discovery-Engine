class CandidateSource {
    discover(context) {
        throw new Error('Not implemented');
    }

    describe() {
        return {
            id: 'unknown-source',
            name: 'Unknown Candidate Source'
        };
    }
}
