// src/utils.js — helpers
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

