# Source Map

> **Status:** CURRENT
>
> **Source:** `Userscript Discovery Prototype.md`; `Continue Architecture Planning.md`
>
> **Purpose:** Machine-readable trace of every extracted source section to its destination in this documentation tree.

This map is mandatory output of the mechanical split. Every source section extracted from the two original documents has exactly one disposition:

`MOVED` (content copied into the destination), `SPLIT` (a source section divided at an existing numbered boundary), `DUPLICATE` (near-duplicate of a retained canonical section) or `ARTIFACT` (conversation continuation marker removed).

Line numbers refer to the original documents as committed before the split (see [`archive/`](../archive/)).

## Summary

| Disposition | Sections |
| --- | --- |
| MOVED | 1196 |
| SPLIT | 3 |
| DUPLICATE | 1 |
| ARTIFACT | 44 |
| **total extracted sections** | **1244** |

## Destination files

| Destination | Sections | Bytes |
| --- | --- | --- |
| [`acquisition/acquisition-model.md`](acquisition/acquisition-model.md) | 8 | 7522 |
| [`acquisition/overview.md`](acquisition/overview.md) | 3 | 2955 |
| [`acquisition/response-recognition.md`](acquisition/response-recognition.md) | 24 | 19472 |
| [`acquisition/runtime.md`](acquisition/runtime.md) | 18 | 16260 |
| [`architecture/candidate-model.md`](architecture/candidate-model.md) | 9 | 7626 |
| [`architecture/capability-model.md`](architecture/capability-model.md) | 17 | 16617 |
| [`architecture/classification.md`](architecture/classification.md) | 23 | 23831 |
| [`architecture/concurrency.md`](architecture/concurrency.md) | 36 | 28621 |
| [`architecture/coordination.md`](architecture/coordination.md) | 38 | 32591 |
| [`architecture/coverage-and-absence.md`](architecture/coverage-and-absence.md) | 50 | 46709 |
| [`architecture/discovery-model.md`](architecture/discovery-model.md) | 26 | 29192 |
| [`architecture/evidence-model.md`](architecture/evidence-model.md) | 41 | 25777 |
| [`architecture/goal-and-query.md`](architecture/goal-and-query.md) | 64 | 56339 |
| [`architecture/observation-model.md`](architecture/observation-model.md) | 13 | 7886 |
| [`architecture/overview.md`](architecture/overview.md) | 1 | 3040 |
| [`architecture/persistence-and-recovery.md`](architecture/persistence-and-recovery.md) | 32 | 24436 |
| [`architecture/provenance.md`](architecture/provenance.md) | 12 | 9947 |
| [`architecture/provider-architecture.md`](architecture/provider-architecture.md) | 13 | 10132 |
| [`architecture/resource-budget.md`](architecture/resource-budget.md) | 24 | 20942 |
| [`architecture/resource-model.md`](architecture/resource-model.md) | 81 | 54314 |
| [`architecture/scheduler.md`](architecture/scheduler.md) | 11 | 9083 |
| [`architecture/search-space.md`](architecture/search-space.md) | 106 | 75714 |
| [`architecture/sessions-and-domains.md`](architecture/sessions-and-domains.md) | 31 | 21879 |
| [`architecture/strategy-and-planning.md`](architecture/strategy-and-planning.md) | 101 | 75939 |
| [`architecture/system-model.md`](architecture/system-model.md) | 36 | 88478 |
| [`architecture/work-and-frontier.md`](architecture/work-and-frontier.md) | 52 | 47280 |
| [`concepts/discovery-loop.md`](concepts/discovery-loop.md) | 9 | 6111 |
| [`concepts/generic-discovery.md`](concepts/generic-discovery.md) | 8 | 9983 |
| [`concepts/overview.md`](concepts/overview.md) | 16 | 24175 |
| [`prototype/limitations.md`](prototype/limitations.md) | 5 | 6277 |
| [`prototype/overview.md`](prototype/overview.md) | 2 | 4609 |
| [`prototype/userscript.md`](prototype/userscript.md) | 14 | 19199 |
| [`prototype/versions/00-v0.1.0-and-v0.2.0-paste.md`](prototype/versions/00-v0.1.0-and-v0.2.0-paste.md) | 1 | 58429 |
| [`prototype/versions/01-v0.1.0.md`](prototype/versions/01-v0.1.0.md) | 2 | 23906 |
| [`prototype/versions/02-v0.2.0.md`](prototype/versions/02-v0.2.0.md) | 2 | 36739 |
| [`prototype/versions/03-v0.3.0.md`](prototype/versions/03-v0.3.0.md) | 2 | 69223 |
| [`prototype/versions/04-v0.4.0-plan.md`](prototype/versions/04-v0.4.0-plan.md) | 2 | 4962 |
| [`prototype/versions/05-v0.4.0.md`](prototype/versions/05-v0.4.0.md) | 2 | 109277 |
| [`prototype/versions/06-v0.5.0.md`](prototype/versions/06-v0.5.0.md) | 1 | 159651 |
| [`prototype/versions/07-v0.4.0-second-iteration.md`](prototype/versions/07-v0.4.0-second-iteration.md) | 1 | 125769 |
| [`prototype/versions/08-v0.5.0-plan.md`](prototype/versions/08-v0.5.0-plan.md) | 1 | 3069 |
| [`prototype/versions/09-v0.5.0-second-iteration.md`](prototype/versions/09-v0.5.0-second-iteration.md) | 1 | 124254 |
| [`prototype/versions/10-v0.6.0.md`](prototype/versions/10-v0.6.0.md) | 1 | 163134 |
| [`prototype/versions/11-v0.5.0-third-iteration.md`](prototype/versions/11-v0.5.0-third-iteration.md) | 1 | 155658 |
| [`prototype/versions/12-v0.6.0-second-iteration.md`](prototype/versions/12-v0.6.0-second-iteration.md) | 1 | 219322 |
| [`prototype/versions/13-v0.6.0-third-iteration.md`](prototype/versions/13-v0.6.0-third-iteration.md) | 1 | 146288 |
| [`prototype/versions/14-v0.7.1.md`](prototype/versions/14-v0.7.1.md) | 1 | 143228 |
| [`providers/candidate-sources.md`](providers/candidate-sources.md) | 22 | 18010 |
| [`providers/overview.md`](providers/overview.md) | 3 | 4434 |
| [`research/dvb-blind-scan.md`](research/dvb-blind-scan.md) | 15 | 15095 |
| [`roadmap/future-work.md`](roadmap/future-work.md) | 16 | 21625 |
| [`validation/failure-taxonomy.md`](validation/failure-taxonomy.md) | 17 | 16677 |
| [`validation/invariants.md`](validation/invariants.md) | 176 | 59966 |
| [`validation/verification.md`](validation/verification.md) | 7 | 4514 |

## Complete mapping

