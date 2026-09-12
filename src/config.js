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
        lifecycle: {
            strict: false // true → illegal transitions throw; false → diagnostic + allow
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

