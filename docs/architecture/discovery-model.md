# Discovery Model

> **Status:** DESIGNED
>
> **Source:** `Continue Architecture Planning.md`; `Userscript Discovery Prototype.md`
>
> **Purpose:** What counts as a discovery: discovery graphs, discovery tasks, discovery control, confidence and evidence levels.

## Contents

- **10. Confidence rather than binary decisions** — `Userscript Discovery Prototype.md` L529–571
- *Turn lead-in* — `Userscript Discovery Prototype.md` L787–787
- **16. Discovery should have evidence levels** — `Userscript Discovery Prototype.md` L789–823
- *Turn lead-in* — `Userscript Discovery Prototype.md` L1111–1111
- **24. Two-dimensional discovery** — `Userscript Discovery Prototype.md` L1113–1145
- **26. Discovery becomes a graph** — `Userscript Discovery Prototype.md` L1208–1245
- **Discovery** — `Userscript Discovery Prototype.md` L1528–1545
- **v0.7.0 — Discovery Graph + Acquisition Planner** — `Continue Architecture Planning.md` L48388–48457
- **v0.7 objectives** — `Continue Architecture Planning.md` L48459–48492
- **v0.7 — Core contract** — `Continue Architecture Planning.md` L48494–48659
- **v0.7 — Important v0.7 distinction** — `Continue Architecture Planning.md` L48661–48720
- **v0.7 state machine** — `Continue Architecture Planning.md` L48722–48800
- **v0.13 — Discovery Controller** — `Continue Architecture Planning.md` L59472–59493
- **v0.13 — 3. DiscoveryTask** — `Continue Architecture Planning.md` L59598–59653
- **v0.13 — 4. Why a task is necessary** — `Continue Architecture Planning.md` L59655–59699
- **v0.13 — 5. Source Policy** — `Continue Architecture Planning.md` L59701–59750
- **v0.13 — 6. Source budgets** — `Continue Architecture Planning.md` L59752–59783
- **v0.13 — 7. Proposal budget is different** — `Continue Architecture Planning.md` L59785–59826
- **v0.13 — 8. Incremental sources** — `Continue Architecture Planning.md` L59828–59867
- **v0.13 — 9. Source execution contract** — `Continue Architecture Planning.md` L59869–59912
- **v0.13 — 16. DiscoveryController** — `Continue Architecture Planning.md` L60168–60208
- **v0.13 — 17. Event ledger** — `Continue Architecture Planning.md` L60210–60258
- **v0.14 — Discovery Engine** — `Continue Architecture Planning.md` L60612–60627
- **v0.14 — 8. Discovery frontier** — `Continue Architecture Planning.md` L60974–61037
- **v0.16 — 28. Discovery confidence changes meaning** — `Continue Architecture Planning.md` L64721–64756
- **v0.16 — Discovery** — `Continue Architecture Planning.md` L65192–65196

## Related Documents

- [Candidate Model](candidate-model.md)
- [Evidence Model](evidence-model.md)
- [Provenance](provenance.md)
- [Response Recognition](../acquisition/response-recognition.md)

---

<!-- source: Userscript Discovery Prototype.md L529–571 | turn 5 | version ? -->
## 10. Confidence rather than binary decisions

Instead of immediately saying:

```
found / not found
```

maintain a confidence score.

For example:

```
CandidateConfidence {
    energy_score
    timing_score
    carrier_score
    synchronization_score
    FEC_score
    transport_score
    metadata_score
}
```

Then define stages:

```
confidence < T1
    → ignore

T1 ≤ confidence < T2
    → investigate

T2 ≤ confidence < T3
    → demodulate

confidence ≥ T3
    → confirmed
```

This is particularly useful near weak signals, where a single measurement may be ambiguous.

---

<!-- source: Userscript Discovery Prototype.md L787–787 | turn 7 | ChatGPT turn lead-in -->
The natural next step is to define **what constitutes a successful discovery** and how the algorithm terminates. This is where a blind scanner becomes deterministic enough to implement.

