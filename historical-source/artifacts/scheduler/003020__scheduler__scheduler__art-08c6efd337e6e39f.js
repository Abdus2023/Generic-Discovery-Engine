    class Scheduler {

        constructor(database) {
            this.database =
                database;
        }

        add(candidate) {
            return this.database
                .addCandidate(
                    candidate
                );
        }

        claim() {
            return this.database
                .claimNextCandidate();
        }

        complete(candidate) {
            this.database
                .completeCandidate(
                    candidate
                );
        }

        fail(
            candidate,
            retry = false
        ) {
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

        inFlight() {
            return this.database
                .claimedSize();
        }
    }
