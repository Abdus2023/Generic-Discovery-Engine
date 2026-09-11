# Persistence and Crash Recovery

> **Status:** DESIGNED
>
> **Source:** `Continue Architecture Planning.md`; `Userscript Discovery Prototype.md`
>
> **Purpose:** Durable state, transactions, write-ahead ledgers, checkpoints, idempotency and recovery.

## Contents

- **20. Cache knowledge between scans** — `Userscript Discovery Prototype.md` L951–991
- **v0.32 boundary** — `Continue Architecture Planning.md` L87703–87765
- **v0.32 — Transactional Persistence & Crash Recovery** — `Continue Architecture Planning.md` L87777–87789
- **v0.32 — 32.1 The crash problem** — `Continue Architecture Planning.md` L87791–87828
- **v0.32 — 32.2 Durable state vs runtime state** — `Continue Architecture Planning.md` L87830–87856
- **v0.32 — 32.3 Persistence is not serialization** — `Continue Architecture Planning.md` L87858–87893
- **v0.32 — 32.4 PersistenceAdapter** — `Continue Architecture Planning.md` L87895–87940
- **v0.32 — 32.5 Transaction** — `Continue Architecture Planning.md` L87942–87990
- **v0.32 — 32.6 Write-ahead event ledger** — `Continue Architecture Planning.md` L87992–88035
- **v0.32 — 32.7 Event identity** — `Continue Architecture Planning.md` L88037–88073
- **v0.32 — 32.8 Monotonic sequence** — `Continue Architecture Planning.md` L88075–88106
- **v0.32 — 32.9 Commit protocol** — `Continue Architecture Planning.md` L88108–88145
- **v0.32 — 32.10 Commit markers** — `Continue Architecture Planning.md` L88147–88170
- **v0.32 — 32.11 Checkpoint correctness** — `Continue Architecture Planning.md` L88172–88211
- **v0.32 — 32.12 At-least-once vs exactly-once** — `Continue Architecture Planning.md` L88213–88245
- **v0.32 — 32.13 Idempotency** — `Continue Architecture Planning.md` L88247–88282
- **v0.32 — 32.14 Work recovery** — `Continue Architecture Planning.md` L88284–88331
- **v0.32 — 32.15 Recovery scan** — `Continue Architecture Planning.md` L88333–88367
- **v0.32 — 32.16 RecoveryManager** — `Continue Architecture Planning.md` L88369–88404
- **v0.32 — 32.17 Reservation recovery** — `Continue Architecture Planning.md` L88406–88452
- **v0.32 — 32.20 Artifact durability** — `Continue Architecture Planning.md` L88501–88531
- **v0.32 — 32.21 Durable checkpoint** — `Continue Architecture Planning.md` L88533–88566
- **v0.32 — 32.23 Schema versioning** — `Continue Architecture Planning.md` L88591–88621
- **v0.32 — 32.24 Snapshot + journal** — `Continue Architecture Planning.md` L88623–88659
- **v0.32 — 32.25 Snapshot integrity** — `Continue Architecture Planning.md` L88661–88686
- **v0.32 — 32.26 Recovery outcomes** — `Continue Architecture Planning.md` L88688–88731
- **v0.32 — 32.27 Recovery must not fabricate knowledge** — `Continue Architecture Planning.md` L88733–88753
- **v0.32 — 32.28 Crash-safe frontier** — `Continue Architecture Planning.md` L88755–88778
- **v0.32 — 32.29 Reconciliation** — `Continue Architecture Planning.md` L88780–88822
- **v0.32 — 32.30 Repair is itself provenance** — `Continue Architecture Planning.md` L88824–88844
- **v0.32 — 32.32 Complete lifecycle** — `Continue Architecture Planning.md` L88897–88933
- **v0.32 — 32.35 What v0.32 changes** — `Continue Architecture Planning.md` L89010–89040

## Related Documents

- [System Model](system-model.md)
- [Coordination, Consistency and Transport](coordination.md)
- [Provenance](provenance.md)
- [Invariants](../validation/invariants.md)

---

