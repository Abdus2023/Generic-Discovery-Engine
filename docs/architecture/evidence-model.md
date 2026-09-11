# Evidence Model

> **Status:** DESIGNED
>
> **Source:** `Continue Architecture Planning.md`
>
> **Purpose:** Evidence: observations versus evidence versus claims, evidence graphs, strength and independence.

## Source Sections

- **v0.16 — EvidenceGraph + Provenance** — `CAP-309` — `Continue Architecture Planning.md` L63509–63552
- **v0.16 — 1. The new abstraction** — `CAP-310` — `Continue Architecture Planning.md` L63554–63588
- **v0.16 — Evidence** — `CAP-313` — `Continue Architecture Planning.md` L63607–63620
- **v0.16 — Claim** — `CAP-314` — `Continue Architecture Planning.md` L63622–63644
- **v0.16 — 3. Resource ≠ Claim** — `CAP-315` — `Continue Architecture Planning.md` L63646–63685
- **v0.16 — 4. EvidenceGraph** — `CAP-316` — `Continue Architecture Planning.md` L63687–63720
- **v0.16 — 6. Evidence object** — `CAP-318` — `Continue Architecture Planning.md` L63776–63817
- **v0.16 — 7. Locator** — `CAP-319` — `Continue Architecture Planning.md` L63819–63890
- **v0.16 — 8. Claim** — `CAP-320` — `Continue Architecture Planning.md` L63892–63944
- **v0.16 — 9. Claims should not be confused with truth** — `CAP-321` — `Continue Architecture Planning.md` L63946–63992
- **v0.16 — 10. Evidence strength** — `CAP-322` — `Continue Architecture Planning.md` L63994–64019
- **v0.16 — 11. Independent evidence** — `CAP-323` — `Continue Architecture Planning.md` L64021–64056
- **v0.16 — 12. Evidence independence** — `CAP-324` — `Continue Architecture Planning.md` L64058–64102
- **v0.16 — 13. Evidence graph edges** — `CAP-325` — `Continue Architecture Planning.md` L64104–64157
- **v0.16 — 14. Why graph edges matter** — `CAP-326` — `Continue Architecture Planning.md` L64159–64190
- **v0.16 — 16. Resource identity** — `CAP-328` — `Continue Architecture Planning.md` L64242–64285
- **v0.16 — 17. Resource fingerprint** — `CAP-329` — `Continue Architecture Planning.md` L64287–64321
- **v0.16 — 18. URL identity vs content identity** — `CAP-330` — `Continue Architecture Planning.md` L64323–64369
- **v0.16 — 19. Revision detection** — `CAP-331` — `Continue Architecture Planning.md` L64371–64406
- **v0.16 — 21. Evidence immutability** — `CAP-333` — `Continue Architecture Planning.md` L64443–64481
- **v0.16 — 22. Extraction method becomes first-class** — `CAP-334` — `Continue Architecture Planning.md` L64483–64512
- **v0.16 — 24. Evidence lifecycle** — `CAP-336` — `Continue Architecture Planning.md` L64557–64607
- **v0.16 — 25. Evidence states** — `CAP-337` — `Continue Architecture Planning.md` L64609–64655
- **v0.16 — 26. Claims can conflict** — `CAP-338` — `Continue Architecture Planning.md` L64657–64687
- **v0.16 — 27. Evidence resolution** — `CAP-339` — `Continue Architecture Planning.md` L64689–64719
- **v0.16 — 30. The evidence ledger** — `CAP-342` — `Continue Architecture Planning.md` L64786–64816
- **v0.16 — 31. Two complementary graphs** — `CAP-343` — `Continue Architecture Planning.md` L64818–64847
- **v0.16 — 32. Example end-to-end trace** — `CAP-344` — `Continue Architecture Planning.md` L64849–64929
- **v0.16 — Evidence provenance** — `CAP-347` — `Continue Architecture Planning.md` L64993–64999
- **v0.16 — Claim support** — `CAP-348` — `Continue Architecture Planning.md` L65001–65005
- **v0.16 — Historical integrity** — `CAP-349` — `Continue Architecture Planning.md` L65007–65011
- **v0.16 — Extraction integrity** — `CAP-350` — `Continue Architecture Planning.md` L65013–65017
- **v0.16 — Resource identity** — `CAP-351` — `Continue Architecture Planning.md` L65019–65024
- **v0.16 — Content identity** — `CAP-352` — `Continue Architecture Planning.md` L65026–65030
- **v0.16 — Conflict preservation** — `CAP-353` — `Continue Architecture Planning.md` L65032–65037
- **v0.16 — Execution** — `CAP-360` — `Continue Architecture Planning.md` L65168–65172
- **v0.16 — Work** — `CAP-361` — `Continue Architecture Planning.md` L65174–65178
- **v0.16 — Evidence** — `CAP-365` — `Continue Architecture Planning.md` L65198–65202
- **v0.16 — History** — `CAP-366` — `Continue Architecture Planning.md` L65204–65214
- **v0.17 — 13. Identity Evidence** — `CAP-385` — `Continue Architecture Planning.md` L65816–65848
- **v0.17 — Evidence-backed identity** — `CAP-413` — `Continue Architecture Planning.md` L66480–66485

