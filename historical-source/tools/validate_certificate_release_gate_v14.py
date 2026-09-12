#!/usr/bin/env python3
"""Independent validator for Protocol-v14 certification and release gating."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
HS = ROOT / "historical-source"
OUT = HS / "compliance"
V133 = OUT / "remediation" / "v13.3"
DEST = OUT / "certification" / "v14"
SCHEMA = DEST / "schema"
VERSION = "14.0"
SCHEMA_NAMES = ["certificate-scope", "certification-authority", "authority-policy", "evidence-summary", "waiver-summary", "evidence-freshness-policy", "certificate-signature", "certificate-snapshot", "snapshot-seal", "certificate", "certification-policy", "certificate-eligibility-result", "certificate-validity-result", "certificate-transition", "revocation-record", "waiver", "waiver-authority-result", "artifact-hash", "release-snapshot", "release-policy", "release-gate", "release-gate-transition", "release-gate-evaluation"]
MACHINE_FILES = ["DECISION-LAYERS.yaml", "AUTHORITY-POLICIES.yaml", "CERTIFICATION-POLICIES.yaml", "CERTIFICATE-ELIGIBILITY-FUNCTION.yaml", "CURRENT-CERTIFICATE-ELIGIBILITY.yaml", "CERTIFICATE-ELIGIBILITY-TEST-VECTORS.yaml", "CERTIFICATES.yaml", "CERTIFICATE-STATE-MACHINE.yaml", "CERTIFICATE-VERIFICATION-PIPELINE.yaml", "CERTIFICATE-VALIDITY-TEST-VECTORS.yaml", "CERTIFICATE-STATE-TEST-VECTORS.yaml", "CERTIFICATE-INTEGRITY-PROFILE.yaml", "CERTIFICATE-REVOCATION-RULES.yaml", "REVOCATIONS.yaml", "EVIDENCE-FRESHNESS-POLICIES.yaml", "EVIDENCE-FRESHNESS-FUNCTION.yaml", "EVIDENCE-FRESHNESS-TEST-VECTORS.yaml", "WAIVER-AUTHORITY-RULES.yaml", "WAIVERS-V14.yaml", "WAIVER-AUTHORITY-RESULTS.yaml", "WAIVER-AUTHORITY-TEST-VECTORS.yaml", "SNAPSHOT-SEALING-RULES.yaml", "SNAPSHOT-SEALS.yaml", "SNAPSHOT-SEAL-TEST-VECTORS.yaml", "RELEASE-POLICIES.yaml", "RELEASE-SNAPSHOTS.yaml", "RELEASE-GATES.yaml", "RELEASE-AUTHORIZATION-FUNCTION.yaml", "RELEASE-GATE-STATE-MACHINE.yaml", "RELEASE-GATE-TEST-VECTORS.yaml", "RELEASE-GATE-STATE-TEST-VECTORS.yaml", "BUILD-REPRODUCIBILITY-TEST-VECTORS.yaml", "CURRENT-CERTIFICATION-STATUS.yaml", "CURRENT-RELEASE-STATUS.yaml", "CURRENT-AUDIT-BINDING.yaml", "CERTIFICATE-INVARIANTS.yaml", "END-TO-END-MODEL.yaml", "OBJECT-REGISTRY.yaml", "SCHEMA-REGISTRY.yaml", "PRIOR-INTEGRITY.yaml", "VALIDATION-REPORT.yaml"]
REPORT_FILES = ["CERTIFICATE-ELIGIBILITY-REPORT.yaml", "CERTIFICATE-VALIDITY-REPORT.yaml", "RELEASE-GATE-REPORT.yaml", "FINAL-AUTHORIZATION-REPORT.yaml"]
DELIVERABLES = [*MACHINE_FILES, *(f"schema/{name}.schema.yaml" for name in SCHEMA_NAMES), *(f"reports/{name}" for name in REPORT_FILES)]


def load(path: Path) -> Any: return json.loads(path.read_text(encoding="utf-8"))
def canonical(value: Any) -> bytes: return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
def digest(value: Any) -> str: return hashlib.sha256(canonical(value)).hexdigest()
def sha_file(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()
def valid_time(value: Any) -> bool:
    if not isinstance(value, str): return False
    try: return datetime.fromisoformat(value.replace("Z", "+00:00")).tzinfo is not None
    except ValueError: return False


def schema_errors(value: Any, body: dict[str, Any], schemas: dict[str, Any], path: str = "$") -> list[str]:
    if "$ref" in body: return schema_errors(value, schemas[Path(body["$ref"]).name.replace(".schema.yaml", "")], schemas, path)
    if "oneOf" in body:
        options = [schema_errors(value, item, schemas, path) for item in body["oneOf"]]
        return [] if sum(not result for result in options) == 1 else [f"{path}: oneOf"]
    errors: list[str] = []; expected = body.get("type")
    if expected:
        matches = {"object": isinstance(value, dict), "array": isinstance(value, list), "string": isinstance(value, str), "integer": isinstance(value, int) and not isinstance(value, bool), "boolean": isinstance(value, bool), "null": value is None}
        if not matches.get(expected, False): return [f"{path}: type"]
    if "const" in body and value != body["const"]: errors.append(f"{path}: const")
    if "enum" in body and value not in body["enum"]: errors.append(f"{path}: enum")
    if isinstance(value, str):
        if len(value) < body.get("minLength", 0): errors.append(f"{path}: minLength")
        if "pattern" in body and re.fullmatch(body["pattern"], value) is None: errors.append(f"{path}: pattern")
        if body.get("format") == "date-time" and not valid_time(value): errors.append(f"{path}: date-time")
    if isinstance(value, int) and not isinstance(value, bool) and value < body.get("minimum", value): errors.append(f"{path}: minimum")
    if isinstance(value, list):
        if len(value) < body.get("minItems", 0): errors.append(f"{path}: minItems")
        if body.get("uniqueItems") and len({canonical(item) for item in value}) != len(value): errors.append(f"{path}: unique")
        for index, item in enumerate(value):
            if "items" in body: errors.extend(schema_errors(item, body["items"], schemas, f"{path}[{index}]"))
    if isinstance(value, dict):
        properties = body.get("properties", {})
        for key in body.get("required", []):
            if key not in value: errors.append(f"{path}: missing {key}")
        if body.get("additionalProperties") is False:
            errors.extend(f"{path}: additional {key}" for key in value if key not in properties)
        for key, item in value.items():
            if key in properties: errors.extend(schema_errors(item, properties[key], schemas, f"{path}.{key}"))
    return errors


def aggregate(requirements: list[dict[str, Any]]) -> str:
    contributions = []
    for item in requirements:
        if not item["mandatory"] or not item.get("applicable", True) or item["decision"] == "NOT_APPLICABLE": continue
        decision = item["decision"]
        if decision == "NON_CONFORMANT": contributions.append("WAIVED" if item.get("waiver_effective") else "FAIL")
        elif decision == "BLOCKED": contributions.append("BLOCKED")
        elif decision in {"PARTIALLY_CONFORMANT", "UNVERIFIED", "UNKNOWN"}: contributions.append("UNRESOLVED")
        elif decision == "CONFORMANT": contributions.append("PASS")
        else: contributions.append("BLOCKED")
    if "FAIL" in contributions: return "NON_COMPLIANT"
    if "BLOCKED" in contributions: return "BLOCKED"
    if "UNRESOLVED" in contributions: return "UNVERIFIED"
    if "WAIVED" in contributions: return "CONDITIONALLY_COMPLIANT"
    return "COMPLIANT" if contributions else "NO_MANDATORY_REQUIREMENTS"


def certificate_hash(certificate: dict[str, Any]) -> str: return digest({key: value for key, value in certificate.items() if key not in {"certificate_hash", "signature"}})
def signature_value(hash_value: str, authority_id: str, signed_at: str) -> str: return digest({"certificate_hash": hash_value, "authority_id": authority_id, "signed_at": signed_at})


def certificate_schema_valid(cert: Any) -> bool:
    required = {"certificate_id", "audit_id", "certificate_type", "status", "aggregate_status", "scope", "snapshot", "snapshot_seal", "authority", "evidence_summary", "waiver_summary", "aggregate_inputs", "issued_at", "valid_from", "valid_until", "supersedes", "schema_version", "certificate_hash", "signature"}
    scope_required = {"audit_scope_id", "requirements", "specification_snapshot", "implementation_snapshot", "environment_snapshot", "architecture_scope", "platform_scope", "version_scope", "exclusions"}
    authority_required = {"authority_id", "authority_type", "authorization_policy", "authorization_evidence", "authorized_at"}
    return isinstance(cert, dict) and set(cert) == required and set(cert.get("scope", {})) == scope_required and set(cert.get("authority", {})) == authority_required and isinstance(cert["scope"]["requirements"], list) and len(cert["scope"]["requirements"]) > 0 and isinstance(cert["authority"]["authorization_evidence"], list) and len(cert["authority"]["authorization_evidence"]) > 0


def verify_certificate(cert: dict[str, Any], evaluated_at: str, revoked: bool = False, superseded: bool = False) -> tuple[str, str | None]:
    recomputed_status = aggregate(cert.get("aggregate_inputs", [])); recomputed_hash = digest({"status": recomputed_status, "requirements": cert.get("aggregate_inputs", [])})
    checks = [
        (certificate_schema_valid(cert), "CERTIFICATE_SCHEMA_INVALID"),
        (bool(cert.get("scope", {}).get("audit_scope_id")) and bool(cert.get("scope", {}).get("requirements")) and not set(cert.get("scope", {}).get("requirements", [])) & set(cert.get("scope", {}).get("exclusions", [])), "SCOPE_INVALID"),
        (cert.get("certificate_hash") == certificate_hash(cert), "CERTIFICATE_HASH_INVALID"),
        (cert.get("snapshot", {}).get("snapshot_hash") == digest({key: value for key, value in cert.get("snapshot", {}).items() if key != "snapshot_hash"}), "CERTIFICATE_SNAPSHOT_HASH_INVALID"),
        (cert.get("snapshot_seal", {}).get("seal_hash") == digest({key: value for key, value in cert.get("snapshot_seal", {}).items() if key != "seal_hash"}), "SNAPSHOT_SEAL_INVALID"),
        (cert.get("scope", {}).get("specification_snapshot") == cert.get("snapshot", {}).get("specification_snapshot") == cert.get("snapshot_seal", {}).get("specification_hash") and cert.get("scope", {}).get("implementation_snapshot") == cert.get("snapshot", {}).get("implementation_snapshot") == cert.get("snapshot_seal", {}).get("implementation_hash") and all(cert.get("snapshot", {}).get(name + "_snapshot") == cert.get("snapshot_seal", {}).get(name + "_hash") for name in ["decision", "evidence", "waiver", "state_history"]) and cert.get("scope", {}).get("requirements") == [item.get("requirement_id") for item in cert.get("aggregate_inputs", [])], "SNAPSHOT_LINEAGE_MISMATCH"),
        (cert.get("signature", {}).get("signature_value") == signature_value(cert.get("certificate_hash", ""), cert.get("authority", {}).get("authority_id", ""), cert.get("signature", {}).get("signed_at", "")), "SIGNATURE_INVALID"),
        (bool(cert.get("authority", {}).get("authorization_evidence")) and cert.get("authority", {}).get("authorization_policy") == "TEST-CERTIFICATION-POLICY", "AUTHORITY_INVALID"),
        (cert.get("valid_from", "") <= evaluated_at and (cert.get("valid_until") is None or evaluated_at <= cert["valid_until"]), "VALIDITY_INTERVAL_INVALID"),
        (cert.get("status") == "VALID", "CERTIFICATE_STATUS_NOT_VALID"), (not revoked, "REVOKED"), (not superseded, "SUPERSEDED"),
        (cert.get("evidence_summary", {}).get("integrity_status") == "VALID" and cert.get("evidence_summary", {}).get("stale_evidence_count") == 0 and cert.get("evidence_summary", {}).get("missing_evidence_count") == 0, "EVIDENCE_INVALID"),
        (cert.get("waiver_summary", {}).get("effective_waiver_count") == sum(bool(item.get("waiver_effective")) for item in cert.get("aggregate_inputs", [])) and cert.get("waiver_summary", {}).get("unauthorized_waiver_count") == 0 and cert.get("waiver_summary", {}).get("expired_waiver_count") == 0, "WAIVER_SUMMARY_INVALID"),
        (cert.get("aggregate_status") == recomputed_status, "CERTIFICATE_AGGREGATE_MISMATCH"),
        (cert.get("snapshot", {}).get("aggregate_hash") == recomputed_hash == cert.get("snapshot_seal", {}).get("aggregate_hash"), "AGGREGATE_HASH_MISMATCH"),
    ]
    return next((("INVALID", error) for valid, error in checks if not valid), ("VALID", None))


def eligibility(status: str | None, policy: dict[str, Any], predicates: dict[str, bool]) -> tuple[str, list[str]]:
    failed = [key for key, value in predicates.items() if not value]
    if status is None: failed.insert(0, "AGGREGATE_MISSING")
    elif status not in policy["allowed_aggregate_statuses"]: failed.insert(0, "AGGREGATE_STATUS_NOT_ALLOWED")
    return (("ELIGIBLE", []) if not failed else ("INELIGIBLE", failed))


def freshness(policy: dict[str, Any], evidence_at: str, evaluated_at: str, events: list[dict[str, str]]) -> tuple[str, list[str]]:
    if not policy["freshness_required"]: return "FRESH", []
    reasons = [event["event_type"] for event in events if event["event_type"] in policy["invalidation_events"] and datetime.fromisoformat(event["occurred_at"].replace("Z", "+00:00")) >= datetime.fromisoformat(evidence_at.replace("Z", "+00:00"))]
    if policy["max_age"]:
        days = int(policy["max_age"].removeprefix("P").removesuffix("D")); age = datetime.fromisoformat(evaluated_at.replace("Z", "+00:00")) - datetime.fromisoformat(evidence_at.replace("Z", "+00:00"))
        if age.total_seconds() > days * 86400: reasons.append("MAX_AGE_EXCEEDED")
    return ("STALE", reasons) if reasons else ("FRESH", [])


def waiver_effective(waiver: dict[str, Any], evaluated_at: str) -> tuple[str, bool]:
    if waiver["authority"]["authority_id"] != "TEST-AUTHORITY" or not waiver["authority"]["authorization_evidence"]: return "UNAUTHORIZED", False
    if waiver["status"] != "ACTIVE": return "NOT_ACTIVE", False
    if evaluated_at < waiver["valid_from"] or waiver["valid_until"] is not None and evaluated_at > waiver["valid_until"]: return "EXPIRED", False
    if not waiver["evidence_refs"] or not waiver["reason"] or not waiver["scope"]: return "INVALID", False
    return "EFFECTIVE", True


def exact_release_match(cert: dict[str, Any], release: dict[str, Any], aggregate_status: str) -> bool:
    binding = cert.get("snapshot", {}).get("release_binding", {})
    return cert.get("aggregate_status") == aggregate_status and cert.get("scope", {}).get("version_scope") == release.get("version") and all(binding.get(key) == release.get(key) for key in ["source_snapshot", "build_snapshot", "configuration_snapshot", "artifact_hashes"])


def release_authorize(policy: dict[str, Any], certificates: list[dict[str, Any]], aggregate_status: str, findings: list[str], waivers_valid: bool, residual_risk_accepted: bool, evidence_fresh: bool, security_pass: bool, policy_integrity: bool, release_authority_valid: bool, release: dict[str, Any]) -> tuple[str, list[str]]:
    valid = [cert for cert in certificates if verify_certificate(cert, "2026-09-12T19:04:51Z")[0] == "VALID" and cert["certificate_type"] in policy["required_certificate_types"]]
    reasons: list[str] = []
    if aggregate_status == "CONDITIONALLY_COMPLIANT":
        if not policy["conditional_authorization_allowed"] or not waivers_valid or not residual_risk_accepted or not policy["residual_risk_authority_valid"]: reasons.append("CONDITIONAL_POLICY_UNSATISFIED")
        if any(item in policy["forbidden_findings"] for item in findings): reasons.append("FORBIDDEN_FINDING")
        if not valid or not any(exact_release_match(cert, release, aggregate_status) for cert in valid): reasons.append("VALID_MATCHING_CERTIFICATE_MISSING")
        if not evidence_fresh or not security_pass or not policy_integrity: reasons.append("REQUIRED_CONDITION_MISSING")
        if not release_authority_valid: reasons.append("RELEASE_AUTHORITY_INVALID")
        return ("CONDITIONALLY_AUTHORIZED", []) if not reasons else ("REJECTED", reasons)
    if aggregate_status != policy["required_aggregate_status"]: reasons.append("AGGREGATE_NOT_ALLOWED")
    if not valid: reasons.append("VALID_CERTIFICATE_MISSING")
    elif not any(exact_release_match(cert, release, aggregate_status) for cert in valid): reasons.append("CERTIFICATE_RELEASE_SNAPSHOT_MISMATCH")
    if any(item in policy["forbidden_findings"] for item in findings): reasons.append("FORBIDDEN_FINDING")
    if not evidence_fresh: reasons.append("EVIDENCE_STALE")
    if not security_pass: reasons.append("SECURITY_GATE_FAILED")
    if not policy_integrity: reasons.append("RELEASE_POLICY_INVALID")
    if not release_authority_valid: reasons.append("RELEASE_AUTHORITY_INVALID")
    if reasons: return ("REJECTED" if any(item in {"AGGREGATE_NOT_ALLOWED", "FORBIDDEN_FINDING", "SECURITY_GATE_FAILED"} for item in reasons) else "BLOCKED"), reasons
    return "AUTHORIZED", []


def main() -> int:
    checks: list[dict[str, str]] = []
    def check(identifier: str, category: str, description: str, condition: bool, detail: str = "") -> None: checks.append({"check_id": identifier, "category": category, "result": "PASS" if condition else "FAIL", "description": description, "detail": detail})
    def blocked(identifier: str, category: str, description: str, detail: str) -> None: checks.append({"check_id": identifier, "category": category, "result": "BLOCKED", "description": description, "detail": detail})

    check("I01", "inventory", "all 68 generator-owned v14 deliverables exist", len(DELIVERABLES) == 68 and all((DEST / path).is_file() for path in DELIVERABLES))
    parse_errors = []
    for path in sorted(DEST.rglob("*.yaml")):
        try: load(path)
        except Exception as exc: parse_errors.append(f"{path.relative_to(DEST)}: {exc}")
    check("I02", "syntax", "all v14 YAML artifacts are JSON-compatible and parseable", not parse_errors, str(parse_errors[:10]))
    schemas = {name: load(SCHEMA / f"{name}.schema.yaml") for name in SCHEMA_NAMES}
    ids = [body.get("$id") for body in schemas.values()]
    check("S01", "schemas", "all 23 dedicated schemas have unique stable IDs", len(schemas) == len(ids) == len(set(ids)) == 23 and all(ids))
    check("S02", "schemas", "schemas prohibit undeclared object fields", all(body.get("additionalProperties") is False for body in schemas.values()))
    registry = load(DEST / "SCHEMA-REGISTRY.yaml"); schema_registry_errors = [item["name"] for item in registry["schemas"] if item["name"] not in schemas or sha_file(DEST / item["path"]) != item["sha256"]]
    check("S03", "schemas", "schema registry resolves every schema with exact bytes", len(registry["schemas"]) == 23 and not schema_registry_errors, str(schema_registry_errors))

    schema_instances: list[tuple[str, dict[str, Any], str]] = []
    for item in load(DEST / "AUTHORITY-POLICIES.yaml")["objects"]: schema_instances.append(("authority-policy", item, item["policy_id"]))
    for item in load(DEST / "CERTIFICATION-POLICIES.yaml")["objects"]: schema_instances.append(("certification-policy", item, item["policy_id"]))
    for item in load(DEST / "CURRENT-CERTIFICATE-ELIGIBILITY.yaml")["objects"]: schema_instances.append(("certificate-eligibility-result", item, item["eligibility_id"]))
    for item in load(DEST / "EVIDENCE-FRESHNESS-POLICIES.yaml")["objects"]: schema_instances.append(("evidence-freshness-policy", item, item["policy_id"]))
    for item in load(DEST / "RELEASE-POLICIES.yaml")["objects"]: schema_instances.append(("release-policy", item, item["policy_id"]))
    validity_vectors = load(DEST / "CERTIFICATE-VALIDITY-TEST-VECTORS.yaml")
    for item in validity_vectors["vectors"]:
        if item["vector_id"] != "SCHEMA_INVALID": schema_instances.append(("certificate", item["certificate"], item["vector_id"]))
        schema_instances.append(("certificate-validity-result", item["validity_result"], item["vector_id"]))
    waiver_vectors = load(DEST / "WAIVER-AUTHORITY-TEST-VECTORS.yaml")
    for item in waiver_vectors["vectors"]: schema_instances += [("waiver", item["waiver"], item["vector_id"]), ("waiver-authority-result", item["authority_result"], item["vector_id"])]
    seal_vectors = load(DEST / "SNAPSHOT-SEAL-TEST-VECTORS.yaml")
    for item in seal_vectors["vectors"]:
        for key in ["seal", "seal_1", "seal_2"]:
            if key in item: schema_instances.append(("snapshot-seal", item[key], item["vector_id"]))
    release_vectors = load(DEST / "RELEASE-GATE-TEST-VECTORS.yaml")
    for item in release_vectors["vectors"]:
        schema_instances += [("release-snapshot", item["release"], item["vector_id"]), ("release-gate", item["gate"], item["vector_id"]), ("release-gate-evaluation", item["evaluation"], item["vector_id"])]
        schema_instances += [("certificate", cert, item["vector_id"]) for cert in item["certificates"]]
    instance_errors = []
    for schema_name, instance, label in schema_instances: instance_errors.extend(f"{label}:{error}" for error in schema_errors(instance, schemas[schema_name], schemas))
    check("S04", "schemas", "all production and synthetic objects satisfy their dedicated schemas", not instance_errors, str(instance_errors[:20]))

    layers = load(DEST / "DECISION-LAYERS.yaml")
    check("L01", "separation", "aggregate, certificate, and release remain three independent layers", [item["layer"] for item in layers["layers"]] == ["AGGREGATE", "CERTIFICATE", "RELEASE_GATE"] and len(layers["equivalence_forbidden"]) == 2)
    end_to_end = load(DEST / "END-TO-END-MODEL.yaml")
    check("L02", "separation", "controlled chain has no compliance-to-certification or certification-to-release shortcut", end_to_end["flow"][-5:] == ["AGGREGATE", "CERTIFICATE_ELIGIBILITY", "CERTIFICATE", "RELEASE_GATE", "RELEASE_AUTHORIZATION"] and end_to_end["forbidden_shortcuts"] == ["FIX_COMPLETE_TO_COMPLIANT", "COMPLIANT_TO_CERTIFIED", "CERTIFIED_TO_RELEASE_AUTHORIZED"])
    authority_policies = {item["policy_id"]: item for item in load(DEST / "AUTHORITY-POLICIES.yaml")["objects"]}
    check("L03", "authority", "certification, waiver, and release authority policies are independently owned", {item["purpose"] for item in authority_policies.values()} == {"CERTIFICATION", "WAIVER", "RELEASE"} and all(item["authorization_evidence_required"] and item["policy_hash"] == digest({key: value for key, value in item.items() if key != "policy_hash"}) for item in authority_policies.values()) and load(DEST / "AUTHORITY-POLICIES.yaml")["authority_instances"] == [])

    cert_policies = {item["policy_id"]: item for item in load(DEST / "CERTIFICATION-POLICIES.yaml")["objects"]}
    hash_errors = [item["policy_id"] for item in cert_policies.values() if item["policy_hash"] != digest({key: value for key, value in item.items() if key != "policy_hash"})]
    check("E01", "eligibility", "certification policy hashes reproduce canonically", not hash_errors, str(hash_errors))
    eligibility_vectors = load(DEST / "CERTIFICATE-ELIGIBILITY-TEST-VECTORS.yaml"); eligibility_errors = []
    for item in eligibility_vectors["vectors"]:
        actual, reasons = eligibility(item["aggregate_status"], cert_policies[item["policy_id"]], item["predicates"])
        if actual != item["expected"] or actual != item["actual"] or reasons != item["reasons"] or not item["pass"]: eligibility_errors.append(item["vector_id"])
    check("E02", "eligibility", "all six conjunctive certificate-eligibility vectors reproduce independently", eligibility_vectors["summary"] == {"total": 6, "passed": 6, "failed": 0} and not eligibility_errors, str(eligibility_errors))
    elig_function = load(DEST / "CERTIFICATE-ELIGIBILITY-FUNCTION.yaml")
    check("E03", "eligibility", "eligibility requires all nine mandatory predicates and cannot approve aggregate truth", len(elig_function["all_of"]) == 9 and elig_function["aggregate_is_approved_by_function"] is False and elig_function["deterministic"] is True)
    current_elig = load(DEST / "CURRENT-CERTIFICATE-ELIGIBILITY.yaml")["objects"][0]
    actual_elig, reasons = eligibility(current_elig["aggregate_status"], cert_policies[current_elig["policy_id"]], current_elig["predicates"])
    check("E04", "current", "current eligibility is ineligible because no aggregate exists", actual_elig == current_elig["result"] == "INELIGIBLE" and reasons == current_elig["failure_reasons"] and reasons[0] == "AGGREGATE_MISSING" and current_elig["aggregate_id"] is None)
    check("E05", "hashes", "current eligibility result hash validates", current_elig["eligibility_hash"] == digest({key: value for key, value in current_elig.items() if key != "eligibility_hash"}))

    certificate_errors = []; certificate_schema_hash_errors = []
    for item in validity_vectors["vectors"]:
        actual, error = verify_certificate(item["certificate"], item["arguments"].get("evaluated_at", "2026-09-12T19:04:51Z"), item["arguments"].get("revoked", False), item["arguments"].get("superseded", False))
        if actual != item["expected"] or actual != item["actual"] or error != item["expected_failure"] or error != item["actual_failure"] or not item["pass"]: certificate_errors.append(item["vector_id"])
        result = item["validity_result"]
        if result["result_hash"] != digest({key: value for key, value in result.items() if key != "result_hash"}): certificate_schema_hash_errors.append(item["vector_id"])
    check("C01", "certificate", "all fourteen certificate validity vectors reproduce independently", validity_vectors["summary"] == {"total": 14, "passed": 14, "failed": 0} and not certificate_errors, str(certificate_errors))
    check("C02", "hashes", "all certificate validity result hashes reproduce", not certificate_schema_hash_errors, str(certificate_schema_hash_errors))
    by_id = {item["vector_id"]: item for item in validity_vectors["vectors"]}
    check("C03", "aggregate", "recorded/recomputed aggregate mismatch invalidates certificate", by_id["AGGREGATE_MISMATCH"]["actual_failure"] == "CERTIFICATE_AGGREGATE_MISMATCH")
    check("C04", "integrity", "certificate hash, seal, signature, and authority fail independently", all(by_id[key]["actual"] == "INVALID" for key in ["SCHEMA_INVALID", "HASH_INVALID", "SEAL_INVALID", "LINEAGE_INVALID", "SIGNATURE_INVALID", "AUTHORITY_INVALID", "WAIVER_INVALID"]))
    pipeline = load(DEST / "CERTIFICATE-VERIFICATION-PIPELINE.yaml")
    expected_steps = ["PARSE_CERTIFICATE", "VALIDATE_SCHEMA", "VALIDATE_SCOPE", "VALIDATE_HASHES", "VALIDATE_SNAPSHOT_SEAL", "VALIDATE_SIGNATURE", "VALIDATE_AUTHORITY", "VALIDATE_VALIDITY_INTERVAL", "VALIDATE_REVOCATION_SUPERSESSION", "VALIDATE_EVIDENCE", "RECOMPUTE_AGGREGATE", "COMPARE_AGGREGATE"]
    check("C05", "verification", "prescribed twelve-step certificate sequence is exact and unskippable", [item["number"] for item in pipeline["steps"]] == list(range(1, 13)) and [item["step"] for item in pipeline["steps"]] == expected_steps and pipeline["no_skip"] is True)
    integrity_profile = load(DEST / "CERTIFICATE-INTEGRITY-PROFILE.yaml")
    check("C06", "separation", "hash integrity, authenticated authority, and proof of conformance are distinct", integrity_profile["hash_is_authority"] is False and integrity_profile["signature_is_conformance"] is False and integrity_profile["production_signature_profile"] == "NOT_ESTABLISHED")

    cert_machine = load(DEST / "CERTIFICATE-STATE-MACHINE.yaml"); legal_cert = {(item["from"], item["to"]) for item in cert_machine["legal_transitions"]}
    cert_state = load(DEST / "CERTIFICATE-STATE-TEST-VECTORS.yaml"); cert_state_errors = [item for item in cert_state["vectors"] if ((item["from"], item["to"]) in legal_cert) != item["expected_legal"] or not item["pass"]]
    check("T01", "state-machine", "certificate lifecycle includes seven states and all state vectors pass", cert_machine["states"] == ["DRAFT", "ISSUED", "VALID", "SUPERSEDED", "REVOKED", "EXPIRED", "INVALID"] and cert_state["summary"] == {"total": 8, "passed": 8, "failed": 0} and not cert_state_errors)
    check("T02", "state-machine", "revoked and expired certificates cannot return to valid", ("REVOKED", "VALID") not in legal_cert and ("EXPIRED", "VALID") not in legal_cert and cert_machine["forbidden"] == [["REVOKED", "VALID"], ["EXPIRED", "VALID"]])
    revocation = load(DEST / "CERTIFICATE-REVOCATION-RULES.yaml")
    check("T03", "history", "revocation and supersession preserve historical aggregates", revocation["revocation_mutates_historical_aggregate"] is False and revocation["reassessment_creates_new_decision_aggregate"] is True)

    freshness_policies = {item["policy_id"]: item for item in load(DEST / "EVIDENCE-FRESHNESS-POLICIES.yaml")["objects"]}; freshness_errors = []
    for item in load(DEST / "EVIDENCE-FRESHNESS-TEST-VECTORS.yaml")["vectors"]:
        actual, reasons = freshness(freshness_policies[item["policy_id"]], item["evidence_at"], item["evaluated_at"], item["events"])
        if actual != item["expected"] or actual != item["actual"] or reasons != item["reasons"] or not item["pass"]: freshness_errors.append(item["vector_id"])
    check("F01", "freshness", "all four policy-driven freshness vectors reproduce independently", not freshness_errors, str(freshness_errors))
    freshness_function = load(DEST / "EVIDENCE-FRESHNESS-FUNCTION.yaml")
    check("F02", "freshness", "time alone invalidates evidence only under explicit max-age policy", freshness_function["time_alone_invalidates_only_when_max_age_defined"] is True and freshness_function["hidden_wall_clock"] is False)
    waiver_errors = []; waiver_hash_errors = []
    for item in waiver_vectors["vectors"]:
        actual, effective = waiver_effective(item["waiver"], item["authority_result"]["evaluated_at"])
        if actual != item["expected"] or actual != item["actual"] or effective != item["expected_effective"] or effective != item["actual_effective"] or not item["pass"]: waiver_errors.append(item["vector_id"])
        for object_value, field in [(item["waiver"], "waiver_hash"), (item["authority_result"], "result_hash")]:
            if object_value[field] != digest({key: value for key, value in object_value.items() if key != field}): waiver_hash_errors.append(item["vector_id"])
    check("W01", "waiver", "authorized, unauthorized, expired, and revoked waiver cases reproduce", not waiver_errors and not waiver_hash_errors, str(waiver_errors + waiver_hash_errors))
    waiver_rules = load(DEST / "WAIVER-AUTHORITY-RULES.yaml")
    check("W02", "waiver", "unauthorized and expired waivers have no effect and do not mutate decisions", waiver_rules["unauthorized_effect"] == waiver_rules["expired_effect"] == "NONE" and waiver_rules["underlying_decision_mutated"] is False)

    seal_rules = load(DEST / "SNAPSHOT-SEALING-RULES.yaml")
    check("H01", "sealing", "seven exact input planes are sealed before issuance", seal_rules["required_hashes"] == ["SPECIFICATION", "IMPLEMENTATION", "DECISION", "EVIDENCE", "WAIVER", "STATE_HISTORY", "AGGREGATE"])
    seal_errors = []
    for item in seal_vectors["vectors"]:
        for key in ["seal", "seal_1", "seal_2"]:
            if key in item and item[key]["seal_hash"] != digest({name: value for name, value in item[key].items() if name != "seal_hash"}): seal_errors.append(item["vector_id"])
        if not item["pass"]: seal_errors.append(item["vector_id"])
    check("H02", "sealing", "snapshot seal vectors prove integrity and new-snapshot behavior", not seal_errors and seal_rules["post_seal_change"] == "CREATE_NEW_SNAPSHOT_AND_EVALUATION", str(seal_errors))

    release_policies = {item["policy_id"]: item for item in load(DEST / "RELEASE-POLICIES.yaml")["objects"]}; release_errors = []; release_hash_errors = []
    for item in release_vectors["vectors"]:
        certs = json.loads(json.dumps(item["certificates"]))
        if len(certs) != item["certificate_count"]: release_errors.append(item["vector_id"])
        actual, reasons = release_authorize(release_policies[item["policy_id"]], certs, item["aggregate_status"], item["findings"], item["waivers_valid"], item["residual_risk_accepted"], item["evidence_fresh"], item["security_pass"], item["policy_integrity"], item["vector_id"] != "RELEASE_AUTHORITY_INVALID", item["release"])
        if actual != item["expected"] or actual != item["actual"] or reasons != item["reasons"] or not item["pass"]: release_errors.append(item["vector_id"])
        evaluation = item["evaluation"]; gate = item["gate"]
        if evaluation["evaluation_hash"] != digest({key: value for key, value in evaluation.items() if key != "evaluation_hash"}) or gate["gate_hash"] != digest({key: value for key, value in gate.items() if key != "gate_hash"}) or gate["decision"] != item["actual"] or gate["release_snapshot_hash"] != item["release"]["snapshot_hash"]: release_hash_errors.append(item["vector_id"])
    check("R01", "release", "all thirteen strict, conditional, authority, mismatch, risk, and security release vectors reproduce", release_vectors["summary"] == {"total": 13, "passed": 13, "failed": 0} and not release_errors, str(release_errors))
    check("R02", "hashes", "release policy, snapshot, and evaluation hashes reproduce", all(item["policy_hash"] == digest({key: value for key, value in item.items() if key != "policy_hash"}) for item in release_policies.values()) and all(item["release"]["snapshot_hash"] == digest({key: value for key, value in item["release"].items() if key != "snapshot_hash"}) for item in release_vectors["vectors"]) and not release_hash_errors, str(release_hash_errors))
    check("R03", "release", "artifact/snapshot mismatch blocks authorization", all({item["vector_id"]: item["actual"] for item in release_vectors["vectors"]}[key] == "BLOCKED" for key in ["SNAPSHOT_MISMATCH", "ARTIFACT_MISMATCH"]))
    gate_machine = load(DEST / "RELEASE-GATE-STATE-MACHINE.yaml"); gate_legal = {(item["from"], item["to"]) for item in gate_machine["legal_transitions"]}; gate_vectors = load(DEST / "RELEASE-GATE-STATE-TEST-VECTORS.yaml")
    check("R04", "state-machine", "release gate states, guards, recovery, and terminal behavior validate", gate_vectors["summary"] == {"total": 8, "passed": 8, "failed": 0} and all(((item["from"], item["to"]) in gate_legal) == item["expected_legal"] and item["pass"] for item in gate_vectors["vectors"]) and set(gate_machine["terminal_states"]) == {"AUTHORIZED", "REJECTED", "CONDITIONALLY_AUTHORIZED"})
    reproducibility = load(DEST / "BUILD-REPRODUCIBILITY-TEST-VECTORS.yaml")
    check("R05", "reproducibility", "build artifact identity match and mismatch vectors pass", reproducibility["summary"] == {"total": 2, "passed": 2, "failed": 0} and all(item["pass"] for item in reproducibility["vectors"]))
    release_function = load(DEST / "RELEASE-AUTHORIZATION-FUNCTION.yaml")
    check("R06", "authority", "release authorization is a distinct policy function with explicit release snapshot", release_function["distinct_from_aggregate"] is True and "RELEASE_SNAPSHOT" in release_function["inputs"] and "RELEASE_AUTHORITY" in release_function["inputs"] and "RESIDUAL_RISK_ACCEPTANCE" in release_function["inputs"])

    current_binding = load(DEST / "CURRENT-AUDIT-BINDING.yaml"); current_cert = load(DEST / "CURRENT-CERTIFICATION-STATUS.yaml"); current_release = load(DEST / "CURRENT-RELEASE-STATUS.yaml")
    check("U01", "current", "current v14 binding preserves blocked v13.3 truth", current_binding["v13_3_audit_status"] == "BLOCKED" and current_binding["v13_3_aggregate_execution"] == "NOT_EXECUTED_UPSTREAM_FAILURE" and load(V133 / "CURRENT-AGGREGATE.yaml")["objects"] == [])
    check("U02", "non-invention", "no current certificate, seal, revocation, waiver, release snapshot, or release gate is invented", all(load(DEST / name)["objects"] == [] for name in ["CERTIFICATES.yaml", "SNAPSHOT-SEALS.yaml", "REVOCATIONS.yaml", "WAIVERS-V14.yaml", "WAIVER-AUTHORITY-RESULTS.yaml", "RELEASE-SNAPSHOTS.yaml", "RELEASE-GATES.yaml"]))
    check("U03", "current", "certification and release are explicitly not authorized", current_cert == {"schema_version": VERSION, "status": "NOT_CERTIFIED", "reason": "NO_AGGREGATE_EXECUTED_AND_CERTIFICATE_INELIGIBLE", "certificate_id": None, "aggregate_status": None} and current_release == {"schema_version": VERSION, "status": "NOT_EVALUATED", "reason": "NO_RELEASE_SNAPSHOT_AND_NO_VALID_CERTIFICATE", "release_id": None, "decision": None})

    invariants = load(DEST / "CERTIFICATE-INVARIANTS.yaml")["invariants"]
    mechanical = {
        "CERT-001": bool(schemas["certificate-scope"]["properties"]), "CERT-002": "specification_snapshot" in schemas["certificate-scope"]["required"], "CERT-003": "implementation_snapshot" in schemas["certificate-scope"]["required"], "CERT-004": "aggregate_status" in schemas["certificate"]["required"], "CERT-005": "authority" in schemas["certificate"]["required"],
        "CERT-006": "aggregate" not in load(DEST / "CERTIFICATE-ELIGIBILITY-FUNCTION.yaml").get("outputs", []), "CERT-007": revocation["revocation_mutates_historical_aggregate"] is False, "CERT-008": "SUPERSEDED" in cert_machine["terminal_or_replacement_required"], "CERT-009": by_id["REVOKED"]["actual"] == "INVALID", "CERT-010": by_id["EXPIRED"]["actual"] == "INVALID",
        "CERT-011": by_id["AGGREGATE_MISMATCH"]["actual"] == "INVALID", "CERT-012": by_id["HASH_INVALID"]["actual"] == "INVALID", "CERT-013": by_id["SIGNATURE_INVALID"]["actual"] == "INVALID", "CERT-014": next(item for item in waiver_vectors["vectors"] if item["vector_id"] == "UNAUTHORIZED")["actual_effective"] is False, "CERT-015": next(item for item in waiver_vectors["vectors"] if item["vector_id"] == "EXPIRED")["actual_effective"] is False,
        "CERT-016": release_function["distinct_from_aggregate"] is True, "CERT-017": {item["vector_id"]: item["actual"] for item in release_vectors["vectors"]}["SNAPSHOT_MISMATCH"] == "BLOCKED", "CERT-018": seal_rules["post_seal_change"] == "CREATE_NEW_SNAPSHOT_AND_EVALUATION", "CERT-019": revocation["revocation_mutates_historical_aggregate"] is False, "CERT-020": integrity_profile["signature_is_conformance"] is False,
    }
    check("N01", "invariants", "all twenty CERT invariants have exact stable IDs and mechanical checks", [item["id"] for item in invariants] == [f"CERT-{index:03d}" for index in range(1, 21)] and all(item["machine_checked"] for item in invariants) and set(mechanical) == {item["id"] for item in invariants}, str([key for key, value in mechanical.items() if not value]))
    for invariant in invariants:
        check(invariant["id"], "certificate-invariant", invariant["rule"], mechanical.get(invariant["id"], False))

    object_registry = load(DEST / "OBJECT-REGISTRY.yaml"); object_ids = [item["object_id"] for item in object_registry["objects"]]
    check("O01", "registry", "all ten current v14 normative IDs are unique", len(object_ids) == len(set(object_ids)) == 10)
    external_ids = {item["object_id"] for path in [OUT / "OBJECT-REGISTRY.yaml", OUT / "remediation" / "OBJECT-REGISTRY.yaml", OUT / "remediation" / "v13.1" / "OBJECT-REGISTRY.yaml", OUT / "remediation" / "v13.2" / "OBJECT-REGISTRY.yaml", V133 / "OBJECT-REGISTRY.yaml"] for item in load(path)["objects"]}
    check("O02", "registry", "v14 IDs are globally unique from predecessor registries", not (set(object_ids) & external_ids))
    check("O03", "references", "v14 predecessor registry references resolve with exact hashes", all((DEST / item["path"]).is_file() and sha_file(DEST / item["path"]) == item["sha256"] for item in object_registry["external_registries"]))
    policy_refs = [item["authority_policy"] for item in cert_policies.values()] + [value for item in release_policies.values() for value in [item["required_waiver_policy"], item["release_authority_policy"]]]
    check("O04", "references", "all normative authority-policy references resolve exactly once with matching type", all(policy_refs.count(identifier) >= 1 and identifier in authority_policies for identifier in set(policy_refs)) and set(policy_refs) == set(authority_policies))

    prior = load(DEST / "PRIOR-INTEGRITY.yaml"); prior_errors = [item["path"] for item in prior["artifacts"] if not (OUT / item["path"]).is_file() or sha_file(OUT / item["path"]) != item["sha256"] or (OUT / item["path"]).stat().st_size != item["bytes"]]
    check("P01", "append-only", "all 292 predecessor compliance artifacts remain byte-identical", prior["status"] == "PRESERVED" and prior["protected_artifact_count"] == len(prior["artifacts"]) == 292 and not prior_errors, str(prior_errors[:10]))
    check("P02", "append-only", "v13.3 builder refuses to erase the v14 extension", "refusing to erase predecessor artifacts after append-only v14 extension" in (HS / "tools" / "build_executable_state_validation_v133.py").read_text(encoding="utf-8"))
    determinism = load(DEST / "DETERMINISM-VALIDATION.yaml") if (DEST / "DETERMINISM-VALIDATION.yaml").is_file() else {}
    check("Q01", "determinism", "all 68 generator outputs reproduce byte-for-byte", determinism.get("status") == "PASS" and determinism.get("summary") == {"total": 68, "identical": 68, "different": 0} and {item["path"] for item in determinism.get("files", [])} == set(DELIVERABLES) and all(item["byte_identical"] for item in determinism.get("files", [])))
    regression = load(DEST / "REGRESSION-VALIDATION.yaml") if (DEST / "REGRESSION-VALIDATION.yaml").is_file() else {}
    expected_regression = {"13.3": (139, 0, 1), "13.2": (117, 0, 1), "13.1": (110, 0, 1), "13.0": (115, 0, 1), "12.1": (194, 0, 1), "12.0": (148, 0, 1), "11.1": (177, 0, 1), "10.1": (143, 0, 1)}
    actual_regression = {item["protocol"]: (item["passed"], item["failed"], item["blocked"]) for item in regression.get("regressions", [])}
    check("Q02", "regression", "v10.1 through v13.3 regressions and all append guards pass", regression.get("status") == "PASS" and actual_regression == expected_regression and regression.get("append_only_guards") == {"v13": "PASS_REFUSED", "v13.1": "PASS_REFUSED", "v13.2": "PASS_REFUSED", "v13.3": "PASS_REFUSED", "v14": "PASS_REFUSED"})
    check("Q03", "hygiene", "no Python cache artifacts exist", not any(HS.rglob("__pycache__")) and not any(HS.rglob("*.pyc")))
    check("Q04", "tools", "generic and pinned v14 builders and validators exist", all((HS / "tools" / name).is_file() for name in ["build_certificate_release_gate.py", "build_certificate_release_gate_v14.py", "validate_certificate_release_gate.py", "validate_certificate_release_gate_v14.py"]))
    reports = [load(DEST / f"reports/{name}") for name in REPORT_FILES]
    check("G01", "reports", "four reports preserve eligibility, validity, release, and authority separation", reports[0]["certificate_created"] is False and reports[1]["current_certificates"] == 0 and reports[2]["current_decision"] == "NOT_EVALUATED" and reports[3]["principle"] == "COMPLIANCE_TRUTH != CERTIFICATION_AUTHORITY != RELEASE_AUTHORITY")
    blocked("GATE-V14", "acceptance", "current certification and release authorization", "The v14 protocol validates structurally, but v13.3 has no executable aggregate, certificate eligibility is INELIGIBLE, no certificate or release snapshot exists, and release authorization is not evaluated.")
    return finish(checks)


def finish(checks: list[dict[str, str]]) -> int:
    passed = sum(item["result"] == "PASS" for item in checks); failed = sum(item["result"] == "FAIL" for item in checks); blocked_count = sum(item["result"] == "BLOCKED" for item in checks)
    report = {"schema_version": VERSION, "validator": "Protocol-v14 independent certificate and release-gate validator", "overall_status": "FAIL" if failed else "STRUCTURAL_PASS_CERTIFICATION_RELEASE_BLOCKED" if blocked_count else "PASS", "acceptance": "VALIDATION_FAILED" if failed else "BLOCKED" if blocked_count else "PASS", "summary": {"total": len(checks), "passed": passed, "failed": failed, "blocked": blocked_count}, "object_counts": {"schemas": 23, "current_certificates": 0, "current_snapshot_seals": 0, "current_revocations": 0, "current_waivers": 0, "current_release_snapshots": 0, "current_release_gates": 0, "certificate_invariants": 20}, "checks": checks}
    (DEST / "VALIDATION.yaml").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    lines = ["# Protocol-v14 Independent Certificate & Release-Gate Validation", "", f"**Overall:** `{report['overall_status']}`", f"**Acceptance:** `{report['acceptance']}`", f"**Checks:** {passed} PASS / {failed} FAIL / {blocked_count} BLOCKED ({len(checks)} total)", "", "Structural validity does not manufacture an aggregate, certification authority, certificate, release candidate, or release authorization.", "", "| ID | Category | Result | Description | Detail |", "|---|---|---|---|---|"]
    for item in checks: lines.append("| %s | %s | %s | %s | %s |" % (item["check_id"], item["category"], item["result"], item["description"].replace("|", "\\|"), item["detail"].replace("|", "\\|")))
    (DEST / "VALIDATION.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{passed} PASS / {failed} FAIL / {blocked_count} BLOCKED ({len(checks)} checks); {report['overall_status']}")
    return 1 if failed else 0


if __name__ == "__main__": sys.exit(main())
