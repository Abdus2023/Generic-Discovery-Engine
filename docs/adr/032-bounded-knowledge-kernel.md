# ADR 032 — Bounded Knowledge Kernel (v1.5 second-pass audit → B3)

**Status:** accepted (v1.6.0)  
**Transcript:** v1.5 second-pass audit (linked artifact v1.5.0 6453 `508e3e…` → 8 findings: ResourceRecord unbounded arrays, bodyBytes not enforced, dangling refs on eviction, visited 2500→∞, candidateKeys≈candidates history accumulation, fingerprint/pattern indexes historical, restore bypasses runtime caps, GM_xhr redirect cross-origin) + retention model proposal (Policy→Search/Execution/Retention/Persistence)  
**Code:** `src/config.js` `retention{visited2k,candidateKeys2k,candidateHistory2k,observations800+5M/150,discoveries2k,resources2k×100,fp500×100,patterns500,clusters500}` `runtimeBudget.maxBodyBytes 5M` `src/models.js` `merge.slice(-100)` `src/knowledge.js` 1019 Bounded Kernel (referential coherence + body budget + bounded restoration) `src/engine.js` `gm-redirect-blocked` `recordNetworkEvent` retention `src/header.txt` `1.6.0` `7efbfd…` 6794

## Context
v1.5 was “containers bounded” (B1). Second-pass audit reclassified GDE state topology and proved B1≠B2/B3:

- **B1 containers have size limits:** discoveries 2k, resources 2k, observations 800, networkEvents 1k — *mostly yes*.
- **B2 total payload has limits:** `maxBodiesInMemory:150` declared but `recordObservation` only capped `observations Map size`, not `retainedBodyBytes`. `800×2M=1.6B` chars still possible. `maxBodies` counted objects not bytes.
- **B3 graph + indexes referentially coherent:** ResourceRecord `parents/candidateIds/observationIds/discoveryIds/networkEventIds` used `unique([...old,…new])` unbounded → `2000×∞` metadata. `visited Set` added via `visited.add(key)` with no `maxVisited` → SPA can accumulate `url:N` indefinitely. `candidateKeys Map` live-only cap left `candidates`+`candidateKeys`+`visited` historical. `fingerprintIndex Map<hash,Set<url>>` accumulated URLs forever. `patternIndex/clusterIndex` incremented but never evicted. Eviction was `map.delete(firstKey)` without reverse-index cleanup → `Resource.discoveryIds→[D17]` dangling after `discoveries.delete(D17)`, `observationIds` dangling, `candidateKeys[k]=id → missing candidate`, edges unbounded restoration.

Additionally: `GM_xmlhttpRequest` records `response.finalUrl` but had no redirect-boundary check (Fetch was hardened to `redirect:'error'`, GM path still allowed same-origin→cross-origin redirect). `restore()` directly inserted persisted state without re-applying runtime caps → `persisted 5000 resources` could bypass `runtime 2000`. `serialize()` emitted `visited:[...Set]` unbounded.

The audit proposed `RetentionPolicy` ownership semantics instead of random `maxX` caps and stronger invariants `∀C size(C)≤bound(C)` plus `cardinality(R)≤bound(R)` and `retainedBodyBytes≤maxBodyBytes`.

## Decision
- **Unified RetentionPolicy (v1.6):** `src/config.js` adds `CONFIG.retention` additive to legacy `max*`/`runtimeBudget` (backwards compatible, new overrides):
  ```
  retention: {
    visited:{maxEntries:2000}, candidateKeys:{maxEntries:2000}, candidateHistory:{maxEntries:2000},
    observations:{maxEntries:800, maxBodyBytes:5_000_000, maxBodies:150},
    discoveries:{maxEntries:2000}, resources:{maxEntries:2000, maxRelationsPerResource:100},
    fingerprint:{maxHashes:500, maxUrlsPerHash:100}, patterns:{maxEntries:500}, clusters:{maxEntries:500},
    networkEvents:{maxEntries:1000}, graphEdges:{maxEntries:5000}, diagnostics:{maxEntries:500}
  }
  runtimeBudget.maxBodyBytes 5M (mirrors retention)
  ```
  Every collection insertion-order FIFO; relation arrays LRU-sliced.

- **ResourceRecord bounded merge:** `src/models.js` `merge()` now reads `maxRelations = retention.resources.maxRelationsPerResource ?? 100` and after `unique(...)` does `.slice(-maxRelations)` for `types/mechanisms/parents/candidateIds/observationIds/discoveryIds/networkEventIds` (vs unbounded). Prevents `2000×∞`.

