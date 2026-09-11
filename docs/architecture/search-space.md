# Search Space

> **Status:** DESIGNED
>
> **Source:** `Continue Architecture Planning.md`; `Userscript Discovery Prototype.md`
>
> **Purpose:** The search space: partitions, frontiers, expansion, reconciliation and search-space versions.

## Contents

- **17. Use observations to update the search space** — `Userscript Discovery Prototype.md` L825–863
- **27. This helps with incremental scanning** — `Userscript Discovery Prototype.md` L1247–1286
- **38. Avoid infinite candidate generation** — `Userscript Discovery Prototype.md` L1775–1800
- **v0.16 — Search space** — `Continue Architecture Planning.md` L65162–65166
- **v0.20 — Search-Space Partitioning + Discovery Strategies** — `Continue Architecture Planning.md` L69700–69732
- **v0.20 — 20.1 The Search Space** — `Continue Architecture Planning.md` L69734–69768
- **v0.20 — 20.2 What Is a Partition?** — `Continue Architecture Planning.md` L69770–69809
- **v0.20 — 20.3 Partition ≠ Candidate** — `Continue Architecture Planning.md` L69811–69841
- **v0.20 — 20.4 Partition Object** — `Continue Architecture Planning.md` L69843–69906
- **v0.20 — 20.5 Partition State** — `Continue Architecture Planning.md` L69908–69945
- **v0.20 — Saturated** — `Continue Architecture Planning.md` L69947–69949
- **v0.20 — Exhausted** — `Continue Architecture Planning.md` L69951–69957
- **v0.20 — 20.6 Search Coverage** — `Continue Architecture Planning.md` L69959–69993
- **v0.20 — 20.7 Strategy Contract** — `Continue Architecture Planning.md` L69995–70024
- **v0.20 — 20.8 Strategy vs Candidate Source** — `Continue Architecture Planning.md` L70026–70060
- **v0.20 — 20.9 Strategy Types** — `Continue Architecture Planning.md` L70062–70064
- **v0.20 — Seed Expansion** — `Continue Architecture Planning.md` L70066–70078
- **v0.20 — Repository Expansion** — `Continue Architecture Planning.md` L70080–70088
- **v0.20 — Sitemap Expansion** — `Continue Architecture Planning.md` L70090–70098
- **v0.20 — API Schema Expansion** — `Continue Architecture Planning.md` L70100–70110
- **v0.20 — Document-Family Expansion** — `Continue Architecture Planning.md` L70112–70127
- **v0.20 — 20.11 Probe** — `Continue Architecture Planning.md` L70197–70227
- **v0.20 — 20.12 Exploration Plan** — `Continue Architecture Planning.md` L70229–70282
- **v0.20 — 20.13 Exploration Must Remain Budgeted** — `Continue Architecture Planning.md` L70284–70320
- **v0.20 — 20.14 Adaptive Partition Priority** — `Continue Architecture Planning.md` L70322–70373
- **v0.20 — 20.15 Exploration vs Exploitation** — `Continue Architecture Planning.md` L70375–70409
- **v0.20 — 20.16 Aging** — `Continue Architecture Planning.md` L70411–70444
- **v0.20 — 20.17 Partition Splitting** — `Continue Architecture Planning.md` L70446–70512
- **v0.20 — 20.18 Partition Merge** — `Continue Architecture Planning.md` L70514–70550
- **v0.20 — 20.19 Partition Graph** — `Continue Architecture Planning.md` L70552–70588
- **v0.20 — 20.20 SearchSpace** — `Continue Architecture Planning.md` L70590–70645
- **v0.20 — 20.21 Search-Space Controller** — `Continue Architecture Planning.md` L70647–70694
- **v0.20 — 20.22 Three-Level Control Plane** — `Continue Architecture Planning.md` L70696–70724
- **v0.20 — 20.23 Candidate Sources Remain Low-Level** — `Continue Architecture Planning.md` L70726–70766
- **v0.20 — 20.24 Termination Becomes More Sophisticated** — `Continue Architecture Planning.md` L70768–70824
- **v0.20 — 20.25 Saturation** — `Continue Architecture Planning.md` L70826–70858
- **v0.20 — 20.26 Partition Statistics** — `Continue Architecture Planning.md` L70860–70905
- **v0.20 — 20.27 Discovery Efficiency** — `Continue Architecture Planning.md` L70907–70942
- **v0.28 — Search-Space Reconciliation & Frontier Deduplication** — `Continue Architecture Planning.md` L81648–81672
- **v0.28 — Search-Space Reconciliation & Frontier Deduplication** — `Continue Architecture Planning.md` L81684–81726
- **v0.28 — 28.1 The problem with naive deduplication** — `Continue Architecture Planning.md` L81728–81776
- **v0.28 — 28.2 Five different kinds of duplication** — `Continue Architecture Planning.md` L81778–81802
- **v0.28 — 28.3 Search-space overlap** — `Continue Architecture Planning.md` L81804–81846
- **v0.28 — 28.4 SearchPartitionRelation** — `Continue Architecture Planning.md` L81848–81892
- **v0.28 — 28.5 Coverage overlap** — `Continue Architecture Planning.md` L81894–81937
- **v0.28 — 28.6 Frontier deduplication** — `Continue Architecture Planning.md` L81939–81969
- **v0.28 — 28.7 SearchWorkKey** — `Continue Architecture Planning.md` L81971–82027
- **v0.28 — 28.8 Work equivalence** — `Continue Architecture Planning.md` L82029–82063
- **v0.28 — 28.9 Candidate convergence** — `Continue Architecture Planning.md` L82065–82106
- **v0.28 — 28.11 Artifact convergence** — `Continue Architecture Planning.md` L82157–82197
- **v0.28 — 28.12 Discovery independence** — `Continue Architecture Planning.md` L82199–82239
- **v0.28 — 28.13 Evidence independence model** — `Continue Architecture Planning.md` L82241–82281
- **v0.28 — 28.14 Coverage provenance** — `Continue Architecture Planning.md` L82283–82323
- **v0.28 — 28.15 Coverage relation** — `Continue Architecture Planning.md` L82325–82360
- **v0.28 — 28.16 Coverage union** — `Continue Architecture Planning.md` L82362–82389
- **v0.28 — 28.17 Disjoint partitions** — `Continue Architecture Planning.md` L82391–82425
- **v0.28 — 28.18 Unknown overlap** — `Continue Architecture Planning.md` L82427–82460
- **v0.28 — 28.19 Frontier duplicate suppression** — `Continue Architecture Planning.md` L82462–82506
- **v0.28 — 28.20 Duplicate suppression must preserve provenance** — `Continue Architecture Planning.md` L82508–82543
- **v0.28 — 28.21 Convergence graph** — `Continue Architecture Planning.md` L82545–82577
- **v0.28 — 28.22 Search-space graph** — `Continue Architecture Planning.md` L82579–82605
- **v0.28 — 28.23 Search-space coverage ledger** — `Continue Architecture Planning.md` L82607–82640
- **v0.28 — 28.24 Candidate count is not coverage** — `Continue Architecture Planning.md` L82642–82693
- **v0.28 — 28.25 Search-space deduplication vs candidate deduplication** — `Continue Architecture Planning.md` L82695–82697
- **v0.28 — Candidate deduplication** — `Continue Architecture Planning.md` L82699–82705
- **v0.28 — Search-space deduplication** — `Continue Architecture Planning.md` L82707–82734
- **v0.28 — 28.26 Adaptive strategy interaction** — `Continue Architecture Planning.md` L82736–82786
- **v0.28 — 28.27 Example** — `Continue Architecture Planning.md` L82788–82839
- **v0.28 — 28.28 Reconciliation algorithm** — `Continue Architecture Planning.md` L82841–82883
- **v0.28 — 28.29 Reconciliation must be monotonic** — `Continue Architecture Planning.md` L82885–82922
- **v0.28 — 28.30 Reconciliation does not delete evidence** — `Continue Architecture Planning.md` L82924–82946
- **v0.28 — 28.34 The deeper architectural result** — `Continue Architecture Planning.md` L83130–83165
- **v0.29 — Dynamic Search-Space Expansion** — `Continue Architecture Planning.md` L83238–83284
- **v0.29 — 29.1 The central distinction** — `Continue Architecture Planning.md` L83286–83322
- **v0.29 — 29.2 PartitionProposal** — `Continue Architecture Planning.md` L83324–83376
- **v0.29 — 29.3 Why proposals are necessary** — `Continue Architecture Planning.md` L83378–83410
- **v0.29 — 29.4 PartitionAdmissionController** — `Continue Architecture Planning.md` L83412–83460
- **v0.29 — 29.5 Partition identity** — `Continue Architecture Planning.md` L83462–83522
- **v0.29 — 29.6 Partition explosion** — `Continue Architecture Planning.md` L83524–83550
- **v0.29 — 29.7 ExpansionBudget** — `Continue Architecture Planning.md` L83552–83581
- **v0.29 — 29.8 Local expansion rate** — `Continue Architecture Planning.md` L83583–83606
- **v0.29 — 29.9 Expansion rate limiting** — `Continue Architecture Planning.md` L83608–83640
- **v0.29 — 29.10 Evidence threshold** — `Continue Architecture Planning.md` L83642–83670
- **v0.29 — 29.11 Partition proposal epistemic status** — `Continue Architecture Planning.md` L83672–83693
- **v0.29 — 29.12 Hypothesis connection** — `Continue Architecture Planning.md` L83695–83726
- **v0.29 — 29.13 Partition generation sources** — `Continue Architecture Planning.md` L83728–83779
- **v0.29 — 29.14 Expansion provider boundary** — `Continue Architecture Planning.md` L83781–83812
- **v0.29 — 29.15 Dynamic search-space graph** — `Continue Architecture Planning.md` L83814–83843
- **v0.29 — 29.16 Partition generation event** — `Continue Architecture Planning.md` L83845–83889
- **v0.29 — 29.17 Search-space versioning** — `Continue Architecture Planning.md` L83891–83922
- **v0.29 — 29.18 SearchSpaceSnapshot** — `Continue Architecture Planning.md` L83924–83960
- **v0.29 — 29.19 Expansion and completeness** — `Continue Architecture Planning.md` L83962–84007
- **v0.29 — 29.20 Dynamic expansion and negative evidence** — `Continue Architecture Planning.md` L84009–84053
- **v0.29 — 29.21 Expansion priorities** — `Continue Architecture Planning.md` L84055–84083
- **v0.29 — 29.22 Expansion depth** — `Continue Architecture Planning.md` L84085–84120
- **v0.29 — 29.23 Expansion loops** — `Continue Architecture Planning.md` L84122–84165
- **v0.29 — 29.24 Expansion cycle ≠ failure** — `Continue Architecture Planning.md` L84167–84195
- **v0.29 — 29.25 Partition admission states** — `Continue Architecture Planning.md` L84197–84230
- **v0.29 — 29.26 Partition proposal accounting** — `Continue Architecture Planning.md` L84232–84262
- **v0.29 — 29.27 Partition explosion protection** — `Continue Architecture Planning.md` L84264–84289
- **v0.29 — 29.28 Admission algorithm** — `Continue Architecture Planning.md` L84291–84337
- **v0.29 — 29.29 Frontier generation** — `Continue Architecture Planning.md` L84339–84367
- **v0.29 — 29.31 Two expansion paths** — `Continue Architecture Planning.md` L84401–84437
- **v0.29 — 29.32 Search-space discovery as first-class knowledge** — `Continue Architecture Planning.md` L84439–84463
- **v0.29 — 29.34 The system after v0.29** — `Continue Architecture Planning.md` L84545–84576
- **v0.29 takeaway** — `Continue Architecture Planning.md` L84610–84662

