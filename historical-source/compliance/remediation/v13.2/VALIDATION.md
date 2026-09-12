# Protocol-v13.2 Independent Validation

**Overall:** `STRUCTURAL_PASS_AUDIT_BLOCKED`
**Acceptance:** `BLOCKED`
**Checks:** 117 PASS / 0 FAIL / 1 BLOCKED (118 total)

Valid history/projection architecture does not alter the blocked requirement and certification truth state.

| ID | Category | Result | Description | Detail |
|---|---|---|---|---|
| F01 | artifacts | PASS | v13.2 artifact exists: STATE-DOMAIN-SEPARATION.yaml |  |
| F02 | artifacts | PASS | v13.2 artifact exists: BASELINE-IMPORT-POLICY.yaml |  |
| F03 | artifacts | PASS | v13.2 artifact exists: STATE-TRANSITION-MODEL.yaml |  |
| F04 | artifacts | PASS | v13.2 artifact exists: CURRENT-STATE-PROJECTION.yaml |  |
| F05 | artifacts | PASS | v13.2 artifact exists: STATE-HISTORIES.yaml |  |
| F06 | artifacts | PASS | v13.2 artifact exists: STATE-TRANSITION-REGISTRY.yaml |  |
| F07 | artifacts | PASS | v13.2 artifact exists: CURRENT-STATES.yaml |  |
| F08 | artifacts | PASS | v13.2 artifact exists: STATE-PROJECTION-TEST-VECTORS.yaml |  |
| F09 | artifacts | PASS | v13.2 artifact exists: DECISION-HISTORY-MODEL.yaml |  |
| F10 | artifacts | PASS | v13.2 artifact exists: COMPLIANCE-DECISION-HISTORIES.yaml |  |
| F11 | artifacts | PASS | v13.2 artifact exists: CURRENT-REQUIREMENT-DECISIONS.yaml |  |
| F12 | artifacts | PASS | v13.2 artifact exists: DECISION-PROJECTION-TEST-VECTORS.yaml |  |
| F13 | artifacts | PASS | v13.2 artifact exists: AGGREGATE-FUNCTION.yaml |  |
| F14 | artifacts | PASS | v13.2 artifact exists: AGGREGATE-TEST-VECTORS.yaml |  |
| F15 | artifacts | PASS | v13.2 artifact exists: AUDIT-SNAPSHOT.yaml |  |
| F16 | artifacts | PASS | v13.2 artifact exists: CURRENT-AGGREGATE.yaml |  |
| F17 | artifacts | PASS | v13.2 artifact exists: AUDIT-STATUS.yaml |  |
| F18 | artifacts | PASS | v13.2 artifact exists: AUDIT-INTEGRITY.yaml |  |
| F19 | artifacts | PASS | v13.2 artifact exists: PROGRAM-STATE-MACHINE.yaml |  |
| F20 | artifacts | PASS | v13.2 artifact exists: PROGRAM-DERIVATION-FUNCTION.yaml |  |
| F21 | artifacts | PASS | v13.2 artifact exists: PROGRAM-DERIVATIONS.yaml |  |
| F22 | artifacts | PASS | v13.2 artifact exists: PROGRAM-TEST-VECTORS.yaml |  |
| F23 | artifacts | PASS | v13.2 artifact exists: TEMPORAL-QUERY-RULES.yaml |  |
| F24 | artifacts | PASS | v13.2 artifact exists: CANONICAL-MODEL.yaml |  |
| F25 | artifacts | PASS | v13.2 artifact exists: CERTIFICATE-POLICY.yaml |  |
| F26 | artifacts | PASS | v13.2 artifact exists: CERTIFICATE-REVISION-STATUS.yaml |  |
| F27 | artifacts | PASS | v13.2 artifact exists: INVARIANTS.yaml |  |
| F28 | artifacts | PASS | v13.2 artifact exists: OBJECT-REGISTRY.yaml |  |
| F29 | artifacts | PASS | v13.2 artifact exists: SCHEMA-REGISTRY.yaml |  |
| F30 | artifacts | PASS | v13.2 artifact exists: VALIDATION-REPORT.yaml |  |
| F31 | artifacts | PASS | v13.2 artifact exists: PRIOR-INTEGRITY.yaml |  |
| F32 | artifacts | PASS | v13.2 artifact exists: schema/state-transition.schema.yaml |  |
| F33 | artifacts | PASS | v13.2 artifact exists: schema/current-state.schema.yaml |  |
| F34 | artifacts | PASS | v13.2 artifact exists: schema/state-history.schema.yaml |  |
| F35 | artifacts | PASS | v13.2 artifact exists: schema/compliance-decision-record.schema.yaml |  |
| F36 | artifacts | PASS | v13.2 artifact exists: schema/current-requirement-decision.schema.yaml |  |
| F37 | artifacts | PASS | v13.2 artifact exists: schema/audit-snapshot.schema.yaml |  |
| F38 | artifacts | PASS | v13.2 artifact exists: schema/audit-aggregate.schema.yaml |  |
| F39 | artifacts | PASS | v13.2 artifact exists: schema/program-state-derivation.schema.yaml |  |
| F40 | artifacts | PASS | v13.2 artifact exists: schema/audit-status.schema.yaml |  |
| F41 | artifacts | PASS | v13.2 artifact exists: reports/CURRENT-STATE-REPORT.yaml |  |
| F42 | artifacts | PASS | v13.2 artifact exists: reports/AGGREGATE-CONFORMANCE-REPORT.yaml |  |
| F43 | artifacts | PASS | v13.2 artifact exists: reports/TEMPORAL-INTEGRITY-REPORT.yaml |  |
| F44 | artifacts | PASS | v13.2 artifact exists: reports/CERTIFICATION-IMPACT-REPORT.yaml |  |
| F45 | artifacts | PASS | generator owns exactly 44 unique v13.2 deliverables |  |
| F46 | artifacts | PASS | all generated YAML is JSON-compatible |  |
| S01 | schemas | PASS | nine dedicated v13.2 schemas are complete |  |
| S02 | schemas | PASS | all schema references resolve | [] |
| S03 | schemas | PASS | transition schema requires immutable identity, sequence, evidence, and hash |  |
| S04 | schemas | PASS | current state schema is projection-specific |  |
| S05 | schemas | PASS | invalid history can carry null current projection |  |
| S06 | schemas | PASS | decision history schema preserves snapshots and supersession |  |
| S07 | schemas | PASS | aggregate schema includes explicit empty-mandatory result |  |
| S08 | schemas | PASS | schema registry hashes all nine schemas |  |
| H01 | history | PASS | all six state histories validate against dedicated schemas | {} |
| H02 | projection | PASS | all six current states independently reproject exactly | [] |
| H03 | history | PASS | history integrity and hashes validate |  |
| H04 | events | PASS | all six baseline events have immutable hashes and contiguous genesis sequence |  |
| H05 | non-invention | PASS | baseline imports explicitly avoid reconstructing unavailable history |  |
| H06 | derived-views | PASS | event registry is an exact reproducible history view |  |
| H07 | derived-views | PASS | current-state registry is an exact reproducible projection |  |
| H08 | projection | PASS | finding and program current states remain separately OPEN and CREATED |  |
| H09 | references | PASS | all baseline evidence references resolve exactly once with matching subject type |  |
| H10 | validation-order | PASS | all twelve projection validation stages and no-skip failure behavior are explicit |  |
| H11 | test-vectors | PASS | all twelve history projection vectors reproduce independently | [] |
| H12 | terminal | PASS | completed-to-active history is rejected |  |
| H13 | block-return | PASS | block return accepts only the previous operational state |  |
| D01 | decision-history | PASS | new decision triggers and immutable supersession semantics are exact |  |
| D02 | decision-projection | PASS | projection key includes audit, requirement, specification, and implementation |  |
| D03 | decision-projection | PASS | invalid latest decision cannot silently fall back |  |
| D04 | test-vectors | PASS | all six decision projection vectors reproduce independently | [] |
| D05 | schemas | PASS | synthetic decision records and valid current projections exercise both schemas | [] |
| D06 | decision-history | PASS | current package invents no requirement decisions |  |
| A01 | aggregate | PASS | canonical precedence is failure, blocked, unresolved, waiver, pass, empty |  |
| A02 | aggregate | PASS | aggregate excludes lifecycle process states |  |
| A03 | optional | PASS | optional results are separately reported and cannot alter mandatory aggregate |  |
| A04 | test-vectors | PASS | all twelve aggregate vectors reproduce independently | [] |
| A05 | precedence | PASS | proven failure dominates blockers |  |
| A06 | precedence | PASS | blocked dominates unresolved |  |
| A07 | precedence | PASS | unresolved dominates waived failure |  |
| A08 | waiver | PASS | waived-only mandatory violation is conditional |  |
| A09 | empty-set | PASS | valid empty/all-excluded/optional-only mandatory sets are not compliant |  |
| A10 | integrity | PASS | integrity failure blocks empty-set evaluation |  |
| A11 | optional | PASS | optional failure with mandatory pass remains compliant |  |
| N01 | snapshot | PASS | audit snapshot validates and hash matches |  |
| N02 | snapshot | PASS | snapshot components and typed audit reference match exact immutable inputs |  |
| N03 | current-aggregate | PASS | current aggregate independently recomputes BLOCKED |  |
| N04 | current-aggregate | PASS | empty mandatory state is explicit without manufacturing compliance |  |
| N05 | current-aggregate | PASS | aggregate validates, identifies snapshot, and has canonical hash |  |
| N06 | integrity | PASS | H/D/R/T/S/E predicates block at invalid specification prerequisite |  |
| N07 | audit-status | PASS | audit status derives from snapshot aggregate and remains uncertifiable |  |
| P01 | program-state | PASS | all ten program states have exact definitions |  |
| P02 | program-state | PASS | canonical operational chain is guarded |  |
| P03 | program-state | PASS | block and return rules cover every operational state |  |
| P04 | program-state | PASS | completed is terminal and cannot return active |  |
| P05 | separation | PASS | program machine has no conformance effect |  |
| P06 | program-derivation | PASS | program predicate precedence is exact and resolves EVALUATING before ACTIVE |  |
| P07 | program-derivation | PASS | three referenced zero-member programs independently derive CREATED | [] |
| P08 | test-vectors | PASS | all ten program derivation vectors reproduce independently | [] |
| T01 | temporal | PASS | five temporal query classes are supported without wall-clock dependence |  |
| T02 | temporal | PASS | baseline temporal queries distinguish before-lineage from current state |  |
| T03 | separation | PASS | canonical flow is forward-only through certificate |  |
| C01 | certificate | PASS | certificate policy requires snapshot scope and immutable lineage |  |
| C02 | certificate | PASS | no certificate revision is authorized |  |
| I01 | invariants | PASS | all twenty canonical v13.2 invariants are mechanically enumerated |  |
| I02 | identities | PASS | all twenty-four v13.2 normative IDs are unique and valid |  |
| I03 | registry | PASS | object registry contains all and only canonical v13.2 objects |  |
| I04 | identities | PASS | v13.2 normative IDs are globally unique against predecessor registries |  |
| I05 | references | PASS | all three predecessor registry hashes resolve exactly |  |
| I06 | validation | PASS | generated report preserves structural pass and blocked audit |  |
| R01 | append-only | PASS | all 169 predecessor compliance artifacts remain byte-identical | [] |
| R02 | append-only | PASS | v13.1 builder contains future-extension refusal |  |
| R03 | reports | PASS | four reports preserve current states, temporal integrity, aggregate, and certification separation |  |
| Q01 | determinism | PASS | all 44 generator-owned outputs reproduce byte-for-byte |  |
| Q02 | regression | PASS | v10.1 through v13.1 regressions and append-only guards pass |  |
| Q03 | hygiene | PASS | no Python cache artifacts exist |  |
| Q04 | tools | PASS | generic and pinned v13.2 tools exist |  |
| GATE-V132 | acceptance | BLOCKED | current audit/certification decision | History and projection structures validate, but invalid normative scope and missing implementation/evidence prerequisites keep the current audit BLOCKED and prohibit certificate revision. |
