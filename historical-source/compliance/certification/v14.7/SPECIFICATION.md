# v14.7 — Mechanical Semantic Closure and Executable Normative Validation

## 1. Objective
Mechanically close v14.6 without adding a broad architectural layer. v14.7 supplies one registry per semantic domain, executable closure tables, and complete schemas.

## 2. v14.6 Audit Findings
The audit found lifecycle/result ambiguity for evaluations, mixed administrative and derived authority status, underspecified reproducibility, freshness clocks, ordering, concurrency, reuse actions, retention state, and missing complete failure/transition matrices.

## 3. Resolved Contradictions
All repairs are explicit in CONTRADICTIONS.yaml. Candidate retention is a disposition rather than lifecycle. Authority expiry/uncertainty are derived effectiveness rather than administrative lifecycle. INVALID terminates evaluation validity and does not compete with FALSE.

## 4. Canonical Evaluation Model
Evaluation lifecycle CREATED, COMPLETED, INVALIDATED is independent of immutable EvaluationResult TRUE, FALSE, UNKNOWN, BLOCKED, INVALID. Reproduction requires identical canonical context, evaluator identity/version/content hash, predicate implementation hash, inputs, evidence, policy, scope, environment, time basis, and deterministic algorithm.

## 5. Canonical Authority Model
Credential proves control of an identity; policy grants capability. Neither substitutes for the other. Issuance and release-decision capabilities are separately scoped. Delegation is set inclusion. N-of-M counts distinct effective authorities bound to identical action basis.

## 6. Fail-Closed Boundary Model
FAIL-CLOSED-MATRIX.yaml contains all 132 required condition/object combinations and records evaluation, eligibility, authorization, continuation, and retry semantics.

## 7. Precedence Model
Six precedence domains are registered. They are intentionally not merged: integrity acceptance, predicate aggregation, eligibility mapping, authorization mapping, decision mapping, and transition conflict resolution answer different questions.

## 8. Certificate Semantics
CertificateReusable, CertificateIssuanceReusable, and CertificateValidity are distinct. Candidate, DRAFT construction, authorization, issuance, lifecycle and validity remain independent.

## 9. Release Semantics
Release and gate are immutable definitions. Eligibility is derived. Decisions are immutable authority actions. Executions and verifications have independent history and projections.

## 10. Decision Reuse
DecisionReusable is conjunction over exact typed comparisons and temporal predicates. DECISION-BASIS-CHANGE-ACTIONS.yaml gives an exact action for each changed field.

## 11. Temporal Semantics
UTC instants and half-open intervals apply. Sequence and predecessor links establish causal stream order; commit index resolves publication. Equal timestamps do not affect order. Profiled clock skew is mandatory.

## 12. Event and Projection Semantics
Events are atomic compare-and-append records. Invalid history yields no trusted projection. Rebuild starts from the genesis event and verifies every reference, hash, signature, sequence and transition before publication.

## 13. Concurrency Semantics
Every authoritative append is linearizable with aggregate expected-version and scoped idempotency uniqueness. The first successful commit-index allocation wins; losers receive CONCURRENCY_FAILURE or an idempotent replay, never a timestamp-based winner.

## 14. Canonical Validation Procedure
VALIDATION-PROCEDURE.yaml is the sole fifteen-stage procedure. Each stage declares inputs, outputs, failure, and whether processing continues.

## 15. Complete Schemas
Forty v14.7 schemas define all inherited and closure objects with required fields, explicit nullability, enums, typed references, identity, hashing, immutability, timestamps, scope and constraints.

## 16. Complete State-Transition Tables
STATE-TRANSITION-TABLES.yaml covers all twelve requested domains. Derived result objects create new immutable snapshots and advance projections; they do not mutate prior results.

## 17. Failure Taxonomy
Eighteen canonical failure classes replace no historical record but normalize all current evaluator output. Translation aliases map predecessor names into the canonical taxonomy.

## 18. Machine-Oriented Test Matrix
Fifty-five synthetic vectors cover positive, negative, boundary, concurrency, history, identity, reuse and temporal behavior.

## 19. Formal Invariants
INVARIANTS.yaml consolidates machine-checkable cross-domain, fail-closed, identity, temporal, event, concurrency, and reuse propositions.

## 20. Contradictions.yaml
Each resolved conflict records location, old rule, new rule, resolution, reason, and impact. No repair is silent.

## 21. Ambiguities.yaml
Only credential mechanism, trusted clock technology and trust-root profile remain safety-relevant UNKNOWNs. Safe defaults prohibit authority or time-dependent reuse when profiles are absent.

## 22. Revised Artifact Tree
The physical append-only v14.7 package implements the logical domains without moving or rewriting historical source.

## 23. Traceability
Forward and reverse links retain the complete history-to-new-evidence chain and add audit finding, contradiction, rule, schema, vector and validator trace.

## 24. Anti-Regression Rules
No domain collapse, implicit authority, vacuous truth, timestamp-only ordering, history mutation, context-wildcard reuse, hash substitution or invalid-to-false conversion is allowed.

## 25. Open Questions
No new semantic layer is justified. Deployment profiles must resolve the three retained safety-relevant ambiguities before affected operations proceed.

## 26. Final Principle
No state transition may establish a stronger semantic claim than its validated evidence, evaluation result, policy, authority, temporal scope, and identity binding justify.
