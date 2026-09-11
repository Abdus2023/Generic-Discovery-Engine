# Coordination, Consistency and Transport

> **Status:** DESIGNED
>
> **Source:** `Continue Architecture Planning.md`
>
> **Purpose:** Multi-context coordination, consistency models, conflict resolution, replication and event transport.

## Source Sections

- **v0.34 — Coordination Protocol & Distributed Consistency** — `CAP-1116` — `Continue Architecture Planning.md` L90351–90396
- **v0.34 — Distributed Consistency & Conflict Resolution** — `CAP-1118` — `Continue Architecture Planning.md` L90408–90446
- **v0.34 — 34.2 The Core Consistency Model** — `CAP-1120` — `Continue Architecture Planning.md` L90500–90585
- **v0.34 — 34.3 Optimistic Concurrency Control** — `CAP-1121` — `Continue Architecture Planning.md` L90587–90651
- **v0.34 — 34.4 Version ≠ Time** — `CAP-1122` — `Continue Architecture Planning.md` L90653–90694
- **v0.34 — 34.5 Event Metadata** — `CAP-1123` — `Continue Architecture Planning.md` L90696–90744
- **v0.34 — 34.6 Versioning + Fencing** — `CAP-1124` — `Continue Architecture Planning.md` L90746–90806
- **v0.34 — 34.7 Conflict Is Not One Thing** — `CAP-1125` — `Continue Architecture Planning.md` L90808–90830
- **v0.34 — Claim conflict** — `CAP-1126` — `Continue Architecture Planning.md` L90832–90839
- **v0.34 — Candidate conflict** — `CAP-1127` — `Continue Architecture Planning.md` L90841–90848
- **v0.34 — Classification conflict** — `CAP-1128` — `Continue Architecture Planning.md` L90850–90857
- **v0.34 — Coverage conflict** — `CAP-1129` — `Continue Architecture Planning.md` L90859–90873
- **v0.34 — Budget conflict** — `CAP-1130` — `Continue Architecture Planning.md` L90875–90886
- **v0.34 — 34.8 Conflict Record** — `CAP-1131` — `Continue Architecture Planning.md` L90888–90952
- **v0.34 — 34.9 Deterministic Conflict Resolver** — `CAP-1132` — `Continue Architecture Planning.md` L90954–90985
- **v0.34 — 34.10 Resolution Policies** — `CAP-1133` — `Continue Architecture Planning.md` L90987–91018
- **v0.34 — 34.11 Classification Conflict** — `CAP-1134` — `Continue Architecture Planning.md` L91020–91068
- **v0.34 — 34.12 Provenance Must Survive Resolution** — `CAP-1135` — `Continue Architecture Planning.md` L91070–91112
- **v0.34 — 34.13 Last-Write-Wins Is Not the Default** — `CAP-1136` — `Continue Architecture Planning.md` L91114–91156
- **v0.34 — 34.14 Append-Only Is Especially Powerful** — `CAP-1137` — `Continue Architecture Planning.md` L91158–91197
- **v0.34 — 34.15 Materialized State** — `CAP-1138` — `Continue Architecture Planning.md` L91199–91256
- **v0.34 — 34.16 State Digest** — `CAP-1139` — `Continue Architecture Planning.md` L91258–91304
- **v0.34 — 34.17 Conflict Detection Pipeline** — `CAP-1140` — `Continue Architecture Planning.md` L91306–91344
- **v0.34 — 34.18 Conflict Detection vs Conflict Resolution** — `CAP-1141` — `Continue Architecture Planning.md` L91346–91374
- **v0.34 — 34.19 Conflict Resolver Context** — `CAP-1142` — `Continue Architecture Planning.md` L91376–91420
- **v0.34 — 34.20 Resolution Event** — `CAP-1143` — `Continue Architecture Planning.md` L91422–91457
- **v0.34 — 34.21 Cross-Object Conflicts** — `CAP-1144` — `Continue Architecture Planning.md` L91459–91496
- **v0.34 — 34.22 Consistency Domains** — `CAP-1145` — `Continue Architecture Planning.md` L91498–91549
- **v0.34 — 34.23 Consistency Is Not Global Ordering** — `CAP-1146` — `Continue Architecture Planning.md` L91551–91585
- **v0.34 — 34.24 Independent Evidence** — `CAP-1147` — `Continue Architecture Planning.md` L91587–91622
- **v0.34 — Consistency** — `CAP-1150` — `Continue Architecture Planning.md` L91670–91677
- **v0.34 — Fencing** — `CAP-1151` — `Continue Architecture Planning.md` L91679–91683
- **v0.34 — Conflict** — `CAP-1152` — `Continue Architecture Planning.md` L91685–91693
- **v0.34 — Provenance** — `CAP-1153` — `Continue Architecture Planning.md` L91695–91700
- **v0.34 — Recovery** — `CAP-1154` — `Continue Architecture Planning.md` L91702–91707
- **v0.34 — Scalability** — `CAP-1155` — `Continue Architecture Planning.md` L91709–91716
- **v0.34 — 34.27 The Unified State Model** — `CAP-1156` — `Continue Architecture Planning.md` L91718–91798
- **v0.34 — Generic discovery** — `CAP-1167` — `Continue Architecture Planning.md` L92103–92123

