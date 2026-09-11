# Invariants

> **Status:** DESIGNED
>
> **Source:** `Continue Architecture Planning.md`
>
> **Purpose:** Every invariant recorded in the planning conversation, grouped by the version that introduced it.

## Contents

- **v0.8 — 15. Updated system invariant** — `Continue Architecture Planning.md` L55493–55532
- **v0.9 — 10. v0.9 invariants** — `Continue Architecture Planning.md` L56193–56195
- **v0.9 — I1 — Discovery independence** — `Continue Architecture Planning.md` L56197–56201
- **v0.9 — I2 — Policy independence** — `Continue Architecture Planning.md` L56203–56207
- **v0.9 — I3 — Capability soundness** — `Continue Architecture Planning.md` L56209–56215
- **v0.9 — I4 — Method safety** — `Continue Architecture Planning.md` L56217–56223
- **v0.9 — I5 — Provenance** — `Continue Architecture Planning.md` L56225–56231
- **v0.9 — I6 — Observation integrity** — `Continue Architecture Planning.md` L56233–56241
- **v0.9 — I7 — Replay distinction** — `Continue Architecture Planning.md` L56243–56253
- **v0.12 — 18. v0.12 invariants** — `Continue Architecture Planning.md` L59208–59208
- **v0.12 — S1 — Source purity** — `Continue Architecture Planning.md` L59210–59215
- **v0.12 — S2 — Core ownership** — `Continue Architecture Planning.md` L59217–59222
- **v0.12 — S3 — Proposal semantics** — `Continue Architecture Planning.md` L59224–59228
- **v0.12 — S4 — Identity** — `Continue Architecture Planning.md` L59230–59235
- **v0.12 — S5 — Provenance** — `Continue Architecture Planning.md` L59237–59242
- **v0.12 — S6 — Representability** — `Continue Architecture Planning.md` L59244–59249
- **v0.12 — S7 — Observation independence** — `Continue Architecture Planning.md` L59251–59265
- **v0.13 — 20. v0.13 invariants** — `Continue Architecture Planning.md` L60327–60327
- **v0.13 — D1 — Source isolation** — `Continue Architecture Planning.md` L60329–60334
- **v0.13 — D2 — Acquisition isolation** — `Continue Architecture Planning.md` L60336–60341
- **v0.13 — D3 — Normalization ownership** — `Continue Architecture Planning.md` L60343–60348
- **v0.13 — D4 — Bounded generation** — `Continue Architecture Planning.md` L60350–60355
- **v0.13 — D5 — Bounded recursion** — `Continue Architecture Planning.md` L60357–60362
- **v0.13 — D6 — Provenance preservation** — `Continue Architecture Planning.md` L60364–60369
- **v0.13 — D7 — Atomic task claiming** — `Continue Architecture Planning.md` L60371–60376
- **v0.13 — D8 — Convergence** — `Continue Architecture Planning.md` L60378–60383
- **v0.13 — D9 — Discovery/acquisition independence** — `Continue Architecture Planning.md` L60385–60392
- **v0.14 — 24. Strong invariants** — `Continue Architecture Planning.md` L61789–61789
- **v0.14 — Domain invariant** — `Continue Architecture Planning.md` L61791–61797
- **v0.14 — Session invariant** — `Continue Architecture Planning.md` L61799–61803
- **v0.14 — Snapshot invariant** — `Continue Architecture Planning.md` L61805–61809
- **v0.14 — Frontier invariant** — `Continue Architecture Planning.md` L61811–61816
- **v0.14 — Termination invariant** — `Continue Architecture Planning.md` L61818–61822
- **v0.14 — Recovery invariant** — `Continue Architecture Planning.md` L61824–61829
- **v0.14 — Provenance invariant** — `Continue Architecture Planning.md` L61831–61836
- **v0.14 — Acquisition invariant** — `Continue Architecture Planning.md` L61838–61842
- **v0.14 — Discovery invariant** — `Continue Architecture Planning.md` L61844–61850
- **v0.15 — 31. The crucial invariant** — `Continue Architecture Planning.md` L63314–63350
- **v0.16 — 34. New invariants** — `Continue Architecture Planning.md` L64991–64991
- **v0.17 — 30. Core invariants** — `Continue Architecture Planning.md` L66450–66450
- **v0.18 — 18.23 Core Invariants** — `Continue Architecture Planning.md` L67966–67966
- **v0.18 — Invariant 1 — Type is not identity** — `Continue Architecture Planning.md` L67968–67974
- **v0.18 — Invariant 2 — URL does not determine semantic type** — `Continue Architecture Planning.md` L67976–67982
- **v0.18 — Invariant 3 — Technical recognition does not determine semantic role** — `Continue Architecture Planning.md` L67984–67990
- **v0.18 — Invariant 4 — Classification requires evidence** — `Continue Architecture Planning.md` L67992–67998
- **v0.18 — Invariant 5 — Classification does not imply authorization** — `Continue Architecture Planning.md` L68000–68006
- **v0.18 — Invariant 6 — Historical classification is immutable** — `Continue Architecture Planning.md` L68008–68018
- **v0.18 — Invariant 7 — Contradiction is preserved** — `Continue Architecture Planning.md` L68020–68028
- **v0.18 — Invariant 8 — Type axes remain independent** — `Continue Architecture Planning.md` L68030–68042
- **v0.19 — 19.25 New Invariants** — `Continue Architecture Planning.md` L69454–69454
- **v0.19 — Artifact invariant** — `Continue Architecture Planning.md` L69456–69464
- **v0.19 — Resource invariant** — `Continue Architecture Planning.md` L69466–69472
- **v0.19 — Representation invariant** — `Continue Architecture Planning.md` L69474–69488
- **v0.19 — Revision invariant** — `Continue Architecture Planning.md` L69490–69498
- **v0.19 — Observation invariant** — `Continue Architecture Planning.md` L69500–69507
- **v0.19 — Deduplication invariant** — `Continue Architecture Planning.md` L69509–69515
- **v0.19 — Change invariant** — `Continue Architecture Planning.md` L69517–69531
- **v0.19 — Classification invariant** — `Continue Architecture Planning.md` L69533–69542
- **v0.20 — 20.29 Core Invariants** — `Continue Architecture Planning.md` L70973–70973
- **v0.20 — Search-space invariant** — `Continue Architecture Planning.md` L70975–70981
- **v0.20 — Strategy invariant** — `Continue Architecture Planning.md` L70983–70989
- **v0.20 — Acquisition invariant** — `Continue Architecture Planning.md` L70991–70997
- **v0.20 — Partition invariant** — `Continue Architecture Planning.md` L70999–71005
- **v0.20 — Coverage invariant** — `Continue Architecture Planning.md` L71007–71013
- **v0.20 — Discovery invariant** — `Continue Architecture Planning.md` L71015–71026
- **v0.21 — 21.29 Invariants** — `Continue Architecture Planning.md` L72452–72452
- **v0.21 — Safety invariant** — `Continue Architecture Planning.md` L72454–72460
- **v0.21 — Capability invariant** — `Continue Architecture Planning.md` L72462–72468
- **v0.21 — Domain invariant** — `Continue Architecture Planning.md` L72470–72476
- **v0.21 — Exploration invariant** — `Continue Architecture Planning.md` L72478–72484
- **v0.21 — Historical invariant** — `Continue Architecture Planning.md` L72486–72492
- **v0.21 — Replay invariant** — `Continue Architecture Planning.md` L72494–72502
- **v0.21 — Provenance invariant** — `Continue Architecture Planning.md` L72504–72511
- **v0.22 — 22.24 Core invariants** — `Continue Architecture Planning.md` L73856–73856
- **v0.22 — Invariant 1** — `Continue Architecture Planning.md` L73858–73862
- **v0.22 — Invariant 2** — `Continue Architecture Planning.md` L73864–73868
- **v0.22 — Invariant 3** — `Continue Architecture Planning.md` L73870–73874
- **v0.22 — Invariant 4** — `Continue Architecture Planning.md` L73876–73880
- **v0.22 — Invariant 5** — `Continue Architecture Planning.md` L73882–73886
- **v0.22 — Invariant 6** — `Continue Architecture Planning.md` L73888–73892
- **v0.22 — Invariant 7** — `Continue Architecture Planning.md` L73894–73898
- **v0.22 — Invariant 8** — `Continue Architecture Planning.md` L73900–73904
- **v0.22 — Invariant 9** — `Continue Architecture Planning.md` L73906–73910
- **v0.22 — Invariant 10** — `Continue Architecture Planning.md` L73912–73935
- **v0.23 — 23.24 New invariants** — `Continue Architecture Planning.md` L75225–75225
- **v0.23 — Invariant 1** — `Continue Architecture Planning.md` L75227–75231
- **v0.23 — Invariant 2** — `Continue Architecture Planning.md` L75233–75237
- **v0.23 — Invariant 3** — `Continue Architecture Planning.md` L75239–75243
- **v0.23 — Invariant 4** — `Continue Architecture Planning.md` L75245–75249
- **v0.23 — Invariant 5** — `Continue Architecture Planning.md` L75251–75255
- **v0.23 — Invariant 6** — `Continue Architecture Planning.md` L75257–75261
- **v0.23 — Invariant 7** — `Continue Architecture Planning.md` L75263–75267
- **v0.23 — Invariant 8** — `Continue Architecture Planning.md` L75269–75273
- **v0.23 — Invariant 9** — `Continue Architecture Planning.md` L75275–75279
- **v0.23 — Invariant 10** — `Continue Architecture Planning.md` L75281–75287
- **v0.24 — 24.32 Core invariants for v0.24** — `Continue Architecture Planning.md` L76876–76876
- **v0.24 — Invariant 1** — `Continue Architecture Planning.md` L76878–76884
- **v0.24 — Invariant 2** — `Continue Architecture Planning.md` L76886–76892
- **v0.24 — Invariant 3** — `Continue Architecture Planning.md` L76894–76900
- **v0.24 — Invariant 4** — `Continue Architecture Planning.md` L76902–76908
- **v0.24 — Invariant 5** — `Continue Architecture Planning.md` L76910–76916
- **v0.24 — Invariant 6** — `Continue Architecture Planning.md` L76918–76924
- **v0.24 — Invariant 7** — `Continue Architecture Planning.md` L76926–76932
- **v0.24 — Invariant 8** — `Continue Architecture Planning.md` L76934–76947
- **v0.24 — Invariant 9** — `Continue Architecture Planning.md` L76949–76964
- **v0.24 — Invariant 10** — `Continue Architecture Planning.md` L76966–76975
- **v0.25 — 25.32 v0.25 invariants** — `Continue Architecture Planning.md` L78415–78415
- **v0.25 — Planner invariants** — `Continue Architecture Planning.md` L78417–78461
- **v0.26 — 26.26 The important safety invariant** — `Continue Architecture Planning.md` L79894–79940
- **v0.26 — 26.27 Resumability invariant** — `Continue Architecture Planning.md` L79942–79964
- **v0.26 — 26.29 v0.26 invariants** — `Continue Architecture Planning.md` L80015–80015
- **v0.26 — I1 — Planning/execution separation** — `Continue Architecture Planning.md` L80017–80021
- **v0.26 — I2 — Execution identity** — `Continue Architecture Planning.md` L80023–80027
- **v0.26 — I3 — Single scheduler authority** — `Continue Architecture Planning.md` L80029–80033
- **v0.26 — I4 — Bounded execution** — `Continue Architecture Planning.md` L80035–80037
- **v0.26 — I5 — Resumability** — `Continue Architecture Planning.md` L80039–80041
- **v0.26 — I6 — No silent cursor advancement** — `Continue Architecture Planning.md` L80043–80045
- **v0.26 — I7 — Proposal boundary** — `Continue Architecture Planning.md` L80047–80057
- **v0.26 — I8 — No authority escalation** — `Continue Architecture Planning.md` L80059–80065
- **v0.26 — I9 — Exhaustion separation** — `Continue Architecture Planning.md` L80067–80075
- **v0.26 — I10 — Failure ≠ absence** — `Continue Architecture Planning.md` L80077–80083
- **v0.26 — I11 — Provenance** — `Continue Architecture Planning.md` L80085–80100
- **v0.26 — I12 — Versioned recovery** — `Continue Architecture Planning.md` L80102–80106
- **v0.27 — 27.30 New invariants** — `Continue Architecture Planning.md` L81497–81497
- **v0.27 — E1 — Enumeration is scoped** — `Continue Architecture Planning.md` L81499–81501
- **v0.27 — E2 — Enumeration termination is not global completeness** — `Continue Architecture Planning.md` L81503–81509
- **v0.27 — E3 — Budget exhaustion is not enumeration exhaustion** — `Continue Architecture Planning.md` L81511–81517
- **v0.27 — E4 — Cursor progress must be durable** — `Continue Architecture Planning.md` L81519–81525
- **v0.27 — E5 — Enumeration entries are not candidates** — `Continue Architecture Planning.md` L81527–81531
- **v0.27 — E6 — Cardinality is evidence** — `Continue Architecture Planning.md` L81533–81537
- **v0.27 — E7 — Historical snapshots remain immutable** — `Continue Architecture Planning.md` L81539–81541
- **v0.27 — E8 — Incomplete enumeration cannot establish absence** — `Continue Architecture Planning.md` L81543–81549
- **v0.27 — E9 — Unstable enumeration weakens completeness** — `Continue Architecture Planning.md` L81551–81553
- **v0.27 — E10 — Enumerator has no acquisition authority** — `Continue Architecture Planning.md` L81555–81557
- **v0.27 — E11 — Enumerator cannot directly mutate the ResourceGraph** — `Continue Architecture Planning.md` L81559–81561
- **v0.27 — E12 — Termination evidence is provenance-bearing** — `Continue Architecture Planning.md` L81563–81567
- **v0.28 — 28.32 Core invariants** — `Continue Architecture Planning.md` L82991–82991
- **v0.28 — R1 — Candidate convergence** — `Continue Architecture Planning.md` L82993–82995
- **v0.28 — R2 — Provenance preservation** — `Continue Architecture Planning.md` L82997–82999
- **v0.28 — R3 — Artifact convergence** — `Continue Architecture Planning.md` L83001–83003
- **v0.28 — R4 — Observation preservation** — `Continue Architecture Planning.md` L83005–83007
- **v0.28 — R5 — Overlap is not duplication** — `Continue Architecture Planning.md` L83009–83019
- **v0.28 — R6 — Equivalent work may be suppressed** — `Continue Architecture Planning.md` L83021–83023
- **v0.28 — R7 — Suppression preserves provenance** — `Continue Architecture Planning.md` L83025–83027
- **v0.28 — R8 — Unknown overlap is not disjointness** — `Continue Architecture Planning.md` L83029–83035
- **v0.28 — R9 — Coverage is union-aware** — `Continue Architecture Planning.md` L83037–83039
- **v0.28 — R10 — Candidate count does not establish coverage** — `Continue Architecture Planning.md` L83041–83047
- **v0.28 — R11 — Evidence independence must be justified** — `Continue Architecture Planning.md` L83049–83051
- **v0.28 — R12 — Historical reconciliation is immutable** — `Continue Architecture Planning.md` L83053–83057
- **v0.29 — 29.33 v0.29 invariants** — `Continue Architecture Planning.md` L84465–84465
- **v0.29 — P1 — Discovery does not create authority** — `Continue Architecture Planning.md` L84467–84475
- **v0.29 — P2 — Partition proposal is not partition** — `Continue Architecture Planning.md` L84477–84481
- **v0.29 — P3 — Every admitted partition belongs to the domain** — `Continue Architecture Planning.md` L84483–84487
- **v0.29 — P4 — Expansion is budgeted** — `Continue Architecture Planning.md` L84489–84491
- **v0.29 — P5 — Expansion is depth-bounded** — `Continue Architecture Planning.md` L84493–84495
- **v0.29 — P6 — Duplicate partitions converge** — `Continue Architecture Planning.md` L84497–84499
- **v0.29 — P7 — Overlap is preserved** — `Continue Architecture Planning.md` L84501–84503
- **v0.29 — P8 — Evidence is preserved** — `Continue Architecture Planning.md` L84505–84507
- **v0.29 — P9 — Partition existence does not schedule execution** — `Continue Architecture Planning.md` L84509–84515
- **v0.29 — P10 — Expansion cannot override policy** — `Continue Architecture Planning.md` L84517–84519
- **v0.29 — P11 — Search-space versions are immutable** — `Continue Architecture Planning.md` L84521–84523
- **v0.29 — P12 — Expansion does not invalidate historical claims automatically** — `Continue Architecture Planning.md` L84525–84527
- **v0.29 — P13 — Cycles are legal** — `Continue Architecture Planning.md` L84529–84531
- **v0.29 — P14 — Unknown remains valid** — `Continue Architecture Planning.md` L84533–84543
- **v0.30 — The fundamental invariant** — `Continue Architecture Planning.md` L84793–84843
- **v0.30 — 30.22 The deeper invariant** — `Continue Architecture Planning.md` L86174–86218
- **v0.30 — 30.25 v0.30 invariants** — `Continue Architecture Planning.md` L86307–86356
- **v0.31 — 31.24 The central v0.31 invariants** — `Continue Architecture Planning.md` L87600–87646
- **v0.32 — 32.18 Accounting invariant under crash** — `Continue Architecture Planning.md` L88454–88470
- **v0.32 — 32.22 Recovery invariant for cursors** — `Continue Architecture Planning.md` L88568–88589
- **v0.32 — 32.34 v0.32 invariants** — `Continue Architecture Planning.md` L88961–89008
- **v0.33 — 33.11 Fencing invariant** — `Continue Architecture Planning.md` L89527–89554
- **v0.33 — 33.33 The complete ownership invariant** — `Continue Architecture Planning.md` L90227–90248
- **v0.33 — 33.34 The deeper distributed invariant** — `Continue Architecture Planning.md` L90250–90274
- **v0.34 — 34.26 New Core Invariants** — `Continue Architecture Planning.md` L91668–91668
- **v0.34 — The major architectural invariants** — `Continue Architecture Planning.md` L92125–92156

