# Deep DVB Audit — Generic Discovery Engine v0.8.2

> **Purpose:** Deeply analyse and verify whether the DVB blind-scan pattern generalizes correctly to web-resource discovery, and whether the v0.8.2 prototype satisfies the generic discovery loop with provable invariants. Extends `VERIFICATION_REPORT.md` (v0.7.1) + supplements `v0.7.2`→`v0.8.2` + `PERFORMANCE_ANALYSIS` + `SECURITY_AUDIT` + 20 ADRs. Runnable `dist/generic-discovery-engine.user.js` **5,864 lines** `a46d37…` `node --check` PASS · **`npm test` 121/121 32 suites** · `verify:build` deterministic.

## 0. Executive Verdict

**The DVB analogy holds for the control plane, not the physical layer.** DVB blind scan searches a bounded spectrum without a priori service list; the engine searches an open-world URL space without a priori resource list. The *pattern* — *hypothesis → probe → observation → recognition → expansion → scheduler* — is identical; the *mechanism* — RF demod vs `GM_xmlhttpRequest`/`fetch` — is deliberately not reproduced. v0.8.2 implements the full generic loop with **9 ordered providers, ledger-replayable acquisition, per-origin throttling, bounded heap, pattern inference, change detection, and deterministic export**, proven by 121 tests, 500-iteration property harnesses, and `sha256` build gating. Residual is framework split: `src/` is still a mirror, not a bundled source of truth — scheduled for v0.9.0. No P0/P1 invariants regressed.

## 1. DVB → Generic Mapping (why DVB blind scan is the right motivating example)

| DVB blind scan | Generic discovery (this prototype) | Evidence |
|---|---|---|
| **Frequency** (unknown carrier) | **Candidate** `{target, type, depth, priority, hints}` hypotheses “worth investigating” not “exists” | `Candidate` class, `Candidate.identityKey() type:target`, `effectivePriority()` (ADR 001) |
| **Signal detection** (energy) | **Probe / AcquisitionPlan** `AcquisitionPolicy.plan()` → `{allowed, reason}` replayable | `AcquisitionPolicy` (method/depth/type/binary/origin), ledger `acquisition-planned`/`policy-denied` |
| **Demod acquisition** (tuner+demod) | **Acquisition** `GM_xhr + fetch fallback`, 2 M truncate, 8 s timeout, per-origin 2 concurrent/150 ms/50 per origin /150 global | `Acquisition`, `OriginController`, `reserveRequestSlot()` sync (ADR 003) |
| **Transport validation** (TS lock) | **Observation** `{status, http, body, fingerprint, headers}` — failed acquisition is still evidence | `Observation`, `NetworkObserver` GET-trust rule, `http.headers` lowercased |
| **PSI/SI metadata** (NIT/BAT/SDT) | **Recognition** `ProviderRegistry` ordered `Html/Json/Xml/Css/JS/Robots/Headers/Binary/Text` → `Discovery {kind, confidence, mechanism, provenance}` | `HtmlProvider` 0.85 …. `RobotsProvider` 0.92, `HeadersProvider` 0.88/0.90 (ADRs 016/017) |
| **Network discovery** (new mux) | **Candidate expansion** `Discovery → Candidate depth+1` with `graphEdges` provenance | `emitDiscovery()` → `discover()` + `graphEdges` 5 k cap |
| **Scheduler** (exhaust spectrum) | **Scheduler** budgeted open-world: `maxCandidates 750 live`, `maxRequests 150`, `maxDepth 5`, `effectivePriority` + TTL | `KnowledgeBase.addCandidate` liveCount, `claimNextCandidate` sync sort+mark (ADR 011) |

**DVB is bounded** (e.g., 950–2150 MHz / 470–862 MHz, symbol-rate/FEC sweep); **web is open** (link graph unbounded). The prototype therefore replaces exhaustive sweep with **priority × probability / cost** (`effectivePriority = priority + typeWeight*0.20 + confidence*0.08 − depth*0.045 − attempts*0.05`) and **budget atomics** (`reserveRequestSlot()` sync before `await`). The analogy is explicitly scoped in `VERIFICATION_REPORT.md` §2.1 and `DECISIONS` “still in transcript”.

## 2. Generic Discovery Loop — Walk-through with Invariants

