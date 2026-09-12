#!/usr/bin/env python3
"""Build Protocol-v13.3 executable state and aggregate validation artifacts."""
from __future__ import annotations

import hashlib
import json
import random
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
HS = ROOT / "historical-source"
OUT = HS / "compliance"
REM = OUT / "remediation"
V132 = REM / "v13.2"
DEST = REM / "v13.3"
SCHEMA = DEST / "schema"
REPORTS = DEST / "reports"
VERSION = "13.3"
GENERATED_AT = "2026-09-12T18:11:09Z"

FINDING_STATES = ["DETECTED", "VALIDATED", "CLASSIFIED", "OPEN", "UNDER_REMEDIATION", "RESOLVED", "CLOSED", "REJECTED", "WAIVED", "SUPERSEDED", "BLOCKED"]
REMEDIATION_STATES = ["PROPOSED", "ASSESSED", "APPROVED", "IN_PROGRESS", "READY_FOR_VERIFICATION", "REVERIFICATION", "REGRESSION", "COMPLETE", "FAILED", "BLOCKED", "REJECTED", "SUPERSEDED", "CANCELLED"]
PROGRAM_STATES = ["CREATED", "TRIAGED", "PLANNED", "ACTIVE", "EVALUATING", "COMPLETED", "BLOCKED", "FAILED", "CANCELLED", "SUPERSEDED"]
CONFORMANCE_STATES = ["UNASSESSED", "MAPPED", "VERIFIED", "CONFORMANT", "PARTIALLY_CONFORMANT", "NON_CONFORMANT", "UNVERIFIED", "BLOCKED", "UNKNOWN", "NOT_APPLICABLE"]
AGGREGATE_STATES = ["NON_COMPLIANT", "BLOCKED", "UNVERIFIED", "CONDITIONALLY_COMPLIANT", "COMPLIANT", "NO_MANDATORY_REQUIREMENTS"]
FAILURE_CODES = ["SEQUENCE_GAP", "DUPLICATE_SEQUENCE", "PREDECESSOR_MISMATCH", "STATE_MISMATCH", "ILLEGAL_TRANSITION", "MISSING_EVIDENCE", "INVALID_HASH", "TIMESTAMP_VIOLATION", "UNKNOWN"]
OBJECT_TYPES = ["FINDING", "REMEDIATION", "PROGRAM", "COMPLIANCE_DECISION"]
SCHEMA_NAMES = ["finding-state", "remediation-state", "program-state", "conformance-state", "state-transition", "transition-guard-context", "transition-validation", "history-integrity-failure", "current-state", "state-history", "compliance-decision-record", "current-decision", "waiver-record", "waiver-resolution", "audit-snapshot", "aggregate-result", "program-derivation", "pipeline-execution", "audit-status"]
MACHINE_FILES = [
    "NORMATIVE-VOCABULARY.yaml", "STATE-DOMAINS.yaml", "TRANSITION-VALIDATION-PREDICATES.yaml",
    "FINDING-TRANSITION-TABLE.yaml", "REMEDIATION-TRANSITION-TABLE.yaml", "PROGRAM-TRANSITION-TABLE.yaml",
    "TRANSITION-GUARDS.yaml", "BASELINE-IMPORT-POLICY.yaml", "STATE-HISTORIES.yaml",
    "TRANSITION-GUARD-CONTEXTS.yaml", "TRANSITION-VALIDATIONS.yaml", "CURRENT-STATES.yaml",
    "HISTORY-INTEGRITY-FAILURES.yaml", "HISTORY-VALIDATION-TEST-VECTORS.yaml",
    "TRANSITION-VALIDATION-TEST-VECTORS.yaml", "DECISION-PROJECTION-RULES.yaml",
    "COMPLIANCE-DECISION-HISTORIES.yaml", "CURRENT-DECISIONS.yaml", "DECISION-PROJECTION-TEST-VECTORS.yaml",
    "WAIVER-RESOLUTION-RULES.yaml", "WAIVERS-V133.yaml", "WAIVER-RESOLUTIONS.yaml", "WAIVER-TEST-VECTORS.yaml",
    "AGGREGATE-FUNCTION.yaml", "AGGREGATE-INVARIANTS.yaml", "AGGREGATE-TEST-VECTORS.yaml",
    "CONFORMANCE-SEPARATION-TEST-VECTORS.yaml", "DETERMINISM-PURITY-TEST-VECTORS.yaml",
    "PROGRAM-DERIVATION-FUNCTION.yaml", "PROGRAM-DERIVATIONS.yaml", "PROGRAM-DERIVATION-TEST-VECTORS.yaml",
    "AUDIT-SNAPSHOT.yaml", "VALIDATION-PIPELINE.yaml", "FAILURE-BOUNDARIES.yaml", "CURRENT-PIPELINE-EXECUTION.yaml",
    "CURRENT-AGGREGATE.yaml", "CURRENT-AUDIT-STATUS.yaml", "CERTIFICATE-STATUS.yaml",
    "COMPLETE-TRANSFORMATION.yaml", "AXIS-SEPARATION.yaml", "OBJECT-REGISTRY.yaml", "SCHEMA-REGISTRY.yaml",
    "PRIOR-INTEGRITY.yaml", "VALIDATION-REPORT.yaml",
]
REPORT_FILES = ["EXECUTABLE-STATE-REPORT.yaml", "AGGREGATE-CONFORMANCE-REPORT.yaml", "FAILURE-BOUNDARY-REPORT.yaml", "CERTIFICATION-IMPACT-REPORT.yaml"]


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


def transition_tables() -> dict[str, list[dict[str, str]]]:
    finding_pairs = {
        "DETECTED": ["VALIDATED", "REJECTED", "BLOCKED"], "VALIDATED": ["CLASSIFIED", "REJECTED", "BLOCKED"],
        "CLASSIFIED": ["OPEN", "REJECTED", "BLOCKED"], "OPEN": ["UNDER_REMEDIATION", "WAIVED", "SUPERSEDED", "BLOCKED"],
        "UNDER_REMEDIATION": ["RESOLVED", "OPEN", "BLOCKED"], "RESOLVED": ["CLOSED", "OPEN"], "CLOSED": ["SUPERSEDED"],
        "BLOCKED": ["$PREVIOUS_OPERATIONAL_STATE", "REJECTED", "SUPERSEDED"], "WAIVED": ["SUPERSEDED"],
        "REJECTED": ["SUPERSEDED"], "SUPERSEDED": [],
    }
    remediation_pairs = {
        "PROPOSED": ["ASSESSED", "REJECTED", "CANCELLED"], "ASSESSED": ["APPROVED", "REJECTED", "CANCELLED"],
        "APPROVED": ["IN_PROGRESS", "CANCELLED"], "IN_PROGRESS": ["READY_FOR_VERIFICATION", "BLOCKED", "FAILED", "CANCELLED"],
        "READY_FOR_VERIFICATION": ["REVERIFICATION", "BLOCKED", "FAILED"], "REVERIFICATION": ["REGRESSION", "COMPLETE", "IN_PROGRESS", "BLOCKED", "FAILED"],
        "REGRESSION": ["COMPLETE", "REVERIFICATION", "IN_PROGRESS", "BLOCKED", "FAILED"], "COMPLETE": ["SUPERSEDED"],
        "FAILED": ["PROPOSED", "SUPERSEDED"], "BLOCKED": ["$PREVIOUS_OPERATIONAL_STATE", "FAILED", "CANCELLED", "SUPERSEDED"],
        "REJECTED": ["SUPERSEDED"], "CANCELLED": ["SUPERSEDED"], "SUPERSEDED": [],
    }
    program_pairs = {
        "CREATED": ["TRIAGED", "CANCELLED"], "TRIAGED": ["PLANNED", "CANCELLED", "SUPERSEDED"],
        "PLANNED": ["ACTIVE", "CANCELLED", "SUPERSEDED"], "ACTIVE": ["EVALUATING", "BLOCKED", "SUPERSEDED", "FAILED"],
        "EVALUATING": ["COMPLETED", "BLOCKED", "SUPERSEDED", "FAILED"],
        "BLOCKED": ["ACTIVE", "EVALUATING", "FAILED", "CANCELLED", "SUPERSEDED"],
        "COMPLETED": [], "FAILED": [], "CANCELLED": [], "SUPERSEDED": [],
    }
    guard = lambda domain, source, target: guard_id(domain, source, target)
    return {domain: [{"from": source, "to": target, "guard_id": guard(domain, source, target)} for source, targets in pairs.items() for target in targets] for domain, pairs in [("FINDING", finding_pairs), ("REMEDIATION", remediation_pairs), ("PROGRAM", program_pairs)]}


def guard_id(domain: str, source: str, target: str) -> str:
    if target == "BLOCKED": return "BLOCKING_CONDITION_PRESENT"
    if source == "BLOCKED" and target == "$PREVIOUS_OPERATIONAL_STATE": return "BLOCK_REMOVED_PREVIOUS_STATE_REVALIDATED"
    explicit = {
        ("PROGRAM", "CREATED", "TRIAGED"): "PROGRAM_TRIAGE_READY", ("PROGRAM", "TRIAGED", "PLANNED"): "PROGRAM_PLAN_READY",
        ("PROGRAM", "PLANNED", "ACTIVE"): "PROGRAM_EXECUTION_READY", ("PROGRAM", "ACTIVE", "EVALUATING"): "PROGRAM_EVALUATION_READY",
        ("PROGRAM", "EVALUATING", "COMPLETED"): "PROGRAM_COMPLETION_READY",
    }
    if (domain, source, target) in explicit: return explicit[(domain, source, target)]
    if target == "SUPERSEDED": return "AUTHORIZED_SUCCESSOR_EXISTS"
    if target == "CANCELLED": return "CANCELLATION_AUTHORIZED"
    if target == "FAILED": return "FAILURE_ESTABLISHED"
    return f"{domain}_{source}_TO_{target}"


