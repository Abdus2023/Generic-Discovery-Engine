// ==UserScript==
// @name         Generic Discovery Engine
// @namespace    generic-discovery
// @version      0.4.0
// @description  Generic web-resource discovery engine inspired by the architecture of DVB blind scanning.
// @match        *://*/*
// @run-at       document-start
// @grant        GM_getValue
// @grant        GM_setValue
// @grant        GM_xmlhttpRequest
// @grant        unsafeWindow
// @connect      *
// ==/UserScript==

(() => {
    'use strict';

    /* =====================================================================
     * GENERIC DISCOVERY ENGINE v0.4.0
     * =====================================================================
     *
     * Architecture:
     *
     *     candidate
     *         ↓
     *     scheduler
     *         ↓
     *     acquisition
     *         ↓
     *     observation
     *         ↓
     *     recognition/provider
     *         ↓
     *     discovery
     *         ↓
     *     new candidates
     *         ↓
     *     scheduler
     *
     * Network-observation path:
     *
     *     page fetch/XHR
     *         ↓
     *     page-context bridge
     *         ↓
     *     userscript
     *         ↓
     *     network candidate
     *         ↓
     *     normal acquisition/discovery pipeline
     *
     * Passive path:
     *
     *     PerformanceResourceTiming
     *         ↓
     *     resource candidate
     *
     * This is NOT a DVB/RF scanner.
     *
     * It does not:
     *   - access RF hardware
     *   - tune frequencies
     *   - synchronize carriers
     *   - perform FEC synchronization
     *   - demodulate DVB signals
     *
     * It applies a similar candidate/acquisition/recognition/discovery
     * architecture to web resources.
     *
     * v0.4.0:
     *   - Page-context fetch/XHR observation
     *   - PerformanceResourceTiming observation
     *   - Atomic candidate claiming
     *   - Depth-aware scheduling
     *   - Exponential retry backoff
     *   - Maximum discovery depth
     *   - HTML metadata discovery
     *   - Manifest discovery
     *   - robots.txt discovery
     *   - sitemap.xml discovery
     *   - XML/sitemap provider
     *   - CSS provider
     *   - JavaScript provider
     *   - Embedded URL extraction
     *   - Bounded persistence
     *   - Compact JSON persistence
     *   - Rich provenance
     *   - Graph-oriented export
     *   - Live progress UI
     * ===================================================================== */

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

        persistState: true,
        maxPersistedDiscoveries: 1200,

        maxStoredTextPreview: 300,

        networkBridge: true,

        debug: true
    };

    const STATE_KEY = 'discovery-state';

    const NETWORK_SOURCE =
        'GenericDiscoveryNetworkBridge';

    const NETWORK_CHANNEL =
        `generic-discovery-${Date.now()}-${Math.random()
            .toString(36)
            .slice(2, 10)}`;

    const log = (...args) => {
        if (CONFIG.debug) {
            console.log('[Discovery]', ...args);
        }
    };

    const warn = (...args) => {
        console.warn('[Discovery]', ...args);
    };

    const now = () => Date.now();

    const sleep = ms =>
        new Promise(resolve =>
            setTimeout(resolve, ms)
        );

    function makeId(prefix = 'id') {
        return `${prefix}-${now()}-${Math.random()
            .toString(36)
            .slice(2, 9)}`;
    }

    function unique(values) {
        return [...new Set(values)];
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

        const trimmed = value.trim();

        if (!trimmed) {
            return null;
        }

        if (
            /^(javascript|mailto|tel|data|blob|about|file|chrome|chrome-extension):/i.test(
                trimmed
            )
        ) {
            return null;
        }

        try {
            const url =
                new URL(
                    trimmed,
                    baseUrl
                );

            if (
                url.protocol !== 'http:' &&
                url.protocol !== 'https:'
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

        if (!CONFIG.sameOriginOnly) {
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

    function normalizeContentType(value) {
        if (!value) {
            return '';
        }

        return String(value)
            .split(';', 1)[0]
            .trim()
            .toLowerCase();
    }

    function isHtmlContentType(value) {
        const type =
            normalizeContentType(value);

        return (
            type === 'text/html' ||
            type === 'application/xhtml+xml'
        );
    }

    function isJsonContentType(value) {
        const type =
            normalizeContentType(value);

        return (
            type === 'application/json' ||
            type.endsWith('+json')
        );
    }

    function isXmlContentType(value) {
        const type =
            normalizeContentType(value);

        return (
            type === 'application/xml' ||
            type === 'text/xml' ||
            type === 'application/rss+xml' ||
            type === 'application/atom+xml' ||
            type === 'application/soap+xml' ||
            type === 'application/sitemap+xml' ||
            type === 'text/xml'
        );
    }

    function isCssContentType(value) {
        return (
            normalizeContentType(value) ===
            'text/css'
        );
    }

    function isJavaScriptContentType(value) {
        const type =
            normalizeContentType(value);

        return (
            type ===
                'application/javascript' ||
            type ===
                'application/x-javascript' ||
            type ===
                'text/javascript' ||
            type ===
                'application/ecmascript' ||
            type ===
                'text/ecmascript'
        );
    }

    function isTextContentType(value) {
        const type =
            normalizeContentType(value);

        return (
            type.startsWith('text/') ||
            type === 'application/xml' ||
            type ===
                'application/xhtml+xml' ||
            type ===
                'application/javascript' ||
            type ===
                'application/x-javascript' ||
            type ===
                'application/ld+json' ||
            type ===
                'application/graphql'
        );
    }

    function looksLikeHtml(body) {
        if (!body) {
            return false;
        }

        return (
            /<!doctype\s+html/i.test(body) ||
            /<html[\s>]/i.test(body) ||
            /<head[\s>]/i.test(body) ||
            /<body[\s>]/i.test(body)
        );
    }

    function looksLikeJson(body) {
        if (!body) {
            return false;
        }

        const trimmed =
            body.trim();

        return (
            (trimmed.startsWith('{') &&
                trimmed.endsWith('}')) ||
            (trimmed.startsWith('[') &&
                trimmed.endsWith(']'))
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

        const absoluteMatches =
            text.match(
                /https?:\/\/[^\s"'<>()[\]{}]+/gi
            ) || [];

        for (
            const value of absoluteMatches
        ) {
            const cleaned =
                value.replace(
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

        const quotedRelativeMatches =
            text.match(
                /["'`](\/[^"'`\s<>]+)["'`]/g
            ) || [];

        for (
            const value of
            quotedRelativeMatches
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

        return unique(result);
    }

    function extractCssUrls(
        css,
        baseUrl
    ) {
        if (!css) {
            return [];
        }

        const result = [];

        const regex =
            /url\s*\(\s*(['"]?)(.*?)\1\s*\)/gi;

        let match;

        while (
            (match =
                regex.exec(css)) !== null
        ) {
            const raw =
                match[2]
                    .trim();

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

        const imports =
            css.match(
                /@import\s+(?:url\s*\(\s*)?["']([^"']+)["']/gi
            ) || [];

        for (
            const item of imports
        ) {
            const match =
                item.match(
                    /["']([^"']+)["']/
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

        return unique(result);
    }

    function extractXmlLocs(
        xml,
        baseUrl
    ) {
        if (!xml) {
            return [];
        }

        const result = [];

        try {
            const doc =
                new DOMParser()
                    .parseFromString(
                        xml,
                        'application/xml'
                    );

            const parserError =
                doc.querySelector(
                    'parsererror'
                );

            if (!parserError) {
                for (
                    const element of
                    doc.getElementsByTagName(
                        'loc'
                    )
                ) {
                    const raw =
                        element.textContent
                            ?.trim();

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

                for (
                    const element of
                    doc.querySelectorAll(
                        'link[href]'
                    )
                ) {
                    const raw =
                        element.getAttribute(
                            'href'
                        );

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
            }
        } catch {
            // Fall through to regex extraction.
        }

        const fallback =
            xml.match(
                /<loc[^>]*>\s*([^<]+)\s*<\/loc>/gi
            ) || [];

        for (
            const value of fallback
        ) {
            const match =
                value.match(
                    /<loc[^>]*>\s*([^<]+)\s*<\/loc>/i
                );

            if (!match) {
                continue;
            }

            const url =
                canonicalizeUrl(
                    match[1].trim(),
                    baseUrl
                );

            if (
                url &&
                isAllowedUrl(url)
            ) {
                result.push(url);
            }
        }

        return unique(result);
    }

    class Candidate {
        constructor({
            target,
            type = 'url',
            origin = 'unknown',
            priority = 0.5,
            parent = null,
            hints = {},
            depth = 0
        }) {
            this.id =
                makeId('candidate');

            this.target =
                target;

            this.type =
                type;

            this.origin =
                origin;

            this.parent =
                parent;

            this.priority =
                priority;

            this.hints =
                hints;

            this.depth =
                Math.max(
                    0,
                    Number(depth) || 0
                );

            this.createdAt =
                now();

            this.attempts =
                0;

            this.status =
                'queued';

            this.nextAttemptAt =
                now();
        }

        key() {
            return (
                `${this.type}:${this.target}`
            );
        }

        effectivePriority() {
            return (
                this.priority -
                this.depth *
                    CONFIG.priorityDepthPenalty
            );
        }
    }

    class Observation {
        constructor(candidate) {
            this.id =
                makeId('observation');

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
                contentType: null,
                contentLength: null,
                finalUrl: null
            };

            this.body =
                null;

            this.errors =
                [];

            this.network =
                candidate.type ===
                    'network'
                    ? {
                          observed: true,
                          mechanism:
                              candidate
                                  .hints
                                  ?.mechanism ||
                              null
                      }
                    : null;
        }

        complete(status) {
            this.completedAt =
                now();

            this.status =
                status;
        }
    }

    class Discovery {
        constructor({
            candidate,
            observation,
            kind,
            confidence = 0.5,
            mechanism = 'provider',
            data = {}
        }) {
            this.id =
                makeId('discovery');

            this.candidateId =
                candidate.id;

            this.observationId =
                observation.id;

            this.kind =
                kind;

            this.confidence =
                confidence;

            this.data =
                data;

            this.provenance = {
                origin:
                    candidate.origin,

                parent:
                    candidate.parent,

                candidateTarget:
                    candidate.target,

                candidateType:
                    candidate.type,

                mechanism,

                depth:
                    candidate.depth
            };

            this.createdAt =
                now();
        }
    }

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
                this.visited.has(key) ||
                this.claimed.has(key) ||
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

            this.persist();

            return true;
        }

        claimNextCandidate() {
            const entries = [
                ...this.candidates.entries()
            ];

            if (!entries.length) {
                return null;
            }

            const current =
                now();

            const ready =
                entries.filter(
                    ([key, candidate]) =>
                        !this.visited.has(key) &&
                        !this.claimed.has(key) &&
                        (
                            !candidate.nextAttemptAt ||
                            candidate.nextAttemptAt <=
                                current
                        )
                );

            if (!ready.length) {
                return null;
            }

            ready.sort(
                (a, b) => {
                    const priorityDifference =
                        b[1].effectivePriority() -
                        a[1].effectivePriority();

                    if (
                        priorityDifference !==
                        0
                    ) {
                        return priorityDifference;
                    }

                    return (
                        a[1].createdAt -
                        b[1].createdAt
                    );
                }
            );

            const [
                key,
                candidate
            ] = ready[0];

            /*
             * IMPORTANT:
             *
             * Remove from the queue and mark claimed
             * BEFORE any asynchronous work occurs.
             *
             * This makes candidate claiming atomic from
             * the scheduler's perspective and prevents two
             * workers from acquiring the same candidate.
             */
            this.candidates.delete(key);

            this.claimed.add(key);

            candidate.status =
                'claimed';

            candidate.claimedAt =
                current;

            this.persist();

            return candidate;
        }

        nextReadyDelay() {
            const entries = [
                ...this.candidates.values()
            ];

            if (!entries.length) {
                return null;
            }

            const current =
                now();

            let minimum =
                Infinity;

            for (
                const candidate of
                entries
            ) {
                if (
                    !candidate.nextAttemptAt
                ) {
                    return 0;
                }

                minimum =
                    Math.min(
                        minimum,
                        Math.max(
                            0,
                            candidate.nextAttemptAt -
                                current
                        )
                    );
            }

            return Number.isFinite(
                minimum
            )
                ? minimum
                : null;
        }

        completeCandidate(candidate) {
            const key =
                this.candidateKey(
                    candidate
                );

            this.claimed.delete(key);

            this.visited.add(key);

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

            this.claimed.delete(key);

            if (retry) {
                const exponent =
                    Math.max(
                        0,
                        candidate.attempts -
                            1
                    );

                const delay =
                    Math.min(
                        CONFIG.retryMaxDelay,
                        CONFIG.retryBaseDelay *
                            Math.pow(
                                2,
                                exponent
                            )
                    );

                candidate.status =
                    'queued';

                candidate.nextAttemptAt =
                    now() + delay;

                this.candidates.set(
                    key,
                    candidate
                );
            } else {
                this.visited.add(key);

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

        addDiscovery(discovery) {
            this.discoveries.set(
                discovery.id,
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

            const bounded =
                discoveries.slice(
                    -CONFIG.maxPersistedDiscoveries
                );

            /*
             * Deliberately do not persist:
             *   - response bodies
             *   - observations
             *   - pending candidates
             *
             * Response bodies can be huge and can also contain
             * sensitive application data.
             */
            return {
                version: 4,

                visited: [
                    ...this.visited
                ],

                discoveries:
                    bounded
            };
        }

        persist() {
            if (
                !CONFIG.persistState
            ) {
                return;
            }

            try {
                const data =
                    JSON.stringify(
                        this.serialize()
                    );

                if (
                    typeof GM_setValue ===
                    'function'
                ) {
                    GM_setValue(
                        STATE_KEY,
                        data
                    );
                } else {
                    localStorage.setItem(
                        'generic-discovery-state',
                        data
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
                            STATE_KEY,
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
                        ? JSON.parse(raw)
                        : raw;

                if (
                    data.version &&
                    data.version > 4
                ) {
                    warn(
                        'Stored state is from a newer version.'
                    );

                    return;
                }

                for (
                    const key of
                    data.visited || []
                ) {
                    if (
                        typeof key ===
                        'string'
                    ) {
                        this.visited.add(
                            key
                        );
                    }
                }

                for (
                    const discovery of
                    data.discoveries || []
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

                log(
                    'Restored state',
                    {
                        visited:
                            this.visited.size,

                        discoveries:
                            this.discoveries.size
                    }
                );
            } catch (error) {
                warn(
                    'Could not restore state:',
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

            this.persist();
        }
    }

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
                        candidate.target
                    );

                observation.signalPresent =
                    true;

                observation.http.status =
                    response.status;

                observation.http.contentType =
                    response.contentType;

                observation.http.contentLength =
                    response.contentLength ??
                    (
                        response.body
                            ? response.body.length
                            : 0
                    );

                observation.http.finalUrl =
                    response.finalUrl ||
                    candidate.target;

                observation.body =
                    response.body;

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

        request(url) {
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
                            method: 'GET',

                            url,

                            timeout:
                                CONFIG.requestTimeout,

                            responseType:
                                'text',

                            onload:
                                response => {
                                    const contentType =
                                        this.extractContentType(
                                            response.responseHeaders
                                        );

                                    const contentLength =
                                        this.extractContentLength(
                                            response.responseHeaders
                                        );

                                    finish(
                                        resolve,
                                        {
                                            status:
                                                response.status,

                                            contentType,

                                            contentLength,

                                            body:
                                                response.responseText ||
                                                '',

                                            finalUrl:
                                                response.finalUrl ||
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

                    fetch(url, {
                        method: 'GET',
                        credentials:
                            'same-origin',
                        signal:
                            controller
                                ? controller.signal
                                : undefined
                    })
                        .then(
                            async response => {
                                const body =
                                    await response.text();

                                return {
                                    status:
                                        response.status,

                                    contentType:
                                        response.headers.get(
                                            'content-type'
                                        ),

                                    contentLength:
                                        response.headers.get(
                                            'content-length'
                                        ),

                                    body,

                                    finalUrl:
                                        response.url ||
                                        url
                                };
                            }
                        )
                        .then(resolve)
                        .catch(error => {
                            if (
                                error &&
                                error.name ===
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
                        })
                        .finally(() => {
                            if (
                                timer
                            ) {
                                clearTimeout(
                                    timer
                                );
                            }
                        });
                }
            );
        }

        extractContentType(
            headers
        ) {
            if (!headers) {
                return '';
            }

            const match =
                String(headers).match(
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
                String(headers).match(
                    /^content-length:\s*(\d+)/im
                );

            if (!match) {
                return null;
            }

            const value =
                Number(match[1]);

            return Number.isFinite(
                value
            )
                ? value
                : null;
        }
    }

    class ResponseProvider {
        matches() {
            return false;
        }

        recognize() {
            return null;
        }

        candidates() {
            return [];
        }
    }

    class HtmlProvider
        extends ResponseProvider {

        matches(observation) {
            return (
                isHtmlContentType(
                    observation
                        .http
                        .contentType
                ) ||
                looksLikeHtml(
                    observation.body
                )
            );
        }

        recognize(
            candidate,
            observation
        ) {
            if (
                !this.matches(
                    observation
                )
            ) {
                return null;
            }

            const body =
                observation.body ||
                '';

            const doc =
                new DOMParser()
                    .parseFromString(
                        body,
                        'text/html'
                    );

            /*
             * The fetched document does not have the URL
             * of the current page as its base. Therefore all
             * relative URLs must be resolved explicitly.
             */
            const baseUrl =
                observation.http.finalUrl ||
                candidate.target;

            const explicitBase =
                doc.querySelector(
                    'base[href]'
                );

            const documentBase =
                explicitBase
                    ? canonicalizeUrl(
                          explicitBase.getAttribute(
                              'href'
                          ),
                          baseUrl
                      ) ||
                      baseUrl
                    : baseUrl;

            const title =
                doc.querySelector(
                    'title'
                )
                    ?.textContent
                    ?.trim() || '';

            const links = [];

            if (
                CONFIG.discoverLinks
            ) {
                for (
                    const element of
                    doc.querySelectorAll(
                        'a[href], area[href]'
                    )
                ) {
                    const raw =
                        element.getAttribute(
                            'href'
                        );

                    const url =
                        canonicalizeUrl(
                            raw,
                            documentBase
                        );

                    if (
                        url &&
                        isAllowedUrl(url)
                    ) {
                        links.push(
                            url
                        );
                    }
                }
            }

            const resources = [];

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
                    'image[href]',
                    'use[href]',
                    'use[xlink\\:href]'
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
                        ) ||
                        element.getAttribute(
                            'xlink:href'
                        );

                    const url =
                        canonicalizeUrl(
                            raw,
                            documentBase
                        );

                    if (
                        url &&
                        isAllowedUrl(url)
                    ) {
                        resources.push(
                            url
                        );
                    }
                }
            }

            const forms = [];

            if (
                CONFIG.discoverForms
            ) {
                for (
                    const form of
                    doc.querySelectorAll(
                        'form[action]'
                    )
                ) {
                    const raw =
                        form.getAttribute(
                            'action'
                        );

                    const url =
                        canonicalizeUrl(
                            raw,
                            documentBase
                        );

                    if (
                        url &&
                        isAllowedUrl(url)
                    ) {
                        forms.push(
                            url
                        );
                    }
                }
            }

            const metadata = [];

            if (
                CONFIG.discoverMetadata
            ) {
                const canonical =
                    doc.querySelector(
                        'link[rel~="canonical"][href]'
                    );

                if (canonical) {
                    const url =
                        canonicalizeUrl(
                            canonical.getAttribute(
                                'href'
                            ),
                            documentBase
                        );

                    if (
                        url &&
                        isAllowedUrl(url)
                    ) {
                        metadata.push(
                            url
                        );
                    }
                }

                for (
                    const element of
                    doc.querySelectorAll(
                        'meta[property="og:url"][content], meta[name="twitter:url"][content]'
                    )
                ) {
                    const url =
                        canonicalizeUrl(
                            element.getAttribute(
                                'content'
                            ),
                            documentBase
                        );

                    if (
                        url &&
                        isAllowedUrl(url)
                    ) {
                        metadata.push(
                            url
                        );
                    }
                }

                const manifest =
                    doc.querySelector(
                        'link[rel~="manifest"][href]'
                    );

                if (manifest) {
                    const url =
                        canonicalizeUrl(
                            manifest.getAttribute(
                                'href'
                            ),
                            documentBase
                        );

                    if (
                        url &&
                        isAllowedUrl(url)
                    ) {
                        metadata.push(
                            url
                        );
                    }
                }

                for (
                    const element of
                    doc.querySelectorAll(
                        'link[rel~="sitemap"][href]'
                    )
                ) {
                    const url =
                        canonicalizeUrl(
                            element.getAttribute(
                                'href'
                            ),
                            documentBase
                        );

                    if (
                        url &&
                        isAllowedUrl(url)
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
                    const httpEquiv =
                        element.getAttribute(
                            'http-equiv'
                        );

                    if (
                        !httpEquiv ||
                        httpEquiv.toLowerCase() !==
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

                    const raw =
                        match[1]
                            .trim()
                            .replace(
                                /^['"]|['"]$/g,
                                ''
                            );

                    const url =
                        canonicalizeUrl(
                            raw,
                            documentBase
                        );

                    if (
                        url &&
                        isAllowedUrl(url)
                    ) {
                        metadata.push(
                            url
                        );
                    }
                }
            }

            const embeddedUrls =
                CONFIG.discoverFromText
                    ? extractUrlsFromText(
                          body,
                          documentBase
                      )
                    : [];

            return new Discovery({
                candidate,
                observation,
                kind:
                    'html-document',
                confidence: 0.95,
                mechanism:
                    'html-parser',
                data: {
                    url:
                        candidate.target,

                    finalUrl:
                        documentBase,

                    title,

                    links:
                        unique(
                            links
                        ),

                    resources:
                        unique(
                            resources
                        ),

                    forms:
                        unique(
                            forms
                        ),

                    metadata:
                        unique(
                            metadata
                        ),

                    embeddedUrls:
                        unique(
                            embeddedUrls
                        )
                }
            });
        }

        candidates(discovery) {
            const result = [];

            const depth =
                (
                    discovery
                        .provenance
                        .depth || 0
                ) + 1;

            const parent =
                discovery.id;

            for (
                const url of
                discovery.data.links ||
                []
            ) {
                result.push(
                    new Candidate({
                        target: url,
                        type: 'url',
                        origin:
                            `html:${discovery.id}`,
                        parent,
                        priority: 0.82,
                        depth
                    })
                );
            }

            for (
                const url of
                discovery.data.resources ||
                []
            ) {
                result.push(
                    new Candidate({
                        target: url,
                        type: 'resource',
                        origin:
                            `html:${discovery.id}`,
                        parent,
                        priority: 0.52,
                        depth
                    })
                );
            }

            for (
                const url of
                discovery.data.forms ||
                []
            ) {
                result.push(
                    new Candidate({
                        target: url,
                        type: 'form',
                        origin:
                            `html:${discovery.id}`,
                        parent,
                        priority: 0.62,
                        depth
                    })
                );
            }

            for (
                const url of
                discovery.data.metadata ||
                []
            ) {
                result.push(
                    new Candidate({
                        target: url,
                        type: 'metadata',
                        origin:
                            `html:${discovery.id}`,
                        parent,
                        priority: 0.72,
                        depth
                    })
                );
            }

            for (
                const url of
                discovery.data.embeddedUrls ||
                []
            ) {
                result.push(
                    new Candidate({
                        target: url,
                        type:
                            'embedded-url',
                        origin:
                            `html:${discovery.id}`,
                        parent,
                        priority: 0.42,
                        depth
                    })
                );
            }

            return result;
        }
    }

    class JsonProvider
        extends ResponseProvider {

        matches(observation) {
            const type =
                observation
                    .http
                    .contentType;

            return (
                isJsonContentType(
                    type
                ) ||
                normalizeContentType(
                    type
                ) ===
                    'application/ld+json' ||
                (
                    !type &&
                    looksLikeJson(
                        observation.body
                    )
                )
            );
        }

        recognize(
            candidate,
            observation
        ) {
            if (
                !this.matches(
                    observation
                )
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
                observation
                    .http
                    .finalUrl ||
                candidate.target;

            const urls =
                this.extractUrls(
                    value,
                    baseUrl
                );

            let summary;

            if (
                Array.isArray(value)
            ) {
                summary = {
                    valueType:
                        'array',

                    arrayLength:
                        value.length
                };
            } else if (
                value &&
                typeof value ===
                    'object'
            ) {
                summary = {
                    valueType:
                        'object',

                    keys:
                        Object.keys(
                            value
                        ).slice(
                            0,
                            100
                        )
                };
            } else {
                summary = {
                    valueType:
                        typeof value
                };
            }

            /*
             * Do not store the complete JSON object.
             * API responses can contain large or sensitive data.
             */
            return new Discovery({
                candidate,
                observation,
                kind:
                    'json-document',
                confidence: 0.95,
                mechanism:
                    'json-parser',
                data: {
                    url:
                        candidate.target,

                    finalUrl:
                        baseUrl,

                    ...summary,

                    urls
                }
            });
        }

        extractUrls(
            value,
            baseUrl
        ) {
            const result = [];

            const visit =
                value => {
                    if (
                        typeof value ===
                        'string'
                    ) {
                        const direct =
                            canonicalizeUrl(
                                value,
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
                                value,
                                baseUrl
                            )
                        );

                        return;
                    }

                    if (
                        !value ||
                        typeof value !==
                            'object'
                    ) {
                        return;
                    }

                    for (
                        const child of
                        Object.values(
                            value
                        )
                    ) {
                        visit(child);
                    }
                };

            visit(value);

            return unique(
                result
            );
        }

        candidates(discovery) {
            const depth =
                (
                    discovery
                        .provenance
                        .depth || 0
                ) + 1;

            return (
                discovery.data.urls ||
                []
            ).map(url =>
                new Candidate({
                    target: url,
                    type: 'api',
                    origin:
                        `json:${discovery.id}`,
                    parent:
                        discovery.id,
                    priority: 0.72,
                    depth
                })
            );
        }
    }

    class XmlProvider
        extends ResponseProvider {

        matches(observation) {
            const type =
                observation
                    .http
                    .contentType;

            const body =
                observation.body ||
                '';

            return (
                isXmlContentType(
                    type
                ) ||
                (
                    !isHtmlContentType(
                        type
                    ) &&
                    /<loc[\s>]/i.test(
                        body
                    )
                )
            );
        }

        recognize(
            candidate,
            observation
        ) {
            if (
                !this.matches(
                    observation
                )
            ) {
                return null;
            }

            const baseUrl =
                observation
                    .http
                    .finalUrl ||
                candidate.target;

            const urls =
                extractXmlLocs(
                    observation.body ||
                        '',
                    baseUrl
                );

            return new Discovery({
                candidate,
                observation,
                kind:
                    'xml-document',
                confidence: 0.92,
                mechanism:
                    'xml-parser',
                data: {
                    url:
                        candidate.target,

                    finalUrl:
                        baseUrl,

                    urls,

                    documentType:
                        this.detectType(
                            observation.body ||
                                ''
                        )
                }
            });
        }

        detectType(xml) {
            if (
                /<urlset[\s>]/i.test(
                    xml
                )
            ) {
                return 'sitemap';
            }

            if (
                /<sitemapindex[\s>]/i.test(
                    xml
                )
            ) {
                return 'sitemap-index';
            }

            if (
                /<rss[\s>]/i.test(
                    xml
                )
            ) {
                return 'rss';
            }

            if (
                /<feed[\s>]/i.test(
                    xml
                )
            ) {
                return 'atom';
            }

            return 'xml';
        }

        candidates(discovery) {
            const depth =
                (
                    discovery
                        .provenance
                        .depth || 0
                ) + 1;

            return (
                discovery.data.urls ||
                []
            ).map(url =>
                new Candidate({
                    target: url,
                    type: 'url',
                    origin:
                        `xml:${discovery.id}`,
                    parent:
                        discovery.id,
                    priority: 0.65,
                    depth
                })
            );
        }
    }

    class CssProvider
        extends ResponseProvider {

        matches(observation) {
            return isCssContentType(
                observation
                    .http
                    .contentType
            );
        }

        recognize(
            candidate,
            observation
        ) {
            if (
                !this.matches(
                    observation
                )
            ) {
                return null;
            }

            const baseUrl =
                observation
                    .http
                    .finalUrl ||
                candidate.target;

            const urls =
                extractCssUrls(
                    observation.body ||
                        '',
                    baseUrl
                );

            return new Discovery({
                candidate,
                observation,
                kind:
                    'css-document',
                confidence: 0.9,
                mechanism:
                    'css-parser',
                data: {
                    url:
                        candidate.target,

                    finalUrl:
                        baseUrl,

                    urls
                }
            });
        }

        candidates(discovery) {
            const depth =
                (
                    discovery
                        .provenance
                        .depth || 0
                ) + 1;

            return (
                discovery.data.urls ||
                []
            ).map(url =>
                new Candidate({
                    target: url,
                    type: 'resource',
                    origin:
                        `css:${discovery.id}`,
                    parent:
                        discovery.id,
                    priority: 0.48,
                    depth
                })
            );
        }
    }

    class JavaScriptProvider
        extends ResponseProvider {

        matches(observation) {
            return isJavaScriptContentType(
                observation
                    .http
                    .contentType
            );
        }

        recognize(
            candidate,
            observation
        ) {
            if (
                !this.matches(
                    observation
                )
            ) {
                return null;
            }

            const baseUrl =
                observation
                    .http
                    .finalUrl ||
                candidate.target;

            const text =
                observation.body ||
                '';

            const urls =
                extractUrlsFromText(
                    text,
                    baseUrl
                );

            const sourceMapUrls =
                this.extractSourceMaps(
                    text,
                    baseUrl
                );

            return new Discovery({
                candidate,
                observation,
                kind:
                    'javascript-document',
                confidence: 0.84,
                mechanism:
                    'javascript-text-parser',
                data: {
                    url:
                        candidate.target,

                    finalUrl:
                        baseUrl,

                    textLength:
                        text.length,

                    urls:
                        unique(
                            [
                                ...urls,
                                ...sourceMapUrls
                            ]
                        )
                }
            });
        }

        extractSourceMaps(
            text,
            baseUrl
        ) {
            const result = [];

            const regex =
                /[#@]\s*sourceMappingURL\s*=\s*([^\s]+)/gi;

            let match;

            while (
                (match =
                    regex.exec(text)) !==
                null
            ) {
                const url =
                    canonicalizeUrl(
                        match[1],
                        baseUrl
                    );

                if (
                    url &&
                    isAllowedUrl(url)
                ) {
                    result.push(
                        url
                    );
                }
            }

            return unique(
                result
            );
        }

        candidates(discovery) {
            const depth =
                (
                    discovery
                        .provenance
                        .depth || 0
                ) + 1;

            return (
                discovery.data.urls ||
                []
            ).map(url =>
                new Candidate({
                    target: url,
                    type:
                        url.endsWith(
                            '.map'
                        )
                            ? 'source-map'
                            : 'url',
                    origin:
                        `javascript:${discovery.id}`,
                    parent:
                        discovery.id,
                    priority:
                        url.endsWith(
                            '.map'
                        )
                            ? 0.6
                            : 0.38,
                    depth
                })
            );
        }
    }

    class RobotsProvider
        extends ResponseProvider {

        matches(observation) {
            const target =
                observation.target ||
                '';

            return (
                /\/robots\.txt$/i.test(
                    target
                )
            );
        }

        recognize(
            candidate,
            observation
        ) {
            if (
                !this.matches(
                    observation
                )
            ) {
                return null;
            }

            const text =
                observation.body ||
                '';

            const sitemaps = [];

            for (
                const line of
                text.split(/\r?\n/)
            ) {
                const match =
                    line.match(
                        /^\s*Sitemap\s*:\s*(\S+)/i
                    );

                if (!match) {
                    continue;
                }

                const url =
                    canonicalizeUrl(
                        match[1],
                        observation
                            .http
                            .finalUrl ||
                            candidate.target
                    );

                if (
                    url &&
                    isAllowedUrl(url)
                ) {
                    sitemaps.push(
                        url
                    );
                }
            }

            return new Discovery({
                candidate,
                observation,
                kind:
                    'robots-document',
                confidence: 0.98,
                mechanism:
                    'robots-parser',
                data: {
                    url:
                        candidate.target,

                    finalUrl:
                        observation
                            .http
                            .finalUrl ||
                        candidate.target,

                    sitemaps:
                        unique(
                            sitemaps
                        ),

                    lineCount:
                        text.split(
                            /\r?\n/
                        ).length
                }
            });
        }

        candidates(discovery) {
            const depth =
                (
                    discovery
                        .provenance
                        .depth || 0
                ) + 1;

            return (
                discovery.data.sitemaps ||
                []
            ).map(url =>
                new Candidate({
                    target: url,
                    type: 'sitemap',
                    origin:
                        `robots:${discovery.id}`,
                    parent:
                        discovery.id,
                    priority: 0.9,
                    depth
                })
            );
        }
    }

    class TextProvider
        extends ResponseProvider {

        matches(observation) {
            const type =
                observation
                    .http
                    .contentType;

            /*
             * Unknown content types are accepted only when
             * the response looks textual. This avoids trying
             * to parse arbitrary binary content as text.
             */
            if (
                isTextContentType(
                    type
                )
            ) {
                return true;
            }

            if (
                !type &&
                observation.body
            ) {
                return (
                    !looksLikeHtml(
                        observation.body
                    ) &&
                    !looksLikeJson(
                        observation.body
                    )
                );
            }

            return false;
        }

        recognize(
            candidate,
            observation
        ) {
            if (
                !this.matches(
                    observation
                )
            ) {
                return null;
            }

            const text =
                observation.body ||
                '';

            const baseUrl =
                observation
                    .http
                    .finalUrl ||
                candidate.target;

            const urls =
                CONFIG.discoverFromText
                    ? extractUrlsFromText(
                          text,
                          baseUrl
                      )
                    : [];

            return new Discovery({
                candidate,
                observation,
                kind:
                    'text-document',
                confidence: 0.72,
                mechanism:
                    'text-url-parser',
                data: {
                    url:
                        candidate.target,

                    finalUrl:
                        baseUrl,

                    textLength:
                        text.length,

                    textPreview:
                        text.slice(
                            0,
                            CONFIG.maxStoredTextPreview
                        ),

                    urls
                }
            });
        }

        candidates(discovery) {
            const depth =
                (
                    discovery
                        .provenance
                        .depth || 0
                ) + 1;

            return (
                discovery.data.urls ||
                []
            ).map(url =>
                new Candidate({
                    target: url,
                    type: 'url',
                    origin:
                        `text:${discovery.id}`,
                    parent:
                        discovery.id,
                    priority: 0.38,
                    depth
                })
            );
        }
    }

    class ProviderRegistry {
        constructor() {
            /*
             * Order matters.
             *
             * Specialized providers come before the
             * generic text provider.
             */
            this.providers = [
                new RobotsProvider(),
                new JsonProvider(),
                new HtmlProvider(),
                new XmlProvider(),
                new CssProvider(),
                new JavaScriptProvider(),
                new TextProvider()
            ];
        }

        recognize(
            candidate,
            observation
        ) {
            for (
                const provider of
                this.providers
            ) {
                try {
                    if (
                        !provider.matches(
                            observation
                        )
                    ) {
                        continue;
                    }

                    const discovery =
                        provider.recognize(
                            candidate,
                            observation
                        );

                    if (
                        discovery
                    ) {
                        return {
                            provider,
                            discovery
                        };
                    }
                } catch (error) {
                    warn(
                        'Provider error:',
                        error
                    );
                }
            }

            return null;
        }
    }

    class Scheduler {
        constructor(
            database
        ) {
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

        nextReadyDelay() {
            return this.database
                .nextReadyDelay();
        }
    }

    class NetworkObserver {
        constructor(engine) {
            this.engine =
                engine;

            this.installed =
                false;

            this.performanceObserver =
                null;

            this.install();
        }

        install() {
            if (
                !CONFIG.discoverNetwork &&
                !CONFIG.discoverPerformance
            ) {
                return;
            }

            if (
                CONFIG.discoverNetwork &&
                CONFIG.networkBridge
            ) {
                this.installPageBridge();
            }

            if (
                CONFIG.discoverPerformance
            ) {
                this.installPerformanceObserver();
            }
        }

        installPageBridge() {
            try {
                const script =
                    document.createElement(
                        'script'
                    );

                script.textContent = `
                    (() => {
                        const CHANNEL = ${JSON.stringify(
                            NETWORK_CHANNEL
                        )};
                        const SOURCE = ${JSON.stringify(
                            NETWORK_SOURCE
                        )};

                        if (
                            window.__genericDiscoveryBridgeInstalled
                        ) {
                            return;
                        }

                        window.__genericDiscoveryBridgeInstalled = true;

                        const emit = detail => {
                            try {
                                window.postMessage(
                                    {
                                        source: SOURCE,
                                        channel: CHANNEL,
                                        ...detail
                                    },
                                    '*'
                                );
                            } catch (_) {}
                        };

                        const normalize = value => {
                            try {
                                if (
                                    typeof value === 'string'
                                ) {
                                    return value;
                                }

                                if (
                                    value &&
                                    typeof value.url === 'string'
                                ) {
                                    return value.url;
                                }
                            } catch (_) {}

                            return null;
                        };

                        try {
                            if (
                                typeof window.fetch ===
                                'function'
                            ) {
                                const originalFetch =
                                    window.fetch;

                                window.fetch =
                                    function(input, init) {
                                        const requestUrl =
                                            normalize(input);

                                        emit({
                                            event: 'request',
                                            api: 'fetch',
                                            url: requestUrl,
                                            time: Date.now()
                                        });

                                        return originalFetch
                                            .apply(this, arguments)
                                            .then(
                                                response => {
                                                    emit({
                                                        event: 'response',
                                                        api: 'fetch',
                                                        url:
                                                            response.url ||
                                                            requestUrl,
                                                        status:
                                                            response.status,
                                                        contentType:
                                                            (() => {
                                                                try {
                                                                    return response.headers.get(
                                                                        'content-type'
                                                                    );
                                                                } catch (_) {
                                                                    return null;
                                                                }
                                                            })(),
                                                        time: Date.now()
                                                    });

                                                    return response;
                                                },
                                                error => {
                                                    emit({
                                                        event: 'error',
                                                        api: 'fetch',
                                                        url: requestUrl,
                                                        error:
                                                            String(error),
                                                        time: Date.now()
                                                    });

                                                    throw error;
                                                }
                                            );
                                    };
                            }
                        } catch (_) {}

                        try {
                            const XHR =
                                window.XMLHttpRequest;

                            if (
                                XHR &&
                                XHR.prototype
                            ) {
                                const originalOpen =
                                    XHR.prototype.open;

                                const originalSend =
                                    XHR.prototype.send;

                                XHR.prototype.open =
                                    function(
                                        method,
                                        url
                                    ) {
                                        try {
                                            this.__gdMethod =
                                                method;

                                            this.__gdUrl =
                                                new URL(
                                                    url,
                                                    location.href
                                                ).href;
                                        } catch (_) {
                                            this.__gdUrl =
                                                String(url || '');
                                        }

                                        return originalOpen
                                            .apply(
                                                this,
                                                arguments
                                            );
                                    };

                                XHR.prototype.send =
                                    function() {
                                        const xhr =
                                            this;

                                        try {
                                            emit({
                                                event:
                                                    'request',
                                                api:
                                                    'xhr',
                                                method:
                                                    xhr.__gdMethod ||
                                                    null,
                                                url:
                                                    xhr.__gdUrl ||
                                                    null,
                                                time:
                                                    Date.now()
                                            });

                                            xhr.addEventListener(
                                                'loadend',
                                                () => {
                                                    emit({
                                                        event:
                                                            'response',
                                                        api:
                                                            'xhr',
                                                        method:
                                                            xhr.__gdMethod ||
                                                            null,
                                                        url:
                                                            xhr.responseURL ||
                                                            xhr.__gdUrl ||
                                                            null,
                                                        status:
                                                            xhr.status,
                                                        contentType:
                                                            xhr.getResponseHeader(
                                                                'content-type'
                                                            ),
                                                        time:
                                                            Date.now()
                                                    });
                                                },
                                                {
                                                    once:
                                                        true
                                                }
                                            );
                                        } catch (_) {}

                                        return originalSend
                                            .apply(
                                                this,
                                                arguments
                                            );
                                    };
                            }
                        } catch (_) {}

                        emit({
                            event: 'installed',
                            api: 'bridge',
                            time: Date.now()
                        });
                    })();
                `;

                (
                    document.documentElement ||
                    document.head ||
                    document.body
                )?.appendChild(
                    script
                );

                script.remove();

                this.installed =
                    true;

                log(
                    'Network page bridge installed'
                );
            } catch (error) {
                warn(
                    'Network bridge installation failed:',
                    error
                );
            }

            window.addEventListener(
                'message',
                this.handleMessage.bind(
                    this
                ),
                false
            );
        }

        handleMessage(event) {
            const data =
                event.data;

            if (
                !data ||
                data.source !==
                    NETWORK_SOURCE ||
                data.channel !==
                    NETWORK_CHANNEL
            ) {
                return;
            }

            if (
                data.event ===
                    'installed'
            ) {
                return;
            }

            if (
                !data.url
            ) {
                return;
            }

            this.engine.observeNetwork({
                url:
                    data.url,

                mechanism:
                    data.api ===
                        'xhr'
                        ? 'network-xhr'
                        : 'network-fetch',

                event:
                    data.event,

                status:
                    data.status ??
                    null,

                contentType:
                    data.contentType ??
                    null
            });
        }

        installPerformanceObserver() {
            const process =
                entries => {
                    for (
                        const entry of
                        entries
                    ) {
                        if (
                            !entry ||
                            !entry.name
                        ) {
                            continue;
                        }

                        this.engine.observeNetwork(
                            {
                                url:
                                    entry.name,

                                mechanism:
                                    'performance-resource',

                                event:
                                    'resource',

                                initiatorType:
                                    entry.initiatorType ||
                                    null
                            }
                        );
                    }
                };

            try {
                if (
                    typeof PerformanceObserver !==
                    'undefined'
                ) {
                    this.performanceObserver =
                        new PerformanceObserver(
                            list => {
                                process(
                                    list.getEntries()
                                );
                            }
                        );

                    this.performanceObserver.observe(
                        {
                            entryTypes: [
                                'resource'
                            ]
                        }
                    );
                }
            } catch (error) {
                warn(
                    'PerformanceObserver unavailable:',
                    error
                );
            }

            try {
                process(
                    performance.getEntriesByType(
                        'resource'
                    )
                );
            } catch {
                // Ignore.
            }
        }
    }

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

            this.running =
                false;

            this.stats =
                this.newStats();

            this.networkSeen =
                new Set();

            this.networkObserver =
                null;

            /*
             * Install the observer as early as possible.
             * Performance entries already present will also
             * be processed.
             */
            if (
                CONFIG.discoverNetwork ||
                CONFIG.discoverPerformance
            ) {
                this.networkObserver =
                    new NetworkObserver(
                        this
                    );
            }
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

                networkCandidates: 0,

                performanceCandidates: 0
            };
        }

        resetStats() {
            this.stats =
                this.newStats();
        }

        addCandidate(
            candidate
        ) {
            if (
                !candidate ||
                !candidate.target
            ) {
                this.stats
                    .candidatesRejected++;

                return false;
            }

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

        observeNetwork({
            url,
            mechanism =
                'network',
            event = 'request',
            status = null,
            contentType = null
        }) {
            if (
                !CONFIG.discoverNetwork &&
                mechanism !==
                    'performance-resource'
            ) {
                return;
            }

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
                this.networkSeen.has(
                    key
                )
            ) {
                return;
            }

            this.networkSeen.add(
                key
            );

            const candidate =
                new Candidate({
                    target:
                        canonical,

                    type:
                        'network',

                    origin:
                        mechanism,

                    parent:
                        null,

                    priority:
                        mechanism ===
                            'network-fetch' ||
                        mechanism ===
                            'network-xhr'
                            ? 0.95
                            : 0.82,

                    depth: 0,

                    hints: {
                        mechanism,
                        event,
                        status,
                        contentType
                    }
                });

            const added =
                this.addCandidate(
                    candidate
                );

            if (added) {
                if (
                    mechanism ===
                    'performance-resource'
                ) {
                    this.stats
                        .performanceCandidates++;
                } else {
                    this.stats
                        .networkCandidates++;
                }

                log(
                    'Network candidate:',
                    canonical,
                    mechanism
                );
            }
        }

        seed() {
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
                            1.0,

                        depth: 0
                    })
                );
            }

            if (
                CONFIG.discoverLinks
            ) {
                for (
                    const element of
                    document.querySelectorAll(
                        'a[href], area[href]'
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
                                    0.72,

                                depth: 1
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
                    'track[src]',
                    'object[data]',
                    'embed[src]',
                    'input[src]'
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
                        ) ||
                        element.getAttribute(
                            'data'
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
                                    0.55,

                                depth: 1
                            })
                        );
                    }
                }
            }

            if (
                CONFIG.discoverMetadata
            ) {
                const manifest =
                    document.querySelector(
                        'link[rel~="manifest"][href]'
                    );

                if (manifest) {
                    const url =
                        canonicalizeUrl(
                            manifest.getAttribute(
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
                                    'manifest',

                                origin:
                                    'initial-dom',

                                priority:
                                    0.85,

                                depth: 1
                            })
                        );
                    }
                }
            }

            if (
                CONFIG.discoverWellKnown
            ) {
                const origin =
                    location.origin;

                const wellKnown = [
                    {
                        path:
                            '/robots.txt',

                        type:
                            'robots',

                        priority:
                            0.88
                    },
                    {
                        path:
                            '/sitemap.xml',

                        type:
                            'sitemap',

                        priority:
                            0.86
                    }
                ];

                for (
                    const item of
                    wellKnown
                ) {
                    const url =
                        canonicalizeUrl(
                            item.path,
                            origin
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
                                    item.type,

                                origin:
                                    'well-known',

                                priority:
                                    item.priority,

                                depth: 1
                            })
                        );
                    }
                }
            }

            log(
                'Seed complete',
                {
                    queue:
                        this.scheduler
                            .size(),

                    inFlight:
                        this.scheduler
                            .inFlight()
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

            this.running =
                true;

            this.stats.startedAt =
                now();

            log(
                'Starting discovery',
                {
                    concurrency:
                        CONFIG.concurrency,

                    maxRequests:
                        CONFIG.maxRequests,

                    maxDepth:
                        CONFIG.maxDepth,

                    queue:
                        this.scheduler
                            .size()
                }
            );

            const workers = [];

            for (
                let i = 0;
                i < CONFIG.concurrency;
                i++
            ) {
                workers.push(
                    this.worker(i)
                );
            }

            await Promise.all(
                workers
            );

            this.stats.finishedAt =
                now();

            this.running =
                false;

            log(
                'Discovery complete',
                this.stats
            );

            this.report();
        }

        async worker(
            workerId
        ) {
            while (
                this.running &&
                this.stats.requests <
                    CONFIG.maxRequests
            ) {
                const candidate =
                    this.scheduler.claim();

                if (
                    !candidate
                ) {
                    const queueSize =
                        this.scheduler
                            .size();

                    const inFlight =
                        this.scheduler
                            .inFlight();

                    if (
                        queueSize === 0
                    ) {
                        break;
                    }

                    /*
                     * There may be queued retry candidates
                     * waiting for backoff.
                     *
                     * Wait rather than terminating the worker.
                     */
                    const delay =
                        this.scheduler
                            .nextReadyDelay();

                    if (
                        delay === null
                    ) {
                        break;
                    }

                    await sleep(
                        Math.min(
                            Math.max(
                                25,
                                delay
                            ),
                            250
                        )
                    );

                    /*
                     * If other workers are still processing
                     * candidates, loop again and see whether
                     * they have produced new work.
                     */
                    if (
                        inFlight > 0
                    ) {
                        continue;
                    }

                    continue;
                }

                this.stats.requests++;

                log(
                    `Worker ${workerId} claimed`,
                    candidate.target,
                    {
                        type:
                            candidate.type,

                        depth:
                            candidate.depth,

                        attempt:
                            candidate.attempts +
                            1
                    }
                );

                let finalized =
                    false;

                try {
                    const observation =
                        await this.acquisition
                            .acquire(
                                candidate
                            );

                    this.database
                        .addObservation(
                            observation
                        );

                    if (
                        observation.status !==
                        'acquired'
                    ) {
                        this.stats
                            .failures++;

                        const retryable =
                            candidate.attempts <=
                            CONFIG.maxRetries;

                        if (
                            retryable
                        ) {
                            this.stats
                                .retries++;

                            this.scheduler.fail(
                                candidate,
                                true
                            );

                            log(
                                `Worker ${workerId} retry scheduled`,
                                candidate.target,
                                candidate.nextAttemptAt
                            );
                        } else {
                            this.scheduler.fail(
                                candidate,
                                false
                            );
                        }

                        finalized =
                            true;

                        continue;
                    }

                    const result =
                        this.providers
                            .recognize(
                                candidate,
                                observation
                            );

                    if (!result) {
                        this.scheduler.complete(
                            candidate
                        );

                        finalized =
                            true;

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
                        this.addCandidate(
                            next
                        );
                    }

                    this.scheduler.complete(
                        candidate
                    );

                    finalized =
                        true;
                } catch (error) {
                    warn(
                        `Worker ${workerId} failed:`,
                        error
                    );

                    this.stats
                        .failures++;

                    const retryable =
                        candidate.attempts <=
                        CONFIG.maxRetries;

                    if (
                        retryable
                    ) {
                        this.stats
                            .retries++;

                        this.scheduler.fail(
                            candidate,
                            true
                        );
                    } else {
                        this.scheduler.fail(
                            candidate,
                            false
                        );
                    }

                    finalized =
                        true;
                } finally {
                    /*
                     * Defensive cleanup.
                     *
                     * This prevents a candidate from remaining
                     * permanently claimed if an unexpected path
                     * bypassed the normal finalization logic.
                     */
                    if (
                        !finalized &&
                        this.database
                            .claimed
                            .has(
                                candidate.key()
                            )
                    ) {
                        this.scheduler.fail(
                            candidate,
                            false
                        );
                    }
                }
            }
        }

        export() {
            const discoveries =
                [
                    ...this.database
                        .discoveries
                        .values()
                ];

            const edges =
                [];

            for (
                const discovery of
                discoveries
            ) {
                const parent =
                    discovery
                        .provenance
                        .parent;

                if (
                    parent
                ) {
                    edges.push({
                        from:
                            parent,

                        to:
                            discovery.id,

                        candidate:
                            discovery
                                .provenance
                                .candidateTarget,

                        mechanism:
                            discovery
                                .provenance
                                .mechanism
                    });
                }
            }

            return {
                version: 4,

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

                statistics:
                    this.stats,

                configuration: {
                    maxCandidates:
                        CONFIG.maxCandidates,

                    maxRequests:
                        CONFIG.maxRequests,

                    concurrency:
                        CONFIG.concurrency,

                    maxDepth:
                        CONFIG.maxDepth,

                    sameOriginOnly:
                        CONFIG.sameOriginOnly
                },

                queue: {
                    pending:
                        this.scheduler
                            .size(),

                    inFlight:
                        this.scheduler
                            .inFlight()
                },

                graph: {
                    nodes:
                        discoveries,

                    edges
                },

                discoveries
            };
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

                        candidate:
                            discovery
                                .provenance
                                .candidateTarget,

                        mechanism:
                            discovery
                                .provenance
                                .mechanism,

                        depth:
                            discovery
                                .provenance
                                .depth,

                        title:
                            discovery.data
                                ?.title ||
                            '',

                        createdAt:
                            discovery.createdAt
                    })
                )
            );

            console.log(
                'Queue:',
                this.scheduler
                    .size()
            );

            console.log(
                'In flight:',
                this.scheduler
                    .inFlight()
            );

            console.log(
                'Statistics:',
                this.stats
            );

            console.groupEnd();
        }

        clear() {
            this.database.clear();

            this.networkSeen.clear();

            this.resetStats();
        }
    }

    /*
     * =====================================================================
     * ENGINE INITIALIZATION
     * =====================================================================
     */

    const engine =
        new DiscoveryEngine();

    window.GenericDiscovery =
        engine;

    /*
     * =====================================================================
     * UI
     * =====================================================================
     */

    function createPanel() {
        const existing =
            document.getElementById(
                'generic-discovery-panel'
            );

        if (existing) {
            existing.remove();
        }

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
            background: rgba(20, 20, 20, .94);
            color: white;
            padding: 10px;
            border-radius: 8px;
            font: 12px monospace;
            line-height: 1.45;
            box-shadow: 0 3px 15px rgba(0, 0, 0, .4);
            min-width: 290px;
            max-width: 360px;
        `;

        panel.innerHTML = `
            <div style="margin-bottom:6px">
                <strong>Generic Discovery v0.4</strong>
            </div>

            <div style="
                margin-bottom:8px;
                opacity:.7;
            ">
                Web-resource discovery engine with
                network observation.
            </div>

            <div style="margin-bottom:8px">
                <button id="gd-start">
                    Scan
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

            <div
                id="gd-progress"
                style="
                    margin-top:6px;
                    opacity:.8;
                "
            >
                queue: 0 |
                in-flight: 0
            </div>

            <div
                id="gd-network"
                style="
                    margin-top:4px;
                    opacity:.8;
                "
            >
                network: 0 |
                performance: 0
            </div>
        `;

        (
            document.documentElement ||
            document.body
        )?.appendChild(
            panel
        );

        return panel;
    }

    function initializeUi() {
        const panel =
            createPanel();

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

        function updateUi() {
            if (
                !status ||
                !progress ||
                !network
            ) {
                return;
            }

            const queue =
                engine.scheduler
                    .size();

            const inFlight =
                engine.scheduler
                    .inFlight();

            const stats =
                engine.stats;

            if (
                engine.running
            ) {
                status.textContent =
                    'scanning...';
            }

            progress.textContent =
                `queue: ${queue} | ` +
                `in-flight: ${inFlight} | ` +
                `requests: ${stats.requests}/${CONFIG.maxRequests} | ` +
                `discoveries: ${stats.discoveries} | ` +
                `failures: ${stats.failures}`;

            network.textContent =
                `network: ${stats.networkCandidates} | ` +
                `performance: ${stats.performanceCandidates} | ` +
                `depth: ${CONFIG.maxDepth}`;
        }

        let uiTimer =
            null;

        function startUiTimer() {
            if (uiTimer) {
                return;
            }

            uiTimer =
                setInterval(
                    updateUi,
                    250
                );
        }

        function stopUiTimer() {
            if (!uiTimer) {
                return;
            }

            clearInterval(
                uiTimer
            );

            uiTimer =
                null;
        }

        panel.querySelector(
            '#gd-start'
        )?.addEventListener(
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

                startUiTimer();

                try {
                    await engine.run();

                    status.textContent =
                        `done — ` +
                        `${engine.stats.discoveries} discoveries`;
                } catch (error) {
                    warn(
                        'Engine run failed:',
                        error
                    );

                    status.textContent =
                        'error — see console';
                } finally {
                    stopUiTimer();

                    updateUi();
                }
            }
        );

        panel.querySelector(
            '#gd-clear'
        )?.addEventListener(
            'click',
            () => {
                if (
                    engine.running
                ) {
                    status.textContent =
                        'cannot clear while scanning';

                    return;
                }

                engine.clear();

                status.textContent =
                    'cleared';

                updateUi();
            }
        );

        panel.querySelector(
            '#gd-export'
        )?.addEventListener(
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

                    status.textContent =
                        'export failed — see console';
                }
            }
        );

        updateUi();
    }

    /*
     * document-start means the DOM may not exist yet.
     *
     * Wait until there is a usable document root for the panel.
     * The network bridge was installed earlier, so page activity
     * occurring after document-start can still be observed.
     */
    if (
        document.readyState ===
        'loading'
    ) {
        document.addEventListener(
            'DOMContentLoaded',
            initializeUi,
            {
                once: true
            }
        );
    } else {
        initializeUi();
    }

    log(
        'Generic Discovery Engine v0.4.0 loaded'
    );

})();
