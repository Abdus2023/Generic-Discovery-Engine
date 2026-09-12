    class NetworkObserver {

        constructor(engine) {
            this.engine =
                engine;

            this.installed =
                false;

            this.originalFetch =
                null;

            this.originalOpen =
                null;

            this.originalSend =
                null;
        }

        install() {
            if (
                this.installed ||
                !CONFIG.observeNetwork
            ) {
                return;
            }

            this.installed =
                true;

            this.installFetchObserver();
            this.installXhrObserver();

            log(
                'Network observer installed'
            );
        }

        installFetchObserver() {
            if (
                typeof window.fetch !==
                'function'
            ) {
                return;
            }

            this.originalFetch =
                window.fetch;

            const engine =
                this.engine;

            window.fetch =
                function (...args) {
                    let url = null;

                    try {
                        const input =
                            args[0];

                        if (
                            typeof input ===
                            'string'
                        ) {
                            url =
                                canonicalizeUrl(
                                    input,
                                    location.href
                                );
                        } else if (
                            input &&
                            typeof input.url ===
                                'string'
                        ) {
                            url =
                                canonicalizeUrl(
                                    input.url,
                                    location.href
                                );
                        }
                    } catch {
                        url = null;
                    }

                    const promise =
                        engine.networkObserver
                            .originalFetch
                            .apply(
                                this,
                                args
                            );

                    if (url) {
                        promise
                            .then(response => {
                                engine.recordPassiveNetwork(
                                    {
                                        url,

                                        status:
                                            response.status,

                                        contentType:
                                            response
                                                .headers
                                                ?.get(
                                                    'content-type'
                                                ),

                                        mechanism:
                                            'fetch'
                                    }
                                );

                                return response;
                            })
                            .catch(() => {
                                /*
                                 * The request itself will have been
                                 * observed as attempted. No additional
                                 * action is required here.
                                 */
                            });
                    }

                    return promise;
                };
        }

        installXhrObserver() {
            if (
                typeof XMLHttpRequest ===
                'undefined'
            ) {
                return;
            }

            this.originalOpen =
                XMLHttpRequest.prototype.open;

            this.originalSend =
                XMLHttpRequest.prototype.send;

            const engine =
                this.engine;

            XMLHttpRequest.prototype.open =
                function (
                    method,
                    url,
                    ...rest
                ) {
                    try {
                        this.__gdUrl =
                            canonicalizeUrl(
                                url,
                                location.href
                            );

                        this.__gdMethod =
                            method;
                    } catch {
                        this.__gdUrl =
                            null;
                    }

                    return engine
                        .networkObserver
                        .originalOpen
                        .call(
                            this,
                            method,
                            url,
                            ...rest
                        );
                };

            XMLHttpRequest.prototype.send =
                function (...args) {
                    const xhr =
                        this;

                    if (
                        xhr.__gdUrl
                    ) {
                        xhr.addEventListener(
                            'load',
                            () => {
                                engine.recordPassiveNetwork(
                                    {
                                        url:
                                            xhr.__gdUrl,

                                        status:
                                            xhr.status,

                                        contentType:
                                            xhr.getResponseHeader(
                                                'content-type'
                                            ),

                                        mechanism:
                                            'xhr'
                                    }
                                );
                            },
                            {
                                once: true
                            }
                        );
                    }

                    return engine
                        .networkObserver
                        .originalSend
                        .apply(
                            this,
                            args
                        );
                };
        }
    }