## Related Documents

- [The Discovery Loop](../concepts/discovery-loop.md)
- [Coverage, Completeness and Absence](coverage-and-absence.md)
- [Strategies, Query Planning and Enumeration](strategy-and-planning.md)
- [Domains, Sessions and Termination](sessions-and-domains.md)

---

<!-- source: Userscript Discovery Prototype.md L825–863 | turn 7 | version ? -->
## 17. Use observations to update the search space

The algorithm can be expressed as a loop over **beliefs**:

```
SearchSpace
     │
     ▼
Candidate
     │
     ▼
Observation
     │
     ▼
Update belief
     │
     ├──────────────┐
     ▼              ▼
Confirmed       New candidates
     │              │
     │              └──────► SearchSpace
     ▼
Discovery DB
```

Formally:

$$S_{n+1}=S_n-\{c_n\}+\operatorname{Expand}(o_n)$$

where:

* $S_n$ is the remaining search space,
* $c_n$ is the candidate just tested,
* $o_n$ is the observation,
* `Expand()` generates candidates suggested by that observation.

This is a very general pattern and isn't specific to DVB.

---

<!-- source: Userscript Discovery Prototype.md L1247–1286 | turn 9 | version ? -->
## 27. This helps with incremental scanning

Imagine a receiver is continuously monitoring an area.

Instead of:

```
scan everything
wait
scan everything again
wait
...
```

use:

```
             Knowledge Base
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
Known candidates         Unknown regions
        │                     │
   quick verification     blind discovery
        │                     │
        └──────────┬──────────┘
                   ▼
             Updated KB
```

Now the algorithm can detect:

* newly appearing multiplexes,
* disappeared multiplexes,
* changed parameters,
* changed service metadata.

That is much closer to a **generic discovery service** than a traditional one-shot blind scan.

---

<!-- source: Userscript Discovery Prototype.md L1775–1800 | turn 11 | version ? -->
## 38. Avoid infinite candidate generation

Metadata can potentially produce candidates you've already investigated.

So the scheduler needs canonicalization:

```
canonicalize(candidate)
```

followed by:

```
if candidate already known:
    merge evidence
else:
    enqueue
```

You can think of this as maintaining a visited set:

$$V = \{\operatorname{canonical}(c)\}$$

Without this, a network graph can repeatedly enqueue the same frequencies.

---

<!-- source: Continue Architecture Planning.md L65162–65166 | turn 45 | version 0.16 -->
### v0.16 — Search space

> Where are we allowed to look?

`DiscoveryDomain`

<!-- source: Continue Architecture Planning.md L69700–69732 | turn 53 | version 0.20 -->
## v0.20 — Search-Space Partitioning + Discovery Strategies

At v0.19 the engine can represent:

```
Locator
   ↓
Resource
   ↓
Representation
   ↓
Artifact
   ↓
Revision
   ↓
Observation
   ↓
Evidence
```

But one major question remains:

> **How does the engine systematically explore an unknown resource universe rather than merely following whatever candidates happen to appear?**

This is the point where the DVB blind-scan analogy becomes structurally useful.

The important abstraction is not “scan URLs.”

It is:

> **Partition an unknown search space, allocate exploration budget across partitions, observe what each partition reveals, then adapt the frontier.**

---

<!-- source: Continue Architecture Planning.md L69734–69768 | turn 53 | version 0.20 -->
## v0.20 — 20.1 The Search Space

A `DiscoveryDomain` currently says:

```
allowed schemes
allowed origins
allowed types
seeds
sources
depth
budgets
```

That defines the boundary, but not its internal structure.

We now introduce:

```
DiscoveryDomain
      │
      ▼
SearchSpace
      │
      ├── Partition A
      ├── Partition B
      ├── Partition C
      └── ...
```

A partition is simply:

> A bounded subset of the discovery universe that can be explored independently.

---

<!-- source: Continue Architecture Planning.md L69770–69809 | turn 53 | version 0.20 -->
## v0.20 — 20.2 What Is a Partition?

For a web/document discovery system, partitions can be based on:

```
Origin
Path prefix
Resource type
Discovery mechanism
Document family
Language
Repository
Protocol
Source
Time/revision range
```

For example:

```
example.com
│
├── /docs/
│
├── /manuals/
│
├── /downloads/
│
├── /api/
│
├── /assets/
│
└── /archive/
```

These are not necessarily directories in the filesystem sense.

They are **search regions**.

---

<!-- source: Continue Architecture Planning.md L69811–69841 | turn 53 | version 0.20 -->
## v0.20 — 20.3 Partition ≠ Candidate

This distinction matters.

```
Partition:
    https://example.com/manuals/*
```

is not:

```
Candidate:
    https://example.com/manuals/gen2.pdf
```

The partition is a region.

The candidate is an individual possible resource.

Therefore:

```
Partition
   ↓
exploration strategy
   ↓
candidate proposals
```

---

<!-- source: Continue Architecture Planning.md L69843–69906 | turn 53 | version 0.20 -->
## v0.20 — 20.4 Partition Object

Introduce:

```JavaScript
class SearchPartition {
    constructor(data = {}) {
        this.id = data.id || makeId('partition');

        this.domainId =
            data.domainId || null;

        this.kind =
            data.kind || 'unknown';

        this.selector =
            data.selector || null;

        this.parentId =
            data.parentId || null;

        this.depth =
            Number.isFinite(data.depth)
                ? data.depth
                : 0;

        this.priority =
            Number.isFinite(data.priority)
                ? data.priority
                : 0;

        this.status =
            data.status || 'unexplored';

        this.createdAt =
            data.createdAt || now();
    }

    serialize() {
        return { ...this };
    }
}
```

Example:

```JavaScript
{
    kind: "path-prefix",
    selector: "https://example.com/manuals/",
    depth: 1
}
```

Another:

```JavaScript
{
    kind: "resource-type",
    selector: "document/service-manual"
}
```

---

<!-- source: Continue Architecture Planning.md L69908–69945 | turn 53 | version 0.20 -->
## v0.20 — 20.5 Partition State

A partition needs its own lifecycle.

```
UNEXPLORED
     ↓
DISCOVERING
     ↓
ACTIVE
     ↓
SATURATED
     ↓
EXHAUSTED
```

Alternative terminals:

```
DENIED
SKIPPED
FAILED
CANCELLED
```

The distinction between:

```
SATURATED
```

and:

```
EXHAUSTED
```

is useful.

<!-- source: Continue Architecture Planning.md L69947–69949 | turn 53 | version 0.20 -->
### v0.20 — Saturated

The current strategy is no longer finding useful new information.

<!-- source: Continue Architecture Planning.md L69951–69957 | turn 53 | version 0.20 -->
### v0.20 — Exhausted

The defined exploration method has completed its search.

