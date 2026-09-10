# ADR 006 — Export Schema (gde-export-v8.0, ledger + coverage)

**Status:** accepted (v0.7.2–v0.7.3)  
**Transcript:** §§26–30 + v0.7.3 patch  
**Code:** `GenericDiscoveryEngine.exportData()`, `KnowledgeBase.serialize()`, `DecisionLedger.export()`, `getCoverageMetrics()`

## Context
Early exports contained only `discoveries` (no ledger, no graph). Users could not answer “why was this URL skipped?” after reload. Verification (§11) asked for a self-contained artifact for post-mortem without re-crawling.

## Decision
- Schema `gde-export-v8.0` with `exportedAt`, `config` (full CONFIG snapshot), `coverage` (from `getCoverageMetrics()`), `engine` (serialized KB), `ledger` (`export()`), `networkEvents`, `diagnostics`.
- `KnowledgeBase.serialize()` caps persisted slices: `discoveries 1200`, `resources 1500`, `edges 3000`; `observations` are body-free (via `Observation.serialize()`), ledger 5k; debounced persistence 400 ms to `GM_setValue`.
- Migration additive: `restore()` accepts `engine.version>=6`, re-creates `fingerprintIndex` from `resources`, resets `requestsReserved` to 0 each execution (fresh budget), clamps concurrency.
- `coverage` added v0.7.3: `frontierSize`, `queuedByType`, `liveCount`, `visitedSize`, `knownResources`, `requestsRemaining`, `ledgerSize`, `graphEdges`, `observations` — all O(n) over ≤750 candidates (~0.1 ms).

## Consequences
- **+** Single JSON file answers coverage, budget, and provenance questions.
- **+** Bounded persistence respects `GM_setValue` quota (~10 MB typical).
- **−** Schema bump 7→8 requires key rotation `STORAGE_KEY v7→v8`; old v7 data migrated if `version>=6`, otherwise fresh start (documented in CHANGELOG).

## Links
- Verification: `CHANGELOG.md` 0.7.2/0.7.3, `e2e-discovery-loop.test.js` asserts `export.coverage` present.
- Perf: `PERFORMANCE_ANALYSIS.md` §6 (coverage 0.1 ms).
