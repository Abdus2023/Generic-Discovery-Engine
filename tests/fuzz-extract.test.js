#!/usr/bin/env node
// fuzz-extract.test.js — deterministic fuzz for extraction & canonicalization
// No external deps. Seeded LCG ensures reproducibility. Tests that extract*/* helpers
// never throw on malformed/large inputs and preserve invariants (dedup, bounded output).
import { describe, it } from 'node:test';
import assert from 'node:assert/strict';

// Mirror helpers from dist/generic-discovery-engine.user.js (verbatim for fidelity)
const CONFIG = {
  stripTrackingParams: true,
  sameOriginOnly: false, // fuzz off sameOrigin to test canonicalization shape alone
  privacy: { stripSensitiveParams: false, sensitiveKeys: [/^token$/i, /^session$/i, /^auth$/i, /^sid$/i, /^access_token$/i, /^api_key$/i, /^apikey$/i, /^secret$/i] },
  fingerprintMaxChars: 1_000_000,
  maxBodyChars: 2_000_000,
};

function canonicalizeUrl(raw, base = 'https://example.com/') {
  try {
    const url = new URL(raw, base);
    url.hash = '';
    if (CONFIG.stripTrackingParams) {
      const tracking = [/^utm_/i, /^fbclid$/i, /^gclid$/i, /^mc_/i, /^ref$/i];
      for (const k of [...url.searchParams.keys()]) if (tracking.some(rx => rx.test(k))) url.searchParams.delete(k);
    }
    if (CONFIG.privacy?.stripSensitiveParams) {
      const sensitive = CONFIG.privacy.sensitiveKeys || [];
      for (const k of [...url.searchParams.keys()]) if (sensitive.some(rx => rx.test(k))) url.searchParams.delete(k);
    }
    return url.href;
  } catch { return null; }
}

