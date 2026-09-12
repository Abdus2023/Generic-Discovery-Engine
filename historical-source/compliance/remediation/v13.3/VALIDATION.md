# Protocol-v13.3 Independent Executable Validation

**Overall:** `STRUCTURAL_PASS_AUDIT_BLOCKED`
**Acceptance:** `BLOCKED`
**Checks:** 139 PASS / 0 FAIL / 1 BLOCKED (140 total)

Executable protocol validity does not bypass the upstream invalid-specification boundary or create an aggregate/certificate claim.

| ID | Category | Result | Description | Detail |
|---|---|---|---|---|
| F01 | artifacts | PASS | v13.3 artifact exists: NORMATIVE-VOCABULARY.yaml |  |
| F02 | artifacts | PASS | v13.3 artifact exists: STATE-DOMAINS.yaml |  |
| F03 | artifacts | PASS | v13.3 artifact exists: TRANSITION-VALIDATION-PREDICATES.yaml |  |
| F04 | artifacts | PASS | v13.3 artifact exists: FINDING-TRANSITION-TABLE.yaml |  |
| F05 | artifacts | PASS | v13.3 artifact exists: REMEDIATION-TRANSITION-TABLE.yaml |  |
| F06 | artifacts | PASS | v13.3 artifact exists: PROGRAM-TRANSITION-TABLE.yaml |  |
| F07 | artifacts | PASS | v13.3 artifact exists: TRANSITION-GUARDS.yaml |  |
| F08 | artifacts | PASS | v13.3 artifact exists: BASELINE-IMPORT-POLICY.yaml |  |
| F09 | artifacts | PASS | v13.3 artifact exists: STATE-HISTORIES.yaml |  |
| F10 | artifacts | PASS | v13.3 artifact exists: TRANSITION-GUARD-CONTEXTS.yaml |  |
| F11 | artifacts | PASS | v13.3 artifact exists: TRANSITION-VALIDATIONS.yaml |  |
| F12 | artifacts | PASS | v13.3 artifact exists: CURRENT-STATES.yaml |  |
| F13 | artifacts | PASS | v13.3 artifact exists: HISTORY-INTEGRITY-FAILURES.yaml |  |
| F14 | artifacts | PASS | v13.3 artifact exists: HISTORY-VALIDATION-TEST-VECTORS.yaml |  |
| F15 | artifacts | PASS | v13.3 artifact exists: TRANSITION-VALIDATION-TEST-VECTORS.yaml |  |
| F16 | artifacts | PASS | v13.3 artifact exists: DECISION-PROJECTION-RULES.yaml |  |
| F17 | artifacts | PASS | v13.3 artifact exists: COMPLIANCE-DECISION-HISTORIES.yaml |  |
| F18 | artifacts | PASS | v13.3 artifact exists: CURRENT-DECISIONS.yaml |  |
| F19 | artifacts | PASS | v13.3 artifact exists: DECISION-PROJECTION-TEST-VECTORS.yaml |  |
| F20 | artifacts | PASS | v13.3 artifact exists: WAIVER-RESOLUTION-RULES.yaml |  |
| F21 | artifacts | PASS | v13.3 artifact exists: WAIVERS-V133.yaml |  |
| F22 | artifacts | PASS | v13.3 artifact exists: WAIVER-RESOLUTIONS.yaml |  |
| F23 | artifacts | PASS | v13.3 artifact exists: WAIVER-TEST-VECTORS.yaml |  |
| F24 | artifacts | PASS | v13.3 artifact exists: AGGREGATE-FUNCTION.yaml |  |
| F25 | artifacts | PASS | v13.3 artifact exists: AGGREGATE-INVARIANTS.yaml |  |
| F26 | artifacts | PASS | v13.3 artifact exists: AGGREGATE-TEST-VECTORS.yaml |  |
| F27 | artifacts | PASS | v13.3 artifact exists: CONFORMANCE-SEPARATION-TEST-VECTORS.yaml |  |
| F28 | artifacts | PASS | v13.3 artifact exists: DETERMINISM-PURITY-TEST-VECTORS.yaml |  |
| F29 | artifacts | PASS | v13.3 artifact exists: PROGRAM-DERIVATION-FUNCTION.yaml |  |
| F30 | artifacts | PASS | v13.3 artifact exists: PROGRAM-DERIVATIONS.yaml |  |
| F31 | artifacts | PASS | v13.3 artifact exists: PROGRAM-DERIVATION-TEST-VECTORS.yaml |  |
| F32 | artifacts | PASS | v13.3 artifact exists: AUDIT-SNAPSHOT.yaml |  |
| F33 | artifacts | PASS | v13.3 artifact exists: VALIDATION-PIPELINE.yaml |  |
| F34 | artifacts | PASS | v13.3 artifact exists: FAILURE-BOUNDARIES.yaml |  |
| F35 | artifacts | PASS | v13.3 artifact exists: CURRENT-PIPELINE-EXECUTION.yaml |  |
| F36 | artifacts | PASS | v13.3 artifact exists: CURRENT-AGGREGATE.yaml |  |
| F37 | artifacts | PASS | v13.3 artifact exists: CURRENT-AUDIT-STATUS.yaml |  |
| F38 | artifacts | PASS | v13.3 artifact exists: CERTIFICATE-STATUS.yaml |  |
| F39 | artifacts | PASS | v13.3 artifact exists: COMPLETE-TRANSFORMATION.yaml |  |
| F40 | artifacts | PASS | v13.3 artifact exists: AXIS-SEPARATION.yaml |  |
| F41 | artifacts | PASS | v13.3 artifact exists: OBJECT-REGISTRY.yaml |  |
| F42 | artifacts | PASS | v13.3 artifact exists: SCHEMA-REGISTRY.yaml |  |
| F43 | artifacts | PASS | v13.3 artifact exists: PRIOR-INTEGRITY.yaml |  |
| F44 | artifacts | PASS | v13.3 artifact exists: VALIDATION-REPORT.yaml |  |
| F45 | artifacts | PASS | v13.3 artifact exists: schema/finding-state.schema.yaml |  |
| F46 | artifacts | PASS | v13.3 artifact exists: schema/remediation-state.schema.yaml |  |
| F47 | artifacts | PASS | v13.3 artifact exists: schema/program-state.schema.yaml |  |
| F48 | artifacts | PASS | v13.3 artifact exists: schema/conformance-state.schema.yaml |  |
| F49 | artifacts | PASS | v13.3 artifact exists: schema/state-transition.schema.yaml |  |
| F50 | artifacts | PASS | v13.3 artifact exists: schema/transition-guard-context.schema.yaml |  |
| F51 | artifacts | PASS | v13.3 artifact exists: schema/transition-validation.schema.yaml |  |
| F52 | artifacts | PASS | v13.3 artifact exists: schema/history-integrity-failure.schema.yaml |  |
| F53 | artifacts | PASS | v13.3 artifact exists: schema/current-state.schema.yaml |  |
| F54 | artifacts | PASS | v13.3 artifact exists: schema/state-history.schema.yaml |  |
| F55 | artifacts | PASS | v13.3 artifact exists: schema/compliance-decision-record.schema.yaml |  |
| F56 | artifacts | PASS | v13.3 artifact exists: schema/current-decision.schema.yaml |  |
| F57 | artifacts | PASS | v13.3 artifact exists: schema/waiver-record.schema.yaml |  |
| F58 | artifacts | PASS | v13.3 artifact exists: schema/waiver-resolution.schema.yaml |  |
| F59 | artifacts | PASS | v13.3 artifact exists: schema/audit-snapshot.schema.yaml |  |
| F60 | artifacts | PASS | v13.3 artifact exists: schema/aggregate-result.schema.yaml |  |
| F61 | artifacts | PASS | v13.3 artifact exists: schema/program-derivation.schema.yaml |  |
| F62 | artifacts | PASS | v13.3 artifact exists: schema/pipeline-execution.schema.yaml |  |
| F63 | artifacts | PASS | v13.3 artifact exists: schema/audit-status.schema.yaml |  |
| F64 | artifacts | PASS | v13.3 artifact exists: reports/EXECUTABLE-STATE-REPORT.yaml |  |
| F65 | artifacts | PASS | v13.3 artifact exists: reports/AGGREGATE-CONFORMANCE-REPORT.yaml |  |
| F66 | artifacts | PASS | v13.3 artifact exists: reports/FAILURE-BOUNDARY-REPORT.yaml |  |
| F67 | artifacts | PASS | v13.3 artifact exists: reports/CERTIFICATION-IMPACT-REPORT.yaml |  |
| F68 | artifacts | PASS | generator owns exactly 67 unique deliverables |  |
| F69 | artifacts | PASS | all generated YAML is JSON-compatible |  |
| N01 | normative | PASS | MUST/MUST_NOT/SHOULD/SHOULD_NOT/MAY are defined |  |
| N02 | states | PASS | all four state vocabularies are exact |  |
| N03 | separation | PASS | truth/process/time axes cannot substitute |  |
| S01 | schemas | PASS | nineteen dedicated schemas exist |  |
| S02 | schemas | PASS | four lifecycle enum schemas are exact |  |
| S03 | schemas | PASS | transition schema matches v13.3 record and sequence begins at zero |  |
| S04 | schemas | PASS | all schema references resolve | [] |
| S05 | schemas | PASS | schema registry hashes all nineteen files |  |
| S06 | schemas | PASS | history failures have the exact nine-code vocabulary |  |
| S07 | schemas | PASS | aggregate result includes empty mandatory scope state |  |
| T01 | transition-table | PASS | finding transition matrix is exact |  |
| T02 | transition-table | PASS | remediation transition matrix is exact |  |
| T03 | transition-table | PASS | program transition matrix is exact |  |
| T04 | terminal | PASS | forbidden direct and terminal restart transitions are absent |  |
| T05 | guards | PASS | every legal transition resolves exactly one non-empty guard |  |
| T06 | guards | PASS | five program operational guards contain all specified predicates |  |
| H01 | schemas | PASS | all actual histories, transitions, currents, contexts, and validations satisfy schemas | [] |
| H02 | initial-transition | PASS | all baseline transitions use null predecessor and sequence zero |  |
| H03 | hashes | PASS | all event/current/history/context/validation hashes validate |  |
| H04 | validation | PASS | all eleven transition predicates are true for all six current events |  |
| H05 | projection | PASS | three findings project OPEN and three programs project CREATED |  |
| H06 | failure-objects | PASS | no current malformed history or fabricated failure exists |  |
| H07 | test-vectors | PASS | all ten history vectors reproduce with exact failure boundaries | [] |
| H07A | failure-schema | PASS | every invalid vector emits a schema-valid HistoryIntegrityFailure | [] |
| H08 | test-vectors | PASS | all twelve transition conjunction vectors execute independently | [] |
| H09 | non-invention | PASS | baseline policy claims no predecessor chronology |  |
| D01 | decision | PASS | snapshot mismatch and invalid-latest outcomes are explicit |  |
| D02 | test-vectors | PASS | all seven decision vectors reproduce, including temporal contamination | [] |
| D03 | schemas | PASS | synthetic decision records and projections exercise both decision schemas | [] |
| D04 | current | PASS | invalid current scope produces no fabricated decision |  |
| D05 | temporal | PASS | superseding decision preserves predecessor in test history |  |
| W01 | waiver | PASS | waiver resolver uses only declared snapshot/as-of inputs and cannot mutate decisions |  |
| W02 | test-vectors | PASS | all five waiver vectors reproduce independently | [] |
| W03 | schemas | PASS | all synthetic waiver records satisfy their schema | [] |
| W04 | current | PASS | current package invents no waiver or waiver resolution |  |
| A01 | aggregate | PASS | one pure normative aggregate function has no hidden inputs |  |
| A02 | aggregate | PASS | aggregate input excludes finding/remediation/program lifecycle state |  |
| A03 | test-vectors | PASS | all twelve canonical aggregate vectors reproduce independently | [] |
| A03A | schemas | PASS | all synthetic aggregate results validate with canonical hashes | [] |
| A04 | precedence | PASS | failure dominates blocker; blocker dominates waiver and unresolved |  |
| A05 | empty-scope | PASS | all-N/A and empty scope are NO_MANDATORY_REQUIREMENTS |  |
| A06 | optional | PASS | optional failure is reported but does not change compliance |  |
| A07 | invariants | PASS | all fifteen aggregate invariants are machine checked |  |
| A08 | separation | PASS | all four lifecycle/conformance/history independence vectors pass |  |
| A09 | purity | PASS | four reordered executions produce identical aggregate and counts |  |
| P01 | program | PASS | program derives from history, member states, and predicates with exact precedence |  |
| P02 | test-vectors | PASS | all ten program derivation vectors reproduce independently | [] |
| P03 | multi-member | PASS | two complete plus one blocked remediation derives BLOCKED |  |
| P04 | current | PASS | three no-member programs reproducibly remain CREATED | [] |
| B01 | pipeline | PASS | all seventeen ordered validation stages are present |  |
| B02 | boundaries | PASS | seven failure boundaries preserve attribution |  |
| B03 | schemas | PASS | snapshot, pipeline execution, and audit status validate | [] |
| B04 | pipeline | PASS | current audit stops at specification validation before aggregate |  |
| B05 | aggregate-boundary | PASS | no aggregate is assigned after upstream specification failure |  |
| B06 | audit-status | PASS | audit status is BLOCKED without an aggregate or certification eligibility |  |
| B07 | hashes | PASS | snapshot, pipeline, and audit status hashes validate |  |
| B08 | certificate | PASS | certificate revision remains unauthorized with exact predecessor lineage |  |
| X01 | transformation | PASS | truth and lifecycle chains remain explicitly parallel |  |
| X02 | axes | PASS | truth/process/time axes and strongest invariants are exact |  |
| X03 | registry | PASS | all thirty-six v13.3 normative object IDs are unique |  |
| X04 | registry | PASS | v13.3 IDs are globally unique from predecessors |  |
| X05 | references | PASS | all four predecessor registries resolve with exact hashes |  |
| X06 | report | PASS | generated validation report preserves blocked boundary and no aggregate |  |
| X07 | reports | PASS | all four reports preserve state, aggregate, boundary, and certificate separation |  |
| R01 | append-only | PASS | all 219 predecessor compliance artifacts remain byte-identical | [] |
| R02 | append-only | PASS | v13.2 builder refuses to erase v13.3 extension |  |
| Q01 | determinism | PASS | all 67 generator outputs reproduce byte-for-byte |  |
| Q02 | regression | PASS | v10.1 through v13.2 regressions and all append guards pass |  |
| Q03 | hygiene | PASS | no Python caches exist |  |
| Q04 | tools | PASS | generic and pinned v13.3 tools exist |  |
| GATE-V133 | acceptance | BLOCKED | current audit certification | The executable protocol validates, but current specification validation fails at stage 2; aggregate execution is correctly suppressed, audit status is BLOCKED, and certificate revision is unauthorized. |
