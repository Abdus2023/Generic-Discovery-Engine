# Coverage, Completeness and Absence

> **Status:** DESIGNED
>
> **Source:** `Continue Architecture Planning.md`; `Userscript Discovery Prototype.md`
>
> **Purpose:** Coverage measurement, completeness claims, negative evidence and absence reasoning.

## Source Sections

- **19. Coverage is a better metric than elapsed time** — `USP-034` — `Userscript Discovery Prototype.md` L917–949
- **v0.22 — Discovery Completeness + Coverage Claims** — `CAP-599` — `Continue Architecture Planning.md` L72638–72695
- **v0.22 — Discovery Completeness + Coverage Claims** — `CAP-601` — `Continue Architecture Planning.md` L72707–72717
- **v0.22 — 22.1 The problem** — `CAP-602` — `Continue Architecture Planning.md` L72719–72763
- **v0.22 — 22.2 Search-space state model** — `CAP-603` — `Continue Architecture Planning.md` L72765–72815
- **v0.22 — 22.3 Coverage is a measurement** — `CAP-604` — `Continue Architecture Planning.md` L72817–72852
- **v0.22 — 22.4 Coverage dimensions** — `CAP-605` — `Continue Architecture Planning.md` L72854–72906
- **v0.22 — 22.5 CoverageRecord** — `CAP-606` — `Continue Architecture Planning.md` L72908–72980
- **v0.22 — 22.6 Coverage state** — `CAP-607` — `Continue Architecture Planning.md` L72982–73020
- **v0.22 — 22.7 CoverageClaim** — `CAP-608` — `Continue Architecture Planning.md` L73022–73075
- **v0.22 — 22.8 Completeness is a stronger assertion** — `CAP-609` — `Continue Architecture Planning.md` L73077–73131
- **v0.22 — 22.9 The finite-enumerator case** — `CAP-610` — `Continue Architecture Planning.md` L73133–73193
- **v0.22 — 22.10 Enumeration contract** — `CAP-611` — `Continue Architecture Planning.md` L73195–73249
- **v0.22 — 22.11 Negative evidence** — `CAP-612` — `Continue Architecture Planning.md` L73251–73323
- **v0.22 — 22.12 Absence reasoning hierarchy** — `CAP-613` — `Continue Architecture Planning.md` L73325–73365
- **v0.22 — 22.13 “Not found” becomes a first-class result** — `CAP-614` — `Continue Architecture Planning.md` L73367–73401
- **v0.22 — 22.14 Coverage cannot necessarily be monotonically interpreted** — `CAP-615` — `Continue Architecture Planning.md` L73403–73459
- **v0.22 — 22.15 Version the search universe** — `CAP-616` — `Continue Architecture Planning.md` L73461–73507
- **v0.22 — 22.16 Coverage ledger** — `CAP-617` — `Continue Architecture Planning.md` L73509–73550
- **v0.22 — 22.17 Three graphs now interact** — `CAP-618` — `Continue Architecture Planning.md` L73552–73607
- **v0.22 — 22.18 Completeness assessment** — `CAP-619` — `Continue Architecture Planning.md` L73609–73663
- **v0.22 — 22.20 Search completeness matrix** — `CAP-621` — `Continue Architecture Planning.md` L73699–73713
- **v0.22 — 22.21 Coverage calculation** — `CAP-622` — `Continue Architecture Planning.md` L73715–73761
- **v0.22 — 22.22 Coverage should be query-relative** — `CAP-623` — `Continue Architecture Planning.md` L73763–73807
- **v0.23 — Negative Evidence + Absence Reasoning** — `CAP-638` — `Continue Architecture Planning.md` L74029–74056
- **v0.23 — Negative Evidence + Absence Reasoning** — `CAP-640` — `Continue Architecture Planning.md` L74068–74090
- **v0.23 — 23.1 The absence problem** — `CAP-641` — `Continue Architecture Planning.md` L74092–74142
- **v0.23 — 23.2 Four fundamental states** — `CAP-642` — `Continue Architecture Planning.md` L74144–74182
- **v0.23 — 23.3 PresenceAssertion** — `CAP-643` — `Continue Architecture Planning.md` L74184–74253
- **v0.23 — 23.4 Absence is always scoped** — `CAP-644` — `Continue Architecture Planning.md` L74255–74296
- **v0.23 — 23.5 NegativeEvidence** — `CAP-645` — `Continue Architecture Planning.md` L74298–74346
- **v0.23 — 23.6 Absence strength** — `CAP-646` — `Continue Architecture Planning.md` L74348–74393
- **v0.23 — 23.7 Search failure must not become negative evidence automatically** — `CAP-647` — `Continue Architecture Planning.md` L74395–74447
- **v0.23 — 23.9 Exact locator absence** — `CAP-649` — `Continue Architecture Planning.md` L74483–74531
- **v0.23 — 23.10 Claims need predicates** — `CAP-650` — `Continue Architecture Planning.md` L74533–74571
- **v0.23 — 23.11 Predicate-aware absence** — `CAP-651` — `Continue Architecture Planning.md` L74573–74629
- **v0.23 — 23.12 Contradiction becomes first-class** — `CAP-652` — `Continue Architecture Planning.md` L74631–74679
- **v0.23 — 23.13 True contradiction** — `CAP-653` — `Continue Architecture Planning.md` L74681–74724
- **v0.23 — 23.14 Absence confidence cannot simply be numeric** — `CAP-654` — `Continue Architecture Planning.md` L74726–74767
- **v0.23 — 23.15 Independent evidence** — `CAP-655` — `Continue Architecture Planning.md` L74769–74817
- **v0.23 — 23.16 Absence reasoning engine** — `CAP-656` — `Continue Architecture Planning.md` L74819–74864
- **v0.23 — 23.17 Formal absence rule** — `CAP-657` — `Continue Architecture Planning.md` L74866–74913
- **v0.23 — 23.18 Dynamic universes** — `CAP-658` — `Continue Architecture Planning.md` L74915–74961
- **v0.23 — 23.19 Temporal validity** — `CAP-659` — `Continue Architecture Planning.md` L74963–74995
- **v0.23 — 23.20 Absence and revision detection** — `CAP-660` — `Continue Architecture Planning.md` L74997–75044
- **v0.23 — 23.21 Search state now becomes richer** — `CAP-661` — `Continue Architecture Planning.md` L75046–75099
- **v0.23 — 23.23 The three epistemic outcomes** — `CAP-663` — `Continue Architecture Planning.md` L75169–75171
- **v0.23 — Presence** — `CAP-664` — `Continue Architecture Planning.md` L75173–75183
- **v0.23 — Absence** — `CAP-665` — `Continue Architecture Planning.md` L75185–75199
- **v0.23 — Unknown** — `CAP-666` — `Continue Architecture Planning.md` L75201–75223