These are not equivalent.

---

<!-- source: Continue Architecture Planning.md L69959–69993 | turn 53 | version 0.20 -->
## v0.20 — 20.6 Search Coverage

Once partitions exist, the engine can ask:

> How much of the search space have we actually explored?

Introduce a coverage concept:

```
Partition
│
├── exploredWork
├── discoveredCandidates
├── successfulAcquisitions
├── usefulDiscoveries
└── coverageState
```

But be careful:

```
100% candidate coverage
```

does not necessarily mean:

```
100% resource coverage
```

The engine cannot generally prove that all web resources have been discovered.

Therefore coverage must be **relative to an exploration strategy**.

---

<!-- source: Continue Architecture Planning.md L69995–70024 | turn 53 | version 0.20 -->
## v0.20 — 20.7 Strategy Contract

Introduce:

```JavaScript
class DiscoveryStrategy {
    canExplore(partition, context) {
        return false;
    }

    async explore(partition, context) {
        throw new Error('Not implemented');
    }

    describe() {
        return {
            id: 'unknown-strategy',
            name: 'Unknown Discovery Strategy'
        };
    }
}
```

The strategy does not own the global scheduler.

It answers:

> Given this search region, how should we explore it?

---

<!-- source: Continue Architecture Planning.md L70026–70060 | turn 53 | version 0.20 -->
## v0.20 — 20.8 Strategy vs Candidate Source

These are different abstractions.

```
CandidateSource
    = HOW TO EXTRACT CANDIDATES FROM EVIDENCE

DiscoveryStrategy
    = HOW TO EXPLORE A SEARCH REGION
```

For example:

```
HTML Link Source
```

can extract:

```
<a href="/manual.pdf">
```

while:

```
Path Exploration Strategy
```

decides which path region deserves attention.

This distinction prevents the CandidateSource interface from becoming overloaded.

---

<!-- source: Continue Architecture Planning.md L70062–70064 | turn 53 | version 0.20 -->
## v0.20 — 20.9 Strategy Types

A generic discovery engine can support several strategies.

<!-- source: Continue Architecture Planning.md L70066–70078 | turn 53 | version 0.20 -->
### v0.20 — Seed Expansion

```
Seed
 ↓
Acquire
 ↓
Extract candidates
 ↓
Expand frontier
```

This is the default crawler-like strategy.

<!-- source: Continue Architecture Planning.md L70080–70088 | turn 53 | version 0.20 -->
### v0.20 — Repository Expansion

```
/docs/
/manuals/
/archive/
```

Explore each discovered repository-like region.

<!-- source: Continue Architecture Planning.md L70090–70098 | turn 53 | version 0.20 -->
### v0.20 — Sitemap Expansion

```
sitemap
 ↓
partition URLs
 ↓
explore partitions
```

<!-- source: Continue Architecture Planning.md L70100–70110 | turn 53 | version 0.20 -->
### v0.20 — API Schema Expansion

```
API
 ↓
schema
 ↓
endpoint families
 ↓
candidate endpoints
```

<!-- source: Continue Architecture Planning.md L70112–70127 | turn 53 | version 0.20 -->
### v0.20 — Document-Family Expansion

```
service-manual
      ↓
related document family
      ↓
parts catalog
bulletin
revision
supplement
```

The last category becomes particularly useful for the user's service-document acquisition work.

---

<!-- source: Continue Architecture Planning.md L70197–70227 | turn 53 | version 0.20 -->
## v0.20 — 20.11 Probe

This suggests another useful abstraction:

```
SearchPartition
       ↓
Probe
       ↓
Observation
```

A probe is an attempt to obtain information about a search region.

In the current engine, a probe usually corresponds to an acquisition work item.

But eventually:

```
Probe
├── HTTP GET
├── HEAD
├── sitemap inspection
├── metadata inspection
├── browser observation
└── other authorized mechanisms
```

This connects discovery strategy to acquisition without allowing the strategy to bypass acquisition policy.

---

<!-- source: Continue Architecture Planning.md L70229–70282 | turn 53 | version 0.20 -->
## v0.20 — 20.12 Exploration Plan

A strategy can produce an exploration plan:

```JavaScript
class ExplorationPlan {
    constructor(data = {}) {
        this.id = data.id || makeId('explore');

        this.partitionId =
            data.partitionId || null;

        this.strategyId =
            data.strategyId || null;

        this.work = data.work || [];

        this.priority =
            Number.isFinite(data.priority)
                ? data.priority
                : 0;

        this.reason =
            data.reason || null;

        this.createdAt =
            data.createdAt || now();
    }
}
```

Example:

```
Partition:
    /manuals/

Strategy:
    sitemap-expansion

Plan:
    inspect sitemap
    acquire candidate URLs
    classify documents
    look for revision relationships
```

The strategy proposes.

The frontier runtime schedules.

The acquisition runtime enforces execution.

---

<!-- source: Continue Architecture Planning.md L70284–70320 | turn 53 | version 0.20 -->
## v0.20 — 20.13 Exploration Must Remain Budgeted

A partition must never become an escape hatch around global limits.

We therefore need:

```
Global Budget
      │
      ├── Partition Budget
      │      │
      │      └── WorkItem Budget
      │
      └── Acquisition Budget
```

For example:

```JavaScript
{
    global: {
        maxProbes: 150
    },

    partition: {
        maxProbes: 20
    },

    strategy: {
        maxWorkItems: 50
    }
}
```

All three must be satisfied.

---

<!-- source: Continue Architecture Planning.md L70322–70373 | turn 53 | version 0.20 -->
## v0.20 — 20.14 Adaptive Partition Priority

This is where the system becomes more interesting.

Suppose:

```
Partition A
    40 candidates
    12 useful documents

Partition B
    80 candidates
    0 useful documents

Partition C
    10 candidates
    7 useful documents
```

A static BFS strategy might continue equally.

An adaptive strategy can prioritize:

```
C > A > B
```

based on observed yield.

Introduce:

```
partition utility
```

Conceptually:

```
Utility =
    expected discovery yield
    × relevance
    × confidence
    − exploration cost
    − failure risk
```

Do not make this formula mandatory in v0.20.

The architecture should expose the concept without locking in a scoring algorithm.

---

<!-- source: Continue Architecture Planning.md L70375–70409 | turn 53 | version 0.20 -->
## v0.20 — 20.15 Exploration vs Exploitation

This creates the classic tradeoff:

```
EXPLORE
"Try regions we know little about."

EXPLOIT
"Continue regions that are already producing useful results."
```

A purely exploitative system can get trapped.

A purely exploratory system wastes budget.

Therefore:

```
Frontier
│
├── exploration quota
└── exploitation quota
```

Example:

```
70% exploitation
30% exploration
```

But the ratio should be policy/configuration, not hardcoded into the architecture.

---

<!-- source: Continue Architecture Planning.md L70411–70444 | turn 53 | version 0.20 -->
## v0.20 — 20.16 Aging

A partition that has waited too long should eventually receive attention.

```
effectivePriority =
    basePriority
    +
    agingFactor × waitingTime
```

This prevents:

```
high-yield partition
```

from permanently starving:

```
low-yield partition
```

The same principle already exists for `WorkItem`.

Now it applies at two levels:

```
Partition fairness
        ↓
Work fairness
```

---

<!-- source: Continue Architecture Planning.md L70446–70512 | turn 53 | version 0.20 -->
## v0.20 — 20.17 Partition Splitting

A partition can reveal enough information to justify subdivision.

Example:

```
/docs/
```

reveals:

```
/docs/manuals/
/docs/bulletins/
/docs/parts/
```

The strategy can produce:

```
/docs/
   │
   ├── /docs/manuals/
   ├── /docs/bulletins/
   └── /docs/parts/
```

This is analogous to recursively refining a search region.

Introduce:

```JavaScript
class PartitionProposal {
    constructor(data = {}) {
        this.parentPartitionId =
            data.parentPartitionId || null;

        this.kind =
            data.kind || 'unknown';

        this.selector =
            data.selector || null;

        this.reason =
            data.reason || null;

        this.evidenceIds =
            data.evidenceIds || [];

        this.confidence =
            Number.isFinite(data.confidence)
                ? data.confidence
                : 0;
    }
}
```

Again:

```
proposal ≠ partition
```

The controller validates and admits it.

---

<!-- source: Continue Architecture Planning.md L70514–70550 | turn 53 | version 0.20 -->
## v0.20 — 20.18 Partition Merge

Partitions can also overlap.

For example:

```
/docs/
```

and:

```
/service/
```

may both include:

```
/docs/service/
```

Do not automatically merge them.

Instead preserve:

```
Partition A
     │
     └── overlaps ──► Partition B
```

Why?

Because the overlap itself may reveal multiple discovery strategies.

---

<!-- source: Continue Architecture Planning.md L70552–70588 | turn 53 | version 0.20 -->
## v0.20 — 20.19 Partition Graph

The ResourceGraph now gets a companion:

```
                    SEARCH SPACE
                         │
                         ▼
                    PARTITION
                    /       \
                   /         \
                  ▼           ▼
             Partition A   Partition B
                  │
                  ▼
                Probe
                  │
                  ▼
             Observation
                  │
                  ▼
               Resource
```

Relationships:

```
contains
parent-of
child-of
overlaps
derived-from
explored-by
saturated-by
```

---

<!-- source: Continue Architecture Planning.md L70590–70645 | turn 53 | version 0.20 -->
## v0.20 — 20.20 SearchSpace

Introduce the aggregate:

```JavaScript
class SearchSpace {
    constructor(data = {}) {
        this.id = data.id || makeId('space');

        this.domainId =
            data.domainId || null;

        this.partitionIds =
            data.partitionIds || [];

        this.rootPartitionIds =
            data.rootPartitionIds || [];

        this.createdAt =
            data.createdAt || now();
    }
}
```

The domain answers:

```
"What universe is permitted?"
```

The search space answers:

```
"How is that universe currently partitioned?"
```

The frontier answers:

```
"What work remains?"
```

Three distinct concepts:

```
Domain
  = legal/search boundary

SearchSpace
  = structural decomposition

Frontier
  = unfinished exploration work
```

---

<!-- source: Continue Architecture Planning.md L70647–70694 | turn 53 | version 0.20 -->
## v0.20 — 20.21 Search-Space Controller

Introduce a controller above strategies.

```JavaScript
class SearchSpaceController {
    constructor(options = {}) {
        this.strategies =
            options.strategies || [];

        this.partitions =
            new Map();

        this.proposals =
            new Map();
    }

    registerPartition(partition) {
        this.partitions.set(
            partition.id,
            partition
        );

        return partition;
    }

    selectStrategy(partition, context) {
        return this.strategies
            .filter(strategy =>
                strategy.canExplore(
                    partition,
                    context
                )
            )
            .sort(
                (a, b) =>
                    b.priority() -
                    a.priority()
            )[0] || null;
    }
}
```

The controller owns partition governance.

Strategies do not directly mutate the search space.

---

<!-- source: Continue Architecture Planning.md L70696–70724 | turn 53 | version 0.20 -->
## v0.20 — 20.22 Three-Level Control Plane

We now have:

```
                 SCAN SESSION
                      │
                      ▼
               DISCOVERY DOMAIN
                      │
                      ▼
                SEARCH SPACE
                      │
                      ▼
             SEARCH-SPACE CONTROLLER
                      │
                      ▼
               DISCOVERY STRATEGY
                      │
                      ▼
                 EXPLORATION PLAN
                      │
                      ▼
                FRONTIER RUNTIME
```

This is cleaner than having every source decide everything.

---

<!-- source: Continue Architecture Planning.md L70726–70766 | turn 53 | version 0.20 -->
## v0.20 — 20.23 Candidate Sources Remain Low-Level

The distinction is now:

```
Search Strategy
    "Explore /manuals/"

        ↓

Candidate Source
    "Extract href values from this HTML"

        ↓

Candidate Proposal
    "/manuals/x.pdf"
```

So:

```
STRATEGY
    decides WHERE/HOW to explore

SOURCE
    decides HOW TO EXTRACT candidates

NORMALIZER
    decides WHAT candidate identity means

POLICY
    decides WHAT is authorized

RUNTIME
    decides HOW execution occurs
```

This division is important.

---

<!-- source: Continue Architecture Planning.md L70768–70824 | turn 53 | version 0.20 -->
## v0.20 — 20.24 Termination Becomes More Sophisticated

Previously:

```
frontier empty
```

was enough for natural completion.

With search partitions, we can have:

```
all admitted partitions exhausted
```

or:

```
all useful strategies exhausted
```

or:

```
global exploration budget exhausted
```

Therefore termination should consider:

```
queued work
+
running work
+
delayed work
+
active partitions
+
future retry
```

A possible condition:

```
Natural completion iff:

No runnable WorkItems
AND
No running WorkItems
AND
No active partition with admitted exploration
AND
No pending retry
```

---

<!-- source: Continue Architecture Planning.md L70826–70858 | turn 53 | version 0.20 -->
## v0.20 — 20.25 Saturation

We should introduce an explicit concept of saturation.

A partition may produce:

```
100 candidates
```

but after normalization:

```
95 duplicates
5 already known
0 new resources
```

The partition may be considered:

```
low-yield
```

rather than simply:

```
completed
```

This matters for adaptive discovery.

---

<!-- source: Continue Architecture Planning.md L70860–70905 | turn 53 | version 0.20 -->
## v0.20 — 20.26 Partition Statistics

Useful metrics:

```JavaScript
{
    probes: 0,

    candidatesProposed: 0,

    candidatesAccepted: 0,

    candidatesMerged: 0,

    resourcesDiscovered: 0,

    artifactsObserved: 0,

    usefulDiscoveries: 0,

    failures: 0,

    duplicates: 0,

    cost: {
        requests: 0,
        bytes: 0,
        elapsedMs: 0
    }
}
```

Then:

```
yield =
    usefulDiscoveries / probes
```

can become an input to adaptive strategy selection.

But again:

> Metrics inform strategy; they do not become truth claims about completeness.

---

<!-- source: Continue Architecture Planning.md L70907–70942 | turn 53 | version 0.20 -->
## v0.20 — 20.27 Discovery Efficiency

This allows a more meaningful metric than raw URL count.

Instead of:

```
10,000 URLs discovered
```

we can measure:

```
10,000 candidates
      ↓
1,800 unique resources
      ↓
430 relevant classifications
      ↓
120 verified artifacts
```

This is much closer to actual discovery value.

Possible metrics:

```
candidate yield
resource yield
artifact yield
classification yield
verification yield
cost per useful resource
```

---

<!-- source: Continue Architecture Planning.md L81648–81672 | turn 67 | version 0.28 -->
## v0.28 — Search-Space Reconciliation & Frontier Deduplication

with the central problem:

```
Sitemap
       \
Repository → same resources
       /
API
```

and the need to distinguish:

```
duplicate candidate
duplicate observation
duplicate enumeration
overlapping partition
independent confirmation
same-content resource
same search-space coverage
```

Without this layer, the engine can become very good at scanning the same universe several times while incorrectly reporting increased coverage.

<!-- source: Continue Architecture Planning.md L81684–81726 | turn 69 | version 0.28 -->
## v0.28 — Search-Space Reconciliation & Frontier Deduplication

v0.27 gave us a formal enumeration layer:

```
Enumerator
    ↓
EnumerationPage
    ↓
EnumerationEntry
    ↓
CandidateProposal
```

But a serious discovery engine now encounters a different problem:

```
Sitemap ─────────────┐
                    │
Repository ─────────┼──→ same URL
                    │
API ────────────────┤
                    │
Document reference ─┘
```

The engine must determine whether these represent:

* the same **candidate**
* the same **locator**
* the same **resource**
* the same **artifact**
* the same **enumeration**
* independent **evidence**
* overlapping **search coverage**

These are not the same question.

The central rule for v0.28 is:

> **Deduplication may collapse redundant work, but must never collapse provenance or falsely convert overlap into independent coverage.**

---

<!-- source: Continue Architecture Planning.md L81728–81776 | turn 69 | version 0.28 -->
## v0.28 — 28.1 The problem with naive deduplication

A simple crawler usually does:

```
URL
 ↓
Set<URL>
 ↓
already seen?
```

That is insufficient.

Consider:

```
Sitemap:
    /manual.pdf

Repository:
    /manual.pdf

HTML:
    /manual.pdf
```

Naive deduplication says:

```
3 discoveries → 1 URL
```

But the epistemic structure is:

```
                 /manual.pdf
                 ▲    ▲    ▲
                 │    │    │
             sitemap repo HTML
```

Those are potentially **three independent discovery paths**.

The candidate should be deduplicated.

The evidence should not.

---

<!-- source: Continue Architecture Planning.md L81778–81802 | turn 69 | version 0.28 -->
## v0.28 — 28.2 Five different kinds of duplication

We now need explicit categories.

| Duplication | Meaning |
| --- | --- |
| Candidate duplicate | Same canonical candidate identity |
| Locator duplicate | Same addressing mechanism |
| Observation duplicate | Same observed response |
| Artifact duplicate | Same bytes |
| Coverage overlap | Two search procedures cover the same space |

These must remain independent.

```
Candidate deduplication
        ≠
Evidence deduplication
        ≠
Artifact deduplication
        ≠
Coverage deduplication
```

---

<!-- source: Continue Architecture Planning.md L81804–81846 | turn 69 | version 0.28 -->
## v0.28 — 28.3 Search-space overlap

Suppose:

```
Partition A = /manuals/*
Partition B = /documents/*
```

and:

```
/manuals/x.pdf
```

belongs to both.

That is not an error.

It means:

```
A ∩ B ≠ ∅
```

The search-space graph therefore needs explicit overlap.

```
Partition A
 ├── x.pdf
 ├── y.pdf
 └── z.pdf
       ▲
       │
       │ overlap
       │
Partition B
 ├── z.pdf
 ├── q.pdf
 └── r.pdf
```

---

<!-- source: Continue Architecture Planning.md L81848–81892 | turn 69 | version 0.28 -->
## v0.28 — 28.4 SearchPartitionRelation

Introduce an explicit relation.

