# Acquisition Runtime

> **Status:** DESIGNED
>
> **Source:** `Continue Architecture Planning.md`
>
> **Purpose:** The runtime that executes acquisition: admission control, budgets, origin control, cancellation, timeouts and retries.

## Source Sections

- **v0.10 — Acquisition Runtime** — `CAP-106` — `Continue Architecture Planning.md` L56357–56366
- **v0.10 — 2. The key distinction: Scheduler vs Runtime** — `CAP-108` — `Continue Architecture Planning.md` L56434–56436
- **v0.10 — Scheduler** — `CAP-109` — `Continue Architecture Planning.md` L56438–56452
- **v0.10 — Runtime** — `CAP-110` — `Continue Architecture Planning.md` L56454–56496
- **v0.10 — 3. AcquisitionRuntime contract** — `CAP-111` — `Continue Architecture Planning.md` L56498–56540
- **v0.10 — 4. Admission control** — `CAP-112` — `Continue Architecture Planning.md` L56542–56598
- **v0.10 — 5. Budget becomes a first-class object** — `CAP-113` — `Continue Architecture Planning.md` L56600–56658
- **v0.10 — 6. Why reservation must precede execution** — `CAP-114` — `Continue Architecture Planning.md` L56660–56704
- **v0.10 — 7. OriginController** — `CAP-115` — `Continue Architecture Planning.md` L56706–56796
- **v0.10 — 8. Provider selection happens after admission prerequisites** — `CAP-116` — `Continue Architecture Planning.md` L56798–56843
- **v0.10 — 9. Provider must not own runtime policy** — `CAP-117` — `Continue Architecture Planning.md` L56845–56889
- **v0.10 — 10. Cancellation becomes explicit** — `CAP-118` — `Continue Architecture Planning.md` L56891–56943
- **v0.10 — 11. Timeout belongs to Runtime** — `CAP-119` — `Continue Architecture Planning.md` L56945–56979
- **v0.10 — 12. Retry belongs to Runtime** — `CAP-120` — `Continue Architecture Planning.md` L56981–57027
- **v0.10 — 13. Plan vs Attempt** — `CAP-121` — `Continue Architecture Planning.md` L57029–57056
- **v0.10 — 14. Runtime event model** — `CAP-122` — `Continue Architecture Planning.md` L57058–57105
- **v0.10 — 15. Runtime state machine** — `CAP-123` — `Continue Architecture Planning.md` L57107–57138
- **v0.10 — 16. The complete execution equation** — `CAP-124` — `Continue Architecture Planning.md` L57140–57179

## Related Documents

- [Acquisition Model](acquisition-model.md)
- [Scheduling](../architecture/scheduler.md)
- [Resource and Cost Ledger](../architecture/resource-budget.md)
- [Provider Architecture](../architecture/provider-architecture.md)

---

<!-- CAP-106 | Continue Architecture Planning.md L56357–56366 | turn 33 | version 0.10 -->
## v0.10 — Acquisition Runtime

> **Source sections:** `CAP-106`

v0.9 separated **how acquisition happens** from the discovery engine.  
v0.10 should now separate **execution control** from the provider.

The central rule becomes:

> **Providers perform I/O. The Acquisition Runtime controls I/O.**

---

<!-- CAP-108 | Continue Architecture Planning.md L56434–56436 | turn 33 | version 0.10 -->
## v0.10 — 2. The key distinction: Scheduler vs Runtime

> **Source sections:** `CAP-108`

These are easy to accidentally merge.

<!-- CAP-109 | Continue Architecture Planning.md L56438–56452 | turn 33 | version 0.10 -->
### v0.10 — Scheduler

> **Source sections:** `CAP-109`

Maintains candidate ordering:

```
candidate A priority 0.91
candidate B priority 0.72
candidate C priority 0.55
```

It answers:

```
Which candidate should run next?
```

<!-- CAP-110 | Continue Architecture Planning.md L56454–56496 | turn 33 | version 0.10 -->
### v0.10 — Runtime

> **Source sections:** `CAP-110`

Controls execution:

```
global concurrency = 4
origin concurrency = 2
origin delay = 150 ms
budget = 150 requests
timeout = 8 s
```

It answers:

```
Can this already-selected acquisition execute now?
```

Therefore:

```
Scheduler
    ↓
"Run candidate A"

Runtime
    ↓
"Not yet: origin budget unavailable"

Scheduler
    ↓
"Run candidate B"

Runtime
    ↓
"Granted"

Provider
    ↓
GET /resource
```

---

<!-- CAP-111 | Continue Architecture Planning.md L56498–56540 | turn 33 | version 0.10 -->
## v0.10 — 3. AcquisitionRuntime contract

> **Source sections:** `CAP-111`

The runtime can have a deliberately narrow interface:

```JavaScript
class AcquisitionRuntime {
    constructor(options = {}) {
        this.scheduler = options.scheduler || null;
        this.providerRegistry = options.providerRegistry || null;
        this.budget = options.budget || null;
        this.originController = options.originController || null;
        this.cancellation = options.cancellation || null;
    }

    async execute(plan) {
        throw new Error('Not implemented');
    }

    describe() {
        return {
            id: 'unknown-runtime'
        };
    }
}
```

The important point is that `execute()` does **not** directly mean:

```
provider.execute()
```

It means:

```
admission
→ provider resolution
→ resource controls
→ execution
→ observation
```

---

<!-- CAP-112 | Continue Architecture Planning.md L56542–56598 | turn 33 | version 0.10 -->
## v0.10 — 4. Admission control

> **Source sections:** `CAP-112`

Before invoking a provider:

```
                  PLAN
                   │
                   ▼
             ┌───────────┐
             │ authorized│
             └─────┬─────┘
                   │
                   ▼
             ┌───────────┐
             │ capability│
             │ satisfied? │
             └─────┬─────┘
                   │
                   ▼
             ┌───────────┐
             │ budget OK?│
             └─────┬─────┘
                   │
                   ▼
             ┌───────────┐
             │ origin OK?│
             └─────┬─────┘
                   │
                   ▼
             ┌───────────┐
             │ cancelled?│
             └─────┬─────┘
                   │
                   ▼
                EXECUTE
```

Every rejection should produce a distinct reason.

For example:

```JavaScript
{
    allowed: false,
    reason: 'global-request-budget-exhausted'
}
```

rather than the vague:

```JavaScript
{
    allowed: false
}
```

---

<!-- CAP-113 | Continue Architecture Planning.md L56600–56658 | turn 33 | version 0.10 -->
## v0.10 — 5. Budget becomes a first-class object

> **Source sections:** `CAP-113`

Instead of scattered counters:

```JavaScript
requests++
if (requests > maxRequests) ...
```

introduce:

```JavaScript
class RequestBudget {
    constructor(maxRequests = Infinity) {
        this.maxRequests = maxRequests;
        this.used = 0;
    }

    available() {
        return this.used < this.maxRequests;
    }

    reserve() {
        if (!this.available()) {
            return false;
        }

        this.used++;
        return true;
    }

    remaining() {
        return Math.max(
            0,
            this.maxRequests - this.used
        );
    }

    serialize() {
        return {
            maxRequests: this.maxRequests,
            used: this.used,
            remaining: this.remaining()
        };
    }
}
```

Now the budget has a semantic meaning:

```
budget reservation
    ≠
request started
```

That distinction matters.

---

<!-- CAP-114 | Continue Architecture Planning.md L56660–56704 | turn 33 | version 0.10 -->
## v0.10 — 6. Why reservation must precede execution

> **Source sections:** `CAP-114`

Consider concurrency:

```
maxRequests = 3
```

Four workers simultaneously ask:

```
"Can I execute?"
```

If the check and increment are separated:

```JavaScript
if (budget.available()) {
    // asynchronous gap
    budget.used++;
}
```

all four can observe availability.

The correct conceptual operation is atomic:

```
reserve()
```

```
Worker A → reserve → success
Worker B → reserve → success
Worker C → reserve → success
Worker D → reserve → DENIED
```

This is the same class of problem you previously identified as **concurrent candidate claiming**.

The general principle is:

> **Admission must be a state transition, not a prediction.**

---

<!-- CAP-115 | Continue Architecture Planning.md L56706–56796 | turn 33 | version 0.10 -->
## v0.10 — 7. OriginController

