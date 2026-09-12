    // UI
    // =====================================================================

    const engine =
        new DiscoveryEngine();

    /*
     * Public API for experimentation.
     */
    window.GenericDiscovery =
        engine;

    /*
     * Avoid creating duplicate panels if the userscript is accidentally
     * injected twice into the same document.
     */
    const existingPanel =
        document.getElementById(
            'generic-discovery-panel'
        );

    if (existingPanel) {
        existingPanel.remove();
    }

    const panel =
        document.createElement('div');

    panel.id =
        'generic-discovery-panel';

    panel.style.cssText = `
        position: fixed;
        right: 12px;
        bottom: 12px;
        z-index: 2147483647;
        background: rgba(20, 20, 20, .94);
        color: white;
        padding: 10px;
        border-radius: 8px;
        font: 12px monospace;
        line-height: 1.45;
        box-shadow: 0 3px 15px rgba(0, 0, 0, .4);
        min-width: 250px;
    `;

    panel.innerHTML = `
        <div style="margin-bottom:6px">
            <strong>Generic Discovery v0.3</strong>
        </div>

        <div style="
            margin-bottom:8px;
            opacity:.7;
            max-width:280px;
        ">
            Web-resource prototype inspired by
            DVB blind-scan architecture.
        </div>

        <div style="margin-bottom:8px">
            <button id="gd-start">Scan</button>
            <button id="gd-clear">Clear</button>
            <button id="gd-export">Export</button>
        </div>

        <div id="gd-status">
            idle
        </div>

        <div id="gd-progress" style="
            margin-top:6px;
            opacity:.8;
        ">
            queue: 0 | in-flight: 0
        </div>
    `;

    document.documentElement.appendChild(
        panel
    );

    const status =
        panel.querySelector(
            '#gd-status'
        );

    const progress =
        panel.querySelector(
            '#gd-progress'
        );

    function updateUi() {
        if (!status || !progress) {
            return;
        }

        const queue =
            engine.scheduler.size();

        const inFlight =
            engine.scheduler.inFlight();

        const stats =
            engine.stats;

        if (engine.running) {
            status.textContent =
                'scanning...';
        }

        progress.textContent =
            `queue: ${queue} | ` +
            `in-flight: ${inFlight} | ` +
            `requests: ${stats.requests}/${CONFIG.maxRequests} | ` +
            `discoveries: ${stats.discoveries} | ` +
            `failures: ${stats.failures}`;
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

        clearInterval(uiTimer);
        uiTimer = null;
    }


    // =====================================================================
