# Candidate Model

> **Status:** DESIGNED
>
> **Source:** `Continue Architecture Planning.md`; `Userscript Discovery Prototype.md`
>
> **Purpose:** Candidates: generation, identity, lifecycle, states, deduplication and candidate budgets.

## Contents

- **2. Candidate generation** — `Userscript Discovery Prototype.md` L146–209
- **6. Deduplication** — `Userscript Discovery Prototype.md` L348–382
- **25. Candidate lifecycle** — `Userscript Discovery Prototype.md` L1147–1206
- **Candidate** — `Userscript Discovery Prototype.md` L1455–1476
- **34. Don't confuse candidate identity with reception identity** — `Userscript Discovery Prototype.md` L1616–1659
- **35. Make deduplication hierarchical** — `Userscript Discovery Prototype.md` L1661–1701
- **36. Treat metadata as a candidate generator** — `Userscript Discovery Prototype.md` L1703–1734
- **v0.13 — 12. Candidate deduplication belongs after normalization** — `Continue Architecture Planning.md` L59996–60033
- **v0.13 — 14. Candidate generation becomes transactional** — `Continue Architecture Planning.md` L60078–60117

## Related Documents

- [System Model](system-model.md)
- [Discovery Model](discovery-model.md)
- [Scheduling](scheduler.md)
- [Candidate Sources](../providers/candidate-sources.md)

---

<!-- source: Userscript Discovery Prototype.md L146–209 | turn 3 | version ? -->
## 2. Candidate generation

Instead of:

```
for frequency:
    try DVB-S
```

define a candidate as a tuple:

```
Candidate = {
    center_frequency,
    bandwidth,
    symbol_rate,
    modulation,
    polarization,
    delivery_system,
    other_parameters
}
```

Some fields can initially be unknown:

```
{
    center_frequency = 650 MHz,
    bandwidth = unknown,
    modulation = unknown
}
```

The scanner progressively resolves those unknowns.

For example, terrestrial scanning might do:

```
frequency
   ↓
energy detection
   ↓
estimate bandwidth
   ↓
try compatible DVB-T/T2 parameters
   ↓
lock
```

while satellite scanning may use:

```
frequency + polarization
        ↓
signal detection
        ↓
symbol-rate estimation
        ↓
DVB-S/S2 synchronization
        ↓
lock
```

---

<!-- source: Userscript Discovery Prototype.md L348–382 | turn 3 | version ? -->
## 6. Deduplication

Multiple observations may describe the same multiplex.

Do not use frequency alone as the identity.

A useful logical identity is approximately:

```
(delivery_system,
 network_id,
 transport_stream_id)
```

with RF parameters retained as attributes.

For example:

```
Multiplex {
    identity:
        network_id = 42
        ts_id      = 17

    reception:
        frequency = ...
        bandwidth = ...
        modulation = ...
        signal     = ...
    }
```

If the same TS is rediscovered at slightly different tuning parameters, merge the observations rather than creating another multiplex.

---

<!-- source: Userscript Discovery Prototype.md L1147–1206 | turn 9 | version ? -->
## 25. Candidate lifecycle

A candidate should have a lifecycle rather than simply existing in a list:

```
GENERATED
    │
    ▼
QUEUED
    │
    ▼
PROBED
    │
    ├───────────────┐
    ▼               ▼
REJECTED         PROMISING
                    │
                    ▼
                 ACQUIRED
                    │
              ┌─────┴─────┐
              ▼           ▼
           CONFIRMED    FAILED
              │
              ▼
          EXPANDED
```

This makes retries and diagnostics straightforward.

For example, a candidate can carry:

```
CandidateState {
    attempts
    last_attempt
    confidence
    best_observation
    status
    parent_candidate
}
```

The `parent_candidate` field is particularly useful because it tells you **why the candidate exists**.

For example:

```
Candidate B
    parent = NIT from Multiplex A
```

versus:

```
Candidate C
    parent = energy peak at 674 MHz
```

---

<!-- source: Userscript Discovery Prototype.md L1455–1476 | turn 11 | version ? -->
### Candidate

A candidate describes **what we intend to test**:

```
Candidate {
    domain
    frequency
    bandwidth?
    symbol_rate?
    modulation?
    polarization?
    delivery_system?
    origin
    priority
    attempt_count
}
```

The `?` fields are important. A blind scanner often starts with incomplete information.

---

<!-- source: Userscript Discovery Prototype.md L1616–1659 | turn 11 | version ? -->
## 34. Don't confuse candidate identity with reception identity

This is subtle but important.

A candidate is an **attempt**:

```
"Try frequency X with parameters Y."
```

A reception is an **observation**:

```
"I received transport stream 123 here."
```

A multiplex is a **logical entity**:

```
"Transport stream 123 belonging to network 7."
```

Therefore:

```
Candidate
   ↓
Observation
   ↓
Reception
   ↓
Logical Multiplex
```

Do not collapse these into one database record.

This becomes important when the same multiplex can be received:

* at different times,
* through different RF paths,
* with different measured signal quality,
* or using different receiver configurations.

---

<!-- source: Userscript Discovery Prototype.md L1661–1701 | turn 11 | version ? -->
## 35. Make deduplication hierarchical

Deduplication can happen at several levels:

```
RF level
    frequency + physical parameters

       ↓

Transport level
    network_id + transport_stream_id

       ↓

Service level
    service_id

       ↓

Observation level
    timestamp + reception context
```

So:

```
same frequency
    ≠ necessarily same multiplex
```

and:

```
same transport stream
    = normally same logical multiplex
```

subject to the semantics of the delivery system and metadata.

---

<!-- source: Userscript Discovery Prototype.md L1703–1734 | turn 11 | version ? -->
## 36. Treat metadata as a candidate generator

This is one of the most powerful pieces of the design.

The parser doesn't merely return metadata:

```
parse(stream) → metadata
```

It also returns possible future work:

```
parse(stream)
    │
    ├── discovered services
    ├── network information
    └── candidate transport streams
```

Conceptually:

```
MetadataProviderResult {
    discoveries[]
    candidate_hints[]
}
```

The scheduler can then decide whether those hints deserve immediate acquisition.

---

<!-- source: Continue Architecture Planning.md L59996–60033 | turn 39 | version 0.13 -->
## v0.13 — 12. Candidate deduplication belongs after normalization

Consider:

```
HTML source
    → /docs/a.pdf

Sitemap source
    → https://example.com/docs/a.pdf

Network source
    → https://example.com/docs/a.pdf?utm=x
```

The flow should be:

```
proposals
    ↓
canonicalization
    ↓
identity
    ↓
deduplication
    ↓
candidate
```

not:

```
source-specific deduplication
```

Otherwise every source implements slightly different identity semantics.

---

<!-- source: Continue Architecture Planning.md L60078–60117 | turn 39 | version 0.13 -->
## v0.13 — 14. Candidate generation becomes transactional

The controller should process each proposal through a pipeline:

```
Proposal
   │
   ▼
Validate
   │
   ▼
Canonicalize
   │
   ▼
Identity
   │
   ▼
Policy
   │
   ▼
Existing candidate?
   │
   ├── yes → merge provenance
   │
   └── no  → create candidate
```

This means discovery is not:

```
"push URL into queue"
```

It is:

```
proposal → normalization → state transition
```

---
