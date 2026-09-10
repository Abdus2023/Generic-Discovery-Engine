# Canonical Claim Records

Every important architectural claim about this repository, with its **three
independent status dimensions**. Status is never collapsed into a single word.

| Dimension | Question | Canonical values |
| --- | --- | --- |
| **Evidence state** | What kind of evidence do we possess? | `DIRECT` · `CORROBORATED` · `INDIRECT` · `ABSENT` · `INACCESSIBLE` |
| **Claim state** | What kind of statement is this? | `CURRENT` · `SPECIFIED` · `PLANNED` · `HISTORICAL` · `HYPOTHESIS` · `NON-GOAL` |
| **Verification state** | What did the analysis establish? | `VERIFIED` · `PARTIALLY_VERIFIED` · `UNVERIFIED` · `CONTRADICTED` · `NOT_APPLICABLE` |

Readings that this vocabulary is specifically designed to prevent:

* `claim state PLANNED` + `verification VERIFIED` means *the fact that it is
  planned is verified* — never that it exists.
* `evidence DIRECT` + `verification CONTRADICTED` means *the code says something
  different from the claim*, not that the evidence is weak.
* `evidence ABSENT` is a positive result of a bounded inspection; it is not
  `INACCESSIBLE` (which this analysis never needed, having full access).

Evidence IDs resolve in the [evidence register](evidence-register.md).

## Current-system claims

