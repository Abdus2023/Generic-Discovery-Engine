class FrontierArbitrator {
    constructor(config = {}) {
        this.classPolicies =
            new Map();

        this.buckets =
            new Map();

        this.now =
            config.now || (() => Date.now());
    }

    admit(work, context) {
        return {
            allowed: false,
            reason: 'not-implemented'
        };
    }

    score(work, context) {
        return {
            score: 0,
            components: {}
        };
    }

    select(workItems, context) {
        return {
            workItem: null,
            decision: null
        };
    }

    describe() {
        return {
            id: 'frontier-arbitrator',
            name: 'Unified Frontier Arbitrator'
        };
    }
}
