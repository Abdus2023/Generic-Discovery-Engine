class TypeEvidence {
    constructor(data = {}) {
        this.id = data.id || makeId('te');

        this.resourceId = data.resourceId || null;

        this.axis = data.axis || null;

        this.observationId = data.observationId || null;

        this.kind = data.kind || 'unknown';

        this.value = data.value ?? null;

        this.locator = data.locator || null;

        this.weight = Number.isFinite(data.weight)
            ? data.weight
            : 0;

        this.provenance = data.provenance || {};

        this.createdAt = data.createdAt || now();
    }
}
