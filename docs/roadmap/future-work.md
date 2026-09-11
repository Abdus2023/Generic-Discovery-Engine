# Future Work

> **Status:** FUTURE
>
> **Source:** `Continue Architecture Planning.md`
>
> **Purpose:** Material the sources mark as the next boundary, next abstraction, open problem or still missing.

## Source Sections

- **v0.7 — Next boundary: v0.8** — `CAP-054` — `Continue Architecture Planning.md` L54582–54619
- **v0.8 — 17. v0.8 → v0.9** — `CAP-078` — `Continue Architecture Planning.md` L55568–55621
- **v0.9 — 11. The next problem is now visible** — `CAP-104` — `Continue Architecture Planning.md` L56255–56345
- **v0.10 — Next boundary: v0.11** — `CAP-127` — `Continue Architecture Planning.md` L57299–57343
- **v0.11 — 19. The next major abstraction: Candidate Sources** — `CAP-152` — `Continue Architecture Planning.md` L58240–58337
- **v0.13 — the next boundary** — `CAP-188` — `Continue Architecture Planning.md` L59398–59460
- **v0.14 — the next missing abstraction** — `CAP-221` — `Continue Architecture Planning.md` L60486–60544
- **v0.14 — 27. The next abstraction** — `CAP-270` — `Continue Architecture Planning.md` L61920–61952
- **v0.16 — 36. The deeper architectural transition** — `CAP-357` — `Continue Architecture Planning.md` L65086–65156
- **v0.16 — 37. What is still missing** — `CAP-358` — `Continue Architecture Planning.md` L65158–65160
- **v0.17 — 34. Next missing abstraction** — `CAP-419` — `Continue Architecture Planning.md` L66653–66694
- **v0.19 — Next boundary: v0.20 — Search-Space Partitioning + Discovery Strategies** — `CAP-511` — `Continue Architecture Planning.md` L69659–69688
- **v0.26 — Next boundary: v0.27** — `CAP-812` — `Continue Architecture Planning.md` L80162–80198
- **v0.28 — Next boundary — v0.29** — `CAP-919` — `Continue Architecture Planning.md` L83167–83226
- **v0.30 — Next boundary — v0.31** — `CAP-1012` — `Continue Architecture Planning.md` L86400–86466
- **v0.34 — 34.30 v0.34 → v0.35** — `CAP-1162` — `Continue Architecture Planning.md` L91907–91970

## Related Documents

- [Concept Overview](../concepts/overview.md)
- [System Model](../architecture/system-model.md)
- [Prototype Scope and Limitations](../prototype/limitations.md)
- [README.md](../README.md)

---

<!-- CAP-054 | Continue Architecture Planning.md L54582–54619 | turn 27 | version 0.7 -->
## v0.7 — Next boundary: v0.8

> **Source sections:** `CAP-054`

The natural next step is **not another provider**.

It is to separate:

```
DISCOVERY GRAPH
       +
ACQUISITION GRAPH
       +
EVIDENCE GRAPH
```

and introduce **capability-aware acquisition planning**:

```
Candidate
   │
   ▼
Capability Requirements
   │
   ├── GET
   ├── same-origin
   ├── textual
   ├── binary
   ├── authenticated
   ├── browser-context
   └── privileged
          │
          ▼
Capability Policy
          │
          ▼
Acquisition Plan
```

That is where the userscript starts becoming a **generic discovery runtime** rather than simply a sophisticated crawler.

<!-- CAP-078 | Continue Architecture Planning.md L55568–55621 | turn 29 | version 0.8 -->
## v0.8 — 17. v0.8 → v0.9

> **Source sections:** `CAP-078`

Once capability-aware acquisition exists, the next architectural problem becomes obvious:

```
Capability
      │
      ▼
Capability Provider
      │
      ├── userscript HTTP
      ├── browser context
      ├── native helper
      ├── WASM module
      └── future connector
```

That leads to the next abstraction:

