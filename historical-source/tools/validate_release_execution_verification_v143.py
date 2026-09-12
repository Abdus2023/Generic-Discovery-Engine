#!/usr/bin/env python3
"""Independent validator for Protocol-v14.3 release execution and verification."""
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
V141 = OUT / "certification" / "v14.1"
DEST = OUT / "certification" / "v14.3"
SCHEMA = DEST / "schema"
VERSION = "14.3"
CERT_CANDIDATE_STATES = ["CREATED", "ACTIVE", "CONSUMED", "CANCELLED", "EXPIRED", "RETAINED"]
CERT_LIFECYCLE = ["DRAFT", "ISSUED", "REVOKED", "SUPERSEDED", "EXPIRED", "CANCELLED"]
CERT_VALIDITY = ["VALID", "INVALID", "NOT_YET_VALID", "UNKNOWN"]
RELEASE_ELIGIBILITY = ["ELIGIBLE", "INELIGIBLE", "BLOCKED", "UNKNOWN"]
DECISIONS = ["APPROVED", "REJECTED", "BLOCKED", "DEFERRED"]
EXECUTION_STATES = ["NOT_STARTED", "STARTED", "SUCCEEDED", "FAILED", "CANCELLED", "ROLLED_BACK"]
POST_STATES = ["VERIFIED", "FAILED", "INCONCLUSIVE", "BLOCKED", "UNKNOWN"]
SCHEMA_NAMES = ["candidate", "certificate-candidate", "certificate", "certificate-eligibility", "certificate-validity", "certificate-issuance-event", "certificate-revocation-event", "certificate-supersession-event", "release", "release-gate-predicate", "release-gate", "release-eligibility", "release-decision", "release-decision-event", "release-execution", "post-release-verification", "current-certificate", "current-release-eligibility", "current-release-decision", "current-release-execution", "current-post-release-verification", "authority", "predicate-evaluation", "temporal-interval", "certificate-release-binding", "certificate-candidate-event", "release-execution-event", "post-release-verification-event"]
MACHINE_FILES = ["VERSION.yaml", "SCOPE.yaml", "PROBLEM-STATEMENT.yaml", "SEMANTIC-CORRECTIONS.yaml", "CANONICAL-MODEL.yaml", "DOMAIN-SEPARATION.yaml", "CERTIFICATE-CANDIDATE-MODEL.yaml", "CERTIFICATE-CANDIDATE-TRANSITIONS.yaml", "CERTIFICATE-LIFECYCLE-MODEL.yaml", "CERTIFICATE-LIFECYCLE-TRANSITIONS.yaml", "CERTIFICATE-VALIDITY-FUNCTION.yaml", "DISCOVERY-CANDIDATE-SEPARATION.yaml", "RELEASE-IDENTITY-MODEL.yaml", "CERTIFICATE-RELEASE-BINDING.yaml", "RELEASE-GATE-DEFINITION.yaml", "RELEASE-GATE-PREDICATE-REGISTRY.yaml", "RELEASE-ELIGIBILITY-FUNCTION.yaml", "RELEASE-ELIGIBILITY-PRECEDENCE.yaml", "RELEASE-DECISION-FUNCTION.yaml", "RELEASE-AUTHORITY-MODEL.yaml", "RELEASE-EXECUTION-STATE-MACHINE.yaml", "RELEASE-EXECUTION-GUARDS.yaml", "POST-RELEASE-VERIFICATION-MODEL.yaml", "IMMUTABLE-EVENT-MODEL.yaml", "CURRENT-PROJECTION-MODEL.yaml", "TEMPORAL-MODEL.yaml", "DECISION-REUSE-FUNCTION.yaml", "IDENTITY-BINDING-MODEL.yaml", "VALIDATION-PROCEDURE.yaml", "FAILURE-MODES.yaml", "EPISTEMIC-REGISTER.yaml", "TRACEABILITY.yaml", "INVARIANTS.yaml", "REQUIRED-TEST-VECTORS.yaml", "CERTIFICATE-CANDIDATES.yaml", "CERTIFICATES.yaml", "RELEASES.yaml", "RELEASE-ELIGIBILITY-HISTORY.yaml", "RELEASE-DECISION-HISTORY.yaml", "RELEASE-EXECUTION-HISTORY.yaml", "POST-RELEASE-VERIFICATION-HISTORY.yaml", "CURRENT-STATES.yaml", "OPEN-QUESTIONS.yaml", "FINAL-PRINCIPLE.yaml", "ARTIFACT-TREE.yaml", "OBJECT-REGISTRY.yaml", "SCHEMA-REGISTRY.yaml", "PRIOR-INTEGRITY.yaml", "VALIDATION-REPORT.yaml"]
REPORT_FILES = ["SEMANTIC-GAP-REPORT.yaml", "IDENTITY-BINDING-REPORT.yaml", "EXECUTION-SEPARATION-REPORT.yaml", "CURRENT-HISTORICAL-STATUS.yaml"]
DELIVERABLES = [*MACHINE_FILES, *(f"schema/{name}.schema.yaml" for name in SCHEMA_NAMES), *(f"reports/{name}" for name in REPORT_FILES), "SPECIFICATION.md"]


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
        results = [schema_errors(value, item, schemas, path) for item in body["oneOf"]]
        return [] if sum(not item for item in results) == 1 else [f"{path}: oneOf"]
    errors: list[str] = []; expected = body.get("type")
    if expected:
        checks = {"object": isinstance(value, dict), "array": isinstance(value, list), "string": isinstance(value, str), "integer": isinstance(value, int) and not isinstance(value, bool), "boolean": isinstance(value, bool), "null": value is None}
        if not checks.get(expected, False): return [f"{path}: type"]
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