<!-- source: Userscript Discovery Prototype.md L951–991 | turn 7 | version ? -->
## 20. Cache knowledge between scans

A major optimization is to persist previous observations.

Suppose yesterday the scanner found:

```
frequency X → DVB-T2 multiplex
frequency Y → empty
frequency Z → DVB-T multiplex
```

On the next scan, you don't need to treat the entire spectrum as equally unknown.

Maintain a knowledge store:

```
ObservationHistory {
    candidate
    result
    timestamp
    signal_quality
    stability
}
```

Then the next scan becomes:

```
known-good candidates
        ↓
known-neighbor candidates
        ↓
new/changed spectrum
        ↓
full blind search
```

This produces a **continuous discovery system**, rather than repeatedly performing the same expensive blind scan.

---

<!-- source: Continue Architecture Planning.md L87703–87765 | turn 77 | version 0.32 -->
## v0.32 boundary

The next unresolved problem is now **not execution capacity**.

It is **state durability and recovery**.

We have:

```
WorkItem
Reservation
Checkpoint
Cursor
Observation
Artifact
Evidence
Search-space snapshot
Coverage
Cost ledger
```

All of these can become inconsistent if the browser tab crashes between operations.

For example:

```
1. reservation created
2. request starts
3. browser crashes
4. reservation remains
5. work remains CLAIMED
6. cursor may or may not have advanced
7. observation may or may not be persisted
```

Therefore the next boundary is naturally:

```
# v0.32 — Transactional Persistence & Crash Recovery

                    WORK
                      │
                      ▼
                  RESERVATION
                      │
                      ▼
                   EXECUTION
                      │
             ┌────────┴────────┐
             ▼                 ▼
          COMMIT             CRASH
             │                 │
             ▼                 ▼
         DURABLE STATE     RECOVERY
                               │
                    ┌──────────┼──────────┐
                    ▼          ▼          ▼
                 replay      retry      abandon
```

That is where the prototype begins confronting the hardest practical property of a real discovery engine:

> **Never silently lose discovered knowledge, silently double-account resources, or falsely advance the search frontier after a crash.**

<!-- source: Continue Architecture Planning.md L87777–87789 | turn 79 | version 0.32 -->
## v0.32 — Transactional Persistence & Crash Recovery

v0.31 established resource accounting.

The next failure mode is **durability**.

The engine now has enough state that a browser crash, tab suspension, userscript reload, quota failure, or partial write can leave the search state inconsistent.

The central question becomes:

> **How can the engine recover without silently losing knowledge, duplicating work, corrupting accounting, or falsely advancing the frontier?**

---

<!-- source: Continue Architecture Planning.md L87791–87828 | turn 79 | version 0.32 -->
## v0.32 — 32.1 The crash problem

Consider:

```
WorkItem
   ↓
Reservation
   ↓
Request started
   ↓
Observation produced
   ↓
Candidate discoveries produced
   ↓
Checkpoint
```

A crash can happen at every arrow.

For example:

```
REQUEST STARTED
      │
      X browser crashes
      │
      ▼
Was the request consumed?
Was the observation persisted?
Was the reservation settled?
Was the work completed?
Was the cursor advanced?
```

The engine cannot simply reconstruct the answer from the current in-memory state.

---

<!-- source: Continue Architecture Planning.md L87830–87856 | turn 79 | version 0.32 -->
## v0.32 — 32.2 Durable state vs runtime state

We now explicitly divide state:

```
                    ENGINE STATE
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
         DURABLE                  EPHEMERAL
             │                       │
             ├── candidates          ├── workers
             ├── observations        ├── timers
             ├── evidence            ├── promises
             ├── artifacts            ├── sockets
             ├── checkpoints          ├── DOM handles
             ├── work state           └── provider objects
             ├── reservations
             ├── settlements
             └── event ledger
```

The rule:

> **Ephemeral state may be reconstructed; durable knowledge must not depend on it.**

---

<!-- source: Continue Architecture Planning.md L87858–87893 | turn 79 | version 0.32 -->
## v0.32 — 32.3 Persistence is not serialization

