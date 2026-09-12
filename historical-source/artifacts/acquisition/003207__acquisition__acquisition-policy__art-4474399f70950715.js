    class AcquisitionPolicy {
        plan(candidate) {
            const method =
                String(
                    candidate.hints?.method ||
                    'GET'
                ).toUpperCase();

            const base = {
                candidateId: candidate.id,
                target: candidate.target,
                method,
                priority:
                    candidate.effectivePriority(),
                origin: candidate.origin,
                expectedType: candidate.type,
                policyInputs: {
                    candidateType: candidate.type,
                    hints: {
                        ...candidate.hints
                    }
                }
            };

            if (!isAllowedUrl(candidate.target)) {
                return new AcquisitionPlan({
                    ...base,
                    allowed: false,
                    reason: 'url-not-allowed'
                });
            }

            if (method !== 'GET') {
                return new AcquisitionPlan({
                    ...base,
                    allowed: false,
                    reason: 'non-get-method'
                });
            }

            if (
                candidate.depth >
                CONFIG.maxDepth
            ) {
                return new AcquisitionPlan({
                    ...base,
                    allowed: false,
                    reason: 'max-depth'
                });
            }

            if (
                candidate.type === 'form' &&
                !CONFIG.policy.acquireForms
            ) {
                return new AcquisitionPlan({
                    ...base,
                    allowed: false,
                    reason: 'forms-disabled'
                });
            }

            if (
                candidate.type === 'media' &&
                !CONFIG.policy.acquireMedia
            ) {
                return new AcquisitionPlan({
                    ...base,
                    allowed: false,
                    reason: 'media-disabled'
                });
            }

            if (
                candidate.type === 'frame' &&
                !CONFIG.policy.acquireFrames
            ) {
                return new AcquisitionPlan({
                    ...base,
                    allowed: false,
                    reason: 'frames-disabled'
                });
            }

            if (
                candidate.type === 'stylesheet' &&
                !CONFIG.policy.acquireStylesheets
            ) {
                return new AcquisitionPlan({
                    ...base,
                    allowed: false,
                    reason: 'stylesheets-disabled'
                });
            }

            if (
                candidate.type === 'script' &&
                !CONFIG.policy.acquireScripts
            ) {
                return new AcquisitionPlan({
                    ...base,
                    allowed: false,
                    reason: 'scripts-disabled'
                });
            }

            if (
                candidate.type === 'network' &&
                !CONFIG.policy.acquireNetworkGet
            ) {
                return new AcquisitionPlan({
                    ...base,
                    allowed: false,
                    reason: 'network-get-disabled'
                });
            }

            if (
                candidate.hints?.binary &&
                !CONFIG.policy.acquireBinaryResources
            ) {
                return new AcquisitionPlan({
                    ...base,
                    allowed: false,
                    reason: 'binary-disabled'
                });
            }

            return new AcquisitionPlan({
                ...base,
                allowed: true,
                reason: null
            });
        }
    }