| Claim ID | Statement | Evidence | Evidence state | Claim state | Verification state | Scope | Interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `CAND-CLAIM-001` | Candidate identity is `type:target`, and inserting a duplicate merges into the existing candidate | CODE-003, CODE-007, TEST-004, TEST-005 | CORROBORATED | CURRENT | VERIFIED | candidate model | identity is type-scoped; the same URL with a different type is deliberately two candidates |
| `CAND-CLAIM-002` | A candidate is a hypothesis, not an assertion of existence | CODE-003, DOC-003 | INDIRECT | CURRENT | PARTIALLY_VERIFIED | candidate model | the code stores no existence assertion, but the "hypothesis" framing is design prose, not something the implementation can demonstrate |
| `CAND-CLAIM-003` | Candidate growth is bounded (candidate cap, depth limit, request budget) | CODE-002, CODE-007, CFG-001 | DIRECT | CURRENT | VERIFIED | search space | dropping is silent except for a diagnostic on the candidate cap |
| `SCHED-CLAIM-001` | Ownership is established synchronously, before the worker's first `await` | CODE-009, CODE-018, TEST-001 | CORROBORATED | CURRENT | VERIFIED | scheduler | the transition happens inside a synchronous method; the first suspension point follows it |
| `SCHED-CLAIM-002` | A candidate has at most one active owner | CODE-008, CODE-021, TEST-009, TEST-011 | CORROBORATED | CURRENT | **CONTRADICTED** | scheduler + expansion | the claim site is safe; re-discovery re-queues in-flight candidates, so the end-to-end invariant fails (D1) |
| `SCHED-CLAIM-003` | Retry is bounded by exponential backoff | CODE-010, CODE-011 | DIRECT | CURRENT | PARTIALLY_VERIFIED | scheduler | backoff applies to `queued` retries; `failed` bypasses it and stays claimable (D3) |
| `SCHED-CLAIM-004` | A permanently failing target eventually stops consuming the budget | CODE-009, CODE-010 | DIRECT | CURRENT | **CONTRADICTED** | scheduler | `failed` is in the claim eligibility set with no backoff (D3) |
| `SCHED-CLAIM-005` | The configured worker pool provides the configured concurrency | CODE-018, TEST-010 | CORROBORATED | CURRENT | **CONTRADICTED** | scheduler | a worker exits permanently on an empty frontier; effective concurrency collapses toward 1 (D2) |
| `SCHED-CLAIM-006` | Adaptive concurrency changes the number of live workers | CODE-018, CODE-029 | DIRECT | CURRENT | **CONTRADICTED** | scheduler | the counter changes and is displayed, but the pool is created once (D5) |
| `ACQ-CLAIM-001` | Acquisition is HTTP-GET-specific and browser/userscript-specific | CODE-013, SCOPE-003 | CORROBORATED | CURRENT | VERIFIED | acquisition | `GM_xmlhttpRequest` with a `fetch` fallback; no transport interface exists |
| `ACQ-CLAIM-002` | Failed acquisition still produces an observation | CODE-004, CODE-013, CODE-019 | CORROBORATED | CURRENT | VERIFIED | acquisition → observation | timeout, transport error and HTTP error all yield observation records |
| `ACQ-CLAIM-003` | Cancelling a scan aborts in-flight requests | CODE-018, CODE-010, DOC-004 | INDIRECT | CURRENT | **CONTRADICTED** | acquisition runtime | `stop()` sets a flag; the in-flight request is not aborted, and cancellation is runtime-owned only in the DESIGNED v0.10 |
| `PROV-CLAIM-001` | A discovery records both its candidate and its observation | CODE-005, CODE-021 | DIRECT | CURRENT | VERIFIED | provenance | the link is stored at creation time |
| `PROV-CLAIM-002` | The derivation chain seed → candidate → observation → discovery → child candidate is reconstructible | CODE-005, TEST-007 | CORROBORATED | CURRENT | VERIFIED | provenance | reconstructed end-to-end in a fresh execution context |
| `PROV-CLAIM-003` | Content fingerprints are used to relate identical content behind different URLs | CODE-022, CODE-023 | DIRECT | **SPECIFIED** | **CONTRADICTED** | provenance / identity | the index is written and probed but never read; identity resolution is DESIGNED (v0.17), not current (D8) |
| `PROV-CLAIM-004` | Observation and discovery are distinct objects | CODE-004, CODE-005 | DIRECT | CURRENT | VERIFIED | provenance | separate records with separate identifiers and lifetimes |
| `PROV-CLAIM-005` | Evidence, competing interpretations and conflict resolution exist | — | ABSENT | SPECIFIED | UNVERIFIED | provenance | no such objects exist; designed in v0.16/v0.34 (see `PLAN-CLAIM-001`) |
| `PROV-CLAIM-006` | Observations are immutable evidence | CODE-006, CODE-025 | INDIRECT | CURRENT | UNVERIFIED | provenance | observations live in a mutable map and are re-serialized on persistence; nothing enforces immutability |

## Architecture-boundary claims

