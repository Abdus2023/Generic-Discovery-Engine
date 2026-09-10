/*
 * ============================================================================
 * Generic Discovery Engine — headless behavioural harness
 * ============================================================================
 *
 * Executes the SHIPPED userscript artifact (prototype/generic-discovery-engine.user.js)
 * inside a minimal browser shim and observes:
 *
 *   - candidate claiming (single-owner invariant)
 *   - per-URL acquisition guard (duplicate suppression)
 *   - retry / backoff behaviour
 *   - termination / quiescence behaviour
 *
 * The artifact is NOT modified. Every observation is produced by wrapping the
 * shipped methods at runtime (monkey-patching) or by counting shim network calls.
 *
 * Usage:
 *   node tools/simulate.mjs [--unsafe-control]
 *
 * Findings produced by this harness are recorded in
 * docs/prototype/limitations.md. A "FAIL" line below is a DETECTED DEFECT of
 * the shipped artifact, not a failure of the harness.
 *
 * --unsafe-control replaces the shipped claim function with a scheduler that has
 * no ownership transition ("inspect -> await -> acquire") and disables the
 * per-URL guard. It exists to prove the harness can DETECT a violation; it is
 * not a description of the shipped design.
 */

import fs from 'node:fs';
import vm from 'node:vm';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ARTIFACT = process.argv[2] && !process.argv[2].startsWith('--')
  ? process.argv[2]
  : path.join(HERE, '..', 'prototype', 'generic-discovery-engine.user.js');
const UNSAFE = process.argv.includes('--unsafe-control');

/* -------------------------------------------------------------------------- */
/* 1. Browser shim                                                            */
/* -------------------------------------------------------------------------- */

function makeEventTarget(target = {}) {
  const listeners = new Map();
  target.addEventListener = (type, fn) => {
    if (!listeners.has(type)) listeners.set(type, []);
    listeners.get(type).push(fn);
  };
  target.removeEventListener = () => {};
  target.dispatchEvent = (ev) => { for (const fn of listeners.get(ev.type) || []) fn(ev); };
  return target;
}

function makeElement(tag = 'div') {
  const el = makeEventTarget({
    tagName: String(tag).toUpperCase(),
    style: { cssText: '', marginBottom: '', display: '', gap: '' },
    textContent: '',
    innerHTML: '',
    children: []
  });
  el.appendChild = (child) => { el.children.push(child); return child; };
  el.querySelector = () => null;
  el.querySelectorAll = () => [];
  return el;
}

const storage = new Map();

globalThis.window = makeEventTarget({ fetch: undefined, XMLHttpRequest: undefined });
globalThis.document = makeEventTarget({
  readyState: 'loading',   // bootstrap deferred until the harness fires DOMContentLoaded
  head: makeElement('head'),
  body: makeElement('body'),
  documentElement: makeElement('html'),
  createElement: (tag) => makeElement(tag),
  querySelectorAll: () => []
});
globalThis.location = {
  href: 'https://example.test/index',
  origin: 'https://example.test',
  reload: () => {}
};
globalThis.MutationObserver = class { observe() {} disconnect() {} };
globalThis.PerformanceObserver = undefined;
globalThis.confirm = () => false;
globalThis.GM_getValue = (key, fallback) => (storage.has(key) ? storage.get(key) : fallback);
globalThis.GM_setValue = (key, value) => { storage.set(key, value); };
globalThis.DOMParser = class {
  // The HTML recognition path needs a real DOM parser; this stub lets the
  // engine run while intentionally producing no HTML discoveries.
  parseFromString() { return { querySelectorAll: () => [], querySelector: () => null }; }
};

/* -------------------------------------------------------------------------- */
/* 2. Instrumented network                                                    */
/* -------------------------------------------------------------------------- */

const DELAY_MS = 40;          // keeps several workers genuinely in flight
const FANOUT = 24;            // URLs emitted by the seed response

const log = {
  requests: [],
  perUrl: new Map(),
  claims: [],
  inFlight: new Map(),
  maxInFlight: new Map(),
  anomalies: []
};

function seedBody() {
  const links = [];
  for (let i = 1; i <= FANOUT; i++) links.push(`https://example.test/p${i}`);
  links.push('https://example.test/shared');
  links.push('https://example.test/flaky');
  return JSON.stringify({ links });
}

