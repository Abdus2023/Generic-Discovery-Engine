class CoverageRecord {
    constructor(data = {}) {
        this.id = data.id || makeId('coverage');

        this.sessionId = data.sessionId || null;
        this.domainId = data.domainId || null;
        this.partitionId = data.partitionId || null;

        this.dimension = data.dimension || 'partition';

        this.status = data.status || 'unknown';

        this.explored = Number.isFinite(data.explored)
            ? data.explored
            : 0;

        this.estimatedTotal = Number.isFinite(data.estimatedTotal)
            ? data.estimatedTotal
            : null;

        this.method = data.method || null;

        this.evidenceIds = data.evidenceIds || [];

        this.createdAt = data.createdAt || now();
    }

    ratio() {
        if (
            this.estimatedTotal === null ||
            this.estimatedTotal <= 0
        ) {
            return null;
        }

        return Math.min(
            1,
            this.explored / this.estimatedTotal
        );
    }

    serialize() {
        return { ...this };
    }
}
