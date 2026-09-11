# Candidate Sources

> **Status:** DESIGNED
>
> **Source:** `Continue Architecture Planning.md`
>
> **Purpose:** Candidate sources as search-space adapters: contracts, proposals, normalization and the source registry.

## Source Sections

- **v0.12 — Candidate Source Architecture** — `CAP-154` — `Continue Architecture Planning.md` L58349–58359
- **v0.12 — 2. CandidateSource contract** — `CAP-156` — `Continue Architecture Planning.md` L58418–58464
- **v0.12 — 3. CandidateSource is a search-space adapter** — `CAP-157` — `Continue Architecture Planning.md` L58466–58480
- **v0.12 — Web page** — `CAP-158` — `Continue Architecture Planning.md` L58482–58490
- **v0.12 — Network traffic** — `CAP-159` — `Continue Architecture Planning.md` L58492–58500
- **v0.12 — Sitemap** — `CAP-160` — `Continue Architecture Planning.md` L58502–58510
- **v0.12 — User seed** — `CAP-161` — `Continue Architecture Planning.md` L58512–58518
- **v0.12 — Document** — `CAP-162` — `Continue Architecture Planning.md` L58520–58532
- **v0.12 — 4. CandidateProposal** — `CAP-163` — `Continue Architecture Planning.md` L58534–58595
- **v0.12 — 5. Why proposals matter** — `CAP-164` — `Continue Architecture Planning.md` L58597–58637
- **v0.12 — 6. CandidateNormalizer** — `CAP-165` — `Continue Architecture Planning.md` L58639–58710
- **v0.12 — 7. Source Registry** — `CAP-166` — `Continue Architecture Planning.md` L58712–58755
- **v0.12 — 9. Evidence becomes an intermediate layer** — `CAP-168` — `Continue Architecture Planning.md` L58813–58864
- **v0.12 — 10. Discovery becomes evidence-driven** — `CAP-169` — `Continue Architecture Planning.md` L58866–58894
- **v0.12 — 11. CandidateSource context** — `CAP-170` — `Continue Architecture Planning.md` L58896–58930
- **v0.12 — 12. CandidateSource examples** — `CAP-171` — `Continue Architecture Planning.md` L58932–58932
- **v0.12 — HTML link source** — `CAP-172` — `Continue Architecture Planning.md` L58934–58978
- **v0.12 — 13. NetworkSource** — `CAP-173` — `Continue Architecture Planning.md` L58980–59027
- **v0.12 — 14. Search-space composition** — `CAP-174` — `Continue Architecture Planning.md` L59029–59056
- **v0.12 — 15. Candidate identity** — `CAP-175` — `Continue Architecture Planning.md` L59058–59094
- **v0.12 — 16. Discovery confidence aggregation** — `CAP-176` — `Continue Architecture Planning.md` L59096–59144
- **v0.12 — 17. v0.12 provenance graph** — `CAP-177` — `Continue Architecture Planning.md` L59146–59206

## Related Documents

- [Search Space](../architecture/search-space.md)
- [Candidate Model](../architecture/candidate-model.md)
- [Strategies, Query Planning and Enumeration](../architecture/strategy-and-planning.md)
- [Provider Architecture](../architecture/provider-architecture.md)

---

<!-- CAP-154 | Continue Architecture Planning.md L58349–58359 | turn 37 | version 0.12 -->
## v0.12 — Candidate Source Architecture

> **Source sections:** `CAP-154`

v0.11 separated **acquisition** from **recognition**.

The next missing boundary is the origin of candidates themselves.

> **A CandidateSource does not acquire resources. It proposes possible resources.**

This is the architectural equivalent of separating a DVB receiver's **search-space generation** from its **tuning and lock process**.

---

<!-- CAP-156 | Continue Architecture Planning.md L58418–58464 | turn 37 | version 0.12 -->
## v0.12 — 2. CandidateSource contract

> **Source sections:** `CAP-156`

The minimal interface:

```JavaScript
class CandidateSource {
    discover(context) {
        throw new Error('Not implemented');
    }

    describe() {
        return {
            id: 'unknown-source',
            name: 'Unknown Candidate Source'
        };
    }
}
```

A source returns **candidate proposals**:

```JavaScript
{
    target: 'https://example.com/manual.pdf',
    type: 'document',
    confidence: 0.91,
    hints: {
        mechanism: 'html-link'
    }
}
```

It does not do this:

```JavaScript
engine.enqueue(...)
```

and it does not do this:

```JavaScript
await fetch(...)
```

Those belong elsewhere.

---