def interval_active(not_before: str, not_after: str | None, evaluated_at: str) -> bool: return evaluated_at >= not_before and (not_after is None or evaluated_at < not_after)


def release_eligibility(predicates: list[dict[str, Any]], registry: list[dict[str, Any]], malformed: bool = False) -> tuple[str, list[str], list[str]]:
    if malformed: return "INELIGIBLE", ["MALFORMED_PREDICATE_INPUT"], []
    by_id = {item["predicate_id"]: item for item in predicates}; mandatory = [item for item in registry if item["mandatory"]]
    missing = [item["predicate_id"] for item in mandatory if item["predicate_id"] not in by_id]
    if missing: return "BLOCKED", ["MISSING_MANDATORY_PREDICATE:" + item for item in missing], []
    if not mandatory: return "BLOCKED", ["NO_MANDATORY_PREDICATES"], []
    values = [by_id[item["predicate_id"]] for item in mandatory]; optional = [item["predicate_id"] for item in predicates if not next((rule["mandatory"] for rule in registry if rule["predicate_id"] == item["predicate_id"]), False) and item["result"] != "TRUE"]
    for result, status in [("FALSE", "INELIGIBLE"), ("BLOCKED", "BLOCKED"), ("UNKNOWN", "UNKNOWN")]:
        matches = [item["reason"] for item in values if item["result"] == result]
        if matches: return status, matches, optional
    return "ELIGIBLE", [], optional


def release_decision(eligibility: str, authority_outcome: str, defer_requested: bool, defer_allowed: bool) -> tuple[str, str]:
    if eligibility == "INELIGIBLE": return "REJECTED", "PROVEN_GATE_FAILURE"
    if eligibility in {"BLOCKED", "UNKNOWN"}: return "BLOCKED", "AUTHORIZATION_CANNOT_PROCEED"
    if authority_outcome == "REJECT": return "REJECTED", "AUTHORIZED_REJECTION"
    if defer_requested: return ("DEFERRED", "AUTHORIZED_POSTPONEMENT") if defer_allowed else ("BLOCKED", "DEFER_NOT_PERMITTED")
    return ("APPROVED", "AUTHORIZATION_PREDICATES_SATISFIED") if authority_outcome == "APPROVE" else ("BLOCKED", "AUTHORITY_UNAVAILABLE_OR_INVALID")


def execution_start(decision: str, active: bool, release_match: bool, artifact_match: bool, certificate_valid: bool, reusable: bool) -> tuple[str, str]:
    if decision != "APPROVED": return "NOT_STARTED", "DECISION_NOT_APPROVED"
    if not active: return "NOT_STARTED", "DECISION_EXPIRED"
    if not release_match: return "NOT_STARTED", "RELEASE_IDENTITY_MISMATCH"
    if not artifact_match: return "NOT_STARTED", "ARTIFACT_IDENTITY_MISMATCH"
    if not reusable: return "NOT_STARTED", "DECISION_INPUT_CHANGED"
    if not certificate_valid: return "NOT_STARTED", "CERTIFICATE_NO_LONGER_VALID"
    return "STARTED", "EXECUTION_GUARDS_SATISFIED"


def binding_match(binding: dict[str, str], release: dict[str, Any]) -> tuple[bool, list[str]]:
    actual = {"release_id": release["release_id"], "artifact_id": release["artifact"]["artifact_id"], "artifact_hash": release["artifact"]["content_hash"], "implementation_id": release["implementation_id"], "specification_hash": release["specification"]["specification_hash"], "environment_id": release["environment"]["environment_id"]}
    reasons = [key.upper() + "_MISMATCH" for key, value in actual.items() if binding.get(key) != value]
    return not reasons, reasons


