// UI
// ---------------------------------------------------------------

const engine =
    new DiscoveryEngine();

window.GenericDiscovery =
    engine;

const panel =
    document.createElement('div');

panel.style.cssText = `
    position: fixed;
    right: 12px;
    bottom: 12px;
    z-index: 2147483647;
    background: rgba(20,20,20,.94);
    color: white;
    padding: 10px;
    border-radius: 8px;
    font: 12px monospace;
    box-shadow: 0 3px 15px rgba(0,0,0,.4);
`;

panel.innerHTML = `
    <div style="margin-bottom:6px">
        <strong>Discovery</strong>
    </div>

    <button id="gd-start">
        Scan
    </button>

    <button id="gd-clear">
        Clear
    </button>

    <button id="gd-export">
        Export
    </button>

    <div id="gd-status"
         style="margin-top:6px">
        idle
    </div>
`;

document.documentElement.appendChild(panel);

const status =
    panel.querySelector('#gd-status');

panel.querySelector('#gd-start')
    .addEventListener('click', async () => {

        status.textContent = 'scanning...';

        engine.seed();

        await engine.run();

        status.textContent =
            `done — ${engine.stats.discoveries} discoveries`;
    });

panel.querySelector('#gd-clear')
    .addEventListener('click', () => {

        engine.clear();

        status.textContent =
            'cleared';
    });

panel.querySelector('#gd-export')
    .addEventListener('click', () => {

        const data =
            engine.export();

        const blob =
            new Blob(
                [JSON.stringify(data, null, 2)],
                { type: 'application/json' }
            );

        const url =
            URL.createObjectURL(blob);

        const a =
            document.createElement('a');

        a.href = url;
        a.download =
            `discovery-${Date.now()}.json`;

        a.click();

        URL.revokeObjectURL(url);
    });
```

})();  
