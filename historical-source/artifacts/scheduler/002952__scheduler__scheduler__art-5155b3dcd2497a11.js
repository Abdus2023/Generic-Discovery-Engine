class Scheduler {

    constructor(database) {
        this.database = database;
    }

    add(candidate) {
        return this.database
            .addCandidate(candidate);
    }

    /*
     * Important:
     *
     * Do NOT implement this as:
     *
     *     candidate = next()
     *     await something
     *     markVisited(candidate)
     *
     * The candidate must be claimed synchronously before the
     * worker performs any asynchronous operation.
     */
    claim() {
        return this.database
            .claimNextCandidate();
    }

    complete(candidate) {
        this.database
            .completeCandidate(candidate);
    }

    fail(candidate, retry = false) {
        this.database
            .failCandidate(
                candidate,
                retry
            );
    }

    size() {
        return this.database
            .queueSize();
    }
}
