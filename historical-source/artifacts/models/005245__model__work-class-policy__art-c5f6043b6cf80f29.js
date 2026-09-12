class WorkClassPolicy {
    constructor(data = {}) {
        this.class = data.class;

        this.enabled = data.enabled !== false;

        this.minShare = data.minShare ?? 0;
        this.maxShare = data.maxShare ?? 1;

        this.weight = data.weight ?? 1;

        this.reservedCapacity =
            data.reservedCapacity ?? 0;

        this.maxConcurrent =
            data.maxConcurrent ?? Infinity;

        this.starvationLimitMs =
            data.starvationLimitMs ?? 30000;
    }

    serialize() {
        return { ...this };
    }
}
