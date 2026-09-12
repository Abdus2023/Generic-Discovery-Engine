class CandidateSourceRegistry {
    constructor() {
        this.sources = [];
    }

    register(source) {
        this.sources.push(source);
        return this;
    }

    get(id) {
        return this.sources.find(
            source => source.describe().id === id
        ) || null;
    }

    describe() {
        return this.sources.map(
            source => source.describe()
        );
    }
}
