class DiscoveryController {
    constructor(options = {}) {
        this.registry =
            options.registry;

        this.policy =
            options.policy;

        this.scheduler =
            options.scheduler;

        this.normalizer =
            options.normalizer;

        this.database =
            options.database;
    }

    schedule(observation, context) {
        // Determine eligible sources.
        // Create DiscoveryTasks.
    }

    async execute(task) {
        // Claim.
        // Policy.
        // Execute source.
        // Normalize proposals.
        // Commit candidates.
    }
}
