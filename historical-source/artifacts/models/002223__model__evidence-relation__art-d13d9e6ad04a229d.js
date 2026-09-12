class EvidenceRelation {
    constructor(data = {}) {
        this.fromEvidenceId = data.fromEvidenceId || null;
        this.toEvidenceId = data.toEvidenceId || null;

        this.relation = data.relation || 'unknown';

        this.evidenceIds = data.evidenceIds || [];

        this.createdAt = data.createdAt || now();
    }
}
