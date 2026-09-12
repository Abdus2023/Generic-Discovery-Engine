class ResourceRepresentation {
    constructor(data = {}) {
        this.id = data.id || makeId('repr');

        this.resourceId =
            data.resourceId || null;

        this.format =
            data.format || 'unknown';

        this.mediaType =
            data.mediaType || null;

        this.artifactIds =
            data.artifactIds || [];

        this.createdAt =
            data.createdAt || now();
    }
}
