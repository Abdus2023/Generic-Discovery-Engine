# Strategies, Query Planning and Enumeration

> **Status:** DESIGNED
>
> **Source:** `Continue Architecture Planning.md`; `Userscript Discovery Prototype.md`
>
> **Purpose:** Discovery strategies, adaptive strategy selection, query planning, tactic execution and enumeration.

## Source Sections

- **33. Discovery strategies should also be pluggable** — `USP-056` — `Userscript Discovery Prototype.md` L1586–1614
- **v0.17 — 27. Querying the graph** — `CAP-399` — `Continue Architecture Planning.md` L66325–66327
- **v0.21 — Discovery Strategy Learning / Adaptive Search** — `CAP-558` — `Continue Architecture Planning.md` L71131–71200
- **v0.21 — Adaptive Discovery Strategy** — `CAP-560` — `Continue Architecture Planning.md` L71212–71240
- **v0.21 — 21.1 The Adaptive Loop** — `CAP-561` — `Continue Architecture Planning.md` L71242–71291
- **v0.21 — 21.2 Strategy Performance Record** — `CAP-562` — `Continue Architecture Planning.md` L71293–71345
- **v0.21 — 21.3 Yield Metrics** — `CAP-563` — `Continue Architecture Planning.md` L71347–71385
- **v0.21 — 21.4 Strategy Score** — `CAP-564` — `Continue Architecture Planning.md` L71387–71432
- **v0.21 — 21.5 Cold Start Problem** — `CAP-565` — `Continue Architecture Planning.md` L71434–71486
- **v0.21 — 21.6 Exploration Quota** — `CAP-566` — `Continue Architecture Planning.md` L71488–71521
- **v0.21 — 21.7 Strategy Selection Must Be Constrained** — `CAP-567` — `Continue Architecture Planning.md` L71523–71570
- **v0.21 — 21.8 Strategy Eligibility** — `CAP-568` — `Continue Architecture Planning.md` L71572–71610
- **v0.21 — 21.9 Temporary vs Permanent Failure** — `CAP-569` — `Continue Architecture Planning.md` L71612–71664
- **v0.21 — 21.10 Strategy Outcome** — `CAP-570` — `Continue Architecture Planning.md` L71666–71711
- **v0.21 — 21.11 Strategy Outcome ≠ Strategy Truth** — `CAP-571` — `Continue Architecture Planning.md` L71713–71752
- **v0.21 — 21.12 Novelty** — `CAP-572` — `Continue Architecture Planning.md` L71754–71787
- **v0.21 — 21.13 Frontier Expansion Value** — `CAP-573` — `Continue Architecture Planning.md` L71789–71826
- **v0.21 — 21.14 Frontier Expansion Metric** — `CAP-574` — `Continue Architecture Planning.md` L71828–71853
- **v0.21 — 21.15 Strategy Memory** — `CAP-575` — `Continue Architecture Planning.md` L71855–71901
- **v0.21 — 21.16 Hierarchical Priors** — `CAP-576` — `Continue Architecture Planning.md` L71903–71955
- **v0.21 — 21.17 Discovery Strategy Ledger** — `CAP-577` — `Continue Architecture Planning.md` L71957–71992
- **v0.21 — 21.18 Deterministic Replay** — `CAP-578` — `Continue Architecture Planning.md` L71994–72028
- **v0.21 — 21.19 Random Exploration** — `CAP-579` — `Continue Architecture Planning.md` L72030–72059
- **v0.21 — 21.20 Learning Must Not Modify Safety Boundaries** — `CAP-580` — `Continue Architecture Planning.md` L72061–72108
- **v0.21 — 21.21 Adaptive Discovery Controller** — `CAP-581` — `Continue Architecture Planning.md` L72110–72216
- **v0.21 — 21.22 Tie-Breaking Must Be Deterministic** — `CAP-582` — `Continue Architecture Planning.md` L72218–72249
- **v0.21 — 21.23 Performance Decay** — `CAP-583` — `Continue Architecture Planning.md` L72251–72277
- **v0.21 — 21.24 Strategy Adaptation and Scan Sessions** — `CAP-584` — `Continue Architecture Planning.md` L72279–72325
- **v0.21 — 21.25 Search Strategy as a First-Class Graph Node** — `CAP-585` — `Continue Architecture Planning.md` L72327–72362
- **v0.21 — 21.26 Search Decision Graph** — `CAP-586` — `Continue Architecture Planning.md` L72364–72400
- **v0.21 — 21.27 Two Kinds of Provenance** — `CAP-587` — `Continue Architecture Planning.md` L72402–72428
- **v0.26 — Search Tactic Runtime** — `CAP-762` — `Continue Architecture Planning.md` L78548–78586
- **v0.26 — Search Tactic Runtime** — `CAP-764` — `Continue Architecture Planning.md` L78598–78628
- **v0.26 — 26.1 The architectural gap** — `CAP-765` — `Continue Architecture Planning.md` L78630–78673
- **v0.26 — 26.2 QueryStep ≠ TacticExecution** — `CAP-766` — `Continue Architecture Planning.md` L78675–78713
- **v0.26 — 26.3 TacticExecution** — `CAP-767` — `Continue Architecture Planning.md` L78715–78766
- **v0.26 — 26.4 TacticRuntime** — `CAP-768` — `Continue Architecture Planning.md` L78768–78810
- **v0.26 — 26.5 TacticRuntime responsibilities** — `CAP-769` — `Continue Architecture Planning.md` L78812–78861
- **v0.26 — 26.6 Tactic contract** — `CAP-770` — `Continue Architecture Planning.md` L78863–78920
- **v0.26 — 26.7 Capability surface** — `CAP-771` — `Continue Architecture Planning.md` L78922–78962
- **v0.26 — 26.8 Bounded execution** — `CAP-772` — `Continue Architecture Planning.md` L78964–79006
- **v0.26 — 26.9 Batch execution** — `CAP-773` — `Continue Architecture Planning.md` L79008–79074
- **v0.26 — 26.10 Cursor** — `CAP-774` — `Continue Architecture Planning.md` L79076–79123
- **v0.26 — 26.11 Checkpoint** — `CAP-775` — `Continue Architecture Planning.md` L79125–79165
- **v0.26 — 26.12 Checkpoint atomicity** — `CAP-776` — `Continue Architecture Planning.md` L79167–79219
- **v0.26 — 26.13 Tactic dependencies** — `CAP-777` — `Continue Architecture Planning.md` L79221–79272
- **v0.26 — 26.14 Tactic lifecycle** — `CAP-778` — `Continue Architecture Planning.md` L79274–79315
- **v0.26 — 26.15 Exhaustion vs completion** — `CAP-779` — `Continue Architecture Planning.md` L79317–79372
- **v0.26 — 26.16 Tactic result** — `CAP-780` — `Continue Architecture Planning.md` L79374–79424
- **v0.26 — 26.17 Tactic does not create candidates directly** — `CAP-781` — `Continue Architecture Planning.md` L79426–79465
- **v0.26 — 26.18 Tactic → Strategy relationship** — `CAP-782` — `Continue Architecture Planning.md` L79467–79521
- **v0.26 — 26.19 Tactic provenance** — `CAP-783` — `Continue Architecture Planning.md` L79523–79580
- **v0.26 — Planning failures** — `CAP-785` — `Continue Architecture Planning.md` L79586–79593
- **v0.26 — Runtime failures** — `CAP-786` — `Continue Architecture Planning.md` L79595–79605
- **v0.26 — Strategy failures** — `CAP-787` — `Continue Architecture Planning.md` L79607–79614
- **v0.26 — Search failures** — `CAP-788` — `Continue Architecture Planning.md` L79616–79624
- **v0.26 — Recovery failures** — `CAP-789` — `Continue Architecture Planning.md` L79626–79649
- **v0.26 — 26.21 Retry semantics** — `CAP-790` — `Continue Architecture Planning.md` L79651–79700
- **v0.26 — 26.22 Cancellation** — `CAP-791` — `Continue Architecture Planning.md` L79702–79735
- **v0.26 — 26.23 Shared Frontier interaction** — `CAP-792` — `Continue Architecture Planning.md` L79737–79782
- **v0.26 — 26.25 Accounting** — `CAP-794` — `Continue Architecture Planning.md` L79854–79892
- **v0.26 — 26.28 New state model** — `CAP-797` — `Continue Architecture Planning.md` L79966–80013
- **v0.27 — Enumeration Runtime** — `CAP-814` — `Continue Architecture Planning.md` L80210–80255
- **v0.27 — 27.1 The central distinction** — `CAP-815` — `Continue Architecture Planning.md` L80257–80301
- **v0.27 — 27.2 Enumeration as a contract** — `CAP-816` — `Continue Architecture Planning.md` L80303–80333
- **v0.27 — 27.3 Enumerator interface** — `CAP-817` — `Continue Architecture Planning.md` L80335–80377
- **v0.27 — 27.4 EnumerationPage** — `CAP-818` — `Continue Architecture Planning.md` L80379–80423
- **v0.27 — 27.5 `hasMore` is not always trustworthy** — `CAP-819` — `Continue Architecture Planning.md` L80425–80475
- **v0.27 — 27.6 Enumeration state machine** — `CAP-820` — `Continue Architecture Planning.md` L80477–80515
- **v0.27 — 27.7 EnumerationRuntime** — `CAP-821` — `Continue Architecture Planning.md` L80517–80563
- **v0.27 — 27.8 Why this should not be inside DiscoveryStrategy** — `CAP-822` — `Continue Architecture Planning.md` L80565–80594
- **v0.27 — 27.9 Enumerator examples** — `CAP-823` — `Continue Architecture Planning.md` L80596–80596
- **v0.27 — Sitemap** — `CAP-824` — `Continue Architecture Planning.md` L80598–80606
- **v0.27 — API** — `CAP-825` — `Continue Architecture Planning.md` L80608–80618
- **v0.27 — Repository** — `CAP-826` — `Continue Architecture Planning.md` L80620–80630
- **v0.27 — Manifest** — `CAP-827` — `Continue Architecture Planning.md` L80632–80644
- **v0.27 — 27.10 EnumerationEntry** — `CAP-828` — `Continue Architecture Planning.md` L80646–80688
- **v0.27 — 27.11 Entry identity** — `CAP-829` — `Continue Architecture Planning.md` L80690–80728
- **v0.27 — 27.12 Enumeration cursor** — `CAP-830` — `Continue Architecture Planning.md` L80730–80732
- **v0.27 — Offset** — `CAP-831` — `Continue Architecture Planning.md` L80734–80741
- **v0.27 — Page** — `CAP-832` — `Continue Architecture Planning.md` L80743–80750
- **v0.27 — Token** — `CAP-833` — `Continue Architecture Planning.md` L80752–80759
- **v0.27 — Locator** — `CAP-834` — `Continue Architecture Planning.md` L80761–80768
- **v0.27 — Composite** — `CAP-835` — `Continue Architecture Planning.md` L80770–80786
- **v0.27 — 27.13 Cursor validity** — `CAP-836` — `Continue Architecture Planning.md` L80788–80835
- **v0.27 — 27.14 Enumeration snapshot** — `CAP-837` — `Continue Architecture Planning.md` L80837–80868
- **v0.27 — 27.15 Why snapshot identity matters** — `CAP-838` — `Continue Architecture Planning.md` L80870–80895
- **v0.27 — 27.16 Cardinality** — `CAP-839` — `Continue Architecture Planning.md` L80897–80932
- **v0.27 — 27.17 Ordering semantics** — `CAP-840` — `Continue Architecture Planning.md` L80934–80974
- **v0.27 — 27.18 Enumeration consistency** — `CAP-841` — `Continue Architecture Planning.md` L80976–81012
- **v0.27 — 27.19 Completeness assessment** — `CAP-842` — `Continue Architecture Planning.md` L81014–81053
- **v0.27 — 27.20 The crucial three-level distinction** — `CAP-843` — `Continue Architecture Planning.md` L81055–81088
- **v0.27 — 27.21 Example: sitemap** — `CAP-844` — `Continue Architecture Planning.md` L81090–81135
- **v0.27 — 27.22 Enumeration → Coverage** — `CAP-845` — `Continue Architecture Planning.md` L81137–81179
- **v0.27 — 27.23 Enumeration and negative evidence** — `CAP-846` — `Continue Architecture Planning.md` L81181–81237
- **v0.27 — 27.24 Enumeration budget** — `CAP-847` — `Continue Architecture Planning.md` L81239–81278
- **v0.27 — 27.25 Enumeration termination states** — `CAP-848` — `Continue Architecture Planning.md` L81280–81314
- **v0.27 — 27.26 Enumeration accounting** — `CAP-849` — `Continue Architecture Planning.md` L81316–81348
- **v0.27 — 27.27 Enumeration provenance** — `CAP-850` — `Continue Architecture Planning.md` L81350–81397
- **v0.27 — 27.28 Enumeration replay** — `CAP-851` — `Continue Architecture Planning.md` L81399–81425
- **v0.27 takeaway** — `CAP-867` — `Continue Architecture Planning.md` L81608–81646

