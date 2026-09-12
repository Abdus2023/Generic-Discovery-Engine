class DiscoveryExecutor extends WorkExecutor {
    canExecute(work) {
        return work.kind === 'discovery';
    }

    async execute(work, context) {
        return context.discoveryController
            .executeTask(work);
    }
}