## Related Documents

- [Search Space](search-space.md)
- [Evidence Model](evidence-model.md)
- [Verification](../validation/verification.md)
- [The Discovery Loop](../concepts/discovery-loop.md)

---

<!-- USP-034 | Userscript Discovery Prototype.md L917–949 | turn 7 | version ? -->
## 19. Coverage is a better metric than elapsed time

> **Source sections:** `USP-034`
>
> [DOCUMENTATION REVIEW] Contradiction **C-05** ([Review Notes](../REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified))

You can track:

$$coverage = \frac{\text{search space sufficiently evaluated}} {\text{configured search space}}$$

For example:

```
Spectrum coverage:       92%
Physical hypotheses:     87%
Confirmed multiplexes:   14
Services discovered:    126
```

This makes the scanner's result reproducible.

A result can then say:

```
SCAN COMPLETE
Coverage: 100%
Confirmed multiplexes: 14
Services: 126
```

rather than simply:

```
Scan finished.
```

---

<!-- CAP-599 | Continue Architecture Planning.md L72638–72695 | turn 55 | version 0.22 -->
## v0.22 — Discovery Completeness + Coverage Claims

> **Source sections:** `CAP-599`
>
> [DOCUMENTATION REVIEW] Contradiction **C-03** ([Review Notes](../REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming))
>
> [DOCUMENTATION REVIEW] Contradiction **C-05** ([Review Notes](../REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified))

There is now one problem that becomes unavoidable.

The engine can report:

```
"I explored 37 partitions."
"I acquired 214 candidates."
"I found 83 resources."
```

But can it say:

> **“The search is complete”?**

Usually, no.

The next version should therefore formalize **coverage and completeness claims**:

```
Search Space
    │
    ├── explored
    ├── unexplored
    ├── inaccessible
    ├── exhausted
    ├── unsupported
    └── unknown
```

and distinguish:

```
EXHAUSTION
    = the current strategy has no more work

COVERAGE
    = how much of the defined search space has been explored

COMPLETENESS
    = whether the evidence justifies "nothing else remains"
```

For an open web, true global completeness will generally be impossible to prove.

But for bounded spaces such as:

```
known sitemap
known repository index
finite API schema
finite document manifest
```

the engine may be able to make much stronger completeness claims.

That leads naturally to **v0.22 — Coverage, Exhaustion, and Completeness Proofs**.

<!-- CAP-601 | Continue Architecture Planning.md L72707–72717 | turn 57 | version 0.22 -->
## v0.22 — Discovery Completeness + Coverage Claims

> **Source sections:** `CAP-601`
>
> [DOCUMENTATION REVIEW] Contradiction **C-03** ([Review Notes](../REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming))
>
> [DOCUMENTATION REVIEW] Contradiction **C-05** ([Review Notes](../REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified))

The next architectural boundary is not “discover more.”

It is:

> **Know what portion of the search space has actually been explored, what remains unknown, and what strength of completeness claim is justified.**

The engine now has enough structure to distinguish **search execution** from **search assurance**.

---

<!-- CAP-602 | Continue Architecture Planning.md L72719–72763 | turn 57 | version 0.22 -->
## v0.22 — 22.1 The problem

> **Source sections:** `CAP-602`

A scan can finish while the search is still incomplete.

```
Frontier = empty
    ↓
No more work known
    ↓
Scan stops
```

This only proves:

> “The engine has no currently admitted work.”

It does **not** prove:

> “No undiscovered resources exist.”

Therefore:

```
EXHAUSTION
    ≠
COVERAGE
    ≠
COMPLETENESS
```

This distinction becomes critical for a document-discovery system.

For example:

```
https://example.com/docs/
        │
        ├── manual-a.pdf
        ├── manual-b.pdf
        └── ??? hidden repository
```

If the engine follows every visible link, it may reach frontier exhaustion while the hidden repository remains unknown.

---

<!-- CAP-603 | Continue Architecture Planning.md L72765–72815 | turn 57 | version 0.22 -->
## v0.22 — 22.2 Search-space state model

> **Source sections:** `CAP-603`

The search space should become explicitly measurable.

```
                         SEARCH SPACE
                              │
             ┌────────────────┼────────────────┐
             │                │                │
         EXPLORED          UNEXPLORED       UNKNOWN
             │                │                │
       ┌─────┴─────┐          │          inaccessible /
       │           │          │          unsupported /
   exhausted    active        │          unenumerable
                              │
                              ▼
                         not evaluated
```

A useful partition state model is:

```
UNEXPLORED
    ↓
ELIGIBLE
    ↓
DISCOVERING
    ↓
ACTIVE
    ↓
SATURATED
    ↓
EXHAUSTED
```

With exceptional states:

```
DENIED
SKIPPED
FAILED
INACCESSIBLE
UNSUPPORTED
UNKNOWN
```

But these states answer **operational questions**.

Coverage needs another dimension.

---

<!-- CAP-604 | Continue Architecture Planning.md L72817–72852 | turn 57 | version 0.22 -->
## v0.22 — 22.3 Coverage is a measurement

> **Source sections:** `CAP-604`
>
> [DOCUMENTATION REVIEW] Contradiction **C-05** ([Review Notes](../REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified))

Define:

```
Coverage(S, E)
```

where:

* `S` = defined search space
* `E` = exploration evidence

The important point is that coverage is always relative to a **defined universe**.

There is no meaningful statement:

```
"The web is 80% covered."
```

without defining what “the web” means and how coverage is measured.

Instead:

```
Coverage(
    domain = example.com/docs,
    partitioning = sitemap paths,
    strategy = sitemap enumeration
)
```

is meaningful.

---

<!-- CAP-605 | Continue Architecture Planning.md L72854–72906 | turn 57 | version 0.22 -->
## v0.22 — 22.4 Coverage dimensions

> **Source sections:** `CAP-605`
>
> [DOCUMENTATION REVIEW] Contradiction **C-05** ([Review Notes](../REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified))

Coverage should not be one scalar.

