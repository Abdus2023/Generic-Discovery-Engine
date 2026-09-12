class CapabilitySet {
    constructor(values = []) {
        this.values = new Set(values);
    }

    has(capability) {
        return this.values.has(capability);
    }

    add(capability) {
        this.values.add(capability);
        return this;
    }

    hasAll(required) {
        return required.every(
            capability =>
                this.values.has(capability)
        );
    }

    missing(required) {
        return required.filter(
            capability =>
                !this.values.has(capability)
        );
    }

    serialize() {
        return [...this.values].sort();
    }
}
