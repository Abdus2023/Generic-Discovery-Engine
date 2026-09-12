# Protocol-v11.1 Validation

**Overall:** `STRUCTURAL_PASS_INPUT_REJECTED`
**Acceptance:** `REJECTED_INVALID_OBLIGATION_PACKAGE`
**Checks:** 177 PASS / 0 FAIL / 1 BLOCKED (178 total)

Structural success validates rejection, schema completeness, and normative/non-normative separation. It does not authorize normative derivation.

| ID | Category | Result | Description | Detail |
|---|---|---|---|---|
| A01 | artifacts | PASS | required v11.1 artifact exists: INPUT-CONTRACT.yaml |  |
| A02 | artifacts | PASS | required v11.1 artifact exists: SPECIFICATION-MANIFEST.yaml |  |
| A03 | artifacts | PASS | required v11.1 artifact exists: SPECIFICATION-CERTIFICATE.yaml |  |
| A04 | artifacts | PASS | required v11.1 artifact exists: EVIDENCE-REFERENCES.yaml |  |
| A05 | artifacts | PASS | required v11.1 artifact exists: PROPERTY-REFERENCES.yaml |  |
| A06 | artifacts | PASS | required v11.1 artifact exists: OBLIGATION-REFERENCES.yaml |  |
| A07 | artifacts | PASS | required v11.1 artifact exists: REQUIREMENTS.yaml |  |
| A08 | artifacts | PASS | required v11.1 artifact exists: NORMATIVE-RULES.yaml |  |
| A09 | artifacts | PASS | required v11.1 artifact exists: CONDITIONS.yaml |  |
| A10 | artifacts | PASS | required v11.1 artifact exists: PREDICATES.yaml |  |
| A11 | artifacts | PASS | required v11.1 artifact exists: CONSTRAINTS.yaml |  |
| A12 | artifacts | PASS | required v11.1 artifact exists: GUIDANCE.yaml |  |
| A13 | artifacts | PASS | required v11.1 artifact exists: RATIONALES.yaml |  |
| A14 | artifacts | PASS | required v11.1 artifact exists: ASSUMPTIONS.yaml |  |
| A15 | artifacts | PASS | required v11.1 artifact exists: IMPLEMENTATION-NOTES.yaml |  |
| A16 | artifacts | PASS | required v11.1 artifact exists: EXAMPLES.yaml |  |
| A17 | artifacts | PASS | required v11.1 artifact exists: ACCEPTANCE-CRITERIA.yaml |  |
| A18 | artifacts | PASS | required v11.1 artifact exists: TEST-ORACLES.yaml |  |
| A19 | artifacts | PASS | required v11.1 artifact exists: INVARIANTS.yaml |  |
| A20 | artifacts | PASS | required v11.1 artifact exists: TRANSITIONS.yaml |  |
| A21 | artifacts | PASS | required v11.1 artifact exists: EFFECTS.yaml |  |
| A22 | artifacts | PASS | required v11.1 artifact exists: EXCEPTIONS.yaml |  |
| A23 | artifacts | PASS | required v11.1 artifact exists: REQUIREMENT-DEPENDENCIES.yaml |  |
| A24 | artifacts | PASS | required v11.1 artifact exists: REQUIREMENT-CONFLICTS.yaml |  |
| A25 | artifacts | PASS | required v11.1 artifact exists: REQUIREMENT-SUPERSESSION.yaml |  |
| A26 | artifacts | PASS | required v11.1 artifact exists: COMPATIBILITY.yaml |  |
| A27 | artifacts | PASS | required v11.1 artifact exists: IMPLEMENTATION-BOUNDARIES.yaml |  |
| A28 | artifacts | PASS | required v11.1 artifact exists: VERIFICATION.yaml |  |
| A29 | artifacts | PASS | required v11.1 artifact exists: TEST-RESULTS.yaml |  |
| A30 | artifacts | PASS | required v11.1 artifact exists: CONFORMANCE.yaml |  |
| A31 | artifacts | PASS | required v11.1 artifact exists: TRACEABILITY.yaml |  |
| A32 | artifacts | PASS | required v11.1 artifact exists: REPORTS/REQUIREMENTS.md |  |
| A33 | artifacts | PASS | required v11.1 artifact exists: REPORTS/NORMATIVE-RULES.md |  |
| A34 | artifacts | PASS | required v11.1 artifact exists: REPORTS/GUIDANCE.md |  |
| A35 | artifacts | PASS | required v11.1 artifact exists: REPORTS/ACCEPTANCE-CRITERIA.md |  |
| A36 | artifacts | PASS | required v11.1 artifact exists: REPORTS/TEST-ORACLES.md |  |
| A37 | artifacts | PASS | required v11.1 artifact exists: REPORTS/DEPENDENCIES.md |  |
| A38 | artifacts | PASS | required v11.1 artifact exists: REPORTS/CONFLICTS.md |  |
| A39 | artifacts | PASS | required v11.1 artifact exists: REPORTS/CONFORMANCE.md |  |
| A40 | artifacts | PASS | required v11.1 artifact exists: REPORTS/VERIFICATION.md |  |
| A41 | artifacts | PASS | required v11.1 artifact exists: REPORTS/TRACEABILITY.md |  |
| A42 | artifacts | PASS | required v11.1 artifact exists: REPORTS/SPECIFICATION-AUDIT.md |  |
| A43 | artifacts | PASS | required v11.1 artifact exists: REPORTS/FINAL-SPECIFICATION.md |  |
| A44 | artifacts | PASS | required v11.1 artifact exists: SCHEMA/specification.schema.yaml |  |
| A45 | artifacts | PASS | required v11.1 artifact exists: SCHEMA/requirement.schema.yaml |  |
| A46 | artifacts | PASS | required v11.1 artifact exists: SCHEMA/rule.schema.yaml |  |
| A47 | artifacts | PASS | required v11.1 artifact exists: SCHEMA/guidance.schema.yaml |  |
| A48 | artifacts | PASS | required v11.1 artifact exists: SCHEMA/rationale.schema.yaml |  |
| A49 | artifacts | PASS | required v11.1 artifact exists: SCHEMA/assumption.schema.yaml |  |
| A50 | artifacts | PASS | required v11.1 artifact exists: SCHEMA/implementation-note.schema.yaml |  |
| A51 | artifacts | PASS | required v11.1 artifact exists: SCHEMA/example.schema.yaml |  |
| A52 | artifacts | PASS | required v11.1 artifact exists: SCHEMA/condition.schema.yaml |  |
| A53 | artifacts | PASS | required v11.1 artifact exists: SCHEMA/predicate.schema.yaml |  |
| A54 | artifacts | PASS | required v11.1 artifact exists: SCHEMA/constraint.schema.yaml |  |
| A55 | artifacts | PASS | required v11.1 artifact exists: SCHEMA/acceptance-criterion.schema.yaml |  |
| A56 | artifacts | PASS | required v11.1 artifact exists: SCHEMA/oracle.schema.yaml |  |
| A57 | artifacts | PASS | required v11.1 artifact exists: SCHEMA/invariant.schema.yaml |  |
| A58 | artifacts | PASS | required v11.1 artifact exists: SCHEMA/transition.schema.yaml |  |
| A59 | artifacts | PASS | required v11.1 artifact exists: SCHEMA/effect.schema.yaml |  |
| A60 | artifacts | PASS | required v11.1 artifact exists: SCHEMA/exception.schema.yaml |  |
| A61 | artifacts | PASS | required v11.1 artifact exists: SCHEMA/compatibility.schema.yaml |  |
| A62 | artifacts | PASS | required v11.1 artifact exists: SCHEMA/dependency.schema.yaml |  |
| A63 | artifacts | PASS | required v11.1 artifact exists: SCHEMA/conflict.schema.yaml |  |
| A64 | artifacts | PASS | required v11.1 artifact exists: SCHEMA/supersession.schema.yaml |  |
| A65 | artifacts | PASS | required v11.1 artifact exists: SCHEMA/boundary.schema.yaml |  |
| A66 | artifacts | PASS | required v11.1 artifact exists: SCHEMA/verification.schema.yaml |  |
| A67 | artifacts | PASS | required v11.1 artifact exists: SCHEMA/test-result.schema.yaml |  |
| A68 | artifacts | PASS | required v11.1 artifact exists: SCHEMA/conformance.schema.yaml |  |
| A69 | artifacts | PASS | required v11.1 artifact exists: SCHEMA/traceability.schema.yaml |  |
| A70 | artifacts | PASS | required v11.1 artifact exists: SCHEMA/evidence.schema.yaml |  |
| A71 | artifacts | PASS | required v11.1 artifact exists: SCHEMA/property.schema.yaml |  |
| A72 | artifacts | PASS | required v11.1 artifact exists: SCHEMA/obligation.schema.yaml |  |
| A73 | artifacts | PASS | required v11.1 artifact exists: SCHEMA/certificate.schema.yaml |  |
| I01 | input | PASS | complete v10.1 role set is bound |  |
| I02 | input | PASS | all input identity/hash fields exist |  |
| I03 | input | PASS | all selected input hashes match |  |
| I04 | input | PASS | v10.1 failure is preserved |  |
| I05 | input | PASS | v11.1 gate is explicitly closed |  |
| I06 | input | PASS | all applicable rejection states are emitted |  |
| I07 | input | PASS | failure classes are valid and independently classified |  |
| I08 | input | PASS | all 54 source obligations remain unverified |  |
| I09 | input | PASS | UNKNOWN obligations are not escalated |  |
| I10 | input | PASS | UNKNOWN properties are not escalated |  |
| I11 | input | PASS | unresolved obligation conflicts remain explicit |  |
| W01 | wrappers | PASS | all evidence records are wrapped without count loss |  |
| W02 | wrappers | PASS | all properties are wrapped without count loss |  |
| W03 | wrappers | PASS | all obligations are wrapped without count loss |  |
| W04 | wrappers | PASS | wrapper object type/schema/lifecycle/provenance fields exist |  |
| W05 | wrappers | PASS | wrapper epistemic and verification status is not strengthened |  |
| W06 | wrappers | PASS | property epistemic status is byte-model equivalent |  |
| W07 | wrappers | PASS | obligation lifecycle and verification remain unverified |  |
| W08 | wrappers | PASS | all wrapper source hashes resolve |  |
| N01 | normative | PASS | all normative/downstream registries are empty under closed gate |  |
| N02 | normative | PASS | no conformance claim is made |  |
| N03 | normative | PASS | requirement type/disposition/strength axes are exact and independent |  |
| N04 | normative | PASS | DEDUPLICATION canonical spelling is used |  |
| N05 | normative | PASS | rule operators are canonical |  |
| N06 | normative | PASS | predicate and compound types remain distinct |  |
| N07 | normative | PASS | REQUIRES graph is empty and acyclic |  |
| N08 | normative | PASS | no obligation conflict is relabeled |  |
| N09 | normative | PASS | no compatibility/exact preservation claim is fabricated |  |
| N10 | normative | PASS | no implementation boundary is substituted for requirement |  |
| G01 | guidance | PASS | three explicit guidance objects are emitted |  |
| G02 | guidance | PASS | guidance type and priority values are valid |  |
| G03 | guidance | PASS | guidance is explicitly non-normative |  |
| G04 | guidance | PASS | guidance contains no normative operator |  |
| G05 | guidance | PASS | one rationale exists per obligation |  |
| G06 | guidance | PASS | rationales retain source property/evidence links |  |
| G07 | guidance | PASS | rationales remain non-normative |  |
| G08 | guidance | PASS | assumptions are explicit and independently validated |  |
| G09 | guidance | PASS | implementation notes are not used as rules |  |
| G10 | guidance | PASS | examples cannot define normative scope |  |
| G11 | guidance | PASS | all non-normative provenance hashes resolve |  |
| G12 | guidance | PASS | harness boundary is separate and non-mutating |  |
| O01 | objects | PASS | all instantiated first-class IDs are globally unique |  |
| O02 | objects | PASS | all instantiated objects have type/schema/lifecycle/provenance |  |
| O03 | objects | PASS | all rationale references resolve |  |
| O04 | objects | PASS | all guidance obligation references resolve |  |
| O05 | objects | PASS | all assumption affected references resolve or are explicitly empty |  |
| O06 | objects | PASS | no broken final mandatory reference can exist |  |
| S01 | schemas | PASS | all 30 dedicated schemas are present |  |
| S02 | schemas | PASS | every schema declares version 1.0 |  |
| S03 | schemas | PASS | required 25-schema tree is complete |  |
| S04 | schemas | PASS | constraint/evidence/property/obligation/certificate extension schemas exist |  |
| S05 | schemas | PASS | requirement schema keeps normative and supporting references separate |  |
| S06 | schemas | PASS | guidance and example schemas force non-normative classification |  |
| S07 | schemas | PASS | predicate schema supports controlled recursion |  |
| S08 | schemas | PASS | rule schema allows only canonical operators |  |
| S09 | schemas | PASS | all object schemas require identity/type/schema/lifecycle/provenance |  |
| S10 | schemas | PASS | schema changes are classified |  |
| T01 | traceability | PASS | single canonical chain is exact |  |
| T02 | traceability | PASS | trace terminates at obligation |  |
| T03 | traceability | PASS | all edge endpoints resolve |  |
| T04 | traceability | PASS | canonical forward edges use FORMALIZED_AS |  |
| T05 | traceability | PASS | supporting edges use only non-canonical attachment relations |  |
| T06 | traceability | PASS | exact reverse traversal is available |  |
| T07 | traceability | PASS | all source objects remain represented |  |
| T08 | traceability | PASS | supporting records do not extend canonical normative chain |  |
| T09 | traceability | PASS | traceability objects have complete identity and provenance |  |
| A80 | audit | PASS | audit executes all fourteen stages in order |  |
| A81 | audit | PASS | all thirteen completeness dimensions are independent |  |
| A82 | audit | PASS | all twenty final invariants pass by explicit separation/gating |  |
| A83 | audit | PASS | all specification failure classes are registered |  |
| A84 | audit | PASS | no aggregate percentage conceals blockers |  |
| M01 | manifest | PASS | manifest identity/version is exact |  |
| M02 | manifest | PASS | manifest object counts are exact |  |
| M03 | manifest | PASS | manifest input hashes match contract |  |
| M04 | manifest | PASS | manifest retains deterministic unknown generation time |  |
| M05 | manifest | PASS | manifest validation fails rather than overclaims |  |
| M06 | manifest | PASS | manifest lists exact generator-owned deliverables |  |
| M07 | manifest | PASS | manifest defines the single canonical transformation |  |
| M08 | manifest | PASS | each transformation stage has one primary responsibility |  |
| M09 | manifest | PASS | normative and non-normative semantic planes are explicit |  |
| C01 | certificate | PASS | certificate hash is valid |  |
| C02 | certificate | PASS | certificate and manifest hashes agree |  |
| C03 | certificate | PASS | certificate version/status are truthful |  |
| C04 | certificate | PASS | certificate counts match manifest |  |
| C05 | certificate | PASS | all seven coverage dimensions remain blocked |  |
| C06 | certificate | PASS | certificate input hashes match |  |
| C07 | certificate | PASS | certificate describes limited evidentiary meaning |  |
| RPT01 | reports | PASS | report states rejected input boundary: REPORTS/REQUIREMENTS.md |  |
| RPT02 | reports | PASS | report states rejected input boundary: REPORTS/NORMATIVE-RULES.md |  |
| RPT03 | reports | PASS | report states rejected input boundary: REPORTS/GUIDANCE.md |  |
| RPT04 | reports | PASS | report states rejected input boundary: REPORTS/ACCEPTANCE-CRITERIA.md |  |
| RPT05 | reports | PASS | report states rejected input boundary: REPORTS/TEST-ORACLES.md |  |
| RPT06 | reports | PASS | report states rejected input boundary: REPORTS/DEPENDENCIES.md |  |
| RPT07 | reports | PASS | report states rejected input boundary: REPORTS/CONFLICTS.md |  |
| RPT08 | reports | PASS | report states rejected input boundary: REPORTS/CONFORMANCE.md |  |
| RPT09 | reports | PASS | report states rejected input boundary: REPORTS/VERIFICATION.md |  |
| RPT10 | reports | PASS | report states rejected input boundary: REPORTS/TRACEABILITY.md |  |
| RPT11 | reports | PASS | report states rejected input boundary: REPORTS/SPECIFICATION-AUDIT.md |  |
| RPT12 | reports | PASS | report states rejected input boundary: REPORTS/FINAL-SPECIFICATION.md |  |
| H01 | hygiene | PASS | all machine/schema YAML is JSON-compatible |  |
| H02 | hygiene | PASS | authoritative documents are not generator outputs |  |
| H03 | hygiene | PASS | no Python cache artifacts exist |  |
| H04 | hygiene | PASS | all generator-owned artifacts reproduce byte-for-byte |  |
| H05 | hygiene | PASS | v11.1 generator and validator exist |  |
| GATE-V111 | acceptance | BLOCKED | v11.1 normative specification acceptance | The v10.1 package is not a verified source package; normative derivation and conformance remain blocked. |