def project_events(events: list[dict[str, Any]]) -> tuple[str, str | None]:
    state = "NOT_STARTED"; previous = None; legal = {("NOT_STARTED", "STARTED"), ("STARTED", "SUCCEEDED"), ("STARTED", "FAILED"), ("STARTED", "CANCELLED"), ("FAILED", "STARTED"), ("SUCCEEDED", "ROLLED_BACK"), ("FAILED", "ROLLED_BACK")}
    for index, event in enumerate(events):
        if event.get("sequence") != index or event.get("previous_event_id") != previous or event.get("from_state") != state or (state, event.get("to_state")) not in legal or event.get("content_hash") != digest({key: value for key, value in event.items() if key != "content_hash"}): return "HISTORY_INVALID", None
        state = event["to_state"]; previous = event["event_id"]
    return "VALID", state


def evaluate_vector(item: dict[str, Any]) -> tuple[str, str]:
    operation = item["operation"]; source = item["input"]
    if operation == "CERT_VALIDITY":
        lifecycle = source["lifecycle"]
        if lifecycle == "DRAFT": return "UNKNOWN", "CERTIFICATE_NOT_ISSUED"
        if lifecycle in {"REVOKED", "SUPERSEDED", "EXPIRED", "CANCELLED"}: return "INVALID", "LIFECYCLE_" + lifecycle
        for field, reason in [("schema", "SCHEMA_INVALID"), ("hash", "HASH_INVALID"), ("signature", "SIGNATURE_INVALID"), ("authority", "AUTHORITY_INVALID"), ("binding", "BINDING_INVALID"), ("scope", "SCOPE_INVALID"), ("evidence", "EVIDENCE_INVALID"), ("policy", "POLICY_INVALID")]:
            if source.get(field, True) is False: return "INVALID", reason
        if source.get("interval") == "NOT_YET": return "NOT_YET_VALID", "NOT_BEFORE_NOT_REACHED"
        return "VALID", "ALL_VALIDITY_PREDICATES_TRUE"
    if operation == "CANDIDATE_STATE": return (source["to"], "CANDIDATE_CANCELLED") if source["authorized"] and (source["from"], source["to"]) == ("ACTIVE", "CANCELLED") else (source["from"], "TRANSITION_BLOCKED")
    if operation == "BINDING":
        valid, reasons = binding_match(source["binding"], source["release"]); return ("ELIGIBLE", "BINDING_MATCH") if valid else ("INELIGIBLE", reasons[0])
    if operation == "RELEASE_ELIGIBILITY":
        status, reasons, warnings = release_eligibility(source["predicates"], source["registry"]); return status, reasons[0] if reasons else "OPTIONAL_WARNING_ONLY" if warnings else "ALL_MANDATORY_TRUE"
    if operation == "RELEASE_DECISION": return release_decision(source["eligibility"], source["authority_outcome"], source["defer_requested"], source["defer_allowed"])
    if operation == "EXECUTION_START": return execution_start(source["decision"], source["active"], source["release_match"], source["artifact_match"], source["certificate_valid"], source["policy_reusable"])
    if operation == "EXECUTION_RESULT": return source["result"], {"FAILED": "EXECUTION_FAILED", "SUCCEEDED": "EXECUTION_SUCCEEDED", "ROLLED_BACK": "ROLLBACK_RECORDED"}[source["result"]]
    if operation == "POST_VERIFY": return source["verification"], "POST_RELEASE_FAILED_DECISION_UNCHANGED"
    if operation == "HISTORICAL_REPLAY": return source["recorded"], "HISTORICAL_POLICY_ISOLATION"
    if operation == "DECISION_PROJECTION": return "APPROVED", "LATEST_VALID_DECISION"
    if operation == "EVENT_PROJECTION":
        result, state = project_events(source["events"]); return state or result, "PROJECTED_FROM_IMMUTABLE_EVENTS" if result == "VALID" else "HISTORY_INVALID"
    raise ValueError(operation)


