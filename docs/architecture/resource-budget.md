# Resource and Cost Ledger

> **Status:** DESIGNED
>
> **Source:** `Continue Architecture Planning.md`
>
> **Purpose:** Resource dimensions, budgets, reservations, cost observation and settlement.

## Contents

- **v0.31 — Unified Resource & Cost Ledger** — `Continue Architecture Planning.md` L86478–86517
- **v0.31 — 31.1 Resource dimensions** — `Continue Architecture Planning.md` L86519–86576
- **v0.31 — 31.2 ResourceBudget** — `Continue Architecture Planning.md` L86578–86627
- **v0.31 — 31.3 Three resource states** — `Continue Architecture Planning.md` L86629–86672
- **v0.31 — 31.4 ResourceReservation** — `Continue Architecture Planning.md` L86674–86734
- **v0.31 — 31.5 Estimated cost vs actual cost** — `Continue Architecture Planning.md` L86736–86789
- **v0.31 — 31.6 CostObservation** — `Continue Architecture Planning.md` L86791–86844
- **v0.31 — 31.7 ResourceLedger** — `Continue Architecture Planning.md` L86846–86879
- **v0.31 — 31.8 Budget scopes** — `Continue Architecture Planning.md` L86881–86933
- **v0.31 — 31.9 Hierarchical budget accounting** — `Continue Architecture Planning.md` L86935–86974
- **v0.31 — 31.10 Resource allocation** — `Continue Architecture Planning.md` L86976–87027
- **v0.31 — 31.11 Allocation is not execution** — `Continue Architecture Planning.md` L87029–87055
- **v0.31 — 31.12 Partial consumption** — `Continue Architecture Planning.md` L87057–87102
- **v0.31 — 31.13 Cost overruns** — `Continue Architecture Planning.md` L87104–87146
- **v0.31 — 31.14 Cost model** — `Continue Architecture Planning.md` L87148–87205
- **v0.31 — 31.15 Cost is context-dependent** — `Continue Architecture Planning.md` L87207–87242
- **v0.31 — 31.16 Resource exhaustion** — `Continue Architecture Planning.md` L87244–87286
- **v0.31 — 31.17 Budget exhaustion vs frontier exhaustion** — `Continue Architecture Planning.md` L87288–87323
- **v0.31 — 31.18 Resource reservation race** — `Continue Architecture Planning.md` L87325–87363
- **v0.31 — 31.19 Settlement** — `Continue Architecture Planning.md` L87365–87415
- **v0.31 — 31.20 Cost feedback** — `Continue Architecture Planning.md` L87417–87459
- **v0.31 — 31.21 ResourceLedger events** — `Continue Architecture Planning.md` L87461–87491
- **v0.31 — 31.22 Resource accounting and provenance** — `Continue Architecture Planning.md` L87493–87536
- **v0.31 — 31.25 What v0.31 adds** — `Continue Architecture Planning.md` L87648–87701

## Related Documents

- [Scheduling](scheduler.md)
- [Acquisition Runtime](../acquisition/runtime.md)
- [Work Items and Frontier Arbitration](work-and-frontier.md)
- [Invariants](../validation/invariants.md)

---

<!-- source: Continue Architecture Planning.md L86478–86517 | turn 77 | version 0.31 -->
## v0.31 — Unified Resource & Cost Ledger

v0.30 solved:

> **Which admissible work should execute next?**

But arbitration is incomplete without answering:

> **What resources may that work consume, how much did it actually consume, and who gets charged for it?**

The new control loop is:

```
                    FRONTIER
                       │
                       ▼
                  ARBITRATION
                       │
                       ▼
                  ALLOCATION
                       │
                       ▼
                   EXECUTION
                       │
                       ▼
                MEASURED COST
                       │
                       ▼
                RESOURCE LEDGER
                       │
                       └──────────► ARBITRATION
```

The critical principle is:

> **A budget is a constraint; a cost is an observation.**

They must not be conflated.

---

<!-- source: Continue Architecture Planning.md L86519–86576 | turn 77 | version 0.31 -->
## v0.31 — 31.1 Resource dimensions

The engine should stop treating "request count" as its universal budget.

A work item may consume:

```
NETWORK
├── requests
├── bytes received
├── bytes transmitted
├── connection slots
└── origin quota

COMPUTE
├── CPU time
├── wall-clock time
├── worker slots
└── WASM execution units

STORAGE
├── artifact bytes
├── database bytes
├── temporary bytes
└── retained evidence

DISCOVERY
├── proposals
├── partitions
├── enumeration pages
└── hypotheses

PROCESSING
├── recognition operations
├── classification operations
├── verification operations
└── reconciliation operations
```

This produces a general resource vector:

```JavaScript
{
    requests: 1,
    bytesIn: 245812,
    bytesOut: 0,

    cpuMs: 38,
    wallMs: 420,

    storageBytes: 245812,

    proposals: 14,
    pages: 1
}
```

---

<!-- source: Continue Architecture Planning.md L86578–86627 | turn 77 | version 0.31 -->
## v0.31 — 31.2 ResourceBudget

A budget is an upper bound.

```JavaScript
class ResourceBudget {
    constructor(data = {}) {
        this.limits = {
            requests: data.requests ?? Infinity,
            bytesIn: data.bytesIn ?? Infinity,
            bytesOut: data.bytesOut ?? Infinity,

            cpuMs: data.cpuMs ?? Infinity,
            wallMs: data.wallMs ?? Infinity,

            storageBytes:
                data.storageBytes ?? Infinity,

            proposals:
                data.proposals ?? Infinity,

            pages:
                data.pages ?? Infinity
        };
    }

    canReserve(cost) {
        return Object.entries(cost).every(
            ([key, value]) =>
                value <= this.limits[key]
        );
    }
}
```

But this is still insufficient.

Why?

Because:

```
limit
≠
reserved
≠
consumed
```

---

<!-- source: Continue Architecture Planning.md L86629–86672 | turn 77 | version 0.31 -->
## v0.31 — 31.3 Three resource states

Every resource dimension should therefore distinguish:

```
             LIMIT
               │
        ┌──────┴──────┐
        ▼             ▼
    RESERVED       AVAILABLE
        │
        ▼
    CONSUMED
```

For example:

```JavaScript
{
    limit: 100,
    reserved: 12,
    consumed: 8,
    available: 80
}
```

The reservation exists because several workers may make decisions concurrently.

Without reservations:

```
Worker A sees 2 requests remaining
Worker B sees 2 requests remaining

A reserves 2
B reserves 2

actual = 4
limit = 2
```

The budget was oversubscribed.

---

<!-- source: Continue Architecture Planning.md L86674–86734 | turn 77 | version 0.31 -->
## v0.31 — 31.4 ResourceReservation

```JavaScript
class ResourceReservation {
    constructor(data = {}) {
        this.id = data.id || makeId('reservation');

        this.workItemId =
            data.workItemId || null;

        this.sessionId =
            data.sessionId || null;

        this.resourceClass =
            data.resourceClass || null;

        this.requested =
            data.requested || {};

        this.reserved =
            data.reserved || {};

        this.status =
            data.status || 'reserved';

        this.createdAt =
            data.createdAt || now();

        this.expiresAt =
            data.expiresAt || null;
    }

    serialize() {
        return { ...this };
    }
}
```

Lifecycle:

```
REQUESTED
    ↓
RESERVED
    ↓
CONSUMED
    │
    ├── SETTLED
    └── RELEASED
```

Exceptional:

```
DENIED
EXPIRED
CANCELLED
CONFLICT
```

---

<!-- source: Continue Architecture Planning.md L86736–86789 | turn 77 | version 0.31 -->
## v0.31 — 31.5 Estimated cost vs actual cost

Before execution:

```
estimatedCost
```

After execution:

```
actualCost
```

Example:

```JavaScript
{
    estimated: {
        bytesIn: 500000,
        cpuMs: 100
    },

    actual: {
        bytesIn: 731842,
        cpuMs: 143
    }
}
```

Never overwrite the estimate.

The difference itself is useful information.

```
estimated cost
      │
      ▼
resource reservation
      │
      ▼
execution
      │
      ▼
actual measurement
      │
      ▼
cost error
      │
      ▼
future estimates
```

---

<!-- source: Continue Architecture Planning.md L86791–86844 | turn 77 | version 0.31 -->
## v0.31 — 31.6 CostObservation