<!-- source: Userscript Discovery Prototype.md L789–823 | turn 7 | version ? -->
### 16. Discovery should have evidence levels

Rather than treating discovery as a single event, attach evidence to it:

```
EvidenceLevel 0
    no signal

EvidenceLevel 1
    RF energy detected

EvidenceLevel 2
    physical-layer synchronization

EvidenceLevel 3
    valid transport stream

EvidenceLevel 4
    DVB PSI/SI validated

EvidenceLevel 5
    one or more services enumerated
```

A scanner can report only level 4/5 as a real DVB discovery, while retaining lower-level observations for diagnostics.

This gives you a useful distinction between:

> "There appears to be a carrier here."

and:

> "There is a confirmed DVB multiplex here containing these services."

---

<!-- source: Userscript Discovery Prototype.md L1111–1111 | turn 9 | ChatGPT turn lead-in -->
There is one more useful abstraction: **separate “where to look” from “how to recognize what you found.”** That lets the same discovery engine work with different tuners, demodulators, and protocols.

<!-- source: Userscript Discovery Prototype.md L1113–1145 | turn 9 | version ? -->
## 24. Two-dimensional discovery

Think of the problem as:

$$\text{Discovery} = \text{Search Strategy} + \text{Recognition Strategy}$$

The search strategy answers:

> Which candidate should I investigate next?

The recognition strategy answers:

> What evidence would convince me that this candidate contains something meaningful?

For DVB:

```
             Discovery Engine
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
 Search Strategy          Recognition Strategy
        │                       │
 frequency              RF detection
 bandwidth              synchronization
 symbol rate            FEC
 modulation             transport stream
                        PSI/SI
```

That distinction makes the architecture much cleaner.

---

<!-- source: Userscript Discovery Prototype.md L1208–1245 | turn 9 | version ? -->
## 26. Discovery becomes a graph

Once you preserve those relationships, the scan naturally forms a graph:

```
                 Network A
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
        TS 1       TS 2       TS 3
          │          │
       services   services
          │
          ▼
    RF observation
```

But there can also be discovery edges:

```
RF observation
      │
      └──► candidate
                │
                └──► multiplex
```

and metadata-derived edges:

```
Multiplex A
      │
      └── NIT ──► Multiplex B
```

So the scanner is effectively constructing a **knowledge graph of the RF environment**.

---

<!-- source: Userscript Discovery Prototype.md L1528–1545 | turn 11 | version ? -->
### Discovery

A discovery is the normalized result:

```
Discovery {
    identity
    protocol
    physical_parameters
    logical_parameters
    services
    evidence
}
```

The discovery should be independent of the particular tuner API that produced it.

---

<!-- source: Continue Architecture Planning.md L48388–48457 | turn 25 | version 0.7 -->
## v0.7.0 — Discovery Graph + Acquisition Planner

The next step should **not** be “add more URL extractors.”

v0.6 already has enough discovery mechanisms. The architectural gap is that the engine still mixes:

```
DISCOVERY
    ↓
CANDIDATE
    ↓
SCHEDULER
    ↓
ACQUISITION
```

A more faithful generic blind-scan architecture needs an explicit **planning boundary**:

```
                    ┌─────────────────────┐
                    │      DISCOVERY      │
                    │                     │
                    │ HTML / JSON / XML   │
                    │ DOM / Network / CSS │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   KNOWLEDGE GRAPH   │
                    │                     │
                    │ resource            │
                    │ provenance          │
                    │ evidence            │
                    │ observations        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ ACQUISITION PLANNER │
                    │                     │
                    │ policy              │
                    │ method              │
                    │ origin budget       │
                    │ priority            │
                    │ deduplication       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     SCHEDULER       │
                    │                     │
                    │ claim → execute     │
                    │ retry → backoff     │
                    │ adaptive concurrency│
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     ACQUISITION     │
                    │                     │
                    │ GET / observe       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    OBSERVATION      │
                    └──────────┬──────────┘
                               │
                               └──────► DISCOVERY
```

<!-- source: Continue Architecture Planning.md L48459–48492 | turn 25 | version 0.7 -->
### v0.7 objectives