## Related Documents

- [Concurrency](concurrency.md)
- [Persistence and Crash Recovery](persistence-and-recovery.md)
- [System Model](system-model.md)
- [Prototype Scope and Limitations](../prototype/limitations.md)

---

<!-- CAP-1116 | Continue Architecture Planning.md L90351–90396 | turn 81 | version 0.34 -->
## v0.34 — Coordination Protocol & Distributed Consistency

> **Source sections:** `CAP-1116`
>
> [DOCUMENTATION REVIEW] Contradiction **C-03** ([Review Notes](../REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming))

The next boundary is now visible.

v0.33 assumes that workers can safely interact with shared durable state.

But once multiple contexts produce concurrent updates, another question appears:

> **How are conflicting state transitions ordered, detected, and resolved?**

For example:

```
Worker A                 Worker B
   │                        │
   │ update candidate       │
   │                        │ update candidate
   │                        │
   └─────────┬──────────────┘
             ▼
        CONFLICT
```

This leads naturally to:

```
# v0.34 — Distributed Consistency & Conflict Resolution

Concurrent Events
        ↓
Ordering / Versioning
        ↓
Conflict Detection
        ↓
Conflict Classification
        ↓
Deterministic Resolution
        ↓
Immutable Conflict Record
        ↓
Reconciled State
```

The key principle for v0.34:

> **Concurrent disagreement must become explicit state, never silent last-write-wins.**

<!-- CAP-1118 | Continue Architecture Planning.md L90408–90446 | turn 83 | version 0.34 -->
## v0.34 — Distributed Consistency & Conflict Resolution

> **Source sections:** `CAP-1118`

v0.33 established **who owns work**.

v0.34 establishes **how shared state remains coherent when multiple workers modify it concurrently**.

The central problem is no longer claiming:

```
        Worker A
           │
           │ mutation
           ▼
      ┌──────────┐
      │  State   │
      └──────────┘
           ▲
           │ mutation
           │
        Worker B
```

The question becomes:

> What happens when A and B both believe they are modifying the same state from different versions of reality?

The answer cannot be:

```
last writer wins
```

because the later write may be based on stale state.

The v0.34 principle is:

> **Concurrent disagreement becomes explicit, durable, and resolvable state.**

---

<!-- CAP-1120 | Continue Architecture Planning.md L90500–90585 | turn 83 | version 0.34 -->
## v0.34 — 34.2 The Core Consistency Model

> **Source sections:** `CAP-1120`

Each mutable aggregate receives a monotonically increasing version.

```JavaScript
class StateVersion {
    constructor(data = {}) {
        this.aggregateId = data.aggregateId || null;
        this.version = data.version ?? 0;
        this.lastEventId = data.lastEventId || null;
        this.updatedAt = data.updatedAt || now();
    }
}
```

A mutation carries the version it was based upon:

```JavaScript
class StateMutation {
    constructor(data = {}) {
        this.aggregateId = data.aggregateId;
        this.expectedVersion = data.expectedVersion ?? 0;
        this.operation = data.operation;
        this.payload = data.payload || {};
        this.workerId = data.workerId || null;
        this.claimId = data.claimId || null;
        this.epoch = data.epoch ?? null;
        this.createdAt = data.createdAt || now();
    }
}
```

The authoritative state might currently be:

```
candidate-42
version = 7
```

Worker A reads version 7.

Worker B also reads version 7.

