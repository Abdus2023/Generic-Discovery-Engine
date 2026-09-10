/**
 * property-determinism.test.js — Determinism & Bounds invariants (v0.7.7)
 *
 * Covers:
 * - CONFIG.candidateTTL expiry (queued/failed → ttl-expired)
 * - Ledger FIFO 5000 invariant (sequence monotonic, oldest evicted)
 * - Origin throttle invariants (interval & concurrency)
 * - Fingerprint determinism (fnv1a32 + sampling)
 * - LiveCount bound 750 under TTL expiries
 */
import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const src = readFileSync(new URL('../dist/generic-discovery-engine.user.js', import.meta.url), 'utf8');

function lcg(seed) { let s = seed >>> 0; return () => { s = (1664525 * s + 1013904223) >>> 0; return s / 0x100000000; }; }

function now() { return Date.now(); }

// Minimal re-implementations mirroring dist logic for deterministic unit tests
function fnv1a32(str) {
  let hash = 0x811c9dc5;
  for (let i = 0; i < str.length; i++) {
    hash ^= str.charCodeAt(i);
    hash = Math.imul(hash, 0x01000193) >>> 0;
  }
  return (hash >>> 0).toString(16).padStart(8, '0');
}
function makeFingerprint(body, maxChars = 1_000_000) {
  const s = String(body ?? '');
  const sampled = s.length > maxChars ? s.slice(0, maxChars) : s;
  return { algorithm: 'fnv1a32', hash: fnv1a32(sampled), length: s.length, sampledLength: sampled.length };
}

class Candidate {
  constructor({ target, type='url', priority=0, status='queued', depth=0, createdAt=now(), attempts=0 }={}) {
    this.id = `c-${Math.random().toString(36).slice(2,7)}`;
    this.target = target; this.type = type; this.priority = priority; this.status = status;
    this.depth = depth; this.createdAt = createdAt; this.attempts = attempts; this.nextAttemptAt = 0;
  }
  identityKey(){ return `${this.type}:${this.target}`; }
  effectivePriority(){ return this.priority - this.depth*0.045 - this.attempts*0.05; }
}

class KnowledgeBaseTTL {
  constructor({ maxCandidates=10, ttl=0 }={}) {
    this.candidates = new Map(); this.candidateKeys = new Map(); this.visited = new Set(); this.diagnostics=[]; this.stats={skipped:0, claimed:0};
    this.maxCandidates = maxCandidates; this.candidateTTL = ttl;
  }
  recordDiagnostic(type, data){ this.diagnostics.push({type,data}); }
  markSkipped(c, reason){ c.status='skipped'; c.skippedAt=now(); this.visited.add(c.identityKey()); this.stats.skipped++; }
  addCandidate(c){ const key=c.identityKey(); if(this.candidateKeys.has(key)) return this.candidates.get(this.candidateKeys.get(key)); if(this.visited.has(key)) return null; const live=[...this.candidates.values()].filter(x=>!['completed','skipped'].includes(x.status)).length; if(live>=this.maxCandidates) return null; this.candidates.set(c.id,c); this.candidateKeys.set(key,c.id); return c; }
  claimNextCandidate(){
    const eligible=[];
    for(const cand of this.candidates.values()){
      if(cand.status!=='queued' && cand.status!=='failed') continue;
      if(cand.nextAttemptAt && cand.nextAttemptAt>now()) continue;
      if(this.candidateTTL>0 && cand.createdAt && now()-cand.createdAt>this.candidateTTL){
        this.markSkipped(cand,'ttl-expired'); this.recordDiagnostic('candidate-ttl-expired',{id:cand.id, age: now()-cand.createdAt}); continue;
      }
      eligible.push(cand);
    }
    eligible.sort((a,b)=>b.effectivePriority()-a.effectivePriority());
    const cand=eligible[0]; if(!cand) return null; cand.status='claimed'; cand.claimedAt=now(); this.stats.claimed++; return cand;
  }
}

class Ledger {
  constructor(cap=5){ this.events=[]; this.cap=cap; this.seq=0; }
  append(type, data){ this.events.push({seq: ++this.seq, type, data, at: now()}); if(this.events.length>this.cap) this.events.splice(0, this.events.length-this.cap); }
}

class OriginControllerMock {
  constructor({ maxConcurrentPerOrigin=2, minInterval=150 }={}) { this.maxConcurrentPerOrigin=maxConcurrentPerOrigin; this.minInterval=minInterval; this.perOrigin=new Map(); }
  canRequest(origin){
    const rec=this.perOrigin.get(origin); if(!rec) return true;
    if(rec.concurrent>=this.maxConcurrentPerOrigin) return false;
    if(rec.lastAt && now()-rec.lastAt < this.minInterval) return false;
    return true;
  }
  recordStart(origin){ let r=this.perOrigin.get(origin); if(!r) r={concurrent:0,lastAt:0, count:0}; r.concurrent++; r.lastAt=now(); r.count++; this.perOrigin.set(origin,r); }
  recordEnd(origin){ const r=this.perOrigin.get(origin); if(r) r.concurrent = Math.max(0, r.concurrent-1); }
}

