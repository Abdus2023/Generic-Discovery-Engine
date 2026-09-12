    class Candidate {
        constructor({
            target,
            type = 'url',
            origin = 'unknown',
            priority = 0.5,
            parent = null,
            depth = 0,
            hints = {}
        }) {
            this.id =
                makeId('candidate');

            this.target =
                target;

            this.type =
                type;

            this.origin =
                origin;

            this.priority =
                priority;

            this.parent =
                parent;

            this.depth =
                depth;

            this.hints =
                hints;

            this.createdAt =
                now();

            this.attempts =
                0;

            this.status =
                'queued';

            this.nextAttemptAt =
                0;
        }

        key() {
            return (
                `${this.type}:${this.target}`
            );
        }
    }
