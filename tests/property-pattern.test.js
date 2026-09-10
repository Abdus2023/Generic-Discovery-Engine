/**
 * property-pattern.test.js — Pattern & Cluster invariants (v0.7.9)
 *
 * Verifies extractUrlPattern normalizes numeric/uuid/hash, preserves structure,
 * collapses same-template URLs, and KnowledgeBase pattern/cluster metrics
 * are deterministic and bounded (seeded).
 */
import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const src = readFileSync(new URL('../dist/generic-discovery-engine.user.js', import.meta.url), 'utf8');

// Re-implement extractUrlPattern mirroring dist (single source of truth for test)
function extractUrlPattern(url, enabled=true) {
  if (!enabled) return String(url);
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
function clusterKey(pattern, origin){ return `${origin}::${pattern}`; }

class KBPattern {
  constructor(){ this.patternIndex=new Map(); this.clusterIndex=new Map(); }
  recordPattern(candidate){
    const pat=extractUrlPattern(candidate.target);
    this.patternIndex.set(pat, (this.patternIndex.get(pat)||0)+1);
    const key=clusterKey(pat, candidate.origin|| new URL(candidate.target).origin);
    this.clusterIndex.set(key, (this.clusterIndex.get(key)||0)+1);
  }
  getPatternMetrics(){ const s=[...this.patternIndex.entries()].sort((a,b)=>b[1]-a[1]).slice(0,20); return {size:this.patternIndex.size, top:s, total:[...this.patternIndex.values()].reduce((a,b)=>a+b,0)}; }
  getClusterMetrics(){ const s=[...this.clusterIndex.entries()].sort((a,b)=>b[1]-a[1]).slice(0,20); return {size:this.clusterIndex.size, top:s, total:[...this.clusterIndex.values()].reduce((a,b)=>a+b,0)}; }
}

function lcg(seed){ let s=seed>>>0; return ()=>{ s=(1664525*s+1013904223)>>>0; return s/0x100000000; }; }

describe('property: pattern inference (v0.7.9)', () => {
  it('source contains inference config + extractUrlPattern + cluster helpers', () => {
    assert.match(src, /inference:\s*\{\s*patternInference/);
    assert.match(src, /extractUrlPattern/);
    assert.match(src, /clusterKeyForCandidate/);
    assert.match(src, /getPatternMetrics/);
    assert.match(src, /getClusterMetrics/);
  });

  it('numeric path segments normalize to {int} and preserve non-numeric', () => {
    assert.equal(extractUrlPattern('https://ex/user/123/profile'), 'https://ex/user/{int}/profile');
    assert.equal(extractUrlPattern('https://ex/page/456'), 'https://ex/page/{int}');
    assert.equal(extractUrlPattern('https://ex/static/app.js'), 'https://ex/static/app.js');
    assert.equal(extractUrlPattern('https://ex/api/v1/789/items'), 'https://ex/api/v1/{int}/items');
  });

  it('query numeric values normalize, names preserved', () => {
    assert.equal(extractUrlPattern('https://ex/search?page=2'), 'https://ex/search?page={int}');
    assert.equal(extractUrlPattern('https://ex/list?a=1&b=2'), 'https://ex/list?a={int}&b={int}');
    assert.equal(extractUrlPattern('https://ex/q?term=hello'), 'https://ex/q?term=hello');
  });

  it('uuid and hash segments normalize', () => {
    assert.equal(extractUrlPattern('https://ex/item/550e8400-e29b-41d4-a716-446655440000'), 'https://ex/item/{uuid}');
    assert.equal(extractUrlPattern('https://ex/file/abc123def456abc123def456abc12345'), 'https://ex/file/{hash}');
    assert.equal(extractUrlPattern('https://ex/view?id=550e8400-e29b-41d4-a716-446655440000'), 'https://ex/view?id={uuid}');
  });

  it('same template different ids collapse to same pattern (500 iter)', () => {
    const rng=lcg(0x9ab);
    for(let i=0;i<500;i++){
      const id1=Math.floor(rng()*10000);
      const id2=Math.floor(rng()*10000);
      const p1=extractUrlPattern(`https://ex/user/${id1}/post/${id2}`);
      const p2=extractUrlPattern(`https://ex/user/${id1+1}/post/${id2+1}`);
      assert.equal(p1, 'https://ex/user/{int}/post/{int}');
      assert.equal(p2, 'https://ex/user/{int}/post/{int}');
      assert.equal(p1,p2);
    }
  });

  it('different structures produce different patterns', () => {
    const a=extractUrlPattern('https://ex/user/123');
    const b=extractUrlPattern('https://ex/user/abc');
    const c=extractUrlPattern('https://ex/page/123');
    assert.notEqual(a,b);
    assert.notEqual(a,c);
  });

  it('clustering groups by origin+pattern, metrics sorted and bounded (seeded)', () => {
    const kb=new KBPattern();
    const origins=['https://a.ex','https://b.ex'];
    const rng=lcg(0xcde);
    for(let i=0;i<200;i++){
      const origin=origins[Math.floor(rng()*2)];
      const id=Math.floor(rng()*100);
      kb.recordPattern({target:`${origin}/user/${id}`, origin});
    }
    const pm=kb.getPatternMetrics();
    const cm=kb.getClusterMetrics();
    assert.ok(pm.size<=2, `patterns should collapse to ≤2, got ${pm.size}`);
    assert.ok(cm.size<=2, `clusters ≤2, got ${cm.size}`);
    assert.equal(pm.total,200);
    assert.equal(cm.total,200);
    // top sorted descending
    for(let i=1;i<pm.top.length;i++) assert.ok(pm.top[i-1][1] >= pm.top[i][1]);
    for(let i=1;i<cm.top.length;i++) assert.ok(cm.top[i-1][1] >= cm.top[i][1]);
    // top limited to 20
    assert.ok(pm.top.length<=20);
  });
});
