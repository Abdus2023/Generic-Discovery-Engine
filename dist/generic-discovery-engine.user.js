// ==UserScript==
// @name         Generic Discovery Engine
// @namespace    generic-discovery
// @version      0.7.5
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
     * v0.7.5 — Trust & Verification (Trusted Types + fuzz + CI + ADRs)
     *
     * Patch notes vs v0.7.4:
     * - Trust: Trusted Types policy (gde-bridge) for installBridge()
     *         + JSDoc typedefs for Candidate/Observation/Discovery/
     *           ResourceRecord/Provider + CI workflow verify.yml +
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

            candidate.status = 'claimed';
            candidate.claimedAt = now();

            this.claimed.add(candidate.id);
            this.stats.claimed++;

            return candidate;
        }

        markPlanned(candidate) {
            candidate.status = 'planned';
            candidate.plannedAt = now();
            this.stats.planned++;
        }

        markAcquiring(candidate) {
            candidate.status = 'acquiring';
            candidate.acquiringAt = now();
        }

        markObserved(candidate) {
            candidate.status = 'observed';
            candidate.observedAt = now();
        }

        markRecognized(candidate) {
            candidate.status = 'recognized';
            candidate.recognizedAt = now();
            this.stats.recognized++;
        }

        markExpanded(candidate) {
            candidate.status = 'expanded';
            candidate.expandedAt = now();
            this.stats.expanded++;
        }

        markCompleted(candidate) {
            candidate.status = 'completed';
            candidate.completedAt = now();
            this.visited.add(candidate.identityKey());
            this.stats.completed++;
        }

        markSkipped(candidate, reason) {
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
            this.providers = [
                new HtmlProvider(),
                new JsonProvider(),
                new XmlProvider(),
                new CssProvider(),
                new JavaScriptProvider(),
                new BinaryProvider(),
                new TextProvider()
            ];
        }

        matching(observation) {
            return this.providers.filter(
                provider =>
                    provider.matches(
                        observation
                    )
            );
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
            const queuedByType = {};
            for (const c of queued) {
                queuedByType[c.type] =
                    (queuedByType[c.type] ||
                        0) + 1;
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
                    this.db.observations.size
            };
        }

        exportData() {
            return {
                schema: 'gde-export-v8.0',

                exportedAt:
                    new Date().toISOString(),

                config: {
                    ...CONFIG
                },

                coverage:
                    this.getCoverageMetrics(),

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
