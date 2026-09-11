# Work Items and Frontier Arbitration

> **Status:** DESIGNED
>
> **Source:** `Continue Architecture Planning.md`
>
> **Purpose:** Work items, work kinds, lifecycle, dependencies, frontier runtime and unified frontier arbitration.

## Contents

- **v0.15 — WorkItem + Frontier Runtime** — `Continue Architecture Planning.md` L61954–61988
- **v0.15 — WorkItem + Frontier Runtime** — `Continue Architecture Planning.md` L62000–62029
- **v0.15 — 1. The key distinction** — `Continue Architecture Planning.md` L62031–62070
- **v0.15 — 2. Why `WorkItem` exists** — `Continue Architecture Planning.md` L62072–62129
- **v0.15 — 3. WorkItem** — `Continue Architecture Planning.md` L62131–62207
- **v0.15 — 4. Work kinds** — `Continue Architecture Planning.md` L62209–62242
- **v0.15 — 5. Work payload** — `Continue Architecture Planning.md` L62244–62294
- **v0.15 — 6. Work lifecycle** — `Continue Architecture Planning.md` L62296–62347
- **v0.15 — 10. Frontier Runtime** — `Continue Architecture Planning.md` L62492–62528
- **v0.15 — 15. Why not one giant queue?** — `Continue Architecture Planning.md` L62697–62734
- **v0.15 — 16. Work dependencies** — `Continue Architecture Planning.md` L62736–62778
- **v0.15 — 17. But dependencies must not create hidden coupling** — `Continue Architecture Planning.md` L62780–62798
- **v0.15 — 18. Dependency states** — `Continue Architecture Planning.md` L62800–62830
- **v0.15 — 19. Work completion** — `Continue Architecture Planning.md` L62832–62873
- **v0.15 — 20. Work execution boundary** — `Continue Architecture Planning.md` L62875–62933
- **v0.15 — 21. Work Runtime** — `Continue Architecture Planning.md` L62935–62977
- **v0.15 — 22. Retry becomes generic** — `Continue Architecture Planning.md` L62979–63027
- **v0.15 — 23. Retry identity** — `Continue Architecture Planning.md` L63029–63071
- **v0.15 — 24. Cancellation** — `Continue Architecture Planning.md` L63073–63108
- **v0.15 — 25. Scan termination with WorkItems** — `Continue Architecture Planning.md` L63110–63150
- **v0.15 — 26. The three frontier states** — `Continue Architecture Planning.md` L63152–63180
- **v0.15 — 28. Work state machine** — `Continue Architecture Planning.md` L63221–63264
- **v0.15 — 29. Domain → Session → Work** — `Continue Architecture Planning.md` L63266–63290
- **v0.15 — 30. What belongs where?** — `Continue Architecture Planning.md` L63292–63312
- **v0.15 — 34. v0.15 architectural result** — `Continue Architecture Planning.md` L63432–63497
- **v0.30 — Unified Frontier Arbitration** — `Continue Architecture Planning.md` L84664–84685
- **v0.30 — The final conceptual separation** — `Continue Architecture Planning.md` L84762–84791
- **v0.30 — The most important safety boundary** — `Continue Architecture Planning.md` L84910–84948
- *Turn lead-in* — `Continue Architecture Planning.md` L85131–85131
- **v0.30 — Unified Frontier Arbitration** — `Continue Architecture Planning.md` L85137–85169
- **v0.30 — 30.2 WorkClass** — `Continue Architecture Planning.md` L85215–85256
- **v0.30 — 30.3 WorkClassPolicy** — `Continue Architecture Planning.md` L85258–85314
- **v0.30 — 30.4 ArbitrationDecision** — `Continue Architecture Planning.md` L85316–85382
- **v0.30 — 30.5 Hard constraints vs soft priorities** — `Continue Architecture Planning.md` L85384–85386
- **v0.30 — Hard constraints** — `Continue Architecture Planning.md` L85388–85402
- **v0.30 — Soft priorities** — `Continue Architecture Planning.md` L85404–85441
- **v0.30 — 30.6 Arbitration score** — `Continue Architecture Planning.md` L85443–85480
- **v0.30 — 30.7 Aging** — `Continue Architecture Planning.md` L85482–85531
- **v0.30 — 30.8 Starvation detection** — `Continue Architecture Planning.md` L85533–85579
- **v0.30 — 30.9 Class starvation** — `Continue Architecture Planning.md` L85581–85625
- **v0.30 — 30.10 Weighted fairness** — `Continue Architecture Planning.md` L85627–85656
- **v0.30 — 30.11 Deficit-style arbitration** — `Continue Architecture Planning.md` L85658–85704
- **v0.30 — 30.12 Cost-aware scheduling** — `Continue Architecture Planning.md` L85706–85759
- **v0.30 — 30.13 Backpressure** — `Continue Architecture Planning.md` L85761–85818
- **v0.30 — 30.14 Reserved capacity** — `Continue Architecture Planning.md` L85820–85854
- **v0.30 — 30.15 Arbitration pipeline** — `Continue Architecture Planning.md` L85856–85909
- **v0.30 — 30.16 The atomicity problem** — `Continue Architecture Planning.md` L85911–85957
- **v0.30 — 30.17 Priority inversion** — `Continue Architecture Planning.md` L85959–85997
- **v0.30 — 30.18 FrontierArbitrator** — `Continue Architecture Planning.md` L85999–86050
- **v0.30 — 30.19 Arbitration result** — `Continue Architecture Planning.md` L86052–86090
- **v0.30 — 30.20 Arbitration ledger** — `Continue Architecture Planning.md` L86092–86119
- **v0.30 — 30.21 Replay** — `Continue Architecture Planning.md` L86121–86172

