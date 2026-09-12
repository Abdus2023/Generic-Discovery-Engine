class Resource {
    constructor(data = {}) {
        this.id = data.id || makeId('resource');

        this.locatorIds = data.locatorIds || [];

        this.observationIds = data.observationIds || [];

        this.claimIds = data.claimIds || [];

        this.fingerprintIds = data.fingerprintIds || [];

        this.classificationIds =
            data.classificationIds || [];

        this.createdAt =
            data.createdAt || now();

        this.updatedAt =
            data.updatedAt || this.createdAt;
    }
}
