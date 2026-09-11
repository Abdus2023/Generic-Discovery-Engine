# DVB Blind Scan

> **Status:** DESIGNED
>
> **Source:** `Continue Architecture Planning.md`; `Userscript Discovery Prototype.md`
>
> **Purpose:** The DVB blind-scan material: the originating analogy, the mapping tables, and how the analogy evolves.

## Contents

- *Turn lead-in* — `Userscript Discovery Prototype.md` L3–3
- *Turn lead-in* — `Userscript Discovery Prototype.md` L9–23
- **Generic pseudocode** — `Userscript Discovery Prototype.md` L25–64
- **5. Use DVB metadata to escape blind mode** — `Userscript Discovery Prototype.md` L303–346
- **The DVB analogy** — `Userscript Discovery Prototype.md` L3009–3025
- **v0.8 — 16. The DVB analogy is now cleaner** — `Continue Architecture Planning.md` L55534–55566
- **v0.13 — 19. The generic blind-scan analogy is now much stronger** — `Continue Architecture Planning.md` L60290–60325
- **v0.14 — 2. DVB analogy** — `Continue Architecture Planning.md` L60649–60689
- **v0.20 — 20.10 Blind-Scan Analogy** — `Continue Architecture Planning.md` L70129–70195
- **v0.20 — 20.31 The DVB Analogy Is Now Structural** — `Continue Architecture Planning.md` L71074–71129
- **v0.25 — 25.26 Query planner and DVB analogy** — `Continue Architecture Planning.md` L78152–78200
- **v0.27 — 27.31 The emerging blind-scan analogy** — `Continue Architecture Planning.md` L81569–81606
- **v0.29 — 29.35 Blind-scan interpretation** — `Continue Architecture Planning.md` L84578–84608
- **v0.30 — What the DVB analogy actually contributed** — `Continue Architecture Planning.md` L84845–84908
- **v0.34 — DVB blind scan** — `Continue Architecture Planning.md` L92089–92101

## Related Documents

- [Concept Overview](../concepts/overview.md)
- [Generic Discovery](../concepts/generic-discovery.md)
- [Prototype Scope and Limitations](../prototype/limitations.md)
- [README.md](../README.md)

---

<!-- source: Userscript Discovery Prototype.md L3–3 | turn 0 | You turn lead-in -->
DVB blind scan as a generic discovery algorithm

<!-- source: Userscript Discovery Prototype.md L9–23 | turn 1 | ChatGPT turn lead-in -->
If you mean **DVB blind scan as a generic algorithm for discovering unknown digital TV/radio multiplexes**, the core idea is:

1. **Sweep the RF spectrum** over a configured frequency range.
2. At each candidate frequency, **detect a signal** above the noise floor.
3. Try plausible **symbol rates / bandwidths / modulation parameters**.
4. Attempt **carrier synchronization and demodulation**.
5. If the signal locks, **parse the transport stream**.
6. Extract service/network metadata such as:
    * Network ID
    * Transport Stream ID
    * Service IDs
    * Service names
    * PIDs
    * LCNs, where available
7. Deduplicate discoveries and continue scanning until the entire range is covered.

<!-- source: Userscript Discovery Prototype.md L25–64 | turn 1 | version ? -->
### Generic pseudocode

```
blind_scan(start_frequency, end_frequency):

    discoveries = {}

    for frequency in frequency_grid(start_frequency, end_frequency):

        tune(frequency)

        if !signal_detected():
            continue

        for parameters in candidate_parameters():

            if !demodulator_lock(parameters):
                continue

            ts = acquire_transport_stream()

            if !valid_transport_stream(ts):
                continue

            metadata = parse_si_tables(ts)

            discovery = {
                frequency,
                parameters,
                network_id: metadata.network_id,
                transport_stream_id: metadata.transport_stream_id,
                services: metadata.services
            }

            discoveries.add_or_merge(discovery)

            break

    return discoveries
```

<!-- source: Userscript Discovery Prototype.md L303–346 | turn 3 | version ? -->
## 5. Use DVB metadata to escape blind mode

Once a multiplex is successfully decoded, the scan can become much more efficient.

For example:

```
Blind scan
    │
    ├── Multiplex A discovered
    │       │
    │       └── NIT says:
    │            ├── Multiplex B
    │            ├── Multiplex C
    │            └── Multiplex D
    │
    ▼
Guided scan
```

This gives two complementary discovery mechanisms:

**Blind discovery**

```
"I don't know what's there."
```

**Network-assisted discovery**

```
"I found one network; tell me what else belongs to it."
```

A practical scanner should maintain both queues:

```
blind_candidates
guided_candidates
```

and prioritize guided candidates because their probability of success is much higher.

