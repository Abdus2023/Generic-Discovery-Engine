# The Discovery Loop

> **Status:** DESIGNED
>
> **Source:** `Userscript Discovery Prototype.md`
>
> **Purpose:** The search/decision loop: coarse-to-fine search, the complete conceptual algorithm, and termination modes.

## Source Sections

- *Turn lead-in* — `USP-016` — `Userscript Discovery Prototype.md` L464–464
- **8. Model scanning as a search problem** — `USP-017` — `Userscript Discovery Prototype.md` L466–489
- **9. Coarse-to-fine search** — `USP-018` — `Userscript Discovery Prototype.md` L491–527
- **18. Termination** — `USP-029` — `Userscript Discovery Prototype.md` L865–869
- **Exhaustive scan** — `USP-030` — `Userscript Discovery Prototype.md` L871–881
- **Confidence-based scan** — `USP-031` — `Userscript Discovery Prototype.md` L883–891
- **Time-bounded scan** — `USP-032` — `Userscript Discovery Prototype.md` L893–901
- **Hybrid** — `USP-033` — `Userscript Discovery Prototype.md` L903–915
- **22. The complete conceptual algorithm** — `USP-037` — `Userscript Discovery Prototype.md` L1025–1069

## Related Documents

- [Generic Discovery](generic-discovery.md)
- [Search Space](../architecture/search-space.md)
- [Scheduling](../architecture/scheduler.md)
- [Coverage, Completeness and Absence](../architecture/coverage-and-absence.md)

---

<!-- USP-016 | Userscript Discovery Prototype.md L464–464 | turn 5 | ChatGPT turn lead-in -->
> **Source sections:** `USP-016`
>
> **Note:** lead-in of the following section

The next step is to make the scanner **adaptive** rather than a simple nested loop. That gives you something closer to a reusable discovery engine.

<!-- USP-017 | Userscript Discovery Prototype.md L466–489 | turn 5 | version ? -->
### 8. Model scanning as a search problem

> **Source sections:** `USP-017`

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

<!-- USP-018 | Userscript Discovery Prototype.md L491–527 | turn 5 | version ? -->
## 9. Coarse-to-fine search

> **Source sections:** `USP-018`

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

<!-- USP-029 | Userscript Discovery Prototype.md L865–869 | turn 7 | version ? -->
## 18. Termination

> **Source sections:** `USP-029`
>
> [DOCUMENTATION REVIEW] Contradiction **C-09** ([Review Notes](../REVIEW-NOTES.md#c-09--two-termination-taxonomies))

A blind scan should not simply stop after finding the first multiplex.

Typical termination conditions are:

<!-- USP-030 | Userscript Discovery Prototype.md L871–881 | turn 7 | version ? -->
### Exhaustive scan

> **Source sections:** `USP-030`

Stop when:

```
all candidates have been evaluated
```

This gives the strongest claim:

> "Everything in the configured search space was examined."

<!-- USP-031 | Userscript Discovery Prototype.md L883–891 | turn 7 | version ? -->
### Confidence-based scan

> **Source sections:** `USP-031`
>
> [DOCUMENTATION REVIEW] Contradiction **C-06** ([Review Notes](../REVIEW-NOTES.md#c-06--confidence-one-score-versus-no-single-global-score))

Stop when:

```
remaining candidates have probability < threshold
```

This is faster but no longer guarantees exhaustive discovery.

<!-- USP-032 | Userscript Discovery Prototype.md L893–901 | turn 7 | version ? -->
### Time-bounded scan

> **Source sections:** `USP-032`

Stop after:

```
scan_time >= configured_budget
```

Useful for receivers that need to remain responsive.

<!-- USP-033 | Userscript Discovery Prototype.md L903–915 | turn 7 | version ? -->
### Hybrid

> **Source sections:** `USP-033`

A practical implementation can do:

```
1. Perform coarse scan.
2. Fully investigate strong candidates.
3. Follow network metadata.
4. Return to unexplored spectrum.
5. Stop when coverage reaches the requested level.
```

---

<!-- USP-037 | Userscript Discovery Prototype.md L1025–1069 | turn 7 | version ? -->
## 22. The complete conceptual algorithm

> **Source sections:** `USP-037`

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
