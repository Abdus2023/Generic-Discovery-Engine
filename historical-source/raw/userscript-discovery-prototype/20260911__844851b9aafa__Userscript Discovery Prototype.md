> **ARCHIVED SOURCE DOCUMENT**
>
> This document has been mechanically split into the structured
> documentation tree. It is retained for provenance and historical
> traceability.
>
> See [`docs/README.md`](../docs/README.md) and
> [`docs/SOURCE-MAP.md`](../docs/SOURCE-MAP.md).

---

**You:**

DVB blind scan as a generic discovery algorithm

* * *

**ChatGPT:**

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

* * *

**You:**

Continue

* * *

**ChatGPT:**

A good way to formalize this is to treat **blind scanning as constrained hypothesis testing over a physical-channel parameter space**.

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

## 3. Detection should precede expensive decoding

A naïve blind scanner tries every possible demodulator configuration. That can become extremely expensive.

A better pipeline is:

```
RF energy?
   │
   ├── no → next candidate
   │
   └── yes
        │
        ▼
rough signal characterization
        │
        ▼
candidate parameter ranking
        │
        ▼
demodulation attempts
```

So instead of testing 100 possible symbol rates equally, you can estimate a likely symbol rate or occupied bandwidth and test the most probable candidates first.

Conceptually:

```
score(candidate) =
    w1 × signal_strength
  + w2 × bandwidth_match
  + w3 × timing_consistency
  + w4 × synchronization_score
```

Then attempt candidates in descending score order.

---

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

### The key insight

**Blind scanning isn't fundamentally a DVB-specific operation.** DVB-specific knowledge enters at the stages where you:

* characterize candidate RF signals,
* synchronize the appropriate physical layer,
* validate the resulting stream,
* parse DVB PSI/SI metadata.

The higher-level algorithm—**generate hypotheses → test → validate → extract new hypotheses → deduplicate → repeat**—is a generic discovery/search algorithm.

That same architecture can therefore support DVB-S/S2, DVB-T/T2, DVB-C, and potentially completely different broadcast protocols by replacing the protocol-specific acquisition and parsing modules.

* * *

**You:**

Continue

* * *

**ChatGPT:**

The next step is to make the scanner **adaptive** rather than a simple nested loop. That gives you something closer to a reusable discovery engine.

### 8. Model scanning as a search problem

Define the complete search space as:

$$X = F \times P \times B \times R \times M \times D$$

where, conceptually:

* $F$ = frequencies
* $P$ = physical-layer parameters
* $B$ = bandwidth-related parameters
* $R$ = symbol-rate-related parameters
* $M$ = modulation/coding hypotheses
* $D$ = delivery-system hypotheses

A blind scan seeks a subset:

$$X^* \subseteq X$$

for which the receiver obtains a **validated multiplex**.

The important part is that you don't necessarily enumerate all of $X$. You progressively eliminate impossible regions.

---

## 9. Coarse-to-fine search

A particularly useful pattern is:

```
                    Whole spectrum
                          │
                          ▼
                 coarse energy scan
                          │
             ┌────────────┴────────────┐
             │                         │
          no energy                 candidate
             │                         │
             ▼                         ▼
          discard              characterize
                                       │
                                       ▼
                              parameter hypotheses
                                       │
                                       ▼
                                demodulator test
                                       │
                              ┌────────┴────────┐
                              │                 │
                            fail              lock
                              │                 │
                              ▼                 ▼
                           discard        validate TS
                                                │
                                                ▼
                                          parse metadata
```

This matters because the cost of an RF measurement can be substantially lower than the cost of repeatedly initializing a full demodulator.

---

## 10. Confidence rather than binary decisions

Instead of immediately saying:

```
found / not found
```

maintain a confidence score.

For example:

```
CandidateConfidence {
    energy_score
    timing_score
    carrier_score
    synchronization_score
    FEC_score
    transport_score
    metadata_score
}
```

Then define stages:

```
confidence < T1
    → ignore

T1 ≤ confidence < T2
    → investigate

T2 ≤ confidence < T3
    → demodulate

confidence ≥ T3
    → confirmed
```

This is particularly useful near weak signals, where a single measurement may be ambiguous.

---

## 11. Don't immediately discard failed candidates

A failed demodulation attempt can mean several things:

```
Candidate
   │
   ├── wrong frequency
   ├── wrong bandwidth
   ├── wrong symbol rate
   ├── wrong modulation
   ├── wrong delivery system
   ├── insufficient signal
   └── valid signal but acquisition timeout
```

Those failures have different meanings.

Therefore record the reason:

```
AttemptResult {
    candidate
    elapsed_time
    signal_present
    lock_state
    failure_reason
}
```

This allows the scheduler to make better decisions.

For example, repeated:

```
signal_present = true
carrier_lock = true
FEC_lock = false
```

suggests that the frequency is probably interesting, but the current physical-layer hypothesis is wrong.

---

## 12. Adaptive retry

The scanner can then expand locally:

```
candidate failed
       │
       ▼
Was there RF energy?
       │
   ┌───┴───┐
   no      yes
   │        │
   ▼        ▼
discard   generate neighboring hypotheses
```

For example, conceptually:

```
failed symbol-rate hypothesis
        │
        ├── test nearby SR values
        ├── test alternative modulation
        └── test alternative DVB mode
```

This is better than globally trying every combination.

---

## 13. Scheduling becomes important

You can give every pending candidate a priority:

$$priority(c) = P(\text{valid}\mid c) \times value(c) \div cost(c)$$

Where:

* **probability** = how likely the candidate is to contain a valid multiplex
* **value** = how useful discovering it is
* **cost** = expected acquisition time

A candidate learned from an NIT would normally receive a much higher probability than an arbitrary point in the spectrum.

So your queues might look like:

```
Priority queue

1. NIT-derived candidate
2. Previously successful neighboring frequency
3. Strong RF candidate
4. Weak RF candidate
5. Uncharacterized spectrum
```

This turns blind scanning into an **active search algorithm**.

---

## 14. Discovery database

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

* * *

**You:**

Continue

* * *

**ChatGPT:**

The natural next step is to define **what constitutes a successful discovery** and how the algorithm terminates. This is where a blind scanner becomes deterministic enough to implement.

### 16. Discovery should have evidence levels

Rather than treating discovery as a single event, attach evidence to it:

```
EvidenceLevel 0
    no signal

EvidenceLevel 1
    RF energy detected

EvidenceLevel 2
    physical-layer synchronization

EvidenceLevel 3
    valid transport stream

EvidenceLevel 4
    DVB PSI/SI validated

EvidenceLevel 5
    one or more services enumerated
```

A scanner can report only level 4/5 as a real DVB discovery, while retaining lower-level observations for diagnostics.

This gives you a useful distinction between:

> "There appears to be a carrier here."

and:

> "There is a confirmed DVB multiplex here containing these services."

---

## 17. Use observations to update the search space

The algorithm can be expressed as a loop over **beliefs**:

```
SearchSpace
     │
     ▼
Candidate
     │
     ▼
Observation
     │
     ▼
Update belief
     │
     ├──────────────┐
     ▼              ▼
Confirmed       New candidates
     │              │
     │              └──────► SearchSpace
     ▼
Discovery DB
```

Formally:

$$S_{n+1}=S_n-\{c_n\}+\operatorname{Expand}(o_n)$$

where:

* $S_n$ is the remaining search space,
* $c_n$ is the candidate just tested,
* $o_n$ is the observation,
* `Expand()` generates candidates suggested by that observation.

This is a very general pattern and isn't specific to DVB.

---

## 18. Termination

A blind scan should not simply stop after finding the first multiplex.

Typical termination conditions are:

### Exhaustive scan

Stop when:

```
all candidates have been evaluated
```

This gives the strongest claim:

> "Everything in the configured search space was examined."

### Confidence-based scan

Stop when:

```
remaining candidates have probability < threshold
```

This is faster but no longer guarantees exhaustive discovery.

### Time-bounded scan

Stop after:

```
scan_time >= configured_budget
```

Useful for receivers that need to remain responsive.

### Hybrid

A practical implementation can do:

```
1. Perform coarse scan.
2. Fully investigate strong candidates.
3. Follow network metadata.
4. Return to unexplored spectrum.
5. Stop when coverage reaches the requested level.
```

---

## 19. Coverage is a better metric than elapsed time

You can track:

$$coverage = \frac{\text{search space sufficiently evaluated}} {\text{configured search space}}$$

For example:

```
Spectrum coverage:       92%
Physical hypotheses:     87%
Confirmed multiplexes:   14
Services discovered:    126
```

This makes the scanner's result reproducible.

A result can then say:

```
SCAN COMPLETE
Coverage: 100%
Confirmed multiplexes: 14
Services: 126
```

rather than simply:

```
Scan finished.
```

---

## 20. Cache knowledge between scans

A major optimization is to persist previous observations.

Suppose yesterday the scanner found:

```
frequency X → DVB-T2 multiplex
frequency Y → empty
frequency Z → DVB-T multiplex
```

On the next scan, you don't need to treat the entire spectrum as equally unknown.

Maintain a knowledge store:

```
ObservationHistory {
    candidate
    result
    timestamp
    signal_quality
    stability
}
```

Then the next scan becomes:

```
known-good candidates
        ↓
known-neighbor candidates
        ↓
new/changed spectrum
        ↓
full blind search
```

This produces a **continuous discovery system**, rather than repeatedly performing the same expensive blind scan.

---

## 21. Handle disappearing multiplexes

Discovery should also be able to represent negative information.

For example:

```
Multiplex X
    previously seen: 17 times
    currently seen: 0 times
```

Don't immediately delete it.

Instead:

```
ACTIVE
  ↓
NOT_SEEN_ONCE
  ↓
NOT_SEEN_REPEATEDLY
  ↓
STALE
  ↓
REMOVED
```

That prevents transient reception problems from being interpreted as network changes.

---

## 22. The complete conceptual algorithm

You can now describe the whole thing compactly:

```
initialize knowledge base
initialize search space
initialize candidate priority queue

while termination_condition_not_met:

    candidate = scheduler.select()

    observation = acquire_and_measure(candidate)

    knowledge.update(observation)

    if observation.contains_valid_DVB_stream:

        metadata = parse_PSI_SI(observation.stream)

        discovery = normalize(metadata, observation)

        database.merge(discovery)

        candidates = derive_candidates(metadata)

        scheduler.add(candidates, high_priority)

    else:

        candidates = refine_hypothesis(candidate, observation)

        scheduler.add(candidates, calculated_priority)

    update_coverage()

return database + coverage + observations
```

The key architectural principle is:

> **Every observation can either confirm a discovery or generate better hypotheses for future discovery.**

That is what distinguishes a robust blind scanner from a simple frequency loop.

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

* * *

**You:**

Continue

* * *

**ChatGPT:**

There is one more useful abstraction: **separate “where to look” from “how to recognize what you found.”** That lets the same discovery engine work with different tuners, demodulators, and protocols.

## 24. Two-dimensional discovery

Think of the problem as:

$$\text{Discovery} = \text{Search Strategy} + \text{Recognition Strategy}$$

The search strategy answers:

> Which candidate should I investigate next?

The recognition strategy answers:

> What evidence would convince me that this candidate contains something meaningful?

For DVB:

```
             Discovery Engine
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
 Search Strategy          Recognition Strategy
        │                       │
 frequency              RF detection
 bandwidth              synchronization
 symbol rate            FEC
 modulation             transport stream
                        PSI/SI
```

That distinction makes the architecture much cleaner.

---

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

## 26. Discovery becomes a graph

Once you preserve those relationships, the scan naturally forms a graph:

```
                 Network A
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
        TS 1       TS 2       TS 3
          │          │
       services   services
          │
          ▼
    RF observation
```

But there can also be discovery edges:

```
RF observation
      │
      └──► candidate
                │
                └──► multiplex
```

and metadata-derived edges:

```
Multiplex A
      │
      └── NIT ──► Multiplex B
```

So the scanner is effectively constructing a **knowledge graph of the RF environment**.

---

## 27. This helps with incremental scanning

Imagine a receiver is continuously monitoring an area.

Instead of:

```
scan everything
wait
scan everything again
wait
...
```

use:

```
             Knowledge Base
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
Known candidates         Unknown regions
        │                     │
   quick verification     blind discovery
        │                     │
        └──────────┬──────────┘
                   ▼
             Updated KB
```

Now the algorithm can detect:

* newly appearing multiplexes,
* disappeared multiplexes,
* changed parameters,
* changed service metadata.

That is much closer to a **generic discovery service** than a traditional one-shot blind scan.

---

## 28. Parameter provenance

For a serious implementation, every parameter should have provenance.

Instead of storing:

```
frequency = X
```

store:

```
frequency = X
source = measured
confidence = high
```

Or:

```
frequency = X
source = NIT
confidence = medium
```

Or:

```
frequency = X
source = user_configuration
confidence = high
```

This allows conflicting information to coexist without corrupting the database.

For example:

```
frequency:
    measured → X
    NIT      → Y
```

The engine can then decide whether this represents:

* a network change,
* a measurement error,
* two different receptions,
* or stale metadata.

---

## 29. The scanner should produce an explanation

A particularly useful design feature is an **explainable discovery result**.

Instead of:

```
DVB multiplex found
```

return something conceptually like:

```
Discovery:
    type: DVB multiplex
    confidence: high

Evidence:
    RF energy detected
    carrier synchronized
    FEC synchronized
    valid MPEG transport stream
    PAT validated
    PMT validated
    DVB SI tables decoded

Origin:
    initially discovered by blind scan

Follow-up:
    additional candidates obtained from NIT
```

This is invaluable when diagnosing why a receiver found—or failed to find—something.

---

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

* * *

**You:**

Continue

* * *

**ChatGPT:**

Yes. The next layer is to make the abstraction **implementable without coupling the discovery engine to DVB hardware**.

## 31. Define the core objects

A clean model has five primary objects:

```
Candidate
Observation
LockResult
Discovery
Evidence
```

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

### Discovery

A discovery is the normalized result:

```
Discovery {
    identity
    protocol
    physical_parameters
    logical_parameters
    services
    evidence
}
```

The discovery should be independent of the particular tuner API that produced it.

---

## 32. Use capability-driven adapters

The generic engine shouldn't know how to tune a specific chipset.

Instead:

```
DiscoveryEngine
      │
      ▼
AcquisitionAdapter
      │
      ├── DVB-S/S2 adapter
      ├── DVB-T/T2 adapter
      └── DVB-C adapter
```

An adapter exposes operations conceptually like:

```
probe(candidate)
acquire(candidate)
measure()
read_stream()
release()
```

The engine doesn't care whether the underlying implementation is:

* a hardware tuner,
* an SDR,
* a kernel driver,
* a networked tuner,
* or a simulator.

That is a major architectural advantage.

---

## 33. Discovery strategies should also be pluggable

The acquisition side is only half the abstraction.

You can have:

```
CandidateStrategy
    ├── ExhaustiveGrid
    ├── EnergyPeakSearch
    ├── NetworkGuided
    ├── Historical
    └── Hybrid
```

A hybrid strategy is probably the most useful:

```
                Candidate Scheduler
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
    NIT-derived    historical       blind
      60%            20%             20%
```

The exact proportions shouldn't be hard-coded; the scheduler should dynamically adjust priority.

---

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

## 37. Candidate provenance creates a discovery tree

Suppose a blind scan finds A.

A's metadata points to B and C.

B points to D.

You get:

```
Blind scan
    │
    ▼
    A
   / \
  B   C
  │
  D
```

