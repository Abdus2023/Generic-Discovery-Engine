    // UI
    // =====================================================================

    const engine =
        new DiscoveryEngine();

    window.GenericDiscovery =
        engine;

    /*
     * Avoid duplicate panels.
     */
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

        background: rgba(20,20,20,.95);
        color: white;

        padding: 10px;

        border-radius: 8px;

        font: 12px monospace;
        line-height: 1.45;

        box-shadow:
            0 3px 15px rgba(0,0,0,.4);

        min-width: 285px;

        user-select: none;
    `;

    panel.innerHTML = `
        <div style="
            margin-bottom:6px;
        ">
            <strong>
                Generic Discovery v0.4
            </strong>
        </div>

        <div style="
            margin-bottom:8px;
            opacity:.7;
            max-width:300px;
        ">
            Web-resource discovery engine
            inspired by blind-scan architecture.
        </div>

        <div style="
            margin-bottom:8px;
        ">
            <button id="gd-start">
                Scan
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
            opacity:.8;
        ">
            queue: 0 |
            in-flight: 0 |
            requests: 0 |
            discoveries: 0
        </div>

        <div id="gd-network" style="
            margin-top:4px;
            opacity:.7;
        ">
            network: 0 |
            DOM: 0
        </div>
    `;

    document.documentElement
        .appendChild(panel);

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

    function updateUi() {
        if (
            !status ||
            !progress
        ) {
            return;
        }

        const stats =
            engine.stats;

        const queue =
            engine.scheduler.size();

        const inFlight =
            engine.scheduler
                .inFlight();

        if (
            engine.running
        ) {
            status.textContent =
                'scanning...';
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
    }

    let uiTimer = null;

    function startUiTimer() {
        if (uiTimer) {
            return;
        }

        uiTimer =
            setInterval(
                updateUi,
                250
            );
    }

    function stopUiTimer() {
        if (!uiTimer) {
            return;
        }

        clearInterval(
            uiTimer
        );

        uiTimer =
            null;
    }


    // =====================================================================
