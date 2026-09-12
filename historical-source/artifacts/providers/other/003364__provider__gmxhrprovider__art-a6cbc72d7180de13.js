class GMXHRProvider {
    async execute(plan) {
        if (requestCount >= 150) return;
        if (originActive >= 2) return;
        await sleep(150);
        ...
    }
}