## Related Documents

- [Verification](verification.md)
- [Failure Taxonomy](failure-taxonomy.md)
- [README.md](../README.md)
- [System Model](../architecture/system-model.md)

---

<!-- source: Continue Architecture Planning.md L55493–55532 | turn 29 | version 0.8 -->
## v0.8 — 15. Updated system invariant

The strongest invariant introduced by v0.8 is:

```
NO ACQUISITION WITHOUT:

    1. candidate identity
    2. acquisition requirements
    3. capability resolution
    4. policy decision
    5. acquisition plan
    6. scheduler authorization
```

Formally:

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

Conversely:

```
Discovered(x)
    ⇏
    Acquire(x)
```

That implication is intentionally one-way.

---

<!-- source: Continue Architecture Planning.md L56193–56195 | turn 31 | version 0.9 -->
## v0.9 — 10. v0.9 invariants

The important contracts should now be explicit.

<!-- source: Continue Architecture Planning.md L56197–56201 | turn 31 | version 0.9 -->
### v0.9 — I1 — Discovery independence

```
Discovery does not imply acquisition.
```

<!-- source: Continue Architecture Planning.md L56203–56207 | turn 31 | version 0.9 -->
### v0.9 — I2 — Policy independence

```
Provider availability does not imply authorization.
```