```
                 version 7
                    │
              ┌─────┴─────┐
              ▼           ▼
          Worker A     Worker B
          expects 7    expects 7
              │           │
              ▼           ▼
          mutation A   mutation B
```

A succeeds:

```
7 → 8
```

B then submits:

```
expectedVersion = 7
```

but authoritative state is already:

```
version = 8
```

Therefore:

```
REJECT AS STALE
```

not:

```
overwrite version 8
```

---

<!-- CAP-1121 | Continue Architecture Planning.md L90587–90651 | turn 83 | version 0.34 -->
## v0.34 — 34.3 Optimistic Concurrency Control

> **Source sections:** `CAP-1121`
>
> [DOCUMENTATION REVIEW] Contradiction **C-03** ([Review Notes](../REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming))

The primitive operation is effectively:

```
compare-and-swap

IF currentVersion == expectedVersion
    apply mutation
    currentVersion++
ELSE
    reject mutation
```

Contract:

```JavaScript
class ConsistencyStore {
    async read(aggregateId) {
        throw new Error('Not implemented');
    }

    async compareAndSwap(
        aggregateId,
        expectedVersion,
        mutation
    ) {
        throw new Error('Not implemented');
    }
}
```

Expected result:

```JavaScript
{
    status: 'committed',
    aggregateId: 'candidate-42',
    previousVersion: 7,
    newVersion: 8,
    eventId: 'evt-...',
}
```

or:

```JavaScript
{
    status: 'conflict',
    aggregateId: 'candidate-42',
    expectedVersion: 7,
    actualVersion: 8,
    conflictingEventId: 'evt-...',
}
```

This is much stronger than:

```JavaScript
state.updatedAt = Date.now();
```

because wall-clock timestamps are not reliable concurrency ordering.

---

<!-- CAP-1122 | Continue Architecture Planning.md L90653–90694 | turn 83 | version 0.34 -->
## v0.34 — 34.4 Version ≠ Time

> **Source sections:** `CAP-1122`

This distinction is important.

```
Timestamp
    =
physical-clock observation

Version
    =
logical state ordering
```

Suppose:

```
Worker A timestamp = 19:01:02.100
Worker B timestamp = 19:01:02.090
```

That does not prove B happened before A.

Clock skew exists.

Instead:

```
version 41
   ↓
version 42
   ↓
version 43
```

gives an authoritative ordering **within an aggregate**.

Therefore:

> Version numbers establish state-transition order, not global physical time.

---

<!-- CAP-1123 | Continue Architecture Planning.md L90696–90744 | turn 83 | version 0.34 -->
## v0.34 — 34.5 Event Metadata

> **Source sections:** `CAP-1123`

v0.32 introduced the durable event ledger.

v0.34 strengthens its causal metadata.

```JavaScript
class EventMetadata {
    constructor(data = {}) {
        this.eventId = data.eventId;
        this.aggregateId = data.aggregateId;
        this.aggregateType = data.aggregateType;

        this.sequence = data.sequence ?? null;
        this.expectedVersion = data.expectedVersion ?? null;
        this.resultingVersion = data.resultingVersion ?? null;

        this.transactionId = data.transactionId || null;

        this.workerId = data.workerId || null;
        this.claimId = data.claimId || null;
        this.epoch = data.epoch ?? null;

        this.parentEventId = data.parentEventId || null;

        this.createdAt = data.createdAt || now();
    }
}
```

This gives:

```
event
 ├── aggregate
 ├── expected version
 ├── resulting version
 ├── transaction
 ├── worker
 ├── claim
 ├── fencing epoch
 └── causal parent
```

Now the engine can answer:

> Why did this state transition happen?

---

<!-- CAP-1124 | Continue Architecture Planning.md L90746–90806 | turn 83 | version 0.34 -->
## v0.34 — 34.6 Versioning + Fencing

> **Source sections:** `CAP-1124`
>
> [DOCUMENTATION REVIEW] Contradiction **C-03** ([Review Notes](../REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming))

v0.33 introduced fencing.

v0.34 combines fencing with optimistic concurrency.

A valid mutation now requires:

```
worker identity
      +
claim identity
      +
claim epoch
      +
valid lease
      +
expected state version
```

Conceptually:

```
                 Mutation
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
     Fencing     Version      Policy
      check       check        check
        │           │           │
        └───────────┼───────────┘
                    ▼
                 COMMIT
```

