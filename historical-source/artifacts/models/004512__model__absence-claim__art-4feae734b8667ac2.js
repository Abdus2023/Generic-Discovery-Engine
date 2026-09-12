class AbsenceClaim {
    constructor(data = {}) {
        this.id = data.id || makeId('absence');

        this.subject = data.subject || null;

        this.predicate = data.predicate || null;

        this.object = data.object ?? null;

        this.scope = data.scope || null;

        this.evidenceIds = data.evidenceIds || [];

        this.assurance = data.assurance || 'unknown';

        this.confidence = Number.isFinite(data.confidence)
            ? data.confidence
            : 0;

        this.conditions = data.conditions || [];

        this.status = data.status || 'active';

        this.createdAt = data.createdAt || now();
    }
}
