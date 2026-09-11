# Source Map

> **Status:** CURRENT
>
> **Source:** `Userscript Discovery Prototype.md`; `Continue Architecture Planning.md`
>
> **Purpose:** Primary audit mechanism of the mechanical split: every extracted source section, its destination, action and status.

Identifiers are stable and assigned in document order:
`USP-nnn` = `Userscript Discovery Prototype.md`, `CAP-nnn` = `Continue Architecture Planning.md`.

Line numbers refer to the original documents as committed before the split. The archived copies carry an 11-line `ARCHIVED SOURCE DOCUMENT` header, so add 11 to map these numbers onto [`archive/`](../archive/).

## Accounting

| Metric | Count |
| --- | --- |
| Total source sections | 1244 |
| MOVE | 1199 |
| MERGE | 0 |
| DUPLICATE | 1 |
| ARCHIVE | 44 |
| REVIEW | 0 |
| Unaccounted | 0 |

Dispositions: `MOVE` — carried into the destination; `DUPLICATE` — retained copy of material that also exists elsewhere (see [Duplicates](#duplicates)); `ARCHIVE` — conversation continuation marker, not carried into the tree, preserved in the archived source document.

## By status

| Status | Sections |
| --- | --- |
| DESIGNED | 1129 |
| UNVERIFIED | 45 |
| CURRENT | 36 |
| FUTURE | 19 |
| OPEN | 15 |

## By category

| Category | Sections |
| --- | --- |
| ARCHITECTURE | 235 |
| ALGORITHM | 210 |
| VALIDATION | 166 |
| DATA_MODEL | 146 |
| SCHEDULING | 71 |
| ACQUISITION | 52 |
| CONCURRENCY | 52 |
| UNKNOWN | 44 |
| DISCOVERY | 36 |
| PROVENANCE | 36 |
| CANDIDATE | 34 |
| PROVIDER | 30 |
| CONCEPT | 20 |
| ROADMAP | 19 |
| OBSERVATION | 17 |
| IMPLEMENTATION | 16 |
| DVB_ANALOGY | 15 |
| HISTORY | 14 |
| SECURITY | 11 |
| EXAMPLE | 7 |
| SCOPE | 6 |
| LIMITATIONS | 4 |
| PROTOTYPE | 2 |
| DUPLICATE | 1 |

## By destination

| Destination | Sections | Bytes |
| --- | --- | --- |
| [`acquisition/acquisition-model.md`](acquisition/acquisition-model.md) | 8 | 8023 |
| [`acquisition/overview.md`](acquisition/overview.md) | 3 | 3176 |
| [`acquisition/response-recognition.md`](acquisition/response-recognition.md) | 24 | 21807 |
| [`acquisition/runtime.md`](acquisition/runtime.md) | 18 | 17261 |
| [`architecture/candidate-model.md`](architecture/candidate-model.md) | 9 | 8177 |
| [`architecture/capability-model.md`](architecture/capability-model.md) | 17 | 17474 |
| [`architecture/classification.md`](architecture/classification.md) | 23 | 25270 |
| [`architecture/concurrency.md`](architecture/concurrency.md) | 36 | 33473 |
| [`architecture/coordination.md`](architecture/coordination.md) | 38 | 35176 |
| [`architecture/coverage-and-absence.md`](architecture/coverage-and-absence.md) | 50 | 51190 |
| [`architecture/discovery-model.md`](architecture/discovery-model.md) | 26 | 30875 |
| [`architecture/evidence-model.md`](architecture/evidence-model.md) | 41 | 29150 |
| [`architecture/goal-and-query.md`](architecture/goal-and-query.md) | 64 | 60204 |
| [`architecture/observation-model.md`](architecture/observation-model.md) | 13 | 8675 |
| [`architecture/overview.md`](architecture/overview.md) | 1 | 3097 |
| [`architecture/persistence-and-recovery.md`](architecture/persistence-and-recovery.md) | 32 | 26512 |
| [`architecture/provenance.md`](architecture/provenance.md) | 12 | 10712 |
| [`architecture/provider-architecture.md`](architecture/provider-architecture.md) | 13 | 10977 |
| [`architecture/resource-budget.md`](architecture/resource-budget.md) | 24 | 22221 |
| [`architecture/resource-model.md`](architecture/resource-model.md) | 81 | 61657 |
| [`architecture/scheduler.md`](architecture/scheduler.md) | 11 | 9640 |
| [`architecture/search-space.md`](architecture/search-space.md) | 106 | 82145 |
| [`architecture/sessions-and-domains.md`](architecture/sessions-and-domains.md) | 31 | 24128 |
| [`architecture/strategy-and-planning.md`](architecture/strategy-and-planning.md) | 101 | 81748 |
| [`architecture/system-model.md`](architecture/system-model.md) | 36 | 90444 |
| [`architecture/work-and-frontier.md`](architecture/work-and-frontier.md) | 52 | 50421 |
| [`concepts/discovery-loop.md`](concepts/discovery-loop.md) | 9 | 6803 |
| [`concepts/generic-discovery.md`](concepts/generic-discovery.md) | 8 | 10437 |
| [`concepts/overview.md`](concepts/overview.md) | 16 | 24997 |
| [`prototype/limitations.md`](prototype/limitations.md) | 5 | 6677 |
| [`prototype/overview.md`](prototype/overview.md) | 2 | 4800 |
| [`prototype/userscript.md`](prototype/userscript.md) | 14 | 19970 |
| [`prototype/versions/00-v0.1.0-and-v0.2.0-paste.md`](prototype/versions/00-v0.1.0-and-v0.2.0-paste.md) | 1 | 59164 |
| [`prototype/versions/01-v0.1.0.md`](prototype/versions/01-v0.1.0.md) | 2 | 24582 |
| [`prototype/versions/02-v0.2.0.md`](prototype/versions/02-v0.2.0.md) | 2 | 37415 |
| [`prototype/versions/03-v0.3.0.md`](prototype/versions/03-v0.3.0.md) | 2 | 69377 |
| [`prototype/versions/04-v0.4.0-plan.md`](prototype/versions/04-v0.4.0-plan.md) | 2 | 5068 |
| [`prototype/versions/05-v0.4.0.md`](prototype/versions/05-v0.4.0.md) | 2 | 109431 |
| [`prototype/versions/06-v0.5.0.md`](prototype/versions/06-v0.5.0.md) | 1 | 159805 |
| [`prototype/versions/07-v0.4.0-second-iteration.md`](prototype/versions/07-v0.4.0-second-iteration.md) | 1 | 125923 |
| [`prototype/versions/08-v0.5.0-plan.md`](prototype/versions/08-v0.5.0-plan.md) | 1 | 3125 |
| [`prototype/versions/09-v0.5.0-second-iteration.md`](prototype/versions/09-v0.5.0-second-iteration.md) | 1 | 124311 |
| [`prototype/versions/10-v0.6.0.md`](prototype/versions/10-v0.6.0.md) | 1 | 163288 |
| [`prototype/versions/11-v0.5.0-third-iteration.md`](prototype/versions/11-v0.5.0-third-iteration.md) | 1 | 155812 |
| [`prototype/versions/12-v0.6.0-second-iteration.md`](prototype/versions/12-v0.6.0-second-iteration.md) | 1 | 219379 |
| [`prototype/versions/13-v0.6.0-third-iteration.md`](prototype/versions/13-v0.6.0-third-iteration.md) | 1 | 146345 |
| [`prototype/versions/14-v0.7.1.md`](prototype/versions/14-v0.7.1.md) | 1 | 143285 |
| [`providers/candidate-sources.md`](providers/candidate-sources.md) | 22 | 19305 |
| [`providers/overview.md`](providers/overview.md) | 3 | 4589 |
| [`research/dvb-blind-scan.md`](research/dvb-blind-scan.md) | 15 | 15936 |
| [`roadmap/future-work.md`](roadmap/future-work.md) | 16 | 22438 |
| [`validation/failure-taxonomy.md`](validation/failure-taxonomy.md) | 17 | 17734 |
| [`validation/invariants.md`](validation/invariants.md) | 176 | 70874 |
| [`validation/verification.md`](validation/verification.md) | 7 | 5007 |

## Mapping

| ID | Source | Original Heading | Destination | Action | Status |
| --- | --- | --- | --- | --- | --- |
| USP-001 | `Userscript Discovery Prototype.md` | *turn 0 you lead-in* | `research/dvb-blind-scan.md` | MOVE | DESIGNED |
| USP-002 | `Userscript Discovery Prototype.md` | *turn 1 chatgpt lead-in* | `research/dvb-blind-scan.md` | MOVE | DESIGNED |
| USP-003 | `Userscript Discovery Prototype.md` | Generic pseudocode | `research/dvb-blind-scan.md` | MOVE | DESIGNED |
| USP-004 | `Userscript Discovery Prototype.md` | Making it genuinely generic | `concepts/generic-discovery.md` | MOVE | DESIGNED |
| USP-005 | `Userscript Discovery Prototype.md` | *turn 2 you lead-in* | — | ARCHIVE | UNVERIFIED |
| USP-006 | `Userscript Discovery Prototype.md` | *turn 3 chatgpt lead-in* | `concepts/generic-discovery.md` | MOVE | DESIGNED |
| USP-007 | `Userscript Discovery Prototype.md` | 1. Separate the layers | `concepts/generic-discovery.md` | MOVE | DESIGNED |
| USP-008 | `Userscript Discovery Prototype.md` | 2. Candidate generation | `architecture/candidate-model.md` | MOVE | DESIGNED |
| USP-009 | `Userscript Discovery Prototype.md` | 3. Detection should precede expensive decoding | `acquisition/overview.md` | MOVE | DESIGNED |
| USP-010 | `Userscript Discovery Prototype.md` | 4. Lock is not discovery | `acquisition/response-recognition.md` | MOVE | DESIGNED |
| USP-011 | `Userscript Discovery Prototype.md` | 5. Use DVB metadata to escape blind mode | `research/dvb-blind-scan.md` | MOVE | DESIGNED |
| USP-012 | `Userscript Discovery Prototype.md` | 6. Deduplication | `architecture/candidate-model.md` | MOVE | DESIGNED |
| USP-013 | `Userscript Discovery Prototype.md` | 7. Generic algorithm | `concepts/generic-discovery.md` | MOVE | DESIGNED |
| USP-014 | `Userscript Discovery Prototype.md` | The key insight | `concepts/generic-discovery.md` | MOVE | DESIGNED |
| USP-015 | `Userscript Discovery Prototype.md` | *turn 4 you lead-in* | — | ARCHIVE | UNVERIFIED |
| USP-016 | `Userscript Discovery Prototype.md` | *turn 5 chatgpt lead-in* | `concepts/discovery-loop.md` | MOVE | DESIGNED |
| USP-017 | `Userscript Discovery Prototype.md` | 8. Model scanning as a search problem | `concepts/discovery-loop.md` | MOVE | DESIGNED |
| USP-018 | `Userscript Discovery Prototype.md` | 9. Coarse-to-fine search | `concepts/discovery-loop.md` | MOVE | DESIGNED |
| USP-019 | `Userscript Discovery Prototype.md` | 10. Confidence rather than binary decisions | `architecture/discovery-model.md` | MOVE | DESIGNED |
| USP-020 | `Userscript Discovery Prototype.md` | 11. Don't immediately discard failed candidates | `architecture/scheduler.md` | MOVE | DESIGNED |
| USP-021 | `Userscript Discovery Prototype.md` | 12. Adaptive retry | `architecture/scheduler.md` | MOVE | DESIGNED |
| USP-022 | `Userscript Discovery Prototype.md` | 13. Scheduling becomes important | `architecture/scheduler.md` | MOVE | DESIGNED |
| USP-023 | `Userscript Discovery Prototype.md` | 14. Discovery database | `architecture/system-model.md` | MOVE | DESIGNED |
| USP-024 | `Userscript Discovery Prototype.md` | 15. The generic discovery abstraction | `concepts/generic-discovery.md` | MOVE | DESIGNED |
| USP-025 | `Userscript Discovery Prototype.md` | *turn 6 you lead-in* | — | ARCHIVE | UNVERIFIED |
| USP-026 | `Userscript Discovery Prototype.md` | *turn 7 chatgpt lead-in* | `architecture/discovery-model.md` | MOVE | DESIGNED |
| USP-027 | `Userscript Discovery Prototype.md` | 16. Discovery should have evidence levels | `architecture/discovery-model.md` | MOVE | DESIGNED |
| USP-028 | `Userscript Discovery Prototype.md` | 17. Use observations to update the search space | `architecture/search-space.md` | MOVE | DESIGNED |
| USP-029 | `Userscript Discovery Prototype.md` | 18. Termination | `concepts/discovery-loop.md` | MOVE | DESIGNED |
| USP-030 | `Userscript Discovery Prototype.md` | Exhaustive scan | `concepts/discovery-loop.md` | MOVE | DESIGNED |
| USP-031 | `Userscript Discovery Prototype.md` | Confidence-based scan | `concepts/discovery-loop.md` | MOVE | DESIGNED |
| USP-032 | `Userscript Discovery Prototype.md` | Time-bounded scan | `concepts/discovery-loop.md` | MOVE | DESIGNED |
| USP-033 | `Userscript Discovery Prototype.md` | Hybrid | `concepts/discovery-loop.md` | MOVE | DESIGNED |
| USP-034 | `Userscript Discovery Prototype.md` | 19. Coverage is a better metric than elapsed time | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| USP-035 | `Userscript Discovery Prototype.md` | 20. Cache knowledge between scans | `architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| USP-036 | `Userscript Discovery Prototype.md` | 21. Handle disappearing multiplexes | `architecture/resource-model.md` | MOVE | DESIGNED |
| USP-037 | `Userscript Discovery Prototype.md` | 22. The complete conceptual algorithm | `concepts/discovery-loop.md` | MOVE | DESIGNED |
| USP-038 | `Userscript Discovery Prototype.md` | 23. A useful formal name | `concepts/generic-discovery.md` | MOVE | DESIGNED |
| USP-039 | `Userscript Discovery Prototype.md` | *turn 8 you lead-in* | — | ARCHIVE | UNVERIFIED |
| USP-040 | `Userscript Discovery Prototype.md` | *turn 9 chatgpt lead-in* | `architecture/discovery-model.md` | MOVE | DESIGNED |
| USP-041 | `Userscript Discovery Prototype.md` | 24. Two-dimensional discovery | `architecture/discovery-model.md` | MOVE | DESIGNED |
| USP-042 | `Userscript Discovery Prototype.md` | 25. Candidate lifecycle | `architecture/candidate-model.md` | MOVE | DESIGNED |
| USP-043 | `Userscript Discovery Prototype.md` | 26. Discovery becomes a graph | `architecture/discovery-model.md` | MOVE | DESIGNED |
| USP-044 | `Userscript Discovery Prototype.md` | 27. This helps with incremental scanning | `architecture/search-space.md` | MOVE | DESIGNED |
| USP-045 | `Userscript Discovery Prototype.md` | 28. Parameter provenance | `architecture/provenance.md` | MOVE | DESIGNED |
| USP-046 | `Userscript Discovery Prototype.md` | 29. The scanner should produce an explanation | `architecture/provenance.md` | MOVE | DESIGNED |
| USP-047 | `Userscript Discovery Prototype.md` | 30. The final abstraction | `concepts/generic-discovery.md` | MOVE | DESIGNED |
| USP-048 | `Userscript Discovery Prototype.md` | *turn 10 you lead-in* | — | ARCHIVE | UNVERIFIED |
| USP-049 | `Userscript Discovery Prototype.md` | *turn 11 chatgpt lead-in* | `architecture/system-model.md` | MOVE | DESIGNED |
| USP-050 | `Userscript Discovery Prototype.md` | 31. Define the core objects | `architecture/system-model.md` | MOVE | DESIGNED |
| USP-051 | `Userscript Discovery Prototype.md` | Candidate | `architecture/candidate-model.md` | MOVE | DESIGNED |
| USP-052 | `Userscript Discovery Prototype.md` | Observation | `architecture/observation-model.md` | MOVE | DESIGNED |
| USP-053 | `Userscript Discovery Prototype.md` | LockResult | `acquisition/response-recognition.md` | MOVE | DESIGNED |
| USP-054 | `Userscript Discovery Prototype.md` | Discovery | `architecture/discovery-model.md` | MOVE | DESIGNED |
| USP-055 | `Userscript Discovery Prototype.md` | 32. Use capability-driven adapters | `architecture/provider-architecture.md` | MOVE | DESIGNED |
| USP-056 | `Userscript Discovery Prototype.md` | 33. Discovery strategies should also be pluggable | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| USP-057 | `Userscript Discovery Prototype.md` | 34. Don't confuse candidate identity with reception identity | `architecture/candidate-model.md` | MOVE | DESIGNED |
| USP-058 | `Userscript Discovery Prototype.md` | 35. Make deduplication hierarchical | `architecture/candidate-model.md` | MOVE | DESIGNED |
| USP-059 | `Userscript Discovery Prototype.md` | 36. Treat metadata as a candidate generator | `architecture/candidate-model.md` | MOVE | DESIGNED |
| USP-060 | `Userscript Discovery Prototype.md` | 37. Candidate provenance creates a discovery tree | `architecture/provenance.md` | MOVE | DESIGNED |
| USP-061 | `Userscript Discovery Prototype.md` | 38. Avoid infinite candidate generation | `architecture/search-space.md` | MOVE | DESIGNED |
| USP-062 | `Userscript Discovery Prototype.md` | 39. A practical scheduler | `architecture/scheduler.md` | MOVE | DESIGNED |
| USP-063 | `Userscript Discovery Prototype.md` | 40. The engine can now become event-driven | `architecture/system-model.md` | MOVE | DESIGNED |
| USP-064 | `Userscript Discovery Prototype.md` | 41. The resulting architecture | `architecture/overview.md` | MOVE | DESIGNED |
| USP-065 | `Userscript Discovery Prototype.md` | *turn 12 you lead-in* | `prototype/versions/01-v0.1.0.md` | MOVE | CURRENT |
| USP-066 | `Userscript Discovery Prototype.md` | *turn 13 chatgpt lead-in* | `prototype/versions/01-v0.1.0.md` | MOVE | CURRENT |
| USP-067 | `Userscript Discovery Prototype.md` | *turn 13 chatgpt lead-in* | `prototype/overview.md` | MOVE | CURRENT |
| USP-068 | `Userscript Discovery Prototype.md` | The DVB analogy | `research/dvb-blind-scan.md` | MOVE | DESIGNED |
| USP-069 | `Userscript Discovery Prototype.md` | *turn 14 you lead-in* | `prototype/versions/02-v0.2.0.md` | MOVE | CURRENT |
| USP-070 | `Userscript Discovery Prototype.md` | *turn 15 chatgpt lead-in* | `prototype/versions/02-v0.2.0.md` | MOVE | CURRENT |
| USP-071 | `Userscript Discovery Prototype.md` | What changed — 1. Concurrent claiming is now explicit | `architecture/concurrency.md` | MOVE | DESIGNED |
| USP-072 | `Userscript Discovery Prototype.md` | What changed — 2. HTML is no longer special | `providers/overview.md` | MOVE | DESIGNED |
| USP-073 | `Userscript Discovery Prototype.md` | What changed — 3. The actual scope is now explicit | `prototype/limitations.md` | MOVE | CURRENT |
| CAP-001 | `Continue Architecture Planning.md` | *turn 0 you lead-in* | `prototype/versions/00-v0.1.0-and-v0.2.0-paste.md` | DUPLICATE | UNVERIFIED |
| CAP-002 | `Continue Architecture Planning.md` | *turn 1 chatgpt lead-in* | `prototype/overview.md` | MOVE | CURRENT |
| CAP-003 | `Continue Architecture Planning.md` | *turn 2 you lead-in* | `prototype/versions/03-v0.3.0.md` | MOVE | CURRENT |
| CAP-004 | `Continue Architecture Planning.md` | *turn 3 chatgpt lead-in* | `prototype/versions/03-v0.3.0.md` | MOVE | CURRENT |
| CAP-005 | `Continue Architecture Planning.md` | What changed from v0.2.0 | `prototype/userscript.md` | MOVE | CURRENT |
| CAP-006 | `Continue Architecture Planning.md` | *turn 4 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-007 | `Continue Architecture Planning.md` | *turn 5 chatgpt lead-in* | `prototype/versions/04-v0.4.0-plan.md` | MOVE | FUTURE |
| CAP-008 | `Continue Architecture Planning.md` | The biggest v0.4 improvement | `prototype/versions/04-v0.4.0-plan.md` | MOVE | FUTURE |
| CAP-009 | `Continue Architecture Planning.md` | *turn 6 you lead-in* | `prototype/versions/05-v0.4.0.md` | MOVE | CURRENT |
| CAP-010 | `Continue Architecture Planning.md` | *turn 7 chatgpt lead-in* | `prototype/versions/05-v0.4.0.md` | MOVE | CURRENT |
| CAP-011 | `Continue Architecture Planning.md` | Notable v0.4.0 behavior | `prototype/userscript.md` | MOVE | CURRENT |
| CAP-012 | `Continue Architecture Planning.md` | *turn 8 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-013 | `Continue Architecture Planning.md` | *turn 9 chatgpt lead-in* | `prototype/versions/06-v0.5.0.md` | MOVE | CURRENT |
| CAP-014 | `Continue Architecture Planning.md` | *turn 9 chatgpt lead-in* | `prototype/userscript.md` | MOVE | CURRENT |
| CAP-015 | `Continue Architecture Planning.md` | *turn 10 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-016 | `Continue Architecture Planning.md` | *turn 11 chatgpt lead-in* | `prototype/versions/07-v0.4.0-second-iteration.md` | MOVE | CURRENT |
| CAP-017 | `Continue Architecture Planning.md` | What changed from v0.3.0 | `prototype/userscript.md` | MOVE | CURRENT |
| CAP-018 | `Continue Architecture Planning.md` | *turn 12 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-019 | `Continue Architecture Planning.md` | *turn 13 chatgpt lead-in* | `prototype/versions/08-v0.5.0-plan.md` | MOVE | FUTURE |
| CAP-020 | `Continue Architecture Planning.md` | *turn 14 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-021 | `Continue Architecture Planning.md` | *turn 15 chatgpt lead-in* | `prototype/versions/09-v0.5.0-second-iteration.md` | MOVE | CURRENT |
| CAP-022 | `Continue Architecture Planning.md` | v0.5 architecture | `prototype/userscript.md` | MOVE | CURRENT |
| CAP-023 | `Continue Architecture Planning.md` | *turn 16 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-024 | `Continue Architecture Planning.md` | *turn 17 chatgpt lead-in* | `prototype/versions/10-v0.6.0.md` | MOVE | CURRENT |
| CAP-025 | `Continue Architecture Planning.md` | What v0.6 changes architecturally | `prototype/userscript.md` | MOVE | CURRENT |
| CAP-026 | `Continue Architecture Planning.md` | *turn 18 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-027 | `Continue Architecture Planning.md` | *turn 19 chatgpt lead-in* | `prototype/versions/11-v0.5.0-third-iteration.md` | MOVE | CURRENT |
| CAP-028 | `Continue Architecture Planning.md` | What v0.5.0 changes architecturally | `prototype/userscript.md` | MOVE | CURRENT |
| CAP-029 | `Continue Architecture Planning.md` | *turn 20 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-030 | `Continue Architecture Planning.md` | *turn 21 chatgpt lead-in* | `prototype/versions/12-v0.6.0-second-iteration.md` | MOVE | CURRENT |
| CAP-031 | `Continue Architecture Planning.md` | v0.6.0's main architectural additions | `prototype/userscript.md` | MOVE | CURRENT |
| CAP-032 | `Continue Architecture Planning.md` | *turn 22 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-033 | `Continue Architecture Planning.md` | *turn 23 chatgpt lead-in* | `prototype/versions/13-v0.6.0-third-iteration.md` | MOVE | CURRENT |
| CAP-034 | `Continue Architecture Planning.md` | What changed in v0.6 | `prototype/userscript.md` | MOVE | CURRENT |
| CAP-035 | `Continue Architecture Planning.md` | *turn 24 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-036 | `Continue Architecture Planning.md` | v0.7.0 — Discovery Graph + Acquisition Planner | `architecture/discovery-model.md` | MOVE | DESIGNED |
| CAP-037 | `Continue Architecture Planning.md` | v0.7 objectives | `architecture/discovery-model.md` | MOVE | DESIGNED |
| CAP-038 | `Continue Architecture Planning.md` | Core contract | `architecture/discovery-model.md` | MOVE | DESIGNED |
| CAP-039 | `Continue Architecture Planning.md` | Important v0.7 distinction | `architecture/discovery-model.md` | MOVE | DESIGNED |
| CAP-040 | `Continue Architecture Planning.md` | v0.7 state machine | `architecture/discovery-model.md` | MOVE | DESIGNED |
| CAP-041 | `Continue Architecture Planning.md` | The deeper abstraction | `concepts/overview.md` | MOVE | DESIGNED |
| CAP-042 | `Continue Architecture Planning.md` | *turn 26 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-043 | `Continue Architecture Planning.md` | *turn 27 chatgpt lead-in* | `prototype/versions/14-v0.7.1.md` | MOVE | CURRENT |
| CAP-044 | `Continue Architecture Planning.md` | *turn 27 chatgpt lead-in* | `prototype/userscript.md` | MOVE | CURRENT |
| CAP-045 | `Continue Architecture Planning.md` | What v0.7.1 actually changes | `prototype/userscript.md` | MOVE | CURRENT |
| CAP-046 | `Continue Architecture Planning.md` | Before | `prototype/userscript.md` | MOVE | CURRENT |
| CAP-047 | `Continue Architecture Planning.md` | Now | `prototype/userscript.md` | MOVE | CURRENT |
| CAP-048 | `Continue Architecture Planning.md` | 2. The ledger becomes the scan's causal trace | `architecture/provenance.md` | MOVE | DESIGNED |
| CAP-049 | `Continue Architecture Planning.md` | 3. PerformanceObserver correction | `architecture/observation-model.md` | MOVE | DESIGNED |
| CAP-050 | `Continue Architecture Planning.md` | 4. Candidate state machine | `prototype/userscript.md` | MOVE | CURRENT |
| CAP-051 | `Continue Architecture Planning.md` | 5. The ledger is not merely logging | `architecture/provenance.md` | MOVE | DESIGNED |
| CAP-052 | `Continue Architecture Planning.md` | 6. One remaining architectural limitation | `prototype/limitations.md` | MOVE | OPEN |
| CAP-053 | `Continue Architecture Planning.md` | 7. Architecture after v0.7.1 | `architecture/system-model.md` | MOVE | DESIGNED |
| CAP-054 | `Continue Architecture Planning.md` | Next boundary: v0.8 | `roadmap/future-work.md` | MOVE | FUTURE |
| CAP-055 | `Continue Architecture Planning.md` | *turn 28 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-056 | `Continue Architecture Planning.md` | v0.8 — Capability-Aware Acquisition Runtime | `architecture/capability-model.md` | MOVE | DESIGNED |
| CAP-057 | `Continue Architecture Planning.md` | 1. The three graphs | `architecture/capability-model.md` | MOVE | DESIGNED |
| CAP-058 | `Continue Architecture Planning.md` | Discovery graph | `architecture/capability-model.md` | MOVE | DESIGNED |
| CAP-059 | `Continue Architecture Planning.md` | Acquisition graph | `acquisition/acquisition-model.md` | MOVE | DESIGNED |
| CAP-060 | `Continue Architecture Planning.md` | Evidence graph | `architecture/capability-model.md` | MOVE | DESIGNED |
| CAP-061 | `Continue Architecture Planning.md` | 2. Capability is now a first-class object | `architecture/capability-model.md` | MOVE | DESIGNED |
| CAP-062 | `Continue Architecture Planning.md` | 3. Capability lattice | `architecture/capability-model.md` | MOVE | DESIGNED |
| CAP-063 | `Continue Architecture Planning.md` | 4. Capability contract | `architecture/capability-model.md` | MOVE | DESIGNED |
| CAP-064 | `Continue Architecture Planning.md` | 5. Candidate requirements | `architecture/capability-model.md` | MOVE | DESIGNED |
| CAP-065 | `Continue Architecture Planning.md` | 6. Acquisition planning becomes capability resolution | `acquisition/acquisition-model.md` | MOVE | DESIGNED |
| CAP-066 | `Continue Architecture Planning.md` | 7. Why this matters for generic discovery | `architecture/capability-model.md` | MOVE | DESIGNED |
| CAP-067 | `Continue Architecture Planning.md` | 8. AcquisitionPlan v0.8 | `acquisition/acquisition-model.md` | MOVE | DESIGNED |
| CAP-068 | `Continue Architecture Planning.md` | 9. Capability provenance | `architecture/capability-model.md` | MOVE | DESIGNED |
| CAP-069 | `Continue Architecture Planning.md` | 10. The four-level authorization model | `architecture/capability-model.md` | MOVE | DESIGNED |
| CAP-070 | `Continue Architecture Planning.md` | 11. New graph model | `architecture/capability-model.md` | MOVE | DESIGNED |
| CAP-071 | `Continue Architecture Planning.md` | 12. v0.8 ledger | `architecture/capability-model.md` | MOVE | DESIGNED |
| CAP-072 | `Continue Architecture Planning.md` | 13. Important architectural consequence | `architecture/capability-model.md` | MOVE | DESIGNED |
| CAP-073 | `Continue Architecture Planning.md` | 14. v0.8 scope boundary | `architecture/capability-model.md` | MOVE | DESIGNED |
| CAP-074 | `Continue Architecture Planning.md` | Implement | `architecture/capability-model.md` | MOVE | DESIGNED |
| CAP-075 | `Continue Architecture Planning.md` | Represent but deny | `architecture/capability-model.md` | MOVE | DESIGNED |
| CAP-076 | `Continue Architecture Planning.md` | 15. Updated system invariant | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-077 | `Continue Architecture Planning.md` | 16. The DVB analogy is now cleaner | `research/dvb-blind-scan.md` | MOVE | DESIGNED |
| CAP-078 | `Continue Architecture Planning.md` | 17. v0.8 → v0.9 | `roadmap/future-work.md` | MOVE | FUTURE |
| CAP-079 | `Continue Architecture Planning.md` | *turn 30 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-080 | `Continue Architecture Planning.md` | v0.9 — Acquisition Provider Architecture | `architecture/provider-architecture.md` | MOVE | DESIGNED |
| CAP-081 | `Continue Architecture Planning.md` | 0.9 architecture | `architecture/system-model.md` | MOVE | DESIGNED |
| CAP-082 | `Continue Architecture Planning.md` | The important separation | `acquisition/overview.md` | MOVE | DESIGNED |
| CAP-083 | `Continue Architecture Planning.md` | 1. AcquisitionProvider contract | `architecture/provider-architecture.md` | MOVE | DESIGNED |
| CAP-084 | `Continue Architecture Planning.md` | 2. Provider capabilities | `architecture/provider-architecture.md` | MOVE | DESIGNED |
| CAP-085 | `Continue Architecture Planning.md` | 3. Provider selection | `architecture/provider-architecture.md` | MOVE | DESIGNED |
| CAP-086 | `Continue Architecture Planning.md` | 4. GM-XHR becomes a component | `architecture/provider-architecture.md` | MOVE | DESIGNED |
| CAP-087 | `Continue Architecture Planning.md` | 5. Observation gets provider provenance | `architecture/observation-model.md` | MOVE | DESIGNED |
| CAP-088 | `Continue Architecture Planning.md` | 6. Provider failure ≠ acquisition denial | `architecture/provider-architecture.md` | MOVE | DESIGNED |
| CAP-089 | `Continue Architecture Planning.md` | Policy denial | `architecture/provider-architecture.md` | MOVE | DESIGNED |
| CAP-090 | `Continue Architecture Planning.md` | Provider failure | `architecture/provider-architecture.md` | MOVE | DESIGNED |
| CAP-091 | `Continue Architecture Planning.md` | 7. Provider selection itself becomes an event | `architecture/provider-architecture.md` | MOVE | DESIGNED |
| CAP-092 | `Continue Architecture Planning.md` | 8. A deeper consequence: acquisition becomes replaceable | `acquisition/overview.md` | MOVE | DESIGNED |
| CAP-093 | `Continue Architecture Planning.md` | Cache provider | `architecture/provider-architecture.md` | MOVE | DESIGNED |
| CAP-094 | `Continue Architecture Planning.md` | Replay provider | `architecture/provider-architecture.md` | MOVE | DESIGNED |
| CAP-095 | `Continue Architecture Planning.md` | 9. The engine is now approaching a general resource runtime | `architecture/provider-architecture.md` | MOVE | DESIGNED |
| CAP-096 | `Continue Architecture Planning.md` | 10. v0.9 invariants | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-097 | `Continue Architecture Planning.md` | I1 — Discovery independence | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-098 | `Continue Architecture Planning.md` | I2 — Policy independence | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-099 | `Continue Architecture Planning.md` | I3 — Capability soundness | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-100 | `Continue Architecture Planning.md` | I4 — Method safety | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-101 | `Continue Architecture Planning.md` | I5 — Provenance | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-102 | `Continue Architecture Planning.md` | I6 — Observation integrity | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-103 | `Continue Architecture Planning.md` | I7 — Replay distinction | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-104 | `Continue Architecture Planning.md` | 11. The next problem is now visible | `roadmap/future-work.md` | MOVE | FUTURE |
| CAP-105 | `Continue Architecture Planning.md` | *turn 32 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-106 | `Continue Architecture Planning.md` | v0.10 — Acquisition Runtime | `acquisition/runtime.md` | MOVE | DESIGNED |
| CAP-107 | `Continue Architecture Planning.md` | 1. The new architecture | `architecture/system-model.md` | MOVE | DESIGNED |
| CAP-108 | `Continue Architecture Planning.md` | 2. The key distinction: Scheduler vs Runtime | `acquisition/runtime.md` | MOVE | DESIGNED |
| CAP-109 | `Continue Architecture Planning.md` | Scheduler | `acquisition/runtime.md` | MOVE | DESIGNED |
| CAP-110 | `Continue Architecture Planning.md` | Runtime | `acquisition/runtime.md` | MOVE | DESIGNED |
| CAP-111 | `Continue Architecture Planning.md` | 3. AcquisitionRuntime contract | `acquisition/runtime.md` | MOVE | DESIGNED |
| CAP-112 | `Continue Architecture Planning.md` | 4. Admission control | `acquisition/runtime.md` | MOVE | DESIGNED |
| CAP-113 | `Continue Architecture Planning.md` | 5. Budget becomes a first-class object | `acquisition/runtime.md` | MOVE | DESIGNED |
| CAP-114 | `Continue Architecture Planning.md` | 6. Why reservation must precede execution | `acquisition/runtime.md` | MOVE | DESIGNED |
| CAP-115 | `Continue Architecture Planning.md` | 7. OriginController | `acquisition/runtime.md` | MOVE | DESIGNED |
| CAP-116 | `Continue Architecture Planning.md` | 8. Provider selection happens after admission prerequisites | `acquisition/runtime.md` | MOVE | DESIGNED |
| CAP-117 | `Continue Architecture Planning.md` | 9. Provider must not own runtime policy | `acquisition/runtime.md` | MOVE | DESIGNED |
| CAP-118 | `Continue Architecture Planning.md` | 10. Cancellation becomes explicit | `acquisition/runtime.md` | MOVE | DESIGNED |
| CAP-119 | `Continue Architecture Planning.md` | 11. Timeout belongs to Runtime | `acquisition/runtime.md` | MOVE | DESIGNED |
| CAP-120 | `Continue Architecture Planning.md` | 12. Retry belongs to Runtime | `acquisition/runtime.md` | MOVE | DESIGNED |
| CAP-121 | `Continue Architecture Planning.md` | 13. Plan vs Attempt | `acquisition/runtime.md` | MOVE | DESIGNED |
| CAP-122 | `Continue Architecture Planning.md` | 14. Runtime event model | `acquisition/runtime.md` | MOVE | DESIGNED |
| CAP-123 | `Continue Architecture Planning.md` | 15. Runtime state machine | `acquisition/runtime.md` | MOVE | DESIGNED |
| CAP-124 | `Continue Architecture Planning.md` | 16. The complete execution equation | `acquisition/runtime.md` | MOVE | DESIGNED |
| CAP-125 | `Continue Architecture Planning.md` | 17. The resulting architecture | `architecture/system-model.md` | MOVE | DESIGNED |
| CAP-126 | `Continue Architecture Planning.md` | What v0.10 accomplishes | `concepts/overview.md` | MOVE | DESIGNED |
| CAP-127 | `Continue Architecture Planning.md` | Next boundary: v0.11 | `roadmap/future-work.md` | MOVE | FUTURE |
| CAP-128 | `Continue Architecture Planning.md` | *turn 34 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-129 | `Continue Architecture Planning.md` | v0.11 — Response Recognition Runtime | `acquisition/response-recognition.md` | MOVE | DESIGNED |
| CAP-130 | `Continue Architecture Planning.md` | 1. v0.11 architecture | `architecture/system-model.md` | MOVE | DESIGNED |
| CAP-131 | `Continue Architecture Planning.md` | 2. RecognitionProvider contract | `acquisition/response-recognition.md` | MOVE | DESIGNED |
| CAP-132 | `Continue Architecture Planning.md` | 3. Recognition is not discovery | `acquisition/response-recognition.md` | MOVE | DESIGNED |
| CAP-133 | `Continue Architecture Planning.md` | 4. Response Router | `acquisition/response-recognition.md` | MOVE | DESIGNED |
| CAP-134 | `Continue Architecture Planning.md` | 5. Provider priority | `acquisition/response-recognition.md` | MOVE | DESIGNED |
| CAP-135 | `Continue Architecture Planning.md` | 6. Recognition confidence | `acquisition/response-recognition.md` | MOVE | DESIGNED |
| CAP-136 | `Continue Architecture Planning.md` | 7. Content-type is only one signal | `acquisition/response-recognition.md` | MOVE | DESIGNED |
| CAP-137 | `Continue Architecture Planning.md` | 8. Recognition evidence | `acquisition/response-recognition.md` | MOVE | DESIGNED |
| CAP-138 | `Continue Architecture Planning.md` | 9. Recognition result contract | `acquisition/response-recognition.md` | MOVE | DESIGNED |
| CAP-139 | `Continue Architecture Planning.md` | 10. Why providers should not enqueue candidates | `acquisition/response-recognition.md` | MOVE | DESIGNED |
| CAP-140 | `Continue Architecture Planning.md` | 11. Recognition Runtime | `acquisition/response-recognition.md` | MOVE | DESIGNED |
| CAP-141 | `Continue Architecture Planning.md` | 12. Recognition failure taxonomy | `validation/failure-taxonomy.md` | MOVE | DESIGNED |
| CAP-142 | `Continue Architecture Planning.md` | No recognizer | `acquisition/response-recognition.md` | MOVE | DESIGNED |
| CAP-143 | `Continue Architecture Planning.md` | Provider rejected | `acquisition/response-recognition.md` | MOVE | DESIGNED |
| CAP-144 | `Continue Architecture Planning.md` | Provider error | `acquisition/response-recognition.md` | MOVE | DESIGNED |
| CAP-145 | `Continue Architecture Planning.md` | Successful recognition, zero discoveries | `acquisition/response-recognition.md` | MOVE | DESIGNED |
| CAP-146 | `Continue Architecture Planning.md` | 13. v0.11 state progression | `acquisition/response-recognition.md` | MOVE | DESIGNED |
| CAP-147 | `Continue Architecture Planning.md` | 14. Multiple recognizers | `acquisition/response-recognition.md` | MOVE | DESIGNED |
| CAP-148 | `Continue Architecture Planning.md` | 15. Recognition graph | `acquisition/response-recognition.md` | MOVE | DESIGNED |
| CAP-149 | `Continue Architecture Planning.md` | 16. The graph is now explicitly causal | `acquisition/response-recognition.md` | MOVE | DESIGNED |
| CAP-150 | `Continue Architecture Planning.md` | 17. v0.11 event ledger | `acquisition/response-recognition.md` | MOVE | DESIGNED |
| CAP-151 | `Continue Architecture Planning.md` | 18. The emerging generic algorithm | `acquisition/response-recognition.md` | MOVE | DESIGNED |
| CAP-152 | `Continue Architecture Planning.md` | 19. The next major abstraction: Candidate Sources | `roadmap/future-work.md` | MOVE | FUTURE |
| CAP-153 | `Continue Architecture Planning.md` | *turn 36 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-154 | `Continue Architecture Planning.md` | v0.12 — Candidate Source Architecture | `providers/candidate-sources.md` | MOVE | DESIGNED |
| CAP-155 | `Continue Architecture Planning.md` | 1. Three independent provider planes | `providers/overview.md` | MOVE | DESIGNED |
| CAP-156 | `Continue Architecture Planning.md` | 2. CandidateSource contract | `providers/candidate-sources.md` | MOVE | DESIGNED |
| CAP-157 | `Continue Architecture Planning.md` | 3. CandidateSource is a search-space adapter | `providers/candidate-sources.md` | MOVE | DESIGNED |
| CAP-158 | `Continue Architecture Planning.md` | Web page | `providers/candidate-sources.md` | MOVE | DESIGNED |
| CAP-159 | `Continue Architecture Planning.md` | Network traffic | `providers/candidate-sources.md` | MOVE | DESIGNED |
| CAP-160 | `Continue Architecture Planning.md` | Sitemap | `providers/candidate-sources.md` | MOVE | DESIGNED |
| CAP-161 | `Continue Architecture Planning.md` | User seed | `providers/candidate-sources.md` | MOVE | DESIGNED |
| CAP-162 | `Continue Architecture Planning.md` | Document | `providers/candidate-sources.md` | MOVE | DESIGNED |
| CAP-163 | `Continue Architecture Planning.md` | 4. CandidateProposal | `providers/candidate-sources.md` | MOVE | DESIGNED |
| CAP-164 | `Continue Architecture Planning.md` | 5. Why proposals matter | `providers/candidate-sources.md` | MOVE | DESIGNED |
| CAP-165 | `Continue Architecture Planning.md` | 6. CandidateNormalizer | `providers/candidate-sources.md` | MOVE | DESIGNED |
| CAP-166 | `Continue Architecture Planning.md` | 7. Source Registry | `providers/candidate-sources.md` | MOVE | DESIGNED |
| CAP-167 | `Continue Architecture Planning.md` | 8. The HTML provider should evolve | `providers/overview.md` | MOVE | DESIGNED |
| CAP-168 | `Continue Architecture Planning.md` | 9. Evidence becomes an intermediate layer | `providers/candidate-sources.md` | MOVE | DESIGNED |
| CAP-169 | `Continue Architecture Planning.md` | 10. Discovery becomes evidence-driven | `providers/candidate-sources.md` | MOVE | DESIGNED |
| CAP-170 | `Continue Architecture Planning.md` | 11. CandidateSource context | `providers/candidate-sources.md` | MOVE | DESIGNED |
| CAP-171 | `Continue Architecture Planning.md` | 12. CandidateSource examples | `providers/candidate-sources.md` | MOVE | DESIGNED |
| CAP-172 | `Continue Architecture Planning.md` | HTML link source | `providers/candidate-sources.md` | MOVE | DESIGNED |
| CAP-173 | `Continue Architecture Planning.md` | 13. NetworkSource | `providers/candidate-sources.md` | MOVE | DESIGNED |
| CAP-174 | `Continue Architecture Planning.md` | 14. Search-space composition | `providers/candidate-sources.md` | MOVE | DESIGNED |
| CAP-175 | `Continue Architecture Planning.md` | 15. Candidate identity | `providers/candidate-sources.md` | MOVE | DESIGNED |
| CAP-176 | `Continue Architecture Planning.md` | 16. Discovery confidence aggregation | `providers/candidate-sources.md` | MOVE | DESIGNED |
| CAP-177 | `Continue Architecture Planning.md` | 17. v0.12 provenance graph | `providers/candidate-sources.md` | MOVE | DESIGNED |
| CAP-178 | `Continue Architecture Planning.md` | 18. v0.12 invariants | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-179 | `Continue Architecture Planning.md` | S1 — Source purity | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-180 | `Continue Architecture Planning.md` | S2 — Core ownership | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-181 | `Continue Architecture Planning.md` | S3 — Proposal semantics | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-182 | `Continue Architecture Planning.md` | S4 — Identity | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-183 | `Continue Architecture Planning.md` | S5 — Provenance | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-184 | `Continue Architecture Planning.md` | S6 — Representability | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-185 | `Continue Architecture Planning.md` | S7 — Observation independence | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-186 | `Continue Architecture Planning.md` | 19. The complete v0.12 architecture | `architecture/system-model.md` | MOVE | DESIGNED |
| CAP-187 | `Continue Architecture Planning.md` | 20. The deeper abstraction | `concepts/overview.md` | MOVE | DESIGNED |
| CAP-188 | `Continue Architecture Planning.md` | v0.13 — the next boundary | `roadmap/future-work.md` | MOVE | FUTURE |
| CAP-189 | `Continue Architecture Planning.md` | *turn 38 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-190 | `Continue Architecture Planning.md` | v0.13 — Discovery Controller | `architecture/discovery-model.md` | MOVE | DESIGNED |
| CAP-191 | `Continue Architecture Planning.md` | 1. The complete v0.13 architecture | `architecture/system-model.md` | MOVE | DESIGNED |
| CAP-192 | `Continue Architecture Planning.md` | 2. Two schedulers, not one | `architecture/scheduler.md` | MOVE | DESIGNED |
| CAP-193 | `Continue Architecture Planning.md` | 3. DiscoveryTask | `architecture/discovery-model.md` | MOVE | DESIGNED |
| CAP-194 | `Continue Architecture Planning.md` | 4. Why a task is necessary | `architecture/discovery-model.md` | MOVE | DESIGNED |
| CAP-195 | `Continue Architecture Planning.md` | 5. Source Policy | `architecture/discovery-model.md` | MOVE | DESIGNED |
| CAP-196 | `Continue Architecture Planning.md` | 6. Source budgets | `architecture/discovery-model.md` | MOVE | DESIGNED |
| CAP-197 | `Continue Architecture Planning.md` | 7. Proposal budget is different | `architecture/discovery-model.md` | MOVE | DESIGNED |
| CAP-198 | `Continue Architecture Planning.md` | 8. Incremental sources | `architecture/discovery-model.md` | MOVE | DESIGNED |
| CAP-199 | `Continue Architecture Planning.md` | 9. Source execution contract | `architecture/discovery-model.md` | MOVE | DESIGNED |
| CAP-200 | `Continue Architecture Planning.md` | 10. Source scheduling | `architecture/scheduler.md` | MOVE | DESIGNED |
| CAP-201 | `Continue Architecture Planning.md` | 11. Fairness | `architecture/scheduler.md` | MOVE | DESIGNED |
| CAP-202 | `Continue Architecture Planning.md` | 12. Candidate deduplication belongs after normalization | `architecture/candidate-model.md` | MOVE | DESIGNED |
| CAP-203 | `Continue Architecture Planning.md` | 13. Discovery provenance | `architecture/provenance.md` | MOVE | DESIGNED |
| CAP-204 | `Continue Architecture Planning.md` | 14. Candidate generation becomes transactional | `architecture/candidate-model.md` | MOVE | DESIGNED |
| CAP-205 | `Continue Architecture Planning.md` | 15. Concurrent source execution | `architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-206 | `Continue Architecture Planning.md` | 16. DiscoveryController | `architecture/discovery-model.md` | MOVE | DESIGNED |
| CAP-207 | `Continue Architecture Planning.md` | 17. Event ledger | `architecture/discovery-model.md` | MOVE | DESIGNED |
| CAP-208 | `Continue Architecture Planning.md` | 18. Discovery failure taxonomy | `validation/failure-taxonomy.md` | MOVE | DESIGNED |
| CAP-209 | `Continue Architecture Planning.md` | 19. The generic blind-scan analogy is now much stronger | `research/dvb-blind-scan.md` | MOVE | DESIGNED |
| CAP-210 | `Continue Architecture Planning.md` | 20. v0.13 invariants | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-211 | `Continue Architecture Planning.md` | D1 — Source isolation | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-212 | `Continue Architecture Planning.md` | D2 — Acquisition isolation | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-213 | `Continue Architecture Planning.md` | D3 — Normalization ownership | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-214 | `Continue Architecture Planning.md` | D4 — Bounded generation | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-215 | `Continue Architecture Planning.md` | D5 — Bounded recursion | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-216 | `Continue Architecture Planning.md` | D6 — Provenance preservation | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-217 | `Continue Architecture Planning.md` | D7 — Atomic task claiming | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-218 | `Continue Architecture Planning.md` | D8 — Convergence | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-219 | `Continue Architecture Planning.md` | D9 — Discovery/acquisition independence | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-220 | `Continue Architecture Planning.md` | 21. The architecture is now approaching a stable core | `architecture/system-model.md` | MOVE | DESIGNED |
| CAP-221 | `Continue Architecture Planning.md` | v0.14 — the next missing abstraction | `roadmap/future-work.md` | MOVE | FUTURE |
| CAP-222 | `Continue Architecture Planning.md` | *turn 40 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-223 | `Continue Architecture Planning.md` | v0.14 — DiscoveryDomain + ScanSession | `architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-224 | `Continue Architecture Planning.md` | 1. The conceptual split | `architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-225 | `Continue Architecture Planning.md` | Discovery Engine | `architecture/discovery-model.md` | MOVE | DESIGNED |
| CAP-226 | `Continue Architecture Planning.md` | DiscoveryDomain | `architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-227 | `Continue Architecture Planning.md` | ScanSession | `architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-228 | `Continue Architecture Planning.md` | 2. DVB analogy | `research/dvb-blind-scan.md` | MOVE | DESIGNED |
| CAP-229 | `Continue Architecture Planning.md` | 3. DiscoveryDomain | `architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-230 | `Continue Architecture Planning.md` | 4. Domain vs policy | `architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-231 | `Continue Architecture Planning.md` | 5. Domain membership | `architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-232 | `Continue Architecture Planning.md` | 6. Explicit seeds | `architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-233 | `Continue Architecture Planning.md` | 7. Seed ≠ Candidate | `architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-234 | `Continue Architecture Planning.md` | 8. Discovery frontier | `architecture/discovery-model.md` | MOVE | DESIGNED |
| CAP-235 | `Continue Architecture Planning.md` | 9. ScanSession | `architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-236 | `Continue Architecture Planning.md` | 10. Session lifecycle | `architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-237 | `Continue Architecture Planning.md` | 11. Termination becomes explicit | `architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-238 | `Continue Architecture Planning.md` | Frontier exhaustion | `architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-239 | `Continue Architecture Planning.md` | Candidate limit | `architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-240 | `Continue Architecture Planning.md` | Acquisition limit | `architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-241 | `Continue Architecture Planning.md` | Discovery-task limit | `architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-242 | `Continue Architecture Planning.md` | Proposal limit | `architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-243 | `Continue Architecture Planning.md` | Depth limit | `architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-244 | `Continue Architecture Planning.md` | Time limit | `architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-245 | `Continue Architecture Planning.md` | External stop | `architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-246 | `Continue Architecture Planning.md` | 12. Termination evaluator | `architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-247 | `Continue Architecture Planning.md` | 13. Limit reached ≠ successful completion | `architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-248 | `Continue Architecture Planning.md` | 14. The session snapshot | `architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-249 | `Continue Architecture Planning.md` | 15. Resumability | `architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-250 | `Continue Architecture Planning.md` | 16. Lease-based claims | `architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-251 | `Continue Architecture Planning.md` | 17. Session ownership | `architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-252 | `Continue Architecture Planning.md` | 18. Scan vs engine knowledge | `architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-253 | `Continue Architecture Planning.md` | 19. Domain snapshot vs mutable domain | `architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-254 | `Continue Architecture Planning.md` | 20. Domain identity | `architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-255 | `Continue Architecture Planning.md` | 21. Search frontier vs knowledge graph | `architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-256 | `Continue Architecture Planning.md` | 22. The complete v0.14 architecture | `architecture/system-model.md` | MOVE | DESIGNED |
| CAP-257 | `Continue Architecture Planning.md` | 23. Four distinct scopes | `architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-258 | `Continue Architecture Planning.md` | 24. Strong invariants | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-259 | `Continue Architecture Planning.md` | Domain invariant | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-260 | `Continue Architecture Planning.md` | Session invariant | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-261 | `Continue Architecture Planning.md` | Snapshot invariant | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-262 | `Continue Architecture Planning.md` | Frontier invariant | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-263 | `Continue Architecture Planning.md` | Termination invariant | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-264 | `Continue Architecture Planning.md` | Recovery invariant | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-265 | `Continue Architecture Planning.md` | Provenance invariant | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-266 | `Continue Architecture Planning.md` | Acquisition invariant | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-267 | `Continue Architecture Planning.md` | Discovery invariant | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-268 | `Continue Architecture Planning.md` | 25. Failure taxonomy | `validation/failure-taxonomy.md` | MOVE | DESIGNED |
| CAP-269 | `Continue Architecture Planning.md` | 26. What v0.14 changes conceptually | `architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-270 | `Continue Architecture Planning.md` | 27. The next abstraction | `roadmap/future-work.md` | MOVE | FUTURE |
| CAP-271 | `Continue Architecture Planning.md` | v0.15 — WorkItem + Frontier Runtime | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-272 | `Continue Architecture Planning.md` | *turn 42 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-273 | `Continue Architecture Planning.md` | v0.15 — WorkItem + Frontier Runtime | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-274 | `Continue Architecture Planning.md` | 1. The key distinction | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-275 | `Continue Architecture Planning.md` | 2. Why `WorkItem` exists | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-276 | `Continue Architecture Planning.md` | 3. WorkItem | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-277 | `Continue Architecture Planning.md` | 4. Work kinds | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-278 | `Continue Architecture Planning.md` | 5. Work payload | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-279 | `Continue Architecture Planning.md` | 6. Work lifecycle | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-280 | `Continue Architecture Planning.md` | 7. Claiming becomes a formal protocol | `architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-281 | `Continue Architecture Planning.md` | 8. Work lease | `architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-282 | `Continue Architecture Planning.md` | 9. Lease recovery | `architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-283 | `Continue Architecture Planning.md` | 10. Frontier Runtime | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-284 | `Continue Architecture Planning.md` | 11. WorkScheduler | `architecture/scheduler.md` | MOVE | DESIGNED |
| CAP-285 | `Continue Architecture Planning.md` | 12. Priority starvation | `architecture/scheduler.md` | MOVE | DESIGNED |
| CAP-286 | `Continue Architecture Planning.md` | 13. Priority aging | `architecture/scheduler.md` | MOVE | DESIGNED |
| CAP-287 | `Continue Architecture Planning.md` | 14. Discovery and acquisition fairness | `acquisition/acquisition-model.md` | MOVE | DESIGNED |
| CAP-288 | `Continue Architecture Planning.md` | 15. Why not one giant queue? | `architecture/work-and-frontier.md` | MOVE | OPEN |
| CAP-289 | `Continue Architecture Planning.md` | 16. Work dependencies | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-290 | `Continue Architecture Planning.md` | 17. But dependencies must not create hidden coupling | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-291 | `Continue Architecture Planning.md` | 18. Dependency states | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-292 | `Continue Architecture Planning.md` | 19. Work completion | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-293 | `Continue Architecture Planning.md` | 20. Work execution boundary | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-294 | `Continue Architecture Planning.md` | 21. Work Runtime | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-295 | `Continue Architecture Planning.md` | 22. Retry becomes generic | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-296 | `Continue Architecture Planning.md` | 23. Retry identity | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-297 | `Continue Architecture Planning.md` | 24. Cancellation | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-298 | `Continue Architecture Planning.md` | 25. Scan termination with WorkItems | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-299 | `Continue Architecture Planning.md` | 26. The three frontier states | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-300 | `Continue Architecture Planning.md` | 27. Scheduled work | `architecture/scheduler.md` | MOVE | DESIGNED |
| CAP-301 | `Continue Architecture Planning.md` | 28. Work state machine | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-302 | `Continue Architecture Planning.md` | 29. Domain → Session → Work | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-303 | `Continue Architecture Planning.md` | 30. What belongs where? | `architecture/work-and-frontier.md` | MOVE | OPEN |
| CAP-304 | `Continue Architecture Planning.md` | 31. The crucial invariant | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-305 | `Continue Architecture Planning.md` | 32. Discovery vs acquisition remains intact | `acquisition/acquisition-model.md` | MOVE | DESIGNED |
| CAP-306 | `Continue Architecture Planning.md` | 33. The resulting architecture | `architecture/system-model.md` | MOVE | DESIGNED |
| CAP-307 | `Continue Architecture Planning.md` | 34. v0.15 architectural result | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-308 | `Continue Architecture Planning.md` | *turn 44 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-309 | `Continue Architecture Planning.md` | v0.16 — EvidenceGraph + Provenance | `architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-310 | `Continue Architecture Planning.md` | 1. The new abstraction | `architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-311 | `Continue Architecture Planning.md` | 2. Observation ≠ Evidence ≠ Claim | `architecture/observation-model.md` | MOVE | DESIGNED |
| CAP-312 | `Continue Architecture Planning.md` | Observation | `architecture/observation-model.md` | MOVE | DESIGNED |
| CAP-313 | `Continue Architecture Planning.md` | Evidence | `architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-314 | `Continue Architecture Planning.md` | Claim | `architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-315 | `Continue Architecture Planning.md` | 3. Resource ≠ Claim | `architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-316 | `Continue Architecture Planning.md` | 4. EvidenceGraph | `architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-317 | `Continue Architecture Planning.md` | 5. Provenance | `architecture/provenance.md` | MOVE | DESIGNED |
| CAP-318 | `Continue Architecture Planning.md` | 6. Evidence object | `architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-319 | `Continue Architecture Planning.md` | 7. Locator | `architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-320 | `Continue Architecture Planning.md` | 8. Claim | `architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-321 | `Continue Architecture Planning.md` | 9. Claims should not be confused with truth | `architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-322 | `Continue Architecture Planning.md` | 10. Evidence strength | `architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-323 | `Continue Architecture Planning.md` | 11. Independent evidence | `architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-324 | `Continue Architecture Planning.md` | 12. Evidence independence | `architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-325 | `Continue Architecture Planning.md` | 13. Evidence graph edges | `architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-326 | `Continue Architecture Planning.md` | 14. Why graph edges matter | `architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-327 | `Continue Architecture Planning.md` | 15. Provenance graph | `architecture/provenance.md` | MOVE | DESIGNED |
| CAP-328 | `Continue Architecture Planning.md` | 16. Resource identity | `architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-329 | `Continue Architecture Planning.md` | 17. Resource fingerprint | `architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-330 | `Continue Architecture Planning.md` | 18. URL identity vs content identity | `architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-331 | `Continue Architecture Planning.md` | 19. Revision detection | `architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-332 | `Continue Architecture Planning.md` | 20. Observation immutability | `architecture/observation-model.md` | MOVE | DESIGNED |
| CAP-333 | `Continue Architecture Planning.md` | 21. Evidence immutability | `architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-334 | `Continue Architecture Planning.md` | 22. Extraction method becomes first-class | `architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-335 | `Continue Architecture Planning.md` | 23. Verification | `validation/verification.md` | MOVE | DESIGNED |
| CAP-336 | `Continue Architecture Planning.md` | 24. Evidence lifecycle | `architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-337 | `Continue Architecture Planning.md` | 25. Evidence states | `architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-338 | `Continue Architecture Planning.md` | 26. Claims can conflict | `architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-339 | `Continue Architecture Planning.md` | 27. Evidence resolution | `architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-340 | `Continue Architecture Planning.md` | 28. Discovery confidence changes meaning | `architecture/discovery-model.md` | MOVE | DESIGNED |
| CAP-341 | `Continue Architecture Planning.md` | 29. Candidate provenance | `architecture/provenance.md` | MOVE | DESIGNED |
| CAP-342 | `Continue Architecture Planning.md` | 30. The evidence ledger | `architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-343 | `Continue Architecture Planning.md` | 31. Two complementary graphs | `architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-344 | `Continue Architecture Planning.md` | 32. Example end-to-end trace | `architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-345 | `Continue Architecture Planning.md` | 33. v0.16 architecture | `architecture/system-model.md` | MOVE | DESIGNED |
| CAP-346 | `Continue Architecture Planning.md` | 34. New invariants | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-347 | `Continue Architecture Planning.md` | Evidence provenance | `architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-348 | `Continue Architecture Planning.md` | Claim support | `architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-349 | `Continue Architecture Planning.md` | Historical integrity | `architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-350 | `Continue Architecture Planning.md` | Extraction integrity | `architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-351 | `Continue Architecture Planning.md` | Resource identity | `architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-352 | `Continue Architecture Planning.md` | Content identity | `architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-353 | `Continue Architecture Planning.md` | Conflict preservation | `architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-354 | `Continue Architecture Planning.md` | Provenance preservation | `architecture/provenance.md` | MOVE | DESIGNED |
| CAP-355 | `Continue Architecture Planning.md` | Session provenance | `architecture/provenance.md` | MOVE | DESIGNED |
| CAP-356 | `Continue Architecture Planning.md` | 35. Failure taxonomy | `validation/failure-taxonomy.md` | MOVE | DESIGNED |
| CAP-357 | `Continue Architecture Planning.md` | 36. The deeper architectural transition | `roadmap/future-work.md` | MOVE | FUTURE |
| CAP-358 | `Continue Architecture Planning.md` | 37. What is still missing | `roadmap/future-work.md` | MOVE | FUTURE |
| CAP-359 | `Continue Architecture Planning.md` | Search space | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-360 | `Continue Architecture Planning.md` | Execution | `architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-361 | `Continue Architecture Planning.md` | Work | `architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-362 | `Continue Architecture Planning.md` | Acquisition | `acquisition/acquisition-model.md` | MOVE | DESIGNED |
| CAP-363 | `Continue Architecture Planning.md` | Recognition | `acquisition/response-recognition.md` | MOVE | DESIGNED |
| CAP-364 | `Continue Architecture Planning.md` | Discovery | `architecture/discovery-model.md` | MOVE | DESIGNED |
| CAP-365 | `Continue Architecture Planning.md` | Evidence | `architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-366 | `Continue Architecture Planning.md` | History | `architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-367 | `Continue Architecture Planning.md` | v0.17 — ResourceGraph + Identity Resolution | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-368 | `Continue Architecture Planning.md` | *turn 46 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-369 | `Continue Architecture Planning.md` | v0.17 — ResourceGraph + Identity Resolution | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-370 | `Continue Architecture Planning.md` | 1. The core problem | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-371 | `Continue Architecture Planning.md` | 2. Resource identity must become graph-based | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-372 | `Continue Architecture Planning.md` | 3. Candidate vs Resource vs Locator | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-373 | `Continue Architecture Planning.md` | Candidate | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-374 | `Continue Architecture Planning.md` | Locator | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-375 | `Continue Architecture Planning.md` | Resource | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-376 | `Continue Architecture Planning.md` | 4. Why not simply canonicalize everything? | `architecture/resource-model.md` | MOVE | OPEN |
| CAP-377 | `Continue Architecture Planning.md` | 5. Locator | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-378 | `Continue Architecture Planning.md` | 6. Resource | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-379 | `Continue Architecture Planning.md` | 7. Resource relationships | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-380 | `Continue Architecture Planning.md` | 8. Redirects | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-381 | `Continue Architecture Planning.md` | 9. Redirect chain | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-382 | `Continue Architecture Planning.md` | 10. Content fingerprints | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-383 | `Continue Architecture Planning.md` | 11. Same content does not prove same resource | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-384 | `Continue Architecture Planning.md` | 12. Representation identity | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-385 | `Continue Architecture Planning.md` | 13. Identity Evidence | `architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-386 | `Continue Architecture Planning.md` | 14. IdentityResolver | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-387 | `Continue Architecture Planning.md` | 15. Identity confidence should be relational | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-388 | `Continue Architecture Planning.md` | 16. Identity classes | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-389 | `Continue Architecture Planning.md` | 17. No destructive merges | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-390 | `Continue Architecture Planning.md` | 18. ResourceGraph | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-391 | `Continue Architecture Planning.md` | 19. Graph edge contract | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-392 | `Continue Architecture Planning.md` | 20. Identity resolution pipeline | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-393 | `Continue Architecture Planning.md` | 21. Canonical URL is still important | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-394 | `Continue Architecture Planning.md` | 22. Canonicalization provenance | `architecture/provenance.md` | MOVE | DESIGNED |
| CAP-395 | `Continue Architecture Planning.md` | 23. Identity resolution must be monotonic where possible | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-396 | `Continue Architecture Planning.md` | 24. Resource revisions | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-397 | `Continue Architecture Planning.md` | 25. Revision object | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-398 | `Continue Architecture Planning.md` | 26. ResourceGraph vs KnowledgeBase | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-399 | `Continue Architecture Planning.md` | 27. Querying the graph | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-400 | `Continue Architecture Planning.md` | What URLs identify this resource? | `architecture/resource-model.md` | MOVE | OPEN |
| CAP-401 | `Continue Architecture Planning.md` | Where was it discovered? | `architecture/resource-model.md` | MOVE | OPEN |
| CAP-402 | `Continue Architecture Planning.md` | What URLs redirect to it? | `architecture/resource-model.md` | MOVE | OPEN |
| CAP-403 | `Continue Architecture Planning.md` | Which URLs have identical observed bytes? | `architecture/resource-model.md` | MOVE | OPEN |
| CAP-404 | `Continue Architecture Planning.md` | Has this resource changed? | `architecture/resource-model.md` | MOVE | OPEN |
| CAP-405 | `Continue Architecture Planning.md` | Why do we believe two URLs are related? | `architecture/resource-model.md` | MOVE | OPEN |
| CAP-406 | `Continue Architecture Planning.md` | 28. Resource graph example | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-407 | `Continue Architecture Planning.md` | 29. Failure taxonomy | `validation/failure-taxonomy.md` | MOVE | DESIGNED |
| CAP-408 | `Continue Architecture Planning.md` | 30. Core invariants | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-409 | `Continue Architecture Planning.md` | Locator preservation | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-410 | `Continue Architecture Planning.md` | No destructive merge | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-411 | `Continue Architecture Planning.md` | Fingerprint independence | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-412 | `Continue Architecture Planning.md` | Redirect independence | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-413 | `Continue Architecture Planning.md` | Evidence-backed identity | `architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-414 | `Continue Architecture Planning.md` | Revision preservation | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-415 | `Continue Architecture Planning.md` | Canonicalization transparency | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-416 | `Continue Architecture Planning.md` | 31. The new architecture | `architecture/system-model.md` | MOVE | DESIGNED |
| CAP-417 | `Continue Architecture Planning.md` | 32. The deeper model | `concepts/overview.md` | MOVE | DESIGNED |
| CAP-418 | `Continue Architecture Planning.md` | 33. The important transition | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-419 | `Continue Architecture Planning.md` | 34. Next missing abstraction | `roadmap/future-work.md` | MOVE | FUTURE |
| CAP-420 | `Continue Architecture Planning.md` | v0.18 — Resource Type System + Semantic Classification | `architecture/classification.md` | MOVE | DESIGNED |
| CAP-421 | `Continue Architecture Planning.md` | *turn 48 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-422 | `Continue Architecture Planning.md` | v0.18 — Resource Type System + Semantic Classification | `architecture/classification.md` | MOVE | DESIGNED |
| CAP-423 | `Continue Architecture Planning.md` | 18.1 The Type Problem | `architecture/classification.md` | MOVE | DESIGNED |
| CAP-424 | `Continue Architecture Planning.md` | 18.2 Four Orthogonal Type Dimensions | `architecture/classification.md` | MOVE | DESIGNED |
| CAP-425 | `Continue Architecture Planning.md` | 18.3 ResourceType | `architecture/classification.md` | MOVE | DESIGNED |
| CAP-426 | `Continue Architecture Planning.md` | 18.4 Classification Assertion | `architecture/classification.md` | MOVE | DESIGNED |
| CAP-427 | `Continue Architecture Planning.md` | 18.5 Type Evidence | `architecture/classification.md` | MOVE | DESIGNED |
| CAP-428 | `Continue Architecture Planning.md` | 18.6 Evidence Strength Must Be Axis-Specific | `architecture/classification.md` | MOVE | DESIGNED |
| CAP-429 | `Continue Architecture Planning.md` | 18.7 Classification Pipeline | `architecture/classification.md` | MOVE | DESIGNED |
| CAP-430 | `Continue Architecture Planning.md` | 18.8 Recognition vs Classification | `architecture/classification.md` | MOVE | DESIGNED |
| CAP-431 | `Continue Architecture Planning.md` | Recognition | `architecture/classification.md` | MOVE | DESIGNED |
| CAP-432 | `Continue Architecture Planning.md` | Classification | `architecture/classification.md` | MOVE | DESIGNED |
| CAP-433 | `Continue Architecture Planning.md` | 18.9 Classification Runtime | `architecture/classification.md` | MOVE | DESIGNED |
| CAP-434 | `Continue Architecture Planning.md` | 18.10 Example Classifiers | `architecture/classification.md` | MOVE | DESIGNED |
| CAP-435 | `Continue Architecture Planning.md` | 18.11 Hierarchical Classification | `architecture/classification.md` | MOVE | DESIGNED |
| CAP-436 | `Continue Architecture Planning.md` | 18.12 Do Not Use One Global Confidence Score | `architecture/classification.md` | MOVE | DESIGNED |
| CAP-437 | `Continue Architecture Planning.md` | 18.13 Classification Is Versioned | `architecture/classification.md` | MOVE | DESIGNED |
| CAP-438 | `Continue Architecture Planning.md` | 18.14 Contradictory Classification | `architecture/classification.md` | MOVE | DESIGNED |
| CAP-439 | `Continue Architecture Planning.md` | 18.15 Classification Graph | `architecture/classification.md` | MOVE | DESIGNED |
| CAP-440 | `Continue Architecture Planning.md` | 18.16 Resource Model After v0.18 | `architecture/classification.md` | MOVE | DESIGNED |
| CAP-441 | `Continue Architecture Planning.md` | 18.17 Resource Type Registry | `architecture/classification.md` | MOVE | DESIGNED |
| CAP-442 | `Continue Architecture Planning.md` | 18.18 Classification Must Not Become Acquisition Policy | `acquisition/acquisition-model.md` | MOVE | DESIGNED |
| CAP-443 | `Continue Architecture Planning.md` | 18.19 Classification → Strategy | `architecture/classification.md` | MOVE | DESIGNED |
| CAP-444 | `Continue Architecture Planning.md` | 18.20 Classification Work as WorkItem | `architecture/classification.md` | MOVE | DESIGNED |
| CAP-445 | `Continue Architecture Planning.md` | 18.21 End-to-End Architecture | `architecture/system-model.md` | MOVE | DESIGNED |
| CAP-446 | `Continue Architecture Planning.md` | 18.22 Failure Taxonomy | `validation/failure-taxonomy.md` | MOVE | DESIGNED |
| CAP-447 | `Continue Architecture Planning.md` | 18.23 Core Invariants | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-448 | `Continue Architecture Planning.md` | Invariant 1 — Type is not identity | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-449 | `Continue Architecture Planning.md` | Invariant 2 — URL does not determine semantic type | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-450 | `Continue Architecture Planning.md` | Invariant 3 — Technical recognition does not determine semantic role | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-451 | `Continue Architecture Planning.md` | Invariant 4 — Classification requires evidence | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-452 | `Continue Architecture Planning.md` | Invariant 5 — Classification does not imply authorization | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-453 | `Continue Architecture Planning.md` | Invariant 6 — Historical classification is immutable | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-454 | `Continue Architecture Planning.md` | Invariant 7 — Contradiction is preserved | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-455 | `Continue Architecture Planning.md` | Invariant 8 — Type axes remain independent | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-456 | `Continue Architecture Planning.md` | 18.24 The Larger Concept | `concepts/overview.md` | MOVE | DESIGNED |
| CAP-457 | `Continue Architecture Planning.md` | v0.19 — Resource Representation & Revision Model | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-458 | `Continue Architecture Planning.md` | *turn 50 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-459 | `Continue Architecture Planning.md` | v0.19 — Resource Representation + Artifact + Revision Model | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-460 | `Continue Architecture Planning.md` | 19.1 The Core Distinction | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-461 | `Continue Architecture Planning.md` | Resource | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-462 | `Continue Architecture Planning.md` | Representation | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-463 | `Continue Architecture Planning.md` | Artifact | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-464 | `Continue Architecture Planning.md` | Observation | `architecture/observation-model.md` | MOVE | DESIGNED |
| CAP-465 | `Continue Architecture Planning.md` | 19.2 Why Resource → Artifact Is Wrong | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-466 | `Continue Architecture Planning.md` | 19.3 New Data Model | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-467 | `Continue Architecture Planning.md` | 19.4 The Complete Identity Chain | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-468 | `Continue Architecture Planning.md` | 19.5 Representation Is Not Just MIME | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-469 | `Continue Architecture Planning.md` | 19.6 Representation Relations | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-470 | `Continue Architecture Planning.md` | 19.7 Artifact Identity | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-471 | `Continue Architecture Planning.md` | 19.8 Content Equivalence | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-472 | `Continue Architecture Planning.md` | 19.9 Revision Detection | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-473 | `Continue Architecture Planning.md` | 19.10 Revision Detection Is Not Always Proof of Semantic Revision | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-474 | `Continue Architecture Planning.md` | 19.11 Revision Evidence | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-475 | `Continue Architecture Planning.md` | 19.12 HTTP Validators Become Evidence | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-476 | `Continue Architecture Planning.md` | 19.13 Conditional Acquisition | `acquisition/acquisition-model.md` | MOVE | DESIGNED |
| CAP-477 | `Continue Architecture Planning.md` | 19.14 Observation Becomes the Historical Bridge | `architecture/observation-model.md` | MOVE | DESIGNED |
| CAP-478 | `Continue Architecture Planning.md` | 19.15 Resource State vs Artifact State | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-479 | `Continue Architecture Planning.md` | Resource state | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-480 | `Continue Architecture Planning.md` | Artifact state | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-481 | `Continue Architecture Planning.md` | Observation state | `architecture/observation-model.md` | MOVE | DESIGNED |
| CAP-482 | `Continue Architecture Planning.md` | 19.16 ResourceGraph v0.19 | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-483 | `Continue Architecture Planning.md` | 19.17 ResourceGraph API | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-484 | `Continue Architecture Planning.md` | 19.18 Artifact Deduplication | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-485 | `Continue Architecture Planning.md` | Locator deduplication | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-486 | `Continue Architecture Planning.md` | Artifact deduplication | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-487 | `Continue Architecture Planning.md` | 19.19 Content-Addressed Storage | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-488 | `Continue Architecture Planning.md` | 19.20 Verification Levels | `validation/verification.md` | MOVE | DESIGNED |
| CAP-489 | `Continue Architecture Planning.md` | 19.21 Independent Confirmation | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-490 | `Continue Architecture Planning.md` | 19.22 Resource Confidence | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-491 | `Continue Architecture Planning.md` | 19.23 Example | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-492 | `Continue Architecture Planning.md` | Step 1 — Locator | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-493 | `Continue Architecture Planning.md` | Step 2 — Resource | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-494 | `Continue Architecture Planning.md` | Step 3 — Observation | `architecture/observation-model.md` | MOVE | DESIGNED |
| CAP-495 | `Continue Architecture Planning.md` | Step 4 — Artifact | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-496 | `Continue Architecture Planning.md` | Step 5 — Representation | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-497 | `Continue Architecture Planning.md` | Step 6 — Classification | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-498 | `Continue Architecture Planning.md` | Step 7 — Revision | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-499 | `Continue Architecture Planning.md` | 19.24 A More Precise End-to-End Pipeline | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-500 | `Continue Architecture Planning.md` | 19.25 New Invariants | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-501 | `Continue Architecture Planning.md` | Artifact invariant | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-502 | `Continue Architecture Planning.md` | Resource invariant | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-503 | `Continue Architecture Planning.md` | Representation invariant | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-504 | `Continue Architecture Planning.md` | Revision invariant | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-505 | `Continue Architecture Planning.md` | Observation invariant | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-506 | `Continue Architecture Planning.md` | Deduplication invariant | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-507 | `Continue Architecture Planning.md` | Change invariant | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-508 | `Continue Architecture Planning.md` | Classification invariant | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-509 | `Continue Architecture Planning.md` | 19.26 Failure Modes | `validation/failure-taxonomy.md` | MOVE | DESIGNED |
| CAP-510 | `Continue Architecture Planning.md` | 19.27 What v0.19 Gives Us | `architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-511 | `Continue Architecture Planning.md` | Next boundary: v0.20 — Search-Space Partitioning + Discovery Strategies | `roadmap/future-work.md` | MOVE | FUTURE |
| CAP-512 | `Continue Architecture Planning.md` | *turn 52 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-513 | `Continue Architecture Planning.md` | v0.20 — Search-Space Partitioning + Discovery Strategies | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-514 | `Continue Architecture Planning.md` | 20.1 The Search Space | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-515 | `Continue Architecture Planning.md` | 20.2 What Is a Partition? | `architecture/search-space.md` | MOVE | OPEN |
| CAP-516 | `Continue Architecture Planning.md` | 20.3 Partition ≠ Candidate | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-517 | `Continue Architecture Planning.md` | 20.4 Partition Object | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-518 | `Continue Architecture Planning.md` | 20.5 Partition State | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-519 | `Continue Architecture Planning.md` | Saturated | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-520 | `Continue Architecture Planning.md` | Exhausted | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-521 | `Continue Architecture Planning.md` | 20.6 Search Coverage | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-522 | `Continue Architecture Planning.md` | 20.7 Strategy Contract | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-523 | `Continue Architecture Planning.md` | 20.8 Strategy vs Candidate Source | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-524 | `Continue Architecture Planning.md` | 20.9 Strategy Types | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-525 | `Continue Architecture Planning.md` | Seed Expansion | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-526 | `Continue Architecture Planning.md` | Repository Expansion | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-527 | `Continue Architecture Planning.md` | Sitemap Expansion | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-528 | `Continue Architecture Planning.md` | API Schema Expansion | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-529 | `Continue Architecture Planning.md` | Document-Family Expansion | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-530 | `Continue Architecture Planning.md` | 20.10 Blind-Scan Analogy | `research/dvb-blind-scan.md` | MOVE | DESIGNED |
| CAP-531 | `Continue Architecture Planning.md` | 20.11 Probe | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-532 | `Continue Architecture Planning.md` | 20.12 Exploration Plan | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-533 | `Continue Architecture Planning.md` | 20.13 Exploration Must Remain Budgeted | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-534 | `Continue Architecture Planning.md` | 20.14 Adaptive Partition Priority | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-535 | `Continue Architecture Planning.md` | 20.15 Exploration vs Exploitation | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-536 | `Continue Architecture Planning.md` | 20.16 Aging | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-537 | `Continue Architecture Planning.md` | 20.17 Partition Splitting | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-538 | `Continue Architecture Planning.md` | 20.18 Partition Merge | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-539 | `Continue Architecture Planning.md` | 20.19 Partition Graph | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-540 | `Continue Architecture Planning.md` | 20.20 SearchSpace | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-541 | `Continue Architecture Planning.md` | 20.21 Search-Space Controller | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-542 | `Continue Architecture Planning.md` | 20.22 Three-Level Control Plane | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-543 | `Continue Architecture Planning.md` | 20.23 Candidate Sources Remain Low-Level | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-544 | `Continue Architecture Planning.md` | 20.24 Termination Becomes More Sophisticated | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-545 | `Continue Architecture Planning.md` | 20.25 Saturation | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-546 | `Continue Architecture Planning.md` | 20.26 Partition Statistics | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-547 | `Continue Architecture Planning.md` | 20.27 Discovery Efficiency | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-548 | `Continue Architecture Planning.md` | 20.28 Failure Modes | `validation/failure-taxonomy.md` | MOVE | DESIGNED |
| CAP-549 | `Continue Architecture Planning.md` | 20.29 Core Invariants | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-550 | `Continue Architecture Planning.md` | Search-space invariant | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-551 | `Continue Architecture Planning.md` | Strategy invariant | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-552 | `Continue Architecture Planning.md` | Acquisition invariant | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-553 | `Continue Architecture Planning.md` | Partition invariant | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-554 | `Continue Architecture Planning.md` | Coverage invariant | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-555 | `Continue Architecture Planning.md` | Discovery invariant | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-556 | `Continue Architecture Planning.md` | 20.30 The Architecture After v0.20 | `architecture/system-model.md` | MOVE | DESIGNED |
| CAP-557 | `Continue Architecture Planning.md` | 20.31 The DVB Analogy Is Now Structural | `research/dvb-blind-scan.md` | MOVE | DESIGNED |
| CAP-558 | `Continue Architecture Planning.md` | v0.21 — Discovery Strategy Learning / Adaptive Search | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-559 | `Continue Architecture Planning.md` | *turn 54 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-560 | `Continue Architecture Planning.md` | v0.21 — Adaptive Discovery Strategy | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-561 | `Continue Architecture Planning.md` | 21.1 The Adaptive Loop | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-562 | `Continue Architecture Planning.md` | 21.2 Strategy Performance Record | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-563 | `Continue Architecture Planning.md` | 21.3 Yield Metrics | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-564 | `Continue Architecture Planning.md` | 21.4 Strategy Score | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-565 | `Continue Architecture Planning.md` | 21.5 Cold Start Problem | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-566 | `Continue Architecture Planning.md` | 21.6 Exploration Quota | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-567 | `Continue Architecture Planning.md` | 21.7 Strategy Selection Must Be Constrained | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-568 | `Continue Architecture Planning.md` | 21.8 Strategy Eligibility | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-569 | `Continue Architecture Planning.md` | 21.9 Temporary vs Permanent Failure | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-570 | `Continue Architecture Planning.md` | 21.10 Strategy Outcome | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-571 | `Continue Architecture Planning.md` | 21.11 Strategy Outcome ≠ Strategy Truth | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-572 | `Continue Architecture Planning.md` | 21.12 Novelty | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-573 | `Continue Architecture Planning.md` | 21.13 Frontier Expansion Value | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-574 | `Continue Architecture Planning.md` | 21.14 Frontier Expansion Metric | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-575 | `Continue Architecture Planning.md` | 21.15 Strategy Memory | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-576 | `Continue Architecture Planning.md` | 21.16 Hierarchical Priors | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-577 | `Continue Architecture Planning.md` | 21.17 Discovery Strategy Ledger | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-578 | `Continue Architecture Planning.md` | 21.18 Deterministic Replay | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-579 | `Continue Architecture Planning.md` | 21.19 Random Exploration | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-580 | `Continue Architecture Planning.md` | 21.20 Learning Must Not Modify Safety Boundaries | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-581 | `Continue Architecture Planning.md` | 21.21 Adaptive Discovery Controller | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-582 | `Continue Architecture Planning.md` | 21.22 Tie-Breaking Must Be Deterministic | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-583 | `Continue Architecture Planning.md` | 21.23 Performance Decay | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-584 | `Continue Architecture Planning.md` | 21.24 Strategy Adaptation and Scan Sessions | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-585 | `Continue Architecture Planning.md` | 21.25 Search Strategy as a First-Class Graph Node | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-586 | `Continue Architecture Planning.md` | 21.26 Search Decision Graph | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-587 | `Continue Architecture Planning.md` | 21.27 Two Kinds of Provenance | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-588 | `Continue Architecture Planning.md` | 21.28 Failure Taxonomy | `validation/failure-taxonomy.md` | MOVE | DESIGNED |
| CAP-589 | `Continue Architecture Planning.md` | 21.29 Invariants | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-590 | `Continue Architecture Planning.md` | Safety invariant | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-591 | `Continue Architecture Planning.md` | Capability invariant | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-592 | `Continue Architecture Planning.md` | Domain invariant | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-593 | `Continue Architecture Planning.md` | Exploration invariant | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-594 | `Continue Architecture Planning.md` | Historical invariant | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-595 | `Continue Architecture Planning.md` | Replay invariant | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-596 | `Continue Architecture Planning.md` | Provenance invariant | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-597 | `Continue Architecture Planning.md` | 21.30 Architecture After v0.21 | `architecture/system-model.md` | MOVE | DESIGNED |
| CAP-598 | `Continue Architecture Planning.md` | 21.31 The Important Conceptual Shift | `concepts/overview.md` | MOVE | DESIGNED |
| CAP-599 | `Continue Architecture Planning.md` | v0.22 — Discovery Completeness + Coverage Claims | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-600 | `Continue Architecture Planning.md` | *turn 56 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-601 | `Continue Architecture Planning.md` | v0.22 — Discovery Completeness + Coverage Claims | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-602 | `Continue Architecture Planning.md` | 22.1 The problem | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-603 | `Continue Architecture Planning.md` | 22.2 Search-space state model | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-604 | `Continue Architecture Planning.md` | 22.3 Coverage is a measurement | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-605 | `Continue Architecture Planning.md` | 22.4 Coverage dimensions | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-606 | `Continue Architecture Planning.md` | 22.5 CoverageRecord | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-607 | `Continue Architecture Planning.md` | 22.6 Coverage state | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-608 | `Continue Architecture Planning.md` | 22.7 CoverageClaim | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-609 | `Continue Architecture Planning.md` | 22.8 Completeness is a stronger assertion | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-610 | `Continue Architecture Planning.md` | 22.9 The finite-enumerator case | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-611 | `Continue Architecture Planning.md` | 22.10 Enumeration contract | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-612 | `Continue Architecture Planning.md` | 22.11 Negative evidence | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-613 | `Continue Architecture Planning.md` | 22.12 Absence reasoning hierarchy | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-614 | `Continue Architecture Planning.md` | 22.13 “Not found” becomes a first-class result | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-615 | `Continue Architecture Planning.md` | 22.14 Coverage cannot necessarily be monotonically interpreted | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-616 | `Continue Architecture Planning.md` | 22.15 Version the search universe | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-617 | `Continue Architecture Planning.md` | 22.16 Coverage ledger | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-618 | `Continue Architecture Planning.md` | 22.17 Three graphs now interact | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-619 | `Continue Architecture Planning.md` | 22.18 Completeness assessment | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-620 | `Continue Architecture Planning.md` | 22.19 Assurance levels | `validation/verification.md` | MOVE | DESIGNED |
| CAP-621 | `Continue Architecture Planning.md` | 22.20 Search completeness matrix | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-622 | `Continue Architecture Planning.md` | 22.21 Coverage calculation | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-623 | `Continue Architecture Planning.md` | 22.22 Coverage should be query-relative | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-624 | `Continue Architecture Planning.md` | 22.23 Failure taxonomy | `validation/failure-taxonomy.md` | MOVE | DESIGNED |
| CAP-625 | `Continue Architecture Planning.md` | 22.24 Core invariants | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-626 | `Continue Architecture Planning.md` | Invariant 1 | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-627 | `Continue Architecture Planning.md` | Invariant 2 | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-628 | `Continue Architecture Planning.md` | Invariant 3 | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-629 | `Continue Architecture Planning.md` | Invariant 4 | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-630 | `Continue Architecture Planning.md` | Invariant 5 | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-631 | `Continue Architecture Planning.md` | Invariant 6 | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-632 | `Continue Architecture Planning.md` | Invariant 7 | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-633 | `Continue Architecture Planning.md` | Invariant 8 | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-634 | `Continue Architecture Planning.md` | Invariant 9 | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-635 | `Continue Architecture Planning.md` | Invariant 10 | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-636 | `Continue Architecture Planning.md` | 22.25 v0.22 architecture | `architecture/system-model.md` | MOVE | DESIGNED |
| CAP-637 | `Continue Architecture Planning.md` | 22.26 The conceptual jump | `concepts/overview.md` | MOVE | DESIGNED |
| CAP-638 | `Continue Architecture Planning.md` | v0.23 — Negative Evidence + Absence Reasoning | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-639 | `Continue Architecture Planning.md` | *turn 58 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-640 | `Continue Architecture Planning.md` | v0.23 — Negative Evidence + Absence Reasoning | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-641 | `Continue Architecture Planning.md` | 23.1 The absence problem | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-642 | `Continue Architecture Planning.md` | 23.2 Four fundamental states | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-643 | `Continue Architecture Planning.md` | 23.3 PresenceAssertion | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-644 | `Continue Architecture Planning.md` | 23.4 Absence is always scoped | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-645 | `Continue Architecture Planning.md` | 23.5 NegativeEvidence | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-646 | `Continue Architecture Planning.md` | 23.6 Absence strength | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-647 | `Continue Architecture Planning.md` | 23.7 Search failure must not become negative evidence automatically | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-648 | `Continue Architecture Planning.md` | 23.8 Failure → evidence mapping | `validation/failure-taxonomy.md` | MOVE | DESIGNED |
| CAP-649 | `Continue Architecture Planning.md` | 23.9 Exact locator absence | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-650 | `Continue Architecture Planning.md` | 23.10 Claims need predicates | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-651 | `Continue Architecture Planning.md` | 23.11 Predicate-aware absence | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-652 | `Continue Architecture Planning.md` | 23.12 Contradiction becomes first-class | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-653 | `Continue Architecture Planning.md` | 23.13 True contradiction | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-654 | `Continue Architecture Planning.md` | 23.14 Absence confidence cannot simply be numeric | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-655 | `Continue Architecture Planning.md` | 23.15 Independent evidence | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-656 | `Continue Architecture Planning.md` | 23.16 Absence reasoning engine | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-657 | `Continue Architecture Planning.md` | 23.17 Formal absence rule | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-658 | `Continue Architecture Planning.md` | 23.18 Dynamic universes | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-659 | `Continue Architecture Planning.md` | 23.19 Temporal validity | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-660 | `Continue Architecture Planning.md` | 23.20 Absence and revision detection | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-661 | `Continue Architecture Planning.md` | 23.21 Search state now becomes richer | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-662 | `Continue Architecture Planning.md` | 23.22 Architecture after v0.23 | `architecture/system-model.md` | MOVE | DESIGNED |
| CAP-663 | `Continue Architecture Planning.md` | 23.23 The three epistemic outcomes | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-664 | `Continue Architecture Planning.md` | Presence | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-665 | `Continue Architecture Planning.md` | Absence | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-666 | `Continue Architecture Planning.md` | Unknown | `architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-667 | `Continue Architecture Planning.md` | 23.24 New invariants | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-668 | `Continue Architecture Planning.md` | Invariant 1 | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-669 | `Continue Architecture Planning.md` | Invariant 2 | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-670 | `Continue Architecture Planning.md` | Invariant 3 | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-671 | `Continue Architecture Planning.md` | Invariant 4 | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-672 | `Continue Architecture Planning.md` | Invariant 5 | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-673 | `Continue Architecture Planning.md` | Invariant 6 | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-674 | `Continue Architecture Planning.md` | Invariant 7 | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-675 | `Continue Architecture Planning.md` | Invariant 8 | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-676 | `Continue Architecture Planning.md` | Invariant 9 | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-677 | `Continue Architecture Planning.md` | Invariant 10 | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-678 | `Continue Architecture Planning.md` | 23.25 v0.23 conceptual result | `concepts/overview.md` | MOVE | DESIGNED |
| CAP-679 | `Continue Architecture Planning.md` | v0.24 — Query/Goal-Constrained Discovery | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-680 | `Continue Architecture Planning.md` | *turn 60 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-681 | `Continue Architecture Planning.md` | v0.24 — Query/Goal-Constrained Discovery | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-682 | `Continue Architecture Planning.md` | 24.1 SearchGoal | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-683 | `Continue Architecture Planning.md` | 24.2 Goal ≠ Domain | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-684 | `Continue Architecture Planning.md` | 24.3 Goal constraints | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-685 | `Continue Architecture Planning.md` | 24.4 Hard constraints vs soft preferences | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-686 | `Continue Architecture Planning.md` | 24.5 GoalConstraint | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-687 | `Continue Architecture Planning.md` | 24.6 Relevance is not classification | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-688 | `Continue Architecture Planning.md` | 24.7 RelevanceAssertion | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-689 | `Continue Architecture Planning.md` | 24.8 Why `UNKNOWN` matters | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-690 | `Continue Architecture Planning.md` | 24.9 Relevance scoring | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-691 | `Continue Architecture Planning.md` | 24.10 The six questions | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-692 | `Continue Architecture Planning.md` | 24.11 Relevant Search Space | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-693 | `Continue Architecture Planning.md` | 24.12 Example | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-694 | `Continue Architecture Planning.md` | 24.13 Goal-directed adaptive discovery | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-695 | `Continue Architecture Planning.md` | 24.14 Expected Goal Value | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-696 | `Continue Architecture Planning.md` | 24.15 Information gain | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-697 | `Continue Architecture Planning.md` | 24.16 Goal-aware partition scoring | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-698 | `Continue Architecture Planning.md` | 24.17 Goal does not grant authority | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-699 | `Continue Architecture Planning.md` | 24.18 Goal provenance | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-700 | `Continue Architecture Planning.md` | 24.19 Goal-aware discovery event | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-701 | `Continue Architecture Planning.md` | 24.20 Goal lifecycle | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-702 | `Continue Architecture Planning.md` | 24.21 Goal termination policies | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-703 | `Continue Architecture Planning.md` | 24.22 Goal satisfaction vs completeness | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-704 | `Continue Architecture Planning.md` | 24.23 GoalResult | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-705 | `Continue Architecture Planning.md` | 24.24 Result ranking | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-706 | `Continue Architecture Planning.md` | 24.25 Result quality model | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-707 | `Continue Architecture Planning.md` | 24.26 Goal conflict | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-708 | `Continue Architecture Planning.md` | 24.27 Goal sessions | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-709 | `Continue Architecture Planning.md` | 24.28 Reuse of previous knowledge | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-710 | `Continue Architecture Planning.md` | 24.29 Knowledge reuse is not evidence reuse without qualification | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-711 | `Continue Architecture Planning.md` | 24.30 New architecture | `architecture/system-model.md` | MOVE | DESIGNED |
| CAP-712 | `Continue Architecture Planning.md` | 24.31 The architecture's semantic layers | `architecture/system-model.md` | MOVE | DESIGNED |
| CAP-713 | `Continue Architecture Planning.md` | 24.32 Core invariants for v0.24 | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-714 | `Continue Architecture Planning.md` | Invariant 1 | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-715 | `Continue Architecture Planning.md` | Invariant 2 | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-716 | `Continue Architecture Planning.md` | Invariant 3 | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-717 | `Continue Architecture Planning.md` | Invariant 4 | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-718 | `Continue Architecture Planning.md` | Invariant 5 | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-719 | `Continue Architecture Planning.md` | Invariant 6 | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-720 | `Continue Architecture Planning.md` | Invariant 7 | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-721 | `Continue Architecture Planning.md` | Invariant 8 | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-722 | `Continue Architecture Planning.md` | Invariant 9 | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-723 | `Continue Architecture Planning.md` | Invariant 10 | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-724 | `Continue Architecture Planning.md` | 24.33 What v0.24 changes fundamentally | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-725 | `Continue Architecture Planning.md` | v0.25 — Discovery Query Planner | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-726 | `Continue Architecture Planning.md` | *turn 62 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-727 | `Continue Architecture Planning.md` | v0.25 — Discovery Query Planner | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-728 | `Continue Architecture Planning.md` | 25.1 Planner ≠ Search Engine | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-729 | `Continue Architecture Planning.md` | 25.2 QueryPlan | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-730 | `Continue Architecture Planning.md` | 25.3 QueryStep | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-731 | `Continue Architecture Planning.md` | 25.4 Query decomposition | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-732 | `Continue Architecture Planning.md` | 25.5 Search axes | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-733 | `Continue Architecture Planning.md` | 25.6 QueryTactic | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-734 | `Continue Architecture Planning.md` | 25.7 Tactic ≠ Strategy | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-735 | `Continue Architecture Planning.md` | 25.8 Planner plugins | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-736 | `Continue Architecture Planning.md` | 25.9 Planner contract | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-737 | `Continue Architecture Planning.md` | 25.10 Query plan example | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-738 | `Continue Architecture Planning.md` | 25.11 Dependencies | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-739 | `Continue Architecture Planning.md` | 25.12 Conditional planning | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-740 | `Continue Architecture Planning.md` | 25.13 Planning boundary | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-741 | `Continue Architecture Planning.md` | 25.14 Query plan validation | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-742 | `Continue Architecture Planning.md` | 25.15 Planner and adaptive discovery | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-743 | `Continue Architecture Planning.md` | 25.16 Exploration vs exploitation moves upward | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-744 | `Continue Architecture Planning.md` | 25.17 Query tactic performance | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-745 | `Continue Architecture Planning.md` | 25.18 Query planner provenance | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-746 | `Continue Architecture Planning.md` | 25.19 Query plan identity | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-747 | `Continue Architecture Planning.md` | 25.20 Plan versioning | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-748 | `Continue Architecture Planning.md` | 25.21 Planner cannot erase old work | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-749 | `Continue Architecture Planning.md` | 25.22 Query expansion | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-750 | `Continue Architecture Planning.md` | 25.23 Expansion evidence | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-751 | `Continue Architecture Planning.md` | 25.24 Planner hallucination boundary | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-752 | `Continue Architecture Planning.md` | 25.25 Search hypothesis | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-753 | `Continue Architecture Planning.md` | 25.26 Query planner and DVB analogy | `research/dvb-blind-scan.md` | MOVE | DESIGNED |
| CAP-754 | `Continue Architecture Planning.md` | 25.27 Planner output is not execution | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-755 | `Continue Architecture Planning.md` | 25.28 Planner budget | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-756 | `Continue Architecture Planning.md` | 25.29 Three different budgets | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-757 | `Continue Architecture Planning.md` | 25.30 Termination propagation | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-758 | `Continue Architecture Planning.md` | 25.31 v0.25 complete architecture | `architecture/system-model.md` | MOVE | DESIGNED |
| CAP-759 | `Continue Architecture Planning.md` | 25.32 v0.25 invariants | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-760 | `Continue Architecture Planning.md` | Planner invariants | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-761 | `Continue Architecture Planning.md` | 25.33 The resulting abstraction stack | `architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-762 | `Continue Architecture Planning.md` | v0.26 — Search Tactic Runtime | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-763 | `Continue Architecture Planning.md` | *turn 64 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-764 | `Continue Architecture Planning.md` | v0.26 — Search Tactic Runtime | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-765 | `Continue Architecture Planning.md` | 26.1 The architectural gap | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-766 | `Continue Architecture Planning.md` | 26.2 QueryStep ≠ TacticExecution | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-767 | `Continue Architecture Planning.md` | 26.3 TacticExecution | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-768 | `Continue Architecture Planning.md` | 26.4 TacticRuntime | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-769 | `Continue Architecture Planning.md` | 26.5 TacticRuntime responsibilities | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-770 | `Continue Architecture Planning.md` | 26.6 Tactic contract | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-771 | `Continue Architecture Planning.md` | 26.7 Capability surface | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-772 | `Continue Architecture Planning.md` | 26.8 Bounded execution | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-773 | `Continue Architecture Planning.md` | 26.9 Batch execution | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-774 | `Continue Architecture Planning.md` | 26.10 Cursor | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-775 | `Continue Architecture Planning.md` | 26.11 Checkpoint | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-776 | `Continue Architecture Planning.md` | 26.12 Checkpoint atomicity | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-777 | `Continue Architecture Planning.md` | 26.13 Tactic dependencies | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-778 | `Continue Architecture Planning.md` | 26.14 Tactic lifecycle | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-779 | `Continue Architecture Planning.md` | 26.15 Exhaustion vs completion | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-780 | `Continue Architecture Planning.md` | 26.16 Tactic result | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-781 | `Continue Architecture Planning.md` | 26.17 Tactic does not create candidates directly | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-782 | `Continue Architecture Planning.md` | 26.18 Tactic → Strategy relationship | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-783 | `Continue Architecture Planning.md` | 26.19 Tactic provenance | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-784 | `Continue Architecture Planning.md` | 26.20 Failure taxonomy | `validation/failure-taxonomy.md` | MOVE | DESIGNED |
| CAP-785 | `Continue Architecture Planning.md` | Planning failures | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-786 | `Continue Architecture Planning.md` | Runtime failures | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-787 | `Continue Architecture Planning.md` | Strategy failures | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-788 | `Continue Architecture Planning.md` | Search failures | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-789 | `Continue Architecture Planning.md` | Recovery failures | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-790 | `Continue Architecture Planning.md` | 26.21 Retry semantics | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-791 | `Continue Architecture Planning.md` | 26.22 Cancellation | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-792 | `Continue Architecture Planning.md` | 26.23 Shared Frontier interaction | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-793 | `Continue Architecture Planning.md` | 26.24 v0.26 architecture | `architecture/system-model.md` | MOVE | DESIGNED |
| CAP-794 | `Continue Architecture Planning.md` | 26.25 Accounting | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-795 | `Continue Architecture Planning.md` | 26.26 The important safety invariant | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-796 | `Continue Architecture Planning.md` | 26.27 Resumability invariant | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-797 | `Continue Architecture Planning.md` | 26.28 New state model | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-798 | `Continue Architecture Planning.md` | 26.29 v0.26 invariants | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-799 | `Continue Architecture Planning.md` | I1 — Planning/execution separation | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-800 | `Continue Architecture Planning.md` | I2 — Execution identity | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-801 | `Continue Architecture Planning.md` | I3 — Single scheduler authority | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-802 | `Continue Architecture Planning.md` | I4 — Bounded execution | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-803 | `Continue Architecture Planning.md` | I5 — Resumability | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-804 | `Continue Architecture Planning.md` | I6 — No silent cursor advancement | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-805 | `Continue Architecture Planning.md` | I7 — Proposal boundary | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-806 | `Continue Architecture Planning.md` | I8 — No authority escalation | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-807 | `Continue Architecture Planning.md` | I9 — Exhaustion separation | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-808 | `Continue Architecture Planning.md` | I10 — Failure ≠ absence | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-809 | `Continue Architecture Planning.md` | I11 — Provenance | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-810 | `Continue Architecture Planning.md` | I12 — Versioned recovery | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-811 | `Continue Architecture Planning.md` | 26.30 What v0.26 actually gives us | `concepts/overview.md` | MOVE | DESIGNED |
| CAP-812 | `Continue Architecture Planning.md` | Next boundary: v0.27 | `roadmap/future-work.md` | MOVE | FUTURE |
| CAP-813 | `Continue Architecture Planning.md` | *turn 66 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-814 | `Continue Architecture Planning.md` | v0.27 — Enumeration Runtime | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-815 | `Continue Architecture Planning.md` | 27.1 The central distinction | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-816 | `Continue Architecture Planning.md` | 27.2 Enumeration as a contract | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-817 | `Continue Architecture Planning.md` | 27.3 Enumerator interface | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-818 | `Continue Architecture Planning.md` | 27.4 EnumerationPage | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-819 | `Continue Architecture Planning.md` | 27.5 `hasMore` is not always trustworthy | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-820 | `Continue Architecture Planning.md` | 27.6 Enumeration state machine | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-821 | `Continue Architecture Planning.md` | 27.7 EnumerationRuntime | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-822 | `Continue Architecture Planning.md` | 27.8 Why this should not be inside DiscoveryStrategy | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-823 | `Continue Architecture Planning.md` | 27.9 Enumerator examples | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-824 | `Continue Architecture Planning.md` | Sitemap | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-825 | `Continue Architecture Planning.md` | API | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-826 | `Continue Architecture Planning.md` | Repository | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-827 | `Continue Architecture Planning.md` | Manifest | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-828 | `Continue Architecture Planning.md` | 27.10 EnumerationEntry | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-829 | `Continue Architecture Planning.md` | 27.11 Entry identity | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-830 | `Continue Architecture Planning.md` | 27.12 Enumeration cursor | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-831 | `Continue Architecture Planning.md` | Offset | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-832 | `Continue Architecture Planning.md` | Page | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-833 | `Continue Architecture Planning.md` | Token | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-834 | `Continue Architecture Planning.md` | Locator | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-835 | `Continue Architecture Planning.md` | Composite | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-836 | `Continue Architecture Planning.md` | 27.13 Cursor validity | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-837 | `Continue Architecture Planning.md` | 27.14 Enumeration snapshot | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-838 | `Continue Architecture Planning.md` | 27.15 Why snapshot identity matters | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-839 | `Continue Architecture Planning.md` | 27.16 Cardinality | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-840 | `Continue Architecture Planning.md` | 27.17 Ordering semantics | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-841 | `Continue Architecture Planning.md` | 27.18 Enumeration consistency | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-842 | `Continue Architecture Planning.md` | 27.19 Completeness assessment | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-843 | `Continue Architecture Planning.md` | 27.20 The crucial three-level distinction | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-844 | `Continue Architecture Planning.md` | 27.21 Example: sitemap | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-845 | `Continue Architecture Planning.md` | 27.22 Enumeration → Coverage | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-846 | `Continue Architecture Planning.md` | 27.23 Enumeration and negative evidence | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-847 | `Continue Architecture Planning.md` | 27.24 Enumeration budget | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-848 | `Continue Architecture Planning.md` | 27.25 Enumeration termination states | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-849 | `Continue Architecture Planning.md` | 27.26 Enumeration accounting | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-850 | `Continue Architecture Planning.md` | 27.27 Enumeration provenance | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-851 | `Continue Architecture Planning.md` | 27.28 Enumeration replay | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-852 | `Continue Architecture Planning.md` | 27.29 Full v0.27 architecture | `architecture/system-model.md` | MOVE | DESIGNED |
| CAP-853 | `Continue Architecture Planning.md` | 27.30 New invariants | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-854 | `Continue Architecture Planning.md` | E1 — Enumeration is scoped | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-855 | `Continue Architecture Planning.md` | E2 — Enumeration termination is not global completeness | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-856 | `Continue Architecture Planning.md` | E3 — Budget exhaustion is not enumeration exhaustion | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-857 | `Continue Architecture Planning.md` | E4 — Cursor progress must be durable | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-858 | `Continue Architecture Planning.md` | E5 — Enumeration entries are not candidates | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-859 | `Continue Architecture Planning.md` | E6 — Cardinality is evidence | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-860 | `Continue Architecture Planning.md` | E7 — Historical snapshots remain immutable | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-861 | `Continue Architecture Planning.md` | E8 — Incomplete enumeration cannot establish absence | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-862 | `Continue Architecture Planning.md` | E9 — Unstable enumeration weakens completeness | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-863 | `Continue Architecture Planning.md` | E10 — Enumerator has no acquisition authority | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-864 | `Continue Architecture Planning.md` | E11 — Enumerator cannot directly mutate the ResourceGraph | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-865 | `Continue Architecture Planning.md` | E12 — Termination evidence is provenance-bearing | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-866 | `Continue Architecture Planning.md` | 27.31 The emerging blind-scan analogy | `research/dvb-blind-scan.md` | MOVE | DESIGNED |
| CAP-867 | `Continue Architecture Planning.md` | v0.27 takeaway | `architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-868 | `Continue Architecture Planning.md` | v0.28 — Search-Space Reconciliation & Frontier Deduplication | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-869 | `Continue Architecture Planning.md` | *turn 68 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-870 | `Continue Architecture Planning.md` | v0.28 — Search-Space Reconciliation & Frontier Deduplication | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-871 | `Continue Architecture Planning.md` | 28.1 The problem with naive deduplication | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-872 | `Continue Architecture Planning.md` | 28.2 Five different kinds of duplication | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-873 | `Continue Architecture Planning.md` | 28.3 Search-space overlap | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-874 | `Continue Architecture Planning.md` | 28.4 SearchPartitionRelation | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-875 | `Continue Architecture Planning.md` | 28.5 Coverage overlap | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-876 | `Continue Architecture Planning.md` | 28.6 Frontier deduplication | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-877 | `Continue Architecture Planning.md` | 28.7 SearchWorkKey | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-878 | `Continue Architecture Planning.md` | 28.8 Work equivalence | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-879 | `Continue Architecture Planning.md` | 28.9 Candidate convergence | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-880 | `Continue Architecture Planning.md` | 28.10 Observation convergence | `architecture/observation-model.md` | MOVE | DESIGNED |
| CAP-881 | `Continue Architecture Planning.md` | 28.11 Artifact convergence | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-882 | `Continue Architecture Planning.md` | 28.12 Discovery independence | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-883 | `Continue Architecture Planning.md` | 28.13 Evidence independence model | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-884 | `Continue Architecture Planning.md` | 28.14 Coverage provenance | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-885 | `Continue Architecture Planning.md` | 28.15 Coverage relation | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-886 | `Continue Architecture Planning.md` | 28.16 Coverage union | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-887 | `Continue Architecture Planning.md` | 28.17 Disjoint partitions | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-888 | `Continue Architecture Planning.md` | 28.18 Unknown overlap | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-889 | `Continue Architecture Planning.md` | 28.19 Frontier duplicate suppression | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-890 | `Continue Architecture Planning.md` | 28.20 Duplicate suppression must preserve provenance | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-891 | `Continue Architecture Planning.md` | 28.21 Convergence graph | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-892 | `Continue Architecture Planning.md` | 28.22 Search-space graph | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-893 | `Continue Architecture Planning.md` | 28.23 Search-space coverage ledger | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-894 | `Continue Architecture Planning.md` | 28.24 Candidate count is not coverage | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-895 | `Continue Architecture Planning.md` | 28.25 Search-space deduplication vs candidate deduplication | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-896 | `Continue Architecture Planning.md` | Candidate deduplication | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-897 | `Continue Architecture Planning.md` | Search-space deduplication | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-898 | `Continue Architecture Planning.md` | 28.26 Adaptive strategy interaction | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-899 | `Continue Architecture Planning.md` | 28.27 Example | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-900 | `Continue Architecture Planning.md` | 28.28 Reconciliation algorithm | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-901 | `Continue Architecture Planning.md` | 28.29 Reconciliation must be monotonic | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-902 | `Continue Architecture Planning.md` | 28.30 Reconciliation does not delete evidence | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-903 | `Continue Architecture Planning.md` | 28.31 Failure taxonomy | `validation/failure-taxonomy.md` | MOVE | DESIGNED |
| CAP-904 | `Continue Architecture Planning.md` | 28.32 Core invariants | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-905 | `Continue Architecture Planning.md` | R1 — Candidate convergence | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-906 | `Continue Architecture Planning.md` | R2 — Provenance preservation | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-907 | `Continue Architecture Planning.md` | R3 — Artifact convergence | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-908 | `Continue Architecture Planning.md` | R4 — Observation preservation | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-909 | `Continue Architecture Planning.md` | R5 — Overlap is not duplication | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-910 | `Continue Architecture Planning.md` | R6 — Equivalent work may be suppressed | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-911 | `Continue Architecture Planning.md` | R7 — Suppression preserves provenance | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-912 | `Continue Architecture Planning.md` | R8 — Unknown overlap is not disjointness | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-913 | `Continue Architecture Planning.md` | R9 — Coverage is union-aware | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-914 | `Continue Architecture Planning.md` | R10 — Candidate count does not establish coverage | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-915 | `Continue Architecture Planning.md` | R11 — Evidence independence must be justified | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-916 | `Continue Architecture Planning.md` | R12 — Historical reconciliation is immutable | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-917 | `Continue Architecture Planning.md` | 28.33 v0.28 architecture | `architecture/system-model.md` | MOVE | DESIGNED |
| CAP-918 | `Continue Architecture Planning.md` | 28.34 The deeper architectural result | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-919 | `Continue Architecture Planning.md` | Next boundary — v0.29 | `roadmap/future-work.md` | MOVE | FUTURE |
| CAP-920 | `Continue Architecture Planning.md` | *turn 70 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-921 | `Continue Architecture Planning.md` | v0.29 — Dynamic Search-Space Expansion | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-922 | `Continue Architecture Planning.md` | 29.1 The central distinction | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-923 | `Continue Architecture Planning.md` | 29.2 PartitionProposal | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-924 | `Continue Architecture Planning.md` | 29.3 Why proposals are necessary | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-925 | `Continue Architecture Planning.md` | 29.4 PartitionAdmissionController | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-926 | `Continue Architecture Planning.md` | 29.5 Partition identity | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-927 | `Continue Architecture Planning.md` | 29.6 Partition explosion | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-928 | `Continue Architecture Planning.md` | 29.7 ExpansionBudget | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-929 | `Continue Architecture Planning.md` | 29.8 Local expansion rate | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-930 | `Continue Architecture Planning.md` | 29.9 Expansion rate limiting | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-931 | `Continue Architecture Planning.md` | 29.10 Evidence threshold | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-932 | `Continue Architecture Planning.md` | 29.11 Partition proposal epistemic status | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-933 | `Continue Architecture Planning.md` | 29.12 Hypothesis connection | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-934 | `Continue Architecture Planning.md` | 29.13 Partition generation sources | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-935 | `Continue Architecture Planning.md` | 29.14 Expansion provider boundary | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-936 | `Continue Architecture Planning.md` | 29.15 Dynamic search-space graph | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-937 | `Continue Architecture Planning.md` | 29.16 Partition generation event | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-938 | `Continue Architecture Planning.md` | 29.17 Search-space versioning | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-939 | `Continue Architecture Planning.md` | 29.18 SearchSpaceSnapshot | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-940 | `Continue Architecture Planning.md` | 29.19 Expansion and completeness | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-941 | `Continue Architecture Planning.md` | 29.20 Dynamic expansion and negative evidence | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-942 | `Continue Architecture Planning.md` | 29.21 Expansion priorities | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-943 | `Continue Architecture Planning.md` | 29.22 Expansion depth | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-944 | `Continue Architecture Planning.md` | 29.23 Expansion loops | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-945 | `Continue Architecture Planning.md` | 29.24 Expansion cycle ≠ failure | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-946 | `Continue Architecture Planning.md` | 29.25 Partition admission states | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-947 | `Continue Architecture Planning.md` | 29.26 Partition proposal accounting | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-948 | `Continue Architecture Planning.md` | 29.27 Partition explosion protection | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-949 | `Continue Architecture Planning.md` | 29.28 Admission algorithm | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-950 | `Continue Architecture Planning.md` | 29.29 Frontier generation | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-951 | `Continue Architecture Planning.md` | 29.30 Dynamic expansion architecture | `architecture/system-model.md` | MOVE | DESIGNED |
| CAP-952 | `Continue Architecture Planning.md` | 29.31 Two expansion paths | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-953 | `Continue Architecture Planning.md` | 29.32 Search-space discovery as first-class knowledge | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-954 | `Continue Architecture Planning.md` | 29.33 v0.29 invariants | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-955 | `Continue Architecture Planning.md` | P1 — Discovery does not create authority | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-956 | `Continue Architecture Planning.md` | P2 — Partition proposal is not partition | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-957 | `Continue Architecture Planning.md` | P3 — Every admitted partition belongs to the domain | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-958 | `Continue Architecture Planning.md` | P4 — Expansion is budgeted | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-959 | `Continue Architecture Planning.md` | P5 — Expansion is depth-bounded | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-960 | `Continue Architecture Planning.md` | P6 — Duplicate partitions converge | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-961 | `Continue Architecture Planning.md` | P7 — Overlap is preserved | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-962 | `Continue Architecture Planning.md` | P8 — Evidence is preserved | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-963 | `Continue Architecture Planning.md` | P9 — Partition existence does not schedule execution | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-964 | `Continue Architecture Planning.md` | P10 — Expansion cannot override policy | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-965 | `Continue Architecture Planning.md` | P11 — Search-space versions are immutable | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-966 | `Continue Architecture Planning.md` | P12 — Expansion does not invalidate historical claims automatically | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-967 | `Continue Architecture Planning.md` | P13 — Cycles are legal | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-968 | `Continue Architecture Planning.md` | P14 — Unknown remains valid | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-969 | `Continue Architecture Planning.md` | 29.34 The system after v0.29 | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-970 | `Continue Architecture Planning.md` | 29.35 Blind-scan interpretation | `research/dvb-blind-scan.md` | MOVE | DESIGNED |
| CAP-971 | `Continue Architecture Planning.md` | v0.29 takeaway | `architecture/search-space.md` | MOVE | DESIGNED |
| CAP-972 | `Continue Architecture Planning.md` | v0.30 — Unified Frontier Arbitration | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-973 | `Continue Architecture Planning.md` | *turn 72 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-974 | `Continue Architecture Planning.md` | Conclusion — Generic Discovery Engine | `concepts/overview.md` | MOVE | DESIGNED |
| CAP-975 | `Continue Architecture Planning.md` | The final conceptual separation | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-976 | `Continue Architecture Planning.md` | The fundamental invariant | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-977 | `Continue Architecture Planning.md` | What the DVB analogy actually contributed | `research/dvb-blind-scan.md` | MOVE | DESIGNED |
| CAP-978 | `Continue Architecture Planning.md` | The most important safety boundary | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-979 | `Continue Architecture Planning.md` | Final architecture | `architecture/system-model.md` | MOVE | DESIGNED |
| CAP-980 | `Continue Architecture Planning.md` | What the userscript should and should not become | `prototype/limitations.md` | MOVE | CURRENT |
| CAP-981 | `Continue Architecture Planning.md` | Final principles | `concepts/overview.md` | MOVE | DESIGNED |
| CAP-982 | `Continue Architecture Planning.md` | *turn 74 you lead-in* | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-983 | `Continue Architecture Planning.md` | v0.30 — Unified Frontier Arbitration | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-984 | `Continue Architecture Planning.md` | 30.1 The new architecture | `architecture/system-model.md` | MOVE | DESIGNED |
| CAP-985 | `Continue Architecture Planning.md` | 30.2 WorkClass | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-986 | `Continue Architecture Planning.md` | 30.3 WorkClassPolicy | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-987 | `Continue Architecture Planning.md` | 30.4 ArbitrationDecision | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-988 | `Continue Architecture Planning.md` | 30.5 Hard constraints vs soft priorities | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-989 | `Continue Architecture Planning.md` | Hard constraints | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-990 | `Continue Architecture Planning.md` | Soft priorities | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-991 | `Continue Architecture Planning.md` | 30.6 Arbitration score | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-992 | `Continue Architecture Planning.md` | 30.7 Aging | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-993 | `Continue Architecture Planning.md` | 30.8 Starvation detection | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-994 | `Continue Architecture Planning.md` | 30.9 Class starvation | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-995 | `Continue Architecture Planning.md` | 30.10 Weighted fairness | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-996 | `Continue Architecture Planning.md` | 30.11 Deficit-style arbitration | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-997 | `Continue Architecture Planning.md` | 30.12 Cost-aware scheduling | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-998 | `Continue Architecture Planning.md` | 30.13 Backpressure | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-999 | `Continue Architecture Planning.md` | 30.14 Reserved capacity | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-1000 | `Continue Architecture Planning.md` | 30.15 Arbitration pipeline | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-1001 | `Continue Architecture Planning.md` | 30.16 The atomicity problem | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-1002 | `Continue Architecture Planning.md` | 30.17 Priority inversion | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-1003 | `Continue Architecture Planning.md` | 30.18 FrontierArbitrator | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-1004 | `Continue Architecture Planning.md` | 30.19 Arbitration result | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-1005 | `Continue Architecture Planning.md` | 30.20 Arbitration ledger | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-1006 | `Continue Architecture Planning.md` | 30.21 Replay | `architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-1007 | `Continue Architecture Planning.md` | 30.22 The deeper invariant | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-1008 | `Continue Architecture Planning.md` | 30.23 Full v0.30 architecture | `architecture/system-model.md` | MOVE | DESIGNED |
| CAP-1009 | `Continue Architecture Planning.md` | 30.24 Failure taxonomy | `validation/failure-taxonomy.md` | MOVE | DESIGNED |
| CAP-1010 | `Continue Architecture Planning.md` | 30.25 v0.30 invariants | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-1011 | `Continue Architecture Planning.md` | 30.26 What v0.30 actually accomplishes | `concepts/overview.md` | MOVE | DESIGNED |
| CAP-1012 | `Continue Architecture Planning.md` | Next boundary — v0.31 | `roadmap/future-work.md` | MOVE | FUTURE |
| CAP-1013 | `Continue Architecture Planning.md` | *turn 76 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-1014 | `Continue Architecture Planning.md` | v0.31 — Unified Resource & Cost Ledger | `architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1015 | `Continue Architecture Planning.md` | 31.1 Resource dimensions | `architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1016 | `Continue Architecture Planning.md` | 31.2 ResourceBudget | `architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1017 | `Continue Architecture Planning.md` | 31.3 Three resource states | `architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1018 | `Continue Architecture Planning.md` | 31.4 ResourceReservation | `architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1019 | `Continue Architecture Planning.md` | 31.5 Estimated cost vs actual cost | `architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1020 | `Continue Architecture Planning.md` | 31.6 CostObservation | `architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1021 | `Continue Architecture Planning.md` | 31.7 ResourceLedger | `architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1022 | `Continue Architecture Planning.md` | 31.8 Budget scopes | `architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1023 | `Continue Architecture Planning.md` | 31.9 Hierarchical budget accounting | `architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1024 | `Continue Architecture Planning.md` | 31.10 Resource allocation | `architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1025 | `Continue Architecture Planning.md` | 31.11 Allocation is not execution | `architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1026 | `Continue Architecture Planning.md` | 31.12 Partial consumption | `architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1027 | `Continue Architecture Planning.md` | 31.13 Cost overruns | `architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1028 | `Continue Architecture Planning.md` | 31.14 Cost model | `architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1029 | `Continue Architecture Planning.md` | 31.15 Cost is context-dependent | `architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1030 | `Continue Architecture Planning.md` | 31.16 Resource exhaustion | `architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1031 | `Continue Architecture Planning.md` | 31.17 Budget exhaustion vs frontier exhaustion | `architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1032 | `Continue Architecture Planning.md` | 31.18 Resource reservation race | `architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1033 | `Continue Architecture Planning.md` | 31.19 Settlement | `architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1034 | `Continue Architecture Planning.md` | 31.20 Cost feedback | `architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1035 | `Continue Architecture Planning.md` | 31.21 ResourceLedger events | `architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1036 | `Continue Architecture Planning.md` | 31.22 Resource accounting and provenance | `architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1037 | `Continue Architecture Planning.md` | 31.23 Unified v0.31 architecture | `architecture/system-model.md` | MOVE | DESIGNED |
| CAP-1038 | `Continue Architecture Planning.md` | 31.24 The central v0.31 invariants | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-1039 | `Continue Architecture Planning.md` | 31.25 What v0.31 adds | `architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1040 | `Continue Architecture Planning.md` | v0.32 boundary | `architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1041 | `Continue Architecture Planning.md` | *turn 78 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-1042 | `Continue Architecture Planning.md` | v0.32 — Transactional Persistence & Crash Recovery | `architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1043 | `Continue Architecture Planning.md` | 32.1 The crash problem | `architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1044 | `Continue Architecture Planning.md` | 32.2 Durable state vs runtime state | `architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1045 | `Continue Architecture Planning.md` | 32.3 Persistence is not serialization | `architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1046 | `Continue Architecture Planning.md` | 32.4 PersistenceAdapter | `architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1047 | `Continue Architecture Planning.md` | 32.5 Transaction | `architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1048 | `Continue Architecture Planning.md` | 32.6 Write-ahead event ledger | `architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1049 | `Continue Architecture Planning.md` | 32.7 Event identity | `architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1050 | `Continue Architecture Planning.md` | 32.8 Monotonic sequence | `architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1051 | `Continue Architecture Planning.md` | 32.9 Commit protocol | `architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1052 | `Continue Architecture Planning.md` | 32.10 Commit markers | `architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1053 | `Continue Architecture Planning.md` | 32.11 Checkpoint correctness | `architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1054 | `Continue Architecture Planning.md` | 32.12 At-least-once vs exactly-once | `architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1055 | `Continue Architecture Planning.md` | 32.13 Idempotency | `architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1056 | `Continue Architecture Planning.md` | 32.14 Work recovery | `architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1057 | `Continue Architecture Planning.md` | 32.15 Recovery scan | `architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1058 | `Continue Architecture Planning.md` | 32.16 RecoveryManager | `architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1059 | `Continue Architecture Planning.md` | 32.17 Reservation recovery | `architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1060 | `Continue Architecture Planning.md` | 32.18 Accounting invariant under crash | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-1061 | `Continue Architecture Planning.md` | 32.19 Observation recovery | `architecture/observation-model.md` | MOVE | DESIGNED |
| CAP-1062 | `Continue Architecture Planning.md` | 32.20 Artifact durability | `architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1063 | `Continue Architecture Planning.md` | 32.21 Durable checkpoint | `architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1064 | `Continue Architecture Planning.md` | 32.22 Recovery invariant for cursors | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-1065 | `Continue Architecture Planning.md` | 32.23 Schema versioning | `architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1066 | `Continue Architecture Planning.md` | 32.24 Snapshot + journal | `architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1067 | `Continue Architecture Planning.md` | 32.25 Snapshot integrity | `architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1068 | `Continue Architecture Planning.md` | 32.26 Recovery outcomes | `architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1069 | `Continue Architecture Planning.md` | 32.27 Recovery must not fabricate knowledge | `architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1070 | `Continue Architecture Planning.md` | 32.28 Crash-safe frontier | `architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1071 | `Continue Architecture Planning.md` | 32.29 Reconciliation | `architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1072 | `Continue Architecture Planning.md` | 32.30 Repair is itself provenance | `architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1073 | `Continue Architecture Planning.md` | 32.31 v0.32 architecture | `architecture/system-model.md` | MOVE | DESIGNED |
| CAP-1074 | `Continue Architecture Planning.md` | 32.32 Complete lifecycle | `architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1075 | `Continue Architecture Planning.md` | 32.33 Failure taxonomy | `validation/failure-taxonomy.md` | MOVE | DESIGNED |
| CAP-1076 | `Continue Architecture Planning.md` | 32.34 v0.32 invariants | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-1077 | `Continue Architecture Planning.md` | 32.35 What v0.32 changes | `architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1078 | `Continue Architecture Planning.md` | v0.33 — Multi-Worker / Multi-Context Coordination | `architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1079 | `Continue Architecture Planning.md` | *turn 80 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-1080 | `Continue Architecture Planning.md` | v0.33 — Multi-Worker Coordination & Distributed Claiming | `architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1081 | `Continue Architecture Planning.md` | 33.1 Worker identity | `architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1082 | `Continue Architecture Planning.md` | 33.2 Worker registration | `architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1083 | `Continue Architecture Planning.md` | 33.3 Worker capabilities | `architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1084 | `Continue Architecture Planning.md` | 33.4 Claiming is the synchronization boundary | `architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1085 | `Continue Architecture Planning.md` | 33.5 ClaimToken | `architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1086 | `Continue Architecture Planning.md` | 33.6 Claim ≠ lease | `architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1087 | `Continue Architecture Planning.md` | 33.7 Lease lifecycle | `architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1088 | `Continue Architecture Planning.md` | 33.8 LeaseManager | `architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1089 | `Continue Architecture Planning.md` | 33.9 Heartbeats | `architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1090 | `Continue Architecture Planning.md` | 33.10 Fencing tokens | `architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1091 | `Continue Architecture Planning.md` | 33.11 Fencing invariant | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-1092 | `Continue Architecture Planning.md` | 33.12 Worker death | `architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1093 | `Continue Architecture Planning.md` | 33.13 Duplicate execution | `architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1094 | `Continue Architecture Planning.md` | 33.14 Execution identity | `architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1095 | `Continue Architecture Planning.md` | 33.15 Duplicate observations | `architecture/observation-model.md` | MOVE | DESIGNED |
| CAP-1096 | `Continue Architecture Planning.md` | 33.16 Duplicate execution ≠ independent evidence | `architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1097 | `Continue Architecture Planning.md` | 33.17 Worker-local vs shared state | `architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1098 | `Continue Architecture Planning.md` | 33.18 CoordinationManager | `architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1099 | `Continue Architecture Planning.md` | 33.19 Coordination vs arbitration | `architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1100 | `Continue Architecture Planning.md` | 33.20 Worker selection | `architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1101 | `Continue Architecture Planning.md` | 33.21 Worker affinity | `architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1102 | `Continue Architecture Planning.md` | 33.22 Worker capacity | `architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1103 | `Continue Architecture Planning.md` | 33.23 Distributed accounting | `architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1104 | `Continue Architecture Planning.md` | 33.24 Worker-local caches | `architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1105 | `Continue Architecture Planning.md` | 33.25 Cross-worker event ordering | `architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1106 | `Continue Architecture Planning.md` | 33.26 Causal provenance | `architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1107 | `Continue Architecture Planning.md` | 33.27 Coordination events | `architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1108 | `Continue Architecture Planning.md` | 33.28 Multi-worker failure modes | `validation/failure-taxonomy.md` | MOVE | DESIGNED |
| CAP-1109 | `Continue Architecture Planning.md` | 33.29 Split-brain | `architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1110 | `Continue Architecture Planning.md` | 33.30 What the browser prototype can guarantee | `prototype/limitations.md` | MOVE | CURRENT |
| CAP-1111 | `Continue Architecture Planning.md` | 33.31 Coordination scope | `architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1112 | `Continue Architecture Planning.md` | 33.32 v0.33 architecture | `architecture/system-model.md` | MOVE | DESIGNED |
| CAP-1113 | `Continue Architecture Planning.md` | 33.33 The complete ownership invariant | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-1114 | `Continue Architecture Planning.md` | 33.34 The deeper distributed invariant | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-1115 | `Continue Architecture Planning.md` | 33.35 v0.33 result | `architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1116 | `Continue Architecture Planning.md` | v0.34 — Coordination Protocol & Distributed Consistency | `architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1117 | `Continue Architecture Planning.md` | *turn 82 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-1118 | `Continue Architecture Planning.md` | v0.34 — Distributed Consistency & Conflict Resolution | `architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1119 | `Continue Architecture Planning.md` | 34.1 New Architecture Boundary | `architecture/system-model.md` | MOVE | DESIGNED |
| CAP-1120 | `Continue Architecture Planning.md` | 34.2 The Core Consistency Model | `architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1121 | `Continue Architecture Planning.md` | 34.3 Optimistic Concurrency Control | `architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1122 | `Continue Architecture Planning.md` | 34.4 Version ≠ Time | `architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1123 | `Continue Architecture Planning.md` | 34.5 Event Metadata | `architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1124 | `Continue Architecture Planning.md` | 34.6 Versioning + Fencing | `architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1125 | `Continue Architecture Planning.md` | 34.7 Conflict Is Not One Thing | `architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1126 | `Continue Architecture Planning.md` | Claim conflict | `architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1127 | `Continue Architecture Planning.md` | Candidate conflict | `architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1128 | `Continue Architecture Planning.md` | Classification conflict | `architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1129 | `Continue Architecture Planning.md` | Coverage conflict | `architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1130 | `Continue Architecture Planning.md` | Budget conflict | `architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1131 | `Continue Architecture Planning.md` | 34.8 Conflict Record | `architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1132 | `Continue Architecture Planning.md` | 34.9 Deterministic Conflict Resolver | `architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1133 | `Continue Architecture Planning.md` | 34.10 Resolution Policies | `architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1134 | `Continue Architecture Planning.md` | 34.11 Classification Conflict | `architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1135 | `Continue Architecture Planning.md` | 34.12 Provenance Must Survive Resolution | `architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1136 | `Continue Architecture Planning.md` | 34.13 Last-Write-Wins Is Not the Default | `architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1137 | `Continue Architecture Planning.md` | 34.14 Append-Only Is Especially Powerful | `architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1138 | `Continue Architecture Planning.md` | 34.15 Materialized State | `architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1139 | `Continue Architecture Planning.md` | 34.16 State Digest | `architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1140 | `Continue Architecture Planning.md` | 34.17 Conflict Detection Pipeline | `architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1141 | `Continue Architecture Planning.md` | 34.18 Conflict Detection vs Conflict Resolution | `architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1142 | `Continue Architecture Planning.md` | 34.19 Conflict Resolver Context | `architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1143 | `Continue Architecture Planning.md` | 34.20 Resolution Event | `architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1144 | `Continue Architecture Planning.md` | 34.21 Cross-Object Conflicts | `architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1145 | `Continue Architecture Planning.md` | 34.22 Consistency Domains | `architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1146 | `Continue Architecture Planning.md` | 34.23 Consistency Is Not Global Ordering | `architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1147 | `Continue Architecture Planning.md` | 34.24 Independent Evidence | `architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1148 | `Continue Architecture Planning.md` | 34.25 Failure Taxonomy | `validation/failure-taxonomy.md` | MOVE | DESIGNED |
| CAP-1149 | `Continue Architecture Planning.md` | 34.26 New Core Invariants | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-1150 | `Continue Architecture Planning.md` | Consistency | `architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1151 | `Continue Architecture Planning.md` | Fencing | `architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1152 | `Continue Architecture Planning.md` | Conflict | `architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1153 | `Continue Architecture Planning.md` | Provenance | `architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1154 | `Continue Architecture Planning.md` | Recovery | `architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1155 | `Continue Architecture Planning.md` | Scalability | `architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1156 | `Continue Architecture Planning.md` | 34.27 The Unified State Model | `architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1157 | `Continue Architecture Planning.md` | 34.28 What v0.34 Actually Proves | `validation/verification.md` | MOVE | OPEN |
| CAP-1158 | `Continue Architecture Planning.md` | PROVED by the architecture | `validation/verification.md` | MOVE | OPEN |
| CAP-1159 | `Continue Architecture Planning.md` | ARGUMENT | `validation/verification.md` | MOVE | OPEN |
| CAP-1160 | `Continue Architecture Planning.md` | OPEN | `validation/verification.md` | MOVE | OPEN |
| CAP-1161 | `Continue Architecture Planning.md` | 34.29 Prototype Boundary | `prototype/limitations.md` | MOVE | CURRENT |
| CAP-1162 | `Continue Architecture Planning.md` | 34.30 v0.34 → v0.35 | `roadmap/future-work.md` | MOVE | FUTURE |
| CAP-1163 | `Continue Architecture Planning.md` | *turn 84 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-1164 | `Continue Architecture Planning.md` | Conclusion — Generic Discovery Engine | `concepts/overview.md` | MOVE | DESIGNED |
| CAP-1165 | `Continue Architecture Planning.md` | The decisive conceptual shift | `concepts/overview.md` | MOVE | DESIGNED |
| CAP-1166 | `Continue Architecture Planning.md` | DVB blind scan | `research/dvb-blind-scan.md` | MOVE | DESIGNED |
| CAP-1167 | `Continue Architecture Planning.md` | Generic discovery | `architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1168 | `Continue Architecture Planning.md` | The major architectural invariants | `validation/invariants.md` | MOVE | DESIGNED |
| CAP-1169 | `Continue Architecture Planning.md` | Final architecture by responsibility | `architecture/system-model.md` | MOVE | DESIGNED |
| CAP-1170 | `Continue Architecture Planning.md` | What the prototype actually becomes | `concepts/overview.md` | MOVE | DESIGNED |
| CAP-1171 | `Continue Architecture Planning.md` | Final formulation | `concepts/overview.md` | MOVE | DESIGNED |

## Section records

Full record per specification section 4. `Level` is the original heading level; `Rendered heading` is the heading as it appears in the destination file (specification section 16).

| ID | Position | Level | Parent | Rendered heading | Category | Duplicates | Conflicts | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| USP-001 | 1 | — | — | — | DVB_ANALOGY | — | — | originating request |
| USP-002 | 2 | — | — | — | DVB_ANALOGY | — | — | lead-in of the following section |
| USP-003 | 3 | 3 | — | Generic pseudocode | DVB_ANALOGY | — | — | — |
| USP-004 | 4 | 3 | — | Making it genuinely generic | CONCEPT | — | — | — |
| USP-005 | 5 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| USP-006 | 6 | — | — | — | CONCEPT | — | — | lead-in of the following section |
| USP-007 | 7 | 3 | — | 1. Separate the layers | CONCEPT | — | — | — |
| USP-008 | 8 | 2 | — | 2. Candidate generation | CANDIDATE | — | — | — |
| USP-009 | 9 | 2 | — | 3. Detection should precede expensive decoding | ACQUISITION | — | — | — |
| USP-010 | 10 | 2 | — | 4. Lock is not discovery | ACQUISITION | — | — | — |
| USP-011 | 11 | 2 | — | 5. Use DVB metadata to escape blind mode | DVB_ANALOGY | — | — | — |
| USP-012 | 12 | 2 | — | 6. Deduplication | DATA_MODEL | — | — | — |
| USP-013 | 13 | 2 | — | 7. Generic algorithm | ALGORITHM | — | — | — |
| USP-014 | 14 | 3 | 7. Generic algorithm | The key insight | CONCEPT | — | — | — |
| USP-015 | 15 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| USP-016 | 16 | — | — | — | ALGORITHM | — | — | lead-in of the following section |
| USP-017 | 17 | 3 | — | 8. Model scanning as a search problem | ALGORITHM | — | — | — |
| USP-018 | 18 | 2 | — | 9. Coarse-to-fine search | ALGORITHM | — | — | — |
| USP-019 | 19 | 2 | — | 10. Confidence rather than binary decisions | DATA_MODEL | — | [C-06](REVIEW-NOTES.md#c-06--confidence-one-score-versus-no-single-global-score) | — |
| USP-020 | 20 | 2 | — | 11. Don't immediately discard failed candidates | SCHEDULING | — | — | — |
| USP-021 | 21 | 2 | — | 12. Adaptive retry | SCHEDULING | — | — | — |
| USP-022 | 22 | 2 | — | 13. Scheduling becomes important | SCHEDULING | — | — | — |
| USP-023 | 23 | 2 | — | 14. Discovery database | DISCOVERY | — | [C-10](REVIEW-NOTES.md#c-10--knowledge-store-naming) | — |
| USP-024 | 24 | 2 | — | 15. The generic discovery abstraction | DISCOVERY | — | — | — |
| USP-025 | 25 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| USP-026 | 26 | — | — | — | DATA_MODEL | — | — | lead-in of the following section |
| USP-027 | 27 | 3 | — | 16. Discovery should have evidence levels | DISCOVERY | — | — | — |
| USP-028 | 28 | 2 | — | 17. Use observations to update the search space | OBSERVATION | — | — | — |
| USP-029 | 29 | 2 | — | 18. Termination | ALGORITHM | — | [C-09](REVIEW-NOTES.md#c-09--two-termination-taxonomies) | — |
| USP-030 | 30 | 3 | 18. Termination | Exhaustive scan | ALGORITHM | — | — | — |
| USP-031 | 31 | 3 | 18. Termination | Confidence-based scan | ALGORITHM | — | [C-06](REVIEW-NOTES.md#c-06--confidence-one-score-versus-no-single-global-score) | — |
| USP-032 | 32 | 3 | 18. Termination | Time-bounded scan | ALGORITHM | — | — | — |
| USP-033 | 33 | 3 | 18. Termination | Hybrid | ALGORITHM | — | — | — |
| USP-034 | 34 | 2 | — | 19. Coverage is a better metric than elapsed time | ALGORITHM | — | [C-05](REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified) | — |
| USP-035 | 35 | 2 | — | 20. Cache knowledge between scans | ARCHITECTURE | — | [C-10](REVIEW-NOTES.md#c-10--knowledge-store-naming) | — |
| USP-036 | 36 | 2 | — | 21. Handle disappearing multiplexes | DATA_MODEL | — | — | — |
| USP-037 | 37 | 2 | — | 22. The complete conceptual algorithm | ALGORITHM | — | — | — |
| USP-038 | 38 | 3 | 22. The complete conceptual algorithm | 23. A useful formal name | CONCEPT | — | — | — |
| USP-039 | 39 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| USP-040 | 40 | — | — | — | DATA_MODEL | — | — | lead-in of the following section |
| USP-041 | 41 | 2 | — | 24. Two-dimensional discovery | DISCOVERY | — | — | — |
| USP-042 | 42 | 2 | — | 25. Candidate lifecycle | CANDIDATE | — | — | — |
| USP-043 | 43 | 2 | — | 26. Discovery becomes a graph | DISCOVERY | — | — | — |
| USP-044 | 44 | 2 | — | 27. This helps with incremental scanning | ARCHITECTURE | — | — | — |
| USP-045 | 45 | 2 | — | 28. Parameter provenance | PROVENANCE | — | — | — |
| USP-046 | 46 | 2 | — | 29. The scanner should produce an explanation | PROVENANCE | — | — | — |
| USP-047 | 47 | 2 | — | 30. The final abstraction | CONCEPT | — | — | — |
| USP-048 | 48 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| USP-049 | 49 | — | — | — | ARCHITECTURE | — | — | lead-in of the following section |
| USP-050 | 50 | 2 | — | 31. Define the core objects | ARCHITECTURE | — | — | — |
| USP-051 | 51 | 3 | 31. Define the core objects | Candidate | CANDIDATE | — | — | — |
| USP-052 | 52 | 3 | 31. Define the core objects | Observation | OBSERVATION | — | — | — |
| USP-053 | 53 | 3 | 31. Define the core objects | LockResult | ACQUISITION | — | [C-02](REVIEW-NOTES.md#c-02--the-discovery-pipeline-is-described-with-two-different-step-sets) | — |
| USP-054 | 54 | 3 | 31. Define the core objects | Discovery | DISCOVERY | — | — | — |
| USP-055 | 55 | 2 | — | 32. Use capability-driven adapters | PROVIDER | — | — | — |
| USP-056 | 56 | 2 | — | 33. Discovery strategies should also be pluggable | DISCOVERY | — | — | — |
| USP-057 | 57 | 2 | — | 34. Don't confuse candidate identity with reception identity | CANDIDATE | — | [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution) | — |
| USP-058 | 58 | 2 | — | 35. Make deduplication hierarchical | DATA_MODEL | — | — | — |
| USP-059 | 59 | 2 | — | 36. Treat metadata as a candidate generator | CANDIDATE | — | — | — |
| USP-060 | 60 | 2 | — | 37. Candidate provenance creates a discovery tree | PROVENANCE | — | — | — |
| USP-061 | 61 | 2 | — | 38. Avoid infinite candidate generation | CANDIDATE | — | — | — |
| USP-062 | 62 | 2 | — | 39. A practical scheduler | SCHEDULING | — | — | — |
| USP-063 | 63 | 2 | — | 40. The engine can now become event-driven | ARCHITECTURE | — | — | — |
| USP-064 | 64 | 2 | — | 41. The resulting architecture | ARCHITECTURE | — | — | — |
| USP-065 | 65 | — | — | — | IMPLEMENTATION | `CAP-001` | [D-02](REVIEW-NOTES.md#d-02--) | lead-in of the following section |
| USP-066 | 66 | — | — | — | IMPLEMENTATION | `CAP-001` | [D-02](REVIEW-NOTES.md#d-02--) | — |
| USP-067 | 67 | — | — | — | PROTOTYPE | — | — | prototype positioning |
| USP-068 | 68 | 3 | — | The DVB analogy | DVB_ANALOGY | — | — | — |
| USP-069 | 69 | — | — | — | IMPLEMENTATION | `CAP-001` | [D-02](REVIEW-NOTES.md#d-02--) | lead-in of the following section |
| USP-070 | 70 | — | — | — | IMPLEMENTATION | `CAP-001` | [D-02](REVIEW-NOTES.md#d-02--) | — |
| USP-071 | 71 | 3 | — | What changed — 1. Concurrent claiming is now explicit | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | split at numbered boundary |
| USP-072 | 72 | 3 | — | What changed — 2. HTML is no longer special | PROVIDER | — | — | split at numbered boundary |
| USP-073 | 73 | 3 | — | What changed — 3. The actual scope is now explicit | SCOPE | — | — | split at numbered boundary |
| CAP-001 | 1 | — | — | — | DUPLICATE | `USP-065`, `USP-066`, `USP-069`, `USP-070` | [D-01](REVIEW-NOTES.md#d-01--) | near-duplicate of prototype/versions/01-v0.1.0.md and 02-v0.2.0.md; retained because both copies are damaged differently |
| CAP-002 | 2 | — | — | — | PROTOTYPE | — | — | assessment of the initial scripts |
| CAP-003 | 3 | — | — | — | IMPLEMENTATION | — | — | lead-in of the following section |
| CAP-004 | 4 | — | — | — | IMPLEMENTATION | — | — | — |
| CAP-005 | 5 | 3 | — | v0.3 — What changed from v0.2.0 | HISTORY | — | — | — |
| CAP-006 | 6 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-007 | 7 | — | — | — | ROADMAP | — | — | — |
| CAP-008 | 8 | 3 | — | v0.4 — The biggest v0.4 improvement | ROADMAP | — | — | — |
| CAP-009 | 9 | — | — | — | IMPLEMENTATION | — | — | lead-in of the following section |
| CAP-010 | 10 | — | — | — | IMPLEMENTATION | — | — | — |
| CAP-011 | 11 | 3 | — | v0.4 — Notable v0.4.0 behavior | HISTORY | — | — | — |
| CAP-012 | 12 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-013 | 13 | — | — | — | IMPLEMENTATION | — | [C-01](REVIEW-NOTES.md#c-01--prototype-version-numbering-is-not-monotonic) | — |
| CAP-014 | 14 | — | — | — | HISTORY | — | — | — |
| CAP-015 | 15 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-016 | 16 | — | — | — | IMPLEMENTATION | — | [C-01](REVIEW-NOTES.md#c-01--prototype-version-numbering-is-not-monotonic) | — |
| CAP-017 | 17 | 3 | — | v0.4 — What changed from v0.3.0 | HISTORY | — | — | — |
| CAP-018 | 18 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-019 | 19 | — | — | — | ROADMAP | — | — | — |
| CAP-020 | 20 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-021 | 21 | — | — | — | IMPLEMENTATION | — | — | — |
| CAP-022 | 22 | 3 | — | v0.5 architecture | HISTORY | — | — | explicit override |
| CAP-023 | 23 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-024 | 24 | — | — | — | IMPLEMENTATION | — | [C-01](REVIEW-NOTES.md#c-01--prototype-version-numbering-is-not-monotonic) | — |
| CAP-025 | 25 | 3 | — | v0.5 — What v0.6 changes architecturally | HISTORY | — | — | — |
| CAP-026 | 26 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-027 | 27 | — | — | — | IMPLEMENTATION | — | [C-01](REVIEW-NOTES.md#c-01--prototype-version-numbering-is-not-monotonic) | — |
| CAP-028 | 28 | 3 | — | v0.5 — What v0.5.0 changes architecturally | HISTORY | — | — | — |
| CAP-029 | 29 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-030 | 30 | — | — | — | IMPLEMENTATION | — | — | — |
| CAP-031 | 31 | 3 | — | v0.6.0's main architectural additions | HISTORY | — | — | explicit override |
| CAP-032 | 32 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-033 | 33 | — | — | — | IMPLEMENTATION | — | — | — |
| CAP-034 | 34 | 3 | — | v0.6 — What changed in v0.6 | HISTORY | — | — | — |
| CAP-035 | 35 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-036 | 36 | 2 | — | v0.7.0 — Discovery Graph + Acquisition Planner | DISCOVERY | — | — | — |
| CAP-037 | 37 | 3 | v0.7.0 — Discovery Graph + Acquisition Planner | v0.7 objectives | DATA_MODEL | — | — | — |
| CAP-038 | 38 | 3 | v0.7.0 — Discovery Graph + Acquisition Planner | v0.7 — Core contract | DATA_MODEL | — | — | — |
| CAP-039 | 39 | 3 | v0.7.0 — Discovery Graph + Acquisition Planner | v0.7 — Important v0.7 distinction | DATA_MODEL | — | — | — |
| CAP-040 | 40 | 2 | — | v0.7 state machine | DATA_MODEL | — | — | — |
| CAP-041 | 41 | 2 | — | v0.7 — The deeper abstraction | CONCEPT | — | — | — |
| CAP-042 | 42 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-043 | 43 | — | — | — | IMPLEMENTATION | — | — | — |
| CAP-044 | 44 | — | — | — | HISTORY | — | — | — |
| CAP-045 | 45 | 1 | — | v0.7 — What v0.7.1 actually changes | HISTORY | — | — | — |
| CAP-046 | 46 | 3 | What v0.7.1 actually changes | v0.7 — Before | HISTORY | — | — | — |
| CAP-047 | 47 | 3 | What v0.7.1 actually changes | v0.7 — Now | HISTORY | — | — | — |
| CAP-048 | 48 | 1 | — | v0.7 — 2. The ledger becomes the scan's causal trace | PROVENANCE | — | — | explicit override |
| CAP-049 | 49 | 1 | — | v0.7 — 3. PerformanceObserver correction | DATA_MODEL | — | — | explicit override |
| CAP-050 | 50 | 1 | — | v0.7 — 4. Candidate state machine | HISTORY | — | — | — |
| CAP-051 | 51 | 1 | — | v0.7 — 5. The ledger is not merely logging | PROVENANCE | — | — | explicit override |
| CAP-052 | 52 | 1 | — | v0.7 — 6. One remaining architectural limitation | LIMITATIONS | — | — | — |
| CAP-053 | 53 | 1 | — | v0.7 — 7. Architecture after v0.7.1 | ARCHITECTURE | — | — | — |
| CAP-054 | 54 | 2 | 7. Architecture after v0.7.1 | v0.7 — Next boundary: v0.8 | ROADMAP | — | — | — |
| CAP-055 | 55 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-056 | 56 | 1 | — | v0.8 — Capability-Aware Acquisition Runtime | ACQUISITION | — | — | — |
| CAP-057 | 57 | 2 | v0.8 — Capability-Aware Acquisition Runtime | v0.8 — 1. The three graphs | ARCHITECTURE | — | — | — |
| CAP-058 | 58 | 3 | 1. The three graphs | v0.8 — Discovery graph | DISCOVERY | — | — | — |
| CAP-059 | 59 | 3 | 1. The three graphs | v0.8 — Acquisition graph | ACQUISITION | — | — | — |
| CAP-060 | 60 | 3 | 1. The three graphs | v0.8 — Evidence graph | ARCHITECTURE | — | — | — |
| CAP-061 | 61 | 1 | — | v0.8 — 2. Capability is now a first-class object | ARCHITECTURE | — | — | — |
| CAP-062 | 62 | 1 | — | v0.8 — 3. Capability lattice | ARCHITECTURE | — | — | — |
| CAP-063 | 63 | 1 | — | v0.8 — 4. Capability contract | ARCHITECTURE | — | — | — |
| CAP-064 | 64 | 1 | — | v0.8 — 5. Candidate requirements | CANDIDATE | — | — | — |
| CAP-065 | 65 | 1 | — | v0.8 — 6. Acquisition planning becomes capability resolution | ACQUISITION | — | — | — |
| CAP-066 | 66 | 1 | — | v0.8 — 7. Why this matters for generic discovery | DISCOVERY | — | — | — |
| CAP-067 | 67 | 1 | — | v0.8 — 8. AcquisitionPlan v0.8 | ACQUISITION | — | — | — |
| CAP-068 | 68 | 1 | — | v0.8 — 9. Capability provenance | PROVENANCE | — | — | — |
| CAP-069 | 69 | 1 | — | v0.8 — 10. The four-level authorization model | SECURITY | — | — | — |
| CAP-070 | 70 | 1 | — | v0.8 — 11. New graph model | ARCHITECTURE | — | — | — |
| CAP-071 | 71 | 1 | — | v0.8 — 12. v0.8 ledger | ARCHITECTURE | — | — | — |
| CAP-072 | 72 | 1 | — | v0.8 — 13. Important architectural consequence | ARCHITECTURE | — | — | — |
| CAP-073 | 73 | 1 | — | v0.8 — 14. v0.8 scope boundary | SCOPE | — | — | — |
| CAP-074 | 74 | 3 | 14. v0.8 scope boundary | v0.8 — Implement | ARCHITECTURE | — | — | — |
| CAP-075 | 75 | 3 | 14. v0.8 scope boundary | v0.8 — Represent but deny | SECURITY | — | — | — |
| CAP-076 | 76 | 1 | — | v0.8 — 15. Updated system invariant | VALIDATION | — | — | — |
| CAP-077 | 77 | 1 | — | v0.8 — 16. The DVB analogy is now cleaner | DVB_ANALOGY | — | — | — |
| CAP-078 | 78 | 1 | — | v0.8 — 17. v0.8 → v0.9 | ROADMAP | — | — | — |
| CAP-079 | 79 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-080 | 80 | 2 | — | v0.9 — Acquisition Provider Architecture | ACQUISITION | — | — | — |
| CAP-081 | 81 | 3 | v0.9 — Acquisition Provider Architecture | v0.9 — 0.9 architecture | ARCHITECTURE | — | — | — |
| CAP-082 | 82 | 3 | v0.9 — Acquisition Provider Architecture | v0.9 — The important separation | ACQUISITION | — | — | explicit override |
| CAP-083 | 83 | 1 | — | v0.9 — 1. AcquisitionProvider contract | ACQUISITION | — | — | — |
| CAP-084 | 84 | 1 | — | v0.9 — 2. Provider capabilities | PROVIDER | — | — | — |
| CAP-085 | 85 | 1 | — | v0.9 — 3. Provider selection | PROVIDER | — | — | — |
| CAP-086 | 86 | 1 | — | v0.9 — 4. GM-XHR becomes a component | PROVIDER | — | — | — |
| CAP-087 | 87 | 1 | — | v0.9 — 5. Observation gets provider provenance | OBSERVATION | — | — | — |
| CAP-088 | 88 | 1 | — | v0.9 — 6. Provider failure ≠ acquisition denial | ACQUISITION | — | — | — |
| CAP-089 | 89 | 3 | 6. Provider failure ≠ acquisition denial | v0.9 — Policy denial | SECURITY | — | [C-11](REVIEW-NOTES.md#c-11--same-origin-default-versus-cross-origin-capability) | — |
| CAP-090 | 90 | 3 | 6. Provider failure ≠ acquisition denial | v0.9 — Provider failure | PROVIDER | — | — | — |
| CAP-091 | 91 | 1 | — | v0.9 — 7. Provider selection itself becomes an event | PROVIDER | — | — | — |
| CAP-092 | 92 | 1 | — | v0.9 — 8. A deeper consequence: acquisition becomes replaceable | ACQUISITION | — | — | explicit override |
| CAP-093 | 93 | 3 | 8. A deeper consequence: acquisition becomes replaceable | v0.9 — Cache provider | PROVIDER | — | — | — |
| CAP-094 | 94 | 3 | 8. A deeper consequence: acquisition becomes replaceable | v0.9 — Replay provider | PROVIDER | — | [C-08](REVIEW-NOTES.md#c-08--replay-decisions-deterministic-network-not) | — |
| CAP-095 | 95 | 1 | — | v0.9 — 9. The engine is now approaching a general resource runtime | PROVIDER | — | — | — |
| CAP-096 | 96 | 1 | — | v0.9 — 10. v0.9 invariants | VALIDATION | — | — | — |
| CAP-097 | 97 | 3 | 10. v0.9 invariants | v0.9 — I1 — Discovery independence | VALIDATION | — | — | — |
| CAP-098 | 98 | 3 | 10. v0.9 invariants | v0.9 — I2 — Policy independence | SECURITY | — | [C-11](REVIEW-NOTES.md#c-11--same-origin-default-versus-cross-origin-capability) | — |
| CAP-099 | 99 | 3 | 10. v0.9 invariants | v0.9 — I3 — Capability soundness | VALIDATION | — | — | — |
| CAP-100 | 100 | 3 | 10. v0.9 invariants | v0.9 — I4 — Method safety | VALIDATION | — | — | — |
| CAP-101 | 101 | 3 | 10. v0.9 invariants | v0.9 — I5 — Provenance | PROVENANCE | — | — | — |
| CAP-102 | 102 | 3 | 10. v0.9 invariants | v0.9 — I6 — Observation integrity | OBSERVATION | — | — | — |
| CAP-103 | 103 | 3 | 10. v0.9 invariants | v0.9 — I7 — Replay distinction | VALIDATION | — | [C-08](REVIEW-NOTES.md#c-08--replay-decisions-deterministic-network-not) | — |
| CAP-104 | 104 | 1 | — | v0.9 — 11. The next problem is now visible | ROADMAP | — | — | — |
| CAP-105 | 105 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-106 | 106 | 1 | — | v0.10 — Acquisition Runtime | ACQUISITION | — | — | — |
| CAP-107 | 107 | 2 | v0.10 — Acquisition Runtime | v0.10 — 1. The new architecture | ARCHITECTURE | — | — | — |
| CAP-108 | 108 | 1 | — | v0.10 — 2. The key distinction: Scheduler vs Runtime | SCHEDULING | — | — | — |
| CAP-109 | 109 | 3 | 2. The key distinction: Scheduler vs Runtime | v0.10 — Scheduler | SCHEDULING | — | — | — |
| CAP-110 | 110 | 3 | 2. The key distinction: Scheduler vs Runtime | v0.10 — Runtime | ACQUISITION | — | — | — |
| CAP-111 | 111 | 1 | — | v0.10 — 3. AcquisitionRuntime contract | ACQUISITION | — | — | — |
| CAP-112 | 112 | 1 | — | v0.10 — 4. Admission control | ACQUISITION | — | — | — |
| CAP-113 | 113 | 1 | — | v0.10 — 5. Budget becomes a first-class object | ACQUISITION | — | — | — |
| CAP-114 | 114 | 1 | — | v0.10 — 6. Why reservation must precede execution | ACQUISITION | — | — | — |
| CAP-115 | 115 | 1 | — | v0.10 — 7. OriginController | ACQUISITION | — | — | — |
| CAP-116 | 116 | 1 | — | v0.10 — 8. Provider selection happens after admission prerequisites | PROVIDER | — | — | — |
| CAP-117 | 117 | 1 | — | v0.10 — 9. Provider must not own runtime policy | PROVIDER | — | [C-11](REVIEW-NOTES.md#c-11--same-origin-default-versus-cross-origin-capability) | — |
| CAP-118 | 118 | 1 | — | v0.10 — 10. Cancellation becomes explicit | ACQUISITION | — | — | — |
| CAP-119 | 119 | 1 | — | v0.10 — 11. Timeout belongs to Runtime | ACQUISITION | — | — | — |
| CAP-120 | 120 | 1 | — | v0.10 — 12. Retry belongs to Runtime | ACQUISITION | — | — | — |
| CAP-121 | 121 | 1 | — | v0.10 — 13. Plan vs Attempt | ACQUISITION | — | — | — |
| CAP-122 | 122 | 1 | — | v0.10 — 14. Runtime event model | ACQUISITION | — | — | — |
| CAP-123 | 123 | 1 | — | v0.10 — 15. Runtime state machine | ACQUISITION | — | — | — |
| CAP-124 | 124 | 1 | — | v0.10 — 16. The complete execution equation | ACQUISITION | — | — | — |
| CAP-125 | 125 | 1 | — | v0.10 — 17. The resulting architecture | ARCHITECTURE | — | — | — |
| CAP-126 | 126 | 2 | 17. The resulting architecture | v0.10 — What v0.10 accomplishes | CONCEPT | — | — | — |
| CAP-127 | 127 | 3 | What v0.10 accomplishes | v0.10 — Next boundary: v0.11 | ROADMAP | — | — | — |
| CAP-128 | 128 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-129 | 129 | 1 | — | v0.11 — Response Recognition Runtime | ACQUISITION | — | [C-02](REVIEW-NOTES.md#c-02--the-discovery-pipeline-is-described-with-two-different-step-sets) | — |
| CAP-130 | 130 | 2 | v0.11 — Response Recognition Runtime | v0.11 — 1. v0.11 architecture | ARCHITECTURE | — | — | — |
| CAP-131 | 131 | 1 | — | v0.11 — 2. RecognitionProvider contract | ACQUISITION | — | [C-02](REVIEW-NOTES.md#c-02--the-discovery-pipeline-is-described-with-two-different-step-sets) | — |
| CAP-132 | 132 | 1 | — | v0.11 — 3. Recognition is not discovery | ACQUISITION | — | [C-02](REVIEW-NOTES.md#c-02--the-discovery-pipeline-is-described-with-two-different-step-sets) | — |
| CAP-133 | 133 | 1 | — | v0.11 — 4. Response Router | ACQUISITION | — | — | — |
| CAP-134 | 134 | 1 | — | v0.11 — 5. Provider priority | SCHEDULING | — | — | — |
| CAP-135 | 135 | 1 | — | v0.11 — 6. Recognition confidence | ACQUISITION | — | [C-02](REVIEW-NOTES.md#c-02--the-discovery-pipeline-is-described-with-two-different-step-sets), [C-06](REVIEW-NOTES.md#c-06--confidence-one-score-versus-no-single-global-score) | — |
| CAP-136 | 136 | 1 | — | v0.11 — 7. Content-type is only one signal | ACQUISITION | — | — | — |
| CAP-137 | 137 | 1 | — | v0.11 — 8. Recognition evidence | ACQUISITION | — | [C-02](REVIEW-NOTES.md#c-02--the-discovery-pipeline-is-described-with-two-different-step-sets) | — |
| CAP-138 | 138 | 1 | — | v0.11 — 9. Recognition result contract | ACQUISITION | — | [C-02](REVIEW-NOTES.md#c-02--the-discovery-pipeline-is-described-with-two-different-step-sets) | — |
| CAP-139 | 139 | 1 | — | v0.11 — 10. Why providers should not enqueue candidates | CANDIDATE | — | — | — |
| CAP-140 | 140 | 1 | — | v0.11 — 11. Recognition Runtime | ACQUISITION | — | [C-02](REVIEW-NOTES.md#c-02--the-discovery-pipeline-is-described-with-two-different-step-sets) | — |
| CAP-141 | 141 | 1 | — | v0.11 — 12. Recognition failure taxonomy | VALIDATION | — | [C-02](REVIEW-NOTES.md#c-02--the-discovery-pipeline-is-described-with-two-different-step-sets) | — |
| CAP-142 | 142 | 3 | 12. Recognition failure taxonomy | v0.11 — No recognizer | ACQUISITION | — | — | — |
| CAP-143 | 143 | 3 | 12. Recognition failure taxonomy | v0.11 — Provider rejected | PROVIDER | — | — | — |
| CAP-144 | 144 | 3 | 12. Recognition failure taxonomy | v0.11 — Provider error | PROVIDER | — | — | — |
| CAP-145 | 145 | 3 | 12. Recognition failure taxonomy | v0.11 — Successful recognition, zero discoveries | ACQUISITION | — | [C-02](REVIEW-NOTES.md#c-02--the-discovery-pipeline-is-described-with-two-different-step-sets) | — |
| CAP-146 | 146 | 1 | — | v0.11 — 13. v0.11 state progression | ACQUISITION | — | — | — |
| CAP-147 | 147 | 1 | — | v0.11 — 14. Multiple recognizers | ACQUISITION | — | — | — |
| CAP-148 | 148 | 1 | — | v0.11 — 15. Recognition graph | ACQUISITION | — | [C-02](REVIEW-NOTES.md#c-02--the-discovery-pipeline-is-described-with-two-different-step-sets) | — |
| CAP-149 | 149 | 1 | — | v0.11 — 16. The graph is now explicitly causal | ACQUISITION | — | — | — |
| CAP-150 | 150 | 1 | — | v0.11 — 17. v0.11 event ledger | ACQUISITION | — | — | — |
| CAP-151 | 151 | 1 | — | v0.11 — 18. The emerging generic algorithm | ALGORITHM | — | — | — |
| CAP-152 | 152 | 1 | — | v0.11 — 19. The next major abstraction: Candidate Sources | ROADMAP | — | — | — |
| CAP-153 | 153 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-154 | 154 | 1 | — | v0.12 — Candidate Source Architecture | CANDIDATE | — | — | — |
| CAP-155 | 155 | 2 | v0.12 — Candidate Source Architecture | v0.12 — 1. Three independent provider planes | PROVIDER | — | — | explicit override |
| CAP-156 | 156 | 1 | — | v0.12 — 2. CandidateSource contract | CANDIDATE | — | — | — |
| CAP-157 | 157 | 1 | — | v0.12 — 3. CandidateSource is a search-space adapter | CANDIDATE | — | — | — |
| CAP-158 | 158 | 3 | 3. CandidateSource is a search-space adapter | v0.12 — Web page | PROVIDER | — | — | — |
| CAP-159 | 159 | 3 | 3. CandidateSource is a search-space adapter | v0.12 — Network traffic | PROVIDER | — | — | — |
| CAP-160 | 160 | 3 | 3. CandidateSource is a search-space adapter | v0.12 — Sitemap | PROVIDER | — | — | — |
| CAP-161 | 161 | 3 | 3. CandidateSource is a search-space adapter | v0.12 — User seed | PROVIDER | — | — | — |
| CAP-162 | 162 | 3 | 3. CandidateSource is a search-space adapter | v0.12 — Document | PROVIDER | — | — | — |
| CAP-163 | 163 | 1 | — | v0.12 — 4. CandidateProposal | CANDIDATE | — | — | — |
| CAP-164 | 164 | 1 | — | v0.12 — 5. Why proposals matter | PROVIDER | — | — | — |
| CAP-165 | 165 | 1 | — | v0.12 — 6. CandidateNormalizer | CANDIDATE | — | — | — |
| CAP-166 | 166 | 1 | — | v0.12 — 7. Source Registry | PROVIDER | — | — | — |
| CAP-167 | 167 | 1 | — | v0.12 — 8. The HTML provider should evolve | PROVIDER | — | — | explicit override |
| CAP-168 | 168 | 1 | — | v0.12 — 9. Evidence becomes an intermediate layer | PROVIDER | — | — | — |
| CAP-169 | 169 | 1 | — | v0.12 — 10. Discovery becomes evidence-driven | PROVIDER | — | — | — |
| CAP-170 | 170 | 1 | — | v0.12 — 11. CandidateSource context | CANDIDATE | — | — | — |
| CAP-171 | 171 | 1 | — | v0.12 — 12. CandidateSource examples | CANDIDATE | — | — | — |
| CAP-172 | 172 | 3 | 12. CandidateSource examples | v0.12 — HTML link source | PROVIDER | — | — | — |
| CAP-173 | 173 | 1 | — | v0.12 — 13. NetworkSource | PROVIDER | — | — | — |
| CAP-174 | 174 | 1 | — | v0.12 — 14. Search-space composition | PROVIDER | — | — | — |
| CAP-175 | 175 | 1 | — | v0.12 — 15. Candidate identity | CANDIDATE | — | [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution) | — |
| CAP-176 | 176 | 1 | — | v0.12 — 16. Discovery confidence aggregation | PROVIDER | — | [C-06](REVIEW-NOTES.md#c-06--confidence-one-score-versus-no-single-global-score) | — |
| CAP-177 | 177 | 1 | — | v0.12 — 17. v0.12 provenance graph | PROVENANCE | — | — | — |
| CAP-178 | 178 | 1 | — | v0.12 — 18. v0.12 invariants | VALIDATION | — | — | — |
| CAP-179 | 179 | 3 | 18. v0.12 invariants | v0.12 — S1 — Source purity | VALIDATION | — | — | — |
| CAP-180 | 180 | 3 | 18. v0.12 invariants | v0.12 — S2 — Core ownership | VALIDATION | — | — | — |
| CAP-181 | 181 | 3 | 18. v0.12 invariants | v0.12 — S3 — Proposal semantics | VALIDATION | — | — | — |
| CAP-182 | 182 | 3 | 18. v0.12 invariants | v0.12 — S4 — Identity | VALIDATION | — | [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution) | — |
| CAP-183 | 183 | 3 | 18. v0.12 invariants | v0.12 — S5 — Provenance | PROVENANCE | — | — | — |
| CAP-184 | 184 | 3 | 18. v0.12 invariants | v0.12 — S6 — Representability | VALIDATION | — | — | — |
| CAP-185 | 185 | 3 | 18. v0.12 invariants | v0.12 — S7 — Observation independence | OBSERVATION | — | — | — |
| CAP-186 | 186 | 1 | — | v0.12 — 19. The complete v0.12 architecture | ARCHITECTURE | — | — | — |
| CAP-187 | 187 | 1 | — | v0.12 — 20. The deeper abstraction | CONCEPT | — | — | — |
| CAP-188 | 188 | 2 | 20. The deeper abstraction | v0.13 — the next boundary | ROADMAP | — | — | — |
| CAP-189 | 189 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-190 | 190 | 1 | — | v0.13 — Discovery Controller | DISCOVERY | — | — | — |
| CAP-191 | 191 | 1 | — | v0.13 — 1. The complete v0.13 architecture | ARCHITECTURE | — | — | — |
| CAP-192 | 192 | 1 | — | v0.13 — 2. Two schedulers, not one | SCHEDULING | — | — | — |
| CAP-193 | 193 | 1 | — | v0.13 — 3. DiscoveryTask | DATA_MODEL | — | — | — |
| CAP-194 | 194 | 1 | — | v0.13 — 4. Why a task is necessary | DATA_MODEL | — | — | — |
| CAP-195 | 195 | 1 | — | v0.13 — 5. Source Policy | SECURITY | — | [C-11](REVIEW-NOTES.md#c-11--same-origin-default-versus-cross-origin-capability) | — |
| CAP-196 | 196 | 1 | — | v0.13 — 6. Source budgets | DATA_MODEL | — | — | — |
| CAP-197 | 197 | 1 | — | v0.13 — 7. Proposal budget is different | DATA_MODEL | — | — | — |
| CAP-198 | 198 | 1 | — | v0.13 — 8. Incremental sources | DATA_MODEL | — | — | — |
| CAP-199 | 199 | 1 | — | v0.13 — 9. Source execution contract | DATA_MODEL | — | — | — |
| CAP-200 | 200 | 1 | — | v0.13 — 10. Source scheduling | SCHEDULING | — | — | — |
| CAP-201 | 201 | 1 | — | v0.13 — 11. Fairness | SCHEDULING | — | — | — |
| CAP-202 | 202 | 1 | — | v0.13 — 12. Candidate deduplication belongs after normalization | CANDIDATE | — | — | — |
| CAP-203 | 203 | 1 | — | v0.13 — 13. Discovery provenance | PROVENANCE | — | — | — |
| CAP-204 | 204 | 1 | — | v0.13 — 14. Candidate generation becomes transactional | CANDIDATE | — | — | — |
| CAP-205 | 205 | 1 | — | v0.13 — 15. Concurrent source execution | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-206 | 206 | 1 | — | v0.13 — 16. DiscoveryController | DATA_MODEL | — | — | — |
| CAP-207 | 207 | 1 | — | v0.13 — 17. Event ledger | DATA_MODEL | — | — | — |
| CAP-208 | 208 | 1 | — | v0.13 — 18. Discovery failure taxonomy | VALIDATION | — | — | — |
| CAP-209 | 209 | 1 | — | v0.13 — 19. The generic blind-scan analogy is now much stronger | DVB_ANALOGY | — | — | — |
| CAP-210 | 210 | 1 | — | v0.13 — 20. v0.13 invariants | VALIDATION | — | — | — |
| CAP-211 | 211 | 3 | 20. v0.13 invariants | v0.13 — D1 — Source isolation | VALIDATION | — | — | — |
| CAP-212 | 212 | 3 | 20. v0.13 invariants | v0.13 — D2 — Acquisition isolation | ACQUISITION | — | — | — |
| CAP-213 | 213 | 3 | 20. v0.13 invariants | v0.13 — D3 — Normalization ownership | VALIDATION | — | — | — |
| CAP-214 | 214 | 3 | 20. v0.13 invariants | v0.13 — D4 — Bounded generation | VALIDATION | — | — | — |
| CAP-215 | 215 | 3 | 20. v0.13 invariants | v0.13 — D5 — Bounded recursion | VALIDATION | — | — | — |
| CAP-216 | 216 | 3 | 20. v0.13 invariants | v0.13 — D6 — Provenance preservation | PROVENANCE | — | — | — |
| CAP-217 | 217 | 3 | 20. v0.13 invariants | v0.13 — D7 — Atomic task claiming | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-218 | 218 | 3 | 20. v0.13 invariants | v0.13 — D8 — Convergence | VALIDATION | — | — | — |
| CAP-219 | 219 | 3 | 20. v0.13 invariants | v0.13 — D9 — Discovery/acquisition independence | ACQUISITION | — | — | — |
| CAP-220 | 220 | 1 | — | v0.13 — 21. The architecture is now approaching a stable core | ARCHITECTURE | — | — | — |
| CAP-221 | 221 | 1 | — | v0.14 — the next missing abstraction | ROADMAP | — | — | — |
| CAP-222 | 222 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-223 | 223 | 1 | — | v0.14 — DiscoveryDomain + ScanSession | ARCHITECTURE | — | — | — |
| CAP-224 | 224 | 1 | — | v0.14 — 1. The conceptual split | ARCHITECTURE | — | — | — |
| CAP-225 | 225 | 3 | 1. The conceptual split | v0.14 — Discovery Engine | DISCOVERY | — | — | — |
| CAP-226 | 226 | 3 | 1. The conceptual split | v0.14 — DiscoveryDomain | ARCHITECTURE | — | — | — |
| CAP-227 | 227 | 3 | 1. The conceptual split | v0.14 — ScanSession | ARCHITECTURE | — | — | — |
| CAP-228 | 228 | 1 | — | v0.14 — 2. DVB analogy | DVB_ANALOGY | — | — | — |
| CAP-229 | 229 | 1 | — | v0.14 — 3. DiscoveryDomain | ARCHITECTURE | — | — | — |
| CAP-230 | 230 | 1 | — | v0.14 — 4. Domain vs policy | SECURITY | — | [C-11](REVIEW-NOTES.md#c-11--same-origin-default-versus-cross-origin-capability) | — |
| CAP-231 | 231 | 1 | — | v0.14 — 5. Domain membership | ARCHITECTURE | — | — | — |
| CAP-232 | 232 | 1 | — | v0.14 — 6. Explicit seeds | ARCHITECTURE | — | — | — |
| CAP-233 | 233 | 1 | — | v0.14 — 7. Seed ≠ Candidate | CANDIDATE | — | — | — |
| CAP-234 | 234 | 1 | — | v0.14 — 8. Discovery frontier | DISCOVERY | — | — | — |
| CAP-235 | 235 | 1 | — | v0.14 — 9. ScanSession | ARCHITECTURE | — | — | — |
| CAP-236 | 236 | 1 | — | v0.14 — 10. Session lifecycle | ARCHITECTURE | — | — | — |
| CAP-237 | 237 | 1 | — | v0.14 — 11. Termination becomes explicit | ARCHITECTURE | — | [C-09](REVIEW-NOTES.md#c-09--two-termination-taxonomies) | — |
| CAP-238 | 238 | 3 | 11. Termination becomes explicit | v0.14 — Frontier exhaustion | ARCHITECTURE | — | — | explicit override |
| CAP-239 | 239 | 3 | 11. Termination becomes explicit | v0.14 — Candidate limit | CANDIDATE | — | — | explicit override |
| CAP-240 | 240 | 3 | 11. Termination becomes explicit | v0.14 — Acquisition limit | ACQUISITION | — | — | explicit override |
| CAP-241 | 241 | 3 | 11. Termination becomes explicit | v0.14 — Discovery-task limit | DISCOVERY | — | — | explicit override |
| CAP-242 | 242 | 3 | 11. Termination becomes explicit | v0.14 — Proposal limit | ARCHITECTURE | — | — | — |
| CAP-243 | 243 | 3 | 11. Termination becomes explicit | v0.14 — Depth limit | ARCHITECTURE | — | — | — |
| CAP-244 | 244 | 3 | 11. Termination becomes explicit | v0.14 — Time limit | ARCHITECTURE | — | — | — |
| CAP-245 | 245 | 3 | 11. Termination becomes explicit | v0.14 — External stop | ARCHITECTURE | — | — | — |
| CAP-246 | 246 | 1 | — | v0.14 — 12. Termination evaluator | ARCHITECTURE | — | [C-09](REVIEW-NOTES.md#c-09--two-termination-taxonomies) | — |
| CAP-247 | 247 | 1 | — | v0.14 — 13. Limit reached ≠ successful completion | ARCHITECTURE | — | — | — |
| CAP-248 | 248 | 1 | — | v0.14 — 14. The session snapshot | ARCHITECTURE | — | — | — |
| CAP-249 | 249 | 1 | — | v0.14 — 15. Resumability | ARCHITECTURE | — | — | — |
| CAP-250 | 250 | 1 | — | v0.14 — 16. Lease-based claims | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-251 | 251 | 1 | — | v0.14 — 17. Session ownership | ARCHITECTURE | — | — | — |
| CAP-252 | 252 | 1 | — | v0.14 — 18. Scan vs engine knowledge | ARCHITECTURE | — | [C-10](REVIEW-NOTES.md#c-10--knowledge-store-naming) | — |
| CAP-253 | 253 | 1 | — | v0.14 — 19. Domain snapshot vs mutable domain | ARCHITECTURE | — | — | — |
| CAP-254 | 254 | 1 | — | v0.14 — 20. Domain identity | ARCHITECTURE | — | [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution) | — |
| CAP-255 | 255 | 1 | — | v0.14 — 21. Search frontier vs knowledge graph | ARCHITECTURE | — | [C-10](REVIEW-NOTES.md#c-10--knowledge-store-naming) | — |
| CAP-256 | 256 | 1 | — | v0.14 — 22. The complete v0.14 architecture | ARCHITECTURE | — | — | — |
| CAP-257 | 257 | 1 | — | v0.14 — 23. Four distinct scopes | SCOPE | — | — | — |
| CAP-258 | 258 | 1 | — | v0.14 — 24. Strong invariants | VALIDATION | — | — | — |
| CAP-259 | 259 | 3 | 24. Strong invariants | v0.14 — Domain invariant | VALIDATION | — | — | — |
| CAP-260 | 260 | 3 | 24. Strong invariants | v0.14 — Session invariant | VALIDATION | — | — | — |
| CAP-261 | 261 | 3 | 24. Strong invariants | v0.14 — Snapshot invariant | VALIDATION | — | — | — |
| CAP-262 | 262 | 3 | 24. Strong invariants | v0.14 — Frontier invariant | VALIDATION | — | — | — |
| CAP-263 | 263 | 3 | 24. Strong invariants | v0.14 — Termination invariant | VALIDATION | — | [C-09](REVIEW-NOTES.md#c-09--two-termination-taxonomies) | — |
| CAP-264 | 264 | 3 | 24. Strong invariants | v0.14 — Recovery invariant | VALIDATION | — | — | — |
| CAP-265 | 265 | 3 | 24. Strong invariants | v0.14 — Provenance invariant | PROVENANCE | — | — | — |
| CAP-266 | 266 | 3 | 24. Strong invariants | v0.14 — Acquisition invariant | ACQUISITION | — | — | — |
| CAP-267 | 267 | 3 | 24. Strong invariants | v0.14 — Discovery invariant | VALIDATION | — | — | — |
| CAP-268 | 268 | 1 | — | v0.14 — 25. Failure taxonomy | VALIDATION | — | — | — |
| CAP-269 | 269 | 1 | — | v0.14 — 26. What v0.14 changes conceptually | ARCHITECTURE | — | — | — |
| CAP-270 | 270 | 1 | — | v0.14 — 27. The next abstraction | ROADMAP | — | — | — |
| CAP-271 | 271 | 1 | — | v0.15 — WorkItem + Frontier Runtime | SCHEDULING | — | — | — |
| CAP-272 | 272 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-273 | 273 | 1 | — | v0.15 — WorkItem + Frontier Runtime | SCHEDULING | — | — | — |
| CAP-274 | 274 | 1 | — | v0.15 — 1. The key distinction | SCHEDULING | — | — | — |
| CAP-275 | 275 | 1 | — | v0.15 — 2. Why `WorkItem` exists | SCHEDULING | — | — | — |
| CAP-276 | 276 | 1 | — | v0.15 — 3. WorkItem | SCHEDULING | — | — | — |
| CAP-277 | 277 | 1 | — | v0.15 — 4. Work kinds | SCHEDULING | — | — | — |
| CAP-278 | 278 | 1 | — | v0.15 — 5. Work payload | SCHEDULING | — | — | — |
| CAP-279 | 279 | 1 | — | v0.15 — 6. Work lifecycle | SCHEDULING | — | — | — |
| CAP-280 | 280 | 1 | — | v0.15 — 7. Claiming becomes a formal protocol | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-281 | 281 | 1 | — | v0.15 — 8. Work lease | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-282 | 282 | 1 | — | v0.15 — 9. Lease recovery | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-283 | 283 | 1 | — | v0.15 — 10. Frontier Runtime | SCHEDULING | — | — | — |
| CAP-284 | 284 | 1 | — | v0.15 — 11. WorkScheduler | SCHEDULING | — | — | — |
| CAP-285 | 285 | 1 | — | v0.15 — 12. Priority starvation | SCHEDULING | — | — | — |
| CAP-286 | 286 | 1 | — | v0.15 — 13. Priority aging | SCHEDULING | — | — | — |
| CAP-287 | 287 | 1 | — | v0.15 — 14. Discovery and acquisition fairness | SCHEDULING | — | — | — |
| CAP-288 | 288 | 1 | — | v0.15 — 15. Why not one giant queue? | SCHEDULING | — | — | — |
| CAP-289 | 289 | 1 | — | v0.15 — 16. Work dependencies | SCHEDULING | — | — | — |
| CAP-290 | 290 | 1 | — | v0.15 — 17. But dependencies must not create hidden coupling | SCHEDULING | — | — | — |
| CAP-291 | 291 | 1 | — | v0.15 — 18. Dependency states | SCHEDULING | — | — | — |
| CAP-292 | 292 | 1 | — | v0.15 — 19. Work completion | SCHEDULING | — | — | — |
| CAP-293 | 293 | 1 | — | v0.15 — 20. Work execution boundary | SCHEDULING | — | — | — |
| CAP-294 | 294 | 1 | — | v0.15 — 21. Work Runtime | SCHEDULING | — | — | — |
| CAP-295 | 295 | 1 | — | v0.15 — 22. Retry becomes generic | SCHEDULING | — | — | — |
| CAP-296 | 296 | 1 | — | v0.15 — 23. Retry identity | SCHEDULING | — | [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution) | — |
| CAP-297 | 297 | 1 | — | v0.15 — 24. Cancellation | SCHEDULING | — | — | — |
| CAP-298 | 298 | 1 | — | v0.15 — 25. Scan termination with WorkItems | SCHEDULING | — | [C-09](REVIEW-NOTES.md#c-09--two-termination-taxonomies) | — |
| CAP-299 | 299 | 1 | — | v0.15 — 26. The three frontier states | SCHEDULING | — | — | — |
| CAP-300 | 300 | 1 | — | v0.15 — 27. Scheduled work | SCHEDULING | — | — | — |
| CAP-301 | 301 | 1 | — | v0.15 — 28. Work state machine | SCHEDULING | — | — | — |
| CAP-302 | 302 | 1 | — | v0.15 — 29. Domain → Session → Work | SCHEDULING | — | — | — |
| CAP-303 | 303 | 1 | — | v0.15 — 30. What belongs where? | SCHEDULING | — | — | — |
| CAP-304 | 304 | 1 | — | v0.15 — 31. The crucial invariant | VALIDATION | — | — | — |
| CAP-305 | 305 | 1 | — | v0.15 — 32. Discovery vs acquisition remains intact | ACQUISITION | — | — | — |
| CAP-306 | 306 | 1 | — | v0.15 — 33. The resulting architecture | ARCHITECTURE | — | — | — |
| CAP-307 | 307 | 1 | — | v0.15 — 34. v0.15 architectural result | SCHEDULING | — | — | — |
| CAP-308 | 308 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-309 | 309 | 1 | — | v0.16 — EvidenceGraph + Provenance | PROVENANCE | — | — | — |
| CAP-310 | 310 | 1 | — | v0.16 — 1. The new abstraction | DATA_MODEL | — | — | — |
| CAP-311 | 311 | 1 | — | v0.16 — 2. Observation ≠ Evidence ≠ Claim | OBSERVATION | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-312 | 312 | 3 | 2. Observation ≠ Evidence ≠ Claim | v0.16 — Observation | OBSERVATION | — | — | — |
| CAP-313 | 313 | 3 | 2. Observation ≠ Evidence ≠ Claim | v0.16 — Evidence | DATA_MODEL | — | — | — |
| CAP-314 | 314 | 3 | 2. Observation ≠ Evidence ≠ Claim | v0.16 — Claim | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-315 | 315 | 1 | — | v0.16 — 3. Resource ≠ Claim | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-316 | 316 | 1 | — | v0.16 — 4. EvidenceGraph | DATA_MODEL | — | — | — |
| CAP-317 | 317 | 1 | — | v0.16 — 5. Provenance | PROVENANCE | — | — | — |
| CAP-318 | 318 | 1 | — | v0.16 — 6. Evidence object | DATA_MODEL | — | — | — |
| CAP-319 | 319 | 1 | — | v0.16 — 7. Locator | DATA_MODEL | — | — | — |
| CAP-320 | 320 | 1 | — | v0.16 — 8. Claim | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-321 | 321 | 1 | — | v0.16 — 9. Claims should not be confused with truth | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-322 | 322 | 1 | — | v0.16 — 10. Evidence strength | DATA_MODEL | — | — | — |
| CAP-323 | 323 | 1 | — | v0.16 — 11. Independent evidence | DATA_MODEL | — | — | — |
| CAP-324 | 324 | 1 | — | v0.16 — 12. Evidence independence | DATA_MODEL | — | — | — |
| CAP-325 | 325 | 1 | — | v0.16 — 13. Evidence graph edges | DATA_MODEL | — | — | — |
| CAP-326 | 326 | 1 | — | v0.16 — 14. Why graph edges matter | DATA_MODEL | — | — | — |
| CAP-327 | 327 | 1 | — | v0.16 — 15. Provenance graph | PROVENANCE | — | — | — |
| CAP-328 | 328 | 1 | — | v0.16 — 16. Resource identity | DATA_MODEL | — | [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution) | — |
| CAP-329 | 329 | 1 | — | v0.16 — 17. Resource fingerprint | DATA_MODEL | — | [C-07](REVIEW-NOTES.md#c-07--resource--artifact-model-revised) | — |
| CAP-330 | 330 | 1 | — | v0.16 — 18. URL identity vs content identity | DATA_MODEL | — | [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution) | — |
| CAP-331 | 331 | 1 | — | v0.16 — 19. Revision detection | DATA_MODEL | — | [C-07](REVIEW-NOTES.md#c-07--resource--artifact-model-revised) | — |
| CAP-332 | 332 | 1 | — | v0.16 — 20. Observation immutability | OBSERVATION | — | — | — |
| CAP-333 | 333 | 1 | — | v0.16 — 21. Evidence immutability | DATA_MODEL | — | — | — |
| CAP-334 | 334 | 1 | — | v0.16 — 22. Extraction method becomes first-class | DATA_MODEL | — | — | — |
| CAP-335 | 335 | 1 | — | v0.16 — 23. Verification | VALIDATION | — | — | — |
| CAP-336 | 336 | 1 | — | v0.16 — 24. Evidence lifecycle | DATA_MODEL | — | — | — |
| CAP-337 | 337 | 1 | — | v0.16 — 25. Evidence states | DATA_MODEL | — | — | — |
| CAP-338 | 338 | 1 | — | v0.16 — 26. Claims can conflict | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-339 | 339 | 1 | — | v0.16 — 27. Evidence resolution | DATA_MODEL | — | — | — |
| CAP-340 | 340 | 1 | — | v0.16 — 28. Discovery confidence changes meaning | DISCOVERY | — | [C-06](REVIEW-NOTES.md#c-06--confidence-one-score-versus-no-single-global-score) | — |
| CAP-341 | 341 | 1 | — | v0.16 — 29. Candidate provenance | PROVENANCE | — | — | — |
| CAP-342 | 342 | 1 | — | v0.16 — 30. The evidence ledger | DATA_MODEL | — | — | — |
| CAP-343 | 343 | 1 | — | v0.16 — 31. Two complementary graphs | DATA_MODEL | — | — | — |
| CAP-344 | 344 | 1 | — | v0.16 — 32. Example end-to-end trace | DATA_MODEL | — | — | — |
| CAP-345 | 345 | 1 | — | v0.16 — 33. v0.16 architecture | ARCHITECTURE | — | — | — |
| CAP-346 | 346 | 1 | — | v0.16 — 34. New invariants | VALIDATION | — | — | — |
| CAP-347 | 347 | 3 | 34. New invariants | v0.16 — Evidence provenance | PROVENANCE | — | — | — |
| CAP-348 | 348 | 3 | 34. New invariants | v0.16 — Claim support | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-349 | 349 | 3 | 34. New invariants | v0.16 — Historical integrity | DATA_MODEL | — | — | — |
| CAP-350 | 350 | 3 | 34. New invariants | v0.16 — Extraction integrity | DATA_MODEL | — | — | — |
| CAP-351 | 351 | 3 | 34. New invariants | v0.16 — Resource identity | DATA_MODEL | — | [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution) | — |
| CAP-352 | 352 | 3 | 34. New invariants | v0.16 — Content identity | DATA_MODEL | — | [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution) | — |
| CAP-353 | 353 | 3 | 34. New invariants | v0.16 — Conflict preservation | DATA_MODEL | — | — | — |
| CAP-354 | 354 | 3 | 34. New invariants | v0.16 — Provenance preservation | PROVENANCE | — | — | — |
| CAP-355 | 355 | 3 | 34. New invariants | v0.16 — Session provenance | PROVENANCE | — | — | — |
| CAP-356 | 356 | 1 | — | v0.16 — 35. Failure taxonomy | VALIDATION | — | — | — |
| CAP-357 | 357 | 1 | — | v0.16 — 36. The deeper architectural transition | ROADMAP | — | — | — |
| CAP-358 | 358 | 1 | — | v0.16 — 37. What is still missing | ROADMAP | — | — | — |
| CAP-359 | 359 | 3 | 37. What is still missing | v0.16 — Search space | ARCHITECTURE | — | — | — |
| CAP-360 | 360 | 3 | 37. What is still missing | v0.16 — Execution | DATA_MODEL | — | — | — |
| CAP-361 | 361 | 3 | 37. What is still missing | v0.16 — Work | DATA_MODEL | — | — | — |
| CAP-362 | 362 | 3 | 37. What is still missing | v0.16 — Acquisition | ACQUISITION | — | — | — |
| CAP-363 | 363 | 3 | 37. What is still missing | v0.16 — Recognition | ACQUISITION | — | [C-02](REVIEW-NOTES.md#c-02--the-discovery-pipeline-is-described-with-two-different-step-sets) | — |
| CAP-364 | 364 | 3 | 37. What is still missing | v0.16 — Discovery | DISCOVERY | — | — | — |
| CAP-365 | 365 | 3 | 37. What is still missing | v0.16 — Evidence | DATA_MODEL | — | — | — |
| CAP-366 | 366 | 3 | 37. What is still missing | v0.16 — History | DATA_MODEL | — | — | — |
| CAP-367 | 367 | 1 | — | v0.17 — ResourceGraph + Identity Resolution | DATA_MODEL | — | [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution) | — |
| CAP-368 | 368 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-369 | 369 | 1 | — | v0.17 — ResourceGraph + Identity Resolution | DATA_MODEL | — | [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution) | — |
| CAP-370 | 370 | 1 | — | v0.17 — 1. The core problem | DATA_MODEL | — | — | — |
| CAP-371 | 371 | 1 | — | v0.17 — 2. Resource identity must become graph-based | DATA_MODEL | — | [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution) | — |
| CAP-372 | 372 | 1 | — | v0.17 — 3. Candidate vs Resource vs Locator | CANDIDATE | — | — | — |
| CAP-373 | 373 | 3 | 3. Candidate vs Resource vs Locator | v0.17 — Candidate | CANDIDATE | — | — | — |
| CAP-374 | 374 | 3 | 3. Candidate vs Resource vs Locator | v0.17 — Locator | DATA_MODEL | — | — | — |
| CAP-375 | 375 | 3 | 3. Candidate vs Resource vs Locator | v0.17 — Resource | DATA_MODEL | — | — | — |
| CAP-376 | 376 | 1 | — | v0.17 — 4. Why not simply canonicalize everything? | DATA_MODEL | — | [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution) | — |
| CAP-377 | 377 | 1 | — | v0.17 — 5. Locator | DATA_MODEL | — | — | — |
| CAP-378 | 378 | 1 | — | v0.17 — 6. Resource | DATA_MODEL | — | — | — |
| CAP-379 | 379 | 1 | — | v0.17 — 7. Resource relationships | DATA_MODEL | — | — | — |
| CAP-380 | 380 | 1 | — | v0.17 — 8. Redirects | DATA_MODEL | — | — | — |
| CAP-381 | 381 | 1 | — | v0.17 — 9. Redirect chain | DATA_MODEL | — | — | — |
| CAP-382 | 382 | 1 | — | v0.17 — 10. Content fingerprints | DATA_MODEL | — | [C-07](REVIEW-NOTES.md#c-07--resource--artifact-model-revised) | — |
| CAP-383 | 383 | 1 | — | v0.17 — 11. Same content does not prove same resource | DATA_MODEL | — | — | — |
| CAP-384 | 384 | 1 | — | v0.17 — 12. Representation identity | DATA_MODEL | — | [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution) | — |
| CAP-385 | 385 | 1 | — | v0.17 — 13. Identity Evidence | DATA_MODEL | — | [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution) | — |
| CAP-386 | 386 | 1 | — | v0.17 — 14. IdentityResolver | DATA_MODEL | — | — | — |
| CAP-387 | 387 | 1 | — | v0.17 — 15. Identity confidence should be relational | DATA_MODEL | — | [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution), [C-06](REVIEW-NOTES.md#c-06--confidence-one-score-versus-no-single-global-score) | — |
| CAP-388 | 388 | 1 | — | v0.17 — 16. Identity classes | DATA_MODEL | — | [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution) | — |
| CAP-389 | 389 | 1 | — | v0.17 — 17. No destructive merges | DATA_MODEL | — | — | — |
| CAP-390 | 390 | 1 | — | v0.17 — 18. ResourceGraph | DATA_MODEL | — | — | — |
| CAP-391 | 391 | 1 | — | v0.17 — 19. Graph edge contract | DATA_MODEL | — | — | — |
| CAP-392 | 392 | 1 | — | v0.17 — 20. Identity resolution pipeline | DATA_MODEL | — | [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution) | — |
| CAP-393 | 393 | 1 | — | v0.17 — 21. Canonical URL is still important | DATA_MODEL | — | [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution) | — |
| CAP-394 | 394 | 1 | — | v0.17 — 22. Canonicalization provenance | PROVENANCE | — | [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution) | — |
| CAP-395 | 395 | 1 | — | v0.17 — 23. Identity resolution must be monotonic where possible | DATA_MODEL | — | [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution) | — |
| CAP-396 | 396 | 1 | — | v0.17 — 24. Resource revisions | DATA_MODEL | — | [C-07](REVIEW-NOTES.md#c-07--resource--artifact-model-revised) | — |
| CAP-397 | 397 | 1 | — | v0.17 — 25. Revision object | DATA_MODEL | — | [C-07](REVIEW-NOTES.md#c-07--resource--artifact-model-revised) | — |
| CAP-398 | 398 | 1 | — | v0.17 — 26. ResourceGraph vs KnowledgeBase | DATA_MODEL | — | [C-10](REVIEW-NOTES.md#c-10--knowledge-store-naming) | — |
| CAP-399 | 399 | 1 | — | v0.17 — 27. Querying the graph | ALGORITHM | — | — | — |
| CAP-400 | 400 | 3 | 27. Querying the graph | v0.17 — What URLs identify this resource? | DATA_MODEL | — | — | — |
| CAP-401 | 401 | 3 | 27. Querying the graph | v0.17 — Where was it discovered? | DATA_MODEL | — | — | — |
| CAP-402 | 402 | 3 | 27. Querying the graph | v0.17 — What URLs redirect to it? | DATA_MODEL | — | — | — |
| CAP-403 | 403 | 3 | 27. Querying the graph | v0.17 — Which URLs have identical observed bytes? | DATA_MODEL | — | — | — |
| CAP-404 | 404 | 3 | 27. Querying the graph | v0.17 — Has this resource changed? | DATA_MODEL | — | — | — |
| CAP-405 | 405 | 3 | 27. Querying the graph | v0.17 — Why do we believe two URLs are related? | DATA_MODEL | — | — | — |
| CAP-406 | 406 | 1 | — | v0.17 — 28. Resource graph example | DATA_MODEL | — | — | — |
| CAP-407 | 407 | 1 | — | v0.17 — 29. Failure taxonomy | VALIDATION | — | — | — |
| CAP-408 | 408 | 1 | — | v0.17 — 30. Core invariants | VALIDATION | — | — | — |
| CAP-409 | 409 | 3 | 30. Core invariants | v0.17 — Locator preservation | DATA_MODEL | — | — | — |
| CAP-410 | 410 | 3 | 30. Core invariants | v0.17 — No destructive merge | DATA_MODEL | — | — | — |
| CAP-411 | 411 | 3 | 30. Core invariants | v0.17 — Fingerprint independence | DATA_MODEL | — | [C-07](REVIEW-NOTES.md#c-07--resource--artifact-model-revised) | — |
| CAP-412 | 412 | 3 | 30. Core invariants | v0.17 — Redirect independence | DATA_MODEL | — | — | — |
| CAP-413 | 413 | 3 | 30. Core invariants | v0.17 — Evidence-backed identity | DATA_MODEL | — | [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution) | — |
| CAP-414 | 414 | 3 | 30. Core invariants | v0.17 — Revision preservation | DATA_MODEL | — | [C-07](REVIEW-NOTES.md#c-07--resource--artifact-model-revised) | — |
| CAP-415 | 415 | 3 | 30. Core invariants | v0.17 — Canonicalization transparency | DATA_MODEL | — | [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution) | — |
| CAP-416 | 416 | 1 | — | v0.17 — 31. The new architecture | ARCHITECTURE | — | — | — |
| CAP-417 | 417 | 1 | — | v0.17 — 32. The deeper model | CONCEPT | — | — | — |
| CAP-418 | 418 | 1 | — | v0.17 — 33. The important transition | DATA_MODEL | — | — | — |
| CAP-419 | 419 | 1 | — | v0.17 — 34. Next missing abstraction | ROADMAP | — | — | — |
| CAP-420 | 420 | 1 | — | v0.18 — Resource Type System + Semantic Classification | DATA_MODEL | — | — | — |
| CAP-421 | 421 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-422 | 422 | 1 | — | v0.18 — Resource Type System + Semantic Classification | DATA_MODEL | — | — | — |
| CAP-423 | 423 | 1 | — | v0.18 — 18.1 The Type Problem | DATA_MODEL | — | — | — |
| CAP-424 | 424 | 1 | — | v0.18 — 18.2 Four Orthogonal Type Dimensions | DATA_MODEL | — | — | — |
| CAP-425 | 425 | 1 | — | v0.18 — 18.3 ResourceType | DATA_MODEL | — | — | — |
| CAP-426 | 426 | 1 | — | v0.18 — 18.4 Classification Assertion | DATA_MODEL | — | — | — |
| CAP-427 | 427 | 1 | — | v0.18 — 18.5 Type Evidence | DATA_MODEL | — | — | — |
| CAP-428 | 428 | 1 | — | v0.18 — 18.6 Evidence Strength Must Be Axis-Specific | DATA_MODEL | — | — | — |
| CAP-429 | 429 | 1 | — | v0.18 — 18.7 Classification Pipeline | DATA_MODEL | — | — | — |
| CAP-430 | 430 | 1 | — | v0.18 — 18.8 Recognition vs Classification | DATA_MODEL | — | [C-02](REVIEW-NOTES.md#c-02--the-discovery-pipeline-is-described-with-two-different-step-sets) | — |
| CAP-431 | 431 | 3 | 18.8 Recognition vs Classification | v0.18 — Recognition | DATA_MODEL | — | [C-02](REVIEW-NOTES.md#c-02--the-discovery-pipeline-is-described-with-two-different-step-sets) | — |
| CAP-432 | 432 | 3 | 18.8 Recognition vs Classification | v0.18 — Classification | DATA_MODEL | — | — | — |
| CAP-433 | 433 | 1 | — | v0.18 — 18.9 Classification Runtime | DATA_MODEL | — | — | — |
| CAP-434 | 434 | 1 | — | v0.18 — 18.10 Example Classifiers | DATA_MODEL | — | — | — |
| CAP-435 | 435 | 1 | — | v0.18 — 18.11 Hierarchical Classification | DATA_MODEL | — | — | — |
| CAP-436 | 436 | 1 | — | v0.18 — 18.12 Do Not Use One Global Confidence Score | DATA_MODEL | — | [C-06](REVIEW-NOTES.md#c-06--confidence-one-score-versus-no-single-global-score) | — |
| CAP-437 | 437 | 1 | — | v0.18 — 18.13 Classification Is Versioned | DATA_MODEL | — | — | — |
| CAP-438 | 438 | 1 | — | v0.18 — 18.14 Contradictory Classification | DATA_MODEL | — | — | — |
| CAP-439 | 439 | 1 | — | v0.18 — 18.15 Classification Graph | DATA_MODEL | — | — | — |
| CAP-440 | 440 | 1 | — | v0.18 — 18.16 Resource Model After v0.18 | DATA_MODEL | — | — | — |
| CAP-441 | 441 | 1 | — | v0.18 — 18.17 Resource Type Registry | DATA_MODEL | — | — | — |
| CAP-442 | 442 | 1 | — | v0.18 — 18.18 Classification Must Not Become Acquisition Policy | SECURITY | — | [C-11](REVIEW-NOTES.md#c-11--same-origin-default-versus-cross-origin-capability) | — |
| CAP-443 | 443 | 1 | — | v0.18 — 18.19 Classification → Strategy | ALGORITHM | — | — | — |
| CAP-444 | 444 | 1 | — | v0.18 — 18.20 Classification Work as WorkItem | DATA_MODEL | — | — | — |
| CAP-445 | 445 | 1 | — | v0.18 — 18.21 End-to-End Architecture | ARCHITECTURE | — | — | — |
| CAP-446 | 446 | 1 | — | v0.18 — 18.22 Failure Taxonomy | VALIDATION | — | — | — |
| CAP-447 | 447 | 1 | — | v0.18 — 18.23 Core Invariants | VALIDATION | — | — | — |
| CAP-448 | 448 | 3 | 18.23 Core Invariants | v0.18 — Invariant 1 — Type is not identity | VALIDATION | — | [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution) | — |
| CAP-449 | 449 | 3 | 18.23 Core Invariants | v0.18 — Invariant 2 — URL does not determine semantic type | VALIDATION | — | — | — |
| CAP-450 | 450 | 3 | 18.23 Core Invariants | v0.18 — Invariant 3 — Technical recognition does not determine semantic role | VALIDATION | — | [C-02](REVIEW-NOTES.md#c-02--the-discovery-pipeline-is-described-with-two-different-step-sets) | — |
| CAP-451 | 451 | 3 | 18.23 Core Invariants | v0.18 — Invariant 4 — Classification requires evidence | VALIDATION | — | — | — |
| CAP-452 | 452 | 3 | 18.23 Core Invariants | v0.18 — Invariant 5 — Classification does not imply authorization | VALIDATION | — | — | — |
| CAP-453 | 453 | 3 | 18.23 Core Invariants | v0.18 — Invariant 6 — Historical classification is immutable | VALIDATION | — | — | — |
| CAP-454 | 454 | 3 | 18.23 Core Invariants | v0.18 — Invariant 7 — Contradiction is preserved | VALIDATION | — | — | — |
| CAP-455 | 455 | 3 | 18.23 Core Invariants | v0.18 — Invariant 8 — Type axes remain independent | VALIDATION | — | — | — |
| CAP-456 | 456 | 1 | — | v0.18 — 18.24 The Larger Concept | CONCEPT | — | — | — |
| CAP-457 | 457 | 1 | — | v0.19 — Resource Representation & Revision Model | DATA_MODEL | — | [C-07](REVIEW-NOTES.md#c-07--resource--artifact-model-revised) | — |
| CAP-458 | 458 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-459 | 459 | 1 | — | v0.19 — Resource Representation + Artifact + Revision Model | DATA_MODEL | — | [C-07](REVIEW-NOTES.md#c-07--resource--artifact-model-revised) | — |
| CAP-460 | 460 | 2 | v0.19 — Resource Representation + Artifact + Revision Model | v0.19 — 19.1 The Core Distinction | DATA_MODEL | — | — | — |
| CAP-461 | 461 | 3 | 19.1 The Core Distinction | v0.19 — Resource | DATA_MODEL | — | — | — |
| CAP-462 | 462 | 3 | 19.1 The Core Distinction | v0.19 — Representation | DATA_MODEL | — | — | — |
| CAP-463 | 463 | 3 | 19.1 The Core Distinction | v0.19 — Artifact | DATA_MODEL | — | [C-07](REVIEW-NOTES.md#c-07--resource--artifact-model-revised) | — |
| CAP-464 | 464 | 3 | 19.1 The Core Distinction | v0.19 — Observation | OBSERVATION | — | — | — |
| CAP-465 | 465 | 1 | — | v0.19 — 19.2 Why Resource → Artifact Is Wrong | DATA_MODEL | — | [C-07](REVIEW-NOTES.md#c-07--resource--artifact-model-revised) | — |
| CAP-466 | 466 | 1 | — | v0.19 — 19.3 New Data Model | DATA_MODEL | — | — | — |
| CAP-467 | 467 | 1 | — | v0.19 — 19.4 The Complete Identity Chain | DATA_MODEL | — | [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution) | — |
| CAP-468 | 468 | 1 | — | v0.19 — 19.5 Representation Is Not Just MIME | DATA_MODEL | — | — | — |
| CAP-469 | 469 | 1 | — | v0.19 — 19.6 Representation Relations | DATA_MODEL | — | — | — |
| CAP-470 | 470 | 1 | — | v0.19 — 19.7 Artifact Identity | DATA_MODEL | — | [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution), [C-07](REVIEW-NOTES.md#c-07--resource--artifact-model-revised) | — |
| CAP-471 | 471 | 1 | — | v0.19 — 19.8 Content Equivalence | DATA_MODEL | — | — | — |
| CAP-472 | 472 | 1 | — | v0.19 — 19.9 Revision Detection | DATA_MODEL | — | [C-07](REVIEW-NOTES.md#c-07--resource--artifact-model-revised) | — |
| CAP-473 | 473 | 1 | — | v0.19 — 19.10 Revision Detection Is Not Always Proof of Semantic Revision | DATA_MODEL | — | [C-07](REVIEW-NOTES.md#c-07--resource--artifact-model-revised) | — |
| CAP-474 | 474 | 1 | — | v0.19 — 19.11 Revision Evidence | DATA_MODEL | — | [C-07](REVIEW-NOTES.md#c-07--resource--artifact-model-revised) | — |
| CAP-475 | 475 | 1 | — | v0.19 — 19.12 HTTP Validators Become Evidence | DATA_MODEL | — | — | — |
| CAP-476 | 476 | 1 | — | v0.19 — 19.13 Conditional Acquisition | ACQUISITION | — | — | — |
| CAP-477 | 477 | 1 | — | v0.19 — 19.14 Observation Becomes the Historical Bridge | OBSERVATION | — | — | — |
| CAP-478 | 478 | 1 | — | v0.19 — 19.15 Resource State vs Artifact State | DATA_MODEL | — | [C-07](REVIEW-NOTES.md#c-07--resource--artifact-model-revised) | — |
| CAP-479 | 479 | 3 | 19.15 Resource State vs Artifact State | v0.19 — Resource state | DATA_MODEL | — | — | — |
| CAP-480 | 480 | 3 | 19.15 Resource State vs Artifact State | v0.19 — Artifact state | DATA_MODEL | — | [C-07](REVIEW-NOTES.md#c-07--resource--artifact-model-revised) | — |
| CAP-481 | 481 | 3 | 19.15 Resource State vs Artifact State | v0.19 — Observation state | OBSERVATION | — | — | — |
| CAP-482 | 482 | 1 | — | v0.19 — 19.16 ResourceGraph v0.19 | DATA_MODEL | — | — | — |
| CAP-483 | 483 | 1 | — | v0.19 — 19.17 ResourceGraph API | DATA_MODEL | — | — | — |
| CAP-484 | 484 | 1 | — | v0.19 — 19.18 Artifact Deduplication | DATA_MODEL | — | [C-07](REVIEW-NOTES.md#c-07--resource--artifact-model-revised) | — |
| CAP-485 | 485 | 3 | 19.18 Artifact Deduplication | v0.19 — Locator deduplication | DATA_MODEL | — | — | — |
| CAP-486 | 486 | 3 | 19.18 Artifact Deduplication | v0.19 — Artifact deduplication | DATA_MODEL | — | [C-07](REVIEW-NOTES.md#c-07--resource--artifact-model-revised) | — |
| CAP-487 | 487 | 1 | — | v0.19 — 19.19 Content-Addressed Storage | DATA_MODEL | — | — | — |
| CAP-488 | 488 | 1 | — | v0.19 — 19.20 Verification Levels | VALIDATION | — | — | — |
| CAP-489 | 489 | 1 | — | v0.19 — 19.21 Independent Confirmation | DATA_MODEL | — | — | — |
| CAP-490 | 490 | 1 | — | v0.19 — 19.22 Resource Confidence | DATA_MODEL | — | [C-06](REVIEW-NOTES.md#c-06--confidence-one-score-versus-no-single-global-score) | — |
| CAP-491 | 491 | 1 | — | v0.19 — 19.23 Example | DATA_MODEL | — | — | — |
| CAP-492 | 492 | 3 | 19.23 Example | v0.19 — Step 1 — Locator | EXAMPLE | — | — | — |
| CAP-493 | 493 | 3 | 19.23 Example | v0.19 — Step 2 — Resource | EXAMPLE | — | — | — |
| CAP-494 | 494 | 3 | 19.23 Example | v0.19 — Step 3 — Observation | OBSERVATION | — | — | — |
| CAP-495 | 495 | 3 | 19.23 Example | v0.19 — Step 4 — Artifact | EXAMPLE | — | [C-07](REVIEW-NOTES.md#c-07--resource--artifact-model-revised) | — |
| CAP-496 | 496 | 3 | 19.23 Example | v0.19 — Step 5 — Representation | EXAMPLE | — | — | — |
| CAP-497 | 497 | 3 | 19.23 Example | v0.19 — Step 6 — Classification | EXAMPLE | — | — | — |
| CAP-498 | 498 | 3 | 19.23 Example | v0.19 — Step 7 — Revision | EXAMPLE | — | [C-07](REVIEW-NOTES.md#c-07--resource--artifact-model-revised) | — |
| CAP-499 | 499 | 1 | — | v0.19 — 19.24 A More Precise End-to-End Pipeline | DATA_MODEL | — | — | — |
| CAP-500 | 500 | 1 | — | v0.19 — 19.25 New Invariants | VALIDATION | — | — | — |
| CAP-501 | 501 | 3 | 19.25 New Invariants | v0.19 — Artifact invariant | VALIDATION | — | [C-07](REVIEW-NOTES.md#c-07--resource--artifact-model-revised) | — |
| CAP-502 | 502 | 3 | 19.25 New Invariants | v0.19 — Resource invariant | VALIDATION | — | — | — |
| CAP-503 | 503 | 3 | 19.25 New Invariants | v0.19 — Representation invariant | VALIDATION | — | — | — |
| CAP-504 | 504 | 3 | 19.25 New Invariants | v0.19 — Revision invariant | VALIDATION | — | [C-07](REVIEW-NOTES.md#c-07--resource--artifact-model-revised) | — |
| CAP-505 | 505 | 3 | 19.25 New Invariants | v0.19 — Observation invariant | OBSERVATION | — | — | — |
| CAP-506 | 506 | 3 | 19.25 New Invariants | v0.19 — Deduplication invariant | VALIDATION | — | — | — |
| CAP-507 | 507 | 3 | 19.25 New Invariants | v0.19 — Change invariant | VALIDATION | — | — | — |
| CAP-508 | 508 | 3 | 19.25 New Invariants | v0.19 — Classification invariant | VALIDATION | — | — | — |
| CAP-509 | 509 | 1 | — | v0.19 — 19.26 Failure Modes | VALIDATION | — | — | — |
| CAP-510 | 510 | 1 | — | v0.19 — 19.27 What v0.19 Gives Us | DATA_MODEL | — | — | — |
| CAP-511 | 511 | 2 | 19.27 What v0.19 Gives Us | v0.19 — Next boundary: v0.20 — Search-Space Partitioning + Discovery Strategies | ROADMAP | — | — | — |
| CAP-512 | 512 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-513 | 513 | 1 | — | v0.20 — Search-Space Partitioning + Discovery Strategies | DISCOVERY | — | — | — |
| CAP-514 | 514 | 1 | — | v0.20 — 20.1 The Search Space | ARCHITECTURE | — | — | — |
| CAP-515 | 515 | 1 | — | v0.20 — 20.2 What Is a Partition? | ARCHITECTURE | — | — | — |
| CAP-516 | 516 | 1 | — | v0.20 — 20.3 Partition ≠ Candidate | CANDIDATE | — | — | — |
| CAP-517 | 517 | 1 | — | v0.20 — 20.4 Partition Object | ARCHITECTURE | — | — | — |
| CAP-518 | 518 | 1 | — | v0.20 — 20.5 Partition State | ARCHITECTURE | — | — | — |
| CAP-519 | 519 | 3 | 20.5 Partition State | v0.20 — Saturated | ARCHITECTURE | — | — | — |
| CAP-520 | 520 | 3 | 20.5 Partition State | v0.20 — Exhausted | ARCHITECTURE | — | — | — |
| CAP-521 | 521 | 1 | — | v0.20 — 20.6 Search Coverage | ARCHITECTURE | — | [C-05](REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified) | — |
| CAP-522 | 522 | 1 | — | v0.20 — 20.7 Strategy Contract | ALGORITHM | — | — | — |
| CAP-523 | 523 | 1 | — | v0.20 — 20.8 Strategy vs Candidate Source | CANDIDATE | — | — | — |
| CAP-524 | 524 | 1 | — | v0.20 — 20.9 Strategy Types | ALGORITHM | — | — | — |
| CAP-525 | 525 | 3 | 20.9 Strategy Types | v0.20 — Seed Expansion | ARCHITECTURE | — | — | — |
| CAP-526 | 526 | 3 | 20.9 Strategy Types | v0.20 — Repository Expansion | ARCHITECTURE | — | — | — |
| CAP-527 | 527 | 3 | 20.9 Strategy Types | v0.20 — Sitemap Expansion | ARCHITECTURE | — | — | — |
| CAP-528 | 528 | 3 | 20.9 Strategy Types | v0.20 — API Schema Expansion | ARCHITECTURE | — | — | — |
| CAP-529 | 529 | 3 | 20.9 Strategy Types | v0.20 — Document-Family Expansion | ARCHITECTURE | — | — | — |
| CAP-530 | 530 | 1 | — | v0.20 — 20.10 Blind-Scan Analogy | DVB_ANALOGY | — | — | — |
| CAP-531 | 531 | 1 | — | v0.20 — 20.11 Probe | ARCHITECTURE | — | — | — |
| CAP-532 | 532 | 1 | — | v0.20 — 20.12 Exploration Plan | ARCHITECTURE | — | — | — |
| CAP-533 | 533 | 1 | — | v0.20 — 20.13 Exploration Must Remain Budgeted | ARCHITECTURE | — | — | — |
| CAP-534 | 534 | 1 | — | v0.20 — 20.14 Adaptive Partition Priority | SCHEDULING | — | — | — |
| CAP-535 | 535 | 1 | — | v0.20 — 20.15 Exploration vs Exploitation | ARCHITECTURE | — | — | — |
| CAP-536 | 536 | 1 | — | v0.20 — 20.16 Aging | SCHEDULING | — | — | — |
| CAP-537 | 537 | 1 | — | v0.20 — 20.17 Partition Splitting | ARCHITECTURE | — | — | — |
| CAP-538 | 538 | 1 | — | v0.20 — 20.18 Partition Merge | ARCHITECTURE | — | — | — |
| CAP-539 | 539 | 1 | — | v0.20 — 20.19 Partition Graph | ARCHITECTURE | — | — | — |
| CAP-540 | 540 | 1 | — | v0.20 — 20.20 SearchSpace | ARCHITECTURE | — | — | — |
| CAP-541 | 541 | 1 | — | v0.20 — 20.21 Search-Space Controller | ARCHITECTURE | — | — | — |
| CAP-542 | 542 | 1 | — | v0.20 — 20.22 Three-Level Control Plane | ARCHITECTURE | — | — | — |
| CAP-543 | 543 | 1 | — | v0.20 — 20.23 Candidate Sources Remain Low-Level | CANDIDATE | — | — | — |
| CAP-544 | 544 | 1 | — | v0.20 — 20.24 Termination Becomes More Sophisticated | ARCHITECTURE | — | [C-09](REVIEW-NOTES.md#c-09--two-termination-taxonomies) | — |
| CAP-545 | 545 | 1 | — | v0.20 — 20.25 Saturation | ARCHITECTURE | — | — | — |
| CAP-546 | 546 | 1 | — | v0.20 — 20.26 Partition Statistics | ARCHITECTURE | — | — | — |
| CAP-547 | 547 | 1 | — | v0.20 — 20.27 Discovery Efficiency | DISCOVERY | — | — | — |
| CAP-548 | 548 | 1 | — | v0.20 — 20.28 Failure Modes | VALIDATION | — | — | — |
| CAP-549 | 549 | 1 | — | v0.20 — 20.29 Core Invariants | VALIDATION | — | — | — |
| CAP-550 | 550 | 3 | 20.29 Core Invariants | v0.20 — Search-space invariant | VALIDATION | — | — | — |
| CAP-551 | 551 | 3 | 20.29 Core Invariants | v0.20 — Strategy invariant | VALIDATION | — | — | — |
| CAP-552 | 552 | 3 | 20.29 Core Invariants | v0.20 — Acquisition invariant | ACQUISITION | — | — | — |
| CAP-553 | 553 | 3 | 20.29 Core Invariants | v0.20 — Partition invariant | VALIDATION | — | — | — |
| CAP-554 | 554 | 3 | 20.29 Core Invariants | v0.20 — Coverage invariant | VALIDATION | — | [C-05](REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified) | — |
| CAP-555 | 555 | 3 | 20.29 Core Invariants | v0.20 — Discovery invariant | VALIDATION | — | — | — |
| CAP-556 | 556 | 1 | — | v0.20 — 20.30 The Architecture After v0.20 | ARCHITECTURE | — | — | — |
| CAP-557 | 557 | 1 | — | v0.20 — 20.31 The DVB Analogy Is Now Structural | DVB_ANALOGY | — | — | — |
| CAP-558 | 558 | 1 | — | v0.21 — Discovery Strategy Learning / Adaptive Search | DISCOVERY | — | — | — |
| CAP-559 | 559 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-560 | 560 | 1 | — | v0.21 — Adaptive Discovery Strategy | DISCOVERY | — | — | — |
| CAP-561 | 561 | 1 | — | v0.21 — 21.1 The Adaptive Loop | ALGORITHM | — | — | — |
| CAP-562 | 562 | 1 | — | v0.21 — 21.2 Strategy Performance Record | ALGORITHM | — | — | — |
| CAP-563 | 563 | 1 | — | v0.21 — 21.3 Yield Metrics | ALGORITHM | — | — | — |
| CAP-564 | 564 | 1 | — | v0.21 — 21.4 Strategy Score | ALGORITHM | — | — | — |
| CAP-565 | 565 | 1 | — | v0.21 — 21.5 Cold Start Problem | ALGORITHM | — | — | — |
| CAP-566 | 566 | 1 | — | v0.21 — 21.6 Exploration Quota | ALGORITHM | — | — | — |
| CAP-567 | 567 | 1 | — | v0.21 — 21.7 Strategy Selection Must Be Constrained | ALGORITHM | — | — | — |
| CAP-568 | 568 | 1 | — | v0.21 — 21.8 Strategy Eligibility | ALGORITHM | — | — | — |
| CAP-569 | 569 | 1 | — | v0.21 — 21.9 Temporary vs Permanent Failure | ALGORITHM | — | — | — |
| CAP-570 | 570 | 1 | — | v0.21 — 21.10 Strategy Outcome | ALGORITHM | — | — | — |
| CAP-571 | 571 | 1 | — | v0.21 — 21.11 Strategy Outcome ≠ Strategy Truth | ALGORITHM | — | — | — |
| CAP-572 | 572 | 1 | — | v0.21 — 21.12 Novelty | ALGORITHM | — | — | — |
| CAP-573 | 573 | 1 | — | v0.21 — 21.13 Frontier Expansion Value | ALGORITHM | — | — | — |
| CAP-574 | 574 | 1 | — | v0.21 — 21.14 Frontier Expansion Metric | ALGORITHM | — | — | — |
| CAP-575 | 575 | 1 | — | v0.21 — 21.15 Strategy Memory | ALGORITHM | — | — | — |
| CAP-576 | 576 | 1 | — | v0.21 — 21.16 Hierarchical Priors | ALGORITHM | — | — | — |
| CAP-577 | 577 | 1 | — | v0.21 — 21.17 Discovery Strategy Ledger | DISCOVERY | — | — | — |
| CAP-578 | 578 | 1 | — | v0.21 — 21.18 Deterministic Replay | ALGORITHM | — | [C-08](REVIEW-NOTES.md#c-08--replay-decisions-deterministic-network-not) | — |
| CAP-579 | 579 | 1 | — | v0.21 — 21.19 Random Exploration | ALGORITHM | — | — | — |
| CAP-580 | 580 | 1 | — | v0.21 — 21.20 Learning Must Not Modify Safety Boundaries | SECURITY | — | — | — |
| CAP-581 | 581 | 1 | — | v0.21 — 21.21 Adaptive Discovery Controller | DISCOVERY | — | — | — |
| CAP-582 | 582 | 1 | — | v0.21 — 21.22 Tie-Breaking Must Be Deterministic | ALGORITHM | — | — | — |
| CAP-583 | 583 | 1 | — | v0.21 — 21.23 Performance Decay | ALGORITHM | — | — | — |
| CAP-584 | 584 | 1 | — | v0.21 — 21.24 Strategy Adaptation and Scan Sessions | ALGORITHM | — | — | — |
| CAP-585 | 585 | 1 | — | v0.21 — 21.25 Search Strategy as a First-Class Graph Node | ALGORITHM | — | — | — |
| CAP-586 | 586 | 1 | — | v0.21 — 21.26 Search Decision Graph | ALGORITHM | — | — | — |
| CAP-587 | 587 | 1 | — | v0.21 — 21.27 Two Kinds of Provenance | PROVENANCE | — | — | — |
| CAP-588 | 588 | 1 | — | v0.21 — 21.28 Failure Taxonomy | VALIDATION | — | — | — |
| CAP-589 | 589 | 1 | — | v0.21 — 21.29 Invariants | VALIDATION | — | — | — |
| CAP-590 | 590 | 3 | 21.29 Invariants | v0.21 — Safety invariant | VALIDATION | — | — | — |
| CAP-591 | 591 | 3 | 21.29 Invariants | v0.21 — Capability invariant | VALIDATION | — | — | — |
| CAP-592 | 592 | 3 | 21.29 Invariants | v0.21 — Domain invariant | VALIDATION | — | — | — |
| CAP-593 | 593 | 3 | 21.29 Invariants | v0.21 — Exploration invariant | VALIDATION | — | — | — |
| CAP-594 | 594 | 3 | 21.29 Invariants | v0.21 — Historical invariant | VALIDATION | — | — | — |
| CAP-595 | 595 | 3 | 21.29 Invariants | v0.21 — Replay invariant | VALIDATION | — | [C-08](REVIEW-NOTES.md#c-08--replay-decisions-deterministic-network-not) | — |
| CAP-596 | 596 | 3 | 21.29 Invariants | v0.21 — Provenance invariant | PROVENANCE | — | — | — |
| CAP-597 | 597 | 1 | — | v0.21 — 21.30 Architecture After v0.21 | ARCHITECTURE | — | — | — |
| CAP-598 | 598 | 1 | — | v0.21 — 21.31 The Important Conceptual Shift | CONCEPT | — | — | — |
| CAP-599 | 599 | 1 | — | v0.22 — Discovery Completeness + Coverage Claims | DISCOVERY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming), [C-05](REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified) | — |
| CAP-600 | 600 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-601 | 601 | 1 | — | v0.22 — Discovery Completeness + Coverage Claims | DISCOVERY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming), [C-05](REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified) | — |
| CAP-602 | 602 | 2 | v0.22 — Discovery Completeness + Coverage Claims | v0.22 — 22.1 The problem | ALGORITHM | — | — | — |
| CAP-603 | 603 | 1 | — | v0.22 — 22.2 Search-space state model | ALGORITHM | — | — | — |
| CAP-604 | 604 | 1 | — | v0.22 — 22.3 Coverage is a measurement | ALGORITHM | — | [C-05](REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified) | — |
| CAP-605 | 605 | 1 | — | v0.22 — 22.4 Coverage dimensions | ALGORITHM | — | [C-05](REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified) | — |
| CAP-606 | 606 | 1 | — | v0.22 — 22.5 CoverageRecord | ALGORITHM | — | [C-05](REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified) | — |
| CAP-607 | 607 | 1 | — | v0.22 — 22.6 Coverage state | ALGORITHM | — | [C-05](REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified) | — |
| CAP-608 | 608 | 1 | — | v0.22 — 22.7 CoverageClaim | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming), [C-05](REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified) | — |
| CAP-609 | 609 | 1 | — | v0.22 — 22.8 Completeness is a stronger assertion | ALGORITHM | — | [C-05](REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified) | — |
| CAP-610 | 610 | 1 | — | v0.22 — 22.9 The finite-enumerator case | ALGORITHM | — | — | — |
| CAP-611 | 611 | 1 | — | v0.22 — 22.10 Enumeration contract | ALGORITHM | — | — | — |
| CAP-612 | 612 | 1 | — | v0.22 — 22.11 Negative evidence | ALGORITHM | — | — | — |
| CAP-613 | 613 | 1 | — | v0.22 — 22.12 Absence reasoning hierarchy | ALGORITHM | — | — | — |
| CAP-614 | 614 | 1 | — | v0.22 — 22.13 “Not found” becomes a first-class result | ALGORITHM | — | — | — |
| CAP-615 | 615 | 1 | — | v0.22 — 22.14 Coverage cannot necessarily be monotonically interpreted | ALGORITHM | — | [C-05](REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified) | — |
| CAP-616 | 616 | 1 | — | v0.22 — 22.15 Version the search universe | ALGORITHM | — | — | — |
| CAP-617 | 617 | 1 | — | v0.22 — 22.16 Coverage ledger | ALGORITHM | — | [C-05](REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified) | — |
| CAP-618 | 618 | 1 | — | v0.22 — 22.17 Three graphs now interact | ALGORITHM | — | — | — |
| CAP-619 | 619 | 1 | — | v0.22 — 22.18 Completeness assessment | ALGORITHM | — | [C-05](REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified) | — |
| CAP-620 | 620 | 1 | — | v0.22 — 22.19 Assurance levels | VALIDATION | — | — | — |
| CAP-621 | 621 | 1 | — | v0.22 — 22.20 Search completeness matrix | ALGORITHM | — | [C-05](REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified) | — |
| CAP-622 | 622 | 1 | — | v0.22 — 22.21 Coverage calculation | ALGORITHM | — | [C-05](REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified) | — |
| CAP-623 | 623 | 1 | — | v0.22 — 22.22 Coverage should be query-relative | ALGORITHM | — | [C-05](REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified) | — |
| CAP-624 | 624 | 1 | — | v0.22 — 22.23 Failure taxonomy | VALIDATION | — | — | — |
| CAP-625 | 625 | 1 | — | v0.22 — 22.24 Core invariants | VALIDATION | — | — | — |
| CAP-626 | 626 | 3 | 22.24 Core invariants | v0.22 — Invariant 1 | VALIDATION | — | — | — |
| CAP-627 | 627 | 3 | 22.24 Core invariants | v0.22 — Invariant 2 | VALIDATION | — | — | — |
| CAP-628 | 628 | 3 | 22.24 Core invariants | v0.22 — Invariant 3 | VALIDATION | — | — | — |
| CAP-629 | 629 | 3 | 22.24 Core invariants | v0.22 — Invariant 4 | VALIDATION | — | — | — |
| CAP-630 | 630 | 3 | 22.24 Core invariants | v0.22 — Invariant 5 | VALIDATION | — | — | — |
| CAP-631 | 631 | 3 | 22.24 Core invariants | v0.22 — Invariant 6 | VALIDATION | — | — | — |
| CAP-632 | 632 | 3 | 22.24 Core invariants | v0.22 — Invariant 7 | VALIDATION | — | — | — |
| CAP-633 | 633 | 3 | 22.24 Core invariants | v0.22 — Invariant 8 | VALIDATION | — | — | — |
| CAP-634 | 634 | 3 | 22.24 Core invariants | v0.22 — Invariant 9 | VALIDATION | — | — | — |
| CAP-635 | 635 | 3 | 22.24 Core invariants | v0.22 — Invariant 10 | VALIDATION | — | — | — |
| CAP-636 | 636 | 1 | — | v0.22 — 22.25 v0.22 architecture | ARCHITECTURE | — | — | — |
| CAP-637 | 637 | 1 | — | v0.22 — 22.26 The conceptual jump | CONCEPT | — | — | — |
| CAP-638 | 638 | 1 | — | v0.23 — Negative Evidence + Absence Reasoning | ALGORITHM | — | — | — |
| CAP-639 | 639 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-640 | 640 | 1 | — | v0.23 — Negative Evidence + Absence Reasoning | ALGORITHM | — | — | — |
| CAP-641 | 641 | 2 | v0.23 — Negative Evidence + Absence Reasoning | v0.23 — 23.1 The absence problem | ALGORITHM | — | — | — |
| CAP-642 | 642 | 1 | — | v0.23 — 23.2 Four fundamental states | ALGORITHM | — | — | — |
| CAP-643 | 643 | 1 | — | v0.23 — 23.3 PresenceAssertion | ALGORITHM | — | — | — |
| CAP-644 | 644 | 1 | — | v0.23 — 23.4 Absence is always scoped | SCOPE | — | — | — |
| CAP-645 | 645 | 1 | — | v0.23 — 23.5 NegativeEvidence | ALGORITHM | — | — | — |
| CAP-646 | 646 | 1 | — | v0.23 — 23.6 Absence strength | ALGORITHM | — | — | — |
| CAP-647 | 647 | 1 | — | v0.23 — 23.7 Search failure must not become negative evidence automatically | SECURITY | — | — | — |
| CAP-648 | 648 | 1 | — | v0.23 — 23.8 Failure → evidence mapping | VALIDATION | — | — | — |
| CAP-649 | 649 | 1 | — | v0.23 — 23.9 Exact locator absence | ALGORITHM | — | — | — |
| CAP-650 | 650 | 1 | — | v0.23 — 23.10 Claims need predicates | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-651 | 651 | 1 | — | v0.23 — 23.11 Predicate-aware absence | ALGORITHM | — | — | — |
| CAP-652 | 652 | 1 | — | v0.23 — 23.12 Contradiction becomes first-class | ALGORITHM | — | — | — |
| CAP-653 | 653 | 1 | — | v0.23 — 23.13 True contradiction | ALGORITHM | — | — | — |
| CAP-654 | 654 | 1 | — | v0.23 — 23.14 Absence confidence cannot simply be numeric | ALGORITHM | — | [C-06](REVIEW-NOTES.md#c-06--confidence-one-score-versus-no-single-global-score) | — |
| CAP-655 | 655 | 1 | — | v0.23 — 23.15 Independent evidence | ALGORITHM | — | — | — |
| CAP-656 | 656 | 1 | — | v0.23 — 23.16 Absence reasoning engine | ALGORITHM | — | — | — |
| CAP-657 | 657 | 1 | — | v0.23 — 23.17 Formal absence rule | ALGORITHM | — | — | — |
| CAP-658 | 658 | 1 | — | v0.23 — 23.18 Dynamic universes | ALGORITHM | — | — | — |
| CAP-659 | 659 | 1 | — | v0.23 — 23.19 Temporal validity | ALGORITHM | — | — | — |
| CAP-660 | 660 | 1 | — | v0.23 — 23.20 Absence and revision detection | ALGORITHM | — | [C-07](REVIEW-NOTES.md#c-07--resource--artifact-model-revised) | — |
| CAP-661 | 661 | 1 | — | v0.23 — 23.21 Search state now becomes richer | ALGORITHM | — | — | — |
| CAP-662 | 662 | 1 | — | v0.23 — 23.22 Architecture after v0.23 | ARCHITECTURE | — | — | — |
| CAP-663 | 663 | 1 | — | v0.23 — 23.23 The three epistemic outcomes | ALGORITHM | — | — | — |
| CAP-664 | 664 | 3 | 23.23 The three epistemic outcomes | v0.23 — Presence | ALGORITHM | — | — | — |
| CAP-665 | 665 | 3 | 23.23 The three epistemic outcomes | v0.23 — Absence | ALGORITHM | — | — | — |
| CAP-666 | 666 | 3 | 23.23 The three epistemic outcomes | v0.23 — Unknown | ALGORITHM | — | — | — |
| CAP-667 | 667 | 1 | — | v0.23 — 23.24 New invariants | VALIDATION | — | — | — |
| CAP-668 | 668 | 3 | 23.24 New invariants | v0.23 — Invariant 1 | VALIDATION | — | — | — |
| CAP-669 | 669 | 3 | 23.24 New invariants | v0.23 — Invariant 2 | VALIDATION | — | — | — |
| CAP-670 | 670 | 3 | 23.24 New invariants | v0.23 — Invariant 3 | VALIDATION | — | — | — |
| CAP-671 | 671 | 3 | 23.24 New invariants | v0.23 — Invariant 4 | VALIDATION | — | — | — |
| CAP-672 | 672 | 3 | 23.24 New invariants | v0.23 — Invariant 5 | VALIDATION | — | — | — |
| CAP-673 | 673 | 3 | 23.24 New invariants | v0.23 — Invariant 6 | VALIDATION | — | — | — |
| CAP-674 | 674 | 3 | 23.24 New invariants | v0.23 — Invariant 7 | VALIDATION | — | — | — |
| CAP-675 | 675 | 3 | 23.24 New invariants | v0.23 — Invariant 8 | VALIDATION | — | — | — |
| CAP-676 | 676 | 3 | 23.24 New invariants | v0.23 — Invariant 9 | VALIDATION | — | — | — |
| CAP-677 | 677 | 3 | 23.24 New invariants | v0.23 — Invariant 10 | VALIDATION | — | — | — |
| CAP-678 | 678 | 1 | — | v0.23 — 23.25 v0.23 conceptual result | CONCEPT | — | — | — |
| CAP-679 | 679 | 1 | — | v0.24 — Query/Goal-Constrained Discovery | DISCOVERY | — | — | — |
| CAP-680 | 680 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-681 | 681 | 1 | — | v0.24 — Query/Goal-Constrained Discovery | DISCOVERY | — | — | — |
| CAP-682 | 682 | 1 | — | v0.24 — 24.1 SearchGoal | ALGORITHM | — | — | — |
| CAP-683 | 683 | 1 | — | v0.24 — 24.2 Goal ≠ Domain | ALGORITHM | — | — | — |
| CAP-684 | 684 | 1 | — | v0.24 — 24.3 Goal constraints | ALGORITHM | — | — | — |
| CAP-685 | 685 | 1 | — | v0.24 — 24.4 Hard constraints vs soft preferences | ALGORITHM | — | — | — |
| CAP-686 | 686 | 1 | — | v0.24 — 24.5 GoalConstraint | ALGORITHM | — | — | — |
| CAP-687 | 687 | 1 | — | v0.24 — 24.6 Relevance is not classification | ALGORITHM | — | — | — |
| CAP-688 | 688 | 1 | — | v0.24 — 24.7 RelevanceAssertion | ALGORITHM | — | — | — |
| CAP-689 | 689 | 1 | — | v0.24 — 24.8 Why `UNKNOWN` matters | ALGORITHM | — | — | — |
| CAP-690 | 690 | 1 | — | v0.24 — 24.9 Relevance scoring | ALGORITHM | — | — | — |
| CAP-691 | 691 | 1 | — | v0.24 — 24.10 The six questions | ALGORITHM | — | — | — |
| CAP-692 | 692 | 1 | — | v0.24 — 24.11 Relevant Search Space | ALGORITHM | — | — | — |
| CAP-693 | 693 | 1 | — | v0.24 — 24.12 Example | ALGORITHM | — | — | — |
| CAP-694 | 694 | 1 | — | v0.24 — 24.13 Goal-directed adaptive discovery | DISCOVERY | — | — | — |
| CAP-695 | 695 | 1 | — | v0.24 — 24.14 Expected Goal Value | ALGORITHM | — | — | — |
| CAP-696 | 696 | 1 | — | v0.24 — 24.15 Information gain | ALGORITHM | — | — | — |
| CAP-697 | 697 | 1 | — | v0.24 — 24.16 Goal-aware partition scoring | ALGORITHM | — | — | — |
| CAP-698 | 698 | 1 | — | v0.24 — 24.17 Goal does not grant authority | ALGORITHM | — | — | — |
| CAP-699 | 699 | 1 | — | v0.24 — 24.18 Goal provenance | PROVENANCE | — | — | — |
| CAP-700 | 700 | 1 | — | v0.24 — 24.19 Goal-aware discovery event | DISCOVERY | — | — | — |
| CAP-701 | 701 | 1 | — | v0.24 — 24.20 Goal lifecycle | ALGORITHM | — | — | — |
| CAP-702 | 702 | 1 | — | v0.24 — 24.21 Goal termination policies | ALGORITHM | — | [C-09](REVIEW-NOTES.md#c-09--two-termination-taxonomies) | — |
| CAP-703 | 703 | 1 | — | v0.24 — 24.22 Goal satisfaction vs completeness | ALGORITHM | — | [C-05](REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified) | — |
| CAP-704 | 704 | 1 | — | v0.24 — 24.23 GoalResult | ALGORITHM | — | — | — |
| CAP-705 | 705 | 1 | — | v0.24 — 24.24 Result ranking | ALGORITHM | — | — | — |
| CAP-706 | 706 | 1 | — | v0.24 — 24.25 Result quality model | ALGORITHM | — | — | — |
| CAP-707 | 707 | 1 | — | v0.24 — 24.26 Goal conflict | ALGORITHM | — | — | — |
| CAP-708 | 708 | 1 | — | v0.24 — 24.27 Goal sessions | ALGORITHM | — | — | — |
| CAP-709 | 709 | 1 | — | v0.24 — 24.28 Reuse of previous knowledge | ALGORITHM | — | [C-10](REVIEW-NOTES.md#c-10--knowledge-store-naming) | — |
| CAP-710 | 710 | 1 | — | v0.24 — 24.29 Knowledge reuse is not evidence reuse without qualification | ALGORITHM | — | [C-10](REVIEW-NOTES.md#c-10--knowledge-store-naming) | — |
| CAP-711 | 711 | 1 | — | v0.24 — 24.30 New architecture | ARCHITECTURE | — | — | — |
| CAP-712 | 712 | 1 | — | v0.24 — 24.31 The architecture's semantic layers | ARCHITECTURE | — | — | — |
| CAP-713 | 713 | 1 | — | v0.24 — 24.32 Core invariants for v0.24 | VALIDATION | — | — | — |
| CAP-714 | 714 | 3 | 24.32 Core invariants for v0.24 | v0.24 — Invariant 1 | VALIDATION | — | — | — |
| CAP-715 | 715 | 3 | 24.32 Core invariants for v0.24 | v0.24 — Invariant 2 | VALIDATION | — | — | — |
| CAP-716 | 716 | 3 | 24.32 Core invariants for v0.24 | v0.24 — Invariant 3 | VALIDATION | — | — | — |
| CAP-717 | 717 | 3 | 24.32 Core invariants for v0.24 | v0.24 — Invariant 4 | VALIDATION | — | — | — |
| CAP-718 | 718 | 3 | 24.32 Core invariants for v0.24 | v0.24 — Invariant 5 | VALIDATION | — | — | — |
| CAP-719 | 719 | 3 | 24.32 Core invariants for v0.24 | v0.24 — Invariant 6 | VALIDATION | — | — | — |
| CAP-720 | 720 | 3 | 24.32 Core invariants for v0.24 | v0.24 — Invariant 7 | VALIDATION | — | — | — |
| CAP-721 | 721 | 3 | 24.32 Core invariants for v0.24 | v0.24 — Invariant 8 | VALIDATION | — | — | — |
| CAP-722 | 722 | 3 | 24.32 Core invariants for v0.24 | v0.24 — Invariant 9 | VALIDATION | — | — | — |
| CAP-723 | 723 | 3 | 24.32 Core invariants for v0.24 | v0.24 — Invariant 10 | VALIDATION | — | — | — |
| CAP-724 | 724 | 1 | — | v0.24 — 24.33 What v0.24 changes fundamentally | ALGORITHM | — | — | — |
| CAP-725 | 725 | 1 | — | v0.25 — Discovery Query Planner | DISCOVERY | — | — | — |
| CAP-726 | 726 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-727 | 727 | 1 | — | v0.25 — Discovery Query Planner | DISCOVERY | — | — | — |
| CAP-728 | 728 | 2 | v0.25 — Discovery Query Planner | v0.25 — 25.1 Planner ≠ Search Engine | ALGORITHM | — | — | — |
| CAP-729 | 729 | 1 | — | v0.25 — 25.2 QueryPlan | ALGORITHM | — | — | — |
| CAP-730 | 730 | 1 | — | v0.25 — 25.3 QueryStep | ALGORITHM | — | — | — |
| CAP-731 | 731 | 1 | — | v0.25 — 25.4 Query decomposition | ALGORITHM | — | — | — |
| CAP-732 | 732 | 1 | — | v0.25 — 25.5 Search axes | ALGORITHM | — | — | — |
| CAP-733 | 733 | 1 | — | v0.25 — 25.6 QueryTactic | ALGORITHM | — | — | — |
| CAP-734 | 734 | 1 | — | v0.25 — 25.7 Tactic ≠ Strategy | ALGORITHM | — | — | — |
| CAP-735 | 735 | 1 | — | v0.25 — 25.8 Planner plugins | ALGORITHM | — | — | — |
| CAP-736 | 736 | 1 | — | v0.25 — 25.9 Planner contract | ALGORITHM | — | — | — |
| CAP-737 | 737 | 1 | — | v0.25 — 25.10 Query plan example | ALGORITHM | — | — | — |
| CAP-738 | 738 | 1 | — | v0.25 — 25.11 Dependencies | ALGORITHM | — | — | — |
| CAP-739 | 739 | 1 | — | v0.25 — 25.12 Conditional planning | ALGORITHM | — | — | — |
| CAP-740 | 740 | 1 | — | v0.25 — 25.13 Planning boundary | ALGORITHM | — | — | — |
| CAP-741 | 741 | 1 | — | v0.25 — 25.14 Query plan validation | ALGORITHM | — | [C-02](REVIEW-NOTES.md#c-02--the-discovery-pipeline-is-described-with-two-different-step-sets) | — |
| CAP-742 | 742 | 1 | — | v0.25 — 25.15 Planner and adaptive discovery | DISCOVERY | — | — | — |
| CAP-743 | 743 | 1 | — | v0.25 — 25.16 Exploration vs exploitation moves upward | ALGORITHM | — | — | — |
| CAP-744 | 744 | 1 | — | v0.25 — 25.17 Query tactic performance | ALGORITHM | — | — | — |
| CAP-745 | 745 | 1 | — | v0.25 — 25.18 Query planner provenance | PROVENANCE | — | — | — |
| CAP-746 | 746 | 1 | — | v0.25 — 25.19 Query plan identity | ALGORITHM | — | [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution) | — |
| CAP-747 | 747 | 1 | — | v0.25 — 25.20 Plan versioning | ALGORITHM | — | — | — |
| CAP-748 | 748 | 1 | — | v0.25 — 25.21 Planner cannot erase old work | ALGORITHM | — | — | — |
| CAP-749 | 749 | 1 | — | v0.25 — 25.22 Query expansion | ALGORITHM | — | — | — |
| CAP-750 | 750 | 1 | — | v0.25 — 25.23 Expansion evidence | ALGORITHM | — | — | — |
| CAP-751 | 751 | 1 | — | v0.25 — 25.24 Planner hallucination boundary | ALGORITHM | — | — | — |
| CAP-752 | 752 | 1 | — | v0.25 — 25.25 Search hypothesis | ALGORITHM | — | — | — |
| CAP-753 | 753 | 1 | — | v0.25 — 25.26 Query planner and DVB analogy | DVB_ANALOGY | — | — | — |
| CAP-754 | 754 | 1 | — | v0.25 — 25.27 Planner output is not execution | ALGORITHM | — | — | — |
| CAP-755 | 755 | 1 | — | v0.25 — 25.28 Planner budget | ALGORITHM | — | — | — |
| CAP-756 | 756 | 1 | — | v0.25 — 25.29 Three different budgets | ALGORITHM | — | — | — |
| CAP-757 | 757 | 1 | — | v0.25 — 25.30 Termination propagation | ALGORITHM | — | [C-09](REVIEW-NOTES.md#c-09--two-termination-taxonomies) | — |
| CAP-758 | 758 | 1 | — | v0.25 — 25.31 v0.25 complete architecture | ARCHITECTURE | — | — | — |
| CAP-759 | 759 | 1 | — | v0.25 — 25.32 v0.25 invariants | VALIDATION | — | — | — |
| CAP-760 | 760 | 3 | 25.32 v0.25 invariants | v0.25 — Planner invariants | VALIDATION | — | — | — |
| CAP-761 | 761 | 1 | — | v0.25 — 25.33 The resulting abstraction stack | ALGORITHM | — | — | — |
| CAP-762 | 762 | 1 | — | v0.26 — Search Tactic Runtime | ALGORITHM | — | — | — |
| CAP-763 | 763 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-764 | 764 | 1 | — | v0.26 — Search Tactic Runtime | ALGORITHM | — | — | — |
| CAP-765 | 765 | 2 | v0.26 — Search Tactic Runtime | v0.26 — 26.1 The architectural gap | ALGORITHM | — | — | — |
| CAP-766 | 766 | 1 | — | v0.26 — 26.2 QueryStep ≠ TacticExecution | ALGORITHM | — | — | — |
| CAP-767 | 767 | 1 | — | v0.26 — 26.3 TacticExecution | ALGORITHM | — | — | — |
| CAP-768 | 768 | 1 | — | v0.26 — 26.4 TacticRuntime | ALGORITHM | — | — | — |
| CAP-769 | 769 | 1 | — | v0.26 — 26.5 TacticRuntime responsibilities | ALGORITHM | — | — | — |
| CAP-770 | 770 | 1 | — | v0.26 — 26.6 Tactic contract | ALGORITHM | — | — | — |
| CAP-771 | 771 | 1 | — | v0.26 — 26.7 Capability surface | ALGORITHM | — | — | — |
| CAP-772 | 772 | 1 | — | v0.26 — 26.8 Bounded execution | ALGORITHM | — | — | — |
| CAP-773 | 773 | 1 | — | v0.26 — 26.9 Batch execution | ALGORITHM | — | — | — |
| CAP-774 | 774 | 1 | — | v0.26 — 26.10 Cursor | ALGORITHM | — | — | — |
| CAP-775 | 775 | 1 | — | v0.26 — 26.11 Checkpoint | ALGORITHM | — | — | — |
| CAP-776 | 776 | 1 | — | v0.26 — 26.12 Checkpoint atomicity | ALGORITHM | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-777 | 777 | 1 | — | v0.26 — 26.13 Tactic dependencies | ALGORITHM | — | — | — |
| CAP-778 | 778 | 1 | — | v0.26 — 26.14 Tactic lifecycle | ALGORITHM | — | — | — |
| CAP-779 | 779 | 1 | — | v0.26 — 26.15 Exhaustion vs completion | ALGORITHM | — | — | — |
| CAP-780 | 780 | 1 | — | v0.26 — 26.16 Tactic result | ALGORITHM | — | — | — |
| CAP-781 | 781 | 1 | — | v0.26 — 26.17 Tactic does not create candidates directly | CANDIDATE | — | — | — |
| CAP-782 | 782 | 1 | — | v0.26 — 26.18 Tactic → Strategy relationship | ALGORITHM | — | — | — |
| CAP-783 | 783 | 1 | — | v0.26 — 26.19 Tactic provenance | PROVENANCE | — | — | — |
| CAP-784 | 784 | 1 | — | v0.26 — 26.20 Failure taxonomy | VALIDATION | — | — | — |
| CAP-785 | 785 | 3 | 26.20 Failure taxonomy | v0.26 — Planning failures | ALGORITHM | — | — | — |
| CAP-786 | 786 | 3 | 26.20 Failure taxonomy | v0.26 — Runtime failures | ALGORITHM | — | — | — |
| CAP-787 | 787 | 3 | 26.20 Failure taxonomy | v0.26 — Strategy failures | ALGORITHM | — | — | — |
| CAP-788 | 788 | 3 | 26.20 Failure taxonomy | v0.26 — Search failures | ALGORITHM | — | — | — |
| CAP-789 | 789 | 3 | 26.20 Failure taxonomy | v0.26 — Recovery failures | ALGORITHM | — | — | — |
| CAP-790 | 790 | 1 | — | v0.26 — 26.21 Retry semantics | ALGORITHM | — | — | — |
| CAP-791 | 791 | 1 | — | v0.26 — 26.22 Cancellation | ALGORITHM | — | — | — |
| CAP-792 | 792 | 1 | — | v0.26 — 26.23 Shared Frontier interaction | ALGORITHM | — | — | — |
| CAP-793 | 793 | 1 | — | v0.26 — 26.24 v0.26 architecture | ARCHITECTURE | — | — | — |
| CAP-794 | 794 | 1 | — | v0.26 — 26.25 Accounting | ALGORITHM | — | — | — |
| CAP-795 | 795 | 1 | — | v0.26 — 26.26 The important safety invariant | VALIDATION | — | — | — |
| CAP-796 | 796 | 1 | — | v0.26 — 26.27 Resumability invariant | VALIDATION | — | — | — |
| CAP-797 | 797 | 1 | — | v0.26 — 26.28 New state model | ALGORITHM | — | — | — |
| CAP-798 | 798 | 1 | — | v0.26 — 26.29 v0.26 invariants | VALIDATION | — | — | — |
| CAP-799 | 799 | 3 | 26.29 v0.26 invariants | v0.26 — I1 — Planning/execution separation | VALIDATION | — | — | — |
| CAP-800 | 800 | 3 | 26.29 v0.26 invariants | v0.26 — I2 — Execution identity | VALIDATION | — | [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution) | — |
| CAP-801 | 801 | 3 | 26.29 v0.26 invariants | v0.26 — I3 — Single scheduler authority | SCHEDULING | — | — | — |
| CAP-802 | 802 | 3 | 26.29 v0.26 invariants | v0.26 — I4 — Bounded execution | VALIDATION | — | — | — |
| CAP-803 | 803 | 3 | 26.29 v0.26 invariants | v0.26 — I5 — Resumability | VALIDATION | — | — | — |
| CAP-804 | 804 | 3 | 26.29 v0.26 invariants | v0.26 — I6 — No silent cursor advancement | VALIDATION | — | — | — |
| CAP-805 | 805 | 3 | 26.29 v0.26 invariants | v0.26 — I7 — Proposal boundary | VALIDATION | — | — | — |
| CAP-806 | 806 | 3 | 26.29 v0.26 invariants | v0.26 — I8 — No authority escalation | VALIDATION | — | — | — |
| CAP-807 | 807 | 3 | 26.29 v0.26 invariants | v0.26 — I9 — Exhaustion separation | VALIDATION | — | — | — |
| CAP-808 | 808 | 3 | 26.29 v0.26 invariants | v0.26 — I10 — Failure ≠ absence | VALIDATION | — | — | — |
| CAP-809 | 809 | 3 | 26.29 v0.26 invariants | v0.26 — I11 — Provenance | PROVENANCE | — | — | — |
| CAP-810 | 810 | 3 | 26.29 v0.26 invariants | v0.26 — I12 — Versioned recovery | VALIDATION | — | — | — |
| CAP-811 | 811 | 1 | — | v0.26 — 26.30 What v0.26 actually gives us | CONCEPT | — | — | — |
| CAP-812 | 812 | 2 | 26.30 What v0.26 actually gives us | v0.26 — Next boundary: v0.27 | ROADMAP | — | — | — |
| CAP-813 | 813 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-814 | 814 | 1 | — | v0.27 — Enumeration Runtime | ALGORITHM | — | — | — |
| CAP-815 | 815 | 1 | — | v0.27 — 27.1 The central distinction | ALGORITHM | — | — | — |
| CAP-816 | 816 | 1 | — | v0.27 — 27.2 Enumeration as a contract | ALGORITHM | — | — | — |
| CAP-817 | 817 | 1 | — | v0.27 — 27.3 Enumerator interface | ALGORITHM | — | — | — |
| CAP-818 | 818 | 1 | — | v0.27 — 27.4 EnumerationPage | ALGORITHM | — | — | — |
| CAP-819 | 819 | 1 | — | v0.27 — 27.5 `hasMore` is not always trustworthy | ALGORITHM | — | — | — |
| CAP-820 | 820 | 1 | — | v0.27 — 27.6 Enumeration state machine | ALGORITHM | — | — | — |
| CAP-821 | 821 | 1 | — | v0.27 — 27.7 EnumerationRuntime | ALGORITHM | — | — | — |
| CAP-822 | 822 | 1 | — | v0.27 — 27.8 Why this should not be inside DiscoveryStrategy | ALGORITHM | — | — | — |
| CAP-823 | 823 | 1 | — | v0.27 — 27.9 Enumerator examples | ALGORITHM | — | — | — |
| CAP-824 | 824 | 3 | 27.9 Enumerator examples | v0.27 — Sitemap | ALGORITHM | — | — | — |
| CAP-825 | 825 | 3 | 27.9 Enumerator examples | v0.27 — API | ALGORITHM | — | — | — |
| CAP-826 | 826 | 3 | 27.9 Enumerator examples | v0.27 — Repository | ALGORITHM | — | — | — |
| CAP-827 | 827 | 3 | 27.9 Enumerator examples | v0.27 — Manifest | ALGORITHM | — | — | — |
| CAP-828 | 828 | 1 | — | v0.27 — 27.10 EnumerationEntry | ALGORITHM | — | — | — |
| CAP-829 | 829 | 1 | — | v0.27 — 27.11 Entry identity | ALGORITHM | — | [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution) | — |
| CAP-830 | 830 | 1 | — | v0.27 — 27.12 Enumeration cursor | ALGORITHM | — | — | — |
| CAP-831 | 831 | 3 | 27.12 Enumeration cursor | v0.27 — Offset | ALGORITHM | — | — | — |
| CAP-832 | 832 | 3 | 27.12 Enumeration cursor | v0.27 — Page | ALGORITHM | — | — | — |
| CAP-833 | 833 | 3 | 27.12 Enumeration cursor | v0.27 — Token | ALGORITHM | — | — | — |
| CAP-834 | 834 | 3 | 27.12 Enumeration cursor | v0.27 — Locator | ALGORITHM | — | — | — |
| CAP-835 | 835 | 3 | 27.12 Enumeration cursor | v0.27 — Composite | ALGORITHM | — | — | — |
| CAP-836 | 836 | 1 | — | v0.27 — 27.13 Cursor validity | ALGORITHM | — | — | — |
| CAP-837 | 837 | 1 | — | v0.27 — 27.14 Enumeration snapshot | ALGORITHM | — | — | — |
| CAP-838 | 838 | 1 | — | v0.27 — 27.15 Why snapshot identity matters | ALGORITHM | — | [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution) | — |
| CAP-839 | 839 | 1 | — | v0.27 — 27.16 Cardinality | ALGORITHM | — | — | — |
| CAP-840 | 840 | 1 | — | v0.27 — 27.17 Ordering semantics | ALGORITHM | — | — | — |
| CAP-841 | 841 | 1 | — | v0.27 — 27.18 Enumeration consistency | ALGORITHM | — | — | — |
| CAP-842 | 842 | 1 | — | v0.27 — 27.19 Completeness assessment | ALGORITHM | — | [C-05](REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified) | — |
| CAP-843 | 843 | 1 | — | v0.27 — 27.20 The crucial three-level distinction | ALGORITHM | — | — | — |
| CAP-844 | 844 | 1 | — | v0.27 — 27.21 Example: sitemap | EXAMPLE | — | — | — |
| CAP-845 | 845 | 1 | — | v0.27 — 27.22 Enumeration → Coverage | ALGORITHM | — | [C-05](REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified) | — |
| CAP-846 | 846 | 1 | — | v0.27 — 27.23 Enumeration and negative evidence | ALGORITHM | — | — | — |
| CAP-847 | 847 | 1 | — | v0.27 — 27.24 Enumeration budget | ALGORITHM | — | — | — |
| CAP-848 | 848 | 1 | — | v0.27 — 27.25 Enumeration termination states | ALGORITHM | — | [C-09](REVIEW-NOTES.md#c-09--two-termination-taxonomies) | — |
| CAP-849 | 849 | 1 | — | v0.27 — 27.26 Enumeration accounting | ALGORITHM | — | — | — |
| CAP-850 | 850 | 1 | — | v0.27 — 27.27 Enumeration provenance | PROVENANCE | — | — | — |
| CAP-851 | 851 | 1 | — | v0.27 — 27.28 Enumeration replay | ALGORITHM | — | [C-08](REVIEW-NOTES.md#c-08--replay-decisions-deterministic-network-not) | — |
| CAP-852 | 852 | 1 | — | v0.27 — 27.29 Full v0.27 architecture | ARCHITECTURE | — | — | — |
| CAP-853 | 853 | 1 | — | v0.27 — 27.30 New invariants | VALIDATION | — | — | — |
| CAP-854 | 854 | 3 | 27.30 New invariants | v0.27 — E1 — Enumeration is scoped | SCOPE | — | — | — |
| CAP-855 | 855 | 3 | 27.30 New invariants | v0.27 — E2 — Enumeration termination is not global completeness | ALGORITHM | — | [C-05](REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified), [C-09](REVIEW-NOTES.md#c-09--two-termination-taxonomies) | — |
| CAP-856 | 856 | 3 | 27.30 New invariants | v0.27 — E3 — Budget exhaustion is not enumeration exhaustion | ALGORITHM | — | — | — |
| CAP-857 | 857 | 3 | 27.30 New invariants | v0.27 — E4 — Cursor progress must be durable | VALIDATION | — | — | — |
| CAP-858 | 858 | 3 | 27.30 New invariants | v0.27 — E5 — Enumeration entries are not candidates | CANDIDATE | — | — | — |
| CAP-859 | 859 | 3 | 27.30 New invariants | v0.27 — E6 — Cardinality is evidence | VALIDATION | — | — | — |
| CAP-860 | 860 | 3 | 27.30 New invariants | v0.27 — E7 — Historical snapshots remain immutable | VALIDATION | — | — | — |
| CAP-861 | 861 | 3 | 27.30 New invariants | v0.27 — E8 — Incomplete enumeration cannot establish absence | ALGORITHM | — | — | — |
| CAP-862 | 862 | 3 | 27.30 New invariants | v0.27 — E9 — Unstable enumeration weakens completeness | ALGORITHM | — | [C-05](REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified) | — |
| CAP-863 | 863 | 3 | 27.30 New invariants | v0.27 — E10 — Enumerator has no acquisition authority | ACQUISITION | — | — | — |
| CAP-864 | 864 | 3 | 27.30 New invariants | v0.27 — E11 — Enumerator cannot directly mutate the ResourceGraph | VALIDATION | — | — | — |
| CAP-865 | 865 | 3 | 27.30 New invariants | v0.27 — E12 — Termination evidence is provenance-bearing | PROVENANCE | — | [C-09](REVIEW-NOTES.md#c-09--two-termination-taxonomies) | — |
| CAP-866 | 866 | 1 | — | v0.27 — 27.31 The emerging blind-scan analogy | DVB_ANALOGY | — | — | — |
| CAP-867 | 867 | 1 | — | v0.27 takeaway | ALGORITHM | — | — | — |
| CAP-868 | 868 | 1 | — | v0.28 — Search-Space Reconciliation & Frontier Deduplication | ARCHITECTURE | — | — | — |
| CAP-869 | 869 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-870 | 870 | 1 | — | v0.28 — Search-Space Reconciliation & Frontier Deduplication | ARCHITECTURE | — | — | — |
| CAP-871 | 871 | 1 | — | v0.28 — 28.1 The problem with naive deduplication | ARCHITECTURE | — | — | — |
| CAP-872 | 872 | 1 | — | v0.28 — 28.2 Five different kinds of duplication | ARCHITECTURE | — | — | — |
| CAP-873 | 873 | 1 | — | v0.28 — 28.3 Search-space overlap | ARCHITECTURE | — | — | — |
| CAP-874 | 874 | 1 | — | v0.28 — 28.4 SearchPartitionRelation | ARCHITECTURE | — | — | — |
| CAP-875 | 875 | 1 | — | v0.28 — 28.5 Coverage overlap | ARCHITECTURE | — | [C-05](REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified) | — |
| CAP-876 | 876 | 1 | — | v0.28 — 28.6 Frontier deduplication | ARCHITECTURE | — | — | — |
| CAP-877 | 877 | 1 | — | v0.28 — 28.7 SearchWorkKey | ARCHITECTURE | — | — | — |
| CAP-878 | 878 | 1 | — | v0.28 — 28.8 Work equivalence | ARCHITECTURE | — | — | — |
| CAP-879 | 879 | 1 | — | v0.28 — 28.9 Candidate convergence | CANDIDATE | — | — | — |
| CAP-880 | 880 | 1 | — | v0.28 — 28.10 Observation convergence | OBSERVATION | — | — | — |
| CAP-881 | 881 | 1 | — | v0.28 — 28.11 Artifact convergence | ARCHITECTURE | — | [C-07](REVIEW-NOTES.md#c-07--resource--artifact-model-revised) | — |
| CAP-882 | 882 | 1 | — | v0.28 — 28.12 Discovery independence | DISCOVERY | — | — | — |
| CAP-883 | 883 | 1 | — | v0.28 — 28.13 Evidence independence model | ARCHITECTURE | — | — | — |
| CAP-884 | 884 | 1 | — | v0.28 — 28.14 Coverage provenance | PROVENANCE | — | [C-05](REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified) | — |
| CAP-885 | 885 | 1 | — | v0.28 — 28.15 Coverage relation | ARCHITECTURE | — | [C-05](REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified) | — |
| CAP-886 | 886 | 1 | — | v0.28 — 28.16 Coverage union | ARCHITECTURE | — | [C-05](REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified) | — |
| CAP-887 | 887 | 1 | — | v0.28 — 28.17 Disjoint partitions | ARCHITECTURE | — | — | — |
| CAP-888 | 888 | 1 | — | v0.28 — 28.18 Unknown overlap | ARCHITECTURE | — | — | — |
| CAP-889 | 889 | 1 | — | v0.28 — 28.19 Frontier duplicate suppression | ARCHITECTURE | — | — | — |
| CAP-890 | 890 | 1 | — | v0.28 — 28.20 Duplicate suppression must preserve provenance | PROVENANCE | — | — | — |
| CAP-891 | 891 | 1 | — | v0.28 — 28.21 Convergence graph | ARCHITECTURE | — | — | — |
| CAP-892 | 892 | 1 | — | v0.28 — 28.22 Search-space graph | ARCHITECTURE | — | — | — |
| CAP-893 | 893 | 1 | — | v0.28 — 28.23 Search-space coverage ledger | ARCHITECTURE | — | [C-05](REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified) | — |
| CAP-894 | 894 | 1 | — | v0.28 — 28.24 Candidate count is not coverage | CANDIDATE | — | [C-05](REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified) | — |
| CAP-895 | 895 | 1 | — | v0.28 — 28.25 Search-space deduplication vs candidate deduplication | CANDIDATE | — | — | — |
| CAP-896 | 896 | 3 | 28.25 Search-space deduplication vs candidate deduplication | v0.28 — Candidate deduplication | CANDIDATE | — | — | — |
| CAP-897 | 897 | 3 | 28.25 Search-space deduplication vs candidate deduplication | v0.28 — Search-space deduplication | ARCHITECTURE | — | — | — |
| CAP-898 | 898 | 1 | — | v0.28 — 28.26 Adaptive strategy interaction | ALGORITHM | — | — | — |
| CAP-899 | 899 | 1 | — | v0.28 — 28.27 Example | ARCHITECTURE | — | — | — |
| CAP-900 | 900 | 1 | — | v0.28 — 28.28 Reconciliation algorithm | ALGORITHM | — | — | — |
| CAP-901 | 901 | 1 | — | v0.28 — 28.29 Reconciliation must be monotonic | ARCHITECTURE | — | — | — |
| CAP-902 | 902 | 1 | — | v0.28 — 28.30 Reconciliation does not delete evidence | ARCHITECTURE | — | — | — |
| CAP-903 | 903 | 1 | — | v0.28 — 28.31 Failure taxonomy | VALIDATION | — | — | — |
| CAP-904 | 904 | 1 | — | v0.28 — 28.32 Core invariants | VALIDATION | — | — | — |
| CAP-905 | 905 | 3 | 28.32 Core invariants | v0.28 — R1 — Candidate convergence | CANDIDATE | — | — | — |
| CAP-906 | 906 | 3 | 28.32 Core invariants | v0.28 — R2 — Provenance preservation | PROVENANCE | — | — | — |
| CAP-907 | 907 | 3 | 28.32 Core invariants | v0.28 — R3 — Artifact convergence | VALIDATION | — | [C-07](REVIEW-NOTES.md#c-07--resource--artifact-model-revised) | — |
| CAP-908 | 908 | 3 | 28.32 Core invariants | v0.28 — R4 — Observation preservation | OBSERVATION | — | — | — |
| CAP-909 | 909 | 3 | 28.32 Core invariants | v0.28 — R5 — Overlap is not duplication | VALIDATION | — | — | — |
| CAP-910 | 910 | 3 | 28.32 Core invariants | v0.28 — R6 — Equivalent work may be suppressed | VALIDATION | — | — | — |
| CAP-911 | 911 | 3 | 28.32 Core invariants | v0.28 — R7 — Suppression preserves provenance | PROVENANCE | — | — | — |
| CAP-912 | 912 | 3 | 28.32 Core invariants | v0.28 — R8 — Unknown overlap is not disjointness | VALIDATION | — | — | — |
| CAP-913 | 913 | 3 | 28.32 Core invariants | v0.28 — R9 — Coverage is union-aware | VALIDATION | — | [C-05](REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified) | — |
| CAP-914 | 914 | 3 | 28.32 Core invariants | v0.28 — R10 — Candidate count does not establish coverage | CANDIDATE | — | [C-05](REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified) | — |
| CAP-915 | 915 | 3 | 28.32 Core invariants | v0.28 — R11 — Evidence independence must be justified | VALIDATION | — | — | — |
| CAP-916 | 916 | 3 | 28.32 Core invariants | v0.28 — R12 — Historical reconciliation is immutable | VALIDATION | — | — | — |
| CAP-917 | 917 | 1 | — | v0.28 — 28.33 v0.28 architecture | ARCHITECTURE | — | — | — |
| CAP-918 | 918 | 1 | — | v0.28 — 28.34 The deeper architectural result | ARCHITECTURE | — | — | — |
| CAP-919 | 919 | 2 | 28.34 The deeper architectural result | v0.28 — Next boundary — v0.29 | ROADMAP | — | — | — |
| CAP-920 | 920 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-921 | 921 | 1 | — | v0.29 — Dynamic Search-Space Expansion | ARCHITECTURE | — | — | — |
| CAP-922 | 922 | 1 | — | v0.29 — 29.1 The central distinction | ARCHITECTURE | — | — | — |
| CAP-923 | 923 | 1 | — | v0.29 — 29.2 PartitionProposal | ARCHITECTURE | — | — | — |
| CAP-924 | 924 | 1 | — | v0.29 — 29.3 Why proposals are necessary | ARCHITECTURE | — | — | — |
| CAP-925 | 925 | 1 | — | v0.29 — 29.4 PartitionAdmissionController | ARCHITECTURE | — | — | — |
| CAP-926 | 926 | 1 | — | v0.29 — 29.5 Partition identity | ARCHITECTURE | — | [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution) | — |
| CAP-927 | 927 | 1 | — | v0.29 — 29.6 Partition explosion | ARCHITECTURE | — | — | — |
| CAP-928 | 928 | 1 | — | v0.29 — 29.7 ExpansionBudget | ARCHITECTURE | — | — | — |
| CAP-929 | 929 | 1 | — | v0.29 — 29.8 Local expansion rate | ARCHITECTURE | — | — | — |
| CAP-930 | 930 | 1 | — | v0.29 — 29.9 Expansion rate limiting | ARCHITECTURE | — | — | — |
| CAP-931 | 931 | 1 | — | v0.29 — 29.10 Evidence threshold | ARCHITECTURE | — | — | — |
| CAP-932 | 932 | 1 | — | v0.29 — 29.11 Partition proposal epistemic status | ARCHITECTURE | — | — | — |
| CAP-933 | 933 | 1 | — | v0.29 — 29.12 Hypothesis connection | ARCHITECTURE | — | — | — |
| CAP-934 | 934 | 1 | — | v0.29 — 29.13 Partition generation sources | ARCHITECTURE | — | — | — |
| CAP-935 | 935 | 1 | — | v0.29 — 29.14 Expansion provider boundary | PROVIDER | — | — | — |
| CAP-936 | 936 | 1 | — | v0.29 — 29.15 Dynamic search-space graph | ARCHITECTURE | — | — | — |
| CAP-937 | 937 | 1 | — | v0.29 — 29.16 Partition generation event | ARCHITECTURE | — | — | — |
| CAP-938 | 938 | 1 | — | v0.29 — 29.17 Search-space versioning | ARCHITECTURE | — | — | — |
| CAP-939 | 939 | 1 | — | v0.29 — 29.18 SearchSpaceSnapshot | ARCHITECTURE | — | — | — |
| CAP-940 | 940 | 1 | — | v0.29 — 29.19 Expansion and completeness | ARCHITECTURE | — | [C-05](REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified) | — |
| CAP-941 | 941 | 1 | — | v0.29 — 29.20 Dynamic expansion and negative evidence | ARCHITECTURE | — | — | — |
| CAP-942 | 942 | 1 | — | v0.29 — 29.21 Expansion priorities | ARCHITECTURE | — | — | — |
| CAP-943 | 943 | 1 | — | v0.29 — 29.22 Expansion depth | ARCHITECTURE | — | — | — |
| CAP-944 | 944 | 1 | — | v0.29 — 29.23 Expansion loops | ARCHITECTURE | — | — | — |
| CAP-945 | 945 | 1 | — | v0.29 — 29.24 Expansion cycle ≠ failure | ARCHITECTURE | — | — | — |
| CAP-946 | 946 | 1 | — | v0.29 — 29.25 Partition admission states | ARCHITECTURE | — | — | — |
| CAP-947 | 947 | 1 | — | v0.29 — 29.26 Partition proposal accounting | ARCHITECTURE | — | — | — |
| CAP-948 | 948 | 1 | — | v0.29 — 29.27 Partition explosion protection | ARCHITECTURE | — | — | — |
| CAP-949 | 949 | 1 | — | v0.29 — 29.28 Admission algorithm | ALGORITHM | — | — | — |
| CAP-950 | 950 | 1 | — | v0.29 — 29.29 Frontier generation | ARCHITECTURE | — | — | — |
| CAP-951 | 951 | 1 | — | v0.29 — 29.30 Dynamic expansion architecture | ARCHITECTURE | — | — | — |
| CAP-952 | 952 | 1 | — | v0.29 — 29.31 Two expansion paths | ARCHITECTURE | — | — | — |
| CAP-953 | 953 | 1 | — | v0.29 — 29.32 Search-space discovery as first-class knowledge | DISCOVERY | — | [C-10](REVIEW-NOTES.md#c-10--knowledge-store-naming) | — |
| CAP-954 | 954 | 1 | — | v0.29 — 29.33 v0.29 invariants | VALIDATION | — | — | — |
| CAP-955 | 955 | 3 | 29.33 v0.29 invariants | v0.29 — P1 — Discovery does not create authority | VALIDATION | — | — | — |
| CAP-956 | 956 | 3 | 29.33 v0.29 invariants | v0.29 — P2 — Partition proposal is not partition | VALIDATION | — | — | — |
| CAP-957 | 957 | 3 | 29.33 v0.29 invariants | v0.29 — P3 — Every admitted partition belongs to the domain | VALIDATION | — | — | — |
| CAP-958 | 958 | 3 | 29.33 v0.29 invariants | v0.29 — P4 — Expansion is budgeted | VALIDATION | — | — | — |
| CAP-959 | 959 | 3 | 29.33 v0.29 invariants | v0.29 — P5 — Expansion is depth-bounded | VALIDATION | — | — | — |
| CAP-960 | 960 | 3 | 29.33 v0.29 invariants | v0.29 — P6 — Duplicate partitions converge | VALIDATION | — | — | — |
| CAP-961 | 961 | 3 | 29.33 v0.29 invariants | v0.29 — P7 — Overlap is preserved | VALIDATION | — | — | — |
| CAP-962 | 962 | 3 | 29.33 v0.29 invariants | v0.29 — P8 — Evidence is preserved | VALIDATION | — | — | — |
| CAP-963 | 963 | 3 | 29.33 v0.29 invariants | v0.29 — P9 — Partition existence does not schedule execution | SCHEDULING | — | — | — |
| CAP-964 | 964 | 3 | 29.33 v0.29 invariants | v0.29 — P10 — Expansion cannot override policy | SECURITY | — | [C-11](REVIEW-NOTES.md#c-11--same-origin-default-versus-cross-origin-capability) | — |
| CAP-965 | 965 | 3 | 29.33 v0.29 invariants | v0.29 — P11 — Search-space versions are immutable | VALIDATION | — | — | — |
| CAP-966 | 966 | 3 | 29.33 v0.29 invariants | v0.29 — P12 — Expansion does not invalidate historical claims automatically | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-967 | 967 | 3 | 29.33 v0.29 invariants | v0.29 — P13 — Cycles are legal | VALIDATION | — | — | — |
| CAP-968 | 968 | 3 | 29.33 v0.29 invariants | v0.29 — P14 — Unknown remains valid | VALIDATION | — | — | — |
| CAP-969 | 969 | 1 | — | v0.29 — 29.34 The system after v0.29 | ARCHITECTURE | — | — | — |
| CAP-970 | 970 | 1 | — | v0.29 — 29.35 Blind-scan interpretation | DVB_ANALOGY | — | — | — |
| CAP-971 | 971 | 1 | — | v0.29 takeaway | ARCHITECTURE | — | — | — |
| CAP-972 | 972 | 1 | — | v0.30 — Unified Frontier Arbitration | SCHEDULING | — | — | — |
| CAP-973 | 973 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-974 | 974 | 1 | — | v0.30 — Conclusion — Generic Discovery Engine | DISCOVERY | — | — | — |
| CAP-975 | 975 | 2 | Conclusion — Generic Discovery Engine | v0.30 — The final conceptual separation | SCHEDULING | — | — | — |
| CAP-976 | 976 | 1 | — | v0.30 — The fundamental invariant | VALIDATION | — | — | — |
| CAP-977 | 977 | 1 | — | v0.30 — What the DVB analogy actually contributed | DVB_ANALOGY | — | — | — |
| CAP-978 | 978 | 1 | — | v0.30 — The most important safety boundary | SCHEDULING | — | — | — |
| CAP-979 | 979 | 1 | — | v0.30 — Final architecture | ARCHITECTURE | — | — | — |
| CAP-980 | 980 | 1 | — | v0.30 — What the userscript should and should not become | LIMITATIONS | — | — | explicit override |
| CAP-981 | 981 | 1 | — | v0.30 — Final principles | CONCEPT | — | — | — |
| CAP-982 | 982 | — | — | — | SCHEDULING | — | — | lead-in of the following section |
| CAP-983 | 983 | 1 | — | v0.30 — Unified Frontier Arbitration | SCHEDULING | — | — | — |
| CAP-984 | 984 | 2 | v0.30 — Unified Frontier Arbitration | v0.30 — 30.1 The new architecture | ARCHITECTURE | — | — | — |
| CAP-985 | 985 | 1 | — | v0.30 — 30.2 WorkClass | SCHEDULING | — | — | — |
| CAP-986 | 986 | 1 | — | v0.30 — 30.3 WorkClassPolicy | SCHEDULING | — | [C-11](REVIEW-NOTES.md#c-11--same-origin-default-versus-cross-origin-capability) | — |
| CAP-987 | 987 | 1 | — | v0.30 — 30.4 ArbitrationDecision | SCHEDULING | — | — | — |
| CAP-988 | 988 | 1 | — | v0.30 — 30.5 Hard constraints vs soft priorities | SCHEDULING | — | — | — |
| CAP-989 | 989 | 3 | 30.5 Hard constraints vs soft priorities | v0.30 — Hard constraints | SCHEDULING | — | — | — |
| CAP-990 | 990 | 3 | 30.5 Hard constraints vs soft priorities | v0.30 — Soft priorities | SCHEDULING | — | — | — |
| CAP-991 | 991 | 1 | — | v0.30 — 30.6 Arbitration score | SCHEDULING | — | — | — |
| CAP-992 | 992 | 1 | — | v0.30 — 30.7 Aging | SCHEDULING | — | — | — |
| CAP-993 | 993 | 1 | — | v0.30 — 30.8 Starvation detection | SCHEDULING | — | — | — |
| CAP-994 | 994 | 1 | — | v0.30 — 30.9 Class starvation | SCHEDULING | — | — | — |
| CAP-995 | 995 | 1 | — | v0.30 — 30.10 Weighted fairness | SCHEDULING | — | — | — |
| CAP-996 | 996 | 1 | — | v0.30 — 30.11 Deficit-style arbitration | SCHEDULING | — | — | — |
| CAP-997 | 997 | 1 | — | v0.30 — 30.12 Cost-aware scheduling | SCHEDULING | — | — | — |
| CAP-998 | 998 | 1 | — | v0.30 — 30.13 Backpressure | SCHEDULING | — | — | — |
| CAP-999 | 999 | 1 | — | v0.30 — 30.14 Reserved capacity | SCHEDULING | — | — | — |
| CAP-1000 | 1000 | 1 | — | v0.30 — 30.15 Arbitration pipeline | SCHEDULING | — | — | — |
| CAP-1001 | 1001 | 1 | — | v0.30 — 30.16 The atomicity problem | SCHEDULING | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-1002 | 1002 | 1 | — | v0.30 — 30.17 Priority inversion | SCHEDULING | — | — | — |
| CAP-1003 | 1003 | 1 | — | v0.30 — 30.18 FrontierArbitrator | SCHEDULING | — | — | — |
| CAP-1004 | 1004 | 1 | — | v0.30 — 30.19 Arbitration result | SCHEDULING | — | — | — |
| CAP-1005 | 1005 | 1 | — | v0.30 — 30.20 Arbitration ledger | SCHEDULING | — | — | — |
| CAP-1006 | 1006 | 1 | — | v0.30 — 30.21 Replay | SCHEDULING | — | [C-08](REVIEW-NOTES.md#c-08--replay-decisions-deterministic-network-not) | — |
| CAP-1007 | 1007 | 1 | — | v0.30 — 30.22 The deeper invariant | VALIDATION | — | — | — |
| CAP-1008 | 1008 | 1 | — | v0.30 — 30.23 Full v0.30 architecture | ARCHITECTURE | — | — | — |
| CAP-1009 | 1009 | 1 | — | v0.30 — 30.24 Failure taxonomy | VALIDATION | — | — | — |
| CAP-1010 | 1010 | 1 | — | v0.30 — 30.25 v0.30 invariants | VALIDATION | — | — | — |
| CAP-1011 | 1011 | 1 | — | v0.30 — 30.26 What v0.30 actually accomplishes | CONCEPT | — | — | — |
| CAP-1012 | 1012 | 1 | — | v0.30 — Next boundary — v0.31 | ROADMAP | — | — | — |
| CAP-1013 | 1013 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-1014 | 1014 | 1 | — | v0.31 — Unified Resource & Cost Ledger | ARCHITECTURE | — | — | — |
| CAP-1015 | 1015 | 2 | v0.31 — Unified Resource & Cost Ledger | v0.31 — 31.1 Resource dimensions | ARCHITECTURE | — | — | — |
| CAP-1016 | 1016 | 1 | — | v0.31 — 31.2 ResourceBudget | ARCHITECTURE | — | — | — |
| CAP-1017 | 1017 | 1 | — | v0.31 — 31.3 Three resource states | ARCHITECTURE | — | — | — |
| CAP-1018 | 1018 | 1 | — | v0.31 — 31.4 ResourceReservation | ARCHITECTURE | — | — | — |
| CAP-1019 | 1019 | 1 | — | v0.31 — 31.5 Estimated cost vs actual cost | ARCHITECTURE | — | — | — |
| CAP-1020 | 1020 | 1 | — | v0.31 — 31.6 CostObservation | ARCHITECTURE | — | — | — |
| CAP-1021 | 1021 | 1 | — | v0.31 — 31.7 ResourceLedger | ARCHITECTURE | — | — | — |
| CAP-1022 | 1022 | 1 | — | v0.31 — 31.8 Budget scopes | SCOPE | — | — | — |
| CAP-1023 | 1023 | 1 | — | v0.31 — 31.9 Hierarchical budget accounting | ARCHITECTURE | — | — | — |
| CAP-1024 | 1024 | 1 | — | v0.31 — 31.10 Resource allocation | ARCHITECTURE | — | — | — |
| CAP-1025 | 1025 | 1 | — | v0.31 — 31.11 Allocation is not execution | ARCHITECTURE | — | — | — |
| CAP-1026 | 1026 | 1 | — | v0.31 — 31.12 Partial consumption | ARCHITECTURE | — | — | — |
| CAP-1027 | 1027 | 1 | — | v0.31 — 31.13 Cost overruns | ARCHITECTURE | — | — | — |
| CAP-1028 | 1028 | 1 | — | v0.31 — 31.14 Cost model | ARCHITECTURE | — | — | — |
| CAP-1029 | 1029 | 1 | — | v0.31 — 31.15 Cost is context-dependent | ARCHITECTURE | — | — | — |
| CAP-1030 | 1030 | 1 | — | v0.31 — 31.16 Resource exhaustion | ARCHITECTURE | — | — | — |
| CAP-1031 | 1031 | 1 | — | v0.31 — 31.17 Budget exhaustion vs frontier exhaustion | ARCHITECTURE | — | — | — |
| CAP-1032 | 1032 | 1 | — | v0.31 — 31.18 Resource reservation race | ARCHITECTURE | — | — | — |
| CAP-1033 | 1033 | 1 | — | v0.31 — 31.19 Settlement | ARCHITECTURE | — | — | — |
| CAP-1034 | 1034 | 1 | — | v0.31 — 31.20 Cost feedback | ARCHITECTURE | — | — | — |
| CAP-1035 | 1035 | 1 | — | v0.31 — 31.21 ResourceLedger events | ARCHITECTURE | — | — | — |
| CAP-1036 | 1036 | 1 | — | v0.31 — 31.22 Resource accounting and provenance | PROVENANCE | — | — | — |
| CAP-1037 | 1037 | 1 | — | v0.31 — 31.23 Unified v0.31 architecture | ARCHITECTURE | — | — | — |
| CAP-1038 | 1038 | 1 | — | v0.31 — 31.24 The central v0.31 invariants | VALIDATION | — | — | — |
| CAP-1039 | 1039 | 1 | — | v0.31 — 31.25 What v0.31 adds | ARCHITECTURE | — | — | — |
| CAP-1040 | 1040 | 1 | — | v0.32 boundary | ARCHITECTURE | — | — | — |
| CAP-1041 | 1041 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-1042 | 1042 | 1 | — | v0.32 — Transactional Persistence & Crash Recovery | ARCHITECTURE | — | — | — |
| CAP-1043 | 1043 | 2 | v0.32 — Transactional Persistence & Crash Recovery | v0.32 — 32.1 The crash problem | ARCHITECTURE | — | — | — |
| CAP-1044 | 1044 | 1 | — | v0.32 — 32.2 Durable state vs runtime state | ARCHITECTURE | — | — | — |
| CAP-1045 | 1045 | 1 | — | v0.32 — 32.3 Persistence is not serialization | ARCHITECTURE | — | — | — |
| CAP-1046 | 1046 | 1 | — | v0.32 — 32.4 PersistenceAdapter | ARCHITECTURE | — | — | — |
| CAP-1047 | 1047 | 1 | — | v0.32 — 32.5 Transaction | ARCHITECTURE | — | — | — |
| CAP-1048 | 1048 | 1 | — | v0.32 — 32.6 Write-ahead event ledger | ARCHITECTURE | — | — | — |
| CAP-1049 | 1049 | 1 | — | v0.32 — 32.7 Event identity | ARCHITECTURE | — | [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution) | — |
| CAP-1050 | 1050 | 1 | — | v0.32 — 32.8 Monotonic sequence | ARCHITECTURE | — | — | — |
| CAP-1051 | 1051 | 1 | — | v0.32 — 32.9 Commit protocol | ARCHITECTURE | — | — | — |
| CAP-1052 | 1052 | 1 | — | v0.32 — 32.10 Commit markers | ARCHITECTURE | — | — | — |
| CAP-1053 | 1053 | 1 | — | v0.32 — 32.11 Checkpoint correctness | ARCHITECTURE | — | — | — |
| CAP-1054 | 1054 | 1 | — | v0.32 — 32.12 At-least-once vs exactly-once | ARCHITECTURE | — | — | — |
| CAP-1055 | 1055 | 1 | — | v0.32 — 32.13 Idempotency | ARCHITECTURE | — | — | — |
| CAP-1056 | 1056 | 1 | — | v0.32 — 32.14 Work recovery | ARCHITECTURE | — | — | — |
| CAP-1057 | 1057 | 1 | — | v0.32 — 32.15 Recovery scan | ARCHITECTURE | — | — | — |
| CAP-1058 | 1058 | 1 | — | v0.32 — 32.16 RecoveryManager | ARCHITECTURE | — | — | — |
| CAP-1059 | 1059 | 1 | — | v0.32 — 32.17 Reservation recovery | ARCHITECTURE | — | — | — |
| CAP-1060 | 1060 | 1 | — | v0.32 — 32.18 Accounting invariant under crash | VALIDATION | — | — | — |
| CAP-1061 | 1061 | 1 | — | v0.32 — 32.19 Observation recovery | OBSERVATION | — | — | — |
| CAP-1062 | 1062 | 1 | — | v0.32 — 32.20 Artifact durability | ARCHITECTURE | — | [C-07](REVIEW-NOTES.md#c-07--resource--artifact-model-revised) | — |
| CAP-1063 | 1063 | 1 | — | v0.32 — 32.21 Durable checkpoint | ARCHITECTURE | — | — | — |
| CAP-1064 | 1064 | 1 | — | v0.32 — 32.22 Recovery invariant for cursors | VALIDATION | — | — | — |
| CAP-1065 | 1065 | 1 | — | v0.32 — 32.23 Schema versioning | ARCHITECTURE | — | — | — |
| CAP-1066 | 1066 | 1 | — | v0.32 — 32.24 Snapshot + journal | ARCHITECTURE | — | — | — |
| CAP-1067 | 1067 | 1 | — | v0.32 — 32.25 Snapshot integrity | ARCHITECTURE | — | — | — |
| CAP-1068 | 1068 | 1 | — | v0.32 — 32.26 Recovery outcomes | ARCHITECTURE | — | — | — |
| CAP-1069 | 1069 | 1 | — | v0.32 — 32.27 Recovery must not fabricate knowledge | SECURITY | — | [C-10](REVIEW-NOTES.md#c-10--knowledge-store-naming) | — |
| CAP-1070 | 1070 | 1 | — | v0.32 — 32.28 Crash-safe frontier | ARCHITECTURE | — | — | — |
| CAP-1071 | 1071 | 1 | — | v0.32 — 32.29 Reconciliation | ARCHITECTURE | — | — | — |
| CAP-1072 | 1072 | 1 | — | v0.32 — 32.30 Repair is itself provenance | PROVENANCE | — | — | — |
| CAP-1073 | 1073 | 1 | — | v0.32 — 32.31 v0.32 architecture | ARCHITECTURE | — | — | — |
| CAP-1074 | 1074 | 1 | — | v0.32 — 32.32 Complete lifecycle | ARCHITECTURE | — | — | — |
| CAP-1075 | 1075 | 1 | — | v0.32 — 32.33 Failure taxonomy | VALIDATION | — | — | — |
| CAP-1076 | 1076 | 1 | — | v0.32 — 32.34 v0.32 invariants | VALIDATION | — | — | — |
| CAP-1077 | 1077 | 1 | — | v0.32 — 32.35 What v0.32 changes | ARCHITECTURE | — | — | — |
| CAP-1078 | 1078 | 1 | — | v0.33 — Multi-Worker / Multi-Context Coordination | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-1079 | 1079 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-1080 | 1080 | 1 | — | v0.33 — Multi-Worker Coordination & Distributed Claiming | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-1081 | 1081 | 2 | v0.33 — Multi-Worker Coordination & Distributed Claiming | v0.33 — 33.1 Worker identity | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming), [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution) | — |
| CAP-1082 | 1082 | 1 | — | v0.33 — 33.2 Worker registration | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-1083 | 1083 | 1 | — | v0.33 — 33.3 Worker capabilities | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-1084 | 1084 | 1 | — | v0.33 — 33.4 Claiming is the synchronization boundary | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-1085 | 1085 | 1 | — | v0.33 — 33.5 ClaimToken | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-1086 | 1086 | 1 | — | v0.33 — 33.6 Claim ≠ lease | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-1087 | 1087 | 1 | — | v0.33 — 33.7 Lease lifecycle | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-1088 | 1088 | 1 | — | v0.33 — 33.8 LeaseManager | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-1089 | 1089 | 1 | — | v0.33 — 33.9 Heartbeats | CONCURRENCY | — | — | — |
| CAP-1090 | 1090 | 1 | — | v0.33 — 33.10 Fencing tokens | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-1091 | 1091 | 1 | — | v0.33 — 33.11 Fencing invariant | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-1092 | 1092 | 1 | — | v0.33 — 33.12 Worker death | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-1093 | 1093 | 1 | — | v0.33 — 33.13 Duplicate execution | CONCURRENCY | — | — | — |
| CAP-1094 | 1094 | 1 | — | v0.33 — 33.14 Execution identity | CONCURRENCY | — | [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution) | — |
| CAP-1095 | 1095 | 1 | — | v0.33 — 33.15 Duplicate observations | OBSERVATION | — | — | — |
| CAP-1096 | 1096 | 1 | — | v0.33 — 33.16 Duplicate execution ≠ independent evidence | CONCURRENCY | — | — | — |
| CAP-1097 | 1097 | 1 | — | v0.33 — 33.17 Worker-local vs shared state | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-1098 | 1098 | 1 | — | v0.33 — 33.18 CoordinationManager | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-1099 | 1099 | 1 | — | v0.33 — 33.19 Coordination vs arbitration | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-1100 | 1100 | 1 | — | v0.33 — 33.20 Worker selection | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-1101 | 1101 | 1 | — | v0.33 — 33.21 Worker affinity | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-1102 | 1102 | 1 | — | v0.33 — 33.22 Worker capacity | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-1103 | 1103 | 1 | — | v0.33 — 33.23 Distributed accounting | CONCURRENCY | — | — | — |
| CAP-1104 | 1104 | 1 | — | v0.33 — 33.24 Worker-local caches | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-1105 | 1105 | 1 | — | v0.33 — 33.25 Cross-worker event ordering | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-1106 | 1106 | 1 | — | v0.33 — 33.26 Causal provenance | CONCURRENCY | — | — | — |
| CAP-1107 | 1107 | 1 | — | v0.33 — 33.27 Coordination events | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-1108 | 1108 | 1 | — | v0.33 — 33.28 Multi-worker failure modes | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-1109 | 1109 | 1 | — | v0.33 — 33.29 Split-brain | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-1110 | 1110 | 1 | — | v0.33 — 33.30 What the browser prototype can guarantee | LIMITATIONS | — | — | explicit override |
| CAP-1111 | 1111 | 1 | — | v0.33 — 33.31 Coordination scope | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-1112 | 1112 | 1 | — | v0.33 — 33.32 v0.33 architecture | ARCHITECTURE | — | — | — |
| CAP-1113 | 1113 | 1 | — | v0.33 — 33.33 The complete ownership invariant | VALIDATION | — | — | — |
| CAP-1114 | 1114 | 1 | — | v0.33 — 33.34 The deeper distributed invariant | VALIDATION | — | — | — |
| CAP-1115 | 1115 | 1 | — | v0.33 — 33.35 v0.33 result | CONCURRENCY | — | — | — |
| CAP-1116 | 1116 | 1 | — | v0.34 — Coordination Protocol & Distributed Consistency | ARCHITECTURE | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-1117 | 1117 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-1118 | 1118 | 1 | — | v0.34 — Distributed Consistency & Conflict Resolution | ARCHITECTURE | — | — | — |
| CAP-1119 | 1119 | 1 | — | v0.34 — 34.1 New Architecture Boundary | ARCHITECTURE | — | — | — |
| CAP-1120 | 1120 | 1 | — | v0.34 — 34.2 The Core Consistency Model | ARCHITECTURE | — | — | — |
| CAP-1121 | 1121 | 1 | — | v0.34 — 34.3 Optimistic Concurrency Control | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-1122 | 1122 | 1 | — | v0.34 — 34.4 Version ≠ Time | ARCHITECTURE | — | — | — |
| CAP-1123 | 1123 | 1 | — | v0.34 — 34.5 Event Metadata | ARCHITECTURE | — | — | — |
| CAP-1124 | 1124 | 1 | — | v0.34 — 34.6 Versioning + Fencing | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-1125 | 1125 | 1 | — | v0.34 — 34.7 Conflict Is Not One Thing | ARCHITECTURE | — | — | — |
| CAP-1126 | 1126 | 3 | 34.7 Conflict Is Not One Thing | v0.34 — Claim conflict | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-1127 | 1127 | 3 | 34.7 Conflict Is Not One Thing | v0.34 — Candidate conflict | CANDIDATE | — | — | — |
| CAP-1128 | 1128 | 3 | 34.7 Conflict Is Not One Thing | v0.34 — Classification conflict | ARCHITECTURE | — | — | — |
| CAP-1129 | 1129 | 3 | 34.7 Conflict Is Not One Thing | v0.34 — Coverage conflict | ARCHITECTURE | — | [C-05](REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified) | — |
| CAP-1130 | 1130 | 3 | 34.7 Conflict Is Not One Thing | v0.34 — Budget conflict | ARCHITECTURE | — | — | — |
| CAP-1131 | 1131 | 1 | — | v0.34 — 34.8 Conflict Record | ARCHITECTURE | — | — | — |
| CAP-1132 | 1132 | 1 | — | v0.34 — 34.9 Deterministic Conflict Resolver | ARCHITECTURE | — | — | — |
| CAP-1133 | 1133 | 1 | — | v0.34 — 34.10 Resolution Policies | ARCHITECTURE | — | — | — |
| CAP-1134 | 1134 | 1 | — | v0.34 — 34.11 Classification Conflict | ARCHITECTURE | — | — | — |
| CAP-1135 | 1135 | 1 | — | v0.34 — 34.12 Provenance Must Survive Resolution | PROVENANCE | — | — | — |
| CAP-1136 | 1136 | 1 | — | v0.34 — 34.13 Last-Write-Wins Is Not the Default | ARCHITECTURE | — | — | — |
| CAP-1137 | 1137 | 1 | — | v0.34 — 34.14 Append-Only Is Especially Powerful | ARCHITECTURE | — | — | — |
| CAP-1138 | 1138 | 1 | — | v0.34 — 34.15 Materialized State | ARCHITECTURE | — | — | — |
| CAP-1139 | 1139 | 1 | — | v0.34 — 34.16 State Digest | ARCHITECTURE | — | — | — |
| CAP-1140 | 1140 | 1 | — | v0.34 — 34.17 Conflict Detection Pipeline | ARCHITECTURE | — | — | — |
| CAP-1141 | 1141 | 1 | — | v0.34 — 34.18 Conflict Detection vs Conflict Resolution | ARCHITECTURE | — | — | — |
| CAP-1142 | 1142 | 1 | — | v0.34 — 34.19 Conflict Resolver Context | ARCHITECTURE | — | — | — |
| CAP-1143 | 1143 | 1 | — | v0.34 — 34.20 Resolution Event | ARCHITECTURE | — | — | — |
| CAP-1144 | 1144 | 1 | — | v0.34 — 34.21 Cross-Object Conflicts | ARCHITECTURE | — | — | — |
| CAP-1145 | 1145 | 1 | — | v0.34 — 34.22 Consistency Domains | ARCHITECTURE | — | — | — |
| CAP-1146 | 1146 | 1 | — | v0.34 — 34.23 Consistency Is Not Global Ordering | ARCHITECTURE | — | — | — |
| CAP-1147 | 1147 | 1 | — | v0.34 — 34.24 Independent Evidence | ARCHITECTURE | — | — | — |
| CAP-1148 | 1148 | 1 | — | v0.34 — 34.25 Failure Taxonomy | VALIDATION | — | — | — |
| CAP-1149 | 1149 | 1 | — | v0.34 — 34.26 New Core Invariants | VALIDATION | — | — | — |
| CAP-1150 | 1150 | 3 | 34.26 New Core Invariants | v0.34 — Consistency | ARCHITECTURE | — | — | — |
| CAP-1151 | 1151 | 3 | 34.26 New Core Invariants | v0.34 — Fencing | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-1152 | 1152 | 3 | 34.26 New Core Invariants | v0.34 — Conflict | ARCHITECTURE | — | — | — |
| CAP-1153 | 1153 | 3 | 34.26 New Core Invariants | v0.34 — Provenance | PROVENANCE | — | — | — |
| CAP-1154 | 1154 | 3 | 34.26 New Core Invariants | v0.34 — Recovery | ARCHITECTURE | — | — | — |
| CAP-1155 | 1155 | 3 | 34.26 New Core Invariants | v0.34 — Scalability | ARCHITECTURE | — | — | — |
| CAP-1156 | 1156 | 1 | — | v0.34 — 34.27 The Unified State Model | ARCHITECTURE | — | — | — |
| CAP-1157 | 1157 | 1 | — | v0.34 — 34.28 What v0.34 Actually Proves | VALIDATION | — | — | explicit override |
| CAP-1158 | 1158 | 3 | 34.28 What v0.34 Actually Proves | v0.34 — PROVED by the architecture | VALIDATION | — | — | explicit override |
| CAP-1159 | 1159 | 3 | 34.28 What v0.34 Actually Proves | v0.34 — ARGUMENT | VALIDATION | — | — | explicit override |
| CAP-1160 | 1160 | 3 | 34.28 What v0.34 Actually Proves | v0.34 — OPEN | VALIDATION | — | — | explicit override |
| CAP-1161 | 1161 | 1 | — | v0.34 — 34.29 Prototype Boundary | LIMITATIONS | — | — | explicit override |
| CAP-1162 | 1162 | 1 | — | v0.34 — 34.30 v0.34 → v0.35 | ROADMAP | — | — | — |
| CAP-1163 | 1163 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-1164 | 1164 | 1 | — | v0.34 — Conclusion — Generic Discovery Engine | DISCOVERY | — | — | — |
| CAP-1165 | 1165 | 2 | Conclusion — Generic Discovery Engine | v0.34 — The decisive conceptual shift | CONCEPT | — | — | — |
| CAP-1166 | 1166 | 3 | The decisive conceptual shift | v0.34 — DVB blind scan | DVB_ANALOGY | — | — | — |
| CAP-1167 | 1167 | 3 | The decisive conceptual shift | v0.34 — Generic discovery | DISCOVERY | — | — | — |
| CAP-1168 | 1168 | 1 | — | v0.34 — The major architectural invariants | VALIDATION | — | — | — |
| CAP-1169 | 1169 | 1 | — | v0.34 — Final architecture by responsibility | ARCHITECTURE | — | — | — |
| CAP-1170 | 1170 | 1 | — | v0.34 — What the prototype actually becomes | CONCEPT | — | — | — |
| CAP-1171 | 1171 | 1 | — | v0.34 — Final formulation | CONCEPT | — | — | — |

## Duplicates

Recorded per specification sections 12–13.

```yaml
duplicate:
  canonical: "docs/prototype/versions/01-v0.1.0.md, docs/prototype/versions/02-v0.2.0.md"
  source_sections:
    - CAP-001
    - USP-065
    - USP-066
    - USP-069
    - USP-070
  action: KEEP_BOTH
  reason: >-
    The two copies are damaged differently (line breaks lost in the paste;
    `@match *://*/*` rendered as `_://_/*` in the prototype document), so they
    express conflicting bytes for the same script. Merged information instead of
    deleted: the difference is recorded in both copies and in REVIEW-NOTES.md.
```

| Set | Sections | Content |
| --- | --- | --- |
| A ∩ B | `CAP-001`, `USP-065`, `USP-066`, `USP-069`, `USP-070` | the v0.1.0 and v0.2.0 userscripts |
| A − B | `USP-065`, `USP-066`, `USP-069`, `USP-070` | internal line breaks and indentation |
| B − A | `CAP-001` | the undamaged `@match *://*/*` directive |

## Heading normalization

Mechanically applied (specification section 16):

1. Every section keeps its original heading wording.
2. Sections extracted from `Continue Architecture Planning.md` are prefixed with the version they belong to (`v0.13 — 3. DiscoveryTask`) so that headings stay intelligible outside their original document. The prefix is metadata, not a wording change; both forms are recorded in *Section records* above.
3. Heading levels are shifted so that each destination file has exactly one `H1` and no level jumps.
4. One heading was renamed because its section was split at existing numbered boundaries:

| ID | Old heading | New heading | Reason |
| --- | --- | --- | --- |
| USP-071 | What changed | What changed — 1. Concurrent claiming is now explicit | section split at its existing `**1.** / **2.** / **3.**` boundaries |
| USP-072 | What changed | What changed — 2. HTML is no longer special | section split at its existing `**1.** / **2.** / **3.**` boundaries |
| USP-073 | What changed | What changed — 3. The actual scope is now explicit | section split at its existing `**1.** / **2.** / **3.**` boundaries |

## Related Documents

- [Documentation index](README.md)
- [Review Notes](REVIEW-NOTES.md)
- [Prototype Overview](prototype/overview.md)
- [Architecture Overview](architecture/overview.md)

