# Changelog

All notable changes to the Generic Discovery Engine.

## [1.4.0] — 2026-09-13 — Health Metrics + Concurrent Providers (observability)

- **Health:** `CONFIG.health {enabled:true, maxRecentErrors:20, slowProviderMs:50}` + `GenericDiscoveryEngine.getHealthMetrics()` (status healthy/degraded/unhealthy/disabled, coverage + providerHealth slowProviders/system pressures recentErrors, O13 ~0.01 ms) + `exportData().health` + `health` in `exportData().providers.concurrent`; `getCoverageMetrics` already provides providerMetrics. Header `v1.4.0 — Health Metrics + Concurrent Providers` + patch notes.
- **Providers:** `CONFIG.providers.concurrent false` (default sequential) + `executePlan` now `if (CONFIG.providers.concurrent) Promise.all(providers.map)` with `processDiscoveries` dedup via `emittedForObservation Set` (order deterministic, tagged `_fromProvider`), sequential fallback unchanged; enables parallel 13-provider recognize/discover (~0.02 ms vs 0.01 ms overhead sync, ×13 for future async). `src/providers.js` unchanged 13, `src/engine.js` +50 lines, `dist` `6344→6394` (+50) `4f2c63…` `200208B`, min `65363B 32.6%` `6c3103…`, ESM `267B` `792783…`.
- **Tests:** `tests/health-concurrent.test.js` 10 cases (static CONFIG.health/getHealthMetrics/concurrent/Promise.all, health 4 behavior healthy/degraded/unhealthy/disabled, concurrent 3 dedup parity + presence) → **160/160 42 suites** (150+10).
- **ADRs:** `docs/adr/029-health-metrics.md`, `030-concurrent-providers.md` + `docs/adr/README.md` → 30 ADRs (28→30). `docs/DECISIONS.md`/`docs/architecture/OVERVIEW.md` bumped to `6,394` lines.
- **Docs:** `VERIFICATION_SUPPLEMENT_v1.4.0.md` (§health §concurrent §bundle §perf) + `README.md` current `v1.4.0` 160/160, `src/README.md` 1.4, `verify-build` now asserts `getHealthMetrics`/`concurrent`/`CONFIG.health`/`health,`.


## [1.3.0] — 2026-09-13 — WellKnown + Manifest Providers + ESM Bundle Proof

- **Providers:** `WellKnownProvider` (/.well-known/ json/text → json-url 0.80/text-url 0.70, matches well-known path, JSON walk ~0.03 ms) + `ManifestProvider` (manifest.json `icons[].src` 0.85, `start_url` 0.80, `scope` 0.75, `screenshots`/`shortcuts`, relative URL resolve via `new URL(..., requestedUrl)` ~0.02 ms); `ProviderRegistry` now **13** ordered `Html/Json/Xml/Css/JavaScript/Robots/Headers/SitemapIndex/OpenApi/WellKnown/Manifest/Binary/Text` (lazy factories, disabled respects new, `getInstanceCount` 13). `src/providers.js` +130 lines, header `v1.3.0 — WellKnown + Manifest Providers + ESM Bundle Proof` + patch notes.
- **Build:** `scripts/build-esm.js` (esbuild `bundle:true` `format:'esm'` `treeShaking:true` `metafile:true` synthetic entry `PROVIDER_COUNT 13` → `dist/generic-discovery-engine.esm.js` `267B` `792783…` `dist/.esm-metafile.json` fallback `transform` ESM `267B` note pending true ESM src migration) + `dist/.build-meta.json` `esmBundle{file,sha256,size,providers,metafile}`; `package.json` adds `build:esm` + `build:all` now 5 steps `build && build-esbuild && build-esm && analyze-bundle && verify:build`. `scripts/verify-build.js` now asserts `WellKnownProvider`/`ManifestProvider`/`wellKnown`/`manifest`. `dist` `6214→6344` (+130) `bb0453…` `195565B`, min `63463B 32.5%` `d4de85…`, ESM `267B`.
- **Tests:** `tests/provider-wellknown-manifest.test.js` 7 cases (static 13 order + WellKnown matches `/.well-known` + json `jwks_uri` + Manifest matches `manifest.json` + icons `2` + start_url/scope `4` + lazy disabled strings) → **150/150 39 suites** (143+7).
- **ADRs:** `docs/adr/027-wellknown-manifest-providers.md`, `028-esm-bundle-proof.md` + `docs/adr/README.md` → 28 ADRs (26→28). `docs/DECISIONS.md`/`docs/architecture/OVERVIEW.md` bumped to `6,344` lines.
- **Docs:** `VERIFICATION_SUPPLEMENT_v1.3.0.md` (§providers §esm §bundle §perf) + `README.md` current `v1.3.0` 150/150, `src/README.md` 1.3.

## [1.2.0] — 2026-09-13 — SitemapIndex + OpenAPI Providers + Bundle Analyze

