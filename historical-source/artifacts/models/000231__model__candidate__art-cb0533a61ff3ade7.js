    class Candidate {
        constructor(options) {
            this.id =
                id('candidate');

            this.target =
                options.target;

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
                now();

            this.attempts =
                0;

            this.status =
                'discovered';

            this.nextAttemptAt =
                now();

            this.lastError =
                null;
        }

        /*
         * v0.5 identity is the canonical target.
         *
         * Candidate type remains descriptive rather than
         * becoming part of resource identity.
         */
        key() {
            return this.target;
        }

        score() {
            let score =
                this.priority -
                this.depth *
                    CONFIG.priorityDepthPenalty;

            const hintType =
                String(
                    this.hints
                        ?.contentType ||
                        ''
                );

            if (
                isJson(hintType)
            ) {
                score += 0.12;
            }

            if (
                isHtml(hintType)
            ) {
                score += 0.08;
            }

            if (
                isCss(hintType) ||
                isJs(hintType)
            ) {
                score += 0.02;
            }

            if (
                this.type ===
                'api'
            ) {
                score += 0.08;
            }

            if (
                this.type ===
                'network'
            ) {
                score += 0.06;
            }

            return score;
        }
    }
