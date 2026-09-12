class GoalResult {
    constructor(data = {}) {
        this.id = data.id || makeId('goal-result');

        this.goalId =
            data.goalId || null;

        this.resourceIds =
            data.resourceIds || [];

        this.relevanceAssertionIds =
            data.relevanceAssertionIds || [];

        this.status =
            data.status || 'incomplete';

        this.satisfaction =
            data.satisfaction || 'unsatisfied';

        this.coverage =
            data.coverage || null;

        this.completenessClaimId =
            data.completenessClaimId || null;

        this.createdAt =
            data.createdAt || now();
    }
}