Now the system knows **why** it found D.

That allows you to distinguish:

```
D found through network metadata
```

from:

```
D independently found through blind RF search
```

The latter is useful corroborating evidence.

---

## 38. Avoid infinite candidate generation

Metadata can potentially produce candidates you've already investigated.

So the scheduler needs canonicalization:

```
canonicalize(candidate)
```

followed by:

```
if candidate already known:
    merge evidence
else:
    enqueue
```

You can think of this as maintaining a visited set:

$$V = \{\operatorname{canonical}(c)\}$$

Without this, a network graph can repeatedly enqueue the same frequencies.

---

## 39. A practical scheduler

The scheduler can maintain three collections:

```
READY
    candidates eligible for acquisition

DEFERRED
    candidates worth testing later

DONE
    candidates sufficiently investigated
```

And each candidate has a priority:

```
priority =
    discovery_probability
    × information_value
    × freshness
    ÷ acquisition_cost
```

That gives you a principled way to choose the next candidate.

---

## 40. The engine can now become event-driven

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

## 41. The resulting architecture

You end up with something like:

```
                         ┌──────────────────┐
                         │  Discovery API   │
                         └────────┬─────────┘
                                  │
                         ┌────────▼─────────┐
                         │ Discovery Engine │
                         └────────┬─────────┘
                                  │
               ┌──────────────────┼──────────────────┐
               ▼                  ▼                  ▼
        ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
        │  Scheduler  │    │  Knowledge  │    │  Event Bus  │
        │             │    │    Base     │    │             │
        └──────┬──────┘    └─────────────┘    └─────────────┘
               │
               ▼
        ┌─────────────┐
        │ Acquisition │
        │   Adapter   │
        └──────┬──────┘
               │
       ┌───────┴────────┐
       ▼                ▼
    DVB-S/S2          DVB-T/T2
       │                │
       └───────┬────────┘
               ▼
        ┌─────────────┐
        │   Metadata  │
        │   Parsers   │
        └──────┬──────┘
               │
               ▼
        ┌─────────────┐
        │ Discoveries │
        └─────────────┘
```

At this point, **blind scanning is just one strategy plugged into a general discovery engine**.

The really interesting consequence is that the same engine can support **continuous spectrum discovery**: initial blind scan → network-guided expansion → periodic verification → change detection → incremental rescan.

* * *

**You:**

A Generic Discovery Algorithm Inspered by DVB Blind Scan

==> Userscript

* * *

**ChatGPT:**

Yes — if the goal is to turn the **DVB-inspired discovery model into a browser userscript**, a good interpretation is:

> Treat elements/URLs/resources in the current web application as the “spectrum,” generate candidates, probe them, validate what is found, extract metadata, and recursively discover additional candidates.

Below is a self-contained **Tampermonkey/Greasemonkey userscript** implementing that architecture. It is deliberately generic: it doesn't assume a particular website or API.

// ==UserScript==  
// @name Generic Discovery Engine  
// @namespace generic-discovery  
// @version 0.1.0  
// @description A DVB-blind-scan-inspired discovery engine for browser userscripts.  
// @match _://_/*  
// @grant GM_getValue  
// @grant GM_setValue  
// @grant GM_xmlhttpRequest  
// @connect *  
// ==/UserScript==

