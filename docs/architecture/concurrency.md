# Concurrency

```
claim_kind:           CURRENT · SPECIFIED for cross-context coordination
implementation_state: IMPLEMENTED for the synchronous claim operation · PARTIAL end to end
                      (re-queue defeats it, D1) · NOT_IMPLEMENTED across execution contexts
test_state:           TESTED (tools/verify.mjs static checks; tools/simulate.mjs measures
                      concurrent owners and duplicate acquisitions)
evidence_level:       CORROBORATED (static code + executed behaviour)
claim_verification:   VERIFIED for the claim operation · CONTRADICTED for the end-to-end
                      single-owner invariant (D1) · UNVERIFIED for cross-context claims
```

## The invariant

> **A candidate may have at most one active owner.**

Ownership means: a candidate is in a state in which exactly one worker may act on
it, and no other worker may select it until that worker releases it.

## Canonical concurrency model

```
              Candidate Queue
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
       Worker A            Worker B
          │                   │
          ▼                   ▼
       claim(X)             claim(X)
          │                   │
          │               REJECT
          ▼
       acquire(X)
```

## What the code actually does

`KnowledgeBase.claimNextCandidate()` is a **synchronous** function:

1. collect candidates whose status is `queued` or `failed` and whose
   `nextAttemptAt` has passed;
2. sort by `effectivePriority()`;
3. take the first, set `status = 'claimed'`, add its id to the `claimed` set;
4. return it.

`GenericDiscoveryEngine.worker()` calls it and, **before its first `await`**,
passes the claimed candidate to `plan()` and then to `executePlan()`, which
transitions the candidate to `planned` and then `acquiring` — also synchronously.

```
Worker A ── claim(X) ──> X.status = 'claimed' ──> plan(X) ──> markAcquiring(X) ──┐
                                                                                 │
                                            first suspension point (network I/O)┘
Worker B ── claim(X) ──> status is 'acquiring'  ──> not eligible ──> REJECT
```

### Why this is safe at the claim site

JavaScript executes to completion between suspension points. No other worker can
run between step 3 and the first `await`, and the status transition removes the
candidate from the eligible set before that suspension. The safety argument is
therefore:

1. the claim is synchronous;
2. the eligibility filter excludes every non-terminal state;
3. the first `await` happens after the transition.

This is **not** a general lock. It holds only because:

* there is exactly one JavaScript execution context (one bookmarklet instance,
  one main thread, one engine object);
* every path from selection to suspension preserves the ownership transition;
* no other writer mutates candidate status concurrently.

It says nothing about multiple tabs, workers, service workers, other browsers, or
another device — that boundary is addressed in design only (v0.33 leases/fencing,
v0.34 conflict resolution).

## The unsafe alternative

```
Worker A ── inspect X ── await ──────────────► acquire X
Worker B ── inspect X ── await ──────────────► acquire X
```

Two workers observe the same state, both suspend, and both proceed: the same
resource is acquired twice. The failure is not caused by the network call; it is
caused by the gap between the **decision** and the **transition** across a
suspension point.

`tools/simulate.mjs --unsafe-control` implements exactly this scheduler (no
ownership transition) and the harness reports concurrent owners > 1, confirming
that the measurement can detect the failure it is looking for.

## The violation that exists today

The claim site is safe, but the invariant is **not preserved end to end**:

```
addCandidate()  → re-discovery of a known type:target returns the EXISTING candidate
discover()      → calls queueCandidate(existing)
queueCandidate()→ refuses only 'completed' and 'skipped'
                → for claimed/planned/acquiring/observed it sets status = 'queued'
claimNextCandidate() → another worker claims the in-flight candidate
```

Result: two workers own one candidate, `shouldAcquireResource()` is checked by
both before either finishes, and the URL is acquired twice.

Observed by `tools/simulate.mjs` (24-way expansion, 4 workers, 27 URLs):

