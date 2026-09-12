class TacticBatch {
    constructor(data = {}) {
        this.id = data.id || makeId('tbatch');

        this.executionId = data.executionId || null;

        this.sequence = data.sequence ?? 0;

        this.cursorBefore = data.cursorBefore ?? null;
        this.cursorAfter = data.cursorAfter ?? null;

        this.probes = data.probes || 0;
        this.proposals = data.proposals || 0;

        this.status = data.status || 'running';

        this.startedAt = data.startedAt || now();
        this.completedAt = data.completedAt || null;

        this.error = data.error || null;
    }
}
