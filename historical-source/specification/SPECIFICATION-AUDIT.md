# Specification Audit

> **Derivation gate: CLOSED — REJECTED_INVALID_OBLIGATION_PACKAGE.** The v10.1 input contract failed, no source obligation is `VERIFIED`, epistemic `UNKNOWN` records remain, and four obligation conflicts are unresolved. Protocol-v11 therefore emits no normative requirements. This is a validated rejection/audit package, not a normative implementation specification.

## Validation procedure

| Step | Name | Result |
|---|---|---|
| 1 | Validate input contract | FAIL |
| 2 | Validate obligation registry | BLOCKED_UNVERIFIED |
| 3 | Validate obligation references | PASS_STRUCTURAL |
| 4 | Validate requirement schema | PASS_EMPTY_REJECTED_REGISTRY |
| 5 | Validate source traceability | PARTIAL_TO_OBLIGATION |
| 6 | Validate dependency graph | PASS_EMPTY_REQUIREMENT_GRAPH |
| 7 | Validate rule predicates | PASS_EMPTY_REJECTED_REGISTRY |
| 8 | Validate acceptance criteria | PASS_EMPTY_REJECTED_REGISTRY |
| 9 | Validate oracle references | PASS_EMPTY_REJECTED_REGISTRY |
| 10 | Validate implementation boundaries | PASS_EMPTY_REJECTED_REGISTRY |
| 11 | Detect contradictions | BLOCKED_UPSTREAM_CONFLICTS |
| 12 | Detect semantic narrowing/widening | BLOCKED_NO_REQUIREMENTS |
| 13 | Compute coverage | BLOCKED |
| 14 | Validate conformance claims | PASS_NO_CLAIM |
| 15 | Produce specification certificate | FAIL_CERTIFICATE_EMITTED |

## Completeness dimensions

| Dimension | Classification | Detail |
|---|---|---|
| TRACEABILITY_COMPLETENESS | PARTIAL | source through obligation only |
| SEMANTIC_COMPLETENESS | BLOCKED | no admitted requirements |
| VALIDATION_COMPLETENESS | FULL | rejection path structurally validated |
| VERIFICATION_COMPLETENESS | BLOCKED | no verified source obligations |
| FAILURE_COMPLETENESS | BLOCKED | no failure requirements admitted |
| SECURITY_COMPLETENESS | BLOCKED | no security requirements admitted |
| COMPATIBILITY_COMPLETENESS | BLOCKED | v7 missing upstream |
| IMPLEMENTATION_BOUNDARY_COMPLETENESS | BLOCKED | no mandatory requirements |

## Failure mode registry

- `REQUIREMENT_WITHOUT_OBLIGATION`
- `REQUIREMENT_WITHOUT_EVIDENCE`
- `UNTRACED_REQUIREMENT`
- `ORPHAN_OBLIGATION`
- `NON_TESTABLE_REQUIREMENT`
- `ORACLE_CIRCULARITY`
- `ORACLE_IMPLEMENTATION_COUPLING`
- `DEPENDENCY_CYCLE`
- `UNRESOLVED_CONFLICT`
- `SEMANTIC_NARROWING`
- `SEMANTIC_WIDENING`
- `RETROACTIVE_NORMATIVITY`
- `HISTORICAL_CONTAMINATION`
- `FALSE_VERIFICATION`
- `FALSE_PROOF`
- `HIDDEN_EXCEPTION`
- `UNDEFINED_SCOPE`
- `UNDEFINED_BOUNDARY`
- `UNMEASURABLE_PROPERTY`
- `MISSING_NEGATIVE_TEST`
- `COMPATIBILITY_OVERCLAIM`
- `UNJUSTIFIED_STRENGTHENING`
- `HARNESS_CONFUSION`
- `UNKNOWN_ESCALATION`

## Detected failure modes

- `ORPHAN_OBLIGATION`
- `UNRESOLVED_CONFLICT`
- `UNKNOWN_ESCALATION`

## Pipeline invariants

| ID | Statement | Status | Basis |
|---|---|---|---|
| V11-I01 | Every historical requirement traces to historical evidence. | PASS | CLOSED_GATE_PREVENTS_INVALID_TRANSFORMATION |
| V11-I02 | Every mandatory requirement has an acceptance criterion. | PASS | CLOSED_GATE_PREVENTS_INVALID_TRANSFORMATION |
| V11-I03 | Every safety/security requirement has a verification path. | PASS | CLOSED_GATE_PREVENTS_INVALID_TRANSFORMATION |
| V11-I04 | Requirement dependencies are explicit. | PASS | CLOSED_GATE_PREVENTS_INVALID_TRANSFORMATION |
| V11-I05 | Requirement conflicts are explicit. | PASS | CLOSED_GATE_PREVENTS_INVALID_TRANSFORMATION |
| V11-I06 | Historical and future requirements are distinguishable. | PASS | CLOSED_GATE_PREVENTS_INVALID_TRANSFORMATION |
| V11-I07 | Implementation location is not confused with semantic definition. | PASS | CLOSED_GATE_PREVENTS_INVALID_TRANSFORMATION |
| V11-I08 | Test existence is not confused with test adequacy. | PASS | CLOSED_GATE_PREVENTS_INVALID_TRANSFORMATION |
| V11-I09 | Verification status is not confused with epistemic status. | PASS | CLOSED_GATE_PREVENTS_INVALID_TRANSFORMATION |
| V11-I10 | Requirement strength is not confused with obligation strength. | PASS | CLOSED_GATE_PREVENTS_INVALID_TRANSFORMATION |
| V11-I11 | Requirement type is not confused with obligation class. | PASS | CLOSED_GATE_PREVENTS_INVALID_TRANSFORMATION |
| V11-I12 | A requirement may not strengthen historical meaning without explicit disposition. | PASS | CLOSED_GATE_PREVENTS_INVALID_TRANSFORMATION |
| V11-I13 | Negative requirements remain testable. | PASS | CLOSED_GATE_PREVENTS_INVALID_TRANSFORMATION |
| V11-I14 | Failed verification remains traceable to the failed requirement. | PASS | CLOSED_GATE_PREVENTS_INVALID_TRANSFORMATION |
| V11-I15 | Specification changes preserve historical lineage. | PASS | UPSTREAM_LINEAGE_RETAINED_AND_REFERENCED |

## Explicit assumptions

| ID | Statement | Epistemic | Validation |
|---|---|---|---|
| ASSUMP-001 | The v10.1 package is source-local and not accepted as complete. | PROVED | Read v10.1 INPUT-CONTRACT status. |
| ASSUMP-002 | No current architecture or roadmap may repair missing historical inputs. | SUPPORTED | Inspect v11 input bindings and traceability graph. |