1. **Candidate ≠ acquisition request**
2. Introduce an explicit `AcquisitionPlan`.
3. Make HTTP method part of the candidate contract.
4. Never infer that a discovered URL should be fetched merely because it exists.
5. Make policy decisions observable.
6. Make scheduler decisions deterministic enough to replay.
7. Separate **resource identity** from **candidate identity**.
8. Treat network-observed POST/PUT/etc. as evidence, never as executable work.
9. Add a proper `SKIPPED_POLICY`, `SKIPPED_BUDGET`, and `SKIPPED_DUPLICATE` state.
10. Make the graph the authoritative source of what is known.

The critical new object is:

```
Candidate
   │
   │ evaluate
   ▼
AcquisitionPlan
   │
   ├── allowed
   ├── method
   ├── reason
   ├── priority
   ├── origin
   ├── expectedType
   ├── retryPolicy
   └── budget requirements
          │
          ▼
      Scheduler
```

<!-- source: Continue Architecture Planning.md L48494–48659 | turn 25 | version 0.7 -->
### v0.7 — Core contract

```JavaScript
class AcquisitionPlan {
    constructor(data = {}) {
        this.id = data.id || makeId('plan');

        this.candidateId =
            data.candidateId || null;

        this.target =
            data.target || '';

        this.method =
            String(data.method || 'GET').toUpperCase();

        this.allowed =
            Boolean(data.allowed);

        this.reason =
            data.reason || null;

        this.priority =
            Number.isFinite(data.priority)
                ? data.priority
                : 0;

        this.origin =
            data.origin || originOf(this.target);

        this.expectedType =
            data.expectedType || 'unknown';

        this.requiresOriginSlot =
            data.requiresOriginSlot !== false;

        this.createdAt =
            data.createdAt || now();
    }

    serialize() {
        return { ...this };
    }
}
```

Then replace the current policy result:

```JavaScript
{
    acquire: true,
    reason: null
}
```

with a real plan:

```JavaScript
class AcquisitionPolicy {
    plan(candidate) {
        const method =
            String(
                candidate.hints.method || 'GET'
            ).toUpperCase();

        if (method !== 'GET') {
            return new AcquisitionPlan({
                candidateId: candidate.id,
                target: candidate.target,
                method,
                allowed: false,
                reason: 'non-get-method',
                priority: candidate.effectivePriority()
            });
        }

        if (candidate.type === 'form') {
            return new AcquisitionPlan({
                candidateId: candidate.id,
                target: candidate.target,
                method,
                allowed: false,
                reason: 'forms-disabled',
                priority: candidate.effectivePriority()
            });
        }

        if (
            candidate.type === 'media' &&
            !CONFIG.policy.acquireMedia
        ) {
            return new AcquisitionPlan({
                candidateId: candidate.id,
                target: candidate.target,
                method,
                allowed: false,
                reason: 'media-disabled',
                priority: candidate.effectivePriority()
            });
        }

        const contentType =
            candidate.hints.contentType ||
            contentTypeForTarget(candidate.target);

        if (
            isBinaryContentType(contentType) &&
            !CONFIG.policy.acquireBinaryResources
        ) {
            return new AcquisitionPlan({
                candidateId: candidate.id,
                target: candidate.target,
                method,
                allowed: false,
                reason: 'binary-disabled',
                priority: candidate.effectivePriority()
            });
        }

        return new AcquisitionPlan({
            candidateId: candidate.id,
            target: candidate.target,
            method: 'GET',
            allowed: true,
            priority: candidate.effectivePriority(),
            expectedType: candidate.type
        });
    }
}
```

The worker then becomes conceptually much cleaner:

```JavaScript
const candidate =
    this.db.claimNextCandidate();

if (!candidate) {
    // no work currently available
    ...
}

const plan =
    this.policy.plan(candidate);

this.db.recordDiagnostic(
    'acquisition-plan',
    plan.serialize()
);

if (!plan.allowed) {
    this.db.markSkipped(
        candidate,
        plan.reason
    );

    continue;
}

if (!this.reserveRequestSlot()) {
    this.db.requeue(candidate);
    break;
}

await this.executePlan(plan);
```

