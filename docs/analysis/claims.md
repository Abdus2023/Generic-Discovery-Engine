# Canonical Claim Records

Normative source: **[analysis.json](analysis.json)**, governed by
**[analysis.schema.json](analysis.schema.json)** (JSON Schema draft 2020-12, sections
185–197). The tables in this document are rendered from it by
`tools/render-claims.mjs` — do not edit them by hand; edit the JSON and re-render.
`tools/validate-analysis.mjs` runs the validation pipeline, and each stage is
validated independently:

```
STRUCTURAL SCHEMA          sections 185-197 (draft 2020-12)
      ↓
CLAIM VALIDATION           C-001…C-043, CV-001…CV-020
      ↓
EVIDENCE ANALYSIS          register resolution, CV-008, CV-010, C-031
      ↓
AUTHORIZATION              AC-001…AC-016 (+ AUTH-017…AUTH-020)
      ↓
EXECUTION                  EV-001…EV-012, section 200 transitions
      ↓
EXECUTION VERIFICATION     EVV-001…EVV-009
      ↓
SERIALIZATION              SER-001…SER-012
```

## Two verification domains (section 168)

"Verification" on its own is ambiguous, and the schema does not allow it. There
are two different objects to verify, and they have different fields, different
lifecycles and different vocabularies:

| Object verified | Field | Vocabulary |
| --- | --- | --- |
| A claim — *is the proposition supported by the available evidence?* | `claim_verification.result` | `VERIFIED` · `PARTIALLY_VERIFIED` · `UNVERIFIED` · `CONTRADICTED` · `NOT_APPLICABLE` |
| The repository *after* execution — *does the resulting state satisfy the required invariants?* | `execution_verification.state` + `execution_verification.result` | state: `PASSED`, `FAILED`, … · result: `CONFORMING`, `NON_CONFORMING`, … |

```
VERIFIED      belongs to claims.
CONFORMING    belongs to execution verification.
```

