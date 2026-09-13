/**
 * provider-lazy.test.js — Lazy ProviderRegistry (v1.1.0)
 * Verifies lazy instantiation, disabled filtering, metrics, and order preservation.
 */
import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

// --- static checks ---------------------------------------------------------
const dist = readFileSync(new URL('../dist/generic-discovery-engine.user.js', import.meta.url), 'utf8');
const srcProviders = readFileSync(new URL('../src/providers.js', import.meta.url), 'utf8');
const srcConfig = readFileSync(new URL('../src/config.js', import.meta.url), 'utf8');

describe('provider lazy static presence (v1.1.0)', () => {
  it('CONFIG.providers exists with lazy true and disabled', () => {
    assert.match(srcConfig, /providers:\s*\{/);
    assert.match(srcConfig, /lazy:\s*true/);
    assert.match(srcConfig, /disabled:\s*\[\]/);
    assert.match(dist, /CONFIG\.providers/);
    assert.match(dist, /lazy/);
  });
  it('ProviderRegistry uses factories and lazy order', () => {
    assert.match(srcProviders, /this\.factories/);
    assert.match(srcProviders, /this\.order/);
    assert.match(srcProviders, /this\.instances/);
    assert.match(srcProviders, /getInstanceCount/);
    assert.match(srcProviders, /getMetrics/);
    assert.match(dist, /factories/);
    assert.match(dist, /getInstanceCount/);
    assert.match(dist, /getProviderMetrics/);
  });
  it('9 providers ordered Html/Json/Xml/Css/JS/Robots/Headers/Binary/Text still present', () => {
    const order = ['HtmlProvider','JsonProvider','XmlProvider','CssProvider','JavaScriptProvider','RobotsProvider','HeadersProvider','BinaryProvider','TextProvider'];
    let lastIdx=-1;
    for(const name of order){
      const idx=dist.indexOf(`new ${name}()`);
      assert.ok(idx>lastIdx, `${name} out of order or missing`);
      lastIdx=idx;
    }
  });
  it('coverage and export include provider metrics', () => {
    assert.match(dist, /providerInstances/);
    assert.match(dist, /providerMetrics/);
    assert.match(dist, /providers:\s*\{/);
  });
});

// --- behavioral harness (replicates src logic) -----------------------------
function makeMockConfig(lazy=true, disabled=[]) {
  return { providers: { lazy, disabled } };
}
class MockHtml { constructor(){this.name='html';} matches(o){return /text\/html/i.test(o.http?.contentType||'') || /<html/i.test(o.body||'');} }
class MockJson { constructor(){this.name='json';} matches(o){return /json/i.test(o.http?.contentType||'');} }
class MockText { constructor(){this.name='text';} matches(o){return true;} }

function createLazyRegistry(CONFIG) {
  const factories = {
    html: () => new MockHtml(),
    json: () => new MockJson(),
    text: () => new MockText(),
  };
  const order = ['html','json','text'];
  const instances = new Map();
  const metrics = new Map();
  if (CONFIG.providers.lazy === false) {
    for(const n of order){
      if (CONFIG.providers.disabled.includes(n)) continue;
      instances.set(n, factories[n]());
      metrics.set(n, {calls:0,matches:0,totalMs:0});
    }
  }
  function _get(name){
    if (CONFIG.providers.disabled.includes(name)) return null;
    if (instances.has(name)) return instances.get(name);
    const f=factories[name]; if(!f) return null;
    const inst=f(); instances.set(name,inst); metrics.set(name,{calls:0,matches:0,totalMs:0}); return inst;
  }
  return {
    _get, instances, metrics, order,
    matching(obs){
      const m=[]; for(const n of order){const p=_get(n); if(!p) continue; const metric=metrics.get(n); const s=Date.now(); let ok=false; try{ok=p.matches(obs);}catch{} const d=Date.now()-s; metric.calls++; if(ok) metric.matches++; metric.totalMs+=d; if(ok) m.push(p);} return m;
    },
    getMetrics(){ const o={}; for(const [k,v] of metrics) o[k]={...v, avgMs: v.calls? v.totalMs/v.calls:0}; return o; },
    getInstanceCount(){return instances.size;}
  };
}

describe('provider lazy behavior', () => {
  it('lazy true starts with 0 instances, instantiates on matching', () => {
    const cfg = makeMockConfig(true, []);
    const reg = createLazyRegistry(cfg);
    assert.equal(reg.getInstanceCount(), 0);
    const obs = {http:{contentType:'text/html'}, body:'<html>'};
    const matched = reg.matching(obs);
    // html and text should match (json no), so 3 factories touched => 3 instances
    assert.equal(reg.getInstanceCount(), 3);
    assert.ok(matched.some(p=>p.name==='html'));
    assert.ok(matched.some(p=>p.name==='text'));
  });
  it('eager false pre-instantiates all non-disabled', () => {
    const cfg = makeMockConfig(false, []);
    const reg = createLazyRegistry(cfg);
    assert.equal(reg.getInstanceCount(), 3);
    const metrics = reg.getMetrics();
    assert.ok(metrics.html && metrics.json && metrics.text);
  });
  it('disabled providers are never instantiated nor matched', () => {
    const cfg = makeMockConfig(true, ['json','text']);
    const reg = createLazyRegistry(cfg);
    const obs = {http:{contentType:'application/json'}, body:'{}'};
    const matched = reg.matching(obs);
    // only html factory will be instantiated (json/text disabled)
    assert.equal(reg.getInstanceCount(), 1);
    assert.ok(!matched.some(p=>p.name==='json'));
    assert.ok(!matched.some(p=>p.name==='text'));
    // metrics should not contain disabled
    const m = reg.getMetrics();
    assert.ok(!m.json);
    assert.ok(!m.text);
  });
  it('metrics track calls/matches and avgMs', () => {
    const cfg = makeMockConfig(true, []);
    const reg = createLazyRegistry(cfg);
    reg.matching({http:{contentType:'text/html'}, body:'<html>'});
    reg.matching({http:{contentType:'application/json'}, body:'{}'});
    const metrics = reg.getMetrics();
    assert.equal(metrics.html.calls, 2);
    assert.equal(metrics.html.matches, 1);
    assert.equal(metrics.json.calls, 2);
    assert.equal(metrics.json.matches, 1);
    assert.equal(metrics.text.calls, 2);
    assert.ok(typeof metrics.html.avgMs === 'number');
  });
  it('order preserved: html before json before text', () => {
    const cfg = makeMockConfig(true, []);
    const reg = createLazyRegistry(cfg);
    const obs = {http:{contentType:'text/html'}, body:'<html>'}; // html and text match
    const matched = reg.matching(obs);
    const idxHtml = matched.findIndex(p=>p.name==='html');
    const idxText = matched.findIndex(p=>p.name==='text');
    assert.ok(idxHtml < idxText, 'html should be before text');
    // json not matched but still instantiated? Check instances order same as definition order
    assert.deepEqual(reg.order, ['html','json','text']);
  });
});