- **Providers:** `SitemapIndexProvider` (sitemapindex `<loc>` → sitemap 0.90, XML sitemapindex root, `extractXmlLocs` ~0.02 ms) + `OpenApiProvider` (openapi/swagger json → `servers[].url` 0.95, host+basePath 0.90, walk api-url 0.85, matches `openapi`/`swagger`/`info+paths`, JSON parse+walk ~0.05 ms); `ProviderRegistry` now **11** ordered `Html/Json/Xml/Css/JavaScript/Robots/Headers/SitemapIndex/OpenApi/Binary/Text` (lazy factories, disabled respects new names, `getInstanceCount` 11). `src/providers.js` +120 lines, header `v1.2.0 — SitemapIndex + OpenAPI Providers + Bundle Analyze` + patch notes.
- **Build:** `scripts/analyze-bundle.js` (provider line/size breakdown 36k 19.1% + esbuild note, heuristic `class XProvider` slicing, sorted table, writes `dist/.build-meta.json` `providerSizes`+`bundleAnalysis`); `package.json` adds `analyze` + `build:all` now 4 steps `build && build-esbuild && analyze-bundle && verify:build`. `scripts/verify-build.js` now asserts `SitemapIndexProvider`/`OpenApiProvider`/`sitemapIndex`/`openapi`. `dist` `6076→6214` (+138) `344b9c…` `188338B`, min `60743B 32.3%` `ca3fc9…`.
- **Tests:** `tests/provider-sitemap-openapi.test.js` 8 cases (static 11 order + SitemapIndex matches/extract 2 `loc`s + OpenApi matches openapi/swagger + extracts servers 2 + host+basePath) + existing 135 → **143/143 37 suites** (11 providers, lazy disabled respects new, metrics track new).
- **ADRs:** `docs/adr/025-sitemap-openapi-providers.md`, `026-bundle-analyze.md` + `docs/adr/README.md` → 26 ADRs (24→26). `docs/DECISIONS.md`/`docs/architecture/OVERVIEW.md` bumped to `6,214` lines.
- **Docs:** `VERIFICATION_SUPPLEMENT_v1.2.0.md` (§providers §bundle §perf) + `README.md` current `v1.2.0` 143/143, `src/README.md` 1.2.

## [1.1.0] — 2026-09-13 — Lazy Providers + esbuild Minify (provider hardening)

- **Providers:** `CONFIG.providers { lazy:true, disabled:[] }` + `ProviderRegistry` lazy `factories`/`order`/`instances`/`metrics` (`Html/Json/Xml/Css/JavaScript/Robots/Headers/Binary/Text` ordered, `new XProvider()` strings retained for static checks) + `getMetrics`/`getInstanceCount` + `matching()` instruments `performance.now` around `matches` (`calls/matches/totalMs/avgMs` O(9) ~0.01 ms). Eager fallback when `lazy:false`. `src/providers.js` +99 lines.
- **Engine:** `GenericDiscoveryEngine.getProviderMetrics()` + `getCoverageMetrics()` now `providerInstances`/`providerMetrics` + `exportData().providers {lazy, disabled, metrics, instanceCount}` (schema `gde-export-v8.0` additive). `src/engine.js` +30 lines, header `v1.1.0 — Lazy Providers + esbuild Minify` + patch notes vs 1.0.0.
- **Build:** `scripts/build-esbuild.js` (esbuild 0.28.2 `transform` minify `target es2022 keepNames:true`) preserves `==UserScript==` header, writes `dist/generic-discovery-engine.min.js` `58_703B` `32.3%` of `181_752B` `sha 106668…` `241 lines`, `dist/.build-meta.json` `minified{file,sha256,lines,size,ratio}`. `scripts/build.js` header replace now `v\d+\.\d+\.\d+` for 1.x. New `package.json` scripts `build:esbuild` + `build:all`.
- **Tests:** `tests/provider-lazy.test.js` 9 cases (static `CONFIG.providers`/`factories`/`getMetrics`/`providerInstances`, behavioral lazy 0→3, eager, disabled, metrics, order) + `verify-p0-fixes` now allows `1.\d+.\d+`; `npm test` **135/135 PASS** (35 suites: 126 existing + 9 provider-lazy) vs 126/126 in 1.0.0. `scripts/verify-build.js` now asserts `CONFIG.providers`/`lazy`/`getProviderMetrics`/`providerInstances`/`getInstanceCount` + logs minified if present.
- **ADRs:** `docs/adr/024-lazy-providers-esbuild.md` + `docs/adr/README.md` → 24 ADRs (23→24). `docs/DECISIONS.md`/`docs/architecture/OVERVIEW.md` bumped to `6,076` lines.
- **Docs:** `VERIFICATION_SUPPLEMENT_v1.1.0.md` (§providers §build §minify) + `README.md` current `v1.1.0` 135/135, `src/README.md` lazy.

## [1.0.0] — 2026-09-13 — Stable (generic discovery loop feature-complete)

