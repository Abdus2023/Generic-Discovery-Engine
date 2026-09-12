class Claim {
    constructor(data = {}) {
        this.id =
            data.id || makeId('claim');

        this.subject =
            data.subject || null;

        this.predicate =
            data.predicate || null;

        this.object =
            data.object ?? null;

        this.evidenceIds =
            data.evidenceIds || [];

        this.sessionId =
            data.sessionId || null;

        this.confidence =
            Number.isFinite(data.confidence)
                ? data.confidence
                : 0.5;

        this.createdAt =
            data.createdAt || now();
    }
}
