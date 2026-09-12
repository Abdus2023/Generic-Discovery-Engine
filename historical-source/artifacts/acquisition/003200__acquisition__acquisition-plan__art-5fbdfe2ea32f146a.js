    class AcquisitionPlan {
        constructor(data = {}) {
            this.id = data.id || makeId('plan');

            this.candidateId =
                data.candidateId || null;

            this.target =
                data.target || '';

            this.method =
                String(data.method || 'GET').toUpperCase();

            this.allowed =
                Boolean(data.allowed);

            this.reason =
                data.reason || null;

            this.priority =
                Number.isFinite(data.priority)
                    ? data.priority
                    : 0;

            this.origin =
                data.origin || originOf(this.target);

            this.expectedType =
                data.expectedType || 'unknown';

            this.requiresOriginSlot =
                data.requiresOriginSlot !== false;

            this.createdAt =
                data.createdAt || now();

            this.policyVersion =
                data.policyVersion || CONFIG.version;

            this.policyInputs =
                data.policyInputs || {};
        }

        serialize() {
            return {
                id: this.id,
                candidateId: this.candidateId,
                target: this.target,
                method: this.method,
                allowed: this.allowed,
                reason: this.reason,
                priority: this.priority,
                origin: this.origin,
                expectedType: this.expectedType,
                requiresOriginSlot: this.requiresOriginSlot,
                createdAt: this.createdAt,
                policyVersion: this.policyVersion,
                policyInputs: this.policyInputs
            };
        }
    }
