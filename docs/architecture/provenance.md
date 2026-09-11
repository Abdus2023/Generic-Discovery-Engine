# Provenance

> **Status:** DESIGNED
>
> **Source:** `Continue Architecture Planning.md`; `Userscript Discovery Prototype.md`
>
> **Purpose:** Provenance: parameter provenance, discovery trees, ledgers, explanations and provenance graphs.

## Source Sections

- **28. Parameter provenance** — `USP-045` — `Userscript Discovery Prototype.md` L1288–1339
- **29. The scanner should produce an explanation** — `USP-046` — `Userscript Discovery Prototype.md` L1341–1376
- **37. Candidate provenance creates a discovery tree** — `USP-060` — `Userscript Discovery Prototype.md` L1736–1773
- **v0.7 — 2. The ledger becomes the scan's causal trace** — `CAP-048` — `Continue Architecture Planning.md` L54165–54211
- **v0.7 — 5. The ledger is not merely logging** — `CAP-051` — `Continue Architecture Planning.md` L54330–54416
- **v0.13 — 13. Discovery provenance** — `CAP-203` — `Continue Architecture Planning.md` L60035–60076
- **v0.16 — 5. Provenance** — `CAP-317` — `Continue Architecture Planning.md` L63722–63774
- **v0.16 — 15. Provenance graph** — `CAP-327` — `Continue Architecture Planning.md` L64192–64240
- **v0.16 — 29. Candidate provenance** — `CAP-341` — `Continue Architecture Planning.md` L64758–64784
- **v0.16 — Provenance preservation** — `CAP-354` — `Continue Architecture Planning.md` L65039–65043
- **v0.16 — Session provenance** — `CAP-355` — `Continue Architecture Planning.md` L65045–65052
- **v0.17 — 22. Canonicalization provenance** — `CAP-394` — `Continue Architecture Planning.md` L66169–66195

## Related Documents

- [Discovery Model](discovery-model.md)
- [Evidence Model](evidence-model.md)
- [Invariants](../validation/invariants.md)
- [Persistence and Crash Recovery](persistence-and-recovery.md)

---

<!-- USP-045 | Userscript Discovery Prototype.md L1288–1339 | turn 9 | version ? -->
## 28. Parameter provenance

> **Source sections:** `USP-045`

For a serious implementation, every parameter should have provenance.

Instead of storing:

```
frequency = X
```

store:

```
frequency = X
source = measured
confidence = high
```

Or:

```
frequency = X
source = NIT
confidence = medium
```

Or:

```
frequency = X
source = user_configuration
confidence = high
```

This allows conflicting information to coexist without corrupting the database.

For example:

```
frequency:
    measured → X
    NIT      → Y
```

The engine can then decide whether this represents:

* a network change,
* a measurement error,
* two different receptions,
* or stale metadata.

---

<!-- USP-046 | Userscript Discovery Prototype.md L1341–1376 | turn 9 | version ? -->
## 29. The scanner should produce an explanation

> **Source sections:** `USP-046`

A particularly useful design feature is an **explainable discovery result**.

Instead of:

```
DVB multiplex found
```

return something conceptually like:

```
Discovery:
    type: DVB multiplex
    confidence: high

Evidence:
    RF energy detected
    carrier synchronized
    FEC synchronized
    valid MPEG transport stream
    PAT validated
    PMT validated
    DVB SI tables decoded

Origin:
    initially discovered by blind scan

Follow-up:
    additional candidates obtained from NIT
```

This is invaluable when diagnosing why a receiver found—or failed to find—something.

---

<!-- USP-060 | Userscript Discovery Prototype.md L1736–1773 | turn 11 | version ? -->
## 37. Candidate provenance creates a discovery tree

> **Source sections:** `USP-060`

Suppose a blind scan finds A.

A's metadata points to B and C.

B points to D.

You get:

```
Blind scan
    │
    ▼
    A
   / \
  B   C
  │
  D
```

Now the system knows **why** it found D.

That allows you to distinguish:

```
D found through network metadata
```

from:

```
D independently found through blind RF search
```

The latter is useful corroborating evidence.

---

<!-- CAP-048 | Continue Architecture Planning.md L54165–54211 | turn 27 | version 0.7 -->
## v0.7 — 2. The ledger becomes the scan's causal trace

> **Source sections:** `CAP-048`
>
> **Note:** explicit override

A typical sequence now looks like:

```
001 candidate-discovered
002 candidate-enqueued
003 candidate-claimed
004 acquisition-planned
005 slot-granted
006 request-started
007 request-completed
008 observation-recorded
009 provider-recognized
010 discovery-emitted
011 candidate-discovered
012 candidate-enqueued
013 candidate-completed
```

For a POST observed by the network bridge:

```
001 network-observed
```

but importantly:

```
NO

candidate → GET plan → POST endpoint
```

The engine therefore distinguishes:

```
OBSERVED NETWORK ACTIVITY
        ≠
DISCOVERED ACQUISITION TARGET
        ≠
AUTHORIZED ACQUISITION
```

That is a major correctness improvement.

---

<!-- CAP-051 | Continue Architecture Planning.md L54330–54416 | turn 27 | version 0.7 -->
## v0.7 — 5. The ledger is not merely logging

> **Source sections:** `CAP-051`
>
> **Note:** explicit override

This distinction matters.

Ordinary logging:

