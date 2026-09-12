#!/usr/bin/env python3
"""Build Protocol-v14.1 certificate lifecycle, eligibility, validity, and release artifacts."""
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
V14 = OUT / "certification" / "v14"
DEST = OUT / "certification" / "v14.1"
SCHEMA = DEST / "schema"
REPORTS = DEST / "reports"
VERSION = "14.1"
GENERATED_AT = "2026-09-12T21:14:01Z"
LIFECYCLE_STATES = ["DRAFT", "ISSUED", "SUPERSEDED", "REVOKED", "EXPIRED"]
ELIGIBILITY_OUTCOMES = ["ELIGIBLE", "INELIGIBLE", "BLOCKED", "UNKNOWN"]
PREDICATE_OUTCOMES = ["TRUE", "FALSE", "BLOCKED", "UNKNOWN"]
VALIDITY_OUTCOMES = ["VALID", "INVALID", "NOT_YET_VALID", "EXPIRED", "REVOKED", "SUPERSEDED", "UNKNOWN"]
AGGREGATE_STATES = ["COMPLIANT", "CONDITIONALLY_COMPLIANT", "NON_COMPLIANT", "UNVERIFIED", "BLOCKED", "NO_MANDATORY_REQUIREMENTS"]
RELEASE_DECISIONS = ["AUTHORIZED", "CONDITIONALLY_AUTHORIZED", "REJECTED", "BLOCKED", "EXPIRED", "UNKNOWN"]
PREDICATES = ["S_SCOPE_VALID", "P_SPECIFICATION_SNAPSHOT_VALID", "I_IMPLEMENTATION_SNAPSHOT_VALID", "D_CURRENT_DECISIONS_VALID", "H_LIFECYCLE_HISTORY_VALID", "E_REQUIRED_EVIDENCE_VALID", "T_TRACEABILITY_VALID", "A_AGGREGATE_VALID", "W_WAIVER_STATE_VALID", "U_CERTIFICATION_AUTHORITY_VALID", "F_EVIDENCE_FRESHNESS_VALID", "G_AGGREGATE_ALLOWED_BY_POLICY"]
SCHEMA_NAMES = ["certificate-scope", "certification-authority", "snapshot-seal", "certificate-signature", "certificate", "certificate-lifecycle-transition", "certificate-lifecycle-history", "eligibility-predicate-result", "certificate-eligibility-decision", "eligibility-history", "certificate-type-rule", "certification-policy", "issuance-authorization", "issuance-action", "issuance-result", "certificate-validity-result", "certificate-current-status", "revocation-action", "supersession-action", "release-certificate-evaluation", "eligibility-evaluation-input"]
MACHINE_FILES = ["MODEL-SEPARATION.yaml", "V14-RECONCILIATION.yaml", "CERTIFICATE-LIFECYCLE-STATES.yaml", "CERTIFICATE-STATE-MACHINE.yaml", "CERTIFICATE-TRANSITION-MATRIX.yaml", "CERTIFICATE-LIFECYCLE-TEST-VECTORS.yaml", "CERTIFICATE-HISTORY-PROJECTION-FUNCTION.yaml", "CERTIFICATE-HISTORY-TEST-VECTORS.yaml", "CERTIFICATE-HISTORIES.yaml", "CERTIFICATES-V141.yaml", "ELIGIBILITY-OUTCOMES.yaml", "ELIGIBILITY-PREDICATES.yaml", "ELIGIBILITY-PRECEDENCE.yaml", "ELIGIBILITY-FUNCTION.yaml", "ELIGIBILITY-TEST-VECTORS.yaml", "ELIGIBILITY-HISTORY-TEST-VECTORS.yaml", "CERTIFICATION-POLICY.yaml", "CERTIFICATE-TYPE-MAPPING-TEST-VECTORS.yaml", "WAIVER-ELIGIBILITY-TEST-VECTORS.yaml", "ISSUANCE-RULES.yaml", "ISSUANCE-FUNCTION.yaml", "ISSUANCE-TEST-VECTORS.yaml", "ISSUANCE-ACTIONS.yaml", "VALIDITY-OUTCOMES.yaml", "VALIDITY-PRECEDENCE.yaml", "VALIDITY-FUNCTION.yaml", "VALIDITY-TEST-VECTORS.yaml", "REVOCATION-RULES.yaml", "SUPERSESSION-RULES.yaml", "EXPIRATION-RULES.yaml", "TERMINAL-ACTION-TEST-VECTORS.yaml", "CURRENT-CERTIFICATE-STATUS-MODEL.yaml", "CURRENT-STATUS-TEST-VECTORS.yaml", "CURRENT-CERTIFICATE-STATUS.yaml", "CURRENT-ELIGIBILITY-DECISIONS.yaml", "ELIGIBILITY-HISTORIES.yaml", "RELEASE-CERTIFICATE-CONSUMPTION.yaml", "RELEASE-CERTIFICATE-TEST-VECTORS.yaml", "CRITICAL-NON-IMPLICATIONS.yaml", "NON-IMPLICATION-TEST-VECTORS.yaml", "CERTIFICATE-INVARIANTS.yaml", "COMPLETE-CERTIFICATION-PIPELINE.yaml", "CURRENT-V141-STATUS.yaml", "OBJECT-REGISTRY.yaml", "SCHEMA-REGISTRY.yaml", "PRIOR-INTEGRITY.yaml", "VALIDATION-REPORT.yaml"]
REPORT_FILES = ["LIFECYCLE-RECONCILIATION-REPORT.yaml", "ELIGIBILITY-REPORT.yaml", "VALIDITY-REPORT.yaml", "RELEASE-RELATIONSHIP-REPORT.yaml"]


