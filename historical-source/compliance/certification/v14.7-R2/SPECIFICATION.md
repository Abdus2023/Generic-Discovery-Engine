# v14.7-R2 — Deterministic Executable Conformance Harness Profile

## 1. Executive Result
The semantic specification remains frozen. v14.7-R2 is an executable realization profile and reference harness, not v14.8.

## 2. v14.7-R1 Audit Findings
The audit found profile omissions—serialization, typed hashes, interfaces and executable oracles—but no unavoidable semantic contradiction.

## 3. Semantic Contradictions
No semantic contradiction was found. Realization choices are profile-level and explicitly scoped.

## 4. Schema Corrections
The inherited 49-schema effective set is audited; eight realization schemas close profile and harness records.

## 5. Canonical Serialization Profile
GDE-CJSON-1 uses constrained canonical JSON, UTF-8, NFC strings/keys, scalar-sorted maps, preserved arrays, integers only, canonical UTC timestamps and literal null.

## 6. Hash Domain Specification
Every hash has a unique domain prefix, exact input, canonicalization, SHA-256 algorithm, lowercase hexadecimal encoding, scope and purpose.

## 7. Reference Resolution Contract
Typed references resolve to exactly one matching type, identity, hash, scope and schema/version. Failures are not semantic FALSE.

## 8. Validation Interface Contract
Sixteen side-effect-free interfaces define input, output, failure, side effect and determinism contracts.

## 9. Evaluation Contract
Evaluate is deterministic over subject, predicate, sealed context, evaluator identity/version/hash and profile.

## 10. Authority Contract
QualifyAuthority deterministically checks credential, operation, set-contained scope, time, delegation and distinct N-of-M approvals.

## 11. State-Machine Contract
Executable transition definitions require state, event, guard, evidence, authority and scope.

## 12. Event-Store Contract
The reference event store implements atomic expected-version append, unique event identity, idempotent retry, canonical sequence and durable commit index.

## 13. Projection Contract
Project and VerifyProjection deterministically fail closed on untrusted history.

## 14. Reuse Contract
Reuse compares every named field and all temporal conditions; missing required comparison input is INVALID.

## 15. Concurrency Contract
Every listed race has uniqueness, serialization point, conflict, winner, retry and history effect.

## 16. Test Oracle Contract
Each oracle is a complete immutable machine record and has independently classified failure origin.

## 17. Property-Based Test Model
Generated finite-domain aggregation, basis mutation, non-implication and replay properties run without human interpretation.

## 18. Negative-Space Test Matrix
Eleven forbidden implications are executed and required to return REJECTED.

## 19. Machine-Readable Conformance Report
The report is immutable and scoped only to the reference harness; it does not attest the target engine.

## 20. Normative Invariants
Executable properties cover the frozen cross-domain invariants.

## 21. Implementation/Profile Boundary
Normative semantics, realization profile choices, and Python reference implementation are explicitly separated.

## 22. Revised Artifact Tree
Artifacts are append-only under certification/v14.7-R2; no historical file is moved.

## 23. Traceability
Specification rule → profile contract → schema/interface → oracle/property → result/report is bidirectional.

## 24. Anti-Regression Rules
No test may hide INVALID, infer authority, mutate history, bypass a stage, or misclassify failure origin.

## 25. Open Questions
Backend, language, clock hardware and trust roots remain implementation choices constrained by the profile contracts.

## 26. Final Principle
Prefer executing the frozen specification over extending it; no v14.8 layer is justified.
