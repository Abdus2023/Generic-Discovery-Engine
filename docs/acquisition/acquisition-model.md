# Acquisition Model

> **Status:** DESIGNED
>
> **Source:** `Continue Architecture Planning.md`
>
> **Purpose:** The acquisition layer: detection before decoding, acquisition plans, conditional acquisition and acquisition policy.

## Source Sections

- **v0.8 — Acquisition graph** — `CAP-059` — `Continue Architecture Planning.md` L54697–54710
- **v0.8 — 6. Acquisition planning becomes capability resolution** — `CAP-065` — `Continue Architecture Planning.md` L54970–55044
- **v0.8 — 8. AcquisitionPlan v0.8** — `CAP-067` — `Continue Architecture Planning.md` L55106–55202
- **v0.15 — 14. Discovery and acquisition fairness** — `CAP-287` — `Continue Architecture Planning.md` L62642–62695
- **v0.15 — 32. Discovery vs acquisition remains intact** — `CAP-305` — `Continue Architecture Planning.md` L63352–63388
- **v0.16 — Acquisition** — `CAP-362` — `Continue Architecture Planning.md` L65180–65184
- **v0.18 — 18.18 Classification Must Not Become Acquisition Policy** — `CAP-442` — `Continue Architecture Planning.md` L67737–67794
- **v0.19 — 19.13 Conditional Acquisition** — `CAP-476` — `Continue Architecture Planning.md` L68811–68864

## Related Documents

- [Acquisition Overview](overview.md)
- [Acquisition Runtime](runtime.md)
- [Observation Model](../architecture/observation-model.md)
- [Provider Architecture](../architecture/provider-architecture.md)

---

<!-- CAP-059 | Continue Architecture Planning.md L54697–54710 | turn 29 | version 0.8 -->
### v0.8 — Acquisition graph

> **Source sections:** `CAP-059`

```
API endpoint
   │
   ├── GET
   ├── same-origin
   ├── textual-response
   └── no-auth
```

Meaning:

> These are the conditions under which the runtime can acquire it.

<!-- CAP-065 | Continue Architecture Planning.md L54970–55044 | turn 29 | version 0.8 -->
## v0.8 — 6. Acquisition planning becomes capability resolution

> **Source sections:** `CAP-065`

v0.7.1:

```
Candidate
    ↓
allowed?
```

v0.8:

```
Candidate
    ↓
Requirements
    ↓
Capability resolution
    ↓
Policy
    ↓
Plan
```

Conceptually:

```JavaScript
class AcquisitionPolicy {
    constructor(runtimeCapabilities) {
        this.runtimeCapabilities =
            runtimeCapabilities;
    }

    plan(candidate) {
        const required =
            candidate.requirements
                ?.capabilities || [];

        const missing =
            this.runtimeCapabilities
                .missing(required);

        if (missing.length) {
            return deniedPlan(
                candidate,
                'missing-capabilities',
                { missing }
            );
        }

        // Continue with normal policy checks...
    }
}
```

This gives us a much cleaner failure reason:

```
policy denied
```

becomes:

```
missing-capabilities:
    network.post
```

instead of an opaque:

```
forms-disabled
```

---

<!-- CAP-067 | Continue Architecture Planning.md L55106–55202 | turn 29 | version 0.8 -->
## v0.8 — 8. AcquisitionPlan v0.8

> **Source sections:** `CAP-067`

The plan should evolve from v0.7.1 into:

```JavaScript
{
    id,

    candidateId,
    target,

    method,

    requiredCapabilities,
    grantedCapabilities,
    missingCapabilities,

    allowed,
    reason,

    expectedType,

    priority,

    origin,

    policyVersion
}
```

Example:

```JSON
{
  "id": "plan-42",
  "candidateId": "candidate-19",
  "target": "https://example.com/api/catalog",
  "method": "GET",

  "requiredCapabilities": [
    "network.http",
    "network.get",
    "same-origin",
    "text-response"
  ],

  "grantedCapabilities": [
    "network.http",
    "network.get",
    "same-origin",
    "text-response"
  ],

  "missingCapabilities": [],

  "allowed": true,
  "reason": null,

  "expectedType": "api",
  "priority": 0.91,
  "origin": "https://example.com",

  "policyVersion": 8
}
```

