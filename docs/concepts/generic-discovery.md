# Generic Discovery

> **Status:** DESIGNED
>
> **Source:** `Userscript Discovery Prototype.md`
>
> **Purpose:** The generic-discovery abstraction itself: layers, parameter-space search, naming and the final abstraction.

## Contents

- **Making it genuinely generic** — `Userscript Discovery Prototype.md` L66–102
- *Turn lead-in* — `Userscript Discovery Prototype.md` L114–114
- **1. Separate the layers** — `Userscript Discovery Prototype.md` L116–144
- **7. Generic algorithm** — `Userscript Discovery Prototype.md` L384–439
- **The key insight** — `Userscript Discovery Prototype.md` L441–452
- **15. The generic discovery abstraction** — `Userscript Discovery Prototype.md` L739–775
- **23. A useful formal name** — `Userscript Discovery Prototype.md` L1071–1099
- **30. The final abstraction** — `Userscript Discovery Prototype.md` L1378–1429

## Related Documents

- [Concept Overview](overview.md)
- [The Discovery Loop](discovery-loop.md)
- [DVB Blind Scan](../research/dvb-blind-scan.md)
- [System Model](../architecture/system-model.md)

---

<!-- source: Userscript Discovery Prototype.md L66–102 | turn 1 | version ? -->
### Making it genuinely generic

The important abstraction is to separate **RF discovery** from **protocol-specific decoding**:

```
Spectrum Scanner
      │
      ▼
Signal Detector
      │
      ▼
Parameter Search
      │
      ▼
Demodulator
      │
      ▼
Transport / Data Stream
      │
      ▼
Protocol Parser
      │
      ▼
Discovered Services
```

For DVB, the parameter search differs by delivery system:

| System | Typical discovery dimensions |
| --- | --- |
| DVB-S/S2 | frequency, polarization, symbol rate, DVB-S/S2 mode |
| DVB-T/T2 | frequency, bandwidth, transmission mode, guard interval, constellation |
| DVB-C | frequency, symbol rate, QAM constellation |

A useful implementation therefore models a blind scan as a **search over a parameter space**, rather than hard-coding “scan frequencies.”

The optimization is also important: once one multiplex is found, its **NIT/network information can provide neighboring frequencies and parameters**, allowing the scanner to switch from expensive blind discovery to much faster guided discovery.

<!-- source: Userscript Discovery Prototype.md L114–114 | turn 3 | ChatGPT turn lead-in -->
A good way to formalize this is to treat **blind scanning as constrained hypothesis testing over a physical-channel parameter space**.

<!-- source: Userscript Discovery Prototype.md L116–144 | turn 3 | version ? -->
### 1. Separate the layers

A generic scanner can expose four interfaces:

```
┌──────────────────────────────────────┐
│          Discovery Controller        │
│  scheduling / deduplication / retry  │
└──────────────────┬───────────────────┘
                   │
┌──────────────────▼───────────────────┐
│          Candidate Generator         │
│ frequencies × bandwidth × SR × ...   │
└──────────────────┬───────────────────┘
                   │
┌──────────────────▼───────────────────┐
│         Signal Acquisition            │
│ tune → detect → synchronize → lock   │
└──────────────────┬───────────────────┘
                   │
┌──────────────────▼───────────────────┐
│        Stream / Metadata Parser       │
│ TS → SI/PSI → services → networks    │
└──────────────────────────────────────┘
```

The **candidate generator** is the part that makes the algorithm generic.

---

<!-- source: Userscript Discovery Prototype.md L384–439 | turn 3 | version ? -->
## 7. Generic algorithm

Putting it together:

```
initialize blind search space
initialize guided search queue
initialize discovered database

while search space is not exhausted:

    candidate = select_next_candidate()

    tune(candidate)

    if not detect_signal():
        continue

    hypotheses = characterize_signal(candidate)

    for hypothesis in rank(hypotheses):

        if not acquire(hypothesis):
            continue

        if not validate_transport_stream():
            continue

        protocol = identify_protocol()

        if protocol != DVB:
            continue

        metadata = parse_DVB_metadata()

        multiplex = identify_or_create_multiplex(metadata)

        merge_reception_parameters(
            multiplex,
            hypothesis
        )

        services = enumerate_services()

        merge_services(multiplex, services)

        new_candidates = extract_network_candidates(metadata)

        add_to_guided_queue(new_candidates)

        mark_candidate_successful(candidate)

        break

return discovered_database
```