```JavaScript
class SearchPartitionRelation {
    constructor(data = {}) {
        this.id = data.id || makeId('prel');

        this.fromPartitionId = data.fromPartitionId || null;
        this.toPartitionId = data.toPartitionId || null;

        this.relation = data.relation || 'unknown';

        this.scope = data.scope || null;

        this.evidenceIds = data.evidenceIds || [];

        this.confidence = Number.isFinite(data.confidence)
            ? data.confidence
            : 0;

        this.createdAt = data.createdAt || now();
    }

    serialize() {
        return { ...this };
    }
}
```

Relations might include:

```
contains
subset-of
overlaps
disjoint
equivalent
unknown
```

Do not infer `disjoint` merely because no overlap has yet been observed.

---

<!-- source: Continue Architecture Planning.md L81894–81937 | turn 69 | version 0.28 -->
## v0.28 — 28.5 Coverage overlap

Suppose:

```
Partition A:
    100 entries

Partition B:
    100 entries

Observed intersection:
    80 entries
```

Naively:

```
coverage = 200
```

is wrong.

The union is:

```
100 + 100 - 80 = 120
```

But even that only works if the entry identities and universe definitions are comparable.

Therefore:

```
Coverage(A) + Coverage(B)
    ≠
Coverage(A ∪ B)
```

unless overlap is known.

This is a key reason coverage cannot simply be accumulated by counting discovered candidates.

---

<!-- source: Continue Architecture Planning.md L81939–81969 | turn 69 | version 0.28 -->
## v0.28 — 28.6 Frontier deduplication

The FrontierRuntime currently prevents duplicate work items based on work identity.

v0.28 introduces another layer:

```
Work deduplication
        ↓
Search-unit deduplication
```

For example:

```
Tactic A → enumerate sitemap page 1
Tactic B → enumerate same sitemap page 1
```

These may be equivalent work.

But:

```
Sitemap → manual.pdf
Repository → manual.pdf
```

are not necessarily equivalent evidence.

---

<!-- source: Continue Architecture Planning.md L81971–82027 | turn 69 | version 0.28 -->
## v0.28 — 28.7 SearchWorkKey

Introduce a semantic work identity.

```JavaScript
class SearchWorkKey {
    constructor(data = {}) {
        this.kind = data.kind || 'unknown';

        this.target = data.target || null;

        this.partitionId = data.partitionId || null;

        this.enumeratorId = data.enumeratorId || null;

        this.cursor = data.cursor ?? null;

        this.strategyId = data.strategyId || null;
    }

    serialize() {
        return { ...this };
    }
}
```

The exact fields depend on work type.

For an enumeration page:

```
enumerator
+
target
+
snapshot
+
cursor
```

may define equivalent work.

For an exploratory probe:

```
partition
+
strategy
+
probe target
```

may be sufficient.

There should therefore be **no universal string key**.

---

<!-- source: Continue Architecture Planning.md L82029–82063 | turn 69 | version 0.28 -->
## v0.28 — 28.8 Work equivalence

Introduce:

```JavaScript
class WorkEquivalenceResolver {

    equivalent(a, b, context) {
        return {
            equivalent: false,
            reason: null,
            evidenceIds: []
        };
    }
}
```

Possible outcomes:

```
EQUIVALENT
OVERLAPPING
DISTINCT
UNKNOWN
```

This is more accurate than:

```JavaScript
if (keyA === keyB)
```

because semantic equivalence can require evidence.

---

<!-- source: Continue Architecture Planning.md L82065–82106 | turn 69 | version 0.28 -->
## v0.28 — 28.9 Candidate convergence

Candidate identity remains relatively simple:

```
Candidate
    = normalized type + canonical target
```

Multiple proposals converge:

```
Proposal A ──┐
Proposal B ──┼──→ Candidate X
Proposal C ──┘
```

But each proposal remains:

```
Proposal
 ├── source
 ├── observation
 ├── tactic
 ├── strategy
 ├── partition
 └── evidence
```

So:

```
Candidate count
    = 1

Discovery evidence count
    = 3
```

This is exactly what we want.

---

<!-- source: Continue Architecture Planning.md L82157–82197 | turn 69 | version 0.28 -->
## v0.28 — 28.11 Artifact convergence

Artifacts are different.

If:

```
SHA-256(A) == SHA-256(B)
```

then under the hash assumptions:

```
A and B have identical observed bytes
```

That allows artifact-level deduplication.

But not resource-level merging.

```
Resource A
   └── Artifact X

Resource B
   └── Artifact X
```

Two logical resources can legitimately reference the same artifact.

Examples include:

```
mirror URL
download alias
duplicate repository entry
CDN URL
localized page linking identical binary
```

---

<!-- source: Continue Architecture Planning.md L82199–82239 | turn 69 | version 0.28 -->
## v0.28 — 28.12 Discovery independence

Now an important epistemic issue.

Suppose:

```
HTML
  ↓
link
  ↓
sitemap
```

and the sitemap also contains the same URL.

These are not necessarily independent confirmations.

The provenance graph might reveal:

```
HTML observation
      ↓
sitemap URL discovered
      ↓
sitemap observation
      ↓
manual.pdf
```

The second path is causally dependent on the first.

Therefore:

```
two paths
    ≠
two independent confirmations
```

---

<!-- source: Continue Architecture Planning.md L82241–82281 | turn 69 | version 0.28 -->
## v0.28 — 28.13 Evidence independence model

Introduce:

```JavaScript
class EvidenceRelation {
    constructor(data = {}) {
        this.fromEvidenceId = data.fromEvidenceId || null;
        this.toEvidenceId = data.toEvidenceId || null;

        this.relation = data.relation || 'unknown';

        this.evidenceIds = data.evidenceIds || [];

        this.createdAt = data.createdAt || now();
    }
}
```

Relations:

```
supports
depends-on
derived-from
duplicates
contradicts
independent-of
```

Then:

```
Evidence A
    │
    └── derived-from → Evidence B
```

should not be counted as an independent confirmation.

---

<!-- source: Continue Architecture Planning.md L82283–82323 | turn 69 | version 0.28 -->
## v0.28 — 28.14 Coverage provenance

Coverage needs similar provenance.

A coverage statement should identify:

```
partition
enumerator
strategy
snapshot
execution
method
evidence
```

Example:

```JavaScript
{
    partitionId: 'partition-7',

    method: {
        enumeratorId: 'sitemap',
        version: '1.1'
    },

    executionId: 'exec-44',

    snapshotId: 'snapshot-3',

    evidenceIds: [
        'obs-100',
        'termination-44'
    ]
}
```

Now two coverage records can be compared.

---

<!-- source: Continue Architecture Planning.md L82325–82360 | turn 69 | version 0.28 -->
## v0.28 — 28.15 Coverage relation

Introduce:

```JavaScript
class CoverageRelation {
    constructor(data = {}) {
        this.id = data.id || makeId('covrel');

        this.fromCoverageId = data.fromCoverageId || null;
        this.toCoverageId = data.toCoverageId || null;

        this.relation = data.relation || 'unknown';

        this.overlapEstimate = data.overlapEstimate ?? null;

        this.evidenceIds = data.evidenceIds || [];

        this.createdAt = data.createdAt || now();
    }
}
```

Possible relations:

```
subset
overlaps
disjoint
equivalent
duplicates
independent
unknown
```

---

<!-- source: Continue Architecture Planning.md L82362–82389 | turn 69 | version 0.28 -->
## v0.28 — 28.16 Coverage union

Coverage aggregation should become an explicit operation.

```JavaScript
class CoverageResolver {

    combine(records, context) {
        return {
            status: 'unknown',
            explored: null,
            estimatedTotal: null,
            overlap: null,
            evidenceIds: []
        };
    }
}
```

Never:

```JavaScript
total += record.explored;
```

unless the records are known to be disjoint.

---

<!-- source: Continue Architecture Planning.md L82391–82425 | turn 69 | version 0.28 -->
## v0.28 — 28.17 Disjoint partitions

If we have evidence that:

```
/manuals/*
```

and:

```
/software/*
```

are disjoint under the domain definition, then:

```
Coverage(A ∪ B)
=
Coverage(A) + Coverage(B)
```

is valid for the relevant dimension.

But the disjointness itself needs a contract.

```
Partition relation
    ↓
disjoint
    ↓
coverage aggregation permitted
```

---

<!-- source: Continue Architecture Planning.md L82427–82460 | turn 69 | version 0.28 -->
## v0.28 — 28.18 Unknown overlap

The default should be:

```
UNKNOWN
```

not:

```
DISJOINT
```

This matters enormously.

If:

```
A = repository documents
B = sitemap documents
```

we often don't know their intersection beforehand.

So:

```
Unknown overlap
```

must prevent the system from making unjustified additive coverage claims.

---

<!-- source: Continue Architecture Planning.md L82462–82506 | turn 69 | version 0.28 -->
## v0.28 — 28.19 Frontier duplicate suppression

The FrontierRuntime can now ask:

```
"Do I already have equivalent unfinished work?"
```

rather than simply:

```
"Does this WorkItem ID already exist?"
```

Example:

```
Work A:
    sitemap
    page 10

Work B:
    sitemap
    page 10
```

If semantically equivalent:

```
B → SUPPRESSED_DUPLICATE
```

But:

```
Work A:
    sitemap

Work B:
    repository
```

should generally remain distinct.

---

