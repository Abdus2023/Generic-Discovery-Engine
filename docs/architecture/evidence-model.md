# Evidence Model

> **Status:** DESIGNED
>
> **Source:** `Continue Architecture Planning.md`
>
> **Purpose:** Evidence: observations versus evidence versus claims, evidence graphs, strength and independence.

## Contents

- **v0.16 — EvidenceGraph + Provenance** — `Continue Architecture Planning.md` L63509–63552
- **v0.16 — 1. The new abstraction** — `Continue Architecture Planning.md` L63554–63588
- **v0.16 — Evidence** — `Continue Architecture Planning.md` L63607–63620
- **v0.16 — Claim** — `Continue Architecture Planning.md` L63622–63644
- **v0.16 — 3. Resource ≠ Claim** — `Continue Architecture Planning.md` L63646–63685
- **v0.16 — 4. EvidenceGraph** — `Continue Architecture Planning.md` L63687–63720
- **v0.16 — 6. Evidence object** — `Continue Architecture Planning.md` L63776–63817
- **v0.16 — 7. Locator** — `Continue Architecture Planning.md` L63819–63890
- **v0.16 — 8. Claim** — `Continue Architecture Planning.md` L63892–63944
- **v0.16 — 9. Claims should not be confused with truth** — `Continue Architecture Planning.md` L63946–63992
- **v0.16 — 10. Evidence strength** — `Continue Architecture Planning.md` L63994–64019
- **v0.16 — 11. Independent evidence** — `Continue Architecture Planning.md` L64021–64056
- **v0.16 — 12. Evidence independence** — `Continue Architecture Planning.md` L64058–64102
- **v0.16 — 13. Evidence graph edges** — `Continue Architecture Planning.md` L64104–64157
- **v0.16 — 14. Why graph edges matter** — `Continue Architecture Planning.md` L64159–64190
- **v0.16 — 16. Resource identity** — `Continue Architecture Planning.md` L64242–64285
- **v0.16 — 17. Resource fingerprint** — `Continue Architecture Planning.md` L64287–64321
- **v0.16 — 18. URL identity vs content identity** — `Continue Architecture Planning.md` L64323–64369
- **v0.16 — 19. Revision detection** — `Continue Architecture Planning.md` L64371–64406
- **v0.16 — 21. Evidence immutability** — `Continue Architecture Planning.md` L64443–64481
- **v0.16 — 22. Extraction method becomes first-class** — `Continue Architecture Planning.md` L64483–64512
- **v0.16 — 24. Evidence lifecycle** — `Continue Architecture Planning.md` L64557–64607
- **v0.16 — 25. Evidence states** — `Continue Architecture Planning.md` L64609–64655
- **v0.16 — 26. Claims can conflict** — `Continue Architecture Planning.md` L64657–64687
- **v0.16 — 27. Evidence resolution** — `Continue Architecture Planning.md` L64689–64719
- **v0.16 — 30. The evidence ledger** — `Continue Architecture Planning.md` L64786–64816
- **v0.16 — 31. Two complementary graphs** — `Continue Architecture Planning.md` L64818–64847
- **v0.16 — 32. Example end-to-end trace** — `Continue Architecture Planning.md` L64849–64929
- **v0.16 — Evidence provenance** — `Continue Architecture Planning.md` L64993–64999
- **v0.16 — Claim support** — `Continue Architecture Planning.md` L65001–65005
- **v0.16 — Historical integrity** — `Continue Architecture Planning.md` L65007–65011
- **v0.16 — Extraction integrity** — `Continue Architecture Planning.md` L65013–65017
- **v0.16 — Resource identity** — `Continue Architecture Planning.md` L65019–65024
- **v0.16 — Content identity** — `Continue Architecture Planning.md` L65026–65030
- **v0.16 — Conflict preservation** — `Continue Architecture Planning.md` L65032–65037
- **v0.16 — Execution** — `Continue Architecture Planning.md` L65168–65172
- **v0.16 — Work** — `Continue Architecture Planning.md` L65174–65178
- **v0.16 — Evidence** — `Continue Architecture Planning.md` L65198–65202
- **v0.16 — History** — `Continue Architecture Planning.md` L65204–65214
- **v0.17 — 13. Identity Evidence** — `Continue Architecture Planning.md` L65816–65848
- **v0.17 — Evidence-backed identity** — `Continue Architecture Planning.md` L66480–66485

## Related Documents

- [Provenance](provenance.md)
- [Resource, Representation and Revision Model](resource-model.md)
- [Coverage, Completeness and Absence](coverage-and-absence.md)
- [Verification](../validation/verification.md)

---

<!-- source: Continue Architecture Planning.md L63509–63552 | turn 45 | version 0.16 -->
## v0.16 — EvidenceGraph + Provenance

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

<!-- source: Continue Architecture Planning.md L63554–63588 | turn 45 | version 0.16 -->
## v0.16 — 1. The new abstraction

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

<!-- source: Continue Architecture Planning.md L63607–63620 | turn 45 | version 0.16 -->
### v0.16 — Evidence

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

<!-- source: Continue Architecture Planning.md L63622–63644 | turn 45 | version 0.16 -->
### v0.16 — Claim

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

<!-- source: Continue Architecture Planning.md L63646–63685 | turn 45 | version 0.16 -->
## v0.16 — 3. Resource ≠ Claim

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

<!-- source: Continue Architecture Planning.md L63687–63720 | turn 45 | version 0.16 -->
## v0.16 — 4. EvidenceGraph

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

<!-- source: Continue Architecture Planning.md L63776–63817 | turn 45 | version 0.16 -->
## v0.16 — 6. Evidence object

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

<!-- source: Continue Architecture Planning.md L63819–63890 | turn 45 | version 0.16 -->
## v0.16 — 7. Locator

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

