    class HttpAcquisitionAdapter {
        async acquire(candidate) {
            const observation =
                new Observation(
                    candidate
                );

            candidate.attempts++;

            try {
                const response =
                    await this.request(
                        candidate.target
                    );

                observation.signalPresent =
                    true;

                observation.http.status =
                    response.status;

                observation.http.contentType =
                    response.contentType;

                observation.http.contentLength =
                    response.contentLength ??
                    (
                        response.body
                            ? response.body.length
                            : 0
                    );

                observation.http.finalUrl =
                    response.finalUrl ||
                    candidate.target;

                observation.body =
                    response.body;

                observation.complete(
                    'acquired'
                );
            } catch (error) {
                observation.errors.push(
                    String(error)
                );

                observation.complete(
                    'failed'
                );
            }

            return observation;
        }

        request(url) {
            return new Promise(
                (resolve, reject) => {
                    if (
                        typeof GM_xmlhttpRequest ===
                        'function'
                    ) {
                        let settled =
                            false;

                        const finish = (
                            callback,
                            value
                        ) => {
                            if (
                                settled
                            ) {
                                return;
                            }

                            settled =
                                true;

                            callback(
                                value
                            );
                        };

                        GM_xmlhttpRequest({
                            method: 'GET',

                            url,

                            timeout:
                                CONFIG.requestTimeout,

                            responseType:
                                'text',

                            onload:
                                response => {
                                    const contentType =
                                        this.extractContentType(
                                            response.responseHeaders
                                        );

                                    const contentLength =
                                        this.extractContentLength(
                                            response.responseHeaders
                                        );

                                    finish(
                                        resolve,
                                        {
                                            status:
                                                response.status,

                                            contentType,

                                            contentLength,

                                            body:
                                                response.responseText ||
                                                '',

                                            finalUrl:
                                                response.finalUrl ||
                                                url
                                        }
                                    );
                                },

                            onerror:
                                () => {
                                    finish(
                                        reject,
                                        new Error(
                                            'request failed'
                                        )
                                    );
                                },

                            ontimeout:
                                () => {
                                    finish(
                                        reject,
                                        new Error(
                                            'request timeout'
                                        )
                                    );
                                },

                            onabort:
                                () => {
                                    finish(
                                        reject,
                                        new Error(
                                            'request aborted'
                                        )
                                    );
                                }
                        });

                        return;
                    }

                    const controller =
                        typeof AbortController !==
                        'undefined'
                            ? new AbortController()
                            : null;

                    let timer =
                        null;

                    if (
                        controller
                    ) {
                        timer =
                            setTimeout(
                                () => {
                                    controller.abort();
                                },
                                CONFIG.requestTimeout
                            );
                    }

                    fetch(url, {
                        method: 'GET',
                        credentials:
                            'same-origin',
                        signal:
                            controller
                                ? controller.signal
                                : undefined
                    })
                        .then(
                            async response => {
                                const body =
                                    await response.text();

                                return {
                                    status:
                                        response.status,

                                    contentType:
                                        response.headers.get(
                                            'content-type'
                                        ),

                                    contentLength:
                                        response.headers.get(
                                            'content-length'
                                        ),

                                    body,

                                    finalUrl:
                                        response.url ||
                                        url
                                };
                            }
                        )
                        .then(resolve)
                        .catch(error => {
                            if (
                                error &&
                                error.name ===
                                    'AbortError'
                            ) {
                                reject(
                                    new Error(
                                        'request timeout'
                                    )
                                );
                            } else {
                                reject(
                                    error
                                );
                            }
                        })
                        .finally(() => {
                            if (
                                timer
                            ) {
                                clearTimeout(
                                    timer
                                );
                            }
                        });
                }
            );
        }

        extractContentType(
            headers
        ) {
            if (!headers) {
                return '';
            }

            const match =
                String(headers).match(
                    /^content-type:\s*([^\r\n]+)/im
                );

            return match
                ? match[1].trim()
                : '';
        }

        extractContentLength(
            headers
        ) {
            if (!headers) {
                return null;
            }

            const match =
                String(headers).match(
                    /^content-length:\s*(\d+)/im
                );

            if (!match) {
                return null;
            }

            const value =
                Number(match[1]);

            return Number.isFinite(
                value
            )
                ? value
                : null;
        }
    }