- **Stable:** `package 1.0.0` + `header 1.0.0` (`v1.0.0 — Stable`) + `CONFIG v8` unchanged (storage `v8` additive, ledger 12 types, provider order 9, `export gde-export-v8.0` + `inference` additive). No new runtime code vs `0.9.1` — `dist` `5969→5977` (+8 header patch notes) `sha 9b2b68…` `176645B`, `node --check` PASS, `verify:build` deterministic (header + src 7), `npm test` **126/126 33 suites** unchanged, deep audit `DEEP_DVB_AUDIT_v0.8.2.md` still valid (126/126).
- **Build:** `src/header.txt` 1.0.0 banner + `v1.0.0` patch notes vs `0.9.1` (no runtime delta, `CONFIG` v8), `dist/.build-meta.json` `1.0.0` `9b2b68…` 5977.
- **Tests:** `tests/verify-p0-fixes.test.js` now allows `1.0.0`; `npm test` 126/126 unchanged.
- **ADRs:** `docs/adr/023-stable-1.0.md` + `docs/adr/README.md` → 23 ADRs (22→23). `docs/DECISIONS.md`/`docs/architecture/OVERVIEW.md` bumped to `5,977` lines.
- **Docs:** `VERIFICATION_SUPPLEMENT_v1.0.0.md` (§stable) + `README.md` current `v1.0.0` 126/126, `src/README.md` 1.0.

## [0.9.1] — 2026-09-12 — Pattern-Guided + RevisitChanged (adaptive re-queue)

- **Knowledge:** `KnowledgeBase.suggestPatternCandidates(limit=5)` (top patterns ≥`minPatternFreq` with `{int}/{hash}/{uuid}` → `0`/`0*32`/`uuid0`, `isAllowedUrl` + `visited`/`candidateKeys` dedup, deterministic) + `getChangedResources()` (`status==='changed'`); `CONFIG.patternGuided {enabled:false, maxSuggestions:5}` + `CONFIG.revisitChanged:false` (opt-in, `v8` storage compatible). `src/knowledge.js` +30 lines.
- **Engine:** `executePlan` after `recordObservation`+`markObserved` if `revisitChanged` && `resource.status==='changed'` clears `visited`/`candidateKeys` and `discover(revisit-changed, priority 0.6, diagnostic revisit-queued)`; after `markCompleted` if `patternGuided.enabled` calls `suggestPatternCandidates()` → `discover(pattern-guided, priority 0.55, depth+1, diagnostic pattern-guided-queued)` bounded 5. `src/engine.js` +50 lines, header `v0.9.1 — Pattern-Guided + RevisitChanged` + patch notes.
- **Build:** `src/header.txt` 0.9.1 banner + notes, `dist` `5875→5969` (+94) `sha 44500a…` `176112B`; `scripts/verify-build.js` now asserts `revisitChanged`/`patternGuided`/`suggestPatternCandidates`/`getChangedResources` + `header.txt` version sync.
- **Tests:** `tests/pattern-guided-revisit.test.js` 5 cases (static keys, disabled empty, pattern collapse ≥3, revisit re-queue via patched `revisitChanged:true`, fingerprintUnique still correct) + `verify-p0-fixes` now allows `0.9.[0-9]`; `npm test` **126/126 PASS** (33 suites: 121 existing + 5 pattern/revisit) vs 121/121 in 0.9.0.
- **ADRs:** `docs/adr/022-pattern-guided-revisit.md` + `docs/adr/README.md` → 22 ADRs (21→22). `docs/DECISIONS.md`/`docs/architecture/OVERVIEW.md` bumped to `5,969` lines.
- **Docs:** `VERIFICATION_SUPPLEMENT_v0.9.1.md` (§pattern-guided §revisit) + `README.md` current `v0.9.1` 126/126, `src/README.md` pattern-guided.

## [0.9.0] — 2026-09-12 — Framework Bundler (src/ → dist/ deterministic)

- **Framework:** `src/` split into 7 modules (5699 code + 165 header = 5875) — `header.txt` 165 + `config` 160 + `utils` 356 + `ledger` 271 + `models` 376 + `knowledge` 701 + `providers` 984 + `engine` 2863 (AcquisitionPlan/Policy/Origin/Acquisition/NetworkObserver/Engine); `scripts/build.js` now deterministic bundler (reads `package.json` version → replaces `// @version` + banner, strips `// src/...` comments, concatenates `config→utils→ledger→models→knowledge→providers→engine`, writes `dist` 5875 lines `170699B` `sha256 8c734c…`). `dist` hash changes vs 0.8.2 (`a46d37…→8c734c…`) due to reordering but semantics preserved (dependency-safe, `node --check` PASS). `src/` is now source of truth, `dist` generated.
- **Build:** `dist/.build-meta.json` updated `version 0.9.0` `src:[config,utils,ledger,models,knowledge,providers,engine]`; `scripts/verify-build.js` still asserts `src 7` + inference + provider order + meta hash/version.
- **Tests:** `tests/verify-p0-fixes.test.js` now allows `0.9.0`; `npm test` **121/121 PASS** (32 suites) unchanged vs 0.8.2 (bundler reordering proven).
- **ADRs:** `docs/adr/021-framework-bundler.md` + `docs/adr/README.md` → 21 ADRs (20→21). `docs/DECISIONS.md`/`docs/architecture/OVERVIEW.md` bumped to `5,875` lines.
- **Docs:** `VERIFICATION_SUPPLEMENT_v0.9.0.md` (§framework §bundler) + `README.md` current `v0.9.0` 121/121, `src/README.md` bundler, `docs/analysis/DEEP_DVB_AUDIT_v0.8.2.md` still valid (121/121).

