# Resource, Representation and Revision Model

> **Status:** DESIGNED
>
> **Source:** `Continue Architecture Planning.md`; `Userscript Discovery Prototype.md`
>
> **Purpose:** Resources, locators, representations, artifacts, identity resolution and revision detection.

## Contents

- **21. Handle disappearing multiplexes** — `Userscript Discovery Prototype.md` L993–1023
- **v0.17 — ResourceGraph + Identity Resolution** — `Continue Architecture Planning.md` L65216–65240
- **v0.17 — ResourceGraph + Identity Resolution** — `Continue Architecture Planning.md` L65252–65295
- **v0.17 — 1. The core problem** — `Continue Architecture Planning.md` L65297–65336
- **v0.17 — 2. Resource identity must become graph-based** — `Continue Architecture Planning.md` L65338–65371
- **v0.17 — 3. Candidate vs Resource vs Locator** — `Continue Architecture Planning.md` L65373–65375
- **v0.17 — Candidate** — `Continue Architecture Planning.md` L65377–65385
- **v0.17 — Locator** — `Continue Architecture Planning.md` L65387–65395
- **v0.17 — Resource** — `Continue Architecture Planning.md` L65397–65429
- **v0.17 — 4. Why not simply canonicalize everything?** — `Continue Architecture Planning.md` L65431–65477
- **v0.17 — 5. Locator** — `Continue Architecture Planning.md` L65479–65526
- **v0.17 — 6. Resource** — `Continue Architecture Planning.md` L65528–65570
- **v0.17 — 7. Resource relationships** — `Continue Architecture Planning.md` L65572–65613
- **v0.17 — 8. Redirects** — `Continue Architecture Planning.md` L65615–65653
- **v0.17 — 9. Redirect chain** — `Continue Architecture Planning.md` L65655–65693
- **v0.17 — 10. Content fingerprints** — `Continue Architecture Planning.md` L65695–65726
- **v0.17 — 11. Same content does not prove same resource** — `Continue Architecture Planning.md` L65728–65775
- **v0.17 — 12. Representation identity** — `Continue Architecture Planning.md` L65777–65814
- **v0.17 — 14. IdentityResolver** — `Continue Architecture Planning.md` L65850–65890
- **v0.17 — 15. Identity confidence should be relational** — `Continue Architecture Planning.md` L65892–65916
- **v0.17 — 16. Identity classes** — `Continue Architecture Planning.md` L65918–65952
- **v0.17 — 17. No destructive merges** — `Continue Architecture Planning.md` L65954–65990
- **v0.17 — 18. ResourceGraph** — `Continue Architecture Planning.md` L65992–66040
- **v0.17 — 19. Graph edge contract** — `Continue Architecture Planning.md` L66042–66080
- **v0.17 — 20. Identity resolution pipeline** — `Continue Architecture Planning.md` L66082–66119
- **v0.17 — 21. Canonical URL is still important** — `Continue Architecture Planning.md` L66121–66167
- **v0.17 — 23. Identity resolution must be monotonic where possible** — `Continue Architecture Planning.md` L66197–66235
- **v0.17 — 24. Resource revisions** — `Continue Architecture Planning.md` L66237–66274
- **v0.17 — 25. Revision object** — `Continue Architecture Planning.md` L66276–66303
- **v0.17 — 26. ResourceGraph vs KnowledgeBase** — `Continue Architecture Planning.md` L66305–66323
- **v0.17 — What URLs identify this resource?** — `Continue Architecture Planning.md` L66329–66333
- **v0.17 — Where was it discovered?** — `Continue Architecture Planning.md` L66335–66342
- **v0.17 — What URLs redirect to it?** — `Continue Architecture Planning.md` L66344–66348
- **v0.17 — Which URLs have identical observed bytes?** — `Continue Architecture Planning.md` L66350–66354
- **v0.17 — Has this resource changed?** — `Continue Architecture Planning.md` L66356–66362
- **v0.17 — Why do we believe two URLs are related?** — `Continue Architecture Planning.md` L66364–66378
- **v0.17 — 28. Resource graph example** — `Continue Architecture Planning.md` L66380–66420
- **v0.17 — Locator preservation** — `Continue Architecture Planning.md` L66452–66457
- **v0.17 — No destructive merge** — `Continue Architecture Planning.md` L66459–66464
- **v0.17 — Fingerprint independence** — `Continue Architecture Planning.md` L66466–66471
- **v0.17 — Redirect independence** — `Continue Architecture Planning.md` L66473–66478
- **v0.17 — Revision preservation** — `Continue Architecture Planning.md` L66487–66492
- **v0.17 — Canonicalization transparency** — `Continue Architecture Planning.md` L66494–66501
- **v0.17 — 33. The important transition** — `Continue Architecture Planning.md` L66608–66651
- **v0.19 — Resource Representation & Revision Model** — `Continue Architecture Planning.md` L68083–68147
- **v0.19 — Resource Representation + Artifact + Revision Model** — `Continue Architecture Planning.md` L68159–68177
- **v0.19 — 19.1 The Core Distinction** — `Continue Architecture Planning.md` L68179–68207
- **v0.19 — Resource** — `Continue Architecture Planning.md` L68209–68217
- **v0.19 — Representation** — `Continue Architecture Planning.md` L68219–68228
- **v0.19 — Artifact** — `Continue Architecture Planning.md` L68230–68237
- **v0.19 — 19.2 Why Resource → Artifact Is Wrong** — `Continue Architecture Planning.md` L68252–68300
- **v0.19 — 19.3 New Data Model** — `Continue Architecture Planning.md` L68302–68417
- **v0.19 — 19.4 The Complete Identity Chain** — `Continue Architecture Planning.md` L68419–68463
- **v0.19 — 19.5 Representation Is Not Just MIME** — `Continue Architecture Planning.md` L68465–68516
- **v0.19 — 19.6 Representation Relations** — `Continue Architecture Planning.md` L68518–68543
- **v0.19 — 19.7 Artifact Identity** — `Continue Architecture Planning.md` L68545–68591
- **v0.19 — 19.8 Content Equivalence** — `Continue Architecture Planning.md` L68593–68636
- **v0.19 — 19.9 Revision Detection** — `Continue Architecture Planning.md` L68638–68678
- **v0.19 — 19.10 Revision Detection Is Not Always Proof of Semantic Revision** — `Continue Architecture Planning.md` L68680–68729
- **v0.19 — 19.11 Revision Evidence** — `Continue Architecture Planning.md` L68731–68772
- **v0.19 — 19.12 HTTP Validators Become Evidence** — `Continue Architecture Planning.md` L68774–68809
- **v0.19 — 19.15 Resource State vs Artifact State** — `Continue Architecture Planning.md` L68904–68935
- **v0.19 — Resource state** — `Continue Architecture Planning.md` L68937–68945
- **v0.19 — Artifact state** — `Continue Architecture Planning.md` L68947–68955
- **v0.19 — 19.16 ResourceGraph v0.19** — `Continue Architecture Planning.md` L68971–69004
- **v0.19 — 19.17 ResourceGraph API** — `Continue Architecture Planning.md` L69006–69073
- **v0.19 — 19.18 Artifact Deduplication** — `Continue Architecture Planning.md` L69075–69087
- **v0.19 — Locator deduplication** — `Continue Architecture Planning.md` L69089–69095
- **v0.19 — Artifact deduplication** — `Continue Architecture Planning.md` L69097–69127
- **v0.19 — 19.19 Content-Addressed Storage** — `Continue Architecture Planning.md` L69129–69181
- **v0.19 — 19.21 Independent Confirmation** — `Continue Architecture Planning.md` L69222–69271
- **v0.19 — 19.22 Resource Confidence** — `Continue Architecture Planning.md` L69273–69310
- **v0.19 — 19.23 Example** — `Continue Architecture Planning.md` L69312–69318
- **v0.19 — Step 1 — Locator** — `Continue Architecture Planning.md` L69320–69325
- **v0.19 — Step 2 — Resource** — `Continue Architecture Planning.md` L69327–69331
- **v0.19 — Step 4 — Artifact** — `Continue Architecture Planning.md` L69341–69346
- **v0.19 — Step 5 — Representation** — `Continue Architecture Planning.md` L69348–69354
- **v0.19 — Step 6 — Classification** — `Continue Architecture Planning.md` L69356–69361
- **v0.19 — Step 7 — Revision** — `Continue Architecture Planning.md` L69363–69397
- **v0.19 — 19.24 A More Precise End-to-End Pipeline** — `Continue Architecture Planning.md` L69399–69452
- **v0.19 — 19.27 What v0.19 Gives Us** — `Continue Architecture Planning.md` L69569–69657

