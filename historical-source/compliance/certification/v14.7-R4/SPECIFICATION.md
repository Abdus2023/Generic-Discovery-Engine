# v14.7-R4 — Reference Domain Model and Executable Conformance Layer

## 1. Reference Architecture
The reference architecture separates typed domain objects, layered validation, evaluation, conformance, authorization, state transitions, event storage, and projection.

## 2. Rust Crate Boundary
The no-dependency Rust crate mirrors domain, validation, evaluation, authorization, state, events, projection, identity, and conformance modules without changing normative semantics.

## 3. Semantic Types
Security-sensitive identities use distinct newtypes rather than a universal string alias.

## 4. Evaluation Result
EvaluationValue remains exactly True, False, Unknown, Blocked, and Invalid; diagnostics remain adjacent metadata.

## 5. Validation Result
ValidationStatus remains exactly Valid, Invalid, Blocked, and Unknown and cannot substitute for EvaluationValue.

## 6. Conformance Result
ConformanceStatus remains the frozen seven-state domain and every result binds a RequirementId.

## 7. Typed Pipeline
Raw, validated, evaluated, conformant, eligible, authorized, decided, executed, and verified APIs remain typed boundaries.

## 8. Validation Gate
Evaluation receives ValidatedSubject; conversion from arbitrary outer data occurs first.

## 9. Validation Errors
ValidationError preserves structural, reference, integrity, temporal, scope, policy, authority, evidence, and freshness provenance.

## 10. Evaluation Errors
EvaluationError is separate; semantic Unknown is not an evaluator execution failure.

## 11. Evaluator Contract
Evaluator cannot certify, authorize, mutate authority or policy, mutate history, or execute releases.

## 12. Aggregation
Aggregation rejects Invalid before precedence and deterministically applies False, Blocked, Unknown, then True.

## 13. Empty Mandatory Set
The R4 runtime profile explicitly selects DENY for the pre-existing EmptyMandatoryAction profile choice; no undocumented default exists.

## 14. Authority Qualification
Authority qualification remains distinct from operation authorization.

## 15. Authorization
Authorization requires eligibility, qualified authority, valid policy, scope, credential, time, and threshold.

## 16. State Transition Guard
Every mutation passes the single transition guard with predecessor, legality, evidence, authority, scope, and temporal checks.

## 17. Event Store Boundary
The event store accepts only ValidatedEvent and returns CommittedEvent.

## 18. Atomicity Requirement
The reference store serializes sequence reservation and append under one lock; production durability remains unverified.

## 19. Projection
Projection consumes committed validated history and cannot repair, invent, rewrite, or consult hidden mutable state.

## 20. Projection Determinism
Identical history, profile, and algorithm version produce identical state identity.

## 21. Canonical Serialization
Hashable objects use profile-pinned canonical bytes, never arbitrary language map order.

## 22. Hash Domain Separation
Identity hashing composes an explicit domain tag with canonical bytes.

## 23. Decision-Basis Hash
Decision basis binds all fifteen supplied decision-relevant inputs.

## 24. Reuse Checker
Reuse is deterministic: identical basis may be reusable subject to constraints; different basis is not reusable.

## 25. Test Vector Structure
Every vector is self-contained and identifies profile, requirements, setup, operation, expected domain results, forbidden behavior, and evidence.

## 26. Golden Test Categories
G-001 through G-036 are executable golden vectors.

## 27. Property Tests
P-001 through P-016 are executable property vectors.

## 28. Boundary Tests
Fifteen typed boundary vectors ask what may cross, which identity is carried, and what failure is produced.

## 29. Conformance Harness
The deterministic harness records profile, implementation, vector identity, outcomes, evidence, timestamp, and version.

## 30. Conformance Levels
ProfileConformance and ImplementationConformance remain separate; the Rust implementation cannot be conformant until compiled and tested.

## 31. CI Gate
The CI gate orders schema, reference, canonicalization, hash, state, vector, property, concurrency, projection, and report stages.

## 32. Rust Safety Boundary
The crate forbids unsafe code; any future exception requires an explicit SAFETY invariant and cannot underwrite semantic conformance.

## 33. Reference Implementation Principle
Types and APIs make evaluate(raw), authorize(TRUE), and execute(APPROVED) inexpressible through the preferred interface.

## 34. Remaining Semantic Questions
Semantic questions remain separate from library, database, async runtime, vector encoding, and performance implementation choices.

## 35. Revised Artifact Tree
Artifacts are physically grouped as normative, profile, implementation, schemas, runtime, vectors, and reports inside the append-only R4 package.

## 36. Closure Test
Closure is reported only to the strength demonstrated by schemas, source checks, vectors, and available toolchains.

## 37. Final Principle
No implementation type, validation result, evaluation result, profile choice, or operational state may acquire higher-layer semantic authority.
