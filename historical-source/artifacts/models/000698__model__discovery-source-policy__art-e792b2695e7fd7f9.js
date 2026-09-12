class DiscoverySourcePolicy {
    constructor(config = {}) {
        this.enabled =
            config.enabled !== false;

        this.maxDepth =
            config.maxDepth ?? 5;

        this.maxTasks =
            config.maxTasks ?? 1000;
    }

    allow(task) {
        if (!this.enabled) {
            return {
                allowed: false,
                reason: 'discovery-disabled'
            };
        }

        if (task.depth > this.maxDepth) {
            return {
                allowed: false,
                reason: 'discovery-depth-limit'
            };
        }

        return {
            allowed: true
        };
    }
}
