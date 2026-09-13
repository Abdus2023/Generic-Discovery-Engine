// src/config.js — CONFIG v8
    const CONFIG = {
        version: 8,

        maxCandidates: 750,
        candidateTTL: 0, // 0=disabled, else ms — queued age > TTL → skipped ttl-expired
        inference: {
            patternInference: true,
            clustering: true,
            minPatternFreq: 3
        },
        changeDetection: true,
        revisitChanged: false,
        patternGuided: {
            enabled: false,
            maxSuggestions: 5
        },
        lifecycle: {
            strict: false // true → illegal transitions throw; false → diagnostic + allow
        },
        providers: {
            lazy: true, // true → providers instantiated on first match; false → eager (v1.0 behavior)
            disabled: [], // e.g. ['text','binary'] to disable noisy providers
            concurrent: false // true → recognize providers via Promise.all (parallel) vs sequential; benchmark ~0.02ms vs ~0.01ms
        },
        health: {
            enabled: true,
            maxRecentErrors: 20,
            slowProviderMs: 50 // provider avgMs > slow threshold → health warning
        },
        maxObservationsInMemory: 800,
        maxRequests: 150,
        concurrency: 4,
        requestTimeout: 8000,

        sameOriginOnly: true,
        stripTrackingParams: true,

        privacy: {
            stripSensitiveParams: false,
            sensitiveKeys: [
                /^token$/i,
                /^session$/i,
                /^auth$/i,
                /^sid$/i,
                /^access_token$/i,
                /^api_key$/i,
                /^apikey$/i,
                /^secret$/i
            ]
        },

        maxDepth: 5,

        maxBodyChars: 2_000_000,
        fingerprintMaxChars: 1_000_000,

        maxNetworkEvents: 1000,
        maxGraphEdges: 5000,
        maxDiagnostics: 500,
        // Runtime retention bounds (P1 hardening — not just persistence slice)
        maxDiscoveriesInMemory: 2000,
        maxResourcesInMemory: 2000,
        // Search budget vs runtime budget distinction (v1.5) + Bounded Knowledge Kernel (v1.6)
        runtimeBudget: {
            maxBodiesInMemory: 150, // cap observations bodies retained (mirrors maxRequests)
            maxDiscoveryHistory: 2000,
            maxResourceHistory: 2000,
            maxBodyBytes: 5_000_000 // global retained body bytes bound (v1.6 B2)
        },
        // RetentionPolicy — explicit bounded retention for every collection (v1.6)
        // Every Map/Set tracks insertion order → FIFO eviction; relation arrays capped.
        retention: {
            visited: { maxEntries: 2000 },
            candidateKeys: { maxEntries: 2000 },
            candidateHistory: { maxEntries: 2000 }, // historical candidates beyond live frontier
            observations: { maxEntries: 800, maxBodyBytes: 5_000_000, maxBodies: 150 },
            discoveries: { maxEntries: 2000 },
            resources: { maxEntries: 2000, maxRelationsPerResource: 100 },
            fingerprint: { maxHashes: 500, maxUrlsPerHash: 100 },
            patterns: { maxEntries: 500 },
            clusters: { maxEntries: 500 },
            networkEvents: { maxEntries: 1000 },
            graphEdges: { maxEntries: 5000 },
            diagnostics: { maxEntries: 500 }
        },

        observeDomMutations: true,
        mutationDebounce: 250,

        persistence: true,
        persistenceDebounce: 400,

        persistedDiscoveries: 1200,
        persistedResources: 1500,
        persistedEdges: 3000,
        persistedLedgerEvents: 5000,

        networkBridge: true,

        debug: true,

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
            minConcurrency: 1,
            failureThreshold: 2,
            successThreshold: 4
        },

        retry: {
            maxRetries: 2,
            baseDelay: 500,
            maxDelay: 8000
        },

        priority: {
            depthPenalty: 0.045,
            confidenceBoost: 0.08,
            retryPenalty: 0.05
        },

        typePriority: {
            api: 1.00,
            manifest: 0.95,
            sitemap: 0.92,
            robots: 0.90,
            url: 0.88,
            feed: 0.87,
            metadata: 0.82,
            network: 0.80,
            frame: 0.65,
            script: 0.60,
            stylesheet: 0.58,
            resource: 0.45,
            form: 0.30,
            media: 0.20,
            embedded: 0.20,
            xml: 0.45,
            text: 0.40,
            unknown: 0.25
        }
    };

    /**
     * @typedef {Object} CandidateData
     * @property {string} target
     * @property {string} type
     * @property {string} origin
     * @property {string|null} parent
     * @property {number} priority
     * @property {Object} hints
     * @property {number} depth
     */

    /** @typedef {Object} ObservationData
     *  @property {string} candidateId
     *  @property {string} planId
     *  @property {string} target
     *  @property {{status:number,contentType:string,contentLength:number|null,finalUrl:string}} http
     *  @property {string} body
     *  @property {{algorithm:string,hash:string,length:number,sampledLength:number}|null} fingerprint
     */

    /** @typedef {Object} DiscoveryData
     *  @property {string} candidateId
     *  @property {string} observationId
     *  @property {string} kind
     *  @property {number} confidence
     *  @property {string} mechanism
     *  @property {Object} data
     *  @property {Object} provenance
     */

    const STORAGE_KEY = 'generic-discovery-engine-v8';

