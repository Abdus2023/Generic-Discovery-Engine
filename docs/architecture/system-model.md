# System Model

> **Status:** DESIGNED
>
> **Source:** `Continue Architecture Planning.md`; `Userscript Discovery Prototype.md`
>
> **Purpose:** Complete system-architecture snapshots, the core object model, data stores and event-driven structure.

## Source Sections

- **14. Discovery database** — `USP-023` — `Userscript Discovery Prototype.md` L678–737
- *Turn lead-in* — `USP-049` — `Userscript Discovery Prototype.md` L1441–1441
- **31. Define the core objects** — `USP-050` — `Userscript Discovery Prototype.md` L1443–1453
- **40. The engine can now become event-driven** — `USP-063` — `Userscript Discovery Prototype.md` L1831–1875
- **v0.7 — 7. Architecture after v0.7.1** — `CAP-053` — `Continue Architecture Planning.md` L54473–54580
- **v0.9 — 0.9 architecture** — `CAP-081` — `Continue Architecture Planning.md` L55641–55697
- **v0.10 — 1. The new architecture** — `CAP-107` — `Continue Architecture Planning.md` L56368–56432
- **v0.10 — 17. The resulting architecture** — `CAP-125` — `Continue Architecture Planning.md` L57181–57233
- **v0.11 — 1. v0.11 architecture** — `CAP-130` — `Continue Architecture Planning.md` L57368–57442
- **v0.12 — 19. The complete v0.12 architecture** — `CAP-186` — `Continue Architecture Planning.md` L59267–59354
- **v0.13 — 1. The complete v0.13 architecture** — `CAP-191` — `Continue Architecture Planning.md` L59495–59546
- **v0.13 — 21. The architecture is now approaching a stable core** — `CAP-220` — `Continue Architecture Planning.md` L60394–60484
- **v0.14 — 22. The complete v0.14 architecture** — `CAP-256` — `Continue Architecture Planning.md` L61697–61772
- **v0.15 — 33. The resulting architecture** — `CAP-306` — `Continue Architecture Planning.md` L63390–63430
- **v0.16 — 33. v0.16 architecture** — `CAP-345` — `Continue Architecture Planning.md` L64931–64989
- **v0.17 — 31. The new architecture** — `CAP-416` — `Continue Architecture Planning.md` L66503–66560
- **v0.18 — 18.21 End-to-End Architecture** — `CAP-445` — `Continue Architecture Planning.md` L67868–67937
- **v0.20 — 20.30 The Architecture After v0.20** — `CAP-556` — `Continue Architecture Planning.md` L71028–71072
- **v0.21 — 21.30 Architecture After v0.21** — `CAP-597` — `Continue Architecture Planning.md` L72513–72578
- **v0.22 — 22.25 v0.22 architecture** — `CAP-636` — `Continue Architecture Planning.md` L73937–73996
- **v0.23 — 23.22 Architecture after v0.23** — `CAP-662` — `Continue Architecture Planning.md` L75101–75167
- **v0.24 — 24.30 New architecture** — `CAP-711` — `Continue Architecture Planning.md` L76763–76828
- **v0.24 — 24.31 The architecture's semantic layers** — `CAP-712` — `Continue Architecture Planning.md` L76830–76874
- **v0.25 — 25.31 v0.25 complete architecture** — `CAP-758` — `Continue Architecture Planning.md` L78350–78413
- **v0.26 — 26.24 v0.26 architecture** — `CAP-793` — `Continue Architecture Planning.md` L79784–79852
- **v0.27 — 27.29 Full v0.27 architecture** — `CAP-852` — `Continue Architecture Planning.md` L81427–81495
- **v0.28 — 28.33 v0.28 architecture** — `CAP-917` — `Continue Architecture Planning.md` L83059–83128
- **v0.29 — 29.30 Dynamic expansion architecture** — `CAP-951` — `Continue Architecture Planning.md` L84369–84399
- **v0.30 — Final architecture** — `CAP-979` — `Continue Architecture Planning.md` L84950–85022
- **v0.30 — 30.1 The new architecture** — `CAP-984` — `Continue Architecture Planning.md` L85171–85213
- **v0.30 — 30.23 Full v0.30 architecture** — `CAP-1008` — `Continue Architecture Planning.md` L86220–86280
- **v0.31 — 31.23 Unified v0.31 architecture** — `CAP-1037` — `Continue Architecture Planning.md` L87538–87598
- **v0.32 — 32.31 v0.32 architecture** — `CAP-1073` — `Continue Architecture Planning.md` L88846–88895
- **v0.33 — 33.32 v0.33 architecture** — `CAP-1112` — `Continue Architecture Planning.md` L90180–90225
- **v0.34 — 34.1 New Architecture Boundary** — `CAP-1119` — `Continue Architecture Planning.md` L90448–90498
- **v0.34 — Final architecture by responsibility** — `CAP-1169` — `Continue Architecture Planning.md` L92158–92188

## Related Documents

- [Architecture Overview](overview.md)
- [Candidate Model](candidate-model.md)
- [Observation Model](observation-model.md)
- [Discovery Model](discovery-model.md)

---

<!-- USP-023 | Userscript Discovery Prototype.md L678–737 | turn 5 | version ? -->
## 14. Discovery database

