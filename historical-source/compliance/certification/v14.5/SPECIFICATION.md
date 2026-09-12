# v14.5 — Normative Evaluation Results, Certificate Issuance Authority & Fail-Closed Validation

## 1. Objective
v14.5 adds one canonical EvaluationResult, explicit certificate issuance authority, and five fail-closed validation boundaries without redesigning v14.3 or v14.4. The protected architecture remains HISTORY → EVIDENCE → HISTORICAL PROPERTY → OBLIGATION → REQUIREMENT → CONFORMANCE → CERTIFICATION → AUTHORIZATION → EXECUTION → OBSERVATION ↺.

## 2. Resolved contradictions
Evaluation results are immutable evaluator claims, not lifecycle, business state, conformance, or authorization. `FALSE` is a trustworthy semantic negative; `INVALID` says the evaluation artifact cannot be trusted. Eligibility and issuance authority are independent. Certificate validity never supplies issuance authority. Fail-closed behavior preserves UNKNOWN, BLOCKED, FALSE, and INVALID rather than collapsing them.

The supplied workflow labels VALIDATED, EVALUATED, and AUTHORIZED are cross-domain workflow milestones, not additions to the CertificateCandidate lifecycle. The v14.4 candidate lifecycle remains CREATED, ACTIVE, CONSUMED, CANCELLED, EXPIRED, RETAINED. Likewise, the supplied lifecycle diagram does not create ISSUED → CANCELLED: CANCELLED remains reachable from DRAFT only.

## 3. Canonical evaluation-result model
Every normative evaluator returns the complete object in `schema/evaluation-result.schema.yaml`. Results are exactly TRUE, FALSE, UNKNOWN, BLOCKED, INVALID. Specialized validity, eligibility, authority, and verification objects reference canonical EvaluationResult identities; they may not create incompatible predicate enums.

## 4. Evaluation integrity and context
An EvaluationResult is accepted only after independent schema, evaluator identity, scope, reference, semantic, time, sequence, and hash validation. Its declared integrity field is not self-authenticating. EvaluationContext is immutable before evaluation starts; any context change creates a new context and evaluation.

## 5. Fail-closed boundaries
The ordered boundaries are L0 structural, L1 referential, L2 integrity, L3 semantic, and L4 authorization. Failure at L0–L2 produces INVALID and prevents semantic aggregation. L3 may produce TRUE, FALSE, UNKNOWN, or BLOCKED. L4 can authorize only independently valid inputs and TRUE required conditions.

## 6. Aggregation and freshness
For valid mandatory results, FALSE > BLOCKED > UNKNOWN > TRUE. Any required INVALID terminates aggregation as INVALID even if FALSE also exists. Freshness is independently evaluated. STALE maps to UNKNOWN by default or BLOCKED under an explicit operational-blocker policy; it never silently becomes FALSE.

## 7. Empty mandatory sets
ReleaseGate requires `empty_mandatory_action = ALLOW|DENY|BLOCK|UNKNOWN`. Omitting the field makes policy INVALID. ALLOW is explicit engineering policy, never vacuous truth.

## 8. Certificate issuance authority
IssuanceAuthority separates capability, credential, temporal effectiveness, certificate/implementation/release scope, delegation, and multi-party threshold. Authority existence, administrator naming, UI access, process ownership, evaluator operation, or audit success never implies issuance permission.

## 9. Issuance authorization
CertificateIssuanceAuthorization references three canonical EvaluationResults: eligibility, authority, and policy. INVALID required input → INVALID; otherwise any FALSE → REFUSED; otherwise BLOCKED → BLOCKED; otherwise UNKNOWN → UNKNOWN; all TRUE plus valid sealed inputs and candidate → AUTHORIZED.

## 10. Candidate and certificate boundary
CertificateCandidate is a proposed immutable payload and evidence binding. Certificate(DRAFT) is a separately identified materialized certificate payload. Candidate construction, validation, evaluation, authorization, DRAFT construction, and ISSUE are distinct transitions. Authorization does not issue.

Candidate creation cannot reference a not-yet-created eligibility result without a cycle. Therefore the immutable candidate binds the eligibility and authority policies; completed eligibility and authority result references are mandatory on IssuanceAuthorization. This is the minimum stage-correct interpretation of the requested cross-object chain.

## 11. Issuance guards and lifecycle
DRAFT → ISSUED requires valid candidate, AUTHORIZED issuance record, active scoped issuance authority, valid payload and snapshot seal, unique certificate identity, and no conflicting active certificate. ISSUED cannot transition to CANCELLED. Terminal lifecycle states cannot reactivate.