(() => {  
'use strict';

```
/*
 * ================================================================
 * Generic Discovery Engine
 * ================================================================
 *
 * Concept:
 *
 *     candidate
 *         ↓
 *     observation
 *         ↓
 *     validation
 *         ↓
 *     discovery
 *         ↓
 *     new candidates
 *         ↓
 *     scheduler
 *
 * Inspired by DVB blind scanning, but independent of DVB.
 *
 * This implementation discovers:
 *
 *   - links
 *   - same-origin resources
 *   - URLs found in HTML
 *   - metadata-derived URLs
 *
 * It maintains:
 *
 *   - candidate queue
 *   - visited set
 *   - observations
 *   - discoveries
 *   - provenance
 *   - confidence
 */

const CONFIG = {
    maxCandidates: 500,
    maxRequests: 100,
    concurrency: 3,

    requestTimeout: 8000,

    sameOriginOnly: true,

    discoverLinks: true,
    discoverResources: true,
    discoverFromHtml: true,

    persistState: true,

    debug: true
};

// ---------------------------------------------------------------
// Utilities
// ---------------------------------------------------------------

const log = (...args) => {
    if (CONFIG.debug) {
        console.log('[Discovery]', ...args);
    }
};

const warn = (...args) => {
    console.warn('[Discovery]', ...args);
};

function canonicalizeUrl(value) {
    try {
        const url = new URL(value, location.href);

        url.hash = '';

        // Normalize the trailing slash for the root only.
        if (url.pathname === '/') {
            url.pathname = '/';
        }

        return url.href;
    } catch {
        return null;
    }
}

function isAllowedUrl(url) {
    if (!url) {
        return false;
    }

    if (!CONFIG.sameOriginOnly) {
        return true;
    }

    try {
        return new URL(url).origin === location.origin;
    } catch {
        return false;
    }
}

function now() {
    return Date.now();
}

function makeId(prefix = 'id') {
    return `${prefix}-${now()}-${Math.random().toString(36).slice(2, 9)}`;
}

// ---------------------------------------------------------------
// Candidate
// ---------------------------------------------------------------

class Candidate {
    constructor({
        target,
        type = 'url',
        origin = 'unknown',
        priority = 0.5,
        parent = null,
        hints = {}
    }) {
        this.id = makeId('candidate');
        this.target = target;
        this.type = type;
        this.origin = origin;
        this.priority = priority;
        this.parent = parent;
        this.hints = hints;

        this.createdAt = now();
        this.attempts = 0;
        this.status = 'queued';
    }

    key() {
        return `${this.type}:${this.target}`;
    }
}

// ---------------------------------------------------------------
// Observation
// ---------------------------------------------------------------

class Observation {
    constructor(candidate) {
        this.id = makeId('observation');

        this.candidateId = candidate.id;
        this.target = candidate.target;

        this.startedAt = now();
        this.completedAt = null;

        this.signalPresent = false;

        this.status = 'unknown';

        this.http = {
            status: null,
            contentType: null,
            contentLength: null
        };

        this.features = {};
        this.errors = [];
    }

    complete(status = 'complete') {
        this.completedAt = now();
        this.status = status;
    }
}

// ---------------------------------------------------------------
// Discovery
// ---------------------------------------------------------------

class Discovery {
    constructor({
        candidate,
        observation,
        kind,
        confidence = 0.5,
        data = {}
    }) {
        this.id = makeId('discovery');

        this.candidateId = candidate.id;
        this.observationId = observation.id;

        this.kind = kind;
        this.confidence = confidence;

        this.data = data;

        this.provenance = {
            origin: candidate.origin,
            parent: candidate.parent
        };

        this.createdAt = now();
    }
}

// ---------------------------------------------------------------
// Knowledge Base
// ---------------------------------------------------------------

class KnowledgeBase {
    constructor() {
        this.candidates = new Map();
        this.observations = new Map();
        this.discoveries = new Map();
        this.visited = new Set();

        this.load();
    }

    candidateKey(candidate) {
        return candidate.key();
    }

    hasCandidate(candidate) {
        return this.candidates.has(this.candidateKey(candidate));
    }

    addCandidate(candidate) {
        const key = this.candidateKey(candidate);

        if (this.visited.has(key)) {
            return false;
        }

        if (this.candidates.has(key)) {
            return false;
        }

        if (this.candidates.size >= CONFIG.maxCandidates) {
            return false;
        }

        this.candidates.set(key, candidate);

        this.persist();

        return true;
    }

    markVisited(candidate) {
        const key = this.candidateKey(candidate);

        this.visited.add(key);
        this.candidates.delete(key);

        this.persist();
    }

    addObservation(observation) {
        this.observations.set(observation.id, observation);
        this.persist();
    }

    addDiscovery(discovery) {
        this.discoveries.set(discovery.id, discovery);
        this.persist();
    }

    serialize() {
        return {
            visited: [...this.visited],
            discoveries: [...this.discoveries.values()]
        };
    }

    persist() {
        if (!CONFIG.persistState) {
            return;
        }

        try {
            const data = this.serialize();

            if (typeof GM_setValue === 'function') {
                GM_setValue('discovery-state', JSON.stringify(data));
            } else {
                localStorage.setItem(
                    'generic-discovery-state',
                    JSON.stringify(data)
                );
            }
        } catch (error) {
            warn('Persistence failed:', error);
        }
    }

    load() {
        if (!CONFIG.persistState) {
            return;
        }

        try {
            let raw = null;

            if (typeof GM_getValue === 'function') {
                raw = GM_getValue('discovery-state', null);
            } else {
                raw = localStorage.getItem(
                    'generic-discovery-state'
                );
            }

            if (!raw) {
                return;
            }

            const data =
                typeof raw === 'string'
                    ? JSON.parse(raw)
                    : raw;

            for (const key of data.visited || []) {
                this.visited.add(key);
            }

            for (const discovery of data.discoveries || []) {
                this.discoveries.set(
                    discovery.id,
                    discovery
                );
            }
        } catch (error) {
            warn('Could not restore discovery state:', error);
        }
    }

    clear() {
        this.candidates.clear();
        this.observations.clear();
        this.discoveries.clear();
        this.visited.clear();

        this.persist();
    }
}

// ---------------------------------------------------------------
// Candidate Scheduler
// ---------------------------------------------------------------

class Scheduler {
    constructor(database) {
        this.database = database;
    }

    add(candidate) {
        return this.database.addCandidate(candidate);
    }

    next() {
        const candidates = [
            ...this.database.candidates.values()
        ];

        if (!candidates.length) {
            return null;
        }

        // Highest priority first.
        candidates.sort((a, b) => {
            return b.priority - a.priority;
        });

        return candidates[0];
    }

    size() {
        return this.database.candidates.size;
    }
}

// ---------------------------------------------------------------
// Acquisition Adapter
// ---------------------------------------------------------------

class HttpAcquisitionAdapter {
    async acquire(candidate) {
        const observation = new Observation(candidate);

        candidate.attempts++;

        try {
            const response = await this.request(
                candidate.target
            );

            observation.signalPresent = true;

            observation.http.status =
                response.status;

            observation.http.contentType =
                response.contentType;

            observation.http.contentLength =
                response.body?.length || 0;

            observation.features.body =
                response.body;

            observation.complete('acquired');

            return observation;

        } catch (error) {
            observation.errors.push(
                String(error)
            );

            observation.complete('failed');

            return observation;
        }
    }

    request(url) {
        return new Promise((resolve, reject) => {

            // Prefer GM_xmlhttpRequest when available.
            if (typeof GM_xmlhttpRequest === 'function') {

                GM_xmlhttpRequest({
                    method: 'GET',
                    url,

                    timeout: CONFIG.requestTimeout,

                    onload: response => {
                        resolve({
                            status: response.status,
                            contentType:
                                response.responseHeaders
                                    ?.match(/content-type:\s*([^\r\n]+)/i)
                                    ?.[1] || null,
                            body: response.responseText
                        });
                    },

                    onerror: () => {
                        reject(
                            new Error('request failed')
                        );
                    },

                    ontimeout: () => {
                        reject(
                            new Error('request timeout')
                        );
                    }
                });

                return;
            }

            fetch(url, {
                credentials: 'same-origin',
                signal: AbortSignal.timeout(
                    CONFIG.requestTimeout
                )
            })
                .then(async response => ({
                    status: response.status,
                    contentType:
                        response.headers.get(
                            'content-type'
                        ),
                    body: await response.text()
                }))
                .then(resolve)
                .catch(reject);
        });
    }
}

// ---------------------------------------------------------------
// Validator / Recognizer
// ---------------------------------------------------------------

class HtmlRecognizer {

    recognize(candidate, observation) {

        if (
            observation.status !== 'acquired' ||
            !observation.features.body
        ) {
            return null;
        }

        const body = observation.features.body;

        const contentType =
            observation.http.contentType || '';

        const looksLikeHtml =
            contentType.includes('text/html') ||
            /<html[\s>]/i.test(body) ||
            /<body[\s>]/i.test(body);

        if (!looksLikeHtml) {
            return null;
        }

        const document =
            new DOMParser().parseFromString(
                body,
                'text/html'
            );

        const title =
            document.querySelector('title')
                ?.textContent
                ?.trim() || '';

        const links = [
            ...document.querySelectorAll(
                'a[href]'
            )
        ]
            .map(a =>
                canonicalizeUrl(a.href)
            )
            .filter(Boolean)
            .filter(isAllowedUrl);

        const resources = [
            ...document.querySelectorAll(
                'script[src],link[href],img[src]'
            )
        ]
            .map(el =>
                el.src ||
                el.href ||
                null
            )
            .filter(Boolean)
            .map(canonicalizeUrl)
            .filter(Boolean)
            .filter(isAllowedUrl);

        return new Discovery({
            candidate,
            observation,

            kind: 'html-document',

            confidence: 0.95,

            data: {
                url: candidate.target,
                title,
                links,
                resources
            }
        });
    }
}

// ---------------------------------------------------------------
// Candidate Extraction
// ---------------------------------------------------------------

class CandidateExtractor {

    fromDocument(document, origin = 'dom') {

        const result = [];

        if (CONFIG.discoverLinks) {

            for (const element of
                document.querySelectorAll(
                    'a[href]'
                )) {

                const url =
                    canonicalizeUrl(
                        element.href
                    );

                if (!isAllowedUrl(url)) {
                    continue;
                }

                result.push(
                    new Candidate({
                        target: url,
                        type: 'url',
                        origin,
                        priority: 0.6
                    })
                );
            }
        }

        if (CONFIG.discoverResources) {

            for (const element of
                document.querySelectorAll(
                    'script[src],link[href],img[src]'
                )) {

                const url =
                    canonicalizeUrl(
                        element.src ||
                        element.href
                    );

                if (!isAllowedUrl(url)) {
                    continue;
                }

                result.push(
                    new Candidate({
                        target: url,
                        type: 'resource',
                        origin,
                        priority: 0.4
                    })
                );
            }
        }

        return result;
    }

    fromDiscovery(discovery) {

        const result = [];

        for (const url of
            discovery.data.links || []) {

            result.push(
                new Candidate({
                    target: url,
                    type: 'url',
                    origin: `discovery:${discovery.id}`,
                    priority: 0.8,
                    parent: discovery.id
                })
            );
        }

        for (const url of
            discovery.data.resources || []) {

            result.push(
                new Candidate({
                    target: url,
                    type: 'resource',
                    origin: `discovery:${discovery.id}`,
                    priority: 0.5,
                    parent: discovery.id
                })
            );
        }

        return result;
    }
}

// ---------------------------------------------------------------
// Discovery Engine
// ---------------------------------------------------------------

class DiscoveryEngine {

    constructor() {

        this.database =
            new KnowledgeBase();

        this.scheduler =
            new Scheduler(this.database);

        this.acquisition =
            new HttpAcquisitionAdapter();

        this.recognizer =
            new HtmlRecognizer();

        this.extractor =
            new CandidateExtractor();

        this.running = false;

        this.stats = {
            startedAt: null,
            requests: 0,
            candidates: 0,
            discoveries: 0,
            failures: 0
        };
    }

    seed() {

        const current =
            canonicalizeUrl(
                location.href
            );

        if (current) {

            this.scheduler.add(
                new Candidate({
                    target: current,
                    type: 'url',
                    origin: 'initial-page',
                    priority: 1.0
                })
            );
        }

        // Discover what is already present in the page.
        const candidates =
            this.extractor.fromDocument(
                document,
                'initial-dom'
            );

        for (const candidate of candidates) {
            this.scheduler.add(candidate);
        }

        this.stats.candidates =
            this.scheduler.size();
    }

    async run() {

        if (this.running) {
            return;
        }

        this.running = true;

        this.stats.startedAt = now();

        log('Starting discovery');

        const workers = [];

        for (
            let i = 0;
            i < CONFIG.concurrency;
            i++
        ) {
            workers.push(
                this.worker(i)
            );
        }

        await Promise.all(workers);

        this.running = false;

        log(
            'Discovery complete',
            this.stats
        );

        this.report();
    }

    async worker(id) {

        while (
            this.running &&
            this.stats.requests <
                CONFIG.maxRequests
        ) {

            const candidate =
                this.scheduler.next();

            if (!candidate) {
                break;
            }

            this.database.markVisited(
                candidate
            );

            log(
                `Worker ${id}:`,
                candidate.target
            );

            this.stats.requests++;

            const observation =
                await this.acquisition.acquire(
                    candidate
                );

            this.database.addObservation(
                observation
            );

            if (
                observation.status !==
                'acquired'
            ) {
                this.stats.failures++;
                continue;
            }

            const discovery =
                this.recognizer.recognize(
                    candidate,
                    observation
                );

            if (!discovery) {
                continue;
            }

            this.database.addDiscovery(
                discovery
            );

            this.stats.discoveries++;

            // Discovery expands the search space.
            const newCandidates =
                this.extractor
                    .fromDiscovery(
                        discovery
                    );

            for (const next of newCandidates) {
                this.scheduler.add(next);
            }
        }
    }

    report() {

        const discoveries =
            [...this.database.discoveries.values()];

        console.group(
            '[Discovery] Results'
        );

        console.table(
            discoveries.map(d => ({
                kind: d.kind,
                confidence: d.confidence,
                url: d.data.url,
                title: d.data.title
            }))
        );

        console.log(
            'Statistics:',
            this.stats
        );

        console.groupEnd();
    }

    export() {

        return {
            version: 1,

            timestamp:
                new Date().toISOString(),

            page:
                location.href,

            statistics:
                this.stats,

            discoveries:
                [...this.database
                    .discoveries
                    .values()]
        };
    }

    clear() {
        this.database.clear();
    }
}

// ---------------------------------------------------------------
// UI
// ---------------------------------------------------------------

const engine =
    new DiscoveryEngine();

window.GenericDiscovery =
    engine;

const panel =
    document.createElement('div');

panel.style.cssText = `
    position: fixed;
    right: 12px;
    bottom: 12px;
    z-index: 2147483647;
    background: rgba(20,20,20,.94);
    color: white;
    padding: 10px;
    border-radius: 8px;
    font: 12px monospace;
    box-shadow: 0 3px 15px rgba(0,0,0,.4);
`;

panel.innerHTML = `
    <div style="margin-bottom:6px">
        <strong>Discovery</strong>
    </div>

    <button id="gd-start">
        Scan
    </button>

    <button id="gd-clear">
        Clear
    </button>

    <button id="gd-export">
        Export
    </button>

    <div id="gd-status"
         style="margin-top:6px">
        idle
    </div>
`;

document.documentElement.appendChild(panel);

const status =
    panel.querySelector('#gd-status');

panel.querySelector('#gd-start')
    .addEventListener('click', async () => {

        status.textContent = 'scanning...';

        engine.seed();

        await engine.run();

        status.textContent =
            `done — ${engine.stats.discoveries} discoveries`;
    });

panel.querySelector('#gd-clear')
    .addEventListener('click', () => {

        engine.clear();

        status.textContent =
            'cleared';
    });

panel.querySelector('#gd-export')
    .addEventListener('click', () => {

        const data =
            engine.export();

        const blob =
            new Blob(
                [JSON.stringify(data, null, 2)],
                { type: 'application/json' }
            );

        const url =
            URL.createObjectURL(blob);

        const a =
            document.createElement('a');

        a.href = url;
        a.download =
            `discovery-${Date.now()}.json`;

        a.click();

        URL.revokeObjectURL(url);
    });
```

})();  
::