The engine should track multiple dimensions.

```
COVERAGE
│
├── partition coverage
│
├── locator coverage
│
├── candidate coverage
│
├── resource coverage
│
├── artifact coverage
│
├── representation coverage
│
└── semantic coverage
```

These answer different questions.

| Dimension | Question |
| --- | --- |
| Partition | Which regions were explored? |
| Locator | Which known addresses were examined? |
| Candidate | Which discovered possibilities were processed? |
| Resource | Which logical resources were identified? |
| Representation | Which representations were observed? |
| Artifact | Which concrete byte sequences were acquired? |
| Semantic | Which relevant document classes were classified? |

Therefore:

```
100% locator coverage
        ≠
100% resource coverage
```

and:

```
100% resource coverage
        ≠
100% semantic coverage
```

---

<!-- CAP-606 | Continue Architecture Planning.md L72908–72980 | turn 57 | version 0.22 -->
## v0.22 — 22.5 CoverageRecord

> **Source sections:** `CAP-606`
>
> [DOCUMENTATION REVIEW] Contradiction **C-05** ([Review Notes](../REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified))

Introduce an explicit record.

```JavaScript
class CoverageRecord {
    constructor(data = {}) {
        this.id = data.id || makeId('coverage');

        this.sessionId = data.sessionId || null;
        this.domainId = data.domainId || null;
        this.partitionId = data.partitionId || null;

        this.dimension = data.dimension || 'partition';

        this.status = data.status || 'unknown';

        this.explored = Number.isFinite(data.explored)
            ? data.explored
            : 0;

        this.estimatedTotal = Number.isFinite(data.estimatedTotal)
            ? data.estimatedTotal
            : null;

        this.method = data.method || null;

        this.evidenceIds = data.evidenceIds || [];

        this.createdAt = data.createdAt || now();
    }

    ratio() {
        if (
            this.estimatedTotal === null ||
            this.estimatedTotal <= 0
        ) {
            return null;
        }

        return Math.min(
            1,
            this.explored / this.estimatedTotal
        );
    }

    serialize() {
        return { ...this };
    }
}
```

The important design choice is:

```
estimatedTotal = null
```

must remain valid.

Unknown denominator means:

```
coverage percentage cannot be honestly calculated
```

rather than:

```
assume 100%
```

---

<!-- CAP-607 | Continue Architecture Planning.md L72982–73020 | turn 57 | version 0.22 -->
## v0.22 — 22.6 Coverage state

> **Source sections:** `CAP-607`
>
> [DOCUMENTATION REVIEW] Contradiction **C-05** ([Review Notes](../REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified))

Use qualitative states in addition to numerical measurements.

```JavaScript
const CoverageState = Object.freeze({
    UNKNOWN: 'unknown',
    NONE: 'none',
    PARTIAL: 'partial',
    SUBSTANTIAL: 'substantial',
    EXHAUSTIVE: 'exhaustive',
    INACCESSIBLE: 'inaccessible',
    UNSUPPORTED: 'unsupported'
});
```

These should not automatically be derived from percentages.

For example:

```
known sitemap
    95 / 100 URLs processed
        ↓
PARTIAL
```

But:

```
finite API enumeration
all 100 / 100 entries processed
        ↓
EXHAUSTIVE
```

provided the enumeration itself is trusted and complete.

---

<!-- CAP-608 | Continue Architecture Planning.md L73022–73075 | turn 57 | version 0.22 -->
## v0.22 — 22.7 CoverageClaim

> **Source sections:** `CAP-608`
>
> [DOCUMENTATION REVIEW] Contradiction **C-03** ([Review Notes](../REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming))
>
> [DOCUMENTATION REVIEW] Contradiction **C-05** ([Review Notes](../REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified))

A measurement is not automatically a claim.

Introduce:

```JavaScript
class CoverageClaim {
    constructor(data = {}) {
        this.id = data.id || makeId('coverage-claim');

        this.sessionId = data.sessionId || null;
        this.domainId = data.domainId || null;
        this.partitionId = data.partitionId || null;

        this.dimension = data.dimension || null;

        this.claim = data.claim || null;

        this.assurance = data.assurance || 'unknown';

        this.evidenceIds = data.evidenceIds || [];

        this.methodId = data.methodId || null;
        this.methodVersion = data.methodVersion || null;

        this.createdAt = data.createdAt || now();
    }

    serialize() {
        return { ...this };
    }
}
```

Examples:

```
claim:
"All entries in sitemap X were enumerated."
```

versus:

```
claim:
"No other documents exist on this website."
```

The first may be defensible.

The second usually is not.

---

<!-- CAP-609 | Continue Architecture Planning.md L73077–73131 | turn 57 | version 0.22 -->
## v0.22 — 22.8 Completeness is a stronger assertion

> **Source sections:** `CAP-609`
>
> [DOCUMENTATION REVIEW] Contradiction **C-05** ([Review Notes](../REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified))

Define:

```
Coverage
    ↓
Exploration evidence
    ↓
Completeness assessment
```

A `CompletenessClaim` should therefore be separate.

```JavaScript
class CompletenessClaim {
    constructor(data = {}) {
        this.id = data.id || makeId('complete');

        this.domainId = data.domainId || null;
        this.sessionId = data.sessionId || null;

        this.scope = data.scope || null;

        this.status = data.status || 'not-established';

        this.assurance = data.assurance || 'unknown';

        this.enumerator = data.enumerator || null;

        this.evidenceIds = data.evidenceIds || [];

        this.conditions = data.conditions || [];

        this.createdAt = data.createdAt || now();
    }

    serialize() {
        return { ...this };
    }
}
```

Possible states:

```
NOT_ESTABLISHED
SUPPORTED
CONDITIONALLY_COMPLETE
EXHAUSTIVE
DISPROVED
UNKNOWN
```

---

<!-- CAP-610 | Continue Architecture Planning.md L73133–73193 | turn 57 | version 0.22 -->
## v0.22 — 22.9 The finite-enumerator case

> **Source sections:** `CAP-610`

This is where genuine completeness becomes possible.

Suppose the engine encounters:

```
manifest.json

{
    "documents": [
        "a.pdf",
        "b.pdf",
        "c.pdf"
    ]
}
```

If the manifest itself has strong evidence that it enumerates the complete collection:

```
manifest
   ↓
enumerator
   ↓
3 declared entries
   ↓
3 acquired/processed
```