## 12. Certificate validity
Validity consumes canonical results for schema, content hash, seal, signature, authority-at-issuance, scope, time, revocation, and supersession. Valid all-TRUE predicates produce VALID; trustworthy FALSE produces derived INVALID; before-interval produces NOT_YET_VALID; uncertainty produces UNKNOWN. A required INVALID EvaluationResult produces no authoritative CertificateValidity projection, rather than falsely claiming semantic invalidity. No validity outcome fabricates lifecycle history.

## 13. Release eligibility and decision
Release eligibility consumes valid canonical results and uses the same precedence. ReleaseDecision remains an immutable authority action. UNKNOWN eligibility is not DEFERRED until an authorized actor records an explicit defer action and reason. Every decision policy maps ELIGIBLE, INELIGIBLE, BLOCKED, UNKNOWN; incomplete policy is INVALID.

## 14. Authorization boundary
The privileged boundary is crossed only with VALID input validation and evaluation integrity, all required TRUE predicates, TRUE authority and policy evaluations, valid scope, and sealed snapshot. A returned error is insufficient: the operation itself must be prevented.

## 15. Event and projection model
All changes emit immutable typed events. Per subject-domain stream, sequence numbers start at zero and increase exactly by one; previous_event_id names the exact preceding event. Sequence, causal link, and commit order must cohere. `occurred_at` is descriptive and never sole ordering authority. Invalid history yields no trusted current projection.

## 16. Validation procedure
The sole canonical twenty-step algorithm is machine-defined in `VALIDATION-PROCEDURE.yaml`: load; structure; nullability; references; compatibility; hashes/signatures; ordering; scope; time; freshness; policy; authority; evaluation integrity; predicates; aggregation; immutable evaluation; guarded transition; immutable event; rebuild; verify.

## 17. Identity, binding, and reuse
Artifact, certificate, snapshot, decision-basis, and event hashes are typed and non-substitutable. Decision reuse requires equality of every listed decision-relevant identity and hash. A single changed input requires a new evaluation and decision. Human-readable versions never satisfy object references.

## 18. Complete schemas
Thirty v14.5 schemas define canonical evaluations, freshness, authority, approvals, certificate and release objects, events, failures, and all current projections. Candidate discovery remains the exact v14.3 discovery-domain schema and is not reused for certificate candidacy. Each schema declares identity, immutability, typed reference resolution, self-excluding hashing, timestamps, and scope constraints.

## 19. State-transition semantics
Candidate lifecycle, certificate lifecycle, evaluation event status, authorization status, release decision, execution, and verification remain independent enums. No workflow diagram is interpreted as one universal lifecycle.

## 20. Failure classification
Every failure record identifies object, boundary, input, class, evidence, severity, retry meaning, and whether authorization is prohibited. Evaluation failures are not implementation failures. The thirteen v14.5 failure classes refine, rather than erase, v14.4 responsible-layer defects.

## 21. Test vectors
Forty synthetic non-normative executable-style vectors cover the fourteen required examples plus aggregation dominance, invalid precedence, freshness, optional references, automation, delegation, distinct multi-party approvals, non-implication boundaries, ordering, projection, reuse, historical replay, and typed hashes.

## 22. Traceability and epistemic discipline
Both forward and reverse traceability extend through EvaluationContext and EvaluationResult. Claims use PROVED, SUPPORTED, INFERRED, CONJECTURED, CONTRADICTED, UNKNOWN and are typed as historical fact, derived historical model, engineering obligation, normative requirement, design option, or current engineering judgment.

## 23. Open questions
Credential technology, freshness-clock mechanism, and deployment trust roots remain UNKNOWN and deployment-profile-defined. Their explicit references and verification are mandatory; no default is invented.

## 24. Current historical status
No current certificate candidate, certificate, authority grant, evaluation, release, decision, execution, or verification record is invented. The historical audit remains blocked at the inherited specification-validation boundary.

## 25. Final principle
FACT → EVALUATION → ATTESTATION → AUTHORIZATION → EXECUTION → OBSERVATION remains grounded in IMMUTABLE EVENTS → VALIDATION → CURRENT PROJECTION. No state transition may establish a stronger semantic claim than its validated evidence, evaluation result, policy, authority, and scope justify. No invalid or insufficient input may cross a fail-closed authorization boundary.