---

<!-- source: Userscript Discovery Prototype.md L3009–3025 | turn 13 | version ? -->
### The DVB analogy

| DVB blind scan | Userscript engine |
| --- | --- |
| Frequency | URL/resource candidate |
| RF energy | Reachable/interesting resource |
| Carrier lock | Successful acquisition |
| FEC/TS lock | Valid response |
| PSI/SI | HTML/metadata |
| NIT | Metadata-derived candidates |
| Multiplex | Discovered resource/page |
| Service | Link/resource/function |
| Scan database | Persistent knowledge base |
| Blind scan | Initial candidate generation |
| Network-guided scan | Recursive discovery |

The **next evolution** would be to make the userscript genuinely protocol-agnostic by introducing a `DiscoveryProvider` interface, so HTML, JSON, JavaScript, GraphQL, DOM elements, and other application-specific sources can all act like different DVB demodulators while sharing the same scheduler and knowledge base.

<!-- source: Continue Architecture Planning.md L55534–55566 | turn 29 | version 0.8 -->
## v0.8 — 16. The DVB analogy is now cleaner

The original inspiration can be expressed without pretending the domains are identical:

```
DVB blind scan                 Generic discovery

unknown spectrum       →       unknown resource space

tuning candidate       →       acquisition candidate

signal detection       →       observable resource

lock                   →       recognizable response

service discovery      →       provider discovery

new transport/service  →       new candidate

scan constraints       →       capability/policy constraints

scan state              →       deterministic decision ledger
```

The reusable principle is therefore not:

> “crawl the web like a DVB tuner.”

It is:

> **Explore a partially unknown space using bounded candidate generation, observation, recognition, expansion, and explicit control constraints.**

---

<!-- source: Continue Architecture Planning.md L60290–60325 | turn 39 | version 0.13 -->
## v0.13 — 19. The generic blind-scan analogy is now much stronger

The mapping becomes:

```
DVB Blind Scan                  Generic Discovery
────────────────────────────────────────────────────
Search space                   Candidate source
Scan controller                Discovery controller
Tuning candidate               Candidate proposal
Tuner resource                 Acquisition provider
Lock detection                 Recognition
Service information            Evidence
Service table                  Knowledge graph
New service                    New candidate
Scan budget                    Discovery budget
Tuning budget                  Acquisition budget
```

The critical abstraction is:

```
SEARCH SPACE
    ↓
CONTROLLED EXPLORATION
    ↓
OBSERVATION
    ↓
INTERPRETATION
    ↓
EXPANDED SEARCH SPACE
```

That is the generic pattern.

---

<!-- source: Continue Architecture Planning.md L60649–60689 | turn 41 | version 0.14 -->
## v0.14 — 2. DVB analogy

The analogy becomes much stronger here.

A DVB blind scan does not mean:

> "Search everything."

It operates within a defined physical search space:

```
frequency range
symbol rates
modulations
bandwidth
delivery system
scan mode
```

The scanner then maintains state for one scan.

The generic discovery equivalent is:

```
DVB                         Generic Discovery

frequency range       →    URL/resource domain
delivery system       →    resource types
tuning parameters     →    acquisition capabilities
scan constraints      →    discovery/acquisition policy
found transponder     →    discovered resource
service scan          →    secondary discovery
scan state             →    ScanSession
scan completion        →    termination condition
```

The key principle is:

> **The domain defines the search universe; the session explores one bounded instance of it.**

---

<!-- source: Continue Architecture Planning.md L70129–70195 | turn 53 | version 0.20 -->
## v0.20 — 20.10 Blind-Scan Analogy

The analogy can now be stated precisely.

DVB:

```
Unknown spectrum
      ↓
Frequency partitions
      ↓
Tune
      ↓
Detect signal
      ↓
Lock
      ↓
Extract services
      ↓
Discover additional structure
```

Generic resource discovery:

```
Unknown resource space
      ↓
Search partitions
      ↓
Acquire candidates
      ↓
Recognize response
      ↓
Resolve resource
      ↓
Extract evidence
      ↓
Discover additional structure
```

The common abstraction is:

```
UNKNOWN SPACE
      ↓
PARTITION
      ↓
PROBE
      ↓
OBSERVE
      ↓
RECOGNIZE
      ↓
EXPAND KNOWLEDGE
      ↓
REFINE SEARCH
```

Not:

```
frequency ↔ URL
```

The latter is only superficial analogy.

---

<!-- source: Continue Architecture Planning.md L71074–71129 | turn 53 | version 0.20 -->
## v0.20 — 20.31 The DVB Analogy Is Now Structural

We can now formulate the analogy without forcing domain-specific concepts:

| DVB blind scan | Generic Discovery Engine |
| --- | --- |
| Unknown spectrum | Unknown resource universe |
| Frequency range | Search-space partition |
| Scan step | Exploration strategy |
| Tune/probe | Acquisition attempt |
| Signal detection | Observable response |
| Lock | Recognition |
| Service information | Evidence |
| Service | Resource |
| Transport/service relationships | Resource graph |
| Repeated scan | New scan session |
| Signal changes | Artifact/revision changes |
| Scan budget | Discovery/acquisition budget |
| Coverage | Strategy-relative exploration coverage |

The abstraction is therefore:

```
UNKNOWN UNIVERSE
       │
       ▼
PARTITION
       │
       ▼
STRATEGIC PROBE
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
       ▼
NEW PARTITIONS
       │
       └───────────────► ...
```

That recursive final edge is the key.

Discovery doesn't merely find objects.

It can discover **new regions in which additional objects may exist**.

---

<!-- source: Continue Architecture Planning.md L78152–78200 | turn 63 | version 0.25 -->
## v0.25 — 25.26 Query planner and DVB analogy

The analogy now becomes more precise.

```
DVB blind scan
──────────────────────────────
Scan objective
      ↓
frequency range
      ↓
scan strategy
      ↓
candidate frequency
      ↓
tune
      ↓
signal
      ↓
lock
      ↓
service discovery
```

Generic discovery:

```
Search goal
      ↓
search domain
      ↓
query plan
      ↓
search tactic
      ↓
candidate region
      ↓
acquisition
      ↓
observation
      ↓
recognition
      ↓
resource discovery
```

The analogy remains architectural rather than literal.

---

<!-- source: Continue Architecture Planning.md L81569–81606 | turn 67 | version 0.27 -->
## v0.27 — 27.31 The emerging blind-scan analogy

At this point the analogy is becoming structurally precise.

```
DVB BLIND SCAN                  GENERIC DISCOVERY
------------------------------------------------------------
frequency space          →      search space
scan range               →      domain/partition
tuning step              →      tactic/strategy
probe                    →      acquisition
signal observation       →      observation
service detection        →      recognition
service metadata         →      classification
discovered service       →      resource
scan progress            →      cursor/checkpoint
scan exhaustion          →      enumerator exhaustion
coverage                 →      search-space coverage
absence evidence         →      scoped negative evidence
```

The analogy should remain architectural rather than literal.

The web has no equivalent of a universally enumerable RF spectrum.

That is why the system must distinguish:

```
systematic exploration
```

from:

```
provable completeness
```

---

<!-- source: Continue Architecture Planning.md L84578–84608 | turn 71 | version 0.29 -->
## v0.29 — 29.35 Blind-scan interpretation

The DVB-inspired analogy becomes even stronger:

```
BLIND SCAN                         GENERIC DISCOVERY
---------------------------------------------------------
known scan range             →     DiscoveryDomain
frequency region             →     SearchPartition
scan strategy                →     DiscoveryStrategy
tuning/probing               →     Acquisition
signal observation           →     Observation
detected service             →     Resource
new multiplex/network info   →     PartitionProposal
new scan region              →     Search-space expansion
scan state                   →     Cursor/checkpoint
overlapping discoveries      →     Reconciliation
coverage                     →     CoverageRecord
```

The essential abstraction is no longer:

```
"scan URLs"
```

but:

> **Discover both resources and the structure of the space in which resources can be discovered.**

---

<!-- source: Continue Architecture Planning.md L84845–84908 | turn 73 | version 0.30 -->
## v0.30 — What the DVB analogy actually contributed

The useful abstraction from blind scanning is:

```
defined search region
        ↓
systematic probing
        ↓
observation
        ↓
discovered structure
        ↓
new search regions
        ↓
persistent scan position
        ↓
explicit exhaustion
```

Generalized:

```
SearchSpace
     ↓
Partition
     ↓
Probe
     ↓
Observation
     ↓
Discovery
     ↓
PartitionExpansion
     ↓
Checkpoint
     ↓
FrontierUpdate
     ↓
Exhaustion / Coverage
```

This is substantially broader than DVB.

The same architecture can describe:

* websites
* document repositories
* APIs
* software registries
* filesystem trees
* knowledge bases
* archives
* package indexes
* browser-visible applications
* service-document universes
* structured databases
* network resource catalogs

The acquisition mechanism changes.

The **control model does not**.

---

<!-- source: Continue Architecture Planning.md L92089–92101 | turn 85 | version 0.34 -->
### v0.34 — DVB blind scan

```
frequency space
      ↓
probe
      ↓
signal
      ↓
transport discovery
      ↓
new services
```
