class PersistenceTransaction {
    constructor(data = {}) {
        this.id = data.id || makeId('tx');

        this.operations =
            data.operations || [];

        this.status =
            data.status || 'active';

        this.createdAt =
            data.createdAt || now();

        this.committedAt =
            data.committedAt || null;
    }

    add(operation) {
        this.operations.push(operation);
    }

    serialize() {
        return { ...this };
    }
}
