# Concurrency

> **Status:** DESIGNED
>
> **Source:** `Continue Architecture Planning.md`; `Userscript Discovery Prototype.md`
>
> **Purpose:** Concurrency: worker ownership, claiming, leases, fencing, heartbeats and concurrent execution.

## Source Sections

- **What changed — 1. Concurrent claiming is now explicit** — `USP-071` — `Userscript Discovery Prototype.md` L4713–4756
- **v0.13 — 15. Concurrent source execution** — `CAP-205` — `Continue Architecture Planning.md` L60119–60166
- **v0.14 — 16. Lease-based claims** — `CAP-250` — `Continue Architecture Planning.md` L61415–61461
- **v0.15 — 7. Claiming becomes a formal protocol** — `CAP-280` — `Continue Architecture Planning.md` L62349–62425
- **v0.15 — 8. Work lease** — `CAP-281` — `Continue Architecture Planning.md` L62427–62458
- **v0.15 — 9. Lease recovery** — `CAP-282` — `Continue Architecture Planning.md` L62460–62490
- **v0.33 — Multi-Worker / Multi-Context Coordination** — `CAP-1078` — `Continue Architecture Planning.md` L89042–89108
- **v0.33 — Multi-Worker Coordination & Distributed Claiming** — `CAP-1080` — `Continue Architecture Planning.md` L89120–89144
- **v0.33 — 33.1 Worker identity** — `CAP-1081` — `Continue Architecture Planning.md` L89146–89198
- **v0.33 — 33.2 Worker registration** — `CAP-1082` — `Continue Architecture Planning.md` L89200–89249
- **v0.33 — 33.3 Worker capabilities** — `CAP-1083` — `Continue Architecture Planning.md` L89251–89300
- **v0.33 — 33.4 Claiming is the synchronization boundary** — `CAP-1084` — `Continue Architecture Planning.md` L89302–89332
- **v0.33 — 33.5 ClaimToken** — `CAP-1085` — `Continue Architecture Planning.md` L89334–89379
- **v0.33 — 33.6 Claim ≠ lease** — `CAP-1086` — `Continue Architecture Planning.md` L89381–89405
- **v0.33 — 33.7 Lease lifecycle** — `CAP-1087` — `Continue Architecture Planning.md` L89407–89427
- **v0.33 — 33.8 LeaseManager** — `CAP-1088` — `Continue Architecture Planning.md` L89429–89462
- **v0.33 — 33.9 Heartbeats** — `CAP-1089` — `Continue Architecture Planning.md` L89464–89486
- **v0.33 — 33.10 Fencing tokens** — `CAP-1090` — `Continue Architecture Planning.md` L89488–89525
- **v0.33 — 33.12 Worker death** — `CAP-1092` — `Continue Architecture Planning.md` L89556–89591
- **v0.33 — 33.13 Duplicate execution** — `CAP-1093` — `Continue Architecture Planning.md` L89593–89621
- **v0.33 — 33.14 Execution identity** — `CAP-1094` — `Continue Architecture Planning.md` L89623–89655
- **v0.33 — 33.16 Duplicate execution ≠ independent evidence** — `CAP-1096` — `Continue Architecture Planning.md` L89698–89728
- **v0.33 — 33.17 Worker-local vs shared state** — `CAP-1097` — `Continue Architecture Planning.md` L89730–89765
- **v0.33 — 33.18 CoordinationManager** — `CAP-1098` — `Continue Architecture Planning.md` L89767–89801
- **v0.33 — 33.19 Coordination vs arbitration** — `CAP-1099` — `Continue Architecture Planning.md` L89803–89827
- **v0.33 — 33.20 Worker selection** — `CAP-1100` — `Continue Architecture Planning.md` L89829–89869
- **v0.33 — 33.21 Worker affinity** — `CAP-1101` — `Continue Architecture Planning.md` L89871–89890
- **v0.33 — 33.22 Worker capacity** — `CAP-1102` — `Continue Architecture Planning.md` L89892–89919
- **v0.33 — 33.23 Distributed accounting** — `CAP-1103` — `Continue Architecture Planning.md` L89921–89953
- **v0.33 — 33.24 Worker-local caches** — `CAP-1104` — `Continue Architecture Planning.md` L89955–89977
- **v0.33 — 33.25 Cross-worker event ordering** — `CAP-1105` — `Continue Architecture Planning.md` L89979–90012
- **v0.33 — 33.26 Causal provenance** — `CAP-1106` — `Continue Architecture Planning.md` L90014–90030
- **v0.33 — 33.27 Coordination events** — `CAP-1107` — `Continue Architecture Planning.md` L90032–90060
- **v0.33 — 33.29 Split-brain** — `CAP-1109` — `Continue Architecture Planning.md` L90085–90111
- **v0.33 — 33.31 Coordination scope** — `CAP-1111` — `Continue Architecture Planning.md` L90154–90178
- **v0.33 — 33.35 v0.33 result** — `CAP-1115` — `Continue Architecture Planning.md` L90276–90349