## Related Documents

- [Search Space](search-space.md)
- [Goal-Constrained Discovery and Query Planning](goal-and-query.md)
- [Resource Type System and Classification](classification.md)
- [Candidate Sources](../providers/candidate-sources.md)

---

<!-- USP-056 | Userscript Discovery Prototype.md L1586–1614 | turn 11 | version ? -->
## 33. Discovery strategies should also be pluggable

> **Source sections:** `USP-056`

The acquisition side is only half the abstraction.

You can have:

```
CandidateStrategy
    ├── ExhaustiveGrid
    ├── EnergyPeakSearch
    ├── NetworkGuided
    ├── Historical
    └── Hybrid
```

A hybrid strategy is probably the most useful:

```
                Candidate Scheduler
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
    NIT-derived    historical       blind
      60%            20%             20%
```

The exact proportions shouldn't be hard-coded; the scheduler should dynamically adjust priority.

---

<!-- CAP-399 | Continue Architecture Planning.md L66325–66327 | turn 47 | version 0.17 -->
## v0.17 — 27. Querying the graph

> **Source sections:** `CAP-399`

The first useful queries become possible.

<!-- CAP-558 | Continue Architecture Planning.md L71131–71200 | turn 53 | version 0.21 -->
## v0.21 — Discovery Strategy Learning / Adaptive Search

> **Source sections:** `CAP-558`

The next boundary now becomes clear.

Once the engine records:

```
partition
strategy
probe
cost
discoveries
resources
classification
outcome
```

it has enough information to ask:

> **Which exploration strategy should be used next, given what previous exploration has taught us?**

That gives:

```
Partition
   ↓
Strategy A
   ↓
Outcome
   ↓
Evidence
   ↓
Strategy scoring
   ↓
Strategy B
   ↓
Outcome
   ↓
...
```

But this should **not** immediately become machine learning.

The safer v0.21 abstraction is:

```
deterministic adaptive strategy selection
```

with explicit state:

```
strategy performance
+
partition history
+
cost
+
yield
+
failure rate
+
novelty
```

before introducing any learned policy.

The critical invariant will be:

> **Adaptation may change search priority and strategy selection, but may never bypass domain boundaries, capability constraints, acquisition policy, budgets, provenance, or auditability.**

<!-- CAP-560 | Continue Architecture Planning.md L71212–71240 | turn 55 | version 0.21 -->
## v0.21 — Adaptive Discovery Strategy

> **Source sections:** `CAP-560`

At v0.20 we introduced:

```
DiscoveryDomain
      ↓
SearchSpace
      ↓
Partitions
      ↓
DiscoveryStrategies
      ↓
Exploration Plans
      ↓
Frontier Runtime
```

The next question is:

> **How should the engine decide which exploration strategy is worth trying next?**

This is where the blind-scan analogy becomes a search-control architecture rather than merely a metaphor.

The engine should learn from exploration outcomes, but **without turning the discovery controller into an opaque ML system**.

The first implementation should be deterministic, inspectable, and replayable.

---

<!-- CAP-561 | Continue Architecture Planning.md L71242–71291 | turn 55 | version 0.21 -->
## v0.21 — 21.1 The Adaptive Loop

> **Source sections:** `CAP-561`

The basic loop becomes:

```
                 SEARCH SPACE
                      │
                      ▼
                   PARTITION
                      │
                      ▼
              AVAILABLE STRATEGIES
                      │
                      ▼
                STRATEGY SCORER
                      │
                      ▼
              EXPLORATION PLAN
                      │
                      ▼
                FRONTIER RUNTIME
                      │
                      ▼
                    PROBE
                      │
                      ▼
                 OBSERVATION
                      │
                      ▼
                   OUTCOME
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
      KNOWLEDGE              PERFORMANCE
      EXPANSION                UPDATE
          │                       │
          └───────────┬───────────┘
                      ▼
                 NEXT DECISION
```

The crucial point:

```
strategy selection
```

becomes a **decision**, not a hard-coded traversal order.

---

<!-- CAP-562 | Continue Architecture Planning.md L71293–71345 | turn 55 | version 0.21 -->
## v0.21 — 21.2 Strategy Performance Record

> **Source sections:** `CAP-562`

Introduce a small historical object:

```JavaScript
class StrategyPerformance {
    constructor(data = {}) {
        this.strategyId =
            data.strategyId || null;

        this.partitionKind =
            data.partitionKind || null;

        this.attempts =
            data.attempts || 0;

        this.successes =
            data.successes || 0;

        this.failures =
            data.failures || 0;

        this.candidates =
            data.candidates || 0;

        this.newResources =
            data.newResources || 0;

        this.newArtifacts =
            data.newArtifacts || 0;

        this.usefulClassifications =
            data.usefulClassifications || 0;

        this.costRequests =
            data.costRequests || 0;

        this.costBytes =
            data.costBytes || 0;

        this.elapsedMs =
            data.elapsedMs || 0;
    }
}
```

This is deliberately boring.

That is a feature.

The engine should first know **what happened** before attempting to predict what will happen.

---

<!-- CAP-563 | Continue Architecture Planning.md L71347–71385 | turn 55 | version 0.21 -->
## v0.21 — 21.3 Yield Metrics

> **Source sections:** `CAP-563`

From the record we can derive:

```
candidateYield
    = candidates / attempts

resourceYield
    = newResources / attempts

artifactYield
    = newArtifacts / attempts

classificationYield
    = usefulClassifications / attempts
```

And cost-aware measures:

```
resourcePerRequest
    = newResources / costRequests

artifactPerByte
    = newArtifacts / costBytes
```

These metrics should remain derived.

Do not persist only:

```JavaScript
score: 0.83
```

because then we lose the explanation.

---

<!-- CAP-564 | Continue Architecture Planning.md L71387–71432 | turn 55 | version 0.21 -->
## v0.21 — 21.4 Strategy Score

> **Source sections:** `CAP-564`

A deterministic first version could use:

```
score =
    basePriority
  + historicalYield
  + noveltyBonus
  + agingBonus
  - failurePenalty
  - costPenalty
```

For example:

```JavaScript
function scoreStrategy(strategy, performance, context) {
    const attempts =
        Math.max(1, performance?.attempts || 0);

    const yieldRate =
        (performance?.newResources || 0) / attempts;

    const failureRate =
        (performance?.failures || 0) / attempts;

    const novelty =
        context.partition?.status === 'unexplored'
            ? 0.20
            : 0;

    return (
        strategy.priority() +
        yieldRate +
        novelty -
        failureRate * 0.5
    );
}
```

The exact formula is not the architecture.

The contract is.

---

<!-- CAP-565 | Continue Architecture Planning.md L71434–71486 | turn 55 | version 0.21 -->
## v0.21 — 21.5 Cold Start Problem

> **Source sections:** `CAP-565`

A new strategy has no history.

For example:

```
Strategy:
    sitemap-expansion

attempts = 0
```

We cannot conclude:

```
yield = 0
```

because:

```
unknown
```

is not:

```
zero
```

Therefore the engine needs a cold-start rule.

Possible options:

```
1. optimistic prior
2. mandatory initial probe
3. exploration quota
4. strategy default priority
```

A simple first implementation:

```
unmeasured strategy
    →
receive at least one bounded opportunity
```

This prevents historical incumbents from permanently dominating.

---

<!-- CAP-566 | Continue Architecture Planning.md L71488–71521 | turn 55 | version 0.21 -->
## v0.21 — 21.6 Exploration Quota

> **Source sections:** `CAP-566`

Introduce an explicit quota:

```JavaScript
{
    explorationRatio: 0.20
}
```

Meaning roughly:

```
80%
exploit known high-yield strategies

20%
explore alternatives
```

But this is not necessarily a fixed percentage of requests.

It could operate at the decision level:

```
10 strategy decisions
│
├── 8 exploitation decisions
└── 2 exploration decisions
```

