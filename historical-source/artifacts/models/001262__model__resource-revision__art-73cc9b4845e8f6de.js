class ResourceRevision {
    constructor(data = {}) {
        this.id = data.id || makeId('revision');

        this.resourceId =
            data.resourceId || null;

        this.representationId =
            data.representationId || null;

        this.artifactId =
            data.artifactId || null;

        this.observationId =
            data.observationId || null;

        this.revisionNumber =
            data.revisionNumber || null;

        this.previousRevisionId =
            data.previousRevisionId || null;

        this.detectedAt =
            data.detectedAt || now();

        this.status =
            data.status || 'active';
    }
}
