# Changelog

All notable changes to the Generic Discovery Engine.

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

