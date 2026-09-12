class LeaseManager {
    constructor(data = {}) {
        this.durationMs =
            data.durationMs ?? 30000;

        this.renewalMarginMs =
            data.renewalMarginMs ?? 10000;
    }

    create(workItemId, workerId) {
        const nowMs = Date.now();

        return new ClaimToken({
            workItemId,
            workerId,
            claimedAt: nowMs,
            expiresAt:
                nowMs + this.durationMs
        });
    }

    isExpired(claim, nowMs = Date.now()) {
        return (
            claim.expiresAt !== null &&
            nowMs >= claim.expiresAt
        );
    }
}
