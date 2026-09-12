    const CONFIG = {
        maxCandidates: 750,
        maxRequests: 150,

        concurrency: 3,

        requestTimeout: 8000,

        sameOriginOnly: true,

        maxDepth: 8,

        maxRetries: 2,

        retryBaseDelay: 500,

        /*
         * Passive observers do not themselves perform requests.
         * They only record resources the current page is already using.
         */
        observeNetwork: true,
        observeDomResources: true,

        discoverLinks: true,
        discoverResources: true,
        discoverForms: true,
        discoverMetadata: true,
        discoverFromText: true,
        discoverCss: true,

        persistState: true,
        maxPersistedDiscoveries: 1500,
        maxPersistedVisited: 5000,

        debug: true
    };
