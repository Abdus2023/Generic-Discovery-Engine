select(observation) {
    return this.providers
        .filter(provider => {
            try {
                return provider.canRecognize(observation);
            } catch (_) {
                return false;
            }
        })
        .sort(
            (a, b) =>
                b.priority() - a.priority()
        )[0] || null;
}
