#!/usr/bin/env node
/*
 * ============================================================================
 * Generic Discovery Engine — invariant checks
 * ============================================================================
 *
 * Focused verification procedures that execute the shipped artifact inside a
 * fresh browser shim per case. Unlike tools/simulate.mjs (one long scenario),
 * each check here isolates one property:
 *
 *   1. candidate uniqueness            (same target, same type → one candidate)
 *   2. candidate type disambiguation   (same target, different type → two)
 *   3. provider selection              (content type → expected providers)
 *   4. provenance chain reconstructible (seed → candidate → observation →
 *                                        discovery → child candidate)
 *   5. persistence round-trip          (serialize → fresh context → restore)
 *
 * Usage:
 *   node tools/checks.mjs
 *
 * Exit code 0 = all checks ran and none FAILED in a way that indicates
 * documentation drift. Known prototype defects are reported as [DEFECT].
 */

import fs from 'node:fs';
import vm from 'node:vm';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const ARTIFACT = path.join(ROOT, 'prototype', 'generic-discovery-engine.user.js');
const SOURCE = fs.readFileSync(ARTIFACT, 'utf8');

const results = [];
const pass = (name, note = '') => results.push({ level: 'PASS', name, note });
const fail = (name, note = '') => results.push({ level: 'FAIL', name, note });
const defect = (name, note = '') => results.push({ level: 'DEFECT', name, note });
const info = (name, note = '') => results.push({ level: 'INFO', name, note });

/* -------------------------------------------------------------------------- */
/* Fresh execution context per case                                           */
/* -------------------------------------------------------------------------- */

function makeContext({ storage = new Map(), routes = {}, deferBootstrap = false, delay = 0 } = {}) {
  const listeners = new Map();
  const eventTarget = (target = {}) => {
    target.addEventListener = (type, fn) => {
      if (!listeners.has(type)) listeners.set(type, []);
      listeners.get(type).push(fn);
    };
    target.removeEventListener = () => {};
    target.dispatchEvent = (ev) => { for (const fn of listeners.get(ev.type) || []) fn(ev); };
    return target;
  };

  const element = (tag = 'div') => {
    const el = eventTarget({
      tagName: String(tag).toUpperCase(),
      style: {}, textContent: '', innerHTML: '', children: []
    });
    el.appendChild = (c) => { el.children.push(c); return c; };
    el.querySelector = () => null;
    el.querySelectorAll = () => [];
    return el;
  };

  const requests = [];

  const sandbox = {
    console: { log() {}, warn() {}, error() {} },
    setTimeout, clearTimeout, setInterval, clearInterval,
    URL, URLSearchParams, TextEncoder, TextDecoder,
    Blob: class { constructor(parts) { this.parts = parts; } },
    confirm: () => false,
    MutationObserver: class { observe() {} disconnect() {} },
    PerformanceObserver: undefined,
    GM_getValue: (k, d) => (storage.has(k) ? storage.get(k) : d),
    GM_setValue: (k, v) => { storage.set(k, v); },
    GM_xmlhttpRequest: ({ url, method, onload }) => {
      requests.push({ url, method });
      setTimeout(() => {
        const route = routes[url];
        if (!route) {
          onload({ status: 404, responseText: 'not found',
                   responseHeaders: 'content-type: text/plain', finalUrl: url });
          return;
        }
        onload({ status: route.status ?? 200, responseText: route.body,
                 responseHeaders: `content-type: ${route.contentType}`,
                 finalUrl: route.finalUrl || url });
      }, delay);
      return { abort() {} };
    },
    DOMParser: class {
      parseFromString() { return { querySelectorAll: () => [], querySelector: () => null }; }
    }
  };

  sandbox.window = eventTarget({ fetch: undefined, XMLHttpRequest: undefined });
  sandbox.document = eventTarget({
    readyState: deferBootstrap ? 'loading' : 'complete',
    head: element('head'), body: element('body'), documentElement: element('html'),
    createElement: element, querySelectorAll: () => []
  });
  sandbox.location = { href: 'https://check.test/index', origin: 'https://check.test', reload() {} };

  const context = vm.createContext(sandbox);
  vm.runInContext(SOURCE, context, { filename: 'generic-discovery-engine.user.js' });

  const engine = sandbox.window.GenericDiscoveryEngine;
  return { sandbox, engine, requests, storage, fireBootstrap: () => sandbox.document.dispatchEvent({ type: 'DOMContentLoaded' }) };
}

