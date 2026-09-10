# Prototype Scope

Status boundary for the shipped userscript (v0.7.1). Statements here are
verifiable against `prototype/generic-discovery-engine.user.js` with
`tools/verify.mjs`.

## CURRENT — implemented and verifiable

| Capability | Evidence in the artifact |
| --- | --- |
| Seed generation | `observeCurrentPage()` (current URL), `observeCurrentDom()` (DOM), `observeNetworkGet()` / performance entries |
| Candidate normalization | `canonicalizeUrl()`: URL resolution, fragment removal, tracking-parameter stripping |
| Candidate deduplication | `KnowledgeBase.addCandidate()` via `identityKey() = type:target` |
| Resource-level acquisition guard | `shouldAcquireResource()` on canonical URL + resource status |
| Candidate claiming | `KnowledgeBase.claimNextCandidate()` — synchronous ownership transition |
| Concurrency | worker pool created by `start()`; default 4 workers; cooperative pause/stop |
| HTTP acquisition | `Acquisition.request()` via `GM_xmlhttpRequest`, `fetch` fallback |
| Timeout behaviour | 8 s timer races the request; timeout produces an `Observation` with `status: 'timeout'` |
| Content-type handling | `contentTypeBase()`, `looksLike*()` sniffing helpers |
| HTML recognition | `HtmlProvider`: links, frames, scripts, media, form actions, metadata (`og:`, `twitter:`, meta-refresh) |
| JSON recognition | `JsonProvider`: recursive walk for URL-like values |
| Text recognition | `TextProvider`: HTTP(S) URLs in free text |
| Additional recognition | `XmlProvider`, `CssProvider`, `JavaScriptProvider`, `BinaryProvider` |
| Resource extraction | DOM observer also proposes scripts, frames, images and form actions |
| URL extraction | per-provider `extractUrlsFromText` / `extractCssUrls` / `extractXmlLocs` |
| Candidate expansion | `emitDiscovery()` → `discover()` with `parent`, `depth + 1`, confidence-derived priority |
| Persistence | `persist()` / `restore()` with caps; `GM_setValue` or `localStorage` |
| Reporting / export | `exportData()` (`gde-export-v7.1`) and the on-page stats block |
| UI | panel with Scan / Pause / Stop / Clear / Export |
| Error handling | per-provider `try/catch`, acquisition failures become observations, diagnostics recorded |
| Request budgeting | `reserveRequestSlot()` against `maxRequests` |
| Origin rate limiting | `OriginController`: cap, interval, per-origin concurrency |
| Retry with backoff | `KnowledgeBase.retryCandidate()`, 2 retries, 500 ms → 8 s |
| Decision ledger | `DecisionLedger`: append-only sequenced events, capped at 5000 |
| Graph edges | `KnowledgeBase.addEdge()` — parent/child relations, capped at 5000 |
| Policy gating | `AcquisitionPolicy.plan()`: GET-only, depth, forms/media/binary classes |

## DESIGNED — specified in the design series, NOT implemented

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

## FUTURE — exploratory, not specified

Adaptive priority learned from observed yield; cross-domain discovery;
non-HTTP transports (filesystem, browser APIs, device services); completeness
claims of any kind. The design series discusses these, but not at specification
level, and none of them has design-reviewed contracts.

## NON-GOAL — deliberately out of scope

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

## Explicit non-implementations to check before writing documentation

```
RF spectrum scanning        NO      carrier synchronization      NO
SDR control                 NO      symbol-rate estimation       NO
DVB tuner control           NO      FEC decoding                 NO
DVB-S/S2 demodulation       NO      MPEG-TS decoding             NO
DVB-T/T2 demodulation       NO      DVB PSI/SI parsing           NO
DVB-C demodulation          NO      NIT-based discovery          NO
```

These are asserted mechanically by `tools/verify.mjs` (symbol scan over the
artifact), so a future edit that introduces such code fails the check.
