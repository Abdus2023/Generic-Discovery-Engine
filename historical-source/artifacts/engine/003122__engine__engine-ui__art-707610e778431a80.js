    class EngineUI {
        constructor(engine) {
            this.engine = engine;

            this.panel = null;
            this.status = null;

            this.scanButton = null;
            this.clearButton = null;
            this.exportButton = null;

            this.timer = null;
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
                'width:310px',
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
                'Generic Discovery Engine v0.5';

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
                'display:flex;gap:6px';

            const buttonStyle = [
                'flex:1',
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

            scan.textContent = 'Scan';
            scan.style.cssText =
                buttonStyle;

            const clear =
                document.createElement(
                    'button'
                );

            clear.textContent = 'Clear';
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

            this.panel = panel;
            this.status = status;

            this.scanButton = scan;
            this.clearButton = clear;
            this.exportButton =
                exportButton;

            this.update();

            this.timer =
                setInterval(
                    () => this.update(),
                    500
                );
        }

        update() {
            if (!this.status) {
                return;
            }

            const report =
                this.engine.report();

            const nextDelay =
                this.engine.scheduler.delay();

            this.status.textContent = [
                `state: ${report.running ? 'scanning' : 'idle'}`,
                `queue: ${report.queue}`,
                `claimed: ${report.claimed}`,
                `in-flight: ${report.inFlight}`,
                `resources: ${report.resources}`,
                `observations: ${report.observations}`,
                `discoveries: ${report.discoveries}`,
                `network: ${report.networkEvents}`,
                `requests: ${report.requests}/${report.maxRequests}`,
                `retries: ${report.retries}`,
                `failures: ${report.failures}`,
                `cache skips: ${report.cacheSkips}`,
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

                anchor.href = url;

                anchor.download =
                    `generic-discovery-${Date.now()}.json`;

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