A common mistake is:

```JavaScript
localStorage.setItem(
    'state',
    JSON.stringify(engine)
);
```

That is not transactional persistence.

It does not guarantee:

* atomic multi-object updates
* ordering
* crash consistency
* version compatibility
* recovery semantics
* duplicate detection
* partial-write handling

Instead, persistence becomes its own subsystem.

```
Runtime State
     ↓
Persistence Boundary
     ↓
Durable Transaction
     ↓
Storage
```

---

<!-- source: Continue Architecture Planning.md L87895–87940 | turn 79 | version 0.32 -->
## v0.32 — 32.4 PersistenceAdapter

```JavaScript
class PersistenceAdapter {
    async begin() {
        throw new Error('Not implemented');
    }

    async commit(transaction) {
        throw new Error('Not implemented');
    }

    async rollback(transaction) {
        throw new Error('Not implemented');
    }

    async read(key) {
        throw new Error('Not implemented');
    }

    async scan(prefix) {
        throw new Error('Not implemented');
    }

    describe() {
        return {
            id: 'unknown-persistence',
            name: 'Unknown Persistence Adapter'
        };
    }
}
```

The core runtime should not care whether persistence is:

```
IndexedDB
Dexie
SQLite
file-backed storage
remote durable store
```

The contract is what matters.

---

<!-- source: Continue Architecture Planning.md L87942–87990 | turn 79 | version 0.32 -->
## v0.32 — 32.5 Transaction

```JavaScript
class PersistenceTransaction {
    constructor(data = {}) {
        this.id = data.id || makeId('tx');

        this.operations =
            data.operations || [];

        this.status =
            data.status || 'active';

        this.createdAt =
            data.createdAt || now();

        this.committedAt =
            data.committedAt || null;
    }

    add(operation) {
        this.operations.push(operation);
    }

    serialize() {
        return { ...this };
    }
}
```

The transaction represents a logical state transition.

For example:

```
Transaction T42

UPDATE WorkItem
UPDATE Reservation
INSERT Observation
INSERT Evidence
INSERT Candidate
UPDATE Checkpoint
APPEND Events
```

These changes should either become durable as one logical transition or be recoverable as an incomplete transaction.

---

<!-- source: Continue Architecture Planning.md L87992–88035 | turn 79 | version 0.32 -->
## v0.32 — 32.6 Write-ahead event ledger

The existing event ledger becomes especially important.

Instead of relying exclusively on final state:

```
STATE
```

we retain:

```
EVENT
EVENT
EVENT
EVENT
...
```

The architecture becomes:

```
                  EVENT
                    │
                    ▼
              DURABLE LOG
                    │
             ┌──────┴──────┐
             ▼             ▼
          STATE          REPLAY
```

This resembles a lightweight event-sourced model, but we should **not** require the entire engine to be purely event-sourced.

A useful hybrid is:

```
Event Ledger = authoritative history

Materialized State = efficient current view
```

---

<!-- source: Continue Architecture Planning.md L88037–88073 | turn 79 | version 0.32 -->
## v0.32 — 32.7 Event identity

Every durable event needs an immutable identity.

```JavaScript
{
    eventId: "evt-823",
    sequence: 1842,

    transactionId: "tx-91",

    type: "observation-recorded",

    aggregateType: "observation",
    aggregateId: "obs-42",

    payload: {},

    createdAt: 1778500000000
}
```

Important distinction:

```
eventId
≠
workItemId
≠
attemptId
≠
transactionId
```

One execution may generate many events.

---

<!-- source: Continue Architecture Planning.md L88075–88106 | turn 79 | version 0.32 -->
## v0.32 — 32.8 Monotonic sequence

A durable ledger benefits from a monotonic sequence:

```
1801
1802
1803
1804
1805
...
```

After recovery:

```
last durable sequence = 1805
```

If the engine sees:

```
1804
1805
1807
```

then it has detected a possible persistence gap.

That should not silently pass.

---

<!-- source: Continue Architecture Planning.md L88108–88145 | turn 79 | version 0.32 -->
## v0.32 — 32.9 Commit protocol

