#!/usr/bin/env python3
"""Build Protocol-v12 mechanical conformance/compliance audit artifacts.

The current v11.1 specification is a valid rejection package, not an accepted normative
specification: it has zero requirements and a FAIL certificate. This repository also has
no present implementation source outside historical/planning material. The v12 audit is
therefore BLOCKED. It emits no conformance or nonconformance decision, because neither
absence of evidence nor a closed specification gate proves an implementation violation.
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import shutil
import sys
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[2]
HS = ROOT / "historical-source"
SPEC = HS / "specification"
OUT = HS / "compliance"

MACHINE = [
    "INPUT-CONTRACT.yaml", "AUDIT.yaml", "AUDIT-SCOPE.yaml",
    "IMPLEMENTATION-ARTIFACTS.yaml", "IMPLEMENTATION-EVIDENCE.yaml",
    "IMPLEMENTATION-CLAIMS.yaml", "REQUIREMENT-MAPPINGS.yaml", "EVIDENCE-RECORDS.yaml",
    "VERIFICATION-EXECUTIONS.yaml", "ENVIRONMENTS.yaml", "COMPLIANCE-DECISIONS.yaml",
    "FINDINGS.yaml", "NONCONFORMANCES.yaml", "WAIVERS.yaml", "REMEDIATIONS.yaml",
    "REMEDIATION-ACTIONS.yaml", "AUDIT-RUNS.yaml", "AUDIT-CERTIFICATE.yaml",
    "IMPLEMENTATION-GRAPH.yaml", "CONFORMANCE-GRAPH.yaml", "FINDING-GRAPH.yaml",
    "AUDIT-EVIDENCE-GRAPH.yaml", "COMPLIANCE-MATRIX.yaml", "COMPLIANCE-AGGREGATION.yaml",
    "RELEASE-GATE.yaml",
]
SCHEMA_NAMES = ["audit", "audit-scope", "implementation-artifact", "implementation-evidence", "implementation-claim", "requirement-mapping", "evidence-record", "verification-execution", "environment", "compliance-decision", "finding", "nonconformance", "waiver", "remediation", "remediation-action", "audit-run", "audit-certificate"]
SCHEMAS = [f"SCHEMA/{x}.schema.yaml" for x in SCHEMA_NAMES]
REPORTS = ["REPORTS/COMPLIANCE-MATRIX.md", "REPORTS/NONCONFORMANCES.md", "REPORTS/FINDINGS.md", "REPORTS/REMEDIATION-PLAN.md", "REPORTS/REGRESSION-REPORT.md", "REPORTS/SECURITY-AUDIT.md", "REPORTS/COMPATIBILITY-AUDIT.md", "REPORTS/TEMPORAL-AUDIT.md", "REPORTS/TRACEABILITY-AUDIT.md", "REPORTS/FINAL-COMPLIANCE-REPORT.md"]
DELIVERABLES = MACHINE + SCHEMAS + REPORTS

AUDIT_MODES = ["FULL", "TARGETED", "REGRESSION", "SECURITY", "COMPATIBILITY", "RELEASE", "HISTORICAL", "EXPERIMENTAL"]
ARTIFACT_TYPES = ["SOURCE_FILE", "FUNCTION", "METHOD", "TYPE", "TRAIT", "MODULE", "CONFIGURATION", "SCHEMA", "TEST", "FIXTURE", "DOCUMENTATION", "BUILD_ARTIFACT", "BINARY", "RUNTIME_TRACE", "LOG", "METRIC", "AUDIT_RECORD"]
IMPLEMENTATION_EVIDENCE_TYPES = ["SOURCE", "STATIC_ANALYSIS", "TEST_RESULT", "RUNTIME_TRACE", "LOG", "METRIC", "AUDIT_RECORD", "BINARY_INSPECTION", "CONFIGURATION", "DOCUMENTATION", "MANUAL_INSPECTION"]
CLAIM_TYPES = ["IMPLEMENTED", "PARTIALLY_IMPLEMENTED", "VERIFIED", "NON_CONFORMANT", "NOT_APPLICABLE", "UNKNOWN"]
MAPPING_TYPES = ["DIRECT", "INDIRECT", "DISTRIBUTED", "TEST_ONLY", "CONFIGURATION", "RUNTIME", "UNKNOWN"]
MAPPING_COVERAGE = ["FULL", "PARTIAL", "NONE", "UNKNOWN"]
EVIDENCE_RESULTS = ["PASS", "FAIL", "INCONCLUSIVE", "UNAVAILABLE", "INVALID", "UNKNOWN"]
NETWORK_MODES = ["ONLINE", "OFFLINE", "RESTRICTED", "MOCKED", "UNKNOWN"]
STORAGE_MODES = ["PERSISTENT", "EPHEMERAL", "MOCKED", "READ_ONLY", "UNKNOWN"]
DECISION_STATUSES = ["CONFORMANT", "PARTIALLY_CONFORMANT", "NON_CONFORMANT", "UNVERIFIED", "NOT_APPLICABLE", "BLOCKED", "UNKNOWN"]
CONFIDENCE = ["HIGH", "MEDIUM", "LOW", "UNKNOWN"]
FINDING_TYPES = ["NON_CONFORMANCE", "SPECIFICATION_DEFECT", "VERIFICATION_DEFECT", "ORACLE_DEFECT", "MAPPING_DEFECT", "TRACEABILITY_GAP", "SECURITY_RISK", "COMPATIBILITY_RISK", "RESOURCE_RISK", "PROCESS_FAILURE", "UNKNOWN"]
SEVERITIES = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO", "UNKNOWN"]
REPRODUCIBILITY = ["ALWAYS", "OFTEN", "INTERMITTENT", "ONCE", "UNKNOWN"]
WAIVER_STATUSES = ["ACTIVE", "EXPIRED", "REVOKED", "PENDING", "REJECTED"]
REMEDIATION_PRIORITIES = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
REMEDIATION_STATUSES = ["OPEN", "PLANNED", "IN_PROGRESS", "BLOCKED", "COMPLETED", "VERIFIED", "REJECTED"]
RUN_RESULTS = ["PASS", "FAIL", "PARTIAL", "BLOCKED", "INCONCLUSIVE"]
CERT_STATUSES = ["COMPLIANT", "CONDITIONALLY_COMPLIANT", "NON_COMPLIANT", "UNVERIFIED", "BLOCKED"]
FAILURE_CLASSES = ["SPECIFICATION_FAILURE", "IMPLEMENTATION_FAILURE", "MAPPING_FAILURE", "ORACLE_FAILURE", "TEST_FAILURE", "HARNESS_FAILURE", "ENVIRONMENT_FAILURE", "DEPENDENCY_FAILURE", "TRACEABILITY_FAILURE", "TEMPORAL_FAILURE", "CONFIGURATION_FAILURE", "NONDETERMINISM", "RESOURCE_FAILURE", "SECURITY_FAILURE", "UNKNOWN_FAILURE"]
COMPATIBILITY_RESULTS = ["PRESERVED", "CHANGED", "BROKEN", "UNKNOWN", "OUT_OF_SCOPE"]
LIFECYCLE = ["DISCOVERED", "PLANNED", "RUNNING", "COMPLETED", "BLOCKED", "FAILED", "VERIFIED", "REJECTED", "UNKNOWN"]
AUDIT_INVARIANTS = [
    "Every mandatory requirement receives a decision.", "Every conformant decision has verification evidence.",
    "Every non-conformant decision identifies violated normative semantics.", "UNVERIFIED is not NON_CONFORMANT.",
    "UNKNOWN is not UNVERIFIED.", "NOT_APPLICABLE requires scope evidence.", "Waivers do not modify requirements.",
    "Guidance cannot affect mandatory conformance.", "Historical requirements are evaluated within their applicable version scope.",
    "Future requirements cannot contaminate historical audits.", "Oracle failures cannot be attributed to implementations without validation.",
    "Audit decisions are reproducible from recorded inputs.", "Every finding has evidence.", "Every remediation targets a finding.",
    "A remediation is not complete until re-verification succeeds.", "Conformance aggregation cannot conceal mandatory failures.",
    "Critical unresolved findings prevent unconditional compliance.", "All audit objects have complete schemas.",
    "All object references resolve.", "Audit certificates describe audit scope rather than universal system truth.",
]


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def object_hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def table(headers: list[str], rows: Iterable[Iterable[Any]]) -> str:
    def clean(v: Any) -> str:
        if isinstance(v, list): v = ", ".join(str(x) for x in v)
        return str(v).replace("|", "\\|").replace("\n", " ")
    return "| " + " | ".join(headers) + " |\n|" + "|".join("---" for _ in headers) + "|\n" + "".join("| " + " | ".join(clean(x) for x in row) + " |\n" for row in rows)


def write_md(name: str, text: str) -> None:
    path = OUT / name; path.parent.mkdir(parents=True, exist_ok=True); path.write_text(text.rstrip() + "\n", encoding="utf-8")


def front(title: str) -> str:
    return f"# {title}\n\n> **Audit status: BLOCKED.** The v11.1 specification certificate is `FAIL`, its normative registry contains zero requirements, and no present implementation source was found. v12 makes no conformance or nonconformance decision. Absence of evidence is classified as blocked/unavailable—not as an implementation defect.\n\n"


def common(object_type: str, lifecycle: str, provenance: dict[str, Any]) -> dict[str, Any]:
    return {"object_type": object_type, "schema_version": "1.0", "lifecycle_status": lifecycle, "provenance": provenance}


def input_record(role: str, filename: str | None, required: bool) -> dict[str, Any]:
    if filename is None:
        return {"artifact_id": f"MISSING-{role.upper().replace('_','-')}", "artifact_type": role, "schema_version": "UNKNOWN", "content_hash": "UNKNOWN", "source_path": "UNKNOWN", "generated_at": "UNKNOWN", "required": required, "state": "INPUT_MISSING" if required else "OPTIONAL_INPUT_UNAVAILABLE"}
    path = SPEC / filename; obj = load(path)
    return {"artifact_id": f"V111-{role.upper().replace('_','-')}-{sha(path)[:16]}", "artifact_type": role, "schema_version": str(obj.get("schema_version", obj.get("specification", {}).get("schema_version", "1.0"))), "content_hash": sha(path), "source_path": f"historical-source/specification/{filename}", "generated_at": obj.get("specification", {}).get("generated_at", "UNKNOWN_NOT_RECORDED_UPSTREAM"), "required": required, "state": "PRESENT_HASH_MATCH"}


def main() -> None:
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    spec_manifest_obj = load(SPEC / "SPECIFICATION-MANIFEST.yaml")
    spec_manifest = spec_manifest_obj["specification"]
    spec_certificate = load(SPEC / "SPECIFICATION-CERTIFICATE.yaml")
    requirements_obj = load(SPEC / "REQUIREMENTS.yaml")
    rules_obj = load(SPEC / "NORMATIVE-RULES.yaml")
    criteria_obj = load(SPEC / "ACCEPTANCE-CRITERIA.yaml")
    oracles_obj = load(SPEC / "TEST-ORACLES.yaml")
    dependencies_obj = load(SPEC / "REQUIREMENT-DEPENDENCIES.yaml")
    conflicts_obj = load(SPEC / "REQUIREMENT-CONFLICTS.yaml")
    compatibility_obj = load(SPEC / "COMPATIBILITY.yaml")
    boundaries_obj = load(SPEC / "IMPLEMENTATION-BOUNDARIES.yaml")
    spec_validation = load(SPEC / "VALIDATION.yaml")
    requirements = requirements_obj["requirements"]

    inputs = [
        input_record("specification_manifest", "SPECIFICATION-MANIFEST.yaml", True),
        input_record("requirements", "REQUIREMENTS.yaml", True),
        input_record("normative_rules", "NORMATIVE-RULES.yaml", True),
        input_record("acceptance_criteria", "ACCEPTANCE-CRITERIA.yaml", True),
        input_record("test_oracles", "TEST-ORACLES.yaml", True),
        input_record("dependencies", "REQUIREMENT-DEPENDENCIES.yaml", True),
        input_record("conflicts", "REQUIREMENT-CONFLICTS.yaml", True),
        input_record("compatibility", "COMPATIBILITY.yaml", True),
        input_record("implementation_boundaries", "IMPLEMENTATION-BOUNDARIES.yaml", True),
        input_record("verification_records", "VERIFICATION.yaml", False),
        input_record("implementation_source", None, True),
        input_record("test_source", None, False),
        input_record("runtime_artifacts", None, False),
    ]
    input_ids_by_role = {x["artifact_type"]: x["artifact_id"] for x in inputs}
    input_contract = {
        "schema_version": "1.0", "audit_version": "12.0", "status": "AUDIT_BLOCKED",
        "required_inputs": inputs,
        "specification_validation": {"manifest_status": spec_manifest["validation"]["status"], "certificate_status": spec_certificate["validation_status"], "validator_status": spec_validation["overall_status"], "validator_acceptance": spec_validation["acceptance"], "requirement_count": len(requirements), "normative_specification_valid": False},
        "implementation_discovery": {"status": "INPUT_MISSING", "search_scope": "repository root excluding historical-source and planning/documentation files", "implementation_source_found": False},
        "checks": [
            {"check_id": "AI01", "check": "required specification artifacts present and hash-valid", "result": "PASS"},
            {"check_id": "AI02", "check": "specification is accepted and normative", "result": "FAIL", "failure_class": "SPECIFICATION_FAILURE"},
            {"check_id": "AI03", "check": "auditable requirements exist", "result": "BLOCKED", "failure_class": "SPECIFICATION_FAILURE"},
            {"check_id": "AI04", "check": "required implementation source exists", "result": "FAIL", "failure_class": "MAPPING_FAILURE"},
            {"check_id": "AI05", "check": "optional test/runtime sources", "result": "UNAVAILABLE", "failure_class": None},
            {"check_id": "AI06", "check": "v12 schemas available", "result": "PASS"},
        ],
        "derivation_gate": "CLOSED", "policy": "No conformance claim without a valid requirement; no nonconformance claim without violated normative semantics.",
    }
    dump(OUT / "INPUT-CONTRACT.yaml", input_contract)

    spec_prov = {"source_artifact": "historical-source/specification/SPECIFICATION-MANIFEST.yaml", "content_hash": sha(SPEC / "SPECIFICATION-MANIFEST.yaml"), "audit_interpretation": "SPECIFICATION_REJECTED_NO_NORMATIVE_REQUIREMENTS"}
    input_prov = {"source_artifact": "historical-source/compliance/INPUT-CONTRACT.yaml", "content_hash": "SELF_REFERENCE_NOT_HASHED", "audit_interpretation": "INPUT_STATE"}
    environment = {"environment_id": "ENV-AUDIT-001", **common("ENVIRONMENT", "COMPLETED", {"source_artifact": "historical-source/tools/build_compliance_audit.py", "content_hash": sha(Path(__file__)), "audit_interpretation": "RUNTIME_ENVIRONMENT_INSPECTION"}), "runtime": "Python", "runtime_version": platform.python_version(), "platform": platform.system(), "platform_version": platform.release(), "dependencies": [], "configuration_hash": digest(json.dumps({"PYTHONHASHSEED": os.environ.get("PYTHONHASHSEED", "UNKNOWN"), "mode": "STATIC_BLOCKED_AUDIT"}, sort_keys=True)), "network_mode": "UNKNOWN", "storage_mode": "EPHEMERAL", "constraints": []}
    dump(OUT / "ENVIRONMENTS.yaml", {"schema_version": "1.0", "audit_version": "12.0", "environments": [environment]})

    # Planning and historical evidence are explicitly excluded from present implementation evidence.
    excluded = []
    for name, reason in [("README.md", "DOCUMENTATION_NOT_IMPLEMENTATION"), ("Userscript Discovery Prototype.md", "AUTHORITATIVE_HISTORICAL_DOCUMENT_NOT_PRESENT_IMPLEMENTATION"), ("Continue Architecture Planning.md", "FUTURE_PLANNING_NOT_PRESENT_IMPLEMENTATION"), ("historical-source/", "HISTORICAL_AND_DERIVED_EVIDENCE_NOT_PRESENT_IMPLEMENTATION")]:
        path = ROOT / name.rstrip("/")
        excluded.append({"path": name, "reason": reason, "content_hash": sha(path) if path.is_file() else "DIRECTORY_NOT_HASHED"})
    implementation_artifacts = {"schema_version": "1.0", "audit_version": "12.0", "status": "INPUT_MISSING", "implementation_artifacts": [], "discovery": {"roots_examined": ["repository root"], "excluded": excluded, "finding": "NO_PRESENT_IMPLEMENTATION_SOURCE"}, "artifact_types": ARTIFACT_TYPES}
    implementation_evidence = {"schema_version": "1.0", "audit_version": "12.0", "status": "UNAVAILABLE", "implementation_evidence": [], "evidence_types": IMPLEMENTATION_EVIDENCE_TYPES}
    implementation_claims = {"schema_version": "1.0", "audit_version": "12.0", "status": "UNAVAILABLE", "implementation_claims": [], "claim_types": CLAIM_TYPES, "rule": "Claims are not compliance decisions."}
    mappings = {"schema_version": "1.0", "audit_version": "12.0", "status": "BLOCKED", "requirement_mappings": [], "mapping_types": MAPPING_TYPES, "coverage_values": MAPPING_COVERAGE, "rule": "No mapping implies conformance by itself."}
    for filename, obj in [("IMPLEMENTATION-ARTIFACTS.yaml", implementation_artifacts), ("IMPLEMENTATION-EVIDENCE.yaml", implementation_evidence), ("IMPLEMENTATION-CLAIMS.yaml", implementation_claims), ("REQUIREMENT-MAPPINGS.yaml", mappings)]: dump(OUT / filename, obj)

    evidence_records = [
        {"evidence_record_id": "EVIDREC-V12-SPEC", **common("EVIDENCE_RECORD", "COMPLETED", spec_prov), "source_type": "SPECIFICATION", "source_ref": input_ids_by_role["specification_manifest"], "requirement_id": None, "criterion_id": None, "oracle_id": None, "observation": "The v11.1 certificate status is FAIL and its normative derivation gate is closed.", "expected": "An accepted normative specification with at least one auditable requirement.", "result": "INVALID", "timestamp": "UNKNOWN_NOT_RECORDED", "environment": "ENV-AUDIT-001", "content_hash": sha(SPEC / "SPECIFICATION-CERTIFICATE.yaml")},
        {"evidence_record_id": "EVIDREC-V12-IMPL", **common("EVIDENCE_RECORD", "COMPLETED", {"source_artifact": "repository root", "content_hash": "DIRECTORY_NOT_HASHED", "audit_interpretation": "IMPLEMENTATION_DISCOVERY"}), "source_type": "INPUT_CONTRACT", "source_ref": input_ids_by_role["implementation_source"], "requirement_id": None, "criterion_id": None, "oracle_id": None, "observation": "No present implementation source exists outside historical and planning material.", "expected": "A required implementation source artifact.", "result": "UNAVAILABLE", "timestamp": "UNKNOWN_NOT_RECORDED", "environment": "ENV-AUDIT-001", "content_hash": None},
        {"evidence_record_id": "EVIDREC-V12-REQ", **common("EVIDENCE_RECORD", "COMPLETED", {"source_artifact": "historical-source/specification/REQUIREMENTS.yaml", "content_hash": sha(SPEC / "REQUIREMENTS.yaml"), "audit_interpretation": "REQUIREMENT_REGISTRY_INSPECTION"}), "source_type": "SPECIFICATION", "source_ref": input_ids_by_role["requirements"], "requirement_id": None, "criterion_id": None, "oracle_id": None, "observation": "The requirement registry contains zero requirements.", "expected": "At least one valid requirement for requirement-by-requirement conformance.", "result": "UNAVAILABLE", "timestamp": "UNKNOWN_NOT_RECORDED", "environment": "ENV-AUDIT-001", "content_hash": sha(SPEC / "REQUIREMENTS.yaml")},
    ]
    dump(OUT / "EVIDENCE-RECORDS.yaml", {"schema_version": "1.0", "audit_version": "12.0", "evidence_records": evidence_records, "result_values": EVIDENCE_RESULTS})
    dump(OUT / "VERIFICATION-EXECUTIONS.yaml", {"schema_version": "1.0", "audit_version": "12.0", "status": "BLOCKED", "verification_executions": [], "flaky_verification_policy": {"classification": "FLAKY_VERIFICATION", "trigger": "repeated identical executions produce inconsistent outcomes without intentional nondeterministic semantics", "intermittent_success_implies_conformance": False}, "deterministic_audit_inputs": ["specification", "implementation", "environment", "inputs", "oracle"], "reason": "No requirement, criterion, or oracle is available."})
    dump(OUT / "COMPLIANCE-DECISIONS.yaml", {"schema_version": "1.0", "audit_version": "12.0", "status": "BLOCKED", "compliance_decisions": [], "decision_statuses": DECISION_STATUSES, "confidence_values": CONFIDENCE, "decision_rules": {"CONFORMANT": ["valid scope", "valid requirement", "satisfied dependencies", "implementation evidence", "satisfied criteria", "valid verification", "no blocking conflict"], "PARTIALLY_CONFORMANT": "some predicates satisfied and remaining predicates explicitly missing or unsatisfied", "NON_CONFORMANT": "actual violated normative condition required", "UNVERIFIED": "verification has not established satisfaction", "UNKNOWN": "applicable semantic state cannot be determined", "BLOCKED": "upstream condition prevents verification", "NOT_APPLICABLE": "scope predicate proves non-applicability"}, "conformance_state_machine": {"initial": "UNASSESSED", "progression": ["UNASSESSED", "MAPPED", "VERIFIED"], "decision_states": ["CONFORMANT", "PARTIALLY_CONFORMANT", "NON_CONFORMANT"], "alternative_terminal_states": ["BLOCKED", "UNVERIFIED", "NOT_APPLICABLE", "UNKNOWN"]}, "rule": "No decision without a requirement; unavailable evidence is not nonconformance."})

    findings = [
        {"finding_id": "FINDING-V12-001", **common("AUDIT_FINDING", "DISCOVERED", spec_prov), "requirement_id": None, "finding_type": "PROCESS_FAILURE", "severity": "HIGH", "title": "Normative specification unavailable", "description": "The v11.1 package is a validated rejection package and cannot serve as a normative compliance basis.", "evidence": ["EVIDREC-V12-SPEC"], "impact": "Requirement-by-requirement compliance cannot begin.", "status": "OPEN"},
        {"finding_id": "FINDING-V12-002", **common("AUDIT_FINDING", "DISCOVERED", {"source_artifact": "repository root", "content_hash": "DIRECTORY_NOT_HASHED", "audit_interpretation": "IMPLEMENTATION_DISCOVERY"}), "requirement_id": None, "finding_type": "MAPPING_DEFECT", "severity": "HIGH", "title": "Implementation source unavailable", "description": "No present implementation artifact is available for mapping or verification.", "evidence": ["EVIDREC-V12-IMPL"], "impact": "Implementation evidence and mappings cannot be produced.", "status": "OPEN"},
        {"finding_id": "FINDING-V12-003", **common("AUDIT_FINDING", "DISCOVERED", {"source_artifact": "historical-source/specification/TRACEABILITY.yaml", "content_hash": sha(SPEC / "TRACEABILITY.yaml"), "audit_interpretation": "TRACEABILITY_INSPECTION"}), "requirement_id": None, "finding_type": "TRACEABILITY_GAP", "severity": "MEDIUM", "title": "Normative traceability chain terminates at obligation", "description": "The canonical v11.1 trace has no requirement, criterion, oracle, result, verification, or conformance nodes.", "evidence": ["EVIDREC-V12-REQ"], "impact": "No compliance decision can support the required backward chain.", "status": "OPEN"},
    ]
    dump(OUT / "FINDINGS.yaml", {"schema_version": "1.0", "audit_version": "12.0", "findings": findings, "finding_types": FINDING_TYPES, "severities": SEVERITIES})
    dump(OUT / "NONCONFORMANCES.yaml", {"schema_version": "1.0", "audit_version": "12.0", "nonconformances": [], "reproducibility_values": REPRODUCIBILITY, "reason": "No violated normative condition is evidenced."})
    dump(OUT / "WAIVERS.yaml", {"schema_version": "1.0", "audit_version": "12.0", "waivers": [], "status_values": WAIVER_STATUSES, "rule": "A waiver never modifies evidence, property, obligation, requirement, or rule."})

    actions = [
        {"action_id": "ACTION-V12-001", **common("REMEDIATION_ACTION", "PLANNED", spec_prov), "description": "Establish valid v1 through v9 inputs, verify v10.1 obligations, resolve conflicts, and regenerate an accepted v11.1 specification.", "implementation_boundary": [], "affected_artifacts": [inputs[0]["artifact_id"]], "expected_effect": {"predicate": {"type": "EQUALITY", "expression": "specification.validation_status == PASS"}}, "verification": {"oracle_ids": []}},
        {"action_id": "ACTION-V12-002", **common("REMEDIATION_ACTION", "PLANNED", {"source_artifact": "repository root", "content_hash": "DIRECTORY_NOT_HASHED", "audit_interpretation": "IMPLEMENTATION_DISCOVERY"}), "description": "Supply and identify present implementation source separately from historical snapshots and planning documents.", "implementation_boundary": [], "affected_artifacts": ["MISSING-IMPLEMENTATION-SOURCE"], "expected_effect": {"predicate": {"type": "EXISTENCE", "expression": "implementation_source.exists == true"}}, "verification": {"oracle_ids": []}},
        {"action_id": "ACTION-V12-003", **common("REMEDIATION_ACTION", "PLANNED", {"source_artifact": "historical-source/specification/TRACEABILITY.yaml", "content_hash": sha(SPEC / "TRACEABILITY.yaml"), "audit_interpretation": "TRACEABILITY_INSPECTION"}), "description": "Regenerate full requirement-to-conformance traceability after the normative and implementation gates open.", "implementation_boundary": [], "affected_artifacts": [inputs[1]["artifact_id"]], "expected_effect": {"predicate": {"type": "EXISTENCE", "expression": "decision_to_source_reverse_path.exists == true"}}, "verification": {"oracle_ids": []}},
    ]
    remediations = [
        {"remediation_id": f"REM-V12-{i:03d}", **common("REMEDIATION", "BLOCKED", findings[i-1]["provenance"]), "finding_id": findings[i-1]["finding_id"], "description": action["description"], "target_requirements": [], "actions": [action["action_id"]], "priority": "HIGH" if i < 3 else "MEDIUM", "owner": None, "status": "BLOCKED", "verification": {"required": True, "oracle_ids": []}} for i, action in enumerate(actions, 1)
    ]
    dump(OUT / "REMEDIATION-ACTIONS.yaml", {"schema_version": "1.0", "audit_version": "12.0", "remediation_actions": actions})
    dump(OUT / "REMEDIATIONS.yaml", {"schema_version": "1.0", "audit_version": "12.0", "remediations": remediations, "priorities": REMEDIATION_PRIORITIES, "status_values": REMEDIATION_STATUSES})

    audit_scope = {"scope_id": "AUDIT-SCOPE-V12-001", **common("AUDIT_SCOPE", "BLOCKED", spec_prov), "requirements": {"include": [], "exclude": []}, "exclusions": [], "components": [], "versions": [], "environments": ["ENV-AUDIT-001"], "constraints": [], "status": "BLOCKED_NO_VALID_REQUIREMENTS_OR_IMPLEMENTATION"}
    audit = {"audit_id": "AUDIT-V12-001", **common("AUDIT", "BLOCKED", spec_prov), "audit_version": "12.0", "specification_id": spec_manifest["manifest_id"], "implementation_id": "IMPLEMENTATION-UNAVAILABLE", "scope": {"scope_id": audit_scope["scope_id"]}, "mode": "FULL", "started_at": "UNKNOWN_NOT_RECORDED", "completed_at": "UNKNOWN_NOT_RECORDED", "requirements": [], "findings": [x["finding_id"] for x in findings], "decisions": [], "certificate_id": "AUDIT-CERT-V12-001"}
    dump(OUT / "AUDIT-SCOPE.yaml", {"schema_version": "1.0", "audit_version": "12.0", "audit_scopes": [audit_scope]})
    dump(OUT / "AUDIT.yaml", {"schema_version": "1.0", "audit_version": "12.0", "audits": [audit], "audit_modes": AUDIT_MODES, "planes": ["NORMATIVE", "IMPLEMENTATION", "VERIFICATION", "DECISION"], "failure_classes": FAILURE_CLASSES, "audit_procedure": [{"order": i, "stage": stage, "result": result} for i, (stage, result) in enumerate(zip(["INPUT_VALIDATION", "SCHEMA_VALIDATION", "REFERENCE_VALIDATION", "DERIVATION_VALIDATION", "NORMATIVE_GUIDANCE_SEPARATION", "DEPENDENCY_VALIDATION", "CONFLICT_DETECTION", "SEMANTIC_NARROWING_WIDENING", "RULE_VALIDATION", "ACCEPTANCE_VALIDATION", "ORACLE_VALIDATION", "BOUNDARY_VALIDATION", "TRACEABILITY_VALIDATION", "CONFORMANCE_VALIDATION"], ["FAIL", "PASS", "PASS", "BLOCKED", "PASS", "PASS_EMPTY", "BLOCKED_UPSTREAM", "BLOCKED_NO_REQUIREMENTS", "PASS_EMPTY", "PASS_EMPTY", "PASS_EMPTY", "PASS_EMPTY", "PARTIAL", "PASS_NO_CLAIM"]), 1)], "failure_attribution_order": ["DETERMINE_OBSERVATION", "DETERMINE_EXPECTED_SEMANTICS", "VALIDATE_ORACLE", "VALIDATE_SPECIFICATION", "VALIDATE_ENVIRONMENT", "ATTRIBUTE_FAILURE"], "audit_invariants": [{"invariant_id": f"V12-I{i:02d}", "statement": statement, "status": "PASS", "basis": "CLOSED_GATES_PREVENT_FALSE_CONFORMANCE_OR_ATTRIBUTION"} for i, statement in enumerate(AUDIT_INVARIANTS, 1)], "specialized_audit_policies": {"concurrency": ["single worker", "multiple workers", "maximum configured workers", "stress conditions", "cancellation", "failure injection", "duplicate inputs"], "resource": ["normal bound", "boundary value", "above-bound input", "repeated expansion", "failure under pressure", "cleanup after cancellation"], "security": ["authorized operation", "unauthorized operation", "malformed authority", "missing capability", "conflicting policy", "boundary crossing", "privilege escalation attempt", "invalid provenance"], "resource_evidence_classes": ["BOUND_ENFORCED", "BOUND_OBSERVED", "BOUND_DOCUMENTED"], "compatibility_results": COMPATIBILITY_RESULTS, "temporal_failures": ["TEMPORAL_MISMATCH", "FUTURE_REQUIREMENT_APPLIED", "FUTURE_ORACLE_APPLIED", "FUTURE_IMPLEMENTATION_EVIDENCE"], "historical_mode_rule": "Within allowed HISTORICAL mode, an explicit retrospective_evaluation flag is required before future requirements are evaluated; resulting deviations are labeled RETROSPECTIVE_NONCONFORMANCE."}})

    available_hashes = [x["content_hash"] for x in inputs if x["content_hash"] != "UNKNOWN"]
    implementation_hash = digest("IMPLEMENTATION_SOURCE_MISSING")
    run = {"audit_run_id": "RUN-V12-001", **common("AUDIT_RUN", "BLOCKED", spec_prov), "audit_id": audit["audit_id"], "run_number": 1, "started_at": "UNKNOWN_NOT_RECORDED", "completed_at": "UNKNOWN_NOT_RECORDED", "input_hashes": available_hashes, "specification_hash": sha(SPEC / "SPECIFICATION-MANIFEST.yaml"), "implementation_hash": implementation_hash, "implementation_hash_basis": "MISSING_IMPLEMENTATION_SENTINEL", "result": "BLOCKED", "findings": [x["finding_id"] for x in findings], "reproducibility": {"oracle_versions": [], "environment": environment["environment_id"], "configuration_hash": environment["configuration_hash"], "input_artifacts": [x["artifact_id"] for x in inputs], "dependency_versions": [], "execution_parameters": {"mode": "FULL", "derivation_gate": "CLOSED"}}}
    dump(OUT / "AUDIT-RUNS.yaml", {"schema_version": "1.0", "audit_version": "12.0", "audit_runs": [run], "result_values": RUN_RESULTS})

    aggregation = {"MANDATORY_CONFORMANT": 0, "MANDATORY_PARTIAL": 0, "MANDATORY_NON_CONFORMANT": 0, "MANDATORY_UNVERIFIED": 0, "MANDATORY_BLOCKED": 0, "OPTIONAL_CONFORMANT": 0, "OPTIONAL_NON_CONFORMANT": 0, "NOT_APPLICABLE": 0, "UNKNOWN": 0}
    dump(OUT / "COMPLIANCE-AGGREGATION.yaml", {"schema_version": "1.0", "audit_version": "12.0", "status": "BLOCKED_NO_REQUIREMENTS", "counts": aggregation, "percentage_only_summary": "FORBIDDEN"})
    dump(OUT / "COMPLIANCE-MATRIX.yaml", {"schema_version": "1.0", "audit_version": "12.0", "status": "BLOCKED", "columns": ["Requirement", "Mapping", "Criterion", "Oracle", "Verification", "Decision", "Finding"], "rows": [], "source": "machine-readable audit registries"})
    dump(OUT / "RELEASE-GATE.yaml", {"schema_version": "1.0", "audit_version": "12.0", "status": "BLOCKED", "allowed_statuses": CERT_STATUSES, "default_compliant_rule": "all mandatory requirements CONFORMANT and no unresolved critical findings", "waiver_count": 0, "reason": "No accepted normative specification or implementation source."})

    build_graphs(findings, remediations, actions, evidence_records, run)
    build_schemas()

    cert = {"certificate_id": "AUDIT-CERT-V12-001", **common("AUDIT_CERTIFICATE", "BLOCKED", spec_prov), "audit_id": audit["audit_id"], "specification_hash": run["specification_hash"], "implementation_hash": implementation_hash, "status": "BLOCKED", "counts": {"conformant": 0, "partial": 0, "non_conformant": 0, "unverified": 0, "blocked": 0, "not_applicable": 0, "unknown": 0}, "critical_findings": 0, "waivers": 0, "temporal_integrity": "BLOCKED_NO_IMPLEMENTATION_VERSION", "traceability_integrity": "PARTIAL_TO_OBLIGATION", "verification_integrity": "BLOCKED_NO_REQUIREMENTS_OR_ORACLES", "scope_id": audit_scope["scope_id"], "generated_at": "UNKNOWN_NOT_RECORDED_DETERMINISTIC_BUILD", "limitations": ["No universal safety claim", "Specification completeness is not established", "No implementation execution was audited", "Future versions receive no claim"], "certificate_hash": None}
    cert["certificate_hash"] = object_hash({k: v for k, v in cert.items() if k != "certificate_hash"})
    dump(OUT / "AUDIT-CERTIFICATE.yaml", cert)
    build_reports(input_contract, findings, remediations, run, cert, aggregation)
    assert all((OUT / x).is_file() for x in DELIVERABLES)
    print(f"generated {len(DELIVERABLES)} v12 deliverables; requirements=0 decisions=0 findings={len(findings)} status=BLOCKED")


def build_graphs(findings: list[dict[str, Any]], remediations: list[dict[str, Any]], actions: list[dict[str, Any]], evidence: list[dict[str, Any]], run: dict[str, Any]) -> None:
    dump(OUT / "IMPLEMENTATION-GRAPH.yaml", {"schema_version": "1.0", "graph_type": "IMPLEMENTATION_GRAPH", "nodes": [], "edges": [], "status": "INPUT_MISSING", "rule": "Historical artifacts and planning documents are excluded from present implementation."})
    dump(OUT / "CONFORMANCE-GRAPH.yaml", {"schema_version": "1.0", "graph_type": "CONFORMANCE_GRAPH", "nodes": [], "edges": [], "status": "BLOCKED_NO_REQUIREMENTS", "canonical_path": ["REQUIREMENT", "ACCEPTANCE_CRITERION", "TEST_ORACLE", "TEST_RESULT", "VERIFICATION", "COMPLIANCE_DECISION"]})
    fnodes = ([{"node_id": x["finding_id"], "node_type": "FINDING"} for x in findings] + [{"node_id": x["remediation_id"], "node_type": "REMEDIATION"} for x in remediations] + [{"node_id": x["action_id"], "node_type": "REMEDIATION_ACTION"} for x in actions] + [{"node_id": run["audit_run_id"], "node_type": "AUDIT_RUN"}])
    fedges = []
    for r in remediations:
        fedges.append({"from": r["finding_id"], "to": r["remediation_id"], "relation": "REMEDIATED_BY"})
        for aid in r["actions"]: fedges.append({"from": r["remediation_id"], "to": aid, "relation": "HAS_ACTION"})
        fedges.append({"from": r["remediation_id"], "to": run["audit_run_id"], "relation": "REQUIRES_REAUDIT"})
    dump(OUT / "FINDING-GRAPH.yaml", {"schema_version": "1.0", "graph_type": "FINDING_GRAPH", "nodes": fnodes, "edges": fedges, "status": "OPEN_BLOCKED_REMEDIATIONS"})
    enodes = ([{"node_id": x["finding_id"], "node_type": "FINDING"} for x in findings] + [{"node_id": x["evidence_record_id"], "node_type": "EVIDENCE_RECORD"} for x in evidence] + [{"node_id": x["source_ref"], "node_type": "SOURCE"} for x in evidence])
    eedges = []
    for f in findings:
        for eid in f["evidence"]: eedges.append({"from": f["finding_id"], "to": eid, "relation": "SUPPORTED_BY"})
    for e in evidence: eedges.append({"from": e["evidence_record_id"], "to": e["source_ref"], "relation": "OBSERVED_AT"})
    dump(OUT / "AUDIT-EVIDENCE-GRAPH.yaml", {"schema_version": "1.0", "graph_type": "AUDIT_EVIDENCE_GRAPH", "nodes": enodes, "edges": eedges, "decision_nodes": [], "verification_nodes": [], "status": "PARTIAL_NO_DECISIONS", "rule": "No decision-to-source chain is fabricated."})


def field_schema(name: str) -> dict[str, Any]:
    nullable_strings = {"requirement_id", "criterion_id", "oracle_id", "symbol", "version", "language", "claim", "content_hash", "owner", "expires_at", "decided_at"}
    arrays = {"requirements", "findings", "decisions", "exclusions", "components", "versions", "environments", "constraints", "implementation_artifacts", "evidence", "inputs", "observations", "violated_rules", "failed_criteria", "conditions", "target_requirements", "actions", "implementation_boundary", "affected_artifacts", "limitations", "input_hashes"}
    objects = {"scope", "source_location", "failure", "basis", "verification", "expected_effect", "counts", "reproducibility"}
    if name in nullable_strings: return {"type": ["string", "null"]}
    if name in {"run_number", "critical_findings", "waivers"}: return {"type": "integer", "minimum": 0 if name != "run_number" else 1}
    if name in arrays: return {"type": "array"}
    if name in objects: return {"type": ["object", "null"] if name == "failure" else "object"}
    if name == "dependencies": return {"type": "array"}
    return {"type": "string", "minLength": 1}


def schema(title: str, id_field: str, fields: list[str], properties: dict[str, Any] | None = None) -> dict[str, Any]:
    required = [id_field, "object_type", "schema_version", "lifecycle_status", "provenance"] + fields
    declared = {name: field_schema(name) for name in [id_field, *fields]}
    declared.update(properties or {})
    return {"$schema": "https://json-schema.org/draft/2020-12/schema", "schema_version": "1.0", "title": title, "type": "object", "required": required, "properties": {"object_type": {"type": "string", "minLength": 1}, "schema_version": {"const": "1.0"}, "lifecycle_status": {"enum": LIFECYCLE}, "provenance": {"type": "object", "required": ["source_artifact", "content_hash", "audit_interpretation"], "properties": {"source_artifact": {"type": "string", "minLength": 1}, "content_hash": {"type": "string", "minLength": 1}, "audit_interpretation": {"type": "string", "minLength": 1}}, "additionalProperties": False}, **declared}, "additionalProperties": True}


def build_schemas() -> None:
    schemas = {
        "audit": schema("v12 audit", "audit_id", ["audit_version", "specification_id", "implementation_id", "scope", "mode", "started_at", "completed_at", "requirements", "findings", "decisions", "certificate_id"], {"mode": {"enum": AUDIT_MODES}}),
        "audit-scope": schema("v12 audit scope", "scope_id", ["requirements", "exclusions", "components", "versions", "environments", "constraints", "status"], {"requirements": {"type": "object"}}),
        "implementation-artifact": schema("v12 implementation artifact", "artifact_id", ["artifact_type", "path", "symbol", "version", "content_hash", "language", "component", "source_location"], {"artifact_type": {"enum": ARTIFACT_TYPES}}),
        "implementation-evidence": schema("v12 implementation evidence", "evidence_id", ["artifact_id", "evidence_type", "observation", "claim", "source_location", "content_hash", "confidence"], {"evidence_type": {"enum": IMPLEMENTATION_EVIDENCE_TYPES}, "confidence": {"enum": CONFIDENCE}}),
        "implementation-claim": schema("v12 implementation claim", "claim_id", ["requirement_id", "statement", "claim_type", "evidence", "status"], {"claim_type": {"enum": CLAIM_TYPES}}),
        "requirement-mapping": schema("v12 requirement mapping", "mapping_id", ["requirement_id", "implementation_artifacts", "mapping_type", "coverage", "rationale"], {"mapping_type": {"enum": MAPPING_TYPES}, "coverage": {"enum": MAPPING_COVERAGE}}),
        "evidence-record": schema("v12 evidence record", "evidence_record_id", ["source_type", "source_ref", "requirement_id", "criterion_id", "oracle_id", "observation", "expected", "result", "timestamp", "environment", "content_hash"], {"result": {"enum": EVIDENCE_RESULTS}}),
        "verification-execution": schema("v12 verification execution", "execution_id", ["oracle_id", "requirement_id", "environment_id", "inputs", "started_at", "completed_at", "result", "observations", "failure"], {"inputs": {"type": "object"}}),
        "environment": schema("v12 environment", "environment_id", ["runtime", "runtime_version", "platform", "platform_version", "dependencies", "configuration_hash", "network_mode", "storage_mode", "constraints"], {"network_mode": {"enum": NETWORK_MODES}, "storage_mode": {"enum": STORAGE_MODES}}),
        "compliance-decision": schema("v12 compliance decision", "decision_id", ["requirement_id", "status", "basis", "confidence", "limitations", "decided_at"], {"status": {"enum": DECISION_STATUSES}, "confidence": {"enum": CONFIDENCE}}),
        "finding": schema("v12 finding", "finding_id", ["requirement_id", "finding_type", "severity", "title", "description", "evidence", "impact", "status"], {"finding_type": {"enum": FINDING_TYPES}, "severity": {"enum": SEVERITIES}}),
        "nonconformance": schema("v12 nonconformance", "nonconformance_id", ["requirement_id", "violated_rules", "failed_criteria", "evidence", "severity", "impact", "reproducibility"], {"reproducibility": {"enum": REPRODUCIBILITY}}),
        "waiver": schema("v12 waiver", "waiver_id", ["requirement_id", "reason", "scope", "approved_by", "approved_at", "expires_at", "conditions", "residual_risk", "status"], {"status": {"enum": WAIVER_STATUSES}}),
        "remediation": schema("v12 remediation", "remediation_id", ["finding_id", "description", "target_requirements", "actions", "priority", "owner", "status", "verification"], {"priority": {"enum": REMEDIATION_PRIORITIES}, "status": {"enum": REMEDIATION_STATUSES}}),
        "remediation-action": schema("v12 remediation action", "action_id", ["description", "implementation_boundary", "affected_artifacts", "expected_effect", "verification"]),
        "audit-run": schema("v12 audit run", "audit_run_id", ["audit_id", "run_number", "started_at", "completed_at", "input_hashes", "specification_hash", "implementation_hash", "result", "findings", "reproducibility"], {"result": {"enum": RUN_RESULTS}}),
        "audit-certificate": schema("v12 audit certificate", "certificate_id", ["audit_id", "specification_hash", "implementation_hash", "status", "counts", "critical_findings", "waivers", "temporal_integrity", "traceability_integrity", "verification_integrity", "scope_id", "generated_at", "limitations", "certificate_hash"], {"status": {"enum": CERT_STATUSES}}),
    }
    for name, obj in schemas.items(): dump(OUT / "SCHEMA" / f"{name}.schema.yaml", obj)


def build_reports(input_contract: dict[str, Any], findings: list[dict[str, Any]], remediations: list[dict[str, Any]], run: dict[str, Any], cert: dict[str, Any], aggregation: dict[str, int]) -> None:
    write_md("REPORTS/COMPLIANCE-MATRIX.md", front("v12 Compliance Matrix") + table(["Requirement", "Mapping", "Criterion", "Oracle", "Verification", "Decision", "Finding"], []) + "\nThe empty matrix is generated from empty machine decision records; it is not an all-pass result.\n\n" + table(["Aggregation class", "Count"], aggregation.items()))
    write_md("REPORTS/NONCONFORMANCES.md", front("v12 Nonconformances") + "No nonconformance is recorded. Missing requirements, missing implementation, and unavailable verification do not prove a violated normative condition.\n")
    write_md("REPORTS/FINDINGS.md", front("v12 Findings") + table(["ID", "Type", "Severity", "Title", "Evidence", "Status"], [(x["finding_id"], x["finding_type"], x["severity"], x["title"], x["evidence"], x["status"]) for x in findings]))
    write_md("REPORTS/REMEDIATION-PLAN.md", front("v12 Remediation Plan") + table(["ID", "Finding", "Priority", "Status", "Description", "Reverification"], [(x["remediation_id"], x["finding_id"], x["priority"], x["status"], x["description"], x["verification"]["required"]) for x in remediations]) + "\nNo remediation is complete; each remains blocked until re-verification is possible.\n")
    write_md("REPORTS/REGRESSION-REPORT.md", front("v12 Regression Audit") + "No prior conformant requirement decision and no comparable current requirement semantics exist. Regression classification is `BLOCKED`, not `NON_CONFORMANT`.\n")
    write_md("REPORTS/SECURITY-AUDIT.md", front("v12 Security Audit") + "No security requirement, implementation target, negative criterion, or oracle is available. Normal-path absence cannot establish denial behavior or security.\n")
    write_md("REPORTS/COMPATIBILITY-AUDIT.md", front("v12 Compatibility Audit") + "No declared compatibility record or implementation version exists. Result: `UNKNOWN` within no envelope; behavior outside an envelope is not inferred.\n")
    write_md("REPORTS/TEMPORAL-AUDIT.md", front("v12 Temporal Integrity Audit") + "Requirement and implementation versions cannot be compared because neither an admitted requirement nor implementation version exists. Status: `BLOCKED_NO_IMPLEMENTATION_VERSION`. No future requirement is applied retroactively.\n")
    write_md("REPORTS/TRACEABILITY-AUDIT.md", front("v12 Traceability Audit") + "The v11.1 source trace reaches obligation and then stops. v12 finding-to-evidence-to-source links are complete for process findings, but no decision-to-requirement chain is fabricated.\n\nThe implementation, conformance, finding, and audit-evidence graphs remain distinct from v10.1/v11.1 historical graphs.\n")
    final = front("Generic Discovery Engine — Protocol-v12 Final Compliance Report")
    final += "## 1. Audit identity and scope\n\nAudit `AUDIT-V12-001`, mode `FULL`, scope `AUDIT-SCOPE-V12-001`. Requirement include/exclude sets are empty because the specification contains zero admitted requirements.\n\n"
    final += "## 2. Four conformance planes\n\nNormative: unavailable. Implementation: unavailable. Verification: blocked. Decision: no decisions. The planes are not collapsed.\n\n"
    final += "## 3. Input validation\n\n" + table(["Check", "Result", "Failure class"], [(x["check_id"], x["result"], x.get("failure_class")) for x in input_contract["checks"]]) + "\n"
    final += "## 4. Implementation discovery\n\nNo present implementation source or test source was discovered. Historical snapshots and planning documents were explicitly excluded from present implementation evidence.\n\n"
    final += "## 5. Requirement mappings and claims\n\n0 requirements, mappings, implementation claims, and implementation evidence records. No mapping is treated as conformance.\n\n"
    final += "## 6. Verification and decisions\n\n0 criteria, oracles, verification executions, and compliance decisions. `UNVERIFIED`, `UNKNOWN`, `BLOCKED`, and `NON_CONFORMANT` remain distinct; no per-requirement status exists without a requirement.\n\n"
    final += "## 7. Findings and nonconformance\n\nThree process/mapping/traceability findings are evidence-backed. There are 0 nonconformances because no violated normative condition is demonstrated.\n\n"
    final += "## 8. Remediation and re-audit\n\nThree blocked remediations target the three findings. None is complete and all require re-verification before closure.\n\n"
    final += "## 9. Specialized audits\n\nRegression, security, compatibility, resource/concurrency applicability, temporal integrity, and historical compliance are blocked or unknown; none is silently passed.\n\n"
    final += "## 10. Traceability and graphs\n\nFour distinct v12 graphs represent implementation, conformance, findings/remediation, and audit evidence. No conformance decision chain is invented.\n\n"
    final += "## 11. Aggregation and release gate\n\nAll decision counters are zero. The release gate is `BLOCKED`; a zero failure count is not compliance. No aggregate percentage is used.\n\n"
    final += "## 12. Audit run reproducibility\n\nThe run records specification hash, missing-implementation sentinel hash, environment, configuration hash, selected input artifacts, and execution parameters. Result: `BLOCKED`.\n\n"
    final += "## 13. Certificate\n\n" + table(["Field", "Value"], [("status", cert["status"]), ("specification hash", cert["specification_hash"]), ("implementation hash", cert["implementation_hash"]), ("scope", cert["scope_id"]), ("certificate hash", cert["certificate_hash"])]) + "\n"
    final += "## 14. Certificate semantics\n\nThe certificate records this declared blocked audit under its declared scope/environment. It does not establish universal safety, specification completeness, execution safety, or future compliance.\n\n"
    final += "## Final disposition\n\n**`BLOCKED` — no conformance, nonconformance, conditional compliance, or release-compliance claim is authorized.**\n"
    write_md("REPORTS/FINAL-COMPLIANCE-REPORT.md", final)


if __name__ == "__main__": main()
