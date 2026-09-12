    // UI
    // =====================================================================

    function installUi() {
        document.getElementById(
            'generic-discovery-panel'
        )?.remove();

        const panel =
            document.createElement(
                'div'
            );

        panel.id =
            'generic-discovery-panel';

        panel.style.cssText = `
            position: fixed;
            right: 12px;
            bottom: 12px;
            z-index: 2147483647;

            background: rgba(20,20,20,.96);
            color: white;

            padding: 10px;

            border-radius: 8px;

            font: 12px monospace;
            line-height: 1.45;

            box-shadow:
                0 3px 15px rgba(0,0,0,.45);

            min-width: 315px;

            user-select: none;
        `;

        panel.innerHTML = `
            <div style="
                margin-bottom:6px;
            ">
                <strong>
                    Generic Discovery v0.5
                </strong>
            </div>

            <div style="
                margin-bottom:8px;
                opacity:.7;
                max-width:320px;
            ">
                Web-resource discovery engine
                with passive network observation
                and provenance tracking.
            </div>

            <div style="
                margin-bottom:8px;
            ">
                <button id="gd-start">
                    Scan
                </button>

                <button id="gd-pause">
                    Pause
                </button>

                <button id="gd-stop">
                    Stop
                </button>

                <button id="gd-clear">
                    Clear
                </button>

                <button id="gd-export">
                    Export
                </button>
            </div>

            <div id="gd-status">
                idle
            </div>

            <div id="gd-progress" style="
                margin-top:6px;
                opacity:.85;
            ">
                queue: 0 |
                in-flight: 0
            </div>

            <div id="gd-network" style="
                margin-top:4px;
                opacity:.7;
            ">
                network: 0 |
                DOM: 0
            </div>

            <div id="gd-graph" style="
                margin-top:4px;
                opacity:.7;
            ">
                graph: 0 nodes / 0 edges
            </div>
        `;

        const attach =
            () => {
                (
                    document.documentElement ||
                    document.body
                )?.appendChild(
                    panel
                );
            };

        attach();

        return panel;
    }

    function initializeUi() {
        const panel =
            installUi();

        if (!panel) {
            return;
        }

        const status =
            panel.querySelector(
                '#gd-status'
            );

        const progress =
            panel.querySelector(
                '#gd-progress'
            );

        const network =
            panel.querySelector(
                '#gd-network'
            );

        const graph =
            panel.querySelector(
                '#gd-graph'
            );

        function updateUi() {
            const stats =
                engine.stats;

            const queue =
                engine.scheduler
                    .size();

            const inFlight =
                engine.scheduler
                    .inFlight();

            if (
                engine.running
            ) {
                status.textContent =
                    engine.paused
                        ? 'paused'
                        : 'scanning...';
            }

            progress.textContent =
                `queue: ${queue} | ` +
                `in-flight: ${inFlight} | ` +
                `requests: ${stats.requests}/${CONFIG.maxRequests} | ` +
                `discoveries: ${stats.discoveries}`;

            network.textContent =
                `network: ${stats.passiveNetworkEvents} | ` +
                `DOM: ${stats.passiveDomEvents} | ` +
                `failures: ${stats.failures} | ` +
                `retries: ${stats.retries}`;

            graph.textContent =
                `graph: ${engine.database.graph.nodes.size} nodes / ` +
                `${engine.database.graph.edges.size} edges`;
        }

        let timer =
            setInterval(
                updateUi,
                250
            );

        const startButton =
            panel.querySelector(
                '#gd-start'
            );

        const pauseButton =
            panel.querySelector(
                '#gd-pause'
            );

        const stopButton =
            panel.querySelector(
                '#gd-stop'
            );

        const clearButton =
            panel.querySelector(
                '#gd-clear'
            );

        const exportButton =
            panel.querySelector(
                '#gd-export'
            );

        startButton.addEventListener(
            'click',
            async () => {
                if (
                    engine.running
                ) {
                    return;
                }

                status.textContent =
                    'seeding...';

                engine.seed();

                updateUi();

                try {
                    await engine.run();

                    status.textContent =
                        `done — ` +
                        `${engine.stats.discoveries} discoveries`;
                } catch (error) {
                    warn(
                        'Run failed:',
                        error
                    );

                    status.textContent =
                        'error — see console';
                }

                updateUi();
            }
        );

        pauseButton.addEventListener(
            'click',
            () => {
                if (
                    !engine.running
                ) {
                    return;
                }

                if (
                    engine.paused
                ) {
                    engine.resume();

                    status.textContent =
                        'scanning...';
                } else {
                    engine.pause();

                    status.textContent =
                        'paused';
                }

                updateUi();
            }
        );

        stopButton.addEventListener(
            'click',
            () => {
                engine.stop();

                status.textContent =
                    'stopped';

                updateUi();
            }
        );

        clearButton.addEventListener(
            'click',
            () => {
                if (
                    engine.running
                ) {
                    status.textContent =
                        'stop the scan first';

                    return;
                }

                if (
                    engine.clear()
                ) {
                    status.textContent =
                        'cleared';
                }

                updateUi();
            }
        );

        exportButton.addEventListener(
            'click',
            () => {
                try {
                    const data =
                        engine.export();

                    const blob =
                        new Blob(
                            [
                                JSON.stringify(
                                    data,
                                    null,
                                    2
                                )
                            ],
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
                        `discovery-${Date.now()}.json`;

                    document.body.appendChild(
                        anchor
                    );

                    anchor.click();

                    anchor.remove();

                    setTimeout(
                        () => {
                            URL.revokeObjectURL(
                                url
                            );
                        },
                        1000
                    );
                } catch (error) {
                    warn(
                        'Export failed:',
                        error
                    );
                }
            }
        );

        /*
         * If the script executes at document-start, the document root may
         * not exist yet. Reattach the UI once DOMContentLoaded fires.
         */
        document.addEventListener(
            'DOMContentLoaded',
            () => {
                if (
                    !document.getElementById(
                        'generic-discovery-panel'
                    )
                ) {
                    initializeUi();
                }

                engine.installDomObserver();
            },
            {
                once: true
            }
        );

        updateUi();

        /*
         * Keep the timer bounded if the page is destroyed.
         */
        window.addEventListener(
            'pagehide',
            () => {
                if (timer) {
                    clearInterval(
                        timer
                    );

                    timer =
                        null;
                }

                engine.networkObserver
                    .dispose();
            },
            {
                once: true
            }
        );
    }


    // =====================================================================