async function settle(engine, budgetMs = 20000) {
  const deadline = Date.now() + budgetMs;
  let quietSince = null;
  while (Date.now() < deadline) {
    if (engine.activeWorkers === 0) {
      quietSince ??= Date.now();
      if (Date.now() - quietSince > 300) return true;
    } else quietSince = null;
    await new Promise(r => setTimeout(r, 20));
  }
  return false;
}

/* -------------------------------------------------------------------------- */
/* 1 + 2. Candidate identity                                                  */
/* -------------------------------------------------------------------------- */

{
  const ctx = makeContext({ deferBootstrap: true });
  const url = 'https://check.test/dup';

  const first = ctx.engine.discover(url, 'url', { priority: 0.5, depth: 1 });
  const countAfterFirst = ctx.engine.db.candidates.size;
  const second = ctx.engine.discover(url, 'url', { priority: 0.9, depth: 1 });
  const countAfterSecond = ctx.engine.db.candidates.size;

  if (first && second && first.id === second.id && countAfterSecond === countAfterFirst) {
    pass('duplicate candidate insertion yields one logical candidate',
      `id=${first.id.slice(0, 18)}…, count=${countAfterSecond}, merged priority=${second.priority}`);
  } else {
    fail('duplicate candidate insertion yields one logical candidate',
      `first=${first?.id} second=${second?.id} count ${countAfterFirst}→${countAfterSecond}`);
  }

  const otherType = ctx.engine.discover(url, 'api', { priority: 0.5, depth: 1 });
  if (otherType && otherType.id !== first.id && ctx.engine.db.candidates.size === countAfterSecond + 1) {
    info('same target with a different type is a distinct candidate',
      `identityKey = type:target → url vs api`);
  } else {
    fail('same target with a different type is a distinct candidate');
  }
}

/* -------------------------------------------------------------------------- */
/* 3. Provider selection (exact sets)                                         */
/* -------------------------------------------------------------------------- */

{
  const ctx = makeContext({ deferBootstrap: true });

  /*
   * Expectations derived from the shipped matching rules:
   *   html       text/html, application/xhtml+xml, or body starting with <!doctype html / <html
   *   json       application/json, *+json, or body starting with [ or {
   *   xml        application/xml, text/xml, *+xml, or body starting with <?xml
   *   css        text/css (content type only)
   *   javascript  application|text/javascript, application/x-javascript, *ecmascript
   *   text       text/* or an empty content type   <-- NOT a universal fallback
   *   binary     image/*, audio/*, video/*, pdf, zip, octet-stream
   */
  const cases = [
    ['application/json', '{"a":"https://x.test/1"}', ['json']],
    ['text/html', '<a href="/x">x</a>', ['html', 'text']],
    ['text/css', 'body{background:url(/x.png)}', ['css', 'text']],
    ['text/xml', '<sitemap><loc>https://x.test/1</loc></sitemap>', ['xml', 'text']],
    ['application/javascript', 'const u="https://x.test/1";', ['javascript']],
    ['text/plain', 'see https://x.test/1', ['text']],
    ['application/octet-stream', 'binary', ['binary']],
    ['application/xml', '<sitemap><loc>https://x.test/1</loc></sitemap>', ['xml']],
    ['', 'no content type header', ['text']],
    // body sniffing fires even when the content type is wrong
    ['text/plain', '<!doctype html><html><a href="/x">x</a></html>', ['html', 'text']],
    ['text/plain', '{"url":"https://x.test/1"}', ['json', 'text']]
  ];

  const mismatches = [];
  for (const [contentType, body, expected] of cases) {
    const observation = { http: { contentType }, body, status: 'success' };
    const matched = ctx.engine.providers.matching(observation)
      .map(p => p.name).sort();
    const want = [...expected].sort();
    const ok = matched.length === want.length && matched.every((n, i) => n === want[i]);
    if (!ok) mismatches.push(`${contentType || '(empty)'}: got [${matched}] want [${want}]`);
  }

  if (mismatches.length === 0) {
    pass('provider selection matches the documented rules', `${cases.length} content-type/value cases, exact sets`);
  } else {
    fail('provider selection matches the documented rules', mismatches.join('; '));
  }

  const htmlMatches = ctx.engine.providers
    .matching({ http: { contentType: 'text/html' }, body: '<html></html>' })
    .map(p => p.name);
  if (htmlMatches.includes('html') && htmlMatches.includes('text')) {
    info('HTML responses are recognized twice',
      'HtmlProvider extracts structure, TextProvider extracts raw URLs from the same body');
  }
}

