class CoverageLedger {
    constructor() {
        this.records = new Map();
        this.relations = new Map();
    }

    addRecord(record) {
        this.records.set(record.id, record);
    }

    addRelation(relation) {
        this.relations.set(relation.id, relation);
    }

    resolve(scope) {
        throw new Error('Not implemented');
    }
}
