class CompletenessClaim {
    constructor(data = {}) {
        this.id = data.id || makeId('complete');

        this.domainId = data.domainId || null;
        this.sessionId = data.sessionId || null;

        this.scope = data.scope || null;

        this.status = data.status || 'not-established';

        this.assurance = data.assurance || 'unknown';

        this.enumerator = data.enumerator || null;

        this.evidenceIds = data.evidenceIds || [];

        this.conditions = data.conditions || [];

        this.createdAt = data.createdAt || now();
    }

    serialize() {
        return { ...this };
    }
}
