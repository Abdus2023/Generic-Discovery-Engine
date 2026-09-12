    const CONFIG = {
        maxCandidates: 1000,
        maxRequests: 200,
        concurrency: 4,

        requestTimeout: 8000,
        maxResponseBytes: 2 * 1024 * 1024,

        sameOriginOnly: true,

        maxDepth: 8,

        maxRetries: 2,
        retryBaseDelay: 500,
        retryMaxDelay: 8000,

        /*
         * Passive observation.
         */
        observeNetwork: true,
        observePerformance: true,
        observeDomResources: true,

        /*
         * Discovery.
         */
        discoverLinks: true,
        discoverResources: true,
        discoverForms: true,
        discoverMetadata: true,
        discoverFromText: true,
        discoverCss: true,
        discoverApis: true,
        discoverSitemaps: true,

        /*
         * Standard well-known discovery endpoints.
         */
        discoverWellKnown: true,

        /*
         * Persistence.
         */
        persistState: true,
        maxPersistedDiscoveries: 2000,
        maxPersistedVisited: 8000,

        /*
         * Safety bounds.
         */
        maxUrlsPerDiscovery: 500,
        maxGraphNodes: 5000,
        maxGraphEdges: 10000,

        debug: true
    };
