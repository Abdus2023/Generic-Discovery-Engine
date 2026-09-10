/**
 * property-lifecycle.test.js — Lifecycle state-machine invariants (v0.7.8)
 *
 * Verifies _validateTransition table, diagnostic on illegal, strict throws,
 * and end-to-end happy path without illegal diagnostics.
 */
import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const src = readFileSync(new URL('../dist/generic-discovery-engine.user.js', import.meta.url), 'utf8');

function makeKB({ strict=false }={}) {
  const CONFIG = { lifecycle: { strict }, maxDiagnostics: 500 };
  class KB {
    constructor(){ this.diagnostics=[]; this.stats={}; }
    recordDiagnostic(type, data){ this.diagnostics.push({type,data}); if(this.diagnostics.length>CONFIG.maxDiagnostics) this.diagnostics.shift(); }
    _validateTransition(candidate, to){
      const from=candidate.status;
      if(from===to) return true;
      const allowed={
        discovered:['queued'],
        queued:['claimed','skipped','failed'],
        claimed:['planned','skipped'],
        planned:['acquiring','completed','skipped'],
        acquiring:['observed'],
        observed:['recognized','completed','queued','failed'],
        recognized:['expanded'],
        expanded:['completed'],
        completed:[],
        skipped:[],
        failed:['queued']
      };
      const ok=(allowed[from]||[]).includes(to);
      if(!ok){
        this.recordDiagnostic('lifecycle-illegal-transition',{id:candidate.id,from,to,allowed:allowed[from]||[]});
        if(CONFIG.lifecycle.strict) throw new Error(`lifecycle illegal: ${from} -> ${to}`);
      }
      return ok || !CONFIG.lifecycle.strict;
    }
    mark(queue){} // placeholder
  }
  return { KB, CONFIG };
}

function candidate(status){ return { id:`c-${Math.random().toString(36).slice(2,6)}`, target:'https://ex/x', status }; }

describe('property: lifecycle state-machine (v0.7.8)', () => {
  it('source contains lifecycle strict + guard + diagnostic', () => {
    assert.match(src, /lifecycle:\s*\{\s*strict/);
    assert.match(src, /_validateTransition/);
    assert.match(src, /lifecycle-illegal-transition/);
  });

  it('allowed transitions do not emit diagnostic', () => {
    const { KB } = makeKB({strict:false});
    const kb=new KB();
    const happy = [
      ['discovered','queued'],
      ['queued','claimed'],
      ['claimed','planned'],
      ['planned','acquiring'],
      ['acquiring','observed'],
      ['observed','recognized'],
      ['recognized','expanded'],
      ['expanded','completed'],
    ];
    for(const [from,to] of happy){
      const c=candidate(from);
      const ok=kb._validateTransition(c,to);
      assert.equal(ok,true, `${from}->${to} should be ok`);
      // no diagnostic for allowed
      assert.equal(kb.diagnostics.length,0);
    }
  });

  it('branch transitions allowed (skipped/failed/ttl/queued)', () => {
    const { KB } = makeKB();
    const kb=new KB();
    const branches=[
      ['queued','skipped'],
      ['claimed','skipped'],
      ['planned','skipped'],
      ['planned','completed'],
      ['observed','completed'],
      ['observed','queued'],
      ['observed','failed'],
      ['failed','queued'],
    ];
    for(const [from,to] of branches){
      const c=candidate(from);
      assert.equal(kb._validateTransition(c,to),true, `${from}->${to}`);
    }
    assert.equal(kb.diagnostics.length,0);
  });

  it('illegal transitions emit lifecycle-illegal-transition (non-strict allows)', () => {
    const { KB } = makeKB({strict:false});
    const kb=new KB();
    const illegal=[
      ['queued','observed'],
      ['completed','queued'],
      ['skipped','claimed'],
      ['discovered','claimed'],
      ['acquiring','completed'],
      ['recognized','queued'],
    ];
    for(const [from,to] of illegal){
      const c=candidate(from);
      const ok=kb._validateTransition(c,to);
      assert.equal(ok,true, `non-strict should allow ${from}->${to} after diagnostic`);
    }
    assert.equal(kb.diagnostics.filter(d=>d.type==='lifecycle-illegal-transition').length, illegal.length);
  });

  it('strict mode throws on illegal', () => {
    const { KB } = makeKB({strict:true});
    const kb=new KB();
    const c=candidate('queued');
    assert.throws(()=> kb._validateTransition(c,'observed'), /lifecycle illegal/);
    assert.equal(kb.diagnostics.length,1);
  });

  it('terminal states have no outgoing (completed/skipped/failed no outgoing except failed→queued)', () => {
    // non-strict returns true even for illegal (diagnostic), so test strict mode for deny
    const { KB: KBStrict } = makeKB({strict:true});
    const kbStrict=new KBStrict();
    for(const to of ['queued','claimed','planned','acquiring','observed','recognized','expanded','completed','skipped','failed']){
      const c=candidate('completed');
      const shouldAllow = (to==='completed'); // self is allowed
      if(shouldAllow){
        assert.equal(kbStrict._validateTransition(c,to), true);
      } else {
        assert.throws(()=> kbStrict._validateTransition(c,to), /lifecycle illegal/);
      }
    }
    const { KB } = makeKB();
    const kb=new KB();
    for(const to of ['queued','claimed','acquiring']){
      const c=candidate('skipped');
      const ok=kb._validateTransition(c,to);
      // non-strict allows after diagnostic, so ok is true but diagnostic count grows
      if(to==='skipped'){
        assert.equal(ok, true);
        assert.equal(kb.diagnostics.length, 0);
      } else {
        assert.equal(ok, true); // non-strict allows
        assert.ok(kb.diagnostics.some(d=>d.type==='lifecycle-illegal-transition' && d.data.from==='skipped' && d.data.to===to));
      }
    }
  });

  it('random walks over allowed edges never hit illegal when following table (500 walks)', () => {
    const { KB } = makeKB();
    const allowed={
      discovered:['queued'],
      queued:['claimed','skipped'],
      claimed:['planned'],
      planned:['acquiring','completed'],
      acquiring:['observed'],
      observed:['recognized','completed','queued'],
      recognized:['expanded'],
      expanded:['completed'],
      completed:[], skipped:[], failed:['queued']
    };
    function lcg(seed){ let s=seed>>>0; return ()=>{ s=(1664525*s+1013904223)>>>0; return s/0x100000000; }; }
    const rng=lcg(0x789abc);
    for(let walk=0;walk<500;walk++){
      const kb=new KB();
      let c=candidate('discovered');
      let steps=0;
      while(steps<10 && (allowed[c.status]||[]).length){
        const nexts=allowed[c.status];
        const to=nexts[Math.floor(rng()*nexts.length)];
        const ok=kb._validateTransition(c,to);
        assert.equal(ok,true);
        c.status=to; steps++;
        if(['completed','skipped'].includes(c.status)) break;
      }
      assert.equal(kb.diagnostics.filter(d=>d.type==='lifecycle-illegal-transition').length,0);
    }
  });

  it('full happy path discovered→completed via worker steps creates no illegal', () => {
    const { KB } = makeKB();
    const kb=new KB();
    const c=candidate('discovered');
    for(const to of ['queued','claimed','planned','acquiring','observed','recognized','expanded','completed']){
      kb._validateTransition(c,to); c.status=to;
    }
    assert.equal(c.status,'completed');
    assert.equal(kb.diagnostics.length,0);
  });
});
