# The Discovery Loop

> **Status:** DESIGNED
>
> **Source:** `Userscript Discovery Prototype.md`
>
> **Purpose:** The search/decision loop: coarse-to-fine search, the complete conceptual algorithm, and termination modes.

## Contents

- *Turn lead-in* — `Userscript Discovery Prototype.md` L464–464
- **8. Model scanning as a search problem** — `Userscript Discovery Prototype.md` L466–489
- **9. Coarse-to-fine search** — `Userscript Discovery Prototype.md` L491–527
- **18. Termination** — `Userscript Discovery Prototype.md` L865–869
- **Exhaustive scan** — `Userscript Discovery Prototype.md` L871–881
- **Confidence-based scan** — `Userscript Discovery Prototype.md` L883–891
- **Time-bounded scan** — `Userscript Discovery Prototype.md` L893–901
- **Hybrid** — `Userscript Discovery Prototype.md` L903–915
- **22. The complete conceptual algorithm** — `Userscript Discovery Prototype.md` L1025–1069

## Related Documents

- [Generic Discovery](generic-discovery.md)
- [Search Space](../architecture/search-space.md)
- [Scheduling](../architecture/scheduler.md)
- [Coverage, Completeness and Absence](../architecture/coverage-and-absence.md)

---

<!-- source: Userscript Discovery Prototype.md L464–464 | turn 5 | ChatGPT turn lead-in -->
The next step is to make the scanner **adaptive** rather than a simple nested loop. That gives you something closer to a reusable discovery engine.

<!-- source: Userscript Discovery Prototype.md L466–489 | turn 5 | version ? -->
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

<!-- source: Userscript Discovery Prototype.md L491–527 | turn 5 | version ? -->
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

<!-- source: Userscript Discovery Prototype.md L865–869 | turn 7 | version ? -->
## 18. Termination

A blind scan should not simply stop after finding the first multiplex.

Typical termination conditions are:

<!-- source: Userscript Discovery Prototype.md L871–881 | turn 7 | version ? -->
### Exhaustive scan

Stop when:

```
all candidates have been evaluated
```

This gives the strongest claim:

> "Everything in the configured search space was examined."

<!-- source: Userscript Discovery Prototype.md L883–891 | turn 7 | version ? -->
### Confidence-based scan

Stop when:

```
remaining candidates have probability < threshold
```

This is faster but no longer guarantees exhaustive discovery.

<!-- source: Userscript Discovery Prototype.md L893–901 | turn 7 | version ? -->
### Time-bounded scan

Stop after:

```
scan_time >= configured_budget
```

Useful for receivers that need to remain responsive.

<!-- source: Userscript Discovery Prototype.md L903–915 | turn 7 | version ? -->
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

<!-- source: Userscript Discovery Prototype.md L1025–1069 | turn 7 | version ? -->
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
