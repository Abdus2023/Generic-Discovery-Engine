class AbsenceReasoner {
    assess(context) {
        const {
            subject,
            claims,
            negativeEvidence,
            coverage
        } = context;

        if (!subject) {
            return {
                state: 'unknown',
                assurance: 'unknown',
                reason: 'subject-missing'
            };
        }

        if (!negativeEvidence?.length) {
            return {
                state: 'not-observed',
                assurance: 'none'
            };
        }

        // Conservative evaluation.
        // Strong absence requires bounded scope and
        // sufficiently complete enumeration.

        return {
            state: 'not-found',
            assurance: 'strategy-relative'
        };
    }
}
