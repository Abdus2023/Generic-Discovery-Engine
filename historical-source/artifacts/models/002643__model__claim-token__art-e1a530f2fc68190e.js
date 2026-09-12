class ClaimToken {
    constructor(data = {}) {
        this.id =
            data.id || makeId('claim');

        this.workItemId =
            data.workItemId || null;

        this.workerId =
            data.workerId || null;

        this.epoch =
            data.epoch ?? 0;

        this.claimedAt =
            data.claimedAt || now();

        this.expiresAt =
            data.expiresAt || null;

        this.status =
            data.status || 'active';
    }

    serialize() {
        return { ...this };
    }
}
