class ResourceRevision {
    constructor(data = {}) {
        this.id =
            data.id || makeId('revision');

        this.resourceId =
            data.resourceId;

        this.fingerprintId =
            data.fingerprintId;

        this.observationId =
            data.observationId;

        this.observedAt =
            data.observedAt || now();
    }
}
