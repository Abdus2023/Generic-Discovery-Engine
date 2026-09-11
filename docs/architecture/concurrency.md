# Concurrency

> **Status:** DESIGNED
>
> **Source:** `Continue Architecture Planning.md`; `Userscript Discovery Prototype.md`
>
> **Purpose:** Concurrency: worker ownership, claiming, leases, fencing, heartbeats and concurrent execution.

## Contents

- **What changed — 1. Concurrent claiming is now explicit** — `Userscript Discovery Prototype.md` L4713–4756
- **v0.13 — 15. Concurrent source execution** — `Continue Architecture Planning.md` L60119–60166
- **v0.14 — 16. Lease-based claims** — `Continue Architecture Planning.md` L61415–61461
- **v0.15 — 7. Claiming becomes a formal protocol** — `Continue Architecture Planning.md` L62349–62425
- **v0.15 — 8. Work lease** — `Continue Architecture Planning.md` L62427–62458
- **v0.15 — 9. Lease recovery** — `Continue Architecture Planning.md` L62460–62490
- **v0.33 — Multi-Worker / Multi-Context Coordination** — `Continue Architecture Planning.md` L89042–89108
- **v0.33 — Multi-Worker Coordination & Distributed Claiming** — `Continue Architecture Planning.md` L89120–89144
- **v0.33 — 33.1 Worker identity** — `Continue Architecture Planning.md` L89146–89198
- **v0.33 — 33.2 Worker registration** — `Continue Architecture Planning.md` L89200–89249
- **v0.33 — 33.3 Worker capabilities** — `Continue Architecture Planning.md` L89251–89300
- **v0.33 — 33.4 Claiming is the synchronization boundary** — `Continue Architecture Planning.md` L89302–89332
- **v0.33 — 33.5 ClaimToken** — `Continue Architecture Planning.md` L89334–89379
- **v0.33 — 33.6 Claim ≠ lease** — `Continue Architecture Planning.md` L89381–89405
- **v0.33 — 33.7 Lease lifecycle** — `Continue Architecture Planning.md` L89407–89427
- **v0.33 — 33.8 LeaseManager** — `Continue Architecture Planning.md` L89429–89462
- **v0.33 — 33.9 Heartbeats** — `Continue Architecture Planning.md` L89464–89486
- **v0.33 — 33.10 Fencing tokens** — `Continue Architecture Planning.md` L89488–89525
- **v0.33 — 33.12 Worker death** — `Continue Architecture Planning.md` L89556–89591
- **v0.33 — 33.13 Duplicate execution** — `Continue Architecture Planning.md` L89593–89621
- **v0.33 — 33.14 Execution identity** — `Continue Architecture Planning.md` L89623–89655
- **v0.33 — 33.16 Duplicate execution ≠ independent evidence** — `Continue Architecture Planning.md` L89698–89728
- **v0.33 — 33.17 Worker-local vs shared state** — `Continue Architecture Planning.md` L89730–89765
- **v0.33 — 33.18 CoordinationManager** — `Continue Architecture Planning.md` L89767–89801
- **v0.33 — 33.19 Coordination vs arbitration** — `Continue Architecture Planning.md` L89803–89827
- **v0.33 — 33.20 Worker selection** — `Continue Architecture Planning.md` L89829–89869
- **v0.33 — 33.21 Worker affinity** — `Continue Architecture Planning.md` L89871–89890
- **v0.33 — 33.22 Worker capacity** — `Continue Architecture Planning.md` L89892–89919
- **v0.33 — 33.23 Distributed accounting** — `Continue Architecture Planning.md` L89921–89953
- **v0.33 — 33.24 Worker-local caches** — `Continue Architecture Planning.md` L89955–89977
- **v0.33 — 33.25 Cross-worker event ordering** — `Continue Architecture Planning.md` L89979–90012
- **v0.33 — 33.26 Causal provenance** — `Continue Architecture Planning.md` L90014–90030
- **v0.33 — 33.27 Coordination events** — `Continue Architecture Planning.md` L90032–90060
- **v0.33 — 33.29 Split-brain** — `Continue Architecture Planning.md` L90085–90111
- **v0.33 — 33.31 Coordination scope** — `Continue Architecture Planning.md` L90154–90178
- **v0.33 — 33.35 v0.33 result** — `Continue Architecture Planning.md` L90276–90349

## Related Documents

- [Scheduling](scheduler.md)
- [Work Items and Frontier Arbitration](work-and-frontier.md)
- [Coordination, Consistency and Transport](coordination.md)
- [Userscript Development Narrative](../prototype/userscript.md)

---

<!-- source: Userscript Discovery Prototype.md L4713–4756 | turn 15 | version ? -->
### What changed — 1. Concurrent claiming is now explicit

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

<!-- source: Continue Architecture Planning.md L60119–60166 | turn 39 | version 0.13 -->
## v0.13 — 15. Concurrent source execution

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

<!-- source: Continue Architecture Planning.md L61415–61461 | turn 41 | version 0.14 -->
## v0.14 — 16. Lease-based claims

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

<!-- source: Continue Architecture Planning.md L62349–62425 | turn 43 | version 0.15 -->
## v0.15 — 7. Claiming becomes a formal protocol

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

