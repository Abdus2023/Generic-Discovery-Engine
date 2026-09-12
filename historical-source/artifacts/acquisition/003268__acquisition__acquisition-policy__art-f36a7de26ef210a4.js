class AcquisitionPolicy {
    constructor(runtimeCapabilities) {
        this.runtimeCapabilities =
            runtimeCapabilities;
    }

    plan(candidate) {
        const required =
            candidate.requirements
                ?.capabilities || [];

        const missing =
            this.runtimeCapabilities
                .missing(required);

        if (missing.length) {
            return deniedPlan(
                candidate,
                'missing-capabilities',
                { missing }
            );
        }

        // Continue with normal policy checks...
    }
}