| Claim ID | Statement | Evidence | Evidence state | Claim state | Verification state | Scope | Interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ARCH-CLAIM-001` | Providers perform no I/O, do not enqueue candidates and own no policy | CODE-014, CODE-015, TEST-002 | CORROBORATED | CURRENT | VERIFIED | provider model | the strongest boundary in the prototype; contract is `matches()` + `recognize()` |
| `ARCH-CLAIM-002` | Providers are protocol-independent | CODE-013, CODE-015, SCOPE-003 | DIRECT | CURRENT | **CONTRADICTED** | provider model | only recognition is an interface; acquisition is one hard-wired HTTP path |
| `ARCH-CLAIM-003` | Candidate expansion is owned by the engine, not by providers | CODE-015, CODE-021 | CORROBORATED | CURRENT | VERIFIED | expansion | providers return `Discovery[]`; `emitDiscovery()` performs expansion |
| `ARCH-CLAIM-004` | Discovery records are deduplicated like candidates | CODE-021, TEST-012 | CORROBORATED | CURRENT | **CONTRADICTED** | expansion | a `Discovery` is stored before the derived candidate is deduplicated; `text/html` is also interpreted twice (D9) |
| `ARCH-CLAIM-005` | Persisted state survives a reload | CODE-025, TEST-008 | CORROBORATED | CURRENT | VERIFIED | persistence | candidates, observations, discoveries, resources, edges and the ledger round-trip |
| `ARCH-CLAIM-006` | Persistence is transactional and crash-safe | CODE-025 | ABSENT | SPECIFIED | UNVERIFIED | persistence | one serialized snapshot; no transaction, validation or recovery (DESIGNED v0.32) |
| `ARCH-CLAIM-007` | The request budget is a per-run allowance | CODE-025, TEST-008 | CORROBORATED | CURRENT | VERIFIED | acquisition runtime | deliberately reset on restore; slots are never released |
| `ARCH-CLAIM-008` | Two tabs scanning the same origin coordinate with each other | CODE-009, SCOPE-004, DOC-005 | DIRECT | CURRENT | **CONTRADICTED** | concurrency | ownership state is per engine instance; profile coordination is DESIGNED (v0.33) |
| `ARCH-CLAIM-009` | Recognition confidence is comparable across providers | CODE-005, CODE-016 | INDIRECT | CURRENT | UNVERIFIED | recognition | confidences are provider-local constants; no calibration or aggregation rule |
| `ARCH-CLAIM-010` | Providers may all match one observation, and do so by design | CODE-016, TEST-006 | CORROBORATED | CURRENT | VERIFIED | provider model | `text/html` matches HTML and text; no router or priority exists (DESIGNED v0.11) |

## Scope and absence claims

| Claim ID | Statement | Evidence | Evidence state | Claim state | Verification state | Scope | Interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SCOPE-CLAIM-001` | No DVB/RF implementation exists (spectrum, tuner, demodulator, FEC, transport stream, PSI/SI) | SCOPE-001, TEST-003 | ABSENT | NON-GOAL | VERIFIED | whole implementation | absence is asserted over one file read in full and scanned mechanically |
| `SCOPE-CLAIM-002` | No v0.8+ design layer is implemented | SCOPE-002, TEST-003, DOC-006 | ABSENT | PLANNED | VERIFIED | whole implementation | the design series exists as prose only |
| `SCOPE-CLAIM-003` | Coverage, absence and completeness are not represented | SCOPE-006, CODE-009 | ABSENT | SPECIFIED | VERIFIED | search space | "exhausted" in logs means "no eligible candidate at this instant" |
| `SCOPE-CLAIM-004` | Non-URL candidate targets are not implemented | SCOPE-007, CODE-003 | ABSENT | SPECIFIED | VERIFIED | candidate model | every `discover()` call passes a URL |
| `SCOPE-CLAIM-005` | The repository contains no tests, CI configuration or build tooling | SCOPE-005 | ABSENT | HISTORICAL | VERIFIED | repository | true at the analysis revision; verification tooling was added afterwards by R-010 |

## Plan, history and hypothesis claims

| Claim ID | Statement | Evidence | Evidence state | Claim state | Verification state | Scope | Interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `PLAN-CLAIM-001` | Acquisition runtime, recognition runtime, candidate sources, domain/sessions, work items, evidence graph, identity, classification, coverage, absence, query planning, reconciliation, arbitration, cost ledger, transactional persistence and multi-context coordination are designed | DOC-006 | INDIRECT | PLANNED | VERIFIED | design series v0.8–v0.34 | *the fact that they are planned is verified; their implementation is not implied* |
| `PLAN-CLAIM-002` | Browser-profile coordination is not distributed consensus | DOC-005 | INDIRECT | SPECIFIED | VERIFIED | coordination | stated by the design series itself as a boundary |
| `PLAN-CLAIM-003` | Decision replay must be separable from acquisition against a changing world | DOC-004 | INDIRECT | SPECIFIED | VERIFIED | replay | an acquisition log is not a deterministic execution trace |
| `HIST-CLAIM-001` | Versions v0.3.0–v0.6.0 existed as code and are superseded by v0.7.1 | DOC-002, DOC-006 | DIRECT | HISTORICAL | VERIFIED | archive | all parse except the v0.5.0 paste at transcript L18378–L23093 |
| `HIST-CLAIM-002` | The v0.5.0 paste in the archive is not valid JavaScript | DOC-006 | DIRECT | HISTORICAL | VERIFIED | archive | `await` appears outside an async function |
| `HIST-CLAIM-003` | The pre-cleanup README described the system accurately | DOC-001 vs CODE-008, CODE-009, TEST-009 | CORROBORATED | CURRENT (at the time) | **CONTRADICTED** | README at `cc8df73` | it claimed atomic claiming and guaranteed concurrency; direct implementation evidence and executed behaviour override documentation evidence, and the contradiction is recorded rather than resolved silently |
| `HYP-CLAIM-001` | A value × probability ÷ cost scheduling model would outperform the static priority heuristic | DOC-006 | INDIRECT | HYPOTHESIS | UNVERIFIED | scheduling | no measurement exists; the cost and probability inputs are not modelled |

