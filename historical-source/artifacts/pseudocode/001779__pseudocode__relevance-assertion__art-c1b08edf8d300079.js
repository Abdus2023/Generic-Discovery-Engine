class RelevanceAssertion {
    constructor(data = {}) {
        this.id = data.id || makeId('relevance');

        this.goalId =
            data.goalId || null;

        this.resourceId =
            data.resourceId || null;

        this.status =
            data.status || 'unknown';

        this.score =
            Number.isFinite(data.score)
                ? data.score
                : 0;

        this.matchedConstraints =
            data.matchedConstraints || [];

        this.failedConstraints =
            data.failedConstraints || [];

        this.evidenceIds =
            data.evidenceIds || [];

        this.evaluatorId =
            data.evaluatorId || null;

        this.evaluatorVersion =
            data.evaluatorVersion || null;

        this.createdAt =
            data.createdAt || now();
    }

    serialize() {
        return { ...this };
    }
}