<!-- source: Continue Architecture Planning.md L63892–63944 | turn 45 | version 0.16 -->
## v0.16 — 8. Claim

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

<!-- source: Continue Architecture Planning.md L63946–63992 | turn 45 | version 0.16 -->
## v0.16 — 9. Claims should not be confused with truth

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

<!-- source: Continue Architecture Planning.md L63994–64019 | turn 45 | version 0.16 -->
## v0.16 — 10. Evidence strength

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

<!-- source: Continue Architecture Planning.md L64021–64056 | turn 45 | version 0.16 -->
## v0.16 — 11. Independent evidence

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

<!-- source: Continue Architecture Planning.md L64058–64102 | turn 45 | version 0.16 -->
## v0.16 — 12. Evidence independence

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

<!-- source: Continue Architecture Planning.md L64104–64157 | turn 45 | version 0.16 -->
## v0.16 — 13. Evidence graph edges

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

<!-- source: Continue Architecture Planning.md L64159–64190 | turn 45 | version 0.16 -->
## v0.16 — 14. Why graph edges matter

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

<!-- source: Continue Architecture Planning.md L64242–64285 | turn 45 | version 0.16 -->
## v0.16 — 16. Resource identity

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

<!-- source: Continue Architecture Planning.md L64287–64321 | turn 45 | version 0.16 -->
## v0.16 — 17. Resource fingerprint

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

<!-- source: Continue Architecture Planning.md L64323–64369 | turn 45 | version 0.16 -->
## v0.16 — 18. URL identity vs content identity

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

<!-- source: Continue Architecture Planning.md L64371–64406 | turn 45 | version 0.16 -->
## v0.16 — 19. Revision detection

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

<!-- source: Continue Architecture Planning.md L64443–64481 | turn 45 | version 0.16 -->
## v0.16 — 21. Evidence immutability

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

<!-- source: Continue Architecture Planning.md L64483–64512 | turn 45 | version 0.16 -->
## v0.16 — 22. Extraction method becomes first-class

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

<!-- source: Continue Architecture Planning.md L64557–64607 | turn 45 | version 0.16 -->
## v0.16 — 24. Evidence lifecycle

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

<!-- source: Continue Architecture Planning.md L64609–64655 | turn 45 | version 0.16 -->
## v0.16 — 25. Evidence states

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

<!-- source: Continue Architecture Planning.md L64657–64687 | turn 45 | version 0.16 -->
## v0.16 — 26. Claims can conflict

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

<!-- source: Continue Architecture Planning.md L64689–64719 | turn 45 | version 0.16 -->
## v0.16 — 27. Evidence resolution

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

<!-- source: Continue Architecture Planning.md L64786–64816 | turn 45 | version 0.16 -->
## v0.16 — 30. The evidence ledger

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

<!-- source: Continue Architecture Planning.md L64818–64847 | turn 45 | version 0.16 -->
## v0.16 — 31. Two complementary graphs

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

<!-- source: Continue Architecture Planning.md L64849–64929 | turn 45 | version 0.16 -->
## v0.16 — 32. Example end-to-end trace

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

<!-- source: Continue Architecture Planning.md L64993–64999 | turn 45 | version 0.16 -->
### v0.16 — Evidence provenance

```
Every Evidence object
must reference an Observation or another
explicitly declared evidence source.
```

<!-- source: Continue Architecture Planning.md L65001–65005 | turn 45 | version 0.16 -->
### v0.16 — Claim support

```
A Claim should have explicit supporting Evidence.
```

<!-- source: Continue Architecture Planning.md L65007–65011 | turn 45 | version 0.16 -->
### v0.16 — Historical integrity

```
Observation is immutable historical evidence.
```

<!-- source: Continue Architecture Planning.md L65013–65017 | turn 45 | version 0.16 -->
### v0.16 — Extraction integrity

```
Evidence records extraction method/version.
```

<!-- source: Continue Architecture Planning.md L65019–65024 | turn 45 | version 0.16 -->
### v0.16 — Resource identity

```
Resource identity is not determined solely
by content fingerprint.
```

<!-- source: Continue Architecture Planning.md L65026–65030 | turn 45 | version 0.16 -->
### v0.16 — Content identity

```
Equal fingerprints do not imply equal resource identity.
```

<!-- source: Continue Architecture Planning.md L65032–65037 | turn 45 | version 0.16 -->
### v0.16 — Conflict preservation

```
Contradictory evidence must not silently overwrite
previous evidence.
```

<!-- source: Continue Architecture Planning.md L65168–65172 | turn 45 | version 0.16 -->
### v0.16 — Execution

> What scan is running?

`ScanSession`

<!-- source: Continue Architecture Planning.md L65174–65178 | turn 45 | version 0.16 -->
### v0.16 — Work

> What remains to be done?

`FrontierRuntime`

<!-- source: Continue Architecture Planning.md L65198–65202 | turn 45 | version 0.16 -->
### v0.16 — Evidence

> What supports that discovery?

`EvidenceGraph`

<!-- source: Continue Architecture Planning.md L65204–65214 | turn 45 | version 0.16 -->
### v0.16 — History

> What actually happened?

`EventLedger`

There is now one major missing layer:

> **How do we turn evidence into a stable, queryable interpretation of the discovered resource universe?**

That leads to the next abstraction:

<!-- source: Continue Architecture Planning.md L65816–65848 | turn 47 | version 0.17 -->
## v0.17 — 13. Identity Evidence

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

<!-- source: Continue Architecture Planning.md L66480–66485 | turn 47 | version 0.17 -->
### v0.17 — Evidence-backed identity

```
A non-trivial identity relation requires
explicit supporting evidence.
```