> **Source sections:** `CAP-115`

The existing v0.6 origin controls should move behind a dedicated interface.

```JavaScript
class OriginController {
    constructor(options = {}) {
        this.maxConcurrent =
            options.maxConcurrent ?? 2;

        this.minInterval =
            options.minInterval ?? 150;

        this.maxRequests =
            options.maxRequests ?? 50;

        this.states = new Map();
    }

    state(origin) {
        if (!this.states.has(origin)) {
            this.states.set(origin, {
                active: 0,
                requests: 0,
                lastRequestAt: 0
            });
        }

        return this.states.get(origin);
    }

    canReserve(origin) {
        const state = this.state(origin);

        return (
            state.active < this.maxConcurrent &&
            state.requests < this.maxRequests
        );
    }

    reserve(origin) {
        if (!this.canReserve(origin)) {
            return false;
        }

        const state = this.state(origin);

        state.active++;
        state.requests++;

        return true;
    }

    release(origin) {
        const state = this.state(origin);

        state.active = Math.max(
            0,
            state.active - 1
        );

        state.lastRequestAt = Date.now();
    }
}
```

But there is an important correction:

**`canReserve()` should not be the authoritative operation.**

Eventually the interface should prefer:

```JavaScript
reserve(origin)
```

because:

```
canReserve()
```

is observational, while:

```
reserve()
```

is state-changing.

---

<!-- CAP-116 | Continue Architecture Planning.md L56798–56843 | turn 33 | version 0.10 -->
## v0.10 — 8. Provider selection happens after admission prerequisites

> **Source sections:** `CAP-116`

A useful sequence is:

```
Plan
 │
 ├── method valid?
 │
 ├── capabilities valid?
 │
 ├── policy allowed?
 │
 ├── global budget available?
 │
 ├── origin budget available?
 │
 ├── provider exists?
 │
 └── cancellation active?
 │
 ▼
Execute
```

There is one subtle optimization:

Provider selection can happen **before** budget reservation because provider selection itself performs no external action.

Thus:

```
plan
 ↓
provider selection
 ↓
admission
 ↓
reservation
 ↓
provider.execute()
```

is preferable.

---

<!-- CAP-117 | Continue Architecture Planning.md L56845–56889 | turn 33 | version 0.10 -->
## v0.10 — 9. Provider must not own runtime policy

