class WorkerIdentity {
    constructor(data = {}) {
        this.id =
            data.id || makeId('worker');

        this.runtimeId =
            data.runtimeId || null;

        this.contextType =
            data.contextType || 'browser-tab';

        this.instanceId =
            data.instanceId || null;

        this.startedAt =
            data.startedAt || now();

        this.lastHeartbeatAt =
            data.lastHeartbeatAt || null;
    }

    serialize() {
        return { ...this };
    }
}
