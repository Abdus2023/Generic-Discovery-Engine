class WorkItem {
    constructor(data = {}) {
        this.id =
            data.id || makeId('work');

        this.kind =
            data.kind || 'unknown';

        this.sessionId =
            data.sessionId || null;

        this.parentId =
            data.parentId || null;

        this.priority =
            Number.isFinite(data.priority)
                ? data.priority
                : 0;

        this.depth =
            Number.isFinite(data.depth)
                ? data.depth
                : 0;

        this.status =
            data.status || 'queued';

        this.attempts =
            data.attempts || 0;

        this.createdAt =
            data.createdAt || now();

        this.queuedAt =
            data.queuedAt || null;

        this.claimedAt =
            data.claimedAt || null;

        this.startedAt =
            data.startedAt || null;

        this.completedAt =
            data.completedAt || null;

        this.claimedBy =
            data.claimedBy || null;

        this.claimId =
            data.claimId || null;

        this.leaseUntil =
            data.leaseUntil || null;

        this.nextAttemptAt =
            data.nextAttemptAt || null;

        this.error =
            data.error || null;
    }
}