```
                    ACQUISITION PLAN
                           │
                           ▼
                   CAPABILITY RESOLVER
                           │
                           ▼
                  PROVIDER SELECTION
                    /      |       \
                   /       |        \
                GM-XHR   Fetch    Browser
                   \       |        /
                    \      |       /
                     ▼     ▼      ▼
                       EXECUTOR
                           │
                           ▼
                       OBSERVATION
```

So **v0.9 should not add more discovery heuristics**.

It should introduce the **Acquisition Provider interface**:

```JavaScript
AcquisitionProvider
    ├── capabilities()
    ├── canExecute(plan)
    ├── execute(plan)
    └── describe()
```

Then the engine can stop assuming that “acquisition” means `GM_xmlhttpRequest`.

That is the point where the generic discovery engine gets a genuine **runtime/plugin boundary**.

<!-- CAP-104 | Continue Architecture Planning.md L56255–56345 | turn 31 | version 0.9 -->
## v0.9 — 11. The next problem is now visible

> **Source sections:** `CAP-104`

Once acquisition providers are pluggable, another architectural issue appears:

```
             PROVIDER
                │
                ▼
        ┌───────────────┐
        │ capabilities  │
        └───────┬───────┘
                │
                ▼
          canExecute()
                │
                ▼
             execute()
                │
                ▼
          OBSERVATION
```

Who owns **timeouts, retries, rate limits, concurrency, cancellation, and origin budgets**?

They should **not** be implemented independently by every provider.

Otherwise:

```
GM-XHR
   ├── retry
   ├── timeout
   └── concurrency

Fetch
   ├── retry
   ├── timeout
   └── concurrency

Browser
   ├── retry
   ├── timeout
   └── concurrency
```

and the runtime loses control.

The cleaner v0.10 boundary is therefore:

```
                 PLAN
                   │
                   ▼
              SCHEDULER
          ┌────────┼────────┐
          │        │        │
       budget   origin   cancellation
          │        │        │
          └────────┼────────┘
                   ▼
             PROVIDER
                   │
                   ▼
              EXECUTION
```

So **v0.10 should introduce an `AcquisitionRuntime` around providers**.

That gives us the eventual separation:

```
Policy
  = may this happen?

Scheduler
  = when may this happen?

Runtime
  = under what execution controls?

Provider
  = how does it happen?

Observer
  = what happened?

Recognizer
  = what does it mean?
```

This is the point where the DVB analogy becomes an actual systems architecture rather than merely a metaphor.

<!-- CAP-127 | Continue Architecture Planning.md L57299–57343 | turn 33 | version 0.10 -->
### v0.10 — Next boundary: v0.11

> **Source sections:** `CAP-127`

The next major problem is **response-provider routing**.

Right now acquisition returns a response and recognition providers inspect it. v0.11 can make that explicit as another capability-driven registry:

```
                  OBSERVATION
                       │
                       ▼
               RESPONSE ROUTER
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
        HTML          JSON         XML
        CSS           JS           PDF*
        Text          Binary       ...
          │            │            │
          └────────────┼────────────┘
                       ▼
                    DISCOVERY
```

That would give the engine symmetrical boundaries:

```
AcquisitionProvider
    = HOW TO GET

RecognitionProvider
    = HOW TO UNDERSTAND
```

and eventually:

```
Candidate
   → Acquisition Runtime
   → Acquisition Provider
   → Observation
   → Recognition Provider
   → Discovery
```

which is a strong foundation for the eventual **generic discovery algorithm**, rather than a specialized crawler.

<!-- CAP-152 | Continue Architecture Planning.md L58240–58337 | turn 35 | version 0.11 -->
## v0.11 — 19. The next major abstraction: Candidate Sources

> **Source sections:** `CAP-152`

There is still one hardcoded assumption hiding underneath the architecture:

```
candidate
    = URL
```

That is appropriate for the userscript prototype, but it is **not** generic.

The DVB analogy exposes the problem.

DVB blind scan does not begin with:

```
URL
```

It begins with a **search space**.

For a generic discovery engine, we should therefore introduce:

```
CandidateSource
```

Examples:

```
HTML links
Network observations
Browser history
User seed
Sitemap
Robots.txt
Search result
Document reference
Local filesystem
Archive index
Database
API response
```

Each source can produce candidates.

So v0.12 should introduce:

```
CandidateSource
        │
        ├── seed source
        ├── document source
        ├── network source
        ├── metadata source
        ├── filesystem source
        └── external index source
```

with the central contract:

```JavaScript
class CandidateSource {
    discover(context) {
        throw new Error('Not implemented');
    }

    describe() {
        return {
            id: 'unknown-source'
        };
    }
}
```

That is the point where the architecture finally separates:

```
WHERE TO SEARCH
        from
HOW TO ACQUIRE
        from
HOW TO RECOGNIZE
```

and gives us the three fundamental extensibility axes:

```
                DISCOVERY ENGINE
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
 CandidateSource  AcquisitionProvider  RecognitionProvider
      │                  │                  │
 "find it"           "get it"          "understand it"
```

That is the natural **v0.12 boundary**.

<!-- CAP-188 | Continue Architecture Planning.md L59398–59460 | turn 37 | version 0.13 -->
## v0.13 — the next boundary

> **Source sections:** `CAP-188`

There is now one major problem left in the loop:

```
many CandidateSources
        ↓
many proposals
        ↓
many candidates
        ↓
scheduler
```

The engine needs a formal **Discovery Controller** that determines:

* which sources run;
* when they run;
* what context they receive;
* how much work each source may generate;
* source-level budgets;
* duplicate suppression;
* source fairness;
* recursion/depth limits;
* provenance;
* cancellation;
* deterministic ordering.

In other words, v0.13 should introduce:

```
                    DISCOVERY CONTROLLER
                             │
             ┌───────────────┼────────────────┐
             ▼               ▼                ▼
       Source Scheduler   Source Budget   Source Policy
             │
             ▼
       CandidateSource
             │
             ▼
          Proposals
```

This is the missing equivalent of the **scan controller** in the DVB analogy.

At that point, the architecture has four independently controllable planes:

```
┌──────────────────────────────────────────────┐
│              GENERIC DISCOVERY               │
│                                              │
│  SOURCE        → WHERE TO LOOK               │
│  SCHEDULER     → WHAT TO TRY NEXT            │
│  ACQUISITION   → HOW TO GET IT               │
│  RECOGNITION   → HOW TO UNDERSTAND IT        │
│                                              │
│             EVIDENCE / PROVENANCE             │
│                 across all planes             │
└──────────────────────────────────────────────┘
```

That is the point where implementing the userscript becomes useful again: **the abstractions have stabilized enough that the next complete implementation can be a v0.13 vertical slice rather than another accumulation of special cases.**

<!-- CAP-221 | Continue Architecture Planning.md L60486–60544 | turn 39 | version 0.14 -->
## v0.14 — the next missing abstraction

> **Source sections:** `CAP-221`

One problem remains before this becomes a genuinely reusable discovery engine:

**the search space itself is still implicit.**

Currently the controller receives observations and asks sources to inspect them.

But a real blind scan has an explicit concept of:

```
SCAN DOMAIN
```

For the generic engine, this should become a **DiscoveryDomain**.

For example:

```
DiscoveryDomain
├── allowed schemes
├── allowed origins
├── allowed resource types
├── seed set
├── source set
├── maximum depth
├── global candidate budget
├── global acquisition budget
├── termination condition
└── policy
```

Then the engine can run:

```
Domain
  ↓
Initialize search frontier
  ↓
Discovery Controller
  ↓
Candidate frontier
  ↓
Acquisition
  ↓
Observation
  ↓
Expansion
  ↓
New frontier
  ↓
Termination
```

That is a major conceptual transition:

> **The userscript stops being “a scanner attached to the current page” and becomes “an engine capable of executing a bounded discovery domain.”**

The next version should therefore define **v0.14 — DiscoveryDomain + ScanSession**, including explicit seeds, frontier state, termination conditions, resumability, and the distinction between a **scan** and the underlying **discovery engine**.