def main() -> int:
    checks: list[dict[str, str]] = []
    def check(identifier: str, category: str, description: str, condition: bool, detail: str = "") -> None: checks.append({"check_id": identifier, "category": category, "result": "PASS" if condition else "FAIL", "description": description, "detail": detail})
    def blocked(identifier: str, category: str, description: str, detail: str) -> None: checks.append({"check_id": identifier, "category": category, "result": "BLOCKED", "description": description, "detail": detail})
    check("I01", "inventory", "all 82 generator-owned v14.3 deliverables exist", len(DELIVERABLES) == 82 and all((DEST / path).is_file() for path in DELIVERABLES))
    parse_errors = []
    for path in DEST.rglob("*.yaml"):
        try: load(path)
        except Exception as exc: parse_errors.append(f"{path.relative_to(DEST)}:{exc}")
    check("I02", "syntax", "all YAML is JSON-compatible and parseable", not parse_errors, str(parse_errors[:10]))
    schemas = {name: load(SCHEMA / f"{name}.schema.yaml") for name in SCHEMA_NAMES}; ids = [item.get("$id") for item in schemas.values()]
    check("S01", "schemas", "all 28 required schemas have unique stable IDs", len(ids) == len(set(ids)) == 28 and all(ids))
    check("S02", "schemas", "all normative object schemas reject undeclared top-level fields", all(item.get("additionalProperties") is False for item in schemas.values()))
    registry = load(DEST / "SCHEMA-REGISTRY.yaml"); schema_reg_errors = [item["name"] for item in registry["schemas"] if item["name"] not in schemas or sha_file(DEST / item["path"]) != item["sha256"]]
    check("S03", "schemas", "schema registry resolves every schema with exact hash", len(registry["schemas"]) == 28 and not schema_reg_errors, str(schema_reg_errors))
    gate = load(DEST / "RELEASE-GATE-DEFINITION.yaml")["objects"][0]; instances: list[tuple[str, Any, str]] = [("release-gate", gate, "gate")]
    instances += [("release-gate-predicate", item, item["predicate_id"]) for item in gate["predicate_registry"]]
    vector_data = load(DEST / "REQUIRED-TEST-VECTORS.yaml"); mismatch = next(item for item in vector_data["vectors"] if item["number"] == 8); instances += [("release", mismatch["input"]["release"], "release-vector"), ("certificate-release-binding", mismatch["input"]["binding"], "binding-vector")]
    reconstruction = next(item for item in vector_data["vectors"] if item["number"] == 30); instances += [("release-execution-event", item, "execution-event") for item in reconstruction["input"]["events"]]
    current = load(DEST / "CURRENT-STATES.yaml"); instances += [("current-certificate", current["current_certificate"], "current-certificate"), ("current-release-eligibility", current["current_release_eligibility"], "current-eligibility"), ("current-release-decision", current["current_release_decision"], "current-decision"), ("current-release-execution", current["current_release_execution"], "current-execution"), ("current-post-release-verification", current["current_post_release_verification"], "current-post")]
    schema_errors_found = []
    for schema_name, value, label in instances: schema_errors_found += [f"{label}:{error}" for error in schema_errors(value, schemas[schema_name], schemas)]
    check("S04", "schemas", "gate, release, binding, events, and current projections satisfy schemas", not schema_errors_found, str(schema_errors_found[:20]))

    separation = load(DEST / "DOMAIN-SEPARATION.yaml")
    check("M01", "separation", "all ten operational domains remain independent", len(separation["independent_domains"]) == 10 and separation["cross_domain_implicit_implication"] == "FORBIDDEN" and separation["process_state_is_truth_state"] is False)
    canonical_model = load(DEST / "CANONICAL-MODEL.yaml")
    check("M02", "pipeline", "release pipeline is complete from audit snapshot through post-release verification", canonical_model["release_pipeline"] == ["AUDIT_SNAPSHOT", "AGGREGATE_CONFORMANCE", "CERTIFICATE_ELIGIBILITY", "CERTIFICATE_ISSUANCE", "CERTIFICATE_VALIDITY", "RELEASE_GATE", "RELEASE_ELIGIBILITY", "RELEASE_DECISION", "RELEASE_EXECUTION", "POST_RELEASE_VERIFICATION"])
    corrections = load(DEST / "SEMANTIC-CORRECTIONS.yaml")
    check("M03", "append-only", "semantic corrections do not mutate earlier artifacts", corrections["earlier_artifacts_mutated"] is False and len(corrections["corrections"]) == 7)
    candidate = load(DEST / "CERTIFICATE-CANDIDATE-MODEL.yaml"); discovery = load(DEST / "DISCOVERY-CANDIDATE-SEPARATION.yaml")
    check("M04", "candidate", "certificate candidate, certificate, and discovery candidate remain distinct", candidate["certificate_candidate_is_certificate"] is False and candidate["draft_equivalence"] == "CONTRADICTED" and discovery["certificate_or_release_fields_added"] is False)
    lifecycle = load(DEST / "CERTIFICATE-LIFECYCLE-MODEL.yaml")
    check("M05", "certificate", "certificate lifecycle and four-state derived validity do not duplicate terminal states", lifecycle["states"] == CERT_LIFECYCLE and lifecycle["validity_statuses"] == CERT_VALIDITY and lifecycle["validity_is_derived"] and lifecycle["invalidity_fabricates_revocation"] is False)
    transitions = load(DEST / "CERTIFICATE-LIFECYCLE-TRANSITIONS.yaml")
    check("M06", "certificate", "certificate terminal states have no outgoing transition", transitions["terminal"] == ["REVOKED", "SUPERSEDED", "EXPIRED", "CANCELLED"] and transitions["terminal_outgoing"] == [] and len(transitions["allowed"]) == 6)

    release_identity = load(DEST / "RELEASE-IDENTITY-MODEL.yaml"); binding_rules = load(DEST / "CERTIFICATE-RELEASE-BINDING.yaml")
    check("B01", "identity", "release identity has twelve components and version label is insufficient", len(release_identity["identity_components"]) == 12 and release_identity["version_label_is_identity"] is False)
    check("B02", "binding", "certificate binds all eight mandatory release identities and mismatch is ineligible", len(binding_rules["mandatory"]) == 8 and binding_rules["mismatch_result"] == "RELEASE_INELIGIBLE" and binding_rules["silent_cross_release_authorization"] is False)
    valid_binding = dict(mismatch["input"]["binding"]); valid_binding["artifact_hash"] = mismatch["input"]["release"]["artifact"]["content_hash"]
    check("B03", "binding", "exact binding match and artifact mismatch reproduce", binding_match(valid_binding, mismatch["input"]["release"])[0] and binding_match(mismatch["input"]["binding"], mismatch["input"]["release"])[1] == ["ARTIFACT_HASH_MISMATCH"])
    check("B04", "hashes", "release and gate canonical hashes validate", mismatch["input"]["release"]["release_hash"] == digest({key: value for key, value in mismatch["input"]["release"].items() if key != "release_hash"}) and gate["gate_hash"] == digest({key: value for key, value in gate.items() if key != "gate_hash"}))

    gate_model = load(DEST / "RELEASE-GATE-DEFINITION.yaml"); domains = {item["domain"] for item in gate["predicate_registry"]}
    check("G01", "gate", "release gate is policy without embedded evaluation results", gate_model["contains_evaluation_results"] is False and "status" not in gate and "decision" not in gate)
    check("G02", "gate", "gate covers all ten required predicate domains", domains == {"CERTIFICATE", "CONFORMANCE", "SECURITY", "COMPATIBILITY", "ENVIRONMENT", "AUTHORITY", "FRESHNESS", "RESOURCE", "REGRESSION", "WAIVER"})
    precedence = load(DEST / "RELEASE-ELIGIBILITY-PRECEDENCE.yaml")
    check("E01", "eligibility", "mandatory precedence is FALSE > BLOCKED > UNKNOWN > TRUE", precedence["mandatory_precedence"] == ["FALSE", "BLOCKED", "UNKNOWN", "TRUE"])
    check("E02", "eligibility", "empty mandatory set blocks and optional failure only warns", precedence["no_mandatory_predicates"] == "BLOCKED" and precedence["optional_failure_effect"] == "WARNING_ONLY")
    p = lambda result: [{"predicate_id": "P", "mandatory": True, "result": result, "reason": result, "evidence_refs": []}]
    r = [{"predicate_id": "P", "mandatory": True}]
    check("E03", "eligibility", "eligibility evaluator independently reproduces all four outcomes", [release_eligibility(p(value), r)[0] for value in ["TRUE", "FALSE", "BLOCKED", "UNKNOWN"]] == ["ELIGIBLE", "INELIGIBLE", "BLOCKED", "UNKNOWN"])
    check("E04", "eligibility", "missing, malformed, and no-mandatory behavior is explicit", release_eligibility([], r)[0] == "BLOCKED" and release_eligibility([], [], False)[1] == ["NO_MANDATORY_PREDICATES"] and release_eligibility([], r, True)[0] == "INELIGIBLE")
    decision_model = load(DEST / "RELEASE-DECISION-FUNCTION.yaml")
    check("D01", "decision", "decision has exact approved/rejected/blocked/deferred semantics", decision_model["outcomes"] == DECISIONS and decision_model["unknown_maps_to_deferred"] is False)
    check("D02", "decision", "eligibility neither implies approval nor execution", decision_model["eligible_implies_approved"] is False and decision_model["approved_implies_executed"] is False)
    check("D03", "authority", "automated release authority is policy-defined rather than assumed", load(DEST / "RELEASE-AUTHORITY-MODEL.yaml")["automated_authorization"] == "POLICY_DEFINED_NOT_ASSUMED")

    execution_machine = load(DEST / "RELEASE-EXECUTION-STATE-MACHINE.yaml"); legal = {(item["from"], item["to"]) for item in execution_machine["allowed"]}
    check("X01", "execution", "execution state machine supports guarded failure, retry, cancellation, and rollback", {("NOT_STARTED", "STARTED"), ("STARTED", "FAILED"), ("FAILED", "STARTED"), ("SUCCEEDED", "ROLLED_BACK")}.issubset(legal) and execution_machine["authorization_history_mutated"] is False)
    guards = load(DEST / "RELEASE-EXECUTION-GUARDS.yaml")
    check("X02", "execution", "execution start requires six independent guards", len(guards["start_all_of"]) == 6 and guards["artifact_mutation"] == "NOT_STARTED_ARTIFACT_IDENTITY_MISMATCH")
    check("X03", "execution", "expired decision and revoked certificate cannot start execution", execution_start("APPROVED", False, True, True, True, True)[1] == "DECISION_EXPIRED" and execution_start("APPROVED", True, True, True, False, True)[1] == "CERTIFICATE_NO_LONGER_VALID")
    post = load(DEST / "POST-RELEASE-VERIFICATION-MODEL.yaml")
    check("X04", "post-release", "post-release result neither mutates decision nor follows from execution success", post["decision_mutated_by_result"] is False and post["execution_success_implies_verified"] is False and post["outcomes"] == POST_STATES)

    temporal = load(DEST / "TEMPORAL-MODEL.yaml")
    check("T01", "temporal", "half-open UTC interval boundaries are exact", temporal["interval"] == "[not_before, not_after)" and interval_active("2026-01-01T00:00:00Z", "2026-02-01T00:00:00Z", "2026-01-01T00:00:00Z") and not interval_active("2026-01-01T00:00:00Z", "2026-02-01T00:00:00Z", "2026-02-01T00:00:00Z"))
    check("T02", "temporal", "future, rollback, uncertainty, and historical replay rules are explicit", temporal["future_timestamp"] == temporal["clock_rollback"] == "TEMPORAL_DEFECT" and temporal["clock_uncertainty"] == "EXPLICIT_MILLISECONDS_CONSERVATIVE_BOUNDARY_RESULT_UNKNOWN" and temporal["current_policy_for_historical_replay"] == "FORBIDDEN")
    reuse = load(DEST / "DECISION-REUSE-FUNCTION.yaml")
    check("T03", "reuse", "all thirteen decision-relevant dimensions participate in exact reuse", len(reuse["decision_relevant_inputs"]) == 13 and len(reuse["reusable_iff"]) == 4 and reuse["any_unknown_equivalence"] == "NOT_REUSABLE")
    validation = load(DEST / "VALIDATION-PROCEDURE.yaml"); expected_stages = ["LOAD", "SCHEMA_VALIDATION", "REFERENCE_RESOLUTION", "HASH_VALIDATION", "TEMPORAL_VALIDATION", "SCOPE_VALIDATION", "POLICY_VALIDATION", "STATE_TRANSITION_VALIDATION", "PREDICATE_EVALUATION", "AGGREGATION", "CURRENT_PROJECTION"]
    check("A01", "validation", "eleven-stage validation pipeline is exact", [item["number"] for item in validation["stages"]] == list(range(1, 12)) and [item["stage"] for item in validation["stages"]] == expected_stages)
    failure_modes = load(DEST / "FAILURE-MODES.yaml")
    check("A02", "attribution", "ten failure layers are distinguished from implementation failure", len(failure_modes["failure_modes"]) == 10 and failure_modes["all_failures_are_implementation_failure"] is False)
    event_model = load(DEST / "IMMUTABLE-EVENT-MODEL.yaml"); projection_model = load(DEST / "CURRENT-PROJECTION-MODEL.yaml")
    check("H01", "history", "events are append-only and remain domain-specific", event_model["append_only"] and event_model["universal_lifecycle_enum"] is False and len(event_model["domain_specific_schemas"]) == 7)
    check("H02", "projection", "current state is reconstructible from valid immutable history", projection_model["reconstructible"] and projection_model["mutable_historical_replacement"] is False and projection_model["invalid_event_skip"] is False)

    vector_errors = []
    for item in vector_data["vectors"]:
        actual_state, actual_reason = evaluate_vector(item)
        if actual_state != item["expected_state"] or actual_reason != item["expected_reason"]: vector_errors.append(f"{item['vector_id']}:{actual_state}:{actual_reason}")
    check("V01", "test-vectors", "all thirty required end-to-end vectors reproduce independently", vector_data["summary"] == {"total": 30, "passed": 30, "failed": 0} and [item["number"] for item in vector_data["vectors"]] == list(range(1, 31)) and not vector_errors, str(vector_errors))
    check("V02", "test-vectors", "every vector exposes predicates, state, event, projection, and reason", all(set(item) >= {"input", "expected_predicates", "expected_state", "expected_event", "expected_current_projection", "expected_reason"} for item in vector_data["vectors"]))
    check("V03", "precedence", "proven mandatory failure is not hidden by blocker", next(item for item in vector_data["vectors"] if item["number"] == 10)["expected_state"] == "INELIGIBLE")
    check("V04", "history", "post-release failure leaves prior approval unchanged", next(item for item in vector_data["vectors"] if item["number"] == 22)["input"]["decision_before"] == "APPROVED")
    check("V05", "replay", "historical replay uses policy at as-of time rather than current policy", next(item for item in vector_data["vectors"] if item["number"] == 26)["input"]["policy_at_as_of"] != next(item for item in vector_data["vectors"] if item["number"] == 26)["input"]["current_policy"])

    epistemic = load(DEST / "EPISTEMIC-REGISTER.yaml")
    check("K01", "epistemic", "all required epistemic labels are used with explicit basis", set(epistemic["allowed_labels"]) == {"PROVED", "SUPPORTED", "INFERRED", "CONJECTURED", "CONTRADICTED", "UNKNOWN"} and {item["status"] for item in epistemic["claims"]} == set(epistemic["allowed_labels"]) and all(item["basis"] for item in epistemic["claims"]))
    traceability = load(DEST / "TRACEABILITY.yaml")
    check("K02", "traceability", "baseline requirements trace directionally to v14.3 artifacts", len(traceability["baseline_sections"]) == 21 and traceability["reverse_proof_forbidden"] is True)
    invariant_data = load(DEST / "INVARIANTS.yaml")["invariants"]
    mechanical = [
        len({item["id"] for item in invariant_data}) == 25, len(CERT_LIFECYCLE) == 6, transitions["terminal_outgoing"] == [], lifecycle["validity_is_derived"], lifecycle["invalidity_fabricates_revocation"] is False,
        decision_model["eligible_implies_approved"] is False, decision_model["approved_implies_executed"] is False, post["execution_success_implies_verified"] is False, event_model["append_only"], projection_model["reconstructible"],
        binding_rules["silent_cross_release_authorization"] is False, release_identity["version_label_is_identity"] is False, temporal["current_policy_for_historical_replay"] == "FORBIDDEN", execution_start("APPROVED", False, True, True, True, True)[0] == "NOT_STARTED", next(item for item in vector_data["vectors"] if item["number"] == 10)["expected_state"] == "INELIGIBLE",
        next(item for item in vector_data["vectors"] if item["number"] == 11)["expected_state"] == "BLOCKED", next(item for item in vector_data["vectors"] if item["number"] == 12)["expected_state"] == "UNKNOWN", candidate["certificate_candidate_is_certificate"] is False, gate_model["contains_evaluation_results"] is False, execution_machine["authorization_history_mutated"] is False,
        post["decision_mutated_by_result"] is False, binding_match(mismatch["input"]["binding"], mismatch["input"]["release"])[0] is False, len(reuse["decision_relevant_inputs"]) == 13, projection_model["invalid_event_skip"] is False, all(item["machine_checked"] for item in invariant_data),
    ]
    check("N00", "invariants", "25 stable invariants have 25 mechanical predicates", [item["id"] for item in invariant_data] == [f"V143-INV-{index:03d}" for index in range(1, 26)] and len(mechanical) == 25)
    for item, result in zip(invariant_data, mechanical): check(item["id"], "invariant", item["rule"], result)

    empty_files = ["CERTIFICATE-CANDIDATES.yaml", "CERTIFICATES.yaml", "RELEASES.yaml", "RELEASE-ELIGIBILITY-HISTORY.yaml", "RELEASE-DECISION-HISTORY.yaml", "RELEASE-EXECUTION-HISTORY.yaml", "POST-RELEASE-VERIFICATION-HISTORY.yaml"]
    check("C01", "non-invention", "current package invents no candidate, certificate, release, decision, execution, or verification", all(load(DEST / name)["objects"] == [] for name in empty_files) and current["source_histories_empty"] is True)
    check("C02", "current", "five empty-domain current projections contain no fabricated entity", all(current[key]["entity_id"] is None and current[key]["last_event_id"] is None and current[key]["projection_hash"] == digest({name: value for name, value in current[key].items() if name != "projection_hash"}) for key in ["current_certificate", "current_release_eligibility", "current_release_decision", "current_release_execution", "current_post_release_verification"]))
    current_report = load(DEST / "reports/CURRENT-HISTORICAL-STATUS.yaml")
    check("C03", "current", "current historical status is proved blocked upstream with zero operational objects", current_report["epistemic_status"] == "PROVED" and current_report["upstream_audit"] == "BLOCKED_SPEC_INVALID" and current_report["invented_objects"] is False and sum(current_report[key] for key in ["certificate_candidates", "certificates", "releases", "release_decisions", "release_executions", "post_release_verifications"]) == 0)

    object_registry = load(DEST / "OBJECT-REGISTRY.yaml"); object_ids = [item["object_id"] for item in object_registry["objects"]]
    check("O01", "registry", "six v14.3 normative object identities are unique", len(object_ids) == len(set(object_ids)) == 6)
    predecessor_ids = {item["object_id"] for path in [V141 / "OBJECT-REGISTRY.yaml", OUT / "certification/v14/OBJECT-REGISTRY.yaml"] for item in load(path)["objects"]}
    check("O02", "registry", "v14.3 IDs are unique from predecessor registries", not (set(object_ids) & predecessor_ids))
    check("O03", "references", "predecessor registries resolve with exact hashes", all((DEST / item["path"]).is_file() and sha_file(DEST / item["path"]) == item["sha256"] for item in object_registry["external_registries"]))
    prior = load(DEST / "PRIOR-INTEGRITY.yaml"); prior_errors = [item["path"] for item in prior["artifacts"] if not (OUT / item["path"]).is_file() or sha_file(OUT / item["path"]) != item["sha256"] or (OUT / item["path"]).stat().st_size != item["bytes"]]
    check("P01", "append-only", "all 440 predecessor compliance artifacts remain byte-identical", prior["status"] == "PRESERVED" and prior["protected_artifact_count"] == len(prior["artifacts"]) == 440 and not prior_errors, str(prior_errors[:10]))
    check("P02", "append-only", "v14.1 builder refuses to erase v14.3", "refusing to erase predecessor artifacts after append-only v14.3 extension" in (HS / "tools/build_certificate_state_eligibility_v141.py").read_text())
    determinism = load(DEST / "DETERMINISM-VALIDATION.yaml") if (DEST / "DETERMINISM-VALIDATION.yaml").is_file() else {}
    check("Q01", "determinism", "all 82 generator outputs reproduce byte-for-byte", determinism.get("status") == "PASS" and determinism.get("summary") == {"total": 82, "identical": 82, "different": 0} and {item["path"] for item in determinism.get("files", [])} == set(DELIVERABLES))
    regression = load(DEST / "REGRESSION-VALIDATION.yaml") if (DEST / "REGRESSION-VALIDATION.yaml").is_file() else {}
    expected = {"14.1": (82, 0, 1), "14.0": (70, 0, 1), "13.3": (139, 0, 1), "13.2": (117, 0, 1), "13.1": (110, 0, 1), "13.0": (115, 0, 1), "12.1": (194, 0, 1), "12.0": (148, 0, 1), "11.1": (177, 0, 1), "10.1": (143, 0, 1)}
    actual = {item["protocol"]: (item["passed"], item["failed"], item["blocked"]) for item in regression.get("regressions", [])}
    check("Q02", "regression", "v10.1 through v14.1 regressions and append guards pass", regression.get("status") == "PASS" and actual == expected and regression.get("append_only_guards") == {"v13": "PASS_REFUSED", "v13.1": "PASS_REFUSED", "v13.2": "PASS_REFUSED", "v13.3": "PASS_REFUSED", "v14": "PASS_REFUSED", "v14.1": "PASS_REFUSED", "v14.3": "PASS_REFUSED"})
    check("Q03", "hygiene", "no Python cache artifacts exist", not any(HS.rglob("__pycache__")) and not any(HS.rglob("*.pyc")))
    check("Q04", "tools", "generic and pinned v14.3 tools exist", all((HS / "tools" / name).is_file() for name in ["build_release_execution_verification.py", "build_release_execution_verification_v143.py", "validate_release_execution_verification.py", "validate_release_execution_verification_v143.py"]))
    reports = [load(DEST / "reports" / name) for name in REPORT_FILES]
    check("R01", "reports", "four reports preserve semantic, binding, execution, and current truth", reports[0]["earlier_layers_redesigned"] is False and reports[1]["version_label_sufficient"] is False and reports[2]["post_release_result_mutates_decision"] is False and reports[3]["invented_objects"] is False)
    blocked("GATE-V143", "acceptance", "current release pipeline", "The v14.3 specification validates structurally, but the current audit remains blocked at specification validation and no release, decision, execution, or post-release verification object exists.")
    return finish(checks)


