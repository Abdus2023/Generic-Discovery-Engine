class EnumerationContract {
    constructor(data = {}) {
        this.id = data.id || makeId('enum');

        this.enumeratorType = data.enumeratorType || 'unknown';

        this.scope = data.scope || null;

        this.completeByDefinition =
            Boolean(data.completeByDefinition);

        this.supportsPagination =
            Boolean(data.supportsPagination);

        this.supportsCursor =
            Boolean(data.supportsCursor);

        this.version = data.version || null;

        this.evidenceIds = data.evidenceIds || [];
    }
}
