class DiscoveryEngine {

    constructor() {

        this.database =
            new KnowledgeBase();

        this.scheduler =
            new Scheduler(this.database);

        this.acquisition =
            new HttpAcquisitionAdapter();

        this.recognizer =
            new HtmlRecognizer();

        this.extractor =
            new CandidateExtractor();

        this.running = false;

        this.stats = {
            startedAt: null,
            requests: 0,
            candidates: 0,
            discoveries: 0,
            failures: 0
        };
    }

    seed() {

        const current =
            canonicalizeUrl(
                location.href
            );

        if (current) {

            this.scheduler.add(
                new Candidate({
                    target: current,
                    type: 'url',
                    origin: 'initial-page',
                    priority: 1.0
                })
            );
        }

        // Discover what is already present in the page.
        const candidates =
            this.extractor.fromDocument(
                document,
                'initial-dom'
            );

        for (const candidate of candidates) {
            this.scheduler.add(candidate);
        }

        this.stats.candidates =
            this.scheduler.size();
    }

    async run() {

        if (this.running) {
            return;
        }

        this.running = true;

        this.stats.startedAt = now();

        log('Starting discovery');

        const workers = [];

        for (
            let i = 0;
            i < CONFIG.concurrency;
            i++
        ) {
            workers.push(
                this.worker(i)
            );
        }

        await Promise.all(workers);

        this.running = false;

        log(
            'Discovery complete',
            this.stats
        );

        this.report();
    }

    async worker(id) {

        while (
            this.running &&
            this.stats.requests <
                CONFIG.maxRequests
        ) {

            const candidate =
                this.scheduler.next();

            if (!candidate) {
                break;
            }

            this.database.markVisited(
                candidate
            );

            log(
                `Worker ${id}:`,
                candidate.target
            );

            this.stats.requests++;

            const observation =
                await this.acquisition.acquire(
                    candidate
                );

            this.database.addObservation(
                observation
            );

            if (
                observation.status !==
                'acquired'
            ) {
                this.stats.failures++;
                continue;
            }

            const discovery =
                this.recognizer.recognize(
                    candidate,
                    observation
                );

            if (!discovery) {
                continue;
            }

            this.database.addDiscovery(
                discovery
            );

            this.stats.discoveries++;

            // Discovery expands the search space.
            const newCandidates =
                this.extractor
                    .fromDiscovery(
                        discovery
                    );

            for (const next of newCandidates) {
                this.scheduler.add(next);
            }
        }
    }

    report() {

        const discoveries =
            [...this.database.discoveries.values()];

        console.group(
            '[Discovery] Results'
        );

        console.table(
            discoveries.map(d => ({
                kind: d.kind,
                confidence: d.confidence,
                url: d.data.url,
                title: d.data.title
            }))
        );

        console.log(
            'Statistics:',
            this.stats
        );

        console.groupEnd();
    }

    export() {

        return {
            version: 1,

            timestamp:
                new Date().toISOString(),

            page:
                location.href,

            statistics:
                this.stats,

            discoveries:
                [...this.database
                    .discoveries
                    .values()]
        };
    }

    clear() {
        this.database.clear();
    }
}