<!-- source: Continue Architecture Planning.md L48661–48720 | turn 25 | version 0.7 -->
### v0.7 — Important v0.7 distinction

A network observation such as:

```
POST /api/order
```

creates:

```
RESOURCE
  /api/order

OBSERVATION
  method = POST

EVIDENCE
  browser actually performed POST
```

but **does not create**:

```
ACQUISITION PLAN
  GET /api/order
```

automatically.

Likewise:

```
<form action="/delete" method="POST">
```

produces knowledge:

```
/form → endpoint → /delete
method = POST
```

but no executable request.

That gives the engine a much stronger invariant:

```
DISCOVERED
   ≠
AUTHORIZED
   ≠
SCHEDULED
   ≠
EXECUTED
```

This is the key architectural transition.

---

<!-- source: Continue Architecture Planning.md L48722–48800 | turn 25 | version 0.7 -->
## v0.7 state machine

The candidate lifecycle should also become explicit:

```
                 ┌─────────────┐
                 │ DISCOVERED  │
                 └──────┬──────┘
                        │
                        ▼
                 ┌─────────────┐
                 │   QUEUED    │
                 └──────┬──────┘
                        │
                        ▼
                 ┌─────────────┐
                 │   CLAIMED   │
                 └──────┬──────┘
                        │
                  policy.plan()
                        │
             ┌──────────┴──────────┐
             │                     │
             ▼                     ▼
      ┌─────────────┐       ┌──────────────┐
      │   PLANNED   │       │    SKIPPED   │
      └──────┬──────┘       └──────────────┘
             │
       budget/slots
             │
             ▼
      ┌─────────────┐
      │  ACQUIRING  │
      └──────┬──────┘
             │
             ▼
      ┌─────────────┐
      │  OBSERVED   │
      └──────┬──────┘
             │
             ▼
      ┌─────────────┐
      │ RECOGNIZED  │
      └──────┬──────┘
             │
             ▼
      ┌─────────────┐
      │  EXPANDED   │
      └──────┬──────┘
             │
             ▼
      ┌─────────────┐
      │  COMPLETED  │
      └─────────────┘

             acquisition failure
                    │
                    ▼
             ┌─────────────┐
             │    RETRY    │
             └──────┬──────┘
                    │
                    └──────► QUEUED
```

And terminal policy states should carry their reason:

```
SKIPPED
 ├── forms-disabled
 ├── media-disabled
 ├── binary-disabled
 ├── non-get-method
 ├── origin-budget
 ├── global-budget
 └── duplicate
```

---

<!-- source: Continue Architecture Planning.md L59472–59493 | turn 39 | version 0.13 -->
## v0.13 — Discovery Controller

v0.12 separated **where candidates come from** from the rest of the pipeline.

The remaining problem is orchestration.

Without a controller, each `CandidateSource` risks becoming an independent mini-crawler:

```
HTML source ──────┐
Network source ───┤
Sitemap source ───┤
Metadata source ──┤──→ uncontrolled proposal generation
Mutation source ──┤
User source ──────┘
```

v0.13 introduces the **Discovery Controller**.

> **Candidate sources generate proposals. The Discovery Controller governs proposal generation.**

---

<!-- source: Continue Architecture Planning.md L59598–59653 | turn 39 | version 0.13 -->
## v0.13 — 3. DiscoveryTask

We need an explicit unit of source work.

```JavaScript
class DiscoveryTask {
    constructor(data = {}) {
        this.id = data.id || makeId('dtask');

        this.sourceId =
            data.sourceId || null;

        this.observationId =
            data.observationId || null;

        this.parentCandidateId =
            data.parentCandidateId || null;

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

        this.createdAt =
            data.createdAt || now();
    }

    serialize() {
        return { ...this };
    }
}
```

Now:

```
Observation
    ↓
DiscoveryTask
    ↓
CandidateSource
    ↓
Proposal[]
```

