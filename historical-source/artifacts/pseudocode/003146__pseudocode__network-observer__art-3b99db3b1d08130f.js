    class NetworkObserver {
        constructor(onEvent) {
            this.onEvent =
                onEvent;

            this.installed =
                false;

            this.performanceObserver =
                null;
        }

        install() {
            if (this.installed) {
                return;
            }

            this.installed =
                true;

            if (
                CONFIG.networkBridge
            ) {
                this.installPageBridge();
            }

            if (
                CONFIG.discoverPerformance
            ) {
                this.installPerformanceObserver();
            }

            window.addEventListener(
                'message',
                event => {
                    if (
                        event.source !==
                            window ||
                        !event.data ||
                        event.data.channel !==
                            NETWORK_CHANNEL
                    ) {
                        return;
                    }

                    this.onEvent({
                        ...event.data,

                        receivedAt:
                            now()
                    });
                }
            );
        }

        installPageBridge() {
            if (
                window
                    .__genericDiscoveryBridgeInstalled
            ) {
                return;
            }

            window
                .__genericDiscoveryBridgeInstalled =
                true;

            const bridge = `
                (() => {
                    'use strict';

                    if (
                        window.__genericDiscoveryBridgeActive
                    ) {
                        return;
                    }

                    window.__genericDiscoveryBridgeActive = true;

                    const CHANNEL =
                        ${JSON.stringify(
                            NETWORK_CHANNEL
                        )};

                    let counter = 0;

                    function nextId(prefix) {
                        counter++;

                        return (
                            prefix +
                            '-' +
                            Date.now().toString(36) +
                            '-' +
                            counter
                        );
                    }

                    function emit(data) {
                        try {
                            window.postMessage({
                                channel: CHANNEL,
                                source:
                                    'GenericDiscoveryNetworkBridge',
                                ...data
                            }, '*');
                        } catch (_) {}
                    }

                    function requestInfo(input, init) {
                        let url = '';

                        try {
                            if (
                                typeof input === 'string'
                            ) {
                                url = input;
                            } else if (
                                input &&
                                typeof input.url === 'string'
                            ) {
                                url = input.url;
                            }
                        } catch (_) {}

                        let method = '';

                        try {
                            if (
                                init &&
                                init.method
                            ) {
                                method = init.method;
                            } else if (
                                input &&
                                input.method
                            ) {
                                method = input.method;
                            }
                        } catch (_) {}

                        return {
                            url,
                            method:
                                String(
                                    method || 'GET'
                                ).toUpperCase()
                        };
                    }

                    if (
                        typeof window.fetch ===
                        'function'
                    ) {
                        const originalFetch =
                            window.fetch;

                        window.fetch =
                            function(input, init) {
                                const info =
                                    requestInfo(
                                        input,
                                        init
                                    );

                                const requestId =
                                    nextId(
                                        'fetch'
                                    );

                                const startedAt =
                                    Date.now();

                                emit({
                                    event:
                                        'request',

                                    api:
                                        'fetch',

                                    requestId,

                                    method:
                                        info.method,

                                    url:
                                        info.url,

                                    requestAt:
                                        startedAt
                                });

                                let result;

                                try {
                                    result =
                                        originalFetch.apply(
                                            this,
                                            arguments
                                        );
                                } catch (error) {
                                    emit({
                                        event:
                                            'error',

                                        api:
                                            'fetch',

                                        requestId,

                                        method:
                                            info.method,

                                        url:
                                            info.url,

                                        error:
                                            String(
                                                error?.message ||
                                                error
                                            ),

                                        responseAt:
                                            Date.now(),

                                        duration:
                                            Date.now() -
                                            startedAt
                                    });

                                    throw error;
                                }

                                return Promise
                                    .resolve(
                                        result
                                    )
                                    .then(
                                        response => {
                                            let contentType =
                                                '';

                                            try {
                                                contentType =
                                                    response
                                                        .headers
                                                        .get(
                                                            'content-type'
                                                        ) ||
                                                    '';
                                            } catch (_) {}

                                            emit({
                                                event:
                                                    'response',

                                                api:
                                                    'fetch',

                                                requestId,

                                                method:
                                                    info.method,

                                                url:
                                                    info.url,

                                                finalUrl:
                                                    response.url ||
                                                    info.url,

                                                status:
                                                    response.status,

                                                contentType,

                                                responseAt:
                                                    Date.now(),

                                                duration:
                                                    Date.now() -
                                                    startedAt
                                            });

                                            return response;
                                        }
                                    )
                                    .catch(
                                        error => {
                                            emit({
                                                event:
                                                    'error',

                                                api:
                                                    'fetch',

                                                requestId,

                                                method:
                                                    info.method,

                                                url:
                                                    info.url,

                                                error:
                                                    String(
                                                        error?.message ||
                                                        error
                                                    ),

                                                responseAt:
                                                    Date.now(),

                                                duration:
                                                    Date.now() -
                                                    startedAt
                                            });

                                            throw error;
                                        }
                                    );
                            };
                    }

                    try {
                        const XHR =
                            window.XMLHttpRequest;

                        const originalOpen =
                            XHR.prototype.open;

                        const originalSend =
                            XHR.prototype.send;

                        XHR.prototype.open =
                            function(method, url) {
                                this.__gdeMethod =
                                    String(
                                        method || 'GET'
                                    ).toUpperCase();

                                try {
                                    this.__gdeUrl =
                                        new URL(
                                            String(url),
                                            location.href
                                        ).href;
                                } catch (_) {
                                    this.__gdeUrl =
                                        String(url);
                                }

                                return originalOpen.apply(
                                    this,
                                    arguments
                                );
                            };

                        XHR.prototype.send =
                            function() {
                                const xhr = this;

                                const requestId =
                                    nextId('xhr');

                                const startedAt =
                                    Date.now();

                                xhr.__gdeRequestId =
                                    requestId;

                                emit({
                                    event:
                                        'request',

                                    api:
                                        'xhr',

                                    requestId,

                                    method:
                                        xhr.__gdeMethod ||
                                        'GET',

                                    url:
                                        xhr.__gdeUrl ||
                                        '',

                                    requestAt:
                                        startedAt
                                });

                                const finish =
                                    () => {
                                        let contentType =
                                            '';

                                        try {
                                            contentType =
                                                xhr.getResponseHeader(
                                                    'content-type'
                                                ) ||
                                                '';
                                        } catch (_) {}

                                        emit({
                                            event:
                                                'response',

                                            api:
                                                'xhr',

                                            requestId,

                                            method:
                                                xhr.__gdeMethod ||
                                                'GET',

                                            url:
                                                xhr.__gdeUrl ||
                                                '',

                                            finalUrl:
                                                xhr.responseURL ||
                                                xhr.__gdeUrl ||
                                                '',

                                            status:
                                                xhr.status,

                                            contentType,

                                            responseAt:
                                                Date.now(),

                                            duration:
                                                Date.now() -
                                                startedAt
                                        });
                                    };

                                try {
                                    xhr.addEventListener(
                                        'loadend',
                                        finish,
                                        {
                                            once: true
                                        }
                                    );
                                } catch (_) {
                                    try {
                                        xhr.addEventListener(
                                            'loadend',
                                            finish
                                        );
                                    } catch (_) {}
                                }

                                return originalSend.apply(
                                    this,
                                    arguments
                                );
                            };
                    } catch (_) {}

                })();
            `;

            try {
                const script =
                    document.createElement(
                        'script'
                    );

                script.textContent =
                    bridge;

                (
                    document.documentElement ||
                    document.head ||
                    document.body
                )?.appendChild(
                    script
                );

                script.remove();

                log(
                    'Network bridge installed'
                );
            } catch (error) {
                warn(
                    'Network bridge installation failed:',
                    error
                );
            }
        }

        installPerformanceObserver() {
            if (
                typeof PerformanceObserver !==
                'function'
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
                                this.onEvent({
                                    event:
                                        'performance',

                                    api:
                                        'performance',

                                    requestId:
                                        null,

                                    method:
                                        null,

                                    url:
                                        entry.name,

                                    finalUrl:
                                        entry.name,

                                    status:
                                        null,

                                    contentType:
                                        '',

                                    initiatorType:
                                        entry.initiatorType ||
                                        null,

                                    duration:
                                        entry.duration ??
                                        null,

                                    responseAt:
                                        now(),

                                    receivedAt:
                                        now()
                                });
                            }
                        }
                    );

                this.performanceObserver.observe({
                    type:
                        'resource',

                    buffered:
                        true
                });
            } catch (error) {
                warn(
                    'PerformanceObserver failed:',
                    error
                );
            }

            try {
                for (
                    const entry of
                    performance.getEntriesByType(
                        'resource'
                    )
                ) {
                    this.onEvent({
                        event:
                            'performance',

                        api:
                            'performance',

                        requestId:
                            null,

                        method:
                            null,

                        url:
                            entry.name,

                        finalUrl:
                            entry.name,

                        status:
                            null,

                        contentType:
                            '',

                        initiatorType:
                            entry.initiatorType ||
                            null,

                        duration:
                            entry.duration ??
                            null,

                        responseAt:
                            now(),

                        receivedAt:
                            now()
                    });
                }
            } catch (error) {
                warn(
                    'Existing performance entries failed:',
                    error
                );
            }
        }
    }