<!-- source: Continue Architecture Planning.md L56209–56215 | turn 31 | version 0.9 -->
### v0.9 — I3 — Capability soundness

```
Provider.execute(plan)
    ⇒
provider.canExecute(plan)
```

<!-- source: Continue Architecture Planning.md L56217–56223 | turn 31 | version 0.9 -->
### v0.9 — I4 — Method safety

```
GET-only runtime
    ⇒
no acquisition provider may execute POST/PUT/PATCH/DELETE.
```

<!-- source: Continue Architecture Planning.md L56225–56231 | turn 31 | version 0.9 -->
### v0.9 — I5 — Provenance

```
Every executed acquisition
    ⇒
provider identity is recorded.
```

<!-- source: Continue Architecture Planning.md L56233–56241 | turn 31 | version 0.9 -->
### v0.9 — I6 — Observation integrity

```
Provider failure
    ≠
Policy denial
    ≠
Recognition failure
```

<!-- source: Continue Architecture Planning.md L56243–56253 | turn 31 | version 0.9 -->
### v0.9 — I7 — Replay distinction

```
Decision replay
    may be deterministic.

Network replay
    requires an explicit replay provider.
```

---

<!-- source: Continue Architecture Planning.md L59208–59208 | turn 37 | version 0.12 -->
## v0.12 — 18. v0.12 invariants



<!-- source: Continue Architecture Planning.md L59210–59215 | turn 37 | version 0.12 -->
### v0.12 — S1 — Source purity

```
CandidateSource
    MUST NOT perform acquisition.
```

<!-- source: Continue Architecture Planning.md L59217–59222 | turn 37 | version 0.12 -->
### v0.12 — S2 — Core ownership

```
CandidateSource
    MUST NOT directly mutate the scheduler or KB.
```

<!-- source: Continue Architecture Planning.md L59224–59228 | turn 37 | version 0.12 -->
### v0.12 — S3 — Proposal semantics

```
Proposal ≠ Candidate
```

<!-- source: Continue Architecture Planning.md L59230–59235 | turn 37 | version 0.12 -->
### v0.12 — S4 — Identity

```
Candidate identity
    is independent of discovery source.
```

<!-- source: Continue Architecture Planning.md L59237–59242 | turn 37 | version 0.12 -->
### v0.12 — S5 — Provenance

```
Every candidate
    SHOULD retain its originating source/evidence.
```

<!-- source: Continue Architecture Planning.md L59244–59249 | turn 37 | version 0.12 -->
### v0.12 — S6 — Representability

```
A discovered target may be represented
even when it cannot currently be acquired.
```

<!-- source: Continue Architecture Planning.md L59251–59265 | turn 37 | version 0.12 -->
### v0.12 — S7 — Observation independence

```
Observation
    ≠
Recognition
    ≠
Evidence
    ≠
Candidate
```

This gives the system much cleaner semantics.

---

<!-- source: Continue Architecture Planning.md L60327–60327 | turn 39 | version 0.13 -->
## v0.13 — 20. v0.13 invariants



<!-- source: Continue Architecture Planning.md L60329–60334 | turn 39 | version 0.13 -->
### v0.13 — D1 — Source isolation

```
CandidateSource
    MUST NOT control scheduling.
```

<!-- source: Continue Architecture Planning.md L60336–60341 | turn 39 | version 0.13 -->
### v0.13 — D2 — Acquisition isolation

```
CandidateSource
    MUST NOT acquire resources.
```

<!-- source: Continue Architecture Planning.md L60343–60348 | turn 39 | version 0.13 -->
### v0.13 — D3 — Normalization ownership

```
Core
    owns candidate identity.
```

<!-- source: Continue Architecture Planning.md L60350–60355 | turn 39 | version 0.13 -->
### v0.13 — D4 — Bounded generation

```
Every source execution
    is subject to a proposal budget.
```

<!-- source: Continue Architecture Planning.md L60357–60362 | turn 39 | version 0.13 -->
### v0.13 — D5 — Bounded recursion

```
Every discovery path
    is subject to a depth/budget policy.
```

<!-- source: Continue Architecture Planning.md L60364–60369 | turn 39 | version 0.13 -->
### v0.13 — D6 — Provenance preservation

```
Candidate merge
    MUST NOT erase discovery provenance.
```

