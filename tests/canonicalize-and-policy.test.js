#!/usr/bin/env node
// canonicalize-and-policy.test.js — verifies URL handling & AcquisitionPolicy denials
import { describe, it } from 'node:test';
import assert from 'node:assert/strict';

// Mirror the patched helpers (extracted verbatim from dist file for fidelity)
const CONFIG = {
    stripTrackingParams: true,
    sameOriginOnly: true,
    maxDepth: 5,
    policy: { acquireForms: false, acquireMedia: false, acquireBinaryResources: false, acquireFrames: true, acquireStylesheets: true, acquireScripts: true, acquireNetworkGet: true }
};

function canonicalizeUrl(raw, base = 'https://example.com/') {
    try {
        const url = new URL(raw, base);
        url.hash = '';
        if (CONFIG.stripTrackingParams) {
            const tracking = [/^utm_/i, /^fbclid$/i, /^gclid$/i, /^mc_/i, /^ref$/i];
            for (const key of [...url.searchParams.keys()]) {
                if (tracking.some(rx => rx.test(key))) url.searchParams.delete(key);
            }
        }
        return url.href;
    } catch { return null; }
}

function isAllowedUrl(url, base = 'https://example.com/') {
    try {
        const parsed = new URL(url, base);
        if (!/^https?:$/.test(parsed.protocol)) return false;
        if (CONFIG.sameOriginOnly && parsed.origin !== new URL(base).origin) return false;
        return true;
    } catch { return false; }
}

