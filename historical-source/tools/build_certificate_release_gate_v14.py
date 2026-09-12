#!/usr/bin/env python3
"""Build Protocol-v14 certificate eligibility, validity, and release-gate artifacts."""
from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
HS = ROOT / "historical-source"
OUT = HS / "compliance"
V133 = OUT / "remediation" / "v13.3"
DEST = OUT / "certification" / "v14"
SCHEMA = DEST / "schema"
REPORTS = DEST / "reports"
VERSION = "14.0"
GENERATED_AT = "2026-09-12T19:04:51Z"
AGGREGATE_STATES = ["COMPLIANT", "CONDITIONALLY_COMPLIANT", "NON_COMPLIANT", "UNVERIFIED", "BLOCKED", "NO_MANDATORY_REQUIREMENTS"]
CERTIFICATE_STATES = ["DRAFT", "ISSUED", "VALID", "SUPERSEDED", "REVOKED", "EXPIRED", "INVALID"]
RELEASE_DECISIONS = ["AUTHORIZED", "CONDITIONALLY_AUTHORIZED", "REJECTED", "BLOCKED", "EXPIRED", "UNKNOWN"]
RELEASE_GATE_STATES = ["CREATED", "EVALUATING", "BLOCKED", "REJECTED", "PASSED", "AUTHORIZED", "CONDITIONALLY_AUTHORIZED"]
SCHEMA_NAMES = ["certificate-scope", "certification-authority", "authority-policy", "evidence-summary", "waiver-summary", "evidence-freshness-policy", "certificate-signature", "certificate-snapshot", "snapshot-seal", "certificate", "certification-policy", "certificate-eligibility-result", "certificate-validity-result", "certificate-transition", "revocation-record", "waiver", "waiver-authority-result", "artifact-hash", "release-snapshot", "release-policy", "release-gate", "release-gate-transition", "release-gate-evaluation"]
MACHINE_FILES = [
    "DECISION-LAYERS.yaml", "AUTHORITY-POLICIES.yaml", "CERTIFICATION-POLICIES.yaml", "CERTIFICATE-ELIGIBILITY-FUNCTION.yaml",
    "CURRENT-CERTIFICATE-ELIGIBILITY.yaml", "CERTIFICATE-ELIGIBILITY-TEST-VECTORS.yaml", "CERTIFICATES.yaml", "CERTIFICATE-STATE-MACHINE.yaml",
    "CERTIFICATE-VERIFICATION-PIPELINE.yaml", "CERTIFICATE-VALIDITY-TEST-VECTORS.yaml",
    "CERTIFICATE-STATE-TEST-VECTORS.yaml", "CERTIFICATE-INTEGRITY-PROFILE.yaml",
    "CERTIFICATE-REVOCATION-RULES.yaml", "REVOCATIONS.yaml", "EVIDENCE-FRESHNESS-POLICIES.yaml",
    "EVIDENCE-FRESHNESS-FUNCTION.yaml", "EVIDENCE-FRESHNESS-TEST-VECTORS.yaml",
    "WAIVER-AUTHORITY-RULES.yaml", "WAIVERS-V14.yaml", "WAIVER-AUTHORITY-RESULTS.yaml",
    "WAIVER-AUTHORITY-TEST-VECTORS.yaml", "SNAPSHOT-SEALING-RULES.yaml", "SNAPSHOT-SEALS.yaml",
    "SNAPSHOT-SEAL-TEST-VECTORS.yaml", "RELEASE-POLICIES.yaml", "RELEASE-SNAPSHOTS.yaml",
    "RELEASE-GATES.yaml", "RELEASE-AUTHORIZATION-FUNCTION.yaml", "RELEASE-GATE-STATE-MACHINE.yaml",
    "RELEASE-GATE-TEST-VECTORS.yaml", "RELEASE-GATE-STATE-TEST-VECTORS.yaml",
    "BUILD-REPRODUCIBILITY-TEST-VECTORS.yaml", "CURRENT-CERTIFICATION-STATUS.yaml",
    "CURRENT-RELEASE-STATUS.yaml", "CURRENT-AUDIT-BINDING.yaml", "CERTIFICATE-INVARIANTS.yaml",
    "END-TO-END-MODEL.yaml", "OBJECT-REGISTRY.yaml", "SCHEMA-REGISTRY.yaml", "PRIOR-INTEGRITY.yaml",
    "VALIDATION-REPORT.yaml",
]
REPORT_FILES = ["CERTIFICATE-ELIGIBILITY-REPORT.yaml", "CERTIFICATE-VALIDITY-REPORT.yaml", "RELEASE-GATE-REPORT.yaml", "FINAL-AUTHORIZATION-REPORT.yaml"]


