# Protocol-v11 Validation

**Overall:** `STRUCTURAL_PASS_INPUT_REJECTED`
**Acceptance:** `REJECTED_INVALID_OBLIGATION_PACKAGE`
**Checks:** 157 PASS / 0 FAIL / 1 BLOCKED (158 total)

A structural pass validates the rejection path. It does not authorize requirement derivation or conformance.

| ID | Category | Result | Description | Detail |
|---|---|---|---|---|
| A01 | deliverables | PASS | required v11 deliverable exists: INPUT-CONTRACT.yaml |  |
| A02 | deliverables | PASS | required v11 deliverable exists: REQUIREMENTS.yaml |  |
| A03 | deliverables | PASS | required v11 deliverable exists: NORMATIVE-RULES.yaml |  |
| A04 | deliverables | PASS | required v11 deliverable exists: ACCEPTANCE-CRITERIA.yaml |  |
| A05 | deliverables | PASS | required v11 deliverable exists: TEST-ORACLES.yaml |  |
| A06 | deliverables | PASS | required v11 deliverable exists: REQUIREMENT-DEPENDENCIES.yaml |  |
| A07 | deliverables | PASS | required v11 deliverable exists: REQUIREMENT-CONFLICTS.yaml |  |
| A08 | deliverables | PASS | required v11 deliverable exists: REQUIREMENT-SUPERSESSION.yaml |  |
| A09 | deliverables | PASS | required v11 deliverable exists: REQUIREMENT-COVERAGE.yaml |  |
| A10 | deliverables | PASS | required v11 deliverable exists: CONFORMANCE-MATRIX.yaml |  |
| A11 | deliverables | PASS | required v11 deliverable exists: VERIFICATION-MATRIX.yaml |  |
| A12 | deliverables | PASS | required v11 deliverable exists: IMPLEMENTATION-BOUNDARIES.yaml |  |
| A13 | deliverables | PASS | required v11 deliverable exists: SEMANTIC-DIFFS.yaml |  |
| A14 | deliverables | PASS | required v11 deliverable exists: TRACEABILITY.yaml |  |
| A15 | deliverables | PASS | required v11 deliverable exists: CONFORMANCE.yaml |  |
| A16 | deliverables | PASS | required v11 deliverable exists: SPECIFICATION-CERTIFICATE.yaml |  |
| A17 | deliverables | PASS | required v11 deliverable exists: REQUIREMENTS.md |  |
| A18 | deliverables | PASS | required v11 deliverable exists: NORMATIVE-RULES.md |  |
| A19 | deliverables | PASS | required v11 deliverable exists: ACCEPTANCE-CRITERIA.md |  |
| A20 | deliverables | PASS | required v11 deliverable exists: TEST-ORACLES.md |  |
| A21 | deliverables | PASS | required v11 deliverable exists: REQUIREMENT-COVERAGE.md |  |
| A22 | deliverables | PASS | required v11 deliverable exists: REQUIREMENT-DEPENDENCIES.md |  |
| A23 | deliverables | PASS | required v11 deliverable exists: REQUIREMENT-CONFLICTS.md |  |
| A24 | deliverables | PASS | required v11 deliverable exists: CONFORMANCE-MATRIX.md |  |
| A25 | deliverables | PASS | required v11 deliverable exists: VERIFICATION-MATRIX.md |  |
| A26 | deliverables | PASS | required v11 deliverable exists: IMPLEMENTATION-BOUNDARIES.md |  |
| A27 | deliverables | PASS | required v11 deliverable exists: SEMANTIC-DIFFS.md |  |
| A28 | deliverables | PASS | required v11 deliverable exists: TRACEABILITY.md |  |
| A29 | deliverables | PASS | required v11 deliverable exists: SPECIFICATION-AUDIT.md |  |
| A30 | deliverables | PASS | required v11 deliverable exists: FINAL-SPECIFICATION.md |  |
| A31 | deliverables | PASS | required v11 deliverable exists: schema/requirement.schema.yaml |  |
| A32 | deliverables | PASS | required v11 deliverable exists: schema/normative-rule.schema.yaml |  |
| A33 | deliverables | PASS | required v11 deliverable exists: schema/acceptance-criterion.schema.yaml |  |
| A34 | deliverables | PASS | required v11 deliverable exists: schema/test-oracle.schema.yaml |  |
| A35 | deliverables | PASS | required v11 deliverable exists: schema/requirement-dependency.schema.yaml |  |
| A36 | deliverables | PASS | required v11 deliverable exists: schema/traceability.schema.yaml |  |
| A37 | deliverables | PASS | required v11 deliverable exists: schema/specification-certificate.schema.yaml |  |
| I01 | input | PASS | all eight v10.1 input roles are present |  |
| I02 | input | PASS | every input records required identity and integrity fields |  |
| I03 | input | PASS | all selected input paths exist |  |
| I04 | input | PASS | all selected content hashes match |  |
| I05 | input | PASS | input/schema versions are v11/1.0 |  |
| I06 | input | PASS | v10.1 failed status is propagated, not repaired |  |
| I07 | input | PASS | derivation gate is closed |  |
| I08 | input | PASS | all normative input rejection states are registered |  |
| I09 | input | PASS | applicable invalid-package states are emitted |  |
| I10 | input | PASS | no unregistered rejection state is emitted |  |
| I11 | input | PASS | all obligations are correctly counted as unverified |  |
| I12 | input | PASS | UNKNOWN obligations are surfaced |  |
| I13 | input | PASS | UNKNOWN properties are surfaced |  |
| I14 | input | PASS | unresolved obligation conflicts are surfaced |  |
| I15 | input | PASS | v10.1 dependency graph remains structurally valid |  |
| I16 | input | PASS | v10.1 lineage references remain valid |  |
| I17 | input | PASS | validation order starts with failed input gate |  |
| L01 | layers | PASS | no requirement is derived from invalid input |  |
| L02 | layers | PASS | no rule substitutes for a requirement |  |
| L03 | layers | PASS | no criterion substitutes for a rule/requirement |  |
| L04 | layers | PASS | no oracle substitutes for a criterion |  |
| L05 | layers | PASS | no implementation boundary is invented |  |
| L06 | layers | PASS | no conformance claim is fabricated |  |
| L07 | layers | PASS | obligation dependencies are not copied into requirement graph |  |
| L08 | layers | PASS | obligation conflicts are not relabeled requirement conflicts |  |
| L09 | layers | PASS | requirement supersession remains independent and empty |  |
| L10 | layers | PASS | semantic narrowing/widening do not pass vacuously |  |
| L11 | layers | PASS | assumptions and exceptions are first-class machine records |  |
| L12 | layers | PASS | configuration and environment assumptions are not silently invented |  |
| R00 | registry | PASS | DEDU PLICATION is normalized to DEDUPLICATION |  |
| R01 | registry | PASS | requirement type registry is exact |  |
| R02 | registry | PASS | disposition registry is exact |  |
| R03 | registry | PASS | requirement strength registry is exact |  |
| R04 | registry | PASS | scope registry is exact |  |
| R05 | registry | PASS | epistemic registry remains independent |  |
| R06 | registry | PASS | lifecycle registry remains independent |  |
| R07 | registry | PASS | requirement dependency relation registry is exact |  |
| R08 | registry | PASS | criticality remains a separate registry |  |
| R09 | registry | PASS | conformance and verification levels remain separate |  |
| R10 | registry | PASS | forbidden equivalences are explicit |  |
| R11 | registry | PASS | all fifteen v11 pipeline invariants are enforced by the rejection gate |  |
| R12 | registry | PASS | compatibility and historical preservation modes are explicit |  |
| R13 | registry | PASS | historical preservation matrix is empty rather than fabricated |  |
| REQ-001 | machine_rules | PASS | source obligations are non-empty unless expressly new/future/design |  |
| REQ-002 | machine_rules | PASS | MANDATORY requirements have acceptance criteria |  |
| REQ-003 | machine_rules | PASS | MANDATORY behavioral/security requirements have oracles |  |
| REQ-004 | machine_rules | PASS | all obligation references resolve |  |
| REQ-005 | machine_rules | PASS | all property references resolve |  |
| REQ-006 | machine_rules | PASS | all rule references resolve |  |
| REQ-007 | machine_rules | PASS | all oracle references resolve |  |
| REQ-008 | machine_rules | PASS | dependency edges reference existing requirements |  |
| REQ-009 | machine_rules | PASS | REQUIRES self-dependency is forbidden |  |
| REQ-010 | machine_rules | PASS | REQUIRES graph is acyclic |  |
| REQ-011 | machine_rules | PASS | CONFLICTS_WITH is symmetric or explicitly directional |  |
| REQ-012 | machine_rules | PASS | SUPERSEDES identifies effective scope |  |
| REQ-013 | machine_rules | PASS | VERIFIED requirements possess verification evidence |  |
| REQ-014 | machine_rules | PASS | PROVED is not inferred solely from implementation |  |
| REQ-015 | machine_rules | PASS | historical requirements trace to source evidence |  |
| C01 | coverage | PASS | every obligation has one coverage record |  |
| C02 | coverage | PASS | all obligation coverage is blocked |  |
| C03 | coverage | PASS | all orphan obligations are reported |  |
| C04 | coverage | PASS | no orphan requirement is hidden |  |
| C05 | coverage | PASS | all six coverage dimensions remain independent |  |
| C06 | coverage | PASS | single aggregate percentage is forbidden |  |
| T01 | traceability | PASS | trace graph supports exact reverse traversal |  |
| T02 | traceability | PASS | trace graph stops at obligation |  |
| T03 | traceability | PASS | all source obligation/property nodes are retained |  |
| T04 | traceability | PASS | source/evidence provenance edges are present |  |
| V01 | verification | PASS | upstream tests remain unverified |  |
| V02 | verification | PASS | no v11 test result is fabricated |  |
| V03 | verification | PASS | harness/system failure classes remain distinct |  |
| V04 | verification | PASS | test existence is not treated as verification |  |
| V05 | verification | PASS | test harness contract defines all required dimensions without altering semantics |  |
| V06 | verification | PASS | negative and mutation testing policies remain explicit |  |
| S01 | audit | PASS | all protocol failure modes are registered |  |
| S02 | audit | PASS | detected failures are explicit |  |
| S03 | audit | PASS | validation procedure has all 15 ordered steps |  |
| S-TRACE | audit | PASS | completeness dimension is reported: TRACEABILITY_COMPLETENESS |  |
| S-SEMAN | audit | PASS | completeness dimension is reported: SEMANTIC_COMPLETENESS |  |
| S-VALID | audit | PASS | completeness dimension is reported: VALIDATION_COMPLETENESS |  |
| S-VERIF | audit | PASS | completeness dimension is reported: VERIFICATION_COMPLETENESS |  |
| S-FAILU | audit | PASS | completeness dimension is reported: FAILURE_COMPLETENESS |  |
| S-SECUR | audit | PASS | completeness dimension is reported: SECURITY_COMPLETENESS |  |
| S-COMPA | audit | PASS | completeness dimension is reported: COMPATIBILITY_COMPLETENESS |  |
| S-IMPLE | audit | PASS | completeness dimension is reported: IMPLEMENTATION_BOUNDARY_COMPLETENESS |  |
| S12 | audit | PASS | hidden assumptions are explicit |  |
| S13 | audit | PASS | future architecture is not used to repair history |  |
| CERT-01 | certificate | PASS | certificate hash is valid |  |
| CERT-02 | certificate | PASS | certificate identifies v11 and deterministic unknown timestamp |  |
| CERT-03 | certificate | PASS | certificate counts match rejected registries |  |
| CERT-04 | certificate | PASS | orphan counts are exact |  |
| CERT-05 | certificate | PASS | input hashes match input contract |  |
| CERT-06 | certificate | PASS | certificate fails rather than overclaims |  |
| CERT-07 | certificate | PASS | certificate states its limited semantics |  |
| SC01 | schemas | PASS | seven schemas are machine readable and version 1.0 |  |
| SC02 | schemas | PASS | requirement schema defines all independent axes |  |
| SC03 | schemas | PASS | requirement class is not substituted for requirement type |  |
| SC04 | schemas | PASS | dependency schema contains direction and relation |  |
| SC05 | schemas | PASS | certificate status enum is exact |  |
| SC06 | schemas | PASS | requirement schema contains complete independent-axis model |  |
| SC07 | schemas | PASS | conformance criticality and verification level enums are independent |  |
| M01 | reports | PASS | report carries rejection disposition: REQUIREMENTS.md |  |
| M02 | reports | PASS | report carries rejection disposition: NORMATIVE-RULES.md |  |
| M03 | reports | PASS | report carries rejection disposition: ACCEPTANCE-CRITERIA.md |  |
| M04 | reports | PASS | report carries rejection disposition: TEST-ORACLES.md |  |
| M05 | reports | PASS | report carries rejection disposition: REQUIREMENT-COVERAGE.md |  |
| M06 | reports | PASS | report carries rejection disposition: REQUIREMENT-DEPENDENCIES.md |  |
| M07 | reports | PASS | report carries rejection disposition: REQUIREMENT-CONFLICTS.md |  |
| M08 | reports | PASS | report carries rejection disposition: CONFORMANCE-MATRIX.md |  |
| M09 | reports | PASS | report carries rejection disposition: VERIFICATION-MATRIX.md |  |
| M10 | reports | PASS | report carries rejection disposition: IMPLEMENTATION-BOUNDARIES.md |  |
| M11 | reports | PASS | report carries rejection disposition: SEMANTIC-DIFFS.md |  |
| M12 | reports | PASS | report carries rejection disposition: TRACEABILITY.md |  |
| M13 | reports | PASS | report carries rejection disposition: SPECIFICATION-AUDIT.md |  |
| M14 | reports | PASS | report carries rejection disposition: FINAL-SPECIFICATION.md |  |
| H01 | hygiene | PASS | all YAML artifacts parse as JSON-compatible YAML |  |
| H02 | hygiene | PASS | authoritative documents are not generator outputs |  |
| H03 | hygiene | PASS | no Python cache artifacts exist |  |
| H04 | hygiene | PASS | all generator-owned outputs reproduce byte-for-byte |  |
| H05 | hygiene | PASS | generator and validator are represented in deterministic source control |  |
| GATE-V11 | acceptance | BLOCKED | v11 normative specification acceptance | The complete v10.1 input package is rejected: upstream input failed, obligations are unverified, unknowns remain, and conflicts are unresolved. |