## Related Documents

- [Evidence Model](evidence-model.md)
- [Resource Type System and Classification](classification.md)
- [Coverage, Completeness and Absence](coverage-and-absence.md)
- [System Model](system-model.md)

---

<!-- source: Userscript Discovery Prototype.md L993–1023 | turn 7 | version ? -->
## 21. Handle disappearing multiplexes

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

<!-- source: Continue Architecture Planning.md L65216–65240 | turn 45 | version 0.17 -->
## v0.17 — ResourceGraph + Identity Resolution

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

<!-- source: Continue Architecture Planning.md L65252–65295 | turn 47 | version 0.17 -->
## v0.17 — ResourceGraph + Identity Resolution

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

<!-- source: Continue Architecture Planning.md L65297–65336 | turn 47 | version 0.17 -->
## v0.17 — 1. The core problem

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

<!-- source: Continue Architecture Planning.md L65338–65371 | turn 47 | version 0.17 -->
## v0.17 — 2. Resource identity must become graph-based

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

<!-- source: Continue Architecture Planning.md L65373–65375 | turn 47 | version 0.17 -->
## v0.17 — 3. Candidate vs Resource vs Locator

We now need three distinct concepts.

<!-- source: Continue Architecture Planning.md L65377–65385 | turn 47 | version 0.17 -->
### v0.17 — Candidate

