// ==UserScript==  
// @name Generic Discovery Engine  
// @namespace generic-discovery  
// @version 0.2.0  
// @description Generic web-resource discovery prototype inspired by the architecture of DVB blind scanning.  
// @match _://_/*  
// @grant GM_getValue  
// @grant GM_setValue  
// @grant GM_xmlhttpRequest  
// @connect *  
// ==/UserScript==

(() => {  
'use strict';

```
/*
 * =====================================================================
 * GENERIC DISCOVERY ENGINE
 * =====================================================================
 *
 * PURPOSE
 * -------
 * This is a browser-side discovery prototype inspired by the
 * architecture of DVB blind scanning:
 *
 *      candidate
 *          ↓
 *      observation
 *          ↓
 *      recognition
 *          ↓
 *      discovery
 *          ↓
 *      new candidates
 *          ↓
 *      scheduler
 *
 * IMPORTANT SCOPE
 * ---------------
 * This script is NOT a DVB/RF scanner.
 *
 * It does not:
 *   - access RF hardware
 *   - tune DVB frequencies
 *   - perform carrier synchronization
 *   - perform DVB FEC synchronization
 *   - demodulate DVB-S/S2/T/T2/C
 *
 * Instead, it applies the same discovery architecture to WEB
 * resources available to the browser:
 *
 *   URL → HTTP response → provider → discovered metadata → new URLs
 *
 * Supported response providers in this prototype:
 *
 *   - HTML
 *   - JSON
 *   - plain text
 *
 * The architecture is intentionally extensible.
 *
 * =====================================================================
 */

const CONFIG = {
    maxCandidates: 500,
    maxRequests: 100,

    // Number of simultaneous acquisitions.
    concurrency: 3,

    requestTimeout: 8000,

    sameOriginOnly: true,

    discoverLinks: true,
    discoverResources: true,

    persistState: true,

    debug: true
};

// =====================================================================
// Utility
// =====================================================================

const log = (...args) => {
    if (CONFIG.debug) {
        console.log('[Discovery]', ...args);
    }
};

const warn = (...args) => {
    console.warn('[Discovery]', ...args);
};

const now = () => Date.now();

function makeId(prefix) {
    return `${prefix}-${now()}-${Math.random()
        .toString(36)
        .slice(2, 9)}`;
}

function canonicalizeUrl(value) {
    try {
        const url = new URL(value, location.href);

        // Fragments don't identify a separately fetchable resource.
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
        return new URL(url).origin === location.origin;
    } catch {
        return false;
    }
}

// =====================================================================
// Candidate
// =====================================================================

class Candidate {
    constructor({
        target,
        type = 'url',
        origin = 'unknown',
        priority = 0.5,
        parent = null,
        hints = {}
    }) {
        this.id = makeId('candidate');

        this.target = target;
        this.type = type;

        // Why was this candidate created?
        // e.g. initial-dom, html-provider, json-provider
        this.origin = origin;

        // Candidate from which this one was derived.
        this.parent = parent;

        this.priority = priority;
        this.hints = hints;

        this.createdAt = now();

        this.attempts = 0;

        // queued → claimed → completed / failed
        this.status = 'queued';
    }

    key() {
        return `${this.type}:${this.target}`;
    }
}

// =====================================================================
// Observation
// =====================================================================

class Observation {
    constructor(candidate) {
        this.id = makeId('observation');

        this.candidateId = candidate.id;
        this.target = candidate.target;

        this.startedAt = now();
        this.completedAt = null;

        this.status = 'unknown';

        this.signalPresent = false;

        this.http = {
            status: null,
            contentType: null,
            contentLength: null
        };

        this.body = null;

        this.errors = [];
    }

    complete(status) {
        this.completedAt = now();
        this.status = status;
    }
}

// =====================================================================
// Discovery
// =====================================================================

class Discovery {
    constructor({
        candidate,
        observation,
        kind,
        confidence = 0.5,
        data = {}
    }) {
        this.id = makeId('discovery');

        this.candidateId = candidate.id;
        this.observationId = observation.id;

        this.kind = kind;
        this.confidence = confidence;

        this.data = data;

        this.provenance = {
            origin: candidate.origin,
            parent: candidate.parent
        };

        this.createdAt = now();
    }
}

// =====================================================================
// Knowledge Base
// =====================================================================

class KnowledgeBase {

    constructor() {
        this.candidates = new Map();

        this.observations = new Map();

        this.discoveries = new Map();

        /*
         * visited:
         *     candidates permanently completed.
         *
         * claimed:
         *     candidates currently owned by a worker.
         *
         * Keeping claimed separate from visited is important.
         */
        this.visited = new Set();
        this.claimed = new Set();

        this.load();
    }

    candidateKey(candidate) {
        return candidate.key();
    }

    addCandidate(candidate) {

        const key =
            this.candidateKey(candidate);

        if (!candidate.target) {
            return false;
        }

        if (this.visited.has(key)) {
            return false;
        }

        if (this.claimed.has(key)) {
            return false;
        }

        if (this.candidates.has(key)) {
            return false;
        }

        if (
            this.candidates.size >=
            CONFIG.maxCandidates
        ) {
            return false;
        }

        this.candidates.set(key, candidate);

        this.persist();

        return true;
    }

    /*
     * ---------------------------------------------------------------
     * ATOMIC CANDIDATE CLAIM
     * ---------------------------------------------------------------
     *
     * JavaScript executes this synchronous section without another
     * worker being able to interleave an await.
     *
     * A worker therefore:
     *
     *     1. asks for the next candidate
     *     2. candidate is immediately removed from the queue
     *     3. candidate is immediately placed in claimed
     *     4. only then does the worker perform async I/O
     *
     * This prevents two concurrent workers from claiming the same
     * candidate.
     */
    claimNextCandidate() {

        const candidates = [
            ...this.candidates.entries()
        ];

        if (!candidates.length) {
            return null;
        }

        candidates.sort((a, b) => {
            return (
                b[1].priority -
                a[1].priority
            );
        });

        for (const [key, candidate]
            of candidates) {

            if (
                this.visited.has(key) ||
                this.claimed.has(key)
            ) {
                continue;
            }

            /*
             * Claim is synchronous and happens before returning.
             */
            this.candidates.delete(key);

            this.claimed.add(key);

            candidate.status = 'claimed';
            candidate.claimedAt = now();

            this.persist();

            return candidate;
        }

        return null;
    }

    completeCandidate(candidate) {

        const key =
            this.candidateKey(candidate);

        this.claimed.delete(key);
        this.visited.add(key);

        candidate.status = 'completed';
        candidate.completedAt = now();

        this.persist();
    }

    failCandidate(candidate, retry = false) {

        const key =
            this.candidateKey(candidate);

        this.claimed.delete(key);

        if (retry) {
            candidate.status = 'queued';

            this.candidates.set(
                key,
                candidate
            );
        } else {
            this.visited.add(key);
            candidate.status = 'failed';
        }

        this.persist();
    }

    addObservation(observation) {
        this.observations.set(
            observation.id,
            observation
        );

        this.persist();
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

    serialize() {
        return {
            visited: [...this.visited],

            discoveries: [
                ...this.discoveries.values()
            ]
        };
    }

    persist() {

        if (!CONFIG.persistState) {
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
                    'discovery-state',
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

        if (!CONFIG.persistState) {
            return;
        }

        try {

            let raw = null;

            if (
                typeof GM_getValue ===
                'function'
            ) {
                raw = GM_getValue(
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
                typeof raw === 'string'
                    ? JSON.parse(raw)
                    : raw;

            for (
                const key of
                data.visited || []
            ) {
                this.visited.add(key);
            }

            for (
                const discovery of
                data.discoveries || []
            ) {
                this.discoveries.set(
                    discovery.id,
                    discovery
                );
            }

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

// =====================================================================
// Acquisition Adapter
// =====================================================================

class HttpAcquisitionAdapter {

    async acquire(candidate) {

        const observation =
            new Observation(candidate);

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
                response.body?.length || 0;

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

                    GM_xmlhttpRequest({

                        method: 'GET',

                        url,

                        timeout:
                            CONFIG.requestTimeout,

                        onload: response => {

                            const contentType =
                                response
                                    .responseHeaders
                                    ?.match(
                                        /content-type:\s*([^\r\n]+)/i
                                    )?.[1] ||
                                null;

                            resolve({
                                status:
                                    response.status,

                                contentType,

                                body:
                                    response.responseText
                            });
                        },

                        onerror: () =>
                            reject(
                                new Error(
                                    'request failed'
                                )
                            ),

                        ontimeout: () =>
                            reject(
                                new Error(
                                    'request timeout'
                                )
                            )
                    });

                    return;
                }

                fetch(url, {
                    credentials:
                        'same-origin',

                    signal:
                        AbortSignal.timeout(
                            CONFIG.requestTimeout
                        )
                })
                    .then(async response => ({
                        status:
                            response.status,

                        contentType:
                            response.headers
                                .get(
                                    'content-type'
                                ),

                        body:
                            await response.text()
                    }))
                    .then(resolve)
                    .catch(reject);
            }
        );
    }
}

// =====================================================================
// Provider Interface
// =====================================================================

/*
 * A provider answers:
 *
 *     "Can I recognize this response?"
 *
 * and, if yes:
 *
 *     "What did I discover, and what new candidates did I learn?"
 *
 * Providers are intentionally independent of acquisition.
 */

class ResponseProvider {

    matches(/* observation */) {
        return false;
    }

    recognize(/* candidate, observation */) {
        return null;
    }

    candidates(/* discovery */) {
        return [];
    }
}

// =====================================================================
// HTML Provider
// =====================================================================

class HtmlProvider extends ResponseProvider {

    matches(observation) {

        const type =
            observation.http.contentType ||
            '';

        const body =
            observation.body || '';

        return (
            type.includes('text/html') ||
            /<html[\s>]/i.test(body) ||
            /<body[\s>]/i.test(body)
        );
    }

    recognize(candidate, observation) {

        if (!this.matches(observation)) {
            return null;
        }

        const body =
            observation.body || '';

        const doc =
            new DOMParser()
                .parseFromString(
                    body,
                    'text/html'
                );

        const title =
            doc.querySelector('title')
                ?.textContent
                ?.trim() || '';

        const links = [
            ...doc.querySelectorAll(
                'a[href]'
            )
        ]
            .map(element =>
                canonicalizeUrl(
                    element.href
                )
            )
            .filter(Boolean)
            .filter(isAllowedUrl);

        const resources = [
            ...doc.querySelectorAll(
                'script[src],' +
                'link[href],' +
                'img[src]'
            )
        ]
            .map(element =>
                canonicalizeUrl(
                    element.src ||
                    element.href
                )
            )
            .filter(Boolean)
            .filter(isAllowedUrl);

        return new Discovery({
            candidate,
            observation,

            kind: 'html-document',

            confidence: 0.95,

            data: {
                url: candidate.target,
                title,
                links,
                resources
            }
        });
    }

    candidates(discovery) {

        const result = [];

        if (CONFIG.discoverLinks) {

            for (
                const url of
                discovery.data.links || []
            ) {

                result.push(
                    new Candidate({
                        target: url,
                        type: 'url',
                        origin:
                            `html:${discovery.id}`,
                        parent:
                            discovery.id,
                        priority: 0.8
                    })
                );
            }
        }

        if (CONFIG.discoverResources) {

            for (
                const url of
                discovery.data.resources || []
            ) {

                result.push(
                    new Candidate({
                        target: url,
                        type: 'resource',
                        origin:
                            `html:${discovery.id}`,
                        parent:
                            discovery.id,
                        priority: 0.5
                    })
                );
            }
        }

        return result;
    }
}

// =====================================================================
// JSON Provider
// =====================================================================

class JsonProvider extends ResponseProvider {

    matches(observation) {

        const type =
            observation.http.contentType ||
            '';

        return (
            type.includes(
                'application/json'
            ) ||
            type.includes(
                '+json'
            )
        );
    }

    recognize(candidate, observation) {

        if (!this.matches(observation)) {
            return null;
        }

        let value;

        try {

            value =
                JSON.parse(
                    observation.body
                );

        } catch {
            return null;
        }

        const urls =
            this.extractUrls(value);

        return new Discovery({
            candidate,
            observation,

            kind: 'json-document',

            confidence: 0.95,

            data: {
                url: candidate.target,
                value,
                urls
            }
        });
    }

    extractUrls(value) {

        const result = [];

        const visit = value => {

            if (typeof value === 'string') {

                const url =
                    canonicalizeUrl(
                        value
                    );

                if (
                    url &&
                    isAllowedUrl(url)
                ) {
                    result.push(url);
                }

                return;
            }

            if (!value || typeof value !== 'object') {
                return;
            }

            for (
                const child of
                Object.values(value)
            ) {
                visit(child);
            }
        };

        visit(value);

        return [
            ...new Set(result)
        ];
    }

    candidates(discovery) {

        return (
            discovery.data.urls || []
        ).map(url =>
            new Candidate({
                target: url,
                type: 'url',
                origin:
                    `json:${discovery.id}`,
                parent:
                    discovery.id,
                priority: 0.7
            })
        );
    }
}

// =====================================================================
// Plain Text Provider
// =====================================================================

class TextProvider extends ResponseProvider {

    matches(observation) {

        const type =
            observation.http.contentType ||
            '';

        return (
            type.startsWith('text/') ||
            type === ''
        );
    }

    recognize(candidate, observation) {

        if (!this.matches(observation)) {
            return null;
        }

        const text =
            observation.body || '';

        /*
         * Find absolute HTTP(S) URLs in text.
         */
        const matches =
            text.match(
                /https?:\/\/[^\s"'<>]+/gi
            ) || [];

        const urls =
            matches
                .map(canonicalizeUrl)
                .filter(Boolean)
                .filter(isAllowedUrl);

        return new Discovery({
            candidate,
            observation,

            kind: 'text-document',

            confidence: 0.75,

            data: {
                url: candidate.target,
                textLength: text.length,
                urls: [
                    ...new Set(urls)
                ]
            }
        });
    }

    candidates(discovery) {

        return (
            discovery.data.urls || []
        ).map(url =>
            new Candidate({
                target: url,
                type: 'url',
                origin:
                    `text:${discovery.id}`,
                parent:
                    discovery.id,
                priority: 0.4
            })
        );
    }
}

// =====================================================================
// Provider Registry
// =====================================================================

class ProviderRegistry {

    constructor() {

        this.providers = [
            new JsonProvider(),
            new HtmlProvider(),
            new TextProvider()
        ];
    }

    recognize(candidate, observation) {

        for (
            const provider of
            this.providers
        ) {

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

            if (discovery) {

                return {
                    provider,
                    discovery
                };
            }
        }

        return null;
    }
}

// =====================================================================
// Scheduler
// =====================================================================

class Scheduler {

    constructor(database) {
        this.database = database;
    }

    add(candidate) {
        return this.database
            .addCandidate(candidate);
    }

    /*
     * Important:
     *
     * Do NOT implement this as:
     *
     *     candidate = next()
     *     await something
     *     markVisited(candidate)
     *
     * The candidate must be claimed synchronously before the
     * worker performs any asynchronous operation.
     */
    claim() {
        return this.database
            .claimNextCandidate();
    }

    complete(candidate) {
        this.database
            .completeCandidate(candidate);
    }

    fail(candidate, retry = false) {
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
}

// =====================================================================
// Discovery Engine
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

        this.running = false;

        this.stats = {
            startedAt: null,
            requests: 0,
            discoveries: 0,
            failures: 0,
            candidatesCreated: 0
        };
    }

    seed() {

        const current =
            canonicalizeUrl(
                location.href
            );

        if (current) {

            this.addCandidate(
                new Candidate({
                    target: current,
                    type: 'url',
                    origin: 'initial-page',
                    priority: 1.0
                })
            );
        }

        /*
         * Treat the already-loaded DOM as an initial observation.
         * This avoids requiring a network request just to discover
         * links already present on the page.
         */
        const initialLinks = [
            ...document.querySelectorAll(
                'a[href]'
            )
        ];

        for (
            const element of initialLinks
        ) {

            const url =
                canonicalizeUrl(
                    element.href
                );

            if (
                url &&
                isAllowedUrl(url)
            ) {

                this.addCandidate(
                    new Candidate({
                        target: url,
                        type: 'url',
                        origin: 'initial-dom',
                        priority: 0.7
                    })
                );
            }
        }
    }

    addCandidate(candidate) {

        const added =
            this.scheduler.add(
                candidate
            );

        if (added) {
            this.stats.candidatesCreated++;
        }

        return added;
    }

    async run() {

        if (this.running) {
            return;
        }

        this.running = true;

        this.stats.startedAt = now();

        log(
            'Starting discovery',
            {
                concurrency:
                    CONFIG.concurrency
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

        await Promise.all(workers);

        this.running = false;

        log(
            'Discovery complete',
            this.stats
        );
    }

    async worker(workerId) {

        while (
            this.running &&
            this.stats.requests <
                CONFIG.maxRequests
        ) {

            /*
             * CLAIM FIRST.
             *
             * This operation is synchronous.
             * No await occurs before ownership is established.
             */
            const candidate =
                this.scheduler.claim();

            if (!candidate) {
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
                        .acquire(candidate);

                this.database
                    .addObservation(
                        observation
                    );

                if (
                    observation.status !==
                    'acquired'
                ) {

                    this.stats.failures++;

                    this.scheduler.fail(
                        candidate,
                        false
                    );

                    continue;
                }

                const result =
                    this.providers.recognize(
                        candidate,
                        observation
                    );

                if (!result) {

                    this.scheduler.complete(
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

                this.stats.discoveries++;

                log(
                    `Worker ${workerId} discovered`,
                    discovery.kind,
                    candidate.target
                );

                /*
                 * A provider can expand the search space.
                 */
                const newCandidates =
                    provider.candidates(
                        discovery
                    );

                for (
                    const next
                    of newCandidates
                ) {
                    this.addCandidate(next);
                }

                this.scheduler.complete(
                    candidate
                );

            } catch (error) {

                warn(
                    `Worker ${workerId} failed:`,
                    error
                );

                this.stats.failures++;

                this.scheduler.fail(
                    candidate,
                    false
                );
            }
        }
    }

    export() {

        return {
            version: 2,

            scope: {
                type:
                    'web-resource-discovery',

                inspiredBy:
                    'DVB blind-scan architecture',

                rfScanning:
                    false
            },

            timestamp:
                new Date().toISOString(),

            page:
                location.href,

            statistics:
                this.stats,

            discoveries: [
                ...this.database
                    .discoveries
                    .values()
            ]
        };
    }

    report() {

        const discoveries = [
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

                    url:
                        discovery.data.url,

                    title:
                        discovery.data.title ||
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
            this.database.claimedSize()
        );

        console.log(
            'Statistics:',
            this.stats
        );

        console.groupEnd();
    }

    clear() {
        this.database.clear();
    }
}

// =====================================================================
// UI
// =====================================================================

const engine =
    new DiscoveryEngine();

/*
 * Public API for experimentation.
 */
window.GenericDiscovery = engine;

const panel =
    document.createElement('div');

panel.style.cssText = `
    position: fixed;
    right: 12px;
    bottom: 12px;
    z-index: 2147483647;
    background: rgba(20,20,20,.94);
    color: white;
    padding: 10px;
    border-radius: 8px;
    font: 12px monospace;
    box-shadow: 0 3px 15px rgba(0,0,0,.4);
`;

panel.innerHTML = `
    <div style="margin-bottom:6px">
        <strong>Generic Discovery</strong>
    </div>

    <div style="
        margin-bottom:8px;
        opacity:.7;
        max-width:260px;
    ">
        Web-resource prototype inspired by
        DVB blind-scan architecture.
    </div>

    <button id="gd-start">
        Scan
    </button>

    <button id="gd-clear">
        Clear
    </button>

    <button id="gd-export">
        Export
    </button>

    <div id="gd-status"
         style="margin-top:6px">
        idle
    </div>
`;

document.documentElement.appendChild(
    panel
);

const status =
    panel.querySelector(
        '#gd-status'
    );

panel.querySelector(
    '#gd-start'
).addEventListener(
    'click',
    async () => {

        if (engine.running) {
            return;
        }

        status.textContent =
            'scanning...';

        engine.seed();

        await engine.run();

        engine.report();

        status.textContent =
            `done — ` +
            `${engine.stats.discoveries} discoveries`;
    }
);

panel.querySelector(
    '#gd-clear'
).addEventListener(
    'click',
    () => {

        engine.clear();

        status.textContent =
            'cleared';
    }
);

panel.querySelector(
    '#gd-export'
).addEventListener(
    'click',
    () => {

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

        const a =
            document.createElement('a');

        a.href = url;

        a.download =
            `discovery-${Date.now()}.json`;

        a.click();

        URL.revokeObjectURL(url);
    }
);
```

})();
