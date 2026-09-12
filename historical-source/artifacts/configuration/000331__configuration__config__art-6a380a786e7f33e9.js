    const CONFIG = {
        maxCandidates: 750,
        maxRequests: 150,
        concurrency: 4,
        requestTimeout: 8000,

        sameOriginOnly: true,

        stripTrackingParams: true,

        discovery: {
            links: true,
            resources: true,
            forms: true,
            metadata: true,
            text: true,
            network: true,
            performance: true,
            wellKnown: true
        },

        policy: {
            acquireForms: false,
            acquireMedia: false,
            acquireBinaryResources: false,
            acquireFrames: true,
            acquireStylesheets: true,
            acquireScripts: true,
            acquireNetworkGet: true
        },

        origin: {
            maxRequestsPerOrigin: 50,
            minRequestInterval: 150,
            maxConcurrentPerOrigin: 2
        },

        adaptive: {
            enabled: true,
            minimumConcurrency: 1,
            failureThreshold: 2,
            successThreshold: 4
        },

        retry: {
            maxRetries: 2,
            baseDelay: 500,
            maxDelay: 8000
        },

        maxDepth: 5,

        priorityDepthPenalty: 0.045,
        confidencePriorityBoost: 0.08,
        retryPriorityPenalty: 0.05,

        typePriority: {
            api: 1.00,
            manifest: 0.96,
            sitemap: 0.95,
            robots: 0.94,
            url: 0.80,
            feed: 0.82,
            metadata: 0.78,
            network: 0.76,
            frame: 0.72,
            script: 0.62,
            stylesheet: 0.58,
            resource: 0.45,
            form: 0.35,
            media: 0.28,
            embedded: 0.25,
            xml: 0.55,
            text: 0.40
        },

        fingerprintMaxChars: 1_000_000,

        maxNetworkEvents: 1000,
        maxGraphEdges: 5000,

        observeDomMutations: true,
        mutationDebounce: 250,

        persistence: true,
        persistenceDebounce: 400,
        persistedDiscoveries: 1200,
        persistedResources: 1500,
        persistedEdges: 3000,

        maxStoredTextPreview: 300,
        maxDiagnostics: 500,

        networkBridge: true,
        debug: true
    };
