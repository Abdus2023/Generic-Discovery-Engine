class SearchHypothesis {
    constructor(data = {}) {
        this.id = data.id || makeId('hypothesis');

        this.goalId =
            data.goalId || null;

        this.target =
            data.target || null;

        this.kind =
            data.kind || 'unknown';

        this.reason =
            data.reason || null;

        this.evidenceIds =
            data.evidenceIds || [];

        this.confidence =
            Number.isFinite(data.confidence)
                ? data.confidence
                : 0;

        this.status =
            data.status || 'proposed';

        this.createdAt =
            data.createdAt || now();
    }
}