## Related Documents

- [Provenance](provenance.md)
- [Resource, Representation and Revision Model](resource-model.md)
- [Coverage, Completeness and Absence](coverage-and-absence.md)
- [Verification](../validation/verification.md)

---

<!-- CAP-309 | Continue Architecture Planning.md L63509–63552 | turn 45 | version 0.16 -->
## v0.16 — EvidenceGraph + Provenance

> **Source sections:** `CAP-309`

v0.15 solved the **work problem**.

We now have:

```
Domain
  ↓
Session
  ↓
Frontier
  ↓
Work
  ↓
Execution
```

But there is still a deeper epistemic problem:

> **Why should the engine believe that a candidate exists?**

At the moment, a discovery can effectively become:

```
"URL X was found."
```

That is insufficient for a serious discovery system.

We need:

```
"What observation produced X?"
"What mechanism extracted X?"
"What evidence supports that interpretation?"
"Can another independent path confirm X?"
"What artifact was actually observed?"
"When was it observed?"
```

This is the purpose of v0.16.

---

<!-- CAP-310 | Continue Architecture Planning.md L63554–63588 | turn 45 | version 0.16 -->
## v0.16 — 1. The new abstraction

> **Source sections:** `CAP-310`

The architecture becomes:

```
Observation
     ↓
Evidence
     ↓
Claim
     ↓
Resource / Candidate
```

More precisely:

```
             OBSERVATION
                  │
                  ▼
              EVIDENCE
                  │
                  ▼
                CLAIM
                  │
                  ▼
              RESOURCE
                  │
                  ▼
             CANDIDATE
```

These are deliberately different entities.

---

<!-- CAP-313 | Continue Architecture Planning.md L63607–63620 | turn 45 | version 0.16 -->
### v0.16 — Evidence

> **Source sections:** `CAP-313`

A structured representation extracted from the observation.

```JavaScript
{
    kind: 'html-link',
    value: '/manual.pdf',
    locator: {
        element: 'a',
        attribute: 'href'
    }
}
```

<!-- CAP-314 | Continue Architecture Planning.md L63622–63644 | turn 45 | version 0.16 -->
### v0.16 — Claim

