# Architecture Overview — Generic Discovery Engine v1.5.0

**Runnable artifact:** `dist/generic-discovery-engine.user.js` (6,453 lines, CONFIG v8, built from `src/` 7 modules, `node --check` PASS) + `dist/generic-discovery-engine.min.js` (66k 32.7% esbuild) + `dist/generic-discovery-engine.esm.js` (267B ESM) + bundle analyze 20.6% + `src/` 7-file mirror (config/utils extracts)  
**Transcript source:** `Continue Architecture Planning.md` (2.2 MB) → split into `docs/DECISIONS.md` + `docs/adr/*` (v0.7.4)  
**Verification:** `VERIFICATION_REPORT.md` (v0.7.1) + `VERIFICATION_SUPPLEMENT_v0.7.2.md` + `VERIFICATION_SUPPLEMENT_v0.7.6.md` + `VERIFICATION_SUPPLEMENT_v0.7.7.md` + `VERIFICATION_SUPPLEMENT_v0.7.8.md` + `VERIFICATION_SUPPLEMENT_v0.7.9.md` + `VERIFICATION_SUPPLEMENT_v0.8.0.md` + `VERIFICATION_SUPPLEMENT_v0.8.1.md + `VERIFICATION_SUPPLEMENT_v0.8.2.md` + `VERIFICATION_SUPPLEMENT_v0.9.0.md` + `VERIFICATION_SUPPLEMENT_v0.9.1.md` + `VERIFICATION_SUPPLEMENT_v1.0.0.md` + `VERIFICATION_SUPPLEMENT_v1.1.0.md` + `VERIFICATION_SUPPLEMENT_v1.2.0.md` + `VERIFICATION_SUPPLEMENT_v1.3.0.md` + `VERIFICATION_SUPPLEMENT_v1.4.0.md` + `docs/analysis/DEEP_VERIFICATION_v1.4.md` + `docs/SECURITY_AUDIT.md` + `docs/PERFORMANCE_ANALYSIS.md` — `npm test` 160/160 PASS

## 1. Control Architecture (DVB-inspired, not DVB-compatible)

```
DVB blind scan                  Generic discovery
─────────────────               ─────────────────
frequency                       candidate (URL + type, depth, priority, hints)
signal detection                acquire (GM_xmlhttpRequest / fetch)
demod acquisition               observation (status, http, body, fingerprint)
validation / PSI                recognition (provider matches)
NIT / new mux                   expansion (new candidates with provenance)
```

The loop is `DISCOVERY → KNOWLEDGE GRAPH → ACQUISITION PLAN → SCHEDULER → ACQUISITION → OBSERVATION → RECOGNITION → DISCOVERY` (README diagram). Exhaustive DVB spectrum is replaced by **budgeted open-world search**: `maxCandidates 750 live`, `maxRequests 150 global`, `maxDepth 5`.

## 2. Module Map (v1.3.0)

```
src/ 7 modules (framework bundler + lazy + providers + ESM + health+concurrent + verification hardening, ADR 021/024/025/027/028/029/030/031) built via `scripts/build.js` (+ `build-esbuild.js` minify + `build-esm.js` ESM + `analyze-bundle.js`):
 ├── header.txt — ==UserScript== + banner 165 lines (version placeholder)
 ├── config.js — CONFIG v8 ~86 keys + `revisitChanged`/`patternGuided` + `providers.concurrent/lazy/disabled` + `health` + `maxDiscoveries/Resources` + `runtimeBudget` (184 lines)
 ├── utils.js — canonicalizeUrl, fnv1a32, makeFingerprint (wired to CONFIG)
 ├── models.js / knowledge.js / ledger.js / providers.js / engine.js — placeholders (plan in src/README.md)
 └── README.md — bundler plan (v0.9.0 esbuild concatenation, header preservation)
