class DiscoveryTask {
    constructor(data = {}) {
        this.id = data.id || makeId('dtask');

        this.sourceId =
            data.sourceId || null;

        this.observationId =
            data.observationId || null;

        this.parentCandidateId =
            data.parentCandidateId || null;

        this.priority =
            Number.isFinite(data.priority)
                ? data.priority
                : 0;

        this.depth =
            Number.isFinite(data.depth)
                ? data.depth
                : 0;

        this.status =
            data.status || 'queued';

        this.createdAt =
            data.createdAt || now();
    }

    serialize() {
        return { ...this };
    }
}
