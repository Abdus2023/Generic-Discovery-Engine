class SearchGoal {
    constructor(data = {}) {
        this.id = data.id || makeId('goal');

        this.name = data.name || null;

        this.target = data.target || null;

        this.constraints = data.constraints || {};

        this.preferences = data.preferences || {};

        this.relevanceModelId =
            data.relevanceModelId || null;

        this.domainId =
            data.domainId || null;

        this.createdAt =
            data.createdAt || now();
    }

    serialize() {
        return { ...this };
    }
}