then the engine may establish:

```
partition = exhausted
enumerator = complete
all entries processed
        ↓
CONDITIONALLY COMPLETE
```

Potentially:

```
EXHAUSTIVE
```

if the enumeration contract is sufficiently authoritative.

The engine should therefore model:

```
Enumerator
    ├── identity
    ├── version
    ├── scope
    ├── completeness semantics
    ├── entries observed
    └── evidence
```

---

<!-- CAP-611 | Continue Architecture Planning.md L73195–73249 | turn 57 | version 0.22 -->
## v0.22 — 22.10 Enumeration contract

> **Source sections:** `CAP-611`

Introduce:

```JavaScript
class EnumerationContract {
    constructor(data = {}) {
        this.id = data.id || makeId('enum');

        this.enumeratorType = data.enumeratorType || 'unknown';

        this.scope = data.scope || null;

        this.completeByDefinition =
            Boolean(data.completeByDefinition);

        this.supportsPagination =
            Boolean(data.supportsPagination);

        this.supportsCursor =
            Boolean(data.supportsCursor);

        this.version = data.version || null;

        this.evidenceIds = data.evidenceIds || [];
    }
}
```

Examples:

| Enumerator | Completeness potential |
| --- | --- |
| Explicit finite manifest | High |
| Complete sitemap index | High |
| Paginated API with verified terminal page | High |
| Repository directory listing | Medium–High |
| Search engine results | Low |
| HTML links | Low |
| Keyword search | Very low |
| Open-web crawling | Generally unprovable |

The engine must not confuse:

```
"the source returned everything it claims to enumerate"
```

with:

```
"everything relevant in existence was found."
```

---

<!-- CAP-612 | Continue Architecture Planning.md L73251–73323 | turn 57 | version 0.22 -->
## v0.22 — 22.11 Negative evidence

> **Source sections:** `CAP-612`

This introduces a subtle but important concept.

Positive evidence:

```
"There is a manual.pdf"
```

Negative evidence:

```
"No manual.pdf was found."
```

These are not symmetric.

Failure to observe something does not normally prove its absence.

Therefore:

```
NOT FOUND
    ≠
DOES NOT EXIST
```

The engine needs explicit negative-evidence semantics.

```JavaScript
class NegativeEvidence {
    constructor(data = {}) {
        this.id = data.id || makeId('neg-evidence');

        this.scope = data.scope || null;

        this.predicate = data.predicate || null;

        this.observationIds = data.observationIds || [];

        this.methodId = data.methodId || null;

        this.strength = data.strength || 'weak';

        this.conditions = data.conditions || [];

        this.createdAt = data.createdAt || now();
    }
}
```

Example:

```
Observed:

GET /docs/index.json
→ 200
→ manifest contains 127 entries

Negative evidence:

"No additional entries are present in this manifest."
```

This is substantially stronger than:

```
"We crawled for 10 minutes and found no more PDFs."
```

---

<!-- CAP-613 | Continue Architecture Planning.md L73325–73365 | turn 57 | version 0.22 -->
## v0.22 — 22.12 Absence reasoning hierarchy

> **Source sections:** `CAP-613`

A useful hierarchy:

```
LEVEL 0
No observation
    ↓
LEVEL 1
Not found by current strategy
    ↓
LEVEL 2
Not found across selected strategies
    ↓
LEVEL 3
Explicit source says absent
    ↓
LEVEL 4
Complete enumerator excludes it
    ↓
LEVEL 5
Authoritative specification proves absence
```

These should never collapse into a single boolean:

```JavaScript
exists = false
```

Instead:

```JavaScript
{
    status: 'not-observed',
    assurance: 'strategy-relative',
    evidenceIds: [...]
}
```

---

<!-- CAP-614 | Continue Architecture Planning.md L73367–73401 | turn 57 | version 0.22 -->
## v0.22 — 22.13 “Not found” becomes a first-class result

> **Source sections:** `CAP-614`

Discovery results should therefore distinguish:

```
FOUND
NOT_FOUND
NOT_OBSERVED
INACCESSIBLE
UNSUPPORTED
UNKNOWN
```

For example:

| Result | Meaning |
| --- | --- |
| FOUND | Positive evidence exists |
| NOT_FOUND | Search method found no matching item |
| NOT_OBSERVED | Search did not establish absence |
| INACCESSIBLE | Relevant region could not be examined |
| UNSUPPORTED | Engine lacks required mechanism |
| UNKNOWN | Insufficient evidence |

This prevents a major false inference:

```
HTTP 403
  ↓
"No manual exists"
```

which is obviously invalid.

---

<!-- CAP-615 | Continue Architecture Planning.md L73403–73459 | turn 57 | version 0.22 -->
## v0.22 — 22.14 Coverage cannot necessarily be monotonically interpreted

> **Source sections:** `CAP-615`
>
> [DOCUMENTATION REVIEW] Contradiction **C-05** ([Review Notes](../REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified))

At first glance:

```
coverage(t+1) >= coverage(t)
```

seems desirable.

But discovery systems encounter revisions.

Example:

```
Session 1
sitemap → 100 entries

Session 2
sitemap → 120 entries
```

If coverage is measured against the current universe:

```
100 / 100 = 100%
```

then later:

```
100 / 120 = 83%
```

The apparent coverage decreases.

That does **not** mean the engine forgot anything.

It means:

```
SEARCH UNIVERSE CHANGED
```

Therefore distinguish:

```
exploration progress
```

from:

```
coverage relative to a versioned universe
```

---

<!-- CAP-616 | Continue Architecture Planning.md L73461–73507 | turn 57 | version 0.22 -->
## v0.22 — 22.15 Version the search universe

> **Source sections:** `CAP-616`

Introduce:

```JavaScript
class SearchSpaceSnapshot {
    constructor(data = {}) {
        this.id = data.id || makeId('space-snapshot');

        this.domainId = data.domainId || null;

        this.partitionIds = data.partitionIds || [];

        this.enumeratorIds = data.enumeratorIds || [];

        this.fingerprint = data.fingerprint || null;

        this.createdAt = data.createdAt || now();
    }
}
```

Then:

```
Session 001
    ↓
SearchSpaceSnapshot A
    ↓
coverage = 100%
```

Later:

```
Session 002
    ↓
SearchSpaceSnapshot B
    ↓
new entries discovered
    ↓
coverage recalculated
```

This preserves historical truth.

---

