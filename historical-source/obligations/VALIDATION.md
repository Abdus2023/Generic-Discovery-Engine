# Protocol-v10.1 Validation

**Overall:** `STRUCTURAL_PASS_INPUT_BLOCKED`
**Acceptance:** `INPUT_CONTRACT_FAILED`
**Checks:** 143 PASS / 0 FAIL / 1 BLOCKED (144 total)

Q01 is intentionally blocked by the actual upstream package; structural success does not convert missing or invalid inputs into acceptance.

| ID | Category | Result | Description | Detail |
|---|---|---|---|---|
| A01 | deliverables | PASS | required deliverable exists: README.md |  |
| A02 | deliverables | PASS | required deliverable exists: INPUT-CONTRACT.yaml |  |
| A03 | deliverables | PASS | required deliverable exists: OBLIGATIONS.yaml |  |
| A04 | deliverables | PASS | required deliverable exists: OBLIGATION-DEPENDENCIES.yaml |  |
| A05 | deliverables | PASS | required deliverable exists: OBLIGATION-DEPENDENCY-MATRIX.yaml |  |
| A06 | deliverables | PASS | required deliverable exists: DEPENDENCY-CLOSURE.md |  |
| A07 | deliverables | PASS | required deliverable exists: DEPENDENCY-CRITICAL-OBLIGATIONS.yaml |  |
| A08 | deliverables | PASS | required deliverable exists: EVIDENCE-GRAPH.yaml |  |
| A09 | deliverables | PASS | required deliverable exists: HISTORICAL-OBLIGATION-GRAPH.yaml |  |
| A10 | deliverables | PASS | required deliverable exists: FUTURE-ENGINEERING-OBLIGATION-GRAPH.yaml |  |
| A11 | deliverables | PASS | required deliverable exists: VERIFICATION-GRAPH.yaml |  |
| A12 | deliverables | PASS | required deliverable exists: OBLIGATION-LINEAGE.yaml |  |
| A13 | deliverables | PASS | required deliverable exists: OBLIGATION-LINEAGE-GRAPH.md |  |
| A14 | deliverables | PASS | required deliverable exists: OBLIGATION-CONFLICTS.yaml |  |
| A15 | deliverables | PASS | required deliverable exists: FAILURE-OBLIGATIONS.yaml |  |
| A16 | deliverables | PASS | required deliverable exists: SECURITY-OBLIGATIONS.yaml |  |
| A17 | deliverables | PASS | required deliverable exists: CONTRACT-OBLIGATIONS.yaml |  |
| A18 | deliverables | PASS | required deliverable exists: NULLABILITY-COMPATIBILITY.yaml |  |
| A19 | deliverables | PASS | required deliverable exists: HISTORICAL-API-SURFACE.yaml |  |
| A20 | deliverables | PASS | required deliverable exists: TRACEABILITY-MATRIX.yaml |  |
| A21 | deliverables | PASS | required deliverable exists: HISTORICAL-REGRESSION-SUITE.md |  |
| A22 | deliverables | PASS | required deliverable exists: COMPATIBILITY-ENVELOPE.md |  |
| A23 | deliverables | PASS | required deliverable exists: ESSENTIAL-VS-ACCIDENTAL.md |  |
| A24 | deliverables | PASS | required deliverable exists: MIGRATION-OBLIGATIONS.md |  |
| A25 | deliverables | PASS | required deliverable exists: OBLIGATION-CONFLICTS.md |  |
| A26 | deliverables | PASS | required deliverable exists: OBLIGATION-GRAPH.md |  |
| A27 | deliverables | PASS | required deliverable exists: ENGINEERING-OBLIGATION-REPORT.md |  |
| A28 | deliverables | PASS | required deliverable exists: schema/input-contract.schema.yaml |  |
| A29 | deliverables | PASS | required deliverable exists: schema/historical-property.schema.yaml |  |
| A30 | deliverables | PASS | required deliverable exists: schema/obligation.schema.yaml |  |
| A31 | deliverables | PASS | required deliverable exists: schema/obligation-dependency.schema.yaml |  |
| A32 | deliverables | PASS | required deliverable exists: schema/obligation-lineage.schema.yaml |  |
| A33 | deliverables | PASS | required deliverable exists: schema/obligation-conflict.schema.yaml |  |
| A34 | deliverables | PASS | required deliverable exists: schema/traceability.schema.yaml |  |
| I00 | input | PASS | input contract and obligation schema versions are 1.0 |  |
| I01 | input | PASS | all nine required input kinds are represented |  |
| I02 | input | PASS | schemas are checked and missing schema inputs remain blocked |  |
| I03 | input | PASS | content hashes and v1 mismatch are distinguished |  |
| I04 | input | PASS | version consistency gate is blocked, not falsely passed |  |
| I05 | input | PASS | provenance references structurally resolve |  |
| I06 | input | PASS | normalized evidence epistemic labels are valid |  |
| I07 | input | PASS | contradictions are preserved |  |
| I08 | input | PASS | unknowns are preserved |  |
| I09 | input | PASS | missing v4 reconstruction verification fails explicitly |  |
| I10 | input | PASS | temporal isolation gate is explicit |  |
| I11 | input | PASS | v4-v7 remain missing, not synthesized |  |
| I12 | input | PASS | overall failed status and downgrade authorization are explicit |  |
| I13 | input | PASS | missing evidence is not evidence of absence |  |
| I14 | input | PASS | every failure state belongs to normative registry |  |
| I15 | input | PASS | normalization envelope has exact core fields |  |
| I16 | input | PASS | derivation declares normalized-evidence-only consumption |  |
| I17 | input | PASS | direct mandatory-source rejection policy is present |  |
| I18 | input | PASS | normalized content hashes bind existing source paths |  |
| I19 | input | PASS | normalized evidence uses only accepted evidence classes |  |
| P01 | properties | PASS | facts remain distinct from properties and obligations |  |
| P02 | properties | PASS | all properties use prescribed uppercase property types |  |
| P03 | properties | PASS | all properties include minimum v10.1 model fields |  |
| P04 | properties | PASS | every property resolves normalized evidence |  |
| P05 | properties | PASS | property is not automatically a requirement |  |
| P06 | properties | PASS | state properties preserve epistemic labels |  |
| O01 | obligations | PASS | every obligation includes the minimum schema |  |
| O02 | obligations | PASS | class enum excludes UNKNOWN |  |
| O03 | obligations | PASS | strength, category, epistemic, and lifecycle enums are independent and valid |  |
| O04 | obligations | PASS | obligation IDs are unique |  |
| O05 | obligations | PASS | all source properties/evidence resolve |  |
| O06 | obligations | PASS | all obligations expose version scope |  |
| O07 | obligations | PASS | no obligation is marked VERIFIED or IMPLEMENTED |  |
| O08 | obligations | PASS | verified status is distinct from implementation and test result |  |
| O09 | obligations | PASS | classes, strengths and categories are not mechanically identical |  |
| O10 | obligations | PASS | historical defects are explicitly rejected |  |
| O11 | obligations | PASS | future strengthenings remain labeled |  |
| O12 | obligations | PASS | requirements retain source-local blocked acceptance |  |
| O13 | obligations | PASS | one invariant and test resolves for every obligation |  |
| O14 | obligations | PASS | priority basis is risk-based rather than chronological |  |
| V02 | dependencies | PASS | dependency direction and relation are valid |  |
| V03 | dependencies | PASS | every dependency has semantic justification and provenance |  |
| V04 | dependencies | PASS | verification edges resolve actual test evidence without false verification |  |
| V05 | dependencies | PASS | REQUIRES cycles are detected and none are silently linearized |  |
| V06 | dependencies | PASS | every REQUIRED obligation exposes complete dependency closure |  |
| V07 | dependencies | PASS | no obligation is VERIFIED while required dependencies are unverified |  |
| V08 | dependencies | PASS | centrality and change impact cover every obligation |  |
| V09 | dependencies | PASS | topological verification order puts REQUIRES targets first |  |
| V10 | dependencies | PASS | failure propagation reaches dependent tests |  |
| V11 | dependencies | PASS | historical and future dependency types are explicit |  |
| V12 | dependencies | PASS | conflicts do not enter dependency graph |  |
| V13 | dependencies | PASS | lineage and supersession remain separate |  |
| V14 | dependencies | PASS | matrix covers all obligation pairs |  |
| V15 | dependencies | PASS | dependency IDs resolve in obligation adjacency |  |
| V16 | dependencies | PASS | required closures are blocked rather than falsely verified |  |
| V17 | dependencies | PASS | dependency layers do not place dependents below prerequisites |  |
| G01 | graphs | PASS | evidence graph is distinct and typed |  |
| G02 | graphs | PASS | historical dependency graph excludes future edges |  |
| G03 | graphs | PASS | future engineering dependency graph does not relabel history |  |
| G04 | graphs | PASS | verification graph remains distinct |  |
| G05 | graphs | PASS | lineage graph has explicit version/status fields |  |
| G06 | graphs | PASS | conflict graph carries semantic differences and resolution status |  |
| G07 | graphs | PASS | dependency graph has distinct typed nodes and edges |  |
| S01 | specialized | PASS | failure classes separate obligation propagation states |  |
| S02 | specialized | PASS | security treats remote content as untrusted data |  |
| S03 | specialized | PASS | contract conclusions remain unknown under missing v7 |  |
| S04 | specialized | PASS | nullability remains unknown without v7 |  |
| S05 | specialized | PASS | API signatures do not prove semantics |  |
| S06 | specialized | PASS | traceability resolves obligations, properties and tests |  |
| S07 | specialized | PASS | traceability includes dependency and verification result |  |
| C01 | schemas | PASS | seven schemas are versioned 1.0 |  |
| C02 | schemas | PASS | obligation schema class enum excludes UNKNOWN |  |
| C03 | schemas | PASS | property schema uses required type enum |  |
| C04 | schemas | PASS | dependency schema permits normative REQUIRES |  |
| C05 | schemas | PASS | traceability schema requires dependency and verification |  |
| M01 | model | PASS | core obligation coverage is present |  |
| M02 | model | PASS | candidate identity dimensions remain independent |  |
| M03 | model | PASS | deduplication scopes remain independent |  |
| M04 | model | PASS | claim scope does not overstate thread/distributed atomicity |  |
| M05 | model | PASS | termination remains an engineering strengthening |  |
| M06 | model | PASS | cancellation API does not imply safety |  |
| M07 | model | PASS | auditability is not inferred from logs |  |
| M08 | model | PASS | provenance visibility and integrity stay separate |  |
| M09 | model | PASS | resource findings are static risk not incidents |  |
| M10 | model | PASS | future mechanisms remain unselected |  |
| M11 | model | PASS | no externally visible API is invented |  |
| M12 | model | PASS | historical parse defect is not future behavior |  |
| M13 | model | PASS | provider ordering uncertainty remains explicit |  |
| M14 | model | PASS | v7 gate is required without inventing contract conclusions |  |
| Q01 | quality | BLOCKED | all required inputs exist, are valid, verified and temporally clean | Protocol-v1 validation fails and Protocol-v4-v7 required artifacts are missing; acceptance cannot proceed. |
| Q02 | quality | PASS | every historical property traces to normalized evidence |  |
| Q03 | quality | PASS | every obligation has historical property/evidence justification |  |
| Q04 | quality | PASS | class strength category epistemic and lifecycle are separately declared |  |
| Q05 | quality | PASS | every dependency has direction, condition, reason, provenance and scope |  |
| Q06 | quality | PASS | REQUIRES graph is acyclic or cycles would be reported |  |
| Q07 | quality | PASS | every REQUIRED obligation exposes closure |  |
| Q08 | quality | PASS | dependency criticality and ordering are reproducible |  |
| Q09 | quality | PASS | dependency failure propagation is encoded |  |
| Q10 | quality | PASS | historical and future dependency models remain distinct |  |
| Q11 | quality | PASS | dependency, lineage, conflict and verification semantics remain distinct |  |
| Q12 | quality | PASS | IMPLEMENTED never implies VERIFIED |  |
| Q13 | quality | PASS | future strengthenings are explicit and not historical claims |  |
| Q14 | quality | PASS | unknowns and contradictions remain preserved |  |
| Q15 | quality | PASS | all reports carry failed-input disposition |  |
| Q16 | quality | PASS | all generator-owned outputs reproduce byte-for-byte |  |
| H01 | hygiene | PASS | authoritative documents remain outside generated corpus |  |
| H02 | hygiene | PASS | no Python cache artifacts exist |  |
| H03 | hygiene | PASS | tool hashes are current |  |
| H04 | hygiene | PASS | all machine artifacts are JSON-compatible YAML |  |
| H05 | hygiene | PASS | no rejected current/future documents enter normalized evidence |  |
