    class NetworkObserver {
        constructor(engine) {
            this.engine =
                engine;

            this.installed =
                false;

            this.performanceObserver =
                null;

            this.install();
        }

        install() {
            if (
                !CONFIG.discoverNetwork &&
                !CONFIG.discoverPerformance
            ) {
                return;
            }

            if (
                CONFIG.discoverNetwork &&
                CONFIG.networkBridge
            ) {
                this.installPageBridge();
            }

            if (
                CONFIG.discoverPerformance
            ) {
                this.installPerformanceObserver();
            }
        }

        installPageBridge() {
            try {
                const script =
                    document.createElement(
                        'script'
                    );

                script.textContent = `
                    (() => {
                        const CHANNEL = ${JSON.stringify(
                            NETWORK_CHANNEL
                        )};
                        const SOURCE = ${JSON.stringify(
                            NETWORK_SOURCE
                        )};

                        if (
                            window.__genericDiscoveryBridgeInstalled
                        ) {
                            return;
                        }

                        window.__genericDiscoveryBridgeInstalled = true;

                        const emit = detail => {
                            try {
                                window.postMessage(
                                    {
                                        source: SOURCE,
                                        channel: CHANNEL,
                                        ...detail
                                    },
                                    '*'
                                );
                            } catch (_) {}
                        };

                        const normalize = value => {
                            try {
                                if (
                                    typeof value === 'string'
                                ) {
                                    return value;
                                }

                                if (
                                    value &&
                                    typeof value.url === 'string'
                                ) {
                                    return value.url;
                                }
                            } catch (_) {}

                            return null;
                        };

                        try {
                            if (
                                typeof window.fetch ===
                                'function'
                            ) {
                                const originalFetch =
                                    window.fetch;

                                window.fetch =
                                    function(input, init) {
                                        const requestUrl =
                                            normalize(input);

                                        emit({
                                            event: 'request',
                                            api: 'fetch',
                                            url: requestUrl,
                                            time: Date.now()
                                        });

                                        return originalFetch
                                            .apply(this, arguments)
                                            .then(
                                                response => {
                                                    emit({
                                                        event: 'response',
                                                        api: 'fetch',
                                                        url:
                                                            response.url ||
                                                            requestUrl,
                                                        status:
                                                            response.status,
                                                        contentType:
                                                            (() => {
                                                                try {
                                                                    return response.headers.get(
                                                                        'content-type'
                                                                    );
                                                                } catch (_) {
                                                                    return null;
                                                                }
                                                            })(),
                                                        time: Date.now()
                                                    });

                                                    return response;
                                                },
                                                error => {
                                                    emit({
                                                        event: 'error',
                                                        api: 'fetch',
                                                        url: requestUrl,
                                                        error:
                                                            String(error),
                                                        time: Date.now()
                                                    });

                                                    throw error;
                                                }
                                            );
                                    };
                            }
                        } catch (_) {}

                        try {
                            const XHR =
                                window.XMLHttpRequest;

                            if (
                                XHR &&
                                XHR.prototype
                            ) {
                                const originalOpen =
                                    XHR.prototype.open;

                                const originalSend =
                                    XHR.prototype.send;

                                XHR.prototype.open =
                                    function(
                                        method,
                                        url
                                    ) {
                                        try {
                                            this.__gdMethod =
                                                method;

                                            this.__gdUrl =
                                                new URL(
                                                    url,
                                                    location.href
                                                ).href;
                                        } catch (_) {
                                            this.__gdUrl =
                                                String(url || '');
                                        }

                                        return originalOpen
                                            .apply(
                                                this,
                                                arguments
                                            );
                                    };

                                XHR.prototype.send =
                                    function() {
                                        const xhr =
                                            this;

                                        try {
                                            emit({
                                                event:
                                                    'request',
                                                api:
                                                    'xhr',
                                                method:
                                                    xhr.__gdMethod ||
                                                    null,
                                                url:
                                                    xhr.__gdUrl ||
                                                    null,
                                                time:
                                                    Date.now()
                                            });

                                            xhr.addEventListener(
                                                'loadend',
                                                () => {
                                                    emit({
                                                        event:
                                                            'response',
                                                        api:
                                                            'xhr',
                                                        method:
                                                            xhr.__gdMethod ||
                                                            null,
                                                        url:
                                                            xhr.responseURL ||
                                                            xhr.__gdUrl ||
                                                            null,
                                                        status:
                                                            xhr.status,
                                                        contentType:
                                                            xhr.getResponseHeader(
                                                                'content-type'
                                                            ),
                                                        time:
                                                            Date.now()
                                                    });
                                                },
                                                {
                                                    once:
                                                        true
                                                }
                                            );
                                        } catch (_) {}

                                        return originalSend
                                            .apply(
                                                this,
                                                arguments
                                            );
                                    };
                            }
                        } catch (_) {}

                        emit({
                            event: 'installed',
                            api: 'bridge',
                            time: Date.now()
                        });
                    })();
                `;

                (
                    document.documentElement ||
                    document.head ||
                    document.body
                )?.appendChild(
                    script
                );

                script.remove();

                this.installed =
                    true;

                log(
                    'Network page bridge installed'
                );
            } catch (error) {
                warn(
                    'Network bridge installation failed:',
                    error
                );
            }

            window.addEventListener(
                'message',
                this.handleMessage.bind(
                    this
                ),
                false
            );
        }

        handleMessage(event) {
            const data =
                event.data;

            if (
                !data ||
                data.source !==
                    NETWORK_SOURCE ||
                data.channel !==
                    NETWORK_CHANNEL
            ) {
                return;
            }

            if (
                data.event ===
                    'installed'
            ) {
                return;
            }

            if (
                !data.url
            ) {
                return;
            }

            this.engine.observeNetwork({
                url:
                    data.url,

                mechanism:
                    data.api ===
                        'xhr'
                        ? 'network-xhr'
                        : 'network-fetch',

                event:
                    data.event,

                status:
                    data.status ??
                    null,

                contentType:
                    data.contentType ??
                    null
            });
        }

        installPerformanceObserver() {
            const process =
                entries => {
                    for (
                        const entry of
                        entries
                    ) {
                        if (
                            !entry ||
                            !entry.name
                        ) {
                            continue;
                        }

                        this.engine.observeNetwork(
                            {
                                url:
                                    entry.name,

                                mechanism:
                                    'performance-resource',

                                event:
                                    'resource',

                                initiatorType:
                                    entry.initiatorType ||
                                    null
                            }
                        );
                    }
                };

            try {
                if (
                    typeof PerformanceObserver !==
                    'undefined'
                ) {
                    this.performanceObserver =
                        new PerformanceObserver(
                            list => {
                                process(
                                    list.getEntries()
                                );
                            }
                        );

                    this.performanceObserver.observe(
                        {
                            entryTypes: [
                                'resource'
                            ]
                        }
                    );
                }
            } catch (error) {
                warn(
                    'PerformanceObserver unavailable:',
                    error
                );
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
