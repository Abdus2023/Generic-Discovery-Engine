    class EngineUI {
        constructor(engine) {
            this.engine =
                engine;

            this.panel =
                null;

            this.status =
                null;

            this.scanButton =
                null;

            this.pauseButton =
                null;

            this.stopButton =
                null;

            this.clearButton =
                null;

            this.exportButton =
                null;

            this.timer =
                null;
        }

        install() {
            const create =
                () => this.create();

            if (document.body) {
                create();
            } else {
                document.addEventListener(
                    'DOMContentLoaded',
                    create,
                    {
                        once: true
                    }
                );
            }
        }

        create() {
            if (this.panel) {
                return;
            }

            const panel =
                document.createElement(
                    'div'
                );

            panel.id =
                'generic-discovery-engine';

            panel.style.cssText = [
                'position:fixed',
                'right:12px',
                'bottom:12px',
                'z-index:2147483647',
                'width:340px',
                'padding:12px',
                'background:#111',
                'color:#eee',
                'font:12px/1.4 monospace',
                'border:1px solid #555',
                'border-radius:8px',
                'box-shadow:0 4px 20px rgba(0,0,0,.45)'
            ].join(';');

            const title =
                document.createElement(
                    'div'
                );

            title.textContent =
                'Generic Discovery Engine v0.6';

            title.style.cssText =
                'font-weight:bold;margin-bottom:8px';

            const status =
                document.createElement(
                    'pre'
                );

            status.style.cssText =
                'margin:0 0 8px;white-space:pre-wrap';

            const controls =
                document.createElement(
                    'div'
                );

            controls.style.cssText =
                'display:grid;grid-template-columns:repeat(3,1fr);gap:6px';

            const buttonStyle = [
                'padding:5px',
                'background:#222',
                'color:#eee',
                'border:1px solid #555',
                'border-radius:4px',
                'cursor:pointer'
            ].join(';');

            const scan =
                document.createElement(
                    'button'
                );

            scan.textContent =
                'Scan';

            scan.style.cssText =
                buttonStyle;

            const pause =
                document.createElement(
                    'button'
                );

            pause.textContent =
                'Pause';

            pause.style.cssText =
                buttonStyle;

            const stop =
                document.createElement(
                    'button'
                );

            stop.textContent =
                'Stop';

            stop.style.cssText =
                buttonStyle;

            const clear =
                document.createElement(
                    'button'
                );

            clear.textContent =
                'Clear';

            clear.style.cssText =
                buttonStyle;

            const exportButton =
                document.createElement(
                    'button'
                );

            exportButton.textContent =
                'Export';

            exportButton.style.cssText =
                buttonStyle;

            scan.addEventListener(
                'click',
                async () => {
                    if (
                        this.engine.running
                    ) {
                        return;
                    }

                    this.engine.seed();

                    await this.engine.run();

                    this.update();
                }
            );

            pause.addEventListener(
                'click',
                () => {
                    if (
                        this.engine.paused
                    ) {
                        this.engine.resume();
                    } else {
                        this.engine.pause();
                    }

                    this.update();
                }
            );

            stop.addEventListener(
                'click',
                () => {
                    this.engine.stop();
                    this.update();
                }
            );

            clear.addEventListener(
                'click',
                () => {
                    this.engine.clear();
                    this.update();
                }
            );

            exportButton.addEventListener(
                'click',
                () => {
                    this.downloadExport();
                }
            );

            controls.append(
                scan,
                pause,
                stop,
                clear,
                exportButton
            );

            panel.append(
                title,
                status,
                controls
            );

            document.body.appendChild(
                panel
            );

            this.panel =
                panel;

            this.status =
                status;

            this.scanButton =
                scan;

            this.pauseButton =
                pause;

            this.stopButton =
                stop;

            this.clearButton =
                clear;

            this.exportButton =
                exportButton;

            this.update();

            this.timer =
                setInterval(
                    () => this.update(),
                    CONFIG.uiRefreshMs
                );
        }

        update() {
            if (!this.status) {
                return;
            }

            const report =
                this.engine.report();

            const nextDelay =
                this.engine.scheduler
                    .delay();

            let state =
                'idle';

            if (
                report.running &&
                report.paused
            ) {
                state =
                    'paused';
            } else if (
                report.running
            ) {
                state =
                    'scanning';
            } else if (
                report.stopRequested
            ) {
                state =
                    'stopped';
            }

            this.status.textContent = [
                `state: ${state}`,

                `queue: ${report.queue}`,

                `claimed: ${report.claimed}`,

                `in-flight: ${report.inFlight}`,

                `resources: ${report.resources}`,

                `observations: ${report.observations}`,

                `discoveries: ${report.discoveries}`,

                `network: ${report.networkEvents}`,

                `requests: ${report.requests}/${report.maxRequests}`,

                `concurrency: ${report.currentConcurrency}/${report.configuredConcurrency}`,

                `retries: ${report.retries}`,

                `failures: ${report.failures}`,

                `successes: ${report.successes}`,

                `policy skips: ${report.policySkips}`,

                `origin skips: ${report.originBudgetSkips}`,

                `duplicates: ${report.duplicateContent}`,

                `redirects: ${report.redirects}`,

                `created: ${report.candidatesCreated}`,

                `merged: ${report.candidatesMerged}`,

                `rejected: ${report.candidatesRejected}`,

                `depth-limit: ${report.maxDepthReached}`,

                `next delay: ${
                    nextDelay === null
                        ? '-'
                        : `${nextDelay}ms`
                }`
            ].join('\n');

            this.scanButton.disabled =
                report.running;

            this.pauseButton.disabled =
                !report.running;

            this.pauseButton.textContent =
                report.paused
                    ? 'Resume'
                    : 'Pause';

            this.stopButton.disabled =
                !report.running;
        }

        downloadExport() {
            try {
                const json =
                    this.engine.exportJson();

                const blob =
                    new Blob(
                        [json],
                        {
                            type:
                                'application/json'
                        }
                    );

                const url =
                    URL.createObjectURL(
                        blob
                    );

                const anchor =
                    document.createElement(
                        'a'
                    );

                anchor.href =
                    url;

                anchor.download =
                    `generic-discovery-v0.6-${Date.now()}.json`;

                document.body.appendChild(
                    anchor
                );

                anchor.click();

                anchor.remove();

                setTimeout(
                    () =>
                        URL.revokeObjectURL(
                            url
                        ),
                    1000
                );
            } catch (error) {
                warn(
                    'Export failed:',
                    error
                );
            }
        }
    }