<!-- CAP-617 | Continue Architecture Planning.md L73509–73550 | turn 57 | version 0.22 -->
## v0.22 — 22.16 Coverage ledger

> **Source sections:** `CAP-617`
>
> [DOCUMENTATION REVIEW] Contradiction **C-05** ([Review Notes](../REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified))

The event ledger now gains explicit search-assurance events.

```
partition-admitted
partition-started
partition-probed
partition-saturated
partition-exhausted

coverage-measured
coverage-updated
coverage-unknown

enumerator-recognized
enumeration-started
enumeration-page-observed
enumeration-completed
enumeration-invalid

negative-evidence-recorded

completeness-assessed
completeness-supported
completeness-rejected
completeness-unknown
```

The temporal ledger answers:

> What did the engine do?

The evidence graph answers:

> Why does it believe what it believes?

The coverage graph answers:

> What portion of the defined search universe has been explored?

---

<!-- CAP-618 | Continue Architecture Planning.md L73552–73607 | turn 57 | version 0.22 -->
## v0.22 — 22.17 Three graphs now interact

> **Source sections:** `CAP-618`

The architecture becomes:

```
                    SEARCH SPACE
                         │
                         ▼
                 COVERAGE GRAPH
                         │
                  ┌──────┴──────┐
                  │             │
             Explored       Unexplored
                  │
                  ▼
             DISCOVERY
                  │
                  ▼
              OBSERVATION
                  │
                  ▼
             EVIDENCE GRAPH
                  │
                  ▼
               RESOURCE
                  │
                  ▼
             CLASSIFICATION


EVENT LEDGER
    │
    └── records how all of the above happened
```

More formally:

```
Operational plane
────────────────────────────────
Domain → Partition → WorkItem → Strategy → Observation


Epistemic plane
────────────────────────────────
Observation → Evidence → Claim → Resource


Assurance plane
────────────────────────────────
SearchSpace → Coverage → Completeness
```

This is a significant architectural separation.

---

<!-- CAP-619 | Continue Architecture Planning.md L73609–73663 | turn 57 | version 0.22 -->
## v0.22 — 22.18 Completeness assessment

> **Source sections:** `CAP-619`
>
> [DOCUMENTATION REVIEW] Contradiction **C-05** ([Review Notes](../REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified))

Completeness should be a deterministic evaluator.

```JavaScript
class CompletenessEvaluator {
    assess(context) {
        const {
            domain,
            snapshot,
            partitions,
            enumerators,
            coverage
        } = context;

        if (!domain) {
            return {
                status: 'unknown',
                reason: 'domain-missing'
            };
        }

        if (!snapshot) {
            return {
                status: 'unknown',
                reason: 'search-space-snapshot-missing'
            };
        }

        // Evaluate explicit finite enumerators first.
        // Never infer global completeness merely from frontier exhaustion.

        return {
            status: 'not-established',
            reason: 'insufficient-completeness-evidence'
        };
    }
}
```

The evaluator must be conservative.

Especially:

```
frontier empty
```

must **not** automatically produce:

```
complete = true
```

---

<!-- CAP-621 | Continue Architecture Planning.md L73699–73713 | turn 57 | version 0.22 -->
## v0.22 — 22.20 Search completeness matrix

> **Source sections:** `CAP-621`
>
> [DOCUMENTATION REVIEW] Contradiction **C-05** ([Review Notes](../REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified))

| Situation | Frontier | Coverage | Completeness |
| --- | --- | --- | --- |
| No work yet | Empty | 0 | None |
| HTML links exhausted | Empty | Partial/unknown | A1 at best |
| Multiple strategies exhausted | Empty | Higher | A2 |
| Complete sitemap enumerated | Empty | High | A3 |
| Verified finite manifest exhausted | Empty | 100% of manifest | A4 |
| Independent authoritative verification | Empty | Verified | A5 |
| 403 prevents partition | Empty | Partial | Cannot establish |
| Dynamic hidden resources | Empty | Unknown | Cannot establish |
| Open-web crawl ends | Empty | Strategy-relative | Cannot prove global completeness |

---

<!-- CAP-622 | Continue Architecture Planning.md L73715–73761 | turn 57 | version 0.22 -->
## v0.22 — 22.21 Coverage calculation

> **Source sections:** `CAP-622`
>
> [DOCUMENTATION REVIEW] Contradiction **C-05** ([Review Notes](../REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified))

For partitions with known weights:

```
coverage =
    explored_weight
    ----------------
    total_known_weight
```

For example:

```
SearchSpace
├── /manuals       weight 40
├── /bulletins     weight 20
├── /parts         weight 30
└── /software      weight 10
```

If:

```
/manuals   explored
/bulletins explored
/parts     partial 50%
/software  unexplored
```

then:

```
40 + 20 + 15
────────────── = 75%
    100
```

But this is only meaningful if the weights have a defensible interpretation.

Therefore:

> **Weighted coverage is a measurement model, not a fact about the universe.**

The engine should preserve the weighting method.

---

<!-- CAP-623 | Continue Architecture Planning.md L73763–73807 | turn 57 | version 0.22 -->
## v0.22 — 22.22 Coverage should be query-relative

> **Source sections:** `CAP-623`
>
> [DOCUMENTATION REVIEW] Contradiction **C-05** ([Review Notes](../REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified))

This is particularly important for the eventual service-document system.

Suppose the universe contains:

```
10,000 web resources
```

but the query is:

```
"Otis Gen2 service manuals"
```

The useful question is not:

```
How much of the website was crawled?
```

It is:

```
How much of the relevant search space for this query was explored?
```

Therefore introduce eventually:

```
Search Goal
    ↓
Relevance Model
    ↓
Relevant Search Space
    ↓
Coverage
```

This should **not** be added to v0.22 as a hard dependency yet.

The generic engine should first establish objective coverage semantics.

---

<!-- CAP-638 | Continue Architecture Planning.md L74029–74056 | turn 57 | version 0.23 -->
## v0.23 — Negative Evidence + Absence Reasoning

> **Source sections:** `CAP-638`

The next natural boundary is now clear.

Once the engine can represent coverage, it can represent **absence claims** without making the classic mistake of treating failure to find something as proof that it does not exist.

The next layer should formalize:

```
Observation
     ↓
Positive Evidence       Negative Evidence
     ↓                         ↓
Presence Claim            Absence Claim
     └────────────┬────────────┘
                  ↓
             Confidence
                  ↓
          Contradiction Graph
                  ↓
          Search Decision
```