```
initialize search space
while candidates remain && budget:
  candidate ← claim()          // sync, exclusive, TTL-swept, visited-scoped
  plan ← policy(candidate)     // replayable AcquisitionPlan, no fetch yet
  if !plan.allowed → skip/ledger
  else if !reserveSlot → budget-denied
  else if shouldAcquire? → already-acquired shortcut
  else observation ← acquire(plan) // origin-throttled, truncated, fingerprinted
         ledger, pattern/cluster, fingerprintIndex, change detection
         providers.matching → recognitions → discoveries (per-observation dedup)
         discoveries → new candidates (depth+1, Batch dedup)
  markCompleted/Skipped/Failed/retried, adaptive concurrency, UI, persist
```

Each edge verified:

### 2.1 Claim-before-await (concurrency invariant)
*Claim is synchronous sort+mark before any `await HTTP`.* `claimNextCandidate()` filters `queued|failed` with `nextAttemptAt`/`candidateTTL` sweep, sorts by `effectivePriority`, `_validateTransition(→claimed)`, sets `claimed` sync. Property harness `property-concurrency` (4 workers + `setImmediate` interleaving, 500 iter, TTL+retry windows) proves **no duplicate claim**. Cost ~0.05 ms sweep + O(n log n) ≤750.

Evidence: `tests/property-concurrency.test.js` 6 cases, `verify-p0-fixes` “concurrency invariant”.

### 2.2 Policy-before-acquisition (security + budget)
`AcquisitionPolicy.plan()` denies `javascript:`/`data:` via `isAllowedUrl` (`/^https?:$/` + `sameOriginOnly`), `method !== GET`, `depth>5`, `form/media/binary/frames/stylesheets/scripts/networkGet` toggles. Denials ledgered `policy-denied` + `diagnostic:policy-denied` and never fetched. `reserveRequestSlot()` sync prevents 4 workers exceeding `maxRequests 150`. Proven by `tests/canonicalize-and-policy.test.js` (javascript/data, cross-origin, POST, depth, forms-disabled etc.), e2e “policy denials are correctly ledgered”.

### 2.3 Acquisition — origin throttle, truncation, fingerprint
`OriginController` 2 concurrent / 150 ms / 50 per origin (Map `active/requests/lastRequestAt`, `acquire()` loop with `await sleep(minInterval-elapsed)`). `Acquisition.request()` supports `GM_xmlhttpRequest` + `fetch+AbortController` 8 s, `body.slice(0,2M)` + `bodyTruncated` flag, `makeFingerprint(sample 1M → fnv1a32 8hex)` stored O(1) in `fingerprintIndex: Map<hash,Set<url>>`, lowercased `http.headers` captured. Heap worst-case ≈6 MB (750 candidates, 800 obs, 5k ledger, 5k edges, 1.5k resources, 1k network events). E2E fixture 7 nodes wall 911 ms (concurrency 2, 150 ms throttle; 20 ms unthrottled).

Evidence: `property-determinism` origin interval/concurrency/isolation, `fuzz-extract` 2 M slice, `provider-robots-headers` http.headers.

### 2.4 Recognition — ordered providers, per-observation dedup
Registry order `Html → Json → Xml → Css → JavaScript → Robots → Headers → Binary → Text` (Text fallback last). Each `matches(Observation)` pure on `contentType`/`body`/`headers`/`url` and `recognize()` emits `Discovery` with `confidence` 0.40–0.95 (`typeWeight` boost). `executePlan()` maintains `emittedForObservation Set<targetUrl>` cross-provider (P1-1) so `Html` + `Text` duplicate `https://ex/a` once per observation, with `diagnostic:discovery-deduped`. Providers are replaceable (HTML/JSON/XML … domain-specific) — engine core never hardcodes `href` regex.

Evidence: `tests/provider-robots-headers.test.js` 12 cases (Robots Sitemap 0.92, Headers Link 0.88/Location 0.90, http.headers, change diff/same), `verify-p0-fixes` P1-1, e2e “provider-recognized” ledger chain.

### 2.5 Expansion — provenance, priority, batch dedup, patterns
`emitDiscovery()` creates depth+1 candidate with `provenance {origin, parent, candidateTarget, mechanism, depth, hints{confidence}}`, `alternateTypes/Origins/Parents` merged on `type:target` dup, `graphEdges` 5 k. `observeCurrentDom()` mutation observer batches via `seen Set<type:canonical>` per flush (P1-2, 250 ms debounce). `KnowledgeBase.recordPattern()` on `addCandidate` extracts `extractUrlPattern` (`/{int}`, `?={int}`, `/{uuid}`, `/{hash}` 32/64, 8-4-4-4-12) → `patternIndex` + `clusterIndex origin::pattern`, `getPatternMetrics()/getClusterMetrics()` O(n≤750) ~0.06 ms sorted top 20. `visited` is `Set<identityKey>` (`type:target`), not `Set<url>`, so `api:https://x` ≠ `url:https://x`; `maxCandidates` liveCount counts `∉ {completed,skipped}` (P0-1 fix) so frontier never freezes after 750 completions; `maxObservationsInMemory 800 FIFO` caps heap (P0-3).