function pageBody(url) {
  const n = url.match(/p(\d+)$/);
  if (!n) return JSON.stringify({ ok: true });
  const i = Number(n[1]);
  return JSON.stringify({
    next: `https://example.test/p${(i % FANOUT) + 1}`,
    shared: 'https://example.test/shared'
  });
}

globalThis.GM_xmlhttpRequest = function ({ url, method, onload }) {
  log.requests.push({ url, method, at: Date.now() });
  log.perUrl.set(url, (log.perUrl.get(url) || 0) + 1);

  setTimeout(() => {
    if (url.includes('/flaky')) {
      onload({ status: 500, responseText: 'server error',
               responseHeaders: 'content-type: text/plain', finalUrl: url });
      return;
    }
    const body = url.endsWith('/index') ? seedBody() : pageBody(url);
    onload({ status: 200, responseText: body,
             responseHeaders: 'content-type: application/json', finalUrl: url });
  }, DELAY_MS);

  return { abort() {} };
};

/* -------------------------------------------------------------------------- */
/* 3. Load the artifact                                                       */
/* -------------------------------------------------------------------------- */

const code = fs.readFileSync(ARTIFACT, 'utf8');
vm.runInThisContext(code, { filename: path.basename(ARTIFACT) });

const engine = globalThis.window.GenericDiscoveryEngine;
if (!engine) { console.error('FAIL: engine object not exposed by artifact'); process.exit(2); }

/*
 * Pre-populate the frontier before the scan starts.
 *
 * The shipped engine starts its worker pool during bootstrap, when the only
 * known candidate is the current page. In a real browser the DOM/network
 * observers have usually already proposed links by the time a scan is started,
 * so this setup mirrors a realistic starting frontier and is what makes
 * concurrent execution observable at all.
 */
const PRE_SEED = [];
for (let i = 1; i <= FANOUT; i++) PRE_SEED.push(`https://example.test/p${i}`);
PRE_SEED.push('https://example.test/shared', 'https://example.test/flaky');
for (const target of PRE_SEED) engine.discover(target, 'url', { priority: 0.5, depth: 1 });

/* -------------------------------------------------------------------------- */
/* 4. Instrument the shipped scheduler                                        */
/* -------------------------------------------------------------------------- */

const shippedClaim = engine.db.claimNextCandidate.bind(engine.db);

engine.db.claimNextCandidate = UNSAFE
  ? function () {
      // NEGATIVE CONTROL — no ownership transition at all.
      const eligible = [...this.candidates.values()].filter(
        c => ['queued', 'failed', 'claimed', 'acquiring'].includes(c.status)
      );
      eligible.sort((a, b) => b.effectivePriority() - a.effectivePriority());
      return eligible[0] || null;
    }
  : function () {
      const candidate = shippedClaim();
      if (candidate) {
        log.claims.push({ id: candidate.id, target: candidate.target });
        if (['claimed', 'acquiring', 'planned'].includes(candidate.__priorStatus)) {
          log.anomalies.push(`DOUBLE_CLAIM ${candidate.target}`);
        }
      }
      return candidate;
    };

// observe the pre-claim status of every candidate without touching shipped code
const seen = new Set();
setInterval(() => {
  for (const c of engine.db.candidates.values()) {
    if (!seen.has(c.id)) { seen.add(c.id); c.__priorStatusFirst = c.status; }
  }
}, 5).unref?.();

let globalConcurrent = 0;
let maxGlobalConcurrent = 0;

const shippedExecute = engine.executePlan.bind(engine);
engine.executePlan = async function (plan) {
  if (UNSAFE) engine.db.shouldAcquireResource = () => true;

  globalConcurrent++;
  maxGlobalConcurrent = Math.max(maxGlobalConcurrent, globalConcurrent);

  const id = plan.candidateId;
  const owners = (log.inFlight.get(id) || 0) + 1;
  log.inFlight.set(id, owners);
  log.maxInFlight.set(id, Math.max(log.maxInFlight.get(id) || 0, owners));
  if (owners > 1) log.anomalies.push(`CONCURRENT_OWNER ${plan.target} owners=${owners} ${UNSAFE ? '(control)' : ''}`);

  try {
    return await shippedExecute(plan);
  } finally {
    log.inFlight.set(id, (log.inFlight.get(id) || 1) - 1);
    globalConcurrent--;
  }
};

