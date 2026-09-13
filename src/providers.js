// src/providers.js — Provider + 9 providers + registry
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
                binary: () => new BinaryProvider(),
                text: () => new TextProvider()
            };
            this.order = ['html','json','xml','css','javascript','robots','headers','sitemapIndex','openapi','binary','text'];
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

