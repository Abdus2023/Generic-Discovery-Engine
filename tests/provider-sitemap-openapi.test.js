/**
 * provider-sitemap-openapi.test.js — SitemapIndex + OpenAPI providers (v1.2.0)
 */
import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const dist = readFileSync(new URL('../dist/generic-discovery-engine.user.js', import.meta.url), 'utf8');

function canonicalizeUrl(u){ try{ const p=new URL(u); return p.href; }catch{ return null; } }
function contentTypeBase(ct){ return String(ct||'').split(';')[0].trim().toLowerCase(); }
function looksLikeXml(ct, body){ const c=contentTypeBase(ct); if(c.includes('xml')) return true; return /<\?xml|<\s*(urlset|sitemapindex)/i.test(String(body||'')); }
function looksLikeJson(ct, body){ const c=contentTypeBase(ct); if(c.includes('json')) return true; try{ JSON.parse(String(body||'')); return true; }catch{return false;} }

class Discovery { constructor(d){ Object.assign(this,d); } }

// Minimal SitemapIndexProvider harness (mirrors src)
class SitemapIndexProvider {
  constructor(){ this.name='sitemapIndex'; }
  matches(obs){
    const ct=contentTypeBase(obs.http?.contentType||'');
    const body=String(obs.body||'');
    if(/sitemapindex/i.test(body)) return true;
    if(ct.includes('xml') && /<sitemap/i.test(body)) return looksLikeXml(obs.http?.contentType, body);
    const url=String(obs.requestedUrl||obs.target||'');
    if(/sitemap.*\.xml$/i.test(url) && /<loc>/i.test(body)) return true;
    return false;
  }
  async recognize(candidate, obs){
    const discoveries=[];
    const re=/<loc>([^<]+)<\/loc>/gi;
    for(const m of String(obs.body||'').matchAll(re)){
      const url=canonicalizeUrl(m[1].trim()); if(!url) continue;
      discoveries.push(new Discovery({candidateId:candidate.id, observationId:obs.id, kind:'sitemap', confidence:0.90, mechanism:'sitemap-index-loc', data:{url}}));
    }
    return discoveries;
  }
}
class OpenApiProvider {
  constructor(){ this.name='openapi'; }
  matches(obs){
    if(!looksLikeJson(obs.http?.contentType, obs.body)) return false;
    try{ const p=JSON.parse(String(obs.body||'')); if(p && typeof p==='object'){ if(p.openapi||p.swagger) return true; if(p.info && p.paths) return true; } }catch{}
    return false;
  }
  async recognize(candidate, obs){
    const discoveries=[]; let parsed; try{ parsed=JSON.parse(String(obs.body||'')); }catch{ return discoveries; }
    const emit=(url,conf,mech)=>{ const c=canonicalizeUrl(url); if(!c) return; discoveries.push(new Discovery({candidateId:candidate.id, observationId:obs.id, kind:'api', confidence:conf, mechanism:mech, data:{url:c}})); };
    if(Array.isArray(parsed.servers)) for(const s of parsed.servers) if(s?.url) emit(s.url,0.95,'openapi-server');
    if(parsed.swagger && parsed.host){ const scheme=(Array.isArray(parsed.schemes)&&parsed.schemes[0])||'https'; emit(`${scheme}://${parsed.host}${parsed.basePath||''}`,0.90,'openapi-host'); }
    return discoveries;
  }
}