This distinction matters because a single strategy may produce many work items.

---

<!-- CAP-567 | Continue Architecture Planning.md L71523–71570 | turn 55 | version 0.21 -->
## v0.21 — 21.7 Strategy Selection Must Be Constrained

> **Source sections:** `CAP-567`

Adaptive selection cannot simply say:

```
"This strategy looks productive; execute it."
```

The selection pipeline remains:

```
Candidate Strategy
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
Resource/Partition Eligibility
       │
       ▼
Strategy Score
       │
       ▼
Selected Strategy
```

Thus:

```
high score
```

does not override:

```
policy denied
```

---

<!-- CAP-568 | Continue Architecture Planning.md L71572–71610 | turn 55 | version 0.21 -->
## v0.21 — 21.8 Strategy Eligibility

> **Source sections:** `CAP-568`

Introduce:

```JavaScript
class StrategyEligibility {
    constructor(data = {}) {
        this.strategyId =
            data.strategyId || null;

        this.allowed =
            data.allowed !== false;

        this.reason =
            data.reason || null;

        this.missingCapabilities =
            data.missingCapabilities || [];

        this.createdAt =
            data.createdAt || now();
    }
}
```

A strategy can therefore be:

```
eligible
ineligible
temporarily unavailable
budget blocked
capability blocked
policy blocked
```

This distinction becomes important for diagnostics.

---

<!-- CAP-569 | Continue Architecture Planning.md L71612–71664 | turn 55 | version 0.21 -->
## v0.21 — 21.9 Temporary vs Permanent Failure

> **Source sections:** `CAP-569`

Suppose:

```
sitemap strategy
```

fails because:

```
HTTP 503
```

That should not permanently damage its score.

Compare:

```
503
```

with:

```
strategy requires capability:
    filesystem.read

runtime:
    capability unavailable
```

The first is temporary.

The second may be structurally unavailable.

Therefore performance needs failure classification:

```JavaScript
{
    failureClass: "transient"
}
```

versus:

```JavaScript
{
    failureClass: "structural"
}
```

---

<!-- CAP-570 | Continue Architecture Planning.md L71666–71711 | turn 55 | version 0.21 -->
## v0.21 — 21.10 Strategy Outcome

> **Source sections:** `CAP-570`

Introduce an explicit result:

```JavaScript
class StrategyOutcome {
    constructor(data = {}) {
        this.strategyId =
            data.strategyId || null;

        this.partitionId =
            data.partitionId || null;

        this.workItemId =
            data.workItemId || null;

        this.status =
            data.status || 'unknown';

        this.candidates =
            data.candidates || 0;

        this.newResources =
            data.newResources || 0;

        this.newArtifacts =
            data.newArtifacts || 0;

        this.usefulDiscoveries =
            data.usefulDiscoveries || 0;

        this.cost =
            data.cost || {};

        this.failure =
            data.failure || null;

        this.createdAt =
            data.createdAt || now();
    }
}
```

Now strategy adaptation has a clean input.

---

<!-- CAP-571 | Continue Architecture Planning.md L71713–71752 | turn 55 | version 0.21 -->
## v0.21 — 21.11 Strategy Outcome ≠ Strategy Truth

> **Source sections:** `CAP-571`

Suppose:

```
Strategy A:
    0 new resources
```

This does not necessarily mean:

```
Strategy A is bad.
```

Possible explanations:

```
partition genuinely empty
partition already explored
strategy exhausted
temporary failure
wrong partition
insufficient budget
```

Therefore the scorer should consume:

```
+
partition state
+
failure classification
+
historical context
```

rather than raw yield alone.

---

<!-- CAP-572 | Continue Architecture Planning.md L71754–71787 | turn 55 | version 0.21 -->
## v0.21 — 21.12 Novelty

> **Source sections:** `CAP-572`

A powerful signal is **novelty**.

Suppose a strategy repeatedly finds:

```
100 URLs
99 already known
1 new candidate
```

Its candidate yield looks impressive:

```
100 candidates
```

but its discovery value is low.

So measure:

```
novelCandidates
novelResources
novelArtifacts
novelPartitions
```

The last one is particularly important.

A strategy that discovers a new search region may have high value even if it produced few immediate resources.

---

<!-- CAP-573 | Continue Architecture Planning.md L71789–71826 | turn 55 | version 0.21 -->
## v0.21 — 21.13 Frontier Expansion Value

> **Source sections:** `CAP-573`

Consider:

```
Strategy A
    discovers 50 PDFs

Strategy B
    discovers 2 URLs
    but those URLs reveal 6 new repositories
```

A naive crawler favors A.

A blind-scan-inspired system may recognize B as strategically important because:

```
B
 ↓
new search regions
 ↓
future exploration
```

So outcome should include:

```
newPartitions
```

and perhaps:

```
frontierExpansion
```

---

<!-- CAP-574 | Continue Architecture Planning.md L71828–71853 | turn 55 | version 0.21 -->
## v0.21 — 21.14 Frontier Expansion Metric

> **Source sections:** `CAP-574`

Conceptually:

```
frontierExpansion =
    newPartitions
    +
    weightedNewWork
```

This lets us distinguish:

```
resource yield
```

from:

```
search-space yield
```

Both are useful.

---

<!-- CAP-575 | Continue Architecture Planning.md L71855–71901 | turn 55 | version 0.21 -->
## v0.21 — 21.15 Strategy Memory

> **Source sections:** `CAP-575`

Performance should be indexed by context.

Avoid:

```
strategyId → one global score
```

because strategy performance depends heavily on where it is used.

Instead:

```
(strategyId, partitionKind, resourceContext)
```

For example:

```
sitemap-expansion + repository
```

may be excellent.

But:

```
sitemap-expansion + API endpoint
```

may be irrelevant.

A contextual performance key:

```JavaScript
function performanceKey(strategyId, context) {
    return [
        strategyId,
        context.partitionKind || 'unknown',
        context.resourceClass || 'unknown'
    ].join(':');
}
```

---

<!-- CAP-576 | Continue Architecture Planning.md L71903–71955 | turn 55 | version 0.21 -->
## v0.21 — 21.16 Hierarchical Priors

> **Source sections:** `CAP-576`

When there is no local history, fall back:

```
specific context
     ↓
partition kind
     ↓
resource class
     ↓
global strategy history
     ↓
strategy default
```

Example:

```
No history for:

sitemap + technical-document repository
```

Use:

```
sitemap + repository
```

if available.

Otherwise:

```
sitemap
```

Otherwise:

```
global sitemap performance
```

Otherwise:

```
base priority
```

This avoids requiring enormous amounts of historical data.

---

<!-- CAP-577 | Continue Architecture Planning.md L71957–71992 | turn 55 | version 0.21 -->
## v0.21 — 21.17 Discovery Strategy Ledger

> **Source sections:** `CAP-577`

The event ledger should now capture:

```
strategy-eligibility-evaluated
strategy-selected
strategy-rejected
strategy-exploration-started
strategy-exploration-completed
strategy-outcome-recorded
strategy-performance-updated
partition-priority-updated
partition-saturated
partition-reactivated
```

For replay:

```
decision:
    partition = P42
    strategy = sitemap
    score = 0.81
    reason = ...
```

This is much more valuable than:

```
strategy = sitemap
```

without explanation.

---

<!-- CAP-578 | Continue Architecture Planning.md L71994–72028 | turn 55 | version 0.21 -->
## v0.21 — 21.18 Deterministic Replay

