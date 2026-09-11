# Concept Overview

> **Status:** DESIGNED
>
> **Source:** `Continue Architecture Planning.md`
>
> **Purpose:** How the project describes itself at the conceptual level: what generic discovery is, what the DVB analogy contributed, and which principles are held invariant.

## Contents

- **v0.7 — The deeper abstraction** — `Continue Architecture Planning.md` L48802–48856
- **v0.10 — What v0.10 accomplishes** — `Continue Architecture Planning.md` L57235–57297
- **v0.12 — 20. The deeper abstraction** — `Continue Architecture Planning.md` L59356–59396
- **v0.17 — 32. The deeper model** — `Continue Architecture Planning.md` L66562–66606
- **v0.18 — 18.24 The Larger Concept** — `Continue Architecture Planning.md` L68044–68081
- **v0.21 — 21.31 The Important Conceptual Shift** — `Continue Architecture Planning.md` L72580–72636
- **v0.22 — 22.26 The conceptual jump** — `Continue Architecture Planning.md` L73998–74027
- **v0.23 — 23.25 v0.23 conceptual result** — `Continue Architecture Planning.md` L75289–75323
- **v0.26 — 26.30 What v0.26 actually gives us** — `Continue Architecture Planning.md` L80108–80160
- **v0.30 — Conclusion — Generic Discovery Engine** — `Continue Architecture Planning.md` L84697–84760
- **v0.30 — Final principles** — `Continue Architecture Planning.md` L85068–85125
- **v0.30 — 30.26 What v0.30 actually accomplishes** — `Continue Architecture Planning.md` L86358–86398
- **v0.34 — Conclusion — Generic Discovery Engine** — `Continue Architecture Planning.md` L91982–92057
- **v0.34 — The decisive conceptual shift** — `Continue Architecture Planning.md` L92059–92087
- **v0.34 — What the prototype actually becomes** — `Continue Architecture Planning.md` L92190–92237
- **v0.34 — Final formulation** — `Continue Architecture Planning.md` L92239–92275

## Related Documents

- [README.md](../README.md)
- [Generic Discovery](generic-discovery.md)
- [The Discovery Loop](discovery-loop.md)
- [Architecture Overview](../architecture/overview.md)
- [DVB Blind Scan](../research/dvb-blind-scan.md)

---

<!-- source: Continue Architecture Planning.md L48802–48856 | turn 25 | version 0.7 -->
## v0.7 — The deeper abstraction

At this point the DVB analogy becomes much clearer.

DVB blind scanning is essentially:

```
search space
     ↓
probe
     ↓
signal observation
     ↓
recognition
     ↓
service discovery
     ↓
new searchable entities
```

The generic web version becomes:

```
candidate space
     ↓
acquisition plan
     ↓
HTTP/browser observation
     ↓
content recognition
     ↓
resource discovery
     ↓
new candidates
```

So the userscript is no longer best described as a **crawler**.

A better name for the architecture is:

> **Generic Discovery Engine = bounded hypothesis-space exploration over observable resources.**

The next implementation step after this is **v0.7.1: replayable acquisition decisions + deterministic event ledger**, which would make a scan explainable as:

```
Why was this candidate discovered?
Why was it prioritized?
Why was it allowed?
Why was it skipped?
Why was it fetched?
What observation resulted?
What new candidates did that observation produce?
```

That is the point where the prototype starts becoming an **instrumentable discovery system**, rather than just a sophisticated userscript crawler.

<!-- source: Continue Architecture Planning.md L57235–57297 | turn 33 | version 0.10 -->
## v0.10 — What v0.10 accomplishes

The userscript is no longer fundamentally:

```
"crawl URLs concurrently"
```

It is becoming:

```
DISCOVER
   ↓
MODEL
   ↓
PLAN
   ↓
AUTHORIZE
   ↓
ADMIT
   ↓
EXECUTE
   ↓
OBSERVE
   ↓
RECOGNIZE
   ↓
EXPAND
```

And the DVB blind-scan analogy is now structurally sharper:

```
DVB tuner/resource
       ↓
candidate acquisition
       ↓
signal observation
       ↓
lock/recognition
       ↓
service discovery
       ↓
new candidates
```

maps to:

```
Generic resource
       ↓
acquisition plan
       ↓
controlled acquisition
       ↓
response observation
       ↓
provider recognition
       ↓
resource discovery
       ↓
new candidates
```

<!-- source: Continue Architecture Planning.md L59356–59396 | turn 37 | version 0.12 -->
## v0.12 — 20. The deeper abstraction

At v0.12, the system can finally be described without mentioning URLs:

```
Search Space
    ↓
Candidate Generation
    ↓
Candidate Normalization
    ↓
Candidate Scheduling
    ↓
Acquisition Planning
    ↓
Controlled Execution
    ↓
Observation
    ↓
Recognition
    ↓
Evidence Extraction
    ↓
Candidate Generation
```

