# Goal-Constrained Discovery and Query Planning

> **Status:** DESIGNED
>
> **Source:** `Continue Architecture Planning.md`
>
> **Purpose:** Search goals, relevance, goal-constrained discovery and the query planner and tactic runtime.

## Source Sections

- **v0.24 — Query/Goal-Constrained Discovery** — `CAP-679` — `Continue Architecture Planning.md` L75325–75390
- **v0.24 — Query/Goal-Constrained Discovery** — `CAP-681` — `Continue Architecture Planning.md` L75402–75455
- **v0.24 — 24.1 SearchGoal** — `CAP-682` — `Continue Architecture Planning.md` L75457–75517
- **v0.24 — 24.2 Goal ≠ Domain** — `CAP-683` — `Continue Architecture Planning.md` L75519–75568
- **v0.24 — 24.3 Goal constraints** — `CAP-684` — `Continue Architecture Planning.md` L75570–75622
- **v0.24 — 24.4 Hard constraints vs soft preferences** — `CAP-685` — `Continue Architecture Planning.md` L75624–75662
- **v0.24 — 24.5 GoalConstraint** — `CAP-686` — `Continue Architecture Planning.md` L75664–75710
- **v0.24 — 24.6 Relevance is not classification** — `CAP-687` — `Continue Architecture Planning.md` L75712–75752
- **v0.24 — 24.7 RelevanceAssertion** — `CAP-688` — `Continue Architecture Planning.md` L75754–75812
- **v0.24 — 24.8 Why `UNKNOWN` matters** — `CAP-689` — `Continue Architecture Planning.md` L75814–75860
- **v0.24 — 24.9 Relevance scoring** — `CAP-690` — `Continue Architecture Planning.md` L75862–75908
- **v0.24 — 24.10 The six questions** — `CAP-691` — `Continue Architecture Planning.md` L75910–75925
- **v0.24 — 24.11 Relevant Search Space** — `CAP-692` — `Continue Architecture Planning.md` L75927–75978
- **v0.24 — 24.12 Example** — `CAP-693` — `Continue Architecture Planning.md` L75980–76037
- **v0.24 — 24.13 Goal-directed adaptive discovery** — `CAP-694` — `Continue Architecture Planning.md` L76039–76091
- **v0.24 — 24.14 Expected Goal Value** — `CAP-695` — `Continue Architecture Planning.md` L76093–76140
- **v0.24 — 24.15 Information gain** — `CAP-696` — `Continue Architecture Planning.md` L76142–76172
- **v0.24 — 24.16 Goal-aware partition scoring** — `CAP-697` — `Continue Architecture Planning.md` L76174–76215
- **v0.24 — 24.17 Goal does not grant authority** — `CAP-698` — `Continue Architecture Planning.md` L76217–76267
- **v0.24 — 24.18 Goal provenance** — `CAP-699` — `Continue Architecture Planning.md` L76269–76307
- **v0.24 — 24.19 Goal-aware discovery event** — `CAP-700` — `Continue Architecture Planning.md` L76309–76352
- **v0.24 — 24.20 Goal lifecycle** — `CAP-701` — `Continue Architecture Planning.md` L76354–76400
- **v0.24 — 24.21 Goal termination policies** — `CAP-702` — `Continue Architecture Planning.md` L76402–76443
- **v0.24 — 24.22 Goal satisfaction vs completeness** — `CAP-703` — `Continue Architecture Planning.md` L76445–76481
- **v0.24 — 24.23 GoalResult** — `CAP-704` — `Continue Architecture Planning.md` L76483–76529
- **v0.24 — 24.24 Result ranking** — `CAP-705` — `Continue Architecture Planning.md` L76531–76577
- **v0.24 — 24.25 Result quality model** — `CAP-706` — `Continue Architecture Planning.md` L76579–76602
- **v0.24 — 24.26 Goal conflict** — `CAP-707` — `Continue Architecture Planning.md` L76604–76641
- **v0.24 — 24.27 Goal sessions** — `CAP-708` — `Continue Architecture Planning.md` L76643–76679
- **v0.24 — 24.28 Reuse of previous knowledge** — `CAP-709` — `Continue Architecture Planning.md` L76681–76720
- **v0.24 — 24.29 Knowledge reuse is not evidence reuse without qualification** — `CAP-710` — `Continue Architecture Planning.md` L76722–76761
- **v0.24 — 24.33 What v0.24 changes fundamentally** — `CAP-724` — `Continue Architecture Planning.md` L76977–77032
- **v0.25 — Discovery Query Planner** — `CAP-725` — `Continue Architecture Planning.md` L77034–77096
- **v0.25 — Discovery Query Planner** — `CAP-727` — `Continue Architecture Planning.md` L77108–77158
- **v0.25 — 25.1 Planner ≠ Search Engine** — `CAP-728` — `Continue Architecture Planning.md` L77160–77200
- **v0.25 — 25.2 QueryPlan** — `CAP-729` — `Continue Architecture Planning.md` L77202–77261
- **v0.25 — 25.3 QueryStep** — `CAP-730` — `Continue Architecture Planning.md` L77263–77321
- **v0.25 — 25.4 Query decomposition** — `CAP-731` — `Continue Architecture Planning.md` L77323–77363
- **v0.25 — 25.5 Search axes** — `CAP-732` — `Continue Architecture Planning.md` L77365–77401
- **v0.25 — 25.6 QueryTactic** — `CAP-733` — `Continue Architecture Planning.md` L77403–77440
- **v0.25 — 25.7 Tactic ≠ Strategy** — `CAP-734` — `Continue Architecture Planning.md` L77442–77479
- **v0.25 — 25.8 Planner plugins** — `CAP-735` — `Continue Architecture Planning.md` L77481–77517
- **v0.25 — 25.9 Planner contract** — `CAP-736` — `Continue Architecture Planning.md` L77519–77555
- **v0.25 — 25.10 Query plan example** — `CAP-737` — `Continue Architecture Planning.md` L77557–77592
- **v0.25 — 25.11 Dependencies** — `CAP-738` — `Continue Architecture Planning.md` L77594–77626
- **v0.25 — 25.12 Conditional planning** — `CAP-739` — `Continue Architecture Planning.md` L77628–77669
- **v0.25 — 25.13 Planning boundary** — `CAP-740` — `Continue Architecture Planning.md` L77671–77701
- **v0.25 — 25.14 Query plan validation** — `CAP-741` — `Continue Architecture Planning.md` L77703–77735
- **v0.25 — 25.15 Planner and adaptive discovery** — `CAP-742` — `Continue Architecture Planning.md` L77737–77765
- **v0.25 — 25.16 Exploration vs exploitation moves upward** — `CAP-743` — `Continue Architecture Planning.md` L77767–77801
- **v0.25 — 25.17 Query tactic performance** — `CAP-744` — `Continue Architecture Planning.md` L77803–77831
- **v0.25 — 25.18 Query planner provenance** — `CAP-745` — `Continue Architecture Planning.md` L77833–77877
- **v0.25 — 25.19 Query plan identity** — `CAP-746` — `Continue Architecture Planning.md` L77879–77907
- **v0.25 — 25.20 Plan versioning** — `CAP-747` — `Continue Architecture Planning.md` L77909–77940
- **v0.25 — 25.21 Planner cannot erase old work** — `CAP-748` — `Continue Architecture Planning.md` L77942–77973
- **v0.25 — 25.22 Query expansion** — `CAP-749` — `Continue Architecture Planning.md` L77975–78028
- **v0.25 — 25.23 Expansion evidence** — `CAP-750` — `Continue Architecture Planning.md` L78030–78052
- **v0.25 — 25.24 Planner hallucination boundary** — `CAP-751` — `Continue Architecture Planning.md` L78054–78084
- **v0.25 — 25.25 Search hypothesis** — `CAP-752` — `Continue Architecture Planning.md` L78086–78150
- **v0.25 — 25.27 Planner output is not execution** — `CAP-754` — `Continue Architecture Planning.md` L78202–78227
- **v0.25 — 25.28 Planner budget** — `CAP-755` — `Continue Architecture Planning.md` L78229–78269
- **v0.25 — 25.29 Three different budgets** — `CAP-756` — `Continue Architecture Planning.md` L78271–78300
- **v0.25 — 25.30 Termination propagation** — `CAP-757` — `Continue Architecture Planning.md` L78302–78348
- **v0.25 — 25.33 The resulting abstraction stack** — `CAP-761` — `Continue Architecture Planning.md` L78463–78546

