    class HttpAcquisition {
        acquire(url) {
            if (
                typeof GM_xmlhttpRequest ===
                'function'
            ) {
                return this.gmRequest(
                    url
                );
            }

            return this.fetchRequest(
                url
            );
        }

        gmRequest(url) {
            return new Promise(
                (resolve, reject) => {
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
                        method:
                            'GET',

                        url,

                        timeout:
                            CONFIG.requestTimeout,

                        responseType:
                            'text',

                        onload:
                            response => {
                                const headers =
                                    String(
                                        response
                                            .responseHeaders ||
                                            ''
                                    );

                                const ct =
                                    headers.match(
                                        /^content-type:\s*([^\r\n]+)/im
                                    );

                                const length =
                                    headers.match(
                                        /^content-length:\s*(\d+)/im
                                    );

                                finish(
                                    resolve,
                                    {
                                        status:
                                            response.status,

                                        contentType:
                                            ct
                                                ? ct[1]
                                                : '',

                                        contentLength:
                                            length
                                                ? Number(
                                                      length[1]
                                                  )
                                                : null,

                                        body:
                                            response
                                                .responseText ||
                                            '',

                                        finalUrl:
                                            response
                                                .finalUrl ||
                                            url
                                    }
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
                }
            );
        }

        async fetchRequest(url) {
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
                        ) || '',

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