The invariant becomes:

```
Mutate(W,S,M)
⇒
Owner(W) = Worker(M)
∧ Claim(W) = Claim(M)
∧ Epoch(W) = Epoch(M)
∧ LeaseValid(M)
∧ ExpectedVersion(M) = CurrentVersion(S)
∧ PolicyAllows(M)
```

This prevents two different classes of stale writes:

```
stale worker
    ↓
fencing rejects

stale state
    ↓
version check rejects
```

---

<!-- CAP-1125 | Continue Architecture Planning.md L90808–90830 | turn 83 | version 0.34 -->
## v0.34 — 34.7 Conflict Is Not One Thing

> **Source sections:** `CAP-1125`

A generic `CONFLICT` state is insufficient.

v0.34 introduces explicit conflict classes.

```JavaScript
const ConflictType = Object.freeze({
    CLAIM: 'claim',
    WORK_STATE: 'work-state',
    CANDIDATE: 'candidate',
    RESOURCE: 'resource',
    CLASSIFICATION: 'classification',
    COVERAGE: 'coverage',
    BUDGET: 'budget',
    CHECKPOINT: 'checkpoint',
    ARTIFACT: 'artifact',
    IDENTITY: 'identity',
    CONFIGURATION: 'configuration'
});
```

Examples:

<!-- CAP-1126 | Continue Architecture Planning.md L90832–90839 | turn 83 | version 0.34 -->
### v0.34 — Claim conflict

> **Source sections:** `CAP-1126`
>
> [DOCUMENTATION REVIEW] Contradiction **C-03** ([Review Notes](../REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming))

```
A claims work-17
B claims work-17
```

Usually resolved by authoritative claim state.

<!-- CAP-1127 | Continue Architecture Planning.md L90841–90848 | turn 83 | version 0.34 -->
### v0.34 — Candidate conflict

> **Source sections:** `CAP-1127`

```
A: candidate status = queued
B: candidate status = completed
```

Requires transition validation.

<!-- CAP-1128 | Continue Architecture Planning.md L90850–90857 | turn 83 | version 0.34 -->
### v0.34 — Classification conflict

> **Source sections:** `CAP-1128`

```
Classifier A → service-manual
Classifier B → parts-catalog
```

This may be a **legitimate epistemic disagreement**, not a database error.

<!-- CAP-1129 | Continue Architecture Planning.md L90859–90873 | turn 83 | version 0.34 -->
### v0.34 — Coverage conflict

> **Source sections:** `CAP-1129`
>
> [DOCUMENTATION REVIEW] Contradiction **C-05** ([Review Notes](../REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified))

```
Partition A
    worker A: 60% explored
    worker B: 35% explored
```

These values cannot simply be:

```
60 + 35 = 95%
```

because exploration may overlap.

<!-- CAP-1130 | Continue Architecture Planning.md L90875–90886 | turn 83 | version 0.34 -->
### v0.34 — Budget conflict

> **Source sections:** `CAP-1130`

```
Worker A reserves 8 requests
Worker B reserves 7 requests

budget = 10
```

This must be prevented atomically.

---

<!-- CAP-1131 | Continue Architecture Planning.md L90888–90952 | turn 83 | version 0.34 -->
## v0.34 — 34.8 Conflict Record

> **Source sections:** `CAP-1131`

Conflicts become durable objects.

```JavaScript
class ConflictRecord {
    constructor(data = {}) {
        this.id = data.id || makeId('conflict');

        this.type = data.type;
        this.aggregateId = data.aggregateId || null;

        this.baseVersion = data.baseVersion ?? null;
        this.currentVersion = data.currentVersion ?? null;

        this.leftEventId = data.leftEventId || null;
        this.rightEventId = data.rightEventId || null;

        this.leftState = data.leftState || null;
        this.rightState = data.rightState || null;

        this.reason = data.reason || null;

        this.status = data.status || 'detected';

        this.resolution = data.resolution || null;

        this.createdAt = data.createdAt || now();
        this.resolvedAt = data.resolvedAt || null;
    }
}
```

Lifecycle:

```
DETECTED
    │
    ▼
CLASSIFIED
    │
    ├──────────────┐
    ▼              ▼
AUTO_RESOLVABLE   HUMAN_REVIEW
    │              │
    ▼              ▼
RESOLVING       UNDER_REVIEW
    │              │
    └──────┬───────┘
           ▼
       RESOLVED
           │
           ▼
      RECONCILED
```

