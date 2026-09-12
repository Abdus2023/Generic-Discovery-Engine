class CandidateNormalizer {
    constructor(config = {}) {
        this.config = config;
    }

    normalize(proposal) {
        if (!proposal || !proposal.target) {
            return {
                accepted: false,
                reason: 'empty-target'
            };
        }

        let target;

        try {
            target = canonicalizeUrl(
                proposal.target,
                proposal.parentTarget ||
                location.href
            );
        } catch (_) {
            return {
                accepted: false,
                reason: 'invalid-url'
            };
        }

        if (!target) {
            return {
                accepted: false,
                reason: 'invalid-target'
            };
        }

        if (!isAllowedUrl(target)) {
            return {
                accepted: false,
                reason: 'url-policy'
            };
        }

        return {
            accepted: true,
            candidate: {
                target,
                type: proposal.type || 'unknown',
                confidence:
                    proposal.confidence,
                hints: {
                    ...proposal.hints
                },
                sourceId:
                    proposal.sourceId,
                sourceObservationId:
                    proposal.sourceObservationId,
                parentTarget:
                    proposal.parentTarget
            }
        };
    }
}
