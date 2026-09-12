class StateDigest {
    constructor(data = {}) {
        this.algorithm = data.algorithm || 'sha256';
        this.digest = data.digest || null;
        this.sequence = data.sequence ?? null;
        this.schemaVersion = data.schemaVersion || null;
    }
}
