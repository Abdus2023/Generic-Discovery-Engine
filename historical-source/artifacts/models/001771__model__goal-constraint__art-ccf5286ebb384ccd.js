class GoalConstraint {
    constructor(data = {}) {
        this.id = data.id || makeId('constraint');

        this.dimension =
            data.dimension || 'unknown';

        this.operator =
            data.operator || 'equals';

        this.value =
            data.value ?? null;

        this.mode =
            data.mode || 'hard';

        this.reason =
            data.reason || null;

        this.createdAt =
            data.createdAt || now();
    }
}
