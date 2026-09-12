class Classifier {
    priority() {
        return 0;
    }

    canClassify(context) {
        return false;
    }

    classify(context) {
        return [];
    }

    describe() {
        return {
            id: 'unknown-classifier',
            name: 'Unknown Classifier'
        };
    }
}
