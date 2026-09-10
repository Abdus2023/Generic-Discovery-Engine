# Prototype: the userscript

```
claim_kind:           CURRENT
implementation_state: IMPLEMENTED (this document describes the artifact's structure and
                      behaviour)
test_state:           TESTED (structure and behaviour exercised by tools/verify.mjs,
                      tools/checks.mjs and tools/simulate.mjs)
evidence_level:       DIRECT (the artifact itself)
claim_verification:   VERIFIED for structure, version, configuration, components and export
                      schema; behaviour-level verdicts live in ../analysis/claims.md
```

This document describes the artifact as it exists, not as the design series
intends it to become.

## Artifact

| Property | Value |
| --- | --- |
| Path | `prototype/generic-discovery-engine.user.js` |
| Version | 0.7.1 (`@version`, `CONFIG.version = 7`) |
| Size | 4,290 lines, ~64 KB |
| Shape | one IIFE, `'use strict'`, no dependencies, no build step |
| `@match` | `*://*/*` |
| `@run-at` | `document-start` |
| `@noframes` | set |
| Grants | `GM_getValue`, `GM_setValue`, `GM_xmlhttpRequest`, `@connect *` |
| Public handle | `window.GenericDiscoveryEngine` |
| Verified | parses and executes; `node tools/verify.mjs`, `node tools/checks.mjs`, `node tools/simulate.mjs` |

It runs under Tampermonkey/Violentmonkey by installing the file as a userscript.
The engine initializes itself (`engine.init()`), renders a small panel in the
bottom-right corner, observes the page, and starts a scan on bootstrap.

## Provenance of this file

The implementation was delivered inside a chat transcript and did not exist as a
repository file. It was extracted **verbatim** from
`archive/Continue Architecture Planning.md`, fenced block 10 (transcript lines
48948–54113, "Complete v0.7.1"), with the transcript's interleaved blank lines
removed. No code was edited, reformatted or repaired during extraction.

Verification of the extraction:

```bash
node --check prototype/generic-discovery-engine.user.js
node tools/verify.mjs    # parse check plus static assertions (47 passed, 4 known defects)
node tools/checks.mjs    # behavioural invariants in fresh contexts (4 passed)
node tools/simulate.mjs  # end-to-end scenario; reproduces D1/D2/D4/D9
```

Behaviour confirmed by executing the artifact: candidate deduplication by
`type:target`; provider selection sets for 11 content-type/body combinations;
provenance chain reconstruction (seed → candidate → observation → discovery →
child candidate); persistence round-trip of candidates, discoveries, resources
**and the ledger**, with the request budget deliberately reset per execution.

## Version history in the archive

| Version | Where | Parseable | Notes |
| --- | --- | --- | --- |
| 0.1.0 | transcript head, unfenced paste | no | backtick collisions from pasting; rejected by the transcript itself |
| 0.2.0 | transcript head, unfenced paste | no | same |
| 0.3.0 | transcript lines 52–2645 | yes | first complete script: candidate/observation/discovery/knowledge base/scheduler |
| 0.4.0 | lines 2791–7122, 13486–18265 | yes | two pastes of the same version |
| 0.5.0 | lines 7177–13452, 29438–34704 | yes | |
| 0.5.0 | lines 18378–23093 | **no** | contains `await` outside an async function |
| 0.6.0 | lines 23140–29350, 34754–43127, 43195–48360 | yes | three pastes |
| **0.7.1** | lines 48948–54113 | **yes** | acquisition plans, decision ledger, seven providers, adaptive counters, persistence caps |

Versions after 0.7.1 (v0.8 … v0.35) exist **only as prose** in
`archive/Continue Architecture Planning.md`. No code was produced for them.

## Configuration reference

Key values from `CONFIG` (see the file for the complete object):

