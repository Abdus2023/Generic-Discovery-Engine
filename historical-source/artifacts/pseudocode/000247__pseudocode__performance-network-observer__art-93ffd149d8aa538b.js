    class PerformanceNetworkObserver {
        constructor(engine) {
            this.engine =
                engine;

            this.seen =
                new Set();

            this.install();
        }

        install() {
            if (
                !CONFIG.discoverPerformance
            ) {
                return;
            }

            const process =
                entries => {
                    for (
                        const entry of
                        entries
                    ) {
                        const url =
                            canonicalizeUrl(
                                entry.name,
                                location.href
                            );

                        if (
                            !url ||
                            !allowed(url)
                        ) {
                            continue;
                        }

                        const key =
                            url;

                        if (
                            this.seen.has(
                                key
                            )
                        ) {
                            continue;
                        }

                        this.seen.add(
                            key
                        );

                        this.engine.recordNetwork(
                            new NetworkEvent({
                                url,

                                api:
                                    'performance',

                                phase:
                                    'resource',

                                initiatorType:
                                    entry.initiatorType ||
                                    null,

                                duration:
                                    entry.duration ||
                                    null
                            })
                        );
                    }
                };

            try {
                if (
                    typeof PerformanceObserver !==
                    'undefined'
                ) {
                    const observer =
                        new PerformanceObserver(
                            list =>
                                process(
                                    list.getEntries()
                                )
                        );

                    observer.observe({
                        entryTypes: [
                            'resource'
                        ]
                    });
                }
            } catch {
                // Ignore.
            }

            try {
                process(
                    performance.getEntriesByType(
                        'resource'
                    )
                );
            } catch {
                // Ignore.
            }
        }
    }