## Related Documents

- [Scheduling](scheduler.md)
- [Concurrency](concurrency.md)
- [Domains, Sessions and Termination](sessions-and-domains.md)
- [Resource and Cost Ledger](resource-budget.md)

---

<!-- source: Continue Architecture Planning.md L61954–61988 | turn 41 | version 0.15 -->
## v0.15 — WorkItem + Frontier Runtime

The goal would be to formalize:

```
                 SCAN SESSION
                      │
                      ▼
                WORK FRONTIER
                 /           \
                /             \
               ▼               ▼
        DiscoveryWork     AcquisitionWork
               │               │
               ▼               ▼
       DiscoveryController   AcquisitionRuntime
```

with explicit:

```
WorkItem
WorkState
WorkLease
WorkPriority
WorkDependency
WorkRetry
WorkCompletion
```

The critical principle for v0.15 would be:

> **Discovery and acquisition remain different operations, but they become instances of one bounded, recoverable work model.**

That would solve the remaining scheduler/queue/lease duplication without merging the semantics of discovery and acquisition.

<!-- source: Continue Architecture Planning.md L62000–62029 | turn 43 | version 0.15 -->
## v0.15 — WorkItem + Frontier Runtime

v0.14 made the **search space explicit**.

The remaining problem is operational:

> How does the engine represent, schedule, claim, execute, retry, recover, and complete the different kinds of work produced during a scan?

Currently we have separate concepts:

```
DiscoveryTask
Candidate
AcquisitionPlan
Attempt
```

They each have their own lifecycle and scheduling logic.

That works, but it creates duplication.

The v0.15 abstraction is:

```
WorkItem
```

Not as a replacement for discovery or acquisition semantics, but as their **common execution envelope**.

---

<!-- source: Continue Architecture Planning.md L62031–62070 | turn 43 | version 0.15 -->
## v0.15 — 1. The key distinction

We should **not** do this:

```
WorkItem
    └── everything is generic
```

That would erase important semantics.

Instead:

```
                     WorkItem
                         │
             ┌───────────┴───────────┐
             │                       │
             ▼                       ▼
      DiscoveryWork          AcquisitionWork
             │                       │
             ▼                       ▼
   DiscoveryController       AcquisitionRuntime
```

So:

```
WorkItem = scheduling/execution identity

DiscoveryWork = discovery semantics

AcquisitionWork = acquisition semantics
```

This is the same architectural principle already established:

> **Common infrastructure should not erase domain semantics.**

---

<!-- source: Continue Architecture Planning.md L62072–62129 | turn 43 | version 0.15 -->
## v0.15 — 2. Why `WorkItem` exists

Without a common work model, every subsystem independently needs:

```
queue
priority
claim
lease
retry
cancellation
timestamps
status
owner
completion
failure
```

We would eventually have:

```
DiscoveryTask
 ├── status
 ├── claimedBy
 ├── retry
 └── priority

AcquisitionPlan
 ├── status
 ├── claimedBy
 ├── retry
 └── priority

RecognitionTask
 ├── status
 ├── claimedBy
 ├── retry
 └── priority
```

The semantics become duplicated.

Instead:

```
WorkItem
├── identity
├── ownership
├── scheduling
├── lifecycle
├── retry
├── lease
└── cancellation
```

while the specialized object contains its own domain data.

---

<!-- source: Continue Architecture Planning.md L62131–62207 | turn 43 | version 0.15 -->
## v0.15 — 3. WorkItem

Conceptual structure:

```JavaScript
class WorkItem {
    constructor(data = {}) {
        this.id =
            data.id || makeId('work');

        this.kind =
            data.kind || 'unknown';

        this.sessionId =
            data.sessionId || null;

        this.parentId =
            data.parentId || null;

        this.priority =
            Number.isFinite(data.priority)
                ? data.priority
                : 0;

        this.depth =
            Number.isFinite(data.depth)
                ? data.depth
                : 0;

        this.status =
            data.status || 'queued';

        this.attempts =
            data.attempts || 0;

        this.createdAt =
            data.createdAt || now();

        this.queuedAt =
            data.queuedAt || null;

        this.claimedAt =
            data.claimedAt || null;

        this.startedAt =
            data.startedAt || null;

        this.completedAt =
            data.completedAt || null;

        this.claimedBy =
            data.claimedBy || null;

        this.claimId =
            data.claimId || null;

        this.leaseUntil =
            data.leaseUntil || null;

        this.nextAttemptAt =
            data.nextAttemptAt || null;

        this.error =
            data.error || null;
    }
}
```

But this object should remain deliberately boring.

It should not know how discovery works.

It should not know how HTTP works.

It should not know how recognition works.

---

<!-- source: Continue Architecture Planning.md L62209–62242 | turn 43 | version 0.15 -->
## v0.15 — 4. Work kinds

Initial work kinds:

```
discovery
acquisition
recognition
```

Potential future kinds:

```
verification
revalidation
indexing
persistence
synchronization
user-review
```

But v0.15 should implement only what the engine actually needs.

Therefore:

```
v0.15
    discovery
    acquisition
```

Recognition can remain inside the acquisition pipeline initially.

---

<!-- source: Continue Architecture Planning.md L62244–62294 | turn 43 | version 0.15 -->
## v0.15 — 5. Work payload

The generic envelope needs a typed payload.

For example:

