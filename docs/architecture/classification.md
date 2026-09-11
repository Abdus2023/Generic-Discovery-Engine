# Resource Type System and Classification

> **Status:** DESIGNED
>
> **Source:** `Continue Architecture Planning.md`
>
> **Purpose:** Semantic classification of resources: type axes, classifiers, classification runtime and the type registry.

## Source Sections

- **v0.18 — Resource Type System + Semantic Classification** — `CAP-420` — `Continue Architecture Planning.md` L66696–66734
- **v0.18 — Resource Type System + Semantic Classification** — `CAP-422` — `Continue Architecture Planning.md` L66746–66789
- **v0.18 — 18.1 The Type Problem** — `CAP-423` — `Continue Architecture Planning.md` L66791–66853
- **v0.18 — 18.2 Four Orthogonal Type Dimensions** — `CAP-424` — `Continue Architecture Planning.md` L66855–66915
- **v0.18 — 18.3 ResourceType** — `CAP-425` — `Continue Architecture Planning.md` L66917–66975
- **v0.18 — 18.4 Classification Assertion** — `CAP-426` — `Continue Architecture Planning.md` L66977–67046
- **v0.18 — 18.5 Type Evidence** — `CAP-427` — `Continue Architecture Planning.md` L67048–67116
- **v0.18 — 18.6 Evidence Strength Must Be Axis-Specific** — `CAP-428` — `Continue Architecture Planning.md` L67118–67166
- **v0.18 — 18.7 Classification Pipeline** — `CAP-429` — `Continue Architecture Planning.md` L67168–67201
- **v0.18 — 18.8 Recognition vs Classification** — `CAP-430` — `Continue Architecture Planning.md` L67203–67205
- **v0.18 — Recognition** — `CAP-431` — `Continue Architecture Planning.md` L67207–67224
- **v0.18 — Classification** — `CAP-432` — `Continue Architecture Planning.md` L67226–67264
- **v0.18 — 18.9 Classification Runtime** — `CAP-433` — `Continue Architecture Planning.md` L67266–67329
- **v0.18 — 18.10 Example Classifiers** — `CAP-434` — `Continue Architecture Planning.md` L67331–67380
- **v0.18 — 18.11 Hierarchical Classification** — `CAP-435` — `Continue Architecture Planning.md` L67382–67434
- **v0.18 — 18.12 Do Not Use One Global Confidence Score** — `CAP-436` — `Continue Architecture Planning.md` L67436–67483
- **v0.18 — 18.13 Classification Is Versioned** — `CAP-437` — `Continue Architecture Planning.md` L67485–67526
- **v0.18 — 18.14 Contradictory Classification** — `CAP-438` — `Continue Architecture Planning.md` L67528–67571
- **v0.18 — 18.15 Classification Graph** — `CAP-439` — `Continue Architecture Planning.md` L67573–67615
- **v0.18 — 18.16 Resource Model After v0.18** — `CAP-440` — `Continue Architecture Planning.md` L67617–67658
- **v0.18 — 18.17 Resource Type Registry** — `CAP-441` — `Continue Architecture Planning.md` L67660–67735
- **v0.18 — 18.19 Classification → Strategy** — `CAP-443` — `Continue Architecture Planning.md` L67796–67823
- **v0.18 — 18.20 Classification Work as WorkItem** — `CAP-444` — `Continue Architecture Planning.md` L67825–67866

## Related Documents

- [Resource, Representation and Revision Model](resource-model.md)
- [Response Recognition](../acquisition/response-recognition.md)
- [Strategies, Query Planning and Enumeration](strategy-and-planning.md)

---

<!-- CAP-420 | Continue Architecture Planning.md L66696–66734 | turn 47 | version 0.18 -->
## v0.18 — Resource Type System + Semantic Classification

> **Source sections:** `CAP-420`

The progression would become:

```
Locator
   ↓
Identity Resolution
   ↓
Resource
   ↓
Semantic Classification
   ↓
Resource Type
   ↓
Capabilities / Acquisition Strategy
   ↓
Verification Requirements
```