> **Source sections:** `USP-023`
>
> [DOCUMENTATION REVIEW] Contradiction **C-10** ([Review Notes](../REVIEW-NOTES.md#c-10--knowledge-store-naming))

The final output should ideally not be "a list of frequencies."

Instead:

```
Network
 ├── Transport Stream
 │    ├── Reception parameters
 │    ├── Physical parameters
 │    └── Services
 │         ├── Service
 │         ├── Service
 │         └── Service
 │
 └── Other Transport Streams
```

That distinction is important because:

```
RF observation
```

and

```
logical DVB network
```

are different concepts.

A database might therefore contain:

```
Network {
    network_id
    name
    transport_streams[]
}

TransportStream {
    ts_id
    reception[]
    services[]
}

Reception {
    frequency
    bandwidth
    polarization
    symbol_rate
    modulation
    delivery_system
    quality_metrics
}
```

---

<!-- USP-049 | Userscript Discovery Prototype.md L1441–1441 | turn 11 | ChatGPT turn lead-in -->
> **Source sections:** `USP-049`
>
> **Note:** lead-in of the following section

Yes. The next layer is to make the abstraction **implementable without coupling the discovery engine to DVB hardware**.

<!-- USP-050 | Userscript Discovery Prototype.md L1443–1453 | turn 11 | version ? -->
## 31. Define the core objects

> **Source sections:** `USP-050`

A clean model has five primary objects:

```
Candidate
Observation
LockResult
Discovery
Evidence
```

<!-- USP-063 | Userscript Discovery Prototype.md L1831–1875 | turn 11 | version ? -->
## 40. The engine can now become event-driven

> **Source sections:** `USP-063`

Instead of one enormous synchronous scan:

```
scan()
```

use events:

```
CandidateCreated
CandidateStarted
SignalDetected
AcquisitionLocked
StreamValidated
DiscoveryCreated
CandidateExpanded
CandidateCompleted
```

Then components communicate through events:

```
CandidateCreated
       │
       ▼
 Acquisition
       │
       ▼
ObservationCreated
       │
       ▼
Validator
       │
       ▼
DiscoveryCreated
       │
       ▼
CandidateCreated
```

This makes the system easier to parallelize, log, test, and monitor.

---

<!-- CAP-053 | Continue Architecture Planning.md L54473–54580 | turn 27 | version 0.7 -->
## v0.7 — 7. Architecture after v0.7.1

> **Source sections:** `CAP-053`

```
                 ┌──────────────────────┐
                 │      SOURCES         │
                 │ DOM / HTML / Network │
                 │ JSON / XML / CSS     │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │      DISCOVERY       │
                 │                      │
                 │ URL + type + hints   │
                 │ confidence           │
                 │ provenance           │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   KNOWLEDGE GRAPH    │
                 │                      │
                 │ candidates           │
                 │ resources            │
                 │ observations         │
                 │ edges                │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   ACQUISITION POLICY │
                 │                      │
                 │ method               │
                 │ scope                │
                 │ type                 │
                 │ depth                │
                 │ capabilities         │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │  ACQUISITION PLAN    │
                 │                      │
                 │ allowed              │
                 │ reason               │
                 │ priority             │
                 │ policyVersion        │
                 │ expectedType         │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │      SCHEDULER       │
                 │                      │
                 │ priority             │
                 │ budget               │
                 │ concurrency          │
                 │ origin limits        │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │     ACQUISITION      │
                 │                      │
                 │ GET only             │
                 │ timeout              │
                 │ origin control       │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │     OBSERVATION      │
                 │                      │
                 │ status               │
                 │ headers              │
                 │ body                 │
                 │ fingerprint          │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │     PROVIDERS        │
                 │                      │
                 │ HTML JSON XML CSS JS │
                 └──────────┬───────────┘
                            │
                            └──────────────► DISCOVERY
```

With the new cross-cutting layer:

```
       ┌──────────────────────────────────────────┐
       │          DETERMINISTIC LEDGER            │
       │                                          │
       │ discovery                                │
       │ claim                                    │
       │ plan                                     │
       │ policy decision                          │
       │ budget decision                           │
       │ request lifecycle                         │
       │ observation                               │
       │ recognition                              │
       │ expansion                                │
       │ retry                                    │
       │ completion                               │
       └──────────────────────────────────────────┘
```

<!-- CAP-081 | Continue Architecture Planning.md L55641–55697 | turn 31 | version 0.9 -->
### v0.9 — 0.9 architecture

> **Source sections:** `CAP-081`

```
                         ┌─────────────────────┐
                         │     DISCOVERY       │
                         │ links / HTML / JSON │
                         │ network / metadata  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      CANDIDATE      │
                         │ target + type +     │
                         │ requirements        │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   ACQUISITION PLAN  │
                         │ method              │
                         │ capabilities       │
                         │ policy decision     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ CAPABILITY RESOLVER │
                         └──────────┬──────────┘
                                    │
                                    ▼
                    ┌──────────────────────────────┐
                    │     PROVIDER REGISTRY        │
                    └──────────────┬───────────────┘
                                   │
                  ┌────────────────┼────────────────┐
                  ▼                ▼                ▼
          ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
          │   GM-XHR    │  │    Fetch    │  │   Browser   │
          │   Provider  │  │   Provider  │  │   Provider  │
          └──────┬──────┘  └──────┬──────┘  └──────┬──────┘
                 │                │                │
                 └────────────────┼────────────────┘
                                  ▼
                         ┌─────────────────────┐
                         │      OBSERVATION    │
                         │ status/body/type    │
                         │ final URL/errors    │
                         │ provider metadata   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     PROVIDERS       │
                         │ HTML / JSON / XML   │
                         │ CSS / JS / text...  │
                         └─────────────────────┘
```

<!-- CAP-107 | Continue Architecture Planning.md L56368–56432 | turn 33 | version 0.10 -->
## v0.10 — 1. The new architecture

> **Source sections:** `CAP-107`

```
                         CANDIDATE
                            │
                            ▼
                    ┌───────────────┐
                    │ ACQUISITION   │
                    │     PLAN      │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │    POLICY     │
                    │ authorized?   │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │   SCHEDULER   │
                    │ when?         │
                    └───────┬───────┘
                            │
                            ▼
              ┌─────────────────────────────┐
              │     ACQUISITION RUNTIME     │
              │                             │
              │  budget                     │
              │  concurrency                │
              │  origin limits              │
              │  timeout                    │
              │  retry                      │
              │  cancellation               │
              │  admission                  │
              └──────────────┬──────────────┘
                             │
                             ▼
                    ┌────────────────┐
                    │    PROVIDER    │
                    │                │
                    │ GM-XHR / Fetch│
                    │ Browser / ... │
                    └───────┬────────┘
                            │
                            ▼
                       OBSERVATION
                            │
                            ▼
                       RECOGNITION
                            │
                            ▼
                       DISCOVERY
```

This gives five distinct responsibilities:

| Layer | Question |
| --- | --- |
| Discovery | **What exists?** |
| Policy | **May we acquire it?** |
| Scheduler | **When should we try?** |
| Runtime | **Under what execution controls?** |
| Provider | **How do we perform it?** |

---

<!-- CAP-125 | Continue Architecture Planning.md L57181–57233 | turn 33 | version 0.10 -->
## v0.10 — 17. The resulting architecture

> **Source sections:** `CAP-125`

```
                    ┌─────────────────────┐
                    │      DISCOVERY      │
                    └──────────┬──────────┘
                               ▼
                    ┌─────────────────────┐
                    │    KNOWLEDGE BASE   │
                    └──────────┬──────────┘
                               ▼
                    ┌─────────────────────┐
                    │     SCHEDULER       │
                    │ candidate ordering  │
                    └──────────┬──────────┘
                               ▼
                    ┌─────────────────────┐
                    │  ACQUISITION PLAN   │
                    └──────────┬──────────┘
                               ▼
                    ┌─────────────────────┐
                    │       POLICY        │
                    └──────────┬──────────┘
                               ▼
                    ┌─────────────────────┐
                    │ ACQUISITION RUNTIME │
                    │                     │
                    │ budget              │
                    │ concurrency         │
                    │ origin limits       │
                    │ timeout             │
                    │ retry               │
                    │ cancellation        │
                    └──────────┬──────────┘
                               ▼
                    ┌─────────────────────┐
                    │ PROVIDER REGISTRY   │
                    └──────────┬──────────┘
                               ▼
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
           GM-XHR            Fetch           Browser
              │                │                │
              └────────────────┼────────────────┘
                               ▼
                         OBSERVATION
                               ▼
                         RECOGNITION
                               ▼
                          DISCOVERY
                               │
                               └──────→ KB
```

<!-- CAP-130 | Continue Architecture Planning.md L57368–57442 | turn 35 | version 0.11 -->
## v0.11 — 1. v0.11 architecture

> **Source sections:** `CAP-130`

```
                         CANDIDATE
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
                  ACQUISITION PROVIDER
                            │
                            ▼
                       OBSERVATION
                            │
                            ▼
                 ┌─────────────────────┐
                 │ RESPONSE ROUTER     │
                 └──────────┬──────────┘
                            │
          ┌─────────────────┼─────────────────┐
          ▼                 ▼                 ▼
       HTML                JSON               XML
          │                 │                 │
          ▼                 ▼                 ▼
     HTML Provider     JSON Provider      XML Provider
          │                 │                 │
          └─────────────────┼─────────────────┘
                            ▼
                       DISCOVERIES
                            │
                            ▼
                     KNOWLEDGE BASE
                            │
                            ▼
                        CANDIDATES
```

The engine now has two independent provider planes:

```
ACQUISITION PLANE

Plan
 ↓
Runtime
 ↓
AcquisitionProvider
 ↓
Observation
```

and:

```
RECOGNITION PLANE

Observation
 ↓
ResponseRouter
 ↓
RecognitionProvider
 ↓
Discovery
```

---

<!-- CAP-186 | Continue Architecture Planning.md L59267–59354 | turn 37 | version 0.12 -->
## v0.12 — 19. The complete v0.12 architecture

> **Source sections:** `CAP-186`

```
                         ┌──────────────────────┐
                         │    SEARCH SPACES     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │  CANDIDATE SOURCES   │
                         │                      │
                         │ HTML                 │
                         │ Network              │
                         │ Metadata             │
                         │ Sitemap              │
                         │ Robots               │
                         │ User Seed            │
                         │ Mutation             │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      PROPOSALS       │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    NORMALIZATION     │
                         │ canonicalization     │
                         │ identity             │
                         │ URL policy           │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      CANDIDATES      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      SCHEDULER       │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   ACQUISITION PLAN   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │        POLICY        │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ ACQUISITION RUNTIME  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ ACQUISITION PROVIDER │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     OBSERVATION      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ RECOGNITION RUNTIME  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ RECOGNITION PROVIDER │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │       EVIDENCE       │
                         └──────────┬───────────┘
                                    │
                                    └──────────────►
                                      Candidate Sources
```

---

<!-- CAP-191 | Continue Architecture Planning.md L59495–59546 | turn 39 | version 0.13 -->
## v0.13 — 1. The complete v0.13 architecture

> **Source sections:** `CAP-191`

```
                         DISCOVERY CONTROLLER
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
              ▼                   ▼                   ▼
        Source Policy       Source Scheduler     Source Budget
              │                   │                   │
              └───────────────────┼───────────────────┘
                                  │
                                  ▼
                         CandidateSource
                                  │
                                  ▼
                             Proposals
                                  │
                                  ▼
                        CandidateNormalizer
                                  │
                                  ▼
                             Candidates
                                  │
                                  ▼
                           Main Scheduler
                                  │
                                  ▼
                        Acquisition Runtime
                                  │
                                  ▼
                       Acquisition Provider
                                  │
                                  ▼
                            Observation
                                  │
                                  ▼
                       Recognition Runtime
                                  │
                                  ▼
                      Recognition Provider
                                  │
                                  ▼
                              Evidence
                                  │
                                  ▼
                         Discovery Controller
```

The controller closes the discovery loop.

---

<!-- CAP-220 | Continue Architecture Planning.md L60394–60484 | turn 39 | version 0.13 -->
## v0.13 — 21. The architecture is now approaching a stable core

> **Source sections:** `CAP-220`

```
                     ┌──────────────────┐
                     │ SEARCH SPACES    │
                     └────────┬─────────┘
                              ▼
                     Candidate Sources
                              │
                              ▼
                    Discovery Controller
                              │
                              ▼
                         Proposals
                              │
                              ▼
                       Normalization
                              │
                              ▼
                         Candidates
                              │
                              ▼
                         Scheduler
                              │
                              ▼
                    Acquisition Planning
                              │
                              ▼
                           Policy
                              │
                              ▼
                    Acquisition Runtime
                              │
                              ▼
                    Acquisition Provider
                              │
                              ▼
                         Observation
                              │
                              ▼
                    Recognition Runtime
                              │
                              ▼
                   Recognition Providers
                              │
                              ▼
                          Evidence
                              │
                              └─────────────┐
                                            ▼
                                   Discovery Controller
```

There is now a clean division of labor:

```
CandidateSource
    FIND

DiscoveryController
    GOVERN DISCOVERY

CandidateNormalizer
    DEFINE IDENTITY

Scheduler
    ORDER WORK

Policy
    AUTHORIZE

AcquisitionRuntime
    CONTROL EXECUTION

AcquisitionProvider
    PERFORM I/O

Observation
    RECORD WHAT HAPPENED

RecognitionRuntime
    ROUTE INTERPRETATION

RecognitionProvider
    INTERPRET

Evidence
    SUPPORT CLAIMS
```

---

<!-- CAP-256 | Continue Architecture Planning.md L61697–61772 | turn 41 | version 0.14 -->
## v0.14 — 22. The complete v0.14 architecture

> **Source sections:** `CAP-256`

We can now assemble the system:

```
                         ┌───────────────────────┐
                         │   DISCOVERY DOMAIN    │
                         │                       │
                         │ schemes               │
                         │ origins               │
                         │ resource types        │
                         │ seeds                 │
                         │ source set             │
                         │ budgets               │
                         │ termination            │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │     SCAN SESSION      │
                         │                       │
                         │ lifecycle             │
                         │ counters              │
                         │ frontier              │
                         │ snapshot              │
                         │ cancellation          │
                         │ termination           │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │ DISCOVERY CONTROLLER   │
                         └───────────┬───────────┘
                                     │
                         ┌───────────┴───────────┐
                         ▼                       ▼
                Discovery Scheduler       Discovery Sources
                         │                       │
                         └───────────┬───────────┘
                                     ▼
                               PROPOSALS
                                     │
                                     ▼
                             NORMALIZATION
                                     │
                                     ▼
                               CANDIDATES
                                     │
                                     ▼
                           ACQUISITION SCHEDULER
                                     │
                                     ▼
                           ACQUISITION RUNTIME
                                     │
                                     ▼
                           ACQUISITION PROVIDER
                                     │
                                     ▼
                              OBSERVATION
                                     │
                                     ▼
                         RECOGNITION RUNTIME
                                     │
                                     ▼
                               EVIDENCE
                                     │
                                     ▼
                         DISCOVERY CONTROLLER
                                     │
                                     └──────────────┐
                                                    │
                                                    ▼
                                               NEW FRONTIER
```

---

<!-- CAP-306 | Continue Architecture Planning.md L63390–63430 | turn 43 | version 0.15 -->
## v0.15 — 33. The resulting architecture

> **Source sections:** `CAP-306`

```
                         DISCOVERY DOMAIN
                                │
                                ▼
                         SCAN SESSION
                                │
                                ▼
                      ┌──────────────────┐
                      │ FRONTIER RUNTIME │
                      └────────┬─────────┘
                               │
                         WORK SCHEDULER
                               │
                  ┌────────────┴────────────┐
                  │                         │
                  ▼                         ▼
           DISCOVERY WORK             ACQUISITION WORK
                  │                         │
                  ▼                         ▼
        DISCOVERY CONTROLLER       ACQUISITION RUNTIME
                  │                         │
                  ▼                         ▼
         CANDIDATE SOURCES         ACQUISITION PROVIDERS
                  │                         │
                  ▼                         ▼
             PROPOSALS                 OBSERVATIONS
                  │                         │
                  ▼                         ▼
            CANDIDATES             RECOGNITION RUNTIME
                  │                         │
                  └──────────┬──────────────┘
                             ▼
                       KNOWLEDGE BASE
                             │
                             ▼
                        EVENT LEDGER
```

---

<!-- CAP-345 | Continue Architecture Planning.md L64931–64989 | turn 45 | version 0.16 -->
## v0.16 — 33. v0.16 architecture

> **Source sections:** `CAP-345`

The full system becomes:

```
                         DISCOVERY DOMAIN
                                │
                                ▼
                          SCAN SESSION
                                │
                                ▼
                        FRONTIER RUNTIME
                                │
                                ▼
                            WORK ITEM
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
              DISCOVERY WORK         ACQUISITION WORK
                    │                       │
                    ▼                       ▼
          DISCOVERY CONTROLLER      ACQUISITION RUNTIME
                    │                       │
                    ▼                       ▼
             CANDIDATE SOURCE        ACQUISITION PROVIDER
                    │                       │
                    ▼                       ▼
               PROPOSAL                 OBSERVATION
                    │                       │
                    ▼                       ▼
               CANDIDATE           RECOGNITION RUNTIME
                    │                       │
                    └──────────┬────────────┘
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
                        KNOWLEDGE GRAPH
```

Cross-cutting:

```
EVENT LEDGER
      │
      ├── Work lifecycle
      ├── Acquisition
      ├── Recognition
      ├── Discovery
      └── Evidence production
```

---

<!-- CAP-416 | Continue Architecture Planning.md L66503–66560 | turn 47 | version 0.17 -->
## v0.17 — 31. The new architecture

> **Source sections:** `CAP-416`

The complete system is now:

```
                         DISCOVERY DOMAIN
                                │
                                ▼
                          SCAN SESSION
                                │
                                ▼
                        FRONTIER RUNTIME
                                │
                                ▼
                             WORK
                                │
                ┌───────────────┴───────────────┐
                ▼                               ▼
          DISCOVERY WORK                  ACQUISITION WORK
                │                               │
                ▼                               ▼
       DISCOVERY CONTROLLER            ACQUISITION RUNTIME
                │                               │
                ▼                               ▼
       CANDIDATE SOURCE                 ACQUISITION PROVIDER
                │                               │
                ▼                               ▼
             PROPOSAL                     OBSERVATION
                │                               │
                ▼                               ▼
           NORMALIZATION                RECOGNITION RUNTIME
                │                               │
                ▼                               ▼
           CANDIDATE                       EVIDENCE
                │                               │
                └──────────────┬────────────────┘
                               ▼
                             CLAIM
                               │
                               ▼
                         IDENTITY RESOLUTION
                               │
                               ▼
                         RESOURCE GRAPH
                               │
                ┌──────────────┼───────────────┐
                ▼              ▼               ▼
             Locators      Relations       Revisions
                               │
                               ▼
                         KNOWLEDGE BASE

                 EVENT LEDGER
                      │
                      └── records every transition
```

---

<!-- CAP-445 | Continue Architecture Planning.md L67868–67937 | turn 49 | version 0.18 -->
## v0.18 — 18.21 End-to-End Architecture

> **Source sections:** `CAP-445`

At this point the engine becomes:

```
                         SCAN SESSION
                              │
                              ▼
                       DISCOVERY DOMAIN
                              │
                              ▼
                       FRONTIER RUNTIME
                              │
                 ┌────────────┴────────────┐
                 ▼                         ▼
          Discovery Work            Acquisition Work
                 │                         │
                 ▼                         ▼
       Candidate Sources           Acquisition Runtime
                 │                         │
                 ▼                         ▼
            Candidate                 Observation
                 │                         │
                 └────────────┬────────────┘
                              ▼
                         EVIDENCE GRAPH
                              │
                              ▼
                     RESPONSE RECOGNITION
                              │
                              ▼
                           RESOURCE
                              │
                              ▼
                   IDENTITY RESOLUTION
                              │
                              ▼
                  CLASSIFICATION RUNTIME
                              │
               ┌──────────────┼──────────────┐
               ▼              ▼              ▼
          Representation   Behavior      Semantic Role
               │              │              │
               └──────────────┼──────────────┘
                              ▼
                     Strategy Resolution
                              │
                              ▼
                       New WorkItems
```

The important property is the feedback loop:

```
Resource
   ↓
Classification
   ↓
Strategy
   ↓
New Work
   ↓
Observation
   ↓
Evidence
   ↓
Updated Resource knowledge
```

---

<!-- CAP-556 | Continue Architecture Planning.md L71028–71072 | turn 53 | version 0.20 -->
## v0.20 — 20.30 The Architecture After v0.20

> **Source sections:** `CAP-556`

The engine now has a much stronger separation:

```
                     DISCOVERY DOMAIN
                            │
                            ▼
                       SEARCH SPACE
                            │
                    ┌───────┴───────┐
                    ▼               ▼
               PARTITION A      PARTITION B
                    │               │
                    └───────┬───────┘
                            ▼
                    STRATEGY CONTROLLER
                            │
                            ▼
                    EXPLORATION PLAN
                            │
                            ▼
                     FRONTIER RUNTIME
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
        Discovery       Acquisition    Classification
          Work             Work            Work
             │              │              │
             ▼              ▼              ▼
        Candidates      Observations     Assertions
             │              │              │
             └──────────────┼──────────────┘
                            ▼
                       KNOWLEDGE GRAPH
                            │
                 ┌──────────┼──────────┐
                 ▼          ▼          ▼
             Resource    Artifact    Evidence
                 │
                 ▼
            Revision History
```

---

<!-- CAP-597 | Continue Architecture Planning.md L72513–72578 | turn 55 | version 0.21 -->
## v0.21 — 21.30 Architecture After v0.21

> **Source sections:** `CAP-597`

The complete control plane is becoming:

```
                         SCAN SESSION
                              │
                              ▼
                       DISCOVERY DOMAIN
                              │
                              ▼
                         SEARCH SPACE
                              │
                              ▼
                         PARTITIONS
                              │
                              ▼
                  ADAPTIVE STRATEGY CONTROLLER
                              │
              ┌───────────────┼────────────────┐
              ▼               ▼                ▼
         Eligibility      Performance       Exploration
            Policy          History            Quota
              │               │                │
              └───────────────┼────────────────┘
                              ▼
                       STRATEGY DECISION
                              │
                              ▼
                      EXPLORATION PLAN
                              │
                              ▼
                       FRONTIER RUNTIME
                              │
              ┌───────────────┼────────────────┐
              ▼               ▼                ▼
         Discovery        Acquisition      Classification
           Work              Work              Work
              │               │                │
              ▼               ▼                ▼
         Candidates       Observations      Assertions
              │               │                │
              └───────────────┼────────────────┘
                              ▼
                        KNOWLEDGE GRAPH
                              │
                 ┌────────────┼────────────┐
                 ▼            ▼            ▼
              Resource      Artifact     Evidence
                 │
                 ▼
             Revisions
                 │
                 ▼
          Search-space expansion
                 │
                 └──────────────► New Partitions
```

The engine now has the beginnings of an **adaptive blind-discovery system**.

Not an autonomous crawler that invents its own permissions.

A bounded search system that can optimize **where and how it explores inside an explicitly defined universe**.

---

<!-- CAP-636 | Continue Architecture Planning.md L73937–73996 | turn 57 | version 0.22 -->
## v0.22 — 22.25 v0.22 architecture

> **Source sections:** `CAP-636`

The complete engine now looks like:

```
                         DISCOVERY DOMAIN
                                │
                                ▼
                         SEARCH SPACE
                                │
                                ▼
                     SEARCH SPACE SNAPSHOT
                                │
                                ▼
                         PARTITIONS
                                │
                                ▼
                  ADAPTIVE STRATEGY SELECTOR
                                │
                                ▼
                         EXPLORATION PLAN
                                │
                                ▼
                        FRONTIER RUNTIME
                                │
                                ▼
                           PROBE
                                │
                                ▼
                         ACQUISITION
                                │
                                ▼
                         OBSERVATION
                                │
                                ▼
                      RECOGNITION RUNTIME
                                │
                                ▼
                            EVIDENCE
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
                 RESOURCE             COVERAGE
                    │                       │
                    ▼                       ▼
             CLASSIFICATION          COMPLETENESS
```

Cross-cutting:

```
                ┌────────────────────────────┐
                │        EVENT LEDGER        │
                │                            │
                │ execution / decisions /   │
                │ failures / transitions    │
                └────────────────────────────┘
```

---

<!-- CAP-662 | Continue Architecture Planning.md L75101–75167 | turn 59 | version 0.23 -->
## v0.23 — 23.22 Architecture after v0.23

> **Source sections:** `CAP-662`

```
                         SEARCH DOMAIN
                              │
                              ▼
                         SEARCH SPACE
                              │
                              ▼
                       COVERAGE MODEL
                              │
             ┌────────────────┼────────────────┐
             │                │                │
         EXPLORED         UNEXPLORED      INACCESSIBLE
             │
             ▼
        DISCOVERY
             │
             ▼
       ACQUISITION
             │
             ▼
        OBSERVATION
             │
             ▼
          EVIDENCE
             │
      ┌──────┴──────┐
      │             │
 POSITIVE       NEGATIVE
 EVIDENCE       EVIDENCE
      │             │
      ▼             ▼
 PRESENCE        ABSENCE
  CLAIM           CLAIM
      │             │
      └──────┬──────┘
             ▼
       CLAIM GRAPH
             │
      ┌──────┴──────┐
      │             │
   SUPPORTS      CONTRADICTS
      │             │
      └──────┬──────┘
             ▼
       ASSURANCE LAYER
             │
             ▼
       COMPLETENESS
```

And independently:

```
EVENT LEDGER
     │
     ├── decisions
     ├── work transitions
     ├── acquisitions
     ├── observations
     ├── failures
     ├── coverage changes
     └── claim assessments
```

---

<!-- CAP-711 | Continue Architecture Planning.md L76763–76828 | turn 61 | version 0.24 -->
## v0.24 — 24.30 New architecture

> **Source sections:** `CAP-711`

The complete architecture now becomes:

```
                         SEARCH GOAL
                              │
                    ┌─────────┴─────────┐
                    │                   │
              Constraints          Preferences
                    │                   │
                    └─────────┬─────────┘
                              │
                              ▼
                     RELEVANCE MODEL
                              │
                              ▼
                         SEARCH DOMAIN
                              │
                              ▼
                         SEARCH SPACE
                              │
                              ▼
                  RELEVANT SEARCH SPACE
                              │
                              ▼
                         PARTITIONS
                              │
                              ▼
                   ADAPTIVE STRATEGIES
                              │
                              ▼
                       FRONTIER RUNTIME
                              │
                              ▼
                         ACQUISITION
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
                          RESOURCE
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
              CLASSIFICATION       RELEVANCE
                    │                   │
                    └─────────┬─────────┘
                              ▼
                         GOAL RESULT
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
                SATISFACTION        COVERAGE
                                        │
                                        ▼
                                  COMPLETENESS
```

---

<!-- CAP-712 | Continue Architecture Planning.md L76830–76874 | turn 61 | version 0.24 -->
## v0.24 — 24.31 The architecture's semantic layers

> **Source sections:** `CAP-712`

At this point, the engine has four distinct reasoning layers:

```
L1 — DISCOVERY
"What could exist?"

L2 — EPISTEMIC
"What evidence do we have?"

L3 — SEMANTIC
"What is this resource?"

L4 — GOAL
"Does it satisfy what we are looking for?"
```

And two assurance layers:

```
L5 — COVERAGE
"What portion did we explore?"

L6 — COMPLETENESS
"What strength of completeness claim is justified?"
```

While the operational plane remains:

```
Domain
 ↓
Policy
 ↓
Capability
 ↓
Scheduler
 ↓
Runtime
```

This is an important architectural separation.

---

<!-- CAP-758 | Continue Architecture Planning.md L78350–78413 | turn 63 | version 0.25 -->
## v0.25 — 25.31 v0.25 complete architecture

> **Source sections:** `CAP-758`

```
                              GOAL
                                │
                                ▼
                         QUERY PLANNER
                                │
                 ┌──────────────┼──────────────┐
                 │              │              │
             Constraints    Expansions      Preferences
                 │              │              │
                 └──────────────┼──────────────┘
                                ▼
                           QUERY PLAN
                                │
                         ┌──────┴──────┐
                         │             │
                    Query Steps    Hypotheses
                         │             │
                         └──────┬──────┘
                                ▼
                         PLAN VALIDATOR
                                │
                  ┌─────────────┼─────────────┐
                  ▼             ▼             ▼
               Domain        Policy       Capability
                  │             │             │
                  └─────────────┼─────────────┘
                                ▼
                         RELEVANT SPACE
                                │
                                ▼
                       ADAPTIVE STRATEGY
                                │
                                ▼
                         FRONTIER RUNTIME
                                │
                                ▼
                           ACQUISITION
                                │
                                ▼
                           OBSERVATION
                                │
                                ▼
                            EVIDENCE
                                │
              ┌─────────────────┼─────────────────┐
              ▼                 ▼                 ▼
          RESOURCE        CLASSIFICATION      COVERAGE
              │                 │                 │
              └─────────────────┼─────────────────┘
                                ▼
                           RELEVANCE
                                │
                                ▼
                           GOAL RESULT
                                │
                       ┌────────┴────────┐
                       ▼                 ▼
                  SATISFACTION      COMPLETENESS
```

---

<!-- CAP-793 | Continue Architecture Planning.md L79784–79852 | turn 65 | version 0.26 -->
## v0.26 — 26.24 v0.26 architecture

> **Source sections:** `CAP-793`

The complete path now becomes:

```
                           SEARCH INTENT
                               │
                               ▼
                              Goal
                               │
                               ▼
                         Query Planner
                               │
                               ▼
                           QueryPlan
                               │
                               ▼
                           QueryStep
                               │
                               ▼
                        TacticExecution
                               │
                               ▼
                       FrontierRuntime
                               │
                         claim / lease
                               │
                               ▼
                         TacticRuntime
                               │
                    ┌──────────┴──────────┐
                    │                     │
                    ▼                     ▼
             SearchTactic          Tactic Budget
                    │
                    ▼
            DiscoveryStrategy
                    │
                    ▼
                 Probe
                    │
                    ▼
             Acquisition Layer
                    │
                    ▼
               Observation
                    │
                    ▼
                Evidence
                    │
                    ▼
          CandidateProposal
                    │
                    ▼
          DiscoveryController
                    │
                    ▼
          CandidateNormalizer
                    │
                    ▼
                Candidate
                    │
                    ▼
             ResourceGraph
```

The key architectural property is that the arrows do not imply authority transfer.

---

<!-- CAP-852 | Continue Architecture Planning.md L81427–81495 | turn 67 | version 0.27 -->
## v0.27 — 27.29 Full v0.27 architecture

> **Source sections:** `CAP-852`

```
                              GOAL
                                │
                                ▼
                         QUERY PLANNER
                                │
                                ▼
                           QUERY PLAN
                                │
                                ▼
                           QUERY STEP
                                │
                                ▼
                       TACTIC EXECUTION
                                │
                                ▼
                        FRONTIER RUNTIME
                                │
                                ▼
                         TACTIC RUNTIME
                                │
                    ┌───────────┴───────────┐
                    │                       │
             ordinary strategy        enumeration
                    │                       │
                    │               ENUMERATION RUNTIME
                    │                       │
                    │                    ENUMERATOR
                    │                       │
                    │                  EnumerationPage
                    │                       │
                    └───────────┬───────────┘
                                │
                        CandidateProposal
                                │
                                ▼
                    DISCOVERY CONTROLLER
                                │
                                ▼
                    CANDIDATE NORMALIZER
                                │
                                ▼
                           CANDIDATE
                                │
                                ▼
                         RESOURCE GRAPH
```

And the evidence path:

```
Enumerator
   ↓
EnumerationPage
   ↓
EnumerationSnapshot
   ↓
TerminationEvidence
   ↓
CoverageRecord
   ↓
CoverageClaim
   ↓
CompletenessAssessment
```

---

<!-- CAP-917 | Continue Architecture Planning.md L83059–83128 | turn 69 | version 0.28 -->
## v0.28 — 28.33 v0.28 architecture

> **Source sections:** `CAP-917`

The engine now looks like:

```
                         GOAL
                           │
                           ▼
                    QUERY PLANNER
                           │
                           ▼
                       QUERY PLAN
                           │
                           ▼
                     TACTIC RUNTIME
                           │
                           ▼
                  ENUMERATION / STRATEGY
                           │
                           ▼
                       FRONTIER
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
      Search-Space Graph           Work Graph
             │                           │
             │                    dedup / lease
             │                           │
             └─────────────┬─────────────┘
                           ▼
                     OBSERVATION
                           │
                           ▼
                        EVIDENCE
                           │
                           ▼
                  CANDIDATE PROPOSAL
                           │
                           ▼
                 CANDIDATE NORMALIZER
                           │
                           ▼
                   IDENTITY RESOLUTION
                           │
                    ┌──────┴──────┐
                    ▼             ▼
              Candidate        Resource
                    │             │
                    └──────┬──────┘
                           ▼
                     Artifact Graph
```

Parallel coverage path:

```
Enumeration
    ↓
Snapshot
    ↓
Coverage Record
    ↓
Coverage Reconciliation
    ↓
Coverage Claim
    ↓
Completeness Assessment
```

---

<!-- CAP-951 | Continue Architecture Planning.md L84369–84399 | turn 71 | version 0.29 -->
## v0.29 — 29.30 Dynamic expansion architecture

> **Source sections:** `CAP-951`

The complete loop becomes:

```
                         OBSERVATION
                              │
                              ▼
                           EVIDENCE
                              │
                 ┌────────────┴────────────┐
                 ▼                         ▼
          CandidateProposal        PartitionProposal
                 │                         │
                 ▼                         ▼
       CandidateNormalizer       PartitionAdmission
                 │                         │
                 ▼                         ▼
             Candidate               SearchPartition
                 │                         │
                 │                         ▼
                 │                  FrontierRuntime
                 │                         │
                 └────────────┬────────────┘
                              ▼
                         NEW WORK
```

This is a major structural symmetry.

---

<!-- CAP-979 | Continue Architecture Planning.md L84950–85022 | turn 73 | version 0.30 -->
## v0.30 — Final architecture

> **Source sections:** `CAP-979`

```
┌───────────────────────────────────────────────────────────┐
│                       SEARCH GOAL                          │
└───────────────────────────┬───────────────────────────────┘
                            ▼
┌───────────────────────────────────────────────────────────┐
│                     QUERY PLANNER                         │
│       plans / tactics / hypotheses / constraints          │
└───────────────────────────┬───────────────────────────────┘
                            ▼
┌───────────────────────────────────────────────────────────┐
│                      SEARCH SPACE                         │
│       domain / partitions / snapshots / relations         │
└───────────────────────────┬───────────────────────────────┘
                            ▼
┌───────────────────────────────────────────────────────────┐
│                    FRONTIER RUNTIME                       │
│       admission / arbitration / fairness / leases         │
└──────────────┬────────────────┬────────────────┬──────────┘
               ▼                ▼                ▼
        DiscoveryWork     AcquisitionWork   EnumerationWork
               │                │                │
               └────────────────┼────────────────┘
                                ▼
                     ┌────────────────────┐
                     │ ACQUISITION POLICY │
                     │ CAPABILITIES       │
                     │ BUDGET             │
                     └─────────┬──────────┘
                               ▼
                     ACQUISITION PROVIDER
                               │
                               ▼
                          OBSERVATION
                               │
                               ▼
                     RECOGNITION RUNTIME
                               │
                ┌──────────────┼──────────────┐
                ▼              ▼              ▼
             Evidence     Classification   Artifact
                │              │              │
                └──────────────┼──────────────┘
                               ▼
                         RESOURCE GRAPH
                               │
                ┌──────────────┼──────────────┐
                ▼              ▼              ▼
            Relevance       Coverage       Absence
                │              │              │
                └──────────────┼──────────────┘
                               ▼
                      COMPLETENESS CLAIMS
```

Cross-cutting:

```
Policy
Capabilities
Budgets
Provenance
Event Ledger
Persistence
Versioning
Cancellation
Recovery
Observability
```

---

<!-- CAP-984 | Continue Architecture Planning.md L85171–85213 | turn 75 | version 0.30 -->
## v0.30 — 30.1 The new architecture

> **Source sections:** `CAP-984`

```
                         FRONTIER
                            │
                            ▼
                  ┌───────────────────┐
                  │ Frontier Arbitrator│
                  └─────────┬─────────┘
                            │
          ┌─────────────────┼──────────────────┐
          ▼                 ▼                  ▼
     admission          arbitration         fairness
          │                 │                  │
          └─────────────────┼──────────────────┘
                            ▼
                    selected WorkItem
                            │
                            ▼
                       EXECUTOR
                            │
                            ▼
                         OUTCOME
                            │
                            ▼
                  frontier state update
```

The critical distinction:

```
Admission
    =
    "May this work execute?"

Arbitration
    =
    "Which admissible work executes next?"
```

Never merge those concepts.

---

<!-- CAP-1008 | Continue Architecture Planning.md L86220–86280 | turn 75 | version 0.30 -->
## v0.30 — 30.23 Full v0.30 architecture

> **Source sections:** `CAP-1008`

```
                         ┌───────────────┐
                         │     GOAL      │
                         └───────┬───────┘
                                 ▼
                         ┌───────────────┐
                         │ QUERY PLAN    │
                         └───────┬───────┘
                                 ▼
                         ┌───────────────┐
                         │ SEARCH SPACE  │
                         └───────┬───────┘
                                 ▼
                    ┌────────────────────────┐
                    │     FRONTIER RUNTIME   │
                    │                        │
                    │ ┌────────────────────┐ │
                    │ │ Admission          │ │
                    │ ├────────────────────┤ │
                    │ │ Dependencies       │ │
                    │ │ Domain             │ │
                    │ │ Capability         │ │
                    │ │ Policy             │ │
                    │ │ Budget             │ │
                    │ │ Backpressure       │ │
                    │ └────────────────────┘ │
                    │                        │
                    │ ┌────────────────────┐ │
                    │ │ Arbitration        │ │
                    │ ├────────────────────┤ │
                    │ │ Class fairness     │ │
                    │ │ Aging              │ │
                    │ │ Goal value         │ │
                    │ │ Coverage value     │ │
                    │ │ Novelty            │ │
                    │ │ Information gain   │ │
                    │ │ Cost               │ │
                    │ │ Failure history    │ │
                    │ └────────────────────┘ │
                    └───────────┬────────────┘
                                ▼
                       ArbitrationDecision
                                │
                                ▼
                           Atomic Claim
                                │
                                ▼
                             Executor
                                │
                                ▼
                             Outcome
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
               Knowledge               Frontier
                 update                  update
```

---

<!-- CAP-1037 | Continue Architecture Planning.md L87538–87598 | turn 77 | version 0.31 -->
## v0.31 — 31.23 Unified v0.31 architecture

> **Source sections:** `CAP-1037`

```
                         SEARCH GOAL
                              │
                              ▼
                        QUERY PLANNER
                              │
                              ▼
                         SEARCH SPACE
                              │
                              ▼
                    ┌───────────────────┐
                    │ FRONTIER RUNTIME  │
                    └─────────┬─────────┘
                              │
                              ▼
                       ADMISSION CONTROL
                              │
                              ▼
                         ARBITRATION
                              │
                              ▼
                    ArbitrationDecision
                              │
                              ▼
                      RESOURCE ALLOCATOR
                              │
                 ┌────────────┼────────────┐
                 ▼            ▼            ▼
              budget       capacity      quotas
                 │            │            │
                 └────────────┼────────────┘
                              ▼
                       RESERVATION
                              │
                              ▼
                           EXECUTE
                              │
                              ▼
                         OBSERVATION
                              │
                              ▼
                       COST OBSERVATION
                              │
                              ▼
                         SETTLEMENT
                              │
                              ▼
                      RESOURCE LEDGER
                              │
                  ┌───────────┴───────────┐
                  ▼                       ▼
             remaining              cost history
                  │                       │
                  └───────────┬───────────┘
                              ▼
                         ARBITRATION
```

---

<!-- CAP-1073 | Continue Architecture Planning.md L88846–88895 | turn 79 | version 0.32 -->
## v0.32 — 32.31 v0.32 architecture

> **Source sections:** `CAP-1073`

```
                       DURABLE STORAGE
                              │
                              ▼
                       RECOVERY MANAGER
                              │
                ┌─────────────┼─────────────┐
                ▼             ▼             ▼
          TX recovery     lease scan    checkpoint scan
                │             │             │
                └─────────────┼─────────────┘
                              ▼
                       STATE RECONCILER
                              │
                              ▼
                     MATERIALIZED STATE
                              │
                              ▼
                       FRONTIER REBUILD
                              │
                              ▼
                       ADMISSION CONTROL
                              │
                              ▼
                         ARBITRATION
                              │
                              ▼
                         ALLOCATION
                              │
                              ▼
                          EXECUTION
                              │
                              ▼
                         OBSERVATION
                              │
                              ▼
                    DURABLE TRANSACTION
                              │
                ┌─────────────┼─────────────┐
                ▼             ▼             ▼
             knowledge       ledger      checkpoint
                │             │             │
                └─────────────┼─────────────┘
                              ▼
                           COMMIT
```

---

<!-- CAP-1112 | Continue Architecture Planning.md L90180–90225 | turn 81 | version 0.33 -->
## v0.33 — 33.32 v0.33 architecture

> **Source sections:** `CAP-1112`

```
                       DURABLE FRONTIER
                              │
                              ▼
                       ADMISSION CONTROL
                              │
                              ▼
                         ARBITRATION
                              │
                              ▼
                      SELECTED WORK ITEM
                              │
                              ▼
                    ┌─────────────────────┐
                    │ COORDINATION MANAGER│
                    └──────────┬──────────┘
                               │
                    ┌──────────┼──────────┐
                    ▼          ▼          ▼
                 Worker A   Worker B   Worker C
                    │          │          │
                    ▼          ▼          ▼
                 Claim/Lease/Capability/Capacity
                    │          │          │
                    └──────────┼──────────┘
                               ▼
                           EXECUTION
                               │
                               ▼
                         OBSERVATION
                               │
                               ▼
                       DURABLE TRANSACTION
                               │
                ┌──────────────┼──────────────┐
                ▼              ▼              ▼
             KNOWLEDGE      ACCOUNTING      EVENTS
                │              │              │
                └──────────────┼──────────────┘
                               ▼
                       SHARED FRONTIER
```

---

<!-- CAP-1119 | Continue Architecture Planning.md L90448–90498 | turn 83 | version 0.34 -->
## v0.34 — 34.1 New Architecture Boundary

> **Source sections:** `CAP-1119`

```
                    WORKERS
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
        Worker A             Worker B
             │                   │
             └─────────┬─────────┘
                       ▼
              Coordination Layer
                       │
              ┌────────┴────────┐
              ▼                 ▼
        Version Check      Causal Metadata
              │                 │
              └────────┬────────┘
                       ▼
                State Mutation
                       │
                ┌──────┴──────┐
                │             │
             ACCEPT        CONFLICT
                │             │
                ▼             ▼
             Commit       Conflict Record
                              │
                              ▼
                       Conflict Resolver
                              │
                       ┌──────┴──────┐
                       ▼             ▼
                    RESOLVED      UNRESOLVED
                       │             │
                       └──────┬──────┘
                              ▼
                       Materialized State
```

The new distinction is:

```
CLAIM OWNERSHIP
      ≠
MUTATE STATE
      ≠
RESOLVE CONFLICT
```

---

<!-- CAP-1169 | Continue Architecture Planning.md L92158–92188 | turn 85 | version 0.34 -->
## v0.34 — Final architecture by responsibility

> **Source sections:** `CAP-1169`

| Layer | Fundamental question |
| --- | --- |
| Goal | What are we looking for? |
| Query Planner | What search tactics could answer it? |
| Search Space | Where may we search? |
| Partition | What bounded region are we exploring? |
| Strategy | How do we explore it? |
| Candidate Source | What possible resources did we observe? |
| Candidate | What might be worth acquiring? |
| Policy | May this operation occur? |
| Capability | Can this runtime perform it? |
| Planner | What acquisition should be attempted? |
| Frontier | What work exists? |
| Arbitrator | What should execute next? |
| Allocator | What resources may it consume? |
| Coordinator | Which worker owns it? |
| Consistency | Is this mutation based on current state? |
| Acquisition | How do we obtain it? |
| Recognition | What did we obtain? |
| Evidence | What supports that interpretation? |
| Classification | What kind of resource is it? |
| Identity | What logical resource does it represent? |
| Revision | Which representation/version is this? |
| Verification | How strongly can we trust it? |
| Reconciliation | How do competing observations converge? |
| Coverage | What part of the search space was explored? |
| Completeness | What can we legitimately claim remains? |

---
