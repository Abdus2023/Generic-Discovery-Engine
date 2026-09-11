# Generic Discovery Engine
 
A browser-based discovery engine inspired by the architecture of **DVB blind scanning**.
 
The project explores whether the fundamental pattern behind blind discovery in digital broadcasting can be generalized to other information-acquisition domains.
 
The prototype applies that pattern to web resources:
 `Candidate     ↓ Probe / Acquisition     ↓ Observation     ↓ Recognition     ↓ Discovery     ↓ Candidate Expansion     ↓ Scheduler     ↺ ` 
## Core Idea
 
A DVB blind scanner does not begin with complete knowledge of the available services.
 
It searches a parameter space, detects potentially interesting signals, attempts acquisition, validates what it receives, extracts metadata, and uses that metadata to discover additional resources.
 
This project generalizes that control pattern:
 `DVB Blind Scan              Generic Discovery  Frequency                   Candidate     ↓                           ↓ Signal detection             Probe     ↓                           ↓ Demodulator acquisition      Observation     ↓                           ↓ Transport validation         Recognition     ↓                           ↓ PSI/SI metadata              Metadata     ↓                           ↓ Network discovery            Candidate expansion ` 
The goal is **not** to implement a DVB receiver in JavaScript.
 
The goal is to investigate the **generic discovery algorithm underlying blind scanning**.
  
## Current Prototype
 
The current implementation is a Tampermonkey/Greasemonkey userscript.
 
It can:
 
 
- generate URL candidates
 
- maintain a priority queue
 
- concurrently acquire candidates
 
- prevent concurrent workers from claiming the same candidate
 
- record observations
 
- recognize different response types
 
- extract new candidates
 
- preserve candidate provenance
 
- deduplicate candidates
 
- persist discovery state
 
- export discovery results
 
- recursively expand the search space
 

 
Current response providers:
 `HTTP Response      │      ├── HTML Provider      │      ├── links      │      └── resources      │      ├── JSON Provider      │      └── URL-like values      │      └── Text Provider             └── HTTP(S) URLs `  
## Architecture
 `                     ┌─────────────────────┐                      │   Discovery Engine  │                      └──────────┬──────────┘                                 │                      ┌──────────▼──────────┐                      │      Scheduler      │                      └──────────┬──────────┘                                 │                      ┌──────────▼──────────┐                      │      Candidate      │                      └──────────┬──────────┘                                 │                      ┌──────────▼──────────┐                      │    Acquisition      │                      │       Adapter       │                      └──────────┬──────────┘                                 │                      ┌──────────▼──────────┐                      │     Observation     │                      └──────────┬──────────┘                                 │                      ┌──────────▼──────────┐                      │  Provider Registry  │                      └──────────┬──────────┘                                 │                  ┌──────────────┼──────────────┐                  ▼              ▼              ▼              HTML           JSON            Text              Provider       Provider        Provider                  │              │              │                  └──────────────┼──────────────┘                                 ▼                          ┌─────────────┐                          │ Discovery   │                          └──────┬──────┘                                 │                          New Candidates                                 │                                 └──────────► Scheduler `  
## Candidate Lifecycle
 
Candidates move through explicit ownership states:
 `QUEUED    │    ▼ CLAIMED    │    ├───────────────┐    ▼               ▼ COMPLETED        FAILED ` 
The critical invariant is:
 `A candidate may have at most one active owner. ` 
Candidate claiming is performed synchronously before asynchronous network acquisition:
 `worker   │   ├── claim candidate   │   └── await HTTP request ` 
This prevents multiple concurrent workers from selecting the same candidate.
  
## Discovery Model
 
The system distinguishes several concepts that are often incorrectly collapsed into one object.
 
### Candidate
 
Something the engine intends to investigate.
 `Candidate {     target     type     priority     origin     parent } ` 
### Observation
 
What acquisition actually produced.
 `Observation {     candidate     HTTP status     content type     body     errors } ` 
### Discovery
 
A validated interpretation of an observation.
 `Discovery {     kind     confidence     data     provenance } ` 
This separation allows the same candidate to have different observations over time and allows discoveries to retain evidence about how they were obtained.
  
## Provenance
 
Candidate generation is recorded.
 
For example:
 `initial page      │      ▼ HTML document      │      ├── link A      ├── link B      └── resource C              │              ▼         JSON response              │              └── URL D ` 
The resulting discovery graph can therefore answer:
 
 
Why did the engine investigate this resource?
 
 
rather than merely reporting:
 
 
This resource was found.
 
  
## Search Strategy
 