The important part is that this **isn't really a “web crawler” disguised as a DVB scanner**. Its architecture deliberately follows the model we developed:

```
                    ┌─────────────────┐
                    │ Search Space    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Scheduler     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    Candidate    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Acquisition   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Observation   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Recognizer    │
                    └────────┬────────┘
                             │
                       ┌─────┴─────┐
                       ▼           ▼
                  rejected     Discovery
                                   │
                                   ▼
                            New Candidates
                                   │
                                   └──────► Scheduler
```

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

* * *

**You:**

Fix concurrent candidate claiming
Add non-HTML response providers
Clarify the prototype's actual scope

* * *

**ChatGPT:**

Agreed. The prototype needs three corrections:

1. **Candidate claiming must be explicit** so workers cannot independently select the same queued candidate.
2. **Recognition must be provider-based**, rather than assuming every successful response is HTML.
3. The script should explicitly say what it **does and does not** implement: it is a web-resource discovery prototype inspired by the _architecture_ of DVB blind scanning, not an RF/DVB scanner.

Here is the revised version.

// ==UserScript==  
// @name Generic Discovery Engine  
// @namespace generic-discovery  
// @version 0.2.0  
// @description Generic web-resource discovery prototype inspired by the architecture of DVB blind scanning.  
// @match _://_/*  
// @grant GM_getValue  
// @grant GM_setValue  
// @grant GM_xmlhttpRequest  
// @connect *  
// ==/UserScript==

