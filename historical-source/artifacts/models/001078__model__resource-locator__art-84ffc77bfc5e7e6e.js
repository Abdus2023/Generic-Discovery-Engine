class ResourceLocator {
    constructor(data = {}) {
        this.id =
            data.id || makeId('locator');

        this.target =
            data.target || '';

        this.canonicalTarget =
            data.canonicalTarget ||
            data.target ||
            '';

        this.scheme =
            data.scheme || null;

        this.origin =
            data.origin || null;

        this.type =
            data.type || 'unknown';

        this.createdAt =
            data.createdAt || now();
    }
}
