class SearchSpace {
    constructor(data = {}) {
        this.id = data.id || makeId('space');

        this.domainId =
            data.domainId || null;

        this.partitionIds =
            data.partitionIds || [];

        this.rootPartitionIds =
            data.rootPartitionIds || [];

        this.createdAt =
            data.createdAt || now();
    }
}
