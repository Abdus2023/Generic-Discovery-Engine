    class NetworkObserver {
        constructor() {
            this.started = false;
            this.requests = new Map();
            this.performanceObserver = null;
            this.messageHandler = null;
        }

        start() {
            if (this.started) {
                return;
            }

            this.started = true;

            this.installMessageListener();
            this.installPerformanceObserver();

            if (CONFIG.networkBridge) {
                this.installPageBridge();
            }
        }

        installMessageListener() {
            this.messageHandler =
                event => {
                    const data =
                        event.data;

                    if (
                        !data ||
                        data.channel !==
                        'gde-network'
                    ) {
                        return;
                    }

                    this.handleBridgeEvent(
                        data.payload
                    );
                };

            window.addEventListener(
                'message',
                this.messageHandler
            );
        }

        installPageBridge() {
            const code = `
                (() => {
                    if (window.__GDE_NETWORK_BRIDGE__) return;
                    window.__GDE_NETWORK_BRIDGE__ = true;

                    const channel = 'gde-network';

                    const emit = payload => {
                        try {
                            window.postMessage({
                                channel,
                                payload
                            }, '*');
                        } catch (_) {}
                    };

                    let sequence = 0;

                    const originalFetch = window.fetch;

                    if (originalFetch) {
                        window.fetch = function(input, init) {
                            const requestId =
                                'fetch-' + Date.now() + '-' + (++sequence);

                            let url = '';
                            let method = 'GET';

                            try {
                                if (typeof input === 'string') {
                                    url = input;
                                } else if (input && input.url) {
                                    url = input.url;
                                    method = input.method || method;
                                }

                                method =
                                    (init && init.method) ||
                                    method ||
                                    'GET';
                            } catch (_) {}

                            emit({
                                phase: 'request',
                                api: 'fetch',
                                requestId,
                                method: String(method).toUpperCase(),
                                url,
                                requestAt: Date.now()
                            });

                            return originalFetch.apply(this, arguments)
                                .then(response => {
                                    try {
                                        emit({
                                            phase: 'response',
                                            api: 'fetch',
                                            requestId,
                                            method: String(method).toUpperCase(),
                                            url,
                                            finalUrl: response.url || url,
                                            status: response.status,
                                            contentType:
                                                response.headers.get('content-type') || '',
                                            responseAt: Date.now()
                                        });
                                    } catch (_) {}

                                    return response;
                                })
                                .catch(error => {
                                    emit({
                                        phase: 'error',
                                        api: 'fetch',
                                        requestId,
                                        method: String(method).toUpperCase(),
                                        url,
                                        error: String(error),
                                        responseAt: Date.now()
                                    });

                                    throw error;
                                });
                        };
                    }

                    const OriginalXHR = XMLHttpRequest;

                    if (OriginalXHR && OriginalXHR.prototype) {
                        const originalOpen =
                            OriginalXHR.prototype.open;

                        const originalSend =
                            OriginalXHR.prototype.send;

                        OriginalXHR.prototype.open =
                            function(method, url) {
                                this.__GDE_METHOD__ =
                                    String(method || 'GET').toUpperCase();

                                this.__GDE_URL__ =
                                    String(url || '');

                                return originalOpen.apply(
                                    this,
                                    arguments
                                );
                            };

                        OriginalXHR.prototype.send =
                            function() {
                                const xhr = this;

                                const requestId =
                                    'xhr-' +
                                    Date.now() +
                                    '-' +
                                    (++sequence);

                                xhr.__GDE_REQUEST_ID__ =
                                    requestId;

                                emit({
                                    phase: 'request',
                                    api: 'xhr',
                                    requestId,
                                    method:
                                        xhr.__GDE_METHOD__ ||
                                        'GET',
                                    url:
                                        xhr.__GDE_URL__ ||
                                        '',
                                    requestAt: Date.now()
                                });

                                xhr.addEventListener(
                                    'loadend',
                                    function() {
                                        let contentType = '';

                                        try {
                                            contentType =
                                                xhr.getResponseHeader(
                                                    'content-type'
                                                ) || '';
                                        } catch (_) {}

                                        emit({
                                            phase: 'response',
                                            api: 'xhr',
                                            requestId,
                                            method:
                                                xhr.__GDE_METHOD__ ||
                                                'GET',
                                            url:
                                                xhr.__GDE_URL__ ||
                                                '',
                                            finalUrl:
                                                xhr.responseURL ||
                                                xhr.__GDE_URL__ ||
                                                '',
                                            status:
                                                xhr.status,
                                            contentType,
                                            responseAt:
                                                Date.now()
                                        });
                                    }
                                );

                                return originalSend.apply(
                                    this,
                                    arguments
                                );
                            };
                    }
                })();
            `;

            const script =
                document.createElement(
                    'script'
                );

            script.textContent = code;

            (
                document.documentElement ||
                document.head ||
                document.body
            )?.appendChild(script);

            script.remove();
        }

        handleBridgeEvent(payload) {
            if (!payload || !payload.url) {
                return;
            }

            const requestId =
                payload.requestId ||
                makeId('network');

            let event =
                this.requests.get(requestId);

            if (!event) {
                event =
                    new NetworkEvent({
                        ...payload,
                        id:
                            stableId(
                                'net',
                                requestId
                            )
                    });

                this.requests.set(
                    requestId,
                    event
                );
            } else {
                Object.assign(
                    event,
                    payload
                );
            }

            event.responseAt =
                payload.responseAt ||
                event.responseAt;

            if (
                event.responseAt &&
                event.requestAt
            ) {
                event.duration =
                    event.responseAt -
                    event.requestAt;
            }

            engine.db.addNetworkEvent(
                event
            );

            if (
                payload.phase ===
                    'response' &&
                String(
                    payload.method || 'GET'
                ).toUpperCase() === 'GET'
            ) {
                if (
                    CONFIG.policy.acquireNetworkGet
                ) {
                    engine.enqueue(
                        payload.url,
                        classifyNetworkType(
                            event
                        ),
                        {
                            mechanism:
                                `network:${payload.api}`,

                            confidence: 0.82,
                            contentType:
                                payload.contentType ||
                                ''
                        },
                        location.href,
                        1
                    );
                }

                if (
                    payload.finalUrl &&
                    payload.finalUrl !==
                    payload.url
                ) {
                    engine.db.recordRedirect(
                        canonicalizeUrl(
                            payload.url
                        ),
                        canonicalizeUrl(
                            payload.finalUrl
                        )
                    );
                }
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
                                this.handlePerformanceEntry(
                                    entry
                                );
                            }
                        }
                    );

                this.performanceObserver.observe({
                    entryTypes: ['resource']
                });

                for (
                    const entry of
                    performance.getEntriesByType(
                        'resource'
                    )
                ) {
                    this.handlePerformanceEntry(
                        entry
                    );
                }
            } catch (error) {
                warn(
                    'Performance observer unavailable',
                    error
                );
            }
        }

        handlePerformanceEntry(entry) {
            const url =
                canonicalizeUrl(
                    entry.name
                );

            if (!url || !isAllowedUrl(url)) {
                return;
            }

            const initiator =
                entry.initiatorType ||
                'resource';

            let type = 'resource';

            if (initiator === 'script') {
                type = 'script';
            } else if (
                initiator === 'link' ||
                initiator === 'css'
            ) {
                type = 'stylesheet';
            } else if (
                /img|image|video|audio/.test(
                    initiator
                )
            ) {
                type = 'media';
            } else if (
                /fetch|xmlhttprequest/.test(
                    initiator
                )
            ) {
                type = 'network';
            } else if (
                /iframe|frame/.test(
                    initiator
                )
            ) {
                type = 'frame';
            }

            const event =
                new NetworkEvent({
                    api: 'performance',
                    method: 'GET',
                    url,
                    finalUrl: url,
                    initiatorType: initiator,
                    requestAt:
                        now() -
                        Math.round(
                            entry.duration || 0
                        ),
                    responseAt: now(),
                    duration:
                        entry.duration || 0,
                    phase: 'response'
                });

            engine.db.addNetworkEvent(
                event
            );

            if (
                type === 'network' &&
                CONFIG.policy.acquireNetworkGet
            ) {
                engine.enqueue(
                    url,
                    type,
                    {
                        mechanism:
                            'performance-resource',

                        confidence: 0.68
                    },
                    location.href,
                    1
                );
            }
        }
    }
