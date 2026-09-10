# Verification Supplement — v0.7.9 Pattern & Cluster + Build Determinism

> Extends `VERIFICATION_REPORT.md` (v0.7.1) + `VERIFICATION_SUPPLEMENT_v0.7.2.md` + `VERIFICATION_SUPPLEMENT_v0.7.6.md` + `VERIFICATION_SUPPLEMENT_v0.7.7.md` + `VERIFICATION_SUPPLEMENT_v0.7.8.md`. Runnable: `dist/generic-discovery-engine.user.js` (5,597 lines, CONFIG v8, `node --check` PASS). `npm test` 96/96 PASS (26 suites). `npm run coverage` 99.25%/94.72%/93.70% (c8 99.24%/94.67%/85.71% gate PASS) · `npm run verify:build` deterministic · `npm run typecheck` informational.

## 1. What shipped in 0.7.9 vs 0.7.8

| Change | File | Lines | Evidence |
|---|---|---|---|
| Pattern inference `CONFIG.inference` + `extractUrlPattern`/`clusterKeyForCandidate` | `dist/...user.js` | +71 (5,526→5,597) | `grep -n inference\|extractUrlPattern` shows `patternInference:true`, `/{int}/{uuid}/{hash}` normalizations, `URL` parse with fallback |
| KnowledgeBase pattern/cluster indices + metrics | `dist/...user.js` | — | `grep -n patternIndex\|clusterIndex\|getPatternMetrics\|getClusterMetrics` shows `Map<pattern,count>`, `Map<origin::pattern,count>`, `recordPattern` called in `addCandidate` after `stats.discovered++`, `sorted top 20`, `total` |
| Build determinism | `scripts/build.js`, `scripts/verify-build.js`, `dist/.build-meta.json` | — | `build.js` sha256+lines+size → `dist/.build-meta.json` `{ version, sha256, lines:5597, size:158541 }`; `verify-build.js` checks forbidden `builtAt` in dist, header `@version` matches `package.json`, `extractUrlPattern` present, hash matches meta |
| Tests | `tests/property-pattern.test.js` | +7 tests | numeric path, query, uuid/hash, collapse 500 iter, different structures, metrics sorted/bounded (seeded) |
| Static check extension | `tests/verify-p0-fixes.test.js` | +1 test | now asserts `patternInference/extractUrlPattern/getPatternMetrics/getClusterMetrics/inference` in dist + `verify:build` in pkg + `scripts/verify-build.js` exists |
| ADRs + docs | `docs/adr/013-pattern-inference.md`, `014-clustering.md`, `015-build-determinism.md`, `adr/README` (12→15), `DECISIONS`/`OVERVIEW` 5,597, `CHANGELOG`/`README` 96/96, `PERFORMANCE`/`SECURITY` →v0.7.9 | — | 15 ADRs cover control-plane |
| CI | `docs/ci/verify.yml.example` build step, `package.json` `build`/`verify:build` | — | `npm run verify:build` deterministic |

No change to `candidateTTL`, `lifecycle` guard, `rAF`, `fingerprint`, `privacy`, `Trusted Types` — all retained.

## 2. Pattern: `extractUrlPattern`

```js
CONFIG.inference = { patternInference:true, clustering:true, minPatternFreq:3 }

function extractUrlPattern(url){
  if(!CONFIG.inference?.patternInference) return String(url);
  try{
    const u=new URL(url);
    let path=u.pathname.replace(/\/\d+(?=\/|$)/g,'/{int}');
    path=path.replace(/\/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}(?=\/|$)/g,'/{uuid}');
    path=path.replace(/\/[0-9a-fA-F]{32,64}(?=\/|$)/g,'/{hash}');
    let search=u.search.replace(/=\d+(&|$)/g,'={int}$1');
    search=search.replace(/=[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}(&|$)/g,'={uuid}$1');
    search=search.replace(/=[0-9a-fA-F]{32,64}(&|$)/g,'={hash}$1');
    return `${u.origin}${path}${search}`;
  }catch{
    return String(url).replace(/\/\d+(?=\/|$)/g,'/{int}').replace(/=\d+(&|$)/g,'={int}$1');
  }
}
```

