/**
 * provider-robots-headers.test.js — Robots/Headers providers + change detection (v0.8.0)
 */
import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const src = readFileSync(new URL('../dist/generic-discovery-engine.user.js', import.meta.url), 'utf8');

function canonicalizeUrl(u){ try{ const p=new URL(u); return p.href; }catch{ return null; } }
function contentTypeBase(ct){ return String(ct||'').split(';')[0].trim().toLowerCase(); }
function isAllowedUrl(u){ try{ const p=new URL(u); return /^https?:$/.test(p.protocol); }catch{ return false; } }

class Discovery { constructor(d){ Object.assign(this,d); } }

class RobotsProvider {
  matches(obs){ const url=String(obs.requestedUrl||obs.target||''); if(/robots\.txt$/i.test(url)) return true; const ct=contentTypeBase(obs.http?.contentType||''); return ct==='text/plain' && /User-agent:/i.test(String(obs.body||'')); }
  async recognize(candidate, obs){
    const discoveries=[]; const re=/Sitemap:\s*(https?:\/\/\S+)/gi;
    for(const m of String(obs.body||'').matchAll(re)){
      const url=canonicalizeUrl(m[1].trim()); if(!url) continue;
      discoveries.push(new Discovery({candidateId:candidate.id, observationId:obs.id, kind:'sitemap', confidence:0.92, mechanism:'robots-sitemap', data:{url}}));
    }
    return discoveries;
  }
}
class HeadersProvider {
  matches(obs){
    const h=obs.http?.headers; if(!h||typeof h!=='object') return false;
    const link=h['link']||h['Link']||h['LINK']; if(link && /<https?:\/\/[^>]+>/.test(String(link))) return true;
    const loc=h['location']||h['Location']||h['LOCATION']; if(loc && isAllowedUrl(String(loc))) return true; return false;
  }
  async recognize(candidate, obs){
    const discoveries=[]; const h=obs.http?.headers||{};
    const emit=(url,type,mech,conf)=>{ const c=canonicalizeUrl(url); if(!c) return; discoveries.push(new Discovery({candidateId:candidate.id, observationId:obs.id, kind:type, confidence:conf, mechanism:mech, data:{url:c}})); };
    const linkVal=String(h['link']||h['Link']||h['LINK']||''); const re=/<([^>]+)>/g; for(const m of linkVal.matchAll(re)) emit(m[1].trim(),'url','headers-link',0.88);
    const loc=h['location']||h['Location']||h['LOCATION']; if(loc) emit(String(loc).trim(),'url','headers-location',0.90);
    return discoveries;
  }
}

// Minimal KB for change detection
function fnv1a32(s){ let h=0x811c9dc5; for(let i=0;i<s.length;i++){ h^=s.charCodeAt(i); h=Math.imul(h,0x01000193)>>>0;} return (h>>>0).toString(16).padStart(8,'0'); }
function makeFingerprint(b){ const s=String(b||'').slice(0,1000000).replace(/\s+/g,' ').trim(); return {hash:fnv1a32(s)}; }
class KBChange {
  constructor(){ this.resources=new Map(); this.diagnostics=[]; }
  recordDiagnostic(t,d){ this.diagnostics.push({type:t,data:d}); }
  ensureResource(url){ if(!this.resources.has(url)) this.resources.set(url,{fingerprint:null,status:'unknown'}); return this.resources.get(url); }
  recordObservation(obs){
    const canon=obs.requestedUrl;
    const prev=this.resources.get(canon)?.fingerprint?.hash||null;
    const res=this.ensureResource(canon);
    res.fingerprint=obs.fingerprint;
    // fingerprintIndex not needed for this test
    if(prev && obs.fingerprint && prev!==obs.fingerprint.hash){
      this.recordDiagnostic('resource-changed',{target:canon, oldHash:prev, newHash:obs.fingerprint.hash});
      res.status='changed';
    } else {
      res.status='acquired';
    }
  }
}

