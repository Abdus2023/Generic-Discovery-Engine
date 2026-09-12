effectivePriority(work, currentTime) {
    const waiting =
        Math.max(
            0,
            currentTime -
            (work.queuedAt || work.createdAt)
        );

    return (
        work.priority +
        waiting * 0.0001
    );
}
