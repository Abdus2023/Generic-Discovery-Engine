    class Candidate {
        constructor(data = {}) {
            this.id = data.id || makeId('cand');
            this.target = canonicalizeUrl(data.target) || data.target;
            this.type = data.type || 'url';

            this.origin = data.origin || location.href;
            this.parent = data.parent || null;

            this.priority = Number.isFinite(data.priority)
                ? data.priority
                : 0.5;

            this.hints = {
                ...(data.hints || {})
            };

            this.depth = Number.isFinite(data.depth)
                ? data.depth
                : 0;

            this.createdAt = data.createdAt || now();

            this.attempts = data.attempts || 0;
            this.status = data.status || 'discovered';
            this.nextAttemptAt = data.nextAttemptAt || 0;

            this.discoveredAt = data.discoveredAt || this.createdAt;
            this.queuedAt = data.queuedAt || null;
            this.claimedAt = data.claimedAt || null;
            this.acquiringAt = data.acquiringAt || null;
            this.observedAt = data.observedAt || null;
            this.recognizedAt = data.recognizedAt || null;
            this.expandedAt = data.expandedAt || null;
            this.completedAt = data.completedAt || null;
            this.failedAt = data.failedAt || null;

            this.alternateTypes = new Set(
                safeArray(data.alternateTypes)
            );

            this.alternateOrigins = new Set(
                safeArray(data.alternateOrigins)
            );

            this.alternateParents = new Set(
                safeArray(data.alternateParents)
            );
        }

        key() {
            return `${this.type}:${this.target}`;
        }

        effectivePriority() {
            const typeBoost = CONFIG.typePriority[this.type] || 0;

            const confidence = Number(this.hints.confidence || 0);

            const retryPenalty =
                this.attempts * CONFIG.retry.retryBaseDelay *
                CONFIG.retryPriorityPenalty;

            return (
                this.priority +
                typeBoost * 0.20 +
                confidence * CONFIG.confidencePriorityBoost -
                this.depth * CONFIG.priorityDepthPenalty -
                retryPenalty
            );
        }

        mark(status) {
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

        serialize() {
            return {
                id: this.id,
                target: this.target,
                type: this.type,
                origin: this.origin,
                parent: this.parent,
                priority: this.priority,
                hints: this.hints,
                depth: this.depth,
                createdAt: this.createdAt,
                attempts: this.attempts,
                status: this.status,
                nextAttemptAt: this.nextAttemptAt,
                discoveredAt: this.discoveredAt,
                queuedAt: this.queuedAt,
                claimedAt: this.claimedAt,
                acquiringAt: this.acquiringAt,
                observedAt: this.observedAt,
                recognizedAt: this.recognizedAt,
                expandedAt: this.expandedAt,
                completedAt: this.completedAt,
                failedAt: this.failedAt,
                alternateTypes: [...this.alternateTypes],
                alternateOrigins: [...this.alternateOrigins],
                alternateParents: [...this.alternateParents]
            };
        }
    }
