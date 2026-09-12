    class HttpAcquisitionAdapter {
        async acquire(candidate) {
            const started = now();

            const observation =
                new Observation({
                    candidateId: candidate.id,
                    target: candidate.target
                });

            observation.startedAt = started;

            try {
                const result =
                    typeof GM_xmlhttpRequest === 'function'
                        ? await this.acquireGM(candidate.target)
                        : await this.acquireFetch(candidate.target);

                observation.completedAt = now();

                observation.http.status =
                    result.status ?? null;

                observation.http.contentType =
                    normalizeContentType(
                        result.contentType || ''
                    );

                observation.http.contentLength =
                    result.contentLength ?? null;

                observation.http.finalUrl =
                    result.finalUrl ||
                    candidate.target;

                observation.body =
                    typeof result.body === 'string'
                        ? result.body
                        : '';

                observation.signalPresent = true;

                observation.status = 'acquired';

                observation.fingerprint =
                    makeFingerprint(observation);

                return observation;
            } catch (error) {
                observation.completedAt = now();

                observation.status = 'failed';

                observation.errors.push(
                    String(error?.message || error)
                );

                throw error;
            }
        }

        acquireGM(target) {
            return new Promise((resolve, reject) => {
                let settled = false;

                const finish = callback => value => {
                    if (settled) {
                        return;
                    }

                    settled = true;
                    callback(value);
                };

                const resolveOnce =
                    finish(resolve);

                const rejectOnce =
                    finish(reject);

                let timeoutId = null;

                try {
                    timeoutId = setTimeout(() => {
                        rejectOnce(
                            new Error('Request timeout')
                        );
                    }, CONFIG.requestTimeout);

                    GM_xmlhttpRequest({
                        method: 'GET',
                        url: target,

                        timeout: CONFIG.requestTimeout,

                        responseType: 'text',

                        onload: response => {
                            clearTimeout(timeoutId);

                            resolveOnce({
                                status: response.status,
                                contentType:
                                    response.responseHeaders
                                        ? this.header(
                                            response.responseHeaders,
                                            'content-type'
                                        )
                                        : '',

                                contentLength:
                                    response.responseHeaders
                                        ? this.header(
                                            response.responseHeaders,
                                            'content-length'
                                        )
                                        : null,

                                finalUrl:
                                    response.finalUrl ||
                                    target,

                                body:
                                    typeof response.responseText === 'string'
                                        ? response.responseText
                                        : ''
                            });
                        },

                        onerror: () => {
                            clearTimeout(timeoutId);
                            rejectOnce(
                                new Error('Network error')
                            );
                        },

                        ontimeout: () => {
                            clearTimeout(timeoutId);
                            rejectOnce(
                                new Error('Request timeout')
                            );
                        },

                        onabort: () => {
                            clearTimeout(timeoutId);
                            rejectOnce(
                                new Error('Request aborted')
                            );
                        }
                    });
                } catch (error) {
                    clearTimeout(timeoutId);
                    rejectOnce(error);
                }
            });
        }

        header(headers, name) {
            const wanted = name.toLowerCase();

            const lines =
                String(headers || '').split(/\r?\n/);

            for (const line of lines) {
                const index = line.indexOf(':');

                if (index < 0) {
                    continue;
                }

                const key =
                    line.slice(0, index)
                        .trim()
                        .toLowerCase();

                if (key === wanted) {
                    return line
                        .slice(index + 1)
                        .trim();
                }
            }

            return '';
        }

        async acquireFetch(target) {
            const controller =
                new AbortController();

            const timeout =
                setTimeout(
                    () => controller.abort(),
                    CONFIG.requestTimeout
                );

            try {
                const response =
                    await fetch(target, {
                        method: 'GET',
                        credentials: 'same-origin',
                        redirect: 'follow',
                        signal: controller.signal
                    });

                const body =
                    await response.text();

                return {
                    status: response.status,

                    contentType:
                        response.headers.get(
                            'content-type'
                        ) || '',

                    contentLength:
                        response.headers.get(
                            'content-length'
                        ),

                    finalUrl:
                        response.url || target,

                    body
                };
            } finally {
                clearTimeout(timeout);
            }
        }
    }
