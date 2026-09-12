class PresenceAssertion {
    constructor(data = {}) {
        this.id = data.id || makeId('presence');

        this.subject = data.subject || null;

        this.state = data.state || 'unknown';

        this.scope = data.scope || null;

        this.sessionId = data.sessionId || null;

        this.evidenceIds = data.evidenceIds || [];

        this.methodId = data.methodId || null;
        this.methodVersion = data.methodVersion || null;

        this.confidence = Number.isFinite(data.confidence)
            ? data.confidence
            : 0;

        this.conditions = data.conditions || [];

        this.status = data.status || 'active';

        this.createdAt = data.createdAt || now();
    }

    serialize() {
        return { ...this };
    }
}
