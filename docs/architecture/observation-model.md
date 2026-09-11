# Observation Model

> **Status:** DESIGNED
>
> **Source:** `Continue Architecture Planning.md`; `Userscript Discovery Prototype.md`
>
> **Purpose:** Observations: what is recorded about a probe, immutability, and how observations feed the search space.

## Contents

- **Observation** — `Userscript Discovery Prototype.md` L1478–1507
- **v0.7 — 3. PerformanceObserver correction** — `Continue Architecture Planning.md` L54213–54268
- **v0.9 — 5. Observation gets provider provenance** — `Continue Architecture Planning.md` L55908–55961
- **v0.16 — 2. Observation ≠ Evidence ≠ Claim** — `Continue Architecture Planning.md` L63590–63592
- **v0.16 — Observation** — `Continue Architecture Planning.md` L63594–63605
- **v0.16 — 20. Observation immutability** — `Continue Architecture Planning.md` L64408–64441
- **v0.19 — Observation** — `Continue Architecture Planning.md` L68239–68250
- **v0.19 — 19.14 Observation Becomes the Historical Bridge** — `Continue Architecture Planning.md` L68866–68902
- **v0.19 — Observation state** — `Continue Architecture Planning.md` L68957–68969
- **v0.19 — Step 3 — Observation** — `Continue Architecture Planning.md` L69333–69339
- **v0.28 — 28.10 Observation convergence** — `Continue Architecture Planning.md` L82108–82155
- **v0.32 — 32.19 Observation recovery** — `Continue Architecture Planning.md` L88472–88499
- **v0.33 — 33.15 Duplicate observations** — `Continue Architecture Planning.md` L89657–89696

## Related Documents

- [System Model](system-model.md)
- [Acquisition Model](../acquisition/acquisition-model.md)
- [Evidence Model](evidence-model.md)
- [Search Space](search-space.md)

---

<!-- source: Userscript Discovery Prototype.md L1478–1507 | turn 11 | version ? -->
### Observation

An observation describes **what the receiver actually saw**:

```
Observation {
    candidate
    signal_present
    signal_strength
    noise_estimate
    occupied_bandwidth?
    carrier_offset?
    synchronization_state
    timestamp
}
```

An observation isn't necessarily a discovery.

For example:

```
signal_present = true
carrier_offset = measurable
transport_stream = unknown
```

is useful information even though nothing has been confirmed.

---

<!-- source: Continue Architecture Planning.md L54213–54268 | turn 27 | version 0.7 -->
## v0.7 — 3. PerformanceObserver correction

The previous architecture had a subtle problem:

```
PerformanceResourceTiming
        ↓
method = GET
        ↓
candidate
```

That is not generally valid.

A performance entry tells us that a resource was loaded, but does not reliably tell us the HTTP method.

v0.7.1 therefore treats:

```
script
link
img
iframe
stylesheet
```

as sufficiently GET-like for discovery purposes, while:

```
fetch
xmlhttprequest
```

remain **evidence only** unless the page bridge reports the actual method.

So:

```
POST /api/order
```

can be recorded as:

```
network evidence
```

without becoming:

```
executable acquisition
```

This is exactly the distinction a generic discovery engine needs.

---

<!-- source: Continue Architecture Planning.md L55908–55961 | turn 31 | version 0.9 -->
## v0.9 — 5. Observation gets provider provenance

The observation model should gain:

```JavaScript
{
    provider: {
        id: 'gm-xhr',
        version: '0.9.0'
    }
}
```

So:

```
Candidate
    │
    ▼
AcquisitionPlan
    │
    ▼
ProviderSelection
    │
    ▼
GM-XHR
    │
    ▼
Observation
```

becomes auditable.

For example:

```JavaScript
{
    candidateId: "cand-91",
    observationId: "obs-33",

    acquisition: {
        planId: "plan-72",
        providerId: "gm-xhr",
        method: "GET"
    },

    http: {
        status: 200,
        contentType: "text/html"
    }
}
```

---

<!-- source: Continue Architecture Planning.md L63590–63592 | turn 45 | version 0.16 -->
## v0.16 — 2. Observation ≠ Evidence ≠ Claim

This distinction is fundamental.

<!-- source: Continue Architecture Planning.md L63594–63605 | turn 45 | version 0.16 -->
### v0.16 — Observation

Something the system directly obtained or measured.

Example:

```
HTTP 200
Content-Type: text/html
body contains:
<a href="/manual.pdf">
```

<!-- source: Continue Architecture Planning.md L64408–64441 | turn 45 | version 0.16 -->
## v0.16 — 20. Observation immutability

An observation should be treated as historical evidence.

Bad:

```
observation.body = newBody
```

Better:

```
Observation 1 → old response
Observation 2 → new response
```

Therefore:

```
Observation
    = historical event
```

not:

```
Observation
    = current resource state
```

This distinction will make later verification and revision analysis much cleaner.

---

<!-- source: Continue Architecture Planning.md L68239–68250 | turn 51 | version 0.19 -->
### v0.19 — Observation

The event in which the engine encountered or acquired something.

```
2026-09-10 18:41
GET /manual.pdf
HTTP 200
artifact hash = abc123
```

---

<!-- source: Continue Architecture Planning.md L68866–68902 | turn 51 | version 0.19 -->
## v0.19 — 19.14 Observation Becomes the Historical Bridge

An observation now connects runtime reality to persistent knowledge.

```
Observation O91
│
├── requested locator
├── final locator
├── HTTP metadata
├── response recognition
├── artifact
└── evidence
```

Graph:

```
Locator
   │
   ▼
Observation
   │
   ├────────► Artifact
   │
   ├────────► Evidence
   │
   └────────► Resource
```

This is much more defensible than:

```
URL → resource.type
```

---

<!-- source: Continue Architecture Planning.md L68957–68969 | turn 51 | version 0.19 -->
### v0.19 — Observation state

```
started
completed
failed
timeout
cancelled
```

Avoid one giant `status`.

---

<!-- source: Continue Architecture Planning.md L69333–69339 | turn 51 | version 0.19 -->
### v0.19 — Step 3 — Observation

```
Observation O1
HTTP 200
Content-Type: application/pdf
```

<!-- source: Continue Architecture Planning.md L82108–82155 | turn 69 | version 0.28 -->
## v0.28 — 28.10 Observation convergence

Suppose two tactics acquire:

```
https://example.org/manual.pdf
```

at nearly the same time.

They may produce:

```
Observation A
Observation B
```

Even if:

```
artifact(A) == artifact(B)
```

the observations should not automatically collapse.

Why?

Because they may differ in:

```
provider
headers
timestamp
authentication context
network path
HTTP status
redirect chain
```

Therefore:

```
Same artifact
    ≠
same observation
```

---

<!-- source: Continue Architecture Planning.md L88472–88499 | turn 79 | version 0.32 -->
## v0.32 — 32.19 Observation recovery

An acquisition can produce an observation before the process crashes.

For example:

```
HTTP response received
      ↓
body hashed
      ↓
observation constructed
      X crash before persistence
```

The artifact may physically exist in temporary memory but not in durable storage.

Therefore:

```
memory observation
      ≠
durable observation
```

Only the latter can participate in durable evidence claims.

---

<!-- source: Continue Architecture Planning.md L89657–89696 | turn 81 | version 0.33 -->
## v0.33 — 33.15 Duplicate observations

Suppose Worker A and Worker B both independently acquire:

```
https://example.com/manual.pdf
```

The system may produce:

```
Observation A
Observation B
```

These should not automatically collapse.

They might differ in:

```
timestamp
headers
redirect chain
provider
response body
network conditions
artifact
```

If the bytes match:

```
Observation A ──┐
                ├──► Artifact X
Observation B ──┘
```

This is exactly the distinction established in v0.28.

---
