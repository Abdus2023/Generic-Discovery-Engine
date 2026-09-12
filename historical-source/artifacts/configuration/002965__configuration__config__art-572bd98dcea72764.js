    const CONFIG = {
        maxCandidates: 500,
        maxRequests: 100,

        concurrency: 3,

        requestTimeout: 8000,

        /*
         * Keep this true unless you intentionally want cross-origin
         * discovery. Cross-origin requests also depend on userscript
         * manager permissions and remote server behavior.
         */
        sameOriginOnly: true,

        discoverLinks: true,
        discoverResources: true,
        discoverForms: true,
        discoverMetadata: true,
        discoverFromText: true,

        /*
         * Number of times an acquisition may be retried after failure.
         */
        maxRetries: 1,

        /*
         * State persistence can become large on long-running scans.
         */
        persistState: true,
        maxPersistedDiscoveries: 1000,

        debug: true
    };
