class RecognitionProvider {
    canRecognize(observation) {
        return false;
    }

    recognize(observation) {
        return [];
    }

    describe() {
        return {
            id: 'unknown',
            name: 'Unknown Recognition Provider'
        };
    }
}
