    const CONFIG = {
        maxCandidates: 750,
        maxRequests: 150,
        concurrency: 4,

        requestTimeout: 8000,

        sameOriginOnly: true,

        discoverLinks: true,
        discoverResources: true,
        discoverForms: true,
        discoverMetadata: true,
        discoverFromText: true,
        discoverNetwork: true,
        discoverPerformance: true,
        discoverWellKnown: true,

        maxRetries: 2,
        retryBaseDelay: 500,
        retryMaxDelay: 8000,

        maxDepth: 5,

        priorityDepthPenalty: 0.045,

        persistState: true,
        maxPersistedDiscoveries: 1200,

        maxStoredTextPreview: 300,

        networkBridge: true,

        debug: true
    };
