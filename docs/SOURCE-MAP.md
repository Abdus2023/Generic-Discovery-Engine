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
| UNVERIFIED | 81 |
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
| [`acquisition/acquisition-model.md`](acquisition/acquisition-model.md) | 8 | 8073 |
| [`acquisition/overview.md`](acquisition/overview.md) | 3 | 3176 |
| [`acquisition/response-recognition.md`](acquisition/response-recognition.md) | 24 | 22561 |
| [`acquisition/runtime.md`](acquisition/runtime.md) | 18 | 17311 |
| [`architecture/candidate-model.md`](architecture/candidate-model.md) | 9 | 8235 |
| [`architecture/capability-model.md`](architecture/capability-model.md) | 17 | 17474 |
| [`architecture/classification.md`](architecture/classification.md) | 23 | 25448 |
| [`architecture/concurrency.md`](architecture/concurrency.md) | 36 | 35648 |
| [`architecture/coordination.md`](architecture/coordination.md) | 38 | 35580 |
| [`architecture/coverage-and-absence.md`](architecture/coverage-and-absence.md) | 50 | 52291 |
| [`architecture/discovery-model.md`](architecture/discovery-model.md) | 26 | 31025 |
| [`architecture/evidence-model.md`](architecture/evidence-model.md) | 41 | 29988 |
| [`architecture/goal-and-query.md`](architecture/goal-and-query.md) | 64 | 60471 |
| [`architecture/observation-model.md`](architecture/observation-model.md) | 13 | 8746 |
| [`architecture/overview.md`](architecture/overview.md) | 1 | 3097 |
| [`architecture/persistence-and-recovery.md`](architecture/persistence-and-recovery.md) | 32 | 26646 |
| [`architecture/provenance.md`](architecture/provenance.md) | 12 | 10770 |
| [`architecture/provider-architecture.md`](architecture/provider-architecture.md) | 13 | 11069 |
| [`architecture/resource-budget.md`](architecture/resource-budget.md) | 24 | 22221 |
| [`architecture/resource-model.md`](architecture/resource-model.md) | 81 | 63141 |
| [`architecture/scheduler.md`](architecture/scheduler.md) | 11 | 9640 |
| [`architecture/search-space.md`](architecture/search-space.md) | 106 | 82675 |
| [`architecture/sessions-and-domains.md`](architecture/sessions-and-domains.md) | 31 | 24332 |
| [`architecture/strategy-and-planning.md`](architecture/strategy-and-planning.md) | 101 | 82143 |
| [`architecture/system-model.md`](architecture/system-model.md) | 36 | 90466 |
| [`architecture/work-and-frontier.md`](architecture/work-and-frontier.md) | 52 | 50668 |
| [`concepts/discovery-loop.md`](concepts/discovery-loop.md) | 9 | 6879 |
| [`concepts/generic-discovery.md`](concepts/generic-discovery.md) | 8 | 10437 |
| [`concepts/overview.md`](concepts/overview.md) | 16 | 24997 |
| [`prototype/limitations.md`](prototype/limitations.md) | 5 | 7106 |
| [`prototype/overview.md`](prototype/overview.md) | 2 | 5329 |
| [`prototype/userscript.md`](prototype/userscript.md) | 14 | 21951 |
| [`prototype/versions/00-v0.1.0-and-v0.2.0-paste.md`](prototype/versions/00-v0.1.0-and-v0.2.0-paste.md) | 1 | 59477 |
| [`prototype/versions/01-v0.1.0.md`](prototype/versions/01-v0.1.0.md) | 2 | 25127 |
| [`prototype/versions/02-v0.2.0.md`](prototype/versions/02-v0.2.0.md) | 2 | 37960 |
| [`prototype/versions/03-v0.3.0.md`](prototype/versions/03-v0.3.0.md) | 2 | 69922 |
| [`prototype/versions/04-v0.4.0-plan.md`](prototype/versions/04-v0.4.0-plan.md) | 2 | 5068 |
| [`prototype/versions/05-v0.4.0.md`](prototype/versions/05-v0.4.0.md) | 2 | 109976 |
| [`prototype/versions/06-v0.5.0.md`](prototype/versions/06-v0.5.0.md) | 1 | 160286 |
| [`prototype/versions/07-v0.4.0-second-iteration.md`](prototype/versions/07-v0.4.0-second-iteration.md) | 1 | 126404 |
| [`prototype/versions/08-v0.5.0-plan.md`](prototype/versions/08-v0.5.0-plan.md) | 1 | 3125 |
| [`prototype/versions/09-v0.5.0-second-iteration.md`](prototype/versions/09-v0.5.0-second-iteration.md) | 1 | 124748 |
| [`prototype/versions/10-v0.6.0.md`](prototype/versions/10-v0.6.0.md) | 1 | 163769 |
| [`prototype/versions/11-v0.5.0-third-iteration.md`](prototype/versions/11-v0.5.0-third-iteration.md) | 1 | 156293 |
| [`prototype/versions/12-v0.6.0-second-iteration.md`](prototype/versions/12-v0.6.0-second-iteration.md) | 1 | 219816 |
| [`prototype/versions/13-v0.6.0-third-iteration.md`](prototype/versions/13-v0.6.0-third-iteration.md) | 1 | 146782 |
| [`prototype/versions/14-v0.7.1.md`](prototype/versions/14-v0.7.1.md) | 1 | 143722 |
| [`providers/candidate-sources.md`](providers/candidate-sources.md) | 22 | 19413 |
| [`providers/overview.md`](providers/overview.md) | 3 | 4589 |
| [`research/dvb-blind-scan.md`](research/dvb-blind-scan.md) | 15 | 15936 |
| [`roadmap/future-work.md`](roadmap/future-work.md) | 16 | 22438 |
| [`validation/failure-taxonomy.md`](validation/failure-taxonomy.md) | 17 | 17869 |
| [`validation/invariants.md`](validation/invariants.md) | 176 | 71928 |
| [`validation/verification.md`](validation/verification.md) | 7 | 5007 |

## Mapping

| ID | Source | Original Heading | Destination | Action | Status |
| --- | --- | --- | --- | --- | --- |
| USP-001 | `Userscript Discovery Prototype.md` | *turn 0 you lead-in* | `docs/research/dvb-blind-scan.md` | MOVE | DESIGNED |
| USP-002 | `Userscript Discovery Prototype.md` | *turn 1 chatgpt lead-in* | `docs/research/dvb-blind-scan.md` | MOVE | DESIGNED |
| USP-003 | `Userscript Discovery Prototype.md` | Generic pseudocode | `docs/research/dvb-blind-scan.md` | MOVE | DESIGNED |
| USP-004 | `Userscript Discovery Prototype.md` | Making it genuinely generic | `docs/concepts/generic-discovery.md` | MOVE | DESIGNED |
| USP-005 | `Userscript Discovery Prototype.md` | *turn 2 you lead-in* | — | ARCHIVE | UNVERIFIED |
| USP-006 | `Userscript Discovery Prototype.md` | *turn 3 chatgpt lead-in* | `docs/concepts/generic-discovery.md` | MOVE | DESIGNED |
| USP-007 | `Userscript Discovery Prototype.md` | 1. Separate the layers | `docs/concepts/generic-discovery.md` | MOVE | DESIGNED |
| USP-008 | `Userscript Discovery Prototype.md` | 2. Candidate generation | `docs/architecture/candidate-model.md` | MOVE | DESIGNED |
| USP-009 | `Userscript Discovery Prototype.md` | 3. Detection should precede expensive decoding | `docs/acquisition/overview.md` | MOVE | DESIGNED |
| USP-010 | `Userscript Discovery Prototype.md` | 4. Lock is not discovery | `docs/acquisition/response-recognition.md` | MOVE | DESIGNED |
| USP-011 | `Userscript Discovery Prototype.md` | 5. Use DVB metadata to escape blind mode | `docs/research/dvb-blind-scan.md` | MOVE | DESIGNED |
| USP-012 | `Userscript Discovery Prototype.md` | 6. Deduplication | `docs/architecture/candidate-model.md` | MOVE | DESIGNED |
| USP-013 | `Userscript Discovery Prototype.md` | 7. Generic algorithm | `docs/concepts/generic-discovery.md` | MOVE | DESIGNED |
| USP-014 | `Userscript Discovery Prototype.md` | The key insight | `docs/concepts/generic-discovery.md` | MOVE | DESIGNED |
| USP-015 | `Userscript Discovery Prototype.md` | *turn 4 you lead-in* | — | ARCHIVE | UNVERIFIED |
| USP-016 | `Userscript Discovery Prototype.md` | *turn 5 chatgpt lead-in* | `docs/concepts/discovery-loop.md` | MOVE | DESIGNED |
| USP-017 | `Userscript Discovery Prototype.md` | 8. Model scanning as a search problem | `docs/concepts/discovery-loop.md` | MOVE | DESIGNED |
| USP-018 | `Userscript Discovery Prototype.md` | 9. Coarse-to-fine search | `docs/concepts/discovery-loop.md` | MOVE | DESIGNED |
| USP-019 | `Userscript Discovery Prototype.md` | 10. Confidence rather than binary decisions | `docs/architecture/discovery-model.md` | MOVE | DESIGNED |
| USP-020 | `Userscript Discovery Prototype.md` | 11. Don't immediately discard failed candidates | `docs/architecture/scheduler.md` | MOVE | DESIGNED |
| USP-021 | `Userscript Discovery Prototype.md` | 12. Adaptive retry | `docs/architecture/scheduler.md` | MOVE | DESIGNED |
| USP-022 | `Userscript Discovery Prototype.md` | 13. Scheduling becomes important | `docs/architecture/scheduler.md` | MOVE | DESIGNED |
| USP-023 | `Userscript Discovery Prototype.md` | 14. Discovery database | `docs/architecture/system-model.md` | MOVE | DESIGNED |
| USP-024 | `Userscript Discovery Prototype.md` | 15. The generic discovery abstraction | `docs/concepts/generic-discovery.md` | MOVE | DESIGNED |
| USP-025 | `Userscript Discovery Prototype.md` | *turn 6 you lead-in* | — | ARCHIVE | UNVERIFIED |
| USP-026 | `Userscript Discovery Prototype.md` | *turn 7 chatgpt lead-in* | `docs/architecture/discovery-model.md` | MOVE | DESIGNED |
| USP-027 | `Userscript Discovery Prototype.md` | 16. Discovery should have evidence levels | `docs/architecture/discovery-model.md` | MOVE | DESIGNED |
| USP-028 | `Userscript Discovery Prototype.md` | 17. Use observations to update the search space | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| USP-029 | `Userscript Discovery Prototype.md` | 18. Termination | `docs/concepts/discovery-loop.md` | MOVE | DESIGNED |
| USP-030 | `Userscript Discovery Prototype.md` | Exhaustive scan | `docs/concepts/discovery-loop.md` | MOVE | DESIGNED |
| USP-031 | `Userscript Discovery Prototype.md` | Confidence-based scan | `docs/concepts/discovery-loop.md` | MOVE | DESIGNED |
| USP-032 | `Userscript Discovery Prototype.md` | Time-bounded scan | `docs/concepts/discovery-loop.md` | MOVE | DESIGNED |
| USP-033 | `Userscript Discovery Prototype.md` | Hybrid | `docs/concepts/discovery-loop.md` | MOVE | DESIGNED |
| USP-034 | `Userscript Discovery Prototype.md` | 19. Coverage is a better metric than elapsed time | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| USP-035 | `Userscript Discovery Prototype.md` | 20. Cache knowledge between scans | `docs/architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| USP-036 | `Userscript Discovery Prototype.md` | 21. Handle disappearing multiplexes | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| USP-037 | `Userscript Discovery Prototype.md` | 22. The complete conceptual algorithm | `docs/concepts/discovery-loop.md` | MOVE | DESIGNED |
| USP-038 | `Userscript Discovery Prototype.md` | 23. A useful formal name | `docs/concepts/generic-discovery.md` | MOVE | DESIGNED |
| USP-039 | `Userscript Discovery Prototype.md` | *turn 8 you lead-in* | — | ARCHIVE | UNVERIFIED |
| USP-040 | `Userscript Discovery Prototype.md` | *turn 9 chatgpt lead-in* | `docs/architecture/discovery-model.md` | MOVE | DESIGNED |
| USP-041 | `Userscript Discovery Prototype.md` | 24. Two-dimensional discovery | `docs/architecture/discovery-model.md` | MOVE | DESIGNED |
| USP-042 | `Userscript Discovery Prototype.md` | 25. Candidate lifecycle | `docs/architecture/candidate-model.md` | MOVE | DESIGNED |
| USP-043 | `Userscript Discovery Prototype.md` | 26. Discovery becomes a graph | `docs/architecture/discovery-model.md` | MOVE | DESIGNED |
| USP-044 | `Userscript Discovery Prototype.md` | 27. This helps with incremental scanning | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| USP-045 | `Userscript Discovery Prototype.md` | 28. Parameter provenance | `docs/architecture/provenance.md` | MOVE | DESIGNED |
| USP-046 | `Userscript Discovery Prototype.md` | 29. The scanner should produce an explanation | `docs/architecture/provenance.md` | MOVE | DESIGNED |
| USP-047 | `Userscript Discovery Prototype.md` | 30. The final abstraction | `docs/concepts/generic-discovery.md` | MOVE | DESIGNED |
| USP-048 | `Userscript Discovery Prototype.md` | *turn 10 you lead-in* | — | ARCHIVE | UNVERIFIED |
| USP-049 | `Userscript Discovery Prototype.md` | *turn 11 chatgpt lead-in* | `docs/architecture/system-model.md` | MOVE | DESIGNED |
| USP-050 | `Userscript Discovery Prototype.md` | 31. Define the core objects | `docs/architecture/system-model.md` | MOVE | DESIGNED |
| USP-051 | `Userscript Discovery Prototype.md` | Candidate | `docs/architecture/candidate-model.md` | MOVE | DESIGNED |
| USP-052 | `Userscript Discovery Prototype.md` | Observation | `docs/architecture/observation-model.md` | MOVE | DESIGNED |
| USP-053 | `Userscript Discovery Prototype.md` | LockResult | `docs/acquisition/response-recognition.md` | MOVE | DESIGNED |
| USP-054 | `Userscript Discovery Prototype.md` | Discovery | `docs/architecture/discovery-model.md` | MOVE | DESIGNED |
| USP-055 | `Userscript Discovery Prototype.md` | 32. Use capability-driven adapters | `docs/architecture/provider-architecture.md` | MOVE | DESIGNED |
| USP-056 | `Userscript Discovery Prototype.md` | 33. Discovery strategies should also be pluggable | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| USP-057 | `Userscript Discovery Prototype.md` | 34. Don't confuse candidate identity with reception identity | `docs/architecture/candidate-model.md` | MOVE | DESIGNED |
| USP-058 | `Userscript Discovery Prototype.md` | 35. Make deduplication hierarchical | `docs/architecture/candidate-model.md` | MOVE | DESIGNED |
| USP-059 | `Userscript Discovery Prototype.md` | 36. Treat metadata as a candidate generator | `docs/architecture/candidate-model.md` | MOVE | DESIGNED |
| USP-060 | `Userscript Discovery Prototype.md` | 37. Candidate provenance creates a discovery tree | `docs/architecture/provenance.md` | MOVE | DESIGNED |
| USP-061 | `Userscript Discovery Prototype.md` | 38. Avoid infinite candidate generation | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| USP-062 | `Userscript Discovery Prototype.md` | 39. A practical scheduler | `docs/architecture/scheduler.md` | MOVE | DESIGNED |
| USP-063 | `Userscript Discovery Prototype.md` | 40. The engine can now become event-driven | `docs/architecture/system-model.md` | MOVE | DESIGNED |
| USP-064 | `Userscript Discovery Prototype.md` | 41. The resulting architecture | `docs/architecture/overview.md` | MOVE | DESIGNED |
| USP-065 | `Userscript Discovery Prototype.md` | *turn 12 you lead-in* | `docs/prototype/versions/01-v0.1.0.md` | MOVE | UNVERIFIED |
| USP-066 | `Userscript Discovery Prototype.md` | *turn 13 chatgpt lead-in* | `docs/prototype/versions/01-v0.1.0.md` | MOVE | UNVERIFIED |
| USP-067 | `Userscript Discovery Prototype.md` | *turn 13 chatgpt lead-in* | `docs/prototype/overview.md` | MOVE | UNVERIFIED |
| USP-068 | `Userscript Discovery Prototype.md` | The DVB analogy | `docs/research/dvb-blind-scan.md` | MOVE | DESIGNED |
| USP-069 | `Userscript Discovery Prototype.md` | *turn 14 you lead-in* | `docs/prototype/versions/02-v0.2.0.md` | MOVE | UNVERIFIED |
| USP-070 | `Userscript Discovery Prototype.md` | *turn 15 chatgpt lead-in* | `docs/prototype/versions/02-v0.2.0.md` | MOVE | UNVERIFIED |
| USP-071 | `Userscript Discovery Prototype.md` | What changed — 1. Concurrent claiming is now explicit | `docs/architecture/concurrency.md` | MOVE | DESIGNED |
| USP-072 | `Userscript Discovery Prototype.md` | What changed — 2. HTML is no longer special | `docs/providers/overview.md` | MOVE | DESIGNED |
| USP-073 | `Userscript Discovery Prototype.md` | What changed — 3. The actual scope is now explicit | `docs/prototype/limitations.md` | MOVE | UNVERIFIED |
| CAP-001 | `Continue Architecture Planning.md` | *turn 0 you lead-in* | `docs/prototype/versions/00-v0.1.0-and-v0.2.0-paste.md` | DUPLICATE | UNVERIFIED |
| CAP-002 | `Continue Architecture Planning.md` | *turn 1 chatgpt lead-in* | `docs/prototype/overview.md` | MOVE | UNVERIFIED |
| CAP-003 | `Continue Architecture Planning.md` | *turn 2 you lead-in* | `docs/prototype/versions/03-v0.3.0.md` | MOVE | UNVERIFIED |
| CAP-004 | `Continue Architecture Planning.md` | *turn 3 chatgpt lead-in* | `docs/prototype/versions/03-v0.3.0.md` | MOVE | UNVERIFIED |
| CAP-005 | `Continue Architecture Planning.md` | What changed from v0.2.0 | `docs/prototype/userscript.md` | MOVE | UNVERIFIED |
| CAP-006 | `Continue Architecture Planning.md` | *turn 4 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-007 | `Continue Architecture Planning.md` | *turn 5 chatgpt lead-in* | `docs/prototype/versions/04-v0.4.0-plan.md` | MOVE | FUTURE |
| CAP-008 | `Continue Architecture Planning.md` | The biggest v0.4 improvement | `docs/prototype/versions/04-v0.4.0-plan.md` | MOVE | FUTURE |
| CAP-009 | `Continue Architecture Planning.md` | *turn 6 you lead-in* | `docs/prototype/versions/05-v0.4.0.md` | MOVE | UNVERIFIED |
| CAP-010 | `Continue Architecture Planning.md` | *turn 7 chatgpt lead-in* | `docs/prototype/versions/05-v0.4.0.md` | MOVE | UNVERIFIED |
| CAP-011 | `Continue Architecture Planning.md` | Notable v0.4.0 behavior | `docs/prototype/userscript.md` | MOVE | UNVERIFIED |
| CAP-012 | `Continue Architecture Planning.md` | *turn 8 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-013 | `Continue Architecture Planning.md` | *turn 9 chatgpt lead-in* | `docs/prototype/versions/06-v0.5.0.md` | MOVE | UNVERIFIED |
| CAP-014 | `Continue Architecture Planning.md` | *turn 9 chatgpt lead-in* | `docs/prototype/userscript.md` | MOVE | UNVERIFIED |
| CAP-015 | `Continue Architecture Planning.md` | *turn 10 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-016 | `Continue Architecture Planning.md` | *turn 11 chatgpt lead-in* | `docs/prototype/versions/07-v0.4.0-second-iteration.md` | MOVE | UNVERIFIED |
| CAP-017 | `Continue Architecture Planning.md` | What changed from v0.3.0 | `docs/prototype/userscript.md` | MOVE | UNVERIFIED |
| CAP-018 | `Continue Architecture Planning.md` | *turn 12 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-019 | `Continue Architecture Planning.md` | *turn 13 chatgpt lead-in* | `docs/prototype/versions/08-v0.5.0-plan.md` | MOVE | FUTURE |
| CAP-020 | `Continue Architecture Planning.md` | *turn 14 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-021 | `Continue Architecture Planning.md` | *turn 15 chatgpt lead-in* | `docs/prototype/versions/09-v0.5.0-second-iteration.md` | MOVE | UNVERIFIED |
| CAP-022 | `Continue Architecture Planning.md` | v0.5 architecture | `docs/prototype/userscript.md` | MOVE | UNVERIFIED |
| CAP-023 | `Continue Architecture Planning.md` | *turn 16 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-024 | `Continue Architecture Planning.md` | *turn 17 chatgpt lead-in* | `docs/prototype/versions/10-v0.6.0.md` | MOVE | UNVERIFIED |
| CAP-025 | `Continue Architecture Planning.md` | What v0.6 changes architecturally | `docs/prototype/userscript.md` | MOVE | UNVERIFIED |
| CAP-026 | `Continue Architecture Planning.md` | *turn 18 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-027 | `Continue Architecture Planning.md` | *turn 19 chatgpt lead-in* | `docs/prototype/versions/11-v0.5.0-third-iteration.md` | MOVE | UNVERIFIED |
| CAP-028 | `Continue Architecture Planning.md` | What v0.5.0 changes architecturally | `docs/prototype/userscript.md` | MOVE | UNVERIFIED |
| CAP-029 | `Continue Architecture Planning.md` | *turn 20 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-030 | `Continue Architecture Planning.md` | *turn 21 chatgpt lead-in* | `docs/prototype/versions/12-v0.6.0-second-iteration.md` | MOVE | UNVERIFIED |
| CAP-031 | `Continue Architecture Planning.md` | v0.6.0's main architectural additions | `docs/prototype/userscript.md` | MOVE | UNVERIFIED |
| CAP-032 | `Continue Architecture Planning.md` | *turn 22 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-033 | `Continue Architecture Planning.md` | *turn 23 chatgpt lead-in* | `docs/prototype/versions/13-v0.6.0-third-iteration.md` | MOVE | UNVERIFIED |
| CAP-034 | `Continue Architecture Planning.md` | What changed in v0.6 | `docs/prototype/userscript.md` | MOVE | UNVERIFIED |
| CAP-035 | `Continue Architecture Planning.md` | *turn 24 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-036 | `Continue Architecture Planning.md` | v0.7.0 — Discovery Graph + Acquisition Planner | `docs/architecture/discovery-model.md` | MOVE | DESIGNED |
| CAP-037 | `Continue Architecture Planning.md` | v0.7 objectives | `docs/architecture/discovery-model.md` | MOVE | DESIGNED |
| CAP-038 | `Continue Architecture Planning.md` | Core contract | `docs/architecture/discovery-model.md` | MOVE | DESIGNED |
| CAP-039 | `Continue Architecture Planning.md` | Important v0.7 distinction | `docs/architecture/discovery-model.md` | MOVE | DESIGNED |
| CAP-040 | `Continue Architecture Planning.md` | v0.7 state machine | `docs/architecture/discovery-model.md` | MOVE | DESIGNED |
| CAP-041 | `Continue Architecture Planning.md` | The deeper abstraction | `docs/concepts/overview.md` | MOVE | DESIGNED |
| CAP-042 | `Continue Architecture Planning.md` | *turn 26 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-043 | `Continue Architecture Planning.md` | *turn 27 chatgpt lead-in* | `docs/prototype/versions/14-v0.7.1.md` | MOVE | UNVERIFIED |
| CAP-044 | `Continue Architecture Planning.md` | *turn 27 chatgpt lead-in* | `docs/prototype/userscript.md` | MOVE | UNVERIFIED |
| CAP-045 | `Continue Architecture Planning.md` | What v0.7.1 actually changes | `docs/prototype/userscript.md` | MOVE | UNVERIFIED |
| CAP-046 | `Continue Architecture Planning.md` | Before | `docs/prototype/userscript.md` | MOVE | UNVERIFIED |
| CAP-047 | `Continue Architecture Planning.md` | Now | `docs/prototype/userscript.md` | MOVE | UNVERIFIED |
| CAP-048 | `Continue Architecture Planning.md` | 2. The ledger becomes the scan's causal trace | `docs/architecture/provenance.md` | MOVE | DESIGNED |
| CAP-049 | `Continue Architecture Planning.md` | 3. PerformanceObserver correction | `docs/architecture/observation-model.md` | MOVE | DESIGNED |
| CAP-050 | `Continue Architecture Planning.md` | 4. Candidate state machine | `docs/prototype/userscript.md` | MOVE | UNVERIFIED |
| CAP-051 | `Continue Architecture Planning.md` | 5. The ledger is not merely logging | `docs/architecture/provenance.md` | MOVE | DESIGNED |
| CAP-052 | `Continue Architecture Planning.md` | 6. One remaining architectural limitation | `docs/prototype/limitations.md` | MOVE | OPEN |
| CAP-053 | `Continue Architecture Planning.md` | 7. Architecture after v0.7.1 | `docs/architecture/system-model.md` | MOVE | DESIGNED |
| CAP-054 | `Continue Architecture Planning.md` | Next boundary: v0.8 | `docs/roadmap/future-work.md` | MOVE | FUTURE |
| CAP-055 | `Continue Architecture Planning.md` | *turn 28 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-056 | `Continue Architecture Planning.md` | v0.8 — Capability-Aware Acquisition Runtime | `docs/architecture/capability-model.md` | MOVE | DESIGNED |
| CAP-057 | `Continue Architecture Planning.md` | 1. The three graphs | `docs/architecture/capability-model.md` | MOVE | DESIGNED |
| CAP-058 | `Continue Architecture Planning.md` | Discovery graph | `docs/architecture/capability-model.md` | MOVE | DESIGNED |
| CAP-059 | `Continue Architecture Planning.md` | Acquisition graph | `docs/acquisition/acquisition-model.md` | MOVE | DESIGNED |
| CAP-060 | `Continue Architecture Planning.md` | Evidence graph | `docs/architecture/capability-model.md` | MOVE | DESIGNED |
| CAP-061 | `Continue Architecture Planning.md` | 2. Capability is now a first-class object | `docs/architecture/capability-model.md` | MOVE | DESIGNED |
| CAP-062 | `Continue Architecture Planning.md` | 3. Capability lattice | `docs/architecture/capability-model.md` | MOVE | DESIGNED |
| CAP-063 | `Continue Architecture Planning.md` | 4. Capability contract | `docs/architecture/capability-model.md` | MOVE | DESIGNED |
| CAP-064 | `Continue Architecture Planning.md` | 5. Candidate requirements | `docs/architecture/capability-model.md` | MOVE | DESIGNED |
| CAP-065 | `Continue Architecture Planning.md` | 6. Acquisition planning becomes capability resolution | `docs/acquisition/acquisition-model.md` | MOVE | DESIGNED |
| CAP-066 | `Continue Architecture Planning.md` | 7. Why this matters for generic discovery | `docs/architecture/capability-model.md` | MOVE | DESIGNED |
| CAP-067 | `Continue Architecture Planning.md` | 8. AcquisitionPlan v0.8 | `docs/acquisition/acquisition-model.md` | MOVE | DESIGNED |
| CAP-068 | `Continue Architecture Planning.md` | 9. Capability provenance | `docs/architecture/capability-model.md` | MOVE | DESIGNED |
| CAP-069 | `Continue Architecture Planning.md` | 10. The four-level authorization model | `docs/architecture/capability-model.md` | MOVE | DESIGNED |
| CAP-070 | `Continue Architecture Planning.md` | 11. New graph model | `docs/architecture/capability-model.md` | MOVE | DESIGNED |
| CAP-071 | `Continue Architecture Planning.md` | 12. v0.8 ledger | `docs/architecture/capability-model.md` | MOVE | DESIGNED |
| CAP-072 | `Continue Architecture Planning.md` | 13. Important architectural consequence | `docs/architecture/capability-model.md` | MOVE | DESIGNED |
| CAP-073 | `Continue Architecture Planning.md` | 14. v0.8 scope boundary | `docs/architecture/capability-model.md` | MOVE | DESIGNED |
| CAP-074 | `Continue Architecture Planning.md` | Implement | `docs/architecture/capability-model.md` | MOVE | DESIGNED |
| CAP-075 | `Continue Architecture Planning.md` | Represent but deny | `docs/architecture/capability-model.md` | MOVE | DESIGNED |
| CAP-076 | `Continue Architecture Planning.md` | 15. Updated system invariant | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-077 | `Continue Architecture Planning.md` | 16. The DVB analogy is now cleaner | `docs/research/dvb-blind-scan.md` | MOVE | DESIGNED |
| CAP-078 | `Continue Architecture Planning.md` | 17. v0.8 → v0.9 | `docs/roadmap/future-work.md` | MOVE | FUTURE |
| CAP-079 | `Continue Architecture Planning.md` | *turn 30 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-080 | `Continue Architecture Planning.md` | v0.9 — Acquisition Provider Architecture | `docs/architecture/provider-architecture.md` | MOVE | DESIGNED |
| CAP-081 | `Continue Architecture Planning.md` | 0.9 architecture | `docs/architecture/system-model.md` | MOVE | DESIGNED |
| CAP-082 | `Continue Architecture Planning.md` | The important separation | `docs/acquisition/overview.md` | MOVE | DESIGNED |
| CAP-083 | `Continue Architecture Planning.md` | 1. AcquisitionProvider contract | `docs/architecture/provider-architecture.md` | MOVE | DESIGNED |
| CAP-084 | `Continue Architecture Planning.md` | 2. Provider capabilities | `docs/architecture/provider-architecture.md` | MOVE | DESIGNED |
| CAP-085 | `Continue Architecture Planning.md` | 3. Provider selection | `docs/architecture/provider-architecture.md` | MOVE | DESIGNED |
| CAP-086 | `Continue Architecture Planning.md` | 4. GM-XHR becomes a component | `docs/architecture/provider-architecture.md` | MOVE | DESIGNED |
| CAP-087 | `Continue Architecture Planning.md` | 5. Observation gets provider provenance | `docs/architecture/observation-model.md` | MOVE | DESIGNED |
| CAP-088 | `Continue Architecture Planning.md` | 6. Provider failure ≠ acquisition denial | `docs/architecture/provider-architecture.md` | MOVE | DESIGNED |
| CAP-089 | `Continue Architecture Planning.md` | Policy denial | `docs/architecture/provider-architecture.md` | MOVE | DESIGNED |
| CAP-090 | `Continue Architecture Planning.md` | Provider failure | `docs/architecture/provider-architecture.md` | MOVE | DESIGNED |
| CAP-091 | `Continue Architecture Planning.md` | 7. Provider selection itself becomes an event | `docs/architecture/provider-architecture.md` | MOVE | DESIGNED |
| CAP-092 | `Continue Architecture Planning.md` | 8. A deeper consequence: acquisition becomes replaceable | `docs/acquisition/overview.md` | MOVE | DESIGNED |
| CAP-093 | `Continue Architecture Planning.md` | Cache provider | `docs/architecture/provider-architecture.md` | MOVE | DESIGNED |
| CAP-094 | `Continue Architecture Planning.md` | Replay provider | `docs/architecture/provider-architecture.md` | MOVE | DESIGNED |
| CAP-095 | `Continue Architecture Planning.md` | 9. The engine is now approaching a general resource runtime | `docs/architecture/provider-architecture.md` | MOVE | DESIGNED |
| CAP-096 | `Continue Architecture Planning.md` | 10. v0.9 invariants | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-097 | `Continue Architecture Planning.md` | I1 — Discovery independence | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-098 | `Continue Architecture Planning.md` | I2 — Policy independence | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-099 | `Continue Architecture Planning.md` | I3 — Capability soundness | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-100 | `Continue Architecture Planning.md` | I4 — Method safety | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-101 | `Continue Architecture Planning.md` | I5 — Provenance | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-102 | `Continue Architecture Planning.md` | I6 — Observation integrity | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-103 | `Continue Architecture Planning.md` | I7 — Replay distinction | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-104 | `Continue Architecture Planning.md` | 11. The next problem is now visible | `docs/roadmap/future-work.md` | MOVE | FUTURE |
| CAP-105 | `Continue Architecture Planning.md` | *turn 32 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-106 | `Continue Architecture Planning.md` | v0.10 — Acquisition Runtime | `docs/acquisition/runtime.md` | MOVE | DESIGNED |
| CAP-107 | `Continue Architecture Planning.md` | 1. The new architecture | `docs/architecture/system-model.md` | MOVE | DESIGNED |
| CAP-108 | `Continue Architecture Planning.md` | 2. The key distinction: Scheduler vs Runtime | `docs/acquisition/runtime.md` | MOVE | DESIGNED |
| CAP-109 | `Continue Architecture Planning.md` | Scheduler | `docs/acquisition/runtime.md` | MOVE | DESIGNED |
| CAP-110 | `Continue Architecture Planning.md` | Runtime | `docs/acquisition/runtime.md` | MOVE | DESIGNED |
| CAP-111 | `Continue Architecture Planning.md` | 3. AcquisitionRuntime contract | `docs/acquisition/runtime.md` | MOVE | DESIGNED |
| CAP-112 | `Continue Architecture Planning.md` | 4. Admission control | `docs/acquisition/runtime.md` | MOVE | DESIGNED |
| CAP-113 | `Continue Architecture Planning.md` | 5. Budget becomes a first-class object | `docs/acquisition/runtime.md` | MOVE | DESIGNED |
| CAP-114 | `Continue Architecture Planning.md` | 6. Why reservation must precede execution | `docs/acquisition/runtime.md` | MOVE | DESIGNED |
| CAP-115 | `Continue Architecture Planning.md` | 7. OriginController | `docs/acquisition/runtime.md` | MOVE | DESIGNED |
| CAP-116 | `Continue Architecture Planning.md` | 8. Provider selection happens after admission prerequisites | `docs/acquisition/runtime.md` | MOVE | DESIGNED |
| CAP-117 | `Continue Architecture Planning.md` | 9. Provider must not own runtime policy | `docs/acquisition/runtime.md` | MOVE | DESIGNED |
| CAP-118 | `Continue Architecture Planning.md` | 10. Cancellation becomes explicit | `docs/acquisition/runtime.md` | MOVE | DESIGNED |
| CAP-119 | `Continue Architecture Planning.md` | 11. Timeout belongs to Runtime | `docs/acquisition/runtime.md` | MOVE | DESIGNED |
| CAP-120 | `Continue Architecture Planning.md` | 12. Retry belongs to Runtime | `docs/acquisition/runtime.md` | MOVE | DESIGNED |
| CAP-121 | `Continue Architecture Planning.md` | 13. Plan vs Attempt | `docs/acquisition/runtime.md` | MOVE | DESIGNED |
| CAP-122 | `Continue Architecture Planning.md` | 14. Runtime event model | `docs/acquisition/runtime.md` | MOVE | DESIGNED |
| CAP-123 | `Continue Architecture Planning.md` | 15. Runtime state machine | `docs/acquisition/runtime.md` | MOVE | DESIGNED |
| CAP-124 | `Continue Architecture Planning.md` | 16. The complete execution equation | `docs/acquisition/runtime.md` | MOVE | DESIGNED |
| CAP-125 | `Continue Architecture Planning.md` | 17. The resulting architecture | `docs/architecture/system-model.md` | MOVE | DESIGNED |
| CAP-126 | `Continue Architecture Planning.md` | What v0.10 accomplishes | `docs/concepts/overview.md` | MOVE | DESIGNED |
| CAP-127 | `Continue Architecture Planning.md` | Next boundary: v0.11 | `docs/roadmap/future-work.md` | MOVE | FUTURE |
| CAP-128 | `Continue Architecture Planning.md` | *turn 34 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-129 | `Continue Architecture Planning.md` | v0.11 — Response Recognition Runtime | `docs/acquisition/response-recognition.md` | MOVE | DESIGNED |
| CAP-130 | `Continue Architecture Planning.md` | 1. v0.11 architecture | `docs/architecture/system-model.md` | MOVE | DESIGNED |
| CAP-131 | `Continue Architecture Planning.md` | 2. RecognitionProvider contract | `docs/acquisition/response-recognition.md` | MOVE | DESIGNED |
| CAP-132 | `Continue Architecture Planning.md` | 3. Recognition is not discovery | `docs/acquisition/response-recognition.md` | MOVE | DESIGNED |
| CAP-133 | `Continue Architecture Planning.md` | 4. Response Router | `docs/acquisition/response-recognition.md` | MOVE | DESIGNED |
| CAP-134 | `Continue Architecture Planning.md` | 5. Provider priority | `docs/acquisition/response-recognition.md` | MOVE | DESIGNED |
| CAP-135 | `Continue Architecture Planning.md` | 6. Recognition confidence | `docs/acquisition/response-recognition.md` | MOVE | DESIGNED |
| CAP-136 | `Continue Architecture Planning.md` | 7. Content-type is only one signal | `docs/acquisition/response-recognition.md` | MOVE | DESIGNED |
| CAP-137 | `Continue Architecture Planning.md` | 8. Recognition evidence | `docs/acquisition/response-recognition.md` | MOVE | DESIGNED |
| CAP-138 | `Continue Architecture Planning.md` | 9. Recognition result contract | `docs/acquisition/response-recognition.md` | MOVE | DESIGNED |
| CAP-139 | `Continue Architecture Planning.md` | 10. Why providers should not enqueue candidates | `docs/acquisition/response-recognition.md` | MOVE | DESIGNED |
| CAP-140 | `Continue Architecture Planning.md` | 11. Recognition Runtime | `docs/acquisition/response-recognition.md` | MOVE | DESIGNED |
| CAP-141 | `Continue Architecture Planning.md` | 12. Recognition failure taxonomy | `docs/validation/failure-taxonomy.md` | MOVE | DESIGNED |
| CAP-142 | `Continue Architecture Planning.md` | No recognizer | `docs/acquisition/response-recognition.md` | MOVE | DESIGNED |
| CAP-143 | `Continue Architecture Planning.md` | Provider rejected | `docs/acquisition/response-recognition.md` | MOVE | DESIGNED |
| CAP-144 | `Continue Architecture Planning.md` | Provider error | `docs/acquisition/response-recognition.md` | MOVE | DESIGNED |
| CAP-145 | `Continue Architecture Planning.md` | Successful recognition, zero discoveries | `docs/acquisition/response-recognition.md` | MOVE | DESIGNED |
| CAP-146 | `Continue Architecture Planning.md` | 13. v0.11 state progression | `docs/acquisition/response-recognition.md` | MOVE | DESIGNED |
| CAP-147 | `Continue Architecture Planning.md` | 14. Multiple recognizers | `docs/acquisition/response-recognition.md` | MOVE | DESIGNED |
| CAP-148 | `Continue Architecture Planning.md` | 15. Recognition graph | `docs/acquisition/response-recognition.md` | MOVE | DESIGNED |
| CAP-149 | `Continue Architecture Planning.md` | 16. The graph is now explicitly causal | `docs/acquisition/response-recognition.md` | MOVE | DESIGNED |
| CAP-150 | `Continue Architecture Planning.md` | 17. v0.11 event ledger | `docs/acquisition/response-recognition.md` | MOVE | DESIGNED |
| CAP-151 | `Continue Architecture Planning.md` | 18. The emerging generic algorithm | `docs/acquisition/response-recognition.md` | MOVE | DESIGNED |
| CAP-152 | `Continue Architecture Planning.md` | 19. The next major abstraction: Candidate Sources | `docs/roadmap/future-work.md` | MOVE | FUTURE |
| CAP-153 | `Continue Architecture Planning.md` | *turn 36 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-154 | `Continue Architecture Planning.md` | v0.12 — Candidate Source Architecture | `docs/providers/candidate-sources.md` | MOVE | DESIGNED |
| CAP-155 | `Continue Architecture Planning.md` | 1. Three independent provider planes | `docs/providers/overview.md` | MOVE | DESIGNED |
| CAP-156 | `Continue Architecture Planning.md` | 2. CandidateSource contract | `docs/providers/candidate-sources.md` | MOVE | DESIGNED |
| CAP-157 | `Continue Architecture Planning.md` | 3. CandidateSource is a search-space adapter | `docs/providers/candidate-sources.md` | MOVE | DESIGNED |
| CAP-158 | `Continue Architecture Planning.md` | Web page | `docs/providers/candidate-sources.md` | MOVE | DESIGNED |
| CAP-159 | `Continue Architecture Planning.md` | Network traffic | `docs/providers/candidate-sources.md` | MOVE | DESIGNED |
| CAP-160 | `Continue Architecture Planning.md` | Sitemap | `docs/providers/candidate-sources.md` | MOVE | DESIGNED |
| CAP-161 | `Continue Architecture Planning.md` | User seed | `docs/providers/candidate-sources.md` | MOVE | DESIGNED |
| CAP-162 | `Continue Architecture Planning.md` | Document | `docs/providers/candidate-sources.md` | MOVE | DESIGNED |
| CAP-163 | `Continue Architecture Planning.md` | 4. CandidateProposal | `docs/providers/candidate-sources.md` | MOVE | DESIGNED |
| CAP-164 | `Continue Architecture Planning.md` | 5. Why proposals matter | `docs/providers/candidate-sources.md` | MOVE | DESIGNED |
| CAP-165 | `Continue Architecture Planning.md` | 6. CandidateNormalizer | `docs/providers/candidate-sources.md` | MOVE | DESIGNED |
| CAP-166 | `Continue Architecture Planning.md` | 7. Source Registry | `docs/providers/candidate-sources.md` | MOVE | DESIGNED |
| CAP-167 | `Continue Architecture Planning.md` | 8. The HTML provider should evolve | `docs/providers/overview.md` | MOVE | DESIGNED |
| CAP-168 | `Continue Architecture Planning.md` | 9. Evidence becomes an intermediate layer | `docs/providers/candidate-sources.md` | MOVE | DESIGNED |
| CAP-169 | `Continue Architecture Planning.md` | 10. Discovery becomes evidence-driven | `docs/providers/candidate-sources.md` | MOVE | DESIGNED |
| CAP-170 | `Continue Architecture Planning.md` | 11. CandidateSource context | `docs/providers/candidate-sources.md` | MOVE | DESIGNED |
| CAP-171 | `Continue Architecture Planning.md` | 12. CandidateSource examples | `docs/providers/candidate-sources.md` | MOVE | DESIGNED |
| CAP-172 | `Continue Architecture Planning.md` | HTML link source | `docs/providers/candidate-sources.md` | MOVE | DESIGNED |
| CAP-173 | `Continue Architecture Planning.md` | 13. NetworkSource | `docs/providers/candidate-sources.md` | MOVE | DESIGNED |
| CAP-174 | `Continue Architecture Planning.md` | 14. Search-space composition | `docs/providers/candidate-sources.md` | MOVE | DESIGNED |
| CAP-175 | `Continue Architecture Planning.md` | 15. Candidate identity | `docs/providers/candidate-sources.md` | MOVE | DESIGNED |
| CAP-176 | `Continue Architecture Planning.md` | 16. Discovery confidence aggregation | `docs/providers/candidate-sources.md` | MOVE | DESIGNED |
| CAP-177 | `Continue Architecture Planning.md` | 17. v0.12 provenance graph | `docs/providers/candidate-sources.md` | MOVE | DESIGNED |
| CAP-178 | `Continue Architecture Planning.md` | 18. v0.12 invariants | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-179 | `Continue Architecture Planning.md` | S1 — Source purity | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-180 | `Continue Architecture Planning.md` | S2 — Core ownership | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-181 | `Continue Architecture Planning.md` | S3 — Proposal semantics | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-182 | `Continue Architecture Planning.md` | S4 — Identity | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-183 | `Continue Architecture Planning.md` | S5 — Provenance | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-184 | `Continue Architecture Planning.md` | S6 — Representability | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-185 | `Continue Architecture Planning.md` | S7 — Observation independence | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-186 | `Continue Architecture Planning.md` | 19. The complete v0.12 architecture | `docs/architecture/system-model.md` | MOVE | DESIGNED |
| CAP-187 | `Continue Architecture Planning.md` | 20. The deeper abstraction | `docs/concepts/overview.md` | MOVE | DESIGNED |
| CAP-188 | `Continue Architecture Planning.md` | v0.13 — the next boundary | `docs/roadmap/future-work.md` | MOVE | FUTURE |
| CAP-189 | `Continue Architecture Planning.md` | *turn 38 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-190 | `Continue Architecture Planning.md` | v0.13 — Discovery Controller | `docs/architecture/discovery-model.md` | MOVE | DESIGNED |
| CAP-191 | `Continue Architecture Planning.md` | 1. The complete v0.13 architecture | `docs/architecture/system-model.md` | MOVE | DESIGNED |
| CAP-192 | `Continue Architecture Planning.md` | 2. Two schedulers, not one | `docs/architecture/scheduler.md` | MOVE | DESIGNED |
| CAP-193 | `Continue Architecture Planning.md` | 3. DiscoveryTask | `docs/architecture/discovery-model.md` | MOVE | DESIGNED |
| CAP-194 | `Continue Architecture Planning.md` | 4. Why a task is necessary | `docs/architecture/discovery-model.md` | MOVE | DESIGNED |
| CAP-195 | `Continue Architecture Planning.md` | 5. Source Policy | `docs/architecture/discovery-model.md` | MOVE | DESIGNED |
| CAP-196 | `Continue Architecture Planning.md` | 6. Source budgets | `docs/architecture/discovery-model.md` | MOVE | DESIGNED |
| CAP-197 | `Continue Architecture Planning.md` | 7. Proposal budget is different | `docs/architecture/discovery-model.md` | MOVE | DESIGNED |
| CAP-198 | `Continue Architecture Planning.md` | 8. Incremental sources | `docs/architecture/discovery-model.md` | MOVE | DESIGNED |
| CAP-199 | `Continue Architecture Planning.md` | 9. Source execution contract | `docs/architecture/discovery-model.md` | MOVE | DESIGNED |
| CAP-200 | `Continue Architecture Planning.md` | 10. Source scheduling | `docs/architecture/scheduler.md` | MOVE | DESIGNED |
| CAP-201 | `Continue Architecture Planning.md` | 11. Fairness | `docs/architecture/scheduler.md` | MOVE | DESIGNED |
| CAP-202 | `Continue Architecture Planning.md` | 12. Candidate deduplication belongs after normalization | `docs/architecture/candidate-model.md` | MOVE | DESIGNED |
| CAP-203 | `Continue Architecture Planning.md` | 13. Discovery provenance | `docs/architecture/provenance.md` | MOVE | DESIGNED |
| CAP-204 | `Continue Architecture Planning.md` | 14. Candidate generation becomes transactional | `docs/architecture/candidate-model.md` | MOVE | DESIGNED |
| CAP-205 | `Continue Architecture Planning.md` | 15. Concurrent source execution | `docs/architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-206 | `Continue Architecture Planning.md` | 16. DiscoveryController | `docs/architecture/discovery-model.md` | MOVE | DESIGNED |
| CAP-207 | `Continue Architecture Planning.md` | 17. Event ledger | `docs/architecture/discovery-model.md` | MOVE | DESIGNED |
| CAP-208 | `Continue Architecture Planning.md` | 18. Discovery failure taxonomy | `docs/validation/failure-taxonomy.md` | MOVE | DESIGNED |
| CAP-209 | `Continue Architecture Planning.md` | 19. The generic blind-scan analogy is now much stronger | `docs/research/dvb-blind-scan.md` | MOVE | DESIGNED |
| CAP-210 | `Continue Architecture Planning.md` | 20. v0.13 invariants | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-211 | `Continue Architecture Planning.md` | D1 — Source isolation | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-212 | `Continue Architecture Planning.md` | D2 — Acquisition isolation | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-213 | `Continue Architecture Planning.md` | D3 — Normalization ownership | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-214 | `Continue Architecture Planning.md` | D4 — Bounded generation | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-215 | `Continue Architecture Planning.md` | D5 — Bounded recursion | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-216 | `Continue Architecture Planning.md` | D6 — Provenance preservation | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-217 | `Continue Architecture Planning.md` | D7 — Atomic task claiming | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-218 | `Continue Architecture Planning.md` | D8 — Convergence | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-219 | `Continue Architecture Planning.md` | D9 — Discovery/acquisition independence | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-220 | `Continue Architecture Planning.md` | 21. The architecture is now approaching a stable core | `docs/architecture/system-model.md` | MOVE | DESIGNED |
| CAP-221 | `Continue Architecture Planning.md` | v0.14 — the next missing abstraction | `docs/roadmap/future-work.md` | MOVE | FUTURE |
| CAP-222 | `Continue Architecture Planning.md` | *turn 40 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-223 | `Continue Architecture Planning.md` | v0.14 — DiscoveryDomain + ScanSession | `docs/architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-224 | `Continue Architecture Planning.md` | 1. The conceptual split | `docs/architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-225 | `Continue Architecture Planning.md` | Discovery Engine | `docs/architecture/discovery-model.md` | MOVE | DESIGNED |
| CAP-226 | `Continue Architecture Planning.md` | DiscoveryDomain | `docs/architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-227 | `Continue Architecture Planning.md` | ScanSession | `docs/architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-228 | `Continue Architecture Planning.md` | 2. DVB analogy | `docs/research/dvb-blind-scan.md` | MOVE | DESIGNED |
| CAP-229 | `Continue Architecture Planning.md` | 3. DiscoveryDomain | `docs/architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-230 | `Continue Architecture Planning.md` | 4. Domain vs policy | `docs/architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-231 | `Continue Architecture Planning.md` | 5. Domain membership | `docs/architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-232 | `Continue Architecture Planning.md` | 6. Explicit seeds | `docs/architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-233 | `Continue Architecture Planning.md` | 7. Seed ≠ Candidate | `docs/architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-234 | `Continue Architecture Planning.md` | 8. Discovery frontier | `docs/architecture/discovery-model.md` | MOVE | DESIGNED |
| CAP-235 | `Continue Architecture Planning.md` | 9. ScanSession | `docs/architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-236 | `Continue Architecture Planning.md` | 10. Session lifecycle | `docs/architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-237 | `Continue Architecture Planning.md` | 11. Termination becomes explicit | `docs/architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-238 | `Continue Architecture Planning.md` | Frontier exhaustion | `docs/architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-239 | `Continue Architecture Planning.md` | Candidate limit | `docs/architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-240 | `Continue Architecture Planning.md` | Acquisition limit | `docs/architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-241 | `Continue Architecture Planning.md` | Discovery-task limit | `docs/architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-242 | `Continue Architecture Planning.md` | Proposal limit | `docs/architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-243 | `Continue Architecture Planning.md` | Depth limit | `docs/architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-244 | `Continue Architecture Planning.md` | Time limit | `docs/architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-245 | `Continue Architecture Planning.md` | External stop | `docs/architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-246 | `Continue Architecture Planning.md` | 12. Termination evaluator | `docs/architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-247 | `Continue Architecture Planning.md` | 13. Limit reached ≠ successful completion | `docs/architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-248 | `Continue Architecture Planning.md` | 14. The session snapshot | `docs/architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-249 | `Continue Architecture Planning.md` | 15. Resumability | `docs/architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-250 | `Continue Architecture Planning.md` | 16. Lease-based claims | `docs/architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-251 | `Continue Architecture Planning.md` | 17. Session ownership | `docs/architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-252 | `Continue Architecture Planning.md` | 18. Scan vs engine knowledge | `docs/architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-253 | `Continue Architecture Planning.md` | 19. Domain snapshot vs mutable domain | `docs/architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-254 | `Continue Architecture Planning.md` | 20. Domain identity | `docs/architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-255 | `Continue Architecture Planning.md` | 21. Search frontier vs knowledge graph | `docs/architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-256 | `Continue Architecture Planning.md` | 22. The complete v0.14 architecture | `docs/architecture/system-model.md` | MOVE | DESIGNED |
| CAP-257 | `Continue Architecture Planning.md` | 23. Four distinct scopes | `docs/architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-258 | `Continue Architecture Planning.md` | 24. Strong invariants | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-259 | `Continue Architecture Planning.md` | Domain invariant | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-260 | `Continue Architecture Planning.md` | Session invariant | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-261 | `Continue Architecture Planning.md` | Snapshot invariant | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-262 | `Continue Architecture Planning.md` | Frontier invariant | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-263 | `Continue Architecture Planning.md` | Termination invariant | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-264 | `Continue Architecture Planning.md` | Recovery invariant | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-265 | `Continue Architecture Planning.md` | Provenance invariant | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-266 | `Continue Architecture Planning.md` | Acquisition invariant | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-267 | `Continue Architecture Planning.md` | Discovery invariant | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-268 | `Continue Architecture Planning.md` | 25. Failure taxonomy | `docs/validation/failure-taxonomy.md` | MOVE | DESIGNED |
| CAP-269 | `Continue Architecture Planning.md` | 26. What v0.14 changes conceptually | `docs/architecture/sessions-and-domains.md` | MOVE | DESIGNED |
| CAP-270 | `Continue Architecture Planning.md` | 27. The next abstraction | `docs/roadmap/future-work.md` | MOVE | FUTURE |
| CAP-271 | `Continue Architecture Planning.md` | v0.15 — WorkItem + Frontier Runtime | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-272 | `Continue Architecture Planning.md` | *turn 42 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-273 | `Continue Architecture Planning.md` | v0.15 — WorkItem + Frontier Runtime | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-274 | `Continue Architecture Planning.md` | 1. The key distinction | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-275 | `Continue Architecture Planning.md` | 2. Why `WorkItem` exists | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-276 | `Continue Architecture Planning.md` | 3. WorkItem | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-277 | `Continue Architecture Planning.md` | 4. Work kinds | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-278 | `Continue Architecture Planning.md` | 5. Work payload | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-279 | `Continue Architecture Planning.md` | 6. Work lifecycle | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-280 | `Continue Architecture Planning.md` | 7. Claiming becomes a formal protocol | `docs/architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-281 | `Continue Architecture Planning.md` | 8. Work lease | `docs/architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-282 | `Continue Architecture Planning.md` | 9. Lease recovery | `docs/architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-283 | `Continue Architecture Planning.md` | 10. Frontier Runtime | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-284 | `Continue Architecture Planning.md` | 11. WorkScheduler | `docs/architecture/scheduler.md` | MOVE | DESIGNED |
| CAP-285 | `Continue Architecture Planning.md` | 12. Priority starvation | `docs/architecture/scheduler.md` | MOVE | DESIGNED |
| CAP-286 | `Continue Architecture Planning.md` | 13. Priority aging | `docs/architecture/scheduler.md` | MOVE | DESIGNED |
| CAP-287 | `Continue Architecture Planning.md` | 14. Discovery and acquisition fairness | `docs/acquisition/acquisition-model.md` | MOVE | DESIGNED |
| CAP-288 | `Continue Architecture Planning.md` | 15. Why not one giant queue? | `docs/architecture/work-and-frontier.md` | MOVE | OPEN |
| CAP-289 | `Continue Architecture Planning.md` | 16. Work dependencies | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-290 | `Continue Architecture Planning.md` | 17. But dependencies must not create hidden coupling | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-291 | `Continue Architecture Planning.md` | 18. Dependency states | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-292 | `Continue Architecture Planning.md` | 19. Work completion | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-293 | `Continue Architecture Planning.md` | 20. Work execution boundary | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-294 | `Continue Architecture Planning.md` | 21. Work Runtime | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-295 | `Continue Architecture Planning.md` | 22. Retry becomes generic | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-296 | `Continue Architecture Planning.md` | 23. Retry identity | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-297 | `Continue Architecture Planning.md` | 24. Cancellation | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-298 | `Continue Architecture Planning.md` | 25. Scan termination with WorkItems | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-299 | `Continue Architecture Planning.md` | 26. The three frontier states | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-300 | `Continue Architecture Planning.md` | 27. Scheduled work | `docs/architecture/scheduler.md` | MOVE | DESIGNED |
| CAP-301 | `Continue Architecture Planning.md` | 28. Work state machine | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-302 | `Continue Architecture Planning.md` | 29. Domain → Session → Work | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-303 | `Continue Architecture Planning.md` | 30. What belongs where? | `docs/architecture/work-and-frontier.md` | MOVE | OPEN |
| CAP-304 | `Continue Architecture Planning.md` | 31. The crucial invariant | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-305 | `Continue Architecture Planning.md` | 32. Discovery vs acquisition remains intact | `docs/acquisition/acquisition-model.md` | MOVE | DESIGNED |
| CAP-306 | `Continue Architecture Planning.md` | 33. The resulting architecture | `docs/architecture/system-model.md` | MOVE | DESIGNED |
| CAP-307 | `Continue Architecture Planning.md` | 34. v0.15 architectural result | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-308 | `Continue Architecture Planning.md` | *turn 44 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-309 | `Continue Architecture Planning.md` | v0.16 — EvidenceGraph + Provenance | `docs/architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-310 | `Continue Architecture Planning.md` | 1. The new abstraction | `docs/architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-311 | `Continue Architecture Planning.md` | 2. Observation ≠ Evidence ≠ Claim | `docs/architecture/observation-model.md` | MOVE | DESIGNED |
| CAP-312 | `Continue Architecture Planning.md` | Observation | `docs/architecture/observation-model.md` | MOVE | DESIGNED |
| CAP-313 | `Continue Architecture Planning.md` | Evidence | `docs/architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-314 | `Continue Architecture Planning.md` | Claim | `docs/architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-315 | `Continue Architecture Planning.md` | 3. Resource ≠ Claim | `docs/architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-316 | `Continue Architecture Planning.md` | 4. EvidenceGraph | `docs/architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-317 | `Continue Architecture Planning.md` | 5. Provenance | `docs/architecture/provenance.md` | MOVE | DESIGNED |
| CAP-318 | `Continue Architecture Planning.md` | 6. Evidence object | `docs/architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-319 | `Continue Architecture Planning.md` | 7. Locator | `docs/architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-320 | `Continue Architecture Planning.md` | 8. Claim | `docs/architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-321 | `Continue Architecture Planning.md` | 9. Claims should not be confused with truth | `docs/architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-322 | `Continue Architecture Planning.md` | 10. Evidence strength | `docs/architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-323 | `Continue Architecture Planning.md` | 11. Independent evidence | `docs/architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-324 | `Continue Architecture Planning.md` | 12. Evidence independence | `docs/architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-325 | `Continue Architecture Planning.md` | 13. Evidence graph edges | `docs/architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-326 | `Continue Architecture Planning.md` | 14. Why graph edges matter | `docs/architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-327 | `Continue Architecture Planning.md` | 15. Provenance graph | `docs/architecture/provenance.md` | MOVE | DESIGNED |
| CAP-328 | `Continue Architecture Planning.md` | 16. Resource identity | `docs/architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-329 | `Continue Architecture Planning.md` | 17. Resource fingerprint | `docs/architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-330 | `Continue Architecture Planning.md` | 18. URL identity vs content identity | `docs/architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-331 | `Continue Architecture Planning.md` | 19. Revision detection | `docs/architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-332 | `Continue Architecture Planning.md` | 20. Observation immutability | `docs/architecture/observation-model.md` | MOVE | DESIGNED |
| CAP-333 | `Continue Architecture Planning.md` | 21. Evidence immutability | `docs/architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-334 | `Continue Architecture Planning.md` | 22. Extraction method becomes first-class | `docs/architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-335 | `Continue Architecture Planning.md` | 23. Verification | `docs/validation/verification.md` | MOVE | DESIGNED |
| CAP-336 | `Continue Architecture Planning.md` | 24. Evidence lifecycle | `docs/architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-337 | `Continue Architecture Planning.md` | 25. Evidence states | `docs/architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-338 | `Continue Architecture Planning.md` | 26. Claims can conflict | `docs/architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-339 | `Continue Architecture Planning.md` | 27. Evidence resolution | `docs/architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-340 | `Continue Architecture Planning.md` | 28. Discovery confidence changes meaning | `docs/architecture/discovery-model.md` | MOVE | DESIGNED |
| CAP-341 | `Continue Architecture Planning.md` | 29. Candidate provenance | `docs/architecture/provenance.md` | MOVE | DESIGNED |
| CAP-342 | `Continue Architecture Planning.md` | 30. The evidence ledger | `docs/architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-343 | `Continue Architecture Planning.md` | 31. Two complementary graphs | `docs/architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-344 | `Continue Architecture Planning.md` | 32. Example end-to-end trace | `docs/architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-345 | `Continue Architecture Planning.md` | 33. v0.16 architecture | `docs/architecture/system-model.md` | MOVE | DESIGNED |
| CAP-346 | `Continue Architecture Planning.md` | 34. New invariants | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-347 | `Continue Architecture Planning.md` | Evidence provenance | `docs/architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-348 | `Continue Architecture Planning.md` | Claim support | `docs/architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-349 | `Continue Architecture Planning.md` | Historical integrity | `docs/architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-350 | `Continue Architecture Planning.md` | Extraction integrity | `docs/architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-351 | `Continue Architecture Planning.md` | Resource identity | `docs/architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-352 | `Continue Architecture Planning.md` | Content identity | `docs/architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-353 | `Continue Architecture Planning.md` | Conflict preservation | `docs/architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-354 | `Continue Architecture Planning.md` | Provenance preservation | `docs/architecture/provenance.md` | MOVE | DESIGNED |
| CAP-355 | `Continue Architecture Planning.md` | Session provenance | `docs/architecture/provenance.md` | MOVE | DESIGNED |
| CAP-356 | `Continue Architecture Planning.md` | 35. Failure taxonomy | `docs/validation/failure-taxonomy.md` | MOVE | DESIGNED |
| CAP-357 | `Continue Architecture Planning.md` | 36. The deeper architectural transition | `docs/roadmap/future-work.md` | MOVE | FUTURE |
| CAP-358 | `Continue Architecture Planning.md` | 37. What is still missing | `docs/roadmap/future-work.md` | MOVE | FUTURE |
| CAP-359 | `Continue Architecture Planning.md` | Search space | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-360 | `Continue Architecture Planning.md` | Execution | `docs/architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-361 | `Continue Architecture Planning.md` | Work | `docs/architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-362 | `Continue Architecture Planning.md` | Acquisition | `docs/acquisition/acquisition-model.md` | MOVE | DESIGNED |
| CAP-363 | `Continue Architecture Planning.md` | Recognition | `docs/acquisition/response-recognition.md` | MOVE | DESIGNED |
| CAP-364 | `Continue Architecture Planning.md` | Discovery | `docs/architecture/discovery-model.md` | MOVE | DESIGNED |
| CAP-365 | `Continue Architecture Planning.md` | Evidence | `docs/architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-366 | `Continue Architecture Planning.md` | History | `docs/architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-367 | `Continue Architecture Planning.md` | v0.17 — ResourceGraph + Identity Resolution | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-368 | `Continue Architecture Planning.md` | *turn 46 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-369 | `Continue Architecture Planning.md` | v0.17 — ResourceGraph + Identity Resolution | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-370 | `Continue Architecture Planning.md` | 1. The core problem | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-371 | `Continue Architecture Planning.md` | 2. Resource identity must become graph-based | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-372 | `Continue Architecture Planning.md` | 3. Candidate vs Resource vs Locator | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-373 | `Continue Architecture Planning.md` | Candidate | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-374 | `Continue Architecture Planning.md` | Locator | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-375 | `Continue Architecture Planning.md` | Resource | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-376 | `Continue Architecture Planning.md` | 4. Why not simply canonicalize everything? | `docs/architecture/resource-model.md` | MOVE | OPEN |
| CAP-377 | `Continue Architecture Planning.md` | 5. Locator | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-378 | `Continue Architecture Planning.md` | 6. Resource | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-379 | `Continue Architecture Planning.md` | 7. Resource relationships | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-380 | `Continue Architecture Planning.md` | 8. Redirects | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-381 | `Continue Architecture Planning.md` | 9. Redirect chain | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-382 | `Continue Architecture Planning.md` | 10. Content fingerprints | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-383 | `Continue Architecture Planning.md` | 11. Same content does not prove same resource | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-384 | `Continue Architecture Planning.md` | 12. Representation identity | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-385 | `Continue Architecture Planning.md` | 13. Identity Evidence | `docs/architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-386 | `Continue Architecture Planning.md` | 14. IdentityResolver | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-387 | `Continue Architecture Planning.md` | 15. Identity confidence should be relational | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-388 | `Continue Architecture Planning.md` | 16. Identity classes | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-389 | `Continue Architecture Planning.md` | 17. No destructive merges | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-390 | `Continue Architecture Planning.md` | 18. ResourceGraph | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-391 | `Continue Architecture Planning.md` | 19. Graph edge contract | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-392 | `Continue Architecture Planning.md` | 20. Identity resolution pipeline | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-393 | `Continue Architecture Planning.md` | 21. Canonical URL is still important | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-394 | `Continue Architecture Planning.md` | 22. Canonicalization provenance | `docs/architecture/provenance.md` | MOVE | DESIGNED |
| CAP-395 | `Continue Architecture Planning.md` | 23. Identity resolution must be monotonic where possible | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-396 | `Continue Architecture Planning.md` | 24. Resource revisions | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-397 | `Continue Architecture Planning.md` | 25. Revision object | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-398 | `Continue Architecture Planning.md` | 26. ResourceGraph vs KnowledgeBase | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-399 | `Continue Architecture Planning.md` | 27. Querying the graph | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-400 | `Continue Architecture Planning.md` | What URLs identify this resource? | `docs/architecture/resource-model.md` | MOVE | OPEN |
| CAP-401 | `Continue Architecture Planning.md` | Where was it discovered? | `docs/architecture/resource-model.md` | MOVE | OPEN |
| CAP-402 | `Continue Architecture Planning.md` | What URLs redirect to it? | `docs/architecture/resource-model.md` | MOVE | OPEN |
| CAP-403 | `Continue Architecture Planning.md` | Which URLs have identical observed bytes? | `docs/architecture/resource-model.md` | MOVE | OPEN |
| CAP-404 | `Continue Architecture Planning.md` | Has this resource changed? | `docs/architecture/resource-model.md` | MOVE | OPEN |
| CAP-405 | `Continue Architecture Planning.md` | Why do we believe two URLs are related? | `docs/architecture/resource-model.md` | MOVE | OPEN |
| CAP-406 | `Continue Architecture Planning.md` | 28. Resource graph example | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-407 | `Continue Architecture Planning.md` | 29. Failure taxonomy | `docs/validation/failure-taxonomy.md` | MOVE | DESIGNED |
| CAP-408 | `Continue Architecture Planning.md` | 30. Core invariants | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-409 | `Continue Architecture Planning.md` | Locator preservation | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-410 | `Continue Architecture Planning.md` | No destructive merge | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-411 | `Continue Architecture Planning.md` | Fingerprint independence | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-412 | `Continue Architecture Planning.md` | Redirect independence | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-413 | `Continue Architecture Planning.md` | Evidence-backed identity | `docs/architecture/evidence-model.md` | MOVE | DESIGNED |
| CAP-414 | `Continue Architecture Planning.md` | Revision preservation | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-415 | `Continue Architecture Planning.md` | Canonicalization transparency | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-416 | `Continue Architecture Planning.md` | 31. The new architecture | `docs/architecture/system-model.md` | MOVE | DESIGNED |
| CAP-417 | `Continue Architecture Planning.md` | 32. The deeper model | `docs/concepts/overview.md` | MOVE | DESIGNED |
| CAP-418 | `Continue Architecture Planning.md` | 33. The important transition | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-419 | `Continue Architecture Planning.md` | 34. Next missing abstraction | `docs/roadmap/future-work.md` | MOVE | FUTURE |
| CAP-420 | `Continue Architecture Planning.md` | v0.18 — Resource Type System + Semantic Classification | `docs/architecture/classification.md` | MOVE | DESIGNED |
| CAP-421 | `Continue Architecture Planning.md` | *turn 48 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-422 | `Continue Architecture Planning.md` | v0.18 — Resource Type System + Semantic Classification | `docs/architecture/classification.md` | MOVE | DESIGNED |
| CAP-423 | `Continue Architecture Planning.md` | 18.1 The Type Problem | `docs/architecture/classification.md` | MOVE | DESIGNED |
| CAP-424 | `Continue Architecture Planning.md` | 18.2 Four Orthogonal Type Dimensions | `docs/architecture/classification.md` | MOVE | DESIGNED |
| CAP-425 | `Continue Architecture Planning.md` | 18.3 ResourceType | `docs/architecture/classification.md` | MOVE | DESIGNED |
| CAP-426 | `Continue Architecture Planning.md` | 18.4 Classification Assertion | `docs/architecture/classification.md` | MOVE | DESIGNED |
| CAP-427 | `Continue Architecture Planning.md` | 18.5 Type Evidence | `docs/architecture/classification.md` | MOVE | DESIGNED |
| CAP-428 | `Continue Architecture Planning.md` | 18.6 Evidence Strength Must Be Axis-Specific | `docs/architecture/classification.md` | MOVE | DESIGNED |
| CAP-429 | `Continue Architecture Planning.md` | 18.7 Classification Pipeline | `docs/architecture/classification.md` | MOVE | DESIGNED |
| CAP-430 | `Continue Architecture Planning.md` | 18.8 Recognition vs Classification | `docs/architecture/classification.md` | MOVE | DESIGNED |
| CAP-431 | `Continue Architecture Planning.md` | Recognition | `docs/architecture/classification.md` | MOVE | DESIGNED |
| CAP-432 | `Continue Architecture Planning.md` | Classification | `docs/architecture/classification.md` | MOVE | DESIGNED |
| CAP-433 | `Continue Architecture Planning.md` | 18.9 Classification Runtime | `docs/architecture/classification.md` | MOVE | DESIGNED |
| CAP-434 | `Continue Architecture Planning.md` | 18.10 Example Classifiers | `docs/architecture/classification.md` | MOVE | DESIGNED |
| CAP-435 | `Continue Architecture Planning.md` | 18.11 Hierarchical Classification | `docs/architecture/classification.md` | MOVE | DESIGNED |
| CAP-436 | `Continue Architecture Planning.md` | 18.12 Do Not Use One Global Confidence Score | `docs/architecture/classification.md` | MOVE | DESIGNED |
| CAP-437 | `Continue Architecture Planning.md` | 18.13 Classification Is Versioned | `docs/architecture/classification.md` | MOVE | DESIGNED |
| CAP-438 | `Continue Architecture Planning.md` | 18.14 Contradictory Classification | `docs/architecture/classification.md` | MOVE | DESIGNED |
| CAP-439 | `Continue Architecture Planning.md` | 18.15 Classification Graph | `docs/architecture/classification.md` | MOVE | DESIGNED |
| CAP-440 | `Continue Architecture Planning.md` | 18.16 Resource Model After v0.18 | `docs/architecture/classification.md` | MOVE | DESIGNED |
| CAP-441 | `Continue Architecture Planning.md` | 18.17 Resource Type Registry | `docs/architecture/classification.md` | MOVE | DESIGNED |
| CAP-442 | `Continue Architecture Planning.md` | 18.18 Classification Must Not Become Acquisition Policy | `docs/acquisition/acquisition-model.md` | MOVE | DESIGNED |
| CAP-443 | `Continue Architecture Planning.md` | 18.19 Classification → Strategy | `docs/architecture/classification.md` | MOVE | DESIGNED |
| CAP-444 | `Continue Architecture Planning.md` | 18.20 Classification Work as WorkItem | `docs/architecture/classification.md` | MOVE | DESIGNED |
| CAP-445 | `Continue Architecture Planning.md` | 18.21 End-to-End Architecture | `docs/architecture/system-model.md` | MOVE | DESIGNED |
| CAP-446 | `Continue Architecture Planning.md` | 18.22 Failure Taxonomy | `docs/validation/failure-taxonomy.md` | MOVE | DESIGNED |
| CAP-447 | `Continue Architecture Planning.md` | 18.23 Core Invariants | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-448 | `Continue Architecture Planning.md` | Invariant 1 — Type is not identity | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-449 | `Continue Architecture Planning.md` | Invariant 2 — URL does not determine semantic type | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-450 | `Continue Architecture Planning.md` | Invariant 3 — Technical recognition does not determine semantic role | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-451 | `Continue Architecture Planning.md` | Invariant 4 — Classification requires evidence | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-452 | `Continue Architecture Planning.md` | Invariant 5 — Classification does not imply authorization | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-453 | `Continue Architecture Planning.md` | Invariant 6 — Historical classification is immutable | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-454 | `Continue Architecture Planning.md` | Invariant 7 — Contradiction is preserved | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-455 | `Continue Architecture Planning.md` | Invariant 8 — Type axes remain independent | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-456 | `Continue Architecture Planning.md` | 18.24 The Larger Concept | `docs/concepts/overview.md` | MOVE | DESIGNED |
| CAP-457 | `Continue Architecture Planning.md` | v0.19 — Resource Representation & Revision Model | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-458 | `Continue Architecture Planning.md` | *turn 50 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-459 | `Continue Architecture Planning.md` | v0.19 — Resource Representation + Artifact + Revision Model | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-460 | `Continue Architecture Planning.md` | 19.1 The Core Distinction | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-461 | `Continue Architecture Planning.md` | Resource | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-462 | `Continue Architecture Planning.md` | Representation | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-463 | `Continue Architecture Planning.md` | Artifact | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-464 | `Continue Architecture Planning.md` | Observation | `docs/architecture/observation-model.md` | MOVE | DESIGNED |
| CAP-465 | `Continue Architecture Planning.md` | 19.2 Why Resource → Artifact Is Wrong | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-466 | `Continue Architecture Planning.md` | 19.3 New Data Model | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-467 | `Continue Architecture Planning.md` | 19.4 The Complete Identity Chain | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-468 | `Continue Architecture Planning.md` | 19.5 Representation Is Not Just MIME | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-469 | `Continue Architecture Planning.md` | 19.6 Representation Relations | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-470 | `Continue Architecture Planning.md` | 19.7 Artifact Identity | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-471 | `Continue Architecture Planning.md` | 19.8 Content Equivalence | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-472 | `Continue Architecture Planning.md` | 19.9 Revision Detection | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-473 | `Continue Architecture Planning.md` | 19.10 Revision Detection Is Not Always Proof of Semantic Revision | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-474 | `Continue Architecture Planning.md` | 19.11 Revision Evidence | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-475 | `Continue Architecture Planning.md` | 19.12 HTTP Validators Become Evidence | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-476 | `Continue Architecture Planning.md` | 19.13 Conditional Acquisition | `docs/acquisition/acquisition-model.md` | MOVE | DESIGNED |
| CAP-477 | `Continue Architecture Planning.md` | 19.14 Observation Becomes the Historical Bridge | `docs/architecture/observation-model.md` | MOVE | DESIGNED |
| CAP-478 | `Continue Architecture Planning.md` | 19.15 Resource State vs Artifact State | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-479 | `Continue Architecture Planning.md` | Resource state | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-480 | `Continue Architecture Planning.md` | Artifact state | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-481 | `Continue Architecture Planning.md` | Observation state | `docs/architecture/observation-model.md` | MOVE | DESIGNED |
| CAP-482 | `Continue Architecture Planning.md` | 19.16 ResourceGraph v0.19 | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-483 | `Continue Architecture Planning.md` | 19.17 ResourceGraph API | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-484 | `Continue Architecture Planning.md` | 19.18 Artifact Deduplication | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-485 | `Continue Architecture Planning.md` | Locator deduplication | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-486 | `Continue Architecture Planning.md` | Artifact deduplication | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-487 | `Continue Architecture Planning.md` | 19.19 Content-Addressed Storage | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-488 | `Continue Architecture Planning.md` | 19.20 Verification Levels | `docs/validation/verification.md` | MOVE | DESIGNED |
| CAP-489 | `Continue Architecture Planning.md` | 19.21 Independent Confirmation | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-490 | `Continue Architecture Planning.md` | 19.22 Resource Confidence | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-491 | `Continue Architecture Planning.md` | 19.23 Example | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-492 | `Continue Architecture Planning.md` | Step 1 — Locator | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-493 | `Continue Architecture Planning.md` | Step 2 — Resource | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-494 | `Continue Architecture Planning.md` | Step 3 — Observation | `docs/architecture/observation-model.md` | MOVE | DESIGNED |
| CAP-495 | `Continue Architecture Planning.md` | Step 4 — Artifact | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-496 | `Continue Architecture Planning.md` | Step 5 — Representation | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-497 | `Continue Architecture Planning.md` | Step 6 — Classification | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-498 | `Continue Architecture Planning.md` | Step 7 — Revision | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-499 | `Continue Architecture Planning.md` | 19.24 A More Precise End-to-End Pipeline | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-500 | `Continue Architecture Planning.md` | 19.25 New Invariants | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-501 | `Continue Architecture Planning.md` | Artifact invariant | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-502 | `Continue Architecture Planning.md` | Resource invariant | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-503 | `Continue Architecture Planning.md` | Representation invariant | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-504 | `Continue Architecture Planning.md` | Revision invariant | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-505 | `Continue Architecture Planning.md` | Observation invariant | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-506 | `Continue Architecture Planning.md` | Deduplication invariant | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-507 | `Continue Architecture Planning.md` | Change invariant | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-508 | `Continue Architecture Planning.md` | Classification invariant | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-509 | `Continue Architecture Planning.md` | 19.26 Failure Modes | `docs/validation/failure-taxonomy.md` | MOVE | DESIGNED |
| CAP-510 | `Continue Architecture Planning.md` | 19.27 What v0.19 Gives Us | `docs/architecture/resource-model.md` | MOVE | DESIGNED |
| CAP-511 | `Continue Architecture Planning.md` | Next boundary: v0.20 — Search-Space Partitioning + Discovery Strategies | `docs/roadmap/future-work.md` | MOVE | FUTURE |
| CAP-512 | `Continue Architecture Planning.md` | *turn 52 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-513 | `Continue Architecture Planning.md` | v0.20 — Search-Space Partitioning + Discovery Strategies | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-514 | `Continue Architecture Planning.md` | 20.1 The Search Space | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-515 | `Continue Architecture Planning.md` | 20.2 What Is a Partition? | `docs/architecture/search-space.md` | MOVE | OPEN |
| CAP-516 | `Continue Architecture Planning.md` | 20.3 Partition ≠ Candidate | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-517 | `Continue Architecture Planning.md` | 20.4 Partition Object | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-518 | `Continue Architecture Planning.md` | 20.5 Partition State | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-519 | `Continue Architecture Planning.md` | Saturated | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-520 | `Continue Architecture Planning.md` | Exhausted | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-521 | `Continue Architecture Planning.md` | 20.6 Search Coverage | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-522 | `Continue Architecture Planning.md` | 20.7 Strategy Contract | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-523 | `Continue Architecture Planning.md` | 20.8 Strategy vs Candidate Source | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-524 | `Continue Architecture Planning.md` | 20.9 Strategy Types | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-525 | `Continue Architecture Planning.md` | Seed Expansion | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-526 | `Continue Architecture Planning.md` | Repository Expansion | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-527 | `Continue Architecture Planning.md` | Sitemap Expansion | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-528 | `Continue Architecture Planning.md` | API Schema Expansion | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-529 | `Continue Architecture Planning.md` | Document-Family Expansion | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-530 | `Continue Architecture Planning.md` | 20.10 Blind-Scan Analogy | `docs/research/dvb-blind-scan.md` | MOVE | DESIGNED |
| CAP-531 | `Continue Architecture Planning.md` | 20.11 Probe | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-532 | `Continue Architecture Planning.md` | 20.12 Exploration Plan | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-533 | `Continue Architecture Planning.md` | 20.13 Exploration Must Remain Budgeted | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-534 | `Continue Architecture Planning.md` | 20.14 Adaptive Partition Priority | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-535 | `Continue Architecture Planning.md` | 20.15 Exploration vs Exploitation | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-536 | `Continue Architecture Planning.md` | 20.16 Aging | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-537 | `Continue Architecture Planning.md` | 20.17 Partition Splitting | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-538 | `Continue Architecture Planning.md` | 20.18 Partition Merge | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-539 | `Continue Architecture Planning.md` | 20.19 Partition Graph | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-540 | `Continue Architecture Planning.md` | 20.20 SearchSpace | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-541 | `Continue Architecture Planning.md` | 20.21 Search-Space Controller | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-542 | `Continue Architecture Planning.md` | 20.22 Three-Level Control Plane | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-543 | `Continue Architecture Planning.md` | 20.23 Candidate Sources Remain Low-Level | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-544 | `Continue Architecture Planning.md` | 20.24 Termination Becomes More Sophisticated | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-545 | `Continue Architecture Planning.md` | 20.25 Saturation | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-546 | `Continue Architecture Planning.md` | 20.26 Partition Statistics | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-547 | `Continue Architecture Planning.md` | 20.27 Discovery Efficiency | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-548 | `Continue Architecture Planning.md` | 20.28 Failure Modes | `docs/validation/failure-taxonomy.md` | MOVE | DESIGNED |
| CAP-549 | `Continue Architecture Planning.md` | 20.29 Core Invariants | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-550 | `Continue Architecture Planning.md` | Search-space invariant | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-551 | `Continue Architecture Planning.md` | Strategy invariant | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-552 | `Continue Architecture Planning.md` | Acquisition invariant | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-553 | `Continue Architecture Planning.md` | Partition invariant | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-554 | `Continue Architecture Planning.md` | Coverage invariant | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-555 | `Continue Architecture Planning.md` | Discovery invariant | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-556 | `Continue Architecture Planning.md` | 20.30 The Architecture After v0.20 | `docs/architecture/system-model.md` | MOVE | DESIGNED |
| CAP-557 | `Continue Architecture Planning.md` | 20.31 The DVB Analogy Is Now Structural | `docs/research/dvb-blind-scan.md` | MOVE | DESIGNED |
| CAP-558 | `Continue Architecture Planning.md` | v0.21 — Discovery Strategy Learning / Adaptive Search | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-559 | `Continue Architecture Planning.md` | *turn 54 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-560 | `Continue Architecture Planning.md` | v0.21 — Adaptive Discovery Strategy | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-561 | `Continue Architecture Planning.md` | 21.1 The Adaptive Loop | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-562 | `Continue Architecture Planning.md` | 21.2 Strategy Performance Record | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-563 | `Continue Architecture Planning.md` | 21.3 Yield Metrics | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-564 | `Continue Architecture Planning.md` | 21.4 Strategy Score | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-565 | `Continue Architecture Planning.md` | 21.5 Cold Start Problem | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-566 | `Continue Architecture Planning.md` | 21.6 Exploration Quota | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-567 | `Continue Architecture Planning.md` | 21.7 Strategy Selection Must Be Constrained | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-568 | `Continue Architecture Planning.md` | 21.8 Strategy Eligibility | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-569 | `Continue Architecture Planning.md` | 21.9 Temporary vs Permanent Failure | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-570 | `Continue Architecture Planning.md` | 21.10 Strategy Outcome | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-571 | `Continue Architecture Planning.md` | 21.11 Strategy Outcome ≠ Strategy Truth | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-572 | `Continue Architecture Planning.md` | 21.12 Novelty | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-573 | `Continue Architecture Planning.md` | 21.13 Frontier Expansion Value | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-574 | `Continue Architecture Planning.md` | 21.14 Frontier Expansion Metric | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-575 | `Continue Architecture Planning.md` | 21.15 Strategy Memory | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-576 | `Continue Architecture Planning.md` | 21.16 Hierarchical Priors | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-577 | `Continue Architecture Planning.md` | 21.17 Discovery Strategy Ledger | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-578 | `Continue Architecture Planning.md` | 21.18 Deterministic Replay | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-579 | `Continue Architecture Planning.md` | 21.19 Random Exploration | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-580 | `Continue Architecture Planning.md` | 21.20 Learning Must Not Modify Safety Boundaries | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-581 | `Continue Architecture Planning.md` | 21.21 Adaptive Discovery Controller | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-582 | `Continue Architecture Planning.md` | 21.22 Tie-Breaking Must Be Deterministic | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-583 | `Continue Architecture Planning.md` | 21.23 Performance Decay | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-584 | `Continue Architecture Planning.md` | 21.24 Strategy Adaptation and Scan Sessions | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-585 | `Continue Architecture Planning.md` | 21.25 Search Strategy as a First-Class Graph Node | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-586 | `Continue Architecture Planning.md` | 21.26 Search Decision Graph | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-587 | `Continue Architecture Planning.md` | 21.27 Two Kinds of Provenance | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-588 | `Continue Architecture Planning.md` | 21.28 Failure Taxonomy | `docs/validation/failure-taxonomy.md` | MOVE | DESIGNED |
| CAP-589 | `Continue Architecture Planning.md` | 21.29 Invariants | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-590 | `Continue Architecture Planning.md` | Safety invariant | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-591 | `Continue Architecture Planning.md` | Capability invariant | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-592 | `Continue Architecture Planning.md` | Domain invariant | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-593 | `Continue Architecture Planning.md` | Exploration invariant | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-594 | `Continue Architecture Planning.md` | Historical invariant | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-595 | `Continue Architecture Planning.md` | Replay invariant | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-596 | `Continue Architecture Planning.md` | Provenance invariant | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-597 | `Continue Architecture Planning.md` | 21.30 Architecture After v0.21 | `docs/architecture/system-model.md` | MOVE | DESIGNED |
| CAP-598 | `Continue Architecture Planning.md` | 21.31 The Important Conceptual Shift | `docs/concepts/overview.md` | MOVE | DESIGNED |
| CAP-599 | `Continue Architecture Planning.md` | v0.22 — Discovery Completeness + Coverage Claims | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-600 | `Continue Architecture Planning.md` | *turn 56 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-601 | `Continue Architecture Planning.md` | v0.22 — Discovery Completeness + Coverage Claims | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-602 | `Continue Architecture Planning.md` | 22.1 The problem | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-603 | `Continue Architecture Planning.md` | 22.2 Search-space state model | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-604 | `Continue Architecture Planning.md` | 22.3 Coverage is a measurement | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-605 | `Continue Architecture Planning.md` | 22.4 Coverage dimensions | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-606 | `Continue Architecture Planning.md` | 22.5 CoverageRecord | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-607 | `Continue Architecture Planning.md` | 22.6 Coverage state | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-608 | `Continue Architecture Planning.md` | 22.7 CoverageClaim | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-609 | `Continue Architecture Planning.md` | 22.8 Completeness is a stronger assertion | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-610 | `Continue Architecture Planning.md` | 22.9 The finite-enumerator case | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-611 | `Continue Architecture Planning.md` | 22.10 Enumeration contract | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-612 | `Continue Architecture Planning.md` | 22.11 Negative evidence | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-613 | `Continue Architecture Planning.md` | 22.12 Absence reasoning hierarchy | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-614 | `Continue Architecture Planning.md` | 22.13 “Not found” becomes a first-class result | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-615 | `Continue Architecture Planning.md` | 22.14 Coverage cannot necessarily be monotonically interpreted | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-616 | `Continue Architecture Planning.md` | 22.15 Version the search universe | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-617 | `Continue Architecture Planning.md` | 22.16 Coverage ledger | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-618 | `Continue Architecture Planning.md` | 22.17 Three graphs now interact | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-619 | `Continue Architecture Planning.md` | 22.18 Completeness assessment | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-620 | `Continue Architecture Planning.md` | 22.19 Assurance levels | `docs/validation/verification.md` | MOVE | DESIGNED |
| CAP-621 | `Continue Architecture Planning.md` | 22.20 Search completeness matrix | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-622 | `Continue Architecture Planning.md` | 22.21 Coverage calculation | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-623 | `Continue Architecture Planning.md` | 22.22 Coverage should be query-relative | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-624 | `Continue Architecture Planning.md` | 22.23 Failure taxonomy | `docs/validation/failure-taxonomy.md` | MOVE | DESIGNED |
| CAP-625 | `Continue Architecture Planning.md` | 22.24 Core invariants | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-626 | `Continue Architecture Planning.md` | Invariant 1 | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-627 | `Continue Architecture Planning.md` | Invariant 2 | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-628 | `Continue Architecture Planning.md` | Invariant 3 | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-629 | `Continue Architecture Planning.md` | Invariant 4 | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-630 | `Continue Architecture Planning.md` | Invariant 5 | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-631 | `Continue Architecture Planning.md` | Invariant 6 | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-632 | `Continue Architecture Planning.md` | Invariant 7 | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-633 | `Continue Architecture Planning.md` | Invariant 8 | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-634 | `Continue Architecture Planning.md` | Invariant 9 | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-635 | `Continue Architecture Planning.md` | Invariant 10 | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-636 | `Continue Architecture Planning.md` | 22.25 v0.22 architecture | `docs/architecture/system-model.md` | MOVE | DESIGNED |
| CAP-637 | `Continue Architecture Planning.md` | 22.26 The conceptual jump | `docs/concepts/overview.md` | MOVE | DESIGNED |
| CAP-638 | `Continue Architecture Planning.md` | v0.23 — Negative Evidence + Absence Reasoning | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-639 | `Continue Architecture Planning.md` | *turn 58 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-640 | `Continue Architecture Planning.md` | v0.23 — Negative Evidence + Absence Reasoning | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-641 | `Continue Architecture Planning.md` | 23.1 The absence problem | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-642 | `Continue Architecture Planning.md` | 23.2 Four fundamental states | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-643 | `Continue Architecture Planning.md` | 23.3 PresenceAssertion | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-644 | `Continue Architecture Planning.md` | 23.4 Absence is always scoped | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-645 | `Continue Architecture Planning.md` | 23.5 NegativeEvidence | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-646 | `Continue Architecture Planning.md` | 23.6 Absence strength | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-647 | `Continue Architecture Planning.md` | 23.7 Search failure must not become negative evidence automatically | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-648 | `Continue Architecture Planning.md` | 23.8 Failure → evidence mapping | `docs/validation/failure-taxonomy.md` | MOVE | DESIGNED |
| CAP-649 | `Continue Architecture Planning.md` | 23.9 Exact locator absence | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-650 | `Continue Architecture Planning.md` | 23.10 Claims need predicates | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-651 | `Continue Architecture Planning.md` | 23.11 Predicate-aware absence | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-652 | `Continue Architecture Planning.md` | 23.12 Contradiction becomes first-class | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-653 | `Continue Architecture Planning.md` | 23.13 True contradiction | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-654 | `Continue Architecture Planning.md` | 23.14 Absence confidence cannot simply be numeric | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-655 | `Continue Architecture Planning.md` | 23.15 Independent evidence | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-656 | `Continue Architecture Planning.md` | 23.16 Absence reasoning engine | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-657 | `Continue Architecture Planning.md` | 23.17 Formal absence rule | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-658 | `Continue Architecture Planning.md` | 23.18 Dynamic universes | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-659 | `Continue Architecture Planning.md` | 23.19 Temporal validity | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-660 | `Continue Architecture Planning.md` | 23.20 Absence and revision detection | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-661 | `Continue Architecture Planning.md` | 23.21 Search state now becomes richer | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-662 | `Continue Architecture Planning.md` | 23.22 Architecture after v0.23 | `docs/architecture/system-model.md` | MOVE | DESIGNED |
| CAP-663 | `Continue Architecture Planning.md` | 23.23 The three epistemic outcomes | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-664 | `Continue Architecture Planning.md` | Presence | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-665 | `Continue Architecture Planning.md` | Absence | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-666 | `Continue Architecture Planning.md` | Unknown | `docs/architecture/coverage-and-absence.md` | MOVE | DESIGNED |
| CAP-667 | `Continue Architecture Planning.md` | 23.24 New invariants | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-668 | `Continue Architecture Planning.md` | Invariant 1 | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-669 | `Continue Architecture Planning.md` | Invariant 2 | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-670 | `Continue Architecture Planning.md` | Invariant 3 | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-671 | `Continue Architecture Planning.md` | Invariant 4 | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-672 | `Continue Architecture Planning.md` | Invariant 5 | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-673 | `Continue Architecture Planning.md` | Invariant 6 | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-674 | `Continue Architecture Planning.md` | Invariant 7 | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-675 | `Continue Architecture Planning.md` | Invariant 8 | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-676 | `Continue Architecture Planning.md` | Invariant 9 | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-677 | `Continue Architecture Planning.md` | Invariant 10 | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-678 | `Continue Architecture Planning.md` | 23.25 v0.23 conceptual result | `docs/concepts/overview.md` | MOVE | DESIGNED |
| CAP-679 | `Continue Architecture Planning.md` | v0.24 — Query/Goal-Constrained Discovery | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-680 | `Continue Architecture Planning.md` | *turn 60 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-681 | `Continue Architecture Planning.md` | v0.24 — Query/Goal-Constrained Discovery | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-682 | `Continue Architecture Planning.md` | 24.1 SearchGoal | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-683 | `Continue Architecture Planning.md` | 24.2 Goal ≠ Domain | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-684 | `Continue Architecture Planning.md` | 24.3 Goal constraints | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-685 | `Continue Architecture Planning.md` | 24.4 Hard constraints vs soft preferences | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-686 | `Continue Architecture Planning.md` | 24.5 GoalConstraint | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-687 | `Continue Architecture Planning.md` | 24.6 Relevance is not classification | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-688 | `Continue Architecture Planning.md` | 24.7 RelevanceAssertion | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-689 | `Continue Architecture Planning.md` | 24.8 Why `UNKNOWN` matters | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-690 | `Continue Architecture Planning.md` | 24.9 Relevance scoring | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-691 | `Continue Architecture Planning.md` | 24.10 The six questions | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-692 | `Continue Architecture Planning.md` | 24.11 Relevant Search Space | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-693 | `Continue Architecture Planning.md` | 24.12 Example | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-694 | `Continue Architecture Planning.md` | 24.13 Goal-directed adaptive discovery | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-695 | `Continue Architecture Planning.md` | 24.14 Expected Goal Value | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-696 | `Continue Architecture Planning.md` | 24.15 Information gain | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-697 | `Continue Architecture Planning.md` | 24.16 Goal-aware partition scoring | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-698 | `Continue Architecture Planning.md` | 24.17 Goal does not grant authority | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-699 | `Continue Architecture Planning.md` | 24.18 Goal provenance | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-700 | `Continue Architecture Planning.md` | 24.19 Goal-aware discovery event | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-701 | `Continue Architecture Planning.md` | 24.20 Goal lifecycle | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-702 | `Continue Architecture Planning.md` | 24.21 Goal termination policies | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-703 | `Continue Architecture Planning.md` | 24.22 Goal satisfaction vs completeness | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-704 | `Continue Architecture Planning.md` | 24.23 GoalResult | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-705 | `Continue Architecture Planning.md` | 24.24 Result ranking | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-706 | `Continue Architecture Planning.md` | 24.25 Result quality model | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-707 | `Continue Architecture Planning.md` | 24.26 Goal conflict | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-708 | `Continue Architecture Planning.md` | 24.27 Goal sessions | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-709 | `Continue Architecture Planning.md` | 24.28 Reuse of previous knowledge | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-710 | `Continue Architecture Planning.md` | 24.29 Knowledge reuse is not evidence reuse without qualification | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-711 | `Continue Architecture Planning.md` | 24.30 New architecture | `docs/architecture/system-model.md` | MOVE | DESIGNED |
| CAP-712 | `Continue Architecture Planning.md` | 24.31 The architecture's semantic layers | `docs/architecture/system-model.md` | MOVE | DESIGNED |
| CAP-713 | `Continue Architecture Planning.md` | 24.32 Core invariants for v0.24 | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-714 | `Continue Architecture Planning.md` | Invariant 1 | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-715 | `Continue Architecture Planning.md` | Invariant 2 | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-716 | `Continue Architecture Planning.md` | Invariant 3 | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-717 | `Continue Architecture Planning.md` | Invariant 4 | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-718 | `Continue Architecture Planning.md` | Invariant 5 | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-719 | `Continue Architecture Planning.md` | Invariant 6 | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-720 | `Continue Architecture Planning.md` | Invariant 7 | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-721 | `Continue Architecture Planning.md` | Invariant 8 | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-722 | `Continue Architecture Planning.md` | Invariant 9 | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-723 | `Continue Architecture Planning.md` | Invariant 10 | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-724 | `Continue Architecture Planning.md` | 24.33 What v0.24 changes fundamentally | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-725 | `Continue Architecture Planning.md` | v0.25 — Discovery Query Planner | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-726 | `Continue Architecture Planning.md` | *turn 62 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-727 | `Continue Architecture Planning.md` | v0.25 — Discovery Query Planner | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-728 | `Continue Architecture Planning.md` | 25.1 Planner ≠ Search Engine | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-729 | `Continue Architecture Planning.md` | 25.2 QueryPlan | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-730 | `Continue Architecture Planning.md` | 25.3 QueryStep | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-731 | `Continue Architecture Planning.md` | 25.4 Query decomposition | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-732 | `Continue Architecture Planning.md` | 25.5 Search axes | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-733 | `Continue Architecture Planning.md` | 25.6 QueryTactic | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-734 | `Continue Architecture Planning.md` | 25.7 Tactic ≠ Strategy | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-735 | `Continue Architecture Planning.md` | 25.8 Planner plugins | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-736 | `Continue Architecture Planning.md` | 25.9 Planner contract | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-737 | `Continue Architecture Planning.md` | 25.10 Query plan example | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-738 | `Continue Architecture Planning.md` | 25.11 Dependencies | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-739 | `Continue Architecture Planning.md` | 25.12 Conditional planning | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-740 | `Continue Architecture Planning.md` | 25.13 Planning boundary | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-741 | `Continue Architecture Planning.md` | 25.14 Query plan validation | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-742 | `Continue Architecture Planning.md` | 25.15 Planner and adaptive discovery | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-743 | `Continue Architecture Planning.md` | 25.16 Exploration vs exploitation moves upward | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-744 | `Continue Architecture Planning.md` | 25.17 Query tactic performance | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-745 | `Continue Architecture Planning.md` | 25.18 Query planner provenance | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-746 | `Continue Architecture Planning.md` | 25.19 Query plan identity | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-747 | `Continue Architecture Planning.md` | 25.20 Plan versioning | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-748 | `Continue Architecture Planning.md` | 25.21 Planner cannot erase old work | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-749 | `Continue Architecture Planning.md` | 25.22 Query expansion | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-750 | `Continue Architecture Planning.md` | 25.23 Expansion evidence | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-751 | `Continue Architecture Planning.md` | 25.24 Planner hallucination boundary | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-752 | `Continue Architecture Planning.md` | 25.25 Search hypothesis | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-753 | `Continue Architecture Planning.md` | 25.26 Query planner and DVB analogy | `docs/research/dvb-blind-scan.md` | MOVE | DESIGNED |
| CAP-754 | `Continue Architecture Planning.md` | 25.27 Planner output is not execution | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-755 | `Continue Architecture Planning.md` | 25.28 Planner budget | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-756 | `Continue Architecture Planning.md` | 25.29 Three different budgets | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-757 | `Continue Architecture Planning.md` | 25.30 Termination propagation | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-758 | `Continue Architecture Planning.md` | 25.31 v0.25 complete architecture | `docs/architecture/system-model.md` | MOVE | DESIGNED |
| CAP-759 | `Continue Architecture Planning.md` | 25.32 v0.25 invariants | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-760 | `Continue Architecture Planning.md` | Planner invariants | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-761 | `Continue Architecture Planning.md` | 25.33 The resulting abstraction stack | `docs/architecture/goal-and-query.md` | MOVE | DESIGNED |
| CAP-762 | `Continue Architecture Planning.md` | v0.26 — Search Tactic Runtime | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-763 | `Continue Architecture Planning.md` | *turn 64 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-764 | `Continue Architecture Planning.md` | v0.26 — Search Tactic Runtime | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-765 | `Continue Architecture Planning.md` | 26.1 The architectural gap | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-766 | `Continue Architecture Planning.md` | 26.2 QueryStep ≠ TacticExecution | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-767 | `Continue Architecture Planning.md` | 26.3 TacticExecution | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-768 | `Continue Architecture Planning.md` | 26.4 TacticRuntime | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-769 | `Continue Architecture Planning.md` | 26.5 TacticRuntime responsibilities | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-770 | `Continue Architecture Planning.md` | 26.6 Tactic contract | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-771 | `Continue Architecture Planning.md` | 26.7 Capability surface | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-772 | `Continue Architecture Planning.md` | 26.8 Bounded execution | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-773 | `Continue Architecture Planning.md` | 26.9 Batch execution | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-774 | `Continue Architecture Planning.md` | 26.10 Cursor | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-775 | `Continue Architecture Planning.md` | 26.11 Checkpoint | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-776 | `Continue Architecture Planning.md` | 26.12 Checkpoint atomicity | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-777 | `Continue Architecture Planning.md` | 26.13 Tactic dependencies | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-778 | `Continue Architecture Planning.md` | 26.14 Tactic lifecycle | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-779 | `Continue Architecture Planning.md` | 26.15 Exhaustion vs completion | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-780 | `Continue Architecture Planning.md` | 26.16 Tactic result | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-781 | `Continue Architecture Planning.md` | 26.17 Tactic does not create candidates directly | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-782 | `Continue Architecture Planning.md` | 26.18 Tactic → Strategy relationship | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-783 | `Continue Architecture Planning.md` | 26.19 Tactic provenance | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-784 | `Continue Architecture Planning.md` | 26.20 Failure taxonomy | `docs/validation/failure-taxonomy.md` | MOVE | DESIGNED |
| CAP-785 | `Continue Architecture Planning.md` | Planning failures | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-786 | `Continue Architecture Planning.md` | Runtime failures | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-787 | `Continue Architecture Planning.md` | Strategy failures | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-788 | `Continue Architecture Planning.md` | Search failures | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-789 | `Continue Architecture Planning.md` | Recovery failures | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-790 | `Continue Architecture Planning.md` | 26.21 Retry semantics | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-791 | `Continue Architecture Planning.md` | 26.22 Cancellation | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-792 | `Continue Architecture Planning.md` | 26.23 Shared Frontier interaction | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-793 | `Continue Architecture Planning.md` | 26.24 v0.26 architecture | `docs/architecture/system-model.md` | MOVE | DESIGNED |
| CAP-794 | `Continue Architecture Planning.md` | 26.25 Accounting | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-795 | `Continue Architecture Planning.md` | 26.26 The important safety invariant | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-796 | `Continue Architecture Planning.md` | 26.27 Resumability invariant | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-797 | `Continue Architecture Planning.md` | 26.28 New state model | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-798 | `Continue Architecture Planning.md` | 26.29 v0.26 invariants | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-799 | `Continue Architecture Planning.md` | I1 — Planning/execution separation | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-800 | `Continue Architecture Planning.md` | I2 — Execution identity | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-801 | `Continue Architecture Planning.md` | I3 — Single scheduler authority | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-802 | `Continue Architecture Planning.md` | I4 — Bounded execution | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-803 | `Continue Architecture Planning.md` | I5 — Resumability | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-804 | `Continue Architecture Planning.md` | I6 — No silent cursor advancement | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-805 | `Continue Architecture Planning.md` | I7 — Proposal boundary | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-806 | `Continue Architecture Planning.md` | I8 — No authority escalation | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-807 | `Continue Architecture Planning.md` | I9 — Exhaustion separation | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-808 | `Continue Architecture Planning.md` | I10 — Failure ≠ absence | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-809 | `Continue Architecture Planning.md` | I11 — Provenance | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-810 | `Continue Architecture Planning.md` | I12 — Versioned recovery | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-811 | `Continue Architecture Planning.md` | 26.30 What v0.26 actually gives us | `docs/concepts/overview.md` | MOVE | DESIGNED |
| CAP-812 | `Continue Architecture Planning.md` | Next boundary: v0.27 | `docs/roadmap/future-work.md` | MOVE | FUTURE |
| CAP-813 | `Continue Architecture Planning.md` | *turn 66 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-814 | `Continue Architecture Planning.md` | v0.27 — Enumeration Runtime | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-815 | `Continue Architecture Planning.md` | 27.1 The central distinction | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-816 | `Continue Architecture Planning.md` | 27.2 Enumeration as a contract | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-817 | `Continue Architecture Planning.md` | 27.3 Enumerator interface | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-818 | `Continue Architecture Planning.md` | 27.4 EnumerationPage | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-819 | `Continue Architecture Planning.md` | 27.5 `hasMore` is not always trustworthy | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-820 | `Continue Architecture Planning.md` | 27.6 Enumeration state machine | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-821 | `Continue Architecture Planning.md` | 27.7 EnumerationRuntime | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-822 | `Continue Architecture Planning.md` | 27.8 Why this should not be inside DiscoveryStrategy | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-823 | `Continue Architecture Planning.md` | 27.9 Enumerator examples | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-824 | `Continue Architecture Planning.md` | Sitemap | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-825 | `Continue Architecture Planning.md` | API | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-826 | `Continue Architecture Planning.md` | Repository | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-827 | `Continue Architecture Planning.md` | Manifest | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-828 | `Continue Architecture Planning.md` | 27.10 EnumerationEntry | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-829 | `Continue Architecture Planning.md` | 27.11 Entry identity | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-830 | `Continue Architecture Planning.md` | 27.12 Enumeration cursor | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-831 | `Continue Architecture Planning.md` | Offset | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-832 | `Continue Architecture Planning.md` | Page | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-833 | `Continue Architecture Planning.md` | Token | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-834 | `Continue Architecture Planning.md` | Locator | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-835 | `Continue Architecture Planning.md` | Composite | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-836 | `Continue Architecture Planning.md` | 27.13 Cursor validity | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-837 | `Continue Architecture Planning.md` | 27.14 Enumeration snapshot | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-838 | `Continue Architecture Planning.md` | 27.15 Why snapshot identity matters | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-839 | `Continue Architecture Planning.md` | 27.16 Cardinality | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-840 | `Continue Architecture Planning.md` | 27.17 Ordering semantics | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-841 | `Continue Architecture Planning.md` | 27.18 Enumeration consistency | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-842 | `Continue Architecture Planning.md` | 27.19 Completeness assessment | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-843 | `Continue Architecture Planning.md` | 27.20 The crucial three-level distinction | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-844 | `Continue Architecture Planning.md` | 27.21 Example: sitemap | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-845 | `Continue Architecture Planning.md` | 27.22 Enumeration → Coverage | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-846 | `Continue Architecture Planning.md` | 27.23 Enumeration and negative evidence | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-847 | `Continue Architecture Planning.md` | 27.24 Enumeration budget | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-848 | `Continue Architecture Planning.md` | 27.25 Enumeration termination states | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-849 | `Continue Architecture Planning.md` | 27.26 Enumeration accounting | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-850 | `Continue Architecture Planning.md` | 27.27 Enumeration provenance | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-851 | `Continue Architecture Planning.md` | 27.28 Enumeration replay | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-852 | `Continue Architecture Planning.md` | 27.29 Full v0.27 architecture | `docs/architecture/system-model.md` | MOVE | DESIGNED |
| CAP-853 | `Continue Architecture Planning.md` | 27.30 New invariants | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-854 | `Continue Architecture Planning.md` | E1 — Enumeration is scoped | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-855 | `Continue Architecture Planning.md` | E2 — Enumeration termination is not global completeness | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-856 | `Continue Architecture Planning.md` | E3 — Budget exhaustion is not enumeration exhaustion | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-857 | `Continue Architecture Planning.md` | E4 — Cursor progress must be durable | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-858 | `Continue Architecture Planning.md` | E5 — Enumeration entries are not candidates | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-859 | `Continue Architecture Planning.md` | E6 — Cardinality is evidence | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-860 | `Continue Architecture Planning.md` | E7 — Historical snapshots remain immutable | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-861 | `Continue Architecture Planning.md` | E8 — Incomplete enumeration cannot establish absence | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-862 | `Continue Architecture Planning.md` | E9 — Unstable enumeration weakens completeness | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-863 | `Continue Architecture Planning.md` | E10 — Enumerator has no acquisition authority | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-864 | `Continue Architecture Planning.md` | E11 — Enumerator cannot directly mutate the ResourceGraph | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-865 | `Continue Architecture Planning.md` | E12 — Termination evidence is provenance-bearing | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-866 | `Continue Architecture Planning.md` | 27.31 The emerging blind-scan analogy | `docs/research/dvb-blind-scan.md` | MOVE | DESIGNED |
| CAP-867 | `Continue Architecture Planning.md` | v0.27 takeaway | `docs/architecture/strategy-and-planning.md` | MOVE | DESIGNED |
| CAP-868 | `Continue Architecture Planning.md` | v0.28 — Search-Space Reconciliation & Frontier Deduplication | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-869 | `Continue Architecture Planning.md` | *turn 68 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-870 | `Continue Architecture Planning.md` | v0.28 — Search-Space Reconciliation & Frontier Deduplication | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-871 | `Continue Architecture Planning.md` | 28.1 The problem with naive deduplication | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-872 | `Continue Architecture Planning.md` | 28.2 Five different kinds of duplication | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-873 | `Continue Architecture Planning.md` | 28.3 Search-space overlap | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-874 | `Continue Architecture Planning.md` | 28.4 SearchPartitionRelation | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-875 | `Continue Architecture Planning.md` | 28.5 Coverage overlap | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-876 | `Continue Architecture Planning.md` | 28.6 Frontier deduplication | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-877 | `Continue Architecture Planning.md` | 28.7 SearchWorkKey | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-878 | `Continue Architecture Planning.md` | 28.8 Work equivalence | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-879 | `Continue Architecture Planning.md` | 28.9 Candidate convergence | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-880 | `Continue Architecture Planning.md` | 28.10 Observation convergence | `docs/architecture/observation-model.md` | MOVE | DESIGNED |
| CAP-881 | `Continue Architecture Planning.md` | 28.11 Artifact convergence | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-882 | `Continue Architecture Planning.md` | 28.12 Discovery independence | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-883 | `Continue Architecture Planning.md` | 28.13 Evidence independence model | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-884 | `Continue Architecture Planning.md` | 28.14 Coverage provenance | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-885 | `Continue Architecture Planning.md` | 28.15 Coverage relation | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-886 | `Continue Architecture Planning.md` | 28.16 Coverage union | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-887 | `Continue Architecture Planning.md` | 28.17 Disjoint partitions | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-888 | `Continue Architecture Planning.md` | 28.18 Unknown overlap | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-889 | `Continue Architecture Planning.md` | 28.19 Frontier duplicate suppression | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-890 | `Continue Architecture Planning.md` | 28.20 Duplicate suppression must preserve provenance | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-891 | `Continue Architecture Planning.md` | 28.21 Convergence graph | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-892 | `Continue Architecture Planning.md` | 28.22 Search-space graph | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-893 | `Continue Architecture Planning.md` | 28.23 Search-space coverage ledger | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-894 | `Continue Architecture Planning.md` | 28.24 Candidate count is not coverage | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-895 | `Continue Architecture Planning.md` | 28.25 Search-space deduplication vs candidate deduplication | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-896 | `Continue Architecture Planning.md` | Candidate deduplication | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-897 | `Continue Architecture Planning.md` | Search-space deduplication | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-898 | `Continue Architecture Planning.md` | 28.26 Adaptive strategy interaction | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-899 | `Continue Architecture Planning.md` | 28.27 Example | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-900 | `Continue Architecture Planning.md` | 28.28 Reconciliation algorithm | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-901 | `Continue Architecture Planning.md` | 28.29 Reconciliation must be monotonic | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-902 | `Continue Architecture Planning.md` | 28.30 Reconciliation does not delete evidence | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-903 | `Continue Architecture Planning.md` | 28.31 Failure taxonomy | `docs/validation/failure-taxonomy.md` | MOVE | DESIGNED |
| CAP-904 | `Continue Architecture Planning.md` | 28.32 Core invariants | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-905 | `Continue Architecture Planning.md` | R1 — Candidate convergence | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-906 | `Continue Architecture Planning.md` | R2 — Provenance preservation | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-907 | `Continue Architecture Planning.md` | R3 — Artifact convergence | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-908 | `Continue Architecture Planning.md` | R4 — Observation preservation | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-909 | `Continue Architecture Planning.md` | R5 — Overlap is not duplication | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-910 | `Continue Architecture Planning.md` | R6 — Equivalent work may be suppressed | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-911 | `Continue Architecture Planning.md` | R7 — Suppression preserves provenance | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-912 | `Continue Architecture Planning.md` | R8 — Unknown overlap is not disjointness | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-913 | `Continue Architecture Planning.md` | R9 — Coverage is union-aware | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-914 | `Continue Architecture Planning.md` | R10 — Candidate count does not establish coverage | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-915 | `Continue Architecture Planning.md` | R11 — Evidence independence must be justified | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-916 | `Continue Architecture Planning.md` | R12 — Historical reconciliation is immutable | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-917 | `Continue Architecture Planning.md` | 28.33 v0.28 architecture | `docs/architecture/system-model.md` | MOVE | DESIGNED |
| CAP-918 | `Continue Architecture Planning.md` | 28.34 The deeper architectural result | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-919 | `Continue Architecture Planning.md` | Next boundary — v0.29 | `docs/roadmap/future-work.md` | MOVE | FUTURE |
| CAP-920 | `Continue Architecture Planning.md` | *turn 70 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-921 | `Continue Architecture Planning.md` | v0.29 — Dynamic Search-Space Expansion | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-922 | `Continue Architecture Planning.md` | 29.1 The central distinction | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-923 | `Continue Architecture Planning.md` | 29.2 PartitionProposal | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-924 | `Continue Architecture Planning.md` | 29.3 Why proposals are necessary | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-925 | `Continue Architecture Planning.md` | 29.4 PartitionAdmissionController | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-926 | `Continue Architecture Planning.md` | 29.5 Partition identity | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-927 | `Continue Architecture Planning.md` | 29.6 Partition explosion | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-928 | `Continue Architecture Planning.md` | 29.7 ExpansionBudget | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-929 | `Continue Architecture Planning.md` | 29.8 Local expansion rate | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-930 | `Continue Architecture Planning.md` | 29.9 Expansion rate limiting | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-931 | `Continue Architecture Planning.md` | 29.10 Evidence threshold | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-932 | `Continue Architecture Planning.md` | 29.11 Partition proposal epistemic status | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-933 | `Continue Architecture Planning.md` | 29.12 Hypothesis connection | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-934 | `Continue Architecture Planning.md` | 29.13 Partition generation sources | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-935 | `Continue Architecture Planning.md` | 29.14 Expansion provider boundary | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-936 | `Continue Architecture Planning.md` | 29.15 Dynamic search-space graph | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-937 | `Continue Architecture Planning.md` | 29.16 Partition generation event | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-938 | `Continue Architecture Planning.md` | 29.17 Search-space versioning | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-939 | `Continue Architecture Planning.md` | 29.18 SearchSpaceSnapshot | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-940 | `Continue Architecture Planning.md` | 29.19 Expansion and completeness | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-941 | `Continue Architecture Planning.md` | 29.20 Dynamic expansion and negative evidence | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-942 | `Continue Architecture Planning.md` | 29.21 Expansion priorities | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-943 | `Continue Architecture Planning.md` | 29.22 Expansion depth | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-944 | `Continue Architecture Planning.md` | 29.23 Expansion loops | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-945 | `Continue Architecture Planning.md` | 29.24 Expansion cycle ≠ failure | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-946 | `Continue Architecture Planning.md` | 29.25 Partition admission states | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-947 | `Continue Architecture Planning.md` | 29.26 Partition proposal accounting | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-948 | `Continue Architecture Planning.md` | 29.27 Partition explosion protection | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-949 | `Continue Architecture Planning.md` | 29.28 Admission algorithm | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-950 | `Continue Architecture Planning.md` | 29.29 Frontier generation | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-951 | `Continue Architecture Planning.md` | 29.30 Dynamic expansion architecture | `docs/architecture/system-model.md` | MOVE | DESIGNED |
| CAP-952 | `Continue Architecture Planning.md` | 29.31 Two expansion paths | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-953 | `Continue Architecture Planning.md` | 29.32 Search-space discovery as first-class knowledge | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-954 | `Continue Architecture Planning.md` | 29.33 v0.29 invariants | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-955 | `Continue Architecture Planning.md` | P1 — Discovery does not create authority | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-956 | `Continue Architecture Planning.md` | P2 — Partition proposal is not partition | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-957 | `Continue Architecture Planning.md` | P3 — Every admitted partition belongs to the domain | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-958 | `Continue Architecture Planning.md` | P4 — Expansion is budgeted | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-959 | `Continue Architecture Planning.md` | P5 — Expansion is depth-bounded | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-960 | `Continue Architecture Planning.md` | P6 — Duplicate partitions converge | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-961 | `Continue Architecture Planning.md` | P7 — Overlap is preserved | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-962 | `Continue Architecture Planning.md` | P8 — Evidence is preserved | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-963 | `Continue Architecture Planning.md` | P9 — Partition existence does not schedule execution | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-964 | `Continue Architecture Planning.md` | P10 — Expansion cannot override policy | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-965 | `Continue Architecture Planning.md` | P11 — Search-space versions are immutable | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-966 | `Continue Architecture Planning.md` | P12 — Expansion does not invalidate historical claims automatically | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-967 | `Continue Architecture Planning.md` | P13 — Cycles are legal | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-968 | `Continue Architecture Planning.md` | P14 — Unknown remains valid | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-969 | `Continue Architecture Planning.md` | 29.34 The system after v0.29 | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-970 | `Continue Architecture Planning.md` | 29.35 Blind-scan interpretation | `docs/research/dvb-blind-scan.md` | MOVE | DESIGNED |
| CAP-971 | `Continue Architecture Planning.md` | v0.29 takeaway | `docs/architecture/search-space.md` | MOVE | DESIGNED |
| CAP-972 | `Continue Architecture Planning.md` | v0.30 — Unified Frontier Arbitration | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-973 | `Continue Architecture Planning.md` | *turn 72 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-974 | `Continue Architecture Planning.md` | Conclusion — Generic Discovery Engine | `docs/concepts/overview.md` | MOVE | DESIGNED |
| CAP-975 | `Continue Architecture Planning.md` | The final conceptual separation | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-976 | `Continue Architecture Planning.md` | The fundamental invariant | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-977 | `Continue Architecture Planning.md` | What the DVB analogy actually contributed | `docs/research/dvb-blind-scan.md` | MOVE | DESIGNED |
| CAP-978 | `Continue Architecture Planning.md` | The most important safety boundary | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-979 | `Continue Architecture Planning.md` | Final architecture | `docs/architecture/system-model.md` | MOVE | DESIGNED |
| CAP-980 | `Continue Architecture Planning.md` | What the userscript should and should not become | `docs/prototype/limitations.md` | MOVE | UNVERIFIED |
| CAP-981 | `Continue Architecture Planning.md` | Final principles | `docs/concepts/overview.md` | MOVE | DESIGNED |
| CAP-982 | `Continue Architecture Planning.md` | *turn 74 you lead-in* | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-983 | `Continue Architecture Planning.md` | v0.30 — Unified Frontier Arbitration | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-984 | `Continue Architecture Planning.md` | 30.1 The new architecture | `docs/architecture/system-model.md` | MOVE | DESIGNED |
| CAP-985 | `Continue Architecture Planning.md` | 30.2 WorkClass | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-986 | `Continue Architecture Planning.md` | 30.3 WorkClassPolicy | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-987 | `Continue Architecture Planning.md` | 30.4 ArbitrationDecision | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-988 | `Continue Architecture Planning.md` | 30.5 Hard constraints vs soft priorities | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-989 | `Continue Architecture Planning.md` | Hard constraints | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-990 | `Continue Architecture Planning.md` | Soft priorities | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-991 | `Continue Architecture Planning.md` | 30.6 Arbitration score | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-992 | `Continue Architecture Planning.md` | 30.7 Aging | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-993 | `Continue Architecture Planning.md` | 30.8 Starvation detection | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-994 | `Continue Architecture Planning.md` | 30.9 Class starvation | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-995 | `Continue Architecture Planning.md` | 30.10 Weighted fairness | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-996 | `Continue Architecture Planning.md` | 30.11 Deficit-style arbitration | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-997 | `Continue Architecture Planning.md` | 30.12 Cost-aware scheduling | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-998 | `Continue Architecture Planning.md` | 30.13 Backpressure | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-999 | `Continue Architecture Planning.md` | 30.14 Reserved capacity | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-1000 | `Continue Architecture Planning.md` | 30.15 Arbitration pipeline | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-1001 | `Continue Architecture Planning.md` | 30.16 The atomicity problem | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-1002 | `Continue Architecture Planning.md` | 30.17 Priority inversion | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-1003 | `Continue Architecture Planning.md` | 30.18 FrontierArbitrator | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-1004 | `Continue Architecture Planning.md` | 30.19 Arbitration result | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-1005 | `Continue Architecture Planning.md` | 30.20 Arbitration ledger | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-1006 | `Continue Architecture Planning.md` | 30.21 Replay | `docs/architecture/work-and-frontier.md` | MOVE | DESIGNED |
| CAP-1007 | `Continue Architecture Planning.md` | 30.22 The deeper invariant | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-1008 | `Continue Architecture Planning.md` | 30.23 Full v0.30 architecture | `docs/architecture/system-model.md` | MOVE | DESIGNED |
| CAP-1009 | `Continue Architecture Planning.md` | 30.24 Failure taxonomy | `docs/validation/failure-taxonomy.md` | MOVE | DESIGNED |
| CAP-1010 | `Continue Architecture Planning.md` | 30.25 v0.30 invariants | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-1011 | `Continue Architecture Planning.md` | 30.26 What v0.30 actually accomplishes | `docs/concepts/overview.md` | MOVE | DESIGNED |
| CAP-1012 | `Continue Architecture Planning.md` | Next boundary — v0.31 | `docs/roadmap/future-work.md` | MOVE | FUTURE |
| CAP-1013 | `Continue Architecture Planning.md` | *turn 76 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-1014 | `Continue Architecture Planning.md` | v0.31 — Unified Resource & Cost Ledger | `docs/architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1015 | `Continue Architecture Planning.md` | 31.1 Resource dimensions | `docs/architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1016 | `Continue Architecture Planning.md` | 31.2 ResourceBudget | `docs/architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1017 | `Continue Architecture Planning.md` | 31.3 Three resource states | `docs/architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1018 | `Continue Architecture Planning.md` | 31.4 ResourceReservation | `docs/architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1019 | `Continue Architecture Planning.md` | 31.5 Estimated cost vs actual cost | `docs/architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1020 | `Continue Architecture Planning.md` | 31.6 CostObservation | `docs/architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1021 | `Continue Architecture Planning.md` | 31.7 ResourceLedger | `docs/architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1022 | `Continue Architecture Planning.md` | 31.8 Budget scopes | `docs/architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1023 | `Continue Architecture Planning.md` | 31.9 Hierarchical budget accounting | `docs/architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1024 | `Continue Architecture Planning.md` | 31.10 Resource allocation | `docs/architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1025 | `Continue Architecture Planning.md` | 31.11 Allocation is not execution | `docs/architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1026 | `Continue Architecture Planning.md` | 31.12 Partial consumption | `docs/architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1027 | `Continue Architecture Planning.md` | 31.13 Cost overruns | `docs/architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1028 | `Continue Architecture Planning.md` | 31.14 Cost model | `docs/architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1029 | `Continue Architecture Planning.md` | 31.15 Cost is context-dependent | `docs/architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1030 | `Continue Architecture Planning.md` | 31.16 Resource exhaustion | `docs/architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1031 | `Continue Architecture Planning.md` | 31.17 Budget exhaustion vs frontier exhaustion | `docs/architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1032 | `Continue Architecture Planning.md` | 31.18 Resource reservation race | `docs/architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1033 | `Continue Architecture Planning.md` | 31.19 Settlement | `docs/architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1034 | `Continue Architecture Planning.md` | 31.20 Cost feedback | `docs/architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1035 | `Continue Architecture Planning.md` | 31.21 ResourceLedger events | `docs/architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1036 | `Continue Architecture Planning.md` | 31.22 Resource accounting and provenance | `docs/architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1037 | `Continue Architecture Planning.md` | 31.23 Unified v0.31 architecture | `docs/architecture/system-model.md` | MOVE | DESIGNED |
| CAP-1038 | `Continue Architecture Planning.md` | 31.24 The central v0.31 invariants | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-1039 | `Continue Architecture Planning.md` | 31.25 What v0.31 adds | `docs/architecture/resource-budget.md` | MOVE | DESIGNED |
| CAP-1040 | `Continue Architecture Planning.md` | v0.32 boundary | `docs/architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1041 | `Continue Architecture Planning.md` | *turn 78 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-1042 | `Continue Architecture Planning.md` | v0.32 — Transactional Persistence & Crash Recovery | `docs/architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1043 | `Continue Architecture Planning.md` | 32.1 The crash problem | `docs/architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1044 | `Continue Architecture Planning.md` | 32.2 Durable state vs runtime state | `docs/architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1045 | `Continue Architecture Planning.md` | 32.3 Persistence is not serialization | `docs/architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1046 | `Continue Architecture Planning.md` | 32.4 PersistenceAdapter | `docs/architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1047 | `Continue Architecture Planning.md` | 32.5 Transaction | `docs/architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1048 | `Continue Architecture Planning.md` | 32.6 Write-ahead event ledger | `docs/architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1049 | `Continue Architecture Planning.md` | 32.7 Event identity | `docs/architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1050 | `Continue Architecture Planning.md` | 32.8 Monotonic sequence | `docs/architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1051 | `Continue Architecture Planning.md` | 32.9 Commit protocol | `docs/architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1052 | `Continue Architecture Planning.md` | 32.10 Commit markers | `docs/architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1053 | `Continue Architecture Planning.md` | 32.11 Checkpoint correctness | `docs/architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1054 | `Continue Architecture Planning.md` | 32.12 At-least-once vs exactly-once | `docs/architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1055 | `Continue Architecture Planning.md` | 32.13 Idempotency | `docs/architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1056 | `Continue Architecture Planning.md` | 32.14 Work recovery | `docs/architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1057 | `Continue Architecture Planning.md` | 32.15 Recovery scan | `docs/architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1058 | `Continue Architecture Planning.md` | 32.16 RecoveryManager | `docs/architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1059 | `Continue Architecture Planning.md` | 32.17 Reservation recovery | `docs/architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1060 | `Continue Architecture Planning.md` | 32.18 Accounting invariant under crash | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-1061 | `Continue Architecture Planning.md` | 32.19 Observation recovery | `docs/architecture/observation-model.md` | MOVE | DESIGNED |
| CAP-1062 | `Continue Architecture Planning.md` | 32.20 Artifact durability | `docs/architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1063 | `Continue Architecture Planning.md` | 32.21 Durable checkpoint | `docs/architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1064 | `Continue Architecture Planning.md` | 32.22 Recovery invariant for cursors | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-1065 | `Continue Architecture Planning.md` | 32.23 Schema versioning | `docs/architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1066 | `Continue Architecture Planning.md` | 32.24 Snapshot + journal | `docs/architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1067 | `Continue Architecture Planning.md` | 32.25 Snapshot integrity | `docs/architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1068 | `Continue Architecture Planning.md` | 32.26 Recovery outcomes | `docs/architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1069 | `Continue Architecture Planning.md` | 32.27 Recovery must not fabricate knowledge | `docs/architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1070 | `Continue Architecture Planning.md` | 32.28 Crash-safe frontier | `docs/architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1071 | `Continue Architecture Planning.md` | 32.29 Reconciliation | `docs/architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1072 | `Continue Architecture Planning.md` | 32.30 Repair is itself provenance | `docs/architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1073 | `Continue Architecture Planning.md` | 32.31 v0.32 architecture | `docs/architecture/system-model.md` | MOVE | DESIGNED |
| CAP-1074 | `Continue Architecture Planning.md` | 32.32 Complete lifecycle | `docs/architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1075 | `Continue Architecture Planning.md` | 32.33 Failure taxonomy | `docs/validation/failure-taxonomy.md` | MOVE | DESIGNED |
| CAP-1076 | `Continue Architecture Planning.md` | 32.34 v0.32 invariants | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-1077 | `Continue Architecture Planning.md` | 32.35 What v0.32 changes | `docs/architecture/persistence-and-recovery.md` | MOVE | DESIGNED |
| CAP-1078 | `Continue Architecture Planning.md` | v0.33 — Multi-Worker / Multi-Context Coordination | `docs/architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1079 | `Continue Architecture Planning.md` | *turn 80 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-1080 | `Continue Architecture Planning.md` | v0.33 — Multi-Worker Coordination & Distributed Claiming | `docs/architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1081 | `Continue Architecture Planning.md` | 33.1 Worker identity | `docs/architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1082 | `Continue Architecture Planning.md` | 33.2 Worker registration | `docs/architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1083 | `Continue Architecture Planning.md` | 33.3 Worker capabilities | `docs/architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1084 | `Continue Architecture Planning.md` | 33.4 Claiming is the synchronization boundary | `docs/architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1085 | `Continue Architecture Planning.md` | 33.5 ClaimToken | `docs/architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1086 | `Continue Architecture Planning.md` | 33.6 Claim ≠ lease | `docs/architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1087 | `Continue Architecture Planning.md` | 33.7 Lease lifecycle | `docs/architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1088 | `Continue Architecture Planning.md` | 33.8 LeaseManager | `docs/architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1089 | `Continue Architecture Planning.md` | 33.9 Heartbeats | `docs/architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1090 | `Continue Architecture Planning.md` | 33.10 Fencing tokens | `docs/architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1091 | `Continue Architecture Planning.md` | 33.11 Fencing invariant | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-1092 | `Continue Architecture Planning.md` | 33.12 Worker death | `docs/architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1093 | `Continue Architecture Planning.md` | 33.13 Duplicate execution | `docs/architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1094 | `Continue Architecture Planning.md` | 33.14 Execution identity | `docs/architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1095 | `Continue Architecture Planning.md` | 33.15 Duplicate observations | `docs/architecture/observation-model.md` | MOVE | DESIGNED |
| CAP-1096 | `Continue Architecture Planning.md` | 33.16 Duplicate execution ≠ independent evidence | `docs/architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1097 | `Continue Architecture Planning.md` | 33.17 Worker-local vs shared state | `docs/architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1098 | `Continue Architecture Planning.md` | 33.18 CoordinationManager | `docs/architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1099 | `Continue Architecture Planning.md` | 33.19 Coordination vs arbitration | `docs/architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1100 | `Continue Architecture Planning.md` | 33.20 Worker selection | `docs/architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1101 | `Continue Architecture Planning.md` | 33.21 Worker affinity | `docs/architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1102 | `Continue Architecture Planning.md` | 33.22 Worker capacity | `docs/architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1103 | `Continue Architecture Planning.md` | 33.23 Distributed accounting | `docs/architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1104 | `Continue Architecture Planning.md` | 33.24 Worker-local caches | `docs/architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1105 | `Continue Architecture Planning.md` | 33.25 Cross-worker event ordering | `docs/architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1106 | `Continue Architecture Planning.md` | 33.26 Causal provenance | `docs/architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1107 | `Continue Architecture Planning.md` | 33.27 Coordination events | `docs/architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1108 | `Continue Architecture Planning.md` | 33.28 Multi-worker failure modes | `docs/validation/failure-taxonomy.md` | MOVE | DESIGNED |
| CAP-1109 | `Continue Architecture Planning.md` | 33.29 Split-brain | `docs/architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1110 | `Continue Architecture Planning.md` | 33.30 What the browser prototype can guarantee | `docs/prototype/limitations.md` | MOVE | UNVERIFIED |
| CAP-1111 | `Continue Architecture Planning.md` | 33.31 Coordination scope | `docs/architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1112 | `Continue Architecture Planning.md` | 33.32 v0.33 architecture | `docs/architecture/system-model.md` | MOVE | DESIGNED |
| CAP-1113 | `Continue Architecture Planning.md` | 33.33 The complete ownership invariant | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-1114 | `Continue Architecture Planning.md` | 33.34 The deeper distributed invariant | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-1115 | `Continue Architecture Planning.md` | 33.35 v0.33 result | `docs/architecture/concurrency.md` | MOVE | DESIGNED |
| CAP-1116 | `Continue Architecture Planning.md` | v0.34 — Coordination Protocol & Distributed Consistency | `docs/architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1117 | `Continue Architecture Planning.md` | *turn 82 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-1118 | `Continue Architecture Planning.md` | v0.34 — Distributed Consistency & Conflict Resolution | `docs/architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1119 | `Continue Architecture Planning.md` | 34.1 New Architecture Boundary | `docs/architecture/system-model.md` | MOVE | DESIGNED |
| CAP-1120 | `Continue Architecture Planning.md` | 34.2 The Core Consistency Model | `docs/architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1121 | `Continue Architecture Planning.md` | 34.3 Optimistic Concurrency Control | `docs/architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1122 | `Continue Architecture Planning.md` | 34.4 Version ≠ Time | `docs/architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1123 | `Continue Architecture Planning.md` | 34.5 Event Metadata | `docs/architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1124 | `Continue Architecture Planning.md` | 34.6 Versioning + Fencing | `docs/architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1125 | `Continue Architecture Planning.md` | 34.7 Conflict Is Not One Thing | `docs/architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1126 | `Continue Architecture Planning.md` | Claim conflict | `docs/architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1127 | `Continue Architecture Planning.md` | Candidate conflict | `docs/architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1128 | `Continue Architecture Planning.md` | Classification conflict | `docs/architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1129 | `Continue Architecture Planning.md` | Coverage conflict | `docs/architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1130 | `Continue Architecture Planning.md` | Budget conflict | `docs/architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1131 | `Continue Architecture Planning.md` | 34.8 Conflict Record | `docs/architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1132 | `Continue Architecture Planning.md` | 34.9 Deterministic Conflict Resolver | `docs/architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1133 | `Continue Architecture Planning.md` | 34.10 Resolution Policies | `docs/architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1134 | `Continue Architecture Planning.md` | 34.11 Classification Conflict | `docs/architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1135 | `Continue Architecture Planning.md` | 34.12 Provenance Must Survive Resolution | `docs/architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1136 | `Continue Architecture Planning.md` | 34.13 Last-Write-Wins Is Not the Default | `docs/architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1137 | `Continue Architecture Planning.md` | 34.14 Append-Only Is Especially Powerful | `docs/architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1138 | `Continue Architecture Planning.md` | 34.15 Materialized State | `docs/architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1139 | `Continue Architecture Planning.md` | 34.16 State Digest | `docs/architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1140 | `Continue Architecture Planning.md` | 34.17 Conflict Detection Pipeline | `docs/architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1141 | `Continue Architecture Planning.md` | 34.18 Conflict Detection vs Conflict Resolution | `docs/architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1142 | `Continue Architecture Planning.md` | 34.19 Conflict Resolver Context | `docs/architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1143 | `Continue Architecture Planning.md` | 34.20 Resolution Event | `docs/architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1144 | `Continue Architecture Planning.md` | 34.21 Cross-Object Conflicts | `docs/architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1145 | `Continue Architecture Planning.md` | 34.22 Consistency Domains | `docs/architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1146 | `Continue Architecture Planning.md` | 34.23 Consistency Is Not Global Ordering | `docs/architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1147 | `Continue Architecture Planning.md` | 34.24 Independent Evidence | `docs/architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1148 | `Continue Architecture Planning.md` | 34.25 Failure Taxonomy | `docs/validation/failure-taxonomy.md` | MOVE | DESIGNED |
| CAP-1149 | `Continue Architecture Planning.md` | 34.26 New Core Invariants | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-1150 | `Continue Architecture Planning.md` | Consistency | `docs/architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1151 | `Continue Architecture Planning.md` | Fencing | `docs/architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1152 | `Continue Architecture Planning.md` | Conflict | `docs/architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1153 | `Continue Architecture Planning.md` | Provenance | `docs/architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1154 | `Continue Architecture Planning.md` | Recovery | `docs/architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1155 | `Continue Architecture Planning.md` | Scalability | `docs/architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1156 | `Continue Architecture Planning.md` | 34.27 The Unified State Model | `docs/architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1157 | `Continue Architecture Planning.md` | 34.28 What v0.34 Actually Proves | `docs/validation/verification.md` | MOVE | OPEN |
| CAP-1158 | `Continue Architecture Planning.md` | PROVED by the architecture | `docs/validation/verification.md` | MOVE | OPEN |
| CAP-1159 | `Continue Architecture Planning.md` | ARGUMENT | `docs/validation/verification.md` | MOVE | OPEN |
| CAP-1160 | `Continue Architecture Planning.md` | OPEN | `docs/validation/verification.md` | MOVE | OPEN |
| CAP-1161 | `Continue Architecture Planning.md` | 34.29 Prototype Boundary | `docs/prototype/limitations.md` | MOVE | UNVERIFIED |
| CAP-1162 | `Continue Architecture Planning.md` | 34.30 v0.34 → v0.35 | `docs/roadmap/future-work.md` | MOVE | FUTURE |
| CAP-1163 | `Continue Architecture Planning.md` | *turn 84 you lead-in* | — | ARCHIVE | UNVERIFIED |
| CAP-1164 | `Continue Architecture Planning.md` | Conclusion — Generic Discovery Engine | `docs/concepts/overview.md` | MOVE | DESIGNED |
| CAP-1165 | `Continue Architecture Planning.md` | The decisive conceptual shift | `docs/concepts/overview.md` | MOVE | DESIGNED |
| CAP-1166 | `Continue Architecture Planning.md` | DVB blind scan | `docs/research/dvb-blind-scan.md` | MOVE | DESIGNED |
| CAP-1167 | `Continue Architecture Planning.md` | Generic discovery | `docs/architecture/coordination.md` | MOVE | DESIGNED |
| CAP-1168 | `Continue Architecture Planning.md` | The major architectural invariants | `docs/validation/invariants.md` | MOVE | DESIGNED |
| CAP-1169 | `Continue Architecture Planning.md` | Final architecture by responsibility | `docs/architecture/system-model.md` | MOVE | DESIGNED |
| CAP-1170 | `Continue Architecture Planning.md` | What the prototype actually becomes | `docs/concepts/overview.md` | MOVE | DESIGNED |
| CAP-1171 | `Continue Architecture Planning.md` | Final formulation | `docs/concepts/overview.md` | MOVE | DESIGNED |

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
| USP-014 | 14 | 3 | USP-013 | The key insight | CONCEPT | — | — | — |
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
| USP-030 | 30 | 3 | USP-029 | Exhaustive scan | ALGORITHM | — | — | — |
| USP-031 | 31 | 3 | USP-029 | Confidence-based scan | ALGORITHM | — | [C-06](REVIEW-NOTES.md#c-06--confidence-one-score-versus-no-single-global-score) | — |
| USP-032 | 32 | 3 | USP-029 | Time-bounded scan | ALGORITHM | — | — | — |
| USP-033 | 33 | 3 | USP-029 | Hybrid | ALGORITHM | — | — | — |
| USP-034 | 34 | 2 | — | 19. Coverage is a better metric than elapsed time | ALGORITHM | — | [C-05](REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified) | — |
| USP-035 | 35 | 2 | — | 20. Cache knowledge between scans | ARCHITECTURE | — | [C-10](REVIEW-NOTES.md#c-10--knowledge-store-naming) | — |
| USP-036 | 36 | 2 | — | 21. Handle disappearing multiplexes | DATA_MODEL | — | — | — |
| USP-037 | 37 | 2 | — | 22. The complete conceptual algorithm | ALGORITHM | — | — | — |
| USP-038 | 38 | 3 | USP-037 | 23. A useful formal name | CONCEPT | — | — | — |
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
| USP-051 | 51 | 3 | USP-050 | Candidate | CANDIDATE | — | — | — |
| USP-052 | 52 | 3 | USP-050 | Observation | OBSERVATION | — | — | — |
| USP-053 | 53 | 3 | USP-050 | LockResult | ACQUISITION | — | [C-02](REVIEW-NOTES.md#c-02--the-discovery-pipeline-is-described-with-two-different-step-sets) | — |
| USP-054 | 54 | 3 | USP-050 | Discovery | DISCOVERY | — | — | — |
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
| USP-065 | 65 | — | — | — | IMPLEMENTATION | `CAP-001` | [D-02](REVIEW-NOTES.md#d-02--) | lead-in of the following section; the source presents this as the delivered prototype; no implementation file in this repository verifies it |
| USP-066 | 66 | — | — | — | IMPLEMENTATION | `CAP-001` | [D-02](REVIEW-NOTES.md#d-02--) | the source presents this as the delivered prototype; no implementation file in this repository verifies it |
| USP-067 | 67 | — | — | — | PROTOTYPE | — | — | prototype positioning; the source presents this as the delivered prototype; no implementation file in this repository verifies it |
| USP-068 | 68 | 3 | — | The DVB analogy | DVB_ANALOGY | — | — | — |
| USP-069 | 69 | — | — | — | IMPLEMENTATION | `CAP-001` | [D-02](REVIEW-NOTES.md#d-02--) | lead-in of the following section; the source presents this as the delivered prototype; no implementation file in this repository verifies it |
| USP-070 | 70 | — | — | — | IMPLEMENTATION | `CAP-001` | [D-02](REVIEW-NOTES.md#d-02--) | the source presents this as the delivered prototype; no implementation file in this repository verifies it |
| USP-071 | 71 | 3 | — | What changed — 1. Concurrent claiming is now explicit | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | split at numbered boundary |
| USP-072 | 72 | 3 | — | What changed — 2. HTML is no longer special | PROVIDER | — | — | split at numbered boundary |
| USP-073 | 73 | 3 | — | What changed — 3. The actual scope is now explicit | SCOPE | — | — | split at numbered boundary; the source presents this as the delivered prototype; no implementation file in this repository verifies it |
| CAP-001 | 1 | — | — | — | DUPLICATE | `USP-065`, `USP-066`, `USP-069`, `USP-070` | [D-01](REVIEW-NOTES.md#d-01--) | near-duplicate of prototype/versions/01-v0.1.0.md and 02-v0.2.0.md; retained because both copies are damaged differently |
| CAP-002 | 2 | — | — | — | PROTOTYPE | — | — | assessment of the initial scripts; the source presents this as the delivered prototype; no implementation file in this repository verifies it |
| CAP-003 | 3 | — | — | — | IMPLEMENTATION | — | — | lead-in of the following section; the source presents this as the delivered prototype; no implementation file in this repository verifies it |
| CAP-004 | 4 | — | — | — | IMPLEMENTATION | — | — | the source presents this as the delivered prototype; no implementation file in this repository verifies it |
| CAP-005 | 5 | 3 | — | v0.3 — What changed from v0.2.0 | HISTORY | — | — | the source presents this as the delivered prototype; no implementation file in this repository verifies it |
| CAP-006 | 6 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-007 | 7 | — | — | — | ROADMAP | — | — | — |
| CAP-008 | 8 | 3 | — | v0.4 — The biggest v0.4 improvement | ROADMAP | — | — | — |
| CAP-009 | 9 | — | — | — | IMPLEMENTATION | — | — | lead-in of the following section; the source presents this as the delivered prototype; no implementation file in this repository verifies it |
| CAP-010 | 10 | — | — | — | IMPLEMENTATION | — | — | the source presents this as the delivered prototype; no implementation file in this repository verifies it |
| CAP-011 | 11 | 3 | — | v0.4 — Notable v0.4.0 behavior | HISTORY | — | — | the source presents this as the delivered prototype; no implementation file in this repository verifies it |
| CAP-012 | 12 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-013 | 13 | — | — | — | IMPLEMENTATION | — | [C-01](REVIEW-NOTES.md#c-01--prototype-version-numbering-is-not-monotonic) | the source presents this as the delivered prototype; no implementation file in this repository verifies it |
| CAP-014 | 14 | — | — | — | HISTORY | — | — | the source presents this as the delivered prototype; no implementation file in this repository verifies it |
| CAP-015 | 15 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-016 | 16 | — | — | — | IMPLEMENTATION | — | [C-01](REVIEW-NOTES.md#c-01--prototype-version-numbering-is-not-monotonic) | the source presents this as the delivered prototype; no implementation file in this repository verifies it |
| CAP-017 | 17 | 3 | — | v0.4 — What changed from v0.3.0 | HISTORY | — | — | the source presents this as the delivered prototype; no implementation file in this repository verifies it |
| CAP-018 | 18 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-019 | 19 | — | — | — | ROADMAP | — | — | — |
| CAP-020 | 20 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-021 | 21 | — | — | — | IMPLEMENTATION | — | — | the source presents this as the delivered prototype; no implementation file in this repository verifies it |
| CAP-022 | 22 | 3 | — | v0.5 architecture | HISTORY | — | — | explicit override; the source presents this as the delivered prototype; no implementation file in this repository verifies it |
| CAP-023 | 23 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-024 | 24 | — | — | — | IMPLEMENTATION | — | [C-01](REVIEW-NOTES.md#c-01--prototype-version-numbering-is-not-monotonic) | the source presents this as the delivered prototype; no implementation file in this repository verifies it |
| CAP-025 | 25 | 3 | — | v0.5 — What v0.6 changes architecturally | HISTORY | — | — | the source presents this as the delivered prototype; no implementation file in this repository verifies it |
| CAP-026 | 26 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-027 | 27 | — | — | — | IMPLEMENTATION | — | [C-01](REVIEW-NOTES.md#c-01--prototype-version-numbering-is-not-monotonic) | the source presents this as the delivered prototype; no implementation file in this repository verifies it |
| CAP-028 | 28 | 3 | — | v0.5 — What v0.5.0 changes architecturally | HISTORY | — | — | the source presents this as the delivered prototype; no implementation file in this repository verifies it |
| CAP-029 | 29 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-030 | 30 | — | — | — | IMPLEMENTATION | — | — | the source presents this as the delivered prototype; no implementation file in this repository verifies it |
| CAP-031 | 31 | 3 | — | v0.6.0's main architectural additions | HISTORY | — | — | explicit override; the source presents this as the delivered prototype; no implementation file in this repository verifies it |
| CAP-032 | 32 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-033 | 33 | — | — | — | IMPLEMENTATION | — | — | the source presents this as the delivered prototype; no implementation file in this repository verifies it |
| CAP-034 | 34 | 3 | — | v0.6 — What changed in v0.6 | HISTORY | — | — | the source presents this as the delivered prototype; no implementation file in this repository verifies it |
| CAP-035 | 35 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-036 | 36 | 2 | — | v0.7.0 — Discovery Graph + Acquisition Planner | DISCOVERY | — | — | — |
| CAP-037 | 37 | 3 | CAP-036 | v0.7 objectives | DATA_MODEL | — | — | — |
| CAP-038 | 38 | 3 | CAP-036 | v0.7 — Core contract | DATA_MODEL | — | — | — |
| CAP-039 | 39 | 3 | CAP-036 | v0.7 — Important v0.7 distinction | DATA_MODEL | — | — | — |
| CAP-040 | 40 | 2 | — | v0.7 state machine | DATA_MODEL | — | — | — |
| CAP-041 | 41 | 2 | — | v0.7 — The deeper abstraction | CONCEPT | — | — | — |
| CAP-042 | 42 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-043 | 43 | — | — | — | IMPLEMENTATION | — | — | the source presents this as the delivered prototype; no implementation file in this repository verifies it |
| CAP-044 | 44 | — | — | — | HISTORY | — | — | the source presents this as the delivered prototype; no implementation file in this repository verifies it |
| CAP-045 | 45 | 1 | — | v0.7 — What v0.7.1 actually changes | HISTORY | — | — | the source presents this as the delivered prototype; no implementation file in this repository verifies it |
| CAP-046 | 46 | 3 | CAP-045 | v0.7 — Before | HISTORY | — | — | the source presents this as the delivered prototype; no implementation file in this repository verifies it |
| CAP-047 | 47 | 3 | CAP-045 | v0.7 — Now | HISTORY | — | — | the source presents this as the delivered prototype; no implementation file in this repository verifies it |
| CAP-048 | 48 | 1 | — | v0.7 — 2. The ledger becomes the scan's causal trace | PROVENANCE | — | — | explicit override |
| CAP-049 | 49 | 1 | — | v0.7 — 3. PerformanceObserver correction | DATA_MODEL | — | — | explicit override |
| CAP-050 | 50 | 1 | — | v0.7 — 4. Candidate state machine | HISTORY | — | — | the source presents this as the delivered prototype; no implementation file in this repository verifies it |
| CAP-051 | 51 | 1 | — | v0.7 — 5. The ledger is not merely logging | PROVENANCE | — | — | explicit override |
| CAP-052 | 52 | 1 | — | v0.7 — 6. One remaining architectural limitation | LIMITATIONS | — | — | — |
| CAP-053 | 53 | 1 | — | v0.7 — 7. Architecture after v0.7.1 | ARCHITECTURE | — | — | — |
| CAP-054 | 54 | 2 | CAP-053 | v0.7 — Next boundary: v0.8 | ROADMAP | — | — | — |
| CAP-055 | 55 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-056 | 56 | 1 | — | v0.8 — Capability-Aware Acquisition Runtime | ACQUISITION | — | — | — |
| CAP-057 | 57 | 2 | CAP-056 | v0.8 — 1. The three graphs | ARCHITECTURE | — | — | — |
| CAP-058 | 58 | 3 | CAP-057 | v0.8 — Discovery graph | DISCOVERY | — | — | — |
| CAP-059 | 59 | 3 | CAP-057 | v0.8 — Acquisition graph | ACQUISITION | — | — | — |
| CAP-060 | 60 | 3 | CAP-057 | v0.8 — Evidence graph | ARCHITECTURE | — | — | — |
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
| CAP-074 | 74 | 3 | CAP-073 | v0.8 — Implement | ARCHITECTURE | — | — | — |
| CAP-075 | 75 | 3 | CAP-073 | v0.8 — Represent but deny | SECURITY | — | — | — |
| CAP-076 | 76 | 1 | — | v0.8 — 15. Updated system invariant | VALIDATION | — | — | — |
| CAP-077 | 77 | 1 | — | v0.8 — 16. The DVB analogy is now cleaner | DVB_ANALOGY | — | — | — |
| CAP-078 | 78 | 1 | — | v0.8 — 17. v0.8 → v0.9 | ROADMAP | — | — | — |
| CAP-079 | 79 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-080 | 80 | 2 | — | v0.9 — Acquisition Provider Architecture | ACQUISITION | — | — | — |
| CAP-081 | 81 | 3 | CAP-080 | v0.9 — 0.9 architecture | ARCHITECTURE | — | — | — |
| CAP-082 | 82 | 3 | CAP-080 | v0.9 — The important separation | ACQUISITION | — | — | explicit override |
| CAP-083 | 83 | 1 | — | v0.9 — 1. AcquisitionProvider contract | ACQUISITION | — | — | — |
| CAP-084 | 84 | 1 | — | v0.9 — 2. Provider capabilities | PROVIDER | — | — | — |
| CAP-085 | 85 | 1 | — | v0.9 — 3. Provider selection | PROVIDER | — | — | — |
| CAP-086 | 86 | 1 | — | v0.9 — 4. GM-XHR becomes a component | PROVIDER | — | — | — |
| CAP-087 | 87 | 1 | — | v0.9 — 5. Observation gets provider provenance | OBSERVATION | — | — | — |
| CAP-088 | 88 | 1 | — | v0.9 — 6. Provider failure ≠ acquisition denial | ACQUISITION | — | — | — |
| CAP-089 | 89 | 3 | CAP-088 | v0.9 — Policy denial | SECURITY | — | [C-11](REVIEW-NOTES.md#c-11--same-origin-default-versus-cross-origin-capability) | — |
| CAP-090 | 90 | 3 | CAP-088 | v0.9 — Provider failure | PROVIDER | — | — | — |
| CAP-091 | 91 | 1 | — | v0.9 — 7. Provider selection itself becomes an event | PROVIDER | — | — | — |
| CAP-092 | 92 | 1 | — | v0.9 — 8. A deeper consequence: acquisition becomes replaceable | ACQUISITION | — | — | explicit override |
| CAP-093 | 93 | 3 | CAP-092 | v0.9 — Cache provider | PROVIDER | — | — | — |
| CAP-094 | 94 | 3 | CAP-092 | v0.9 — Replay provider | PROVIDER | — | [C-08](REVIEW-NOTES.md#c-08--replay-decisions-deterministic-network-not) | — |
| CAP-095 | 95 | 1 | — | v0.9 — 9. The engine is now approaching a general resource runtime | PROVIDER | — | — | — |
| CAP-096 | 96 | 1 | — | v0.9 — 10. v0.9 invariants | VALIDATION | — | — | — |
| CAP-097 | 97 | 3 | CAP-096 | v0.9 — I1 — Discovery independence | VALIDATION | — | — | — |
| CAP-098 | 98 | 3 | CAP-096 | v0.9 — I2 — Policy independence | SECURITY | — | [C-11](REVIEW-NOTES.md#c-11--same-origin-default-versus-cross-origin-capability) | — |
| CAP-099 | 99 | 3 | CAP-096 | v0.9 — I3 — Capability soundness | VALIDATION | — | — | — |
| CAP-100 | 100 | 3 | CAP-096 | v0.9 — I4 — Method safety | VALIDATION | — | — | — |
| CAP-101 | 101 | 3 | CAP-096 | v0.9 — I5 — Provenance | PROVENANCE | — | — | — |
| CAP-102 | 102 | 3 | CAP-096 | v0.9 — I6 — Observation integrity | OBSERVATION | — | — | — |
| CAP-103 | 103 | 3 | CAP-096 | v0.9 — I7 — Replay distinction | VALIDATION | — | [C-08](REVIEW-NOTES.md#c-08--replay-decisions-deterministic-network-not) | — |
| CAP-104 | 104 | 1 | — | v0.9 — 11. The next problem is now visible | ROADMAP | — | — | — |
| CAP-105 | 105 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-106 | 106 | 1 | — | v0.10 — Acquisition Runtime | ACQUISITION | — | — | — |
| CAP-107 | 107 | 2 | CAP-106 | v0.10 — 1. The new architecture | ARCHITECTURE | — | — | — |
| CAP-108 | 108 | 1 | — | v0.10 — 2. The key distinction: Scheduler vs Runtime | SCHEDULING | — | — | — |
| CAP-109 | 109 | 3 | CAP-108 | v0.10 — Scheduler | SCHEDULING | — | — | — |
| CAP-110 | 110 | 3 | CAP-108 | v0.10 — Runtime | ACQUISITION | — | — | — |
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
| CAP-126 | 126 | 2 | CAP-125 | v0.10 — What v0.10 accomplishes | CONCEPT | — | — | — |
| CAP-127 | 127 | 3 | CAP-126 | v0.10 — Next boundary: v0.11 | ROADMAP | — | — | — |
| CAP-128 | 128 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-129 | 129 | 1 | — | v0.11 — Response Recognition Runtime | ACQUISITION | — | [C-02](REVIEW-NOTES.md#c-02--the-discovery-pipeline-is-described-with-two-different-step-sets) | — |
| CAP-130 | 130 | 2 | CAP-129 | v0.11 — 1. v0.11 architecture | ARCHITECTURE | — | — | — |
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
| CAP-142 | 142 | 3 | CAP-141 | v0.11 — No recognizer | ACQUISITION | — | — | — |
| CAP-143 | 143 | 3 | CAP-141 | v0.11 — Provider rejected | PROVIDER | — | — | — |
| CAP-144 | 144 | 3 | CAP-141 | v0.11 — Provider error | PROVIDER | — | — | — |
| CAP-145 | 145 | 3 | CAP-141 | v0.11 — Successful recognition, zero discoveries | ACQUISITION | — | [C-02](REVIEW-NOTES.md#c-02--the-discovery-pipeline-is-described-with-two-different-step-sets) | — |
| CAP-146 | 146 | 1 | — | v0.11 — 13. v0.11 state progression | ACQUISITION | — | — | — |
| CAP-147 | 147 | 1 | — | v0.11 — 14. Multiple recognizers | ACQUISITION | — | — | — |
| CAP-148 | 148 | 1 | — | v0.11 — 15. Recognition graph | ACQUISITION | — | [C-02](REVIEW-NOTES.md#c-02--the-discovery-pipeline-is-described-with-two-different-step-sets) | — |
| CAP-149 | 149 | 1 | — | v0.11 — 16. The graph is now explicitly causal | ACQUISITION | — | — | — |
| CAP-150 | 150 | 1 | — | v0.11 — 17. v0.11 event ledger | ACQUISITION | — | — | — |
| CAP-151 | 151 | 1 | — | v0.11 — 18. The emerging generic algorithm | ALGORITHM | — | — | — |
| CAP-152 | 152 | 1 | — | v0.11 — 19. The next major abstraction: Candidate Sources | ROADMAP | — | — | — |
| CAP-153 | 153 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-154 | 154 | 1 | — | v0.12 — Candidate Source Architecture | CANDIDATE | — | — | — |
| CAP-155 | 155 | 2 | CAP-154 | v0.12 — 1. Three independent provider planes | PROVIDER | — | — | explicit override |
| CAP-156 | 156 | 1 | — | v0.12 — 2. CandidateSource contract | CANDIDATE | — | — | — |
| CAP-157 | 157 | 1 | — | v0.12 — 3. CandidateSource is a search-space adapter | CANDIDATE | — | — | — |
| CAP-158 | 158 | 3 | CAP-157 | v0.12 — Web page | PROVIDER | — | — | — |
| CAP-159 | 159 | 3 | CAP-157 | v0.12 — Network traffic | PROVIDER | — | — | — |
| CAP-160 | 160 | 3 | CAP-157 | v0.12 — Sitemap | PROVIDER | — | — | — |
| CAP-161 | 161 | 3 | CAP-157 | v0.12 — User seed | PROVIDER | — | — | — |
| CAP-162 | 162 | 3 | CAP-157 | v0.12 — Document | PROVIDER | — | — | — |
| CAP-163 | 163 | 1 | — | v0.12 — 4. CandidateProposal | CANDIDATE | — | — | — |
| CAP-164 | 164 | 1 | — | v0.12 — 5. Why proposals matter | PROVIDER | — | — | — |
| CAP-165 | 165 | 1 | — | v0.12 — 6. CandidateNormalizer | CANDIDATE | — | — | — |
| CAP-166 | 166 | 1 | — | v0.12 — 7. Source Registry | PROVIDER | — | — | — |
| CAP-167 | 167 | 1 | — | v0.12 — 8. The HTML provider should evolve | PROVIDER | — | — | explicit override |
| CAP-168 | 168 | 1 | — | v0.12 — 9. Evidence becomes an intermediate layer | PROVIDER | — | — | — |
| CAP-169 | 169 | 1 | — | v0.12 — 10. Discovery becomes evidence-driven | PROVIDER | — | — | — |
| CAP-170 | 170 | 1 | — | v0.12 — 11. CandidateSource context | CANDIDATE | — | — | — |
| CAP-171 | 171 | 1 | — | v0.12 — 12. CandidateSource examples | CANDIDATE | — | — | — |
| CAP-172 | 172 | 3 | CAP-171 | v0.12 — HTML link source | PROVIDER | — | — | — |
| CAP-173 | 173 | 1 | — | v0.12 — 13. NetworkSource | PROVIDER | — | — | — |
| CAP-174 | 174 | 1 | — | v0.12 — 14. Search-space composition | PROVIDER | — | — | — |
| CAP-175 | 175 | 1 | — | v0.12 — 15. Candidate identity | CANDIDATE | — | [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution) | — |
| CAP-176 | 176 | 1 | — | v0.12 — 16. Discovery confidence aggregation | PROVIDER | — | [C-06](REVIEW-NOTES.md#c-06--confidence-one-score-versus-no-single-global-score) | — |
| CAP-177 | 177 | 1 | — | v0.12 — 17. v0.12 provenance graph | PROVENANCE | — | — | — |
| CAP-178 | 178 | 1 | — | v0.12 — 18. v0.12 invariants | VALIDATION | — | — | — |
| CAP-179 | 179 | 3 | CAP-178 | v0.12 — S1 — Source purity | VALIDATION | — | — | — |
| CAP-180 | 180 | 3 | CAP-178 | v0.12 — S2 — Core ownership | VALIDATION | — | — | — |
| CAP-181 | 181 | 3 | CAP-178 | v0.12 — S3 — Proposal semantics | VALIDATION | — | — | — |
| CAP-182 | 182 | 3 | CAP-178 | v0.12 — S4 — Identity | VALIDATION | — | [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution) | — |
| CAP-183 | 183 | 3 | CAP-178 | v0.12 — S5 — Provenance | PROVENANCE | — | — | — |
| CAP-184 | 184 | 3 | CAP-178 | v0.12 — S6 — Representability | VALIDATION | — | — | — |
| CAP-185 | 185 | 3 | CAP-178 | v0.12 — S7 — Observation independence | OBSERVATION | — | — | — |
| CAP-186 | 186 | 1 | — | v0.12 — 19. The complete v0.12 architecture | ARCHITECTURE | — | — | — |
| CAP-187 | 187 | 1 | — | v0.12 — 20. The deeper abstraction | CONCEPT | — | — | — |
| CAP-188 | 188 | 2 | CAP-187 | v0.13 — the next boundary | ROADMAP | — | — | — |
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
| CAP-211 | 211 | 3 | CAP-210 | v0.13 — D1 — Source isolation | VALIDATION | — | — | — |
| CAP-212 | 212 | 3 | CAP-210 | v0.13 — D2 — Acquisition isolation | ACQUISITION | — | — | — |
| CAP-213 | 213 | 3 | CAP-210 | v0.13 — D3 — Normalization ownership | VALIDATION | — | — | — |
| CAP-214 | 214 | 3 | CAP-210 | v0.13 — D4 — Bounded generation | VALIDATION | — | — | — |
| CAP-215 | 215 | 3 | CAP-210 | v0.13 — D5 — Bounded recursion | VALIDATION | — | — | — |
| CAP-216 | 216 | 3 | CAP-210 | v0.13 — D6 — Provenance preservation | PROVENANCE | — | — | — |
| CAP-217 | 217 | 3 | CAP-210 | v0.13 — D7 — Atomic task claiming | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-218 | 218 | 3 | CAP-210 | v0.13 — D8 — Convergence | VALIDATION | — | — | — |
| CAP-219 | 219 | 3 | CAP-210 | v0.13 — D9 — Discovery/acquisition independence | ACQUISITION | — | — | — |
| CAP-220 | 220 | 1 | — | v0.13 — 21. The architecture is now approaching a stable core | ARCHITECTURE | — | — | — |
| CAP-221 | 221 | 1 | — | v0.14 — the next missing abstraction | ROADMAP | — | — | — |
| CAP-222 | 222 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-223 | 223 | 1 | — | v0.14 — DiscoveryDomain + ScanSession | ARCHITECTURE | — | — | — |
| CAP-224 | 224 | 1 | — | v0.14 — 1. The conceptual split | ARCHITECTURE | — | — | — |
| CAP-225 | 225 | 3 | CAP-224 | v0.14 — Discovery Engine | DISCOVERY | — | — | — |
| CAP-226 | 226 | 3 | CAP-224 | v0.14 — DiscoveryDomain | ARCHITECTURE | — | — | — |
| CAP-227 | 227 | 3 | CAP-224 | v0.14 — ScanSession | ARCHITECTURE | — | — | — |
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
| CAP-238 | 238 | 3 | CAP-237 | v0.14 — Frontier exhaustion | ARCHITECTURE | — | — | explicit override |
| CAP-239 | 239 | 3 | CAP-237 | v0.14 — Candidate limit | CANDIDATE | — | — | explicit override |
| CAP-240 | 240 | 3 | CAP-237 | v0.14 — Acquisition limit | ACQUISITION | — | — | explicit override |
| CAP-241 | 241 | 3 | CAP-237 | v0.14 — Discovery-task limit | DISCOVERY | — | — | explicit override |
| CAP-242 | 242 | 3 | CAP-237 | v0.14 — Proposal limit | ARCHITECTURE | — | — | — |
| CAP-243 | 243 | 3 | CAP-237 | v0.14 — Depth limit | ARCHITECTURE | — | — | — |
| CAP-244 | 244 | 3 | CAP-237 | v0.14 — Time limit | ARCHITECTURE | — | — | — |
| CAP-245 | 245 | 3 | CAP-237 | v0.14 — External stop | ARCHITECTURE | — | — | — |
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
| CAP-259 | 259 | 3 | CAP-258 | v0.14 — Domain invariant | VALIDATION | — | — | — |
| CAP-260 | 260 | 3 | CAP-258 | v0.14 — Session invariant | VALIDATION | — | — | — |
| CAP-261 | 261 | 3 | CAP-258 | v0.14 — Snapshot invariant | VALIDATION | — | — | — |
| CAP-262 | 262 | 3 | CAP-258 | v0.14 — Frontier invariant | VALIDATION | — | — | — |
| CAP-263 | 263 | 3 | CAP-258 | v0.14 — Termination invariant | VALIDATION | — | [C-09](REVIEW-NOTES.md#c-09--two-termination-taxonomies) | — |
| CAP-264 | 264 | 3 | CAP-258 | v0.14 — Recovery invariant | VALIDATION | — | — | — |
| CAP-265 | 265 | 3 | CAP-258 | v0.14 — Provenance invariant | PROVENANCE | — | — | — |
| CAP-266 | 266 | 3 | CAP-258 | v0.14 — Acquisition invariant | ACQUISITION | — | — | — |
| CAP-267 | 267 | 3 | CAP-258 | v0.14 — Discovery invariant | VALIDATION | — | — | — |
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
| CAP-312 | 312 | 3 | CAP-311 | v0.16 — Observation | OBSERVATION | — | — | — |
| CAP-313 | 313 | 3 | CAP-311 | v0.16 — Evidence | DATA_MODEL | — | — | — |
| CAP-314 | 314 | 3 | CAP-311 | v0.16 — Claim | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
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
| CAP-347 | 347 | 3 | CAP-346 | v0.16 — Evidence provenance | PROVENANCE | — | — | — |
| CAP-348 | 348 | 3 | CAP-346 | v0.16 — Claim support | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-349 | 349 | 3 | CAP-346 | v0.16 — Historical integrity | DATA_MODEL | — | — | — |
| CAP-350 | 350 | 3 | CAP-346 | v0.16 — Extraction integrity | DATA_MODEL | — | — | — |
| CAP-351 | 351 | 3 | CAP-346 | v0.16 — Resource identity | DATA_MODEL | — | [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution) | — |
| CAP-352 | 352 | 3 | CAP-346 | v0.16 — Content identity | DATA_MODEL | — | [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution) | — |
| CAP-353 | 353 | 3 | CAP-346 | v0.16 — Conflict preservation | DATA_MODEL | — | — | — |
| CAP-354 | 354 | 3 | CAP-346 | v0.16 — Provenance preservation | PROVENANCE | — | — | — |
| CAP-355 | 355 | 3 | CAP-346 | v0.16 — Session provenance | PROVENANCE | — | — | — |
| CAP-356 | 356 | 1 | — | v0.16 — 35. Failure taxonomy | VALIDATION | — | — | — |
| CAP-357 | 357 | 1 | — | v0.16 — 36. The deeper architectural transition | ROADMAP | — | — | — |
| CAP-358 | 358 | 1 | — | v0.16 — 37. What is still missing | ROADMAP | — | — | — |
| CAP-359 | 359 | 3 | CAP-358 | v0.16 — Search space | ARCHITECTURE | — | — | — |
| CAP-360 | 360 | 3 | CAP-358 | v0.16 — Execution | DATA_MODEL | — | — | — |
| CAP-361 | 361 | 3 | CAP-358 | v0.16 — Work | DATA_MODEL | — | — | — |
| CAP-362 | 362 | 3 | CAP-358 | v0.16 — Acquisition | ACQUISITION | — | — | — |
| CAP-363 | 363 | 3 | CAP-358 | v0.16 — Recognition | ACQUISITION | — | [C-02](REVIEW-NOTES.md#c-02--the-discovery-pipeline-is-described-with-two-different-step-sets) | — |
| CAP-364 | 364 | 3 | CAP-358 | v0.16 — Discovery | DISCOVERY | — | — | — |
| CAP-365 | 365 | 3 | CAP-358 | v0.16 — Evidence | DATA_MODEL | — | — | — |
| CAP-366 | 366 | 3 | CAP-358 | v0.16 — History | DATA_MODEL | — | — | — |
| CAP-367 | 367 | 1 | — | v0.17 — ResourceGraph + Identity Resolution | DATA_MODEL | — | [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution) | — |
| CAP-368 | 368 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-369 | 369 | 1 | — | v0.17 — ResourceGraph + Identity Resolution | DATA_MODEL | — | [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution) | — |
| CAP-370 | 370 | 1 | — | v0.17 — 1. The core problem | DATA_MODEL | — | — | — |
| CAP-371 | 371 | 1 | — | v0.17 — 2. Resource identity must become graph-based | DATA_MODEL | — | [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution) | — |
| CAP-372 | 372 | 1 | — | v0.17 — 3. Candidate vs Resource vs Locator | CANDIDATE | — | — | — |
| CAP-373 | 373 | 3 | CAP-372 | v0.17 — Candidate | CANDIDATE | — | — | — |
| CAP-374 | 374 | 3 | CAP-372 | v0.17 — Locator | DATA_MODEL | — | — | — |
| CAP-375 | 375 | 3 | CAP-372 | v0.17 — Resource | DATA_MODEL | — | — | — |
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
| CAP-400 | 400 | 3 | CAP-399 | v0.17 — What URLs identify this resource? | DATA_MODEL | — | — | — |
| CAP-401 | 401 | 3 | CAP-399 | v0.17 — Where was it discovered? | DATA_MODEL | — | — | — |
| CAP-402 | 402 | 3 | CAP-399 | v0.17 — What URLs redirect to it? | DATA_MODEL | — | — | — |
| CAP-403 | 403 | 3 | CAP-399 | v0.17 — Which URLs have identical observed bytes? | DATA_MODEL | — | — | — |
| CAP-404 | 404 | 3 | CAP-399 | v0.17 — Has this resource changed? | DATA_MODEL | — | — | — |
| CAP-405 | 405 | 3 | CAP-399 | v0.17 — Why do we believe two URLs are related? | DATA_MODEL | — | — | — |
| CAP-406 | 406 | 1 | — | v0.17 — 28. Resource graph example | DATA_MODEL | — | — | — |
| CAP-407 | 407 | 1 | — | v0.17 — 29. Failure taxonomy | VALIDATION | — | — | — |
| CAP-408 | 408 | 1 | — | v0.17 — 30. Core invariants | VALIDATION | — | — | — |
| CAP-409 | 409 | 3 | CAP-408 | v0.17 — Locator preservation | DATA_MODEL | — | — | — |
| CAP-410 | 410 | 3 | CAP-408 | v0.17 — No destructive merge | DATA_MODEL | — | — | — |
| CAP-411 | 411 | 3 | CAP-408 | v0.17 — Fingerprint independence | DATA_MODEL | — | [C-07](REVIEW-NOTES.md#c-07--resource--artifact-model-revised) | — |
| CAP-412 | 412 | 3 | CAP-408 | v0.17 — Redirect independence | DATA_MODEL | — | — | — |
| CAP-413 | 413 | 3 | CAP-408 | v0.17 — Evidence-backed identity | DATA_MODEL | — | [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution) | — |
| CAP-414 | 414 | 3 | CAP-408 | v0.17 — Revision preservation | DATA_MODEL | — | [C-07](REVIEW-NOTES.md#c-07--resource--artifact-model-revised) | — |
| CAP-415 | 415 | 3 | CAP-408 | v0.17 — Canonicalization transparency | DATA_MODEL | — | [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution) | — |
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
| CAP-431 | 431 | 3 | CAP-430 | v0.18 — Recognition | DATA_MODEL | — | [C-02](REVIEW-NOTES.md#c-02--the-discovery-pipeline-is-described-with-two-different-step-sets) | — |
| CAP-432 | 432 | 3 | CAP-430 | v0.18 — Classification | DATA_MODEL | — | — | — |
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
| CAP-448 | 448 | 3 | CAP-447 | v0.18 — Invariant 1 — Type is not identity | VALIDATION | — | [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution) | — |
| CAP-449 | 449 | 3 | CAP-447 | v0.18 — Invariant 2 — URL does not determine semantic type | VALIDATION | — | — | — |
| CAP-450 | 450 | 3 | CAP-447 | v0.18 — Invariant 3 — Technical recognition does not determine semantic role | VALIDATION | — | [C-02](REVIEW-NOTES.md#c-02--the-discovery-pipeline-is-described-with-two-different-step-sets) | — |
| CAP-451 | 451 | 3 | CAP-447 | v0.18 — Invariant 4 — Classification requires evidence | VALIDATION | — | — | — |
| CAP-452 | 452 | 3 | CAP-447 | v0.18 — Invariant 5 — Classification does not imply authorization | VALIDATION | — | — | — |
| CAP-453 | 453 | 3 | CAP-447 | v0.18 — Invariant 6 — Historical classification is immutable | VALIDATION | — | — | — |
| CAP-454 | 454 | 3 | CAP-447 | v0.18 — Invariant 7 — Contradiction is preserved | VALIDATION | — | — | — |
| CAP-455 | 455 | 3 | CAP-447 | v0.18 — Invariant 8 — Type axes remain independent | VALIDATION | — | — | — |
| CAP-456 | 456 | 1 | — | v0.18 — 18.24 The Larger Concept | CONCEPT | — | — | — |
| CAP-457 | 457 | 1 | — | v0.19 — Resource Representation & Revision Model | DATA_MODEL | — | [C-07](REVIEW-NOTES.md#c-07--resource--artifact-model-revised) | — |
| CAP-458 | 458 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-459 | 459 | 1 | — | v0.19 — Resource Representation + Artifact + Revision Model | DATA_MODEL | — | [C-07](REVIEW-NOTES.md#c-07--resource--artifact-model-revised) | — |
| CAP-460 | 460 | 2 | CAP-459 | v0.19 — 19.1 The Core Distinction | DATA_MODEL | — | — | — |
| CAP-461 | 461 | 3 | CAP-460 | v0.19 — Resource | DATA_MODEL | — | — | — |
| CAP-462 | 462 | 3 | CAP-460 | v0.19 — Representation | DATA_MODEL | — | — | — |
| CAP-463 | 463 | 3 | CAP-460 | v0.19 — Artifact | DATA_MODEL | — | [C-07](REVIEW-NOTES.md#c-07--resource--artifact-model-revised) | — |
| CAP-464 | 464 | 3 | CAP-460 | v0.19 — Observation | OBSERVATION | — | — | — |
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
| CAP-479 | 479 | 3 | CAP-478 | v0.19 — Resource state | DATA_MODEL | — | — | — |
| CAP-480 | 480 | 3 | CAP-478 | v0.19 — Artifact state | DATA_MODEL | — | [C-07](REVIEW-NOTES.md#c-07--resource--artifact-model-revised) | — |
| CAP-481 | 481 | 3 | CAP-478 | v0.19 — Observation state | OBSERVATION | — | — | — |
| CAP-482 | 482 | 1 | — | v0.19 — 19.16 ResourceGraph v0.19 | DATA_MODEL | — | — | — |
| CAP-483 | 483 | 1 | — | v0.19 — 19.17 ResourceGraph API | DATA_MODEL | — | — | — |
| CAP-484 | 484 | 1 | — | v0.19 — 19.18 Artifact Deduplication | DATA_MODEL | — | [C-07](REVIEW-NOTES.md#c-07--resource--artifact-model-revised) | — |
| CAP-485 | 485 | 3 | CAP-484 | v0.19 — Locator deduplication | DATA_MODEL | — | — | — |
| CAP-486 | 486 | 3 | CAP-484 | v0.19 — Artifact deduplication | DATA_MODEL | — | [C-07](REVIEW-NOTES.md#c-07--resource--artifact-model-revised) | — |
| CAP-487 | 487 | 1 | — | v0.19 — 19.19 Content-Addressed Storage | DATA_MODEL | — | — | — |
| CAP-488 | 488 | 1 | — | v0.19 — 19.20 Verification Levels | VALIDATION | — | — | — |
| CAP-489 | 489 | 1 | — | v0.19 — 19.21 Independent Confirmation | DATA_MODEL | — | — | — |
| CAP-490 | 490 | 1 | — | v0.19 — 19.22 Resource Confidence | DATA_MODEL | — | [C-06](REVIEW-NOTES.md#c-06--confidence-one-score-versus-no-single-global-score) | — |
| CAP-491 | 491 | 1 | — | v0.19 — 19.23 Example | DATA_MODEL | — | — | — |
| CAP-492 | 492 | 3 | CAP-491 | v0.19 — Step 1 — Locator | EXAMPLE | — | — | — |
| CAP-493 | 493 | 3 | CAP-491 | v0.19 — Step 2 — Resource | EXAMPLE | — | — | — |
| CAP-494 | 494 | 3 | CAP-491 | v0.19 — Step 3 — Observation | OBSERVATION | — | — | — |
| CAP-495 | 495 | 3 | CAP-491 | v0.19 — Step 4 — Artifact | EXAMPLE | — | [C-07](REVIEW-NOTES.md#c-07--resource--artifact-model-revised) | — |
| CAP-496 | 496 | 3 | CAP-491 | v0.19 — Step 5 — Representation | EXAMPLE | — | — | — |
| CAP-497 | 497 | 3 | CAP-491 | v0.19 — Step 6 — Classification | EXAMPLE | — | — | — |
| CAP-498 | 498 | 3 | CAP-491 | v0.19 — Step 7 — Revision | EXAMPLE | — | [C-07](REVIEW-NOTES.md#c-07--resource--artifact-model-revised) | — |
| CAP-499 | 499 | 1 | — | v0.19 — 19.24 A More Precise End-to-End Pipeline | DATA_MODEL | — | — | — |
| CAP-500 | 500 | 1 | — | v0.19 — 19.25 New Invariants | VALIDATION | — | — | — |
| CAP-501 | 501 | 3 | CAP-500 | v0.19 — Artifact invariant | VALIDATION | — | [C-07](REVIEW-NOTES.md#c-07--resource--artifact-model-revised) | — |
| CAP-502 | 502 | 3 | CAP-500 | v0.19 — Resource invariant | VALIDATION | — | — | — |
| CAP-503 | 503 | 3 | CAP-500 | v0.19 — Representation invariant | VALIDATION | — | — | — |
| CAP-504 | 504 | 3 | CAP-500 | v0.19 — Revision invariant | VALIDATION | — | [C-07](REVIEW-NOTES.md#c-07--resource--artifact-model-revised) | — |
| CAP-505 | 505 | 3 | CAP-500 | v0.19 — Observation invariant | OBSERVATION | — | — | — |
| CAP-506 | 506 | 3 | CAP-500 | v0.19 — Deduplication invariant | VALIDATION | — | — | — |
| CAP-507 | 507 | 3 | CAP-500 | v0.19 — Change invariant | VALIDATION | — | — | — |
| CAP-508 | 508 | 3 | CAP-500 | v0.19 — Classification invariant | VALIDATION | — | — | — |
| CAP-509 | 509 | 1 | — | v0.19 — 19.26 Failure Modes | VALIDATION | — | — | — |
| CAP-510 | 510 | 1 | — | v0.19 — 19.27 What v0.19 Gives Us | DATA_MODEL | — | — | — |
| CAP-511 | 511 | 2 | CAP-510 | v0.19 — Next boundary: v0.20 — Search-Space Partitioning + Discovery Strategies | ROADMAP | — | — | — |
| CAP-512 | 512 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-513 | 513 | 1 | — | v0.20 — Search-Space Partitioning + Discovery Strategies | DISCOVERY | — | — | — |
| CAP-514 | 514 | 1 | — | v0.20 — 20.1 The Search Space | ARCHITECTURE | — | — | — |
| CAP-515 | 515 | 1 | — | v0.20 — 20.2 What Is a Partition? | ARCHITECTURE | — | — | — |
| CAP-516 | 516 | 1 | — | v0.20 — 20.3 Partition ≠ Candidate | CANDIDATE | — | — | — |
| CAP-517 | 517 | 1 | — | v0.20 — 20.4 Partition Object | ARCHITECTURE | — | — | — |
| CAP-518 | 518 | 1 | — | v0.20 — 20.5 Partition State | ARCHITECTURE | — | — | — |
| CAP-519 | 519 | 3 | CAP-518 | v0.20 — Saturated | ARCHITECTURE | — | — | — |
| CAP-520 | 520 | 3 | CAP-518 | v0.20 — Exhausted | ARCHITECTURE | — | — | — |
| CAP-521 | 521 | 1 | — | v0.20 — 20.6 Search Coverage | ARCHITECTURE | — | [C-05](REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified) | — |
| CAP-522 | 522 | 1 | — | v0.20 — 20.7 Strategy Contract | ALGORITHM | — | — | — |
| CAP-523 | 523 | 1 | — | v0.20 — 20.8 Strategy vs Candidate Source | CANDIDATE | — | — | — |
| CAP-524 | 524 | 1 | — | v0.20 — 20.9 Strategy Types | ALGORITHM | — | — | — |
| CAP-525 | 525 | 3 | CAP-524 | v0.20 — Seed Expansion | ARCHITECTURE | — | — | — |
| CAP-526 | 526 | 3 | CAP-524 | v0.20 — Repository Expansion | ARCHITECTURE | — | — | — |
| CAP-527 | 527 | 3 | CAP-524 | v0.20 — Sitemap Expansion | ARCHITECTURE | — | — | — |
| CAP-528 | 528 | 3 | CAP-524 | v0.20 — API Schema Expansion | ARCHITECTURE | — | — | — |
| CAP-529 | 529 | 3 | CAP-524 | v0.20 — Document-Family Expansion | ARCHITECTURE | — | — | — |
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
| CAP-550 | 550 | 3 | CAP-549 | v0.20 — Search-space invariant | VALIDATION | — | — | — |
| CAP-551 | 551 | 3 | CAP-549 | v0.20 — Strategy invariant | VALIDATION | — | — | — |
| CAP-552 | 552 | 3 | CAP-549 | v0.20 — Acquisition invariant | ACQUISITION | — | — | — |
| CAP-553 | 553 | 3 | CAP-549 | v0.20 — Partition invariant | VALIDATION | — | — | — |
| CAP-554 | 554 | 3 | CAP-549 | v0.20 — Coverage invariant | VALIDATION | — | [C-05](REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified) | — |
| CAP-555 | 555 | 3 | CAP-549 | v0.20 — Discovery invariant | VALIDATION | — | — | — |
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
| CAP-590 | 590 | 3 | CAP-589 | v0.21 — Safety invariant | VALIDATION | — | — | — |
| CAP-591 | 591 | 3 | CAP-589 | v0.21 — Capability invariant | VALIDATION | — | — | — |
| CAP-592 | 592 | 3 | CAP-589 | v0.21 — Domain invariant | VALIDATION | — | — | — |
| CAP-593 | 593 | 3 | CAP-589 | v0.21 — Exploration invariant | VALIDATION | — | — | — |
| CAP-594 | 594 | 3 | CAP-589 | v0.21 — Historical invariant | VALIDATION | — | — | — |
| CAP-595 | 595 | 3 | CAP-589 | v0.21 — Replay invariant | VALIDATION | — | [C-08](REVIEW-NOTES.md#c-08--replay-decisions-deterministic-network-not) | — |
| CAP-596 | 596 | 3 | CAP-589 | v0.21 — Provenance invariant | PROVENANCE | — | — | — |
| CAP-597 | 597 | 1 | — | v0.21 — 21.30 Architecture After v0.21 | ARCHITECTURE | — | — | — |
| CAP-598 | 598 | 1 | — | v0.21 — 21.31 The Important Conceptual Shift | CONCEPT | — | — | — |
| CAP-599 | 599 | 1 | — | v0.22 — Discovery Completeness + Coverage Claims | DISCOVERY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming), [C-05](REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified) | — |
| CAP-600 | 600 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-601 | 601 | 1 | — | v0.22 — Discovery Completeness + Coverage Claims | DISCOVERY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming), [C-05](REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified) | — |
| CAP-602 | 602 | 2 | CAP-601 | v0.22 — 22.1 The problem | ALGORITHM | — | — | — |
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
| CAP-626 | 626 | 3 | CAP-625 | v0.22 — Invariant 1 | VALIDATION | — | — | — |
| CAP-627 | 627 | 3 | CAP-625 | v0.22 — Invariant 2 | VALIDATION | — | — | — |
| CAP-628 | 628 | 3 | CAP-625 | v0.22 — Invariant 3 | VALIDATION | — | — | — |
| CAP-629 | 629 | 3 | CAP-625 | v0.22 — Invariant 4 | VALIDATION | — | — | — |
| CAP-630 | 630 | 3 | CAP-625 | v0.22 — Invariant 5 | VALIDATION | — | — | — |
| CAP-631 | 631 | 3 | CAP-625 | v0.22 — Invariant 6 | VALIDATION | — | — | — |
| CAP-632 | 632 | 3 | CAP-625 | v0.22 — Invariant 7 | VALIDATION | — | — | — |
| CAP-633 | 633 | 3 | CAP-625 | v0.22 — Invariant 8 | VALIDATION | — | — | — |
| CAP-634 | 634 | 3 | CAP-625 | v0.22 — Invariant 9 | VALIDATION | — | — | — |
| CAP-635 | 635 | 3 | CAP-625 | v0.22 — Invariant 10 | VALIDATION | — | — | — |
| CAP-636 | 636 | 1 | — | v0.22 — 22.25 v0.22 architecture | ARCHITECTURE | — | — | — |
| CAP-637 | 637 | 1 | — | v0.22 — 22.26 The conceptual jump | CONCEPT | — | — | — |
| CAP-638 | 638 | 1 | — | v0.23 — Negative Evidence + Absence Reasoning | ALGORITHM | — | — | — |
| CAP-639 | 639 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-640 | 640 | 1 | — | v0.23 — Negative Evidence + Absence Reasoning | ALGORITHM | — | — | — |
| CAP-641 | 641 | 2 | CAP-640 | v0.23 — 23.1 The absence problem | ALGORITHM | — | — | — |
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
| CAP-664 | 664 | 3 | CAP-663 | v0.23 — Presence | ALGORITHM | — | — | — |
| CAP-665 | 665 | 3 | CAP-663 | v0.23 — Absence | ALGORITHM | — | — | — |
| CAP-666 | 666 | 3 | CAP-663 | v0.23 — Unknown | ALGORITHM | — | — | — |
| CAP-667 | 667 | 1 | — | v0.23 — 23.24 New invariants | VALIDATION | — | — | — |
| CAP-668 | 668 | 3 | CAP-667 | v0.23 — Invariant 1 | VALIDATION | — | — | — |
| CAP-669 | 669 | 3 | CAP-667 | v0.23 — Invariant 2 | VALIDATION | — | — | — |
| CAP-670 | 670 | 3 | CAP-667 | v0.23 — Invariant 3 | VALIDATION | — | — | — |
| CAP-671 | 671 | 3 | CAP-667 | v0.23 — Invariant 4 | VALIDATION | — | — | — |
| CAP-672 | 672 | 3 | CAP-667 | v0.23 — Invariant 5 | VALIDATION | — | — | — |
| CAP-673 | 673 | 3 | CAP-667 | v0.23 — Invariant 6 | VALIDATION | — | — | — |
| CAP-674 | 674 | 3 | CAP-667 | v0.23 — Invariant 7 | VALIDATION | — | — | — |
| CAP-675 | 675 | 3 | CAP-667 | v0.23 — Invariant 8 | VALIDATION | — | — | — |
| CAP-676 | 676 | 3 | CAP-667 | v0.23 — Invariant 9 | VALIDATION | — | — | — |
| CAP-677 | 677 | 3 | CAP-667 | v0.23 — Invariant 10 | VALIDATION | — | — | — |
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
| CAP-714 | 714 | 3 | CAP-713 | v0.24 — Invariant 1 | VALIDATION | — | — | — |
| CAP-715 | 715 | 3 | CAP-713 | v0.24 — Invariant 2 | VALIDATION | — | — | — |
| CAP-716 | 716 | 3 | CAP-713 | v0.24 — Invariant 3 | VALIDATION | — | — | — |
| CAP-717 | 717 | 3 | CAP-713 | v0.24 — Invariant 4 | VALIDATION | — | — | — |
| CAP-718 | 718 | 3 | CAP-713 | v0.24 — Invariant 5 | VALIDATION | — | — | — |
| CAP-719 | 719 | 3 | CAP-713 | v0.24 — Invariant 6 | VALIDATION | — | — | — |
| CAP-720 | 720 | 3 | CAP-713 | v0.24 — Invariant 7 | VALIDATION | — | — | — |
| CAP-721 | 721 | 3 | CAP-713 | v0.24 — Invariant 8 | VALIDATION | — | — | — |
| CAP-722 | 722 | 3 | CAP-713 | v0.24 — Invariant 9 | VALIDATION | — | — | — |
| CAP-723 | 723 | 3 | CAP-713 | v0.24 — Invariant 10 | VALIDATION | — | — | — |
| CAP-724 | 724 | 1 | — | v0.24 — 24.33 What v0.24 changes fundamentally | ALGORITHM | — | — | — |
| CAP-725 | 725 | 1 | — | v0.25 — Discovery Query Planner | DISCOVERY | — | — | — |
| CAP-726 | 726 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-727 | 727 | 1 | — | v0.25 — Discovery Query Planner | DISCOVERY | — | — | — |
| CAP-728 | 728 | 2 | CAP-727 | v0.25 — 25.1 Planner ≠ Search Engine | ALGORITHM | — | — | — |
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
| CAP-760 | 760 | 3 | CAP-759 | v0.25 — Planner invariants | VALIDATION | — | — | — |
| CAP-761 | 761 | 1 | — | v0.25 — 25.33 The resulting abstraction stack | ALGORITHM | — | — | — |
| CAP-762 | 762 | 1 | — | v0.26 — Search Tactic Runtime | ALGORITHM | — | — | — |
| CAP-763 | 763 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-764 | 764 | 1 | — | v0.26 — Search Tactic Runtime | ALGORITHM | — | — | — |
| CAP-765 | 765 | 2 | CAP-764 | v0.26 — 26.1 The architectural gap | ALGORITHM | — | — | — |
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
| CAP-785 | 785 | 3 | CAP-784 | v0.26 — Planning failures | ALGORITHM | — | — | — |
| CAP-786 | 786 | 3 | CAP-784 | v0.26 — Runtime failures | ALGORITHM | — | — | — |
| CAP-787 | 787 | 3 | CAP-784 | v0.26 — Strategy failures | ALGORITHM | — | — | — |
| CAP-788 | 788 | 3 | CAP-784 | v0.26 — Search failures | ALGORITHM | — | — | — |
| CAP-789 | 789 | 3 | CAP-784 | v0.26 — Recovery failures | ALGORITHM | — | — | — |
| CAP-790 | 790 | 1 | — | v0.26 — 26.21 Retry semantics | ALGORITHM | — | — | — |
| CAP-791 | 791 | 1 | — | v0.26 — 26.22 Cancellation | ALGORITHM | — | — | — |
| CAP-792 | 792 | 1 | — | v0.26 — 26.23 Shared Frontier interaction | ALGORITHM | — | — | — |
| CAP-793 | 793 | 1 | — | v0.26 — 26.24 v0.26 architecture | ARCHITECTURE | — | — | — |
| CAP-794 | 794 | 1 | — | v0.26 — 26.25 Accounting | ALGORITHM | — | — | — |
| CAP-795 | 795 | 1 | — | v0.26 — 26.26 The important safety invariant | VALIDATION | — | — | — |
| CAP-796 | 796 | 1 | — | v0.26 — 26.27 Resumability invariant | VALIDATION | — | — | — |
| CAP-797 | 797 | 1 | — | v0.26 — 26.28 New state model | ALGORITHM | — | — | — |
| CAP-798 | 798 | 1 | — | v0.26 — 26.29 v0.26 invariants | VALIDATION | — | — | — |
| CAP-799 | 799 | 3 | CAP-798 | v0.26 — I1 — Planning/execution separation | VALIDATION | — | — | — |
| CAP-800 | 800 | 3 | CAP-798 | v0.26 — I2 — Execution identity | VALIDATION | — | [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution) | — |
| CAP-801 | 801 | 3 | CAP-798 | v0.26 — I3 — Single scheduler authority | SCHEDULING | — | — | — |
| CAP-802 | 802 | 3 | CAP-798 | v0.26 — I4 — Bounded execution | VALIDATION | — | — | — |
| CAP-803 | 803 | 3 | CAP-798 | v0.26 — I5 — Resumability | VALIDATION | — | — | — |
| CAP-804 | 804 | 3 | CAP-798 | v0.26 — I6 — No silent cursor advancement | VALIDATION | — | — | — |
| CAP-805 | 805 | 3 | CAP-798 | v0.26 — I7 — Proposal boundary | VALIDATION | — | — | — |
| CAP-806 | 806 | 3 | CAP-798 | v0.26 — I8 — No authority escalation | VALIDATION | — | — | — |
| CAP-807 | 807 | 3 | CAP-798 | v0.26 — I9 — Exhaustion separation | VALIDATION | — | — | — |
| CAP-808 | 808 | 3 | CAP-798 | v0.26 — I10 — Failure ≠ absence | VALIDATION | — | — | — |
| CAP-809 | 809 | 3 | CAP-798 | v0.26 — I11 — Provenance | PROVENANCE | — | — | — |
| CAP-810 | 810 | 3 | CAP-798 | v0.26 — I12 — Versioned recovery | VALIDATION | — | — | — |
| CAP-811 | 811 | 1 | — | v0.26 — 26.30 What v0.26 actually gives us | CONCEPT | — | — | — |
| CAP-812 | 812 | 2 | CAP-811 | v0.26 — Next boundary: v0.27 | ROADMAP | — | — | — |
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
| CAP-824 | 824 | 3 | CAP-823 | v0.27 — Sitemap | ALGORITHM | — | — | — |
| CAP-825 | 825 | 3 | CAP-823 | v0.27 — API | ALGORITHM | — | — | — |
| CAP-826 | 826 | 3 | CAP-823 | v0.27 — Repository | ALGORITHM | — | — | — |
| CAP-827 | 827 | 3 | CAP-823 | v0.27 — Manifest | ALGORITHM | — | — | — |
| CAP-828 | 828 | 1 | — | v0.27 — 27.10 EnumerationEntry | ALGORITHM | — | — | — |
| CAP-829 | 829 | 1 | — | v0.27 — 27.11 Entry identity | ALGORITHM | — | [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution) | — |
| CAP-830 | 830 | 1 | — | v0.27 — 27.12 Enumeration cursor | ALGORITHM | — | — | — |
| CAP-831 | 831 | 3 | CAP-830 | v0.27 — Offset | ALGORITHM | — | — | — |
| CAP-832 | 832 | 3 | CAP-830 | v0.27 — Page | ALGORITHM | — | — | — |
| CAP-833 | 833 | 3 | CAP-830 | v0.27 — Token | ALGORITHM | — | — | — |
| CAP-834 | 834 | 3 | CAP-830 | v0.27 — Locator | ALGORITHM | — | — | — |
| CAP-835 | 835 | 3 | CAP-830 | v0.27 — Composite | ALGORITHM | — | — | — |
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
| CAP-854 | 854 | 3 | CAP-853 | v0.27 — E1 — Enumeration is scoped | SCOPE | — | — | — |
| CAP-855 | 855 | 3 | CAP-853 | v0.27 — E2 — Enumeration termination is not global completeness | ALGORITHM | — | [C-05](REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified), [C-09](REVIEW-NOTES.md#c-09--two-termination-taxonomies) | — |
| CAP-856 | 856 | 3 | CAP-853 | v0.27 — E3 — Budget exhaustion is not enumeration exhaustion | ALGORITHM | — | — | — |
| CAP-857 | 857 | 3 | CAP-853 | v0.27 — E4 — Cursor progress must be durable | VALIDATION | — | — | — |
| CAP-858 | 858 | 3 | CAP-853 | v0.27 — E5 — Enumeration entries are not candidates | CANDIDATE | — | — | — |
| CAP-859 | 859 | 3 | CAP-853 | v0.27 — E6 — Cardinality is evidence | VALIDATION | — | — | — |
| CAP-860 | 860 | 3 | CAP-853 | v0.27 — E7 — Historical snapshots remain immutable | VALIDATION | — | — | — |
| CAP-861 | 861 | 3 | CAP-853 | v0.27 — E8 — Incomplete enumeration cannot establish absence | ALGORITHM | — | — | — |
| CAP-862 | 862 | 3 | CAP-853 | v0.27 — E9 — Unstable enumeration weakens completeness | ALGORITHM | — | [C-05](REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified) | — |
| CAP-863 | 863 | 3 | CAP-853 | v0.27 — E10 — Enumerator has no acquisition authority | ACQUISITION | — | — | — |
| CAP-864 | 864 | 3 | CAP-853 | v0.27 — E11 — Enumerator cannot directly mutate the ResourceGraph | VALIDATION | — | — | — |
| CAP-865 | 865 | 3 | CAP-853 | v0.27 — E12 — Termination evidence is provenance-bearing | PROVENANCE | — | [C-09](REVIEW-NOTES.md#c-09--two-termination-taxonomies) | — |
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
| CAP-896 | 896 | 3 | CAP-895 | v0.28 — Candidate deduplication | CANDIDATE | — | — | — |
| CAP-897 | 897 | 3 | CAP-895 | v0.28 — Search-space deduplication | ARCHITECTURE | — | — | — |
| CAP-898 | 898 | 1 | — | v0.28 — 28.26 Adaptive strategy interaction | ALGORITHM | — | — | — |
| CAP-899 | 899 | 1 | — | v0.28 — 28.27 Example | ARCHITECTURE | — | — | — |
| CAP-900 | 900 | 1 | — | v0.28 — 28.28 Reconciliation algorithm | ALGORITHM | — | — | — |
| CAP-901 | 901 | 1 | — | v0.28 — 28.29 Reconciliation must be monotonic | ARCHITECTURE | — | — | — |
| CAP-902 | 902 | 1 | — | v0.28 — 28.30 Reconciliation does not delete evidence | ARCHITECTURE | — | — | — |
| CAP-903 | 903 | 1 | — | v0.28 — 28.31 Failure taxonomy | VALIDATION | — | — | — |
| CAP-904 | 904 | 1 | — | v0.28 — 28.32 Core invariants | VALIDATION | — | — | — |
| CAP-905 | 905 | 3 | CAP-904 | v0.28 — R1 — Candidate convergence | CANDIDATE | — | — | — |
| CAP-906 | 906 | 3 | CAP-904 | v0.28 — R2 — Provenance preservation | PROVENANCE | — | — | — |
| CAP-907 | 907 | 3 | CAP-904 | v0.28 — R3 — Artifact convergence | VALIDATION | — | [C-07](REVIEW-NOTES.md#c-07--resource--artifact-model-revised) | — |
| CAP-908 | 908 | 3 | CAP-904 | v0.28 — R4 — Observation preservation | OBSERVATION | — | — | — |
| CAP-909 | 909 | 3 | CAP-904 | v0.28 — R5 — Overlap is not duplication | VALIDATION | — | — | — |
| CAP-910 | 910 | 3 | CAP-904 | v0.28 — R6 — Equivalent work may be suppressed | VALIDATION | — | — | — |
| CAP-911 | 911 | 3 | CAP-904 | v0.28 — R7 — Suppression preserves provenance | PROVENANCE | — | — | — |
| CAP-912 | 912 | 3 | CAP-904 | v0.28 — R8 — Unknown overlap is not disjointness | VALIDATION | — | — | — |
| CAP-913 | 913 | 3 | CAP-904 | v0.28 — R9 — Coverage is union-aware | VALIDATION | — | [C-05](REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified) | — |
| CAP-914 | 914 | 3 | CAP-904 | v0.28 — R10 — Candidate count does not establish coverage | CANDIDATE | — | [C-05](REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified) | — |
| CAP-915 | 915 | 3 | CAP-904 | v0.28 — R11 — Evidence independence must be justified | VALIDATION | — | — | — |
| CAP-916 | 916 | 3 | CAP-904 | v0.28 — R12 — Historical reconciliation is immutable | VALIDATION | — | — | — |
| CAP-917 | 917 | 1 | — | v0.28 — 28.33 v0.28 architecture | ARCHITECTURE | — | — | — |
| CAP-918 | 918 | 1 | — | v0.28 — 28.34 The deeper architectural result | ARCHITECTURE | — | — | — |
| CAP-919 | 919 | 2 | CAP-918 | v0.28 — Next boundary — v0.29 | ROADMAP | — | — | — |
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
| CAP-955 | 955 | 3 | CAP-954 | v0.29 — P1 — Discovery does not create authority | VALIDATION | — | — | — |
| CAP-956 | 956 | 3 | CAP-954 | v0.29 — P2 — Partition proposal is not partition | VALIDATION | — | — | — |
| CAP-957 | 957 | 3 | CAP-954 | v0.29 — P3 — Every admitted partition belongs to the domain | VALIDATION | — | — | — |
| CAP-958 | 958 | 3 | CAP-954 | v0.29 — P4 — Expansion is budgeted | VALIDATION | — | — | — |
| CAP-959 | 959 | 3 | CAP-954 | v0.29 — P5 — Expansion is depth-bounded | VALIDATION | — | — | — |
| CAP-960 | 960 | 3 | CAP-954 | v0.29 — P6 — Duplicate partitions converge | VALIDATION | — | — | — |
| CAP-961 | 961 | 3 | CAP-954 | v0.29 — P7 — Overlap is preserved | VALIDATION | — | — | — |
| CAP-962 | 962 | 3 | CAP-954 | v0.29 — P8 — Evidence is preserved | VALIDATION | — | — | — |
| CAP-963 | 963 | 3 | CAP-954 | v0.29 — P9 — Partition existence does not schedule execution | SCHEDULING | — | — | — |
| CAP-964 | 964 | 3 | CAP-954 | v0.29 — P10 — Expansion cannot override policy | SECURITY | — | [C-11](REVIEW-NOTES.md#c-11--same-origin-default-versus-cross-origin-capability) | — |
| CAP-965 | 965 | 3 | CAP-954 | v0.29 — P11 — Search-space versions are immutable | VALIDATION | — | — | — |
| CAP-966 | 966 | 3 | CAP-954 | v0.29 — P12 — Expansion does not invalidate historical claims automatically | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-967 | 967 | 3 | CAP-954 | v0.29 — P13 — Cycles are legal | VALIDATION | — | — | — |
| CAP-968 | 968 | 3 | CAP-954 | v0.29 — P14 — Unknown remains valid | VALIDATION | — | — | — |
| CAP-969 | 969 | 1 | — | v0.29 — 29.34 The system after v0.29 | ARCHITECTURE | — | — | — |
| CAP-970 | 970 | 1 | — | v0.29 — 29.35 Blind-scan interpretation | DVB_ANALOGY | — | — | — |
| CAP-971 | 971 | 1 | — | v0.29 takeaway | ARCHITECTURE | — | — | — |
| CAP-972 | 972 | 1 | — | v0.30 — Unified Frontier Arbitration | SCHEDULING | — | — | — |
| CAP-973 | 973 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-974 | 974 | 1 | — | v0.30 — Conclusion — Generic Discovery Engine | DISCOVERY | — | — | — |
| CAP-975 | 975 | 2 | CAP-974 | v0.30 — The final conceptual separation | SCHEDULING | — | — | — |
| CAP-976 | 976 | 1 | — | v0.30 — The fundamental invariant | VALIDATION | — | — | — |
| CAP-977 | 977 | 1 | — | v0.30 — What the DVB analogy actually contributed | DVB_ANALOGY | — | — | — |
| CAP-978 | 978 | 1 | — | v0.30 — The most important safety boundary | SCHEDULING | — | — | — |
| CAP-979 | 979 | 1 | — | v0.30 — Final architecture | ARCHITECTURE | — | — | — |
| CAP-980 | 980 | 1 | — | v0.30 — What the userscript should and should not become | LIMITATIONS | — | — | explicit override; the source presents this as the delivered prototype; no implementation file in this repository verifies it |
| CAP-981 | 981 | 1 | — | v0.30 — Final principles | CONCEPT | — | — | — |
| CAP-982 | 982 | — | — | — | SCHEDULING | — | — | lead-in of the following section |
| CAP-983 | 983 | 1 | — | v0.30 — Unified Frontier Arbitration | SCHEDULING | — | — | — |
| CAP-984 | 984 | 2 | CAP-983 | v0.30 — 30.1 The new architecture | ARCHITECTURE | — | — | — |
| CAP-985 | 985 | 1 | — | v0.30 — 30.2 WorkClass | SCHEDULING | — | — | — |
| CAP-986 | 986 | 1 | — | v0.30 — 30.3 WorkClassPolicy | SCHEDULING | — | [C-11](REVIEW-NOTES.md#c-11--same-origin-default-versus-cross-origin-capability) | — |
| CAP-987 | 987 | 1 | — | v0.30 — 30.4 ArbitrationDecision | SCHEDULING | — | — | — |
| CAP-988 | 988 | 1 | — | v0.30 — 30.5 Hard constraints vs soft priorities | SCHEDULING | — | — | — |
| CAP-989 | 989 | 3 | CAP-988 | v0.30 — Hard constraints | SCHEDULING | — | — | — |
| CAP-990 | 990 | 3 | CAP-988 | v0.30 — Soft priorities | SCHEDULING | — | — | — |
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
| CAP-1015 | 1015 | 2 | CAP-1014 | v0.31 — 31.1 Resource dimensions | ARCHITECTURE | — | — | — |
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
| CAP-1043 | 1043 | 2 | CAP-1042 | v0.32 — 32.1 The crash problem | ARCHITECTURE | — | — | — |
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
| CAP-1081 | 1081 | 2 | CAP-1080 | v0.33 — 33.1 Worker identity | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming), [C-04](REVIEW-NOTES.md#c-04--resource-identity-canonical-url-versus-identity-resolution) | — |
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
| CAP-1110 | 1110 | 1 | — | v0.33 — 33.30 What the browser prototype can guarantee | LIMITATIONS | — | — | explicit override; the source presents this as the delivered prototype; no implementation file in this repository verifies it |
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
| CAP-1126 | 1126 | 3 | CAP-1125 | v0.34 — Claim conflict | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-1127 | 1127 | 3 | CAP-1125 | v0.34 — Candidate conflict | CANDIDATE | — | — | — |
| CAP-1128 | 1128 | 3 | CAP-1125 | v0.34 — Classification conflict | ARCHITECTURE | — | — | — |
| CAP-1129 | 1129 | 3 | CAP-1125 | v0.34 — Coverage conflict | ARCHITECTURE | — | [C-05](REVIEW-NOTES.md#c-05--coverage-preferred-metric-later-heavily-qualified) | — |
| CAP-1130 | 1130 | 3 | CAP-1125 | v0.34 — Budget conflict | ARCHITECTURE | — | — | — |
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
| CAP-1150 | 1150 | 3 | CAP-1149 | v0.34 — Consistency | ARCHITECTURE | — | — | — |
| CAP-1151 | 1151 | 3 | CAP-1149 | v0.34 — Fencing | CONCURRENCY | — | [C-03](REVIEW-NOTES.md#c-03--candidate-claiming-single-thread-assumption-versus-distributed-claiming) | — |
| CAP-1152 | 1152 | 3 | CAP-1149 | v0.34 — Conflict | ARCHITECTURE | — | — | — |
| CAP-1153 | 1153 | 3 | CAP-1149 | v0.34 — Provenance | PROVENANCE | — | — | — |
| CAP-1154 | 1154 | 3 | CAP-1149 | v0.34 — Recovery | ARCHITECTURE | — | — | — |
| CAP-1155 | 1155 | 3 | CAP-1149 | v0.34 — Scalability | ARCHITECTURE | — | — | — |
| CAP-1156 | 1156 | 1 | — | v0.34 — 34.27 The Unified State Model | ARCHITECTURE | — | — | — |
| CAP-1157 | 1157 | 1 | — | v0.34 — 34.28 What v0.34 Actually Proves | VALIDATION | — | — | explicit override |
| CAP-1158 | 1158 | 3 | CAP-1157 | v0.34 — PROVED by the architecture | VALIDATION | — | — | explicit override |
| CAP-1159 | 1159 | 3 | CAP-1157 | v0.34 — ARGUMENT | VALIDATION | — | — | explicit override |
| CAP-1160 | 1160 | 3 | CAP-1157 | v0.34 — OPEN | VALIDATION | — | — | explicit override |
| CAP-1161 | 1161 | 1 | — | v0.34 — 34.29 Prototype Boundary | LIMITATIONS | — | — | explicit override; the source presents this as the delivered prototype; no implementation file in this repository verifies it |
| CAP-1162 | 1162 | 1 | — | v0.34 — 34.30 v0.34 → v0.35 | ROADMAP | — | — | — |
| CAP-1163 | 1163 | — | — | — | UNKNOWN | — | — | conversation continuation marker; not carried into the tree (retained in archive/) |
| CAP-1164 | 1164 | 1 | — | v0.34 — Conclusion — Generic Discovery Engine | DISCOVERY | — | — | — |
| CAP-1165 | 1165 | 2 | CAP-1164 | v0.34 — The decisive conceptual shift | CONCEPT | — | — | — |
| CAP-1166 | 1166 | 3 | CAP-1165 | v0.34 — DVB blind scan | DVB_ANALOGY | — | — | — |
| CAP-1167 | 1167 | 3 | CAP-1165 | v0.34 — Generic discovery | DISCOVERY | — | — | — |
| CAP-1168 | 1168 | 1 | — | v0.34 — The major architectural invariants | VALIDATION | — | — | — |
| CAP-1169 | 1169 | 1 | — | v0.34 — Final architecture by responsibility | ARCHITECTURE | — | — | — |
| CAP-1170 | 1170 | 1 | — | v0.34 — What the prototype actually becomes | CONCEPT | — | — | — |
| CAP-1171 | 1171 | 1 | — | v0.34 — Final formulation | CONCEPT | — | — | — |

## Anchors

Every source section is identified deterministically. `Heading path` is the complete structural path from the document root; the hashes are the first 16 hexadecimal characters of `sha256` over the normalized text (LF endings, no trailing whitespace, no repeated blank lines — wording, code, tables, diagrams and list order preserved).

| ID | Heading path | Heading hash | Content hash |
| --- | --- | --- | --- |
| USP-001 | Userscript Discovery Prototype.md > lead-in | `e3b0c44298fc1c14` | `0f5ece5efa469a24` |
| USP-002 | Userscript Discovery Prototype.md > lead-in | `e3b0c44298fc1c14` | `cfa5771c837cac60` |
| USP-003 | Userscript Discovery Prototype.md > Generic pseudocode | `6d107753608781c2` | `f4eadc03184a4c21` |
| USP-004 | Userscript Discovery Prototype.md > Making it genuinely generic | `36e2c9a9132634b4` | `df7adf7cf87e980d` |
| USP-005 | Userscript Discovery Prototype.md > lead-in | `e3b0c44298fc1c14` | `31fbef162594de01` |
| USP-006 | Userscript Discovery Prototype.md > lead-in | `e3b0c44298fc1c14` | `fbf2b3ce3b315f08` |
| USP-007 | Userscript Discovery Prototype.md > 1. Separate the layers | `16bc1fc0c02be562` | `a4fa5b32d489428c` |
| USP-008 | Userscript Discovery Prototype.md > 2. Candidate generation | `a0da1daaea91d111` | `589a901912676b46` |
| USP-009 | Userscript Discovery Prototype.md > 3. Detection should precede expensive decoding | `ace88a026cacd0a8` | `1464027ac733f2d9` |
| USP-010 | Userscript Discovery Prototype.md > 4. Lock is not discovery | `97272c479b9bc430` | `dd2ea55b94bb4646` |
| USP-011 | Userscript Discovery Prototype.md > 5. Use DVB metadata to escape blind mode | `813d6961aa5e79ef` | `f0f4aa9c4aa0a992` |
| USP-012 | Userscript Discovery Prototype.md > 6. Deduplication | `8aeb08e367edc6dc` | `164747cd49218cb5` |
| USP-013 | Userscript Discovery Prototype.md > 7. Generic algorithm | `882303bd2f00a7a9` | `cd4ed25c96c87966` |
| USP-014 | Userscript Discovery Prototype.md > 7. Generic algorithm > The key insight | `d4f7889c45cfb475` | `2db0fab03abcbb7e` |
| USP-015 | Userscript Discovery Prototype.md > lead-in | `e3b0c44298fc1c14` | `31fbef162594de01` |
| USP-016 | Userscript Discovery Prototype.md > lead-in | `e3b0c44298fc1c14` | `44e45b94c6ad7bd9` |
| USP-017 | Userscript Discovery Prototype.md > 8. Model scanning as a search problem | `7bd639fdf9c17b83` | `15e565846fca686a` |
| USP-018 | Userscript Discovery Prototype.md > 9. Coarse-to-fine search | `687d70289f4e5fce` | `b9d65b962936ef8d` |
| USP-019 | Userscript Discovery Prototype.md > 10. Confidence rather than binary decisions | `2c4c71cca7721a01` | `81fb77125b0f065f` |
| USP-020 | Userscript Discovery Prototype.md > 11. Don't immediately discard failed candidates | `3ccea48f58cf3f64` | `f87101fc9df60f8d` |
| USP-021 | Userscript Discovery Prototype.md > 12. Adaptive retry | `d1ef653f57f7502e` | `60fb13dc4c2f465a` |
| USP-022 | Userscript Discovery Prototype.md > 13. Scheduling becomes important | `d94bc65b7792738b` | `fc64b7e3debdbe6a` |
| USP-023 | Userscript Discovery Prototype.md > 14. Discovery database | `23f59e8acbe5240c` | `b9028a3224086a48` |
| USP-024 | Userscript Discovery Prototype.md > 15. The generic discovery abstraction | `c6ab4d6bfff97acd` | `bae08a575c0ae298` |
| USP-025 | Userscript Discovery Prototype.md > lead-in | `e3b0c44298fc1c14` | `31fbef162594de01` |
| USP-026 | Userscript Discovery Prototype.md > lead-in | `e3b0c44298fc1c14` | `7782969047bf8563` |
| USP-027 | Userscript Discovery Prototype.md > 16. Discovery should have evidence levels | `5db28552cbfdcc54` | `e59587e8afc36000` |
| USP-028 | Userscript Discovery Prototype.md > 17. Use observations to update the search space | `e1b5b717b55b28ac` | `17bbb853c826dcac` |
| USP-029 | Userscript Discovery Prototype.md > 18. Termination | `9c487f1a6f14edc0` | `8f9148bb87c9733b` |
| USP-030 | Userscript Discovery Prototype.md > 18. Termination > Exhaustive scan | `6b5ae3125b3ce271` | `d7246e142b89bc02` |
| USP-031 | Userscript Discovery Prototype.md > 18. Termination > Confidence-based scan | `2d2ab6491b2e05b4` | `ca9689166378eb48` |
| USP-032 | Userscript Discovery Prototype.md > 18. Termination > Time-bounded scan | `cca7772f3ae9a933` | `1d085e928b05ccf6` |
| USP-033 | Userscript Discovery Prototype.md > 18. Termination > Hybrid | `6c67dc13f83949fe` | `3d96b12f6de24a0d` |
| USP-034 | Userscript Discovery Prototype.md > 19. Coverage is a better metric than elapsed time | `c6f250199f4e78fd` | `73aa9769f26b3a7a` |
| USP-035 | Userscript Discovery Prototype.md > 20. Cache knowledge between scans | `c7d3599ab1085f2b` | `33ee106bf19eab32` |
| USP-036 | Userscript Discovery Prototype.md > 21. Handle disappearing multiplexes | `55d1a81ed28cd4df` | `67a5415e69ace28b` |
| USP-037 | Userscript Discovery Prototype.md > 22. The complete conceptual algorithm | `b5dc87267ee95973` | `9e037410823c0319` |
| USP-038 | Userscript Discovery Prototype.md > 22. The complete conceptual algorithm > 23. A useful formal name | `7a9b66accae9a516` | `6a53064e48507810` |
| USP-039 | Userscript Discovery Prototype.md > lead-in | `e3b0c44298fc1c14` | `31fbef162594de01` |
| USP-040 | Userscript Discovery Prototype.md > lead-in | `e3b0c44298fc1c14` | `5985ea4bb456fd4a` |
| USP-041 | Userscript Discovery Prototype.md > 24. Two-dimensional discovery | `36c5f11e0b2fd6e3` | `c3e4cfd1b7766f36` |
| USP-042 | Userscript Discovery Prototype.md > 25. Candidate lifecycle | `da1ec9310cd7bf11` | `febc51987edde80e` |
| USP-043 | Userscript Discovery Prototype.md > 26. Discovery becomes a graph | `b4e2494907724c43` | `d973c1fdbf33119f` |
| USP-044 | Userscript Discovery Prototype.md > 27. This helps with incremental scanning | `8049633b0c22e2d8` | `d134a00a11e4898f` |
| USP-045 | Userscript Discovery Prototype.md > 28. Parameter provenance | `5339f69cd64f122b` | `a29f4e771688467f` |
| USP-046 | Userscript Discovery Prototype.md > 29. The scanner should produce an explanation | `c30c34bfa9c3cd60` | `f44b0854913a3fe2` |
| USP-047 | Userscript Discovery Prototype.md > 30. The final abstraction | `ba350df48edd1c0c` | `1ed30ea5c3b9565a` |
| USP-048 | Userscript Discovery Prototype.md > lead-in | `e3b0c44298fc1c14` | `31fbef162594de01` |
| USP-049 | Userscript Discovery Prototype.md > lead-in | `e3b0c44298fc1c14` | `dfae4a056b49426d` |
| USP-050 | Userscript Discovery Prototype.md > 31. Define the core objects | `ca352d4c553b8289` | `5a144ebcd8aaeb4a` |
| USP-051 | Userscript Discovery Prototype.md > 31. Define the core objects > Candidate | `b2452d1eba32254a` | `b3f9638030924cbc` |
| USP-052 | Userscript Discovery Prototype.md > 31. Define the core objects > Observation | `d239e9cf6a51335b` | `2cbc40a3f6277e73` |
| USP-053 | Userscript Discovery Prototype.md > 31. Define the core objects > LockResult | `5406733bf54e6323` | `4b05c50c2de599f6` |
| USP-054 | Userscript Discovery Prototype.md > 31. Define the core objects > Discovery | `80fc402133201fbe` | `73785403ffb3b656` |
| USP-055 | Userscript Discovery Prototype.md > 32. Use capability-driven adapters | `1d007bf27474be1e` | `99f21f0a24161a3d` |
| USP-056 | Userscript Discovery Prototype.md > 33. Discovery strategies should also be pluggable | `6a89256a93a754f5` | `9e2209eaae424175` |
| USP-057 | Userscript Discovery Prototype.md > 34. Don't confuse candidate identity with reception identity | `71412d74043ce9b3` | `c30824315a247171` |
| USP-058 | Userscript Discovery Prototype.md > 35. Make deduplication hierarchical | `d7fc480221ef9d09` | `fb355ecaa0d2ce48` |
| USP-059 | Userscript Discovery Prototype.md > 36. Treat metadata as a candidate generator | `825591401d0b3858` | `622fd5cc2f600d12` |
| USP-060 | Userscript Discovery Prototype.md > 37. Candidate provenance creates a discovery tree | `1a5064b2b7b7e153` | `e3afcf1d9e8906c4` |
| USP-061 | Userscript Discovery Prototype.md > 38. Avoid infinite candidate generation | `a1f16c717772a94d` | `36e99512356e4ce0` |
| USP-062 | Userscript Discovery Prototype.md > 39. A practical scheduler | `4b78707fbc13f4aa` | `131dd20fa507a26d` |
| USP-063 | Userscript Discovery Prototype.md > 40. The engine can now become event-driven | `afa16309ae8e3109` | `16bde40e79af3cbc` |
| USP-064 | Userscript Discovery Prototype.md > 41. The resulting architecture | `e61fd1721c7afb34` | `64b79866d9b882ec` |
| USP-065 | Userscript Discovery Prototype.md > lead-in | `e3b0c44298fc1c14` | `7d75f9de801e99e3` |
| USP-066 | Userscript Discovery Prototype.md > lead-in | `e3b0c44298fc1c14` | `a7c81f0b6941afa6` |
| USP-067 | Userscript Discovery Prototype.md > lead-in | `e3b0c44298fc1c14` | `87c7a173ff39f6a5` |
| USP-068 | Userscript Discovery Prototype.md > The DVB analogy | `b1299dbf7aee6f3b` | `b905901136b28b15` |
| USP-069 | Userscript Discovery Prototype.md > lead-in | `e3b0c44298fc1c14` | `41585f6f0d95ad96` |
| USP-070 | Userscript Discovery Prototype.md > lead-in | `e3b0c44298fc1c14` | `ba67c87a81bede6c` |
| USP-071 | Userscript Discovery Prototype.md > What changed — 1. Concurrent claiming is now explicit | `ded4a05516a2d4ae` | `c20b8401739bc075` |
| USP-072 | Userscript Discovery Prototype.md > What changed — 2. HTML is no longer special | `49faf02b9b55f0a3` | `fdfebd466ed47b10` |
| USP-073 | Userscript Discovery Prototype.md > What changed — 3. The actual scope is now explicit | `253672b1b8028a3d` | `73ac05b1d1b7a29d` |
| CAP-001 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `fda9c8226a9d1420` |
| CAP-002 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `38bd2c1028ee1540` |
| CAP-003 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `0f8cb71d84462ca1` |
| CAP-004 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `320a70f7dbbf1ee1` |
| CAP-005 | Continue Architecture Planning.md > v0.3 > What changed from v0.2.0 | `a3e47d7ee19d3a0a` | `0930c87165baecb4` |
| CAP-006 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `31fbef162594de01` |
| CAP-007 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `417364d62cc9c5ce` |
| CAP-008 | Continue Architecture Planning.md > The biggest v0.4 improvement | `6998ab3c6da5ec2f` | `2d7ad3694f0f5462` |
| CAP-009 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `538d5ded86aa91f8` |
| CAP-010 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `c54a391f97ac08eb` |
| CAP-011 | Continue Architecture Planning.md > v0.4 > Notable v0.4.0 behavior | `e34b5dad0a3995b7` | `8468be2533772488` |
| CAP-012 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `31fbef162594de01` |
| CAP-013 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `42dea67f1f79898d` |
| CAP-014 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `53e22da5c61b6673` |
| CAP-015 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `31fbef162594de01` |
| CAP-016 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `32c295ca03b64b2b` |
| CAP-017 | Continue Architecture Planning.md > v0.4 > What changed from v0.3.0 | `e8ccf10b83c6b8fe` | `36b75485646a7fe8` |
| CAP-018 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `31fbef162594de01` |
| CAP-019 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `9623458c4668005b` |
| CAP-020 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `31fbef162594de01` |
| CAP-021 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `6d3ec3687db0ddc5` |
| CAP-022 | Continue Architecture Planning.md > v0.5 > v0.5 architecture | `50b7be5a6b4042cd` | `d41eac692b7361db` |
| CAP-023 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `31fbef162594de01` |
| CAP-024 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `6dc15dc65bcdd936` |
| CAP-025 | Continue Architecture Planning.md > v0.5 > What v0.6 changes architecturally | `2f2907a8f1c3f7f2` | `c4fc9f1b96ec3f6a` |
| CAP-026 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `31fbef162594de01` |
| CAP-027 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `dcf7b8a76ac0e6ae` |
| CAP-028 | Continue Architecture Planning.md > v0.5 > What v0.5.0 changes architecturally | `ef78757d20df1c2b` | `d00d8b794dbb2c62` |
| CAP-029 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `31fbef162594de01` |
| CAP-030 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `a24d2ea817340faa` |
| CAP-031 | Continue Architecture Planning.md > v0.6 > v0.6.0's main architectural additions | `4527e4283e625212` | `a159c0f7ab5f8318` |
| CAP-032 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `31fbef162594de01` |
| CAP-033 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `83d727c28876b42a` |
| CAP-034 | Continue Architecture Planning.md > v0.6 > What changed in v0.6 | `4e9fd1a787eb194d` | `e290ba4693f09df4` |
| CAP-035 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `31fbef162594de01` |
| CAP-036 | Continue Architecture Planning.md > v0.7 > v0.7.0 — Discovery Graph + Acquisition Planner | `cc055988fa9433c6` | `c4eca9a6d10aae02` |
| CAP-037 | Continue Architecture Planning.md > v0.7 > v0.7.0 — Discovery Graph + Acquisition Planner > v0.7 objectives | `21015707caae73fd` | `365be0586710c8ad` |
| CAP-038 | Continue Architecture Planning.md > v0.7 > v0.7.0 — Discovery Graph + Acquisition Planner > Core contract | `5a4670fe47184781` | `c6715dd060f88dd8` |
| CAP-039 | Continue Architecture Planning.md > v0.7 > v0.7.0 — Discovery Graph + Acquisition Planner > Important v0.7 distinction | `fe68861822b06d0d` | `09fc867910032065` |
| CAP-040 | Continue Architecture Planning.md > v0.7 > v0.7 state machine | `07460837804bc887` | `dcc8ae238478ca0a` |
| CAP-041 | Continue Architecture Planning.md > v0.7 > The deeper abstraction | `c3e5fc9deda56995` | `537f4bbcbb422db3` |
| CAP-042 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `31fbef162594de01` |
| CAP-043 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `a1fbf385211aad7a` |
| CAP-044 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `cb3f91d54eee30e5` |
| CAP-045 | Continue Architecture Planning.md > v0.7 > What v0.7.1 actually changes | `179ed76c206894a8` | `a845f497e648c10f` |
| CAP-046 | Continue Architecture Planning.md > v0.7 > What v0.7.1 actually changes > Before | `9bb725005055412c` | `9d8f9c0aef7ca07e` |
| CAP-047 | Continue Architecture Planning.md > v0.7 > What v0.7.1 actually changes > Now | `fe18013d93d22f4f` | `dbb6b72f15ffdf1d` |
| CAP-048 | Continue Architecture Planning.md > v0.7 > 2. The ledger becomes the scan's causal trace | `6b47df19cd9d7f13` | `39540c168c1513bd` |
| CAP-049 | Continue Architecture Planning.md > v0.7 > 3. PerformanceObserver correction | `9ed2e1d36bdba91c` | `b7bca59bb479edc2` |
| CAP-050 | Continue Architecture Planning.md > v0.7 > 4. Candidate state machine | `716639e48944812f` | `37ae6b10636fc8c0` |
| CAP-051 | Continue Architecture Planning.md > v0.7 > 5. The ledger is not merely logging | `6236a7eb287e4843` | `1699925e613b4387` |
| CAP-052 | Continue Architecture Planning.md > v0.7 > 6. One remaining architectural limitation | `43fb4ede78abd311` | `8cb1859d92d09a21` |
| CAP-053 | Continue Architecture Planning.md > v0.7 > 7. Architecture after v0.7.1 | `9da8370aecab51a7` | `22f43250c3caeefb` |
| CAP-054 | Continue Architecture Planning.md > v0.7 > 7. Architecture after v0.7.1 > Next boundary: v0.8 | `31eaa6f32daf5c51` | `b49102570603a1c1` |
| CAP-055 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `31fbef162594de01` |
| CAP-056 | Continue Architecture Planning.md > v0.8 > v0.8 — Capability-Aware Acquisition Runtime | `1806284940e3464a` | `64e756af16ef1748` |
| CAP-057 | Continue Architecture Planning.md > v0.8 > v0.8 — Capability-Aware Acquisition Runtime > 1. The three graphs | `17b87e731a05834e` | `4408b6f0b1187cd0` |
| CAP-058 | Continue Architecture Planning.md > v0.8 > v0.8 — Capability-Aware Acquisition Runtime > 1. The three graphs > Discovery graph | `5fae96f70e8f8688` | `bc7efd828b4e5972` |
| CAP-059 | Continue Architecture Planning.md > v0.8 > v0.8 — Capability-Aware Acquisition Runtime > 1. The three graphs > Acquisition graph | `bf9e270f56dba9a5` | `0cd1adb2cdaf32f7` |
| CAP-060 | Continue Architecture Planning.md > v0.8 > v0.8 — Capability-Aware Acquisition Runtime > 1. The three graphs > Evidence graph | `0eb3df32a017aeca` | `5f2f8a1c7bce1a4b` |
| CAP-061 | Continue Architecture Planning.md > v0.8 > 2. Capability is now a first-class object | `dc03adc1d414b788` | `791b2a6170461131` |
| CAP-062 | Continue Architecture Planning.md > v0.8 > 3. Capability lattice | `312d21efc5b8e23b` | `68bd9131da83c2c0` |
| CAP-063 | Continue Architecture Planning.md > v0.8 > 4. Capability contract | `f6856c8bc2750639` | `df9abb557c4d6b34` |
| CAP-064 | Continue Architecture Planning.md > v0.8 > 5. Candidate requirements | `51268a980b781744` | `7253a97b160c888b` |
| CAP-065 | Continue Architecture Planning.md > v0.8 > 6. Acquisition planning becomes capability resolution | `4fd522b7066db2b6` | `d146a23f8953dcf8` |
| CAP-066 | Continue Architecture Planning.md > v0.8 > 7. Why this matters for generic discovery | `f952387aa2945feb` | `1d84f1e2c14c7638` |
| CAP-067 | Continue Architecture Planning.md > v0.8 > 8. AcquisitionPlan v0.8 | `ae167954a5124ec4` | `fe163ad63fbdde95` |
| CAP-068 | Continue Architecture Planning.md > v0.8 > 9. Capability provenance | `ee752e82c6aa9a3e` | `f5c0c6f108f833f1` |
| CAP-069 | Continue Architecture Planning.md > v0.8 > 10. The four-level authorization model | `426fdc7c0a9dfe2c` | `1c5d4a14fb57769d` |
| CAP-070 | Continue Architecture Planning.md > v0.8 > 11. New graph model | `640f207acbfaef73` | `188a4a341fb4c49f` |
| CAP-071 | Continue Architecture Planning.md > v0.8 > 12. v0.8 ledger | `4fc2f5fc20edcb2a` | `61bb873f1cd1107c` |
| CAP-072 | Continue Architecture Planning.md > v0.8 > 13. Important architectural consequence | `efb7776e82aa9ce1` | `5db9026c3fd5ccad` |
| CAP-073 | Continue Architecture Planning.md > v0.8 > 14. v0.8 scope boundary | `1d9833bd9b67cf86` | `b682850423f8f792` |
| CAP-074 | Continue Architecture Planning.md > v0.8 > 14. v0.8 scope boundary > Implement | `c7a2b3bc051ae2ef` | `91e986e0a1b67a4e` |
| CAP-075 | Continue Architecture Planning.md > v0.8 > 14. v0.8 scope boundary > Represent but deny | `f13f548d15433230` | `eda4cfdd2ff0e364` |
| CAP-076 | Continue Architecture Planning.md > v0.8 > 15. Updated system invariant | `60cd4f7c77970998` | `6f3e8e9fc30ccb38` |
| CAP-077 | Continue Architecture Planning.md > v0.8 > 16. The DVB analogy is now cleaner | `56e612e3a0c83b19` | `949bad2a7c21b50b` |
| CAP-078 | Continue Architecture Planning.md > v0.8 > 17. v0.8 → v0.9 | `2d63a7796ec91185` | `276ab0ae5e02b6c8` |
| CAP-079 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `31fbef162594de01` |
| CAP-080 | Continue Architecture Planning.md > v0.9 > v0.9 — Acquisition Provider Architecture | `eea1348bf2068f01` | `d4887385d398032c` |
| CAP-081 | Continue Architecture Planning.md > v0.9 > v0.9 — Acquisition Provider Architecture > 0.9 architecture | `5fc310077e8ecc5d` | `d8e69e34cd22ac65` |
| CAP-082 | Continue Architecture Planning.md > v0.9 > v0.9 — Acquisition Provider Architecture > The important separation | `6dd6891bdf68d1d1` | `8625d74d3086c8f9` |
| CAP-083 | Continue Architecture Planning.md > v0.9 > 1. AcquisitionProvider contract | `e730c4c75f6355bc` | `11b4cb4f313dc62e` |
| CAP-084 | Continue Architecture Planning.md > v0.9 > 2. Provider capabilities | `dfe9de2b5b7cab4b` | `cdf2be7863598182` |
| CAP-085 | Continue Architecture Planning.md > v0.9 > 3. Provider selection | `6f05b9a80e4a43e9` | `8507f5fa0f351131` |
| CAP-086 | Continue Architecture Planning.md > v0.9 > 4. GM-XHR becomes a component | `ad4e800afa701a04` | `e258065b06856087` |
| CAP-087 | Continue Architecture Planning.md > v0.9 > 5. Observation gets provider provenance | `5da69b344aa3c4cc` | `d48615f555d51837` |
| CAP-088 | Continue Architecture Planning.md > v0.9 > 6. Provider failure ≠ acquisition denial | `e7f9398fa681b613` | `ec0a86609c55f24a` |
| CAP-089 | Continue Architecture Planning.md > v0.9 > 6. Provider failure ≠ acquisition denial > Policy denial | `1f3a157b32502400` | `7cf12d8b7ce61f15` |
| CAP-090 | Continue Architecture Planning.md > v0.9 > 6. Provider failure ≠ acquisition denial > Provider failure | `23a583db79941838` | `e28950d9221929a0` |
| CAP-091 | Continue Architecture Planning.md > v0.9 > 7. Provider selection itself becomes an event | `b194cd6e72bb2a6d` | `30f5d7acba90861e` |
| CAP-092 | Continue Architecture Planning.md > v0.9 > 8. A deeper consequence: acquisition becomes replaceable | `457fcfb8c66450fe` | `899f38a3c3b51725` |
| CAP-093 | Continue Architecture Planning.md > v0.9 > 8. A deeper consequence: acquisition becomes replaceable > Cache provider | `4772487d0ddb9619` | `81b34d002f281ec8` |
| CAP-094 | Continue Architecture Planning.md > v0.9 > 8. A deeper consequence: acquisition becomes replaceable > Replay provider | `9a8749b47ac5b848` | `30cd65f576d131e5` |
| CAP-095 | Continue Architecture Planning.md > v0.9 > 9. The engine is now approaching a general resource runtime | `5803d003271c0890` | `c031529afc561ed7` |
| CAP-096 | Continue Architecture Planning.md > v0.9 > 10. v0.9 invariants | `2bf2843126fa35e9` | `72fc842eef73d720` |
| CAP-097 | Continue Architecture Planning.md > v0.9 > 10. v0.9 invariants > I1 — Discovery independence | `fe3b15e6c58f6967` | `ce10dcc162ac30e4` |
| CAP-098 | Continue Architecture Planning.md > v0.9 > 10. v0.9 invariants > I2 — Policy independence | `f0806177d0a99c13` | `9e912bf54e6adf55` |
| CAP-099 | Continue Architecture Planning.md > v0.9 > 10. v0.9 invariants > I3 — Capability soundness | `1a338b6cc3409ae8` | `fa018fc120c7f709` |
| CAP-100 | Continue Architecture Planning.md > v0.9 > 10. v0.9 invariants > I4 — Method safety | `20c13d6e8a4fac65` | `73ca2874fdd738e0` |
| CAP-101 | Continue Architecture Planning.md > v0.9 > 10. v0.9 invariants > I5 — Provenance | `4fc8a197b8e801ab` | `1ca415cd287ed5f2` |
| CAP-102 | Continue Architecture Planning.md > v0.9 > 10. v0.9 invariants > I6 — Observation integrity | `e14f0c9dbd9a62c1` | `210a9965342a4da2` |
| CAP-103 | Continue Architecture Planning.md > v0.9 > 10. v0.9 invariants > I7 — Replay distinction | `84c9f6b9fb8f72ec` | `3b0c2afeb419ced3` |
| CAP-104 | Continue Architecture Planning.md > v0.9 > 11. The next problem is now visible | `b23ff230a0bac42f` | `cfcf3aaca1d511e1` |
| CAP-105 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `31fbef162594de01` |
| CAP-106 | Continue Architecture Planning.md > v0.10 > v0.10 — Acquisition Runtime | `fe26d64c07077eed` | `bfce9740e5b2aec3` |
| CAP-107 | Continue Architecture Planning.md > v0.10 > v0.10 — Acquisition Runtime > 1. The new architecture | `daf02802e49a82c8` | `edd74a32e98d626c` |
| CAP-108 | Continue Architecture Planning.md > v0.10 > 2. The key distinction: Scheduler vs Runtime | `d41e0d5dda70656b` | `f5ec0d705e49d1c4` |
| CAP-109 | Continue Architecture Planning.md > v0.10 > 2. The key distinction: Scheduler vs Runtime > Scheduler | `d3a27d96cd0791a2` | `fdf4c7eb3a1297c6` |
| CAP-110 | Continue Architecture Planning.md > v0.10 > 2. The key distinction: Scheduler vs Runtime > Runtime | `1093115897879aa3` | `fe6db2ab853b4fef` |
| CAP-111 | Continue Architecture Planning.md > v0.10 > 3. AcquisitionRuntime contract | `e7f6c6d07005e7ec` | `db21da3c0055379f` |
| CAP-112 | Continue Architecture Planning.md > v0.10 > 4. Admission control | `ebf97fd0ebf9f87d` | `a8959fa5c50a80fe` |
| CAP-113 | Continue Architecture Planning.md > v0.10 > 5. Budget becomes a first-class object | `a42999d924379a9a` | `80baa48ce1c3d86f` |
| CAP-114 | Continue Architecture Planning.md > v0.10 > 6. Why reservation must precede execution | `d2e67a95d884089d` | `6027dc0b27675c4b` |
| CAP-115 | Continue Architecture Planning.md > v0.10 > 7. OriginController | `1d04600810b3b2aa` | `62fe9dfb3a09df35` |
| CAP-116 | Continue Architecture Planning.md > v0.10 > 8. Provider selection happens after admission prerequisites | `49d46da9fb44e15a` | `d060a8f05a748c40` |
| CAP-117 | Continue Architecture Planning.md > v0.10 > 9. Provider must not own runtime policy | `729a52faa1711674` | `49f1071a7d13bc5f` |
| CAP-118 | Continue Architecture Planning.md > v0.10 > 10. Cancellation becomes explicit | `e77c18c087b45f04` | `0967662d0913c2fb` |
| CAP-119 | Continue Architecture Planning.md > v0.10 > 11. Timeout belongs to Runtime | `882482eed009f245` | `00d0dd45f899f1ae` |
| CAP-120 | Continue Architecture Planning.md > v0.10 > 12. Retry belongs to Runtime | `f8ef2abf6a24af3c` | `f56f4449526753d5` |
| CAP-121 | Continue Architecture Planning.md > v0.10 > 13. Plan vs Attempt | `c71ebe69a03b1d14` | `89b6087ec2cff15b` |
| CAP-122 | Continue Architecture Planning.md > v0.10 > 14. Runtime event model | `aefb5d5161effece` | `ea5c9a560fa6243e` |
| CAP-123 | Continue Architecture Planning.md > v0.10 > 15. Runtime state machine | `ba86bf732da6cea7` | `13c72ecb05fda76c` |
| CAP-124 | Continue Architecture Planning.md > v0.10 > 16. The complete execution equation | `c052686db8bb2280` | `e3e80fdb37642317` |
| CAP-125 | Continue Architecture Planning.md > v0.10 > 17. The resulting architecture | `6a593c3249c4d194` | `02fa514c07bc1a8e` |
| CAP-126 | Continue Architecture Planning.md > v0.10 > 17. The resulting architecture > What v0.10 accomplishes | `97ca351252ad969b` | `4a564a66b97f5551` |
| CAP-127 | Continue Architecture Planning.md > v0.10 > 17. The resulting architecture > What v0.10 accomplishes > Next boundary: v0.11 | `a2165d23ebedd83e` | `100e548fae82f8ab` |
| CAP-128 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `31fbef162594de01` |
| CAP-129 | Continue Architecture Planning.md > v0.11 > v0.11 — Response Recognition Runtime | `ca5088e61f854e38` | `7a048cc715ad0d56` |
| CAP-130 | Continue Architecture Planning.md > v0.11 > v0.11 — Response Recognition Runtime > 1. v0.11 architecture | `70c9ad8d4d8f5137` | `c260ee4b2c359ed9` |
| CAP-131 | Continue Architecture Planning.md > v0.11 > 2. RecognitionProvider contract | `b411a63eed9efe55` | `fac7a271073b5b59` |
| CAP-132 | Continue Architecture Planning.md > v0.11 > 3. Recognition is not discovery | `5a368cad0c094f91` | `d1032449e68f3da9` |
| CAP-133 | Continue Architecture Planning.md > v0.11 > 4. Response Router | `7864f99b6e194005` | `aea72c08cc47ddd0` |
| CAP-134 | Continue Architecture Planning.md > v0.11 > 5. Provider priority | `88b92c75855bbfc5` | `1a70b03f71d106dd` |
| CAP-135 | Continue Architecture Planning.md > v0.11 > 6. Recognition confidence | `c9266637fc0c48f2` | `6467286c2221ffad` |
| CAP-136 | Continue Architecture Planning.md > v0.11 > 7. Content-type is only one signal | `909414eb52323d9a` | `af029dcba896a72e` |
| CAP-137 | Continue Architecture Planning.md > v0.11 > 8. Recognition evidence | `dc51869bec183b62` | `56b8c7b7c93170ca` |
| CAP-138 | Continue Architecture Planning.md > v0.11 > 9. Recognition result contract | `4255e54d8482757e` | `0ac93c978a6b2001` |
| CAP-139 | Continue Architecture Planning.md > v0.11 > 10. Why providers should not enqueue candidates | `69c0ebbda678cc77` | `1d1f22157bda67de` |
| CAP-140 | Continue Architecture Planning.md > v0.11 > 11. Recognition Runtime | `10cab9e72695dd48` | `e7461321334b85dc` |
| CAP-141 | Continue Architecture Planning.md > v0.11 > 12. Recognition failure taxonomy | `0ee2d1fe5760aaff` | `9d6729b54beaec59` |
| CAP-142 | Continue Architecture Planning.md > v0.11 > 12. Recognition failure taxonomy > No recognizer | `08089d24fa14c2cd` | `1514b4435ac66c89` |
| CAP-143 | Continue Architecture Planning.md > v0.11 > 12. Recognition failure taxonomy > Provider rejected | `14183937595280c0` | `9042661fd62f5568` |
| CAP-144 | Continue Architecture Planning.md > v0.11 > 12. Recognition failure taxonomy > Provider error | `9ade31ecd1b5e04c` | `cf5533aa14fc20ab` |
| CAP-145 | Continue Architecture Planning.md > v0.11 > 12. Recognition failure taxonomy > Successful recognition, zero discoveries | `3da35f02079371a2` | `9f1d336484069c9f` |
| CAP-146 | Continue Architecture Planning.md > v0.11 > 13. v0.11 state progression | `dc2fb5bd4e61d414` | `58d973d63fe64c01` |
| CAP-147 | Continue Architecture Planning.md > v0.11 > 14. Multiple recognizers | `abbf71ce9c30478f` | `97b03a0a7cfcbd45` |
| CAP-148 | Continue Architecture Planning.md > v0.11 > 15. Recognition graph | `2819c51de5d2660f` | `2150dc55d0661278` |
| CAP-149 | Continue Architecture Planning.md > v0.11 > 16. The graph is now explicitly causal | `baad7fe2cbbe1c51` | `0805d92d2530a0da` |
| CAP-150 | Continue Architecture Planning.md > v0.11 > 17. v0.11 event ledger | `d1b48bf7f9f835ed` | `2dfd0cfceb529205` |
| CAP-151 | Continue Architecture Planning.md > v0.11 > 18. The emerging generic algorithm | `ee8699282c7f1a96` | `ca941d6d54ce78a3` |
| CAP-152 | Continue Architecture Planning.md > v0.11 > 19. The next major abstraction: Candidate Sources | `d19149474e1f64da` | `df831afc9014de88` |
| CAP-153 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `31fbef162594de01` |
| CAP-154 | Continue Architecture Planning.md > v0.12 > v0.12 — Candidate Source Architecture | `642f728210a8b7c2` | `c4ed7682752f4f31` |
| CAP-155 | Continue Architecture Planning.md > v0.12 > v0.12 — Candidate Source Architecture > 1. Three independent provider planes | `aa76ddd0754ea9bd` | `58c4d91d53adcf61` |
| CAP-156 | Continue Architecture Planning.md > v0.12 > 2. CandidateSource contract | `c130fecc0d20b836` | `2dca0b4676486419` |
| CAP-157 | Continue Architecture Planning.md > v0.12 > 3. CandidateSource is a search-space adapter | `e1c5e0d0ed0dc365` | `cd23c77de5b5eba7` |
| CAP-158 | Continue Architecture Planning.md > v0.12 > 3. CandidateSource is a search-space adapter > Web page | `fae9f11dea030429` | `38565c6a193786f8` |
| CAP-159 | Continue Architecture Planning.md > v0.12 > 3. CandidateSource is a search-space adapter > Network traffic | `09dd03f138771d88` | `002ef4f6405cd889` |
| CAP-160 | Continue Architecture Planning.md > v0.12 > 3. CandidateSource is a search-space adapter > Sitemap | `4db550cd984016b9` | `6085866c00039f3a` |
| CAP-161 | Continue Architecture Planning.md > v0.12 > 3. CandidateSource is a search-space adapter > User seed | `e437ef92dec28ca2` | `c73568bead979546` |
| CAP-162 | Continue Architecture Planning.md > v0.12 > 3. CandidateSource is a search-space adapter > Document | `d6bd8c0aeee80fed` | `f5ebb217af119a26` |
| CAP-163 | Continue Architecture Planning.md > v0.12 > 4. CandidateProposal | `78ee8219b43d53a3` | `62c884db84a76474` |
| CAP-164 | Continue Architecture Planning.md > v0.12 > 5. Why proposals matter | `16ab33ddd5276755` | `7dff7f1106691cb6` |
| CAP-165 | Continue Architecture Planning.md > v0.12 > 6. CandidateNormalizer | `2408de8c28d90d9f` | `4bf4eb2a533a2750` |
| CAP-166 | Continue Architecture Planning.md > v0.12 > 7. Source Registry | `070c330e40ecf59a` | `0805492fd8729d75` |
| CAP-167 | Continue Architecture Planning.md > v0.12 > 8. The HTML provider should evolve | `91b423b7ee0450f0` | `99804773304bc633` |
| CAP-168 | Continue Architecture Planning.md > v0.12 > 9. Evidence becomes an intermediate layer | `4a4a063b0144ec68` | `6b1947a337850a9c` |
| CAP-169 | Continue Architecture Planning.md > v0.12 > 10. Discovery becomes evidence-driven | `e2f7c4390b1f6d96` | `d78fe1dac449931c` |
| CAP-170 | Continue Architecture Planning.md > v0.12 > 11. CandidateSource context | `fa47ce60b3f495de` | `ce09c8cac3d5b01e` |
| CAP-171 | Continue Architecture Planning.md > v0.12 > 12. CandidateSource examples | `11954e516ad57d41` | `60e91dd608485435` |
| CAP-172 | Continue Architecture Planning.md > v0.12 > 12. CandidateSource examples > HTML link source | `d973ca2a5d61b75a` | `b339e6a217552bfd` |
| CAP-173 | Continue Architecture Planning.md > v0.12 > 13. NetworkSource | `2bc08c1f759747d6` | `bb1651d3b7187581` |
| CAP-174 | Continue Architecture Planning.md > v0.12 > 14. Search-space composition | `27a78c6473ad2e85` | `207d8ff36e1c1bff` |
| CAP-175 | Continue Architecture Planning.md > v0.12 > 15. Candidate identity | `b05d4b74fa6468de` | `c4a8b0f00a70ea21` |
| CAP-176 | Continue Architecture Planning.md > v0.12 > 16. Discovery confidence aggregation | `a5d954ad3b3ac52c` | `2cc63aa9a9039d09` |
| CAP-177 | Continue Architecture Planning.md > v0.12 > 17. v0.12 provenance graph | `5f22d46a9e3bfb47` | `6274a932eb73a2f3` |
| CAP-178 | Continue Architecture Planning.md > v0.12 > 18. v0.12 invariants | `8f8a3d562755563f` | `f165ae77538c114b` |
| CAP-179 | Continue Architecture Planning.md > v0.12 > 18. v0.12 invariants > S1 — Source purity | `e37ee7cf14d5c738` | `1595872ad2c3e04f` |
| CAP-180 | Continue Architecture Planning.md > v0.12 > 18. v0.12 invariants > S2 — Core ownership | `10fb53e9cf60bb72` | `b37d3aa4ee4c1a6e` |
| CAP-181 | Continue Architecture Planning.md > v0.12 > 18. v0.12 invariants > S3 — Proposal semantics | `461335663644ae4f` | `93fa8f65ad50fb9b` |
| CAP-182 | Continue Architecture Planning.md > v0.12 > 18. v0.12 invariants > S4 — Identity | `ce6b7c768d967f05` | `1fc69ca4d2edeee8` |
| CAP-183 | Continue Architecture Planning.md > v0.12 > 18. v0.12 invariants > S5 — Provenance | `40e09ded17850681` | `4bede606fac32936` |
| CAP-184 | Continue Architecture Planning.md > v0.12 > 18. v0.12 invariants > S6 — Representability | `5f9c3c2adb79af6d` | `34a0a88677ab9d72` |
| CAP-185 | Continue Architecture Planning.md > v0.12 > 18. v0.12 invariants > S7 — Observation independence | `171afc361b44a047` | `9eccc35dd40cb094` |
| CAP-186 | Continue Architecture Planning.md > v0.12 > 19. The complete v0.12 architecture | `25f6942ae05cde11` | `7ecde91811b7c649` |
| CAP-187 | Continue Architecture Planning.md > v0.12 > 20. The deeper abstraction | `7975ae31e688debe` | `6304869c614ff8b1` |
| CAP-188 | Continue Architecture Planning.md > v0.12 > 20. The deeper abstraction > v0.13 — the next boundary | `9f00703694deca2b` | `5943c56c5f55986a` |
| CAP-189 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `31fbef162594de01` |
| CAP-190 | Continue Architecture Planning.md > v0.13 > v0.13 — Discovery Controller | `3832d7b44bb1c243` | `c5d58b221b262396` |
| CAP-191 | Continue Architecture Planning.md > v0.13 > 1. The complete v0.13 architecture | `6a59e2189ab2b669` | `15523b3f437e4bbd` |
| CAP-192 | Continue Architecture Planning.md > v0.13 > 2. Two schedulers, not one | `0397ad6c9e776b72` | `b0c5505e5528056f` |
| CAP-193 | Continue Architecture Planning.md > v0.13 > 3. DiscoveryTask | `a1865db9880bf729` | `50448163703f1795` |
| CAP-194 | Continue Architecture Planning.md > v0.13 > 4. Why a task is necessary | `e8809510f4a1bf37` | `f32928703e4f6afe` |
| CAP-195 | Continue Architecture Planning.md > v0.13 > 5. Source Policy | `86ed0443622ce9f0` | `9c31056bdf3d8c51` |
| CAP-196 | Continue Architecture Planning.md > v0.13 > 6. Source budgets | `5c0f9cbb043357d1` | `4df2f1fec1402b34` |
| CAP-197 | Continue Architecture Planning.md > v0.13 > 7. Proposal budget is different | `80e3cf5c6d164361` | `c6742346fa6d3c22` |
| CAP-198 | Continue Architecture Planning.md > v0.13 > 8. Incremental sources | `c69d9342c506f419` | `f451723d5ee8f6bb` |
| CAP-199 | Continue Architecture Planning.md > v0.13 > 9. Source execution contract | `97e31343c44cf050` | `cdcdf311302a3b19` |
| CAP-200 | Continue Architecture Planning.md > v0.13 > 10. Source scheduling | `32fa4d27faecbea8` | `fcdc112915fa2bfb` |
| CAP-201 | Continue Architecture Planning.md > v0.13 > 11. Fairness | `9b7eed41f36ba6df` | `03822532720e36d2` |
| CAP-202 | Continue Architecture Planning.md > v0.13 > 12. Candidate deduplication belongs after normalization | `27950cef160f1a1b` | `6cc44e86e9e60b78` |
| CAP-203 | Continue Architecture Planning.md > v0.13 > 13. Discovery provenance | `508a9c05fde07aa2` | `b83099b0fc146c8c` |
| CAP-204 | Continue Architecture Planning.md > v0.13 > 14. Candidate generation becomes transactional | `ce32b334f6c8ac5b` | `21420354bdcc97f7` |
| CAP-205 | Continue Architecture Planning.md > v0.13 > 15. Concurrent source execution | `fd5b14ce2169b83a` | `90b011dca93419e7` |
| CAP-206 | Continue Architecture Planning.md > v0.13 > 16. DiscoveryController | `25484819b08e0c12` | `d98b429748e51f22` |
| CAP-207 | Continue Architecture Planning.md > v0.13 > 17. Event ledger | `532dc51fd32e9dd2` | `689d9a1ce715fb6f` |
| CAP-208 | Continue Architecture Planning.md > v0.13 > 18. Discovery failure taxonomy | `42535a44857dc9f1` | `17c24e9a7df0c35c` |
| CAP-209 | Continue Architecture Planning.md > v0.13 > 19. The generic blind-scan analogy is now much stronger | `5a100a1b66c86c3f` | `c2a23a30629f8a79` |
| CAP-210 | Continue Architecture Planning.md > v0.13 > 20. v0.13 invariants | `dfe76c3c98b39490` | `d70c33581fd2e6b9` |
| CAP-211 | Continue Architecture Planning.md > v0.13 > 20. v0.13 invariants > D1 — Source isolation | `2f6040751d8f408d` | `9c67effd6baf5b0d` |
| CAP-212 | Continue Architecture Planning.md > v0.13 > 20. v0.13 invariants > D2 — Acquisition isolation | `2c63f9f962bffc01` | `467993573d6b2e97` |
| CAP-213 | Continue Architecture Planning.md > v0.13 > 20. v0.13 invariants > D3 — Normalization ownership | `13efed07ad1fa835` | `38855385393ca167` |
| CAP-214 | Continue Architecture Planning.md > v0.13 > 20. v0.13 invariants > D4 — Bounded generation | `fa941a6c33a4d5d5` | `6f186dcefc67119b` |
| CAP-215 | Continue Architecture Planning.md > v0.13 > 20. v0.13 invariants > D5 — Bounded recursion | `4b9015dca1fd2fee` | `875c88b839d345d2` |
| CAP-216 | Continue Architecture Planning.md > v0.13 > 20. v0.13 invariants > D6 — Provenance preservation | `d02d05028a92da2a` | `310623bcb1a0384f` |
| CAP-217 | Continue Architecture Planning.md > v0.13 > 20. v0.13 invariants > D7 — Atomic task claiming | `0e9a94aadc81dee1` | `271edad98c351f07` |
| CAP-218 | Continue Architecture Planning.md > v0.13 > 20. v0.13 invariants > D8 — Convergence | `13f6fa027bfa860d` | `f7bbc40869877ea6` |
| CAP-219 | Continue Architecture Planning.md > v0.13 > 20. v0.13 invariants > D9 — Discovery/acquisition independence | `4bf160db155cfe43` | `8f6b7ddbc4393733` |
| CAP-220 | Continue Architecture Planning.md > v0.13 > 21. The architecture is now approaching a stable core | `afae5f609fead712` | `a974855b0b3f6fa7` |
| CAP-221 | Continue Architecture Planning.md > v0.14 > v0.14 — the next missing abstraction | `64d39e3ea527b974` | `465e7bf108310f16` |
| CAP-222 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `31fbef162594de01` |
| CAP-223 | Continue Architecture Planning.md > v0.14 > v0.14 — DiscoveryDomain + ScanSession | `b02a4f8e96d89613` | `8f21dcb315450245` |
| CAP-224 | Continue Architecture Planning.md > v0.14 > 1. The conceptual split | `ff477c5be74d62dd` | `e46b149a9684595b` |
| CAP-225 | Continue Architecture Planning.md > v0.14 > 1. The conceptual split > Discovery Engine | `617dd64f5e72f0f9` | `3e39d4795d78cd20` |
| CAP-226 | Continue Architecture Planning.md > v0.14 > 1. The conceptual split > DiscoveryDomain | `b7d87495dcee13ad` | `b57accedf8bd119d` |
| CAP-227 | Continue Architecture Planning.md > v0.14 > 1. The conceptual split > ScanSession | `6c9a3494e477a752` | `eda14b01544a0ea9` |
| CAP-228 | Continue Architecture Planning.md > v0.14 > 2. DVB analogy | `9e4e106a44e2636d` | `d2772735d0df687e` |
| CAP-229 | Continue Architecture Planning.md > v0.14 > 3. DiscoveryDomain | `a80e935ffd4208af` | `ef5898936fa18881` |
| CAP-230 | Continue Architecture Planning.md > v0.14 > 4. Domain vs policy | `958622513a849a8a` | `05d74678a84cdcce` |
| CAP-231 | Continue Architecture Planning.md > v0.14 > 5. Domain membership | `cbab5fcf17ee3b58` | `9fae3f802177ba0c` |
| CAP-232 | Continue Architecture Planning.md > v0.14 > 6. Explicit seeds | `dcd28df8b69e83a7` | `978d41f89fc4eb14` |
| CAP-233 | Continue Architecture Planning.md > v0.14 > 7. Seed ≠ Candidate | `4cc40ee2d84d6a26` | `d44e30c350b66f59` |
| CAP-234 | Continue Architecture Planning.md > v0.14 > 8. Discovery frontier | `c50ea81370c60ebe` | `c79083ec2687fb64` |
| CAP-235 | Continue Architecture Planning.md > v0.14 > 9. ScanSession | `37b91dcb4be5bff3` | `9188866aabc706f4` |
| CAP-236 | Continue Architecture Planning.md > v0.14 > 10. Session lifecycle | `2dd0009e726d876b` | `fe32abe3b2b4e82d` |
| CAP-237 | Continue Architecture Planning.md > v0.14 > 11. Termination becomes explicit | `ea92e9620d4badb7` | `be4ee98ba291b26e` |
| CAP-238 | Continue Architecture Planning.md > v0.14 > 11. Termination becomes explicit > Frontier exhaustion | `54cc94239c86c950` | `a1c6a61ccff798cc` |
| CAP-239 | Continue Architecture Planning.md > v0.14 > 11. Termination becomes explicit > Candidate limit | `079765d39f3c9e6a` | `f622b845463af0c3` |
| CAP-240 | Continue Architecture Planning.md > v0.14 > 11. Termination becomes explicit > Acquisition limit | `09f6498895685096` | `b39651dc79ccd481` |
| CAP-241 | Continue Architecture Planning.md > v0.14 > 11. Termination becomes explicit > Discovery-task limit | `3ed20ada9461450d` | `e9dc11139d7443f4` |
| CAP-242 | Continue Architecture Planning.md > v0.14 > 11. Termination becomes explicit > Proposal limit | `1c260b08a96ad107` | `85e0991c65f7407b` |
| CAP-243 | Continue Architecture Planning.md > v0.14 > 11. Termination becomes explicit > Depth limit | `ef72c1e4c6847210` | `63e353a3f72f2923` |
| CAP-244 | Continue Architecture Planning.md > v0.14 > 11. Termination becomes explicit > Time limit | `e592a9cae0957d20` | `4ad46908a05c59de` |
| CAP-245 | Continue Architecture Planning.md > v0.14 > 11. Termination becomes explicit > External stop | `288b7a211f0618d2` | `9b6cb6d0d389c994` |
| CAP-246 | Continue Architecture Planning.md > v0.14 > 12. Termination evaluator | `3a2180a47b8f242b` | `6a6d8c5a3e1f55a2` |
| CAP-247 | Continue Architecture Planning.md > v0.14 > 13. Limit reached ≠ successful completion | `12d38f53cddb1c9a` | `7773199bb0e49c2d` |
| CAP-248 | Continue Architecture Planning.md > v0.14 > 14. The session snapshot | `44d3c6888a4e5318` | `651ef6aafcf06fdc` |
| CAP-249 | Continue Architecture Planning.md > v0.14 > 15. Resumability | `8c1ca2f3812891aa` | `68093b6845bb69cd` |
| CAP-250 | Continue Architecture Planning.md > v0.14 > 16. Lease-based claims | `6f132c02f6066934` | `4614f832711a8cac` |
| CAP-251 | Continue Architecture Planning.md > v0.14 > 17. Session ownership | `af9755434191daaf` | `358e779385e7e746` |
| CAP-252 | Continue Architecture Planning.md > v0.14 > 18. Scan vs engine knowledge | `789bc6aa2942f2a5` | `8281f81f32b500e9` |
| CAP-253 | Continue Architecture Planning.md > v0.14 > 19. Domain snapshot vs mutable domain | `e4eb92d81e5ffe68` | `b8858b7603b94982` |
| CAP-254 | Continue Architecture Planning.md > v0.14 > 20. Domain identity | `19b643573d816493` | `477446eb2d2a4cb2` |
| CAP-255 | Continue Architecture Planning.md > v0.14 > 21. Search frontier vs knowledge graph | `4246c5780ba21f61` | `2fd1d485cef2af17` |
| CAP-256 | Continue Architecture Planning.md > v0.14 > 22. The complete v0.14 architecture | `90c9e1e94822e059` | `f231f38722db7e0d` |
| CAP-257 | Continue Architecture Planning.md > v0.14 > 23. Four distinct scopes | `7fbfb38c612cd1de` | `85cd9a4fb41bea6f` |
| CAP-258 | Continue Architecture Planning.md > v0.14 > 24. Strong invariants | `fa5f9bcf90f2b28e` | `edd92d13597a3d97` |
| CAP-259 | Continue Architecture Planning.md > v0.14 > 24. Strong invariants > Domain invariant | `f59d566824f84afb` | `a08c5dd9cd868f39` |
| CAP-260 | Continue Architecture Planning.md > v0.14 > 24. Strong invariants > Session invariant | `2f40ec6bdca44bbb` | `214fd49378236867` |
| CAP-261 | Continue Architecture Planning.md > v0.14 > 24. Strong invariants > Snapshot invariant | `aa5e3d252f4b44df` | `f5f2c3a3e757201b` |
| CAP-262 | Continue Architecture Planning.md > v0.14 > 24. Strong invariants > Frontier invariant | `a59b3c705f71eeb2` | `a80627dca5cf7103` |
| CAP-263 | Continue Architecture Planning.md > v0.14 > 24. Strong invariants > Termination invariant | `dec12949043d78dc` | `2c8c5439ac4ca964` |
| CAP-264 | Continue Architecture Planning.md > v0.14 > 24. Strong invariants > Recovery invariant | `f162cdd51f8e91f2` | `59371c39397fa93a` |
| CAP-265 | Continue Architecture Planning.md > v0.14 > 24. Strong invariants > Provenance invariant | `8aba9c8e873e0baa` | `c7be00190d38cff0` |
| CAP-266 | Continue Architecture Planning.md > v0.14 > 24. Strong invariants > Acquisition invariant | `a4aacdac7065e23a` | `6a19386ffb79ebd4` |
| CAP-267 | Continue Architecture Planning.md > v0.14 > 24. Strong invariants > Discovery invariant | `3ae3c840bf249a3a` | `cea36b1c701b8658` |
| CAP-268 | Continue Architecture Planning.md > v0.14 > 25. Failure taxonomy | `57f07e4a7844b7bf` | `7b74f27ff2f0bb22` |
| CAP-269 | Continue Architecture Planning.md > v0.14 > 26. What v0.14 changes conceptually | `43cd8cc3f96eef53` | `7c6554a1d42f11f8` |
| CAP-270 | Continue Architecture Planning.md > v0.14 > 27. The next abstraction | `2a42088294d5a5bc` | `0324ac7de4f2db33` |
| CAP-271 | Continue Architecture Planning.md > v0.15 > v0.15 — WorkItem + Frontier Runtime | `dd4d431dabc7e4f4` | `fc8389e9672844db` |
| CAP-272 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `31fbef162594de01` |
| CAP-273 | Continue Architecture Planning.md > v0.15 > v0.15 — WorkItem + Frontier Runtime | `dd4d431dabc7e4f4` | `7e5bf52138b2ae06` |
| CAP-274 | Continue Architecture Planning.md > v0.15 > 1. The key distinction | `a85941005d16b5fa` | `7cb4a1ca3a35a079` |
| CAP-275 | Continue Architecture Planning.md > v0.15 > 2. Why `WorkItem` exists | `c561df2398a0a5ee` | `cf520317741be884` |
| CAP-276 | Continue Architecture Planning.md > v0.15 > 3. WorkItem | `429dbe768927d64d` | `7bd9007539bf4905` |
| CAP-277 | Continue Architecture Planning.md > v0.15 > 4. Work kinds | `8296519710cb6f8e` | `b714210243abb969` |
| CAP-278 | Continue Architecture Planning.md > v0.15 > 5. Work payload | `6509db8f63f0b0c8` | `4fa9bbb2c7e3064f` |
| CAP-279 | Continue Architecture Planning.md > v0.15 > 6. Work lifecycle | `8b57202cf299155a` | `7e51e10900a3e89b` |
| CAP-280 | Continue Architecture Planning.md > v0.15 > 7. Claiming becomes a formal protocol | `e82a9ba21f80a731` | `dfb92e9a9ec9b4ac` |
| CAP-281 | Continue Architecture Planning.md > v0.15 > 8. Work lease | `df87bd6493e2d168` | `81c260c0ee8e1090` |
| CAP-282 | Continue Architecture Planning.md > v0.15 > 9. Lease recovery | `f61dbf0789caaf96` | `d1cdab5b972a3a58` |
| CAP-283 | Continue Architecture Planning.md > v0.15 > 10. Frontier Runtime | `abea896a54cd4731` | `ecb03b77288d139a` |
| CAP-284 | Continue Architecture Planning.md > v0.15 > 11. WorkScheduler | `403e7f7591f46293` | `59c524ee8cafbf6d` |
| CAP-285 | Continue Architecture Planning.md > v0.15 > 12. Priority starvation | `96793b6d62407b91` | `0d4adefb94314c48` |
| CAP-286 | Continue Architecture Planning.md > v0.15 > 13. Priority aging | `0f7d415c526ed679` | `c11aae08cfbe2696` |
| CAP-287 | Continue Architecture Planning.md > v0.15 > 14. Discovery and acquisition fairness | `327e2fcc16ba68e6` | `3df61df74ccfb2e5` |
| CAP-288 | Continue Architecture Planning.md > v0.15 > 15. Why not one giant queue? | `10c88175fe256fac` | `a7d86fd4f8f9c84a` |
| CAP-289 | Continue Architecture Planning.md > v0.15 > 16. Work dependencies | `4f1b6d7228cb7835` | `2722bbf14eb7d2ad` |
| CAP-290 | Continue Architecture Planning.md > v0.15 > 17. But dependencies must not create hidden coupling | `a5b60e64d2260b54` | `512b8e2a7ae34473` |
| CAP-291 | Continue Architecture Planning.md > v0.15 > 18. Dependency states | `415df6d16a942ae1` | `f96dd34daaa4e299` |
| CAP-292 | Continue Architecture Planning.md > v0.15 > 19. Work completion | `ee2e1e0bd6dda03d` | `c32844b1d5ecba88` |
| CAP-293 | Continue Architecture Planning.md > v0.15 > 20. Work execution boundary | `b881d8fdab16ebec` | `e7db284ff7591f24` |
| CAP-294 | Continue Architecture Planning.md > v0.15 > 21. Work Runtime | `35e8d02a88cffc43` | `fa04fc8d1e19eb57` |
| CAP-295 | Continue Architecture Planning.md > v0.15 > 22. Retry becomes generic | `fe06065d9669c952` | `c3a69a9cbae6c111` |
| CAP-296 | Continue Architecture Planning.md > v0.15 > 23. Retry identity | `2b12a9c726fc626c` | `dd95eca6b1c4d367` |
| CAP-297 | Continue Architecture Planning.md > v0.15 > 24. Cancellation | `52665574318eb9b9` | `08f4345e7454cc15` |
| CAP-298 | Continue Architecture Planning.md > v0.15 > 25. Scan termination with WorkItems | `af21c2059313a202` | `0af2067c33ac6238` |
| CAP-299 | Continue Architecture Planning.md > v0.15 > 26. The three frontier states | `f8fb1f1fba193a40` | `633abb0009e840ad` |
| CAP-300 | Continue Architecture Planning.md > v0.15 > 27. Scheduled work | `a982bd10a900ea2c` | `223a1f5c8be1b0a8` |
| CAP-301 | Continue Architecture Planning.md > v0.15 > 28. Work state machine | `f239ea94a5539c66` | `02b3e3225bdbcffc` |
| CAP-302 | Continue Architecture Planning.md > v0.15 > 29. Domain → Session → Work | `fda427b46c9976a5` | `ae0846f5b5b28e27` |
| CAP-303 | Continue Architecture Planning.md > v0.15 > 30. What belongs where? | `a23acb44ca790e05` | `efd539b83b49c788` |
| CAP-304 | Continue Architecture Planning.md > v0.15 > 31. The crucial invariant | `ce32d31c253fa81c` | `75d76e40c86c328d` |
| CAP-305 | Continue Architecture Planning.md > v0.15 > 32. Discovery vs acquisition remains intact | `2b149458dac24861` | `ee224ce3f0a96c24` |
| CAP-306 | Continue Architecture Planning.md > v0.15 > 33. The resulting architecture | `7a113576e9527ddd` | `4536d11631879a41` |
| CAP-307 | Continue Architecture Planning.md > v0.15 > 34. v0.15 architectural result | `929248f2ff3cf017` | `c81befdf62150ac5` |
| CAP-308 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `31fbef162594de01` |
| CAP-309 | Continue Architecture Planning.md > v0.16 > v0.16 — EvidenceGraph + Provenance | `2cedacf2d72edcb5` | `eba80cae20a7d00b` |
| CAP-310 | Continue Architecture Planning.md > v0.16 > 1. The new abstraction | `ddc2707ae323abe3` | `8538c35739bf9d24` |
| CAP-311 | Continue Architecture Planning.md > v0.16 > 2. Observation ≠ Evidence ≠ Claim | `bd3524faa2869ea1` | `2d504d0b5c999368` |
| CAP-312 | Continue Architecture Planning.md > v0.16 > 2. Observation ≠ Evidence ≠ Claim > Observation | `d239e9cf6a51335b` | `826f3756179d57bf` |
| CAP-313 | Continue Architecture Planning.md > v0.16 > 2. Observation ≠ Evidence ≠ Claim > Evidence | `03867aea70acaf4c` | `8bb367ddde47f09d` |
| CAP-314 | Continue Architecture Planning.md > v0.16 > 2. Observation ≠ Evidence ≠ Claim > Claim | `4ca41db028253700` | `b5117645f8ddbe14` |
| CAP-315 | Continue Architecture Planning.md > v0.16 > 3. Resource ≠ Claim | `134b077fbaf8d48c` | `25ee10ff703249df` |
| CAP-316 | Continue Architecture Planning.md > v0.16 > 4. EvidenceGraph | `a9d6ca7ed9682264` | `3963d65a69a1a40f` |
| CAP-317 | Continue Architecture Planning.md > v0.16 > 5. Provenance | `01d24b842e9086be` | `dc5de7470a4ab6da` |
| CAP-318 | Continue Architecture Planning.md > v0.16 > 6. Evidence object | `2ae2508661250afd` | `6ef3b5e31984447f` |
| CAP-319 | Continue Architecture Planning.md > v0.16 > 7. Locator | `2444ef4c61742979` | `a2f72adf972d1945` |
| CAP-320 | Continue Architecture Planning.md > v0.16 > 8. Claim | `8741740df57b3106` | `de684d6f1462a797` |
| CAP-321 | Continue Architecture Planning.md > v0.16 > 9. Claims should not be confused with truth | `c215bfd0628518fb` | `de98fc87ff0f3221` |
| CAP-322 | Continue Architecture Planning.md > v0.16 > 10. Evidence strength | `92bda503a149e60a` | `a129d5b73c24f737` |
| CAP-323 | Continue Architecture Planning.md > v0.16 > 11. Independent evidence | `2e11865684886ddf` | `f115207f0970dc54` |
| CAP-324 | Continue Architecture Planning.md > v0.16 > 12. Evidence independence | `f2024e77cd632ff7` | `1ff88fa99fa58e39` |
| CAP-325 | Continue Architecture Planning.md > v0.16 > 13. Evidence graph edges | `52b8e168398a087e` | `4dc6fd7a71d76c39` |
| CAP-326 | Continue Architecture Planning.md > v0.16 > 14. Why graph edges matter | `8b6fc08a160460c5` | `5042f6de70ebde01` |
| CAP-327 | Continue Architecture Planning.md > v0.16 > 15. Provenance graph | `414c40d19a3d7b78` | `28d244b528243dc7` |
| CAP-328 | Continue Architecture Planning.md > v0.16 > 16. Resource identity | `208b17084d0025ae` | `e1746ee4e8486766` |
| CAP-329 | Continue Architecture Planning.md > v0.16 > 17. Resource fingerprint | `a8de8690760eeab7` | `f1aa889125fafb5e` |
| CAP-330 | Continue Architecture Planning.md > v0.16 > 18. URL identity vs content identity | `801fc24b5923e284` | `dbf366071fe80426` |
| CAP-331 | Continue Architecture Planning.md > v0.16 > 19. Revision detection | `8e20e8a7565f6621` | `7ded4b1cbdfd1328` |
| CAP-332 | Continue Architecture Planning.md > v0.16 > 20. Observation immutability | `e23ef8b00ffc470f` | `ff04520889a16070` |
| CAP-333 | Continue Architecture Planning.md > v0.16 > 21. Evidence immutability | `98f923d05aa29eb8` | `4ab88e77b115a30c` |
| CAP-334 | Continue Architecture Planning.md > v0.16 > 22. Extraction method becomes first-class | `5b76250ff924dc7c` | `e0f139620c38d9c6` |
| CAP-335 | Continue Architecture Planning.md > v0.16 > 23. Verification | `bf90be54d63b1fd1` | `43864d23674edf2f` |
| CAP-336 | Continue Architecture Planning.md > v0.16 > 24. Evidence lifecycle | `d820de8343545064` | `cd98e45e7bc5a3f0` |
| CAP-337 | Continue Architecture Planning.md > v0.16 > 25. Evidence states | `799f6348f688b245` | `3b34a2fd6a27c2e2` |
| CAP-338 | Continue Architecture Planning.md > v0.16 > 26. Claims can conflict | `aafc8458cdba2d86` | `186b2c26defc0183` |
| CAP-339 | Continue Architecture Planning.md > v0.16 > 27. Evidence resolution | `bc050aa54b9ed0a4` | `079ca9f14ca1493b` |
| CAP-340 | Continue Architecture Planning.md > v0.16 > 28. Discovery confidence changes meaning | `6e4d107cedbc735a` | `fca4477976fa467c` |
| CAP-341 | Continue Architecture Planning.md > v0.16 > 29. Candidate provenance | `f3b96c7f5748dba3` | `d6e4f2f0e6695b3c` |
| CAP-342 | Continue Architecture Planning.md > v0.16 > 30. The evidence ledger | `43ddf3da0512c744` | `ffc70e8c1d96e401` |
| CAP-343 | Continue Architecture Planning.md > v0.16 > 31. Two complementary graphs | `484035a02298b2fa` | `381b2a056ff1db1d` |
| CAP-344 | Continue Architecture Planning.md > v0.16 > 32. Example end-to-end trace | `693bc75a4d91483b` | `f969d16fd19470d0` |
| CAP-345 | Continue Architecture Planning.md > v0.16 > 33. v0.16 architecture | `76d4cce17c5ecd7d` | `bd78e4173435585b` |
| CAP-346 | Continue Architecture Planning.md > v0.16 > 34. New invariants | `ab2b2ea811150f42` | `5b21110f200e2489` |
| CAP-347 | Continue Architecture Planning.md > v0.16 > 34. New invariants > Evidence provenance | `cafc4a3834700ed3` | `a78b1078ab88a24d` |
| CAP-348 | Continue Architecture Planning.md > v0.16 > 34. New invariants > Claim support | `0b9d1cb11a9aabd0` | `7e3d60dee21fb947` |
| CAP-349 | Continue Architecture Planning.md > v0.16 > 34. New invariants > Historical integrity | `b1950dcb6b271f02` | `5972fa4b29df9331` |
| CAP-350 | Continue Architecture Planning.md > v0.16 > 34. New invariants > Extraction integrity | `4306d1fd4c61709d` | `fab2c1704db123fe` |
| CAP-351 | Continue Architecture Planning.md > v0.16 > 34. New invariants > Resource identity | `1f5c12a171c11344` | `8673a1c04ed51b60` |
| CAP-352 | Continue Architecture Planning.md > v0.16 > 34. New invariants > Content identity | `69dab80e97330d85` | `8b76b227ffeeee4e` |
| CAP-353 | Continue Architecture Planning.md > v0.16 > 34. New invariants > Conflict preservation | `db25e4c3cad48694` | `60a65d0941a6ba4c` |
| CAP-354 | Continue Architecture Planning.md > v0.16 > 34. New invariants > Provenance preservation | `54fb692da276cc80` | `0d6767065334608b` |
| CAP-355 | Continue Architecture Planning.md > v0.16 > 34. New invariants > Session provenance | `50641643deecec9a` | `efcf7ee6db7d1bd8` |
| CAP-356 | Continue Architecture Planning.md > v0.16 > 35. Failure taxonomy | `2f16055f49c4b2ea` | `b290ce77bc5a1f61` |
| CAP-357 | Continue Architecture Planning.md > v0.16 > 36. The deeper architectural transition | `8373774f235662fd` | `3cfc1905febbaf09` |
| CAP-358 | Continue Architecture Planning.md > v0.16 > 37. What is still missing | `16ed0faff87bd424` | `fd3e4a10c94f0c84` |
| CAP-359 | Continue Architecture Planning.md > v0.16 > 37. What is still missing > Search space | `ec5ba5c82d384efb` | `e8c9be754092bc35` |
| CAP-360 | Continue Architecture Planning.md > v0.16 > 37. What is still missing > Execution | `a45cd4bd0998e568` | `7c04cd3b1774a842` |
| CAP-361 | Continue Architecture Planning.md > v0.16 > 37. What is still missing > Work | `104ab9213e28e4ff` | `1fda83fc4b9bf33b` |
| CAP-362 | Continue Architecture Planning.md > v0.16 > 37. What is still missing > Acquisition | `a0f0155586e8f497` | `84b9c32c9945e812` |
| CAP-363 | Continue Architecture Planning.md > v0.16 > 37. What is still missing > Recognition | `22466b5a68ad045f` | `48078895592116a4` |
| CAP-364 | Continue Architecture Planning.md > v0.16 > 37. What is still missing > Discovery | `80fc402133201fbe` | `0f6e23893f446b35` |
| CAP-365 | Continue Architecture Planning.md > v0.16 > 37. What is still missing > Evidence | `03867aea70acaf4c` | `25edd48a9a7d0d76` |
| CAP-366 | Continue Architecture Planning.md > v0.16 > 37. What is still missing > History | `0e76960093379060` | `265b184bf948c1ad` |
| CAP-367 | Continue Architecture Planning.md > v0.17 > v0.17 — ResourceGraph + Identity Resolution | `de3ace3c3138081d` | `31b947ccbc87249d` |
| CAP-368 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `31fbef162594de01` |
| CAP-369 | Continue Architecture Planning.md > v0.17 > v0.17 — ResourceGraph + Identity Resolution | `de3ace3c3138081d` | `45c97ef66b65f647` |
| CAP-370 | Continue Architecture Planning.md > v0.17 > 1. The core problem | `5dd91ffaf66e0d52` | `df361dc9bf80d7ed` |
| CAP-371 | Continue Architecture Planning.md > v0.17 > 2. Resource identity must become graph-based | `d97ed4dbeb9f8157` | `5370473506b57920` |
| CAP-372 | Continue Architecture Planning.md > v0.17 > 3. Candidate vs Resource vs Locator | `2126a0a46d42611d` | `d044a7a48c6ee930` |
| CAP-373 | Continue Architecture Planning.md > v0.17 > 3. Candidate vs Resource vs Locator > Candidate | `b2452d1eba32254a` | `d3d47c4868eb6e15` |
| CAP-374 | Continue Architecture Planning.md > v0.17 > 3. Candidate vs Resource vs Locator > Locator | `cb4796be826cde7d` | `5d8653a942ba572b` |
| CAP-375 | Continue Architecture Planning.md > v0.17 > 3. Candidate vs Resource vs Locator > Resource | `eb7a842ff958c49c` | `e9d6bfe97972b7df` |
| CAP-376 | Continue Architecture Planning.md > v0.17 > 4. Why not simply canonicalize everything? | `92f757d79359af3c` | `1ca74e8311d6cde2` |
| CAP-377 | Continue Architecture Planning.md > v0.17 > 5. Locator | `54646a776e76192d` | `e02f5f676f7522b4` |
| CAP-378 | Continue Architecture Planning.md > v0.17 > 6. Resource | `d37ebc4c8620ac9a` | `82f027da68dd458c` |
| CAP-379 | Continue Architecture Planning.md > v0.17 > 7. Resource relationships | `7e42f991633a4430` | `bf3897580ec0f91a` |
| CAP-380 | Continue Architecture Planning.md > v0.17 > 8. Redirects | `9977e279ca87f8f5` | `2b65c19c2bb3f7af` |
| CAP-381 | Continue Architecture Planning.md > v0.17 > 9. Redirect chain | `deb5bbe993c1b0f9` | `0f5f9dfc9cb2cfdf` |
| CAP-382 | Continue Architecture Planning.md > v0.17 > 10. Content fingerprints | `31013b810c2d7bce` | `97909324ef8bb264` |
| CAP-383 | Continue Architecture Planning.md > v0.17 > 11. Same content does not prove same resource | `78ee3a6307f33aec` | `dcd25aebd9330a83` |
| CAP-384 | Continue Architecture Planning.md > v0.17 > 12. Representation identity | `2493f3e32fb3bf18` | `5cc84a4247f55c7e` |
| CAP-385 | Continue Architecture Planning.md > v0.17 > 13. Identity Evidence | `8b67c7a1a713a4e7` | `2122862a815b2b39` |
| CAP-386 | Continue Architecture Planning.md > v0.17 > 14. IdentityResolver | `9e29bb9cfc8ee2c8` | `38ab4627d4c19f66` |
| CAP-387 | Continue Architecture Planning.md > v0.17 > 15. Identity confidence should be relational | `082727104098c026` | `8226e16aee73ce4d` |
| CAP-388 | Continue Architecture Planning.md > v0.17 > 16. Identity classes | `e3dd7e872c2a7320` | `4e013fc31a5b83d1` |
| CAP-389 | Continue Architecture Planning.md > v0.17 > 17. No destructive merges | `1579e3eb7abbc6f4` | `a33edc0130bb0804` |
| CAP-390 | Continue Architecture Planning.md > v0.17 > 18. ResourceGraph | `16f2b0fbb024d263` | `86f8be602f5d06e9` |
| CAP-391 | Continue Architecture Planning.md > v0.17 > 19. Graph edge contract | `56ee27d7f7ae0d06` | `4568bc89fe33188b` |
| CAP-392 | Continue Architecture Planning.md > v0.17 > 20. Identity resolution pipeline | `f09b4d86b7c8c3f2` | `2d9328b14622fa74` |
| CAP-393 | Continue Architecture Planning.md > v0.17 > 21. Canonical URL is still important | `7ea26cdfe364aef3` | `f9d732ef66e630a6` |
| CAP-394 | Continue Architecture Planning.md > v0.17 > 22. Canonicalization provenance | `1a2fd593fbf180cf` | `d5804879fb2bc439` |
| CAP-395 | Continue Architecture Planning.md > v0.17 > 23. Identity resolution must be monotonic where possible | `65c3e065e9e26376` | `76392c9ac239d061` |
| CAP-396 | Continue Architecture Planning.md > v0.17 > 24. Resource revisions | `655dd569b13a0699` | `121eadf598f1de51` |
| CAP-397 | Continue Architecture Planning.md > v0.17 > 25. Revision object | `132aec7609c18747` | `f79141813c5bf348` |
| CAP-398 | Continue Architecture Planning.md > v0.17 > 26. ResourceGraph vs KnowledgeBase | `72713fa5322852f1` | `2c9c14b21472a393` |
| CAP-399 | Continue Architecture Planning.md > v0.17 > 27. Querying the graph | `00b4dd7c9d1a8d43` | `e22f058d0ebe3a62` |
| CAP-400 | Continue Architecture Planning.md > v0.17 > 27. Querying the graph > What URLs identify this resource? | `a85662f41315a34a` | `b7b8d73756e23521` |
| CAP-401 | Continue Architecture Planning.md > v0.17 > 27. Querying the graph > Where was it discovered? | `10ca6bf30ef412c2` | `ee8d1332e9f1e3a3` |
| CAP-402 | Continue Architecture Planning.md > v0.17 > 27. Querying the graph > What URLs redirect to it? | `b3f9857f55dd6f37` | `c7259163b17115dc` |
| CAP-403 | Continue Architecture Planning.md > v0.17 > 27. Querying the graph > Which URLs have identical observed bytes? | `f2b0d0cd8cc58422` | `9b749d27de6890eb` |
| CAP-404 | Continue Architecture Planning.md > v0.17 > 27. Querying the graph > Has this resource changed? | `23353475c75e42c1` | `d467b54aaa165fdb` |
| CAP-405 | Continue Architecture Planning.md > v0.17 > 27. Querying the graph > Why do we believe two URLs are related? | `d068d7e2b4a17ccf` | `8533ba9288a4c22d` |
| CAP-406 | Continue Architecture Planning.md > v0.17 > 28. Resource graph example | `b2cc4ed5ebda2944` | `63f356cf70302481` |
| CAP-407 | Continue Architecture Planning.md > v0.17 > 29. Failure taxonomy | `25eab0fb3f9b1adc` | `70a72b0d20ff7476` |
| CAP-408 | Continue Architecture Planning.md > v0.17 > 30. Core invariants | `f9e6d12d6b456ae9` | `c7e4bd62397e9c68` |
| CAP-409 | Continue Architecture Planning.md > v0.17 > 30. Core invariants > Locator preservation | `0b0dab23a13ffaf2` | `4393d685ff7439ac` |
| CAP-410 | Continue Architecture Planning.md > v0.17 > 30. Core invariants > No destructive merge | `d6a6ec911affc8ee` | `1f22754afeaddb79` |
| CAP-411 | Continue Architecture Planning.md > v0.17 > 30. Core invariants > Fingerprint independence | `567a6a7cf82383d2` | `04f7e1f1f20cb561` |
| CAP-412 | Continue Architecture Planning.md > v0.17 > 30. Core invariants > Redirect independence | `74cbfc3bd6ff4275` | `bbb591b1b77887e5` |
| CAP-413 | Continue Architecture Planning.md > v0.17 > 30. Core invariants > Evidence-backed identity | `9064aaaffca7a84c` | `013732e0d6903fb2` |
| CAP-414 | Continue Architecture Planning.md > v0.17 > 30. Core invariants > Revision preservation | `62b08ce201c191db` | `57e9a316ab1964eb` |
| CAP-415 | Continue Architecture Planning.md > v0.17 > 30. Core invariants > Canonicalization transparency | `ab286917ca17fce7` | `67179866fc0b0828` |
| CAP-416 | Continue Architecture Planning.md > v0.17 > 31. The new architecture | `191e8ac4ebb63204` | `e36891e104f438c1` |
| CAP-417 | Continue Architecture Planning.md > v0.17 > 32. The deeper model | `e9d92faeff5de7fc` | `942a3f47bc4f80d3` |
| CAP-418 | Continue Architecture Planning.md > v0.17 > 33. The important transition | `ce4d423c480e2c4b` | `e7819b3eb909d589` |
| CAP-419 | Continue Architecture Planning.md > v0.17 > 34. Next missing abstraction | `a0816db5e9107b23` | `0edfb11fe7952156` |
| CAP-420 | Continue Architecture Planning.md > v0.18 > v0.18 — Resource Type System + Semantic Classification | `3b3a44d7e3b047e7` | `1ff4a0204d7d9a5e` |
| CAP-421 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `31fbef162594de01` |
| CAP-422 | Continue Architecture Planning.md > v0.18 > v0.18 — Resource Type System + Semantic Classification | `3b3a44d7e3b047e7` | `0b74761bc6ceaa51` |
| CAP-423 | Continue Architecture Planning.md > v0.18 > 18.1 The Type Problem | `a24ef6476efc1387` | `013b47785cf59481` |
| CAP-424 | Continue Architecture Planning.md > v0.18 > 18.2 Four Orthogonal Type Dimensions | `38dbe123fffb9da7` | `32d34a69b3b9869a` |
| CAP-425 | Continue Architecture Planning.md > v0.18 > 18.3 ResourceType | `151d207b3d8be763` | `0ead61c0d070ff60` |
| CAP-426 | Continue Architecture Planning.md > v0.18 > 18.4 Classification Assertion | `d31197c4683e66a0` | `ced49583c882c22f` |
| CAP-427 | Continue Architecture Planning.md > v0.18 > 18.5 Type Evidence | `536b8a115d0f80db` | `8f1629935b60accd` |
| CAP-428 | Continue Architecture Planning.md > v0.18 > 18.6 Evidence Strength Must Be Axis-Specific | `48d6e3adc7ab0502` | `7c4083937ff12cd4` |
| CAP-429 | Continue Architecture Planning.md > v0.18 > 18.7 Classification Pipeline | `5f3f0e4760993c21` | `8d5e3631dbef6a94` |
| CAP-430 | Continue Architecture Planning.md > v0.18 > 18.8 Recognition vs Classification | `b3324e2ed9f5b7db` | `27667f5f9ca79926` |
| CAP-431 | Continue Architecture Planning.md > v0.18 > 18.8 Recognition vs Classification > Recognition | `22466b5a68ad045f` | `31f84a0d9fa641c1` |
| CAP-432 | Continue Architecture Planning.md > v0.18 > 18.8 Recognition vs Classification > Classification | `72f049954fdd06c8` | `699331505fd3b174` |
| CAP-433 | Continue Architecture Planning.md > v0.18 > 18.9 Classification Runtime | `c5ea5bd7e386f879` | `b8617f2d80263869` |
| CAP-434 | Continue Architecture Planning.md > v0.18 > 18.10 Example Classifiers | `8cbfe371b3ae9513` | `795b90eac9a3fc84` |
| CAP-435 | Continue Architecture Planning.md > v0.18 > 18.11 Hierarchical Classification | `4a5dd43acb24845a` | `a3b0e89871a2e32c` |
| CAP-436 | Continue Architecture Planning.md > v0.18 > 18.12 Do Not Use One Global Confidence Score | `baa15e12400c325f` | `438c68f9dade66f7` |
| CAP-437 | Continue Architecture Planning.md > v0.18 > 18.13 Classification Is Versioned | `7c3cdbd581908409` | `7ed50d97ec5291b4` |
| CAP-438 | Continue Architecture Planning.md > v0.18 > 18.14 Contradictory Classification | `2a9028e6ac92186d` | `97fa938a544a9ea6` |
| CAP-439 | Continue Architecture Planning.md > v0.18 > 18.15 Classification Graph | `68a02ffd8eaa511e` | `c14bda96bff7c620` |
| CAP-440 | Continue Architecture Planning.md > v0.18 > 18.16 Resource Model After v0.18 | `1d705929f53cc00c` | `19d845d4b7a0312d` |
| CAP-441 | Continue Architecture Planning.md > v0.18 > 18.17 Resource Type Registry | `b9e31476c3b3a9bf` | `7dd78025fa389184` |
| CAP-442 | Continue Architecture Planning.md > v0.18 > 18.18 Classification Must Not Become Acquisition Policy | `6b3d61c592642f09` | `e154ea6db95233ea` |
| CAP-443 | Continue Architecture Planning.md > v0.18 > 18.19 Classification → Strategy | `2725258adb72dc07` | `10e5f701acced142` |
| CAP-444 | Continue Architecture Planning.md > v0.18 > 18.20 Classification Work as WorkItem | `209d2051ac4febb5` | `14417ea2b4203b11` |
| CAP-445 | Continue Architecture Planning.md > v0.18 > 18.21 End-to-End Architecture | `8224a90937412d94` | `3fd1d0fd8d9acab7` |
| CAP-446 | Continue Architecture Planning.md > v0.18 > 18.22 Failure Taxonomy | `44901ea1535122f7` | `6491ebe754a359f8` |
| CAP-447 | Continue Architecture Planning.md > v0.18 > 18.23 Core Invariants | `daa289dafd2562d1` | `7b76908235fc9fd1` |
| CAP-448 | Continue Architecture Planning.md > v0.18 > 18.23 Core Invariants > Invariant 1 — Type is not identity | `4f98959c9de8d7c9` | `6484f7f04e1bae3b` |
| CAP-449 | Continue Architecture Planning.md > v0.18 > 18.23 Core Invariants > Invariant 2 — URL does not determine semantic type | `7759fdee3c16ffed` | `7c8e78e0bf221b48` |
| CAP-450 | Continue Architecture Planning.md > v0.18 > 18.23 Core Invariants > Invariant 3 — Technical recognition does not determine semantic role | `6f9c90f126c2632a` | `57bc8460e43fcf8e` |
| CAP-451 | Continue Architecture Planning.md > v0.18 > 18.23 Core Invariants > Invariant 4 — Classification requires evidence | `2735319e7e487629` | `3a9055de1d768743` |
| CAP-452 | Continue Architecture Planning.md > v0.18 > 18.23 Core Invariants > Invariant 5 — Classification does not imply authorization | `50ef40bc017d5061` | `a03dad015cd506fa` |
| CAP-453 | Continue Architecture Planning.md > v0.18 > 18.23 Core Invariants > Invariant 6 — Historical classification is immutable | `33f98c4f654e018a` | `ccc87ea6abd1e917` |
| CAP-454 | Continue Architecture Planning.md > v0.18 > 18.23 Core Invariants > Invariant 7 — Contradiction is preserved | `beca1d47bb6fdb62` | `86b4cd0e9c061911` |
| CAP-455 | Continue Architecture Planning.md > v0.18 > 18.23 Core Invariants > Invariant 8 — Type axes remain independent | `f29475809ff6a640` | `9c53b04e137e2774` |
| CAP-456 | Continue Architecture Planning.md > v0.18 > 18.24 The Larger Concept | `a766b7b1192483d5` | `d840bcc1c9890e96` |
| CAP-457 | Continue Architecture Planning.md > v0.19 > v0.19 — Resource Representation & Revision Model | `fe561126e4f94299` | `7761bfffb3f5ae5b` |
| CAP-458 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `31fbef162594de01` |
| CAP-459 | Continue Architecture Planning.md > v0.19 > v0.19 — Resource Representation + Artifact + Revision Model | `2ed169c1b3c11f96` | `20eb5e23084f4803` |
| CAP-460 | Continue Architecture Planning.md > v0.19 > v0.19 — Resource Representation + Artifact + Revision Model > 19.1 The Core Distinction | `4f54ec493c46737a` | `19c04e4694c55cc1` |
| CAP-461 | Continue Architecture Planning.md > v0.19 > v0.19 — Resource Representation + Artifact + Revision Model > 19.1 The Core Distinction > Resource | `eb7a842ff958c49c` | `0b066a3213942f9b` |
| CAP-462 | Continue Architecture Planning.md > v0.19 > v0.19 — Resource Representation + Artifact + Revision Model > 19.1 The Core Distinction > Representation | `15ecda5bfdb815c1` | `395c7dca71d7115b` |
| CAP-463 | Continue Architecture Planning.md > v0.19 > v0.19 — Resource Representation + Artifact + Revision Model > 19.1 The Core Distinction > Artifact | `e06171a1c467f2d4` | `31299ef6493dd2d2` |
| CAP-464 | Continue Architecture Planning.md > v0.19 > v0.19 — Resource Representation + Artifact + Revision Model > 19.1 The Core Distinction > Observation | `d239e9cf6a51335b` | `0eb4afe3264af328` |
| CAP-465 | Continue Architecture Planning.md > v0.19 > 19.2 Why Resource → Artifact Is Wrong | `b91547021a68b8b4` | `d28f11bcf957d08c` |
| CAP-466 | Continue Architecture Planning.md > v0.19 > 19.3 New Data Model | `3b20052035ba9e52` | `3944e992b256cf7a` |
| CAP-467 | Continue Architecture Planning.md > v0.19 > 19.4 The Complete Identity Chain | `9b8fdc13e4325d33` | `db8dbf21fa3c97bf` |
| CAP-468 | Continue Architecture Planning.md > v0.19 > 19.5 Representation Is Not Just MIME | `298a6280c8cbe2e9` | `632690ccc11122fc` |
| CAP-469 | Continue Architecture Planning.md > v0.19 > 19.6 Representation Relations | `ae1b5d90ed5ed81c` | `1becf9e0c8ad68d1` |
| CAP-470 | Continue Architecture Planning.md > v0.19 > 19.7 Artifact Identity | `16b015b717a24d3a` | `acc71c2e3acdfd16` |
| CAP-471 | Continue Architecture Planning.md > v0.19 > 19.8 Content Equivalence | `2faa2add2afc8f1d` | `d33954e5a0e301f4` |
| CAP-472 | Continue Architecture Planning.md > v0.19 > 19.9 Revision Detection | `2cbd6afdb24ee598` | `3381e6c9de3da85e` |
| CAP-473 | Continue Architecture Planning.md > v0.19 > 19.10 Revision Detection Is Not Always Proof of Semantic Revision | `192399f9b2e16aa0` | `ae370dc3aa59d275` |
| CAP-474 | Continue Architecture Planning.md > v0.19 > 19.11 Revision Evidence | `acece22720a9aa47` | `e393fa667306ea7b` |
| CAP-475 | Continue Architecture Planning.md > v0.19 > 19.12 HTTP Validators Become Evidence | `3a295aece3375b7a` | `385189ecd6e4ea63` |
| CAP-476 | Continue Architecture Planning.md > v0.19 > 19.13 Conditional Acquisition | `ac98674c23d68a3f` | `27773af558033385` |
| CAP-477 | Continue Architecture Planning.md > v0.19 > 19.14 Observation Becomes the Historical Bridge | `4e7f693eed480193` | `f9e65da535eca382` |
| CAP-478 | Continue Architecture Planning.md > v0.19 > 19.15 Resource State vs Artifact State | `f7d539c395ebe057` | `acdea065f098928a` |
| CAP-479 | Continue Architecture Planning.md > v0.19 > 19.15 Resource State vs Artifact State > Resource state | `1ef1dc8338203ef6` | `2977a4c9807f965b` |
| CAP-480 | Continue Architecture Planning.md > v0.19 > 19.15 Resource State vs Artifact State > Artifact state | `85ef858837932259` | `54faad08bad07ace` |
| CAP-481 | Continue Architecture Planning.md > v0.19 > 19.15 Resource State vs Artifact State > Observation state | `059439cbaa57c0a2` | `557e18ec02e82a67` |
| CAP-482 | Continue Architecture Planning.md > v0.19 > 19.16 ResourceGraph v0.19 | `736d8c2c51659083` | `a4d74c2e5ecb2e23` |
| CAP-483 | Continue Architecture Planning.md > v0.19 > 19.17 ResourceGraph API | `2bfb05da4f180a8f` | `f2f99aec1131310c` |
| CAP-484 | Continue Architecture Planning.md > v0.19 > 19.18 Artifact Deduplication | `d4f7448f62203919` | `e4e72cf6137b4ac7` |
| CAP-485 | Continue Architecture Planning.md > v0.19 > 19.18 Artifact Deduplication > Locator deduplication | `ceb2d6b316e3aa2f` | `0e104256012403e2` |
| CAP-486 | Continue Architecture Planning.md > v0.19 > 19.18 Artifact Deduplication > Artifact deduplication | `282b2479f4ecbd92` | `829c8c26430f4da9` |
| CAP-487 | Continue Architecture Planning.md > v0.19 > 19.19 Content-Addressed Storage | `b0a1b66f89e85450` | `39e15c6a35a11866` |
| CAP-488 | Continue Architecture Planning.md > v0.19 > 19.20 Verification Levels | `81fa0243c16b8a25` | `d077595014454dd6` |
| CAP-489 | Continue Architecture Planning.md > v0.19 > 19.21 Independent Confirmation | `c4df7d9cc616eaa1` | `9695fdab51ef0ff9` |
| CAP-490 | Continue Architecture Planning.md > v0.19 > 19.22 Resource Confidence | `148c7ffc4575753e` | `488fa8046bd6d258` |
| CAP-491 | Continue Architecture Planning.md > v0.19 > 19.23 Example | `c5144b71466e9ea5` | `f44390bcc33d6fd4` |
| CAP-492 | Continue Architecture Planning.md > v0.19 > 19.23 Example > Step 1 — Locator | `3726a766db6f8371` | `e2ce10ae205a128a` |
| CAP-493 | Continue Architecture Planning.md > v0.19 > 19.23 Example > Step 2 — Resource | `894424656ffd8b64` | `cdd617c8100a3bad` |
| CAP-494 | Continue Architecture Planning.md > v0.19 > 19.23 Example > Step 3 — Observation | `3f9b41acb6e9b9e9` | `2ce9397e7af8c122` |
| CAP-495 | Continue Architecture Planning.md > v0.19 > 19.23 Example > Step 4 — Artifact | `3702782ca18b7bd0` | `00019acec3f0d39e` |
| CAP-496 | Continue Architecture Planning.md > v0.19 > 19.23 Example > Step 5 — Representation | `ac581fb8908f82d8` | `a2ffb04f0950c27b` |
| CAP-497 | Continue Architecture Planning.md > v0.19 > 19.23 Example > Step 6 — Classification | `19a97b863fd98f30` | `4a9c3d77a44e1568` |
| CAP-498 | Continue Architecture Planning.md > v0.19 > 19.23 Example > Step 7 — Revision | `d0fc12ddc1894df5` | `10f2e98cc7f3fe3a` |
| CAP-499 | Continue Architecture Planning.md > v0.19 > 19.24 A More Precise End-to-End Pipeline | `ebfa1350b3bef096` | `69847c05913a1b5c` |
| CAP-500 | Continue Architecture Planning.md > v0.19 > 19.25 New Invariants | `3c45d08eb63411e2` | `f9fd6bbaf14c0359` |
| CAP-501 | Continue Architecture Planning.md > v0.19 > 19.25 New Invariants > Artifact invariant | `9be19d3e174c62a3` | `c066822a06cf276f` |
| CAP-502 | Continue Architecture Planning.md > v0.19 > 19.25 New Invariants > Resource invariant | `f42a5178d50a26a8` | `5f698817d8836139` |
| CAP-503 | Continue Architecture Planning.md > v0.19 > 19.25 New Invariants > Representation invariant | `c3fe215c46845cb6` | `23465f8a8940140f` |
| CAP-504 | Continue Architecture Planning.md > v0.19 > 19.25 New Invariants > Revision invariant | `25d85c9270a48437` | `231818635c845d84` |
| CAP-505 | Continue Architecture Planning.md > v0.19 > 19.25 New Invariants > Observation invariant | `c561d687ee54e6aa` | `f48ff384bb66300f` |
| CAP-506 | Continue Architecture Planning.md > v0.19 > 19.25 New Invariants > Deduplication invariant | `82be7a77d2870494` | `01062f27d0669bdc` |
| CAP-507 | Continue Architecture Planning.md > v0.19 > 19.25 New Invariants > Change invariant | `ffd4cf39205730d4` | `8e1d93492355773f` |
| CAP-508 | Continue Architecture Planning.md > v0.19 > 19.25 New Invariants > Classification invariant | `a1e15125ec9d1d8d` | `2629b98dfc41746a` |
| CAP-509 | Continue Architecture Planning.md > v0.19 > 19.26 Failure Modes | `1debc20de5f7cd2e` | `d6cfdf602a9b65f4` |
| CAP-510 | Continue Architecture Planning.md > v0.19 > 19.27 What v0.19 Gives Us | `60b69e519ac33e9a` | `5c156c4b7dfbcaaa` |
| CAP-511 | Continue Architecture Planning.md > v0.19 > 19.27 What v0.19 Gives Us > Next boundary: v0.20 — Search-Space Partitioning + Discovery Strategies | `bb14e0fd2fa94079` | `bd2a2e1e5eb53115` |
| CAP-512 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `31fbef162594de01` |
| CAP-513 | Continue Architecture Planning.md > v0.20 > v0.20 — Search-Space Partitioning + Discovery Strategies | `c9bc63697999ee8e` | `9264e26132342ebe` |
| CAP-514 | Continue Architecture Planning.md > v0.20 > 20.1 The Search Space | `71fe2b8b71499de1` | `d9f9ccedd9648641` |
| CAP-515 | Continue Architecture Planning.md > v0.20 > 20.2 What Is a Partition? | `b230a2391b425a91` | `b66f8807b48027d0` |
| CAP-516 | Continue Architecture Planning.md > v0.20 > 20.3 Partition ≠ Candidate | `ce52a168078394c0` | `e53c0e0fbe14f757` |
| CAP-517 | Continue Architecture Planning.md > v0.20 > 20.4 Partition Object | `8d9fc23776213def` | `b908203e43833156` |
| CAP-518 | Continue Architecture Planning.md > v0.20 > 20.5 Partition State | `acbf319c3753d0d1` | `c4c209a9ea9b9ed4` |
| CAP-519 | Continue Architecture Planning.md > v0.20 > 20.5 Partition State > Saturated | `ca707893aaf9b56c` | `fb1b1df3d43fe79b` |
| CAP-520 | Continue Architecture Planning.md > v0.20 > 20.5 Partition State > Exhausted | `a51ee30495b32b91` | `fc940901a4d5e3d8` |
| CAP-521 | Continue Architecture Planning.md > v0.20 > 20.6 Search Coverage | `335c405bcb1b5e7b` | `e6545d8d275628a6` |
| CAP-522 | Continue Architecture Planning.md > v0.20 > 20.7 Strategy Contract | `a39f2617648bfc08` | `8e176e3403588a26` |
| CAP-523 | Continue Architecture Planning.md > v0.20 > 20.8 Strategy vs Candidate Source | `a3b83a2baa773211` | `d257c0c88c127d2d` |
| CAP-524 | Continue Architecture Planning.md > v0.20 > 20.9 Strategy Types | `bc1face88ceccf21` | `38084024fd1a9b89` |
| CAP-525 | Continue Architecture Planning.md > v0.20 > 20.9 Strategy Types > Seed Expansion | `71e28883db9f0c8d` | `e7cfc3280da0908a` |
| CAP-526 | Continue Architecture Planning.md > v0.20 > 20.9 Strategy Types > Repository Expansion | `8752036e8e6dcc1c` | `cc3e30731056474c` |
| CAP-527 | Continue Architecture Planning.md > v0.20 > 20.9 Strategy Types > Sitemap Expansion | `77d40de28416c5e0` | `7e1744b410e7ea49` |
| CAP-528 | Continue Architecture Planning.md > v0.20 > 20.9 Strategy Types > API Schema Expansion | `0608e94f288a62c2` | `70ad2f14f9f87079` |
| CAP-529 | Continue Architecture Planning.md > v0.20 > 20.9 Strategy Types > Document-Family Expansion | `d920295821827076` | `4139b826d8c9ca0c` |
| CAP-530 | Continue Architecture Planning.md > v0.20 > 20.10 Blind-Scan Analogy | `1f282895d65167de` | `d58a99acf175e7c0` |
| CAP-531 | Continue Architecture Planning.md > v0.20 > 20.11 Probe | `090322852985dde1` | `2fa109350f5b38f8` |
| CAP-532 | Continue Architecture Planning.md > v0.20 > 20.12 Exploration Plan | `084115b33f827a88` | `ac4db8c46a8b0da2` |
| CAP-533 | Continue Architecture Planning.md > v0.20 > 20.13 Exploration Must Remain Budgeted | `55330d67e275bc80` | `2ac6a9732230432d` |
| CAP-534 | Continue Architecture Planning.md > v0.20 > 20.14 Adaptive Partition Priority | `0f0fd287e46dd97c` | `e2e9f5c86be5b375` |
| CAP-535 | Continue Architecture Planning.md > v0.20 > 20.15 Exploration vs Exploitation | `b0b37688f38be675` | `2ae022035e5dd508` |
| CAP-536 | Continue Architecture Planning.md > v0.20 > 20.16 Aging | `98c1eeaf466cde6d` | `efa51801c196c5d8` |
| CAP-537 | Continue Architecture Planning.md > v0.20 > 20.17 Partition Splitting | `789f20925ebc5f99` | `a49e1ad118fb1134` |
| CAP-538 | Continue Architecture Planning.md > v0.20 > 20.18 Partition Merge | `49fe4f0f42a8f92f` | `9215400c030196c1` |
| CAP-539 | Continue Architecture Planning.md > v0.20 > 20.19 Partition Graph | `5ba3aae0993531ca` | `a40fb769b3183df5` |
| CAP-540 | Continue Architecture Planning.md > v0.20 > 20.20 SearchSpace | `9823468d343d584f` | `7dbe7be1566bb53a` |
| CAP-541 | Continue Architecture Planning.md > v0.20 > 20.21 Search-Space Controller | `064ed7251ba26649` | `913f3b5cf4552221` |
| CAP-542 | Continue Architecture Planning.md > v0.20 > 20.22 Three-Level Control Plane | `f2dad287cde50e0c` | `ce2899eeac9e543a` |
| CAP-543 | Continue Architecture Planning.md > v0.20 > 20.23 Candidate Sources Remain Low-Level | `cc3468524045bf5f` | `ab4fad392f272285` |
| CAP-544 | Continue Architecture Planning.md > v0.20 > 20.24 Termination Becomes More Sophisticated | `f712448a23f3b14b` | `11c57f7f12e23e4a` |
| CAP-545 | Continue Architecture Planning.md > v0.20 > 20.25 Saturation | `cdaed04abbd4f7d8` | `6462d9abf73142e0` |
| CAP-546 | Continue Architecture Planning.md > v0.20 > 20.26 Partition Statistics | `262d8958d2cda483` | `fa16df8485ae4522` |
| CAP-547 | Continue Architecture Planning.md > v0.20 > 20.27 Discovery Efficiency | `790b9f223d75e680` | `a7c833c810ab7e98` |
| CAP-548 | Continue Architecture Planning.md > v0.20 > 20.28 Failure Modes | `dee0753331d96eb7` | `ab885c050cf1d5e5` |
| CAP-549 | Continue Architecture Planning.md > v0.20 > 20.29 Core Invariants | `5b8c196802a5604d` | `318d2d9a69629ce6` |
| CAP-550 | Continue Architecture Planning.md > v0.20 > 20.29 Core Invariants > Search-space invariant | `b50232fb7df514cb` | `294c6d90503308da` |
| CAP-551 | Continue Architecture Planning.md > v0.20 > 20.29 Core Invariants > Strategy invariant | `af70de4aa9a8a26e` | `e5350d6a63e412b0` |
| CAP-552 | Continue Architecture Planning.md > v0.20 > 20.29 Core Invariants > Acquisition invariant | `a4aacdac7065e23a` | `8c1e12ccac633cfd` |
| CAP-553 | Continue Architecture Planning.md > v0.20 > 20.29 Core Invariants > Partition invariant | `1ec2ecd8181904a5` | `02b9cff60c545d7b` |
| CAP-554 | Continue Architecture Planning.md > v0.20 > 20.29 Core Invariants > Coverage invariant | `1a8737e63fc57673` | `3a7d48e618a94a42` |
| CAP-555 | Continue Architecture Planning.md > v0.20 > 20.29 Core Invariants > Discovery invariant | `3ae3c840bf249a3a` | `27aed8a6dc216be1` |
| CAP-556 | Continue Architecture Planning.md > v0.20 > 20.30 The Architecture After v0.20 | `6129992f38fae995` | `dcc0550d9c910e31` |
| CAP-557 | Continue Architecture Planning.md > v0.20 > 20.31 The DVB Analogy Is Now Structural | `1820e44c6c402b11` | `95ee7b66f40eac59` |
| CAP-558 | Continue Architecture Planning.md > v0.21 > v0.21 — Discovery Strategy Learning / Adaptive Search | `34b84a33a6b44d40` | `c334607ee5b2a85f` |
| CAP-559 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `31fbef162594de01` |
| CAP-560 | Continue Architecture Planning.md > v0.21 > v0.21 — Adaptive Discovery Strategy | `98f1a4e864fa29b3` | `28f324fafa79d0ad` |
| CAP-561 | Continue Architecture Planning.md > v0.21 > 21.1 The Adaptive Loop | `0e9377bc0c85c126` | `5e0980971763b6f8` |
| CAP-562 | Continue Architecture Planning.md > v0.21 > 21.2 Strategy Performance Record | `97c687f711bf01b7` | `c1c3430917d34142` |
| CAP-563 | Continue Architecture Planning.md > v0.21 > 21.3 Yield Metrics | `fe28bb91f4a1e943` | `572d7bcd025dbea7` |
| CAP-564 | Continue Architecture Planning.md > v0.21 > 21.4 Strategy Score | `1008d3d3c4d7c812` | `5755b3d9a08f915b` |
| CAP-565 | Continue Architecture Planning.md > v0.21 > 21.5 Cold Start Problem | `25145f5a4ac8d54e` | `d682a06a6ab0cd24` |
| CAP-566 | Continue Architecture Planning.md > v0.21 > 21.6 Exploration Quota | `b7d4845f395f430b` | `4b569b7c2ae79c0f` |
| CAP-567 | Continue Architecture Planning.md > v0.21 > 21.7 Strategy Selection Must Be Constrained | `efc1d91af4e0e4b4` | `514f25a5df3a4297` |
| CAP-568 | Continue Architecture Planning.md > v0.21 > 21.8 Strategy Eligibility | `6a0ced10a8bdfb5a` | `ee9e6c6d34e805ce` |
| CAP-569 | Continue Architecture Planning.md > v0.21 > 21.9 Temporary vs Permanent Failure | `2a5445d19d7a8092` | `4720b15c60e30193` |
| CAP-570 | Continue Architecture Planning.md > v0.21 > 21.10 Strategy Outcome | `4ca74da30053a0a5` | `3eddd280b954f961` |
| CAP-571 | Continue Architecture Planning.md > v0.21 > 21.11 Strategy Outcome ≠ Strategy Truth | `789f1722a015576f` | `3a864fb2cfde88b0` |
| CAP-572 | Continue Architecture Planning.md > v0.21 > 21.12 Novelty | `25559ce80438469d` | `0b0b5b6595ed5961` |
| CAP-573 | Continue Architecture Planning.md > v0.21 > 21.13 Frontier Expansion Value | `6ebbf2d5515f0979` | `4284fcd97f4dcb14` |
| CAP-574 | Continue Architecture Planning.md > v0.21 > 21.14 Frontier Expansion Metric | `c77a3853a7851aab` | `ff71b2ce11c2a50f` |
| CAP-575 | Continue Architecture Planning.md > v0.21 > 21.15 Strategy Memory | `b08703714898636f` | `5f1222e154431a87` |
| CAP-576 | Continue Architecture Planning.md > v0.21 > 21.16 Hierarchical Priors | `dfe2a86e35eeef70` | `dc1298486214e640` |
| CAP-577 | Continue Architecture Planning.md > v0.21 > 21.17 Discovery Strategy Ledger | `90e30db80d50c291` | `7be49ae998d94558` |
| CAP-578 | Continue Architecture Planning.md > v0.21 > 21.18 Deterministic Replay | `0172f1a9181ad50f` | `7f4105e6a21fb359` |
| CAP-579 | Continue Architecture Planning.md > v0.21 > 21.19 Random Exploration | `9de3fd5ab45dd47f` | `57ee203b8c5fdd5a` |
| CAP-580 | Continue Architecture Planning.md > v0.21 > 21.20 Learning Must Not Modify Safety Boundaries | `34c8c15da053904f` | `29b997ebb55b93e3` |
| CAP-581 | Continue Architecture Planning.md > v0.21 > 21.21 Adaptive Discovery Controller | `b4abb054cc47fcfc` | `1ac49306718aa890` |
| CAP-582 | Continue Architecture Planning.md > v0.21 > 21.22 Tie-Breaking Must Be Deterministic | `975f4b36c03a4c66` | `95c7a092e59da15a` |
| CAP-583 | Continue Architecture Planning.md > v0.21 > 21.23 Performance Decay | `0d27e311f56002c7` | `a2aa88da1a9a6554` |
| CAP-584 | Continue Architecture Planning.md > v0.21 > 21.24 Strategy Adaptation and Scan Sessions | `09765fd491ebeb5d` | `a21cf0c1e360211c` |
| CAP-585 | Continue Architecture Planning.md > v0.21 > 21.25 Search Strategy as a First-Class Graph Node | `2e0cc32480eec025` | `5c07206bc44b79ce` |
| CAP-586 | Continue Architecture Planning.md > v0.21 > 21.26 Search Decision Graph | `2a5b5ddaad365deb` | `6db726adee274bf7` |
| CAP-587 | Continue Architecture Planning.md > v0.21 > 21.27 Two Kinds of Provenance | `e9c796369ca9772d` | `689887c2efbb077d` |
| CAP-588 | Continue Architecture Planning.md > v0.21 > 21.28 Failure Taxonomy | `74dbbba51daf76ad` | `7fee354ed4753135` |
| CAP-589 | Continue Architecture Planning.md > v0.21 > 21.29 Invariants | `f7a1f612b6ef5680` | `cb9ac745cc044fc4` |
| CAP-590 | Continue Architecture Planning.md > v0.21 > 21.29 Invariants > Safety invariant | `b14fa5737afdd4dc` | `22300e8f75ceb485` |
| CAP-591 | Continue Architecture Planning.md > v0.21 > 21.29 Invariants > Capability invariant | `b1dc87a33c81e06a` | `3389dd8e1d09ba3d` |
| CAP-592 | Continue Architecture Planning.md > v0.21 > 21.29 Invariants > Domain invariant | `f59d566824f84afb` | `aaf8f248d68a577a` |
| CAP-593 | Continue Architecture Planning.md > v0.21 > 21.29 Invariants > Exploration invariant | `35aaa6b11547c5c1` | `4e6056521e3da1f0` |
| CAP-594 | Continue Architecture Planning.md > v0.21 > 21.29 Invariants > Historical invariant | `e73052c9acd3d89e` | `f2c419504c776a14` |
| CAP-595 | Continue Architecture Planning.md > v0.21 > 21.29 Invariants > Replay invariant | `d9605286f736f106` | `979773fe38f65316` |
| CAP-596 | Continue Architecture Planning.md > v0.21 > 21.29 Invariants > Provenance invariant | `8aba9c8e873e0baa` | `6741cda7add599e7` |
| CAP-597 | Continue Architecture Planning.md > v0.21 > 21.30 Architecture After v0.21 | `b9958785c9c1cd45` | `7c019216c9f48ec1` |
| CAP-598 | Continue Architecture Planning.md > v0.21 > 21.31 The Important Conceptual Shift | `ef96b18641e5b466` | `4670b5c7438340bc` |
| CAP-599 | Continue Architecture Planning.md > v0.22 > v0.22 — Discovery Completeness + Coverage Claims | `8588d4359f7d6546` | `9ad35c81f95c6a4e` |
| CAP-600 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `31fbef162594de01` |
| CAP-601 | Continue Architecture Planning.md > v0.22 > v0.22 — Discovery Completeness + Coverage Claims | `8588d4359f7d6546` | `a2dd6b725edc2f80` |
| CAP-602 | Continue Architecture Planning.md > v0.22 > v0.22 — Discovery Completeness + Coverage Claims > 22.1 The problem | `b07850dfa6d1f0c6` | `0a974b9ee421d081` |
| CAP-603 | Continue Architecture Planning.md > v0.22 > 22.2 Search-space state model | `b489d890ba43d9fc` | `ac776249acdd312d` |
| CAP-604 | Continue Architecture Planning.md > v0.22 > 22.3 Coverage is a measurement | `2280044ce7ab8784` | `8b96d13e3a831864` |
| CAP-605 | Continue Architecture Planning.md > v0.22 > 22.4 Coverage dimensions | `df03708a993a02d6` | `551a73f91139ff4c` |
| CAP-606 | Continue Architecture Planning.md > v0.22 > 22.5 CoverageRecord | `3481b041b7cc2598` | `215f798176dc6a1f` |
| CAP-607 | Continue Architecture Planning.md > v0.22 > 22.6 Coverage state | `e9faea1fd719f28f` | `f3f0da8047f99ac2` |
| CAP-608 | Continue Architecture Planning.md > v0.22 > 22.7 CoverageClaim | `33eab8f62a59c908` | `5b8cb06b6197217f` |
| CAP-609 | Continue Architecture Planning.md > v0.22 > 22.8 Completeness is a stronger assertion | `7e152e36c2787d8a` | `55b0ccfd8ef34de7` |
| CAP-610 | Continue Architecture Planning.md > v0.22 > 22.9 The finite-enumerator case | `75b30cafe426f828` | `c36558e9707fe692` |
| CAP-611 | Continue Architecture Planning.md > v0.22 > 22.10 Enumeration contract | `e927a9589640a7d9` | `2cf04836c7f0a6db` |
| CAP-612 | Continue Architecture Planning.md > v0.22 > 22.11 Negative evidence | `1d8be6f0eacd9a92` | `b5557d137620f097` |
| CAP-613 | Continue Architecture Planning.md > v0.22 > 22.12 Absence reasoning hierarchy | `e698eb9314f82b35` | `86c6198cf004690d` |
| CAP-614 | Continue Architecture Planning.md > v0.22 > 22.13 “Not found” becomes a first-class result | `efcfdbe9afcdc2df` | `0293f32b90e47bc7` |
| CAP-615 | Continue Architecture Planning.md > v0.22 > 22.14 Coverage cannot necessarily be monotonically interpreted | `ebf54648c75a7b42` | `1684bb57a491fd67` |
| CAP-616 | Continue Architecture Planning.md > v0.22 > 22.15 Version the search universe | `b9b4564f799ba2c4` | `3d76bf0a5399cea6` |
| CAP-617 | Continue Architecture Planning.md > v0.22 > 22.16 Coverage ledger | `3c6b32064a09c613` | `f4ce35e37efa19b9` |
| CAP-618 | Continue Architecture Planning.md > v0.22 > 22.17 Three graphs now interact | `49a28978b78a8ad6` | `40b760296392d145` |
| CAP-619 | Continue Architecture Planning.md > v0.22 > 22.18 Completeness assessment | `c7ce1a588131ec7b` | `dd94193ea2175f28` |
| CAP-620 | Continue Architecture Planning.md > v0.22 > 22.19 Assurance levels | `b9fd73c503228813` | `ffd1f185cbc66987` |
| CAP-621 | Continue Architecture Planning.md > v0.22 > 22.20 Search completeness matrix | `9acf51863563582a` | `2d61f95148fb95b7` |
| CAP-622 | Continue Architecture Planning.md > v0.22 > 22.21 Coverage calculation | `386cd025e226554d` | `c71b81b70948c7de` |
| CAP-623 | Continue Architecture Planning.md > v0.22 > 22.22 Coverage should be query-relative | `3911545c55c2285e` | `6e8a5cd3baf26129` |
| CAP-624 | Continue Architecture Planning.md > v0.22 > 22.23 Failure taxonomy | `8f09b8c4b4f15fa8` | `1f76718043699104` |
| CAP-625 | Continue Architecture Planning.md > v0.22 > 22.24 Core invariants | `4fa2c793e827677e` | `d657e9a5acc5410f` |
| CAP-626 | Continue Architecture Planning.md > v0.22 > 22.24 Core invariants > Invariant 1 | `0f3f4cf90daef9a8` | `d85aa6d6f9093a36` |
| CAP-627 | Continue Architecture Planning.md > v0.22 > 22.24 Core invariants > Invariant 2 | `c83ee83a00023944` | `134377126d463ab8` |
| CAP-628 | Continue Architecture Planning.md > v0.22 > 22.24 Core invariants > Invariant 3 | `ff318fcf8271d879` | `ca67ec1c278d0cb5` |
| CAP-629 | Continue Architecture Planning.md > v0.22 > 22.24 Core invariants > Invariant 4 | `e1ce66c44f570280` | `bcfd5f9de25a5ac2` |
| CAP-630 | Continue Architecture Planning.md > v0.22 > 22.24 Core invariants > Invariant 5 | `bb6067b9e33d7d05` | `fb39abd2d65c9c97` |
| CAP-631 | Continue Architecture Planning.md > v0.22 > 22.24 Core invariants > Invariant 6 | `2c06117f40c5939b` | `aa819dc1a3438a71` |
| CAP-632 | Continue Architecture Planning.md > v0.22 > 22.24 Core invariants > Invariant 7 | `c5fcb7f01e3fb674` | `9961ba6e4283a02e` |
| CAP-633 | Continue Architecture Planning.md > v0.22 > 22.24 Core invariants > Invariant 8 | `146d14f1f195c362` | `41f031d6c415c230` |
| CAP-634 | Continue Architecture Planning.md > v0.22 > 22.24 Core invariants > Invariant 9 | `da37a2b4721d9966` | `423e380758fb7bb2` |
| CAP-635 | Continue Architecture Planning.md > v0.22 > 22.24 Core invariants > Invariant 10 | `16657d5a1eb43a15` | `44fe39c0ffbbd124` |
| CAP-636 | Continue Architecture Planning.md > v0.22 > 22.25 v0.22 architecture | `04c700ac3e6a0caf` | `3a4724fcd879f90a` |
| CAP-637 | Continue Architecture Planning.md > v0.22 > 22.26 The conceptual jump | `4548ff31c5c1b908` | `d2c1bdf16d5614d4` |
| CAP-638 | Continue Architecture Planning.md > v0.23 > v0.23 — Negative Evidence + Absence Reasoning | `29f205f695089a2a` | `af3783e5c7648443` |
| CAP-639 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `31fbef162594de01` |
| CAP-640 | Continue Architecture Planning.md > v0.23 > v0.23 — Negative Evidence + Absence Reasoning | `29f205f695089a2a` | `553db7359fe8e954` |
| CAP-641 | Continue Architecture Planning.md > v0.23 > v0.23 — Negative Evidence + Absence Reasoning > 23.1 The absence problem | `88c61d31471e0172` | `62899321c92c4e4f` |
| CAP-642 | Continue Architecture Planning.md > v0.23 > 23.2 Four fundamental states | `d42c95f56158d1e4` | `806a3dffc433f996` |
| CAP-643 | Continue Architecture Planning.md > v0.23 > 23.3 PresenceAssertion | `d5587c385f07c80c` | `b57dca351196f1f9` |
| CAP-644 | Continue Architecture Planning.md > v0.23 > 23.4 Absence is always scoped | `c2fa5ed5d7609a8e` | `d3360627eb7a96d0` |
| CAP-645 | Continue Architecture Planning.md > v0.23 > 23.5 NegativeEvidence | `53178f950d2600bb` | `7b1bc2b1eb797048` |
| CAP-646 | Continue Architecture Planning.md > v0.23 > 23.6 Absence strength | `9276760cca1456bf` | `6c43a980a10bedfa` |
| CAP-647 | Continue Architecture Planning.md > v0.23 > 23.7 Search failure must not become negative evidence automatically | `ffd7bfd20ab95ebb` | `d2ae2219286b1894` |
| CAP-648 | Continue Architecture Planning.md > v0.23 > 23.8 Failure → evidence mapping | `5557c25980f74a55` | `14a334028bdf638f` |
| CAP-649 | Continue Architecture Planning.md > v0.23 > 23.9 Exact locator absence | `86de52299d6ee585` | `b734bc97dc175787` |
| CAP-650 | Continue Architecture Planning.md > v0.23 > 23.10 Claims need predicates | `7b007b4ba75ade96` | `a35607bf04893dba` |
| CAP-651 | Continue Architecture Planning.md > v0.23 > 23.11 Predicate-aware absence | `48fe4476448ab5bc` | `d7f969b2187202b5` |
| CAP-652 | Continue Architecture Planning.md > v0.23 > 23.12 Contradiction becomes first-class | `f9bdbfbdddf83ec7` | `58e156d8bd2e082a` |
| CAP-653 | Continue Architecture Planning.md > v0.23 > 23.13 True contradiction | `b8f1f5103fb44a07` | `88d2e3e89f63acc3` |
| CAP-654 | Continue Architecture Planning.md > v0.23 > 23.14 Absence confidence cannot simply be numeric | `4d0df94361facef0` | `4aee2e7a433f9d27` |
| CAP-655 | Continue Architecture Planning.md > v0.23 > 23.15 Independent evidence | `257be58fc74ae6c2` | `ca323cce3f292072` |
| CAP-656 | Continue Architecture Planning.md > v0.23 > 23.16 Absence reasoning engine | `44ecaaaf83172612` | `81699a3af2018b26` |
| CAP-657 | Continue Architecture Planning.md > v0.23 > 23.17 Formal absence rule | `83e664dff0c7d9c3` | `e3a9f59e2f6ea6d1` |
| CAP-658 | Continue Architecture Planning.md > v0.23 > 23.18 Dynamic universes | `58ba0af0387fc5e4` | `98c8cea995ef6a9f` |
| CAP-659 | Continue Architecture Planning.md > v0.23 > 23.19 Temporal validity | `4ea68240b79760f8` | `2ba65c61bce44514` |
| CAP-660 | Continue Architecture Planning.md > v0.23 > 23.20 Absence and revision detection | `d493ea77056dc28a` | `cf1c07921e2c157c` |
| CAP-661 | Continue Architecture Planning.md > v0.23 > 23.21 Search state now becomes richer | `237eedac21da0f2c` | `1250a7b929887faa` |
| CAP-662 | Continue Architecture Planning.md > v0.23 > 23.22 Architecture after v0.23 | `55728f460111d2fa` | `d07f89d1c254d2a1` |
| CAP-663 | Continue Architecture Planning.md > v0.23 > 23.23 The three epistemic outcomes | `442daeabc6a22767` | `7857d173ee4de5d3` |
| CAP-664 | Continue Architecture Planning.md > v0.23 > 23.23 The three epistemic outcomes > Presence | `d6b3e8c828d37420` | `e5d2b0495727aba9` |
| CAP-665 | Continue Architecture Planning.md > v0.23 > 23.23 The three epistemic outcomes > Absence | `8a43b9ea9c817849` | `c3c799d09ac9f39d` |
| CAP-666 | Continue Architecture Planning.md > v0.23 > 23.23 The three epistemic outcomes > Unknown | `b764cdc0eab71374` | `e79008b1f70a25a5` |
| CAP-667 | Continue Architecture Planning.md > v0.23 > 23.24 New invariants | `958104d64c687179` | `317c416a6e83a060` |
| CAP-668 | Continue Architecture Planning.md > v0.23 > 23.24 New invariants > Invariant 1 | `0f3f4cf90daef9a8` | `0eec933089847587` |
| CAP-669 | Continue Architecture Planning.md > v0.23 > 23.24 New invariants > Invariant 2 | `c83ee83a00023944` | `c6c9ebe21bc39559` |
| CAP-670 | Continue Architecture Planning.md > v0.23 > 23.24 New invariants > Invariant 3 | `ff318fcf8271d879` | `38795b92363c16b0` |
| CAP-671 | Continue Architecture Planning.md > v0.23 > 23.24 New invariants > Invariant 4 | `e1ce66c44f570280` | `9beaa624367760bd` |
| CAP-672 | Continue Architecture Planning.md > v0.23 > 23.24 New invariants > Invariant 5 | `bb6067b9e33d7d05` | `be5f6a960d1f14e5` |
| CAP-673 | Continue Architecture Planning.md > v0.23 > 23.24 New invariants > Invariant 6 | `2c06117f40c5939b` | `1cabca0c42935885` |
| CAP-674 | Continue Architecture Planning.md > v0.23 > 23.24 New invariants > Invariant 7 | `c5fcb7f01e3fb674` | `a5ed01d6021a555d` |
| CAP-675 | Continue Architecture Planning.md > v0.23 > 23.24 New invariants > Invariant 8 | `146d14f1f195c362` | `891563ecfa0cc780` |
| CAP-676 | Continue Architecture Planning.md > v0.23 > 23.24 New invariants > Invariant 9 | `da37a2b4721d9966` | `7911ee6ddefa72e8` |
| CAP-677 | Continue Architecture Planning.md > v0.23 > 23.24 New invariants > Invariant 10 | `16657d5a1eb43a15` | `3fba10e4cfc5647f` |
| CAP-678 | Continue Architecture Planning.md > v0.23 > 23.25 v0.23 conceptual result | `095a95b7690345a1` | `bd4fb47821cb8877` |
| CAP-679 | Continue Architecture Planning.md > v0.24 > v0.24 — Query/Goal-Constrained Discovery | `31b35949b56aad6a` | `bc500ba5767796fe` |
| CAP-680 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `31fbef162594de01` |
| CAP-681 | Continue Architecture Planning.md > v0.24 > v0.24 — Query/Goal-Constrained Discovery | `31b35949b56aad6a` | `1342e7c8adb423f0` |
| CAP-682 | Continue Architecture Planning.md > v0.24 > 24.1 SearchGoal | `29d980dcbf5e38ee` | `cfdfaeada6edfbc6` |
| CAP-683 | Continue Architecture Planning.md > v0.24 > 24.2 Goal ≠ Domain | `c754410256c2d771` | `777135d3a7b1ec5e` |
| CAP-684 | Continue Architecture Planning.md > v0.24 > 24.3 Goal constraints | `7fa95b407755348b` | `98f577303259f3c8` |
| CAP-685 | Continue Architecture Planning.md > v0.24 > 24.4 Hard constraints vs soft preferences | `94acee1dd4ef7a22` | `c18757cd9511061d` |
| CAP-686 | Continue Architecture Planning.md > v0.24 > 24.5 GoalConstraint | `8441a724073f4d86` | `0091120be27bad41` |
| CAP-687 | Continue Architecture Planning.md > v0.24 > 24.6 Relevance is not classification | `c132e86892dd7c34` | `b55f0618fc2af529` |
| CAP-688 | Continue Architecture Planning.md > v0.24 > 24.7 RelevanceAssertion | `c60e1154e4c8fa91` | `17afc1608bbed17d` |
| CAP-689 | Continue Architecture Planning.md > v0.24 > 24.8 Why `UNKNOWN` matters | `f8efbb75264663a3` | `70636041e899feed` |
| CAP-690 | Continue Architecture Planning.md > v0.24 > 24.9 Relevance scoring | `5a6b23b2550ae7f9` | `92d84ba656deb517` |
| CAP-691 | Continue Architecture Planning.md > v0.24 > 24.10 The six questions | `17338a9f7e914ead` | `b057541430f79b0b` |
| CAP-692 | Continue Architecture Planning.md > v0.24 > 24.11 Relevant Search Space | `efeb161d8cd773a7` | `45a45f98edf1fe01` |
| CAP-693 | Continue Architecture Planning.md > v0.24 > 24.12 Example | `15d1d6b1527ff39f` | `15b526b95b98e719` |
| CAP-694 | Continue Architecture Planning.md > v0.24 > 24.13 Goal-directed adaptive discovery | `f9499a135d26b012` | `f6eda85a6bb5be24` |
| CAP-695 | Continue Architecture Planning.md > v0.24 > 24.14 Expected Goal Value | `bb8e903fb6cd4679` | `3fa7503b3ad1e1f9` |
| CAP-696 | Continue Architecture Planning.md > v0.24 > 24.15 Information gain | `2714e3bb767d8da0` | `0c1bf97a7a77b1d1` |
| CAP-697 | Continue Architecture Planning.md > v0.24 > 24.16 Goal-aware partition scoring | `b3b5d92a0792aae7` | `376072ff2625d6e4` |
| CAP-698 | Continue Architecture Planning.md > v0.24 > 24.17 Goal does not grant authority | `50d8ab9a7a2a4096` | `d3915c039b861062` |
| CAP-699 | Continue Architecture Planning.md > v0.24 > 24.18 Goal provenance | `2d14ab05879632dc` | `d56af137015ab377` |
| CAP-700 | Continue Architecture Planning.md > v0.24 > 24.19 Goal-aware discovery event | `eaed172a0950bd3e` | `0d7d583ae4e81b99` |
| CAP-701 | Continue Architecture Planning.md > v0.24 > 24.20 Goal lifecycle | `3a23dafc2e953beb` | `0022812be31e7bd3` |
| CAP-702 | Continue Architecture Planning.md > v0.24 > 24.21 Goal termination policies | `2c0e9bf1f079e599` | `153ffd028b6fded2` |
| CAP-703 | Continue Architecture Planning.md > v0.24 > 24.22 Goal satisfaction vs completeness | `78e9f7e41b5270b5` | `98413b8eaeb04a75` |
| CAP-704 | Continue Architecture Planning.md > v0.24 > 24.23 GoalResult | `75890ffd014e99f5` | `7ec7590f9a2e38cc` |
| CAP-705 | Continue Architecture Planning.md > v0.24 > 24.24 Result ranking | `aafcc2cfe1ea6073` | `6828ef3c3f1f50c6` |
| CAP-706 | Continue Architecture Planning.md > v0.24 > 24.25 Result quality model | `bd91b6f04cee9c62` | `40b7baca40885cbf` |
| CAP-707 | Continue Architecture Planning.md > v0.24 > 24.26 Goal conflict | `8158ad0eea8adb39` | `46babb179aa97876` |
| CAP-708 | Continue Architecture Planning.md > v0.24 > 24.27 Goal sessions | `433ccaf1ee92ed2f` | `b6f4ce8986b4fe17` |
| CAP-709 | Continue Architecture Planning.md > v0.24 > 24.28 Reuse of previous knowledge | `4fe31a835eea26d8` | `473b04fc8d5cab1d` |
| CAP-710 | Continue Architecture Planning.md > v0.24 > 24.29 Knowledge reuse is not evidence reuse without qualification | `b87c3381c7b40e09` | `79491f360b6816c0` |
| CAP-711 | Continue Architecture Planning.md > v0.24 > 24.30 New architecture | `713a408fc7570dcf` | `fc3b7f73ec0ee259` |
| CAP-712 | Continue Architecture Planning.md > v0.24 > 24.31 The architecture's semantic layers | `4b07b83c875e864e` | `4c672c0810c53e3a` |
| CAP-713 | Continue Architecture Planning.md > v0.24 > 24.32 Core invariants for v0.24 | `abb6e3cb2d834745` | `920815de48ba867c` |
| CAP-714 | Continue Architecture Planning.md > v0.24 > 24.32 Core invariants for v0.24 > Invariant 1 | `0f3f4cf90daef9a8` | `1927406fce8c0b7b` |
| CAP-715 | Continue Architecture Planning.md > v0.24 > 24.32 Core invariants for v0.24 > Invariant 2 | `c83ee83a00023944` | `29dde59a46ee9747` |
| CAP-716 | Continue Architecture Planning.md > v0.24 > 24.32 Core invariants for v0.24 > Invariant 3 | `ff318fcf8271d879` | `716598b217f55ea9` |
| CAP-717 | Continue Architecture Planning.md > v0.24 > 24.32 Core invariants for v0.24 > Invariant 4 | `e1ce66c44f570280` | `eaf3a02b6e3e20f1` |
| CAP-718 | Continue Architecture Planning.md > v0.24 > 24.32 Core invariants for v0.24 > Invariant 5 | `bb6067b9e33d7d05` | `9c39b66247691080` |
| CAP-719 | Continue Architecture Planning.md > v0.24 > 24.32 Core invariants for v0.24 > Invariant 6 | `2c06117f40c5939b` | `ef636f42691fe304` |
| CAP-720 | Continue Architecture Planning.md > v0.24 > 24.32 Core invariants for v0.24 > Invariant 7 | `c5fcb7f01e3fb674` | `9062d6d2645a6896` |
| CAP-721 | Continue Architecture Planning.md > v0.24 > 24.32 Core invariants for v0.24 > Invariant 8 | `146d14f1f195c362` | `0cf32f84f7460d5d` |
| CAP-722 | Continue Architecture Planning.md > v0.24 > 24.32 Core invariants for v0.24 > Invariant 9 | `da37a2b4721d9966` | `ccaf7d6c27c0f9ea` |
| CAP-723 | Continue Architecture Planning.md > v0.24 > 24.32 Core invariants for v0.24 > Invariant 10 | `16657d5a1eb43a15` | `b1a593afd42e5bb4` |
| CAP-724 | Continue Architecture Planning.md > v0.24 > 24.33 What v0.24 changes fundamentally | `f29c2f60dd0f8d8e` | `5bac664c93be4e34` |
| CAP-725 | Continue Architecture Planning.md > v0.25 > v0.25 — Discovery Query Planner | `c701e853f6a12f10` | `9c729a6a929ce5e1` |
| CAP-726 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `31fbef162594de01` |
| CAP-727 | Continue Architecture Planning.md > v0.25 > v0.25 — Discovery Query Planner | `c701e853f6a12f10` | `acbab0c06dd10812` |
| CAP-728 | Continue Architecture Planning.md > v0.25 > v0.25 — Discovery Query Planner > 25.1 Planner ≠ Search Engine | `fb0dc1e82d7b7a54` | `3a5508a1d57e5ff5` |
| CAP-729 | Continue Architecture Planning.md > v0.25 > 25.2 QueryPlan | `c4cd8b518dffd497` | `1442d22e160a4007` |
| CAP-730 | Continue Architecture Planning.md > v0.25 > 25.3 QueryStep | `ba06ca94e5cd8d01` | `6fd03f28a4d8ac39` |
| CAP-731 | Continue Architecture Planning.md > v0.25 > 25.4 Query decomposition | `5759ada60d3d4668` | `e77947e4a21ae577` |
| CAP-732 | Continue Architecture Planning.md > v0.25 > 25.5 Search axes | `41971f14f04900c7` | `e20b50f09efe0537` |
| CAP-733 | Continue Architecture Planning.md > v0.25 > 25.6 QueryTactic | `dc2538bb540a0659` | `58289c6628334862` |
| CAP-734 | Continue Architecture Planning.md > v0.25 > 25.7 Tactic ≠ Strategy | `1109f32f092f17b1` | `009a6cca8321ba1e` |
| CAP-735 | Continue Architecture Planning.md > v0.25 > 25.8 Planner plugins | `a9d3262c13e718b7` | `9279a67e5909e9da` |
| CAP-736 | Continue Architecture Planning.md > v0.25 > 25.9 Planner contract | `03f10a94f46f0e86` | `bc2e2d3568d2ba33` |
| CAP-737 | Continue Architecture Planning.md > v0.25 > 25.10 Query plan example | `8d39723c8980cfa1` | `8b6404d334c426e6` |
| CAP-738 | Continue Architecture Planning.md > v0.25 > 25.11 Dependencies | `a7572aee7768a246` | `5e11d69d9d6670ca` |
| CAP-739 | Continue Architecture Planning.md > v0.25 > 25.12 Conditional planning | `2ad9dc47d1242f3d` | `63f379af776a0d04` |
| CAP-740 | Continue Architecture Planning.md > v0.25 > 25.13 Planning boundary | `875512217bb36a06` | `9c97c4c033a733f3` |
| CAP-741 | Continue Architecture Planning.md > v0.25 > 25.14 Query plan validation | `ddbb6dd15e31fb6f` | `13c5a5ee362f43f2` |
| CAP-742 | Continue Architecture Planning.md > v0.25 > 25.15 Planner and adaptive discovery | `3baa19cc7be8811d` | `b2736425a3ec3451` |
| CAP-743 | Continue Architecture Planning.md > v0.25 > 25.16 Exploration vs exploitation moves upward | `27fa5b885246c31c` | `49547809eb3b77e3` |
| CAP-744 | Continue Architecture Planning.md > v0.25 > 25.17 Query tactic performance | `1bd7830931158e68` | `45f0918ed0fd25fb` |
| CAP-745 | Continue Architecture Planning.md > v0.25 > 25.18 Query planner provenance | `684fddd45164158b` | `8ae05c115040fe8f` |
| CAP-746 | Continue Architecture Planning.md > v0.25 > 25.19 Query plan identity | `3221260aefaaf2fe` | `95040ca9eda252d8` |
| CAP-747 | Continue Architecture Planning.md > v0.25 > 25.20 Plan versioning | `206648e2b7c5507b` | `8133232e1a9e406d` |
| CAP-748 | Continue Architecture Planning.md > v0.25 > 25.21 Planner cannot erase old work | `b91c08d75a5ba7b1` | `79c5ca60a3f5af9f` |
| CAP-749 | Continue Architecture Planning.md > v0.25 > 25.22 Query expansion | `35933498daf935d0` | `9ad773b5ea0889cf` |
| CAP-750 | Continue Architecture Planning.md > v0.25 > 25.23 Expansion evidence | `4b814ca3ea59b0b1` | `7d55d3f10bc70965` |
| CAP-751 | Continue Architecture Planning.md > v0.25 > 25.24 Planner hallucination boundary | `6d391b7d72bea8b0` | `57357551a56baf90` |
| CAP-752 | Continue Architecture Planning.md > v0.25 > 25.25 Search hypothesis | `39a197bb04695a90` | `7b979017a72de8d8` |
| CAP-753 | Continue Architecture Planning.md > v0.25 > 25.26 Query planner and DVB analogy | `6ac09f9df0ec8426` | `ccdae0bfb7e7606f` |
| CAP-754 | Continue Architecture Planning.md > v0.25 > 25.27 Planner output is not execution | `fb2f82790db85264` | `647e33e4aa984477` |
| CAP-755 | Continue Architecture Planning.md > v0.25 > 25.28 Planner budget | `40c94ffe57f5b321` | `36ca9188785de869` |
| CAP-756 | Continue Architecture Planning.md > v0.25 > 25.29 Three different budgets | `85e8682d1f5a5c7d` | `14d70bb10e4587ee` |
| CAP-757 | Continue Architecture Planning.md > v0.25 > 25.30 Termination propagation | `6619ef641ac2ee1f` | `af452acc409b9dc3` |
| CAP-758 | Continue Architecture Planning.md > v0.25 > 25.31 v0.25 complete architecture | `397e4d7caa136b6f` | `c6f35846bacadc8e` |
| CAP-759 | Continue Architecture Planning.md > v0.25 > 25.32 v0.25 invariants | `24c15fe644b4f3c2` | `a5879da27be5bfa4` |
| CAP-760 | Continue Architecture Planning.md > v0.25 > 25.32 v0.25 invariants > Planner invariants | `4d44f63dc49d7e7a` | `0827e0e152643977` |
| CAP-761 | Continue Architecture Planning.md > v0.25 > 25.33 The resulting abstraction stack | `4a8be2029d2c15e8` | `7f14a4b694be7ae6` |
| CAP-762 | Continue Architecture Planning.md > v0.26 > v0.26 — Search Tactic Runtime | `0db41a7d631b46d0` | `b512806289e0cd4a` |
| CAP-763 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `31fbef162594de01` |
| CAP-764 | Continue Architecture Planning.md > v0.26 > v0.26 — Search Tactic Runtime | `0db41a7d631b46d0` | `4be92bd270666ff3` |
| CAP-765 | Continue Architecture Planning.md > v0.26 > v0.26 — Search Tactic Runtime > 26.1 The architectural gap | `5716f1c8a73ef06b` | `529001449fb6971f` |
| CAP-766 | Continue Architecture Planning.md > v0.26 > 26.2 QueryStep ≠ TacticExecution | `546bfa0acc2e8141` | `259382664322da8d` |
| CAP-767 | Continue Architecture Planning.md > v0.26 > 26.3 TacticExecution | `757c9ef3db05ce9d` | `4ab79516e338cca8` |
| CAP-768 | Continue Architecture Planning.md > v0.26 > 26.4 TacticRuntime | `b237792222ad9134` | `1a869b21f4d924ba` |
| CAP-769 | Continue Architecture Planning.md > v0.26 > 26.5 TacticRuntime responsibilities | `0870de5da7408b3c` | `c3079c04051dc55b` |
| CAP-770 | Continue Architecture Planning.md > v0.26 > 26.6 Tactic contract | `713ed47e4ed0e8be` | `a045799654ed137c` |
| CAP-771 | Continue Architecture Planning.md > v0.26 > 26.7 Capability surface | `a144c378b78b0402` | `d4b7c4f5778d0109` |
| CAP-772 | Continue Architecture Planning.md > v0.26 > 26.8 Bounded execution | `8ccde41379f41d58` | `5f74dac937b32495` |
| CAP-773 | Continue Architecture Planning.md > v0.26 > 26.9 Batch execution | `97fe534f6ee9df85` | `b7b52f21640e0828` |
| CAP-774 | Continue Architecture Planning.md > v0.26 > 26.10 Cursor | `ee5582614932d7a8` | `4ce09e2df8f0c5d2` |
| CAP-775 | Continue Architecture Planning.md > v0.26 > 26.11 Checkpoint | `b85d471828e213ae` | `a533b21922d0905e` |
| CAP-776 | Continue Architecture Planning.md > v0.26 > 26.12 Checkpoint atomicity | `258f4cc9924968a7` | `e4565707459b7e4c` |
| CAP-777 | Continue Architecture Planning.md > v0.26 > 26.13 Tactic dependencies | `f6755b6a5275b6e2` | `1f66052d65bbc724` |
| CAP-778 | Continue Architecture Planning.md > v0.26 > 26.14 Tactic lifecycle | `339dfaf602b9b3df` | `9e48221ec268545d` |
| CAP-779 | Continue Architecture Planning.md > v0.26 > 26.15 Exhaustion vs completion | `751566523d53f77b` | `5424bf678ff39d7b` |
| CAP-780 | Continue Architecture Planning.md > v0.26 > 26.16 Tactic result | `d6e802da8da70f7b` | `5c066624e5b1af84` |
| CAP-781 | Continue Architecture Planning.md > v0.26 > 26.17 Tactic does not create candidates directly | `5d3a99e4db7141ca` | `6605d877bcf6bcad` |
| CAP-782 | Continue Architecture Planning.md > v0.26 > 26.18 Tactic → Strategy relationship | `23d61f29000a72db` | `2eac0a8728238bbf` |
| CAP-783 | Continue Architecture Planning.md > v0.26 > 26.19 Tactic provenance | `d0a2c77053eb0c74` | `6ffc9127c7410451` |
| CAP-784 | Continue Architecture Planning.md > v0.26 > 26.20 Failure taxonomy | `3042737cc68b9456` | `4a4fe9b56c64d139` |
| CAP-785 | Continue Architecture Planning.md > v0.26 > 26.20 Failure taxonomy > Planning failures | `ceaf279dbe1b58fe` | `fcee1db3e38fab9e` |
| CAP-786 | Continue Architecture Planning.md > v0.26 > 26.20 Failure taxonomy > Runtime failures | `d2a65a747b55321c` | `2fb5941fffaac75d` |
| CAP-787 | Continue Architecture Planning.md > v0.26 > 26.20 Failure taxonomy > Strategy failures | `61e279695f24e45e` | `42c8d1003870d298` |
| CAP-788 | Continue Architecture Planning.md > v0.26 > 26.20 Failure taxonomy > Search failures | `d6b354c7143aebd8` | `5c55f28938f7f7b5` |
| CAP-789 | Continue Architecture Planning.md > v0.26 > 26.20 Failure taxonomy > Recovery failures | `d8a0fd302fb6fb9d` | `ac63ff08681c07f1` |
| CAP-790 | Continue Architecture Planning.md > v0.26 > 26.21 Retry semantics | `76ff07e3d1df1a40` | `85465bf311209ff3` |
| CAP-791 | Continue Architecture Planning.md > v0.26 > 26.22 Cancellation | `00dc1fdcb2d3c8b2` | `7ac9ceafa4d7f7d2` |
| CAP-792 | Continue Architecture Planning.md > v0.26 > 26.23 Shared Frontier interaction | `a834b62d64b7e440` | `09146de7f807fbc0` |
| CAP-793 | Continue Architecture Planning.md > v0.26 > 26.24 v0.26 architecture | `16dc49325e75bcc0` | `015fd4918911b526` |
| CAP-794 | Continue Architecture Planning.md > v0.26 > 26.25 Accounting | `d44ece79ee66e481` | `3174df9385841eb5` |
| CAP-795 | Continue Architecture Planning.md > v0.26 > 26.26 The important safety invariant | `c26cad5097f7c02c` | `052807dfb0da175a` |
| CAP-796 | Continue Architecture Planning.md > v0.26 > 26.27 Resumability invariant | `9517b5a22c59ff4a` | `a5584db48e089e32` |
| CAP-797 | Continue Architecture Planning.md > v0.26 > 26.28 New state model | `a86e956494f39e47` | `df4c8abda8f48e51` |
| CAP-798 | Continue Architecture Planning.md > v0.26 > 26.29 v0.26 invariants | `fa7f4132bab9a099` | `2ee5eab06899264c` |
| CAP-799 | Continue Architecture Planning.md > v0.26 > 26.29 v0.26 invariants > I1 — Planning/execution separation | `37f5c792d27c37f0` | `67accc1707d202cd` |
| CAP-800 | Continue Architecture Planning.md > v0.26 > 26.29 v0.26 invariants > I2 — Execution identity | `4891a4f80d9240ae` | `fe7f0526ac6e1c49` |
| CAP-801 | Continue Architecture Planning.md > v0.26 > 26.29 v0.26 invariants > I3 — Single scheduler authority | `e1e78cd1124ccb49` | `f393fb3bcdc69860` |
| CAP-802 | Continue Architecture Planning.md > v0.26 > 26.29 v0.26 invariants > I4 — Bounded execution | `3bae6f6b0632552c` | `06acd60112c5ff16` |
| CAP-803 | Continue Architecture Planning.md > v0.26 > 26.29 v0.26 invariants > I5 — Resumability | `a7c47e6e27969698` | `5fa6fe60b93fd0a4` |
| CAP-804 | Continue Architecture Planning.md > v0.26 > 26.29 v0.26 invariants > I6 — No silent cursor advancement | `71e1e36ada037fc8` | `be9236c24dbe7f05` |
| CAP-805 | Continue Architecture Planning.md > v0.26 > 26.29 v0.26 invariants > I7 — Proposal boundary | `610c7c9da34258cf` | `c3312af775215b22` |
| CAP-806 | Continue Architecture Planning.md > v0.26 > 26.29 v0.26 invariants > I8 — No authority escalation | `790c60d61b0caaf7` | `3d25eb635267ec9f` |
| CAP-807 | Continue Architecture Planning.md > v0.26 > 26.29 v0.26 invariants > I9 — Exhaustion separation | `59ca11d5c17244f5` | `904f92ace1327e0e` |
| CAP-808 | Continue Architecture Planning.md > v0.26 > 26.29 v0.26 invariants > I10 — Failure ≠ absence | `d627e47adc4066c3` | `9c81d756e67e3b3b` |
| CAP-809 | Continue Architecture Planning.md > v0.26 > 26.29 v0.26 invariants > I11 — Provenance | `3faee28ac4d4d928` | `731b600be1d6c9c7` |
| CAP-810 | Continue Architecture Planning.md > v0.26 > 26.29 v0.26 invariants > I12 — Versioned recovery | `2b4d0cafc1693712` | `405f62d4d4d83f91` |
| CAP-811 | Continue Architecture Planning.md > v0.26 > 26.30 What v0.26 actually gives us | `a05e58d2d5726bd7` | `119b5f0cd9d66833` |
| CAP-812 | Continue Architecture Planning.md > v0.26 > 26.30 What v0.26 actually gives us > Next boundary: v0.27 | `c0200807f2eae5c0` | `05e0a782cca5e8b5` |
| CAP-813 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `31fbef162594de01` |
| CAP-814 | Continue Architecture Planning.md > v0.27 > v0.27 — Enumeration Runtime | `88172a5792cbb03d` | `1f86ac6a0ddb6746` |
| CAP-815 | Continue Architecture Planning.md > v0.27 > 27.1 The central distinction | `91674f4bd6004631` | `7bab4a156381b8ae` |
| CAP-816 | Continue Architecture Planning.md > v0.27 > 27.2 Enumeration as a contract | `7f4904b8747a4afc` | `a6d4a227be224b20` |
| CAP-817 | Continue Architecture Planning.md > v0.27 > 27.3 Enumerator interface | `b837326227adf67a` | `1d4bf3685a1f1b44` |
| CAP-818 | Continue Architecture Planning.md > v0.27 > 27.4 EnumerationPage | `da8f212cb7742ab8` | `662dd2ee42014810` |
| CAP-819 | Continue Architecture Planning.md > v0.27 > 27.5 `hasMore` is not always trustworthy | `1e2cfb24903212bd` | `56d2236a40bfe45d` |
| CAP-820 | Continue Architecture Planning.md > v0.27 > 27.6 Enumeration state machine | `6fd11c082abbf862` | `14257914fbcf6bd0` |
| CAP-821 | Continue Architecture Planning.md > v0.27 > 27.7 EnumerationRuntime | `9f1b09ac785c6897` | `f46e3ec6bf2fe105` |
| CAP-822 | Continue Architecture Planning.md > v0.27 > 27.8 Why this should not be inside DiscoveryStrategy | `4002323cd11aa739` | `cf18fd25e59ed8ed` |
| CAP-823 | Continue Architecture Planning.md > v0.27 > 27.9 Enumerator examples | `001b82ce36aa4cba` | `ee03dcce0716b211` |
| CAP-824 | Continue Architecture Planning.md > v0.27 > 27.9 Enumerator examples > Sitemap | `4db550cd984016b9` | `791d02c62d19c65a` |
| CAP-825 | Continue Architecture Planning.md > v0.27 > 27.9 Enumerator examples > API | `c8e5998f6a3955c2` | `622d8057c8f1b16e` |
| CAP-826 | Continue Architecture Planning.md > v0.27 > 27.9 Enumerator examples > Repository | `13d6ff07b8a5d792` | `d8d87416a3fc441c` |
| CAP-827 | Continue Architecture Planning.md > v0.27 > 27.9 Enumerator examples > Manifest | `3c99f1f33643ed94` | `e635cee59dbbdd17` |
| CAP-828 | Continue Architecture Planning.md > v0.27 > 27.10 EnumerationEntry | `57e2809829c291f9` | `df06d493af1a5c2e` |
| CAP-829 | Continue Architecture Planning.md > v0.27 > 27.11 Entry identity | `fdba7a69c575529b` | `f2f9441f59ef8dae` |
| CAP-830 | Continue Architecture Planning.md > v0.27 > 27.12 Enumeration cursor | `12ede8e997c3c19b` | `cfd18b7f3c037725` |
| CAP-831 | Continue Architecture Planning.md > v0.27 > 27.12 Enumeration cursor > Offset | `b1a1e8e3cf7c522e` | `683b5318ba12d47e` |
| CAP-832 | Continue Architecture Planning.md > v0.27 > 27.12 Enumeration cursor > Page | `0a30a815d67d7dd2` | `f1032e4b25269ceb` |
| CAP-833 | Continue Architecture Planning.md > v0.27 > 27.12 Enumeration cursor > Token | `d2089be672953d11` | `82aff66c9a7a9423` |
| CAP-834 | Continue Architecture Planning.md > v0.27 > 27.12 Enumeration cursor > Locator | `cb4796be826cde7d` | `3ecea4825f88a707` |
| CAP-835 | Continue Architecture Planning.md > v0.27 > 27.12 Enumeration cursor > Composite | `8e3588157fcf8d7c` | `dfae643ab8898e52` |
| CAP-836 | Continue Architecture Planning.md > v0.27 > 27.13 Cursor validity | `3d9321aefdd42185` | `4c0500361809ee32` |
| CAP-837 | Continue Architecture Planning.md > v0.27 > 27.14 Enumeration snapshot | `e2084977b77b4374` | `9076dfdd8481aa8f` |
| CAP-838 | Continue Architecture Planning.md > v0.27 > 27.15 Why snapshot identity matters | `ff7c3fbd9a4d151e` | `bc19d05f6113d802` |
| CAP-839 | Continue Architecture Planning.md > v0.27 > 27.16 Cardinality | `253ed24be49adc6e` | `c7691cb566c2363c` |
| CAP-840 | Continue Architecture Planning.md > v0.27 > 27.17 Ordering semantics | `6078c58f77f945a2` | `1b52bd3f4d0aa2df` |
| CAP-841 | Continue Architecture Planning.md > v0.27 > 27.18 Enumeration consistency | `e2b8d4bb0405ae63` | `72ef4d507d25f186` |
| CAP-842 | Continue Architecture Planning.md > v0.27 > 27.19 Completeness assessment | `8a43a304c89cedaa` | `d8246d37a4040a35` |
| CAP-843 | Continue Architecture Planning.md > v0.27 > 27.20 The crucial three-level distinction | `24ddbc8fb99c5ef6` | `228976abe8db66eb` |
| CAP-844 | Continue Architecture Planning.md > v0.27 > 27.21 Example: sitemap | `d43b3e8d23941f74` | `cb6376b49bc4be96` |
| CAP-845 | Continue Architecture Planning.md > v0.27 > 27.22 Enumeration → Coverage | `ce906d8f9e579b2b` | `d7831baa33627959` |
| CAP-846 | Continue Architecture Planning.md > v0.27 > 27.23 Enumeration and negative evidence | `d771604492eb8c93` | `14deb1807ee75980` |
| CAP-847 | Continue Architecture Planning.md > v0.27 > 27.24 Enumeration budget | `4d977d444e0d09b8` | `8dc4de644de8c42d` |
| CAP-848 | Continue Architecture Planning.md > v0.27 > 27.25 Enumeration termination states | `19113ed31f122dbc` | `13bd1b9bf0f21a6f` |
| CAP-849 | Continue Architecture Planning.md > v0.27 > 27.26 Enumeration accounting | `c6fb9fd8f6b1b6fb` | `a501c7e1e39a6861` |
| CAP-850 | Continue Architecture Planning.md > v0.27 > 27.27 Enumeration provenance | `3ba4191ee2ab89fb` | `b145525d033c6455` |
| CAP-851 | Continue Architecture Planning.md > v0.27 > 27.28 Enumeration replay | `06a970781642437c` | `3652c625b0324ecc` |
| CAP-852 | Continue Architecture Planning.md > v0.27 > 27.29 Full v0.27 architecture | `f39ce54c4e49d620` | `aa472f68d28aba76` |
| CAP-853 | Continue Architecture Planning.md > v0.27 > 27.30 New invariants | `81b420dfface1b7d` | `78c0ebe53c7bb1dd` |
| CAP-854 | Continue Architecture Planning.md > v0.27 > 27.30 New invariants > E1 — Enumeration is scoped | `518613152d92de8c` | `2bae70fbb3d3e1c7` |
| CAP-855 | Continue Architecture Planning.md > v0.27 > 27.30 New invariants > E2 — Enumeration termination is not global completeness | `4daf389cd8b01cda` | `38dff2dedbd695f6` |
| CAP-856 | Continue Architecture Planning.md > v0.27 > 27.30 New invariants > E3 — Budget exhaustion is not enumeration exhaustion | `1dc9778b40414d62` | `caf2fe82e754d669` |
| CAP-857 | Continue Architecture Planning.md > v0.27 > 27.30 New invariants > E4 — Cursor progress must be durable | `0b84d9f58274ff6f` | `7e10d70ae57d2a8c` |
| CAP-858 | Continue Architecture Planning.md > v0.27 > 27.30 New invariants > E5 — Enumeration entries are not candidates | `78b7cf6fc72a18ed` | `d7200dfd6cea7199` |
| CAP-859 | Continue Architecture Planning.md > v0.27 > 27.30 New invariants > E6 — Cardinality is evidence | `730dad7986707eeb` | `bffca439c6bba63b` |
| CAP-860 | Continue Architecture Planning.md > v0.27 > 27.30 New invariants > E7 — Historical snapshots remain immutable | `abefcea4d8d5b142` | `e2713e02e2bfb665` |
| CAP-861 | Continue Architecture Planning.md > v0.27 > 27.30 New invariants > E8 — Incomplete enumeration cannot establish absence | `32c8519e6811b66b` | `84a6578c9a594c44` |
| CAP-862 | Continue Architecture Planning.md > v0.27 > 27.30 New invariants > E9 — Unstable enumeration weakens completeness | `b4a768d4cc539b4a` | `eb6662e70a0ef4f2` |
| CAP-863 | Continue Architecture Planning.md > v0.27 > 27.30 New invariants > E10 — Enumerator has no acquisition authority | `4866adf6e58b1efb` | `d48dba60c9e4a06e` |
| CAP-864 | Continue Architecture Planning.md > v0.27 > 27.30 New invariants > E11 — Enumerator cannot directly mutate the ResourceGraph | `8eb4496917dba477` | `1b099dcbcc554f7c` |
| CAP-865 | Continue Architecture Planning.md > v0.27 > 27.30 New invariants > E12 — Termination evidence is provenance-bearing | `099758799b7adc54` | `418d41a2cd2c4b06` |
| CAP-866 | Continue Architecture Planning.md > v0.27 > 27.31 The emerging blind-scan analogy | `44f2e2785932b553` | `bc2e1589ea4b504d` |
| CAP-867 | Continue Architecture Planning.md > v0.27 > v0.27 takeaway | `64b8d51adef3f5a5` | `ceb3e7848965aa42` |
| CAP-868 | Continue Architecture Planning.md > v0.28 > v0.28 — Search-Space Reconciliation & Frontier Deduplication | `bf6d6800a8aa9b97` | `3cb68ed50dc3335e` |
| CAP-869 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `31fbef162594de01` |
| CAP-870 | Continue Architecture Planning.md > v0.28 > v0.28 — Search-Space Reconciliation & Frontier Deduplication | `bf6d6800a8aa9b97` | `e7d2cc2815863465` |
| CAP-871 | Continue Architecture Planning.md > v0.28 > 28.1 The problem with naive deduplication | `bd6e5f314d1c0d88` | `dce9ca0f7ceb92f5` |
| CAP-872 | Continue Architecture Planning.md > v0.28 > 28.2 Five different kinds of duplication | `3c24917a4da4fa01` | `dcd11a92abf14126` |
| CAP-873 | Continue Architecture Planning.md > v0.28 > 28.3 Search-space overlap | `69742855667a3390` | `4605f81892910d2a` |
| CAP-874 | Continue Architecture Planning.md > v0.28 > 28.4 SearchPartitionRelation | `98731615433cb09b` | `dc4e8cf7af77eb49` |
| CAP-875 | Continue Architecture Planning.md > v0.28 > 28.5 Coverage overlap | `0990bb02286f12a1` | `899311b8ae2a0343` |
| CAP-876 | Continue Architecture Planning.md > v0.28 > 28.6 Frontier deduplication | `20aae61ddca02646` | `7cb45c3065538249` |
| CAP-877 | Continue Architecture Planning.md > v0.28 > 28.7 SearchWorkKey | `0251b153acbb0196` | `eba7f53382806d04` |
| CAP-878 | Continue Architecture Planning.md > v0.28 > 28.8 Work equivalence | `baccc5df0d275fa5` | `0b9f54b1947d41d3` |
| CAP-879 | Continue Architecture Planning.md > v0.28 > 28.9 Candidate convergence | `4bda835519ab4f5b` | `29c5722aa355456a` |
| CAP-880 | Continue Architecture Planning.md > v0.28 > 28.10 Observation convergence | `7481b48da4c4258b` | `a0067daf7271872d` |
| CAP-881 | Continue Architecture Planning.md > v0.28 > 28.11 Artifact convergence | `c825ff624a900c54` | `b72bdb249077a4b5` |
| CAP-882 | Continue Architecture Planning.md > v0.28 > 28.12 Discovery independence | `3614e201c5a80f47` | `3acab98691c6aa43` |
| CAP-883 | Continue Architecture Planning.md > v0.28 > 28.13 Evidence independence model | `78551a22ab252d93` | `87bf36097af36f22` |
| CAP-884 | Continue Architecture Planning.md > v0.28 > 28.14 Coverage provenance | `5694f6a2156dcb79` | `566a08f56b7741a6` |
| CAP-885 | Continue Architecture Planning.md > v0.28 > 28.15 Coverage relation | `918007a2f9c0a007` | `9594b4b443af69d1` |
| CAP-886 | Continue Architecture Planning.md > v0.28 > 28.16 Coverage union | `8bdd473339237f78` | `27c617ef5e54ab1b` |
| CAP-887 | Continue Architecture Planning.md > v0.28 > 28.17 Disjoint partitions | `630e503e3c6fb2fd` | `c90a440cd4177f23` |
| CAP-888 | Continue Architecture Planning.md > v0.28 > 28.18 Unknown overlap | `30d5c706f94221ac` | `c68ffafbc530f1ec` |
| CAP-889 | Continue Architecture Planning.md > v0.28 > 28.19 Frontier duplicate suppression | `87e5561c99373471` | `a2c8da5e37b465f0` |
| CAP-890 | Continue Architecture Planning.md > v0.28 > 28.20 Duplicate suppression must preserve provenance | `d566f7cc6f96775f` | `f3994d2dac5c4ef6` |
| CAP-891 | Continue Architecture Planning.md > v0.28 > 28.21 Convergence graph | `2187438ca0e2a5f6` | `1f3a4b12b37e84be` |
| CAP-892 | Continue Architecture Planning.md > v0.28 > 28.22 Search-space graph | `9fd143aa9e966c96` | `3064b8a897ebc2a9` |
| CAP-893 | Continue Architecture Planning.md > v0.28 > 28.23 Search-space coverage ledger | `b5851ac245d5067d` | `c61dea8830a01aaa` |
| CAP-894 | Continue Architecture Planning.md > v0.28 > 28.24 Candidate count is not coverage | `6211fb878181323c` | `cdf3808f1d095015` |
| CAP-895 | Continue Architecture Planning.md > v0.28 > 28.25 Search-space deduplication vs candidate deduplication | `f3351dbe96cefd93` | `a2dca0811b77bcc5` |
| CAP-896 | Continue Architecture Planning.md > v0.28 > 28.25 Search-space deduplication vs candidate deduplication > Candidate deduplication | `2463500687ef4561` | `5735e6d5267de8fb` |
| CAP-897 | Continue Architecture Planning.md > v0.28 > 28.25 Search-space deduplication vs candidate deduplication > Search-space deduplication | `25746cf5f4adc19e` | `fa6db65afa745857` |
| CAP-898 | Continue Architecture Planning.md > v0.28 > 28.26 Adaptive strategy interaction | `8fd112b1563ac89d` | `5728690f4ae09b91` |
| CAP-899 | Continue Architecture Planning.md > v0.28 > 28.27 Example | `f6c01cb32d15325a` | `a80bdafc9687db6f` |
| CAP-900 | Continue Architecture Planning.md > v0.28 > 28.28 Reconciliation algorithm | `1c6c336119a4898c` | `8c20d6de11dd7d45` |
| CAP-901 | Continue Architecture Planning.md > v0.28 > 28.29 Reconciliation must be monotonic | `c87493e22f53bff4` | `836ad9a6f6fa14ba` |
| CAP-902 | Continue Architecture Planning.md > v0.28 > 28.30 Reconciliation does not delete evidence | `aa576589e1b194e8` | `c1b344d0f4910c24` |
| CAP-903 | Continue Architecture Planning.md > v0.28 > 28.31 Failure taxonomy | `b214b726d8a804c2` | `fa4b2d4ad3e43ec3` |
| CAP-904 | Continue Architecture Planning.md > v0.28 > 28.32 Core invariants | `f6ebb03505457b75` | `b55430e644d8de71` |
| CAP-905 | Continue Architecture Planning.md > v0.28 > 28.32 Core invariants > R1 — Candidate convergence | `ebccd734b1c23c5e` | `b7e4155c8a6a32e1` |
| CAP-906 | Continue Architecture Planning.md > v0.28 > 28.32 Core invariants > R2 — Provenance preservation | `e501f0bac1ccb451` | `e04d131c15560ed9` |
| CAP-907 | Continue Architecture Planning.md > v0.28 > 28.32 Core invariants > R3 — Artifact convergence | `eff90490c014ec3c` | `47960d2ccfee9fc1` |
| CAP-908 | Continue Architecture Planning.md > v0.28 > 28.32 Core invariants > R4 — Observation preservation | `4a764c7b2800d094` | `0df5058eec6f538f` |
| CAP-909 | Continue Architecture Planning.md > v0.28 > 28.32 Core invariants > R5 — Overlap is not duplication | `f971ea60ec067e9e` | `167ac4c289ee5314` |
| CAP-910 | Continue Architecture Planning.md > v0.28 > 28.32 Core invariants > R6 — Equivalent work may be suppressed | `c1a8de0a8578858a` | `b9366736a4ec51fb` |
| CAP-911 | Continue Architecture Planning.md > v0.28 > 28.32 Core invariants > R7 — Suppression preserves provenance | `a3d55cafbb98c71a` | `48df3f0bbb5d9371` |
| CAP-912 | Continue Architecture Planning.md > v0.28 > 28.32 Core invariants > R8 — Unknown overlap is not disjointness | `57c0f78d0e7bf061` | `15e37c8f9fb14db4` |
| CAP-913 | Continue Architecture Planning.md > v0.28 > 28.32 Core invariants > R9 — Coverage is union-aware | `dc1ded9009a2ae92` | `1312bc1a19a541e7` |
| CAP-914 | Continue Architecture Planning.md > v0.28 > 28.32 Core invariants > R10 — Candidate count does not establish coverage | `783ea17afeacf8df` | `64ea270142dc00c9` |
| CAP-915 | Continue Architecture Planning.md > v0.28 > 28.32 Core invariants > R11 — Evidence independence must be justified | `18e46e087b027249` | `93d63bbbba661947` |
| CAP-916 | Continue Architecture Planning.md > v0.28 > 28.32 Core invariants > R12 — Historical reconciliation is immutable | `a3f69cc25f9d4846` | `34671d5ceb44143a` |
| CAP-917 | Continue Architecture Planning.md > v0.28 > 28.33 v0.28 architecture | `6358ad8fabf2fc58` | `d091885989d1ecfd` |
| CAP-918 | Continue Architecture Planning.md > v0.28 > 28.34 The deeper architectural result | `9f6ea17063b96f40` | `a6e3ee3c3d0669dc` |
| CAP-919 | Continue Architecture Planning.md > v0.28 > 28.34 The deeper architectural result > Next boundary — v0.29 | `9deaf194a3c2d610` | `5292b5c819f25d9f` |
| CAP-920 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `31fbef162594de01` |
| CAP-921 | Continue Architecture Planning.md > v0.29 > v0.29 — Dynamic Search-Space Expansion | `ec261954575012bf` | `2e29314052289f4d` |
| CAP-922 | Continue Architecture Planning.md > v0.29 > 29.1 The central distinction | `57d314927a247b97` | `e81adc634d97acb1` |
| CAP-923 | Continue Architecture Planning.md > v0.29 > 29.2 PartitionProposal | `319dc67755014df9` | `a0700ea01b3dcad1` |
| CAP-924 | Continue Architecture Planning.md > v0.29 > 29.3 Why proposals are necessary | `89b999efa5c9b425` | `ce60d883edf4dd7d` |
| CAP-925 | Continue Architecture Planning.md > v0.29 > 29.4 PartitionAdmissionController | `cdc15ffc59281dea` | `680c92590e45f351` |
| CAP-926 | Continue Architecture Planning.md > v0.29 > 29.5 Partition identity | `f4135a2ef0d720f7` | `22e30ee9d2e84d4e` |
| CAP-927 | Continue Architecture Planning.md > v0.29 > 29.6 Partition explosion | `0ada1cdca0fb0233` | `869ae3a2e8ed6765` |
| CAP-928 | Continue Architecture Planning.md > v0.29 > 29.7 ExpansionBudget | `6b1dbb9989858555` | `c16770a0a1649a70` |
| CAP-929 | Continue Architecture Planning.md > v0.29 > 29.8 Local expansion rate | `42db1dbea93112a8` | `9b138a23bb654e60` |
| CAP-930 | Continue Architecture Planning.md > v0.29 > 29.9 Expansion rate limiting | `c5b5c01a8877cb62` | `6b79193d00041bff` |
| CAP-931 | Continue Architecture Planning.md > v0.29 > 29.10 Evidence threshold | `fd74397d783e78ef` | `5c5598150aa7a52c` |
| CAP-932 | Continue Architecture Planning.md > v0.29 > 29.11 Partition proposal epistemic status | `373da47007b1c315` | `56d60bbe8eb4c615` |
| CAP-933 | Continue Architecture Planning.md > v0.29 > 29.12 Hypothesis connection | `d3cfbd55a96cf15b` | `f328bd825cce1049` |
| CAP-934 | Continue Architecture Planning.md > v0.29 > 29.13 Partition generation sources | `5570ed42985befe3` | `e9f58eb0f17bcafb` |
| CAP-935 | Continue Architecture Planning.md > v0.29 > 29.14 Expansion provider boundary | `b4f404e482609522` | `c7afc1b270f9d98e` |
| CAP-936 | Continue Architecture Planning.md > v0.29 > 29.15 Dynamic search-space graph | `acd1a61f26feeb5d` | `d6f9e752bc29e135` |
| CAP-937 | Continue Architecture Planning.md > v0.29 > 29.16 Partition generation event | `96f333a1644875f3` | `801a7c3962d4efab` |
| CAP-938 | Continue Architecture Planning.md > v0.29 > 29.17 Search-space versioning | `f10b2eb5ff96b2b8` | `6f23d27a1ebedf2a` |
| CAP-939 | Continue Architecture Planning.md > v0.29 > 29.18 SearchSpaceSnapshot | `dcfa39dc347ba86c` | `3e2bd798f7a676bf` |
| CAP-940 | Continue Architecture Planning.md > v0.29 > 29.19 Expansion and completeness | `e0ce04cb2bd60442` | `6920d932a7bbd556` |
| CAP-941 | Continue Architecture Planning.md > v0.29 > 29.20 Dynamic expansion and negative evidence | `7b9e03f894843b0d` | `1278b99ece627c70` |
| CAP-942 | Continue Architecture Planning.md > v0.29 > 29.21 Expansion priorities | `263a04c1ac502b82` | `c7774e97ec4887d5` |
| CAP-943 | Continue Architecture Planning.md > v0.29 > 29.22 Expansion depth | `6b694f39fc3fe7a6` | `5fcacc0a93489e96` |
| CAP-944 | Continue Architecture Planning.md > v0.29 > 29.23 Expansion loops | `723e11b514eb2083` | `cc0bdc39479ac522` |
| CAP-945 | Continue Architecture Planning.md > v0.29 > 29.24 Expansion cycle ≠ failure | `51e836189404122f` | `0503d84bdd77b661` |
| CAP-946 | Continue Architecture Planning.md > v0.29 > 29.25 Partition admission states | `9add07dc879b0c9b` | `f60483c02a60ddde` |
| CAP-947 | Continue Architecture Planning.md > v0.29 > 29.26 Partition proposal accounting | `6f297fc7dd02bc7b` | `52ee467dc5f0720c` |
| CAP-948 | Continue Architecture Planning.md > v0.29 > 29.27 Partition explosion protection | `7708a59c5e5f052d` | `c765b37f172682f5` |
| CAP-949 | Continue Architecture Planning.md > v0.29 > 29.28 Admission algorithm | `ef265b1e54c50950` | `4eee74000e0d3345` |
| CAP-950 | Continue Architecture Planning.md > v0.29 > 29.29 Frontier generation | `da1215d6b76c28fe` | `35414120c7c020cc` |
| CAP-951 | Continue Architecture Planning.md > v0.29 > 29.30 Dynamic expansion architecture | `cd2b00c28d9e9f58` | `1dacff4d6582e2c7` |
| CAP-952 | Continue Architecture Planning.md > v0.29 > 29.31 Two expansion paths | `71d14a7a748fb8ff` | `194a173e7c726600` |
| CAP-953 | Continue Architecture Planning.md > v0.29 > 29.32 Search-space discovery as first-class knowledge | `732f0dd8f62ee3c1` | `c04d35fa9b16c750` |
| CAP-954 | Continue Architecture Planning.md > v0.29 > 29.33 v0.29 invariants | `54c677feeceda125` | `331061cdb330e1ff` |
| CAP-955 | Continue Architecture Planning.md > v0.29 > 29.33 v0.29 invariants > P1 — Discovery does not create authority | `33711fd6f12eb607` | `ec190a53ace6b127` |
| CAP-956 | Continue Architecture Planning.md > v0.29 > 29.33 v0.29 invariants > P2 — Partition proposal is not partition | `17ab23fa66018531` | `1696591f500e289e` |
| CAP-957 | Continue Architecture Planning.md > v0.29 > 29.33 v0.29 invariants > P3 — Every admitted partition belongs to the domain | `444ca3793d2becf2` | `3540c5cb3b70acc8` |
| CAP-958 | Continue Architecture Planning.md > v0.29 > 29.33 v0.29 invariants > P4 — Expansion is budgeted | `d4a720c6e59f97cd` | `c1e9fc35f515e0d0` |
| CAP-959 | Continue Architecture Planning.md > v0.29 > 29.33 v0.29 invariants > P5 — Expansion is depth-bounded | `b3e6a0e04562086e` | `4808d9729a1221e0` |
| CAP-960 | Continue Architecture Planning.md > v0.29 > 29.33 v0.29 invariants > P6 — Duplicate partitions converge | `a56baccdeb5ade73` | `083a27c5e85321fa` |
| CAP-961 | Continue Architecture Planning.md > v0.29 > 29.33 v0.29 invariants > P7 — Overlap is preserved | `1f8c4300048fc153` | `937dec7842f4482b` |
| CAP-962 | Continue Architecture Planning.md > v0.29 > 29.33 v0.29 invariants > P8 — Evidence is preserved | `23415d485114ed73` | `920c680eaf6ecf3a` |
| CAP-963 | Continue Architecture Planning.md > v0.29 > 29.33 v0.29 invariants > P9 — Partition existence does not schedule execution | `15e3d5767b27a521` | `c9696cedde4754d6` |
| CAP-964 | Continue Architecture Planning.md > v0.29 > 29.33 v0.29 invariants > P10 — Expansion cannot override policy | `7ea500e602bd21ad` | `7af32279b87e8f45` |
| CAP-965 | Continue Architecture Planning.md > v0.29 > 29.33 v0.29 invariants > P11 — Search-space versions are immutable | `5d528b842ac785e1` | `d1b3be24bb77e7b7` |
| CAP-966 | Continue Architecture Planning.md > v0.29 > 29.33 v0.29 invariants > P12 — Expansion does not invalidate historical claims automatically | `ea523f111dcbdef6` | `804ae04398b23c47` |
| CAP-967 | Continue Architecture Planning.md > v0.29 > 29.33 v0.29 invariants > P13 — Cycles are legal | `178aba0a32648941` | `921a36e1de7b8834` |
| CAP-968 | Continue Architecture Planning.md > v0.29 > 29.33 v0.29 invariants > P14 — Unknown remains valid | `1457cdac10f27ffe` | `85282c2db65fe89b` |
| CAP-969 | Continue Architecture Planning.md > v0.29 > 29.34 The system after v0.29 | `e80ced6b92780485` | `dc66f8785c35b8de` |
| CAP-970 | Continue Architecture Planning.md > v0.29 > 29.35 Blind-scan interpretation | `173c6a0c923acfb8` | `6a1e6a77e060ecc1` |
| CAP-971 | Continue Architecture Planning.md > v0.29 > v0.29 takeaway | `f44a113257b25590` | `2365024dece2d639` |
| CAP-972 | Continue Architecture Planning.md > v0.30 > v0.30 — Unified Frontier Arbitration | `50ee0d4995fe58fa` | `2c1a142235b1b813` |
| CAP-973 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `873a965344fa3ee3` |
| CAP-974 | Continue Architecture Planning.md > v0.30 > Conclusion — Generic Discovery Engine | `c26eaef98f9eca6b` | `76dc181563e70465` |
| CAP-975 | Continue Architecture Planning.md > v0.30 > Conclusion — Generic Discovery Engine > The final conceptual separation | `06aa14676b5eee0f` | `36fe08afd7abe22b` |
| CAP-976 | Continue Architecture Planning.md > v0.30 > The fundamental invariant | `c6892a46717c326b` | `3faa6b941bebd11e` |
| CAP-977 | Continue Architecture Planning.md > v0.30 > What the DVB analogy actually contributed | `eddd9240079ac046` | `70577180641ea170` |
| CAP-978 | Continue Architecture Planning.md > v0.30 > The most important safety boundary | `e639f15c29c8c448` | `52c6439430c7085e` |
| CAP-979 | Continue Architecture Planning.md > v0.30 > Final architecture | `1009a85ac15d1e9f` | `2ba5e1cfb9fdaf97` |
| CAP-980 | Continue Architecture Planning.md > v0.30 > What the userscript should and should not become | `f3d8fee5e60de50a` | `7e5bf2933c42595a` |
| CAP-981 | Continue Architecture Planning.md > v0.30 > Final principles | `0f3fff8ef37ea65d` | `d2973ea46d60b844` |
| CAP-982 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `4f9b8ead071c6442` |
| CAP-983 | Continue Architecture Planning.md > v0.30 > v0.30 — Unified Frontier Arbitration | `50ee0d4995fe58fa` | `d74a53227472c529` |
| CAP-984 | Continue Architecture Planning.md > v0.30 > v0.30 — Unified Frontier Arbitration > 30.1 The new architecture | `904afd19085188d8` | `6040ecc6ba41f358` |
| CAP-985 | Continue Architecture Planning.md > v0.30 > 30.2 WorkClass | `04dd5bc9f0a8423b` | `d8c72046b8fb6eca` |
| CAP-986 | Continue Architecture Planning.md > v0.30 > 30.3 WorkClassPolicy | `d88f6b3f83c9c11d` | `ee39bcc472461244` |
| CAP-987 | Continue Architecture Planning.md > v0.30 > 30.4 ArbitrationDecision | `d5177515f03e5fbf` | `8a091bc8f5d301ea` |
| CAP-988 | Continue Architecture Planning.md > v0.30 > 30.5 Hard constraints vs soft priorities | `8225eb3a9ed85bef` | `ffe91510bd49a1e6` |
| CAP-989 | Continue Architecture Planning.md > v0.30 > 30.5 Hard constraints vs soft priorities > Hard constraints | `be73db5de5e8d7e0` | `85cea6425eb5562e` |
| CAP-990 | Continue Architecture Planning.md > v0.30 > 30.5 Hard constraints vs soft priorities > Soft priorities | `9e620fb2a8ba82fd` | `39690b66a6fcefe3` |
| CAP-991 | Continue Architecture Planning.md > v0.30 > 30.6 Arbitration score | `28f06c2de8476d47` | `7887afc504fcfafb` |
| CAP-992 | Continue Architecture Planning.md > v0.30 > 30.7 Aging | `342597924edc6e84` | `4ea33c33c24f9181` |
| CAP-993 | Continue Architecture Planning.md > v0.30 > 30.8 Starvation detection | `cc93463864a94155` | `bbda7cfd1c240451` |
| CAP-994 | Continue Architecture Planning.md > v0.30 > 30.9 Class starvation | `1e40fe6b92f76ef2` | `78375bdae4946ecf` |
| CAP-995 | Continue Architecture Planning.md > v0.30 > 30.10 Weighted fairness | `59fe5a2e04df996f` | `a18859a184f1a9a1` |
| CAP-996 | Continue Architecture Planning.md > v0.30 > 30.11 Deficit-style arbitration | `fffc784d4654c9e4` | `677dfeec2540b67c` |
| CAP-997 | Continue Architecture Planning.md > v0.30 > 30.12 Cost-aware scheduling | `6125860a03b1b8e5` | `e82b1f1ee1708c92` |
| CAP-998 | Continue Architecture Planning.md > v0.30 > 30.13 Backpressure | `0e166edaecfa0de6` | `10ff554873ffef04` |
| CAP-999 | Continue Architecture Planning.md > v0.30 > 30.14 Reserved capacity | `7e6447d7f3cc05f9` | `79091fc74ba2d2f6` |
| CAP-1000 | Continue Architecture Planning.md > v0.30 > 30.15 Arbitration pipeline | `c280afa768f12919` | `8588bb6d384809df` |
| CAP-1001 | Continue Architecture Planning.md > v0.30 > 30.16 The atomicity problem | `9486633b6f38365c` | `3825fe5239f613e5` |
| CAP-1002 | Continue Architecture Planning.md > v0.30 > 30.17 Priority inversion | `f5ae54cb4664b1d4` | `17b9a5c003ae96ed` |
| CAP-1003 | Continue Architecture Planning.md > v0.30 > 30.18 FrontierArbitrator | `d52fde9a5b34ab50` | `ad2bea138f986c08` |
| CAP-1004 | Continue Architecture Planning.md > v0.30 > 30.19 Arbitration result | `50fe8427d210bf99` | `5645cdd9d631f2ee` |
| CAP-1005 | Continue Architecture Planning.md > v0.30 > 30.20 Arbitration ledger | `ce6ed2f0e4640222` | `f13d81aa03b8c6d2` |
| CAP-1006 | Continue Architecture Planning.md > v0.30 > 30.21 Replay | `c719ed857ce09553` | `6caef789dbe196ee` |
| CAP-1007 | Continue Architecture Planning.md > v0.30 > 30.22 The deeper invariant | `ac233f763089d26d` | `e669c4d9b8fb168b` |
| CAP-1008 | Continue Architecture Planning.md > v0.30 > 30.23 Full v0.30 architecture | `d05645171acea307` | `a1cadb036a7c85ac` |
| CAP-1009 | Continue Architecture Planning.md > v0.30 > 30.24 Failure taxonomy | `1fe9724760569f23` | `cebd05e94c42f9c4` |
| CAP-1010 | Continue Architecture Planning.md > v0.30 > 30.25 v0.30 invariants | `f57d365e422a0583` | `2cce4e0c5bd5dd6e` |
| CAP-1011 | Continue Architecture Planning.md > v0.30 > 30.26 What v0.30 actually accomplishes | `ee47cc764b34a267` | `17faac3681899b4d` |
| CAP-1012 | Continue Architecture Planning.md > v0.30 > Next boundary — v0.31 | `10b966f6486c521a` | `5343ef569c64f1ba` |
| CAP-1013 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `31fbef162594de01` |
| CAP-1014 | Continue Architecture Planning.md > v0.31 > v0.31 — Unified Resource & Cost Ledger | `a6cbdebb7a28aaea` | `e7480b1aaf0fa4d8` |
| CAP-1015 | Continue Architecture Planning.md > v0.31 > v0.31 — Unified Resource & Cost Ledger > 31.1 Resource dimensions | `7088b13b8b11e2d1` | `b5c6632aba3bcf8b` |
| CAP-1016 | Continue Architecture Planning.md > v0.31 > 31.2 ResourceBudget | `c342df742d8a04d8` | `f1a0311423579a12` |
| CAP-1017 | Continue Architecture Planning.md > v0.31 > 31.3 Three resource states | `c12a77c2b34cf689` | `0902425eedec0af5` |
| CAP-1018 | Continue Architecture Planning.md > v0.31 > 31.4 ResourceReservation | `e65fbc610ea2a360` | `dcf6e4e7be92e806` |
| CAP-1019 | Continue Architecture Planning.md > v0.31 > 31.5 Estimated cost vs actual cost | `81fe2e836580fa48` | `bfc6a20e1c5a2af4` |
| CAP-1020 | Continue Architecture Planning.md > v0.31 > 31.6 CostObservation | `4081eb3203df1296` | `020dfa3e1c200e16` |
| CAP-1021 | Continue Architecture Planning.md > v0.31 > 31.7 ResourceLedger | `bab779807525af0e` | `91dc42f25a3e4756` |
| CAP-1022 | Continue Architecture Planning.md > v0.31 > 31.8 Budget scopes | `b5b7b244c71382c9` | `0ec3fb10eb988127` |
| CAP-1023 | Continue Architecture Planning.md > v0.31 > 31.9 Hierarchical budget accounting | `dff03fcf81ed3d52` | `91c60d6f3531a4e0` |
| CAP-1024 | Continue Architecture Planning.md > v0.31 > 31.10 Resource allocation | `ef3cd19232f78f82` | `08a875d56d483284` |
| CAP-1025 | Continue Architecture Planning.md > v0.31 > 31.11 Allocation is not execution | `a03c4e4e1dea7fd7` | `c2bf200260561727` |
| CAP-1026 | Continue Architecture Planning.md > v0.31 > 31.12 Partial consumption | `e0d593f4b63eb2e6` | `46bfd07d82d276cc` |
| CAP-1027 | Continue Architecture Planning.md > v0.31 > 31.13 Cost overruns | `6cab4155a63f8fd6` | `4dab060b66e852bc` |
| CAP-1028 | Continue Architecture Planning.md > v0.31 > 31.14 Cost model | `05621a23ed3bccaa` | `27b223c67f9451c5` |
| CAP-1029 | Continue Architecture Planning.md > v0.31 > 31.15 Cost is context-dependent | `72f9ac33d7303cb4` | `06bbde828eb3ac0b` |
| CAP-1030 | Continue Architecture Planning.md > v0.31 > 31.16 Resource exhaustion | `23caff0ec71581d3` | `58f53bc11f8dcde0` |
| CAP-1031 | Continue Architecture Planning.md > v0.31 > 31.17 Budget exhaustion vs frontier exhaustion | `0fea9e73a13eb8a5` | `1e6c6756343228bd` |
| CAP-1032 | Continue Architecture Planning.md > v0.31 > 31.18 Resource reservation race | `526fe2289806da58` | `ecbf3f232af2e7dd` |
| CAP-1033 | Continue Architecture Planning.md > v0.31 > 31.19 Settlement | `f71e5247406982c2` | `820da57b66f27c29` |
| CAP-1034 | Continue Architecture Planning.md > v0.31 > 31.20 Cost feedback | `5213915a4919e075` | `abe7797d567f8667` |
| CAP-1035 | Continue Architecture Planning.md > v0.31 > 31.21 ResourceLedger events | `137d1e59d81650ec` | `c28dd1d60ba96cf0` |
| CAP-1036 | Continue Architecture Planning.md > v0.31 > 31.22 Resource accounting and provenance | `be3f7e3a7405ab15` | `31445bc1a4871b41` |
| CAP-1037 | Continue Architecture Planning.md > v0.31 > 31.23 Unified v0.31 architecture | `99589469701184da` | `5091e154405253f8` |
| CAP-1038 | Continue Architecture Planning.md > v0.31 > 31.24 The central v0.31 invariants | `46ffc59840d249b8` | `edfc58966ee174ef` |
| CAP-1039 | Continue Architecture Planning.md > v0.31 > 31.25 What v0.31 adds | `6dc716de9dc454ec` | `7496a8662d05f5bf` |
| CAP-1040 | Continue Architecture Planning.md > v0.32 > v0.32 boundary | `3a2c9d491f57ddba` | `fe6d14facd06c972` |
| CAP-1041 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `31fbef162594de01` |
| CAP-1042 | Continue Architecture Planning.md > v0.32 > v0.32 — Transactional Persistence & Crash Recovery | `e84a63345a7a07e5` | `3be4374c59e60b09` |
| CAP-1043 | Continue Architecture Planning.md > v0.32 > v0.32 — Transactional Persistence & Crash Recovery > 32.1 The crash problem | `f43c0f63ba2ebc4e` | `c427435efa3d5cec` |
| CAP-1044 | Continue Architecture Planning.md > v0.32 > 32.2 Durable state vs runtime state | `13106fe452f74fbd` | `9913836e77e27b97` |
| CAP-1045 | Continue Architecture Planning.md > v0.32 > 32.3 Persistence is not serialization | `0778d230463d367b` | `fa277960adb5ff92` |
| CAP-1046 | Continue Architecture Planning.md > v0.32 > 32.4 PersistenceAdapter | `40a5950dd100e8fe` | `9ed3a640fce6b062` |
| CAP-1047 | Continue Architecture Planning.md > v0.32 > 32.5 Transaction | `9f4792aa6d33f544` | `9d09f77950858c44` |
| CAP-1048 | Continue Architecture Planning.md > v0.32 > 32.6 Write-ahead event ledger | `5c2b377f3f99d427` | `049681cc3d8084f4` |
| CAP-1049 | Continue Architecture Planning.md > v0.32 > 32.7 Event identity | `3f51fce9a7ce913b` | `230b66d0b413491b` |
| CAP-1050 | Continue Architecture Planning.md > v0.32 > 32.8 Monotonic sequence | `819edc0ceef45a7d` | `ce87777c477bb157` |
| CAP-1051 | Continue Architecture Planning.md > v0.32 > 32.9 Commit protocol | `6af4fba9a37c0256` | `9727d4de709fa0c2` |
| CAP-1052 | Continue Architecture Planning.md > v0.32 > 32.10 Commit markers | `8689fb56a9a05bbd` | `53f99109b962acd5` |
| CAP-1053 | Continue Architecture Planning.md > v0.32 > 32.11 Checkpoint correctness | `888c10bdb7e3e8e6` | `813cdea055f3d5f0` |
| CAP-1054 | Continue Architecture Planning.md > v0.32 > 32.12 At-least-once vs exactly-once | `cd133b8bf71ef158` | `b6b0561441655f96` |
| CAP-1055 | Continue Architecture Planning.md > v0.32 > 32.13 Idempotency | `a7dccd142dd628cd` | `32fcea98abf49661` |
| CAP-1056 | Continue Architecture Planning.md > v0.32 > 32.14 Work recovery | `e34e8d1df40b8844` | `e4941bcaa79ac0bc` |
| CAP-1057 | Continue Architecture Planning.md > v0.32 > 32.15 Recovery scan | `bc96d42edf562807` | `89a68cb9ebad6c4d` |
| CAP-1058 | Continue Architecture Planning.md > v0.32 > 32.16 RecoveryManager | `01ba16c4b7422a14` | `35f1cf48bbbb070d` |
| CAP-1059 | Continue Architecture Planning.md > v0.32 > 32.17 Reservation recovery | `96adcab9d2e284fa` | `ce736ffa4c05efcc` |
| CAP-1060 | Continue Architecture Planning.md > v0.32 > 32.18 Accounting invariant under crash | `ae1f3a2f6e29c960` | `98a04c692c4a0803` |
| CAP-1061 | Continue Architecture Planning.md > v0.32 > 32.19 Observation recovery | `f923e810a200cfa1` | `ea838aff560e7776` |
| CAP-1062 | Continue Architecture Planning.md > v0.32 > 32.20 Artifact durability | `c99a69a7e8ee65ff` | `d313123492b0ea2d` |
| CAP-1063 | Continue Architecture Planning.md > v0.32 > 32.21 Durable checkpoint | `1ff5de6bed2843bc` | `a27b73f0a1f79568` |
| CAP-1064 | Continue Architecture Planning.md > v0.32 > 32.22 Recovery invariant for cursors | `6bbe5de822a14922` | `84e13cf56e76b5d8` |
| CAP-1065 | Continue Architecture Planning.md > v0.32 > 32.23 Schema versioning | `f45de563b034119c` | `87f310b503e1715a` |
| CAP-1066 | Continue Architecture Planning.md > v0.32 > 32.24 Snapshot + journal | `ee465292bf4ba8dc` | `f869264adb9a8863` |
| CAP-1067 | Continue Architecture Planning.md > v0.32 > 32.25 Snapshot integrity | `ac8dc618fea43474` | `4676cd75a4e6baaf` |
| CAP-1068 | Continue Architecture Planning.md > v0.32 > 32.26 Recovery outcomes | `c37c2762756287e7` | `9aaf3b78b4153390` |
| CAP-1069 | Continue Architecture Planning.md > v0.32 > 32.27 Recovery must not fabricate knowledge | `536c7bb5c41ec8b3` | `b0f74760cd511b97` |
| CAP-1070 | Continue Architecture Planning.md > v0.32 > 32.28 Crash-safe frontier | `4d1183c245fd2170` | `d3a8bfaad420d934` |
| CAP-1071 | Continue Architecture Planning.md > v0.32 > 32.29 Reconciliation | `9ad2002e8de2885c` | `47ccaa79188c30ab` |
| CAP-1072 | Continue Architecture Planning.md > v0.32 > 32.30 Repair is itself provenance | `5a26ed5ddeea9dc6` | `414d5a1d891405e8` |
| CAP-1073 | Continue Architecture Planning.md > v0.32 > 32.31 v0.32 architecture | `d01496a4ff3fe2f6` | `5517329f7b8c1c20` |
| CAP-1074 | Continue Architecture Planning.md > v0.32 > 32.32 Complete lifecycle | `4237f29f9b617855` | `887534ed0f1533e6` |
| CAP-1075 | Continue Architecture Planning.md > v0.32 > 32.33 Failure taxonomy | `4ee3bd1fa42b6a97` | `f3397a3e0f8e113b` |
| CAP-1076 | Continue Architecture Planning.md > v0.32 > 32.34 v0.32 invariants | `a62db136a1508dfc` | `a568782f5f23b0d3` |
| CAP-1077 | Continue Architecture Planning.md > v0.32 > 32.35 What v0.32 changes | `a98853ecd999abaf` | `a3c3b666ef84f4c6` |
| CAP-1078 | Continue Architecture Planning.md > v0.33 > v0.33 — Multi-Worker / Multi-Context Coordination | `06d94e02394836b1` | `3ecb56dc9f3ecb0b` |
| CAP-1079 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `31fbef162594de01` |
| CAP-1080 | Continue Architecture Planning.md > v0.33 > v0.33 — Multi-Worker Coordination & Distributed Claiming | `ee47614190d45c6e` | `a7bc9f7c77311132` |
| CAP-1081 | Continue Architecture Planning.md > v0.33 > v0.33 — Multi-Worker Coordination & Distributed Claiming > 33.1 Worker identity | `ee4e1a6cf915ec2a` | `4237f23ac081dea7` |
| CAP-1082 | Continue Architecture Planning.md > v0.33 > 33.2 Worker registration | `646bd628fa9e4f9a` | `2202fdacd1acac04` |
| CAP-1083 | Continue Architecture Planning.md > v0.33 > 33.3 Worker capabilities | `d5f07b275c58aa9f` | `a8e401c528dde7dc` |
| CAP-1084 | Continue Architecture Planning.md > v0.33 > 33.4 Claiming is the synchronization boundary | `9ec1fb987d5bb678` | `dbc56d56cf567f3b` |
| CAP-1085 | Continue Architecture Planning.md > v0.33 > 33.5 ClaimToken | `9a8f9000c9e4c2c9` | `46376d5b429aff8d` |
| CAP-1086 | Continue Architecture Planning.md > v0.33 > 33.6 Claim ≠ lease | `73275a23523b1b2e` | `9b0dd7e2d2b7a7b7` |
| CAP-1087 | Continue Architecture Planning.md > v0.33 > 33.7 Lease lifecycle | `d8dc1ee71c3c9bba` | `5a74f9b5a6cf797c` |
| CAP-1088 | Continue Architecture Planning.md > v0.33 > 33.8 LeaseManager | `8ad19a6d49b535a4` | `438252a72acb4234` |
| CAP-1089 | Continue Architecture Planning.md > v0.33 > 33.9 Heartbeats | `e70d7fcd9c3e0de3` | `465530e05b616072` |
| CAP-1090 | Continue Architecture Planning.md > v0.33 > 33.10 Fencing tokens | `6a06264a8a01a9f4` | `5e4a3022359f660f` |
| CAP-1091 | Continue Architecture Planning.md > v0.33 > 33.11 Fencing invariant | `34db3d08545394b5` | `4fa06635752c14e7` |
| CAP-1092 | Continue Architecture Planning.md > v0.33 > 33.12 Worker death | `a6bc76a5d69bb879` | `ee8ac4e317e0720a` |
| CAP-1093 | Continue Architecture Planning.md > v0.33 > 33.13 Duplicate execution | `8232ed1d1ea692c9` | `6ce5f5fd5034fd3d` |
| CAP-1094 | Continue Architecture Planning.md > v0.33 > 33.14 Execution identity | `48ecdaa61150adce` | `ff5d0bf702908313` |
| CAP-1095 | Continue Architecture Planning.md > v0.33 > 33.15 Duplicate observations | `6d5624b5b0943778` | `7bc4f88d7d3d2807` |
| CAP-1096 | Continue Architecture Planning.md > v0.33 > 33.16 Duplicate execution ≠ independent evidence | `2f738ac37a4fc92b` | `594a24efe208652f` |
| CAP-1097 | Continue Architecture Planning.md > v0.33 > 33.17 Worker-local vs shared state | `27f3d2d35f56ec10` | `6c95844372a7e0f0` |
| CAP-1098 | Continue Architecture Planning.md > v0.33 > 33.18 CoordinationManager | `4a08f02583bdd1ae` | `9575b8ab7d9a758d` |
| CAP-1099 | Continue Architecture Planning.md > v0.33 > 33.19 Coordination vs arbitration | `488a0fb3e1e64c1a` | `d64819c5e14d03be` |
| CAP-1100 | Continue Architecture Planning.md > v0.33 > 33.20 Worker selection | `355fcc6e09fa1425` | `8f1bc210c3178330` |
| CAP-1101 | Continue Architecture Planning.md > v0.33 > 33.21 Worker affinity | `a770d63321dac424` | `9d0a2d6f3f411658` |
| CAP-1102 | Continue Architecture Planning.md > v0.33 > 33.22 Worker capacity | `df13ecdb0301ce0d` | `e9260795fffb6948` |
| CAP-1103 | Continue Architecture Planning.md > v0.33 > 33.23 Distributed accounting | `f3f82f1b2cb4f174` | `9151207456ceb505` |
| CAP-1104 | Continue Architecture Planning.md > v0.33 > 33.24 Worker-local caches | `461570e2961eb37a` | `6de676f46b25138b` |
| CAP-1105 | Continue Architecture Planning.md > v0.33 > 33.25 Cross-worker event ordering | `10bd7573820d2c65` | `a43df5937c1294a0` |
| CAP-1106 | Continue Architecture Planning.md > v0.33 > 33.26 Causal provenance | `23d24b8865ea6418` | `0977c7cade0de951` |
| CAP-1107 | Continue Architecture Planning.md > v0.33 > 33.27 Coordination events | `45c1e306c48f8499` | `fec1fae8f4cab444` |
| CAP-1108 | Continue Architecture Planning.md > v0.33 > 33.28 Multi-worker failure modes | `c6d93e726f5da8c0` | `26135ab426742a56` |
| CAP-1109 | Continue Architecture Planning.md > v0.33 > 33.29 Split-brain | `a2108e0581349600` | `2bab5a9f83e2e75c` |
| CAP-1110 | Continue Architecture Planning.md > v0.33 > 33.30 What the browser prototype can guarantee | `76e6742b074fa0f8` | `7bbfc9e46db7b3c6` |
| CAP-1111 | Continue Architecture Planning.md > v0.33 > 33.31 Coordination scope | `5f7283124f0a4826` | `4373c09cbfe3a48d` |
| CAP-1112 | Continue Architecture Planning.md > v0.33 > 33.32 v0.33 architecture | `eea48c0e42d743a1` | `aa290fc20bea9e73` |
| CAP-1113 | Continue Architecture Planning.md > v0.33 > 33.33 The complete ownership invariant | `a0d809e2ab35917e` | `4a16d9d8afa4c6cb` |
| CAP-1114 | Continue Architecture Planning.md > v0.33 > 33.34 The deeper distributed invariant | `c59552fa9c41c60d` | `236689f75ae78dba` |
| CAP-1115 | Continue Architecture Planning.md > v0.33 > 33.35 v0.33 result | `1a64e418bddc6854` | `a893407dedc0a8aa` |
| CAP-1116 | Continue Architecture Planning.md > v0.34 > v0.34 — Coordination Protocol & Distributed Consistency | `7ba322357fca7127` | `8a4153823981d569` |
| CAP-1117 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `31fbef162594de01` |
| CAP-1118 | Continue Architecture Planning.md > v0.34 > v0.34 — Distributed Consistency & Conflict Resolution | `d24abe7f82c9f60d` | `f61b73d00560847f` |
| CAP-1119 | Continue Architecture Planning.md > v0.34 > 34.1 New Architecture Boundary | `bc1ebe7239685847` | `41c2d0e2da783be0` |
| CAP-1120 | Continue Architecture Planning.md > v0.34 > 34.2 The Core Consistency Model | `6fa59592adacbbc1` | `2c733a0531919fe4` |
| CAP-1121 | Continue Architecture Planning.md > v0.34 > 34.3 Optimistic Concurrency Control | `ea080838b73ba648` | `e52d8cebfce3922a` |
| CAP-1122 | Continue Architecture Planning.md > v0.34 > 34.4 Version ≠ Time | `c05e4196daff24ba` | `158427430dcc3697` |
| CAP-1123 | Continue Architecture Planning.md > v0.34 > 34.5 Event Metadata | `e038de16491d8fd4` | `7a4d2da58c213ef4` |
| CAP-1124 | Continue Architecture Planning.md > v0.34 > 34.6 Versioning + Fencing | `18aa5c49616cf083` | `d88f5162fa056a78` |
| CAP-1125 | Continue Architecture Planning.md > v0.34 > 34.7 Conflict Is Not One Thing | `3e7997c200a427c5` | `3996a69a9a882992` |
| CAP-1126 | Continue Architecture Planning.md > v0.34 > 34.7 Conflict Is Not One Thing > Claim conflict | `b70494b63ede957b` | `bb4b793eec719b7e` |
| CAP-1127 | Continue Architecture Planning.md > v0.34 > 34.7 Conflict Is Not One Thing > Candidate conflict | `4e50696acb5e700f` | `d265c880f524ffa7` |
| CAP-1128 | Continue Architecture Planning.md > v0.34 > 34.7 Conflict Is Not One Thing > Classification conflict | `4f71b7a6f4311dba` | `281a6b912d9cefaa` |
| CAP-1129 | Continue Architecture Planning.md > v0.34 > 34.7 Conflict Is Not One Thing > Coverage conflict | `4d00389cb2ab8275` | `7bdc8350e660f116` |
| CAP-1130 | Continue Architecture Planning.md > v0.34 > 34.7 Conflict Is Not One Thing > Budget conflict | `77ea05cfbda5e899` | `b9239283726dbb8c` |
| CAP-1131 | Continue Architecture Planning.md > v0.34 > 34.8 Conflict Record | `ddd63c5c38974e86` | `56fdb3bcc8c1d4fb` |
| CAP-1132 | Continue Architecture Planning.md > v0.34 > 34.9 Deterministic Conflict Resolver | `a96666680cb6daeb` | `359161a7d2f9fa5d` |
| CAP-1133 | Continue Architecture Planning.md > v0.34 > 34.10 Resolution Policies | `32638e392a9b1b39` | `814015944fd6580b` |
| CAP-1134 | Continue Architecture Planning.md > v0.34 > 34.11 Classification Conflict | `48be677049f68e45` | `93c044b4956f9e52` |
| CAP-1135 | Continue Architecture Planning.md > v0.34 > 34.12 Provenance Must Survive Resolution | `454de4008820fa58` | `298f34f23fdf7eeb` |
| CAP-1136 | Continue Architecture Planning.md > v0.34 > 34.13 Last-Write-Wins Is Not the Default | `9c09d3cfa71e156c` | `432bd14f691f841e` |
| CAP-1137 | Continue Architecture Planning.md > v0.34 > 34.14 Append-Only Is Especially Powerful | `00928d27202a95ff` | `2b482fac33fca349` |
| CAP-1138 | Continue Architecture Planning.md > v0.34 > 34.15 Materialized State | `175ede4363b4e36e` | `6f446d4da57e215c` |
| CAP-1139 | Continue Architecture Planning.md > v0.34 > 34.16 State Digest | `e531617e0436fdd8` | `2a9233b36a4e6470` |
| CAP-1140 | Continue Architecture Planning.md > v0.34 > 34.17 Conflict Detection Pipeline | `e42c3383287de3a8` | `77871bb8c85cce40` |
| CAP-1141 | Continue Architecture Planning.md > v0.34 > 34.18 Conflict Detection vs Conflict Resolution | `5ad80fb4098032fe` | `837478263583bc79` |
| CAP-1142 | Continue Architecture Planning.md > v0.34 > 34.19 Conflict Resolver Context | `9c0007e58e55ee1f` | `06dcebd4ca0922bd` |
| CAP-1143 | Continue Architecture Planning.md > v0.34 > 34.20 Resolution Event | `54e9d59fd73fcafa` | `138f79536839c001` |
| CAP-1144 | Continue Architecture Planning.md > v0.34 > 34.21 Cross-Object Conflicts | `a9ca47112c6830d9` | `f4ac9233735ce5f1` |
| CAP-1145 | Continue Architecture Planning.md > v0.34 > 34.22 Consistency Domains | `334f8d7baefd0dd5` | `ccca1d0165c7e424` |
| CAP-1146 | Continue Architecture Planning.md > v0.34 > 34.23 Consistency Is Not Global Ordering | `0a44172ea1b833b9` | `41ef144099604f43` |
| CAP-1147 | Continue Architecture Planning.md > v0.34 > 34.24 Independent Evidence | `1d8c2b2492e55322` | `d07f56575b8b529f` |
| CAP-1148 | Continue Architecture Planning.md > v0.34 > 34.25 Failure Taxonomy | `e2159ee41f3dfdf5` | `313bcf8a20fab528` |
| CAP-1149 | Continue Architecture Planning.md > v0.34 > 34.26 New Core Invariants | `de1602b730976523` | `4cb24c491deea645` |
| CAP-1150 | Continue Architecture Planning.md > v0.34 > 34.26 New Core Invariants > Consistency | `36e8309d0868e112` | `bebc3a16412fe12a` |
| CAP-1151 | Continue Architecture Planning.md > v0.34 > 34.26 New Core Invariants > Fencing | `be34540662047b2a` | `ac87d83408975726` |
| CAP-1152 | Continue Architecture Planning.md > v0.34 > 34.26 New Core Invariants > Conflict | `014659ab9d98c8fe` | `92cda685b50ba3aa` |
| CAP-1153 | Continue Architecture Planning.md > v0.34 > 34.26 New Core Invariants > Provenance | `1c4b8ff60530a1bf` | `f37a57d1619c9312` |
| CAP-1154 | Continue Architecture Planning.md > v0.34 > 34.26 New Core Invariants > Recovery | `48f6a8d5688b0cf5` | `cdadf721a1698ead` |
| CAP-1155 | Continue Architecture Planning.md > v0.34 > 34.26 New Core Invariants > Scalability | `814fe33f11b361fc` | `9b8928f9613c1091` |
| CAP-1156 | Continue Architecture Planning.md > v0.34 > 34.27 The Unified State Model | `9be77f85b45873ac` | `14e90c0e00bb39d2` |
| CAP-1157 | Continue Architecture Planning.md > v0.34 > 34.28 What v0.34 Actually Proves | `5b62e6775365a28c` | `937ad0232ec3ce5e` |
| CAP-1158 | Continue Architecture Planning.md > v0.34 > 34.28 What v0.34 Actually Proves > PROVED by the architecture | `b5fe0bc2963a686a` | `cec82a2966710e0f` |
| CAP-1159 | Continue Architecture Planning.md > v0.34 > 34.28 What v0.34 Actually Proves > ARGUMENT | `4bfae6d732b2e5ca` | `87b4cba2dbc83754` |
| CAP-1160 | Continue Architecture Planning.md > v0.34 > 34.28 What v0.34 Actually Proves > OPEN | `6e10953f3e4ca159` | `17aa1918a586a826` |
| CAP-1161 | Continue Architecture Planning.md > v0.34 > 34.29 Prototype Boundary | `06298f5e52b9b43b` | `29e9cd777aba8516` |
| CAP-1162 | Continue Architecture Planning.md > v0.34 > 34.30 v0.34 → v0.35 | `f24944262a29fc36` | `6ea433d2699de359` |
| CAP-1163 | Continue Architecture Planning.md > lead-in | `e3b0c44298fc1c14` | `aaf40ec2eebcbff6` |
| CAP-1164 | Continue Architecture Planning.md > v0.34 > Conclusion — Generic Discovery Engine | `c26eaef98f9eca6b` | `e084e2289a79a797` |
| CAP-1165 | Continue Architecture Planning.md > v0.34 > Conclusion — Generic Discovery Engine > The decisive conceptual shift | `15c1da9e92c914d0` | `71323e286789654e` |
| CAP-1166 | Continue Architecture Planning.md > v0.34 > Conclusion — Generic Discovery Engine > The decisive conceptual shift > DVB blind scan | `30bd46f39c4b5089` | `91f0b953ce42fbdd` |
| CAP-1167 | Continue Architecture Planning.md > v0.34 > Conclusion — Generic Discovery Engine > The decisive conceptual shift > Generic discovery | `2d04049845309adf` | `d0291b804b4c2a56` |
| CAP-1168 | Continue Architecture Planning.md > v0.34 > The major architectural invariants | `0e7f42fa89b38c4c` | `8767f8c9ec610f0a` |
| CAP-1169 | Continue Architecture Planning.md > v0.34 > Final architecture by responsibility | `e76cab3ba32440d3` | `0cbb04c266393848` |
| CAP-1170 | Continue Architecture Planning.md > v0.34 > What the prototype actually becomes | `16c01a4ff5c61762` | `06d940eb297aa955` |
| CAP-1171 | Continue Architecture Planning.md > v0.34 > Final formulation | `9dda9e2767936570` | `d219b9a5a28edad6` |

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

## Related Documents

- [Documentation index](README.md)
- [Review Notes](REVIEW-NOTES.md)
- [Prototype Overview](prototype/overview.md)
- [Architecture Overview](architecture/overview.md)