That is the generic algorithm.

The web is merely **one runtime instance**.

DVB is another possible analogy.

A filesystem scanner could be another.

A document repository scanner could be another.

An API topology explorer could be another.

A software-package dependency discovery system could be another.

---

<!-- source: Continue Architecture Planning.md L66562–66606 | turn 47 | version 0.17 -->
## v0.17 — 32. The deeper model

At this point, the generic discovery engine has three graphs:

```
┌─────────────────────────────────────────────┐
│              EXECUTION GRAPH                │
│                                             │
│ Domain → Session → Work → Attempt → Event   │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│              DISCOVERY GRAPH                │
│                                             │
│ Source → Evidence → Candidate → Expansion   │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│               RESOURCE GRAPH                │
│                                             │
│ Locator ↔ Resource ↔ Relation ↔ Revision    │
└─────────────────────────────────────────────┘
```

And the EvidenceGraph connects them:

```
Execution
   │
   ▼
Observation
   │
   ▼
Evidence
   │
   ├──────────────► Candidate
   │
   ├──────────────► Claim
   │
   └──────────────► Resource Relation
```

This is a much more complete model of discovery than a conventional crawler queue.

---

<!-- source: Continue Architecture Planning.md L68044–68081 | turn 49 | version 0.18 -->
## v0.18 — 18.24 The Larger Concept

We now have five increasingly distinct questions:

```
1. Candidate
   "Could something exist here?"

2. Acquisition
   "May/can we obtain it?"

3. Observation
   "What actually happened when we obtained it?"

4. Resource
   "What logical thing does this locator refer to?"

5. Classification
   "What kind of thing is that resource?"
```

That gives the engine a much cleaner epistemic pipeline:

```
POSSIBILITY
    ↓
AUTHORIZATION
    ↓
OBSERVATION
    ↓
IDENTITY
    ↓
INTERPRETATION
```

This is considerably closer to a generic discovery system than simply treating URLs as a queue.

---

<!-- source: Continue Architecture Planning.md L72580–72636 | turn 55 | version 0.21 -->
## v0.21 — 21.31 The Important Conceptual Shift

The original engine looked like:

```
URL queue
   ↓
HTTP
   ↓
parse
   ↓
more URLs
```

The architecture is now:

```
                    UNKNOWN SEARCH UNIVERSE
                              │
                              ▼
                         DOMAIN BOUNDARY
                              │
                              ▼
                        SEARCH PARTITIONS
                              │
                              ▼
                    ADAPTIVE EXPLORATION
                              │
                              ▼
                           PROBES
                              │
                              ▼
                        OBSERVATIONS
                              │
                              ▼
                           EVIDENCE
                              │
                              ▼
                          RESOURCES
                              │
                  ┌───────────┴───────────┐
                  ▼                       ▼
             CLASSIFICATION          RELATIONS
                  │                       │
                  └───────────┬───────────┘
                              ▼
                       SEARCH EXPANSION
                              │
                              ▼
                     NEW SEARCH PARTITIONS
                              │
                              └──────────────► ...
```

That recursive structure is the real payoff of the DVB blind-scan abstraction.

---

<!-- source: Continue Architecture Planning.md L73998–74027 | turn 57 | version 0.22 -->
## v0.22 — 22.26 The conceptual jump

At v0.21 the engine could answer:

> **“What should I explore next?”**

At v0.22 it can begin answering:

> **“How much of the defined search space have I actually explored?”**

And, under sufficiently strong conditions:

> **“What evidence supports saying this bounded search is complete?”**

That creates three different outputs:

```
DISCOVERY RESULT
    "I found these resources."

COVERAGE RESULT
    "I explored these parts of the defined search space."

ASSURANCE RESULT
    "These conditions justify this level of completeness."
```

Those should never be collapsed into one `scanComplete` boolean.

---

<!-- source: Continue Architecture Planning.md L75289–75323 | turn 59 | version 0.23 -->
## v0.23 — 23.25 v0.23 conceptual result

The engine has now evolved from:

```
Crawler
```

into:

```
Discovery + Acquisition + Evidence + Search Assurance System
```

The architecture can distinguish:

```
What did we find?
        ↓
What did we observe?
        ↓
Why do we believe it?
        ↓
What did we not find?
        ↓
Why didn't we find it?
        ↓
Can we justify saying it is absent?
        ↓
How complete was the search?
```

That is a substantially stronger foundation for the eventual **service-document universe**.

---

<!-- source: Continue Architecture Planning.md L80108–80160 | turn 65 | version 0.26 -->
## v0.26 — 26.30 What v0.26 actually gives us

