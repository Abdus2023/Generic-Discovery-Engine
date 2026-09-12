class ConflictRecord {
    constructor(data = {}) {
        this.id = data.id || makeId('conflict');

        this.type = data.type;
        this.aggregateId = data.aggregateId || null;

        this.baseVersion = data.baseVersion ?? null;
        this.currentVersion = data.currentVersion ?? null;

        this.leftEventId = data.leftEventId || null;
        this.rightEventId = data.rightEventId || null;

        this.leftState = data.leftState || null;
        this.rightState = data.rightState || null;

        this.reason = data.reason || null;

        this.status = data.status || 'detected';

        this.resolution = data.resolution || null;

        this.createdAt = data.createdAt || now();
        this.resolvedAt = data.resolvedAt || null;
    }
}