## Related Documents

- [Strategies, Query Planning and Enumeration](strategy-and-planning.md)
- [Search Space](search-space.md)
- [Coverage, Completeness and Absence](coverage-and-absence.md)

---

<!-- CAP-679 | Continue Architecture Planning.md L75325–75390 | turn 59 | version 0.24 -->
## v0.24 — Query/Goal-Constrained Discovery

> **Source sections:** `CAP-679`

The next missing abstraction is now unavoidable.

So far, the engine knows:

```
WHERE may I search?
WHAT regions have I explored?
WHAT resources exist?
WHAT is absent?
HOW complete is the search?
```

But it does not yet formally know:

```
WHAT AM I TRYING TO FIND?
```

That distinction matters because a search for:

```
all resources
```

is fundamentally different from:

```
service manuals for Otis Gen2
```

and different again from:

```
all revisions of Gen2 service manuals published between 1995–2010
```

The next layer should therefore introduce:

```
                    SEARCH GOAL
                         │
             ┌───────────┼───────────┐
             │           │           │
          Target      Constraints   Relevance
             │           │           │
             └───────────┼───────────┘
                         ▼
                 RELEVANT SEARCH SPACE
                         │
                         ▼
                DISCOVERY STRATEGIES
                         │
                         ▼
                    COVERAGE
                         │
                         ▼
                  RESULT SET
```

This is where the generic engine can become **goal-directed without embedding domain-specific knowledge into its core**.

The crucial architectural rule for v0.24 should be:

> **The goal defines relevance; it must never weaken domain, capability, acquisition, policy, evidence, or completeness invariants.**

<!-- CAP-681 | Continue Architecture Planning.md L75402–75455 | turn 61 | version 0.24 -->
## v0.24 — Query/Goal-Constrained Discovery

> **Source sections:** `CAP-681`

v0.23 gave the engine the ability to reason about **presence, absence, and search assurance**.

But the engine still lacks a formal answer to:

> **Relevant to what?**

A generic discovery engine should not merely maximize discovered resources. It should maximize discovery **relative to an explicit search goal**.

The new abstraction is:

```
                         SEARCH GOAL
                              │
                              ▼
                    GOAL CONSTRAINTS
                              │
                              ▼
                    RELEVANCE MODEL
                              │
                              ▼
                    RELEVANT SEARCH SPACE
                              │
                              ▼
                    DISCOVERY / ACQUISITION
                              │
                              ▼
                         OBSERVATION
                              │
                              ▼
                    CLASSIFICATION
                              │
                              ▼
                      RELEVANCE EVIDENCE
                              │
                              ▼
                         RESULT SET
```

The crucial distinction is:

```
DISCOVERY
    = Can this resource be found?

RELEVANCE
    = Does this resource satisfy the current goal?

COMPLETENESS
    = Have we sufficiently explored the relevant search space?
```

---

<!-- CAP-682 | Continue Architecture Planning.md L75457–75517 | turn 61 | version 0.24 -->
## v0.24 — 24.1 SearchGoal

> **Source sections:** `CAP-682`

Introduce a first-class object.

```JavaScript
class SearchGoal {
    constructor(data = {}) {
        this.id = data.id || makeId('goal');

        this.name = data.name || null;

        this.target = data.target || null;

        this.constraints = data.constraints || {};

        this.preferences = data.preferences || {};

        this.relevanceModelId =
            data.relevanceModelId || null;

        this.domainId =
            data.domainId || null;

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
    name: 'Find service manuals',

    target: {
        resourceClass: 'technical-document'
    },

    constraints: {
        semanticTypes: [
            'service-manual'
        ]
    },

    preferences: {
        preferOfficialSources: true,
        preferNewestRevision: true
    }
}
```

Notice that the generic engine does not need to know what a `service-manual` means.

That belongs to a domain classifier/type registry.

---

<!-- CAP-683 | Continue Architecture Planning.md L75519–75568 | turn 61 | version 0.24 -->
## v0.24 — 24.2 Goal ≠ Domain

> **Source sections:** `CAP-683`

This distinction is essential.

```
DOMAIN
"What universe may I search?"

GOAL
"What am I trying to find within that universe?"
```

For example:

```
Domain
└── example.com
    ├── /docs/
    ├── /support/
    ├── /parts/
    └── /software/
```

Goal:

```
Find:
    technical documents
    semantic type = service-manual
```

Therefore:

```
Domain
    ⊇
Relevant Search Space
```

A goal must never expand the domain.

Formally:

```
RelevantSpace(goal, domain)
    ⊆
domain
```

---

<!-- CAP-684 | Continue Architecture Planning.md L75570–75622 | turn 61 | version 0.24 -->
## v0.24 — 24.3 Goal constraints

> **Source sections:** `CAP-684`

Constraints can operate on different dimensions.

```
SearchGoal
│
├── identity constraints
│
├── resource constraints
│
├── representation constraints
│
├── semantic constraints
│
├── source constraints
│
├── temporal constraints
│
├── geographic constraints
│
├── revision constraints
│
└── provenance constraints
```

Examples:

```JavaScript
{
    semanticTypes: ['service-manual'],

    representations: ['pdf'],

    source: {
        organizations: ['example-corp']
    },

    time: {
        before: '2015-01-01'
    },

    revision: {
        includeSuperseded: true
    }
}
```

The generic engine stores these as structured constraints.

Domain plugins interpret domain-specific fields.

---

<!-- CAP-685 | Continue Architecture Planning.md L75624–75662 | turn 61 | version 0.24 -->
## v0.24 — 24.4 Hard constraints vs soft preferences

> **Source sections:** `CAP-685`

Do not mix:

```
MUST
```

with:

```
PREFER
```

Introduce:

```
HardConstraint
SoftPreference
```

Example:

```
Goal
│
├── HARD
│   ├── semantic type = service-manual
│   └── organization = X
│
└── SOFT
    ├── official source preferred
    ├── newer revision preferred
    └── PDF preferred
```

This prevents a ranking preference from accidentally becoming an exclusion rule.

---