```
maxConcurrentOwnersPerCandidate : 2 – 4
URLs fetched more than once     : 12 – 18
anomalies                       : CONCURRENT_OWNER … owners=2
```

The path is reachable whenever expansion, the DOM observer or the network bridge
re-proposes a URL while it is being acquired — which is the normal case in a
densely linked page.

| Aspect | Verdict |
| --- | --- |
| Claim operation is atomic | PROVED (static + dynamic) |
| End-to-end single-owner invariant | **VIOLATED** in v0.7.1 (dynamic) |
| Cross-context safety | NOT IMPLEMENTED, NOT CLAIMED |
| Duplicate suppression after a completed acquisition | holds via `shouldAcquireResource()` |
| Duplicate suppression while an acquisition is in flight | does not hold |

Repairing this requires either (a) making `queueCandidate()` refuse every
non-terminal state, or (b) separating "work exists" from "candidate state" — the
`WorkItem`/frontier model of v0.15. Both are implementation decisions, not
documentation decisions; see
[../prototype/limitations.md](../prototype/limitations.md#d1).

## Other concurrency-relevant behaviour

| Behaviour | Current implementation |
| --- | --- |
| Worker cancellation | `stop()` sets `stopRequested`; workers finish the current candidate and exit |
| Pause / resume | cooperative: workers `await sleep(100)` while `paused` |
| Dynamic candidate generation | workers expand the frontier while looping; new candidates are claimable by any worker |
| Duplicate candidates generated concurrently | prevented at identity level by `candidateKeys` only if the *type* matches |
| Worker termination | a worker exits permanently when no candidate is eligible at that instant (see limitations, D2) |
| Queue exhaustion | treated as termination, not as a pause; `running` stays `true` (D4) |
| Retry | exponential backoff written to `nextAttemptAt`; the backoff gate is ignored for `failed` candidates (D3) |

## DESIGNED (no code)

* **v0.15** — work items with explicit leases, lease recovery, priority aging.
* **v0.33** — multi-worker coordination: registration, capabilities, claim
  tokens, leases, heartbeats, fencing tokens, worker death handling.
* **v0.34** — optimistic concurrency, versioned events, conflict records,
  deterministic resolution, provenance preserving merges.
* **v0.35** — cross-context event transport and replication.

The design series states its own boundary explicitly: a browser profile may offer
shared storage and claim records, but that is *profile coordination*, **not**
distributed consensus. Keep that distinction if those layers are ever built.

## Decisions

### D-03 — Ownership is established synchronously before any suspension

* **Decision:** `claimNextCandidate()` mutates candidate state before the worker
  performs its first `await`.
* **Rationale:** JavaScript runs to completion between suspension points, so a
  synchronous transition is sufficient to exclude other workers in the same
  context, without locks.
* **Alternatives considered:** "inspect, then acquire" with a re-check after the
  network call (rejected: two workers can pass the check and both acquire, as the
  `--unsafe-control` harness mode demonstrates).
* **Constraint:** safety depends on a single execution context and on every path
  from selection to suspension preserving the transition.
* **Consequence:** the guard is correct but *local*; it says nothing about tabs,
  workers or devices, and it is defeated elsewhere by the re-queue path (D1).
* **Status:** IMPLEMENTED at the claim site; **CONTRADICTED end to end** by D1.

### D-04 — No distributed coordination in the prototype

* **Decision:** the prototype does not attempt cross-context ownership.
* **Rationale:** the browser offers shared storage, not atomic claims; a
  half-implemented lease protocol would be worse than none.
* **Alternatives considered:** `localStorage`-based claim records (rejected for
  the prototype; DESIGNED properly in v0.33 with leases, heartbeats and fencing).
* **Consequence:** two tabs scanning the same site duplicate each other's work by
  construction. The design series keeps the boundary explicit: profile
  coordination ≠ distributed consensus.
* **Status:** DESIGNED (v0.33/v0.34), not implemented.