The key problem becomes:

> **When is “nothing was found” meaningful evidence, and when is it merely an artifact of an incomplete search?**

That is the boundary between a crawler and an actual discovery/knowledge system.

<!-- CAP-640 | Continue Architecture Planning.md L74068–74090 | turn 59 | version 0.23 -->
## v0.23 — Negative Evidence + Absence Reasoning

> **Source sections:** `CAP-640`

v0.22 established **coverage** and **completeness claims**.

The next problem is the inverse:

> If the engine does not find something, what exactly is justified by that absence?

The critical distinction is:

```
NOT OBSERVED
    ≠
NOT FOUND
    ≠
ABSENT
    ≠
PROVABLY ABSENT
```

A discovery engine that cannot distinguish these will eventually generate false negatives.

---

<!-- CAP-641 | Continue Architecture Planning.md L74092–74142 | turn 59 | version 0.23 -->
## v0.23 — 23.1 The absence problem

> **Source sections:** `CAP-641`

Consider:

```
Query:
"Gen2 service manual"
```

The engine searches:

```
site.example/
├── /docs/
├── /manuals/
└── /support/
```

No matching document appears.

There are several possible explanations:

```
                   NO RESULT
                       │
       ┌───────────────┼────────────────┐
       │               │                │
   doesn't exist    not exposed      not accessible
       │               │                │
       │          hidden repository     │
       │          dynamic endpoint      │
       │          unlinked document     │
       │                                │
       └───────────────┬────────────────┘
                       │
                 unknown cause
```

Therefore the engine must not produce:

```JavaScript
exists: false
```

simply because:

```JavaScript
results.length === 0
```

---

<!-- CAP-642 | Continue Architecture Planning.md L74144–74182 | turn 59 | version 0.23 -->
## v0.23 — 23.2 Four fundamental states

> **Source sections:** `CAP-642`

v0.23 introduces a formal presence state.

```JavaScript
const PresenceState = Object.freeze({
    PRESENT: 'present',
    NOT_FOUND: 'not-found',
    NOT_OBSERVED: 'not-observed',
    ABSENT: 'absent',
    UNKNOWN: 'unknown'
});
```

But these states have different semantics.

| State | Meaning |
| --- | --- |
| `present` | Positive evidence establishes presence |
| `not-found` | Current search found no matching candidate |
| `not-observed` | Relevant observation never occurred |
| `absent` | Evidence supports absence within defined scope |
| `unknown` | Evidence is insufficient to determine state |

The most important distinction:

```
NOT_FOUND
```

is a **search result**.

```
ABSENT
```

is an **epistemic claim**.

---

<!-- CAP-643 | Continue Architecture Planning.md L74184–74253 | turn 59 | version 0.23 -->
## v0.23 — 23.3 PresenceAssertion

> **Source sections:** `CAP-643`

Introduce an explicit assertion model.

```JavaScript
class PresenceAssertion {
    constructor(data = {}) {
        this.id = data.id || makeId('presence');

        this.subject = data.subject || null;

        this.state = data.state || 'unknown';

        this.scope = data.scope || null;

        this.sessionId = data.sessionId || null;

        this.evidenceIds = data.evidenceIds || [];

        this.methodId = data.methodId || null;
        this.methodVersion = data.methodVersion || null;

        this.confidence = Number.isFinite(data.confidence)
            ? data.confidence
            : 0;

        this.conditions = data.conditions || [];

        this.status = data.status || 'active';

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
    subject: 'resource:manual-42',
    state: 'present',
    scope: {
        domainId: 'domain-1'
    },
    evidenceIds: ['ev-123'],
    confidence: 0.99
}
```

Absence:

```JavaScript
{
    subject: 'resource:manual-99',
    state: 'absent',
    scope: {
        partitionId: 'partition-manuals'
    },
    evidenceIds: ['ev-enumeration-44'],
    confidence: 0.98
}
```

The scope is essential.

---

<!-- CAP-644 | Continue Architecture Planning.md L74255–74296 | turn 59 | version 0.23 -->
## v0.23 — 23.4 Absence is always scoped

> **Source sections:** `CAP-644`

Never store:

```
manual-99 = absent
```

Store:

```
manual-99
    absent
    within:
        sitemap-X
        version-2026-09
        partition-/manuals/
```

Because:

```
ABSENT(IN SCOPE A)
```

does not imply:

```
ABSENT(EVERYWHERE)
```

Formally:

```
Absent(x, S)
    ⇏
Absent(x, Universe)
```

This is one of the central invariants of the system.

---

<!-- CAP-645 | Continue Architecture Planning.md L74298–74346 | turn 59 | version 0.23 -->
## v0.23 — 23.5 NegativeEvidence

> **Source sections:** `CAP-645`

The previous version introduced the concept; v0.23 makes it operational.

```JavaScript
class NegativeEvidence {
    constructor(data = {}) {
        this.id = data.id || makeId('neg');

        this.subject = data.subject || null;

        this.scope = data.scope || null;

        this.predicate = data.predicate || null;

        this.observationIds = data.observationIds || [];

        this.enumeratorId = data.enumeratorId || null;

        this.methodId = data.methodId || null;
        this.methodVersion = data.methodVersion || null;

        this.strength = data.strength || 'weak';

        this.conditions = data.conditions || [];

        this.createdAt = data.createdAt || now();
    }

    serialize() {
        return { ...this };
    }
}
```

Example:

```
NegativeEvidence
├── subject: "manual-X"
├── scope: "/manuals/"
├── predicate: "contains"
├── observations:
│     └── sitemap-observation-17
├── enumerator: sitemap-v3
└── strength: strong
```

---

<!-- CAP-646 | Continue Architecture Planning.md L74348–74393 | turn 59 | version 0.23 -->
## v0.23 — 23.6 Absence strength

> **Source sections:** `CAP-646`

Not all negative evidence has equal value.

A useful hierarchy:

```
N0 — NO EVIDENCE
     No meaningful search occurred.

N1 — WEAK
     One strategy did not find it.

N2 — MODERATE
     Several relevant strategies did not find it.

N3 — STRONG
     Explicit enumeration excludes it.

N4 — VERY STRONG
     Complete finite enumeration excludes it.

N5 — VERIFIED
     Independent authoritative evidence establishes absence.
```

For example:

```
HTML crawler found no PDF
        ↓
N1
```

