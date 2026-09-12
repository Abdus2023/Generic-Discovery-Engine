class QueryPlan {
    constructor(data = {}) {
        this.id = data.id || makeId('qplan');

        this.goalId =
            data.goalId || null;

        this.domainId =
            data.domainId || null;

        this.steps =
            data.steps || [];

        this.constraints =
            data.constraints || [];

        this.priority =
            Number.isFinite(data.priority)
                ? data.priority
                : 0;

        this.status =
            data.status || 'planned';

        this.plannerId =
            data.plannerId || null;

        this.plannerVersion =
            data.plannerVersion || null;

        this.createdAt =
            data.createdAt || now();
    }

    serialize() {
        return { ...this };
    }
}
