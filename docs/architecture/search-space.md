# Search Space

Claim state: `CURRENT` for the sections describing today's behaviour,
`SPECIFIED`/`PLANNED` where marked. Evidence state: `DIRECT` (code) and
`CORROBORATED` (executed checks). Verification state: `VERIFIED` for bounds and
termination triggers, `PARTIALLY_VERIFIED` for duplicate suppression.
This document owns the question *"what is being searched, and what bounds
it?"* — no other document redefines it.

## Model

```
Search space
     │
     ▼
Candidate generator / seeds
     │
     ▼
Scheduler
     │
     ▼
Acquisition (probe)
     │
     ▼
Observation
     │
     ▼
Recognition (knowledge update)
     │
     ▼
New search space  ↺
```

The prototype realizes this loop for one origin. The search space is *the set of
candidates reachable from the seeds through expansion*, and it exists only as the
candidate store — there is no separate partition, region or coverage object.

## Properties

| Question | Answer in v0.7.1 | Status |
| --- | --- | --- |
| Is the space finite? | Bounded in practice, not enumerable: URL space is infinite, but candidate creation is capped (`maxCandidates` 750) and the run is capped by budget (150 requests) | CURRENT |
| Is it dynamically expanding? | Yes — recognition emits discoveries, discoveries emit candidates while workers are running | CURRENT |
| What bounds candidate growth? | `maxCandidates`; `maxDepth` 5 denies deeper acquisition after planning; origin scope (`sameOriginOnly`) rejects off-origin targets | CURRENT |
| What prevents duplicate work? | Candidate identity (`type:target`), the resource acquisition guard, and `visited` (set on completion) | CURRENT (with defect D1 while in flight, D9 at discovery level) |
| What determines priority? | `effectivePriority()`: base priority + type weight + confidence hint − depth penalty − retry penalty | CURRENT |
| What determines termination? | Empty eligible set, `maxRequests` reached, or `stop()` | CURRENT (no completion criterion; D4) |
| What is negative evidence? | Nothing is modelled. A failed acquisition is an observation, not evidence of absence | **NOT IMPLEMENTED** (DESIGNED v0.23) |
| What constitutes coverage? | Nothing is measured. "Exhausted" in logs means "no candidate is currently eligible" | **NOT IMPLEMENTED** (DESIGNED v0.22) |
| Can candidates be revisited? | Yes while `queued`; yes after `failed` (unbounded, D3); no after `completed`/`skipped` | CURRENT |
| Can candidates become stale? | No expiry, no TTL, no revalidation window | **NOT IMPLEMENTED** |
| Is historical knowledge used? | Only within a run and across reloads through the persisted store; nothing influences scoring | CURRENT (persistence), **NOT IMPLEMENTED** (scoring) |
| Is discovery exhaustive or opportunistic? | Opportunistic: whatever the current frontier and priority order yield before the budget is spent | CURRENT |

## Seeds

| Seed | Depth | Priority | Hint confidence | Mechanism |
| --- | --- | --- | --- | --- |
| Current page URL | 0 | 1.0 | 1.0 | `current-page` |
| Observed network GET | 0 | 0.65 | 0.70 | `network-get` |
| DOM link / script / resource | 1 | 0.50 / 0.45 / 0.40 | — | `dom-observer-*` |
| Discovery-derived | parent depth + 1 | discovery confidence | discovery confidence | provider mechanism tag |

The prototype has no *explicit* seed object: seeds are the first calls to
`discover()`. Design series v0.14 introduces explicit seeds and separates
*seed ≠ candidate*; that distinction does not exist in code.

## Growth, deduplication and starvation

```
expansion ──► addCandidate() ──► dedup by type:target ──► queueCandidate()
     │                │                                        │
     │                └── cap reached → dropped (diagnostic)    └── D1: re-queues in-flight work
     ▼
emitDiscovery() always stores a Discovery first (D9)
```

* **Growth is bounded, not throttled.** There is no rate control on candidate
  creation, only a hard cap and a silent drop.
* **Priority is static.** There is no aging, so a low-priority candidate can be
  postponed indefinitely while higher-priority work keeps being generated
  (starvation is possible; no fairness term exists).
* **Persistence does not change the search space.** Reloading restores the
  candidate store, but `requestsReserved` is deliberately reset and `running` is
  not restored, so a restored scan is a new run over old state.

## Termination semantics (current vs desired)

| Situation | Current | Desired (DESIGNED) |
| --- | --- | --- |
| no candidate eligible *now* | worker exits permanently (D2) | wait for new work or declare quiescence |
| work waiting on backoff | abandoned if all workers exit (D4) | re-scheduled |
| request budget exhausted | `running = false`; scan ends | explicit, reported exhaustion |
| `stop()` called | cooperative stop; in-flight request continues | cancellation with runtime ownership (v0.10) |
| "the space is covered" | not representable | coverage claim (v0.22) |

## What must never be claimed

The prototype cannot state that its results are exhaustive, that a URL does not
exist, or that a region was fully searched. Those claims require coverage and
absence objects that do not exist. The strongest accurate statements are: which
candidates existed and why, what each attempt observed, what was interpreted,
what budget was consumed, and what remained unclaimable at that moment.

## DESIGNED

| Layer | Version | Effect on the search space |
| --- | --- | --- |
| Partitions and strategies | v0.20 | the space becomes explicitly partitioned; strategy becomes selectable per region |
| Adaptive strategy learning | v0.21 | observed yield per partition/strategy influences future selection |
| Coverage claims | v0.22 | the engine can state what was explored, with evidence |
| Negative evidence / absence | v0.23 | failure-to-find becomes an assertion *backed by coverage*, not a conclusion |
| Goal-constrained discovery | v0.24–v0.25 | relevance filters the frontier against a goal |
| Reconciliation and expansion | v0.28–v0.29 | reconverging paths and newly revealed regions are handled |
| Unified frontier arbitration | v0.30 | one arbiter across discovery, acquisition and enumeration work |

See [../roadmap/future-architecture.md](../roadmap/future-architecture.md).