Something the engine proposes to acquire.

```
candidate
=
"this target may be worth acquiring"
```

<!-- source: Continue Architecture Planning.md L65387–65395 | turn 47 | version 0.17 -->
### v0.17 — Locator

A way of addressing something.

```
locator
=
URL / endpoint / URI
```

<!-- source: Continue Architecture Planning.md L65397–65429 | turn 47 | version 0.17 -->
### v0.17 — Resource

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

<!-- source: Continue Architecture Planning.md L65431–65477 | turn 47 | version 0.17 -->
## v0.17 — 4. Why not simply canonicalize everything?

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

<!-- source: Continue Architecture Planning.md L65479–65526 | turn 47 | version 0.17 -->
## v0.17 — 5. Locator

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

<!-- source: Continue Architecture Planning.md L65528–65570 | turn 47 | version 0.17 -->
## v0.17 — 6. Resource

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

<!-- source: Continue Architecture Planning.md L65572–65613 | turn 47 | version 0.17 -->
## v0.17 — 7. Resource relationships

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

<!-- source: Continue Architecture Planning.md L65615–65653 | turn 47 | version 0.17 -->
## v0.17 — 8. Redirects

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

<!-- source: Continue Architecture Planning.md L65655–65693 | turn 47 | version 0.17 -->
## v0.17 — 9. Redirect chain

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

<!-- source: Continue Architecture Planning.md L65695–65726 | turn 47 | version 0.17 -->
## v0.17 — 10. Content fingerprints

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

<!-- source: Continue Architecture Planning.md L65728–65775 | turn 47 | version 0.17 -->
## v0.17 — 11. Same content does not prove same resource

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

<!-- source: Continue Architecture Planning.md L65777–65814 | turn 47 | version 0.17 -->
## v0.17 — 12. Representation identity

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

<!-- source: Continue Architecture Planning.md L65850–65890 | turn 47 | version 0.17 -->
## v0.17 — 14. IdentityResolver

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

<!-- source: Continue Architecture Planning.md L65892–65916 | turn 47 | version 0.17 -->
## v0.17 — 15. Identity confidence should be relational

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

<!-- source: Continue Architecture Planning.md L65918–65952 | turn 47 | version 0.17 -->
## v0.17 — 16. Identity classes

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

<!-- source: Continue Architecture Planning.md L65954–65990 | turn 47 | version 0.17 -->
## v0.17 — 17. No destructive merges

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

<!-- source: Continue Architecture Planning.md L65992–66040 | turn 47 | version 0.17 -->
## v0.17 — 18. ResourceGraph

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

<!-- source: Continue Architecture Planning.md L66042–66080 | turn 47 | version 0.17 -->
## v0.17 — 19. Graph edge contract

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

<!-- source: Continue Architecture Planning.md L66082–66119 | turn 47 | version 0.17 -->
## v0.17 — 20. Identity resolution pipeline

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

<!-- source: Continue Architecture Planning.md L66121–66167 | turn 47 | version 0.17 -->
## v0.17 — 21. Canonical URL is still important

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

<!-- source: Continue Architecture Planning.md L66197–66235 | turn 47 | version 0.17 -->
## v0.17 — 23. Identity resolution must be monotonic where possible

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

<!-- source: Continue Architecture Planning.md L66237–66274 | turn 47 | version 0.17 -->
## v0.17 — 24. Resource revisions

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

<!-- source: Continue Architecture Planning.md L66276–66303 | turn 47 | version 0.17 -->
## v0.17 — 25. Revision object

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

<!-- source: Continue Architecture Planning.md L66305–66323 | turn 47 | version 0.17 -->
## v0.17 — 26. ResourceGraph vs KnowledgeBase

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

