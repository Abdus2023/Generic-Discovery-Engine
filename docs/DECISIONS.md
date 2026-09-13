# Architecture Decisions — Index

> Source transcript: [`Continue Architecture Planning.md`](../Continue%20Architecture%20Planning.md) (2.2 MB, 92,274 lines, 12 userscript iterations v0.1.0→v0.7.1).  This index is the **P2-10 hygiene split** (v0.7.4) that extracts the durable decisions into ADRs without deleting the transcript.

## How to use this file
- Each ADR is a one-page record: **Context → Decision → Consequences → Alternatives → Links**.
- The transcript remains the provenance; ADRs are the normative summary.
- New decisions get a new `docs/adr/NNN-title.md` and are linked here.

## Decisions extracted (v1.2.0 — 26 ADRs)

| ADR | Title | Status | Transcript range | Code |
|-----|-------|--------|------------------|------|
| [001](adr/001-provider-pipeline.md) | Provider pipeline (7 providers, ordered matching) | ✅ accepted | §§7–23, lines ~45k–58k | `Provider`, `ProviderRegistry`, `Html/Json/Xml/Css/JS/Binary/Text` |
| [002](adr/002-ledger.md) | Deterministic Decision Ledger (12 typed events, 5k FIFO) | ✅ accepted | §§18–24, lines ~58k–65k | `DecisionLedger`, `exportData().ledger` |
| [003](adr/003-origin-controller.md) | Per-origin throttle & budget (2 concurrent / 150 ms / 50 per origin, 150 global) | ✅ accepted | §§20–22, lines ~60k–64k | `OriginController`, `CONFIG.origin`, `reserveRequestSlot` |
| [004](adr/004-fingerprint.md) | Content fingerprint (fnv1a32, 1M sample, Resource dedup) | ✅ accepted | §§24–26, lines ~65k–70k | `fnv1a32`, `makeFingerprint`, `fingerprintIndex` |
| [005](adr/005-mutation-batch.md) | Mutation observer batch dedup | ✅ accepted | §28 → v0.7.2 P1-2 | `installMutationObserver`, `seen Set` |
| [006](adr/006-export-schema.md) | Export schema (gde-export-v8.0, ledger + coverage) | ✅ accepted | §§26–30 → v0.7.2–v0.7.3 | `exportData()`, `serialize`, `getCoverageMetrics` |
| — | Coverage frontier metric (planned §19, shipped v0.7.3) | ✅ accepted | §19, §39 → v0.7.3 patch | `getCoverageMetrics()` |
| — | Privacy scrub opt-in (v0.7.4) | ✅ accepted | SECURITY_AUDIT S-07 → v0.7.4 | `CONFIG.privacy` |
| — | Trusted Types bridge (v0.7.5) | ✅ accepted | SECURITY_AUDIT S-02 → v0.7.5 | `trustedTypes.createPolicy('gde-bridge')` |
| — | Fuzz harness (v0.7.5) | ✅ accepted | PERFORMANCE + SECURITY → v0.7.5 | `tests/fuzz-extract.test.js` |
| — | rAF UI batching (v0.7.6) | ✅ accepted | PERFORMANCE S-04 → v0.7.6 | `updateUI/_doUpdateUI`, `_uiRaf` |
| — | Coverage + invariants (v0.7.6) | ✅ accepted | VERIFICATION → v0.7.6 | `tests/property-priority.test.js`, `npm run coverage` |
| [007](adr/007-candidate-ttl.md) | Candidate TTL (bounded freshness, sweep before sort) | ✅ accepted | Roadmap Phase 1 → v0.7.7 | `CONFIG.candidateTTL`, `claimNextCandidate` ttl-expired |
| [008](adr/008-origin-throttle-invariants.md) | Origin throttle invariants (interval/concurrency/isolation) | ✅ accepted | ADR 003 → v0.7.7 invariants | `OriginController` mock, `CONFIG.origin` |
| [009](adr/009-coverage-gates.md) | Coverage gates (85/75/80, c8 check-coverage) | ✅ accepted | VERIFICATION → v0.7.7 | `.c8rc.json`, `coverage:check` |
| [010](adr/010-lifecycle-state-machine.md) | Lifecycle state-machine guard (strict + table) | ✅ accepted | Worker audit → v0.7.8 | `CONFIG.lifecycle`, `_validateTransition`, `lifecycle-illegal-transition` |
| [011](adr/011-concurrency-claim.md) | Concurrency claim exclusivity (sync sort+mark) | ✅ accepted | Scheduler → v0.7.8 | `claimNextCandidate` sync, `property-concurrency` |
| [012](adr/012-type-safety.md) | Type safety (tsconfig checkJs + typecheck) | ✅ accepted | JSDoc → v0.7.8 | `tsconfig.json`, `typecheck`, `typescript` |
| [013](adr/013-pattern-inference.md) | URL pattern inference (template extraction) | ✅ accepted | Roadmap Phase 2 → v0.7.9 | `extractUrlPattern`, `patternIndex`, `getPatternMetrics` |
| [014](adr/014-clustering.md) | Candidate clustering (origin + pattern) | ✅ accepted | Phase 3 → v0.7.9 | `clusterKeyForCandidate`, `clusterIndex`, `getClusterMetrics` |
| [015](adr/015-build-determinism.md) | Build determinism (hash + line count + verify) | ✅ accepted | Hygiene → v0.7.9 | `scripts/build.js`, `verify-build.js`, `dist/.build-meta.json` |
| [016](adr/016-robots-provider.md) | Robots provider (Sitemap extraction) | ✅ accepted | Phase 2 → v0.8.0 | `RobotsProvider`, `ProviderRegistry` 9 providers |
| [017](adr/017-headers-provider.md) | Headers provider (Link/Location) | ✅ accepted | Phase 2 → v0.8.0 | `HeadersProvider`, `Observation.http.headers` |
| [018](adr/018-change-detection.md) | Change detection (fingerprint diff) | ✅ accepted | Phase 3 → v0.8.0 | `CONFIG.changeDetection`, `resource-changed` |
| [019](adr/019-modular-prelude.md) | Modular prelude + export hardening (src/ mirror) | ✅ accepted | Phase 4 → v0.8.1 | `src/config.js`, `src/utils.js`, 7-file mirror, `verify:build` src check |
| [020](adr/020-export-hardening.md) | Export hardening + inference metrics (coverage/export deterministic) | ✅ accepted | Phase 4 → v0.8.2 | `getCoverageMetrics` sorted, `exportData().inference`, verify:build inference gate |
| [021](adr/021-framework-bundler.md) | Framework bundler (src/ → dist/ deterministic) | ✅ accepted | Phase 4 → v0.9.0 | `src/header.txt` + 7 modules, `scripts/build.js` bundler, `dist` generated |
| [022](adr/022-pattern-guided-revisit.md) | Pattern-guided + revisitChanged (adaptive re-queue) | ✅ accepted | Phase 4 → v0.9.1 | `suggestPatternCandidates`, `getChangedResources`, `revisitChanged`/`patternGuided` |
| [023](adr/023-stable-1.0.md) | Stable 1.0 (generic discovery loop feature-complete) | ✅ accepted | 1.0 → stable | `package 1.0.0`, `header 1.0.0`, 22 ADRs 126/126 5977, `9b2b68…` |
| [024](adr/024-lazy-providers-esbuild.md) | Lazy Providers + esbuild Minify (provider hardening) | ✅ accepted | 1.1 → minify | `CONFIG.providers`, `ProviderRegistry` lazy + metrics, `build-esbuild` 6076 `6dcfa8…` 135/135 |
| [025](adr/025-sitemap-openapi-providers.md) | SitemapIndex + OpenAPI Providers (11-provider) | ✅ accepted | 1.2 → providers | `SitemapIndexProvider` `OpenApiProvider` `11` `344b9c…` 143/143 |
| [026](adr/026-bundle-analyze.md) | Bundle Analyze (provider size breakdown) | ✅ accepted | 1.2 → analyze | `analyze-bundle.js` `providerSizes` `bundleAnalysis` 19.1% |

