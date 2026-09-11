# Observation Model

> **Status:** DESIGNED
>
> **Source:** `Continue Architecture Planning.md`; `Userscript Discovery Prototype.md`
>
> **Purpose:** Observations: what is recorded about a probe, immutability, and how observations feed the search space.

## Source Sections

- **Observation** — `USP-052` — `Userscript Discovery Prototype.md` L1478–1507
- **v0.7 — 3. PerformanceObserver correction** — `CAP-049` — `Continue Architecture Planning.md` L54213–54268
- **v0.9 — 5. Observation gets provider provenance** — `CAP-087` — `Continue Architecture Planning.md` L55908–55961
- **v0.16 — 2. Observation ≠ Evidence ≠ Claim** — `CAP-311` — `Continue Architecture Planning.md` L63590–63592
- **v0.16 — Observation** — `CAP-312` — `Continue Architecture Planning.md` L63594–63605
- **v0.16 — 20. Observation immutability** — `CAP-332` — `Continue Architecture Planning.md` L64408–64441
- **v0.19 — Observation** — `CAP-464` — `Continue Architecture Planning.md` L68239–68250
- **v0.19 — 19.14 Observation Becomes the Historical Bridge** — `CAP-477` — `Continue Architecture Planning.md` L68866–68902
- **v0.19 — Observation state** — `CAP-481` — `Continue Architecture Planning.md` L68957–68969
- **v0.19 — Step 3 — Observation** — `CAP-494` — `Continue Architecture Planning.md` L69333–69339
- **v0.28 — 28.10 Observation convergence** — `CAP-880` — `Continue Architecture Planning.md` L82108–82155
- **v0.32 — 32.19 Observation recovery** — `CAP-1061` — `Continue Architecture Planning.md` L88472–88499
- **v0.33 — 33.15 Duplicate observations** — `CAP-1095` — `Continue Architecture Planning.md` L89657–89696

## Related Documents

- [System Model](system-model.md)
- [Acquisition Model](../acquisition/acquisition-model.md)
- [Evidence Model](evidence-model.md)
- [Search Space](search-space.md)

---

<!-- USP-052 | Userscript Discovery Prototype.md L1478–1507 | turn 11 | version ? -->
### Observation

> **Source sections:** `USP-052`

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

<!-- CAP-049 | Continue Architecture Planning.md L54213–54268 | turn 27 | version 0.7 -->
## v0.7 — 3. PerformanceObserver correction

> **Source sections:** `CAP-049`
>
> **Note:** explicit override

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

<!-- CAP-087 | Continue Architecture Planning.md L55908–55961 | turn 31 | version 0.9 -->
## v0.9 — 5. Observation gets provider provenance

> **Source sections:** `CAP-087`

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

<!-- CAP-311 | Continue Architecture Planning.md L63590–63592 | turn 45 | version 0.16 -->
## v0.16 — 2. Observation ≠ Evidence ≠ Claim

> **Source sections:** `CAP-311`
>
> [DOCUMENTATION REVIEW] Contradiction **C-03** ([Review Notes](../REVIEW-NOTES.md#c-03--))

This distinction is fundamental.

<!-- CAP-312 | Continue Architecture Planning.md L63594–63605 | turn 45 | version 0.16 -->
### v0.16 — Observation

> **Source sections:** `CAP-312`

Something the system directly obtained or measured.

Example:

```
HTTP 200
Content-Type: text/html
body contains:
<a href="/manual.pdf">
```

<!-- CAP-332 | Continue Architecture Planning.md L64408–64441 | turn 45 | version 0.16 -->
## v0.16 — 20. Observation immutability

> **Source sections:** `CAP-332`

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

<!-- CAP-464 | Continue Architecture Planning.md L68239–68250 | turn 51 | version 0.19 -->
### v0.19 — Observation

> **Source sections:** `CAP-464`

The event in which the engine encountered or acquired something.

```
2026-09-10 18:41
GET /manual.pdf
HTTP 200
artifact hash = abc123
```

---

<!-- CAP-477 | Continue Architecture Planning.md L68866–68902 | turn 51 | version 0.19 -->
## v0.19 — 19.14 Observation Becomes the Historical Bridge

> **Source sections:** `CAP-477`

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

<!-- CAP-481 | Continue Architecture Planning.md L68957–68969 | turn 51 | version 0.19 -->
### v0.19 — Observation state

> **Source sections:** `CAP-481`

```
started
completed
failed
timeout
cancelled
```

Avoid one giant `status`.

---

<!-- CAP-494 | Continue Architecture Planning.md L69333–69339 | turn 51 | version 0.19 -->
### v0.19 — Step 3 — Observation

> **Source sections:** `CAP-494`

```
Observation O1
HTTP 200
Content-Type: application/pdf
```

<!-- CAP-880 | Continue Architecture Planning.md L82108–82155 | turn 69 | version 0.28 -->
## v0.28 — 28.10 Observation convergence

> **Source sections:** `CAP-880`

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

<!-- CAP-1061 | Continue Architecture Planning.md L88472–88499 | turn 79 | version 0.32 -->
## v0.32 — 32.19 Observation recovery

> **Source sections:** `CAP-1061`

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

<!-- CAP-1095 | Continue Architecture Planning.md L89657–89696 | turn 81 | version 0.33 -->
## v0.33 — 33.15 Duplicate observations

> **Source sections:** `CAP-1095`

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
