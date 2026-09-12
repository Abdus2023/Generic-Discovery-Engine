#!/usr/bin/env python3
"""Independent validator for Protocol-v14.1 certificate-state reconciliation."""
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
V14 = OUT / "certification" / "v14"
DEST = OUT / "certification" / "v14.1"
SCHEMA = DEST / "schema"
VERSION = "14.1"
LIFECYCLE_STATES = ["DRAFT", "ISSUED", "SUPERSEDED", "REVOKED", "EXPIRED"]
ELIGIBILITY_OUTCOMES = ["ELIGIBLE", "INELIGIBLE", "BLOCKED", "UNKNOWN"]
PREDICATE_OUTCOMES = ["TRUE", "FALSE", "BLOCKED", "UNKNOWN"]
VALIDITY_OUTCOMES = ["VALID", "INVALID", "NOT_YET_VALID", "EXPIRED", "REVOKED", "SUPERSEDED", "UNKNOWN"]
PREDICATES = ["S_SCOPE_VALID", "P_SPECIFICATION_SNAPSHOT_VALID", "I_IMPLEMENTATION_SNAPSHOT_VALID", "D_CURRENT_DECISIONS_VALID", "H_LIFECYCLE_HISTORY_VALID", "E_REQUIRED_EVIDENCE_VALID", "T_TRACEABILITY_VALID", "A_AGGREGATE_VALID", "W_WAIVER_STATE_VALID", "U_CERTIFICATION_AUTHORITY_VALID", "F_EVIDENCE_FRESHNESS_VALID", "G_AGGREGATE_ALLOWED_BY_POLICY"]
SCHEMA_NAMES = ["certificate-scope", "certification-authority", "snapshot-seal", "certificate-signature", "certificate", "certificate-lifecycle-transition", "certificate-lifecycle-history", "eligibility-predicate-result", "certificate-eligibility-decision", "eligibility-history", "certificate-type-rule", "certification-policy", "issuance-authorization", "issuance-action", "issuance-result", "certificate-validity-result", "certificate-current-status", "revocation-action", "supersession-action", "release-certificate-evaluation", "eligibility-evaluation-input"]
MACHINE_FILES = ["MODEL-SEPARATION.yaml", "V14-RECONCILIATION.yaml", "CERTIFICATE-LIFECYCLE-STATES.yaml", "CERTIFICATE-STATE-MACHINE.yaml", "CERTIFICATE-TRANSITION-MATRIX.yaml", "CERTIFICATE-LIFECYCLE-TEST-VECTORS.yaml", "CERTIFICATE-HISTORY-PROJECTION-FUNCTION.yaml", "CERTIFICATE-HISTORY-TEST-VECTORS.yaml", "CERTIFICATE-HISTORIES.yaml", "CERTIFICATES-V141.yaml", "ELIGIBILITY-OUTCOMES.yaml", "ELIGIBILITY-PREDICATES.yaml", "ELIGIBILITY-PRECEDENCE.yaml", "ELIGIBILITY-FUNCTION.yaml", "ELIGIBILITY-TEST-VECTORS.yaml", "ELIGIBILITY-HISTORY-TEST-VECTORS.yaml", "CERTIFICATION-POLICY.yaml", "CERTIFICATE-TYPE-MAPPING-TEST-VECTORS.yaml", "WAIVER-ELIGIBILITY-TEST-VECTORS.yaml", "ISSUANCE-RULES.yaml", "ISSUANCE-FUNCTION.yaml", "ISSUANCE-TEST-VECTORS.yaml", "ISSUANCE-ACTIONS.yaml", "VALIDITY-OUTCOMES.yaml", "VALIDITY-PRECEDENCE.yaml", "VALIDITY-FUNCTION.yaml", "VALIDITY-TEST-VECTORS.yaml", "REVOCATION-RULES.yaml", "SUPERSESSION-RULES.yaml", "EXPIRATION-RULES.yaml", "TERMINAL-ACTION-TEST-VECTORS.yaml", "CURRENT-CERTIFICATE-STATUS-MODEL.yaml", "CURRENT-STATUS-TEST-VECTORS.yaml", "CURRENT-CERTIFICATE-STATUS.yaml", "CURRENT-ELIGIBILITY-DECISIONS.yaml", "ELIGIBILITY-HISTORIES.yaml", "RELEASE-CERTIFICATE-CONSUMPTION.yaml", "RELEASE-CERTIFICATE-TEST-VECTORS.yaml", "CRITICAL-NON-IMPLICATIONS.yaml", "NON-IMPLICATION-TEST-VECTORS.yaml", "CERTIFICATE-INVARIANTS.yaml", "COMPLETE-CERTIFICATION-PIPELINE.yaml", "CURRENT-V141-STATUS.yaml", "OBJECT-REGISTRY.yaml", "SCHEMA-REGISTRY.yaml", "PRIOR-INTEGRITY.yaml", "VALIDATION-REPORT.yaml"]
REPORT_FILES = ["LIFECYCLE-RECONCILIATION-REPORT.yaml", "ELIGIBILITY-REPORT.yaml", "VALIDITY-REPORT.yaml", "RELEASE-RELATIONSHIP-REPORT.yaml"]
DELIVERABLES = [*MACHINE_FILES, *(f"schema/{name}.schema.yaml" for name in SCHEMA_NAMES), *(f"reports/{name}" for name in REPORT_FILES)]


