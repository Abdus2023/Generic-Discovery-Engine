# ADR 020 — Export Hardening + Inference Metrics (coverage/export deterministic)

**Status:** accepted (v0.8.2)  
**Transcript:** Phase 4 “export hardening” + coverage determinism  
**Code:** `GenericDiscoveryEngine.getCoverageMetrics()` sorted `queuedByType`, inference `patternCount/clusterCount/fingerprintUnique/inferenceEnabled`, `exportData().inference {patternMetrics, clusterMetrics, fingerprintStats}`, `scripts/verify-build.js` inference gate

## Context
`getCoverageMetrics()` returned `queuedByType` in Map insertion order (non-deterministic under different claim orders) and neither `coverage` nor `exportData()` exposed the inference state (`patternIndex`, `clusterIndex`, `fingerprintIndex`) that v0.7.9–v0.8.0 had been collecting. `exportData()` schema `gde-export-v8.0` was therefore not “hardened”: two runs with the same frontier could export different JSON key orders, and operators could not see pattern collapse or fingerprint uniqueness without inspecting `engine.db` directly. Verification needed a deterministic, additive export.

## Decision
- `getCoverageMetrics()`: build `queuedByTypeUnsorted` then copy into `queuedByType` in **alphabetical key order**; compute `patternMetrics`/`clusterMetrics` via `KnowledgeBase.getPatternMetrics()`/`getClusterMetrics()` (or `{size:0}` fallback) and add `patternCount`, `clusterCount`, `fingerprintUnique: fingerprintIndex.size`, `inferenceEnabled: !!CONFIG.inference.patternInference` to the returned object. Sort is O(k log k) with k≤~10 types, cost `<0.01 ms`.
- `exportData()`: snapshot `coverage = getCoverageMetrics()` once, then build `inference = {enabled, patternMetrics, clusterMetrics, fingerprintStats:{unique, total: sum Set sizes}}` bounded top 20, total via `reduce`. Return `{schema:'gde-export-v8.0', exportedAt, config, coverage, inference, engine, ledger, networkEvents, diagnostics}`. Schema stays `v8.0` (additive, JSON-stable sorted keys), ledger remains seq-ordered 5 k FIFO.
- Build: `package.json` version `0.8.2`, dist header `@version 0.8.2` (+80 lines vs 0.8.1, 5864 total, sha `a46d37…`), `scripts/verify-build.js` now asserts `patternCount`/`clusterCount`/`fingerprintUnique`/`inferenceEnabled`/`patternMetrics`/`clusterMetrics`/`fingerprintStats` in dist before hash comparison; comment “no builtAt drift” → “no build-time drift” and forbidden check narrowed to `/"builtAt"/` so the comment no longer trips the gate.

## Consequences
- **+** Operators see `export.coverage.patternCount 3 → collapsed /user/{int} 200` vs `export.inference.patternMetrics.top[0] ["https://a.ex/user/{int}",200]` and `fingerprintUnique 12` without reaching into `db`; `queuedByType {"api":2,"url":1}` is now alphabetically stable for diff tools.
- **+** Deterministic: same frontier → same `JSON.stringify(coverage.queuedByType)`; same pattern/cluster maps → same `top` order (sorted by count); proven by `tests/export-inference.test.js` 6 cases (sorted keys, inference block, pattern collapse, JSON-stable, fingerprint size).
- **−** `exportData` payload grows by ~2 kB (top 20 patterns/clusters); still bounded and export remains `JSON.stringify` with no new network fetch. Schema not bumped, so old consumers ignore `inference` — additive migration noted.
- **−** `fingerprintStats.total` counts `fingerprintIndex` value Set sizes, not distinct bodies — documented as “indexed URLs per hash”.

## Links
- Code: `GenericDiscoveryEngine.getCoverageMetrics()` sorted block, `exportData()` inference snapshot, `dist/generic-discovery-engine.user.js` v0.8.2 header, `scripts/verify-build.js` inference asserts, `dist/.build-meta.json` v0.8.2 (`a46d37…`, 5864).
- Tests: `tests/export-inference.test.js` 6 cases, `tests/e2e-discovery-loop.test.js` still asserts `export.coverage.frontierSize`, `tests/verify-p0-fixes.test.js` now allows `0.8.[0-9]`.
- Prior: ADR 015 build determinism, ADR 019 modular prelude, ADR 013 pattern inference / ADR 014 clustering.
