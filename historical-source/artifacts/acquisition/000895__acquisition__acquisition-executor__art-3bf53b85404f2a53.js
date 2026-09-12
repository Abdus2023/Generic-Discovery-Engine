class AcquisitionExecutor extends WorkExecutor {
    canExecute(work) {
        return work.kind === 'acquisition';
    }

    async execute(work, context) {
        return context.acquisitionRuntime
            .executeWork(work);
    }
}