/* -------------------------------------------------------------------------- */
/* 4. Provenance chain                                                        */
/* -------------------------------------------------------------------------- */

{
  const routes = {
    'https://check.test/index': { contentType: 'application/json',
      body: JSON.stringify({ links: ['https://check.test/a'] }) },
    'https://check.test/a': { contentType: 'application/json',
      body: JSON.stringify({ links: ['https://check.test/b'] }) },
    'https://check.test/b': { contentType: 'application/json', body: '{"ok":true}' }
  };
  const ctx = makeContext({ routes, delay: 4 });
  ctx.fireBootstrap();
  await settle(ctx.engine);

  const chain = [];
  let candidate = [...ctx.engine.db.candidates.values()].find(c => c.target.endsWith('/b'));
  const observations = new Set([...ctx.engine.db.observations.values()].map(o => o.candidateId));

  while (candidate) {
    chain.push({
      target: candidate.target.replace('https://check.test', ''),
      mechanism: candidate.hints?.mechanism || candidate.hints?.root ? 'current-page' : 'unknown',
      hasObservation: observations.has(candidate.id),
      parent: candidate.parent || null
    });
    candidate = candidate.parent ? ctx.engine.db.candidates.get(candidate.parent) : null;
  }

  const complete = chain.length >= 3 && chain.every(link => link.hasObservation);
  const line = chain.map(c => `${c.target}${c.hasObservation ? ' (observed)' : ''}`).join(' ← ');
  if (complete) pass('candidate derivation chain is reconstructible', line);
  else fail('candidate derivation chain is reconstructible', line || 'no chain found');

  const ledgersForChain = [...ctx.engine.db.discoveries.values()]
    .filter(d => d.candidateId && d.observationId).length;
  info('discoveries carrying candidate+observation ids', `${ledgersForChain}/${ctx.engine.db.discoveries.size}`);
}

/* -------------------------------------------------------------------------- */
/* 5. Persistence round-trip                                                  */
/* -------------------------------------------------------------------------- */

{
  const routes = {
    'https://check.test/index': { contentType: 'application/json',
      body: JSON.stringify({ links: ['https://check.test/a', 'https://check.test/b'] }) },
    'https://check.test/a': { contentType: 'application/json', body: '{"ok":true}' },
    'https://check.test/b': { contentType: 'application/json', body: '{"ok":true}' }
  };
  const storage = new Map();
  const first = makeContext({ routes, delay: 4, storage });
  first.fireBootstrap();
  await settle(first.engine);

  const before = {
    candidates: first.engine.db.candidates.size,
    discoveries: first.engine.db.discoveries.size,
    resources: first.engine.db.resources.size,
    ledger: first.engine.ledger.events.length
  };

  const second = makeContext({ storage, deferBootstrap: true });
  const after = {
    candidates: second.engine.db.candidates.size,
    discoveries: second.engine.db.discoveries.size,
    resources: second.engine.db.resources.size,
    ledger: second.engine.ledger.events.length
  };

  const persisted = storage.size > 0;
  const candidatesMatch = after.candidates === before.candidates;
  const discoveriesMatch = after.discoveries === before.discoveries;
  const resourcesMatch = after.resources === before.resources;

  if (persisted && candidatesMatch && discoveriesMatch && resourcesMatch) {
    pass('persistence round-trip preserves state', JSON.stringify({ before, after }));
  } else {
    fail('persistence round-trip preserves state',
      `persisted=${persisted} before=${JSON.stringify(before)} after=${JSON.stringify(after)}`);
  }

  info('ledger across restore',
    `${before.ledger} → ${after.ledger} events (the ledger IS persisted and restored)`);

  const freshBudget = second.engine.requestsReserved === 0;
  if (freshBudget) {
    info('request budget resets per execution context',
      'restore() deliberately does not carry requestsReserved over');
  } else {
    defect('request budget carried across restore', String(second.engine.requestsReserved));
  }
}

/* -------------------------------------------------------------------------- */
/* Report                                                                     */
/* -------------------------------------------------------------------------- */

const width = Math.max(...results.map(r => r.name.length));
console.log('invariant checks against prototype/generic-discovery-engine.user.js\n');
for (const r of results) console.log(`[${r.level}] ${r.name.padEnd(width)}  ${r.note}`);
const failures = results.filter(r => r.level === 'FAIL').length;
const defects = results.filter(r => r.level === 'DEFECT').length;
console.log(`\n${results.filter(r => r.level === 'PASS').length} passed, ${failures} failed, ${defects} defect(s)`);
process.exit(failures === 0 ? 0 : 1);
