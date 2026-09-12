#!/usr/bin/env node
// export-inference.test.js — Export Hardening + Inference Metrics (v0.8.2)
// Verifies getCoverageMetrics determinism + exportData inference block
import { describe, it, before } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import path from 'node:path';

function createSandbox() {
  const store = new Map();
  const sandbox = {
    console, setTimeout, clearTimeout, setInterval, clearInterval,
    Date, Math, JSON, RegExp, URL, URLSearchParams, AbortController, AbortSignal,
    location: { href: 'https://example.com/', origin: 'https://example.com', hostname: 'example.com', pathname: '/' },
    GM_getValue: (k,d)=> store.has(k)?store.get(k):d,
    GM_setValue: (k,v)=> store.set(k,v),
    GM_xmlhttpRequest: undefined,
    document: {
      readyState: 'loading',
      addEventListener: ()=>{},
      createElement: (tag)=>({ tagName: tag.toUpperCase(), style:{}, appendChild:()=>{}, remove:()=>{}, set textContent(v){this._text=v}, get textContent(){return this._text||''}, addEventListener:()=>{}, querySelectorAll:()=>[], querySelector:()=>null }),
      querySelectorAll:()=>[], querySelector:()=>null,
      documentElement: { appendChild:()=>{}, querySelectorAll:()=>[], querySelector:()=>null },
      head: { appendChild:()=>{} },
      body: { appendChild:()=>{} }
    },
    window: null,
    PerformanceObserver: undefined,
    MutationObserver: undefined,
    DOMParser: class { parseFromString(body){ return { querySelectorAll:()=>[], querySelector:()=>null, documentElement:{ outerHTML: body } } } },
    confirm: ()=>false, Blob: globalThis.Blob, URL: globalThis.URL,
  };
  sandbox.window = sandbox; sandbox.globalThis = sandbox; sandbox.self = sandbox;
  return { sandbox, store };
}
function loadEngine(sandbox){
  const code = fs.readFileSync(path.join(import.meta.dirname,'../dist/generic-discovery-engine.user.js'),'utf8');
  const script = new vm.Script(code, {filename:'generic-discovery-engine.user.js'});
  vm.createContext(sandbox); script.runInContext(sandbox);
  return sandbox.GenericDiscoveryEngine || sandbox.window.GenericDiscoveryEngine;
}

