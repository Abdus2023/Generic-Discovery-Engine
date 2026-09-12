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
                makeId(
                    'candidate'
                );

            this.target =
                target;

            this.type =
                type;

            this.origin =
                origin;

            this.priority =
                clamp(
                    Number(priority) ||
                        0,
                    0,
                    1
                );

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
            /*
             * Type is intentionally NOT part of the primary fingerprint.
             *
             * /api/data discovered by HTML and /api/data discovered by
             * network observation are the same acquisition target.
             */
            return (
                `url:${this.target}`
            );
        }
    }
