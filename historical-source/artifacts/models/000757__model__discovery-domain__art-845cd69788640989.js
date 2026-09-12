class DiscoveryDomain {
    constructor(data = {}) {
        this.id = data.id || makeId('domain');

        this.schemes =
            data.schemes || ['https'];

        this.origins =
            data.origins || [];

        this.resourceTypes =
            data.resourceTypes || [];

        this.seeds =
            data.seeds || [];

        this.sources =
            data.sources || [];

        this.maxDepth =
            data.maxDepth ?? 5;

        this.budgets = {
            maxCandidates:
                data.budgets?.maxCandidates ?? 750,

            maxDiscoveryTasks:
                data.budgets?.maxDiscoveryTasks ?? 1000,

            maxProposals:
                data.budgets?.maxProposals ?? 2000,

            maxAcquisitions:
                data.budgets?.maxAcquisitions ?? 150
        };

        this.policy =
            data.policy || {};

        this.termination =
            data.termination || {};

        this.createdAt =
            data.createdAt || now();
    }
}