A simplified durable transition:

```
         BEGIN
           │
           ▼
      validate state
           │
           ▼
      append intent
           │
           ▼
      write objects
           │
           ▼
      append commit
           │
           ▼
         COMMIT
```

If a crash occurs before commit:

```
incomplete transaction
       ↓
recovery
       ↓
rollback / finish / reconcile
```

The exact mechanism depends on the storage backend.

The invariant is more important than the implementation.

---

<!-- source: Continue Architecture Planning.md L88147–88170 | turn 79 | version 0.32 -->
## v0.32 — 32.10 Commit markers

A transaction should have an explicit durable completion marker.

```
TX-42
│
├── operation 1
├── operation 2
├── operation 3
└── COMMIT
```

Recovery can then distinguish:

```
complete transaction
vs
incomplete transaction
```

Without this distinction, partially written state can look valid.

---

<!-- source: Continue Architecture Planning.md L88172–88211 | turn 79 | version 0.32 -->
## v0.32 — 32.11 Checkpoint correctness

v0.26 established:

```
discover
   ↓
persist discoveries
   ↓
persist candidates
   ↓
persist checkpoint
```

v0.32 strengthens that rule.

For enumeration:

```
PAGE N
  │
  ├── persist entries
  ├── persist candidates
  ├── persist evidence
  └── persist cursor N+1
```

Only after the page's knowledge is durable should the cursor advance.

Otherwise:

```
cursor → N+1
crash
knowledge from N lost
```

The engine would incorrectly believe page N had been processed.

---

<!-- source: Continue Architecture Planning.md L88213–88245 | turn 79 | version 0.32 -->
## v0.32 — 32.12 At-least-once vs exactly-once

Distributed-systems terminology is useful here.

The browser engine should generally prefer:

```
AT-LEAST-ONCE KNOWLEDGE PROCESSING
```

rather than attempting impossible global exactly-once external execution.

A crash may cause:

```
same page processed twice
same candidate proposed twice
same artifact observed twice
```

That is acceptable if identity reconciliation handles it.

The dangerous failure is:

```
page silently skipped
```

Therefore:

> **Duplicate work is preferable to silent knowledge loss.**

---

<!-- source: Continue Architecture Planning.md L88247–88282 | turn 79 | version 0.32 -->
## v0.32 — 32.13 Idempotency

This requires durable idempotency keys.

For example:

```JavaScript
{
    operation: 'enumeration-page',
    executionId: 'exec-42',
    sequence: 17
}
```

Identity:

```
(exec-42, page-17)
```

If the engine encounters it again:

```
already committed?
     │
   yes
     │
     ▼
do not duplicate durable effect
```

This does not require suppressing provenance.

The second observation attempt can still exist as a distinct event if it actually happened.

---

<!-- source: Continue Architecture Planning.md L88284–88331 | turn 79 | version 0.32 -->
## v0.32 — 32.14 Work recovery

A persisted work item might say:

```JavaScript
{
    id: "work-42",
    status: "claimed",
    claimedBy: "worker-7",
    leaseUntil: 1778500010000
}
```

After a crash, that worker does not exist.

Recovery evaluates:

```
lease expired?
   │
   ├── no → preserve
   │
   └── yes
         ↓
      requeue
```

Therefore:

```
CLAIMED + expired lease
        ↓
QUEUED
```

Not:

```
COMPLETED
```

and not:

```
FAILED
```

---

<!-- source: Continue Architecture Planning.md L88333–88367 | turn 79 | version 0.32 -->
## v0.32 — 32.15 Recovery scan

At startup:

```
LOAD DURABLE STATE
        │
        ▼
VALIDATE SCHEMA
        │
        ▼
CHECK TRANSACTION LOG
        │
        ▼
CHECK WORK LEASES
        │
        ▼
CHECK RESERVATIONS
        │
        ▼
CHECK CHECKPOINTS
        │
        ▼
RECONCILE STATE
        │
        ▼
RECOVERY COMPLETE
        │
        ▼
START FRONTIER
```