The prototype currently uses priority-based scheduling.
 
Conceptually:
 `priority(candidate) =     estimated_value     × estimated_probability     ÷ acquisition_cost ` 
The current implementation uses simpler heuristic priorities, but the architecture leaves room for more sophisticated search strategies.
 
Potential future strategies include:
 `Exhaustive Energy/Signal-inspired Priority-first Historical Metadata-guided Breadth-first Depth-first Adaptive Hybrid `  
## Generic Discovery Loop
 
The fundamental algorithm is:
 `initialize search space  while candidates remain:      candidate ← scheduler.claim()      observation ← acquire(candidate)      provider ← recognize(observation)      if provider accepts observation:          discovery ← provider.discover(observation)          store discovery          candidates ← provider.expand(discovery)          enqueue candidates      mark candidate complete ` 
The important operation is the feedback loop:
 `Observation     ↓ Discovery     ↓ New knowledge     ↓ New candidates ` 
This transforms discovery from a static list traversal into an **adaptive search process**.
  
## Scope
 
### This repository currently implements
 
 
- browser-side discovery
 
- URL candidate generation
 
- concurrent HTTP acquisition
 
- candidate ownership
 
- response recognition
 
- HTML discovery
 
- JSON discovery
 
- text discovery
 
- recursive candidate expansion
 
- provenance
 
- deduplication
 
- persistent state
 
- JSON export
 

 
### This repository does not currently implement
 
 
- RF spectrum scanning
 
- SDR hardware access
 
- DVB tuner control
 
- DVB-S/S2 demodulation
 
- DVB-T/T2 demodulation
 
- DVB-C demodulation
 
- carrier synchronization
 
- symbol-rate estimation
 
- FEC decoding
 
- MPEG transport-stream decoding
 
- DVB PSI/SI parsing
 
- NIT-based DVB discovery
 

 
Therefore:
 
 
**This is DVB-inspired, not DVB-compatible.**
 
 
The analogy concerns the **discovery architecture**, not the physical-layer implementation.
  
## Why DVB Blind Scan?
 
DVB blind scanning provides a useful model because the receiver begins with incomplete information.
 
It must:
 
 
1. search an unknown space
 
2. detect candidates
 
3. test hypotheses
 
4. validate observations
 
5. extract structured information
 
6. discover additional candidates
 
7. avoid duplicate work
 
8. continue until the search space is sufficiently covered
 

 
That pattern appears in many other domains.
 
Possible applications include:
 `Web discovery Document discovery Repository discovery API discovery Service discovery Network resource discovery Device discovery Knowledge-base acquisition Digital archive discovery ` 
The project investigates whether these can share a common discovery substrate.
  
## Design Principles
 
### 1. Discovery is not acquisition
 `Acquisition → produces observations  Recognition → interprets observations  Discovery → creates knowledge ` 
### 2. Candidates are hypotheses
 
A candidate means:
 
 
"This is worth investigating."
 
 
It does not mean:
 
 
"This resource exists."
 
 
### 3. Observations are evidence
 
A failed acquisition is still an observation.
 
### 4. Metadata expands the search space
 
Discovery is recursive.
 
### 5. Provenance matters
 
Every discovery should retain its origin.
 
### 6. Concurrency requires explicit ownership
 
Workers must claim work before performing asynchronous operations.
 
### 7. Providers should be replaceable
 
HTML, JSON, text, APIs, documents, and other protocols should not require rewriting the scheduler.
 
### 8. The search engine should remain protocol-independent
 
Protocol-specific knowledge belongs in providers/adapters.
  
## Roadmap
 
### Phase 0 — Prototype
 
 
- [x] candidate model
 
- [x] scheduler
 
- [x] concurrent acquisition
 
- [x] atomic candidate claiming
 
- [x] observation model
 
- [x] discovery model
 
- [x] provenance
 
- [x] HTML provider
 
- [x] JSON provider
 
- [x] text provider
 
- [x] persistent state
 
- [x] export
 

 
### Phase 1 — Discovery Core
 
 
- [ ] formal provider interface
 
- [ ] candidate fingerprints
 
- [ ] observation fingerprints
 
- [ ] configurable retry policy
 
- [ ] candidate expiration
 
- [ ] discovery confidence model
 
- [ ] search-space coverage metrics
 
- [ ] event stream
 
- [ ] structured logging
 

 
### Phase 2 — Web Intelligence
 
 
- [ ] HTTP headers provider
 
- [ ] XML provider
 
- [ ] RSS/Atom provider
 
- [ ] JavaScript resource provider
 