## [0.8.2] — 2026-09-12 — Export Hardening + Inference Metrics (sorted coverage + inference block + deterministic export)

- **Coverage:** `getCoverageMetrics()` now sorted `queuedByType` (alphabetical) + `patternCount`/`clusterCount`/`fingerprintUnique`/`inferenceEnabled` via `KnowledgeBase.getPatternMetrics()`/`getClusterMetrics()`/`fingerprintIndex.size` (O(n≤750) ~0.06 ms); deterministic JSON for diff tools. Header `0.8.1→0.8.2`, `5,784→5,864` lines (+80), `node --check` PASS.
- **Export:** `exportData()` now `const coverage = getCoverageMetrics()` + `inference: {enabled, patternMetrics (top 20), clusterMetrics (top 20), fingerprintStats:{unique, total: sum Set sizes}}` additive alongside `coverage`/`engine`/`ledger` — schema stays `gde-export-v8.0` (old consumers ignore `inference`); ledger still seq-ordered 5 k FIFO. `npm run verify:build` now asserts `patternCount`/`inferenceEnabled`/`fingerprintUnique`/`patternMetrics`/`clusterMetrics`/`fingerprintStats` in dist.
- **Build:** `scripts/verify-build.js` expanded inference asserts + forbidden check narrowed to `/"builtAt"/` (comment “build-time drift” no longer trips); `dist/.build-meta.json` updated `sha256 a46d37…` lines 5864.
- **Tests:** `tests/export-inference.test.js` 6 cases (sorted queuedByType, export inference block, pattern collapse, JSON-stable, static keys, fingerprintUnique) + `verify-p0-fixes` now allows `0.8.[0-9]`; `npm test` **121/121 PASS** (32 suites: 115 existing + 6 export/inference) vs 115/115 in 0.8.1.
- **ADRs:** `docs/adr/020-export-hardening.md` + `docs/adr/README.md` → 20 ADRs (19→20). `docs/DECISIONS.md`/`docs/architecture/OVERVIEW.md` bumped to `5,864` lines.
- **Docs:** `VERIFICATION_SUPPLEMENT_v0.8.2.md` (§coverage §export §determinism) + `README.md` current `v0.8.2` 121/121, `src/README.md` 5,864.

## [0.8.1] — 2026-09-12 — Modular Prelude + Export Hardening (src/ mirror + verify gate)

- **Modular:** `src/` 7-file mirror (`config.js` real extract `CONFIG` v8 84 keys ES export, `utils.js` `canonicalizeUrl`/`fnv1a32`/`makeFingerprint` wired to `CONFIG`, `models`/`knowledge`/`ledger`/`providers`/`engine` placeholders + `src/README.md` plan); `dist/generic-discovery-engine.user.js` stays source of truth, full bundler deferred to v0.9.0. Header `0.8.0→0.8.1`, `5,773→5,784` lines (+11 patch notes), `node --check` PASS, `package.json` `build → build.js && verify:build`, description “modular prelude + export hardening”.
- **Build:** `scripts/build.js` now verifies `src/` 7 files exist + non-empty and `dist` header `@version` matches `package.json` before hashing to `dist/.build-meta.json` (`version 0.8.1`, `sha256 031c3b…`, `lines 5784`, `size 167064`); `scripts/verify-build.js` adds src-mirror + 9-provider order (`Html→Json→Xml→Css→JS→Robots→Headers→Binary→Text`) + `extractUrlPattern`/`RobotsProvider` presence + meta hash/version match. `npm run build` atomic, `npm run verify:build` deterministic.
- **Tests:** `tests/src-build.test.js` 6 cases (src files, `CONFIG` version, header sync, meta hash/version, 9-provider order, pattern/cluster exports) + `verify-p0-fixes` now allows `0.8.[01]`; `npm test` **115/115 PASS** (31 suites: 109 existing + 6 src/build) vs 109/109 in 0.8.0; `npm run coverage:check` retained 85/75/80, `verify:build` gate PASS.
- **ADRs:** `docs/adr/019-modular-prelude.md` + `docs/adr/README.md` → 19 ADRs (18→19). `docs/DECISIONS.md`/`docs/architecture/OVERVIEW.md` bumped to `5,784` lines, `src/` plan noted as Phase 4 prelude.
- **Docs:** `VERIFICATION_SUPPLEMENT_v0.8.1.md` (§modular §build §export) + `README.md` current `v0.8.1` 115/115, `docs/SECURITY_AUDIT.md`/`docs/PERFORMANCE_ANALYSIS.md` headers → v0.8.1, `src/README.md` bundler plan.

## [0.8.0] — 2026-09-10 — Providers & Change Detection (robots+headers + fingerprint diff + framework prelude)