For POST:

```JSON
{
  "target": "https://example.com/api/order",
  "method": "POST",

  "requiredCapabilities": [
    "network.http",
    "network.post",
    "request-body"
  ],

  "grantedCapabilities": [
    "network.http",
    "network.get"
  ],

  "missingCapabilities": [
    "network.post",
    "request-body"
  ],

  "allowed": false,
  "reason": "missing-capabilities"
}
```

That is substantially better evidence.

---

<!-- CAP-287 | Continue Architecture Planning.md L62642–62695 | turn 43 | version 0.15 -->
## v0.15 — 14. Discovery and acquisition fairness

> **Source sections:** `CAP-287`

There is another starvation problem.

Imagine:

```
discovery tasks = 10,000
acquisition tasks = 10
```

A scheduler that simply sees the largest queue could spend all its time discovering.

Conversely:

```
acquisition tasks = 10,000
discovery tasks = 10
```

could prevent graph expansion.

Therefore the scheduler needs a **work-class policy**.

For example:

```
                 WORK SCHEDULER
                       │
             ┌─────────┴─────────┐
             │                   │
       Discovery quota     Acquisition quota
             │                   │
             └─────────┬─────────┘
                       ▼
                  Work selection
```

A simple initial policy:

```JavaScript
{
    discoveryWeight: 0.35,
    acquisitionWeight: 0.65
}
```

This is not necessarily the final algorithm.

The architectural point is:

> **Work-class fairness is separate from item priority.**

---

<!-- CAP-305 | Continue Architecture Planning.md L63352–63388 | turn 43 | version 0.15 -->
## v0.15 — 32. Discovery vs acquisition remains intact

> **Source sections:** `CAP-305`

This is worth emphasizing because generic work abstractions often cause architectural regression.

We still have:

```
CandidateSource
    ↓
CandidateProposal
    ↓
Candidate
```

and separately:

```
Candidate
    ↓
AcquisitionPlan
    ↓
AcquisitionWork
    ↓
AcquisitionRuntime
```

Discovery does not secretly acquire.

Acquisition does not invent discovery semantics.

The common layer is only:

```
scheduling + lifecycle + ownership
```

---

<!-- CAP-362 | Continue Architecture Planning.md L65180–65184 | turn 45 | version 0.16 -->
### v0.16 — Acquisition

> **Source sections:** `CAP-362`

> How do we obtain something?

`AcquisitionRuntime + AcquisitionProvider`

<!-- CAP-442 | Continue Architecture Planning.md L67737–67794 | turn 49 | version 0.18 -->
## v0.18 — 18.18 Classification Must Not Become Acquisition Policy

> **Source sections:** `CAP-442`
>
> [DOCUMENTATION REVIEW] Contradiction **C-11** ([Review Notes](../REVIEW-NOTES.md#c-11--same-origin-default-versus-cross-origin-capability))

This boundary is critical.

Suppose:

```
Resource = PDF
Semantic type = service-manual
```

It does **not** automatically mean:

```
download it
```

Instead:

```
Classification
      ↓
Strategy Hint
      ↓
Acquisition Policy
      ↓
Capability Resolution
      ↓
Acquisition Runtime
```

So:

```
classified-as(service-manual)
```

may influence priority:

```
priority += 0.4
```

but should not bypass policy.

This preserves the earlier invariant:

```
classification ≠ authorization
```

and:

```
classification ≠ capability
```

---

<!-- CAP-476 | Continue Architecture Planning.md L68811–68864 | turn 51 | version 0.19 -->
## v0.19 — 19.13 Conditional Acquisition

> **Source sections:** `CAP-476`

The representation model also enables future acquisition optimization.

Instead of:

```
GET
download entire file
hash entire file
```

the engine can eventually perform:

```
HEAD /manual.pdf
        │
        ├── ETag unchanged
        │
        └── skip body acquisition
```

or:

```
GET
If-None-Match: "abc"
```

result:

```
304 Not Modified
```

Then:

```
existing artifact remains current
```

This introduces an important distinction:

```
discovery budget
≠
acquisition budget
≠
verification budget
```

That distinction will matter later.

---