- [ ] sitemap provider
 
- [ ] robots.txt provider
 
- [ ] API/JSON-LD provider
 
- [ ] document-link provider
 
- [ ] URL pattern inference
 

 
### Phase 3 — Adaptive Search
 `Blind discovery       ↓ Observation       ↓ Inference       ↓ Candidate ranking       ↓ Guided discovery       ↓ New observations ` 
Potential additions:
 
 
- adaptive priority
 
- search-space partitioning
 
- negative evidence
 
- candidate clustering
 
- historical knowledge
 
- change detection
 
- active exploration
 

 
### Phase 4 — Generic Acquisition Framework
 
Separate the browser implementation into:
 `Discovery Core      │      ├── Candidate Store      ├── Scheduler      ├── Evidence Store      ├── Provenance Graph      └── Discovery Graph  Acquisition Adapters      │      ├── HTTP      ├── Browser DOM      ├── Browser APIs      └── External sources  Recognition Providers      │      ├── HTML      ├── JSON      ├── XML      ├── Documents      └── Domain-specific protocols `  
## Non-Goals
 
This project is not intended to become:
 
 
- a general-purpose web crawler clone
 
- a browser automation framework
 
- an RF scanner implemented in JavaScript
 
- an unrestricted Internet crawler
 
- a replacement for specialized DVB software
 

 
The purpose is to investigate a **general discovery architecture**.
  
## Conceptual Formula
 
The project can be summarized as:
 
[ \boxed{ Candidate \rightarrow Observation \rightarrow Evidence \rightarrow Discovery \rightarrow Candidate\ Expansion } ]
 
Or more compactly:
 `SEARCH   ↓ PROBE   ↓ OBSERVE   ↓ RECOGNIZE   ↓ DISCOVER   ↓ EXPAND   ↺ ` 
DVB blind scanning is the motivating example.
 
The intended destination is a **generic, adaptive discovery engine**.

## Documentation
 
The two original planning documents have been mechanically split into a structured documentation tree under [`docs/`](docs/README.md):
 
```
docs/
├── README.md               documentation index
├── SOURCE-MAP.md           traceability map: every source section has an id
├── SPLIT-MANIFEST.yaml     machine-readable source of truth (records, hashes, diff)
├── REVIEW-NOTES.md         contradictions, defects and unverified claims
├── concepts/               concept overview, generic discovery, discovery loop
├── architecture/           system model, data models, models derived from DVB,
│                           scheduler, concurrency, providers, sessions, budgets
├── acquisition/            acquisition model, response recognition, runtime
├── providers/              prototype response providers and candidate sources
├── prototype/              userscript prototype: overview, narrative, configuration,
│                           limitations, and every complete version artifact
├── research/               DVB blind-scan material
├── validation/             invariants, verification, failure taxonomy
└── roadmap/                future work
```

Every extracted section is identified as `USP-nnn`
(`Userscript Discovery Prototype.md`) or `CAP-nnn`
(`Continue Architecture Planning.md`) and listed with its destination, action and
status in [`docs/SOURCE-MAP.md`](docs/SOURCE-MAP.md). Each section in the tree
carries a `> **Source sections:**` attribution line pointing back to those ids.
[`docs/SPLIT-MANIFEST.yaml`](docs/SPLIT-MANIFEST.yaml) is the machine-readable
source of truth for the same mapping.
 
Start at [`docs/README.md`](docs/README.md).
 
The split is **mechanical**: material was moved, grouped and cross-referenced, not redesigned. No architecture, algorithm, interface or requirement was changed, added or removed. All 1,244 identified source sections are accounted for (0 unaccounted). Contradictions (`C-01`–`C-11`) and source-document defects (`D-01`–`D-05`) were deliberately left unresolved and recorded in [`docs/REVIEW-NOTES.md`](docs/REVIEW-NOTES.md).
 
## Repository Structure
 
```
.
├── README.md               this file
├── archive/                original planning documents, retained for provenance
│   ├── Continue Architecture Planning.md
│   └── Userscript Discovery Prototype.md
└── docs/                   structured documentation tree
```
 
## Current Status
 
- **Documentation:** mechanically split into 61 documents, cross-referenced, with full traceability; contradictions preserved as open items.
- **Prototype:** browser userscript; the last complete script artifact in the planning conversation is v0.7.1 ([`docs/prototype/versions/`](docs/prototype/versions/README.md)).
- **Designed architecture:** specified through v0.35 in the planning conversation; treated as design, not implementation, in the documentation tree.
- **Source code:** none. The split operation modified documentation only.
