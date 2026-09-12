class HttpAcquisitionAdapter {

    async acquire(candidate) {

        const observation =
            new Observation(candidate);

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
                response.body?.length || 0;

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

                    GM_xmlhttpRequest({

                        method: 'GET',

                        url,

                        timeout:
                            CONFIG.requestTimeout,

                        onload: response => {

                            const contentType =
                                response
                                    .responseHeaders
                                    ?.match(
                                        /content-type:\s*([^\r\n]+)/i
                                    )?.[1] ||
                                null;

                            resolve({
                                status:
                                    response.status,

                                contentType,

                                body:
                                    response.responseText
                            });
                        },

                        onerror: () =>
                            reject(
                                new Error(
                                    'request failed'
                                )
                            ),

                        ontimeout: () =>
                            reject(
                                new Error(
                                    'request timeout'
                                )
                            )
                    });

                    return;
                }

                fetch(url, {
                    credentials:
                        'same-origin',

                    signal:
                        AbortSignal.timeout(
                            CONFIG.requestTimeout
                        )
                })
                    .then(async response => ({
                        status:
                            response.status,

                        contentType:
                            response.headers
                                .get(
                                    'content-type'
                                ),

                        body:
                            await response.text()
                    }))
                    .then(resolve)
                    .catch(reject);
            }
        );
    }
}
