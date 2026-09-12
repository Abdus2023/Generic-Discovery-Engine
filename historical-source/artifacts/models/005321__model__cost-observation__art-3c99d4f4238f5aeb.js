class CostObservation {
    constructor(data = {}) {
        this.id = data.id || makeId('cost');

        this.workItemId =
            data.workItemId || null;

        this.attemptId =
            data.attemptId || null;

        this.providerId =
            data.providerId || null;

        this.values =
            data.values || {};

        this.measurementMethod =
            data.measurementMethod || null;

        this.confidence =
            Number.isFinite(data.confidence)
                ? data.confidence
                : 1;

        this.createdAt =
            data.createdAt || now();
    }

    serialize() {
        return { ...this };
    }
}
