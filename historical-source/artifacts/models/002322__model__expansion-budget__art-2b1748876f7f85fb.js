class ExpansionBudget {
    constructor(data = {}) {
        this.maxProposals = data.maxProposals ?? 1000;
        this.maxAdmissions = data.maxAdmissions ?? 500;
        this.maxDepth = data.maxDepth ?? 5;
        this.maxChildrenPerPartition =
            data.maxChildrenPerPartition ?? 25;

        this.proposals = 0;
        this.admissions = 0;
    }

    canPropose() {
        return this.proposals < this.maxProposals;
    }

    canAdmit() {
        return this.admissions < this.maxAdmissions;
    }
}
