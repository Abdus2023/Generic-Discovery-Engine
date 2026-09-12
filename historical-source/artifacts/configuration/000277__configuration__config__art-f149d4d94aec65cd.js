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
        confidencePriorityBoost: 0.08,
        retryPriorityPenalty: 0.05,

        typePriority: {
            api: 0.95,
            manifest: 0.92,
            sitemap: 0.90,
            robots: 0.88,
            url: 0.84,
            feed: 0.82,
            metadata: 0.76,
            network: 0.80,
            frame: 0.62,
            script: 0.56,
            stylesheet: 0.54,
            resource: 0.48,
            form: 0.42,
            media: 0.25,
            embedded: 0.40,
            xml: 0.70,
            text: 0.30
        },

        fingerprintMaxChars: 1000000,

        maxNetworkEvents: 1000,
        maxGraphEdges: 5000,

        persistState: true,
        persistDebounceMs: 400,
        maxPersistedDiscoveries: 1200,
        maxPersistedResources: 1500,
        maxPersistedEdges: 3000,

        maxStoredTextPreview: 300,

        networkBridge: true,

        debug: true
    };
