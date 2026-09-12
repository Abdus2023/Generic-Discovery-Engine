class CoverageClaim {
    constructor(data = {}) {
        this.id = data.id || makeId('coverage-claim');

        this.sessionId = data.sessionId || null;
        this.domainId = data.domainId || null;
        this.partitionId = data.partitionId || null;

        this.dimension = data.dimension || null;

        this.claim = data.claim || null;

        this.assurance = data.assurance || 'unknown';

        this.evidenceIds = data.evidenceIds || [];

        this.methodId = data.methodId || null;
        this.methodVersion = data.methodVersion || null;

        this.createdAt = data.createdAt || now();
    }

    serialize() {
        return { ...this };
    }
}
