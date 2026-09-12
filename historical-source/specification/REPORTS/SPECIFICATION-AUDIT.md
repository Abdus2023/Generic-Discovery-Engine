# v11.1 Specification Audit

> **v11.1 derivation gate: CLOSED — REJECTED_INVALID_OBLIGATION_PACKAGE.** The v10.1 input contract failed; 54 obligations are unverified, two retain UNKNOWN epistemic status, fourteen properties remain UNKNOWN, and four obligation conflicts are unresolved. No normative object, verification result, or conformance claim is derived. Non-normative context is explicitly classified and cannot impose behavior.

## Ordered audit

| Order | Stage | Result |
|---|---|---|
| 1 | INPUT VALIDATION | FAIL |
| 2 | SCHEMA VALIDATION | PASS |
| 3 | REFERENCE VALIDATION | PASS |
| 4 | DERIVATION VALIDATION | FAIL_GATE_CLOSED |
| 5 | NORMATIVE/GUIDANCE SEPARATION | PASS |
| 6 | DEPENDENCY VALIDATION | PASS_EMPTY_REQUIREMENT_GRAPH |
| 7 | CONFLICT DETECTION | BLOCKED_UPSTREAM_CONFLICTS |
| 8 | SEMANTIC NARROWING/WIDENING | BLOCKED_NO_REQUIREMENTS |
| 9 | RULE VALIDATION | PASS_EMPTY |
| 10 | ACCEPTANCE VALIDATION | PASS_EMPTY |
| 11 | ORACLE VALIDATION | PASS_EMPTY |
| 12 | BOUNDARY VALIDATION | PASS_EMPTY |
| 13 | TRACEABILITY VALIDATION | PARTIAL_TO_OBLIGATION |
| 14 | CONFORMANCE VALIDATION | PASS_NO_CLAIM |

## Completeness

| Dimension | Classification | Reason |
|---|---|---|
| TRACEABILITY | PARTIAL | canonical trace reaches obligation |
| SEMANTICS | BLOCKED | normative derivation gate closed |
| NORMATIVITY | BLOCKED | normative derivation gate closed |
| SCHEMA | FULL | all first-class schemas emitted |
| DEPENDENCY | BLOCKED | normative derivation gate closed |
| CONFLICT | BLOCKED | normative derivation gate closed |
| ACCEPTANCE | BLOCKED | normative derivation gate closed |
| ORACLE | BLOCKED | normative derivation gate closed |
| VERIFICATION | BLOCKED | normative derivation gate closed |
| SECURITY | BLOCKED | normative derivation gate closed |
| FAILURE | BLOCKED | normative derivation gate closed |
| COMPATIBILITY | BLOCKED | normative derivation gate closed |
| BOUNDARY | BLOCKED | normative derivation gate closed |

## Final invariants