The source itself does not need to know when it should run.

---

<!-- source: Continue Architecture Planning.md L59655–59699 | turn 39 | version 0.13 -->
## v0.13 — 4. Why a task is necessary

Without a task:

```
Observation
    ↓
run every source immediately
```

Suppose there are:

```
10 recognition providers
15 candidate sources
100 observations
```

That can become:

```
100 × 15 = 1500 source executions
```

before any meaningful scheduling exists.

With tasks:

```
Observation
    ↓
eligible sources
    ↓
tasks
    ↓
budget
    ↓
scheduler
    ↓
execution
```

Discovery itself becomes bounded.

---

<!-- source: Continue Architecture Planning.md L59701–59750 | turn 39 | version 0.13 -->
## v0.13 — 5. Source Policy

A source needs an explicit policy boundary.

```JavaScript
class DiscoverySourcePolicy {
    constructor(config = {}) {
        this.enabled =
            config.enabled !== false;

        this.maxDepth =
            config.maxDepth ?? 5;

        this.maxTasks =
            config.maxTasks ?? 1000;
    }

    allow(task) {
        if (!this.enabled) {
            return {
                allowed: false,
                reason: 'discovery-disabled'
            };
        }

        if (task.depth > this.maxDepth) {
            return {
                allowed: false,
                reason: 'discovery-depth-limit'
            };
        }

        return {
            allowed: true
        };
    }
}
```

This is deliberately separate from acquisition policy.

```
AcquisitionPolicy
    → controls resource acquisition

DiscoverySourcePolicy
    → controls candidate generation
```

---

<!-- source: Continue Architecture Planning.md L59752–59783 | turn 39 | version 0.13 -->
## v0.13 — 6. Source budgets

The controller should support both global and per-source budgets.

```
Global discovery budget
        │
        ├── HTML source
        ├── Network source
        ├── Sitemap source
        ├── Metadata source
        └── Mutation source
```

Example:

```JavaScript
{
    maxDiscoveryTasks: 1000,

    sourceBudgets: {
        'html-link': 300,
        'network': 200,
        'sitemap': 200,
        'metadata': 100
    }
}
```

This prevents a single source from consuming the entire scan.

---

<!-- source: Continue Architecture Planning.md L59785–59826 | turn 39 | version 0.13 -->
## v0.13 — 7. Proposal budget is different

There are actually two separate quantities:

```
Tasks
    = how many source executions?

Proposals
    = how many candidates did those executions produce?
```

For example:

```
1 sitemap task
    ↓
50,000 URLs
```

One task could therefore overwhelm the candidate system.

So v0.13 needs:

```JavaScript
maxProposalsPerTask
maxTotalProposals
```

Example:

```
sitemap task
    ↓
50,000 entries
    ↓
proposal cap = 500
```

The rest are not necessarily discarded forever; the source can eventually become **incremental**.

---

<!-- source: Continue Architecture Planning.md L59828–59867 | turn 39 | version 0.13 -->
## v0.13 — 8. Incremental sources

This exposes an important future interface.

A source should ideally support:

```JavaScript
discover(context)
```

but large sources eventually need:

```JavaScript
discoverBatch(context, cursor)
```

Example:

```
Sitemap
   │
   ├── batch 1 → 500 URLs
   ├── batch 2 → 500 URLs
   ├── batch 3 → 500 URLs
   └── ...
```

The controller owns the cursor.

```JavaScript
{
    sourceId: 'sitemap',
    cursor: 'opaque-source-cursor',
    status: 'paused'
}
```

This is much safer than allowing a provider to dump an unbounded result set into memory.

---

<!-- source: Continue Architecture Planning.md L59869–59912 | turn 39 | version 0.13 -->
## v0.13 — 9. Source execution contract

A more mature interface becomes:

```JavaScript
class CandidateSource {
    describe() {
        return {
            id: 'unknown-source',
            priority: 0
        };
    }

    canDiscover(context) {
        return true;
    }

    discover(context) {
        return {
            proposals: []
        };
    }
}
```

