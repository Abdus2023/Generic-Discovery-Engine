# Generic Discovery Engine — Protocol-v11.1 Final Specification

> **v11.1 derivation gate: CLOSED — REJECTED_INVALID_OBLIGATION_PACKAGE.** The v10.1 input contract failed; 54 obligations are unverified, two retain UNKNOWN epistemic status, fourteen properties remain UNKNOWN, and four obligation conflicts are unresolved. No normative object, verification result, or conformance claim is derived. Non-normative context is explicitly classified and cannot impose behavior.

## 1. Three-plane model

**Evidence** explains historical basis. **Normative objects** would state enforceable behavior. **Guidance** explains possible approaches without imposing behavior. Verification and conformance remain downstream.

## 2. Canonical chain

`SOURCE → EVIDENCE → PROPERTY → OBLIGATION → REQUIREMENT → RULE → CRITERION → ORACLE → RESULT → VERIFICATION → CONFORMANCE`. The current chain stops at obligation.

## 3. Input rejection

| Failure | Class | Affected | Detail |
|---|---|---|---|
| INPUT_MISSING | INPUT_FAILURE | 4 | Required Protocol-v4 through Protocol-v7 upstream stages remain absent. |
| INPUT_HASH_MISMATCH | INPUT_FAILURE | 1 | The v10.1 package preserves the Protocol-v1 byte/range integrity failure. |
| UNVERIFIED_SOURCE | VERIFICATION_FAILURE | 54 | No source obligation is VERIFIED with verification evidence. |
| OBLIGATION_UNKNOWN | SEMANTIC_FAILURE | 2 | Obligation epistemic uncertainty cannot be escalated into normativity. |
| PROPERTY_UNKNOWN | SEMANTIC_FAILURE | 14 | Unknown historical properties cannot silently define a normative domain. |
| CONFLICT_UNRESOLVED | CONFLICT_FAILURE | 4 | Unresolved obligation conflicts block affected normative derivation. |
| DERIVATION_GATE_CLOSED | DERIVATION_FAILURE | 54 | No normative semantic transformation is authorized. |

## 4. Normative plane

All normative registries are empty: 0 requirements, rules, conditions, predicates, criteria, oracles, invariants, transitions, effects, exceptions, boundaries, verifications, results, and conformance records.

## 5. Non-normative plane

Three guidance records, 54 source-qualified rationales, and three explicit assumptions are emitted. There are no implementation notes or examples because no requirement exists.

## 6. Object identity and schemas

Every instantiated first-class object has a stable ID, type, schema version, lifecycle status, and provenance. Thirty dedicated schemas cover the required registry plus constraint, evidence, property, obligation, and certificate records.

## 7. Dependencies, conflicts, and lineage

The requirement dependency graph is empty and acyclic. Obligation dependencies and lineage are not reused as requirement dependencies. Four unresolved obligation conflicts remain explicit blockers.

## 8. Guidance separation

Guidance contains no uppercase normative operator, is marked `normative: false`, and has no related requirement. Rationale and assumptions also remain non-normative.

## 9. Acceptance, oracle, and harness boundary

No acceptance criterion or oracle exists without a requirement. The harness is modeled separately and cannot silently alter tested semantics.

## 10. Verification and conformance

No test result or verification record is fabricated. Highest claimed conformance is `L0_NONE`, with claims disabled.

## 11. Traceability

Forward and reverse canonical traceability reaches obligations. Supporting rationale, guidance, and assumption edges are explicitly non-normative and do not extend the canonical transformation.

## 12. Completeness

Schema completeness is `FULL`; traceability is `PARTIAL`; all normative, acceptance, oracle, verification, conflict-resolution, compatibility, security, failure, and boundary dimensions are `BLOCKED`. No aggregate score hides this.

## 13. Certificate

| Field | Value |
|---|---|
| specification | 11.1 |
| validation | FAIL |
| requirements | 0 |
| guidance | 3 |
| rationales | 54 |
| certificate hash | 976a8ca2280b6b85f33744b130a4915a0c65450c31a44aa255b80d3b8472ce46 |

## 14. Remediation boundary

Opening the normative gate requires valid upstream v1–v9 evidence, verified v10.1 obligations, resolved UNKNOWN properties and obligations, and explicit conflict resolution. Future architecture cannot be used backward to repair these inputs.

## Final disposition

**`REJECTED_INVALID_OBLIGATION_PACKAGE` — the v11.1 framework is machine-valid, but no normative specification or conformance claim is authorized.**