The crucial rule for v0.18 should be:

> **Resource type is an evidence-backed interpretation, not an intrinsic property of a URL.**

That will let the engine distinguish:

```
URL extension
    ≠
declared MIME type
    ≠
observed MIME type
    ≠
magic-byte identity
    ≠
semantic document classification
```

and prevent the discovery engine from prematurely deciding that every `.pdf`, `/api/`, `/manual/`, or `download` URL means the same thing.

<!-- CAP-422 | Continue Architecture Planning.md L66746–66789 | turn 49 | version 0.18 -->
## v0.18 — Resource Type System + Semantic Classification

> **Source sections:** `CAP-422`

The next boundary should make one distinction explicit:

> **A resource's identity is not the same thing as its type, format, or semantic role.**

At v0.17 we established:

```
Candidate
   ↓
Locator
   ↓
Resource
   ↓
Identity / Relations
```

Now we add interpretation:

```
                         RESOURCE
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
       Representation    Behavior       Semantic Role
       / Format          / Function      / Meaning
             │              │              │
        PDF / HTML       page / API     service-manual
        JSON / ZIP       feed / file    parts-catalog
        JPEG / XML       endpoint       bulletin
```

This is important because:

```
PDF
≠
Service Manual
```

A PDF can be a service manual, parts catalog, brochure, bulletin, or completely unrelated document.

---

<!-- CAP-423 | Continue Architecture Planning.md L66791–66853 | turn 49 | version 0.18 -->
## v0.18 — 18.1 The Type Problem

> **Source sections:** `CAP-423`

The old model tends toward:

```JavaScript
resource.type = "pdf";
```

That is too coarse.

Consider:

```
https://example.com/document
```

Evidence might say:

```
URL:
    no .pdf extension

HTTP:
    Content-Type: application/pdf

Bytes:
    %PDF-

Title:
    "Gen2 Service Manual"

Text:
    "Maintenance procedures..."
    "Troubleshooting..."
    "Adjustment..."
```

The resulting interpretation should be something like:

```
Representation:
    PDF

Technical format:
    application/pdf

Semantic class:
    service-manual

Domain role:
    maintenance-document

Confidence:
    high
```

Not:

```
type = "pdf"
```

---

<!-- CAP-424 | Continue Architecture Planning.md L66855–66915 | turn 49 | version 0.18 -->
## v0.18 — 18.2 Four Orthogonal Type Dimensions

> **Source sections:** `CAP-424`

I would make the type system explicitly multidimensional.

```
Resource
│
├── representation
│   ├── html
│   ├── pdf
│   ├── json
│   ├── xml
│   ├── jpeg
│   ├── zip
│   └── binary
│
├── transport_role
│   ├── page
│   ├── endpoint
│   ├── download
│   ├── feed
│   ├── sitemap
│   └── media
│
├── semantic_role
│   ├── service-manual
│   ├── parts-catalog
│   ├── troubleshooting-guide
│   ├── technical-bulletin
│   ├── maintenance-guide
│   └── unknown
│
└── domain_class
    ├── technical-document
    ├── software-artifact
    ├── dataset
    ├── media
    └── unknown
```

This prevents an important category error:

```
"PDF"
```

answers:

> What representation is this?

while:

```
"Service Manual"
```

answers:

> What does this resource mean/function as?

---

<!-- CAP-425 | Continue Architecture Planning.md L66917–66975 | turn 49 | version 0.18 -->
## v0.18 — 18.3 ResourceType

> **Source sections:** `CAP-425`

Instead of a single string, introduce a structured type descriptor.

```JavaScript
class ResourceType {
    constructor(data = {}) {
        this.id = data.id || makeId('rtype');

        this.axis = data.axis || 'unknown';

        this.namespace = data.namespace || 'generic';

        this.name = data.name || 'unknown';

        this.parent = data.parent || null;

        this.version = data.version || '1';

        this.createdAt = data.createdAt || now();
    }

    serialize() {
        return {
            id: this.id,
            axis: this.axis,
            namespace: this.namespace,
            name: this.name,
            parent: this.parent,
            version: this.version,
            createdAt: this.createdAt
        };
    }
}
```