<!-- source: Continue Architecture Planning.md L82508–82543 | turn 69 | version 0.28 -->
## v0.28 — 28.20 Duplicate suppression must preserve provenance

Suppose work B is suppressed.

We still record:

```
Work B
   ↓
duplicate-of
   ↓
Work A
```

This prevents loss of reasoning history.

```JavaScript
{
    workId: 'work-b',
    status: 'suppressed',
    relation: {
        kind: 'duplicate-of',
        targetWorkId: 'work-a'
    }
}
```

Thus:

```
execution reduction
    +
provenance preservation
```

---

<!-- source: Continue Architecture Planning.md L82545–82577 | turn 69 | version 0.28 -->
## v0.28 — 28.21 Convergence graph

We can now represent convergence explicitly:

```
                  Sitemap
                     │
                     ▼
Repository ──────→ Candidate X ←────── HTML
                     │
                     ▼
                  Resource X
                     │
               ┌─────┴─────┐
               ▼           ▼
          Artifact A   Artifact B
```

This is fundamentally different from a tree.

A crawler tends toward:

```
root
 ├── A
 │   └── X
 └── B
     └── X
```

The discovery engine should become a **graph convergence system**.

---

<!-- source: Continue Architecture Planning.md L82579–82605 | turn 69 | version 0.28 -->
## v0.28 — 28.22 Search-space graph

The search space itself is also a graph:

```
                Search Domain
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
      Partition A  Partition B  Partition C
          │           │
          └────overlap┘
```

Therefore the architecture now contains two related graphs:

```
SEARCH-SPACE GRAPH
"What regions have we explored?"

RESOURCE GRAPH
"What entities have we discovered?"
```

They must not be merged.

---

<!-- source: Continue Architecture Planning.md L82607–82640 | turn 69 | version 0.28 -->
## v0.28 — 28.23 Search-space coverage ledger

A useful aggregate structure:

```JavaScript
class CoverageLedger {
    constructor() {
        this.records = new Map();
        this.relations = new Map();
    }

    addRecord(record) {
        this.records.set(record.id, record);
    }

    addRelation(relation) {
        this.relations.set(relation.id, relation);
    }

    resolve(scope) {
        throw new Error('Not implemented');
    }
}
```

The ledger becomes the authority for coverage accounting.

Not:

```
candidate count
```

---

<!-- source: Continue Architecture Planning.md L82642–82693 | turn 69 | version 0.28 -->
## v0.28 — 28.24 Candidate count is not coverage

This deserves explicit treatment.

Suppose:

```
Strategy A → 100 candidates
Strategy B → 100 candidates
```

If both found the same 100:

```
unique candidates = 100
```

not 200.

But even:

```
unique candidates = 100
```

doesn't establish:

```
coverage = 100%
```

There could be:

```
10,000 undiscovered resources
```

outside the enumerated regions.

Therefore:

```
candidate count
    ≠
resource count
    ≠
coverage
    ≠
completeness
```

---

<!-- source: Continue Architecture Planning.md L82695–82697 | turn 69 | version 0.28 -->
## v0.28 — 28.25 Search-space deduplication vs candidate deduplication

These are opposite operations.

<!-- source: Continue Architecture Planning.md L82699–82705 | turn 69 | version 0.28 -->
### v0.28 — Candidate deduplication

```
Many observations
       ↓
one candidate
```

<!-- source: Continue Architecture Planning.md L82707–82734 | turn 69 | version 0.28 -->
### v0.28 — Search-space deduplication

```
Many planned searches
       ↓
one equivalent search operation
```

But search-space **overlap** should not necessarily be deduplicated.

Why?

Because different methods can provide independent evidence.

Therefore:

```
Equivalent work
    → suppress

Overlapping work
    → preserve unless cost/policy says otherwise

Independent evidence
    → always preserve
```

---

<!-- source: Continue Architecture Planning.md L82736–82786 | turn 69 | version 0.28 -->
## v0.28 — 28.26 Adaptive strategy interaction

v0.21's adaptive selector can now use overlap-aware metrics.

Previously:

```
strategy yield
```

might mean:

```
new candidates / request
```

Now we can distinguish:

```
raw candidates
unique candidates
novel resources
novel artifacts
novel partitions
independent confirmations
overlap rate
```

A strategy producing:

```
100 candidates
90 duplicates
```

should not be treated the same as:

```
100 candidates
90 novel resources
```

Therefore:

```
StrategyPerformance
    ↓
novelty-aware metrics
```

---

<!-- source: Continue Architecture Planning.md L82788–82839 | turn 69 | version 0.28 -->
## v0.28 — 28.27 Example

Suppose:

```
Sitemap:
    100 URLs

Repository:
    80 URLs

Intersection:
    70 URLs
```

Then:

```
unique URLs = 110
```

not:

```
180
```

But provenance contains:

```
100 sitemap observations
80 repository observations
```

And the 70 overlapping URLs may have two discovery paths.

So:

```
candidate universe
    = 110

discovery observations
    = 180

independent confirmation opportunities
    ≠ 180
```

This is the right accounting model.

---

<!-- source: Continue Architecture Planning.md L82841–82883 | turn 69 | version 0.28 -->
## v0.28 — 28.28 Reconciliation algorithm

A conceptual reconciliation pass:

```
NEW PROPOSAL
     ↓
Normalize
     ↓
Candidate identity
     ↓
Existing candidate?
   /       \
 no         yes
 |           |
create      merge provenance
             |
             ▼
        identity resolution
             |
             ▼
        resource graph
```

For coverage:

```
NEW COVERAGE RECORD
        ↓
identify scope
        ↓
compare partitions
        ↓
resolve overlap
        ↓
compare enumeration snapshots
        ↓
aggregate only justified regions
        ↓
CoverageClaim
```

---

<!-- source: Continue Architecture Planning.md L82885–82922 | turn 69 | version 0.28 -->
## v0.28 — 28.29 Reconciliation must be monotonic

A dangerous design would allow:

```
coverage = 90%
```

then later:

```
coverage = 70%
```

without explaining why.

Instead, a new assessment should produce a new claim:

```
CoverageClaim v1
    90%
    
CoverageClaim v2
    70%
    reason = revised-universe-definition
```

Historical claims remain immutable.

This follows the same pattern as:

```
classification history
revision history
completeness claims
```

---

<!-- source: Continue Architecture Planning.md L82924–82946 | turn 69 | version 0.28 -->
## v0.28 — 28.30 Reconciliation does not delete evidence

Never:

```JavaScript
delete duplicateEvidence;
```

Instead:

```
Evidence B
   ↓
duplicate-of
   ↓
Evidence A
```

This is especially important for auditability.

Deduplication is a **graph relation**, not destructive garbage collection.

---

<!-- source: Continue Architecture Planning.md L83130–83165 | turn 69 | version 0.28 -->
## v0.28 — 28.34 The deeper architectural result

The system has crossed another important threshold.

It is no longer simply:

```
discovery → deduplication
```

It is becoming:

```
                     SEARCH
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
       WORK          SPACE        EVIDENCE
        GRAPH         GRAPH         GRAPH
          │            │            │
          └────────────┼────────────┘
                       ▼
                 RECONCILIATION
                       │
             ┌─────────┼─────────┐
             ▼         ▼         ▼
          frontier   identity   coverage
```

This gives us a useful general principle:

> **The engine should deduplicate execution, converge identity, and reconcile coverage — but it should never deduplicate away the evidence that made those operations possible.**

That is the distinction that prevents a discovery engine from becoming a black-box crawler with a misleading `seen[]` set.

---

<!-- source: Continue Architecture Planning.md L83238–83284 | turn 71 | version 0.29 -->
## v0.29 — Dynamic Search-Space Expansion

v0.28 solved **reconciliation**:

```
many discovery paths
        ↓
reconcile work / identity / coverage
```

The next problem is the opposite:

> **What happens when discovery reveals a search region that did not exist when the scan started?**

For example:

```
HTML
 ↓
/sitemap.xml
 ↓
new enumeration region
```

or:

```
Repository index
 ↓
/archive/2024/
 ↓
new partition
```

or:

```
Document
 ↓
references "firmware v3 manuals"
 ↓
new document-family region
```

We therefore need a controlled mechanism for turning **discovered structure into new search-space partitions**.

---

<!-- source: Continue Architecture Planning.md L83286–83322 | turn 71 | version 0.29 -->
## v0.29 — 29.1 The central distinction

A discovery result may suggest:

```
"there is probably another region worth searching"
```

That is not yet:

```
"create and execute 500 new search tasks"
```

So the pipeline becomes:

```
Discovery
   ↓
PartitionProposal
   ↓
Validation
   ↓
Admission
   ↓
SearchPartition
   ↓
Frontier Work
```

The new object is:

```
PartitionProposal
```

---

<!-- source: Continue Architecture Planning.md L83324–83376 | turn 71 | version 0.29 -->
## v0.29 — 29.2 PartitionProposal

```JavaScript
class PartitionProposal {
    constructor(data = {}) {
        this.id = data.id || makeId('pprop');

        this.domainId = data.domainId || null;
        this.sessionId = data.sessionId || null;

        this.parentPartitionId = data.parentPartitionId || null;

        this.kind = data.kind || 'unknown';
        this.selector = data.selector || null;

        this.reason = data.reason || null;

        this.evidenceIds = data.evidenceIds || [];

        this.confidence = Number.isFinite(data.confidence)
            ? data.confidence
            : 0;

        this.status = data.status || 'proposed';

        this.createdAt = data.createdAt || now();
    }

    serialize() {
        return { ...this };
    }
}
```