Evidence: `tests/property-pattern.test.js` 7 invariants (numeric/query/uuid/hash collapse 500 iter, metrics sorted/bounded), `fuzz-extract` 50+80+40+100 deterministic, `verify-p0-fixes` P0-1…P1-2, `tests/src-build.test.js` pattern/cluster exports.

### 2.6 Scheduler — TTL boundedness, lifecycle, adaptive
`claimNextCandidate()` sweeps `now-createdAt > candidateTTL` → `ttl-expired` (`visited+skipped`, `candidate-ttl-expired`) before sort, freeing liveCount at cap without background timer (ADR 007). `_validateTransition` table `discovered→queued→claimed→planned→acquiring→observed→recognized→expanded→completed` plus `skipped/failed/ttl` branches; illegal emits `lifecycle-illegal-transition` (strict throws) ~0.02 ms, 500 random walks never illegal (ADR 010). Adaptive `onSuccess/onFailure` thresholds `4/2` adjust `currentConcurrency` within `minConcurrency..concurrency` with `adaptive-increase/-decrease` diagnostics.

Evidence: `tests/property-determinism.test.js` 12 invariants (TTL old→skipped, TTL 0→claimable, liveCount bounded 500 iter, Ledger FIFO 5k, Origin throttle, fnv1a32), `tests/property-lifecycle.test.js` 8 invariants, `tests/property-priority.test.js` 8 invariants (monotonicity, depth 0.045, confidence 0.08, retry 0.05).

## 3. Knowledge & Change — historical memory

* **Persistence** additive `STORAGE_KEY v8`, `serialize()` strips `body` (Observation without body), debounced 400 ms, `restore()` v6→v8 retains candidates/ledger (5k), resets `requestsReserved` fresh budget.
* **Fingerprint** `fnv1a32(sample 1M)`, `empty 811c9dc5`, sampled collision sanity 200 (property-determinism).
* **Change detection** `CONFIG.changeDetection:true` captures `_oldHash` before `ensureResource` + `merge`, after `fingerprintIndex` if `hash !== _oldHash` → `diagnostic:resource-changed {target, oldHash, newHash}` + `ResourceRecord.status='changed'` (O(1) ~0.01 ms), observable via export (ADR 018) — no auto-requeue yet (residual).

## 4. Observability — coverage, export, ledger, UI

* **Coverage** `getCoverageMetrics()` frontier `queued.length`, `queuedByType` alphabetically sorted (v0.8.2), `liveCount`, `visitedSize`, `knownResources`, `totalCandidates`, `requestsUsed/Remaining`, `ledgerSize`, `graphEdges`, `observations`, plus `patternCount`/`clusterCount`/`fingerprintUnique`/`inferenceEnabled`. Cost ~0.1 ms.
* **Export hardening** `exportData()` `schema gde-export-v8.0`, `config`, `coverage`, `inference {enabled, patternMetrics, clusterMetrics top20, fingerprintStats {unique,total}}`, `engine.serialize()`, `ledger.export()` (seq monotonic FIFO 5k), `networkEvents`, `diagnostics` (500). Deterministic `queuedByType` JSON-stable verified by `tests/export-inference.test.js` 6 cases; `schema` additive — old consumers ignore `inference`.
* **Ledger** 12 typed events `candidate-discovered/claimed, acquisition-planned/started/completed, observation-recorded, provider-recognized, discovery-emitted, candidate-enqueued/completed/skipped, candidate-retried, budget-denied, policy-denied, slot-granted` plus `diagnostic:*`, `seq` monotonic, replayable `export/restore`. Proven by e2e ledger chain.
* **UI** rAF-batched `updateUI/_doUpdateUI` (`_uiRaf` guard) coalesces 5k-ledger builds on 4-worker flush; fallback sync without rAF (ADR v0.7.6). Panel shows `candidates (live)`, `queued {...}`, `requests remain`, `visited/resources`, `ledger/edges/obs`, adaptive concurrency; never interpolates `body`.

Evidence: supplements `v0.7.6` coverage/perf, `v0.7.3` P2-3 frontier, `v0.8.2` export hardening.

