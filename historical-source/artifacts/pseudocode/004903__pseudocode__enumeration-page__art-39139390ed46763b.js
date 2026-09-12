class EnumerationPage {
    constructor(data = {}) {
        this.sequence = data.sequence ?? 0;

        this.entries = data.entries || [];

        this.cursorBefore = data.cursorBefore ?? null;
        this.cursorAfter = data.cursorAfter ?? null;

        this.hasMore = data.hasMore ?? null;

        this.total = Number.isFinite(data.total)
            ? data.total
            : null;

        this.status = data.status || 'partial';

        this.evidenceIds = data.evidenceIds || [];

        this.createdAt = data.createdAt || now();
    }

    serialize() {
        return { ...this };
    }
}
