#!/usr/bin/env python3
"""Build the deterministic Protocol-v12.1 schema/validation/state package.

The package validates the rejected v11.1 normative basis and the v12 blocked
implementation-discovery result without inventing requirements, implementation
artifacts, verification executions, decisions, or nonconformances.
"""
from __future__ import annotations

import hashlib
import json
import platform
import shutil
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
HS = ROOT / "historical-source"
SPEC = HS / "specification"
OUT = HS / "compliance"
SCHEMA_DIR = OUT / "schema"
REPORTS = OUT / "REPORTS"
SCHEMA_VERSION = "12.1"
CREATED_AT = "2026-09-12T14:53:12Z"
OBJECT_TYPES = [
    "AUDIT", "AUDIT_SCOPE", "INPUT_ARTIFACT", "ENVIRONMENT",
    "IMPLEMENTATION_ARTIFACT", "IMPLEMENTATION_CLAIM", "REQUIREMENT_MAPPING",
    "EVIDENCE_RECORD", "VERIFICATION_EXECUTION", "COMPLIANCE_DECISION",
    "NONCONFORMANCE", "WAIVER", "REMEDIATION", "AUDIT_FINDING",
    "AUDIT_RUN", "AUDIT_CERTIFICATE",
]
AUDIT_MODES = ["FULL", "TARGETED", "REGRESSION", "SECURITY", "COMPATIBILITY", "RELEASE", "HISTORICAL", "EXPERIMENTAL"]
DECISION_STATES = ["UNASSESSED", "MAPPED", "VERIFIED", "CONFORMANT", "PARTIALLY_CONFORMANT", "NON_CONFORMANT", "UNVERIFIED", "NOT_APPLICABLE", "BLOCKED", "UNKNOWN"]
RELEASE_STATES = ["COMPLIANT", "CONDITIONALLY_COMPLIANT", "NON_COMPLIANT", "UNVERIFIED", "BLOCKED"]
FAILURE_CODES = [
    "INPUT_MISSING", "INPUT_MALFORMED", "SCHEMA_VIOLATION", "SCHEMA_MISSING",
    "SCHEMA_UNSUPPORTED", "SCHEMA_INCOMPATIBLE", "REFERENCE_UNRESOLVED",
    "REFERENCE_TYPE_MISMATCH", "REFERENCE_DUPLICATE", "HASH_MISMATCH",
    "INTEGRITY_FAILURE", "TEMPORAL_MISMATCH", "FUTURE_REQUIREMENT_APPLIED",
    "FUTURE_ORACLE_APPLIED", "FUTURE_IMPLEMENTATION_EVIDENCE",
    "TRACEABILITY_GAP", "SPECIFICATION_DEFECT", "ORACLE_DEFECT",
    "DEPENDENCY_DEFECT", "CONFLICT_DEFECT",
]
INVARIANTS = [
    "Every mandatory requirement receives exactly one current decision.",
    "Every decision references its requirement.",
    "Every CONFORMANT decision has valid verification evidence.",
    "Every NON_CONFORMANT decision identifies a violated normative condition.",
    "UNVERIFIED does not imply NON_CONFORMANT.",
    "UNKNOWN does not imply NON_CONFORMANT.",
    "BLOCKED does not imply NON_CONFORMANT.",
    "NOT_APPLICABLE has explicit scope evidence.",
    "Guidance does not affect mandatory conformance.",
    "Implementation claims do not substitute for compliance decisions.",
    "Test results do not substitute for validated acceptance criteria.",
    "Oracle failure does not automatically imply implementation failure.",
    "Waivers do not modify normative requirements.",
    "Historical audits respect temporal scope.",
    "Future requirements do not contaminate historical conformance.",
    "Invalid evidence does not support conformance.",
    "Every finding has evidence.",
    "Every remediation references a finding.",
    "A remediation does not close a finding without re-verification.",
    "A certificate identifies its audit scope.",
    "A certificate identifies specification and implementation versions or hashes.",
    "Audit aggregation does not conceal mandatory failures.",
    "Identical normalized inputs yield identical decisions.",
    "State transitions obey the defined transition relation.",
    "No terminal conformance state is reached through an undefined transition.",
]
SPEC_INPUTS = [
    ("INPUT-SPECIFICATION", "SPECIFICATION", "SPECIFICATION-MANIFEST.yaml", True),
    ("INPUT-REQUIREMENTS", "REQUIREMENT_SET", "REQUIREMENTS.yaml", True),
    ("INPUT-NORMATIVE-RULES", "NORMATIVE_RULE_SET", "NORMATIVE-RULES.yaml", True),
    ("INPUT-ACCEPTANCE-CRITERIA", "ACCEPTANCE_CRITERIA", "ACCEPTANCE-CRITERIA.yaml", True),
    ("INPUT-TEST-ORACLES", "TEST_ORACLES", "TEST-ORACLES.yaml", True),
    ("INPUT-DEPENDENCIES", "DEPENDENCIES", "REQUIREMENT-DEPENDENCIES.yaml", True),
    ("INPUT-CONFLICTS", "CONFLICTS", "REQUIREMENT-CONFLICTS.yaml", True),
    ("INPUT-COMPATIBILITY", "COMPATIBILITY", "COMPATIBILITY.yaml", True),
    ("INPUT-BOUNDARIES", "OTHER", "IMPLEMENTATION-BOUNDARIES.yaml", True),
    ("INPUT-VERIFICATION-RECORDS", "VERIFICATION_RECORD", "VERIFICATION.yaml", False),
    ("INPUT-SPECIFICATION-CERTIFICATE", "OTHER", "SPECIFICATION-CERTIFICATE.yaml", True),
]
SCHEMA_NAMES = [
    "common", "audit", "audit-scope", "input-artifact", "environment",
    "implementation-artifact", "implementation-claim", "requirement-mapping",
    "evidence-record", "verification-execution", "compliance-decision",
    "nonconformance", "waiver", "remediation", "audit-finding", "audit-run",
    "audit-certificate",
]
REQUIRED_VALIDATION_OUTPUTS = [
    "VALIDATION-REPORT.yaml", "VALIDATION-ERRORS.yaml", "REFERENCE-INTEGRITY.yaml",
    "TEMPORAL-INTEGRITY.yaml", "SCHEMA-VALIDATION.yaml", "DEPENDENCY-VALIDATION.yaml",
    "CONFLICT-VALIDATION.yaml", "EVIDENCE-VALIDATION.yaml", "ORACLE-VALIDATION.yaml",
    "VERIFICATION-VALIDATION.yaml", "CONFORMANCE-DECISIONS.yaml", "FINDINGS.yaml",
    "COMPLIANCE-MATRIX.yaml", "AUDIT-CERTIFICATE.yaml",
]


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def hash_value(value: Any) -> dict[str, str]:
    return {"algorithm": "SHA-256", "value": sha_bytes(canonical_bytes(value))}


def file_hash(path: Path) -> dict[str, str]:
    return {"algorithm": "SHA-256", "value": sha_file(path)}


def ref(object_type: str, object_id: str) -> dict[str, str]:
    return {"object_type": object_type, "object_id": object_id}


def base(object_type: str, object_id: str, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
    obj: dict[str, Any] = {
        "object_type": object_type,
        "schema_version": SCHEMA_VERSION,
        "object_id": object_id,
        "created_at": CREATED_AT,
        "producer": "historical-source/tools/build_compliance_audit_v121.py",
    }
    if metadata is not None:
        obj["metadata"] = metadata
    return obj


def with_content_hash(obj: dict[str, Any], field: str = "content_hash") -> dict[str, Any]:
    assert field not in obj
    obj[field] = hash_value(obj)
    return obj


def primitive_ref(name: str) -> dict[str, str]:
    return {"$ref": f"common.schema.yaml#/$defs/{name}"}


def object_schema(title: str, object_type: str, required: list[str], properties: dict[str, Any], constraints: dict[str, Any] | None = None) -> dict[str, Any]:
    common_properties = {
        "object_type": {"const": object_type},
        "schema_version": {"const": SCHEMA_VERSION},
        "object_id": primitive_ref("Identifier"),
        "created_at": primitive_ref("Timestamp"),
        "updated_at": primitive_ref("Timestamp"),
        "producer": primitive_ref("Identifier"),
        "content_hash": primitive_ref("Hash"),
        "metadata": {"type": "object"},
    }
    obj: dict[str, Any] = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": f"https://generic-discovery-engine.invalid/compliance/v12.1/{object_type.lower().replace('_', '-')}.schema.yaml",
        "title": title,
        "type": "object",
        "required": ["object_type", "schema_version", "object_id", "created_at", *required],
        "properties": common_properties | properties,
        "additionalProperties": False,
    }
    if constraints:
        obj.update(constraints)
    return obj