The engine should not immediately resume execution before reconciliation.

---

<!-- source: Continue Architecture Planning.md L88369–88404 | turn 79 | version 0.32 -->
## v0.32 — 32.16 RecoveryManager

```JavaScript
class RecoveryManager {
    async inspect(context) {
        return {
            transactions: [],
            expiredClaims: [],
            activeReservations: [],
            inconsistentCheckpoints: [],
            errors: []
        };
    }

    async recover(context) {
        throw new Error('Not implemented');
    }

    async validate(context) {
        return {
            valid: true,
            errors: [],
            warnings: []
        };
    }

    describe() {
        return {
            id: 'recovery-manager',
            name: 'Transactional Recovery Manager'
        };
    }
}
```

---

<!-- source: Continue Architecture Planning.md L88406–88452 | turn 79 | version 0.32 -->
## v0.32 — 32.17 Reservation recovery

Reservations are particularly dangerous.

Suppose:

```
reservation = 1 request

request started

browser crashed
```

Did the request happen?

The engine may not know.

Therefore avoid pretending:

```
request definitely happened
```

Instead represent uncertainty:

```JavaScript
{
    reservationId: "res-42",
    status: "recovery-uncertain",
    reason: "execution-interrupted"
}
```

Then the policy decides whether to:

```
reconcile
release
charge conservatively
retry
abandon
```

This is much safer than silently resetting the budget.

---

<!-- source: Continue Architecture Planning.md L88501–88531 | turn 79 | version 0.32 -->
## v0.32 — 32.20 Artifact durability

The artifact lifecycle should become:

```
ACQUIRED
   ↓
TEMPORARY
   ↓
HASHED
   ↓
PERSISTED
   ↓
DURABLE
```

A hash alone does not guarantee the bytes remain available.

Therefore:

```
artifact digest
+
storage status
+
storage location
```

must remain separate.

---

<!-- source: Continue Architecture Planning.md L88533–88566 | turn 79 | version 0.32 -->
## v0.32 — 32.21 Durable checkpoint

A checkpoint should contain enough information to reconstruct execution intent:

```JavaScript
{
    executionId: "exec-42",

    sequence: 17,

    cursor: "opaque-token",

    stats: {
        entries: 170,
        proposals: 94
    },

    strategyState: {},

    frontierWatermark: "evt-1830",

    createdAt: 1778500000000
}
```

The `frontierWatermark` is useful because it connects:

```
checkpoint
↔
durable event history
```

---

<!-- source: Continue Architecture Planning.md L88591–88621 | turn 79 | version 0.32 -->
## v0.32 — 32.23 Schema versioning

Persistent state will evolve.

Therefore every durable object needs a schema version:

```JavaScript
{
    schema: "work-item",
    version: 3,
    ...
}
```

Recovery then becomes:

```
stored v1
   ↓
migration
   ↓
v2
   ↓
migration
   ↓
v3
```

Never assume:

---

<!-- source: Continue Architecture Planning.md L88623–88659 | turn 79 | version 0.32 -->
## v0.32 — 32.24 Snapshot + journal

For a userscript, a practical persistence model is:

```
              EVENT JOURNAL
                   │
                   ▼
            MATERIALIZED STATE
                   │
                   ▼
               SNAPSHOT
```

Periodically:

```
events 1..1000
      ↓
snapshot
      ↓
events 1001..1030
```

Recovery:

```
latest snapshot
      +
events after snapshot
      ↓
current state
```

This avoids replaying the entire history every time.

---

<!-- source: Continue Architecture Planning.md L88661–88686 | turn 79 | version 0.32 -->
## v0.32 — 32.25 Snapshot integrity

Snapshots should themselves be verifiable.

```JavaScript
{
    snapshotId: "snap-42",

    sequence: 1830,

    schemaVersion: 5,

    stateDigest: {
        algorithm: "sha256",
        digest: "..."
    },

    createdAt: 1778500000000
}
```

The digest is not proof that the state is semantically correct.

It provides integrity against accidental corruption.

---

