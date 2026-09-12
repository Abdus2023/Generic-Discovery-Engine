class Scheduler {
    constructor(database) {
        this.database = database;
    }

    add(candidate) {
        return this.database.addCandidate(candidate);
    }

    next() {
        const candidates = [
            ...this.database.candidates.values()
        ];

        if (!candidates.length) {
            return null;
        }

        // Highest priority first.
        candidates.sort((a, b) => {
            return b.priority - a.priority;
        });

        return candidates[0];
    }

    size() {
        return this.database.candidates.size;
    }
}
