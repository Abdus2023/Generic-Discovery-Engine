class ArbitrationDecision {
    constructor(data = {}) {
        this.id = data.id || makeId('arb');

        this.sessionId = data.sessionId || null;

        this.workItemId = data.workItemId || null;

        this.workClass = data.workClass || null;

        this.reason = data.reason || null;

        this.score = Number.isFinite(data.score)
            ? data.score
            : null;

        this.components = data.components || {};

        this.constraints = data.constraints || [];

        this.alternatives = data.alternatives || [];

        this.createdAt = data.createdAt || now();
    }

    serialize() {
        return { ...this };
    }
}
