class CandidateProposal {
    constructor(data = {}) {
        this.target = data.target || '';
        this.type = data.type || 'unknown';

        this.confidence =
            Number.isFinite(data.confidence)
                ? data.confidence
                : 0.5;

        this.hints = {
            ...(data.hints || {})
        };

        this.sourceId =
            data.sourceId || null;

        this.sourceObservationId =
            data.sourceObservationId || null;

        this.parentTarget =
            data.parentTarget || null;

        this.createdAt =
            data.createdAt || Date.now();
    }

    serialize() {
        return {
            target: this.target,
            type: this.type,
            confidence: this.confidence,
            hints: this.hints,
            sourceId: this.sourceId,
            sourceObservationId:
                this.sourceObservationId,
            parentTarget:
                this.parentTarget,
            createdAt: this.createdAt
        };
    }
}