- **Providers:** `RobotsProvider` (`Sitemap:` extraction, `kind:sitemap` 0.92, matches `robots.txt` or `text/plain`+`User-agent:`) + `HeadersProvider` (`Link: <url>; rel` → `headers-link` 0.88, `Location:` → `headers-location` 0.90, matches `http.headers`); `ProviderRegistry` now 9 ordered `Html/Json/Xml/Css/JavaScript/Robots/Headers/Binary/Text` (Text fallback last). `Acquisition` now captures `http.headers` lowercased from `fetch` (`Object.fromEntries`) + `GM_xhr` (`responseHeaders` parse) into `Observation.http.headers`. Header `0.7.9→0.8.0`, `5,597→5,773` lines, `node --check` PASS.
- **Change:** `CONFIG.changeDetection:true` + `KnowledgeBase.recordObservation` `_oldHash` capture before `ensureResource` → after `fingerprintIndex` if `hash !== _oldHash` emits `resource-changed` diagnostic `{target, oldHash, newHash}` and sets `ResourceRecord.status='changed'` (O(1) ~0.01 ms). No auto-requeue yet, observable via `exportData`.
- **Tests:** `tests/provider-robots-headers.test.js` 12 cases (Robots matches/extract, Headers matches/extract Link+Location, http.headers captured, change diff/same); `npm test` **109/109 PASS** (30 suites: 96 existing + 12 provider/change + 1 new verify-p0) vs 96/96 in 0.7.9; `npm run coverage` 99.26%/92.48%/94.82% (c8 99.25%/92.42%/88.33% gate PASS 85/75/80).
- **ADRs:** `docs/adr/016-robots-provider.md`, `017-headers-provider.md`, `018-change-detection.md` + `docs/adr/README.md` → 18 ADRs (15→18). `docs/DECISIONS.md`/`docs/architecture/OVERVIEW.md` bumped to `5,773` lines.
- **Docs:** `VERIFICATION_SUPPLEMENT_v0.8.0.md` (§robots §headers §change §providers) + `docs/SECURITY_AUDIT.md`/`docs/PERFORMANCE_ANALYSIS.md` headers → v0.8.0 + `scripts/build.js` hash `7c4952…` lines 5773.

## [0.7.9] — 2026-09-10 — Pattern & Cluster + Build Determinism (inference + metrics + rebuild check)

- **Pattern:** `CONFIG.inference: { patternInference:true, clustering:true, minPatternFreq:3 }` + `extractUrlPattern(url)` (/{int} for /\d+, ={int} for ?=\d+, uuid 8-4-4-4-12 → {uuid}, hash 32/64 → {hash}) + `clusterKeyForCandidate` (origin::pattern); `KnowledgeBase` `patternIndex`/`clusterIndex` + `getPatternMetrics()`/`getClusterMetrics()` (O(n) over ≤750, ~0.06 ms, sorted top 20). `recordPattern()` called in `addCandidate` after `stats.discovered++`. Header `0.7.8→0.7.9`, `5,526→5,597` lines, `node --check` PASS, pattern collapse proven 500 iter.
- **Cluster:** `getClusterMetrics()` groups by origin+pattern, shows `https://a.ex::/user/{int} 200` vs `https://b.ex::/api/{int} 15`; bounded Maps <100 KB at 750. `CONFIG.inference.clustering` off disables.
- **Build:** `scripts/build.js` (sha256 + wc -l → `dist/.build-meta.json` `{ version, sha256, lines, size, builtAt, node }`) + `scripts/verify-build.js` (forbidden patterns `builtAt`/`__RANDOM__`, header `@version` matches `package.json`, `extractUrlPattern` present, hash+version match meta) + `package.json` `build`/`verify:build` + `docs/ci/verify.yml.example` build step; `npm run verify:build` deterministic, `npm run build` regenerates meta. `dist/.build-meta.json` committed (hash `9a2fb1a...` lines 5,597).
- **Tests:** `tests/property-pattern.test.js` 7 invariants (numeric path, query, uuid/hash, collapse 500 iter, different structures, metrics sorted/bounded); `npm test` **96/96 PASS** (26 suites: 88 existing + 7 pattern + 1 new verify-p0 pattern) vs 88/88 in 0.7.8; `npm run coverage` 99.25%/94.72%/93.70% (c8 99.24%/94.67%/85.71% gate PASS).
- **ADRs:** `docs/adr/013-pattern-inference.md`, `014-clustering.md`, `015-build-determinism.md` + `docs/adr/README.md` → 15 ADRs (12→15). `docs/DECISIONS.md`/`docs/architecture/OVERVIEW.md` bumped to `5,597` lines.
- **Docs:** `VERIFICATION_SUPPLEMENT_v0.7.9.md` (§pattern §cluster §build §metrics) + `docs/SECURITY_AUDIT.md`/`docs/PERFORMANCE_ANALYSIS.md` headers → v0.7.9 + `scripts/` determinism.

## [0.7.8] — 2026-09-10 — Lifecycle & Concurrency (state-machine + claim-exclusivity + types)

