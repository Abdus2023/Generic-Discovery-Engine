class ConflictContext {
    constructor(data = {}) {
        this.conflict = data.conflict;

        this.baseState = data.baseState;
        this.currentState = data.currentState;

        this.events = data.events || [];
        this.evidence = data.evidence || [];

        this.policy = data.policy;
        this.version = data.version;

        this.emitEvent = data.emitEvent;
    }
}