<!-- source: Continue Architecture Planning.md L66329–66333 | turn 47 | version 0.17 -->
### v0.17 — What URLs identify this resource?

```
resource → locators
```

<!-- source: Continue Architecture Planning.md L66335–66342 | turn 47 | version 0.17 -->
### v0.17 — Where was it discovered?

```
resource
 → claims
 → evidence
 → observations
```

<!-- source: Continue Architecture Planning.md L66344–66348 | turn 47 | version 0.17 -->
### v0.17 — What URLs redirect to it?

```
resource ← redirects-to ← locator
```

<!-- source: Continue Architecture Planning.md L66350–66354 | turn 47 | version 0.17 -->
### v0.17 — Which URLs have identical observed bytes?

```
fingerprint → resources
```

<!-- source: Continue Architecture Planning.md L66356–66362 | turn 47 | version 0.17 -->
### v0.17 — Has this resource changed?

```
resource
 → revisions
 → fingerprints
```

<!-- source: Continue Architecture Planning.md L66364–66378 | turn 47 | version 0.17 -->
### v0.17 — Why do we believe two URLs are related?

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

<!-- source: Continue Architecture Planning.md L66380–66420 | turn 47 | version 0.17 -->
## v0.17 — 28. Resource graph example

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

<!-- source: Continue Architecture Planning.md L66452–66457 | turn 47 | version 0.17 -->
### v0.17 — Locator preservation

```
Every acquired target remains historically identifiable,
even if it redirects.
```

<!-- source: Continue Architecture Planning.md L66459–66464 | turn 47 | version 0.17 -->
### v0.17 — No destructive merge

```
Identity resolution must not destroy
previously recorded provenance.
```

<!-- source: Continue Architecture Planning.md L66466–66471 | turn 47 | version 0.17 -->
### v0.17 — Fingerprint independence

```
Content equality does not automatically imply
resource identity.
```

<!-- source: Continue Architecture Planning.md L66473–66478 | turn 47 | version 0.17 -->
### v0.17 — Redirect independence

```
A redirect relation does not require destructive
locator replacement.
```

<!-- source: Continue Architecture Planning.md L66487–66492 | turn 47 | version 0.17 -->
### v0.17 — Revision preservation

```
Different observations of the same locator remain
historically distinct.
```

<!-- source: Continue Architecture Planning.md L66494–66501 | turn 47 | version 0.17 -->
### v0.17 — Canonicalization transparency

```
Identity convergence caused by normalization
must be explainable.
```

---

<!-- source: Continue Architecture Planning.md L66608–66651 | turn 47 | version 0.17 -->
## v0.17 — 33. The important transition

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

<!-- source: Continue Architecture Planning.md L68083–68147 | turn 49 | version 0.19 -->
## v0.19 — Resource Representation & Revision Model

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

<!-- source: Continue Architecture Planning.md L68159–68177 | turn 51 | version 0.19 -->
## v0.19 — Resource Representation + Artifact + Revision Model

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

<!-- source: Continue Architecture Planning.md L68179–68207 | turn 51 | version 0.19 -->
## v0.19 — 19.1 The Core Distinction

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

<!-- source: Continue Architecture Planning.md L68209–68217 | turn 51 | version 0.19 -->
### v0.19 — Resource

The logical thing.

Example:

```
"Otis Gen2 Service Manual"
```

<!-- source: Continue Architecture Planning.md L68219–68228 | turn 51 | version 0.19 -->
### v0.19 — Representation

A particular way that resource is expressed.

```
PDF
HTML landing page
OCR text
JSON metadata
```

<!-- source: Continue Architecture Planning.md L68230–68237 | turn 51 | version 0.19 -->
### v0.19 — Artifact

A concrete byte sequence.

```
SHA-256 = abc123...
size = 18,421,991
```

<!-- source: Continue Architecture Planning.md L68252–68300 | turn 51 | version 0.19 -->
## v0.19 — 19.2 Why Resource → Artifact Is Wrong

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

<!-- source: Continue Architecture Planning.md L68302–68417 | turn 51 | version 0.19 -->
## v0.19 — 19.3 New Data Model

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

<!-- source: Continue Architecture Planning.md L68419–68463 | turn 51 | version 0.19 -->
## v0.19 — 19.4 The Complete Identity Chain

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

<!-- source: Continue Architecture Planning.md L68465–68516 | turn 51 | version 0.19 -->
## v0.19 — 19.5 Representation Is Not Just MIME

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

<!-- source: Continue Architecture Planning.md L68518–68543 | turn 51 | version 0.19 -->
## v0.19 — 19.6 Representation Relations

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