(() => {  
'use strict';

```
/*
 * =====================================================================
 * GENERIC DISCOVERY ENGINE
 * =====================================================================
 *
 * PURPOSE
 * -------
 * This is a browser-side discovery prototype inspired by the
 * architecture of DVB blind scanning:
 *
 *      candidate
 *          ↓
 *      observation
 *          ↓
 *      recognition
 *          ↓
 *      discovery
 *          ↓
 *      new candidates
 *          ↓
 *      scheduler
 *
 * IMPORTANT SCOPE
 * ---------------
 * This script is NOT a DVB/RF scanner.
 *
 * It does not:
 *   - access RF hardware
 *   - tune DVB frequencies
 *   - perform carrier synchronization
 *   - perform DVB FEC synchronization
 *   - demodulate DVB-S/S2/T/T2/C
 *
 * Instead, it applies the same discovery architecture to WEB
 * resources available to the browser:
 *
 *   URL → HTTP response → provider → discovered metadata → new URLs
 *
 * Supported response providers in this prototype:
 *
 *   - HTML
 *   - JSON
 *   - plain text
 *
 * The architecture is intentionally extensible.
 *
 * =====================================================================
 */

const CONFIG = {
    maxCandidates: 500,
    maxRequests: 100,

    // Number of simultaneous acquisitions.
    concurrency: 3,

    requestTimeout: 8000,

    sameOriginOnly: true,

    discoverLinks: true,
    discoverResources: true,

    persistState: true,

    debug: true
};

// =====================================================================
// Utility
// =====================================================================

const log = (...args) => {
    if (CONFIG.debug) {
        console.log('[Discovery]', ...args);
    }
};

const warn = (...args) => {
    console.warn('[Discovery]', ...args);
};

const now = () => Date.now();

function makeId(prefix) {
    return `${prefix}-${now()}-${Math.random()
        .toString(36)
        .slice(2, 9)}`;
}

function canonicalizeUrl(value) {
    try {
        const url = new URL(value, location.href);

        // Fragments don't identify a separately fetchable resource.
        url.hash = '';

        return url.href;
    } catch {
        return null;
    }
}

function isAllowedUrl(url) {
    if (!url) {
        return false;
    }

    if (!CONFIG.sameOriginOnly) {
        return true;
    }

    try {
        return new URL(url).origin === location.origin;
    } catch {
        return false;
    }
}

// =====================================================================
// Candidate
// =====================================================================

class Candidate {
    constructor({
        target,
        type = 'url',
        origin = 'unknown',
        priority = 0.5,
        parent = null,
        hints = {}
    }) {
        this.id = makeId('candidate');

        this.target = target;
        this.type = type;

        // Why was this candidate created?
        // e.g. initial-dom, html-provider, json-provider
        this.origin = origin;

        // Candidate from which this one was derived.
        this.parent = parent;

        this.priority = priority;
        this.hints = hints;

        this.createdAt = now();

        this.attempts = 0;

        // queued → claimed → completed / failed
        this.status = 'queued';
    }

    key() {
        return `${this.type}:${this.target}`;
    }
}

// =====================================================================
// Observation
// =====================================================================

class Observation {
    constructor(candidate) {
        this.id = makeId('observation');

        this.candidateId = candidate.id;
        this.target = candidate.target;

        this.startedAt = now();
        this.completedAt = null;

        this.status = 'unknown';

        this.signalPresent = false;

        this.http = {
            status: null,
            contentType: null,
            contentLength: null
        };

        this.body = null;

        this.errors = [];
    }

    complete(status) {
        this.completedAt = now();
        this.status = status;
    }
}

// =====================================================================
// Discovery
// =====================================================================

class Discovery {
    constructor({
        candidate,
        observation,
        kind,
        confidence = 0.5,
        data = {}
    }) {
        this.id = makeId('discovery');

        this.candidateId = candidate.id;
        this.observationId = observation.id;

        this.kind = kind;
        this.confidence = confidence;

        this.data = data;

        this.provenance = {
            origin: candidate.origin,
            parent: candidate.parent
        };

        this.createdAt = now();
    }
}

// =====================================================================
// Knowledge Base
// =====================================================================

class KnowledgeBase {

    constructor() {
        this.candidates = new Map();

        this.observations = new Map();

        this.discoveries = new Map();

        /*
         * visited:
         *     candidates permanently completed.
         *
         * claimed:
         *     candidates currently owned by a worker.
         *
         * Keeping claimed separate from visited is important.
         */
        this.visited = new Set();
        this.claimed = new Set();

        this.load();
    }

    candidateKey(candidate) {
        return candidate.key();
    }

    addCandidate(candidate) {

        const key =
            this.candidateKey(candidate);

        if (!candidate.target) {
            return false;
        }

        if (this.visited.has(key)) {
            return false;
        }

        if (this.claimed.has(key)) {
            return false;
        }

        if (this.candidates.has(key)) {
            return false;
        }

        if (
            this.candidates.size >=
            CONFIG.maxCandidates
        ) {
            return false;
        }

        this.candidates.set(key, candidate);

        this.persist();

        return true;
    }

    /*
     * ---------------------------------------------------------------
     * ATOMIC CANDIDATE CLAIM
     * ---------------------------------------------------------------
     *
     * JavaScript executes this synchronous section without another
     * worker being able to interleave an await.
     *
     * A worker therefore:
     *
     *     1. asks for the next candidate
     *     2. candidate is immediately removed from the queue
     *     3. candidate is immediately placed in claimed
     *     4. only then does the worker perform async I/O
     *
     * This prevents two concurrent workers from claiming the same
     * candidate.
     */
    claimNextCandidate() {

        const candidates = [
            ...this.candidates.entries()
        ];

        if (!candidates.length) {
            return null;
        }

        candidates.sort((a, b) => {
            return (
                b[1].priority -
                a[1].priority
            );
        });

        for (const [key, candidate]
            of candidates) {

            if (
                this.visited.has(key) ||
                this.claimed.has(key)
            ) {
                continue;
            }

            /*
             * Claim is synchronous and happens before returning.
             */
            this.candidates.delete(key);

            this.claimed.add(key);

            candidate.status = 'claimed';
            candidate.claimedAt = now();

            this.persist();

            return candidate;
        }

        return null;
    }

    completeCandidate(candidate) {

        const key =
            this.candidateKey(candidate);

        this.claimed.delete(key);
        this.visited.add(key);

        candidate.status = 'completed';
        candidate.completedAt = now();

        this.persist();
    }

    failCandidate(candidate, retry = false) {

        const key =
            this.candidateKey(candidate);

        this.claimed.delete(key);

        if (retry) {
            candidate.status = 'queued';

            this.candidates.set(
                key,
                candidate
            );
        } else {
            this.visited.add(key);
            candidate.status = 'failed';
        }

        this.persist();
    }

    addObservation(observation) {
        this.observations.set(
            observation.id,
            observation
        );

        this.persist();
    }

    addDiscovery(discovery) {
        this.discoveries.set(
            discovery.id,
            discovery
        );

        this.persist();
    }

    queueSize() {
        return this.candidates.size;
    }

    claimedSize() {
        return this.claimed.size;
    }

    serialize() {
        return {
            visited: [...this.visited],

            discoveries: [
                ...this.discoveries.values()
            ]
        };
    }

    persist() {

        if (!CONFIG.persistState) {
            return;
        }

        try {

            const data =
                JSON.stringify(
                    this.serialize()
                );

            if (
                typeof GM_setValue ===
                'function'
            ) {
                GM_setValue(
                    'discovery-state',
                    data
                );
            } else {
                localStorage.setItem(
                    'generic-discovery-state',
                    data
                );
            }

        } catch (error) {
            warn(
                'Persistence failed:',
                error
            );
        }
    }

    load() {

        if (!CONFIG.persistState) {
            return;
        }

        try {

            let raw = null;

            if (
                typeof GM_getValue ===
                'function'
            ) {
                raw = GM_getValue(
                    'discovery-state',
                    null
                );
            } else {
                raw =
                    localStorage.getItem(
                        'generic-discovery-state'
                    );
            }

            if (!raw) {
                return;
            }

            const data =
                typeof raw === 'string'
                    ? JSON.parse(raw)
                    : raw;

            for (
                const key of
                data.visited || []
            ) {
                this.visited.add(key);
            }

            for (
                const discovery of
                data.discoveries || []
            ) {
                this.discoveries.set(
                    discovery.id,
                    discovery
                );
            }

        } catch (error) {
            warn(
                'Could not restore state:',
                error
            );
        }
    }

    clear() {

        this.candidates.clear();
        this.observations.clear();
        this.discoveries.clear();

        this.visited.clear();
        this.claimed.clear();

        this.persist();
    }
}

// =====================================================================
// Acquisition Adapter
// =====================================================================

class HttpAcquisitionAdapter {

    async acquire(candidate) {

        const observation =
            new Observation(candidate);

        candidate.attempts++;

        try {

            const response =
                await this.request(
                    candidate.target
                );

            observation.signalPresent =
                true;

            observation.http.status =
                response.status;

            observation.http.contentType =
                response.contentType;

            observation.http.contentLength =
                response.body?.length || 0;

            observation.body =
                response.body;

            observation.complete(
                'acquired'
            );

        } catch (error) {

            observation.errors.push(
                String(error)
            );

            observation.complete(
                'failed'
            );
        }

        return observation;
    }

    request(url) {

        return new Promise(
            (resolve, reject) => {

                if (
                    typeof GM_xmlhttpRequest ===
                    'function'
                ) {

                    GM_xmlhttpRequest({

                        method: 'GET',

                        url,

                        timeout:
                            CONFIG.requestTimeout,

                        onload: response => {

                            const contentType =
                                response
                                    .responseHeaders
                                    ?.match(
                                        /content-type:\s*([^\r\n]+)/i
                                    )?.[1] ||
                                null;

                            resolve({
                                status:
                                    response.status,

                                contentType,

                                body:
                                    response.responseText
                            });
                        },

                        onerror: () =>
                            reject(
                                new Error(
                                    'request failed'
                                )
                            ),

                        ontimeout: () =>
                            reject(
                                new Error(
                                    'request timeout'
                                )
                            )
                    });

                    return;
                }

                fetch(url, {
                    credentials:
                        'same-origin',

                    signal:
                        AbortSignal.timeout(
                            CONFIG.requestTimeout
                        )
                })
                    .then(async response => ({
                        status:
                            response.status,

                        contentType:
                            response.headers
                                .get(
                                    'content-type'
                                ),

                        body:
                            await response.text()
                    }))
                    .then(resolve)
                    .catch(reject);
            }
        );
    }
}

// =====================================================================
// Provider Interface
// =====================================================================

/*
 * A provider answers:
 *
 *     "Can I recognize this response?"
 *
 * and, if yes:
 *
 *     "What did I discover, and what new candidates did I learn?"
 *
 * Providers are intentionally independent of acquisition.
 */

class ResponseProvider {

    matches(/* observation */) {
        return false;
    }

    recognize(/* candidate, observation */) {
        return null;
    }

    candidates(/* discovery */) {
        return [];
    }
}

// =====================================================================
// HTML Provider
// =====================================================================

class HtmlProvider extends ResponseProvider {

    matches(observation) {

        const type =
            observation.http.contentType ||
            '';

        const body =
            observation.body || '';

        return (
            type.includes('text/html') ||
            /<html[\s>]/i.test(body) ||
            /<body[\s>]/i.test(body)
        );
    }

    recognize(candidate, observation) {

        if (!this.matches(observation)) {
            return null;
        }

        const body =
            observation.body || '';

        const doc =
            new DOMParser()
                .parseFromString(
                    body,
                    'text/html'
                );

        const title =
            doc.querySelector('title')
                ?.textContent
                ?.trim() || '';

        const links = [
            ...doc.querySelectorAll(
                'a[href]'
            )
        ]
            .map(element =>
                canonicalizeUrl(
                    element.href
                )
            )
            .filter(Boolean)
            .filter(isAllowedUrl);

        const resources = [
            ...doc.querySelectorAll(
                'script[src],' +
                'link[href],' +
                'img[src]'
            )
        ]
            .map(element =>
                canonicalizeUrl(
                    element.src ||
                    element.href
                )
            )
            .filter(Boolean)
            .filter(isAllowedUrl);

        return new Discovery({
            candidate,
            observation,

            kind: 'html-document',

            confidence: 0.95,

            data: {
                url: candidate.target,
                title,
                links,
                resources
            }
        });
    }

    candidates(discovery) {

        const result = [];

        if (CONFIG.discoverLinks) {

            for (
                const url of
                discovery.data.links || []
            ) {

                result.push(
                    new Candidate({
                        target: url,
                        type: 'url',
                        origin:
                            `html:${discovery.id}`,
                        parent:
                            discovery.id,
                        priority: 0.8
                    })
                );
            }
        }

        if (CONFIG.discoverResources) {

            for (
                const url of
                discovery.data.resources || []
            ) {

                result.push(
                    new Candidate({
                        target: url,
                        type: 'resource',
                        origin:
                            `html:${discovery.id}`,
                        parent:
                            discovery.id,
                        priority: 0.5
                    })
                );
            }
        }

        return result;
    }
}

// =====================================================================
// JSON Provider
// =====================================================================

class JsonProvider extends ResponseProvider {

    matches(observation) {

        const type =
            observation.http.contentType ||
            '';

        return (
            type.includes(
                'application/json'
            ) ||
            type.includes(
                '+json'
            )
        );
    }

    recognize(candidate, observation) {

        if (!this.matches(observation)) {
            return null;
        }

        let value;

        try {

            value =
                JSON.parse(
                    observation.body
                );

        } catch {
            return null;
        }

        const urls =
            this.extractUrls(value);

        return new Discovery({
            candidate,
            observation,

            kind: 'json-document',

            confidence: 0.95,

            data: {
                url: candidate.target,
                value,
                urls
            }
        });
    }

    extractUrls(value) {

        const result = [];

        const visit = value => {

            if (typeof value === 'string') {

                const url =
                    canonicalizeUrl(
                        value
                    );

                if (
                    url &&
                    isAllowedUrl(url)
                ) {
                    result.push(url);
                }

                return;
            }

            if (!value || typeof value !== 'object') {
                return;
            }

            for (
                const child of
                Object.values(value)
            ) {
                visit(child);
            }
        };

        visit(value);

        return [
            ...new Set(result)
        ];
    }

    candidates(discovery) {

        return (
            discovery.data.urls || []
        ).map(url =>
            new Candidate({
                target: url,
                type: 'url',
                origin:
                    `json:${discovery.id}`,
                parent:
                    discovery.id,
                priority: 0.7
            })
        );
    }
}

// =====================================================================
// Plain Text Provider
// =====================================================================

class TextProvider extends ResponseProvider {

    matches(observation) {

        const type =
            observation.http.contentType ||
            '';

        return (
            type.startsWith('text/') ||
            type === ''
        );
    }

    recognize(candidate, observation) {

        if (!this.matches(observation)) {
            return null;
        }

        const text =
            observation.body || '';

        /*
         * Find absolute HTTP(S) URLs in text.
         */
        const matches =
            text.match(
                /https?:\/\/[^\s"'<>]+/gi
            ) || [];

        const urls =
            matches
                .map(canonicalizeUrl)
                .filter(Boolean)
                .filter(isAllowedUrl);

        return new Discovery({
            candidate,
            observation,

            kind: 'text-document',

            confidence: 0.75,

            data: {
                url: candidate.target,
                textLength: text.length,
                urls: [
                    ...new Set(urls)
                ]
            }
        });
    }

    candidates(discovery) {

        return (
            discovery.data.urls || []
        ).map(url =>
            new Candidate({
                target: url,
                type: 'url',
                origin:
                    `text:${discovery.id}`,
                parent:
                    discovery.id,
                priority: 0.4
            })
        );
    }
}

// =====================================================================
// Provider Registry
// =====================================================================

class ProviderRegistry {

    constructor() {

        this.providers = [
            new JsonProvider(),
            new HtmlProvider(),
            new TextProvider()
        ];
    }

    recognize(candidate, observation) {

        for (
            const provider of
            this.providers
        ) {

            if (
                !provider.matches(
                    observation
                )
            ) {
                continue;
            }

            const discovery =
                provider.recognize(
                    candidate,
                    observation
                );

            if (discovery) {

                return {
                    provider,
                    discovery
                };
            }
        }

        return null;
    }
}

// =====================================================================
// Scheduler
// =====================================================================

class Scheduler {

    constructor(database) {
        this.database = database;
    }

    add(candidate) {
        return this.database
            .addCandidate(candidate);
    }

    /*
     * Important:
     *
     * Do NOT implement this as:
     *
     *     candidate = next()
     *     await something
     *     markVisited(candidate)
     *
     * The candidate must be claimed synchronously before the
     * worker performs any asynchronous operation.
     */
    claim() {
        return this.database
            .claimNextCandidate();
    }

    complete(candidate) {
        this.database
            .completeCandidate(candidate);
    }

    fail(candidate, retry = false) {
        this.database
            .failCandidate(
                candidate,
                retry
            );
    }

    size() {
        return this.database
            .queueSize();
    }
}

// =====================================================================
// Discovery Engine
// =====================================================================

class DiscoveryEngine {

    constructor() {

        this.database =
            new KnowledgeBase();

        this.scheduler =
            new Scheduler(
                this.database
            );

        this.acquisition =
            new HttpAcquisitionAdapter();

        this.providers =
            new ProviderRegistry();

        this.running = false;

        this.stats = {
            startedAt: null,
            requests: 0,
            discoveries: 0,
            failures: 0,
            candidatesCreated: 0
        };
    }

    seed() {

        const current =
            canonicalizeUrl(
                location.href
            );

        if (current) {

            this.addCandidate(
                new Candidate({
                    target: current,
                    type: 'url',
                    origin: 'initial-page',
                    priority: 1.0
                })
            );
        }

        /*
         * Treat the already-loaded DOM as an initial observation.
         * This avoids requiring a network request just to discover
         * links already present on the page.
         */
        const initialLinks = [
            ...document.querySelectorAll(
                'a[href]'
            )
        ];

        for (
            const element of initialLinks
        ) {

            const url =
                canonicalizeUrl(
                    element.href
                );

            if (
                url &&
                isAllowedUrl(url)
            ) {

                this.addCandidate(
                    new Candidate({
                        target: url,
                        type: 'url',
                        origin: 'initial-dom',
                        priority: 0.7
                    })
                );
            }
        }
    }

    addCandidate(candidate) {

        const added =
            this.scheduler.add(
                candidate
            );

        if (added) {
            this.stats.candidatesCreated++;
        }

        return added;
    }

    async run() {

        if (this.running) {
            return;
        }

        this.running = true;

        this.stats.startedAt = now();

        log(
            'Starting discovery',
            {
                concurrency:
                    CONFIG.concurrency
            }
        );

        const workers = [];

        for (
            let i = 0;
            i < CONFIG.concurrency;
            i++
        ) {

            workers.push(
                this.worker(i)
            );
        }

        await Promise.all(workers);

        this.running = false;

        log(
            'Discovery complete',
            this.stats
        );
    }

    async worker(workerId) {

        while (
            this.running &&
            this.stats.requests <
                CONFIG.maxRequests
        ) {

            /*
             * CLAIM FIRST.
             *
             * This operation is synchronous.
             * No await occurs before ownership is established.
             */
            const candidate =
                this.scheduler.claim();

            if (!candidate) {
                break;
            }

            this.stats.requests++;

            log(
                `Worker ${workerId} claimed`,
                candidate.target
            );

            try {

                const observation =
                    await this.acquisition
                        .acquire(candidate);

                this.database
                    .addObservation(
                        observation
                    );

                if (
                    observation.status !==
                    'acquired'
                ) {

                    this.stats.failures++;

                    this.scheduler.fail(
                        candidate,
                        false
                    );

                    continue;
                }

                const result =
                    this.providers.recognize(
                        candidate,
                        observation
                    );

                if (!result) {

                    this.scheduler.complete(
                        candidate
                    );

                    continue;
                }

                const {
                    provider,
                    discovery
                } = result;

                this.database
                    .addDiscovery(
                        discovery
                    );

                this.stats.discoveries++;

                log(
                    `Worker ${workerId} discovered`,
                    discovery.kind,
                    candidate.target
                );

                /*
                 * A provider can expand the search space.
                 */
                const newCandidates =
                    provider.candidates(
                        discovery
                    );

                for (
                    const next
                    of newCandidates
                ) {
                    this.addCandidate(next);
                }

                this.scheduler.complete(
                    candidate
                );

            } catch (error) {

                warn(
                    `Worker ${workerId} failed:`,
                    error
                );

                this.stats.failures++;

                this.scheduler.fail(
                    candidate,
                    false
                );
            }
        }
    }

    export() {

        return {
            version: 2,

            scope: {
                type:
                    'web-resource-discovery',

                inspiredBy:
                    'DVB blind-scan architecture',

                rfScanning:
                    false
            },

            timestamp:
                new Date().toISOString(),

            page:
                location.href,

            statistics:
                this.stats,

            discoveries: [
                ...this.database
                    .discoveries
                    .values()
            ]
        };
    }

    report() {

        const discoveries = [
            ...this.database
                .discoveries
                .values()
        ];

        console.group(
            '[Discovery] Results'
        );

        console.table(
            discoveries.map(
                discovery => ({
                    kind:
                        discovery.kind,

                    confidence:
                        discovery.confidence,

                    url:
                        discovery.data.url,

                    title:
                        discovery.data.title ||
                        ''
                })
            )
        );

        console.log(
            'Queue:',
            this.scheduler.size()
        );

        console.log(
            'In flight:',
            this.database.claimedSize()
        );

        console.log(
            'Statistics:',
            this.stats
        );

        console.groupEnd();
    }

    clear() {
        this.database.clear();
    }
}

// =====================================================================
// UI
// =====================================================================

const engine =
    new DiscoveryEngine();

/*
 * Public API for experimentation.
 */
window.GenericDiscovery = engine;

const panel =
    document.createElement('div');

panel.style.cssText = `
    position: fixed;
    right: 12px;
    bottom: 12px;
    z-index: 2147483647;
    background: rgba(20,20,20,.94);
    color: white;
    padding: 10px;
    border-radius: 8px;
    font: 12px monospace;
    box-shadow: 0 3px 15px rgba(0,0,0,.4);
`;

panel.innerHTML = `
    <div style="margin-bottom:6px">
        <strong>Generic Discovery</strong>
    </div>

    <div style="
        margin-bottom:8px;
        opacity:.7;
        max-width:260px;
    ">
        Web-resource prototype inspired by
        DVB blind-scan architecture.
    </div>

    <button id="gd-start">
        Scan
    </button>

    <button id="gd-clear">
        Clear
    </button>

    <button id="gd-export">
        Export
    </button>

    <div id="gd-status"
         style="margin-top:6px">
        idle
    </div>
`;

document.documentElement.appendChild(
    panel
);

const status =
    panel.querySelector(
        '#gd-status'
    );

panel.querySelector(
    '#gd-start'
).addEventListener(
    'click',
    async () => {

        if (engine.running) {
            return;
        }

        status.textContent =
            'scanning...';

        engine.seed();

        await engine.run();

        engine.report();

        status.textContent =
            `done — ` +
            `${engine.stats.discoveries} discoveries`;
    }
);

panel.querySelector(
    '#gd-clear'
).addEventListener(
    'click',
    () => {

        engine.clear();

        status.textContent =
            'cleared';
    }
);

panel.querySelector(
    '#gd-export'
).addEventListener(
    'click',
    () => {

        const data =
            engine.export();

        const blob =
            new Blob(
                [
                    JSON.stringify(
                        data,
                        null,
                        2
                    )
                ],
                {
                    type:
                        'application/json'
                }
            );

        const url =
            URL.createObjectURL(
                blob
            );

        const a =
            document.createElement('a');

        a.href = url;

        a.download =
            `discovery-${Date.now()}.json`;

        a.click();

        URL.revokeObjectURL(url);
    }
);
```

})();