```JavaScript
{
    id: 'work-123',

    kind: 'discovery',

    sessionId: 'scan-001',

    priority: 0.84,

    status: 'queued',

    payload: {
        sourceId: 'html-link',
        observationId: 'obs-991'
    }
}
```

Acquisition:

```JavaScript
{
    id: 'work-456',

    kind: 'acquisition',

    sessionId: 'scan-001',

    priority: 0.71,

    status: 'queued',

    payload: {
        candidateId: 'cand-42',
        planId: 'plan-99'
    }
}
```

The scheduler only needs the envelope.

The executor interprets the payload.

---

<!-- source: Continue Architecture Planning.md L62296–62347 | turn 43 | version 0.15 -->
## v0.15 — 6. Work lifecycle

A common lifecycle can now be defined.

```
                 ┌─────────┐
                 │ QUEUED  │
                 └────┬────┘
                      │
                      ▼
                 ┌─────────┐
                 │ CLAIMED │
                 └────┬────┘
                      │
                      ▼
                 ┌─────────┐
                 │ RUNNING │
                 └────┬────┘
                      │
          ┌───────────┼────────────┐
          │           │            │
          ▼           ▼            ▼
      COMPLETED    RETRY       FAILED
                      │
                      ▼
                   QUEUED
```

Cancellation:

```
QUEUED ───────→ CANCELLED
CLAIMED ──────→ CANCELLED
RUNNING ──────→ CANCELLED
```

Lease expiration:

```
CLAIMED
   │
   ▼
lease expired
   │
   ▼
RECOVERABLE
   │
   ▼
QUEUED
```

---

<!-- source: Continue Architecture Planning.md L62492–62528 | turn 43 | version 0.15 -->
## v0.15 — 10. Frontier Runtime

Now we can introduce the actual common frontier.

```
                  FRONTIER RUNTIME
                        │
              ┌─────────┴─────────┐
              │                   │
              ▼                   ▼
       Discovery Work      Acquisition Work
              │                   │
              └─────────┬─────────┘
                        │
                        ▼
                    Scheduler
                        │
                        ▼
                      Claim
                        │
                        ▼
                     Execute
```

The frontier contains work.

It does **not** contain knowledge.

That distinction remains:

```
KnowledgeBase = what we know

FrontierRuntime = what remains to do
```

---

<!-- source: Continue Architecture Planning.md L62697–62734 | turn 43 | version 0.15 -->
## v0.15 — 15. Why not one giant queue?

A single queue sounds simpler:

```
everything → priority queue
```

but it hides an important difference.

Discovery produces knowledge.

Acquisition consumes network budget.

They have different:

* resource costs
* policies
* failure modes
* capabilities
* rate limits
* termination implications

Therefore:

```
one WorkItem model
```

does not imply:

```
one undifferentiated execution policy
```

The runtime should preserve work-class boundaries.

---

<!-- source: Continue Architecture Planning.md L62736–62778 | turn 43 | version 0.15 -->
## v0.15 — 16. Work dependencies

Now another useful property becomes possible.

Suppose:

```
Acquire observation
       ↓
Recognition
       ↓
Discovery
```

Some work cannot start before another operation completes.

Represent:

```JavaScript
{
    id: 'work-2',

    kind: 'discovery',

    dependencies: [
        'work-1'
    ]
}
```

Then:

```
work-1
  │
  │ completed
  ▼
work-2
```

This gives us a work DAG.

---

<!-- source: Continue Architecture Planning.md L62780–62798 | turn 43 | version 0.15 -->
## v0.15 — 17. But dependencies must not create hidden coupling

The engine should not turn into a giant workflow engine.

A dependency should mean only:

> This work item is not eligible until the referenced work has reached an acceptable state.

For example:

```
discovery task
depends on
observation
```

But the actual discovery semantics remain in `DiscoveryController`.

---

<!-- source: Continue Architecture Planning.md L62800–62830 | turn 43 | version 0.15 -->
## v0.15 — 18. Dependency states

A work item can therefore be:

```
BLOCKED
```

until dependencies resolve.

Lifecycle:

```
BLOCKED
   │
   │ dependencies satisfied
   ▼
QUEUED
```

This gives a useful distinction:

```
BLOCKED ≠ QUEUED
```

A queued task can run.

A blocked task cannot.

---

<!-- source: Continue Architecture Planning.md L62832–62873 | turn 43 | version 0.15 -->
## v0.15 — 19. Work completion

A work item should produce a result, not directly mutate unrelated state.

For example:

```JavaScript
{
    workId: 'work-123',

    status: 'completed',

    result: {
        type: 'discovery',
        proposalCount: 17
    }
}
```

Then the controller consumes the result.

This preserves the architecture:

```
Executor
   ↓
WorkResult
   ↓
Controller
   ↓
State transition
```

rather than:

```
Executor
   ↓
mutates everything
```

---

<!-- source: Continue Architecture Planning.md L62875–62933 | turn 43 | version 0.15 -->
## v0.15 — 20. Work execution boundary

Define:

```JavaScript
class WorkExecutor {
    canExecute(work) {
        return false;
    }

    async execute(work, context) {
        throw new Error(
            'Not implemented'
        );
    }
}
```

Then:

```
WorkScheduler
      ↓
WorkExecutorRegistry
      ↓
DiscoveryExecutor / AcquisitionExecutor
```

For example:

```JavaScript
class DiscoveryExecutor extends WorkExecutor {
    canExecute(work) {
        return work.kind === 'discovery';
    }

    async execute(work, context) {
        return context.discoveryController
            .executeTask(work);
    }
}
```

And:

```JavaScript
class AcquisitionExecutor extends WorkExecutor {
    canExecute(work) {
        return work.kind === 'acquisition';
    }

    async execute(work, context) {
        return context.acquisitionRuntime
            .executeWork(work);
    }
}
```

---

<!-- source: Continue Architecture Planning.md L62935–62977 | turn 43 | version 0.15 -->
## v0.15 — 21. Work Runtime

The pieces now form:

```
                    ScanSession
                         │
                         ▼
                  FrontierRuntime
                         │
                         ▼
                   WorkScheduler
                         │
                         ▼
                      Claim
                         │
                         ▼
                   WorkExecutor
                    /          \
                   /            \
                  ▼              ▼
          DiscoveryExecutor  AcquisitionExecutor
                  │              │
                  ▼              ▼
        DiscoveryController  AcquisitionRuntime
```

The frontier runtime owns:

* queueing
* claiming
* leases
* cancellation
* retry metadata
* fairness
* work lifecycle

The specialized runtimes own:

* discovery semantics
* acquisition semantics

---

<!-- source: Continue Architecture Planning.md L62979–63027 | turn 43 | version 0.15 -->
## v0.15 — 22. Retry becomes generic

Previously acquisition had retry.

Now the infrastructure can represent retry for any work.

```JavaScript
{
    attempts: 2,

    retry: {
        maxAttempts: 3,
        baseDelay: 500,
        maxDelay: 8000
    },

    nextAttemptAt: 1757500100000
}
```

But the **decision to retry** should remain specialized.

For example:

```
network timeout
    → potentially retry

invalid proposal
    → don't retry

policy denied
    → don't retry

temporary provider unavailable
    → potentially retry
```

So:

```
WorkRuntime
    stores retry state

Specialized runtime
    decides retryability
```

---

<!-- source: Continue Architecture Planning.md L63029–63071 | turn 43 | version 0.15 -->
## v0.15 — 23. Retry identity

An important rule:

```
WorkItem identity
       ≠
Attempt identity
```

Example:

```
work-123
 ├── attempt-1
 ├── attempt-2
 └── attempt-3
```

This gives clean provenance:

```
    ↓
Attempt
    ↓
Execution
    ↓
Result
```

The event ledger can then distinguish:

```
work-created
attempt-started
attempt-failed
retry-scheduled
attempt-started
attempt-completed
work-completed
```

---

<!-- source: Continue Architecture Planning.md L63073–63108 | turn 43 | version 0.15 -->
## v0.15 — 24. Cancellation

Cancellation should also become work-level.

```
ScanSession.cancel()
        │
        ▼
FrontierRuntime
        │
 ┌──────┼──────────┐
 ▼      ▼          ▼
queued claimed   running
 │       │          │
cancel  cancel     cancellation token
```

Important:

```
cancelled work
```

does not mean:

```
already completed network request magically disappears
```

Cancellation is cooperative.

This keeps the earlier distinction:

> Stop admission first; then settle active operations.

---

<!-- source: Continue Architecture Planning.md L63110–63150 | turn 43 | version 0.15 -->
## v0.15 — 25. Scan termination with WorkItems

v0.14 termination can now become much more precise.

Natural completion:

```
Discovery frontier empty
AND
Acquisition frontier empty
AND
No running work
AND
No blocked work that can become eligible
```

That final condition matters.

Consider:

```
work A = blocked
depends on work B
work B = queued
```

The frontier isn't exhausted.

Therefore:

```
queued = 0
```

does not necessarily mean:

```
scan complete
```

---

<!-- source: Continue Architecture Planning.md L63152–63180 | turn 43 | version 0.15 -->
## v0.15 — 26. The three frontier states

We can now distinguish:

```
READY
  ↓
QUEUED / eligible

BLOCKED
  ↓
waiting for dependency

RUNNING
  ↓
currently executing
```

A scan is naturally complete only when:

```
READY      = 0
BLOCKED    = 0
RUNNING    = 0
```

assuming no future scheduled retry remains.

---

<!-- source: Continue Architecture Planning.md L63221–63264 | turn 43 | version 0.15 -->
## v0.15 — 28. Work state machine

```
                     ┌─────────┐
                     │ BLOCKED │
                     └────┬────┘
                          │
                    dependency ready
                          │
                          ▼
                     ┌─────────┐
                     │ QUEUED  │
                     └────┬────┘
                          │
                        claim
                          │
                          ▼
                     ┌─────────┐
                     │ CLAIMED │
                     └────┬────┘
                          │
                        start
                          │
                          ▼
                     ┌─────────┐
                     │ RUNNING │
                     └────┬────┘
                          │
            ┌─────────────┼──────────────┐
            │             │              │
            ▼             ▼              ▼
       COMPLETED       FAILED         DELAYED
                            │              │
                       retryable?         │
                            │              │
                            └──────┬───────┘
                                   ▼
                                QUEUED

Any active state ───────────────→ CANCELLED
Expired CLAIMED ────────────────→ QUEUED
```

---

<!-- source: Continue Architecture Planning.md L63266–63290 | turn 43 | version 0.15 -->
## v0.15 — 29. Domain → Session → Work

We now have a much cleaner hierarchy:

```
DiscoveryDomain
       │
       ▼
ScanSession
       │
       ▼
FrontierRuntime
       │
       ▼
WorkItem
       │
 ┌─────┴──────┐
 ▼            ▼
Discovery   Acquisition
 Work         Work
```

This gives each abstraction one job.

---

<!-- source: Continue Architecture Planning.md L63292–63312 | turn 43 | version 0.15 -->
## v0.15 — 30. What belongs where?