Actual consumption is an observation.

```JavaScript
class CostObservation {
    constructor(data = {}) {
        this.id = data.id || makeId('cost');

        this.workItemId =
            data.workItemId || null;

        this.attemptId =
            data.attemptId || null;

        this.providerId =
            data.providerId || null;

        this.values =
            data.values || {};

        this.measurementMethod =
            data.measurementMethod || null;

        this.confidence =
            Number.isFinite(data.confidence)
                ? data.confidence
                : 1;

        this.createdAt =
            data.createdAt || now();
    }

    serialize() {
        return { ...this };
    }
}
```

This follows the existing epistemic architecture:

```
Execution
   ↓
Observation
   ↓
CostObservation
```

The runtime should not pretend that every measurement is exact.

For example, browser CPU time may be unavailable or approximate.

---

<!-- source: Continue Architecture Planning.md L86846–86879 | turn 77 | version 0.31 -->
## v0.31 — 31.7 ResourceLedger

The ledger becomes the authoritative accounting structure.

```JavaScript
class ResourceLedger {
    constructor() {
        this.budgets = new Map();
        this.reservations = new Map();
        this.consumption = new Map();
        this.observations = new Map();
    }

    reserve(resourceScope, cost) {
        throw new Error('Not implemented');
    }

    settle(reservationId, actualCost) {
        throw new Error('Not implemented');
    }

    release(reservationId) {
        throw new Error('Not implemented');
    }

    remaining(resourceScope) {
        throw new Error('Not implemented');
    }
}
```

The ledger should support multiple scopes.

---

<!-- source: Continue Architecture Planning.md L86881–86933 | turn 77 | version 0.31 -->
## v0.31 — 31.8 Budget scopes

Budgets can exist at several levels:

```
GLOBAL
  │
  ├── SESSION
  │     │
  │     ├── GOAL
  │     │     │
  │     │     └── QUERY PLAN
  │     │
  │     └── PARTITION
  │
  └── ORIGIN
        │
        └── WORK CLASS
```

For example:

```
Global:
    150 acquisitions

Session:
    50 acquisitions

Goal:
    20 acquisitions

Origin:
    10 acquisitions

Partition:
    5 acquisitions
```

A request must satisfy **all applicable limits**.

```
Acquire(w)
    ⇒
    global budget
    ∧ session budget
    ∧ goal budget
    ∧ origin budget
    ∧ partition budget
    ∧ class budget
```

---

<!-- source: Continue Architecture Planning.md L86935–86974 | turn 77 | version 0.31 -->
## v0.31 — 31.9 Hierarchical budget accounting

This creates a budget tree:

```
GLOBAL
│
├── Scan A
│   │
│   ├── Goal 1
│   │   ├── Partition P1
│   │   └── Partition P2
│   │
│   └── Goal 2
│
└── Scan B
```

Consumption should be visible at every relevant scope.

If:

```
P1 consumes 3 requests
```

then:

```
P1       +3
Goal     +3
Session  +3
Global   +3
```

But the system must avoid double-counting.

A single physical request is one consumption event with multiple accounting views.

---

<!-- source: Continue Architecture Planning.md L86976–87027 | turn 77 | version 0.31 -->
## v0.31 — 31.10 Resource allocation

Arbitration says:

```
"work-42 should run"
```

Allocation says:

```
"work-42 receives these resources"
```

Therefore:

```
ArbitrationDecision
       ↓
ResourceAllocator
       ↓
Reservation
       ↓
Execution
```

Contract:

```JavaScript
class ResourceAllocator {
    canAllocate(work, context) {
        return {
            allowed: false,
            reason: 'not-implemented'
        };
    }

    estimate(work, context) {
        return {};
    }

    reserve(work, estimate, context) {
        throw new Error('Not implemented');
    }

    release(reservation, context) {
        throw new Error('Not implemented');
    }
}
```

---

<!-- source: Continue Architecture Planning.md L87029–87055 | turn 77 | version 0.31 -->
## v0.31 — 31.11 Allocation is not execution

This distinction is important.

```
RESERVED
   ≠
STARTED
   ≠
COMPLETED
```

Example:

```
reserve 1 request
      ↓
browser provider unavailable
      ↓
request never starts
```

The reservation should be released or settled appropriately.