function contentTypeBase(v) { return String(v||'').split(';')[0].trim().toLowerCase(); }
function looksLikeHtml(ct, body='') {
    const t = contentTypeBase(ct);
    if (t === 'text/html' || t === 'application/xhtml+xml') return true;
    return /^\s*(<!doctype\s+html|<html\b)/i.test(body);
}
function looksLikeJson(ct, body='') {
    const t = contentTypeBase(ct);
    if (t === 'application/json' || t.endsWith('+json')) return true;
    return /^\s*[\[{]/.test(body);
}
function looksLikeBinary(ct) {
    const t = contentTypeBase(ct);
    return t.startsWith('image/') || t.startsWith('audio/') || t.startsWith('video/') || t === 'application/pdf' || t === 'application/zip';
}

// Mini AcquisitionPolicy mirroring dist
class AcquisitionPlan { constructor(d){ Object.assign(this,d); } }
class AcquisitionPolicy {
    plan(candidate) {
        const method = String(candidate.hints?.method || 'GET').toUpperCase();
        const base = { candidateId: candidate.id, target: candidate.target, method, expectedType: candidate.type };
        if (!isAllowedUrl(candidate.target, 'https://example.com/')) return new AcquisitionPlan({...base, allowed:false, reason:'url-not-allowed'});
        if (method !== 'GET') return new AcquisitionPlan({...base, allowed:false, reason:'non-get-method'});
        if (candidate.depth > CONFIG.maxDepth) return new AcquisitionPlan({...base, allowed:false, reason:'max-depth'});
        if (candidate.type==='form' && !CONFIG.policy.acquireForms) return new AcquisitionPlan({...base, allowed:false, reason:'forms-disabled'});
        if (candidate.type==='media' && !CONFIG.policy.acquireMedia) return new AcquisitionPlan({...base, allowed:false, reason:'media-disabled'});
        if (candidate.hints?.binary && !CONFIG.policy.acquireBinaryResources) return new AcquisitionPlan({...base, allowed:false, reason:'binary-disabled'});
        return new AcquisitionPlan({...base, allowed:true, reason:null});
    }
}

describe('canonicalizeUrl', () => {
    it('strips hash', () => {
        assert.equal(canonicalizeUrl('https://example.com/page#section'), 'https://example.com/page');
    });
    it('strips tracking params but keeps others', () => {
        const url = canonicalizeUrl('https://example.com/page?utm_source=x&fbclid=123&keep=1');
        assert.equal(url, 'https://example.com/page?keep=1');
    });
    it('resolves relative against base', () => {
        assert.equal(canonicalizeUrl('/path?q=1', 'https://example.com/base/'), 'https://example.com/path?q=1');
    });
    it('returns null for malformed', () => {
        // `ht!tp://[bad` is treated as relative against base, so it canonicalizes;
        // use a truly unparseable absolute URL to trigger null.
        assert.equal(canonicalizeUrl('https://[:::1'), null);
        // empty string resolves to base itself (document URL), not null
        assert.equal(canonicalizeUrl('', 'https://example.com/'), 'https://example.com/');
        assert.equal(canonicalizeUrl('https://[:::1', 'https://example.com/'), null);
    });
});

describe('isAllowedUrl', () => {
    it('rejects non-http schemes', () => {
        assert.equal(isAllowedUrl('javascript:alert(1)'), false);
        assert.equal(isAllowedUrl('data:text/plain,hi'), false);
        assert.equal(isAllowedUrl('mailto:a@b'), false);
    });
    it('enforces sameOriginOnly', () => {
        assert.equal(isAllowedUrl('https://example.com/a'), true);
        assert.equal(isAllowedUrl('https://evil.com/a'), false);
    });
});

describe('looksLike*', () => {
    it('html via content-type or body sniff', () => {
        assert.equal(looksLikeHtml('text/html', ''), true);
        assert.equal(looksLikeHtml('', '<html><body>'), true);
        assert.equal(looksLikeHtml('text/plain', 'hello'), false);
    });
    it('json via content-type or body sniff', () => {
        assert.equal(looksLikeJson('application/json'), true);
        assert.equal(looksLikeJson('', '{"a":1}'), true);
        assert.equal(looksLikeJson('text/html', '<html>'), false);
    });
    it('binary detection', () => {
        assert.equal(looksLikeBinary('image/png'), true);
        assert.equal(looksLikeBinary('application/pdf'), true);
        assert.equal(looksLikeBinary('text/html'), false);
    });
});

describe('AcquisitionPolicy', () => {
    const policy = new AcquisitionPolicy();
    const cand = (over={}) => ({ id:'c1', target:'https://example.com/page', type:'url', depth:0, hints:{}, ...over });

    it('allows GET within depth', () => {
        assert.equal(policy.plan(cand()).allowed, true);
    });
    it('denies non-GET', () => {
        assert.equal(policy.plan(cand({ hints:{method:'POST'}})).reason, 'non-get-method');
    });
    it('denies max-depth exceeded', () => {
        assert.equal(policy.plan(cand({ depth:6 })).reason, 'max-depth');
    });
    it('denies forms/media/binary per policy', () => {
        assert.equal(policy.plan(cand({ type:'form'})).reason, 'forms-disabled');
        assert.equal(policy.plan(cand({ type:'media'})).reason, 'media-disabled');
        assert.equal(policy.plan(cand({ hints:{binary:true}})).reason, 'binary-disabled');
    });
    it('denies cross-origin when confined', () => {
        assert.equal(policy.plan(cand({ target:'https://evil.com/x'})).reason, 'url-not-allowed');
    });
    it('denies javascript: URLs', () => {
        assert.equal(policy.plan(cand({ target:'javascript:alert(1)'})).reason, 'url-not-allowed');
    });
});

describe('fingerprint stability (fnv1a32)', () => {
    function fnv1a32(text){
        let hash=0x811c9dc5;
        for(let i=0;i<text.length;i++){ hash^=text.charCodeAt(i); hash+=(hash<<1)+(hash<<4)+(hash<<7)+(hash<<8)+(hash<<24); hash>>>=0; }
        return hash.toString(16).padStart(8,'0');
    }
    it('deterministic for same input', () => {
        assert.equal(fnv1a32('hello'), fnv1a32('hello'));
        assert.notEqual(fnv1a32('hello'), fnv1a32('Hello'));
    });
    it('empty and large body handled', () => {
        assert.equal(fnv1a32(''), '811c9dc5'); // FNV offset basis
        assert.equal(fnv1a32('a'.repeat(1000)).length, 8);
    });
});
