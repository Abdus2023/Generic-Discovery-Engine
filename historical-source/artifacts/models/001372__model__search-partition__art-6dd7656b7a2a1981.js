class SearchPartition {
    constructor(data = {}) {
        this.id = data.id || makeId('partition');

        this.domainId =
            data.domainId || null;

        this.kind =
            data.kind || 'unknown';

        this.selector =
            data.selector || null;

        this.parentId =
            data.parentId || null;

        this.depth =
            Number.isFinite(data.depth)
                ? data.depth
                : 0;

        this.priority =
            Number.isFinite(data.priority)
                ? data.priority
                : 0;

        this.status =
            data.status || 'unexplored';

        this.createdAt =
            data.createdAt || now();
    }

    serialize() {
        return { ...this };
    }
}
