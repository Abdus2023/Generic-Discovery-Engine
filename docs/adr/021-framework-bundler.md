# ADR 021 — Framework Bundler (src/ → dist/ deterministic)

**Status:** accepted (v0.9.0)  
**Transcript:** Phase 4 framework split — *src/ as source of truth*  
**Code:** `src/header.txt` + `src/config.js`/`utils.js`/`models.js`/`ledger.js`/`knowledge.js`/`providers.js`/`engine.js` (5699 lines code + 165 header = 5875), `scripts/build.js` concatenating bundler, `dist/generic-discovery-engine.user.js` generated artifact, `dist/.build-meta.json` sha `8c734c…`

## Context
`dist/generic-discovery-engine.user.js` grew as a 5,864-line monolith. Verifying a single provider required grepping the whole file; `src/` existed as a 7-file mirror (v0.8.1) but `dist` was still hand-edited, so drift was possible despite `verify:build` hashing. The roadmap called for `src/` to become the source of truth and `dist` to be a deterministic build, preserving the `sha256`/`lines` gate (ADR 015) while enabling modular review and future tree-shaking.

## Decision
- **Split** `dist` into 7 `src/` modules by contiguous original order, verified to total 5699 code lines + 165 header = 5875:
  * `src/header.txt` — `==UserScript==` metadata + ` (function () {'use strict';` + patch-notes banner (165 lines, version placeholder `0.8.2` → replaced by build).
  * `src/config.js` — `CONFIG` v8 84 keys (160 lines).
  * `src/utils.js` — `log`/`warn`…`originOf`/`canonicalizeUrl`…`fnv1a32`/`makeFingerprint`/`extractUrlPattern`/`clusterKey`/`contentTypeForTarget` (356 lines).
  * `src/ledger.js` — `DecisionLedger` 12 types 5k FIFO (271 lines).
  * `src/models.js` — `Candidate`/`Observation`/`Discovery`/`ResourceRecord` (376 lines).
  * `src/knowledge.js` — `KnowledgeBase` (701 lines, `visited` identityKey, `liveCount`, `candidateTTL` sweep, `_validateTransition`, `patternIndex`/`clusterIndex`, `_oldHash` change detection, `fingerprintIndex`).
  * `src/providers.js` — `Provider` + 9 providers `Html/Json/Xml/Css/JS/Text/Robots/Headers/Binary` + `ProviderRegistry` ordered 9 (984 lines, `Text` fallback last).
  * `src/engine.js` — `AcquisitionPlan`, `AcquisitionPolicy`, `OriginController`, `Acquisition` (GM_xhr + fetch), `NetworkObserver` (bridge `gde-bridge` Trusted Types + `PerformanceObserver` GET-trust), `GenericDiscoveryEngine` (discover/plan/execute/worker/adaptive/persist/UI rAF + coverage/export hardening) (2863 lines with section comments).
- **Bundler** `scripts/build.js` v0.9.0: reads `package.json` version, loads `src/header.txt` and replaces `// @version 0.x.y` + `v0.x.y —` banner, strips leading `// src/...` comment from each module, concatenates in dependency-safe order `config → utils → ledger → models → knowledge → providers → engine` (ledger before models, engine last ensures `AcquisitionPlan` et al. defined before `GenericDiscoveryEngine` instantiates), writes `dist/generic-discovery-engine.user.js` 5875 lines `170699B` `sha256 8c734c…`, records `dist/.build-meta.json` `{version, sha256, lines, size, src:[7], builtAt, node}`. No external bundler (no esbuild/rollup) — pure `node:fs`/`node:crypto`, deterministic `wc -l` via `/\n/g`.

## Consequences
- **+** Reviewable: `src/knowledge.js` diff for TTL no longer buried in monolith; `src/providers.js` diff for `RobotsProvider` isolated; `git blame` per module.
- **+** Deterministic: same `src/` → same `dist` hash (`8c734c…`); `verify:build` still asserts `header @version`, `src 7` existence, `extractUrlPattern`/`RobotsProvider`/`patternCount`… present, meta `sha256`/`version` match; reordering is dependency-safe (all classes defined before `engine` boot `window.GenericDiscoveryEngine = new …; engine.init()`), proven by `npm test` 121/121 32 suites unchanged.
- **−** `src/` modules are still plain IIFE snippets (no `import/export` tree-shaking) — true ES-module bundling deferred; `src/header.txt` is not JS and must be handled specially.
- **−** Concatenation order `ledger→models→knowledge` differs from original `AcquisitionPlan→ledger→models` (original had `AcquisitionPlan` before `ledger`), so `dist` hash changes vs 0.8.2 (`a46d37…`→`8c734c…`) even though runtime semantics preserved — documented as intentional framework split.

## Links
- Code: `src/header.txt` 165, `src/config.js` 160, `src/utils.js` 356, `src/ledger.js` 271, `src/models.js` 376, `src/knowledge.js` 701, `src/providers.js` 984, `src/engine.js` 2863 → `dist` 5875, `scripts/build.js` bundler, `dist/.build-meta.json` v0.9.0.
- Tests: `npm test` 121/121 (unchanged), `tests/verify-p0-fixes.test.js` now allows `0.9.0`, `tests/export-inference.test.js` still 6, `node --check` PASS.
- Prior: ADR 015 build determinism, ADR 019 modular prelude (mirror), ADR 020 export hardening.