<!-- source: Continue Architecture Planning.md L60371–60376 | turn 39 | version 0.13 -->
### v0.13 — D7 — Atomic task claiming

```
A DiscoveryTask
    MUST NOT be concurrently claimed twice.
```

<!-- source: Continue Architecture Planning.md L60378–60383 | turn 39 | version 0.13 -->
### v0.13 — D8 — Convergence

```
Multiple discovery paths
    MAY converge on one candidate.
```

<!-- source: Continue Architecture Planning.md L60385–60392 | turn 39 | version 0.13 -->
### v0.13 — D9 — Discovery/acquisition independence

```
Candidate creation
    does not imply acquisition.
```

---

<!-- source: Continue Architecture Planning.md L61789–61789 | turn 41 | version 0.14 -->
## v0.14 — 24. Strong invariants



<!-- source: Continue Architecture Planning.md L61791–61797 | turn 41 | version 0.14 -->
### v0.14 — Domain invariant

```
Candidate ∈ Domain
```

must be evaluated explicitly.

<!-- source: Continue Architecture Planning.md L61799–61803 | turn 41 | version 0.14 -->
### v0.14 — Session invariant

```
Every active operation belongs to exactly one ScanSession.
```

<!-- source: Continue Architecture Planning.md L61805–61809 | turn 41 | version 0.14 -->
### v0.14 — Snapshot invariant

```
A running session uses an immutable domain snapshot.
```

<!-- source: Continue Architecture Planning.md L61811–61816 | turn 41 | version 0.14 -->
### v0.14 — Frontier invariant

```
Frontier state represents unfinished work,
not the complete knowledge graph.
```

<!-- source: Continue Architecture Planning.md L61818–61822 | turn 41 | version 0.14 -->
### v0.14 — Termination invariant

```
Session completion requires an explicit termination reason.
```

<!-- source: Continue Architecture Planning.md L61824–61829 | turn 41 | version 0.14 -->
### v0.14 — Recovery invariant

```
An expired claim cannot remain permanently owned by
a dead session.
```

<!-- source: Continue Architecture Planning.md L61831–61836 | turn 41 | version 0.14 -->
### v0.14 — Provenance invariant

```
Candidate identity survives across sessions;
discovery provenance remains session-specific.
```

<!-- source: Continue Architecture Planning.md L61838–61842 | turn 41 | version 0.14 -->
### v0.14 — Acquisition invariant

```
Candidate creation does not imply acquisition.
```

<!-- source: Continue Architecture Planning.md L61844–61850 | turn 41 | version 0.14 -->
### v0.14 — Discovery invariant

```
Discovery is bounded by the domain and session budgets.
```

---

<!-- source: Continue Architecture Planning.md L63314–63350 | turn 43 | version 0.15 -->
## v0.15 — 31. The crucial invariant

The strongest v0.15 invariant is:

```
Work execution
    ⇒
    work was eligible
    ∧
    work was claimed
    ∧
    claim was valid
    ∧
    session was active
    ∧
    domain was valid
    ∧
    executor was authorized
```

And:

```
Work execution ⇏ Work success
```

Execution can fail.

Likewise:

```
Candidate creation ⇏ Work creation
```

A discovered candidate might be rejected by domain or acquisition policy.

---

<!-- source: Continue Architecture Planning.md L64991–64991 | turn 45 | version 0.16 -->
## v0.16 — 34. New invariants



<!-- source: Continue Architecture Planning.md L66450–66450 | turn 47 | version 0.17 -->
## v0.17 — 30. Core invariants



<!-- source: Continue Architecture Planning.md L67966–67966 | turn 49 | version 0.18 -->
## v0.18 — 18.23 Core Invariants



<!-- source: Continue Architecture Planning.md L67968–67974 | turn 49 | version 0.18 -->
### v0.18 — Invariant 1 — Type is not identity

```
ResourceIdentity(x)
    ⇏
ResourceType(x)
```

<!-- source: Continue Architecture Planning.md L67976–67982 | turn 49 | version 0.18 -->
### v0.18 — Invariant 2 — URL does not determine semantic type

```
URL(x)
    ⇏
SemanticType(x)
```

<!-- source: Continue Architecture Planning.md L67984–67990 | turn 49 | version 0.18 -->
### v0.18 — Invariant 3 — Technical recognition does not determine semantic role

```
RecognizedAsPDF(x)
    ⇏
ServiceManual(x)
```

<!-- source: Continue Architecture Planning.md L67992–67998 | turn 49 | version 0.18 -->
### v0.18 — Invariant 4 — Classification requires evidence

```
Classification(x, T)
    ⇒
∃ Evidence supporting (x, T)
```

<!-- source: Continue Architecture Planning.md L68000–68006 | turn 49 | version 0.18 -->
### v0.18 — Invariant 5 — Classification does not imply authorization

```
Classified(x, T)
    ⇏
Acquire(x)
```

<!-- source: Continue Architecture Planning.md L68008–68018 | turn 49 | version 0.18 -->
### v0.18 — Invariant 6 — Historical classification is immutable

```
Classification_v1
```

must remain distinguishable from:

```
Classification_v2
```

<!-- source: Continue Architecture Planning.md L68020–68028 | turn 49 | version 0.18 -->
### v0.18 — Invariant 7 — Contradiction is preserved

```
Evidence(A)
+
Evidence(not-A)
```

must not silently collapse into either one.

<!-- source: Continue Architecture Planning.md L68030–68042 | turn 49 | version 0.18 -->
### v0.18 — Invariant 8 — Type axes remain independent

```
representation(x)
```

must not overwrite:

```
semantic_role(x)
```

---

<!-- source: Continue Architecture Planning.md L69454–69454 | turn 51 | version 0.19 -->
## v0.19 — 19.25 New Invariants



<!-- source: Continue Architecture Planning.md L69456–69464 | turn 51 | version 0.19 -->
### v0.19 — Artifact invariant

```
Artifact identity
    =
cryptographic digest identity
```

subject to the chosen algorithm's assumptions.

<!-- source: Continue Architecture Planning.md L69466–69472 | turn 51 | version 0.19 -->
### v0.19 — Resource invariant

```
Resource identity
    ≠
Artifact identity
```

<!-- source: Continue Architecture Planning.md L69474–69488 | turn 51 | version 0.19 -->
### v0.19 — Representation invariant

```
Representation
    belongs to
Resource
```

but:

```
Representation
    ≠
Resource
```

<!-- source: Continue Architecture Planning.md L69490–69498 | turn 51 | version 0.19 -->
### v0.19 — Revision invariant

```
Revision
    references
Artifact
```

rather than replacing it.

<!-- source: Continue Architecture Planning.md L69500–69507 | turn 51 | version 0.19 -->
### v0.19 — Observation invariant

```
Observation
    records what happened
```

It does not retroactively redefine history.

<!-- source: Continue Architecture Planning.md L69509–69515 | turn 51 | version 0.19 -->
### v0.19 — Deduplication invariant

```
same artifact
    ⇏
same resource
```

<!-- source: Continue Architecture Planning.md L69517–69531 | turn 51 | version 0.19 -->
### v0.19 — Change invariant

```
different artifact
    ⇒
different bytes
```

but:

```
different artifact
    ⇏
different semantic resource
```

<!-- source: Continue Architecture Planning.md L69533–69542 | turn 51 | version 0.19 -->
### v0.19 — Classification invariant

```
classification
    requires evidence
```

and remains independent of artifact identity.

---

<!-- source: Continue Architecture Planning.md L70973–70973 | turn 53 | version 0.20 -->
## v0.20 — 20.29 Core Invariants



<!-- source: Continue Architecture Planning.md L70975–70981 | turn 53 | version 0.20 -->
### v0.20 — Search-space invariant

```
Every admitted partition
    ⊆
DiscoveryDomain
```

<!-- source: Continue Architecture Planning.md L70983–70989 | turn 53 | version 0.20 -->
### v0.20 — Strategy invariant

```
Strategy
    cannot bypass
    FrontierRuntime
```

