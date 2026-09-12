    class Acquisition {
        constructor(originController) {
            this.origins =
                originController;
        }

        async execute(plan, ledger) {
            const startedAt = now();

            ledger.recordRequestStarted(plan);

            const originGranted =
                await this.origins.acquire(
                    plan.origin
                );

            if (!originGranted) {
                const observation =
                    new Observation({
                        candidateId:
                            plan.candidateId,
                        planId: plan.id,
                        target: plan.target,
                        requestedUrl:
                            plan.target,
                        startedAt,
                        completedAt: now(),
                        status: 'skipped',
                        reason:
                            'origin-request-budget'
                    });

                ledger.recordRequestCompleted(
                    plan,
                    observation
                );

                return observation;
            }

            try {
                return await this.request(
                    plan,
                    startedAt,
                    ledger
                );
            } finally {
                this.origins.release(
                    plan.origin
                );
            }
        }

        async request(plan, startedAt, ledger) {
            if (
                typeof GM_xmlhttpRequest ===
                'function'
            ) {
                return new Promise(resolve => {
                    let finished = false;

                    const finish =
                        observation => {
                            if (finished) return;

                            finished = true;

                            ledger.recordRequestCompleted(
                                plan,
                                observation
                            );

                            resolve(observation);
                        };

                    const timeoutId =
                        setTimeout(() => {
                            finish(
                                new Observation({
                                    candidateId:
                                        plan.candidateId,
                                    planId: plan.id,
                                    target:
                                        plan.target,
                                    requestedUrl:
                                        plan.target,
                                    startedAt,
                                    completedAt:
                                        now(),
                                    status: 'timeout',
                                    reason:
                                        'request-timeout'
                                })
                            );
                        }, CONFIG.requestTimeout);

                    try {
                        GM_xmlhttpRequest({
                            method: plan.method,
                            url: plan.target,
                            timeout:
                                CONFIG.requestTimeout,

                            onload: response => {
                                clearTimeout(timeoutId);

                                let body =
                                    String(
                                        response.responseText ||
                                        ''
                                    );

                                let bodyTruncated =
                                    false;

                                if (
                                    body.length >
                                    CONFIG.maxBodyChars
                                ) {
                                    body =
                                        body.slice(
                                            0,
                                            CONFIG.maxBodyChars
                                        );

                                    bodyTruncated = true;
                                }

                                const observation =
                                    new Observation({
                                        candidateId:
                                            plan.candidateId,

                                        planId:
                                            plan.id,

                                        target:
                                            plan.target,

                                        requestedUrl:
                                            plan.target,

                                        startedAt,

                                        completedAt:
                                            now(),

                                        status:
                                            response.status >=
                                                200 &&
                                            response.status <
                                                400
                                                ? 'success'
                                                : 'http-error',

                                        http: {
                                            status:
                                                response.status,

                                            contentType:
                                                response.responseHeaders
                                                    ?.match(
                                                        /content-type:\s*([^\r\n]+)/i
                                                    )?.[1]
                                                    ?.trim() ||
                                                '',

                                            contentLength:
                                                response.responseHeaders
                                                    ?.match(
                                                        /content-length:\s*(\d+)/i
                                                    )?.[1] ||
                                                null,

                                            finalUrl:
                                                response.finalUrl ||
                                                plan.target
                                        },

                                        body,
                                        bodyTruncated,

                                        fingerprint:
                                            makeFingerprint(
                                                body
                                            )
                                    });

                                finish(observation);
                            },

                            ontimeout: () => {
                                clearTimeout(timeoutId);

                                finish(
                                    new Observation({
                                        candidateId:
                                            plan.candidateId,
                                        planId: plan.id,
                                        target: plan.target,
                                        requestedUrl:
                                            plan.target,
                                        startedAt,
                                        completedAt:
                                            now(),
                                        status: 'timeout',
                                        reason:
                                            'request-timeout'
                                    })
                                );
                            },

                            onerror: error => {
                                clearTimeout(timeoutId);

                                finish(
                                    new Observation({
                                        candidateId:
                                            plan.candidateId,
                                        planId: plan.id,
                                        target: plan.target,
                                        requestedUrl:
                                            plan.target,
                                        startedAt,
                                        completedAt:
                                            now(),
                                        status: 'error',
                                        reason:
                                            'request-error',
                                        errors: [
                                            String(
                                                error?.error ||
                                                'unknown-error'
                                            )
                                        ]
                                    })
                                );
                            }
                        });
                    } catch (error) {
                        clearTimeout(timeoutId);

                        finish(
                            new Observation({
                                candidateId:
                                    plan.candidateId,
                                planId: plan.id,
                                target: plan.target,
                                requestedUrl:
                                    plan.target,
                                startedAt,
                                completedAt:
                                    now(),
                                status: 'error',
                                reason:
                                    'request-exception',
                                errors: [
                                    String(error)
                                ]
                            })
                        );
                    }
                });
            }

            /*
             * Fetch fallback.
             *
             * IMPORTANT:
             * AbortController is used so a timeout does not leave
             * an uncontrolled fetch alive.
             */

            const controller =
                new AbortController();

            const timeoutId =
                setTimeout(
                    () => controller.abort(),
                    CONFIG.requestTimeout
                );

            try {
                const response =
                    await fetch(
                        plan.target,
                        {
                            method: plan.method,
                            credentials: 'same-origin',
                            redirect: 'follow',
                            signal:
                                controller.signal
                        }
                    );

                let body =
                    await response.text();

                let bodyTruncated = false;

                if (
                    body.length >
                    CONFIG.maxBodyChars
                ) {
                    body =
                        body.slice(
                            0,
                            CONFIG.maxBodyChars
                        );

                    bodyTruncated = true;
                }

                const observation =
                    new Observation({
                        candidateId:
                            plan.candidateId,

                        planId:
                            plan.id,

                        target:
                            plan.target,

                        requestedUrl:
                            plan.target,

                        startedAt,

                        completedAt:
                            now(),

                        status:
                            response.ok
                                ? 'success'
                                : 'http-error',

                        http: {
                            status:
                                response.status,

                            contentType:
                                response.headers.get(
                                    'content-type'
                                ) || '',

                            contentLength:
                                response.headers.get(
                                    'content-length'
                                ),

                            finalUrl:
                                response.url ||
                                plan.target
                        },

                        body,
                        bodyTruncated,

                        fingerprint:
                            makeFingerprint(body)
                    });

                ledger.recordRequestCompleted(
                    plan,
                    observation
                );

                return observation;
            } catch (error) {
                const observation =
                    new Observation({
                        candidateId:
                            plan.candidateId,
                        planId: plan.id,
                        target: plan.target,
                        requestedUrl:
                            plan.target,
                        startedAt,
                        completedAt: now(),
                        status:
                            error?.name ===
                            'AbortError'
                                ? 'timeout'
                                : 'error',
                        reason:
                            error?.name ===
                            'AbortError'
                                ? 'request-timeout'
                                : 'request-error',
                        errors: [
                            String(error)
                        ]
                    });

                ledger.recordRequestCompleted(
                    plan,
                    observation
                );

                return observation;
            } finally {
                clearTimeout(timeoutId);
            }
        }
    }