| Component | Responsibility |
| --- | --- |
| `DiscoveryDomain` | Defines search space |
| `ScanSession` | Defines one execution |
| `FrontierRuntime` | Owns unfinished work |
| `WorkItem` | Represents executable work |
| `WorkScheduler` | Selects work |
| `WorkLease` | Provides recoverable ownership |
| `DiscoveryController` | Governs discovery |
| `AcquisitionRuntime` | Governs acquisition |
| `CandidateSource` | Produces proposals |
| `AcquisitionProvider` | Performs I/O |
| `RecognitionRuntime` | Interprets observations |
| `KnowledgeBase` | Stores knowledge |
| `EventLedger` | Records what happened |

That is a considerably cleaner architecture than letting each subsystem implement its own mini-scheduler.

---

<!-- source: Continue Architecture Planning.md L63432–63497 | turn 43 | version 0.15 -->
## v0.15 — 34. v0.15 architectural result

The progression is now:

```
v0.6   Resource discovery engine
v0.7   Acquisition planning
v0.8   Capability model
v0.9   Acquisition providers
v0.10  Acquisition runtime
v0.11  Recognition runtime
v0.12  Candidate sources
v0.13  Discovery controller
v0.14  Discovery domain + scan session
v0.15  Work + frontier runtime
```

The system is no longer fundamentally a crawler.

It is becoming:

```
                 BOUNDED DISCOVERY RUNTIME

Domain
  ↓
Session
  ↓
Frontier
  ↓
Work
  ↓
Execution
  ↓
Observation
  ↓
Evidence
  ↓
Expansion
  ↓
New Work
```

And the DVB blind-scan analogy has now reached its useful architectural limit:

```
Unknown search space
        ↓
Bounded scan domain
        ↓
Work frontier
        ↓
Observation
        ↓
Recognition
        ↓
Expansion
        ↓
Frontier exhaustion / explicit limit
```

The next missing abstraction is **not another provider**.

It is the boundary between **observation, evidence, and knowledge**.

That leads naturally to **v0.16 — EvidenceGraph + Provenance**, where the engine stops treating a discovery merely as “a URL we found” and starts representing **why the candidate exists, what observation supports it, what recognition mechanism produced it, and how independently verified paths converge on the same resource**.

<!-- source: Continue Architecture Planning.md L84664–84685 | turn 71 | version 0.30 -->
## v0.30 — Unified Frontier Arbitration

The question becomes:

```
                FRONTIER
                   │
       ┌───────────┼───────────┐
       ▼           ▼           ▼
   discovery   acquisition   expansion
       │           │           │
       └───────────┼───────────┘
                   ▼
             arbitration
                   │
       ┌───────────┼───────────┐
       ▼           ▼           ▼
     goal       coverage      cost
    value       value         limits
```

The critical design issue will be ensuring that **adaptive prioritization can choose what to do next without becoming an authority layer that silently starves entire classes of work**.

<!-- source: Continue Architecture Planning.md L84762–84791 | turn 73 | version 0.30 -->
## v0.30 — The final conceptual separation

The architecture converged on these distinct questions:

| Layer | Question |
| --- | --- |
| **Goal** | What am I looking for? |
| **Domain** | Where am I allowed to search? |
| **Search Space** | How is that universe partitioned? |
| **Query Plan** | What search tactics should be attempted? |
| **Tactic** | What kind of exploration should occur? |
| **Strategy** | How should a region be explored? |
| **Candidate** | What might exist? |
| **Acquisition** | Can I obtain it? |
| **Observation** | What did I actually observe? |
| **Recognition** | What is the observation? |
| **Evidence** | Why do I believe that interpretation? |
| **Resource** | What logical entity does it concern? |
| **Artifact** | What exact bytes were observed? |
| **Revision** | Which observed version is this? |
| **Classification** | What kind of resource is it? |
| **Relevance** | Does it satisfy the goal? |
| **Coverage** | What part of the search space was explored? |
| **Absence** | What can legitimately be said was not found? |
| **Completeness** | What can legitimately be claimed as exhaustive? |
| **Frontier** | What remains to be done? |

That separation is the main architectural achievement.

---

<!-- source: Continue Architecture Planning.md L84910–84948 | turn 73 | version 0.30 -->
## v0.30 — The most important safety boundary

Dynamic discovery is powerful because:

```
observation → new knowledge → new search space
```

But it must never become:

```
observation → arbitrary authority
```

Therefore:

```
Discovery
   ↓
Proposal
   ↓
Validation
   ↓
Admission
   ↓
Work
```

not:

```
Discovery
   ↓
execute whatever was discovered
```

This distinction is what keeps the system from turning into an uncontrolled crawler, brute-force engine, or self-expanding executor.

---

<!-- source: Continue Architecture Planning.md L85131–85131 | turn 74 | You turn lead-in -->
V 0.30

<!-- source: Continue Architecture Planning.md L85137–85169 | turn 75 | version 0.30 -->
## v0.30 — Unified Frontier Arbitration

The next boundary is the **control problem**.

By v0.29, the frontier can contain many different kinds of work:

```
FRONTIER
├── discovery
├── acquisition
├── enumeration
├── partition expansion
├── classification
├── relevance evaluation
├── verification
└── reconciliation
```

They all compete for finite execution capacity.

The mistake would be to solve this with:

```JavaScript
queue.sort((a, b) => b.priority - a.priority)
```

That creates a priority queue, but not a robust frontier controller.

The v0.30 abstraction is:

> **Frontier arbitration decides which admissible work should execute next while preserving fairness, budgets, policy, and explainability.**