<!-- source: Continue Architecture Planning.md L70991–70997 | turn 53 | version 0.20 -->
### v0.20 — Acquisition invariant

```
Strategy
    cannot bypass
    AcquisitionPolicy
```

<!-- source: Continue Architecture Planning.md L70999–71005 | turn 53 | version 0.20 -->
### v0.20 — Partition invariant

```
Partition
    ≠
Candidate
```

<!-- source: Continue Architecture Planning.md L71007–71013 | turn 53 | version 0.20 -->
### v0.20 — Coverage invariant

```
Exhausted(partition)
    ≠
Complete(domain)
```

<!-- source: Continue Architecture Planning.md L71015–71026 | turn 53 | version 0.20 -->
### v0.20 — Discovery invariant

```
No candidate
    may be created
    merely because
    a partition exists.
```

A partition represents search potential, not evidence that a resource exists.

---

<!-- source: Continue Architecture Planning.md L72452–72452 | turn 55 | version 0.21 -->
## v0.21 — 21.29 Invariants



<!-- source: Continue Architecture Planning.md L72454–72460 | turn 55 | version 0.21 -->
### v0.21 — Safety invariant

```
AdaptiveScore(x)
    cannot override
Policy(x)
```

<!-- source: Continue Architecture Planning.md L72462–72468 | turn 55 | version 0.21 -->
### v0.21 — Capability invariant

```
HighStrategyScore
    ⇏
CapabilityAvailable
```

<!-- source: Continue Architecture Planning.md L72470–72476 | turn 55 | version 0.21 -->
### v0.21 — Domain invariant

```
StrategySelected(P)
    ⇒
P ∈ DiscoveryDomain
```

<!-- source: Continue Architecture Planning.md L72478–72484 | turn 55 | version 0.21 -->
### v0.21 — Exploration invariant

```
UnknownStrategy
    ≠
BadStrategy
```

<!-- source: Continue Architecture Planning.md L72486–72492 | turn 55 | version 0.21 -->
### v0.21 — Historical invariant

```
HistoricalPerformance
    is evidence,
    not authority.
```

<!-- source: Continue Architecture Planning.md L72494–72502 | turn 55 | version 0.21 -->
### v0.21 — Replay invariant

```
Same decision inputs
    ⇒
same strategy selection
```

assuming deterministic strategy selection.

<!-- source: Continue Architecture Planning.md L72504–72511 | turn 55 | version 0.21 -->
### v0.21 — Provenance invariant

```
Every adaptive decision
    has an explainable reason.
```

---

<!-- source: Continue Architecture Planning.md L73856–73856 | turn 57 | version 0.22 -->
## v0.22 — 22.24 Core invariants



<!-- source: Continue Architecture Planning.md L73858–73862 | turn 57 | version 0.22 -->
### v0.22 — Invariant 1

```
EXHAUSTED ≠ COMPLETE
```

<!-- source: Continue Architecture Planning.md L73864–73868 | turn 57 | version 0.22 -->
### v0.22 — Invariant 2

```
COVERAGE MUST HAVE A DEFINED SCOPE
```

<!-- source: Continue Architecture Planning.md L73870–73874 | turn 57 | version 0.22 -->
### v0.22 — Invariant 3

```
UNKNOWN DENOMINATOR ≠ 100%
```

<!-- source: Continue Architecture Planning.md L73876–73880 | turn 57 | version 0.22 -->
### v0.22 — Invariant 4

```
NOT FOUND ≠ DOES NOT EXIST
```

<!-- source: Continue Architecture Planning.md L73882–73886 | turn 57 | version 0.22 -->
### v0.22 — Invariant 5

```
INACCESSIBLE ≠ ABSENT
```

<!-- source: Continue Architecture Planning.md L73888–73892 | turn 57 | version 0.22 -->
### v0.22 — Invariant 6

```
UNSUPPORTED ≠ ABSENT
```

<!-- source: Continue Architecture Planning.md L73894–73898 | turn 57 | version 0.22 -->
### v0.22 — Invariant 7

```
COMPLETENESS CLAIMS REQUIRE EVIDENCE
```

<!-- source: Continue Architecture Planning.md L73900–73904 | turn 57 | version 0.22 -->
### v0.22 — Invariant 8

```
SEARCH-SPACE CHANGES MUST NOT ERASE HISTORICAL COVERAGE
```

<!-- source: Continue Architecture Planning.md L73906–73910 | turn 57 | version 0.22 -->
### v0.22 — Invariant 9

```
COVERAGE IS RELATIVE TO A METHOD AND SNAPSHOT
```

<!-- source: Continue Architecture Planning.md L73912–73935 | turn 57 | version 0.22 -->
### v0.22 — Invariant 10

```
NO ADAPTIVE STRATEGY MAY UPGRADE COMPLETENESS
WITHOUT NEW EVIDENCE
```

That last invariant is especially important.

An adaptive controller may decide:

```
"This strategy is probably sufficient."
```

It may **not** convert that belief into:

```
"Search is complete."
```

without the required assurance evidence.

---

<!-- source: Continue Architecture Planning.md L75225–75225 | turn 59 | version 0.23 -->
## v0.23 — 23.24 New invariants



<!-- source: Continue Architecture Planning.md L75227–75231 | turn 59 | version 0.23 -->
### v0.23 — Invariant 1

```
NOT_FOUND ≠ ABSENT
```

<!-- source: Continue Architecture Planning.md L75233–75237 | turn 59 | version 0.23 -->
### v0.23 — Invariant 2

```
ABSENT(S) ⇒ S IS EXPLICITLY DEFINED
```

<!-- source: Continue Architecture Planning.md L75239–75243 | turn 59 | version 0.23 -->
### v0.23 — Invariant 3

```
ABSENT(x, S) ⇏ ABSENT(x, Universe)
```

<!-- source: Continue Architecture Planning.md L75245–75249 | turn 59 | version 0.23 -->
### v0.23 — Invariant 4

```
INACCESSIBLE ⇒ ABSENCE UNPROVEN
```

<!-- source: Continue Architecture Planning.md L75251–75255 | turn 59 | version 0.23 -->
### v0.23 — Invariant 5

```
INCOMPLETE ENUMERATION ⇒ ABSENCE UNPROVEN
```

<!-- source: Continue Architecture Planning.md L75257–75261 | turn 59 | version 0.23 -->
### v0.23 — Invariant 6

```
FAILURE TO OBSERVE ≠ NEGATIVE EVIDENCE
```

<!-- source: Continue Architecture Planning.md L75263–75267 | turn 59 | version 0.23 -->
### v0.23 — Invariant 7

```
NEGATIVE EVIDENCE MUST RETAIN SCOPE
```

<!-- source: Continue Architecture Planning.md L75269–75273 | turn 59 | version 0.23 -->
### v0.23 — Invariant 8

```
CLAIMS MUST NOT DESTROY CONFLICTING CLAIMS
```

<!-- source: Continue Architecture Planning.md L75275–75279 | turn 59 | version 0.23 -->
### v0.23 — Invariant 9

```
SAME METHOD REPEATED ≠ INDEPENDENT EVIDENCE
```

<!-- source: Continue Architecture Planning.md L75281–75287 | turn 59 | version 0.23 -->
### v0.23 — Invariant 10

```
TEMPORAL CHANGE ≠ LOGICAL CONTRADICTION
```

---

<!-- source: Continue Architecture Planning.md L76876–76876 | turn 61 | version 0.24 -->
## v0.24 — 24.32 Core invariants for v0.24



<!-- source: Continue Architecture Planning.md L76878–76884 | turn 61 | version 0.24 -->
### v0.24 — Invariant 1

```
GOAL ⊆ DOMAIN
```

A goal cannot expand the authorized search universe.

<!-- source: Continue Architecture Planning.md L76886–76892 | turn 61 | version 0.24 -->
### v0.24 — Invariant 2

```
RELEVANCE ≠ CLASSIFICATION
```

Classification provides evidence for relevance; it does not equal relevance.

