    class NetworkBridge {
        constructor(engine) {
            this.engine =
                engine;

            this.seen =
                new Set();

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

                        const resolveUrl = value => {
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
                            if (
                                typeof window.fetch ===
                                'function'
                            ) {
                                const originalFetch =
                                    window.fetch;

                                window.fetch =
                                    function(
                                        input,
                                        init
                                    ) {
                                        const url =
                                            resolveUrl(
                                                input
                                            );

                                        const method =
                                            (
                                                init &&
                                                init.method
                                            ) ||
                                            'GET';

                                        emit({
                                            phase:
                                                'request',

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
                                                originalFetch
                                                    .apply(
                                                        this,
                                                        arguments
                                                    );
                                        } catch (
                                            error
                                        ) {
                                            emit({
                                                phase:
                                                    'error',

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

                                                    api:
                                                        'fetch',

                                                    url:
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
                                const open =
                                    XHR.prototype.open;

                                const send =
                                    XHR.prototype.send;

                                XHR.prototype.open =
                                    function(
                                        method,
                                        url
                                    ) {
                                        try {
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
                                        } catch (_) {
                                            this.__GDE =
                                                {
                                                    method:
                                                        'GET',

                                                    url:
                                                        null
                                                };
                                        }

                                        return open.apply(
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

                                        emit({
                                            phase:
                                                'request',

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

                                                        api:
                                                            'xhr',

                                                        url:
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

                                        return send.apply(
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
        }

        handle(data) {
            if (
                data.phase ===
                'installed'
            ) {
                return;
            }

            const url =
                canonicalizeUrl(
                    data.url,
                    location.href
                );

            if (
                !url ||
                !allowed(url)
            ) {
                return;
            }

            const event =
                new NetworkEvent({
                    url,

                    api:
                        data.api,

                    phase:
                        data.phase,

                    method:
                        data.method,

                    status:
                        data.status,

                    contentType:
                        data.contentType
                });

            this.engine.recordNetwork(
                event
            );
        }
    }
