    class Candidate {
        constructor(data = {}) {
            this.id =
                data.id || makeId('candidate');

            this.target =
                canonicalizeUrl(data.target) ||
                data.target ||
                '';

            this.type =
                data.type || 'unknown';

            this.origin =
                data.origin ||
                originOf(this.target);

            this.parent =
                data.parent || null;

            this.priority =
                Number.isFinite(data.priority)
                    ? data.priority
                    : 0;

            this.hints =
                data.hints || {};

            this.depth =
                Number.isFinite(data.depth)
                    ? data.depth
                    : 0;

            this.createdAt =
                data.createdAt || now();

            this.attempts =
                Number.isFinite(data.attempts)
                    ? data.attempts
                    : 0;

            this.status =
                data.status || 'discovered';

            this.nextAttemptAt =
                data.nextAttemptAt || 0;

            this.discoveredAt =
                data.discoveredAt || now();

            this.queuedAt =
                data.queuedAt || null;

            this.claimedAt =
                data.claimedAt || null;

            this.plannedAt =
                data.plannedAt || null;

            this.acquiringAt =
                data.acquiringAt || null;

            this.observedAt =
                data.observedAt || null;

            this.recognizedAt =
                data.recognizedAt || null;

            this.expandedAt =
                data.expandedAt || null;

            this.completedAt =
                data.completedAt || null;

            this.failedAt =
                data.failedAt || null;

            this.skippedAt =
                data.skippedAt || null;

            this.alternateTypes =
                safeArray(data.alternateTypes);

            this.alternateOrigins =
                safeArray(data.alternateOrigins);

            this.alternateParents =
                safeArray(data.alternateParents);
        }

        identityKey() {
            return `${this.type}:${this.target}`;
        }

        effectivePriority() {
            const typeWeight =
                CONFIG.typePriority[this.type] ??
                CONFIG.typePriority.unknown;

            const confidence =
                Number(this.hints.confidence || 0);

            const retryPenalty =
                this.attempts *
                CONFIG.priority.retryPenalty;

            return (
                this.priority +
                typeWeight * 0.20 +
                confidence *
                    CONFIG.priority.confidenceBoost -
                this.depth *
                    CONFIG.priority.depthPenalty -
                retryPenalty
            );
        }

        serialize() {
            return {
                ...this,
                alternateTypes:
                    [...this.alternateTypes],
                alternateOrigins:
                    [...this.alternateOrigins],
                alternateParents:
                    [...this.alternateParents]
            };
        }
    }
