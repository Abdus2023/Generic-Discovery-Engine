    class Candidate {
        constructor({
            target,
            type = 'url',
            origin = 'unknown',
            parent = null,
            priority = 0.5,
            hints = {},
            depth = 0
        }) {
            this.id = makeId('candidate');
            this.target = target;
            this.type = type;
            this.origin = origin;
            this.parent = parent;
            this.priority = clamp(Number(priority) || 0, 0, 1);
            this.hints = { ...hints };
            this.depth = Math.max(0, Number(depth) || 0);

            this.createdAt = now();
            this.attempts = 0;

            this.status = 'discovered';

            this.queuedAt = null;
            this.claimedAt = null;
            this.acquiringAt = null;
            this.observedAt = null;
            this.recognizedAt = null;
            this.expandedAt = null;
            this.completedAt = null;
            this.failedAt = null;

            this.nextAttemptAt = 0;

            this.alternateTypes = [];
            this.alternateOrigins = [];
            this.parents = parent ? [parent] : [];
        }

        key() {
            return `${this.type}:${this.target}`;
        }

        effectivePriority() {
            const typeBoost =
                CONFIG.typePriority[this.type] ??
                CONFIG.typePriority.resource;

            const confidence =
                Number(this.hints.confidence || 0);

            const retryPenalty =
                this.attempts * CONFIG.retryPriorityPenalty;

            return clamp(
                this.priority +
                typeBoost * 0.20 +
                confidence * CONFIG.confidencePriorityBoost -
                this.depth * CONFIG.priorityDepthPenalty -
                retryPenalty,
                0,
                1
            );
        }

        transition(status) {
            this.status = status;

            const timestamp = now();

            switch (status) {
                case 'queued':
                    this.queuedAt = timestamp;
                    break;
                case 'claimed':
                    this.claimedAt = timestamp;
                    break;
                case 'acquiring':
                    this.acquiringAt = timestamp;
                    break;
                case 'observed':
                    this.observedAt = timestamp;
                    break;
                case 'recognized':
                    this.recognizedAt = timestamp;
                    break;
                case 'expanded':
                    this.expandedAt = timestamp;
                    break;
                case 'completed':
                    this.completedAt = timestamp;
                    break;
                case 'failed':
                    this.failedAt = timestamp;
                    break;
            }
        }

        merge(other) {
            if (!other) {
                return;
            }

            this.alternateTypes = unique([
                ...this.alternateTypes,
                other.type,
                ...(other.alternateTypes || [])
            ]);

            this.alternateOrigins = unique([
                ...this.alternateOrigins,
                other.origin,
                ...(other.alternateOrigins || [])
            ]);

            this.parents = unique([
                ...this.parents,
                other.parent,
                ...(other.parents || [])
            ]);

            this.priority = Math.max(
                this.priority,
                Number(other.priority) || 0
            );

            this.depth = Math.min(
                this.depth,
                Number(other.depth) || 0
            );

            this.hints = {
                ...this.hints,
                ...other.hints
            };
        }
    }