<!-- CAP-686 | Continue Architecture Planning.md L75664–75710 | turn 61 | version 0.24 -->
## v0.24 — 24.5 GoalConstraint

> **Source sections:** `CAP-686`

```JavaScript
class GoalConstraint {
    constructor(data = {}) {
        this.id = data.id || makeId('constraint');

        this.dimension =
            data.dimension || 'unknown';

        this.operator =
            data.operator || 'equals';

        this.value =
            data.value ?? null;

        this.mode =
            data.mode || 'hard';

        this.reason =
            data.reason || null;

        this.createdAt =
            data.createdAt || now();
    }
}
```

Examples:

```
dimension = semantic.type
operator  = equals
value     = service-manual
mode      = hard
```

or:

```
dimension = representation.format
operator  = prefers
value     = pdf
mode      = soft
```

---

<!-- CAP-687 | Continue Architecture Planning.md L75712–75752 | turn 61 | version 0.24 -->
## v0.24 — 24.6 Relevance is not classification

> **Source sections:** `CAP-687`

A resource may be classified as:

```
technical-document
```

without being relevant.

Likewise:

```
PDF
```

does not imply:

```
service-manual
```

Therefore:

```
Observation
   ↓
Classification
   ↓
Relevance Evaluation
```

not:

```
PDF
 ↓
Relevant = true
```

---

<!-- CAP-688 | Continue Architecture Planning.md L75754–75812 | turn 61 | version 0.24 -->
## v0.24 — 24.7 RelevanceAssertion

> **Source sections:** `CAP-688`

Introduce:

```JavaScript
class RelevanceAssertion {
    constructor(data = {}) {
        this.id = data.id || makeId('relevance');

        this.goalId =
            data.goalId || null;

        this.resourceId =
            data.resourceId || null;

        this.status =
            data.status || 'unknown';

        this.score =
            Number.isFinite(data.score)
                ? data.score
                : 0;

        this.matchedConstraints =
            data.matchedConstraints || [];

        this.failedConstraints =
            data.failedConstraints || [];

        this.evidenceIds =
            data.evidenceIds || [];

        this.evaluatorId =
            data.evaluatorId || null;

        this.evaluatorVersion =
            data.evaluatorVersion || null;

        this.createdAt =
            data.createdAt || now();
    }

    serialize() {
        return { ...this };
    }
}
```

Possible statuses:

```
RELEVANT
IRRELEVANT
POSSIBLY_RELEVANT
UNKNOWN
EXCLUDED
```

---

<!-- CAP-689 | Continue Architecture Planning.md L75814–75860 | turn 61 | version 0.24 -->
## v0.24 — 24.8 Why `UNKNOWN` matters

> **Source sections:** `CAP-689`

Suppose the engine finds:

```
manual.pdf
```

but the PDF cannot be downloaded.

It knows:

```
URL exists
```

It may know:

```
filename suggests manual
```

but it cannot inspect the document.

Therefore:

```
relevance = unknown
```

may be correct.

Not:

```
irrelevant
```

and not necessarily:

```
relevant
```

This preserves uncertainty.

---

<!-- CAP-690 | Continue Architecture Planning.md L75862–75908 | turn 61 | version 0.24 -->
## v0.24 — 24.9 Relevance scoring

> **Source sections:** `CAP-690`

A simple model might be:

```
score =
    evidence-supported matches
    -
    evidence-supported exclusions
```

But the engine should avoid embedding a universal formula.

Instead:

```JavaScript
class RelevanceEvaluator {
    canEvaluate(goal, resource, context) {
        return false;
    }

    evaluate(goal, resource, context) {
        throw new Error('Not implemented');
    }

    describe() {
        return {
            id: 'unknown-relevance-evaluator',
            name: 'Unknown Relevance Evaluator'
        };
    }
}
```

This mirrors the existing architecture:

```
CandidateSource
AcquisitionProvider
RecognitionProvider
Classifier
RelevanceEvaluator
```

Each answers a different question.

---

<!-- CAP-691 | Continue Architecture Planning.md L75910–75925 | turn 61 | version 0.24 -->
## v0.24 — 24.10 The six questions

> **Source sections:** `CAP-691`

The system now has a clean semantic separation:

| Component | Question |
| --- | --- |
| CandidateSource | Where might something exist? |
| AcquisitionProvider | How can I obtain it? |
| RecognitionProvider | What did I obtain? |
| Classifier | What kind of thing is it? |
| RelevanceEvaluator | Does it satisfy this goal? |
| CompletenessEvaluator | Can I justify that the relevant search is sufficiently complete? |

This is becoming a genuine discovery architecture rather than a crawler.

---

<!-- CAP-692 | Continue Architecture Planning.md L75927–75978 | turn 61 | version 0.24 -->
## v0.24 — 24.11 Relevant Search Space

> **Source sections:** `CAP-692`

The goal should derive a **view** over the domain.

```
DiscoveryDomain
       │
       ▼
SearchSpace
       │
       ▼
Goal
       │
       ▼
Relevance Constraints
       │
       ▼
RelevantSearchSpace
```

Introduce:

```JavaScript
class RelevantSearchSpace {
    constructor(data = {}) {
        this.id = data.id || makeId('relevant-space');

        this.goalId =
            data.goalId || null;

        this.domainId =
            data.domainId || null;

        this.partitionIds =
            data.partitionIds || [];

        this.constraintIds =
            data.constraintIds || [];

        this.createdAt =
            data.createdAt || now();
    }
}
```

Important:

> A relevant search space is not necessarily a smaller physical region.

It can be a **logical filter over the entire search space**.

---

<!-- CAP-693 | Continue Architecture Planning.md L75980–76037 | turn 61 | version 0.24 -->
## v0.24 — 24.12 Example

> **Source sections:** `CAP-693`

Suppose:

```
Domain
└── example.com
    ├── /docs/
    ├── /support/
    ├── /parts/
    ├── /software/
    └── /news/
```

Goal:

```
service manuals
```

The relevant-space estimator may initially produce:

```
HIGH relevance
├── /docs/
└── /support/

MEDIUM relevance
└── /parts/

LOW relevance
├── /software/
└── /news/
```

This does **not** mean the low-relevance partitions can be deleted.

Instead:

```
priority ↓
```

They remain searchable.

This is a crucial distinction between:

```
relevance prioritization
```

and:

```
hard exclusion
```

---

<!-- CAP-694 | Continue Architecture Planning.md L76039–76091 | turn 61 | version 0.24 -->
## v0.24 — 24.13 Goal-directed adaptive discovery

> **Source sections:** `CAP-694`

v0.21 already introduced adaptive strategy selection.

v0.24 adds goal relevance to the decision context.

The loop becomes:

```
Goal
 ↓
Relevant Search Space
 ↓
Partition
 ↓
Available Strategies
 ↓
Adaptive Strategy Score
 ↓
Expected Goal Value
 ↓
Exploration Plan
 ↓
Frontier
```

The score might conceptually include:

```
strategy value
+
historical yield
+
goal relevance
+
novelty
+
aging
-
cost
-
failure
```

But:

```
goal relevance
```

is still only a prioritization signal unless declared as a hard constraint.

---

<!-- CAP-695 | Continue Architecture Planning.md L76093–76140 | turn 61 | version 0.24 -->
## v0.24 — 24.14 Expected Goal Value

> **Source sections:** `CAP-695`