- **Bounded Knowledge Kernel:** `src/knowledge.js` rewritten 744→1019 lines, introduces retention helpers `_retention()`, `_maxVisited()` etc., and coherent eviction:
  - `_enforceVisitedBound()` FIFO `visited` to 2k, diagnostic `visited-evicted`.
  - `_enforceCandidateKeysBound()` historical-first FIFO (scans for `completed/skipped/missing` before evicting live frontier), diagnostic `candidateKeys-evicted`/`candidateKeys-pressure`.
  - `_enforceCandidateHistoryBound()` evicts oldest `completed/skipped` candidates FIFO when `candidates.size>2000`, cleans `candidateKeys`/`claimed`/`resource.candidateIds` via `_removeCandidateReferences`, diagnostic `candidate-history-evicted`.
  - `addCandidate` cleans stale `candidateKeys`→missing candidate (`candidateKeys-stale-cleaned`), then enforces `candidateKeys` + `candidateHistory` after insertion + `recordPattern` → `_enforcePatternBound`.
  - `markCompleted/markSkipped` after `visited.add` enforce visited + history bounds (vs unbounded).
  - `recordObservation` FIFO evicts oldest observation **with** `_removeObservationReferences` cleanup, fingerprints per-hash+global caps via `_enforceFingerprintBound` (maxHashes 500 FIFO, maxUrlsPerHash 100 per hash), body budget via `_enforceBodyBudget` (iterate insertion order, while `bodies>150||bytes>5M` clear oldest `body=""` `bodyTruncated=true`, diagnostic `body-evicted`). fixes `maxBodiesInMemory` without enforcement.
  - `addDiscovery` FIFO with `_removeDiscoveryReferences`, `ensureResource` FIFO with `_removeResourceFingerprint` (cleans `fingerprintIndex[hash].delete(url)` and `delete(hash)` if empty), `addEdge` FIFO shift (was drop) with `graphEdge-evicted`, diagnostics FIFO via `retention.diagnostics`.
  - `serialize()` now `visited.slice(-2000)` (was `[...visited]` unbounded).
  - `restore()` bounded restoration after loading: `_enforceCandidateHistoryBound/_enforceCandidateKeysBound/_enforceVisitedBound`, while `observations.size>800` FIFO+cleanup+`observation-evicted-on-restore`, `_enforceBodyBudget`, while `discoveries/resources` over caps FIFO+cleanup, `_enforceFingerprintBound/_enforcePatternBound/_enforceGraphEdgesBound`, diagnostics trim. Guarantees `∀C size(C)≤bound(C)` even if persisted state larger than runtime.

- **Referential integrity:** new helpers `_removeObservationReferences`/`_removeDiscoveryReferences`/`_removeCandidateReferences`/`_removeResourceFingerprint` loop `resources` (≤2k) O(2k) to splice dangling IDs, and stale `candidateKeys` cleaned on duplicate. Replaces local `Map.delete` with graph-aware `evict(entity)` semantics (ledger event + reverse-index update).

- **GM redirect enforcement:** `src/engine.js` `GM_xmlhttpRequest.onload` now checks `finalUrl = response.finalUrl||plan.target`; if `sameOriginOnly && finalUrl!==plan.target && !isAllowedUrl(canonicalizeUrl(finalUrl))` → `ledger.recordDiagnostic('gm-redirect-blocked')` + `finish(new Observation{status:'blocked',reason:'redirect-cross-origin'})` and return, mirroring `fetch redirect:'error'` boundary (was fetch-hardened only, GM open).

- **NetworkEvents retention:** `GenericDiscoveryEngine.recordNetworkEvent` now reads `max = retention.networkEvents.maxEntries ?? maxNetworkEvents` (was legacy only), FIFO eviction diagnostic `network-events-evicted`.

- **Build:** `src/header.txt` bump `1.5.0→1.6.0` + 1.6 patch notes (retention + resource slice + kernel + GM + retention checks), fix no `src/**/*.js` inside comment. `scripts/verify-build.js` adds 8 new asserts: `CONFIG.retention`, `maxBodyBytes`, `maxRelationsPerResource`, `body-evicted`, `gm-redirect-blocked`, `_enforceVisitedBound`, `_removeObservationReferences`, `observation-evicted-on-restore`. New build `6794 lines 223914B sha 7efbfd…` `min 74783 33.4% ba83e9…` `esm 267 792783` providers now `18.9%` (vs 20.6%).

## Consequences
- **+** B2 achieved: retained body bytes bounded to `5M` and `150` bodies FIFO (was 1.6B possible), relation arrays bounded to `100` per field (was ∞), historical visited/candidateKeys/candidates/patterns/fingerprints bounded (was accumulation). `restore` can no longer bypass runtime caps.
- **+** B3 achieved: eviction is referentially coherent — discovery/observation/candidate/resource eviction cleans reverse edges (no dangling `discoveryIds→missing`), stale `candidateKeys` auto-cleaned, fingerprint graph pruned. Formal invariant `candidateKeys[k]=id ⇒ candidates.has(id)` or explicit `stale-cleaned`.
- **+** Security complete: both acquisition paths now enforce same-origin redirect boundary (`fetch error` + `GM blocked`), diagnostic observable.
- **+** Tests still `160/160 42 suites` (no regressions), new stress harness `12/12` (relation cap, body budget 5M, visited 2k, discovery/observation dangling cleaned, fingerprint 500×100, pattern 500, restore 2k/800/5k, GM blocked, stale cleaned, history 2k, edges 5k) proves B3 semantically, not merely present.
- **−** Dist grows `6453→6794 (+341)` due to kernel helpers, hash `508e3e…→7efbfd…`, min `66k 32.7%→74k 33.4%` (extra logic, still deterministic). O(2k) loops on eviction add ~0.05ms per eviction (acceptable vs network 150ms). Retention caps are still generous (2k/500) — fine for browser heap (~6–10 MB vs 600MB before).

## Links
- Audit: linked artifact v1.5.0 `508e3e…` + second-pass `B1/B2/B3` analysis + `RetentionPolicy` proposal (visited/history/fingerprint/pattern restoration diagram).
- Code: `src/config.js` `retention`, `src/models.js` `slice(-maxRelations)`, `src/knowledge.js` `Bounded Knowledge Kernel 1019`, `src/engine.js` `gm-redirect-blocked`, `src/header.txt` `1.6.0 7efbfd…`, `scripts/verify-build.js` 8 new gates, `dist/.build-meta.json` `6794`.
- Prior: ADR 031 verification hardening, ADR 030 concurrent, `DEEP_VERIFICATION_v1.4.md`, `VERIFICATION_SUPPLEMENT_v1.5.0.md`.