Exceptional terminal state:

```
UNRESOLVED
```

Unresolved is preferable to fabricated agreement.

---

<!-- CAP-1132 | Continue Architecture Planning.md L90954–90985 | turn 83 | version 0.34 -->
## v0.34 — 34.9 Deterministic Conflict Resolver

> **Source sections:** `CAP-1132`

```JavaScript
class ConflictResolver {
    canResolve(conflict, context) {
        return false;
    }

    async resolve(conflict, context) {
        throw new Error('Not implemented');
    }

    describe() {
        return {
            id: 'unknown-resolver',
            name: 'Unknown Conflict Resolver'
        };
    }
}
```

Resolution must be **type-specific**.

There should not be one universal:

```JavaScript
return newer;
```

policy.

---

<!-- CAP-1133 | Continue Architecture Planning.md L90987–91018 | turn 83 | version 0.34 -->
## v0.34 — 34.10 Resolution Policies

> **Source sections:** `CAP-1133`

A useful initial matrix:

| Conflict | Default resolution |
| --- | --- |
| claim | authoritative lease/fencing state |
| work status | valid state-transition ordering |
| budget | atomic reservation ledger |
| checkpoint | highest valid durable checkpoint |
| candidate metadata | field-wise deterministic merge |
| provenance | union, never overwrite |
| observation | preserve both |
| artifact | content-addressed identity |
| classification | preserve competing assertions |
| coverage | union only when overlap semantics permit |
| identity | explicit resolver / unresolved |
| configuration | versioned policy decision |

The crucial distinction:

```
STATE CONFLICT
    ≠
EVIDENCE CONFLICT
```

A database conflict may be automatically resolvable.

An epistemic conflict may not be.

---

<!-- CAP-1134 | Continue Architecture Planning.md L91020–91068 | turn 83 | version 0.34 -->
## v0.34 — 34.11 Classification Conflict

> **Source sections:** `CAP-1134`

Consider:

```
artifact-91
     │
     ├── classifier-A
     │      └── "service-manual"
     │
     └── classifier-B
            └── "parts-catalog"
```

It would be wrong to choose:

```
service-manual
```

simply because classifier A ran later.

Instead:

```
ClassificationAssertion A
ClassificationAssertion B
        │
        ▼
Conflict / ambiguity
```

The knowledge graph retains both.

A later verification step can produce:

```
VerificationEvidence
       │
       ▼
Resolution:
"service-manual"
```

Thus:

> Conflict resolution does not mean deleting disagreement. It means establishing what the system is justified in believing.

---

<!-- CAP-1135 | Continue Architecture Planning.md L91070–91112 | turn 83 | version 0.34 -->
## v0.34 — 34.12 Provenance Must Survive Resolution

> **Source sections:** `CAP-1135`

Bad:

```
A + B
 ↓
C
```

where A and B disappear.

Correct:

```
A ───────────────┐
                 ├── Conflict C
B ───────────────┘
                      │
                      ▼
                 Resolution R
                      │
                      ▼
                 State S
```

The history remains:

```
Event A
Event B
Conflict C
Resolution R
State S
```

Therefore a future auditor can reconstruct:

```
why was this state selected?
```

---

<!-- CAP-1136 | Continue Architecture Planning.md L91114–91156 | turn 83 | version 0.34 -->
## v0.34 — 34.13 Last-Write-Wins Is Not the Default

> **Source sections:** `CAP-1136`

LWW can be useful for some explicitly declared fields.

For example:

```
UI heartbeat
temporary presentation metadata
non-authoritative cache hints
```

But dangerous for:

```
audit evidence
claims
classification
budget
coverage
checkpoints
security policy
resource identity
artifact provenance
```

Therefore:

```JavaScript
const MergePolicy = Object.freeze({
    REJECT_STALE: 'reject-stale',
    FIELD_MERGE: 'field-merge',
    APPEND_ONLY: 'append-only',
    MAX_VALID_VERSION: 'max-valid-version',
    UNION_IF_DISJOINT: 'union-if-disjoint',
    PRESERVE_CONFLICT: 'preserve-conflict',
    EXPLICIT_RESOLUTION: 'explicit-resolution'
});
```

Every mutable aggregate should have an explicit merge policy.

---