versus:

```
Complete manifest contains 127 items
requested item absent
        ↓
N4
```

The latter can support a much stronger absence claim.

---

<!-- CAP-647 | Continue Architecture Planning.md L74395–74447 | turn 59 | version 0.23 -->
## v0.23 — 23.7 Search failure must not become negative evidence automatically

> **Source sections:** `CAP-647`

This is a major failure mode.

Suppose:

```
GET /docs/
→ 403 Forbidden
```

The engine must **not** produce:

```
NegativeEvidence:
"no documents exist"
```

Instead:

```
Observation
    ↓
Access failure
    ↓
INACCESSIBLE
```

Similarly:

```
timeout
DNS failure
TLS failure
unsupported protocol
authentication required
robots restriction
rate limiting
```

should normally generate:

```
search uncertainty
```

rather than:

```
absence
```

---

<!-- CAP-649 | Continue Architecture Planning.md L74483–74531 | turn 59 | version 0.23 -->
## v0.23 — 23.9 Exact locator absence

> **Source sections:** `CAP-649`

There is one useful special case.

Suppose:

```
GET /manuals/x.pdf
→ HTTP 404
```

The engine can reasonably record:

```
NegativeEvidence
subject = /manuals/x.pdf
predicate = "retrievable"
strength = moderate
```

But this still does not necessarily prove:

```
resource does not exist
```

The resource might exist at:

```
/manuals/x-2026.pdf
/manuals/x.pdf?revision=2
/archive/manuals/x.pdf
```

Therefore the claim must remain about the observed predicate:

```
NOT RETRIEVABLE AT LOCATOR X
```

rather than:

```
RESOURCE DOES NOT EXIST
```

This is an important predicate-level distinction.

---

<!-- CAP-650 | Continue Architecture Planning.md L74533–74571 | turn 59 | version 0.23 -->
## v0.23 — 23.10 Claims need predicates

> **Source sections:** `CAP-650`
>
> [DOCUMENTATION REVIEW] Contradiction **C-03** ([Review Notes](../REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming))

The engine should therefore stop thinking about presence as one universal boolean.

Instead:

```
Claim(subject, predicate, object)
```

Examples:

```
Resource A
    has-locator
    /manual.pdf
```

```
Locator /manual.pdf
    is-retrievable
    false
```

```
Manifest X
    contains
    Resource A
```

```
Manifest X
    does-not-contain
    Resource B
```

These are different propositions.

---

<!-- CAP-651 | Continue Architecture Planning.md L74573–74629 | turn 59 | version 0.23 -->
## v0.23 — 23.11 Predicate-aware absence

> **Source sections:** `CAP-651`

Introduce:

```JavaScript
class AbsenceClaim {
    constructor(data = {}) {
        this.id = data.id || makeId('absence');

        this.subject = data.subject || null;

        this.predicate = data.predicate || null;

        this.object = data.object ?? null;

        this.scope = data.scope || null;

        this.evidenceIds = data.evidenceIds || [];

        this.assurance = data.assurance || 'unknown';

        this.confidence = Number.isFinite(data.confidence)
            ? data.confidence
            : 0;

        this.conditions = data.conditions || [];

        this.status = data.status || 'active';

        this.createdAt = data.createdAt || now();
    }
}
```

Example:

```JavaScript
{
    subject: 'manifest-42',
    predicate: 'contains',
    object: 'manual-99',
    scope: {
        manifestVersion: '2026-09'
    },
    assurance: 'enumerator-bounded'
}
```

This means:

> The manifest does not contain this resource.

It does **not** mean:

> The resource does not exist anywhere.

---

<!-- CAP-652 | Continue Architecture Planning.md L74631–74679 | turn 59 | version 0.23 -->
## v0.23 — 23.12 Contradiction becomes first-class

> **Source sections:** `CAP-652`

Now suppose two observations produce:

```
Claim A:
manifest-X does-not-contain manual-42

Claim B:
page-Y references manual-42
```

The engine should not overwrite either.

Instead:

```
                manual-42
                    │
        ┌───────────┴───────────┐
        │                       │
   NEGATIVE CLAIM          POSITIVE CLAIM
        │                       │
   manifest-X              page-Y
        │                       │
   does-not-contain         references
```

These claims may both be true.

Why?

Because:

```
manifest-X
```

might be incomplete while:

```
page-Y
```

contains a valid reference.

Therefore contradiction resolution must consider **scope and predicate** before declaring an actual contradiction.

---

<!-- CAP-653 | Continue Architecture Planning.md L74681–74724 | turn 59 | version 0.23 -->
## v0.23 — 23.13 True contradiction

> **Source sections:** `CAP-653`

A genuine contradiction might be:

```
Manifest X v5:
contains manual-42

Manifest X v5:
does-not-contain manual-42
```

under the same:

```
scope
version
predicate
identity
```

Now:

```
CLAIM CONFLICT
```

should be recorded.

```JavaScript
{
    relation: 'contradicts',
    leftClaimId: 'claim-a',
    rightClaimId: 'claim-b',
    evidenceIds: [
        'ev-a',
        'ev-b'
    ]
}
```

Never silently choose one.

---

<!-- CAP-654 | Continue Architecture Planning.md L74726–74767 | turn 59 | version 0.23 -->
## v0.23 — 23.14 Absence confidence cannot simply be numeric