| Source | Lines | Original Section | Destination | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| `Userscript Discovery Prototype.md` | 3–3 | *turn 0 you lead-in* | `research/dvb-blind-scan.md` | MOVED | originating request |
| `Userscript Discovery Prototype.md` | 9–23 | *turn 1 chatgpt lead-in* | `research/dvb-blind-scan.md` | MOVED | lead-in of the following section |
| `Userscript Discovery Prototype.md` | 25–64 | Generic pseudocode | `research/dvb-blind-scan.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 66–102 | Making it genuinely generic | `concepts/generic-discovery.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 108–108 | *turn 2 you lead-in* | — (removed) | ARTIFACT | conversation continuation marker |
| `Userscript Discovery Prototype.md` | 114–114 | *turn 3 chatgpt lead-in* | `concepts/generic-discovery.md` | MOVED | lead-in of the following section |
| `Userscript Discovery Prototype.md` | 116–144 | 1. Separate the layers | `concepts/generic-discovery.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 146–209 | 2. Candidate generation | `architecture/candidate-model.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 211–248 | 3. Detection should precede expensive decoding | `acquisition/overview.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 250–301 | 4. Lock is not discovery | `acquisition/response-recognition.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 303–346 | 5. Use DVB metadata to escape blind mode | `research/dvb-blind-scan.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 348–382 | 6. Deduplication | `architecture/candidate-model.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 384–439 | 7. Generic algorithm | `concepts/generic-discovery.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 441–452 | 7. Generic algorithm › The key insight | `concepts/generic-discovery.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 458–458 | *turn 4 you lead-in* | — (removed) | ARTIFACT | conversation continuation marker |
| `Userscript Discovery Prototype.md` | 464–464 | *turn 5 chatgpt lead-in* | `concepts/discovery-loop.md` | MOVED | lead-in of the following section |
| `Userscript Discovery Prototype.md` | 466–489 | 8. Model scanning as a search problem | `concepts/discovery-loop.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 491–527 | 9. Coarse-to-fine search | `concepts/discovery-loop.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 529–571 | 10. Confidence rather than binary decisions | `architecture/discovery-model.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 573–615 | 11. Don't immediately discard failed candidates | `architecture/scheduler.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 617–646 | 12. Adaptive retry | `architecture/scheduler.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 648–676 | 13. Scheduling becomes important | `architecture/scheduler.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 678–737 | 14. Discovery database | `architecture/system-model.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 739–775 | 15. The generic discovery abstraction | `concepts/generic-discovery.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 781–781 | *turn 6 you lead-in* | — (removed) | ARTIFACT | conversation continuation marker |
| `Userscript Discovery Prototype.md` | 787–787 | *turn 7 chatgpt lead-in* | `architecture/discovery-model.md` | MOVED | lead-in of the following section |
| `Userscript Discovery Prototype.md` | 789–823 | 16. Discovery should have evidence levels | `architecture/discovery-model.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 825–863 | 17. Use observations to update the search space | `architecture/search-space.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 865–869 | 18. Termination | `concepts/discovery-loop.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 871–881 | 18. Termination › Exhaustive scan | `concepts/discovery-loop.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 883–891 | 18. Termination › Confidence-based scan | `concepts/discovery-loop.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 893–901 | 18. Termination › Time-bounded scan | `concepts/discovery-loop.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 903–915 | 18. Termination › Hybrid | `concepts/discovery-loop.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 917–949 | 19. Coverage is a better metric than elapsed time | `architecture/coverage-and-absence.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 951–991 | 20. Cache knowledge between scans | `architecture/persistence-and-recovery.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 993–1023 | 21. Handle disappearing multiplexes | `architecture/resource-model.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 1025–1069 | 22. The complete conceptual algorithm | `concepts/discovery-loop.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 1071–1099 | 22. The complete conceptual algorithm › 23. A useful formal name | `concepts/generic-discovery.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 1105–1105 | *turn 8 you lead-in* | — (removed) | ARTIFACT | conversation continuation marker |
| `Userscript Discovery Prototype.md` | 1111–1111 | *turn 9 chatgpt lead-in* | `architecture/discovery-model.md` | MOVED | lead-in of the following section |
| `Userscript Discovery Prototype.md` | 1113–1145 | 24. Two-dimensional discovery | `architecture/discovery-model.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 1147–1206 | 25. Candidate lifecycle | `architecture/candidate-model.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 1208–1245 | 26. Discovery becomes a graph | `architecture/discovery-model.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 1247–1286 | 27. This helps with incremental scanning | `architecture/search-space.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 1288–1339 | 28. Parameter provenance | `architecture/provenance.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 1341–1376 | 29. The scanner should produce an explanation | `architecture/provenance.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 1378–1429 | 30. The final abstraction | `concepts/generic-discovery.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 1435–1435 | *turn 10 you lead-in* | — (removed) | ARTIFACT | conversation continuation marker |
| `Userscript Discovery Prototype.md` | 1441–1441 | *turn 11 chatgpt lead-in* | `architecture/system-model.md` | MOVED | lead-in of the following section |
| `Userscript Discovery Prototype.md` | 1443–1453 | 31. Define the core objects | `architecture/system-model.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 1455–1476 | 31. Define the core objects › Candidate | `architecture/candidate-model.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 1478–1507 | 31. Define the core objects › Observation | `architecture/observation-model.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 1509–1526 | 31. Define the core objects › LockResult | `acquisition/response-recognition.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 1528–1545 | 31. Define the core objects › Discovery | `architecture/discovery-model.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 1547–1584 | 32. Use capability-driven adapters | `architecture/provider-architecture.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 1586–1614 | 33. Discovery strategies should also be pluggable | `architecture/strategy-and-planning.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 1616–1659 | 34. Don't confuse candidate identity with reception identity | `architecture/candidate-model.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 1661–1701 | 35. Make deduplication hierarchical | `architecture/candidate-model.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 1703–1734 | 36. Treat metadata as a candidate generator | `architecture/candidate-model.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 1736–1773 | 37. Candidate provenance creates a discovery tree | `architecture/provenance.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 1775–1800 | 38. Avoid infinite candidate generation | `architecture/search-space.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 1802–1829 | 39. A practical scheduler | `architecture/scheduler.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 1831–1875 | 40. The engine can now become event-driven | `architecture/system-model.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 1877–1922 | 41. The resulting architecture | `architecture/overview.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 1928–1930 | *turn 12 you lead-in* | `prototype/versions/01-v0.1.0.md` | MOVED | lead-in of the following section |
| `Userscript Discovery Prototype.md` | 1936–2964 | *turn 13 chatgpt lead-in* | `prototype/versions/01-v0.1.0.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 2967–3007 | *turn 13 chatgpt lead-in* | `prototype/overview.md` | MOVED | prototype positioning |
| `Userscript Discovery Prototype.md` | 3009–3025 | The DVB analogy | `research/dvb-blind-scan.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 3031–3033 | *turn 14 you lead-in* | `prototype/versions/02-v0.2.0.md` | MOVED | lead-in of the following section |
| `Userscript Discovery Prototype.md` | 3039–4711 | *turn 15 chatgpt lead-in* | `prototype/versions/02-v0.2.0.md` | MOVED | — |
| `Userscript Discovery Prototype.md` | 4713–4756 | What changed — 1. Concurrent claiming is now explicit | `architecture/concurrency.md` | SPLIT | split at numbered boundary |
| `Userscript Discovery Prototype.md` | 4756–4784 | What changed — 2. HTML is no longer special | `providers/overview.md` | SPLIT | split at numbered boundary |
| `Userscript Discovery Prototype.md` | 4784–4807 | What changed — 3. The actual scope is now explicit | `prototype/limitations.md` | SPLIT | split at numbered boundary |
| `Continue Architecture Planning.md` | 3–15 | *turn 0 you lead-in* | `prototype/versions/00-v0.1.0-and-v0.2.0-paste.md` | DUPLICATE | near-duplicate of prototype/versions/01-v0.1.0.md and 02-v0.2.0.md; retained because both copies are damaged differently |
| `Continue Architecture Planning.md` | 21–38 | *turn 1 chatgpt lead-in* | `prototype/overview.md` | MOVED | v0.1; assessment of the initial scripts |
| `Continue Architecture Planning.md` | 44–44 | *turn 2 you lead-in* | `prototype/versions/03-v0.3.0.md` | MOVED | v0.2; lead-in of the following section |
| `Continue Architecture Planning.md` | 50–2645 | *turn 3 chatgpt lead-in* | `prototype/versions/03-v0.3.0.md` | MOVED | v0.3 |
| `Continue Architecture Planning.md` | 2647–2671 | What changed from v0.2.0 | `prototype/userscript.md` | MOVED | v0.3 |
| `Continue Architecture Planning.md` | 2677–2677 | *turn 4 you lead-in* | — (removed) | ARTIFACT | conversation continuation marker |
| `Continue Architecture Planning.md` | 2683–2734 | *turn 5 chatgpt lead-in* | `prototype/versions/04-v0.4.0-plan.md` | MOVED | v0.4 |
| `Continue Architecture Planning.md` | 2736–2777 | The biggest v0.4 improvement | `prototype/versions/04-v0.4.0-plan.md` | MOVED | v0.4 |
| `Continue Architecture Planning.md` | 2783–2783 | *turn 6 you lead-in* | `prototype/versions/05-v0.4.0.md` | MOVED | v0.4; lead-in of the following section |
| `Continue Architecture Planning.md` | 2789–7122 | *turn 7 chatgpt lead-in* | `prototype/versions/05-v0.4.0.md` | MOVED | v0.4 |
| `Continue Architecture Planning.md` | 7124–7148 | Notable v0.4.0 behavior | `prototype/userscript.md` | MOVED | v0.4 |
| `Continue Architecture Planning.md` | 7154–7154 | *turn 8 you lead-in* | — (removed) | ARTIFACT | conversation continuation marker |
| `Continue Architecture Planning.md` | 7160–13452 | *turn 9 chatgpt lead-in* | `prototype/versions/06-v0.5.0.md` | MOVED | v0.5 |
| `Continue Architecture Planning.md` | 13454–13472 | *turn 9 chatgpt lead-in* | `prototype/userscript.md` | MOVED | v0.5 |
| `Continue Architecture Planning.md` | 13478–13478 | *turn 10 you lead-in* | — (removed) | ARTIFACT | conversation continuation marker |
| `Continue Architecture Planning.md` | 13484–18265 | *turn 11 chatgpt lead-in* | `prototype/versions/07-v0.4.0-second-iteration.md` | MOVED | v0.4 |
| `Continue Architecture Planning.md` | 18267–18282 | What changed from v0.3.0 | `prototype/userscript.md` | MOVED | v0.4 |
| `Continue Architecture Planning.md` | 18288–18288 | *turn 12 you lead-in* | — (removed) | ARTIFACT | conversation continuation marker |
| `Continue Architecture Planning.md` | 18294–18364 | *turn 13 chatgpt lead-in* | `prototype/versions/08-v0.5.0-plan.md` | MOVED | v0.5 |
| `Continue Architecture Planning.md` | 18370–18370 | *turn 14 you lead-in* | — (removed) | ARTIFACT | conversation continuation marker |
| `Continue Architecture Planning.md` | 18376–23093 | *turn 15 chatgpt lead-in* | `prototype/versions/09-v0.5.0-second-iteration.md` | MOVED | v0.5 |
| `Continue Architecture Planning.md` | 23095–23126 | v0.5 architecture | `prototype/userscript.md` | MOVED | v0.5; explicit override |
| `Continue Architecture Planning.md` | 23132–23132 | *turn 16 you lead-in* | — (removed) | ARTIFACT | v0.5; conversation continuation marker |
| `Continue Architecture Planning.md` | 23138–29350 | *turn 17 chatgpt lead-in* | `prototype/versions/10-v0.6.0.md` | MOVED | v0.5 |
| `Continue Architecture Planning.md` | 29352–29424 | What v0.6 changes architecturally | `prototype/userscript.md` | MOVED | v0.5 |
| `Continue Architecture Planning.md` | 29430–29430 | *turn 18 you lead-in* | — (removed) | ARTIFACT | v0.5; conversation continuation marker |
| `Continue Architecture Planning.md` | 29436–34704 | *turn 19 chatgpt lead-in* | `prototype/versions/11-v0.5.0-third-iteration.md` | MOVED | v0.5 |
| `Continue Architecture Planning.md` | 34706–34740 | What v0.5.0 changes architecturally | `prototype/userscript.md` | MOVED | v0.5 |
| `Continue Architecture Planning.md` | 34746–34746 | *turn 20 you lead-in* | — (removed) | ARTIFACT | v0.5; conversation continuation marker |
| `Continue Architecture Planning.md` | 34752–43127 | *turn 21 chatgpt lead-in* | `prototype/versions/12-v0.6.0-second-iteration.md` | MOVED | v0.5 |
| `Continue Architecture Planning.md` | 43129–43181 | v0.6.0's main architectural additions | `prototype/userscript.md` | MOVED | v0.6; explicit override |
| `Continue Architecture Planning.md` | 43187–43187 | *turn 22 you lead-in* | — (removed) | ARTIFACT | v0.6; conversation continuation marker |
| `Continue Architecture Planning.md` | 43193–48360 | *turn 23 chatgpt lead-in* | `prototype/versions/13-v0.6.0-third-iteration.md` | MOVED | v0.6 |
| `Continue Architecture Planning.md` | 48362–48376 | What changed in v0.6 | `prototype/userscript.md` | MOVED | v0.6 |
| `Continue Architecture Planning.md` | 48382–48382 | *turn 24 you lead-in* | — (removed) | ARTIFACT | v0.6; conversation continuation marker |
| `Continue Architecture Planning.md` | 48388–48457 | v0.7.0 — Discovery Graph + Acquisition Planner | `architecture/discovery-model.md` | MOVED | v0.7 |
| `Continue Architecture Planning.md` | 48459–48492 | v0.7.0 — Discovery Graph + Acquisition Planner › v0.7 objectives | `architecture/discovery-model.md` | MOVED | v0.7 |
| `Continue Architecture Planning.md` | 48494–48659 | v0.7.0 — Discovery Graph + Acquisition Planner › Core contract | `architecture/discovery-model.md` | MOVED | v0.7 |
| `Continue Architecture Planning.md` | 48661–48720 | v0.7.0 — Discovery Graph + Acquisition Planner › Important v0.7 distinction | `architecture/discovery-model.md` | MOVED | v0.7 |
| `Continue Architecture Planning.md` | 48722–48800 | v0.7 state machine | `architecture/discovery-model.md` | MOVED | v0.7 |
| `Continue Architecture Planning.md` | 48802–48856 | The deeper abstraction | `concepts/overview.md` | MOVED | v0.7 |
| `Continue Architecture Planning.md` | 48862–48862 | *turn 26 you lead-in* | — (removed) | ARTIFACT | v0.7; conversation continuation marker |
| `Continue Architecture Planning.md` | 48868–54113 | *turn 27 chatgpt lead-in* | `prototype/versions/14-v0.7.1.md` | MOVED | v0.7 |
| `Continue Architecture Planning.md` | 54115–54115 | *turn 27 chatgpt lead-in* | `prototype/userscript.md` | MOVED | v0.7 |
| `Continue Architecture Planning.md` | 54117–54121 | What v0.7.1 actually changes | `prototype/userscript.md` | MOVED | v0.7 |
| `Continue Architecture Planning.md` | 54123–54133 | What v0.7.1 actually changes › Before | `prototype/userscript.md` | MOVED | v0.7 |
| `Continue Architecture Planning.md` | 54135–54163 | What v0.7.1 actually changes › Now | `prototype/userscript.md` | MOVED | v0.7 |
| `Continue Architecture Planning.md` | 54165–54211 | 2. The ledger becomes the scan's causal trace | `architecture/provenance.md` | MOVED | v0.7; explicit override |
| `Continue Architecture Planning.md` | 54213–54268 | 3. PerformanceObserver correction | `architecture/observation-model.md` | MOVED | v0.7; explicit override |
| `Continue Architecture Planning.md` | 54270–54328 | 4. Candidate state machine | `prototype/userscript.md` | MOVED | v0.7 |
| `Continue Architecture Planning.md` | 54330–54416 | 5. The ledger is not merely logging | `architecture/provenance.md` | MOVED | v0.7; explicit override |
| `Continue Architecture Planning.md` | 54418–54471 | 6. One remaining architectural limitation | `prototype/limitations.md` | MOVED | v0.7 |
| `Continue Architecture Planning.md` | 54473–54580 | 7. Architecture after v0.7.1 | `architecture/system-model.md` | MOVED | v0.7 |
| `Continue Architecture Planning.md` | 54582–54619 | 7. Architecture after v0.7.1 › Next boundary: v0.8 | `roadmap/future-work.md` | MOVED | v0.7 |
| `Continue Architecture Planning.md` | 54625–54625 | *turn 28 you lead-in* | — (removed) | ARTIFACT | v0.7; conversation continuation marker |
| `Continue Architecture Planning.md` | 54631–54653 | v0.8 — Capability-Aware Acquisition Runtime | `architecture/capability-model.md` | MOVED | v0.8 |
| `Continue Architecture Planning.md` | 54655–54681 | v0.8 — Capability-Aware Acquisition Runtime › 1. The three graphs | `architecture/capability-model.md` | MOVED | v0.8 |
| `Continue Architecture Planning.md` | 54683–54695 | 1. The three graphs › Discovery graph | `architecture/capability-model.md` | MOVED | v0.8 |
| `Continue Architecture Planning.md` | 54697–54710 | 1. The three graphs › Acquisition graph | `acquisition/acquisition-model.md` | MOVED | v0.8 |
| `Continue Architecture Planning.md` | 54712–54729 | 1. The three graphs › Evidence graph | `architecture/capability-model.md` | MOVED | v0.8 |
| `Continue Architecture Planning.md` | 54731–54803 | 2. Capability is now a first-class object | `architecture/capability-model.md` | MOVED | v0.8 |
| `Continue Architecture Planning.md` | 54805–54839 | 3. Capability lattice | `architecture/capability-model.md` | MOVED | v0.8 |
| `Continue Architecture Planning.md` | 54841–54905 | 4. Capability contract | `architecture/capability-model.md` | MOVED | v0.8 |
| `Continue Architecture Planning.md` | 54907–54968 | 5. Candidate requirements | `architecture/capability-model.md` | MOVED | v0.8 |
| `Continue Architecture Planning.md` | 54970–55044 | 6. Acquisition planning becomes capability resolution | `acquisition/acquisition-model.md` | MOVED | v0.8 |
| `Continue Architecture Planning.md` | 55046–55104 | 7. Why this matters for generic discovery | `architecture/capability-model.md` | MOVED | v0.8 |
| `Continue Architecture Planning.md` | 55106–55202 | 8. AcquisitionPlan v0.8 | `acquisition/acquisition-model.md` | MOVED | v0.8 |
| `Continue Architecture Planning.md` | 55204–55257 | 9. Capability provenance | `architecture/capability-model.md` | MOVED | v0.8 |
| `Continue Architecture Planning.md` | 55259–55301 | 10. The four-level authorization model | `architecture/capability-model.md` | MOVED | v0.8 |
| `Continue Architecture Planning.md` | 55303–55340 | 11. New graph model | `architecture/capability-model.md` | MOVED | v0.8 |
| `Continue Architecture Planning.md` | 55342–55402 | 12. v0.8 ledger | `architecture/capability-model.md` | MOVED | v0.8 |
| `Continue Architecture Planning.md` | 55404–55458 | 13. Important architectural consequence | `architecture/capability-model.md` | MOVED | v0.8 |
| `Continue Architecture Planning.md` | 55460–55462 | 14. v0.8 scope boundary | `architecture/capability-model.md` | MOVED | v0.8 |
| `Continue Architecture Planning.md` | 55464–55472 | 14. v0.8 scope boundary › Implement | `architecture/capability-model.md` | MOVED | v0.8 |
| `Continue Architecture Planning.md` | 55474–55491 | 14. v0.8 scope boundary › Represent but deny | `architecture/capability-model.md` | MOVED | v0.8 |
| `Continue Architecture Planning.md` | 55493–55532 | 15. Updated system invariant | `validation/invariants.md` | MOVED | v0.8 |
| `Continue Architecture Planning.md` | 55534–55566 | 16. The DVB analogy is now cleaner | `research/dvb-blind-scan.md` | MOVED | v0.8 |
| `Continue Architecture Planning.md` | 55568–55621 | 17. v0.8 → v0.9 | `roadmap/future-work.md` | MOVED | v0.8 |
| `Continue Architecture Planning.md` | 55627–55627 | *turn 30 you lead-in* | — (removed) | ARTIFACT | v0.8; conversation continuation marker |
| `Continue Architecture Planning.md` | 55633–55639 | v0.9 — Acquisition Provider Architecture | `architecture/provider-architecture.md` | MOVED | v0.9 |
| `Continue Architecture Planning.md` | 55641–55697 | v0.9 — Acquisition Provider Architecture › 0.9 architecture | `architecture/system-model.md` | MOVED | v0.9 |
| `Continue Architecture Planning.md` | 55699–55730 | v0.9 — Acquisition Provider Architecture › The important separation | `acquisition/overview.md` | MOVED | v0.9; explicit override |
| `Continue Architecture Planning.md` | 55732–55779 | 1. AcquisitionProvider contract | `architecture/provider-architecture.md` | MOVED | v0.9 |
| `Continue Architecture Planning.md` | 55781–55807 | 2. Provider capabilities | `architecture/provider-architecture.md` | MOVED | v0.9 |
| `Continue Architecture Planning.md` | 55809–55860 | 3. Provider selection | `architecture/provider-architecture.md` | MOVED | v0.9 |
| `Continue Architecture Planning.md` | 55862–55906 | 4. GM-XHR becomes a component | `architecture/provider-architecture.md` | MOVED | v0.9 |
| `Continue Architecture Planning.md` | 55908–55961 | 5. Observation gets provider provenance | `architecture/observation-model.md` | MOVED | v0.9 |
| `Continue Architecture Planning.md` | 55963–55965 | 6. Provider failure ≠ acquisition denial | `architecture/provider-architecture.md` | MOVED | v0.9 |
| `Continue Architecture Planning.md` | 55967–55989 | 6. Provider failure ≠ acquisition denial › Policy denial | `architecture/provider-architecture.md` | MOVED | v0.9 |
| `Continue Architecture Planning.md` | 55991–56016 | 6. Provider failure ≠ acquisition denial › Provider failure | `architecture/provider-architecture.md` | MOVED | v0.9 |
| `Continue Architecture Planning.md` | 56018–56069 | 7. Provider selection itself becomes an event | `architecture/provider-architecture.md` | MOVED | v0.9 |
| `Continue Architecture Planning.md` | 56071–56087 | 8. A deeper consequence: acquisition becomes replaceable | `acquisition/overview.md` | MOVED | v0.9; explicit override |
| `Continue Architecture Planning.md` | 56089–56099 | 8. A deeper consequence: acquisition becomes replaceable › Cache provider | `architecture/provider-architecture.md` | MOVED | v0.9 |
| `Continue Architecture Planning.md` | 56101–56113 | 8. A deeper consequence: acquisition becomes replaceable › Replay provider | `architecture/provider-architecture.md` | MOVED | v0.9 |
| `Continue Architecture Planning.md` | 56115–56191 | 9. The engine is now approaching a general resource runtime | `architecture/provider-architecture.md` | MOVED | v0.9 |
| `Continue Architecture Planning.md` | 56193–56195 | 10. v0.9 invariants | `validation/invariants.md` | MOVED | v0.9 |
| `Continue Architecture Planning.md` | 56197–56201 | 10. v0.9 invariants › I1 — Discovery independence | `validation/invariants.md` | MOVED | v0.9 |
| `Continue Architecture Planning.md` | 56203–56207 | 10. v0.9 invariants › I2 — Policy independence | `validation/invariants.md` | MOVED | v0.9 |
| `Continue Architecture Planning.md` | 56209–56215 | 10. v0.9 invariants › I3 — Capability soundness | `validation/invariants.md` | MOVED | v0.9 |
| `Continue Architecture Planning.md` | 56217–56223 | 10. v0.9 invariants › I4 — Method safety | `validation/invariants.md` | MOVED | v0.9 |
| `Continue Architecture Planning.md` | 56225–56231 | 10. v0.9 invariants › I5 — Provenance | `validation/invariants.md` | MOVED | v0.9 |
| `Continue Architecture Planning.md` | 56233–56241 | 10. v0.9 invariants › I6 — Observation integrity | `validation/invariants.md` | MOVED | v0.9 |
| `Continue Architecture Planning.md` | 56243–56253 | 10. v0.9 invariants › I7 — Replay distinction | `validation/invariants.md` | MOVED | v0.9 |
| `Continue Architecture Planning.md` | 56255–56345 | 11. The next problem is now visible | `roadmap/future-work.md` | MOVED | v0.9 |
| `Continue Architecture Planning.md` | 56351–56351 | *turn 32 you lead-in* | — (removed) | ARTIFACT | v0.9; conversation continuation marker |
| `Continue Architecture Planning.md` | 56357–56366 | v0.10 — Acquisition Runtime | `acquisition/runtime.md` | MOVED | v0.10 |
| `Continue Architecture Planning.md` | 56368–56432 | v0.10 — Acquisition Runtime › 1. The new architecture | `architecture/system-model.md` | MOVED | v0.10 |
| `Continue Architecture Planning.md` | 56434–56436 | 2. The key distinction: Scheduler vs Runtime | `acquisition/runtime.md` | MOVED | v0.10 |
| `Continue Architecture Planning.md` | 56438–56452 | 2. The key distinction: Scheduler vs Runtime › Scheduler | `acquisition/runtime.md` | MOVED | v0.10 |
| `Continue Architecture Planning.md` | 56454–56496 | 2. The key distinction: Scheduler vs Runtime › Runtime | `acquisition/runtime.md` | MOVED | v0.10 |
| `Continue Architecture Planning.md` | 56498–56540 | 3. AcquisitionRuntime contract | `acquisition/runtime.md` | MOVED | v0.10 |
| `Continue Architecture Planning.md` | 56542–56598 | 4. Admission control | `acquisition/runtime.md` | MOVED | v0.10 |
| `Continue Architecture Planning.md` | 56600–56658 | 5. Budget becomes a first-class object | `acquisition/runtime.md` | MOVED | v0.10 |
| `Continue Architecture Planning.md` | 56660–56704 | 6. Why reservation must precede execution | `acquisition/runtime.md` | MOVED | v0.10 |
| `Continue Architecture Planning.md` | 56706–56796 | 7. OriginController | `acquisition/runtime.md` | MOVED | v0.10 |
| `Continue Architecture Planning.md` | 56798–56843 | 8. Provider selection happens after admission prerequisites | `acquisition/runtime.md` | MOVED | v0.10 |
| `Continue Architecture Planning.md` | 56845–56889 | 9. Provider must not own runtime policy | `acquisition/runtime.md` | MOVED | v0.10 |
| `Continue Architecture Planning.md` | 56891–56943 | 10. Cancellation becomes explicit | `acquisition/runtime.md` | MOVED | v0.10 |
| `Continue Architecture Planning.md` | 56945–56979 | 11. Timeout belongs to Runtime | `acquisition/runtime.md` | MOVED | v0.10 |
| `Continue Architecture Planning.md` | 56981–57027 | 12. Retry belongs to Runtime | `acquisition/runtime.md` | MOVED | v0.10 |
| `Continue Architecture Planning.md` | 57029–57056 | 13. Plan vs Attempt | `acquisition/runtime.md` | MOVED | v0.10 |
| `Continue Architecture Planning.md` | 57058–57105 | 14. Runtime event model | `acquisition/runtime.md` | MOVED | v0.10 |
| `Continue Architecture Planning.md` | 57107–57138 | 15. Runtime state machine | `acquisition/runtime.md` | MOVED | v0.10 |
| `Continue Architecture Planning.md` | 57140–57179 | 16. The complete execution equation | `acquisition/runtime.md` | MOVED | v0.10 |
| `Continue Architecture Planning.md` | 57181–57233 | 17. The resulting architecture | `architecture/system-model.md` | MOVED | v0.10 |
| `Continue Architecture Planning.md` | 57235–57297 | 17. The resulting architecture › What v0.10 accomplishes | `concepts/overview.md` | MOVED | v0.10 |
| `Continue Architecture Planning.md` | 57299–57343 | What v0.10 accomplishes › Next boundary: v0.11 | `roadmap/future-work.md` | MOVED | v0.10 |
| `Continue Architecture Planning.md` | 57349–57349 | *turn 34 you lead-in* | — (removed) | ARTIFACT | v0.10; conversation continuation marker |
| `Continue Architecture Planning.md` | 57355–57366 | v0.11 — Response Recognition Runtime | `acquisition/response-recognition.md` | MOVED | v0.11 |
| `Continue Architecture Planning.md` | 57368–57442 | v0.11 — Response Recognition Runtime › 1. v0.11 architecture | `architecture/system-model.md` | MOVED | v0.11 |
| `Continue Architecture Planning.md` | 57444–57493 | 2. RecognitionProvider contract | `acquisition/response-recognition.md` | MOVED | v0.11 |
| `Continue Architecture Planning.md` | 57495–57542 | 3. Recognition is not discovery | `acquisition/response-recognition.md` | MOVED | v0.11 |
| `Continue Architecture Planning.md` | 57544–57581 | 4. Response Router | `acquisition/response-recognition.md` | MOVED | v0.11 |
| `Continue Architecture Planning.md` | 57583–57642 | 5. Provider priority | `acquisition/response-recognition.md` | MOVED | v0.11 |
| `Continue Architecture Planning.md` | 57644–57679 | 6. Recognition confidence | `acquisition/response-recognition.md` | MOVED | v0.11 |
| `Continue Architecture Planning.md` | 57681–57715 | 7. Content-type is only one signal | `acquisition/response-recognition.md` | MOVED | v0.11 |
| `Continue Architecture Planning.md` | 57717–57760 | 8. Recognition evidence | `acquisition/response-recognition.md` | MOVED | v0.11 |
| `Continue Architecture Planning.md` | 57762–57796 | 9. Recognition result contract | `acquisition/response-recognition.md` | MOVED | v0.11 |
| `Continue Architecture Planning.md` | 57798–57842 | 10. Why providers should not enqueue candidates | `acquisition/response-recognition.md` | MOVED | v0.11 |
| `Continue Architecture Planning.md` | 57844–57891 | 11. Recognition Runtime | `acquisition/response-recognition.md` | MOVED | v0.11 |
| `Continue Architecture Planning.md` | 57893–57897 | 12. Recognition failure taxonomy | `validation/failure-taxonomy.md` | MOVED | v0.11 |
| `Continue Architecture Planning.md` | 57899–57905 | 12. Recognition failure taxonomy › No recognizer | `acquisition/response-recognition.md` | MOVED | v0.11 |
| `Continue Architecture Planning.md` | 57907–57913 | 12. Recognition failure taxonomy › Provider rejected | `acquisition/response-recognition.md` | MOVED | v0.11 |
| `Continue Architecture Planning.md` | 57915–57921 | 12. Recognition failure taxonomy › Provider error | `acquisition/response-recognition.md` | MOVED | v0.11 |
| `Continue Architecture Planning.md` | 57923–57935 | 12. Recognition failure taxonomy › Successful recognition, zero discoveries | `acquisition/response-recognition.md` | MOVED | v0.11 |
| `Continue Architecture Planning.md` | 57937–57989 | 13. v0.11 state progression | `acquisition/response-recognition.md` | MOVED | v0.11 |
| `Continue Architecture Planning.md` | 57991–58034 | 14. Multiple recognizers | `acquisition/response-recognition.md` | MOVED | v0.11 |
| `Continue Architecture Planning.md` | 58036–58066 | 15. Recognition graph | `acquisition/response-recognition.md` | MOVED | v0.11 |
| `Continue Architecture Planning.md` | 58068–58127 | 16. The graph is now explicitly causal | `acquisition/response-recognition.md` | MOVED | v0.11 |
| `Continue Architecture Planning.md` | 58129–58167 | 17. v0.11 event ledger | `acquisition/response-recognition.md` | MOVED | v0.11 |
| `Continue Architecture Planning.md` | 58169–58238 | 18. The emerging generic algorithm | `acquisition/response-recognition.md` | MOVED | v0.11 |
| `Continue Architecture Planning.md` | 58240–58337 | 19. The next major abstraction: Candidate Sources | `roadmap/future-work.md` | MOVED | v0.11 |
| `Continue Architecture Planning.md` | 58343–58343 | *turn 36 you lead-in* | — (removed) | ARTIFACT | v0.11; conversation continuation marker |
| `Continue Architecture Planning.md` | 58349–58359 | v0.12 — Candidate Source Architecture | `providers/candidate-sources.md` | MOVED | v0.12 |
| `Continue Architecture Planning.md` | 58361–58416 | v0.12 — Candidate Source Architecture › 1. Three independent provider planes | `providers/overview.md` | MOVED | v0.12; explicit override |
| `Continue Architecture Planning.md` | 58418–58464 | 2. CandidateSource contract | `providers/candidate-sources.md` | MOVED | v0.12 |
| `Continue Architecture Planning.md` | 58466–58480 | 3. CandidateSource is a search-space adapter | `providers/candidate-sources.md` | MOVED | v0.12 |
| `Continue Architecture Planning.md` | 58482–58490 | 3. CandidateSource is a search-space adapter › Web page | `providers/candidate-sources.md` | MOVED | v0.12 |
| `Continue Architecture Planning.md` | 58492–58500 | 3. CandidateSource is a search-space adapter › Network traffic | `providers/candidate-sources.md` | MOVED | v0.12 |
| `Continue Architecture Planning.md` | 58502–58510 | 3. CandidateSource is a search-space adapter › Sitemap | `providers/candidate-sources.md` | MOVED | v0.12 |
| `Continue Architecture Planning.md` | 58512–58518 | 3. CandidateSource is a search-space adapter › User seed | `providers/candidate-sources.md` | MOVED | v0.12 |
| `Continue Architecture Planning.md` | 58520–58532 | 3. CandidateSource is a search-space adapter › Document | `providers/candidate-sources.md` | MOVED | v0.12 |
| `Continue Architecture Planning.md` | 58534–58595 | 4. CandidateProposal | `providers/candidate-sources.md` | MOVED | v0.12 |
| `Continue Architecture Planning.md` | 58597–58637 | 5. Why proposals matter | `providers/candidate-sources.md` | MOVED | v0.12 |
| `Continue Architecture Planning.md` | 58639–58710 | 6. CandidateNormalizer | `providers/candidate-sources.md` | MOVED | v0.12 |
| `Continue Architecture Planning.md` | 58712–58755 | 7. Source Registry | `providers/candidate-sources.md` | MOVED | v0.12 |
| `Continue Architecture Planning.md` | 58757–58811 | 8. The HTML provider should evolve | `providers/overview.md` | MOVED | v0.12; explicit override |
| `Continue Architecture Planning.md` | 58813–58864 | 9. Evidence becomes an intermediate layer | `providers/candidate-sources.md` | MOVED | v0.12 |
| `Continue Architecture Planning.md` | 58866–58894 | 10. Discovery becomes evidence-driven | `providers/candidate-sources.md` | MOVED | v0.12 |
| `Continue Architecture Planning.md` | 58896–58930 | 11. CandidateSource context | `providers/candidate-sources.md` | MOVED | v0.12 |
| `Continue Architecture Planning.md` | 58932–58932 | 12. CandidateSource examples | `providers/candidate-sources.md` | MOVED | v0.12 |
| `Continue Architecture Planning.md` | 58934–58978 | 12. CandidateSource examples › HTML link source | `providers/candidate-sources.md` | MOVED | v0.12 |
| `Continue Architecture Planning.md` | 58980–59027 | 13. NetworkSource | `providers/candidate-sources.md` | MOVED | v0.12 |
| `Continue Architecture Planning.md` | 59029–59056 | 14. Search-space composition | `providers/candidate-sources.md` | MOVED | v0.12 |
| `Continue Architecture Planning.md` | 59058–59094 | 15. Candidate identity | `providers/candidate-sources.md` | MOVED | v0.12 |
| `Continue Architecture Planning.md` | 59096–59144 | 16. Discovery confidence aggregation | `providers/candidate-sources.md` | MOVED | v0.12 |
| `Continue Architecture Planning.md` | 59146–59206 | 17. v0.12 provenance graph | `providers/candidate-sources.md` | MOVED | v0.12 |
| `Continue Architecture Planning.md` | 59208–59208 | 18. v0.12 invariants | `validation/invariants.md` | MOVED | v0.12 |
| `Continue Architecture Planning.md` | 59210–59215 | 18. v0.12 invariants › S1 — Source purity | `validation/invariants.md` | MOVED | v0.12 |
| `Continue Architecture Planning.md` | 59217–59222 | 18. v0.12 invariants › S2 — Core ownership | `validation/invariants.md` | MOVED | v0.12 |
| `Continue Architecture Planning.md` | 59224–59228 | 18. v0.12 invariants › S3 — Proposal semantics | `validation/invariants.md` | MOVED | v0.12 |
| `Continue Architecture Planning.md` | 59230–59235 | 18. v0.12 invariants › S4 — Identity | `validation/invariants.md` | MOVED | v0.12 |
| `Continue Architecture Planning.md` | 59237–59242 | 18. v0.12 invariants › S5 — Provenance | `validation/invariants.md` | MOVED | v0.12 |
| `Continue Architecture Planning.md` | 59244–59249 | 18. v0.12 invariants › S6 — Representability | `validation/invariants.md` | MOVED | v0.12 |
| `Continue Architecture Planning.md` | 59251–59265 | 18. v0.12 invariants › S7 — Observation independence | `validation/invariants.md` | MOVED | v0.12 |
| `Continue Architecture Planning.md` | 59267–59354 | 19. The complete v0.12 architecture | `architecture/system-model.md` | MOVED | v0.12 |
| `Continue Architecture Planning.md` | 59356–59396 | 20. The deeper abstraction | `concepts/overview.md` | MOVED | v0.12 |
| `Continue Architecture Planning.md` | 59398–59460 | 20. The deeper abstraction › v0.13 — the next boundary | `roadmap/future-work.md` | MOVED | v0.13 |
| `Continue Architecture Planning.md` | 59466–59466 | *turn 38 you lead-in* | — (removed) | ARTIFACT | v0.13; conversation continuation marker |
| `Continue Architecture Planning.md` | 59472–59493 | v0.13 — Discovery Controller | `architecture/discovery-model.md` | MOVED | v0.13 |
| `Continue Architecture Planning.md` | 59495–59546 | 1. The complete v0.13 architecture | `architecture/system-model.md` | MOVED | v0.13 |
| `Continue Architecture Planning.md` | 59548–59596 | 2. Two schedulers, not one | `architecture/scheduler.md` | MOVED | v0.13 |
| `Continue Architecture Planning.md` | 59598–59653 | 3. DiscoveryTask | `architecture/discovery-model.md` | MOVED | v0.13 |
| `Continue Architecture Planning.md` | 59655–59699 | 4. Why a task is necessary | `architecture/discovery-model.md` | MOVED | v0.13 |
| `Continue Architecture Planning.md` | 59701–59750 | 5. Source Policy | `architecture/discovery-model.md` | MOVED | v0.13 |
| `Continue Architecture Planning.md` | 59752–59783 | 6. Source budgets | `architecture/discovery-model.md` | MOVED | v0.13 |
| `Continue Architecture Planning.md` | 59785–59826 | 7. Proposal budget is different | `architecture/discovery-model.md` | MOVED | v0.13 |
| `Continue Architecture Planning.md` | 59828–59867 | 8. Incremental sources | `architecture/discovery-model.md` | MOVED | v0.13 |
| `Continue Architecture Planning.md` | 59869–59912 | 9. Source execution contract | `architecture/discovery-model.md` | MOVED | v0.13 |
| `Continue Architecture Planning.md` | 59914–59948 | 10. Source scheduling | `architecture/scheduler.md` | MOVED | v0.13 |
| `Continue Architecture Planning.md` | 59950–59994 | 11. Fairness | `architecture/scheduler.md` | MOVED | v0.13 |
| `Continue Architecture Planning.md` | 59996–60033 | 12. Candidate deduplication belongs after normalization | `architecture/candidate-model.md` | MOVED | v0.13 |
| `Continue Architecture Planning.md` | 60035–60076 | 13. Discovery provenance | `architecture/provenance.md` | MOVED | v0.13 |
| `Continue Architecture Planning.md` | 60078–60117 | 14. Candidate generation becomes transactional | `architecture/candidate-model.md` | MOVED | v0.13 |
| `Continue Architecture Planning.md` | 60119–60166 | 15. Concurrent source execution | `architecture/concurrency.md` | MOVED | v0.13 |
| `Continue Architecture Planning.md` | 60168–60208 | 16. DiscoveryController | `architecture/discovery-model.md` | MOVED | v0.13 |
| `Continue Architecture Planning.md` | 60210–60258 | 17. Event ledger | `architecture/discovery-model.md` | MOVED | v0.13 |
| `Continue Architecture Planning.md` | 60260–60288 | 18. Discovery failure taxonomy | `validation/failure-taxonomy.md` | MOVED | v0.13 |
| `Continue Architecture Planning.md` | 60290–60325 | 19. The generic blind-scan analogy is now much stronger | `research/dvb-blind-scan.md` | MOVED | v0.13 |
| `Continue Architecture Planning.md` | 60327–60327 | 20. v0.13 invariants | `validation/invariants.md` | MOVED | v0.13 |
| `Continue Architecture Planning.md` | 60329–60334 | 20. v0.13 invariants › D1 — Source isolation | `validation/invariants.md` | MOVED | v0.13 |
| `Continue Architecture Planning.md` | 60336–60341 | 20. v0.13 invariants › D2 — Acquisition isolation | `validation/invariants.md` | MOVED | v0.13 |
| `Continue Architecture Planning.md` | 60343–60348 | 20. v0.13 invariants › D3 — Normalization ownership | `validation/invariants.md` | MOVED | v0.13 |
| `Continue Architecture Planning.md` | 60350–60355 | 20. v0.13 invariants › D4 — Bounded generation | `validation/invariants.md` | MOVED | v0.13 |
| `Continue Architecture Planning.md` | 60357–60362 | 20. v0.13 invariants › D5 — Bounded recursion | `validation/invariants.md` | MOVED | v0.13 |
| `Continue Architecture Planning.md` | 60364–60369 | 20. v0.13 invariants › D6 — Provenance preservation | `validation/invariants.md` | MOVED | v0.13 |
| `Continue Architecture Planning.md` | 60371–60376 | 20. v0.13 invariants › D7 — Atomic task claiming | `validation/invariants.md` | MOVED | v0.13 |
| `Continue Architecture Planning.md` | 60378–60383 | 20. v0.13 invariants › D8 — Convergence | `validation/invariants.md` | MOVED | v0.13 |
| `Continue Architecture Planning.md` | 60385–60392 | 20. v0.13 invariants › D9 — Discovery/acquisition independence | `validation/invariants.md` | MOVED | v0.13 |
| `Continue Architecture Planning.md` | 60394–60484 | 21. The architecture is now approaching a stable core | `architecture/system-model.md` | MOVED | v0.13 |
| `Continue Architecture Planning.md` | 60486–60544 | v0.14 — the next missing abstraction | `roadmap/future-work.md` | MOVED | v0.14 |
| `Continue Architecture Planning.md` | 60550–60550 | *turn 40 you lead-in* | — (removed) | ARTIFACT | v0.14; conversation continuation marker |
| `Continue Architecture Planning.md` | 60556–60588 | v0.14 — DiscoveryDomain + ScanSession | `architecture/sessions-and-domains.md` | MOVED | v0.14 |
| `Continue Architecture Planning.md` | 60590–60610 | 1. The conceptual split | `architecture/sessions-and-domains.md` | MOVED | v0.14 |
| `Continue Architecture Planning.md` | 60612–60627 | 1. The conceptual split › Discovery Engine | `architecture/discovery-model.md` | MOVED | v0.14 |
| `Continue Architecture Planning.md` | 60629–60633 | 1. The conceptual split › DiscoveryDomain | `architecture/sessions-and-domains.md` | MOVED | v0.14 |
| `Continue Architecture Planning.md` | 60635–60647 | 1. The conceptual split › ScanSession | `architecture/sessions-and-domains.md` | MOVED | v0.14 |
| `Continue Architecture Planning.md` | 60649–60689 | 2. DVB analogy | `research/dvb-blind-scan.md` | MOVED | v0.14 |
| `Continue Architecture Planning.md` | 60691–60748 | 3. DiscoveryDomain | `architecture/sessions-and-domains.md` | MOVED | v0.14 |
| `Continue Architecture Planning.md` | 60750–60798 | 4. Domain vs policy | `architecture/sessions-and-domains.md` | MOVED | v0.14 |
| `Continue Architecture Planning.md` | 60800–60878 | 5. Domain membership | `architecture/sessions-and-domains.md` | MOVED | v0.14 |
| `Continue Architecture Planning.md` | 60880–60932 | 6. Explicit seeds | `architecture/sessions-and-domains.md` | MOVED | v0.14 |
| `Continue Architecture Planning.md` | 60934–60972 | 7. Seed ≠ Candidate | `architecture/sessions-and-domains.md` | MOVED | v0.14 |
| `Continue Architecture Planning.md` | 60974–61037 | 8. Discovery frontier | `architecture/discovery-model.md` | MOVED | v0.14 |
| `Continue Architecture Planning.md` | 61039–61102 | 9. ScanSession | `architecture/sessions-and-domains.md` | MOVED | v0.14 |
| `Continue Architecture Planning.md` | 61104–61147 | 10. Session lifecycle | `architecture/sessions-and-domains.md` | MOVED | v0.14 |
| `Continue Architecture Planning.md` | 61149–61153 | 11. Termination becomes explicit | `architecture/sessions-and-domains.md` | MOVED | v0.14 |
| `Continue Architecture Planning.md` | 61155–61165 | 11. Termination becomes explicit › Frontier exhaustion | `architecture/sessions-and-domains.md` | MOVED | v0.14; explicit override |
| `Continue Architecture Planning.md` | 61167–61171 | 11. Termination becomes explicit › Candidate limit | `architecture/sessions-and-domains.md` | MOVED | v0.14; explicit override |
| `Continue Architecture Planning.md` | 61173–61177 | 11. Termination becomes explicit › Acquisition limit | `architecture/sessions-and-domains.md` | MOVED | v0.14; explicit override |
| `Continue Architecture Planning.md` | 61179–61183 | 11. Termination becomes explicit › Discovery-task limit | `architecture/sessions-and-domains.md` | MOVED | v0.14; explicit override |
| `Continue Architecture Planning.md` | 61185–61189 | 11. Termination becomes explicit › Proposal limit | `architecture/sessions-and-domains.md` | MOVED | v0.14 |
| `Continue Architecture Planning.md` | 61191–61195 | 11. Termination becomes explicit › Depth limit | `architecture/sessions-and-domains.md` | MOVED | v0.14 |
| `Continue Architecture Planning.md` | 61197–61201 | 11. Termination becomes explicit › Time limit | `architecture/sessions-and-domains.md` | MOVED | v0.14 |
| `Continue Architecture Planning.md` | 61203–61209 | 11. Termination becomes explicit › External stop | `architecture/sessions-and-domains.md` | MOVED | v0.14 |
| `Continue Architecture Planning.md` | 61211–61265 | 12. Termination evaluator | `architecture/sessions-and-domains.md` | MOVED | v0.14 |
| `Continue Architecture Planning.md` | 61267–61306 | 13. Limit reached ≠ successful completion | `architecture/sessions-and-domains.md` | MOVED | v0.14 |
| `Continue Architecture Planning.md` | 61308–61352 | 14. The session snapshot | `architecture/sessions-and-domains.md` | MOVED | v0.14 |
| `Continue Architecture Planning.md` | 61354–61413 | 15. Resumability | `architecture/sessions-and-domains.md` | MOVED | v0.14 |
| `Continue Architecture Planning.md` | 61415–61461 | 16. Lease-based claims | `architecture/concurrency.md` | MOVED | v0.14 |
| `Continue Architecture Planning.md` | 61463–61501 | 17. Session ownership | `architecture/sessions-and-domains.md` | MOVED | v0.14 |
| `Continue Architecture Planning.md` | 61503–61557 | 18. Scan vs engine knowledge | `architecture/sessions-and-domains.md` | MOVED | v0.14 |
| `Continue Architecture Planning.md` | 61559–61615 | 19. Domain snapshot vs mutable domain | `architecture/sessions-and-domains.md` | MOVED | v0.14 |
| `Continue Architecture Planning.md` | 61617–61666 | 20. Domain identity | `architecture/sessions-and-domains.md` | MOVED | v0.14 |
| `Continue Architecture Planning.md` | 61668–61695 | 21. Search frontier vs knowledge graph | `architecture/sessions-and-domains.md` | MOVED | v0.14 |
| `Continue Architecture Planning.md` | 61697–61772 | 22. The complete v0.14 architecture | `architecture/system-model.md` | MOVED | v0.14 |
| `Continue Architecture Planning.md` | 61774–61787 | 23. Four distinct scopes | `architecture/sessions-and-domains.md` | MOVED | v0.14 |
| `Continue Architecture Planning.md` | 61789–61789 | 24. Strong invariants | `validation/invariants.md` | MOVED | v0.14 |
| `Continue Architecture Planning.md` | 61791–61797 | 24. Strong invariants › Domain invariant | `validation/invariants.md` | MOVED | v0.14 |
| `Continue Architecture Planning.md` | 61799–61803 | 24. Strong invariants › Session invariant | `validation/invariants.md` | MOVED | v0.14 |
| `Continue Architecture Planning.md` | 61805–61809 | 24. Strong invariants › Snapshot invariant | `validation/invariants.md` | MOVED | v0.14 |
| `Continue Architecture Planning.md` | 61811–61816 | 24. Strong invariants › Frontier invariant | `validation/invariants.md` | MOVED | v0.14 |
| `Continue Architecture Planning.md` | 61818–61822 | 24. Strong invariants › Termination invariant | `validation/invariants.md` | MOVED | v0.14 |
| `Continue Architecture Planning.md` | 61824–61829 | 24. Strong invariants › Recovery invariant | `validation/invariants.md` | MOVED | v0.14 |
| `Continue Architecture Planning.md` | 61831–61836 | 24. Strong invariants › Provenance invariant | `validation/invariants.md` | MOVED | v0.14 |
| `Continue Architecture Planning.md` | 61838–61842 | 24. Strong invariants › Acquisition invariant | `validation/invariants.md` | MOVED | v0.14 |
| `Continue Architecture Planning.md` | 61844–61850 | 24. Strong invariants › Discovery invariant | `validation/invariants.md` | MOVED | v0.14 |
| `Continue Architecture Planning.md` | 61852–61884 | 25. Failure taxonomy | `validation/failure-taxonomy.md` | MOVED | v0.14 |
| `Continue Architecture Planning.md` | 61886–61918 | 26. What v0.14 changes conceptually | `architecture/sessions-and-domains.md` | MOVED | v0.14 |
| `Continue Architecture Planning.md` | 61920–61952 | 27. The next abstraction | `roadmap/future-work.md` | MOVED | v0.14 |
| `Continue Architecture Planning.md` | 61954–61988 | v0.15 — WorkItem + Frontier Runtime | `architecture/work-and-frontier.md` | MOVED | v0.15 |
| `Continue Architecture Planning.md` | 61994–61994 | *turn 42 you lead-in* | — (removed) | ARTIFACT | v0.15; conversation continuation marker |
| `Continue Architecture Planning.md` | 62000–62029 | v0.15 — WorkItem + Frontier Runtime | `architecture/work-and-frontier.md` | MOVED | v0.15 |
| `Continue Architecture Planning.md` | 62031–62070 | 1. The key distinction | `architecture/work-and-frontier.md` | MOVED | v0.15 |
| `Continue Architecture Planning.md` | 62072–62129 | 2. Why `WorkItem` exists | `architecture/work-and-frontier.md` | MOVED | v0.15 |
| `Continue Architecture Planning.md` | 62131–62207 | 3. WorkItem | `architecture/work-and-frontier.md` | MOVED | v0.15 |
| `Continue Architecture Planning.md` | 62209–62242 | 4. Work kinds | `architecture/work-and-frontier.md` | MOVED | v0.15 |
| `Continue Architecture Planning.md` | 62244–62294 | 5. Work payload | `architecture/work-and-frontier.md` | MOVED | v0.15 |
| `Continue Architecture Planning.md` | 62296–62347 | 6. Work lifecycle | `architecture/work-and-frontier.md` | MOVED | v0.15 |
| `Continue Architecture Planning.md` | 62349–62425 | 7. Claiming becomes a formal protocol | `architecture/concurrency.md` | MOVED | v0.15 |
| `Continue Architecture Planning.md` | 62427–62458 | 8. Work lease | `architecture/concurrency.md` | MOVED | v0.15 |
| `Continue Architecture Planning.md` | 62460–62490 | 9. Lease recovery | `architecture/concurrency.md` | MOVED | v0.15 |
| `Continue Architecture Planning.md` | 62492–62528 | 10. Frontier Runtime | `architecture/work-and-frontier.md` | MOVED | v0.15 |
| `Continue Architecture Planning.md` | 62530–62568 | 11. WorkScheduler | `architecture/scheduler.md` | MOVED | v0.15 |
| `Continue Architecture Planning.md` | 62570–62597 | 12. Priority starvation | `architecture/scheduler.md` | MOVED | v0.15 |
| `Continue Architecture Planning.md` | 62599–62640 | 13. Priority aging | `architecture/scheduler.md` | MOVED | v0.15 |
| `Continue Architecture Planning.md` | 62642–62695 | 14. Discovery and acquisition fairness | `acquisition/acquisition-model.md` | MOVED | v0.15 |
| `Continue Architecture Planning.md` | 62697–62734 | 15. Why not one giant queue? | `architecture/work-and-frontier.md` | MOVED | v0.15 |
| `Continue Architecture Planning.md` | 62736–62778 | 16. Work dependencies | `architecture/work-and-frontier.md` | MOVED | v0.15 |
| `Continue Architecture Planning.md` | 62780–62798 | 17. But dependencies must not create hidden coupling | `architecture/work-and-frontier.md` | MOVED | v0.15 |
| `Continue Architecture Planning.md` | 62800–62830 | 18. Dependency states | `architecture/work-and-frontier.md` | MOVED | v0.15 |
| `Continue Architecture Planning.md` | 62832–62873 | 19. Work completion | `architecture/work-and-frontier.md` | MOVED | v0.15 |
| `Continue Architecture Planning.md` | 62875–62933 | 20. Work execution boundary | `architecture/work-and-frontier.md` | MOVED | v0.15 |
| `Continue Architecture Planning.md` | 62935–62977 | 21. Work Runtime | `architecture/work-and-frontier.md` | MOVED | v0.15 |
| `Continue Architecture Planning.md` | 62979–63027 | 22. Retry becomes generic | `architecture/work-and-frontier.md` | MOVED | v0.15 |
| `Continue Architecture Planning.md` | 63029–63071 | 23. Retry identity | `architecture/work-and-frontier.md` | MOVED | v0.15 |
| `Continue Architecture Planning.md` | 63073–63108 | 24. Cancellation | `architecture/work-and-frontier.md` | MOVED | v0.15 |
| `Continue Architecture Planning.md` | 63110–63150 | 25. Scan termination with WorkItems | `architecture/work-and-frontier.md` | MOVED | v0.15 |
| `Continue Architecture Planning.md` | 63152–63180 | 26. The three frontier states | `architecture/work-and-frontier.md` | MOVED | v0.15 |
| `Continue Architecture Planning.md` | 63182–63219 | 27. Scheduled work | `architecture/scheduler.md` | MOVED | v0.15 |
| `Continue Architecture Planning.md` | 63221–63264 | 28. Work state machine | `architecture/work-and-frontier.md` | MOVED | v0.15 |
| `Continue Architecture Planning.md` | 63266–63290 | 29. Domain → Session → Work | `architecture/work-and-frontier.md` | MOVED | v0.15 |
| `Continue Architecture Planning.md` | 63292–63312 | 30. What belongs where? | `architecture/work-and-frontier.md` | MOVED | v0.15 |
| `Continue Architecture Planning.md` | 63314–63350 | 31. The crucial invariant | `validation/invariants.md` | MOVED | v0.15 |
| `Continue Architecture Planning.md` | 63352–63388 | 32. Discovery vs acquisition remains intact | `acquisition/acquisition-model.md` | MOVED | v0.15 |
| `Continue Architecture Planning.md` | 63390–63430 | 33. The resulting architecture | `architecture/system-model.md` | MOVED | v0.15 |
| `Continue Architecture Planning.md` | 63432–63497 | 34. v0.15 architectural result | `architecture/work-and-frontier.md` | MOVED | v0.15 |
| `Continue Architecture Planning.md` | 63503–63503 | *turn 44 you lead-in* | — (removed) | ARTIFACT | v0.15; conversation continuation marker |
| `Continue Architecture Planning.md` | 63509–63552 | v0.16 — EvidenceGraph + Provenance | `architecture/evidence-model.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 63554–63588 | 1. The new abstraction | `architecture/evidence-model.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 63590–63592 | 2. Observation ≠ Evidence ≠ Claim | `architecture/observation-model.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 63594–63605 | 2. Observation ≠ Evidence ≠ Claim › Observation | `architecture/observation-model.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 63607–63620 | 2. Observation ≠ Evidence ≠ Claim › Evidence | `architecture/evidence-model.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 63622–63644 | 2. Observation ≠ Evidence ≠ Claim › Claim | `architecture/evidence-model.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 63646–63685 | 3. Resource ≠ Claim | `architecture/evidence-model.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 63687–63720 | 4. EvidenceGraph | `architecture/evidence-model.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 63722–63774 | 5. Provenance | `architecture/provenance.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 63776–63817 | 6. Evidence object | `architecture/evidence-model.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 63819–63890 | 7. Locator | `architecture/evidence-model.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 63892–63944 | 8. Claim | `architecture/evidence-model.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 63946–63992 | 9. Claims should not be confused with truth | `architecture/evidence-model.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 63994–64019 | 10. Evidence strength | `architecture/evidence-model.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 64021–64056 | 11. Independent evidence | `architecture/evidence-model.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 64058–64102 | 12. Evidence independence | `architecture/evidence-model.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 64104–64157 | 13. Evidence graph edges | `architecture/evidence-model.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 64159–64190 | 14. Why graph edges matter | `architecture/evidence-model.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 64192–64240 | 15. Provenance graph | `architecture/provenance.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 64242–64285 | 16. Resource identity | `architecture/evidence-model.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 64287–64321 | 17. Resource fingerprint | `architecture/evidence-model.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 64323–64369 | 18. URL identity vs content identity | `architecture/evidence-model.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 64371–64406 | 19. Revision detection | `architecture/evidence-model.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 64408–64441 | 20. Observation immutability | `architecture/observation-model.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 64443–64481 | 21. Evidence immutability | `architecture/evidence-model.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 64483–64512 | 22. Extraction method becomes first-class | `architecture/evidence-model.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 64514–64555 | 23. Verification | `validation/verification.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 64557–64607 | 24. Evidence lifecycle | `architecture/evidence-model.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 64609–64655 | 25. Evidence states | `architecture/evidence-model.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 64657–64687 | 26. Claims can conflict | `architecture/evidence-model.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 64689–64719 | 27. Evidence resolution | `architecture/evidence-model.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 64721–64756 | 28. Discovery confidence changes meaning | `architecture/discovery-model.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 64758–64784 | 29. Candidate provenance | `architecture/provenance.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 64786–64816 | 30. The evidence ledger | `architecture/evidence-model.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 64818–64847 | 31. Two complementary graphs | `architecture/evidence-model.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 64849–64929 | 32. Example end-to-end trace | `architecture/evidence-model.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 64931–64989 | 33. v0.16 architecture | `architecture/system-model.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 64991–64991 | 34. New invariants | `validation/invariants.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 64993–64999 | 34. New invariants › Evidence provenance | `architecture/evidence-model.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 65001–65005 | 34. New invariants › Claim support | `architecture/evidence-model.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 65007–65011 | 34. New invariants › Historical integrity | `architecture/evidence-model.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 65013–65017 | 34. New invariants › Extraction integrity | `architecture/evidence-model.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 65019–65024 | 34. New invariants › Resource identity | `architecture/evidence-model.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 65026–65030 | 34. New invariants › Content identity | `architecture/evidence-model.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 65032–65037 | 34. New invariants › Conflict preservation | `architecture/evidence-model.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 65039–65043 | 34. New invariants › Provenance preservation | `architecture/provenance.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 65045–65052 | 34. New invariants › Session provenance | `architecture/provenance.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 65054–65084 | 35. Failure taxonomy | `validation/failure-taxonomy.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 65086–65156 | 36. The deeper architectural transition | `roadmap/future-work.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 65158–65160 | 37. What is still missing | `roadmap/future-work.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 65162–65166 | 37. What is still missing › Search space | `architecture/search-space.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 65168–65172 | 37. What is still missing › Execution | `architecture/evidence-model.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 65174–65178 | 37. What is still missing › Work | `architecture/evidence-model.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 65180–65184 | 37. What is still missing › Acquisition | `acquisition/acquisition-model.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 65186–65190 | 37. What is still missing › Recognition | `acquisition/response-recognition.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 65192–65196 | 37. What is still missing › Discovery | `architecture/discovery-model.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 65198–65202 | 37. What is still missing › Evidence | `architecture/evidence-model.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 65204–65214 | 37. What is still missing › History | `architecture/evidence-model.md` | MOVED | v0.16 |
| `Continue Architecture Planning.md` | 65216–65240 | v0.17 — ResourceGraph + Identity Resolution | `architecture/resource-model.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 65246–65246 | *turn 46 you lead-in* | — (removed) | ARTIFACT | v0.17; conversation continuation marker |
| `Continue Architecture Planning.md` | 65252–65295 | v0.17 — ResourceGraph + Identity Resolution | `architecture/resource-model.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 65297–65336 | 1. The core problem | `architecture/resource-model.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 65338–65371 | 2. Resource identity must become graph-based | `architecture/resource-model.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 65373–65375 | 3. Candidate vs Resource vs Locator | `architecture/resource-model.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 65377–65385 | 3. Candidate vs Resource vs Locator › Candidate | `architecture/resource-model.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 65387–65395 | 3. Candidate vs Resource vs Locator › Locator | `architecture/resource-model.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 65397–65429 | 3. Candidate vs Resource vs Locator › Resource | `architecture/resource-model.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 65431–65477 | 4. Why not simply canonicalize everything? | `architecture/resource-model.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 65479–65526 | 5. Locator | `architecture/resource-model.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 65528–65570 | 6. Resource | `architecture/resource-model.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 65572–65613 | 7. Resource relationships | `architecture/resource-model.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 65615–65653 | 8. Redirects | `architecture/resource-model.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 65655–65693 | 9. Redirect chain | `architecture/resource-model.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 65695–65726 | 10. Content fingerprints | `architecture/resource-model.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 65728–65775 | 11. Same content does not prove same resource | `architecture/resource-model.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 65777–65814 | 12. Representation identity | `architecture/resource-model.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 65816–65848 | 13. Identity Evidence | `architecture/evidence-model.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 65850–65890 | 14. IdentityResolver | `architecture/resource-model.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 65892–65916 | 15. Identity confidence should be relational | `architecture/resource-model.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 65918–65952 | 16. Identity classes | `architecture/resource-model.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 65954–65990 | 17. No destructive merges | `architecture/resource-model.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 65992–66040 | 18. ResourceGraph | `architecture/resource-model.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 66042–66080 | 19. Graph edge contract | `architecture/resource-model.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 66082–66119 | 20. Identity resolution pipeline | `architecture/resource-model.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 66121–66167 | 21. Canonical URL is still important | `architecture/resource-model.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 66169–66195 | 22. Canonicalization provenance | `architecture/provenance.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 66197–66235 | 23. Identity resolution must be monotonic where possible | `architecture/resource-model.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 66237–66274 | 24. Resource revisions | `architecture/resource-model.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 66276–66303 | 25. Revision object | `architecture/resource-model.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 66305–66323 | 26. ResourceGraph vs KnowledgeBase | `architecture/resource-model.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 66325–66327 | 27. Querying the graph | `architecture/strategy-and-planning.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 66329–66333 | 27. Querying the graph › What URLs identify this resource? | `architecture/resource-model.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 66335–66342 | 27. Querying the graph › Where was it discovered? | `architecture/resource-model.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 66344–66348 | 27. Querying the graph › What URLs redirect to it? | `architecture/resource-model.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 66350–66354 | 27. Querying the graph › Which URLs have identical observed bytes? | `architecture/resource-model.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 66356–66362 | 27. Querying the graph › Has this resource changed? | `architecture/resource-model.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 66364–66378 | 27. Querying the graph › Why do we believe two URLs are related? | `architecture/resource-model.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 66380–66420 | 28. Resource graph example | `architecture/resource-model.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 66422–66448 | 29. Failure taxonomy | `validation/failure-taxonomy.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 66450–66450 | 30. Core invariants | `validation/invariants.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 66452–66457 | 30. Core invariants › Locator preservation | `architecture/resource-model.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 66459–66464 | 30. Core invariants › No destructive merge | `architecture/resource-model.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 66466–66471 | 30. Core invariants › Fingerprint independence | `architecture/resource-model.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 66473–66478 | 30. Core invariants › Redirect independence | `architecture/resource-model.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 66480–66485 | 30. Core invariants › Evidence-backed identity | `architecture/evidence-model.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 66487–66492 | 30. Core invariants › Revision preservation | `architecture/resource-model.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 66494–66501 | 30. Core invariants › Canonicalization transparency | `architecture/resource-model.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 66503–66560 | 31. The new architecture | `architecture/system-model.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 66562–66606 | 32. The deeper model | `concepts/overview.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 66608–66651 | 33. The important transition | `architecture/resource-model.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 66653–66694 | 34. Next missing abstraction | `roadmap/future-work.md` | MOVED | v0.17 |
| `Continue Architecture Planning.md` | 66696–66734 | v0.18 — Resource Type System + Semantic Classification | `architecture/classification.md` | MOVED | v0.18 |
| `Continue Architecture Planning.md` | 66740–66740 | *turn 48 you lead-in* | — (removed) | ARTIFACT | v0.18; conversation continuation marker |
| `Continue Architecture Planning.md` | 66746–66789 | v0.18 — Resource Type System + Semantic Classification | `architecture/classification.md` | MOVED | v0.18 |
| `Continue Architecture Planning.md` | 66791–66853 | 18.1 The Type Problem | `architecture/classification.md` | MOVED | v0.18 |
| `Continue Architecture Planning.md` | 66855–66915 | 18.2 Four Orthogonal Type Dimensions | `architecture/classification.md` | MOVED | v0.18 |
| `Continue Architecture Planning.md` | 66917–66975 | 18.3 ResourceType | `architecture/classification.md` | MOVED | v0.18 |
| `Continue Architecture Planning.md` | 66977–67046 | 18.4 Classification Assertion | `architecture/classification.md` | MOVED | v0.18 |
| `Continue Architecture Planning.md` | 67048–67116 | 18.5 Type Evidence | `architecture/classification.md` | MOVED | v0.18 |
| `Continue Architecture Planning.md` | 67118–67166 | 18.6 Evidence Strength Must Be Axis-Specific | `architecture/classification.md` | MOVED | v0.18 |
| `Continue Architecture Planning.md` | 67168–67201 | 18.7 Classification Pipeline | `architecture/classification.md` | MOVED | v0.18 |
| `Continue Architecture Planning.md` | 67203–67205 | 18.8 Recognition vs Classification | `architecture/classification.md` | MOVED | v0.18 |
| `Continue Architecture Planning.md` | 67207–67224 | 18.8 Recognition vs Classification › Recognition | `architecture/classification.md` | MOVED | v0.18 |
| `Continue Architecture Planning.md` | 67226–67264 | 18.8 Recognition vs Classification › Classification | `architecture/classification.md` | MOVED | v0.18 |
| `Continue Architecture Planning.md` | 67266–67329 | 18.9 Classification Runtime | `architecture/classification.md` | MOVED | v0.18 |
| `Continue Architecture Planning.md` | 67331–67380 | 18.10 Example Classifiers | `architecture/classification.md` | MOVED | v0.18 |
| `Continue Architecture Planning.md` | 67382–67434 | 18.11 Hierarchical Classification | `architecture/classification.md` | MOVED | v0.18 |
| `Continue Architecture Planning.md` | 67436–67483 | 18.12 Do Not Use One Global Confidence Score | `architecture/classification.md` | MOVED | v0.18 |
| `Continue Architecture Planning.md` | 67485–67526 | 18.13 Classification Is Versioned | `architecture/classification.md` | MOVED | v0.18 |
| `Continue Architecture Planning.md` | 67528–67571 | 18.14 Contradictory Classification | `architecture/classification.md` | MOVED | v0.18 |
| `Continue Architecture Planning.md` | 67573–67615 | 18.15 Classification Graph | `architecture/classification.md` | MOVED | v0.18 |
| `Continue Architecture Planning.md` | 67617–67658 | 18.16 Resource Model After v0.18 | `architecture/classification.md` | MOVED | v0.18 |
| `Continue Architecture Planning.md` | 67660–67735 | 18.17 Resource Type Registry | `architecture/classification.md` | MOVED | v0.18 |
| `Continue Architecture Planning.md` | 67737–67794 | 18.18 Classification Must Not Become Acquisition Policy | `acquisition/acquisition-model.md` | MOVED | v0.18 |
| `Continue Architecture Planning.md` | 67796–67823 | 18.19 Classification → Strategy | `architecture/classification.md` | MOVED | v0.18 |
| `Continue Architecture Planning.md` | 67825–67866 | 18.20 Classification Work as WorkItem | `architecture/classification.md` | MOVED | v0.18 |
| `Continue Architecture Planning.md` | 67868–67937 | 18.21 End-to-End Architecture | `architecture/system-model.md` | MOVED | v0.18 |
| `Continue Architecture Planning.md` | 67939–67964 | 18.22 Failure Taxonomy | `validation/failure-taxonomy.md` | MOVED | v0.18 |
| `Continue Architecture Planning.md` | 67966–67966 | 18.23 Core Invariants | `validation/invariants.md` | MOVED | v0.18 |
| `Continue Architecture Planning.md` | 67968–67974 | 18.23 Core Invariants › Invariant 1 — Type is not identity | `validation/invariants.md` | MOVED | v0.18 |
| `Continue Architecture Planning.md` | 67976–67982 | 18.23 Core Invariants › Invariant 2 — URL does not determine semantic type | `validation/invariants.md` | MOVED | v0.18 |
| `Continue Architecture Planning.md` | 67984–67990 | 18.23 Core Invariants › Invariant 3 — Technical recognition does not determine semantic role | `validation/invariants.md` | MOVED | v0.18 |
| `Continue Architecture Planning.md` | 67992–67998 | 18.23 Core Invariants › Invariant 4 — Classification requires evidence | `validation/invariants.md` | MOVED | v0.18 |
| `Continue Architecture Planning.md` | 68000–68006 | 18.23 Core Invariants › Invariant 5 — Classification does not imply authorization | `validation/invariants.md` | MOVED | v0.18 |
| `Continue Architecture Planning.md` | 68008–68018 | 18.23 Core Invariants › Invariant 6 — Historical classification is immutable | `validation/invariants.md` | MOVED | v0.18 |
| `Continue Architecture Planning.md` | 68020–68028 | 18.23 Core Invariants › Invariant 7 — Contradiction is preserved | `validation/invariants.md` | MOVED | v0.18 |
| `Continue Architecture Planning.md` | 68030–68042 | 18.23 Core Invariants › Invariant 8 — Type axes remain independent | `validation/invariants.md` | MOVED | v0.18 |
| `Continue Architecture Planning.md` | 68044–68081 | 18.24 The Larger Concept | `concepts/overview.md` | MOVED | v0.18 |
| `Continue Architecture Planning.md` | 68083–68147 | v0.19 — Resource Representation & Revision Model | `architecture/resource-model.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 68153–68153 | *turn 50 you lead-in* | — (removed) | ARTIFACT | v0.19; conversation continuation marker |
| `Continue Architecture Planning.md` | 68159–68177 | v0.19 — Resource Representation + Artifact + Revision Model | `architecture/resource-model.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 68179–68207 | v0.19 — Resource Representation + Artifact + Revision Model › 19.1 The Core Distinction | `architecture/resource-model.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 68209–68217 | 19.1 The Core Distinction › Resource | `architecture/resource-model.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 68219–68228 | 19.1 The Core Distinction › Representation | `architecture/resource-model.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 68230–68237 | 19.1 The Core Distinction › Artifact | `architecture/resource-model.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 68239–68250 | 19.1 The Core Distinction › Observation | `architecture/observation-model.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 68252–68300 | 19.2 Why Resource → Artifact Is Wrong | `architecture/resource-model.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 68302–68417 | 19.3 New Data Model | `architecture/resource-model.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 68419–68463 | 19.4 The Complete Identity Chain | `architecture/resource-model.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 68465–68516 | 19.5 Representation Is Not Just MIME | `architecture/resource-model.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 68518–68543 | 19.6 Representation Relations | `architecture/resource-model.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 68545–68591 | 19.7 Artifact Identity | `architecture/resource-model.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 68593–68636 | 19.8 Content Equivalence | `architecture/resource-model.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 68638–68678 | 19.9 Revision Detection | `architecture/resource-model.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 68680–68729 | 19.10 Revision Detection Is Not Always Proof of Semantic Revision | `architecture/resource-model.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 68731–68772 | 19.11 Revision Evidence | `architecture/resource-model.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 68774–68809 | 19.12 HTTP Validators Become Evidence | `architecture/resource-model.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 68811–68864 | 19.13 Conditional Acquisition | `acquisition/acquisition-model.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 68866–68902 | 19.14 Observation Becomes the Historical Bridge | `architecture/observation-model.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 68904–68935 | 19.15 Resource State vs Artifact State | `architecture/resource-model.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 68937–68945 | 19.15 Resource State vs Artifact State › Resource state | `architecture/resource-model.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 68947–68955 | 19.15 Resource State vs Artifact State › Artifact state | `architecture/resource-model.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 68957–68969 | 19.15 Resource State vs Artifact State › Observation state | `architecture/observation-model.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 68971–69004 | 19.16 ResourceGraph v0.19 | `architecture/resource-model.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 69006–69073 | 19.17 ResourceGraph API | `architecture/resource-model.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 69075–69087 | 19.18 Artifact Deduplication | `architecture/resource-model.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 69089–69095 | 19.18 Artifact Deduplication › Locator deduplication | `architecture/resource-model.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 69097–69127 | 19.18 Artifact Deduplication › Artifact deduplication | `architecture/resource-model.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 69129–69181 | 19.19 Content-Addressed Storage | `architecture/resource-model.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 69183–69220 | 19.20 Verification Levels | `validation/verification.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 69222–69271 | 19.21 Independent Confirmation | `architecture/resource-model.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 69273–69310 | 19.22 Resource Confidence | `architecture/resource-model.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 69312–69318 | 19.23 Example | `architecture/resource-model.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 69320–69325 | 19.23 Example › Step 1 — Locator | `architecture/resource-model.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 69327–69331 | 19.23 Example › Step 2 — Resource | `architecture/resource-model.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 69333–69339 | 19.23 Example › Step 3 — Observation | `architecture/observation-model.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 69341–69346 | 19.23 Example › Step 4 — Artifact | `architecture/resource-model.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 69348–69354 | 19.23 Example › Step 5 — Representation | `architecture/resource-model.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 69356–69361 | 19.23 Example › Step 6 — Classification | `architecture/resource-model.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 69363–69397 | 19.23 Example › Step 7 — Revision | `architecture/resource-model.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 69399–69452 | 19.24 A More Precise End-to-End Pipeline | `architecture/resource-model.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 69454–69454 | 19.25 New Invariants | `validation/invariants.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 69456–69464 | 19.25 New Invariants › Artifact invariant | `validation/invariants.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 69466–69472 | 19.25 New Invariants › Resource invariant | `validation/invariants.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 69474–69488 | 19.25 New Invariants › Representation invariant | `validation/invariants.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 69490–69498 | 19.25 New Invariants › Revision invariant | `validation/invariants.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 69500–69507 | 19.25 New Invariants › Observation invariant | `validation/invariants.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 69509–69515 | 19.25 New Invariants › Deduplication invariant | `validation/invariants.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 69517–69531 | 19.25 New Invariants › Change invariant | `validation/invariants.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 69533–69542 | 19.25 New Invariants › Classification invariant | `validation/invariants.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 69544–69567 | 19.26 Failure Modes | `validation/failure-taxonomy.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 69569–69657 | 19.27 What v0.19 Gives Us | `architecture/resource-model.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 69659–69688 | 19.27 What v0.19 Gives Us › Next boundary: v0.20 — Search-Space Partitioning + Discovery Strategies | `roadmap/future-work.md` | MOVED | v0.19 |
| `Continue Architecture Planning.md` | 69694–69694 | *turn 52 you lead-in* | — (removed) | ARTIFACT | v0.19; conversation continuation marker |
| `Continue Architecture Planning.md` | 69700–69732 | v0.20 — Search-Space Partitioning + Discovery Strategies | `architecture/search-space.md` | MOVED | v0.20 |
| `Continue Architecture Planning.md` | 69734–69768 | 20.1 The Search Space | `architecture/search-space.md` | MOVED | v0.20 |
| `Continue Architecture Planning.md` | 69770–69809 | 20.2 What Is a Partition? | `architecture/search-space.md` | MOVED | v0.20 |
| `Continue Architecture Planning.md` | 69811–69841 | 20.3 Partition ≠ Candidate | `architecture/search-space.md` | MOVED | v0.20 |
| `Continue Architecture Planning.md` | 69843–69906 | 20.4 Partition Object | `architecture/search-space.md` | MOVED | v0.20 |
| `Continue Architecture Planning.md` | 69908–69945 | 20.5 Partition State | `architecture/search-space.md` | MOVED | v0.20 |
| `Continue Architecture Planning.md` | 69947–69949 | 20.5 Partition State › Saturated | `architecture/search-space.md` | MOVED | v0.20 |
| `Continue Architecture Planning.md` | 69951–69957 | 20.5 Partition State › Exhausted | `architecture/search-space.md` | MOVED | v0.20 |
| `Continue Architecture Planning.md` | 69959–69993 | 20.6 Search Coverage | `architecture/search-space.md` | MOVED | v0.20 |
| `Continue Architecture Planning.md` | 69995–70024 | 20.7 Strategy Contract | `architecture/search-space.md` | MOVED | v0.20 |
| `Continue Architecture Planning.md` | 70026–70060 | 20.8 Strategy vs Candidate Source | `architecture/search-space.md` | MOVED | v0.20 |
| `Continue Architecture Planning.md` | 70062–70064 | 20.9 Strategy Types | `architecture/search-space.md` | MOVED | v0.20 |
| `Continue Architecture Planning.md` | 70066–70078 | 20.9 Strategy Types › Seed Expansion | `architecture/search-space.md` | MOVED | v0.20 |
| `Continue Architecture Planning.md` | 70080–70088 | 20.9 Strategy Types › Repository Expansion | `architecture/search-space.md` | MOVED | v0.20 |
| `Continue Architecture Planning.md` | 70090–70098 | 20.9 Strategy Types › Sitemap Expansion | `architecture/search-space.md` | MOVED | v0.20 |
| `Continue Architecture Planning.md` | 70100–70110 | 20.9 Strategy Types › API Schema Expansion | `architecture/search-space.md` | MOVED | v0.20 |
| `Continue Architecture Planning.md` | 70112–70127 | 20.9 Strategy Types › Document-Family Expansion | `architecture/search-space.md` | MOVED | v0.20 |
| `Continue Architecture Planning.md` | 70129–70195 | 20.10 Blind-Scan Analogy | `research/dvb-blind-scan.md` | MOVED | v0.20 |
| `Continue Architecture Planning.md` | 70197–70227 | 20.11 Probe | `architecture/search-space.md` | MOVED | v0.20 |
| `Continue Architecture Planning.md` | 70229–70282 | 20.12 Exploration Plan | `architecture/search-space.md` | MOVED | v0.20 |
| `Continue Architecture Planning.md` | 70284–70320 | 20.13 Exploration Must Remain Budgeted | `architecture/search-space.md` | MOVED | v0.20 |
| `Continue Architecture Planning.md` | 70322–70373 | 20.14 Adaptive Partition Priority | `architecture/search-space.md` | MOVED | v0.20 |
| `Continue Architecture Planning.md` | 70375–70409 | 20.15 Exploration vs Exploitation | `architecture/search-space.md` | MOVED | v0.20 |
| `Continue Architecture Planning.md` | 70411–70444 | 20.16 Aging | `architecture/search-space.md` | MOVED | v0.20 |
| `Continue Architecture Planning.md` | 70446–70512 | 20.17 Partition Splitting | `architecture/search-space.md` | MOVED | v0.20 |
| `Continue Architecture Planning.md` | 70514–70550 | 20.18 Partition Merge | `architecture/search-space.md` | MOVED | v0.20 |
| `Continue Architecture Planning.md` | 70552–70588 | 20.19 Partition Graph | `architecture/search-space.md` | MOVED | v0.20 |
| `Continue Architecture Planning.md` | 70590–70645 | 20.20 SearchSpace | `architecture/search-space.md` | MOVED | v0.20 |
| `Continue Architecture Planning.md` | 70647–70694 | 20.21 Search-Space Controller | `architecture/search-space.md` | MOVED | v0.20 |
| `Continue Architecture Planning.md` | 70696–70724 | 20.22 Three-Level Control Plane | `architecture/search-space.md` | MOVED | v0.20 |
| `Continue Architecture Planning.md` | 70726–70766 | 20.23 Candidate Sources Remain Low-Level | `architecture/search-space.md` | MOVED | v0.20 |
| `Continue Architecture Planning.md` | 70768–70824 | 20.24 Termination Becomes More Sophisticated | `architecture/search-space.md` | MOVED | v0.20 |
| `Continue Architecture Planning.md` | 70826–70858 | 20.25 Saturation | `architecture/search-space.md` | MOVED | v0.20 |
| `Continue Architecture Planning.md` | 70860–70905 | 20.26 Partition Statistics | `architecture/search-space.md` | MOVED | v0.20 |
| `Continue Architecture Planning.md` | 70907–70942 | 20.27 Discovery Efficiency | `architecture/search-space.md` | MOVED | v0.20 |
| `Continue Architecture Planning.md` | 70944–70971 | 20.28 Failure Modes | `validation/failure-taxonomy.md` | MOVED | v0.20 |
| `Continue Architecture Planning.md` | 70973–70973 | 20.29 Core Invariants | `validation/invariants.md` | MOVED | v0.20 |
| `Continue Architecture Planning.md` | 70975–70981 | 20.29 Core Invariants › Search-space invariant | `validation/invariants.md` | MOVED | v0.20 |
| `Continue Architecture Planning.md` | 70983–70989 | 20.29 Core Invariants › Strategy invariant | `validation/invariants.md` | MOVED | v0.20 |
| `Continue Architecture Planning.md` | 70991–70997 | 20.29 Core Invariants › Acquisition invariant | `validation/invariants.md` | MOVED | v0.20 |
| `Continue Architecture Planning.md` | 70999–71005 | 20.29 Core Invariants › Partition invariant | `validation/invariants.md` | MOVED | v0.20 |
| `Continue Architecture Planning.md` | 71007–71013 | 20.29 Core Invariants › Coverage invariant | `validation/invariants.md` | MOVED | v0.20 |
| `Continue Architecture Planning.md` | 71015–71026 | 20.29 Core Invariants › Discovery invariant | `validation/invariants.md` | MOVED | v0.20 |
| `Continue Architecture Planning.md` | 71028–71072 | 20.30 The Architecture After v0.20 | `architecture/system-model.md` | MOVED | v0.20 |
| `Continue Architecture Planning.md` | 71074–71129 | 20.31 The DVB Analogy Is Now Structural | `research/dvb-blind-scan.md` | MOVED | v0.20 |
| `Continue Architecture Planning.md` | 71131–71200 | v0.21 — Discovery Strategy Learning / Adaptive Search | `architecture/strategy-and-planning.md` | MOVED | v0.21 |
| `Continue Architecture Planning.md` | 71206–71206 | *turn 54 you lead-in* | — (removed) | ARTIFACT | v0.21; conversation continuation marker |
| `Continue Architecture Planning.md` | 71212–71240 | v0.21 — Adaptive Discovery Strategy | `architecture/strategy-and-planning.md` | MOVED | v0.21 |
| `Continue Architecture Planning.md` | 71242–71291 | 21.1 The Adaptive Loop | `architecture/strategy-and-planning.md` | MOVED | v0.21 |
| `Continue Architecture Planning.md` | 71293–71345 | 21.2 Strategy Performance Record | `architecture/strategy-and-planning.md` | MOVED | v0.21 |
| `Continue Architecture Planning.md` | 71347–71385 | 21.3 Yield Metrics | `architecture/strategy-and-planning.md` | MOVED | v0.21 |
| `Continue Architecture Planning.md` | 71387–71432 | 21.4 Strategy Score | `architecture/strategy-and-planning.md` | MOVED | v0.21 |
| `Continue Architecture Planning.md` | 71434–71486 | 21.5 Cold Start Problem | `architecture/strategy-and-planning.md` | MOVED | v0.21 |
| `Continue Architecture Planning.md` | 71488–71521 | 21.6 Exploration Quota | `architecture/strategy-and-planning.md` | MOVED | v0.21 |
| `Continue Architecture Planning.md` | 71523–71570 | 21.7 Strategy Selection Must Be Constrained | `architecture/strategy-and-planning.md` | MOVED | v0.21 |
| `Continue Architecture Planning.md` | 71572–71610 | 21.8 Strategy Eligibility | `architecture/strategy-and-planning.md` | MOVED | v0.21 |
| `Continue Architecture Planning.md` | 71612–71664 | 21.9 Temporary vs Permanent Failure | `architecture/strategy-and-planning.md` | MOVED | v0.21 |
| `Continue Architecture Planning.md` | 71666–71711 | 21.10 Strategy Outcome | `architecture/strategy-and-planning.md` | MOVED | v0.21 |
| `Continue Architecture Planning.md` | 71713–71752 | 21.11 Strategy Outcome ≠ Strategy Truth | `architecture/strategy-and-planning.md` | MOVED | v0.21 |
| `Continue Architecture Planning.md` | 71754–71787 | 21.12 Novelty | `architecture/strategy-and-planning.md` | MOVED | v0.21 |
| `Continue Architecture Planning.md` | 71789–71826 | 21.13 Frontier Expansion Value | `architecture/strategy-and-planning.md` | MOVED | v0.21 |
| `Continue Architecture Planning.md` | 71828–71853 | 21.14 Frontier Expansion Metric | `architecture/strategy-and-planning.md` | MOVED | v0.21 |
| `Continue Architecture Planning.md` | 71855–71901 | 21.15 Strategy Memory | `architecture/strategy-and-planning.md` | MOVED | v0.21 |
| `Continue Architecture Planning.md` | 71903–71955 | 21.16 Hierarchical Priors | `architecture/strategy-and-planning.md` | MOVED | v0.21 |
| `Continue Architecture Planning.md` | 71957–71992 | 21.17 Discovery Strategy Ledger | `architecture/strategy-and-planning.md` | MOVED | v0.21 |
| `Continue Architecture Planning.md` | 71994–72028 | 21.18 Deterministic Replay | `architecture/strategy-and-planning.md` | MOVED | v0.21 |
| `Continue Architecture Planning.md` | 72030–72059 | 21.19 Random Exploration | `architecture/strategy-and-planning.md` | MOVED | v0.21 |
| `Continue Architecture Planning.md` | 72061–72108 | 21.20 Learning Must Not Modify Safety Boundaries | `architecture/strategy-and-planning.md` | MOVED | v0.21 |
| `Continue Architecture Planning.md` | 72110–72216 | 21.21 Adaptive Discovery Controller | `architecture/strategy-and-planning.md` | MOVED | v0.21 |
| `Continue Architecture Planning.md` | 72218–72249 | 21.22 Tie-Breaking Must Be Deterministic | `architecture/strategy-and-planning.md` | MOVED | v0.21 |
| `Continue Architecture Planning.md` | 72251–72277 | 21.23 Performance Decay | `architecture/strategy-and-planning.md` | MOVED | v0.21 |
| `Continue Architecture Planning.md` | 72279–72325 | 21.24 Strategy Adaptation and Scan Sessions | `architecture/strategy-and-planning.md` | MOVED | v0.21 |
| `Continue Architecture Planning.md` | 72327–72362 | 21.25 Search Strategy as a First-Class Graph Node | `architecture/strategy-and-planning.md` | MOVED | v0.21 |
| `Continue Architecture Planning.md` | 72364–72400 | 21.26 Search Decision Graph | `architecture/strategy-and-planning.md` | MOVED | v0.21 |
| `Continue Architecture Planning.md` | 72402–72428 | 21.27 Two Kinds of Provenance | `architecture/strategy-and-planning.md` | MOVED | v0.21 |
| `Continue Architecture Planning.md` | 72430–72450 | 21.28 Failure Taxonomy | `validation/failure-taxonomy.md` | MOVED | v0.21 |
| `Continue Architecture Planning.md` | 72452–72452 | 21.29 Invariants | `validation/invariants.md` | MOVED | v0.21 |
| `Continue Architecture Planning.md` | 72454–72460 | 21.29 Invariants › Safety invariant | `validation/invariants.md` | MOVED | v0.21 |
| `Continue Architecture Planning.md` | 72462–72468 | 21.29 Invariants › Capability invariant | `validation/invariants.md` | MOVED | v0.21 |
| `Continue Architecture Planning.md` | 72470–72476 | 21.29 Invariants › Domain invariant | `validation/invariants.md` | MOVED | v0.21 |
| `Continue Architecture Planning.md` | 72478–72484 | 21.29 Invariants › Exploration invariant | `validation/invariants.md` | MOVED | v0.21 |
| `Continue Architecture Planning.md` | 72486–72492 | 21.29 Invariants › Historical invariant | `validation/invariants.md` | MOVED | v0.21 |
| `Continue Architecture Planning.md` | 72494–72502 | 21.29 Invariants › Replay invariant | `validation/invariants.md` | MOVED | v0.21 |
| `Continue Architecture Planning.md` | 72504–72511 | 21.29 Invariants › Provenance invariant | `validation/invariants.md` | MOVED | v0.21 |
| `Continue Architecture Planning.md` | 72513–72578 | 21.30 Architecture After v0.21 | `architecture/system-model.md` | MOVED | v0.21 |
| `Continue Architecture Planning.md` | 72580–72636 | 21.31 The Important Conceptual Shift | `concepts/overview.md` | MOVED | v0.21 |
| `Continue Architecture Planning.md` | 72638–72695 | v0.22 — Discovery Completeness + Coverage Claims | `architecture/coverage-and-absence.md` | MOVED | v0.22 |
| `Continue Architecture Planning.md` | 72701–72701 | *turn 56 you lead-in* | — (removed) | ARTIFACT | v0.22; conversation continuation marker |
| `Continue Architecture Planning.md` | 72707–72717 | v0.22 — Discovery Completeness + Coverage Claims | `architecture/coverage-and-absence.md` | MOVED | v0.22 |
| `Continue Architecture Planning.md` | 72719–72763 | v0.22 — Discovery Completeness + Coverage Claims › 22.1 The problem | `architecture/coverage-and-absence.md` | MOVED | v0.22 |
| `Continue Architecture Planning.md` | 72765–72815 | 22.2 Search-space state model | `architecture/coverage-and-absence.md` | MOVED | v0.22 |
| `Continue Architecture Planning.md` | 72817–72852 | 22.3 Coverage is a measurement | `architecture/coverage-and-absence.md` | MOVED | v0.22 |
| `Continue Architecture Planning.md` | 72854–72906 | 22.4 Coverage dimensions | `architecture/coverage-and-absence.md` | MOVED | v0.22 |
| `Continue Architecture Planning.md` | 72908–72980 | 22.5 CoverageRecord | `architecture/coverage-and-absence.md` | MOVED | v0.22 |
| `Continue Architecture Planning.md` | 72982–73020 | 22.6 Coverage state | `architecture/coverage-and-absence.md` | MOVED | v0.22 |
| `Continue Architecture Planning.md` | 73022–73075 | 22.7 CoverageClaim | `architecture/coverage-and-absence.md` | MOVED | v0.22 |
| `Continue Architecture Planning.md` | 73077–73131 | 22.8 Completeness is a stronger assertion | `architecture/coverage-and-absence.md` | MOVED | v0.22 |
| `Continue Architecture Planning.md` | 73133–73193 | 22.9 The finite-enumerator case | `architecture/coverage-and-absence.md` | MOVED | v0.22 |
| `Continue Architecture Planning.md` | 73195–73249 | 22.10 Enumeration contract | `architecture/coverage-and-absence.md` | MOVED | v0.22 |
| `Continue Architecture Planning.md` | 73251–73323 | 22.11 Negative evidence | `architecture/coverage-and-absence.md` | MOVED | v0.22 |
| `Continue Architecture Planning.md` | 73325–73365 | 22.12 Absence reasoning hierarchy | `architecture/coverage-and-absence.md` | MOVED | v0.22 |
| `Continue Architecture Planning.md` | 73367–73401 | 22.13 “Not found” becomes a first-class result | `architecture/coverage-and-absence.md` | MOVED | v0.22 |
| `Continue Architecture Planning.md` | 73403–73459 | 22.14 Coverage cannot necessarily be monotonically interpreted | `architecture/coverage-and-absence.md` | MOVED | v0.22 |
| `Continue Architecture Planning.md` | 73461–73507 | 22.15 Version the search universe | `architecture/coverage-and-absence.md` | MOVED | v0.22 |
| `Continue Architecture Planning.md` | 73509–73550 | 22.16 Coverage ledger | `architecture/coverage-and-absence.md` | MOVED | v0.22 |
| `Continue Architecture Planning.md` | 73552–73607 | 22.17 Three graphs now interact | `architecture/coverage-and-absence.md` | MOVED | v0.22 |
| `Continue Architecture Planning.md` | 73609–73663 | 22.18 Completeness assessment | `architecture/coverage-and-absence.md` | MOVED | v0.22 |
| `Continue Architecture Planning.md` | 73665–73697 | 22.19 Assurance levels | `validation/verification.md` | MOVED | v0.22 |
| `Continue Architecture Planning.md` | 73699–73713 | 22.20 Search completeness matrix | `architecture/coverage-and-absence.md` | MOVED | v0.22 |
| `Continue Architecture Planning.md` | 73715–73761 | 22.21 Coverage calculation | `architecture/coverage-and-absence.md` | MOVED | v0.22 |
| `Continue Architecture Planning.md` | 73763–73807 | 22.22 Coverage should be query-relative | `architecture/coverage-and-absence.md` | MOVED | v0.22 |
| `Continue Architecture Planning.md` | 73809–73854 | 22.23 Failure taxonomy | `validation/failure-taxonomy.md` | MOVED | v0.22 |
| `Continue Architecture Planning.md` | 73856–73856 | 22.24 Core invariants | `validation/invariants.md` | MOVED | v0.22 |
| `Continue Architecture Planning.md` | 73858–73862 | 22.24 Core invariants › Invariant 1 | `validation/invariants.md` | MOVED | v0.22 |
| `Continue Architecture Planning.md` | 73864–73868 | 22.24 Core invariants › Invariant 2 | `validation/invariants.md` | MOVED | v0.22 |
| `Continue Architecture Planning.md` | 73870–73874 | 22.24 Core invariants › Invariant 3 | `validation/invariants.md` | MOVED | v0.22 |
| `Continue Architecture Planning.md` | 73876–73880 | 22.24 Core invariants › Invariant 4 | `validation/invariants.md` | MOVED | v0.22 |
| `Continue Architecture Planning.md` | 73882–73886 | 22.24 Core invariants › Invariant 5 | `validation/invariants.md` | MOVED | v0.22 |
| `Continue Architecture Planning.md` | 73888–73892 | 22.24 Core invariants › Invariant 6 | `validation/invariants.md` | MOVED | v0.22 |
| `Continue Architecture Planning.md` | 73894–73898 | 22.24 Core invariants › Invariant 7 | `validation/invariants.md` | MOVED | v0.22 |
| `Continue Architecture Planning.md` | 73900–73904 | 22.24 Core invariants › Invariant 8 | `validation/invariants.md` | MOVED | v0.22 |
| `Continue Architecture Planning.md` | 73906–73910 | 22.24 Core invariants › Invariant 9 | `validation/invariants.md` | MOVED | v0.22 |
| `Continue Architecture Planning.md` | 73912–73935 | 22.24 Core invariants › Invariant 10 | `validation/invariants.md` | MOVED | v0.22 |
| `Continue Architecture Planning.md` | 73937–73996 | 22.25 v0.22 architecture | `architecture/system-model.md` | MOVED | v0.22 |
| `Continue Architecture Planning.md` | 73998–74027 | 22.26 The conceptual jump | `concepts/overview.md` | MOVED | v0.22 |
| `Continue Architecture Planning.md` | 74029–74056 | v0.23 — Negative Evidence + Absence Reasoning | `architecture/coverage-and-absence.md` | MOVED | v0.23 |
| `Continue Architecture Planning.md` | 74062–74062 | *turn 58 you lead-in* | — (removed) | ARTIFACT | v0.23; conversation continuation marker |
| `Continue Architecture Planning.md` | 74068–74090 | v0.23 — Negative Evidence + Absence Reasoning | `architecture/coverage-and-absence.md` | MOVED | v0.23 |
| `Continue Architecture Planning.md` | 74092–74142 | v0.23 — Negative Evidence + Absence Reasoning › 23.1 The absence problem | `architecture/coverage-and-absence.md` | MOVED | v0.23 |
| `Continue Architecture Planning.md` | 74144–74182 | 23.2 Four fundamental states | `architecture/coverage-and-absence.md` | MOVED | v0.23 |
| `Continue Architecture Planning.md` | 74184–74253 | 23.3 PresenceAssertion | `architecture/coverage-and-absence.md` | MOVED | v0.23 |
| `Continue Architecture Planning.md` | 74255–74296 | 23.4 Absence is always scoped | `architecture/coverage-and-absence.md` | MOVED | v0.23 |
| `Continue Architecture Planning.md` | 74298–74346 | 23.5 NegativeEvidence | `architecture/coverage-and-absence.md` | MOVED | v0.23 |
| `Continue Architecture Planning.md` | 74348–74393 | 23.6 Absence strength | `architecture/coverage-and-absence.md` | MOVED | v0.23 |
| `Continue Architecture Planning.md` | 74395–74447 | 23.7 Search failure must not become negative evidence automatically | `architecture/coverage-and-absence.md` | MOVED | v0.23 |
| `Continue Architecture Planning.md` | 74449–74481 | 23.8 Failure → evidence mapping | `validation/failure-taxonomy.md` | MOVED | v0.23 |
| `Continue Architecture Planning.md` | 74483–74531 | 23.9 Exact locator absence | `architecture/coverage-and-absence.md` | MOVED | v0.23 |
| `Continue Architecture Planning.md` | 74533–74571 | 23.10 Claims need predicates | `architecture/coverage-and-absence.md` | MOVED | v0.23 |
| `Continue Architecture Planning.md` | 74573–74629 | 23.11 Predicate-aware absence | `architecture/coverage-and-absence.md` | MOVED | v0.23 |
| `Continue Architecture Planning.md` | 74631–74679 | 23.12 Contradiction becomes first-class | `architecture/coverage-and-absence.md` | MOVED | v0.23 |
| `Continue Architecture Planning.md` | 74681–74724 | 23.13 True contradiction | `architecture/coverage-and-absence.md` | MOVED | v0.23 |
| `Continue Architecture Planning.md` | 74726–74767 | 23.14 Absence confidence cannot simply be numeric | `architecture/coverage-and-absence.md` | MOVED | v0.23 |
| `Continue Architecture Planning.md` | 74769–74817 | 23.15 Independent evidence | `architecture/coverage-and-absence.md` | MOVED | v0.23 |
| `Continue Architecture Planning.md` | 74819–74864 | 23.16 Absence reasoning engine | `architecture/coverage-and-absence.md` | MOVED | v0.23 |
| `Continue Architecture Planning.md` | 74866–74913 | 23.17 Formal absence rule | `architecture/coverage-and-absence.md` | MOVED | v0.23 |
| `Continue Architecture Planning.md` | 74915–74961 | 23.18 Dynamic universes | `architecture/coverage-and-absence.md` | MOVED | v0.23 |
| `Continue Architecture Planning.md` | 74963–74995 | 23.19 Temporal validity | `architecture/coverage-and-absence.md` | MOVED | v0.23 |
| `Continue Architecture Planning.md` | 74997–75044 | 23.20 Absence and revision detection | `architecture/coverage-and-absence.md` | MOVED | v0.23 |
| `Continue Architecture Planning.md` | 75046–75099 | 23.21 Search state now becomes richer | `architecture/coverage-and-absence.md` | MOVED | v0.23 |
| `Continue Architecture Planning.md` | 75101–75167 | 23.22 Architecture after v0.23 | `architecture/system-model.md` | MOVED | v0.23 |
| `Continue Architecture Planning.md` | 75169–75171 | 23.23 The three epistemic outcomes | `architecture/coverage-and-absence.md` | MOVED | v0.23 |
| `Continue Architecture Planning.md` | 75173–75183 | 23.23 The three epistemic outcomes › Presence | `architecture/coverage-and-absence.md` | MOVED | v0.23 |
| `Continue Architecture Planning.md` | 75185–75199 | 23.23 The three epistemic outcomes › Absence | `architecture/coverage-and-absence.md` | MOVED | v0.23 |
| `Continue Architecture Planning.md` | 75201–75223 | 23.23 The three epistemic outcomes › Unknown | `architecture/coverage-and-absence.md` | MOVED | v0.23 |
| `Continue Architecture Planning.md` | 75225–75225 | 23.24 New invariants | `validation/invariants.md` | MOVED | v0.23 |
| `Continue Architecture Planning.md` | 75227–75231 | 23.24 New invariants › Invariant 1 | `validation/invariants.md` | MOVED | v0.23 |
| `Continue Architecture Planning.md` | 75233–75237 | 23.24 New invariants › Invariant 2 | `validation/invariants.md` | MOVED | v0.23 |
| `Continue Architecture Planning.md` | 75239–75243 | 23.24 New invariants › Invariant 3 | `validation/invariants.md` | MOVED | v0.23 |
| `Continue Architecture Planning.md` | 75245–75249 | 23.24 New invariants › Invariant 4 | `validation/invariants.md` | MOVED | v0.23 |
| `Continue Architecture Planning.md` | 75251–75255 | 23.24 New invariants › Invariant 5 | `validation/invariants.md` | MOVED | v0.23 |
| `Continue Architecture Planning.md` | 75257–75261 | 23.24 New invariants › Invariant 6 | `validation/invariants.md` | MOVED | v0.23 |
| `Continue Architecture Planning.md` | 75263–75267 | 23.24 New invariants › Invariant 7 | `validation/invariants.md` | MOVED | v0.23 |
| `Continue Architecture Planning.md` | 75269–75273 | 23.24 New invariants › Invariant 8 | `validation/invariants.md` | MOVED | v0.23 |
| `Continue Architecture Planning.md` | 75275–75279 | 23.24 New invariants › Invariant 9 | `validation/invariants.md` | MOVED | v0.23 |
| `Continue Architecture Planning.md` | 75281–75287 | 23.24 New invariants › Invariant 10 | `validation/invariants.md` | MOVED | v0.23 |
| `Continue Architecture Planning.md` | 75289–75323 | 23.25 v0.23 conceptual result | `concepts/overview.md` | MOVED | v0.23 |
| `Continue Architecture Planning.md` | 75325–75390 | v0.24 — Query/Goal-Constrained Discovery | `architecture/goal-and-query.md` | MOVED | v0.24 |
| `Continue Architecture Planning.md` | 75396–75396 | *turn 60 you lead-in* | — (removed) | ARTIFACT | v0.24; conversation continuation marker |
| `Continue Architecture Planning.md` | 75402–75455 | v0.24 — Query/Goal-Constrained Discovery | `architecture/goal-and-query.md` | MOVED | v0.24 |
| `Continue Architecture Planning.md` | 75457–75517 | 24.1 SearchGoal | `architecture/goal-and-query.md` | MOVED | v0.24 |
| `Continue Architecture Planning.md` | 75519–75568 | 24.2 Goal ≠ Domain | `architecture/goal-and-query.md` | MOVED | v0.24 |
| `Continue Architecture Planning.md` | 75570–75622 | 24.3 Goal constraints | `architecture/goal-and-query.md` | MOVED | v0.24 |
| `Continue Architecture Planning.md` | 75624–75662 | 24.4 Hard constraints vs soft preferences | `architecture/goal-and-query.md` | MOVED | v0.24 |
| `Continue Architecture Planning.md` | 75664–75710 | 24.5 GoalConstraint | `architecture/goal-and-query.md` | MOVED | v0.24 |
| `Continue Architecture Planning.md` | 75712–75752 | 24.6 Relevance is not classification | `architecture/goal-and-query.md` | MOVED | v0.24 |
| `Continue Architecture Planning.md` | 75754–75812 | 24.7 RelevanceAssertion | `architecture/goal-and-query.md` | MOVED | v0.24 |
| `Continue Architecture Planning.md` | 75814–75860 | 24.8 Why `UNKNOWN` matters | `architecture/goal-and-query.md` | MOVED | v0.24 |
| `Continue Architecture Planning.md` | 75862–75908 | 24.9 Relevance scoring | `architecture/goal-and-query.md` | MOVED | v0.24 |
| `Continue Architecture Planning.md` | 75910–75925 | 24.10 The six questions | `architecture/goal-and-query.md` | MOVED | v0.24 |
| `Continue Architecture Planning.md` | 75927–75978 | 24.11 Relevant Search Space | `architecture/goal-and-query.md` | MOVED | v0.24 |
| `Continue Architecture Planning.md` | 75980–76037 | 24.12 Example | `architecture/goal-and-query.md` | MOVED | v0.24 |
| `Continue Architecture Planning.md` | 76039–76091 | 24.13 Goal-directed adaptive discovery | `architecture/goal-and-query.md` | MOVED | v0.24 |
| `Continue Architecture Planning.md` | 76093–76140 | 24.14 Expected Goal Value | `architecture/goal-and-query.md` | MOVED | v0.24 |
| `Continue Architecture Planning.md` | 76142–76172 | 24.15 Information gain | `architecture/goal-and-query.md` | MOVED | v0.24 |
| `Continue Architecture Planning.md` | 76174–76215 | 24.16 Goal-aware partition scoring | `architecture/goal-and-query.md` | MOVED | v0.24 |
| `Continue Architecture Planning.md` | 76217–76267 | 24.17 Goal does not grant authority | `architecture/goal-and-query.md` | MOVED | v0.24 |
| `Continue Architecture Planning.md` | 76269–76307 | 24.18 Goal provenance | `architecture/goal-and-query.md` | MOVED | v0.24 |
| `Continue Architecture Planning.md` | 76309–76352 | 24.19 Goal-aware discovery event | `architecture/goal-and-query.md` | MOVED | v0.24 |
| `Continue Architecture Planning.md` | 76354–76400 | 24.20 Goal lifecycle | `architecture/goal-and-query.md` | MOVED | v0.24 |
| `Continue Architecture Planning.md` | 76402–76443 | 24.21 Goal termination policies | `architecture/goal-and-query.md` | MOVED | v0.24 |
| `Continue Architecture Planning.md` | 76445–76481 | 24.22 Goal satisfaction vs completeness | `architecture/goal-and-query.md` | MOVED | v0.24 |
| `Continue Architecture Planning.md` | 76483–76529 | 24.23 GoalResult | `architecture/goal-and-query.md` | MOVED | v0.24 |
| `Continue Architecture Planning.md` | 76531–76577 | 24.24 Result ranking | `architecture/goal-and-query.md` | MOVED | v0.24 |
| `Continue Architecture Planning.md` | 76579–76602 | 24.25 Result quality model | `architecture/goal-and-query.md` | MOVED | v0.24 |
| `Continue Architecture Planning.md` | 76604–76641 | 24.26 Goal conflict | `architecture/goal-and-query.md` | MOVED | v0.24 |
| `Continue Architecture Planning.md` | 76643–76679 | 24.27 Goal sessions | `architecture/goal-and-query.md` | MOVED | v0.24 |
| `Continue Architecture Planning.md` | 76681–76720 | 24.28 Reuse of previous knowledge | `architecture/goal-and-query.md` | MOVED | v0.24 |
| `Continue Architecture Planning.md` | 76722–76761 | 24.29 Knowledge reuse is not evidence reuse without qualification | `architecture/goal-and-query.md` | MOVED | v0.24 |
| `Continue Architecture Planning.md` | 76763–76828 | 24.30 New architecture | `architecture/system-model.md` | MOVED | v0.24 |
| `Continue Architecture Planning.md` | 76830–76874 | 24.31 The architecture's semantic layers | `architecture/system-model.md` | MOVED | v0.24 |
| `Continue Architecture Planning.md` | 76876–76876 | 24.32 Core invariants for v0.24 | `validation/invariants.md` | MOVED | v0.24 |
| `Continue Architecture Planning.md` | 76878–76884 | 24.32 Core invariants for v0.24 › Invariant 1 | `validation/invariants.md` | MOVED | v0.24 |
| `Continue Architecture Planning.md` | 76886–76892 | 24.32 Core invariants for v0.24 › Invariant 2 | `validation/invariants.md` | MOVED | v0.24 |
| `Continue Architecture Planning.md` | 76894–76900 | 24.32 Core invariants for v0.24 › Invariant 3 | `validation/invariants.md` | MOVED | v0.24 |
| `Continue Architecture Planning.md` | 76902–76908 | 24.32 Core invariants for v0.24 › Invariant 4 | `validation/invariants.md` | MOVED | v0.24 |
| `Continue Architecture Planning.md` | 76910–76916 | 24.32 Core invariants for v0.24 › Invariant 5 | `validation/invariants.md` | MOVED | v0.24 |
| `Continue Architecture Planning.md` | 76918–76924 | 24.32 Core invariants for v0.24 › Invariant 6 | `validation/invariants.md` | MOVED | v0.24 |
| `Continue Architecture Planning.md` | 76926–76932 | 24.32 Core invariants for v0.24 › Invariant 7 | `validation/invariants.md` | MOVED | v0.24 |
| `Continue Architecture Planning.md` | 76934–76947 | 24.32 Core invariants for v0.24 › Invariant 8 | `validation/invariants.md` | MOVED | v0.24 |
| `Continue Architecture Planning.md` | 76949–76964 | 24.32 Core invariants for v0.24 › Invariant 9 | `validation/invariants.md` | MOVED | v0.24 |
| `Continue Architecture Planning.md` | 76966–76975 | 24.32 Core invariants for v0.24 › Invariant 10 | `validation/invariants.md` | MOVED | v0.24 |
| `Continue Architecture Planning.md` | 76977–77032 | 24.33 What v0.24 changes fundamentally | `architecture/goal-and-query.md` | MOVED | v0.24 |
| `Continue Architecture Planning.md` | 77034–77096 | v0.25 — Discovery Query Planner | `architecture/goal-and-query.md` | MOVED | v0.25 |
| `Continue Architecture Planning.md` | 77102–77102 | *turn 62 you lead-in* | — (removed) | ARTIFACT | v0.25; conversation continuation marker |
| `Continue Architecture Planning.md` | 77108–77158 | v0.25 — Discovery Query Planner | `architecture/goal-and-query.md` | MOVED | v0.25 |
| `Continue Architecture Planning.md` | 77160–77200 | v0.25 — Discovery Query Planner › 25.1 Planner ≠ Search Engine | `architecture/goal-and-query.md` | MOVED | v0.25 |
| `Continue Architecture Planning.md` | 77202–77261 | 25.2 QueryPlan | `architecture/goal-and-query.md` | MOVED | v0.25 |
| `Continue Architecture Planning.md` | 77263–77321 | 25.3 QueryStep | `architecture/goal-and-query.md` | MOVED | v0.25 |
| `Continue Architecture Planning.md` | 77323–77363 | 25.4 Query decomposition | `architecture/goal-and-query.md` | MOVED | v0.25 |
| `Continue Architecture Planning.md` | 77365–77401 | 25.5 Search axes | `architecture/goal-and-query.md` | MOVED | v0.25 |
| `Continue Architecture Planning.md` | 77403–77440 | 25.6 QueryTactic | `architecture/goal-and-query.md` | MOVED | v0.25 |
| `Continue Architecture Planning.md` | 77442–77479 | 25.7 Tactic ≠ Strategy | `architecture/goal-and-query.md` | MOVED | v0.25 |
| `Continue Architecture Planning.md` | 77481–77517 | 25.8 Planner plugins | `architecture/goal-and-query.md` | MOVED | v0.25 |
| `Continue Architecture Planning.md` | 77519–77555 | 25.9 Planner contract | `architecture/goal-and-query.md` | MOVED | v0.25 |
| `Continue Architecture Planning.md` | 77557–77592 | 25.10 Query plan example | `architecture/goal-and-query.md` | MOVED | v0.25 |
| `Continue Architecture Planning.md` | 77594–77626 | 25.11 Dependencies | `architecture/goal-and-query.md` | MOVED | v0.25 |
| `Continue Architecture Planning.md` | 77628–77669 | 25.12 Conditional planning | `architecture/goal-and-query.md` | MOVED | v0.25 |
| `Continue Architecture Planning.md` | 77671–77701 | 25.13 Planning boundary | `architecture/goal-and-query.md` | MOVED | v0.25 |
| `Continue Architecture Planning.md` | 77703–77735 | 25.14 Query plan validation | `architecture/goal-and-query.md` | MOVED | v0.25 |
| `Continue Architecture Planning.md` | 77737–77765 | 25.15 Planner and adaptive discovery | `architecture/goal-and-query.md` | MOVED | v0.25 |
| `Continue Architecture Planning.md` | 77767–77801 | 25.16 Exploration vs exploitation moves upward | `architecture/goal-and-query.md` | MOVED | v0.25 |
| `Continue Architecture Planning.md` | 77803–77831 | 25.17 Query tactic performance | `architecture/goal-and-query.md` | MOVED | v0.25 |
| `Continue Architecture Planning.md` | 77833–77877 | 25.18 Query planner provenance | `architecture/goal-and-query.md` | MOVED | v0.25 |
| `Continue Architecture Planning.md` | 77879–77907 | 25.19 Query plan identity | `architecture/goal-and-query.md` | MOVED | v0.25 |
| `Continue Architecture Planning.md` | 77909–77940 | 25.20 Plan versioning | `architecture/goal-and-query.md` | MOVED | v0.25 |
| `Continue Architecture Planning.md` | 77942–77973 | 25.21 Planner cannot erase old work | `architecture/goal-and-query.md` | MOVED | v0.25 |
| `Continue Architecture Planning.md` | 77975–78028 | 25.22 Query expansion | `architecture/goal-and-query.md` | MOVED | v0.25 |
| `Continue Architecture Planning.md` | 78030–78052 | 25.23 Expansion evidence | `architecture/goal-and-query.md` | MOVED | v0.25 |
| `Continue Architecture Planning.md` | 78054–78084 | 25.24 Planner hallucination boundary | `architecture/goal-and-query.md` | MOVED | v0.25 |
| `Continue Architecture Planning.md` | 78086–78150 | 25.25 Search hypothesis | `architecture/goal-and-query.md` | MOVED | v0.25 |
| `Continue Architecture Planning.md` | 78152–78200 | 25.26 Query planner and DVB analogy | `research/dvb-blind-scan.md` | MOVED | v0.25 |
| `Continue Architecture Planning.md` | 78202–78227 | 25.27 Planner output is not execution | `architecture/goal-and-query.md` | MOVED | v0.25 |
| `Continue Architecture Planning.md` | 78229–78269 | 25.28 Planner budget | `architecture/goal-and-query.md` | MOVED | v0.25 |
| `Continue Architecture Planning.md` | 78271–78300 | 25.29 Three different budgets | `architecture/goal-and-query.md` | MOVED | v0.25 |
| `Continue Architecture Planning.md` | 78302–78348 | 25.30 Termination propagation | `architecture/goal-and-query.md` | MOVED | v0.25 |
| `Continue Architecture Planning.md` | 78350–78413 | 25.31 v0.25 complete architecture | `architecture/system-model.md` | MOVED | v0.25 |
| `Continue Architecture Planning.md` | 78415–78415 | 25.32 v0.25 invariants | `validation/invariants.md` | MOVED | v0.25 |
| `Continue Architecture Planning.md` | 78417–78461 | 25.32 v0.25 invariants › Planner invariants | `validation/invariants.md` | MOVED | v0.25 |
| `Continue Architecture Planning.md` | 78463–78546 | 25.33 The resulting abstraction stack | `architecture/goal-and-query.md` | MOVED | v0.25 |
| `Continue Architecture Planning.md` | 78548–78586 | v0.26 — Search Tactic Runtime | `architecture/strategy-and-planning.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 78592–78592 | *turn 64 you lead-in* | — (removed) | ARTIFACT | v0.26; conversation continuation marker |
| `Continue Architecture Planning.md` | 78598–78628 | v0.26 — Search Tactic Runtime | `architecture/strategy-and-planning.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 78630–78673 | v0.26 — Search Tactic Runtime › 26.1 The architectural gap | `architecture/strategy-and-planning.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 78675–78713 | 26.2 QueryStep ≠ TacticExecution | `architecture/strategy-and-planning.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 78715–78766 | 26.3 TacticExecution | `architecture/strategy-and-planning.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 78768–78810 | 26.4 TacticRuntime | `architecture/strategy-and-planning.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 78812–78861 | 26.5 TacticRuntime responsibilities | `architecture/strategy-and-planning.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 78863–78920 | 26.6 Tactic contract | `architecture/strategy-and-planning.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 78922–78962 | 26.7 Capability surface | `architecture/strategy-and-planning.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 78964–79006 | 26.8 Bounded execution | `architecture/strategy-and-planning.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 79008–79074 | 26.9 Batch execution | `architecture/strategy-and-planning.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 79076–79123 | 26.10 Cursor | `architecture/strategy-and-planning.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 79125–79165 | 26.11 Checkpoint | `architecture/strategy-and-planning.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 79167–79219 | 26.12 Checkpoint atomicity | `architecture/strategy-and-planning.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 79221–79272 | 26.13 Tactic dependencies | `architecture/strategy-and-planning.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 79274–79315 | 26.14 Tactic lifecycle | `architecture/strategy-and-planning.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 79317–79372 | 26.15 Exhaustion vs completion | `architecture/strategy-and-planning.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 79374–79424 | 26.16 Tactic result | `architecture/strategy-and-planning.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 79426–79465 | 26.17 Tactic does not create candidates directly | `architecture/strategy-and-planning.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 79467–79521 | 26.18 Tactic → Strategy relationship | `architecture/strategy-and-planning.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 79523–79580 | 26.19 Tactic provenance | `architecture/strategy-and-planning.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 79582–79584 | 26.20 Failure taxonomy | `validation/failure-taxonomy.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 79586–79593 | 26.20 Failure taxonomy › Planning failures | `architecture/strategy-and-planning.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 79595–79605 | 26.20 Failure taxonomy › Runtime failures | `architecture/strategy-and-planning.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 79607–79614 | 26.20 Failure taxonomy › Strategy failures | `architecture/strategy-and-planning.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 79616–79624 | 26.20 Failure taxonomy › Search failures | `architecture/strategy-and-planning.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 79626–79649 | 26.20 Failure taxonomy › Recovery failures | `architecture/strategy-and-planning.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 79651–79700 | 26.21 Retry semantics | `architecture/strategy-and-planning.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 79702–79735 | 26.22 Cancellation | `architecture/strategy-and-planning.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 79737–79782 | 26.23 Shared Frontier interaction | `architecture/strategy-and-planning.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 79784–79852 | 26.24 v0.26 architecture | `architecture/system-model.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 79854–79892 | 26.25 Accounting | `architecture/strategy-and-planning.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 79894–79940 | 26.26 The important safety invariant | `validation/invariants.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 79942–79964 | 26.27 Resumability invariant | `validation/invariants.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 79966–80013 | 26.28 New state model | `architecture/strategy-and-planning.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 80015–80015 | 26.29 v0.26 invariants | `validation/invariants.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 80017–80021 | 26.29 v0.26 invariants › I1 — Planning/execution separation | `validation/invariants.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 80023–80027 | 26.29 v0.26 invariants › I2 — Execution identity | `validation/invariants.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 80029–80033 | 26.29 v0.26 invariants › I3 — Single scheduler authority | `validation/invariants.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 80035–80037 | 26.29 v0.26 invariants › I4 — Bounded execution | `validation/invariants.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 80039–80041 | 26.29 v0.26 invariants › I5 — Resumability | `validation/invariants.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 80043–80045 | 26.29 v0.26 invariants › I6 — No silent cursor advancement | `validation/invariants.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 80047–80057 | 26.29 v0.26 invariants › I7 — Proposal boundary | `validation/invariants.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 80059–80065 | 26.29 v0.26 invariants › I8 — No authority escalation | `validation/invariants.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 80067–80075 | 26.29 v0.26 invariants › I9 — Exhaustion separation | `validation/invariants.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 80077–80083 | 26.29 v0.26 invariants › I10 — Failure ≠ absence | `validation/invariants.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 80085–80100 | 26.29 v0.26 invariants › I11 — Provenance | `validation/invariants.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 80102–80106 | 26.29 v0.26 invariants › I12 — Versioned recovery | `validation/invariants.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 80108–80160 | 26.30 What v0.26 actually gives us | `concepts/overview.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 80162–80198 | 26.30 What v0.26 actually gives us › Next boundary: v0.27 | `roadmap/future-work.md` | MOVED | v0.26 |
| `Continue Architecture Planning.md` | 80204–80204 | *turn 66 you lead-in* | — (removed) | ARTIFACT | v0.26; conversation continuation marker |
| `Continue Architecture Planning.md` | 80210–80255 | v0.27 — Enumeration Runtime | `architecture/strategy-and-planning.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 80257–80301 | 27.1 The central distinction | `architecture/strategy-and-planning.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 80303–80333 | 27.2 Enumeration as a contract | `architecture/strategy-and-planning.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 80335–80377 | 27.3 Enumerator interface | `architecture/strategy-and-planning.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 80379–80423 | 27.4 EnumerationPage | `architecture/strategy-and-planning.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 80425–80475 | 27.5 `hasMore` is not always trustworthy | `architecture/strategy-and-planning.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 80477–80515 | 27.6 Enumeration state machine | `architecture/strategy-and-planning.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 80517–80563 | 27.7 EnumerationRuntime | `architecture/strategy-and-planning.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 80565–80594 | 27.8 Why this should not be inside DiscoveryStrategy | `architecture/strategy-and-planning.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 80596–80596 | 27.9 Enumerator examples | `architecture/strategy-and-planning.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 80598–80606 | 27.9 Enumerator examples › Sitemap | `architecture/strategy-and-planning.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 80608–80618 | 27.9 Enumerator examples › API | `architecture/strategy-and-planning.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 80620–80630 | 27.9 Enumerator examples › Repository | `architecture/strategy-and-planning.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 80632–80644 | 27.9 Enumerator examples › Manifest | `architecture/strategy-and-planning.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 80646–80688 | 27.10 EnumerationEntry | `architecture/strategy-and-planning.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 80690–80728 | 27.11 Entry identity | `architecture/strategy-and-planning.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 80730–80732 | 27.12 Enumeration cursor | `architecture/strategy-and-planning.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 80734–80741 | 27.12 Enumeration cursor › Offset | `architecture/strategy-and-planning.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 80743–80750 | 27.12 Enumeration cursor › Page | `architecture/strategy-and-planning.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 80752–80759 | 27.12 Enumeration cursor › Token | `architecture/strategy-and-planning.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 80761–80768 | 27.12 Enumeration cursor › Locator | `architecture/strategy-and-planning.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 80770–80786 | 27.12 Enumeration cursor › Composite | `architecture/strategy-and-planning.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 80788–80835 | 27.13 Cursor validity | `architecture/strategy-and-planning.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 80837–80868 | 27.14 Enumeration snapshot | `architecture/strategy-and-planning.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 80870–80895 | 27.15 Why snapshot identity matters | `architecture/strategy-and-planning.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 80897–80932 | 27.16 Cardinality | `architecture/strategy-and-planning.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 80934–80974 | 27.17 Ordering semantics | `architecture/strategy-and-planning.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 80976–81012 | 27.18 Enumeration consistency | `architecture/strategy-and-planning.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 81014–81053 | 27.19 Completeness assessment | `architecture/strategy-and-planning.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 81055–81088 | 27.20 The crucial three-level distinction | `architecture/strategy-and-planning.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 81090–81135 | 27.21 Example: sitemap | `architecture/strategy-and-planning.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 81137–81179 | 27.22 Enumeration → Coverage | `architecture/strategy-and-planning.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 81181–81237 | 27.23 Enumeration and negative evidence | `architecture/strategy-and-planning.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 81239–81278 | 27.24 Enumeration budget | `architecture/strategy-and-planning.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 81280–81314 | 27.25 Enumeration termination states | `architecture/strategy-and-planning.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 81316–81348 | 27.26 Enumeration accounting | `architecture/strategy-and-planning.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 81350–81397 | 27.27 Enumeration provenance | `architecture/strategy-and-planning.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 81399–81425 | 27.28 Enumeration replay | `architecture/strategy-and-planning.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 81427–81495 | 27.29 Full v0.27 architecture | `architecture/system-model.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 81497–81497 | 27.30 New invariants | `validation/invariants.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 81499–81501 | 27.30 New invariants › E1 — Enumeration is scoped | `validation/invariants.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 81503–81509 | 27.30 New invariants › E2 — Enumeration termination is not global completeness | `validation/invariants.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 81511–81517 | 27.30 New invariants › E3 — Budget exhaustion is not enumeration exhaustion | `validation/invariants.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 81519–81525 | 27.30 New invariants › E4 — Cursor progress must be durable | `validation/invariants.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 81527–81531 | 27.30 New invariants › E5 — Enumeration entries are not candidates | `validation/invariants.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 81533–81537 | 27.30 New invariants › E6 — Cardinality is evidence | `validation/invariants.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 81539–81541 | 27.30 New invariants › E7 — Historical snapshots remain immutable | `validation/invariants.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 81543–81549 | 27.30 New invariants › E8 — Incomplete enumeration cannot establish absence | `validation/invariants.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 81551–81553 | 27.30 New invariants › E9 — Unstable enumeration weakens completeness | `validation/invariants.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 81555–81557 | 27.30 New invariants › E10 — Enumerator has no acquisition authority | `validation/invariants.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 81559–81561 | 27.30 New invariants › E11 — Enumerator cannot directly mutate the ResourceGraph | `validation/invariants.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 81563–81567 | 27.30 New invariants › E12 — Termination evidence is provenance-bearing | `validation/invariants.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 81569–81606 | 27.31 The emerging blind-scan analogy | `research/dvb-blind-scan.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 81608–81646 | v0.27 takeaway | `architecture/strategy-and-planning.md` | MOVED | v0.27 |
| `Continue Architecture Planning.md` | 81648–81672 | v0.28 — Search-Space Reconciliation & Frontier Deduplication | `architecture/search-space.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 81678–81678 | *turn 68 you lead-in* | — (removed) | ARTIFACT | v0.28; conversation continuation marker |
| `Continue Architecture Planning.md` | 81684–81726 | v0.28 — Search-Space Reconciliation & Frontier Deduplication | `architecture/search-space.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 81728–81776 | 28.1 The problem with naive deduplication | `architecture/search-space.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 81778–81802 | 28.2 Five different kinds of duplication | `architecture/search-space.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 81804–81846 | 28.3 Search-space overlap | `architecture/search-space.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 81848–81892 | 28.4 SearchPartitionRelation | `architecture/search-space.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 81894–81937 | 28.5 Coverage overlap | `architecture/search-space.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 81939–81969 | 28.6 Frontier deduplication | `architecture/search-space.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 81971–82027 | 28.7 SearchWorkKey | `architecture/search-space.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 82029–82063 | 28.8 Work equivalence | `architecture/search-space.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 82065–82106 | 28.9 Candidate convergence | `architecture/search-space.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 82108–82155 | 28.10 Observation convergence | `architecture/observation-model.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 82157–82197 | 28.11 Artifact convergence | `architecture/search-space.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 82199–82239 | 28.12 Discovery independence | `architecture/search-space.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 82241–82281 | 28.13 Evidence independence model | `architecture/search-space.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 82283–82323 | 28.14 Coverage provenance | `architecture/search-space.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 82325–82360 | 28.15 Coverage relation | `architecture/search-space.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 82362–82389 | 28.16 Coverage union | `architecture/search-space.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 82391–82425 | 28.17 Disjoint partitions | `architecture/search-space.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 82427–82460 | 28.18 Unknown overlap | `architecture/search-space.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 82462–82506 | 28.19 Frontier duplicate suppression | `architecture/search-space.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 82508–82543 | 28.20 Duplicate suppression must preserve provenance | `architecture/search-space.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 82545–82577 | 28.21 Convergence graph | `architecture/search-space.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 82579–82605 | 28.22 Search-space graph | `architecture/search-space.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 82607–82640 | 28.23 Search-space coverage ledger | `architecture/search-space.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 82642–82693 | 28.24 Candidate count is not coverage | `architecture/search-space.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 82695–82697 | 28.25 Search-space deduplication vs candidate deduplication | `architecture/search-space.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 82699–82705 | 28.25 Search-space deduplication vs candidate deduplication › Candidate deduplication | `architecture/search-space.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 82707–82734 | 28.25 Search-space deduplication vs candidate deduplication › Search-space deduplication | `architecture/search-space.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 82736–82786 | 28.26 Adaptive strategy interaction | `architecture/search-space.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 82788–82839 | 28.27 Example | `architecture/search-space.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 82841–82883 | 28.28 Reconciliation algorithm | `architecture/search-space.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 82885–82922 | 28.29 Reconciliation must be monotonic | `architecture/search-space.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 82924–82946 | 28.30 Reconciliation does not delete evidence | `architecture/search-space.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 82948–82989 | 28.31 Failure taxonomy | `validation/failure-taxonomy.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 82991–82991 | 28.32 Core invariants | `validation/invariants.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 82993–82995 | 28.32 Core invariants › R1 — Candidate convergence | `validation/invariants.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 82997–82999 | 28.32 Core invariants › R2 — Provenance preservation | `validation/invariants.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 83001–83003 | 28.32 Core invariants › R3 — Artifact convergence | `validation/invariants.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 83005–83007 | 28.32 Core invariants › R4 — Observation preservation | `validation/invariants.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 83009–83019 | 28.32 Core invariants › R5 — Overlap is not duplication | `validation/invariants.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 83021–83023 | 28.32 Core invariants › R6 — Equivalent work may be suppressed | `validation/invariants.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 83025–83027 | 28.32 Core invariants › R7 — Suppression preserves provenance | `validation/invariants.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 83029–83035 | 28.32 Core invariants › R8 — Unknown overlap is not disjointness | `validation/invariants.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 83037–83039 | 28.32 Core invariants › R9 — Coverage is union-aware | `validation/invariants.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 83041–83047 | 28.32 Core invariants › R10 — Candidate count does not establish coverage | `validation/invariants.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 83049–83051 | 28.32 Core invariants › R11 — Evidence independence must be justified | `validation/invariants.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 83053–83057 | 28.32 Core invariants › R12 — Historical reconciliation is immutable | `validation/invariants.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 83059–83128 | 28.33 v0.28 architecture | `architecture/system-model.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 83130–83165 | 28.34 The deeper architectural result | `architecture/search-space.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 83167–83226 | 28.34 The deeper architectural result › Next boundary — v0.29 | `roadmap/future-work.md` | MOVED | v0.28 |
| `Continue Architecture Planning.md` | 83232–83232 | *turn 70 you lead-in* | — (removed) | ARTIFACT | v0.28; conversation continuation marker |
| `Continue Architecture Planning.md` | 83238–83284 | v0.29 — Dynamic Search-Space Expansion | `architecture/search-space.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 83286–83322 | 29.1 The central distinction | `architecture/search-space.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 83324–83376 | 29.2 PartitionProposal | `architecture/search-space.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 83378–83410 | 29.3 Why proposals are necessary | `architecture/search-space.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 83412–83460 | 29.4 PartitionAdmissionController | `architecture/search-space.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 83462–83522 | 29.5 Partition identity | `architecture/search-space.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 83524–83550 | 29.6 Partition explosion | `architecture/search-space.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 83552–83581 | 29.7 ExpansionBudget | `architecture/search-space.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 83583–83606 | 29.8 Local expansion rate | `architecture/search-space.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 83608–83640 | 29.9 Expansion rate limiting | `architecture/search-space.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 83642–83670 | 29.10 Evidence threshold | `architecture/search-space.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 83672–83693 | 29.11 Partition proposal epistemic status | `architecture/search-space.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 83695–83726 | 29.12 Hypothesis connection | `architecture/search-space.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 83728–83779 | 29.13 Partition generation sources | `architecture/search-space.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 83781–83812 | 29.14 Expansion provider boundary | `architecture/search-space.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 83814–83843 | 29.15 Dynamic search-space graph | `architecture/search-space.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 83845–83889 | 29.16 Partition generation event | `architecture/search-space.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 83891–83922 | 29.17 Search-space versioning | `architecture/search-space.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 83924–83960 | 29.18 SearchSpaceSnapshot | `architecture/search-space.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 83962–84007 | 29.19 Expansion and completeness | `architecture/search-space.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 84009–84053 | 29.20 Dynamic expansion and negative evidence | `architecture/search-space.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 84055–84083 | 29.21 Expansion priorities | `architecture/search-space.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 84085–84120 | 29.22 Expansion depth | `architecture/search-space.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 84122–84165 | 29.23 Expansion loops | `architecture/search-space.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 84167–84195 | 29.24 Expansion cycle ≠ failure | `architecture/search-space.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 84197–84230 | 29.25 Partition admission states | `architecture/search-space.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 84232–84262 | 29.26 Partition proposal accounting | `architecture/search-space.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 84264–84289 | 29.27 Partition explosion protection | `architecture/search-space.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 84291–84337 | 29.28 Admission algorithm | `architecture/search-space.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 84339–84367 | 29.29 Frontier generation | `architecture/search-space.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 84369–84399 | 29.30 Dynamic expansion architecture | `architecture/system-model.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 84401–84437 | 29.31 Two expansion paths | `architecture/search-space.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 84439–84463 | 29.32 Search-space discovery as first-class knowledge | `architecture/search-space.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 84465–84465 | 29.33 v0.29 invariants | `validation/invariants.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 84467–84475 | 29.33 v0.29 invariants › P1 — Discovery does not create authority | `validation/invariants.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 84477–84481 | 29.33 v0.29 invariants › P2 — Partition proposal is not partition | `validation/invariants.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 84483–84487 | 29.33 v0.29 invariants › P3 — Every admitted partition belongs to the domain | `validation/invariants.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 84489–84491 | 29.33 v0.29 invariants › P4 — Expansion is budgeted | `validation/invariants.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 84493–84495 | 29.33 v0.29 invariants › P5 — Expansion is depth-bounded | `validation/invariants.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 84497–84499 | 29.33 v0.29 invariants › P6 — Duplicate partitions converge | `validation/invariants.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 84501–84503 | 29.33 v0.29 invariants › P7 — Overlap is preserved | `validation/invariants.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 84505–84507 | 29.33 v0.29 invariants › P8 — Evidence is preserved | `validation/invariants.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 84509–84515 | 29.33 v0.29 invariants › P9 — Partition existence does not schedule execution | `validation/invariants.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 84517–84519 | 29.33 v0.29 invariants › P10 — Expansion cannot override policy | `validation/invariants.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 84521–84523 | 29.33 v0.29 invariants › P11 — Search-space versions are immutable | `validation/invariants.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 84525–84527 | 29.33 v0.29 invariants › P12 — Expansion does not invalidate historical claims automatically | `validation/invariants.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 84529–84531 | 29.33 v0.29 invariants › P13 — Cycles are legal | `validation/invariants.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 84533–84543 | 29.33 v0.29 invariants › P14 — Unknown remains valid | `validation/invariants.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 84545–84576 | 29.34 The system after v0.29 | `architecture/search-space.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 84578–84608 | 29.35 Blind-scan interpretation | `research/dvb-blind-scan.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 84610–84662 | v0.29 takeaway | `architecture/search-space.md` | MOVED | v0.29 |
| `Continue Architecture Planning.md` | 84664–84685 | v0.30 — Unified Frontier Arbitration | `architecture/work-and-frontier.md` | MOVED | v0.30 |
| `Continue Architecture Planning.md` | 84691–84691 | *turn 72 you lead-in* | — (removed) | ARTIFACT | v0.30; conversation continuation marker |
| `Continue Architecture Planning.md` | 84697–84760 | Conclusion — Generic Discovery Engine | `concepts/overview.md` | MOVED | v0.30 |
| `Continue Architecture Planning.md` | 84762–84791 | Conclusion — Generic Discovery Engine › The final conceptual separation | `architecture/work-and-frontier.md` | MOVED | v0.30 |
| `Continue Architecture Planning.md` | 84793–84843 | The fundamental invariant | `validation/invariants.md` | MOVED | v0.30 |
| `Continue Architecture Planning.md` | 84845–84908 | What the DVB analogy actually contributed | `research/dvb-blind-scan.md` | MOVED | v0.30 |
| `Continue Architecture Planning.md` | 84910–84948 | The most important safety boundary | `architecture/work-and-frontier.md` | MOVED | v0.30 |
| `Continue Architecture Planning.md` | 84950–85022 | Final architecture | `architecture/system-model.md` | MOVED | v0.30 |
| `Continue Architecture Planning.md` | 85024–85066 | What the userscript should and should not become | `prototype/limitations.md` | MOVED | v0.30; explicit override |
| `Continue Architecture Planning.md` | 85068–85125 | Final principles | `concepts/overview.md` | MOVED | v0.30 |
| `Continue Architecture Planning.md` | 85131–85131 | *turn 74 you lead-in* | `architecture/work-and-frontier.md` | MOVED | v0.30; lead-in of the following section |
| `Continue Architecture Planning.md` | 85137–85169 | v0.30 — Unified Frontier Arbitration | `architecture/work-and-frontier.md` | MOVED | v0.30 |
| `Continue Architecture Planning.md` | 85171–85213 | v0.30 — Unified Frontier Arbitration › 30.1 The new architecture | `architecture/system-model.md` | MOVED | v0.30 |
| `Continue Architecture Planning.md` | 85215–85256 | 30.2 WorkClass | `architecture/work-and-frontier.md` | MOVED | v0.30 |
| `Continue Architecture Planning.md` | 85258–85314 | 30.3 WorkClassPolicy | `architecture/work-and-frontier.md` | MOVED | v0.30 |
| `Continue Architecture Planning.md` | 85316–85382 | 30.4 ArbitrationDecision | `architecture/work-and-frontier.md` | MOVED | v0.30 |
| `Continue Architecture Planning.md` | 85384–85386 | 30.5 Hard constraints vs soft priorities | `architecture/work-and-frontier.md` | MOVED | v0.30 |
| `Continue Architecture Planning.md` | 85388–85402 | 30.5 Hard constraints vs soft priorities › Hard constraints | `architecture/work-and-frontier.md` | MOVED | v0.30 |
| `Continue Architecture Planning.md` | 85404–85441 | 30.5 Hard constraints vs soft priorities › Soft priorities | `architecture/work-and-frontier.md` | MOVED | v0.30 |
| `Continue Architecture Planning.md` | 85443–85480 | 30.6 Arbitration score | `architecture/work-and-frontier.md` | MOVED | v0.30 |
| `Continue Architecture Planning.md` | 85482–85531 | 30.7 Aging | `architecture/work-and-frontier.md` | MOVED | v0.30 |
| `Continue Architecture Planning.md` | 85533–85579 | 30.8 Starvation detection | `architecture/work-and-frontier.md` | MOVED | v0.30 |
| `Continue Architecture Planning.md` | 85581–85625 | 30.9 Class starvation | `architecture/work-and-frontier.md` | MOVED | v0.30 |
| `Continue Architecture Planning.md` | 85627–85656 | 30.10 Weighted fairness | `architecture/work-and-frontier.md` | MOVED | v0.30 |
| `Continue Architecture Planning.md` | 85658–85704 | 30.11 Deficit-style arbitration | `architecture/work-and-frontier.md` | MOVED | v0.30 |
| `Continue Architecture Planning.md` | 85706–85759 | 30.12 Cost-aware scheduling | `architecture/work-and-frontier.md` | MOVED | v0.30 |
| `Continue Architecture Planning.md` | 85761–85818 | 30.13 Backpressure | `architecture/work-and-frontier.md` | MOVED | v0.30 |
| `Continue Architecture Planning.md` | 85820–85854 | 30.14 Reserved capacity | `architecture/work-and-frontier.md` | MOVED | v0.30 |
| `Continue Architecture Planning.md` | 85856–85909 | 30.15 Arbitration pipeline | `architecture/work-and-frontier.md` | MOVED | v0.30 |
| `Continue Architecture Planning.md` | 85911–85957 | 30.16 The atomicity problem | `architecture/work-and-frontier.md` | MOVED | v0.30 |
| `Continue Architecture Planning.md` | 85959–85997 | 30.17 Priority inversion | `architecture/work-and-frontier.md` | MOVED | v0.30 |
| `Continue Architecture Planning.md` | 85999–86050 | 30.18 FrontierArbitrator | `architecture/work-and-frontier.md` | MOVED | v0.30 |
| `Continue Architecture Planning.md` | 86052–86090 | 30.19 Arbitration result | `architecture/work-and-frontier.md` | MOVED | v0.30 |
| `Continue Architecture Planning.md` | 86092–86119 | 30.20 Arbitration ledger | `architecture/work-and-frontier.md` | MOVED | v0.30 |
| `Continue Architecture Planning.md` | 86121–86172 | 30.21 Replay | `architecture/work-and-frontier.md` | MOVED | v0.30 |
| `Continue Architecture Planning.md` | 86174–86218 | 30.22 The deeper invariant | `validation/invariants.md` | MOVED | v0.30 |
| `Continue Architecture Planning.md` | 86220–86280 | 30.23 Full v0.30 architecture | `architecture/system-model.md` | MOVED | v0.30 |
| `Continue Architecture Planning.md` | 86282–86305 | 30.24 Failure taxonomy | `validation/failure-taxonomy.md` | MOVED | v0.30 |
| `Continue Architecture Planning.md` | 86307–86356 | 30.25 v0.30 invariants | `validation/invariants.md` | MOVED | v0.30 |
| `Continue Architecture Planning.md` | 86358–86398 | 30.26 What v0.30 actually accomplishes | `concepts/overview.md` | MOVED | v0.30 |
| `Continue Architecture Planning.md` | 86400–86466 | Next boundary — v0.31 | `roadmap/future-work.md` | MOVED | v0.30 |
| `Continue Architecture Planning.md` | 86472–86472 | *turn 76 you lead-in* | — (removed) | ARTIFACT | v0.30; conversation continuation marker |
| `Continue Architecture Planning.md` | 86478–86517 | v0.31 — Unified Resource & Cost Ledger | `architecture/resource-budget.md` | MOVED | v0.31 |
| `Continue Architecture Planning.md` | 86519–86576 | v0.31 — Unified Resource & Cost Ledger › 31.1 Resource dimensions | `architecture/resource-budget.md` | MOVED | v0.31 |
| `Continue Architecture Planning.md` | 86578–86627 | 31.2 ResourceBudget | `architecture/resource-budget.md` | MOVED | v0.31 |
| `Continue Architecture Planning.md` | 86629–86672 | 31.3 Three resource states | `architecture/resource-budget.md` | MOVED | v0.31 |
| `Continue Architecture Planning.md` | 86674–86734 | 31.4 ResourceReservation | `architecture/resource-budget.md` | MOVED | v0.31 |
| `Continue Architecture Planning.md` | 86736–86789 | 31.5 Estimated cost vs actual cost | `architecture/resource-budget.md` | MOVED | v0.31 |
| `Continue Architecture Planning.md` | 86791–86844 | 31.6 CostObservation | `architecture/resource-budget.md` | MOVED | v0.31 |
| `Continue Architecture Planning.md` | 86846–86879 | 31.7 ResourceLedger | `architecture/resource-budget.md` | MOVED | v0.31 |
| `Continue Architecture Planning.md` | 86881–86933 | 31.8 Budget scopes | `architecture/resource-budget.md` | MOVED | v0.31 |
| `Continue Architecture Planning.md` | 86935–86974 | 31.9 Hierarchical budget accounting | `architecture/resource-budget.md` | MOVED | v0.31 |
| `Continue Architecture Planning.md` | 86976–87027 | 31.10 Resource allocation | `architecture/resource-budget.md` | MOVED | v0.31 |
| `Continue Architecture Planning.md` | 87029–87055 | 31.11 Allocation is not execution | `architecture/resource-budget.md` | MOVED | v0.31 |
| `Continue Architecture Planning.md` | 87057–87102 | 31.12 Partial consumption | `architecture/resource-budget.md` | MOVED | v0.31 |
| `Continue Architecture Planning.md` | 87104–87146 | 31.13 Cost overruns | `architecture/resource-budget.md` | MOVED | v0.31 |
| `Continue Architecture Planning.md` | 87148–87205 | 31.14 Cost model | `architecture/resource-budget.md` | MOVED | v0.31 |
| `Continue Architecture Planning.md` | 87207–87242 | 31.15 Cost is context-dependent | `architecture/resource-budget.md` | MOVED | v0.31 |
| `Continue Architecture Planning.md` | 87244–87286 | 31.16 Resource exhaustion | `architecture/resource-budget.md` | MOVED | v0.31 |
| `Continue Architecture Planning.md` | 87288–87323 | 31.17 Budget exhaustion vs frontier exhaustion | `architecture/resource-budget.md` | MOVED | v0.31 |
| `Continue Architecture Planning.md` | 87325–87363 | 31.18 Resource reservation race | `architecture/resource-budget.md` | MOVED | v0.31 |
| `Continue Architecture Planning.md` | 87365–87415 | 31.19 Settlement | `architecture/resource-budget.md` | MOVED | v0.31 |
| `Continue Architecture Planning.md` | 87417–87459 | 31.20 Cost feedback | `architecture/resource-budget.md` | MOVED | v0.31 |
| `Continue Architecture Planning.md` | 87461–87491 | 31.21 ResourceLedger events | `architecture/resource-budget.md` | MOVED | v0.31 |
| `Continue Architecture Planning.md` | 87493–87536 | 31.22 Resource accounting and provenance | `architecture/resource-budget.md` | MOVED | v0.31 |
| `Continue Architecture Planning.md` | 87538–87598 | 31.23 Unified v0.31 architecture | `architecture/system-model.md` | MOVED | v0.31 |
| `Continue Architecture Planning.md` | 87600–87646 | 31.24 The central v0.31 invariants | `validation/invariants.md` | MOVED | v0.31 |
| `Continue Architecture Planning.md` | 87648–87701 | 31.25 What v0.31 adds | `architecture/resource-budget.md` | MOVED | v0.31 |
| `Continue Architecture Planning.md` | 87703–87765 | v0.32 boundary | `architecture/persistence-and-recovery.md` | MOVED | v0.32 |
| `Continue Architecture Planning.md` | 87771–87771 | *turn 78 you lead-in* | — (removed) | ARTIFACT | v0.32; conversation continuation marker |
| `Continue Architecture Planning.md` | 87777–87789 | v0.32 — Transactional Persistence & Crash Recovery | `architecture/persistence-and-recovery.md` | MOVED | v0.32 |
| `Continue Architecture Planning.md` | 87791–87828 | v0.32 — Transactional Persistence & Crash Recovery › 32.1 The crash problem | `architecture/persistence-and-recovery.md` | MOVED | v0.32 |
| `Continue Architecture Planning.md` | 87830–87856 | 32.2 Durable state vs runtime state | `architecture/persistence-and-recovery.md` | MOVED | v0.32 |
| `Continue Architecture Planning.md` | 87858–87893 | 32.3 Persistence is not serialization | `architecture/persistence-and-recovery.md` | MOVED | v0.32 |
| `Continue Architecture Planning.md` | 87895–87940 | 32.4 PersistenceAdapter | `architecture/persistence-and-recovery.md` | MOVED | v0.32 |
| `Continue Architecture Planning.md` | 87942–87990 | 32.5 Transaction | `architecture/persistence-and-recovery.md` | MOVED | v0.32 |
| `Continue Architecture Planning.md` | 87992–88035 | 32.6 Write-ahead event ledger | `architecture/persistence-and-recovery.md` | MOVED | v0.32 |
| `Continue Architecture Planning.md` | 88037–88073 | 32.7 Event identity | `architecture/persistence-and-recovery.md` | MOVED | v0.32 |
| `Continue Architecture Planning.md` | 88075–88106 | 32.8 Monotonic sequence | `architecture/persistence-and-recovery.md` | MOVED | v0.32 |
| `Continue Architecture Planning.md` | 88108–88145 | 32.9 Commit protocol | `architecture/persistence-and-recovery.md` | MOVED | v0.32 |
| `Continue Architecture Planning.md` | 88147–88170 | 32.10 Commit markers | `architecture/persistence-and-recovery.md` | MOVED | v0.32 |
| `Continue Architecture Planning.md` | 88172–88211 | 32.11 Checkpoint correctness | `architecture/persistence-and-recovery.md` | MOVED | v0.32 |
| `Continue Architecture Planning.md` | 88213–88245 | 32.12 At-least-once vs exactly-once | `architecture/persistence-and-recovery.md` | MOVED | v0.32 |
| `Continue Architecture Planning.md` | 88247–88282 | 32.13 Idempotency | `architecture/persistence-and-recovery.md` | MOVED | v0.32 |
| `Continue Architecture Planning.md` | 88284–88331 | 32.14 Work recovery | `architecture/persistence-and-recovery.md` | MOVED | v0.32 |
| `Continue Architecture Planning.md` | 88333–88367 | 32.15 Recovery scan | `architecture/persistence-and-recovery.md` | MOVED | v0.32 |
| `Continue Architecture Planning.md` | 88369–88404 | 32.16 RecoveryManager | `architecture/persistence-and-recovery.md` | MOVED | v0.32 |
| `Continue Architecture Planning.md` | 88406–88452 | 32.17 Reservation recovery | `architecture/persistence-and-recovery.md` | MOVED | v0.32 |
| `Continue Architecture Planning.md` | 88454–88470 | 32.18 Accounting invariant under crash | `validation/invariants.md` | MOVED | v0.32 |
| `Continue Architecture Planning.md` | 88472–88499 | 32.19 Observation recovery | `architecture/observation-model.md` | MOVED | v0.32 |
| `Continue Architecture Planning.md` | 88501–88531 | 32.20 Artifact durability | `architecture/persistence-and-recovery.md` | MOVED | v0.32 |
| `Continue Architecture Planning.md` | 88533–88566 | 32.21 Durable checkpoint | `architecture/persistence-and-recovery.md` | MOVED | v0.32 |
| `Continue Architecture Planning.md` | 88568–88589 | 32.22 Recovery invariant for cursors | `validation/invariants.md` | MOVED | v0.32 |
| `Continue Architecture Planning.md` | 88591–88621 | 32.23 Schema versioning | `architecture/persistence-and-recovery.md` | MOVED | v0.32 |
| `Continue Architecture Planning.md` | 88623–88659 | 32.24 Snapshot + journal | `architecture/persistence-and-recovery.md` | MOVED | v0.32 |
| `Continue Architecture Planning.md` | 88661–88686 | 32.25 Snapshot integrity | `architecture/persistence-and-recovery.md` | MOVED | v0.32 |
| `Continue Architecture Planning.md` | 88688–88731 | 32.26 Recovery outcomes | `architecture/persistence-and-recovery.md` | MOVED | v0.32 |
| `Continue Architecture Planning.md` | 88733–88753 | 32.27 Recovery must not fabricate knowledge | `architecture/persistence-and-recovery.md` | MOVED | v0.32 |
| `Continue Architecture Planning.md` | 88755–88778 | 32.28 Crash-safe frontier | `architecture/persistence-and-recovery.md` | MOVED | v0.32 |
| `Continue Architecture Planning.md` | 88780–88822 | 32.29 Reconciliation | `architecture/persistence-and-recovery.md` | MOVED | v0.32 |
| `Continue Architecture Planning.md` | 88824–88844 | 32.30 Repair is itself provenance | `architecture/persistence-and-recovery.md` | MOVED | v0.32 |
| `Continue Architecture Planning.md` | 88846–88895 | 32.31 v0.32 architecture | `architecture/system-model.md` | MOVED | v0.32 |
| `Continue Architecture Planning.md` | 88897–88933 | 32.32 Complete lifecycle | `architecture/persistence-and-recovery.md` | MOVED | v0.32 |
| `Continue Architecture Planning.md` | 88935–88959 | 32.33 Failure taxonomy | `validation/failure-taxonomy.md` | MOVED | v0.32 |
| `Continue Architecture Planning.md` | 88961–89008 | 32.34 v0.32 invariants | `validation/invariants.md` | MOVED | v0.32 |
| `Continue Architecture Planning.md` | 89010–89040 | 32.35 What v0.32 changes | `architecture/persistence-and-recovery.md` | MOVED | v0.32 |
| `Continue Architecture Planning.md` | 89042–89108 | v0.33 — Multi-Worker / Multi-Context Coordination | `architecture/concurrency.md` | MOVED | v0.33 |
| `Continue Architecture Planning.md` | 89114–89114 | *turn 80 you lead-in* | — (removed) | ARTIFACT | v0.33; conversation continuation marker |
| `Continue Architecture Planning.md` | 89120–89144 | v0.33 — Multi-Worker Coordination & Distributed Claiming | `architecture/concurrency.md` | MOVED | v0.33 |
| `Continue Architecture Planning.md` | 89146–89198 | v0.33 — Multi-Worker Coordination & Distributed Claiming › 33.1 Worker identity | `architecture/concurrency.md` | MOVED | v0.33 |
| `Continue Architecture Planning.md` | 89200–89249 | 33.2 Worker registration | `architecture/concurrency.md` | MOVED | v0.33 |
| `Continue Architecture Planning.md` | 89251–89300 | 33.3 Worker capabilities | `architecture/concurrency.md` | MOVED | v0.33 |
| `Continue Architecture Planning.md` | 89302–89332 | 33.4 Claiming is the synchronization boundary | `architecture/concurrency.md` | MOVED | v0.33 |
| `Continue Architecture Planning.md` | 89334–89379 | 33.5 ClaimToken | `architecture/concurrency.md` | MOVED | v0.33 |
| `Continue Architecture Planning.md` | 89381–89405 | 33.6 Claim ≠ lease | `architecture/concurrency.md` | MOVED | v0.33 |
| `Continue Architecture Planning.md` | 89407–89427 | 33.7 Lease lifecycle | `architecture/concurrency.md` | MOVED | v0.33 |
| `Continue Architecture Planning.md` | 89429–89462 | 33.8 LeaseManager | `architecture/concurrency.md` | MOVED | v0.33 |
| `Continue Architecture Planning.md` | 89464–89486 | 33.9 Heartbeats | `architecture/concurrency.md` | MOVED | v0.33 |
| `Continue Architecture Planning.md` | 89488–89525 | 33.10 Fencing tokens | `architecture/concurrency.md` | MOVED | v0.33 |
| `Continue Architecture Planning.md` | 89527–89554 | 33.11 Fencing invariant | `validation/invariants.md` | MOVED | v0.33 |
| `Continue Architecture Planning.md` | 89556–89591 | 33.12 Worker death | `architecture/concurrency.md` | MOVED | v0.33 |
| `Continue Architecture Planning.md` | 89593–89621 | 33.13 Duplicate execution | `architecture/concurrency.md` | MOVED | v0.33 |
| `Continue Architecture Planning.md` | 89623–89655 | 33.14 Execution identity | `architecture/concurrency.md` | MOVED | v0.33 |
| `Continue Architecture Planning.md` | 89657–89696 | 33.15 Duplicate observations | `architecture/observation-model.md` | MOVED | v0.33 |
| `Continue Architecture Planning.md` | 89698–89728 | 33.16 Duplicate execution ≠ independent evidence | `architecture/concurrency.md` | MOVED | v0.33 |
| `Continue Architecture Planning.md` | 89730–89765 | 33.17 Worker-local vs shared state | `architecture/concurrency.md` | MOVED | v0.33 |
| `Continue Architecture Planning.md` | 89767–89801 | 33.18 CoordinationManager | `architecture/concurrency.md` | MOVED | v0.33 |
| `Continue Architecture Planning.md` | 89803–89827 | 33.19 Coordination vs arbitration | `architecture/concurrency.md` | MOVED | v0.33 |
| `Continue Architecture Planning.md` | 89829–89869 | 33.20 Worker selection | `architecture/concurrency.md` | MOVED | v0.33 |
| `Continue Architecture Planning.md` | 89871–89890 | 33.21 Worker affinity | `architecture/concurrency.md` | MOVED | v0.33 |
| `Continue Architecture Planning.md` | 89892–89919 | 33.22 Worker capacity | `architecture/concurrency.md` | MOVED | v0.33 |
| `Continue Architecture Planning.md` | 89921–89953 | 33.23 Distributed accounting | `architecture/concurrency.md` | MOVED | v0.33 |
| `Continue Architecture Planning.md` | 89955–89977 | 33.24 Worker-local caches | `architecture/concurrency.md` | MOVED | v0.33 |
| `Continue Architecture Planning.md` | 89979–90012 | 33.25 Cross-worker event ordering | `architecture/concurrency.md` | MOVED | v0.33 |
| `Continue Architecture Planning.md` | 90014–90030 | 33.26 Causal provenance | `architecture/concurrency.md` | MOVED | v0.33 |
| `Continue Architecture Planning.md` | 90032–90060 | 33.27 Coordination events | `architecture/concurrency.md` | MOVED | v0.33 |
| `Continue Architecture Planning.md` | 90062–90083 | 33.28 Multi-worker failure modes | `validation/failure-taxonomy.md` | MOVED | v0.33 |
| `Continue Architecture Planning.md` | 90085–90111 | 33.29 Split-brain | `architecture/concurrency.md` | MOVED | v0.33 |
| `Continue Architecture Planning.md` | 90113–90152 | 33.30 What the browser prototype can guarantee | `prototype/limitations.md` | MOVED | v0.33; explicit override |
| `Continue Architecture Planning.md` | 90154–90178 | 33.31 Coordination scope | `architecture/concurrency.md` | MOVED | v0.33 |
| `Continue Architecture Planning.md` | 90180–90225 | 33.32 v0.33 architecture | `architecture/system-model.md` | MOVED | v0.33 |
| `Continue Architecture Planning.md` | 90227–90248 | 33.33 The complete ownership invariant | `validation/invariants.md` | MOVED | v0.33 |
| `Continue Architecture Planning.md` | 90250–90274 | 33.34 The deeper distributed invariant | `validation/invariants.md` | MOVED | v0.33 |
| `Continue Architecture Planning.md` | 90276–90349 | 33.35 v0.33 result | `architecture/concurrency.md` | MOVED | v0.33 |
| `Continue Architecture Planning.md` | 90351–90396 | v0.34 — Coordination Protocol & Distributed Consistency | `architecture/coordination.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 90402–90402 | *turn 82 you lead-in* | — (removed) | ARTIFACT | v0.34; conversation continuation marker |
| `Continue Architecture Planning.md` | 90408–90446 | v0.34 — Distributed Consistency & Conflict Resolution | `architecture/coordination.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 90448–90498 | 34.1 New Architecture Boundary | `architecture/system-model.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 90500–90585 | 34.2 The Core Consistency Model | `architecture/coordination.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 90587–90651 | 34.3 Optimistic Concurrency Control | `architecture/coordination.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 90653–90694 | 34.4 Version ≠ Time | `architecture/coordination.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 90696–90744 | 34.5 Event Metadata | `architecture/coordination.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 90746–90806 | 34.6 Versioning + Fencing | `architecture/coordination.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 90808–90830 | 34.7 Conflict Is Not One Thing | `architecture/coordination.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 90832–90839 | 34.7 Conflict Is Not One Thing › Claim conflict | `architecture/coordination.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 90841–90848 | 34.7 Conflict Is Not One Thing › Candidate conflict | `architecture/coordination.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 90850–90857 | 34.7 Conflict Is Not One Thing › Classification conflict | `architecture/coordination.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 90859–90873 | 34.7 Conflict Is Not One Thing › Coverage conflict | `architecture/coordination.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 90875–90886 | 34.7 Conflict Is Not One Thing › Budget conflict | `architecture/coordination.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 90888–90952 | 34.8 Conflict Record | `architecture/coordination.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 90954–90985 | 34.9 Deterministic Conflict Resolver | `architecture/coordination.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 90987–91018 | 34.10 Resolution Policies | `architecture/coordination.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 91020–91068 | 34.11 Classification Conflict | `architecture/coordination.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 91070–91112 | 34.12 Provenance Must Survive Resolution | `architecture/coordination.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 91114–91156 | 34.13 Last-Write-Wins Is Not the Default | `architecture/coordination.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 91158–91197 | 34.14 Append-Only Is Especially Powerful | `architecture/coordination.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 91199–91256 | 34.15 Materialized State | `architecture/coordination.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 91258–91304 | 34.16 State Digest | `architecture/coordination.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 91306–91344 | 34.17 Conflict Detection Pipeline | `architecture/coordination.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 91346–91374 | 34.18 Conflict Detection vs Conflict Resolution | `architecture/coordination.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 91376–91420 | 34.19 Conflict Resolver Context | `architecture/coordination.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 91422–91457 | 34.20 Resolution Event | `architecture/coordination.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 91459–91496 | 34.21 Cross-Object Conflicts | `architecture/coordination.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 91498–91549 | 34.22 Consistency Domains | `architecture/coordination.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 91551–91585 | 34.23 Consistency Is Not Global Ordering | `architecture/coordination.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 91587–91622 | 34.24 Independent Evidence | `architecture/coordination.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 91624–91666 | 34.25 Failure Taxonomy | `validation/failure-taxonomy.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 91668–91668 | 34.26 New Core Invariants | `validation/invariants.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 91670–91677 | 34.26 New Core Invariants › Consistency | `architecture/coordination.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 91679–91683 | 34.26 New Core Invariants › Fencing | `architecture/coordination.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 91685–91693 | 34.26 New Core Invariants › Conflict | `architecture/coordination.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 91695–91700 | 34.26 New Core Invariants › Provenance | `architecture/coordination.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 91702–91707 | 34.26 New Core Invariants › Recovery | `architecture/coordination.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 91709–91716 | 34.26 New Core Invariants › Scalability | `architecture/coordination.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 91718–91798 | 34.27 The Unified State Model | `architecture/coordination.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 91800–91800 | 34.28 What v0.34 Actually Proves | `validation/verification.md` | MOVED | v0.34; explicit override |
| `Continue Architecture Planning.md` | 91802–91832 | 34.28 What v0.34 Actually Proves › PROVED by the architecture | `validation/verification.md` | MOVED | v0.34; explicit override |
| `Continue Architecture Planning.md` | 91834–91836 | 34.28 What v0.34 Actually Proves › ARGUMENT | `validation/verification.md` | MOVED | v0.34; explicit override |
| `Continue Architecture Planning.md` | 91838–91857 | 34.28 What v0.34 Actually Proves › OPEN | `validation/verification.md` | MOVED | v0.34; explicit override |
| `Continue Architecture Planning.md` | 91859–91905 | 34.29 Prototype Boundary | `prototype/limitations.md` | MOVED | v0.34; explicit override |
| `Continue Architecture Planning.md` | 91907–91970 | 34.30 v0.34 → v0.35 | `roadmap/future-work.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 91976–91976 | *turn 84 you lead-in* | — (removed) | ARTIFACT | v0.34; conversation continuation marker |
| `Continue Architecture Planning.md` | 91982–92057 | Conclusion — Generic Discovery Engine | `concepts/overview.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 92059–92087 | Conclusion — Generic Discovery Engine › The decisive conceptual shift | `concepts/overview.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 92089–92101 | The decisive conceptual shift › DVB blind scan | `research/dvb-blind-scan.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 92103–92123 | The decisive conceptual shift › Generic discovery | `architecture/coordination.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 92125–92156 | The major architectural invariants | `validation/invariants.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 92158–92188 | Final architecture by responsibility | `architecture/system-model.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 92190–92237 | What the prototype actually becomes | `concepts/overview.md` | MOVED | v0.34 |
| `Continue Architecture Planning.md` | 92239–92275 | Final formulation | `concepts/overview.md` | MOVED | v0.34 |

## Duplicate handling

| Duplicate source | Retained canonical copy | Type | Notes |
| --- | --- | --- | --- |
| `Continue Architecture Planning.md` L3–16 (flattened v0.1.0 + v0.2.0 paste) | `prototype/versions/01-v0.1.0.md`, `prototype/versions/02-v0.2.0.md` | near-duplicate | Same two scripts, pasted into the planning conversation with internal line breaks lost. Both copies are retained: the planning-conversation paste is preserved verbatim in `prototype/versions/00-v0.1.0-and-v0.2.0-paste.md`, because the two copies are damaged differently (see [Review Notes](REVIEW-NOTES.md)). |

## Related Documents

- [Documentation index](README.md)
- [Review Notes](REVIEW-NOTES.md)
- [Prototype Overview](prototype/overview.md)
- [Architecture Overview](architecture/overview.md)