| ID | Invariant | Status | Basis |
|---|---|---|---|
| V111-I01 | Normative rules are distinct from guidance. | PASS | CLOSED_GATE_OR_EXPLICIT_SEPARATION |
| V111-I02 | Guidance cannot create hidden mandatory behavior. | PASS | CLOSED_GATE_OR_EXPLICIT_SEPARATION |
| V111-I03 | Every mandatory requirement has a normative rule. | PASS | CLOSED_GATE_OR_EXPLICIT_SEPARATION |
| V111-I04 | Every mandatory requirement has an acceptance criterion. | PASS | CLOSED_GATE_OR_EXPLICIT_SEPARATION |
| V111-I05 | Every mandatory requirement has a verification path. | PASS | CLOSED_GATE_OR_EXPLICIT_SEPARATION |
| V111-I06 | Every historical requirement remains traceable to evidence. | PASS | CLOSED_GATE_OR_EXPLICIT_SEPARATION |
| V111-I07 | Future strengthening cannot masquerade as historical fact. | PASS | CLOSED_GATE_OR_EXPLICIT_SEPARATION |
| V111-I08 | Requirement class and obligation class remain independent. | PASS | CLOSED_GATE_OR_EXPLICIT_SEPARATION |
| V111-I09 | Requirement strength and obligation strength remain independent. | PASS | CLOSED_GATE_OR_EXPLICIT_SEPARATION |
| V111-I10 | Epistemic status and verification status remain independent. | PASS | CLOSED_GATE_OR_EXPLICIT_SEPARATION |
| V111-I11 | Dependencies and lineage remain distinct. | PASS | CLOSED_GATE_OR_EXPLICIT_SEPARATION |
| V111-I12 | Conflicts cannot be silently resolved. | PASS | CLOSED_GATE_OR_EXPLICIT_SEPARATION |
| V111-I13 | Implementation notes cannot redefine normative semantics. | PASS | CLOSED_GATE_OR_EXPLICIT_SEPARATION |
| V111-I14 | Examples cannot define normative scope. | PASS | CLOSED_GATE_OR_EXPLICIT_SEPARATION |
| V111-I15 | A test result cannot establish historical truth. | PASS | CLOSED_GATE_OR_EXPLICIT_SEPARATION |
| V111-I16 | Implementation location cannot substitute for a requirement. | PASS | CLOSED_GATE_OR_EXPLICIT_SEPARATION |
| V111-I17 | Every first-class object has a complete schema. | PASS | CLOSED_GATE_OR_EXPLICIT_SEPARATION |
| V111-I18 | Every cross-object reference is resolvable. | PASS | CLOSED_GATE_OR_EXPLICIT_SEPARATION |
| V111-I19 | Mandatory conformance requires verification evidence. | PASS | CLOSED_GATE_OR_EXPLICIT_SEPARATION |
| V111-I20 | No normative semantic transformation may occur without explicit traceability. | PASS | CLOSED_GATE_OR_EXPLICIT_SEPARATION |

## Failure-class registry

- `INPUT_FAILURE`
- `SCHEMA_FAILURE`
- `REFERENCE_FAILURE`
- `DERIVATION_FAILURE`
- `NORMATIVE_CLASSIFICATION_FAILURE`
- `DEPENDENCY_FAILURE`
- `CONFLICT_FAILURE`
- `SCOPE_FAILURE`
- `SEMANTIC_FAILURE`
- `RULE_FAILURE`
- `ACCEPTANCE_FAILURE`
- `ORACLE_FAILURE`
- `BOUNDARY_FAILURE`
- `TRACEABILITY_FAILURE`
- `VERIFICATION_FAILURE`
- `CONFORMANCE_FAILURE`

## Detected failures

| ID | Class | State | Affected | Detail |
|---|---|---|---|---|
| V111-INPUT-001 | INPUT_FAILURE | INPUT_MISSING | 4 | Required Protocol-v4 through Protocol-v7 upstream stages remain absent. |
| V111-INPUT-002 | INPUT_FAILURE | INPUT_HASH_MISMATCH | 1 | The v10.1 package preserves the Protocol-v1 byte/range integrity failure. |
| V111-VERIFY-001 | VERIFICATION_FAILURE | UNVERIFIED_SOURCE | 54 | No source obligation is VERIFIED with verification evidence. |
| V111-SEMANTIC-001 | SEMANTIC_FAILURE | OBLIGATION_UNKNOWN | 2 | Obligation epistemic uncertainty cannot be escalated into normativity. |
| V111-SEMANTIC-002 | SEMANTIC_FAILURE | PROPERTY_UNKNOWN | 14 | Unknown historical properties cannot silently define a normative domain. |
| V111-CONFLICT-001 | CONFLICT_FAILURE | CONFLICT_UNRESOLVED | 4 | Unresolved obligation conflicts block affected normative derivation. |
| V111-DERIVE-001 | DERIVATION_FAILURE | DERIVATION_GATE_CLOSED | 54 | No normative semantic transformation is authorized. |

No aggregate percentage is reported.