```
"Fetching https://example.com/api"
```

Ledger event:

```JavaScript
{
    seq: 17,
    type: "acquisition-planned",

    planId: "plan-...",
    candidateId: "candidate-...",

    target: "https://example.com/api",
    method: "GET",

    allowed: true,
    reason: null,

    priority: 0.83,
    expectedType: "api",

    policyVersion: 7
}
```

The latter is a **machine-readable decision record**.

That allows future tooling to ask:

```
Why was this URL fetched?
```

and answer:

```
Candidate:
    candidate-abc

Discovered by:
    javascript-url

Type:
    api

Depth:
    2

Priority:
    0.83

Policy:
    v7

Method:
    GET

Policy result:
    allowed

Budget:
    granted

Origin:
    slot granted

Observation:
    HTTP 200

Provider:
    json

New discoveries:
    14
```

That is much closer to an actual discovery system than a conventional crawler.

---

<!-- CAP-203 | Continue Architecture Planning.md L60035–60076 | turn 39 | version 0.13 -->
## v0.13 — 13. Discovery provenance

> **Source sections:** `CAP-203`

Each candidate should retain **all contributing discovery paths**.

Example:

```JavaScript
{
    candidateId: 'cand-17',

    provenance: [
        {
            sourceId: 'html-link',
            observationId: 'obs-4',
            evidenceId: 'ev-19'
        },
        {
            sourceId: 'sitemap',
            observationId: 'obs-9',
            evidenceId: 'ev-42'
        }
    ]
}
```

Thus the graph can say:

```
                ┌── HTML link ──────┐
                │                   │
                │                   ▼
Candidate ──────┼────────────── manual.pdf
                │                   ▲
                │                   │
                └── sitemap ────────┘
```

The resource is one identity.

The discovery paths are multiple.

---

<!-- CAP-317 | Continue Architecture Planning.md L63722–63774 | turn 45 | version 0.16 -->
## v0.16 — 5. Provenance

> **Source sections:** `CAP-317`

Every evidence object should answer:

```
WHO/WHAT produced it?
FROM WHAT?
WHEN?
HOW?
UNDER WHICH SESSION?
```

A minimal provenance object:

```JavaScript
{
    sessionId,
    observationId,
    providerId,
    mechanism,
    createdAt
}
```

For example:

```JavaScript
{
    sessionId: 'scan-001',
    observationId: 'obs-782',
    providerId: 'html',
    mechanism: 'anchor-href',
    createdAt: 1757500000000
}
```

This turns:

```
"found URL"
```

into:

```
"URL was extracted from attribute href of an anchor
in observation obs-782 using HTML recognition provider
html during scan-001."
```

That is a very different level of traceability.

---

<!-- CAP-327 | Continue Architecture Planning.md L64192–64240 | turn 45 | version 0.16 -->
## v0.16 — 15. Provenance graph

> **Source sections:** `CAP-327`

The resulting structure becomes:

```
                    SESSION
                       │
                       ▼
                   CANDIDATE
                       │
                  acquired-by
                       │
                       ▼
                 ACQUISITION
                       │
                    produces
                       │
                       ▼
                 OBSERVATION
                       │
                    produces
                       │
                       ▼
                   EVIDENCE
                       │
                    supports
                       │
                       ▼
                    CLAIM
                       │
                    concerns
                       │
                       ▼
                   RESOURCE
```

And discovery loops back:

```
RESOURCE
   │
   │ represented by
   ▼
CANDIDATE
```

This creates the complete provenance cycle without conflating the objects.

---

<!-- CAP-341 | Continue Architecture Planning.md L64758–64784 | turn 45 | version 0.16 -->
## v0.16 — 29. Candidate provenance

> **Source sections:** `CAP-341`

A candidate can now have:

```JavaScript
{
    id: 'candidate-42',

    resourceId: 'resource-17',

    evidenceIds: [
        'evidence-1',
        'evidence-7',
        'evidence-11'
    ],

    claimIds: [
        'claim-2'
    ]
}
```

But these should ideally be graph relationships rather than only denormalized arrays.

The arrays can remain as indexes for performance.

---

<!-- CAP-354 | Continue Architecture Planning.md L65039–65043 | turn 45 | version 0.16 -->
### v0.16 — Provenance preservation

> **Source sections:** `CAP-354`

```
Candidate convergence must preserve all discovery paths.
```

<!-- CAP-355 | Continue Architecture Planning.md L65045–65052 | turn 45 | version 0.16 -->
### v0.16 — Session provenance

> **Source sections:** `CAP-355`

```
Every observation/evidence-producing operation
belongs to a ScanSession.
```

---

<!-- CAP-394 | Continue Architecture Planning.md L66169–66195 | turn 47 | version 0.17 -->
## v0.17 — 22. Canonicalization provenance

> **Source sections:** `CAP-394`
>
> [DOCUMENTATION REVIEW] Contradiction **C-04** ([Review Notes](../REVIEW-NOTES.md#c-04--))

A useful addition:

```JavaScript
{
    rawTarget:
        'https://example.com/page?utm_source=x',

    canonicalTarget:
        'https://example.com/page',

    transformations: [
        'remove-tracking-param'
    ]
}
```

This makes normalization auditable.

The engine can then explain:

> These two candidates converged because the canonicalizer removed `utm_source`.

That is much better than unexplained deduplication.

---
