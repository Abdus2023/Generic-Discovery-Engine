class ResourceType {
    constructor(data = {}) {
        this.id = data.id || makeId('rtype');

        this.axis = data.axis || 'unknown';

        this.namespace = data.namespace || 'generic';

        this.name = data.name || 'unknown';

        this.parent = data.parent || null;

        this.version = data.version || '1';

        this.createdAt = data.createdAt || now();
    }

    serialize() {
        return {
            id: this.id,
            axis: this.axis,
            namespace: this.namespace,
            name: this.name,
            parent: this.parent,
            version: this.version,
            createdAt: this.createdAt
        };
    }
}
