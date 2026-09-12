# ADR 022 — Pattern-Guided + RevisitChanged (adaptive re-queue)

**Status:** accepted (v0.9.1)  
**Transcript:** Phase 4 “adaptive re-queue” + pattern-guided exploration  
**Code:** `CONFIG.revisitChanged`, `CONFIG.patternGuided`, `KnowledgeBase.suggestPatternCandidates()`, `getChangedResources()`, `GenericDiscoveryEngine` revisit + pattern-guided hooks, `src/header.txt` patch notes

## Context
`changeDetection` marked `ResourceRecord.status='changed'` on fingerprint diff but never re-queued, so a changed page stayed `changed` until manual revisit. `patternInference` collected `patternIndex`/`clusterIndex` and `getPatternMetrics()` but never suggested new candidates, so the engine observed `https://a.ex/user/{int} 200` without probing `…/user/0`. Both are DVB-like “spectrum re-scan” and “next frequency from pattern” strategies that were future in ADR 018/013. The generic loop needs an *opt-in* adaptive re-queue that respects `visited` dedup and `isAllowedUrl` while staying deterministic and bounded.

## Decision
- **Config** `CONFIG.revisitChanged: false` (off by default, opt-in) and `CONFIG.patternGuided: {enabled:false, maxSuggestions:5}` (off, bounded). Added to `src/config.js` (164→~172 lines), `STORAGE_KEY` stays `v8`.
- **Knowledge** `KnowledgeBase.suggestPatternCandidates(limit=5)` (knowledge.js +~30 lines): if `patternGuided.enabled && patternInference`, takes `getPatternMetrics().top` (sorted, top 20), filters `count < minPatternFreq` and patterns without `{int}/{hash}/{uuid}`, deterministically replaces placeholders (`{int}`→`0`, `{hash}`→`0*32`, `{uuid}`→`00000000-0000-4000-a000…`, handling `?x={int}`), skips `visited`/`candidateKeys` and `!isAllowedUrl`, returns up to `limit` `{pattern,count,suggestion}`. `getChangedResources()` returns `resources.filter(status==='changed')`.
- **Engine hooks** (engine.js +~50 lines, inside `executePlan`):
  * After `recordObservation` + `markObserved`, if `revisitChanged` and `resource.status==='changed'`, clear `visited.delete('url:'+url)` + `candidateKeys.delete`, `discover(url,'url',{priority:0.6, depth, hints:{revisit:true}, mechanism:'revisit-changed'})` and `ledger diagnostic revisit-queued`.
  * After `markCompleted` + `recordCandidateCompleted`, if `patternGuided.enabled`, call `suggestPatternCandidates()` and for each `discover(suggestion,'url',{priority:0.55, depth+1, hints:{patternGuided:true,pattern}, mechanism:'pattern-guided'})` with `diagnostic pattern-guided-queued`. Both bounded (5) and synchronous before `schedulePersistence`.
- **Build** header `src/header.txt` now `v0.9.1 — Pattern-Guided + RevisitChanged` + patch notes vs `0.9.0` (knowledge/engine), `package.json` `0.9.1` description “pattern-guided + revisitChanged”, `dist` `5875→5969` (+94, `44500a…`).

## Consequences
- **+** Operators with `revisitChanged:true` see `resource-changed` automatically re-queued (one revisit per change, clears visited, so same URL can be re-acquired; ledger shows `revisit-queued`, no infinite loop because fingerprint must change again).
- **+** With `patternGuided:true` and after 3+ hits to `https://a.ex/user/{int}` (minPatternFreq), the engine suggests `https://a.ex/user/0` etc. (up to 5, deterministic, `isAllowedUrl` + visited dedup), enabling “scan the pattern” without manual seeding — DVB-like blind scan of collapsed template.
- **+** Both off by default → no behavior change for existing `npm test` 121/121 → 126/126 (new `pattern-guided-revisit` 5 cases + existing). Cost: suggestion O(20) + `discover` O(1), ~0.02 ms; revisit O(1) Map ops.
- **−** `patternGuided` suggestion is naive (`0` for `{int}`) — may suggest already-visited or 404; future could increment from max seen int or use `clusterIndex` to weight.
- **−** `revisitChanged` deletes `visited` entry, so a flapping resource (alternating hash) could revisit repeatedly — bounded by `maxRequests 150` and `origin` throttle; documented as opt-in.

## Links
- Code: `src/config.js` new keys, `src/knowledge.js` `suggestPatternCandidates`/`getChangedResources`, `src/engine.js` revisit + pattern-guided hooks, `src/header.txt` v0.9.1, `dist` 5969 `44500a…`, `scripts/verify-build.js` asserts `revisitChanged`/`patternGuided`/`suggestPatternCandidates`/`getChangedResources`.
- Tests: `tests/pattern-guided-revisit.test.js` 5 cases (static keys, disabled empty, pattern collapse, revisit re-queue via patched CONFIG true, fingerprintUnique still correct).
- Prior: ADR 018 change detection, ADR 013/014 pattern/cluster, ADR 021 bundler.
