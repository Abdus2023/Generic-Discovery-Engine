    class Candidate {
        constructor(options) {
            this.id =
                options.id ||
                makeId('candidate');

            this.target =
                canonicalizeUrl(
                    options.target
                );

            this.type =
                options.type ||
                'resource';

            this.origin =
                options.origin ||
                'unknown';

            this.parent =
                options.parent ||
                null;

            this.priority =
                Number.isFinite(
                    options.priority
                )
                    ? options.priority
                    : 0.5;

            this.depth =
                Number.isFinite(
                    options.depth
                )
                    ? options.depth
                    : 0;

            this.hints =
                options.hints ||
                {};

            this.createdAt =
                options.createdAt ||
                now();

            this.attempts =
                options.attempts ||
                0;

            this.status =
                options.status ||
                'discovered';

            this.nextAttemptAt =
                options.nextAttemptAt ||
                now();

            this.lastError =
                options.lastError ||
                null;

            this.queuedAt =
                options.queuedAt ||
                null;

            this.claimedAt =
                options.claimedAt ||
                null;

            this.acquiringAt =
                options.acquiringAt ||
                null;

            this.observedAt =
                options.observedAt ||
                null;

            this.recognizedAt =
                options.recognizedAt ||
                null;

            this.expandedAt =
                options.expandedAt ||
                null;

            this.completedAt =
                options.completedAt ||
                null;

            this.failedAt =
                options.failedAt ||
                null;
        }

        key() {
            return this.target;
        }

        lifecycle(status) {
            this.status =
                status;

            const stamp =
                now();

            if (
                status ===
                'queued'
            ) {
                this.queuedAt =
                    stamp;
            } else if (
                status ===
                'claimed'
            ) {
                this.claimedAt =
                    stamp;
            } else if (
                status ===
                'acquiring'
            ) {
                this.acquiringAt =
                    stamp;
            } else if (
                status ===
                'observed'
            ) {
                this.observedAt =
                    stamp;
            } else if (
                status ===
                'recognized'
            ) {
                this.recognizedAt =
                    stamp;
            } else if (
                status ===
                'expanded'
            ) {
                this.expandedAt =
                    stamp;
            } else if (
                status ===
                'completed'
            ) {
                this.completedAt =
                    stamp;
            } else if (
                status ===
                'failed'
            ) {
                this.failedAt =
                    stamp;
            }
        }

        score() {
            let score =
                this.priority;

            score +=
                (
                    TYPE_PRIORITY[
                        this.type
                    ] ||
                    TYPE_PRIORITY.resource
                ) * 0.22;

            const confidence =
                Number(
                    this.hints
                        ?.confidence ||
                        0
                );

            score +=
                confidence *
                CONFIG.confidencePriorityBoost;

            score -=
                this.depth *
                CONFIG.priorityDepthPenalty;

            score -=
                this.attempts *
                CONFIG.retryPriorityPenalty;

            if (
                isJson(
                    this.hints
                        ?.contentType
                )
            ) {
                score +=
                    0.08;
            }

            return score;
        }
    }