<!-- CAP-1137 | Continue Architecture Planning.md L91158–91197 | turn 83 | version 0.34 -->
## v0.34 — 34.14 Append-Only Is Especially Powerful

> **Source sections:** `CAP-1137`

For evidence:

```
Worker A → Evidence A
Worker B → Evidence B
```

No merge is necessary.

Just:

```
EvidenceSet = {A, B}
```

This makes evidence naturally concurrency-friendly.

Likewise:

```
ObservationSet
DiscoverySet
ProvenanceSet
ConflictSet
EventSet
```

are preferably append-only.

This yields an important architectural pattern:

```
Mutable operational state
        +
Append-only epistemic history
```

---

<!-- CAP-1138 | Continue Architecture Planning.md L91199–91256 | turn 83 | version 0.34 -->
## v0.34 — 34.15 Materialized State

> **Source sections:** `CAP-1138`

The engine should treat current state as a projection.

```
             EVENT JOURNAL
                   │
          ┌────────┴────────┐
          ▼                 ▼
     Materializer       Auditor
          │
          ▼
   MATERIALIZED STATE
          │
          ▼
       Frontier
```

Example:

```
event 101
candidate queued

event 102
candidate claimed

event 103
attempt started

event 104
observation recorded

event 105
candidate completed
```

Materialized state:

```JavaScript
{
    status: 'completed',
    attempts: 1,
    observationId: 'obs-42'
}
```

If the materialized state becomes corrupted:

```
replay events
      ↓
rebuild
      ↓
compare state digest
```

---

<!-- CAP-1139 | Continue Architecture Planning.md L91258–91304 | turn 83 | version 0.34 -->
## v0.34 — 34.16 State Digest

> **Source sections:** `CAP-1139`

Snapshots introduced in v0.32 can now carry deterministic state hashes.

```JavaScript
class StateDigest {
    constructor(data = {}) {
        this.algorithm = data.algorithm || 'sha256';
        this.digest = data.digest || null;
        this.sequence = data.sequence ?? null;
        this.schemaVersion = data.schemaVersion || null;
    }
}
```

Checkpoint:

```
snapshot
   ├── eventSequence = 8421
   ├── schemaVersion = 34
   └── stateDigest = SHA-256(...)
```

Recovery:

```
snapshot
   ↓
replay events 8422...
   ↓
reconstructed state
   ↓
digest
   ↓
compare
```

Mismatch becomes:

```
STATE_INTEGRITY_CONFLICT
```

not silent repair.

---

<!-- CAP-1140 | Continue Architecture Planning.md L91306–91344 | turn 83 | version 0.34 -->
## v0.34 — 34.17 Conflict Detection Pipeline

> **Source sections:** `CAP-1140`

The complete v0.34 pipeline:

```
Mutation Request
      │
      ▼
Validate Worker
      │
      ▼
Validate Fencing
      │
      ▼
Validate Expected Version
      │
      ├───────────────┐
      │               │
      ▼               ▼
    VALID           STALE
      │               │
      ▼               ▼
   COMMIT         ConflictRecord
      │               │
      ▼               ▼
 New Version      ConflictClassifier
                      │
              ┌───────┴────────┐
              ▼                ▼
         Auto-resolve      Unresolved
              │                │
              ▼                ▼
        ResolutionEvent    Review Queue
              │
              ▼
        Materialized State
```

---

<!-- CAP-1141 | Continue Architecture Planning.md L91346–91374 | turn 83 | version 0.34 -->
## v0.34 — 34.18 Conflict Detection vs Conflict Resolution

> **Source sections:** `CAP-1141`

Keep these separate.

```
Detection:
"Something disagrees."

Classification:
"What kind of disagreement?"

Resolution:
"Can it be safely reconciled?"

Verification:
"Do we have evidence that the resolution is justified?"
```

This prevents:

```
conflict detected
      ↓
automatic overwrite
```

from becoming the architecture.

---

<!-- CAP-1142 | Continue Architecture Planning.md L91376–91420 | turn 83 | version 0.34 -->
## v0.34 — 34.19 Conflict Resolver Context

> **Source sections:** `CAP-1142`

A resolver should receive restricted context:

```JavaScript
class ConflictContext {
    constructor(data = {}) {
        this.conflict = data.conflict;

        this.baseState = data.baseState;
        this.currentState = data.currentState;

        this.events = data.events || [];
        this.evidence = data.evidence || [];

        this.policy = data.policy;
        this.version = data.version;

        this.emitEvent = data.emitEvent;
    }
}
```

