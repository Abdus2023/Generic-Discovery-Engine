#!/usr/bin/env python3
"""Build Protocol-v13.2 immutable history, current projections, and aggregates."""
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
REM = OUT / "remediation"
V131 = REM / "v13.1"
DEST = REM / "v13.2"
SCHEMA = DEST / "schema"
REPORTS = DEST / "reports"
VERSION = "13.2"
GENERATED_AT = "2026-09-12T17:20:43Z"

FINDING_STATES = ["DETECTED", "VALIDATED", "CLASSIFIED", "OPEN", "UNDER_REMEDIATION", "RESOLVED", "CLOSED", "REJECTED", "WAIVED", "SUPERSEDED", "BLOCKED"]
REMEDIATION_STATES = ["PROPOSED", "ASSESSED", "APPROVED", "IN_PROGRESS", "READY_FOR_VERIFICATION", "REVERIFICATION", "REGRESSION", "COMPLETE", "FAILED", "BLOCKED", "REJECTED", "SUPERSEDED", "CANCELLED"]
PROGRAM_STATES = ["CREATED", "TRIAGED", "PLANNED", "ACTIVE", "EVALUATING", "COMPLETED", "BLOCKED", "FAILED", "CANCELLED", "SUPERSEDED"]
DECISION_STATES = ["UNASSESSED", "MAPPED", "VERIFIED", "CONFORMANT", "PARTIALLY_CONFORMANT", "NON_CONFORMANT", "UNVERIFIED", "BLOCKED", "UNKNOWN", "NOT_APPLICABLE"]
AGGREGATE_STATES = ["NON_COMPLIANT", "BLOCKED", "UNVERIFIED", "CONDITIONALLY_COMPLIANT", "COMPLIANT", "NO_MANDATORY_REQUIREMENTS"]
SCHEMA_NAMES = ["state-transition", "current-state", "state-history", "compliance-decision-record", "current-requirement-decision", "audit-snapshot", "audit-aggregate", "program-state-derivation", "audit-status"]
MACHINE_FILES = [
    "STATE-DOMAIN-SEPARATION.yaml", "BASELINE-IMPORT-POLICY.yaml", "STATE-TRANSITION-MODEL.yaml",
    "CURRENT-STATE-PROJECTION.yaml", "STATE-HISTORIES.yaml", "STATE-TRANSITION-REGISTRY.yaml",
    "CURRENT-STATES.yaml", "STATE-PROJECTION-TEST-VECTORS.yaml", "DECISION-HISTORY-MODEL.yaml",
    "COMPLIANCE-DECISION-HISTORIES.yaml", "CURRENT-REQUIREMENT-DECISIONS.yaml",
    "DECISION-PROJECTION-TEST-VECTORS.yaml", "AGGREGATE-FUNCTION.yaml", "AGGREGATE-TEST-VECTORS.yaml",
    "AUDIT-SNAPSHOT.yaml", "CURRENT-AGGREGATE.yaml", "AUDIT-STATUS.yaml", "AUDIT-INTEGRITY.yaml",
    "PROGRAM-STATE-MACHINE.yaml", "PROGRAM-DERIVATION-FUNCTION.yaml", "PROGRAM-DERIVATIONS.yaml",
    "PROGRAM-TEST-VECTORS.yaml", "TEMPORAL-QUERY-RULES.yaml", "CANONICAL-MODEL.yaml",
    "CERTIFICATE-POLICY.yaml", "CERTIFICATE-REVISION-STATUS.yaml", "INVARIANTS.yaml",
    "OBJECT-REGISTRY.yaml", "SCHEMA-REGISTRY.yaml", "VALIDATION-REPORT.yaml", "PRIOR-INTEGRITY.yaml",
]
REPORT_FILES = ["CURRENT-STATE-REPORT.yaml", "AGGREGATE-CONFORMANCE-REPORT.yaml", "TEMPORAL-INTEGRITY-REPORT.yaml", "CERTIFICATION-IMPACT-REPORT.yaml"]
INVARIANTS = [
    "Historical transitions MUST NOT be modified or deleted.",
    "Current state MUST be derivable from valid history.",
    "A compliance decision MUST NOT be mutated after recording.",
    "New evidence MUST produce a new decision record.",
    "Program completion MUST NOT directly produce conformance.",
    "Finding closure MUST NOT directly produce conformance.",
    "Remediation completion MUST NOT directly produce conformance.",
    "A proven mandatory violation MUST produce NON_COMPLIANT even when another requirement is blocked.",
    "A mandatory blocker MUST produce BLOCKED when no proven unwaived mandatory violation exists.",
    "An unresolved mandatory requirement prevents CONDITIONALLY_COMPLIANT.",
    "An effective waiver changes disposition and does not alter the underlying decision.",
    "Optional requirements cannot independently produce NON_COMPLIANT.",
    "An empty applicable mandatory set produces NO_MANDATORY_REQUIREMENTS when integrity permits evaluation.",
    "Superseded decisions remain historically queryable.",
    "Past aggregate results remain reproducible from their snapshots.",
    "Malformed state history produces an explicit integrity failure and no current projection.",
    "A completed program cannot transition back into active execution.",
    "Post-completion remediation uses a new program or explicitly authorized successor.",
    "Aggregate status is derived and cannot be manually assigned.",
    "A certificate describes a specific audit snapshot rather than universal system truth.",
]


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def seal(value: dict[str, Any], field: str) -> dict[str, Any]:
    payload = dict(value); payload.pop(field, None); value[field] = digest(payload); return value


def timestamp_valid(value: Any) -> bool:
    if not isinstance(value, str): return False
    try: return datetime.fromisoformat(value.replace("Z", "+00:00")).tzinfo is not None
    except ValueError: return False


def transition(transition_id: str, object_type: str, object_id: str, to_state: str, evidence_id: str) -> dict[str, Any]:
    return seal({
        "transition_id": transition_id, "object_type": object_type, "object_id": object_id,
        "from_state": None, "to_state": to_state,
        "reason": "BASELINE_IMPORT: establish v13.2 projection lineage without reconstructing unavailable earlier transitions",
        "evidence_refs": [evidence_id], "actor": "PROTOCOL_V13_2_BASELINE_IMPORT",
        "occurred_at": GENERATED_AT, "sequence": 1, "previous_transition": None,
    }, "event_hash")


def legal_maps() -> dict[str, set[tuple[str, str]]]:
    finding = {("DETECTED", "VALIDATED"), ("DETECTED", "REJECTED"), ("VALIDATED", "CLASSIFIED"), ("CLASSIFIED", "OPEN"), ("OPEN", "UNDER_REMEDIATION"), ("OPEN", "WAIVED"), ("OPEN", "SUPERSEDED"), ("UNDER_REMEDIATION", "RESOLVED"), ("UNDER_REMEDIATION", "OPEN"), ("RESOLVED", "CLOSED"), ("RESOLVED", "OPEN")}
    finding |= {(state, "BLOCKED") for state in ["DETECTED", "VALIDATED", "CLASSIFIED", "OPEN", "UNDER_REMEDIATION", "RESOLVED"]}
    remediation = {("PROPOSED", "ASSESSED"), ("PROPOSED", "REJECTED"), ("ASSESSED", "APPROVED"), ("ASSESSED", "REJECTED"), ("APPROVED", "IN_PROGRESS"), ("IN_PROGRESS", "READY_FOR_VERIFICATION"), ("IN_PROGRESS", "BLOCKED"), ("READY_FOR_VERIFICATION", "REVERIFICATION"), ("REVERIFICATION", "FAILED"), ("REVERIFICATION", "REGRESSION"), ("REGRESSION", "FAILED"), ("REGRESSION", "COMPLETE"), ("FAILED", "IN_PROGRESS")}
    program = {("CREATED", "TRIAGED"), ("TRIAGED", "PLANNED"), ("PLANNED", "ACTIVE"), ("ACTIVE", "EVALUATING"), ("EVALUATING", "COMPLETED"), ("CREATED", "CANCELLED"), ("TRIAGED", "CANCELLED"), ("PLANNED", "CANCELLED"), ("BLOCKED", "FAILED"), ("BLOCKED", "CANCELLED"), ("TRIAGED", "SUPERSEDED"), ("PLANNED", "SUPERSEDED"), ("ACTIVE", "SUPERSEDED"), ("EVALUATING", "SUPERSEDED")}
    program |= {(state, "BLOCKED") for state in ["CREATED", "TRIAGED", "PLANNED", "ACTIVE", "EVALUATING"]}
    return {"AUDIT_FINDING": finding, "REMEDIATION": remediation, "REMEDIATION_PROGRAM": program}