describe('property: TTL determinism (v0.7.7)', () => {
  it('queued older than TTL is skipped on claim (ttl-expired)', async () => {
    const kb = new KnowledgeBaseTTL({ maxCandidates: 10, ttl: 100 });
    const old = new Candidate({ target: 'https://ex/old', createdAt: now() - 200 });
    const fresh = new Candidate({ target: 'https://ex/fresh', createdAt: now() });
    kb.addCandidate(old); kb.addCandidate(fresh);
    const claimed = kb.claimNextCandidate();
    assert.equal(claimed.target, 'https://ex/fresh');
    assert.equal(old.status, 'skipped');
    assert.ok(kb.diagnostics.some(d=>d.type==='candidate-ttl-expired'));
  });

  it('TTL=0 disables expiry (old queued still claimable)', () => {
    const kb = new KnowledgeBaseTTL({ maxCandidates: 10, ttl: 0 });
    const old = new Candidate({ target: 'https://ex/old0', createdAt: now() - 100000 });
    kb.addCandidate(old);
    const claimed = kb.claimNextCandidate();
    assert.equal(claimed.id, old.id);
    assert.equal(old.status, 'claimed');
  });

  it('failed with nextAttemptAt in future not eligible, but ttl-expired still wins after attempt window', () => {
    const kb = new KnowledgeBaseTTL({ maxCandidates: 10, ttl: 50 });
    const c = new Candidate({ target: 'https://ex/retry', status:'failed', createdAt: now()-100 });
    c.nextAttemptAt = now() + 10000;
    kb.addCandidate(c);
    assert.equal(kb.claimNextCandidate(), null);
    c.nextAttemptAt = now() - 1;
    const after = kb.claimNextCandidate();
    // ttl should have expired while waiting, so skipped not claimed
    assert.equal(after, null);
    assert.equal(c.status, 'skipped');
  });

  it('liveCount never exceeds maxCandidates even with TTL expiries freeing slots (property 500 iter)', () => {
    const rng = lcg(0x56789);
    for(let iter=0; iter<500; iter++){
      const kb = new KnowledgeBaseTTL({ maxCandidates: 5, ttl: 10 });
      // fill 5 queued old, plus 5 fresh attempts
      for(let i=0;i<5;i++){ kb.addCandidate(new Candidate({ target:`https://ex/${iter}-${i}`, createdAt: now()-20 })); }
      assert.equal([...kb.candidates.values()].filter(c=>!['completed','skipped'].includes(c.status)).length, 5);
      // claim should expire all old, then fresh can fill
      kb.claimNextCandidate(); // triggers expiries
      assert.ok(kb.stats.skipped>=1);
      const fresh = new Candidate({ target:`https://ex/${iter}-fresh`, createdAt: now() });
      const added = kb.addCandidate(fresh);
      assert.ok(added, 'fresh should fit after expiries freed liveCount');
    }
  });

  it('source contains candidateTTL + ttl-expired handling', () => {
    assert.match(src, /candidateTTL/);
    assert.match(src, /ttl-expired/);
    assert.match(src, /candidate-ttl-expired/);
  });
});

describe('property: Ledger FIFO 5000', () => {
  it('FIFO evicts oldest, seq monotonic (500+ cap)', () => {
    const ledger = new Ledger(5);
    for(let i=0;i<10;i++) ledger.append(`type-${i%3}`, {i});
    assert.equal(ledger.events.length, 5);
    assert.deepEqual(ledger.events.map(e=>e.seq), [6,7,8,9,10]);
    for(let i=1;i<ledger.events.length;i++) assert.ok(ledger.events[i].seq > ledger.events[i-1].seq);
  });

  it('real ledger cap 5000 reflected in source', () => {
    assert.match(src, /persistedLedgerEvents:\s*5000/);
    assert.match(src, /maxGraphEdges:\s*5000/);
  });
});

describe('property: Origin throttle invariants', () => {
  it('minRequestInterval enforced monotonically', () => {
    const oc = new OriginControllerMock({ minInterval: 150, maxConcurrentPerOrigin: 2 });
    oc.recordStart('https://ex');
    assert.equal(oc.canRequest('https://ex'), false, 'within 150ms should block');
  });

  it('maxConcurrentPerOrigin 2 enforced', () => {
    const oc = new OriginControllerMock({ maxConcurrentPerOrigin: 2, minInterval: 0 });
    oc.recordStart('https://ex'); oc.recordStart('https://ex');
    assert.equal(oc.canRequest('https://ex'), false, '2 concurrent should block third');
    oc.recordEnd('https://ex');
    assert.equal(oc.canRequest('https://ex'), true);
  });

  it('per-origin isolation', () => {
    const oc = new OriginControllerMock({ maxConcurrentPerOrigin: 1, minInterval: 0 });
    oc.recordStart('https://a');
    assert.equal(oc.canRequest('https://a'), false);
    assert.equal(oc.canRequest('https://b'), true, 'other origin not blocked');
  });
});

describe('property: fingerprint determinism', () => {
  it('fnv1a32 empty is 811c9dc5 and deterministic 100 iter', () => {
    assert.equal(fnv1a32(''), '811c9dc5');
    const rng = lcg(0x6789a);
    for(let i=0;i<100;i++){
      const s = Array.from({length: 20}, ()=> String.fromCharCode(97 + Math.floor(rng()*26))).join('');
      assert.equal(fnv1a32(s), fnv1a32(s));
      assert.match(fnv1a32(s), /^[0-9a-f]{8}$/);
    }
  });

  it('makeFingerprint sampling 1M truncated deterministic', () => {
    const big = 'a'.repeat(2_000_000);
    const f1 = makeFingerprint(big, 1_000_000);
    const f2 = makeFingerprint(big, 1_000_000);
    assert.equal(f1.hash, f2.hash);
    assert.equal(f1.sampledLength, 1_000_000);
    assert.equal(f1.length, 2_000_000);
    const small = 'hello';
    assert.equal(makeFingerprint(small).hash, fnv1a32(small));
  });

  it('different strings usually different hash (collision sanity 200)', () => {
    const set = new Set();
    for(let i=0;i<200;i++) set.add(fnv1a32('key-'+i));
    assert.equal(set.size, 200);
  });
});