Example:

```JavaScript
{
    kind: 'origin',
    selector: {
        origin: 'https://docs.example.org'
    },

    reason: {
        kind: 'discovered-origin',
        source: 'html-link'
    },

    evidenceIds: ['ev-882']
}
```

---

<!-- source: Continue Architecture Planning.md L83378–83410 | turn 71 | version 0.29 -->
## v0.29 — 29.3 Why proposals are necessary

Without a proposal layer:

```
Discovery
   ↓
create partition
```

becomes dangerous.

A malicious or malformed document could contain:

```
10,000 unique domains
```

and immediately generate:

```
10,000 partitions
```

That is effectively an uncontrolled search-space expansion attack.

Therefore:

```
discovery ≠ partition authority
```

---

<!-- source: Continue Architecture Planning.md L83412–83460 | turn 71 | version 0.29 -->
## v0.29 — 29.4 PartitionAdmissionController

Introduce:

```JavaScript
class PartitionAdmissionController {

    evaluate(proposal, context) {
        return {
            allowed: false,
            reason: 'not-implemented'
        };
    }
}
```

It checks:

```
Domain
Policy
Budget
Depth
Existing partitions
Overlap
Evidence
Goal relevance
Expansion rate
```

Pipeline:

```
PartitionProposal
       ↓
Domain validation
       ↓
Policy validation
       ↓
Deduplication
       ↓
Overlap analysis
       ↓
Budget check
       ↓
Admission
```

---

<!-- source: Continue Architecture Planning.md L83462–83522 | turn 71 | version 0.29 -->
## v0.29 — 29.5 Partition identity

A partition needs a canonical identity.

But unlike a URL, partition identity is semantic.

For example:

```
origin = example.org
```

and:

```
origin = https://example.org
```

may represent the same partition.

Similarly:

```
/manuals/*
```

and:

```
/manuals/
```

may or may not mean the same thing depending on partition semantics.

Therefore introduce:

```JavaScript
class PartitionIdentityResolver {

    resolve(proposal, context) {
        return {
            identity: null,
            matches: [],
            relation: 'unknown'
        };
    }
}
```

Possible results:

```
same
subset
superset
overlap
disjoint
unknown
```

---

<!-- source: Continue Architecture Planning.md L83524–83550 | turn 71 | version 0.29 -->
## v0.29 — 29.6 Partition explosion

This is the major v0.29 failure mode.

Suppose:

```
1 page
 ↓
100 links
 ↓
100 new partitions
 ↓
10,000 partitions
 ↓
1,000,000 partitions
```

The search engine becomes dominated by its own planning activity.

Therefore we need:

```
Expansion Budget
```

---

<!-- source: Continue Architecture Planning.md L83552–83581 | turn 71 | version 0.29 -->
## v0.29 — 29.7 ExpansionBudget

```JavaScript
class ExpansionBudget {
    constructor(data = {}) {
        this.maxProposals = data.maxProposals ?? 1000;
        this.maxAdmissions = data.maxAdmissions ?? 500;
        this.maxDepth = data.maxDepth ?? 5;
        this.maxChildrenPerPartition =
            data.maxChildrenPerPartition ?? 25;

        this.proposals = 0;
        this.admissions = 0;
    }

    canPropose() {
        return this.proposals < this.maxProposals;
    }

    canAdmit() {
        return this.admissions < this.maxAdmissions;
    }
}
```

But a global count is not enough.

We also need local limits.

---

<!-- source: Continue Architecture Planning.md L83583–83606 | turn 71 | version 0.29 -->
## v0.29 — 29.8 Local expansion rate

A partition should have a child-generation budget:

```
Partition A
 ├── child 1
 ├── child 2
 ├── child 3
 └── ...
```

Example:

```JavaScript
{
    maxChildren: 25,
    maxExpansionDepth: 3
}
```

This prevents one highly connected partition from monopolizing the entire search.

---

<!-- source: Continue Architecture Planning.md L83608–83640 | turn 71 | version 0.29 -->
## v0.29 — 29.9 Expansion rate limiting

A useful metric:

```
expansionRate =
    admittedPartitions /
    triggeringObservations
```

A partition that repeatedly generates enormous numbers of children should be penalized.

But:

```
high expansion
    ≠
bad discovery
```

A legitimate repository may genuinely contain many subspaces.

So expansion rate should be used for:

```
prioritization
throttling
budget allocation
```

not as a correctness judgment.

---

<!-- source: Continue Architecture Planning.md L83642–83670 | turn 71 | version 0.29 -->
## v0.29 — 29.10 Evidence threshold

A partition proposal should normally identify why the region exists.

Strong:

```
Observed:
    sitemap index references sitemap-2026.xml
```

Weak:

```
LLM guessed:
    maybe /manuals/2026/
```

Therefore:

```
Observed structural reference
    >
inferred path
```

The latter can still be a hypothesis, but must remain explicitly labeled.

---

<!-- source: Continue Architecture Planning.md L83672–83693 | turn 71 | version 0.29 -->
## v0.29 — 29.11 Partition proposal epistemic status

Use:

```
PROPOSED
SUPPORTED
REJECTED
UNKNOWN
```

This fits the user's preferred epistemic separation.

A proposal is not a fact.

```
PartitionProposal
    ≠
SearchPartition
```

---

<!-- source: Continue Architecture Planning.md L83695–83726 | turn 71 | version 0.29 -->
## v0.29 — 29.12 Hypothesis connection

v0.25 introduced:

```
SearchHypothesis
```

Dynamic expansion can use it.

Example:

```
SearchHypothesis
    "There may be a 2025 archive"
          ↓
PartitionProposal
          ↓
Validation
```

But:

```
Hypothesis
    ≠
Partition
```

The hypothesis may be rejected.

---

<!-- source: Continue Architecture Planning.md L83728–83779 | turn 71 | version 0.29 -->
## v0.29 — 29.13 Partition generation sources

Potential generators:

```
HTML
 ├── discovered origin
 ├── path family
 └── repository reference

Sitemap
 ├── sitemap index
 └── child sitemap

Repository
 ├── subrepository
 ├── branch
 └── archive

Document
 ├── revision family
 ├── language family
 └── referenced document family

API
 ├── related endpoint
 └── pagination namespace
```

These should be implemented as **PartitionExpansionProviders**.

```JavaScript
class PartitionExpansionProvider {

    canExpand(evidence, context) {
        return false;
    }

    expand(evidence, context) {
        return [];
    }

    describe() {
        return {
            id: 'unknown-expander',
            name: 'Unknown Partition Expansion Provider'
        };
    }
}
```

---

<!-- source: Continue Architecture Planning.md L83781–83812 | turn 71 | version 0.29 -->
## v0.29 — 29.14 Expansion provider boundary

The provider only proposes:

```
Evidence
   ↓
PartitionProposal[]
```

It does not:

```
create partitions
schedule work
acquire resources
change policy
```

Therefore:

```
Provider
   ↓
proposal
   ↓
AdmissionController
```

remains the authority boundary.

---

<!-- source: Continue Architecture Planning.md L83814–83843 | turn 71 | version 0.29 -->
## v0.29 — 29.15 Dynamic search-space graph

The search-space graph is now dynamic:

```
                 Domain
                   │
                   ▼
             Partition A
              /       \
             /         \
            ▼           ▼
     Partition B     Partition C
          │               │
          ▼               ▼
     Partition D      Partition E
```

New partitions appear as evidence arrives.

But the graph must remain:

```
versioned
auditable
bounded
reconcilable
```

---

<!-- source: Continue Architecture Planning.md L83845–83889 | turn 71 | version 0.29 -->
## v0.29 — 29.16 Partition generation event

Every expansion should create an event.

```JavaScript
{
    type: 'partition-proposed',

    proposalId: 'pprop-44',

    parentPartitionId: 'partition-8',

    reason: {
        kind: 'sitemap-reference'
    },

    evidenceIds: [
        'ev-991'
    ]
}
```

Then:

```
partition-proposed
        ↓
partition-validated
        ↓
partition-admitted
        ↓
partition-created
        ↓
work-created
```

Or:

```
partition-rejected
```

with an explicit reason.

---

<!-- source: Continue Architecture Planning.md L83891–83922 | turn 71 | version 0.29 -->
## v0.29 — 29.17 Search-space versioning

Dynamic expansion creates another issue.

At time T1:

```
SearchSpace v1
    A
    B
```

At T2:

```
SearchSpace v2
    A
    B
    C
```

Historical coverage under v1 must remain valid.

Therefore:

```
SearchSpaceSnapshot
```

should identify the state of the search universe.

---

<!-- source: Continue Architecture Planning.md L83924–83960 | turn 71 | version 0.29 -->
## v0.29 — 29.18 SearchSpaceSnapshot

```JavaScript
class SearchSpaceSnapshot {
    constructor(data = {}) {
        this.id = data.id || makeId('space-snapshot');

        this.spaceId = data.spaceId || null;

        this.partitionIds = data.partitionIds || [];

        this.parentSnapshotId = data.parentSnapshotId || null;

        this.version = data.version ?? 1;

        this.fingerprint = data.fingerprint || null;

        this.createdAt = data.createdAt || now();
    }

    serialize() {
        return { ...this };
    }
}
```