A useful new metric:

```
ExpectedGoalValue
```

Conceptually:

```
EGV =
P(relevant resource)
×
expected novelty
×
expected information gain
÷
expected cost
```

Do not treat this formula as canonical.

The important abstraction is:

```
strategy/partition
        ↓
expected value for current goal
```

This allows the engine to prefer:

```
partition A:
2 highly probable service manuals
```

over:

```
partition B:
50 generic PDFs
```

when the goal is service manuals.

---

<!-- CAP-696 | Continue Architecture Planning.md L76142–76172 | turn 61 | version 0.24 -->
## v0.24 — 24.15 Information gain

> **Source sections:** `CAP-696`

A discovery can be valuable even when it does not directly produce a result.

Example:

```
Search /support/
       ↓
find repository index
       ↓
repository contains 12,000 entries
```

The index itself may not satisfy the goal.

But it dramatically improves future discovery.

Therefore:

```
Goal Value
├── direct result value
├── search-space expansion value
├── classification value
└── evidence value
```

This prevents the adaptive engine from becoming excessively greedy.

---

<!-- CAP-697 | Continue Architecture Planning.md L76174–76215 | turn 61 | version 0.24 -->
## v0.24 — 24.16 Goal-aware partition scoring

> **Source sections:** `CAP-697`

Partition context can now contain:

```JavaScript
{
    partitionId,
    partitionKind,
    historicalYield,
    estimatedCost,

    goalContext: {
        relevancePrior: 0.82,
        expectedGoalValue: 0.76,
        informationGain: 0.63
    }
}
```

Then:

```
Adaptive Strategy
       │
       ├── historical performance
       ├── partition relevance
       ├── goal value
       ├── novelty
       ├── cost
       └── fairness
```

The optimizer still cannot bypass:

```
Domain
Policy
Capability
Budget
```

---

<!-- CAP-698 | Continue Architecture Planning.md L76217–76267 | turn 61 | version 0.24 -->
## v0.24 — 24.17 Goal does not grant authority

> **Source sections:** `CAP-698`

This needs an explicit invariant.

A malicious or poorly constructed goal cannot say:

```
"Find everything, including protected resources."
```

and thereby bypass policy.

The authorization ordering remains:

```
GOAL
  ↓
DOMAIN
  ↓
CAPABILITY
  ↓
POLICY
  ↓
BUDGET
  ↓
SCHEDULER
  ↓
ACQUISITION
```

More precisely:

```
Goal relevance
      │
      ▼
Search prioritization
```

while:

```
Policy authorization
      │
      ▼
Execution permission
```

remain separate.

---

<!-- CAP-699 | Continue Architecture Planning.md L76269–76307 | turn 61 | version 0.24 -->
## v0.24 — 24.18 Goal provenance

> **Source sections:** `CAP-699`

Every result should be traceable back to the goal that caused it to be selected.

```
Goal
 ↓
GoalConstraint
 ↓
RelevantSearchSpace
 ↓
Partition
 ↓
Strategy
 ↓
WorkItem
 ↓
Observation
 ↓
Evidence
 ↓
Resource
 ↓
Classification
 ↓
RelevanceAssertion
```

This provides **operational provenance**:

> Why did the system investigate this resource?

while v0.16 provided **epistemic provenance**:

> Why does the system believe this resource has these properties?

These should remain distinct.

---

<!-- CAP-700 | Continue Architecture Planning.md L76309–76352 | turn 61 | version 0.24 -->
## v0.24 — 24.19 Goal-aware discovery event

> **Source sections:** `CAP-700`

Extend the event ledger:

```
goal-created
goal-validated
goal-activated

goal-constraint-evaluated
goal-relevance-estimated

relevant-space-created
partition-goal-scored

goal-driven-strategy-selected

resource-relevance-evaluated
resource-marked-relevant
resource-marked-irrelevant
resource-relevance-unknown
```

Now a future audit can answer:

```
Why was resource R acquired?
```

Potential chain:

```
Goal G
 → partition P had relevance prior 0.82
 → strategy S selected
 → candidate C discovered
 → policy allowed
 → acquisition executed
 → observation O
 → classification service-manual
 → relevance assertion relevant
```

---

<!-- CAP-701 | Continue Architecture Planning.md L76354–76400 | turn 61 | version 0.24 -->
## v0.24 — 24.20 Goal lifecycle

> **Source sections:** `CAP-701`

A goal itself should have state.

```
CREATED
   ↓
VALIDATING
   ↓
ACTIVE
   ↓
SEARCHING
   ↓
DRAINING
   ↓
SATISFIED / EXHAUSTED / CANCELLED
```

But:

```
SATISFIED ≠ COMPLETE
```

Suppose the user asks:

```
"Find at least one service manual."
```

Once one valid result is found:

```
goal satisfied
```

The search can terminate.

But:

```
completeness = unknown
```

because the goal did not require exhaustive discovery.

---

<!-- CAP-702 | Continue Architecture Planning.md L76402–76443 | turn 61 | version 0.24 -->
## v0.24 — 24.21 Goal termination policies

