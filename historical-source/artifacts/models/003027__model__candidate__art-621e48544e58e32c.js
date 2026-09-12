    class Candidate {
        constructor({
            target,
            type = 'url',
            origin = 'unknown',
            priority = 0.5,
            parent = null,
            hints = {},
            depth = 0
        }) {
            this.id =
                makeId('candidate');

            this.target =
                target;

            this.type =
                type;

            this.origin =
                origin;

            this.parent =
                parent;

            this.priority =
                priority;

            this.hints =
                hints;

            this.depth =
                Math.max(
                    0,
                    Number(depth) || 0
                );

            this.createdAt =
                now();

            this.attempts =
                0;

            this.status =
                'queued';

            this.nextAttemptAt =
                now();
        }

        key() {
            return (
                `${this.type}:${this.target}`
            );
        }

        effectivePriority() {
            return (
                this.priority -
                this.depth *
                    CONFIG.priorityDepthPenalty
            );
        }
    }