## Contradicted claims

A contradiction is a relationship between claims, never an evidence state. Each
row below names the two claims and which one the stronger evidence supports.

| Claims in conflict | Supporting evidence | What evidence supports | Resolution recorded |
| --- | --- | --- | --- |
| `SCHED-CLAIM-002` vs README "at most one active owner" | CODE-008, CODE-021, TEST-009, TEST-011 | the implementation (re-queue path) — direct + executed | invariant violated end to end; claim reclassified as CONTRADICTED; defect D1 |
| `SCHED-CLAIM-005` vs README "concurrently acquire candidates" | CODE-018, TEST-010 | the implementation (permanent worker exit) | configured ≠ provided; defect D2 |
| `SCHED-CLAIM-004` vs README "retry policy" | CODE-009, CODE-010 | the implementation (`failed` claimable, no backoff) | defect D3 |
| `ARCH-CLAIM-002` vs README "protocol-independent" | CODE-013, CODE-015, SCOPE-003 | the implementation (single HTTP path) | scope narrowed to recognition providers |
| `ARCH-CLAIM-004` vs README "deduplicate candidates" | CODE-021, TEST-012 | the implementation (discovery stored before dedup) | defect D9 |
| `PROV-CLAIM-003` vs the presence of a fingerprint index | CODE-022, CODE-023 | the implementation (index never read) | dead evidence; defect D8 |
| `ARCH-CLAIM-008` vs any expectation of shared work between tabs | CODE-009, SCOPE-004 | the implementation (per-instance ownership) | cross-context coordination is DESIGNED only |
| `HIST-CLAIM-003` | DOC-001 vs CODE-008, TEST-009 | the implementation | retrospective documentation was wrong; superseded by R-002 |

## Claims deliberately not made

| Not claimed | Reason |
| --- | --- |
| "The engine produces evidence" | observations and discoveries exist; the evidence layer is DESIGNED (`PROV-CLAIM-005`) |
| "The engine measures coverage" | no coverage object exists (`SCOPE-CLAIM-003`) |
| "The search is exhaustive / complete" | no termination or coverage criterion exists |
| "The architecture is protocol-agnostic" | acquisition is HTTP-only (`ARCH-CLAIM-002`) |
| "Claiming can never occur twice" | true at the claim site, false end to end (`SCHED-CLAIM-002`) |
| "DVB compatibility" | non-goal, absence verified (`SCOPE-CLAIM-001`) |
| "The prototype is production-ready" | nine documented defects, four of them P0 |

## Change-control note

These claim records describe the repository at the analysis revision
`cc8df73` plus the executed documentation changes `R-001 … R-013`. No code change
was made: the artifact digest is unchanged and enforced by `tools/verify.mjs`.
Proposed code changes are listed as `PLAN ONLY` in the
[change register](change-register-2026-09-10.md) and are not reflected in any
claim above.
