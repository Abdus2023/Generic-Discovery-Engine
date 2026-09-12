class ClassificationAssertion {
    constructor(data = {}) {
        this.id = data.id || makeId('class');

        this.resourceId = data.resourceId || null;

        this.axis = data.axis || 'unknown';

        this.type = data.type || 'unknown';

        this.confidence = Number.isFinite(data.confidence)
            ? data.confidence
            : 0;

        this.evidenceIds = data.evidenceIds || [];

        this.classifierId = data.classifierId || null;

        this.classifierVersion = data.classifierVersion || null;

        this.status = data.status || 'active';

        this.createdAt = data.createdAt || now();
    }

    serialize() {
        return { ...this };
    }
}
