# Generic Discovery Engine — Protocol-v11 Final Specification

> **Derivation gate: CLOSED — REJECTED_INVALID_OBLIGATION_PACKAGE.** The v10.1 input contract failed, no source obligation is `VERIFIED`, epistemic `UNKNOWN` records remain, and four obligation conflicts are unresolved. Protocol-v11 therefore emits no normative requirements. This is a validated rejection/audit package, not a normative implementation specification.

## 1. Objective and disposition

The deterministic v11 implementation validates the complete v10.1 package before derivation. The package is rejected; no normative requirement is produced.

## 2. Input contract

| Input role | Schema | Path | Hash validation |
|---|---|---|---|
| obligation_contract | 1.0 | historical-source/obligations/INPUT-CONTRACT.yaml | MATCH |
| obligation_registry | 1.0 | historical-source/obligations/OBLIGATIONS.yaml | MATCH |
| historical_properties | 1.0 | historical-source/obligations/OBLIGATIONS.yaml | MATCH |
| obligation_dependencies | 1.0 | historical-source/obligations/OBLIGATION-DEPENDENCIES.yaml | MATCH |
| obligation_lineage | 1.0 | historical-source/obligations/OBLIGATION-LINEAGE.yaml | MATCH |
| obligation_conflicts | 1.0 | historical-source/obligations/OBLIGATION-CONFLICTS.yaml | MATCH |
| traceability | 1.0 | historical-source/obligations/TRACEABILITY-MATRIX.yaml | MATCH |
| verification_records | 1.0 | historical-source/obligations/VERIFICATION-GRAPH.yaml | MATCH |

## 3. Rejection causes

| State | Affected count | Detail |
|---|---|---|
| INPUT_MISSING | 4 | The v10.1 source package is missing required Protocol-v4 through Protocol-v7 stages. |
| INPUT_HASH_MISMATCH | 1 | The v10.1 package preserves the Protocol-v1 raw/source-range integrity failure. |
| UNVERIFIED_SOURCE | 54 | 54 obligations are not VERIFIED with verification evidence. |
| OBLIGATION_UNKNOWN | 2 | 2 obligations retain UNKNOWN epistemic or lifecycle state. |
| PROPERTY_UNKNOWN | 14 | 14 historical properties retain UNKNOWN epistemic or historical state. |
| CONFLICT_UNRESOLVED | 4 | 4 obligation conflicts remain unresolved. |

## 4. Layer separation

Evidence, historical property, rationale, obligation, requirement, rule, criterion, oracle, test, implementation, verification, and conformance remain distinct. The chain stops at obligation.

## 5. Requirement registry

`0` admitted requirements; `54` blocked/orphan source obligations. No `UNTRACED_REQUIREMENT` or `NEW_ENGINEERING_REQUIREMENT` was introduced.

## 6. Normative rules and predicates

`0` rules. The operator, predicate, and compound-logic registries are defined but uninstantiated.

## 7. Acceptance criteria and oracles

`0` criteria and `0` oracles. No mandatory requirement exists, and no oracle can substitute for one.

## 8. Dependencies, conflicts, and supersession

Requirement dependency and supersession graphs are empty. Four unresolved obligation conflicts remain blocking inputs and are not relabeled as requirement conflicts.

## 9. Coverage

All obligation-to-requirement rows are `BLOCKED`; downstream coverage dimensions remain independently `BLOCKED`.

## 10. Boundaries

No implementation boundary is assigned without a requirement. Enforcement, observation, and verification are not conflated.

## 11. Semantic narrowing/widening

Both audits are blocked because there is no admitted requirement domain. This is not a pass-by-vacuity.

## 12. Traceability

Forward and reverse traversal is preserved through source → evidence → property → obligation. No edge crosses the closed gate.

## 13. Verification and conformance

All levels remain unclaimed. A test candidate is not a passing test; an implementation is not verification; a certificate is not semantic proof.

## 14. Certificate

| Field | Value |
|---|---|
| validation_status | FAIL |
| requirements | 0 |
| orphan obligations | 54 |
| certificate hash | c0f76bcdfbd94b6cdaf98afb12f23ce13a2e9fbedad205971ba8b6380442e806 |

## 15. Remediation boundary

To open derivation, repair or replace invalid v1 evidence without rewriting it, supply and validate Protocol-v4–v7 artifacts, resolve unknown obligation/property states, execute independent verification, and explicitly resolve obligation conflicts. v11 must then be regenerated from that newly valid package.

## Final disposition

**`REJECTED_INVALID_OBLIGATION_PACKAGE` — no normative specification or implementation conformance claim is authorized.**