/* -------------------------------------------------------------------------- */
/* 5. Run to quiescence                                                       */
/* -------------------------------------------------------------------------- */

// worker-pool observation
let peakActiveWorkers = 0;
const workerSampler = setInterval(() => {
  peakActiveWorkers = Math.max(peakActiveWorkers, engine.activeWorkers);
}, 2);

const startedAt = Date.now();
document.dispatchEvent({ type: 'DOMContentLoaded' });   // bootstrap -> start()
await engine.start();                                   // no-op if already running

async function waitQuiet(budgetMs = 60000) {
  const deadline = Date.now() + budgetMs;
  let quietSince = null;
  while (Date.now() < deadline) {
    if (engine.activeWorkers === 0) {
      quietSince ??= Date.now();
      if (Date.now() - quietSince > 400) return true;
    } else quietSince = null;
    await new Promise(r => setTimeout(r, 20));
  }
  return false;
}

const quiesced = await waitQuiet();
clearInterval(workerSampler);
const elapsedMs = Date.now() - startedAt;

const statuses = {};
for (const c of engine.db.candidates.values()) statuses[c.status] = (statuses[c.status] || 0) + 1;

const repeated = [...log.perUrl.entries()].filter(([url, n]) => n > 1 && !url.includes('/flaky'));
const stuck = [...engine.db.candidates.values()]
  .filter(c => c.status === 'queued' || c.status === 'failed')
  .map(c => ({ target: c.target, status: c.status, attempts: c.attempts,
               backoffMs: Math.max(0, (c.nextAttemptAt || 0) - Date.now()) }));

const results = {
  mode: UNSAFE ? 'UNSAFE CONTROL (not shipped behaviour)' : 'SHIPPED ARTIFACT',
  artifact: path.relative(process.cwd(), ARTIFACT),
  quiesced,
  elapsedMs,
  workersAtEnd: engine.activeWorkers,
  peakActiveWorkers,
  configuredConcurrency: engine.currentConcurrency,
  engineRunningFlagAtEnd: engine.running,
  requests: log.requests.length,
  uniqueUrls: log.perUrl.size,
  candidates: engine.db.candidates.size,
  statuses,
  stats: engine.db.stats,
  discoveries: engine.db.discoveries.size,
  resources: engine.db.resources.size,
  ledgerEvents: engine.ledger.events.length,
  maxConcurrentOwnersPerCandidate: Math.max(0, ...log.maxInFlight.values()),
  maxConcurrentExecutionsOverall: maxGlobalConcurrent,
  duplicateAcquisitionsOfSameUrl: repeated.map(([url, n]) => `${url} x${n}`),
  flakyUrlRequests: log.perUrl.get('https://example.test/flaky') || 0,
  pendingWorkAtQuiescence: stuck,
  anomalies: log.anomalies.slice(0, 10)
};

const checks = [
  ['single owner per candidate',
   results.maxConcurrentOwnersPerCandidate === 1,
   `${results.maxConcurrentOwnersPerCandidate} concurrent owner(s) observed for one candidate`],
  ['no duplicate acquisition of a successful URL',
   repeated.length === 0,
   `${repeated.length} URL(s) fetched more than once`],
  ['scan reaches quiescence',
   results.quiesced === true,
   'workers returned to zero'],
  ['no work left claimable at quiescence',
   results.pendingWorkAtQuiescence.length === 0,
   `${results.pendingWorkAtQuiescence.length} candidate(s) still pending`]
];

console.log(JSON.stringify(results, null, 2));
console.log('\nchecks:');
for (const [name, ok, note] of checks) console.log(`  ${ok ? 'PASS' : 'FAIL'}  ${name.padEnd(52)} ${note}`);
const failed = checks.filter(([, ok]) => !ok).length;
console.log(UNSAFE
  ? `\nnegative control: ${failed} check(s) failing — the harness can detect violations.`
  : `\n${failed === 0 ? 'all checks passed against the shipped artifact' : failed + ' check(s) failed'}`);