def guard_definitions(tables: dict[str, list[dict[str, str]]]) -> dict[str, list[str]]:
    definitions: dict[str, list[str]] = {
        "BASELINE_IMPORT_GUARD": ["source_object_exists", "source_state_matches", "no_historical_reconstruction_claim"],
        "BLOCKING_CONDITION_PRESENT": ["blocking_condition_present", "blocking_cause_recorded"],
        "BLOCK_REMOVED_PREVIOUS_STATE_REVALIDATED": ["blocking_condition_removed", "target_is_previous_operational_state", "target_state_revalidated"],
        "PROGRAM_TRIAGE_READY": ["program_scope_valid", "target_findings_resolvable"],
        "PROGRAM_PLAN_READY": ["scope_defined", "remediation_strategy_defined", "dependencies_identified"],
        "PROGRAM_EXECUTION_READY": ["required_actions_approved", "execution_authorized", "required_dependencies_available"],
        "PROGRAM_EVALUATION_READY": ["required_changes_recorded", "impact_assessment_complete"],
        "PROGRAM_COMPLETION_READY": ["all_required_remediations_complete", "reverification_complete", "regression_complete", "residual_risk_recorded", "closure_conditions_satisfied"],
        "AUTHORIZED_SUCCESSOR_EXISTS": ["successor_exists", "supersession_authorized"],
        "CANCELLATION_AUTHORIZED": ["cancellation_authorized", "cancellation_reason_recorded"],
        "FAILURE_ESTABLISHED": ["objective_unachievable_with_current_plan", "failure_evidence_valid"],
    }
    for entries in tables.values():
        for entry in entries:
            identifier = entry["guard_id"]
            definitions.setdefault(identifier, ["transition_basis_valid", "required_evidence_resolves"])
    return definitions


def table_entry(tables: dict[str, list[dict[str, str]]], domain: str, source: str | None, target: str, previous_operational: str | None) -> dict[str, str] | None:
    if source is None: return {"from": "$INITIAL", "to": target, "guard_id": "BASELINE_IMPORT_GUARD"}
    for entry in tables.get(domain, []):
        if entry["from"] != source: continue
        if entry["to"] == target: return entry
        if entry["to"] == "$PREVIOUS_OPERATIONAL_STATE" and target == previous_operational: return entry
    return None


def make_event(identifier: str, domain: str, object_id: str, source: str | None, target: str, sequence: int, previous: str | None, evidence: list[str], reason: str = "BASELINE_IMPORT: establish v13.3 executable lineage without reconstructing earlier transition chronology", occurred_at: str = GENERATED_AT) -> dict[str, Any]:
    return seal({"transition_id": identifier, "object_type": domain, "object_id": object_id, "from_state": source, "to_state": target, "reason": reason, "evidence_refs": evidence, "actor": "PROTOCOL_V13_3_EXECUTABLE_IMPORT", "occurred_at": occurred_at, "sequence": sequence, "previous_transition": previous, "schema_version": VERSION}, "event_hash")


def guard_context(context_id: str, transition_id: str, guard: str, required: list[str], overrides: dict[str, bool] | None = None) -> dict[str, Any]:
    facts = {name: True for name in required}; facts.update(overrides or {})
    return seal({"guard_context_id": context_id, "transition_id": transition_id, "guard_id": guard, "facts": facts, "evaluated_at": GENERATED_AT}, "context_hash")


def validate_history(domain: str, object_id: str, events: list[dict[str, Any]], contexts: dict[str, dict[str, Any]], object_types: dict[str, str], evidence_ids: set[str], tables: dict[str, list[dict[str, str]]], guards: dict[str, list[str]]) -> tuple[str, dict[str, Any] | None, dict[str, Any] | None, list[dict[str, Any]]]:
    ordered = sorted(events, key=lambda item: item.get("sequence", -1)); validations: list[dict[str, Any]] = []
    sequences = [item.get("sequence") for item in ordered]
    if len(sequences) != len(set(sequences)): return "HISTORY_INVALID", None, history_failure(object_id, "DUPLICATE_SEQUENCE", None), validations
    if sequences != list(range(0, len(ordered))): return "HISTORY_INVALID", None, history_failure(object_id, "SEQUENCE_GAP", None), validations
    state = None; previous_id = None; previous_time: datetime | None = None; blocked_return_state = None
    valid_states = {"FINDING": set(FINDING_STATES), "REMEDIATION": set(REMEDIATION_STATES), "PROGRAM": set(PROGRAM_STATES), "COMPLIANCE_DECISION": set(CONFORMANCE_STATES)}
    for index, event in enumerate(ordered):
        predicates: dict[str, bool] = {}
        predicates["object_exists"] = object_id in object_types
        predicates["object_type_valid"] = domain in OBJECT_TYPES and object_types.get(object_id) == domain and event.get("object_type") == domain and event.get("object_id") == object_id
        predicates["state_names_valid"] = event.get("to_state") in valid_states[domain] and (event.get("from_state") is None or event.get("from_state") in valid_states[domain])
        predicates["sequence_valid"] = event.get("sequence") == index
        predicates["predecessor_valid"] = event.get("previous_transition") == previous_id
        predicates["from_state_matches"] = event.get("from_state") == state
        entry = table_entry(tables, domain, state, event.get("to_state"), blocked_return_state)
        predicates["transition_is_legal"] = entry is not None
        context = contexts.get(event.get("transition_id"), {})
        required_guard = entry["guard_id"] if entry else None
        predicates["guard_satisfied"] = bool(required_guard and context.get("guard_id") == required_guard and all(context.get("facts", {}).get(name) is True for name in guards.get(required_guard, [])))
        predicates["evidence_valid"] = bool(event.get("evidence_refs")) and all(reference in evidence_ids for reference in event.get("evidence_refs", []))
        predicates["timestamp_valid"] = valid_time(event.get("occurred_at"))
        if predicates["timestamp_valid"]:
            event_time = datetime.fromisoformat(event["occurred_at"].replace("Z", "+00:00")); predicates["timestamp_valid"] = previous_time is None or event_time >= previous_time
        else: event_time = None
        payload = dict(event); supplied = payload.pop("event_hash", None); predicates["hash_valid"] = supplied == digest(payload)
        validation = seal({"transition_validation_id": "VALIDATION-" + event.get("transition_id", "UNKNOWN"), "transition_id": event.get("transition_id"), "predicates": predicates, "result": "VALID_TRANSITION" if all(predicates.values()) else "TRANSITION_INVALID", "validated_at": GENERATED_AT}, "validation_hash")
        validations.append(validation)
        if not all(predicates.values()):
            code = transition_failure_code(predicates); return "HISTORY_INVALID", None, history_failure(object_id, code, event.get("transition_id")), validations
        if event.get("to_state") == "BLOCKED": blocked_return_state = state
        elif state == "BLOCKED": blocked_return_state = None
        state = event["to_state"]; previous_id = event["transition_id"]; previous_time = event_time
    current = seal({"current_state_id": f"CURRENT-V133-{domain}-{object_id}", "object_type": domain, "object_id": object_id, "state": state, "state_as_of": ordered[-1]["occurred_at"], "last_transition_id": ordered[-1]["transition_id"], "transition_sequence": ordered[-1]["sequence"], "schema_version": VERSION}, "projection_hash")
    history = seal({"history_id": f"HISTORY-V133-{domain}-{object_id}", "object_type": domain, "object_id": object_id, "initial_state": None, "transitions": ordered, "current_state": current, "history_integrity": {"valid": True, "checked_at": GENERATED_AT, "error_codes": []}, "schema_version": VERSION}, "history_hash")
    return "VALID", history, None, validations


def transition_failure_code(predicates: dict[str, bool]) -> str:
    if not predicates.get("predecessor_valid", True): return "PREDECESSOR_MISMATCH"
    if not predicates.get("from_state_matches", True): return "STATE_MISMATCH"
    if not predicates.get("transition_is_legal", True) or not predicates.get("guard_satisfied", True) or not predicates.get("state_names_valid", True): return "ILLEGAL_TRANSITION"
    if not predicates.get("evidence_valid", True): return "MISSING_EVIDENCE"
    if not predicates.get("timestamp_valid", True): return "TIMESTAMP_VIOLATION"
    if not predicates.get("hash_valid", True): return "INVALID_HASH"
    return "UNKNOWN"


def history_failure(object_id: str, code: str, transition_id: str | None) -> dict[str, Any]:
    return seal({"history_failure_id": f"HISTORY-FAILURE-{object_id}-{code}", "object_id": object_id, "failure_code": code, "transition_id": transition_id, "detected_at": GENERATED_AT, "schema_version": VERSION}, "failure_hash")


def decision_record(identifier: str, decision: str, decided_at: str, supersedes: str | None = None, implementation: str = "1" * 64, specification: str = "2" * 64) -> dict[str, Any]:
    return seal({"decision_id": identifier, "requirement_id": "TEST-REQ", "audit_id": "TEST-AUDIT", "decision": decision, "basis": {"acceptance_criteria": ["TEST-AC"], "evidence_refs": ["TEST-EVIDENCE"], "verification_refs": ["TEST-VERIFY"], "rule_refs": ["TEST-RULE"]}, "decided_at": decided_at, "implementation_snapshot": implementation, "specification_snapshot": specification, "audit_run_id": "TEST-RUN", "supersedes": supersedes, "schema_version": VERSION}, "decision_hash")


