# Providers Overview

> **Status:** CURRENT
>
> **Source:** `Continue Architecture Planning.md`; `Userscript Discovery Prototype.md`
>
> **Purpose:** The provider interface used by the prototype and the separation between provider planes.

## Contents

- **What changed — 2. HTML is no longer special** — `Userscript Discovery Prototype.md` L4756–4784
- **v0.12 — 1. Three independent provider planes** — `Continue Architecture Planning.md` L58361–58416
- **v0.12 — 8. The HTML provider should evolve** — `Continue Architecture Planning.md` L58757–58811
- **base Provider class (v0.7.1)** — code extract from `Continue Architecture Planning.md` L51337–51349

## Related Documents

- [HTML Provider](html.md)
- [JSON Provider](json.md)
- [Text Provider](text.md)
- [Provider Architecture](../architecture/provider-architecture.md)
- [Prototype Overview](../prototype/overview.md)

---

<!-- source: Userscript Discovery Prototype.md L4756–4784 | turn 15 | version ? -->
### What changed — 2. HTML is no longer special

**2. HTML is no longer special.**

The prototype now has a provider interface:

```
Response
   │
   ├── JSON provider
   ├── HTML provider
   └── Text provider
```

Each provider can both **recognize** a response and **expand the search space**.

For example:

```
JSON response
     ↓
JSON provider
     ↓
extract URL-like values
     ↓
new candidates
```

That is much closer to the DVB abstraction: the acquisition layer produces an observation, and a protocol/content-specific provider decides whether that observation is meaningful.

<!-- source: Continue Architecture Planning.md L58361–58416 | turn 37 | version 0.12 -->
## v0.12 — 1. Three independent provider planes

The engine now has:

```
                     DISCOVERY ENGINE
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
 CandidateSource   AcquisitionProvider  RecognitionProvider
          │                │                │
       "find"            "get"          "understand"
          │                │                │
          └───────────────┬┴───────────────┘
                          │
                       GRAPH
```

More precisely:

```
CandidateSource
      │
      ▼
Candidate
      │
      ▼
AcquisitionPlan
      │
      ▼
AcquisitionRuntime
      │
      ▼
AcquisitionProvider
      │
      ▼
Observation
      │
      ▼
RecognitionRuntime
      │
      ▼
RecognitionProvider
      │
      ▼
Discovery
      │
      └──────────────► CandidateSource / Candidate
```

The last arrow is the important one:

**recognition creates new candidate material, but does not directly control the scheduler.**

---

<!-- source: Continue Architecture Planning.md L58757–58811 | turn 37 | version 0.12 -->
## v0.12 — 8. The HTML provider should evolve

There is a subtle architectural correction here.

Previously:

```
HtmlProvider
   └── extracts links
```

But now we have:

```
RecognitionProvider
   └── recognizes HTML
```

and:

```
CandidateSource
   └── generates candidates
```

So HTML parsing should conceptually produce **evidence**, which candidate sources consume.

Better:

```
Observation
    │
    ▼
HTML Recognition
    │
    ▼
HTML Evidence
    │
    ├── anchors
    ├── scripts
    ├── stylesheets
    ├── forms
    ├── metadata
    └── embedded URLs
             │
             ▼
       Candidate Sources
             │
             ▼
         Proposals
```

This avoids overloading recognition with discovery.

---

<!-- extracted from Continue Architecture Planning.md L51337–51349 -->
### base Provider class (v0.7.1)

Extracted verbatim from `Continue Architecture Planning.md` lines 51337–51349. The complete script is preserved in [prototype/versions/14-v0.7.1.md](../prototype/versions/14-v0.7.1.md).

```
    class Provider {
        constructor(name) {
            this.name = name;
        }

        matches() {
            return false;
        }

        async recognize() {
            return [];
        }
    }
```