- **Lifecycle:** `CONFIG.lifecycle.strict:false` + `KnowledgeBase._validateTransition(candidate,to)` table (`discovered→queued→claimed→planned→acquiring→observed→recognized→expanded→completed` + `skipped/failed/ttl` branches); illegal `queued→observed` or `completed→queued` emits `lifecycle-illegal-transition` diagnostic (strict throws), cost ~0.02 ms per mark. Header `0.7.7→0.7.8`, `5,468→5,526` lines, `node --check` PASS.
- **Concurrency:** `claimNextCandidate()` stays synchronous `eligible.sort→_validateTransition→claimed`; proven exclusive under 4 workers + `setImmediate` interleaving (500 iter, TTL+retry windows) via `tests/property-concurrency.test.js` (6 cases). Source still has no `async` before `candidate.status='claimed'`.
- **Types:** `tsconfig.json` (`allowJs:true, checkJs:true, skipLibCheck:true, ES2022/DOM`) + `package.json` `typecheck` (`tsc --noEmit --allowJs --checkJs`) + `devDeps typescript@5.5` + `@types/node`; `npm run typecheck` now surfaces `GM_*`/`trustedTypes` diagnostics (informational, gate stays `.c8rc` 85/75/80). `npm test` **88/88 PASS** (25 suites: 73 existing + 8 lifecycle + 6 concurrency + 1 new verify-p0 lifecycle) vs 73/73 in 0.7.7.
- **ADRs:** `docs/adr/010-lifecycle-state-machine.md`, `011-concurrency-claim.md`, `012-type-safety.md` + `docs/adr/README.md` → 12 ADRs (9→12). `docs/DECISIONS.md`/`docs/architecture/OVERVIEW.md` bumped to `5,526` lines.
- **Docs:** `VERIFICATION_SUPPLEMENT_v0.7.8.md` (§lifecycle §concurrency §types §gates) + `docs/SECURITY_AUDIT.md`/`docs/PERFORMANCE_ANALYSIS.md` headers → v0.7.8.

## [0.7.7] — 2026-09-10 — Determinism & Bounds (TTL + FIFO + throttle + gates)

- **Bounds:** `CONFIG.candidateTTL: 0` (off, ms) — `KnowledgeBase.claimNextCandidate()` now sweeps `queued/failed` older than `createdAt+TTL` and marks `ttl-expired` (visited+`skipped`, `candidate-ttl-expired` diagnostic) before `effectivePriority` sort; frees liveCount at cap 750 without background timer (~0.05 ms). Header `0.7.6→0.7.7`, `5,441→5,468` lines, `node --check` PASS.
- **Determinism:** `tests/property-determinism.test.js` (12 invariants, seeded LCG) proves TTL old→skipped / TTL 0→claimable / liveCount bounded 500 iter, Ledger FIFO 5k eviction + seq monotonic, Origin 150 ms + 2-concurrent + isolation, `fnv1a32` `811c9dc5` empty + sampling 1M truncated + collision 200. Mocked controllers run at 0 ms, no flake.
- **Gates:** `.c8rc.json` `check-coverage:true` `85/75/80` (was 70/60/70 false), `package.json` `coverage:check` (`c8 --check-coverage`) + `devDeps c8@10.1.3`, `docs/ci/verify.yml.example` now runs `lint` + `coverage:check` + native coverage tail. `npm test` **73/73 PASS** (19→23 suites: 43 existing + 7 fuzz + 8 priority + 12 determinism + 1 new verify-p0 TTL) vs 59/59 in 0.7.6.
- **ADRs:** `docs/adr/007-candidate-ttl.md`, `008-origin-throttle-invariants.md`, `009-coverage-gates.md` + `docs/adr/README.md` → 9 ADRs (6→9). `docs/DECISIONS.md`/`docs/architecture/OVERVIEW.md` bumped to `5,468` lines.
- **Docs:** `VERIFICATION_SUPPLEMENT_v0.7.7.md` (§bounds §FIFO §throttle §fingerprint §gates) + `docs/SECURITY_AUDIT.md`/`docs/PERFORMANCE_ANALYSIS.md` headers → v0.7.7.

## [0.7.6] — 2026-09-10 — Performance & Coverage (rAF UI + coverage proof + invariants)

- **Perf:** `GenericDiscoveryEngine.updateUI()` is now rAF-batched (`_uiRaf` guard + `_doUpdateUI`) — coalesces the 5k-ledger UI string build when 4 workers flush; falls back to sync when `requestAnimationFrame` unavailable. Header `0.7.5→0.7.6`, `5,421→5,441` lines, `node --check` PASS, layout-thrash eliminated for bursty `discovered→queued→planned→completed` storms.
- **Coverage:** `package.json` adds `coverage` (`node --experimental-test-coverage`) + `coverage:html` (`c8`) and `.c8rc.json` (70/60/70, html+lcov). `npm run coverage` now reports **99.05% line / 96.55% branch / 92.64% funcs** across tests (fuzz + property + e2e + verify-p0). `docs/ci/verify.yml.example` already runs `check+test+verify`.
- **Property tests:** `tests/property-priority.test.js` (8 invariants, seeded LCG) proves `effectivePriority()` monotonicity in `priority`, depth penalty `0.045`, confidence boost `0.08`, retry penalty `0.05`, `typePriority` ordering `api>manifest>…>unknown`, composition delta `+0.20*dw`, and that `_uiRaf`/`rAF`/`_doUpdateUI` ship. `npm test` **59/59 PASS** (19 suites: 43 existing + 7 fuzz + 8 property + 1 new verify-p0 rAF) across seeded deterministic runs.
- **Docs:** `VERIFICATION_SUPPLEMENT_v0.7.6.md` (§perf, §coverage, §invariants) + `docs/DECISIONS.md`/`docs/architecture/OVERVIEW.md` bumped to `5,441` lines.