### What changed

**1. Concurrent claiming is now explicit.**

The important change is:

```
claimNextCandidate()
```

which synchronously moves a candidate:

```
queued → claimed
```

before the worker performs its first `await`.

So with three workers:

```
Queue: A B C D E

Worker 1 → claims A
Worker 2 → claims B
Worker 3 → claims C

Queue: D E
Claimed: A B C
```

There is no opportunity for two workers to acquire `A`.

`visited` and `claimed` are deliberately different:

```
visited = completed candidates
claimed = currently owned candidates
queued  = candidates waiting for a worker
```

That distinction becomes particularly important once acquisition is asynchronous.

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

**3. The actual scope is now explicit.**

This script is **not** implementing DVB blind scanning. It implements the _algorithmic pattern_:

> search → probe → recognize → discover → expand → schedule

against web resources.

The correspondence is architectural:

```
DVB                         Prototype

frequency candidate    →   URL candidate
RF detection            →   HTTP acquisition
demodulator lock        →   response recognition
PSI/SI                  →   content metadata
NIT                     →   metadata-derived candidates
multiplex discovery     →   resource discovery
scan database           →   knowledge base
```

It intentionally does **not** claim that HTTP discovery is equivalent to RF discovery. The useful research question here is whether the **blind-scan control architecture** generalizes beyond DVB—and this prototype gives you a concrete testbed for that idea.