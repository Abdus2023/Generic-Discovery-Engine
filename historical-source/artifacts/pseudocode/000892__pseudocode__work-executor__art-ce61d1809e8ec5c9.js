class WorkExecutor {
    canExecute(work) {
        return false;
    }

    async execute(work, context) {
        throw new Error(
            'Not implemented'
        );
    }
}