> **Source sections:** `CAP-578`
>
> [DOCUMENTATION REVIEW] Contradiction **C-08** ([Review Notes](../REVIEW-NOTES.md#c-08--replay-decisions-deterministic-network-not))

Given:

```
same domain
same search-space state
same strategy registry
same performance history
same budgets
same policy
```

the strategy-selection decision should be reproducible.

Therefore:

```
Decision
=
f(
    domain,
    partition,
    history,
    policy,
    budget,
    strategy-registry
)
```

This is a major architectural property.

Adaptive does not have to mean nondeterministic.

---

<!-- CAP-579 | Continue Architecture Planning.md L72030–72059 | turn 55 | version 0.21 -->
## v0.21 — 21.19 Random Exploration

> **Source sections:** `CAP-579`

At some point, randomization may be useful.

But random selection creates replay problems.

If introduced later, make randomness explicit:

```JavaScript
{
    decisionId: "decision-91",
    randomSeed: 123456
}
```

Then:

```
seed
+
state
+
policy
```

reproduces the decision.

Do not introduce hidden `Math.random()` into the discovery controller.

---

<!-- CAP-580 | Continue Architecture Planning.md L72061–72108 | turn 55 | version 0.21 -->
## v0.21 — 21.20 Learning Must Not Modify Safety Boundaries

> **Source sections:** `CAP-580`

This is probably the most important v0.21 invariant.

An adaptive system can learn:

```
which partition is productive
```

It cannot learn:

```
what is allowed
```

Those are different concerns.

Therefore:

```
LEARNING
    │
    ├── priority
    ├── strategy selection
    ├── exploration order
    └── budget allocation hints
```

while:

```
POLICY
    │
    ├── allowed origins
    ├── allowed methods
    ├── capabilities
    ├── safety constraints
    └── hard budgets
```

remain authoritative.

In other words:

> **Adaptive optimization is subordinate to policy.**

---

<!-- CAP-581 | Continue Architecture Planning.md L72110–72216 | turn 55 | version 0.21 -->
## v0.21 — 21.21 Adaptive Discovery Controller

> **Source sections:** `CAP-581`

We can now extend the controller.

```JavaScript
class AdaptiveDiscoveryController {
    constructor(options = {}) {
        this.strategies =
            options.strategies || [];

        this.performance =
            new Map();

        this.explorationRatio =
            options.explorationRatio ?? 0.2;
    }

    eligibleStrategies(partition, context) {
        return this.strategies.filter(
            strategy =>
                strategy.canExplore(
                    partition,
                    context
                )
        );
    }

    select(partition, context) {
        const eligible =
            this.eligibleStrategies(
                partition,
                context
            );

        if (!eligible.length) {
            return null;
        }

        // Deterministic scoring would occur here.
        return eligible
            .map(strategy => ({
                strategy,
                score: this.score(
                    strategy,
                    partition,
                    context
                )
            }))
            .sort((a, b) =>
                b.score - a.score
            )[0].strategy;
    }

    score(strategy, partition, context) {
        const key =
            performanceKey(
                strategy.describe().id,
                {
                    partitionKind:
                        partition.kind
                }
            );

        const history =
            this.performance.get(key);

        return (
            strategy.priority() +
            this.historyScore(history)
        );
    }

    historyScore(history) {
        if (!history) {
            return 0;
        }

        const attempts =
            Math.max(1, history.attempts);

        const yieldRate =
            history.newResources /
            attempts;

        const failures =
            history.failures /
            attempts;

        return yieldRate -
            failures * 0.5;
    }
}
```

This is only a blueprint.

The production version needs explicit:

* exploration quota,
* aging,
* budget checks,
* deterministic tie-breaking,
* context hierarchy,
* failure decay,
* concurrency awareness.

---

<!-- CAP-582 | Continue Architecture Planning.md L72218–72249 | turn 55 | version 0.21 -->
## v0.21 — 21.22 Tie-Breaking Must Be Deterministic

> **Source sections:** `CAP-582`

Suppose:

```
strategy A = 0.80
strategy B = 0.80
```

Do not rely on:

```
Map iteration order
```

as an implicit policy.

Use:

```
score
↓
strategy priority
↓
strategy ID
```

or another explicit ordering.

This matters for replay.

---

<!-- CAP-583 | Continue Architecture Planning.md L72251–72277 | turn 55 | version 0.21 -->
## v0.21 — 21.23 Performance Decay

> **Source sections:** `CAP-583`

Old history can become stale.

A strategy that worked yesterday may perform poorly today.

Therefore performance should eventually decay.

For example:

```
effectiveHistory =
    recentOutcome × 0.7
    +
    olderHistory × 0.3
```

But again, don't immediately implement complicated exponential statistics.

The architectural requirement is simply:

```
historical performance
    must not become permanent truth.
```

---

<!-- CAP-584 | Continue Architecture Planning.md L72279–72325 | turn 55 | version 0.21 -->
## v0.21 — 21.24 Strategy Adaptation and Scan Sessions

> **Source sections:** `CAP-584`

Performance has another scope question.

Should history survive sessions?

Yes, but carefully.

Separate:

```
Session Performance
```

from:

```
Historical Strategy Performance
```

Session:

```
scan-001
    sitemap = productive
```

Global history:

```
sitemap
    generally productive
```

The session can override global history without modifying the global record.

This gives:

```
Global prior
      ↓
Session adaptation
      ↓
Current decision
```

---

<!-- CAP-585 | Continue Architecture Planning.md L72327–72362 | turn 55 | version 0.21 -->
## v0.21 — 21.25 Search Strategy as a First-Class Graph Node

> **Source sections:** `CAP-585`

At this point, strategy itself can become provenance.

Instead of merely:

```
candidate.sourceId
```

we can record:

```
Candidate
   │
   ▼
Discovery Event
   │
   ├── partition
   ├── strategy
   ├── source
   ├── observation
   └── evidence
```

This answers:

> Why did the engine search this region?

and:

> Why did it use this strategy?

That becomes valuable for later audit and replay.

---

<!-- CAP-586 | Continue Architecture Planning.md L72364–72400 | turn 55 | version 0.21 -->
## v0.21 — 21.26 Search Decision Graph

> **Source sections:** `CAP-586`

We now have a second epistemic layer:

```
             SEARCH DECISION
                    │
          ┌─────────┼─────────┐
          ▼         ▼         ▼
      Partition   Strategy   Context
          │         │
          └────┬────┘
               ▼
             Probe
               │
               ▼
          Observation
               │
               ▼
             Outcome
```

This is different from the EvidenceGraph.

EvidenceGraph answers:

```
Why believe resource X exists?
```

SearchDecisionGraph answers:

```
Why did the engine search here?
```

---

<!-- CAP-587 | Continue Architecture Planning.md L72402–72428 | turn 55 | version 0.21 -->
## v0.21 — 21.27 Two Kinds of Provenance

> **Source sections:** `CAP-587`

This produces an important distinction:

```
EPISTEMIC PROVENANCE
    "Why believe this?"

OPERATIONAL PROVENANCE
    "Why did we do this?"
```

Examples:

```
Epistemic:
    PDF classified as service-manual
    because title + structure + metadata

Operational:
    PDF acquired
    because strategy S ranked partition P highly
```

These should not be merged.

---

<!-- CAP-762 | Continue Architecture Planning.md L78548–78586 | turn 63 | version 0.26 -->
## v0.26 — Search Tactic Runtime

> **Source sections:** `CAP-762`

The next missing boundary is now between:

and:

The planner can describe _what should be searched_, but there is still no formal runtime for executing a **search tactic as a bounded unit of work**.

That suggests:

```
QueryStep
    ↓
TacticRuntime
    ↓
TacticExecution
    ↓
DiscoveryStrategy
    ↓
WorkItems
```

This layer should solve:

* tactic lifecycle
* tactic-specific budgets
* tactic dependencies
* tactic cursors/checkpoints
* tactic-local state
* tactic retries
* tactic cancellation
* tactic result accounting
* tactic-level provenance
* resumability
* interaction between tactic execution and the shared frontier

The key rule should be:

> **A QueryPlan describes search intent; TacticRuntime turns that intent into bounded, resumable execution without acquiring authority beyond the existing domain/policy/capability/runtime boundaries.**

<!-- CAP-764 | Continue Architecture Planning.md L78598–78628 | turn 65 | version 0.26 -->
## v0.26 — Search Tactic Runtime

> **Source sections:** `CAP-764`

We now have:

```
Goal
 ↓
Query Planner
 ↓
QueryPlan
 ↓
QueryStep
 ↓
???
 ↓
DiscoveryStrategy
 ↓
WorkItem
 ↓
FrontierRuntime
```

The missing layer is the **runtime for a planned search tactic**.

The important distinction is:

> **Query planning produces search intent. TacticRuntime executes that intent as a bounded, resumable operation.**

It does not acquire resources directly and it does not bypass the existing discovery/acquisition controls.

---

<!-- CAP-765 | Continue Architecture Planning.md L78630–78673 | turn 65 | version 0.26 -->
## v0.26 — 26.1 The architectural gap

> **Source sections:** `CAP-765`

Previously:

```
QueryPlan
    │
    ├── "enumerate sitemap"
    ├── "expand repository"
    ├── "look for related documents"
    └── "search revision references"
```

But a `QueryStep` is only a description.

A real system needs to answer:

* Has this tactic started?
* Which execution owns it?
* How many probes may it perform?
* Where did it stop?
* Can it resume?
* What happened during the previous batch?
* Which discoveries came from this tactic?
* Can it retry?
* What dependencies must finish first?
* Can it be cancelled?
* Has it exhausted its search region?

Therefore:

```
QueryStep
   ↓
TacticExecution
   ↓
TacticRuntime
   ↓
bounded tactic invocation
   ↓
DiscoveryStrategy
```

---

<!-- CAP-766 | Continue Architecture Planning.md L78675–78713 | turn 65 | version 0.26 -->
## v0.26 — 26.2 QueryStep ≠ TacticExecution

> **Source sections:** `CAP-766`

This distinction is critical.

```
QueryStep
    │
    │ may execute many times
    ▼
TacticExecution #1
    ├── batch 1
    ├── batch 2
    └── batch 3

TacticExecution #2
    ├── batch 1
    └── batch 2
```

A plan is declarative.

An execution is temporal.

Therefore:

```
QueryPlan      = intended search procedure
QueryStep      = one planned tactic
TacticExecution = one execution instance
TacticAttempt   = one attempt/batch execution
```

This follows the same principle already established for acquisition:

```
Plan ≠ Attempt
```

---

<!-- CAP-767 | Continue Architecture Planning.md L78715–78766 | turn 65 | version 0.26 -->
## v0.26 — 26.3 TacticExecution

> **Source sections:** `CAP-767`

```JavaScript
class TacticExecution {
    constructor(data = {}) {
        this.id = data.id || makeId('texec');

        this.planId = data.planId || null;
        this.planVersion = data.planVersion ?? null;

        this.queryStepId = data.queryStepId || null;
        this.tacticId = data.tacticId || null;

        this.sessionId = data.sessionId || null;
        this.partitionId = data.partitionId || null;

        this.status = data.status || 'queued';

        this.attempts = data.attempts || 0;

        this.cursor = data.cursor ?? null;
        this.checkpoint = data.checkpoint ?? null;

        this.stats = {
            batches: 0,
            probes: 0,
            proposals: 0,
            accepted: 0,
            merged: 0,
            rejected: 0,
            errors: 0,
            ...(data.stats || {})
        };

        this.budget = data.budget || null;

        this.createdAt = data.createdAt || now();
        this.startedAt = data.startedAt || null;
        this.completedAt = data.completedAt || null;

        this.error = data.error || null;
    }

    serialize() {
        return { ...this };
    }
}
```

The execution is therefore the durable identity of the tactic's progress.

---

<!-- CAP-768 | Continue Architecture Planning.md L78768–78810 | turn 65 | version 0.26 -->
## v0.26 — 26.4 TacticRuntime

> **Source sections:** `CAP-768`

The runtime owns execution mechanics.

```JavaScript
class TacticRuntime {

    canExecute(execution, context) {
        return false;
    }

    async execute(execution, context) {
        throw new Error('Not implemented');
    }

    cancel(execution, reason = 'cancelled') {
        throw new Error('Not implemented');
    }

    checkpoint(execution, state) {
        throw new Error('Not implemented');
    }

    describe() {
        return {
            id: 'unknown-tactic-runtime',
            name: 'Unknown Tactic Runtime'
        };
    }
}
```

The runtime does **not** decide:

```
"this URL is safe"
"this endpoint may be accessed"
"this resource is relevant"
```

Those decisions remain with existing layers.

---

<!-- CAP-769 | Continue Architecture Planning.md L78812–78861 | turn 65 | version 0.26 -->
## v0.26 — 26.5 TacticRuntime responsibilities

> **Source sections:** `CAP-769`

The runtime owns:

```
Lifecycle
Budget
Batching
Checkpointing
Cursor persistence
Cancellation
Retry
Dependency validation
Accounting
Provenance
Resume
```

It does not own:

```
Domain authority
Acquisition authority
Resource identity
Semantic truth
Policy override
```

This gives us another clean boundary:

```
TacticRuntime
│
├── execution mechanics
│
├── progress
│
├── accounting
│
└── resumability

        BUT NOT

├── authorization
├── acquisition
├── classification truth
└── identity truth
```

---

<!-- CAP-770 | Continue Architecture Planning.md L78863–78920 | turn 65 | version 0.26 -->
## v0.26 — 26.6 Tactic contract

> **Source sections:** `CAP-770`

A tactic should itself remain relatively small.

```JavaScript
class SearchTactic {

    canExecute(step, context) {
        return false;
    }

    async execute(context) {
        throw new Error('Not implemented');
    }

    describe() {
        return {
            id: 'unknown-tactic',
            name: 'Unknown Search Tactic'
        };
    }
}
```

The important part is the `context`.

The tactic receives controlled capabilities rather than the entire engine.

Conceptually:

```JavaScript
const context = {
    goal,
    domain,
    partition,
    step,
    execution,

    budget,
    cursor,

    proposeCandidate,
    scheduleProbe,
    emitEvidence,

    cancellation
};
```

Not:

```JavaScript
context.engine = engine;
```

That would recreate the global-coupling problem.

---

<!-- CAP-771 | Continue Architecture Planning.md L78922–78962 | turn 65 | version 0.26 -->
## v0.26 — 26.7 Capability surface

> **Source sections:** `CAP-771`

A tactic should receive the smallest possible interface.

```
Tactic
  │
  ├── read Goal
  ├── read Domain
  ├── read Partition
  ├── read checkpoint
  │
  ├── propose Candidate
  ├── request Probe
  ├── emit Evidence
  │
  └── observe Cancellation
```

It should **not** receive:

```
scheduler.enqueue(...)
kernel.modifyPolicy(...)
database.delete(...)
network.fetch(...)
```

Instead:

```
Tactic
  ↓
TacticContext
  ↓
controlled interfaces
```

This is particularly important for a userscript because every JavaScript component otherwise effectively shares the same authority.

---

<!-- CAP-772 | Continue Architecture Planning.md L78964–79006 | turn 65 | version 0.26 -->
## v0.26 — 26.8 Bounded execution

> **Source sections:** `CAP-772`

A tactic must not be allowed to run indefinitely.

For example:

```JavaScript
{
    maxBatches: 20,
    maxProbes: 100,
    maxProposals: 500,
    maxBytes: 10_000_000,
    maxElapsedMs: 30_000
}
```

The tactic runtime checks these limits.

```
TacticExecution
       │
       ├── batch budget
       ├── probe budget
       ├── proposal budget
       ├── byte budget
       └── time budget
```

This is separate from the global acquisition budget.

Therefore:

```
Global acquisition budget
        │
        └── Tactic budget
                │
                └── Batch budget
```

A tactic cannot create unlimited work simply because the global system still has capacity.

---

<!-- CAP-773 | Continue Architecture Planning.md L79008–79074 | turn 65 | version 0.26 -->
## v0.26 — 26.9 Batch execution

> **Source sections:** `CAP-773`

The fundamental execution unit becomes a **tactic batch**.

```
TacticExecution
       │
       ├── Batch 1
       ├── Batch 2
       ├── Batch 3
       └── ...
```

Example:

```JavaScript
class TacticBatch {
    constructor(data = {}) {
        this.id = data.id || makeId('tbatch');

        this.executionId = data.executionId || null;

        this.sequence = data.sequence ?? 0;

        this.cursorBefore = data.cursorBefore ?? null;
        this.cursorAfter = data.cursorAfter ?? null;

        this.probes = data.probes || 0;
        this.proposals = data.proposals || 0;

        this.status = data.status || 'running';

        this.startedAt = data.startedAt || now();
        this.completedAt = data.completedAt || null;

        this.error = data.error || null;
    }
}
```

Why batches matter:

```
large enumeration
       ↓
small bounded units
       ↓
checkpoint
       ↓
resume
```

This is much closer to the original **blind-scan analogy**:

```
scan region
   ↓
inspect bounded portion
   ↓
record findings
   ↓
move scan cursor
   ↓
continue
```

---

<!-- CAP-774 | Continue Architecture Planning.md L79076–79123 | turn 65 | version 0.26 -->
## v0.26 — 26.10 Cursor

> **Source sections:** `CAP-774`

A tactic may need to remember where it stopped.

```JavaScript
{
    kind: 'opaque',
    provider: 'sitemap',
    value: 'page-token-42'
}
```

Or:

```JavaScript
{
    kind: 'offset',
    value: 500
}
```

Or:

```JavaScript
{
    kind: 'partition',
    value: 'path-prefix:/manuals/'
}
```

The runtime should **not interpret opaque cursors**.

That belongs to the tactic.

```
TacticRuntime
      │
      │ stores
      ▼
opaque cursor
      ▲
      │
Tactic understands it
```

This avoids coupling the generic engine to every possible enumeration protocol.

---

<!-- CAP-775 | Continue Architecture Planning.md L79125–79165 | turn 65 | version 0.26 -->
## v0.26 — 26.11 Checkpoint

> **Source sections:** `CAP-775`

Cursor alone is insufficient.

A checkpoint should describe durable progress.

```JavaScript
class TacticCheckpoint {
    constructor(data = {}) {
        this.id = data.id || makeId('checkpoint');

        this.executionId = data.executionId || null;

        this.sequence = data.sequence ?? 0;

        this.cursor = data.cursor ?? null;

        this.stats = data.stats || {};

        this.strategyState = data.strategyState ?? null;

        this.createdAt = data.createdAt || now();
    }

    serialize() {
        return { ...this };
    }
}
```

Important distinction:

```
Cursor
= where the tactic believes it is

Checkpoint
= durable execution state at that point
```

---

<!-- CAP-776 | Continue Architecture Planning.md L79167–79219 | turn 65 | version 0.26 -->
## v0.26 — 26.12 Checkpoint atomicity

> **Source sections:** `CAP-776`
>
> [DOCUMENTATION REVIEW] Contradiction **C-03** ([Review Notes](../REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming))

A dangerous failure exists:

```
1. discover candidates
2. advance cursor
3. crash
4. candidate records not persisted
```

Now the engine may skip resources.

The reverse is also possible:

```
1. persist candidates
2. crash before cursor update
3. resume
4. candidates discovered again
```

The second case is usually safer because candidate identity + provenance deduplication can tolerate repetition.

Therefore the default recovery preference should be:

```
duplicate work
    >
silent loss of search coverage
```

A durable ordering should resemble:

```
discover
  ↓
persist discoveries/candidates
  ↓
persist checkpoint
```

rather than:

```
advance cursor
  ↓
discover
```

This is an important completeness invariant.

---

<!-- CAP-777 | Continue Architecture Planning.md L79221–79272 | turn 65 | version 0.26 -->
## v0.26 — 26.13 Tactic dependencies

> **Source sections:** `CAP-777`

Query steps can depend on other steps:

```
Step A
  ↓
discover repository
  ↓
Step B
  ↓
enumerate repository
```

Therefore:

```JavaScript
{
    id: 'step-b',
    dependsOn: ['step-a']
}
```

The runtime must not execute B until the dependency contract is satisfied.

```
PLANNED
   ↓
BLOCKED
   ↓
READY
   ↓
RUNNING
```

Dependency completion should be explicit.

Do not use:

```JavaScript
if (somePreviousThingProbablyFinished)
```

Instead:

```
DependencyResolver
       ↓
explicit execution state
```

---

<!-- CAP-778 | Continue Architecture Planning.md L79274–79315 | turn 65 | version 0.26 -->
## v0.26 — 26.14 Tactic lifecycle

> **Source sections:** `CAP-778`

A useful lifecycle is:

```
PLANNED
   ↓
BLOCKED
   ↓
READY
   ↓
CLAIMED
   ↓
RUNNING
   ↓
CHECKPOINTED
   ↓
RUNNING
   ↓
EXHAUSTED
   ↓
COMPLETED
```

Exceptional states:

```
CANCELLED
FAILED
DELAYED
DENIED
BUDGET_EXHAUSTED
PAUSED
```

`CHECKPOINTED` does not necessarily mean stopped.

It means:

> durable progress has been established.

---

<!-- CAP-779 | Continue Architecture Planning.md L79317–79372 | turn 65 | version 0.26 -->
## v0.26 — 26.15 Exhaustion vs completion

> **Source sections:** `CAP-779`

We already established this distinction for partitions.

It applies here too.

```
TACTIC EXHAUSTED
```

means:

> The tactic's enumerator has no more work under its current execution semantics.

It does **not** mean:

```
Goal complete
Domain complete
Partition complete
Universe complete
```

For example:

```
SitemapTactic
   ↓
sitemap exhausted
```

does not establish:

```
website exhausted
```

The sitemap may be incomplete.

Therefore:

```
TacticExhausted
    ≠
PartitionExhausted
    ≠
SearchSpaceExhausted
    ≠
GoalSatisfied
    ≠
GoalComplete
```

This separation should remain explicit throughout the architecture.

---

<!-- CAP-780 | Continue Architecture Planning.md L79374–79424 | turn 65 | version 0.26 -->
## v0.26 — 26.16 Tactic result

> **Source sections:** `CAP-780`

The tactic should return structured results rather than mutating the engine.

```JavaScript
class TacticResult {
    constructor(data = {}) {
        this.executionId = data.executionId || null;

        this.status = data.status || 'unknown';

        this.proposals = data.proposals || [];
        this.evidence = data.evidence || [];

        this.cursor = data.cursor ?? null;
        this.checkpoint = data.checkpoint ?? null;

        this.exhausted = data.exhausted === true;

        this.stats = data.stats || {};

        this.reason = data.reason || null;
    }
}
```

For example:

```JavaScript
{
    status: 'progress',

    proposals: [
        {
            target: 'https://example.org/manual.pdf',
            type: 'document'
        }
    ],

    cursor: {
        kind: 'offset',
        value: 100
    },

    exhausted: false
}
```

The runtime then feeds proposals through the **existing CandidateNormalizer / DiscoveryController**.

---

<!-- CAP-781 | Continue Architecture Planning.md L79426–79465 | turn 65 | version 0.26 -->
## v0.26 — 26.17 Tactic does not create candidates directly

> **Source sections:** `CAP-781`

This is important.

Avoid:

```
Tactic
  ↓
KB.candidates.add(...)
```

Instead:

```
Tactic
  ↓
CandidateProposal
  ↓
DiscoveryController
  ↓
CandidateNormalizer
  ↓
Candidate
```

Therefore all candidate creation still passes through:

```
identity
policy
domain
provenance
deduplication
accounting
```

The tactic only proposes.

---

<!-- CAP-782 | Continue Architecture Planning.md L79467–79521 | turn 65 | version 0.26 -->
## v0.26 — 26.18 Tactic → Strategy relationship

> **Source sections:** `CAP-782`

The hierarchy is now:

```
Goal
 │
 ▼
QueryPlan
 │
 ▼
QueryStep
 │
 ▼
TacticExecution
 │
 ▼
SearchTactic
 │
 ▼
DiscoveryStrategy
 │
 ▼
CandidateSource / probes
```

But the distinction must remain:

| Layer | Question |
| --- | --- |
| Goal | What do we want? |
| Query Plan | What search operations should be attempted? |
| Query Step | What tactic should be executed? |
| Tactic | What search procedure does this step represent? |
| Strategy | How should that region be explored? |
| Candidate Source | How do we extract candidates? |
| Acquisition Runtime | How may we obtain something? |

A tactic can invoke one or more strategies.

Example:

```
DocumentFamilyTactic
       │
       ├── DocumentFamilyStrategy
       │
       ├── CrossReferenceStrategy
       │
       └── SitemapStrategy
```

But the tactic still cannot bypass runtime controls.

---

<!-- CAP-783 | Continue Architecture Planning.md L79523–79580 | turn 65 | version 0.26 -->
## v0.26 — 26.19 Tactic provenance

> **Source sections:** `CAP-783`

Every tactic execution should explain itself.

```JavaScript
{
    executionId: 'texec-41',

    provenance: {
        goalId: 'goal-7',
        planId: 'qplan-3',
        planVersion: 2,
        queryStepId: 'qstep-9',

        tacticId: 'repository-discovery',
        tacticVersion: '1.2',

        partitionId: 'partition-14',

        reason: {
            kind: 'goal-driven',
            evidenceIds: ['ev-81', 'ev-92']
        }
    }
}
```

Then the provenance chain becomes:

```
Goal
 ↓
QueryPlan
 ↓
QueryStep
 ↓
TacticExecution
 ↓
Strategy
 ↓
Probe
 ↓
Observation
 ↓
Evidence
 ↓
Candidate
 ↓
Resource
```

This is substantially stronger than:

```
candidate.source = "some tactic"
```

---

<!-- CAP-785 | Continue Architecture Planning.md L79586–79593 | turn 65 | version 0.26 -->
### v0.26 — Planning failures

> **Source sections:** `CAP-785`

```
invalid-step
unknown-tactic
unsupported-tactic
dependency-unsatisfied
```

<!-- CAP-786 | Continue Architecture Planning.md L79595–79605 | turn 65 | version 0.26 -->
### v0.26 — Runtime failures

> **Source sections:** `CAP-786`

```
execution-claim-failed
checkpoint-failed
cursor-invalid
state-corrupt
budget-exhausted
timeout
cancelled
```

<!-- CAP-787 | Continue Architecture Planning.md L79607–79614 | turn 65 | version 0.26 -->
### v0.26 — Strategy failures

> **Source sections:** `CAP-787`

```
strategy-unavailable
strategy-failed
strategy-policy-conflict
strategy-capability-missing
```

<!-- CAP-788 | Continue Architecture Planning.md L79616–79624 | turn 65 | version 0.26 -->
### v0.26 — Search failures

> **Source sections:** `CAP-788`

```
enumeration-incomplete
enumeration-invalid
pagination-error
cursor-expired
partition-inaccessible
```

<!-- CAP-789 | Continue Architecture Planning.md L79626–79649 | turn 65 | version 0.26 -->
### v0.26 — Recovery failures

> **Source sections:** `CAP-789`

```
checkpoint-incompatible
plan-version-mismatch
tactic-version-mismatch
resume-state-invalid
```

Crucially:

```
Tactic failure
    ≠
Search absence
```

A failed enumeration must not generate:

```
ABSENT
```

---

<!-- CAP-790 | Continue Architecture Planning.md L79651–79700 | turn 65 | version 0.26 -->
## v0.26 — 26.21 Retry semantics

> **Source sections:** `CAP-790`

Tactic retries must preserve execution identity.

```
TacticExecution
       │
       ├── Attempt 1
       ├── Attempt 2
       └── Attempt 3
```

Not:

```
new tactic execution
```

unless the planner explicitly creates a new execution.

This gives:

```
executionId = stable
attemptId   = transient
```

Retry policy can depend on failure class.

For example:

```
503
 ↓
retry

invalid cursor
 ↓
do not blindly retry

policy denied
 ↓
do not retry

checkpoint corruption
 ↓
recovery path
```

---

<!-- CAP-791 | Continue Architecture Planning.md L79702–79735 | turn 65 | version 0.26 -->
## v0.26 — 26.22 Cancellation

> **Source sections:** `CAP-791`

Cancellation must propagate through the tactic context.

```JavaScript
const cancellation = {
    isCancelled() {
        return false;
    },

    throwIfCancelled() {
        if (this.isCancelled()) {
            throw new Error('cancelled');
        }
    }
};
```

A tactic should check cancellation at bounded points:

```
before batch
after probe
before persistence
before next batch
```

The runtime should not assume JavaScript can forcibly terminate arbitrary synchronous tactic code.

Therefore:

> Cancellation is cooperative unless execution is delegated to an independently cancellable primitive.

---

<!-- CAP-792 | Continue Architecture Planning.md L79737–79782 | turn 65 | version 0.26 -->
## v0.26 — 26.23 Shared Frontier interaction

> **Source sections:** `CAP-792`

The tactic runtime must not create a competing scheduler.

Bad:

```
FrontierRuntime
       +
TacticRuntime scheduler
       +
Acquisition scheduler
```

This creates multiple authorities.

Better:

```
                 FrontierRuntime
                       │
             ┌─────────┴─────────┐
             │                   │
      Tactic WorkItems    Acquisition WorkItems
             │                   │
       TacticRuntime      AcquisitionRuntime
```

So:

```
FrontierRuntime
= global work admission/order/claim/lease

TacticRuntime
= tactic execution semantics

AcquisitionRuntime
= acquisition execution semantics
```

One scheduler authority.

Multiple execution semantics.

---

<!-- CAP-794 | Continue Architecture Planning.md L79854–79892 | turn 65 | version 0.26 -->
## v0.26 — 26.25 Accounting

> **Source sections:** `CAP-794`

A tactic should produce explicit accounting.

```JavaScript
{
    probes: 12,
    proposals: 43,
    accepted: 31,
    merged: 9,
    rejected: 3,

    newResources: 18,
    newArtifacts: 7,

    bytesRequested: 245000,
    elapsedMs: 3812
}
```

This feeds the adaptive layer:

```
TacticOutcome
      ↓
StrategyPerformance
      ↓
AdaptiveStrategySelector
```

But the result must remain evidence, not authority.

```
historical yield
    ≠
guaranteed future yield
```

---

<!-- CAP-797 | Continue Architecture Planning.md L79966–80013 | turn 65 | version 0.26 -->
## v0.26 — 26.28 New state model

> **Source sections:** `CAP-797`

We now have three different state machines:

```
PLAN STATE

planned
   ↓
validated
   ↓
admitted
   ↓
executing
   ↓
completed / superseded
```

```
TACTIC EXECUTION STATE

queued
   ↓
claimed
   ↓
running
   ├── checkpointed ──→ running
   ├── delayed ───────→ queued
   ├── exhausted ─────→ completed
   ├── cancelled
   └── failed
```

```
SEARCH STATE

partition
   ↓
exploring
   ↓
partial
   ↓
saturated / exhausted
```

These states should not be collapsed.

---

<!-- CAP-814 | Continue Architecture Planning.md L80210–80255 | turn 67 | version 0.27 -->
## v0.27 — Enumeration Runtime

> **Source sections:** `CAP-814`

v0.26 gave us:

```
QueryStep
   ↓
TacticExecution
   ↓
TacticRuntime
   ↓
DiscoveryStrategy
```

But some search procedures are not merely exploratory. They are **enumerators**.

Examples:

```
Sitemap
Repository index
API pagination
Manifest
Feed
Catalog
Finite document listing
Directory-like index
```

These have an additional property:

> They claim to traverse a sequence or set of entries according to an explicit enumeration mechanism.

That introduces a new boundary:

```
TacticRuntime
      ↓
EnumerationRuntime
      ↓
Enumerator
      ↓
Entries
```

---

<!-- CAP-815 | Continue Architecture Planning.md L80257–80301 | turn 67 | version 0.27 -->
## v0.27 — 27.1 The central distinction

> **Source sections:** `CAP-815`

We must distinguish:

```
Exploration
```

from:

```
Enumeration
```

Exploration:

```
"Try this strategy and see what you discover."
```

Enumeration:

```
"Traverse this defined sequence until its termination condition is satisfied."
```

Therefore:

```
StrategyExhausted
    ≠
EnumeratorExhausted
```

and more importantly:

```
EnumeratorExhausted
    ≠
EnumerationComplete
```

unless the enumeration contract establishes that relationship.

---

<!-- CAP-816 | Continue Architecture Planning.md L80303–80333 | turn 67 | version 0.27 -->
## v0.27 — 27.2 Enumeration as a contract

> **Source sections:** `CAP-816`

An enumerator should answer:

1. What is being enumerated?
2. What constitutes one entry?
3. How are entries ordered?
4. How does pagination work?
5. How is progress represented?
6. What means "end of enumeration"?
7. Can entries repeat?
8. Can entries disappear?
9. Can the enumeration be incomplete?
10. What evidence supports completeness?

Conceptually:

```
EnumerationContract
├── subject
├── entry model
├── ordering
├── pagination
├── cursor semantics
├── termination semantics
├── cardinality
├── completeness conditions
└── consistency model
```

---

<!-- CAP-817 | Continue Architecture Planning.md L80335–80377 | turn 67 | version 0.27 -->
## v0.27 — 27.3 Enumerator interface

> **Source sections:** `CAP-817`

```JavaScript
class Enumerator {

    canEnumerate(target, context) {
        return false;
    }

    async begin(context) {
        throw new Error('Not implemented');
    }

    async next(context, cursor) {
        throw new Error('Not implemented');
    }

    async checkpoint(context, state) {
        return state;
    }

    async validateCursor(context, cursor) {
        return { valid: true };
    }

    describe() {
        return {
            id: 'unknown-enumerator',
            name: 'Unknown Enumerator'
        };
    }
}
```

The crucial operation is:

```
next(cursor)
```

which produces a bounded page/batch.

---

<!-- CAP-818 | Continue Architecture Planning.md L80379–80423 | turn 67 | version 0.27 -->
## v0.27 — 27.4 EnumerationPage

> **Source sections:** `CAP-818`

The result of one enumeration operation should be explicit.

```JavaScript
class EnumerationPage {
    constructor(data = {}) {
        this.sequence = data.sequence ?? 0;

        this.entries = data.entries || [];

        this.cursorBefore = data.cursorBefore ?? null;
        this.cursorAfter = data.cursorAfter ?? null;

        this.hasMore = data.hasMore ?? null;

        this.total = Number.isFinite(data.total)
            ? data.total
            : null;

        this.status = data.status || 'partial';

        this.evidenceIds = data.evidenceIds || [];

        this.createdAt = data.createdAt || now();
    }

    serialize() {
        return { ...this };
    }
}
```

This creates an explicit unit:

```
Enumeration
    │
    ├── Page 0
    ├── Page 1
    ├── Page 2
    └── ...
```

---

<!-- CAP-819 | Continue Architecture Planning.md L80425–80475 | turn 67 | version 0.27 -->
## v0.27 — 27.5 `hasMore` is not always trustworthy

> **Source sections:** `CAP-819`

A major failure mode is assuming:

```JavaScript
hasMore === false
```

means:

```
complete enumeration
```

It may only mean:

```
this provider says there are no more pages
```

Those are different claims.

Therefore:

```
ProviderTermination
        ≠
CompletenessProof
```

For example:

```
API:
page=7
has_more=false
```

supports:

```
"No further page was reported by this API response."
```

It does not necessarily prove:

```
"No resources exist outside this API."
```

---

<!-- CAP-820 | Continue Architecture Planning.md L80477–80515 | turn 67 | version 0.27 -->
## v0.27 — 27.6 Enumeration state machine

> **Source sections:** `CAP-820`

```
UNINITIALIZED
      ↓
INITIALIZED
      ↓
ENUMERATING
      ↓
PAGE_OBSERVED
      ↓
CHECKPOINTED
      ↓
ENUMERATING
      │
      ├── MORE
      │    ↓
      │  ENUMERATING
      │
      └── NO_MORE
           ↓
       TERMINATED
           ↓
     COMPLETENESS ASSESSMENT
```

Exceptional states:

```
INVALID_CURSOR
PAGINATION_ERROR
INCONSISTENT
INCOMPLETE
CANCELLED
FAILED
BUDGET_EXHAUSTED
```

---

<!-- CAP-821 | Continue Architecture Planning.md L80517–80563 | turn 67 | version 0.27 -->
## v0.27 — 27.7 EnumerationRuntime

> **Source sections:** `CAP-821`

The runtime sits between tactic execution and the concrete enumerator.

```
QueryStep
    ↓
TacticExecution
    ↓
TacticRuntime
    ↓
EnumerationRuntime
    ↓
Enumerator
    ↓
EnumerationPage
    ↓
CandidateProposal
```

Contract:

```JavaScript
class EnumerationRuntime {

    async execute(execution, enumerator, context) {
        throw new Error('Not implemented');
    }

    async resume(execution, enumerator, context) {
        throw new Error('Not implemented');
    }

    validateTermination(page, context) {
        return {
            terminated: false,
            evidenceIds: []
        };
    }
}
```

The runtime owns enumeration mechanics.

The enumerator owns protocol-specific semantics.

---

<!-- CAP-822 | Continue Architecture Planning.md L80565–80594 | turn 67 | version 0.27 -->
## v0.27 — 27.8 Why this should not be inside DiscoveryStrategy

> **Source sections:** `CAP-822`

Without this layer:

```
DiscoveryStrategy
   ├── sitemap logic
   ├── cursor logic
   ├── pagination
   ├── retry
   ├── checkpoint
   ├── duplicate detection
   └── termination
```

Every strategy reinvents the same machinery.

Instead:

```
DiscoveryStrategy
        ↓
EnumerationRuntime
        ↓
Enumerator
```

The reusable machinery becomes centralized.

---

<!-- CAP-823 | Continue Architecture Planning.md L80596–80596 | turn 67 | version 0.27 -->
## v0.27 — 27.9 Enumerator examples

> **Source sections:** `CAP-823`



<!-- CAP-824 | Continue Architecture Planning.md L80598–80606 | turn 67 | version 0.27 -->
### v0.27 — Sitemap

> **Source sections:** `CAP-824`

```
Sitemap
  ↓
URL entries
  ↓
next sitemap page
```

<!-- CAP-825 | Continue Architecture Planning.md L80608–80618 | turn 67 | version 0.27 -->
### v0.27 — API

> **Source sections:** `CAP-825`

```
API endpoint
  ↓
page/token
  ↓
entries
  ↓
next token
```

<!-- CAP-826 | Continue Architecture Planning.md L80620–80630 | turn 67 | version 0.27 -->
### v0.27 — Repository

> **Source sections:** `CAP-826`

```
repository index
  ↓
items
  ↓
pagination
  ↓
next page
```

<!-- CAP-827 | Continue Architecture Planning.md L80632–80644 | turn 67 | version 0.27 -->
### v0.27 — Manifest

> **Source sections:** `CAP-827`

```
manifest
  ↓
finite entry set
  ↓
end-of-list
```

All four can use the same runtime.

---

<!-- CAP-828 | Continue Architecture Planning.md L80646–80688 | turn 67 | version 0.27 -->
## v0.27 — 27.10 EnumerationEntry

> **Source sections:** `CAP-828`

Entries should not immediately become candidates.

```JavaScript
class EnumerationEntry {
    constructor(data = {}) {
        this.id = data.id || makeId('entry');

        this.position = data.position ?? null;

        this.value = data.value ?? null;

        this.type = data.type || 'unknown';

        this.sourceLocator = data.sourceLocator || null;

        this.evidenceIds = data.evidenceIds || [];

        this.createdAt = data.createdAt || now();
    }

    serialize() {
        return { ...this };
    }
}
```

Pipeline:

```
EnumerationEntry
       ↓
CandidateProposal
       ↓
CandidateNormalizer
       ↓
Candidate
```

This preserves the existing architecture.

---

<!-- CAP-829 | Continue Architecture Planning.md L80690–80728 | turn 67 | version 0.27 -->
## v0.27 — 27.11 Entry identity

> **Source sections:** `CAP-829`
>
> [DOCUMENTATION REVIEW] Contradiction **C-04** ([Review Notes](../REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution))

An enumerator can encounter duplicates:

```
page 1 → /manual.pdf
page 4 → /manual.pdf
```

or:

```
repository A → X
repository B → X
```

Do not assume:

```
same position = same resource
```

Instead:

```
Entry identity
    ≠
Candidate identity
    ≠
Resource identity
```

The entry records the enumeration fact.

The normalizer resolves the candidate.

The ResourceGraph resolves logical identity.

---

<!-- CAP-830 | Continue Architecture Planning.md L80730–80732 | turn 67 | version 0.27 -->
## v0.27 — 27.12 Enumeration cursor

> **Source sections:** `CAP-830`

There are several cursor classes.

<!-- CAP-831 | Continue Architecture Planning.md L80734–80741 | turn 67 | version 0.27 -->
### v0.27 — Offset

> **Source sections:** `CAP-831`

```JavaScript
{
    kind: 'offset',
    value: 200
}
```

<!-- CAP-832 | Continue Architecture Planning.md L80743–80750 | turn 67 | version 0.27 -->
### v0.27 — Page

> **Source sections:** `CAP-832`

```JavaScript
{
    kind: 'page',
    value: 5
}
```

<!-- CAP-833 | Continue Architecture Planning.md L80752–80759 | turn 67 | version 0.27 -->
### v0.27 — Token

> **Source sections:** `CAP-833`

```JavaScript
{
    kind: 'opaque-token',
    value: 'abc123'
}
```

<!-- CAP-834 | Continue Architecture Planning.md L80761–80768 | turn 67 | version 0.27 -->
### v0.27 — Locator

> **Source sections:** `CAP-834`

```JavaScript
{
    kind: 'last-entry',
    value: 'https://example.org/item/42'
}
```

<!-- CAP-835 | Continue Architecture Planning.md L80770–80786 | turn 67 | version 0.27 -->
### v0.27 — Composite

> **Source sections:** `CAP-835`

```JavaScript
{
    kind: 'composite',
    value: {
        page: 5,
        token: 'abc'
    }
}
```

The generic runtime stores these.

It should not reinterpret opaque values.

---

<!-- CAP-836 | Continue Architecture Planning.md L80788–80835 | turn 67 | version 0.27 -->
## v0.27 — 27.13 Cursor validity

> **Source sections:** `CAP-836`

A cursor can become invalid.

Examples:

```
API token expired
repository changed
pagination scheme changed
manifest replaced
cursor belongs to old revision
```

Therefore:

```JavaScript
{
    valid: false,
    reason: 'cursor-expired'
}
```

must be a normal outcome.

Do not automatically reset to the beginning.

That could cause:

```
infinite replay
```

or enormous duplicate work.

Recovery should be explicit:

```
invalid cursor
   ↓
attempt recovery policy
   ├── restart
   ├── alternate cursor
   ├── abandon
   └── manual intervention
```

---

<!-- CAP-837 | Continue Architecture Planning.md L80837–80868 | turn 67 | version 0.27 -->
## v0.27 — 27.14 Enumeration snapshot

> **Source sections:** `CAP-837`

For stronger completeness reasoning, the engine should identify what enumeration was observed.

```JavaScript
class EnumerationSnapshot {
    constructor(data = {}) {
        this.id = data.id || makeId('enum-snapshot');

        this.enumeratorId = data.enumeratorId || null;
        this.enumeratorVersion = data.enumeratorVersion || null;

        this.target = data.target || null;

        this.observationId = data.observationId || null;
        this.artifactId = data.artifactId || null;

        this.startedAt = data.startedAt || null;
        this.completedAt = data.completedAt || null;

        this.entryCount = data.entryCount ?? null;

        this.consistency = data.consistency || 'unknown';

        this.createdAt = data.createdAt || now();
    }
}
```

Now completeness can refer to a concrete snapshot.

---

<!-- CAP-838 | Continue Architecture Planning.md L80870–80895 | turn 67 | version 0.27 -->
## v0.27 — 27.15 Why snapshot identity matters

> **Source sections:** `CAP-838`
>
> [DOCUMENTATION REVIEW] Contradiction **C-04** ([Review Notes](../REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution))

Suppose:

```
10:00 sitemap → 100 entries
10:05 sitemap → 103 entries
```

The second observation does not invalidate the first historical observation.

Instead:

```
Sitemap Snapshot A
    → 100 entries

Sitemap Snapshot B
    → 103 entries
```

The engine can then reason about change.

This connects directly to v0.23 temporal absence reasoning.

---

<!-- CAP-839 | Continue Architecture Planning.md L80897–80932 | turn 67 | version 0.27 -->
## v0.27 — 27.16 Cardinality

> **Source sections:** `CAP-839`

Some enumerators expose a total:

```
total = 10,000
```

The runtime can record:

```JavaScript
{
    observed: 750,
    reportedTotal: 10000
}
```

But:

```
reportedTotal
```

is evidence, not truth.

Therefore:

```
ReportedCardinality
    ≠
VerifiedCardinality
```

A provider could be wrong, stale, filtered, paginated incorrectly, or access-dependent.

---

<!-- CAP-840 | Continue Architecture Planning.md L80934–80974 | turn 67 | version 0.27 -->
## v0.27 — 27.17 Ordering semantics

> **Source sections:** `CAP-840`

Enumeration ordering matters for recovery.

Possible semantics:

```
stable
unstable
unknown
```

Stable:

```
page 1 → A B C
page 2 → D E F
```

Unstable:

```
page 1 → A B C
database changes
page 2 → C D E
```

This can produce duplicates or skipped entries.

Therefore:

```JavaScript
{
    ordering: 'unstable',
    consistency: 'eventually-consistent'
}
```

should affect completeness claims.

---

<!-- CAP-841 | Continue Architecture Planning.md L80976–81012 | turn 67 | version 0.27 -->
## v0.27 — 27.18 Enumeration consistency

> **Source sections:** `CAP-841`

Useful states:

```
consistent
snapshot-consistent
eventually-consistent
unstable
unknown
```

A snapshot-consistent enumeration is much stronger than repeatedly querying a changing endpoint.

For example:

```
Repository snapshot
       ↓
pages 1..N
       ↓
same snapshot ID
```

supports stronger coverage reasoning than:

```
live repository
 ↓
page 1
 ↓
live repository
 ↓
page 2
```

---

<!-- CAP-842 | Continue Architecture Planning.md L81014–81053 | turn 67 | version 0.27 -->
## v0.27 — 27.19 Completeness assessment

> **Source sections:** `CAP-842`
>
> [DOCUMENTATION REVIEW] Contradiction **C-05** ([Review Notes](../REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified))

The EnumerationRuntime should produce a **termination observation**, not directly assert global completeness.

```JavaScript
class EnumerationTermination {
    constructor(data = {}) {
        this.executionId = data.executionId || null;

        this.status = data.status || 'unknown';

        this.reason = data.reason || null;

        this.conditions = data.conditions || [];

        this.evidenceIds = data.evidenceIds || [];

        this.createdAt = data.createdAt || now();
    }
}
```

Example:

```
status:
    terminated

reason:
    provider-reported-end

conditions:
    pagination-complete
    cursor-valid
    snapshot-consistent
```

This becomes evidence for v0.22's coverage/completeness layer.

---

<!-- CAP-843 | Continue Architecture Planning.md L81055–81088 | turn 67 | version 0.27 -->
## v0.27 — 27.20 The crucial three-level distinction

> **Source sections:** `CAP-843`

We now have:

```
Level 1
Enumerator terminated

Level 2
Enumeration contract satisfied

Level 3
Completeness claim justified
```

Formally:

```
Terminated(E)
    ⇏
CompleteEnumeration(E)
```

unless:

```
TerminationConditionsSatisfied(E)
∧
EnumerationContractValid(E)
```

and even then the resulting completeness claim is scoped to the enumeration contract.

---

<!-- CAP-844 | Continue Architecture Planning.md L81090–81135 | turn 67 | version 0.27 -->
## v0.27 — 27.21 Example: sitemap

> **Source sections:** `CAP-844`

Suppose:

```
/sitemap.xml
```

contains:

```
100 URLs
```

The runtime establishes:

```
Enumeration:
    target = sitemap.xml
    entries = 100
    termination = end-of-document
```

That supports:

```
"The observed sitemap contained 100 entries."
```

It may support:

```
"The sitemap enumeration was exhausted."
```

It does **not automatically support**:

```
"The website contains exactly 100 resources."
```

because the sitemap may be incomplete.

This distinction is one of the most important properties of the system.

---

<!-- CAP-845 | Continue Architecture Planning.md L81137–81179 | turn 67 | version 0.27 -->
## v0.27 — 27.22 Enumeration → Coverage

> **Source sections:** `CAP-845`
>
> [DOCUMENTATION REVIEW] Contradiction **C-05** ([Review Notes](../REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified))

Now the earlier coverage machinery becomes connected.

```
EnumerationSnapshot
       ↓
EnumerationTermination
       ↓
CoverageRecord
       ↓
CoverageClaim
```

For example:

```JavaScript
{
    dimension: 'locator',
    status: 'exhaustive',
    explored: 100,
    estimatedTotal: 100,
    method: 'sitemap-enumeration',
    evidenceIds: [
        'enum-snapshot-1',
        'termination-1'
    ]
}
```

Notice:

```
coverage scope = sitemap
```

not:

```
coverage scope = entire web origin
```

---

<!-- CAP-846 | Continue Architecture Planning.md L81181–81237 | turn 67 | version 0.27 -->
## v0.27 — 27.23 Enumeration and negative evidence

> **Source sections:** `CAP-846`

v0.23 becomes more powerful here.

Suppose:

```
CompleteEnumeration(S)
```

and:

```
x ∉ S
```

Then we can establish:

```
¬Contains(S,x)
```

This is **negative evidence**.

But again:

```
¬Contains(S,x)
    ⇏
¬Exists(x,Universe)
```

unless:

```
S ≡ Universe
```

under a valid enumeration contract.

This gives us a rigorous bridge:

```
Enumerator
    ↓
Positive entries
    ↓
Candidate proposals

Enumerator
    ↓
Complete enumeration
    ↓
Negative evidence
```

---

<!-- CAP-847 | Continue Architecture Planning.md L81239–81278 | turn 67 | version 0.27 -->
## v0.27 — 27.24 Enumeration budget

> **Source sections:** `CAP-847`

Enumeration introduces another potential runaway:

```
API returns millions of entries
```

Therefore:

```JavaScript
{
    maxPages: 100,
    maxEntries: 5000,
    maxBytes: 50_000_000,
    maxElapsedMs: 60_000
}
```

When the budget ends:

```
BUDGET_EXHAUSTED
```

not:

```
EXHAUSTED
```

and certainly not:

```
COMPLETE
```

This is a hard semantic distinction.

---

<!-- CAP-848 | Continue Architecture Planning.md L81280–81314 | turn 67 | version 0.27 -->
## v0.27 — 27.25 Enumeration termination states

> **Source sections:** `CAP-848`
>
> [DOCUMENTATION REVIEW] Contradiction **C-09** ([Review Notes](../REVIEW-NOTES.md#c-09--two-termination-taxonomies))

Use explicit states:

```
EXHAUSTED
BUDGET_EXHAUSTED
CANCELLED
FAILED
INCOMPLETE
INVALID
UNKNOWN
```

Only:

```
EXHAUSTED
```

means the enumerator itself reached its termination condition.

Even then:

```
EXHAUSTED
```

does not necessarily mean:

```
COMPLETE
```

---

<!-- CAP-849 | Continue Architecture Planning.md L81316–81348 | turn 67 | version 0.27 -->
## v0.27 — 27.26 Enumeration accounting

> **Source sections:** `CAP-849`

An execution can now record:

```JavaScript
{
    pages: 17,
    entries: 482,
    uniqueEntries: 461,
    duplicateEntries: 21,

    candidatesProposed: 461,
    candidatesAccepted: 398,

    bytesObserved: 2400000,

    cursorAdvances: 17,

    retries: 2
}
```

These metrics become useful for:

```
adaptive strategy selection
cost modeling
coverage
diagnostics
replay
```

---

<!-- CAP-850 | Continue Architecture Planning.md L81350–81397 | turn 67 | version 0.27 -->
## v0.27 — 27.27 Enumeration provenance

> **Source sections:** `CAP-850`

A candidate should be traceable all the way back:

```
Candidate
   ↑
EnumerationEntry
   ↑
EnumerationPage
   ↑
EnumerationExecution
   ↑
QueryStep
   ↑
QueryPlan
   ↑
Goal
```

For example:

```JavaScript
{
    provenance: {
        goalId: 'goal-1',
        planId: 'plan-4',
        stepId: 'step-2',

        executionId: 'enum-exec-8',

        enumeratorId: 'sitemap',
        enumeratorVersion: '1.1',

        snapshotId: 'snapshot-12',
        pageSequence: 7,
        entryPosition: 42
    }
}
```

This is much stronger than:

```
foundBy = "sitemap"
```

---

<!-- CAP-851 | Continue Architecture Planning.md L81399–81425 | turn 67 | version 0.27 -->
## v0.27 — 27.28 Enumeration replay

> **Source sections:** `CAP-851`
>
> [DOCUMENTATION REVIEW] Contradiction **C-08** ([Review Notes](../REVIEW-NOTES.md#c-08--replay-decisions-deterministic-network-not))

A deterministic enumerator can be replayed from:

```
target
enumerator version
snapshot/artifact
cursor
configuration
```

For live network enumeration, exact replay is not guaranteed.

Therefore:

```
Decision replay
    may be deterministic

Network replay
    may not be
```

This distinction was already established for the broader system.

---

<!-- CAP-867 | Continue Architecture Planning.md L81608–81646 | turn 67 | version 0.27 -->
## v0.27 takeaway

> **Source sections:** `CAP-867`

The architecture now has a proper bridge between **search tactics** and **coverage claims**:

```
Goal
 ↓
Query Plan
 ↓
Tactic Execution
 ↓
Enumeration Runtime
 ↓
Enumerator
 ↓
Pages / Entries
 ↓
Candidates
```

while simultaneously producing:

```
Enumeration
 ↓
Snapshot
 ↓
Termination Evidence
 ↓
Coverage
 ↓
Completeness Assessment
```

The next unresolved problem is no longer enumeration itself.

It is **how multiple enumerators and strategies cooperate over overlapping search spaces without repeatedly scanning the same region or accidentally treating overlap as independent coverage**.

That leads naturally to:
