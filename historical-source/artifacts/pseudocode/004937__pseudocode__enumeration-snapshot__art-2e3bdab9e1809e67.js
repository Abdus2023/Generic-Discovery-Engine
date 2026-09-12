class EnumerationSnapshot {
    constructor(data = {}) {
        this.id = data.id || makeId('enum-snapshot');

        this.enumeratorId = data.enumeratorId || null;
        this.enumeratorVersion = data.enumeratorVersion || null;

        this.target = data.target || null;

        this.observationId = data.observationId || null;
        this.artifactId = data.artifactId || null;

        this.startedAt = data.startedAt || null;
        this.completedAt = data.completedAt || null;

        this.entryCount = data.entryCount ?? null;

        this.consistency = data.consistency || 'unknown';

        this.createdAt = data.createdAt || now();
    }
}