It must not automatically count as an actual request.

---

<!-- source: Continue Architecture Planning.md L87057–87102 | turn 77 | version 0.31 -->
## v0.31 — 31.12 Partial consumption

Real execution often consumes less or more than estimated.

Example:

```
Reserved:
    bytes = 1 MB

Actual:
    bytes = 640 KB
```

Then:

```
640 KB → consumed
384 KB → released
```

But:

```
Reserved:
    CPU = 100 ms

Actual:
    CPU = 180 ms
```

Now the ledger detects an overrun.

Possible policies:

```
ALLOW
WARN
STOP
CHARGE_OVERAGE
RETRY_WITH_NEW_RESERVATION
```

The policy belongs to the resource allocator, not the arbitrator.

---

<!-- source: Continue Architecture Planning.md L87104–87146 | turn 77 | version 0.31 -->
## v0.31 — 31.13 Cost overruns

Define:

```JavaScript
class CostVariance {
    constructor(data = {}) {
        this.dimension = data.dimension;
        this.estimated = data.estimated ?? 0;
        this.actual = data.actual ?? 0;

        this.delta =
            this.actual - this.estimated;

        this.ratio =
            this.estimated > 0
                ? this.actual / this.estimated
                : null;
    }
}
```

Then:

```
actual / estimated

< 1      under-estimate? no
         actually cheaper

= 1      accurate

> 1      cost overrun
```

The terminology should remain explicit:

```
actual < estimated → underrun
actual > estimated → overrun
```

---

<!-- source: Continue Architecture Planning.md L87148–87205 | turn 77 | version 0.31 -->
## v0.31 — 31.14 Cost model

The engine can eventually calculate:

```
ExpectedUtility(work)
───────────────────────
ExpectedCost(work)
```

But cost has multiple dimensions.

A more general model:

```
CostVector(w) =
[
    requests,
    bytes,
    cpu,
    wall_time,
    storage,
    provider_load
]
```

And:

```
UtilityVector(w) =
[
    goal_value,
    novelty,
    coverage_value,
    information_gain
]
```

The arbitrator can use a policy-specific scalarization:

```
utility =
    weighted_value(UtilityVector)
    /
    weighted_cost(CostVector)
```

But the original vectors should be retained.

Otherwise:

```
"0.73 utility"
```

becomes uninterpretable.

---

<!-- source: Continue Architecture Planning.md L87207–87242 | turn 77 | version 0.31 -->
## v0.31 — 31.15 Cost is context-dependent

A request may be cheap for one origin and expensive for another.

Likewise:

```
HTML page
    ↓
100 KB

PDF
    ↓
25 MB
```

Therefore historical cost should be keyed contextually:

```
(provider,
 workClass,
 originClass,
 resourceType,
 strategy,
 partitionKind)
```

Not merely:

```
strategy → average cost
```

This follows the same contextual-prior principle established in v0.21.

---

<!-- source: Continue Architecture Planning.md L87244–87286 | turn 77 | version 0.31 -->
## v0.31 — 31.16 Resource exhaustion

The ledger needs explicit states.

```JavaScript
const ResourceState = Object.freeze({
    AVAILABLE: 'available',
    RESERVED: 'reserved',
    EXHAUSTED: 'exhausted',
    BLOCKED: 'blocked',
    UNKNOWN: 'unknown'
});
```

Example:

```
acquisition budget
      │
      ├── 137 used
      ├── 13 available
      └── 0 reserved
```

At zero:

```
AVAILABLE → EXHAUSTED
```

This is different from:

```
policy denied
```

and:

```
provider unavailable
```

---

<!-- source: Continue Architecture Planning.md L87288–87323 | turn 77 | version 0.31 -->
## v0.31 — 31.17 Budget exhaustion vs frontier exhaustion

These must remain separate.

```
FRONTIER EXHAUSTED
    =
    no admissible unfinished work

BUDGET EXHAUSTED
    =
    work may remain, but resources are unavailable
```

Therefore:

```
queue empty + budget remaining
        → frontier exhausted

queue nonempty + budget exhausted
        → resource-limited

queue empty + budget exhausted
        → both conditions
```

This distinction directly affects completeness claims.

Budget exhaustion cannot support:

```
"nothing else exists"
```

---

<!-- source: Continue Architecture Planning.md L87325–87363 | turn 77 | version 0.31 -->
## v0.31 — 31.18 Resource reservation race

Consider:

```
budget = 10

Worker A reserves 6
Worker B reserves 5
```

Naive implementation:

```
A sees 10
B sees 10
A reserves
B reserves
```

Result:

```
11 > 10
```

Therefore reservation must be atomic relative to the ledger state.

The invariant:

```
Σ reservations + Σ consumed
    ≤
budget limit
```

for every scope.

---

<!-- source: Continue Architecture Planning.md L87365–87415 | turn 77 | version 0.31 -->
## v0.31 — 31.19 Settlement

After execution:

```
Reservation
     │
     ▼
Actual Cost
     │
     ▼
Settlement
     │
 ┌───┴────┐
 ▼        ▼
under    over
run      run
 │        │
 ▼        ▼
release  charge /
remaining reallocate
```

A settlement record should retain:

```JavaScript
{
    reservationId: "res-42",

    estimated: {
        requests: 1,
        bytesIn: 500000
    },

    actual: {
        requests: 1,
        bytesIn: 731842
    },

    released: {
        requests: 0,
        bytesIn: 0
    },

    overrun: {
        bytesIn: 231842
    }
}
```

---

<!-- source: Continue Architecture Planning.md L87417–87459 | turn 77 | version 0.31 -->
## v0.31 — 31.20 Cost feedback

Now the complete adaptive loop exists:

```
WORK
 │
 ▼
ESTIMATE
 │
 ▼
ARBITRATE
 │
 ▼
RESERVE
 │
 ▼
EXECUTE
 │
 ▼
MEASURE
 │
 ▼
SETTLE
 │
 ▼
COST HISTORY
 │
 ▼
FUTURE ESTIMATE
 │
 └──────────────► ARBITRATION
```

This is much stronger than simply tracking:

```JavaScript
requestsUsed++
```

because the engine begins learning **operational economics**.

---

<!-- source: Continue Architecture Planning.md L87461–87491 | turn 77 | version 0.31 -->
## v0.31 — 31.21 ResourceLedger events

Add:

```
budget-created
budget-updated
budget-exhausted

resource-estimate-created
resource-reservation-requested
resource-reservation-granted
resource-reservation-denied
resource-reservation-released
resource-reservation-expired

resource-consumption-observed
resource-settlement-started
resource-settlement-completed

cost-underrun
cost-overrun

resource-allocation-created
resource-allocation-revoked
resource-accounting-conflict
```

Every accounting transition becomes auditable.

---

<!-- source: Continue Architecture Planning.md L87493–87536 | turn 77 | version 0.31 -->
## v0.31 — 31.22 Resource accounting and provenance

A useful provenance chain is now:

```
Goal
 ↓
QueryPlan
 ↓
WorkItem
 ↓
ArbitrationDecision
 ↓
ResourceReservation
 ↓
Execution
 ↓
Observation
 ↓
CostObservation
 ↓
Settlement
```

This permits questions such as:

> Why did this request consume the acquisition budget?

Answer:

```
Goal G
→ QueryPlan P
→ WorkItem W
→ Arbitration A
→ Reservation R
→ Attempt X
→ Observation O
→ Cost C
```

This is exactly the kind of accountability needed for a trustworthy acquisition system.

---

<!-- source: Continue Architecture Planning.md L87648–87701 | turn 77 | version 0.31 -->
## v0.31 — 31.25 What v0.31 adds

The architecture now has three distinct control layers:

```
                 AUTHORITY
                    │
             Policy / Capability
                    │
                    ▼
                 ELIGIBILITY
                    │
                    ▼
                 ARBITRATION
                    │
                    ▼
                 ALLOCATION
                    │
                    ▼
                 EXECUTION
                    │
                    ▼
                OBSERVATION
                    │
                    ▼
                 ACCOUNTING
```

So:

```
Policy answers:
    "May it?"

Arbitration answers:
    "Which one?"

Allocation answers:
    "With how much?"

Execution answers:
    "What happened?"

Accounting answers:
    "What did it actually cost?"
```

That is a much cleaner architecture than a conventional crawler's:

```
queue → request → parse
```

---
