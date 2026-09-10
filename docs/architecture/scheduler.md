# Scheduler

Status: **CURRENT**; DESIGNED improvements are labelled.

## Responsibility

The scheduler answers one question: *which candidate is acquired next, if any?*
It does not perform I/O, does not interpret responses, and does not create
candidates.

## Claim algorithm (as implemented)

```
claimNextCandidate():
    eligible ← candidates where
                   status ∈ {queued, failed}
                   and nextAttemptAt ≤ now
    if eligible is empty: return null
    sort eligible by effectivePriority descending
    candidate ← eligible[0]
    candidate.status ← 'claimed'
    candidate.claimedAt ← now
    return candidate
```

The operation is a bounded scan of an in-memory `Map` plus a full sort: O(n log n)
per claim. There is no heap, no separate queue object, and no aging or fairness
term.

| Property | Value |
| --- | --- |
| Selection | highest `effectivePriority()`; ties break by insertion order (stable sort) |
| Eligibility | `queued` or `failed`, not in backoff |
| Ownership | status transition happens inside this synchronous call |
| Complexity | full scan + sort per claim |
| Persistence | candidate store is serialized; the claim is not a durable lock |

## Supporting limits

| Mechanism | Default | Where enforced |
| --- | --- | --- |
| Global request budget | 150 | `reserveRequestSlot()`; a slot is never released |
| Per-origin request cap | 50 | `OriginController` |
| Per-origin concurrency | 2 | `OriginController` |
| Per-origin minimum interval | 150 ms | `OriginController` |
| Request timeout | 8 s | `Acquisition` |
| Retry budget | 2 retries, 500 ms → 8 s exponential | `KnowledgeBase.retryCandidate()` |
| Worker pool size | 4 (`currentConcurrency`) | `GenericDiscoveryEngine.start()` |

Policy denials (non-GET method, depth exceeded, forms/media/binary resources
disabled) happen *after* the claim; the candidate is then marked `skipped`.
`skipped` is terminal, so a policy change does not re-open denied candidates
within a session.

## Termination

The loop stops when any of the following is true:

1. every worker finds no eligible candidate and exits;
2. `requestsReserved >= maxRequests`;
3. `stop()` sets `stopRequested`.

There is **no completion criterion** beyond these: the engine cannot say that a
search space was covered, only that no work was claimable at a given instant.
`engine.running` is reset only for cases 2 and 3, so a scan that drains naturally
leaves `running === true` and the UI reports `running` indefinitely (defect D4).

## Adaptive concurrency — implemented in name only

`onSuccess()` / `onFailure()` adjust `currentConcurrency` between
`minConcurrency` (1) and `concurrency` (4) and log `adaptive-increase` /
`adaptive-decrease` to the ledger. The worker pool is created once inside
`start()`, and `start()` returns immediately while `running === true`, so the
adjusted value never changes the number of live workers (defect D5). The UI
displays the adjusted number next to the real worker count (`active`), which
makes the discrepancy visible.

## Worker-pool behaviour (verified)

* Workers are created only by `start()`; a user-triggered scan cannot re-create
  them while `running` is true.
* A worker exits permanently when `claimNextCandidate()` returns `null`. Because
  the queue is drained at a moment in time, a worker can exit while another
  worker is still expanding the frontier.
* Consequently the effective concurrency of a scan is often 1, even though
  `configured concurrency` is 4. `tools/simulate.mjs` measures the peak number of
  live workers; with an empty starting frontier it is 1, with a pre-populated
  frontier it reaches 4.

## DESIGNED (no code)

The following scheduling capabilities are specified in
`archive/Continue Architecture Planning.md` and are **not** implemented:

| Design | Version | Content |
| --- | --- | --- |
| Admission control and budget reservation before execution | v0.10 | runtime owns slots, not the provider |
| Work items, leases, lease recovery, priority aging | v0.15 | generic work model independent of candidates |
| Unified frontier arbitration across discovery/acquisition/expansion | v0.30 | one arbiter for all work kinds |
| Cost ledger | v0.31 | reservation → allocation → consumption accounting |
| Strategy learning / adaptive priority | v0.21 | learn from observed yield per region |

Until those exist, priority remains a static heuristic and fairness between
resource types is an emergent property of the priority table.
