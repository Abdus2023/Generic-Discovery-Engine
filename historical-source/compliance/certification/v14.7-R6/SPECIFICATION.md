# v14.7-R6 — Machine Schema and Typed Domain Realization

## 1. Purpose
R6 converts frozen R5 semantics into a machine-oriented contract and introduces no semantic state.

## 2. Layer Model
Five planes are explicit and no plane implicitly inherits authority.

## 3. Closed Enum Registry
The supplied sixteen machine enums and four inherited frozen domains reject unknown values.

## 4. Identifier Domains
Semantic identifier domains remain distinct even when serialized as strings.

## 5. Normative Requirement Schema
Normative obligations remain technology-neutral and machine-representable.

## 6. Implementation Requirement Schema
Implementation requirements require traceable normative and profile origins.

## 7. Implementation Instruction
Instruction mandatory flags apply only within owning implementation authority.

## 8. ValidationResult
Validation controls processing eligibility and never establishes proposition truth.

## 9. EvaluationResult
EvaluationResult records a completed evaluation and remains distinct from error.

## 10. Evaluator Error
Twelve observable errors preserve the eleven supplied codes plus inherited dependency-unavailable coverage.

## 11. Evaluator Contract
Evaluator returns Result<EvaluationResult, EvaluationError> and has no higher-layer authority.

## 12. Error Policy
Error defaults to evaluation failure; semantic mapping requires explicit profile policy.

## 13. Error Classification
Infrastructure failure never becomes a false claim about the subject.

## 14. Conformance Result
Conformance is requirement-bound and cannot be inferred from isolated TRUE.

## 15. Explicit Conversion Matrix
Five named conversion contracts replace generic conversion.

## 16. State Transition Guard
State changes require structural, reference, integrity, temporal, scope, authority, and transition checks.

## 17. Certificate Transitions
Only the five supplied certificate lifecycle edges are legal.

## 18. Release Execution Transitions
Only the six supplied release-execution edges are legal.

## 19. Event Contract
Invalid events are rejected in the declared validation order and never repaired.

## 20. Projection Contract
Projection is deterministic from validated history, profile, and algorithm.

## 21. Decision-Basis Reuse
Changed decision basis is NOT_REUSABLE absent explicit safe compatibility.

## 22. Typed Pipeline
Typed stages preserve independent validation, evaluation, conformance, authorization, decision, execution, and verification.

## 23. Rust Type-State Boundary
Typestate is an implementation technique; equivalent machine-checkable boundaries are required.

## 24. Conformance Test Categories
T1 through T7 are executable and mandatory.

## 25. Minimum Negative Test Set
N-001 through N-018 are executable negative vectors.

## 26. Machine-Checkable Invariants
R6-I01 through R6-I18 are executable invariants.

## 27. Updated Artifact Tree
Artifacts are physically grouped by semantics, plane, runtime, errors, conversions, transitions, Rust, and tests.

## 28. What R6 Resolves
Closed enums, authority separation, and result/error separation resolve the supplied practical ambiguities.

## 29. What R6 Does Not Yet Define
Concrete production backends, predicate language, concurrency, and target integration remain implementation-only.

## 30. Closure Assessment
The machine contract is realized without v14.8 or a new semantic state; production implementation remains unverified.

## Final Principle
Semantic authority belongs to the defining layer. Evaluation produces a semantic result only on contractual completion; otherwise it produces an explicit evaluator error interpreted only by explicit policy.
