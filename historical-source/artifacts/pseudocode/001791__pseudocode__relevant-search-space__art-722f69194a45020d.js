class RelevantSearchSpace {
    constructor(data = {}) {
        this.id = data.id || makeId('relevant-space');

        this.goalId =
            data.goalId || null;

        this.domainId =
            data.domainId || null;

        this.partitionIds =
            data.partitionIds || [];

        this.constraintIds =
            data.constraintIds || [];

        this.createdAt =
            data.createdAt || now();
    }
}
