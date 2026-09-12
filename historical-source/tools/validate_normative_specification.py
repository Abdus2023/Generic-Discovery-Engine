#!/usr/bin/env python3
"""Independent Protocol-v11 validator.

The expected acceptance outcome for the current repository is a structurally correct
rejection: the v10.1 source package is not verified and cannot produce requirements.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
HS = ROOT / "historical-source"
OBL = HS / "obligations"
OUT = HS / "specification"
MACHINE = ["INPUT-CONTRACT.yaml", "REQUIREMENTS.yaml", "NORMATIVE-RULES.yaml", "ACCEPTANCE-CRITERIA.yaml", "TEST-ORACLES.yaml", "REQUIREMENT-DEPENDENCIES.yaml", "REQUIREMENT-CONFLICTS.yaml", "REQUIREMENT-SUPERSESSION.yaml", "REQUIREMENT-COVERAGE.yaml", "CONFORMANCE-MATRIX.yaml", "VERIFICATION-MATRIX.yaml", "IMPLEMENTATION-BOUNDARIES.yaml", "SEMANTIC-DIFFS.yaml", "TRACEABILITY.yaml", "CONFORMANCE.yaml", "SPECIFICATION-CERTIFICATE.yaml"]
REPORTS = ["REQUIREMENTS.md", "NORMATIVE-RULES.md", "ACCEPTANCE-CRITERIA.md", "TEST-ORACLES.md", "REQUIREMENT-COVERAGE.md", "REQUIREMENT-DEPENDENCIES.md", "REQUIREMENT-CONFLICTS.md", "CONFORMANCE-MATRIX.md", "VERIFICATION-MATRIX.md", "IMPLEMENTATION-BOUNDARIES.md", "SEMANTIC-DIFFS.md", "TRACEABILITY.md", "SPECIFICATION-AUDIT.md", "FINAL-SPECIFICATION.md"]
SCHEMAS = ["schema/requirement.schema.yaml", "schema/normative-rule.schema.yaml", "schema/acceptance-criterion.schema.yaml", "schema/test-oracle.schema.yaml", "schema/requirement-dependency.schema.yaml", "schema/traceability.schema.yaml", "schema/specification-certificate.schema.yaml"]
DELIVERABLES = MACHINE + REPORTS + SCHEMAS
REQUIREMENT_TYPES = {"BEHAVIORAL", "STRUCTURAL", "INTERFACE", "SEMANTIC", "STATE", "LIFECYCLE", "ERROR", "SECURITY", "AUTHORIZATION", "CONCURRENCY", "RESOURCE", "PERFORMANCE", "PERSISTENCE", "PROVENANCE", "OBSERVABILITY", "COMPATIBILITY", "CONFIGURATION", "SERIALIZATION", "DISCOVERY", "DEDUPLICATION", "SCHEDULING", "CANCELLATION", "RECOVERY", "AUDIT", "EXPORT", "UI", "TESTABILITY", "VERIFICATION", "NEGATIVE", "INVARIANT", "TRANSITION", "BOUNDARY"}
DISPOSITIONS = {"PRESERVE", "STABILIZE", "GENERALIZE", "FORMALIZE", "STRENGTHEN", "RESTRICT", "COMPATIBILIZE", "DEPRECATE", "REJECT", "INTRODUCE", "OPTIONALIZE"}
STRENGTHS = {"MANDATORY", "CONDITIONAL", "RECOMMENDED", "OPTIONAL", "EXPERIMENTAL", "NON_NORMATIVE", "UNKNOWN"}
SCOPES = {"GLOBAL", "VERSION", "COMPONENT", "INTERFACE", "OPERATION", "STATE", "TRANSITION", "CANDIDATE", "OBSERVATION", "DISCOVERY", "PROVIDER", "SCHEDULER", "WORKER", "KNOWLEDGE_BASE", "PERSISTENCE", "EXPORT", "UI", "TEST", "SECURITY_BOUNDARY", "TRUST_BOUNDARY", "CONFIGURATION", "RUNTIME"}
EPISTEMIC = {"PROVED", "SUPPORTED", "INFERRED", "CONJECTURED", "CONTRADICTED", "UNKNOWN"}
LIFECYCLE = {"DISCOVERED", "DERIVED", "DRAFTED", "FORMALIZED", "IMPLEMENTED", "PARTIALLY_IMPLEMENTED", "VERIFIED", "FAILED", "SUPERSEDED", "REJECTED", "DEPRECATED", "UNKNOWN"}
RDEP = {"REQUIRES", "ENABLES", "SUPPORTS", "REFINES", "STRENGTHENS", "CONSTRAINS", "CONFLICTS_WITH", "SUPERSEDES", "VERIFIED_BY", "DERIVED_FROM"}
INPUT_REJECTIONS = {"INPUT_MISSING", "INPUT_SCHEMA_MISMATCH", "INPUT_HASH_MISMATCH", "OBLIGATION_UNKNOWN", "PROPERTY_UNKNOWN", "BROKEN_LINEAGE", "BROKEN_DEPENDENCY", "TEMPORAL_CONTAMINATION", "UNVERIFIED_SOURCE", "CONFLICT_UNRESOLVED"}
FAILURE_MODES = {"REQUIREMENT_WITHOUT_OBLIGATION", "REQUIREMENT_WITHOUT_EVIDENCE", "UNTRACED_REQUIREMENT", "ORPHAN_OBLIGATION", "NON_TESTABLE_REQUIREMENT", "ORACLE_CIRCULARITY", "ORACLE_IMPLEMENTATION_COUPLING", "DEPENDENCY_CYCLE", "UNRESOLVED_CONFLICT", "SEMANTIC_NARROWING", "SEMANTIC_WIDENING", "RETROACTIVE_NORMATIVITY", "HISTORICAL_CONTAMINATION", "FALSE_VERIFICATION", "FALSE_PROOF", "HIDDEN_EXCEPTION", "UNDEFINED_SCOPE", "UNDEFINED_BOUNDARY", "UNMEASURABLE_PROPERTY", "MISSING_NEGATIVE_TEST", "COMPATIBILITY_OVERCLAIM", "UNJUSTIFIED_STRENGTHENING", "HARNESS_CONFUSION", "UNKNOWN_ESCALATION"}


def load(base: Path, name: str) -> Any:
    return json.loads((base / name).read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def object_hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest()


def main() -> int:
    checks: list[dict[str, str]] = []
    def check(cid: str, category: str, description: str, ok: bool, detail: str = "") -> None:
        checks.append({"check_id": cid, "category": category, "description": description, "result": "PASS" if ok else "FAIL", "detail": detail})
    def blocked(cid: str, category: str, description: str, detail: str) -> None:
        checks.append({"check_id": cid, "category": category, "description": description, "result": "BLOCKED", "detail": detail})

    for i, name in enumerate(DELIVERABLES, 1):
        check(f"A{i:02d}", "deliverables", f"required v11 deliverable exists: {name}", (OUT / name).is_file())
    if any(x["result"] == "FAIL" for x in checks):
        return finish(checks, {})

    ic = load(OUT, "INPUT-CONTRACT.yaml")
    requirements = load(OUT, "REQUIREMENTS.yaml")
    rules = load(OUT, "NORMATIVE-RULES.yaml")
    criteria = load(OUT, "ACCEPTANCE-CRITERIA.yaml")
    oracles = load(OUT, "TEST-ORACLES.yaml")
    deps = load(OUT, "REQUIREMENT-DEPENDENCIES.yaml")
    conflicts = load(OUT, "REQUIREMENT-CONFLICTS.yaml")
    supersession = load(OUT, "REQUIREMENT-SUPERSESSION.yaml")
    coverage = load(OUT, "REQUIREMENT-COVERAGE.yaml")
    conformance_matrix = load(OUT, "CONFORMANCE-MATRIX.yaml")
    verification = load(OUT, "VERIFICATION-MATRIX.yaml")
    boundaries = load(OUT, "IMPLEMENTATION-BOUNDARIES.yaml")
    diffs = load(OUT, "SEMANTIC-DIFFS.yaml")
    trace = load(OUT, "TRACEABILITY.yaml")
    conformance = load(OUT, "CONFORMANCE.yaml")
    certificate = load(OUT, "SPECIFICATION-CERTIFICATE.yaml")
    upstream_contract = load(OBL, "INPUT-CONTRACT.yaml")
    upstream = load(OBL, "OBLIGATIONS.yaml")
    upstream_deps = load(OBL, "OBLIGATION-DEPENDENCIES.yaml")
    upstream_lineage = load(OBL, "OBLIGATION-LINEAGE.yaml")
    upstream_conflicts = load(OBL, "OBLIGATION-CONFLICTS.yaml")
    audit_text = (OUT / "SPECIFICATION-AUDIT.md").read_text(encoding="utf-8")
    obligations = upstream["obligations"]
    properties = upstream["historical_properties"]
    O = {x["obligation_id"]: x for x in obligations}
    P = {x["property_id"]: x for x in properties}
    R = {x["requirement_id"]: x for x in requirements["requirements"]}
    RULE = {x["rule_id"]: x for x in rules["rules"]}
    AC = {x["criterion_id"]: x for x in criteria["acceptance_criteria"]}
    ORACLE = {x["oracle_id"]: x for x in oracles["test_oracles"]}

    # Input contract (§§703-704).
    required_roles = {"obligation_contract", "obligation_registry", "historical_properties", "obligation_dependencies", "obligation_lineage", "obligation_conflicts", "traceability", "verification_records"}
    check("I01", "input", "all eight v10.1 input roles are present", {x["artifact_type"] for x in ic["required_inputs"]} == required_roles)
    required_fields = {"artifact_id", "schema_version", "source_path", "producer_stage", "generated_at", "content_hash"}
    check("I02", "input", "every input records required identity and integrity fields", all(required_fields <= set(x) for x in ic["required_inputs"]))
    check("I03", "input", "all selected input paths exist", all((ROOT / x["source_path"]).is_file() for x in ic["required_inputs"]))
    check("I04", "input", "all selected content hashes match", all(sha(ROOT / x["source_path"]) == x["content_hash"] and x["hash_validation"] == "MATCH" for x in ic["required_inputs"]))
    check("I05", "input", "input/schema versions are v11/1.0", ic["specification_version"] == "11.0" and ic["requirement_input_contract_version"] == "1.0" and all(x["schema_version"] == "1.0" for x in ic["required_inputs"]))
    check("I06", "input", "v10.1 failed status is propagated, not repaired", upstream_contract["status"] == "INPUT_CONTRACT_FAILED" and ic["source_package"]["input_contract_status"] == "INPUT_CONTRACT_FAILED")
    check("I07", "input", "derivation gate is closed", ic["status"] == "REJECTED_INVALID_OBLIGATION_PACKAGE" and ic["derivation_gate"] == "CLOSED")
    check("I08", "input", "all normative input rejection states are registered", set(ic["rejection_registry"]) == INPUT_REJECTIONS)
    emitted = {x["state"] for x in ic["failure_states"]}
    check("I09", "input", "applicable invalid-package states are emitted", {"INPUT_MISSING", "INPUT_HASH_MISMATCH", "UNVERIFIED_SOURCE", "OBLIGATION_UNKNOWN", "PROPERTY_UNKNOWN", "CONFLICT_UNRESOLVED"} <= emitted)
    check("I10", "input", "no unregistered rejection state is emitted", emitted <= INPUT_REJECTIONS)
    check("I11", "input", "all obligations are correctly counted as unverified", ic["source_package"]["obligation_count"] == len(O) and ic["source_package"]["verified_obligation_count"] == 0 and len(next(x for x in ic["failure_states"] if x["state"] == "UNVERIFIED_SOURCE")["affected"]) == len(O))
    unknown_o = {x["obligation_id"] for x in obligations if x["epistemic_status"] == "UNKNOWN" or x["status"] == "UNKNOWN"}
    check("I12", "input", "UNKNOWN obligations are surfaced", set(next(x for x in ic["failure_states"] if x["state"] == "OBLIGATION_UNKNOWN")["affected"]) == unknown_o and len(unknown_o) > 0)
    unknown_p = {x["property_id"] for x in properties if x["epistemic_status"] == "UNKNOWN" or x["historical_status"] == "UNKNOWN"}
    check("I13", "input", "UNKNOWN properties are surfaced", set(next(x for x in ic["failure_states"] if x["state"] == "PROPERTY_UNKNOWN")["affected"]) == unknown_p and len(unknown_p) > 0)
    unresolved = {x["conflict_id"] for x in upstream_conflicts["conflicts"] if x["resolution_status"] == "UNRESOLVED"}
    check("I14", "input", "unresolved obligation conflicts are surfaced", set(next(x for x in ic["failure_states"] if x["state"] == "CONFLICT_UNRESOLVED")["affected"]) == unresolved and len(unresolved) == 4)
    check("I15", "input", "v10.1 dependency graph remains structurally valid", upstream_deps["cycle_status"] == "ACYCLIC" and not upstream_deps["requires_cycles"] and all(x["from_obligation"] in O and x["to_obligation"] in O for x in upstream_deps["dependencies"]))
    check("I16", "input", "v10.1 lineage references remain valid", all(x["from_obligation"] in O and x["to_obligation"] in O for x in upstream_lineage["lineage"]))
    check("I17", "input", "validation order starts with failed input gate", [x["check_id"] for x in ic["validation_checks"]] == [f"RI{i:02d}" for i in range(1, 11)] and next(x for x in ic["validation_checks"] if x["check_id"] == "RI04")["result"] == "FAIL")

    # Closed-gate non-production and layer separation.
    check("L01", "layers", "no requirement is derived from invalid input", not R and requirements["status"] == "DERIVATION_REJECTED" and requirements["derivation_gate"] == "CLOSED")
    check("L02", "layers", "no rule substitutes for a requirement", not RULE and rules["status"] == "DERIVATION_REJECTED")
    check("L03", "layers", "no criterion substitutes for a rule/requirement", not AC and criteria["status"] == "DERIVATION_REJECTED")
    check("L04", "layers", "no oracle substitutes for a criterion", not ORACLE and oracles["status"] == "DERIVATION_REJECTED")
    check("L05", "layers", "no implementation boundary is invented", not boundaries["requirement_boundaries"] and boundaries["status"] == "BLOCKED")
    check("L06", "layers", "no conformance claim is fabricated", not conformance["claim_allowed"] and conformance["highest_claimed_level"] == "L0_NONE" and not conformance_matrix["implementation_claims"])
    check("L07", "layers", "obligation dependencies are not copied into requirement graph", not deps["nodes"] and not deps["edges"] and not deps["requirement_dependencies"])
    check("L08", "layers", "obligation conflicts are not relabeled requirement conflicts", not conflicts["requirement_conflicts"] and set(conflicts["upstream_obligation_conflict_blockers"]) == unresolved)
    check("L09", "layers", "requirement supersession remains independent and empty", not supersession["supersessions"])
    check("L10", "layers", "semantic narrowing/widening do not pass vacuously", diffs["narrowing_audit"]["status"] == "BLOCKED" and diffs["widening_audit"]["status"] == "BLOCKED")
    check("L11", "layers", "assumptions and exceptions are first-class machine records", {x["assumption_id"] for x in diffs["assumptions"]} == {"ASSUMP-001", "ASSUMP-002"} and diffs["exceptions"] == [])
    check("L12", "layers", "configuration and environment assumptions are not silently invented", diffs["configurations"] == [] and diffs["environment_preconditions"] == [])

    # Registry correctness and canonical spelling.
    reg = requirements["registries"]
    check("R00", "registry", "DEDU PLICATION is normalized to DEDUPLICATION", "DEDUPLICATION" in reg["requirement_types"] and "DEDU PLICATION" not in reg["requirement_types"])
    check("R01", "registry", "requirement type registry is exact", set(reg["requirement_types"]) == REQUIREMENT_TYPES)
    check("R02", "registry", "disposition registry is exact", set(reg["dispositions"]) == DISPOSITIONS)
    check("R03", "registry", "requirement strength registry is exact", set(reg["strengths"]) == STRENGTHS)
    check("R04", "registry", "scope registry is exact", set(reg["scope_types"]) == SCOPES)
    check("R05", "registry", "epistemic registry remains independent", set(reg["epistemic_states"]) == EPISTEMIC)
    check("R06", "registry", "lifecycle registry remains independent", set(reg["lifecycle_states"]) == LIFECYCLE)
    check("R07", "registry", "requirement dependency relation registry is exact", set(reg["dependency_relations"]) == RDEP)
    check("R08", "registry", "criticality remains a separate registry", set(reg["criticality_values"]) == {"CRITICAL", "HIGH", "MEDIUM", "LOW", "UNKNOWN"})
    check("R09", "registry", "conformance and verification levels remain separate", reg["conformance_levels"] != reg["verification_levels"] and len(reg["conformance_levels"]) == len(reg["verification_levels"]) == 7)
    check("R10", "registry", "forbidden equivalences are explicit", len(requirements["forbidden_equivalences"]) == 7)
    check("R11", "registry", "all fifteen v11 pipeline invariants are enforced by the rejection gate", [x["invariant_id"] for x in requirements["pipeline_invariants"]] == [f"V11-I{i:02d}" for i in range(1, 16)] and all(x["status"] == "PASS" for x in requirements["pipeline_invariants"]))
    check("R12", "registry", "compatibility and historical preservation modes are explicit", len(requirements["compatibility_types"]) == 8 and set(requirements["historical_preservation_modes"]) == {"EXACT", "SEMANTIC", "COMPATIBLE", "NORMALIZED", "GENERALIZED", "INTENTIONALLY_CHANGED", "REJECTED", "UNKNOWN"})
    check("R13", "registry", "historical preservation matrix is empty rather than fabricated", coverage["historical_preservation"] == [] and coverage["historical_preservation_modes"] == requirements["historical_preservation_modes"])

    # Machine validation rules REQ-001..REQ-015 (empty registry is allowed only because gate is closed).
    check("REQ-001", "machine_rules", "source obligations are non-empty unless expressly new/future/design", all(x["source_obligations"] or x.get("final_category") in {"DESIGN_OPTION", "FUTURE_STRENGTHENING"} or x.get("origin") == "NEW_ENGINEERING_REQUIREMENT" for x in R.values()))
    check("REQ-002", "machine_rules", "MANDATORY requirements have acceptance criteria", all(x["acceptance_criteria"] for x in R.values() if x["strength"] == "MANDATORY"))
    check("REQ-003", "machine_rules", "MANDATORY behavioral/security requirements have oracles", all(x["test_oracles"] for x in R.values() if x["strength"] == "MANDATORY" and x["requirement_type"] in {"BEHAVIORAL", "SECURITY", "AUTHORIZATION", "LIFECYCLE", "CONCURRENCY"}))
    check("REQ-004", "machine_rules", "all obligation references resolve", all(set(x["source_obligations"]) <= set(O) for x in R.values()))
    check("REQ-005", "machine_rules", "all property references resolve", all(set(x["source_properties"]) <= set(P) for x in R.values()))
    check("REQ-006", "machine_rules", "all rule references resolve", all(set(x["normative_rules"]) <= set(RULE) for x in R.values()))
    check("REQ-007", "machine_rules", "all oracle references resolve", all(set(x["test_oracles"]) <= set(ORACLE) for x in R.values()))
    check("REQ-008", "machine_rules", "dependency edges reference existing requirements", all(x["from_requirement"] in R and x["to_requirement"] in R for x in deps["requirement_dependencies"]))
    check("REQ-009", "machine_rules", "REQUIRES self-dependency is forbidden", not any(x["relation"] == "REQUIRES" and x["from_requirement"] == x["to_requirement"] for x in deps["requirement_dependencies"]))
    check("REQ-010", "machine_rules", "REQUIRES graph is acyclic", not deps["requires_cycles"])
    directional = all(x.get("directional") is True for x in conflicts["requirement_conflicts"] if x.get("relation") == "CONFLICTS_WITH")
    check("REQ-011", "machine_rules", "CONFLICTS_WITH is symmetric or explicitly directional", directional)
    check("REQ-012", "machine_rules", "SUPERSEDES identifies effective scope", all(x.get("effective_scope") for x in supersession["supersessions"]))
    check("REQ-013", "machine_rules", "VERIFIED requirements possess verification evidence", all(x.get("verification", {}).get("evidence") for x in R.values() if x["lifecycle_status"] == "VERIFIED"))
    check("REQ-014", "machine_rules", "PROVED is not inferred solely from implementation", all(x.get("proof_basis") not in {None, "IMPLEMENTATION_EXISTENCE"} for x in R.values() if x["epistemic_status"] == "PROVED"))
    check("REQ-015", "machine_rules", "historical requirements trace to source evidence", all(x["source_evidence"] for x in R.values() if x.get("historical_basis") == "HISTORICAL"))

    # Coverage, orphans, traceability, and verification.
    cov = {x["obligation_id"]: x for x in coverage["obligation_coverage"]}
    check("C01", "coverage", "every obligation has one coverage record", set(cov) == set(O) and len(cov) == len(O))
    check("C02", "coverage", "all obligation coverage is blocked", all(x["coverage_status"] == "BLOCKED" and not x["requirements"] for x in cov.values()))
    check("C03", "coverage", "all orphan obligations are reported", set(coverage["orphan_obligations"]) == set(O) and all(x["orphan_status"] == "ORPHAN_OBLIGATION" for x in cov.values()))
    check("C04", "coverage", "no orphan requirement is hidden", coverage["orphan_requirements"] == [] and requirements["untraced_requirements"] == [])
    check("C05", "coverage", "all six coverage dimensions remain independent", {x["dimension"] for x in coverage["coverage_metrics"]} == {"obligation_to_requirement", "requirement_to_rule", "requirement_to_criterion", "criterion_to_oracle", "oracle_to_test", "test_to_evidence"})
    check("C06", "coverage", "single aggregate percentage is forbidden", coverage["single_aggregate_percentage"] == "FORBIDDEN")
    check("T01", "traceability", "trace graph supports exact reverse traversal", len(trace["forward_edges"]) == len(trace["reverse_edges"]) and {(x["to"], x["from"], "REVERSE_" + x["relation"]) for x in trace["forward_edges"]} == {(x["from"], x["to"], x["relation"]) for x in trace["reverse_edges"]})
    check("T02", "traceability", "trace graph stops at obligation", trace["status"] == "PARTIAL_BLOCKED_AT_OBLIGATION" and not trace["requirement_nodes"] and not any(x["relation"] == "DERIVES_REQUIREMENT" for x in trace["forward_edges"]))
    node_ids = {x["node_id"] for x in trace["nodes"]}
    check("T03", "traceability", "all source obligation/property nodes are retained", set(O) <= node_ids and set(P) <= node_ids)
    check("T04", "traceability", "source/evidence provenance edges are present", any(x["relation"] == "SUPPORTS" for x in trace["forward_edges"]) and any(x["relation"] == "SUPPORTS_PROPERTY" for x in trace["forward_edges"]) and any(x["relation"] == "SUPPORTS_OBLIGATION" for x in trace["forward_edges"]))
    check("V01", "verification", "upstream tests remain unverified", verification["upstream_obligation_tests"]["verified"] == 0 and verification["upstream_obligation_tests"]["status"] == "UNVERIFIED_SOURCE")
    check("V02", "verification", "no v11 test result is fabricated", not verification["records"])
    check("V03", "verification", "harness/system failure classes remain distinct", {"HARNESS_FAILURE", "IMPLEMENTATION_FAILURE", "ENVIRONMENT_FAILURE", "TEST_ORACLE_FAILURE", "CONTRACT_VIOLATION"} <= set(verification["failure_taxonomy"]))
    check("V04", "verification", "test existence is not treated as verification", not conformance["claim_allowed"] and conformance["status"] == "BLOCKED")
    check("V05", "verification", "test harness contract defines all required dimensions without altering semantics", set(oracles["test_harness_contract"]["required_dimensions"]) == {"input_generation", "environment", "isolation", "reset", "execution", "observation", "oracle_evaluation", "evidence_capture", "cleanup"} and oracles["test_harness_contract"]["may_silently_alter_tested_semantics"] is False)
    check("V06", "verification", "negative and mutation testing policies remain explicit", "negative-test" in oracles["negative_test_policy"] and "weakening" in oracles["mutation_testing_policy"])

    # Audit and certificate.
    check("S01", "audit", "all protocol failure modes are registered", all(x in audit_text for x in FAILURE_MODES))
    check("S02", "audit", "detected failures are explicit", all(x in audit_text for x in ["ORPHAN_OBLIGATION", "UNRESOLVED_CONFLICT", "UNKNOWN_ESCALATION"]))
    check("S03", "audit", "validation procedure has all 15 ordered steps", all(f"| {i} |" in audit_text for i in range(1, 16)))
    for dimension in ["TRACEABILITY_COMPLETENESS", "SEMANTIC_COMPLETENESS", "VALIDATION_COMPLETENESS", "VERIFICATION_COMPLETENESS", "FAILURE_COMPLETENESS", "SECURITY_COMPLETENESS", "COMPATIBILITY_COMPLETENESS", "IMPLEMENTATION_BOUNDARY_COMPLETENESS"]:
        check("S-" + dimension[:5], "audit", f"completeness dimension is reported: {dimension}", dimension in audit_text)
    check("S12", "audit", "hidden assumptions are explicit", "ASSUMP-001" in audit_text and "ASSUMP-002" in audit_text)
    check("S13", "audit", "future architecture is not used to repair history", "No current architecture or roadmap" in audit_text)
    cert_copy = {k: v for k, v in certificate.items() if k != "certificate_hash"}
    check("CERT-01", "certificate", "certificate hash is valid", certificate["certificate_hash"] == object_hash(cert_copy))
    check("CERT-02", "certificate", "certificate identifies v11 and deterministic unknown timestamp", certificate["specification_version"] == "11.0" and certificate["generated_at"] == "UNKNOWN_NOT_RECORDED_DETERMINISTIC_BUILD")
    check("CERT-03", "certificate", "certificate counts match rejected registries", certificate["requirement_count"] == len(R) == 0 and certificate["rule_count"] == len(RULE) == 0 and certificate["criterion_count"] == len(AC) == 0 and certificate["oracle_count"] == len(ORACLE) == 0)
    check("CERT-04", "certificate", "orphan counts are exact", certificate["orphan_requirement_count"] == 0 and certificate["orphan_obligation_count"] == len(O))
    check("CERT-05", "certificate", "input hashes match input contract", certificate["input_hashes"] == [{"artifact_id": x["artifact_id"], "content_hash": x["content_hash"]} for x in ic["required_inputs"]])
    check("CERT-06", "certificate", "certificate fails rather than overclaims", certificate["validation_status"] == "FAIL" and certificate["derivation_gate"] == "CLOSED")
    check("CERT-07", "certificate", "certificate states its limited semantics", "not proof" in certificate["certificate_semantics"])

    # Schemas.
    schema = {x: load(OUT, "schema/" + x) for x in ["requirement.schema.yaml", "normative-rule.schema.yaml", "acceptance-criterion.schema.yaml", "test-oracle.schema.yaml", "requirement-dependency.schema.yaml", "traceability.schema.yaml", "specification-certificate.schema.yaml"]}
    check("SC01", "schemas", "seven schemas are machine readable and version 1.0", len(schema) == 7 and all(x["schema_version"] == "1.0" for x in schema.values()))
    check("SC02", "schemas", "requirement schema defines all independent axes", {"requirement_type", "disposition", "strength", "epistemic_status", "lifecycle_status", "scope"} <= set(schema["requirement.schema.yaml"]["properties"]))
    check("SC03", "schemas", "requirement class is not substituted for requirement type", "class" not in schema["requirement.schema.yaml"]["properties"] and set(schema["requirement.schema.yaml"]["properties"]["requirement_type"]["enum"]) == REQUIREMENT_TYPES)
    check("SC04", "schemas", "dependency schema contains direction and relation", {"from_requirement", "to_requirement", "relation", "condition", "reason", "evidence"} <= set(schema["requirement-dependency.schema.yaml"]["required"]))
    check("SC05", "schemas", "certificate status enum is exact", set(schema["specification-certificate.schema.yaml"]["properties"]["validation_status"]["enum"]) == {"PASS", "FAIL", "PARTIAL"})
    canonical_fields = {"requirement_id", "requirement_version", "statement", "requirement_type", "disposition", "strength", "final_category", "epistemic_status", "lifecycle_status", "scope", "conformance_level", "criticality", "source_obligations", "source_properties", "source_evidence", "derivation", "preconditions", "postconditions", "normative_rules", "acceptance_criteria", "test_oracles", "invariants", "transitions", "dependencies", "conflicts", "compatibility", "implementation_boundary", "boundary_model", "exceptions", "assumptions", "verification"}
    check("SC06", "schemas", "requirement schema contains complete independent-axis model", canonical_fields <= set(schema["requirement.schema.yaml"]["required"]))
    check("SC07", "schemas", "conformance criticality and verification level enums are independent", set(schema["requirement.schema.yaml"]["properties"]["conformance_level"]["enum"]) == set(reg["conformance_levels"]) and set(schema["requirement.schema.yaml"]["properties"]["criticality"]["enum"]) == set(reg["criticality_values"]) and set(schema["requirement.schema.yaml"]["properties"]["verification"]["properties"]["verification_level"]["enum"]) == set(reg["verification_levels"]))

    # Reports and deterministic/hygiene gates.
    for i, name in enumerate(REPORTS, 1):
        check(f"M{i:02d}", "reports", f"report carries rejection disposition: {name}", "REJECTED_INVALID_OBLIGATION_PACKAGE" in (OUT / name).read_text(encoding="utf-8"))
    check("H01", "hygiene", "all YAML artifacts parse as JSON-compatible YAML", all(parseable(OUT / x) for x in MACHINE + SCHEMAS))
    check("H02", "hygiene", "authoritative documents are not generator outputs", all("Userscript Discovery Prototype.md" not in x and "Continue Architecture Planning.md" not in x for x in DELIVERABLES))
    check("H03", "hygiene", "no Python cache artifacts exist", not any(HS.rglob("__pycache__")) and not any(HS.rglob("*.pyc")))
    det_path = OUT / "DETERMINISM-VALIDATION.yaml"
    det = load(OUT, "DETERMINISM-VALIDATION.yaml") if det_path.is_file() else {}
    check("H04", "hygiene", "all generator-owned outputs reproduce byte-for-byte", det.get("status") == "PASS" and det.get("summary", {}).get("total") == len(DELIVERABLES) and det.get("summary", {}).get("identical") == len(DELIVERABLES) and {x["path"] for x in det.get("files", [])} == set(DELIVERABLES))
    check("H05", "hygiene", "generator and validator are represented in deterministic source control", (HS / "tools/build_normative_specification.py").is_file() and (HS / "tools/validate_normative_specification.py").is_file())

    blocked("GATE-V11", "acceptance", "v11 normative specification acceptance", "The complete v10.1 input package is rejected: upstream input failed, obligations are unverified, unknowns remain, and conflicts are unresolved.")
    return finish(checks, {"requirements": len(R), "rules": len(RULE), "criteria": len(AC), "oracles": len(ORACLE), "orphan_obligations": len(coverage["orphan_obligations"])})


def parseable(path: Path) -> bool:
    try:
        json.loads(path.read_text(encoding="utf-8")); return True
    except Exception:
        return False


def finish(checks: list[dict[str, str]], counts: dict[str, int]) -> int:
    passed = sum(x["result"] == "PASS" for x in checks)
    failed = sum(x["result"] == "FAIL" for x in checks)
    blocked = sum(x["result"] == "BLOCKED" for x in checks)
    report = {
        "schema_version": "1.0", "specification_version": "11.0",
        "overall_status": "FAIL" if failed else "STRUCTURAL_PASS_INPUT_REJECTED" if blocked else "PASS",
        "acceptance": "VALIDATION_FAILED" if failed else "REJECTED_INVALID_OBLIGATION_PACKAGE" if blocked else "PASS",
        "summary": {"total": len(checks), "passed": passed, "failed": failed, "blocked": blocked},
        "registry_counts": counts, "checks": checks,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "VALIDATION.yaml").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    lines = ["# Protocol-v11 Validation", "", f"**Overall:** `{report['overall_status']}`", f"**Acceptance:** `{report['acceptance']}`", f"**Checks:** {passed} PASS / {failed} FAIL / {blocked} BLOCKED ({len(checks)} total)", "", "A structural pass validates the rejection path. It does not authorize requirement derivation or conformance.", "", "| ID | Category | Result | Description | Detail |", "|---|---|---|---|---|"]
    for x in checks:
        lines.append("| %s | %s | %s | %s | %s |" % (x["check_id"], x["category"], x["result"], x["description"].replace("|", "\\|"), x["detail"].replace("|", "\\|")))
    (OUT / "VALIDATION.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{passed} PASS / {failed} FAIL / {blocked} BLOCKED ({len(checks)} checks); {report['overall_status']}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