## Decisions still in transcript (not yet ADR-ified)

- DVB analogy scope (web is open-world, DVB is bounded spectrum) — see `VERIFICATION_REPORT.md` §2.1.
- Adaptive concurrency (thresholds 4/2) — `GenericDiscoveryEngine.onSuccess/onFailure`.
- Persistence migration v6→v8 additive — `KnowledgeBase.restore` + `STORAGE_KEY v8`.
- Network bridge vs PerformanceObserver separation (GET-trust rule) — `NetworkObserver` header comment.

## Process
1. ChatGPT proposes; user selects v0.2.0 as base.
2. Each iteration adds one control-plane concern (claim-before-await, policy-before-acquisition, ledger-for-explainability).
3. Verification (v0.7.1 audit) files P0/P1; patches landed v0.7.2/v0.7.3/v0.7.4/v0.7.5/v0.7.6/v0.7.7/v0.7.8/v0.7.9/v0.8.0/v0.8.1/v0.8.2/v0.9.0/v0.9.1/v1.0.0/v1.1.0/v1.2.0.

## Further splits
- The 2.2 MB file also contains 12 full code fences. The runnable artifact is now `dist/generic-discovery-engine.user.js` (v1.2.0, 6,214 lines, `344b9c…` + `dist/generic-discovery-engine.min.js` 60k 32.3%, `providerSizes` 36k 19.1%, built from `src/` 7 modules) (was v1.1.0 6,076 / v1.0.0 5,977 / v0.9.1 5,969). The fences are retained for diff archaeology but are no longer the source of truth.
- With 26 ADRs + rAF + coverage + TTL + gates + lifecycle + concurrency + pattern/cluster + build determinism + robots/headers + change detection + modular prelude + export hardening + framework bundler + pattern-guided/revisit + stable + lazy/sitemap/openapi/bundle the control-plane is **stable 1.2** for v1.2.0; `docs/analysis/DEEP_DVB_AUDIT_v0.8.2.md` remains valid (143/143) and `src/` is source of truth — 1.2 adds 11-provider pipeline + bundle analyze 19.1% with `build:all`.