---

<!-- source: Continue Architecture Planning.md L85215–85256 | turn 75 | version 0.30 -->
## v0.30 — 30.2 WorkClass

The frontier now needs an explicit classification of work.

```JavaScript
const WorkClass = Object.freeze({
    DISCOVERY: 'discovery',
    ACQUISITION: 'acquisition',
    ENUMERATION: 'enumeration',
    PARTITION_EXPANSION: 'partition-expansion',
    CLASSIFICATION: 'classification',
    RELEVANCE: 'relevance',
    VERIFICATION: 'verification',
    RECONCILIATION: 'reconciliation'
});
```

A `WorkItem` therefore has:

```JavaScript
{
    id: "work-123",
    kind: "acquisition",
    class: "acquisition",

    sessionId: "scan-001",

    priority: 0.72,

    payload: {
        candidateId: "cand-42"
    }
}
```

`kind` describes the concrete operation.

`class` describes its scheduling category.

That distinction becomes important later.

---

<!-- source: Continue Architecture Planning.md L85258–85314 | turn 75 | version 0.30 -->
## v0.30 — 30.3 WorkClassPolicy

Each class needs a scheduling policy.

```JavaScript
class WorkClassPolicy {
    constructor(data = {}) {
        this.class = data.class;

        this.enabled = data.enabled !== false;

        this.minShare = data.minShare ?? 0;
        this.maxShare = data.maxShare ?? 1;

        this.weight = data.weight ?? 1;

        this.reservedCapacity =
            data.reservedCapacity ?? 0;

        this.maxConcurrent =
            data.maxConcurrent ?? Infinity;

        this.starvationLimitMs =
            data.starvationLimitMs ?? 30000;
    }

    serialize() {
        return { ...this };
    }
}
```

Example:

```JavaScript
[
    {
        class: 'acquisition',
        minShare: 0.20,
        weight: 3
    },
    {
        class: 'discovery',
        minShare: 0.10,
        weight: 2
    },
    {
        class: 'classification',
        minShare: 0.05,
        weight: 1
    }
]
```

These are **scheduler preferences**, not authority.

---

<!-- source: Continue Architecture Planning.md L85316–85382 | turn 75 | version 0.30 -->
## v0.30 — 30.4 ArbitrationDecision

The arbitrator should not simply return a work item.

It should produce a decision record.

```JavaScript
class ArbitrationDecision {
    constructor(data = {}) {
        this.id = data.id || makeId('arb');

        this.sessionId = data.sessionId || null;

        this.workItemId = data.workItemId || null;

        this.workClass = data.workClass || null;

        this.reason = data.reason || null;

        this.score = Number.isFinite(data.score)
            ? data.score
            : null;

        this.components = data.components || {};

        this.constraints = data.constraints || [];

        this.alternatives = data.alternatives || [];

        this.createdAt = data.createdAt || now();
    }

    serialize() {
        return { ...this };
    }
}
```

For example:

```JavaScript
{
    workItemId: "work-42",
    workClass: "acquisition",

    score: 0.83,

    components: {
        basePriority: 0.62,
        goalValue: 0.91,
        coverageValue: 0.73,
        aging: 0.18,
        costPenalty: 0.07,
        starvationBoost: 0.00
    },

    reason: "highest admissible score"
}
```

Now the question:

> Why did the engine choose this work?

has an actual answer.

---

<!-- source: Continue Architecture Planning.md L85384–85386 | turn 75 | version 0.30 -->
## v0.30 — 30.5 Hard constraints vs soft priorities

This is one of the most important v0.30 boundaries.

<!-- source: Continue Architecture Planning.md L85388–85402 | turn 75 | version 0.30 -->
### v0.30 — Hard constraints

These determine **eligibility**.

```
outside domain
policy denied
capability unavailable
budget exhausted
dependency unsatisfied
work cancelled
class disabled
```

The arbitrator cannot override them.

<!-- source: Continue Architecture Planning.md L85404–85441 | turn 75 | version 0.30 -->
### v0.30 — Soft priorities

These determine **ordering**.

```
goal relevance
base priority
coverage value
information gain
novelty
aging
cost
historical yield
class weight
```

Therefore:

```
                  WORK ITEM
                      │
                      ▼
                 ELIGIBILITY
                      │
            ┌─────────┴─────────┐
            │                   │
          DENIED              ELIGIBLE
            │                   │
            X                   ▼
                         ARBITRATION SCORE
                               │
                               ▼
                         SELECT NEXT WORK
```

A score of `1000` must not make unauthorized work executable.

---

<!-- source: Continue Architecture Planning.md L85443–85480 | turn 75 | version 0.30 -->
## v0.30 — 30.6 Arbitration score

A conceptual scoring function:

```
Score(w) =
    BasePriority(w)
  + GoalValue(w)
  + CoverageValue(w)
  + InformationGain(w)
  + Novelty(w)
  + Aging(w)
  + StarvationBoost(w)
  - CostPenalty(w)
  - FailurePenalty(w)
```

But the score is only evaluated **after admission**.

```
Eligible(w)
    ↓
Score(w)
```

Never:

```
Score(w)
    ↓
therefore
    ↓
Eligible(w)
```

This preserves the authority boundary established in earlier versions.

---

<!-- source: Continue Architecture Planning.md L85482–85531 | turn 75 | version 0.30 -->
## v0.30 — 30.7 Aging

Pure priority produces starvation.

Example:

```
HIGH PRIORITY
HIGH PRIORITY
HIGH PRIORITY
HIGH PRIORITY
HIGH PRIORITY
...
```