The architecture now has a complete path from **search intent to bounded execution**:

```
                         WHY?
                          │
                         Goal
                          │
                         WHAT?
                          │
                     QueryPlan
                          │
                     QueryStep
                          │
                     HOW/WHEN?
                          │
                  TacticExecution
                          │
                       Runtime
                          │
                     Strategy
                          │
                       Probe
                          │
                    Observation
                          │
                      Evidence
                          │
                     Candidate
```

The important new capability is **resumable search execution**.

The system is no longer merely:

```
crawl → extract → enqueue
```

It is becoming:

```
goal
 → explicit search plan
 → bounded tactic
 → checkpointed execution
 → evidence-producing exploration
 → candidate convergence
 → measurable coverage
```

That is much closer to the original blind-scan abstraction: **systematically traverse a defined search space, remember where the scan reached, distinguish discovered signal from unexplored space, and make exhaustion an explicit claim rather than an assumption.**

<!-- source: Continue Architecture Planning.md L84697–84760 | turn 73 | version 0.30 -->
## v0.30 — Conclusion — Generic Discovery Engine

The DVB blind-scan analogy has now produced a much more general architecture.

The important result is **not** “a web crawler that behaves like DVB scanning.”

It is a general model for **bounded, evidence-producing exploration of an unknown resource universe**.

```
                         SEARCH GOAL
                             │
                             ▼
                       QUERY PLANNER
                             │
                             ▼
                         QUERY PLAN
                             │
                             ▼
                       TACTIC RUNTIME
                             │
                             ▼
                       SEARCH SPACE
                             │
                 ┌───────────┴───────────┐
                 ▼                       ▼
            PARTITIONS              EXPANSION
                 │                       │
                 ▼                       │
          ADAPTIVE STRATEGY              │
                 │                       │
                 ▼                       │
             FRONTIER ◄─────────────────┘
                 │
          ┌──────┼─────────┐
          ▼      ▼         ▼
      discovery acquisition enumeration
          │      │         │
          └──────┼─────────┘
                 ▼
             ACQUISITION
                 │
                 ▼
             OBSERVATION
                 │
                 ▼
           RECOGNITION
                 │
          ┌──────┼──────────┐
          ▼      ▼          ▼
       EVIDENCE CLASSIFICATION ARTIFACT
          │      │          │
          └──────┼──────────┘
                 ▼
             RESOURCE
                 │
                 ▼
             RELEVANCE
                 │
                 ▼
              COVERAGE
                 │
                 ▼
          COMPLETENESS CLAIM
```

<!-- source: Continue Architecture Planning.md L85068–85125 | turn 73 | version 0.30 -->
## v0.30 — Final principles

1. **Discovery is not acquisition.**
2. **A candidate is not a resource.**
3. **A resource is not an artifact.**
4. **An observation is not automatically evidence of a stronger claim.**
5. **Classification is an assertion backed by evidence.**
6. **Relevance is goal-relative.**
7. **Coverage is search-space-relative.**
8. **Exhaustion is not completeness.**
9. **Not found is not absent.**
10. **Dynamic expansion produces proposals, not authority.**
11. **Adaptive optimization cannot override policy.**
12. **Deduplication must preserve provenance.**
13. **Overlap must not be counted as independent coverage.**
14. **Every resumable traversal needs durable progress.**
15. **Every externally meaningful decision should be replayable/explainable.**
16. **Failure must remain distinguishable from absence.**
17. **Historical claims must remain immutable and scoped to their search-space snapshot.**
18. **The frontier is the operational representation of unfinished knowledge.**

The deepest abstraction is therefore:

```
              UNKNOWN UNIVERSE
                     │
                     ▼
              BOUNDED SEARCH SPACE
                     │
                     ▼
               SYSTEMATIC EXPLORATION
                     │
                     ▼
                 OBSERVATION
                     │
                     ▼
             EVIDENCE-BACKED KNOWLEDGE
                     │
                     ▼
              SEARCH-SPACE EXPANSION
                     │
                     └──────────────┐
                                    │
                                    ▼
                              MORE EXPLORATION
                                    │
                                    ▼
                              COVERAGE / LIMITS
                                    │
                                    ▼
                         JUSTIFIED TERMINATION
```

That is the **Generic Discovery Algorithm inspired by DVB Blind Scan**.

The DVB part is the inspiration.

The actual abstraction is **evidence-driven, bounded, resumable search over an evolving search space**.

<!-- source: Continue Architecture Planning.md L86358–86398 | turn 75 | version 0.30 -->
## v0.30 — 30.26 What v0.30 actually accomplishes

Before v0.30:

```
Many work types
       ↓
one frontier
       ↓
potential competition
```

After v0.30:

```
Many work types
       ↓
admission
       ↓
fairness
       ↓
utility
       ↓
cost
       ↓
arbitration
       ↓
atomic claim
       ↓
execution
```

The system has therefore acquired a **control plane for exploration**.

This is an important transition.

Up to v0.29, the architecture primarily described **how knowledge expands**.

v0.30 begins defining **how finite computational resources are allocated among competing knowledge-expansion processes**.

---

<!-- source: Continue Architecture Planning.md L91982–92057 | turn 85 | version 0.34 -->
## v0.34 — Conclusion — Generic Discovery Engine

The DVB blind-scan analogy has now produced a much stronger abstraction than “URL crawler.”

The essential idea is:

> **A Generic Discovery Engine is a bounded, evidence-driven, resumable search system that progressively discovers and explores an evolving resource universe.**

Its architecture can be reduced to this:

```
                         SEARCH GOAL
                             │
                             ▼
                        QUERY PLAN
                             │
                             ▼
                         SEARCH SPACE
                             │
                    ┌────────┴────────┐
                    ▼                 ▼
               PARTITIONS          STRATEGIES
                    │                 │
                    └────────┬────────┘
                             ▼
                         DISCOVERY
                             │
                             ▼
                         CANDIDATES
                             │
                             ▼
                    FRONTIER RUNTIME
                             │
                   ┌─────────┴─────────┐
                   ▼                   ▼
              ARBITRATION          BUDGET
                   │                   │
                   └─────────┬─────────┘
                             ▼
                        COORDINATION
                             │
                     ┌───────┴───────┐
                     ▼               ▼
                  WORKER A        WORKER B
                     │               │
                     └───────┬───────┘
                             ▼
                       CONSISTENCY
                             │
                       ┌─────┴─────┐
                       ▼           ▼
                    COMMIT      CONFLICT
                                  │
                               RESOLVE
                                  │
                       ┌──────────┴──────────┐
                       ▼                     ▼
                  ACQUISITION            EVIDENCE
                       │                     │
                       ▼                     ▼
                   OBSERVATION ───────► KNOWLEDGE
                                             │
                              ┌──────────────┼──────────────┐
                              ▼              ▼              ▼
                         CLASSIFICATION  VERIFICATION   RELEVANCE
                              │              │              │
                              └──────────────┼──────────────┘
                                             ▼
                                      RESOURCE GRAPH
                                             │
                                             ▼
                                      COVERAGE MODEL
                                             │
                                             ▼
                                    COMPLETENESS CLAIM
```

<!-- source: Continue Architecture Planning.md L92059–92087 | turn 85 | version 0.34 -->
## v0.34 — The decisive conceptual shift

The engine is **not** fundamentally:

```
URL → fetch → parse → more URLs
```

It is:

```
Unknown Search Universe
        ↓
Bounded Search Space
        ↓
Systematic Exploration
        ↓
Evidence
        ↓
Knowledge
        ↓
New Search Space
        ↓
Systematic Exploration
        ↓
...
```

That makes the DVB analogy precise.

<!-- source: Continue Architecture Planning.md L92190–92237 | turn 85 | version 0.34 -->
## v0.34 — What the prototype actually becomes

The original userscript idea has therefore evolved from a crawler into a prototype of a:

```
                    GENERIC DISCOVERY ENGINE

        bounded
        systematic
        resumable
        evidence-driven
        policy-controlled
        capability-aware
        provenance-preserving
        concurrency-safe
        conflict-aware
        coverage-aware
        completeness-conscious
```

But one boundary should remain explicit:

> **The userscript does not prove completeness of the open web.**

It can prove things such as:

```
this partition was enumerated
this cursor was exhausted
these candidates were observed
these artifacts were acquired
these bytes have this digest
these classifications have this evidence
these regions were inaccessible
these strategies were attempted
this budget was consumed
this frontier is currently exhausted
```

It generally cannot prove:

```
nothing else exists anywhere on the web
```

That distinction is fundamental.

---

<!-- source: Continue Architecture Planning.md L92239–92275 | turn 85 | version 0.34 -->
## v0.34 — Final formulation

The strongest concise definition is:

> **Generic Discovery Engine is a bounded, resumable, evidence-producing search runtime that systematically explores an evolving search space, converts observations into provenance-bearing knowledge, expands its frontier from discovered structure, and maintains explicit semantics for authorization, resource consumption, concurrency, coverage, uncertainty, and completeness.**

And the DVB inspiration can be stated even more compactly:

```
BLIND SCAN
    =
systematic exploration
    +
observation
    +
discovery
    +
frontier expansion
    +
checkpointing
    +
explicit exhaustion
```

The web/document generalization preserves exactly those properties while replacing:

```
frequency → signal → transport
```

with:

```
partition → probe → observation → resource
```

That is the core result of the architecture from **v0.6 through v0.34**.