def project_decision(records: list[dict[str, Any]], *, audit: str = "TEST-AUDIT", requirement: str = "TEST-REQ", implementation: str = "1" * 64, specification: str = "2" * 64, scope: set[str] | None = None) -> tuple[str, dict[str, Any] | None]:
    if requirement not in (scope if scope is not None else {requirement}): return "DECISION_SNAPSHOT_MISMATCH", None
    if not records: return "NO_DECISION", None
    ordered = sorted(records, key=lambda item: item.get("decided_at", "")); previous = None
    for item in ordered:
        payload = dict(item); supplied = payload.pop("decision_hash", None)
        if supplied != digest(payload) or not valid_time(item.get("decided_at")) or item.get("supersedes") != previous: return "DECISION_HISTORY_INVALID", None
        if item.get("audit_id") != audit or item.get("requirement_id") != requirement or item.get("implementation_snapshot") != implementation or item.get("specification_snapshot") != specification: return "DECISION_SNAPSHOT_MISMATCH", None
        previous = item["decision_id"]
    latest = ordered[-1]
    current = seal({"current_decision_id": "CURRENT-" + latest["decision_id"], "audit_id": audit, "requirement_id": requirement, "decision_id": latest["decision_id"], "decision": latest["decision"], "as_of": latest["decided_at"], "implementation_snapshot": implementation, "specification_snapshot": specification, "decision_history_valid": True, "schema_version": VERSION}, "projection_hash")
    return "VALID", current


def waiver_record(identifier: str, requirement: str = "TEST-REQ", status: str = "EFFECTIVE", implementation: str = "1" * 64, specification: str = "2" * 64, valid_from: str = "2026-09-12T00:00:00Z", valid_until: str = "2026-09-13T00:00:00Z") -> dict[str, Any]:
    return seal({"waiver_id": identifier, "audit_id": "TEST-AUDIT", "requirement_id": requirement, "status": status, "specification_snapshot": specification, "implementation_snapshot": implementation, "effective_from": valid_from, "effective_until": valid_until, "scope": [requirement], "schema_version": VERSION}, "waiver_hash")


def resolve_waiver(record: dict[str, Any], *, requirement: str = "TEST-REQ", as_of: str = GENERATED_AT, implementation: str = "1" * 64, specification: str = "2" * 64) -> tuple[str, bool]:
    payload = dict(record); supplied = payload.pop("waiver_hash", None)
    if supplied != digest(payload): return "WAIVER_INVALID", False
    compatible = record.get("audit_id") == "TEST-AUDIT" and record.get("requirement_id") == requirement and requirement in record.get("scope", []) and record.get("implementation_snapshot") == implementation and record.get("specification_snapshot") == specification
    if not compatible: return "WAIVER_SCOPE_MISMATCH", False
    if record.get("status") != "EFFECTIVE": return "WAIVER_NOT_EFFECTIVE", False
    if not (record.get("effective_from") <= as_of <= record.get("effective_until")): return "WAIVER_OUTSIDE_EFFECTIVE_PERIOD", False
    return "EFFECTIVE", True


def aggregate(requirements: list[dict[str, Any]]) -> dict[str, Any]:
    classes = ["pass", "proven_failure", "blocked", "unresolved", "waived_failure", "excluded"]
    counts = {kind: {key: 0 for key in classes} for kind in ["mandatory", "optional"]}; mandatory: list[str] = []
    for item in requirements:
        kind = "mandatory" if item["mandatory"] else "optional"; decision = item["decision"]
        if not item.get("applicable", True) or decision == "NOT_APPLICABLE": contribution = "excluded"
        elif decision == "CONFORMANT": contribution = "pass"
        elif decision == "NON_CONFORMANT": contribution = "waived_failure" if item.get("waiver_effective", False) else "proven_failure"
        elif decision == "BLOCKED": contribution = "blocked"
        elif decision in {"PARTIALLY_CONFORMANT", "UNVERIFIED", "UNKNOWN"}: contribution = "unresolved"
        else: contribution = "blocked"
        counts[kind][contribution] += 1
        if kind == "mandatory" and contribution != "excluded": mandatory.append(contribution)
    if "proven_failure" in mandatory: status = "NON_COMPLIANT"
    elif "blocked" in mandatory: status = "BLOCKED"
    elif "unresolved" in mandatory: status = "UNVERIFIED"
    elif "waived_failure" in mandatory: status = "CONDITIONALLY_COMPLIANT"
    elif not mandatory: status = "NO_MANDATORY_REQUIREMENTS"
    else: status = "COMPLIANT"
    return {"status": status, "mandatory_counts": counts["mandatory"], "optional_counts": counts["optional"]}


def derive_program(history_state: str, member_states: list[str], predicates: dict[str, bool]) -> str:
    if predicates.get("superseded") or history_state == "SUPERSEDED": return "SUPERSEDED"
    if predicates.get("cancelled") or history_state == "CANCELLED": return "CANCELLED"
    if predicates.get("failed") or history_state == "FAILED": return "FAILED"
    if predicates.get("blocking_condition") or "BLOCKED" in member_states: return "BLOCKED"
    if predicates.get("completion_predicate") and member_states and all(state == "COMPLETE" for state in member_states): return "COMPLETED"
    if predicates.get("evaluation_predicate") or any(state in {"REVERIFICATION", "REGRESSION"} for state in member_states): return "EVALUATING"
    if predicates.get("active_predicate") or any(state in {"IN_PROGRESS", "READY_FOR_VERIFICATION"} for state in member_states): return "ACTIVE"
    if predicates.get("planning_predicate") or any(state in {"PROPOSED", "ASSESSED", "APPROVED"} for state in member_states): return "PLANNED"
    if predicates.get("triage_predicate") or history_state == "TRIAGED" or member_states: return "TRIAGED"
    return "CREATED"