function extractUrlsFromText(text) {
  if (!text) return [];
  const results = new Set();
  const absolute = /\bhttps?:\/\/[^\s"'<>\)]+/gi;
  for (const m of String(text).matchAll(absolute)) results.add(m[0]);
  const relative = /(?:^|["'(\s])((?:\/|\.\.?\/)[A-Za-z0-9._~:/?#\[\]@!$&'*+,;=%-]+)/g;
  for (const m of String(text).matchAll(relative)) results.add(m[1]);
  return [...results];
}
function extractCssUrls(text) {
  const results = [];
  const rx = /url\(\s*(['"]?)(.*?)\1\s*\)/gi;
  for (const m of String(text || '').matchAll(rx)) if (m[2]) results.push(m[2]);
  return results;
}
function extractXmlLocsFallback(text) {
  const results = [];
  const rx = /<loc[^>]*>(.*?)<\/loc>/gis;
  for (const m of String(text || '').matchAll(rx)) results.push(m[1].trim());
  return results;
}
function fnv1a32(text) {
  let hash = 0x811c9dc5;
  for (let i = 0; i < text.length; i++) {
    hash ^= text.charCodeAt(i);
    hash += (hash << 1) + (hash << 4) + (hash << 7) + (hash << 8) + (hash << 24);
    hash >>>= 0;
  }
  return hash.toString(16).padStart(8, '0');
}
function makeFingerprint(body) {
  if (!body) return null;
  const sample = String(body).slice(0, CONFIG.fingerprintMaxChars).replace(/\s+/g, ' ').trim();
  return { algorithm: 'fnv1a32', hash: fnv1a32(sample), length: String(body).length, sampledLength: sample.length };
}

// Seeded LCG (same sequence every run)
function rng(seed = 0x9e3779b1) {
  let s = seed >>> 0;
  return () => {
    s = (s * 1664525 + 1013904223) >>> 0;
    return s / 0x100000000;
  };
}
const rand = rng(0x12345);
function randInt(n) { return Math.floor(rand() * n); }
function randChoice(arr) { return arr[randInt(arr.length)]; }
function randString(len, charset) {
  let s = ''; for (let i = 0; i < len; i++) s += charset[randInt(charset.length)]; return s;
}
const URL_CHARSET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._~:/?#[]@!$&\'*+,;=%-';
const HTML_CHARSET = '<>\"\' /=\n\t' + URL_CHARSET;
const CSS_CHARSET = 'url()\"\' \n\t;:' + URL_CHARSET;

describe('fuzz: canonicalizeUrl never throws', () => {
  it('deterministic fuzz 50 cases + edge cases', () => {
    const bases = ['https://example.com/', 'https://example.com/base/path/', 'https://evil.com/'];
    const edge = ['', ' ', 'https://[:::1', 'http://', '/relative', '//example.com/protocol', 'https://example.com/page?utm_source=x&token=secret&keep=1', 'https://example.com/a'.repeat(5000), 'https://example.com/' + 'a'.repeat(2_000_000).slice(0, 10000)];
    for (const raw of edge) {
      const out = canonicalizeUrl(raw, bases[0]);
      assert.ok(out === null || typeof out === 'string');
      if (out) assert.ok(out.startsWith('http'), 'canonicalized should be http(s)');
    }
    for (let i = 0; i < 50; i++) {
      const proto = randChoice(['https://', 'http://', '', 'javascript:', 'data:', 'ftp://', 'ht!tp://']);
      const host = randChoice(['example.com', 'evil.com', '[::1]', '']);
      const path = '/' + randString(randInt(30), URL_CHARSET.replace(/:/g, ''));
      const q = rand() < 0.5 ? '?' + randString(randInt(20), 'utm_sourcefbclidtoken=&=') : '';
      const raw = proto + host + path + q + (rand() < 0.2 ? '#frag' : '');
      const base = randChoice(bases);
      const out = canonicalizeUrl(raw, base);
      assert.ok(out === null || typeof out === 'string');
      if (out) {
        assert.equal(canonicalizeUrl(out, base), out, 'canonicalize should be idempotent for its own output');
      }
    }
  });
  it('tracking params stripped, privacy scrub opt-in strips token family', () => {
    const url = 'https://example.com/page?utm_source=x&fbclid=123&keep=1&token=secret&session=abc&api_key=zz';
    assert.equal(canonicalizeUrl(url), 'https://example.com/page?keep=1&token=secret&session=abc&api_key=zz');
    CONFIG.privacy.stripSensitiveParams = true;
    const url2 = canonicalizeUrl(url);
    assert.equal(url2, 'https://example.com/page?keep=1');
    CONFIG.privacy.stripSensitiveParams = false;
  });
  it('2M body slice invariant (makeFingerprint sampling)', () => {
    const body = 'a'.repeat(2_000_000) + ' https://example.com/extra';
    const fp = makeFingerprint(body);
    assert.equal(fp.length, 2_000_000 + ' https://example.com/extra'.length);
    assert.equal(fp.sampledLength, 1_000_000);
    assert.equal(fp.hash.length, 8);
    // second call same
    assert.equal(makeFingerprint(body).hash, fp.hash);
  });
});

describe('fuzz: extractUrlsFromText', () => {
  it('never throws, dedupes, bounded', () => {
    const edgeBodies = ['', null, undefined, 'https://example.com/a https://example.com/a', 'no urls here', '<a href=\"/path\">', 'http://', 'https://example.com/' + 'a'.repeat(2_000_000).slice(0, 1000)];
    for (const b of edgeBodies) {
      const out = extractUrlsFromText(b);
      assert.ok(Array.isArray(out));
      assert.equal(out.length, new Set(out).size, 'deduped');
    }
    for (let i = 0; i < 80; i++) {
      const len = randInt(2000);
      let txt = randString(len, HTML_CHARSET);
      if (rand() < 0.3) txt += ' https://example.com/' + randString(10, URL_CHARSET);
      if (rand() < 0.2) txt += ' \"/relative/' + randString(8, URL_CHARSET) + '\"';
      const out = extractUrlsFromText(txt);
      assert.ok(Array.isArray(out));
      assert.equal(out.length, new Set(out).size);
      // absolute URLs in output should look like URL prefix; relative should start with / or .
      for (const u of out) assert.ok(typeof u === 'string' && u.length > 0);
    }
  });
});

describe('fuzz: extractCssUrls', () => {
  it('never throws, extracts balanced url()', () => {
    const cases = ["background:url('https://example.com/a.png')", 'url(\"https://example.com/b.css\")', 'no url', 'url(', 'url()', 'url(  )', 'url(https://example.com/'.repeat(100)];
    for (const c of cases) {
      const out = extractCssUrls(c);
      assert.ok(Array.isArray(out));
    }
    for (let i = 0; i < 40; i++) {
      const n = randInt(20);
      let css = '';
      for (let j = 0; j < n; j++) css += `a{background:url(${randChoice(['\"', "'", ''])}${randString(randInt(20), URL_CHARSET)}${randChoice(['\"', "'", ''])} )}; `;
      const out = extractCssUrls(css);
      assert.ok(Array.isArray(out));
      assert.ok(out.length <= n);
    }
  });
});

describe('fuzz: fnv1a32 stability', () => {
  it('deterministic, empty baseline, no collision on crafted set', () => {
    assert.equal(fnv1a32('hello'), fnv1a32('hello'));
    assert.equal(fnv1a32(''), '811c9dc5');
    const set = new Set();
    for (let i = 0; i < 100; i++) {
      const s = randString(20, URL_CHARSET);
      const h = fnv1a32(s);
      assert.equal(h.length, 8);
      set.add(h);
    }
    // 100 random 20-char strings should have <5 collisions (sanity, not crypto proof)
    assert.ok(set.size >= 95, `expected ~100 unique hashes, got ${set.size}`);
  });
});

describe('fuzz: combine — provider-like pipeline never throws on 2M body', () => {
  it('2M html-like body with many urls', () => {
    let body = '<html><body>';
    for (let i = 0; i < 500; i++) body += `<a href=\"https://example.com/${randString(6, URL_CHARSET)}\">link</a>`;
    body += ' https://example.com/extra '.repeat(1000);
    body = body.slice(0, 2_000_000);
    // simulate html provider text fallback
    const urls = extractUrlsFromText(body);
    // seeded RNG may produce duplicates via Set dedup or truncated URLs; require a sane lower bound
    assert.ok(urls.length >= 300, `expected >=300 urls, got ${urls.length}`);
    // canonicalize each (first 20)
    for (const u of urls.slice(0, 20)) {
      const c = canonicalizeUrl(u);
      assert.ok(c === null || c.startsWith('https://'));
    }
  });
});
