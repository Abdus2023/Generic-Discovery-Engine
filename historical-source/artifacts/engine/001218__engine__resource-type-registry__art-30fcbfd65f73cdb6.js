class ResourceTypeRegistry {
    constructor() {
        this.types = new Map();
    }

    register(type) {
        if (this.types.has(type.id)) {
            throw new Error(
                `Resource type already registered: ${type.id}`
            );
        }

        this.types.set(type.id, type);
        return type;
    }

    get(id) {
        return this.types.get(id) || null;
    }

    find(axis, name) {
        for (const type of this.types.values()) {
            if (
                type.axis === axis &&
                type.name === name
            ) {
                return type;
            }
        }

        return null;
    }
}
