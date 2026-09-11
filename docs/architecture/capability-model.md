# Capability Model

> **Status:** DESIGNED
>
> **Source:** `Continue Architecture Planning.md`
>
> **Purpose:** Capabilities as first-class objects: the capability lattice, contracts and capability resolution.

## Source Sections

- **v0.8 — Capability-Aware Acquisition Runtime** — `CAP-056` — `Continue Architecture Planning.md` L54631–54653
- **v0.8 — 1. The three graphs** — `CAP-057` — `Continue Architecture Planning.md` L54655–54681
- **v0.8 — Discovery graph** — `CAP-058` — `Continue Architecture Planning.md` L54683–54695
- **v0.8 — Evidence graph** — `CAP-060` — `Continue Architecture Planning.md` L54712–54729
- **v0.8 — 2. Capability is now a first-class object** — `CAP-061` — `Continue Architecture Planning.md` L54731–54803
- **v0.8 — 3. Capability lattice** — `CAP-062` — `Continue Architecture Planning.md` L54805–54839
- **v0.8 — 4. Capability contract** — `CAP-063` — `Continue Architecture Planning.md` L54841–54905
- **v0.8 — 5. Candidate requirements** — `CAP-064` — `Continue Architecture Planning.md` L54907–54968
- **v0.8 — 7. Why this matters for generic discovery** — `CAP-066` — `Continue Architecture Planning.md` L55046–55104
- **v0.8 — 9. Capability provenance** — `CAP-068` — `Continue Architecture Planning.md` L55204–55257
- **v0.8 — 10. The four-level authorization model** — `CAP-069` — `Continue Architecture Planning.md` L55259–55301
- **v0.8 — 11. New graph model** — `CAP-070` — `Continue Architecture Planning.md` L55303–55340
- **v0.8 — 12. v0.8 ledger** — `CAP-071` — `Continue Architecture Planning.md` L55342–55402
- **v0.8 — 13. Important architectural consequence** — `CAP-072` — `Continue Architecture Planning.md` L55404–55458
- **v0.8 — 14. v0.8 scope boundary** — `CAP-073` — `Continue Architecture Planning.md` L55460–55462
- **v0.8 — Implement** — `CAP-074` — `Continue Architecture Planning.md` L55464–55472
- **v0.8 — Represent but deny** — `CAP-075` — `Continue Architecture Planning.md` L55474–55491

## Related Documents

- [Provider Architecture](provider-architecture.md)
- [Acquisition Model](../acquisition/acquisition-model.md)
- [Invariants](../validation/invariants.md)

---

<!-- CAP-056 | Continue Architecture Planning.md L54631–54653 | turn 29 | version 0.8 -->
## v0.8 — Capability-Aware Acquisition Runtime

> **Source sections:** `CAP-056`

v0.7.1 established the **decision boundary**:

```
Candidate
    ↓
Policy
    ↓
AcquisitionPlan
    ↓
Scheduler
    ↓
Acquisition
```

v0.8 makes the next distinction explicit:

> **A target is not just a URL. It is a resource requiring a set of acquisition capabilities.**

This is the point where the engine starts moving from a crawler toward a **generic discovery runtime**.

---

<!-- CAP-057 | Continue Architecture Planning.md L54655–54681 | turn 29 | version 0.8 -->
## v0.8 — 1. The three graphs

> **Source sections:** `CAP-057`

The v0.8 architecture should stop treating everything as one graph.

```
                    ┌─────────────────────┐
                    │   DISCOVERY GRAPH   │
                    │                     │
                    │ "How did we find it?"│
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  ACQUISITION GRAPH │
                    │                     │
                    │ "How may we get it?"│
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    EVIDENCE GRAPH  │
                    │                     │
                    │ "What did we observe?"│
                    └─────────────────────┘
```

These answer three different questions.

<!-- CAP-058 | Continue Architecture Planning.md L54683–54695 | turn 29 | version 0.8 -->
### v0.8 — Discovery graph

> **Source sections:** `CAP-058`

```
HTML page
   │
   └── script
         │
         └── API endpoint
```

Meaning:

> The API endpoint was discovered through a JavaScript resource.

<!-- CAP-060 | Continue Architecture Planning.md L54712–54729 | turn 29 | version 0.8 -->
### v0.8 — Evidence graph

> **Source sections:** `CAP-060`

```
API endpoint
   │
   └── Observation #42
          │
          ├── HTTP 200
          ├── application/json
          ├── fingerprint
          └── timestamp
```

Meaning:

> This is what actually happened when acquisition was attempted.

---

<!-- CAP-061 | Continue Architecture Planning.md L54731–54803 | turn 29 | version 0.8 -->
## v0.8 — 2. Capability is now a first-class object

> **Source sections:** `CAP-061`

Instead of:

```JavaScript
candidate.type === "api"
```

we move toward:

```JavaScript
candidate.requirements
```

For example:

```JavaScript
{
    method: "GET",

    capabilities: [
        "network.http",
        "same-origin",
        "text-response"
    ]
}
```

A more interesting target:

```JavaScript
{
    target: "https://example.com/report.pdf",

    capabilities: [
        "network.http",
        "same-origin",
        "binary-response"
    ]
}
```

And a browser-context resource:

```JavaScript
{
    target: "https://example.com/dashboard",

    capabilities: [
        "browser-context",
        "session-context",
        "network.http"
    ]
}
```

The important consequence:

```
TYPE
 ≠
CAPABILITY
```

An `api` candidate may require HTTP GET.

A `frame` candidate may require browser-context acquisition.

A discovered PDF may require binary acquisition.

A POST endpoint may be observable but not executable by the current runtime.

---

<!-- CAP-062 | Continue Architecture Planning.md L54805–54839 | turn 29 | version 0.8 -->
## v0.8 — 3. Capability lattice

> **Source sections:** `CAP-062`

The initial capability model can remain deliberately small.

```
                    acquisition
                         │
             ┌───────────┴───────────┐
             │                       │
         network                 browser
             │                       │
       ┌─────┴─────┐           ┌─────┴─────┐
       │           │           │           │
      HTTP       DNS*       context     session*
       │
   ┌───┴────┐
   │        │
  GET    binary
   │
 textual
```

`DNS` and authenticated/session capabilities are deliberately not implemented merely because they can be represented.

That distinction matters:

```
REPRESENTABLE
    ≠
AVAILABLE
    ≠
AUTHORIZED
```

---

<!-- CAP-063 | Continue Architecture Planning.md L54841–54905 | turn 29 | version 0.8 -->
## v0.8 — 4. Capability contract

> **Source sections:** `CAP-063`

Introduce a small contract:

```JavaScript
class CapabilitySet {
    constructor(values = []) {
        this.values = new Set(values);
    }

    has(capability) {
        return this.values.has(capability);
    }

    add(capability) {
        this.values.add(capability);
        return this;
    }

    hasAll(required) {
        return required.every(
            capability =>
                this.values.has(capability)
        );
    }

    missing(required) {
        return required.filter(
            capability =>
                !this.values.has(capability)
        );
    }

    serialize() {
        return [...this.values].sort();
    }
}
```

The runtime advertises:

```JavaScript
const RUNTIME_CAPABILITIES =
    new CapabilitySet([
        'network.http',
        'network.get',
        'same-origin',
        'text-response'
    ]);
```

It therefore does **not** advertise:

```
network.post
network.put
network.delete
browser.privileged
credential.access
filesystem.write
```

This makes the safety boundary explicit.

---

<!-- CAP-064 | Continue Architecture Planning.md L54907–54968 | turn 29 | version 0.8 -->
## v0.8 — 5. Candidate requirements

> **Source sections:** `CAP-064`

A candidate can now carry:

```JavaScript
{
    target,
    type,

    requirements: {
        method: "GET",

        capabilities: [
            "network.http",
            "network.get",
            "same-origin"
        ]
    }
}
```

But there is an important design rule:

> Discovery mechanisms should propose requirements; policy determines whether those requirements can be satisfied.

For example:

```
HTML <form method="POST">
        │
        ▼
Candidate
        │
        ├── method = POST
        └── capability = network.post
```

The candidate is valid.

The acquisition is simply unsupported.

That means:

```
POST endpoint discovered
        │
        ▼
candidate exists
        │
        ▼
plan generated
        │
        ▼
capability missing
        │
        ▼
SKIPPED
```

We don't need to pretend that the discovery itself was invalid.

---

<!-- CAP-066 | Continue Architecture Planning.md L55046–55104 | turn 29 | version 0.8 -->
## v0.8 — 7. Why this matters for generic discovery

> **Source sections:** `CAP-066`

Consider three resources discovered from the same JavaScript file:

```
/api/catalog
/api/order
/report.pdf
```

Their discovery origin is identical:

```
script.js
   ├── /api/catalog
   ├── /api/order
   └── /report.pdf
```

But acquisition requirements differ:

```
/api/catalog
    GET
    textual
    same-origin

/api/order
    POST
    request-body
    session-dependent

/report.pdf
    GET
    binary
    same-origin
```

A type-only engine struggles with this.

A capability-aware engine can represent all three:

```
                 discovered
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
       catalog      order      PDF
          │          │          │
         GET        POST       GET
          │          │          │
        allowed    denied    denied*
```

`*` only if binary acquisition remains disabled.

No special crawler logic is required.

---

<!-- CAP-068 | Continue Architecture Planning.md L55204–55257 | turn 29 | version 0.8 -->
## v0.8 — 9. Capability provenance

> **Source sections:** `CAP-068`

There is another subtle distinction.

Where did the requirement come from?

```
HTML
 │
 └── form method=POST
          │
          ▼
    requirement:
       network.post
```

or:

```
Network bridge
 │
 └── observed POST
          │
          ▼
    requirement:
       network.post
```

Therefore requirements themselves should have provenance:

```JavaScript
{
    capability: 'network.post',

    source: {
        mechanism: 'network-observation',
        observationId: 'obs-123'
    }
}
```

This gives us:

```
WHY does this candidate require POST?
```

not merely:

```
IT requires POST.
```

---

<!-- CAP-069 | Continue Architecture Planning.md L55259–55301 | turn 29 | version 0.8 -->
## v0.8 — 10. The four-level authorization model

> **Source sections:** `CAP-069`

At this point the engine has four distinct gates:

```
             DISCOVERED
                  │
                  ▼
            REPRESENTABLE
                  │
                  ▼
             CAPABLE
                  │
                  ▼
            POLICY-ALLOWED
                  │
                  ▼
             SCHEDULABLE
                  │
                  ▼
             EXECUTABLE
```

These must not be collapsed.

For example:

```
POST endpoint
    │
    ├── discovered        YES
    ├── representable     YES
    ├── runtime capable   NO
    ├── policy allowed    NO
    ├── schedulable       NO
    └── executable        NO
```

That is a **successful discovery with an unsuccessful acquisition**.

Those are completely different outcomes.

---

<!-- CAP-070 | Continue Architecture Planning.md L55303–55340 | turn 29 | version 0.8 -->
## v0.8 — 11. New graph model

> **Source sections:** `CAP-070`

The graph now looks like:

```
                   ┌──────────────┐
                   │   Candidate  │
                   └──────┬───────┘
                          │
             ┌────────────┼─────────────┐
             │            │             │
             ▼            ▼             ▼
        Discovery     Requirement    Resource
          edges          edges         identity
             │            │             │
             │            ▼             │
             │       Capabilities      │
             │            │             │
             │            ▼             │
             │       Policy Decision    │
             │            │             │
             │            ▼             │
             │     Acquisition Plan     │
             │            │             │
             │            ▼             │
             │        Execution         │
             │            │             │
             └────────────┼─────────────┘
                          ▼
                     Observation
                          │
                          ▼
                       Evidence
```

This is much closer to a knowledge graph than a queue of URLs.

---

<!-- CAP-071 | Continue Architecture Planning.md L55342–55402 | turn 29 | version 0.8 -->
## v0.8 — 12. v0.8 ledger

> **Source sections:** `CAP-071`

The event ledger should gain capability events:

```
candidate-discovered
candidate-enqueued
candidate-claimed

requirements-derived

capability-resolution
capability-missing

acquisition-planned

policy-denied
budget-denied
slot-granted

request-started
request-completed

observation-recorded

provider-recognized
discovery-emitted

candidate-retried
candidate-completed
candidate-skipped
```

Example:

```
421 requirements-derived
422 capability-resolution
423 capability-missing
424 acquisition-planned
425 policy-denied
426 candidate-skipped
```

Now the complete causal explanation is available:

```
Why wasn't /api/order fetched?

→ discovered from script.js
→ recognized as POST
→ POST capability required
→ runtime only exposes GET
→ capability resolution failed
→ acquisition plan denied
→ candidate skipped
```

No guesswork.

---

<!-- CAP-072 | Continue Architecture Planning.md L55404–55458 | turn 29 | version 0.8 -->
## v0.8 — 13. Important architectural consequence

> **Source sections:** `CAP-072`

The engine now has a clean separation:

```
             DISCOVERY PLANE
                    │
                    ▼
              WHAT EXISTS?
                    │
                    ▼
             KNOWLEDGE GRAPH
                    │
                    ▼
            WHAT IS REQUIRED?
                    │
                    ▼
            CAPABILITY PLANE
                    │
                    ▼
             WHAT IS POSSIBLE?
                    │
                    ▼
              POLICY PLANE
                    │
                    ▼
              WHAT IS ALLOWED?
                    │
                    ▼
             SCHEDULING PLANE
                    │
                    ▼
              WHAT NOW?
                    │
                    ▼
             ACQUISITION
                    │
                    ▼
             WHAT HAPPENED?
                    │
                    ▼
              EVIDENCE PLANE
```

This gives us a much stronger abstraction than:

```
URL crawler
```

The engine is becoming:

> **A bounded system for discovering resources, deriving acquisition requirements, resolving capabilities, making explicit authorization decisions, and recording observations.**

---

<!-- CAP-073 | Continue Architecture Planning.md L55460–55462 | turn 29 | version 0.8 -->
## v0.8 — 14. v0.8 scope boundary

> **Source sections:** `CAP-073`

We should deliberately **not** implement everything represented by the capability system.

<!-- CAP-074 | Continue Architecture Planning.md L55464–55472 | turn 29 | version 0.8 -->
### v0.8 — Implement

> **Source sections:** `CAP-074`

```
network.http
network.get
same-origin
text-response
binary-response [optional]
```

<!-- CAP-075 | Continue Architecture Planning.md L55474–55491 | turn 29 | version 0.8 -->
### v0.8 — Represent but deny

> **Source sections:** `CAP-075`

```
network.post
network.put
network.delete
request-body
credential.access
browser.privileged
filesystem
cross-origin
```

This is important because otherwise the abstraction starts becoming an excuse to expand permissions.

The capability registry describes the **runtime contract**, not a wish list.

---
