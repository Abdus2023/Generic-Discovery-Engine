class CoverageResolver {

    combine(records, context) {
        return {
            status: 'unknown',
            explored: null,
            estimatedTotal: null,
            overlap: null,
            evidenceIds: []
        };
    }
}
