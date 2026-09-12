class EnumerationEntry {
    constructor(data = {}) {
        this.id = data.id || makeId('entry');

        this.position = data.position ?? null;

        this.value = data.value ?? null;

        this.type = data.type || 'unknown';

        this.sourceLocator = data.sourceLocator || null;

        this.evidenceIds = data.evidenceIds || [];

        this.createdAt = data.createdAt || now();
    }

    serialize() {
        return { ...this };
    }
}
