    const CONFIG = {
        maxCandidates: 1000,
        maxRequests: 200,

        concurrency: 5,

        requestTimeout: 8000,

        sameOriginOnly: true,

        /*
         * URL canonicalization.
         *
         * Tracking parameters are removed only when this option is enabled.
         * Query parameters are otherwise deliberately NOT sorted because
         * parameter ordering can occasionally have application semantics.
         */
        stripTrackingParams: true,

        trackingParameterPrefixes: [
            'utm_'
        ],

        trackingParameters: [
            'fbclid',
            'gclid',
            'dclid',
            'msclkid',
            'mc_cid',
            'mc_eid',
            '_ga'
        ],

        /*
         * Acquisition policy.
         *
         * Discovery can still record these resources even when acquisition
         * is disabled. The policy therefore affects fetching, not knowledge.
         */
        acquireForms: false,
        acquireMedia: false,
        acquireBinaryResources: false,
        acquireFrames: true,

        /*
         * Origin politeness.
         */
        maxRequestsPerOrigin: 40,
        minRequestInterval: 150,
        maxConcurrentPerOrigin: 2,

        /*
         * Adaptive scheduler.
         *
         * current concurrency begins at configured concurrency and is reduced
         * when repeated failures/timeouts occur.
         */
        adaptiveConcurrency: true,
        adaptiveMinConcurrency: 1,
        adaptiveRecoverySuccesses: 5,
        adaptiveFailureThreshold: 2,

        /*
         * Discovery.
         */
        discoverLinks: true,
        discoverResources: true,
        discoverForms: true,
        discoverMetadata: true,
        discoverFromText: true,
        discoverNetwork: true,
        discoverPerformance: true,
        discoverWellKnown: true,

        /*
         * Retry policy.
         */
        maxRetries: 2,
        retryBaseDelay: 500,
        retryMaxDelay: 8000,

        /*
         * Depth / priority.
         */
        maxDepth: 6,
        priorityDepthPenalty: 0.045,
        confidencePriorityBoost: 0.08,
        retryPriorityPenalty: 0.05,

        typePriority: {
            api: 0.96,
            manifest: 0.92,
            sitemap: 0.90,
            robots: 0.88,
            url: 0.84,
            feed: 0.82,
            network: 0.80,
            metadata: 0.76,
            xml: 0.70,
            frame: 0.62,
            script: 0.56,
            stylesheet: 0.54,
            resource: 0.48,
            embedded: 0.44,
            form: 0.35,
            text: 0.30,
            media: 0.20
        },

        /*
         * Fingerprinting.
         */
        fingerprintMaxChars: 1000000,

        /*
         * Duplicate-content detection.
         *
         * Different URLs remain different graph nodes; the fingerprint index
         * merely records that their acquired representations are identical.
         */
        detectDuplicateContent: true,
        maxDuplicateGroups: 1000,

        /*
         * Persistence.
         */
        persistState: true,
        persistDebounceMs: 500,

        maxPersistedDiscoveries: 1500,
        maxPersistedResources: 2000,
        maxPersistedEdges: 4000,
        maxPersistedDiagnostics: 500,

        /*
         * Network / diagnostics.
         */
        networkBridge: true,
        maxNetworkEvents: 1500,
        maxDiagnostics: 500,

        /*
         * UI.
         */
        uiRefreshMs: 400,

        debug: true
    };
