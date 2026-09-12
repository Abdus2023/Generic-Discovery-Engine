recoverExpired(nowValue = now()) {
    for (const work of this.items.values()) {
        if (
            work.status === 'claimed' &&
            work.leaseUntil &&
            work.leaseUntil <= nowValue
        ) {
            work.status = 'queued';
            work.claimedBy = null;
            work.claimId = null;
            work.leaseUntil = null;
        }
    }
}
