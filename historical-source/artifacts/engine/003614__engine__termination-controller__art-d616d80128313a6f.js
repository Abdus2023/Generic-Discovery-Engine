class TerminationController {
    constructor(domain, session) {
        this.domain = domain;
        this.session = session;
    }

    evaluate(state) {
        const limits =
            this.domain.budgets;

        if (
            state.candidates >=
            limits.maxCandidates
        ) {
            return {
                terminate: true,
                reason: 'candidate-limit'
            };
        }

        if (
            state.acquisitions >=
            limits.maxAcquisitions
        ) {
            return {
                terminate: true,
                reason: 'acquisition-limit'
            };
        }

        if (
            state.discoveryTasks >=
            limits.maxDiscoveryTasks
        ) {
            return {
                terminate: true,
                reason: 'discovery-task-limit'
            };
        }

        return {
            terminate: false
        };
    }
}
