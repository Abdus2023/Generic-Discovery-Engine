# Response Recognition

> **Status:** DESIGNED
>
> **Source:** `Continue Architecture Planning.md`; `Userscript Discovery Prototype.md`
>
> **Purpose:** Recognition of acquired responses: recognition providers, routers, confidence, evidence and failure taxonomy.

## Contents

- **4. Lock is not discovery** — `Userscript Discovery Prototype.md` L250–301
- **LockResult** — `Userscript Discovery Prototype.md` L1509–1526
- **v0.11 — Response Recognition Runtime** — `Continue Architecture Planning.md` L57355–57366
- **v0.11 — 2. RecognitionProvider contract** — `Continue Architecture Planning.md` L57444–57493
- **v0.11 — 3. Recognition is not discovery** — `Continue Architecture Planning.md` L57495–57542
- **v0.11 — 4. Response Router** — `Continue Architecture Planning.md` L57544–57581
- **v0.11 — 5. Provider priority** — `Continue Architecture Planning.md` L57583–57642
- **v0.11 — 6. Recognition confidence** — `Continue Architecture Planning.md` L57644–57679
- **v0.11 — 7. Content-type is only one signal** — `Continue Architecture Planning.md` L57681–57715
- **v0.11 — 8. Recognition evidence** — `Continue Architecture Planning.md` L57717–57760
- **v0.11 — 9. Recognition result contract** — `Continue Architecture Planning.md` L57762–57796
- **v0.11 — 10. Why providers should not enqueue candidates** — `Continue Architecture Planning.md` L57798–57842
- **v0.11 — 11. Recognition Runtime** — `Continue Architecture Planning.md` L57844–57891
- **v0.11 — No recognizer** — `Continue Architecture Planning.md` L57899–57905
- **v0.11 — Provider rejected** — `Continue Architecture Planning.md` L57907–57913
- **v0.11 — Provider error** — `Continue Architecture Planning.md` L57915–57921
- **v0.11 — Successful recognition, zero discoveries** — `Continue Architecture Planning.md` L57923–57935
- **v0.11 — 13. v0.11 state progression** — `Continue Architecture Planning.md` L57937–57989
- **v0.11 — 14. Multiple recognizers** — `Continue Architecture Planning.md` L57991–58034
- **v0.11 — 15. Recognition graph** — `Continue Architecture Planning.md` L58036–58066
- **v0.11 — 16. The graph is now explicitly causal** — `Continue Architecture Planning.md` L58068–58127
- **v0.11 — 17. v0.11 event ledger** — `Continue Architecture Planning.md` L58129–58167
- **v0.11 — 18. The emerging generic algorithm** — `Continue Architecture Planning.md` L58169–58238
- **v0.16 — Recognition** — `Continue Architecture Planning.md` L65186–65190

## Related Documents

- [Acquisition Model](acquisition-model.md)
- [Resource Type System and Classification](../architecture/classification.md)
- [Discovery Model](../architecture/discovery-model.md)
- [Providers Overview](../providers/overview.md)

---

<!-- source: Userscript Discovery Prototype.md L250–301 | turn 3 | version ? -->
## 4. Lock is not discovery

A very important distinction is:

```
RF detection
    ≠
demodulator lock
    ≠
valid transport stream
    ≠
valid DVB service
```

You can have:

```
Signal detected       ✓
Carrier synchronized  ✓
FEC synchronized      ✓
Transport stream      ✗
```

and that should **not** become a discovered multiplex.

A robust state machine might therefore be:

```
UNKNOWN
  │
  ▼
SIGNAL_DETECTED
  │
  ▼
CARRIER_LOCK
  │
  ▼
FEC_LOCK
  │
  ▼
STREAM_LOCK
  │
  ▼
DVB_CONFIRMED
  │
  ▼
SERVICES_DISCOVERED
```

Each transition should have a timeout so one bad candidate cannot stall the scan.

---

<!-- source: Userscript Discovery Prototype.md L1509–1526 | turn 11 | version ? -->
### LockResult

Keep acquisition details separate:

```
LockResult {
    carrier_lock
    timing_lock
    fec_lock
    stream_lock
    delivery_system?
    acquisition_time
}
```

This makes failure analysis much easier.

---

<!-- source: Continue Architecture Planning.md L57355–57366 | turn 35 | version 0.11 -->
## v0.11 — Response Recognition Runtime

v0.10 established the **Acquisition Runtime** boundary.

The next symmetry is:

> **Acquisition providers answer: “How do I obtain this?”**  
> **Recognition providers answer: “What did I obtain?”**

