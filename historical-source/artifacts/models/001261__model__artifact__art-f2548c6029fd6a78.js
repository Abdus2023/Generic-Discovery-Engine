class Artifact {
    constructor(data = {}) {
        this.id = data.id || makeId('artifact');

        this.algorithm =
            data.algorithm || 'sha256';

        this.digest =
            data.digest || null;

        this.size =
            Number.isFinite(data.size)
                ? data.size
                : null;

        this.storage =
            data.storage || 'none';

        this.createdAt =
            data.createdAt || now();
    }
}
