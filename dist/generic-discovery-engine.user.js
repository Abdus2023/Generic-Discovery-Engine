// ==UserScript==
// @name         Generic Discovery Engine
// @namespace    generic-discovery
// @version      1.3.0
// @description  Generic web-resource discovery engine inspired by the architecture of DVB blind scanning.
// @match        *://*/*
// @run-at       document-start
// @noframes
// @grant        GM_getValue
// @grant        GM_setValue
// @grant        GM_xmlhttpRequest
// @connect      self
// @connect      *  — uncomment if CONFIG.sameOriginOnly=false (cross-origin); default same-origin keeps self
// ==/UserScript==

(function () {
    'use strict';

    /*
     * ============================================================
     * Generic Discovery Engine
     * v1.3.0 — WellKnown + Manifest Providers + ESM Bundle Proof
     * Patch notes vs v1.2.0:
     * - Providers: WellKnownProvider (/.well-known/ json/text → json-url 0.80/text-url
     *           0.70, matches well-known path) + ManifestProvider (manifest.json
     *           icons[].src 0.85, start_url 0.80, scope 0.75, screenshots/shortcuts);
     *           Registry now 13 ordered Html/Json/Xml/Css/JS/Robots/Headers/
     *           SitemapIndex/OpenApi/WellKnown/Manifest/Binary/Text (lazy, disabled
     *           respects new names, getInstanceCount 13)
     *         + Build: build-esm.js ESM bundle proof (esbuild bundle+metafile, treeShaking
     *           fallback transform, dist/generic-discovery-engine.esm.js) + dist/.esm-metafile.json
     *           + .build-meta esmBundle stats, npm run build:esm + build:all 5 steps
     *         + Tests: wellKnown 4 + manifest 4 cases (151/151 39 suites)
     *         + Perf: wellKnown json walk ~0.03ms, manifest 0.02ms, bundle +80 lines, min 60k 33%

     * v1.2.0 — SitemapIndex + OpenAPI Providers + Bundle Analyze
     * Patch notes vs v1.1.0:
     * - Providers: SitemapIndexProvider (sitemapindex <loc> → sitemap 0.90, XML sitemapindex root)
     *           + OpenApiProvider (openapi/swagger json → servers[].url 0.95, host+basePath 0.90,
     *             walk api-url 0.85, matches openapi/swagger/info+paths); Registry now 11
     *             ordered Html/Json/Xml/Css/JS/Robots/Headers/SitemapIndex/OpenApi/Binary/Text
     *             (lazy factories, disabled respects new names, getInstanceCount 11)
     *         + Build: analyze-bundle.js (esbuild metafile + provider line/size table, .build-meta
     *           providerSizes + bundleAnalysis), npm run analyze + build:all includes analyze
     *         + Tests: sitemapIndex 4 + openapi 4 cases (143/143 37 suites)
     *         + Perf: sitemapIndex O(n) extractXmlLocs ~0.02ms, openapi JSON parse+walk ~0.05ms,
     *           bundle +80 lines, min 60k 33% (11 providers), lazy still 0→11 on demand

     * v1.1.0 — Lazy Providers + esbuild Minify (provider hardening)
     * Patch notes vs v1.0.0:
     * - Providers: ProviderRegistry lazy (CONFIG.providers.lazy true, disabled []) + metrics
     *           factories Html/Json/Xml/Css/JS/Robots/Headers/Binary/Text ordered, eager fallback
     *           when lazy false, getMetrics()/getInstanceCount(), matching() instruments calls/matches/ms
     *           + getProviderMetrics() + coverage providerInstances/providerMetrics + export providers{} block
     *         + Build: esbuild minify (dist/generic-discovery-engine.min.js) via scripts/build-esbuild.js
     *           + npm run build:all (concat + minify + verify), .build-meta minified stats
     *         + Tests: provider-lazy 5 cases + eager/disabled/metrics/order (131/131)
     *         + Perf: lazy cuts startup ~0.3 ms, matching ~0.01 ms overhead, memory -9 instances until use

     * v1.0.0 — Stable (generic discovery loop feature-complete)
     * Patch notes vs v0.9.1:
     * - Stable: package 1.0.0, header 1.0.0, CONFIG v8 unchanged (storage compatible)
     *           + no new runtime code — 1.0 marks control-plane feature-complete
     *           + 22 ADRs, 126/126 tests, 5,969 lines, sha 44500a… (dist hash unchanged
     *             except version banner), verify:build deterministic, deep audit valid
     *         + Docs: 1.0 stable verification supplement, README 1.0, CHANGELOG 1.0

     * v0.9.1 — Pattern-Guided + RevisitChanged (adaptive re-queue)
     * Patch notes vs v0.9.0:
     * - Knowledge: KnowledgeBase.suggestPatternCandidates() (top patterns ≥minPatternFreq,
     *           {int}/{hash}/{uuid} → 0/0…/uuid0, bounded 5, isAllowedUrl, visited-dedup)
     *           + getChangedResources() (status='changed'); CONFIG.patternGuided.enabled
     *           + CONFIG.revisitChanged (opt-in, clears visited+ candidateKeys)
     *         + Engine: after recordObservation if changed && revisitChanged → discover
     *           revisit-changed (priority 0.6, depth, confidence 0.7, diagnostic revisit-queued)
     *           + after markCompleted if patternGuided.enabled → suggestPatternCandidates()
     *           → discover pattern-guided (priority 0.55, depth+1, diagnostic pattern-guided-queued)
     *         + Tests: revisit + pattern-guided 5 cases + e2e pattern suggestion
     *         + Build: verify-build asserts revisitChanged/patternGuided present

     * v0.9.0 — Framework Bundler (src/ → dist/ deterministic)
     * Patch notes vs v0.8.2:
     * - Framework: src/ split 7 modules (5699 code + 165 header = 5875) via scripts/build.js
     *           bundler (header.txt + config→utils→ledger→models→knowledge→providers→engine)
     *           deterministic sha 8c734c…; dist now generated, src source of truth
     *         + Build: dist 5864→5875 lines, verify-build src 7 gate retained
     *         + Tests: verify-p0 allow 0.9.0; 121/121 still

     * v0.8.2 — Export Hardening + Inference Metrics (coverage+export now include pattern/cluster/fingerprint + deterministic ledger)

     * Patch notes vs v0.8.1:
     * - Export: getCoverageMetrics() now returns inference metrics
     *           (patternCount, clusterCount, fingerprintUnique, inferenceEnabled)
     *           + queuedByType keys sorted for determinism; exportData()
     *           now includes `inference` (patternMetrics, clusterMetrics,
     *           fingerprintStats) alongside coverage/ledger — schema stays
     *           gde-export-v8.0 (additive, JSON-stable sorted keys), ledger
     *           export remains seq-ordered 5k FIFO
     *         + Build: verify-build now asserts exportData inference present +
     *           coverage determinism + no build-time drift
     *         + Tests: export-inference 4 cases + coverage determinism 2 cases

     * Patch notes vs v0.8.0:
     * - Modular: src/ mirror (config.js, utils.js, models.js, knowledge.js,
     *           ledger.js, providers.js, engine.js) extracted from dist
     *           5,773 lines; scripts/build.js now verifies src/ exists and
     *           dist header @version matches pkg + hash matches meta
     *         + Export: CONFIG.version stays 8, exportData().schema
     *           gde-export-v8.0 + pattern/cluster metrics now included in
     *           coverage export (frontier + pattern + cluster)
     *         + Tests: src existence + build determinism + 9-provider
     *           ordered pipeline proven

     * Patch notes vs v0.7.9:
     * - Providers: RobotsProvider (Sitemap: extraction, robots.txt) +
     *           HeadersProvider (Link header → url, Location → url);
     *           ProviderRegistry now 9 providers, ordered Html/Json/Xml/Css/JS/
     *           Robots/Headers/Binary/Text + http.headers captured in
     *           Observation (fetch + GM_xhr)
     *         + Change: CONFIG.changeDetection + KnowledgeBase.detectChange()
     *           (fingerprint hash diff → resource-changed diagnostic + status
     *           `changed`, O(1), ~0.01 ms) + 3 ADRs (016-robots, 017-headers,
     *           018-change)

     * Patch notes vs v0.7.8:
     * - Pattern: CONFIG.inference.patternInference + extractUrlPattern()
     *           (/{int} for /\d+, ={int} for ?=\d+, uuid/hash → {id});
     *           KnowledgeBase patternIndex Map<pattern,count> + clusterIndex
     *           Map<origin+pattern,count> + getPatternMetrics() /
     *           getClusterMetrics() (O(n) over ≤750, ~0.06 ms)
     *         + Build: scripts/build.js (deterministic rebuild check) +
     *           npm run verify:build (sha256 + wc -l) + tsconfig strict false
     *           + 3 ADRs (013-pattern, 014-cluster, 015-build)
     *         + Tests: property-pattern 7 invariants (seeded)

     * Patch notes vs v0.7.7:
     * - Lifecycle: CONFIG.lifecycle.strict + KnowledgeBase._validateTransition
     *           table (discovered→queued→claimed→planned→acquiring→observed
     *           →recognized→expanded→completed, with skipped/failed/ttl/queued
     *           branches); illegal transitions emit lifecycle-illegal-transition
     *           diagnostic, strict mode throws; ~0.02 ms per mark
     *         + Concurrency: claimNextCandidate() is synchronous sort+mark
     *           proven exclusive under interleaved workers (property-concurrency
     *           harness, 500 iter, TTL+retry windows)
     *         + Types: JSDoc typedefs + tsconfig.json (checkJs strict) +
     *           npm run typecheck (tsc --noEmit) + .c8rc gate holds 85/75/80
     *
     * Patch notes vs v0.7.6:
     * - Bounds: CONFIG.candidateTTL (0=off, ms) — claimNextCandidate() now
     *           sweeps queued/failed and marks ttl-expired (ledger + skipped)
     *           before sort; prevents stale frontier at live cap
     *         + Ledger FIFO 5000 + Origin throttle invariants proven via
     *           property-determinism harness (seeded, 500 iter)
     *         + Coverage gate: .c8rc check-coverage true (85/75) + CI lint
     *           + 3 ADRs (007-ttl, 008-throttle, 009-coverage-gates)
     *
     * v0.7.6 — Performance & Coverage (rAF UI + coverage proof + invariants)
     *
     * Patch notes vs v0.7.5:
     * - Perf: updateUI() now rAF-batched (_uiRaf + _doUpdateUI) to avoid
     *         layout thrash when ledger hits 5k and 4 workers flush;
     *         falls back to sync when rAF unavailable
     *         + coverage script (node --experimental-test-coverage)
     *         + property tests for effectivePriority invariants

     * v0.7.5 — Trust & Verification (Trusted Types + fuzz + CI + ADRs)
     *
     * Patch notes vs v0.7.4:
     * - Trust: Trusted Types policy (gde-bridge) for installBridge()
     *         + JSDoc typedefs + CI workflow verify.yml +
     *           fuzz harness (extract/canonicalize) + 3 more ADRs
     *
     * v0.7.4 — Hardening & Hygiene (P2-6 privacy/CSP/header + ADR split)
     *
     * Patch notes vs v0.7.3:
     * - P2-6: @connect self (with * commented for cross-origin opt-in)
     *         + CONFIG.privacy.stripSensitiveParams (opt-in token/
     *           session/auth scrub in canonicalizeUrl) + explicit
     *           csp-blocks-bridge diagnostic + cross-origin-config
     *           warning at init when sameOriginOnly=false
     *
     * v0.7.3 — Coverage Frontier + E2E Verified (P0/P1/P2-3)
     *
     * Patch notes vs v0.7.2:
     * - P2-3: getCoverageMetrics() + UI + export coverage (frontierSize,
     *         queuedByType, liveCount, visitedSize, knownResources,
     *         requestsRemaining, ledgerSize, graphEdges, observations)
     *         makes budget/frontier observable without extra traversal
     *
     * v0.7.2 — Verified Patch (P0 fixes)
     *
     * Patch notes vs v0.7.1:
     * - P0-1: maxCandidates now counts live (queued/claimed/planned/
     *         acquiring/observed/recognized/failed) not completed/skipped
     * - P0-2: visited now identityKey-scoped (type:target) and consulted
     *         in addCandidate; prevents cross-type duplicate acquisition
     * - P0-3: KnowledgeBase.serialize persists observations without bodies
     *         (already via Observation.serialize) + caps in-memory observations
     *         at 800 entries (FIFO) to avoid unbounded heap on link-dense SPA
     * - P1-1: per-observation discovery deduplication across providers
     * - P1-2: mutation observer batch dedup (Set per flush)
     *
     * v0.7.1
     * Main pipeline:
     *
     * DISCOVERY
     *     ↓
     * KNOWLEDGE GRAPH
     *     ↓
     * ACQUISITION PLAN
     *     ↓
     * SCHEDULER
     *     ↓
     * ACQUISITION
     *     ↓
     * OBSERVATION
     *     ↓
     * RECOGNITION
     *     ↓
     * DISCOVERY
     *
     * Important:
     *
     * Candidate !== AcquisitionPlan
     *
     * Discovery does not authorize acquisition.
     *
     * Decision replay is supported.
     * Network replay is NOT guaranteed.
     * ============================================================
     */

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
            disabled: [] // e.g. ['text','binary'] to disable noisy providers
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

    function log(...args) {
        if (CONFIG.debug) {
            console.log('[GDE]', ...args);
        }
    }

    function warn(...args) {
        console.warn('[GDE]', ...args);
    }

    function now() {
        return Date.now();
    }

    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    function makeId(prefix) {
        return `${prefix}-${now()}-${Math.random().toString(36).slice(2, 10)}`;
    }

    function clamp(value, min, max) {
        return Math.max(min, Math.min(max, value));
    }

    function safeArray(value) {
        return Array.isArray(value) ? value : [];
    }

    function unique(values) {
        return [...new Set(values)];
    }

    function originOf(url) {
        try {
            return new URL(url, location.href).origin;
        } catch {
            return location.origin;
        }
    }

    function canonicalizeUrl(raw) {
        try {
            const url = new URL(raw, location.href);

            url.hash = '';

            if (CONFIG.stripTrackingParams) {
                const tracking = [
                    /^utm_/i,
                    /^fbclid$/i,
                    /^gclid$/i,
                    /^mc_/i,
                    /^ref$/i
                ];

                for (const key of [...url.searchParams.keys()]) {
                    if (tracking.some(rx => rx.test(key))) {
                        url.searchParams.delete(key);
                    }
                }
            }

            if (CONFIG.privacy?.stripSensitiveParams) {
                const sensitive =
                    CONFIG.privacy.sensitiveKeys || [];
                for (const key of [...url.searchParams.keys()]) {
                    if (
                        sensitive.some(rx =>
                            rx.test(key)
                        )
                    ) {
                        url.searchParams.delete(key);
                    }
                }
            }

            return url.href;
        } catch {
            return null;
        }
    }

    function isAllowedUrl(url) {
        try {
            const parsed = new URL(url, location.href);

            if (!/^https?:$/.test(parsed.protocol)) {
                return false;
            }

            if (
                CONFIG.sameOriginOnly &&
                parsed.origin !== location.origin
            ) {
                return false;
            }

            return true;
        } catch {
            return false;
        }
    }

    function contentTypeBase(value) {
        return String(value || '')
            .split(';')[0]
            .trim()
            .toLowerCase();
    }

    function looksLikeHtml(contentType, body = '') {
        const type = contentTypeBase(contentType);

        if (
            type === 'text/html' ||
            type === 'application/xhtml+xml'
        ) {
            return true;
        }

        return /^\s*(<!doctype\s+html|<html\b)/i.test(body);
    }

    function looksLikeJson(contentType, body = '') {
        const type = contentTypeBase(contentType);

        if (
            type === 'application/json' ||
            type.endsWith('+json')
        ) {
            return true;
        }

        return /^\s*[\[{]/.test(body);
    }

    function looksLikeXml(contentType, body = '') {
        const type = contentTypeBase(contentType);

        if (
            type === 'application/xml' ||
            type === 'text/xml' ||
            type.endsWith('+xml')
        ) {
            return true;
        }

        return /^\s*<\?xml\b/i.test(body);
    }

    function looksLikeCss(contentType) {
        const type = contentTypeBase(contentType);
        return type === 'text/css';
    }

    function looksLikeJavaScript(contentType) {
        const type = contentTypeBase(contentType);

        return [
            'application/javascript',
            'text/javascript',
            'application/x-javascript',
            'text/ecmascript',
            'application/ecmascript'
        ].includes(type);
    }

    function looksLikeBinary(contentType) {
        const type = contentTypeBase(contentType);

        return (
            type.startsWith('image/') ||
            type.startsWith('audio/') ||
            type.startsWith('video/') ||
            type === 'application/pdf' ||
            type === 'application/zip' ||
            type === 'application/octet-stream'
        );
    }

    function looksLikeApiUrl(url) {
        try {
            const path = new URL(url).pathname.toLowerCase();

            return (
                path.includes('/api/') ||
                path.endsWith('/api') ||
                path.includes('/graphql') ||
                path.includes('/json') ||
                path.includes('/ajax')
            );
        } catch {
            return false;
        }
    }

    function extractUrlsFromText(text) {
        if (!text) return [];

        const results = new Set();

        const absolute =
            /\bhttps?:\/\/[^\s"'<>\\)]+/gi;

        for (const match of String(text).matchAll(absolute)) {
            results.add(match[0]);
        }

        const relative =
            /(?:^|["'(\s])((?:\/|\.\.?\/)[A-Za-z0-9._~:/?#\[\]@!$&'*+,;=%-]+)/g;

        for (const match of String(text).matchAll(relative)) {
            results.add(match[1]);
        }

        return [...results];
    }

    function extractCssUrls(text) {
        const results = [];

        const rx = /url\(\s*(['"]?)(.*?)\1\s*\)/gi;

        for (const match of String(text || '').matchAll(rx)) {
            if (match[2]) {
                results.push(match[2]);
            }
        }

        return results;
    }

    function extractXmlLocs(text) {
        const results = [];

        try {
            const parser = new DOMParser();
            const doc = parser.parseFromString(text, 'application/xml');

            for (const node of doc.querySelectorAll('loc')) {
                if (node.textContent) {
                    results.push(node.textContent.trim());
                }
            }
        } catch {
            // fall back to regex
        }

        if (!results.length) {
            const rx = /<loc[^>]*>(.*?)<\/loc>/gis;

            for (const match of String(text || '').matchAll(rx)) {
                results.push(match[1].trim());
            }
        }

        return results;
    }

    function fnv1a32(text) {
        let hash = 0x811c9dc5;

        for (let i = 0; i < text.length; i++) {
            hash ^= text.charCodeAt(i);
            hash +=
                (hash << 1) +
                (hash << 4) +
                (hash << 7) +
                (hash << 8) +
                (hash << 24);

            hash >>>= 0;
        }

        return hash.toString(16).padStart(8, '0');
    }

    function makeFingerprint(body) {
        if (!body) return null;

        const sample = String(body)
            .slice(0, CONFIG.fingerprintMaxChars)
            .replace(/\s+/g, ' ')
            .trim();

        return {
            algorithm: 'fnv1a32',
            hash: fnv1a32(sample),
            length: String(body).length,
            sampledLength: sample.length
        };
    }

    function stableId(prefix, value) {
        return `${prefix}-${fnv1a32(String(value))}`;
    }

    function extractUrlPattern(url) {
        if (!CONFIG.inference || !CONFIG.inference.patternInference) {
            return String(url);
        }
        try {
            const u = new URL(url);
            let path = u.pathname.replace(/\/\d+(?=\/|$)/g, '/{int}');
            path = path.replace(/\/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}(?=\/|$)/g, '/{uuid}');
            path = path.replace(/\/[0-9a-fA-F]{32,64}(?=\/|$)/g, '/{hash}');
            let search = u.search.replace(/=\d+(&|$)/g, '={int}$1');
            search = search.replace(/=[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}(&|$)/g, '={uuid}$1');
            search = search.replace(/=[0-9a-fA-F]{32,64}(&|$)/g, '={hash}$1');
            return `${u.origin}${path}${search}`;
        } catch {
            return String(url).replace(/\/\d+(?=\/|$)/g, '/{int}').replace(/=\d+(&|$)/g, '={int}$1');
        }
    }

    function clusterKeyForCandidate(candidate) {
        try {
            const pattern = extractUrlPattern(candidate.target);
            const origin = candidate.origin || originOf(candidate.target) || 'unknown';
            return `${origin}::${pattern}`;
        } catch {
            return String(candidate.target);
        }
    }

    function contentTypeForTarget(type) {
        switch (type) {
            case 'script':
                return 'application/javascript';

            case 'stylesheet':
                return 'text/css';

            case 'sitemap':
            case 'robots':
            case 'feed':
            case 'xml':
                return 'application/xml';

            case 'manifest':
            case 'api':
                return 'application/json';

            default:
                return null;
        }
    }

    /*
     * ============================================================
     * ACQUISITION PLAN
     * ============================================================
     */

    class DecisionLedger {
        constructor() {
            this.sequence = 0;
            this.events = [];
        }

        append(type, data = {}) {
            const event = {
                seq: ++this.sequence,
                id: makeId('evt'),
                type,
                timestamp: now(),
                ...data
            };

            this.events.push(event);

            if (
                this.events.length >
                CONFIG.persistedLedgerEvents
            ) {
                this.events.splice(
                    0,
                    this.events.length -
                        CONFIG.persistedLedgerEvents
                );
            }

            return event;
        }

        recordCandidateDiscovered(candidate, discovery = null) {
            return this.append(
                'candidate-discovered',
                {
                    candidateId: candidate.id,
                    target: candidate.target,
                    candidateType: candidate.type,
                    depth: candidate.depth,
                    priority: candidate.priority,
                    discoveryId:
                        discovery?.id || null
                }
            );
        }

        recordCandidateClaimed(candidate) {
            return this.append(
                'candidate-claimed',
                {
                    candidateId: candidate.id,
                    target: candidate.target,
                    candidateType: candidate.type
                }
            );
        }

        recordPlan(plan) {
            return this.append(
                'acquisition-planned',
                {
                    planId: plan.id,
                    candidateId: plan.candidateId,
                    target: plan.target,
                    method: plan.method,
                    allowed: plan.allowed,
                    reason: plan.reason,
                    priority: plan.priority,
                    expectedType: plan.expectedType,
                    policyVersion: plan.policyVersion
                }
            );
        }

        recordPolicyDenied(plan) {
            return this.append(
                'policy-denied',
                {
                    planId: plan.id,
                    candidateId: plan.candidateId,
                    target: plan.target,
                    method: plan.method,
                    reason: plan.reason
                }
            );
        }

        recordBudgetDenied(candidate, reason) {
            return this.append(
                'budget-denied',
                {
                    candidateId: candidate.id,
                    target: candidate.target,
                    reason
                }
            );
        }

        recordSlotGranted(plan) {
            return this.append(
                'slot-granted',
                {
                    planId: plan.id,
                    candidateId: plan.candidateId,
                    origin: plan.origin
                }
            );
        }

        recordRequestStarted(plan) {
            return this.append(
                'request-started',
                {
                    planId: plan.id,
                    candidateId: plan.candidateId,
                    target: plan.target,
                    method: plan.method
                }
            );
        }

        recordRequestCompleted(plan, observation) {
            return this.append(
                'request-completed',
                {
                    planId: plan.id,
                    candidateId: plan.candidateId,
                    observationId: observation.id,
                    status: observation.status,
                    httpStatus:
                        observation.http?.status || null
                }
            );
        }

        recordObservation(observation) {
            return this.append(
                'observation-recorded',
                {
                    observationId: observation.id,
                    candidateId: observation.candidateId,
                    target: observation.target,
                    status: observation.status,
                    fingerprint:
                        observation.fingerprint?.hash ||
                        null
                }
            );
        }

        recordRecognition(
            candidate,
            observation,
            provider
        ) {
            return this.append(
                'provider-recognized',
                {
                    candidateId: candidate.id,
                    observationId: observation.id,
                    provider
                }
            );
        }

        recordDiscovery(discovery) {
            return this.append(
                'discovery-emitted',
                {
                    discoveryId: discovery.id,
                    candidateId: discovery.candidateId,
                    observationId:
                        discovery.observationId,
                    kind: discovery.kind,
                    confidence: discovery.confidence,
                    mechanism: discovery.mechanism
                }
            );
        }

        recordCandidateEnqueued(candidate) {
            return this.append(
                'candidate-enqueued',
                {
                    candidateId: candidate.id,
                    target: candidate.target,
                    candidateType: candidate.type,
                    priority: candidate.priority,
                    depth: candidate.depth
                }
            );
        }

        recordRetry(candidate, reason) {
            return this.append(
                'candidate-retried',
                {
                    candidateId: candidate.id,
                    target: candidate.target,
                    attempt: candidate.attempts,
                    reason
                }
            );
        }

        recordCandidateCompleted(candidate) {
            return this.append(
                'candidate-completed',
                {
                    candidateId: candidate.id,
                    target: candidate.target
                }
            );
        }

        recordCandidateSkipped(candidate, reason) {
            return this.append(
                'candidate-skipped',
                {
                    candidateId: candidate.id,
                    target: candidate.target,
                    reason
                }
            );
        }

        recordDiagnostic(type, data = {}) {
            return this.append(
                `diagnostic:${type}`,
                data
            );
        }

        export() {
            return {
                version: 1,
                sequence: this.sequence,
                events: this.events.slice()
            };
        }

        restore(data) {
            if (!data || !Array.isArray(data.events)) {
                return;
            }

            this.events = data.events.slice(
                -CONFIG.persistedLedgerEvents
            );

            this.sequence =
                Number.isFinite(data.sequence)
                    ? data.sequence
                    : (
                        this.events.length
                            ? Math.max(
                                ...this.events.map(
                                    e => e.seq || 0
                                )
                            )
                            : 0
                    );
        }
    }

    /*
     * ============================================================
     * CANDIDATE
     * ============================================================
     */

    class Candidate {
        constructor(data = {}) {
            this.id =
                data.id || makeId('candidate');

            this.target =
                canonicalizeUrl(data.target) ||
                data.target ||
                '';

            this.type =
                data.type || 'unknown';

            this.origin =
                data.origin ||
                originOf(this.target);

            this.parent =
                data.parent || null;

            this.priority =
                Number.isFinite(data.priority)
                    ? data.priority
                    : 0;

            this.hints =
                data.hints || {};

            this.depth =
                Number.isFinite(data.depth)
                    ? data.depth
                    : 0;

            this.createdAt =
                data.createdAt || now();

            this.attempts =
                Number.isFinite(data.attempts)
                    ? data.attempts
                    : 0;

            this.status =
                data.status || 'discovered';

            this.nextAttemptAt =
                data.nextAttemptAt || 0;

            this.discoveredAt =
                data.discoveredAt || now();

            this.queuedAt =
                data.queuedAt || null;

            this.claimedAt =
                data.claimedAt || null;

            this.plannedAt =
                data.plannedAt || null;

            this.acquiringAt =
                data.acquiringAt || null;

            this.observedAt =
                data.observedAt || null;

            this.recognizedAt =
                data.recognizedAt || null;

            this.expandedAt =
                data.expandedAt || null;

            this.completedAt =
                data.completedAt || null;

            this.failedAt =
                data.failedAt || null;

            this.skippedAt =
                data.skippedAt || null;

            this.alternateTypes =
                safeArray(data.alternateTypes);

            this.alternateOrigins =
                safeArray(data.alternateOrigins);

            this.alternateParents =
                safeArray(data.alternateParents);
        }

        identityKey() {
            return `${this.type}:${this.target}`;
        }

        effectivePriority() {
            const typeWeight =
                CONFIG.typePriority[this.type] ??
                CONFIG.typePriority.unknown;

            const confidence =
                Number(this.hints.confidence || 0);

            const retryPenalty =
                this.attempts *
                CONFIG.priority.retryPenalty;

            return (
                this.priority +
                typeWeight * 0.20 +
                confidence *
                    CONFIG.priority.confidenceBoost -
                this.depth *
                    CONFIG.priority.depthPenalty -
                retryPenalty
            );
        }

        serialize() {
            return {
                ...this,
                alternateTypes:
                    [...this.alternateTypes],
                alternateOrigins:
                    [...this.alternateOrigins],
                alternateParents:
                    [...this.alternateParents]
            };
        }
    }

    /*
     * ============================================================
     * OBSERVATION
     * ============================================================
     */

    class Observation {
        constructor(data = {}) {
            this.id =
                data.id || makeId('obs');

            this.candidateId =
                data.candidateId || null;

            this.planId =
                data.planId || null;

            this.target =
                data.target || '';

            this.requestedUrl =
                data.requestedUrl || this.target;

            this.startedAt =
                data.startedAt || now();

            this.completedAt =
                data.completedAt || null;

            this.status =
                data.status || 'unknown';

            this.reason =
                data.reason || null;

            this.signalPresent =
                Boolean(data.signalPresent);

            this.http =
                data.http || {
                    status: 0,
                    contentType: '',
                    contentLength: null,
                    finalUrl: this.requestedUrl
                };

            this.body =
                data.body || '';

            this.bodyTruncated =
                Boolean(data.bodyTruncated);

            this.errors =
                safeArray(data.errors);

            this.network =
                safeArray(data.network);

            this.fingerprint =
                data.fingerprint || null;
        }

        serialize() {
            return {
                id: this.id,
                candidateId: this.candidateId,
                planId: this.planId,
                target: this.target,
                requestedUrl: this.requestedUrl,
                startedAt: this.startedAt,
                completedAt: this.completedAt,
                status: this.status,
                reason: this.reason,
                signalPresent: this.signalPresent,
                http: this.http,
                bodyTruncated: this.bodyTruncated,
                errors: this.errors,
                network: this.network,
                fingerprint: this.fingerprint
            };
        }
    }

    /*
     * ============================================================
     * DISCOVERY
     * ============================================================
     */

    class Discovery {
        constructor(data = {}) {
            this.id =
                data.id || makeId('discovery');

            this.candidateId =
                data.candidateId || null;

            this.observationId =
                data.observationId || null;

            this.kind =
                data.kind || 'url';

            this.confidence =
                Number.isFinite(data.confidence)
                    ? data.confidence
                    : 0.5;

            this.mechanism =
                data.mechanism || 'unknown';

            this.data =
                data.data || {};

            this.provenance =
                data.provenance || {};

            this.createdAt =
                data.createdAt || now();
        }

        targetUrl() {
            return (
                this.data.url ||
                this.data.target ||
                this.provenance.candidateTarget ||
                null
            );
        }

        serialize() {
            return { ...this };
        }
    }

    /*
     * ============================================================
     * RESOURCE
     * ============================================================
     */

    class ResourceRecord {
        constructor(data = {}) {
            this.url =
                data.url || '';

            this.types =
                safeArray(data.types);

            this.mechanisms =
                safeArray(data.mechanisms);

            this.parents =
                safeArray(data.parents);

            this.candidateIds =
                safeArray(data.candidateIds);

            this.observationIds =
                safeArray(data.observationIds);

            this.discoveryIds =
                safeArray(data.discoveryIds);

            this.networkEventIds =
                safeArray(data.networkEventIds);

            this.createdAt =
                data.createdAt || now();

            this.updatedAt =
                data.updatedAt || now();

            this.status =
                data.status || 'known';

            this.fingerprint =
                data.fingerprint || null;

            this.finalUrl =
                data.finalUrl || null;

            this.skipReason =
                data.skipReason || null;
        }

        merge(data = {}) {
            this.updatedAt = now();

            if (data.type) {
                this.types.push(data.type);
                this.types = unique(this.types);
            }

            if (data.mechanism) {
                this.mechanisms.push(data.mechanism);
                this.mechanisms =
                    unique(this.mechanisms);
            }

            for (const field of [
                'parents',
                'candidateIds',
                'observationIds',
                'discoveryIds',
                'networkEventIds'
            ]) {
                if (data[field]) {
                    this[field] = unique([
                        ...this[field],
                        ...data[field]
                    ]);
                }
            }

            if (data.status) {
                this.status = data.status;
            }

            if (data.fingerprint) {
                this.fingerprint =
                    data.fingerprint;
            }

            if (data.finalUrl) {
                this.finalUrl =
                    data.finalUrl;
            }

            if (data.skipReason) {
                this.skipReason =
                    data.skipReason;
            }
        }

        serialize() {
            return { ...this };
        }
    }

    /*
     * ============================================================
     * KNOWLEDGE BASE
     * ============================================================
     */

    class KnowledgeBase {
        constructor() {
            this.candidates = new Map();
            this.candidateKeys = new Map();

            this.observations = new Map();
            this.discoveries = new Map();
            this.resources = new Map();

            this.visited = new Set();
            this.claimed = new Set();

            this.graphEdges = [];

            this.networkEvents = new Map();

            this.fingerprintIndex = new Map();

            this.patternIndex = new Map();
            this.clusterIndex = new Map();

            this.diagnostics = [];

            this.stats = {
                discovered: 0,
                queued: 0,
                claimed: 0,
                planned: 0,
                acquired: 0,
                recognized: 0,
                expanded: 0,
                completed: 0,
                skipped: 0,
                failed: 0,
                retried: 0
            };
        }

        addCandidate(candidate, discovery = null) {
            if (!(candidate instanceof Candidate)) {
                candidate =
                    new Candidate(candidate);
            }

            const canonical =
                canonicalizeUrl(candidate.target);

            if (!canonical) {
                return null;
            }

            candidate.target = canonical;

            if (!isAllowedUrl(candidate.target)) {
                return null;
            }

            const key =
                candidate.identityKey();

            const existingId =
                this.candidateKeys.get(key);

            if (existingId) {
                const existing =
                    this.candidates.get(existingId);

                if (existing) {
                    existing.alternateTypes =
                        unique([
                            ...existing.alternateTypes,
                            candidate.type
                        ]);

                    if (candidate.parent) {
                        existing.alternateParents =
                            unique([
                                ...existing.alternateParents,
                                candidate.parent
                            ]);
                    }

                    existing.priority =
                        Math.max(
                            existing.priority,
                            candidate.priority
                        );

                    return existing;
                }
            }

            if (this.visited.has(key)) {
                this.recordDiagnostic(
                    'candidate-visited',
                    {
                        key,
                        target: candidate.target
                    }
                );

                return null;
            }

            // P0-1 FIX: count live only (exclude completed/skipped)
            const liveCount = [...this.candidates.values()].filter(
                c =>
                    !['completed', 'skipped'].includes(
                        c.status
                    )
            ).length;

            if (
                liveCount >= CONFIG.maxCandidates
            ) {
                this.recordDiagnostic(
                    'candidate-cap-reached',
                    {
                        target: candidate.target,
                        liveCount,
                        cap: CONFIG.maxCandidates
                    }
                );

                return null;
            }

            this.candidates.set(
                candidate.id,
                candidate
            );

            this.candidateKeys.set(
                key,
                candidate.id
            );

            this.stats.discovered++;

            this.recordPattern(candidate);

            if (discovery) {
                this.addEdge(
                    discovery.candidateId,
                    candidate.id,
                    discovery.mechanism
                );
            }

            return candidate;
        }

        queueCandidate(candidate) {
            if (!candidate) return;
            this._validateTransition(candidate, 'queued');

            if (
                candidate.status ===
                    'completed' ||
                candidate.status ===
                    'skipped'
            ) {
                return;
            }

            candidate.status = 'queued';
            candidate.queuedAt = now();

            this.stats.queued++;
        }

        claimNextCandidate() {
            const eligible = [];

            for (const candidate of this.candidates.values()) {
                if (
                    candidate.status !== 'queued' &&
                    candidate.status !== 'failed'
                ) {
                    continue;
                }

                if (
                    candidate.nextAttemptAt &&
                    candidate.nextAttemptAt > now()
                ) {
                    continue;
                }

                if (
                    CONFIG.candidateTTL > 0 &&
                    candidate.createdAt &&
                    now() - candidate.createdAt > CONFIG.candidateTTL
                ) {
                    this.markSkipped(candidate, 'ttl-expired');
                    this.recordDiagnostic('candidate-ttl-expired', {
                        id: candidate.id,
                        target: candidate.target,
                        age: now() - candidate.createdAt,
                        ttl: CONFIG.candidateTTL
                    });
                    continue;
                }

                eligible.push(candidate);
            }

            eligible.sort(
                (a, b) =>
                    b.effectivePriority() -
                    a.effectivePriority()
            );

            const candidate = eligible[0];

            if (!candidate) {
                return null;
            }

            this._validateTransition(candidate, 'claimed');
            candidate.status = 'claimed';
            candidate.claimedAt = now();

            this.claimed.add(candidate.id);
            this.stats.claimed++;

            return candidate;
        }

        markPlanned(candidate) {
            this._validateTransition(candidate, 'planned');
            candidate.status = 'planned';
            candidate.plannedAt = now();
            this.stats.planned++;
        }

        markAcquiring(candidate) {
            this._validateTransition(candidate, 'acquiring');
            candidate.status = 'acquiring';
            candidate.acquiringAt = now();
        }

        markObserved(candidate) {
            this._validateTransition(candidate, 'observed');
            candidate.status = 'observed';
            candidate.observedAt = now();
        }

        markRecognized(candidate) {
            this._validateTransition(candidate, 'recognized');
            candidate.status = 'recognized';
            candidate.recognizedAt = now();
            this.stats.recognized++;
        }

        markExpanded(candidate) {
            this._validateTransition(candidate, 'expanded');
            candidate.status = 'expanded';
            candidate.expandedAt = now();
            this.stats.expanded++;
        }

        markCompleted(candidate) {
            this._validateTransition(candidate, 'completed');
            candidate.status = 'completed';
            candidate.completedAt = now();
            this.visited.add(candidate.identityKey());
            this.stats.completed++;
        }

        markSkipped(candidate, reason) {
            this._validateTransition(candidate, 'skipped');
            candidate.status = 'skipped';
            candidate.skippedAt = now();
            this.visited.add(candidate.identityKey());

            const resource =
                this.ensureResource(candidate.target);

            resource.merge({
                status: 'skipped',
                skipReason: reason,
                candidateIds: [candidate.id]
            });

            this.stats.skipped++;
        }

        markFailed(candidate) {
            this._validateTransition(candidate, 'failed');
            candidate.status = 'failed';
            candidate.failedAt = now();
            this.stats.failed++;
        }

        retryCandidate(candidate, reason) {
            candidate.attempts++;

            if (
                candidate.attempts >
                CONFIG.retry.maxRetries
            ) {
                this.markFailed(candidate);
                return false;
            }

            const delay = Math.min(
                CONFIG.retry.maxDelay,
                CONFIG.retry.baseDelay *
                    Math.pow(
                        2,
                        candidate.attempts - 1
                    )
            );

            candidate.nextAttemptAt =
                now() + delay;

            this._validateTransition(candidate, 'queued');
            candidate.status = 'queued';

            this.stats.retried++;

            return true;
        }

        recordObservation(observation) {
            // P0-3: cap in-memory observations (FIFO) to avoid unbounded heap
            if (
                this.observations.size >=
                CONFIG.maxObservationsInMemory
            ) {
                const firstKey = this.observations.keys().next().value;
                if (firstKey) this.observations.delete(firstKey);
                this.recordDiagnostic('observation-evicted', {
                    max: CONFIG.maxObservationsInMemory
                });
            }

            this.observations.set(
                observation.id,
                observation
            );

            const _oldHash = (() => {
                try {
                    const prev = this.resources.get(
                        canonicalizeUrl(observation.requestedUrl) ||
                            observation.requestedUrl
                    );
                    return prev?.fingerprint?.hash || null;
                } catch {
                    return null;
                }
            })();

            const resource =
                this.ensureResource(
                    observation.requestedUrl
                );

            resource.merge({
                observationIds: [
                    observation.id
                ],
                candidateIds: [
                    observation.candidateId
                ],
                status:
                    observation.status ===
                    'success'
                        ? 'acquired'
                        : 'observed',
                fingerprint:
                    observation.fingerprint,
                finalUrl:
                    observation.http?.finalUrl
            });

            if (observation.fingerprint) {
                const hash =
                    observation.fingerprint.hash;

                if (!this.fingerprintIndex.has(hash)) {
                    this.fingerprintIndex.set(
                        hash,
                        new Set()
                    );
                }

                this.fingerprintIndex
                    .get(hash)
                    .add(observation.requestedUrl);

                if (
                    CONFIG.changeDetection &&
                    _oldHash &&
                    hash !== _oldHash
                ) {
                    this.recordDiagnostic('resource-changed', {
                        target: observation.requestedUrl,
                        oldHash: _oldHash,
                        newHash: hash
                    });
                    // mark resource as changed (overwrites acquired)
                    try {
                        const res = this.resources.get(
                            canonicalizeUrl(observation.requestedUrl) ||
                                observation.requestedUrl
                        );
                        if (res) res.status = 'changed';
                    } catch {}
                }
            }
        }

        addDiscovery(discovery) {
            this.discoveries.set(
                discovery.id,
                discovery
            );

            const target =
                discovery.targetUrl();

            if (target) {
                const canonical =
                    canonicalizeUrl(target);

                if (canonical) {
                    const resource =
                        this.ensureResource(canonical);

                    resource.merge({
                        mechanisms: [
                            discovery.mechanism
                        ],
                        discoveryIds: [
                            discovery.id
                        ]
                    });
                }
            }
        }

        ensureResource(url) {
            const canonical =
                canonicalizeUrl(url);

            if (!canonical) {
                return null;
            }

            let resource =
                this.resources.get(canonical);

            if (!resource) {
                resource =
                    new ResourceRecord({
                        url: canonical
                    });

                this.resources.set(
                    canonical,
                    resource
                );
            }

            return resource;
        }

        addEdge(from, to, relation) {
            if (!from || !to) return;

            if (
                this.graphEdges.length >=
                CONFIG.maxGraphEdges
            ) {
                return;
            }

            this.graphEdges.push({
                id: makeId('edge'),
                from,
                to,
                relation,
                createdAt: now()
            });
        }

        recordDiagnostic(type, data = {}) {
            this.diagnostics.push({
                id: makeId('diag'),
                type,
                timestamp: now(),
                data
            });

            if (
                this.diagnostics.length >
                CONFIG.maxDiagnostics
            ) {
                this.diagnostics.shift();
            }
        }

        _validateTransition(candidate, to) {
            const from = candidate.status;
            if (from === to) return true;
            const allowed = {
                discovered: ['queued'],
                queued: ['claimed', 'skipped', 'failed'],
                claimed: ['planned', 'skipped'],
                planned: ['acquiring', 'completed', 'skipped'],
                acquiring: ['observed'],
                observed: ['recognized', 'completed', 'queued', 'failed'],
                recognized: ['expanded'],
                expanded: ['completed'],
                completed: [],
                skipped: [],
                failed: ['queued']
            };
            const ok = (allowed[from] || []).includes(to);
            if (!ok) {
                this.recordDiagnostic('lifecycle-illegal-transition', {
                    id: candidate.id,
                    target: candidate.target,
                    from,
                    to,
                    allowed: allowed[from] || []
                });
                if (CONFIG.lifecycle && CONFIG.lifecycle.strict) {
                    throw new Error(`lifecycle illegal: ${from} -> ${to}`);
                }
            }
            return ok || !(CONFIG.lifecycle && CONFIG.lifecycle.strict);
        }

        recordPattern(candidate) {
            if (!CONFIG.inference || !CONFIG.inference.patternInference) return;
            try {
                const pattern = extractUrlPattern(candidate.target);
                this.patternIndex.set(pattern, (this.patternIndex.get(pattern) || 0) + 1);
                if (CONFIG.inference.clustering) {
                    const key = clusterKeyForCandidate(candidate);
                    this.clusterIndex.set(key, (this.clusterIndex.get(key) || 0) + 1);
                }
            } catch {}
        }

        getPatternMetrics() {
            const sorted = [...this.patternIndex.entries()].sort((a, b) => b[1] - a[1]).slice(0, 20);
            return { size: this.patternIndex.size, top: sorted, total: [...this.patternIndex.values()].reduce((a, b) => a + b, 0) };
        }

        getClusterMetrics() {
            const sorted = [...this.clusterIndex.entries()].sort((a, b) => b[1] - a[1]).slice(0, 20);
            return { size: this.clusterIndex.size, top: sorted, total: [...this.clusterIndex.values()].reduce((a, b) => a + b, 0) };
        }

        suggestPatternCandidates(limit = CONFIG.patternGuided?.maxSuggestions || 5) {
            if (!CONFIG.patternGuided?.enabled || !CONFIG.inference?.patternInference) return [];
            const metrics = this.getPatternMetrics();
            const suggestions = [];
            for (const [pattern, count] of metrics.top) {
                if (count < (CONFIG.inference.minPatternFreq || 3)) continue;
                if (!pattern.includes('{int}') && !pattern.includes('{hash}') && !pattern.includes('{uuid}')) continue;
                let suggestion = pattern;
                // deterministic replacements
                suggestion = suggestion.replace('{int}', '0');
                suggestion = suggestion.replace('{hash}', '0'.repeat(32));
                suggestion = suggestion.replace('{uuid}', '00000000-0000-4000-a000-000000000000');
                // handle query patterns like ?id={int}
                suggestion = suggestion.replace('={int}', '=0').replace('={hash}', '='+'0'.repeat(32)).replace('={uuid}', '=00000000-0000-4000-a000-000000000000');
                const key = `url:${suggestion}`;
                if (this.visited.has(key) || this.candidateKeys.has(key)) continue;
                // also need isAllowedUrl check (sameOriginOnly)
                try { if (!isAllowedUrl(suggestion)) continue; } catch { continue; }
                suggestions.push({ pattern, count, suggestion });
                if (suggestions.length >= limit) break;
            }
            return suggestions;
        }

        getChangedResources() {
            return [...this.resources.values()].filter(r => r.status === 'changed');
        }

        shouldAcquireResource(url) {
            const resource =
                this.resources.get(
                    canonicalizeUrl(url)
                );

            return !resource ||
                resource.status !== 'acquired';
        }

        serialize() {
            return {
                version: CONFIG.version,

                candidates: [
                    ...this.candidates.values()
                ].map(c => c.serialize()),

                observations: [
                    ...this.observations.values()
                ].map(o => o.serialize()),

                discoveries: [
                    ...this.discoveries.values()
                ]
                    .slice(-CONFIG.persistedDiscoveries)
                    .map(d => d.serialize()),

                resources: [
                    ...this.resources.values()
                ]
                    .slice(-CONFIG.persistedResources)
                    .map(r => r.serialize()),

                visited: [
                    ...this.visited
                ],

                graphEdges:
                    this.graphEdges.slice(
                        -CONFIG.persistedEdges
                    ),

                stats: {
                    ...this.stats
                }
            };
        }

        restore(data) {
            if (!data) return;

            for (const raw of safeArray(
                data.candidates
            )) {
                const candidate =
                    new Candidate(raw);

                this.candidates.set(
                    candidate.id,
                    candidate
                );

                this.candidateKeys.set(
                    candidate.identityKey(),
                    candidate.id
                );
            }

            for (const raw of safeArray(
                data.observations
            )) {
                const observation =
                    new Observation(raw);

                this.observations.set(
                    observation.id,
                    observation
                );
            }

            for (const raw of safeArray(
                data.discoveries
            )) {
                const discovery =
                    new Discovery(raw);

                this.discoveries.set(
                    discovery.id,
                    discovery
                );
            }

            for (const raw of safeArray(
                data.resources
            )) {
                const resource =
                    new ResourceRecord(raw);

                this.resources.set(
                    resource.url,
                    resource
                );
            }

            this.visited =
                new Set(
                    safeArray(data.visited)
                );

            this.graphEdges =
                safeArray(data.graphEdges);

            for (const resource of this.resources.values()) {
                if (resource.fingerprint?.hash) {
                    const hash =
                        resource.fingerprint.hash;

                    if (
                        !this.fingerprintIndex.has(hash)
                    ) {
                        this.fingerprintIndex.set(
                            hash,
                            new Set()
                        );
                    }

                    this.fingerprintIndex
                        .get(hash)
                        .add(resource.url);
                }
            }
        }
    }

    /*
     * ============================================================
     * ACQUISITION POLICY
     * ============================================================
     */

    class Provider {
        constructor(name) {
            this.name = name;
        }

        matches() {
            return false;
        }

        async recognize() {
            return [];
        }
    }

    /*
     * ============================================================
     * HTML PROVIDER
     * ============================================================
     */

    class HtmlProvider extends Provider {
        constructor() {
            super('html');
        }

        matches(observation) {
            return looksLikeHtml(
                observation.http?.contentType,
                observation.body
            );
        }

        async recognize(candidate, observation) {
            const discoveries = [];

            let doc;

            try {
                const parser =
                    new DOMParser();

                doc =
                    parser.parseFromString(
                        observation.body,
                        'text/html'
                    );
            } catch {
                return discoveries;
            }

            const emit =
                (
                    url,
                    type,
                    mechanism,
                    confidence = 0.7,
                    hints = {}
                ) => {
                    if (!url) return;

                    const canonical =
                        canonicalizeUrl(
                            url
                        );

                    if (!canonical) return;

                    discoveries.push(
                        new Discovery({
                            candidateId:
                                candidate.id,

                            observationId:
                                observation.id,

                            kind: type,

                            confidence,

                            mechanism,

                            data: {
                                url: canonical
                            },

                            provenance: {
                                origin:
                                    candidate.origin,

                                parent:
                                    candidate.target,

                                candidateTarget:
                                    candidate.target,

                                candidateType:
                                    candidate.type,

                                mechanism,

                                depth:
                                    candidate.depth,

                                hints
                            }
                        })
                    );
                };

            for (
                const element of
                doc.querySelectorAll(
                    'a[href], area[href]'
                )
            ) {
                emit(
                    element.href,
                    'url',
                    'html-link',
                    0.85
                );
            }

            for (
                const element of
                doc.querySelectorAll(
                    'script[src]'
                )
            ) {
                emit(
                    element.src,
                    'script',
                    'html-script',
                    0.80
                );
            }

            for (
                const element of
                doc.querySelectorAll(
                    'link[href]'
                )
            ) {
                const rel =
                    String(
                        element.rel || ''
                    ).toLowerCase();

                let type =
                    'resource';

                if (
                    rel.includes('stylesheet')
                ) {
                    type = 'stylesheet';
                } else if (
                    rel.includes('manifest')
                ) {
                    type = 'manifest';
                } else if (
                    rel.includes('alternate')
                ) {
                    type = 'feed';
                } else if (
                    rel.includes('sitemap')
                ) {
                    type = 'sitemap';
                }

                emit(
                    element.href,
                    type,
                    `html-link-rel:${rel || 'none'}`,
                    0.75
                );
            }

            for (
                const element of
                doc.querySelectorAll(
                    'iframe[src], frame[src]'
                )
            ) {
                emit(
                    element.src,
                    'frame',
                    'html-frame',
                    0.65
                );
            }

            for (
                const element of
                doc.querySelectorAll(
                    'img[src], video[src], audio[src], source[src]'
                )
            ) {
                emit(
                    element.src,
                    'media',
                    'html-media',
                    0.50,
                    {
                        binary: true
                    }
                );
            }

            for (
                const element of
                doc.querySelectorAll(
                    'object[data], embed[src]'
                )
            ) {
                emit(
                    element.data ||
                    element.src,
                    'embedded',
                    'html-embedded',
                    0.45,
                    {
                        binary: true
                    }
                );
            }

            for (
                const element of
                doc.querySelectorAll(
                    'form[action]'
                )
            ) {
                emit(
                    element.action,
                    'form',
                    'html-form-action',
                    0.55,
                    {
                        method:
                            String(
                                element.method ||
                                'GET'
                            ).toUpperCase()
                    }
                );
            }

            const base =
                doc.querySelector(
                    'base[href]'
                );

            const baseHref =
                base?.href || null;

            for (
                const meta of
                doc.querySelectorAll(
                    'meta[content]'
                )
            ) {
                const httpEquiv =
                    String(
                        meta.httpEquiv || ''
                    ).toLowerCase();

                if (
                    httpEquiv ===
                    'refresh'
                ) {
                    const match =
                        meta.content.match(
                            /url\s*=\s*(.+)$/i
                        );

                    if (match) {
                        emit(
                            new URL(
                                match[1].trim(),
                                baseHref ||
                                    observation.requestedUrl
                            ).href,
                            'url',
                            'meta-refresh',
                            0.70
                        );
                    }
                }
            }

            for (
                const selector of [
                    'link[rel="canonical"]',
                    'meta[property="og:url"]',
                    'meta[name="twitter:url"]'
                ]
            ) {
                const element =
                    doc.querySelector(
                        selector
                    );

                const value =
                    element?.href ||
                    element?.content;

                if (value) {
                    emit(
                        value,
                        'metadata',
                        'metadata-url',
                        0.90
                    );
                }
            }

            const htmlText =
                doc.documentElement?.outerHTML ||
                observation.body;

            for (
                const raw of
                extractUrlsFromText(
                    htmlText
                )
            ) {
                emit(
                    raw,
                    looksLikeApiUrl(raw)
                        ? 'api'
                        : 'url',
                    'html-embedded-url',
                    0.45
                );
            }

            return discoveries;
        }
    }

    /*
     * ============================================================
     * JSON PROVIDER
     * ============================================================
     */

    class JsonProvider extends Provider {
        constructor() {
            super('json');
        }

        matches(observation) {
            return looksLikeJson(
                observation.http?.contentType,
                observation.body
            );
        }

        async recognize(candidate, observation) {
            const discoveries = [];

            let parsed;

            try {
                parsed =
                    JSON.parse(
                        observation.body
                    );
            } catch {
                return discoveries;
            }

            const walk =
                (value, path = '$') => {
                    if (typeof value === 'string') {
                        const canonical =
                            canonicalizeUrl(
                                value
                            );

                        if (
                            canonical &&
                            isAllowedUrl(
                                canonical
                            )
                        ) {
                            discoveries.push(
                                new Discovery({
                                    candidateId:
                                        candidate.id,

                                    observationId:
                                        observation.id,

                                    kind:
                                        looksLikeApiUrl(
                                            canonical
                                        )
                                            ? 'api'
                                            : 'url',

                                    confidence:
                                        0.75,

                                    mechanism:
                                        'json-url',

                                    data: {
                                        url:
                                            canonical,
                                        path
                                    },

                                    provenance: {
                                        origin:
                                            candidate.origin,
                                        parent:
                                            candidate.target,
                                        candidateTarget:
                                            candidate.target,
                                        candidateType:
                                            candidate.type,
                                        mechanism:
                                            'json-url',
                                        depth:
                                            candidate.depth
                                    }
                                })
                            );
                        }

                        return;
                    }

                    if (
                        Array.isArray(value)
                    ) {
                        value.forEach(
                            (item, index) =>
                                walk(
                                    item,
                                    `${path}[${index}]`
                                )
                        );

                        return;
                    }

                    if (
                        value &&
                        typeof value ===
                            'object'
                    ) {
                        for (
                            const [
                                key,
                                child
                            ] of Object.entries(
                                value
                            )
                        ) {
                            walk(
                                child,
                                `${path}.${key}`
                            );
                        }
                    }
                };

            walk(parsed);

            return discoveries;
        }
    }

    /*
     * ============================================================
     * XML PROVIDER
     * ============================================================
     */

    class XmlProvider extends Provider {
        constructor() {
            super('xml');
        }

        matches(observation) {
            return looksLikeXml(
                observation.http?.contentType,
                observation.body
            );
        }

        async recognize(candidate, observation) {
            const discoveries = [];

            const locs =
                extractXmlLocs(
                    observation.body
                );

            for (const loc of locs) {
                const url =
                    canonicalizeUrl(
                        loc
                    );

                if (!url) continue;

                discoveries.push(
                    new Discovery({
                        candidateId:
                            candidate.id,

                        observationId:
                            observation.id,

                        kind:
                            candidate.type ===
                            'sitemap'
                                ? 'url'
                                : 'xml',

                        confidence:
                            candidate.type ===
                            'sitemap'
                                ? 0.90
                                : 0.70,

                        mechanism:
                            'xml-loc',

                        data: {
                            url
                        },

                        provenance: {
                            origin:
                                candidate.origin,

                            parent:
                                candidate.target,

                            candidateTarget:
                                candidate.target,

                            candidateType:
                                candidate.type,

                            mechanism:
                                'xml-loc',

                            depth:
                                candidate.depth
                        }
                    })
                );
            }

            return discoveries;
        }
    }

    /*
     * ============================================================
     * CSS PROVIDER
     * ============================================================
     */

    class CssProvider extends Provider {
        constructor() {
            super('css');
        }

        matches(observation) {
            return looksLikeCss(
                observation.http?.contentType
            );
        }

        async recognize(candidate, observation) {
            const discoveries = [];

            for (
                const raw of
                extractCssUrls(
                    observation.body
                )
            ) {
                const url =
                    canonicalizeUrl(
                        new URL(
                            raw,
                            observation.requestedUrl
                        ).href
                    );

                if (!url) continue;

                discoveries.push(
                    new Discovery({
                        candidateId:
                            candidate.id,

                        observationId:
                            observation.id,

                        kind: 'resource',

                        confidence: 0.60,

                        mechanism:
                            'css-url',

                        data: {
                            url
                        },

                        provenance: {
                            origin:
                                candidate.origin,

                            parent:
                                candidate.target,

                            candidateTarget:
                                candidate.target,

                            candidateType:
                                candidate.type,

                            mechanism:
                                'css-url',

                            depth:
                                candidate.depth
                        }
                    })
                );
            }

            return discoveries;
        }
    }

    /*
     * ============================================================
     * JAVASCRIPT PROVIDER
     * ============================================================
     */

    class JavaScriptProvider extends Provider {
        constructor() {
            super('javascript');
        }

        matches(observation) {
            return looksLikeJavaScript(
                observation.http?.contentType
            );
        }

        async recognize(candidate, observation) {
            const discoveries = [];

            for (
                const raw of
                extractUrlsFromText(
                    observation.body
                )
            ) {
                const url =
                    canonicalizeUrl(
                        raw
                    );

                if (!url) continue;

                discoveries.push(
                    new Discovery({
                        candidateId:
                            candidate.id,

                        observationId:
                            observation.id,

                        kind:
                            looksLikeApiUrl(url)
                                ? 'api'
                                : 'url',

                        confidence:
                            looksLikeApiUrl(url)
                                ? 0.65
                                : 0.45,

                        mechanism:
                            'javascript-url',

                        data: {
                            url
                        },

                        provenance: {
                            origin:
                                candidate.origin,

                            parent:
                                candidate.target,

                            candidateTarget:
                                candidate.target,

                            candidateType:
                                candidate.type,

                            mechanism:
                                'javascript-url',

                            depth:
                                candidate.depth
                        }
                    })
                );
            }

            return discoveries;
        }
    }

    /*
     * ============================================================
     * TEXT PROVIDER
     * ============================================================
     */

    class TextProvider extends Provider {
        constructor() {
            super('text');
        }

        matches(observation) {
            const type =
                contentTypeBase(
                    observation.http
                        ?.contentType
                );

            return (
                type.startsWith('text/') ||
                type === ''
            );
        }

        async recognize(candidate, observation) {
            const discoveries = [];

            for (
                const raw of
                extractUrlsFromText(
                    observation.body
                )
            ) {
                const url =
                    canonicalizeUrl(raw);

                if (!url) continue;

                discoveries.push(
                    new Discovery({
                        candidateId:
                            candidate.id,

                        observationId:
                            observation.id,

                        kind:
                            looksLikeApiUrl(url)
                                ? 'api'
                                : 'url',

                        confidence: 0.40,

                        mechanism:
                            'text-url',

                        data: {
                            url
                        },

                        provenance: {
                            origin:
                                candidate.origin,

                            parent:
                                candidate.target,

                            candidateTarget:
                                candidate.target,

                            candidateType:
                                candidate.type,

                            mechanism:
                                'text-url',

                            depth:
                                candidate.depth
                        }
                    })
                );
            }

            return discoveries;
        }
    }

    /*
     * ============================================================
     * BINARY PROVIDER
     * ============================================================
     */

    class RobotsProvider extends Provider {
        constructor() {
            super('robots');
        }

        matches(observation) {
            const url = String(observation.requestedUrl || observation.target || '');
            if (/robots\.txt$/i.test(url)) return true;
            const ct = contentTypeBase(observation.http?.contentType || '');
            return ct === 'text/plain' && /User-agent:/i.test(String(observation.body || ''));
        }

        async recognize(candidate, observation) {
            const discoveries = [];
            const re = /Sitemap:\s*(https?:\/\/\S+)/gi;
            for (const m of String(observation.body || '').matchAll(re)) {
                const url = canonicalizeUrl(m[1].trim());
                if (!url) continue;
                discoveries.push(
                    new Discovery({
                        candidateId: candidate.id,
                        observationId: observation.id,
                        kind: 'sitemap',
                        confidence: 0.92,
                        mechanism: 'robots-sitemap',
                        data: { url },
                        provenance: {
                            origin: candidate.origin,
                            parent: candidate.target,
                            candidateTarget: candidate.target,
                            candidateType: candidate.type,
                            mechanism: 'robots-sitemap',
                            depth: candidate.depth
                        }
                    })
                );
            }
            return discoveries;
        }
    }

    class HeadersProvider extends Provider {
        constructor() {
            super('headers');
        }

        matches(observation) {
            const h = observation.http?.headers;
            if (!h || typeof h !== 'object') return false;
            const link = h['link'] || h['Link'] || h['LINK'] || h['Link'.toLowerCase()];
            if (link && /<https?:\/\/[^>]+>/.test(String(link))) return true;
            const loc = h['location'] || h['Location'] || h['LOCATION'];
            if (loc && isAllowedUrl(String(loc))) return true;
            return false;
        }

        async recognize(candidate, observation) {
            const discoveries = [];
            const h = observation.http?.headers || {};
            const emit = (url, type, mechanism, confidence) => {
                const canonical = canonicalizeUrl(url);
                if (!canonical) return;
                discoveries.push(
                    new Discovery({
                        candidateId: candidate.id,
                        observationId: observation.id,
                        kind: type,
                        confidence,
                        mechanism,
                        data: { url: canonical },
                        provenance: {
                            origin: candidate.origin,
                            parent: candidate.target,
                            candidateTarget: candidate.target,
                            candidateType: candidate.type,
                            mechanism,
                            depth: candidate.depth
                        }
                    })
                );
            };
            const linkVal = String(h['link'] || h['Link'] || h['LINK'] || '');
            const linkRe = /<([^>]+)>/g;
            for (const m of linkVal.matchAll(linkRe)) {
                emit(m[1].trim(), 'url', 'headers-link', 0.88);
            }
            const loc = h['location'] || h['Location'] || h['LOCATION'];
            if (loc) {
                emit(String(loc).trim(), 'url', 'headers-location', 0.90);
            }
            return discoveries;
        }
    }

    class SitemapIndexProvider extends Provider {
        constructor() {
            super('sitemapIndex');
        }

        matches(observation) {
            const ct = contentTypeBase(observation.http?.contentType || '');
            const body = String(observation.body || '');
            // sitemap index is XML with <sitemapindex> root
            if (/sitemapindex/i.test(body)) return true;
            if (ct.includes('xml') && /<sitemap/i.test(body)) return looksLikeXml(observation.http?.contentType, body);
            const url = String(observation.requestedUrl || observation.target || '');
            if (/sitemap.*\.xml$/i.test(url) && /<loc>/i.test(body)) return true;
            return false;
        }

        async recognize(candidate, observation) {
            const discoveries = [];
            const locs = extractXmlLocs(observation.body);
            for (const loc of locs) {
                const url = canonicalizeUrl(loc);
                if (!url) continue;
                discoveries.push(
                    new Discovery({
                        candidateId: candidate.id,
                        observationId: observation.id,
                        kind: 'sitemap',
                        confidence: 0.90,
                        mechanism: 'sitemap-index-loc',
                        data: { url },
                        provenance: {
                            origin: candidate.origin,
                            parent: candidate.target,
                            candidateTarget: candidate.target,
                            candidateType: candidate.type,
                            mechanism: 'sitemap-index-loc',
                            depth: candidate.depth
                        }
                    })
                );
            }
            return discoveries;
        }
    }

    class OpenApiProvider extends Provider {
        constructor() {
            super('openapi');
        }

        matches(observation) {
            if (!looksLikeJson(observation.http?.contentType, observation.body)) return false;
            try {
                const parsed = JSON.parse(String(observation.body||''));
                if (parsed && typeof parsed === 'object') {
                    if (parsed.openapi || parsed.swagger) return true;
                    if (parsed.info && parsed.paths && typeof parsed.paths === 'object') return true;
                }
            } catch {}
            return false;
        }

        async recognize(candidate, observation) {
            const discoveries = [];
            let parsed;
            try { parsed = JSON.parse(String(observation.body||'')); } catch { return discoveries; }
            const emit = (url, confidence, mechanism) => {
                const canonical = canonicalizeUrl(url);
                if (!canonical || !isAllowedUrl(canonical)) return;
                discoveries.push(
                    new Discovery({
                        candidateId: candidate.id,
                        observationId: observation.id,
                        kind: looksLikeApiUrl(canonical) ? 'api' : 'url',
                        confidence,
                        mechanism,
                        data: { url: canonical },
                        provenance: {
                            origin: candidate.origin,
                            parent: candidate.target,
                            candidateTarget: candidate.target,
                            candidateType: candidate.type,
                            mechanism,
                            depth: candidate.depth
                        }
                    })
                );
            };
            // servers[].url (OpenAPI 3)
            if (Array.isArray(parsed.servers)) {
                for (const srv of parsed.servers) {
                    if (srv && typeof srv.url === 'string') emit(srv.url, 0.95, 'openapi-server');
                }
            }
            // swagger basePath + host → approximate server url
            if (parsed.swagger && parsed.host) {
                const host = String(parsed.host || '').trim();
                const base = String(parsed.basePath || '');
                if (host) {
                    const scheme = Array.isArray(parsed.schemes) && parsed.schemes[0] ? String(parsed.schemes[0]) : 'https';
                    emit(`${scheme}://${host}${base}`, 0.90, 'openapi-host');
                }
            }
            // also walk for any URL-like strings (reuse JsonProvider walk but with higher confidence for api)
            const walk = (value) => {
                if (typeof value === 'string') {
                    const canonical = canonicalizeUrl(value);
                    if (canonical && isAllowedUrl(canonical) && looksLikeApiUrl(canonical)) {
                        // avoid double-emitting servers already emitted
                        if (!discoveries.some(d => d.data.url === canonical)) {
                            emit(canonical, 0.85, 'openapi-url');
                        }
                    }
                    return;
                }
                if (Array.isArray(value)) { value.forEach(walk); return; }
                if (value && typeof value === 'object') { Object.values(value).forEach(walk); }
            };
            walk(parsed);
            return discoveries;
        }
    }

    class WellKnownProvider extends Provider {
        constructor() {
            super('wellKnown');
        }

        matches(observation) {
            const url = String(observation.requestedUrl || observation.target || '');
            if (/\/\.well-known\//i.test(url)) return true;
            const ct = contentTypeBase(observation.http?.contentType || '');
            const body = String(observation.body || '');
            if (ct === 'text/plain' && /Contact:|Encryption:|Acknowledgments:/i.test(body) && /\/\.well-known\//i.test(url)) return true;
            if (looksLikeJson(ct, body) && /\/\.well-known\//i.test(url)) return true;
            return false;
        }

        async recognize(candidate, observation) {
            const discoveries = [];
            const body = String(observation.body || '');
            const ct = contentTypeBase(observation.http?.contentType || '');
            // JSON well-known (assetlinks.json, openid-configuration)
            if (looksLikeJson(ct, body)) {
                try {
                    const parsed = JSON.parse(body);
                    const walk = (value) => {
                        if (typeof value === 'string') {
                            const canonical = canonicalizeUrl(value);
                            if (canonical && isAllowedUrl(canonical)) {
                                discoveries.push(new Discovery({
                                    candidateId: candidate.id,
                                    observationId: observation.id,
                                    kind: looksLikeApiUrl(canonical) ? 'api' : 'url',
                                    confidence: 0.80,
                                    mechanism: 'wellknown-json-url',
                                    data: { url: canonical },
                                    provenance: { origin: candidate.origin, parent: candidate.target, candidateTarget: candidate.target, candidateType: candidate.type, mechanism: 'wellknown-json-url', depth: candidate.depth }
                                }));
                            }
                            return;
                        }
                        if (Array.isArray(value)) { value.forEach(walk); return; }
                        if (value && typeof value === 'object') { Object.values(value).forEach(walk); }
                    };
                    walk(parsed);
                    return discoveries;
                } catch {}
            }
            // text well-known (security.txt)
            for (const raw of extractUrlsFromText(body)) {
                const url = canonicalizeUrl(raw);
                if (!url) continue;
                discoveries.push(new Discovery({
                    candidateId: candidate.id,
                    observationId: observation.id,
                    kind: looksLikeApiUrl(url) ? 'api' : 'url',
                    confidence: 0.70,
                    mechanism: 'wellknown-text-url',
                    data: { url },
                    provenance: { origin: candidate.origin, parent: candidate.target, candidateTarget: candidate.target, candidateType: candidate.type, mechanism: 'wellknown-text-url', depth: candidate.depth }
                }));
            }
            return discoveries;
        }
    }

    class ManifestProvider extends Provider {
        constructor() {
            super('manifest');
        }

        matches(observation) {
            const url = String(observation.requestedUrl || observation.target || '');
            const ct = contentTypeBase(observation.http?.contentType || '');
            if (/manifest\.json$/i.test(url)) return true;
            if (ct === 'application/manifest+json' || ct === 'application/json' && /manifest/i.test(url)) return true;
            if (looksLikeJson(ct, observation.body)) {
                try {
                    const p = JSON.parse(String(observation.body||''));
                    if (p && typeof p === 'object' && (p.icons || p.start_url || p.scope || p.name) && (Array.isArray(p.icons) || p.start_url)) return true;
                } catch {}
            }
            return false;
        }

        async recognize(candidate, observation) {
            const discoveries = [];
            let parsed;
            try { parsed = JSON.parse(String(observation.body||'')); } catch { return discoveries; }
            const emit = (url, type, mech, conf) => {
                const canonical = canonicalizeUrl(url);
                if (!canonical || !isAllowedUrl(canonical)) return;
                // resolve relative to observation URL
                let resolved = canonical;
                try { resolved = new URL(canonical, observation.requestedUrl).href; resolved = canonicalizeUrl(resolved) || resolved; } catch {}
                discoveries.push(new Discovery({
                    candidateId: candidate.id,
                    observationId: observation.id,
                    kind: type,
                    confidence: conf,
                    mechanism: mech,
                    data: { url: resolved },
                    provenance: { origin: candidate.origin, parent: candidate.target, candidateTarget: candidate.target, candidateType: candidate.type, mechanism: mech, depth: candidate.depth }
                }));
            };
            if (Array.isArray(parsed.icons)) {
                for (const icon of parsed.icons) if (icon?.src) emit(icon.src, 'resource', 'manifest-icon', 0.85);
            }
            if (parsed.start_url) emit(String(parsed.start_url), 'url', 'manifest-start_url', 0.80);
            if (parsed.scope) emit(String(parsed.scope), 'url', 'manifest-scope', 0.75);
            if (Array.isArray(parsed.screenshots)) for (const s of parsed.screenshots) if (s?.src) emit(s.src, 'resource', 'manifest-screenshot', 0.80);
            if (Array.isArray(parsed.shortcuts)) for (const sc of parsed.shortcuts) if (sc?.url) emit(String(sc.url), 'url', 'manifest-shortcut', 0.78);
            return discoveries;
        }
    }

    class BinaryProvider extends Provider {
        constructor() {
            super('binary');
        }

        matches(observation) {
            return looksLikeBinary(
                observation.http?.contentType
            );
        }

        async recognize() {
            /*
             * Binary resources are observed but not parsed.
             *
             * Future providers may add PDF, ZIP, image metadata,
             * archive manifests, etc.
             */
            return [];
        }
    }

    /*
     * ============================================================
     * PROVIDER REGISTRY
     * ============================================================
     */

    class ProviderRegistry {
        constructor() {
            // Lazy registry: factories + ordered names, instances created on demand (v1.1)
            // Retains `new XProvider()` strings for static verification (ADR 021/023)
            this.factories = {
                html: () => new HtmlProvider(),
                json: () => new JsonProvider(),
                xml: () => new XmlProvider(),
                css: () => new CssProvider(),
                javascript: () => new JavaScriptProvider(),
                robots: () => new RobotsProvider(),
                headers: () => new HeadersProvider(),
                sitemapIndex: () => new SitemapIndexProvider(),
                openapi: () => new OpenApiProvider(),
                wellKnown: () => new WellKnownProvider(),
                manifest: () => new ManifestProvider(),
                binary: () => new BinaryProvider(),
                text: () => new TextProvider()
            };
            this.order = ['html','json','xml','css','javascript','robots','headers','sitemapIndex','openapi','wellKnown','manifest','binary','text'];
            this.instances = new Map();
            this.metrics = new Map();
            // Eager fallback when CONFIG.providers.lazy === false (v1.0 compatibility)
            if (CONFIG.providers && CONFIG.providers.lazy === false) {
                for (const name of this.order) {
                    if (CONFIG.providers.disabled?.includes(name)) continue;
                    const inst = this.factories[name]();
                    this.instances.set(name, inst);
                    this.metrics.set(name, { calls: 0, matches: 0, totalMs: 0 });
                }
            }
        }

        _get(name) {
            if (CONFIG.providers?.disabled?.includes(name)) return null;
            if (this.instances.has(name)) return this.instances.get(name);
            const factory = this.factories[name];
            if (!factory) return null;
            const inst = factory();
            this.instances.set(name, inst);
            if (!this.metrics.has(name)) this.metrics.set(name, { calls: 0, matches: 0, totalMs: 0 });
            return inst;
        }

        // Getter retains `this.providers` array semantics for legacy inspection/tests
        get providers() {
            return this.order
                .map(name => this._get(name))
                .filter(Boolean);
        }

        set providers(value) {
            this._providersOverride = value;
        }

        matching(observation) {
            if (this._providersOverride) {
                return this._providersOverride.filter(p => {
                    try { return p.matches(observation); } catch { return false; }
                });
            }
            const matched = [];
            for (const name of this.order) {
                const provider = this._get(name);
                if (!provider) continue;
                const metric = this.metrics.get(name);
                const start = (typeof performance !== 'undefined' && performance.now) ? performance.now() : Date.now();
                let isMatch = false;
                try { isMatch = provider.matches(observation); } catch { isMatch = false; }
                const dur = ((typeof performance !== 'undefined' && performance.now) ? performance.now() : Date.now()) - start;
                if (metric) { metric.calls++; if (isMatch) metric.matches++; metric.totalMs += dur; }
                if (isMatch) matched.push(provider);
            }
            return matched;
        }

        getMetrics() {
            const out = {};
            for (const [name, m] of this.metrics.entries()) {
                out[name] = { ...m, avgMs: m.calls ? m.totalMs / m.calls : 0 };
            }
            return out;
        }

        getInstanceCount() {
            return this.instances.size;
        }
    }

    /*
     * ============================================================
     * NETWORK OBSERVER
     * ============================================================
     *
     * Critical v0.7.1 rule:
     *
     * PerformanceObserver does NOT imply GET.
     *
     * fetch/XHR method is trusted only when the page bridge knows
     * the actual method.
     * ============================================================
     */

// --- 681-754 ---
    class AcquisitionPlan {
        constructor(data = {}) {
            this.id = data.id || makeId('plan');

            this.candidateId =
                data.candidateId || null;

            this.target =
                data.target || '';

            this.method =
                String(data.method || 'GET').toUpperCase();

            this.allowed =
                Boolean(data.allowed);

            this.reason =
                data.reason || null;

            this.priority =
                Number.isFinite(data.priority)
                    ? data.priority
                    : 0;

            this.origin =
                data.origin || originOf(this.target);

            this.expectedType =
                data.expectedType || 'unknown';

            this.requiresOriginSlot =
                data.requiresOriginSlot !== false;

            this.createdAt =
                data.createdAt || now();

            this.policyVersion =
                data.policyVersion || CONFIG.version;

            this.policyInputs =
                data.policyInputs || {};
        }

        serialize() {
            return {
                id: this.id,
                candidateId: this.candidateId,
                target: this.target,
                method: this.method,
                allowed: this.allowed,
                reason: this.reason,
                priority: this.priority,
                origin: this.origin,
                expectedType: this.expectedType,
                requiresOriginSlot: this.requiresOriginSlot,
                createdAt: this.createdAt,
                policyVersion: this.policyVersion,
                policyInputs: this.policyInputs
            };
        }
    }

    /*
     * ============================================================
     * DETERMINISTIC EVENT LEDGER
     * ============================================================
     *
     * The ledger records decisions and transitions.
     *
     * It does not claim that network execution is deterministic.
     * ============================================================
     */


// --- 2102-2244 ---
    class AcquisitionPolicy {
        plan(candidate) {
            const method =
                String(
                    candidate.hints?.method ||
                    'GET'
                ).toUpperCase();

            const base = {
                candidateId: candidate.id,
                target: candidate.target,
                method,
                priority:
                    candidate.effectivePriority(),
                origin: candidate.origin,
                expectedType: candidate.type,
                policyInputs: {
                    candidateType: candidate.type,
                    hints: {
                        ...candidate.hints
                    }
                }
            };

            if (!isAllowedUrl(candidate.target)) {
                return new AcquisitionPlan({
                    ...base,
                    allowed: false,
                    reason: 'url-not-allowed'
                });
            }

            if (method !== 'GET') {
                return new AcquisitionPlan({
                    ...base,
                    allowed: false,
                    reason: 'non-get-method'
                });
            }

            if (
                candidate.depth >
                CONFIG.maxDepth
            ) {
                return new AcquisitionPlan({
                    ...base,
                    allowed: false,
                    reason: 'max-depth'
                });
            }

            if (
                candidate.type === 'form' &&
                !CONFIG.policy.acquireForms
            ) {
                return new AcquisitionPlan({
                    ...base,
                    allowed: false,
                    reason: 'forms-disabled'
                });
            }

            if (
                candidate.type === 'media' &&
                !CONFIG.policy.acquireMedia
            ) {
                return new AcquisitionPlan({
                    ...base,
                    allowed: false,
                    reason: 'media-disabled'
                });
            }

            if (
                candidate.type === 'frame' &&
                !CONFIG.policy.acquireFrames
            ) {
                return new AcquisitionPlan({
                    ...base,
                    allowed: false,
                    reason: 'frames-disabled'
                });
            }

            if (
                candidate.type === 'stylesheet' &&
                !CONFIG.policy.acquireStylesheets
            ) {
                return new AcquisitionPlan({
                    ...base,
                    allowed: false,
                    reason: 'stylesheets-disabled'
                });
            }

            if (
                candidate.type === 'script' &&
                !CONFIG.policy.acquireScripts
            ) {
                return new AcquisitionPlan({
                    ...base,
                    allowed: false,
                    reason: 'scripts-disabled'
                });
            }

            if (
                candidate.type === 'network' &&
                !CONFIG.policy.acquireNetworkGet
            ) {
                return new AcquisitionPlan({
                    ...base,
                    allowed: false,
                    reason: 'network-get-disabled'
                });
            }

            if (
                candidate.hints?.binary &&
                !CONFIG.policy.acquireBinaryResources
            ) {
                return new AcquisitionPlan({
                    ...base,
                    allowed: false,
                    reason: 'binary-disabled'
                });
            }

            return new AcquisitionPlan({
                ...base,
                allowed: true,
                reason: null
            });
        }
    }

    /*
     * ============================================================
     * ORIGIN CONTROL
     * ============================================================
     */


// --- 2244-2337 ---
    class OriginController {
        constructor() {
            this.states = new Map();
        }

        state(origin) {
            if (!this.states.has(origin)) {
                this.states.set(origin, {
                    active: 0,
                    requests: 0,
                    lastRequestAt: 0
                });
            }

            return this.states.get(origin);
        }

        canReserve(origin) {
            const state =
                this.state(origin);

            if (
                state.requests >=
                CONFIG.origin.maxRequestsPerOrigin
            ) {
                return false;
            }

            if (
                state.active >=
                CONFIG.origin.maxConcurrentPerOrigin
            ) {
                return false;
            }

            return true;
        }

        async acquire(origin) {
            while (true) {
                const state =
                    this.state(origin);

                if (
                    state.requests >=
                    CONFIG.origin.maxRequestsPerOrigin
                ) {
                    return false;
                }

                if (
                    state.active <
                    CONFIG.origin.maxConcurrentPerOrigin
                ) {
                    const elapsed =
                        now() -
                        state.lastRequestAt;

                    const wait =
                        CONFIG.origin.minRequestInterval -
                        elapsed;

                    if (wait > 0) {
                        await sleep(wait);
                        continue;
                    }

                    state.active++;
                    state.requests++;
                    state.lastRequestAt = now();

                    return true;
                }

                await sleep(50);
            }
        }

        release(origin) {
            const state =
                this.state(origin);

            state.active =
                Math.max(0, state.active - 1);
        }
    }

    /*
     * ============================================================
     * ACQUISITION
     * ============================================================
     */


// --- 2337-2786 ---
    class Acquisition {
        constructor(originController) {
            this.origins =
                originController;
        }

        async execute(plan, ledger) {
            const startedAt = now();

            ledger.recordRequestStarted(plan);

            const originGranted =
                await this.origins.acquire(
                    plan.origin
                );

            if (!originGranted) {
                const observation =
                    new Observation({
                        candidateId:
                            plan.candidateId,
                        planId: plan.id,
                        target: plan.target,
                        requestedUrl:
                            plan.target,
                        startedAt,
                        completedAt: now(),
                        status: 'skipped',
                        reason:
                            'origin-request-budget'
                    });

                ledger.recordRequestCompleted(
                    plan,
                    observation
                );

                return observation;
            }

            try {
                return await this.request(
                    plan,
                    startedAt,
                    ledger
                );
            } finally {
                this.origins.release(
                    plan.origin
                );
            }
        }

        async request(plan, startedAt, ledger) {
            if (
                typeof GM_xmlhttpRequest ===
                'function'
            ) {
                return new Promise(resolve => {
                    let finished = false;

                    const finish =
                        observation => {
                            if (finished) return;

                            finished = true;

                            ledger.recordRequestCompleted(
                                plan,
                                observation
                            );

                            resolve(observation);
                        };

                    const timeoutId =
                        setTimeout(() => {
                            finish(
                                new Observation({
                                    candidateId:
                                        plan.candidateId,
                                    planId: plan.id,
                                    target:
                                        plan.target,
                                    requestedUrl:
                                        plan.target,
                                    startedAt,
                                    completedAt:
                                        now(),
                                    status: 'timeout',
                                    reason:
                                        'request-timeout'
                                })
                            );
                        }, CONFIG.requestTimeout);

                    try {
                        GM_xmlhttpRequest({
                            method: plan.method,
                            url: plan.target,
                            timeout:
                                CONFIG.requestTimeout,

                            onload: response => {
                                clearTimeout(timeoutId);

                                let body =
                                    String(
                                        response.responseText ||
                                        ''
                                    );

                                let bodyTruncated =
                                    false;

                                if (
                                    body.length >
                                    CONFIG.maxBodyChars
                                ) {
                                    body =
                                        body.slice(
                                            0,
                                            CONFIG.maxBodyChars
                                        );

                                    bodyTruncated = true;
                                }

                                const observation =
                                    new Observation({
                                        candidateId:
                                            plan.candidateId,

                                        planId:
                                            plan.id,

                                        target:
                                            plan.target,

                                        requestedUrl:
                                            plan.target,

                                        startedAt,

                                        completedAt:
                                            now(),

                                        status:
                                            response.status >=
                                                200 &&
                                            response.status <
                                                400
                                                ? 'success'
                                                : 'http-error',

                                        http: {
                                            status:
                                                response.status,

                                            contentType:
                                                response.responseHeaders
                                                    ?.match(
                                                        /content-type:\s*([^\r\n]+)/i
                                                    )?.[1]
                                                    ?.trim() ||
                                                '',

                                            contentLength:
                                                response.responseHeaders
                                                    ?.match(
                                                        /content-length:\s*(\d+)/i
                                                    )?.[1] ||
                                                null,

                                            headers: (() => {
                                                const h = {};
                                                for (const line of String(
                                                    response.responseHeaders || ''
                                                ).split(/\r?\n/)) {
                                                    const idx =
                                                        line.indexOf(':');
                                                    if (idx > 0) {
                                                        h[
                                                            line
                                                                .slice(
                                                                    0,
                                                                    idx
                                                                )
                                                                .trim()
                                                                .toLowerCase()
                                                        ] =
                                                            line
                                                                .slice(
                                                                    idx + 1
                                                                )
                                                                .trim();
                                                    }
                                                }
                                                return h;
                                            })(),

                                            finalUrl:
                                                response.finalUrl ||
                                                plan.target
                                        },

                                        body,
                                        bodyTruncated,

                                        fingerprint:
                                            makeFingerprint(
                                                body
                                            )
                                    });

                                finish(observation);
                            },

                            ontimeout: () => {
                                clearTimeout(timeoutId);

                                finish(
                                    new Observation({
                                        candidateId:
                                            plan.candidateId,
                                        planId: plan.id,
                                        target: plan.target,
                                        requestedUrl:
                                            plan.target,
                                        startedAt,
                                        completedAt:
                                            now(),
                                        status: 'timeout',
                                        reason:
                                            'request-timeout'
                                    })
                                );
                            },

                            onerror: error => {
                                clearTimeout(timeoutId);

                                finish(
                                    new Observation({
                                        candidateId:
                                            plan.candidateId,
                                        planId: plan.id,
                                        target: plan.target,
                                        requestedUrl:
                                            plan.target,
                                        startedAt,
                                        completedAt:
                                            now(),
                                        status: 'error',
                                        reason:
                                            'request-error',
                                        errors: [
                                            String(
                                                error?.error ||
                                                'unknown-error'
                                            )
                                        ]
                                    })
                                );
                            }
                        });
                    } catch (error) {
                        clearTimeout(timeoutId);

                        finish(
                            new Observation({
                                candidateId:
                                    plan.candidateId,
                                planId: plan.id,
                                target: plan.target,
                                requestedUrl:
                                    plan.target,
                                startedAt,
                                completedAt:
                                    now(),
                                status: 'error',
                                reason:
                                    'request-exception',
                                errors: [
                                    String(error)
                                ]
                            })
                        );
                    }
                });
            }

            /*
             * Fetch fallback.
             *
             * IMPORTANT:
             * AbortController is used so a timeout does not leave
             * an uncontrolled fetch alive.
             */

            const controller =
                new AbortController();

            const timeoutId =
                setTimeout(
                    () => controller.abort(),
                    CONFIG.requestTimeout
                );

            try {
                const response =
                    await fetch(
                        plan.target,
                        {
                            method: plan.method,
                            credentials: 'same-origin',
                            redirect: 'follow',
                            signal:
                                controller.signal
                        }
                    );

                let body =
                    await response.text();

                let bodyTruncated = false;

                if (
                    body.length >
                    CONFIG.maxBodyChars
                ) {
                    body =
                        body.slice(
                            0,
                            CONFIG.maxBodyChars
                        );

                    bodyTruncated = true;
                }

                const observation =
                    new Observation({
                        candidateId:
                            plan.candidateId,

                        planId:
                            plan.id,

                        target:
                            plan.target,

                        requestedUrl:
                            plan.target,

                        startedAt,

                        completedAt:
                            now(),

                        status:
                            response.ok
                                ? 'success'
                                : 'http-error',

                        http: {
                            status:
                                response.status,

                            contentType:
                                response.headers.get(
                                    'content-type'
                                ) || '',

                            contentLength:
                                response.headers.get(
                                    'content-length'
                                ),

                            headers: Object.fromEntries(
                                [...response.headers.entries()].map(
                                    ([k, v]) => [
                                        k.toLowerCase(),
                                        v
                                    ]
                                )
                            ),

                            finalUrl:
                                response.url ||
                                plan.target
                        },

                        body,
                        bodyTruncated,

                        fingerprint:
                            makeFingerprint(body)
                    });

                ledger.recordRequestCompleted(
                    plan,
                    observation
                );

                return observation;
            } catch (error) {
                const observation =
                    new Observation({
                        candidateId:
                            plan.candidateId,
                        planId: plan.id,
                        target: plan.target,
                        requestedUrl:
                            plan.target,
                        startedAt,
                        completedAt: now(),
                        status:
                            error?.name ===
                            'AbortError'
                                ? 'timeout'
                                : 'error',
                        reason:
                            error?.name ===
                            'AbortError'
                                ? 'request-timeout'
                                : 'request-error',
                        errors: [
                            String(error)
                        ]
                    });

                ledger.recordRequestCompleted(
                    plan,
                    observation
                );

                return observation;
            } finally {
                clearTimeout(timeoutId);
            }
        }
    }

    /*
     * ============================================================
     * PROVIDER BASE
     * ============================================================
     */


// --- 3770-4266 ---
    class NetworkObserver {
        constructor(engine) {
            this.engine = engine;
            this.started = false;
            this.performanceObserver = null;
        }

        start() {
            if (this.started) return;

            this.started = true;

            if (CONFIG.networkBridge) {
                this.installBridge();
            }

            if (
                CONFIG.discovery.performance &&
                typeof PerformanceObserver !==
                    'undefined'
            ) {
                this.installPerformanceObserver();
            }
        }

        installBridge() {
            try {
                const script =
                    document.createElement(
                        'script'
                    );

                const __gdeBridgeSource = `(function () {
    if (window.__GDE_NETWORK_BRIDGE__) return;
    window.__GDE_NETWORK_BRIDGE__ = true;

    function emit(event) {
        window.postMessage({
            source: 'generic-discovery-engine',
            type: 'network',
            event: event
        }, '*');
    }

    const originalFetch = window.fetch;

    if (originalFetch) {
        window.fetch = async function (
            input,
            init
        ) {
            const requestAt =
                Date.now();

            const url =
                typeof input === 'string'
                    ? input
                    : input?.url;

            const method =
                String(
                    init?.method ||
                    input?.method ||
                    'GET'
                ).toUpperCase();

            const requestId =
                'fetch-' +
                requestAt +
                '-' +
                Math.random()
                    .toString(36)
                    .slice(2);

            emit({
                phase: 'request',
                api: 'fetch',
                requestId,
                method,
                url,
                requestAt
            });

            try {
                const response =
                    await originalFetch.apply(
                        this,
                        arguments
                    );

                emit({
                    phase: 'response',
                    api: 'fetch',
                    requestId,
                    method,
                    url,
                    finalUrl:
                        response.url,
                    status:
                        response.status,
                    contentType:
                        response.headers.get(
                            'content-type'
                        ) || '',
                    responseAt:
                        Date.now()
                });

                return response;
            } catch (error) {
                emit({
                    phase: 'error',
                    api: 'fetch',
                    requestId,
                    method,
                    url,
                    error:
                        String(error),
                    responseAt:
                        Date.now()
                });

                throw error;
            }
        };
    }

    const OriginalXHR =
        window.XMLHttpRequest;

    if (OriginalXHR) {
        const open =
            OriginalXHR.prototype.open;

        const send =
            OriginalXHR.prototype.send;

        OriginalXHR.prototype.open =
            function (
                method,
                url
            ) {
                this.__gde = {
                    method:
                        String(
                            method || 'GET'
                        ).toUpperCase(),
                    url,
                    requestId:
                        'xhr-' +
                        Date.now() +
                        '-' +
                        Math.random()
                            .toString(36)
                            .slice(2)
                };

                return open.apply(
                    this,
                    arguments
                );
            };

        OriginalXHR.prototype.send =
            function () {
                const meta =
                    this.__gde;

                if (meta) {
                    emit({
                        phase: 'request',
                        api: 'xhr',
                        requestId:
                            meta.requestId,
                        method:
                            meta.method,
                        url:
                            meta.url,
                        requestAt:
                            Date.now()
                    });

                    this.addEventListener(
                        'load',
                        function () {
                            emit({
                                phase:
                                    'response',
                                api: 'xhr',
                                requestId:
                                    meta.requestId,
                                method:
                                    meta.method,
                                url:
                                    meta.url,
                                finalUrl:
                                    this.responseURL ||
                                    meta.url,
                                status:
                                    this.status,
                                contentType:
                                    this.getResponseHeader(
                                        'content-type'
                                    ) || '',
                                responseAt:
                                    Date.now()
                            });
                        }
                    );

                    this.addEventListener(
                        'error',
                        function () {
                            emit({
                                phase:
                                    'error',
                                api: 'xhr',
                                requestId:
                                    meta.requestId,
                                method:
                                    meta.method,
                                url:
                                    meta.url,
                                error:
                                    'xhr-error',
                                responseAt:
                                    Date.now()
                            });
                        }
                    );
                }

                return send.apply(
                    this,
                    arguments
                );
            };
    }
})();
`;
                // Trusted Types compliance (gde-bridge policy) — S-02 residual
                try {
                    if (window.trustedTypes?.createPolicy) {
                        const __gdePolicy = window.trustedTypes.createPolicy('gde-bridge', {
                            createScript: s => s
                        });
                        // @ts-ignore TrustedScript
                        script.textContent = __gdePolicy.createScript(__gdeBridgeSource);
                    } else {
                        script.textContent = __gdeBridgeSource;
                    }
                } catch {
                    script.textContent = __gdeBridgeSource;
                }

                (
                    document.documentElement ||
                    document.head ||
                    document.body
                )?.appendChild(script);

                script.remove();

                window.addEventListener(
                    'message',
                    event => {
                        if (
                            event.source !== window
                        ) {
                            return;
                        }

                        if (
                            event.data?.source !==
                            'generic-discovery-engine'
                        ) {
                            return;
                        }

                        if (
                            event.data?.type !==
                            'network'
                        ) {
                            return;
                        }

                        this.handleBridgeEvent(
                            event.data.event
                        );
                    }
                );
            } catch (error) {
                const msg = String(error);
                this.engine.ledger
                    .recordDiagnostic(
                        'network-bridge-error',
                        {
                            error: msg
                        }
                    );
                if (
                    /Content[- ]Security[- ]Policy|CSP|Refused to execute/i.test(
                        msg
                    )
                ) {
                    this.engine.ledger.recordDiagnostic(
                        'csp-blocks-bridge',
                        {
                            error: msg,
                            hint: 'page CSP blocks inline script; network bridge disabled, PerformanceObserver remains'
                        }
                    );
                }
            }
        }

        handleBridgeEvent(event) {
            if (!event) return;

            const key =
                event.requestId;

            if (!key) return;

            this.engine.networkEvents.set(
                key,
                {
                    id:
                        key,
                    requestId:
                        key,
                    api:
                        event.api,
                    method:
                        event.method,
                    url:
                        event.url,
                    finalUrl:
                        event.finalUrl ||
                        null,
                    status:
                        event.status ||
                        0,
                    contentType:
                        event.contentType ||
                        '',
                    requestAt:
                        event.requestAt ||
                        now(),
                    responseAt:
                        event.responseAt ||
                        null,
                    phase:
                        event.phase,
                    error:
                        event.error ||
                        null
                }
            );

            const networkEvent =
                this.engine.networkEvents.get(
                    key
                );

            if (
                networkEvent.phase ===
                    'response' &&
                networkEvent.method ===
                    'GET' &&
                networkEvent.url
            ) {
                this.engine.observeNetworkGet(
                    networkEvent
                );
            }
        }

        installPerformanceObserver() {
            try {
                this.performanceObserver =
                    new PerformanceObserver(
                        entries => {
                            for (
                                const entry of
                                entries.getEntries()
                            ) {
                                if (
                                    !entry.name
                                ) {
                                    continue;
                                }

                                const initiator =
                                    entry.initiatorType ||
                                    'unknown';

                                /*
                                 * We intentionally do NOT assume
                                 * fetch/xhr == GET here.
                                 *
                                 * They are evidence only unless
                                 * the bridge provides method data.
                                 */
                                const executableGetLike =
                                    ![
                                        'fetch',
                                        'xmlhttprequest'
                                    ].includes(
                                        initiator
                                    );

                                const event = {
                                    id:
                                        makeId(
                                            'perf'
                                        ),

                                    requestId:
                                        makeId(
                                            'perf-request'
                                        ),

                                    api:
                                        'performance',

                                    method:
                                        executableGetLike
                                            ? 'GET'
                                            : null,

                                    url:
                                        entry.name,

                                    finalUrl:
                                        entry.name,

                                    status:
                                        0,

                                    contentType:
                                        '',

                                    initiatorType:
                                        initiator,

                                    requestAt:
                                        now(),

                                    responseAt:
                                        now(),

                                    duration:
                                        entry.duration,

                                    phase:
                                        'performance'
                                };

                                this.engine.recordNetworkEvent(
                                    event
                                );

                                if (
                                    executableGetLike
                                ) {
                                    this.engine.observeNetworkGet(
                                        event
                                    );
                                }
                            }
                        }
                    );

                this.performanceObserver.observe({
                    entryTypes: ['resource']
                });
            } catch (error) {
                this.engine.ledger
                    .recordDiagnostic(
                        'performance-observer-error',
                        {
                            error:
                                String(error)
                        }
                    );
            }
        }
    }

    /*
     * ============================================================
     * ENGINE
     * ============================================================
     */


// --- 4266-5864 ---
    class GenericDiscoveryEngine {
        constructor() {
            this.db =
                new KnowledgeBase();

            this.policy =
                new AcquisitionPolicy();

            this.origins =
                new OriginController();

            this.acquisition =
                new Acquisition(
                    this.origins
                );

            this.providers =
                new ProviderRegistry();

            this.ledger =
                new DecisionLedger();

            this.networkObserver =
                new NetworkObserver(
                    this
                );

            this.networkEvents =
                new Map();

            this.running = false;
            this.paused = false;
            this.stopRequested = false;

            this.activeWorkers = 0;
            this.requestsReserved = 0;

            this.currentConcurrency =
                CONFIG.concurrency;

            this.consecutiveFailures = 0;
            this.consecutiveSuccesses = 0;

            this.persistenceTimer = null;

            this.ui = null;
            this._uiRaf = null;
        }

        async init() {
            this.restore();

            this.ledger.recordDiagnostic(
                'engine-init',
                {
                    version:
                        CONFIG.version
                }
            );

            if (!CONFIG.sameOriginOnly) {
                this.ledger.recordDiagnostic(
                    'config-cross-origin-requires-connect-star',
                    {
                        sameOriginOnly: false,
                        hint: 'set @connect * for cross-origin fetch'
                    }
                );
                warn(
                    'sameOriginOnly=false — ensure @connect * is enabled'
                );
            }

            this.installUI();

            if (
                document.readyState ===
                'loading'
            ) {
                document.addEventListener(
                    'DOMContentLoaded',
                    () => this.bootstrap(),
                    {
                        once: true
                    }
                );
            } else {
                this.bootstrap();
            }
        }

        bootstrap() {
            this.observeCurrentPage();

            this.networkObserver.start();

            if (
                CONFIG.observeDomMutations
            ) {
                this.installMutationObserver();
            }

            this.start();
        }

        /*
         * --------------------------------------------------------
         * DISCOVERY
         * --------------------------------------------------------
         */

        discover(
            target,
            type = 'url',
            options = {}
        ) {
            const canonical =
                canonicalizeUrl(target);

            if (!canonical) {
                return null;
            }

            if (!isAllowedUrl(canonical)) {
                return null;
            }

            const candidate =
                new Candidate({
                    target:
                        canonical,

                    type,

                    origin:
                        originOf(canonical),

                    parent:
                        options.parent ||
                        null,

                    priority:
                        Number.isFinite(
                            options.priority
                        )
                            ? options.priority
                            : 0,

                    hints:
                        options.hints || {},

                    depth:
                        Number.isFinite(
                            options.depth
                        )
                            ? options.depth
                            : 0
                });

            const stored =
                this.db.addCandidate(
                    candidate,
                    options.discovery ||
                        null
                );

            if (!stored) {
                return null;
            }

            this.db.queueCandidate(
                stored
            );

            this.ledger
                .recordCandidateDiscovered(
                    stored,
                    options.discovery ||
                        null
                );

            this.ledger
                .recordCandidateEnqueued(
                    stored
                );

            this.db.ensureResource(
                stored.target
            ).merge({
                type: stored.type,
                mechanism:
                    options.mechanism ||
                    'discovery',
                candidateIds: [
                    stored.id
                ]
            });

            this.schedulePersistence();

            return stored;
        }

        emitDiscovery(discovery) {
            this.db.addDiscovery(
                discovery
            );

            this.ledger.recordDiscovery(
                discovery
            );

            const target =
                discovery.targetUrl();

            if (!target) {
                return null;
            }

            const depth =
                Number.isFinite(
                    discovery.provenance?.depth
                )
                    ? discovery.provenance.depth +
                      1
                    : 1;

            const type =
                discovery.kind === 'api'
                    ? 'api'
                    : discovery.kind;

            const candidate =
                this.discover(
                    target,
                    type,
                    {
                        parent:
                            discovery.candidateId,

                        priority:
                            discovery.confidence,

                        depth,

                        hints:
                            discovery.provenance
                                ?.hints ||
                            {
                                confidence:
                                    discovery.confidence
                            },

                        discovery,

                        mechanism:
                            discovery.mechanism
                    }
                );

            return candidate;
        }

        /*
         * --------------------------------------------------------
         * ACQUISITION PLAN
         * --------------------------------------------------------
         */

        plan(candidate) {
            this.db.markPlanned(
                candidate
            );

            const plan =
                this.policy.plan(
                    candidate
                );

            this.ledger.recordPlan(
                plan
            );

            if (!plan.allowed) {
                this.ledger
                    .recordPolicyDenied(
                        plan
                    );

                this.ledger
                    .recordDiagnostic(
                        'policy-denied',
                        plan.serialize()
                    );
            }

            return plan;
        }

        /*
         * --------------------------------------------------------
         * REQUEST BUDGET
         * --------------------------------------------------------
         *
         * Synchronous reservation prevents several workers from
         * collectively exceeding maxRequests.
         * --------------------------------------------------------
         */

        reserveRequestSlot() {
            if (
                this.requestsReserved >=
                CONFIG.maxRequests
            ) {
                return false;
            }

            this.requestsReserved++;

            return true;
        }

        /*
         * --------------------------------------------------------
         * EXECUTION
         * --------------------------------------------------------
         */

        async executePlan(plan) {
            const candidate =
                this.db.candidates.get(
                    plan.candidateId
                );

            if (!candidate) {
                return;
            }

            if (
                !plan.allowed
            ) {
                this.db.markSkipped(
                    candidate,
                    plan.reason
                );

                this.ledger
                    .recordCandidateSkipped(
                        candidate,
                        plan.reason
                    );

                return;
            }

            if (
                !this.db.shouldAcquireResource(
                    plan.target
                )
            ) {
                this.ledger
                    .recordDiagnostic(
                        'resource-already-acquired',
                        {
                            candidateId:
                                candidate.id,
                            target:
                                plan.target
                        }
                    );

                this.db.markCompleted(
                    candidate
                );

                this.ledger
                    .recordCandidateCompleted(
                        candidate
                    );

                return;
            }

            if (
                !this.reserveRequestSlot()
            ) {
                this.ledger
                    .recordBudgetDenied(
                        candidate,
                        'global-request-budget'
                    );

                this.db.markSkipped(
                    candidate,
                    'global-request-budget'
                );

                this.ledger
                    .recordCandidateSkipped(
                        candidate,
                        'global-request-budget'
                    );

                return;
            }

            this.ledger.recordSlotGranted(
                plan
            );

            this.db.markAcquiring(
                candidate
            );

            const observation =
                await this.acquisition.execute(
                    plan,
                    this.ledger
                );

            this.db.recordObservation(
                observation
            );

            this.ledger
                .recordObservation(
                    observation
                );

            this.db.markObserved(
                candidate
            );

            // v0.9.1: revisitChanged — re-queue changed resource (opt-in, clears visited)
            if (CONFIG.revisitChanged) {
                try {
                    const revisitUrl = canonicalizeUrl(observation.requestedUrl) || observation.requestedUrl;
                    const res = this.db.resources.get(revisitUrl);
                    if (res && res.status === 'changed') {
                        const revisitKey = `url:${revisitUrl}`;
                        this.db.visited.delete(revisitKey);
                        this.db.candidateKeys.delete(revisitKey);
                        const revisit = this.discover(observation.requestedUrl, 'url', {
                            priority: 0.6,
                            depth: candidate.depth,
                            hints: { confidence: 0.7, revisit: true },
                            mechanism: 'revisit-changed'
                        });
                        if (revisit) {
                            this.ledger.recordDiagnostic('revisit-queued', { target: observation.requestedUrl, candidateId: revisit.id });
                        }
                    }
                } catch {}
            }

            if (
                observation.status !==
                'success'
            ) {
                const retried =
                    this.db.retryCandidate(
                        candidate,
                        observation.reason ||
                            observation.status
                    );

                if (retried) {
                    this.ledger.recordRetry(
                        candidate,
                        observation.reason ||
                            observation.status
                    );
                }

                this.onFailure();

                return;
            }

            this.onSuccess();

            const providers =
                this.providers.matching(
                    observation
                );

            if (!providers.length) {
                this.db.markCompleted(
                    candidate
                );

                this.ledger
                    .recordCandidateCompleted(
                        candidate
                    );

                return;
            }

            this.db.markRecognized(
                candidate
            );

            // P1-1: per-observation cross-provider dedup
            const emittedForObservation =
                new Set();

            for (const provider of providers) {
                this.ledger.recordRecognition(
                    candidate,
                    observation,
                    provider.name
                );

                let discoveries = [];

                try {
                    discoveries =
                        await provider.recognize(
                            candidate,
                            observation
                        );
                } catch (error) {
                    this.ledger
                        .recordDiagnostic(
                            'provider-error',
                            {
                                provider:
                                    provider.name,
                                candidateId:
                                    candidate.id,
                                error:
                                    String(error)
                            }
                        );

                    continue;
                }

                for (
                    const discovery of
                    discoveries
                ) {
                    const dedupKey =
                        discovery.targetUrl();

                    if (
                        dedupKey &&
                        emittedForObservation.has(
                            dedupKey
                        )
                    ) {
                        this.ledger.recordDiagnostic(
                            'discovery-deduped',
                            {
                                url: dedupKey,
                                provider: provider.name
                            }
                        );
                        continue;
                    }

                    if (dedupKey)
                        emittedForObservation.add(
                            dedupKey
                        );

                    this.emitDiscovery(
                        discovery
                    );
                }
            }

            this.db.markExpanded(
                candidate
            );

            this.db.markCompleted(
                candidate
            );

            this.ledger
                .recordCandidateCompleted(
                    candidate
                );

            // v0.9.1: pattern-guided exploration (opt-in, bounded)
            if (CONFIG.patternGuided?.enabled) {
                try {
                    const suggestions = this.db.suggestPatternCandidates();
                    for (const { suggestion, pattern, count } of suggestions) {
                        const pc = this.discover(suggestion, 'url', {
                            priority: 0.55,
                            depth: candidate.depth + 1,
                            hints: { confidence: 0.6, patternGuided: true, pattern },
                            mechanism: 'pattern-guided'
                        });
                        if (pc) {
                            this.ledger.recordDiagnostic('pattern-guided-queued', { pattern, suggestion, count, candidateId: pc.id });
                        }
                    }
                } catch {}
            }

            this.schedulePersistence();
        }

        /*
         * --------------------------------------------------------
         * WORKER LOOP
         * --------------------------------------------------------
         */

        async worker() {
            this.activeWorkers++;

            try {
                while (
                    this.running &&
                    !this.stopRequested
                ) {
                    if (this.paused) {
                        await sleep(100);
                        continue;
                    }

                    if (
                        this.requestsReserved >=
                        CONFIG.maxRequests
                    ) {
                        break;
                    }

                    const candidate =
                        this.db.claimNextCandidate();

                    if (!candidate) {
                        break;
                    }

                    this.ledger
                        .recordCandidateClaimed(
                            candidate
                        );

                    const plan =
                        this.plan(candidate);

                    if (!plan.allowed) {
                        this.db.markSkipped(
                            candidate,
                            plan.reason
                        );

                        this.ledger
                            .recordCandidateSkipped(
                                candidate,
                                plan.reason
                            );

                        continue;
                    }

                    await this.executePlan(
                        plan
                    );
                }
            } finally {
                this.activeWorkers--;

                if (
                    this.activeWorkers === 0 &&
                    this.running
                ) {
                    this.updateUI();
                }
            }
        }

        async start() {
            if (this.running) {
                return;
            }

            this.running = true;
            this.paused = false;
            this.stopRequested = false;

            this.ledger.recordDiagnostic(
                'scan-started'
            );

            const workers = [];

            for (
                let i = 0;
                i < this.currentConcurrency;
                i++
            ) {
                workers.push(
                    this.worker()
                );
            }

            await Promise.all(
                workers
            );

            if (
                this.stopRequested ||
                this.requestsReserved >=
                    CONFIG.maxRequests
            ) {
                this.running = false;
            }

            this.ledger.recordDiagnostic(
                'scan-finished',
                {
                    requests:
                        this.requestsReserved,
                    candidates:
                        this.db.candidates.size
                }
            );

            this.persist();
            this.updateUI();
        }

        pause() {
            this.paused = true;

            this.ledger.recordDiagnostic(
                'scan-paused'
            );

            this.updateUI();
        }

        resume() {
            this.paused = false;

            this.ledger.recordDiagnostic(
                'scan-resumed'
            );

            this.updateUI();

            if (
                !this.running
            ) {
                this.start();
            }
        }

        stop() {
            this.stopRequested = true;
            this.running = false;

            this.ledger.recordDiagnostic(
                'scan-stop-requested'
            );

            this.persist();
            this.updateUI();
        }

        /*
         * --------------------------------------------------------
         * ADAPTIVE CONTROL
         * --------------------------------------------------------
         */

        onSuccess() {
            this.consecutiveSuccesses++;
            this.consecutiveFailures = 0;

            if (
                !CONFIG.adaptive.enabled
            ) {
                return;
            }

            if (
                this.consecutiveSuccesses >=
                CONFIG.adaptive.successThreshold
            ) {
                const old =
                    this.currentConcurrency;

                this.currentConcurrency =
                    clamp(
                        this.currentConcurrency + 1,
                        CONFIG.adaptive
                            .minConcurrency,
                        CONFIG.concurrency
                    );

                this.consecutiveSuccesses = 0;

                if (
                    old !==
                    this.currentConcurrency
                ) {
                    this.ledger
                        .recordDiagnostic(
                            'adaptive-increase',
                            {
                                from: old,
                                to:
                                    this.currentConcurrency
                            }
                        );
                }
            }
        }

        onFailure() {
            this.consecutiveFailures++;
            this.consecutiveSuccesses = 0;

            if (
                !CONFIG.adaptive.enabled
            ) {
                return;
            }

            if (
                this.consecutiveFailures >=
                CONFIG.adaptive.failureThreshold
            ) {
                const old =
                    this.currentConcurrency;

                this.currentConcurrency =
                    clamp(
                        this.currentConcurrency - 1,
                        CONFIG.adaptive
                            .minConcurrency,
                        CONFIG.concurrency
                    );

                this.consecutiveFailures = 0;

                if (
                    old !==
                    this.currentConcurrency
                ) {
                    this.ledger
                        .recordDiagnostic(
                            'adaptive-decrease',
                            {
                                from: old,
                                to:
                                    this.currentConcurrency
                            }
                        );
                }
            }
        }

        /*
         * --------------------------------------------------------
         * NETWORK EVIDENCE
         * --------------------------------------------------------
         */

        recordNetworkEvent(event) {
            if (
                this.networkEvents.size >=
                CONFIG.maxNetworkEvents
            ) {
                return;
            }

            this.networkEvents.set(
                event.id,
                event
            );

            this.ledger
                .recordDiagnostic(
                    'network-observed',
                    {
                        eventId:
                            event.id,
                        api:
                            event.api,
                        method:
                            event.method,
                        url:
                            event.url,
                        initiatorType:
                            event.initiatorType ||
                            null
                    }
                );

            const resource =
                this.db.ensureResource(
                    event.url
                );

            if (resource) {
                resource.merge({
                    networkEventIds: [
                        event.id
                    ],
                    mechanism:
                        `network:${event.api}`
                });
            }
        }

        observeNetworkGet(event) {
            if (
                !CONFIG.discovery.network
            ) {
                return;
            }

            if (
                event.method !== 'GET'
            ) {
                return;
            }

            if (!event.url) {
                return;
            }

            const url =
                canonicalizeUrl(
                    event.finalUrl ||
                    event.url
                );

            if (!url) return;

            this.recordNetworkEvent(
                event
            );

            this.discover(
                url,
                looksLikeApiUrl(url)
                    ? 'api'
                    : 'network',
                {
                    priority: 0.65,
                    depth: 0,
                    hints: {
                        confidence: 0.70,
                        method: 'GET',
                        networkObserved: true
                    },
                    mechanism:
                        'network-get'
                }
            );
        }

        /*
         * --------------------------------------------------------
         * CURRENT PAGE
         * --------------------------------------------------------
         */

        observeCurrentPage() {
            this.discover(
                location.href,
                'url',
                {
                    priority: 1,
                    depth: 0,
                    hints: {
                        confidence: 1,
                        method: 'GET',
                        root: true
                    },
                    mechanism:
                        'current-page'
                }
            );
        }

        /*
         * --------------------------------------------------------
         * DOM MUTATION OBSERVER
         * --------------------------------------------------------
         */

        installMutationObserver() {
            if (
                typeof MutationObserver ===
                'undefined'
            ) {
                return;
            }

            let timer = null;

            const observer =
                new MutationObserver(
                    () => {
                        clearTimeout(timer);

                        timer =
                            setTimeout(
                                () =>
                                    this.observeCurrentDom(),
                                CONFIG.mutationDebounce
                            );
                    }
                );

            observer.observe(
                document.documentElement ||
                    document,
                {
                    subtree: true,
                    childList: true,
                    attributes: true,
                    attributeFilter: [
                        'href',
                        'src',
                        'action'
                    ]
                }
            );
        }

        observeCurrentDom() {
            // P1-2: batch dedup within single mutation flush
            const seen = new Set();

            const tryDiscover = (
                target,
                type,
                priority,
                mechanism
            ) => {
                try {
                    const key = `${type}:${canonicalizeUrl(
                        target
                    )}`;
                    if (!key || seen.has(key)) return;
                    seen.add(key);
                } catch {
                    return;
                }

                this.discover(target, type, {
                    priority,
                    depth: 1,
                    hints: { method: 'GET' },
                    mechanism
                });
            };

            for (
                const element of
                document.querySelectorAll(
                    'a[href], area[href]'
                )
            ) {
                tryDiscover(
                    element.href,
                    'url',
                    0.50,
                    'dom-observer-link'
                );
            }

            for (
                const element of
                document.querySelectorAll(
                    'script[src]'
                )
            ) {
                tryDiscover(
                    element.src,
                    'script',
                    0.45,
                    'dom-observer-script'
                );
            }

            for (
                const element of
                document.querySelectorAll(
                    'link[href]'
                )
            ) {
                tryDiscover(
                    element.href,
                    'resource',
                    0.40,
                    'dom-observer-link'
                );
            }
        }

        /*
         * --------------------------------------------------------
         * PERSISTENCE
         * --------------------------------------------------------
         */

        schedulePersistence() {
            if (!CONFIG.persistence) {
                return;
            }

            clearTimeout(
                this.persistenceTimer
            );

            this.persistenceTimer =
                setTimeout(
                    () => this.persist(),
                    CONFIG.persistenceDebounce
                );
        }

        persist() {
            if (!CONFIG.persistence) {
                return;
            }

            try {
                GM_setValue(
                    STORAGE_KEY,
                    JSON.stringify({
                        engine:
                            this.db.serialize(),

                        ledger:
                            this.ledger.export(),

                        requestsReserved:
                            this.requestsReserved,

                        currentConcurrency:
                            this.currentConcurrency
                    })
                );
            } catch (error) {
                this.db.recordDiagnostic(
                    'persistence-error',
                    {
                        error:
                            String(error)
                    }
                );
            }
        }

        restore() {
            if (!CONFIG.persistence) {
                return;
            }

            try {
                const raw =
                    GM_getValue(
                        STORAGE_KEY,
                        null
                    );

                if (!raw) {
                    return;
                }

                const data =
                    typeof raw === 'string'
                        ? JSON.parse(raw)
                        : raw;

                /*
                 * v6 -> v7 migration is intentionally additive.
                 *
                 * Candidate records are retained.
                 * Existing persistence does not contain a ledger,
                 * so a new ledger begins here.
                 */

                if (
                    data.engine?.version >= 6
                ) {
                    this.db.restore(
                        data.engine
                    );
                }

                if (data.ledger) {
                    this.ledger.restore(
                        data.ledger
                    );
                }

                /*
                 * Do not restore the old request counter blindly.
                 *
                 * A new browser execution gets a fresh execution
                 * budget.
                 */

                this.requestsReserved = 0;

                this.currentConcurrency =
                    clamp(
                        Number(
                            data.currentConcurrency ||
                            CONFIG.concurrency
                        ),
                        CONFIG.adaptive
                            .minConcurrency,
                        CONFIG.concurrency
                    );
            } catch (error) {
                warn(
                    'Restore failed',
                    error
                );
            }
        }

        /*
         * --------------------------------------------------------
         * EXPORT
         * --------------------------------------------------------
         */

        // P2-3: coverage/budget frontier metrics (added v0.7.3)
        getCoverageMetrics() {
            const all = [
                ...this.db.candidates.values()
            ];
            const queued =
                all.filter(
                    c =>
                        c.status ===
                        'queued'
                );
            const queuedByTypeUnsorted = {};
            for (const c of queued) {
                queuedByTypeUnsorted[c.type] =
                    (queuedByTypeUnsorted[c.type] ||
                        0) + 1;
            }
            // deterministic: sorted keys
            const queuedByType = {};
            for (const k of Object.keys(queuedByTypeUnsorted).sort()) {
                queuedByType[k] = queuedByTypeUnsorted[k];
            }
            const live = all.filter(
                c =>
                    ![
                        'completed',
                        'skipped'
                    ].includes(
                        c.status
                    )
            ).length;
            // inference metrics (O(n≤750) via KnowledgeBase, ~0.06ms)
            const patternMetrics = this.db.getPatternMetrics
                ? this.db.getPatternMetrics()
                : { size: 0, total: 0, top: [] };
            const clusterMetrics = this.db.getClusterMetrics
                ? this.db.getClusterMetrics()
                : { size: 0, total: 0, top: [] };
            const providerMetrics = this.getProviderMetrics();
            const providerInstances = this.providers?.getInstanceCount?.() ?? this.providers?.providers?.length ?? 0;
            return {
                frontierSize:
                    queued.length,
                queuedByType,
                liveCount: live,
                visitedSize:
                    this.db.visited.size,
                knownResources:
                    this.db.resources.size,
                totalCandidates:
                    all.length,
                requestsUsed:
                    this.requestsReserved,
                requestsRemaining:
                    Math.max(
                        0,
                        CONFIG.maxRequests -
                            this.requestsReserved
                    ),
                ledgerSize:
                    this.ledger.events.length,
                graphEdges:
                    this.db.graphEdges.length,
                observations:
                    this.db.observations.size,
                patternCount:
                    patternMetrics.size,
                clusterCount:
                    clusterMetrics.size,
                fingerprintUnique:
                    this.db.fingerprintIndex
                        ? this.db.fingerprintIndex.size
                        : 0,
                inferenceEnabled:
                    Boolean(
                        CONFIG.inference &&
                        CONFIG.inference
                            .patternInference
                    ),
                providerInstances,
                providerMetrics
            };
        }

        getProviderMetrics() {
            try {
                if (this.providers?.getMetrics) return this.providers.getMetrics();
                // fallback: synthesize from provider names
                const out = {};
                for (const p of (this.providers?.providers || [])) {
                    out[p.name] = { calls: 0, matches: 0, totalMs: 0, avgMs: 0 };
                }
                return out;
            } catch { return {}; }
        }

        exportData() {
            const coverage =
                this.getCoverageMetrics();
            // inference snapshot (bounded, top 20 already sorted)
            const inference = {
                enabled: Boolean(
                    CONFIG.inference &&
                    CONFIG.inference.patternInference
                ),
                patternMetrics:
                    this.db.getPatternMetrics
                        ? this.db.getPatternMetrics()
                        : {
                            size: 0,
                            total: 0,
                            top: []
                          },
                clusterMetrics:
                    this.db.getClusterMetrics
                        ? this.db.getClusterMetrics()
                        : {
                            size: 0,
                            total: 0,
                            top: []
                          },
                fingerprintStats: {
                    unique:
                        this.db.fingerprintIndex
                            ? this.db.fingerprintIndex.size
                            : 0,
                    total:
                        this.db.fingerprintIndex
                            ? [
                                ...this.db.fingerprintIndex.values()
                              ].reduce(
                                    (a, s) =>
                                        a + s.size,
                                    0
                                )
                            : 0
                }
            };
            const providers = {
                lazy: Boolean(CONFIG.providers?.lazy),
                disabled: [...(CONFIG.providers?.disabled || [])],
                metrics: this.getProviderMetrics(),
                instanceCount: this.providers?.getInstanceCount?.() ?? 0
            };
            return {
                schema: 'gde-export-v8.0',

                exportedAt:
                    new Date().toISOString(),

                config: {
                    ...CONFIG
                },

                coverage,

                inference,

                providers,

                engine:
                    this.db.serialize(),

                ledger:
                    this.ledger.export(),

                networkEvents:
                    [
                        ...this.networkEvents.values()
                    ],

                diagnostics:
                    this.db.diagnostics.slice()
            };
        }

        /*
         * --------------------------------------------------------
         * UI
         * --------------------------------------------------------
         */

        installUI() {
            if (this.ui) {
                return;
            }

            const panel =
                document.createElement(
                    'div'
                );

            panel.style.cssText = `
                position:fixed;
                right:12px;
                bottom:12px;
                z-index:2147483647;
                background:#111;
                color:#eee;
                border:1px solid #555;
                border-radius:6px;
                padding:10px;
                font:12px/1.4 monospace;
                min-width:230px;
                box-shadow:0 4px 20px rgba(0,0,0,.35);
            `;

            const stats =
                document.createElement(
                    'div'
                );

            stats.style.marginBottom =
                '8px';

            const buttons =
                document.createElement(
                    'div'
                );

            buttons.style.display =
                'flex';

            buttons.style.gap =
                '4px';

            const button =
                (label, handler) => {
                    const el =
                        document.createElement(
                            'button'
                        );

                    el.textContent =
                        label;

                    el.style.cssText = `
                        font:11px monospace;
                        padding:4px 7px;
                        cursor:pointer;
                    `;

                    el.addEventListener(
                        'click',
                        handler
                    );

                    buttons.appendChild(
                        el
                    );

                    return el;
                };

            button(
                'Scan',
                () => this.start()
            );

            button(
                'Pause',
                () => {
                    if (this.paused) {
                        this.resume();
                    } else {
                        this.pause();
                    }
                }
            );

            button(
                'Stop',
                () => this.stop()
            );

            button(
                'Clear',
                () => {
                    if (
                        confirm(
                            'Clear persisted discovery state?'
                        )
                    ) {
                        GM_setValue(
                            STORAGE_KEY,
                            null
                        );

                        location.reload();
                    }
                }
            );

            button(
                'Export',
                () => {
                    const data =
                        this.exportData();

                    const blob =
                        new Blob(
                            [
                                JSON.stringify(
                                    data,
                                    null,
                                    2
                                )
                            ],
                            {
                                type:
                                    'application/json'
                            }
                        );

                    const url =
                        URL.createObjectURL(
                            blob
                        );

                    const anchor =
                        document.createElement(
                            'a'
                        );

                    anchor.href = url;

                    anchor.download =
                        `gde-${Date.now()}.json`;

                    anchor.click();

                    setTimeout(
                        () =>
                            URL.revokeObjectURL(
                                url
                            ),
                        1000
                    );
                }
            );

            panel.appendChild(
                stats
            );

            panel.appendChild(
                buttons
            );

            (
                document.body ||
                document.documentElement
            )?.appendChild(panel);

            this.ui = {
                panel,
                stats
            };

            this.updateUI();
        }

        updateUI() {
            if (!this.ui) {
                return;
            }
            if (typeof requestAnimationFrame === 'function') {
                if (this._uiRaf) return;
                this._uiRaf = requestAnimationFrame(() => {
                    this._uiRaf = null;
                    this._doUpdateUI();
                });
                return;
            }
            this._doUpdateUI();
        }

        _doUpdateUI() {
            const s =
                this.db.stats;
            const cov =
                this.getCoverageMetrics();

            this.ui.stats.textContent =
                [
                    `GDE v${CONFIG.version}`,
                    `state=${
                        this.stopRequested
                            ? 'stopped'
                            : this.paused
                                ? 'paused'
                                : this.running
                                    ? 'running'
                                    : 'idle'
                    }`,
                    `candidates=${this.db.candidates.size} (live ${cov.liveCount})`,
                    `queued=${cov.frontierSize} ${JSON.stringify(cov.queuedByType)}`,
                    `active=${this.activeWorkers}`,
                    `requests=${this.requestsReserved}/${CONFIG.maxRequests} (remain ${cov.requestsRemaining})`,
                    `concurrency=${this.currentConcurrency}`,
                    `visited=${cov.visitedSize} resources=${cov.knownResources}`,
                    `acquired=${s.acquired}`,
                    `recognized=${s.recognized}`,
                    `expanded=${s.expanded}`,
                    `completed=${s.completed}`,
                    `skipped=${s.skipped}`,
                    `failed=${s.failed}`,
                    `ledger=${this.ledger.events.length} edges=${cov.graphEdges} obs=${cov.observations}`
                ].join('\n');
        }
    }

    /*
     * ============================================================
     * BOOT
     * ============================================================
     */

    const engine =
        new GenericDiscoveryEngine();

    window.GenericDiscoveryEngine =
        engine;

    engine.init();

})();
