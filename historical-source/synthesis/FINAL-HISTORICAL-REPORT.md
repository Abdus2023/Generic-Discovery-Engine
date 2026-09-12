# Final Historical Report — Generic Discovery Engine

> **Acceptance: PROVISIONAL_ONLY_UPSTREAM_BLOCKED.** Protocol-v1 raw/range validation fails and Protocol-v4 through Protocol-v7 outputs are absent. `SUPPORTED` in this report is source-local and does not mean the full v1→v9 chain is verified. Missing dimensions remain `UNKNOWN`.

## Executive conclusion

The earliest recovered complete architecture, **v0.1.0**, is already a candidate-centric recursive discovery engine rather than a URL-only precursor. At source-local `SUPPORTED` confidence it represents Candidate identity, web acquisition, structured Observation, separable recognition, Discovery, discovery-to-candidate expansion, revisiting scheduling, duplicate-management state, and an entry-to-output workflow. It is also the earliest recovered occurrence classified `LIKELY_EXECUTABLE`, although historical execution is `UNKNOWN`.

The architecture then becomes multi-provider and explicitly claimed (v0.2), adds bounded retries and controller-based timeout handling (v0.3), branches into richer provider, provenance, error-containment, and observability experiments (v0.4-v0.6), and reaches an explicit policy/plan/decision-ledger recomposition at v0.7.1. This sequence is not asserted to be one linear source lineage.

**Full historical acceptance is impossible here:** Protocol-v1 byte/range validation fails, Protocol-v4-v7 outputs are absent, and Protocol-v8 is provisional. Contract-driven onset therefore remains `UNKNOWN`.

## Strict earliest-generic definition A-H

| Condition | v0.1.0 result | Confidence | Provenance |
|---|---|---|---|
| A | Strict-generic condition A: stable discovery identity is represented in v0.1.0. | SUPPORTED | `claim-generic-a` |
| B | Strict-generic condition B: executable acquisition code is represented in the statically parseable occurrence in v0.1.0. | SUPPORTED | `claim-generic-b` |
| C | Strict-generic condition C: structured Observation is represented in v0.1.0. | SUPPORTED | `claim-generic-c` |
| D | Strict-generic condition D: recognition is separable from acquisition in v0.1.0. | SUPPORTED | `claim-generic-d` |
| E | Strict-generic condition E: discoveries can yield new candidates in v0.1.0. | SUPPORTED | `claim-generic-e` |
| F | Strict-generic condition F: scheduled revisiting/repetition is represented in v0.1.0. | SUPPORTED | `claim-generic-f` |
| G | Strict-generic condition G: duplicate-management and scheduling state are represented in v0.1.0. | SUPPORTED | `claim-generic-g` |
| H | Strict-generic condition H: an entry-to-discovery/output-state path is represented in v0.1.0. | SUPPORTED | `claim-generic-h` |

The strict result is **v0.1.0 (SUPPORTED, source-local, prerequisite-blocked)**. This is not silently upgraded to `PROVED`; the conjunctive dependency is `claim-earliest-generic`.

## Version-by-version model

| Version | What it became | Historical caution | Provenance |
|---|---|---|---|
| v0.1.0 | Candidate-centric closed web discovery loop with structured observations, recognition, discoveries, expansion, worker scheduling, duplicate state, and knowledge storage | Historical runtime unknown | `claim-version-v010`; `state-snapshot-0001` |
| v0.2.0 | Reusable multi-provider interpretation plus explicit candidate claiming | Cause mostly unknown | `claim-version-v020`; `state-snapshot-0003` |
| v0.3.0 | Claimed provider pipeline with bounded retries and controller-based timeout handling | No historical tests | `claim-version-v030`; `state-snapshot-0005` |
| v0.4.0 | Divergent richer-provider/provenance/error-handling architectures | Two complete alternatives; no canonical branch | `claim-version-v040`; states 0006/0008 |
| v0.5.0 | Further provider, resource, and observability divergence | Three variants; one exact occurrence is non-executable | `claim-version-v050`; states 0007/0009/0011 |
| v0.6.0 | Broader provider and policy/diagnostic/resource-control experiments | Three variants; lineage unknown | `claim-version-v060`; states 0010/0012/0013 |
| v0.7.1 | Policy/plan/decision-ledger recomposition around acquisition and provider execution | Contract validation unavailable | `claim-version-v071`; `state-snapshot-0014` |

## Twenty final historical questions