## Related Documents

- [Scheduling](scheduler.md)
- [Work Items and Frontier Arbitration](work-and-frontier.md)
- [Coordination, Consistency and Transport](coordination.md)
- [Userscript Development Narrative](../prototype/userscript.md)

---

<!-- USP-071 | Userscript Discovery Prototype.md L4713–4756 | turn 15 | version ? -->
### What changed — 1. Concurrent claiming is now explicit

> **Source sections:** `USP-071`
>
> [DOCUMENTATION REVIEW] Contradiction **C-03** ([Review Notes](../REVIEW-NOTES.md#c-03--))
>
> **Note:** split at numbered boundary

**1. Concurrent claiming is now explicit.**

The important change is:

```
claimNextCandidate()
```

which synchronously moves a candidate:

```
queued → claimed
```

before the worker performs its first `await`.

So with three workers:

```
Queue: A B C D E

Worker 1 → claims A
Worker 2 → claims B
Worker 3 → claims C

Queue: D E
Claimed: A B C
```

There is no opportunity for two workers to acquire `A`.

`visited` and `claimed` are deliberately different:

```
visited = completed candidates
claimed = currently owned candidates
queued  = candidates waiting for a worker
```

That distinction becomes particularly important once acquisition is asynchronous.

<!-- CAP-205 | Continue Architecture Planning.md L60119–60166 | turn 39 | version 0.13 -->
## v0.13 — 15. Concurrent source execution

> **Source sections:** `CAP-205`
>
> [DOCUMENTATION REVIEW] Contradiction **C-03** ([Review Notes](../REVIEW-NOTES.md#c-03--))

The same race condition from candidate claiming appears here.

Suppose:

```
Observation O
```

causes two controllers/workers to schedule:

```
HTML source
HTML source
```

If both execute concurrently, we may duplicate work.

Therefore source task claiming must be atomic:

```
QUEUED
   │
   │ atomic claim
   ▼
CLAIMED
   │
   ▼
RUNNING
```

Not:

```JavaScript
if (task.status === 'queued') {
    await something();
    task.status = 'running';
}
```

The check and transition need to occur as one logical operation.

This is the same invariant:

> **Claiming is a state transition, not a boolean check.**

---

<!-- CAP-250 | Continue Architecture Planning.md L61415–61461 | turn 41 | version 0.14 -->
## v0.14 — 16. Lease-based claims

> **Source sections:** `CAP-250`
>
> [DOCUMENTATION REVIEW] Contradiction **C-03** ([Review Notes](../REVIEW-NOTES.md#c-03--))

This leads directly to a stronger version of the v0.13 atomic-claim rule.

A simple state:

```
QUEUED → CLAIMED
```

is insufficient for resumability.

Instead:

```JavaScript
{
    status: 'claimed',

    claimedBy: 'scan-session-id',

    claimId: 'claim-123',

    claimedAt: 1757500000000,

    leaseUntil: 1757500030000
}
```

Then the system can determine:

```
lease valid?
    │
    ├── yes → owner still active
    │
    └── no → claim recoverable
```

This is especially valuable if the userscript eventually supports:

* multiple tabs
* workers
* background execution
* multiple browser contexts
* crash recovery

---

<!-- CAP-280 | Continue Architecture Planning.md L62349–62425 | turn 43 | version 0.15 -->
## v0.15 — 7. Claiming becomes a formal protocol

> **Source sections:** `CAP-280`
>
> [DOCUMENTATION REVIEW] Contradiction **C-03** ([Review Notes](../REVIEW-NOTES.md#c-03--))

This is one of the most important improvements.

Bad:

```JavaScript
if (item.status === 'queued') {
    item.status = 'claimed';
}
```

That is vulnerable to concurrent workers.

Instead:

```
             QUEUED
                │
         atomic claim()
                │
       ┌────────┴────────┐
       │                 │
    success            failure
       │                 │
       ▼                 ▼
   CLAIMED             QUEUED
```

The operation itself must atomically establish ownership.

Conceptually:

```JavaScript
claim(workId, ownerId, leaseMs) {
    const work = this.items.get(workId);

    if (!work) {
        return null;
    }

    if (work.status !== 'queued') {
        return null;
    }

    work.status = 'claimed';
    work.claimedBy = ownerId;
    work.claimId = makeId('claim');
    work.claimedAt = now();
    work.leaseUntil =
        now() + leaseMs;

    return work;
}
```

In a single-threaded userscript this is locally atomic because there is no `await` between the check and mutation.

But if the state eventually moves to:

* IndexedDB transactions
* SharedWorker
* multiple tabs
* service worker
* server-backed coordination

the storage layer must provide an actual atomic compare-and-set/transaction.

Therefore the **contract**, not this implementation detail, is what matters:

```
Claim(x)
    ⇒
    exactly one owner
```

---

<!-- CAP-281 | Continue Architecture Planning.md L62427–62458 | turn 43 | version 0.15 -->
## v0.15 — 8. Work lease

> **Source sections:** `CAP-281`
>
> [DOCUMENTATION REVIEW] Contradiction **C-03** ([Review Notes](../REVIEW-NOTES.md#c-03--))

The lease is different from ownership forever.

```
claim
 │
 ├── owner = worker A
 └── lease = 30 seconds
```

If worker A disappears:

```
lease expires
    ↓
work becomes recoverable
```

This prevents:

```
dead worker
   ↓
permanent CLAIMED state
   ↓
lost work
```

A lease therefore gives us crash recovery without requiring a distributed consensus system.

---

<!-- CAP-282 | Continue Architecture Planning.md L62460–62490 | turn 43 | version 0.15 -->
## v0.15 — 9. Lease recovery

> **Source sections:** `CAP-282`
>
> [DOCUMENTATION REVIEW] Contradiction **C-03** ([Review Notes](../REVIEW-NOTES.md#c-03--))

A recovery operation:

```JavaScript
recoverExpired(nowValue = now()) {
    for (const work of this.items.values()) {
        if (
            work.status === 'claimed' &&
            work.leaseUntil &&
            work.leaseUntil <= nowValue
        ) {
            work.status = 'queued';
            work.claimedBy = null;
            work.claimId = null;
            work.leaseUntil = null;
        }
    }
}
```

The event ledger should record:

```
work-lease-expired
work-requeued-after-expiry
```

so recovery is observable rather than invisible mutation.

---

<!-- CAP-1078 | Continue Architecture Planning.md L89042–89108 | turn 79 | version 0.33 -->
## v0.33 — Multi-Worker / Multi-Context Coordination

> **Source sections:** `CAP-1078`
>
> [DOCUMENTATION REVIEW] Contradiction **C-03** ([Review Notes](../REVIEW-NOTES.md#c-03--))

The next problem emerges naturally.

A browser userscript may eventually have:

```
Tab A
  └── Worker A

Tab B
  └── Worker B

Service Worker
  └── Worker C

Background runtime
  └── Worker D
```

All may see the same durable frontier.

That introduces:

```
              DURABLE FRONTIER
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
       Worker A   Worker B   Worker C
          │          │          │
          └──────────┼──────────┘
                     ▼
                shared state
```

The next architectural question therefore becomes:

> **How can multiple execution contexts safely share the frontier without double-claiming work, corrupting accounting, or producing false independence?**

That leads to:

**v0.33 — Multi-Worker Coordination & Distributed Claiming**

with the new boundaries:

```
shared frontier
        ↓
worker identity
        ↓
leases
        ↓
atomic claiming
        ↓
heartbeat
        ↓
fencing
        ↓
duplicate execution detection
        ↓
cross-worker accounting
        ↓
coordination provenance
```

This is where the userscript prototype starts approaching the coordination semantics of a real distributed runtime.

<!-- CAP-1080 | Continue Architecture Planning.md L89120–89144 | turn 81 | version 0.33 -->
## v0.33 — Multi-Worker Coordination & Distributed Claiming

> **Source sections:** `CAP-1080`
>
> [DOCUMENTATION REVIEW] Contradiction **C-03** ([Review Notes](../REVIEW-NOTES.md#c-03--))

v0.32 made the frontier durable.

The next problem is concurrency.

Once multiple execution contexts share that frontier, this becomes possible:

```
                    DURABLE FRONTIER
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
          Worker A      Worker B      Worker C
             │             │             │
             └─────────────┼─────────────┘
                           ▼
                    SHARED STATE
```

The central question is:

> **How can multiple workers execute concurrently without claiming the same work, corrupting resource accounting, or confusing duplicate execution with independent evidence?**

---

<!-- CAP-1081 | Continue Architecture Planning.md L89146–89198 | turn 81 | version 0.33 -->
## v0.33 — 33.1 Worker identity

> **Source sections:** `CAP-1081`
>
> [DOCUMENTATION REVIEW] Contradiction **C-03** ([Review Notes](../REVIEW-NOTES.md#c-03--))
>
> [DOCUMENTATION REVIEW] Contradiction **C-04** ([Review Notes](../REVIEW-NOTES.md#c-04--))

Every execution context needs a durable identity.

```JavaScript
class WorkerIdentity {
    constructor(data = {}) {
        this.id =
            data.id || makeId('worker');

        this.runtimeId =
            data.runtimeId || null;

        this.contextType =
            data.contextType || 'browser-tab';

        this.instanceId =
            data.instanceId || null;

        this.startedAt =
            data.startedAt || now();

        this.lastHeartbeatAt =
            data.lastHeartbeatAt || null;
    }

    serialize() {
        return { ...this };
    }
}
```

Examples:

```
worker-A
  contextType = browser-tab

worker-B
  contextType = iframe

worker-C
  contextType = service-worker

worker-D
  contextType = background-runtime
```

Worker identity is not user identity.

It identifies an execution participant.

---

<!-- CAP-1082 | Continue Architecture Planning.md L89200–89249 | turn 81 | version 0.33 -->
## v0.33 — 33.2 Worker registration

> **Source sections:** `CAP-1082`
>
> [DOCUMENTATION REVIEW] Contradiction **C-03** ([Review Notes](../REVIEW-NOTES.md#c-03--))

A worker first registers:

```
START
  ↓
REGISTER
  ↓
HEARTBEAT
  ↓
AVAILABLE
  ↓
CLAIM WORK
```

Registration record:

```JavaScript
{
    workerId: "worker-7",
    runtimeId: "runtime-1",
    contextType: "browser-tab",

    capabilities: [
        "network.http",
        "network.get",
        "text-response"
    ],

    status: "active",

    registeredAt: 1778500000000,
    lastHeartbeatAt: 1778500005000
}
```

This allows the frontier to know not merely:

```
"something wants work"
```

but:

```
"which execution context with which capabilities wants work?"
```

---

<!-- CAP-1083 | Continue Architecture Planning.md L89251–89300 | turn 81 | version 0.33 -->
## v0.33 — 33.3 Worker capabilities

> **Source sections:** `CAP-1083`
>
> [DOCUMENTATION REVIEW] Contradiction **C-03** ([Review Notes](../REVIEW-NOTES.md#c-03--))

v0.8 introduced capabilities at the acquisition layer.

v0.33 extends the idea to workers.

```
Worker
 │
 ├── network.http
 ├── network.get
 ├── binary-response
 ├── wasm.execute
 └── browser.dom
```

A work item can therefore require:

```JavaScript
{
    requiredCapabilities: [
        "network.http",
        "binary-response"
    ]
}
```

Worker eligibility becomes:

```
Work Requirements
       │
       ▼
Worker Capabilities
       │
       ▼
Capability Match
```

But:

```
capability match
≠
authorization
```

Policy still applies.

---

<!-- CAP-1084 | Continue Architecture Planning.md L89302–89332 | turn 81 | version 0.33 -->
## v0.33 — 33.4 Claiming is the synchronization boundary

> **Source sections:** `CAP-1084`
>
> [DOCUMENTATION REVIEW] Contradiction **C-03** ([Review Notes](../REVIEW-NOTES.md#c-03--))

The critical race remains:

```
Worker A reads work-42
Worker B reads work-42

A → claim
B → claim
```

The authoritative transition must be atomic:

```
QUEUED
   │
   ├── Worker A ──► CLAIMED
   │
   └── Worker B ──► rejected
```

The second worker must not receive:

```
"claim succeeded"
```

even if it observed the item immediately before Worker A.

---

<!-- CAP-1085 | Continue Architecture Planning.md L89334–89379 | turn 81 | version 0.33 -->
## v0.33 — 33.5 ClaimToken

> **Source sections:** `CAP-1085`
>
> [DOCUMENTATION REVIEW] Contradiction **C-03** ([Review Notes](../REVIEW-NOTES.md#c-03--))

A claim needs its own identity.

```JavaScript
class ClaimToken {
    constructor(data = {}) {
        this.id =
            data.id || makeId('claim');

        this.workItemId =
            data.workItemId || null;

        this.workerId =
            data.workerId || null;

        this.epoch =
            data.epoch ?? 0;

        this.claimedAt =
            data.claimedAt || now();

        this.expiresAt =
            data.expiresAt || null;

        this.status =
            data.status || 'active';
    }

    serialize() {
        return { ...this };
    }
}
```

Now:

```
WorkItem
   │
   └── ClaimToken
          │
          └── WorkerIdentity
```

---

<!-- CAP-1086 | Continue Architecture Planning.md L89381–89405 | turn 81 | version 0.33 -->
## v0.33 — 33.6 Claim ≠ lease

> **Source sections:** `CAP-1086`
>
> [DOCUMENTATION REVIEW] Contradiction **C-03** ([Review Notes](../REVIEW-NOTES.md#c-03--))

A claim says:

> Worker X owns this work.

A lease says:

> Worker X owns this work **until time T**, subject to renewal.

Therefore:

```
CLAIM
  +
EXPIRATION
  +
RENEWAL
=
LEASE
```

This is essential for crash recovery.

---

<!-- CAP-1087 | Continue Architecture Planning.md L89407–89427 | turn 81 | version 0.33 -->
## v0.33 — 33.7 Lease lifecycle

> **Source sections:** `CAP-1087`
>
> [DOCUMENTATION REVIEW] Contradiction **C-03** ([Review Notes](../REVIEW-NOTES.md#c-03--))

```
QUEUED
   ↓
CLAIMED
   ↓
LEASE ACTIVE
   │
   ├── heartbeat ──► renewed
   │
   └── expiration
            ↓
        RECOVERABLE
            ↓
          QUEUED
```

The worker cannot simply retain ownership forever.

---

<!-- CAP-1088 | Continue Architecture Planning.md L89429–89462 | turn 81 | version 0.33 -->
## v0.33 — 33.8 LeaseManager

> **Source sections:** `CAP-1088`
>
> [DOCUMENTATION REVIEW] Contradiction **C-03** ([Review Notes](../REVIEW-NOTES.md#c-03--))

```JavaScript
class LeaseManager {
    constructor(data = {}) {
        this.durationMs =
            data.durationMs ?? 30000;

        this.renewalMarginMs =
            data.renewalMarginMs ?? 10000;
    }

    create(workItemId, workerId) {
        const nowMs = Date.now();

        return new ClaimToken({
            workItemId,
            workerId,
            claimedAt: nowMs,
            expiresAt:
                nowMs + this.durationMs
        });
    }

    isExpired(claim, nowMs = Date.now()) {
        return (
            claim.expiresAt !== null &&
            nowMs >= claim.expiresAt
        );
    }
}
```

---

<!-- CAP-1089 | Continue Architecture Planning.md L89464–89486 | turn 81 | version 0.33 -->
## v0.33 — 33.9 Heartbeats

> **Source sections:** `CAP-1089`

A worker periodically renews its lease:

```
Worker
  │
  ├── heartbeat
  │
  ├── heartbeat
  │
  ├── heartbeat
  │
  └── heartbeat
```

But heartbeat itself needs a durable authority.

A stale worker must not be able to renew an already-reassigned work item.

That leads to **fencing**.

---

<!-- CAP-1090 | Continue Architecture Planning.md L89488–89525 | turn 81 | version 0.33 -->
## v0.33 — 33.10 Fencing tokens

> **Source sections:** `CAP-1090`
>
> [DOCUMENTATION REVIEW] Contradiction **C-03** ([Review Notes](../REVIEW-NOTES.md#c-03--))

Suppose:

```
Worker A
lease epoch = 4
```

The lease expires.

Recovery assigns the work to Worker B:

```
Worker B
lease epoch = 5
```

Worker A wakes up and continues.

Without fencing:

```
A → write result
B → write result
```

Now both workers believe they own the work.

The solution:

```
lease epoch
```

Every ownership generation receives a monotonically increasing epoch.

---

<!-- CAP-1092 | Continue Architecture Planning.md L89556–89591 | turn 81 | version 0.33 -->
## v0.33 — 33.12 Worker death

> **Source sections:** `CAP-1092`
>
> [DOCUMENTATION REVIEW] Contradiction **C-03** ([Review Notes](../REVIEW-NOTES.md#c-03--))

Suppose:

```
Worker A
   │
   ├── claim work-42
   ├── execute
   X
 crash
```

After lease expiration:

```
Recovery
   ↓
lease expired
   ↓
epoch++
   ↓
work requeued
```

Then:

```
Worker B
   ↓
claim epoch 5
```

Worker A's epoch 4 operations are rejected.

---

<!-- CAP-1093 | Continue Architecture Planning.md L89593–89621 | turn 81 | version 0.33 -->
## v0.33 — 33.13 Duplicate execution

> **Source sections:** `CAP-1093`

Fencing prevents concurrent ownership corruption, but duplicates can still occur.

For example:

```
Worker A sends HTTP request
server receives it
Worker A crashes before durable completion
```

Recovery:

```
Worker B retries request
```

The server may receive the request twice.

Therefore:

> **Exactly-once local claiming does not imply exactly-once external effects.**

This is especially important for GET discovery, but becomes critical if future providers support mutations.

The current policy of GET-only acquisition reduces the danger substantially.

---

<!-- CAP-1094 | Continue Architecture Planning.md L89623–89655 | turn 81 | version 0.33 -->
## v0.33 — 33.14 Execution identity

> **Source sections:** `CAP-1094`
>
> [DOCUMENTATION REVIEW] Contradiction **C-04** ([Review Notes](../REVIEW-NOTES.md#c-04--))

Every execution attempt should retain:

```
WorkItem
   │
   ├── Attempt 1
   │
   ├── Attempt 2
   │
   └── Attempt 3
```

Worker identity belongs to the attempt:

```JavaScript
{
    attemptId: "attempt-3",

    workItemId: "work-42",

    workerId: "worker-B",

    claimId: "claim-9",

    epoch: 5
}
```

This makes execution history explicit.

---

<!-- CAP-1096 | Continue Architecture Planning.md L89698–89728 | turn 81 | version 0.33 -->
## v0.33 — 33.16 Duplicate execution ≠ independent evidence

> **Source sections:** `CAP-1096`

This is subtle.

Two workers observing the same URL does not automatically mean:

```
independent confirmation = 2
```

If both use:

```
same origin
same endpoint
same acquisition provider
same artifact
same method
```

they may provide little additional epistemic independence.

Therefore:

```
execution count
≠
evidence independence
```

---

<!-- CAP-1097 | Continue Architecture Planning.md L89730–89765 | turn 81 | version 0.33 -->
## v0.33 — 33.17 Worker-local vs shared state

> **Source sections:** `CAP-1097`
>
> [DOCUMENTATION REVIEW] Contradiction **C-03** ([Review Notes](../REVIEW-NOTES.md#c-03--))

Workers should not each maintain authoritative versions of:

```
candidate status
budget
resource identity
coverage
claim ownership
```

Instead:

```
Worker-local
├── temporary buffers
├── provider instances
├── timers
├── execution context
└── ephemeral metrics

Shared durable state
├── WorkItems
├── Claims
├── Reservations
├── Candidates
├── Observations
├── Evidence
├── Budgets
└── Ledger
```

This prevents divergent truths.

---

<!-- CAP-1098 | Continue Architecture Planning.md L89767–89801 | turn 81 | version 0.33 -->
## v0.33 — 33.18 CoordinationManager

> **Source sections:** `CAP-1098`
>
> [DOCUMENTATION REVIEW] Contradiction **C-03** ([Review Notes](../REVIEW-NOTES.md#c-03--))

```JavaScript
class CoordinationManager {
    async registerWorker(worker) {
        throw new Error('Not implemented');
    }

    async heartbeat(workerId) {
        throw new Error('Not implemented');
    }

    async claim(workItemId, workerId) {
        throw new Error('Not implemented');
    }

    async renew(claimId, workerId) {
        throw new Error('Not implemented');
    }

    async release(claimId, workerId) {
        throw new Error('Not implemented');
    }

    async recoverExpiredClaims(context) {
        throw new Error('Not implemented');
    }
}
```

The manager coordinates.

It does not become a second scheduler.

---

<!-- CAP-1099 | Continue Architecture Planning.md L89803–89827 | turn 81 | version 0.33 -->
## v0.33 — 33.19 Coordination vs arbitration

> **Source sections:** `CAP-1099`
>
> [DOCUMENTATION REVIEW] Contradiction **C-03** ([Review Notes](../REVIEW-NOTES.md#c-03--))

This distinction must remain explicit.

```
Arbitrator
    ↓
"work-42 should execute"

Coordinator
    ↓
"worker-B successfully owns work-42"
```

Therefore:

```
ARBITRATION
≠
OWNERSHIP
```

A worker can lose the race after arbitration.

---

<!-- CAP-1100 | Continue Architecture Planning.md L89829–89869 | turn 81 | version 0.33 -->
## v0.33 — 33.20 Worker selection

> **Source sections:** `CAP-1100`
>
> [DOCUMENTATION REVIEW] Contradiction **C-03** ([Review Notes](../REVIEW-NOTES.md#c-03--))

Worker suitability can become an additional eligibility dimension.

```
Work
 │
 ├── required capabilities
 ├── resource requirements
 ├── affinity
 └── constraints
       │
       ▼
Worker pool
       │
       ▼
eligible workers
```

Examples of affinity:

```
browser DOM work
    → browser worker

WASM execution
    → WASM-capable worker

privileged acquisition
    → privileged provider worker
```

But again:

```
worker capability
≠
authorization
```

---

<!-- CAP-1101 | Continue Architecture Planning.md L89871–89890 | turn 81 | version 0.33 -->
## v0.33 — 33.21 Worker affinity

> **Source sections:** `CAP-1101`
>
> [DOCUMENTATION REVIEW] Contradiction **C-03** ([Review Notes](../REVIEW-NOTES.md#c-03--))

Affinity can improve efficiency:

```JavaScript
{
    preferredWorkerContext:
        "browser-tab",

    requiredCapabilities: [
        "browser.dom"
    ]
}
```

However, affinity should generally be a **soft preference** unless the operation genuinely cannot execute elsewhere.

Otherwise an unavailable preferred worker can cause starvation.

---

<!-- CAP-1102 | Continue Architecture Planning.md L89892–89919 | turn 81 | version 0.33 -->
## v0.33 — 33.22 Worker capacity

> **Source sections:** `CAP-1102`
>
> [DOCUMENTATION REVIEW] Contradiction **C-03** ([Review Notes](../REVIEW-NOTES.md#c-03--))

Workers can advertise capacity:

```JavaScript
{
    workerId: "worker-A",

    capacity: {
        maxConcurrent: 2,
        current: 1
    }
}
```

Then:

```
Worker A
capacity 2
current 2
      ↓
not eligible for more work
```

This is another resource constraint.

---

<!-- CAP-1103 | Continue Architecture Planning.md L89921–89953 | turn 81 | version 0.33 -->
## v0.33 — 33.23 Distributed accounting

> **Source sections:** `CAP-1103`

Multiple workers make v0.31's resource ledger more important.

```
Worker A ──┐
Worker B ──┼──► Resource Ledger
Worker C ──┘
```

Reservations must be globally visible.

Otherwise:

```
Global budget = 10

Worker A sees 10
Worker B sees 10
Worker C sees 10
```

Each can reserve ten.

The actual total becomes:

```
30 > 10
```

So reservation authority must be shared.

---

<!-- CAP-1104 | Continue Architecture Planning.md L89955–89977 | turn 81 | version 0.33 -->
## v0.33 — 33.24 Worker-local caches

> **Source sections:** `CAP-1104`
>
> [DOCUMENTATION REVIEW] Contradiction **C-03** ([Review Notes](../REVIEW-NOTES.md#c-03--))

Caching is allowed, but only as an optimization.

```
AUTHORITATIVE STATE
       │
       ▼
Worker cache
```

The cache may become stale.

Therefore:

```
cache says QUEUED
authoritative state says CLAIMED
```

The authoritative state wins.

---

<!-- CAP-1105 | Continue Architecture Planning.md L89979–90012 | turn 81 | version 0.33 -->
## v0.33 — 33.25 Cross-worker event ordering

> **Source sections:** `CAP-1105`
>
> [DOCUMENTATION REVIEW] Contradiction **C-03** ([Review Notes](../REVIEW-NOTES.md#c-03--))

Distributed workers produce events concurrently:

```
Worker A: event 100
Worker B: event 101
Worker C: event 102
```

Local timestamps cannot reliably establish causal order.

Therefore distinguish:

```
wall-clock timestamp
≠
causal ordering
```

The event ledger can use:

```
sequence
transactionId
workerId
attemptId
claimId
parentEventId
```

where appropriate.

---

<!-- CAP-1106 | Continue Architecture Planning.md L90014–90030 | turn 81 | version 0.33 -->
## v0.33 — 33.26 Causal provenance

> **Source sections:** `CAP-1106`

Example:

```
candidate-created
       │
       └── caused by
             discovery-emitted
                  │
                  └── caused by
                       observation-recorded
```

A worker ID adds execution provenance but does not itself establish causality.

---

<!-- CAP-1107 | Continue Architecture Planning.md L90032–90060 | turn 81 | version 0.33 -->
## v0.33 — 33.27 Coordination events

> **Source sections:** `CAP-1107`
>
> [DOCUMENTATION REVIEW] Contradiction **C-03** ([Review Notes](../REVIEW-NOTES.md#c-03--))

Add:

```
worker-registered
worker-heartbeat
worker-expired
worker-capabilities-updated

claim-requested
claim-granted
claim-rejected
claim-renewed
claim-released
claim-expired
claim-fenced

worker-capacity-updated
worker-task-started
worker-task-finished

duplicate-execution-detected
stale-worker-operation-rejected
```

These become part of the event ledger.

---

<!-- CAP-1109 | Continue Architecture Planning.md L90085–90111 | turn 81 | version 0.33 -->
## v0.33 — 33.29 Split-brain

> **Source sections:** `CAP-1109`
>
> [DOCUMENTATION REVIEW] Contradiction **C-03** ([Review Notes](../REVIEW-NOTES.md#c-03--))

A particularly dangerous failure:

```
Worker A                    Worker B
   │                           │
   │ "I own work-42"           │
   │                           │
   │                    "I own work-42"
```

The solution is not merely heartbeat.

It requires a single authoritative ownership mechanism:

```
             AUTHORITY
                 │
        ┌────────┴────────┐
        ▼                 ▼
     Worker A          Worker B
```

For the userscript prototype, IndexedDB transaction semantics can provide local coordination across supported contexts, but true cross-device coordination requires a shared authority.

---

<!-- CAP-1111 | Continue Architecture Planning.md L90154–90178 | turn 81 | version 0.33 -->
## v0.33 — 33.31 Coordination scope

> **Source sections:** `CAP-1111`
>
> [DOCUMENTATION REVIEW] Contradiction **C-03** ([Review Notes](../REVIEW-NOTES.md#c-03--))

Therefore explicitly define:

```JavaScript
{
    coordinationScope:
        "browser-profile"
}
```

Possible scopes:

```
LOCAL_WORKER
BROWSER_TAB_GROUP
BROWSER_PROFILE
DEVICE
NETWORK
CLUSTER
```

Claims must never silently imply a wider scope than the coordination mechanism actually supports.

---

<!-- CAP-1115 | Continue Architecture Planning.md L90276–90349 | turn 81 | version 0.33 -->
## v0.33 — 33.35 v0.33 result

> **Source sections:** `CAP-1115`

The architecture has now evolved from:

```
single queue
```

to:

```
durable shared frontier
        +
arbitration
        +
resource allocation
        +
worker coordination
        +
lease-based ownership
        +
fencing
        +
recovery
```

The resulting execution model is:

```
                    GOAL
                     │
                     ▼
                SEARCH PLAN
                     │
                     ▼
               SEARCH SPACE
                     │
                     ▼
                 FRONTIER
                     │
                     ▼
               ADMISSION
                     │
                     ▼
               ARBITRATION
                     │
                     ▼
                ALLOCATION
                     │
                     ▼
             WORKER SELECTION
                     │
                     ▼
              CLAIM + LEASE
                     │
                     ▼
                 EXECUTION
                     │
                     ▼
                OBSERVATION
                     │
                     ▼
             DURABLE COMMIT
                     │
            ┌────────┼────────┐
            ▼        ▼        ▼
        KNOWLEDGE  COST    PROVENANCE
            │        │        │
            └────────┼────────┘
                     ▼
                  FRONTIER
```

---
