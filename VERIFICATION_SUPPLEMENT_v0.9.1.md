# Verification Supplement — v0.9.1 Pattern-Guided + RevisitChanged (adaptive re-queue)

> Extends `VERIFICATION_REPORT.md` (v0.7.1) + supplements `v0.7.2`→`v0.9.0` + `DEEP_DVB_AUDIT_v0.8.2.md`. Runnable `dist/generic-discovery-engine.user.js` **5,969 lines** (`sha 44500a…` `176112B`) built from `src/` 7 modules via bundler (`node --check` PASS). `npm test` **126/126 33 suites** (was 121/121). `verify:build` deterministic (header + src 7 + `44500…` + revisit/pattern gate).

## 1. What shipped in 0.9.1 vs 0.9.0

| Change | File | Lines | Evidence |
|---|---|---|---|
| `revisitChanged` + `patternGuided` config | `src/config.js` | +12 (160→172) | `grep -n revisitChanged src/config.js` → `false` + `patternGuided {enabled:false, maxSuggestions:5}` |
| Pattern-guided API | `src/knowledge.js` `suggestPatternCandidates` + `getChangedResources` | +30 (701→731) | `grep -n suggestPatternCandidates src/knowledge.js` → `enabled && patternInference`, `top` filter `minPatternFreq`, `{int}→0` etc., `isAllowedUrl` + `visited` dedup, `getChangedResources` filter `status==='changed'` |
| Engine hooks | `src/engine.js` revisit + pattern-guided | +50 (2863→2913) | `grep -n revisit-queued src/engine.js` after `recordObservation` clears `visited`/`candidateKeys` → `discover revisit-changed`; after `markCompleted` → `suggestPatternCandidates` → `discover pattern-guided` bounded 5 |
| Header banner | `src/header.txt` | `v0.9.1 — Pattern-Guided + RevisitChanged` | `head -n 20 src/header.txt` shows `v0.9.1` + patch notes vs `0.9.0` |
| Dist | `dist/...user.js` | `5875→5969` (+94) `44500a…` | `wc -l` 5969, `grep -n patternGuided dist/...user.js` 3 hits |
| Build gate | `scripts/verify-build.js` | — | now asserts `revisitChanged`/`patternGuided`/`suggestPatternCandidates`/`getChangedResources` + `header.txt` |
| Tests | `tests/pattern-guided-revisit.test.js` | +5 tests | static keys, disabled empty, pattern collapse ≥3, revisit re-queue via patched `revisitChanged:true`, fingerprint still correct; `verify-p0` now allows `0.9.[0-9]` |
| Package | `package.json` `0.9.1` | — | description “pattern-guided + revisitChanged” |

Both flags **off by default**, so 0.9.0 behavior unchanged unless opted-in; `npm test` 126/126 vs 121/121 (+5 new) proves no regression.

## 2. Pattern-guided exploration

```js
suggestPatternCandidates(limit=5) {
  if (!CONFIG.patternGuided.enabled || !CONFIG.inference.patternInference) return [];
  const {top} = getPatternMetrics(); // sorted top 20
  for ([pattern,count] of top) {
    if (count < minPatternFreq) continue;
    if (!pattern.includes('{int}') && … ) continue;
    let suggestion = pattern.replace('{int}','0').replace('{hash}','0'*32)…;
    suggestion = suggestion.replace('={int}','=0')…;
    if (visited.has('url:'+suggestion) || candidateKeys.has(...)) continue;
    if (!isAllowedUrl(suggestion)) continue;
    suggestions.push({pattern,count,suggestion});
    if (suggestions.length>=limit) break;
  }
  return suggestions;
}
```

* Deterministic: `top` sorted by count, replacement `0`/`uuid0` fixed, `isAllowedUrl` respects `sameOriginOnly`, visited dedup prevents loops.
* Example: after `discover('https://a.ex/user/1')`, `…/2`, `…/3` → `patternIndex` has `https://a.ex/user/{int}:3` → `suggest` returns `https://a.ex/user/0` (if not visited) — DVB-like “scan the next frequency from pattern”.
* Cost O(20) + `discover` O(1) ~0.02 ms, bounded 5, called once per `executePlan` after `markCompleted`.
* Engine hook: if `patternGuided.enabled`, after `markCompleted` → `suggestPatternCandidates()` → `discover(pattern-guided, priority 0.55, depth+1)` + `diagnostic pattern-guided-queued`.

## 3. RevisitChanged

```js
// after recordObservation + markObserved
if (CONFIG.revisitChanged) {
  const res = resources.get(canonicalizeUrl(observation.requestedUrl));
  if (res?.status==='changed') {
    visited.delete('url:'+url); candidateKeys.delete(...);
    const revisit = discover(url,'url',{priority:0.6, depth, hints:{revisit:true}, mechanism:'revisit-changed'});
    if (revisit) ledger diagnostic revisit-queued;
  }
}
```

* Clears `visited` + `candidateKeys` so `addCandidate` not blocked by P0-2 `visited.has(key)` — allows same `type:target` to be re-queued once per change.
* No infinite loop: fingerprint must change again to trigger second revisit; bounded by `maxRequests 150` + `origin` throttle.
* `getChangedResources()` exposes `resources.filter(status==='changed')` for operators (also via `export.inference`? — not yet, but `getCoverageMetrics` still shows `fingerprintUnique`; future export may include `changedCount`).

## 4. How to reproduce

```bash
npm run build                 # header 0.9.1 + 7 modules → dist 5969 44500… 
node --check dist/generic-discovery-engine.user.js # PASS
npm test                      # 126/126 33 suites ~2.9s
node --test tests/pattern-guided-revisit.test.js # 5/5
node --test tests/export-inference.test.js      # 6/6
npm run verify:build          # sha256 44500a… lines 5969 src 7 + revisit/pattern OK
```

To enable adaptive features in the field, set in console before `engine.start()`:

```js
// After engine loads (window.GenericDiscoveryEngine)
CONFIG.revisitChanged = true;
CONFIG.patternGuided.enabled = true;
```

Or edit `src/config.js` and `npm run build`.

## 5. Residual

* `patternGuided` suggestion `0` may be 404 or already visited (deduped) — future could increment from `max` seen `int` or use `clusterIndex` weighting; current deterministic `0` is safe for verification.
* `revisitChanged` deletes `visited` entry — if resource flaps (`hash A→B→A`), it will revisit each flap; bounded by budget, but no `backoff` yet — future `revisitTTL` could debounce.
* `suggestPatternCandidates` uses `patternMetrics.top` (count-sorted) not `clusterIndex`; cluster-guided suggestions (`origin::pattern`) not yet — extensible.
* Next: `v1.0` `esbuild` tree-shaking, `provider` lazy-load, `export --stable` (deterministic `exportedAt:0`), `Allow/Disallow` soft deny via `Robots`.