> **Source sections:** `CAP-314`
>
> [DOCUMENTATION REVIEW] Contradiction **C-03** ([Review Notes](../REVIEW-NOTES.md#c-03--))

An assertion derived from evidence.

```
"https://example.com/manual.pdf is a discoverable resource."
```

Therefore:

```
Observation → Evidence → Claim
```

not:

```
Observation → Truth
```

The latter would overstate what the system knows.

---

<!-- CAP-315 | Continue Architecture Planning.md L63646–63685 | turn 45 | version 0.16 -->
## v0.16 — 3. Resource ≠ Claim

> **Source sections:** `CAP-315`
>
> [DOCUMENTATION REVIEW] Contradiction **C-03** ([Review Notes](../REVIEW-NOTES.md#c-03--))

A resource is an identity in the discovery universe.

For example:

```
https://example.com/manual.pdf
```

A claim is an assertion about that resource:

```
resource exists
resource is PDF
resource is linked from page X
resource was observed at time T
resource has fingerprint H
```

One resource can have many claims:

```
RESOURCE
   │
   ├── exists
   ├── type = PDF
   ├── linked by page A
   ├── linked by page B
   ├── discovered through sitemap
   └── observed with fingerprint H
```

This is much richer than storing:

```JavaScript
resource.discoveryCount = 3;
```

---

<!-- CAP-316 | Continue Architecture Planning.md L63687–63720 | turn 45 | version 0.16 -->
## v0.16 — 4. EvidenceGraph

> **Source sections:** `CAP-316`

The KnowledgeBase can therefore contain an explicit evidence graph.

```
                  ┌──────────────┐
                  │  OBSERVATION │
                  └──────┬───────┘
                         │
                    supports
                         │
                         ▼
                  ┌──────────────┐
                  │   EVIDENCE   │
                  └──────┬───────┘
                         │
                    supports
                         │
                         ▼
                  ┌──────────────┐
                  │    CLAIM     │
                  └──────┬───────┘
                         │
                     concerns
                         │
                         ▼
                  ┌──────────────┐
                  │   RESOURCE   │
                  └──────────────┘
```

But we also need provenance.

---

<!-- CAP-318 | Continue Architecture Planning.md L63776–63817 | turn 45 | version 0.16 -->
## v0.16 — 6. Evidence object

> **Source sections:** `CAP-318`

Conceptually:

```JavaScript
class Evidence {
    constructor(data = {}) {
        this.id =
            data.id || makeId('evidence');

        this.kind =
            data.kind || 'unknown';

        this.value =
            data.value ?? null;

        this.observationId =
            data.observationId || null;

        this.sessionId =
            data.sessionId || null;

        this.locator =
            data.locator || null;

        this.provenance =
            data.provenance || {};

        this.confidence =
            Number.isFinite(data.confidence)
                ? data.confidence
                : 0.5;

        this.createdAt =
            data.createdAt || now();
    }
}
```

The important part is that evidence references the observation from which it came.

---

<!-- CAP-319 | Continue Architecture Planning.md L63819–63890 | turn 45 | version 0.16 -->
## v0.16 — 7. Locator

> **Source sections:** `CAP-319`

For document discovery, provenance needs a locator.

HTML:

```JavaScript
{
    kind: 'html-link',

    locator: {
        element: 'a',
        attribute: 'href',
        selector: 'a[href]',
        value: '/manual.pdf'
    }
}
```

JSON:

```JavaScript
{
    kind: 'json-url',

    locator: {
        path: '$.documents[3].download'
    }
}
```

XML:

```JavaScript
{
    kind: 'xml-loc',

    locator: {
        element: 'loc',
        index: 17
    }
}
```

CSS:

```JavaScript
{
    kind: 'css-url',

    locator: {
        rule: '@font-face',
        property: 'src'
    }
}
```

JavaScript:

```JavaScript
{
    kind: 'javascript-url',

    locator: {
        mechanism: 'string-literal'
    }
}
```

This is the beginning of **reproducible extraction**.

---

<!-- CAP-320 | Continue Architecture Planning.md L63892–63944 | turn 45 | version 0.16 -->
## v0.16 — 8. Claim

> **Source sections:** `CAP-320`
>
> [DOCUMENTATION REVIEW] Contradiction **C-03** ([Review Notes](../REVIEW-NOTES.md#c-03--))

A claim should be explicit.

```JavaScript
class Claim {
    constructor(data = {}) {
        this.id =
            data.id || makeId('claim');

        this.subject =
            data.subject || null;

        this.predicate =
            data.predicate || null;

        this.object =
            data.object ?? null;

        this.evidenceIds =
            data.evidenceIds || [];

        this.sessionId =
            data.sessionId || null;

        this.confidence =
            Number.isFinite(data.confidence)
                ? data.confidence
                : 0.5;

        this.createdAt =
            data.createdAt || now();
    }
}
```

Example:

```JavaScript
{
    subject: 'https://example.com/manual.pdf',

    predicate: 'discovered-from',

    object: 'https://example.com/docs',

    evidenceIds: [
        'ev-123'
    ]
}
```

---

<!-- CAP-321 | Continue Architecture Planning.md L63946–63992 | turn 45 | version 0.16 -->
## v0.16 — 9. Claims should not be confused with truth

> **Source sections:** `CAP-321`
>
> [DOCUMENTATION REVIEW] Contradiction **C-03** ([Review Notes](../REVIEW-NOTES.md#c-03--))

This is an important epistemic boundary.

The engine should say:

```
CLAIM:
Resource X was referenced by page Y.
```

rather than:

```
FACT:
Resource X definitely exists.
```

A link is evidence for discoverability.

It is not necessarily proof that the target is currently accessible.

Therefore:

```
linked
    ≠
accessible
```

Likewise:

```
URL ends in .pdf
    ≠
response is actually PDF
```

And:

```
HTTP 200
    ≠
resource is semantically valid
```

---

<!-- CAP-322 | Continue Architecture Planning.md L63994–64019 | turn 45 | version 0.16 -->
## v0.16 — 10. Evidence strength

> **Source sections:** `CAP-322`

We can classify evidence.

For example:

| Evidence | Strength |
| --- | --- |
| URL string | Low |
| HTML href | Medium |
| Sitemap `<loc>` | Medium |
| HTTP 200 | Medium |
| Content-Type | Medium |
| Magic bytes | High |
| Cryptographic hash | Very high for byte identity |
| Independent repeated observation | Strengthening evidence |

But these should not simply become one arbitrary numeric score.

The system should preserve the underlying evidence.

This is the same principle established earlier:

> **Do not collapse independent evidence into a single opaque confidence value.**

---

<!-- CAP-323 | Continue Architecture Planning.md L64021–64056 | turn 45 | version 0.16 -->
## v0.16 — 11. Independent evidence

> **Source sections:** `CAP-323`

Suppose:

```
Page A → manual.pdf
Page B → manual.pdf
Sitemap → manual.pdf
```

We now have:

```
Resource
   ↑
   │
 ┌─┼───────────────┐
 │ │               │
 ▼ ▼               ▼
A-link             B-link
                     │
                     ▼
                 sitemap
```

The resource has three discovery paths.

That is much more useful than:

```JavaScript
discoveryCount = 3
```

because the paths themselves are preserved.

---

<!-- CAP-324 | Continue Architecture Planning.md L64058–64102 | turn 45 | version 0.16 -->
## v0.16 — 12. Evidence independence

> **Source sections:** `CAP-324`

But there is another subtle issue.

Suppose:

```
Page A
  ↓
iframe B
  ↓
Page C
  ↓
manual.pdf
```

and:

```
Page A
  ↓
network observation
  ↓
manual.pdf
```

These may not actually be independent.

They may both originate from the same underlying application mechanism.

Therefore:

```
number of evidence objects
```

does not necessarily equal:

```
number of independent confirmations
```

We should preserve the provenance graph and let later verification logic determine independence.

---

<!-- CAP-325 | Continue Architecture Planning.md L64104–64157 | turn 45 | version 0.16 -->
## v0.16 — 13. Evidence graph edges

> **Source sections:** `CAP-325`

Instead of only storing arrays, explicitly model relationships:

```JavaScript
{
    from: 'obs-123',
    to: 'ev-456',
    relation: 'produced'
}
```

Then:

```JavaScript
{
    from: 'ev-456',
    to: 'claim-789',
    relation: 'supports'
}
```

And:

```JavaScript
{
    from: 'claim-789',
    to: 'resource-42',
    relation: 'concerns'
}
```

Graph:

```
obs-123
   │
produced
   │
   ▼
ev-456
   │
supports
   │
   ▼
claim-789
   │
concerns
   │
   ▼
resource-42
```

---

<!-- CAP-326 | Continue Architecture Planning.md L64159–64190 | turn 45 | version 0.16 -->
## v0.16 — 14. Why graph edges matter

> **Source sections:** `CAP-326`

Previously the engine had:

```
candidate.parent
candidate.origin
discovery.provenance
```

Those fields are useful but become increasingly awkward as relationships multiply.

For example:

```
Observation A
   supports Evidence B
Evidence B
   supports Claim C
Claim C
   concerns Resource D
Observation A
   derived from Acquisition E
Acquisition E
   generated by Candidate F
Candidate F
   discovered by Evidence G
```

This is naturally a graph.

---

<!-- CAP-328 | Continue Architecture Planning.md L64242–64285 | turn 45 | version 0.16 -->
## v0.16 — 16. Resource identity

> **Source sections:** `CAP-328`
>
> [DOCUMENTATION REVIEW] Contradiction **C-04** ([Review Notes](../REVIEW-NOTES.md#c-04--))

The resource remains identified independently of evidence.

For example:

```
Resource Identity
=
canonical URL
```

initially.

But v0.16 should explicitly acknowledge that URL identity is imperfect.

Consider:

```
/page
/page/
?page=1
```

Canonicalization may collapse some of these.

Or:

```
/download?id=123
/download?id=456
```

may point to different resources.

Therefore:

```
canonical URL
```

is an **identity hypothesis**, not universal truth.

---

<!-- CAP-329 | Continue Architecture Planning.md L64287–64321 | turn 45 | version 0.16 -->
## v0.16 — 17. Resource fingerprint

> **Source sections:** `CAP-329`
>
> [DOCUMENTATION REVIEW] Contradiction **C-07** ([Review Notes](../REVIEW-NOTES.md#c-07--))

When bytes are obtained:

```
Observation
   ↓
body
   ↓
hash
   ↓
fingerprint
```

For example:

```JavaScript
{
    algorithm: 'sha256',
    digest: '...',
    size: 481239
}
```

This provides a second identity dimension:

```
URL identity
+
content identity
```

These should not be merged.

---

<!-- CAP-330 | Continue Architecture Planning.md L64323–64369 | turn 45 | version 0.16 -->
## v0.16 — 18. URL identity vs content identity

> **Source sections:** `CAP-330`
>
> [DOCUMENTATION REVIEW] Contradiction **C-04** ([Review Notes](../REVIEW-NOTES.md#c-04--))

Example:

```
URL A → hash X
URL B → hash X
```

This means:

```
different URLs
same observed bytes
```

The engine should record:

```
A ─────┐
       ├── hash X
B ─────┘
```

but should **not** automatically conclude:

```
A = B
```

They may be:

* aliases
* mirrors
* cached copies
* different resources with identical content
* generated duplicate endpoints

Therefore:

```
same fingerprint
≠
same resource identity
```

---

<!-- CAP-331 | Continue Architecture Planning.md L64371–64406 | turn 45 | version 0.16 -->
## v0.16 — 19. Revision detection

> **Source sections:** `CAP-331`
>
> [DOCUMENTATION REVIEW] Contradiction **C-07** ([Review Notes](../REVIEW-NOTES.md#c-07--))

Now consider:

```
Scan A
URL X → hash A

Scan B
URL X → hash B
```

We can detect:

```
resource changed
```

without changing the resource identity.

Graph:

```
             RESOURCE X
              /       \
             /         \
         Scan A       Scan B
           │             │
         hash A        hash B
```

This becomes extremely important for document acquisition.

A manual can remain the same logical resource while its bytes change.

---

<!-- CAP-333 | Continue Architecture Planning.md L64443–64481 | turn 45 | version 0.16 -->
## v0.16 — 21. Evidence immutability

> **Source sections:** `CAP-333`

Likewise, once an extraction was made:

```
Observation O
    ↓
Evidence E
```

we should not rewrite E because a later parser version produces a different result.

Instead:

```
Parser v1
    ↓
Evidence E1

Parser v2
    ↓
Evidence E2
```

Both remain attributable to their extraction method.

This gives:

```
parser version
+
observation
+
evidence
```

as reproducibility metadata.

---

<!-- CAP-334 | Continue Architecture Planning.md L64483–64512 | turn 45 | version 0.16 -->
## v0.16 — 22. Extraction method becomes first-class

> **Source sections:** `CAP-334`

An evidence record should contain:

```JavaScript
{
    extraction: {
        providerId: 'html',
        providerVersion: '0.16.0',
        method: 'anchor-href'
    }
}
```

Then:

```
Same observation
      │
 ┌────┴────┐
 ▼         ▼
Parser v1 Parser v2
 │         │
 ▼         ▼
Evidence1 Evidence2
```

This is the foundation for parser evolution without destroying historical provenance.

---

<!-- CAP-336 | Continue Architecture Planning.md L64557–64607 | turn 45 | version 0.16 -->
## v0.16 — 24. Evidence lifecycle

> **Source sections:** `CAP-336`

Conceptually:

```
Reference discovered
        ↓
Weak evidence
        ↓
Candidate created
        ↓
Acquisition
        ↓
Observation
        ↓
Recognition
        ↓
Stronger evidence
        ↓
Claim strengthened
```

This is a major conceptual improvement.

Discovery is no longer binary.

It can evolve from:

```
"someone referenced it"
```

toward:

```
"we actually observed it"
```

toward:

```
"we verified its content type"
```

toward:

```
"we verified its exact bytes"
```

---

<!-- CAP-337 | Continue Architecture Planning.md L64609–64655 | turn 45 | version 0.16 -->
## v0.16 — 25. Evidence states

> **Source sections:** `CAP-337`

We should avoid treating evidence as simply:

```
true / false
```

Instead:

```
observed
derived
verified
contradicted
superseded
```

For example:

```
Evidence:
Content-Type: application/pdf
```

could later be contradicted by:

```
Magic bytes:
HTML document
```

The engine should preserve both.

```
Evidence A
Content-Type = PDF
        │
        │ contradicted-by
        ▼
Evidence B
Magic bytes = HTML
```

This is much better than silently overwriting the first observation.

---

<!-- CAP-338 | Continue Architecture Planning.md L64657–64687 | turn 45 | version 0.16 -->
## v0.16 — 26. Claims can conflict

> **Source sections:** `CAP-338`
>
> [DOCUMENTATION REVIEW] Contradiction **C-03** ([Review Notes](../REVIEW-NOTES.md#c-03--))

Example:

```
Claim A:
resource type = PDF

Claim B:
resource type = HTML
```

Both may be supported by different observations.

The graph should preserve the conflict:

```
              RESOURCE
               │
        ┌──────┴──────┐
        ▼             ▼
     Claim A        Claim B
       │              │
     PDF             HTML
```

A later resolver may determine which claim currently has stronger support.

But the evidence history is never destroyed.

---

<!-- CAP-339 | Continue Architecture Planning.md L64689–64719 | turn 45 | version 0.16 -->
## v0.16 — 27. Evidence resolution

> **Source sections:** `CAP-339`

This suggests a future component:

```
EvidenceResolver
```

but **not yet** as a large v0.16 subsystem.

For now:

```
EvidenceGraph
```

stores the competing evidence.

Later:

```
EvidenceGraph
      ↓
EvidenceResolver
      ↓
Current Resource Interpretation
```

This prevents premature confidence logic.

---

<!-- CAP-342 | Continue Architecture Planning.md L64786–64816 | turn 45 | version 0.16 -->
## v0.16 — 30. The evidence ledger

> **Source sections:** `CAP-342`

We already have an event ledger:

```
what happened?
```

The evidence graph answers a different question:

```
what supports what?
```

Therefore:

```
EVENT LEDGER
    =
    temporal execution history

EVIDENCE GRAPH
    =
    epistemic/provenance structure
```

These should remain separate.

This distinction is extremely important.

---

<!-- CAP-343 | Continue Architecture Planning.md L64818–64847 | turn 45 | version 0.16 -->
## v0.16 — 31. Two complementary graphs

> **Source sections:** `CAP-343`

We now have:

```
             EVENT GRAPH
          "What happened?"
                 │
                 │
                 ▼
        ┌─────────────────┐
        │   EVENT LEDGER  │
        └─────────────────┘


             EVIDENCE GRAPH
          "Why believe it?"
                 │
                 │
                 ▼
        ┌─────────────────┐
        │  EVIDENCE GRAPH │
        └─────────────────┘
```

An event can create evidence.

But an event itself is not necessarily evidence.

---

<!-- CAP-344 | Continue Architecture Planning.md L64849–64929 | turn 45 | version 0.16 -->
## v0.16 — 32. Example end-to-end trace

> **Source sections:** `CAP-344`

Suppose the seed is:

```
https://example.com/docs
```

The browser acquires it.

```
Scan
 ↓
Candidate
 ↓
Acquisition
 ↓
Observation O1
```

HTML recognition finds:

```HTML
<a href="/manual.pdf">
```

Then:

```
O1
 ↓
Evidence E1
 ↓
Claim C1
 ↓
Resource R1
 ↓
Candidate CAND1
```

Later the candidate is acquired:

```
CAND1
 ↓
Acquisition
 ↓
Observation O2
```

O2 contains:

```
Content-Type: application/pdf
Magic bytes: %PDF-
```

Now:

```
O2
 ├── Evidence E2
 │      └── content-type
 │
 └── Evidence E3
        └── magic-bytes
```

And:

```
E2 + E3
      ↓
Claims
      ↓
Resource R1
```

The resulting graph explains not just **what was found**, but **how the engine came to know it**.

---

<!-- CAP-347 | Continue Architecture Planning.md L64993–64999 | turn 45 | version 0.16 -->
### v0.16 — Evidence provenance

> **Source sections:** `CAP-347`

```
Every Evidence object
must reference an Observation or another
explicitly declared evidence source.
```

<!-- CAP-348 | Continue Architecture Planning.md L65001–65005 | turn 45 | version 0.16 -->
### v0.16 — Claim support

> **Source sections:** `CAP-348`
>
> [DOCUMENTATION REVIEW] Contradiction **C-03** ([Review Notes](../REVIEW-NOTES.md#c-03--))

```
A Claim should have explicit supporting Evidence.
```

<!-- CAP-349 | Continue Architecture Planning.md L65007–65011 | turn 45 | version 0.16 -->
### v0.16 — Historical integrity

> **Source sections:** `CAP-349`

```
Observation is immutable historical evidence.
```

<!-- CAP-350 | Continue Architecture Planning.md L65013–65017 | turn 45 | version 0.16 -->
### v0.16 — Extraction integrity

> **Source sections:** `CAP-350`

```
Evidence records extraction method/version.
```

<!-- CAP-351 | Continue Architecture Planning.md L65019–65024 | turn 45 | version 0.16 -->
### v0.16 — Resource identity

> **Source sections:** `CAP-351`
>
> [DOCUMENTATION REVIEW] Contradiction **C-04** ([Review Notes](../REVIEW-NOTES.md#c-04--))

```
Resource identity is not determined solely
by content fingerprint.
```

<!-- CAP-352 | Continue Architecture Planning.md L65026–65030 | turn 45 | version 0.16 -->
### v0.16 — Content identity

> **Source sections:** `CAP-352`
>
> [DOCUMENTATION REVIEW] Contradiction **C-04** ([Review Notes](../REVIEW-NOTES.md#c-04--))

```
Equal fingerprints do not imply equal resource identity.
```

<!-- CAP-353 | Continue Architecture Planning.md L65032–65037 | turn 45 | version 0.16 -->
### v0.16 — Conflict preservation

> **Source sections:** `CAP-353`

```
Contradictory evidence must not silently overwrite
previous evidence.
```

<!-- CAP-360 | Continue Architecture Planning.md L65168–65172 | turn 45 | version 0.16 -->
### v0.16 — Execution

> **Source sections:** `CAP-360`

> What scan is running?

`ScanSession`

<!-- CAP-361 | Continue Architecture Planning.md L65174–65178 | turn 45 | version 0.16 -->
### v0.16 — Work

> **Source sections:** `CAP-361`

> What remains to be done?

`FrontierRuntime`

<!-- CAP-365 | Continue Architecture Planning.md L65198–65202 | turn 45 | version 0.16 -->
### v0.16 — Evidence

> **Source sections:** `CAP-365`

> What supports that discovery?

`EvidenceGraph`

<!-- CAP-366 | Continue Architecture Planning.md L65204–65214 | turn 45 | version 0.16 -->
### v0.16 — History

> **Source sections:** `CAP-366`

> What actually happened?

`EventLedger`

There is now one major missing layer:

> **How do we turn evidence into a stable, queryable interpretation of the discovered resource universe?**

That leads to the next abstraction:

<!-- CAP-385 | Continue Architecture Planning.md L65816–65848 | turn 47 | version 0.17 -->
## v0.17 — 13. Identity Evidence

> **Source sections:** `CAP-385`
>
> [DOCUMENTATION REVIEW] Contradiction **C-04** ([Review Notes](../REVIEW-NOTES.md#c-04--))

Identity resolution must never simply say:

```JavaScript
if (hashA === hashB) {
    resources.merge();
}
```

Instead it should produce an **identity decision** backed by evidence.

Example:

```JavaScript
{
    relation: 'same-content-as',

    left: 'resource-A',
    right: 'resource-B',

    evidenceIds: [
        'evidence-hash-1',
        'evidence-hash-2'
    ],

    confidence: 1.0
}
```

The relationship itself becomes a graph fact.

---

<!-- CAP-413 | Continue Architecture Planning.md L66480–66485 | turn 47 | version 0.17 -->
### v0.17 — Evidence-backed identity

> **Source sections:** `CAP-413`
>
> [DOCUMENTATION REVIEW] Contradiction **C-04** ([Review Notes](../REVIEW-NOTES.md#c-04--))

```
A non-trivial identity relation requires
explicit supporting evidence.
```
