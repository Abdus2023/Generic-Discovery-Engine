# Verification Supplement — v0.8.0 Providers & Change Detection

> Extends `VERIFICATION_REPORT.md` (v0.7.1) + `VERIFICATION_SUPPLEMENT_v0.7.2.md` + `VERIFICATION_SUPPLEMENT_v0.7.6.md` + `VERIFICATION_SUPPLEMENT_v0.7.7.md` + `VERIFICATION_SUPPLEMENT_v0.7.8.md` + `VERIFICATION_SUPPLEMENT_v0.7.9.md`. Runnable: `dist/generic-discovery-engine.user.js` (5,773 lines, CONFIG v8, `node --check` PASS). `npm test` 109/109 PASS (30 suites). `npm run coverage` 99.26%/92.48%/94.82% (c8 99.25%/92.42%/88.33% gate PASS 85/75/80) · `npm run verify:build` sha256 7c495… lines 5773 deterministic · `npm run typecheck` informational.

## 1. What shipped in 0.8.0 vs 0.7.9

| Change | File | Lines | Evidence |
|---|---|---|---|
| Providers `RobotsProvider` + `HeadersProvider` (9 total) | `dist/...user.js` | +108 (5,597→5,773) | `grep -n class.*Provider` shows `RobotsProvider` (Sitemap 0.92) + `HeadersProvider` (Link 0.88/Location 0.90), `ProviderRegistry` 9 ordered `Html/Json/Xml/Css/JavaScript/Robots/Headers/Binary/Text` |
| Acquisition `http.headers` capture | `dist/...user.js` | — | `grep -n headers:` shows `Object.fromEntries([...response.headers.entries()])` (fetch) + `responseHeaders` parse (GM_xhr) → `Observation.http.headers` |
| Change detection `CONFIG.changeDetection` + `_oldHash` | `dist/...user.js` | — | `grep -n changeDetection\|_oldHash\|resource-changed` shows `changeDetection:true`, `_oldHash` capture before `ensureResource`, `hash !== _oldHash` → `resource-changed` diagnostic + `status='changed'` |
| Tests | `tests/provider-robots-headers.test.js` | +12 tests | Robots matches/extract Sitemap 2, Headers matches Link/Location + extract 3, http.headers captured, change diff/same (3) |
| Static check extension | `tests/verify-p0-fixes.test.js` | +1 test | now asserts `RobotsProvider/HeadersProvider/resource-changed/changeDetection/Object.fromEntries` in dist + `0.8.0` in pkg |
| ADRs + docs | `docs/adr/016-robots-provider.md`, `017-headers-provider.md`, `018-change-detection.md`, `adr/README` (15→18), `DECISIONS`/`OVERVIEW` 5,773, `CHANGELOG`/`README` 109/109, `PERFORMANCE`/`SECURITY` →v0.8.0 | — | 18 ADRs cover control-plane |
| Build | `dist/.build-meta.json` updated `sha256 7c495…` lines 5773 | — | `npm run verify:build` deterministic |

No change to `candidateTTL`, `lifecycle` guard, `rAF`, `pattern/cluster`, `fingerprint` sampling, `privacy`, `Trusted Types` — all retained. `CONFIG.version` stays 8 (storage compatible).

## 2. Providers: Robots & Headers

**RobotsProvider** (`robots-sitemap` 0.92)

```js
matches(obs){
  const url=String(obs.requestedUrl||obs.target||'');
  if(/robots\.txt$/i.test(url)) return true;
  const ct=contentTypeBase(obs.http?.contentType||'');
  return ct==='text/plain' && /User-agent:/i.test(String(obs.body||''));
}
recognize:
  re=/Sitemap:\s*(https?:\/\/\S+)/gi
  canonicalizeUrl(m[1]) → Discovery kind:sitemap confidence0.92 mechanism robots-sitemap
```

- Ordered 6th (after `JavaScriptProvider`, before `HeadersProvider`); `TextProvider` remains fallback last, so `robots.txt` body `User-agent:` does not get mis-classified as generic `text-url` 0.40. Proven by 4 cases: source contains, matches URL, matches body, Sitemap extraction 2 URLs.

