class Evidence {
    constructor(data = {}) {
        this.id =
            data.id || makeId('evidence');

        this.kind =
            data.kind || 'unknown';

        this.value =
            data.value ?? null;

        this.observationId =
            data.observationId || null;

        this.sessionId =
            data.sessionId || null;

        this.locator =
            data.locator || null;

        this.provenance =
            data.provenance || {};

        this.confidence =
            Number.isFinite(data.confidence)
                ? data.confidence
                : 0.5;

        this.createdAt =
            data.createdAt || now();
    }
}