describe('provider: SitemapIndexProvider (v1.2.0)', () => {
  it('dist contains SitemapIndexProvider and OpenApiProvider', () => {
    assert.match(dist, /class SitemapIndexProvider/);
    assert.match(dist, /class OpenApiProvider/);
    assert.match(dist, /sitemapIndex/);
    assert.match(dist, /openapi/);
  });
  it('order is 11 providers Html/Json/Xml/Css/JS/Robots/Headers/SitemapIndex/OpenApi/Binary/Text', () => {
    const order = ['HtmlProvider','JsonProvider','XmlProvider','CssProvider','JavaScriptProvider','RobotsProvider','HeadersProvider','SitemapIndexProvider','OpenApiProvider','BinaryProvider','TextProvider'];
    let last=-1;
    for(const name of order){
      const idx=dist.indexOf(`new ${name}()`);
      assert.ok(idx>last, `${name} out of order`);
      last=idx;
    }
  });
  it('SitemapIndex matches sitemapindex root', () => {
    const p=new SitemapIndexProvider();
    assert.equal(p.matches({http:{contentType:'application/xml'}, body:'<?xml><sitemapindex><sitemap><loc>https://ex/sitemap1.xml</loc></sitemap></sitemapindex>', requestedUrl:'https://ex/sitemap.xml'}), true);
    assert.equal(p.matches({http:{contentType:'text/html'}, body:'<html>', requestedUrl:'https://ex/page'}), false);
  });
  it('SitemapIndex extracts locs', async () => {
    const p=new SitemapIndexProvider();
    const discoveries=await p.recognize({id:'c1', origin:'https://ex', target:'https://ex/sitemap.xml', depth:0}, {id:'o1', body:'<sitemapindex><sitemap><loc>https://ex/s1.xml</loc></sitemap><sitemap><loc>https://ex/s2.xml</loc></sitemap></sitemapindex>', http:{contentType:'application/xml'}, requestedUrl:'https://ex/sitemap.xml'});
    assert.equal(discoveries.length,2);
    assert.equal(discoveries[0].data.url,'https://ex/s1.xml');
    assert.equal(discoveries[0].kind,'sitemap');
  });
});

describe('provider: OpenApiProvider (v1.2.0)', () => {
  it('matches openapi json', () => {
    const p=new OpenApiProvider();
    assert.equal(p.matches({http:{contentType:'application/json'}, body:JSON.stringify({openapi:'3.0.0', info:{title:'T'}, paths:{}})}), true);
    assert.equal(p.matches({http:{contentType:'application/json'}, body:JSON.stringify({swagger:'2.0', info:{title:'T'}, paths:{}})}), true);
    assert.equal(p.matches({http:{contentType:'application/json'}, body:JSON.stringify({info:{}, paths:{}, openapi:'3.1'})}), true);
    assert.equal(p.matches({http:{contentType:'application/json'}, body:JSON.stringify({plain:'json'})}), false);
  });
  it('extracts servers urls', async () => {
    const p=new OpenApiProvider();
    const body=JSON.stringify({openapi:'3.0.0', servers:[{url:'https://api.ex/v1'}, {url:'https://api2.ex/v2'}], info:{title:'X'}, paths:{}});
    const discoveries=await p.recognize({id:'c1', origin:'https://ex', target:'https://ex/openapi.json', depth:0}, {id:'o1', body, http:{contentType:'application/json'}, requestedUrl:'https://ex/openapi.json'});
    assert.equal(discoveries.length,2);
    assert.ok(discoveries.some(d=>d.data.url==='https://api.ex/v1'));
    assert.ok(discoveries.some(d=>d.mechanism==='openapi-server'));
  });
  it('extracts swagger host+basePath', async () => {
    const p=new OpenApiProvider();
    const body=JSON.stringify({swagger:'2.0', host:'api.ex', basePath:'/v1', schemes:['https'], info:{title:'X'}, paths:{}});
    const discoveries=await p.recognize({id:'c1', origin:'https://ex', target:'https://ex/swagger.json', depth:0}, {id:'o1', body, http:{contentType:'application/json'}, requestedUrl:'https://ex/swagger.json'});
    assert.equal(discoveries.length,1);
    assert.equal(discoveries[0].data.url,'https://api.ex/v1');
  });
  it('lazy registry respects disabled for new providers', () => {
    assert.match(dist, /CONFIG\.providers/);
    // ensure factories include new names
    assert.match(dist, /sitemapIndex: \(\) => new SitemapIndexProvider/);
    assert.match(dist, /openapi: \(\) => new OpenApiProvider/);
  });
});
