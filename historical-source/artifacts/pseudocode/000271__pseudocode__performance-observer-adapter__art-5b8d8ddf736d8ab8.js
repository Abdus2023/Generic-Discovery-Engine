    class PerformanceObserverAdapter {
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
                                entry.name
                            );

                        if (
                            !url ||
                            !allowed(url)
                        ) {
                            continue;
                        }

                        const key =
                            `${url}|${entry.initiatorType}`;

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

                        this.engine
                            .handleNetworkEvent(
                                new NetworkEvent({
                                    api:
                                        'performance',

                                    phase:
                                        'resource',

                                    url,

                                    initiatorType:
                                        entry.initiatorType,

                                    duration:
                                        entry.duration
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
                        entryTypes:
                            ['resource']
                    });
                }
            } catch {
                // Optional API.
            }

            try {
                process(
                    performance.getEntriesByType(
                        'resource'
                    )
                );
            } catch {
                // Optional API.
            }
        }
    }
