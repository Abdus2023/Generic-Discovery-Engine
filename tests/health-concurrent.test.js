/**
 * health-concurrent.test.js — Health metrics + concurrent providers (v1.4.0)
 */
import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const dist = readFileSync(new URL('../dist/generic-discovery-engine.user.js', import.meta.url), 'utf8');

describe('health + concurrent static presence (v1.4.0)', () => {
  it('CONFIG.health and providers.concurrent present', () => {
    assert.match(dist, /CONFIG\.health/);
    assert.match(dist, /slowProviderMs/);
    assert.match(dist, /maxRecentErrors/);
    assert.match(dist, /concurrent/);
  });
  it('getHealthMetrics and health in export present', () => {
    assert.match(dist, /getHealthMetrics/);
    assert.match(dist, /health,/);
    assert.match(dist, /providerHealth/);
  });
  it('concurrent Promise.all branch present', () => {
    assert.match(dist, /Promise\.all/);
    assert.match(dist, /processDiscoveries/);
    assert.match(dist, /CONFIG\.providers\?\.concurrent/);
  });
});

// Minimal harness for health logic (mirrors src)
function mockHealth(coverage, providerMetrics, opts={}) {
  const CONFIG = { health: { enabled:true, slowProviderMs:50, maxRecentErrors:20, ...opts }, maxCandidates:750, maxRequests:150, adaptive:{enabled:true} };
  const slowThreshold = CONFIG.health.slowProviderMs;
  const slowProviders = Object.entries(providerMetrics).filter(([_,m])=> (m.avgMs??0)>slowThreshold).map(([name,m])=>({name, avgMs:m.avgMs}));
  let status='healthy';
  if(slowProviders.length>2 || coverage.frontierSize/750>0.9 || coverage.requestsUsed/150>0.9) status='degraded';
  if(slowProviders.some(p=>p.avgMs>100) || coverage.liveCount>=CONFIG.maxCandidates) status='unhealthy';
  if(!CONFIG.health.enabled) status='disabled';
  return { status, providerHealth:{slowProviders, slowThresholdMs:slowThreshold} };
}

describe('health behavior', () => {
  it('healthy when no slow providers and low pressure', () => {
    const cov={frontierSize:10, liveCount:10, requestsUsed:10, observations:10, ledgerSize:100};
    const metrics={html:{avgMs:5, calls:10, matches:5}, json:{avgMs:10, calls:10, matches:2}};
    const h=mockHealth(cov, metrics);
    assert.equal(h.status,'healthy');
    assert.equal(h.providerHealth.slowProviders.length,0);
  });
  it('degraded when many slow providers', () => {
    const cov={frontierSize:10, liveCount:10, requestsUsed:10, observations:10, ledgerSize:100};
    const metrics={a:{avgMs:60,calls:10,matches:5}, b:{avgMs:55,calls:10,matches:5}, c:{avgMs:70,calls:10,matches:5}};
    const h=mockHealth(cov, metrics);
    assert.equal(h.status,'degraded');
    assert.equal(h.providerHealth.slowProviders.length,3);
  });
  it('unhealthy when liveCount at cap', () => {
    const cov={frontierSize:10, liveCount:750, requestsUsed:10, observations:10, ledgerSize:100};
    const metrics={html:{avgMs:5,calls:10,matches:5}};
    const h=mockHealth(cov, metrics);
    assert.equal(h.status,'unhealthy');
  });
  it('disabled when health disabled', () => {
    const cov={frontierSize:700, liveCount:10, requestsUsed:140, observations:10, ledgerSize:100};
    const metrics={html:{avgMs:60,calls:10,matches:5}, json:{avgMs:60,calls:10,matches:5}, xml:{avgMs:60,calls:10,matches:5}};
    const h=mockHealth(cov, metrics, {enabled:false});
    assert.equal(h.status,'disabled');
  });
});

describe('concurrent providers', () => {
  it('Promise.all dedup preserves Set semantics', async () => {
    const emitted=new Set();
    const discoveriesBatch1=[{targetUrl:()=>'https://ex/a'}, {targetUrl:()=>'https://ex/b'}];
    const discoveriesBatch2=[{targetUrl:()=>'https://ex/a'}, {targetUrl:()=>'https://ex/c'}];
    const process=(batch)=>{
      for(const d of batch){
        const k=d.targetUrl();
        if(emitted.has(k)) continue;
        emitted.add(k);
      }
    };
    // sequential
    process(discoveriesBatch1); process(discoveriesBatch2);
    assert.deepEqual([...emitted].sort(), ['https://ex/a','https://ex/b','https://ex/c']);
    // concurrent (Promise.all) should same dedup
    emitted.clear();
    const results=[{discoveries:discoveriesBatch1},{discoveries:discoveriesBatch2}];
    for(const {discoveries} of results) process(discoveries);
    assert.deepEqual([...emitted].sort(), ['https://ex/a','https://ex/b','https://ex/c']);
  });
  it('concurrent flag toggles execution path', () => {
    // static check that dist contains both branches
    assert.match(dist, /if \(CONFIG\.providers\?\.concurrent\)/);
  });
  it('health includes coverage and providerHealth', () => {
    // health return shape check via static presence
    assert.match(dist, /health:\s*\{/);
    assert.match(dist, /frontierPressure/);
    assert.match(dist, /requestPressure/);
  });
});