<!-- CAP-157 | Continue Architecture Planning.md L58466–58480 | turn 37 | version 0.12 -->
## v0.12 — 3. CandidateSource is a search-space adapter

> **Source sections:** `CAP-157`

This is the deeper abstraction:

```
UNKNOWN SPACE
     │
     ▼
CandidateSource
     │
     ▼
NORMALIZED CANDIDATES
```

Different spaces can therefore be normalized into the same candidate model.

<!-- CAP-158 | Continue Architecture Planning.md L58482–58490 | turn 37 | version 0.12 -->
### v0.12 — Web page

> **Source sections:** `CAP-158`

```
HTML
 ↓
links
 ↓
Candidate
```

<!-- CAP-159 | Continue Architecture Planning.md L58492–58500 | turn 37 | version 0.12 -->
### v0.12 — Network traffic

> **Source sections:** `CAP-159`

```
Network observation
 ↓
GET endpoint
 ↓
Candidate
```

<!-- CAP-160 | Continue Architecture Planning.md L58502–58510 | turn 37 | version 0.12 -->
### v0.12 — Sitemap

> **Source sections:** `CAP-160`

```
sitemap.xml
 ↓
<loc>
 ↓
Candidate
```

<!-- CAP-161 | Continue Architecture Planning.md L58512–58518 | turn 37 | version 0.12 -->
### v0.12 — User seed

> **Source sections:** `CAP-161`

```
user enters URL
 ↓
Candidate
```

<!-- CAP-162 | Continue Architecture Planning.md L58520–58532 | turn 37 | version 0.12 -->
### v0.12 — Document

> **Source sections:** `CAP-162`

```
PDF
 ↓
embedded references
 ↓
Candidate
```

The scheduler doesn't need to know which one produced the candidate.

---

<!-- CAP-163 | Continue Architecture Planning.md L58534–58595 | turn 37 | version 0.12 -->
## v0.12 — 4. CandidateProposal

> **Source sections:** `CAP-163`

I would introduce an intermediate object rather than allowing sources to manufacture full `Candidate` objects.

```JavaScript
class CandidateProposal {
    constructor(data = {}) {
        this.target = data.target || '';
        this.type = data.type || 'unknown';

        this.confidence =
            Number.isFinite(data.confidence)
                ? data.confidence
                : 0.5;

        this.hints = {
            ...(data.hints || {})
        };

        this.sourceId =
            data.sourceId || null;

        this.sourceObservationId =
            data.sourceObservationId || null;

        this.parentTarget =
            data.parentTarget || null;

        this.createdAt =
            data.createdAt || Date.now();
    }

    serialize() {
        return {
            target: this.target,
            type: this.type,
            confidence: this.confidence,
            hints: this.hints,
            sourceId: this.sourceId,
            sourceObservationId:
                this.sourceObservationId,
            parentTarget:
                this.parentTarget,
            createdAt: this.createdAt
        };
    }
}
```

The distinction is:

```
Proposal
    │
    │ validation + canonicalization
    ▼
Candidate
```

That gives the engine a clean admission boundary.

---

<!-- CAP-164 | Continue Architecture Planning.md L58597–58637 | turn 37 | version 0.12 -->
## v0.12 — 5. Why proposals matter

> **Source sections:** `CAP-164`

Suppose an HTML parser emits:

```
https://example.com/a
https://example.com/a
https://example.com/a?utm_source=x
```

The source should not need to know the engine's identity rules.

The candidate normalizer handles:

```
URL normalization
       ↓
tracking stripping
       ↓
same-origin policy
       ↓
type inference
       ↓
identity
       ↓
deduplication
```

Thus:

```
CandidateSource
      ↓
raw proposals
      ↓
CandidateNormalizer
      ↓
KnowledgeBase
```

---

<!-- CAP-165 | Continue Architecture Planning.md L58639–58710 | turn 37 | version 0.12 -->
## v0.12 — 6. CandidateNormalizer

> **Source sections:** `CAP-165`

```JavaScript
class CandidateNormalizer {
    constructor(config = {}) {
        this.config = config;
    }

    normalize(proposal) {
        if (!proposal || !proposal.target) {
            return {
                accepted: false,
                reason: 'empty-target'
            };
        }

        let target;

        try {
            target = canonicalizeUrl(
                proposal.target,
                proposal.parentTarget ||
                location.href
            );
        } catch (_) {
            return {
                accepted: false,
                reason: 'invalid-url'
            };
        }

        if (!target) {
            return {
                accepted: false,
                reason: 'invalid-target'
            };
        }

        if (!isAllowedUrl(target)) {
            return {
                accepted: false,
                reason: 'url-policy'
            };
        }

        return {
            accepted: true,
            candidate: {
                target,
                type: proposal.type || 'unknown',
                confidence:
                    proposal.confidence,
                hints: {
                    ...proposal.hints
                },
                sourceId:
                    proposal.sourceId,
                sourceObservationId:
                    proposal.sourceObservationId,
                parentTarget:
                    proposal.parentTarget
            }
        };
    }
}
```

