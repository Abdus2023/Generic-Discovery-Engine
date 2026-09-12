class NegativeEvidence {
    constructor(data = {}) {
        this.id = data.id || makeId('neg-evidence');

        this.scope = data.scope || null;

        this.predicate = data.predicate || null;

        this.observationIds = data.observationIds || [];

        this.methodId = data.methodId || null;

        this.strength = data.strength || 'weak';

        this.conditions = data.conditions || [];

        this.createdAt = data.createdAt || now();
    }
}
