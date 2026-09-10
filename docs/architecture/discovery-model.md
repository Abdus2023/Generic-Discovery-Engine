# Discovery Model

Status: **normative for the canonical loop**; each stage is labelled CURRENT
(implemented in v0.7.1) or DESIGNED (prose only).

## The loop

```
Candidate
   │
   ▼
Acquisition
   │
   ▼
Observation
   │
   ▼
Recognition
   │
   ▼
Discovery
   │
   ▼
Candidate Expansion
   │
   ▼
Scheduler
   └───────────────↺
```

This is the only canonical system diagram in the repository. Documents that need
to show the loop must reproduce this shape rather than invent variants.

## Stage contracts

| Stage | Input | Output | Invariant | Failure mode | Owner (CURRENT) | Provenance recorded |
| --- | --- | --- | --- | --- | --- | --- |
| Candidate generation | seeds (current page, DOM, observed GETs), discoveries | `Candidate` with `type`, `target`, `depth`, `parent`, `priority` | target is canonical and allowed by scope; identity = `type:target` | malformed URL rejected; depth/candidate caps silently drop | Engine (`discover()`), seeded by `observeCurrentPage()`, DOM and network observers | `parent`, `hints`, `mechanism`, `depth` |
| Scheduler | candidate store | one `claimed` candidate, or nothing | **at most one active owner** (intended; violated by the re-queue path — see `concurrency.md`) | starvation, premature worker exit | `KnowledgeBase.claimNextCandidate()` | ledger `candidate-claimed` |
| Acquisition | `AcquisitionPlan` | `Observation` | ownership is declared before the network call; budget reserved before execution | timeout, HTTP error, origin cap, redirect loop | `Acquisition` (+ `OriginController`, `AcquisitionPolicy`) | ledger `request-started` / `request-completed` |
| Observation | HTTP result | `Observation` record | an observation exists even when acquisition fails | truncated body, unknown content type | `Observation` | `observationId` on the discovery |
| Recognition | `(candidate, observation)` | `Discovery[]` | providers are pure: no I/O, no scheduling, no enqueueing | no provider matches; provider throws (isolated, logged) | `ProviderRegistry` + provider classes | `providerName`, `mechanism`, `confidence` |
| Discovery | recognition output | stored `Discovery` + `ResourceRecord` merge | a discovery never creates candidates by itself | duplicate discoveries | `KnowledgeBase.addDiscovery()` | `candidateId`, `observationId`, `provenance` |
| Candidate expansion | `Discovery` with a URL | new candidate(s) | expansion owns dedup and depth bounds | unbounded growth, self-expansion | `GenericDiscoveryEngine.emitDiscovery()` → `discover()` | graph edge `parent → child` |

## Missing or weak contracts

| Gap | Consequence | Status |
| --- | --- | --- |
| No explicit contract for **candidate sources** (DOM, network, performance) | seeding logic lives in engine methods; a new source must edit the engine | DESIGNED as `CandidateSource` (v0.12) |
| No contract for **when a scan is finished** | "empty eligible set" and "budget exhausted" are conflated with completion | OPEN |
| No **coverage** or **exhaustion** object | the engine cannot state what has been searched | DESIGNED (v0.22 – v0.23) |
| No **observation immutability** guarantee | observations are plain records; the body can be referenced after truncation | OPEN |
| No **retry policy contract** | retry/backoff semantics live inside `KnowledgeBase.retryCandidate()` | CURRENT (implicit) |
| Recognition **confidence is not comparable across providers** | a 0.9 from CSS and a 0.9 from JSON mean different things | OPEN |

## Invariants that hold today

1. **Discovery is not acquisition.** Providers never perform I/O; only
   `Acquisition` and the network observer touch the network.
2. **Observations include failures.** A timeout or HTTP error produces an
   `Observation`, not an exception that escapes the loop.
3. **Expansion is engine-owned.** Providers return `Discovery[]`; only the
   engine turns a discovery into a candidate.
4. **Every candidate has a reason to exist.** `parent`, `mechanism` and hints are
   recorded at creation time.
5. **Every decision is replayable as a log.** The decision ledger records
   planning, denial, reservation, request, observation, discovery and completion
   with sequence numbers.

## Invariants that do NOT hold today

1. **Single ownership end to end** — an in-flight candidate can be re-queued by
   re-discovery (`queueCandidate()`), producing two owners and two acquisitions.
2. **Terminal failure** — `failed` candidates remain claimable and carry no
   backoff, so a broken target can consume the remaining request budget.
3. **Adaptive concurrency** — the adaptive counters update a value that the
   already-created worker pool never reads.
4. **Work preservation at quiescence** — a candidate waiting for backoff can be
   left behind when all workers exit.

## Designed extension of the model

The v0.8 … v0.35 series keeps this loop and inserts boundaries around it
(capabilities, work items, evidence, coverage). Those layers are **not** part of
the prototype; see [../roadmap/future-architecture.md](../roadmap/future-architecture.md).
Any statement that the engine "produces evidence", "measures coverage" or
"claims completeness" is a description of that design series, not of this code.