<!-- source: Userscript Discovery Prototype.md L441–452 | turn 3 | version ? -->
### The key insight

**Blind scanning isn't fundamentally a DVB-specific operation.** DVB-specific knowledge enters at the stages where you:

* characterize candidate RF signals,
* synchronize the appropriate physical layer,
* validate the resulting stream,
* parse DVB PSI/SI metadata.

The higher-level algorithm—**generate hypotheses → test → validate → extract new hypotheses → deduplicate → repeat**—is a generic discovery/search algorithm.

That same architecture can therefore support DVB-S/S2, DVB-T/T2, DVB-C, and potentially completely different broadcast protocols by replacing the protocol-specific acquisition and parsing modules.

<!-- source: Userscript Discovery Prototype.md L739–775 | turn 5 | version ? -->
## 15. The generic discovery abstraction

At this point you can abstract DVB away almost completely:

```
interface DiscoveryProvider:

    generate_initial_candidates()

    detect(candidate)

    characterize(candidate)

    acquire(candidate)

    validate(stream)

    parse_metadata(stream)

    generate_followup_candidates(metadata)
```

Then the generic engine is:

```
DiscoveryEngine
       │
       ├── CandidateStore
       ├── Scheduler
       ├── AcquisitionProvider
       ├── MetadataProvider
       └── DiscoveryDatabase
```

A DVB-T2 implementation and DVB-S2 implementation can provide different acquisition modules while sharing the same scheduler, deduplication, confidence model, persistence, and discovery logic.

That is the point where **“DVB blind scan” becomes a general-purpose discovery algorithm rather than merely a receiver feature**.

<!-- source: Userscript Discovery Prototype.md L1071–1099 | turn 7 | version ? -->
### 23. A useful formal name

If you're designing this as a generic library, I'd avoid naming the core abstraction `DVBBlindScan`.

Something like:

```
DiscoveryEngine
CandidateSpace
AcquisitionStrategy
Observation
Discovery
KnowledgeBase
```

is more reusable.

Then DVB becomes one implementation:

```
DiscoveryEngine
      │
      └── DVBDiscoveryProvider
              ├── DVB-S/S2
              ├── DVB-T/T2
              └── DVB-C
```

The same engine could theoretically host other RF discovery protocols without changing the scheduler or database model.

<!-- source: Userscript Discovery Prototype.md L1378–1429 | turn 9 | version ? -->
## 30. The final abstraction

At the highest level, the algorithm is simply:

```
                ┌──────────────┐
                │ Search Space │
                └──────┬───────┘
                       │
                       ▼
                ┌──────────────┐
                │   Scheduler  │
                └──────┬───────┘
                       │
                       ▼
                ┌──────────────┐
                │   Candidate  │
                └──────┬───────┘
                       │
                       ▼
                ┌──────────────┐
                │  Observation │
                └──────┬───────┘
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
       Not confirmed          Confirmed
             │                   │
             ▼                   ▼
      Refine hypotheses      Parse metadata
             │                   │
             │                   ▼
             │             Create discovery
             │                   │
             └──────────┬────────┘
                        ▼
                 Generate new
                  candidates
                        │
                        ▼
                   Scheduler
```

So the fundamental primitive isn't actually **“scan frequency.”**

It's:

$$\boxed{\text{candidate} \rightarrow \text{observation} \rightarrow \text{evidence} \rightarrow \text{discovery} \rightarrow \text{new candidates}}$$

DVB blind scan is simply one concrete instantiation of that loop.

If you're implementing this in software, the next useful step would be to turn this model into a **concrete state-machine/API design**, including `Candidate`, `Observation`, `Discovery`, scheduler interfaces, retry policy, and DVB-S/S2/T/T2/C adapters.
