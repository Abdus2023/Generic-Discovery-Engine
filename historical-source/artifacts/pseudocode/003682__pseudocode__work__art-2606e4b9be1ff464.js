claim(workId, ownerId, leaseMs) {
    const work = this.items.get(workId);

    if (!work) {
        return null;
    }

    if (work.status !== 'queued') {
        return null;
    }

    work.status = 'claimed';
    work.claimedBy = ownerId;
    work.claimId = makeId('claim');
    work.claimedAt = now();
    work.leaseUntil =
        now() + leaseMs;

    return work;
}