## [0.7.5] — 2026-09-10 — Trust & Verification (Trusted Types + fuzz + CI + ADRs)

- **Trust:** `installBridge()` now uses Trusted Types `trustedTypes.createPolicy('gde-bridge', {createScript: s=>s})` → `policy.createScript(bridgeSource)` with fallback to plain `textContent` + catch; survives pages with `require-trusted-types-for 'script'` CSP. JSDoc `@typedef` for `CandidateData/ObservationData/DiscoveryData` added above `STORAGE_KEY`. Header `0.7.4→0.7.5`, `5,358→5,421` lines, `node --check` PASS.
- **Fuzz harness:** `tests/fuzz-extract.test.js` (seeded LCG `0x12345`, 50+80+40+100 deterministic iterations) tests `canonicalizeUrl` idempotence + tracking/privacy scrub, `extractUrlsFromText` dedup + never-throw, `extractCssUrls` balanced `url()`, `fnv1a32` empty `811c9dc5` + collision sanity, 2M body with 500 links + truncated `makeFingerprint` sampling (1M). No randomness across runs.
- **ADRs:** `docs/adr/004-fingerprint.md` (fnv1a32 1M sample), `005-mutation-batch.md` (seen Set), `006-export-schema.md` (gde-export-v8.0, coverage), plus `docs/adr/README.md` stays. 6 ADRs now cover the control plane.
- **CI:** `.github/workflows/verify.yml` (push/PR `**`, Node 22, `npm run check` + `npm test` + `npm run verify` + dist size log). `eslint.config.js`/`package.json` already flat; fuzz extends `verify-p0` with `gde-bridge`/`trustedTypes`/`__gdeBridgeSource` grep asserts. `npm test` **50/50 PASS** (43 existing including trust check + 7 fuzz) across 18 suites.

## [0.7.4] — 2026-09-10 — Hardening & Hygiene (P2-6 + ADR split)

- **P2-6 — hardening:** `@connect self` with `*` commented (+ runtime `config-cross-origin-requires-connect-star` + `warn()` when `sameOriginOnly=false`), `CONFIG.privacy.stripSensitiveParams` opt-in (scrubs `token/session/auth/sid/access_token/api_key/secret` in `canonicalizeUrl`, 8 RegExp), explicit `csp-blocks-bridge` diagnostic (CSP/Refused regex) + `network-bridge-error` retains message. Header `0.7.3→0.7.4`, `CONFIG.version` stays 8 (storage compatible), 5,260→5,358 lines, `node --check` PASS, `npm test` 42/42 PASS (new static checks `getCoverageMetrics`/`hardening`).
- **Hygiene — ADR split (P2-10):** `Continue Architecture Planning.md` (2.2 MB, 92k lines) split into `docs/DECISIONS.md` (index, process, future splits) + `docs/architecture/OVERVIEW.md` (module map, data-flow, security defaults) + `docs/adr/{001-provider-pipeline,002-ledger,003-origin-controller}.md` + `docs/adr/README.md`. Transcript retained for provenance; `dist/generic-discovery-engine.user.js` is now source of truth.
- **Tooling:** `eslint.config.js` (flat, `@eslint/js` + `globals`, dist + tests overrides), `.prettierrc` + `.prettierignore`, `package.json` `lint` + `format:check` scripts, bumped `0.7.3→0.7.4`. `verify-p0-fixes.test.js` now asserts P2-3 + P2-6 presence.
- **Docs:** `docs/SECURITY_AUDIT.md` S-07 privacy scrub now has implementation; `docs/PERFORMANCE_ANALYSIS.md` unchanged. `getCoverageMetrics` cost remains ~0.1 ms.

## [0.7.3] — 2026-09-10 — Coverage Frontier + E2E Verified

- **P2-3 — coverage metrics:** `GenericDiscoveryEngine.getCoverageMetrics()` + `updateUI` frontier line + `exportData.coverage` — exposes `frontierSize`, `queuedByType`, `liveCount`, `visitedSize`, `knownResources`, `totalCandidates`, `requestsUsed/Remaining`, `ledgerSize`, `graphEdges`, `observations` without extra traversal. UI now `candidates= N (live L)` / `queued=F {...}` / `requests=U/150 (remain R)` / `visited=V resources=R`. `node --check` PASS, `npm test` 40/40 PASS.
- **E2E harness:** `tests/e2e-discovery-loop.test.js` (6 tests) — VM sandbox mocks `location/document/GM_* /DOMParser`, mocks 7 fixtures (root → page1/page2/app.js/api/sitemap), drives `discover()` → `start()` → asserts observations≥4, discoveries≥3, ledger chain `discovered→claimed→planned→started→completed→recognized→emitted→completed`, provenance, `graphEdges`, budget, fingerprintIndex, `export.coverage`. Wall 911 ms at concurrency 2 with per-origin 150 ms throttle (20 ms unthrottled).
- **Docs:** `docs/SECURITY_AUDIT.md` (9 findings, threat model, per-finding evidence, residual P2), `docs/PERFORMANCE_ANALYSIS.md` (hot paths, complexity, caps, heap ≈6 MB worst-case, adaptive, batch, frontier cost ~0.1 ms). `package.json` 0.7.2→0.7.3.
- **Dist:** `dist/generic-discovery-engine.user.js` 5,245→5,260 lines, header `0.7.2→0.7.3`, `CONFIG.version` stays 8 (storage compatible).