They are not interchangeable, and neither is a substitute for `execution.state`
(what actually happened) or for `check.result` (one invariant's outcome).

## Typed state model (canonical)

Status is never a single word. Six independent fields describe every claim, each
answering a different question:

| Field | Question it answers | Canonical values |
| --- | --- | --- |
| `claim_kind` | What kind of repository statement is this? | `CURRENT` · `SPECIFIED` · `PLANNED` · `HISTORICAL` · `HYPOTHESIS` · `NON_GOAL` |
| `implementation_state` | Is the behaviour named in the claim implemented? | `IMPLEMENTED` · `PARTIAL` · `NOT_IMPLEMENTED` · `NOT_APPLICABLE` · `UNKNOWN` |
| `test_state` | Is that behaviour exercised? | `TESTED` · `PARTIALLY_TESTED` · `UNTESTED` · `NOT_APPLICABLE` · `UNKNOWN` |
| `evidence_level` | How strong is the repository evidence? | `DIRECT` · `CORROBORATED` · `INDIRECT` · `ABSENT` · `INACCESSIBLE` |
| `claim_verification.result` | What did verification of *this claim* conclude? | `VERIFIED` · `PARTIALLY_VERIFIED` · `UNVERIFIED` · `CONTRADICTED` · `NOT_APPLICABLE` |
| `confidence` | How strong is the evidential basis, graded? | `VERY_LOW` · `LOW` · `MEDIUM` · `HIGH` · `VERY_HIGH` |

`confidence` is advisory: it grades evidential strength and never overrides
`claim_verification.result`. This repository assigns it by rule — `HIGH` only when
direct or corroborated evidence is joined by an executed test and verification did
not return `UNVERIFIED`; `MEDIUM` for direct evidence without execution, an
inspected absence, or any unverified claim; `LOW` for indirect evidence;
`VERY_LOW` for inaccessible scope. The confusing combination `HIGH` with
`UNVERIFIED` is rejected by the validator.

Deprecated field names — do not use them: `verification_result` (superseded by
`claim_verification.result`), `post_verification` (superseded by
`execution_verification`), `status`, and an unqualified `verification` object.
`tools/verify.mjs` fails the build if any of them reappears, and the validator
rejects `status` and `verification` as field names anywhere in the record.

```
CLAIM
  │
  ├── claim_kind                 what kind of statement this is
  ├── implementation_state       whether the named behaviour is implemented
  ├── test_state                 whether it is exercised
  ├── evidence_level             how strong / available the evidence is
  ├── claim_verification.result  what verification of the claim concluded
  └── confidence                 how strong the evidential basis is, graded
```

Combinations that are valid and must not be collapsed:

| Combination | Reading |
| --- | --- |
| `PLANNED` + `NOT_IMPLEMENTED` + `VERIFIED` | the fact that it is planned is verified; implementation is not implied |
| `CURRENT` + `IMPLEMENTED` + `UNTESTED` | implemented, but nothing exercises it |
| `CURRENT` + `NOT_IMPLEMENTED` + `CONTRADICTED` | the code contradicts the documented guarantee; the contradiction is recorded, not normalised |
| `SPECIFIED` + `NOT_IMPLEMENTED` + `UNVERIFIED` | designed in prose; nothing establishes it |
| `ACCESS_LEVEL: FULL` + `evidence_level: ABSENT` | the scope was inspected and the evidence was not found — **not** the same as `INACCESSIBLE` |

Convention used throughout: `implementation_state` describes **the behaviour
named in the claim**, not the truth of the claim. A guarantee that the evidence
shows to fail is therefore `PARTIAL` or `NOT_IMPLEMENTED` with
`claim_verification.result: CONTRADICTED`.

## What the rules forbid

| Situation | Rule | Why it matters here |
| --- | --- | --- |
| A dimension outside its canonical enum | `CV-001`…`CV-005` | no invented values, no substituted vocabulary |
| `VERIFIED` with `INDIRECT`, `ABSENT` or `INACCESSIBLE` evidence | `CV-006` | a verified conclusion needs a directly relevant artifact (an inspected absence needs its recorded procedure) |
| `INACCESSIBLE` evidence with any verdict other than `UNVERIFIED` | `CV-007` | "could not inspect" must never be reported as a finding |
| `CONTRADICTED` without conflicting evidence | `CV-008` | a contradiction is a relationship between evidence, not an adjective |
| `IMPLEMENTED` without an implementation artifact | `CV-009` | a feature is not implemented because a document says so |
| `NOT_IMPLEMENTED` resting on unreachable scope | `CV-010` | use `UNKNOWN` + `INACCESSIBLE` + `UNVERIFIED` instead |
| `HYPOTHESIS` or `NON_GOAL` with an implementation state | `CV-011`, `CV-012` | a hypothesis and an excluded capability are not implementation claims |
| `PLANNED` read as `IMPLEMENTED` | `CV-013` | the design series must never be read as shipped behaviour |
| `TESTED` without execution evidence | `CV-014` | a test file alone proves availability, not testing |
| `UNTESTED` read as `NOT_IMPLEMENTED` | `CV-015` | untested is not missing |
| `IMPLEMENTED` ⇏ `TESTED`, `TESTED` ⇏ `VERIFIED`, `VERIFIED` ⇏ `IMPLEMENTED` | `CV-016`…`CV-018` | each transition needs its own evidence |
| `PARTIAL` read as `PARTIALLY_VERIFIED` | `CV-019` | partial implementation and partial verification are different dimensions |
| `INACCESSIBLE` relabelled as `ABSENT` | `CV-020` | converting "could not inspect" into "not found" would fabricate a finding |
| `NOT_IMPLEMENTED` + `TESTED` without an absence test | `C-093` | testing absence is recorded explicitly (`absence_test`) |
| `CORROBORATED` from one source repeated | `C-031` | corroboration needs materially independent sources |

`CV-015`…`CV-019` are checked as independence properties rather than as
prohibitions: the validator verifies that the observed combinations do not
collapse into a single mapping. A rule that one dimension *does not imply*
another cannot be checked by inspecting one record; what can be checked is that
the record does not encode the implication.

The authority and lifecycle sides have their own rule sets: `AC-001`…`AC-016`
(authorization state, profile resolution, capability states, scope, change
authorization), `EV-001`…`EV-012` (the execution lifecycle) and `EVV-001`…`EVV-009`
(execution verification). Section 200 additionally constrains which lifecycle
transitions are legal, and the validator checks that every recorded state is
reachable in that graph. The full model is in
[scope-and-authorization.md](scope-and-authorization.md) §5.

## Valid patterns actually used here

| claim_kind | implementation_state | test_state | evidence_level | claim_verification.result | Example |
| --- | --- | --- | --- | --- | --- |
| `CURRENT` | `IMPLEMENTED` | `TESTED` | `CORROBORATED` | `VERIFIED` | `CAND-CLAIM-001` |
| `CURRENT` | `NOT_IMPLEMENTED` | `TESTED` | `DIRECT` | `CONTRADICTED` | `SCHED-CLAIM-004` (documentation/implementation contradiction — **not** normalised to `PLANNED`) |
| `SPECIFIED` | `NOT_IMPLEMENTED` | `NOT_APPLICABLE` | `DIRECT` | `VERIFIED` | `PLAN-CLAIM-003` |
| `PLANNED` | `NOT_IMPLEMENTED` | `NOT_APPLICABLE` | `DIRECT` | `VERIFIED` | `PLAN-CLAIM-001` — the *planned status* is verified, nothing more |
| `HISTORICAL` | `IMPLEMENTED` | `UNTESTED` | `DIRECT` | `VERIFIED` | `HIST-CLAIM-001` |
| `HYPOTHESIS` | `NOT_APPLICABLE` | `NOT_APPLICABLE` | `INDIRECT` | `UNVERIFIED` | `HYP-CLAIM-001` |
| `NON_GOAL` | `NOT_APPLICABLE` | `NOT_APPLICABLE` | `DIRECT` | `VERIFIED` | `SCOPE-CLAIM-006` |

## Lifecycle: what was authorized, executed and verified

Claims describe the repository. The work done to this repository has its own
lifecycles, and they are **not** claim fields (sections 180–184):

| Stage | Field | Values |
| --- | --- | --- |
| Authorization | `authorization.state` | `NOT_REQUESTED` · `REQUESTED` · `GRANTED` · `DENIED` · `REVOKED` · `EXPIRED` |
| Capability | `capabilities.grants[].state` | `DECLARED` · `ENABLED` · `RESTRICTED` · `DENIED` · `REVOKED` · `EXPIRED` |
| Execution lifecycle | `execution.state` | `NOT_STARTED` · `AUTHORIZATION_BLOCKED` · `READY` · `RUNNING` · `SUCCEEDED` · `PARTIALLY_SUCCEEDED` · `FAILED` · `CANCELLED` · `STOPPED` |
| Per-operation | `execution.operations[]` | `authorization_decision` `ALLOWED`/`DENIED` + `result` `SUCCEEDED` · `FAILED` · `AUTHORIZATION_DENIED` · … |
| Execution verification lifecycle | `execution_verification.state` | `NOT_REQUIRED` · `NOT_STARTED` · `READY` · `RUNNING` · `PASSED` · `PARTIALLY_PASSED` · `FAILED` · `BLOCKED` · `INCONCLUSIVE` |
| Execution verification outcome | `execution_verification.result` | `CONFORMING` · `PARTIALLY_CONFORMING` · `NON_CONFORMING` · `INCONCLUSIVE` · `NOT_APPLICABLE` |
| Individual check | `execution_verification.checks[].result` | `NOT_RUN` · `PASSED` · `FAILED` · `BLOCKED` · `INCONCLUSIVE` |

`SUCCEEDED ≠ PASSED` and `FAILED ≠ UNVERIFIED`: execution and execution
verification may disagree, and in this record they are different facts — 21
operations succeeded, all with an `ALLOWED` decision, and eight independent checks
conformed, which is why `execution.state: SUCCEEDED` and
`execution_verification.state: PASSED` are recorded separately rather than as one
verdict (EVV-001).

<!-- CLAIMS:BEGIN (generated from analysis.json — do not edit by hand) -->

### Current-system claims

| Claim ID | Statement | claim_kind | implementation_state | test_state | evidence_level | claim_verification.result | confidence | Evidence | Interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `CAND-CLAIM-001` | Candidate identity is type:target, and inserting a duplicate merges into the existing candidate. | `CURRENT` | `IMPLEMENTED` | `TESTED` | `CORROBORATED` | `VERIFIED` | `HIGH` | [EVID:CODE-003] [EVID:CODE-007] [EVID:TEST-004] [EVID:TEST-005] | Identity is type-scoped: the same URL discovered as a different type is deliberately a second candidate. Limitation: Observed in the bundled harness: one browser profile and one simulated request log, not a production measurement. |
| `CAND-CLAIM-002` | A candidate is a hypothesis, not an assertion that the target exists. | `CURRENT` | `IMPLEMENTED` | `UNTESTED` | `INDIRECT` | `PARTIALLY_VERIFIED` | `LOW` | [EVID:CODE-003] [EVID:DOC-003] | The implementation stores no existence assertion, but the hypothesis framing is design prose; the code cannot demonstrate a framing. test_state UNTESTED: no executed check asserts the hypothesis framing; the implementation shows the absence of an existence assertion, which is a code reading, not a test. Limitation: Indirect evidence supports the interpretation without establishing the claim directly. |
| `CAND-CLAIM-003` | Candidate growth is bounded by a candidate cap, a depth limit and a request budget. | `CURRENT` | `IMPLEMENTED` | `UNTESTED` | `DIRECT` | `VERIFIED` | `MEDIUM` | [EVID:CODE-002] [EVID:CODE-007] [EVID:CFG-001] | Dropping is silent; only the candidate cap records a diagnostic. test_state UNTESTED: the caps, depth limit and budget are enforced in code and inspected statically, but no executed check asserts them; the simulate run stays far below the caps. |
| `SCHED-CLAIM-001` | Candidate ownership is established synchronously, before the worker's first await. | `CURRENT` | `IMPLEMENTED` | `TESTED` | `CORROBORATED` | `VERIFIED` | `HIGH` | [EVID:CODE-009] [EVID:CODE-018] [EVID:TEST-001] | The transition happens inside a synchronous method and the first suspension point follows it; this is valid only within one execution context. |
| `SCHED-CLAIM-002` | A candidate has at most one active owner. | `CURRENT` | `PARTIAL` | `TESTED` | `CORROBORATED` | `**CONTRADICTED**` | `HIGH` | [EVID:CODE-008] [EVID:CODE-021] [EVID:TEST-009] [EVID:TEST-011] | The claim site is safe; re-discovery re-queues in-flight candidates, so the end-to-end invariant fails (defect D1). Limitation: The design intent and the implementation conflict; this record states the conflict and does not resolve it. Limitation: Observed in the bundled harness: one browser profile and one simulated request log, not a production measurement. |
| `SCHED-CLAIM-003` | Retry is bounded by exponential backoff. | `CURRENT` | `PARTIAL` | `TESTED` | `DIRECT` | `PARTIALLY_VERIFIED` | `HIGH` | [EVID:CODE-010] [EVID:CODE-011] [EVID:TEST-010] | Backoff applies to queued retries; the failed state bypasses it and remains claimable (defect D3). Limitation: Observed in the bundled harness: one browser profile and one simulated request log, not a production measurement. |
| `SCHED-CLAIM-004` | A permanently failing target eventually stops consuming the request budget. | `CURRENT` | `NOT_IMPLEMENTED` | `TESTED` | `DIRECT` | `**CONTRADICTED**` | `HIGH` | [EVID:CODE-009] [EVID:CODE-010] [EVID:TEST-010] | failed is part of the claim eligibility set with no backoff, so the target is retried indefinitely (defect D3). The absence of a terminal failure state is tested, not inferred: the harness reports failed candidates still in the pool at quiescence with their attempt counts. Limitation: The design intent and the implementation conflict; this record states the conflict and does not resolve it. Limitation: Observed in the bundled harness: one browser profile and one simulated request log, not a production measurement. |
| `SCHED-CLAIM-005` | The configured worker pool provides the configured concurrency. | `CURRENT` | `PARTIAL` | `TESTED` | `CORROBORATED` | `**CONTRADICTED**` | `HIGH` | [EVID:CODE-018] [EVID:TEST-010] | A worker exits permanently on an empty frontier and the pool is never refilled, so effective concurrency collapses toward one (defect D2). Limitation: The design intent and the implementation conflict; this record states the conflict and does not resolve it. Limitation: Observed in the bundled harness: one browser profile and one simulated request log, not a production measurement. |
| `SCHED-CLAIM-006` | Adaptive concurrency changes the number of live workers. | `CURRENT` | `NOT_IMPLEMENTED` | `UNTESTED` | `DIRECT` | `**CONTRADICTED**` | `MEDIUM` | [EVID:CODE-018] [EVID:CODE-029] | The counter and its diagnostics change, but the pool is created once before it is read (defect D5). Conflicting evidence: the pool is created once (CODE-018) and the adaptive counter only changes diagnostics (CODE-029). Limitation: The design intent and the implementation conflict; this record states the conflict and does not resolve it. |
| `ACQ-CLAIM-001` | Acquisition is HTTP-GET-specific and browser/userscript-specific. | `CURRENT` | `IMPLEMENTED` | `TESTED` | `CORROBORATED` | `VERIFIED` | `HIGH` | [EVID:CODE-013] [EVID:SCOPE-003] [EVID:TEST-002] | GM_xmlhttpRequest with a fetch fallback; no transport interface exists in the inspected scope. |
| `ACQ-CLAIM-002` | A failed acquisition still produces an observation. | `CURRENT` | `IMPLEMENTED` | `UNTESTED` | `CORROBORATED` | `VERIFIED` | `MEDIUM` | [EVID:CODE-004] [EVID:CODE-013] [EVID:CODE-019] | Timeout, transport error and HTTP error all yield observation records with distinct statuses. test_state UNTESTED: the failure paths create observations in code (CODE-004, CODE-013, CODE-019), but no executed check asserts the resulting observation. |
| `ACQ-CLAIM-003` | Cancelling a scan aborts in-flight requests. | `CURRENT` | `NOT_IMPLEMENTED` | `UNTESTED` | `DIRECT` | `**CONTRADICTED**` | `MEDIUM` | [EVID:CODE-018] [EVID:CODE-010] [EVID:DOC-004] | stop() sets a flag; in-flight requests continue, and runtime-owned cancellation exists only in the DESIGNED v0.10. Conflicting evidence: stop() only sets a flag (CODE-018) and no request is aborted (CODE-010). DIRECT evidence: the code itself shows that only a flag is set (CODE-018) and no in-flight request is aborted (CODE-010); the design prose is context, not the ground of the finding. Limitation: The design intent and the implementation conflict; this record states the conflict and does not resolve it. |
| `PROV-CLAIM-001` | A discovery records both its candidate and its observation. | `CURRENT` | `IMPLEMENTED` | `TESTED` | `DIRECT` | `VERIFIED` | `HIGH` | [EVID:CODE-005] [EVID:CODE-021] [EVID:TEST-007] | The linkage is stored at creation time. Tested: the harness reconstructs the chain and reads both records. |
| `PROV-CLAIM-002` | The derivation chain seed to candidate to observation to discovery to child candidate is reconstructible. | `CURRENT` | `IMPLEMENTED` | `TESTED` | `CORROBORATED` | `VERIFIED` | `HIGH` | [EVID:CODE-005] [EVID:CODE-007] [EVID:TEST-007] | Reconstructed end to end in a fresh execution context, including the observations for each link. |
| `PROV-CLAIM-003` | Content fingerprints are used to relate identical content behind different URLs. | `SPECIFIED` | `NOT_IMPLEMENTED` | `UNTESTED` | `DIRECT` | `**CONTRADICTED**` | `MEDIUM` | [EVID:CODE-022] [EVID:CODE-023] | The fingerprint index is written and probed but never read; identity resolution is DESIGNED (v0.17), not current (defect D8). Limitation: The design intent and the implementation conflict; this record states the conflict and does not resolve it. |
| `PROV-CLAIM-004` | Observation and discovery are distinct objects. | `CURRENT` | `IMPLEMENTED` | `TESTED` | `DIRECT` | `VERIFIED` | `HIGH` | [EVID:CODE-004] [EVID:CODE-005] [EVID:TEST-007] | Separate records, separate identifiers, separate lifetimes. Tested: the harness reads observations and discoveries as separate maps. |
| `PROV-CLAIM-005` | An evidence layer with competing interpretations and conflict resolution exists. | `SPECIFIED` | `NOT_IMPLEMENTED` | `NOT_APPLICABLE` | `ABSENT` | `UNVERIFIED` | `MEDIUM` | [EVID:SCOPE-002] [EVID:DOC-006] | No such objects exist; designed in v0.16 and v0.34. Evidence is ABSENT (inspected scope covered), not INACCESSIBLE. Limitation: Absence holds only for the inspected scope and revision recorded in AV-006. |
| `PROV-CLAIM-006` | Observations are immutable evidence. | `CURRENT` | `NOT_IMPLEMENTED` | `UNTESTED` | `DIRECT` | `UNVERIFIED` | `MEDIUM` | [EVID:CODE-006] [EVID:CODE-025] | Observations live in a mutable map and are re-serialized on persistence; nothing enforces immutability. DIRECT evidence: observation records are plain objects with no freeze, copy-on-write or integrity check, so immutability is not enforced (CODE-004, CODE-005). |

### Architecture-boundary claims

| Claim ID | Statement | claim_kind | implementation_state | test_state | evidence_level | claim_verification.result | confidence | Evidence | Interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `ARCH-CLAIM-001` | Providers perform no I/O, do not enqueue candidates and own no policy. | `CURRENT` | `IMPLEMENTED` | `TESTED` | `CORROBORATED` | `VERIFIED` | `HIGH` | [EVID:CODE-014] [EVID:CODE-015] [EVID:TEST-002] | The strongest boundary in the prototype: the contract is matches() plus recognize(), with expansion owned by the engine. |
| `ARCH-CLAIM-002` | Providers are protocol-independent. | `CURRENT` | `NOT_IMPLEMENTED` | `PARTIALLY_TESTED` | `DIRECT` | `**CONTRADICTED**` | `HIGH` | [EVID:CODE-013] [EVID:CODE-015] [EVID:SCOPE-003] [EVID:TEST-006] | Only recognition is an interface; acquisition is one hard-wired HTTP path. PARTIALLY_TESTED: provider matching is executed (TEST-006); the transport half of the claim is not tested. Limitation: The design intent and the implementation conflict; this record states the conflict and does not resolve it. |
| `ARCH-CLAIM-003` | Candidate expansion is owned by the engine, not by providers. | `CURRENT` | `IMPLEMENTED` | `TESTED` | `CORROBORATED` | `VERIFIED` | `HIGH` | [EVID:CODE-015] [EVID:CODE-021] [EVID:TEST-002] | Providers return Discovery objects; emitDiscovery performs expansion under engine policy. |
| `ARCH-CLAIM-004` | Discovery records are deduplicated like candidates. | `CURRENT` | `NOT_IMPLEMENTED` | `TESTED` | `CORROBORATED` | `**CONTRADICTED**` | `HIGH` | [EVID:CODE-016] [EVID:CODE-021] [EVID:TEST-012] | A discovery is stored before the derived candidate is deduplicated, and text/html is interpreted twice; 74 discoveries for 27 URLs in one run (defect D9). The absence of deduplication is tested, not inferred: the harness counts discoveries against unique URLs in one run. Limitation: The design intent and the implementation conflict; this record states the conflict and does not resolve it. Limitation: Observed in the bundled harness: one browser profile and one simulated request log, not a production measurement. |
| `ARCH-CLAIM-005` | Persisted state survives a reload. | `CURRENT` | `IMPLEMENTED` | `TESTED` | `CORROBORATED` | `VERIFIED` | `HIGH` | [EVID:CODE-025] [EVID:TEST-008] | Candidates, observations, discoveries, resources, graph edges and the decision ledger round-trip; the request budget deliberately resets. Limitation: Observed in the bundled harness: one browser profile and one simulated request log, not a production measurement. |
| `ARCH-CLAIM-006` | Persistence is transactional and crash-safe. | `SPECIFIED` | `NOT_IMPLEMENTED` | `NOT_APPLICABLE` | `ABSENT` | `UNVERIFIED` | `MEDIUM` | [EVID:CODE-025] [EVID:SCOPE-002] [EVID:DOC-006] | One serialized snapshot with caps; no transaction, validation or recovery. Designed in v0.32. Limitation: Absence holds only for the inspected scope and revision recorded in AV-007. |
| `ARCH-CLAIM-007` | The request budget is a per-run allowance. | `CURRENT` | `IMPLEMENTED` | `TESTED` | `CORROBORATED` | `VERIFIED` | `HIGH` | [EVID:CODE-020] [EVID:CODE-025] [EVID:TEST-008] | Restore deliberately resets requestsReserved; reserved slots are never released, so the budget counts attempts. Limitation: Observed in the bundled harness: one browser profile and one simulated request log, not a production measurement. |
| `ARCH-CLAIM-008` | Cross-context coordination is part of the current implementation. | `SPECIFIED` | `NOT_IMPLEMENTED` | `NOT_APPLICABLE` | `DIRECT` | `**CONTRADICTED**` | `MEDIUM` | [EVID:CODE-009] [EVID:SCOPE-004] [EVID:DOC-005] | Ownership state is per engine instance; two tabs duplicate each other's work. Profile coordination is DESIGNED (v0.33) and is explicitly not distributed consensus. Limitation: The design intent and the implementation conflict; this record states the conflict and does not resolve it. |
| `ARCH-CLAIM-009` | Recognition confidence is comparable across providers. | `CURRENT` | `NOT_IMPLEMENTED` | `UNTESTED` | `DIRECT` | `UNVERIFIED` | `MEDIUM` | [EVID:CODE-005] [EVID:CODE-016] | Confidences are provider-local constants with no calibration or aggregation rule. |
| `ARCH-CLAIM-010` | Several providers may match one observation, and do so by design. | `CURRENT` | `IMPLEMENTED` | `TESTED` | `CORROBORATED` | `VERIFIED` | `HIGH` | [EVID:CODE-016] [EVID:TEST-006] | text/html matches HTML and text because TextProvider matches text/*; there is no router or priority (DESIGNED v0.11). |

### Scope and absence claims

| Claim ID | Statement | claim_kind | implementation_state | test_state | evidence_level | claim_verification.result | confidence | Evidence | Interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SCOPE-CLAIM-001` | The repository contains no DVB/RF implementation (spectrum, tuner, demodulator, FEC, transport stream, PSI/SI). | `CURRENT` | `NOT_IMPLEMENTED` | `NOT_APPLICABLE` | `ABSENT` | `VERIFIED` | `MEDIUM` | [EVID:SCOPE-001] [EVID:TEST-003] | Absence is asserted over a single implementation file read in full and scanned mechanically, so it is ABSENT (inspected, not found), not INACCESSIBLE. Limitation: Absence holds only for the inspected scope and revision recorded in AV-001. |
| `SCOPE-CLAIM-002` | No v0.8+ design layer is implemented (capabilities, work items, evidence graph, leases, coverage, fencing). | `CURRENT` | `NOT_IMPLEMENTED` | `NOT_APPLICABLE` | `ABSENT` | `VERIFIED` | `MEDIUM` | [EVID:SCOPE-002] [EVID:TEST-003] [EVID:DOC-006] | The design series exists as prose only. Limitation: Absence holds only for the inspected scope and revision recorded in AV-002. |
| `SCOPE-CLAIM-003` | Coverage, absence and completeness are not represented. | `CURRENT` | `NOT_IMPLEMENTED` | `NOT_APPLICABLE` | `ABSENT` | `VERIFIED` | `MEDIUM` | [EVID:SCOPE-006] [EVID:CODE-009] | "Exhausted" in logs means no eligible candidate at that instant; coverage objects are DESIGNED (v0.22, v0.23). Limitation: Absence holds only for the inspected scope and revision recorded in AV-003. |
| `SCOPE-CLAIM-004` | Non-URL candidate targets are not implemented. | `CURRENT` | `NOT_IMPLEMENTED` | `NOT_APPLICABLE` | `ABSENT` | `VERIFIED` | `MEDIUM` | [EVID:SCOPE-007] [EVID:CODE-003] | Every discover() call passes a URL; the candidate type list is URL-oriented. Limitation: Absence holds only for the inspected scope and revision recorded in AV-004. |
| `SCOPE-CLAIM-005` | The repository contained no tests, CI configuration or build tooling at the analysis revision. | `HISTORICAL` | `NOT_IMPLEMENTED` | `NOT_APPLICABLE` | `ABSENT` | `VERIFIED` | `MEDIUM` | [EVID:SCOPE-005] | True at cc8df73; verification tooling was added afterwards under change R-010, which is recorded as an executed documentation-scope change. Limitation: Absence holds only for the inspected scope and revision recorded in AV-005. |
| `SCOPE-CLAIM-006` | DVB/RF support is an explicit non-goal of the project. | `NON_GOAL` | `NOT_APPLICABLE` | `NOT_APPLICABLE` | `DIRECT` | `VERIFIED` | `MEDIUM` | [EVID:DOC-007] [EVID:SCOPE-001] | Stated in the project scope and enforced mechanically by a symbol scan in tools/verify.mjs. implementation_state is NOT_APPLICABLE because a non-goal is not an implementation claim (§92); the boundary statement itself is DIRECT evidence. |

### Plan, history and hypothesis claims

| Claim ID | Statement | claim_kind | implementation_state | test_state | evidence_level | claim_verification.result | confidence | Evidence | Interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `PLAN-CLAIM-001` | Acquisition runtime, recognition runtime, candidate sources, domain/sessions, work items, evidence graph, identity, classification, coverage, absence, query planning, reconciliation, arbitration, cost ledger, transactional persistence and multi-context coordination are designed. | `PLANNED` | `NOT_IMPLEMENTED` | `NOT_APPLICABLE` | `DIRECT` | `VERIFIED` | `MEDIUM` | [EVID:DOC-006] [EVID:SCOPE-002] | The fact that these layers are planned is verified; their implementation is not implied. DIRECT evidence: the design documents are repository artifacts and are directly relevant to the claim that the layers are designed and unimplemented (§89). |
| `PLAN-CLAIM-002` | Browser-profile coordination is not distributed consensus. | `SPECIFIED` | `NOT_IMPLEMENTED` | `NOT_APPLICABLE` | `DIRECT` | `VERIFIED` | `MEDIUM` | [EVID:DOC-005] | Stated as a boundary by the design series itself. DIRECT evidence: the design documents are repository artifacts and are directly relevant to the claim that the layers are designed and unimplemented (§89). |
| `PLAN-CLAIM-003` | Deterministic decision replay must be separable from acquisition against a changing world. | `SPECIFIED` | `NOT_IMPLEMENTED` | `NOT_APPLICABLE` | `DIRECT` | `VERIFIED` | `MEDIUM` | [EVID:DOC-004] | An acquisition log is not a deterministic execution trace. DIRECT evidence: the design documents are repository artifacts and are directly relevant to the claim that the layers are designed and unimplemented (§89). |
| `HIST-CLAIM-001` | Versions v0.3.0 to v0.6.0 existed as code and are superseded by v0.7.1. | `HISTORICAL` | `IMPLEMENTED` | `UNTESTED` | `DIRECT` | `VERIFIED` | `MEDIUM` | [EVID:CODE-033] [EVID:DOC-006] | All extracted revisions parse except the v0.5.0 paste at transcript L18378-L23093. Supersession is historical: these revisions are not maintained, and the evidence is the historical code blocks themselves, not the prose around them. |
| `HIST-CLAIM-002` | The v0.5.0 paste in the archive is not valid JavaScript. | `HISTORICAL` | `NOT_IMPLEMENTED` | `NOT_APPLICABLE` | `DIRECT` | `VERIFIED` | `MEDIUM` | [EVID:DOC-006] | await appears outside an async function (node --check). |
| `HIST-CLAIM-003` | The pre-cleanup README described the system accurately. | `HISTORICAL` | `NOT_APPLICABLE` | `NOT_APPLICABLE` | `CORROBORATED` | `**CONTRADICTED**` | `HIGH` | [EVID:DOC-001] [EVID:CODE-008] [EVID:CODE-009] [EVID:TEST-009] | It claimed atomic claiming and guaranteed concurrency. Direct implementation evidence and executed behaviour override documentation evidence, and the contradiction is recorded rather than silently resolved. Limitation: The design intent and the implementation conflict; this record states the conflict and does not resolve it. Limitation: Observed in the bundled harness: one browser profile and one simulated request log, not a production measurement. |
| `HYP-CLAIM-001` | A value x probability / cost scheduling model would outperform the static priority heuristic. | `HYPOTHESIS` | `NOT_APPLICABLE` | `NOT_APPLICABLE` | `INDIRECT` | `UNVERIFIED` | `LOW` | [EVID:DOC-006] | No measurement exists; the cost and probability inputs are not modelled. implementation_state is NOT_APPLICABLE because a hypothesis is not an implementation claim (§91). Limitation: Indirect evidence supports the interpretation without establishing the claim directly. |

<!-- CLAIMS:END -->

## Contradicted claims

A contradiction is a relationship between two claims, never an evidence level or
a verdict on a document. Each row names both claims and states which one the
stronger evidence supports. Machine-readable form: `contradictions` in
`analysis.json`.

| Relationship | Claims | Evidence | Which claim the evidence supports | Defect |
| --- | --- | --- | --- | --- |
| CONTA-001 | `SCHED-CLAIM-002` vs `HIST-CLAIM-003` | [EVID:CODE-008] [EVID:CODE-021] [EVID:TEST-009] [EVID:TEST-011] | the implementation (re-queue path) | D1 |
| CONTA-002 | `SCHED-CLAIM-005` vs `HIST-CLAIM-003` | [EVID:CODE-018] [EVID:TEST-010] | the implementation (permanent worker exit) | D2 |
| CONTA-003 | `SCHED-CLAIM-004` vs `HIST-CLAIM-003` | [EVID:CODE-009] [EVID:CODE-010] | the implementation (`failed` stays claimable) | D3 |
| CONTA-004 | `ARCH-CLAIM-002` vs `HIST-CLAIM-003` | [EVID:CODE-013] [EVID:CODE-015] [EVID:SCOPE-003] | the implementation (single HTTP path) | — |
| CONTA-005 | `ARCH-CLAIM-004` vs `HIST-CLAIM-003` | [EVID:CODE-016] [EVID:CODE-021] [EVID:TEST-012] | the implementation (discovery stored before dedup) | D9 |
| CONTA-006 | `PROV-CLAIM-003` vs `HIST-CLAIM-003` | [EVID:CODE-022] [EVID:CODE-023] | the implementation (fingerprint index never read) | D8 |
| CONTA-007 | `ARCH-CLAIM-008` vs `HIST-CLAIM-003` | [EVID:CODE-009] [EVID:SCOPE-004] | the implementation (per-instance ownership) | — |

## Claims deliberately not made

| Not claimed | Why not |
| --- | --- |
| "The engine produces evidence" | observations and discoveries exist; the evidence layer is `NOT_IMPLEMENTED` (`PROV-CLAIM-005`) |
| "The engine measures coverage" | no coverage object exists (`SCOPE-CLAIM-003`) |
| "The search is exhaustive / complete" | no termination or coverage criterion exists |
| "The architecture is protocol-agnostic" | acquisition is HTTP-only (`ARCH-CLAIM-002`) |
| "Candidate claiming can never occur twice" | true at the claim site, contradicted end to end (`SCHED-CLAIM-002`) |
| "DVB compatibility" | non-goal, absence verified (`SCOPE-CLAIM-001`, `SCOPE-CLAIM-006`) |
| "The prototype is production-ready" | nine documented defects, four of them P0 |

## Change control

These records describe the repository at `cc8df73` plus the executed
documentation changes `R-001 … R-018`. No code change was made: the artifact
digest is unchanged and enforced by `tools/verify.mjs`. Proposed code changes
(`R-101 … R-112`) are listed as `PLAN ONLY` in the
[change register](change-register-2026-09-10.md) and are not reflected in any
claim above.