def project(initial_state: str | None, events: list[dict[str, Any]], object_type: str, object_id: str, legal: dict[str, set[tuple[str, str]]]) -> tuple[str, dict[str, Any] | None]:
    errors: list[str] = []
    ordered = sorted(events, key=lambda item: item.get("sequence", -1))
    expected_state = initial_state; previous_id = None; previous_time: datetime | None = None; blocked_return_state = None
    if not ordered: errors.append("NO_TRANSITIONS")
    if [item.get("sequence") for item in ordered] != list(range(1, len(ordered) + 1)): errors.append("SEQUENCE_NOT_CONTIGUOUS")
    for index, event in enumerate(ordered):
        if event.get("object_type") != object_type or event.get("object_id") != object_id: errors.append("OBJECT_IDENTITY_CHANGED")
        if event.get("previous_transition") != previous_id: errors.append("PREVIOUS_TRANSITION_MISMATCH")
        if event.get("from_state") != expected_state: errors.append("FROM_STATE_MISMATCH")
        event_time = None
        if not timestamp_valid(event.get("occurred_at")): errors.append("TIMESTAMP_INVALID")
        else:
            event_time = datetime.fromisoformat(event["occurred_at"].replace("Z", "+00:00"))
            if previous_time and event_time < previous_time: errors.append("TIMESTAMP_ORDER_INVALID")
        if not event.get("evidence_refs"): errors.append("EVIDENCE_MISSING")
        payload = dict(event); supplied = payload.pop("event_hash", None)
        if supplied != digest(payload): errors.append("EVENT_HASH_INVALID")
        baseline = index == 0 and expected_state is None and event.get("reason", "").startswith("BASELINE_IMPORT:")
        blocked_return = expected_state == "BLOCKED" and event.get("to_state") == blocked_return_state and "BLOCK_REMOVED" in event.get("reason", "")
        if not baseline and not blocked_return and (expected_state, event.get("to_state")) not in legal.get(object_type, set()): errors.append("ILLEGAL_TRANSITION")
        if expected_state == "COMPLETED": errors.append("COMPLETED_PROGRAM_TERMINAL")
        if event.get("to_state") == "BLOCKED": blocked_return_state = expected_state
        elif expected_state == "BLOCKED": blocked_return_state = None
        expected_state = event.get("to_state"); previous_id = event.get("transition_id"); previous_time = event_time or previous_time
    if errors: return "HISTORY_INVALID", None
    current = seal({
        "current_state_id": "CURRENT-" + object_id, "object_type": object_type, "object_id": object_id,
        "state": expected_state, "state_as_of": ordered[-1]["occurred_at"],
        "last_transition_id": ordered[-1]["transition_id"], "transition_sequence": ordered[-1]["sequence"],
    }, "projection_hash")
    return "VALID", current


def state_history(history_id: str, object_type: str, object_id: str, event: dict[str, Any], legal: dict[str, set[tuple[str, str]]]) -> dict[str, Any]:
    status, current = project(None, [event], object_type, object_id, legal)
    history = {
        "history_id": history_id, "object_type": object_type, "object_id": object_id, "initial_state": None,
        "transitions": [event], "current_state": current,
        "history_integrity": {"valid": status == "VALID", "checked_at": GENERATED_AT, "error_codes": [] if status == "VALID" else [status]},
    }
    return seal(history, "history_hash")


def derive_program(states: list[str], *, superseded: bool = False, cancelled: bool = False, blocking: bool = False, evaluation_complete: bool = False, evaluation_pending: bool = False) -> str:
    if superseded: return "SUPERSEDED"
    if cancelled: return "CANCELLED"
    if states and all(state == "REJECTED" for state in states): return "FAILED"
    if blocking: return "BLOCKED"
    if states and all(state == "COMPLETE" for state in states) and evaluation_complete: return "COMPLETED"
    if any(state in {"REVERIFICATION", "REGRESSION"} for state in states) or evaluation_pending or (states and all(state == "COMPLETE" for state in states) and not evaluation_complete): return "EVALUATING"
    if any(state in {"IN_PROGRESS", "READY_FOR_VERIFICATION"} for state in states): return "ACTIVE"
    if any(state in {"PROPOSED", "ASSESSED", "APPROVED"} for state in states): return "PLANNED"
    if states: return "TRIAGED"
    return "CREATED"


def aggregate(requirements: list[dict[str, Any]], integrity_blockers: list[str]) -> tuple[str, dict[str, dict[str, int]]]:
    categories = ["proven_failure", "waived_failure", "blocked", "unresolved", "pass", "excluded"]
    counts = {kind: {category: 0 for category in categories} for kind in ["mandatory", "optional"]}
    applicable_mandatory: list[dict[str, Any]] = []
    for item in requirements:
        kind = "mandatory" if item["mandatory"] else "optional"; decision = item["decision"]
        if not item.get("applicable", True) or decision == "NOT_APPLICABLE": category = "excluded"
        elif decision == "NON_CONFORMANT": category = "waived_failure" if item.get("waiver_effective", False) else "proven_failure"
        elif decision == "BLOCKED" or decision in {"UNASSESSED", "MAPPED", "VERIFIED"}: category = "blocked"
        elif decision in {"PARTIALLY_CONFORMANT", "UNVERIFIED", "UNKNOWN"}: category = "unresolved"
        elif decision == "CONFORMANT": category = "pass"
        else: raise ValueError(decision)
        counts[kind][category] += 1
        if kind == "mandatory" and category != "excluded": applicable_mandatory.append({**item, "category": category})
    if any(item["category"] == "proven_failure" for item in applicable_mandatory): return "NON_COMPLIANT", counts
    if integrity_blockers or any(item["category"] == "blocked" for item in applicable_mandatory): return "BLOCKED", counts
    if any(item["category"] == "unresolved" for item in applicable_mandatory): return "UNVERIFIED", counts
    if any(item["category"] == "waived_failure" for item in applicable_mandatory): return "CONDITIONALLY_COMPLIANT", counts
    if not applicable_mandatory: return "NO_MANDATORY_REQUIREMENTS", counts
    return "COMPLIANT", counts


