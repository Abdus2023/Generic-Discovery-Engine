class RecognitionRuntime {
    constructor(router, database) {
        this.router = router;
        this.database = database;
    }

    recognize(observation) {
        const provider =
            this.router.select(observation);

        if (!provider) {
            return {
                recognized: false,
                reason: 'no-recognizer'
            };
        }

        const result =
            provider.recognize(observation);

        return {
            recognized: true,
            providerId:
                provider.describe().id,
            result
        };
    }
}