Examples:

```JavaScript
new ResourceType({
    axis: 'representation',
    namespace: 'mime',
    name: 'application/pdf'
});
```

and:

```JavaScript
new ResourceType({
    axis: 'semantic-role',
    namespace: 'document',
    name: 'service-manual'
});
```

These are different types because they live on different axes.

---

<!-- CAP-426 | Continue Architecture Planning.md L66977–67046 | turn 49 | version 0.18 -->
## v0.18 — 18.4 Classification Assertion

> **Source sections:** `CAP-426`

The engine should not simply overwrite the resource.

Instead:

```
Resource
   │
   ├── Classification Assertion A
   ├── Classification Assertion B
   ├── Classification Assertion C
   └── Classification Assertion D
```

Each assertion has evidence.

```JavaScript
class ClassificationAssertion {
    constructor(data = {}) {
        this.id = data.id || makeId('class');

        this.resourceId = data.resourceId || null;

        this.axis = data.axis || 'unknown';

        this.type = data.type || 'unknown';

        this.confidence = Number.isFinite(data.confidence)
            ? data.confidence
            : 0;

        this.evidenceIds = data.evidenceIds || [];

        this.classifierId = data.classifierId || null;

        this.classifierVersion = data.classifierVersion || null;

        this.status = data.status || 'active';

        this.createdAt = data.createdAt || now();
    }

    serialize() {
        return { ...this };
    }
}
```

Now we can represent:

```
Resource R42

representation:
    PDF                  confidence 1.00
    evidence: magic-bytes

semantic-role:
    service-manual       confidence 0.94
    evidence: title + text structure

semantic-role:
    technical-bulletin   confidence 0.12
    evidence: weak keyword match
```

The second assertion does not need to disappear.

---

<!-- CAP-427 | Continue Architecture Planning.md L67048–67116 | turn 49 | version 0.18 -->
## v0.18 — 18.5 Type Evidence

> **Source sections:** `CAP-427`

Classification must be evidence-backed.

```JavaScript
class TypeEvidence {
    constructor(data = {}) {
        this.id = data.id || makeId('te');

        this.resourceId = data.resourceId || null;

        this.axis = data.axis || null;

        this.observationId = data.observationId || null;

        this.kind = data.kind || 'unknown';

        this.value = data.value ?? null;

        this.locator = data.locator || null;

        this.weight = Number.isFinite(data.weight)
            ? data.weight
            : 0;

        this.provenance = data.provenance || {};

        this.createdAt = data.createdAt || now();
    }
}
```

Examples:

```JavaScript
{
    kind: 'http-content-type',
    value: 'application/pdf',
    weight: 0.80
}
```

```JavaScript
{
    kind: 'magic-bytes',
    value: '%PDF-',
    weight: 1.00
}
```

```JavaScript
{
    kind: 'url-extension',
    value: '.pdf',
    weight: 0.20
}
```

And semantic evidence:

```JavaScript
{
    kind: 'document-title',
    value: 'Gen2 Service Manual',
    weight: 0.85
}
```

---

<!-- CAP-428 | Continue Architecture Planning.md L67118–67166 | turn 49 | version 0.18 -->
## v0.18 — 18.6 Evidence Strength Must Be Axis-Specific

> **Source sections:** `CAP-428`

A major refinement:

> **Evidence strength cannot be globally ranked.**

For example:

```
URL extension ".pdf"
```

is weak evidence for representation.

But:

```
URL contains "/manual/"
```

could be moderately useful evidence for semantic role.

Similarly:

```
application/pdf
```

is strong technical evidence but almost useless for deciding whether the document is a service manual.

Therefore:

```
Evidence Weight
```

must be interpreted relative to:

```
Axis + Classification Target
```

Not:

```
Evidence = universally strong/weak
```

---

