class ClassificationRuntime {
    constructor(classifiers = []) {
        this.classifiers = classifiers;
    }

    async classify(resource, context) {
        const assertions = [];

        for (const classifier of this.classifiers) {
            if (!classifier.canClassify({
                resource,
                context
            })) {
                continue;
            }

            const results = await classifier.classify({
                resource,
                context
            });

            assertions.push(...results);
        }

        return assertions;
    }
}