> **Source sections:** `CAP-702`
>
> [DOCUMENTATION REVIEW] Contradiction **C-09** ([Review Notes](../REVIEW-NOTES.md#c-09--))

Introduce:

```JavaScript
{
    termination: {
        mode: 'first-match'
    }
}
```

Possible modes:

```
FIRST_MATCH
TOP_K
TARGET_COUNT
QUALITY_THRESHOLD
EXHAUSTIVE
TIME_LIMIT
COST_LIMIT
CUSTOM
```

This is important because not every search is exhaustive.

For example:

```
Goal:
"Find any valid service manual."
```

requires very different behavior from:

```
Goal:
"Enumerate every service manual in the defined repository."
```

---

<!-- CAP-703 | Continue Architecture Planning.md L76445–76481 | turn 61 | version 0.24 -->
## v0.24 — 24.22 Goal satisfaction vs completeness

> **Source sections:** `CAP-703`
>
> [DOCUMENTATION REVIEW] Contradiction **C-05** ([Review Notes](../REVIEW-NOTES.md#c-05--))

This distinction should be explicit:

```
Goal satisfaction
    =
Have we achieved the requested outcome?

Completeness
    =
Have we sufficiently explored the relevant universe?
```

Example:

```
Goal:
Find 3 service manuals.

Results:
R1
R2
R3
```

Then:

```
goal = SATISFIED
coverage = PARTIAL
completeness = NOT_ESTABLISHED
```

All three statements can be simultaneously true.

---

<!-- CAP-704 | Continue Architecture Planning.md L76483–76529 | turn 61 | version 0.24 -->
## v0.24 — 24.23 GoalResult

> **Source sections:** `CAP-704`

Introduce:

```JavaScript
class GoalResult {
    constructor(data = {}) {
        this.id = data.id || makeId('goal-result');

        this.goalId =
            data.goalId || null;

        this.resourceIds =
            data.resourceIds || [];

        this.relevanceAssertionIds =
            data.relevanceAssertionIds || [];

        this.status =
            data.status || 'incomplete';

        this.satisfaction =
            data.satisfaction || 'unsatisfied';

        this.coverage =
            data.coverage || null;

        this.completenessClaimId =
            data.completenessClaimId || null;

        this.createdAt =
            data.createdAt || now();
    }
}
```

Possible satisfaction states:

```
UNSATISFIED
PARTIALLY_SATISFIED
SATISFIED
EXHAUSTIVELY_SATISFIED
UNKNOWN
```

---

<!-- CAP-705 | Continue Architecture Planning.md L76531–76577 | turn 61 | version 0.24 -->
## v0.24 — 24.24 Result ranking

> **Source sections:** `CAP-705`

Once relevant resources exist, ranking becomes another layer.

```
Resource
    ↓
Relevance
    ↓
Evidence quality
    ↓
Revision quality
    ↓
Source quality
    ↓
Result ranking
```

Do not let ranking mutate relevance.

For example:

```
R1 relevance = 0.98
R2 relevance = 0.91
```

Ranking might still prefer R2 because:

```
R2
├── official source
├── newer revision
└── verified artifact
```

Therefore:

```
RELEVANCE
    ≠
QUALITY
    ≠
RANK
```

---

<!-- CAP-706 | Continue Architecture Planning.md L76579–76602 | turn 61 | version 0.24 -->
## v0.24 — 24.25 Result quality model

> **Source sections:** `CAP-706`

Eventually:

```
ResultQuality
├── relevance
├── evidence strength
├── provenance quality
├── source authority
├── artifact integrity
├── revision freshness
└── verification level
```

This is preferable to one opaque:

```
score = 0.94
```

The latter loses explanatory power.

---

<!-- CAP-707 | Continue Architecture Planning.md L76604–76641 | turn 61 | version 0.24 -->
## v0.24 — 24.26 Goal conflict

> **Source sections:** `CAP-707`

Two goals may coexist:

```
Goal A
Find newest manuals.

Goal B
Find historical manuals.
```

The same resource can be:

```
relevant to A
relevant to B
```

but ranked differently.

Or:

```
Goal A
exclude superseded revisions.

Goal B
include superseded revisions.
```

Therefore goal state must never mutate the underlying resource graph.

The graph stores facts and assertions.

Goals create **views over those facts**.

---

<!-- CAP-708 | Continue Architecture Planning.md L76643–76679 | turn 61 | version 0.24 -->
## v0.24 — 24.27 Goal sessions

> **Source sections:** `CAP-708`

A scan session should now optionally belong to a goal.

```JavaScript
class ScanSession {
    constructor(domain, options = {}) {
        this.id = makeId('scan');

        this.domainId = domain.id;

        this.goalId =
            options.goalId || null;

        // ...
    }
}
```

Thus:

```
Domain
   │
   ├── Scan A
   │     └── Goal A
   │
   ├── Scan B
   │     └── Goal B
   │
   └── Scan C
         └── no goal
```

The same resource graph can support all of them.

---

<!-- CAP-709 | Continue Architecture Planning.md L76681–76720 | turn 61 | version 0.24 -->
## v0.24 — 24.28 Reuse of previous knowledge

> **Source sections:** `CAP-709`
>
> [DOCUMENTATION REVIEW] Contradiction **C-10** ([Review Notes](../REVIEW-NOTES.md#c-10--))

This creates an important optimization.

Suppose:

```
Scan 1
Goal A
    ↓
discovers 5,000 resources
```

Later:

```
Scan 2
Goal B
```

The engine should not blindly reacquire everything.

Instead:

```
Existing Knowledge
        │
        ▼
Goal B Relevance Evaluation
        │
   ┌────┴────┐
   │         │
 relevant  unknown
   │         │
reuse      acquire
```

This is one of the major reasons the resource/evidence graph must be separated from individual scan sessions.

---

<!-- CAP-710 | Continue Architecture Planning.md L76722–76761 | turn 61 | version 0.24 -->
## v0.24 — 24.29 Knowledge reuse is not evidence reuse without qualification

> **Source sections:** `CAP-710`
>
> [DOCUMENTATION REVIEW] Contradiction **C-10** ([Review Notes](../REVIEW-NOTES.md#c-10--))

An old classification may still be useful:

```
service-manual
classifier v1
observed 2025
```

But it should not automatically prove:

```
service-manual
current artifact 2026
```

The engine therefore needs temporal/evidence freshness.

Conceptually:

```
Historical evidence
       ↓
Can inform
       ↓
Current search
```

but:

```
historical evidence
    ≠
current observation
```

unless the assertion's validity conditions allow reuse.

---

<!-- CAP-724 | Continue Architecture Planning.md L76977–77032 | turn 61 | version 0.24 -->
## v0.24 — 24.33 What v0.24 changes fundamentally

> **Source sections:** `CAP-724`

Before v0.24:

```
Search
  ↓
Find resources
```

After v0.24:

```
                    GOAL
                     │
                     ▼
             Define relevance
                     │
                     ▼
             Allocate search effort
                     │
                     ▼
                 Discover
                     │
                     ▼
               Gather evidence
                     │
                     ▼
             Evaluate relevance
                     │
                     ▼
                 Produce results
                     │
                     ▼
            Measure coverage
                     │
                     ▼
         Assess completeness
```

The system is now capable of **goal-directed discovery without making the generic core domain-specific**.

That is exactly the property needed for later plugging in things such as:

```
service-manual
parts-catalog
troubleshooting-guide
technical-bulletin
field-modification-notice
software-artifact
```

as domain knowledge rather than hardcoded crawler behavior.

---

<!-- CAP-725 | Continue Architecture Planning.md L77034–77096 | turn 61 | version 0.25 -->
## v0.25 — Discovery Query Planner

> **Source sections:** `CAP-725`

The next architectural boundary is the transition from:

```
Goal
  ↓
Relevance
```

to:

```
Goal
  ↓
Query decomposition
  ↓
Search tactics
  ↓
Multiple discovery paths
```

A sophisticated goal such as:

```
"Find every relevant service manual, including historical revisions,
from all accessible repositories."
```

cannot be represented efficiently as one search operation.

It needs decomposition into independent but coordinated tactics:

```
                         GOAL
                           │
                           ▼
                    QUERY PLANNER
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
        Source Search   Repository     Document
                         Search       Family Search
             │             │             │
             └─────────────┼─────────────┘
                           ▼
                     Search Tactics
                           │
                           ▼
                     Discovery Plans
                           │
                           ▼
                     Shared Frontier
                           │
                           ▼
                    Evidence / Results
```

The key question for v0.25 becomes:

> **How does one high-level discovery goal get decomposed into multiple bounded, auditable search strategies without turning the planner into an uncontrolled autonomous agent?**

That is the next missing layer.

<!-- CAP-727 | Continue Architecture Planning.md L77108–77158 | turn 63 | version 0.25 -->
## v0.25 — Discovery Query Planner

> **Source sections:** `CAP-727`

v0.24 established:

```
Goal → Relevance → Relevant Search Space
```

The next problem is decomposition.

A complex goal rarely maps to one discovery mechanism.

For example:

```
"Find all relevant service manuals, including historical revisions,
across all accessible repositories."
```

contains several distinct search problems:

```
                    GOAL
                      │
                      ▼
                QUERY PLANNER
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
   Source search   Repository    Document-family
                    search          search
        │             │             │
        └─────────────┼─────────────┘
                      ▼
                 Search Tactics
                      │
                      ▼
                Discovery Plans
                      │
                      ▼
                 Shared Frontier
```

The planner therefore becomes responsible for:

> **Turning a high-level goal into a finite, explicit set of search tactics without directly executing them.**

That last clause is important.

---

<!-- CAP-728 | Continue Architecture Planning.md L77160–77200 | turn 63 | version 0.25 -->
## v0.25 — 25.1 Planner ≠ Search Engine

> **Source sections:** `CAP-728`

The planner should not become another crawler.

Separate:

```
Query Planner
    = decide WHAT search operations should exist

Discovery Strategy
    = decide HOW a search operation explores its partition

Candidate Source
    = extract possible resources from observations

Acquisition Runtime
    = execute authorized I/O
```

So:

```
Goal
 ↓
Planner
 ↓
Search Plan
 ↓
Strategy
 ↓
WorkItem
 ↓
Acquisition
```

The planner creates work.

It does not execute work.

---

<!-- CAP-729 | Continue Architecture Planning.md L77202–77261 | turn 63 | version 0.25 -->
## v0.25 — 25.2 QueryPlan

> **Source sections:** `CAP-729`

Introduce:

```JavaScript
class QueryPlan {
    constructor(data = {}) {
        this.id = data.id || makeId('qplan');

        this.goalId =
            data.goalId || null;

        this.domainId =
            data.domainId || null;

        this.steps =
            data.steps || [];

        this.constraints =
            data.constraints || [];

        this.priority =
            Number.isFinite(data.priority)
                ? data.priority
                : 0;

        this.status =
            data.status || 'planned';

        this.plannerId =
            data.plannerId || null;

        this.plannerVersion =
            data.plannerVersion || null;

        this.createdAt =
            data.createdAt || now();
    }

    serialize() {
        return { ...this };
    }
}
```

A plan is declarative.

Example:

```
QueryPlan
├── source-discovery
├── repository-discovery
├── sitemap-expansion
├── document-family-search
├── revision-search
└── cross-reference-expansion
```

---

<!-- CAP-730 | Continue Architecture Planning.md L77263–77321 | turn 63 | version 0.25 -->
## v0.25 — 25.3 QueryStep

> **Source sections:** `CAP-730`

Each plan contains explicit steps.

```JavaScript
class QueryStep {
    constructor(data = {}) {
        this.id = data.id || makeId('qstep');

        this.planId =
            data.planId || null;

        this.kind =
            data.kind || 'unknown';

        this.target =
            data.target || null;

        this.constraints =
            data.constraints || {};

        this.dependsOn =
            data.dependsOn || [];

        this.priority =
            Number.isFinite(data.priority)
                ? data.priority
                : 0;

        this.status =
            data.status || 'planned';

        this.createdAt =
            data.createdAt || now();
    }

    serialize() {
        return { ...this };
    }
}
```

Examples:

```
QueryStep
kind = repository-discovery
target = domain-root
```

or:

```
QueryStep
kind = revision-discovery
target = resource-family
```

---

<!-- CAP-731 | Continue Architecture Planning.md L77323–77363 | turn 63 | version 0.25 -->
## v0.25 — 25.4 Query decomposition

> **Source sections:** `CAP-731`

A planner takes:

```
SearchGoal
```

and produces:

```
QueryPlan
```

Conceptually:

```
                    GOAL
                      │
                      ▼
                 PARSE GOAL
                      │
                      ▼
             EXTRACT CONSTRAINTS
                      │
                      ▼
             IDENTIFY SEARCH AXES
                      │
                      ▼
              GENERATE TACTICS
                      │
                      ▼
             CHECK DOMAIN/POLICY
                      │
                      ▼
                QUERY PLAN
```

The planner should be deterministic for the same inputs.

---

<!-- CAP-732 | Continue Architecture Planning.md L77365–77401 | turn 63 | version 0.25 -->
## v0.25 — 25.5 Search axes

> **Source sections:** `CAP-732`

A useful abstraction is the **search axis**.

```
SearchGoal
│
├── source axis
├── repository axis
├── locator axis
├── document-family axis
├── semantic axis
├── revision axis
├── temporal axis
└── relationship axis
```

For example:

```
Goal:
Find service manuals

Search axes:
├── where might documents live?
├── what repositories expose them?
├── what document families exist?
├── what historical names were used?
├── what revisions exist?
└── what documents reference other documents?
```

The generic planner does not need to know domain semantics.

It asks registered planners/plugins to expose applicable axes.

---

<!-- CAP-733 | Continue Architecture Planning.md L77403–77440 | turn 63 | version 0.25 -->
## v0.25 — 25.6 QueryTactic

> **Source sections:** `CAP-733`

Introduce a reusable tactic abstraction.

```JavaScript
class QueryTactic {
    canPlan(goal, context) {
        return false;
    }

    plan(goal, context) {
        throw new Error('Not implemented');
    }

    describe() {
        return {
            id: 'unknown-tactic',
            name: 'Unknown Query Tactic'
        };
    }
}
```

Examples:

```
SeedExpansionTactic
RepositoryDiscoveryTactic
SitemapTactic
DocumentFamilyTactic
RevisionTactic
CrossReferenceTactic
MetadataTactic
```

These produce `QueryStep`s.

---

<!-- CAP-734 | Continue Architecture Planning.md L77442–77479 | turn 63 | version 0.25 -->
## v0.25 — 25.7 Tactic ≠ Strategy

> **Source sections:** `CAP-734`

This distinction becomes important.

```
TACTIC
"What kind of search should we perform?"

STRATEGY
"How do we explore the selected search region?"

SOURCE
"How do we extract candidates from evidence?"
```

Example:

```
Tactic:
RepositoryDiscovery

        ↓

Strategy:
RepositoryExpansionStrategy

        ↓

Observation:
repository-index.json

        ↓

CandidateSource:
JsonUrlSource
```

---

<!-- CAP-735 | Continue Architecture Planning.md L77481–77517 | turn 63 | version 0.25 -->
## v0.25 — 25.8 Planner plugins

> **Source sections:** `CAP-735`

The generic planner should support domain-independent and domain-specific plugins.

```
                    QUERY PLANNER
                         │
        ┌────────────────┼────────────────┐
        │                │                │
     Generic          Domain           User
     Tactics          Tactics          Tactics
        │                │                │
        └────────────────┼────────────────┘
                         ▼
                    QueryPlan
```

For example:

```
Generic:
├── sitemap
├── robots
├── links
├── metadata
└── repository-index

Domain:
├── service-manual family
├── parts-catalog family
├── bulletin family
└── revision terminology
```

The generic core remains unchanged.

---

<!-- CAP-736 | Continue Architecture Planning.md L77519–77555 | turn 63 | version 0.25 -->
## v0.25 — 25.9 Planner contract

> **Source sections:** `CAP-736`

```JavaScript
class QueryPlanner {
    tactics() {
        return [];
    }

    canPlan(goal, context) {
        return true;
    }

    plan(goal, context) {
        throw new Error('Not implemented');
    }

    describe() {
        return {
            id: 'unknown-planner',
            name: 'Unknown Query Planner'
        };
    }
}
```

The planner should return facts about the proposed search, not mutate:

```
KnowledgeBase
Scheduler
Policy
ResourceGraph
```

This keeps planning pure enough to inspect and audit.

---

<!-- CAP-737 | Continue Architecture Planning.md L77557–77592 | turn 63 | version 0.25 -->
## v0.25 — 25.10 Query plan example

> **Source sections:** `CAP-737`

Suppose:

```
Goal:
Find all relevant technical documents.
```

The planner might generate:

```
QueryPlan
│
├── Step 1
│   └── inspect robots.txt
│
├── Step 2
│   └── inspect sitemap indexes
│
├── Step 3
│   └── inspect discovered repositories
│
├── Step 4
│   └── expand document-family terminology
│
├── Step 5
│   └── follow technical-document references
│
└── Step 6
    └── search revision relationships
```

Each step becomes independently auditable.

---

<!-- CAP-738 | Continue Architecture Planning.md L77594–77626 | turn 63 | version 0.25 -->
## v0.25 — 25.11 Dependencies

> **Source sections:** `CAP-738`

Some query steps depend on previous discoveries.

For example:

```
robots
   ↓
sitemap
   ↓
repository
   ↓
document family
   ↓
revision search
```

Represent this explicitly:

```JavaScript
{
    id: 'step-4',
    dependsOn: [
        'step-2',
        'step-3'
    ]
}
```

Then the planner does not pretend it knows resources that have not yet been discovered.

---

<!-- CAP-739 | Continue Architecture Planning.md L77628–77669 | turn 63 | version 0.25 -->
## v0.25 — 25.12 Conditional planning

> **Source sections:** `CAP-739`

A more interesting case:

```
IF repository discovered
    THEN generate repository enumeration step

IF sitemap discovered
    THEN generate sitemap expansion

IF document index discovered
    THEN generate index traversal
```

This introduces:

```
STATIC PLAN
+
CONDITIONAL PLAN EXPANSION
```

The planner therefore has two modes:

```
Initial planning
    ↓
initial QueryPlan

Execution
    ↓
new evidence
    ↓
conditional planning
    ↓
new QuerySteps
```

But this must not become unconstrained self-modification.

---

<!-- CAP-740 | Continue Architecture Planning.md L77671–77701 | turn 63 | version 0.25 -->
## v0.25 — 25.13 Planning boundary

> **Source sections:** `CAP-740`

A strict boundary:

```
Evidence
   ↓
Planner
   ↓
Proposal for new work
   ↓
Policy/domain validation
   ↓
Frontier admission
```

The planner cannot directly inject:

```
RUN THIS REQUEST
```

It can only propose:

```
EXPLORE THIS REGION
```

The normal admission chain remains mandatory.

---

<!-- CAP-741 | Continue Architecture Planning.md L77703–77735 | turn 63 | version 0.25 -->
## v0.25 — 25.14 Query plan validation

> **Source sections:** `CAP-741`
>
> [DOCUMENTATION REVIEW] Contradiction **C-02** ([Review Notes](../REVIEW-NOTES.md#c-02--))

Before execution:

```
QueryPlan
   ↓
PlanValidator
   ├── domain
   ├── capabilities
   ├── policy
   ├── budgets
   ├── dependencies
   └── termination
```

Introduce:

```JavaScript
class QueryPlanValidator {
    validate(plan, context) {
        return {
            valid: true,
            errors: [],
            warnings: []
        };
    }
}
```

This prevents the planner from becoming an authority boundary.

---

<!-- CAP-742 | Continue Architecture Planning.md L77737–77765 | turn 63 | version 0.25 -->
## v0.25 — 25.15 Planner and adaptive discovery

> **Source sections:** `CAP-742`

v0.21 selected strategies adaptively.

Now the hierarchy becomes:

```
Goal
 ↓
Query Planner
 ↓
Query Tactic
 ↓
Relevant Partition
 ↓
Adaptive Strategy Selector
 ↓
Strategy
 ↓
WorkItem
```

This is cleaner than allowing the adaptive selector to invent arbitrary searches.

The planner defines the **space of legitimate tactics**.

The adaptive layer selects among them.

---

<!-- CAP-743 | Continue Architecture Planning.md L77767–77801 | turn 63 | version 0.25 -->
## v0.25 — 25.16 Exploration vs exploitation moves upward

> **Source sections:** `CAP-743`

Previously:

```
Strategy selection
```

handled exploration/exploitation.

Now there are two levels:

```
PLAN LEVEL
├── Which search tactics should exist?
│
└── Which tactic deserves exploration?

STRATEGY LEVEL
├── Which strategy should explore it?
│
└── How should the partition be probed?
```

Therefore:

```
exploration/exploitation
```

should not be implemented as one global score.

There are multiple decision layers.

---

<!-- CAP-744 | Continue Architecture Planning.md L77803–77831 | turn 63 | version 0.25 -->
## v0.25 — 25.17 Query tactic performance

> **Source sections:** `CAP-744`

A planner can eventually track:

```
TacticPerformance
├── attempts
├── relevantResources
├── newPartitions
├── newRepositories
├── newArtifacts
├── usefulEvidence
├── cost
└── failures
```

Then:

```
Tactic selection
```

can become adaptive too.

But the same rule from v0.21 applies:

> Historical performance is evidence, not authority.

---

<!-- CAP-745 | Continue Architecture Planning.md L77833–77877 | turn 63 | version 0.25 -->
## v0.25 — 25.18 Query planner provenance

> **Source sections:** `CAP-745`

Every generated step should explain why it exists.

```JavaScript
{
    stepId: 'step-42',

    tacticId: 'repository-discovery',

    goalId: 'goal-1',

    reason: {
        constraintIds: [
            'constraint-source',
            'constraint-semantic'
        ],

        evidenceIds: [
            'evidence-99'
        ]
    }
}
```

Then:

```
Why did the engine search repository R?
```

can be answered:

```
Goal G
 → tactic T
 → evidence E
 → plan step S
 → work item W
 → observation O
```

This is operational provenance.

---

<!-- CAP-746 | Continue Architecture Planning.md L77879–77907 | turn 63 | version 0.25 -->
## v0.25 — 25.19 Query plan identity

> **Source sections:** `CAP-746`
>
> [DOCUMENTATION REVIEW] Contradiction **C-04** ([Review Notes](../REVIEW-NOTES.md#c-04--))

Plans and executions must remain separate.

```
QueryPlan
   │
   ├── Execution 1
   ├── Execution 2
   └── Execution 3
```

A planner may produce:

```
plan-v1
```

and later:

```
plan-v2
```

after new evidence.

Do not mutate historical plans.

---

<!-- CAP-747 | Continue Architecture Planning.md L77909–77940 | turn 63 | version 0.25 -->
## v0.25 — 25.20 Plan versioning

> **Source sections:** `CAP-747`

```JavaScript
{
    planId: 'qplan-1',
    version: 2,

    parentPlanId: 'qplan-1',
    parentVersion: 1,

    reason: {
        trigger: 'new-repository-discovered',
        evidenceIds: ['ev-88']
    }
}
```

This gives:

```
Plan v1
   ↓
new evidence
   ↓
Plan v2
   ↓
new work
```

Historical execution remains reproducible.

---

<!-- CAP-748 | Continue Architecture Planning.md L77942–77973 | turn 63 | version 0.25 -->
## v0.25 — 25.21 Planner cannot erase old work

> **Source sections:** `CAP-748`

Suppose v1 says:

```
search sitemap
search repository
```

v2 says:

```
repository is irrelevant
```

The old execution remains in the ledger.

The planner can:

```
cancel future work
```

but cannot rewrite:

```
historical decisions
observations
evidence
```

---

<!-- CAP-749 | Continue Architecture Planning.md L77975–78028 | turn 63 | version 0.25 -->
## v0.25 — 25.22 Query expansion

> **Source sections:** `CAP-749`

A query may generate new search terms.

For example:

```
service manual
```

could eventually produce:

```
service manual
maintenance manual
technical manual
field manual
workshop manual
```

But the generic planner should not invent semantic synonyms.

Instead:

```
Domain knowledge provider
        ↓
QueryExpansionProvider
        ↓
Expansion proposals
```

Contract:

```JavaScript
class QueryExpansionProvider {
    canExpand(goal, context) {
        return false;
    }

    expand(goal, context) {
        return [];
    }

    describe() {
        return {
            id: 'unknown-expander',
            name: 'Unknown Query Expansion Provider'
        };
    }
}
```

---

<!-- CAP-750 | Continue Architecture Planning.md L78030–78052 | turn 63 | version 0.25 -->
## v0.25 — 25.23 Expansion evidence

> **Source sections:** `CAP-750`

An expansion should have provenance.

```JavaScript
{
    sourceTerm: 'service manual',

    expandedTerm: 'maintenance manual',

    providerId: 'domain-terminology',

    evidenceIds: [
        'ontology-17'
    ],

    confidence: 0.81
}
```

This prevents a language model from silently generating arbitrary search vocabulary and presenting it as domain truth.

---

<!-- CAP-751 | Continue Architecture Planning.md L78054–78084 | turn 63 | version 0.25 -->
## v0.25 — 25.24 Planner hallucination boundary

> **Source sections:** `CAP-751`

This is one of the most important failure modes.

A planner may generate:

```
"/service/manuals/"
```

simply because that path seems plausible.

That does **not** make it a discovered resource.

Therefore:

```
PLANNER HYPOTHESIS
    ≠
CANDIDATE
```

A hypothetical target must be marked:

```
proposalType = 'hypothesis'
```

and pass the normal candidate validation process.

---

<!-- CAP-752 | Continue Architecture Planning.md L78086–78150 | turn 63 | version 0.25 -->
## v0.25 — 25.25 Search hypothesis

> **Source sections:** `CAP-752`

Introduce:

```JavaScript
class SearchHypothesis {
    constructor(data = {}) {
        this.id = data.id || makeId('hypothesis');

        this.goalId =
            data.goalId || null;

        this.target =
            data.target || null;

        this.kind =
            data.kind || 'unknown';

        this.reason =
            data.reason || null;

        this.evidenceIds =
            data.evidenceIds || [];

        this.confidence =
            Number.isFinite(data.confidence)
                ? data.confidence
                : 0;

        this.status =
            data.status || 'proposed';

        this.createdAt =
            data.createdAt || now();
    }
}
```

Lifecycle:

```
PROPOSED
   ↓
VALIDATED
   ↓
ADMITTED
   ↓
TESTED
   ↓
SUPPORTED / REJECTED / UNKNOWN
```

This provides a clean boundary between:

```
inference
```

and:

```
observation
```

---

<!-- CAP-754 | Continue Architecture Planning.md L78202–78227 | turn 63 | version 0.25 -->
## v0.25 — 25.27 Planner output is not execution

> **Source sections:** `CAP-754`

The clean contract is:

```
                 QUERY PLANNER
                       │
                       ▼
                   QueryPlan
                       │
                       ▼
                Plan Validator
                       │
                       ▼
                 Work Proposals
                       │
                       ▼
                Frontier Runtime
                       │
                       ▼
                 Actual Work
```

This is important for security and reproducibility.

---

<!-- CAP-755 | Continue Architecture Planning.md L78229–78269 | turn 63 | version 0.25 -->
## v0.25 — 25.28 Planner budget

> **Source sections:** `CAP-755`

Planning itself must be bounded.

Otherwise:

```
goal
 ↓
query expansion
 ↓
new tactic
 ↓
new query
 ↓
new tactic
 ↓
...
```

can become infinite.

Introduce:

```JavaScript
{
    maxPlanSteps: 100,
    maxExpansionDepth: 4,
    maxHypotheses: 200,
    maxConditionalExpansions: 50
}
```

These are **planning budgets**, separate from:

```
discovery budget
acquisition budget
```

---

<!-- CAP-756 | Continue Architecture Planning.md L78271–78300 | turn 63 | version 0.25 -->
## v0.25 — 25.29 Three different budgets

> **Source sections:** `CAP-756`

We now have:

```
PLANNING BUDGET
    "How much search planning may occur?"

DISCOVERY BUDGET
    "How much candidate generation may occur?"

ACQUISITION BUDGET
    "How much external I/O may occur?"
```

Never collapse them.

For example:

```
10 planning steps
→
500 discovery proposals
→
100 acquisitions
```

is perfectly valid.

---

<!-- CAP-757 | Continue Architecture Planning.md L78302–78348 | turn 63 | version 0.25 -->
## v0.25 — 25.30 Termination propagation

> **Source sections:** `CAP-757`
>
> [DOCUMENTATION REVIEW] Contradiction **C-09** ([Review Notes](../REVIEW-NOTES.md#c-09--))

Goal termination must propagate through the plan.

```
Goal satisfied
      ↓
Query plan
      ↓
future work admission stops
      ↓
frontier drains
      ↓
session terminates
```

But if the goal is:

```
EXHAUSTIVE
```

then:

```
Goal satisfied
```

does not terminate until:

```
relevant search space
+
required completeness conditions
```

are satisfied.

Thus:

```
Termination policy
```

must be attached to the goal.

---

<!-- CAP-761 | Continue Architecture Planning.md L78463–78546 | turn 63 | version 0.25 -->
## v0.25 — 25.33 The resulting abstraction stack

> **Source sections:** `CAP-761`

After v0.25, the system has a fairly clean hierarchy:

```
                    USER / APPLICATION
                           │
                           ▼
                         GOAL
                           │
                           ▼
                    QUERY PLANNER
                           │
                           ▼
                      QUERY PLAN
                           │
                           ▼
                  RELEVANT SEARCH SPACE
                           │
                           ▼
                 DISCOVERY STRATEGIES
                           │
                           ▼
                    FRONTIER RUNTIME
                           │
                           ▼
                  ACQUISITION RUNTIME
                           │
                           ▼
                  ACQUISITION PROVIDER
                           │
                           ▼
                      OBSERVATION
                           │
                           ▼
                 RECOGNITION RUNTIME
                           │
                           ▼
                       EVIDENCE
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
         RESOURCE                  CLASSIFICATION
             │                           │
             └─────────────┬─────────────┘
                           ▼
                       RELEVANCE
                           │
                           ▼
                       RESULTS
                           │
                 ┌─────────┴─────────┐
                 ▼                   ▼
             COVERAGE           COMPLETENESS
```

And beneath all of it:

```
             DOMAIN
                │
             POLICY
                │
           CAPABILITIES
                │
             BUDGETS
                │
           FRONTIER
                │
            EXECUTION
```

with:

```
EVENT LEDGER
EVIDENCE GRAPH
RESOURCE GRAPH
SEARCH/COVERAGE GRAPH
```

as persistent explanatory structures.

---
