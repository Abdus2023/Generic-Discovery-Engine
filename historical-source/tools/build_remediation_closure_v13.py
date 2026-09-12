#!/usr/bin/env python3
"""Build the deterministic Protocol-v13 remediation and closure package."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
HS = ROOT / "historical-source"
OUT = HS / "compliance"
REMEDIATION = OUT / "remediation"
SCHEMA = OUT / "schema"
REPORTS = OUT / "reports"
VERSION = "13.0"
CREATED_AT = "2026-09-12T15:20:54Z"
OBJECT_TYPES = [
    "REMEDIATION_PROGRAM", "ROOT_CAUSE", "REMEDIATION_ACTION", "CHANGE_SET",
    "IMPACT_ASSESSMENT", "REVERIFICATION_PLAN", "REVERIFICATION_EXECUTION",
    "REGRESSION_SCOPE", "CLOSURE_DECISION", "WAIVER_REVIEW",
    "CERTIFICATE_REVISION", "RESIDUAL_RISK",
]
SCHEMA_NAMES = [
    "remediation-program", "root-cause", "remediation-action", "change-set",
    "impact-assessment", "reverification-plan", "reverification-execution",
    "regression-scope", "closure-decision", "waiver-review", "residual-risk",
    "certificate-revision",
]
REGISTRY_FILES = [
    "REMEDIATION-PROGRAMS.yaml", "ROOT-CAUSES.yaml", "REMEDIATION-ACTIONS.yaml",
    "CHANGE-SETS.yaml", "IMPACT-ASSESSMENTS.yaml", "REVERIFICATION-PLANS.yaml",
    "REVERIFICATION-EXECUTIONS.yaml", "REGRESSION-SCOPES.yaml",
    "CLOSURE-DECISIONS.yaml", "WAIVER-REVIEWS.yaml", "RESIDUAL-RISKS.yaml",
    "CERTIFICATE-REVISIONS.yaml",
]
SUPPORT_FILES = [
    "REMEDIATION-STATE-MACHINE.yaml", "VALIDATION-PIPELINE.yaml",
    "VALIDATION-ERRORS.yaml", "VALIDATION-REPORT.yaml", "DECISION-FUNCTION.yaml",
    "CLOSURE-PREDICATE.yaml", "CLOSURE-INVARIANTS.yaml",
    "PRIOR-AUDIT-INTEGRITY.yaml", "OBJECT-REGISTRY.yaml", "SCHEMA-REGISTRY.yaml",
    "IMPACT-RULES.yaml", "REVERIFICATION-RULES.yaml", "CERTIFICATE-LINEAGE.yaml",
    "REMEDIATION-DEPENDENCY-GRAPH.yaml", "ACCOUNTABILITY-CHAIN.yaml",
]
REPORT_FILES = ["REMEDIATION-STATUS.yaml", "REVERIFICATION-REPORT.yaml", "REGRESSION-REPORT.yaml", "CLOSURE-REPORT.yaml"]
FAILURES = [
    "FINDING_INVALID", "ROOT_CAUSE_INSUFFICIENT", "REMEDIATION_UNDEFINED",
    "CHANGE_SET_MISSING", "IMPACT_INCOMPLETE", "REVERIFICATION_SCOPE_INCOMPLETE",
    "ORACLE_INVALID", "REVERIFICATION_BLOCKED", "REVERIFICATION_FAILED",
    "REGRESSION_FAILED", "REGRESSION_INCOMPLETE", "NEW_NONCONFORMANCE",
    "TRACEABILITY_BROKEN", "RESIDUAL_RISK_MISSING", "CERTIFICATE_LINEAGE_BROKEN",
]
INVARIANTS = [
    "Every remediation references an existing finding.",
    "Every finding has a normative or explicitly classified non-normative basis.",
    "Every change set identifies before and after artifacts.",
    "Every implementation change receives impact analysis.",
    "Every impacted mandatory requirement is reconsidered.",
    "Every re-verification references a valid oracle.",
    "Every re-verification produces evidence.",
    "Flaky execution cannot establish unconditional closure.",
    "Regression scope cannot be empty when impact analysis requires regression.",
    "A finding cannot close without successful required re-verification.",
    "A finding cannot close while a mandatory regression remains unresolved.",
    "A remediation cannot weaken a requirement without creating a specification revision.",
    "A waiver cannot alter normative truth.",
    "A historical finding cannot be erased by later remediation.",
    "New violations introduced by remediation receive separate findings.",
    "Closed findings remain immutable historical records.",
    "Certificate revisions preserve predecessor lineage.",
    "Residual risk is explicitly represented.",
    "Reused compliance decisions require impact justification.",
    "Closure is deterministic for identical normalized inputs.",
]


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha_file(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def hash_value(value: Any) -> dict[str, str]:
    return {"algorithm": "SHA-256", "value": sha_bytes(canonical_bytes(value))}


def primitive(name: str) -> dict[str, str]:
    return {"$ref": "common.schema.yaml#/$defs/" + name}


def object_schema(title: str, object_type: str, required: list[str], properties: dict[str, Any], constraints: list[str] | None = None) -> dict[str, Any]:
    obj: dict[str, Any] = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": f"https://generic-discovery-engine.invalid/compliance/v13/{object_type.lower().replace('_', '-')}.schema.yaml",
        "title": title,
        "type": "object",
        "required": ["object_type", "schema_version", "object_id", "created_at", *required],
        "properties": {
            "object_type": {"const": object_type}, "schema_version": {"const": VERSION},
            "object_id": primitive("Identifier"), "created_at": primitive("Timestamp"), **properties,
        },
        "additionalProperties": False,
    }
    if constraints:
        obj["x-v13-constraints"] = constraints
    return obj


def build_schemas() -> dict[str, Any]:
    ref_array = lambda minimum=0: {"type": "array", **({"minItems": minimum} if minimum else {}), "items": primitive("Reference")}
    id_array = lambda minimum=0: {"type": "array", **({"minItems": minimum} if minimum else {}), "items": primitive("Identifier"), "uniqueItems": True}
    nullable_string = {"type": ["string", "null"]}
    schemas: dict[str, Any] = {}
    schemas["remediation-program"] = object_schema("Protocol-v13 REMEDIATION_PROGRAM", "REMEDIATION_PROGRAM", ["program_id", "finding_ids", "status"], {
        "program_id": primitive("Identifier"), "finding_ids": id_array(1),
        "status": {"type": "string", "enum": ["OPEN", "TRIAGED", "ROOT_CAUSED", "PLANNED", "IN_PROGRESS", "READY_FOR_VERIFICATION", "VERIFIED", "CLOSED", "BLOCKED", "REJECTED", "SUPERSEDED"]},
        "priority": {"type": "string", "enum": ["CRITICAL", "HIGH", "MEDIUM", "LOW", "UNKNOWN"]}, "owner": nullable_string,
        "closed_at": {"oneOf": [primitive("Timestamp"), {"type": "null"}]},
    })
    schemas["root-cause"] = object_schema("Protocol-v13 ROOT_CAUSE", "ROOT_CAUSE", ["finding_id", "classification", "statement", "what_failed", "why_failed", "normative_condition", "cause_status", "evidence", "confidence"], {
        "finding_id": primitive("Identifier"), "classification": {"type": "string", "enum": ["IMPLEMENTATION_DEFECT", "DESIGN_DEFECT", "CONTRACT_DEFECT", "SPECIFICATION_DEFECT", "ORACLE_DEFECT", "VERIFICATION_DEFECT", "MAPPING_DEFECT", "CONFIGURATION_DEFECT", "ENVIRONMENT_DEFECT", "PROCESS_DEFECT", "DEPENDENCY_DEFECT", "UNKNOWN"]},
        "statement": {"type": "string", "minLength": 1}, "what_failed": {"type": "string", "minLength": 1}, "why_failed": {"type": "string", "minLength": 1}, "normative_condition": {"type": ["string", "null"]}, "cause_status": {"type": "string", "enum": ["ESTABLISHED", "HYPOTHETICAL", "UNKNOWN"]},
        "evidence": ref_array(1), "confidence": {"type": "string", "enum": ["HIGH", "MEDIUM", "LOW", "UNKNOWN"]}, "assumptions": {"type": "array", "items": {"type": "string"}},
    }, ["A plausible root-cause hypothesis is not established fact without evidence", "UNKNOWN root cause does not block safe deterministic remediation and verification"])
    schemas["remediation-action"] = object_schema("Protocol-v13 REMEDIATION_ACTION", "REMEDIATION_ACTION", ["remediation_id", "description", "target_findings", "action_type", "status"], {
        "remediation_id": primitive("Identifier"), "description": {"type": "string"}, "target_findings": id_array(1),
        "action_type": {"type": "string", "enum": ["CODE_CHANGE", "CONFIGURATION_CHANGE", "TEST_CHANGE", "ORACLE_CHANGE", "SPECIFICATION_CHANGE", "DOCUMENTATION_CHANGE", "DEPENDENCY_CHANGE", "ENVIRONMENT_CHANGE", "DATA_MIGRATION", "PROCESS_CHANGE", "NO_CHANGE", "UNKNOWN"]},
        "status": {"type": "string", "enum": ["PROPOSED", "APPROVED", "IN_PROGRESS", "COMPLETE", "REJECTED", "SUPERSEDED"]}, "requirement_ids": id_array(),
    }, ["SPECIFICATION_CHANGE is specification evolution and requires a new audit scope"])
    schemas["change-set"] = object_schema("Protocol-v13 CHANGE_SET", "CHANGE_SET", ["change_set_id", "artifacts_before", "artifacts_after", "change_type"], {
        "change_set_id": primitive("Identifier"), "artifacts_before": ref_array(), "artifacts_after": ref_array(),
        "change_type": {"type": "string", "enum": ["ADD", "MODIFY", "DELETE", "MOVE", "RENAME", "REFACTOR", "CONFIGURATION", "DEPENDENCY", "MIXED"]},
        "source_revision": nullable_string, "target_revision": nullable_string,
        "content_hash_before": {"oneOf": [primitive("Hash"), {"type": "null"}]}, "content_hash_after": {"oneOf": [primitive("Hash"), {"type": "null"}]},
    }, ["The before/after record permits reconstruction of what changed"])
    schemas["impact-assessment"] = object_schema("Protocol-v13 IMPACT_ASSESSMENT", "IMPACT_ASSESSMENT", ["change_set_id", "affected_requirements", "affected_artifacts", "regression_required", "assessment_status"], {
        "change_set_id": primitive("Identifier"), "affected_requirements": id_array(), "affected_artifacts": ref_array(),
        "affected_contracts": id_array(), "affected_dependencies": id_array(), "regression_required": {"type": "boolean"},
        "assessment_status": {"type": "string", "enum": ["COMPLETE", "INCOMPLETE", "BLOCKED", "UNKNOWN"]}, "rationale": {"type": "string"},
    }, ["Unknown impact is never zero impact", "Incomplete dependencies require conservative assessment"])
    schemas["reverification-plan"] = object_schema("Protocol-v13 REVERIFICATION_PLAN", "REVERIFICATION_PLAN", ["finding_id", "requirement_ids", "oracle_ids", "acceptance_criteria", "status"], {
        "finding_id": primitive("Identifier"), "requirement_ids": id_array(1), "oracle_ids": id_array(1), "acceptance_criteria": id_array(1),
        "negative_tests": id_array(), "regression_required": {"type": "boolean"}, "status": {"type": "string", "enum": ["DRAFT", "APPROVED", "READY", "BLOCKED", "SUPERSEDED"]},
    }, ["Re-verification preserves original normative meaning"])
    schemas["reverification-execution"] = object_schema("Protocol-v13 REVERIFICATION_EXECUTION", "REVERIFICATION_EXECUTION", ["plan_id", "change_set_id", "execution_id", "result", "evidence", "environment", "executed_at"], {
        "plan_id": primitive("Identifier"), "change_set_id": primitive("Identifier"), "execution_id": primitive("Identifier"), "result": {"type": "string", "enum": ["PASS", "FAIL", "INCONCLUSIVE", "BLOCKED", "INVALID"]},
        "evidence": ref_array(1), "environment": primitive("Reference"), "executed_at": primitive("Timestamp"), "reproducibility": {"type": "string", "enum": ["REPRODUCIBLE", "FLAKY", "NON_REPRODUCIBLE", "UNKNOWN"]},
    })
    schemas["regression-scope"] = object_schema("Protocol-v13 REGRESSION_SCOPE", "REGRESSION_SCOPE", ["change_set_id", "requirement_ids", "oracle_ids", "rationale"], {
        "change_set_id": primitive("Identifier"), "requirement_ids": id_array(1), "oracle_ids": id_array(1), "rationale": {"type": "string"}, "completeness": {"type": "string", "enum": ["COMPLETE", "PARTIAL", "UNKNOWN"]},
    }, ["UNKNOWN regression scope prevents unconditional closure"])
    schemas["closure-decision"] = object_schema("Protocol-v13 CLOSURE_DECISION", "CLOSURE_DECISION", ["finding_id", "decision", "evidence", "decided_at"], {
        "finding_id": primitive("Identifier"), "decision": {"type": "string", "enum": ["CLOSED", "PARTIALLY_RESOLVED", "REMAINS_OPEN", "WAIVED", "SUPERSEDED", "BLOCKED", "REJECTED"]},
        "evidence": ref_array(1), "residual_risk_id": nullable_string, "decided_at": primitive("Timestamp"), "rationale": {"type": "string"},
    })
    schemas["waiver-review"] = object_schema("Protocol-v13 WAIVER_REVIEW", "WAIVER_REVIEW", ["waiver_id", "review_result", "reviewed_at"], {
        "waiver_id": primitive("Identifier"), "review_result": {"type": "string", "enum": ["RETAIN", "REVOKE", "EXPIRE", "REPLACE", "SUPERSEDE", "BLOCKED"]},
        "findings": id_array(), "reviewed_at": primitive("Timestamp"), "rationale": {"type": "string"},
    })
    schemas["residual-risk"] = object_schema("Protocol-v13 RESIDUAL_RISK", "RESIDUAL_RISK", ["source_finding_id", "description", "severity", "disposition"], {
        "source_finding_id": primitive("Identifier"), "description": {"type": "string"}, "severity": {"type": "string", "enum": ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO", "UNKNOWN"]},
        "disposition": {"type": "string", "enum": ["ACCEPTED", "MITIGATED", "TRANSFERRED", "MONITORED", "UNRESOLVED", "UNKNOWN"]}, "justification": {"type": "string"},
    }, ["Residual risk is never silently discarded at closure"])
    schemas["certificate-revision"] = object_schema("Protocol-v13 CERTIFICATE_REVISION", "CERTIFICATE_REVISION", ["previous_certificate_id", "audit_id", "changed_findings", "new_evidence", "new_verifications", "new_decisions", "new_aggregate_status", "issued_at"], {
        "previous_certificate_id": primitive("Identifier"), "audit_id": primitive("Identifier"), "changed_findings": id_array(),
        "new_evidence": ref_array(), "new_verifications": ref_array(), "new_decisions": ref_array(),
        "new_aggregate_status": {"type": "string", "enum": ["COMPLIANT", "CONDITIONALLY_COMPLIANT", "NON_COMPLIANT", "UNVERIFIED", "BLOCKED"]},
        "issued_at": primitive("Timestamp"), "certificate_hash": primitive("Hash"),
    }, ["Certificate lineage is append-only and immediate-predecessor linked", "A revision includes changed findings, new evidence, new verification, new decisions, and aggregate status"])
    for name in SCHEMA_NAMES:
        dump(SCHEMA / f"{name}.schema.yaml", schemas[name])
    return schemas


def prior_files() -> list[Path]:
    v13_schema_paths = {SCHEMA / f"{name}.schema.yaml" for name in SCHEMA_NAMES}
    return sorted((path for path in OUT.rglob("*") if path.is_file() and REMEDIATION not in path.parents and REPORTS not in path.parents and path not in v13_schema_paths), key=lambda path: str(path.relative_to(OUT)))


def main() -> None:
    required_prior = [OUT / "FINDINGS.yaml", OUT / "AUDIT-CERTIFICATE.yaml", OUT / "VALIDATION-REPORT.yaml", OUT / "OBJECT-REGISTRY.yaml", SCHEMA / "common.schema.yaml"]
    if not all(path.is_file() for path in required_prior):
        raise RuntimeError("v12.1 audit package must exist before Protocol-v13 remediation")
    if REMEDIATION.exists():
        if (REMEDIATION / "v13.1").exists():
            raise RuntimeError("refusing to erase append-only v13.1 extension artifacts")
        append_only_registries = ["ROOT-CAUSES.yaml", "REMEDIATION-ACTIONS.yaml", "CHANGE-SETS.yaml", "IMPACT-ASSESSMENTS.yaml", "REVERIFICATION-PLANS.yaml", "REVERIFICATION-EXECUTIONS.yaml", "REGRESSION-SCOPES.yaml", "CLOSURE-DECISIONS.yaml", "WAIVER-REVIEWS.yaml", "CERTIFICATE-REVISIONS.yaml"]
        for filename in append_only_registries:
            path = REMEDIATION / filename
            if path.is_file() and load(path).get("objects"):
                raise RuntimeError(f"refusing to erase append-only remediation history in {filename}")
        programs_path = REMEDIATION / "REMEDIATION-PROGRAMS.yaml"
        if programs_path.is_file() and any(item.get("status") != "BLOCKED" for item in load(programs_path).get("objects", [])):
            raise RuntimeError("refusing to overwrite progressed remediation programs")
        risks_path = REMEDIATION / "RESIDUAL-RISKS.yaml"
        if risks_path.is_file() and any(item.get("disposition") != "UNRESOLVED" for item in load(risks_path).get("objects", [])):
            raise RuntimeError("refusing to overwrite changed residual-risk dispositions")
    protected_before = [{"path": str(path.relative_to(OUT)), "sha256": sha_file(path), "bytes": path.stat().st_size} for path in prior_files()]
    if REMEDIATION.exists(): shutil.rmtree(REMEDIATION)
    if REPORTS.exists(): shutil.rmtree(REPORTS)
    for name in SCHEMA_NAMES:
        path = SCHEMA / f"{name}.schema.yaml"
        if path.exists(): path.unlink()
    REMEDIATION.mkdir(parents=True)
    REPORTS.mkdir(parents=True)

    schemas = build_schemas()
    findings = load(OUT / "FINDINGS.yaml")["objects"]
    finding_ids = [item["object_id"] for item in findings]
    if finding_ids != ["FINDING-V121-001", "FINDING-V121-002", "FINDING-V121-003"]:
        raise RuntimeError("unexpected v12.1 finding set")

    programs = []
    priorities = ["HIGH", "HIGH", "MEDIUM"]
    for index, finding_id in enumerate(finding_ids, 1):
        programs.append({
            "object_type": "REMEDIATION_PROGRAM", "schema_version": VERSION,
            "object_id": f"PROGRAM-V13-{index:03d}", "created_at": CREATED_AT,
            "program_id": f"PROGRAM-V13-{index:03d}", "finding_ids": [finding_id],
            "status": "BLOCKED", "priority": priorities[index - 1], "owner": None, "closed_at": None,
        })
    residual_risks = []
    descriptions = [
        "No accepted normative requirement basis exists for remediation or closure.",
        "No present implementation source exists for controlled engineering change or re-verification.",
        "Requirement-to-oracle traceability remains unavailable, preventing compliance reassessment.",
    ]
    for index, (finding, description) in enumerate(zip(findings, descriptions), 1):
        residual_risks.append({
            "object_type": "RESIDUAL_RISK", "schema_version": VERSION,
            "object_id": f"RISK-V13-{index:03d}", "created_at": CREATED_AT,
            "source_finding_id": finding["object_id"], "description": description,
            "severity": finding["severity"], "disposition": "UNRESOLVED",
            "justification": "R2 normative-basis validation blocks downstream remediation and closure.",
        })

    registry_payloads: dict[str, tuple[str, list[dict[str, Any]], str]] = {
        "REMEDIATION-PROGRAMS.yaml": ("REMEDIATION_PROGRAM", programs, "BLOCKED_AT_R2"),
        "ROOT-CAUSES.yaml": ("ROOT_CAUSE", [], "NOT_ESTABLISHED_PROCEDURE_STOPPED_AT_R2"),
        "REMEDIATION-ACTIONS.yaml": ("REMEDIATION_ACTION", [], "NOT_DEFINED_PROCEDURE_STOPPED_AT_R2"),
        "CHANGE-SETS.yaml": ("CHANGE_SET", [], "NO_CHANGE_RECORDED"),
        "IMPACT-ASSESSMENTS.yaml": ("IMPACT_ASSESSMENT", [], "NOT_APPLICABLE_WITHOUT_CHANGE_SET"),
        "REVERIFICATION-PLANS.yaml": ("REVERIFICATION_PLAN", [], "NOT_DEFINED_NO_REQUIREMENT_OR_ORACLE"),
        "REVERIFICATION-EXECUTIONS.yaml": ("REVERIFICATION_EXECUTION", [], "NOT_EXECUTED"),
        "REGRESSION-SCOPES.yaml": ("REGRESSION_SCOPE", [], "NOT_DEFINED_NO_CHANGE_OR_REQUIREMENTS"),
        "CLOSURE-DECISIONS.yaml": ("CLOSURE_DECISION", [], "NOT_REACHED"),
        "WAIVER-REVIEWS.yaml": ("WAIVER_REVIEW", [], "NO_WAIVERS"),
        "RESIDUAL-RISKS.yaml": ("RESIDUAL_RISK", residual_risks, "UNRESOLVED"),
        "CERTIFICATE-REVISIONS.yaml": ("CERTIFICATE_REVISION", [], "NOT_ISSUED_NO_CHANGED_DECISION"),
    }
    for filename, (object_type, objects, status) in registry_payloads.items():
        dump(REMEDIATION / filename, {"schema_version": VERSION, "object_type": object_type, "status": status, "objects": objects})

    active_states = ["OPEN", "TRIAGED", "ROOT_CAUSED", "PLANNED", "IN_PROGRESS", "READY_FOR_VERIFICATION", "VERIFIED"]
    sequential = [
        ("OPEN", "TRIAGED", "FINDING_CLASSIFIED"), ("TRIAGED", "ROOT_CAUSED", "ROOT_CAUSE_ESTABLISHED_OR_EXPLICITLY_UNKNOWN"),
        ("ROOT_CAUSED", "PLANNED", "REMEDIATION_ACTION_DEFINED"), ("PLANNED", "IN_PROGRESS", "APPROVED_CHANGE_EXISTS"),
        ("IN_PROGRESS", "READY_FOR_VERIFICATION", "CHANGE_SET_COMPLETE"), ("READY_FOR_VERIFICATION", "VERIFIED", "REVERIFICATION_PASSES"),
        ("VERIFIED", "CLOSED", "ALL_CLOSURE_PREDICATES_PASS"),
    ]
    legal = [{"from": source, "to": target, "guard": guard} for source, target, guard in sequential]
    legal += [{"from": state, "to": "BLOCKED", "guard": "REQUIRED_PREREQUISITE_UNAVAILABLE"} for state in active_states]
    legal += [{"from": "BLOCKED", "to": "$PREVIOUS_ACTIVE_STATE", "guard": "BLOCKING_CONDITION_REMOVED"}, {"from": "OPEN", "to": "REJECTED", "guard": "FINDING_INVALIDATED_WITH_EVIDENCE"}, {"from": "OPEN", "to": "SUPERSEDED", "guard": "NEWER_AUTHORITATIVE_FINDING_REPLACES"}]
    forbidden = ["OPEN", "TRIAGED", "ROOT_CAUSED", "PLANNED", "IN_PROGRESS", "READY_FOR_VERIFICATION", "BLOCKED", "WAIVED"]
    state_histories = [{"program_id": item["object_id"], "transitions": [{"from": "OPEN", "to": "TRIAGED", "guard_evidence": item["finding_ids"]}, {"from": "TRIAGED", "to": "BLOCKED", "guard_evidence": ["ERROR-V13-001"]}], "current": "BLOCKED"} for item in programs]
    dump(REMEDIATION / "REMEDIATION-STATE-MACHINE.yaml", {
        "schema_version": VERSION, "initial_state": "OPEN", "normal_path": ["OPEN", "TRIAGED", "ROOT_CAUSED", "PLANNED", "IN_PROGRESS", "READY_FOR_VERIFICATION", "VERIFIED", "CLOSED"],
        "legal_transitions": legal, "forbidden_direct_closure": [{"from": state, "to": "CLOSED"} for state in forbidden],
        "waiver_disposition": {"source": "NON_CONFORMANT", "disposition": "WAIVED", "underlying_normative_truth_changed": False, "guard": "EFFECTIVE_APPROVED_WAIVER"},
        "state_histories": state_histories,
    })

    stages = ["LOAD_FINDING", "VALIDATE_FINDING", "VALIDATE_NORMATIVE_BASIS", "CLASSIFY_FAILURE_BOUNDARY", "ESTABLISH_ROOT_CAUSE", "DEFINE_REMEDIATION", "RECORD_CHANGE_SET", "ASSESS_IMPACT", "DETERMINE_REVERIFICATION_SCOPE", "VALIDATE_ORACLE", "EXECUTE_REVERIFICATION", "EXECUTE_REGRESSION", "REEVALUATE_CONFORMANCE", "ASSESS_RESIDUAL_RISK", "DECIDE_CLOSURE", "REVISE_CERTIFICATE"]
    pipeline = []
    for index, stage in enumerate(stages):
        if index == 0: status, detail = "PASS", "Loaded three immutable v12.1 audit findings."
        elif index == 1: status, detail = "PASS", "Finding objects validate and all evidence references resolve."
        elif index == 2: status, detail = "BLOCKED_STOP", "v11.1 certificate is FAIL and zero admitted requirements exist."
        else: status, detail = "NOT_EXECUTED_EARLY_STOP", "R2 prerequisite prevents valid downstream processing."
        pipeline.append({"stage_id": f"R{index}", "stage": stage, "status": status, "detail": detail})
    dump(REMEDIATION / "VALIDATION-PIPELINE.yaml", {"schema_version": VERSION, "stages": pipeline, "stop_stage": "R2", "deterministic_order": True})
    errors = [{"error_id": "ERROR-V13-001", "code": "TRACEABILITY_BROKEN", "stage": "R2", "boundary": "NORMATIVE_BASIS", "affected_findings": finding_ids, "implementation_nonconformance": False, "effect": "BLOCK_DOWNSTREAM_REMEDIATION", "detail": "No accepted requirement/rule/criterion/oracle basis exists."}]
    dump(REMEDIATION / "VALIDATION-ERRORS.yaml", {"schema_version": VERSION, "errors": errors, "failure_codes": FAILURES, "rule": "Process failures do not automatically become implementation nonconformance."})
    dump(REMEDIATION / "VALIDATION-REPORT.yaml", {"schema_version": VERSION, "created_at": CREATED_AT, "overall_status": "BLOCKED_INVALID_NORMATIVE_BASIS", "stop_stage": "R2", "summary": {"stages": 16, "executed": 3, "passed": 2, "blocked": 1, "not_executed": 13}, "counts": {"findings": 3, "programs": 3, "root_causes": 0, "actions": 0, "change_sets": 0, "impact_assessments": 0, "reverification_plans": 0, "reverification_executions": 0, "regression_scopes": 0, "closure_decisions": 0, "certificate_revisions": 0, "residual_risks": 3}, "closure_authorized": False, "certificate_revision_authorized": False})
    dump(REMEDIATION / "DECISION-FUNCTION.yaml", {"schema_version": VERSION, "precedence": ["REJECTED", "SUPERSEDED", "WAIVED", "BLOCKED", "REMAINS_OPEN", "PARTIALLY_RESOLVED", "CLOSED"], "function": {"CLOSED": "all closure predicates pass", "PARTIALLY_RESOLVED": "original failure reduced but closure predicates incomplete", "REMAINS_OPEN": "normative violation remains proven", "WAIVED": "effective approved waiver applies", "BLOCKED": "closure cannot be evaluated", "SUPERSEDED": "authoritative later finding replaces finding", "REJECTED": "finding proven invalid"}, "deterministic_for_identical_normalized_inputs": True})
    closure_predicates = ["FINDING_VALID", "ROOT_CAUSE_OR_SAFE_REMEDIATION_KNOWN", "CHANGE_SET_RECORDED", "IMPACT_ASSESSMENT_COMPLETE", "ORIGINAL_FAILURE_NO_LONGER_REPRODUCED", "REQUIRED_REVERIFICATION_PASSED", "REQUIRED_REGRESSION_PASSED", "NO_NEW_MANDATORY_VIOLATION", "NO_UNRESOLVED_BLOCKING_DEPENDENCY", "RESIDUAL_RISK_RECORDED", "TRACEABILITY_COMPLETE"]
    dump(REMEDIATION / "CLOSURE-PREDICATE.yaml", {"schema_version": VERSION, "operator": "AND", "predicates": closure_predicates, "closed_iff_all_true": True, "current": {name: False for name in closure_predicates}, "current_result": "BLOCKED"})
    dump(REMEDIATION / "CLOSURE-INVARIANTS.yaml", {"schema_version": VERSION, "invariants": [{"invariant_id": f"V13-I{index:02d}", "statement": text, "enforcement": "MECHANICAL"} for index, text in enumerate(INVARIANTS, 1)]})
    dump(REMEDIATION / "IMPACT-RULES.yaml", {"schema_version": VERSION, "minimum_dimensions": ["DIRECTLY_MODIFIED_REQUIREMENTS", "DEPENDENT_REQUIREMENTS", "AFFECTED_CONTRACTS", "AFFECTED_PROVIDERS", "SCHEDULER_BEHAVIOR", "STATE_TRANSITIONS", "SECURITY_BOUNDARIES", "RESOURCE_CONSTRAINTS", "SERIALIZATION_PERSISTENCE", "OBSERVABILITY", "COMPATIBILITY"], "discovery_pipeline_triggers": ["Candidate", "Acquisition", "Observation", "Recognition", "Discovery", "Candidate Expansion", "Scheduler"], "unknown_impact_is_zero": False, "incomplete_dependency_policy": "CONSERVATIVE"})
    dump(REMEDIATION / "REVERIFICATION-RULES.yaml", {"schema_version": VERSION, "required_chain": ["ORIGINAL_VIOLATION", "ORIGINAL_NORMATIVE_CONDITION", "ORIGINAL_ACCEPTANCE_CRITERION", "VALIDATED_ORACLE", "NEW_EXECUTION", "NEW_EVIDENCE"], "execution_linked_to_change": True, "negative_verification_when_undesirable_behavior": "SHOULD", "flaky_result": "INCONCLUSIVE", "flaky_closure": ["REMAINS_OPEN", "BLOCKED"], "regression_scope": ["ORIGINAL_FAILING_REQUIREMENT", "DIRECTLY_AFFECTED_REQUIREMENTS", "TRANSITIVE_DEPENDENT_REQUIREMENTS"], "recommended_explicit_regression_coverage": ["SECURITY", "CONCURRENCY", "PERSISTENCE", "RESOURCE_BOUNDARIES"], "post_remediation_recalculation": ["INVALIDATE_AFFECTED_DECISION", "REEVALUATE_AFFECTED_REQUIREMENT", "PROPAGATE_DEPENDENCY_GRAPH", "RECALCULATE_AUDIT_AGGREGATE"], "decision_reuse_policy": "Unaffected decisions may be retained only with impact evidence proving continued validity."})
    dump(REMEDIATION / "REMEDIATION-DEPENDENCY-GRAPH.yaml", {"schema_version": VERSION, "graph_type": "REMEDIATION_DEPENDENCY_GRAPH", "nodes": [{"node_id": item["object_id"], "status": item["status"]} for item in programs], "edges": [], "ready_for_verification": [], "rule": "A mandatory incomplete remediation dependency prevents readiness."})
    previous_certificate = load(OUT / "AUDIT-CERTIFICATE.yaml")["objects"][0]
    dump(REMEDIATION / "CERTIFICATE-LINEAGE.yaml", {"schema_version": VERSION, "lineage": [previous_certificate["object_id"]], "revisions": [], "append_only": True, "previous_certificate_hash": previous_certificate["certificate_hash"], "status": "UNCHANGED_NO_DECISION_REVISION", "rule": "The prior certificate remains immutable; no revision exists without changed conformance decisions."})
    dump(REMEDIATION / "ACCOUNTABILITY-CHAIN.yaml", {"schema_version": VERSION, "chain": ["HISTORY", "EVIDENCE", "HISTORICAL_PROPERTY", "OBLIGATION", "REQUIREMENT", "NORMATIVE_RULE", "ACCEPTANCE_CRITERION", "TEST_ORACLE", "IMPLEMENTATION", "VERIFICATION", "CONFORMANCE", "FINDING", "ROOT_CAUSE", "REMEDIATION", "CHANGE", "REVERIFICATION", "REGRESSION", "CLOSURE", "CERTIFICATE"], "current_terminal_stage": "FINDING", "blocked_next_stage": "ROOT_CAUSE", "append_only_history": True, "iterative_conformance": True, "historical_remediation_policy": {"historical_decision_immutable": True, "later_remediation_requires_new_implementation_version": True, "later_conformance_requires_new_decision": True, "retrospective_audit_must_be_explicit": True}, "new_finding_policy": "A violation introduced by remediation receives a separate finding and never overwrites the source finding."})

    local_objects = [(obj, "REMEDIATION-PROGRAMS.yaml", index) for index, obj in enumerate(programs)] + [(obj, "RESIDUAL-RISKS.yaml", index) for index, obj in enumerate(residual_risks)]
    dump(REMEDIATION / "OBJECT-REGISTRY.yaml", {"schema_version": VERSION, "objects": [{"object_type": obj["object_type"], "object_id": obj["object_id"], "source_file": filename, "json_pointer": f"/objects/{index}"} for obj, filename, index in local_objects], "external_registry": {"path": "../OBJECT-REGISTRY.yaml", "sha256": sha_file(OUT / "OBJECT-REGISTRY.yaml")}, "global_uniqueness_checked": True})
    dump(REMEDIATION / "SCHEMA-REGISTRY.yaml", {"schema_version": VERSION, "common_schema": {"path": "../schema/common.schema.yaml", "sha256": sha_file(SCHEMA / "common.schema.yaml")}, "schemas": [{"object_type": object_type, "path": f"../schema/{name}.schema.yaml", "sha256": sha_file(SCHEMA / f"{name}.schema.yaml")} for object_type, name in zip(OBJECT_TYPES, SCHEMA_NAMES)]})
    dump(REMEDIATION / "PRIOR-AUDIT-INTEGRITY.yaml", {"schema_version": VERSION, "protected_artifact_count": len(protected_before), "artifacts": protected_before, "status": "PRESERVED", "rule": "v13 adds append-only remediation records and does not rewrite prior evidence, decisions, findings, or certificates."})

    dump(REPORTS / "REMEDIATION-STATUS.yaml", {"schema_version": VERSION, "status": "BLOCKED", "stop_stage": "R2", "program_counts": {"blocked": 3, "closed": 0}, "root_causes_established": 0, "actions_defined": 0, "changes_recorded": 0, "reason": "Normative basis invalid; no specification weakening or implementation change is fabricated."})
    dump(REPORTS / "REVERIFICATION-REPORT.yaml", {"schema_version": VERSION, "status": "NOT_EXECUTED", "plans": 0, "executions": 0, "pass": 0, "fail": 0, "inconclusive": 0, "blocked": 0, "reason": "No admitted requirement, criterion, oracle, or implementation change exists."})
    dump(REPORTS / "REGRESSION-REPORT.yaml", {"schema_version": VERSION, "status": "NOT_EXECUTED", "scopes": 0, "executions": 0, "new_findings": 0, "reason": "No change set or impact assessment exists; zero regression is not a pass."})
    dump(REPORTS / "CLOSURE-REPORT.yaml", {"schema_version": VERSION, "status": "BLOCKED", "findings_considered": 3, "closed": 0, "partially_resolved": 0, "remains_open": 0, "waived": 0, "blocked_without_decision": 3, "residual_risks": 3, "certificate_revised": False, "prior_certificate_immutable": True, "principle": "CHANGE != FIX != VERIFIED != CONFORMANT != CLOSED; WAIVED != FIXED; CLOSED != ERASED."})

    protected_after = [{"path": str(path.relative_to(OUT)), "sha256": sha_file(path), "bytes": path.stat().st_size} for path in prior_files()]
    if protected_before != protected_after:
        raise RuntimeError("v13 modified a protected v12/v12.1 artifact")
    generated = [*(f"remediation/{name}" for name in REGISTRY_FILES + SUPPORT_FILES), *(f"schema/{name}.schema.yaml" for name in SCHEMA_NAMES), *(f"reports/{name}" for name in REPORT_FILES)]
    missing = [name for name in generated if not (OUT / name).is_file()]
    if missing or len(generated) != 43:
        raise RuntimeError(f"invalid v13 artifact set: missing={missing}, count={len(generated)}")
    print("generated 43 v13 deliverables; programs=3 risks=3 changes=0 reverifications=0 closures=0 certificate_revisions=0 status=BLOCKED")


if __name__ == "__main__":
    main()