<!-- source: Continue Architecture Planning.md L88688–88731 | turn 79 | version 0.32 -->
## v0.32 — 32.26 Recovery outcomes

Recovery should produce an explicit result:

```JavaScript
{
    status: "recovered",

    resumedWork: [
        "work-42",
        "work-91"
    ],

    abandonedWork: [
        "work-17"
    ],

    replayedTransactions: [
        "tx-88"
    ],

    uncertainReservations: [
        "res-12"
    ],

    invalidCheckpoints: [],

    warnings: [
        "execution exec-9 ended without durable observation"
    ]
}
```

Possible session outcomes:

```
RECOVERED
RECOVERED_WITH_WARNINGS
RECOVERY_PARTIAL
RECOVERY_BLOCKED
RECOVERY_FAILED
```

---

<!-- source: Continue Architecture Planning.md L88733–88753 | turn 79 | version 0.32 -->
## v0.32 — 32.27 Recovery must not fabricate knowledge

This is fundamental.

If the engine cannot determine whether something happened:

```
UNKNOWN
```

is the correct answer.

Not:

and not:

This connects v0.32 directly to v0.23.

Crash uncertainty is another form of epistemic uncertainty.

---

<!-- source: Continue Architecture Planning.md L88755–88778 | turn 79 | version 0.32 -->
## v0.32 — 32.28 Crash-safe frontier

After recovery:

```
DURABLE STATE
     │
     ▼
RECOVERY
     │
     ├── completed work
     ├── queued work
     ├── blocked work
     ├── expired work
     ├── uncertain work
     └── corrupted work
             │
             ▼
        FRONTIER REBUILD
```

The frontier should be rebuilt from durable state rather than trusting the old in-memory queue.

---

<!-- source: Continue Architecture Planning.md L88780–88822 | turn 79 | version 0.32 -->
## v0.32 — 32.29 Reconciliation

v0.32 therefore introduces a dedicated reconciliation phase.

```JavaScript
class StateReconciler {
    async reconcile(state, context) {
        return {
            repairs: [],
            conflicts: [],
            warnings: []
        };
    }
}
```

It can identify:

```
claimed work without valid lease
reservation without owner
settlement without reservation
checkpoint without preceding evidence
candidate without provenance
artifact without durable storage
transaction without commit
```

But reconciliation must not silently rewrite history.

Instead:

```
detect conflict
     ↓
record conflict
     ↓
apply explicit recovery rule
     ↓
record repair event
```

---

<!-- source: Continue Architecture Planning.md L88824–88844 | turn 79 | version 0.32 -->
## v0.32 — 32.30 Repair is itself provenance

Suppose recovery requeues a work item.

Record:

```JavaScript
{
    type: "work-requeued-after-lease-expiry",

    workItemId: "work-42",

    reason: "worker lease expired",

    recoveryId: "recovery-7"
}
```

Now the history remains explainable.

---

<!-- source: Continue Architecture Planning.md L88897–88933 | turn 79 | version 0.32 -->
## v0.32 — 32.32 Complete lifecycle

The system now has a durable lifecycle:

```
PROPOSE
   ↓
ADMIT
   ↓
ARBITRATE
   ↓
ALLOCATE
   ↓
RESERVE
   ↓
CLAIM
   ↓
EXECUTE
   ↓
OBSERVE
   ↓
PERSIST KNOWLEDGE
   ↓
PERSIST ACCOUNTING
   ↓
PERSIST CHECKPOINT
   ↓
COMMIT
   ↓
RELEASE / SETTLE
   ↓
COMPLETE
```

Failure at any point enters explicit recovery semantics.

---

<!-- source: Continue Architecture Planning.md L89010–89040 | turn 79 | version 0.32 -->
## v0.32 — 32.35 What v0.32 changes

The engine has now crossed another important boundary.

Before:

```
runtime state
    ↓
search
```

After:

```
durable state
    ↓
reconstruct
    ↓
recover
    ↓
rebuild frontier
    ↓
resume
```

The search process is no longer merely **resumable by convention**.

It has an explicit recovery model.

---
