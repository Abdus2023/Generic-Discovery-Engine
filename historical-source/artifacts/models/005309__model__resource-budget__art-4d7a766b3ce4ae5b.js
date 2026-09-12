class ResourceBudget {
    constructor(data = {}) {
        this.limits = {
            requests: data.requests ?? Infinity,
            bytesIn: data.bytesIn ?? Infinity,
            bytesOut: data.bytesOut ?? Infinity,

            cpuMs: data.cpuMs ?? Infinity,
            wallMs: data.wallMs ?? Infinity,

            storageBytes:
                data.storageBytes ?? Infinity,

            proposals:
                data.proposals ?? Infinity,

            pages:
                data.pages ?? Infinity
        };
    }

    canReserve(cost) {
        return Object.entries(cost).every(
            ([key, value]) =>
                value <= this.limits[key]
        );
    }
}
