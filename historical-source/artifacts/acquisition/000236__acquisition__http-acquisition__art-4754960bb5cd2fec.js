    class HttpAcquisition {
        async acquire(
            candidate
        ) {
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
                    contentType(
                        response.contentType
                    );

                observation.http.contentLength =
                    response.contentLength;

                observation.http.finalUrl =
                    canonicalizeUrl(
                        response.finalUrl ||
                            candidate.target
                    ) ||
                    candidate.target;

                observation.body =
                    response.body || '';

                observation.fingerprint
                    .length =
                    observation.body.length;

                observation.complete(
                    'observed'
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
            if (
                typeof GM_xmlhttpRequest ===
                'function'
            ) {
                return new Promise(
                    (resolve, reject) => {
                        let done =
                            false;

                        const finish =
                            (
                                callback,
                                value
                            ) => {
                                if (
                                    done
                                ) {
                                    return;
                                }

                                done =
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
                                    resolveResponse(
                                        response
                                    );
                                },

                            onerror:
                                () =>
                                    finish(
                                        reject,
                                        new Error(
                                            'request failed'
                                        )
                                    ),

                            ontimeout:
                                () =>
                                    finish(
                                        reject,
                                        new Error(
                                            'request timeout'
                                        )
                                    ),

                            onabort:
                                () =>
                                    finish(
                                        reject,
                                        new Error(
                                            'request aborted'
                                        )
                                    )
                        });

                        function resolveResponse(
                            response
                        ) {
                            const headers =
                                String(
                                    response.responseHeaders ||
                                        ''
                                );

                            const typeMatch =
                                headers.match(
                                    /^content-type:\s*([^\r\n]+)/im
                                );

                            const lengthMatch =
                                headers.match(
                                    /^content-length:\s*(\d+)/im
                                );

                            finish(
                                resolve,
                                {
                                    status:
                                        response.status,

                                    contentType:
                                        typeMatch
                                            ? typeMatch[1]
                                            : '',

                                    contentLength:
                                        lengthMatch
                                            ? Number(
                                                  lengthMatch[1]
                                              )
                                            : null,

                                    body:
                                        response.responseText ||
                                        '',

                                    finalUrl:
                                        response.finalUrl ||
                                        url
                                }
                            );
                        }
                    }
                );
            }

            const controller =
                typeof AbortController !==
                'undefined'
                    ? new AbortController()
                    : null;

            let timer;

            if (controller) {
                timer =
                    setTimeout(
                        () =>
                            controller.abort(),
                        CONFIG.requestTimeout
                    );
            }

            try {
                const response =
                    await fetch(
                        url,
                        {
                            method:
                                'GET',

                            credentials:
                                'same-origin',

                            signal:
                                controller
                                    ?.signal
                        }
                    );

                return {
                    status:
                        response.status,

                    contentType:
                        response.headers.get(
                            'content-type'
                        ),

                    contentLength:
                        Number(
                            response.headers.get(
                                'content-length'
                            )
                        ) || null,

                    body:
                        await response.text(),

                    finalUrl:
                        response.url ||
                        url
                };
            } finally {
                if (timer) {
                    clearTimeout(
                        timer
                    );
                }
            }
        }
    }
