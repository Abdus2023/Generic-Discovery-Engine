class SearchSpaceSnapshot {
    constructor(data = {}) {
        this.id = data.id || makeId('space-snapshot');

        this.domainId = data.domainId || null;

        this.partitionIds = data.partitionIds || [];

        this.enumeratorIds = data.enumeratorIds || [];

        this.fingerprint = data.fingerprint || null;

        this.createdAt = data.createdAt || now();
    }
}
