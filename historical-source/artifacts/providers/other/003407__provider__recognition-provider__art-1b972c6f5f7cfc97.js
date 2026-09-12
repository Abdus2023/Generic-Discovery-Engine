class RecognitionProvider {
    priority() {
        return 0;
    }

    canRecognize(observation) {
        return false;
    }

    recognize(observation) {
        return [];
    }
}
