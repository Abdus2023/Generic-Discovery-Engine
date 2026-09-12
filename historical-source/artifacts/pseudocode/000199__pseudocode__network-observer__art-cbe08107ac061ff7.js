    class NetworkObserver {

        constructor(engine) {
            this.engine =
                engine;

            this.installed =
                false;

            this.channel =
                `generic-discovery-${makeId(
                    'channel'
                )}`;

            this.messageHandler =
                null;

            this.performanceObserver =
                null;
        }

        install() {
            if (
                this.installed
            ) {
                return;
            }

            this.installed =
                true;

            if (
                CONFIG.observeNetwork
            ) {
                this.installPageBridge();
                this.installMessageListener();
            }

            if (
                CONFIG.observePerformance
            ) {
                this.installPerformanceObserver();
            }

            log(
                'Passive network observation enabled'
            );
        }

        installMessageListener() {
            this.messageHandler =
                event => {
                    const data =
                        event.data;

                    if (
                        !data ||
                        data.source !==
                            'GenericDiscoveryNetwork' ||
                        data.channel !==
                            this.channel
                    ) {
                        return;
                    }

                    if (
                        !data.url
                    ) {
                        return;
                    }

                    this.engine
                        .recordPassiveNetwork(
                            {
                                url:
                                    data.url,

                                status:
                                    data.status ??
                                    null,

                                contentType:
                                    data.contentType ??
                                    null,

                                mechanism:
                                    data.mechanism ||
                                    'network'
                            }
                        );
                };

            window.addEventListener(
                'message',
                this.messageHandler
            );
        }

        installPageBridge() {
            /*
             * A userscript sandbox may not share the page's JavaScript
             * execution world. Inject a small page-context bridge so
             * page fetch/XHR activity can be observed.
             *
             * The bridge only reports metadata:
             *   URL
             *   status
             *   Content-Type
             *
             * It does NOT copy response bodies.
             */
            const nonce =
                this.channel;

            const source =
                `
                (() => {
                    const CHANNEL =
                        ${JSON.stringify(
                            nonce
                        )};

                    const SOURCE =
                        'GenericDiscoveryNetwork';

                    const emit = payload => {
                        try {
                            window.postMessage(
                                {
                                    source: SOURCE,
                                    channel: CHANNEL,
                                    ...payload
                                },
                                '*'
                            );
                        } catch {}
                    };

                    try {
                        if (
                            window.__GenericDiscoveryNetworkInstalled
                        ) {
                            return;
                        }

                        window.__GenericDiscoveryNetworkInstalled =
                            true;

                        /*
                         * -------------------------------------------------
                         * fetch()
                         * -------------------------------------------------
                         */

                        if (
                            typeof window.fetch ===
                            'function'
                        ) {
                            const originalFetch =
                                window.fetch;

                            window.fetch =
                                function(...args) {
                                    let requestedUrl =
                                        null;

                                    try {
                                        const input =
                                            args[0];

                                        if (
                                            typeof input ===
                                            'string'
                                        ) {
                                            requestedUrl =
                                                new URL(
                                                    input,
                                                    location.href
                                                ).href;
                                        } else if (
                                            input &&
                                            typeof input.url ===
                                                'string'
                                        ) {
                                            requestedUrl =
                                                new URL(
                                                    input.url,
                                                    location.href
                                                ).href;
                                        }
                                    } catch {}

                                    const promise =
                                        originalFetch.apply(
                                            this,
                                            args
                                        );

                                    if (
                                        requestedUrl
                                    ) {
                                        emit({
                                            mechanism:
                                                'fetch-request',

                                            url:
                                                requestedUrl
                                        });
                                    }

                                    Promise.resolve(
                                        promise
                                    )
                                        .then(
                                            response => {
                                                try {
                                                    emit({
                                                        mechanism:
                                                            'fetch-response',

                                                        url:
                                                            response.url ||
                                                            requestedUrl,

                                                        status:
                                                            response.status,

                                                        contentType:
                                                            response.headers?.get(
                                                                'content-type'
                                                            ) || ''
                                                    });
                                                } catch {}

                                                return response;
                                            }
                                        )
                                        .catch(
                                            () => {}
                                        );

                                    return promise;
                                };
                        }

                        /*
                         * -------------------------------------------------
                         * XMLHttpRequest
                         * -------------------------------------------------
                         */

                        if (
                            typeof XMLHttpRequest !==
                            'undefined'
                        ) {
                            const xhrOpen =
                                XMLHttpRequest
                                    .prototype
                                    .open;

                            const xhrSend =
                                XMLHttpRequest
                                    .prototype
                                    .send;

                            XMLHttpRequest
                                .prototype
                                .open =
                                function(
                                    method,
                                    url,
                                    ...rest
                                ) {
                                    try {
                                        this.__gdUrl =
                                            new URL(
                                                url,
                                                location.href
                                            ).href;

                                        this.__gdMethod =
                                            method;
                                    } catch {
                                        this.__gdUrl =
                                            null;
                                    }

                                    return xhrOpen.call(
                                        this,
                                        method,
                                        url,
                                        ...rest
                                    );
                                };

                            XMLHttpRequest
                                .prototype
                                .send =
                                function(...args) {
                                    const xhr =
                                        this;

                                    if (
                                        xhr.__gdUrl
                                    ) {
                                        emit({
                                            mechanism:
                                                'xhr-request',

                                            url:
                                                xhr.__gdUrl
                                        });

                                        xhr.addEventListener(
                                            'loadend',
                                            () => {
                                                try {
                                                    emit({
                                                        mechanism:
                                                            'xhr-response',

                                                        url:
                                                            xhr.responseURL ||
                                                            xhr.__gdUrl,

                                                        status:
                                                            xhr.status,

                                                        contentType:
                                                            xhr.getResponseHeader(
                                                                'content-type'
                                                            ) || ''
                                                    });
                                                } catch {}
                                            },
                                            {
                                                once:
                                                    true
                                            }
                                        );
                                    }

                                    return xhrSend.apply(
                                        this,
                                        args
                                    );
                                };
                        }
                    } catch {}
                })();
            `;

            try {
                const script =
                    document.createElement(
                        'script'
                    );

                script.textContent =
                    source;

                (
                    document.documentElement ||
                    document.head ||
                    document.body
                )?.appendChild(
                    script
                );

                script.remove();

                log(
                    'Page network bridge injected'
                );
            } catch (error) {
                warn(
                    'Page network bridge unavailable:',
                    error
                );
            }
        }

        installPerformanceObserver() {
            if (
                typeof PerformanceObserver ===
                'undefined'
            ) {
                return;
            }

            try {
                this.performanceObserver =
                    new PerformanceObserver(
                        list => {
                            for (
                                const entry of
                                list.getEntries()
                            ) {
                                if (
                                    entry &&
                                    entry.name
                                ) {
                                    this.engine
                                        .recordPassiveNetwork(
                                            {
                                                url:
                                                    entry.name,

                                                status:
                                                    null,

                                                contentType:
                                                    null,

                                                mechanism:
                                                    'performance-resource'
                                            }
                                        );
                                }
                            }
                        }
                    );

                this.performanceObserver
                    .observe({
                        type:
                            'resource',

                        buffered:
                            true
                    });

                log(
                    'PerformanceObserver installed'
                );
            } catch (error) {
                warn(
                    'PerformanceObserver unavailable:',
                    error
                );
            }
        }

        dispose() {
            if (
                this.messageHandler
            ) {
                window.removeEventListener(
                    'message',
                    this.messageHandler
                );

                this.messageHandler =
                    null;
            }

            try {
                this.performanceObserver
                    ?.disconnect();
            } catch {}

            this.performanceObserver =
                null;
        }
    }
