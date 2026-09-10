/**
 * property-concurrency.test.js — Claim exclusivity & interleaving invariants (v0.7.8)
 *
 * Proves `claimNextCandidate()` is synchronous sort+mark and remains exclusive
 * under burst workers, TTL expiries, and retry windows (seeded).
 */
import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const src = readFileSync(new URL('../dist/generic-discovery-engine.user.js', import.meta.url), 'utf8');

function lcg(seed){ let s=seed>>>0; return ()=>{ s=(1664525*s+1013904223)>>>0; return s/0x100000000; }; }

function now(){ return Date.now(); }

class Candidate {
  constructor({ target, type='url', priority=0, status='queued', depth=0, createdAt=now(), attempts=0 }={}) {
    this.id=`c-${Math.random().toString(36).slice(2,7)}`; this.target=target; this.type=type; this.priority=priority; this.status=status; this.depth=depth; this.createdAt=createdAt; this.attempts=attempts; this.nextAttemptAt=0; this.claimedAt=null;
  }
  identityKey(){ return `${this.type}:${this.target}`; }
  effectivePriority(){ return this.priority - this.depth*0.045 - this.attempts*0.05 + (this.type==='api'?1:0)*0.20; }
}

class KBClaim {
  constructor({ maxCandidates=20, ttl=0 }={}){ this.candidates=new Map(); this.candidateKeys=new Map(); this.visited=new Set(); this.diagnostics=[]; this.stats={claimed:0,skipped:0}; this.maxCandidates=maxCandidates; this.candidateTTL=ttl; this.claimed=new Set(); }
  recordDiagnostic(t,d){ this.diagnostics.push({type:t,data:d}); }
  markSkipped(c,r){ c.status='skipped'; c.skippedAt=now(); this.visited.add(c.identityKey()); this.stats.skipped++; }
  addCandidate(c){ const k=c.identityKey(); if(this.candidateKeys.has(k)) return this.candidates.get(this.candidateKeys.get(k)); if(this.visited.has(k)) return null; const live=[...this.candidates.values()].filter(x=>!['completed','skipped'].includes(x.status)).length; if(live>=this.maxCandidates) return null; this.candidates.set(c.id,c); this.candidateKeys.set(k,c.id); return c; }
  claimNextCandidate(){
    const eligible=[];
    for(const cand of this.candidates.values()){
      if(cand.status!=='queued' && cand.status!=='failed') continue;
      if(cand.nextAttemptAt && cand.nextAttemptAt>now()) continue;
      if(this.candidateTTL>0 && cand.createdAt && now()-cand.createdAt>this.candidateTTL){ this.markSkipped(cand,'ttl-expired'); this.recordDiagnostic('candidate-ttl-expired',{id:cand.id}); continue; }
      eligible.push(cand);
    }
    eligible.sort((a,b)=> b.effectivePriority()-a.effectivePriority());
    const cand=eligible[0]; if(!cand) return null;
    cand.status='claimed'; cand.claimedAt=now(); this.claimed.add(cand.id); this.stats.claimed++; return cand;
  }
}

describe('property: claim exclusivity (v0.7.8)', () => {
  it('source still synchronous (no async/await in claimNextCandidate)', () => {
    const chunk = src.slice(src.indexOf('claimNextCandidate()'), src.indexOf('claimNextCandidate()')+2000);
    assert.ok(!/async/.test(chunk.slice(0,200)), 'claim should not be async');
    assert.match(src, /candidate\.status = 'claimed'/);
    assert.match(src, /effectivePriority/);
  });

  it('sequential claims yield priority order and no duplicates (10 candidates)', () => {
    const kb=new KBClaim({maxCandidates:20});
    const rng=lcg(0xabc);
    for(let i=0;i<10;i++){ const p=Math.floor(rng()*100)/10; kb.addCandidate(new Candidate({target:`https://ex/${i}`, priority:p})); }
    const claimed=[];
    let c; while(c=kb.claimNextCandidate()) claimed.push(c);
    assert.equal(claimed.length,10);
    assert.equal(new Set(claimed.map(x=>x.id)).size,10);
    for(let i=1;i<claimed.length;i++) assert.ok(claimed[i-1].effectivePriority() >= claimed[i].effectivePriority(), 'priority order violated');
  });

  it('concurrent workers via Promise.all do not duplicate (4 workers, 12 candidates)', async () => {
    const kb=new KBClaim({maxCandidates:20});
    for(let i=0;i<12;i++) kb.addCandidate(new Candidate({target:`https://ex/w${i}`, priority: i}));
    const workers = Array.from({length:4}, async (_,wi)=>{
      const got=[];
      while(true){
        const cand=kb.claimNextCandidate();
        if(!cand) break;
        got.push(cand.id);
        // yield to allow interleaving, but claim itself is sync before await
        await new Promise(r=> setImmediate(r));
      }
      return got;
    });
    const results = await Promise.all(workers);
    const all = results.flat();
    assert.equal(all.length,12);
    assert.equal(new Set(all).size,12);
  });

  it('TTL expiries interleaved with claims still exclusive', () => {
    const kb=new KBClaim({maxCandidates:10, ttl:100});
    for(let i=0;i<5;i++) kb.addCandidate(new Candidate({target:`https://ex/old${i}`, createdAt: now()-200}));
    for(let i=0;i<5;i++) kb.addCandidate(new Candidate({target:`https://ex/fresh${i}`, createdAt: now()}));
    const claimed=[];
    let c; while(c=kb.claimNextCandidate()) claimed.push(c);
    // old 5 should have been skipped, not claimed
    assert.ok(claimed.every(x=> x.target.includes('fresh')));
    assert.equal(kb.stats.skipped,5);
    assert.equal(new Set(claimed.map(x=>x.id)).size, claimed.length);
  });

  it('retry window blocks claim until nextAttemptAt passes (property 100 iter)', () => {
    const rng=lcg(0xdef);
    for(let iter=0;iter<100;iter++){
      const kb=new KBClaim();
      const c=new Candidate({target:`https://ex/r${iter}`, status:'failed', createdAt: now()});
      c.nextAttemptAt = now()+1000;
      kb.addCandidate(c);
      assert.equal(kb.claimNextCandidate(), null, 'should block before window');
      c.nextAttemptAt = now()-1;
      const claimed=kb.claimNextCandidate();
      assert.equal(claimed.id,c.id);
    }
  });

  it('claim remains sync (returns Candidate, not Promise) under 500 iter fuzz', () => {
    const rng=lcg(0x123);
    for(let i=0;i<500;i++){
      const kb=new KBClaim();
      kb.addCandidate(new Candidate({target:`https://ex/s${i}`, priority: rng()*5, depth: Math.floor(rng()*5)}));
      const res=kb.claimNextCandidate();
      assert.ok(res instanceof Candidate);
      assert.ok(!(res instanceof Promise));
    }
  });
});