The important change is that recognition should no longer be a large `if/else` chain inside the engine.

---

<!-- source: Continue Architecture Planning.md L57444–57493 | turn 35 | version 0.11 -->
## v0.11 — 2. RecognitionProvider contract

The provider should remain deliberately small.

```JavaScript
class RecognitionProvider {
    canRecognize(observation) {
        return false;
    }

    recognize(observation) {
        return [];
    }

    describe() {
        return {
            id: 'unknown',
            name: 'Unknown Recognition Provider'
        };
    }
}
```

But there is an important refinement.

`canRecognize()` should not parse the entire response.

It should primarily inspect:

```
content type
target type
HTTP metadata
magic bytes
candidate hints
```

Then:

```
canRecognize()
      ↓
cheap routing decision
      ↓
recognize()
      ↓
actual parsing
```

---

<!-- source: Continue Architecture Planning.md L57495–57542 | turn 35 | version 0.11 -->
## v0.11 — 3. Recognition is not discovery

These concepts should remain separate.

```
Observation
    ↓
Recognition
    ↓
Discovery
```

For example:

```
GET /index.html
       ↓
200 text/html
       ↓
recognized as HTML
       ↓
extract:
  /manual.pdf
  /api/status
  /docs/
```

Recognition:

```
HTML
```

Discovery:

```
manual.pdf
/api/status
/docs/
```

So:

```
recognized ≠ discovered
```

---

<!-- source: Continue Architecture Planning.md L57544–57581 | turn 35 | version 0.11 -->
## v0.11 — 4. Response Router

The router is responsible for provider selection.

```JavaScript
class ResponseRouter {
    constructor() {
        this.providers = [];
    }

    register(provider) {
        this.providers.push(provider);
        return this;
    }

    select(observation) {
        for (const provider of this.providers) {
            try {
                if (provider.canRecognize(observation)) {
                    return provider;
                }
            } catch (_) {
                // Provider routing must not kill the scan.
            }
        }

        return null;
    }
}
```

The critical property is:

> **Recognition provider selection must be deterministic.**

Provider registration order should therefore either be explicitly defined or replaced by a priority system.

---

<!-- source: Continue Architecture Planning.md L57583–57642 | turn 35 | version 0.11 -->
## v0.11 — 5. Provider priority

A better v0.11 contract:

```JavaScript
class RecognitionProvider {
    priority() {
        return 0;
    }

    canRecognize(observation) {
        return false;
    }

    recognize(observation) {
        return [];
    }
}
```

Router:

```JavaScript
select(observation) {
    return this.providers
        .filter(provider => {
            try {
                return provider.canRecognize(observation);
            } catch (_) {
                return false;
            }
        })
        .sort(
            (a, b) =>
                b.priority() - a.priority()
        )[0] || null;
}
```

This matters because several providers may recognize the same response.

For example:

```
application/octet-stream
```

could potentially be:

```
PDF
ZIP
WASM
image
unknown binary
```

The router should allow more specialized recognizers to win.

---

<!-- source: Continue Architecture Planning.md L57644–57679 | turn 35 | version 0.11 -->
## v0.11 — 6. Recognition confidence

Recognition itself can have confidence:

```JavaScript
{
    providerId: 'pdf',
    confidence: 0.98
}
```

But confidence should not silently become authorization.

Therefore:

```
confidence
    ≠
authority
```

A provider saying:

```
"This looks like PDF"
```

does not mean:

```
"This is definitely PDF"
```

The evidence model should preserve that distinction.

---

<!-- source: Continue Architecture Planning.md L57681–57715 | turn 35 | version 0.11 -->
## v0.11 — 7. Content-type is only one signal

A robust recognizer should not blindly trust:

```http
Content-Type: text/html
```

because servers frequently mislabel resources.

The routing hierarchy should be approximately:

```
                    OBSERVATION
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
      HTTP metadata   URL hints       body signals
          │              │              │
          └──────────────┼──────────────┘
                         ▼
                  recognition
```

For example:

```
Content-Type: application/octet-stream
URL: /manual.pdf
Body: %PDF-
```

should still be recognized as PDF.

---

<!-- source: Continue Architecture Planning.md L57717–57760 | turn 35 | version 0.11 -->
## v0.11 — 8. Recognition evidence

The provider should report _why_ it recognized something.

Example:

```JavaScript
{
    providerId: 'pdf',
    confidence: 0.99,

    evidence: [
        {
            kind: 'magic-bytes',
            value: '%PDF-'
        },
        {
            kind: 'url-extension',
            value: '.pdf'
        }
    ]
}
```

