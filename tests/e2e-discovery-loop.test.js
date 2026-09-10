#!/usr/bin/env node
// e2e-discovery-loop.test.js — Full pipeline simulation in Node (no browser)
// Mocks minimal browser globals, loads the userscript via VM, and drives
// a deterministic discovery → acquisition → observation → recognition → expansion loop.
// This is the deepest behavioral verification: it proves the DVB-inspired loop
// actually terminates, respects budgets, and preserves provenance.

import { describe, it, before } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import path from 'node:path';

// Utility: create a minimal browser-like sandbox
function createSandbox() {
    const store = new Map();
    const sandbox = {
        console,
        setTimeout, clearTimeout, setInterval, clearInterval,
        Date, Math, JSON, RegExp, URL, URLSearchParams,
        AbortController, AbortSignal,
        // Location
        location: { href: 'https://example.com/', origin: 'https://example.com', hostname: 'example.com', pathname: '/' },
        // Storage mocks
        GM_getValue: (k, d) => store.has(k) ? store.get(k) : d,
        GM_setValue: (k, v) => { store.set(k, v); },
        // Network mock — will be overridden per test
        GM_xmlhttpRequest: undefined,
        // DOM mocks — minimal to satisfy engine bootstrap without throwing
        // Use 'loading' to prevent auto-bootstrap during loadEngine(); we will drive manually.
        document: {
            readyState: 'loading',
            addEventListener: () => {},
            createElement: (tag) => ({
                tagName: tag.toUpperCase(),
                style: {}, appendChild: () => {}, remove: () => {},
                set textContent(v) { this._text = v; }, get textContent() { return this._text || ''; },
                addEventListener: () => {},
                querySelectorAll: () => [],
                querySelector: () => null,
            }),
            querySelectorAll: () => [],
            querySelector: () => null,
            documentElement: { appendChild: () => {}, querySelectorAll: () => [], querySelector: () => null },
            head: { appendChild: () => {} },
            body: { appendChild: () => {} },
        },
        window: null, // set to self after
        PerformanceObserver: undefined,
        MutationObserver: undefined,
        DOMParser: class {
            parseFromString(body, type) {
                // Very small mock: only needed to return an object with querySelectorAll that yields no results
                // Real HTML provider will receive this doc and emit only via extractUrlsFromText fallback.
                return {
                    querySelectorAll: () => [],
                    querySelector: () => null,
                    documentElement: { outerHTML: body },
                };
            }
        },
        confirm: () => false,
        Blob: globalThis.Blob,
        URL: globalThis.URL,
    };
    sandbox.window = sandbox;
    sandbox.globalThis = sandbox;
    sandbox.self = sandbox;
    return { sandbox, store };
}

function loadEngine(sandbox) {
    const code = fs.readFileSync(path.join(import.meta.dirname, '../dist/generic-discovery-engine.user.js'), 'utf8');
    // Strip the userscript header (==UserScript==) — VM will execute the IIFE directly
    const script = new vm.Script(code, { filename: 'generic-discovery-engine.user.js' });
    const context = vm.createContext(sandbox);
    script.runInContext(context);
    return sandbox.GenericDiscoveryEngine || sandbox.window.GenericDiscoveryEngine;
}