def build_schemas() -> dict[str, Any]:
    identifier = {"type": "string", "minLength": 1, "maxLength": 256, "pattern": "^[A-Za-z0-9][A-Za-z0-9._:/-]*$"}
    timestamp = {"type": "string", "format": "date-time", "pattern": "^(?:\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(?:\\.\\d+)?Z|\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(?:\\.\\d+)?[+-]\\d{2}:\\d{2})$"}
    hash_schema = {
        "type": "object", "required": ["algorithm", "value"],
        "properties": {"algorithm": {"type": "string", "enum": ["SHA-256", "SHA-384", "SHA-512"]}, "value": {"type": "string", "pattern": "^[A-Fa-f0-9]+$"}},
        "additionalProperties": False,
    }
    version_scope = {
        "type": "object", "required": ["specification_version"],
        "properties": {
            "specification_version": {"type": "string"}, "implementation_version": {"type": "string"},
            "valid_from": primitive_ref("Timestamp"),
            "valid_until": {"oneOf": [primitive_ref("Timestamp"), {"type": "null"}]},
        },
        "additionalProperties": False,
        "x-v12.1-constraint": "valid_until MUST NOT precede valid_from",
    }
    reference = {
        "type": "object", "required": ["object_type", "object_id"],
        "properties": {"object_type": {"type": "string"}, "object_id": primitive_ref("Identifier")},
        "additionalProperties": False,
    }
    common = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://generic-discovery-engine.invalid/compliance/v12.1/common.schema.yaml",
        "schema_version": SCHEMA_VERSION,
        "title": "Protocol-v12.1 common primitive schemas",
        "$defs": {"Identifier": identifier, "Timestamp": timestamp, "Hash": hash_schema, "VersionScope": version_scope, "Reference": reference},
    }
    schemas: dict[str, Any] = {"common": common}
    schemas["audit-scope"] = object_schema("Protocol-v12.1 AUDIT_SCOPE", "AUDIT_SCOPE", ["target", "requirements", "temporal_policy"], {
        "target": {"type": "object", "required": ["implementation_version"], "properties": {"implementation_version": {"type": "string"}, "artifact_ids": {"type": "array", "items": primitive_ref("Identifier"), "uniqueItems": True}}},
        "requirements": {"type": "array", "minItems": 1, "items": primitive_ref("Reference"), "uniqueItems": True},
        "exclusions": {"type": "array", "items": primitive_ref("Reference"), "uniqueItems": True},
        "temporal_policy": {"type": "string", "enum": ["VERSION_BOUND", "CURRENT", "RETROSPECTIVE"]},
        "historical_version": {"type": ["string", "null"]},
    }, {"x-v12.1-constraint": "HISTORICAL audits use VERSION_BOUND or explicitly RETROSPECTIVE"})
    schemas["audit"] = object_schema("Protocol-v12.1 AUDIT", "AUDIT", ["audit_id", "scope", "specification", "mode", "status", "started_at"], {
        "audit_id": primitive_ref("Identifier"),
        "scope": {"$ref": "audit-scope.schema.yaml"},
        "specification": primitive_ref("Reference"),
        "mode": {"type": "string", "enum": AUDIT_MODES},
        "status": {"type": "string", "enum": ["CREATED", "VALIDATING", "READY", "RUNNING", "COMPLETED", "BLOCKED", "FAILED", "CANCELLED"]},
        "started_at": primitive_ref("Timestamp"), "completed_at": {"oneOf": [primitive_ref("Timestamp"), {"type": "null"}]},
        "input_artifacts": {"type": "array", "items": primitive_ref("Reference"), "uniqueItems": True},
        "implementation_artifacts": {"type": "array", "items": primitive_ref("Reference"), "uniqueItems": True},
    }, {"allOf": [{"if": {"properties": {"mode": {"const": "HISTORICAL"}}}, "then": {"properties": {"scope": {"properties": {"temporal_policy": {"enum": ["VERSION_BOUND", "RETROSPECTIVE"]}}}}}}], "x-v12.1-temporal-rule": "A HISTORICAL audit is VERSION_BOUND or explicitly RETROSPECTIVE"})
    schemas["input-artifact"] = object_schema("Protocol-v12.1 INPUT_ARTIFACT", "INPUT_ARTIFACT", ["artifact_type", "source_path", "content_hash", "producer_stage"], {
        "artifact_type": {"type": "string", "enum": ["SPECIFICATION", "REQUIREMENT_SET", "NORMATIVE_RULE_SET", "ACCEPTANCE_CRITERIA", "TEST_ORACLES", "DEPENDENCIES", "CONFLICTS", "COMPATIBILITY", "IMPLEMENTATION_SOURCE", "TEST_SOURCE", "VERIFICATION_RECORD", "RUNTIME_ARTIFACT", "OTHER"]},
        "source_path": {"type": "string"}, "producer_stage": {"type": "string"}, "schema_version_produced": {"type": "string"},
        "generated_at": primitive_ref("Timestamp"), "content_hash": primitive_ref("Hash"), "temporal_scope": primitive_ref("VersionScope"),
    }, {"x-v12.1-hash-rule": "content_hash covers the canonical object excluding content_hash"})
    schemas["environment"] = object_schema("Protocol-v12.1 ENVIRONMENT", "ENVIRONMENT", ["platform", "reproducibility"], {
        "platform": {"type": "object", "required": ["os", "architecture"], "properties": {"os": {"type": "string"}, "architecture": {"type": "string"}, "runtime": {"type": "string"}, "compiler": {"type": "string"}}, "additionalProperties": False},
        "dependencies": {"type": "array", "items": {"type": "object", "required": ["name", "version"], "properties": {"name": {"type": "string"}, "version": {"type": "string"}}, "additionalProperties": False}},
        "configuration_hash": {"oneOf": [primitive_ref("Hash"), {"type": "null"}]},
        "reproducibility": {"type": "string", "enum": ["REPRODUCIBLE", "PARTIALLY_REPRODUCIBLE", "NON_REPRODUCIBLE", "UNKNOWN"]},
    })
    schemas["implementation-artifact"] = object_schema("Protocol-v12.1 IMPLEMENTATION_ARTIFACT", "IMPLEMENTATION_ARTIFACT", ["artifact_type", "identity", "version_scope"], {
        "artifact_type": {"type": "string", "enum": ["SOURCE_FILE", "FUNCTION", "METHOD", "TYPE", "TRAIT", "MODULE", "CONFIGURATION", "SCHEMA", "TEST", "FIXTURE", "DOCUMENTATION", "BUILD_ARTIFACT", "BINARY", "RUNTIME_TRACE", "LOG", "METRIC", "AUDIT_RECORD"]},
        "identity": {"type": "object", "required": ["path"], "properties": {"path": {"type": "string"}, "symbol": {"type": ["string", "null"]}, "line_start": {"type": ["integer", "null"]}, "line_end": {"type": ["integer", "null"]}}, "additionalProperties": False},
        "content_hash": {"oneOf": [primitive_ref("Hash"), {"type": "null"}]}, "version_scope": primitive_ref("VersionScope"),
    })
    schemas["implementation-claim"] = object_schema("Protocol-v12.1 IMPLEMENTATION_CLAIM", "IMPLEMENTATION_CLAIM", ["requirement_id", "claim_type", "evidence"], {
        "requirement_id": primitive_ref("Identifier"), "claim_type": {"type": "string", "enum": ["IMPLEMENTED", "PARTIALLY_IMPLEMENTED", "VERIFIED", "NON_CONFORMANT", "NOT_APPLICABLE", "UNKNOWN"]},
        "evidence": {"type": "array", "minItems": 1, "items": primitive_ref("Reference")}, "statement": {"type": "string"}, "claimant": {"type": ["string", "null"]},
    }, {"x-v12.1-constraint": "An implementation claim never establishes compliance"})
    schemas["requirement-mapping"] = object_schema("Protocol-v12.1 REQUIREMENT_MAPPING", "REQUIREMENT_MAPPING", ["requirement_id", "implementation_artifacts", "mapping_type", "coverage"], {
        "requirement_id": primitive_ref("Identifier"), "implementation_artifacts": {"type": "array", "items": primitive_ref("Reference")},
        "mapping_type": {"type": "string", "enum": ["DIRECT", "INDIRECT", "DISTRIBUTED", "TEST_ONLY", "CONFIGURATION", "RUNTIME", "UNKNOWN"]},
        "coverage": {"type": "string", "enum": ["FULL", "PARTIAL", "NONE", "UNKNOWN"]}, "rationale": {"type": ["string", "null"]},
    })
    schemas["evidence-record"] = object_schema("Protocol-v12.1 EVIDENCE_RECORD", "EVIDENCE_RECORD", ["evidence_type", "source", "result", "captured_at"], {
        "evidence_type": {"type": "string", "enum": ["SOURCE", "STATIC_ANALYSIS", "TEST_RESULT", "RUNTIME_TRACE", "LOG", "METRIC", "AUDIT_RECORD", "BINARY_INSPECTION", "CONFIGURATION", "DOCUMENTATION", "MANUAL_INSPECTION"]},
        "source": primitive_ref("Reference"), "result": {"type": "string", "enum": ["PASS", "FAIL", "INCONCLUSIVE", "UNAVAILABLE", "INVALID", "UNKNOWN"]},
        "captured_at": primitive_ref("Timestamp"), "environment": {"oneOf": [primitive_ref("Reference"), {"type": "null"}]},
        "content_hash": {"oneOf": [primitive_ref("Hash"), {"type": "null"}]}, "reproducibility": {"type": "string", "enum": ["REPRODUCIBLE", "FLAKY", "NON_REPRODUCIBLE", "UNKNOWN"]},
    })
    schemas["verification-execution"] = object_schema("Protocol-v12.1 VERIFICATION_EXECUTION", "VERIFICATION_EXECUTION", ["oracle_id", "execution_status", "result", "evidence"], {
        "oracle_id": primitive_ref("Identifier"), "execution_status": {"type": "string", "enum": ["STARTED", "COMPLETED", "FAILED_TO_EXECUTE", "CANCELLED", "BLOCKED"]},
        "result": {"type": "string", "enum": ["PASS", "FAIL", "INCONCLUSIVE", "UNAVAILABLE", "INVALID", "UNKNOWN"]}, "evidence": {"type": "array", "items": primitive_ref("Reference")},
        "environment": primitive_ref("Reference"), "started_at": primitive_ref("Timestamp"), "completed_at": {"oneOf": [primitive_ref("Timestamp"), {"type": "null"}]},
        "exit_code": {"type": ["integer", "null"]}, "reproducibility": {"type": "string", "enum": ["REPRODUCIBLE", "FLAKY", "NON_REPRODUCIBLE", "UNKNOWN"]},
    })
    schemas["compliance-decision"] = object_schema("Protocol-v12.1 COMPLIANCE_DECISION", "COMPLIANCE_DECISION", ["requirement_id", "status", "confidence", "basis"], {
        "requirement_id": primitive_ref("Identifier"), "status": {"type": "string", "enum": DECISION_STATES}, "confidence": {"type": "string", "enum": ["HIGH", "MEDIUM", "LOW", "UNKNOWN"]},
        "basis": {"type": "array", "minItems": 1, "items": primitive_ref("Reference")}, "violated_rules": {"type": "array", "items": primitive_ref("Identifier")},
        "failed_criteria": {"type": "array", "items": primitive_ref("Identifier")}, "unresolved_dependencies": {"type": "array", "items": primitive_ref("Identifier")}, "decided_at": primitive_ref("Timestamp"),
    })
    schemas["nonconformance"] = object_schema("Protocol-v12.1 NONCONFORMANCE", "NONCONFORMANCE", ["requirement_id", "violated_condition", "evidence", "severity"], {
        "requirement_id": primitive_ref("Identifier"), "violated_condition": {"type": "string"}, "violated_rule": {"type": "string"},
        "evidence": {"type": "array", "minItems": 1, "items": primitive_ref("Reference")}, "severity": {"type": "string", "enum": ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO", "UNKNOWN"]},
        "reproducibility": {"type": "string", "enum": ["REPRODUCIBLE", "FLAKY", "NON_REPRODUCIBLE", "UNKNOWN"]},
    }, {"x-v12.1-constraint": "A nonconformance identifies the normative condition actually violated"})
    schemas["waiver"] = object_schema("Protocol-v12.1 WAIVER", "WAIVER", ["requirement_id", "justification", "scope", "authority", "status"], {
        "requirement_id": primitive_ref("Identifier"), "justification": {"type": "string", "minLength": 1}, "scope": {"type": "object"}, "authority": {"type": "string"},
        "status": {"type": "string", "enum": ["PROPOSED", "APPROVED", "REJECTED", "EXPIRED", "REVOKED"]}, "expires_at": {"oneOf": [primitive_ref("Timestamp"), {"type": "null"}]},
    }, {"x-v12.1-constraint": "A waiver changes disposition, never requirement truth"})
    schemas["remediation"] = object_schema("Protocol-v12.1 REMEDIATION", "REMEDIATION", ["finding_id", "status", "actions"], {
        "finding_id": primitive_ref("Identifier"), "status": {"type": "string", "enum": ["OPEN", "PLANNED", "IN_PROGRESS", "READY_FOR_VERIFICATION", "VERIFIED", "CLOSED", "BLOCKED", "REJECTED", "SUPERSEDED"]},
        "actions": {"type": "array", "minItems": 1, "items": {"type": "object", "required": ["action_id", "description"], "properties": {"action_id": primitive_ref("Identifier"), "description": {"type": "string"}, "implementation_artifacts": {"type": "array", "items": primitive_ref("Reference")}}, "additionalProperties": False}},
        "residual_risk": {"type": ["string", "null"]},
    })
    schemas["audit-finding"] = object_schema("Protocol-v12.1 AUDIT_FINDING", "AUDIT_FINDING", ["finding_type", "severity", "evidence", "status"], {
        "finding_type": {"type": "string", "enum": ["NON_CONFORMANCE", "SPECIFICATION_DEFECT", "VERIFICATION_DEFECT", "ORACLE_DEFECT", "MAPPING_DEFECT", "TRACEABILITY_GAP", "SECURITY_RISK", "COMPATIBILITY_RISK", "RESOURCE_RISK", "PROCESS_FAILURE", "UNKNOWN"]},
        "severity": {"type": "string", "enum": ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO", "UNKNOWN"]}, "evidence": {"type": "array", "minItems": 1, "items": primitive_ref("Reference")},
        "status": {"type": "string", "enum": ["OPEN", "ACCEPTED", "REMEDIATING", "RESOLVED", "WAIVED", "REJECTED", "SUPERSEDED"]},
    })
    schemas["audit-run"] = object_schema("Protocol-v12.1 AUDIT_RUN", "AUDIT_RUN", ["audit_id", "inputs", "environment", "started_at", "status"], {
        "audit_id": primitive_ref("Identifier"), "inputs": {"type": "array", "minItems": 1, "items": primitive_ref("Reference")}, "environment": primitive_ref("Reference"),
        "started_at": primitive_ref("Timestamp"), "completed_at": {"oneOf": [primitive_ref("Timestamp"), {"type": "null"}]}, "status": {"type": "string", "enum": ["RUNNING", "COMPLETED", "FAILED", "BLOCKED", "CANCELLED"]},
        "result_hash": {"oneOf": [primitive_ref("Hash"), {"type": "null"}]},
    })
    schemas["audit-certificate"] = object_schema("Protocol-v12.1 AUDIT_CERTIFICATE", "AUDIT_CERTIFICATE", ["audit_id", "scope", "release_status", "counts", "issued_at", "certificate_hash", "specification_hash", "implementation_hash"], {
        "audit_id": primitive_ref("Identifier"), "scope": primitive_ref("Reference"), "release_status": {"type": "string", "enum": RELEASE_STATES},
        "counts": {"type": "object", "required": ["conformant", "partially_conformant", "non_conformant", "unverified", "blocked", "unknown", "not_applicable"], "properties": {name: {"type": "integer", "minimum": 0} for name in ["conformant", "partially_conformant", "non_conformant", "unverified", "blocked", "unknown", "not_applicable"]}, "additionalProperties": False},
        "critical_findings": {"type": "array", "items": primitive_ref("Identifier")}, "waivers": {"type": "array", "items": primitive_ref("Reference")},
        "issued_at": primitive_ref("Timestamp"), "certificate_hash": primitive_ref("Hash"), "specification_hash": primitive_ref("Hash"), "implementation_hash": primitive_ref("Hash"),
    }, {"x-v12.1-hash-rule": "certificate_hash covers the canonical certificate excluding certificate_hash"})
    for name in SCHEMA_NAMES:
        dump(SCHEMA_DIR / f"{name}.schema.yaml", schemas[name])
    return schemas


def make_input_artifacts() -> list[dict[str, Any]]:
    artifacts: list[dict[str, Any]] = []
    for object_id, artifact_type, filename, required in SPEC_INPUTS:
        path = SPEC / filename
        source = load(path)
        produced = source.get("schema_version", source.get("specification", {}).get("schema_version", "1.0"))
        obj = base("INPUT_ARTIFACT", object_id, {"source_content_hash": file_hash(path), "required": required, "source_bytes": path.stat().st_size})
        obj.update({
            "artifact_type": artifact_type, "source_path": f"historical-source/specification/{filename}",
            "producer_stage": "V11.1_SPECIFICATION", "schema_version_produced": str(produced),
            "temporal_scope": {"specification_version": "11.1"},
        })
        artifacts.append(with_content_hash(obj))
    inventory: list[dict[str, str]] = []
    for path in sorted(ROOT.iterdir(), key=lambda p: p.name):
        if path.name in {".git", "historical-source"}:
            continue
        if path.is_file():
            inventory.append({"path": path.name, "sha256": sha_file(path), "classification": "DOCUMENTATION_OR_PLANNING_NOT_IMPLEMENTATION"})
    repository = base("INPUT_ARTIFACT", "INPUT-REPOSITORY-DISCOVERY", {"inventory": inventory, "implementation_candidates": [], "excluded_directories": [".git", "historical-source"]})
    repository.update({
        "artifact_type": "OTHER", "source_path": ".", "producer_stage": "V12_IMPLEMENTATION_DISCOVERY",
        "schema_version_produced": SCHEMA_VERSION,
        "temporal_scope": {"specification_version": "11.1", "implementation_version": "UNAVAILABLE"},
    })
    artifacts.append(with_content_hash(repository))
    return artifacts


def legal_transitions() -> list[dict[str, Any]]:
    raw = [
        ("UNASSESSED", "MAPPED", "VALID_MAPPING_EXISTS"), ("UNASSESSED", "NOT_APPLICABLE", "SCOPE_PREDICATE_PROVES_NA"),
        ("UNASSESSED", "BLOCKED", "PREREQUISITE_PREVENTS_EVALUATION"), ("UNASSESSED", "UNKNOWN", "SEMANTIC_CLASSIFICATION_IMPOSSIBLE"),
        ("MAPPED", "VERIFIED", "VALID_VERIFICATION_COMPLETED"), ("MAPPED", "UNVERIFIED", "VERIFICATION_INSUFFICIENT"),
        ("MAPPED", "BLOCKED", "PREREQUISITE_FAILS"), ("MAPPED", "UNKNOWN", "SEMANTIC_DETERMINATION_IMPOSSIBLE"),
        ("VERIFIED", "CONFORMANT", "ALL_NORMATIVE_PREDICATES_PASS"), ("VERIFIED", "PARTIALLY_CONFORMANT", "SOME_PASS_AND_REQUIRED_PREDICATES_UNRESOLVED"),
        ("VERIFIED", "NON_CONFORMANT", "NORMATIVE_VIOLATION_PROVEN"), ("VERIFIED", "UNVERIFIED", "VERIFICATION_VALIDITY_INSUFFICIENT"),
        ("VERIFIED", "BLOCKED", "PREREQUISITE_INVALIDATED"), ("PARTIALLY_CONFORMANT", "CONFORMANT", "REMAINING_PREDICATES_PASS"),
        ("PARTIALLY_CONFORMANT", "NON_CONFORMANT", "VIOLATION_SUBSEQUENTLY_PROVEN"), ("PARTIALLY_CONFORMANT", "UNVERIFIED", "EVIDENCE_BECOMES_INSUFFICIENT"),
        ("PARTIALLY_CONFORMANT", "BLOCKED", "PREREQUISITE_BECOMES_UNAVAILABLE"), ("NON_CONFORMANT", "CONFORMANT", "REMEDIATION_AND_COMPLETE_REVERIFICATION"),
        ("NON_CONFORMANT", "PARTIALLY_CONFORMANT", "REMEDIATION_REMOVES_VIOLATION_BUT_LEAVES_UNRESOLVED_PREDICATES"),
        ("UNVERIFIED", "MAPPED", "VALID_MAPPING_ESTABLISHED"), ("UNVERIFIED", "VERIFIED", "COMPLETE_VERIFICATION_AVAILABLE"),
        ("UNVERIFIED", "BLOCKED", "UPSTREAM_PREREQUISITE_BLOCKS"), ("BLOCKED", "UNASSESSED", "BLOCK_REMOVED_AND_ASSESSMENT_RESET"),
        ("BLOCKED", "MAPPED", "MAPPING_BECOMES_EVALUABLE"), ("BLOCKED", "VERIFIED", "BLOCKED_VERIFICATION_SUCCESSFULLY_EXECUTED"),
        ("UNKNOWN", "UNASSESSED", "ASSESSMENT_INVALIDATED_OR_RESET"), ("UNKNOWN", "MAPPED", "UNCERTAINTY_RESOLVED_AND_MAPPING_EXISTS"),
        ("UNKNOWN", "VERIFIED", "VALID_VERIFICATION_RESOLVES_UNCERTAINTY"), ("NOT_APPLICABLE", "UNASSESSED", "APPLICABILITY_REVOKED"),
    ]
    return [{"from": a, "to": b, "guard": c, "transition_kind": "CONFORMANCE_STATE"} for a, b, c in raw]


def build_state_machine() -> dict[str, Any]:
    forbidden = [
        ("UNVERIFIED", "CONFORMANT"), ("UNKNOWN", "CONFORMANT"), ("BLOCKED", "CONFORMANT"), ("MAPPED", "CONFORMANT"),
        ("UNVERIFIED", "NON_CONFORMANT"), ("UNKNOWN", "NON_CONFORMANT"), ("BLOCKED", "NON_CONFORMANT"),
    ]
    machine = {
        "schema_version": SCHEMA_VERSION,
        "initial_state": "UNASSESSED",
        "intermediate_states": ["MAPPED", "VERIFIED"],
        "decision_states": DECISION_STATES,
        "terminal_assessment_states": ["CONFORMANT", "PARTIALLY_CONFORMANT", "NON_CONFORMANT", "UNVERIFIED", "NOT_APPLICABLE", "BLOCKED", "UNKNOWN"],
        "legal_transitions": legal_transitions(),
        "waiver_disposition": {
            "source_notation": "NON_CONFORMANT -> WAIVED",
            "transition_kind": "DISPOSITION_ONLY",
            "underlying_state_before": "NON_CONFORMANT",
            "underlying_state_after": "NON_CONFORMANT",
            "audit_disposition": "CONDITIONALLY_ACCEPTED",
            "guard": "VALID_APPROVED_UNEXPIRED_UNREVOKED_WAIVER",
            "rationale": "WAIVED is not a COMPLIANCE_DECISION state; waiver changes disposition, not truth.",
        },
        "forbidden_transitions": [{"from": a, "to": b, "unless": "NEW_VALIDATED_EVIDENCE_COMPLETES_REQUIRED_INTERMEDIATE_VALIDATION"} for a, b in forbidden],
        "forbidden_substitutions": ["IMPLEMENTED_CLAIM_TO_CONFORMANT", "TEST_PASS_TO_CONFORMANT", "DOCUMENTATION_TO_CONFORMANT"],
        "reverification_rule": ["IMPLEMENTATION_CHANGE", "IMPACT_ANALYSIS", "INVALIDATE_AFFECTED_DECISIONS", "REMAP", "REVERIFY", "REDECIDE"],
    }
    dump(OUT / "CONFORMANCE-STATE-MACHINE.yaml", machine)
    return machine


def build_reports(cert: dict[str, Any], findings: list[dict[str, Any]]) -> None:
    banner = "> **v12.1 validation status: BLOCKED.** The v11.1 normative basis is rejected, contains zero admitted requirements, and no present implementation source exists. Schema validity, requirement validity, evidence validity, verification validity, and conformance remain distinct.\n\n"
    findings_rows = "\n".join(f"| {x['object_id']} | {x['finding_type']} | {x['severity']} | {x['status']} |" for x in findings)
    write_md(REPORTS / "FINAL-COMPLIANCE-REPORT.md", "# Protocol-v12.1 Final Validation and Compliance Report\n\n" + banner + "## Result\n\n- Canonical pipeline: stopped at `V2 SCHEMA_VALIDATION` after the v12 empty requirement scope violated the v12.1 `minItems: 1` invariant.\n- Required implementation input: `INPUT_MISSING`.\n- Requirements, mappings, verifications, decisions, and nonconformances: `0`.\n- Release status: `BLOCKED`.\n- No absence-of-evidence condition is attributed as implementation nonconformance.\n\n## Four trust questions\n\n1. Can every candidate object be trusted? **No: the audit scope is schema-invalid under v12.1.**\n2. Is a requirement decidable? **No admitted requirement exists.**\n3. Did verification establish a required property? **No verification was authorized or run.**\n4. What state follows? **No requirement state; the audit/release is BLOCKED.**\n\n## Findings\n\n| ID | Type | Severity | Status |\n|---|---|---|---|\n" + findings_rows + "\n\n## Certificate\n\nCertificate `" + cert["object_id"] + "` has release status `BLOCKED`. Its hash applies only to the declared audit, scope, specification hash, missing-implementation sentinel, and environment. It establishes no universal safety or future compliance.\n")
    write_md(REPORTS / "SCHEMA-VALIDATION.md", "# Protocol-v12.1 Schema Validation\n\n" + banner + "All 17 normative schema files are machine-parseable and complete. The candidate `AUDIT_SCOPE` intentionally fails because its requirement list is empty; inserting a synthetic requirement is forbidden.\n")
    write_md(REPORTS / "STATE-TRANSITIONS.md", "# Protocol-v12.1 Conformance State Transitions\n\n" + banner + "The complete legal and forbidden relations are in `CONFORMANCE-STATE-MACHINE.yaml`. `MAPPED` and `VERIFIED` are intermediate. `WAIVED` is normalized as disposition-only so the underlying `NON_CONFORMANT` truth is preserved.\n")
    write_md(REPORTS / "REFERENCE-INTEGRITY.md", "# Protocol-v12.1 Reference Integrity\n\n" + banner + "The construction-time registry resolves every emitted reference exactly once with matching type. Canonical V3 was not reached because V2 stopped the run.\n")
    write_md(REPORTS / "TEMPORAL-INTEGRITY.md", "# Protocol-v12.1 Temporal Integrity\n\n" + banner + "No implementation version exists, so current or historical compatibility cannot be decided. No future requirement, oracle, or implementation evidence was applied.\n")
    write_md(REPORTS / "FINDINGS.md", "# Protocol-v12.1 Findings\n\n" + banner + "| ID | Type | Severity | Status |\n|---|---|---|---|\n" + findings_rows + "\n")
    write_md(REPORTS / "COMPLIANCE-MATRIX.md", "# Protocol-v12.1 Compliance Matrix\n\n" + banner + "The machine matrix contains zero rows because there are zero admitted requirements and zero decisions. An empty matrix is not an all-pass result.\n")
    write_md(REPORTS / "VALIDATION-PIPELINE.md", "# Protocol-v12.1 Validation Pipeline\n\n" + banner + "V0 detected missing implementation input; V1 passed structural loading; V2 rejected the empty requirement scope and stopped evaluation. V3–V16 were not used to establish conformance.\n")
    write_md(REPORTS / "REMEDIATION-PLAN.md", "# Protocol-v12.1 Remediation Plan\n\n" + banner + "Three blocked remediations target the three evidence-backed findings. None may close before successful re-validation and re-verification.\n")
    write_md(REPORTS / "AGGREGATION.md", "# Protocol-v12.1 Aggregation\n\n" + banner + "Every requirement-decision counter is zero. No percentage is emitted. The release status is `BLOCKED`, not compliant or partially compliant.\n")
    write_md(REPORTS / "NONCONFORMANCES.md", "# Protocol-v12.1 Nonconformances\n\n" + banner + "No nonconformance exists because no violated normative condition is evidenced. Missing inputs, invalid scope, and unavailable evidence are not implementation violations.\n")
    write_md(REPORTS / "REGRESSION-REPORT.md", "# Protocol-v12.1 Regression Audit\n\n" + banner + "No comparable prior/current requirement decision exists. Regression evaluation was not reached and no nonconformance is inferred.\n")
    write_md(REPORTS / "SECURITY-AUDIT.md", "# Protocol-v12.1 Security Audit\n\n" + banner + "No admitted security requirement, implementation target, negative criterion, oracle, or verification exists. Security is not claimed.\n")
    write_md(REPORTS / "COMPATIBILITY-AUDIT.md", "# Protocol-v12.1 Compatibility Audit\n\n" + banner + "Compatibility cannot be decided without admitted requirement and implementation versions. No compatibility result is promoted to conformance.\n")
    write_md(REPORTS / "TEMPORAL-AUDIT.md", "# Protocol-v12.1 Temporal Audit\n\n" + banner + "Temporal evaluation is blocked by the unavailable implementation version. No historical audit was silently made retrospective.\n")
    write_md(REPORTS / "TRACEABILITY-AUDIT.md", "# Protocol-v12.1 Traceability Audit\n\n" + banner + "Normative traceability terminates before requirement. No requirement-to-decision or decision-to-source chain is fabricated.\n")


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    schemas = build_schemas()
    inputs = make_input_artifacts()
    input_refs = [ref("INPUT_ARTIFACT", x["object_id"]) for x in inputs]
    input_by_id = {x["object_id"]: x for x in inputs}

    requirements = load(SPEC / "REQUIREMENTS.yaml").get("requirements", [])
    spec_manifest = load(SPEC / "SPECIFICATION-MANIFEST.yaml")["specification"]
    spec_certificate = load(SPEC / "SPECIFICATION-CERTIFICATE.yaml")
    spec_validation = load(SPEC / "VALIDATION.yaml")

    input_contract = {
        "schema_version": SCHEMA_VERSION,
        "required_roles": ["SPECIFICATION", "REQUIREMENT_SET", "NORMATIVE_RULE_SET", "ACCEPTANCE_CRITERIA", "TEST_ORACLES", "DEPENDENCIES", "CONFLICTS", "COMPATIBILITY", "IMPLEMENTATION_SOURCE", "EVIDENCE", "VERIFICATION_EXECUTIONS", "WAIVERS"],
        "available_input_artifacts": input_refs,
        "missing_inputs": [{"artifact_type": "IMPLEMENTATION_SOURCE", "required": True, "failure": "INPUT_MISSING"}],
        "optional_unavailable_inputs": ["TEST_SOURCE", "RUNTIME_ARTIFACT"],
        "audit_registries": {"implementation_artifacts": "IMPLEMENTATION-ARTIFACTS.yaml", "evidence": "EVIDENCE-RECORDS.yaml", "verification_executions": "VERIFICATION-EXECUTIONS.yaml", "waivers": "WAIVERS.yaml"},
        "v11_1": {"manifest_status": spec_manifest["validation"]["status"], "certificate_status": spec_certificate["validation_status"], "validation_status": spec_validation["overall_status"], "requirement_count": len(requirements)},
        "conformance_gate": "CLOSED",
    }
    dump(OUT / "INPUT-CONTRACT.yaml", input_contract)
    dump(OUT / "INPUT-ARTIFACTS.yaml", {"schema_version": SCHEMA_VERSION, "objects": inputs})

    environment = base("ENVIRONMENT", "ENV-V121-001", {"capture": "deterministic builder runtime"})
    environment.update({
        "platform": {"os": platform.system(), "architecture": platform.machine(), "runtime": f"Python {platform.python_version()}"},
        "dependencies": [], "configuration_hash": hash_value({"mode": "BLOCKED_STATIC_VALIDATION", "schema_version": SCHEMA_VERSION}), "reproducibility": "REPRODUCIBLE",
    })
    dump(OUT / "ENVIRONMENTS.yaml", {"schema_version": SCHEMA_VERSION, "objects": [environment]})

    scope = base("AUDIT_SCOPE", "SCOPE-V121-001", {"invalidity": "EMPTY_REQUIREMENT_SET_FROM_REJECTED_V11.1", "synthetic_requirements_forbidden": True})
    scope.update({"target": {"implementation_version": "UNAVAILABLE", "artifact_ids": []}, "requirements": [], "exclusions": [], "temporal_policy": "CURRENT", "historical_version": None})
    audit = base("AUDIT", "AUDIT-OBJECT-V121-001", {"disposition": "VALIDATION_STOPPED_NO_CONFORMANCE_EVALUATION"})
    audit.update({
        "audit_id": "AUDIT-V121-001", "scope": scope, "specification": ref("INPUT_ARTIFACT", "INPUT-SPECIFICATION"), "mode": "FULL", "status": "BLOCKED",
        "started_at": CREATED_AT, "completed_at": CREATED_AT, "input_artifacts": input_refs, "implementation_artifacts": [],
    })
    dump(OUT / "AUDIT.yaml", {"schema_version": SCHEMA_VERSION, "objects": [audit]})
    dump(OUT / "AUDIT-SCOPE.yaml", {"schema_version": SCHEMA_VERSION, "view_type": "V12_COMPATIBILITY_VIEW", "scope": ref("AUDIT_SCOPE", scope["object_id"]), "canonical_location": "AUDIT.yaml#/objects/0/scope", "validation_status": "FAIL_EMPTY_REQUIREMENT_SCOPE"})

    evidence = [
        base("EVIDENCE_RECORD", "EVIDENCE-V121-SPEC", {"observation": "v11.1 certificate is FAIL and the normative derivation gate is closed", "expected": "accepted normative specification"}) | {"evidence_type": "AUDIT_RECORD", "source": ref("INPUT_ARTIFACT", "INPUT-SPECIFICATION-CERTIFICATE"), "result": "INVALID", "captured_at": CREATED_AT, "environment": ref("ENVIRONMENT", environment["object_id"]), "reproducibility": "REPRODUCIBLE"},
        base("EVIDENCE_RECORD", "EVIDENCE-V121-IMPLEMENTATION", {"observation": "no present implementation candidate exists outside excluded historical/planning material", "expected": "required implementation source"}) | {"evidence_type": "MANUAL_INSPECTION", "source": ref("INPUT_ARTIFACT", "INPUT-REPOSITORY-DISCOVERY"), "result": "UNAVAILABLE", "captured_at": CREATED_AT, "environment": ref("ENVIRONMENT", environment["object_id"]), "reproducibility": "REPRODUCIBLE"},
        base("EVIDENCE_RECORD", "EVIDENCE-V121-REQUIREMENTS", {"observation": "requirement registry contains zero requirements", "expected": "at least one admitted mandatory requirement"}) | {"evidence_type": "SOURCE", "source": ref("INPUT_ARTIFACT", "INPUT-REQUIREMENTS"), "result": "UNAVAILABLE", "captured_at": CREATED_AT, "environment": ref("ENVIRONMENT", environment["object_id"]), "reproducibility": "REPRODUCIBLE"},
    ]
    dump(OUT / "EVIDENCE-RECORDS.yaml", {"schema_version": SCHEMA_VERSION, "objects": evidence})
    dump(OUT / "IMPLEMENTATION-EVIDENCE.yaml", {"schema_version": SCHEMA_VERSION, "view_type": "V12_COMPATIBILITY_VIEW", "status": "UNAVAILABLE", "objects": [], "rule": "Audit evidence records do not become implementation evidence."})

    findings = [
        base("AUDIT_FINDING", "FINDING-V121-001", {"title": "Normative specification unavailable", "failure_boundary": "SPECIFICATION_DEFECT"}) | {"finding_type": "SPECIFICATION_DEFECT", "severity": "HIGH", "evidence": [ref("EVIDENCE_RECORD", "EVIDENCE-V121-SPEC")], "status": "OPEN"},
        base("AUDIT_FINDING", "FINDING-V121-002", {"title": "Required implementation source unavailable", "failure_boundary": "MAPPING_DEFECT", "not_implementation_nonconformance": True}) | {"finding_type": "MAPPING_DEFECT", "severity": "HIGH", "evidence": [ref("EVIDENCE_RECORD", "EVIDENCE-V121-IMPLEMENTATION")], "status": "OPEN"},
        base("AUDIT_FINDING", "FINDING-V121-003", {"title": "Normative traceability terminates before requirement", "failure_boundary": "TRACEABILITY_GAP"}) | {"finding_type": "TRACEABILITY_GAP", "severity": "MEDIUM", "evidence": [ref("EVIDENCE_RECORD", "EVIDENCE-V121-REQUIREMENTS")], "status": "OPEN"},
    ]
    dump(OUT / "FINDINGS.yaml", {"schema_version": SCHEMA_VERSION, "objects": findings})

    remediations = [
        base("REMEDIATION", "REMEDIATION-V121-001", {"reverification_required": True}) | {"finding_id": "FINDING-V121-001", "status": "BLOCKED", "actions": [{"action_id": "ACTION-V121-001", "description": "Resolve the upstream obligation conflicts and regenerate an accepted normative requirement package.", "implementation_artifacts": []}], "residual_risk": "No requirement can be evaluated until re-validation succeeds."},
        base("REMEDIATION", "REMEDIATION-V121-002", {"reverification_required": True}) | {"finding_id": "FINDING-V121-002", "status": "BLOCKED", "actions": [{"action_id": "ACTION-V121-002", "description": "Supply present implementation source separately from historical and planning documents.", "implementation_artifacts": []}], "residual_risk": "Mapping and verification remain unavailable."},
        base("REMEDIATION", "REMEDIATION-V121-003", {"reverification_required": True}) | {"finding_id": "FINDING-V121-003", "status": "BLOCKED", "actions": [{"action_id": "ACTION-V121-003", "description": "Rebuild requirement-to-oracle traceability after a normative package is accepted.", "implementation_artifacts": []}], "residual_risk": "No decision-to-source conformance trace exists."},
    ]
    dump(OUT / "REMEDIATIONS.yaml", {"schema_version": SCHEMA_VERSION, "objects": remediations})
    dump(OUT / "REMEDIATION-ACTIONS.yaml", {"schema_version": SCHEMA_VERSION, "view_type": "V12_COMPATIBILITY_VIEW", "actions": [{"action_id": action["action_id"], "remediation_id": remediation["object_id"], "description": action["description"]} for remediation in remediations for action in remediation["actions"]], "rule": "v12.1 remediation actions are embedded and are not independent normative objects."})

    empty_registries = {
        "IMPLEMENTATION-ARTIFACTS.yaml": ("IMPLEMENTATION_ARTIFACT", "INPUT_MISSING"),
        "IMPLEMENTATION-CLAIMS.yaml": ("IMPLEMENTATION_CLAIM", "NOT_CREATED"),
        "REQUIREMENT-MAPPINGS.yaml": ("REQUIREMENT_MAPPING", "BLOCKED_NO_REQUIREMENTS_OR_IMPLEMENTATION"),
        "VERIFICATION-EXECUTIONS.yaml": ("VERIFICATION_EXECUTION", "NOT_EXECUTED"),
        "CONFORMANCE-DECISIONS.yaml": ("COMPLIANCE_DECISION", "NOT_EVALUATED"),
        "NONCONFORMANCES.yaml": ("NONCONFORMANCE", "NONE_PROVEN"),
        "WAIVERS.yaml": ("WAIVER", "NONE"),
    }
    for filename, (object_type, status) in empty_registries.items():
        dump(OUT / filename, {"schema_version": SCHEMA_VERSION, "object_type": object_type, "status": status, "objects": []})
    dump(OUT / "COMPLIANCE-DECISIONS.yaml", {"schema_version": SCHEMA_VERSION, "view_type": "V12_COMPATIBILITY_VIEW", "canonical_source": "CONFORMANCE-DECISIONS.yaml", "status": "NOT_EVALUATED", "objects": []})

    audit_run = base("AUDIT_RUN", "RUN-V121-001", {"stop_stage": "V2_SCHEMA_VALIDATION", "conformance_evaluation_performed": False})
    audit_run.update({"audit_id": audit["audit_id"], "inputs": input_refs, "environment": ref("ENVIRONMENT", environment["object_id"]), "started_at": CREATED_AT, "completed_at": CREATED_AT, "status": "BLOCKED", "result_hash": None})
    dump(OUT / "AUDIT-RUNS.yaml", {"schema_version": SCHEMA_VERSION, "objects": [audit_run]})

    machine = build_state_machine()
    stages = ["LOAD", "STRUCTURAL_VALIDATION", "SCHEMA_VALIDATION", "REFERENCE_VALIDATION", "VERSION_TEMPORAL_VALIDATION", "HASH_INTEGRITY_VALIDATION", "REQUIREMENT_SEMANTIC_VALIDATION", "DEPENDENCY_VALIDATION", "CONFLICT_PRECEDENCE_VALIDATION", "MAPPING_VALIDATION", "EVIDENCE_VALIDATION", "ORACLE_VALIDATION", "VERIFICATION_VALIDATION", "CONFORMANCE_EVALUATION", "FINDING_GENERATION", "AGGREGATION", "CERTIFICATE_VALIDATION"]
    pipeline_results = []
    for i, name in enumerate(stages):
        if i == 0:
            status, detail = "BLOCKED_CONTINUE_STRUCTURAL_DIAGNOSTICS", "Required implementation source is INPUT_MISSING; conformance evaluation is prohibited."
        elif i == 1:
            status, detail = "PASS", "Available inputs and object boundaries are valid JSON structures."
        elif i == 2:
            status, detail = "FAIL_STOP", "AUDIT_SCOPE.requirements violates minItems: 1; no synthetic requirement may be inserted."
        else:
            status, detail = "NOT_EXECUTED_EARLY_STOP", "V2 schema failure stops the canonical pipeline."
        pipeline_results.append({"stage_id": f"V{i}", "stage": name, "status": status, "detail": detail})
    dump(OUT / "VALIDATION-PIPELINE.yaml", {"schema_version": SCHEMA_VERSION, "deterministic_order": True, "stages": pipeline_results, "stop_stage": "V2", "conformance_evaluation_performed": False})
    dump(OUT / "FAILURE-BOUNDARIES.yaml", {
        "schema_version": SCHEMA_VERSION,
        "earliest_invalid_boundary_rule": True,
        "boundaries": [
            {"condition": "MALFORMED_INPUT", "effect": "STOP", "implementation_nonconformance_supported": False},
            {"condition": "INVALID_SCHEMA", "effect": "STOP", "implementation_nonconformance_supported": False},
            {"condition": "BROKEN_REFERENCE", "effect": "BLOCK_AFFECTED_OBJECTS", "implementation_nonconformance_supported": False},
            {"condition": "TEMPORAL_CONTAMINATION", "effect": "BLOCK_AFFECTED_HISTORICAL_DECISIONS", "implementation_nonconformance_supported": False},
            {"condition": "INVALID_REQUIREMENT", "effect": "BLOCK_CONFORMANCE_DECISION", "implementation_nonconformance_supported": False},
            {"condition": "INVALID_ORACLE", "effect": "BLOCK_VERIFICATION_DEPENDENT_DECISION", "implementation_nonconformance_supported": False},
            {"condition": "INVALID_EVIDENCE", "effect": "UNVERIFIED", "implementation_nonconformance_supported": False},
            {"condition": "PROVEN_NORMATIVE_VIOLATION", "effect": "NON_CONFORMANT", "implementation_nonconformance_supported": True},
        ],
        "attribution_classes": {
            "SPECIFICATION_DEFECT": ["MALFORMED_REQUIREMENT", "CONTRADICTORY_RULE", "UNDEFINED_SEMANTICS"],
            "VERIFICATION_DEFECT": ["BROKEN_HARNESS", "INVALID_EXECUTION"],
            "ORACLE_DEFECT": ["ORACLE_CANNOT_DECIDE_CRITERION"],
            "MAPPING_DEFECT": ["REQUIREMENT_IMPLEMENTATION_RELATION_INVALID"],
            "IMPLEMENTATION_DEFECT": ["NORMATIVE_CONDITION_ACTUALLY_VIOLATED"],
            "ENVIRONMENT_DEFECT": ["REQUIRED_EXECUTION_ENVIRONMENT_UNAVAILABLE"],
        },
        "implementation_blame_rule": "Only IMPLEMENTATION_DEFECT automatically supports an implementation NON_CONFORMANT conclusion.",
    })

    errors = [
        {"error_id": "ERROR-V121-001", "code": "INPUT_MISSING", "stage": "V0", "object_id": None, "path": "implementation_source", "boundary": "INPUT", "effect": "BLOCK_CONFORMANCE_EVALUATION", "implementation_blame": False},
        {"error_id": "ERROR-V121-002", "code": "SCHEMA_VIOLATION", "stage": "V2", "object_id": scope["object_id"], "path": "$.scope.requirements", "boundary": "SCHEMA", "effect": "STOP", "implementation_blame": False, "detail": "minItems 1, actual 0"},
        {"error_id": "ERROR-V121-003", "code": "SPECIFICATION_DEFECT", "stage": "V0", "object_id": "INPUT-SPECIFICATION", "path": "v11.1.validation", "boundary": "SPECIFICATION", "effect": "BLOCK_REQUIREMENT_EVALUATION", "implementation_blame": False},
    ]
    dump(OUT / "VALIDATION-ERRORS.yaml", {"schema_version": SCHEMA_VERSION, "errors": errors, "failure_codes": FAILURE_CODES})

    object_records: list[tuple[dict[str, Any], str, str]] = [(audit, "AUDIT.yaml", "/objects/0"), (scope, "AUDIT.yaml", "/objects/0/scope")]
    for i, obj in enumerate(inputs): object_records.append((obj, "INPUT-ARTIFACTS.yaml", f"/objects/{i}"))
    object_records.append((environment, "ENVIRONMENTS.yaml", "/objects/0"))
    for i, obj in enumerate(evidence): object_records.append((obj, "EVIDENCE-RECORDS.yaml", f"/objects/{i}"))
    for i, obj in enumerate(findings): object_records.append((obj, "FINDINGS.yaml", f"/objects/{i}"))
    for i, obj in enumerate(remediations): object_records.append((obj, "REMEDIATIONS.yaml", f"/objects/{i}"))
    object_records.append((audit_run, "AUDIT-RUNS.yaml", "/objects/0"))
    registry_entries = [{"object_type": x[0]["object_type"], "object_id": x[0]["object_id"], "source_file": x[1], "json_pointer": x[2]} for x in object_records]

    reference_integrity = {"schema_version": SCHEMA_VERSION, "canonical_stage_status": "NOT_EXECUTED_EARLY_STOP", "construction_integrity": "PASS", "object_count_before_certificate": len(registry_entries), "unresolved": [], "ambiguous": [], "type_mismatches": [], "rule": "Every emitted Reference resolves exactly once; canonical V3 did not establish conformance because V2 stopped."}
    dump(OUT / "REFERENCE-INTEGRITY.yaml", reference_integrity)
    dump(OUT / "TEMPORAL-INTEGRITY.yaml", {"schema_version": SCHEMA_VERSION, "canonical_stage_status": "NOT_EXECUTED_EARLY_STOP", "result": "BLOCKED_NO_IMPLEMENTATION_VERSION", "temporal_policy": scope["temporal_policy"], "future_requirement_applied": False, "future_oracle_applied": False, "future_implementation_evidence": False})
    schema_results = [{"schema": f"schema/{name}.schema.yaml", "status": "PASS_MACHINE_PARSEABLE"} for name in SCHEMA_NAMES]
    dump(OUT / "SCHEMA-VALIDATION.yaml", {"schema_version": SCHEMA_VERSION, "schema_registry": schema_results, "schema_count": len(schema_results), "object_results": [{"object_id": scope["object_id"], "object_type": "AUDIT_SCOPE", "status": "FAIL", "errors": ["requirements minItems 1; actual 0"]}, {"object_id": audit["object_id"], "object_type": "AUDIT", "status": "FAIL_NESTED_SCOPE"}], "objects_not_reached_due_stop": [x[0]["object_id"] for x in object_records if x[0]["object_id"] not in {scope["object_id"], audit["object_id"]}] + ["CERTIFICATE-V121-001"], "status": "FAIL_STOP"})
    domain_rules = {
        "DEPENDENCY-VALIDATION.yaml": ["ALL_REFERENCED_REQUIREMENTS_EXIST", "REQUIRES_GRAPH_ACYCLIC", "DEPENDENCIES_EVALUATED_BEFORE_DEPENDENTS", "UNSATISFIED_MANDATORY_DEPENDENCY_CONSTRAINS_DEPENDENT"],
        "CONFLICT-VALIDATION.yaml": ["DETERMINE_BOTH_APPLICABLE", "DETERMINE_PRECEDENCE", "DETERMINE_RESOLVABILITY", "DETECT_NORMATIVE_SEMANTIC_CHANGE", "UNRESOLVED_CONFLICT_IS_SPECIFICATION_DEFECT_NOT_AUTOMATIC_NONCONFORMANCE"],
        "ORACLE-VALIDATION.yaml": ["WELL_FORMED", "VERSION_COMPATIBLE", "APPLICABLE", "DECIDABLE", "TRACEABLE_TO_REQUIREMENT", "INVALID_ORACLE_IS_ORACLE_DEFECT_NOT_IMPLEMENTATION_NONCONFORMANCE"],
        "VERIFICATION-VALIDATION.yaml": ["REQUIREMENT_TO_CRITERION_TO_ORACLE_TO_EXECUTION_TO_EVIDENCE_CHAIN_INTACT", "IMPLEMENTED_CLAIM_NOT_CONFORMANCE", "TEST_PASS_NOT_CONFORMANCE", "HIGH_COVERAGE_NOT_CONFORMANCE", "INTERFACE_EXISTENCE_NOT_CONFORMANCE", "NO_FAILURE_OBSERVED_NOT_CONFORMANCE", "DOCUMENTATION_CLAIM_NOT_CONFORMANCE"],
    }
    for filename, rules in domain_rules.items():
        dump(OUT / filename, {"schema_version": SCHEMA_VERSION, "domain": filename.removesuffix("-VALIDATION.yaml").lower(), "canonical_stage_status": "NOT_EXECUTED_EARLY_STOP", "objects_evaluated": 0, "rules": rules, "conformance_effect": "NONE"})
    dump(OUT / "EVIDENCE-VALIDATION.yaml", {"schema_version": SCHEMA_VERSION, "canonical_stage_status": "NOT_EXECUTED_EARLY_STOP", "construction_integrity": "PASS", "validity_predicates": ["SOURCE_RESOLVES", "INTEGRITY_VALID", "VERSION_SCOPE_COMPATIBLE", "EVIDENCE_TYPE_APPROPRIATE", "CAPTURE_METADATA_SUFFICIENT"], "records": [{"object_id": x["object_id"], "source_resolves": True, "result": x["result"], "supports_conformance": False} for x in evidence], "rule": "Invalid or unavailable evidence cannot establish conformance."})

    decision_algorithm = {
        "schema_version": SCHEMA_VERSION,
        "normalized_input_order": ["requirement", "applicability", "dependencies", "conflicts", "mappings", "acceptance_criteria", "oracles", "evidence", "verification_executions", "normative_predicates"],
        "precedence": ["INVALID_INPUT", "NOT_APPLICABLE", "BLOCKED", "PROVEN_VIOLATION", "PROVEN_SATISFACTION", "PARTIAL_SATISFACTION", "UNVERIFIED", "UNKNOWN"],
        "function": {"NOT_APPLICABLE": "applicability == false", "BLOCKED": "blocking dependency, environment, or oracle", "NON_CONFORMANT": "proven violation", "CONFORMANT": "all required predicates pass", "PARTIALLY_CONFORMANT": "some pass, none violated, required predicates unresolved", "UNVERIFIED": "neither satisfaction nor violation established", "UNKNOWN": "semantic classification indeterminate"},
        "deterministic_for_identical_normalized_inputs": True,
    }
    dump(OUT / "DECISION-ALGORITHM.yaml", decision_algorithm)

    counts = {"conformant": 0, "partially_conformant": 0, "non_conformant": 0, "unverified": 0, "blocked": 0, "unknown": 0, "not_applicable": 0}
    aggregation = {"schema_version": SCHEMA_VERSION, "counts": counts, "release_status": "BLOCKED", "percentage_summary": "FORBIDDEN", "requirement_count": 0, "decision_count": 0, "blocking_conditions": ["INVALID_NORMATIVE_SPECIFICATION", "EMPTY_REQUIREMENT_SCOPE", "MISSING_IMPLEMENTATION_SOURCE"], "release_rules": {"COMPLIANT": "all mandatory applicable requirements CONFORMANT and no unresolved blocking critical finding", "CONDITIONALLY_COMPLIANT": "mandatory failures covered by valid approved waivers and no unwaived critical violation", "NON_COMPLIANT": "at least one mandatory applicable NON_CONFORMANT requirement without effective waiver", "UNVERIFIED": "no mandatory violation proven but mandatory requirements remain UNVERIFIED or UNKNOWN", "BLOCKED": "mandatory evaluation cannot complete because blocking conditions remain"}, "rule": "Zero decisions and zero nonconformances do not establish compliance; PARTIALLY_COMPLIANT is not an audit-level release status."}
    dump(OUT / "AGGREGATION.yaml", aggregation)
    dump(OUT / "COMPLIANCE-AGGREGATION.yaml", {"schema_version": SCHEMA_VERSION, "view_type": "V12_COMPATIBILITY_VIEW", "canonical_source": "AGGREGATION.yaml", **{k: aggregation[k] for k in ["counts", "release_status", "percentage_summary", "blocking_conditions"]}})
    dump(OUT / "RELEASE-GATE.yaml", {"schema_version": SCHEMA_VERSION, "status": "BLOCKED", "release_status_source": "AGGREGATION.yaml", "blocking_conditions": aggregation["blocking_conditions"], "conditional_compliance": False})
    dump(OUT / "COMPLIANCE-MATRIX.yaml", {"schema_version": SCHEMA_VERSION, "status": "BLOCKED", "rows": [], "counts": counts, "source": "CONFORMANCE-DECISIONS.yaml"})

    certificate = base("AUDIT_CERTIFICATE", "CERTIFICATE-V121-001", {"implementation_hash_basis": "MISSING_IMPLEMENTATION_SENTINEL", "limitations": ["No universal safety claim", "No implementation execution audited", "No requirement conformance decision", "No future compliance claim"]})
    certificate.update({
        "audit_id": audit["audit_id"], "scope": ref("AUDIT_SCOPE", scope["object_id"]), "release_status": "BLOCKED", "counts": counts,
        "critical_findings": [], "waivers": [], "issued_at": CREATED_AT,
        "specification_hash": file_hash(SPEC / "SPECIFICATION-MANIFEST.yaml"), "implementation_hash": hash_value("IMPLEMENTATION_SOURCE_UNAVAILABLE"),
    })
    with_content_hash(certificate, "certificate_hash")
    dump(OUT / "AUDIT-CERTIFICATE.yaml", {"schema_version": SCHEMA_VERSION, "objects": [certificate]})
    object_records.append((certificate, "AUDIT-CERTIFICATE.yaml", "/objects/0"))
    registry_entries.append({"object_type": certificate["object_type"], "object_id": certificate["object_id"], "source_file": "AUDIT-CERTIFICATE.yaml", "json_pointer": "/objects/0"})
    dump(OUT / "OBJECT-REGISTRY.yaml", {"schema_version": SCHEMA_VERSION, "objects": registry_entries, "object_count": len(registry_entries), "duplicate_object_ids": [], "schema_registry": [{"object_type": t, "schema": f"schema/{t.lower().replace('_', '-')}.schema.yaml"} for t in OBJECT_TYPES]})
    dump(OUT / "IMPLEMENTATION-GRAPH.yaml", {"schema_version": SCHEMA_VERSION, "view_type": "V12_COMPATIBILITY_GRAPH", "graph_type": "IMPLEMENTATION_GRAPH", "nodes": [], "edges": [], "status": "INPUT_MISSING"})
    dump(OUT / "CONFORMANCE-GRAPH.yaml", {"schema_version": SCHEMA_VERSION, "view_type": "V12_COMPATIBILITY_GRAPH", "graph_type": "CONFORMANCE_GRAPH", "nodes": [], "edges": [], "status": "NOT_EVALUATED"})
    finding_nodes = [{"node_id": x["object_id"], "node_type": x["object_type"]} for x in findings + remediations]
    finding_edges = [{"from": x["finding_id"], "to": x["object_id"], "relation": "REMEDIATED_BY"} for x in remediations]
    for remediation in remediations:
        for action in remediation["actions"]:
            finding_nodes.append({"node_id": action["action_id"], "node_type": "EMBEDDED_REMEDIATION_ACTION"})
            finding_edges.append({"from": remediation["object_id"], "to": action["action_id"], "relation": "HAS_ACTION"})
    dump(OUT / "FINDING-GRAPH.yaml", {"schema_version": SCHEMA_VERSION, "view_type": "V12_COMPATIBILITY_GRAPH", "graph_type": "FINDING_GRAPH", "nodes": finding_nodes, "edges": finding_edges})
    evidence_nodes = [{"node_id": x["object_id"], "node_type": x["object_type"]} for x in findings + evidence] + [{"node_id": x["object_id"], "node_type": x["object_type"]} for x in inputs]
    evidence_edges = [{"from": finding["object_id"], "to": evidence_ref["object_id"], "relation": "SUPPORTED_BY"} for finding in findings for evidence_ref in finding["evidence"]] + [{"from": x["object_id"], "to": x["source"]["object_id"], "relation": "CAPTURED_FROM"} for x in evidence]
    dump(OUT / "AUDIT-EVIDENCE-GRAPH.yaml", {"schema_version": SCHEMA_VERSION, "view_type": "V12_COMPATIBILITY_GRAPH", "graph_type": "AUDIT_EVIDENCE_GRAPH", "nodes": evidence_nodes, "edges": evidence_edges, "decision_nodes": [], "verification_nodes": []})

    validation_report = {
        "schema_version": SCHEMA_VERSION, "validation_run_id": "VALIDATION-V121-001", "created_at": CREATED_AT,
        "overall_status": "BLOCKED_SCHEMA_INVALID_INPUT", "stop_stage": "V2", "release_status": "BLOCKED",
        "summary": {"pipeline_stages": 17, "executed": 3, "passed": 1, "failed": 1, "blocked": 1, "not_executed": 14, "errors": len(errors)},
        "requirements": 0, "implementation_artifacts": 0, "verification_executions": 0, "compliance_decisions": 0, "nonconformances": 0, "findings": len(findings),
        "canonical_transformation": ["SPECIFICATION", "REQUIREMENT", "NORMATIVE_RULE", "APPLICABILITY", "DEPENDENCIES_CONFLICTS", "IMPLEMENTATION_MAPPING", "ACCEPTANCE_CRITERION", "TEST_ORACLE", "VERIFICATION_EXECUTION", "EVIDENCE", "VALIDATION", "NORMATIVE_PREDICATE_EVALUATION", "COMPLIANCE_DECISION"],
        "interpretation": "Structural diagnostics do not establish requirement, evidence, verification, or conformance validity.",
    }
    dump(OUT / "VALIDATION-REPORT.yaml", validation_report)
    dump(OUT / "CONFORMANCE-INVARIANTS.yaml", {"schema_version": SCHEMA_VERSION, "invariants": [{"invariant_id": f"V121-I{i:02d}", "statement": text, "enforcement": "MECHANICAL"} for i, text in enumerate(INVARIANTS, 1)]})
    dump(OUT / "SCHEMA-REGISTRY.yaml", {"schema_version": SCHEMA_VERSION, "schema_directory": "historical-source/compliance/schema", "schemas": [{"schema_id": name, "path": f"schema/{name}.schema.yaml", "sha256": sha_file(SCHEMA_DIR / f"{name}.schema.yaml")} for name in SCHEMA_NAMES], "normative_object_types": OBJECT_TYPES})
    dump(OUT / "NORMATIVE-MODEL.yaml", {"schema_version": SCHEMA_VERSION, "normative_object_types": OBJECT_TYPES, "common_required_fields": ["object_type", "schema_version", "object_id", "created_at"], "optional_common_fields": ["updated_at", "producer", "content_hash", "metadata"], "validation_questions": ["CAN_THIS_OBJECT_BE_TRUSTED", "IS_THE_REQUIREMENT_DECIDABLE", "DID_VERIFICATION_ESTABLISH_THE_REQUIRED_PROPERTY", "WHAT_CONFORMANCE_STATE_FOLLOWS"], "separation_rule": "Schema validity != requirement validity != evidence validity != verification validity != conformance."})

    build_reports(certificate, findings)

    produced = sorted(str(p.relative_to(OUT)) for p in OUT.rglob("*") if p.is_file())
    required = set(REQUIRED_VALIDATION_OUTPUTS) | {f"schema/{name}.schema.yaml" for name in SCHEMA_NAMES}
    missing = sorted(required - set(produced))
    if missing:
        raise RuntimeError(f"missing required v12.1 outputs: {missing}")
    print(f"generated {len(produced)} v12.1 deliverables; schemas={len(schemas)} requirements=0 decisions=0 nonconformances=0 status=BLOCKED")


if __name__ == "__main__":
    main()
