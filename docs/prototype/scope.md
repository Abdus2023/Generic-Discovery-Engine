# Prototype Scope

Status boundary for the shipped userscript (v0.7.1). Statements here are
verifiable against `prototype/generic-discovery-engine.user.js` with
`tools/verify.mjs` and `tools/checks.mjs`.

The tiers used below map onto the canonical status dimensions as follows; the
tiers are shorthand for readers, and the claim records in
[../analysis/claims.md](../analysis/claims.md) carry the full status.

| Tier | claim_kind | implementation_state | test_state | evidence_level | claim_verification.result |
| --- | --- | --- | --- | --- | --- |
| Implemented | `CURRENT` | `IMPLEMENTED` | `TESTED` | `DIRECT` or `CORROBORATED` | `VERIFIED` |
| Partially implemented | `CURRENT` | `PARTIAL` | `TESTED` or `PARTIALLY_TESTED` | `DIRECT` or `CORROBORATED` | `PARTIALLY_VERIFIED`, or `CONTRADICTED` for the named limitation |
| Not implemented (designed) | `SPECIFIED` / `PLANNED` | `NOT_IMPLEMENTED` | `NOT_APPLICABLE` | `INDIRECT` | `VERIFIED` as planned, `UNVERIFIED` as behaviour |
| Not implemented (non-goal) | `NON_GOAL` | `NOT_IMPLEMENTED` | `NOT_APPLICABLE` | `ABSENT` | `VERIFIED` as absent |
| Future | `HYPOTHESIS` | `NOT_IMPLEMENTED` | `NOT_APPLICABLE` | `INDIRECT` | `UNVERIFIED` |

## Implemented

Confirmed by reading the artifact and by executing it (`tools/checks.mjs`,
`tools/simulate.mjs`).

| Capability | Evidence in the artifact |
| --- | --- |
| Seed generation | `observeCurrentPage()` (current URL), `observeCurrentDom()` (DOM), `observeNetworkGet()` / performance entries |
| Candidate normalization | `canonicalizeUrl()`: URL resolution, fragment removal, tracking-parameter stripping |
| Candidate deduplication | `KnowledgeBase.addCandidate()` via `identityKey() = type:target` |
| Resource-level acquisition guard | `shouldAcquireResource()` on canonical URL + resource status |
| Candidate claiming | `KnowledgeBase.claimNextCandidate()` — synchronous ownership transition |
| HTTP acquisition | `Acquisition.request()` via `GM_xmlhttpRequest`, `fetch` fallback |
| Timeout behaviour | 8 s timer races the request; a timeout produces an `Observation` with `status: 'timeout'` |
| Content-type handling | `contentTypeBase()` plus body sniffing for HTML/JSON/XML |
| HTML recognition | `HtmlProvider`: links, frames, scripts, media, form actions, metadata (`og:`, `twitter:`, meta-refresh) |
| JSON recognition | `JsonProvider`: recursive walk for URL-like values |
| Text recognition | `TextProvider`: absolute and relative URLs in `text/*` bodies |
| Additional recognition | `XmlProvider`, `CssProvider`, `JavaScriptProvider`, `BinaryProvider` |
| Resource extraction | DOM observer also proposes scripts, link resources and form actions |
| Candidate expansion | `emitDiscovery()` → `discover()` with `parent`, `depth + 1`, confidence-derived priority |
| Reporting / export | `exportData()` (`gde-export-v7.1`) and the on-page stats block |
| UI | panel with Scan / Pause / Stop / Clear / Export |
| Error handling | per-provider `try/catch`; acquisition failures become observations; diagnostics recorded |
| Request budgeting | `reserveRequestSlot()` against `maxRequests` |
| Origin rate limiting | `OriginController`: cap, interval, per-origin concurrency |
| Retry with backoff | `KnowledgeBase.retryCandidate()`, 2 retries, 500 ms → 8 s |
| Decision ledger | `DecisionLedger`: append-only sequenced events, capped at 5000, persisted and restored |
| Content fingerprinting | `makeFingerprint()` (fnv1a32 over a normalized sample), stored per observation and resource |
| Graph edges | `KnowledgeBase.addEdge()` — parent/child relations, capped at 5000 |
| Policy gating | `AcquisitionPolicy.plan()`: GET-only, depth, forms/media/binary classes |
| Persistence | `persist()` / `restore()` with caps; `GM_setValue` or `localStorage` |

## Partially implemented

Real functionality with meaningful limitations. Each entry names the defect or
gap that limits it.

