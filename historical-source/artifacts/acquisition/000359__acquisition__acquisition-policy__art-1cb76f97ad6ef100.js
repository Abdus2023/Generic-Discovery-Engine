class AcquisitionPolicy {
    plan(candidate) {
        const method =
            String(
                candidate.hints.method || 'GET'
            ).toUpperCase();

        if (method !== 'GET') {
            return new AcquisitionPlan({
                candidateId: candidate.id,
                target: candidate.target,
                method,
                allowed: false,
                reason: 'non-get-method',
                priority: candidate.effectivePriority()
            });
        }

        if (candidate.type === 'form') {
            return new AcquisitionPlan({
                candidateId: candidate.id,
                target: candidate.target,
                method,
                allowed: false,
                reason: 'forms-disabled',
                priority: candidate.effectivePriority()
            });
        }

        if (
            candidate.type === 'media' &&
            !CONFIG.policy.acquireMedia
        ) {
            return new AcquisitionPlan({
                candidateId: candidate.id,
                target: candidate.target,
                method,
                allowed: false,
                reason: 'media-disabled',
                priority: candidate.effectivePriority()
            });
        }

        const contentType =
            candidate.hints.contentType ||
            contentTypeForTarget(candidate.target);

        if (
            isBinaryContentType(contentType) &&
            !CONFIG.policy.acquireBinaryResources
        ) {
            return new AcquisitionPlan({
                candidateId: candidate.id,
                target: candidate.target,
                method,
                allowed: false,
                reason: 'binary-disabled',
                priority: candidate.effectivePriority()
            });
        }

        return new AcquisitionPlan({
            candidateId: candidate.id,
            target: candidate.target,
            method: 'GET',
            allowed: true,
            priority: candidate.effectivePriority(),
            expectedType: candidate.type
        });
    }
}