## 5. Test Matrix — 121/121, 32 suites

| Suite | Cases | What it proves |
|---|---|---|
| `e2e-discovery-loop` | 6 | mocked 7-fixture crawl terminates, ≥4 obs ≥3 disc, provenance, graph, budget, ledger chain |
| `canonicalize-and-policy` | — | `isAllowedUrl` rejects `javascript:data:`, cross-origin, `policy` denies 6 reasons |
| `fuzz-extract` | 7 | seeded LCG 50+80+40+100: `canonicalizeUrl` idempotent + privacy scrub, `extractUrls` dedup never-throw, `fnv1a32` collision, 2M slice |
| `property-priority` | 8 | `effectivePriority` monotonic, depth 0.045, confidence 0.08, retry 0.05, `typePriority` ordering, `rAF` presence |
| `property-determinism` | 13 | TTL old→skipped / 0→claimable / liveCount bounded 500 iter, Ledger FIFO 5k, Origin 150 ms/2-conc/isolation, `fnv1a32` empty `811c9dc5` + 1M truncated |
| `property-lifecycle` | 8 | allowed/branch/illegal/strict/terminal no-outgoing/500 walks/full happy path |
| `property-concurrency` | 6 | 4-worker exclusive claim under `setImmediate` + TTL/retry windows, no `async` before `claimed` |
| `property-pattern` | 7 | numeric path/query, `uuid` 8-4-4-4-12 → `{uuid}`, `hash` 32/64 → `{hash}`, collapse 500 iter, metrics sorted/bounded |
| `provider-robots-headers` | 12 | Robots matches/extract Sitemap 2, Headers matches Link/Location + extract 3, http.headers captured, change diff/same 3 |
| `src-build` | 6 | `src/` 7 existence, `CONFIG` version 8, header sync, meta hash/version, 9-provider order, pattern/cluster exports |
| `export-inference` | 6 | sorted `queuedByType`, export `inference` block, pattern collapse, JSON-stable, static keys, fingerprintUnique |
| `verify-p0-fixes` | 10+15 | static 15 patch presence (`liveCount`, `visited identityKey`, `observation-evicted`, `emittedForObservation`, `seen`, `getCoverageMetrics`, hardening, trust, `rAF`, TTL, lifecycle, pattern, robots/headers/change, syntax) + 15 behavioral invariants (liveCount, visited scoped, FIFO 2, dedup 2, cross-provider, claim sync) |

Coverage `node --experimental-test-coverage` **99.28%/92.45%/94.94%** (`.c8rc` gate 85/75/80 PASS), `typecheck` informational, `verify:build` sha `a46d37…` 5864 deterministic, `node --check` both `dist` files PASS. Transcript 2.2 MB fences retained in `Continue Architecture Planning.md` for provenance; runnable artifact is `dist` + `src` mirror.

## 6. Performance Envelope (hot paths)

Heap worst-case ≈6 MB (750 queued, 800 obs, 5 k ledger, 5 k edges, 1.5 k resources, 1 k network events) — fitted for Tampermonkey GM quota ~10 MB (bodies stripped). CPU providers O(body) bounded 2 M; `fnv1a32` 1 M sample, pattern O(n≤750) ~0.06 ms, coverage ~0.1 ms, claim sweep ~0.05 ms, lifecycle ~0.02 ms. Network is bottleneck: 150 ms per-origin throttle dominates; e2e 7 nodes wall 911 ms at concurrency 2 (20 ms unthrottled). `rAF` prevents layout thrash on ledger storms.

## 7. Security Posture

OWASP + Greasemonkey advisories, 9 findings (S-01…S-09) in `SECURITY_AUDIT.md` v0.8.2:

