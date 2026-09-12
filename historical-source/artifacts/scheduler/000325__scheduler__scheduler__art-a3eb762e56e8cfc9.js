    class Scheduler {
        constructor(engine) {
            this.engine =
                engine;
        }

        next() {
            return this.engine.database
                .claimNextCandidate();
        }

        delay() {
            return this.engine.database
                .nextReadyDelay();
        }

        async waitForGlobalSlot() {
            while (
                this.engine.running &&
                !this.engine.stopRequested
            ) {
                if (
                    this.engine.paused
                ) {
                    await sleep(100);
                    continue;
                }

                if (
                    this.engine.inFlight <
                    this.engine.currentConcurrency
                ) {
                    return true;
                }

                await sleep(25);
            }

            return false;
        }
    }
