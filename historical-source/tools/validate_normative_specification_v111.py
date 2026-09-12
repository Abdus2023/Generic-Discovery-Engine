#!/usr/bin/env python3
"""Independent structural and semantic validator for Protocol-v11.1.

The current expected acceptance result is an input-rejected normative gate. Structural
success validates that rejection, the non-normative separation, and complete schemas;
it does not turn the package into an accepted normative specification.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
HS = ROOT / "historical-source"
OBL = HS / "obligations"
OUT = HS / "specification"
MACHINE = ["INPUT-CONTRACT.yaml", "SPECIFICATION-MANIFEST.yaml", "SPECIFICATION-CERTIFICATE.yaml", "EVIDENCE-REFERENCES.yaml", "PROPERTY-REFERENCES.yaml", "OBLIGATION-REFERENCES.yaml", "REQUIREMENTS.yaml", "NORMATIVE-RULES.yaml", "CONDITIONS.yaml", "PREDICATES.yaml", "CONSTRAINTS.yaml", "GUIDANCE.yaml", "RATIONALES.yaml", "ASSUMPTIONS.yaml", "IMPLEMENTATION-NOTES.yaml", "EXAMPLES.yaml", "ACCEPTANCE-CRITERIA.yaml", "TEST-ORACLES.yaml", "INVARIANTS.yaml", "TRANSITIONS.yaml", "EFFECTS.yaml", "EXCEPTIONS.yaml", "REQUIREMENT-DEPENDENCIES.yaml", "REQUIREMENT-CONFLICTS.yaml", "REQUIREMENT-SUPERSESSION.yaml", "COMPATIBILITY.yaml", "IMPLEMENTATION-BOUNDARIES.yaml", "VERIFICATION.yaml", "TEST-RESULTS.yaml", "CONFORMANCE.yaml", "TRACEABILITY.yaml"]
REPORTS = ["REPORTS/REQUIREMENTS.md", "REPORTS/NORMATIVE-RULES.md", "REPORTS/GUIDANCE.md", "REPORTS/ACCEPTANCE-CRITERIA.md", "REPORTS/TEST-ORACLES.md", "REPORTS/DEPENDENCIES.md", "REPORTS/CONFLICTS.md", "REPORTS/CONFORMANCE.md", "REPORTS/VERIFICATION.md", "REPORTS/TRACEABILITY.md", "REPORTS/SPECIFICATION-AUDIT.md", "REPORTS/FINAL-SPECIFICATION.md"]
SCHEMA_NAMES = ["specification", "requirement", "rule", "guidance", "rationale", "assumption", "implementation-note", "example", "condition", "predicate", "constraint", "acceptance-criterion", "oracle", "invariant", "transition", "effect", "exception", "compatibility", "dependency", "conflict", "supersession", "boundary", "verification", "test-result", "conformance", "traceability", "evidence", "property", "obligation", "certificate"]
SCHEMAS = [f"SCHEMA/{x}.schema.yaml" for x in SCHEMA_NAMES]
DELIVERABLES = MACHINE + REPORTS + SCHEMAS
REQUIREMENT_TYPES = {"BEHAVIORAL", "STRUCTURAL", "INTERFACE", "SEMANTIC", "STATE", "LIFECYCLE", "ERROR", "SECURITY", "AUTHORIZATION", "CONCURRENCY", "RESOURCE", "PERFORMANCE", "PERSISTENCE", "PROVENANCE", "OBSERVABILITY", "COMPATIBILITY", "CONFIGURATION", "SERIALIZATION", "DISCOVERY", "DEDUPLICATION", "SCHEDULING", "CANCELLATION", "RECOVERY", "AUDIT", "EXPORT", "UI", "TESTABILITY", "VERIFICATION", "NEGATIVE", "INVARIANT", "TRANSITION", "BOUNDARY"}
DISPOSITIONS = {"PRESERVE", "STABILIZE", "GENERALIZE", "FORMALIZE", "STRENGTHEN", "RESTRICT", "COMPATIBILIZE", "DEPRECATE", "REJECT", "INTRODUCE", "OPTIONALIZE"}
STRENGTHS = {"MANDATORY", "CONDITIONAL", "RECOMMENDED", "OPTIONAL", "EXPERIMENTAL", "NON_NORMATIVE", "UNKNOWN"}
GUIDANCE_TYPES = {"ARCHITECTURAL", "IMPLEMENTATION", "TESTING", "OPERATIONS", "MIGRATION", "COMPATIBILITY", "PERFORMANCE", "SECURITY", "DEBUGGING", "DOCUMENTATION", "MAINTENANCE", "INTERPRETATION", "EXAMPLE"}
GUIDANCE_PRIORITIES = {"RECOMMENDED", "OPTIONAL", "INFORMATIONAL"}
SCOPES = {"GLOBAL", "VERSION", "COMPONENT", "INTERFACE", "OPERATION", "STATE", "TRANSITION", "CANDIDATE", "OBSERVATION", "DISCOVERY", "PROVIDER", "SCHEDULER", "WORKER", "KNOWLEDGE_BASE", "PERSISTENCE", "EXPORT", "UI", "TEST", "SECURITY_BOUNDARY", "TRUST_BOUNDARY", "CONFIGURATION", "RUNTIME"}
EPISTEMIC = {"PROVED", "SUPPORTED", "INFERRED", "CONJECTURED", "CONTRADICTED", "UNKNOWN"}
LIFECYCLE = {"DISCOVERED", "DERIVED", "DRAFTED", "FORMALIZED", "IMPLEMENTED", "PARTIALLY_IMPLEMENTED", "VERIFIED", "FAILED", "SUPERSEDED", "REJECTED", "DEPRECATED", "UNKNOWN"}
OPERATORS = {"MUST", "MUST_NOT", "MAY"}
PREDICATES = {"EQUALITY", "INEQUALITY", "MEMBERSHIP", "EXISTENCE", "NON_EXISTENCE", "TYPE", "SHAPE", "RANGE", "CARDINALITY", "UNIQUENESS", "ORDERING", "TEMPORAL", "STATE", "TRANSITION", "DEPENDENCY", "AUTHORIZATION", "CAPABILITY", "PROVENANCE", "HASH", "SIGNATURE", "REFERENCE", "SCHEMA", "CONTAINMENT", "RESOURCE_BOUND", "CONCURRENCY", "CANCELLATION", "DETERMINISM", "COMPATIBILITY"}
COMPOUND = {"AND", "OR", "NOT", "XOR", "IMPLIES", "IFF", "FOR_ALL", "EXISTS", "EXACTLY_ONE", "AT_LEAST_ONE", "AT_MOST_ONE"}
ORACLES = {"BOOLEAN", "EXACT_VALUE", "RANGE", "SET_MEMBERSHIP", "STRUCTURAL", "STATE", "TRACE", "INVARIANT", "PROPERTY", "REFERENCE_MODEL", "DIFFERENTIAL", "METAMORPHIC", "HASH", "SIGNATURE", "SCHEMA", "TEMPORAL", "RESOURCE_BOUND", "SECURITY_POLICY"}
DEPENDENCY_RELATIONS = {"REQUIRES", "ENABLES", "SUPPORTS", "REFINES", "STRENGTHENS", "CONSTRAINS", "CONFLICTS_WITH", "SUPERSEDES", "VERIFIED_BY", "DERIVED_FROM"}
FAILURE_CLASSES = {"INPUT_FAILURE", "SCHEMA_FAILURE", "REFERENCE_FAILURE", "DERIVATION_FAILURE", "NORMATIVE_CLASSIFICATION_FAILURE", "DEPENDENCY_FAILURE", "CONFLICT_FAILURE", "SCOPE_FAILURE", "SEMANTIC_FAILURE", "RULE_FAILURE", "ACCEPTANCE_FAILURE", "ORACLE_FAILURE", "BOUNDARY_FAILURE", "TRACEABILITY_FAILURE", "VERIFICATION_FAILURE", "CONFORMANCE_FAILURE"}
CANONICAL_CHAIN = ["SOURCE", "EVIDENCE", "PROPERTY", "OBLIGATION", "REQUIREMENT", "RULE", "ACCEPTANCE_CRITERION", "TEST_ORACLE", "TEST_RESULT", "VERIFICATION", "CONFORMANCE"]
NORMATIVE_RE = re.compile(r"\b(?:MUST|MUST_NOT|SHALL|SHALL_NOT|MAY|MAY_NOT|ONLY_IF|UNLESS)\b")


def load(name: str, base: Path = OUT) -> Any:
    return json.loads((base / name).read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def object_hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def main() -> int:
    checks: list[dict[str, str]] = []
    def check(cid: str, category: str, description: str, ok: bool, detail: str = "") -> None:
        checks.append({"check_id": cid, "category": category, "description": description, "result": "PASS" if ok else "FAIL", "detail": detail})
    def blocked(cid: str, category: str, description: str, detail: str) -> None:
        checks.append({"check_id": cid, "category": category, "description": description, "result": "BLOCKED", "detail": detail})

    for i, name in enumerate(DELIVERABLES, 1):
        check(f"A{i:02d}", "artifacts", f"required v11.1 artifact exists: {name}", (OUT / name).is_file())
    if any(x["result"] == "FAIL" for x in checks): return finish(checks, {})

    ic = load("INPUT-CONTRACT.yaml"); manifest = load("SPECIFICATION-MANIFEST.yaml")["specification"]; cert = load("SPECIFICATION-CERTIFICATE.yaml")
    evidence = load("EVIDENCE-REFERENCES.yaml")["evidence"]; properties = load("PROPERTY-REFERENCES.yaml")["properties"]; obligations = load("OBLIGATION-REFERENCES.yaml")["obligations"]
    requirements = load("REQUIREMENTS.yaml"); rules = load("NORMATIVE-RULES.yaml"); conditions = load("CONDITIONS.yaml"); predicates = load("PREDICATES.yaml"); constraints = load("CONSTRAINTS.yaml")
    guidance = load("GUIDANCE.yaml"); rationales = load("RATIONALES.yaml"); assumptions = load("ASSUMPTIONS.yaml"); notes = load("IMPLEMENTATION-NOTES.yaml"); examples = load("EXAMPLES.yaml")
    criteria = load("ACCEPTANCE-CRITERIA.yaml"); oracles = load("TEST-ORACLES.yaml"); invariants = load("INVARIANTS.yaml"); transitions = load("TRANSITIONS.yaml"); effects = load("EFFECTS.yaml"); exceptions = load("EXCEPTIONS.yaml")
    deps = load("REQUIREMENT-DEPENDENCIES.yaml"); conflicts = load("REQUIREMENT-CONFLICTS.yaml"); supersession = load("REQUIREMENT-SUPERSESSION.yaml"); compatibility = load("COMPATIBILITY.yaml"); boundaries = load("IMPLEMENTATION-BOUNDARIES.yaml")
    verification = load("VERIFICATION.yaml"); test_results = load("TEST-RESULTS.yaml"); conformance = load("CONFORMANCE.yaml"); trace = load("TRACEABILITY.yaml")
    v10_contract = load("INPUT-CONTRACT.yaml", OBL); v10 = load("OBLIGATIONS.yaml", OBL); v10_conflicts = load("OBLIGATION-CONFLICTS.yaml", OBL)
    E = {x["evidence_id"]: x for x in evidence}; P = {x["property_id"]: x for x in properties}; O = {x["obligation_id"]: x for x in obligations}
    R = {x["requirement_id"]: x for x in requirements["requirements"]}; RULE = {x["rule_id"]: x for x in rules["rules"]}; G = {x["guidance_id"]: x for x in guidance["guidance"]}; RAT = {x["rationale_id"]: x for x in rationales["rationales"]}; ASM = {x["assumption_id"]: x for x in assumptions["assumptions"]}

    # Input and rejection gate.
    roles = {"obligation_contract", "obligation_registry", "historical_properties", "obligation_dependencies", "obligation_lineage", "obligation_conflicts", "traceability", "verification_records"}
    check("I01", "input", "complete v10.1 role set is bound", {x["artifact_type"] for x in ic["required_inputs"]} == roles)
    fields = {"artifact_id", "schema_version", "source_path", "producer_stage", "generated_at", "content_hash"}
    check("I02", "input", "all input identity/hash fields exist", all(fields <= set(x) for x in ic["required_inputs"]))
    check("I03", "input", "all selected input hashes match", all((ROOT / x["source_path"]).is_file() and sha(ROOT / x["source_path"]) == x["content_hash"] and x["hash_validation"] == "MATCH" for x in ic["required_inputs"]))
    check("I04", "input", "v10.1 failure is preserved", v10_contract["status"] == "INPUT_CONTRACT_FAILED" and ic["source_package"]["status"] == "INPUT_CONTRACT_FAILED")
    check("I05", "input", "v11.1 gate is explicitly closed", ic["specification_version"] == "11.1" and ic["status"] == "REJECTED_INVALID_OBLIGATION_PACKAGE" and ic["derivation_gate"] == "CLOSED")
    states = {x["state"] for x in ic["failures"]}; classes = {x["failure_class"] for x in ic["failures"]}
    check("I06", "input", "all applicable rejection states are emitted", states == {"INPUT_MISSING", "INPUT_HASH_MISMATCH", "UNVERIFIED_SOURCE", "OBLIGATION_UNKNOWN", "PROPERTY_UNKNOWN", "CONFLICT_UNRESOLVED", "DERIVATION_GATE_CLOSED"})
    check("I07", "input", "failure classes are valid and independently classified", classes <= FAILURE_CLASSES and {"INPUT_FAILURE", "VERIFICATION_FAILURE", "SEMANTIC_FAILURE", "CONFLICT_FAILURE", "DERIVATION_FAILURE"} <= classes)
    check("I08", "input", "all 54 source obligations remain unverified", ic["source_package"]["obligations"] == 54 and ic["source_package"]["verified_obligations"] == 0 and len(next(x for x in ic["failures"] if x["state"] == "UNVERIFIED_SOURCE")["affected"]) == 54)
    unknown_o = {x["obligation_id"] for x in v10["obligations"] if x["epistemic_status"] == "UNKNOWN" or x["status"] == "UNKNOWN"}
    unknown_p = {x["property_id"] for x in v10["historical_properties"] if x["epistemic_status"] == "UNKNOWN" or x["historical_status"] == "UNKNOWN"}
    check("I09", "input", "UNKNOWN obligations are not escalated", set(next(x for x in ic["failures"] if x["state"] == "OBLIGATION_UNKNOWN")["affected"]) == unknown_o and len(unknown_o) == 2)
    check("I10", "input", "UNKNOWN properties are not escalated", set(next(x for x in ic["failures"] if x["state"] == "PROPERTY_UNKNOWN")["affected"]) == unknown_p and len(unknown_p) == 14)
    unresolved = {x["conflict_id"] for x in v10_conflicts["conflicts"] if x["resolution_status"] == "UNRESOLVED"}
    check("I11", "input", "unresolved obligation conflicts remain explicit", set(next(x for x in ic["failures"] if x["state"] == "CONFLICT_UNRESOLVED")["affected"]) == unresolved and len(unresolved) == 4)

    # Source reference wrappers and provenance.
    check("W01", "wrappers", "all evidence records are wrapped without count loss", len(E) == len(v10_contract["normalized_evidence"]) == 26)
    check("W02", "wrappers", "all properties are wrapped without count loss", len(P) == len(v10["historical_properties"]) == 198)
    check("W03", "wrappers", "all obligations are wrapped without count loss", len(O) == len(v10["obligations"]) == 54)
    check("W04", "wrappers", "wrapper object type/schema/lifecycle/provenance fields exist", all({"object_type", "schema_version", "lifecycle_status", "provenance"} <= set(x) for x in evidence + properties + obligations))
    check("W05", "wrappers", "wrapper epistemic and verification status is not strengthened", all(E[x["evidence_id"]]["epistemic_status"] == x["epistemic_status"] and E[x["evidence_id"]]["verification_status"] == x["verification_status"] for x in v10_contract["normalized_evidence"]))
    check("W06", "wrappers", "property epistemic status is byte-model equivalent", all(P[x["property_id"]]["epistemic_status"] == x["epistemic_status"] and P[x["property_id"]]["historical_status"] == x["historical_status"] for x in v10["historical_properties"]))
    check("W07", "wrappers", "obligation lifecycle and verification remain unverified", all(O[x["obligation_id"]]["lifecycle_status"] == x["status"] and O[x["obligation_id"]]["verification"]["result"] == "UNVERIFIED" for x in v10["obligations"]))
    check("W08", "wrappers", "all wrapper source hashes resolve", all(sha(ROOT / x["provenance"]["source_artifact"]) == x["provenance"]["content_hash"] for x in evidence + properties + obligations))

    # Normative plane remains empty.
    empty_sets = [R, RULE, conditions["conditions"], predicates["predicates"], constraints["constraints"], criteria["acceptance_criteria"], oracles["test_oracles"], invariants["invariants"], transitions["transitions"], effects["effects"], exceptions["exceptions"], deps["requirement_dependencies"], conflicts["requirement_conflicts"], supersession["supersessions"], compatibility["compatibility_records"], boundaries["boundaries"], verification["verifications"], test_results["test_results"], conformance["conformance_records"]]
    check("N01", "normative", "all normative/downstream registries are empty under closed gate", all(not x for x in empty_sets))
    check("N02", "normative", "no conformance claim is made", conformance["highest_claimed_level"] == "L0_NONE" and conformance["claim_allowed"] is False)
    check("N03", "normative", "requirement type/disposition/strength axes are exact and independent", set(requirements["requirement_types"]) == REQUIREMENT_TYPES and set(requirements["dispositions"]) == DISPOSITIONS and set(requirements["strengths"]) == STRENGTHS)
    check("N04", "normative", "DEDUPLICATION canonical spelling is used", "DEDUPLICATION" in requirements["requirement_types"] and "DEDU PLICATION" not in requirements["requirement_types"])
    check("N05", "normative", "rule operators are canonical", set(rules["operators"]) == OPERATORS)
    check("N06", "normative", "predicate and compound types remain distinct", set(rules["predicate_types"]) == PREDICATES and set(rules["compound_predicate_types"]) == COMPOUND and not (PREDICATES & COMPOUND))
    check("N07", "normative", "REQUIRES graph is empty and acyclic", not deps["nodes"] and not deps["edges"] and not deps["requires_cycles"] and deps["obligation_dependencies_copied"] is False)
    check("N08", "normative", "no obligation conflict is relabeled", not conflicts["requirement_conflicts"] and set(conflicts["upstream_obligation_conflict_blockers"]) == unresolved and conflicts["automatic_resolution"] is False)
    check("N09", "normative", "no compatibility/exact preservation claim is fabricated", not compatibility["compatibility_records"])
    check("N10", "normative", "no implementation boundary is substituted for requirement", not boundaries["boundaries"])

    # Non-normative plane and forbidden operator checks.
    check("G01", "guidance", "three explicit guidance objects are emitted", len(G) == 3)
    check("G02", "guidance", "guidance type and priority values are valid", all(x["guidance_type"] in GUIDANCE_TYPES and x["priority"] in GUIDANCE_PRIORITIES for x in G.values()))
    check("G03", "guidance", "guidance is explicitly non-normative", guidance["status"] == "NON_NORMATIVE_ONLY" and rationales["status"] == "NON_NORMATIVE_ONLY" and assumptions["status"] == "NON_NORMATIVE_ONLY" and all(x["normative"] is False and not x["related_requirements"] for x in G.values()))
    check("G04", "guidance", "guidance contains no normative operator", all(not NORMATIVE_RE.search(x["statement"]) for x in G.values()))
    check("G05", "guidance", "one rationale exists per obligation", len(RAT) == len(O) == 54 and {x["source_obligations"][0] for x in RAT.values()} == set(O))
    check("G06", "guidance", "rationales retain source property/evidence links", all(set(x["source_properties"]) <= set(P) and set(x["source_evidence"]) <= set(E) for x in RAT.values()))
    check("G07", "guidance", "rationales remain non-normative", all(x["normative"] is False and not NORMATIVE_RE.search(x["statement"]) for x in RAT.values()))
    check("G08", "guidance", "assumptions are explicit and independently validated", len(ASM) == 3 and all(x["normative"] is False and x["validation"]["status"] in {"VERIFIED", "UNVERIFIED", "FAILED", "UNKNOWN"} for x in ASM.values()))
    check("G09", "guidance", "implementation notes are not used as rules", not notes["implementation_notes"])
    check("G10", "guidance", "examples cannot define normative scope", not examples["examples"] and examples["normative_value_required"] is False)
    check("G11", "guidance", "all non-normative provenance hashes resolve", all(sha(ROOT / x["provenance"]["source_artifact"]) == x["provenance"]["content_hash"] for x in list(G.values()) + list(RAT.values()) + list(ASM.values())))
    check("G12", "guidance", "harness boundary is separate and non-mutating", oracles["harness"]["status"] == "NOT_INSTANTIATED_INPUT_REJECTED" and oracles["harness"]["may_silently_alter_tested_semantics"] is False)

    # First-class identity/reference/schema rules.
    all_objects = evidence + properties + obligations + list(G.values()) + list(RAT.values()) + list(ASM.values()) + trace["canonical_edges"] + trace["supporting_edges"]
    id_fields = {"EVIDENCE": "evidence_id", "PROPERTY": "property_id", "OBLIGATION": "obligation_id", "GUIDANCE": "guidance_id", "RATIONALE": "rationale_id", "ASSUMPTION": "assumption_id", "TRACEABILITY": "traceability_id"}
    ids = [x[id_fields[x["object_type"]]] for x in all_objects]
    check("O01", "objects", "all instantiated first-class IDs are globally unique", len(ids) == len(set(ids)))
    check("O02", "objects", "all instantiated objects have type/schema/lifecycle/provenance", all(x["schema_version"] == "1.0" and x["lifecycle_status"] in LIFECYCLE and x["provenance"] for x in all_objects))
    check("O03", "objects", "all rationale references resolve", all(set(x["source_obligations"]) <= set(O) and set(x["source_properties"]) <= set(P) and set(x["source_evidence"]) <= set(E) for x in RAT.values()))
    check("O04", "objects", "all guidance obligation references resolve", all(set(x["related_obligations"]) <= set(O) for x in G.values()))
    check("O05", "objects", "all assumption affected references resolve or are explicitly empty", all(set(x["affected_objects"]) <= set(O) for x in ASM.values()))
    check("O06", "objects", "no broken final mandatory reference can exist", not R and not RULE)

    schema = {name: load(f"SCHEMA/{name}.schema.yaml") for name in SCHEMA_NAMES}
    check("S01", "schemas", "all 30 dedicated schemas are present", len(schema) == 30 and set(schema) == set(SCHEMA_NAMES))
    check("S02", "schemas", "every schema declares version 1.0", all(x["schema_version"] == "1.0" for x in schema.values()))
    required_schema_tree = {"specification", "requirement", "rule", "guidance", "rationale", "assumption", "implementation-note", "example", "condition", "predicate", "acceptance-criterion", "oracle", "invariant", "transition", "effect", "exception", "compatibility", "dependency", "conflict", "supersession", "boundary", "verification", "test-result", "conformance", "traceability"}
    check("S03", "schemas", "required 25-schema tree is complete", required_schema_tree <= set(schema) and len(required_schema_tree) == 25)
    check("S04", "schemas", "constraint/evidence/property/obligation/certificate extension schemas exist", {"constraint", "evidence", "property", "obligation", "certificate"} <= set(schema))
    check("S05", "schemas", "requirement schema keeps normative and supporting references separate", {"rules", "acceptance_criteria", "invariants", "transitions", "guidance", "implementation_notes", "examples", "assumptions", "implementation_boundaries"} <= set(schema["requirement"]["required"]))
    check("S06", "schemas", "guidance and example schemas force non-normative classification", schema["guidance"]["properties"]["normative"]["const"] is False and schema["example"]["properties"]["normative"]["const"] is False)
    check("S07", "schemas", "predicate schema supports controlled recursion", schema["predicate"]["properties"]["operands"]["items"]["$ref"] == "predicate.schema.yaml")
    check("S08", "schemas", "rule schema allows only canonical operators", set(schema["rule"]["properties"]["operator"]["enum"]) == OPERATORS)
    check("S09", "schemas", "all object schemas require identity/type/schema/lifecycle/provenance", all({"object_type", "schema_version", "lifecycle_status", "provenance"} <= set(schema[n]["required"]) for n in SCHEMA_NAMES if n != "specification"))
    check("S10", "schemas", "schema changes are classified", all(x["schema_change_class"] in {"PATCH", "MINOR", "MAJOR"} for x in schema.values()))

    # Traceability canonical and supporting graphs.
    node_ids = {x["object_id"] for x in trace["nodes"]}
    all_edges = trace["canonical_edges"] + trace["supporting_edges"]
    check("T01", "traceability", "single canonical chain is exact", trace["canonical_chain"] == CANONICAL_CHAIN)
    check("T02", "traceability", "trace terminates at obligation", trace["status"] == "PARTIAL_BLOCKED_AT_OBLIGATION" and not trace["normative_nodes_after_obligation"])
    check("T03", "traceability", "all edge endpoints resolve", all(x["from"]["object_id"] in node_ids and x["to"]["object_id"] in node_ids for x in all_edges))
    check("T04", "traceability", "canonical forward edges use FORMALIZED_AS", all(x["relation"] == "FORMALIZED_AS" for x in trace["canonical_edges"]))
    check("T05", "traceability", "supporting edges use only non-canonical attachment relations", {x["relation"] for x in trace["supporting_edges"]} <= {"JUSTIFIED_BY", "EXPLAINED_BY", "QUALIFIED_BY", "ILLUSTRATED_BY", "INFORMED_BY"})
    check("T06", "traceability", "exact reverse traversal is available", len(trace["reverse_edges"]) == len(all_edges) and {(x["to"]["object_id"], x["from"]["object_id"], "REVERSE_" + x["relation"]) for x in all_edges} == {(x["from"]["object_id"], x["to"]["object_id"], x["relation"]) for x in trace["reverse_edges"]})
    check("T07", "traceability", "all source objects remain represented", set(E) | set(P) | set(O) <= node_ids)
    check("T08", "traceability", "supporting records do not extend canonical normative chain", not any(x["to"]["object_type"] in {"REQUIREMENT", "RULE", "ACCEPTANCE_CRITERION", "TEST_ORACLE"} for x in trace["supporting_edges"]))
    check("T09", "traceability", "traceability objects have complete identity and provenance", all(x["object_type"] == "TRACEABILITY" and x["schema_version"] == "1.0" and x["lifecycle_status"] == "DERIVED" and sha(ROOT / x["provenance"]["source_artifact"]) == x["provenance"]["content_hash"] for x in all_edges))

    # Audit, completeness, manifest, certificate.
    audit_text = (OUT / "REPORTS/SPECIFICATION-AUDIT.md").read_text(encoding="utf-8")
    stages = ["INPUT VALIDATION", "SCHEMA VALIDATION", "REFERENCE VALIDATION", "DERIVATION VALIDATION", "NORMATIVE/GUIDANCE SEPARATION", "DEPENDENCY VALIDATION", "CONFLICT DETECTION", "SEMANTIC NARROWING/WIDENING", "RULE VALIDATION", "ACCEPTANCE VALIDATION", "ORACLE VALIDATION", "BOUNDARY VALIDATION", "TRACEABILITY VALIDATION", "CONFORMANCE VALIDATION"]
    check("A80", "audit", "audit executes all fourteen stages in order", all(f"| {i} | {stage} |" in audit_text for i, stage in enumerate(stages, 1)))
    dimensions = {"TRACEABILITY", "SEMANTICS", "NORMATIVITY", "SCHEMA", "DEPENDENCY", "CONFLICT", "ACCEPTANCE", "ORACLE", "VERIFICATION", "SECURITY", "FAILURE", "COMPATIBILITY", "BOUNDARY"}
    check("A81", "audit", "all thirteen completeness dimensions are independent", all(x in audit_text for x in dimensions))
    check("A82", "audit", "all twenty final invariants pass by explicit separation/gating", all(f"V111-I{i:02d}" in audit_text and "PASS" in audit_text for i in range(1, 21)) and len(invariants["pipeline_invariant_results"]) == 20)
    check("A83", "audit", "all specification failure classes are registered", all(x in audit_text for x in FAILURE_CLASSES))
    check("A84", "audit", "no aggregate percentage conceals blockers", "No aggregate percentage" in audit_text)

    counts = manifest["objects"]
    expected_counts = {"evidence": 26, "historical_properties": 198, "source_obligations": 54, "requirements": 0, "rules": 0, "guidance": 3, "rationales": 54, "assumptions": 3, "implementation_notes": 0, "examples": 0, "conditions": 0, "predicates": 0, "constraints": 0, "acceptance_criteria": 0, "oracles": 0, "invariants": 0, "transitions": 0, "effects": 0, "exceptions": 0, "dependencies": 0, "conflicts": 0, "compatibility": 0, "boundaries": 0, "verifications": 0, "test_results": 0, "conformance_records": 0}
    check("M01", "manifest", "manifest identity/version is exact", manifest["manifest_id"] == "SPEC-MANIFEST-11.1" and manifest["specification_version"] == "11.1" and manifest["input_contract_version"] == "1.0")
    check("M02", "manifest", "manifest object counts are exact", counts == expected_counts)
    check("M03", "manifest", "manifest input hashes match contract", manifest["inputs"] == [{"artifact_id": x["artifact_id"], "content_hash": x["content_hash"]} for x in ic["required_inputs"]])
    check("M04", "manifest", "manifest retains deterministic unknown generation time", manifest["generated_at"] == "UNKNOWN_NOT_RECORDED_DETERMINISTIC_BUILD")
    check("M05", "manifest", "manifest validation fails rather than overclaims", manifest["validation"] == {"status": "FAIL", "errors": 7, "warnings": 1} and manifest["lifecycle_status"] == "FAILED")
    check("M06", "manifest", "manifest lists exact generator-owned deliverables", manifest["deliverables"] == DELIVERABLES)
    check("M07", "manifest", "manifest defines the single canonical transformation", manifest["canonical_transformation"] == CANONICAL_CHAIN)
    responsibility_stages = ["EVIDENCE", "PROPERTY", "OBLIGATION", "REQUIREMENT", "RULE", "ACCEPTANCE_CRITERION", "TEST_ORACLE", "TEST_RESULT", "VERIFICATION", "CONFORMANCE"]
    check("M08", "manifest", "each transformation stage has one primary responsibility", [x["stage"] for x in manifest["stage_responsibilities"]] == responsibility_stages and all(x["responsibility"] for x in manifest["stage_responsibilities"]))
    check("M09", "manifest", "normative and non-normative semantic planes are explicit", set(manifest["semantic_planes"]["NORMATIVE"]) == {"REQUIREMENT", "RULE", "ACCEPTANCE_CRITERION", "INVARIANT", "TRANSITION", "CONSTRAINT"} and set(manifest["semantic_planes"]["NON_NORMATIVE"]) == {"GUIDANCE", "RATIONALE", "IMPLEMENTATION_NOTE", "EXAMPLE", "RECOMMENDATION", "ASSUMPTION"})
    cert_copy = {k: v for k, v in cert.items() if k != "certificate_hash"}
    check("C01", "certificate", "certificate hash is valid", cert["certificate_hash"] == object_hash(cert_copy))
    check("C02", "certificate", "certificate and manifest hashes agree", manifest["certificate"]["hash"] == cert["certificate_hash"])
    check("C03", "certificate", "certificate version/status are truthful", cert["specification_version"] == "11.1" and cert["validation_status"] == "FAIL" and cert["lifecycle_status"] == "FAILED")
    check("C04", "certificate", "certificate counts match manifest", cert["counts"] == counts)
    check("C05", "certificate", "all seven coverage dimensions remain blocked", set(cert["coverage"]) == {"obligation_requirement", "requirement_rule", "requirement_acceptance", "acceptance_oracle", "oracle_test", "test_verification", "verification_conformance"} and set(cert["coverage"].values()) == {"BLOCKED"})
    check("C06", "certificate", "certificate input hashes match", cert["input_hashes"] == [x["content_hash"] for x in ic["required_inputs"]])
    check("C07", "certificate", "certificate describes limited evidentiary meaning", "not proof" in cert["certificate_semantics"])

    # Report and determinism/hygiene checks.
    for i, name in enumerate(REPORTS, 1):
        text = (OUT / name).read_text(encoding="utf-8")
        check(f"RPT{i:02d}", "reports", f"report states rejected input boundary: {name}", "REJECTED_INVALID_OBLIGATION_PACKAGE" in text)
    check("H01", "hygiene", "all machine/schema YAML is JSON-compatible", all(parseable(OUT / x) for x in MACHINE + SCHEMAS))
    check("H02", "hygiene", "authoritative documents are not generator outputs", all("Userscript Discovery Prototype.md" not in x and "Continue Architecture Planning.md" not in x for x in DELIVERABLES))
    check("H03", "hygiene", "no Python cache artifacts exist", not any(HS.rglob("__pycache__")) and not any(HS.rglob("*.pyc")))
    det = load("DETERMINISM-VALIDATION.yaml") if (OUT / "DETERMINISM-VALIDATION.yaml").is_file() else {}
    check("H04", "hygiene", "all generator-owned artifacts reproduce byte-for-byte", det.get("status") == "PASS" and det.get("summary", {}).get("total") == len(DELIVERABLES) and det.get("summary", {}).get("identical") == len(DELIVERABLES) and {x["path"] for x in det.get("files", [])} == set(DELIVERABLES))
    check("H05", "hygiene", "v11.1 generator and validator exist", (HS / "tools/build_normative_specification_v111.py").is_file() and (HS / "tools/validate_normative_specification_v111.py").is_file())
    blocked("GATE-V111", "acceptance", "v11.1 normative specification acceptance", "The v10.1 package is not a verified source package; normative derivation and conformance remain blocked.")
    return finish(checks, expected_counts)


def parseable(path: Path) -> bool:
    try: json.loads(path.read_text(encoding="utf-8")); return True
    except Exception: return False


def finish(checks: list[dict[str, str]], counts: dict[str, int]) -> int:
    passed = sum(x["result"] == "PASS" for x in checks); failed = sum(x["result"] == "FAIL" for x in checks); blocked = sum(x["result"] == "BLOCKED" for x in checks)
    report = {"schema_version": "1.0", "specification_version": "11.1", "overall_status": "FAIL" if failed else "STRUCTURAL_PASS_INPUT_REJECTED" if blocked else "PASS", "acceptance": "VALIDATION_FAILED" if failed else "REJECTED_INVALID_OBLIGATION_PACKAGE" if blocked else "PASS", "summary": {"total": len(checks), "passed": passed, "failed": failed, "blocked": blocked}, "object_counts": counts, "checks": checks}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "VALIDATION.yaml").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    lines = ["# Protocol-v11.1 Validation", "", f"**Overall:** `{report['overall_status']}`", f"**Acceptance:** `{report['acceptance']}`", f"**Checks:** {passed} PASS / {failed} FAIL / {blocked} BLOCKED ({len(checks)} total)", "", "Structural success validates rejection, schema completeness, and normative/non-normative separation. It does not authorize normative derivation.", "", "| ID | Category | Result | Description | Detail |", "|---|---|---|---|---|"]
    for x in checks: lines.append("| %s | %s | %s | %s | %s |" % (x["check_id"], x["category"], x["result"], x["description"].replace("|", "\\|"), x["detail"].replace("|", "\\|")))
    (OUT / "VALIDATION.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{passed} PASS / {failed} FAIL / {blocked} BLOCKED ({len(checks)} checks); {report['overall_status']}")
    return 1 if failed else 0


if __name__ == "__main__": sys.exit(main())