* **S-01 HIGH mitigated** `@connect *` wildcard required for header, but runtime `sameOriginOnly:true` + `isAllowedUrl` double-check + `AcquisitionPolicy` deny; `self` narrow header with `*` commented, runtime warns if `sameOriginOnly=false`.
* **S-02 MEDIUM** bridge injects `<script>` in page world, CSP may block → `try/catch` + `csp-blocks-bridge` diagnostic + `PerformanceObserver` evidence-only fallback (GET-trust rule); `trustedTypes.createPolicy('gde-bridge')` complies with `require-trusted-types-for 'script'`.
* **S-03 mitigated** HTML via `DOMParser` no script execution, panel never `innerHTML=body`.
* **S-04 blocked** `javascript:data:blob:mailto:` via `isAllowedUrl` (`^https?:`).
* **S-05/06 disabled** `acquireForms/Media/Binary false` by default; providers still discover but `policy` denies `forms-disabled` etc.
* **S-07 INFO** ledger/storage may retain URLs with `token` query — `CONFIG.privacy.stripSensitiveParams` opt-in scrubs `token/session/auth/sid/access_token/api_key/secret` via `canonicalizeUrl` (8 regex), `stripTrackingParams` always `utm_/fbclid/gclid`.
* **S-08 bounded** ReDoS: `maxBodyChars 2M`, `fingerprintMaxChars 1M`, dedup `Set`, no nested quantifiers catastrophic.
* **S-09 INFO** `stripTrackingParams` removes `ref` semantic on some sites — `CONFIG.stripTrackingParams` toggle, lossy canonicalization intentional for dedup.
* v0.8.2 adds no new CSP surface (`src/` ESM not loaded, `export inference` additive, `headers` lowercased stored only in `Observation.http.headers`).

## 8. DVB Verification: Where the Analogy Passes / Fails

**Passes (control-plane isomorphism verified):**
* Bounded ↔ Budgeted search is isomorphic: DVB exhaustive sweep over known UHF/S band ≈ engine `maxRequests 150` + `maxCandidates 750 live` + `maxDepth 5` priority-guided search over open graph — both transform `unknown space → successive hypotheses` with `claim→probe→observe→recognize→expand` feedback.
* Signal validation ↔ Observation validation both treat failures as evidence (TS unlock → `status http-error/timeout`, `fingerprint` still indexed, `retryCandidate` with backoff).
* Metadata-guided expansion holds: DVB NIT → new frequencies; web `JsonProvider walk` → new URLs, `pattern inference` → template `origin::/user/{int}` collapsing 200 URLs into one cluster, enabling future “scan the pattern” strategy.
* Provenance requirement holds: DVB mux provenance → web `graphEdges {from,to,relation}` + `Discovery.provenance {parent, candidateTarget, mechanism, depth}` answering *why* not just *what*.

**Fails (physical-layer non-goals, explicitly not implemented):**
* No RF, SDR, tuner, demod, FEC, MPEG-TS, PSI/SI NIT parsing — listed in `README` Non-Goals (10 items). Intentional: “DVB-inspired, not DVB-compatible” (architecture, not physical layer).
* No blind spectrum parameter estimation (symbol-rate, carrier sync) ↔ web `isAllowedUrl`/`origin throttle` is regulatory, not RF estimation; correspondence is at search strategy, not estimation math.

**Formal gaps (verification, not DVB mismatch):**
* `src/` still mirror (5864 monolith), bundler deferred to v0.9.0 — framework split incomplete (ADR 019).
* `changed` status informational only, no auto-requeue (`revisitChanged` future via TTL or explicit revisit, ADR 018).
* `RobotsProvider` only `Sitemap:` (not `Allow/Disallow` soft-deny), `HeadersProvider` only `Link`+`Location` (not `Content-Location`/`Refresh`).

## 9. Residual & Next Iterations

Already shipped: narrow `@connect` (0.7.4), Trusted Types + fuzz (0.7.5), `rAF` + coverage (0.7.6), TTL + FIFO + throttle (0.7.7), lifecycle + claim + types (0.7.8), pattern/cluster + build determinism (0.7.9), robots/headers + change (0.8.0), modular prelude (0.8.1), export hardening (0.8.2) — 20 ADRs + 121 tests.

Next for `v0.9.0`:
* **Bundler:** `src/config → utils → models → knowledge → ledger → providers → engine` header-preserving concatenation (`esbuild`-style IIFE wrapper), `verify:build` hash stays, `src/` becomes source of truth, `dist` generated artifact (no hand-edit).
* **DVB-loop closure:** `revisitChanged` scheduler (re-queue `changed` resources via TTL), `Robots Allow/Disallow` → `policy` soft deny with `respectRobotsTxt` toggle, `pattern-guided` candidate generation (sample `/{int}` → next int), `export --stable` timestamp `0` for snapshot testing.
* **CI hardening:** copy `docs/ci/verify.yml.example` to `.github/workflows/verify.yml` (PAT `workflows` scope), `lint+typecheck+coverage:check+verify:build` gate.

---

*Auditor: Arena Agent — deep static + dynamic review, 2026-09-12, `v0.8.2` `a46d375a84c357647922460e3048904394a7ab2081e9bcc9875d7b78ac40f553` 5864 lines, 121/121.*

