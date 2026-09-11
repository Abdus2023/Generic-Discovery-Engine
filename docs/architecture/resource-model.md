# Resource, Representation and Revision Model

> **Status:** OPEN
>
> **Source:** `Continue Architecture Planning.md`; `Userscript Discovery Prototype.md`
>
> **Purpose:** Resources, locators, representations, artifacts, identity resolution and revision detection.

## Source Sections

- **21. Handle disappearing multiplexes** — `USP-036` — `Userscript Discovery Prototype.md` L993–1023
- **v0.17 — ResourceGraph + Identity Resolution** — `CAP-367` — `Continue Architecture Planning.md` L65216–65240
- **v0.17 — ResourceGraph + Identity Resolution** — `CAP-369` — `Continue Architecture Planning.md` L65252–65295
- **v0.17 — 1. The core problem** — `CAP-370` — `Continue Architecture Planning.md` L65297–65336
- **v0.17 — 2. Resource identity must become graph-based** — `CAP-371` — `Continue Architecture Planning.md` L65338–65371
- **v0.17 — 3. Candidate vs Resource vs Locator** — `CAP-372` — `Continue Architecture Planning.md` L65373–65375
- **v0.17 — Candidate** — `CAP-373` — `Continue Architecture Planning.md` L65377–65385
- **v0.17 — Locator** — `CAP-374` — `Continue Architecture Planning.md` L65387–65395
- **v0.17 — Resource** — `CAP-375` — `Continue Architecture Planning.md` L65397–65429
- **v0.17 — 4. Why not simply canonicalize everything?** — `CAP-376` — `Continue Architecture Planning.md` L65431–65477
- **v0.17 — 5. Locator** — `CAP-377` — `Continue Architecture Planning.md` L65479–65526
- **v0.17 — 6. Resource** — `CAP-378` — `Continue Architecture Planning.md` L65528–65570
- **v0.17 — 7. Resource relationships** — `CAP-379` — `Continue Architecture Planning.md` L65572–65613
- **v0.17 — 8. Redirects** — `CAP-380` — `Continue Architecture Planning.md` L65615–65653
- **v0.17 — 9. Redirect chain** — `CAP-381` — `Continue Architecture Planning.md` L65655–65693
- **v0.17 — 10. Content fingerprints** — `CAP-382` — `Continue Architecture Planning.md` L65695–65726
- **v0.17 — 11. Same content does not prove same resource** — `CAP-383` — `Continue Architecture Planning.md` L65728–65775
- **v0.17 — 12. Representation identity** — `CAP-384` — `Continue Architecture Planning.md` L65777–65814
- **v0.17 — 14. IdentityResolver** — `CAP-386` — `Continue Architecture Planning.md` L65850–65890
- **v0.17 — 15. Identity confidence should be relational** — `CAP-387` — `Continue Architecture Planning.md` L65892–65916
- **v0.17 — 16. Identity classes** — `CAP-388` — `Continue Architecture Planning.md` L65918–65952
- **v0.17 — 17. No destructive merges** — `CAP-389` — `Continue Architecture Planning.md` L65954–65990
- **v0.17 — 18. ResourceGraph** — `CAP-390` — `Continue Architecture Planning.md` L65992–66040
- **v0.17 — 19. Graph edge contract** — `CAP-391` — `Continue Architecture Planning.md` L66042–66080
- **v0.17 — 20. Identity resolution pipeline** — `CAP-392` — `Continue Architecture Planning.md` L66082–66119
- **v0.17 — 21. Canonical URL is still important** — `CAP-393` — `Continue Architecture Planning.md` L66121–66167
- **v0.17 — 23. Identity resolution must be monotonic where possible** — `CAP-395` — `Continue Architecture Planning.md` L66197–66235
- **v0.17 — 24. Resource revisions** — `CAP-396` — `Continue Architecture Planning.md` L66237–66274
- **v0.17 — 25. Revision object** — `CAP-397` — `Continue Architecture Planning.md` L66276–66303
- **v0.17 — 26. ResourceGraph vs KnowledgeBase** — `CAP-398` — `Continue Architecture Planning.md` L66305–66323
- **v0.17 — What URLs identify this resource?** — `CAP-400` — `Continue Architecture Planning.md` L66329–66333
- **v0.17 — Where was it discovered?** — `CAP-401` — `Continue Architecture Planning.md` L66335–66342
- **v0.17 — What URLs redirect to it?** — `CAP-402` — `Continue Architecture Planning.md` L66344–66348
- **v0.17 — Which URLs have identical observed bytes?** — `CAP-403` — `Continue Architecture Planning.md` L66350–66354
- **v0.17 — Has this resource changed?** — `CAP-404` — `Continue Architecture Planning.md` L66356–66362
- **v0.17 — Why do we believe two URLs are related?** — `CAP-405` — `Continue Architecture Planning.md` L66364–66378
- **v0.17 — 28. Resource graph example** — `CAP-406` — `Continue Architecture Planning.md` L66380–66420
- **v0.17 — Locator preservation** — `CAP-409` — `Continue Architecture Planning.md` L66452–66457
- **v0.17 — No destructive merge** — `CAP-410` — `Continue Architecture Planning.md` L66459–66464
- **v0.17 — Fingerprint independence** — `CAP-411` — `Continue Architecture Planning.md` L66466–66471
- **v0.17 — Redirect independence** — `CAP-412` — `Continue Architecture Planning.md` L66473–66478
- **v0.17 — Revision preservation** — `CAP-414` — `Continue Architecture Planning.md` L66487–66492
- **v0.17 — Canonicalization transparency** — `CAP-415` — `Continue Architecture Planning.md` L66494–66501
- **v0.17 — 33. The important transition** — `CAP-418` — `Continue Architecture Planning.md` L66608–66651
- **v0.19 — Resource Representation & Revision Model** — `CAP-457` — `Continue Architecture Planning.md` L68083–68147
- **v0.19 — Resource Representation + Artifact + Revision Model** — `CAP-459` — `Continue Architecture Planning.md` L68159–68177
- **v0.19 — 19.1 The Core Distinction** — `CAP-460` — `Continue Architecture Planning.md` L68179–68207
- **v0.19 — Resource** — `CAP-461` — `Continue Architecture Planning.md` L68209–68217
- **v0.19 — Representation** — `CAP-462` — `Continue Architecture Planning.md` L68219–68228
- **v0.19 — Artifact** — `CAP-463` — `Continue Architecture Planning.md` L68230–68237
- **v0.19 — 19.2 Why Resource → Artifact Is Wrong** — `CAP-465` — `Continue Architecture Planning.md` L68252–68300
- **v0.19 — 19.3 New Data Model** — `CAP-466` — `Continue Architecture Planning.md` L68302–68417
- **v0.19 — 19.4 The Complete Identity Chain** — `CAP-467` — `Continue Architecture Planning.md` L68419–68463
- **v0.19 — 19.5 Representation Is Not Just MIME** — `CAP-468` — `Continue Architecture Planning.md` L68465–68516
- **v0.19 — 19.6 Representation Relations** — `CAP-469` — `Continue Architecture Planning.md` L68518–68543
- **v0.19 — 19.7 Artifact Identity** — `CAP-470` — `Continue Architecture Planning.md` L68545–68591
- **v0.19 — 19.8 Content Equivalence** — `CAP-471` — `Continue Architecture Planning.md` L68593–68636
- **v0.19 — 19.9 Revision Detection** — `CAP-472` — `Continue Architecture Planning.md` L68638–68678
- **v0.19 — 19.10 Revision Detection Is Not Always Proof of Semantic Revision** — `CAP-473` — `Continue Architecture Planning.md` L68680–68729
- **v0.19 — 19.11 Revision Evidence** — `CAP-474` — `Continue Architecture Planning.md` L68731–68772
- **v0.19 — 19.12 HTTP Validators Become Evidence** — `CAP-475` — `Continue Architecture Planning.md` L68774–68809
- **v0.19 — 19.15 Resource State vs Artifact State** — `CAP-478` — `Continue Architecture Planning.md` L68904–68935
- **v0.19 — Resource state** — `CAP-479` — `Continue Architecture Planning.md` L68937–68945
- **v0.19 — Artifact state** — `CAP-480` — `Continue Architecture Planning.md` L68947–68955
- **v0.19 — 19.16 ResourceGraph v0.19** — `CAP-482` — `Continue Architecture Planning.md` L68971–69004
- **v0.19 — 19.17 ResourceGraph API** — `CAP-483` — `Continue Architecture Planning.md` L69006–69073
- **v0.19 — 19.18 Artifact Deduplication** — `CAP-484` — `Continue Architecture Planning.md` L69075–69087
- **v0.19 — Locator deduplication** — `CAP-485` — `Continue Architecture Planning.md` L69089–69095
- **v0.19 — Artifact deduplication** — `CAP-486` — `Continue Architecture Planning.md` L69097–69127
- **v0.19 — 19.19 Content-Addressed Storage** — `CAP-487` — `Continue Architecture Planning.md` L69129–69181
- **v0.19 — 19.21 Independent Confirmation** — `CAP-489` — `Continue Architecture Planning.md` L69222–69271
- **v0.19 — 19.22 Resource Confidence** — `CAP-490` — `Continue Architecture Planning.md` L69273–69310
- **v0.19 — 19.23 Example** — `CAP-491` — `Continue Architecture Planning.md` L69312–69318
- **v0.19 — Step 1 — Locator** — `CAP-492` — `Continue Architecture Planning.md` L69320–69325
- **v0.19 — Step 2 — Resource** — `CAP-493` — `Continue Architecture Planning.md` L69327–69331
- **v0.19 — Step 4 — Artifact** — `CAP-495` — `Continue Architecture Planning.md` L69341–69346
- **v0.19 — Step 5 — Representation** — `CAP-496` — `Continue Architecture Planning.md` L69348–69354
- **v0.19 — Step 6 — Classification** — `CAP-497` — `Continue Architecture Planning.md` L69356–69361
- **v0.19 — Step 7 — Revision** — `CAP-498` — `Continue Architecture Planning.md` L69363–69397
- **v0.19 — 19.24 A More Precise End-to-End Pipeline** — `CAP-499` — `Continue Architecture Planning.md` L69399–69452
- **v0.19 — 19.27 What v0.19 Gives Us** — `CAP-510` — `Continue Architecture Planning.md` L69569–69657

