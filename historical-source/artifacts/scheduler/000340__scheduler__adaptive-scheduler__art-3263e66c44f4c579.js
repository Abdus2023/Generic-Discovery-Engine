    class AdaptiveScheduler {
        constructor() {
            this.configuredConcurrency =
                CONFIG.concurrency;

            this.currentConcurrency =
                CONFIG.concurrency;

            this.consecutiveFailures = 0;
            this.consecutiveSuccesses = 0;
        }

        async waitForGlobalSlot() {
            while (
                engine.inFlight >=
                this.currentConcurrency
            ) {
                if (engine.stopRequested) {
                    return false;
                }

                await sleep(50);
            }

            return !engine.stopRequested;
        }

        recordSuccess() {
            if (!CONFIG.adaptive.enabled) {
                return;
            }

            this.consecutiveFailures = 0;
            this.consecutiveSuccesses++;

            if (
                this.consecutiveSuccesses >=
                CONFIG.adaptive.successThreshold
            ) {
                this.consecutiveSuccesses = 0;

                if (
                    this.currentConcurrency <
                    this.configuredConcurrency
                ) {
                    this.currentConcurrency++;

                    engine.db.recordDiagnostic(
                        'concurrency-restore',
                        {
                            concurrency:
                                this.currentConcurrency
                        }
                    );
                }
            }
        }

        recordFailure() {
            if (!CONFIG.adaptive.enabled) {
                return;
            }

            this.consecutiveSuccesses = 0;
            this.consecutiveFailures++;

            if (
                this.consecutiveFailures >=
                CONFIG.adaptive.failureThreshold
            ) {
                this.consecutiveFailures = 0;

                if (
                    this.currentConcurrency >
                    CONFIG.adaptive.minimumConcurrency
                ) {
                    this.currentConcurrency--;

                    engine.db.recordDiagnostic(
                        'concurrency-reduce',
                        {
                            concurrency:
                                this.currentConcurrency
                        }
                    );
                }
            }
        }

        snapshot() {
            return {
                configuredConcurrency:
                    this.configuredConcurrency,

                currentConcurrency:
                    this.currentConcurrency,

                consecutiveFailures:
                    this.consecutiveFailures,

                consecutiveSuccesses:
                    this.consecutiveSuccesses
            };
        }
    }