- Deterministic, no allocation beyond `URL` parse, O(len). `minPatternFreq` reserved for future template suggestion (not yet enforced).
- Collapses same template different ids: `https://ex/user/123` and `https://ex/user/456` → `https://ex/user/{int}` (500-iter property test with `lcg 0x9ab`).
- Different structures stay different: `/user/123` vs `/user/abc` vs `/page/123` → distinct patterns.
- Verified by `property-pattern.test.js` 7 invariants:
  1. source contains `inference`/`extractUrlPattern`/`clusterKeyForCandidate`/`getPatternMetrics`/`getClusterMetrics`
  2. numeric path `…/123/profile` → `…/{int}/profile`, non-numeric preserved
  3. query `?page=2` → `?page={int}`, `?term=hello` preserved
  4. uuid `550e8400-e29b-41d4-a716-446655440000` → `/{uuid}`, hash 32/64 → `/{hash}` (fixed 8-4-4-4-12)
  5. collapse 500 iter `user/{int}/post/{int}` same
  6. different structures different
  7. clustering `origin::pattern` metrics sorted/bounded

## 3. Cluster: `getClusterMetrics` / `getPatternMetrics`

```js
this.patternIndex = new Map(); // pattern → count
this.clusterIndex = new Map(); // origin::pattern → count

recordPattern(candidate){
  if(!CONFIG.inference?.patternInference) return;
  const pattern=extractUrlPattern(candidate.target);
  this.patternIndex.set(pattern,(this.patternIndex.get(pattern)||0)+1);
  if(CONFIG.inference.clustering){
    const key=clusterKeyForCandidate(candidate);
    this.clusterIndex.set(key,(this.clusterIndex.get(key)||0)+1);
  }
}
getPatternMetrics(){ const s=[...this.patternIndex.entries()].sort((a,b)=>b[1]-a[1]).slice(0,20); return {size:s.size, top:s, total: sum};}
getClusterMetrics(){ ... clusterIndex ...}
```

- `recordPattern` called in `KnowledgeBase.addCandidate` after `candidateKeys.set` and `stats.discovered++` (not when `visited` deduped), O(1) ~0.01 ms.
- `getPatternMetrics` / `getClusterMetrics` O(n) over ≤750 distinct patterns/clusters, sorted top 20, ~0.06 ms; bounded `<100 KB` at 750.
- Property test seeds 200 random `origin/user/{int}` across 2 origins → `pattern size ≤2`, `cluster size ≤2`, `total 200`, top sorted descending, top ≤20.
- No scheduler change yet; metrics observable via `exportData` future and via direct `db.getClusterMetrics()` for UI.

## 4. Build determinism: `scripts/build.js` + `verify-build.js`

`scripts/build.js`:
```js
const content=readFileSync('dist/generic-discovery-engine.user.js','utf8');
const hash=createHash('sha256').update(content).digest('hex');
const lines=(content.match(/\n/g)||[]).length; // wc -l
const size=Buffer.byteLength(content);
const pkg=JSON.parse(readFileSync('package.json','utf8'));
writeFileSync('dist/.build-meta.json', JSON.stringify({version:pkg.version, file:'dist/...user.js', sha256:hash, lines, size, builtAt:new Date().toISOString(), node:process.version},null,2));
```

`scripts/verify-build.js`:
- Forbidden patterns `builtAt`/`__RANDOM__` in dist (ensures no timestamp in artifact)
- Header `@version` and `v${version} —` banner match `package.json` version
- `extractUrlPattern` present
- If `dist/.build-meta.json` exists, `sha256` and `version` must match (must run `npm run build` after `dist` edit)
- `dist/.build-meta.json` committed (hash `9a2fb1a73faa...` lines 5597 size 158541)

Until `src/` split, `build.js` is a stub that captures hash; future v0.8.0 will replace stub with `src/` → `dist` bundler; `verify-build` already enforces hash, so transition non-breaking. CI `verify.yml.example` now runs `npm run verify:build` after `typecheck`.

## 5. How to reproduce

```bash
npm run check          # node --check both dist files
npm test               # 96/96 PASS 26 suites ~2.1s
npm run coverage       # native 99.25%/94.72%/93.70%
npm run coverage:check # c8 99.24%/94.67%/85.71% gate PASS
npm run verify:build   # deterministic sha256 9a2fb1a... lines 5597
npm run build          # regenerate dist/.build-meta.json
npm run typecheck 2>&1 | head -n 50  # informational
node --test tests/property-pattern.test.js # 7/7
```

`dist/generic-discovery-engine.v0.7.1.user.js` (5,164 lines) retained; `docs/ci/verify.yml.example` is CI source (copy to `.github/workflows/verify.yml` with PAT that has `workflows` scope).

## 6. Residual

- `minPatternFreq:3` not yet used for template suggestion; future will emit `Discovery` kind `pattern` when pattern count reaches threshold.
- `clusterIndex` not yet used for scheduler deprioritization of over-represented `origin::pattern` (planned Phase 3 `candidate clustering`).
- `build.js` stub will be replaced by `src/` bundler in v0.8.0; `dist` remains source of truth until then, but `verify:build` already gates version/header/hash drift.