It should **not** receive unrestricted engine authority.

The resolver can:

```
inspect
compare
validate
emit resolution
```

but cannot:

```
acquire arbitrary URLs
change domain
increase budget
disable policy
delete evidence
```

---

<!-- CAP-1143 | Continue Architecture Planning.md L91422–91457 | turn 83 | version 0.34 -->
## v0.34 — 34.20 Resolution Event

> **Source sections:** `CAP-1143`

A resolution itself is an event.

```JavaScript
{
    type: 'conflict-resolved',

    conflictId: 'conflict-17',

    resolution: {
        policy: 'append-only',
        selected: [
            'event-801',
            'event-802'
        ],
        rejected: [],
        merged: true
    },

    resolverId: 'candidate-merge-v1',
    resolverVersion: '1.0.0'
}
```

Thus:

```
Conflict
   ↓
Resolution
```

is itself auditable.

---

<!-- CAP-1144 | Continue Architecture Planning.md L91459–91496 | turn 83 | version 0.34 -->
## v0.34 — 34.21 Cross-Object Conflicts

> **Source sections:** `CAP-1144`

Some conflicts cannot be understood from one aggregate.

Example:

```
Budget = 10

Worker A reservation = 6
Worker B reservation = 6
```

Each worker's local state may appear valid.

The conflict exists at the budget aggregate.

Therefore:

> **Consistency boundaries must correspond to the invariant being protected.**

Bad:

```
worker-local reservation state
```

Good:

```
shared budget aggregate
        │
        └── atomic reservation transition
```

This is the same principle used for claims.

---

<!-- CAP-1145 | Continue Architecture Planning.md L91498–91549 | turn 83 | version 0.34 -->
## v0.34 — 34.22 Consistency Domains

> **Source sections:** `CAP-1145`

v0.34 therefore introduces:

```JavaScript
const ConsistencyScope = Object.freeze({
    WORK_ITEM: 'work-item',
    CANDIDATE: 'candidate',
    RESOURCE: 'resource',
    BUDGET: 'budget',
    PARTITION: 'partition',
    SESSION: 'session',
    DOMAIN: 'domain',
    GLOBAL: 'global'
});
```

Not every object needs global serialization.

For scalability:

```
candidate-1 → independent
candidate-2 → independent
candidate-3 → independent
```

can progress concurrently.

But:

```
budget-global
```

may require serialized mutation.

This gives:

```
parallelism
    +
local consistency boundaries
```

rather than:

```
global lock
```

---

<!-- CAP-1146 | Continue Architecture Planning.md L91551–91585 | turn 83 | version 0.34 -->
## v0.34 — 34.23 Consistency Is Not Global Ordering

> **Source sections:** `CAP-1146`

The engine should explicitly reject the assumption:

```
all events have one universal meaningful order
```

Instead:

```
Aggregate A
  v1 → v2 → v3

Aggregate B
  v1 → v2

Aggregate C
  v1 → v2 → v3 → v4
```

Cross-aggregate relationships are represented by:

```
transactionId
parentEventId
causal references
sessionId
workerId
claimId
```

rather than pretending that wall-clock order is causality.

---

<!-- CAP-1147 | Continue Architecture Planning.md L91587–91622 | turn 83 | version 0.34 -->
## v0.34 — 34.24 Independent Evidence

> **Source sections:** `CAP-1147`

This also connects back to v0.28.

Suppose:

```
Worker A discovers URL X
Worker B discovers URL X
```

These are not necessarily:

```
independent confirmations
```

if both workers observed the same source.

Therefore the conflict/coordination layer should retain:

```JavaScript
{
    observationId,
    sourceObservationId,
    workerId,
    mechanism,
    parentEventId
}
```

Then independence can be evaluated later.

This is important for completeness and negative evidence.

---

<!-- CAP-1150 | Continue Architecture Planning.md L91670–91677 | turn 83 | version 0.34 -->
### v0.34 — Consistency

> **Source sections:** `CAP-1150`

1. Every mutable aggregate has an authoritative version.
2. A mutation must declare its expected version.
3. Stale mutations cannot silently overwrite newer state.
4. Version increments are monotonic.
5. Version regression is invalid.
6. Event sequence gaps are detectable.