| Area | What works | Limitation |
| --- | --- | --- |
| Concurrency | worker pool of `currentConcurrency` workers; runs genuinely in parallel when the frontier is populated | pool is never refilled (D2); effective concurrency often 1; ownership invariant broken by re-queue (D1) |
| Adaptive concurrency | counters, thresholds and ledger diagnostics exist | the pool never resizes (D5) |
| Persistence | state and ledger round-trip across reload | no transaction, no validation, no in-flight reconciliation; `running` is not restored (CONFLICT 4) |
| Retry | exponential backoff before retry | `failed` bypasses backoff and stays claimable (D3) |
| Termination | stops on empty eligible set, budget exhaustion or `stop()` | no completion criterion; a scan can look "running" while idle (D4) |
| Cancellation | cooperative `stopRequested` / `paused` | in-flight requests are not aborted; budget already reserved is not reclaimed |
| Content identity | fingerprints computed and indexed | index is never read (D8) |
| Discovery accounting | each recognition stores a discovery record | duplicates are not merged; counts overstate the frontier (D9) |
| Statistics | most counters are maintained | `stats.acquired` is never incremented (D7) |

## Not implemented

### Explicitly absent (non-goals)

These capabilities are absent by design, not by omission. No implementation of
them was found in the inspected scope (ABSENCE_VERIFIED, [EVID:SCOPE-001]: the
entire implementation is one file, read in full and scanned mechanically), and
`tools/verify.mjs` fails if such a symbol ever appears in the artifact.

```
RF spectrum scanning        NO      carrier synchronization      NO
SDR control                 NO      symbol-rate estimation       NO
DVB tuner control           NO      FEC decoding                 NO
DVB-S/S2 demodulation       NO      MPEG-TS decoding             NO
DVB-T/T2 demodulation       NO      DVB PSI/SI parsing           NO
DVB-C demodulation          NO      NIT-based discovery          NO
```

### Designed but not implemented

Specified in the design series (v0.8 … v0.35) in prose only. No code exists for any row.

| Area | Design reference | Missing artifact |
| --- | --- | --- |
| Capability-aware acquisition | v0.8 | capability lattice, requirements, capability provenance |
| Acquisition runtime | v0.10 | admission control, cancellation tokens, runtime-owned timeout/retry |
| Recognition runtime | v0.11 | response router, provider priority, recognition evidence |
| Candidate sources | v0.12–v0.13 | `CandidateSource` interface, discovery controller |
| Search domain and sessions | v0.14 | `DiscoveryDomain`, `ScanSession`, termination evaluator |
| Work items and frontier | v0.15 | `WorkItem`, leases, priority aging, fair arbitration |
| Evidence and provenance graph | v0.16 | `EvidenceGraph`, `Evidence`, `Claim` |
| Resource identity | v0.17 | `Locator`, identity resolution, redirect chains |
| Classification | v0.18 | type axes, classification assertions |
| Representations, artifacts, revisions | v0.19 | identity chain beyond the URL |
| Partitioning and strategies | v0.20–v0.21 | search-space partitions, strategy learning |
| Coverage and absence | v0.22–v0.23 | coverage claims, negative evidence |
| Goal-constrained discovery | v0.24–v0.27 | query planner, tactics, enumeration runtime |
| Reconciliation and expansion | v0.28–v0.30 | frontier dedup, unified arbitration |
| Cost ledger | v0.31 | reservation/allocation/consumption accounting |
| Durable, crash-safe state | v0.32 | transactions, checkpoints, recovery |
| Multi-worker coordination | v0.33–v0.35 | leases, fencing, conflicts, replication |

## Future — exploratory, not specified

Adaptive priority learned from observed yield; cross-domain discovery;
non-HTTP transports (filesystem, browser APIs, device services); completeness
claims of any kind. The design series discusses these, but not at specification
level, and none of them has design-reviewed contracts.

## Non-goals — deliberately out of scope

* RF spectrum scanning, SDR control, tuner control
* DVB-S/S2, DVB-T/T2, DVB-C demodulation
* carrier synchronization, symbol-rate estimation, FEC decoding
* MPEG transport-stream decoding
* DVB PSI/SI parsing and NIT-based discovery
* being a general-purpose crawler, an unrestricted Internet crawler, or a
  browser-automation framework
* replacing specialized DVB tooling
* claiming completeness of the open web

**The DVB relationship is inspiration only.** The generic analogues are
candidate generation, acquisition, observation, recognition and expansion —
never demodulation or transport decoding. See
[../research/dvb-blind-scan-inspiration.md](../research/dvb-blind-scan-inspiration.md).


## How these lists are verified

| List | Verification |
| --- | --- |
| Implemented | `tools/verify.mjs` (static: methods, providers, contracts) and `tools/checks.mjs` (behaviour: dedup, providers, provenance, persistence) |
| Partially implemented | `tools/simulate.mjs` reproduces D1/D2/D4/D9; `tools/verify.mjs` reports D3/D7/D8 |
| Not implemented (designed) | `tools/verify.mjs` symbol scan for design-only layers (ABSENCE_VERIFIED, [EVID:SCOPE-002]) |
| Not implemented (non-goal) | `tools/verify.mjs` symbol scan for DVB/RF terms |
