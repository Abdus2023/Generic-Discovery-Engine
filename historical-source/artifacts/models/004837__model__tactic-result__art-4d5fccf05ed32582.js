class TacticResult {
    constructor(data = {}) {
        this.executionId = data.executionId || null;

        this.status = data.status || 'unknown';

        this.proposals = data.proposals || [];
        this.evidence = data.evidence || [];

        this.cursor = data.cursor ?? null;
        this.checkpoint = data.checkpoint ?? null;

        this.exhausted = data.exhausted === true;

        this.stats = data.stats || {};

        this.reason = data.reason || null;
    }
}