def load(path: Path) -> Any: return json.loads(path.read_text(encoding="utf-8"))
def canonical(value: Any) -> bytes: return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
def digest(value: Any) -> str: return hashlib.sha256(canonical(value)).hexdigest()
def sha_file(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()
def certificate_hash(value: dict[str, Any]) -> str: return digest({key: item for key, item in value.items() if key not in {"certificate_hash", "signature"}})
def signature_value(hash_value: str, authority_id: str, signed_at: str) -> str: return digest({"certificate_hash": hash_value, "authority_id": authority_id, "signed_at": signed_at})
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
        valid = {"object": isinstance(value, dict), "array": isinstance(value, list), "string": isinstance(value, str), "integer": isinstance(value, int) and not isinstance(value, bool), "boolean": isinstance(value, bool), "null": value is None}
        if not valid.get(expected, False): return [f"{path}: type"]
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
        if "items" in body:
            for index, item in enumerate(value): errors.extend(schema_errors(item, body["items"], schemas, f"{path}[{index}]"))
    if isinstance(value, dict):
        properties = body.get("properties", {})
        for key in body.get("required", []):
            if key not in value: errors.append(f"{path}: missing {key}")
        if body.get("additionalProperties") is False: errors.extend(f"{path}: additional {key}" for key in value if key not in properties)
        for key, item in value.items():
            if key in properties: errors.extend(schema_errors(item, properties[key], schemas, f"{path}.{key}"))
    return errors


def eligibility(predicate_results: list[dict[str, Any]], invalid_required_input: bool = False) -> tuple[str, list[str], list[str], list[str]]:
    grouped = {name: [item["predicate_id"] for item in predicate_results if item["result"] == name] for name in PREDICATE_OUTCOMES}
    if invalid_required_input or grouped["FALSE"]: outcome = "INELIGIBLE"
    elif grouped["BLOCKED"]: outcome = "BLOCKED"
    elif grouped["UNKNOWN"]: outcome = "UNKNOWN"
    else: outcome = "ELIGIBLE"
    return outcome, (["INVALID_REQUIRED_INPUT"] if invalid_required_input else []) + grouped["FALSE"], grouped["BLOCKED"], grouped["UNKNOWN"]


def transition_allowed(source: str, target: str) -> bool:
    return (source, target) in {("DRAFT", "ISSUED"), ("DRAFT", "SUPERSEDED"), ("DRAFT", "REVOKED"), ("ISSUED", "SUPERSEDED"), ("ISSUED", "REVOKED"), ("ISSUED", "EXPIRED")}


def project_history(events: list[dict[str, Any]]) -> tuple[str, str | None]:
    if not events: return "HISTORY_INVALID", None
    state = None
    for index, event in enumerate(events):
        if event.get("sequence") != index or event.get("from_state") != state or event.get("transition_hash") != digest({key: value for key, value in event.items() if key != "transition_hash"}): return "HISTORY_INVALID", None
        if index == 0:
            if event.get("to_state") != "DRAFT" or event.get("action") != "CREATE_DRAFT": return "HISTORY_INVALID", None
        else:
            expected_action = {"ISSUED": "ISSUE", "SUPERSEDED": "SUPERSEDE", "REVOKED": "REVOKE", "EXPIRED": "EXPIRE"}.get(event.get("to_state"))
            if not transition_allowed(state or "", event.get("to_state", "")) or event.get("action") != expected_action: return "HISTORY_INVALID", None
            if event.get("action") in {"ISSUE", "SUPERSEDE", "REVOKE"} and (not event.get("reason") or not event.get("authority", {}).get("authorization_evidence") or not event.get("evidence_refs")): return "HISTORY_INVALID", None
        state = event["to_state"]
    return "VALID", state


def issue(draft: dict[str, Any], eligibility_outcome: str, authorization_valid: bool, payload_valid: bool, seal_valid: bool, action_requested: bool) -> tuple[str, dict[str, bool]]:
    predicates = {"ELIGIBILITY_VALID": eligibility_outcome == "ELIGIBLE", "AUTHORIZATION_VALID": authorization_valid, "PAYLOAD_VALID": payload_valid, "SNAPSHOT_SEAL_VALID": seal_valid, "ACTION_REQUESTED": action_requested, "DRAFT_STATE_VALID": draft.get("lifecycle_state") == "DRAFT"}
    return ("ISSUED" if all(predicates.values()) else "DRAFT"), predicates


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
    if any(item in {"SCHEMA_INVALID", "CERTIFICATE_HASH_INVALID", "SNAPSHOT_SEAL_INVALID", "SIGNATURE_INVALID", "AUTHORITY_INVALID", "SCOPE_INVALID"} for item in failures): return "INVALID", failures
    if "NOT_YET_VALID" in failures and failures == ["NOT_YET_VALID"]: return "NOT_YET_VALID", failures
    if "VALIDITY_INTERVAL_EXPIRED" in failures: return "EXPIRED", failures
    if "EVIDENCE_INVALID" in failures or "AGGREGATE_MISMATCH" in failures or "NOT_YET_VALID" in failures: return "INVALID", failures
    return "VALID", []


def main() -> int:
    checks: list[dict[str, str]] = []
    def check(identifier: str, category: str, description: str, condition: bool, detail: str = "") -> None: checks.append({"check_id": identifier, "category": category, "result": "PASS" if condition else "FAIL", "description": description, "detail": detail})
    def blocked(identifier: str, category: str, description: str, detail: str) -> None: checks.append({"check_id": identifier, "category": category, "result": "BLOCKED", "description": description, "detail": detail})

    check("I01", "inventory", "all 72 generator-owned v14.1 deliverables exist", len(DELIVERABLES) == 72 and all((DEST / path).is_file() for path in DELIVERABLES))
    parse_errors = []
    for path in sorted(DEST.rglob("*.yaml")):
        try: load(path)
        except Exception as exc: parse_errors.append(f"{path.relative_to(DEST)}:{exc}")
    check("I02", "syntax", "all v14.1 YAML is JSON-compatible and parseable", not parse_errors, str(parse_errors[:10]))
    schemas = {name: load(SCHEMA / f"{name}.schema.yaml") for name in SCHEMA_NAMES}; schema_ids = [item.get("$id") for item in schemas.values()]
    check("S01", "schemas", "all 21 schemas have unique stable IDs", len(schemas) == len(schema_ids) == len(set(schema_ids)) == 21 and all(schema_ids))
    check("S02", "schemas", "all object schemas reject undeclared fields", all(item.get("additionalProperties") is False for item in schemas.values()))
    schema_registry = load(DEST / "SCHEMA-REGISTRY.yaml"); schema_reg_errors = [item["name"] for item in schema_registry["schemas"] if item["name"] not in schemas or sha_file(DEST / item["path"]) != item["sha256"]]
    check("S03", "schemas", "schema registry resolves all 21 schemas with exact hashes", len(schema_registry["schemas"]) == 21 and not schema_reg_errors, str(schema_reg_errors))

    instances: list[tuple[str, dict[str, Any], str]] = []
    policy = load(DEST / "CERTIFICATION-POLICY.yaml")["objects"][0]; instances.append(("certification-policy", policy, policy["policy_id"]))
    for rule in policy["certificate_types"]: instances.append(("certificate-type-rule", rule, rule["certificate_type"]))
    eligibility_vectors = load(DEST / "ELIGIBILITY-TEST-VECTORS.yaml")
    for item in eligibility_vectors["vectors"]: instances += [("eligibility-evaluation-input", item["input"], item["vector_id"]), ("certificate-eligibility-decision", item["decision"], item["vector_id"])]
    eligibility_history = load(DEST / "ELIGIBILITY-HISTORY-TEST-VECTORS.yaml")["history"]; instances.append(("eligibility-history", eligibility_history, "ELIGIBILITY-HISTORY"))
    history_vectors = load(DEST / "CERTIFICATE-HISTORY-TEST-VECTORS.yaml")
    for item in history_vectors["vectors"]:
        instances.append(("certificate-lifecycle-history", item["history"], item["vector_id"]))
        instances += [("certificate-lifecycle-transition", event, item["vector_id"]) for event in item["events"]]
    issuance_vectors = load(DEST / "ISSUANCE-TEST-VECTORS.yaml")
    for item in issuance_vectors["vectors"]: instances += [("certificate", item["draft"], item["vector_id"]), ("issuance-authorization", item["authorization"], item["vector_id"]), ("issuance-action", item["action"], item["vector_id"]), ("issuance-result", item["result"], item["vector_id"])]
    validity_vectors = load(DEST / "VALIDITY-TEST-VECTORS.yaml")
    for item in validity_vectors["vectors"]:
        if item["vector_id"] != "SCHEMA_INVALID": instances.append(("certificate", item["certificate"], item["vector_id"]))
        instances.append(("certificate-validity-result", item["result"], item["vector_id"]))
    status_vectors = load(DEST / "CURRENT-STATUS-TEST-VECTORS.yaml")
    for item in status_vectors["vectors"]: instances.append(("certificate-current-status", item["status"], item["vector_id"]))
    current_status = load(DEST / "CURRENT-CERTIFICATE-STATUS.yaml")["objects"][0]; instances.append(("certificate-current-status", current_status, current_status["status_id"]))
    release_vectors = load(DEST / "RELEASE-CERTIFICATE-TEST-VECTORS.yaml")
    for item in release_vectors["vectors"]: instances.append(("release-certificate-evaluation", item["evaluation"], item["vector_id"]))
    terminal_actions = load(DEST / "TERMINAL-ACTION-TEST-VECTORS.yaml"); instances += [("revocation-action", terminal_actions["revocation"], "TERMINAL-REVOCATION"), ("supersession-action", terminal_actions["supersession"], "TERMINAL-SUPERSESSION")]
    schema_instance_errors = []
    for name, value, label in instances: schema_instance_errors += [f"{label}:{error}" for error in schema_errors(value, schemas[name], schemas)]
    check("S04", "schemas", "all applicable production and synthetic objects satisfy schemas", not schema_instance_errors, str(schema_instance_errors[:20]))

    separation = load(DEST / "MODEL-SEPARATION.yaml")
    check("M01", "separation", "lifecycle, eligibility, validity, and release are independent", separation["independent_dimensions"] == ["CERTIFICATE_LIFECYCLE", "CERTIFICATE_ELIGIBILITY", "CERTIFICATE_VALIDITY", "RELEASE_DECISION"] and len(separation["non_equivalence"]) == 3)
    reconciliation = load(DEST / "V14-RECONCILIATION.yaml")
    check("M02", "reconciliation", "v14 is preserved while VALID and INVALID move to derived validity", reconciliation["predecessor_artifacts_mutated"] is False and reconciliation["existing_v14_certificates_to_migrate"] == 0 and reconciliation["existing_v14_lifecycle_events_to_migrate"] == 0 and {item["v14_construct"] for item in reconciliation["corrections"]} == {"VALID_AS_CERTIFICATE_STATE", "INVALID_AS_CERTIFICATE_STATE"})
    lifecycle = load(DEST / "CERTIFICATE-LIFECYCLE-STATES.yaml")
    check("M03", "lifecycle", "normative lifecycle contains exactly five states and excludes validity terms", lifecycle["states"] == LIFECYCLE_STATES and "VALID" not in lifecycle["states"] and "INVALID" not in lifecycle["states"])

    machine = load(DEST / "CERTIFICATE-STATE-MACHINE.yaml"); legal = {(item["from"], item["to"]) for item in machine["allowed_transitions"]}
    expected_legal = {("DRAFT", "ISSUED"), ("DRAFT", "SUPERSEDED"), ("DRAFT", "REVOKED"), ("ISSUED", "SUPERSEDED"), ("ISSUED", "REVOKED"), ("ISSUED", "EXPIRED")}
    check("T01", "state-machine", "six permitted lifecycle transitions are exact", legal == expected_legal and machine["invalid_is_derived_not_transition"] is True)
    check("T02", "state-machine", "all terminal states prohibit outgoing transitions", machine["terminal_states"] == ["SUPERSEDED", "REVOKED", "EXPIRED"] and machine["terminal_outgoing_transitions"] == [] and all(source not in set(machine["terminal_states"]) for source, _ in legal))
    matrix = load(DEST / "CERTIFICATE-TRANSITION-MATRIX.yaml")
    check("T03", "state-machine", "complete 5x5 transition matrix reproduces", matrix["complete_pair_count"] == len(matrix["matrix"]) == 25 and all(item["allowed"] == transition_allowed(item["from"], item["to"]) for item in matrix["matrix"]))
    lifecycle_vectors = load(DEST / "CERTIFICATE-LIFECYCLE-TEST-VECTORS.yaml")
    check("T04", "test-vectors", "all 25 lifecycle transition vectors reproduce", lifecycle_vectors["summary"] == {"total": 25, "passed": 25, "failed": 0} and all(item["actual"] == transition_allowed(item["from"], item["to"]) and item["pass"] for item in lifecycle_vectors["vectors"]))
    history_errors = []
    for item in history_vectors["vectors"]:
        result, state = project_history(item["events"]); history_record = item["history"]
        if result != item["expected"] or result != item["actual"] or state != item["expected_state"] or state != item["actual_state"] or history_record["history_hash"] != digest({key: value for key, value in history_record.items() if key != "history_hash"}) or history_record["transitions"] != item["events"] or not item["pass"]: history_errors.append(item["vector_id"])
    check("T05", "history", "all lifecycle history projections reproduce without skipping malformed events", history_vectors["summary"] == {"total": 5, "passed": 5, "failed": 0} and not history_errors, str(history_errors))
    check("T06", "revocation", "revocation requires reason, authority, evidence, and timestamp", load(DEST / "REVOCATION-RULES.yaml")["required_fields"] == ["REASON", "AUTHORITY", "EVIDENCE", "TIMESTAMP"] and all(all(event.get(key) for key in ["reason", "authority", "evidence_refs", "occurred_at"]) for item in history_vectors["vectors"] for event in item["events"] if event["action"] == "REVOKE"))
    check("T07", "supersession", "replacement requires new identity and preserves old certificate", load(DEST / "SUPERSESSION-RULES.yaml")["replacement_requires_new_certificate_identity"] is True and load(DEST / "SUPERSESSION-RULES.yaml")["old_certificate_queryable"] is True)
    expiration_rules = load(DEST / "EXPIRATION-RULES.yaml")
    check("T08", "expiration", "expiration derives deterministically from valid-until, policy, and explicit evaluation time", expiration_rules["inputs"] == ["VALID_UNTIL", "EXPLICIT_EVALUATED_AT", "APPLICABLE_VALIDITY_POLICY"] and expiration_rules["deterministic"] is True and expiration_rules["hidden_wall_clock"] is False)
    check("T09", "terminal-actions", "revocation completeness and supersession identity are executable", terminal_actions["revocation_complete"] and terminal_actions["replacement_identity_distinct"] and terminal_actions["hashes_valid"] and terminal_actions["pass"])

    eligibility_outcomes = load(DEST / "ELIGIBILITY-OUTCOMES.yaml")
    check("E01", "eligibility", "exact four eligibility outcomes retain blocked/unknown distinction", eligibility_outcomes["outcomes"] == ELIGIBILITY_OUTCOMES and eligibility_outcomes["definitions"]["BLOCKED"] != eligibility_outcomes["definitions"]["UNKNOWN"])
    predicate_model = load(DEST / "ELIGIBILITY-PREDICATES.yaml")
    check("E02", "eligibility", "all twelve mandatory predicates expose four predicate outcomes", [item["id"] for item in predicate_model["predicates"]] == PREDICATES and all(item["mandatory"] for item in predicate_model["predicates"]) and predicate_model["predicate_outcomes"] == PREDICATE_OUTCOMES)
    precedence = load(DEST / "ELIGIBILITY-PRECEDENCE.yaml")
    check("E03", "precedence", "invalid/false dominates blocked and blocked dominates unknown", precedence["precedence"] == ["INVALID_REQUIRED_INPUT", "PROVEN_INELIGIBILITY", "BLOCKED", "UNKNOWN", "ELIGIBLE"] and precedence["proven_failure_dominates_blocker"] and precedence["blocked_dominates_unknown"])
    eligibility_errors = []; eligibility_hash_errors = []
    for item in eligibility_vectors["vectors"]:
        source = item["input"]; actual, failed, blocking, unknown = eligibility(source["predicate_results"], source["invalid_required_input"]); decision = item["decision"]
        if actual != item["expected"] or actual != item["actual"] or decision["outcome"] != actual or decision["failed_predicates"] != failed or decision["blocking_predicates"] != blocking or decision["unknown_predicates"] != unknown or decision["snapshot_hash"] != source["snapshot_hash"] or decision["aggregate_status"] != source["aggregate_status"] or not item["pass"]: eligibility_errors.append(item["vector_id"])
        if source["input_hash"] != digest({key: value for key, value in source.items() if key != "input_hash"}) or decision["decision_hash"] != digest({key: value for key, value in decision.items() if key != "decision_hash"}): eligibility_hash_errors.append(item["vector_id"])
    check("E04", "test-vectors", "all nine deterministic eligibility vectors reproduce", eligibility_vectors["summary"] == {"total": 9, "passed": 9, "failed": 0} and not eligibility_errors, str(eligibility_errors))
    check("E05", "hashes", "eligibility inputs and immutable decisions have canonical hashes", not eligibility_hash_errors, str(eligibility_hash_errors))
    vector_by_id = {item["vector_id"]: item for item in eligibility_vectors["vectors"]}
    check("E06", "precedence", "proven ineligibility dominates blocked mechanically", vector_by_id["FALSE_DOMINATES_BLOCKED"]["actual"] == "INELIGIBLE")
    check("E07", "precedence", "blocked dominates semantic unknown mechanically", vector_by_id["BLOCKED_DOMINATES_UNKNOWN"]["actual"] == "BLOCKED")
    check("E08", "unknown", "unknown remains UNKNOWN rather than INELIGIBLE", vector_by_id["UNKNOWN_ONLY"]["actual"] == "UNKNOWN")
    history_decisions = eligibility_history["decisions"]
    history_valid = eligibility_history["history_hash"] == digest({key: value for key, value in eligibility_history.items() if key != "history_hash"}) and all(item["decision_hash"] == digest({key: value for key, value in item.items() if key != "decision_hash"}) for item in history_decisions)
    history_fixture = load(DEST / "ELIGIBILITY-HISTORY-TEST-VECTORS.yaml")
    check("E09", "history", "INELIGIBLE→BLOCKED→ELIGIBLE remains three immutable decisions", history_fixture["actual_outcomes"] == history_fixture["expected_outcomes"] == ["INELIGIBLE", "BLOCKED", "ELIGIBLE"] and history_fixture["immutable_distinct_decisions"] and history_fixture["changed_snapshot_new_decision"] and history_valid)
    check("E10", "policy", "certification policy hash and precedence reproduce", policy["policy_hash"] == digest({key: value for key, value in policy.items() if key != "policy_hash"}) and policy["precedence"] == precedence["precedence"])
    mapping_vectors = load(DEST / "CERTIFICATE-TYPE-MAPPING-TEST-VECTORS.yaml"); mapping_errors = []
    for item in mapping_vectors["vectors"]:
        rule = next(rule for rule in policy["certificate_types"] if rule["certificate_type"] == item["certificate_type"]); actual = item["aggregate_status"] in rule["allowed_aggregate_results"]
        if actual != item["expected_allowed"] or actual != item["actual_allowed"] or item["aggregate_after_evaluation"] != item["aggregate_status"] or not item["pass"]: mapping_errors.append(item["vector_id"])
    check("E11", "policy", "certificate type explicitly maps to aggregate without changing aggregate truth", len(policy["certificate_types"]) == 4 and mapping_vectors["summary"] == {"total": 6, "passed": 6, "failed": 0} and not mapping_errors, str(mapping_errors))
    waiver_vectors = load(DEST / "WAIVER-ELIGIBILITY-TEST-VECTORS.yaml"); waiver_errors = []
    for item in waiver_vectors["vectors"]:
        actual, failed, blocking, unknown = eligibility(item["predicate_results"])
        if actual != item["expected"] or actual != item["actual"] or failed != item["failed_predicates"] or blocking != item["blocking_predicates"] or unknown != item["unknown_predicates"] or item["aggregate_after"] != item["aggregate_before"] or not item["pass"]: waiver_errors.append(item["vector_id"])
    check("E12", "waiver", "waiver validity influences eligibility without changing aggregate truth", waiver_vectors["summary"] == {"total": 4, "passed": 4, "failed": 0} and not waiver_errors, str(waiver_errors))

    issuance_rules = load(DEST / "ISSUANCE-RULES.yaml")
    check("U01", "issuance", "issuance requires eligibility, authority, payload, seal, action, and draft", len(issuance_rules["all_of"]) == 6 and issuance_rules["eligible_automatically_issues"] is False and issuance_rules["failure_behavior"] == "REMAIN_DRAFT")
    issuance_errors = []; issuance_hash_errors = []
    for item in issuance_vectors["vectors"]:
        actual, predicates = issue(item["draft"], item["eligibility"], item["authorization"]["valid"], item["payload_valid"], item["seal_valid"], item["action"]["requested"]); result = item["result"]
        if actual != item["expected"] or actual != item["actual"] or result["resulting_state"] != actual or result["predicates"] != predicates or not item["pass"]: issuance_errors.append(item["vector_id"])
        for value, field in [(item["authorization"], "authorization_hash"), (item["action"], "action_hash"), (result, "result_hash")]:
            if value[field] != digest({key: item_value for key, item_value in value.items() if key != field}): issuance_hash_errors.append(item["vector_id"])
    check("U02", "test-vectors", "all six issuance vectors reproduce independently", issuance_vectors["summary"] == {"total": 6, "passed": 6, "failed": 0} and not issuance_errors, str(issuance_errors))
    check("U03", "hashes", "issuance authority, action, and result records have canonical hashes", not issuance_hash_errors, str(issuance_hash_errors))
    check("U04", "non-implication", "ELIGIBLE without issuance action remains DRAFT", next(item for item in issuance_vectors["vectors"] if item["vector_id"] == "NO_ACTION")["actual"] == "DRAFT")

    validity_model = load(DEST / "VALIDITY-OUTCOMES.yaml"); validity_function = load(DEST / "VALIDITY-FUNCTION.yaml")
    expected_steps = ["SCHEMA", "CERTIFICATE_HASH", "SNAPSHOT_SEAL", "SIGNATURE", "AUTHORITY", "SCOPE", "VALIDITY_INTERVAL", "REVOCATION", "SUPERSESSION", "EVIDENCE_VALIDITY", "AGGREGATE_CONSISTENCY"]
    check("V01", "validity", "seven validity outcomes are derived outside lifecycle", validity_model["outcomes"] == VALIDITY_OUTCOMES and validity_model["derived_not_lifecycle"] is True)
    check("V02", "validity", "eleven ordered validity checks are explicit and deterministic", [item["number"] for item in validity_function["ordered_steps"]] == list(range(1, 12)) and [item["step"] for item in validity_function["ordered_steps"]] == expected_steps and validity_function["hidden_wall_clock"] is False)
    validity_errors = []; validity_hash_errors = []
    for item in validity_vectors["vectors"]:
        result = item["result"]; actual, reasons = validity(item["certificate"], result["evaluated_at"])
        if actual != item["expected"] or actual != item["actual"] or result["status"] != actual or result["reasons"] != reasons or not item["pass"]: validity_errors.append(item["vector_id"])
        if result["validity_hash"] != digest({key: value for key, value in result.items() if key != "validity_hash"}): validity_hash_errors.append(item["vector_id"])
    check("V03", "test-vectors", "all eighteen derived validity vectors reproduce independently", validity_vectors["summary"] == {"total": 18, "passed": 18, "failed": 0} and not validity_errors, str(validity_errors))
    check("V04", "hashes", "all validity result hashes reproduce", not validity_hash_errors, str(validity_hash_errors))
    validity_by_id = {item["vector_id"]: item for item in validity_vectors["vectors"]}
    check("V05", "derived-status", "issued certificate may derive INVALID without lifecycle transition", validity_by_id["HASH_INVALID"]["certificate"]["lifecycle_state"] == "ISSUED" and validity_by_id["HASH_INVALID"]["actual"] == "INVALID")
    check("V06", "terminal-status", "terminal lifecycle state remains authoritative while all failures are reported", all(validity_by_id[key]["actual"] == expected for key, expected in [("REVOKED", "REVOKED"), ("REVOKED_WITH_CORRUPTION", "REVOKED"), ("SUPERSEDED", "SUPERSEDED"), ("LIFECYCLE_EXPIRED", "EXPIRED")]) and "CERTIFICATE_HASH_INVALID" in validity_by_id["REVOKED_WITH_CORRUPTION"]["result"]["reasons"])
    check("V07", "validity", "NOT_YET_VALID and interval expiration derive from explicit evaluated_at", validity_by_id["NOT_YET"]["actual"] == "NOT_YET_VALID" and validity_by_id["NOT_YET_WITH_EVIDENCE_FAILURE"]["actual"] == "INVALID" and validity_by_id["INTERVAL_EXPIRED"]["actual"] == "EXPIRED")
    check("V08", "precedence", "multiple validity failures report all while integrity selects INVALID", validity_by_id["MULTIPLE_FAILURES"]["actual"] == "INVALID" and {"CERTIFICATE_HASH_INVALID", "EVIDENCE_INVALID"}.issubset(validity_by_id["MULTIPLE_FAILURES"]["result"]["reasons"]))

    consumption = load(DEST / "RELEASE-CERTIFICATE-CONSUMPTION.yaml")
    check("R01", "release", "release consumes ISSUED plus VALID and never substitutes eligibility", consumption["required"][:2] == ["CERTIFICATE_LIFECYCLE_ISSUED", "CERTIFICATE_VALIDITY_VALID"] and consumption["eligibility_consumed_as_validity_substitute"] is False)
    release_errors = []; release_hash_errors = []
    for item in release_vectors["vectors"]:
        record = item["evaluation"]; reasons = []
        if record["lifecycle_state"] != "ISSUED": reasons.append("CERTIFICATE_NOT_ISSUED")
        if record["validity"] != "VALID": reasons.append("CERTIFICATE_NOT_VALID")
        if not record["scope_matches"]: reasons.append("SCOPE_MISMATCH")
        if not record["aggregate_allowed"]: reasons.append("AGGREGATE_DISALLOWED")
        actual = "AUTHORIZED" if not reasons else "REJECTED" if any(reason in {"SCOPE_MISMATCH", "AGGREGATE_DISALLOWED"} for reason in reasons) else "BLOCKED"
        if actual != item["expected"] or actual != item["actual"] or record["decision"] != actual or record["reasons"] != reasons or not item["pass"]: release_errors.append(item["vector_id"])
        if record["evaluation_hash"] != digest({key: value for key, value in record.items() if key != "evaluation_hash"}): release_hash_errors.append(item["vector_id"])
    check("R02", "test-vectors", "all seven release-certificate vectors reproduce", release_vectors["summary"] == {"total": 7, "passed": 7, "failed": 0} and not release_errors, str(release_errors))
    check("R03", "release", "current eligibility is not used as substitute for issued certificate validity", next(item for item in release_vectors["vectors"] if item["vector_id"] == "ELIGIBILITY_BLOCKED_NOT_CONSUMED")["actual"] == "AUTHORIZED")
    check("R04", "hashes", "release-certificate evaluation hashes reproduce", not release_hash_errors, str(release_hash_errors))

    nonimplications = load(DEST / "CRITICAL-NON-IMPLICATIONS.yaml"); nonimp_vectors = load(DEST / "NON-IMPLICATION-TEST-VECTORS.yaml")
    check("N00", "non-implication", "all eight critical non-implications are executable", len(nonimplications["forbidden_implications"]) == 8 and nonimp_vectors["summary"] == {"total": 8, "passed": 8, "failed": 0} and all(item["pass"] and item["implication_rejected"] for item in nonimp_vectors["vectors"]))
    invariants = load(DEST / "CERTIFICATE-INVARIANTS.yaml")["invariants"]
    mechanical = {
        "CERT-021": "VALID" not in lifecycle["states"], "CERT-022": "CERTIFICATE_ELIGIBILITY" in separation["independent_dimensions"], "CERT-023": validity_model["derived_not_lifecycle"], "CERT-024": next(item for item in issuance_vectors["vectors"] if item["vector_id"] == "NO_ACTION")["actual"] == "DRAFT", "CERT-025": validity_by_id["HASH_INVALID"]["certificate"]["lifecycle_state"] == "ISSUED" and validity_by_id["HASH_INVALID"]["actual"] == "INVALID",
        "CERT-026": load(DEST / "COMPLETE-CERTIFICATION-PIPELINE.yaml")["ordered_stages"].index("CERTIFICATE_ELIGIBILITY") < load(DEST / "COMPLETE-CERTIFICATION-PIPELINE.yaml")["ordered_stages"].index("ISSUANCE"), "CERT-027": vector_by_id["FALSE_DOMINATES_BLOCKED"]["actual"] == "INELIGIBLE", "CERT-028": vector_by_id["BLOCKED_DOMINATES_UNKNOWN"]["actual"] == "BLOCKED", "CERT-029": vector_by_id["UNKNOWN_ONLY"]["actual"] == "UNKNOWN", "CERT-030": vector_by_id["INVALID_INPUT"]["actual"] == "INELIGIBLE",
        "CERT-031": history_fixture["immutable_distinct_decisions"], "CERT-032": lifecycle_vectors["summary"]["failed"] == 0, "CERT-033": all(source not in {"SUPERSEDED", "REVOKED", "EXPIRED"} for source, _ in legal), "CERT-034": machine["replacement_requires_new_certificate_identity"], "CERT-035": not validity_errors,
        "CERT-036": consumption["eligibility_consumed_as_validity_substitute"] is False, "CERT-037": validity_by_id["AGGREGATE_MISMATCH"]["certificate"]["signature"]["signature_value"] == signature_value(validity_by_id["AGGREGATE_MISMATCH"]["certificate"]["certificate_hash"], validity_by_id["AGGREGATE_MISMATCH"]["certificate"]["authority"]["authority_id"], validity_by_id["AGGREGATE_MISMATCH"]["certificate"]["signature"]["signed_at"]) and validity_by_id["AGGREGATE_MISMATCH"]["actual"] == "INVALID", "CERT-038": all(item["aggregate_after"] == item["aggregate_before"] for item in waiver_vectors["vectors"]), "CERT-039": len(policy["certificate_types"]) == 4 and all(item["allowed_aggregate_results"] for item in policy["certificate_types"]), "CERT-040": set(load(DEST / "ELIGIBILITY-FUNCTION.yaml")["output_reason_arrays"]) == {"FAILED_PREDICATES", "BLOCKING_PREDICATES", "UNKNOWN_PREDICATES", "WARNINGS"},
    }
    check("N01", "invariants", "CERT-021 through CERT-040 have exact stable IDs and checks", [item["id"] for item in invariants] == [f"CERT-{index:03d}" for index in range(21, 41)] and all(item["machine_checked"] for item in invariants) and set(mechanical) == {item["id"] for item in invariants})
    for invariant in invariants: check(invariant["id"], "certificate-invariant", invariant["rule"], mechanical.get(invariant["id"], False))

    current = load(DEST / "CURRENT-V141-STATUS.yaml")
    check("C01", "current", "current upstream truth remains blocked at SPEC_INVALID with no aggregate", current["upstream_status"] == "BLOCKED" and current["upstream_failure"] == "SPEC_INVALID_AT_PIPELINE_STAGE_2" and current["aggregate"] is None and load(V133 / "CURRENT-AGGREGATE.yaml")["objects"] == [])
    check("C02", "non-invention", "no current candidate, certificate, history, eligibility decision, or issuance action is invented", current["invented_objects"] is False and current["certificate_candidate"] is None and all(load(DEST / name)["objects"] == [] for name in ["CERTIFICATES-V141.yaml", "CERTIFICATE-HISTORIES.yaml", "CURRENT-ELIGIBILITY-DECISIONS.yaml", "ELIGIBILITY-HISTORIES.yaml", "ISSUANCE-ACTIONS.yaml"]))
    check("C03", "current", "current no-certificate projection preserves independent dimensions", current_status["certificate_id"] is None and current_status["lifecycle_state"] is None and current_status["eligibility"] == "NOT_APPLICABLE" and current_status["validity"] == "UNKNOWN" and current_status["status_hash"] == digest({key: value for key, value in current_status.items() if key != "status_hash"}))
    check("C04", "current", "release remains not evaluated", current["release_decision"] == "NOT_EVALUATED")

    registry = load(DEST / "OBJECT-REGISTRY.yaml"); object_ids = [item["object_id"] for item in registry["objects"]]
    check("O01", "registry", "two v14.1 current normative object IDs are unique", len(object_ids) == len(set(object_ids)) == 2)
    predecessor_ids = {item["object_id"] for path in [OUT / "OBJECT-REGISTRY.yaml", OUT / "remediation" / "OBJECT-REGISTRY.yaml", OUT / "remediation" / "v13.1" / "OBJECT-REGISTRY.yaml", OUT / "remediation" / "v13.2" / "OBJECT-REGISTRY.yaml", V133 / "OBJECT-REGISTRY.yaml", V14 / "OBJECT-REGISTRY.yaml"] for item in load(path)["objects"]}
    check("O02", "registry", "v14.1 object IDs are globally unique from predecessors", not (set(object_ids) & predecessor_ids))
    check("O03", "references", "predecessor registry references resolve with exact hashes", all((DEST / item["path"]).is_file() and sha_file(DEST / item["path"]) == item["sha256"] for item in registry["external_registries"]))

    prior = load(DEST / "PRIOR-INTEGRITY.yaml"); prior_errors = [item["path"] for item in prior["artifacts"] if not (OUT / item["path"]).is_file() or sha_file(OUT / item["path"]) != item["sha256"] or (OUT / item["path"]).stat().st_size != item["bytes"]]
    check("P01", "append-only", "all 364 predecessor compliance artifacts remain byte-identical", prior["status"] == "PRESERVED" and prior["protected_artifact_count"] == len(prior["artifacts"]) == 364 and not prior_errors, str(prior_errors[:10]))
    check("P02", "append-only", "v14 builder refuses to erase v14.1 extension", "refusing to erase predecessor artifacts after append-only v14.1 extension" in (HS / "tools" / "build_certificate_release_gate_v14.py").read_text(encoding="utf-8"))
    determinism = load(DEST / "DETERMINISM-VALIDATION.yaml") if (DEST / "DETERMINISM-VALIDATION.yaml").is_file() else {}
    check("Q01", "determinism", "all 72 generator outputs reproduce byte-for-byte", determinism.get("status") == "PASS" and determinism.get("summary") == {"total": 72, "identical": 72, "different": 0} and {item["path"] for item in determinism.get("files", [])} == set(DELIVERABLES) and all(item["byte_identical"] for item in determinism.get("files", [])))
    regression = load(DEST / "REGRESSION-VALIDATION.yaml") if (DEST / "REGRESSION-VALIDATION.yaml").is_file() else {}
    expected_regression = {"14.0": (70, 0, 1), "13.3": (139, 0, 1), "13.2": (117, 0, 1), "13.1": (110, 0, 1), "13.0": (115, 0, 1), "12.1": (194, 0, 1), "12.0": (148, 0, 1), "11.1": (177, 0, 1), "10.1": (143, 0, 1)}
    actual_regression = {item["protocol"]: (item["passed"], item["failed"], item["blocked"]) for item in regression.get("regressions", [])}
    check("Q02", "regression", "v10.1 through v14 regressions and append guards pass", regression.get("status") == "PASS" and actual_regression == expected_regression and regression.get("append_only_guards") == {"v13": "PASS_REFUSED", "v13.1": "PASS_REFUSED", "v13.2": "PASS_REFUSED", "v13.3": "PASS_REFUSED", "v14": "PASS_REFUSED", "v14.1": "PASS_REFUSED"})
    check("Q03", "hygiene", "no Python cache artifacts exist", not any(HS.rglob("__pycache__")) and not any(HS.rglob("*.pyc")))
    check("Q04", "tools", "generic and pinned v14.1 builders and validators exist", all((HS / "tools" / name).is_file() for name in ["build_certificate_state_eligibility.py", "build_certificate_state_eligibility_v141.py", "validate_certificate_state_eligibility.py", "validate_certificate_state_eligibility_v141.py"]))
    reports = [load(DEST / "reports" / name) for name in REPORT_FILES]
    check("G01", "reports", "four reports preserve lifecycle, eligibility, validity, and release separation", reports[0]["valid_removed_from_v14_1_lifecycle"] and reports[1]["current_decision"] == "NOT_APPLICABLE_NO_CANDIDATE" and reports[2]["derived_property"] and reports[3]["eligibility_used_as_validity_substitute"] is False)
    blocked("GATE-V141", "acceptance", "current certification and release", "The v14.1 protocol validates structurally; current v13.3 specification validation remains blocked, no certificate candidate or certificate exists, eligibility is not applicable, validity is UNKNOWN, and release is not evaluated.")
    return finish(checks)


def finish(checks: list[dict[str, str]]) -> int:
    passed = sum(item["result"] == "PASS" for item in checks); failed = sum(item["result"] == "FAIL" for item in checks); blocked_count = sum(item["result"] == "BLOCKED" for item in checks)
    report = {"schema_version": VERSION, "validator": "Protocol-v14.1 independent certificate-state validator", "overall_status": "FAIL" if failed else "STRUCTURAL_PASS_CURRENT_CERTIFICATION_NOT_APPLICABLE" if blocked_count else "PASS", "acceptance": "VALIDATION_FAILED" if failed else "BLOCKED" if blocked_count else "PASS", "summary": {"total": len(checks), "passed": passed, "failed": failed, "blocked": blocked_count}, "object_counts": {"schemas": 21, "lifecycle_states": 5, "eligibility_outcomes": 4, "validity_outcomes": 7, "current_certificates": 0, "current_candidates": 0, "certificate_invariants": 20}, "checks": checks}
    (DEST / "VALIDATION.yaml").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    lines = ["# Protocol-v14.1 Independent Certificate-State Validation", "", f"**Overall:** `{report['overall_status']}`", f"**Acceptance:** `{report['acceptance']}`", f"**Checks:** {passed} PASS / {failed} FAIL / {blocked_count} BLOCKED ({len(checks)} total)", "", "Structural validity does not create a certificate candidate, eligibility decision, issuance action, certificate, or release authorization.", "", "| ID | Category | Result | Description | Detail |", "|---|---|---|---|---|"]
    for item in checks: lines.append("| %s | %s | %s | %s | %s |" % (item["check_id"], item["category"], item["result"], item["description"].replace("|", "\\|"), item["detail"].replace("|", "\\|")))
    (DEST / "VALIDATION.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{passed} PASS / {failed} FAIL / {blocked_count} BLOCKED ({len(checks)} checks); {report['overall_status']}")
    return 1 if failed else 0


if __name__ == "__main__": sys.exit(main())
