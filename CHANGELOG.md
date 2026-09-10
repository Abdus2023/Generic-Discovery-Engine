# Changelog

All notable changes to the Generic Discovery Engine.

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