> **Source sections:** `CAP-117`
>
> [DOCUMENTATION REVIEW] Contradiction **C-11** ([Review Notes](../REVIEW-NOTES.md#c-11--same-origin-default-versus-cross-origin-capability))

This would be wrong:

```JavaScript
class GMXHRProvider {
    async execute(plan) {
        if (requestCount >= 150) return;
        if (originActive >= 2) return;
        await sleep(150);
        ...
    }
}
```

Now the provider has become another scheduler.

Instead:

```JavaScript
class GMXHRProvider {
    async execute(plan) {
        return gmXmlHttpRequest(plan);
    }
}
```

The runtime controls:

```
budget
rate
concurrency
retry
timeout
cancellation
```

The provider controls:

```
transport mechanism
```

---

<!-- CAP-118 | Continue Architecture Planning.md L56891–56943 | turn 33 | version 0.10 -->
## v0.10 — 10. Cancellation becomes explicit

> **Source sections:** `CAP-118`

v0.6 had an important limitation:

> stopping the engine did not necessarily abort in-flight requests.

v0.10 should fix the model.

Introduce:

```JavaScript
class CancellationToken {
    constructor() {
        this.cancelled = false;
        this.reason = null;
    }

    cancel(reason = 'cancelled') {
        this.cancelled = true;
        this.reason = reason;
    }

    throwIfCancelled() {
        if (this.cancelled) {
            throw new Error(this.reason);
        }
    }
}
```

The runtime checks it before execution:

```JavaScript
token.throwIfCancelled();
```

and the provider receives the cancellation context:

```JavaScript
await provider.execute(plan, {
    signal: token
});
```

For GM-XHR, the provider can map cancellation to:

```JavaScript
request.abort();
```

when the userscript API supports it.

---

<!-- CAP-119 | Continue Architecture Planning.md L56945–56979 | turn 33 | version 0.10 -->
## v0.10 — 11. Timeout belongs to Runtime

> **Source sections:** `CAP-119`

Timeout is also execution control.

Not:

```
GM-XHR provider policy
```

but:

```
Acquisition Runtime
```

The plan might specify:

```JavaScript
{
    timeoutMs: 8000
}
```

The runtime applies the default:

```JavaScript
const timeout =
    plan.timeoutMs ??
    config.requestTimeout;
```

The provider merely executes under that constraint.

---

<!-- CAP-120 | Continue Architecture Planning.md L56981–57027 | turn 33 | version 0.10 -->
## v0.10 — 12. Retry belongs to Runtime

> **Source sections:** `CAP-120`

Similarly:

```
provider
    → "request failed"

runtime
    → classify failure

runtime
    → retry?

runtime
    → backoff

runtime
    → execute again
```

Not:

```
GM-XHR provider
    → secretly retries
```

This is important for deterministic accounting.

One acquisition plan may produce:

```
plan-123
 ├── attempt 1
 │    └── timeout
 │
 ├── attempt 2
 │    └── HTTP 503
 │
 └── attempt 3
      └── 200 OK
```

The event ledger records all three.

---

<!-- CAP-121 | Continue Architecture Planning.md L57029–57056 | turn 33 | version 0.10 -->
## v0.10 — 13. Plan vs Attempt

> **Source sections:** `CAP-121`

This introduces another useful identity distinction:

```
PLAN
  │
  ├── attempt 1
  ├── attempt 2
  └── attempt 3
```

Therefore:

```JavaScript
{
    planId: 'plan-123',
    attemptId: 'attempt-3',
    candidateId: 'cand-42',
    providerId: 'gm-xhr'
}
```

A retry does **not** create a new candidate.

It creates a new execution attempt.

---

<!-- CAP-122 | Continue Architecture Planning.md L57058–57105 | turn 33 | version 0.10 -->
## v0.10 — 14. Runtime event model

> **Source sections:** `CAP-122`

v0.10 extends the ledger:

```
candidate-discovered
candidate-claimed

acquisition-planned

provider-selected

admission-requested
admission-granted

budget-reserved
origin-slot-reserved

attempt-started
request-started
request-completed

observation-recorded

origin-slot-released
budget-accounted

attempt-completed
candidate-completed
```

Failure paths:

```
policy-denied
capability-denied
provider-unavailable
budget-denied
origin-denied
cancelled
timeout
provider-error
retry-scheduled
```

This gives a much stronger causal history.

---

<!-- CAP-123 | Continue Architecture Planning.md L57107–57138 | turn 33 | version 0.10 -->
## v0.10 — 15. Runtime state machine

> **Source sections:** `CAP-123`

```
                         ┌──────────────┐
                         │    PLANNED   │
                         └──────┬───────┘
                                │
                                ▼
                         PROVIDER SELECTED
                                │
                                ▼
                           ADMISSION
                         /           \
                       deny          grant
                       │               │
                       ▼               ▼
                    SKIPPED       RESERVED
                                       │
                                       ▼
                                    RUNNING
                                  /    |    \
                                 /     |     \
                            success  retry   cancel
                              │       │        │
                              ▼       ▼        ▼
                         OBSERVED  BACKOFF   CANCELLED
                                      │
                                      ▼
                                    RUNNING
```

---

<!-- CAP-124 | Continue Architecture Planning.md L57140–57179 | turn 33 | version 0.10 -->
## v0.10 — 16. The complete execution equation

> **Source sections:** `CAP-124`

v0.8 had:

```
Acquire(x)
⇒
Candidate(x)
∧ Requirements(x)
∧ CapabilitiesSatisfied(x)
∧ PolicyAllowed(x)
∧ PlanExists(x)
∧ BudgetAvailable(x)
∧ SchedulerGranted(x)
```

v0.10 can refine this:

```
Execute(plan)
⇒
PlanValid
∧ ProviderSelected
∧ ProviderCapable
∧ PolicyAllowed
∧ BudgetReserved
∧ OriginSlotReserved
∧ CancellationClear
∧ AttemptAuthorized
```

And:

```
Provider.execute(plan)
```

is only called **after all runtime invariants hold**.

---