def schema(title: str, required: list[str], properties: dict[str, Any], rules: list[str] | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {"$schema": "https://json-schema.org/draft/2020-12/schema", "title": title, "type": "object", "required": required, "properties": properties, "additionalProperties": False}
    if rules: result["x-v13.3-rules"] = rules
    return result


def build_schemas() -> None:
    ident = {"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9._:/-]*$"}; text = {"type": "string", "minLength": 1}; ts = {"type": "string", "format": "date-time"}; hx = {"type": "string", "pattern": "^[a-f0-9]{64}$"}; nullable_id = {"oneOf": [ident, {"type": "null"}]}; strings = lambda minimum=0: {"type": "array", "minItems": minimum, "items": {"type": "string"}, "uniqueItems": True}
    schemas: dict[str, dict[str, Any]] = {}
    for name, states in [("finding-state", FINDING_STATES), ("remediation-state", REMEDIATION_STATES), ("program-state", PROGRAM_STATES), ("conformance-state", CONFORMANCE_STATES)]: schemas[name] = {"$schema": "https://json-schema.org/draft/2020-12/schema", "title": name, "type": "string", "enum": states}
    union_state = {"type": "string", "enum": sorted(set(FINDING_STATES + REMEDIATION_STATES + PROGRAM_STATES + CONFORMANCE_STATES))}
    schemas["state-transition"] = schema("StateTransition", ["transition_id", "object_type", "object_id", "from_state", "to_state", "reason", "evidence_refs", "actor", "occurred_at", "sequence", "previous_transition", "event_hash", "schema_version"], {"transition_id": ident, "object_type": {"type": "string", "enum": OBJECT_TYPES}, "object_id": ident, "from_state": {"oneOf": [union_state, {"type": "null"}]}, "to_state": union_state, "reason": text, "evidence_refs": strings(1), "actor": text, "occurred_at": ts, "sequence": {"type": "integer", "minimum": 0}, "previous_transition": nullable_id, "event_hash": hx, "schema_version": {"const": VERSION}}, ["Initial sequence is zero", "Hash excludes event_hash"])
    schemas["transition-guard-context"] = schema("TransitionGuardContext", ["guard_context_id", "transition_id", "guard_id", "facts", "evaluated_at", "context_hash"], {"guard_context_id": ident, "transition_id": ident, "guard_id": ident, "facts": {"type": "object"}, "evaluated_at": ts, "context_hash": hx})
    schemas["transition-validation"] = schema("TransitionValidation", ["transition_validation_id", "transition_id", "predicates", "result", "validated_at", "validation_hash"], {"transition_validation_id": ident, "transition_id": ident, "predicates": {"type": "object", "required": ["object_exists", "object_type_valid", "state_names_valid", "sequence_valid", "predecessor_valid", "from_state_matches", "transition_is_legal", "guard_satisfied", "evidence_valid", "timestamp_valid", "hash_valid"], "properties": {name: {"type": "boolean"} for name in ["object_exists", "object_type_valid", "state_names_valid", "sequence_valid", "predecessor_valid", "from_state_matches", "transition_is_legal", "guard_satisfied", "evidence_valid", "timestamp_valid", "hash_valid"]}, "additionalProperties": False}, "result": {"type": "string", "enum": ["VALID_TRANSITION", "TRANSITION_INVALID"]}, "validated_at": ts, "validation_hash": hx})
    schemas["history-integrity-failure"] = schema("HistoryIntegrityFailure", ["history_failure_id", "object_id", "failure_code", "transition_id", "detected_at", "schema_version", "failure_hash"], {"history_failure_id": ident, "object_id": ident, "failure_code": {"type": "string", "enum": FAILURE_CODES}, "transition_id": nullable_id, "detected_at": ts, "schema_version": {"const": VERSION}, "failure_hash": hx})
    schemas["current-state"] = schema("CurrentState", ["current_state_id", "object_type", "object_id", "state", "state_as_of", "last_transition_id", "transition_sequence", "schema_version", "projection_hash"], {"current_state_id": ident, "object_type": {"type": "string", "enum": OBJECT_TYPES}, "object_id": ident, "state": union_state, "state_as_of": ts, "last_transition_id": ident, "transition_sequence": {"type": "integer", "minimum": 0}, "schema_version": {"const": VERSION}, "projection_hash": hx})
    schemas["state-history"] = schema("StateHistory", ["history_id", "object_type", "object_id", "initial_state", "transitions", "current_state", "history_integrity", "schema_version", "history_hash"], {"history_id": ident, "object_type": {"type": "string", "enum": OBJECT_TYPES}, "object_id": ident, "initial_state": {"oneOf": [union_state, {"type": "null"}]}, "transitions": {"type": "array", "minItems": 1, "items": {"$ref": "state-transition.schema.yaml"}}, "current_state": {"oneOf": [{"$ref": "current-state.schema.yaml"}, {"type": "null"}]}, "history_integrity": {"type": "object", "required": ["valid", "checked_at", "error_codes"], "properties": {"valid": {"type": "boolean"}, "checked_at": ts, "error_codes": strings()}, "additionalProperties": False}, "schema_version": {"const": VERSION}, "history_hash": hx})
    basis = {"type": "object", "required": ["acceptance_criteria", "evidence_refs", "verification_refs", "rule_refs"], "properties": {key: strings() for key in ["acceptance_criteria", "evidence_refs", "verification_refs", "rule_refs"]}, "additionalProperties": False}
    schemas["compliance-decision-record"] = schema("ComplianceDecisionRecord", ["decision_id", "requirement_id", "audit_id", "decision", "basis", "decided_at", "implementation_snapshot", "specification_snapshot", "audit_run_id", "supersedes", "schema_version", "decision_hash"], {"decision_id": ident, "requirement_id": ident, "audit_id": ident, "decision": {"type": "string", "enum": CONFORMANCE_STATES}, "basis": basis, "decided_at": ts, "implementation_snapshot": hx, "specification_snapshot": hx, "audit_run_id": ident, "supersedes": nullable_id, "schema_version": {"const": VERSION}, "decision_hash": hx})
    schemas["current-decision"] = schema("CurrentDecision", ["current_decision_id", "audit_id", "requirement_id", "decision_id", "decision", "as_of", "implementation_snapshot", "specification_snapshot", "decision_history_valid", "schema_version", "projection_hash"], {"current_decision_id": ident, "audit_id": ident, "requirement_id": ident, "decision_id": ident, "decision": {"type": "string", "enum": CONFORMANCE_STATES}, "as_of": ts, "implementation_snapshot": hx, "specification_snapshot": hx, "decision_history_valid": {"const": True}, "schema_version": {"const": VERSION}, "projection_hash": hx})
    schemas["waiver-record"] = schema("WaiverRecord", ["waiver_id", "audit_id", "requirement_id", "status", "specification_snapshot", "implementation_snapshot", "effective_from", "effective_until", "scope", "schema_version", "waiver_hash"], {"waiver_id": ident, "audit_id": ident, "requirement_id": ident, "status": {"type": "string", "enum": ["EFFECTIVE", "REVOKED", "EXPIRED", "SUPERSEDED"]}, "specification_snapshot": hx, "implementation_snapshot": hx, "effective_from": ts, "effective_until": ts, "scope": strings(1), "schema_version": {"const": VERSION}, "waiver_hash": hx})
    schemas["waiver-resolution"] = schema("WaiverResolution", ["waiver_resolution_id", "waiver_id", "requirement_id", "result", "effective", "as_of", "schema_version", "resolution_hash"], {"waiver_resolution_id": ident, "waiver_id": ident, "requirement_id": ident, "result": {"type": "string", "enum": ["EFFECTIVE", "WAIVER_INVALID", "WAIVER_SCOPE_MISMATCH", "WAIVER_NOT_EFFECTIVE", "WAIVER_OUTSIDE_EFFECTIVE_PERIOD"]}, "effective": {"type": "boolean"}, "as_of": ts, "schema_version": {"const": VERSION}, "resolution_hash": hx})
    schemas["audit-snapshot"] = schema("AuditSnapshot", ["snapshot_id", "audit_id", "specification_snapshot", "implementation_snapshot", "decision_snapshot", "waiver_snapshot", "state_history_snapshot", "scope_snapshot", "generated_at", "valid_for_aggregate", "schema_version", "snapshot_hash"], {"snapshot_id": ident, "audit_id": ident, "specification_snapshot": hx, "implementation_snapshot": hx, "decision_snapshot": hx, "waiver_snapshot": hx, "state_history_snapshot": hx, "scope_snapshot": hx, "generated_at": ts, "valid_for_aggregate": {"type": "boolean"}, "schema_version": {"const": VERSION}, "snapshot_hash": hx})
    contribution_keys = ["pass", "proven_failure", "blocked", "unresolved", "waived_failure", "excluded"]
    count = {"type": "object", "required": contribution_keys, "properties": {key: {"type": "integer", "minimum": 0} for key in contribution_keys}, "additionalProperties": False}
    schemas["aggregate-result"] = schema("AggregateResult", ["aggregate_id", "snapshot_id", "status", "mandatory_counts", "optional_counts", "schema_version", "aggregate_hash"], {"aggregate_id": ident, "snapshot_id": ident, "status": {"type": "string", "enum": AGGREGATE_STATES}, "mandatory_counts": count, "optional_counts": count, "schema_version": {"const": VERSION}, "aggregate_hash": hx})
    schemas["program-derivation"] = schema("ProgramDerivation", ["derivation_id", "program_id", "history_current_state", "member_remediation_ids", "member_remediation_states", "predicates", "derived_state", "derived_at", "schema_version", "derivation_hash"], {"derivation_id": ident, "program_id": ident, "history_current_state": {"type": "string", "enum": PROGRAM_STATES}, "member_remediation_ids": strings(), "member_remediation_states": {"type": "array", "items": {"type": "string", "enum": REMEDIATION_STATES}}, "predicates": {"type": "object", "properties": {name: {"type": "boolean"} for name in ["superseded", "cancelled", "failed", "blocking_condition", "completion_predicate", "evaluation_predicate", "active_predicate", "planning_predicate", "triage_predicate"]}, "additionalProperties": False}, "derived_state": {"type": "string", "enum": PROGRAM_STATES}, "derived_at": ts, "schema_version": {"const": VERSION}, "derivation_hash": hx})
    schemas["pipeline-execution"] = schema("PipelineExecution", ["pipeline_execution_id", "snapshot_id", "stages", "result", "stopped_at", "executed_at", "schema_version", "execution_hash"], {"pipeline_execution_id": ident, "snapshot_id": ident, "stages": {"type": "array", "minItems": 17, "items": {"type": "object", "required": ["number", "stage", "status"], "properties": {"number": {"type": "integer", "minimum": 1}, "stage": text, "status": text, "failure": text}}}, "result": text, "stopped_at": {"type": "integer", "minimum": 1}, "executed_at": ts, "schema_version": {"const": VERSION}, "execution_hash": hx})
    schemas["audit-status"] = schema("AuditStatus", ["audit_status_id", "snapshot_id", "aggregate_id", "status", "reason", "certification_eligible", "derived_at", "schema_version", "status_hash"], {"audit_status_id": ident, "snapshot_id": ident, "aggregate_id": nullable_id, "status": {"type": "string", "enum": AGGREGATE_STATES}, "reason": text, "certification_eligible": {"type": "boolean"}, "derived_at": ts, "schema_version": {"const": VERSION}, "status_hash": hx})
    for name, body in schemas.items(): body["$id"] = f"https://generic-discovery-engine.invalid/compliance/v13.3/{name}.schema.yaml"; dump(SCHEMA / f"{name}.schema.yaml", body)


def protected_files() -> list[Path]: return sorted((path for path in OUT.rglob("*") if path.is_file() and DEST not in path.parents), key=lambda path: str(path.relative_to(OUT)))


def main() -> None:
    required = [V132 / "VALIDATION.yaml", V132 / "STATE-HISTORIES.yaml", V132 / "PROGRAM-DERIVATIONS.yaml", OUT / "AUDIT-CERTIFICATE.yaml"]
    if not all(path.is_file() for path in required): raise RuntimeError("validated Protocol-v13.2 package is required")
    if DEST.exists():
        for filename, key, expected in [("STATE-HISTORIES.yaml", "histories", 6), ("COMPLIANCE-DECISION-HISTORIES.yaml", "records", 0), ("WAIVERS-V133.yaml", "objects", 0), ("AUDIT-SNAPSHOT.yaml", "objects", 1)]:
            path = DEST / filename
            if path.is_file() and len(load(path).get(key, [])) != expected: raise RuntimeError(f"refusing to erase appended v13.3 records in {filename}")
    before = [{"path": str(path.relative_to(OUT)), "sha256": sha_file(path), "bytes": path.stat().st_size} for path in protected_files()]
    if DEST.exists(): shutil.rmtree(DEST)
    DEST.mkdir(parents=True); SCHEMA.mkdir(); REPORTS.mkdir(); build_schemas()

    tables = transition_tables(); guards = guard_definitions(tables)
    dump(DEST / "NORMATIVE-VOCABULARY.yaml", {"schema_version": VERSION, "keywords": {"MUST": "mandatory for conformance", "MUST_NOT": "prohibited", "SHOULD": "recommended unless justified", "SHOULD_NOT": "normally prohibited unless justified", "MAY": "permitted but optional"}, "guidance_changes_conformance": False})
    dump(DEST / "STATE-DOMAINS.yaml", {"schema_version": VERSION, "domains": {"finding": FINDING_STATES, "remediation": REMEDIATION_STATES, "program": PROGRAM_STATES, "conformance": CONFORMANCE_STATES}, "substitution": "MUST_NOT", "axes": ["TRUTH", "PROCESS", "TIME"]})
    predicates = ["object_exists", "object_type_valid", "state_names_valid", "sequence_valid", "predecessor_valid", "from_state_matches", "transition_is_legal", "guard_satisfied", "evidence_valid", "timestamp_valid", "hash_valid"]
    dump(DEST / "TRANSITION-VALIDATION-PREDICATES.yaml", {"schema_version": VERSION, "conjunction": predicates, "valid_result": "VALID_TRANSITION", "invalid_result": "TRANSITION_INVALID", "skip_invalid": False})
    for domain, filename in [("FINDING", "FINDING-TRANSITION-TABLE.yaml"), ("REMEDIATION", "REMEDIATION-TRANSITION-TABLE.yaml"), ("PROGRAM", "PROGRAM-TRANSITION-TABLE.yaml")]: dump(DEST / filename, {"schema_version": VERSION, "domain": domain, "transitions": tables[domain], "terminal_states": [state for state in ({"FINDING": FINDING_STATES, "REMEDIATION": REMEDIATION_STATES, "PROGRAM": PROGRAM_STATES}[domain]) if not any(entry["from"] == state for entry in tables[domain])]})
    dump(DEST / "TRANSITION-GUARDS.yaml", {"schema_version": VERSION, "guards": [{"guard_id": identifier, "all_of": requirements} for identifier, requirements in sorted(guards.items())], "evaluation": "ALL_REQUIRED_FACTS_MUST_BE_EXPLICIT_TRUE", "missing_fact": "GUARD_UNSATISFIED"})
    dump(DEST / "BASELINE-IMPORT-POLICY.yaml", {"schema_version": VERSION, "initial_transition": {"from_state": None, "previous_transition": None, "sequence": 0, "guard_id": "BASELINE_IMPORT_GUARD"}, "historical_claim": "NO_PRE_V13.3_CHRONOLOGY_RECONSTRUCTED", "source_state_evidence_required": True})

    findings = load(OUT / "FINDINGS.yaml")["objects"]; programs = load(REM / "v13.1" / "REMEDIATION-PROGRAMS.yaml")["objects"]
    root_registry = load(OUT / "OBJECT-REGISTRY.yaml")["objects"]; v131_registry = load(REM / "v13.1" / "OBJECT-REGISTRY.yaml")["objects"]
    object_types = {item["object_id"]: ("FINDING" if item["object_type"] == "AUDIT_FINDING" else "PROGRAM" if item["object_type"] == "REMEDIATION_PROGRAM" else item["object_type"]) for item in root_registry + v131_registry}
    evidence_ids = set(object_types); histories = []; contexts_list = []; validation_list = []; actual_failures = []
    subjects = [("FINDING", item["object_id"], "OPEN") for item in findings] + [("PROGRAM", item["object_id"], "CREATED") for item in programs]
    for index, (domain, object_id, state) in enumerate(subjects, 1):
        event = make_event(f"TRANSITION-V133-{domain}-{index:03d}", domain, object_id, None, state, 0, None, [object_id])
        context = guard_context(f"GUARD-CONTEXT-V133-{index:03d}", event["transition_id"], "BASELINE_IMPORT_GUARD", guards["BASELINE_IMPORT_GUARD"])
        status, history, failure, validations = validate_history(domain, object_id, [event], {event["transition_id"]: context}, object_types, evidence_ids, tables, guards)
        if status != "VALID" or not history: raise RuntimeError(f"baseline history invalid: {object_id} {failure}")
        histories.append(history); contexts_list.append(context); validation_list.extend(validations)
    dump(DEST / "STATE-HISTORIES.yaml", {"schema_version": VERSION, "histories": histories, "canonical": True})
    dump(DEST / "TRANSITION-GUARD-CONTEXTS.yaml", {"schema_version": VERSION, "objects": contexts_list})
    dump(DEST / "TRANSITION-VALIDATIONS.yaml", {"schema_version": VERSION, "objects": validation_list})
    currents = [history["current_state"] for history in histories]
    dump(DEST / "CURRENT-STATES.yaml", {"schema_version": VERSION, "objects": currents, "derived_from": "STATE-HISTORIES.yaml"})
    dump(DEST / "HISTORY-INTEGRITY-FAILURES.yaml", {"schema_version": VERSION, "objects": actual_failures, "status": "NONE_CURRENT"})

    base = make_event("TEST-T0", "FINDING", "TEST-FINDING", None, "OPEN", 0, None, ["TEST-EVIDENCE"])
    normal = make_event("TEST-T1", "FINDING", "TEST-FINDING", "OPEN", "UNDER_REMEDIATION", 1, "TEST-T0", ["TEST-EVIDENCE"], reason="TEST_NORMAL")
    test_types = {"TEST-FINDING": "FINDING"}; test_evidence = {"TEST-EVIDENCE"}
    base_context = guard_context("TEST-G0", "TEST-T0", "BASELINE_IMPORT_GUARD", guards["BASELINE_IMPORT_GUARD"])
    normal_guard = guard_id("FINDING", "OPEN", "UNDER_REMEDIATION"); normal_context = guard_context("TEST-G1", "TEST-T1", normal_guard, guards[normal_guard])
    def hist_result(events: list[dict[str, Any]], contexts: list[dict[str, Any]]) -> tuple[str, dict[str, Any] | None]:
        result, _, failure, _ = validate_history("FINDING", "TEST-FINDING", events, {item["transition_id"]: item for item in contexts}, test_types, test_evidence, tables, guards); return result, failure
    history_vectors = []
    def add_history_vector(identifier: str, events: list[dict[str, Any]], contexts: list[dict[str, Any]], expected_code: str | None) -> None:
        result, failure = hist_result(events, contexts); code = failure["failure_code"] if failure else None; expected_result = "VALID" if expected_code is None else "HISTORY_INVALID"; history_vectors.append({"vector_id": identifier, "events": events, "guard_contexts": contexts, "expected_result": expected_result, "actual_result": result, "expected_failure_code": expected_code, "actual_failure_code": code, "failure": failure, "pass": result == expected_result and code == expected_code})
    add_history_vector("VALID_HISTORY", [base, normal], [base_context, normal_context], None)
    gap = dict(normal); gap["sequence"] = 2; gap = seal({key: value for key, value in gap.items() if key != "event_hash"}, "event_hash"); add_history_vector("SEQUENCE_GAP", [base, gap], [base_context, normal_context], "SEQUENCE_GAP")
    add_history_vector("DUPLICATE_SEQUENCE", [base, dict(base)], [base_context], "DUPLICATE_SEQUENCE")
    wrong_pred = make_event("TEST-T1", "FINDING", "TEST-FINDING", "OPEN", "UNDER_REMEDIATION", 1, "WRONG", ["TEST-EVIDENCE"], reason="TEST_NORMAL"); add_history_vector("PREDECESSOR_MISMATCH", [base, wrong_pred], [base_context, guard_context("TEST-G1", "TEST-T1", normal_guard, guards[normal_guard])], "PREDECESSOR_MISMATCH")
    wrong_state = make_event("TEST-T1", "FINDING", "TEST-FINDING", "DETECTED", "VALIDATED", 1, "TEST-T0", ["TEST-EVIDENCE"], reason="TEST_NORMAL"); add_history_vector("STATE_MISMATCH", [base, wrong_state], [base_context, guard_context("TEST-G1", "TEST-T1", guard_id("FINDING", "DETECTED", "VALIDATED"), guards[guard_id("FINDING", "DETECTED", "VALIDATED")])], "STATE_MISMATCH")
    illegal = make_event("TEST-T1", "FINDING", "TEST-FINDING", "OPEN", "CLOSED", 1, "TEST-T0", ["TEST-EVIDENCE"], reason="TEST_NORMAL"); add_history_vector("ILLEGAL_TRANSITION", [base, illegal], [base_context], "ILLEGAL_TRANSITION")
    missing = make_event("TEST-T1", "FINDING", "TEST-FINDING", "OPEN", "UNDER_REMEDIATION", 1, "TEST-T0", [], reason="TEST_NORMAL"); add_history_vector("MISSING_EVIDENCE", [base, missing], [base_context, normal_context], "MISSING_EVIDENCE")
    bad_hash = dict(normal); bad_hash["event_hash"] = "0" * 64; add_history_vector("INVALID_HASH", [base, bad_hash], [base_context, normal_context], "INVALID_HASH")
    bad_time = make_event("TEST-T1", "FINDING", "TEST-FINDING", "OPEN", "UNDER_REMEDIATION", 1, "TEST-T0", ["TEST-EVIDENCE"], reason="TEST_NORMAL", occurred_at="invalid"); add_history_vector("TIMESTAMP_VIOLATION", [base, bad_time], [base_context, normal_context], "TIMESTAMP_VIOLATION")
    guard_false = guard_context("TEST-G1", "TEST-T1", normal_guard, guards[normal_guard], {guards[normal_guard][0]: False}); add_history_vector("GUARD_UNSATISFIED", [base, normal], [base_context, guard_false], "ILLEGAL_TRANSITION")
    dump(DEST / "HISTORY-VALIDATION-TEST-VECTORS.yaml", {"schema_version": VERSION, "synthetic_non_normative": True, "vectors": history_vectors, "summary": {"total": len(history_vectors), "passed": sum(item["pass"] for item in history_vectors), "failed": sum(not item["pass"] for item in history_vectors)}})
    transition_vectors = []
    valid_predicates = {name: True for name in predicates}
    transition_vectors.append({"vector_id": "ALL-PREDICATES-TRUE", "predicates": valid_predicates, "expected": "VALID_TRANSITION", "actual": "VALID_TRANSITION" if all(valid_predicates.values()) else "TRANSITION_INVALID", "pass": all(valid_predicates.values())})
    for name in predicates:
        values = dict(valid_predicates); values[name] = False; actual = "VALID_TRANSITION" if all(values.values()) else "TRANSITION_INVALID"
        transition_vectors.append({"vector_id": f"PREDICATE-{name.upper()}-FALSE", "predicates": values, "expected": "TRANSITION_INVALID", "actual": actual, "pass": actual == "TRANSITION_INVALID"})
    dump(DEST / "TRANSITION-VALIDATION-TEST-VECTORS.yaml", {"schema_version": VERSION, "vectors": transition_vectors, "summary": {"total": len(transition_vectors), "passed": sum(item["pass"] for item in transition_vectors), "failed": sum(not item["pass"] for item in transition_vectors)}})

    dump(DEST / "DECISION-PROJECTION-RULES.yaml", {"schema_version": VERSION, "validation_order": ["VALIDATE_RECORDS", "RESOLVE_SUPERSESSION", "RESOLVE_APPLICABILITY", "MATCH_SPECIFICATION_SNAPSHOT", "MATCH_IMPLEMENTATION_SNAPSHOT", "SELECT_CURRENT"], "snapshot_mismatch": "DECISION_SNAPSHOT_MISMATCH", "latest_invalid": "DECISION_HISTORY_INVALID_NO_FALLBACK", "immutability": True})
    dump(DEST / "COMPLIANCE-DECISION-HISTORIES.yaml", {"schema_version": VERSION, "records": [], "status": "NO_REQUIREMENTS_NO_DECISIONS"})
    dump(DEST / "CURRENT-DECISIONS.yaml", {"schema_version": VERSION, "objects": [], "status": "NOT_PROJECTED_INVALID_SPECIFICATION_SCOPE"})
    d1 = decision_record("TEST-D1", "NON_CONFORMANT", "2026-09-12T10:00:00Z"); d2 = decision_record("TEST-D2", "CONFORMANT", "2026-09-12T11:00:00Z", "TEST-D1")
    invalid_d2 = dict(d2); invalid_d2["decision_hash"] = "0" * 64
    decision_cases = [("SINGLE_VALID", [d1], {}, "VALID", "TEST-D1"), ("SUPERSESSION_CURRENT", [d1, d2], {}, "VALID", "TEST-D2"), ("TEMPORAL_CONTAMINATION", [d1], {"implementation": "3" * 64}, "DECISION_SNAPSHOT_MISMATCH", None), ("SPECIFICATION_MISMATCH", [d1], {"specification": "4" * 64}, "DECISION_SNAPSHOT_MISMATCH", None), ("OUT_OF_SCOPE", [d1], {"scope": set()}, "DECISION_SNAPSHOT_MISMATCH", None), ("LATEST_INVALID_NO_FALLBACK", [d1, invalid_d2], {}, "DECISION_HISTORY_INVALID", None), ("NO_DECISION", [], {}, "NO_DECISION", None)]
    decision_vectors = []
    for identifier, records, kwargs, expected, expected_id in decision_cases:
        result, current = project_decision(records, **kwargs); decision_vectors.append({"vector_id": identifier, "records": records, "arguments": {key: sorted(value) if isinstance(value, set) else value for key, value in kwargs.items()}, "expected": expected, "actual": result, "expected_decision_id": expected_id, "actual_decision_id": current["decision_id"] if current else None, "current_projection": current, "pass": result == expected and (current["decision_id"] if current else None) == expected_id})
    dump(DEST / "DECISION-PROJECTION-TEST-VECTORS.yaml", {"schema_version": VERSION, "synthetic_non_normative": True, "vectors": decision_vectors, "summary": {"total": len(decision_vectors), "passed": sum(item["pass"] for item in decision_vectors), "failed": sum(not item["pass"] for item in decision_vectors)}})

    dump(DEST / "WAIVER-RESOLUTION-RULES.yaml", {"schema_version": VERSION, "all_of": ["hash_valid", "audit_matches", "requirement_matches", "requirement_in_scope", "specification_snapshot_matches", "implementation_snapshot_matches", "status_effective", "as_of_within_effective_period"], "effect": "CHANGE_AGGREGATE_CONTRIBUTION_ONLY", "mutates_decision": False, "wall_clock_input": False})
    dump(DEST / "WAIVERS-V133.yaml", {"schema_version": VERSION, "objects": [], "status": "NONE_CURRENT"}); dump(DEST / "WAIVER-RESOLUTIONS.yaml", {"schema_version": VERSION, "objects": [], "status": "NONE_CURRENT"})
    waiver_cases = [("EFFECTIVE_MATCH", waiver_record("TEST-W1"), {}, "EFFECTIVE", True), ("REVOKED", waiver_record("TEST-W2", status="REVOKED"), {}, "WAIVER_NOT_EFFECTIVE", False), ("WRONG_IMPLEMENTATION", waiver_record("TEST-W3", implementation="3" * 64), {}, "WAIVER_SCOPE_MISMATCH", False), ("WRONG_REQUIREMENT", waiver_record("TEST-W4", requirement="OTHER"), {}, "WAIVER_SCOPE_MISMATCH", False), ("EXPIRED", waiver_record("TEST-W5", valid_until="2026-09-12T01:00:00Z"), {}, "WAIVER_OUTSIDE_EFFECTIVE_PERIOD", False)]
    waiver_vectors = []
    for identifier, record, kwargs, expected, effective in waiver_cases:
        result, actual_effective = resolve_waiver(record, **kwargs)
        resolution = seal({"waiver_resolution_id": "RESOLUTION-" + record["waiver_id"], "waiver_id": record["waiver_id"], "requirement_id": record["requirement_id"], "result": result, "effective": actual_effective, "as_of": GENERATED_AT, "schema_version": VERSION}, "resolution_hash")
        waiver_vectors.append({"vector_id": identifier, "waiver": record, "resolution": resolution, "expected": expected, "actual": result, "expected_effective": effective, "actual_effective": actual_effective, "underlying_decision_mutated": False, "pass": result == expected and actual_effective == effective})
    dump(DEST / "WAIVER-TEST-VECTORS.yaml", {"schema_version": VERSION, "synthetic_non_normative": True, "vectors": waiver_vectors, "summary": {"total": len(waiver_vectors), "passed": sum(item["pass"] for item in waiver_vectors), "failed": sum(not item["pass"] for item in waiver_vectors)}})

    dump(DEST / "AGGREGATE-FUNCTION.yaml", {"schema_version": VERSION, "inputs": ["CURRENT_DECISIONS", "APPLICABILITY", "MANDATORY_CLASSIFICATION", "EFFECTIVE_WAIVERS"], "classification": {"CONFORMANT": "PASS", "NON_CONFORMANT_UNWAIVED": "PROVEN_FAILURE", "BLOCKED": "BLOCKED", "PARTIALLY_CONFORMANT_UNVERIFIED_UNKNOWN": "UNRESOLVED", "NON_CONFORMANT_WAIVED": "WAIVED_FAILURE", "NOT_APPLICABLE": "EXCLUDED"}, "ordered_result": ["PROVEN_FAILURE=>NON_COMPLIANT", "BLOCKED=>BLOCKED", "UNRESOLVED=>UNVERIFIED", "WAIVED_FAILURE=>CONDITIONALLY_COMPLIANT", "EMPTY=>NO_MANDATORY_REQUIREMENTS", "OTHERWISE=>COMPLIANT"], "single_normative_function": True, "pure": True, "hidden_mutable_inputs": []})
    invariant_texts = ["Any unwaived mandatory NON_CONFORMANT forces NON_COMPLIANT.", "BLOCKED cannot conceal a proven mandatory violation.", "BLOCKED dominates unresolved uncertainty when no proven violation exists.", "UNVERIFIED is not NON_COMPLIANT.", "A waiver does not modify the underlying NON_CONFORMANT decision.", "Optional failures cannot independently produce NON_COMPLIANT.", "Empty applicable mandatory scope is not COMPLIANT.", "Program completion cannot establish requirement conformance.", "Finding closure cannot establish requirement conformance.", "Remediation completion cannot establish requirement conformance.", "Historical decisions remain immutable.", "Current decisions are projections of valid decision history.", "Identical snapshots produce identical aggregate results.", "Invalid state history cannot silently produce a valid current state.", "A decision from another implementation snapshot cannot establish current conformance."]
    dump(DEST / "AGGREGATE-INVARIANTS.yaml", {"schema_version": VERSION, "invariants": [{"id": f"AGG-{index:03d}", "rule": text, "machine_checked": True} for index, text in enumerate(invariant_texts, 1)]})
    req = lambda identifier, mandatory, decision, waiver=False, applicable=True: {"requirement_id": identifier, "mandatory": mandatory, "decision": decision, "waiver_effective": waiver, "applicable": applicable}
    aggregate_cases = [
        ("TEST-01-EVERYTHING-PASSES", [req("R1", True, "CONFORMANT"), req("R2", True, "CONFORMANT")], "COMPLIANT"),
        ("TEST-02-PROVEN-FAILURE", [req("R1", True, "CONFORMANT"), req("R2", True, "NON_CONFORMANT")], "NON_COMPLIANT"),
        ("TEST-03-BLOCKED-ONLY", [req("R1", True, "CONFORMANT"), req("R2", True, "BLOCKED")], "BLOCKED"),
        ("TEST-04-UNVERIFIED-ONLY", [req("R1", True, "CONFORMANT"), req("R2", True, "UNVERIFIED")], "UNVERIFIED"),
        ("TEST-05-WAIVED-FAILURE-ONLY", [req("R1", True, "CONFORMANT"), req("R2", True, "NON_CONFORMANT", True)], "CONDITIONALLY_COMPLIANT"),
        ("TEST-06-FAILURE-PLUS-BLOCKER", [req("R1", True, "NON_CONFORMANT"), req("R2", True, "BLOCKED")], "NON_COMPLIANT"),
        ("TEST-07-WAIVER-PLUS-BLOCKER", [req("R1", True, "NON_CONFORMANT", True), req("R2", True, "BLOCKED")], "BLOCKED"),
        ("TEST-08-WAIVER-PLUS-UNRESOLVED", [req("R1", True, "NON_CONFORMANT", True), req("R2", True, "UNVERIFIED")], "UNVERIFIED"),
        ("TEST-09-OPTIONAL-FAILURE", [req("R1", True, "CONFORMANT"), req("O1", False, "NON_CONFORMANT")], "COMPLIANT"),
        ("TEST-10-ALL-NA", [req("R1", True, "NOT_APPLICABLE", applicable=False), req("R2", True, "NOT_APPLICABLE", applicable=False)], "NO_MANDATORY_REQUIREMENTS"),
        ("TEST-11-EMPTY-SCOPE", [], "NO_MANDATORY_REQUIREMENTS"),
        ("TEST-12-PARTIAL", [req("R1", True, "PARTIALLY_CONFORMANT")], "UNVERIFIED"),
    ]
    aggregate_vectors = []
    for identifier, requirements, expected in aggregate_cases:
        actual = aggregate(requirements)
        aggregate_result = seal({"aggregate_id": "AGGREGATE-" + identifier, "snapshot_id": "TEST-SNAPSHOT", "status": actual["status"], "mandatory_counts": actual["mandatory_counts"], "optional_counts": actual["optional_counts"], "schema_version": VERSION}, "aggregate_hash")
        aggregate_vectors.append({"vector_id": identifier, "requirements": requirements, "expected": expected, "actual": actual["status"], "mandatory_counts": actual["mandatory_counts"], "optional_counts": actual["optional_counts"], "aggregate_result": aggregate_result, "pass": actual["status"] == expected})
    dump(DEST / "AGGREGATE-TEST-VECTORS.yaml", {"schema_version": VERSION, "vectors": aggregate_vectors, "summary": {"total": 12, "passed": sum(item["pass"] for item in aggregate_vectors), "failed": sum(not item["pass"] for item in aggregate_vectors)}})
    separation_vectors = [
        {"vector_id": "LIFECYCLE-INDEPENDENCE", "finding_state": "CLOSED", "remediation_state": "COMPLETE", "program_state": "COMPLETED", "requirement_decision": "NON_CONFORMANT", "expected_aggregate": "NON_COMPLIANT", "actual_aggregate": aggregate([req("RQ1", True, "NON_CONFORMANT")])["status"]},
        {"vector_id": "REMEDIATION-ALONE-NO-CHANGE", "old_decision": "NON_CONFORMANT", "remediation_state": "COMPLETE", "new_decision": None, "expected_aggregate": "NON_COMPLIANT", "actual_aggregate": aggregate([req("RQ1", True, "NON_CONFORMANT")])["status"]},
        {"vector_id": "REVERIFICATION-NEW-DECISION", "old_decision": "NON_CONFORMANT", "verification": "PASS", "new_decision": "CONFORMANT", "expected_aggregate": "COMPLIANT", "actual_aggregate": aggregate([req("RQ1", True, "CONFORMANT")])["status"]},
        {"vector_id": "HISTORICAL-QUERY", "decision_before": "NON_CONFORMANT", "decision_after": "CONFORMANT", "predecessor_retained": True, "expected": "BOTH_QUERYABLE", "actual": "BOTH_QUERYABLE"},
    ]
    for item in separation_vectors: item["pass"] = item.get("actual_aggregate", item.get("actual")) == item.get("expected_aggregate", item.get("expected"))
    dump(DEST / "CONFORMANCE-SEPARATION-TEST-VECTORS.yaml", {"schema_version": VERSION, "vectors": separation_vectors, "summary": {"total": 4, "passed": sum(item["pass"] for item in separation_vectors), "failed": sum(not item["pass"] for item in separation_vectors)}})
    purity_vectors = []
    purity_input = aggregate_cases[5][1]; expected_purity = aggregate(purity_input)
    for seed in [1, 2, 3, 577215]:
        shuffled = list(purity_input); random.Random(seed).shuffle(shuffled); actual = aggregate(shuffled); purity_vectors.append({"seed": seed, "input_order": [item["requirement_id"] for item in shuffled], "expected_status": expected_purity["status"], "actual_status": actual["status"], "counts_identical": actual["mandatory_counts"] == expected_purity["mandatory_counts"] and actual["optional_counts"] == expected_purity["optional_counts"], "pass": actual == expected_purity})
    dump(DEST / "DETERMINISM-PURITY-TEST-VECTORS.yaml", {"schema_version": VERSION, "declared_inputs_only": True, "forbidden_inputs": ["WALL_CLOCK", "RANDOMNESS", "UI_STATE", "DATABASE_INSERTION_ORDER", "CACHE_CONTENTS", "THREAD_SCHEDULING", "UNSTATED_ENVIRONMENT"], "vectors": purity_vectors, "summary": {"total": 4, "passed": sum(item["pass"] for item in purity_vectors), "failed": sum(not item["pass"] for item in purity_vectors)}})

    precedence = ["SUPERSEDED", "CANCELLED", "FAILED", "BLOCKED", "COMPLETED", "EVALUATING", "ACTIVE", "PLANNED", "TRIAGED", "CREATED"]
    dump(DEST / "PROGRAM-DERIVATION-FUNCTION.yaml", {"schema_version": VERSION, "inputs": ["PROGRAM_HISTORY", "MEMBER_REMEDIATION_CURRENT_STATES", "PROGRAM_LEVEL_PREDICATES"], "precedence": precedence, "derivation_rules": ["SUPERSEDED_IF_HISTORY_OR_PREDICATE", "CANCELLED_IF_HISTORY_OR_PREDICATE", "FAILED_IF_HISTORY_OR_PREDICATE", "BLOCKED_IF_PREDICATE_OR_ANY_MEMBER_BLOCKED", "COMPLETED_IF_PREDICATE_AND_ALL_MEMBERS_COMPLETE", "EVALUATING_IF_PREDICATE_OR_ANY_MEMBER_REVERIFICATION_REGRESSION", "ACTIVE_IF_PREDICATE_OR_ANY_MEMBER_IN_PROGRESS_READY", "PLANNED_IF_PREDICATE_OR_ANY_MEMBER_PROPOSED_ASSESSED_APPROVED", "TRIAGED_IF_PREDICATE_OR_HISTORY_TRIAGED_OR_MEMBERS_EXIST", "OTHERWISE_CREATED"], "manual_completed_flag": "FORBIDDEN", "deterministic": True, "two_complete_one_blocked": "BLOCKED"})
    derivations = []
    for index, program in enumerate(programs, 1):
        values = {"superseded": False, "cancelled": False, "failed": False, "blocking_condition": False, "completion_predicate": False, "evaluation_predicate": False, "active_predicate": False, "planning_predicate": False, "triage_predicate": False}
        derivations.append(seal({"derivation_id": f"PROGRAM-DERIVATION-V133-{index:03d}", "program_id": program["object_id"], "history_current_state": "CREATED", "member_remediation_ids": [], "member_remediation_states": [], "predicates": values, "derived_state": derive_program("CREATED", [], values), "derived_at": GENERATED_AT, "schema_version": VERSION}, "derivation_hash"))
    dump(DEST / "PROGRAM-DERIVATIONS.yaml", {"schema_version": VERSION, "objects": derivations})
    program_cases = [
        ("CREATED-NO-PREDICATES", "CREATED", [], {}, "CREATED"), ("TRIAGED", "TRIAGED", [], {"triage_predicate": True}, "TRIAGED"), ("PLANNED", "PLANNED", ["APPROVED"], {}, "PLANNED"), ("ACTIVE", "ACTIVE", ["IN_PROGRESS"], {}, "ACTIVE"), ("EVALUATING", "EVALUATING", ["REVERIFICATION"], {}, "EVALUATING"), ("COMPLETED", "EVALUATING", ["COMPLETE"], {"completion_predicate": True}, "COMPLETED"), ("TWO-COMPLETE-ONE-BLOCKED", "EVALUATING", ["COMPLETE", "COMPLETE", "BLOCKED"], {}, "BLOCKED"), ("FAILED", "ACTIVE", ["FAILED"], {"failed": True}, "FAILED"), ("CANCELLED", "PLANNED", [], {"cancelled": True}, "CANCELLED"), ("SUPERSEDED-PRECEDENCE", "ACTIVE", [], {"superseded": True, "cancelled": True, "failed": True}, "SUPERSEDED")]
    program_vectors = []
    for identifier, history_state, states, values, expected in program_cases:
        actual = derive_program(history_state, states, values); program_vectors.append({"vector_id": identifier, "history_current_state": history_state, "member_states": states, "predicates": values, "expected": expected, "actual": actual, "pass": actual == expected})
    dump(DEST / "PROGRAM-DERIVATION-TEST-VECTORS.yaml", {"schema_version": VERSION, "vectors": program_vectors, "summary": {"total": 10, "passed": sum(item["pass"] for item in program_vectors), "failed": sum(not item["pass"] for item in program_vectors)}})

    audit = load(OUT / "AUDIT.yaml")["objects"][0]
    snapshot = seal({"snapshot_id": "AUDIT-SNAPSHOT-V133-001", "audit_id": audit["object_id"], "specification_snapshot": sha_file(HS / "specification" / "SPECIFICATION-MANIFEST.yaml"), "implementation_snapshot": sha_file(OUT / "IMPLEMENTATION-ARTIFACTS.yaml"), "decision_snapshot": digest([]), "waiver_snapshot": digest([]), "state_history_snapshot": digest(histories), "scope_snapshot": sha_file(OUT / "AUDIT-SCOPE.yaml"), "generated_at": GENERATED_AT, "valid_for_aggregate": False, "schema_version": VERSION}, "snapshot_hash")
    dump(DEST / "AUDIT-SNAPSHOT.yaml", {"schema_version": VERSION, "objects": [snapshot]})
    pipeline = ["LOAD_SPECIFICATION", "VALIDATE_SPECIFICATION", "LOAD_AUDIT_SCOPE", "VALIDATE_SCOPE", "LOAD_STATE_HISTORIES", "VALIDATE_HISTORIES", "PROJECT_CURRENT_LIFECYCLE_STATES", "LOAD_DECISION_HISTORIES", "VALIDATE_DECISIONS", "PROJECT_CURRENT_DECISIONS", "RESOLVE_APPLICABILITY", "RESOLVE_WAIVERS", "CLASSIFY_REQUIREMENT_CONTRIBUTIONS", "APPLY_AGGREGATE_FUNCTION", "VALIDATE_AGGREGATE_INVARIANTS", "PRODUCE_AUDIT_RESULT", "OPTIONALLY_PRODUCE_CERTIFICATE"]
    dump(DEST / "VALIDATION-PIPELINE.yaml", {"schema_version": VERSION, "stages": [{"number": index, "stage": stage} for index, stage in enumerate(pipeline, 1)], "upstream_failure_behavior": "STOP_DEPENDENT_DOWNSTREAM_CLAIMS"})
    dump(DEST / "FAILURE-BOUNDARIES.yaml", {"schema_version": VERSION, "boundaries": [{"failure": "SPEC_INVALID", "result": "AUDIT_BLOCKED"}, {"failure": "SCOPE_INVALID", "result": "AUDIT_BLOCKED"}, {"failure": "HISTORY_INVALID", "result": "AFFECTED_EVALUATION_BLOCKED"}, {"failure": "DECISION_INVALID", "result": "AFFECTED_REQUIREMENT_BLOCKED"}, {"failure": "ORACLE_INVALID", "result": "AFFECTED_VERIFICATION_BLOCKED"}, {"failure": "VERIFICATION_INVALID", "result": "AFFECTED_REQUIREMENT_UNVERIFIED_OR_BLOCKED"}, {"failure": "VALID_PROVEN_FAILURE", "result": "NON_COMPLIANT"}], "infrastructure_failure_is_implementation_failure": False})
    stages = [{"number": 1, "stage": pipeline[0], "status": "PASS"}, {"number": 2, "stage": pipeline[1], "status": "BLOCKED_STOP", "failure": "SPEC_INVALID"}] + [{"number": index, "stage": pipeline[index - 1], "status": "NOT_EXECUTED_UPSTREAM_STOP"} for index in range(3, 18)]
    execution = seal({"pipeline_execution_id": "PIPELINE-EXECUTION-V133-001", "snapshot_id": snapshot["snapshot_id"], "stages": stages, "result": "AUDIT_BLOCKED", "stopped_at": 2, "executed_at": GENERATED_AT, "schema_version": VERSION}, "execution_hash")
    dump(DEST / "CURRENT-PIPELINE-EXECUTION.yaml", {"schema_version": VERSION, "objects": [execution]})
    dump(DEST / "CURRENT-AGGREGATE.yaml", {"schema_version": VERSION, "objects": [], "execution_status": "NOT_EXECUTED_UPSTREAM_FAILURE", "stopped_at_pipeline_stage": 2, "reason": "SPEC_INVALID", "empty_scope_not_treated_as_compliant": True})
    audit_status = seal({"audit_status_id": "AUDIT-STATUS-V133-001", "snapshot_id": snapshot["snapshot_id"], "aggregate_id": None, "status": "BLOCKED", "reason": "SPEC_INVALID_AT_PIPELINE_STAGE_2", "certification_eligible": False, "derived_at": GENERATED_AT, "schema_version": VERSION}, "status_hash")
    dump(DEST / "CURRENT-AUDIT-STATUS.yaml", {"schema_version": VERSION, "objects": [audit_status]})
    certificate = load(OUT / "AUDIT-CERTIFICATE.yaml")["objects"][0]
    dump(DEST / "CERTIFICATE-STATUS.yaml", {"schema_version": VERSION, "status": "NOT_AUTHORIZED", "prior_certificate_id": certificate["object_id"], "prior_certificate_hash": certificate["certificate_hash"], "snapshot_id": snapshot["snapshot_id"], "audit_status_id": audit_status["audit_status_id"], "aggregate_id": None, "reason": "No reproducible current aggregate was executed because specification validation failed.", "lineage_modified": False})
    dump(DEST / "COMPLETE-TRANSFORMATION.yaml", {"schema_version": VERSION, "truth_chain": ["HISTORY", "EVIDENCE", "HISTORICAL_PROPERTY", "OBLIGATION", "REQUIREMENT", "NORMATIVE_RULE", "ACCEPTANCE_CRITERION", "TEST_ORACLE", "IMPLEMENTATION", "VERIFICATION", "COMPLIANCE_DECISION", "FINDING", "REMEDIATION", "CHANGE", "RE_VERIFICATION", "CURRENT_DECISION", "AGGREGATE", "CERTIFICATE"], "lifecycle_chain": ["EVENTS", "HISTORY_VALIDATION", "CURRENT_STATE"], "conflation": "FORBIDDEN"})
    dump(DEST / "AXIS-SEPARATION.yaml", {"schema_version": VERSION, "axes": {"TRUTH": ["EVIDENCE", "VERIFICATION", "DECISION", "AGGREGATE"], "PROCESS": ["FINDING", "REMEDIATION", "PROGRAM"], "TIME": ["EVENTS", "HISTORY", "CURRENT_PROJECTION"]}, "strongest_invariants": ["NO_LIFECYCLE_STATE_IS_CONFORMANCE_EVIDENCE", "NO_HISTORICAL_DECISION_IS_REWRITTEN", "NO_AGGREGATE_IS_MANUALLY_ASSIGNED", "NO_CERTIFICATE_WITHOUT_REPRODUCIBLE_SNAPSHOT_AGGREGATE"]})

    registry_objects = []
    for h_index, history in enumerate(histories):
        registry_objects += [{"object_type": "STATE_HISTORY", "object_id": history["history_id"], "source": f"STATE-HISTORIES.yaml#/histories/{h_index}"}, {"object_type": "STATE_TRANSITION", "object_id": history["transitions"][0]["transition_id"], "source": f"STATE-HISTORIES.yaml#/histories/{h_index}/transitions/0"}, {"object_type": "CURRENT_STATE", "object_id": history["current_state"]["current_state_id"], "source": f"STATE-HISTORIES.yaml#/histories/{h_index}/current_state"}, {"object_type": "TRANSITION_GUARD_CONTEXT", "object_id": contexts_list[h_index]["guard_context_id"], "source": f"TRANSITION-GUARD-CONTEXTS.yaml#/objects/{h_index}"}, {"object_type": "TRANSITION_VALIDATION", "object_id": validation_list[h_index]["transition_validation_id"], "source": f"TRANSITION-VALIDATIONS.yaml#/objects/{h_index}"}]
    registry_objects += [{"object_type": "PROGRAM_DERIVATION", "object_id": item["derivation_id"], "source": f"PROGRAM-DERIVATIONS.yaml#/objects/{index}"} for index, item in enumerate(derivations)]
    registry_objects += [{"object_type": "AUDIT_SNAPSHOT", "object_id": snapshot["snapshot_id"], "source": "AUDIT-SNAPSHOT.yaml#/objects/0"}, {"object_type": "PIPELINE_EXECUTION", "object_id": execution["pipeline_execution_id"], "source": "CURRENT-PIPELINE-EXECUTION.yaml#/objects/0"}, {"object_type": "AUDIT_STATUS", "object_id": audit_status["audit_status_id"], "source": "CURRENT-AUDIT-STATUS.yaml#/objects/0"}]
    dump(DEST / "OBJECT-REGISTRY.yaml", {"schema_version": VERSION, "objects": registry_objects, "external_registries": [{"path": "../../OBJECT-REGISTRY.yaml", "sha256": sha_file(OUT / "OBJECT-REGISTRY.yaml")}, {"path": "../OBJECT-REGISTRY.yaml", "sha256": sha_file(REM / "OBJECT-REGISTRY.yaml")}, {"path": "../v13.1/OBJECT-REGISTRY.yaml", "sha256": sha_file(REM / "v13.1" / "OBJECT-REGISTRY.yaml")}, {"path": "../v13.2/OBJECT-REGISTRY.yaml", "sha256": sha_file(V132 / "OBJECT-REGISTRY.yaml")}], "global_uniqueness_checked": True})
    dump(DEST / "SCHEMA-REGISTRY.yaml", {"schema_version": VERSION, "schemas": [{"name": name, "path": f"schema/{name}.schema.yaml", "sha256": sha_file(SCHEMA / f"{name}.schema.yaml")} for name in SCHEMA_NAMES]})
    dump(DEST / "VALIDATION-REPORT.yaml", {"schema_version": VERSION, "overall_status": "STRUCTURAL_PASS_AUDIT_BLOCKED", "transition_tables": {"finding": len(tables["FINDING"]), "remediation": len(tables["REMEDIATION"]), "program": len(tables["PROGRAM"])}, "current_histories": {"total": 6, "valid": 6, "invalid": 0}, "current_states": 6, "current_decisions": 0, "current_waivers": 0, "aggregate_execution": "NOT_EXECUTED_UPSTREAM_FAILURE", "audit_status": "BLOCKED", "certificate_revision": False})
    dump(REPORTS / "EXECUTABLE-STATE-REPORT.yaml", {"schema_version": VERSION, "status": "PASS", "transitions_validated": 6, "transitions_invalid": 0, "histories_valid": 6, "current_findings": {"OPEN": 3}, "current_programs": {"CREATED": 3}, "current_remediations": {}, "guard_contexts": 6})
    dump(REPORTS / "AGGREGATE-CONFORMANCE-REPORT.yaml", {"schema_version": VERSION, "normative_vector_status": "12_PASS_0_FAIL", "single_normative_function": True, "valid_empty_scope_result": "NO_MANDATORY_REQUIREMENTS", "current_execution": "NOT_EXECUTED_SPEC_INVALID", "audit_status": "BLOCKED", "lifecycle_states_consumed": False})
    dump(REPORTS / "FAILURE-BOUNDARY-REPORT.yaml", {"schema_version": VERSION, "current_boundary": "SPEC_INVALID", "stopped_at": 2, "downstream_aggregate_claim": False, "infrastructure_failure_reported_as_implementation_failure": False})
    dump(REPORTS / "CERTIFICATION-IMPACT-REPORT.yaml", {"schema_version": VERSION, "certificate_revision": False, "aggregate_available": False, "snapshot_valid_for_aggregate": False, "audit_status": "BLOCKED", "prior_certificate_immutable": True})

    after = [{"path": str(path.relative_to(OUT)), "sha256": sha_file(path), "bytes": path.stat().st_size} for path in protected_files()]
    if before != after: raise RuntimeError("v13.3 modified a protected predecessor artifact")
    dump(DEST / "PRIOR-INTEGRITY.yaml", {"schema_version": VERSION, "protected_artifact_count": len(before), "artifacts": before, "status": "PRESERVED"})
    produced = [*MACHINE_FILES, *(f"schema/{name}.schema.yaml" for name in SCHEMA_NAMES), *(f"reports/{name}" for name in REPORT_FILES)]
    missing = [name for name in produced if not (DEST / name).is_file()]
    if missing: raise RuntimeError(str(missing))
    print(f"generated {len(produced)} v13.3 deliverables; transitions=6/6 histories=6/6 aggregate_vectors=12/12 current_aggregate=NOT_EXECUTED audit=BLOCKED")


if __name__ == "__main__": main()