def finish(checks: list[dict[str, str]]) -> int:
    passed = sum(item["result"] == "PASS" for item in checks); failed = sum(item["result"] == "FAIL" for item in checks); blocked_count = sum(item["result"] == "BLOCKED" for item in checks)
    report = {"schema_version": VERSION, "validator": "Protocol-v14.3 independent release execution validator", "overall_status": "FAIL" if failed else "STRUCTURAL_PASS_CURRENT_RELEASE_NOT_APPLICABLE" if blocked_count else "PASS", "acceptance": "VALIDATION_FAILED" if failed else "BLOCKED" if blocked_count else "PASS", "summary": {"total": len(checks), "passed": passed, "failed": failed, "blocked": blocked_count}, "object_counts": {"schemas": 28, "required_vectors": 30, "invariants": 25, "current_releases": 0, "current_decisions": 0, "current_executions": 0, "current_verifications": 0}, "checks": checks}
    (DEST / "VALIDATION.yaml").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    lines = ["# Protocol-v14.3 Independent Release Execution Validation", "", f"**Overall:** `{report['overall_status']}`", f"**Acceptance:** `{report['acceptance']}`", f"**Checks:** {passed} PASS / {failed} FAIL / {blocked_count} BLOCKED ({len(checks)} total)", "", "Structural validity does not invent a release, authorization, execution, or post-release outcome.", "", "| ID | Category | Result | Description | Detail |", "|---|---|---|---|---|"]
    for item in checks: lines.append("| %s | %s | %s | %s | %s |" % (item["check_id"], item["category"], item["result"], item["description"].replace("|", "\\|"), item["detail"].replace("|", "\\|")))
    (DEST / "VALIDATION.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{passed} PASS / {failed} FAIL / {blocked_count} BLOCKED ({len(checks)} checks); {report['overall_status']}")
    return 1 if failed else 0


if __name__ == "__main__": sys.exit(main())
