    const CONFIG = {
        maxCandidates: 1000,
        maxRequests: 200,
        concurrency: 4,

        requestTimeout: 8000,

        sameOriginOnly: true,

        maxDepth: 6,

        maxRetries: 2,
        retryBaseDelay: 500,
        retryMaxDelay: 8000,

        priorityDepthPenalty: 0.045,

        discoverLinks: true,
        discoverResources: true,
        discoverForms: true,
        discoverMetadata: true,
        discoverFromText: true,
        discoverNetwork: true,
        discoverPerformance: true,
        discoverWellKnown: true,

        /*
         * Network candidates are only actively acquired when the
         * observed request is GET/HEAD/unknown. POST/PUT/PATCH/DELETE
         * activity is recorded but is not replayed.
         */
        acquireObservedNonGet: false,

        maxNetworkEvents: 1500,

        persistState: true,
        maxPersistedDiscoveries: 1500,

        maxTextPreview: 300,

        debug: true
    };