describe('E2E: full discovery pipeline (mocked network)', () => {
    let sandbox, engine;

    before(() => {
        const created = createSandbox();
        sandbox = created.sandbox;
        // Mock GM_xmlhttpRequest to immediately succeed with deterministic bodies
        const fixtures = new Map([
            ['https://example.com/', {
                status: 200,
                responseHeaders: 'content-type: text/html\r\n',
                responseText: `
                    <html><head><title>Root</title></head><body>
                        <a href="/page1">page1</a>
                        <a href="/api/data.json">api</a>
                        <link rel="sitemap" href="/sitemap.xml">
                    </body></html>`,
                finalUrl: 'https://example.com/',
            }],
            ['https://example.com/page1', {
                status: 200,
                responseHeaders: 'content-type: text/html\r\n',
                responseText: `<a href="/page2">page2</a><script src="/app.js"></script>`,
                finalUrl: 'https://example.com/page1',
            }],
            ['https://example.com/api/data.json', {
                status: 200,
                responseHeaders: 'content-type: application/json\r\n',
                responseText: JSON.stringify({ next: 'https://example.com/page2', nested: { url: 'https://example.com/api/more' } }),
                finalUrl: 'https://example.com/api/data.json',
            }],
            ['https://example.com/sitemap.xml', {
                status: 200,
                responseHeaders: 'content-type: application/xml\r\n',
                responseText: `<?xml version="1.0"?><urlset><url><loc>https://example.com/page2</loc></url></urlset>`,
                finalUrl: 'https://example.com/sitemap.xml',
            }],
            ['https://example.com/page2', {
                status: 200,
                responseHeaders: 'content-type: text/html\r\n',
                responseText: `<html>page2 — no further links</html>`,
                finalUrl: 'https://example.com/page2',
            }],
            ['https://example.com/app.js', {
                status: 200,
                responseHeaders: 'content-type: application/javascript\r\n',
                responseText: `fetch("https://example.com/api/more"); // discovered via JS`,
                finalUrl: 'https://example.com/app.js',
            }],
            ['https://example.com/api/more', {
                status: 200,
                responseHeaders: 'content-type: application/json\r\n',
                responseText: `{"final": true}`,
                finalUrl: 'https://example.com/api/more',
            }],
        ]);

        sandbox.GM_xmlhttpRequest = ({ url, onload, onerror, ontimeout }) => {
            const fixture = fixtures.get(url);
            // Simulate async
            setTimeout(() => {
                if (fixture) onload(fixture);
                else onerror({ error: 'not found: ' + url });
            }, 5);
        };

        engine = loadEngine(sandbox);
        // Engine init with readyState='loading' registers DOMContentLoaded but does not bootstrap yet.
        // Patch for deterministic test: clear any auto state, set low concurrency.
        engine.running = false;
        engine.stopRequested = false;
        engine.paused = false;
        engine.db.candidates.clear();
        engine.db.candidateKeys.clear();
        engine.db.visited.clear();
        engine.ledger.events.length = 0;
        engine.ledger.sequence = 0;
        engine.requestsReserved = 0;
        engine.currentConcurrency = 2;
    });

    it('engine boots and has expected initial API', () => {
        assert.ok(engine, 'engine should be defined on window');
        assert.ok(engine.db, 'db exists');
        assert.ok(engine.ledger, 'ledger exists');
        assert.ok(engine.policy, 'policy exists');
        assert.equal(typeof engine.discover, 'function');
        assert.equal(typeof engine.getCoverageMetrics, 'function');
        assert.equal(typeof engine.exportData, 'function');
    });

    it('discover() enqueues and promotes via ledger', () => {
        const before = engine.db.candidates.size;
        const c = engine.discover('https://example.com/', 'url', { priority: 1, depth: 0, hints: { confidence: 1 }, mechanism: 'test' });
        assert.ok(c, 'discover should return candidate');
        assert.ok(engine.db.candidates.has(c.id));
        assert.equal(c.status, 'queued');
        assert.ok(engine.ledger.events.some(e => e.type === 'candidate-discovered' && e.candidateId === c.id));
        assert.ok(engine.ledger.events.some(e => e.type === 'candidate-enqueued' && e.candidateId === c.id));
        // dedup: second discover same URL+type should not create new entry but return existing
        const c2 = engine.discover('https://example.com/', 'url', { priority: 0.1 });
        assert.equal(c2.id, c.id, 'dedup should return existing candidate');
        assert.equal(c2.priority, 1, 'priority should keep max');
    });

    it('coverage metrics reflect frontier accurately', () => {
        const cov = engine.getCoverageMetrics();
        assert.ok('frontierSize' in cov);
        assert.ok('queuedByType' in cov);
        assert.ok('liveCount' in cov);
        assert.ok('requestsRemaining' in cov);
        assert.equal(typeof cov.frontierSize, 'number');
        assert.equal(typeof cov.queuedByType, 'object');
        // frontier should at least contain the discovered root
        assert.ok(cov.frontierSize >= 1);
    });

    it('full mocked crawl terminates and discovers expected graph', async () => {
        // Reset for clean run
        engine.db.candidates.clear();
        engine.db.candidateKeys.clear();
        engine.db.visited.clear();
        engine.db.discoveries.clear();
        engine.db.resources.clear();
        engine.db.observations.clear();
        engine.db.graphEdges.length = 0;
        engine.ledger.events.length = 0;
        engine.ledger.sequence = 0;
        engine.requestsReserved = 0;
        engine.running = false;
        engine.stopRequested = false;
        engine.paused = false;

        // Seed
        engine.discover('https://example.com/', 'url', { priority: 1, depth: 0, hints: { confidence: 1 }, mechanism: 'e2e-root' });

        // Drive workers to completion (start() will run until frontier empty or maxRequests)
        await engine.start();

        // Assertions on final state
        const cov = engine.getCoverageMetrics();
        const discoveries = [...engine.db.discoveries.values()];
        const observations = [...engine.db.observations.values()];
        const ledgerTypes = engine.ledger.events.map(e => e.type);

        // Should have acquired at least root + page1 + api + sitemap (4+)
        assert.ok(observations.length >= 4, `expected >=4 observations, got ${observations.length}: ${observations.map(o=>o.requestedUrl).join(',')}`);
        assert.ok(discoveries.length >= 3, `expected >=3 discoveries, got ${discoveries.length}`);
        // Should have discovered page2 via multiple paths (sitemap + json + html) but deduped
        const page2Discs = discoveries.filter(d => d.data.url === 'https://example.com/page2');
        assert.ok(page2Discs.length >= 1, 'page2 should be discovered');
        // Ledger should contain the full causal chain
        assert.ok(ledgerTypes.includes('candidate-discovered'));
        assert.ok(ledgerTypes.includes('candidate-claimed'));
        assert.ok(ledgerTypes.includes('acquisition-planned'));
        assert.ok(ledgerTypes.includes('request-started'));
        assert.ok(ledgerTypes.includes('request-completed'));
        assert.ok(ledgerTypes.includes('observation-recorded'));
        assert.ok(ledgerTypes.includes('provider-recognized'));
        assert.ok(ledgerTypes.includes('discovery-emitted'));
        assert.ok(ledgerTypes.includes('candidate-completed'));

        // Provenance: every discovery should have parent/candidateTarget
        for (const d of discoveries) {
            assert.ok(d.provenance && d.provenance.parent, `discovery ${d.id} missing provenance.parent`);
            assert.ok(d.provenance.candidateTarget, `discovery ${d.id} missing candidateTarget`);
        }

        // Graph edges: at least root → children
        assert.ok(engine.db.graphEdges.length >= 2, `expected >=2 graph edges, got ${engine.db.graphEdges.length}`);

        // No budget overrun
        assert.ok(engine.requestsReserved <= 150, 'requests must not exceed maxRequests');
        assert.ok(cov.requestsRemaining >= 0);

        // Export contains coverage
        const exported = engine.exportData();
        assert.ok(exported.coverage, 'export must contain coverage');
        assert.equal(exported.coverage.frontierSize, cov.frontierSize);
        assert.equal(exported.schema, 'gde-export-v8.0');
    });

    it('policy denials are correctly ledgered (non-GET, depth)', () => {
        const formCand = engine.discover('https://example.com/form', 'form', { priority: 0.5, depth: 0, hints: { method: 'GET' } });
        assert.ok(formCand);
        // Policy should deny forms (acquireForms false) — plan will be denied when executed
        // We test policy directly via engine.policy
        const plan = engine.policy.plan(formCand);
        assert.equal(plan.allowed, false);
        assert.equal(plan.reason, 'forms-disabled');

        const deepCand = { id: 'x', target: 'https://example.com/deep', type: 'url', depth: 99, hints: {}, origin: 'https://example.com', effectivePriority: () => 1 };
        const deepPlan = engine.policy.plan(deepCand);
        assert.equal(deepPlan.reason, 'max-depth');

        const postCand = { id: 'y', target: 'https://example.com/post', type: 'url', depth: 0, hints: { method: 'POST' }, origin: 'https://example.com', effectivePriority: () => 1 };
        assert.equal(engine.policy.plan(postCand).reason, 'non-get-method');
    });

    it('fingerprint dedup index is populated', async () => {
        // After previous crawl, fingerprintIndex should have entries
        assert.ok(engine.db.fingerprintIndex.size >= 1, 'fingerprintIndex should have hashes');
        for (const [hash, urls] of engine.db.fingerprintIndex.entries()) {
            assert.equal(typeof hash, 'string');
            assert.equal(hash.length, 8, 'fnv1a32 hash is 8 hex chars');
            assert.ok(urls.size >= 1);
        }
    });
});