A low-priority classification task may never run.

Aging solves this:

```JavaScript
function agingScore(work, nowMs) {
    if (!work.queuedAt) return 0;

    const waited = Math.max(
        0,
        nowMs - work.queuedAt
    );

    return Math.min(
        1,
        waited / 30000
    );
}
```

Conceptually:

```
waiting time ↑
     │
     ▼
aging score ↑
     │
     ▼
eventual selection
```

Aging is therefore a fairness mechanism rather than a relevance mechanism.

---

<!-- source: Continue Architecture Planning.md L85533–85579 | turn 75 | version 0.30 -->
## v0.30 — 30.8 Starvation detection

Aging alone is not enough.

The system should explicitly detect starvation.

```JavaScript
class StarvationDetector {
    constructor(limitMs = 30000) {
        this.limitMs = limitMs;
    }

    isStarved(work, nowMs = Date.now()) {
        if (work.status !== 'queued') {
            return false;
        }

        if (!work.queuedAt) {
            return false;
        }

        return (
            nowMs - work.queuedAt >=
            this.limitMs
        );
    }
}
```

A starved item receives a fairness boost.

```
NORMAL
  │
  │ waiting
  ▼
AGING
  │
  │ threshold exceeded
  ▼
STARVED
  │
  ▼
PRIORITY BOOST
```

---

<!-- source: Continue Architecture Planning.md L85581–85625 | turn 75 | version 0.30 -->
## v0.30 — 30.9 Class starvation

Individual starvation is only half the problem.

An entire work class can starve.

For example:

```
acquisition:     92%
discovery:        7%
classification:   1%
```

If this persists, classification may effectively disappear from the system.

Therefore track:

```JavaScript
class FrontierClassStats {
    constructor() {
        this.queued = 0;
        this.running = 0;
        this.completed = 0;

        this.waitTimeMs = 0;
        this.maxWaitTimeMs = 0;

        this.selected = 0;
        this.skipped = 0;

        this.starved = 0;
    }
}
```

The arbitrator therefore sees both:

```
individual fairness
+
class fairness
```

---

<!-- source: Continue Architecture Planning.md L85627–85656 | turn 75 | version 0.30 -->
## v0.30 — 30.10 Weighted fairness

A useful baseline is weighted fair scheduling.

```
class              weight

acquisition          4
discovery            3
enumeration          3
verification         2
classification      1
relevance            1
reconciliation       1
```

This does **not** mean:

```
4 acquisitions
3 discoveries
3 enumerations
...
```

because actual work availability changes dynamically.

Instead, weights influence the long-run allocation.

---

<!-- source: Continue Architecture Planning.md L85658–85704 | turn 75 | version 0.30 -->
## v0.30 — 30.11 Deficit-style arbitration

A stronger model is deficit-based scheduling.

Each work class receives a deficit counter:

```JavaScript
class ArbitrationBucket {
    constructor(workClass, weight = 1) {
        this.workClass = workClass;
        this.weight = weight;
        this.deficit = 0;
    }

    accrue(quantum) {
        this.deficit +=
            this.weight * quantum;
    }

    consume(cost) {
        this.deficit -= cost;
    }
}
```

Conceptually:

```
                 ┌─────────────┐
                 │ acquisition │ +4
                 └──────┬──────┘
                        │
                 ┌──────▼──────┐
                 │ discovery   │ +3
                 └──────┬──────┘
                        │
                 ┌──────▼──────┐
                 │ enumeration │ +3
                 └──────┬──────┘
                        │
                        ▼
                    arbitration
```

This makes scheduling less sensitive to the instantaneous queue ordering.

---

<!-- source: Continue Architecture Planning.md L85706–85759 | turn 75 | version 0.30 -->
## v0.30 — 30.12 Cost-aware scheduling

Not all work costs the same.

For example:

```
HTML recognition       cheap
JSON parsing            cheap
PDF download            expensive
large enumeration       expensive
WASM verification       medium
remote acquisition      expensive
```

Work can carry an estimated cost:

```JavaScript
{
    estimatedCost: {
        requests: 1,
        bytes: 2500000,
        cpuMs: 120,
        wallMs: 900
    }
}
```

The scheduler can prefer:

```
high expected value
+
low expected cost
```

rather than simply:

```
highest priority
```

A useful conceptual metric:

```
utility =
    expectedValue / max(expectedCost, ε)
```

But estimates are not facts.

The actual outcome must later update the model.

---

<!-- source: Continue Architecture Planning.md L85761–85818 | turn 75 | version 0.30 -->
## v0.30 — 30.13 Backpressure

Suppose discovery produces candidates faster than acquisition can consume them:

```
Discovery
   │
   │ +1000 candidates
   ▼
┌──────────────┐
│ acquisition  │
│ queue        │
└──────────────┘
   │
   │ only 4/sec
   ▼
    backlog
```

Without backpressure:

```
candidate explosion
       ↓
memory growth
       ↓
storage pressure
       ↓
scheduler degradation
```

Therefore the frontier needs admission pressure.

```
Discovery production
        │
        ▼
Frontier pressure
        │
        ├── normal
        ├── elevated
        ├── high
        └── saturated
```

A discovery task may then be delayed even though it is otherwise valid.

Important:

```
backpressure ≠ policy denial
```

It means:

> valid work cannot currently be admitted because downstream capacity is constrained.

---

<!-- source: Continue Architecture Planning.md L85820–85854 | turn 75 | version 0.30 -->
## v0.30 — 30.14 Reserved capacity

One way to prevent monopolization is to reserve capacity.