| # | Question | Answer | Status | Provenance |
|---|---|---|---|---|
| 1 | What is the earliest runnable architecture? | v0.1.0 is earliest `LIKELY_EXECUTABLE`; historical execution is `UNKNOWN`. | SUPPORTED | `claim-earliest-runnable` |
| 2 | What is the earliest generic architecture under A-H? | v0.1.0 satisfies all eight represented-mechanism conditions. | SUPPORTED | `claim-earliest-generic` + A-H dependencies |
| 3 | What is the earliest contract-driven architecture? | Unavailable because Protocol-v7 is absent. | UNKNOWN | `claim-earliest-contract` |
| 4 | What was the first coherent architecture? | v0.1.0, already candidate-centric and recursively closed. | SUPPORTED | `claim-version-v010` |
| 5 | When did reusable provider extensibility emerge? | v0.2.0 is the first recovered multi-provider abstraction occurrence. | SUPPORTED | `claim-version-v020` |
| 6 | When did discovery become recursively closed? | Already represented in v0.1.0 through expansion and revisiting. | SUPPORTED | `claim-closure` |
| 7 | Is closure exhaustive? | No exhaustive-completeness proof exists; asserting it is contradicted by bounded, provider-dependent search. | CONTRADICTED | `claim-exhaustive-closure` |
| 8 | How did scheduling evolve? | Persistent queue/knowledge revisiting gains explicit claiming, retry/backoff, cancellation, and policy/resource controls in varying variants. | SUPPORTED | `EVOLUTION-EVENTS.yaml` scheduler events |
| 9 | How did acquisition evolve? | Web acquisition persists while implementation varies from userscript/fetch-shaped mechanisms to explicit policy/plan structures. | SUPPORTED | `PROVIDER-AND-ACQUISITION-EVOLUTION.md` + event records |
| 10 | How did observation evolve? | Structured Observation exists at v0.1; later variants enrich network, diagnostic, trace, and decision context. | SUPPORTED | `OBSERVATION-PROVENANCE-EVOLUTION.md`; state vectors |
| 11 | How did provenance evolve? | Candidate-observation-discovery links persist and later grow graph/trace/ledger forms; integrity remains unproved. | SUPPORTED | `OBSERVATION-PROVENANCE-EVOLUTION.md`; state vectors |
| 12 | How did failure handling evolve? | Local catches and status handling expand into retries, cancellation, varying recognition error containment, and structured diagnostics, unevenly by branch. | SUPPORTED | `FAILURE-EVENTS.yaml`; event records |
| 13 | How did concurrency evolve? | Worker concurrency exists early; explicit atomic claiming and origin/resource controls address additional coordination surfaces. | SUPPORTED | state vectors; claim events |
| 14 | How did security evolve? | Trust, authority, parser, and resource mechanisms become more explicit, but mechanisms are not guarantees. | SUPPORTED | `CONTRACT-SECURITY-INTEGRATION.md`; Protocol-v8 records |
| 15 | Which invariants survived? | Candidate work identity, acquisition-before-interpretation, Observation/Discovery separation, expansion, revisiting, and web coupling recur. | INFERRED | `INVARIANTS.yaml` |
| 16 | Where did architectures diverge? | Most visibly across v0.4-v0.6 complete alternatives and acquisition/provider forms. | SUPPORTED | `CONVERGENCE-AND-DIVERGENCE.md`; occurrence states |
| 17 | Which concepts were abandoned or reintroduced? | None can be proved abandoned/reintroduced; disappearance and recurrence preserve identity uncertainty. | UNKNOWN | `CONCEPT-GENEALOGY.yaml` |
| 18 | What pressures caused transitions? | Duplicate coordination, failure continuation, bounded resources, provider growth, provenance, and inspectability are mechanism-supported pressures; authorial intent is mostly unknown. | SUPPORTED | `CAUSAL-CLAIMS.yaml` |
| 19 | What was tested and stabilized historically? | No verified historical test lineage or stabilization point is available. | UNKNOWN | `CONCEPT-GENEALOGY.yaml`; `PLANNED-VS-IMPLEMENTED.md` |
| 20 | What did the system ultimately become? | By v0.7.1 it is a web-coupled, candidate-centric, recursive, provider-extensible discovery engine with explicit acquisition policy/plans and decision records—not yet a proved protocol-independent or contract-verified engine. | SUPPORTED | `claim-version-v071` |

Machine-resolvable evidence identifiers for claim records are in `CLAIMS.yaml`; every identifier resolves through `HISTORICAL-CLAIMS-GRAPH.json` to `EVIDENCE-LEDGER.yaml`.

## Causal reconstruction

The corpus records 34 atomic adjacent-version events and 34 corresponding causal assessments: SUPPORTED=2, UNKNOWN=32. Most causal labels remain `UNKNOWN`; alternatives are explicit in `CAUSAL-CLAIMS.yaml`.

## Maturity without collapse

| Axis | Terminal recovered state | Confidence |
|---|---|---|
| Architecture | Policy/plan/ledger candidate-centric pipeline | SUPPORTED |
| Algorithm | Recursive bounded work loop; exhaustive convergence unproved | SUPPORTED |
| Contracts | Unavailable Protocol-v7 integration | UNKNOWN |
| Execution | v0.7.1 likely executable; historical runtime unknown | SUPPORTED / UNKNOWN |
| Providers | Broad multi-provider family | SUPPORTED |
| Provenance/observability | Structured records and ledger-shaped visibility | SUPPORTED |
| Security | Mechanisms and boundaries modeled; guarantees limited | SUPPORTED |
| Testing/stability | No verified historical evidence | UNKNOWN |

## Contradictions and uncertainty

Four contradictions or input-consistency conflicts are preserved: broken v1 bytes/ranges, v3's internal pass over that broken chain, an exact v0.5 variant that fails parsing, and absent required v4-v7 outputs. Fifteen major uncertainties remain registered. Nothing was repaired or filled.

## Acceptance

- Protocol-v8 validation: `87/87 PASS`, acceptance `PROVISIONAL_ONLY_UPSTREAM_BLOCKED`.
- Protocol-v9 corpus disposition (even when internal checks pass): `PROVISIONAL_ONLY_UPSTREAM_BLOCKED`; independent results are recorded in `VALIDATION.yaml`.
- Full acceptance: **BLOCKED** until source integrity and missing Protocol-v4-v7 prerequisites are resolved outside this synthesis.
