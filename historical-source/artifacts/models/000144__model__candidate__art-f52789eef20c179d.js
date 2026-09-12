    class Candidate {
        constructor({
            target,
            type = 'url',
            origin = 'unknown',
            priority = 0.5,
            parent = null,
            hints = {}
        }) {
            this.id = makeId('candidate');

            this.target = target;
            this.type = type;

            /*
             * Why was this candidate created?
             *
             * Examples:
             *   initial-page
             *   initial-dom
             *   html:<discovery-id>
             *   json:<discovery-id>
             */
            this.origin = origin;

            /*
             * Discovery from which this candidate originated.
             */
            this.parent = parent;

            this.priority = priority;
            this.hints = hints;

            this.createdAt = now();
            this.attempts = 0;

            /*
             * queued → claimed → completed / failed
             */
            this.status = 'queued';
        }

        key() {
            return `${this.type}:${this.target}`;
        }
    }