> **Source sections:** `CAP-654`
>
> [DOCUMENTATION REVIEW] Contradiction **C-06** ([Review Notes](../REVIEW-NOTES.md#c-06--confidence-one-score-versus-no-single-global-score))

A dangerous implementation would do:

```JavaScript
confidence = 0.95;
```

after several failed searches.

That can be misleading because the failures may all depend on the same weak strategy.

Instead retain:

```
Evidence independence
Evidence quality
Scope
Method completeness
Accessibility
Freshness
Contradictions
```

Conceptually:

```
Absence Assurance
├── scope completeness
├── enumerator quality
├── observation integrity
├── method relevance
├── independence
├── freshness
└── contradiction state
```

A numerical score can be derived later.

It should not replace these dimensions.

---

<!-- CAP-655 | Continue Architecture Planning.md L74769–74817 | turn 59 | version 0.23 -->
## v0.23 — 23.15 Independent evidence

> **Source sections:** `CAP-655`

Suppose the engine searches the same page three times:

```
HTML crawler
HTML crawler
HTML crawler
```

All fail to find a document.

That is not three independent confirmations.

The underlying observation source is effectively the same.

Contrast:

```
Sitemap
    ↓
no document

Repository API
    ↓
no document

Directory index
    ↓
no document
```

These provide more independent evidence.

Therefore the engine should preserve:

```JavaScript
{
    methodId,
    sourceId,
    observationId,
    strategyId,
    enumeratorId
}
```

and allow later independence analysis.

---

<!-- CAP-656 | Continue Architecture Planning.md L74819–74864 | turn 59 | version 0.23 -->
## v0.23 — 23.16 Absence reasoning engine

> **Source sections:** `CAP-656`

Introduce:

```JavaScript
class AbsenceReasoner {
    assess(context) {
        const {
            subject,
            claims,
            negativeEvidence,
            coverage
        } = context;

        if (!subject) {
            return {
                state: 'unknown',
                assurance: 'unknown',
                reason: 'subject-missing'
            };
        }

        if (!negativeEvidence?.length) {
            return {
                state: 'not-observed',
                assurance: 'none'
            };
        }

        // Conservative evaluation.
        // Strong absence requires bounded scope and
        // sufficiently complete enumeration.

        return {
            state: 'not-found',
            assurance: 'strategy-relative'
        };
    }
}
```

The important property:

> **The absence reasoner interprets evidence; it does not create observations.**

---

<!-- CAP-657 | Continue Architecture Planning.md L74866–74913 | turn 59 | version 0.23 -->
## v0.23 — 23.17 Formal absence rule

> **Source sections:** `CAP-657`

A useful first rule:

```
Absent(x, S)
```

requires:

```
1. S is explicitly defined
2. S is sufficiently observable
3. the relevant enumerator/strategy covers S
4. enumeration completed
5. x was absent from the enumerated result
6. no contradictory evidence exists within S
```

Therefore:

```
CompleteEnumeration(S)
∧
¬Contains(S, x)
∧
NoContradiction(S, x)
──────────────────────────
Absence(x, S)
```

This is deliberately scoped.

It does **not** derive:

```
Absence(x, Universe)
```

unless:

```
S = Universe
```

and the universe itself is well-defined and enumerable.

---

<!-- CAP-658 | Continue Architecture Planning.md L74915–74961 | turn 59 | version 0.23 -->
## v0.23 — 23.18 Dynamic universes

> **Source sections:** `CAP-658`

The web is not static.

Consider:

```
10:00
manifest = [A, B, C]

10:05
manifest = [A, B, C, D]
```

At 10:00:

```
D absent from manifest
```

At 10:05:

```
D present
```

There is no contradiction if the claims carry temporal scope.

Therefore:

```JavaScript
{
    validFrom: timestamp,
    observedAt: timestamp,
    snapshotId: 'snapshot-42'
}
```

should eventually be part of absence claims.

The claim becomes:

> D was absent from snapshot 42.

That is a durable historical statement.

---

<!-- CAP-659 | Continue Architecture Planning.md L74963–74995 | turn 59 | version 0.23 -->
## v0.23 — 23.19 Temporal validity

> **Source sections:** `CAP-659`

The epistemic model now becomes:

```
Claim
├── subject
├── predicate
├── object
├── scope
├── evidence
├── method
├── confidence
├── status
├── observedAt
└── snapshotId
```

This allows:

```
PRESENT at T2
```

to coexist with:

```
ABSENT at T1
```

without corruption.

---

<!-- CAP-660 | Continue Architecture Planning.md L74997–75044 | turn 59 | version 0.23 -->
## v0.23 — 23.20 Absence and revision detection

> **Source sections:** `CAP-660`
>
> [DOCUMENTATION REVIEW] Contradiction **C-07** ([Review Notes](../REVIEW-NOTES.md#c-07--resource--artifact-model-revised))

This becomes especially useful for document aggregation.

Suppose:

```
Session 1
────────────────
manual-v1.pdf present

Session 2
────────────────
manual-v1.pdf missing
manual-v2.pdf present
```

Possible interpretations:

```
A. v1 removed
B. v1 moved
C. repository reorganized
D. index incomplete
E. access changed
```

The engine must not immediately assert:

```
v1 deleted
```

Instead:

```
Observation delta
       ↓
Negative evidence
       ↓
Revision/removal hypothesis
       ↓
Further verification
```

This is the beginning of **change-aware discovery**.

---

<!-- CAP-661 | Continue Architecture Planning.md L75046–75099 | turn 59 | version 0.23 -->
## v0.23 — 23.21 Search state now becomes richer

> **Source sections:** `CAP-661`

The frontier can report:

```
FOUND
NOT_FOUND
NOT_OBSERVED
INACCESSIBLE
UNSUPPORTED
UNKNOWN
```

while the assurance layer reports:

```
NO_ASSURANCE
STRATEGY_RELATIVE
MULTI_STRATEGY
ENUMERATOR_BOUNDED
VERIFIED
```

These dimensions should remain independent.

For example:

```
NOT_FOUND
+
ENUMERATOR_BOUNDED
```

can become:

```
ABSENT
```

whereas:

```
NOT_FOUND
+
NO_ASSURANCE
```

must remain:

```
NOT_FOUND
```

---

<!-- CAP-663 | Continue Architecture Planning.md L75169–75171 | turn 59 | version 0.23 -->
## v0.23 — 23.23 The three epistemic outcomes

> **Source sections:** `CAP-663`

The engine should now be able to say three fundamentally different things:

<!-- CAP-664 | Continue Architecture Planning.md L75173–75183 | turn 59 | version 0.23 -->
### v0.23 — Presence

> **Source sections:** `CAP-664`

```
FOUND
```

with evidence:

```
Observation → Evidence → PresenceClaim
```

<!-- CAP-665 | Continue Architecture Planning.md L75185–75199 | turn 59 | version 0.23 -->
### v0.23 — Absence

> **Source sections:** `CAP-665`

```
ABSENT WITHIN SCOPE
```

with evidence:

```
Complete Enumeration
        ↓
Negative Evidence
        ↓
Absence Claim
```

<!-- CAP-666 | Continue Architecture Planning.md L75201–75223 | turn 59 | version 0.23 -->
### v0.23 — Unknown

> **Source sections:** `CAP-666`

```
NOT DETERMINED
```

because:

```
scope incomplete
OR
access unavailable
OR
enumeration incomplete
OR
strategies insufficient
OR
contradictory evidence
```

This is much safer than binary search results.

---
