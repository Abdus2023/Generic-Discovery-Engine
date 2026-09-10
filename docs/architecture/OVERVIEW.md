# Architecture Overview — Generic Discovery Engine v0.7.8

**Runnable artifact:** `dist/generic-discovery-engine.user.js` (5,526 lines, CONFIG v8, `node --check` PASS)  
**Transcript source:** `Continue Architecture Planning.md` (2.2 MB) → split into `docs/DECISIONS.md` + `docs/adr/*` (v0.7.4)  
**Verification:** `VERIFICATION_REPORT.md` (v0.7.1) + `VERIFICATION_SUPPLEMENT_v0.7.2.md` + `VERIFICATION_SUPPLEMENT_v0.7.6.md` + `VERIFICATION_SUPPLEMENT_v0.7.7.md` + `VERIFICATION_SUPPLEMENT_v0.7.8.md` + `docs/SECURITY_AUDIT.md` + `docs/PERFORMANCE_ANALYSIS.md` — `npm test` 88/88 PASS

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

## 2. Module Map (v0.7.8)

```
CONFIG (v8, ~82 keys) + privacy stripSensitiveParams + candidateTTL 0/off + lifecycle strict:false
├── utils: canonicalizeUrl (tracking+privacy), isAllowedUrl, contentTypeBase,
│          extractUrlsFromText/Css/Xml, fnv1a32, makeFingerprint, originOf
├── AcquisitionPlan / AcquisitionPolicy → AcquisitionPlan{allowed,reason}
├── OriginController (per-origin 2 concurrent, 150 ms, 50/origin)
├── Acquisition (GM_xhr + fetch fallback, 2M truncate, 8s timeout)
├── ProviderRegistry [Html, Json, Xml, Css, JavaScript, Binary, Text] — ordered
├── KnowledgeBase (candidates Map, candidateKeys, visited identityKey, candidateTTL sweep, lifecycle guard _validateTransition, observations 800 FIFO,
│                  discoveries, resources, graphEdges 5k, fingerprintIndex, diagnostics 500)
├── DecisionLedger (12 types, 5k FIFO, seq, export/restore)
├── NetworkObserver (bridge fetch/XHR + PerformanceObserver, GET-trust rule)
└── GenericDiscoveryEngine (discover/plan/execute/worker/adaptive/persist/UI + rAF-batched updateUI + TTL-bounded claim + lifecycle-guarded marks + getCoverageMetrics)
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
- **Claim exclusivity:** `claimNextCandidate()` remains synchronous `eligible.sort → _validateTransition → claimed`; 4 workers + `setImmediate` interleaving never duplicate (ADR 011).
- **TTL boundedness:** `claimNextCandidate()` sweeps `queued/failed` with `now()-createdAt > CONFIG.candidateTTL` → `ttl-expired` (visited+skipped); liveCount freed before sort, deterministic at 0.05 ms (see ADR 007).
- **Coverage:** `getCoverageMetrics()` exposes `frontierSize/queuedByType/liveCount/requestsRemaining` in UI + export without extra traversal.

## 4. Security Defaults (v0.7.8)

- `sameOriginOnly:true` + `isAllowedUrl` (https only) enforced in both `discover()` and `policy`.
- `@connect self` (header) with `*` commented; runtime warns if `sameOriginOnly=false`.
- `acquireForms/Media/Binary:false` by default.
- `DOMParser` for HTML (no script execution); panel never interpolates untrusted body.
- `stripTrackingParams` always; `privacy.stripSensitiveParams` opt-in scrubs `token/session/auth/...` via `canonicalizeUrl`.
- Bridge injection wrapped in `try/catch`; CSP block emits `csp-blocks-bridge` + fallback to `PerformanceObserver` (evidence-only).

## 5. Persistence & Provenance

- `STORAGE_KEY generic-discovery-engine-v8`, debounced 400 ms.
- `restore()` is additive: v7 state with `version>=6` restored, ledger appended, `requestsReserved` reset to 0 each execution (fresh budget).
- `exportData()` schema `gde-export-v8.0` with `config + coverage + engine + ledger + networkEvents + diagnostics`.
- Graph provenance: every `discover()` via `Discovery` adds `graphEdges {from, to, relation}` (5k cap).

## 6. Performance Envelope (see PERFORMANCE_ANALYSIS.md)

- Heap worst-case ≈6 MB (750 queued, 800 obs, 5k ledger, 5k edges, 1.5k resources).
- Hot path is network (150 ms per-origin throttle dominates); CPU providers are `O(body)` bounded at 2M.
- E2E fixture (7 nodes, concurrency 2): 911 ms wall (20 ms unthrottled).

## 7. Open Iterations (from DECISIONS.md)

- Narrow `@connect` shipped v0.7.4; Trusted Types `gde-bridge` + fuzz + priority invariants shipped v0.7.5/v0.7.6; TTL + FIFO + throttle + gates shipped v0.7.7; lifecycle + concurrency + typecheck shipped v0.7.8.
- Planning doc fully split is incremental; this overview + 12 ADRs + coverage gates + TTL + lifecycle + concurrency + typecheck completes the v0.7.x hygiene pass; `npm run coverage:check` 85/75/80 gate, `npm run coverage` 99% line, `npm run typecheck` informational.