<!-- source: Continue Architecture Planning.md L62427–62458 | turn 43 | version 0.15 -->
## v0.15 — 8. Work lease

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

<!-- source: Continue Architecture Planning.md L62460–62490 | turn 43 | version 0.15 -->
## v0.15 — 9. Lease recovery

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

<!-- source: Continue Architecture Planning.md L89042–89108 | turn 79 | version 0.33 -->
## v0.33 — Multi-Worker / Multi-Context Coordination

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

<!-- source: Continue Architecture Planning.md L89120–89144 | turn 81 | version 0.33 -->
## v0.33 — Multi-Worker Coordination & Distributed Claiming

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

<!-- source: Continue Architecture Planning.md L89146–89198 | turn 81 | version 0.33 -->
## v0.33 — 33.1 Worker identity

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

<!-- source: Continue Architecture Planning.md L89200–89249 | turn 81 | version 0.33 -->
## v0.33 — 33.2 Worker registration

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

<!-- source: Continue Architecture Planning.md L89251–89300 | turn 81 | version 0.33 -->
## v0.33 — 33.3 Worker capabilities

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

<!-- source: Continue Architecture Planning.md L89302–89332 | turn 81 | version 0.33 -->
## v0.33 — 33.4 Claiming is the synchronization boundary

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

<!-- source: Continue Architecture Planning.md L89334–89379 | turn 81 | version 0.33 -->
## v0.33 — 33.5 ClaimToken

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

<!-- source: Continue Architecture Planning.md L89381–89405 | turn 81 | version 0.33 -->
## v0.33 — 33.6 Claim ≠ lease

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

<!-- source: Continue Architecture Planning.md L89407–89427 | turn 81 | version 0.33 -->
## v0.33 — 33.7 Lease lifecycle

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

<!-- source: Continue Architecture Planning.md L89429–89462 | turn 81 | version 0.33 -->
## v0.33 — 33.8 LeaseManager

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

<!-- source: Continue Architecture Planning.md L89464–89486 | turn 81 | version 0.33 -->
## v0.33 — 33.9 Heartbeats

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

<!-- source: Continue Architecture Planning.md L89488–89525 | turn 81 | version 0.33 -->
## v0.33 — 33.10 Fencing tokens

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

<!-- source: Continue Architecture Planning.md L89556–89591 | turn 81 | version 0.33 -->
## v0.33 — 33.12 Worker death

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

<!-- source: Continue Architecture Planning.md L89593–89621 | turn 81 | version 0.33 -->
## v0.33 — 33.13 Duplicate execution

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

<!-- source: Continue Architecture Planning.md L89623–89655 | turn 81 | version 0.33 -->
## v0.33 — 33.14 Execution identity

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

<!-- source: Continue Architecture Planning.md L89698–89728 | turn 81 | version 0.33 -->
## v0.33 — 33.16 Duplicate execution ≠ independent evidence

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

<!-- source: Continue Architecture Planning.md L89730–89765 | turn 81 | version 0.33 -->
## v0.33 — 33.17 Worker-local vs shared state

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

<!-- source: Continue Architecture Planning.md L89767–89801 | turn 81 | version 0.33 -->
## v0.33 — 33.18 CoordinationManager

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

<!-- source: Continue Architecture Planning.md L89803–89827 | turn 81 | version 0.33 -->
## v0.33 — 33.19 Coordination vs arbitration

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

<!-- source: Continue Architecture Planning.md L89829–89869 | turn 81 | version 0.33 -->
## v0.33 — 33.20 Worker selection

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

<!-- source: Continue Architecture Planning.md L89871–89890 | turn 81 | version 0.33 -->
## v0.33 — 33.21 Worker affinity

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

<!-- source: Continue Architecture Planning.md L89892–89919 | turn 81 | version 0.33 -->
## v0.33 — 33.22 Worker capacity

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

<!-- source: Continue Architecture Planning.md L89921–89953 | turn 81 | version 0.33 -->
## v0.33 — 33.23 Distributed accounting

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

<!-- source: Continue Architecture Planning.md L89955–89977 | turn 81 | version 0.33 -->
## v0.33 — 33.24 Worker-local caches

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

<!-- source: Continue Architecture Planning.md L89979–90012 | turn 81 | version 0.33 -->
## v0.33 — 33.25 Cross-worker event ordering

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

<!-- source: Continue Architecture Planning.md L90014–90030 | turn 81 | version 0.33 -->
## v0.33 — 33.26 Causal provenance

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

<!-- source: Continue Architecture Planning.md L90032–90060 | turn 81 | version 0.33 -->
## v0.33 — 33.27 Coordination events

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

<!-- source: Continue Architecture Planning.md L90085–90111 | turn 81 | version 0.33 -->
## v0.33 — 33.29 Split-brain

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

<!-- source: Continue Architecture Planning.md L90154–90178 | turn 81 | version 0.33 -->
## v0.33 — 33.31 Coordination scope

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

<!-- source: Continue Architecture Planning.md L90276–90349 | turn 81 | version 0.33 -->
## v0.33 — 33.35 v0.33 result

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