Now:

```
CoverageClaim
    ↓
SearchSpaceSnapshot
```

makes the scope explicit.

---

<!-- source: Continue Architecture Planning.md L83962–84007 | turn 71 | version 0.29 -->
## v0.29 — 29.19 Expansion and completeness

A critical consequence:

```
SearchSpace expands
```

after a previous completeness assessment.

That does **not** mean the old claim was necessarily false.

Example:

```
10:00
SearchSpace = A
Completeness(A) = supported

10:05
Evidence reveals B

SearchSpace = A ∪ B
```

The 10:00 claim was relative to the then-known search space.

It does not automatically become:

```
"false"
```

Instead:

```
old claim
    scope = snapshot 1

new claim
    scope = snapshot 2
```

This preserves temporal epistemic correctness.

---

<!-- source: Continue Architecture Planning.md L84009–84053 | turn 71 | version 0.29 -->
## v0.29 — 29.20 Dynamic expansion and negative evidence

Similarly, absence claims must be scoped.

Suppose:

```
Complete enumeration of A
```

establishes:

```
X absent from A
```

Later:

```
B discovered
```

and:

```
X exists in B
```

There is no contradiction.

The original statement was:

```
X ∉ A
```

not:

```
X does not exist anywhere.
```

This demonstrates why scoped predicates matter.

---

<!-- source: Continue Architecture Planning.md L84055–84083 | turn 71 | version 0.29 -->
## v0.29 — 29.21 Expansion priorities

Not all new partitions deserve equal priority.

Possible score:

```
ExpansionPriority =
    evidenceStrength
  + goalRelevance
  + expectedNovelty
  + parentPriority
  - estimatedCost
  - overlapPenalty
  - expansionRisk
```

Again, this is a scheduling heuristic.

It cannot override:

```
domain
policy
capability
budget
```

---

<!-- source: Continue Architecture Planning.md L84085–84120 | turn 71 | version 0.29 -->
## v0.29 — 29.22 Expansion depth

The parent-child relationship gives us a natural expansion depth:

```
Domain
  ↓ depth 0
Partition A
  ↓ depth 1
Partition B
  ↓ depth 2
Partition C
```

The domain can establish:

```JavaScript
maxPartitionDepth: 5
```

A proposal at depth 6 is rejected or deferred.

This is different from resource discovery depth.

We now have:

```
candidateDepth
partitionDepth
tacticDepth
queryExpansionDepth
```

These must not be conflated.

---

<!-- source: Continue Architecture Planning.md L84122–84165 | turn 71 | version 0.29 -->
## v0.29 — 29.23 Expansion loops

Dynamic expansion creates cycles.

Example:

```
A → B
B → C
C → A
```

The search-space graph is therefore not necessarily a tree.

Use identity resolution:

```
new proposal
    ↓
existing partition?
    ↓
relation:
    same / overlap / subset / ...
```

If:

```
same partition
```

then:

```
do not create another partition
```

Instead add:

```
new evidence/provenance
```

---

<!-- source: Continue Architecture Planning.md L84167–84195 | turn 71 | version 0.29 -->
## v0.29 — 29.24 Expansion cycle ≠ failure

A cycle:

```
A → B → A
```

is not necessarily a system failure.

It may simply indicate:

```
two discovery paths converge
```

The correct response is:

```
identity reconciliation
```

not:

```
delete branch
```

---

<!-- source: Continue Architecture Planning.md L84197–84230 | turn 71 | version 0.29 -->
## v0.29 — 29.25 Partition admission states

```
PROPOSED
   ↓
VALIDATING
   ↓
   ├── REJECTED
   │
   └── ADMITTED
          ↓
       CREATED
          ↓
       READY
```

Additional states:

```
DUPLICATE
OVERLAPPING
DEFERRED
BUDGET_BLOCKED
POLICY_BLOCKED
OUTSIDE_DOMAIN
```

`DUPLICATE` is not the same as `REJECTED`.

The former means:

> the information was already represented.

---

<!-- source: Continue Architecture Planning.md L84232–84262 | turn 71 | version 0.29 -->
## v0.29 — 29.26 Partition proposal accounting

Track:

```JavaScript
{
    proposed: 100,
    validated: 82,
    admitted: 60,
    duplicates: 12,
    overlaps: 7,
    rejected: 8,
    budgetBlocked: 5,
    policyBlocked: 1,
    outsideDomain: 7
}
```

This tells us whether the discovery system is:

```
finding useful structure
```

or:

```
mostly generating redundant search regions
```

---

<!-- source: Continue Architecture Planning.md L84264–84289 | turn 71 | version 0.29 -->
## v0.29 — 29.27 Partition explosion protection

A robust runtime should use several independent controls:

```
Global
 ├── max partition proposals
 ├── max admitted partitions
 └── max total expansion cost

Per session
 ├── expansion rate
 └── expansion depth

Per partition
 ├── max children
 └── max child cost

Per provider
 ├── proposal quota
 └── admission quota
```

No single limit should be trusted as the only protection.

---

<!-- source: Continue Architecture Planning.md L84291–84337 | turn 71 | version 0.29 -->
## v0.29 — 29.28 Admission algorithm

Conceptually:

```
PartitionProposal
       │
       ▼
Is domain valid?
       │
    no ─────→ OUTSIDE_DOMAIN
       │
      yes
       ▼
Evidence sufficient?
       │
    no ─────→ DEFER / REJECT
       │
      yes
       ▼
Already represented?
       │
    yes ─────→ DUPLICATE / RELATION
       │
      no
       ▼
Overlap known?
       │
       ├── yes → record relation
       │
       ▼
Budget available?
       │
    no ─────→ BUDGET_BLOCKED
       │
      yes
       ▼
ADMIT
       │
       ▼
CREATE PARTITION
       │
       ▼
CREATE FRONTIER WORK
```

---

<!-- source: Continue Architecture Planning.md L84339–84367 | turn 71 | version 0.29 -->
## v0.29 — 29.29 Frontier generation

Once admitted:

```
SearchPartition
      ↓
Partition exploration work
      ↓
FrontierRuntime
```

The partition itself should not automatically execute.

This preserves:

```
Partition existence
    ≠
Partition authorization
    ≠
Partition scheduling
    ≠
Partition execution
```

Exactly the same separation established earlier for candidates.

---

<!-- source: Continue Architecture Planning.md L84401–84437 | turn 71 | version 0.29 -->
## v0.29 — 29.31 Two expansion paths

The engine now has:

```
OBSERVATION
    │
    ├── expands RESOURCE KNOWLEDGE
    │       ↓
    │    Candidate
    │       ↓
    │    Resource
    │
    └── expands SEARCH KNOWLEDGE
            ↓
        PartitionProposal
            ↓
        SearchPartition
```

That distinction is fundamental.

A discovered URL may mean:

```
"Here is another resource."
```

while a discovered sitemap may mean:

```
"Here is another mechanism for discovering resources."
```

The latter expands the **search space itself**.

---

<!-- source: Continue Architecture Planning.md L84439–84463 | turn 71 | version 0.29 -->
## v0.29 — 29.32 Search-space discovery as first-class knowledge

We can now model:

```
Knowledge
├── Resource knowledge
│   ├── candidates
│   ├── resources
│   ├── representations
│   └── artifacts
│
└── Search knowledge
    ├── partitions
    ├── enumerators
    ├── strategies
    ├── coverage
    └── completeness
```

This is an important evolution.

The engine is discovering not just **things**, but also **ways of finding things**.

---

<!-- source: Continue Architecture Planning.md L84545–84576 | turn 71 | version 0.29 -->
## v0.29 — 29.34 The system after v0.29

We now have three dynamic graphs:

```
                    DISCOVERY ENGINE
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
   WORK GRAPH        SEARCH-SPACE GRAPH   RESOURCE GRAPH
        │                  │                  │
        │                  │                  │
    scheduling         partitions          resources
    leases             overlap             locators
    retries            coverage            artifacts
    checkpoints        completeness        revisions
```

And evidence connects them:

```
                       EVIDENCE GRAPH
                       /      |       \
                      /       |        \
                     ▼        ▼         ▼
                 Work      Search     Resource
```

This is becoming a much more general architecture than a crawler.

---

<!-- source: Continue Architecture Planning.md L84610–84662 | turn 71 | version 0.29 -->
## v0.29 takeaway

The discovery engine can now grow its own search space, but only through a controlled path:

```
Observation
    ↓
Evidence
    ↓
PartitionProposal
    ↓
Validation
    ↓
Reconciliation
    ↓
Budget / Policy
    ↓
PartitionAdmission
    ↓
SearchPartition
    ↓
Frontier Work
```

This closes the major gap between:

```
"we discovered a new discovery mechanism"
```

and:

```
"the engine should now explore it."
```

The next problem is the **control problem created by all these dynamically generated partitions**.

At this point, the frontier can contain:

```
resource work
discovery work
enumeration work
partition-expansion work
classification work
relevance work
verification work
```

They compete for the same finite budgets.

So the next natural boundary is:
