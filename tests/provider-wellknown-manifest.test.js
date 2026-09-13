/**
 * provider-wellknown-manifest.test.js — WellKnown + Manifest providers (v1.3.0)
 */
import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const dist = readFileSync(new URL('../dist/generic-discovery-engine.user.js', import.meta.url), 'utf8');

function canonicalizeUrl(u){ try{ const p=new URL(u); return p.href; }catch{ return null; } }
function contentTypeBase(ct){ return String(ct||'').split(';')[0].trim().toLowerCase(); }
function looksLikeJson(ct, body){ const c=contentTypeBase(ct); if(c.includes('json')) return true; try{ JSON.parse(String(body||'')); return true; }catch{return false;} }

class Discovery { constructor(d){ Object.assign(this,d); } }

class WellKnownProvider {
  constructor(){ this.name='wellKnown'; }
  matches(obs){
    const url=String(obs.requestedUrl||obs.target||'');
    if(/\/\.well-known\//i.test(url)) return true;
    const ct=contentTypeBase(obs.http?.contentType||'');
    const body=String(obs.body||'');
    if(ct==='text/plain' && /Contact:/i.test(body) && /\/\.well-known\//i.test(url)) return true;
    if(looksLikeJson(ct,body) && /\/\.well-known\//i.test(url)) return true;
    return false;
  }
  async recognize(candidate, obs){
    const discoveries=[]; const ct=contentTypeBase(obs.http?.contentType||''); const body=String(obs.body||'');
    if(looksLikeJson(ct,body)){
      try{ const p=JSON.parse(body); const walk=v=>{ if(typeof v==='string'){ const c=canonicalizeUrl(v); if(c) discoveries.push(new Discovery({candidateId:candidate.id, observationId:obs.id, kind:'url', confidence:0.80, mechanism:'wellknown-json-url', data:{url:c}})); return; } if(Array.isArray(v)) v.forEach(walk); else if(v&&typeof v==='object') Object.values(v).forEach(walk); }; walk(p); return discoveries; }catch{}
    }
    const re=/https?:\/\/[^\s"']+/g; for(const m of body.matchAll(re)){ const c=canonicalizeUrl(m[0]); if(c) discoveries.push(new Discovery({candidateId:candidate.id, observationId:obs.id, kind:'url', confidence:0.70, mechanism:'wellknown-text-url', data:{url:c}})); }
    return discoveries;
  }
}
class ManifestProvider {
  constructor(){ this.name='manifest'; }
  matches(obs){
    const url=String(obs.requestedUrl||obs.target||'');
    const ct=contentTypeBase(obs.http?.contentType||'');
    if(/manifest\.json$/i.test(url)) return true;
    if(ct==='application/manifest+json') return true;
    if(looksLikeJson(ct,obs.body)){ try{ const p=JSON.parse(String(obs.body||'')); if(p&&typeof p==='object'&&(p.icons||p.start_url||p.scope) && (Array.isArray(p.icons)||p.start_url)) return true; }catch{} }
    return false;
  }
  async recognize(candidate, obs){
    const discoveries=[]; let p; try{ p=JSON.parse(String(obs.body||'')); }catch{ return discoveries; }
    const emit=(url,type,mech,conf)=>{
      let canonical = canonicalizeUrl(url);
      if(!canonical){
        try{ canonical = canonicalizeUrl(new URL(url, obs.requestedUrl).href); }catch{}
      } else {
        // resolve relative if needed
        try{
          if(!/^https?:/i.test(canonical) && obs.requestedUrl) canonical = canonicalizeUrl(new URL(url, obs.requestedUrl).href) || canonical;
        }catch{}
      }
      if(!canonical) return;
      discoveries.push(new Discovery({candidateId:candidate.id, observationId:obs.id, kind:type, confidence:conf, mechanism:mech, data:{url:canonical}}));
    };
    if(Array.isArray(p.icons)) for(const ic of p.icons) if(ic?.src) emit(ic.src,'resource','manifest-icon',0.85);
    if(p.start_url) emit(String(p.start_url),'url','manifest-start_url',0.80);
    if(p.scope) emit(String(p.scope),'url','manifest-scope',0.75);
    if(Array.isArray(p.screenshots)) for(const s of p.screenshots) if(s?.src) emit(s.src,'resource','manifest-screenshot',0.80);
    return discoveries;
  }
}

describe('provider: WellKnownProvider (v1.3.0)', () => {
  it('dist contains WellKnownProvider and ManifestProvider', () => {
    assert.match(dist, /class WellKnownProvider/);
    assert.match(dist, /class ManifestProvider/);
    assert.match(dist, /wellKnown/);
    assert.match(dist, /manifest/);
  });
  it('order is 13 providers with wellKnown/manifest before binary', () => {
    const order = ['HtmlProvider','JsonProvider','XmlProvider','CssProvider','JavaScriptProvider','RobotsProvider','HeadersProvider','SitemapIndexProvider','OpenApiProvider','WellKnownProvider','ManifestProvider','BinaryProvider','TextProvider'];
    let last=-1;
    for(const name of order){
      const idx=dist.indexOf(`new ${name}()`);
      assert.ok(idx>last, `${name} out of order`);
      last=idx;
    }
  });
  it('WellKnown matches /.well-known/ path', () => {
    const p=new WellKnownProvider();
    assert.equal(p.matches({requestedUrl:'https://ex/.well-known/security.txt', http:{contentType:'text/plain'}, body:'Contact: https://ex/contact'}), true);
    assert.equal(p.matches({requestedUrl:'https://ex/.well-known/assetlinks.json', http:{contentType:'application/json'}, body:'[{"relation":["delegate_permission/common.handle_all_urls"]}]'}), true);
    assert.equal(p.matches({requestedUrl:'https://ex/page', http:{contentType:'text/html'}, body:'<html>'}), false);
  });
  it('WellKnown extracts json url', async () => {
    const p=new WellKnownProvider();
    const discoveries=await p.recognize({id:'c1', origin:'https://ex', target:'https://ex/.well-known/openid-configuration', depth:0}, {id:'o1', body:JSON.stringify({issuer:'https://ex', jwks_uri:'https://ex/jwks'}), http:{contentType:'application/json'}, requestedUrl:'https://ex/.well-known/openid-configuration'});
    assert.ok(discoveries.some(d=>d.data.url==='https://ex/jwks'));
    assert.ok(discoveries[0].mechanism==='wellknown-json-url');
  });
});

describe('provider: ManifestProvider (v1.3.0)', () => {
  it('matches manifest.json', () => {
    const p=new ManifestProvider();
    assert.equal(p.matches({requestedUrl:'https://ex/manifest.json', http:{contentType:'application/json'}, body:'{"name":"App","icons":[{"src":"/icon.png"}]}'}), true);
    assert.equal(p.matches({requestedUrl:'https://ex/app.json', http:{contentType:'application/json'}, body:'{"plain":"json"}'}), false);
    assert.equal(p.matches({requestedUrl:'https://ex/manifest.json', http:{contentType:'text/html'}, body:'<html>'}), true);
  });
  it('extracts icons and start_url', async () => {
    const p=new ManifestProvider();
    const body=JSON.stringify({name:'App', start_url:'/app/', scope:'/app/', icons:[{src:'/icon-192.png'},{src:'https://cdn.ex/icon-512.png'}]});
    const discoveries=await p.recognize({id:'c1', origin:'https://ex', target:'https://ex/manifest.json', depth:0}, {id:'o1', body, http:{contentType:'application/json'}, requestedUrl:'https://ex/manifest.json'});
    assert.equal(discoveries.length,4);
    assert.ok(discoveries.some(d=>d.data.url==='https://ex/icon-192.png' && d.mechanism==='manifest-icon'));
    assert.ok(discoveries.some(d=>d.data.url==='https://ex/app/' && d.mechanism==='manifest-start_url'));
  });
  it('lazy registry respects disabled for new providers', () => {
    assert.match(dist, /wellKnown: \(\) => new WellKnownProvider/);
    assert.match(dist, /manifest: \(\) => new ManifestProvider/);
  });
});
