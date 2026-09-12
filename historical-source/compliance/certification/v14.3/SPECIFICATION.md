# Protocol-v14.3 — Release Identity, Authorization, Execution & Verification

## Version
v14.3, refining the user-supplied v14.2 normative baseline without mutating predecessor artifacts.

## Scope and semantic corrections
- CERTIFICATE_CANDIDATE_DISTINCT_FROM_DISCOVERY_CANDIDATE_AND_CERTIFICATE
- CERTIFICATE_VALIDITY_HAS_NO_LIFECYCLE_DUPLICATE_STATUSES
- RELEASE_GATE_IS_POLICY_NOT_RESULT
- RELEASE_ELIGIBILITY_DISTINCT_FROM_DECISION
- DECISION_DISTINCT_FROM_EXECUTION
- EXECUTION_DISTINCT_FROM_POST_RELEASE_RESULT
- CURRENT_OBJECTS_ARE_HISTORY_PROJECTIONS

## State and data flow
```text
AUDIT SNAPSHOT → AGGREGATE → CERTIFICATE ELIGIBILITY → ISSUANCE → VALIDITY
→ RELEASE GATE → RELEASE ELIGIBILITY → RELEASE DECISION → EXECUTION → POST-RELEASE VERIFICATION
```

## Normative models
The complete machine definitions, transition tables, precedence rules, object schemas, temporal model, event model, projection model, validation procedure, invariants, traceability, failure modes, open questions, and 30 executable vectors are registered in `ARTIFACT-TREE.yaml`.

## Final principle
- NO_FACT_IS_A_DECISION
- NO_DECISION_IS_AN_ATTESTATION
- NO_ATTESTATION_IS_AUTHORIZATION
- NO_AUTHORIZATION_IS_EXECUTION
- NO_EXECUTION_IS_PROOF_OF_OUTCOME