<!-- CAP-1151 | Continue Architecture Planning.md L91679–91683 | turn 83 | version 0.34 -->
### v0.34 — Fencing

> **Source sections:** `CAP-1151`
>
> [DOCUMENTATION REVIEW] Contradiction **C-03** ([Review Notes](../REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming))

7. Fencing prevents stale workers from mutating current state.
8. Versioning prevents stale state from producing valid-looking mutations.
9. Fencing and versioning protect different failure modes.

<!-- CAP-1152 | Continue Architecture Planning.md L91685–91693 | turn 83 | version 0.34 -->
### v0.34 — Conflict

> **Source sections:** `CAP-1152`

10. Concurrent disagreement becomes explicit state.
11. Conflict records are immutable.
12. Resolution never deletes historical evidence.
13. Unresolvable conflicts remain unresolved.
14. Conflict resolution is type-specific.
15. Merge policy is explicit.
16. Last-write-wins is never implicit.

<!-- CAP-1153 | Continue Architecture Planning.md L91695–91700 | turn 83 | version 0.34 -->
### v0.34 — Provenance

> **Source sections:** `CAP-1153`

17. Every resolution references the conflicting inputs.
18. Provenance is append-only.
19. Duplicate execution does not automatically create independent evidence.
20. Resolution cannot increase epistemic strength without evidence.

<!-- CAP-1154 | Continue Architecture Planning.md L91702–91707 | turn 83 | version 0.34 -->
### v0.34 — Recovery

> **Source sections:** `CAP-1154`

21. Materialized state remains reconstructable from the event journal.
22. Snapshot digests detect divergence.
23. Recovery cannot fabricate missing events.
24. Repairs produce explicit events.

<!-- CAP-1155 | Continue Architecture Planning.md L91709–91716 | turn 83 | version 0.34 -->
### v0.34 — Scalability

> **Source sections:** `CAP-1155`

25. Consistency scope is no broader than necessary.
26. Global serialization is avoided unless the invariant requires it.
27. Independent aggregates may progress concurrently.
28. Cross-aggregate invariants use explicit shared consistency boundaries.

---

<!-- CAP-1156 | Continue Architecture Planning.md L91718–91798 | turn 83 | version 0.34 -->
## v0.34 — 34.27 The Unified State Model

> **Source sections:** `CAP-1156`

At this point the architecture is becoming:

```
                         SEARCH GOAL
                              │
                              ▼
                         QUERY PLAN
                              │
                              ▼
                       SEARCH TACTICS
                              │
                              ▼
                         PARTITIONS
                              │
                              ▼
                         DISCOVERY
                              │
                              ▼
                         CANDIDATES
                              │
                              ▼
                    FRONTIER ARBITRATION
                              │
                              ▼
                         WORK ITEMS
                              │
                              ▼
                       COORDINATION
                              │
                       ┌──────┴──────┐
                       ▼             ▼
                    Worker A      Worker B
                       │             │
                       └──────┬──────┘
                              ▼
                    CONSISTENCY CONTROL
                              │
                  ┌───────────┴───────────┐
                  ▼                       ▼
               COMMIT                 CONFLICT
                  │                       │
                  │                  RESOLUTION
                  │                       │
                  └───────────┬───────────┘
                              ▼
                       ACQUISITION
                              │
                              ▼
                        OBSERVATION
                              │
                              ▼
                           EVIDENCE
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
              CLASSIFICATION       VERIFICATION
                    │                   │
                    └─────────┬─────────┘
                              ▼
                       RESOURCE GRAPH
                              │
                              ▼
                       COVERAGE MODEL
                              │
                              ▼
                     COMPLETENESS CLAIM
```

The important architectural progression is now:

```
v0.30  Which work next?
v0.31  What may it consume?
v0.32  What survives a crash?
v0.33  Who owns concurrent work?
v0.34  How do concurrent states converge?
```

---

<!-- CAP-1167 | Continue Architecture Planning.md L92103–92123 | turn 85 | version 0.34 -->
### v0.34 — Generic discovery

> **Source sections:** `CAP-1167`

```
resource space
      ↓
probe
      ↓
observation
      ↓
resource discovery
      ↓
new partitions
```

The transferable principle is therefore **not DVB**.

It is:

> **Systematic exploration of an incompletely known space through bounded probes, observations, stateful frontier expansion, and explicit termination semantics.**

---