<!-- source: Continue Architecture Planning.md L76894–76900 | turn 61 | version 0.24 -->
### v0.24 — Invariant 3

```
RELEVANCE ≠ AUTHORIZATION
```

A highly relevant resource can still be inaccessible or unauthorized to acquire.

<!-- source: Continue Architecture Planning.md L76902–76908 | turn 61 | version 0.24 -->
### v0.24 — Invariant 4

```
SATISFIED ≠ COMPLETE
```

A goal can be satisfied without exhaustive search.

<!-- source: Continue Architecture Planning.md L76910–76916 | turn 61 | version 0.24 -->
### v0.24 — Invariant 5

```
RANK ≠ RELEVANCE
```

Ranking may incorporate additional quality dimensions.

<!-- source: Continue Architecture Planning.md L76918–76924 | turn 61 | version 0.24 -->
### v0.24 — Invariant 6

```
PREFERENCE ≠ CONSTRAINT
```

A preference cannot accidentally become an exclusion rule.

<!-- source: Continue Architecture Planning.md L76926–76932 | turn 61 | version 0.24 -->
### v0.24 — Invariant 7

```
HISTORICAL KNOWLEDGE ≠ CURRENT OBSERVATION
```

Knowledge reuse must preserve temporal provenance.

<!-- source: Continue Architecture Planning.md L76934–76947 | turn 61 | version 0.24 -->
### v0.24 — Invariant 8

```
GOAL OPTIMIZATION CANNOT OVERRIDE SAFETY
```

No relevance score can bypass:

```
policy
capability
budget
domain
```

<!-- source: Continue Architecture Planning.md L76949–76964 | turn 61 | version 0.24 -->
### v0.24 — Invariant 9

```
GOAL RESULT MUST BE EXPLAINABLE
```

A result should be traceable through:

```
Goal
 → Constraint
 → Discovery decision
 → Evidence
 → Resource
 → Relevance assertion
```

<!-- source: Continue Architecture Planning.md L76966–76975 | turn 61 | version 0.24 -->
### v0.24 — Invariant 10

```
COMPLETENESS IS ABOUT SEARCH SPACE,
NOT RESULT COUNT
```

Finding 10,000 results does not imply completeness.

---

<!-- source: Continue Architecture Planning.md L78415–78415 | turn 63 | version 0.25 -->
## v0.25 — 25.32 v0.25 invariants



<!-- source: Continue Architecture Planning.md L78417–78461 | turn 63 | version 0.25 -->
### v0.25 — Planner invariants

```
1. Planner proposes; it does not execute.
```

```
2. QueryPlan ⊄ authority.
```

A plan cannot grant capabilities.

```
3. Goal ⊆ Domain.
```

```
4. Planner hypotheses ≠ discovered candidates.
```

```
5. Historical plans are immutable.
```

```
6. Every generated step has provenance.
```

```
7. Planning is budgeted.
```

```
8. Conditional planning cannot bypass admission controls.
```

```
9. Query expansion must identify its provider/evidence.
```

```
10. Plan optimization cannot upgrade evidence strength.
```

---

<!-- source: Continue Architecture Planning.md L79894–79940 | turn 65 | version 0.26 -->
## v0.26 — 26.26 The important safety invariant

A tactic must never be able to turn:

```
"the planner requested this"
```

into:

```
"the system is authorized to do this"
```

Formally:

```
Planned(step)
    ⇏
Authorized(step)
```

and:

```
TacticExecution(step)
    ⇏
Acquisition
```

The actual chain remains:

```
Planned
 ↓
Admitted
 ↓
CapabilitySatisfied
 ↓
PolicyAllowed
 ↓
Scheduled
 ↓
Executed
```

---

<!-- source: Continue Architecture Planning.md L79942–79964 | turn 65 | version 0.26 -->
## v0.26 — 26.27 Resumability invariant

A successfully checkpointed execution should satisfy:

```
CheckpointValid(E)
    ⇒
    Resume(E)
    can continue without
    silently skipping the unprocessed search region
```

The system may repeat work.

It must not silently lose work.

This gives a stronger principle:

> **At-least-once discovery is preferable to at-most-once discovery when the cost of duplicate work is lower than the cost of silent coverage loss.**

Deduplication and provenance then absorb repeated proposals.

---

<!-- source: Continue Architecture Planning.md L80015–80015 | turn 65 | version 0.26 -->
## v0.26 — 26.29 v0.26 invariants



<!-- source: Continue Architecture Planning.md L80017–80021 | turn 65 | version 0.26 -->
### v0.26 — I1 — Planning/execution separation

```
QueryPlan ≠ TacticExecution
```

<!-- source: Continue Architecture Planning.md L80023–80027 | turn 65 | version 0.26 -->
### v0.26 — I2 — Execution identity

```
TacticExecution ≠ TacticAttempt
```

<!-- source: Continue Architecture Planning.md L80029–80033 | turn 65 | version 0.26 -->
### v0.26 — I3 — Single scheduler authority

```
FrontierRuntime owns work admission/claiming.
```

<!-- source: Continue Architecture Planning.md L80035–80037 | turn 65 | version 0.26 -->
### v0.26 — I4 — Bounded execution

Every tactic execution has finite runtime/budget boundaries.

<!-- source: Continue Architecture Planning.md L80039–80041 | turn 65 | version 0.26 -->
### v0.26 — I5 — Resumability

Checkpointed progress can be resumed or explicitly abandoned.

<!-- source: Continue Architecture Planning.md L80043–80045 | turn 65 | version 0.26 -->
### v0.26 — I6 — No silent cursor advancement

A cursor must not advance past unpersisted discoveries.

<!-- source: Continue Architecture Planning.md L80047–80057 | turn 65 | version 0.26 -->
### v0.26 — I7 — Proposal boundary

```
Tactic → Proposal
```

not:

```
Tactic → Candidate mutation
```

<!-- source: Continue Architecture Planning.md L80059–80065 | turn 65 | version 0.26 -->
### v0.26 — I8 — No authority escalation

```
QueryPlan ⇏ Authorization
Tactic ⇏ Authorization
Strategy ⇏ Authorization
```

<!-- source: Continue Architecture Planning.md L80067–80075 | turn 65 | version 0.26 -->
### v0.26 — I9 — Exhaustion separation

```
TacticExhausted
⇏
PartitionExhausted
⇏
SearchComplete
```

<!-- source: Continue Architecture Planning.md L80077–80083 | turn 65 | version 0.26 -->
### v0.26 — I10 — Failure ≠ absence

```
TacticFailure
⇏
ResourceAbsent
```

<!-- source: Continue Architecture Planning.md L80085–80100 | turn 65 | version 0.26 -->
### v0.26 — I11 — Provenance

Every tactic-generated proposal must retain:

```
goal
plan
step
execution
tactic
strategy
partition
evidence
```

where applicable.

<!-- source: Continue Architecture Planning.md L80102–80106 | turn 65 | version 0.26 -->
### v0.26 — I12 — Versioned recovery

A checkpoint created under incompatible tactic/plan semantics must not be silently resumed.

---

<!-- source: Continue Architecture Planning.md L81497–81497 | turn 67 | version 0.27 -->
## v0.27 — 27.30 New invariants



<!-- source: Continue Architecture Planning.md L81499–81501 | turn 67 | version 0.27 -->
### v0.27 — E1 — Enumeration is scoped

Every enumeration has an explicit target/scope.

<!-- source: Continue Architecture Planning.md L81503–81509 | turn 67 | version 0.27 -->
### v0.27 — E2 — Enumeration termination is not global completeness

```
EnumeratorExhausted
⇏
UniverseComplete
```

<!-- source: Continue Architecture Planning.md L81511–81517 | turn 67 | version 0.27 -->
### v0.27 — E3 — Budget exhaustion is not enumeration exhaustion

```
BudgetExhausted
⇏
Exhausted
```

<!-- source: Continue Architecture Planning.md L81519–81525 | turn 67 | version 0.27 -->
### v0.27 — E4 — Cursor progress must be durable