Example:

```
Global concurrency = 8

Reserved:
    acquisition      2
    discovery        1
    enumeration      1

Shared:
    4
```

Thus a flood of acquisition work cannot consume every execution slot.

```
┌──────────────────────────────┐
│         8 slots              │
├────────┬───────┬─────────────┤
│ Acq    │ Disc  │ Enumeration  │
│ 2      │ 1     │ 1            │
├────────┴───────┴─────────────┤
│       Shared capacity        │
│              4               │
└──────────────────────────────┘
```

Reserved capacity provides a stronger non-starvation guarantee than priority aging alone.

---

<!-- source: Continue Architecture Planning.md L85856–85909 | turn 75 | version 0.30 -->
## v0.30 — 30.15 Arbitration pipeline

The complete decision path becomes:

```
WorkItem
   │
   ▼
Dependency Check
   │
   ▼
Domain Check
   │
   ▼
Capability Check
   │
   ▼
Policy Check
   │
   ▼
Budget Check
   │
   ▼
Backpressure Check
   │
   ▼
Eligible Set
   │
   ▼
Class Fairness
   │
   ▼
Aging
   │
   ▼
Goal / Coverage / Information Value
   │
   ▼
Cost / Failure Penalties
   │
   ▼
Arbitration
   │
   ▼
ArbitrationDecision
   │
   ▼
Atomic Claim
   │
   ▼
Execution
```

---

<!-- source: Continue Architecture Planning.md L85911–85957 | turn 75 | version 0.30 -->
## v0.30 — 30.16 The atomicity problem

There is an important race:

```
Worker A sees work-42
Worker B sees work-42

A: "best candidate"
B: "best candidate"

A claims
B claims
```

Therefore:

```
ARBITRATE
    ↓
CLAIM
```

must be treated as one logical scheduling transaction.

The scheduler must not assume:

```
selected ⇒ successfully claimed
```

Instead:

```
selected
   ↓
claim attempted
   ↓
┌─────────────┬─────────────┐
│ success     │ conflict    │
▼             ▼
execute       discard/retry
```

This becomes particularly important if the userscript eventually supports multiple workers/tabs.

---

<!-- source: Continue Architecture Planning.md L85959–85997 | turn 75 | version 0.30 -->
## v0.30 — 30.17 Priority inversion

Another failure mode:

```
Work A
high priority
depends on Work B

Work B
low priority
```

If B is never selected:

```
A blocked forever
```

Therefore dependency-aware arbitration must propagate urgency.

Conceptually:

```
A high priority
    │
    │ depends on
    ▼
B low priority
    │
    ▼
B receives dependency boost
```

But:

> Dependency priority propagation must not override policy or capability constraints.

---

<!-- source: Continue Architecture Planning.md L85999–86050 | turn 75 | version 0.30 -->
## v0.30 — 30.18 FrontierArbitrator

The central interface:

```JavaScript
class FrontierArbitrator {
    constructor(config = {}) {
        this.classPolicies =
            new Map();

        this.buckets =
            new Map();

        this.now =
            config.now || (() => Date.now());
    }

    admit(work, context) {
        return {
            allowed: false,
            reason: 'not-implemented'
        };
    }

    score(work, context) {
        return {
            score: 0,
            components: {}
        };
    }

    select(workItems, context) {
        return {
            workItem: null,
            decision: null
        };
    }

    describe() {
        return {
            id: 'frontier-arbitrator',
            name: 'Unified Frontier Arbitrator'
        };
    }
}
```

The key point is that the arbitrator **does not execute work**.

It selects work.

---

<!-- source: Continue Architecture Planning.md L86052–86090 | turn 75 | version 0.30 -->
## v0.30 — 30.19 Arbitration result

A complete result might look like:

```JavaScript
{
    workItemId: "work-781",

    eligible: true,

    score: 0.87,

    components: {
        basePriority: 0.70,
        goalValue: 0.91,
        coverageValue: 0.82,
        informationGain: 0.61,
        novelty: 0.40,
        aging: 0.23,
        starvationBoost: 0.00,
        costPenalty: 0.08,
        failurePenalty: 0.02
    },

    fairness: {
        workClass: "enumeration",
        classShare: 0.18,
        targetShare: 0.25,
        deficit: 0.07
    },

    reason:
        "eligible; high goal value; class under target share"
}
```

This is operational provenance.

---

<!-- source: Continue Architecture Planning.md L86092–86119 | turn 75 | version 0.30 -->
## v0.30 — 30.20 Arbitration ledger

Add events:

```
work-eligible
work-ineligible
work-class-selected
work-starvation-detected
work-fairness-boosted
work-score-calculated
work-selected
work-claim-conflict
work-claim-succeeded
work-backpressured
work-dependency-blocked
work-budget-blocked
```

Now the engine can answer:

> Why didn't you process this candidate?

Not merely:

> It was somewhere in the queue.

---

<!-- source: Continue Architecture Planning.md L86121–86172 | turn 75 | version 0.30 -->
## v0.30 — 30.21 Replay

Arbitration must be replayable.

Therefore avoid:

```JavaScript
Math.random()
```

inside scheduling.

Instead:

```JavaScript
ArbitrationContext {
    sessionId,
    frontierSnapshotId,
    policyVersion,
    arbitratorVersion,
    timestamp,
    deterministicSeed
}
```

A replay can then reconstruct:

```
same frontier
+
same policy
+
same weights
+
same history
+
same seed
=
same arbitration decision
```

Live execution may differ because external observations differ.

So distinguish:

```
decision replay
≠
network replay
```

---
