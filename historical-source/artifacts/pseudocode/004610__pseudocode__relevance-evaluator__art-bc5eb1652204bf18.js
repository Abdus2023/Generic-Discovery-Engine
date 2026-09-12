class RelevanceEvaluator {
    canEvaluate(goal, resource, context) {
        return false;
    }

    evaluate(goal, resource, context) {
        throw new Error('Not implemented');
    }

    describe() {
        return {
            id: 'unknown-relevance-evaluator',
            name: 'Unknown Relevance Evaluator'
        };
    }
}