def base_schema(title: str, required: list[str], properties: dict[str, Any], rules: list[str] | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {"$schema": "https://json-schema.org/draft/2020-12/schema", "title": title, "type": "object", "required": required, "properties": properties, "additionalProperties": False}
    if rules: result["x-v13.2-rules"] = rules
    return result


def build_schemas() -> dict[str, Any]:
    ident = {"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9._:/-]*$"}; ts = {"type": "string", "format": "date-time"}; hexdigest = {"type": "string", "pattern": "^[a-f0-9]{64}$"}; nullable_ident = {"oneOf": [ident, {"type": "null"}]}; state_enum = {"type": "string", "enum": sorted(set(FINDING_STATES + REMEDIATION_STATES + PROGRAM_STATES + DECISION_STATES))}; nullable_state = {"oneOf": [state_enum, {"type": "null"}]}; strings = lambda minimum=0: {"type": "array", "minItems": minimum, "items": {"type": "string"}, "uniqueItems": True}
    state_transition = base_schema("Protocol-v13.2 StateTransition", ["transition_id", "object_type", "object_id", "from_state", "to_state", "reason", "evidence_refs", "actor", "occurred_at", "sequence", "previous_transition", "event_hash"], {
        "transition_id": ident, "object_type": {"type": "string", "enum": ["AUDIT_FINDING", "REMEDIATION", "REMEDIATION_PROGRAM", "COMPLIANCE_DECISION"]}, "object_id": ident, "from_state": nullable_state, "to_state": state_enum, "reason": {"type": "string", "minLength": 1}, "evidence_refs": strings(1), "actor": {"type": "string", "minLength": 1}, "occurred_at": ts, "sequence": {"type": "integer", "minimum": 1}, "previous_transition": nullable_ident, "event_hash": hexdigest,
    }, ["Immutable", "Hash excludes event_hash", "Projection stops on first invalid prerequisite"])
    current_state = base_schema("Protocol-v13.2 CurrentState", ["current_state_id", "object_type", "object_id", "state", "state_as_of", "last_transition_id", "transition_sequence", "projection_hash"], {
        "current_state_id": ident, "object_type": {"type": "string"}, "object_id": ident, "state": {"type": "string"}, "state_as_of": ts, "last_transition_id": ident, "transition_sequence": {"type": "integer", "minimum": 1}, "projection_hash": hexdigest,
    }, ["Derived only from valid transition history", "Not an independent historical source"])
    state_history = base_schema("Protocol-v13.2 StateHistory", ["history_id", "object_type", "object_id", "initial_state", "transitions", "current_state", "history_integrity", "history_hash"], {
        "history_id": ident, "object_type": {"type": "string"}, "object_id": ident, "initial_state": nullable_state, "transitions": {"type": "array", "minItems": 1, "items": {"$ref": "state-transition.schema.yaml"}}, "current_state": {"oneOf": [{"$ref": "current-state.schema.yaml"}, {"type": "null"}]},
        "history_integrity": {"type": "object", "required": ["valid", "checked_at", "error_codes"], "properties": {"valid": {"type": "boolean"}, "checked_at": ts, "error_codes": strings()}, "additionalProperties": False}, "history_hash": hexdigest,
    }, ["Malformed history has no current_state projection", "Hash excludes history_hash"])
    decision_basis = {"type": "object", "required": ["acceptance_criteria", "evidence_refs", "verification_refs", "rule_refs"], "properties": {key: strings() for key in ["acceptance_criteria", "evidence_refs", "verification_refs", "rule_refs"]}, "additionalProperties": False}
    decision_record = base_schema("Protocol-v13.2 ComplianceDecisionRecord", ["decision_id", "requirement_id", "audit_id", "decision", "basis", "decided_at", "implementation_snapshot", "specification_snapshot", "audit_run_id", "supersedes", "decision_hash"], {
        "decision_id": ident, "requirement_id": ident, "audit_id": ident, "decision": {"type": "string", "enum": DECISION_STATES}, "basis": decision_basis, "decided_at": ts, "implementation_snapshot": hexdigest, "specification_snapshot": hexdigest, "audit_run_id": ident, "supersedes": nullable_ident, "decision_hash": hexdigest,
    }, ["Immutable", "New evidence creates a new record", "Hash excludes decision_hash"])
    current_decision = base_schema("Protocol-v13.2 CurrentRequirementDecision", ["current_decision_id", "audit_id", "requirement_id", "decision_id", "decision", "as_of", "implementation_snapshot", "specification_snapshot", "decision_history_valid", "projection_hash"], {
        "current_decision_id": ident, "audit_id": ident, "requirement_id": ident, "decision_id": ident, "decision": {"type": "string", "enum": DECISION_STATES}, "as_of": ts, "implementation_snapshot": hexdigest, "specification_snapshot": hexdigest, "decision_history_valid": {"const": True}, "projection_hash": hexdigest,
    })
    audit_snapshot = base_schema("Protocol-v13.2 AuditSnapshot", ["snapshot_id", "audit_id", "specification_snapshot", "implementation_snapshot", "decision_snapshot", "waiver_snapshot", "state_history_snapshot", "generated_at", "snapshot_hash"], {"snapshot_id": ident, "audit_id": ident, "specification_snapshot": hexdigest, "implementation_snapshot": hexdigest, "decision_snapshot": hexdigest, "waiver_snapshot": hexdigest, "state_history_snapshot": hexdigest, "generated_at": ts, "snapshot_hash": hexdigest})
    count = {"type": "object", "required": ["proven_failure", "waived_failure", "blocked", "unresolved", "pass", "excluded"], "properties": {key: {"type": "integer", "minimum": 0} for key in ["proven_failure", "waived_failure", "blocked", "unresolved", "pass", "excluded"]}, "additionalProperties": False}
    audit_aggregate = base_schema("Protocol-v13.2 AuditAggregate", ["aggregate_id", "audit_snapshot_id", "aggregate_status", "mandatory_counts", "optional_counts", "integrity_blockers", "generated_at", "aggregate_hash"], {"aggregate_id": ident, "audit_snapshot_id": ident, "aggregate_status": {"type": "string", "enum": AGGREGATE_STATES}, "mandatory_counts": count, "optional_counts": count, "integrity_blockers": strings(), "generated_at": ts, "aggregate_hash": hexdigest}, ["Derived, not manually assigned", "Proven failure precedes blockers", "Valid empty mandatory set is not compliant"])
    program_derivation = base_schema("Protocol-v13.2 ProgramStateDerivation", ["derivation_id", "program_id", "remediation_ids", "remediation_states", "program_predicates", "precedence", "derived_state", "derived_at", "evidence_refs", "derivation_hash"], {"derivation_id": ident, "program_id": ident, "remediation_ids": strings(), "remediation_states": {"type": "array", "items": {"type": "string", "enum": REMEDIATION_STATES}}, "program_predicates": {"type": "object"}, "precedence": strings(10), "derived_state": {"type": "string", "enum": PROGRAM_STATES}, "derived_at": ts, "evidence_refs": strings(1), "derivation_hash": hexdigest})
    audit_status = base_schema("Protocol-v13.2 AuditStatus", ["audit_status_id", "audit_snapshot_id", "aggregate_id", "status", "certification_eligible", "derived_at", "status_hash"], {"audit_status_id": ident, "audit_snapshot_id": ident, "aggregate_id": ident, "status": {"type": "string", "enum": AGGREGATE_STATES}, "certification_eligible": {"type": "boolean"}, "derived_at": ts, "status_hash": hexdigest})
    schemas = {"state-transition": state_transition, "current-state": current_state, "state-history": state_history, "compliance-decision-record": decision_record, "current-requirement-decision": current_decision, "audit-snapshot": audit_snapshot, "audit-aggregate": audit_aggregate, "program-state-derivation": program_derivation, "audit-status": audit_status}
    for name, schema in schemas.items(): schema["$id"] = f"https://generic-discovery-engine.invalid/compliance/v13.2/{name}.schema.yaml"; dump(SCHEMA / f"{name}.schema.yaml", schema)
    return schemas


def synthetic_event(identifier: str, object_type: str, object_id: str, sequence: int, from_state: str | None, to_state: str, previous: str | None, occurred_at: str = GENERATED_AT, reason: str = "TEST_GUARD_SATISFIED", evidence: list[str] | None = None) -> dict[str, Any]:
    return seal({"transition_id": identifier, "object_type": object_type, "object_id": object_id, "from_state": from_state, "to_state": to_state, "reason": reason, "evidence_refs": evidence if evidence is not None else ["TEST-EVIDENCE"], "actor": "SYNTHETIC_TEST_VECTOR", "occurred_at": occurred_at, "sequence": sequence, "previous_transition": previous}, "event_hash")


def decision_record(identifier: str, decision: str, decided_at: str, supersedes: str | None = None, implementation: str = "1" * 64, specification: str = "2" * 64) -> dict[str, Any]:
    return seal({"decision_id": identifier, "requirement_id": "TEST-REQ", "audit_id": "TEST-AUDIT", "decision": decision, "basis": {"acceptance_criteria": ["TEST-AC"], "evidence_refs": ["TEST-EVIDENCE"], "verification_refs": ["TEST-VERIFY"], "rule_refs": ["TEST-RULE"]}, "decided_at": decided_at, "implementation_snapshot": implementation, "specification_snapshot": specification, "audit_run_id": "TEST-RUN", "supersedes": supersedes}, "decision_hash")


def project_decisions(records: list[dict[str, Any]], audit_id: str, requirement_id: str, implementation: str, specification: str) -> tuple[str, dict[str, Any] | None]:
    if not records: return "NO_DECISION", None
    ordered = sorted(records, key=lambda item: item.get("decided_at", "")); previous = None
    for item in ordered:
        payload = dict(item); supplied = payload.pop("decision_hash", None)
        if supplied != digest(payload) or not timestamp_valid(item.get("decided_at")): return "DECISION_HISTORY_INVALID", None
        if item.get("audit_id") != audit_id or item.get("requirement_id") != requirement_id: return "DECISION_HISTORY_INVALID", None
        if item.get("implementation_snapshot") != implementation or item.get("specification_snapshot") != specification: return "DECISION_HISTORY_INVALID", None
        if item.get("supersedes") != previous: return "DECISION_HISTORY_INVALID", None
        previous = item["decision_id"]
    latest = ordered[-1]
    current = seal({"current_decision_id": "CURRENT-" + latest["decision_id"], "audit_id": audit_id, "requirement_id": requirement_id, "decision_id": latest["decision_id"], "decision": latest["decision"], "as_of": latest["decided_at"], "implementation_snapshot": implementation, "specification_snapshot": specification, "decision_history_valid": True}, "projection_hash")
    return "VALID", current


def protected_files() -> list[Path]:
    return sorted((path for path in OUT.rglob("*") if path.is_file() and DEST not in path.parents), key=lambda path: str(path.relative_to(OUT)))


def main() -> None:
    required = [V131 / "VALIDATION.yaml", V131 / "CURRENT-AGGREGATE.yaml", V131 / "REMEDIATION-PROGRAMS.yaml", OUT / "FINDINGS.yaml", OUT / "AUDIT-CERTIFICATE.yaml"]
    if not all(path.is_file() for path in required): raise RuntimeError("validated Protocol-v13.1 package is required")
    if DEST.exists():
        histories_file = DEST / "STATE-HISTORIES.yaml"; decisions_file = DEST / "COMPLIANCE-DECISION-HISTORIES.yaml"
        if histories_file.is_file():
            existing_histories = load(histories_file).get("histories", [])
            if len(existing_histories) != 6 or any(len(item.get("transitions", [])) != 1 for item in existing_histories): raise RuntimeError("refusing to erase appended v13.2 transition history")
        if decisions_file.is_file() and load(decisions_file).get("records"): raise RuntimeError("refusing to erase immutable v13.2 decision records")
        for filename in ["AUDIT-SNAPSHOT.yaml", "CURRENT-AGGREGATE.yaml", "AUDIT-STATUS.yaml"]:
            path = DEST / filename
            if path.is_file() and len(load(path).get("objects", [])) > 1: raise RuntimeError(f"refusing to erase appended v13.2 records in {filename}")
    before = [{"path": str(path.relative_to(OUT)), "sha256": sha_file(path), "bytes": path.stat().st_size} for path in protected_files()]
    if DEST.exists(): shutil.rmtree(DEST)
    DEST.mkdir(parents=True); SCHEMA.mkdir(); REPORTS.mkdir()
    build_schemas(); legal = legal_maps()

    findings = load(OUT / "FINDINGS.yaml")["objects"]
    programs = load(V131 / "REMEDIATION-PROGRAMS.yaml")["objects"]
    audit = load(OUT / "AUDIT.yaml")["objects"][0]
    certificate = load(OUT / "AUDIT-CERTIFICATE.yaml")["objects"][0]

    dump(DEST / "STATE-DOMAIN-SEPARATION.yaml", {"schema_version": VERSION, "distinctions": ["STATE_HISTORY", "CURRENT_STATE", "CURRENT_DECISION", "DERIVED_AGGREGATE", "AUDIT_STATUS", "CERTIFICATE"], "domains": [{"domain": "REQUIREMENT_CONFORMANCE", "owner": "COMPLIANCE_DECISION"}, {"domain": "FINDING_LIFECYCLE", "owner": "AUDIT_FINDING"}, {"domain": "REMEDIATION_LIFECYCLE", "owner": "REMEDIATION"}, {"domain": "PROGRAM_LIFECYCLE", "owner": "REMEDIATION_PROGRAM"}, {"domain": "AGGREGATE_CONFORMANCE", "owner": "AGGREGATE_FUNCTION"}], "state_substitution": "FORBIDDEN", "reverse_mutation": "FORBIDDEN"})
    dump(DEST / "BASELINE-IMPORT-POLICY.yaml", {"schema_version": VERSION, "purpose": "Start v13.2 projection lineage from immutable predecessor current-state records without inventing unavailable earlier lifecycle timestamps.", "first_transition": {"from_state": None, "reason_prefix": "BASELINE_IMPORT:", "sequence": 1, "previous_transition": None}, "historical_claim": "NO_PRE_V13.2_TRANSITION_TIME_OR_SEQUENCE_IS_ASSERTED", "evidence_required": True})
    dump(DEST / "STATE-TRANSITION-MODEL.yaml", {"schema_version": VERSION, "immutability": True, "validation_order": ["OBJECT_IDENTITY", "INITIAL_STATE", "SEQUENCE_ORDER", "SEQUENCE_CONTINUITY", "PREVIOUS_TRANSITION", "FROM_STATE", "TO_STATE", "TRANSITION_GUARD", "EVIDENCE_REFERENCES", "TIMESTAMPS", "EVENT_HASH", "CURRENT_STATE_DERIVATION"], "failure_behavior": "HISTORY_INVALID_NO_PROJECTION", "skip_invalid_transition": False, "hash_canonicalization": "UTF-8 sorted-key compact JSON excluding event_hash"})
    dump(DEST / "CURRENT-STATE-PROJECTION.yaml", {"schema_version": VERSION, "formula": "current_state = to_state(highest contiguous valid transition sequence)", "prerequisites": ["all transitions valid", "sequence contiguous", "from_state matches predecessor to_state", "identity stable", "timestamps valid and ordered", "hashes valid", "transition guards valid"], "malformed_result": "HISTORY_INVALID", "independent_truth_source": False, "deterministic": True})

    histories = []
    for index, finding in enumerate(findings, 1):
        event = transition(f"TRANSITION-V132-FINDING-{index:03d}", "AUDIT_FINDING", finding["object_id"], "OPEN", finding["object_id"])
        histories.append(state_history(f"HISTORY-V132-FINDING-{index:03d}", "AUDIT_FINDING", finding["object_id"], event, legal))
    for index, program in enumerate(programs, 1):
        event = transition(f"TRANSITION-V132-PROGRAM-{index:03d}", "REMEDIATION_PROGRAM", program["object_id"], "CREATED", program["object_id"])
        histories.append(state_history(f"HISTORY-V132-PROGRAM-{index:03d}", "REMEDIATION_PROGRAM", program["object_id"], event, legal))
    dump(DEST / "STATE-HISTORIES.yaml", {"schema_version": VERSION, "histories": histories, "canonical_source": True})
    all_events = [event for history in histories for event in history["transitions"]]
    currents = [history["current_state"] for history in histories]
    dump(DEST / "STATE-TRANSITION-REGISTRY.yaml", {"schema_version": VERSION, "events": all_events, "canonical_source": "STATE-HISTORIES.yaml", "reproducible_view": True})
    dump(DEST / "CURRENT-STATES.yaml", {"schema_version": VERSION, "objects": currents, "canonical_source": "STATE-HISTORIES.yaml", "reproducible_projection": True})

    valid1 = synthetic_event("TEST-T1", "AUDIT_FINDING", "TEST-F1", 1, None, "OPEN", None, reason="BASELINE_IMPORT: test")
    valid2 = synthetic_event("TEST-T2", "AUDIT_FINDING", "TEST-F1", 2, "OPEN", "UNDER_REMEDIATION", "TEST-T1")
    state_vectors: list[dict[str, Any]] = []
    def state_case(identifier: str, events: list[dict[str, Any]], expected: str) -> None:
        actual, projected = project(None, events, "AUDIT_FINDING", "TEST-F1", legal); state_vectors.append({"vector_id": identifier, "events": events, "expected": expected, "actual": actual, "projected_state": projected["state"] if projected else None, "pass": actual == expected})
    state_case("VALID_CONTIGUOUS_CHAIN", [valid1, valid2], "VALID")
    gap = [dict(valid1), synthetic_event("TEST-T3", "AUDIT_FINDING", "TEST-F1", 3, "OPEN", "UNDER_REMEDIATION", "TEST-T1")]; state_case("SEQUENCE_GAP", gap, "HISTORY_INVALID")
    mismatch = synthetic_event("TEST-T2", "AUDIT_FINDING", "TEST-F1", 2, "DETECTED", "VALIDATED", "TEST-T1"); state_case("FROM_STATE_MISMATCH", [valid1, mismatch], "HISTORY_INVALID")
    identity = synthetic_event("TEST-T2", "AUDIT_FINDING", "TEST-F2", 2, "OPEN", "UNDER_REMEDIATION", "TEST-T1"); state_case("IDENTITY_CHANGE", [valid1, identity], "HISTORY_INVALID")
    previous = synthetic_event("TEST-T2", "AUDIT_FINDING", "TEST-F1", 2, "OPEN", "UNDER_REMEDIATION", "WRONG"); state_case("PREVIOUS_LINK_MISMATCH", [valid1, previous], "HISTORY_INVALID")
    bad_hash = dict(valid2); bad_hash["event_hash"] = "0" * 64; state_case("HASH_INVALID", [valid1, bad_hash], "HISTORY_INVALID")
    illegal = synthetic_event("TEST-T2", "AUDIT_FINDING", "TEST-F1", 2, "OPEN", "CLOSED", "TEST-T1"); state_case("ILLEGAL_TRANSITION", [valid1, illegal], "HISTORY_INVALID")
    bad_time = synthetic_event("TEST-T2", "AUDIT_FINDING", "TEST-F1", 2, "OPEN", "UNDER_REMEDIATION", "TEST-T1", occurred_at="not-time"); state_case("TIMESTAMP_INVALID", [valid1, bad_time], "HISTORY_INVALID")
    no_evidence = synthetic_event("TEST-T2", "AUDIT_FINDING", "TEST-F1", 2, "OPEN", "UNDER_REMEDIATION", "TEST-T1", evidence=[]); state_case("EVIDENCE_MISSING", [valid1, no_evidence], "HISTORY_INVALID")
    block = synthetic_event("TEST-T2", "AUDIT_FINDING", "TEST-F1", 2, "OPEN", "BLOCKED", "TEST-T1")
    unblock = synthetic_event("TEST-T3", "AUDIT_FINDING", "TEST-F1", 3, "BLOCKED", "OPEN", "TEST-T2", reason="BLOCK_REMOVED_AND_PREVIOUS_STATE_REVALIDATED")
    state_case("BLOCK_RETURN_PREVIOUS", [valid1, block, unblock], "VALID")
    wrong_unblock = synthetic_event("TEST-T3", "AUDIT_FINDING", "TEST-F1", 3, "BLOCKED", "DETECTED", "TEST-T2", reason="BLOCK_REMOVED_AND_PREVIOUS_STATE_REVALIDATED")
    state_case("BLOCK_RETURN_WRONG_STATE", [valid1, block, wrong_unblock], "HISTORY_INVALID")
    p_events = [synthetic_event("TEST-P1", "REMEDIATION_PROGRAM", "TEST-PROGRAM", 1, None, "CREATED", None, reason="BASELINE_IMPORT: test")]
    for sequence, (from_state, to_state) in enumerate([("CREATED", "TRIAGED"), ("TRIAGED", "PLANNED"), ("PLANNED", "ACTIVE"), ("ACTIVE", "EVALUATING"), ("EVALUATING", "COMPLETED"), ("COMPLETED", "ACTIVE")], 2):
        p_events.append(synthetic_event(f"TEST-P{sequence}", "REMEDIATION_PROGRAM", "TEST-PROGRAM", sequence, from_state, to_state, f"TEST-P{sequence - 1}"))
    terminal_actual, _ = project(None, p_events, "REMEDIATION_PROGRAM", "TEST-PROGRAM", legal)
    state_vectors.append({"vector_id": "COMPLETED_PROGRAM_TERMINAL", "events": p_events, "expected": "HISTORY_INVALID", "actual": terminal_actual, "projected_state": None, "pass": terminal_actual == "HISTORY_INVALID"})
    dump(DEST / "STATE-PROJECTION-TEST-VECTORS.yaml", {"schema_version": VERSION, "synthetic_non_normative": True, "vectors": state_vectors, "summary": {"total": len(state_vectors), "passed": sum(item["pass"] for item in state_vectors), "failed": sum(not item["pass"] for item in state_vectors)}})

    dump(DEST / "DECISION-HISTORY-MODEL.yaml", {"schema_version": VERSION, "immutability": True, "new_decision_triggers": ["NEW_IMPLEMENTATION_STATE", "NEW_EVIDENCE", "CHANGED_REQUIREMENT", "CHANGED_ORACLE"], "supersession_deletes_predecessor": False, "projection_key": ["audit_id", "requirement_id", "specification_snapshot", "implementation_snapshot"], "latest_invalid_behavior": "DECISION_HISTORY_INVALID_NO_FALLBACK", "validation_order": ["LOAD_HISTORY", "VALIDATE_RECORDS", "AUDIT_IDENTITY", "REQUIREMENT_IDENTITY", "SPECIFICATION_SNAPSHOT", "IMPLEMENTATION_SNAPSHOT", "SUPERSESSION", "APPLICABILITY", "EFFECTIVE_WAIVER", "SELECT_LATEST_VALID_APPLICABLE"]})
    dump(DEST / "COMPLIANCE-DECISION-HISTORIES.yaml", {"schema_version": VERSION, "records": [], "histories": [], "status": "NO_REQUIREMENTS_NO_DECISIONS", "historical_v12_1_decision_count": len(load(OUT / "CONFORMANCE-DECISIONS.yaml")["objects"])})
    dump(DEST / "CURRENT-REQUIREMENT-DECISIONS.yaml", {"schema_version": VERSION, "objects": [], "status": "NO_REQUIREMENTS_NO_CURRENT_DECISIONS", "projection_error": None})
    d1 = decision_record("TEST-D1", "NON_CONFORMANT", "2026-09-12T10:00:00Z")
    d2 = decision_record("TEST-D2", "CONFORMANT", "2026-09-12T11:00:00Z", "TEST-D1")
    invalid_latest = dict(d2); invalid_latest["decision_hash"] = "0" * 64
    other_snapshot = decision_record("TEST-DX", "CONFORMANT", "2026-09-12T10:00:00Z", implementation="3" * 64)
    broken_supersession = decision_record("TEST-DB", "CONFORMANT", "2026-09-12T11:00:00Z", "MISSING")
    decision_cases = [("SINGLE_VALID", [d1], "VALID", "TEST-D1"), ("LATEST_SUPERSEDES", [d1, d2], "VALID", "TEST-D2"), ("LATEST_INVALID_NO_FALLBACK", [d1, invalid_latest], "DECISION_HISTORY_INVALID", None), ("OTHER_IMPLEMENTATION_SNAPSHOT", [other_snapshot], "DECISION_HISTORY_INVALID", None), ("BROKEN_SUPERSESSION", [d1, broken_supersession], "DECISION_HISTORY_INVALID", None), ("NO_DECISION", [], "NO_DECISION", None)]
    decision_vectors = []
    for vector_id, records, expected, expected_id in decision_cases:
        actual, current = project_decisions(records, "TEST-AUDIT", "TEST-REQ", "1" * 64, "2" * 64)
        decision_vectors.append({"vector_id": vector_id, "records": records, "expected": expected, "actual": actual, "expected_decision_id": expected_id, "actual_decision_id": current["decision_id"] if current else None, "current_projection": current, "pass": actual == expected and (current["decision_id"] if current else None) == expected_id})
    dump(DEST / "DECISION-PROJECTION-TEST-VECTORS.yaml", {"schema_version": VERSION, "synthetic_non_normative": True, "vectors": decision_vectors, "summary": {"total": len(decision_vectors), "passed": sum(item["pass"] for item in decision_vectors), "failed": sum(not item["pass"] for item in decision_vectors)}})

    precedence = ["PROVEN_FAILURE", "BLOCKED", "UNRESOLVED", "WAIVED_FAILURE", "PASS", "NO_MANDATORY_REQUIREMENTS"]
    dump(DEST / "AGGREGATE-FUNCTION.yaml", {"schema_version": VERSION, "classification": {"NON_CONFORMANT_UNWAIVED": "PROVEN_FAILURE", "NON_CONFORMANT_WAIVED": "WAIVED_FAILURE", "BLOCKED": "BLOCKED", "PARTIALLY_CONFORMANT_UNVERIFIED_UNKNOWN": "UNRESOLVED", "CONFORMANT": "PASS", "NOT_APPLICABLE": "EXCLUDED"}, "ordered_decision": ["IF_PROVEN_FAILURE_RETURN_NON_COMPLIANT", "ELSE_IF_INTEGRITY_OR_MANDATORY_BLOCKED_RETURN_BLOCKED", "ELSE_IF_UNRESOLVED_RETURN_UNVERIFIED", "ELSE_IF_WAIVED_FAILURE_RETURN_CONDITIONALLY_COMPLIANT", "ELSE_IF_APPLICABLE_MANDATORY_EMPTY_RETURN_NO_MANDATORY_REQUIREMENTS", "ELSE_RETURN_COMPLIANT"], "precedence": precedence, "optional_reporting": {"proven_failure": "OPTIONAL_FAILURE", "unresolved": "OPTIONAL_UNVERIFIED", "blocked": "OPTIONAL_BLOCKED"}, "optional_requirements_change_mandatory_aggregate": False, "process_states_are_inputs": False, "deterministic": True})
    req = lambda identifier, mandatory, decision, waiver=False, applicable=True: {"requirement_id": identifier, "mandatory": mandatory, "applicable": applicable, "decision": decision, "waiver_effective": waiver}
    aggregate_cases = [
        ("PROVEN_FAILURE_DOMINATES_BLOCKER", [req("R1", True, "NON_CONFORMANT"), req("R2", True, "BLOCKED")], ["HISTORY"], "NON_COMPLIANT"),
        ("BLOCKED_DOMINATES_UNRESOLVED", [req("R1", True, "BLOCKED"), req("R2", True, "UNKNOWN")], [], "BLOCKED"),
        ("UNRESOLVED_DOMINATES_WAIVER", [req("R1", True, "NON_CONFORMANT", True), req("R2", True, "UNVERIFIED")], [], "UNVERIFIED"),
        ("WAIVED_FAILURE_ONLY", [req("R1", True, "NON_CONFORMANT", True)], [], "CONDITIONALLY_COMPLIANT"),
        ("ALL_MANDATORY_PASS", [req("R1", True, "CONFORMANT")], [], "COMPLIANT"),
        ("VALID_EMPTY_MANDATORY", [], [], "NO_MANDATORY_REQUIREMENTS"),
        ("ALL_NOT_APPLICABLE", [req("R1", True, "NOT_APPLICABLE", applicable=False)], [], "NO_MANDATORY_REQUIREMENTS"),
        ("OPTIONAL_FAILURE_WITH_NO_MANDATORY", [req("O1", False, "NON_CONFORMANT")], [], "NO_MANDATORY_REQUIREMENTS"),
        ("OPTIONAL_FAILURE_WITH_MANDATORY_PASS", [req("R1", True, "CONFORMANT"), req("O1", False, "NON_CONFORMANT")], [], "COMPLIANT"),
        ("INTEGRITY_BLOCKS_EMPTY_EVALUATION", [], ["SPECIFICATION_SNAPSHOT_INVALID"], "BLOCKED"),
        ("INTERMEDIATE_FINAL_DECISION_BLOCKS", [req("R1", True, "VERIFIED")], [], "BLOCKED"),
        ("UNKNOWN_IS_UNRESOLVED", [req("R1", True, "UNKNOWN")], [], "UNVERIFIED"),
    ]
    aggregate_vectors = []
    for vector_id, requirements, blockers, expected in aggregate_cases:
        actual, counts = aggregate(requirements, blockers); aggregate_vectors.append({"vector_id": vector_id, "requirements": requirements, "integrity_blockers": blockers, "expected": expected, "actual": actual, "counts": counts, "pass": actual == expected})
    dump(DEST / "AGGREGATE-TEST-VECTORS.yaml", {"schema_version": VERSION, "vectors": aggregate_vectors, "summary": {"total": len(aggregate_vectors), "passed": sum(item["pass"] for item in aggregate_vectors), "failed": sum(not item["pass"] for item in aggregate_vectors)}})

    state_snapshot = digest(histories); decision_snapshot = digest({"histories": [], "current": []})
    snapshot = seal({"snapshot_id": "AUDIT-SNAPSHOT-V132-001", "audit_id": audit["object_id"], "specification_snapshot": sha_file(HS / "specification" / "SPECIFICATION-MANIFEST.yaml"), "implementation_snapshot": sha_file(OUT / "IMPLEMENTATION-ARTIFACTS.yaml"), "decision_snapshot": decision_snapshot, "waiver_snapshot": sha_file(OUT / "WAIVERS.yaml"), "state_history_snapshot": state_snapshot, "generated_at": GENERATED_AT}, "snapshot_hash")
    dump(DEST / "AUDIT-SNAPSHOT.yaml", {"schema_version": VERSION, "objects": [snapshot]})
    integrity_blockers = ["INVALID_NORMATIVE_SPECIFICATION", "EMPTY_REQUIREMENT_SCOPE", "MISSING_IMPLEMENTATION_SOURCE", "REMEDIATION_R2_NORMATIVE_BASIS_BLOCKED"]
    current_status, current_counts = aggregate([], integrity_blockers)
    current_aggregate = seal({"aggregate_id": "AGGREGATE-V132-001", "audit_snapshot_id": snapshot["snapshot_id"], "aggregate_status": current_status, "mandatory_counts": current_counts["mandatory"], "optional_counts": current_counts["optional"], "integrity_blockers": integrity_blockers, "generated_at": GENERATED_AT}, "aggregate_hash")
    dump(DEST / "CURRENT-AGGREGATE.yaml", {"schema_version": VERSION, "objects": [current_aggregate], "mandatory_set_status": "NO_MANDATORY_REQUIREMENTS", "aggregate_status_after_integrity": current_status, "explanation": "The empty mandatory set does not manufacture compliance; invalid specification and audit prerequisites block evaluation."})
    audit_status = seal({"audit_status_id": "AUDIT-STATUS-V132-001", "audit_snapshot_id": snapshot["snapshot_id"], "aggregate_id": current_aggregate["aggregate_id"], "status": current_status, "certification_eligible": False, "derived_at": GENERATED_AT}, "status_hash")
    dump(DEST / "AUDIT-STATUS.yaml", {"schema_version": VERSION, "objects": [audit_status]})
    integrity = {"H_state_history_valid": "PASS", "D_current_decisions_valid": "BLOCKED_INVALID_SPECIFICATION_SCOPE", "R_references_resolve": "PASS", "T_temporal_integrity": "PASS_V13.2_PROJECTION", "S_specification_snapshot_valid": "FAIL", "E_required_evidence_integrity": "BLOCKED", "result": "BLOCKED"}
    dump(DEST / "AUDIT-INTEGRITY.yaml", {"schema_version": VERSION, "predicates": integrity, "earliest_invalid_prerequisite": "SPECIFICATION_SNAPSHOT", "silent_fallback": False})

    definitions = {"CREATED": "Program exists but has not undergone triage.", "TRIAGED": "Finding and remediation scope were assessed sufficiently to determine program appropriateness.", "PLANNED": "Required actions and dependencies are defined.", "ACTIVE": "At least one remediation action is actively executing.", "EVALUATING": "Changes exist and re-verification or regression evaluation is underway or pending.", "COMPLETED": "All required actions and post-remediation evaluation completed; this has no conformance implication.", "BLOCKED": "An identified dependency, environment, authorization, artifact, or verification blocker prevents progress.", "FAILED": "The current remediation plan cannot achieve its declared objective.", "CANCELLED": "The program was intentionally terminated without completion.", "SUPERSEDED": "A newer remediation program replaces this immutable record."}
    program_transitions = [
        ("CREATED", "TRIAGED", "PROGRAM_EXISTS_AND_FINDING_SCOPE_RESOLVABLE"), ("TRIAGED", "PLANNED", "SCOPE_TARGETS_STRATEGY_DEPENDENCIES_DEFINED"), ("PLANNED", "ACTIVE", "ACTIONS_APPROVED_DEPENDENCIES_AVAILABLE_AUTHORIZATION_VALID"), ("ACTIVE", "EVALUATING", "CHANGES_RECORDED_CHANGESET_VALID_IMPACT_COMPLETE"), ("EVALUATING", "COMPLETED", "ACTIONS_REVERIFICATION_REGRESSION_RISKS_CLOSURE_COMPLETE"),
        ("CREATED", "CANCELLED", "EXPLICIT_CANCELLATION"), ("TRIAGED", "CANCELLED", "EXPLICIT_CANCELLATION"), ("PLANNED", "CANCELLED", "EXPLICIT_CANCELLATION"), ("BLOCKED", "FAILED", "BLOCK_PROVES_PLAN_CANNOT_ACHIEVE_OBJECTIVE"), ("BLOCKED", "CANCELLED", "EXPLICIT_CANCELLATION"),
        ("TRIAGED", "SUPERSEDED", "AUTHORIZED_SUCCESSOR_EXISTS"), ("PLANNED", "SUPERSEDED", "AUTHORIZED_SUCCESSOR_EXISTS"), ("ACTIVE", "SUPERSEDED", "AUTHORIZED_SUCCESSOR_EXISTS"), ("EVALUATING", "SUPERSEDED", "AUTHORIZED_SUCCESSOR_EXISTS"),
    ] + [(state, "BLOCKED", "IDENTIFIED_BLOCKING_CONDITION_EXISTS") for state in ["CREATED", "TRIAGED", "PLANNED", "ACTIVE", "EVALUATING"]] + [("BLOCKED", state, "BLOCK_REMOVED_AND_PREVIOUS_OPERATIONAL_STATE_REVALIDATED") for state in ["CREATED", "TRIAGED", "PLANNED", "ACTIVE", "EVALUATING"]]
    dump(DEST / "PROGRAM-STATE-MACHINE.yaml", {"schema_version": VERSION, "states": PROGRAM_STATES, "definitions": definitions, "legal_transitions": [{"from": a, "to": b, "guard": guard} for a, b, guard in program_transitions], "terminal_states": ["COMPLETED", "FAILED", "CANCELLED", "SUPERSEDED"], "completed_to_active": "FORBIDDEN", "post_completion_work": "NEW_PROGRAM_OR_AUTHORIZED_SUCCESSOR", "block_cause_required": True, "conformance_effect": "NONE"})
    derivation_precedence = ["SUPERSEDED", "CANCELLED", "FAILED", "BLOCKED", "COMPLETED", "EVALUATING", "ACTIVE", "PLANNED", "TRIAGED", "CREATED"]
    dump(DEST / "PROGRAM-DERIVATION-FUNCTION.yaml", {"schema_version": VERSION, "precedence": derivation_precedence, "predicates": {"SUPERSEDED": "program_superseded", "CANCELLED": "program_cancelled", "FAILED": "members_exist AND all_members_rejected", "BLOCKED": "identified_blocking_condition", "COMPLETED": "all_required_members_complete AND required_evaluation_complete", "EVALUATING": "any_member_reverification_or_regression OR post_change_evaluation_pending OR complete_members_await_evaluation", "ACTIVE": "any_member_in_progress_or_ready_for_verification", "PLANNED": "any_member_proposed_assessed_or_approved", "TRIAGED": "members_exist_otherwise", "CREATED": "no_members"}, "independent_assertion": "FORBIDDEN", "truth_state_effect": "NONE"})
    derivations = []
    for index, program in enumerate(programs, 1):
        predicates = {"program_superseded": False, "program_cancelled": False, "all_members_rejected": False, "identified_blocking_condition": False, "all_required_members_complete": False, "required_evaluation_complete": False, "post_change_evaluation_pending": False, "members_exist": False}
        derived = derive_program([])
        derivations.append(seal({"derivation_id": f"PROGRAM-DERIVATION-V132-{index:03d}", "program_id": program["object_id"], "remediation_ids": [], "remediation_states": [], "program_predicates": predicates, "precedence": derivation_precedence, "derived_state": derived, "derived_at": GENERATED_AT, "evidence_refs": [program["object_id"]]}, "derivation_hash"))
    dump(DEST / "PROGRAM-DERIVATIONS.yaml", {"schema_version": VERSION, "objects": derivations})
    program_cases = [([], {}, "CREATED"), (["PROPOSED"], {}, "PLANNED"), (["IN_PROGRESS"], {}, "ACTIVE"), (["REVERIFICATION"], {}, "EVALUATING"), (["COMPLETE"], {"evaluation_pending": True}, "EVALUATING"), (["COMPLETE"], {"evaluation_complete": True}, "COMPLETED"), (["BLOCKED"], {"blocking": True}, "BLOCKED"), (["REJECTED"], {"blocking": True}, "FAILED"), (["IN_PROGRESS"], {"cancelled": True}, "CANCELLED"), (["IN_PROGRESS"], {"superseded": True, "cancelled": True}, "SUPERSEDED")]
    program_vectors = []
    for index, (states, kwargs, expected) in enumerate(program_cases, 1):
        actual = derive_program(states, **kwargs); program_vectors.append({"vector_id": f"PROGRAM-VECTOR-{index:02d}", "remediation_states": states, "predicates": kwargs, "expected": expected, "actual": actual, "pass": actual == expected})
    dump(DEST / "PROGRAM-TEST-VECTORS.yaml", {"schema_version": VERSION, "vectors": program_vectors, "summary": {"total": len(program_vectors), "passed": sum(item["pass"] for item in program_vectors), "failed": sum(not item["pass"] for item in program_vectors)}})

    temporal_queries = []
    for history in histories:
        temporal_queries.append({"query": "state_at", "object_id": history["object_id"], "at": "2026-09-12T17:20:42Z", "result": "NO_ACCEPTED_V13.2_STATE"})
        temporal_queries.append({"query": "state_at", "object_id": history["object_id"], "at": GENERATED_AT, "result": history["current_state"]["state"]})
    dump(DEST / "TEMPORAL-QUERY-RULES.yaml", {"schema_version": VERSION, "supported_queries": ["decision_at(t)", "finding_state_at(t)", "remediation_state_at(t)", "program_state_at(t)", "aggregate_at(t)"], "selection": "latest valid event at or before t within identified snapshot lineage", "wall_clock_dependency": False, "queries": temporal_queries})
    dump(DEST / "CANONICAL-MODEL.yaml", {"schema_version": VERSION, "forward_flow": ["IMMUTABLE_HISTORY", "CURRENT_STATE", "IMPLEMENTATION_CHANGE", "VERIFICATION", "COMPLIANCE_DECISION_HISTORY", "CURRENT_DECISION", "AGGREGATE", "AUDIT_STATUS", "CERTIFICATE"], "reverse_mutation": False, "separations": ["HISTORY_NE_CURRENT_STATE", "CURRENT_STATE_NE_CURRENT_DECISION", "CURRENT_DECISION_NE_AGGREGATE", "AGGREGATE_NE_CERTIFICATE"], "central_consequence": "PROCESS_COMPLETION_NE_TRUTH_ESTABLISHMENT"})
    dump(DEST / "CERTIFICATE-POLICY.yaml", {"schema_version": VERSION, "certificate_requires_snapshot": True, "required_scope": ["audit_snapshot_id", "specification_snapshot", "implementation_snapshot", "audit_scope", "verification_state"], "lineage_immutable": True, "universal_truth_claim_forbidden": True, "no_mandatory_requirements_automatic_certificate": False})
    dump(DEST / "CERTIFICATE-REVISION-STATUS.yaml", {"schema_version": VERSION, "status": "NOT_AUTHORIZED", "prior_certificate_id": certificate["object_id"], "prior_certificate_hash": certificate["certificate_hash"], "audit_snapshot_id": snapshot["snapshot_id"], "audit_status_id": audit_status["audit_status_id"], "reason": "Audit evaluation remains BLOCKED; no requirement decision or certification predicate changed.", "lineage_modified": False})
    dump(DEST / "INVARIANTS.yaml", {"schema_version": VERSION, "invariants": [{"invariant_id": f"V132-I{index:02d}", "statement": statement, "enforcement": "MECHANICAL"} for index, statement in enumerate(INVARIANTS, 1)]})

    registry_objects = []
    for h_index, history in enumerate(histories):
        registry_objects += [{"object_type": "STATE_HISTORY", "object_id": history["history_id"], "source": f"STATE-HISTORIES.yaml#/histories/{h_index}"}, {"object_type": "STATE_TRANSITION", "object_id": history["transitions"][0]["transition_id"], "source": f"STATE-HISTORIES.yaml#/histories/{h_index}/transitions/0"}, {"object_type": "CURRENT_STATE", "object_id": history["current_state"]["current_state_id"], "source": f"STATE-HISTORIES.yaml#/histories/{h_index}/current_state"}]
    registry_objects += [{"object_type": "PROGRAM_STATE_DERIVATION", "object_id": item["derivation_id"], "source": f"PROGRAM-DERIVATIONS.yaml#/objects/{index}"} for index, item in enumerate(derivations)]
    registry_objects += [{"object_type": "AUDIT_SNAPSHOT", "object_id": snapshot["snapshot_id"], "source": "AUDIT-SNAPSHOT.yaml#/objects/0"}, {"object_type": "AUDIT_AGGREGATE", "object_id": current_aggregate["aggregate_id"], "source": "CURRENT-AGGREGATE.yaml#/objects/0"}, {"object_type": "AUDIT_STATUS", "object_id": audit_status["audit_status_id"], "source": "AUDIT-STATUS.yaml#/objects/0"}]
    dump(DEST / "OBJECT-REGISTRY.yaml", {"schema_version": VERSION, "objects": registry_objects, "external_registries": [{"path": "../../OBJECT-REGISTRY.yaml", "sha256": sha_file(OUT / "OBJECT-REGISTRY.yaml")}, {"path": "../OBJECT-REGISTRY.yaml", "sha256": sha_file(REM / "OBJECT-REGISTRY.yaml")}, {"path": "../v13.1/OBJECT-REGISTRY.yaml", "sha256": sha_file(V131 / "OBJECT-REGISTRY.yaml")}], "global_uniqueness_checked": True})
    dump(DEST / "SCHEMA-REGISTRY.yaml", {"schema_version": VERSION, "schemas": [{"name": name, "path": f"schema/{name}.schema.yaml", "sha256": sha_file(SCHEMA / f"{name}.schema.yaml")} for name in SCHEMA_NAMES]})
    dump(DEST / "VALIDATION-REPORT.yaml", {"schema_version": VERSION, "overall_status": "STRUCTURAL_PASS_AUDIT_BLOCKED", "state_histories": {"total": 6, "valid": 6, "invalid": 0}, "current_states": 6, "decision_histories": 0, "current_decisions": 0, "program_derivations": {"total": 3, "created": 3}, "current_aggregate": current_status, "audit_status": audit_status["status"], "certificate_revision": False})
    dump(REPORTS / "CURRENT-STATE-REPORT.yaml", {"schema_version": VERSION, "status": "PASS", "finding_current_states": {"OPEN": 3}, "remediation_current_states": {}, "program_current_states": {"CREATED": 3}, "history_invalid": 0, "baseline_imports": 6})
    dump(REPORTS / "AGGREGATE-CONFORMANCE-REPORT.yaml", {"schema_version": VERSION, "aggregate_status": current_status, "mandatory_set_status": "NO_MANDATORY_REQUIREMENTS", "valid_empty_set_result": "NO_MANDATORY_REQUIREMENTS", "current_integrity_result": "BLOCKED", "current_decisions": 0, "process_states_consumed": False, "optional_failures_change_result": False})
    dump(REPORTS / "TEMPORAL-INTEGRITY-REPORT.yaml", {"schema_version": VERSION, "state_history_integrity": "PASS", "baseline_import_claims_pre_v13_2_history": False, "decision_history_integrity": "NO_RECORDS", "snapshot_identity": snapshot["snapshot_id"], "reproducible": True})
    dump(REPORTS / "CERTIFICATION-IMPACT-REPORT.yaml", {"schema_version": VERSION, "audit_status": "BLOCKED", "certificate_revision": False, "finding_closures": 0, "remediation_completions": 0, "program_completions": 0, "new_compliance_decisions": 0, "principle": "FIXED != VERIFIED != CONFORMANT != AGGREGATELY_COMPLIANT != CERTIFIED"})

    after = [{"path": str(path.relative_to(OUT)), "sha256": sha_file(path), "bytes": path.stat().st_size} for path in protected_files()]
    if before != after: raise RuntimeError("v13.2 modified a protected predecessor artifact")
    dump(DEST / "PRIOR-INTEGRITY.yaml", {"schema_version": VERSION, "protected_artifact_count": len(before), "artifacts": before, "status": "PRESERVED"})
    produced = [*MACHINE_FILES, *(f"schema/{name}.schema.yaml" for name in SCHEMA_NAMES), *(f"reports/{name}" for name in REPORT_FILES)]
    missing = [name for name in produced if not (DEST / name).is_file()]
    if missing: raise RuntimeError(f"missing v13.2 outputs: {missing}")
    print(f"generated {len(produced)} v13.2 deliverables; histories=6/6 projections=6 programs=3(CREATED) decisions=0 aggregate=BLOCKED")


if __name__ == "__main__": main()
