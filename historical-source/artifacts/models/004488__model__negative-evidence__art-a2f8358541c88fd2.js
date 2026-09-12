class NegativeEvidence {
    constructor(data = {}) {
        this.id = data.id || makeId('neg');

        this.subject = data.subject || null;

        this.scope = data.scope || null;

        this.predicate = data.predicate || null;

        this.observationIds = data.observationIds || [];

        this.enumeratorId = data.enumeratorId || null;

        this.methodId = data.methodId || null;
        this.methodVersion = data.methodVersion || null;

        this.strength = data.strength || 'weak';

        this.conditions = data.conditions || [];

        this.createdAt = data.createdAt || now();
    }

    serialize() {
        return { ...this };
    }
}