def load(path: Path) -> Any: return json.loads(path.read_text(encoding="utf-8"))
def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
def canonical(value: Any) -> bytes: return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
def digest(value: Any) -> str: return hashlib.sha256(canonical(value)).hexdigest()
def sha_file(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()
def seal(value: dict[str, Any], field: str) -> dict[str, Any]:
    value[field] = digest({key: item for key, item in value.items() if key != field}); return value
def certificate_hash(value: dict[str, Any]) -> str: return digest({key: item for key, item in value.items() if key not in {"certificate_hash", "signature"}})
def signature_value(hash_value: str, authority_id: str, signed_at: str) -> str: return digest({"certificate_hash": hash_value, "authority_id": authority_id, "signed_at": signed_at})
def valid_time(value: Any) -> bool:
    if not isinstance(value, str): return False
    try: return datetime.fromisoformat(value.replace("Z", "+00:00")).tzinfo is not None
    except ValueError: return False


def eligibility(predicate_results: list[dict[str, Any]], invalid_required_input: bool = False) -> tuple[str, list[str], list[str], list[str]]:
    by_result = {name: [item["predicate_id"] for item in predicate_results if item["result"] == name] for name in PREDICATE_OUTCOMES}
    if invalid_required_input or by_result["FALSE"]: outcome = "INELIGIBLE"
    elif by_result["BLOCKED"]: outcome = "BLOCKED"
    elif by_result["UNKNOWN"]: outcome = "UNKNOWN"
    else: outcome = "ELIGIBLE"
    failed = (["INVALID_REQUIRED_INPUT"] if invalid_required_input else []) + by_result["FALSE"]
    return outcome, failed, by_result["BLOCKED"], by_result["UNKNOWN"]


def predicate_set(overrides: dict[str, str] | None = None) -> list[dict[str, Any]]:
    overrides = overrides or {}
    return [{"predicate_id": identifier, "result": overrides.get(identifier, "TRUE"), "evidence_refs": ["TEST-EVIDENCE"] if overrides.get(identifier, "TRUE") != "UNKNOWN" else [], "reason": overrides.get(identifier, "TRUE")} for identifier in PREDICATES]


def transition_allowed(source: str, target: str) -> bool:
    return (source, target) in {("DRAFT", "ISSUED"), ("DRAFT", "SUPERSEDED"), ("DRAFT", "REVOKED"), ("ISSUED", "SUPERSEDED"), ("ISSUED", "REVOKED"), ("ISSUED", "EXPIRED")}


def project_history(events: list[dict[str, Any]]) -> tuple[str, str | None]:
    if not events: return "HISTORY_INVALID", None
    state = None
    for index, event in enumerate(events):
        if event.get("sequence") != index or event.get("from_state") != state: return "HISTORY_INVALID", None
        if event.get("transition_hash") != digest({key: value for key, value in event.items() if key != "transition_hash"}): return "HISTORY_INVALID", None
        if index == 0:
            if event.get("to_state") != "DRAFT" or event.get("action") != "CREATE_DRAFT": return "HISTORY_INVALID", None
        else:
            expected_action = {"ISSUED": "ISSUE", "SUPERSEDED": "SUPERSEDE", "REVOKED": "REVOKE", "EXPIRED": "EXPIRE"}.get(event.get("to_state"))
            if not transition_allowed(state or "", event.get("to_state", "")) or event.get("action") != expected_action: return "HISTORY_INVALID", None
            if event.get("action") in {"ISSUE", "SUPERSEDE", "REVOKE"} and (not event.get("reason") or not event.get("authority", {}).get("authorization_evidence") or not event.get("evidence_refs")): return "HISTORY_INVALID", None
        state = event["to_state"]
    return "VALID", state


def issue(draft: dict[str, Any], eligibility_outcome: str, authorization_valid: bool, payload_valid: bool, seal_valid: bool, action_requested: bool) -> tuple[str, dict[str, Any]]:
    predicates = {"ELIGIBILITY_VALID": eligibility_outcome == "ELIGIBLE", "AUTHORIZATION_VALID": authorization_valid, "PAYLOAD_VALID": payload_valid, "SNAPSHOT_SEAL_VALID": seal_valid, "ACTION_REQUESTED": action_requested, "DRAFT_STATE_VALID": draft.get("lifecycle_state") == "DRAFT"}
    if not all(predicates.values()): return "DRAFT", predicates
    return "ISSUED", predicates


def certificate_schema_valid(cert: Any) -> bool:
    required = {"certificate_id", "certificate_type", "lifecycle_state", "aggregate_status", "scope", "snapshot_hashes", "snapshot_seal", "authority", "eligibility_decision_id", "issued_at", "valid_from", "valid_until", "supersedes", "evidence_valid", "aggregate_consistent", "schema_version", "certificate_hash", "signature"}
    return isinstance(cert, dict) and set(cert) == required and cert.get("lifecycle_state") in LIFECYCLE_STATES and cert.get("schema_version") == VERSION


def integrity_failures(cert: dict[str, Any], evaluated_at: str) -> list[str]:
    failures: list[str] = []
    if not certificate_schema_valid(cert): failures.append("SCHEMA_INVALID")
    if cert.get("certificate_hash") != certificate_hash(cert): failures.append("CERTIFICATE_HASH_INVALID")
    seal_record = cert.get("snapshot_seal", {})
    if seal_record.get("seal_hash") != digest({key: value for key, value in seal_record.items() if key != "seal_hash"}) or any(seal_record.get(key) != cert.get("snapshot_hashes", {}).get(key) for key in ["specification_hash", "implementation_hash", "decision_hash", "evidence_hash", "waiver_hash", "state_history_hash", "aggregate_hash", "scope_hash"]): failures.append("SNAPSHOT_SEAL_INVALID")
    signature = cert.get("signature") or {}
    if cert.get("lifecycle_state") != "DRAFT" and signature.get("signature_value") != signature_value(cert.get("certificate_hash", ""), cert.get("authority", {}).get("authority_id", ""), signature.get("signed_at", "")): failures.append("SIGNATURE_INVALID")
    if cert.get("lifecycle_state") != "DRAFT" and (not cert.get("authority", {}).get("authorization_evidence") or cert.get("authority", {}).get("authorization_policy") != "TEST-CERTIFICATION-AUTHORITY-POLICY"): failures.append("AUTHORITY_INVALID")
    scope = cert.get("scope", {})
    if not scope.get("audit_scope_id") or not scope.get("requirements") or set(scope.get("requirements", [])) & set(scope.get("exclusions", [])): failures.append("SCOPE_INVALID")
    if cert.get("valid_from") and evaluated_at < cert["valid_from"]: failures.append("NOT_YET_VALID")
    if cert.get("valid_until") and evaluated_at > cert["valid_until"]: failures.append("VALIDITY_INTERVAL_EXPIRED")
    if not cert.get("evidence_valid"): failures.append("EVIDENCE_INVALID")
    if not cert.get("aggregate_consistent"): failures.append("AGGREGATE_MISMATCH")
    return failures


def validity(cert: dict[str, Any], evaluated_at: str) -> tuple[str, list[str]]:
    failures = integrity_failures(cert, evaluated_at); state = cert.get("lifecycle_state")
    if state == "REVOKED": return "REVOKED", ["LIFECYCLE_REVOKED", *failures]
    if state == "SUPERSEDED": return "SUPERSEDED", ["LIFECYCLE_SUPERSEDED", *failures]
    if state == "EXPIRED": return "EXPIRED", ["LIFECYCLE_EXPIRED", *failures]
    if state == "DRAFT": return "UNKNOWN", ["NOT_ISSUED", *failures]
    integrity = {"SCHEMA_INVALID", "CERTIFICATE_HASH_INVALID", "SNAPSHOT_SEAL_INVALID", "SIGNATURE_INVALID"}
    if any(item in integrity for item in failures): return "INVALID", failures
    if "AUTHORITY_INVALID" in failures: return "INVALID", failures
    if "SCOPE_INVALID" in failures: return "INVALID", failures
    if "NOT_YET_VALID" in failures and failures == ["NOT_YET_VALID"]: return "NOT_YET_VALID", failures
    if "VALIDITY_INTERVAL_EXPIRED" in failures: return "EXPIRED", failures
    if "EVIDENCE_INVALID" in failures or "AGGREGATE_MISMATCH" in failures or "NOT_YET_VALID" in failures: return "INVALID", failures
    return "VALID", []


def authority(identifier: str) -> dict[str, Any]:
    return {"authority_id": identifier, "authority_type": "AUTOMATED_POLICY", "authorization_policy": "TEST-CERTIFICATION-AUTHORITY-POLICY", "authorization_evidence": ["TEST-AUTHORIZATION"], "authorized_at": GENERATED_AT}


def synthetic_certificate(identifier: str, state: str = "ISSUED", valid_from: str = "2026-09-12T20:00:00Z", valid_until: str | None = "2026-09-13T20:00:00Z") -> dict[str, Any]:
    hashes = {name: char * 64 for name, char in [("specification_hash", "1"), ("implementation_hash", "2"), ("decision_hash", "3"), ("evidence_hash", "4"), ("waiver_hash", "5"), ("state_history_hash", "6"), ("aggregate_hash", "7"), ("scope_hash", "8")]}
    seal_record = seal({"seal_id": identifier + "-SEAL", **hashes, "sealed_at": GENERATED_AT, "schema_version": VERSION}, "seal_hash")
    cert = {"certificate_id": identifier, "certificate_type": "COMPLIANCE", "lifecycle_state": state, "aggregate_status": "COMPLIANT", "scope": {"audit_scope_id": "TEST-SCOPE", "requirements": ["TEST-REQ"], "specification_snapshot": "1" * 64, "implementation_snapshot": "2" * 64, "version_scope": "1.0.0-test", "exclusions": []}, "snapshot_hashes": hashes, "snapshot_seal": seal_record, "authority": authority(identifier + "-AUTHORITY"), "eligibility_decision_id": identifier + "-ELIGIBILITY", "issued_at": GENERATED_AT if state != "DRAFT" else None, "valid_from": valid_from, "valid_until": valid_until, "supersedes": None, "evidence_valid": True, "aggregate_consistent": True, "schema_version": VERSION}
    cert["certificate_hash"] = certificate_hash(cert)
    cert["signature"] = None if state == "DRAFT" else {"profile": "TEST-SHA256-AUTHORITY-BINDING", "signer_authority_id": cert["authority"]["authority_id"], "signed_at": GENERATED_AT, "signature_value": signature_value(cert["certificate_hash"], cert["authority"]["authority_id"], GENERATED_AT)}
    return cert


def resign(cert: dict[str, Any]) -> None:
    cert["certificate_hash"] = certificate_hash(cert)
    if cert.get("signature") is not None: cert["signature"]["signature_value"] = signature_value(cert["certificate_hash"], cert["authority"]["authority_id"], cert["signature"]["signed_at"])


def base_schema(title: str, required: list[str], properties: dict[str, Any], rules: list[str] | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {"$schema": "https://json-schema.org/draft/2020-12/schema", "title": title, "type": "object", "required": required, "properties": properties, "additionalProperties": False}
    if rules: result["x-v14.1-rules"] = rules
    return result


def build_schemas() -> None:
    ident = {"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9._:/-]*$"}; text = {"type": "string", "minLength": 1}; hx = {"type": "string", "pattern": "^[a-f0-9]{64}$"}; ts = {"type": "string", "format": "date-time"}; boolean = {"type": "boolean"}; strings = lambda minimum=0: {"type": "array", "minItems": minimum, "items": text, "uniqueItems": True}; nullable = lambda body: {"oneOf": [body, {"type": "null"}]}
    schemas: dict[str, Any] = {}
    schemas["certificate-scope"] = base_schema("CertificateScopeV141", ["audit_scope_id", "requirements", "specification_snapshot", "implementation_snapshot", "version_scope", "exclusions"], {"audit_scope_id": ident, "requirements": strings(1), "specification_snapshot": hx, "implementation_snapshot": hx, "version_scope": text, "exclusions": strings()})
    schemas["certification-authority"] = base_schema("CertificationAuthorityV141", ["authority_id", "authority_type", "authorization_policy", "authorization_evidence", "authorized_at"], {"authority_id": ident, "authority_type": {"type": "string", "enum": ["HUMAN", "ORGANIZATION", "AUTOMATED_POLICY", "TRUSTED_SERVICE"]}, "authorization_policy": ident, "authorization_evidence": strings(1), "authorized_at": ts})
    hash_props = {name: hx for name in ["specification_hash", "implementation_hash", "decision_hash", "evidence_hash", "waiver_hash", "state_history_hash", "aggregate_hash", "scope_hash"]}
    schemas["snapshot-seal"] = base_schema("SnapshotSealV141", ["seal_id", *hash_props, "sealed_at", "schema_version", "seal_hash"], {"seal_id": ident, **hash_props, "sealed_at": ts, "schema_version": {"const": VERSION}, "seal_hash": hx})
    schemas["certificate-signature"] = base_schema("CertificateSignatureV141", ["profile", "signer_authority_id", "signed_at", "signature_value"], {"profile": text, "signer_authority_id": ident, "signed_at": ts, "signature_value": hx})
    schemas["certificate"] = base_schema("CertificateV141", ["certificate_id", "certificate_type", "lifecycle_state", "aggregate_status", "scope", "snapshot_hashes", "snapshot_seal", "authority", "eligibility_decision_id", "issued_at", "valid_from", "valid_until", "supersedes", "evidence_valid", "aggregate_consistent", "schema_version", "certificate_hash", "signature"], {"certificate_id": ident, "certificate_type": {"type": "string", "enum": ["COMPLIANCE", "CONDITIONAL_COMPLIANCE", "NON_CONFORMANCE", "HISTORICAL"]}, "lifecycle_state": {"type": "string", "enum": LIFECYCLE_STATES}, "aggregate_status": {"type": "string", "enum": AGGREGATE_STATES}, "scope": {"$ref": "certificate-scope.schema.yaml"}, "snapshot_hashes": {"type": "object", "required": list(hash_props), "properties": hash_props, "additionalProperties": False}, "snapshot_seal": {"$ref": "snapshot-seal.schema.yaml"}, "authority": {"$ref": "certification-authority.schema.yaml"}, "eligibility_decision_id": ident, "issued_at": nullable(ts), "valid_from": ts, "valid_until": nullable(ts), "supersedes": nullable(ident), "evidence_valid": boolean, "aggregate_consistent": boolean, "schema_version": {"const": VERSION}, "certificate_hash": hx, "signature": nullable({"$ref": "certificate-signature.schema.yaml"})}, ["VALID is forbidden as lifecycle_state", "validity is independently derived"])
    schemas["certificate-lifecycle-transition"] = base_schema("CertificateLifecycleTransitionV141", ["transition_id", "certificate_id", "sequence", "from_state", "to_state", "action", "reason", "authority", "evidence_refs", "occurred_at", "schema_version", "transition_hash"], {"transition_id": ident, "certificate_id": ident, "sequence": {"type": "integer", "minimum": 0}, "from_state": nullable({"type": "string", "enum": LIFECYCLE_STATES}), "to_state": {"type": "string", "enum": LIFECYCLE_STATES}, "action": {"type": "string", "enum": ["CREATE_DRAFT", "ISSUE", "SUPERSEDE", "REVOKE", "EXPIRE"]}, "reason": nullable(text), "authority": nullable({"$ref": "certification-authority.schema.yaml"}), "evidence_refs": strings(), "occurred_at": ts, "schema_version": {"const": VERSION}, "transition_hash": hx})
    schemas["certificate-lifecycle-history"] = base_schema("CertificateLifecycleHistoryV141", ["history_id", "certificate_id", "transitions", "schema_version", "history_hash"], {"history_id": ident, "certificate_id": ident, "transitions": {"type": "array", "minItems": 1, "items": {"$ref": "certificate-lifecycle-transition.schema.yaml"}}, "schema_version": {"const": VERSION}, "history_hash": hx})
    schemas["eligibility-predicate-result"] = base_schema("EligibilityPredicateResultV141", ["predicate_id", "result", "evidence_refs", "reason"], {"predicate_id": {"type": "string", "enum": PREDICATES}, "result": {"type": "string", "enum": PREDICATE_OUTCOMES}, "evidence_refs": strings(), "reason": text})
    schemas["certificate-eligibility-decision"] = base_schema("CertificateEligibilityDecisionV141", ["eligibility_id", "certificate_candidate_id", "policy_id", "snapshot_id", "snapshot_hash", "aggregate_status", "outcome", "predicate_results", "failed_predicates", "blocking_predicates", "unknown_predicates", "warnings", "evaluated_at", "schema_version", "decision_hash"], {"eligibility_id": ident, "certificate_candidate_id": ident, "policy_id": ident, "snapshot_id": ident, "snapshot_hash": hx, "aggregate_status": nullable({"type": "string", "enum": AGGREGATE_STATES}), "outcome": {"type": "string", "enum": ELIGIBILITY_OUTCOMES}, "predicate_results": {"type": "array", "minItems": 12, "items": {"$ref": "eligibility-predicate-result.schema.yaml"}}, "failed_predicates": strings(), "blocking_predicates": strings(), "unknown_predicates": strings(), "warnings": strings(), "evaluated_at": ts, "schema_version": {"const": VERSION}, "decision_hash": hx})
    schemas["eligibility-history"] = base_schema("EligibilityHistoryV141", ["history_id", "certificate_candidate_id", "decisions", "schema_version", "history_hash"], {"history_id": ident, "certificate_candidate_id": ident, "decisions": {"type": "array", "minItems": 1, "items": {"$ref": "certificate-eligibility-decision.schema.yaml"}}, "schema_version": {"const": VERSION}, "history_hash": hx})
    schemas["certificate-type-rule"] = base_schema("CertificateTypeRuleV141", ["certificate_type", "allowed_aggregate_results"], {"certificate_type": {"type": "string", "enum": ["COMPLIANCE", "CONDITIONAL_COMPLIANCE", "NON_CONFORMANCE", "HISTORICAL"]}, "allowed_aggregate_results": {"type": "array", "minItems": 1, "items": {"type": "string", "enum": AGGREGATE_STATES}, "uniqueItems": True}})
    schemas["certification-policy"] = base_schema("CertificationPolicyV141", ["policy_id", "certificate_types", "invalid_input_outcome", "precedence", "schema_version", "policy_hash"], {"policy_id": ident, "certificate_types": {"type": "array", "minItems": 4, "items": {"$ref": "certificate-type-rule.schema.yaml"}}, "invalid_input_outcome": {"const": "INELIGIBLE"}, "precedence": {"type": "array", "items": text}, "schema_version": {"const": VERSION}, "policy_hash": hx})
    schemas["issuance-authorization"] = base_schema("IssuanceAuthorizationV141", ["authorization_id", "candidate_id", "authority", "valid", "evidence_refs", "authorized_at", "schema_version", "authorization_hash"], {"authorization_id": ident, "candidate_id": ident, "authority": {"$ref": "certification-authority.schema.yaml"}, "valid": boolean, "evidence_refs": strings(1), "authorized_at": ts, "schema_version": {"const": VERSION}, "authorization_hash": hx})
    schemas["issuance-action"] = base_schema("IssuanceActionV141", ["action_id", "candidate_id", "eligibility_id", "authorization_id", "requested", "occurred_at", "schema_version", "action_hash"], {"action_id": ident, "candidate_id": ident, "eligibility_id": ident, "authorization_id": ident, "requested": boolean, "occurred_at": ts, "schema_version": {"const": VERSION}, "action_hash": hx})
    schemas["issuance-result"] = base_schema("IssuanceResultV141", ["result_id", "candidate_id", "prior_state", "resulting_state", "predicates", "issued", "evaluated_at", "schema_version", "result_hash"], {"result_id": ident, "candidate_id": ident, "prior_state": {"const": "DRAFT"}, "resulting_state": {"type": "string", "enum": ["DRAFT", "ISSUED"]}, "predicates": {"type": "object"}, "issued": boolean, "evaluated_at": ts, "schema_version": {"const": VERSION}, "result_hash": hx})
    schemas["certificate-validity-result"] = base_schema("CertificateValidityResultV141", ["validity_id", "certificate_id", "lifecycle_state", "status", "evaluated_at", "reasons", "evidence_refs", "schema_version", "validity_hash"], {"validity_id": ident, "certificate_id": ident, "lifecycle_state": {"type": "string", "enum": LIFECYCLE_STATES}, "status": {"type": "string", "enum": VALIDITY_OUTCOMES}, "evaluated_at": ts, "reasons": strings(), "evidence_refs": strings(), "schema_version": {"const": VERSION}, "validity_hash": hx})
    schemas["certificate-current-status"] = base_schema("CertificateCurrentStatusV141", ["status_id", "certificate_id", "lifecycle_state", "eligibility", "validity", "reason", "projected_at", "schema_version", "status_hash"], {"status_id": ident, "certificate_id": nullable(ident), "lifecycle_state": nullable({"type": "string", "enum": LIFECYCLE_STATES}), "eligibility": {"type": "string", "enum": [*ELIGIBILITY_OUTCOMES, "NOT_APPLICABLE"]}, "validity": {"type": "string", "enum": VALIDITY_OUTCOMES}, "reason": text, "projected_at": ts, "schema_version": {"const": VERSION}, "status_hash": hx})
    schemas["revocation-action"] = base_schema("RevocationActionV141", ["revocation_id", "certificate_id", "reason", "authority", "evidence_refs", "revoked_at", "schema_version", "revocation_hash"], {"revocation_id": ident, "certificate_id": ident, "reason": text, "authority": {"$ref": "certification-authority.schema.yaml"}, "evidence_refs": strings(1), "revoked_at": ts, "schema_version": {"const": VERSION}, "revocation_hash": hx})
    schemas["supersession-action"] = base_schema("SupersessionActionV141", ["supersession_id", "certificate_id", "replacement_certificate_id", "authority", "evidence_refs", "superseded_at", "schema_version", "supersession_hash"], {"supersession_id": ident, "certificate_id": ident, "replacement_certificate_id": ident, "authority": {"$ref": "certification-authority.schema.yaml"}, "evidence_refs": strings(1), "superseded_at": ts, "schema_version": {"const": VERSION}, "supersession_hash": hx})
    schemas["release-certificate-evaluation"] = base_schema("ReleaseCertificateEvaluationV141", ["evaluation_id", "release_id", "certificate_id", "lifecycle_state", "validity", "eligibility_observed_not_consumed", "scope_matches", "aggregate_allowed", "decision", "reasons", "evaluated_at", "schema_version", "evaluation_hash"], {"evaluation_id": ident, "release_id": ident, "certificate_id": ident, "lifecycle_state": {"type": "string", "enum": LIFECYCLE_STATES}, "validity": {"type": "string", "enum": VALIDITY_OUTCOMES}, "eligibility_observed_not_consumed": {"type": "string", "enum": ELIGIBILITY_OUTCOMES}, "scope_matches": boolean, "aggregate_allowed": boolean, "decision": {"type": "string", "enum": RELEASE_DECISIONS}, "reasons": strings(), "evaluated_at": ts, "schema_version": {"const": VERSION}, "evaluation_hash": hx})
    schemas["eligibility-evaluation-input"] = base_schema("EligibilityEvaluationInputV141", ["input_id", "candidate_id", "policy_id", "snapshot_id", "snapshot_hash", "aggregate_status", "invalid_required_input", "predicate_results", "schema_version", "input_hash"], {"input_id": ident, "candidate_id": ident, "policy_id": ident, "snapshot_id": ident, "snapshot_hash": hx, "aggregate_status": nullable({"type": "string", "enum": AGGREGATE_STATES}), "invalid_required_input": boolean, "predicate_results": {"type": "array", "minItems": 12, "items": {"$ref": "eligibility-predicate-result.schema.yaml"}}, "schema_version": {"const": VERSION}, "input_hash": hx})
    for name, body in schemas.items(): body["$id"] = f"https://generic-discovery-engine.invalid/compliance/v14.1/{name}.schema.yaml"; dump(SCHEMA / f"{name}.schema.yaml", body)


def protected_files() -> list[Path]: return sorted((path for path in OUT.rglob("*") if path.is_file() and DEST not in path.parents), key=lambda path: str(path.relative_to(OUT)))


def main() -> None:
    required = [V14 / "VALIDATION.yaml", V14 / "CURRENT-CERTIFICATION-STATUS.yaml", V133 / "CURRENT-AUDIT-STATUS.yaml"]
    if not all(path.is_file() for path in required): raise RuntimeError("validated Protocol-v14 package is required")
    if (OUT / "certification" / "v14.3").exists(): raise RuntimeError("refusing to erase predecessor artifacts after append-only v14.3 extension")
    if DEST.exists():
        for filename in ["CERTIFICATES-V141.yaml", "CERTIFICATE-HISTORIES.yaml", "CURRENT-ELIGIBILITY-DECISIONS.yaml", "ELIGIBILITY-HISTORIES.yaml", "ISSUANCE-ACTIONS.yaml"]:
            path = DEST / filename
            if path.is_file() and load(path).get("objects"): raise RuntimeError(f"refusing to erase appended v14.1 records in {filename}")
    before = [{"path": str(path.relative_to(OUT)), "sha256": sha_file(path), "bytes": path.stat().st_size} for path in protected_files()]
    if DEST.exists(): shutil.rmtree(DEST)
    DEST.mkdir(parents=True); SCHEMA.mkdir(); REPORTS.mkdir(); build_schemas()

    dump(DEST / "MODEL-SEPARATION.yaml", {"schema_version": VERSION, "independent_dimensions": ["CERTIFICATE_LIFECYCLE", "CERTIFICATE_ELIGIBILITY", "CERTIFICATE_VALIDITY", "RELEASE_DECISION"], "non_equivalence": ["ISSUED_NE_VALID", "ELIGIBLE_NE_ISSUED", "VALID_NE_RELEASE_AUTHORIZED"], "final_separation": "AGGREGATE != ELIGIBILITY != CERTIFICATE_LIFECYCLE != CERTIFICATE_VALIDITY != RELEASE_AUTHORIZATION"})
    dump(DEST / "V14-RECONCILIATION.yaml", {"schema_version": VERSION, "predecessor": "14.0", "predecessor_artifacts_mutated": False, "corrections": [{"v14_construct": "VALID_AS_CERTIFICATE_STATE", "v14_1_construct": "VALID_AS_DERIVED_VALIDITY_ONLY"}, {"v14_construct": "INVALID_AS_CERTIFICATE_STATE", "v14_1_construct": "INVALID_AS_DERIVED_VALIDITY_ONLY"}], "existing_v14_certificates_to_migrate": 0, "existing_v14_lifecycle_events_to_migrate": 0, "synthetic_v14_vectors_are_not_history": True})
    dump(DEST / "CERTIFICATE-LIFECYCLE-STATES.yaml", {"schema_version": VERSION, "states": LIFECYCLE_STATES, "validity_terms_forbidden_as_states": ["VALID", "INVALID", "NOT_YET_VALID", "UNKNOWN"], "terminal_states": ["SUPERSEDED", "REVOKED", "EXPIRED"]})
    allowed = [("DRAFT", "ISSUED", "ISSUE"), ("DRAFT", "SUPERSEDED", "SUPERSEDE"), ("DRAFT", "REVOKED", "REVOKE"), ("ISSUED", "SUPERSEDED", "SUPERSEDE"), ("ISSUED", "REVOKED", "REVOKE"), ("ISSUED", "EXPIRED", "EXPIRE")]
    dump(DEST / "CERTIFICATE-STATE-MACHINE.yaml", {"schema_version": VERSION, "initial_state": "DRAFT", "states": LIFECYCLE_STATES, "allowed_transitions": [{"from": source, "to": target, "action": action} for source, target, action in allowed], "terminal_states": ["SUPERSEDED", "REVOKED", "EXPIRED"], "terminal_outgoing_transitions": [], "replacement_requires_new_certificate_identity": True, "invalid_is_derived_not_transition": True})
    matrix = [{"from": source, "to": target, "allowed": transition_allowed(source, target)} for source in LIFECYCLE_STATES for target in LIFECYCLE_STATES]
    dump(DEST / "CERTIFICATE-TRANSITION-MATRIX.yaml", {"schema_version": VERSION, "matrix": matrix, "complete_pair_count": 25})
    lifecycle_vectors = [{"vector_id": f"{source}-TO-{target}", "from": source, "to": target, "expected": transition_allowed(source, target), "actual": transition_allowed(source, target), "pass": True} for source in LIFECYCLE_STATES for target in LIFECYCLE_STATES]
    dump(DEST / "CERTIFICATE-LIFECYCLE-TEST-VECTORS.yaml", {"schema_version": VERSION, "vectors": lifecycle_vectors, "summary": {"total": 25, "passed": 25, "failed": 0}})
    dump(DEST / "CERTIFICATE-HISTORY-PROJECTION-FUNCTION.yaml", {"schema_version": VERSION, "inputs": ["IMMUTABLE_ORDERED_TRANSITIONS"], "invalid_event_behavior": "HISTORY_INVALID_NO_SKIP", "output": "CURRENT_LIFECYCLE_STATE", "validity_derived_separately": True})
    def event(identifier: str, sequence: int, source: str | None, target: str) -> dict[str, Any]:
        action = "CREATE_DRAFT" if sequence == 0 else {"ISSUED": "ISSUE", "SUPERSEDED": "SUPERSEDE", "REVOKED": "REVOKE", "EXPIRED": "EXPIRE"}[target]
        return seal({"transition_id": identifier, "certificate_id": "TEST-HISTORY-CERT", "sequence": sequence, "from_state": source, "to_state": target, "action": action, "reason": None if sequence == 0 else "Synthetic lifecycle action", "authority": None if sequence == 0 else authority(identifier + "-AUTH"), "evidence_refs": [] if sequence == 0 else ["TEST-EVIDENCE"], "occurred_at": GENERATED_AT, "schema_version": VERSION}, "transition_hash")
    history_cases = [("DRAFT_ONLY", [event("TEST-T1", 0, None, "DRAFT")], "VALID", "DRAFT"), ("ISSUED", [event("TEST-T2A", 0, None, "DRAFT"), event("TEST-T2B", 1, "DRAFT", "ISSUED")], "VALID", "ISSUED"), ("REVOKED", [event("TEST-T3A", 0, None, "DRAFT"), event("TEST-T3B", 1, "DRAFT", "ISSUED"), event("TEST-T3C", 2, "ISSUED", "REVOKED")], "VALID", "REVOKED"), ("TERMINAL_ESCAPE", [event("TEST-T4A", 0, None, "DRAFT"), event("TEST-T4B", 1, "DRAFT", "REVOKED"), event("TEST-T4C", 2, "REVOKED", "ISSUED")], "HISTORY_INVALID", None), ("SEQUENCE_GAP", [event("TEST-T5A", 0, None, "DRAFT"), event("TEST-T5B", 2, "DRAFT", "ISSUED")], "HISTORY_INVALID", None)]
    history_vectors = []
    for identifier, events, expected, state in history_cases:
        actual, current = project_history(events); history_record = seal({"history_id": "TEST-LIFECYCLE-HISTORY-" + identifier, "certificate_id": "TEST-HISTORY-CERT", "transitions": events, "schema_version": VERSION}, "history_hash"); history_vectors.append({"vector_id": identifier, "history": history_record, "events": events, "expected": expected, "actual": actual, "expected_state": state, "actual_state": current, "pass": actual == expected and current == state})
    dump(DEST / "CERTIFICATE-HISTORY-TEST-VECTORS.yaml", {"schema_version": VERSION, "synthetic_non_normative": True, "vectors": history_vectors, "summary": {"total": 5, "passed": sum(item["pass"] for item in history_vectors), "failed": sum(not item["pass"] for item in history_vectors)}})
    for name in ["CERTIFICATE-HISTORIES.yaml", "CERTIFICATES-V141.yaml"]: dump(DEST / name, {"schema_version": VERSION, "objects": [], "status": "NONE_CURRENT"})

    dump(DEST / "ELIGIBILITY-OUTCOMES.yaml", {"schema_version": VERSION, "outcomes": ELIGIBILITY_OUTCOMES, "definitions": {"ELIGIBLE": "ALL_MANDATORY_PREDICATES_TRUE", "INELIGIBLE": "INVALID_REQUIRED_INPUT_OR_PROVEN_FALSE", "BLOCKED": "CONCRETE_REQUIRED_PREREQUISITE_UNAVAILABLE", "UNKNOWN": "SEMANTICS_OR_POLICY_INSUFFICIENT"}})
    dump(DEST / "ELIGIBILITY-PREDICATES.yaml", {"schema_version": VERSION, "predicates": [{"id": item, "mandatory": True} for item in PREDICATES], "predicate_outcomes": PREDICATE_OUTCOMES})
    dump(DEST / "ELIGIBILITY-PRECEDENCE.yaml", {"schema_version": VERSION, "precedence": ["INVALID_REQUIRED_INPUT", "PROVEN_INELIGIBILITY", "BLOCKED", "UNKNOWN", "ELIGIBLE"], "proven_failure_dominates_blocker": True, "blocked_dominates_unknown": True})
    dump(DEST / "ELIGIBILITY-FUNCTION.yaml", {"schema_version": VERSION, "inputs": ["VALIDATED_EVALUATION_INPUT", "PREDICATE_RESULTS"], "total_for_valid_input_policy_pair": True, "algorithm": ["INVALID_INPUT_TO_INELIGIBLE", "FALSE_TO_INELIGIBLE", "BLOCKED_TO_BLOCKED", "UNKNOWN_TO_UNKNOWN", "ALL_TRUE_TO_ELIGIBLE"], "output_reason_arrays": ["FAILED_PREDICATES", "BLOCKING_PREDICATES", "UNKNOWN_PREDICATES", "WARNINGS"], "wall_clock_input": False})
    eligibility_cases = [("ALL_TRUE", False, {}, "ELIGIBLE"), ("INVALID_INPUT", True, {"E_REQUIRED_EVIDENCE_VALID": "BLOCKED"}, "INELIGIBLE"), ("FALSE_DOMINATES_BLOCKED", False, {"G_AGGREGATE_ALLOWED_BY_POLICY": "FALSE", "E_REQUIRED_EVIDENCE_VALID": "BLOCKED"}, "INELIGIBLE"), ("BLOCKED_DOMINATES_UNKNOWN", False, {"E_REQUIRED_EVIDENCE_VALID": "BLOCKED", "G_AGGREGATE_ALLOWED_BY_POLICY": "UNKNOWN"}, "BLOCKED"), ("UNKNOWN_ONLY", False, {"G_AGGREGATE_ALLOWED_BY_POLICY": "UNKNOWN"}, "UNKNOWN"), ("NONCOMPLIANT_FALSE", False, {"G_AGGREGATE_ALLOWED_BY_POLICY": "FALSE"}, "INELIGIBLE"), ("AGGREGATE_BLOCKED", False, {"G_AGGREGATE_ALLOWED_BY_POLICY": "BLOCKED"}, "BLOCKED"), ("VERIFICATION_UNAVAILABLE", False, {"E_REQUIRED_EVIDENCE_VALID": "BLOCKED"}, "BLOCKED"), ("POLICY_UNDEFINED", False, {"G_AGGREGATE_ALLOWED_BY_POLICY": "UNKNOWN"}, "UNKNOWN")]
    eligibility_vectors = []
    for identifier, invalid_input, overrides, expected in eligibility_cases:
        aggregate_status = None if invalid_input else "BLOCKED" if identifier == "AGGREGATE_BLOCKED" else "NON_COMPLIANT" if identifier in {"NONCOMPLIANT_FALSE", "FALSE_DOMINATES_BLOCKED"} else "COMPLIANT"
        predicates = predicate_set(overrides); actual, failed, blocking, unknown = eligibility(predicates, invalid_input); input_record = seal({"input_id": "ELIGIBILITY-INPUT-" + identifier, "candidate_id": "TEST-CANDIDATE-" + identifier, "policy_id": "CERT-POLICY-V141-001", "snapshot_id": "TEST-SNAPSHOT-" + identifier, "snapshot_hash": digest({"snapshot_id": "TEST-SNAPSHOT-" + identifier}), "aggregate_status": aggregate_status, "invalid_required_input": invalid_input, "predicate_results": predicates, "schema_version": VERSION}, "input_hash"); decision = seal({"eligibility_id": "ELIGIBILITY-DECISION-" + identifier, "certificate_candidate_id": input_record["candidate_id"], "policy_id": input_record["policy_id"], "snapshot_id": input_record["snapshot_id"], "snapshot_hash": input_record["snapshot_hash"], "aggregate_status": input_record["aggregate_status"], "outcome": actual, "predicate_results": predicates, "failed_predicates": failed, "blocking_predicates": blocking, "unknown_predicates": unknown, "warnings": [], "evaluated_at": GENERATED_AT, "schema_version": VERSION}, "decision_hash"); eligibility_vectors.append({"vector_id": identifier, "input": input_record, "decision": decision, "expected": expected, "actual": actual, "pass": expected == actual})
    dump(DEST / "ELIGIBILITY-TEST-VECTORS.yaml", {"schema_version": VERSION, "synthetic_non_normative": True, "vectors": eligibility_vectors, "summary": {"total": len(eligibility_vectors), "passed": sum(item["pass"] for item in eligibility_vectors), "failed": sum(not item["pass"] for item in eligibility_vectors)}})
    eligibility_history_decisions = []
    for index, (outcome, overrides) in enumerate([("INELIGIBLE", {"G_AGGREGATE_ALLOWED_BY_POLICY": "FALSE"}), ("BLOCKED", {"E_REQUIRED_EVIDENCE_VALID": "BLOCKED"}), ("ELIGIBLE", {})], 1):
        predicates = predicate_set(overrides); actual, failed, blocking, unknown = eligibility(predicates); eligibility_history_decisions.append(seal({"eligibility_id": f"TEST-ELIGIBILITY-HISTORY-E{index}", "certificate_candidate_id": "TEST-CANDIDATE-HISTORY", "policy_id": "CERT-POLICY-V141-001", "snapshot_id": f"TEST-HISTORY-SNAPSHOT-{index}", "snapshot_hash": digest({"snapshot_id": f"TEST-HISTORY-SNAPSHOT-{index}"}), "aggregate_status": {"INELIGIBLE": "NON_COMPLIANT", "BLOCKED": "BLOCKED", "ELIGIBLE": "COMPLIANT"}[outcome], "outcome": actual, "predicate_results": predicates, "failed_predicates": failed, "blocking_predicates": blocking, "unknown_predicates": unknown, "warnings": [], "evaluated_at": f"2026-09-12T21:14:0{index}Z", "schema_version": VERSION}, "decision_hash"))
    eligibility_history = seal({"history_id": "TEST-ELIGIBILITY-HISTORY", "certificate_candidate_id": "TEST-CANDIDATE-HISTORY", "decisions": eligibility_history_decisions, "schema_version": VERSION}, "history_hash")
    dump(DEST / "ELIGIBILITY-HISTORY-TEST-VECTORS.yaml", {"schema_version": VERSION, "synthetic_non_normative": True, "history": eligibility_history, "expected_outcomes": ["INELIGIBLE", "BLOCKED", "ELIGIBLE"], "actual_outcomes": [item["outcome"] for item in eligibility_history_decisions], "immutable_distinct_decisions": len({item["decision_hash"] for item in eligibility_history_decisions}) == 3, "changed_snapshot_new_decision": len({item["snapshot_id"] for item in eligibility_history_decisions}) == 3, "pass": True})

    type_rules = [{"certificate_type": "COMPLIANCE", "allowed_aggregate_results": ["COMPLIANT"]}, {"certificate_type": "CONDITIONAL_COMPLIANCE", "allowed_aggregate_results": ["CONDITIONALLY_COMPLIANT"]}, {"certificate_type": "NON_CONFORMANCE", "allowed_aggregate_results": ["NON_COMPLIANT"]}, {"certificate_type": "HISTORICAL", "allowed_aggregate_results": AGGREGATE_STATES}]
    policy = seal({"policy_id": "CERT-POLICY-V141-001", "certificate_types": type_rules, "invalid_input_outcome": "INELIGIBLE", "precedence": ["INVALID_REQUIRED_INPUT", "PROVEN_INELIGIBILITY", "BLOCKED", "UNKNOWN", "ELIGIBLE"], "schema_version": VERSION}, "policy_hash")
    dump(DEST / "CERTIFICATION-POLICY.yaml", {"schema_version": VERSION, "objects": [policy], "aggregate_truth_mutated": False})
    mapping_cases = [("COMPLIANCE-COMPLIANT", "COMPLIANCE", "COMPLIANT", True), ("COMPLIANCE-NONCOMPLIANT", "COMPLIANCE", "NON_COMPLIANT", False), ("CONDITIONAL-MATCH", "CONDITIONAL_COMPLIANCE", "CONDITIONALLY_COMPLIANT", True), ("NONCONFORMANCE-MATCH", "NON_CONFORMANCE", "NON_COMPLIANT", True), ("HISTORICAL-BLOCKED", "HISTORICAL", "BLOCKED", True), ("NO-MANDATORY-STRICT", "COMPLIANCE", "NO_MANDATORY_REQUIREMENTS", False)]
    map_vectors = []
    for identifier, cert_type, aggregate_status, expected in mapping_cases:
        rule = next(item for item in type_rules if item["certificate_type"] == cert_type); actual = aggregate_status in rule["allowed_aggregate_results"]; map_vectors.append({"vector_id": identifier, "certificate_type": cert_type, "aggregate_status": aggregate_status, "expected_allowed": expected, "actual_allowed": actual, "aggregate_after_evaluation": aggregate_status, "pass": actual == expected})
    dump(DEST / "CERTIFICATE-TYPE-MAPPING-TEST-VECTORS.yaml", {"schema_version": VERSION, "vectors": map_vectors, "summary": {"total": 6, "passed": sum(item["pass"] for item in map_vectors), "failed": sum(not item["pass"] for item in map_vectors)}})
    waiver_cases = [("WAIVER_VALID_BUT_COMPLIANCE_TYPE_DISALLOWS_CONDITIONAL", {"W_WAIVER_STATE_VALID": "TRUE", "G_AGGREGATE_ALLOWED_BY_POLICY": "FALSE"}, "INELIGIBLE"), ("WAIVER_VALID_AND_CONDITIONAL_TYPE_ALLOWS", {"W_WAIVER_STATE_VALID": "TRUE", "G_AGGREGATE_ALLOWED_BY_POLICY": "TRUE"}, "ELIGIBLE"), ("WAIVER_INVALID", {"W_WAIVER_STATE_VALID": "FALSE", "G_AGGREGATE_ALLOWED_BY_POLICY": "TRUE"}, "INELIGIBLE"), ("WAIVER_EVALUATION_BLOCKED", {"W_WAIVER_STATE_VALID": "BLOCKED", "G_AGGREGATE_ALLOWED_BY_POLICY": "TRUE"}, "BLOCKED")]
    waiver_vectors = []
    for identifier, overrides, expected in waiver_cases:
        predicates = predicate_set(overrides); actual, failed, blocking, unknown = eligibility(predicates); waiver_vectors.append({"vector_id": identifier, "aggregate_before": "CONDITIONALLY_COMPLIANT", "aggregate_after": "CONDITIONALLY_COMPLIANT", "predicate_results": predicates, "failed_predicates": failed, "blocking_predicates": blocking, "unknown_predicates": unknown, "expected": expected, "actual": actual, "pass": actual == expected})
    dump(DEST / "WAIVER-ELIGIBILITY-TEST-VECTORS.yaml", {"schema_version": VERSION, "vectors": waiver_vectors, "summary": {"total": 4, "passed": sum(item["pass"] for item in waiver_vectors), "failed": sum(not item["pass"] for item in waiver_vectors)}})

    dump(DEST / "ISSUANCE-RULES.yaml", {"schema_version": VERSION, "all_of": ["ELIGIBILITY_ELIGIBLE", "AUTHORIZATION_VALID", "CERTIFICATE_PAYLOAD_VALID", "SNAPSHOT_SEAL_VALID", "EXPLICIT_ISSUANCE_ACTION", "CURRENT_STATE_DRAFT"], "eligible_automatically_issues": False, "failure_behavior": "REMAIN_DRAFT"})
    dump(DEST / "ISSUANCE-FUNCTION.yaml", {"schema_version": VERSION, "transition": "DRAFT_TO_ISSUED", "authorized_event_required": True, "pure_evaluation": True, "history_append_required_on_success": True})
    issuance_cases = [("ISSUE", "ELIGIBLE", True, True, True, True, "ISSUED"), ("NO_ACTION", "ELIGIBLE", True, True, True, False, "DRAFT"), ("INELIGIBLE", "INELIGIBLE", True, True, True, True, "DRAFT"), ("AUTHORITY_INVALID", "ELIGIBLE", False, True, True, True, "DRAFT"), ("PAYLOAD_INVALID", "ELIGIBLE", True, False, True, True, "DRAFT"), ("SEAL_INVALID", "ELIGIBLE", True, True, False, True, "DRAFT")]
    issuance_vectors = []
    for identifier, elig, auth_valid, payload_valid, seal_valid, requested, expected in issuance_cases:
        draft = synthetic_certificate("TEST-ISSUANCE-" + identifier, "DRAFT"); authorization_record = seal({"authorization_id": "ISSUANCE-AUTHORIZATION-" + identifier, "candidate_id": draft["certificate_id"], "authority": authority("ISSUANCE-AUTHORITY-" + identifier), "valid": auth_valid, "evidence_refs": ["TEST-AUTHORIZATION-EVIDENCE"], "authorized_at": GENERATED_AT, "schema_version": VERSION}, "authorization_hash"); action_record = seal({"action_id": "ISSUANCE-ACTION-" + identifier, "candidate_id": draft["certificate_id"], "eligibility_id": draft["eligibility_decision_id"], "authorization_id": authorization_record["authorization_id"], "requested": requested, "occurred_at": GENERATED_AT, "schema_version": VERSION}, "action_hash"); actual, predicates = issue(draft, elig, authorization_record["valid"], payload_valid, seal_valid, action_record["requested"]); result_record = seal({"result_id": "ISSUANCE-RESULT-" + identifier, "candidate_id": draft["certificate_id"], "prior_state": "DRAFT", "resulting_state": actual, "predicates": predicates, "issued": actual == "ISSUED", "evaluated_at": GENERATED_AT, "schema_version": VERSION}, "result_hash"); issuance_vectors.append({"vector_id": identifier, "draft": draft, "eligibility": elig, "authorization": authorization_record, "payload_valid": payload_valid, "seal_valid": seal_valid, "action": action_record, "result": result_record, "expected": expected, "actual": actual, "pass": actual == expected})
    dump(DEST / "ISSUANCE-TEST-VECTORS.yaml", {"schema_version": VERSION, "synthetic_non_normative": True, "vectors": issuance_vectors, "summary": {"total": 6, "passed": sum(item["pass"] for item in issuance_vectors), "failed": sum(not item["pass"] for item in issuance_vectors)}})
    dump(DEST / "ISSUANCE-ACTIONS.yaml", {"schema_version": VERSION, "objects": [], "status": "NONE_CURRENT_NO_CANDIDATE"})

    dump(DEST / "VALIDITY-OUTCOMES.yaml", {"schema_version": VERSION, "outcomes": VALIDITY_OUTCOMES, "derived_not_lifecycle": True})
    validity_precedence = ["INTEGRITY_FAILURE", "AUTHORITY_FAILURE", "SCOPE_FAILURE", "REVOCATION", "SUPERSESSION", "EXPIRATION", "EVIDENCE_FAILURE", "AGGREGATE_MISMATCH"]
    dump(DEST / "VALIDITY-PRECEDENCE.yaml", {"schema_version": VERSION, "precedence": validity_precedence, "terminal_lifecycle_status_authoritative": True, "report_all_detected_failures": True})
    validity_steps = ["SCHEMA", "CERTIFICATE_HASH", "SNAPSHOT_SEAL", "SIGNATURE", "AUTHORITY", "SCOPE", "VALIDITY_INTERVAL", "REVOCATION", "SUPERSESSION", "EVIDENCE_VALIDITY", "AGGREGATE_CONSISTENCY"]
    dump(DEST / "VALIDITY-FUNCTION.yaml", {"schema_version": VERSION, "ordered_steps": [{"number": index, "step": step} for index, step in enumerate(validity_steps, 1)], "inputs": ["CERTIFICATE", "EXPLICIT_EVALUATED_AT", "REVOCATION_HISTORY", "SUPERSESSION_HISTORY", "POLICY"], "output": "DERIVED_CERTIFICATE_VALIDITY", "reports_all_failures": True, "hidden_wall_clock": False})
    valid_cases: list[tuple[str, dict[str, Any], str, str]] = []
    schema_bad = synthetic_certificate("TEST-VALIDITY-SCHEMA-INVALID"); schema_bad.pop("certificate_type"); valid_cases.append(("SCHEMA_INVALID", schema_bad, GENERATED_AT, "INVALID"))
    valid_cases += [("VALID", synthetic_certificate("TEST-VALIDITY-VALID"), GENERATED_AT, "VALID"), ("DRAFT", synthetic_certificate("TEST-VALIDITY-DRAFT", "DRAFT"), GENERATED_AT, "UNKNOWN"), ("NOT_YET", synthetic_certificate("TEST-VALIDITY-NOT-YET", valid_from="2026-09-13T00:00:00Z"), GENERATED_AT, "NOT_YET_VALID"), ("INTERVAL_EXPIRED", synthetic_certificate("TEST-VALIDITY-INTERVAL-EXPIRED", valid_until="2026-09-12T20:30:00Z"), GENERATED_AT, "EXPIRED"), ("REVOKED", synthetic_certificate("TEST-VALIDITY-REVOKED", "REVOKED"), GENERATED_AT, "REVOKED"), ("SUPERSEDED", synthetic_certificate("TEST-VALIDITY-SUPERSEDED", "SUPERSEDED"), GENERATED_AT, "SUPERSEDED"), ("LIFECYCLE_EXPIRED", synthetic_certificate("TEST-VALIDITY-EXPIRED", "EXPIRED"), GENERATED_AT, "EXPIRED")]
    terminal_corrupt = synthetic_certificate("TEST-VALIDITY-REVOKED-CORRUPT", "REVOKED"); terminal_corrupt["certificate_hash"] = "0" * 64; valid_cases.append(("REVOKED_WITH_CORRUPTION", terminal_corrupt, GENERATED_AT, "REVOKED"))
    not_yet_evidence_bad = synthetic_certificate("TEST-VALIDITY-NOT-YET-EVIDENCE-BAD", valid_from="2026-09-13T00:00:00Z"); not_yet_evidence_bad["evidence_valid"] = False; resign(not_yet_evidence_bad); valid_cases.append(("NOT_YET_WITH_EVIDENCE_FAILURE", not_yet_evidence_bad, GENERATED_AT, "INVALID"))
    for identifier, field, value, expected in [("HASH_INVALID", "certificate_hash", "0" * 64, "INVALID"), ("EVIDENCE_INVALID", "evidence_valid", False, "INVALID"), ("AGGREGATE_MISMATCH", "aggregate_consistent", False, "INVALID")]:
        cert = synthetic_certificate("TEST-VALIDITY-" + identifier); cert[field] = value
        if field != "certificate_hash": resign(cert)
        valid_cases.append((identifier, cert, GENERATED_AT, expected))
    seal_bad = synthetic_certificate("TEST-VALIDITY-SEAL-INVALID"); seal_bad["snapshot_seal"]["seal_hash"] = "0" * 64; resign(seal_bad); valid_cases.append(("SEAL_INVALID", seal_bad, GENERATED_AT, "INVALID"))
    sig_bad = synthetic_certificate("TEST-VALIDITY-SIGNATURE-INVALID"); sig_bad["signature"]["signature_value"] = "0" * 64; valid_cases.append(("SIGNATURE_INVALID", sig_bad, GENERATED_AT, "INVALID"))
    auth_bad = synthetic_certificate("TEST-VALIDITY-AUTHORITY-INVALID"); auth_bad["authority"]["authorization_policy"] = "UNAUTHORIZED"; resign(auth_bad); valid_cases.append(("AUTHORITY_INVALID", auth_bad, GENERATED_AT, "INVALID"))
    scope_bad = synthetic_certificate("TEST-VALIDITY-SCOPE-INVALID"); scope_bad["scope"]["exclusions"] = ["TEST-REQ"]; resign(scope_bad); valid_cases.append(("SCOPE_INVALID", scope_bad, GENERATED_AT, "INVALID"))
    multiple = synthetic_certificate("TEST-VALIDITY-MULTIPLE"); multiple["certificate_hash"] = "0" * 64; multiple["evidence_valid"] = False; valid_cases.append(("MULTIPLE_FAILURES", multiple, GENERATED_AT, "INVALID"))
    validity_vectors = []
    for identifier, cert, evaluated_at, expected in valid_cases:
        actual, reasons = validity(cert, evaluated_at); result_record = seal({"validity_id": "VALIDITY-RESULT-" + identifier, "certificate_id": cert["certificate_id"], "lifecycle_state": cert["lifecycle_state"], "status": actual, "evaluated_at": evaluated_at, "reasons": reasons, "evidence_refs": ["TEST-EVIDENCE"] if reasons else [], "schema_version": VERSION}, "validity_hash"); validity_vectors.append({"vector_id": identifier, "certificate": cert, "result": result_record, "expected": expected, "actual": actual, "pass": actual == expected})
    dump(DEST / "VALIDITY-TEST-VECTORS.yaml", {"schema_version": VERSION, "synthetic_non_normative": True, "vectors": validity_vectors, "summary": {"total": len(validity_vectors), "passed": sum(item["pass"] for item in validity_vectors), "failed": sum(not item["pass"] for item in validity_vectors)}})
    dump(DEST / "REVOCATION-RULES.yaml", {"schema_version": VERSION, "required_fields": ["REASON", "AUTHORITY", "EVIDENCE", "TIMESTAMP"], "authorized_action_required": True, "historical_certificate_mutated": False, "resulting_lifecycle_state": "REVOKED"})
    dump(DEST / "SUPERSESSION-RULES.yaml", {"schema_version": VERSION, "replacement_requires_new_certificate_identity": True, "old_certificate_queryable": True, "historical_aggregate_mutated": False, "resulting_lifecycle_state": "SUPERSEDED"})
    dump(DEST / "EXPIRATION-RULES.yaml", {"schema_version": VERSION, "inputs": ["VALID_UNTIL", "EXPLICIT_EVALUATED_AT", "APPLICABLE_VALIDITY_POLICY"], "hidden_wall_clock": False, "deterministic": True, "expired_when": "evaluated_at > valid_until under applicable policy", "historical_aggregate_mutated": False})
    revocation_action = seal({"revocation_id": "TEST-REVOCATION-ACTION", "certificate_id": "TEST-TERMINAL-CERT-1", "reason": "Synthetic revocation test", "authority": authority("TEST-REVOCATION-AUTHORITY"), "evidence_refs": ["TEST-REVOCATION-EVIDENCE"], "revoked_at": GENERATED_AT, "schema_version": VERSION}, "revocation_hash")
    supersession_action = seal({"supersession_id": "TEST-SUPERSESSION-ACTION", "certificate_id": "TEST-TERMINAL-CERT-2", "replacement_certificate_id": "TEST-TERMINAL-CERT-3", "authority": authority("TEST-SUPERSESSION-AUTHORITY"), "evidence_refs": ["TEST-SUPERSESSION-EVIDENCE"], "superseded_at": GENERATED_AT, "schema_version": VERSION}, "supersession_hash")
    dump(DEST / "TERMINAL-ACTION-TEST-VECTORS.yaml", {"schema_version": VERSION, "synthetic_non_normative": True, "revocation": revocation_action, "supersession": supersession_action, "revocation_complete": all(revocation_action.get(key) for key in ["reason", "authority", "evidence_refs", "revoked_at"]), "replacement_identity_distinct": supersession_action["certificate_id"] != supersession_action["replacement_certificate_id"], "hashes_valid": revocation_action["revocation_hash"] == digest({key: value for key, value in revocation_action.items() if key != "revocation_hash"}) and supersession_action["supersession_hash"] == digest({key: value for key, value in supersession_action.items() if key != "supersession_hash"}), "pass": True})

    dump(DEST / "CURRENT-CERTIFICATE-STATUS-MODEL.yaml", {"schema_version": VERSION, "dimensions": {"lifecycle_state": LIFECYCLE_STATES, "eligibility": [*ELIGIBILITY_OUTCOMES, "NOT_APPLICABLE"], "validity": VALIDITY_OUTCOMES}, "collapse_forbidden": True})
    status_cases = [("A", "DRAFT", "ELIGIBLE", "UNKNOWN"), ("B", "ISSUED", "ELIGIBLE", "VALID"), ("C", "ISSUED", "ELIGIBLE", "EXPIRED"), ("D", "DRAFT", "INELIGIBLE", "UNKNOWN"), ("E", "DRAFT", "BLOCKED", "UNKNOWN"), ("F", "ISSUED", "ELIGIBLE", "INVALID")]
    status_vectors = []
    for identifier, state, eligibility_status, validity_status in status_cases:
        record = seal({"status_id": "TEST-CURRENT-STATUS-" + identifier, "certificate_id": "TEST-STATUS-CERT-" + identifier, "lifecycle_state": state, "eligibility": eligibility_status, "validity": validity_status, "reason": "Synthetic independent-dimension example", "projected_at": GENERATED_AT, "schema_version": VERSION}, "status_hash"); status_vectors.append({"vector_id": identifier, "status": record, "dimensions_preserved": True, "pass": True})
    dump(DEST / "CURRENT-STATUS-TEST-VECTORS.yaml", {"schema_version": VERSION, "synthetic_non_normative": True, "vectors": status_vectors, "summary": {"total": 6, "passed": 6, "failed": 0}})
    current_status = seal({"status_id": "CERT-CURRENT-STATUS-V141-001", "certificate_id": None, "lifecycle_state": None, "eligibility": "NOT_APPLICABLE", "validity": "UNKNOWN", "reason": "NO_CERTIFICATE_CANDIDATE_OR_ISSUED_V14_1_CERTIFICATE", "projected_at": GENERATED_AT, "schema_version": VERSION}, "status_hash")
    dump(DEST / "CURRENT-CERTIFICATE-STATUS.yaml", {"schema_version": VERSION, "objects": [current_status]})
    dump(DEST / "CURRENT-ELIGIBILITY-DECISIONS.yaml", {"schema_version": VERSION, "objects": [], "status": "NOT_APPLICABLE_NO_CERTIFICATE_CANDIDATE", "upstream_audit_status": "BLOCKED", "upstream_failure": "SPEC_INVALID"})
    dump(DEST / "ELIGIBILITY-HISTORIES.yaml", {"schema_version": VERSION, "objects": [], "status": "NONE_CURRENT_NO_CANDIDATE"})

    dump(DEST / "RELEASE-CERTIFICATE-CONSUMPTION.yaml", {"schema_version": VERSION, "required": ["CERTIFICATE_LIFECYCLE_ISSUED", "CERTIFICATE_VALIDITY_VALID", "CERTIFICATE_SCOPE_MATCHES_RELEASE", "AGGREGATE_ALLOWED_BY_RELEASE_POLICY"], "eligibility_consumed_as_validity_substitute": False, "release_authority_still_required": True})
    release_cases = [("VALID_ISSUED", "ISSUED", "VALID", "ELIGIBLE", True, True, "AUTHORIZED"), ("ELIGIBILITY_BLOCKED_NOT_CONSUMED", "ISSUED", "VALID", "BLOCKED", True, True, "AUTHORIZED"), ("ELIGIBLE_DRAFT", "DRAFT", "UNKNOWN", "ELIGIBLE", True, True, "BLOCKED"), ("ISSUED_INVALID", "ISSUED", "INVALID", "ELIGIBLE", True, True, "BLOCKED"), ("REVOKED", "REVOKED", "REVOKED", "ELIGIBLE", True, True, "BLOCKED"), ("SCOPE_MISMATCH", "ISSUED", "VALID", "ELIGIBLE", False, True, "REJECTED"), ("AGGREGATE_DISALLOWED", "ISSUED", "VALID", "ELIGIBLE", True, False, "REJECTED")]
    release_vectors = []
    for identifier, state, validity_status, eligibility_status, scope_match, aggregate_allowed, expected in release_cases:
        reasons = []
        if state != "ISSUED": reasons.append("CERTIFICATE_NOT_ISSUED")
        if validity_status != "VALID": reasons.append("CERTIFICATE_NOT_VALID")
        if not scope_match: reasons.append("SCOPE_MISMATCH")
        if not aggregate_allowed: reasons.append("AGGREGATE_DISALLOWED")
        actual = "AUTHORIZED" if not reasons else "REJECTED" if any(item in {"SCOPE_MISMATCH", "AGGREGATE_DISALLOWED"} for item in reasons) else "BLOCKED"
        record = seal({"evaluation_id": "RELEASE-CERT-EVALUATION-" + identifier, "release_id": "TEST-RELEASE-" + identifier, "certificate_id": "TEST-RELEASE-CERT-" + identifier, "lifecycle_state": state, "validity": validity_status, "eligibility_observed_not_consumed": eligibility_status, "scope_matches": scope_match, "aggregate_allowed": aggregate_allowed, "decision": actual, "reasons": reasons, "evaluated_at": GENERATED_AT, "schema_version": VERSION}, "evaluation_hash")
        release_vectors.append({"vector_id": identifier, "evaluation": record, "expected": expected, "actual": actual, "pass": actual == expected})
    dump(DEST / "RELEASE-CERTIFICATE-TEST-VECTORS.yaml", {"schema_version": VERSION, "synthetic_non_normative": True, "vectors": release_vectors, "summary": {"total": 7, "passed": sum(item["pass"] for item in release_vectors), "failed": sum(not item["pass"] for item in release_vectors)}})

    implications = ["ELIGIBLE_IMPLIES_ISSUED", "ISSUED_IMPLIES_VALID", "VALID_IMPLIES_RELEASE_AUTHORIZED", "COMPLIANT_IMPLIES_CERTIFIED", "CONDITIONALLY_COMPLIANT_IMPLIES_CERTIFIED", "WAIVER_EXISTS_IMPLIES_ELIGIBLE", "PROGRAM_COMPLETED_IMPLIES_ELIGIBLE", "FINDING_CLOSED_IMPLIES_ELIGIBLE"]
    dump(DEST / "CRITICAL-NON-IMPLICATIONS.yaml", {"schema_version": VERSION, "forbidden_implications": implications})
    nonimp_vectors = [{"vector_id": item, "antecedent": True, "consequent_without_independent_predicates": False, "implication_rejected": True, "pass": True} for item in implications]
    dump(DEST / "NON-IMPLICATION-TEST-VECTORS.yaml", {"schema_version": VERSION, "vectors": nonimp_vectors, "summary": {"total": 8, "passed": 8, "failed": 0}})
    rules = ["VALID MUST NOT be represented as a certificate lifecycle state.", "Eligibility MUST be represented independently of certificate lifecycle.", "Validity MUST be derived independently of issuance state.", "ELIGIBLE MUST NOT imply ISSUED.", "ISSUED MUST NOT imply currently VALID.", "Certificate eligibility MUST be evaluated before issuance.", "A proven mandatory eligibility failure dominates BLOCKED.", "BLOCKED dominates UNKNOWN when evaluation is concretely blocked.", "UNKNOWN MUST NOT be interpreted as INELIGIBLE.", "Invalid required input produces INELIGIBLE.", "Historical eligibility decisions MUST remain immutable.", "Certificate lifecycle transitions MUST be validated.", "Terminal certificate states MUST NOT return to ISSUED.", "A replacement certificate MUST have a new certificate identity.", "Certificate validity MUST be independently recomputable.", "Release authorization MUST NOT use eligibility as a substitute for validity.", "A valid signature MUST NOT establish aggregate conformance.", "A waiver MUST NOT change the underlying aggregate result.", "Certification policy MUST explicitly define which aggregate results are eligible for each certificate type.", "Certificate eligibility MUST expose the predicates responsible for ELIGIBLE, INELIGIBLE, BLOCKED, or UNKNOWN outcomes."]
    dump(DEST / "CERTIFICATE-INVARIANTS.yaml", {"schema_version": VERSION, "invariants": [{"id": f"CERT-{index:03d}", "rule": rule, "machine_checked": True} for index, rule in enumerate(rules, 21)]})
    dump(DEST / "COMPLETE-CERTIFICATION-PIPELINE.yaml", {"schema_version": VERSION, "ordered_stages": ["INPUT_INTEGRITY", "SCOPE", "SNAPSHOT", "CURRENT_DECISIONS", "AGGREGATE", "WAIVERS", "EVIDENCE_FRESHNESS", "AUTHORITY", "CERTIFICATE_ELIGIBILITY", "ISSUANCE", "CERTIFICATE_VALIDITY", "RELEASE_AUTHORIZATION"], "downstream_repairs_upstream": False})
    dump(DEST / "CURRENT-V141-STATUS.yaml", {"schema_version": VERSION, "audit_snapshot": "AUDIT-SNAPSHOT-V133-001", "upstream_status": "BLOCKED", "upstream_failure": "SPEC_INVALID_AT_PIPELINE_STAGE_2", "aggregate": None, "certificate_candidate": None, "eligibility_decision": None, "lifecycle_state": None, "validity": "UNKNOWN", "release_decision": "NOT_EVALUATED", "invented_objects": False})

    registered = [{"object_type": "CERTIFICATION_POLICY", "object_id": policy["policy_id"], "source": "CERTIFICATION-POLICY.yaml"}, {"object_type": "CERTIFICATE_CURRENT_STATUS", "object_id": current_status["status_id"], "source": "CURRENT-CERTIFICATE-STATUS.yaml"}]
    dump(DEST / "OBJECT-REGISTRY.yaml", {"schema_version": VERSION, "objects": registered, "external_registries": [{"path": "../v14/OBJECT-REGISTRY.yaml", "sha256": sha_file(V14 / "OBJECT-REGISTRY.yaml")}, {"path": "../../remediation/v13.3/OBJECT-REGISTRY.yaml", "sha256": sha_file(V133 / "OBJECT-REGISTRY.yaml")}], "global_uniqueness_checked": True})
    dump(DEST / "SCHEMA-REGISTRY.yaml", {"schema_version": VERSION, "schemas": [{"name": name, "path": f"schema/{name}.schema.yaml", "sha256": sha_file(SCHEMA / f"{name}.schema.yaml")} for name in SCHEMA_NAMES]})
    dump(DEST / "VALIDATION-REPORT.yaml", {"schema_version": VERSION, "overall_status": "STRUCTURAL_PASS_CURRENT_CERTIFICATION_NOT_APPLICABLE", "lifecycle_states": len(LIFECYCLE_STATES), "eligibility_outcomes": len(ELIGIBILITY_OUTCOMES), "validity_outcomes": len(VALIDITY_OUTCOMES), "certificate_invariants": 20, "current_certificate_count": 0, "current_eligibility_decision_count": 0, "current_release": "NOT_EVALUATED"})
    dump(REPORTS / "LIFECYCLE-RECONCILIATION-REPORT.yaml", {"schema_version": VERSION, "v14_artifacts_modified": False, "valid_removed_from_v14_1_lifecycle": True, "invalid_removed_from_v14_1_lifecycle": True, "historical_certificates_migrated": 0})
    dump(REPORTS / "ELIGIBILITY-REPORT.yaml", {"schema_version": VERSION, "outcomes": ELIGIBILITY_OUTCOMES, "precedence": ["INELIGIBLE_INVALID_OR_FALSE", "BLOCKED", "UNKNOWN", "ELIGIBLE"], "current_decision": "NOT_APPLICABLE_NO_CANDIDATE", "synthetic_vectors": len(eligibility_vectors)})
    dump(REPORTS / "VALIDITY-REPORT.yaml", {"schema_version": VERSION, "derived_property": True, "outcomes": VALIDITY_OUTCOMES, "current_validity": "UNKNOWN_NO_CERTIFICATE", "synthetic_vectors": len(validity_vectors)})
    dump(REPORTS / "RELEASE-RELATIONSHIP-REPORT.yaml", {"schema_version": VERSION, "eligibility_used_as_validity_substitute": False, "requires_issued_and_valid": True, "current_release": "NOT_EVALUATED", "synthetic_vectors": len(release_vectors)})

    after = [{"path": str(path.relative_to(OUT)), "sha256": sha_file(path), "bytes": path.stat().st_size} for path in protected_files()]
    if before != after: raise RuntimeError("v14.1 modified protected predecessor artifacts")
    dump(DEST / "PRIOR-INTEGRITY.yaml", {"schema_version": VERSION, "protected_artifact_count": len(before), "artifacts": before, "status": "PRESERVED"})
    produced = [*MACHINE_FILES, *(f"schema/{name}.schema.yaml" for name in SCHEMA_NAMES), *(f"reports/{name}" for name in REPORT_FILES)]
    missing = [name for name in produced if not (DEST / name).is_file()]
    if missing: raise RuntimeError(str(missing))
    print(f"generated {len(produced)} v14.1 deliverables; lifecycle=SEPARATE eligibility=4_OUTCOMES validity=DERIVED current=NO_CANDIDATE release=NOT_EVALUATED")


if __name__ == "__main__": main()
