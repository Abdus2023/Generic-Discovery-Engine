class DiscoveryEngine {

    constructor() {

        this.database =
            new KnowledgeBase();

        this.scheduler =
            new Scheduler(
                this.database
            );

        this.acquisition =
            new HttpAcquisitionAdapter();

        this.providers =
            new ProviderRegistry();

        this.running = false;

        this.stats = {
            startedAt: null,
            requests: 0,
            discoveries: 0,
            failures: 0,
            candidatesCreated: 0
        };
    }

    seed() {

        const current =
            canonicalizeUrl(
                location.href
            );

        if (current) {

            this.addCandidate(
                new Candidate({
                    target: current,
                    type: 'url',
                    origin: 'initial-page',
                    priority: 1.0
                })
            );
        }

        /*
         * Treat the already-loaded DOM as an initial observation.
         * This avoids requiring a network request just to discover
         * links already present on the page.
         */
        const initialLinks = [
            ...document.querySelectorAll(
                'a[href]'
            )
        ];

        for (
            const element of initialLinks
        ) {

            const url =
                canonicalizeUrl(
                    element.href
                );

            if (
                url &&
                isAllowedUrl(url)
            ) {

                this.addCandidate(
                    new Candidate({
                        target: url,
                        type: 'url',
                        origin: 'initial-dom',
                        priority: 0.7
                    })
                );
            }
        }
    }

    addCandidate(candidate) {

        const added =
            this.scheduler.add(
                candidate
            );

        if (added) {
            this.stats.candidatesCreated++;
        }

        return added;
    }

    async run() {

        if (this.running) {
            return;
        }

        this.running = true;

        this.stats.startedAt = now();

        log(
            'Starting discovery',
            {
                concurrency:
                    CONFIG.concurrency
            }
        );

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
    }

    async worker(workerId) {

        while (
            this.running &&
            this.stats.requests <
                CONFIG.maxRequests
        ) {

            /*
             * CLAIM FIRST.
             *
             * This operation is synchronous.
             * No await occurs before ownership is established.
             */
            const candidate =
                this.scheduler.claim();

            if (!candidate) {
                break;
            }

            this.stats.requests++;

            log(
                `Worker ${workerId} claimed`,
                candidate.target
            );

            try {

                const observation =
                    await this.acquisition
                        .acquire(candidate);

                this.database
                    .addObservation(
                        observation
                    );

                if (
                    observation.status !==
                    'acquired'
                ) {

                    this.stats.failures++;

                    this.scheduler.fail(
                        candidate,
                        false
                    );

                    continue;
                }

                const result =
                    this.providers.recognize(
                        candidate,
                        observation
                    );

                if (!result) {

                    this.scheduler.complete(
                        candidate
                    );

                    continue;
                }

                const {
                    provider,
                    discovery
                } = result;

                this.database
                    .addDiscovery(
                        discovery
                    );

                this.stats.discoveries++;

                log(
                    `Worker ${workerId} discovered`,
                    discovery.kind,
                    candidate.target
                );

                /*
                 * A provider can expand the search space.
                 */
                const newCandidates =
                    provider.candidates(
                        discovery
                    );

                for (
                    const next
                    of newCandidates
                ) {
                    this.addCandidate(next);
                }

                this.scheduler.complete(
                    candidate
                );

            } catch (error) {

                warn(
                    `Worker ${workerId} failed:`,
                    error
                );

                this.stats.failures++;

                this.scheduler.fail(
                    candidate,
                    false
                );
            }
        }
    }

    export() {

        return {
            version: 2,

            scope: {
                type:
                    'web-resource-discovery',

                inspiredBy:
                    'DVB blind-scan architecture',

                rfScanning:
                    false
            },

            timestamp:
                new Date().toISOString(),

            page:
                location.href,

            statistics:
                this.stats,

            discoveries: [
                ...this.database
                    .discoveries
                    .values()
            ]
        };
    }

    report() {

        const discoveries = [
            ...this.database
                .discoveries
                .values()
        ];

        console.group(
            '[Discovery] Results'
        );

        console.table(
            discoveries.map(
                discovery => ({
                    kind:
                        discovery.kind,

                    confidence:
                        discovery.confidence,

                    url:
                        discovery.data.url,

                    title:
                        discovery.data.title ||
                        ''
                })
            )
        );

        console.log(
            'Queue:',
            this.scheduler.size()
        );

        console.log(
            'In flight:',
            this.database.claimedSize()
        );

        console.log(
            'Statistics:',
            this.stats
        );

        console.groupEnd();
    }

    clear() {
        this.database.clear();
    }
}