<!-- source: Continue Architecture Planning.md L68545–68591 | turn 51 | version 0.19 -->
## v0.19 — 19.7 Artifact Identity

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

<!-- source: Continue Architecture Planning.md L68593–68636 | turn 51 | version 0.19 -->
## v0.19 — 19.8 Content Equivalence

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

<!-- source: Continue Architecture Planning.md L68638–68678 | turn 51 | version 0.19 -->
## v0.19 — 19.9 Revision Detection

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

<!-- source: Continue Architecture Planning.md L68680–68729 | turn 51 | version 0.19 -->
## v0.19 — 19.10 Revision Detection Is Not Always Proof of Semantic Revision

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

<!-- source: Continue Architecture Planning.md L68731–68772 | turn 51 | version 0.19 -->
## v0.19 — 19.11 Revision Evidence

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

<!-- source: Continue Architecture Planning.md L68774–68809 | turn 51 | version 0.19 -->
## v0.19 — 19.12 HTTP Validators Become Evidence

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

<!-- source: Continue Architecture Planning.md L68904–68935 | turn 51 | version 0.19 -->
## v0.19 — 19.15 Resource State vs Artifact State

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

<!-- source: Continue Architecture Planning.md L68937–68945 | turn 51 | version 0.19 -->
### v0.19 — Resource state

```
unknown
known
classified
superseded
archived
```

<!-- source: Continue Architecture Planning.md L68947–68955 | turn 51 | version 0.19 -->
### v0.19 — Artifact state

```
observed
verified
stored
corrupted
missing
```

<!-- source: Continue Architecture Planning.md L68971–69004 | turn 51 | version 0.19 -->
## v0.19 — 19.16 ResourceGraph v0.19

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

<!-- source: Continue Architecture Planning.md L69006–69073 | turn 51 | version 0.19 -->
## v0.19 — 19.17 ResourceGraph API

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

<!-- source: Continue Architecture Planning.md L69075–69087 | turn 51 | version 0.19 -->
## v0.19 — 19.18 Artifact Deduplication

This also fixes an earlier limitation.

Previously:

```
URL deduplication
```

was primary.

Now there are two distinct deduplication layers.

<!-- source: Continue Architecture Planning.md L69089–69095 | turn 51 | version 0.19 -->
### v0.19 — Locator deduplication

```
same canonical locator
        ↓
same locator identity
```

<!-- source: Continue Architecture Planning.md L69097–69127 | turn 51 | version 0.19 -->
### v0.19 — Artifact deduplication

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

<!-- source: Continue Architecture Planning.md L69129–69181 | turn 51 | version 0.19 -->
## v0.19 — 19.19 Content-Addressed Storage

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

<!-- source: Continue Architecture Planning.md L69222–69271 | turn 51 | version 0.19 -->
## v0.19 — 19.21 Independent Confirmation

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

<!-- source: Continue Architecture Planning.md L69273–69310 | turn 51 | version 0.19 -->
## v0.19 — 19.22 Resource Confidence

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

<!-- source: Continue Architecture Planning.md L69312–69318 | turn 51 | version 0.19 -->
## v0.19 — 19.23 Example

Suppose the engine encounters:

```
https://example.com/docs/gen2.pdf
```

<!-- source: Continue Architecture Planning.md L69320–69325 | turn 51 | version 0.19 -->
### v0.19 — Step 1 — Locator

```
Locator L1
target = /docs/gen2.pdf
```

<!-- source: Continue Architecture Planning.md L69327–69331 | turn 51 | version 0.19 -->
### v0.19 — Step 2 — Resource

```
Resource R1
```

<!-- source: Continue Architecture Planning.md L69341–69346 | turn 51 | version 0.19 -->
### v0.19 — Step 4 — Artifact

```
Artifact A1
SHA256 = H1
```

<!-- source: Continue Architecture Planning.md L69348–69354 | turn 51 | version 0.19 -->
### v0.19 — Step 5 — Representation

```
Representation P1
format = PDF
mediaType = application/pdf
```

<!-- source: Continue Architecture Planning.md L69356–69361 | turn 51 | version 0.19 -->
### v0.19 — Step 6 — Classification

```
service-manual
confidence = 0.93
```

<!-- source: Continue Architecture Planning.md L69363–69397 | turn 51 | version 0.19 -->
### v0.19 — Step 7 — Revision

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

<!-- source: Continue Architecture Planning.md L69399–69452 | turn 51 | version 0.19 -->
## v0.19 — 19.24 A More Precise End-to-End Pipeline

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

<!-- source: Continue Architecture Planning.md L69569–69657 | turn 51 | version 0.19 -->
## v0.19 — 19.27 What v0.19 Gives Us

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
