class Resource {
    constructor(data = {}) {
        this.id = data.id || makeId('resource');

        this.locatorIds = data.locatorIds || [];

        this.representationIds =
            data.representationIds || [];

        this.claimIds =
            data.claimIds || [];

        this.classificationIds =
            data.classificationIds || [];

        this.createdAt =
            data.createdAt || now();

        this.updatedAt =
            data.updatedAt || this.createdAt;
    }
}
