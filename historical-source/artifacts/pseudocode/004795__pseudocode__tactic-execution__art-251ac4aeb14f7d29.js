class TacticExecution {
    constructor(data = {}) {
        this.id = data.id || makeId('texec');

        this.planId = data.planId || null;
        this.planVersion = data.planVersion ?? null;

        this.queryStepId = data.queryStepId || null;
        this.tacticId = data.tacticId || null;

        this.sessionId = data.sessionId || null;
        this.partitionId = data.partitionId || null;

        this.status = data.status || 'queued';

        this.attempts = data.attempts || 0;

        this.cursor = data.cursor ?? null;
        this.checkpoint = data.checkpoint ?? null;

        this.stats = {
            batches: 0,
            probes: 0,
            proposals: 0,
            accepted: 0,
            merged: 0,
            rejected: 0,
            errors: 0,
            ...(data.stats || {})
        };

        this.budget = data.budget || null;

        this.createdAt = data.createdAt || now();
        this.startedAt = data.startedAt || null;
        this.completedAt = data.completedAt || null;

        this.error = data.error || null;
    }

    serialize() {
        return { ...this };
    }
}