**HeadersProvider** (`headers-link` 0.88, `headers-location` 0.90)

```js
matches(obs){
  const h=obs.http?.headers; if(!h) return false;
  const link=h['link']||h['Link']; if(link && /<https?:\/\/[^>]+>/.test(String(link))) return true;
  const loc=h['location']||h['Location']; if(loc && isAllowedUrl(String(loc))) return true; return false;
}
recognize:
  linkVal = String(h['link']||h['Link']||''); re=/<([^>]+)>/g → emit headers-link 0.88
  loc = h['location']||h['Location']; emit headers-location 0.90
```

- Requires `http.headers` lowercased (case-insensitive). Proven by 4 cases: source contains, matches Link, matches Location, extracts 3 URLs (2 Link +1 Location).

**Acquisition `http.headers`**

- Fetch: `headers: Object.fromEntries([...response.headers.entries()].map(([k,v])=>[k.toLowerCase(),v]))`
- GM_xhr: parse `response.responseHeaders` string split `\r?\n`, `:` index, lowercased keys.
- `Observation` stores `http.headers` as provided (no class change, `http` is `data.http || {…}`); `serialize` already includes `http` whole, so headers persist in `exportData` if needed and are stripped from `fingerprint` (fingerprint only body).

## 3. Change Detection

```js
CONFIG.changeDetection = true;

recordObservation(obs){
  const _oldHash = (()=>{ try{ const prev=this.resources.get(canonicalizeUrl(obs.requestedUrl)||obs.requestedUrl); return prev?.fingerprint?.hash||null; }catch{return null;} })();
  const resource=this.ensureResource(obs.requestedUrl);
  resource.merge({..., fingerprint:obs.fingerprint});
  if(obs.fingerprint){
    const hash=obs.fingerprint.hash;
    // fingerprintIndex update...
    if(CONFIG.changeDetection && _oldHash && hash!==_oldHash){
      this.recordDiagnostic('resource-changed',{target:obs.requestedUrl, oldHash:_oldHash, newHash:hash});
      try{ const res=this.resources.get(canonicalizeUrl(obs.requestedUrl)||obs.requestedUrl); if(res) res.status='changed'; }catch{}
    }
  }
}
```

- Capture `_oldHash` **before** `ensureResource` + `merge`, so it is previous hash, not new.
- Cost O(1) Map lookup + string compare, ~0.01 ms.
- No auto-requeue; `changed` observable via `resource.status` and `ledger/diagnostics`; future scheduler could re-queue `changed` via `candidateTTL` or explicit `revisit`.
- Proven by 3 cases: source contains `changeDetection/_oldHash/resource-changed`; `hello` → `hello world` emits `resource-changed` and `status='changed'`; same hash no diagnostic.

## 4. How to reproduce

```bash
npm run check          # node --check both dist files
npm test               # 109/109 PASS 30 suites ~2.1s
npm run coverage       # native 99.26%/92.48%/94.82%
npm run coverage:check # c8 99.25%/92.42%/88.33% gate PASS
npm run verify:build   # sha256 7c4952… lines 5773 deterministic
npm run typecheck 2>&1 | head -n 50  # informational
node --test tests/provider-robots-headers.test.js # 12/12
```

`dist/generic-discovery-engine.v0.7.1.user.js` (5,164 lines) retained; `docs/ci/verify.yml.example` is CI source (copy to `.github/workflows/verify.yml` with PAT that has `workflows` scope).

## 5. Residual

- `RobotsProvider` only extracts `Sitemap:`; `Allow`/`Disallow` not yet used for `AcquisitionPolicy` soft deny — future may add `policy: { respectRobotsTxt:false }` toggle.
- `HeadersProvider` only handles `Link` and `Location`; `Content-Location`, `Refresh`, `X-Robots-Tag` not yet — extensible.
- `changed` status not yet re-queues; Phase 3 “historical knowledge + change detection” will add `revisitChanged` option.
- Next Phase 4 framework split (`src/` modular build) will replace `dist` stub `build.js` with true bundler; `verify-build` hash already gates drift, so transition non-breaking.