describe('export hardening (v0.8.2)', ()=>{
  let engine, sandbox;
  before(()=>{
    const created = createSandbox(); sandbox = created.sandbox;
    // minimal GM_xhr mock for observations with fingerprint
    sandbox.GM_xmlhttpRequest = ({url,onload})=>{
      setTimeout(()=> onload({ status:200, responseHeaders:'content-type: text/html\n', responseText:`<a href=\"/page/${Math.floor(Math.random()*1000)}\">x</a>`, finalUrl:url }), 1)
    };
    engine = loadEngine(sandbox);
    engine.running=false; engine.stopRequested=false; engine.paused=false;
    engine.db.candidates.clear(); engine.db.candidateKeys.clear(); engine.db.visited.clear();
    engine.ledger.events.length=0; engine.ledger.sequence=0; engine.requestsReserved=0;
    engine.currentConcurrency=2;
  });

  it('getCoverageMetrics includes inference keys and sorted queuedByType', ()=>{
    // seed two candidates of different types in reverse insertion order
    engine.db.candidates.clear(); engine.db.candidateKeys.clear();
    engine.discover('https://example.com/api/1','api',{priority:0.9});
    engine.discover('https://example.com/zz','url',{priority:0.5});
    // also add a second api so order would be api, api, url if insertion-ordered, but sorted should be alphabetical
    engine.discover('https://example.com/api/2','api',{priority:0.8});
    const cov = engine.getCoverageMetrics();
    assert.ok('patternCount' in cov, 'patternCount missing');
    assert.ok('clusterCount' in cov, 'clusterCount missing');
    assert.ok('fingerprintUnique' in cov, 'fingerprintUnique missing');
    assert.ok('inferenceEnabled' in cov, 'inferenceEnabled missing');
    assert.equal(typeof cov.patternCount,'number');
    assert.equal(typeof cov.clusterCount,'number');
    assert.equal(coverageHasSortedKeys(cov.queuedByType), true, 'queuedByType keys not sorted');
    // inferenceEnabled should be true by default
    assert.equal(cov.inferenceEnabled, true);
  });

  it('exportData includes inference block with patternMetrics/clusterMetrics/fingerprintStats', ()=>{
    const exported = engine.exportData();
    assert.equal(exported.schema,'gde-export-v8.0');
    assert.ok(exported.coverage, 'coverage missing');
    assert.ok(exported.inference, 'inference missing (hardening)');
    assert.ok('patternMetrics' in exported.inference, 'patternMetrics missing');
    assert.ok('clusterMetrics' in exported.inference, 'clusterMetrics missing');
    assert.ok('fingerprintStats' in exported.inference, 'fingerprintStats missing');
    assert.equal(typeof exported.inference.patternMetrics.size,'number');
    assert.ok(Array.isArray(exported.inference.patternMetrics.top));
    assert.ok(exported.inference.patternMetrics.top.length <= 20, 'pattern top bounded 20');
    assert.ok(Array.isArray(exported.inference.clusterMetrics.top));
    assert.equal(typeof exported.inference.fingerprintStats.unique,'number');
  });

  it('pattern inference populates after discover, coverage patternCount grows', ()=>{
    engine.db.candidates.clear(); engine.db.candidateKeys.clear(); engine.db.patternIndex.clear(); engine.db.clusterIndex.clear();
    const before = engine.getCoverageMetrics().patternCount;
    engine.discover('https://example.com/user/123','url',{priority:0.5});
    engine.discover('https://example.com/user/456','url',{priority:0.5});
    engine.discover('https://example.com/user/789','url',{priority:0.5});
    const after = engine.getCoverageMetrics().patternCount;
    // patterns should collapse numeric segment to /{int}, so at least one pattern bucket
    assert.ok(after >= before, 'patternCount should not decrease');
    const pm = engine.db.getPatternMetrics();
    assert.ok(pm.top.some(([pat])=> pat.includes('{int}')), 'pattern top should include collapsed {int}');
  });

  it('exportData is JSON-stable (sorted queuedByType) across multiple calls', ()=>{
    const a = engine.exportData();
    const b = engine.exportData();
    // coverage queuedByType JSON should be identical string when re-serialized
    const sa = JSON.stringify(a.coverage.queuedByType);
    const sb = JSON.stringify(b.coverage.queuedByType);
    assert.equal(sa, sb, 'queuedByType JSON not stable');
    // ledger export is seq-ordered
    assert.ok(a.ledger.events.every((e,i)=> e.seq === i+1 || e.seq > (a.ledger.events[i-1]?.seq||0)), 'ledger seq not monotonic');
  });

  it('static dist contains inference keys', ()=>{
    const src = fs.readFileSync(path.join(import.meta.dirname,'../dist/generic-discovery-engine.user.js'),'utf8');
    assert.match(src, /patternCount/);
    assert.match(src, /clusterCount/);
    assert.match(src, /fingerprintUnique/);
    assert.match(src, /inferenceEnabled/);
    assert.match(src, /patternMetrics/);
    assert.match(src, /clusterMetrics/);
    assert.match(src, /fingerprintStats/);
  });

  it('coverage fingerprintUnique matches fingerprintIndex size', ()=>{
    // fingerprintUnique is derived from fingerprintIndex size (no observation side-effects needed)
    engine.db.fingerprintIndex.clear();
    // also clear observations to keep serialize stable (no plain objects)
    engine.db.observations.clear();
    assert.equal(engine.getCoverageMetrics().fingerprintUnique, 0);
    // directly populate fingerprintIndex deterministically (avoids needing Observation.serialize)
    engine.db.fingerprintIndex.set('abcd1234', new Set(['https://example.com/a']));
    assert.equal(engine.getCoverageMetrics().fingerprintUnique, 1);
    assert.equal(engine.exportData().inference.fingerprintStats.unique, 1);
    assert.equal(engine.exportData().inference.fingerprintStats.total, 1);
    // cleanup for other tests
    engine.db.fingerprintIndex.clear();
    engine.db.observations.clear();
  });
});

function coverageHasSortedKeys(obj){
  const keys = Object.keys(obj);
  const sorted = [...keys].sort();
  return keys.join(',') === sorted.join(',');
}