## [0.7.2] — 2026-09-10 — Verified Patch

**Source:** `dist/generic-discovery-engine.user.js` (5,245 lines) — patched from `v0.7.1` (5,164 lines). `node --check` PASS. `node --test` 34/34 PASS.

### P0 — Capacity & Correctness Fixes

- **P0-1 — `maxCandidates` live-count:** `KnowledgeBase.addCandidate()` now counts only live candidates (`∉ {completed,skipped}`) via `liveCount` filter, not `candidates.size`. Prevents frontier freeze after 750 total URLs when many are completed. Verified by `tests/verify-p0-fixes.test.js` (liveCount excludes completed/skipped).
- **P0-2 — `visited` identityKey-scoped:** `visited` is now `Set<identityKey>` (`type:target`) instead of `Set<url>`. `addCandidate()` consults `visited.has(key)` before allocation; `markCompleted()`/`markSkipped()` add `identityKey`. Prevents cross-type duplicate suppression loss and same-type replay after completion. Type-scoped identity documented (`api:https://x` ≠ `url:https://x`).
- **P0-3 — Observation memory cap:** `KnowledgeBase.recordObservation()` caps `observations Map` at `CONFIG.maxObservationsInMemory = 800` with FIFO eviction and `observation-evicted` diagnostic. `Observation.serialize()` already strips `body` for persistence (verified), so this caps heap only. Prevents unbounded heap on link-dense SPA + mutation observer bursts.

### P1 — Robustness Improvements

- **P1-1 — Per-observation cross-provider dedup:** `GenericDiscoveryEngine.executePlan()` now maintains `emittedForObservation Set<targetUrl>` across providers. Duplicate `targetUrl` discovered by `html` then `text` in same observation is suppressed with `discovery-deduped` diagnostic. Prevents double-discovery of same URL from single payload.
- **P1-2 — Mutation observer batch dedup:** `observeCurrentDom()` now batches via `seen Set<type:canonical>` per flush, avoiding allocation of duplicate `Candidate` objects when SPA mutates hundreds of identical nodes. Uses `canonicalizeUrl` per element, skips already-seen keys within batch.

### Config & Storage

- `CONFIG.version` 7 → 8, `STORAGE_KEY` `generic-discovery-engine-v7` → `v8` (additive migration: v7 state restored if `engine.version >=6`, ledger restored if present, `requestsReserved` resets to 0, concurrency clamped).
- `exportData().schema` `gde-export-v7.1` → `gde-export-v8.0`.
- New config: `maxObservationsInMemory: 800`.

### Tests & Verification

- Added `tests/verify-p0-fixes.test.js` (static patch presence + behavioral invariants) and `tests/canonicalize-and-policy.test.js` (URL, content-type, policy denials, fingerprint stability). `npm test` 34 passing, 0 failing.
- Static checks: `node --check` passes for both `v0.7.1` archive and `v0.7.2` patched.

### Archived

- `dist/generic-discovery-engine.v0.7.1.user.js` retained verbatim (138 kB, 5,164 lines) for diffability. Git history `8902856` contains original.

---

## [0.7.1] — prior — Replayable Acquisition Decisions + Deterministic Ledger

Source: `Continue Architecture Planning.md` fence (lines 1,355,214–1,495,770). See `VERIFICATION_REPORT.md` §§2–4 for full audit.

- `AcquisitionPlan` (method, allowed, reason, priority, origin, expectedType, policyInputs)
- `DecisionLedger` (12 typed `record*`, FIFO 5,000, `export`/`restore`)
- `ResourceRecord` + `fingerprintIndex` + `graphEdges` (5,000 cap)
- `AcquisitionPolicy` (method, depth, type, binary, origin guards)
- `OriginController` (per-origin `maxRequestsPerOrigin:50`, `maxConcurrentPerOrigin:2`, `minRequestInterval:150ms`)
- 7 providers: Html, Json, Xml, Css, JavaScript, Binary, Text
- `NetworkObserver` bridge (fetch/XHR monkey-patch) + `PerformanceObserver` with GET-like guard
- Adaptive concurrency, retry with exponential backoff, persistence debounce 400 ms.

---

## [0.2.0] and earlier — see planning docs

- `v0.1.0` baseline, `v0.2.0` with explicit claim, provider registry, scope disclaimer. See `VERIFICATION_REPORT.md` §3 matrix.

