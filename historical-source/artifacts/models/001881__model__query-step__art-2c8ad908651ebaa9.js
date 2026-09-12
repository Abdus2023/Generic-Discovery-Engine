class QueryStep {
    constructor(data = {}) {
        this.id = data.id || makeId('qstep');

        this.planId =
            data.planId || null;

        this.kind =
            data.kind || 'unknown';

        this.target =
            data.target || null;

        this.constraints =
            data.constraints || {};

        this.dependsOn =
            data.dependsOn || [];

        this.priority =
            Number.isFinite(data.priority)
                ? data.priority
                : 0;

        this.status =
            data.status || 'planned';

        this.createdAt =
            data.createdAt || now();
    }

    serialize() {
        return { ...this };
    }
}