This establishes another important rule:

> **Sources generate possibilities; the core decides whether those possibilities become candidates.**

---

<!-- CAP-166 | Continue Architecture Planning.md L58712–58755 | turn 37 | version 0.12 -->
## v0.12 — 7. Source Registry

> **Source sections:** `CAP-166`

Just as v0.9 introduced an acquisition-provider registry, v0.12 needs a source registry.

```JavaScript
class CandidateSourceRegistry {
    constructor() {
        this.sources = [];
    }

    register(source) {
        this.sources.push(source);
        return this;
    }

    get(id) {
        return this.sources.find(
            source => source.describe().id === id
        ) || null;
    }

    describe() {
        return this.sources.map(
            source => source.describe()
        );
    }
}
```

The initial sources could be:

```
HTMLLinkSource
NetworkSource
MetadataSource
RobotsSource
SitemapSource
TextUrlSource
PerformanceSource
UserSeedSource
MutationSource
```

---

<!-- CAP-168 | Continue Architecture Planning.md L58813–58864 | turn 37 | version 0.12 -->
## v0.12 — 9. Evidence becomes an intermediate layer

> **Source sections:** `CAP-168`

This is an important v0.12 improvement.

Instead of:

```
HTML Provider → Candidate
```

use:

```
HTML Provider
     ↓
Evidence
     ↓
CandidateSource
     ↓
CandidateProposal
     ↓
Candidate
```

Example:

```JavaScript
{
    kind: 'html-link',
    value: '/manuals/x.pdf',
    locator: {
        selector: 'a[href]',
        attribute: 'href'
    }
}
```

Then:

```JavaScript
{
    target: 'https://example.com/manuals/x.pdf',
    type: 'document',
    confidence: 0.95,
    sourceId: 'html-link-source',
    evidenceId: 'ev-381'
}
```

Now provenance is explicit.

---

<!-- CAP-169 | Continue Architecture Planning.md L58866–58894 | turn 37 | version 0.12 -->
## v0.12 — 10. Discovery becomes evidence-driven

> **Source sections:** `CAP-169`

The complete chain becomes:

```
             OBSERVATION
                  │
                  ▼
             RECOGNITION
                  │
                  ▼
               EVIDENCE
                  │
                  ▼
          CANDIDATE SOURCES
                  │
                  ▼
             PROPOSALS
                  │
                  ▼
          NORMALIZATION/POLICY
                  │
                  ▼
             CANDIDATES
```

This is significantly stronger than directly extracting URLs.

---

<!-- CAP-170 | Continue Architecture Planning.md L58896–58930 | turn 37 | version 0.12 -->
## v0.12 — 11. CandidateSource context

> **Source sections:** `CAP-170`

A source should receive a context object:

```JavaScript
{
    observation,
    evidence,
    parentCandidate,
    knowledgeBase,
    configuration
}
```

But there is an important boundary:

**the source gets read access to context; it should not mutate the core.**

Conceptually:

```
CandidateSource
       │
       ├── READ observation
       ├── READ evidence
       ├── READ parent
       └── READ configuration
                │
                ▼
           proposals[]
```

This prevents source plugins from becoming hidden engines.

---

<!-- CAP-171 | Continue Architecture Planning.md L58932–58932 | turn 37 | version 0.12 -->
## v0.12 — 12. CandidateSource examples

> **Source sections:** `CAP-171`



<!-- CAP-172 | Continue Architecture Planning.md L58934–58978 | turn 37 | version 0.12 -->
### v0.12 — HTML link source

> **Source sections:** `CAP-172`

```JavaScript
class HtmlLinkSource extends CandidateSource {
    discover(context) {
        const proposals = [];

        for (const link of context.evidence.links || []) {
            proposals.push(
                new CandidateProposal({
                    target: link.url,
                    type: 'link',
                    confidence: 0.9,
                    sourceId: 'html-link',
                    sourceObservationId:
                        context.observation.id,
                    parentTarget:
                        context.observation.target
                })
            );
        }

        return proposals;
    }

    describe() {
        return {
            id: 'html-link',
            name: 'HTML Link Source'
        };
    }
}
```

Notice what it doesn't do:

```
no fetch
no queue
no policy decision
no persistence
no scheduler
```

---

<!-- CAP-173 | Continue Architecture Planning.md L58980–59027 | turn 37 | version 0.12 -->
## v0.12 — 13. NetworkSource

> **Source sections:** `CAP-173`

Network observations become another candidate source.

```
NetworkEvent
      │
      ├── GET
      │     ↓
      │   CandidateProposal
      │
      └── POST
            ↓
       representational evidence
       but no executable candidate
```

This is where the v0.8 capability model pays off.

A POST endpoint can be represented:

```JavaScript
{
    target: '/api/order',
    type: 'api',
    hints: {
        method: 'POST'
    }
}
```

But the normal acquisition policy can still reject it.

Thus:

```
Network observation
       ↓
Candidate representation
       ↓
Policy
       ↓
DENIED
```

rather than silently throwing the information away.

---

<!-- CAP-174 | Continue Architecture Planning.md L59029–59056 | turn 37 | version 0.12 -->
## v0.12 — 14. Search-space composition

> **Source sections:** `CAP-174`

The most interesting consequence is that multiple sources can operate simultaneously.

```
                  DISCOVERY CONTEXT
                         │
       ┌─────────────────┼──────────────────┐
       ▼                 ▼                  ▼
 HTML Source       Network Source     Metadata Source
       │                 │                  │
       ▼                 ▼                  ▼
 proposals[]        proposals[]        proposals[]
       │                 │                  │
       └─────────────────┼──────────────────┘
                         ▼
                  NORMALIZATION
                         ▼
                    DEDUPLICATION
                         ▼
                     CANDIDATES
```

This is much closer to a generalized blind scan.

The engine does not assume one discovery mechanism.

---

<!-- CAP-175 | Continue Architecture Planning.md L59058–59094 | turn 37 | version 0.12 -->
## v0.12 — 15. Candidate identity

> **Source sections:** `CAP-175`
>
> [DOCUMENTATION REVIEW] Contradiction **C-04** ([Review Notes](../REVIEW-NOTES.md#c-04--))

The identity remains:

```
(type, canonical-target)
```

not:

```
source + target
```

Therefore five sources discovering the same resource produce:

```
                    resource X
                 /   /   |   \   \
              HTML net meta sitemap user
```

but one canonical candidate.

The provenance retains all five discovery paths.

That gives us:

```
IDENTITY
    ≠
PROVENANCE
```

This distinction is essential.

---

<!-- CAP-176 | Continue Architecture Planning.md L59096–59144 | turn 37 | version 0.12 -->
## v0.12 — 16. Discovery confidence aggregation

> **Source sections:** `CAP-176`
>
> [DOCUMENTATION REVIEW] Contradiction **C-06** ([Review Notes](../REVIEW-NOTES.md#c-06--))

Multiple independent sources can strengthen confidence.

Example:

```
HTML link       0.90
sitemap         0.95
network         0.85
metadata        0.70
```

Do **not** simply sum:

```
0.90 + 0.95 + ...
```

because confidence isn't necessarily additive.

Instead store evidence independently:

```JavaScript
{
    candidateId: 'cand-123',

    evidence: [
        {
            sourceId: 'html-link',
            confidence: 0.90
        },
        {
            sourceId: 'sitemap',
            confidence: 0.95
        },
        {
            sourceId: 'network',
            confidence: 0.85
        }
    ]
}
```

A later scoring layer can decide how to combine them.

This avoids baking probabilistic assumptions into discovery.

---

<!-- CAP-177 | Continue Architecture Planning.md L59146–59206 | turn 37 | version 0.12 -->
## v0.12 — 17. v0.12 provenance graph

> **Source sections:** `CAP-177`

We now have:

```
SOURCE
  │
  ▼
PROPOSAL
  │
  ▼
CANDIDATE
  │
  ▼
PLAN
  │
  ▼
PROVIDER
  │
  ▼
OBSERVATION
  │
  ▼
RECOGNITION
  │
  ▼
EVIDENCE
  │
  ▼
PROPOSAL
```

Which creates a loop:

```
       ┌────────────────────────────────────┐
       │                                    │
       ▼                                    │
  CandidateSource                           │
       │                                    │
       ▼                                    │
   Candidate                                │
       │                                    │
       ▼                                    │
   Acquisition                              │
       │                                    │
       ▼                                    │
  Observation                               │
       │                                    │
       ▼                                    │
 Recognition                                │
       │                                    │
       ▼                                    │
   Evidence                                 │
       │                                    │
       └──────────► CandidateSource ─────────┘
```

That is the actual **discovery feedback loop**.

---
