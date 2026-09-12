class ResourceReservation {
    constructor(data = {}) {
        this.id = data.id || makeId('reservation');

        this.workItemId =
            data.workItemId || null;

        this.sessionId =
            data.sessionId || null;

        this.resourceClass =
            data.resourceClass || null;

        this.requested =
            data.requested || {};

        this.reserved =
            data.reserved || {};

        this.status =
            data.status || 'reserved';

        this.createdAt =
            data.createdAt || now();

        this.expiresAt =
            data.expiresAt || null;
    }

    serialize() {
        return { ...this };
    }
}
