function agingScore(work, nowMs) {
    if (!work.queuedAt) return 0;

    const waited = Math.max(
        0,
        nowMs - work.queuedAt
    );

    return Math.min(
        1,
        waited / 30000
    );
}