## Related Documents

- [Evidence Model](evidence-model.md)
- [Resource Type System and Classification](classification.md)
- [Coverage, Completeness and Absence](coverage-and-absence.md)
- [System Model](system-model.md)

---

<!-- USP-036 | Userscript Discovery Prototype.md L993–1023 | turn 7 | version ? -->
## 21. Handle disappearing multiplexes

> **Source sections:** `USP-036`

Discovery should also be able to represent negative information.

For example:

```
Multiplex X
    previously seen: 17 times
    currently seen: 0 times
```

Don't immediately delete it.

Instead:

```
ACTIVE
  ↓
NOT_SEEN_ONCE
  ↓
NOT_SEEN_REPEATEDLY
  ↓
STALE
  ↓
REMOVED
```

That prevents transient reception problems from being interpreted as network changes.

---

<!-- CAP-367 | Continue Architecture Planning.md L65216–65240 | turn 45 | version 0.17 -->
## v0.17 — ResourceGraph + Identity Resolution

> **Source sections:** `CAP-367`
>
> [DOCUMENTATION REVIEW] Contradiction **C-04** ([Review Notes](../REVIEW-NOTES.md#c-04--))

The central problem will be:

```
                  EVIDENCE
                     │
            ┌────────┴────────┐
            ▼                 ▼
         URL A              URL B
            │                 │
            └────────┬────────┘
                     ▼
             Identity Resolver
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
      same resource?       different resource?
          │                     │
          └──────────┬──────────┘
                     ▼
                RESOURCE GRAPH
```

That is where canonical URLs, redirects, content fingerprints, aliases, mirrors, revisions, MIME identity, and conflicting observations can finally be modeled without abusing the candidate model.

<!-- CAP-369 | Continue Architecture Planning.md L65252–65295 | turn 47 | version 0.17 -->
## v0.17 — ResourceGraph + Identity Resolution

> **Source sections:** `CAP-369`
>
> [DOCUMENTATION REVIEW] Contradiction **C-04** ([Review Notes](../REVIEW-NOTES.md#c-04--))

v0.16 established the provenance chain:

```
Observation
    ↓
Evidence
    ↓
Claim
    ↓
Resource
```

But `Resource` is still too simple.

The engine currently tends toward:

```
canonical URL → resource
```

That breaks down quickly in real web discovery.

A single logical document can have:

```
multiple URLs
redirects
aliases
mirrors
query variants
download endpoints
different representations
different revisions
```

while two URLs that look related may actually identify completely different resources.

So v0.17 introduces:

> **ResourceGraph + Identity Resolution**

---

<!-- CAP-370 | Continue Architecture Planning.md L65297–65336 | turn 47 | version 0.17 -->
## v0.17 — 1. The core problem

> **Source sections:** `CAP-370`

Consider:

```
https://example.com/manual.pdf
https://example.com/download?id=42
https://cdn.example.com/manual.pdf
```

Are these:

```
A = B = C
```

or:

```
A ≠ B ≠ C
```

or perhaps:

```
A = B
C = mirror(A)
```

A crawler cannot safely answer this merely from URL strings.

Likewise:

```
URL A → HTTP 301 → URL B
```

is strong evidence of an alias relationship, but even a redirect should not cause the engine to destroy A.

---

<!-- CAP-371 | Continue Architecture Planning.md L65338–65371 | turn 47 | version 0.17 -->
## v0.17 — 2. Resource identity must become graph-based

> **Source sections:** `CAP-371`
>
> [DOCUMENTATION REVIEW] Contradiction **C-04** ([Review Notes](../REVIEW-NOTES.md#c-04--))

Instead of:

```
Candidate
   ↓
URL
```

we move toward:

```
                     RESOURCE GRAPH

       ┌─────────────┐
       │ Resource R1 │
       └──────┬──────┘
              │
       ┌──────┼─────────────┐
       │      │             │
       ▼      ▼             ▼
     URL A  URL B         URL C
       │      │             │
    alias   redirect      mirror
       │      │             │
       └──────┴─────────────┘
```

The URLs are **identifiers or representations**.

The resource is the entity those identifiers may refer to.

---

<!-- CAP-372 | Continue Architecture Planning.md L65373–65375 | turn 47 | version 0.17 -->
## v0.17 — 3. Candidate vs Resource vs Locator

> **Source sections:** `CAP-372`

We now need three distinct concepts.

<!-- CAP-373 | Continue Architecture Planning.md L65377–65385 | turn 47 | version 0.17 -->
### v0.17 — Candidate

> **Source sections:** `CAP-373`

Something the engine proposes to acquire.

```
candidate
=
"this target may be worth acquiring"
```

<!-- CAP-374 | Continue Architecture Planning.md L65387–65395 | turn 47 | version 0.17 -->
### v0.17 — Locator

> **Source sections:** `CAP-374`

A way of addressing something.

```
locator
=
URL / endpoint / URI
```

<!-- CAP-375 | Continue Architecture Planning.md L65397–65429 | turn 47 | version 0.17 -->
### v0.17 — Resource

> **Source sections:** `CAP-375`

A logical discovered entity.

```
resource
=
the thing the locator may identify
```

Therefore:

```
Candidate
   │
   ▼
Locator
   │
   ▼
Resource
```

but:

```
one Resource
   ↑
   ├── Locator A
   ├── Locator B
   └── Locator C
```

---

<!-- CAP-376 | Continue Architecture Planning.md L65431–65477 | turn 47 | version 0.17 -->
## v0.17 — 4. Why not simply canonicalize everything?

> **Source sections:** `CAP-376`
>
> [DOCUMENTATION REVIEW] Contradiction **C-04** ([Review Notes](../REVIEW-NOTES.md#c-04--))

Canonicalization is useful:

```
HTTP
  ↓
canonicalize URL
  ↓
identity key
```

But canonicalization is deterministic string normalization.

Identity resolution is an **inference problem**.

For example:

```
/page
/page/
```

may plausibly be equivalent.

But:

```
/download?id=42
/download?id=43
```

must not be collapsed merely because their path is identical.

So:

```
Canonicalization
    ≠
Identity Resolution
```

Canonicalization happens first.

Identity resolution happens afterward.

---

<!-- CAP-377 | Continue Architecture Planning.md L65479–65526 | turn 47 | version 0.17 -->
## v0.17 — 5. Locator

> **Source sections:** `CAP-377`

A locator can become explicit:

```JavaScript
class ResourceLocator {
    constructor(data = {}) {
        this.id =
            data.id || makeId('locator');

        this.target =
            data.target || '';

        this.canonicalTarget =
            data.canonicalTarget ||
            data.target ||
            '';

        this.scheme =
            data.scheme || null;

        this.origin =
            data.origin || null;

        this.type =
            data.type || 'unknown';

        this.createdAt =
            data.createdAt || now();
    }
}
```

Later, this can support things other than URLs:

```
URL
URI
URN
browser route
document locator
API endpoint
local file reference
```

For the current userscript, URLs remain the primary implementation.

---

<!-- CAP-378 | Continue Architecture Planning.md L65528–65570 | turn 47 | version 0.17 -->
## v0.17 — 6. Resource

> **Source sections:** `CAP-378`

A resource becomes an identity node:

```JavaScript
class Resource {
    constructor(data = {}) {
        this.id =
            data.id || makeId('resource');

        this.type =
            data.type || 'unknown';

        this.locatorIds =
            data.locatorIds || [];

        this.observationIds =
            data.observationIds || [];

        this.claimIds =
            data.claimIds || [];

        this.fingerprintIds =
            data.fingerprintIds || [];

        this.createdAt =
            data.createdAt || now();

        this.updatedAt =
            data.updatedAt || this.createdAt;
    }
}
```

Notice:

```
Resource
    ≠
current URL
```

---

<!-- CAP-379 | Continue Architecture Planning.md L65572–65613 | turn 47 | version 0.17 -->
## v0.17 — 7. Resource relationships

> **Source sections:** `CAP-379`

Now relationships become explicit.

Initial relation types:

```
alias-of
redirects-to
references
mirrors
same-content-as
derived-from
representation-of
supersedes
```

Example:

```
URL A
   │
redirects-to
   ▼
URL B
```

Or:

```
Resource A
   │
same-content-as
   ▼
Resource B
```

The distinction matters.

A redirect is not necessarily the same relationship as identical bytes.

---

<!-- CAP-380 | Continue Architecture Planning.md L65615–65653 | turn 47 | version 0.17 -->
## v0.17 — 8. Redirects

> **Source sections:** `CAP-380`

Suppose acquisition produces:

```
requested:
https://example.com/manual

final:
https://cdn.example.com/manual.pdf
```

The observation should retain both:

```JavaScript
{
    requestedUrl:
        'https://example.com/manual',

    finalUrl:
        'https://cdn.example.com/manual.pdf'
}
```

Then the graph records:

```
Locator A
    │
 redirects-to
    ▼
Locator B
```

But **do not rewrite A into B**.

The original request remains historically meaningful.

---

<!-- CAP-381 | Continue Architecture Planning.md L65655–65693 | turn 47 | version 0.17 -->
## v0.17 — 9. Redirect chain

> **Source sections:** `CAP-381`

Real redirects can form:

```
A
 ↓
B
 ↓
C
 ↓
D
```

The graph should preserve the chain.

The final resource may be:

```
Resource R
```

with:

```
A ──redirects-to──> B
B ──redirects-to──> C
C ──redirects-to──> D
```

This is much better than:

```
requestedUrl = D
```

because the acquisition history disappears if we overwrite the request.

---

<!-- CAP-382 | Continue Architecture Planning.md L65695–65726 | turn 47 | version 0.17 -->
## v0.17 — 10. Content fingerprints

> **Source sections:** `CAP-382`
>
> [DOCUMENTATION REVIEW] Contradiction **C-07** ([Review Notes](../REVIEW-NOTES.md#c-07--))

Now integrate v0.16 fingerprint evidence.

Suppose:

```
URL A → SHA256(X)
URL B → SHA256(X)
```

We can create:

```
Fingerprint X
       ↑
   ┌───┴───┐
   │       │
 URL A   URL B
```

The graph can express:

```
same-content-as
```

without declaring:

That distinction is essential.

---

<!-- CAP-383 | Continue Architecture Planning.md L65728–65775 | turn 47 | version 0.17 -->
## v0.17 — 11. Same content does not prove same resource

> **Source sections:** `CAP-383`

Suppose two sites host the same PDF:

```
manufacturer.example/manual.pdf
archive.example/manual.pdf
```

They have identical bytes.

Possible interpretations:

```
same document
```

is reasonable.

But:

```
same URL/resource identity
```

is not.

The archive copy could be:

* a mirror
* a redistribution
* an independently stored copy
* an archived revision

Therefore:

```
same fingerprint
    ⇒ same observed bytes

same fingerprint
    ⇏ same locator

same fingerprint
    ⇏ same resource identity
```

---

<!-- CAP-384 | Continue Architecture Planning.md L65777–65814 | turn 47 | version 0.17 -->
## v0.17 — 12. Representation identity

> **Source sections:** `CAP-384`
>
> [DOCUMENTATION REVIEW] Contradiction **C-04** ([Review Notes](../REVIEW-NOTES.md#c-04--))

HTTP introduces another complication.

One resource may have multiple representations:

```
Resource
   ├── HTML representation
   ├── JSON representation
   └── PDF representation
```

For example:

```
/api/document/42
```

might return JSON metadata while:

```
/api/document/42/download
```

returns the actual document.

These should not automatically become one resource.

We need a relationship:

```
representation-of
```

where evidence supports it.

---

<!-- CAP-386 | Continue Architecture Planning.md L65850–65890 | turn 47 | version 0.17 -->
## v0.17 — 14. IdentityResolver

> **Source sections:** `CAP-386`

Conceptually:

```JavaScript
class IdentityResolver {
    resolve(locator, context) {
        return {
            matches: [],
            relations: [],
            unresolved: true
        };
    }
}
```

The resolver should consider evidence in stages.

```
Locator
  ↓
Canonicalization
  ↓
Existing locator match?
  │
  ├── yes → known identity
  │
  └── no
       ↓
Redirect evidence?
       ↓
Fingerprint evidence?
       ↓
Explicit canonical metadata?
       ↓
Strong semantic evidence?
       ↓
Unresolved
```

---

<!-- CAP-387 | Continue Architecture Planning.md L65892–65916 | turn 47 | version 0.17 -->
## v0.17 — 15. Identity confidence should be relational

> **Source sections:** `CAP-387`
>
> [DOCUMENTATION REVIEW] Contradiction **C-04** ([Review Notes](../REVIEW-NOTES.md#c-04--))
>
> [DOCUMENTATION REVIEW] Contradiction **C-06** ([Review Notes](../REVIEW-NOTES.md#c-06--))

Instead of:

```
resource.confidence = 0.87
```

use:

```
Relation:
A same-content-as B
confidence = 1.0

Relation:
A representation-of B
confidence = 0.82
```

The graph can then contain different confidence values for different claims.

This avoids one global confidence number pretending to summarize everything.

---

<!-- CAP-388 | Continue Architecture Planning.md L65918–65952 | turn 47 | version 0.17 -->
## v0.17 — 16. Identity classes

> **Source sections:** `CAP-388`
>
> [DOCUMENTATION REVIEW] Contradiction **C-04** ([Review Notes](../REVIEW-NOTES.md#c-04--))

A useful initial classification:

```
EXACT
PROBABLE
POSSIBLE
UNKNOWN
CONTRADICTED
```

For example:

```
same canonical locator
        ↓
EXACT

redirect relation
        ↓
STRONG / PROBABLE

same fingerprint
        ↓
SAME-CONTENT

same title + same size
        ↓
POSSIBLE
```

But the engine should preserve the actual evidence rather than only storing the class.

---

<!-- CAP-389 | Continue Architecture Planning.md L65954–65990 | turn 47 | version 0.17 -->
## v0.17 — 17. No destructive merges

> **Source sections:** `CAP-389`

This is perhaps the most important v0.17 rule.

Do not do:

```
Resource A
   +
Resource B
   ↓
delete B
```

Instead:

```
Resource A
   │
   └── relation ── Resource B
```

Why?

Because identity resolution can be wrong.

A false merge destroys provenance.

A relation can be revised.

Therefore:

> **Prefer reversible identity assertions over destructive identity merges.**

This aligns directly with the evidence architecture.

---

<!-- CAP-390 | Continue Architecture Planning.md L65992–66040 | turn 47 | version 0.17 -->
## v0.17 — 18. ResourceGraph

> **Source sections:** `CAP-390`

The graph can now be modeled:

```JavaScript
class ResourceGraph {
    constructor() {
        this.resources = new Map();
        this.locators = new Map();
        this.edges = new Map();
    }

    addResource(resource) {
        this.resources.set(
            resource.id,
            resource
        );

        return resource;
    }

    addLocator(locator) {
        this.locators.set(
            locator.id,
            locator
        );

        return locator;
    }

    addEdge(edge) {
        const id =
            edge.id || makeId('redge');

        this.edges.set(id, {
            id,
            ...edge
        });

        return id;
    }
}
```

This is deliberately simple.

The semantic rules belong in the resolver, not the graph container.

---

<!-- CAP-391 | Continue Architecture Planning.md L66042–66080 | turn 47 | version 0.17 -->
## v0.17 — 19. Graph edge contract

> **Source sections:** `CAP-391`

An edge should contain:

```JavaScript
{
    id: 'edge-123',

    from: 'locator-A',

    to: 'locator-B',

    relation: 'redirects-to',

    evidenceIds: [
        'observation-123'
    ],

    sessionId: 'scan-001',

    confidence: 1.0,

    createdAt: 1757500000000
}
```

This gives us:

```
relationship
+
support
+
time
+
session
```

---

<!-- CAP-392 | Continue Architecture Planning.md L66082–66119 | turn 47 | version 0.17 -->
## v0.17 — 20. Identity resolution pipeline

> **Source sections:** `CAP-392`
>
> [DOCUMENTATION REVIEW] Contradiction **C-04** ([Review Notes](../REVIEW-NOTES.md#c-04--))

The full process:

```
                  LOCATOR
                     │
                     ▼
               NORMALIZATION
                     │
                     ▼
              EXISTING MATCH?
                /          \
              yes           no
               │             │
               ▼             ▼
           known node    OBSERVATIONS
                             │
                     ┌───────┼────────┐
                     ▼       ▼        ▼
                  redirect hash   metadata
                     │       │        │
                     └───────┼────────┘
                             ▼
                     IDENTITY EVIDENCE
                             │
                             ▼
                     IDENTITY RESOLVER
                             │
                  ┌──────────┴──────────┐
                  ▼                     ▼
              relation              unresolved
                  │
                  ▼
             RESOURCE GRAPH
```

---

<!-- CAP-393 | Continue Architecture Planning.md L66121–66167 | turn 47 | version 0.17 -->
## v0.17 — 21. Canonical URL is still important

> **Source sections:** `CAP-393`
>
> [DOCUMENTATION REVIEW] Contradiction **C-04** ([Review Notes](../REVIEW-NOTES.md#c-04--))

None of this means canonicalization becomes unnecessary.

We still want:

```
raw target
   ↓
URL normalization
   ↓
canonical target
   ↓
locator identity
```

For example:

* remove fragment where appropriate
* normalize scheme/host
* normalize default ports
* normalize path
* optionally strip known tracking parameters

But every transformation must remain policy-controlled.

For example:

```
?lang=en
```

may be semantically meaningful.

So:

```
stripTrackingParams
```

must never become:

```
stripEverythingWeDon'tUnderstand
```

---

<!-- CAP-395 | Continue Architecture Planning.md L66197–66235 | turn 47 | version 0.17 -->
## v0.17 — 23. Identity resolution must be monotonic where possible

> **Source sections:** `CAP-395`
>
> [DOCUMENTATION REVIEW] Contradiction **C-04** ([Review Notes](../REVIEW-NOTES.md#c-04--))

Suppose initially:

```
A ?= B
```

Later:

```
A same-content-as B
```

Then later:

```
A redirects-to B
```

The knowledge increases.

But we should avoid silently changing:

```
A ≠ B
```

to:

```
A = B
```

unless new evidence actually justifies it.

The graph should accumulate evidence rather than repeatedly rewriting identity.

---

<!-- CAP-396 | Continue Architecture Planning.md L66237–66274 | turn 47 | version 0.17 -->
## v0.17 — 24. Resource revisions

> **Source sections:** `CAP-396`
>
> [DOCUMENTATION REVIEW] Contradiction **C-07** ([Review Notes](../REVIEW-NOTES.md#c-07--))

Now the earlier revision problem becomes explicit.

A resource can have versions:

```
RESOURCE R
    │
    ├── Observation O1 → Fingerprint H1
    │
    └── Observation O2 → Fingerprint H2
```

Then:

```
H1 ≠ H2
```

indicates observed content changed.

But we should not immediately say:

and:

are different resources.

Instead:

```
same logical locator
different observed representations/revisions
```

is the safer default.

---

<!-- CAP-397 | Continue Architecture Planning.md L66276–66303 | turn 47 | version 0.17 -->
## v0.17 — 25. Revision object

> **Source sections:** `CAP-397`
>
> [DOCUMENTATION REVIEW] Contradiction **C-07** ([Review Notes](../REVIEW-NOTES.md#c-07--))

We can later introduce:

```JavaScript
class ResourceRevision {
    constructor(data = {}) {
        this.id =
            data.id || makeId('revision');

        this.resourceId =
            data.resourceId;

        this.fingerprintId =
            data.fingerprintId;

        this.observationId =
            data.observationId;

        this.observedAt =
            data.observedAt || now();
    }
}
```

For v0.17, this can remain conceptual or be represented directly through graph edges.

---

<!-- CAP-398 | Continue Architecture Planning.md L66305–66323 | turn 47 | version 0.17 -->
## v0.17 — 26. ResourceGraph vs KnowledgeBase

> **Source sections:** `CAP-398`
>
> [DOCUMENTATION REVIEW] Contradiction **C-10** ([Review Notes](../REVIEW-NOTES.md#c-10--))

The KnowledgeBase remains the system's storage facade.

But internally:

```
KnowledgeBase
├── CandidateStore
├── ObservationStore
├── EvidenceStore
├── ClaimStore
├── ResourceGraph
└── EventLedger
```

This is preferable to turning `KnowledgeBase` into one enormous class with every semantic responsibility.

---

<!-- CAP-400 | Continue Architecture Planning.md L66329–66333 | turn 47 | version 0.17 -->
### v0.17 — What URLs identify this resource?

> **Source sections:** `CAP-400`

```
resource → locators
```

<!-- CAP-401 | Continue Architecture Planning.md L66335–66342 | turn 47 | version 0.17 -->
### v0.17 — Where was it discovered?

> **Source sections:** `CAP-401`

```
resource
 → claims
 → evidence
 → observations
```

<!-- CAP-402 | Continue Architecture Planning.md L66344–66348 | turn 47 | version 0.17 -->
### v0.17 — What URLs redirect to it?

> **Source sections:** `CAP-402`

```
resource ← redirects-to ← locator
```

<!-- CAP-403 | Continue Architecture Planning.md L66350–66354 | turn 47 | version 0.17 -->
### v0.17 — Which URLs have identical observed bytes?

> **Source sections:** `CAP-403`

```
fingerprint → resources
```

<!-- CAP-404 | Continue Architecture Planning.md L66356–66362 | turn 47 | version 0.17 -->
### v0.17 — Has this resource changed?

> **Source sections:** `CAP-404`

```
resource
 → revisions
 → fingerprints
```

<!-- CAP-405 | Continue Architecture Planning.md L66364–66378 | turn 47 | version 0.17 -->
### v0.17 — Why do we believe two URLs are related?

> **Source sections:** `CAP-405`

```
A
 ↓
relation
 ↓
B
 ↓
evidence
```

This is where the graph starts paying for its complexity.

---

<!-- CAP-406 | Continue Architecture Planning.md L66380–66420 | turn 47 | version 0.17 -->
## v0.17 — 28. Resource graph example

> **Source sections:** `CAP-406`

Suppose we discover:

```
https://otis.example/manual
https://otis.example/download?id=42
https://cdn.example/manual-2026.pdf
```

The graph might become:

```
                   Resource R1
                       │
            ┌──────────┼───────────┐
            │          │           │
            ▼          ▼           ▼
          URL A      URL B       URL C
            │          │           │
            │       redirects      │
            │          │           │
            └──────────▼───────────┘
                       │
                 same-content
                       │
                       ▼
                   Fingerprint H
```

But if the evidence is insufficient:

```
URL C
  │
  └── possible-mirror-of → R1
```

rather than forcing the merge.

---

<!-- CAP-409 | Continue Architecture Planning.md L66452–66457 | turn 47 | version 0.17 -->
### v0.17 — Locator preservation

> **Source sections:** `CAP-409`

```
Every acquired target remains historically identifiable,
even if it redirects.
```

<!-- CAP-410 | Continue Architecture Planning.md L66459–66464 | turn 47 | version 0.17 -->
### v0.17 — No destructive merge

> **Source sections:** `CAP-410`

```
Identity resolution must not destroy
previously recorded provenance.
```

<!-- CAP-411 | Continue Architecture Planning.md L66466–66471 | turn 47 | version 0.17 -->
### v0.17 — Fingerprint independence

> **Source sections:** `CAP-411`
>
> [DOCUMENTATION REVIEW] Contradiction **C-07** ([Review Notes](../REVIEW-NOTES.md#c-07--))

```
Content equality does not automatically imply
resource identity.
```

<!-- CAP-412 | Continue Architecture Planning.md L66473–66478 | turn 47 | version 0.17 -->
### v0.17 — Redirect independence

> **Source sections:** `CAP-412`

```
A redirect relation does not require destructive
locator replacement.
```

<!-- CAP-414 | Continue Architecture Planning.md L66487–66492 | turn 47 | version 0.17 -->
### v0.17 — Revision preservation

> **Source sections:** `CAP-414`
>
> [DOCUMENTATION REVIEW] Contradiction **C-07** ([Review Notes](../REVIEW-NOTES.md#c-07--))

```
Different observations of the same locator remain
historically distinct.
```

<!-- CAP-415 | Continue Architecture Planning.md L66494–66501 | turn 47 | version 0.17 -->
### v0.17 — Canonicalization transparency

> **Source sections:** `CAP-415`
>
> [DOCUMENTATION REVIEW] Contradiction **C-04** ([Review Notes](../REVIEW-NOTES.md#c-04--))

```
Identity convergence caused by normalization
must be explainable.
```

---

<!-- CAP-418 | Continue Architecture Planning.md L66608–66651 | turn 47 | version 0.17 -->
## v0.17 — 33. The important transition

> **Source sections:** `CAP-418`

The project has now crossed another conceptual boundary:

```
v0.6
"Find URLs"

        ↓

v0.13
"Govern discovery"

        ↓

v0.15
"Execute bounded work"

        ↓

v0.16
"Preserve evidence"

        ↓

v0.17
"Resolve resource identity"
```

The system can now distinguish:

```
URL
Candidate
Observation
Evidence
Claim
Resource
Revision
```

instead of treating all of them as variants of “a URL.”

---

<!-- CAP-457 | Continue Architecture Planning.md L68083–68147 | turn 49 | version 0.19 -->
## v0.19 — Resource Representation & Revision Model

> **Source sections:** `CAP-457`
>
> [DOCUMENTATION REVIEW] Contradiction **C-07** ([Review Notes](../REVIEW-NOTES.md#c-07--))

The next boundary follows naturally.

Once we can say:

```
Resource R42
    representation = PDF
    semantic-role = service-manual
```

we immediately hit another problem:

**What exactly is the relationship between the logical resource and the bytes/representations observed over time?**

For example:

```
Resource R42
│
├── Locator A
│
├── Locator B
│
├── PDF representation
│      ├── revision 1
│      └── revision 2
│
└── HTML landing page
```

So v0.19 should separate:

```
Resource
    ↓
Representation
    ↓
Artifact
    ↓
Revision
    ↓
Observation
```

leading toward:

```
RESOURCE GRAPH
       │
       ▼
REPRESENTATION GRAPH
       │
       ▼
ARTIFACT IDENTITY
       │
       ▼
REVISION HISTORY
       │
       ▼
EVIDENCE
```

That will be the point where the Generic Discovery Engine starts becoming a genuine **resource intelligence system**, rather than merely a sophisticated crawler.

<!-- CAP-459 | Continue Architecture Planning.md L68159–68177 | turn 51 | version 0.19 -->
## v0.19 — Resource Representation + Artifact + Revision Model

> **Source sections:** `CAP-459`
>
> [DOCUMENTATION REVIEW] Contradiction **C-07** ([Review Notes](../REVIEW-NOTES.md#c-07--))

At v0.18 we separated **resource identity** from **resource classification**.

The next problem is more fundamental:

> A logical resource is not the bytes we downloaded.

The same logical resource can have:

* multiple URLs,
* multiple representations,
* multiple revisions,
* multiple observations,
* different bytes at different times.

So we need another identity layer.

---

<!-- CAP-460 | Continue Architecture Planning.md L68179–68207 | turn 51 | version 0.19 -->
## v0.19 — 19.1 The Core Distinction

> **Source sections:** `CAP-460`

The model should become:

```
Locator
   │
   ▼
Resource
   │
   ├───────────────┐
   ▼               ▼
Representation   Representation
   │               │
   ▼               ▼
Artifact         Artifact
   │               │
   ├── Revision 1  ├── Revision 1
   └── Revision 2  └── Revision 2
          │
          ▼
      Observation
```

A useful rule:

```
Resource ≠ Representation ≠ Artifact ≠ Observation
```

<!-- CAP-461 | Continue Architecture Planning.md L68209–68217 | turn 51 | version 0.19 -->
### v0.19 — Resource

> **Source sections:** `CAP-461`

The logical thing.

Example:

```
"Otis Gen2 Service Manual"
```

<!-- CAP-462 | Continue Architecture Planning.md L68219–68228 | turn 51 | version 0.19 -->
### v0.19 — Representation

> **Source sections:** `CAP-462`

A particular way that resource is expressed.

```
PDF
HTML landing page
OCR text
JSON metadata
```

<!-- CAP-463 | Continue Architecture Planning.md L68230–68237 | turn 51 | version 0.19 -->
### v0.19 — Artifact

> **Source sections:** `CAP-463`
>
> [DOCUMENTATION REVIEW] Contradiction **C-07** ([Review Notes](../REVIEW-NOTES.md#c-07--))

A concrete byte sequence.

```
SHA-256 = abc123...
size = 18,421,991
```

<!-- CAP-465 | Continue Architecture Planning.md L68252–68300 | turn 51 | version 0.19 -->
## v0.19 — 19.2 Why Resource → Artifact Is Wrong

> **Source sections:** `CAP-465`
>
> [DOCUMENTATION REVIEW] Contradiction **C-07** ([Review Notes](../REVIEW-NOTES.md#c-07--))

A tempting model is:

```JavaScript
resource.fingerprint = sha256(bytes);
```

That creates several problems.

Suppose:

```
URL A
  ↓
Resource R
  ↓
Artifact H1

One week later:

URL A
  ↓
Resource R
  ↓
Artifact H2
```

The resource did not necessarily become a new resource.

It may simply have received a new revision.

Therefore:

```
same resource
≠
same artifact
```

And:

```
different artifact
≠
different resource
```

---

<!-- CAP-466 | Continue Architecture Planning.md L68302–68417 | turn 51 | version 0.19 -->
## v0.19 — 19.3 New Data Model

> **Source sections:** `CAP-466`

Introduce four explicit objects.

```JavaScript
class Resource {
    constructor(data = {}) {
        this.id = data.id || makeId('resource');

        this.locatorIds = data.locatorIds || [];

        this.representationIds =
            data.representationIds || [];

        this.claimIds =
            data.claimIds || [];

        this.classificationIds =
            data.classificationIds || [];

        this.createdAt =
            data.createdAt || now();

        this.updatedAt =
            data.updatedAt || this.createdAt;
    }
}
```

Representation:

```JavaScript
class ResourceRepresentation {
    constructor(data = {}) {
        this.id = data.id || makeId('repr');

        this.resourceId =
            data.resourceId || null;

        this.format =
            data.format || 'unknown';

        this.mediaType =
            data.mediaType || null;

        this.artifactIds =
            data.artifactIds || [];

        this.createdAt =
            data.createdAt || now();
    }
}
```

Artifact:

```JavaScript
class Artifact {
    constructor(data = {}) {
        this.id = data.id || makeId('artifact');

        this.algorithm =
            data.algorithm || 'sha256';

        this.digest =
            data.digest || null;

        this.size =
            Number.isFinite(data.size)
                ? data.size
                : null;

        this.storage =
            data.storage || 'none';

        this.createdAt =
            data.createdAt || now();
    }
}
```

Revision:

```JavaScript
class ResourceRevision {
    constructor(data = {}) {
        this.id = data.id || makeId('revision');

        this.resourceId =
            data.resourceId || null;

        this.representationId =
            data.representationId || null;

        this.artifactId =
            data.artifactId || null;

        this.observationId =
            data.observationId || null;

        this.revisionNumber =
            data.revisionNumber || null;

        this.previousRevisionId =
            data.previousRevisionId || null;

        this.detectedAt =
            data.detectedAt || now();

        this.status =
            data.status || 'active';
    }
}
```

---

<!-- CAP-467 | Continue Architecture Planning.md L68419–68463 | turn 51 | version 0.19 -->
## v0.19 — 19.4 The Complete Identity Chain

> **Source sections:** `CAP-467`
>
> [DOCUMENTATION REVIEW] Contradiction **C-04** ([Review Notes](../REVIEW-NOTES.md#c-04--))

We now have:

```
                    LOGICAL WORLD
                         │
                         ▼
                     RESOURCE
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
        REPRESENTATION         REPRESENTATION
              │                     │
              ▼                     ▼
           ARTIFACT              ARTIFACT
              │                     │
              ▼                     ▼
          REVISION               REVISION
              │
              ▼
         OBSERVATION
```

And separately:

```
LOCATOR ────────► RESOURCE
```

This gives:

```
many locators
      ↓
one resource
      ↓
many representations
      ↓
many artifacts/revisions
      ↓
many observations
```

---

<!-- CAP-468 | Continue Architecture Planning.md L68465–68516 | turn 51 | version 0.19 -->
## v0.19 — 19.5 Representation Is Not Just MIME

> **Source sections:** `CAP-468`

Representation deserves its own identity because:

```
application/pdf
```

is not necessarily enough.

Consider:

```
Resource R1
├── HTML representation
├── PDF representation
└── OCR-text representation
```

These can all describe the same logical thing.

For example:

```
https://example.com/manual
```

might return:

```
text/html
```

while:

```
https://example.com/manual.pdf
```

returns:

```
application/pdf
```

The URLs differ.

The representations differ.

The logical resource may still be the same.

---

<!-- CAP-469 | Continue Architecture Planning.md L68518–68543 | turn 51 | version 0.19 -->
## v0.19 — 19.6 Representation Relations

> **Source sections:** `CAP-469`

Add explicit relationships:

```
representation-of
alternate-representation
derived-representation
canonical-representation
```

Example:

```
PDF artifact
     │
     └── representation-of ──► Resource R42

OCR TXT artifact
     │
     └── derived-representation ──► PDF representation
```

This is safer than pretending all representations are identical.

---

<!-- CAP-470 | Continue Architecture Planning.md L68545–68591 | turn 51 | version 0.19 -->
## v0.19 — 19.7 Artifact Identity

> **Source sections:** `CAP-470`
>
> [DOCUMENTATION REVIEW] Contradiction **C-04** ([Review Notes](../REVIEW-NOTES.md#c-04--))
>
> [DOCUMENTATION REVIEW] Contradiction **C-07** ([Review Notes](../REVIEW-NOTES.md#c-07--))

Artifact identity should be byte-oriented.

The fundamental identity:

```
algorithm + digest
```

For example:

```JavaScript
{
    algorithm: "sha256",
    digest: "...",
    size: 18421991
}
```

The size is useful metadata, but should not define identity.

Therefore:

```
SHA-256(A) == SHA-256(B)
```

is strong evidence that:

```
bytes(A) == bytes(B)
```

assuming the hash algorithm's collision assumptions hold.

But:

```
same bytes
≠
same resource
```

This distinction must remain explicit.

---

<!-- CAP-471 | Continue Architecture Planning.md L68593–68636 | turn 51 | version 0.19 -->
## v0.19 — 19.8 Content Equivalence

> **Source sections:** `CAP-471`

Now the old `same-content-as` relation becomes more precise.

```
Resource A
   │
   └── Representation A
            │
            └── Artifact H1
                         │
                         │ same artifact
                         ▼
Resource B
   │
   └── Representation B
            │
            └── Artifact H1
```

We can assert:

```
Artifact(H1) == Artifact(H1)
```

and therefore:

```
same-content-as
```

may be supported.

But we should not automatically merge:

```
Resource A
Resource B
```

because identical bytes can legitimately represent different logical entities.

---

<!-- CAP-472 | Continue Architecture Planning.md L68638–68678 | turn 51 | version 0.19 -->
## v0.19 — 19.9 Revision Detection

> **Source sections:** `CAP-472`
>
> [DOCUMENTATION REVIEW] Contradiction **C-07** ([Review Notes](../REVIEW-NOTES.md#c-07--))

Now we can model change properly.

Example:

```
Resource R42
│
├── Revision 1
│      artifact = H1
│      observed = Jan 10
│
├── Revision 2
│      artifact = H2
│      observed = Feb 04
│
└── Revision 3
       artifact = H3
       observed = Sep 10
```

Graph:

```
R42
 │
 ▼
Rev1 ─────► Rev2 ─────► Rev3
 H1          H2          H3
```

This gives us:

```
changed(resource, t1, t2)
```

without changing resource identity.

---

<!-- CAP-473 | Continue Architecture Planning.md L68680–68729 | turn 51 | version 0.19 -->
## v0.19 — 19.10 Revision Detection Is Not Always Proof of Semantic Revision

> **Source sections:** `CAP-473`
>
> [DOCUMENTATION REVIEW] Contradiction **C-07** ([Review Notes](../REVIEW-NOTES.md#c-07--))

This is an important edge case.

Suppose:

```
H1 != H2
```

because the server changes:

```HTML
<footer>
Generated at 18:42
</footer>
```

The bytes changed.

But the document itself may not have meaningfully changed.

Therefore:

```
artifact difference
```

proves:

```
byte difference
```

but not necessarily:

```
semantic revision
```

We therefore need two levels:

```
Byte Revision
Semantic Revision
```

Initially, the engine should only claim the first.

---

<!-- CAP-474 | Continue Architecture Planning.md L68731–68772 | turn 51 | version 0.19 -->
## v0.19 — 19.11 Revision Evidence

> **Source sections:** `CAP-474`
>
> [DOCUMENTATION REVIEW] Contradiction **C-07** ([Review Notes](../REVIEW-NOTES.md#c-07--))

A revision record should therefore contain evidence:

```JavaScript
{
    previousArtifactId: "artifact-1",
    currentArtifactId: "artifact-2",

    evidenceIds: [
        "hash-difference",
        "etag-change",
        "last-modified-change"
    ]
}
```

Potential signals:

```
strong:
    byte hash changed

supporting:
    ETag changed
    Last-Modified changed
    explicit version changed
    document revision number changed
    publication date changed
```

But:

```
HTTP Last-Modified
```

should not be treated as proof of content change.

Servers can provide inaccurate metadata.

---

<!-- CAP-475 | Continue Architecture Planning.md L68774–68809 | turn 51 | version 0.19 -->
## v0.19 — 19.12 HTTP Validators Become Evidence

> **Source sections:** `CAP-475`

Acquisition observations can now capture:

```JavaScript
http: {
    status: 200,
    contentType: "application/pdf",
    etag: "...",
    lastModified: "...",
    contentLength: 18421991,
    finalUrl: "..."
}
```

This creates useful evidence:

```
ETag changed
```

or:

```
Content-Length changed
```

or:

```
Last-Modified changed
```

But these remain **signals**, not identity.

---

<!-- CAP-478 | Continue Architecture Planning.md L68904–68935 | turn 51 | version 0.19 -->
## v0.19 — 19.15 Resource State vs Artifact State

> **Source sections:** `CAP-478`
>
> [DOCUMENTATION REVIEW] Contradiction **C-07** ([Review Notes](../REVIEW-NOTES.md#c-07--))

Do not combine them.

A resource might be:

```
Resource:
    known
    classified
    stale
```

while its artifact might be:

```
Artifact:
    stored
    verified
    corrupted
    unavailable
```

And an observation:

```
Observation:
    HTTP 200
    recognition successful
```

These are different state machines.

<!-- CAP-479 | Continue Architecture Planning.md L68937–68945 | turn 51 | version 0.19 -->
### v0.19 — Resource state

> **Source sections:** `CAP-479`

```
unknown
known
classified
superseded
archived
```

<!-- CAP-480 | Continue Architecture Planning.md L68947–68955 | turn 51 | version 0.19 -->
### v0.19 — Artifact state

> **Source sections:** `CAP-480`
>
> [DOCUMENTATION REVIEW] Contradiction **C-07** ([Review Notes](../REVIEW-NOTES.md#c-07--))

```
observed
verified
stored
corrupted
missing
```

<!-- CAP-482 | Continue Architecture Planning.md L68971–69004 | turn 51 | version 0.19 -->
## v0.19 — 19.16 ResourceGraph v0.19

> **Source sections:** `CAP-482`

The graph now expands substantially:

```
                       ┌─────────────┐
                       │   Locator   │
                       └──────┬──────┘
                              │
                              ▼
                       ┌─────────────┐
                       │  Resource   │
                       └──────┬──────┘
                              │
                 ┌────────────┼────────────┐
                 ▼            ▼            ▼
          Representation   Claim    Classification
                 │
                 ▼
             Artifact
                 │
                 ▼
             Revision
                 │
                 ▼
           Observation
                 │
                 ▼
              Evidence
```

This is now an actual **knowledge graph**, not simply a URL database.

---

<!-- CAP-483 | Continue Architecture Planning.md L69006–69073 | turn 51 | version 0.19 -->
## v0.19 — 19.17 ResourceGraph API

> **Source sections:** `CAP-483`

Extend the previous graph:

```JavaScript
class ResourceGraph {
    constructor() {
        this.resources = new Map();
        this.locators = new Map();
        this.representations = new Map();
        this.artifacts = new Map();
        this.revisions = new Map();
        this.classifications = new Map();
        this.claims = new Map();
        this.edges = new Map();
    }

    addResource(resource) {
        this.resources.set(resource.id, resource);
        return resource;
    }

    addLocator(locator) {
        this.locators.set(locator.id, locator);
        return locator;
    }

    addRepresentation(representation) {
        this.representations.set(
            representation.id,
            representation
        );

        return representation;
    }

    addArtifact(artifact) {
        this.artifacts.set(
            artifact.id,
            artifact
        );

        return artifact;
    }

    addRevision(revision) {
        this.revisions.set(
            revision.id,
            revision
        );

        return revision;
    }

    addEdge(edge) {
        const id = edge.id || makeId('redge');

        this.edges.set(id, {
            id,
            ...edge
        });

        return id;
    }
}
```

---

<!-- CAP-484 | Continue Architecture Planning.md L69075–69087 | turn 51 | version 0.19 -->
## v0.19 — 19.18 Artifact Deduplication

> **Source sections:** `CAP-484`
>
> [DOCUMENTATION REVIEW] Contradiction **C-07** ([Review Notes](../REVIEW-NOTES.md#c-07--))

This also fixes an earlier limitation.

Previously:

```
URL deduplication
```

was primary.

Now there are two distinct deduplication layers.

<!-- CAP-485 | Continue Architecture Planning.md L69089–69095 | turn 51 | version 0.19 -->
### v0.19 — Locator deduplication

> **Source sections:** `CAP-485`

```
same canonical locator
        ↓
same locator identity
```

<!-- CAP-486 | Continue Architecture Planning.md L69097–69127 | turn 51 | version 0.19 -->
### v0.19 — Artifact deduplication

> **Source sections:** `CAP-486`
>
> [DOCUMENTATION REVIEW] Contradiction **C-07** ([Review Notes](../REVIEW-NOTES.md#c-07--))

```
same cryptographic digest
        ↓
same byte artifact
```

These should never be conflated.

Example:

```
URL A ──► Artifact H1
URL B ──► Artifact H1
URL C ──► Artifact H1
```

Storage can retain H1 only once.

Graph still retains:

```
A
B
C
```

because those URLs are meaningful evidence.

---

<!-- CAP-487 | Continue Architecture Planning.md L69129–69181 | turn 51 | version 0.19 -->
## v0.19 — 19.19 Content-Addressed Storage

> **Source sections:** `CAP-487`

This points naturally toward content-addressed storage.

Conceptually:

```
Artifact
   │
   ▼
sha256:d7e...
   │
   ▼
Blob Store
```

Possible future structure:

```
artifacts/
└── sha256/
    ├── d7/
    │   └── d7e...
    ├── 81/
    │   └── 81a...
    └── ...
```

The userscript does not need to implement this immediately.

For v0.19:

```
Artifact identity
```

is enough.

Storage can remain:

```
storage: "none"
```

or:

```
storage: "memory"
```

until a durable artifact store is introduced.

---

<!-- CAP-489 | Continue Architecture Planning.md L69222–69271 | turn 51 | version 0.19 -->
## v0.19 — 19.21 Independent Confirmation

> **Source sections:** `CAP-489`

This becomes particularly useful for the discovery algorithm.

Suppose:

```
URL X
```

was discovered from:

```
HTML
robots.txt
sitemap
network observation
```

That gives four discovery paths.

But they may not be independent.

For example:

```
HTML
  ↓
JavaScript
  ↓
API
```

may ultimately originate from one source.

Therefore:

```
4 evidence objects
```

does not automatically mean:

```
4 independent confirmations
```

The graph should preserve provenance so independence can later be reasoned about.

---

<!-- CAP-490 | Continue Architecture Planning.md L69273–69310 | turn 51 | version 0.19 -->
## v0.19 — 19.22 Resource Confidence

> **Source sections:** `CAP-490`
>
> [DOCUMENTATION REVIEW] Contradiction **C-06** ([Review Notes](../REVIEW-NOTES.md#c-06--))

This suggests another important separation.

Do not make:

```JavaScript
resource.confidence
```

the central truth.

Instead:

```
Resource
│
├── identity claims
├── classification assertions
├── artifact evidence
├── locator evidence
└── revision evidence
```

Confidence belongs primarily to **assertions**.

Then queries can derive:

```
identity confidence
classification confidence
revision confidence
artifact confidence
```

independently.

---

<!-- CAP-491 | Continue Architecture Planning.md L69312–69318 | turn 51 | version 0.19 -->
## v0.19 — 19.23 Example

> **Source sections:** `CAP-491`

Suppose the engine encounters:

```
https://example.com/docs/gen2.pdf
```

<!-- CAP-492 | Continue Architecture Planning.md L69320–69325 | turn 51 | version 0.19 -->
### v0.19 — Step 1 — Locator

> **Source sections:** `CAP-492`

```
Locator L1
target = /docs/gen2.pdf
```

<!-- CAP-493 | Continue Architecture Planning.md L69327–69331 | turn 51 | version 0.19 -->
### v0.19 — Step 2 — Resource

> **Source sections:** `CAP-493`

```
Resource R1
```

<!-- CAP-495 | Continue Architecture Planning.md L69341–69346 | turn 51 | version 0.19 -->
### v0.19 — Step 4 — Artifact

> **Source sections:** `CAP-495`
>
> [DOCUMENTATION REVIEW] Contradiction **C-07** ([Review Notes](../REVIEW-NOTES.md#c-07--))

```
Artifact A1
SHA256 = H1
```

<!-- CAP-496 | Continue Architecture Planning.md L69348–69354 | turn 51 | version 0.19 -->
### v0.19 — Step 5 — Representation

> **Source sections:** `CAP-496`

```
Representation P1
format = PDF
mediaType = application/pdf
```

<!-- CAP-497 | Continue Architecture Planning.md L69356–69361 | turn 51 | version 0.19 -->
### v0.19 — Step 6 — Classification

> **Source sections:** `CAP-497`

```
service-manual
confidence = 0.93
```

<!-- CAP-498 | Continue Architecture Planning.md L69363–69397 | turn 51 | version 0.19 -->
### v0.19 — Step 7 — Revision

> **Source sections:** `CAP-498`
>
> [DOCUMENTATION REVIEW] Contradiction **C-07** ([Review Notes](../REVIEW-NOTES.md#c-07--))

```
Revision V1
artifact = A1
```

The graph becomes:

```
L1
 │
 ▼
R1
 │
 ▼
P1 ─────► PDF
 │
 ▼
V1
 │
 ▼
A1 ─────► H1
 │
 ▼
O1
 │
 ▼
Evidence
 │
 ▼
"service-manual"
```

---

<!-- CAP-499 | Continue Architecture Planning.md L69399–69452 | turn 51 | version 0.19 -->
## v0.19 — 19.24 A More Precise End-to-End Pipeline

> **Source sections:** `CAP-499`

The Generic Discovery Engine now has:

```
                         DISCOVERY DOMAIN
                                │
                                ▼
                         FRONTIER RUNTIME
                                │
               ┌────────────────┴────────────────┐
               ▼                                 ▼
       DISCOVERY WORK                     ACQUISITION WORK
               │                                 │
               ▼                                 ▼
       Candidate Source                  Acquisition Runtime
               │                                 │
               ▼                                 ▼
          Candidate                          Observation
               │                                 │
               └────────────────┬────────────────┘
                                ▼
                          Evidence Graph
                                │
                                ▼
                       Response Recognition
                                │
                                ▼
                            Locator
                                │
                                ▼
                            Resource
                                │
                 ┌──────────────┼──────────────┐
                 ▼              ▼              ▼
           Representation    Identity      Classification
                 │              │              │
                 ▼              │              ▼
              Artifact          │        Semantic Type
                 │              │
                 ▼              │
              Revision          │
                 │              │
                 └──────────────┴──────────────┐
                                                ▼
                                         Strategy Resolution
                                                │
                                                ▼
                                            New Work
```

This is now a closed discovery loop.

---

<!-- CAP-510 | Continue Architecture Planning.md L69569–69657 | turn 51 | version 0.19 -->
## v0.19 — 19.27 What v0.19 Gives Us

> **Source sections:** `CAP-510`

The system has now moved through:

```
v0.12 Candidate Source
        ↓
v0.13 Discovery Controller
        ↓
v0.14 Discovery Domain
        ↓
v0.15 Frontier Runtime
        ↓
v0.16 Evidence Graph
        ↓
v0.17 Resource Identity
        ↓
v0.18 Semantic Classification
        ↓
v0.19 Representation / Artifact / Revision
```

The conceptual transformation is:

```
v0.6

URL
 ↓
download
 ↓
parse
 ↓
new URL
```

becoming:

```
v0.19

Possibility
    ↓
Candidate
    ↓
Discovery Evidence
    ↓
Acquisition Decision
    ↓
Observation
    ↓
Artifact
    ↓
Representation
    ↓
Resource Identity
    ↓
Classification
    ↓
Revision History
    ↓
New Discovery Work
```

That is the point where the original **DVB blind-scan analogy** becomes more precise.

A blind scan does not merely collect frequencies. It progressively transforms an unknown search space into structured knowledge.

The Generic Discovery Engine is doing the same thing at the resource level:

```
UNKNOWN SPACE
     ↓
LOCATORS
     ↓
OBSERVATIONS
     ↓
ARTIFACTS
     ↓
RESOURCES
     ↓
RELATIONS
     ↓
CLASSIFICATIONS
     ↓
REVISIONS
     ↓
NEW SEARCH SPACE
```