| Setting | Default | Meaning |
| --- | --- | --- |
| `maxCandidates` | 750 | candidate-store cap |
| `maxRequests` | 150 | global acquisition budget per session |
| `concurrency` | 4 | workers created by `start()` |
| `requestTimeout` | 8000 ms | acquisition timeout |
| `maxDepth` | 5 | expansion depth limit |
| `maxBodyChars` | 2,000,000 | response truncation before recognition |
| `sameOriginOnly` | true | scope gate for candidates |
| `stripTrackingParams` | true | canonicalization rule |
| `networkBridge` | true | installs the page fetch/XHR bridge |
| `observeDomMutations` | true | MutationObserver on `href`/`src`/`action` |
| `discovery.*` | all true | enables links, resources, forms, metadata, text, network, performance, well-known |
| `policy.*` | forms/media/binary false | acquisition classes that are planned but denied |
| `origin.*` | 50 per origin / 150 ms / 2 concurrent | origin-level rate limiting |
| `adaptive.*` | enabled, 1…4 workers | counters only; the pool does not resize (D5) |
| `retry.*` | 2 retries, 500 ms → 8 s | exponential backoff |
| `priority.*` | depth 0.045 / confidence 0.08 / retry 0.05 | coefficients of `effectivePriority()` |

## Runtime components

| Component | Responsibility |
| --- | --- |
| `Candidate`, `Observation`, `Discovery`, `ResourceRecord`, `AcquisitionPlan` | data records with `serialize()` |
| `KnowledgeBase` | candidate/observation/discovery/resource stores, dedup, claiming, status transitions, retries, graph edges |
| `AcquisitionPolicy` | turns a candidate into an `AcquisitionPlan`; denies non-GET, depth, disabled classes, off-scope URLs |
| `OriginController` | per-origin cap, interval and concurrency |
| `Acquisition` | performs the HTTP request, produces the `Observation` |
| `Provider` + 7 providers | recognition |
| `ProviderRegistry` | `matching(observation)` |
| `NetworkObserver` | page bridge, performance observer, bridge event intake |
| `DecisionLedger` | append-only sequenced event log (cap 5000) |
| `GenericDiscoveryEngine` | orchestration, sources, expansion, persistence, UI, worker pool |

## User interface

A fixed panel with five buttons — **Scan**, **Pause**, **Stop**, **Clear**,
**Export** — and a status block showing version, run state, candidate/queue
counts, active workers, request budget, configured concurrency, statistics and
ledger length.

Two behaviours are visible in the UI and matter when interpreting a run:

* `Scan` calls `start()`, which is a no-op while `running === true`; after a scan
  drains naturally the flag stays true, so `Scan` appears dead until the page is
  reloaded (D4).
* the displayed concurrency is `currentConcurrency` (adaptive counter), not the
  number of live workers (`active`).

## Output

`Export` writes `gde-<timestamp>.json` with schema `gde-export-v7.1`:

```
{ schema, exportedAt, config, engine, ledger, networkEvents, diagnostics }
```

`engine` contains candidates, observations, discoveries (last 1200), resources
(last 1500), visited URLs, graph edges (last 3000) and statistics. Persistence
uses `GM_setValue(STORAGE_KEY, …)` with `STORAGE_KEY = 'generic-discovery-engine-v7'`,
debounced by 400 ms; `localStorage` is used when GM storage is unavailable.

## Extension points that actually exist

| Task | Where |
| --- | --- |
| Add a recognition provider | subclass `Provider`, implement `matches`/`recognize`, add to `ProviderRegistry` |
| Change scheduling weight | `CONFIG.typePriority`, `CONFIG.priority.*`, `Candidate.effectivePriority()` |
| Change acquisition policy | `AcquisitionPolicy.plan()` and `CONFIG.policy` |
| Add a candidate source | currently requires editing the engine (`observeCurrentPage`, `observeCurrentDom`, `observeNetworkGet`) |
| Change an acquisition transport | requires editing `Acquisition.request()`; there is no provider interface |

## What this file is not

* not a crawler product: it is scoped to one origin and bounded by budget, depth
  and candidate caps;
* not a DVB implementation: it contains no tuner, spectrum, demodulation, FEC,
  transport-stream or PSI/SI code;
* not the architecture of v0.8+: no capabilities, work items, evidence graph,
  coverage claims, leases or multi-context coordination exist here.
