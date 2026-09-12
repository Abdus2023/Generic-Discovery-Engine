// ==UserScript==
// @name         Generic Discovery Engine
// @namespace    generic-discovery
// @version      0.5.0
// @description  Generic web-resource discovery engine inspired by the architecture of DVB blind scanning.
// @match        *://*/*
// @grant        GM_getValue
// @grant        GM_setValue
// @grant        GM_xmlhttpRequest
// @connect      *
// @run-at       document-start
// ==/UserScript==

(() => {
    'use strict';

    /* =====================================================================
     * GENERIC DISCOVERY ENGINE v0.5.0
     * =====================================================================
     *
     * Generic discovery architecture:
     *
     *     observation
     *          ↓
     *       candidate
     *          ↓
     *       scheduler
     *          ↓
     *      acquisition
     *          ↓
     *      observation
     *          ↓
     *       provider
     *          ↓
     *      discovery
     *          ↓
     *   provenance graph
     *          ↓
     *    new candidates
     *
     * Sources:
     *
     *   - current document
     *   - DOM mutations
     *   - page fetch()
     *   - page XMLHttpRequest
     *   - PerformanceObserver
     *   - active HTTP acquisition
     *
     * Providers:
     *
     *   - HTML
     *   - JSON
     *   - Web Manifest
     *   - XML
     *   - Sitemap
     *   - robots.txt
     *   - OpenAPI / Swagger
     *   - CSS
     *   - JavaScript / text
     *
     * This is NOT an RF/DVB scanner.
     *
     * It does not access radio hardware, tune frequencies, demodulate
     * signals, or perform DVB synchronization.
     *
     * ===================================================================== */


    // =====================================================================
    // CONFIG
    // =====================================================================

    const CONFIG = {
        maxCandidates: 1000,
        maxRequests: 200,
        concurrency: 4,

        requestTimeout: 8000,
        maxResponseBytes: 2 * 1024 * 1024,

        sameOriginOnly: true,

        maxDepth: 8,

        maxRetries: 2,
        retryBaseDelay: 500,
        retryMaxDelay: 8000,

        /*
         * Passive observation.
         */
        observeNetwork: true,
        observePerformance: true,
        observeDomResources: true,

        /*
         * Discovery.
         */
        discoverLinks: true,
        discoverResources: true,
        discoverForms: true,
        discoverMetadata: true,
        discoverFromText: true,
        discoverCss: true,
        discoverApis: true,
        discoverSitemaps: true,

        /*
         * Standard well-known discovery endpoints.
         */
        discoverWellKnown: true,

        /*
         * Persistence.
         */
        persistState: true,
        maxPersistedDiscoveries: 2000,
        maxPersistedVisited: 8000,

        /*
         * Safety bounds.
         */
        maxUrlsPerDiscovery: 500,
        maxGraphNodes: 5000,
        maxGraphEdges: 10000,

        debug: true
    };


    // =====================================================================
    // LOGGING
    // =====================================================================

    const log = (...args) => {
        if (CONFIG.debug) {
            console.log(
                '[Discovery]',
                ...args
            );
        }
    };

    const warn = (...args) => {
        console.warn(
            '[Discovery]',
            ...args
        );
    };


    // =====================================================================
    // UTILITIES
    // =====================================================================

    const now = () =>
        Date.now();

    function makeId(prefix = 'id') {
        return (
            `${prefix}-${now()}-` +
            Math.random()
                .toString(36)
                .slice(2, 10)
        );
    }

    function unique(values) {
        return [
            ...new Set(values)
        ];
    }

    function sleep(ms) {
        return new Promise(
            resolve =>
                setTimeout(
                    resolve,
                    ms
                )
        );
    }

    function clamp(
        value,
        minimum,
        maximum
    ) {
        return Math.min(
            maximum,
            Math.max(
                minimum,
                value
            )
        );
    }

    function normalizeContentType(value) {
        if (!value) {
            return '';
        }

        return String(value)
            .split(';', 1)[0]
            .trim()
            .toLowerCase();
    }

    function canonicalizeUrl(
        value,
        baseUrl = location.href
    ) {
        if (
            !value ||
            typeof value !== 'string'
        ) {
            return null;
        }

        let input =
            value.trim();

        if (!input) {
            return null;
        }

        /*
         * Strip common wrapping characters.
         */
        input =
            input
                .replace(
                    /^["'`]|["'`]$/g,
                    ''
                )
                .trim();

        /*
         * Ignore non-HTTP resource schemes.
         */
        if (
            /^(javascript|mailto|tel|data|blob|about|file|chrome|moz-extension):/i.test(
                input
            )
        ) {
            return null;
        }

        try {
            const url =
                new URL(
                    input,
                    baseUrl
                );

            if (
                url.protocol !==
                    'http:' &&
                url.protocol !==
                    'https:'
            ) {
                return null;
            }

            url.hash = '';

            return url.href;
        } catch {
            return null;
        }
    }

    function isAllowedUrl(url) {
        if (!url) {
            return false;
        }

        if (
            !CONFIG.sameOriginOnly
        ) {
            return true;
        }

        try {
            return (
                new URL(url).origin ===
                location.origin
            );
        } catch {
            return false;
        }
    }

    function looksLikeHtml(body) {
        return (
            /<!doctype\s+html/i.test(
                body
            ) ||
            /<html[\s>]/i.test(
                body
            ) ||
            /<head[\s>]/i.test(
                body
            ) ||
            /<body[\s>]/i.test(
                body
            )
        );
    }

    function looksLikeJson(body) {
        if (!body) {
            return false;
        }

        const value =
            body.trim();

        return (
            value.startsWith('{') ||
            value.startsWith('[')
        );
    }

    function looksLikeXml(body) {
        if (!body) {
            return false;
        }

        const value =
            body.trim();

        return (
            /^<\?xml\b/i.test(
                value
            ) ||
            /^<urlset[\s>]/i.test(
                value
            ) ||
            /^<sitemapindex[\s>]/i.test(
                value
            ) ||
            /^<rss[\s>]/i.test(
                value
            ) ||
            /^<feed[\s>]/i.test(
                value
            )
        );
    }

    function extractUrlsFromText(
        text,
        baseUrl = location.href
    ) {
        if (!text) {
            return [];
        }

        const result = [];

        const absolute =
            text.match(
                /https?:\/\/[^\s"'<>()[\]{}]+/gi
            ) || [];

        for (
            const raw of absolute
        ) {
            const cleaned =
                raw.replace(
                    /[.,;:!?]+$/,
                    ''
                );

            const url =
                canonicalizeUrl(
                    cleaned,
                    baseUrl
                );

            if (
                url &&
                isAllowedUrl(url)
            ) {
                result.push(url);
            }
        }

        /*
         * Root-relative strings.
         */
        const relative =
            text.match(
                /["'`](\/[^"'`\s<>]+)["'`]/g
            ) || [];

        for (
            const value of relative
        ) {
            const match =
                value.match(
                    /["'`](\/[^"'`\s<>]+)["'`]/
                );

            if (!match) {
                continue;
            }

            const url =
                canonicalizeUrl(
                    match[1],
                    baseUrl
                );

            if (
                url &&
                isAllowedUrl(url)
            ) {
                result.push(url);
            }
        }

        return unique(
            result
        ).slice(
            0,
            CONFIG.maxUrlsPerDiscovery
        );
    }

    function extractCssUrls(
        css,
        baseUrl
    ) {
        if (!css) {
            return [];
        }

        const result = [];

        const urlRegex =
            /url\(\s*(['"]?)(.*?)\1\s*\)/gi;

        let match;

        while (
            (match =
                urlRegex.exec(css))
        ) {
            const raw =
                match[2].trim();

            const url =
                canonicalizeUrl(
                    raw,
                    baseUrl
                );

            if (
                url &&
                isAllowedUrl(url)
            ) {
                result.push(url);
            }
        }

        const importRegex =
            /@import\s+(?:url\(\s*)?(['"])(.*?)\1/gi;

        while (
            (match =
                importRegex.exec(css))
        ) {
            const url =
                canonicalizeUrl(
                    match[2],
                    baseUrl
                );

            if (
                url &&
                isAllowedUrl(url)
            ) {
                result.push(url);
            }
        }

        return unique(
            result
        ).slice(
            0,
            CONFIG.maxUrlsPerDiscovery
        );
    }


    // =====================================================================
    // HTTP STATUS CLASSIFICATION
    // =====================================================================

    function classifyHttpStatus(
        status
    ) {
        if (
            status >= 200 &&
            status < 300
        ) {
            return 'success';
        }

        if (
            status >= 300 &&
            status < 400
        ) {
            return 'redirect';
        }

        if (
            status >= 400 &&
            status < 500
        ) {
            return 'client-error';
        }

        if (
            status >= 500
        ) {
            return 'server-error';
        }

        return 'unknown';
    }


    // =====================================================================
    // CANDIDATE
    // =====================================================================

    class Candidate {
        constructor({
            target,
            type = 'url',
            origin = 'unknown',
            priority = 0.5,
            parent = null,
            depth = 0,
            hints = {}
        }) {
            this.id =
                makeId(
                    'candidate'
                );

            this.target =
                target;

            this.type =
                type;

            this.origin =
                origin;

            this.priority =
                clamp(
                    Number(priority) ||
                        0,
                    0,
                    1
                );

            this.parent =
                parent;

            this.depth =
                depth;

            this.hints =
                hints;

            this.createdAt =
                now();

            this.attempts =
                0;

            this.status =
                'queued';

            this.nextAttemptAt =
                0;
        }

        key() {
            /*
             * Type is intentionally NOT part of the primary fingerprint.
             *
             * /api/data discovered by HTML and /api/data discovered by
             * network observation are the same acquisition target.
             */
            return (
                `url:${this.target}`
            );
        }
    }


    // =====================================================================
    // OBSERVATION
    // =====================================================================

    class Observation {
        constructor(candidate) {
            this.id =
                makeId(
                    'observation'
                );

            this.candidateId =
                candidate.id;

            this.target =
                candidate.target;

            this.startedAt =
                now();

            this.completedAt =
                null;

            this.status =
                'unknown';

            this.signalPresent =
                false;

            this.http = {
                status: null,
                statusClass:
                    'unknown',

                contentType: null,

                contentLength: null,

                finalUrl: null
            };

            this.body =
                null;

            this.bodyTruncated =
                false;

            this.errors =
                [];
        }

        complete(status) {
            this.completedAt =
                now();

            this.status =
                status;

            this.http.statusClass =
                classifyHttpStatus(
                    this.http.status
                );
        }
    }


    // =====================================================================
    // DISCOVERY
    // =====================================================================

    class Discovery {
        constructor({
            candidate,
            observation = null,
            kind,
            confidence = 0.5,
            data = {},
            mechanism =
                'active-acquisition'
        }) {
            this.id =
                makeId(
                    'discovery'
                );

            this.candidateId =
                candidate.id;

            this.observationId =
                observation
                    ? observation.id
                    : null;

            this.kind =
                kind;

            this.confidence =
                clamp(
                    Number(confidence) ||
                        0,
                    0,
                    1
                );

            this.mechanism =
                mechanism;

            this.data =
                data;

            this.provenance = {
                origin:
                    candidate.origin,

                parent:
                    candidate.parent,

                depth:
                    candidate.depth,

                candidateType:
                    candidate.type,

                target:
                    candidate.target
            };

            this.createdAt =
                now();
        }
    }


    // =====================================================================
    // GRAPH
    // =====================================================================

    class ProvenanceGraph {
        constructor() {
            this.nodes =
                new Map();

            this.edges =
                new Map();
        }

        addNode(node) {
            if (
                !node ||
                !node.id
            ) {
                return;
            }

            if (
                this.nodes.size >=
                CONFIG.maxGraphNodes
            ) {
                return;
            }

            this.nodes.set(
                node.id,
                node
            );
        }

        addEdge({
            from,
            to,
            relation,
            confidence = 0.5,
            mechanism = null
        }) {
            if (
                !from ||
                !to
            ) {
                return;
            }

            if (
                this.edges.size >=
                CONFIG.maxGraphEdges
            ) {
                return;
            }

            const id =
                makeId(
                    'edge'
                );

            this.edges.set(
                id,
                {
                    id,
                    from,
                    to,
                    relation,
                    confidence,
                    mechanism,
                    createdAt:
                        now()
                }
            );
        }

        addCandidate(candidate) {
            this.addNode({
                id:
                    candidate.id,

                type:
                    'candidate',

                candidateType:
                    candidate.type,

                target:
                    candidate.target,

                depth:
                    candidate.depth
            });

            if (
                candidate.parent
            ) {
                this.addEdge({
                    from:
                        candidate.parent,

                    to:
                        candidate.id,

                    relation:
                        'generated',

                    confidence:
                        candidate.priority,

                    mechanism:
                        candidate.origin
                });
            }
        }

        addDiscovery(discovery) {
            this.addNode({
                id:
                    discovery.id,

                type:
                    'discovery',

                kind:
                    discovery.kind,

                target:
                    discovery.data?.url ||
                    discovery.provenance
                        ?.target ||
                    null,

                confidence:
                    discovery.confidence,

                mechanism:
                    discovery.mechanism
            });

            if (
                discovery.candidateId
            ) {
                this.addEdge({
                    from:
                        discovery.candidateId,

                    to:
                        discovery.id,

                    relation:
                        'observed',

                    confidence:
                        discovery.confidence,

                    mechanism:
                        discovery.mechanism
                });
            }

            if (
                discovery.provenance.parent
            ) {
                this.addEdge({
                    from:
                        discovery.provenance.parent,

                    to:
                        discovery.id,

                    relation:
                        'produced',

                    confidence:
                        discovery.confidence,

                    mechanism:
                        discovery.mechanism
                });
            }
        }

        addPassiveObservation({
            url,
            mechanism,
            status,
            contentType
        }) {
            const id =
                makeId(
                    'passive'
                );

            this.addNode({
                id,

                type:
                    'passive-observation',

                target:
                    url,

                mechanism,

                status,
                contentType
            });

            return id;
        }

        serialize() {
            return {
                nodes:
                    [
                        ...this.nodes.values()
                    ],

                edges:
                    [
                        ...this.edges.values()
                    ]
            };
        }

        clear() {
            this.nodes.clear();
            this.edges.clear();
        }
    }


    // =====================================================================
    // KNOWLEDGE BASE
    // =====================================================================

    class KnowledgeBase {
        constructor() {
            this.candidates =
                new Map();

            this.observations =
                new Map();

            this.discoveries =
                new Map();

            this.visited =
                new Set();

            this.claimed =
                new Set();

            this.graph =
                new ProvenanceGraph();

            this.load();
        }

        candidateKey(candidate) {
            return candidate.key();
        }

        addCandidate(candidate) {
            if (
                !candidate ||
                !candidate.target
            ) {
                return false;
            }

            if (
                candidate.depth >
                CONFIG.maxDepth
            ) {
                return false;
            }

            const key =
                this.candidateKey(
                    candidate
                );

            if (
                this.visited.has(key)
            ) {
                return false;
            }

            if (
                this.claimed.has(key)
            ) {
                return false;
            }

            if (
                this.candidates.has(key)
            ) {
                return false;
            }

            if (
                this.candidates.size >=
                CONFIG.maxCandidates
            ) {
                return false;
            }

            this.candidates.set(
                key,
                candidate
            );

            this.graph.addCandidate(
                candidate
            );

            this.persist();

            return true;
        }

        claimNextCandidate() {
            const entries =
                [
                    ...this.candidates
                        .entries()
                ];

            if (
                !entries.length
            ) {
                return null;
            }

            /*
             * Higher priority first.
             *
             * Depth is a small penalty, preventing deep recursive
             * discovery from completely starving shallow resources.
             */
            entries.sort(
                (a, b) => {
                    const ca =
                        a[1];

                    const cb =
                        b[1];

                    const scoreA =
                        ca.priority -
                        ca.depth *
                            0.025;

                    const scoreB =
                        cb.priority -
                        cb.depth *
                            0.025;

                    return (
                        scoreB -
                        scoreA
                    );
                }
            );

            const timestamp =
                now();

            for (
                const [
                    key,
                    candidate
                ] of entries
            ) {
                if (
                    this.visited.has(
                        key
                    ) ||
                    this.claimed.has(
                        key
                    )
                ) {
                    continue;
                }

                if (
                    candidate.nextAttemptAt >
                    timestamp
                ) {
                    continue;
                }

                /*
                 * Atomic ownership transfer occurs synchronously before
                 * any asynchronous operation.
                 */
                this.candidates.delete(
                    key
                );

                this.claimed.add(
                    key
                );

                candidate.status =
                    'claimed';

                candidate.claimedAt =
                    timestamp;

                this.persist();

                return candidate;
            }

            return null;
        }

        completeCandidate(candidate) {
            const key =
                this.candidateKey(
                    candidate
                );

            this.claimed.delete(
                key
            );

            this.visited.add(
                key
            );

            candidate.status =
                'completed';

            candidate.completedAt =
                now();

            this.persist();
        }

        failCandidate(
            candidate,
            retry = false
        ) {
            const key =
                this.candidateKey(
                    candidate
                );

            this.claimed.delete(
                key
            );

            if (
                retry &&
                candidate.attempts <=
                    CONFIG.maxRetries
            ) {
                candidate.status =
                    'queued';

                const delay =
                    clamp(
                        CONFIG.retryBaseDelay *
                            Math.pow(
                                2,
                                Math.max(
                                    0,
                                    candidate.attempts -
                                        1
                                )
                            ),
                        0,
                        CONFIG.retryMaxDelay
                    );

                candidate.nextAttemptAt =
                    now() +
                    delay;

                this.candidates.set(
                    key,
                    candidate
                );
            } else {
                this.visited.add(
                    key
                );

                candidate.status =
                    'failed';

                candidate.failedAt =
                    now();
            }

            this.persist();
        }

        addObservation(
            observation
        ) {
            this.observations.set(
                observation.id,
                observation
            );
        }

        addDiscovery(
            discovery
        ) {
            this.discoveries.set(
                discovery.id,
                discovery
            );

            this.graph.addDiscovery(
                discovery
            );

            this.persist();
        }

        queueSize() {
            return this.candidates.size;
        }

        claimedSize() {
            return this.claimed.size;
        }

        discoveryCount() {
            return this.discoveries.size;
        }

        serialize() {
            const discoveries =
                [
                    ...this.discoveries
                        .values()
                ];

            const visited =
                [
                    ...this.visited
                ];

            /*
             * Deliberately persist only bounded discovery records.
             *
             * Providers should not place complete HTTP response bodies
             * into discovery.data.
             */
            return {
                version: 5,

                visited:
                    visited.slice(
                        -CONFIG.maxPersistedVisited
                    ),

                discoveries:
                    discoveries.slice(
                        -CONFIG.maxPersistedDiscoveries
                    ),

                graph:
                    this.graph.serialize()
            };
        }

        persist() {
            if (
                !CONFIG.persistState
            ) {
                return;
            }

            try {
                const raw =
                    JSON.stringify(
                        this.serialize()
                    );

                if (
                    typeof GM_setValue ===
                    'function'
                ) {
                    GM_setValue(
                        'discovery-state',
                        raw
                    );
                } else {
                    localStorage.setItem(
                        'generic-discovery-state',
                        raw
                    );
                }
            } catch (error) {
                warn(
                    'Persistence failed:',
                    error
                );
            }
        }

        load() {
            if (
                !CONFIG.persistState
            ) {
                return;
            }

            try {
                let raw =
                    null;

                if (
                    typeof GM_getValue ===
                    'function'
                ) {
                    raw =
                        GM_getValue(
                            'discovery-state',
                            null
                        );
                } else {
                    raw =
                        localStorage.getItem(
                            'generic-discovery-state'
                        );
                }

                if (!raw) {
                    return;
                }

                const data =
                    typeof raw ===
                    'string'
                        ? JSON.parse(
                              raw
                          )
                        : raw;

                if (
                    data.version &&
                    data.version > 5
                ) {
                    warn(
                        'Stored state belongs to a newer version.'
                    );

                    return;
                }

                for (
                    const key of
                    data.visited || []
                ) {
                    this.visited.add(
                        key
                    );
                }

                for (
                    const discovery of
                    data.discoveries ||
                    []
                ) {
                    if (
                        discovery &&
                        discovery.id
                    ) {
                        this.discoveries.set(
                            discovery.id,
                            discovery
                        );
                    }
                }

                for (
                    const node of
                    data.graph?.nodes ||
                    []
                ) {
                    if (
                        node &&
                        node.id
                    ) {
                        this.graph.nodes.set(
                            node.id,
                            node
                        );
                    }
                }

                for (
                    const edge of
                    data.graph?.edges ||
                    []
                ) {
                    if (
                        edge &&
                        edge.id
                    ) {
                        this.graph.edges.set(
                            edge.id,
                            edge
                        );
                    }
                }

                log(
                    'State restored',
                    {
                        visited:
                            this.visited.size,

                        discoveries:
                            this.discoveries
                                .size,

                        graphNodes:
                            this.graph.nodes
                                .size,

                        graphEdges:
                            this.graph.edges
                                .size
                    }
                );
            } catch (error) {
                warn(
                    'State restore failed:',
                    error
                );
            }
        }

        clear() {
            this.candidates.clear();
            this.observations.clear();
            this.discoveries.clear();

            this.visited.clear();
            this.claimed.clear();

            this.graph.clear();

            this.persist();
        }
    }


    // =====================================================================
    // HTTP ACQUISITION
    // =====================================================================

    class HttpAcquisitionAdapter {

        async acquire(candidate) {
            const observation =
                new Observation(
                    candidate
                );

            candidate.attempts++;

            try {
                const response =
                    await this.request(
                        candidate.target,
                        candidate
                    );

                observation.signalPresent =
                    true;

                observation.http.status =
                    response.status;

                observation.http.contentType =
                    response.contentType;

                observation.http.contentLength =
                    response.contentLength;

                observation.http.finalUrl =
                    response.finalUrl ||
                    candidate.target;

                observation.body =
                    response.body;

                observation.bodyTruncated =
                    Boolean(
                        response.bodyTruncated
                    );

                observation.complete(
                    'acquired'
                );
            } catch (error) {
                observation.errors.push(
                    String(error)
                );

                observation.complete(
                    'failed'
                );
            }

            return observation;
        }

        request(
            url,
            candidate
        ) {
            return new Promise(
                (resolve, reject) => {

                    if (
                        typeof GM_xmlhttpRequest ===
                        'function'
                    ) {
                        let settled =
                            false;

                        const finish = (
                            callback,
                            value
                        ) => {
                            if (
                                settled
                            ) {
                                return;
                            }

                            settled =
                                true;

                            callback(
                                value
                            );
                        };

                        GM_xmlhttpRequest({
                            method:
                                candidate
                                    .hints
                                    ?.method ||
                                'GET',

                            url,

                            timeout:
                                CONFIG.requestTimeout,

                            responseType:
                                'text',

                            onload:
                                response => {
                                    const body =
                                        String(
                                            response
                                                .responseText ||
                                                ''
                                        );

                                    const limited =
                                        this.limitBody(
                                            body
                                        );

                                    finish(
                                        resolve,
                                        {
                                            status:
                                                response
                                                    .status,

                                            contentType:
                                                this.extractContentType(
                                                    response.responseHeaders
                                                ),

                                            contentLength:
                                                this.extractContentLength(
                                                    response.responseHeaders
                                                ),

                                            body:
                                                limited
                                                    .body,

                                            bodyTruncated:
                                                limited
                                                    .truncated,

                                            finalUrl:
                                                response
                                                    .finalUrl ||
                                                url
                                        }
                                    );
                                },

                            onerror:
                                () => {
                                    finish(
                                        reject,
                                        new Error(
                                            'request failed'
                                        )
                                    );
                                },

                            ontimeout:
                                () => {
                                    finish(
                                        reject,
                                        new Error(
                                            'request timeout'
                                        )
                                    );
                                },

                            onabort:
                                () => {
                                    finish(
                                        reject,
                                        new Error(
                                            'request aborted'
                                        )
                                    );
                                }
                        });

                        return;
                    }

                    const controller =
                        typeof AbortController !==
                        'undefined'
                            ? new AbortController()
                            : null;

                    let timer =
                        null;

                    if (
                        controller
                    ) {
                        timer =
                            setTimeout(
                                () => {
                                    controller.abort();
                                },
                                CONFIG.requestTimeout
                            );
                    }

                    fetch(
                        url,
                        {
                            method:
                                'GET',

                            credentials:
                                'same-origin',

                            signal:
                                controller
                                    ? controller
                                          .signal
                                    : undefined
                        }
                    )
                        .then(
                            async response => {
                                const body =
                                    await response.text();

                                const limited =
                                    this.limitBody(
                                        body
                                    );

                                return {
                                    status:
                                        response.status,

                                    contentType:
                                        response
                                            .headers
                                            .get(
                                                'content-type'
                                            ),

                                    contentLength:
                                        response
                                            .headers
                                            .get(
                                                'content-length'
                                            ),

                                    body:
                                        limited.body,

                                    bodyTruncated:
                                        limited
                                            .truncated,

                                    finalUrl:
                                        response.url ||
                                        url
                                };
                            }
                        )
                        .then(
                            resolve
                        )
                        .catch(
                            error => {
                                if (
                                    error?.name ===
                                    'AbortError'
                                ) {
                                    reject(
                                        new Error(
                                            'request timeout'
                                        )
                                    );
                                } else {
                                    reject(
                                        error
                                    );
                                }
                            }
                        )
                        .finally(
                            () => {
                                if (
                                    timer
                                ) {
                                    clearTimeout(
                                        timer
                                    );
                                }
                            }
                        );
                }
            );
        }

        limitBody(body) {
            const max =
                CONFIG.maxResponseBytes;

            if (
                body.length <= max
            ) {
                return {
                    body,
                    truncated:
                        false
                };
            }

            return {
                body:
                    body.slice(
                        0,
                        max
                    ),

                truncated:
                    true
            };
        }

        extractContentType(
            headers
        ) {
            if (!headers) {
                return '';
            }

            const match =
                String(
                    headers
                ).match(
                    /^content-type:\s*([^\r\n]+)/im
                );

            return match
                ? match[1].trim()
                : '';
        }

        extractContentLength(
            headers
        ) {
            if (!headers) {
                return null;
            }

            const match =
                String(
                    headers
                ).match(
                    /^content-length:\s*(\d+)/im
                );

            return match
                ? Number(
                      match[1]
                  )
                : null;
        }
    }


    // =====================================================================
    // PROVIDER BASE
    // =====================================================================

    class ResponseProvider {

        score(/* observation */) {
            return 0;
        }

        recognize(
            /* candidate, observation */
        ) {
            return null;
        }

        candidates(
            /* discovery */
        ) {
            return [];
        }
    }


    // =====================================================================
    // HTML PROVIDER
    // =====================================================================

    class HtmlProvider
        extends ResponseProvider {

        score(observation) {
            const type =
                normalizeContentType(
                    observation.http
                        .contentType
                );

            const body =
                observation.body ||
                '';

            if (
                type ===
                'text/html'
            ) {
                return 1;
            }

            if (
                type ===
                'application/xhtml+xml'
            ) {
                return 0.98;
            }

            if (
                looksLikeHtml(body)
            ) {
                return 0.9;
            }

            return 0;
        }

        recognize(
            candidate,
            observation
        ) {
            if (
                this.score(
                    observation
                ) <= 0
            ) {
                return null;
            }

            const body =
                observation.body ||
                '';

            const baseUrl =
                observation.http
                    .finalUrl ||
                candidate.target;

            const doc =
                new DOMParser()
                    .parseFromString(
                        body,
                        'text/html'
                    );

            const title =
                doc.querySelector(
                    'title'
                )
                    ?.textContent
                    ?.trim() ||
                '';

            const links =
                [];

            const resources =
                [];

            const forms =
                [];

            const metadata =
                [];

            const cssUrls =
                [];

            if (
                CONFIG.discoverLinks
            ) {
                for (
                    const element of
                    doc.querySelectorAll(
                        'a[href],area[href]'
                    )
                ) {
                    const url =
                        canonicalizeUrl(
                            element.getAttribute(
                                'href'
                            ),
                            baseUrl
                        );

                    if (
                        url &&
                        isAllowedUrl(
                            url
                        )
                    ) {
                        links.push(
                            url
                        );
                    }
                }
            }

            if (
                CONFIG.discoverResources
            ) {
                const selector = [
                    'script[src]',
                    'link[href]',
                    'img[src]',
                    'iframe[src]',
                    'frame[src]',
                    'source[src]',
                    'video[src]',
                    'audio[src]',
                    'track[src]',
                    'object[data]',
                    'embed[src]',
                    'input[src]',
                    'image[href]'
                ].join(',');

                for (
                    const element of
                    doc.querySelectorAll(
                        selector
                    )
                ) {
                    const raw =
                        element.getAttribute(
                            'src'
                        ) ||
                        element.getAttribute(
                            'href'
                        ) ||
                        element.getAttribute(
                            'data'
                        );

                    const url =
                        canonicalizeUrl(
                            raw,
                            baseUrl
                        );

                    if (
                        url &&
                        isAllowedUrl(
                            url
                        )
                    ) {
                        resources.push(
                            url
                        );
                    }
                }

                for (
                    const element of
                    doc.querySelectorAll(
                        '[srcset]'
                    )
                ) {
                    const srcset =
                        element.getAttribute(
                            'srcset'
                        ) || '';

                    for (
                        const entry of
                        srcset.split(',')
                    ) {
                        const raw =
                            entry
                                .trim()
                                .split(
                                    /\s+/
                                )[0];

                        const url =
                            canonicalizeUrl(
                                raw,
                                baseUrl
                            );

                        if (
                            url &&
                            isAllowedUrl(
                                url
                            )
                        ) {
                            resources.push(
                                url
                            );
                        }
                    }
                }
            }

            if (
                CONFIG.discoverForms
            ) {
                for (
                    const form of
                    doc.querySelectorAll(
                        'form[action]'
                    )
                ) {
                    const url =
                        canonicalizeUrl(
                            form.getAttribute(
                                'action'
                            ),
                            baseUrl
                        );

                    if (
                        url &&
                        isAllowedUrl(
                            url
                        )
                    ) {
                        forms.push(
                            url
                        );
                    }
                }
            }

            if (
                CONFIG.discoverMetadata
            ) {
                for (
                    const element of
                    doc.querySelectorAll(
                        'link[rel][href]'
                    )
                ) {
                    const rel =
                        (
                            element.getAttribute(
                                'rel'
                            ) || ''
                        ).toLowerCase();

                    if (
                        !(
                            rel.includes(
                                'canonical'
                            ) ||
                            rel.includes(
                                'alternate'
                            ) ||
                            rel.includes(
                                'manifest'
                            ) ||
                            rel.includes(
                                'sitemap'
                            ) ||
                            rel.includes(
                                'preload'
                            ) ||
                            rel.includes(
                                'prefetch'
                            )
                        )
                    ) {
                        continue;
                    }

                    const url =
                        canonicalizeUrl(
                            element.getAttribute(
                                'href'
                            ),
                            baseUrl
                        );

                    if (
                        url &&
                        isAllowedUrl(
                            url
                        )
                    ) {
                        metadata.push(
                            url
                        );
                    }
                }

                for (
                    const element of
                    doc.querySelectorAll(
                        'meta[content]'
                    )
                ) {
                    const property =
                        (
                            element.getAttribute(
                                'property'
                            ) ||
                            element.getAttribute(
                                'name'
                            ) ||
                            ''
                        ).toLowerCase();

                    if (
                        !(
                            property ===
                                'og:url' ||
                            property ===
                                'twitter:url' ||
                            property ===
                                'application-url'
                        )
                    ) {
                        continue;
                    }

                    const url =
                        canonicalizeUrl(
                            element.getAttribute(
                                'content'
                            ),
                            baseUrl
                        );

                    if (
                        url &&
                        isAllowedUrl(
                            url
                        )
                    ) {
                        metadata.push(
                            url
                        );
                    }
                }

                for (
                    const element of
                    doc.querySelectorAll(
                        'meta[http-equiv][content]'
                    )
                ) {
                    const directive =
                        (
                            element.getAttribute(
                                'http-equiv'
                            ) || ''
                        ).toLowerCase();

                    if (
                        directive !==
                        'refresh'
                    ) {
                        continue;
                    }

                    const content =
                        element.getAttribute(
                            'content'
                        ) || '';

                    const match =
                        content.match(
                            /url\s*=\s*(.+)$/i
                        );

                    if (!match) {
                        continue;
                    }

                    const url =
                        canonicalizeUrl(
                            match[1]
                                .trim()
                                .replace(
                                    /^['"]|['"]$/g,
                                    ''
                                ),
                            baseUrl
                        );

                    if (
                        url &&
                        isAllowedUrl(
                            url
                        )
                    ) {
                        metadata.push(
                            url
                        );
                    }
                }
            }

            if (
                CONFIG.discoverCss
            ) {
                for (
                    const style of
                    doc.querySelectorAll(
                        'style'
                    )
                ) {
                    cssUrls.push(
                        ...extractCssUrls(
                            style.textContent ||
                                '',
                            baseUrl
                        )
                    );
                }
            }

            const embeddedUrls =
                CONFIG.discoverFromText
                    ? extractUrlsFromText(
                          body,
                          baseUrl
                      )
                    : [];

            return new Discovery({
                candidate,
                observation,

                kind:
                    'html-document',

                confidence:
                    0.96,

                data: {
                    url:
                        candidate.target,

                    finalUrl:
                        baseUrl,

                    title,

                    links:
                        unique(
                            links
                        ).slice(
                            0,
                            CONFIG.maxUrlsPerDiscovery
                        ),

                    resources:
                        unique(
                            resources
                        ).slice(
                            0,
                            CONFIG.maxUrlsPerDiscovery
                        ),

                    forms:
                        unique(
                            forms
                        ).slice(
                            0,
                            CONFIG.maxUrlsPerDiscovery
                        ),

                    metadata:
                        unique(
                            metadata
                        ).slice(
                            0,
                            CONFIG.maxUrlsPerDiscovery
                        ),

                    embeddedUrls:
                        unique(
                            embeddedUrls
                        ).slice(
                            0,
                            CONFIG.maxUrlsPerDiscovery
                        ),

                    cssUrls:
                        unique(
                            cssUrls
                        ).slice(
                            0,
                            CONFIG.maxUrlsPerDiscovery
                        )
                }
            });
        }

        candidates(
            discovery
        ) {
            const depth =
                (
                    discovery
                        .provenance
                        .depth ||
                    0
                ) + 1;

            const result = [];

            const add =
                (
                    urls,
                    type,
                    priority
                ) => {
                    for (
                        const url of
                        urls || []
                    ) {
                        result.push(
                            makeDerivedCandidate(
                                url,
                                type,
                                discovery,
                                priority,
                                depth
                            )
                        );
                    }
                };

            if (
                CONFIG.discoverLinks
            ) {
                add(
                    discovery.data.links,
                    'url',
                    0.8
                );
            }

            if (
                CONFIG.discoverResources
            ) {
                add(
                    discovery.data.resources,
                    'resource',
                    0.5
                );
            }

            if (
                CONFIG.discoverForms
            ) {
                add(
                    discovery.data.forms,
                    'form',
                    0.6
                );
            }

            if (
                CONFIG.discoverMetadata
            ) {
                add(
                    discovery.data.metadata,
                    'metadata',
                    0.72
                );
            }

            if (
                CONFIG.discoverFromText
            ) {
                add(
                    discovery.data.embeddedUrls,
                    'embedded-url',
                    0.4
                );
            }

            if (
                CONFIG.discoverCss
            ) {
                add(
                    discovery.data.cssUrls,
                    'stylesheet-url',
                    0.45
                );
            }

            return result;
        }
    }


    // =====================================================================
    // JSON PROVIDER
    // =====================================================================

    class JsonProvider
        extends ResponseProvider {

        score(observation) {
            const type =
                normalizeContentType(
                    observation.http
                        .contentType
                );

            if (
                type ===
                'application/json'
            ) {
                return 1;
            }

            if (
                type.endsWith(
                    '+json'
                )
            ) {
                return 0.98;
            }

            if (
                type === '' &&
                looksLikeJson(
                    observation.body
                )
            ) {
                return 0.82;
            }

            return 0;
        }

        recognize(
            candidate,
            observation
        ) {
            if (
                this.score(
                    observation
                ) <= 0
            ) {
                return null;
            }

            let value;

            try {
                value =
                    JSON.parse(
                        observation.body ||
                            ''
                    );
            } catch {
                return null;
            }

            const baseUrl =
                observation.http
                    .finalUrl ||
                candidate.target;

            const urls =
                this.extractUrls(
                    value,
                    baseUrl
                );

            /*
             * Do not persist the complete JSON object.
             */
            const summary =
                this.summarize(
                    value
                );

            return new Discovery({
                candidate,
                observation,

                kind:
                    'json-document',

                confidence:
                    0.95,

                data: {
                    url:
                        candidate.target,

                    finalUrl:
                        baseUrl,

                    summary,

                    urls
                }
            });
        }

        summarize(value) {
            if (
                Array.isArray(value)
            ) {
                return {
                    type:
                        'array',

                    length:
                        value.length
                };
            }

            if (
                value &&
                typeof value ===
                    'object'
            ) {
                return {
                    type:
                        'object',

                    keys:
                        Object.keys(
                            value
                        ).slice(
                            0,
                            100
                        )
                };
            }

            return {
                type:
                    typeof value
            };
        }

        extractUrls(
            value,
            baseUrl
        ) {
            const result = [];

            const visit =
                current => {
                    if (
                        typeof current ===
                        'string'
                    ) {
                        const direct =
                            canonicalizeUrl(
                                current,
                                baseUrl
                            );

                        if (
                            direct &&
                            isAllowedUrl(
                                direct
                            )
                        ) {
                            result.push(
                                direct
                            );
                        }

                        result.push(
                            ...extractUrlsFromText(
                                current,
                                baseUrl
                            )
                        );

                        return;
                    }

                    if (
                        !current ||
                        typeof current !==
                            'object'
                    ) {
                        return;
                    }

                    for (
                        const child of
                        Object.values(
                            current
                        )
                    ) {
                        visit(
                            child
                        );

                        if (
                            result.length >=
                            CONFIG.maxUrlsPerDiscovery
                        ) {
                            return;
                        }
                    }
                };

            visit(value);

            return unique(
                result
            ).slice(
                0,
                CONFIG.maxUrlsPerDiscovery
            );
        }

        candidates(
            discovery
        ) {
            const depth =
                (
                    discovery
                        .provenance
                        .depth ||
                    0
                ) + 1;

            return (
                discovery.data.urls ||
                []
            ).map(
                url =>
                    makeDerivedCandidate(
                        url,
                        'url',
                        discovery,
                        0.7,
                        depth
                    )
            );
        }
    }


    // =====================================================================
    // WEB MANIFEST PROVIDER
    // =====================================================================

    class ManifestProvider
        extends ResponseProvider {

        score(observation) {
            const type =
                normalizeContentType(
                    observation.http
                        .contentType
                );

            return type ===
                'application/manifest+json'
                ? 1
                : 0;
        }

        recognize(
            candidate,
            observation
        ) {
            if (
                this.score(
                    observation
                ) <= 0
            ) {
                return null;
            }

            let value;

            try {
                value =
                    JSON.parse(
                        observation.body ||
                            ''
                    );
            } catch {
                return null;
            }

            const baseUrl =
                observation.http
                    .finalUrl ||
                candidate.target;

            const urls =
                [];

            const visit =
                current => {
                    if (
                        typeof current ===
                        'string'
                    ) {
                        const url =
                            canonicalizeUrl(
                                current,
                                baseUrl
                            );

                        if (
                            url &&
                            isAllowedUrl(
                                url
                            )
                        ) {
                            urls.push(
                                url
                            );
                        }

                        return;
                    }

                    if (
                        !current ||
                        typeof current !==
                            'object'
                    ) {
                        return;
                    }

                    for (
                        const child of
                        Object.values(
                            current
                        )
                    ) {
                        visit(
                            child
                        );
                    }
                };

            visit(value);

            return new Discovery({
                candidate,
                observation,

                kind:
                    'web-manifest',

                confidence:
                    0.98,

                data: {
                    url:
                        candidate.target,

                    finalUrl:
                        baseUrl,

                    name:
                        typeof value.name ===
                        'string'
                            ? value.name
                            : '',

                    startUrl:
                        canonicalizeUrl(
                            value.start_url,
                            baseUrl
                        ),

                    scope:
                        canonicalizeUrl(
                            value.scope,
                            baseUrl
                        ),

                    urls:
                        unique(
                            urls
                        ).slice(
                            0,
                            CONFIG.maxUrlsPerDiscovery
                        )
                }
            });
        }

        candidates(
            discovery
        ) {
            const depth =
                (
                    discovery
                        .provenance
                        .depth ||
                    0
                ) + 1;

            return (
                discovery.data.urls ||
                []
            ).map(
                url =>
                    makeDerivedCandidate(
                        url,
                        'manifest-resource',
                        discovery,
                        0.55,
                        depth
                    )
            );
        }
    }


    // =====================================================================
    // XML / SITEMAP PROVIDER
    // =====================================================================

    class XmlProvider
        extends ResponseProvider {

        score(observation) {
            const type =
                normalizeContentType(
                    observation.http
                        .contentType
                );

            const body =
                observation.body ||
                '';

            if (
                type ===
                'application/xml' ||
                type ===
                'text/xml'
            ) {
                return 1;
            }

            if (
                type.endsWith(
                    '+xml'
                )
            ) {
                return 0.95;
            }

            if (
                type === '' &&
                looksLikeXml(body)
            ) {
                return 0.82;
            }

            return 0;
        }

        recognize(
            candidate,
            observation
        ) {
            if (
                this.score(
                    observation
                ) <= 0
            ) {
                return null;
            }

            const body =
                observation.body ||
                '';

            const baseUrl =
                observation.http
                    .finalUrl ||
                candidate.target;

            const doc =
                new DOMParser()
                    .parseFromString(
                        body,
                        'application/xml'
                    );

            if (
                doc.querySelector(
                    'parsererror'
                )
            ) {
                return null;
            }

            const urls =
                [];

            for (
                const element of
                doc.querySelectorAll(
                    'loc'
                )
            ) {
                const url =
                    canonicalizeUrl(
                        element
                            .textContent
                            ?.trim(),
                        baseUrl
                    );

                if (
                    url &&
                    isAllowedUrl(
                        url
                    )
                ) {
                    urls.push(
                        url
                    );
                }
            }

            for (
                const element of
                doc.querySelectorAll(
                    'link'
                )
            ) {
                const raw =
                    element.getAttribute(
                        'href'
                    ) ||
                    element.textContent
                        ?.trim();

                const url =
                    canonicalizeUrl(
                        raw,
                        baseUrl
                    );

                if (
                    url &&
                    isAllowedUrl(
                        url
                    )
                ) {
                    urls.push(
                        url
                    );
                }
            }

            const root =
                doc.documentElement
                    ?.localName ||
                '';

            let kind =
                'xml-document';

            if (
                root ===
                'urlset'
            ) {
                kind =
                    'sitemap';
            } else if (
                root ===
                'sitemapindex'
            ) {
                kind =
                    'sitemap-index';
            } else if (
                root ===
                'rss'
            ) {
                kind =
                    'rss-feed';
            } else if (
                root ===
                'feed'
            ) {
                kind =
                    'atom-feed';
            }

            return new Discovery({
                candidate,
                observation,

                kind,

                confidence:
                    kind ===
                        'sitemap' ||
                    kind ===
                        'sitemap-index'
                        ? 0.99
                        : 0.88,

                data: {
                    url:
                        candidate.target,

                    finalUrl:
                        baseUrl,

                    root,

                    urls:
                        unique(
                            urls
                        ).slice(
                            0,
                            CONFIG.maxUrlsPerDiscovery
                        )
                }
            });
        }

        candidates(
            discovery
        ) {
            const depth =
                (
                    discovery
                        .provenance
                        .depth ||
                    0
                ) + 1;

            const type =
                discovery.kind ===
                    'sitemap' ||
                discovery.kind ===
                    'sitemap-index'
                    ? 'sitemap-url'
                    : 'xml-url';

            return (
                discovery.data.urls ||
                []
            ).map(
                url =>
                    makeDerivedCandidate(
                        url,
                        type,
                        discovery,
                        0.68,
                        depth
                    )
            );
        }
    }


    // =====================================================================
    // ROBOTS.TXT PROVIDER
    // =====================================================================

    class RobotsProvider
        extends ResponseProvider {

        score(observation) {
            const type =
                normalizeContentType(
                    observation.http
                        .contentType
                );

            const target =
                observation.target
                    .toLowerCase();

            const body =
                observation.body ||
                '';

            if (
                target.endsWith(
                    '/robots.txt'
                )
            ) {
                return 1;
            }

            if (
                type.startsWith(
                    'text/plain'
                ) &&
                /^\s*(user-agent|sitemap|allow|disallow)\s*:/im.test(
                    body
                )
            ) {
                return 0.95;
            }

            return 0;
        }

        recognize(
            candidate,
            observation
        ) {
            if (
                this.score(
                    observation
                ) <= 0
            ) {
                return null;
            }

            const body =
                observation.body ||
                '';

            const baseUrl =
                observation.http
                    .finalUrl ||
                candidate.target;

            const sitemaps =
                [];

            const urls =
                [];

            for (
                const line of
                body.split(/\r?\n/)
            ) {
                const match =
                    line.match(
                        /^\s*Sitemap\s*:\s*(\S+)/i
                    );

                if (
                    !match
                ) {
                    continue;
                }

                const url =
                    canonicalizeUrl(
                        match[1],
                        baseUrl
                    );

                if (
                    url &&
                    isAllowedUrl(
                        url
                    )
                ) {
                    sitemaps.push(
                        url
                    );

                    urls.push(
                        url
                    );
                }
            }

            /*
             * Extract absolute HTTP URLs appearing elsewhere in robots.txt.
             */
            urls.push(
                ...extractUrlsFromText(
                    body,
                    baseUrl
                )
            );

            return new Discovery({
                candidate,
                observation,

                kind:
                    'robots-txt',

                confidence:
                    0.99,

                data: {
                    url:
                        candidate.target,

                    finalUrl:
                        baseUrl,

                    sitemaps:
                        unique(
                            sitemaps
                        ),

                    urls:
                        unique(
                            urls
                        ).slice(
                            0,
                            CONFIG.maxUrlsPerDiscovery
                        )
                }
            });
        }

        candidates(
            discovery
        ) {
            const depth =
                (
                    discovery
                        .provenance
                        .depth ||
                    0
                ) + 1;

            return (
                discovery.data.urls ||
                []
            ).map(
                url =>
                    makeDerivedCandidate(
                        url,
                        'sitemap',
                        discovery,
                        0.9,
                        depth
                    )
            );
        }
    }


    // =====================================================================
    // OPENAPI / SWAGGER PROVIDER
    // =====================================================================

    class ApiDescriptionProvider
        extends ResponseProvider {

        score(observation) {
            const type =
                normalizeContentType(
                    observation.http
                        .contentType
                );

            const body =
                observation.body ||
                '';

            if (
                !(
                    type ===
                        'application/json' ||
                    type.endsWith(
                        '+json'
                    ) ||
                    type === ''
                )
            ) {
                return 0;
            }

            if (
                /"openapi"\s*:/i.test(
                    body
                )
            ) {
                return 1;
            }

            if (
                /"swagger"\s*:/i.test(
                    body
                )
            ) {
                return 0.98;
            }

            return 0;
        }

        recognize(
            candidate,
            observation
        ) {
            if (
                this.score(
                    observation
                ) <= 0
            ) {
                return null;
            }

            let value;

            try {
                value =
                    JSON.parse(
                        observation.body ||
                            ''
                    );
            } catch {
                return null;
            }

            const baseUrl =
                observation.http
                    .finalUrl ||
                candidate.target;

            const urls =
                [];

            /*
             * servers[].url
             */
            for (
                const server of
                value.servers ||
                []
            ) {
                const url =
                    canonicalizeUrl(
                        server?.url,
                        baseUrl
                    );

                if (
                    url &&
                    isAllowedUrl(
                        url
                    )
                ) {
                    urls.push(
                        url
                    );
                }
            }

            /*
             * OpenAPI 2 host/basePath.
             */
            if (
                value.host
            ) {
                const scheme =
                    value.schemes?.[0] ||
                    new URL(
                        baseUrl
                    ).protocol
                        .replace(
                            ':',
                            ''
                        );

                const base =
                    `${scheme}://${value.host}` +
                    (
                        value.basePath ||
                        '/'
                    );

                const url =
                    canonicalizeUrl(
                        base,
                        baseUrl
                    );

                if (
                    url &&
                    isAllowedUrl(
                        url
                    )
                ) {
                    urls.push(
                        url
                    );
                }
            }

            /*
             * External documentation and referenced schemas.
             */
            const references =
                extractJsonReferences(
                    value,
                    baseUrl
                );

            urls.push(
                ...references
            );

            return new Discovery({
                candidate,
                observation,

                kind:
                    'api-description',

                confidence:
                    0.99,

                data: {
                    url:
                        candidate.target,

                    finalUrl:
                        baseUrl,

                    specification:
                        value.openapi ||
                        value.swagger ||
                        null,

                    title:
                        value.info?.title ||
                        '',

                    pathCount:
                        value.paths
                            ? Object.keys(
                                  value.paths
                              ).length
                            : 0,

                    urls:
                        unique(
                            urls
                        ).slice(
                            0,
                            CONFIG.maxUrlsPerDiscovery
                        )
                }
            });
        }

        candidates(
            discovery
        ) {
            const depth =
                (
                    discovery
                        .provenance
                        .depth ||
                    0
                ) + 1;

            return (
                discovery.data.urls ||
                []
            ).map(
                url =>
                    makeDerivedCandidate(
                        url,
                        'api',
                        discovery,
                        0.85,
                        depth
                    )
            );
        }
    }

    function extractJsonReferences(
        value,
        baseUrl
    ) {
        const result =
            [];

        const visit =
            current => {
                if (
                    typeof current ===
                    'string'
                ) {
                    const direct =
                        canonicalizeUrl(
                            current,
                            baseUrl
                        );

                    if (
                        direct &&
                        isAllowedUrl(
                            direct
                        )
                    ) {
                        result.push(
                            direct
                        );
                    }

                    return;
                }

                if (
                    !current ||
                    typeof current !==
                        'object'
                ) {
                    return;
                }

                for (
                    const child of
                    Object.values(
                        current
                    )
                ) {
                    visit(
                        child
                    );
                }
            };

        visit(value);

        return unique(
            result
        );
    }


    // =====================================================================
    // TEXT / CSS / JAVASCRIPT PROVIDER
    // =====================================================================

    class TextProvider
        extends ResponseProvider {

        score(observation) {
            const type =
                normalizeContentType(
                    observation.http
                        .contentType
                );

            if (
                type.startsWith(
                    'text/'
                )
            ) {
                return 0.7;
            }

            if (
                type ===
                    'application/javascript' ||
                type ===
                    'application/x-javascript'
            ) {
                return 0.82;
            }

            /*
             * No Content-Type is treated conservatively.
             */
            if (
                type === '' &&
                !looksLikeHtml(
                    observation.body
                ) &&
                !looksLikeJson(
                    observation.body
                ) &&
                !looksLikeXml(
                    observation.body
                )
            ) {
                return 0.3;
            }

            return 0;
        }

        recognize(
            candidate,
            observation
        ) {
            const score =
                this.score(
                    observation
                );

            if (
                score <= 0
            ) {
                return null;
            }

            const text =
                observation.body ||
                '';

            const baseUrl =
                observation.http
                    .finalUrl ||
                candidate.target;

            const urls =
                extractUrlsFromText(
                    text,
                    baseUrl
                );

            const cssUrls =
                CONFIG.discoverCss
                    ? extractCssUrls(
                          text,
                          baseUrl
                      )
                    : [];

            const contentType =
                normalizeContentType(
                    observation.http
                        .contentType
                );

            const isCss =
                contentType ===
                    'text/css' ||
                /\.css(?:[?#]|$)/i.test(
                    candidate.target
                );

            return new Discovery({
                candidate,
                observation,

                kind:
                    isCss
                        ? 'stylesheet'
                        : 'text-document',

                confidence:
                    isCss
                        ? 0.92
                        : 0.72,

                data: {
                    url:
                        candidate.target,

                    finalUrl:
                        baseUrl,

                    contentType,

                    textLength:
                        text.length,

                    urls:
                        unique(
                            urls
                        ),

                    cssUrls:
                        unique(
                            cssUrls
                        )
                }
            });
        }

        candidates(
            discovery
        ) {
            const depth =
                (
                    discovery
                        .provenance
                        .depth ||
                    0
                ) + 1;

            const result =
                [];

            for (
                const url of
                discovery.data.urls ||
                []
            ) {
                result.push(
                    makeDerivedCandidate(
                        url,
                        'url',
                        discovery,
                        0.4,
                        depth
                    )
                );
            }

            for (
                const url of
                discovery.data.cssUrls ||
                []
            ) {
                result.push(
                    makeDerivedCandidate(
                        url,
                        'stylesheet-url',
                        discovery,
                        0.48,
                        depth
                    )
                );
            }

            return result;
        }
    }


    // =====================================================================
    // PROVIDER REGISTRY
    // =====================================================================

    class ProviderRegistry {

        constructor() {
            /*
             * The registry is scored rather than simply first-match.
             *
             * This prevents a generic JSON provider from stealing an
             * OpenAPI document before the specialized provider sees it.
             */
            this.providers = [
                new ApiDescriptionProvider(),
                new ManifestProvider(),
                new RobotsProvider(),
                new HtmlProvider(),
                new XmlProvider(),
                new JsonProvider(),
                new TextProvider()
            ];
        }

        recognize(
            candidate,
            observation
        ) {
            let best =
                null;

            let bestScore =
                0;

            for (
                const provider of
                this.providers
            ) {
                let score =
                    0;

                try {
                    score =
                        provider.score(
                            observation
                        );
                } catch {
                    score =
                        0;
                }

                if (
                    score <=
                    bestScore
                ) {
                    continue;
                }

                let discovery =
                    null;

                try {
                    discovery =
                        provider.recognize(
                            candidate,
                            observation
                        );
                } catch (error) {
                    warn(
                        'Provider error:',
                        error
                    );

                    discovery =
                        null;
                }

                if (
                    discovery
                ) {
                    best =
                        {
                            provider,
                            discovery
                        };

                    bestScore =
                        score;
                }
            }

            return best;
        }
    }


    // =====================================================================
    // DERIVED CANDIDATE
    // =====================================================================

    function makeDerivedCandidate(
        url,
        type,
        discovery,
        priority,
        depth
    ) {
        return new Candidate({
            target:
                url,

            type,

            origin:
                `${discovery.kind}:${discovery.id}`,

            parent:
                discovery.id,

            priority,

            depth
        });
    }


    // =====================================================================
    // SCHEDULER
    // =====================================================================

    class Scheduler {

        constructor(database) {
            this.database =
                database;
        }

        add(candidate) {
            return this.database
                .addCandidate(
                    candidate
                );
        }

        claim() {
            return this.database
                .claimNextCandidate();
        }

        complete(candidate) {
            this.database
                .completeCandidate(
                    candidate
                );
        }

        fail(
            candidate,
            retry = false
        ) {
            this.database
                .failCandidate(
                    candidate,
                    retry
                );
        }

        size() {
            return this.database
                .queueSize();
        }

        inFlight() {
            return this.database
                .claimedSize();
        }
    }


    // =====================================================================
    // NETWORK BRIDGE
    // =====================================================================

    class NetworkObserver {

        constructor(engine) {
            this.engine =
                engine;

            this.installed =
                false;

            this.channel =
                `generic-discovery-${makeId(
                    'channel'
                )}`;

            this.messageHandler =
                null;

            this.performanceObserver =
                null;
        }

        install() {
            if (
                this.installed
            ) {
                return;
            }

            this.installed =
                true;

            if (
                CONFIG.observeNetwork
            ) {
                this.installPageBridge();
                this.installMessageListener();
            }

            if (
                CONFIG.observePerformance
            ) {
                this.installPerformanceObserver();
            }

            log(
                'Passive network observation enabled'
            );
        }

        installMessageListener() {
            this.messageHandler =
                event => {
                    const data =
                        event.data;

                    if (
                        !data ||
                        data.source !==
                            'GenericDiscoveryNetwork' ||
                        data.channel !==
                            this.channel
                    ) {
                        return;
                    }

                    if (
                        !data.url
                    ) {
                        return;
                    }

                    this.engine
                        .recordPassiveNetwork(
                            {
                                url:
                                    data.url,

                                status:
                                    data.status ??
                                    null,

                                contentType:
                                    data.contentType ??
                                    null,

                                mechanism:
                                    data.mechanism ||
                                    'network'
                            }
                        );
                };

            window.addEventListener(
                'message',
                this.messageHandler
            );
        }

        installPageBridge() {
            /*
             * A userscript sandbox may not share the page's JavaScript
             * execution world. Inject a small page-context bridge so
             * page fetch/XHR activity can be observed.
             *
             * The bridge only reports metadata:
             *   URL
             *   status
             *   Content-Type
             *
             * It does NOT copy response bodies.
             */
            const nonce =
                this.channel;

            const source =
                `
                (() => {
                    const CHANNEL =
                        ${JSON.stringify(
                            nonce
                        )};

                    const SOURCE =
                        'GenericDiscoveryNetwork';

                    const emit = payload => {
                        try {
                            window.postMessage(
                                {
                                    source: SOURCE,
                                    channel: CHANNEL,
                                    ...payload
                                },
                                '*'
                            );
                        } catch {}
                    };

                    try {
                        if (
                            window.__GenericDiscoveryNetworkInstalled
                        ) {
                            return;
                        }

                        window.__GenericDiscoveryNetworkInstalled =
                            true;

                        /*
                         * -------------------------------------------------
                         * fetch()
                         * -------------------------------------------------
                         */

                        if (
                            typeof window.fetch ===
                            'function'
                        ) {
                            const originalFetch =
                                window.fetch;

                            window.fetch =
                                function(...args) {
                                    let requestedUrl =
                                        null;

                                    try {
                                        const input =
                                            args[0];

                                        if (
                                            typeof input ===
                                            'string'
                                        ) {
                                            requestedUrl =
                                                new URL(
                                                    input,
                                                    location.href
                                                ).href;
                                        } else if (
                                            input &&
                                            typeof input.url ===
                                                'string'
                                        ) {
                                            requestedUrl =
                                                new URL(
                                                    input.url,
                                                    location.href
                                                ).href;
                                        }
                                    } catch {}

                                    const promise =
                                        originalFetch.apply(
                                            this,
                                            args
                                        );

                                    if (
                                        requestedUrl
                                    ) {
                                        emit({
                                            mechanism:
                                                'fetch-request',

                                            url:
                                                requestedUrl
                                        });
                                    }

                                    Promise.resolve(
                                        promise
                                    )
                                        .then(
                                            response => {
                                                try {
                                                    emit({
                                                        mechanism:
                                                            'fetch-response',

                                                        url:
                                                            response.url ||
                                                            requestedUrl,

                                                        status:
                                                            response.status,

                                                        contentType:
                                                            response.headers?.get(
                                                                'content-type'
                                                            ) || ''
                                                    });
                                                } catch {}

                                                return response;
                                            }
                                        )
                                        .catch(
                                            () => {}
                                        );

                                    return promise;
                                };
                        }

                        /*
                         * -------------------------------------------------
                         * XMLHttpRequest
                         * -------------------------------------------------
                         */

                        if (
                            typeof XMLHttpRequest !==
                            'undefined'
                        ) {
                            const xhrOpen =
                                XMLHttpRequest
                                    .prototype
                                    .open;

                            const xhrSend =
                                XMLHttpRequest
                                    .prototype
                                    .send;

                            XMLHttpRequest
                                .prototype
                                .open =
                                function(
                                    method,
                                    url,
                                    ...rest
                                ) {
                                    try {
                                        this.__gdUrl =
                                            new URL(
                                                url,
                                                location.href
                                            ).href;

                                        this.__gdMethod =
                                            method;
                                    } catch {
                                        this.__gdUrl =
                                            null;
                                    }

                                    return xhrOpen.call(
                                        this,
                                        method,
                                        url,
                                        ...rest
                                    );
                                };

                            XMLHttpRequest
                                .prototype
                                .send =
                                function(...args) {
                                    const xhr =
                                        this;

                                    if (
                                        xhr.__gdUrl
                                    ) {
                                        emit({
                                            mechanism:
                                                'xhr-request',

                                            url:
                                                xhr.__gdUrl
                                        });

                                        xhr.addEventListener(
                                            'loadend',
                                            () => {
                                                try {
                                                    emit({
                                                        mechanism:
                                                            'xhr-response',

                                                        url:
                                                            xhr.responseURL ||
                                                            xhr.__gdUrl,

                                                        status:
                                                            xhr.status,

                                                        contentType:
                                                            xhr.getResponseHeader(
                                                                'content-type'
                                                            ) || ''
                                                    });
                                                } catch {}
                                            },
                                            {
                                                once:
                                                    true
                                            }
                                        );
                                    }

                                    return xhrSend.apply(
                                        this,
                                        args
                                    );
                                };
                        }
                    } catch {}
                })();
            `;

            try {
                const script =
                    document.createElement(
                        'script'
                    );

                script.textContent =
                    source;

                (
                    document.documentElement ||
                    document.head ||
                    document.body
                )?.appendChild(
                    script
                );

                script.remove();

                log(
                    'Page network bridge injected'
                );
            } catch (error) {
                warn(
                    'Page network bridge unavailable:',
                    error
                );
            }
        }

        installPerformanceObserver() {
            if (
                typeof PerformanceObserver ===
                'undefined'
            ) {
                return;
            }

            try {
                this.performanceObserver =
                    new PerformanceObserver(
                        list => {
                            for (
                                const entry of
                                list.getEntries()
                            ) {
                                if (
                                    entry &&
                                    entry.name
                                ) {
                                    this.engine
                                        .recordPassiveNetwork(
                                            {
                                                url:
                                                    entry.name,

                                                status:
                                                    null,

                                                contentType:
                                                    null,

                                                mechanism:
                                                    'performance-resource'
                                            }
                                        );
                                }
                            }
                        }
                    );

                this.performanceObserver
                    .observe({
                        type:
                            'resource',

                        buffered:
                            true
                    });

                log(
                    'PerformanceObserver installed'
                );
            } catch (error) {
                warn(
                    'PerformanceObserver unavailable:',
                    error
                );
            }
        }

        dispose() {
            if (
                this.messageHandler
            ) {
                window.removeEventListener(
                    'message',
                    this.messageHandler
                );

                this.messageHandler =
                    null;
            }

            try {
                this.performanceObserver
                    ?.disconnect();
            } catch {}

            this.performanceObserver =
                null;
        }
    }


    // =====================================================================
    // DISCOVERY ENGINE
    // =====================================================================

    class DiscoveryEngine {

        constructor() {
            this.database =
                new KnowledgeBase();

            this.scheduler =
                new Scheduler(
                    this.database
                );

            this.acquisition =
                new HttpAcquisitionAdapter();

            this.providers =
                new ProviderRegistry();

            this.networkObserver =
                new NetworkObserver(
                    this
                );

            this.domObserver =
                null;

            this.running =
                false;

            this.paused =
                false;

            this.stopRequested =
                false;

            this.runId =
                0;

            this.stats =
                this.newStats();

            this.passiveObserved =
                new Set();
        }

        newStats() {
            return {
                startedAt: null,
                finishedAt: null,

                requests: 0,

                discoveries: 0,

                failures: 0,

                retries: 0,

                candidatesCreated: 0,

                candidatesRejected: 0,

                passiveNetworkEvents: 0,

                passiveDomEvents: 0,

                providerMisses: 0
            };
        }

        resetStats() {
            this.stats =
                this.newStats();
        }

        startObservers() {
            this.networkObserver
                .install();

            if (
                CONFIG.observeDomResources
            ) {
                this.installDomObserver();
            }
        }

        installDomObserver() {
            if (
                this.domObserver ||
                typeof MutationObserver ===
                    'undefined'
            ) {
                return;
            }

            const root =
                document.documentElement;

            if (!root) {
                /*
                 * document-start may execute before <html> exists.
                 */
                return;
            }

            this.domObserver =
                new MutationObserver(
                    mutations => {
                        for (
                            const mutation of
                            mutations
                        ) {
                            for (
                                const node of
                                mutation.addedNodes
                            ) {
                                if (
                                    node.nodeType !==
                                    Node.ELEMENT_NODE
                                ) {
                                    continue;
                                }

                                this.inspectDomNode(
                                    node
                                );
                            }
                        }
                    }
                );

            this.domObserver.observe(
                root,
                {
                    subtree:
                        true,

                    childList:
                        true
                }
            );

            log(
                'DOM observer installed'
            );
        }

        inspectDomNode(node) {
            if (
                !node ||
                !node.querySelectorAll
            ) {
                return;
            }

            const selector = [
                'a[href]',
                'area[href]',
                'script[src]',
                'link[href]',
                'img[src]',
                'iframe[src]',
                'frame[src]',
                'source[src]',
                'video[src]',
                'audio[src]',
                'form[action]',
                'object[data]',
                'embed[src]'
            ].join(',');

            const elements =
                [];

            try {
                if (
                    node.matches?.(
                        selector
                    )
                ) {
                    elements.push(
                        node
                    );
                }

                elements.push(
                    ...node.querySelectorAll(
                        selector
                    )
                );
            } catch {
                return;
            }

            for (
                const element of
                elements
            ) {
                this.observeDomElement(
                    element
                );
            }
        }

        observeDomElement(
            element
        ) {
            let raw =
                null;

            let type =
                'dom-resource';

            if (
                element.matches(
                    'a[href],area[href]'
                )
            ) {
                raw =
                    element.getAttribute(
                        'href'
                    );

                type =
                    'dom-link';
            } else if (
                element.matches(
                    'form[action]'
                )
            ) {
                raw =
                    element.getAttribute(
                        'action'
                    );

                type =
                    'dom-form';
            } else {
                raw =
                    element.getAttribute(
                        'src'
                    ) ||
                    element.getAttribute(
                        'href'
                    ) ||
                    element.getAttribute(
                        'data'
                    );
            }

            const url =
                canonicalizeUrl(
                    raw,
                    location.href
                );

            if (
                !url ||
                !isAllowedUrl(
                    url
                )
            ) {
                return;
            }

            const key =
                `dom:${url}`;

            if (
                this.passiveObserved
                    .has(key)
            ) {
                return;
            }

            this.passiveObserved
                .add(key);

            this.stats
                .passiveDomEvents++;

            this.addCandidate(
                new Candidate({
                    target:
                        url,

                    type:
                        type ===
                        'dom-link'
                            ? 'url'
                            : 'resource',

                    origin:
                        'passive-dom',

                    priority:
                        type ===
                        'dom-link'
                            ? 0.68
                            : 0.46,

                    depth: 0
                })
            );
        }

        recordPassiveNetwork({
            url,
            status = null,
            contentType = null,
            mechanism =
                'network'
        }) {
            const canonical =
                canonicalizeUrl(
                    url,
                    location.href
                );

            if (
                !canonical ||
                !isAllowedUrl(
                    canonical
                )
            ) {
                return;
            }

            const key =
                `${mechanism}:${canonical}`;

            if (
                this.passiveObserved
                    .has(key)
            ) {
                return;
            }

            this.passiveObserved
                .add(key);

            this.stats
                .passiveNetworkEvents++;

            const nodeId =
                this.database.graph
                    .addPassiveObservation(
                        {
                            url:
                                canonical,

                            mechanism,

                            status,

                            contentType
                        }
                    );

            const candidate =
                new Candidate({
                    target:
                        canonical,

                    type:
                        'network-resource',

                    origin:
                        `network:${mechanism}`,

                    priority:
                        mechanism.includes(
                            'response'
                        )
                            ? 0.94
                            : 0.88,

                    depth: 0,

                    hints: {
                        observedStatus:
                            status,

                        observedContentType:
                            contentType,

                        mechanism,

                        passiveNodeId:
                            nodeId
                    }
                });

            this.addCandidate(
                candidate
            );
        }

        addCandidate(
            candidate
        ) {
            const added =
                this.scheduler.add(
                    candidate
                );

            if (added) {
                this.stats
                    .candidatesCreated++;
            } else {
                this.stats
                    .candidatesRejected++;
            }

            return added;
        }

        seed() {
            this.startObservers();

            const current =
                canonicalizeUrl(
                    location.href
                );

            if (current) {
                this.addCandidate(
                    new Candidate({
                        target:
                            current,

                        type:
                            'url',

                        origin:
                            'initial-page',

                        priority:
                            1,

                        depth:
                            0
                    })
                );
            }

            if (
                CONFIG.discoverLinks
            ) {
                for (
                    const element of
                    document.querySelectorAll(
                        'a[href],area[href]'
                    )
                ) {
                    const url =
                        canonicalizeUrl(
                            element.getAttribute(
                                'href'
                            ),
                            location.href
                        );

                    if (
                        url &&
                        isAllowedUrl(
                            url
                        )
                    ) {
                        this.addCandidate(
                            new Candidate({
                                target:
                                    url,

                                type:
                                    'url',

                                origin:
                                    'initial-dom',

                                priority:
                                    0.7,

                                depth:
                                    0
                            })
                        );
                    }
                }
            }

            if (
                CONFIG.discoverResources
            ) {
                const selector = [
                    'script[src]',
                    'link[href]',
                    'img[src]',
                    'iframe[src]',
                    'frame[src]',
                    'source[src]',
                    'video[src]',
                    'audio[src]',
                    'track[src]'
                ].join(',');

                for (
                    const element of
                    document.querySelectorAll(
                        selector
                    )
                ) {
                    const raw =
                        element.getAttribute(
                            'src'
                        ) ||
                        element.getAttribute(
                            'href'
                        );

                    const url =
                        canonicalizeUrl(
                            raw,
                            location.href
                        );

                    if (
                        url &&
                        isAllowedUrl(
                            url
                        )
                    ) {
                        this.addCandidate(
                            new Candidate({
                                target:
                                    url,

                                type:
                                    'resource',

                                origin:
                                    'initial-dom',

                                priority:
                                    0.5,

                                depth:
                                    0
                            })
                        );
                    }
                }
            }

            if (
                CONFIG.discoverMetadata
            ) {
                for (
                    const element of
                    document.querySelectorAll(
                        'link[rel][href]'
                    )
                ) {
                    const rel =
                        (
                            element.getAttribute(
                                'rel'
                            ) || ''
                        ).toLowerCase();

                    if (
                        !(
                            rel.includes(
                                'manifest'
                            ) ||
                            rel.includes(
                                'sitemap'
                            ) ||
                            rel.includes(
                                'alternate'
                            ) ||
                            rel.includes(
                                'canonical'
                            )
                        )
                    ) {
                        continue;
                    }

                    const url =
                        canonicalizeUrl(
                            element.getAttribute(
                                'href'
                            ),
                            location.href
                        );

                    if (
                        url &&
                        isAllowedUrl(
                            url
                        )
                    ) {
                        this.addCandidate(
                            new Candidate({
                                target:
                                    url,

                                type:
                                    'metadata',

                                origin:
                                    'initial-dom',

                                priority:
                                    0.78,

                                depth:
                                    0
                            })
                        );
                    }
                }
            }

            /*
             * Standard discovery endpoints.
             */
            if (
                CONFIG.discoverWellKnown
            ) {
                const origin =
                    location.origin;

                const standard =
                    [
                        [
                            `${origin}/robots.txt`,
                            'robots',
                            0.82
                        ],

                        [
                            `${origin}/sitemap.xml`,
                            'sitemap',
                            0.78
                        ],

                        [
                            `${origin}/sitemap_index.xml`,
                            'sitemap',
                            0.72
                        ]
                    ];

                for (
                    const [
                        target,
                        type,
                        priority
                    ] of standard
                ) {
                    this.addCandidate(
                        new Candidate({
                            target,
                            type,
                            origin:
                                'well-known',
                            priority,
                            depth:
                                0
                        })
                    );
                }
            }

            /*
             * Performance entries may have been created before the
             * PerformanceObserver was installed.
             */
            if (
                CONFIG.observePerformance &&
                typeof performance !==
                    'undefined' &&
                typeof performance.getEntriesByType ===
                    'function'
            ) {
                try {
                    for (
                        const entry of
                        performance.getEntriesByType(
                            'resource'
                        )
                    ) {
                        if (
                            entry?.name
                        ) {
                            this.recordPassiveNetwork(
                                {
                                    url:
                                        entry.name,

                                    mechanism:
                                        'performance-initial'
                                }
                            );
                        }
                    }
                } catch {}
            }

            /*
             * MutationObserver may not have been possible at
             * document-start, so install it again after seeding.
             */
            this.installDomObserver();

            if (
                this.domObserver
            ) {
                this.inspectDomNode(
                    document.documentElement
                );
            }

            log(
                'Seed complete',
                {
                    queue:
                        this.scheduler.size()
                }
            );
        }

        async run() {
            if (
                this.running
            ) {
                return;
            }

            this.resetStats();

            this.runId++;
            const currentRun =
                this.runId;

            this.stopRequested =
                false;

            this.paused =
                false;

            this.running =
                true;

            this.stats.startedAt =
                now();

            log(
                'Starting discovery',
                {
                    run:
                        currentRun,

                    concurrency:
                        CONFIG.concurrency,

                    maxRequests:
                        CONFIG.maxRequests,

                    maxDepth:
                        CONFIG.maxDepth
                }
            );

            const workers =
                [];

            for (
                let i = 0;
                i <
                    CONFIG.concurrency;
                i++
            ) {
                workers.push(
                    this.worker(
                        i,
                        currentRun
                    )
                );
            }

            await Promise.all(
                workers
            );

            /*
             * Only the active run may finalize itself.
             */
            if (
                currentRun ===
                this.runId
            ) {
                this.stats.finishedAt =
                    now();

                this.running =
                    false;

                this.paused =
                    false;
            }

            log(
                'Discovery complete',
                this.stats
            );

            this.report();
        }

        async worker(
            workerId,
            currentRun
        ) {
            while (
                this.running &&
                !this.stopRequested &&
                currentRun ===
                    this.runId &&
                this.stats.requests <
                    CONFIG.maxRequests
            ) {
                if (
                    this.paused
                ) {
                    await sleep(
                        100
                    );

                    continue;
                }

                const candidate =
                    this.scheduler.claim();

                if (!candidate) {
                    if (
                        this.scheduler.size() >
                        0
                    ) {
                        await sleep(
                            100
                        );

                        continue;
                    }

                    break;
                }

                this.stats.requests++;

                log(
                    `Worker ${workerId} claimed`,
                    candidate.target
                );

                try {
                    const observation =
                        await this.acquisition
                            .acquire(
                                candidate
                            );

                    if (
                        currentRun !==
                        this.runId
                    ) {
                        /*
                         * The run was superseded.
                         */
                        this.scheduler.fail(
                            candidate,
                            false
                        );

                        continue;
                    }

                    this.database
                        .addObservation(
                            observation
                        );

                    if (
                        observation.status !==
                        'acquired'
                    ) {
                        this.handleFailure(
                            candidate
                        );

                        continue;
                    }

                    const result =
                        this.providers
                            .recognize(
                                candidate,
                                observation
                            );

                    if (!result) {
                        this.stats
                            .providerMisses++;

                        this.scheduler
                            .complete(
                                candidate
                            );

                        continue;
                    }

                    const {
                        provider,
                        discovery
                    } = result;

                    this.database
                        .addDiscovery(
                            discovery
                        );

                    this.stats
                        .discoveries++;

                    log(
                        `Worker ${workerId} discovered`,
                        discovery.kind,
                        candidate.target
                    );

                    let newCandidates =
                        [];

                    try {
                        newCandidates =
                            provider.candidates(
                                discovery
                            );
                    } catch (error) {
                        warn(
                            'Candidate expansion failed:',
                            error
                        );
                    }

                    for (
                        const next of
                        newCandidates
                    ) {
                        if (
                            next.depth <=
                            CONFIG.maxDepth
                        ) {
                            this.addCandidate(
                                next
                            );
                        }
                    }

                    this.scheduler
                        .complete(
                            candidate
                        );
                } catch (error) {
                    warn(
                        `Worker ${workerId} failed:`,
                        error
                    );

                    this.handleFailure(
                        candidate
                    );
                }
            }
        }

        handleFailure(
            candidate
        ) {
            this.stats.failures++;

            if (
                candidate.attempts <=
                CONFIG.maxRetries
            ) {
                this.stats.retries++;

                this.scheduler.fail(
                    candidate,
                    true
                );

                return;
            }

            this.scheduler.fail(
                candidate,
                false
            );
        }

        pause() {
            if (
                this.running
            ) {
                this.paused =
                    true;
            }
        }

        resume() {
            if (
                this.running
            ) {
                this.paused =
                    false;
            }
        }

        stop() {
            if (
                !this.running
            ) {
                return;
            }

            this.stopRequested =
                true;

            this.running =
                false;

            this.runId++;

            log(
                'Discovery stopped'
            );
        }

        export() {
            return {
                version:
                    5,

                scope: {
                    type:
                        'web-resource-discovery',

                    inspiredBy:
                        'DVB blind-scan architecture',

                    rfScanning:
                        false
                },

                timestamp:
                    new Date()
                        .toISOString(),

                page:
                    location.href,

                configuration: {
                    maxCandidates:
                        CONFIG.maxCandidates,

                    maxRequests:
                        CONFIG.maxRequests,

                    concurrency:
                        CONFIG.concurrency,

                    requestTimeout:
                        CONFIG.requestTimeout,

                    maxDepth:
                        CONFIG.maxDepth,

                    sameOriginOnly:
                        CONFIG.sameOriginOnly
                },

                statistics:
                    this.stats,

                queue: {
                    pending:
                        this.scheduler
                            .size(),

                    inFlight:
                        this.scheduler
                            .inFlight()
                },

                discoveries:
                    [
                        ...this.database
                            .discoveries
                            .values()
                    ],

                provenance:
                    this.database.graph
                        .serialize()
            };
        }

        async importState(
            data
        ) {
            if (
                !data ||
                typeof data !==
                    'object'
            ) {
                throw new Error(
                    'Invalid discovery state'
                );
            }

            if (
                data.version >
                5
            ) {
                throw new Error(
                    'State belongs to a newer engine version'
                );
            }

            if (
                this.running
            ) {
                throw new Error(
                    'Stop the current scan before importing'
                );
            }

            this.database.clear();

            for (
                const key of
                data.provenance
                    ?.nodes || []
            ) {
                if (
                    key?.id
                ) {
                    this.database
                        .graph
                        .nodes.set(
                            key.id,
                            key
                        );
                }
            }

            for (
                const edge of
                data.provenance
                    ?.edges || []
            ) {
                if (
                    edge?.id
                ) {
                    this.database
                        .graph
                        .edges.set(
                            edge.id,
                            edge
                        );
                }
            }

            for (
                const discovery of
                data.discoveries ||
                []
            ) {
                if (
                    discovery?.id
                ) {
                    this.database
                        .discoveries
                        .set(
                            discovery.id,
                            discovery
                        );
                }
            }

            this.database
                .persist();
        }

        report() {
            const discoveries =
                [
                    ...this.database
                        .discoveries
                        .values()
                ];

            console.group(
                '[Discovery] Results'
            );

            console.table(
                discoveries.map(
                    discovery => ({
                        kind:
                            discovery.kind,

                        confidence:
                            discovery.confidence,

                        mechanism:
                            discovery.mechanism,

                        depth:
                            discovery
                                .provenance
                                ?.depth ??
                            '',

                        type:
                            discovery
                                .provenance
                                ?.candidateType ||
                            '',

                        url:
                            discovery.data
                                ?.url ||
                            '',

                        title:
                            discovery.data
                                ?.title ||
                            ''
                    })
                )
            );

            console.log(
                'Queue:',
                this.scheduler.size()
            );

            console.log(
                'In flight:',
                this.scheduler.inFlight()
            );

            console.log(
                'Graph nodes:',
                this.database.graph
                    .nodes.size
            );

            console.log(
                'Graph edges:',
                this.database.graph
                    .edges.size
            );

            console.log(
                'Statistics:',
                this.stats
            );

            console.groupEnd();
        }

        clear() {
            if (
                this.running
            ) {
                return false;
            }

            this.database.clear();

            this.passiveObserved
                .clear();

            this.resetStats();

            return true;
        }
    }


    // =====================================================================
    // ENGINE INSTANCE
    // =====================================================================

    const engine =
        new DiscoveryEngine();

    window.GenericDiscovery =
        engine;


    // =====================================================================
    // UI
    // =====================================================================

    function installUi() {
        document.getElementById(
            'generic-discovery-panel'
        )?.remove();

        const panel =
            document.createElement(
                'div'
            );

        panel.id =
            'generic-discovery-panel';

        panel.style.cssText = `
            position: fixed;
            right: 12px;
            bottom: 12px;
            z-index: 2147483647;

            background: rgba(20,20,20,.96);
            color: white;

            padding: 10px;

            border-radius: 8px;

            font: 12px monospace;
            line-height: 1.45;

            box-shadow:
                0 3px 15px rgba(0,0,0,.45);

            min-width: 315px;

            user-select: none;
        `;

        panel.innerHTML = `
            <div style="
                margin-bottom:6px;
            ">
                <strong>
                    Generic Discovery v0.5
                </strong>
            </div>

            <div style="
                margin-bottom:8px;
                opacity:.7;
                max-width:320px;
            ">
                Web-resource discovery engine
                with passive network observation
                and provenance tracking.
            </div>

            <div style="
                margin-bottom:8px;
            ">
                <button id="gd-start">
                    Scan
                </button>

                <button id="gd-pause">
                    Pause
                </button>

                <button id="gd-stop">
                    Stop
                </button>

                <button id="gd-clear">
                    Clear
                </button>

                <button id="gd-export">
                    Export
                </button>
            </div>

            <div id="gd-status">
                idle
            </div>

            <div id="gd-progress" style="
                margin-top:6px;
                opacity:.85;
            ">
                queue: 0 |
                in-flight: 0
            </div>

            <div id="gd-network" style="
                margin-top:4px;
                opacity:.7;
            ">
                network: 0 |
                DOM: 0
            </div>

            <div id="gd-graph" style="
                margin-top:4px;
                opacity:.7;
            ">
                graph: 0 nodes / 0 edges
            </div>
        `;

        const attach =
            () => {
                (
                    document.documentElement ||
                    document.body
                )?.appendChild(
                    panel
                );
            };

        attach();

        return panel;
    }

    function initializeUi() {
        const panel =
            installUi();

        if (!panel) {
            return;
        }

        const status =
            panel.querySelector(
                '#gd-status'
            );

        const progress =
            panel.querySelector(
                '#gd-progress'
            );

        const network =
            panel.querySelector(
                '#gd-network'
            );

        const graph =
            panel.querySelector(
                '#gd-graph'
            );

        function updateUi() {
            const stats =
                engine.stats;

            const queue =
                engine.scheduler
                    .size();

            const inFlight =
                engine.scheduler
                    .inFlight();

            if (
                engine.running
            ) {
                status.textContent =
                    engine.paused
                        ? 'paused'
                        : 'scanning...';
            }

            progress.textContent =
                `queue: ${queue} | ` +
                `in-flight: ${inFlight} | ` +
                `requests: ${stats.requests}/${CONFIG.maxRequests} | ` +
                `discoveries: ${stats.discoveries}`;

            network.textContent =
                `network: ${stats.passiveNetworkEvents} | ` +
                `DOM: ${stats.passiveDomEvents} | ` +
                `failures: ${stats.failures} | ` +
                `retries: ${stats.retries}`;

            graph.textContent =
                `graph: ${engine.database.graph.nodes.size} nodes / ` +
                `${engine.database.graph.edges.size} edges`;
        }

        let timer =
            setInterval(
                updateUi,
                250
            );

        const startButton =
            panel.querySelector(
                '#gd-start'
            );

        const pauseButton =
            panel.querySelector(
                '#gd-pause'
            );

        const stopButton =
            panel.querySelector(
                '#gd-stop'
            );

        const clearButton =
            panel.querySelector(
                '#gd-clear'
            );

        const exportButton =
            panel.querySelector(
                '#gd-export'
            );

        startButton.addEventListener(
            'click',
            async () => {
                if (
                    engine.running
                ) {
                    return;
                }

                status.textContent =
                    'seeding...';

                engine.seed();

                updateUi();

                try {
                    await engine.run();

                    status.textContent =
                        `done — ` +
                        `${engine.stats.discoveries} discoveries`;
                } catch (error) {
                    warn(
                        'Run failed:',
                        error
                    );

                    status.textContent =
                        'error — see console';
                }

                updateUi();
            }
        );

        pauseButton.addEventListener(
            'click',
            () => {
                if (
                    !engine.running
                ) {
                    return;
                }

                if (
                    engine.paused
                ) {
                    engine.resume();

                    status.textContent =
                        'scanning...';
                } else {
                    engine.pause();

                    status.textContent =
                        'paused';
                }

                updateUi();
            }
        );

        stopButton.addEventListener(
            'click',
            () => {
                engine.stop();

                status.textContent =
                    'stopped';

                updateUi();
            }
        );

        clearButton.addEventListener(
            'click',
            () => {
                if (
                    engine.running
                ) {
                    status.textContent =
                        'stop the scan first';

                    return;
                }

                if (
                    engine.clear()
                ) {
                    status.textContent =
                        'cleared';
                }

                updateUi();
            }
        );

        exportButton.addEventListener(
            'click',
            () => {
                try {
                    const data =
                        engine.export();

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

                    anchor.href =
                        url;

                    anchor.download =
                        `discovery-${Date.now()}.json`;

                    document.body.appendChild(
                        anchor
                    );

                    anchor.click();

                    anchor.remove();

                    setTimeout(
                        () => {
                            URL.revokeObjectURL(
                                url
                            );
                        },
                        1000
                    );
                } catch (error) {
                    warn(
                        'Export failed:',
                        error
                    );
                }
            }
        );

        /*
         * If the script executes at document-start, the document root may
         * not exist yet. Reattach the UI once DOMContentLoaded fires.
         */
        document.addEventListener(
            'DOMContentLoaded',
            () => {
                if (
                    !document.getElementById(
                        'generic-discovery-panel'
                    )
                ) {
                    initializeUi();
                }

                engine.installDomObserver();
            },
            {
                once: true
            }
        );

        updateUi();

        /*
         * Keep the timer bounded if the page is destroyed.
         */
        window.addEventListener(
            'pagehide',
            () => {
                if (timer) {
                    clearInterval(
                        timer
                    );

                    timer =
                        null;
                }

                engine.networkObserver
                    .dispose();
            },
            {
                once: true
            }
        );
    }


    // =====================================================================
    // STARTUP
    // =====================================================================

    /*
     * At document-start the DOM may not exist.
     */
    if (
        document.documentElement
    ) {
        initializeUi();
    } else {
        document.addEventListener(
            'DOMContentLoaded',
            initializeUi,
            {
                once: true
            }
        );
    }

    log(
        'Generic Discovery Engine v0.5.0 loaded'
    );

})();