<!-- CAP-270 | Continue Architecture Planning.md L61920–61952 | turn 41 | version 0.14 -->
## v0.14 — 27. The next abstraction

> **Source sections:** `CAP-270`

There is now another gap.

We have:

```
DiscoveryDomain
       ↓
ScanSession
       ↓
DiscoveryController
       ↓
DiscoveryTask
       ↓
Candidate
```

But the frontier is still split conceptually between:

```
discovery work
```

and:

```
acquisition work
```

A real scan needs a unified notion of **work state** without collapsing discovery and acquisition into the same operation.

That suggests the next boundary:

<!-- CAP-357 | Continue Architecture Planning.md L65086–65156 | turn 45 | version 0.16 -->
## v0.16 — 36. The deeper architectural transition

> **Source sections:** `CAP-357`

The progression now looks like:

```
v0.6
Resource discovery

v0.7
Acquisition planning

v0.8
Capabilities

v0.9
Acquisition providers

v0.10
Acquisition runtime

v0.11
Recognition runtime

v0.12
Candidate sources

v0.13
Discovery controller

v0.14
Discovery domain + scan session

v0.15
Work + frontier runtime

v0.16
Evidence + provenance
```

The system now has three fundamental layers of state:

```
EXECUTION STATE
    │
    └── Work / Session / Event Ledger

KNOWLEDGE STATE
    │
    └── Candidate / Resource / Claim

EVIDENCE STATE
    │
    └── Observation / Evidence / Provenance
```

That separation is important enough to make explicit:

```
                    DISCOVERY ENGINE
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
      EXECUTION         KNOWLEDGE        EVIDENCE
          │                │                │
       Session          Resource        Observation
       Work             Candidate       Evidence
       Events           Claim           Provenance
```

---

<!-- CAP-358 | Continue Architecture Planning.md L65158–65160 | turn 45 | version 0.16 -->
## v0.16 — 37. What is still missing

> **Source sections:** `CAP-358`

At this point the engine can answer:

<!-- CAP-419 | Continue Architecture Planning.md L66653–66694 | turn 47 | version 0.17 -->
## v0.17 — 34. Next missing abstraction

> **Source sections:** `CAP-419`

There is now a remaining problem at the **resource semantics** layer.

We can identify:

```
Resource R
```

and know:

```
R has URL A
R has URL B
R had fingerprint H1
R later had fingerprint H2
```

But we still do not have a rigorous way to say:

> **What kind of thing is R?**

For example:

```
HTML page
PDF document
service manual
image
API endpoint
JSON dataset
sitemap
software artifact
binary
video
feed
```

More importantly, one resource may have several observations with conflicting or evolving classifications.

So the next boundary is:

<!-- CAP-511 | Continue Architecture Planning.md L69659–69688 | turn 51 | version 0.19 -->
## v0.19 — Next boundary: v0.20 — Search-Space Partitioning + Discovery Strategies

> **Source sections:** `CAP-511`

The next missing abstraction is now **how the engine chooses where to search next**.

At present, the frontier contains WorkItems, but the engine still lacks a rigorous model for:

```
"Which region of the resource universe should I explore?"
```

That leads naturally to:

```
DiscoveryDomain
      │
      ├── partitions
      │
      ├── strategies
      │
      ├── exploration budget
      │
      ├── exploitation priority
      │
      └── adaptive expansion
               │
               ▼
          WorkItem Frontier
```

This is where the DVB analogy becomes especially useful: **blind scanning is not merely candidate generation; it is systematic partitioning and coverage of an unknown search space.**

<!-- CAP-812 | Continue Architecture Planning.md L80162–80198 | turn 65 | version 0.26 -->
## v0.26 — Next boundary: v0.27

> **Source sections:** `CAP-812`

The next missing layer is now the **Enumeration Runtime**.

The key problem is that some tactics are fundamentally enumerators:

```
Sitemap
Repository index
API pagination
Manifest
Directory-like listing
Feed
Finite catalog
```

They need stronger semantics than an ordinary strategy:

```
Enumerator
 ├── ordering
 ├── cursor
 ├── pagination
 ├── cardinality
 ├── duplicate detection
 ├── termination proof/evidence
 ├── completeness conditions
 └── invalidation
```

So the natural next step is:

```
v0.27 — Enumeration Runtime
```

which connects **tactic execution** to the **coverage/completeness machinery** from v0.22–v0.23 without falsely turning “enumerated” into “complete.”

<!-- CAP-919 | Continue Architecture Planning.md L83167–83226 | turn 69 | version 0.28 -->
## v0.28 — Next boundary — v0.29

> **Source sections:** `CAP-919`

The next unresolved problem is **dynamic frontier generation**.

We currently have:

```
QueryPlan
   ↓
Tactic
   ↓
Strategy
   ↓
Partition
   ↓
Work
```

But real discovery constantly creates new search regions:

```
Repository discovered
        ↓
new repository partition

New sitemap discovered
        ↓
new enumeration partition

New document family discovered
        ↓
new semantic partition

New language/version path discovered
        ↓
new partition
```

So v0.29 should formalize:

```
                    DISCOVERY
                       │
                       ▼
                NEW SEARCH REGION
                       │
                       ▼
               PARTITION PROPOSAL
                       │
                       ▼
              PARTITION VALIDATION
                       │
                       ▼
              SEARCH-SPACE EXPANSION
                       │
                       ▼
                    FRONTIER
```

The key issue will be preventing **partition explosion**: a discovery result must not automatically become an unlimited number of new search regions.

<!-- CAP-1012 | Continue Architecture Planning.md L86400–86466 | turn 75 | version 0.30 -->
## v0.30 — Next boundary — v0.31

> **Source sections:** `CAP-1012`

The natural next problem is now:

> **Who owns the finite resources being allocated?**

v0.30 can say:

```
"run this work next"
```

but it still needs a rigorous accounting model for:

```
requests
bytes
CPU
wall-clock time
storage
concurrency
origin quotas
discovery budget
acquisition budget
planning budget
verification budget
```

So the next boundary becomes:

```
# v0.31 — Unified Resource & Cost Ledger

Budget
    ↓
Reservation
    ↓
Allocation
    ↓
Consumption
    ↓
Actual Cost
    ↓
Settlement
    ↓
Remaining Capacity
    ↓
Frontier Arbitration
```

That would close the loop:

```
ARBITRATION
     ↓
ALLOCATION
     ↓
EXECUTION
     ↓
MEASURED COST
     ↓
RESOURCE LEDGER
     ↓
ARBITRATION
```

That is the point where the blind-scan-inspired discovery engine starts becoming a genuine **resource-bounded search runtime**, rather than merely an advanced crawler.

<!-- CAP-1162 | Continue Architecture Planning.md L91907–91970 | turn 83 | version 0.34 -->
## v0.34 — 34.30 v0.34 → v0.35

> **Source sections:** `CAP-1162`

The next missing layer is now visible.

v0.34 can establish:

```
A and B
   ↓
shared state
   ↓
conflict detection
   ↓
deterministic convergence
```

But there is still a larger question:

> How do independent execution contexts exchange state, events, frontier changes, leases, observations, and conflicts?

That produces the next boundary:

```
# v0.35 — Cross-Context Event Transport & Replication

Worker A
   │
   │ events
   ▼
Transport
   │
   ├──────────────► Worker B
   │
   ├──────────────► Worker C
   │
   └──────────────► Persistence
                         │
                         ▼
                    Event Journal
```

The conceptual progression becomes:

```
v0.33
WHO OWNS WORK?

        ↓

v0.34
WHOSE STATE IS AUTHORITATIVE?

        ↓

v0.35
HOW DOES STATE MOVE BETWEEN CONTEXTS?

        ↓

v0.36
HOW DO WE RECOVER FROM PARTITIONED / DISCONNECTED CONTEXTS?
```

That is the natural continuation from the DVB-inspired **blind scan** abstraction: the scanner is no longer merely discovering candidates; it is becoming a **distributed, resumable, evidence-producing search system whose frontier itself is a coordinated state machine**.
