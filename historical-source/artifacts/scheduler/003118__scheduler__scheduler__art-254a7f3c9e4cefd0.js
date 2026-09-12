    class Scheduler {
        constructor(database) {
            this.database = database;
        }

        add(candidate) {
            return this.database.addCandidate(
                candidate
            );
        }

        next() {
            return this.database.claimNextCandidate();
        }

        delay() {
            return this.database.nextReadyDelay();
        }
    }
