class WorkScheduler {
    constructor() {
        this.items = new Map();
    }

    enqueue(work) {
        this.items.set(work.id, work);
        return work;
    }

    eligible(nowValue = now()) {
        return [...this.items.values()]
            .filter(work =>
                work.status === 'queued' &&
                (
                    work.nextAttemptAt === null ||
                    work.nextAttemptAt <= nowValue
                )
            );
    }

    next(nowValue = now()) {
        return this.eligible(nowValue)
            .sort(
                (a, b) =>
                    b.priority - a.priority
            )[0] || null;
    }
}