Later:

```JavaScript
discoverBatch(context, cursor)
```

can be optional.

The controller can therefore support both:

```
simple source
    → discover()

streaming source
    → discoverBatch()
```

---

<!-- source: Continue Architecture Planning.md L60168–60208 | turn 39 | version 0.13 -->
## v0.13 — 16. DiscoveryController

Conceptually:

```JavaScript
class DiscoveryController {
    constructor(options = {}) {
        this.registry =
            options.registry;

        this.policy =
            options.policy;

        this.scheduler =
            options.scheduler;

        this.normalizer =
            options.normalizer;

        this.database =
            options.database;
    }

    schedule(observation, context) {
        // Determine eligible sources.
        // Create DiscoveryTasks.
    }

    async execute(task) {
        // Claim.
        // Policy.
        // Execute source.
        // Normalize proposals.
        // Commit candidates.
    }
}
```

The controller becomes the sole owner of the discovery loop.

---

<!-- source: Continue Architecture Planning.md L60210–60258 | turn 39 | version 0.13 -->
## v0.13 — 17. Event ledger

v0.13 adds:

```
discovery-task-created
discovery-task-claimed
discovery-task-denied
discovery-task-started
discovery-task-completed
discovery-task-failed

proposal-produced
proposal-rejected
proposal-normalized

candidate-created
candidate-merged
candidate-provenance-added

source-budget-reserved
source-budget-exhausted
```

Now the causal chain can be reconstructed:

```
obs-91
 │
 ├── task-201 html-link
 │      └── proposal-301
 │             └── cand-401
 │
 ├── task-202 metadata
 │      └── proposal-302
 │             └── cand-401 merged
 │
 └── task-203 network
        └── proposal-303
               └── cand-402
```

That is substantially more useful than simply recording:

```
"found 2 URLs"
```

---

<!-- source: Continue Architecture Planning.md L60612–60627 | turn 41 | version 0.14 -->
### v0.14 — Discovery Engine

The engine contains mechanisms:

* candidate normalization
* source registry
* discovery controller
* acquisition runtime
* recognition runtime
* schedulers
* budgets
* policies
* knowledge graph
* event ledger

It should be reusable across scans.

<!-- source: Continue Architecture Planning.md L60974–61037 | turn 41 | version 0.14 -->
## v0.14 — 8. Discovery frontier

Now we can introduce the central scan concept:

```
FRONTIER
```

The frontier is the set of currently discovered but not yet fully explored work.

For discovery:

```
Discovery Frontier
    =
    DiscoveryTasks that are eligible for execution
```

For acquisition:

```
Acquisition Frontier
    =
    Candidates eligible for acquisition
```

The overall scan therefore looks like:

```
             ┌──────────────────────┐
             │    DISCOVERY DOMAIN  │
             └──────────┬───────────┘
                        │
                       Seeds
                        │
                        ▼
                ┌───────────────┐
                │   Candidates  │
                └───────┬───────┘
                        │
                     Acquire
                        │
                        ▼
                  Observations
                        │
                    Recognize
                        │
                        ▼
                    Evidence
                        │
                   Discover
                        │
                        ▼
              New Discovery Tasks
                        │
                        └──────────────┐
                                       │
                                       ▼
                                   Frontier
```

This gives us a genuine exploration process.

---

<!-- source: Continue Architecture Planning.md L64721–64756 | turn 45 | version 0.16 -->
## v0.16 — 28. Discovery confidence changes meaning

Earlier we had:

```JavaScript
confidence: 0.95
```

for proposals.

With v0.16, confidence should be treated more carefully.

Instead of:

```
candidate confidence = 0.95
```

we can store:

```
Evidence:
  kind = html-link
  confidence = 0.95
```

and separately:

```
Claim:
  support = [evidence-1, evidence-7]
```

This preserves the reasons behind the assessment.

---

<!-- source: Continue Architecture Planning.md L65192–65196 | turn 45 | version 0.16 -->
### v0.16 — Discovery

> What new possibilities were found?

`CandidateSource`
