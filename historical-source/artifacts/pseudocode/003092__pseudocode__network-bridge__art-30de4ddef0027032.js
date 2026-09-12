    class NetworkBridge {
        constructor(engine) {
            this.engine =
                engine;

            this.install();
        }

        install() {
            if (
                !CONFIG.discoverNetwork
            ) {
                return;
            }

            window.addEventListener(
                'message',
                event => {
                    if (
                        event.source !==
                        window
                    ) {
                        return;
                    }

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

                    this.handle(
                        data
                    );
                }
            );

            const inject =
                () => {
                    try {
                        const script =
                            document.createElement(
                                'script'
                            );

                        script.textContent = `
                            (() => {
                                const SOURCE =
                                    ${JSON.stringify(
                                        NETWORK_SOURCE
                                    )};

                                const CHANNEL =
                                    ${JSON.stringify(
                                        NETWORK_CHANNEL
                                    )};

                                if (
                                    window.__GDE_NETWORK_BRIDGE__
                                ) {
                                    return;
                                }

                                window.__GDE_NETWORK_BRIDGE__ =
                                    true;

                                let sequence = 0;

                                const nextId = prefix =>
                                    prefix +
                                    '-' +
                                    Date.now() +
                                    '-' +
                                    (++sequence);

                                const emit = payload => {
                                    try {
                                        window.postMessage(
                                            {
                                                source:
                                                    SOURCE,

                                                channel:
                                                    CHANNEL,

                                                ...payload
                                            },
                                            '*'
                                        );
                                    } catch (_) {}
                                };

                                const resolveUrl =
                                    value => {
                                        try {
                                            if (
                                                value &&
                                                typeof value.url ===
                                                    'string'
                                            ) {
                                                value =
                                                    value.url;
                                            }

                                            if (
                                                typeof value !==
                                                'string'
                                            ) {
                                                return null;
                                            }

                                            return new URL(
                                                value,
                                                location.href
                                            ).href;
                                        } catch (_) {
                                            return null;
                                        }
                                    };

                                /*
                                 * fetch()
                                 */
                                try {
                                    const originalFetch =
                                        window.fetch;

                                    if (
                                        typeof originalFetch ===
                                        'function'
                                    ) {
                                        window.fetch =
                                            function(
                                                input,
                                                init
                                            ) {
                                                const requestId =
                                                    nextId(
                                                        'fetch'
                                                    );

                                                const url =
                                                    resolveUrl(
                                                        input
                                                    );

                                                let method =
                                                    init &&
                                                    init.method;

                                                if (
                                                    !method &&
                                                    input &&
                                                    typeof input.method ===
                                                        'string'
                                                ) {
                                                    method =
                                                        input.method;
                                                }

                                                method =
                                                    String(
                                                        method ||
                                                        'GET'
                                                    ).toUpperCase();

                                                emit({
                                                    phase:
                                                        'request',

                                                    requestId,

                                                    api:
                                                        'fetch',

                                                    url,

                                                    method,

                                                    timestamp:
                                                        Date.now()
                                                });

                                                let promise;

                                                try {
                                                    promise =
                                                        originalFetch.apply(
                                                            this,
                                                            arguments
                                                        );
                                                } catch (
                                                    error
                                                ) {
                                                    emit({
                                                        phase:
                                                            'error',

                                                        requestId,

                                                        api:
                                                            'fetch',

                                                        url,

                                                        method,

                                                        error:
                                                            String(
                                                                error
                                                            ),

                                                        timestamp:
                                                            Date.now()
                                                    });

                                                    throw error;
                                                }

                                                return promise.then(
                                                    response => {
                                                        let ct =
                                                            '';

                                                        try {
                                                            ct =
                                                                response.headers.get(
                                                                    'content-type'
                                                                ) ||
                                                                '';
                                                        } catch (_) {}

                                                        emit({
                                                            phase:
                                                                'response',

                                                            requestId,

                                                            api:
                                                                'fetch',

                                                            url,

                                                            finalUrl:
                                                                response.url ||
                                                                url,

                                                            method,

                                                            status:
                                                                response.status,

                                                            contentType:
                                                                ct,

                                                            timestamp:
                                                                Date.now()
                                                        });

                                                        return response;
                                                    },

                                                    error => {
                                                        emit({
                                                            phase:
                                                                'error',

                                                            requestId,

                                                            api:
                                                                'fetch',

                                                            url,

                                                            method,

                                                            error:
                                                                String(
                                                                    error
                                                                ),

                                                            timestamp:
                                                                Date.now()
                                                        });

                                                        throw error;
                                                    }
                                                );
                                            };
                                    }
                                } catch (_) {}

                                /*
                                 * XMLHttpRequest
                                 */
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
                                                this.__GDE =
                                                    {
                                                        method:
                                                            String(
                                                                method ||
                                                                'GET'
                                                            ).toUpperCase(),

                                                        url:
                                                            resolveUrl(
                                                                url
                                                            )
                                                    };

                                                return originalOpen.apply(
                                                    this,
                                                    arguments
                                                );
                                            };

                                        XHR.prototype.send =
                                            function() {
                                                const xhr =
                                                    this;

                                                const meta =
                                                    xhr.__GDE ||
                                                    {
                                                        method:
                                                            'GET',

                                                        url:
                                                            null
                                                    };

                                                const requestId =
                                                    nextId(
                                                        'xhr'
                                                    );

                                                emit({
                                                    phase:
                                                        'request',

                                                    requestId,

                                                    api:
                                                        'xhr',

                                                    url:
                                                        meta.url,

                                                    method:
                                                        meta.method,

                                                    timestamp:
                                                        Date.now()
                                                });

                                                try {
                                                    xhr.addEventListener(
                                                        'loadend',
                                                        () => {
                                                            let ct =
                                                                '';

                                                            try {
                                                                ct =
                                                                    xhr.getResponseHeader(
                                                                        'content-type'
                                                                    ) ||
                                                                    '';
                                                            } catch (_) {}

                                                            emit({
                                                                phase:
                                                                    'response',

                                                                requestId,

                                                                api:
                                                                    'xhr',

                                                                url:
                                                                    meta.url,

                                                                finalUrl:
                                                                    xhr.responseURL ||
                                                                    meta.url,

                                                                method:
                                                                    meta.method,

                                                                status:
                                                                    xhr.status,

                                                                contentType:
                                                                    ct,

                                                                timestamp:
                                                                    Date.now()
                                                            });
                                                        },
                                                        {
                                                            once:
                                                                true
                                                        }
                                                    );
                                                } catch (_) {}

                                                return originalSend.apply(
                                                    this,
                                                    arguments
                                                );
                                            };
                                    }
                                } catch (_) {}

                                emit({
                                    phase:
                                        'installed',

                                    api:
                                        'bridge',

                                    timestamp:
                                        Date.now()
                                });
                            })();
                        `;

                        const root =
                            document.documentElement ||
                            document.head ||
                            document.body;

                        if (root) {
                            root.appendChild(
                                script
                            );

                            script.remove();
                        }
                    } catch (error) {
                        warn(
                            'Network bridge injection failed',
                            error
                        );
                    }
                };

            if (
                document.documentElement
            ) {
                inject();
            } else {
                setTimeout(
                    inject,
                    0
                );
            }
        }

        handle(data) {
            const url =
                canonicalizeUrl(
                    data.url
                );

            if (
                !url ||
                !allowed(url)
            ) {
                return;
            }

            const event =
                new NetworkEvent({
                    requestId:
                        data.requestId,

                    api:
                        data.api,

                    phase:
                        data.phase,

                    url,

                    finalUrl:
                        canonicalizeUrl(
                            data.finalUrl
                        ) || null,

                    method:
                        data.method,

                    status:
                        data.status,

                    contentType:
                        data.contentType,

                    error:
                        data.error,

                    timestamp:
                        data.timestamp ||
                        now()
                });

            this.engine
                .handleNetworkEvent(
                    event
                );
        }
    }
