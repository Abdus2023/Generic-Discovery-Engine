# Candidate Model

Claim state: `CURRENT` unless marked otherwise. Evidence state: `CORROBORATED`
(code + executed checks). Verification state: `VERIFIED` for identity,
lifecycle vocabulary and bounds; `CONTRADICTED` for the in-flight ownership
window (D1) and for terminal failure semantics (D3).

## Definition

> A **candidate** is a hypothesis that a target is worth acquiring.
> It does not assert that the target exists, is reachable, or is useful.

The prototype's target is always a URL, but the model is not URL-specific:
`target` is an opaque string and `type` selects the acquisition policy. No
non-URL target type is implemented.

## Object

```
Candidate {
    id                  unique id
    target              canonical URL
    type                api | manifest | sitemap | robots | url | feed | metadata |
                        network | frame | script | stylesheet | resource | form |
                        media | embedded | xml | text | unknown
    origin              scheme://host
    parent              id of the discovery's candidate (provenance)
    priority            caller-supplied base weight (defaults to discovery confidence)
    hints               { confidence, method, root, networkObserved, ... }
    depth               expansion depth (root = 0)
    attempts            retry counter
    status              lifecycle state (see below)
    nextAttemptAt       backoff gate for re-claiming
    createdAt, discoveredAt, queuedAt, claimedAt, plannedAt, acquiringAt,
    observedAt, recognizedAt, expandedAt, completedAt, failedAt, skippedAt
    alternateTypes, alternateOrigins, alternateParents    merge history
}
```

`identityKey()` returns `type:target`; `effectivePriority()` computes the
scheduling weight:

```
effectivePriority =
      priority
    + typePriority[type] * 0.20
    + hints.confidence   * 0.08
    - depth              * 0.045
    - attempts           * 0.05
```

`typePriority` is a static table (api 1.00 … unknown 0.25). The formula is a
fixed heuristic; it is not the "value × probability ÷ cost" expression that
appears in design material.

## Lifecycle

```
discovered → queued → claimed → planned → acquiring → observed
                                                      │
                             recognized → expanded → completed
                             (otherwise)  skipped | failed
                                                 │
                                          retry → queued
```

Claiming accepts states `queued` and `failed` whose `nextAttemptAt` has passed.
Backoff uses exponential delay `min(8000, 500 · 2^(attempts-1))` with
`maxRetries = 2`.

## Identity and deduplication

Deduplication happens at two levels.

1. **Candidate identity — `type:target`.** `addCandidate()` looks up
   `candidateKeys`; on a hit it merges `alternateTypes`, `alternateParents` and
   the maximum priority into the **existing** candidate and returns it.
   Consequence: the same URL discovered as a `script` and as a `url` is two
   candidates, by design (different acquisition intent).
2. **Resource identity — the canonical URL.** `ResourceRecord`s are keyed by
   canonical URL and carry a `status`. `shouldAcquireResource(url)` refuses a new
   acquisition when the resource is already `acquired`.

Canonicalization: `new URL(target, location.href)`, fragment removed, tracking
parameters stripped when `stripTrackingParams` is set, `http(s)` only.

**Scope gate:** `isAllowedUrl()` restricts candidates to the current origin
while `CONFIG.sameOriginOnly` is true (the shipped default). A non-URL or
cross-origin target is rejected at creation time and again at planning time.

## Bounds

| Limit | Default | Effect |
| --- | --- | --- |
| `maxCandidates` | 750 | new candidates are dropped when the store is full |
| `maxDepth` | 5 | deeper candidates are planned but denied (`max-depth`) |
| `maxRequests` | 150 | global acquisition budget for the process lifetime |
| `maxBodyChars` | 2,000,000 | response bodies are truncated before recognition |

Dropping is silent from the caller's perspective: `discover()` returns `null`
and records a diagnostic only for the candidate cap.

## Known deviations from the stated model

| Deviation | Evidence | Consequence |
| --- | --- | --- |
| Re-discovery can re-queue a candidate that is `claimed`, `planned`, `acquiring` or `observed` | `KnowledgeBase.queueCandidate()` refuses only `completed`/`skipped` | two owners, duplicate acquisition (defect D1) |
| `failed` is a claimable state with no backoff after retries are exhausted | `claimNextCandidate()` eligibility + `markFailed()` | budget burn on permanently failing targets (defect D3) |
| Re-queued candidates reuse the existing id, so the ledger shows repeated `candidate-claimed`/`candidate-enqueued` events for one candidate | `stats.queued` exceeds the number of candidates | ledger length is not a work estimate |
| `stats.acquired` is never incremented | `Acquisition` does not update it | UI/export expose a permanently zero counter |

## Design-only extensions

`CandidateSource` (v0.12), `WorkItem` (v0.15), capability requirements (v0.8) and
candidate fingerprints are **DESIGNED** and are not present in the code. See
[../roadmap/future-architecture.md](../roadmap/future-architecture.md).