describe('provider: RobotsProvider (v0.8.0)', () => {
  it('source contains RobotsProvider and Sitemap extraction', () => {
    assert.match(src, /class RobotsProvider/);
    assert.match(src, /robots-sitemap/);
    assert.match(src, /Sitemap:\\s\*\(https/);
  });
  it('matches robots.txt URL', () => {
    const p=new RobotsProvider();
    assert.equal(p.matches({requestedUrl:'https://ex/robots.txt', http:{contentType:'text/plain'}, body:'User-agent: *'}), true);
    assert.equal(p.matches({requestedUrl:'https://ex/page', http:{contentType:'text/html'}, body:'<html>'}), false);
  });
  it('matches text/plain with User-agent', () => {
    const p=new RobotsProvider();
    assert.equal(p.matches({requestedUrl:'https://ex/file.txt', http:{contentType:'text/plain; charset=utf-8'}, body:'User-agent: *\nDisallow: /private\nSitemap: https://ex/sitemap.xml'}), true);
  });
  it('extracts Sitemap URLs', async () => {
    const p=new RobotsProvider();
    const obs={id:'obs1', requestedUrl:'https://ex/robots.txt', body:'Sitemap: https://ex/sitemap.xml\nSitemap: https://ex/other.xml', http:{contentType:'text/plain'}};
    const ds=await p.recognize({id:'c1', target:'https://ex/robots.txt', origin:'https://ex'}, obs);
    assert.equal(ds.length,2);
    assert.equal(ds[0].data.url,'https://ex/sitemap.xml');
    assert.equal(ds[1].data.url,'https://ex/other.xml');
    assert.equal(ds[0].kind,'sitemap');
  });
});

describe('provider: HeadersProvider (v0.8.0)', () => {
  it('source contains HeadersProvider and Link/Location', () => {
    assert.match(src, /class HeadersProvider/);
    assert.match(src, /headers-link/);
    assert.match(src, /headers-location/);
  });
  it('matches Link header', () => {
    const p=new HeadersProvider();
    assert.equal(p.matches({http:{headers:{link:'<https://ex/next>; rel="next"'}}}) , true);
    assert.equal(p.matches({http:{headers:{}}}) , false);
  });
  it('matches Location header', () => {
    const p=new HeadersProvider();
    assert.equal(p.matches({http:{headers:{location:'https://ex/redirect'}}}) , true);
    assert.equal(p.matches({http:{headers:{link:'<https://ex/a>'}}}) , true);
  });
  it('extracts Link and Location URLs', async () => {
    const p=new HeadersProvider();
    const obs={id:'obs1', http:{headers:{link:'<https://ex/next>; rel="next", <https://ex/prev>; rel="prev"', location:'https://ex/final'}}};
    const ds=await p.recognize({id:'c1', target:'https://ex/page', origin:'https://ex'}, obs);
    assert.equal(ds.length,3);
    assert.ok(ds.some(d=>d.data.url==='https://ex/next'));
    assert.ok(ds.some(d=>d.data.url==='https://ex/final'));
  });
});

describe('acquisition: http.headers captured (v0.8.0)', () => {
  it('source captures headers in both GM_xhr and fetch', () => {
    assert.match(src, /headers: Object\.fromEntries/);
    assert.match(src, /response\.responseHeaders/);
    assert.match(src, /headers: \(\(\) => \{/);
  });
});

describe('change detection (v0.8.0)', () => {
  it('source contains changeDetection + resource-changed', () => {
    assert.match(src, /changeDetection/);
    assert.match(src, /resource-changed/);
    assert.match(src, /_oldHash/);
  });
  it('emits resource-changed when fingerprint hash differs', () => {
    const kb=new KBChange();
    const obs1={requestedUrl:'https://ex/page', fingerprint:makeFingerprint('hello')};
    kb.recordObservation(obs1);
    assert.equal(kb.diagnostics.length,0);
    assert.equal(kb.resources.get('https://ex/page').status,'acquired');
    const obs2={requestedUrl:'https://ex/page', fingerprint:makeFingerprint('hello world')};
    kb.recordObservation(obs2);
    assert.equal(kb.diagnostics.length,1);
    assert.equal(kb.diagnostics[0].type,'resource-changed');
    assert.equal(kb.resources.get('https://ex/page').status,'changed');
    assert.notEqual(kb.diagnostics[0].data.oldHash, kb.diagnostics[0].data.newHash);
  });
  it('no diagnostic when hash same', () => {
    const kb=new KBChange();
    const f=makeFingerprint('same');
    kb.recordObservation({requestedUrl:'https://ex/a', fingerprint:f});
    kb.recordObservation({requestedUrl:'https://ex/a', fingerprint:f});
    assert.equal(kb.diagnostics.length,0);
  });
});