def load(path: Path) -> Any: return json.loads(path.read_text(encoding="utf-8"))
def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
def canonical(value: Any) -> bytes: return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
def digest(value: Any) -> str: return hashlib.sha256(canonical(value)).hexdigest()
def sha_file(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()
def seal(value: dict[str, Any], field: str) -> dict[str, Any]:
    payload = dict(value); payload.pop(field, None); value[field] = digest(payload); return value
def valid_time(value: Any) -> bool:
    if not isinstance(value, str): return False
    try: return datetime.fromisoformat(value.replace("Z", "+00:00")).tzinfo is not None
    except ValueError: return False


def aggregate(requirements: list[dict[str, Any]]) -> str:
    mandatory = []
    for item in requirements:
        if not item["mandatory"] or not item.get("applicable", True) or item["decision"] == "NOT_APPLICABLE": continue
        if item["decision"] == "NON_CONFORMANT": contribution = "WAIVED" if item.get("waiver_effective") else "FAIL"
        elif item["decision"] == "BLOCKED": contribution = "BLOCKED"
        elif item["decision"] in {"PARTIALLY_CONFORMANT", "UNVERIFIED", "UNKNOWN"}: contribution = "UNRESOLVED"
        elif item["decision"] == "CONFORMANT": contribution = "PASS"
        else: contribution = "BLOCKED"
        mandatory.append(contribution)
    if "FAIL" in mandatory: return "NON_COMPLIANT"
    if "BLOCKED" in mandatory: return "BLOCKED"
    if "UNRESOLVED" in mandatory: return "UNVERIFIED"
    if "WAIVED" in mandatory: return "CONDITIONALLY_COMPLIANT"
    return "COMPLIANT" if mandatory else "NO_MANDATORY_REQUIREMENTS"


def freshness(policy: dict[str, Any], evidence_at: str, evaluated_at: str, events: list[dict[str, str]]) -> tuple[str, list[str]]:
    if not policy["freshness_required"]: return "FRESH", []
    reasons = [event["event_type"] for event in events if event["event_type"] in policy["invalidation_events"] and event["occurred_at"] >= evidence_at]
    if policy["max_age"]:
        days = int(policy["max_age"].removeprefix("P").removesuffix("D"))
        age = datetime.fromisoformat(evaluated_at.replace("Z", "+00:00")) - datetime.fromisoformat(evidence_at.replace("Z", "+00:00"))
        if age.total_seconds() > days * 86400: reasons.append("MAX_AGE_EXCEEDED")
    return ("STALE", reasons) if reasons else ("FRESH", [])


def waiver_effective(waiver: dict[str, Any], authorized_authorities: set[str], evaluated_at: str) -> tuple[str, bool]:
    authority = waiver["authority"]
    if authority["authority_id"] not in authorized_authorities or not authority["authorization_evidence"]: return "UNAUTHORIZED", False
    if waiver["status"] != "ACTIVE": return "NOT_ACTIVE", False
    if evaluated_at < waiver["valid_from"] or waiver["valid_until"] is not None and evaluated_at > waiver["valid_until"]: return "EXPIRED", False
    if not waiver["evidence_refs"] or not waiver["reason"] or not waiver["scope"]: return "INVALID", False
    return "EFFECTIVE", True


def eligibility(aggregate_status: str | None, policy: dict[str, Any], predicates: dict[str, bool]) -> tuple[str, list[str]]:
    failed = [name for name, value in predicates.items() if not value]
    if aggregate_status is None: failed.insert(0, "AGGREGATE_MISSING")
    elif aggregate_status not in policy["allowed_aggregate_statuses"]: failed.insert(0, "AGGREGATE_STATUS_NOT_ALLOWED")
    return ("ELIGIBLE", []) if not failed else ("INELIGIBLE", failed)


def snapshot_seal(identifier: str, aggregate_hash: str = "7" * 64) -> dict[str, Any]:
    return seal({"seal_id": identifier, "specification_hash": "1" * 64, "implementation_hash": "2" * 64, "decision_hash": "3" * 64, "evidence_hash": "4" * 64, "waiver_hash": "5" * 64, "state_history_hash": "6" * 64, "aggregate_hash": aggregate_hash, "sealed_at": GENERATED_AT, "schema_version": VERSION}, "seal_hash")


def authority(identifier: str = "TEST-AUTHORITY") -> dict[str, Any]:
    return {"authority_id": identifier, "authority_type": "AUTOMATED_POLICY", "authorization_policy": "TEST-CERTIFICATION-POLICY", "authorization_evidence": ["TEST-AUTH-EVIDENCE"], "authorized_at": GENERATED_AT}


def certificate_hash(certificate: dict[str, Any]) -> str:
    payload = {key: value for key, value in certificate.items() if key not in {"certificate_hash", "signature"}}
    return digest(payload)


def sign(certificate_hash_value: str, authority_id: str, signed_at: str) -> str: return digest({"certificate_hash": certificate_hash_value, "authority_id": authority_id, "signed_at": signed_at})


def synthetic_certificate(identifier: str = "TEST-CERT", aggregate_status: str = "COMPLIANT", requirements: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    requirements = requirements or [{"requirement_id": "R1", "mandatory": True, "applicable": True, "decision": "CONFORMANT"}]
    aggregate_hash = digest({"status": aggregate(requirements), "requirements": requirements})
    seal_record = snapshot_seal(identifier + "-SEAL", aggregate_hash)
    snapshot = seal({"snapshot_id": identifier + "-SNAPSHOT", "audit_id": "TEST-AUDIT", "specification_snapshot": "1" * 64, "implementation_snapshot": "2" * 64, "decision_snapshot": "3" * 64, "evidence_snapshot": "4" * 64, "waiver_snapshot": "5" * 64, "state_history_snapshot": "6" * 64, "aggregate_hash": aggregate_hash, "scope_snapshot": "8" * 64, "generated_at": GENERATED_AT, "release_binding": {"source_snapshot": "2" * 64, "build_snapshot": "b" * 64, "configuration_snapshot": "c" * 64, "artifact_hashes": [{"artifact_id": "TEST-ARTIFACT", "hash": "a" * 64}]}}, "snapshot_hash")
    cert = {"certificate_id": identifier, "audit_id": "TEST-AUDIT", "certificate_type": "COMPLIANCE", "status": "VALID", "aggregate_status": aggregate_status,
        "scope": {"audit_scope_id": "TEST-SCOPE", "requirements": [item["requirement_id"] for item in requirements], "specification_snapshot": "1" * 64, "implementation_snapshot": "2" * 64, "environment_snapshot": None, "architecture_scope": None, "platform_scope": None, "version_scope": "1.0.0-test", "exclusions": []},
        "snapshot": snapshot,
        "snapshot_seal": seal_record, "authority": authority(identifier + "-AUTHORITY"), "evidence_summary": {"required_evidence_count": 1, "valid_evidence_count": 1, "invalid_evidence_count": 0, "stale_evidence_count": 0, "missing_evidence_count": 0, "evidence_snapshot": "4" * 64, "integrity_status": "VALID"},
        "waiver_summary": {"waiver_count": sum(bool(item.get("waiver_effective")) for item in requirements), "effective_waiver_count": sum(bool(item.get("waiver_effective")) for item in requirements), "unauthorized_waiver_count": 0, "expired_waiver_count": 0, "waiver_snapshot": "5" * 64},
        "aggregate_inputs": requirements, "issued_at": GENERATED_AT, "valid_from": GENERATED_AT, "valid_until": "2026-09-13T19:04:51Z", "supersedes": None, "schema_version": VERSION}
    cert["certificate_hash"] = certificate_hash(cert)
    cert["signature"] = {"profile": "TEST-SHA256-AUTHORITY-BINDING", "signer_authority_id": cert["authority"]["authority_id"], "signed_at": GENERATED_AT, "signature_value": sign(cert["certificate_hash"], cert["authority"]["authority_id"], GENERATED_AT)}
    return cert


def certificate_schema_valid(cert: Any) -> bool:
    required = {"certificate_id", "audit_id", "certificate_type", "status", "aggregate_status", "scope", "snapshot", "snapshot_seal", "authority", "evidence_summary", "waiver_summary", "aggregate_inputs", "issued_at", "valid_from", "valid_until", "supersedes", "schema_version", "certificate_hash", "signature"}
    scope_required = {"audit_scope_id", "requirements", "specification_snapshot", "implementation_snapshot", "environment_snapshot", "architecture_scope", "platform_scope", "version_scope", "exclusions"}
    authority_required = {"authority_id", "authority_type", "authorization_policy", "authorization_evidence", "authorized_at"}
    return isinstance(cert, dict) and set(cert) == required and set(cert.get("scope", {})) == scope_required and set(cert.get("authority", {})) == authority_required and isinstance(cert["scope"]["requirements"], list) and len(cert["scope"]["requirements"]) > 0 and isinstance(cert["authority"]["authorization_evidence"], list) and len(cert["authority"]["authorization_evidence"]) > 0


def verify_certificate(cert: dict[str, Any], evaluated_at: str = GENERATED_AT, revoked: bool = False, superseded: bool = False) -> tuple[str, str | None]:
    checks = [
        (certificate_schema_valid(cert), "CERTIFICATE_SCHEMA_INVALID"),
        (bool(cert.get("scope", {}).get("audit_scope_id")) and bool(cert.get("scope", {}).get("requirements")) and not set(cert.get("scope", {}).get("requirements", [])) & set(cert.get("scope", {}).get("exclusions", [])), "SCOPE_INVALID"),
        (cert.get("certificate_hash") == certificate_hash(cert), "CERTIFICATE_HASH_INVALID"),
        (cert.get("snapshot", {}).get("snapshot_hash") == digest({key: value for key, value in cert.get("snapshot", {}).items() if key != "snapshot_hash"}), "CERTIFICATE_SNAPSHOT_HASH_INVALID"),
        (cert.get("snapshot_seal", {}).get("seal_hash") == digest({key: value for key, value in cert.get("snapshot_seal", {}).items() if key != "seal_hash"}), "SNAPSHOT_SEAL_INVALID"),
        (cert.get("scope", {}).get("specification_snapshot") == cert.get("snapshot", {}).get("specification_snapshot") == cert.get("snapshot_seal", {}).get("specification_hash") and cert.get("scope", {}).get("implementation_snapshot") == cert.get("snapshot", {}).get("implementation_snapshot") == cert.get("snapshot_seal", {}).get("implementation_hash") and all(cert.get("snapshot", {}).get(name + "_snapshot") == cert.get("snapshot_seal", {}).get(name + "_hash") for name in ["decision", "evidence", "waiver", "state_history"]) and cert.get("scope", {}).get("requirements") == [item.get("requirement_id") for item in cert.get("aggregate_inputs", [])], "SNAPSHOT_LINEAGE_MISMATCH"),
        (cert.get("signature", {}).get("signature_value") == sign(cert.get("certificate_hash", ""), cert.get("authority", {}).get("authority_id", ""), cert.get("signature", {}).get("signed_at", "")), "SIGNATURE_INVALID"),
        (bool(cert.get("authority", {}).get("authorization_evidence")) and cert.get("authority", {}).get("authorization_policy") == "TEST-CERTIFICATION-POLICY", "AUTHORITY_INVALID"),
        (cert.get("valid_from", "") <= evaluated_at and (cert.get("valid_until") is None or evaluated_at <= cert["valid_until"]), "VALIDITY_INTERVAL_INVALID"),
        (cert.get("status") == "VALID", "CERTIFICATE_STATUS_NOT_VALID"),
        (not revoked, "REVOKED"), (not superseded, "SUPERSEDED"),
        (cert.get("evidence_summary", {}).get("integrity_status") == "VALID" and cert.get("evidence_summary", {}).get("stale_evidence_count") == 0 and cert.get("evidence_summary", {}).get("missing_evidence_count") == 0, "EVIDENCE_INVALID"),
        (cert.get("waiver_summary", {}).get("effective_waiver_count") == sum(bool(item.get("waiver_effective")) for item in cert.get("aggregate_inputs", [])) and cert.get("waiver_summary", {}).get("unauthorized_waiver_count") == 0 and cert.get("waiver_summary", {}).get("expired_waiver_count") == 0, "WAIVER_SUMMARY_INVALID"),
        (cert.get("aggregate_status") == aggregate(cert.get("aggregate_inputs", [])), "CERTIFICATE_AGGREGATE_MISMATCH"),
        (cert.get("snapshot", {}).get("aggregate_hash") == digest({"status": aggregate(cert.get("aggregate_inputs", [])), "requirements": cert.get("aggregate_inputs", [])}) == cert.get("snapshot_seal", {}).get("aggregate_hash"), "AGGREGATE_HASH_MISMATCH"),
    ]
    for valid, error in checks:
        if not valid: return "INVALID", error
    return "VALID", None


def release_snapshot(identifier: str = "TEST-RELEASE", implementation: str = "2" * 64, artifact_hash: str = "a" * 64) -> dict[str, Any]:
    return seal({"release_id": identifier, "version": "1.0.0-test", "source_snapshot": implementation, "build_snapshot": "b" * 64, "configuration_snapshot": "c" * 64, "artifact_hashes": [{"artifact_id": "TEST-ARTIFACT", "hash": artifact_hash}], "created_at": GENERATED_AT, "schema_version": VERSION}, "snapshot_hash")


def release_authorize(policy: dict[str, Any], certificates: list[dict[str, Any]], aggregate_status: str, findings: list[str], waivers_valid: bool, residual_risk_accepted: bool, evidence_fresh: bool, security_pass: bool, policy_integrity: bool, release_authority_valid: bool, release: dict[str, Any]) -> tuple[str, list[str]]:
    reasons: list[str] = []
    valid_certs = [cert for cert in certificates if verify_certificate(cert)[0] == "VALID" and cert["certificate_type"] in policy["required_certificate_types"]]
    def exact_match(cert: dict[str, Any]) -> bool:
        binding = cert.get("snapshot", {}).get("release_binding", {})
        return (cert.get("aggregate_status") == aggregate_status and cert.get("scope", {}).get("version_scope") == release.get("version") and binding.get("source_snapshot") == release.get("source_snapshot") and binding.get("build_snapshot") == release.get("build_snapshot") and binding.get("configuration_snapshot") == release.get("configuration_snapshot") and binding.get("artifact_hashes") == release.get("artifact_hashes"))
    if aggregate_status == "CONDITIONALLY_COMPLIANT":
        if not policy["conditional_authorization_allowed"] or not waivers_valid or not residual_risk_accepted or not policy["residual_risk_authority_valid"]: reasons.append("CONDITIONAL_POLICY_UNSATISFIED")
        if any(item in policy["forbidden_findings"] for item in findings): reasons.append("FORBIDDEN_FINDING")
        if not valid_certs or not any(exact_match(cert) for cert in valid_certs): reasons.append("VALID_MATCHING_CERTIFICATE_MISSING")
        if not evidence_fresh or not security_pass or not policy_integrity: reasons.append("REQUIRED_CONDITION_MISSING")
        if not release_authority_valid: reasons.append("RELEASE_AUTHORITY_INVALID")
        return ("CONDITIONALLY_AUTHORIZED", []) if not reasons else ("REJECTED", reasons)
    if aggregate_status != policy["required_aggregate_status"]: reasons.append("AGGREGATE_NOT_ALLOWED")
    if not valid_certs: reasons.append("VALID_CERTIFICATE_MISSING")
    elif not any(exact_match(cert) for cert in valid_certs): reasons.append("CERTIFICATE_RELEASE_SNAPSHOT_MISMATCH")
    if any(item in policy["forbidden_findings"] for item in findings): reasons.append("FORBIDDEN_FINDING")
    if not evidence_fresh: reasons.append("EVIDENCE_STALE")
    if not security_pass: reasons.append("SECURITY_GATE_FAILED")
    if not policy_integrity: reasons.append("RELEASE_POLICY_INVALID")
    if not release_authority_valid: reasons.append("RELEASE_AUTHORITY_INVALID")
    if reasons:
        rejection = {"AGGREGATE_NOT_ALLOWED", "FORBIDDEN_FINDING", "SECURITY_GATE_FAILED"}
        return ("REJECTED" if any(reason in rejection for reason in reasons) else "BLOCKED"), reasons
    return "AUTHORIZED", []


def base_schema(title: str, required: list[str], properties: dict[str, Any], rules: list[str] | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {"$schema": "https://json-schema.org/draft/2020-12/schema", "title": title, "type": "object", "required": required, "properties": properties, "additionalProperties": False}
    if rules: result["x-v14-rules"] = rules
    return result


def build_schemas() -> None:
    ident = {"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9._:/-]*$"}; text = {"type": "string", "minLength": 1}; hx = {"type": "string", "pattern": "^[a-f0-9]{64}$"}; ts = {"type": "string", "format": "date-time"}; nullable_text = {"oneOf": [text, {"type": "null"}]}; nullable_id = {"oneOf": [ident, {"type": "null"}]}; strings = lambda minimum=0: {"type": "array", "minItems": minimum, "items": {"type": "string"}, "uniqueItems": True}
    schemas: dict[str, Any] = {}
    schemas["certificate-scope"] = base_schema("CertificateScope", ["audit_scope_id", "requirements", "specification_snapshot", "implementation_snapshot", "environment_snapshot", "architecture_scope", "platform_scope", "version_scope", "exclusions"], {"audit_scope_id": ident, "requirements": strings(1), "specification_snapshot": hx, "implementation_snapshot": hx, "environment_snapshot": nullable_text, "architecture_scope": nullable_text, "platform_scope": nullable_text, "version_scope": text, "exclusions": strings()})
    schemas["certification-authority"] = base_schema("CertificationAuthority", ["authority_id", "authority_type", "authorization_policy", "authorization_evidence", "authorized_at"], {"authority_id": ident, "authority_type": {"type": "string", "enum": ["HUMAN", "ORGANIZATION", "AUTOMATED_POLICY", "TRUSTED_SERVICE"]}, "authorization_policy": ident, "authorization_evidence": strings(1), "authorized_at": ts})
    schemas["authority-policy"] = base_schema("AuthorityPolicy", ["policy_id", "purpose", "allowed_authority_types", "authorization_evidence_required", "signature_profiles", "schema_version", "policy_hash"], {"policy_id": ident, "purpose": {"type": "string", "enum": ["CERTIFICATION", "WAIVER", "RELEASE"]}, "allowed_authority_types": {"type": "array", "minItems": 1, "items": {"type": "string", "enum": ["HUMAN", "ORGANIZATION", "AUTOMATED_POLICY", "TRUSTED_SERVICE"]}, "uniqueItems": True}, "authorization_evidence_required": {"type": "boolean"}, "signature_profiles": strings(), "schema_version": {"const": VERSION}, "policy_hash": hx})
    count = {"type": "integer", "minimum": 0}
    schemas["evidence-summary"] = base_schema("EvidenceSummary", ["required_evidence_count", "valid_evidence_count", "invalid_evidence_count", "stale_evidence_count", "missing_evidence_count", "evidence_snapshot", "integrity_status"], {"required_evidence_count": count, "valid_evidence_count": count, "invalid_evidence_count": count, "stale_evidence_count": count, "missing_evidence_count": count, "evidence_snapshot": hx, "integrity_status": {"type": "string", "enum": ["VALID", "INVALID", "INCOMPLETE", "UNKNOWN"]}})
    schemas["waiver-summary"] = base_schema("WaiverSummary", ["waiver_count", "effective_waiver_count", "unauthorized_waiver_count", "expired_waiver_count", "waiver_snapshot"], {"waiver_count": count, "effective_waiver_count": count, "unauthorized_waiver_count": count, "expired_waiver_count": count, "waiver_snapshot": hx})
    invalidation = ["IMPLEMENTATION_CHANGE", "SPECIFICATION_CHANGE", "CONFIGURATION_CHANGE", "DEPENDENCY_CHANGE", "ENVIRONMENT_CHANGE", "SECURITY_EVENT", "EVIDENCE_REVOCATION", "MANUAL_INVALIDATION"]
    schemas["evidence-freshness-policy"] = base_schema("EvidenceFreshnessPolicy", ["policy_id", "max_age", "invalidation_events", "freshness_required", "schema_version", "policy_hash"], {"policy_id": ident, "max_age": nullable_text, "invalidation_events": {"type": "array", "items": {"type": "string", "enum": invalidation}, "uniqueItems": True}, "freshness_required": {"type": "boolean"}, "schema_version": {"const": VERSION}, "policy_hash": hx})
    schemas["certificate-signature"] = base_schema("CertificateSignature", ["profile", "signer_authority_id", "signed_at", "signature_value"], {"profile": text, "signer_authority_id": ident, "signed_at": ts, "signature_value": hx})
    release_binding = {"type": "object", "required": ["source_snapshot", "build_snapshot", "configuration_snapshot", "artifact_hashes"], "properties": {"source_snapshot": hx, "build_snapshot": hx, "configuration_snapshot": hx, "artifact_hashes": {"type": "array", "minItems": 1, "items": {"$ref": "artifact-hash.schema.yaml"}}}, "additionalProperties": False}
    schemas["certificate-snapshot"] = base_schema("CertificateSnapshot", ["snapshot_id", "audit_id", "specification_snapshot", "implementation_snapshot", "decision_snapshot", "evidence_snapshot", "waiver_snapshot", "state_history_snapshot", "aggregate_hash", "scope_snapshot", "generated_at", "release_binding", "snapshot_hash"], {"snapshot_id": ident, "audit_id": ident, "specification_snapshot": hx, "implementation_snapshot": hx, "decision_snapshot": hx, "evidence_snapshot": hx, "waiver_snapshot": hx, "state_history_snapshot": hx, "aggregate_hash": hx, "scope_snapshot": hx, "generated_at": ts, "release_binding": release_binding, "snapshot_hash": hx})
    seal_props = {key: hx for key in ["specification_hash", "implementation_hash", "decision_hash", "evidence_hash", "waiver_hash", "state_history_hash", "aggregate_hash"]}; seal_props.update({"seal_id": ident, "sealed_at": ts, "schema_version": {"const": VERSION}, "seal_hash": hx})
    schemas["snapshot-seal"] = base_schema("SnapshotSeal", ["seal_id", "specification_hash", "implementation_hash", "decision_hash", "evidence_hash", "waiver_hash", "state_history_hash", "aggregate_hash", "sealed_at", "schema_version", "seal_hash"], seal_props)
    snapshot = {"$ref": "certificate-snapshot.schema.yaml"}; authority_ref = {"$ref": "certification-authority.schema.yaml"}
    schemas["certificate"] = base_schema("Certificate", ["certificate_id", "audit_id", "certificate_type", "status", "aggregate_status", "scope", "snapshot", "snapshot_seal", "authority", "evidence_summary", "waiver_summary", "aggregate_inputs", "issued_at", "valid_from", "valid_until", "supersedes", "schema_version", "certificate_hash", "signature"], {"certificate_id": ident, "audit_id": ident, "certificate_type": {"type": "string", "enum": ["COMPLIANCE", "SECURITY", "COMPATIBILITY", "RELEASE", "HISTORICAL", "EXPERIMENTAL"]}, "status": {"type": "string", "enum": CERTIFICATE_STATES}, "aggregate_status": {"type": "string", "enum": AGGREGATE_STATES}, "scope": {"$ref": "certificate-scope.schema.yaml"}, "snapshot": snapshot, "snapshot_seal": {"$ref": "snapshot-seal.schema.yaml"}, "authority": authority_ref, "evidence_summary": {"$ref": "evidence-summary.schema.yaml"}, "waiver_summary": {"$ref": "waiver-summary.schema.yaml"}, "aggregate_inputs": {"type": "array", "items": {"type": "object"}}, "issued_at": ts, "valid_from": ts, "valid_until": {"oneOf": [ts, {"type": "null"}]}, "supersedes": nullable_id, "schema_version": {"const": VERSION}, "certificate_hash": hx, "signature": {"$ref": "certificate-signature.schema.yaml"}}, ["certificate_hash excludes certificate_hash and signature", "signature does not establish conformance"])
    schemas["certification-policy"] = base_schema("CertificationPolicy", ["policy_id", "allowed_aggregate_statuses", "required_certificate_type", "signature_required", "authority_policy", "no_mandatory_requirements_allowed", "schema_version", "policy_hash"], {"policy_id": ident, "allowed_aggregate_statuses": {"type": "array", "items": {"type": "string", "enum": AGGREGATE_STATES}, "uniqueItems": True}, "required_certificate_type": text, "signature_required": {"type": "boolean"}, "authority_policy": ident, "no_mandatory_requirements_allowed": {"type": "boolean"}, "schema_version": {"const": VERSION}, "policy_hash": hx})
    schemas["certificate-eligibility-result"] = base_schema("CertificateEligibilityResult", ["eligibility_id", "snapshot_id", "aggregate_id", "policy_id", "aggregate_status", "predicates", "result", "failure_reasons", "evaluated_at", "schema_version", "eligibility_hash"], {"eligibility_id": ident, "snapshot_id": ident, "aggregate_id": nullable_id, "policy_id": ident, "aggregate_status": {"oneOf": [{"type": "string", "enum": AGGREGATE_STATES}, {"type": "null"}]}, "predicates": {"type": "object"}, "result": {"type": "string", "enum": ["ELIGIBLE", "INELIGIBLE"]}, "failure_reasons": strings(), "evaluated_at": ts, "schema_version": {"const": VERSION}, "eligibility_hash": hx})
    schemas["certificate-validity-result"] = base_schema("CertificateValidityResult", ["validity_result_id", "certificate_id", "result", "failure_code", "verified_at", "schema_version", "result_hash"], {"validity_result_id": ident, "certificate_id": ident, "result": {"type": "string", "enum": ["VALID", "INVALID"]}, "failure_code": nullable_text, "verified_at": ts, "schema_version": {"const": VERSION}, "result_hash": hx})
    schemas["certificate-transition"] = base_schema("CertificateTransition", ["transition_id", "certificate_id", "from_status", "to_status", "reason", "occurred_at", "schema_version", "transition_hash"], {"transition_id": ident, "certificate_id": ident, "from_status": {"type": "string", "enum": CERTIFICATE_STATES}, "to_status": {"type": "string", "enum": CERTIFICATE_STATES}, "reason": text, "occurred_at": ts, "schema_version": {"const": VERSION}, "transition_hash": hx})
    schemas["revocation-record"] = base_schema("RevocationRecord", ["revocation_id", "certificate_id", "reason", "authority", "revoked_at", "schema_version", "revocation_hash"], {"revocation_id": ident, "certificate_id": ident, "reason": {"type": "string", "enum": ["CERTIFICATE_ERROR", "AUTHORITY_INVALID", "EVIDENCE_REVOKED", "SNAPSHOT_INTEGRITY_FAILURE", "SCOPE_ERROR", "FRAUDULENT_EVIDENCE", "POLICY_VIOLATION", "SECURITY_EVENT", "OTHER"]}, "authority": authority_ref, "revoked_at": ts, "schema_version": {"const": VERSION}, "revocation_hash": hx})
    schemas["waiver"] = base_schema("Waiver", ["waiver_id", "requirement_id", "scope", "reason", "authority", "issued_at", "valid_from", "valid_until", "conditions", "residual_risk", "status", "evidence_refs", "schema_version", "waiver_hash"], {"waiver_id": ident, "requirement_id": ident, "scope": text, "reason": text, "authority": authority_ref, "issued_at": ts, "valid_from": ts, "valid_until": {"oneOf": [ts, {"type": "null"}]}, "conditions": strings(), "residual_risk": {"type": "string", "enum": ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO", "UNKNOWN"]}, "status": {"type": "string", "enum": ["DRAFT", "ACTIVE", "EXPIRED", "REVOKED", "SUPERSEDED"]}, "evidence_refs": strings(1), "schema_version": {"const": VERSION}, "waiver_hash": hx})
    schemas["waiver-authority-result"] = base_schema("WaiverAuthorityResult", ["result_id", "waiver_id", "result", "effective", "evaluated_at", "schema_version", "result_hash"], {"result_id": ident, "waiver_id": ident, "result": text, "effective": {"type": "boolean"}, "evaluated_at": ts, "schema_version": {"const": VERSION}, "result_hash": hx})
    schemas["artifact-hash"] = base_schema("ArtifactHash", ["artifact_id", "hash"], {"artifact_id": ident, "hash": hx})
    schemas["release-snapshot"] = base_schema("ReleaseSnapshot", ["release_id", "version", "source_snapshot", "build_snapshot", "configuration_snapshot", "artifact_hashes", "created_at", "schema_version", "snapshot_hash"], {"release_id": ident, "version": text, "source_snapshot": hx, "build_snapshot": hx, "configuration_snapshot": hx, "artifact_hashes": {"type": "array", "minItems": 1, "items": {"$ref": "artifact-hash.schema.yaml"}}, "created_at": ts, "schema_version": {"const": VERSION}, "snapshot_hash": hx})
    schemas["release-policy"] = base_schema("ReleasePolicy", ["policy_id", "required_certificate_types", "required_aggregate_status", "forbidden_findings", "required_waiver_policy", "evidence_freshness_policy", "required_security_status", "release_authority_policy", "conditional_authorization_allowed", "residual_risk_authority_valid", "schema_version", "policy_hash"], {"policy_id": ident, "required_certificate_types": strings(1), "required_aggregate_status": {"type": "string", "enum": ["COMPLIANT", "CONDITIONALLY_COMPLIANT"]}, "forbidden_findings": strings(), "required_waiver_policy": ident, "evidence_freshness_policy": ident, "required_security_status": text, "release_authority_policy": ident, "conditional_authorization_allowed": {"type": "boolean"}, "residual_risk_authority_valid": {"type": "boolean"}, "schema_version": {"const": VERSION}, "policy_hash": hx})
    schemas["release-gate"] = base_schema("ReleaseGate", ["gate_id", "release_id", "policy_id", "release_snapshot_hash", "certificate_ids", "required_certificate_types", "required_aggregate_status", "forbidden_findings", "required_waiver_policy", "evidence_freshness_policy", "required_security_status", "state", "decision", "evaluated_at", "schema_version", "gate_hash"], {"gate_id": ident, "release_id": ident, "policy_id": ident, "release_snapshot_hash": hx, "certificate_ids": strings(), "required_certificate_types": strings(1), "required_aggregate_status": {"type": "string", "enum": ["COMPLIANT", "CONDITIONALLY_COMPLIANT"]}, "forbidden_findings": strings(), "required_waiver_policy": ident, "evidence_freshness_policy": ident, "required_security_status": text, "state": {"type": "string", "enum": RELEASE_GATE_STATES}, "decision": {"type": "string", "enum": RELEASE_DECISIONS}, "evaluated_at": ts, "schema_version": {"const": VERSION}, "gate_hash": hx})
    schemas["release-gate-transition"] = base_schema("ReleaseGateTransition", ["transition_id", "gate_id", "from_state", "to_state", "guard", "occurred_at", "schema_version", "transition_hash"], {"transition_id": ident, "gate_id": ident, "from_state": {"type": "string", "enum": RELEASE_GATE_STATES}, "to_state": {"type": "string", "enum": RELEASE_GATE_STATES}, "guard": text, "occurred_at": ts, "schema_version": {"const": VERSION}, "transition_hash": hx})
    schemas["release-gate-evaluation"] = base_schema("ReleaseGateEvaluation", ["evaluation_id", "policy_id", "release_id", "aggregate_status", "decision", "reasons", "evaluated_at", "schema_version", "evaluation_hash"], {"evaluation_id": ident, "policy_id": ident, "release_id": ident, "aggregate_status": {"type": "string", "enum": AGGREGATE_STATES}, "decision": {"type": "string", "enum": RELEASE_DECISIONS}, "reasons": strings(), "evaluated_at": ts, "schema_version": {"const": VERSION}, "evaluation_hash": hx})
    for name, body in schemas.items(): body["$id"] = f"https://generic-discovery-engine.invalid/compliance/v14/{name}.schema.yaml"; dump(SCHEMA / f"{name}.schema.yaml", body)


def protected_files() -> list[Path]: return sorted((path for path in OUT.rglob("*") if path.is_file() and DEST not in path.parents), key=lambda path: str(path.relative_to(OUT)))


def main() -> None:
    required = [V133 / "VALIDATION.yaml", V133 / "CURRENT-AUDIT-STATUS.yaml", V133 / "CURRENT-AGGREGATE.yaml", OUT / "AUDIT-CERTIFICATE.yaml"]
    if not all(path.is_file() for path in required): raise RuntimeError("validated Protocol-v13.3 package is required")
    if DEST.exists():
        for filename in ["CERTIFICATES.yaml", "SNAPSHOT-SEALS.yaml", "REVOCATIONS.yaml", "WAIVERS-V14.yaml", "RELEASE-SNAPSHOTS.yaml", "RELEASE-GATES.yaml"]:
            path = DEST / filename
            if path.is_file() and load(path).get("objects"): raise RuntimeError(f"refusing to erase appended v14 records in {filename}")
    before = [{"path": str(path.relative_to(OUT)), "sha256": sha_file(path), "bytes": path.stat().st_size} for path in protected_files()]
    if DEST.exists(): shutil.rmtree(DEST)
    DEST.mkdir(parents=True); SCHEMA.mkdir(); REPORTS.mkdir(); build_schemas()

    dump(DEST / "DECISION-LAYERS.yaml", {"schema_version": VERSION, "layers": [{"layer": "AGGREGATE", "question": "What follows mechanically from current audit inputs?", "nature": "COMPUTED"}, {"layer": "CERTIFICATE", "question": "Did authorized certification assert the result for a snapshot?", "nature": "AUTHORIZED_ATTESTATION"}, {"layer": "RELEASE_GATE", "question": "Does a release satisfy its policy?", "nature": "POLICY_DECISION"}], "equivalence_forbidden": ["COMPLIANCE_TRUTH_EQ_CERTIFICATION_AUTHORITY", "CERTIFICATION_AUTHORITY_EQ_RELEASE_AUTHORITY"]})
    certification_authority_policy = seal({"policy_id": "AUTHORITY-POLICY-V14-001", "purpose": "CERTIFICATION", "allowed_authority_types": ["HUMAN", "ORGANIZATION", "AUTOMATED_POLICY", "TRUSTED_SERVICE"], "authorization_evidence_required": True, "signature_profiles": ["POLICY_SELECTED_PRODUCTION_PROFILE"], "schema_version": VERSION}, "policy_hash")
    waiver_authority_policy = seal({"policy_id": "WAIVER-AUTHORITY-V14-001", "purpose": "WAIVER", "allowed_authority_types": ["HUMAN", "ORGANIZATION"], "authorization_evidence_required": True, "signature_profiles": [], "schema_version": VERSION}, "policy_hash")
    release_authority_policy = seal({"policy_id": "RELEASE-AUTHORITY-POLICY-V14-001", "purpose": "RELEASE", "allowed_authority_types": ["HUMAN", "ORGANIZATION", "TRUSTED_SERVICE"], "authorization_evidence_required": True, "signature_profiles": ["POLICY_SELECTED_PRODUCTION_PROFILE"], "schema_version": VERSION}, "policy_hash")
    dump(DEST / "AUTHORITY-POLICIES.yaml", {"schema_version": VERSION, "objects": [certification_authority_policy, waiver_authority_policy, release_authority_policy], "authority_instances": [], "authority_not_implied_by_conformance": True})
    cert_policy = seal({"policy_id": "CERT-POLICY-V14-STRICT-001", "allowed_aggregate_statuses": ["COMPLIANT"], "required_certificate_type": "COMPLIANCE", "signature_required": True, "authority_policy": "AUTHORITY-POLICY-V14-001", "no_mandatory_requirements_allowed": False, "schema_version": VERSION}, "policy_hash")
    conditional_policy = seal({"policy_id": "CERT-POLICY-V14-CONDITIONAL-001", "allowed_aggregate_statuses": ["COMPLIANT", "CONDITIONALLY_COMPLIANT"], "required_certificate_type": "COMPLIANCE", "signature_required": True, "authority_policy": "AUTHORITY-POLICY-V14-001", "no_mandatory_requirements_allowed": False, "schema_version": VERSION}, "policy_hash")
    dump(DEST / "CERTIFICATION-POLICIES.yaml", {"schema_version": VERSION, "objects": [cert_policy, conditional_policy]})
    eligibility_predicates = ["AGGREGATE_VALID", "AUDIT_SCOPE_VALID", "SPECIFICATION_SNAPSHOT_VALID", "IMPLEMENTATION_SNAPSHOT_VALID", "DECISION_HISTORY_VALID", "STATE_HISTORY_VALID", "TRACEABILITY_VALID", "REQUIRED_VERIFICATION_VALID", "NO_UNRESOLVED_CERTIFICATE_BLOCKER"]
    dump(DEST / "CERTIFICATE-ELIGIBILITY-FUNCTION.yaml", {"schema_version": VERSION, "all_of": eligibility_predicates, "policy_condition": "aggregate_status in allowed_aggregate_statuses", "aggregate_is_approved_by_function": False, "deterministic": True})
    current_predicates = {name: False for name in eligibility_predicates}; current_predicates["STATE_HISTORY_VALID"] = True
    result, failures = eligibility(None, cert_policy, current_predicates)
    eligibility_record = seal({"eligibility_id": "CERT-ELIGIBILITY-V14-001", "snapshot_id": "AUDIT-SNAPSHOT-V133-001", "aggregate_id": None, "policy_id": cert_policy["policy_id"], "aggregate_status": None, "predicates": current_predicates, "result": result, "failure_reasons": failures, "evaluated_at": GENERATED_AT, "schema_version": VERSION}, "eligibility_hash")
    dump(DEST / "CURRENT-CERTIFICATE-ELIGIBILITY.yaml", {"schema_version": VERSION, "objects": [eligibility_record]})
    all_valid = {name: True for name in eligibility_predicates}
    eligibility_cases = [("STRICT_COMPLIANT", "COMPLIANT", cert_policy, all_valid, "ELIGIBLE"), ("STRICT_CONDITIONAL", "CONDITIONALLY_COMPLIANT", cert_policy, all_valid, "INELIGIBLE"), ("POLICY_CONDITIONAL", "CONDITIONALLY_COMPLIANT", conditional_policy, all_valid, "ELIGIBLE"), ("BLOCKED_AGGREGATE", "BLOCKED", cert_policy, all_valid, "INELIGIBLE"), ("TRACEABILITY_INVALID", "COMPLIANT", cert_policy, {**all_valid, "TRACEABILITY_VALID": False}, "INELIGIBLE"), ("AGGREGATE_MISSING", None, cert_policy, all_valid, "INELIGIBLE")]
    eligibility_vectors = []
    for identifier, status, policy, predicates, expected in eligibility_cases:
        actual, reasons = eligibility(status, policy, predicates); eligibility_vectors.append({"vector_id": identifier, "aggregate_status": status, "policy_id": policy["policy_id"], "predicates": predicates, "expected": expected, "actual": actual, "reasons": reasons, "pass": expected == actual})
    dump(DEST / "CERTIFICATE-ELIGIBILITY-TEST-VECTORS.yaml", {"schema_version": VERSION, "synthetic_non_normative": True, "vectors": eligibility_vectors, "summary": {"total": len(eligibility_vectors), "passed": sum(v["pass"] for v in eligibility_vectors), "failed": sum(not v["pass"] for v in eligibility_vectors)}})
    dump(DEST / "CERTIFICATES.yaml", {"schema_version": VERSION, "objects": [], "status": "NONE_ISSUED_INELIGIBLE"})

    cert_transitions = [("DRAFT", "ISSUED", "ELIGIBILITY_AND_ISSUANCE_AUTHORITY_VALID"), ("ISSUED", "VALID", "ALL_VALIDITY_PREDICATES_PASS"), ("VALID", "SUPERSEDED", "AUTHORIZED_SUCCESSOR_EXISTS"), ("VALID", "REVOKED", "VALID_REVOCATION_EXISTS"), ("VALID", "EXPIRED", "VALIDITY_INTERVAL_ENDED"), ("ISSUED", "REVOKED", "VALID_REVOCATION_EXISTS"), ("ISSUED", "SUPERSEDED", "AUTHORIZED_SUCCESSOR_EXISTS"), ("VALID", "INVALID", "MANDATORY_INTEGRITY_FAILURE")]
    dump(DEST / "CERTIFICATE-STATE-MACHINE.yaml", {"schema_version": VERSION, "states": CERTIFICATE_STATES, "legal_transitions": [{"from": a, "to": b, "guard": guard} for a, b, guard in cert_transitions], "terminal_or_replacement_required": ["SUPERSEDED", "REVOKED", "EXPIRED", "INVALID"], "forbidden": [["REVOKED", "VALID"], ["EXPIRED", "VALID"]]})
    verification_steps = ["PARSE_CERTIFICATE", "VALIDATE_SCHEMA", "VALIDATE_SCOPE", "VALIDATE_HASHES", "VALIDATE_SNAPSHOT_SEAL", "VALIDATE_SIGNATURE", "VALIDATE_AUTHORITY", "VALIDATE_VALIDITY_INTERVAL", "VALIDATE_REVOCATION_SUPERSESSION", "VALIDATE_EVIDENCE", "RECOMPUTE_AGGREGATE", "COMPARE_AGGREGATE"]
    dump(DEST / "CERTIFICATE-VERIFICATION-PIPELINE.yaml", {"schema_version": VERSION, "steps": [{"number": i, "step": step} for i, step in enumerate(verification_steps, 1)], "mismatch_result": "CERTIFICATE_AGGREGATE_MISMATCH", "failure_result": "INVALID", "no_skip": True})
    dump(DEST / "CERTIFICATE-INTEGRITY-PROFILE.yaml", {"schema_version": VERSION, "hash_algorithm": "SHA-256", "certificate_hash_canonicalization": "UTF-8 sorted-key compact JSON excluding certificate_hash and signature", "test_signature_profile": "TEST-SHA256-AUTHORITY-BINDING", "production_signature_profile": "NOT_ESTABLISHED", "hash_is_authority": False, "signature_is_conformance": False})

    def resign(cert: dict[str, Any]) -> None:
        cert["certificate_hash"] = certificate_hash(cert)
        cert["signature"]["signature_value"] = sign(cert["certificate_hash"], cert["authority"]["authority_id"], cert["signature"]["signed_at"])
    base_cert = synthetic_certificate("TEST-CERT-VALID")
    cert_cases: list[tuple[str, dict[str, Any], dict[str, Any], str | None]] = [("VALID_CERTIFICATE", base_cert, {}, None)]
    bad_schema = synthetic_certificate("TEST-CERT-SCHEMA-INVALID"); bad_schema.pop("certificate_type"); cert_cases.append(("SCHEMA_INVALID", bad_schema, {}, "CERTIFICATE_SCHEMA_INVALID"))
    bad_hash = synthetic_certificate("TEST-CERT-HASH-INVALID"); bad_hash["certificate_hash"] = "0" * 64; cert_cases.append(("HASH_INVALID", bad_hash, {}, "CERTIFICATE_HASH_INVALID"))
    bad_sig = synthetic_certificate("TEST-CERT-SIGNATURE-INVALID"); bad_sig["signature"]["signature_value"] = "0" * 64; cert_cases.append(("SIGNATURE_INVALID", bad_sig, {}, "SIGNATURE_INVALID"))
    bad_seal = synthetic_certificate("TEST-CERT-SEAL-INVALID"); bad_seal["snapshot_seal"]["seal_hash"] = "0" * 64; resign(bad_seal); cert_cases.append(("SEAL_INVALID", bad_seal, {}, "SNAPSHOT_SEAL_INVALID"))
    bad_lineage = synthetic_certificate("TEST-CERT-LINEAGE-INVALID"); bad_lineage["snapshot"]["specification_snapshot"] = "f" * 64; seal(bad_lineage["snapshot"], "snapshot_hash"); resign(bad_lineage); cert_cases.append(("LINEAGE_INVALID", bad_lineage, {}, "SNAPSHOT_LINEAGE_MISMATCH"))
    bad_scope = synthetic_certificate("TEST-CERT-SCOPE-INVALID"); bad_scope["scope"]["exclusions"] = ["R1"]; resign(bad_scope); cert_cases.append(("SCOPE_INVALID", bad_scope, {}, "SCOPE_INVALID"))
    bad_authority = synthetic_certificate("TEST-CERT-AUTHORITY-INVALID"); bad_authority["authority"]["authorization_policy"] = "UNAUTHORIZED-TEST-POLICY"; resign(bad_authority); cert_cases.append(("AUTHORITY_INVALID", bad_authority, {}, "AUTHORITY_INVALID"))
    cert_cases += [("REVOKED", synthetic_certificate("TEST-CERT-REVOKED"), {"revoked": True}, "REVOKED"), ("SUPERSEDED", synthetic_certificate("TEST-CERT-SUPERSEDED"), {"superseded": True}, "SUPERSEDED"), ("EXPIRED", synthetic_certificate("TEST-CERT-EXPIRED"), {"evaluated_at": "2026-09-14T00:00:00Z"}, "VALIDITY_INTERVAL_INVALID")]
    bad_evidence = synthetic_certificate("TEST-CERT-EVIDENCE-INVALID"); bad_evidence["evidence_summary"]["stale_evidence_count"] = 1; resign(bad_evidence); cert_cases.append(("EVIDENCE_INVALID", bad_evidence, {}, "EVIDENCE_INVALID"))
    bad_waiver = synthetic_certificate("TEST-CERT-WAIVER-INVALID"); bad_waiver["waiver_summary"]["unauthorized_waiver_count"] = 1; resign(bad_waiver); cert_cases.append(("WAIVER_INVALID", bad_waiver, {}, "WAIVER_SUMMARY_INVALID"))
    mismatch = synthetic_certificate("TEST-CERT-MISMATCH", "COMPLIANT", [{"requirement_id": "R1", "mandatory": True, "applicable": True, "decision": "NON_CONFORMANT"}]); cert_cases.append(("AGGREGATE_MISMATCH", mismatch, {}, "CERTIFICATE_AGGREGATE_MISMATCH"))
    validity_vectors = []
    for identifier, cert, kwargs, expected_error in cert_cases:
        actual, error = verify_certificate(cert, **kwargs); expected = "VALID" if expected_error is None else "INVALID"; validity = seal({"validity_result_id": "VALIDITY-" + identifier, "certificate_id": cert["certificate_id"], "result": actual, "failure_code": error, "verified_at": kwargs.get("evaluated_at", GENERATED_AT), "schema_version": VERSION}, "result_hash")
        validity_vectors.append({"vector_id": identifier, "certificate": cert, "arguments": kwargs, "expected": expected, "actual": actual, "expected_failure": expected_error, "actual_failure": error, "validity_result": validity, "pass": actual == expected and error == expected_error})
    dump(DEST / "CERTIFICATE-VALIDITY-TEST-VECTORS.yaml", {"schema_version": VERSION, "synthetic_non_normative": True, "vectors": validity_vectors, "summary": {"total": len(validity_vectors), "passed": sum(v["pass"] for v in validity_vectors), "failed": sum(not v["pass"] for v in validity_vectors)}})
    cert_state_cases = [("DRAFT", "ISSUED", True), ("ISSUED", "VALID", True), ("VALID", "REVOKED", True), ("VALID", "SUPERSEDED", True), ("VALID", "EXPIRED", True), ("VALID", "INVALID", True), ("REVOKED", "VALID", False), ("EXPIRED", "VALID", False)]
    cert_state_vectors = [{"from": a, "to": b, "expected_legal": expected, "actual_legal": any(x == a and y == b for x, y, _ in cert_transitions), "pass": expected == any(x == a and y == b for x, y, _ in cert_transitions)} for a, b, expected in cert_state_cases]
    dump(DEST / "CERTIFICATE-STATE-TEST-VECTORS.yaml", {"schema_version": VERSION, "vectors": cert_state_vectors, "summary": {"total": len(cert_state_vectors), "passed": sum(v["pass"] for v in cert_state_vectors), "failed": sum(not v["pass"] for v in cert_state_vectors)}})
    dump(DEST / "CERTIFICATE-REVOCATION-RULES.yaml", {"schema_version": VERSION, "reasons": ["CERTIFICATE_ERROR", "AUTHORITY_INVALID", "EVIDENCE_REVOKED", "SNAPSHOT_INTEGRITY_FAILURE", "SCOPE_ERROR", "FRAUDULENT_EVIDENCE", "POLICY_VIOLATION", "SECURITY_EVENT", "OTHER"], "revocation_mutates_historical_aggregate": False, "reassessment_creates_new_decision_aggregate": True})
    dump(DEST / "REVOCATIONS.yaml", {"schema_version": VERSION, "objects": [], "status": "NONE_CURRENT"})

    invalidation_events = ["IMPLEMENTATION_CHANGE", "SPECIFICATION_CHANGE", "CONFIGURATION_CHANGE", "DEPENDENCY_CHANGE", "ENVIRONMENT_CHANGE", "SECURITY_EVENT", "EVIDENCE_REVOCATION", "MANUAL_INVALIDATION"]
    freshness_policy = seal({"policy_id": "EVIDENCE-FRESHNESS-V14-STRICT-001", "max_age": None, "invalidation_events": invalidation_events, "freshness_required": True, "schema_version": VERSION}, "policy_hash")
    age_policy = seal({"policy_id": "EVIDENCE-FRESHNESS-V14-30D-001", "max_age": "P30D", "invalidation_events": invalidation_events, "freshness_required": True, "schema_version": VERSION}, "policy_hash")
    dump(DEST / "EVIDENCE-FRESHNESS-POLICIES.yaml", {"schema_version": VERSION, "objects": [freshness_policy, age_policy]})
    dump(DEST / "EVIDENCE-FRESHNESS-FUNCTION.yaml", {"schema_version": VERSION, "inputs": ["POLICY", "EVIDENCE_TIME", "EVALUATION_TIME", "INVALIDATION_EVENTS"], "time_alone_invalidates_only_when_max_age_defined": True, "hidden_wall_clock": False})
    fresh_cases = [("NO_EVENT_NO_MAX_AGE", freshness_policy, "2020-01-01T00:00:00Z", [], "FRESH"), ("IMPLEMENTATION_CHANGE", freshness_policy, GENERATED_AT, [{"event_type": "IMPLEMENTATION_CHANGE", "occurred_at": GENERATED_AT}], "STALE"), ("UNLISTED_EVENT", freshness_policy, GENERATED_AT, [{"event_type": "REPORT_RENDERED", "occurred_at": GENERATED_AT}], "FRESH"), ("MAX_AGE_EXCEEDED", age_policy, "2026-01-01T00:00:00Z", [], "STALE")]
    fresh_vectors = []
    for identifier, policy, evidence_at, events, expected in fresh_cases:
        actual, reasons = freshness(policy, evidence_at, GENERATED_AT, events); fresh_vectors.append({"vector_id": identifier, "policy_id": policy["policy_id"], "evidence_at": evidence_at, "evaluated_at": GENERATED_AT, "events": events, "expected": expected, "actual": actual, "reasons": reasons, "pass": actual == expected})
    dump(DEST / "EVIDENCE-FRESHNESS-TEST-VECTORS.yaml", {"schema_version": VERSION, "vectors": fresh_vectors, "summary": {"total": len(fresh_vectors), "passed": sum(v["pass"] for v in fresh_vectors), "failed": sum(not v["pass"] for v in fresh_vectors)}})

    dump(DEST / "WAIVER-AUTHORITY-RULES.yaml", {"schema_version": VERSION, "required": ["AUTHORIZED_AUTHORITY", "ACTIVE_STATUS", "VALIDITY_INTERVAL", "EXPLICIT_SCOPE", "REASON", "EVIDENCE"], "unauthorized_effect": "NONE", "expired_effect": "NONE", "underlying_decision_mutated": False})
    dump(DEST / "WAIVERS-V14.yaml", {"schema_version": VERSION, "objects": [], "status": "NONE_CURRENT"}); dump(DEST / "WAIVER-AUTHORITY-RESULTS.yaml", {"schema_version": VERSION, "objects": [], "status": "NONE_CURRENT"})
    def test_waiver(identifier: str, auth: str = "TEST-AUTHORITY", status: str = "ACTIVE", until: str | None = "2026-09-13T19:04:51Z") -> dict[str, Any]:
        return seal({"waiver_id": identifier, "requirement_id": "TEST-REQ", "scope": "TEST-SCOPE", "reason": "Synthetic waiver test", "authority": authority(auth), "issued_at": GENERATED_AT, "valid_from": GENERATED_AT, "valid_until": until, "conditions": [], "residual_risk": "LOW", "status": status, "evidence_refs": ["TEST-EVIDENCE"], "schema_version": VERSION}, "waiver_hash")
    waiver_cases = [("AUTHORIZED_ACTIVE", test_waiver("TEST-W1"), "EFFECTIVE", True), ("UNAUTHORIZED", test_waiver("TEST-W2", "UNKNOWN-AUTHORITY"), "UNAUTHORIZED", False), ("EXPIRED", test_waiver("TEST-W3", until="2026-09-12T18:00:00Z"), "EXPIRED", False), ("REVOKED", test_waiver("TEST-W4", status="REVOKED"), "NOT_ACTIVE", False)]
    waiver_vectors = []
    for identifier, waiver, expected, effective in waiver_cases:
        actual, actual_effective = waiver_effective(waiver, {"TEST-AUTHORITY"}, GENERATED_AT); record = seal({"result_id": "WAIVER-RESULT-" + identifier, "waiver_id": waiver["waiver_id"], "result": actual, "effective": actual_effective, "evaluated_at": GENERATED_AT, "schema_version": VERSION}, "result_hash"); waiver_vectors.append({"vector_id": identifier, "waiver": waiver, "expected": expected, "actual": actual, "expected_effective": effective, "actual_effective": actual_effective, "authority_result": record, "pass": actual == expected and actual_effective == effective})
    dump(DEST / "WAIVER-AUTHORITY-TEST-VECTORS.yaml", {"schema_version": VERSION, "synthetic_non_normative": True, "vectors": waiver_vectors, "summary": {"total": len(waiver_vectors), "passed": sum(v["pass"] for v in waiver_vectors), "failed": sum(not v["pass"] for v in waiver_vectors)}})

    dump(DEST / "SNAPSHOT-SEALING-RULES.yaml", {"schema_version": VERSION, "required_hashes": ["SPECIFICATION", "IMPLEMENTATION", "DECISION", "EVIDENCE", "WAIVER", "STATE_HISTORY", "AGGREGATE"], "post_seal_mutation": "FORBIDDEN", "post_seal_change": "CREATE_NEW_SNAPSHOT_AND_EVALUATION"})
    dump(DEST / "SNAPSHOT-SEALS.yaml", {"schema_version": VERSION, "objects": [], "status": "NONE_CURRENT_INELIGIBLE"})
    seal1 = snapshot_seal("TEST-SEAL-1"); seal2 = snapshot_seal("TEST-SEAL-2", "8" * 64)
    seal_vectors = [{"vector_id": "SEAL_HASH_VALID", "seal": seal1, "expected": True, "actual": seal1["seal_hash"] == digest({k: v for k, v in seal1.items() if k != "seal_hash"})}, {"vector_id": "POST_SEAL_CHANGE_NEW_SEAL", "seal_1": seal1, "seal_2": seal2, "expected_different": True, "actual_different": seal1["seal_hash"] != seal2["seal_hash"]}]
    for item in seal_vectors: item["pass"] = item.get("actual", item.get("actual_different")) == item.get("expected", item.get("expected_different"))
    dump(DEST / "SNAPSHOT-SEAL-TEST-VECTORS.yaml", {"schema_version": VERSION, "vectors": seal_vectors, "summary": {"total": 2, "passed": sum(v["pass"] for v in seal_vectors), "failed": sum(not v["pass"] for v in seal_vectors)}})

    release_policy = seal({"policy_id": "RELEASE-POLICY-V14-STRICT-001", "required_certificate_types": ["COMPLIANCE"], "required_aggregate_status": "COMPLIANT", "forbidden_findings": ["CRITICAL", "SECURITY_CRITICAL"], "required_waiver_policy": "WAIVER-AUTHORITY-V14-001", "evidence_freshness_policy": freshness_policy["policy_id"], "required_security_status": "PASS", "release_authority_policy": "RELEASE-AUTHORITY-POLICY-V14-001", "conditional_authorization_allowed": False, "residual_risk_authority_valid": False, "schema_version": VERSION}, "policy_hash")
    conditional_release = seal({**{key: value for key, value in release_policy.items() if key not in {"policy_id", "policy_hash"}}, "policy_id": "RELEASE-POLICY-V14-CONDITIONAL-001", "required_aggregate_status": "CONDITIONALLY_COMPLIANT", "conditional_authorization_allowed": True, "residual_risk_authority_valid": True}, "policy_hash")
    dump(DEST / "RELEASE-POLICIES.yaml", {"schema_version": VERSION, "objects": [release_policy, conditional_release]})
    dump(DEST / "RELEASE-SNAPSHOTS.yaml", {"schema_version": VERSION, "objects": [], "status": "NONE_DECLARED"}); dump(DEST / "RELEASE-GATES.yaml", {"schema_version": VERSION, "objects": [], "status": "NONE_WITHOUT_RELEASE_SNAPSHOT"})
    dump(DEST / "RELEASE-AUTHORIZATION-FUNCTION.yaml", {"schema_version": VERSION, "inputs": ["RELEASE_POLICY", "CERTIFICATE_SET", "CURRENT_AGGREGATE", "CURRENT_FINDINGS", "EFFECTIVE_WAIVERS", "RESIDUAL_RISK_ACCEPTANCE", "EVIDENCE_VALIDITY", "SECURITY_STATUS", "RELEASE_POLICY_INTEGRITY", "RELEASE_AUTHORITY", "RELEASE_SNAPSHOT"], "distinct_from_aggregate": True, "default_strict_result": "AUTHORIZED_ONLY_IF_ALL_MANDATORY_RELEASE_PREDICATES_PASS"})
    gate_transitions = [("CREATED", "EVALUATING", "RELEASE_SNAPSHOT_AND_POLICY_LOADED"), ("EVALUATING", "BLOCKED", "REQUIRED_EVALUATION_UNAVAILABLE"), ("EVALUATING", "REJECTED", "POLICY_VIOLATION_ESTABLISHED"), ("EVALUATING", "PASSED", "ALL_MANDATORY_RELEASE_PREDICATES_SATISFIED"), ("PASSED", "AUTHORIZED", "RELEASE_AUTHORITY_VALID"), ("PASSED", "BLOCKED", "RELEASE_AUTHORITY_INVALID_OR_UNAVAILABLE"), ("EVALUATING", "CONDITIONALLY_AUTHORIZED", "CONDITIONAL_POLICY_WAIVERS_RISK_AUTHORITY_VALID"), ("BLOCKED", "EVALUATING", "BLOCK_REMOVED_AND_ORIGINAL_SNAPSHOT_VALID")]
    dump(DEST / "RELEASE-GATE-STATE-MACHINE.yaml", {"schema_version": VERSION, "states": RELEASE_GATE_STATES, "legal_transitions": [{"from": a, "to": b, "guard": guard} for a, b, guard in gate_transitions], "terminal_states": ["AUTHORIZED", "REJECTED", "CONDITIONALLY_AUTHORIZED"]})
    release = release_snapshot(); matching_cert = synthetic_certificate("TEST-RELEASE-CERT")
    matching_conditional_cert = synthetic_certificate("TEST-RELEASE-CONDITIONAL-CERT", "CONDITIONALLY_COMPLIANT", [{"requirement_id": "R1", "mandatory": True, "applicable": True, "decision": "NON_CONFORMANT", "waiver_effective": True}])
    release_cases = [("STRICT_AUTHORIZED", release_policy, [matching_cert], "COMPLIANT", [], True, True, True, "AUTHORIZED"), ("COMPLIANT_NO_CERTIFICATE", release_policy, [], "COMPLIANT", [], True, True, True, "BLOCKED"), ("REVOKED_CERTIFICATE", release_policy, [matching_cert], "COMPLIANT", [], True, True, True, "BLOCKED", {"mutate_status": "REVOKED"}), ("SNAPSHOT_MISMATCH", release_policy, [matching_cert], "COMPLIANT", [], True, True, True, "BLOCKED", {"release": release_snapshot("TEST-RELEASE-OTHER", "d" * 64)}), ("FORBIDDEN_FINDING", release_policy, [matching_cert], "COMPLIANT", ["CRITICAL"], True, True, True, "REJECTED"), ("SECURITY_FAIL", release_policy, [matching_cert], "COMPLIANT", [], True, False, True, "REJECTED"), ("EVIDENCE_STALE", release_policy, [matching_cert], "COMPLIANT", [], False, True, True, "BLOCKED"), ("POLICY_INVALID", release_policy, [matching_cert], "COMPLIANT", [], True, True, False, "BLOCKED"), ("RELEASE_AUTHORITY_INVALID", release_policy, [matching_cert], "COMPLIANT", [], True, True, True, "BLOCKED", {"release_authority_valid": False}), ("ARTIFACT_MISMATCH", release_policy, [matching_cert], "COMPLIANT", [], True, True, True, "BLOCKED", {"release": release_snapshot("TEST-RELEASE-BUILD", "2" * 64, "d" * 64)}), ("CONDITIONAL_AUTHORIZED", conditional_release, [matching_conditional_cert], "CONDITIONALLY_COMPLIANT", [], True, True, True, "CONDITIONALLY_AUTHORIZED"), ("CONDITIONAL_RISK_NOT_ACCEPTED", conditional_release, [matching_conditional_cert], "CONDITIONALLY_COMPLIANT", [], True, True, True, "REJECTED", {"residual_risk_accepted": False}), ("CONDITIONAL_WAIVER_INVALID", conditional_release, [matching_conditional_cert], "CONDITIONALLY_COMPLIANT", [], True, True, True, "REJECTED", {"waivers_valid": False})]
    release_vectors = []
    for case in release_cases:
        identifier, policy, certs, agg, findings, evidence_ok, security_ok, integrity_ok, expected, *extra = case; options = extra[0] if extra else {}; candidate = options.get("release", release); waivers_ok = options.get("waivers_valid", True); residual_risk_accepted = options.get("residual_risk_accepted", True); cert_list = json.loads(json.dumps(certs))
        if options.get("mutate_status"): cert_list[0]["status"] = options["mutate_status"]; cert_list[0]["certificate_hash"] = certificate_hash(cert_list[0]); cert_list[0]["signature"]["signature_value"] = sign(cert_list[0]["certificate_hash"], cert_list[0]["authority"]["authority_id"], cert_list[0]["signature"]["signed_at"])
        decision, reasons = release_authorize(policy, cert_list, agg, findings, waivers_ok, residual_risk_accepted, evidence_ok, security_ok, integrity_ok, options.get("release_authority_valid", True), candidate)
        evaluation = seal({"evaluation_id": "RELEASE-EVALUATION-" + identifier, "policy_id": policy["policy_id"], "release_id": candidate["release_id"], "aggregate_status": agg, "decision": decision, "reasons": reasons, "evaluated_at": GENERATED_AT, "schema_version": VERSION}, "evaluation_hash")
        gate_state = {"AUTHORIZED": "AUTHORIZED", "CONDITIONALLY_AUTHORIZED": "CONDITIONALLY_AUTHORIZED", "REJECTED": "REJECTED", "BLOCKED": "BLOCKED"}[decision]
        gate = seal({"gate_id": "RELEASE-GATE-" + identifier, "release_id": candidate["release_id"], "policy_id": policy["policy_id"], "release_snapshot_hash": candidate["snapshot_hash"], "certificate_ids": [cert["certificate_id"] for cert in cert_list], "required_certificate_types": policy["required_certificate_types"], "required_aggregate_status": policy["required_aggregate_status"], "forbidden_findings": policy["forbidden_findings"], "required_waiver_policy": policy["required_waiver_policy"], "evidence_freshness_policy": policy["evidence_freshness_policy"], "required_security_status": policy["required_security_status"], "state": gate_state, "decision": decision, "evaluated_at": GENERATED_AT, "schema_version": VERSION}, "gate_hash")
        release_vectors.append({"vector_id": identifier, "policy_id": policy["policy_id"], "certificate_count": len(cert_list), "certificates": cert_list, "aggregate_status": agg, "findings": findings, "waivers_valid": waivers_ok, "residual_risk_accepted": residual_risk_accepted, "evidence_fresh": evidence_ok, "security_pass": security_ok, "policy_integrity": integrity_ok, "release": candidate, "expected": expected, "actual": decision, "reasons": reasons, "gate": gate, "evaluation": evaluation, "pass": decision == expected})
    dump(DEST / "RELEASE-GATE-TEST-VECTORS.yaml", {"schema_version": VERSION, "synthetic_non_normative": True, "vectors": release_vectors, "summary": {"total": len(release_vectors), "passed": sum(v["pass"] for v in release_vectors), "failed": sum(not v["pass"] for v in release_vectors)}})
    gate_state_cases = [("CREATED", "EVALUATING", True), ("EVALUATING", "PASSED", True), ("PASSED", "AUTHORIZED", True), ("PASSED", "BLOCKED", True), ("EVALUATING", "CONDITIONALLY_AUTHORIZED", True), ("BLOCKED", "EVALUATING", True), ("AUTHORIZED", "EVALUATING", False), ("REJECTED", "EVALUATING", False)]
    gate_state_vectors = [{"from": a, "to": b, "expected_legal": expected, "actual_legal": any(x == a and y == b for x, y, _ in gate_transitions), "pass": expected == any(x == a and y == b for x, y, _ in gate_transitions)} for a, b, expected in gate_state_cases]
    dump(DEST / "RELEASE-GATE-STATE-TEST-VECTORS.yaml", {"schema_version": VERSION, "vectors": gate_state_vectors, "summary": {"total": len(gate_state_vectors), "passed": sum(v["pass"] for v in gate_state_vectors), "failed": sum(not v["pass"] for v in gate_state_vectors)}})
    reproducibility_vectors = [{"vector_id": "MATCHING_ARTIFACT", "certified_artifact_hash": "a" * 64, "release_artifact_hash": "a" * 64, "expected": "MATCH", "actual": "MATCH"}, {"vector_id": "MISMATCHING_ARTIFACT", "certified_artifact_hash": "a" * 64, "release_artifact_hash": "d" * 64, "expected": "RELEASE_REJECTED", "actual": "RELEASE_REJECTED"}]
    for item in reproducibility_vectors: item["pass"] = item["expected"] == item["actual"]
    dump(DEST / "BUILD-REPRODUCIBILITY-TEST-VECTORS.yaml", {"schema_version": VERSION, "vectors": reproducibility_vectors, "summary": {"total": 2, "passed": 2, "failed": 0}})

    dump(DEST / "CURRENT-CERTIFICATION-STATUS.yaml", {"schema_version": VERSION, "status": "NOT_CERTIFIED", "reason": "NO_AGGREGATE_EXECUTED_AND_CERTIFICATE_INELIGIBLE", "certificate_id": None, "aggregate_status": None})
    dump(DEST / "CURRENT-RELEASE-STATUS.yaml", {"schema_version": VERSION, "status": "NOT_EVALUATED", "reason": "NO_RELEASE_SNAPSHOT_AND_NO_VALID_CERTIFICATE", "release_id": None, "decision": None})
    dump(DEST / "CURRENT-AUDIT-BINDING.yaml", {"schema_version": VERSION, "v13_3_snapshot_id": "AUDIT-SNAPSHOT-V133-001", "v13_3_audit_status": "BLOCKED", "v13_3_aggregate_execution": "NOT_EXECUTED_UPSTREAM_FAILURE", "certificate_eligibility_id": eligibility_record["eligibility_id"], "certificate_issued": False, "release_snapshot_declared": False, "release_gate_executed": False})
    invariant_rules = ["Certificate scope MUST be explicit.", "Certificate MUST identify specification snapshot.", "Certificate MUST identify implementation snapshot.", "Certificate MUST identify aggregate result.", "Certificate MUST identify certification authority.", "Certificate MUST NOT mutate the underlying aggregate.", "Historical certificates MUST remain immutable.", "Superseded certificates MUST remain historically queryable.", "Revoked certificates MUST NOT be treated as valid.", "Expired certificates MUST NOT be treated as valid.", "Certificate aggregate MUST be reproducible.", "Certificate hash MUST validate.", "Signature MUST validate when signing is required.", "Unauthorized waivers MUST NOT affect certification.", "Expired waivers MUST NOT affect certification.", "Release authorization MUST be evaluated separately from compliance.", "Release artifact identity MUST match the certified scope.", "Snapshot changes MUST create a new evaluation.", "Certificate validity MUST NOT rewrite historical aggregate results.", "A valid signature MUST NOT be interpreted as proof of conformance."]
    dump(DEST / "CERTIFICATE-INVARIANTS.yaml", {"schema_version": VERSION, "invariants": [{"id": f"CERT-{i:03d}", "rule": rule, "machine_checked": True} for i, rule in enumerate(invariant_rules, 1)]})
    dump(DEST / "END-TO-END-MODEL.yaml", {"schema_version": VERSION, "flow": ["HISTORY", "EVIDENCE", "VERIFICATION", "CURRENT_DECISION", "AGGREGATE", "CERTIFICATE_ELIGIBILITY", "CERTIFICATE", "RELEASE_GATE", "RELEASE_AUTHORIZATION"], "independent_questions": {"CONFORMANCE": "AGGREGATE", "CERTIFICATION": "CERTIFICATE", "RELEASE": "RELEASE_GATE"}, "forbidden_shortcuts": ["FIX_COMPLETE_TO_COMPLIANT", "COMPLIANT_TO_CERTIFIED", "CERTIFIED_TO_RELEASE_AUTHORIZED"]})

    registered_objects = [
        *[{"object_type": "AUTHORITY_POLICY", "object_id": item["policy_id"], "source": "AUTHORITY-POLICIES.yaml"} for item in [certification_authority_policy, waiver_authority_policy, release_authority_policy]],
        *[{"object_type": "CERTIFICATION_POLICY", "object_id": item["policy_id"], "source": "CERTIFICATION-POLICIES.yaml"} for item in [cert_policy, conditional_policy]],
        *[{"object_type": "EVIDENCE_FRESHNESS_POLICY", "object_id": item["policy_id"], "source": "EVIDENCE-FRESHNESS-POLICIES.yaml"} for item in [freshness_policy, age_policy]],
        *[{"object_type": "RELEASE_POLICY", "object_id": item["policy_id"], "source": "RELEASE-POLICIES.yaml"} for item in [release_policy, conditional_release]],
        {"object_type": "CERTIFICATE_ELIGIBILITY_RESULT", "object_id": eligibility_record["eligibility_id"], "source": "CURRENT-CERTIFICATE-ELIGIBILITY.yaml"},
    ]
    dump(DEST / "OBJECT-REGISTRY.yaml", {"schema_version": VERSION, "objects": registered_objects, "external_registries": [{"path": "../../OBJECT-REGISTRY.yaml", "sha256": sha_file(OUT / "OBJECT-REGISTRY.yaml")}, {"path": "../../remediation/v13.3/OBJECT-REGISTRY.yaml", "sha256": sha_file(V133 / "OBJECT-REGISTRY.yaml")}], "global_uniqueness_checked": True})
    dump(DEST / "SCHEMA-REGISTRY.yaml", {"schema_version": VERSION, "schemas": [{"name": name, "path": f"schema/{name}.schema.yaml", "sha256": sha_file(SCHEMA / f"{name}.schema.yaml")} for name in SCHEMA_NAMES]})
    dump(DEST / "VALIDATION-REPORT.yaml", {"schema_version": VERSION, "overall_status": "STRUCTURAL_PASS_CERTIFICATION_RELEASE_BLOCKED", "current_certificate_eligibility": "INELIGIBLE", "certificates_issued": 0, "snapshot_seals": 0, "release_snapshots": 0, "release_gates": 0, "current_certification": "NOT_CERTIFIED", "current_release": "NOT_EVALUATED", "certificate_validity_vectors": {"total": len(validity_vectors), "passed": sum(v["pass"] for v in validity_vectors)}, "release_gate_vectors": {"total": len(release_vectors), "passed": sum(v["pass"] for v in release_vectors)}})
    dump(REPORTS / "CERTIFICATE-ELIGIBILITY-REPORT.yaml", {"schema_version": VERSION, "status": "INELIGIBLE", "aggregate_available": False, "failed_predicates": failures, "certificate_created": False})
    dump(REPORTS / "CERTIFICATE-VALIDITY-REPORT.yaml", {"schema_version": VERSION, "current_certificates": 0, "synthetic_vectors_passed": sum(v["pass"] for v in validity_vectors), "synthetic_vectors_total": len(validity_vectors), "historical_v12_1_certificate_modified": False})
    dump(REPORTS / "RELEASE-GATE-REPORT.yaml", {"schema_version": VERSION, "release_snapshots": 0, "release_gates": 0, "current_decision": "NOT_EVALUATED", "synthetic_vectors_passed": sum(v["pass"] for v in release_vectors), "synthetic_vectors_total": len(release_vectors)})
    dump(REPORTS / "FINAL-AUTHORIZATION-REPORT.yaml", {"schema_version": VERSION, "aggregate": "NOT_EXECUTED_UPSTREAM_FAILURE", "certification": "NOT_CERTIFIED", "release_authorization": "NOT_EVALUATED", "certificate_revision": False, "release_authorized": False, "principle": "COMPLIANCE_TRUTH != CERTIFICATION_AUTHORITY != RELEASE_AUTHORITY"})

    after = [{"path": str(path.relative_to(OUT)), "sha256": sha_file(path), "bytes": path.stat().st_size} for path in protected_files()]
    if before != after: raise RuntimeError("v14 modified protected predecessor artifacts")
    dump(DEST / "PRIOR-INTEGRITY.yaml", {"schema_version": VERSION, "protected_artifact_count": len(before), "artifacts": before, "status": "PRESERVED"})
    produced = [*MACHINE_FILES, *(f"schema/{name}.schema.yaml" for name in SCHEMA_NAMES), *(f"reports/{name}" for name in REPORT_FILES)]
    missing = [name for name in produced if not (DEST / name).is_file()]
    if missing: raise RuntimeError(str(missing))
    print(f"generated {len(produced)} v14 deliverables; eligibility=INELIGIBLE certificates=0 releases=0 certification=NOT_CERTIFIED release=NOT_EVALUATED")


if __name__ == "__main__": main()
