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
        confidencePriorityBoost: 0.10,
        retryPriorityPenalty: 0.035,

        maxNetworkEvents: 1500,
        maxGraphEdges: 5000,

        maxPersistedDiscoveries: 1500,
        maxPersistedResources: 1500,
        maxPersistedEdges: 4000,

        fingerprintMaxChars: 1000000,

        persistState: true,
        persistDebounceMs: 500,

        discoverLinks: true,
        discoverResources: true,
        discoverForms: true,
        discoverMetadata: true,
        discoverFromText: true,
        discoverNetwork: true,
        discoverPerformance: true,
        discoverWellKnown: true,

        /*
         * Only GET/HEAD/unknown observed requests are considered
         * automatically replayable. State-changing requests remain
         * observational only unless explicitly enabled.
         */
        acquireObservedNonGet: false,

        debug: true
    };