This becomes particularly useful for the document-discovery system you've been building.

Instead of merely:

```
manual.pdf
```

the graph can retain:

```
manual.pdf
   │
   ├── discovered from HTML link
   ├── recognized as PDF
   ├── magic bytes confirmed
   └── SHA-256 = ...
```

---

<!-- source: Continue Architecture Planning.md L57762–57796 | turn 35 | version 0.11 -->
## v0.11 — 9. Recognition result contract

A provider should return a structured result rather than directly mutating the knowledge base.

```JavaScript
{
    recognized: true,

    classification: {
        type: 'html',
        confidence: 0.99
    },

    evidence: [
        {
            kind: 'content-type',
            value: 'text/html'
        }
    ],

    discoveries: [
        {
            kind: 'link',
            target: 'https://example.com/docs/manual.pdf',
            confidence: 0.95
        }
    ]
}
```

This preserves the architectural rule:

> **Providers produce facts; the knowledge base owns state.**

---

<!-- source: Continue Architecture Planning.md L57798–57842 | turn 35 | version 0.11 -->
## v0.11 — 10. Why providers should not enqueue candidates

Bad:

```JavaScript
class HtmlProvider {
    recognize(observation) {
        engine.enqueue(url);
    }
}
```

Now the provider knows about:

```
scheduler
knowledge base
candidate lifecycle
policy
```

That destroys the boundary.

Correct:

```
HTML Provider
    │
    ▼
Discovery[]
    │
    ▼
Recognition Runtime
    │
    ▼
Knowledge Base
    │
    ▼
Candidate creation
    │
    ▼
Scheduler
```

---

<!-- source: Continue Architecture Planning.md L57844–57891 | turn 35 | version 0.11 -->
## v0.11 — 11. Recognition Runtime

This suggests another explicit component:

```JavaScript
class RecognitionRuntime {
    constructor(router, database) {
        this.router = router;
        this.database = database;
    }

    recognize(observation) {
        const provider =
            this.router.select(observation);

        if (!provider) {
            return {
                recognized: false,
                reason: 'no-recognizer'
            };
        }

        const result =
            provider.recognize(observation);

        return {
            recognized: true,
            providerId:
                provider.describe().id,
            result
        };
    }
}
```

This runtime is intentionally much smaller than the acquisition runtime.

But it establishes the same architectural principle:

```
Acquisition Runtime
    controls execution

Recognition Runtime
    controls interpretation
```

---

<!-- source: Continue Architecture Planning.md L57899–57905 | turn 35 | version 0.11 -->
### v0.11 — No recognizer

```
application/x-unknown
       ↓
no provider
```

<!-- source: Continue Architecture Planning.md L57907–57913 | turn 35 | version 0.11 -->
### v0.11 — Provider rejected

```
HTML provider
       ↓
not HTML
```

<!-- source: Continue Architecture Planning.md L57915–57921 | turn 35 | version 0.11 -->
### v0.11 — Provider error

```
HTML provider
       ↓
parser exception
```

<!-- source: Continue Architecture Planning.md L57923–57935 | turn 35 | version 0.11 -->
### v0.11 — Successful recognition, zero discoveries

```
HTML
       ↓
recognized
       ↓
0 discoverable targets
```

The last one is **not a failure**.

---

<!-- source: Continue Architecture Planning.md L57937–57989 | turn 35 | version 0.11 -->
## v0.11 — 13. v0.11 state progression

The candidate lifecycle now becomes:

```
DISCOVERED
    ↓
QUEUED
    ↓
CLAIMED
    ↓
PLANNED
    ↓
AUTHORIZED
    ↓
SCHEDULED
    ↓
ACQUIRING
    ↓
OBSERVED
    ↓
RECOGNIZING
    ↓
RECOGNIZED
    ↓
EXPANDING
    ↓
COMPLETED
```

Alternative terminal paths:

```
                    ┌── POLICY_DENIED
                    │
                    ├── CAPABILITY_DENIED
                    │
                    ├── ACQUISITION_UNAVAILABLE
                    │
                    ├── ACQUISITION_FAILED
                    │
                    ├── UNRECOGNIZED
                    │
                    └── CANCELLED
```

This gives us a much more useful diagnostic model than:

```
visited = true
```

---

<!-- source: Continue Architecture Planning.md L57991–58034 | turn 35 | version 0.11 -->
## v0.11 — 14. Multiple recognizers

There is a deeper issue.

Should the router choose **one** recognizer or **all compatible** recognizers?

For v0.11, the answer should be:

> **Primary recognizer + optional secondary recognizers.**

Example:

```
response
 │
 ├── HTML recognizer
 │       └── primary
 │
 ├── URL metadata recognizer
 │       └── secondary
 │
 └── generic URL extractor
         └── secondary
```

Why?

Because recognition can be compositional.

An HTML document may simultaneously contain:

```
canonical URL
OpenGraph URL
JSON-LD
embedded JSON
forms
scripts
links
```

Choosing only one parser can unnecessarily discard evidence.

---

<!-- source: Continue Architecture Planning.md L58036–58066 | turn 35 | version 0.11 -->
## v0.11 — 15. Recognition graph

We therefore get:

```
                         OBSERVATION
                              │
                              ▼
                    ┌──────────────────┐
                    │ RESPONSE ROUTER  │
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
           HTML           Metadata        Generic
         recognizer       recognizer      extractor
              │              │              │
              └──────────────┼──────────────┘
                             ▼
                      DISCOVERY SET
                             │
                             ▼
                       DEDUPLICATION
                             │
                             ▼
                     KNOWLEDGE GRAPH
```

This is closer to a **recognition pipeline** than a single parser.

---

<!-- source: Continue Architecture Planning.md L58068–58127 | turn 35 | version 0.11 -->
## v0.11 — 16. The graph is now explicitly causal

We can represent:

```
Candidate
   │
   │ acquired-by
   ▼
AcquisitionPlan
   │
   │ executed-by
   ▼
AcquisitionProvider
   │
   │ produced
   ▼
Observation
   │
   │ recognized-by
   ▼
RecognitionProvider
   │
   │ emitted
   ▼
Discovery
   │
   │ creates
   ▼
Candidate
```

Example:

```
cand-001
   │
   ▼
plan-001
   │
   ▼
gm-xhr
   │
   ▼
obs-001
   │
   ▼
html-provider
   │
   ├───────────────┐
   ▼               ▼
disc-001        disc-002
   │               │
   ▼               ▼
manual.pdf      /api/status
```

This is the beginning of a real **provenance graph**.

---

<!-- source: Continue Architecture Planning.md L58129–58167 | turn 35 | version 0.11 -->
## v0.11 — 17. v0.11 event ledger

Add:

```
recognition-started
recognition-provider-selected
recognition-provider-rejected
recognition-completed
recognition-failed
recognition-unrecognized

discovery-extraction-started
discovery-extraction-completed
discovery-emitted
```

Example:

```
seq 101 candidate-claimed
seq 102 acquisition-planned
seq 103 provider-selected: gm-xhr
seq 104 request-started
seq 105 request-completed
seq 106 observation-recorded
seq 107 recognition-provider-selected: html
seq 108 recognition-started
seq 109 discovery-emitted: manual.pdf
seq 110 discovery-emitted: /api/status
seq 111 recognition-completed
seq 112 candidate-completed
```

Now an exported scan is no longer merely a URL list.

It is a reproducible **causal record**.

---

<!-- source: Continue Architecture Planning.md L58169–58238 | turn 35 | version 0.11 -->
## v0.11 — 18. The emerging generic algorithm

At this point the original DVB inspiration can be expressed more abstractly.

```
┌────────────────────────────────────────────┐
│             UNKNOWN RESOURCE SPACE         │
└─────────────────────┬──────────────────────┘
                      │
                      ▼
                CANDIDATE GENERATION
                      │
                      ▼
                CANDIDATE QUEUE
                      │
                      ▼
               ACQUISITION PLAN
                      │
                      ▼
                   POLICY
                      │
                      ▼
                 SCHEDULER
                      │
                      ▼
             ACQUISITION RUNTIME
                      │
                      ▼
                OBSERVATION
                      │
                      ▼
              RECOGNITION RUNTIME
                      │
                      ▼
                 DISCOVERY
                      │
                      ▼
             NEW CANDIDATES
                      │
                      └───────────┐
                                  │
                                  ▼
                         CANDIDATE QUEUE
```

The loop is the actual algorithm:

```
Discover
   ↓
Represent
   ↓
Prioritize
   ↓
Plan
   ↓
Authorize
   ↓
Acquire
   ↓
Observe
   ↓
Recognize
   ↓
Expand
   ↓
Repeat
```

---

<!-- source: Continue Architecture Planning.md L65186–65190 | turn 45 | version 0.16 -->
### v0.16 — Recognition

> What did we obtain?

`RecognitionRuntime`
