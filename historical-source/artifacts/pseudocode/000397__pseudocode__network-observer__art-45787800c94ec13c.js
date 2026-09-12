    class NetworkObserver {
        constructor(engine) {
            this.engine = engine;
            this.started = false;
            this.performanceObserver = null;
        }

        start() {
            if (this.started) return;

            this.started = true;

            if (CONFIG.networkBridge) {
                this.installBridge();
            }

            if (
                CONFIG.discovery.performance &&
                typeof PerformanceObserver !==
                    'undefined'
            ) {
                this.installPerformanceObserver();
            }
        }

        installBridge() {
            try {
                const script =
                    document.createElement(
                        'script'
                    );

                script.textContent = `
(function () {
    if (window.__GDE_NETWORK_BRIDGE__) return;
    window.__GDE_NETWORK_BRIDGE__ = true;

    function emit(event) {
        window.postMessage({
            source: 'generic-discovery-engine',
            type: 'network',
            event: event
        }, '*');
    }

    const originalFetch = window.fetch;

    if (originalFetch) {
        window.fetch = async function (
            input,
            init
        ) {
            const requestAt =
                Date.now();

            const url =
                typeof input === 'string'
                    ? input
                    : input?.url;

            const method =
                String(
                    init?.method ||
                    input?.method ||
                    'GET'
                ).toUpperCase();

            const requestId =
                'fetch-' +
                requestAt +
                '-' +
                Math.random()
                    .toString(36)
                    .slice(2);

            emit({
                phase: 'request',
                api: 'fetch',
                requestId,
                method,
                url,
                requestAt
            });

            try {
                const response =
                    await originalFetch.apply(
                        this,
                        arguments
                    );

                emit({
                    phase: 'response',
                    api: 'fetch',
                    requestId,
                    method,
                    url,
                    finalUrl:
                        response.url,
                    status:
                        response.status,
                    contentType:
                        response.headers.get(
                            'content-type'
                        ) || '',
                    responseAt:
                        Date.now()
                });

                return response;
            } catch (error) {
                emit({
                    phase: 'error',
                    api: 'fetch',
                    requestId,
                    method,
                    url,
                    error:
                        String(error),
                    responseAt:
                        Date.now()
                });

                throw error;
            }
        };
    }

    const OriginalXHR =
        window.XMLHttpRequest;

    if (OriginalXHR) {
        const open =
            OriginalXHR.prototype.open;

        const send =
            OriginalXHR.prototype.send;

        OriginalXHR.prototype.open =
            function (
                method,
                url
            ) {
                this.__gde = {
                    method:
                        String(
                            method || 'GET'
                        ).toUpperCase(),
                    url,
                    requestId:
                        'xhr-' +
                        Date.now() +
                        '-' +
                        Math.random()
                            .toString(36)
                            .slice(2)
                };

                return open.apply(
                    this,
                    arguments
                );
            };

        OriginalXHR.prototype.send =
            function () {
                const meta =
                    this.__gde;

                if (meta) {
                    emit({
                        phase: 'request',
                        api: 'xhr',
                        requestId:
                            meta.requestId,
                        method:
                            meta.method,
                        url:
                            meta.url,
                        requestAt:
                            Date.now()
                    });

                    this.addEventListener(
                        'load',
                        function () {
                            emit({
                                phase:
                                    'response',
                                api: 'xhr',
                                requestId:
                                    meta.requestId,
                                method:
                                    meta.method,
                                url:
                                    meta.url,
                                finalUrl:
                                    this.responseURL ||
                                    meta.url,
                                status:
                                    this.status,
                                contentType:
                                    this.getResponseHeader(
                                        'content-type'
                                    ) || '',
                                responseAt:
                                    Date.now()
                            });
                        }
                    );

                    this.addEventListener(
                        'error',
                        function () {
                            emit({
                                phase:
                                    'error',
                                api: 'xhr',
                                requestId:
                                    meta.requestId,
                                method:
                                    meta.method,
                                url:
                                    meta.url,
                                error:
                                    'xhr-error',
                                responseAt:
                                    Date.now()
                            });
                        }
                    );
                }

                return send.apply(
                    this,
                    arguments
                );
            };
    }
})();
`;

                (
                    document.documentElement ||
                    document.head ||
                    document.body
                )?.appendChild(script);

                script.remove();

                window.addEventListener(
                    'message',
                    event => {
                        if (
                            event.source !== window
                        ) {
                            return;
                        }

                        if (
                            event.data?.source !==
                            'generic-discovery-engine'
                        ) {
                            return;
                        }

                        if (
                            event.data?.type !==
                            'network'
                        ) {
                            return;
                        }

                        this.handleBridgeEvent(
                            event.data.event
                        );
                    }
                );
            } catch (error) {
                this.engine.ledger
                    .recordDiagnostic(
                        'network-bridge-error',
                        {
                            error:
                                String(error)
                        }
                    );
            }
        }

        handleBridgeEvent(event) {
            if (!event) return;

            const key =
                event.requestId;

            if (!key) return;

            this.engine.networkEvents.set(
                key,
                {
                    id:
                        key,
                    requestId:
                        key,
                    api:
                        event.api,
                    method:
                        event.method,
                    url:
                        event.url,
                    finalUrl:
                        event.finalUrl ||
                        null,
                    status:
                        event.status ||
                        0,
                    contentType:
                        event.contentType ||
                        '',
                    requestAt:
                        event.requestAt ||
                        now(),
                    responseAt:
                        event.responseAt ||
                        null,
                    phase:
                        event.phase,
                    error:
                        event.error ||
                        null
                }
            );

            const networkEvent =
                this.engine.networkEvents.get(
                    key
                );

            if (
                networkEvent.phase ===
                    'response' &&
                networkEvent.method ===
                    'GET' &&
                networkEvent.url
            ) {
                this.engine.observeNetworkGet(
                    networkEvent
                );
            }
        }

        installPerformanceObserver() {
            try {
                this.performanceObserver =
                    new PerformanceObserver(
                        entries => {
                            for (
                                const entry of
                                entries.getEntries()
                            ) {
                                if (
                                    !entry.name
                                ) {
                                    continue;
                                }

                                const initiator =
                                    entry.initiatorType ||
                                    'unknown';

                                /*
                                 * We intentionally do NOT assume
                                 * fetch/xhr == GET here.
                                 *
                                 * They are evidence only unless
                                 * the bridge provides method data.
                                 */
                                const executableGetLike =
                                    ![
                                        'fetch',
                                        'xmlhttprequest'
                                    ].includes(
                                        initiator
                                    );

                                const event = {
                                    id:
                                        makeId(
                                            'perf'
                                        ),

                                    requestId:
                                        makeId(
                                            'perf-request'
                                        ),

                                    api:
                                        'performance',

                                    method:
                                        executableGetLike
                                            ? 'GET'
                                            : null,

                                    url:
                                        entry.name,

                                    finalUrl:
                                        entry.name,

                                    status:
                                        0,

                                    contentType:
                                        '',

                                    initiatorType:
                                        initiator,

                                    requestAt:
                                        now(),

                                    responseAt:
                                        now(),

                                    duration:
                                        entry.duration,

                                    phase:
                                        'performance'
                                };

                                this.engine.recordNetworkEvent(
                                    event
                                );

                                if (
                                    executableGetLike
                                ) {
                                    this.engine.observeNetworkGet(
                                        event
                                    );
                                }
                            }
                        }
                    );

                this.performanceObserver.observe({
                    entryTypes: ['resource']
                });
            } catch (error) {
                this.engine.ledger
                    .recordDiagnostic(
                        'performance-observer-error',
                        {
                            error:
                                String(error)
                        }
                    );
            }
        }
    }