CONFIG (v8, ~84 keys) + privacy stripSensitiveParams + candidateTTL 0/off + lifecycle strict:false + inference patternInference/clustering + changeDetection:true
├── utils: canonicalizeUrl (tracking+privacy), isAllowedUrl, contentTypeBase,
│          extractUrlsFromText/Css/Xml, fnv1a32, makeFingerprint, originOf
├── AcquisitionPlan / AcquisitionPolicy → AcquisitionPlan{allowed,reason}
├── OriginController (per-origin 2 concurrent, 150 ms, 50/origin)
├── Acquisition (GM_xhr + fetch fallback, 2M truncate, 8s timeout)
├── ProviderRegistry [Html, Json, Xml, Css, JavaScript, Robots, Headers, SitemapIndex, OpenApi, WellKnown, Manifest, Binary, Text] — ordered 13 (ADR 016/017/025/027)
├── KnowledgeBase (candidates Map, candidateKeys, visited identityKey, candidateTTL sweep, lifecycle guard _validateTransition, patternIndex/clusterIndex, change detection _oldHash, observations 800 FIFO,
│                  discoveries, resources, graphEdges 5k, fingerprintIndex, diagnostics 500)
├── DecisionLedger (12 types, 5k FIFO, seq, export/restore)
├── NetworkObserver (bridge fetch/XHR + PerformanceObserver, GET-trust rule)
└── GenericDiscoveryEngine (discover/plan/execute/worker/adaptive/persist/UI + rAF-batched updateUI + TTL-bounded claim + lifecycle-guarded marks + pattern/cluster metrics + getCoverageMetrics + ProviderRegistry 9 providers)
dist/generic-discovery-engine.user.js (6,344 lines) **generated** from `src/` via `scripts/build.js` `config→utils→ledger→models→knowledge→providers→engine` (204882B, sha 508e3e…); `dist/generic-discovery-engine.min.js` (66k, 32.7%, 241 lines, sha bf049e…), `dist/generic-discovery-engine.esm.js` (267B, sha 792783…), `providerSizes` 42k 20.6% (analyze-bundle) generated via `scripts/build-esbuild.js` esbuild transform; `src/` is source of truth (1.1 lazy), `scripts/build.js` checks src 7 exist before hashing.
```

## 3. Data-Flow & Invariants

- **Claim-before-await:** `claimNextCandidate()` is synchronous, sorts by `effectivePriority`, marks `claimed` before any `await`. Prevents duplicate acquisition under `concurrency:4`.
- **Policy-before-acquisition:** `AcquisitionPolicy.plan()` produces a replayable `AcquisitionPlan` (method/depth/type/binary/origin). Denials are ledgered (`policy-denied`) and scored as `skipped`, never fetched.
- **Budget atomics:** `reserveRequestSlot()` is synchronous before `acquire()`. Global `maxRequests` cannot be exceeded by racing workers.
- **Identity:** `Candidate.identityKey = type:target`. `visited` is identityKey-scoped; `candidateKeys` merges `alternateTypes`.
- **Observation cap:** `maxObservationsInMemory 800 FIFO` + `bodyTruncated` flag; `serialize()` strips bodies for `GM_setValue` quota (≈10 MB).
- **Cross-provider dedup:** `emittedForObservation Set<targetUrl>` per observation; mutation batches dedup via `seen Set<type:canonical>`.
- **UI batching:** `updateUI()` coalesces via `requestAnimationFrame` (`_uiRaf` guard → `_doUpdateUI`), prevents layout thrash on ledger storms; sync fallback when rAF absent.
- **Lifecycle guard:** `_validateTransition(candidate, to)` enforces `discovered→queued→claimed→planned→acquiring→observed→recognized→expanded→completed` plus `skipped/failed/ttl` branches; illegal emits `lifecycle-illegal-transition` (strict throws), cost 0.02 ms; proven by 500 random walks (ADR 010).
- **Pattern & cluster:** `extractUrlPattern` normalizes `/{int}/{uuid}/{hash}` and `clusterKeyForCandidate` groups `origin::pattern`; `recordPattern` O(1) on `addCandidate`, `getPatternMetrics`/`getClusterMetrics` O(n≤750) sorted top 20, ~0.06 ms (ADR 013/014).
- **Providers 9:** `ProviderRegistry` ordered `Html/Json/Xml/Css/JavaScript/Robots/Headers/Binary/Text`; `RobotsProvider` `Sitemap:` 0.92, `HeadersProvider` `Link` 0.88/`Location` 0.90, `http.headers` captured from `fetch` + `GM_xhr` (ADR 016/017).
- **Change detection:** `recordObservation` captures `_oldHash` before `ensureResource`, compares `hash !== _oldHash` when `CONFIG.changeDetection` → `resource-changed` diagnostic + `status='changed'`, O(1) ~0.01 ms (ADR 018).
- **Coverage determinism:** `getCoverageMetrics()` now sorted `queuedByType` + `patternCount`/`clusterCount`/`fingerprintUnique`/`inferenceEnabled` via `getPatternMetrics()`, O(n≤750) ~0.06 ms; `exportData().inference` adds bounded pattern/cluster/fingerprint stats (ADR 020).
- **Stable 1.0:** `package 1.0.0` + `header 1.0.0` + `CONFIG v8` unchanged — no runtime delta, 22 ADRs 126/126 5977 `9b2b68…` marks stable control-plane (ADR 023).
- **Lazy + esbuild 1.1:** `CONFIG.providers` lazy true + `ProviderRegistry` factories/metrics + `getProviderMetrics` + `export.providers` + `dist/*.min.js` 58k 32.3% esbuild 106668… + `build:all` (ADR 024, 135/135, 6076 `6dcfa8…`).
- **Sitemap/OpenAPI + analyze 1.2:** `SitemapIndexProvider` sitemapindex 0.90 + `OpenApiProvider` openapi 0.95 + `Registry` 11 ordered (Html→Text) + `analyze-bundle.js` 36k 19.1% provider breakdown + `build:all` 4-steps (ADR 025/026, 143/143, 6214 `344b9c…`).
- **Verification hardening + runtime bounds 1.5:** `maxDiscoveriesInMemory`/`maxResourcesInMemory` + `runtimeBudget` + `redirect:error` + `@connect self` + `diagnosticCount` + `configuredProviders` + `concurrencyTarget` + honest c8/lint/typecheck (ADR 031, 160/160, 6453 `508e3e…`).
- **Health+concurrent 1.4:** `CONFIG.health` + `getHealthMetrics()` status/pressures/slowProviders/recentErrors + `providers.concurrent` + `Promise.all` parallel with dedup + `export.health` (ADR 029/030, 160/160, 6394 `4f2c63…`).
- **WellKnown/Manifest + ESM 1.3:** `WellKnownProvider` wellKnown 0.80/0.70 + `ManifestProvider` manifest 0.85/0.80 + `Registry` 13 ordered (Html→Text) + `build-esm.js` ESM bundle proof 267B + `analyze-bundle.js` 42k 21.6% (ADR 027/028, 150/150, 6344 `bb0453…`).
- **Pattern-guided & revisit:** `KnowledgeBase.suggestPatternCandidates()` top patterns ≥minPatternFreq → `0`/`uuid0` suggestions (5 bounded, visited dedup) and `getChangedResources()` + `Engine` revisit (`revisit-queued`) + pattern-guided (`pattern-guided-queued`) when `CONFIG.revisitChanged`/`patternGuided.enabled` (ADR 022, opt-in, ~0.02 ms).
- **Framework bundler:** `scripts/build.js` concatenates `src/header.txt` + 7 modules in dependency order `config→utils→ledger→models→knowledge→providers→engine`, replacing `// @version` + banner from `package.json`, deterministic `sha256`/`wc -l` → `dist/.build-meta.json` (ADR 021).
- **Build determinism:** `scripts/build.js` captures `sha256`/`lines`/`size` → `dist/.build-meta.json`; `scripts/verify-build.js` asserts no `builtAt` in dist, header version matches `package.json`, hash matches meta, `extractUrlPattern` present, 9-provider order, src 7 present (ADR 015 → 019). `npm run build` now atomic `build && verify:build`.
- **Modular prelude:** `src/config.js` is real `CONFIG` extract, `src/utils.js` re-exports canonical helpers; build fails if any `src/*.js` missing — guarantees mirror never drifts (ADR 019).
- **Claim exclusivity:** `claimNextCandidate()` remains synchronous `eligible.sort → _validateTransition → claimed`; 4 workers + `setImmediate` interleaving never duplicate (ADR 011).
- **TTL boundedness:** `claimNextCandidate()` sweeps `queued/failed` with `now()-createdAt > CONFIG.candidateTTL` → `ttl-expired` (visited+skipped); liveCount freed before sort, deterministic at 0.05 ms (see ADR 007).
- **Coverage:** `getCoverageMetrics()` exposes `frontierSize/queuedByType/liveCount/requestsRemaining` in UI + export without extra traversal.

## 4. Security Defaults (v1.0.0)

- `sameOriginOnly:true` + `isAllowedUrl` (https only) enforced in both `discover()` and `policy`.
- `@connect self` (header) with `*` commented; runtime warns if `sameOriginOnly=false`.
- `acquireForms/Media/Binary:false` by default.
- `DOMParser` for HTML (no script execution); panel never interpolates untrusted body.
- `stripTrackingParams` always; `privacy.stripSensitiveParams` opt-in scrubs `token/session/auth/...` via `canonicalizeUrl`.
- Bridge injection wrapped in `try/catch`; CSP block emits `csp-blocks-bridge` + fallback to `PerformanceObserver` (evidence-only).
- `src/` mirror is ESM, not loaded in userscript — no new CSP surface; `trustedTypes.createPolicy('gde-bridge')` still guards bridge.

## 5. Persistence & Provenance

- `STORAGE_KEY generic-discovery-engine-v8`, debounced 400 ms.
- `restore()` is additive: v7 state with `version>=6` restored, ledger appended, `requestsReserved` reset to 0 each execution (fresh budget).
- `exportData()` schema `gde-export-v8.0` with `config + coverage + engine + ledger + networkEvents + diagnostics`.
- Graph provenance: every `discover()` via `Discovery` adds `graphEdges {from, to, relation}` (5k cap).

## 6. Performance Envelope (see PERFORMANCE_ANALYSIS.md)

- Heap worst-case ≈6 MB (750 queued, 800 obs, 5k ledger, 5k edges, 1.5k resources).
- Hot path is network (150 ms per-origin throttle dominates); CPU providers are `O(body)` bounded at 2M.
- E2E fixture (7 nodes, concurrency 2): 911 ms wall (20 ms unthrottled).
- `src/` adds ~0 runtime (not bundled yet); build adds <10 ms src check.

## 7. Open Iterations (from DECISIONS.md)

- Narrow `@connect` shipped v0.7.4; Trusted Types `gde-bridge` + fuzz + priority invariants shipped v0.7.5/v0.7.6; TTL + FIFO + throttle + gates shipped v0.7.7; lifecycle + concurrency + typecheck shipped v0.7.8; pattern/cluster + build determinism shipped v0.7.9; robots/headers + change detection shipped v0.8.0; modular prelude shipped v0.8.1; export hardening shipped v0.8.2; framework bundler shipped v0.9.0; pattern-guided/revisit shipped v0.9.1; stable shipped v1.0.0.
- Planning doc fully split is incremental; this overview + 19 ADRs + coverage gates + TTL + lifecycle + concurrency + pattern/cluster + build determinism + robots/headers + change detection + modular prelude completes the v0.8.1 feature pass; `npm run coverage:check` 85/75/80 gate, `npm run coverage` 99% line, `npm run typecheck` informational, `npm run verify:build` deterministic (sha256 bb0453… lines 6344, src 7 + header, inference + bundler + revisit/pattern + lazy/provider + sitemap/openapi/wellKnown/manifest gate, 1.3 providers).