```
cursorAfter
```

must not become authoritative before corresponding discoveries are durable.

<!-- source: Continue Architecture Planning.md L81527–81531 | turn 67 | version 0.27 -->
### v0.27 — E5 — Enumeration entries are not candidates

```
Entry ≠ Candidate
```

<!-- source: Continue Architecture Planning.md L81533–81537 | turn 67 | version 0.27 -->
### v0.27 — E6 — Cardinality is evidence

```
reportedTotal ≠ provenTotal
```

<!-- source: Continue Architecture Planning.md L81539–81541 | turn 67 | version 0.27 -->
### v0.27 — E7 — Historical snapshots remain immutable

A later enumeration does not rewrite an earlier snapshot.

<!-- source: Continue Architecture Planning.md L81543–81549 | turn 67 | version 0.27 -->
### v0.27 — E8 — Incomplete enumeration cannot establish absence

```
Incomplete(S)
⇏
Absent(x,S)
```

<!-- source: Continue Architecture Planning.md L81551–81553 | turn 67 | version 0.27 -->
### v0.27 — E9 — Unstable enumeration weakens completeness

Changing enumeration state must be reflected in coverage assurance.

<!-- source: Continue Architecture Planning.md L81555–81557 | turn 67 | version 0.27 -->
### v0.27 — E10 — Enumerator has no acquisition authority

It can request probes through the existing acquisition machinery but cannot bypass policy.

<!-- source: Continue Architecture Planning.md L81559–81561 | turn 67 | version 0.27 -->
### v0.27 — E11 — Enumerator cannot directly mutate the ResourceGraph

All discoveries pass through the normal proposal/normalization path.

<!-- source: Continue Architecture Planning.md L81563–81567 | turn 67 | version 0.27 -->
### v0.27 — E12 — Termination evidence is provenance-bearing

A completeness-relevant termination event must identify the enumerator, version, target, execution, and supporting observation.

---

<!-- source: Continue Architecture Planning.md L82991–82991 | turn 69 | version 0.28 -->
## v0.28 — 28.32 Core invariants



<!-- source: Continue Architecture Planning.md L82993–82995 | turn 69 | version 0.28 -->
### v0.28 — R1 — Candidate convergence

Equivalent candidate identities converge to one candidate.

<!-- source: Continue Architecture Planning.md L82997–82999 | turn 69 | version 0.28 -->
### v0.28 — R2 — Provenance preservation

Candidate convergence never destroys discovery provenance.

<!-- source: Continue Architecture Planning.md L83001–83003 | turn 69 | version 0.28 -->
### v0.28 — R3 — Artifact convergence

Identical artifact hashes may converge at artifact identity without merging logical resources.

<!-- source: Continue Architecture Planning.md L83005–83007 | turn 69 | version 0.28 -->
### v0.28 — R4 — Observation preservation

Different observations remain distinct unless an explicit observation-equivalence rule exists.

<!-- source: Continue Architecture Planning.md L83009–83019 | turn 69 | version 0.28 -->
### v0.28 — R5 — Overlap is not duplication

```
Partition A overlaps B
```

does not mean:

```
B should be discarded
```

<!-- source: Continue Architecture Planning.md L83021–83023 | turn 69 | version 0.28 -->
### v0.28 — R6 — Equivalent work may be suppressed

If semantic equivalence is established, duplicate unfinished work may be suppressed.

<!-- source: Continue Architecture Planning.md L83025–83027 | turn 69 | version 0.28 -->
### v0.28 — R7 — Suppression preserves provenance

Suppressed work remains auditable.

<!-- source: Continue Architecture Planning.md L83029–83035 | turn 69 | version 0.28 -->
### v0.28 — R8 — Unknown overlap is not disjointness

```
unknown
⇏
disjoint
```

<!-- source: Continue Architecture Planning.md L83037–83039 | turn 69 | version 0.28 -->
### v0.28 — R9 — Coverage is union-aware

Coverage must account for overlap before aggregation.

<!-- source: Continue Architecture Planning.md L83041–83047 | turn 69 | version 0.28 -->
### v0.28 — R10 — Candidate count does not establish coverage

```
N candidates
⇏
N units of search coverage
```

<!-- source: Continue Architecture Planning.md L83049–83051 | turn 69 | version 0.28 -->
### v0.28 — R11 — Evidence independence must be justified

Multiple paths do not automatically constitute independent confirmation.

<!-- source: Continue Architecture Planning.md L83053–83057 | turn 69 | version 0.28 -->
### v0.28 — R12 — Historical reconciliation is immutable

New reconciliation results do not rewrite historical observations or claims.

---

<!-- source: Continue Architecture Planning.md L84465–84465 | turn 71 | version 0.29 -->
## v0.29 — 29.33 v0.29 invariants



<!-- source: Continue Architecture Planning.md L84467–84475 | turn 71 | version 0.29 -->
### v0.29 — P1 — Discovery does not create authority

```
Evidence
⇏
Partition
```

without admission.

<!-- source: Continue Architecture Planning.md L84477–84481 | turn 71 | version 0.29 -->
### v0.29 — P2 — Partition proposal is not partition

```
PartitionProposal ≠ SearchPartition
```

<!-- source: Continue Architecture Planning.md L84483–84487 | turn 71 | version 0.29 -->
### v0.29 — P3 — Every admitted partition belongs to the domain

```
Partition ⊆ Domain
```

<!-- source: Continue Architecture Planning.md L84489–84491 | turn 71 | version 0.29 -->
### v0.29 — P4 — Expansion is budgeted

No dynamic expansion path may bypass expansion budgets.

<!-- source: Continue Architecture Planning.md L84493–84495 | turn 71 | version 0.29 -->
### v0.29 — P5 — Expansion is depth-bounded

Partition expansion cannot recurse indefinitely.

<!-- source: Continue Architecture Planning.md L84497–84499 | turn 71 | version 0.29 -->
### v0.29 — P6 — Duplicate partitions converge

Equivalent partition proposals resolve to existing partition identity.

<!-- source: Continue Architecture Planning.md L84501–84503 | turn 71 | version 0.29 -->
### v0.29 — P7 — Overlap is preserved

Overlapping partitions are related, not blindly merged.

<!-- source: Continue Architecture Planning.md L84505–84507 | turn 71 | version 0.29 -->
### v0.29 — P8 — Evidence is preserved

Rejecting/merging a partition proposal does not discard its evidence.

<!-- source: Continue Architecture Planning.md L84509–84515 | turn 71 | version 0.29 -->
### v0.29 — P9 — Partition existence does not schedule execution

```
PartitionCreated
⇏
WorkStarted
```

<!-- source: Continue Architecture Planning.md L84517–84519 | turn 71 | version 0.29 -->
### v0.29 — P10 — Expansion cannot override policy

A highly relevant partition may still be denied.

<!-- source: Continue Architecture Planning.md L84521–84523 | turn 71 | version 0.29 -->
### v0.29 — P11 — Search-space versions are immutable

Historical coverage remains attached to the snapshot under which it was measured.

<!-- source: Continue Architecture Planning.md L84525–84527 | turn 71 | version 0.29 -->
### v0.29 — P12 — Expansion does not invalidate historical claims automatically

New search-space knowledge creates new assessments.

<!-- source: Continue Architecture Planning.md L84529–84531 | turn 71 | version 0.29 -->
### v0.29 — P13 — Cycles are legal

The search-space graph is not required to be a tree.

<!-- source: Continue Architecture Planning.md L84533–84543 | turn 71 | version 0.29 -->
### v0.29 — P14 — Unknown remains valid

Insufficient evidence must produce:

```
UNKNOWN
```

rather than an invented relation.

---

<!-- source: Continue Architecture Planning.md L84793–84843 | turn 73 | version 0.30 -->
## v0.30 — The fundamental invariant

The entire system can be reduced to:

```
DISCOVER
   ≠
ACQUIRE
   ≠
RECOGNIZE
   ≠
CLASSIFY
   ≠
VERIFY
   ≠
RELEVANCE
   ≠
COMPLETE
```

And:

```
possible
   ↓
candidate
   ↓
authorized
   ↓
scheduled
   ↓
acquired
   ↓
observed
   ↓
recognized
   ↓
classified
   ↓
verified
   ↓
relevant
   ↓
covered
   ↓
possibly complete
```

No lower-cost observation should silently become a stronger epistemic claim.

---

<!-- source: Continue Architecture Planning.md L86174–86218 | turn 75 | version 0.30 -->
## v0.30 — 30.22 The deeper invariant

The frontier arbitrator must satisfy:

```
SELECT(w)
    ⇒
    ELIGIBLE(w)
```

but:

```
ELIGIBLE(w)
    ⇏
    SELECT(w)
```

And:

```
HIGH_SCORE(w)
    ⇏
    AUTHORIZED(w)
```

And:

```
LOW_PRIORITY(w)
    ⇏
    STARVABLE_FOREVER(w)
```

And:

```
SELECTED(w)
    ⇏
    EXECUTED(w)
```

because claiming or execution can still fail.

---

<!-- source: Continue Architecture Planning.md L86307–86356 | turn 75 | version 0.30 -->
## v0.30 — 30.25 v0.30 invariants

The important invariants are now:

```
1. Admission precedes arbitration.

2. Arbitration cannot override authorization.

3. Policy is not a priority.

4. Capability is not a priority.

5. Budget is not a priority.

6. Selected work must be eligible.

7. Selection does not guarantee successful claiming.

8. Selection does not guarantee execution.

9. Every work class has an explicit fairness policy.

10. No eligible work may starve indefinitely under
    a configured starvation guarantee.

11. Dependency priority may propagate but cannot
    bypass authorization.

12. Backpressure delays work; it does not redefine
    work as invalid.

13. Arbitration decisions are provenance-bearing.

14. Arbitration decisions are replayable under the
    same decision context.

15. Class-level fairness is distinct from item priority.

16. Cost estimates influence priority but do not
    become facts.

17. Historical performance influences arbitration but
    cannot override current evidence or policy.

18. Frontier state remains authoritative over
    scheduler assumptions.
```

---

<!-- source: Continue Architecture Planning.md L87600–87646 | turn 77 | version 0.31 -->
## v0.31 — 31.24 The central v0.31 invariants

```
1. Limit ≠ reservation ≠ consumption.

2. Estimated cost ≠ actual cost.

3. Reservation does not imply execution.

4. Consumed resources must be accounted exactly once.

5. Reservations must be atomic.

6. Hierarchical budgets cannot permit oversubscription.

7. Actual cost remains immutable evidence.

8. Cost estimates may influence scheduling but cannot
   override admission constraints.

9. Budget exhaustion ≠ frontier exhaustion.

10. Budget exhaustion ≠ search completeness.

11. Resource release must be distinguishable from
    actual consumption.

12. Overruns must be explicitly represented.

13. Every allocation has provenance.

14. Every settlement has an execution basis.

15. Resource accounting is independent from semantic
    relevance.

16. Historical cost is evidence for future estimation,
    not an authority over current execution.

17. Resource dimensions remain separately observable;
    scalar cost is derived, not fundamental.

18. Accounting conflicts must never be silently repaired
    by overwriting history.
```

---

<!-- source: Continue Architecture Planning.md L88454–88470 | turn 79 | version 0.32 -->
## v0.32 — 32.18 Accounting invariant under crash

For every resource dimension:

```
consumed
+
active reservations
+
recoverable uncertain consumption
≤
authorized accounting envelope
```

The exact accounting policy may differ, but uncertainty must not disappear.

---

<!-- source: Continue Architecture Planning.md L88568–88589 | turn 79 | version 0.32 -->
## v0.32 — 32.22 Recovery invariant for cursors

The key rule:

```
PersistedCursor(C)
    ⇒
    all knowledge required to justify C
    is durable
```

Equivalently:

```
cursor advancement
    requires
durable knowledge advancement
```

This is one of the strongest invariants in the entire architecture.

---

<!-- source: Continue Architecture Planning.md L88961–89008 | turn 79 | version 0.32 -->
## v0.32 — 32.34 v0.32 invariants

```
1. Durable knowledge must not depend on ephemeral runtime state.

2. A cursor cannot advance beyond durably persisted knowledge.

3. Incomplete transactions are distinguishable from committed
   transactions.

4. Recovery never fabricates observations.

5. Unknown execution outcome remains unknown until resolved.

6. Expired claims are recoverable.

7. Reservations and consumption remain distinct during recovery.

8. Duplicate processing is preferable to silent knowledge loss.

9. Idempotent operations may suppress duplicate durable effects
   without suppressing provenance.

10. Historical events are immutable.

11. Repairs produce explicit recovery events.

12. Materialized state may be rebuilt from durable state.

13. Schema evolution requires explicit versioning.

14. Snapshot integrity is independently verifiable.

15. Recovery occurs before normal frontier execution resumes.

16. Reconciliation may repair state but cannot rewrite history.

17. An artifact digest does not imply artifact durability.

18. A completed request does not imply a durable observation.

19. A durable observation does not automatically imply a durable
    semantic claim.

20. Crash recovery cannot upgrade epistemic confidence.
```

---

<!-- source: Continue Architecture Planning.md L89527–89554 | turn 81 | version 0.33 -->
## v0.33 — 33.11 Fencing invariant

A worker may mutate leased execution state only if:

```
workerId matches
AND
claimId matches
AND
epoch matches
AND
lease valid
```

Formally:

```
CanMutate(W, C)
    ⇒
    Owner(W) = Worker(C)
    ∧ Claim(W) = C
    ∧ Epoch(W) = Epoch(C)
    ∧ LeaseValid(C)
```

This prevents stale workers from corrupting current state.

---

<!-- source: Continue Architecture Planning.md L90227–90248 | turn 81 | version 0.33 -->
## v0.33 — 33.33 The complete ownership invariant

The strongest v0.33 rule is:

```
Only the current valid lease holder
with the current fencing epoch
may mutate execution state.
```

Formally:

```
Mutate(W, Worker, Claim)
    ⇒
    Valid(Claim)
    ∧ Owner(Claim) = Worker
    ∧ Epoch(Claim) = CurrentEpoch(W)
    ∧ LeaseNotExpired(Claim)
```

---

<!-- source: Continue Architecture Planning.md L90250–90274 | turn 81 | version 0.33 -->
## v0.33 — 33.34 The deeper distributed invariant

And:

```
At most one current authoritative claim
exists for a WorkItem
within a coordination scope.
```

This does **not** mean:

because crashes and external effects can produce duplicates.

The correct guarantee is:

```
one authoritative owner at a time
```

not:

That distinction prevents overclaiming.

---

<!-- source: Continue Architecture Planning.md L91668–91668 | turn 83 | version 0.34 -->
## v0.34 — 34.26 New Core Invariants



<!-- source: Continue Architecture Planning.md L92125–92156 | turn 85 | version 0.34 -->
## v0.34 — The major architectural invariants

The entire system ultimately rests on a few separations:

```
Candidate       ≠ Resource
Locator         ≠ Resource
Observation     ≠ Evidence
Evidence        ≠ Claim
Claim           ≠ Truth
Discovery       ≠ Acquisition
Acquisition     ≠ Recognition
Recognition     ≠ Classification
Classification  ≠ Relevance
Exhaustion      ≠ Completeness
Coverage        ≠ Completeness
Failure         ≠ Absence
Artifact        ≠ Resource
Artifact hash   ≠ Resource identity
Claim           ≠ Authorization
Capability      ≠ Authorization
Priority        ≠ Permission
Reservation     ≠ Consumption
Selection       ≠ Claim
Claim           ≠ Execution
Duplicate       ≠ Independent Evidence
Conflict        ≠ Failure
```

These separations are more important than any particular implementation.

---
