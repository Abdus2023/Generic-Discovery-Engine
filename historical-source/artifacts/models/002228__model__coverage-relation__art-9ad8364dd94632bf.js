class CoverageRelation {
    constructor(data = {}) {
        this.id = data.id || makeId('covrel');

        this.fromCoverageId = data.fromCoverageId || null;
        this.toCoverageId = data.toCoverageId || null;

        this.relation = data.relation || 'unknown';

        this.overlapEstimate = data.overlapEstimate ?? null;

        this.evidenceIds = data.evidenceIds || [];

        this.createdAt = data.createdAt || now();
    }
}
