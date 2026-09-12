class SearchSpaceSnapshot {
    constructor(data = {}) {
        this.id = data.id || makeId('space-snapshot');

        this.spaceId = data.spaceId || null;

        this.partitionIds = data.partitionIds || [];

        this.parentSnapshotId = data.parentSnapshotId || null;

        this.version = data.version ?? 1;

        this.fingerprint = data.fingerprint || null;

        this.createdAt = data.createdAt || now();
    }

    serialize() {
        return { ...this };
    }
}