<!-- CAP-429 | Continue Architecture Planning.md L67168–67201 | turn 49 | version 0.18 -->
## v0.18 — 18.7 Classification Pipeline

> **Source sections:** `CAP-429`

The resulting architecture becomes:

```
                  OBSERVATION
                       │
                       ▼
              RESPONSE RECOGNITION
                       │
                       ▼
             TECHNICAL EVIDENCE
                       │
                       ▼
                    RESOURCE
                       │
                       ▼
             CLASSIFICATION RUNTIME
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
   Representation   Behavior    Semantic Role
          │            │            │
          ▼            ▼            ▼
       PDF          endpoint    service-manual
          │            │            │
          └────────────┼────────────┘
                       ▼
             Classification Graph
```

This is deliberately downstream from recognition.

---

<!-- CAP-430 | Continue Architecture Planning.md L67203–67205 | turn 49 | version 0.18 -->
## v0.18 — 18.8 Recognition vs Classification

> **Source sections:** `CAP-430`
>
> [DOCUMENTATION REVIEW] Contradiction **C-02** ([Review Notes](../REVIEW-NOTES.md#c-02--))

These two concepts should remain separate.

<!-- CAP-431 | Continue Architecture Planning.md L67207–67224 | turn 49 | version 0.18 -->
### v0.18 — Recognition

> **Source sections:** `CAP-431`
>
> [DOCUMENTATION REVIEW] Contradiction **C-02** ([Review Notes](../REVIEW-NOTES.md#c-02--))

Answers:

> What did we obtain?

Examples:

```
HTML
JSON
PDF
XML
JPEG
unknown binary
```

Recognition primarily operates on an **Observation**.

<!-- CAP-432 | Continue Architecture Planning.md L67226–67264 | turn 49 | version 0.18 -->
### v0.18 — Classification

> **Source sections:** `CAP-432`

Answers:

> What kind of resource does this represent?

Examples:

```
web page
API endpoint
service manual
parts catalog
technical bulletin
software package
dataset
```

Classification primarily operates on a **Resource**, using one or more observations.

Therefore:

```
Observation
     ↓
Recognition
     ↓
Resource
     ↓
Classification
```

Not:

```
Observation → "final type"
```

---

<!-- CAP-433 | Continue Architecture Planning.md L67266–67329 | turn 49 | version 0.18 -->
## v0.18 — 18.9 Classification Runtime

> **Source sections:** `CAP-433`

Introduce:

```JavaScript
class Classifier {
    priority() {
        return 0;
    }

    canClassify(context) {
        return false;
    }

    classify(context) {
        return [];
    }

    describe() {
        return {
            id: 'unknown-classifier',
            name: 'Unknown Classifier'
        };
    }
}
```

Then:

```JavaScript
class ClassificationRuntime {
    constructor(classifiers = []) {
        this.classifiers = classifiers;
    }

    async classify(resource, context) {
        const assertions = [];

        for (const classifier of this.classifiers) {
            if (!classifier.canClassify({
                resource,
                context
            })) {
                continue;
            }

            const results = await classifier.classify({
                resource,
                context
            });

            assertions.push(...results);
        }

        return assertions;
    }
}
```

The runtime coordinates classifiers.

It does **not** decide the semantic truth itself.

---

<!-- CAP-434 | Continue Architecture Planning.md L67331–67380 | turn 49 | version 0.18 -->
## v0.18 — 18.10 Example Classifiers

> **Source sections:** `CAP-434`

A generic engine can start with technical classifiers:

```
MimeClassifier
MagicByteClassifier
ExtensionClassifier
HeaderClassifier
```

Then semantic classifiers:

```
TitleClassifier
MetadataClassifier
DocumentStructureClassifier
KeywordClassifier
LinkStructureClassifier
SchemaClassifier
```

And eventually domain-specific classifiers:

```
TechnicalDocumentClassifier
ServiceManualClassifier
PartsCatalogClassifier
BulletinClassifier
```

This gives us a clean extension point.

The generic engine does not need to know anything about Otis.

Instead:

```
Generic Discovery Engine
        │
        ├── generic classifiers
        │
        └── domain classifier plugins
                 │
                 ├── elevator documents
                 ├── automotive manuals
                 └── industrial documentation
```

---

<!-- CAP-435 | Continue Architecture Planning.md L67382–67434 | turn 49 | version 0.18 -->
## v0.18 — 18.11 Hierarchical Classification

> **Source sections:** `CAP-435`

Types should support hierarchy.

For example:

```
document
│
├── technical-document
│   │
│   ├── service-manual
│   ├── maintenance-guide
│   ├── troubleshooting-guide
│   ├── parts-catalog
│   └── technical-bulletin
│
├── administrative-document
│
└── marketing-document
```

This gives useful reasoning:

```
service-manual
      ↓
technical-document
      ↓
document
```

A query can therefore ask:

```
find resources classified as "document"
```

or:

```
find resources classified as "technical-document"
```

or specifically:

```
find resources classified as "service-manual"
```

without losing the finer classification.

---

<!-- CAP-436 | Continue Architecture Planning.md L67436–67483 | turn 49 | version 0.18 -->
## v0.18 — 18.12 Do Not Use One Global Confidence Score

> **Source sections:** `CAP-436`
>
> [DOCUMENTATION REVIEW] Contradiction **C-06** ([Review Notes](../REVIEW-NOTES.md#c-06--))

Another important constraint.

Avoid:

```JavaScript
confidence: 0.93
```

as the sole representation of classification certainty.

Instead:

```
Assertion
│
├── confidence
├── evidenceIds
├── classifier
├── classifierVersion
├── status
└── contradictions
```

For example:

```
service-manual
confidence = 0.91

Supporting:
    title-match             +0.40
    maintenance-terms       +0.25
    troubleshooting-section +0.20
    PDF representation      +0.05

Contradicting:
    brochure-like structure -0.10
```

The exact scoring model can evolve later.

The important architectural property is:

> **The evidence remains inspectable even if the scoring algorithm changes.**

---

<!-- CAP-437 | Continue Architecture Planning.md L67485–67526 | turn 49 | version 0.18 -->
## v0.18 — 18.13 Classification Is Versioned

> **Source sections:** `CAP-437`

Suppose classifier v1 says:

```
service-manual = 0.72
```

Later classifier v2 improves its rules:

```
service-manual = 0.94
```

Do not mutate historical evidence.

Store:

```
Classification A
classifier = service-doc-v1
confidence = 0.72

Classification B
classifier = service-doc-v2
confidence = 0.94
```

Then:

```
Resource
  │
  ├── Observation
  ├── Evidence
  ├── Classification v1
  └── Classification v2
```

This is especially important if the engine eventually becomes a research/acquisition system.

---

<!-- CAP-438 | Continue Architecture Planning.md L67528–67571 | turn 49 | version 0.18 -->
## v0.18 — 18.14 Contradictory Classification

> **Source sections:** `CAP-438`

Consider:

```
Title:
"Service Manual"

Body:
"Product Brochure"

Metadata:
"marketing"
```

The system should not silently choose one.

Instead:

```
Resource R
│
├── service-manual
│     ├── supported by title
│     └── confidence 0.71
│
└── marketing-brochure
      ├── supported by structure
      └── confidence 0.64
```

Classification assertions can therefore have:

```
active
rejected
contradicted
superseded
uncertain
```

This preserves epistemic history.

---

<!-- CAP-439 | Continue Architecture Planning.md L67573–67615 | turn 49 | version 0.18 -->
## v0.18 — 18.15 Classification Graph

> **Source sections:** `CAP-439`

We now extend the ResourceGraph:

```
                         RESOURCE
                            │
             ┌──────────────┼──────────────┐
             │              │              │
             ▼              ▼              ▼
         Locator       Observation     Classification
                            │              │
                            ▼              ▼
                         Evidence       Type
                                           │
                                           ▼
                                       Assertion
```

Graph edges:

```JavaScript
{
    from: 'resource-42',
    to: 'class-91',
    relation: 'classified-as',
    evidenceIds: ['te-17', 'te-18']
}
```

And:

```JavaScript
{
    from: 'class-91',
    to: 'type-service-manual',
    relation: 'instance-of'
}
```

This means classification becomes queryable rather than being hidden inside a field.

---

<!-- CAP-440 | Continue Architecture Planning.md L67617–67658 | turn 49 | version 0.18 -->
## v0.18 — 18.16 Resource Model After v0.18

> **Source sections:** `CAP-440`

The resource model should now look approximately like:

```JavaScript
class Resource {
    constructor(data = {}) {
        this.id = data.id || makeId('resource');

        this.locatorIds = data.locatorIds || [];

        this.observationIds = data.observationIds || [];

        this.claimIds = data.claimIds || [];

        this.fingerprintIds = data.fingerprintIds || [];

        this.classificationIds =
            data.classificationIds || [];

        this.createdAt =
            data.createdAt || now();

        this.updatedAt =
            data.updatedAt || this.createdAt;
    }
}
```

Notice what disappeared:

```JavaScript
this.type
```

That is intentional.

The resource itself does not need to contain a single authoritative `type`.

Its classifications live in the graph.

---

<!-- CAP-441 | Continue Architecture Planning.md L67660–67735 | turn 49 | version 0.18 -->
## v0.18 — 18.17 Resource Type Registry

> **Source sections:** `CAP-441`

We need a registry for known types.

```JavaScript
class ResourceTypeRegistry {
    constructor() {
        this.types = new Map();
    }

    register(type) {
        if (this.types.has(type.id)) {
            throw new Error(
                `Resource type already registered: ${type.id}`
            );
        }

        this.types.set(type.id, type);
        return type;
    }

    get(id) {
        return this.types.get(id) || null;
    }

    find(axis, name) {
        for (const type of this.types.values()) {
            if (
                type.axis === axis &&
                type.name === name
            ) {
                return type;
            }
        }

        return null;
    }
}
```

Example registry:

```
representation:
    html
    pdf
    json
    xml
    css
    javascript
    jpeg
    png
    zip
    binary

transport-role:
    page
    endpoint
    download
    feed
    sitemap
    media

semantic-role:
    document
    technical-document
    service-manual
    maintenance-guide
    troubleshooting-guide
    parts-catalog
    bulletin
    dataset
    software-artifact
```

---

<!-- CAP-443 | Continue Architecture Planning.md L67796–67823 | turn 49 | version 0.18 -->
## v0.18 — 18.19 Classification → Strategy

> **Source sections:** `CAP-443`

This gives us the beginning of a much more powerful architecture.

```
Resource
   │
   ▼
Classification
   │
   ├── PDF
   ├── service-manual
   └── technical-document
          │
          ▼
     Strategy Resolver
          │
          ├── extract text
          ├── inspect metadata
          ├── inspect pages
          ├── OCR
          ├── search references
          └── discover revisions
```

The classification therefore informs **what to do next**, rather than pretending to be the action itself.

---

<!-- CAP-444 | Continue Architecture Planning.md L67825–67866 | turn 49 | version 0.18 -->
## v0.18 — 18.20 Classification Work as WorkItem

> **Source sections:** `CAP-444`

The v0.15 `WorkItem` model now pays off.

We can introduce:

```JavaScript
{
    kind: 'classification',

    sessionId: 'scan-001',

    parentId: 'work-acquisition-42',

    payload: {
        resourceId: 'resource-77',
        observationIds: [
            'obs-91',
            'obs-92'
        ]
    }
}
```

The unified frontier becomes:

```
                  FRONTIER RUNTIME
                        │
        ┌───────────────┼────────────────┐
        │               │                │
        ▼               ▼                ▼
   DiscoveryWork   AcquisitionWork   ClassificationWork
        │               │                │
        └───────────────┼────────────────┘
                        ▼
                  Shared lifecycle
```

This is cleaner than inventing a completely separate queue.

---
