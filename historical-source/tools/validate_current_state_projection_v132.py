#!/usr/bin/env python3
"""Independent Protocol-v13.2 history/projection/aggregate validator."""
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
REM = OUT / "remediation"
V131 = REM / "v13.1"
DEST = REM / "v13.2"
SCHEMA = DEST / "schema"
VERSION = "13.2"
FINDING_STATES = {"DETECTED", "VALIDATED", "CLASSIFIED", "OPEN", "UNDER_REMEDIATION", "RESOLVED", "CLOSED", "REJECTED", "WAIVED", "SUPERSEDED", "BLOCKED"}
REMEDIATION_STATES = {"PROPOSED", "ASSESSED", "APPROVED", "IN_PROGRESS", "READY_FOR_VERIFICATION", "REVERIFICATION", "REGRESSION", "COMPLETE", "FAILED", "BLOCKED", "REJECTED", "SUPERSEDED", "CANCELLED"}
PROGRAM_STATES = {"CREATED", "TRIAGED", "PLANNED", "ACTIVE", "EVALUATING", "COMPLETED", "BLOCKED", "FAILED", "CANCELLED", "SUPERSEDED"}
DECISION_STATES = {"UNASSESSED", "MAPPED", "VERIFIED", "CONFORMANT", "PARTIALLY_CONFORMANT", "NON_CONFORMANT", "UNVERIFIED", "BLOCKED", "UNKNOWN", "NOT_APPLICABLE"}
AGGREGATE_STATES = {"NON_COMPLIANT", "BLOCKED", "UNVERIFIED", "CONDITIONALLY_COMPLIANT", "COMPLIANT", "NO_MANDATORY_REQUIREMENTS"}
SCHEMA_NAMES = ["state-transition", "current-state", "state-history", "compliance-decision-record", "current-requirement-decision", "audit-snapshot", "audit-aggregate", "program-state-derivation", "audit-status"]
MACHINE_FILES = ["STATE-DOMAIN-SEPARATION.yaml", "BASELINE-IMPORT-POLICY.yaml", "STATE-TRANSITION-MODEL.yaml", "CURRENT-STATE-PROJECTION.yaml", "STATE-HISTORIES.yaml", "STATE-TRANSITION-REGISTRY.yaml", "CURRENT-STATES.yaml", "STATE-PROJECTION-TEST-VECTORS.yaml", "DECISION-HISTORY-MODEL.yaml", "COMPLIANCE-DECISION-HISTORIES.yaml", "CURRENT-REQUIREMENT-DECISIONS.yaml", "DECISION-PROJECTION-TEST-VECTORS.yaml", "AGGREGATE-FUNCTION.yaml", "AGGREGATE-TEST-VECTORS.yaml", "AUDIT-SNAPSHOT.yaml", "CURRENT-AGGREGATE.yaml", "AUDIT-STATUS.yaml", "AUDIT-INTEGRITY.yaml", "PROGRAM-STATE-MACHINE.yaml", "PROGRAM-DERIVATION-FUNCTION.yaml", "PROGRAM-DERIVATIONS.yaml", "PROGRAM-TEST-VECTORS.yaml", "TEMPORAL-QUERY-RULES.yaml", "CANONICAL-MODEL.yaml", "CERTIFICATE-POLICY.yaml", "CERTIFICATE-REVISION-STATUS.yaml", "INVARIANTS.yaml", "OBJECT-REGISTRY.yaml", "SCHEMA-REGISTRY.yaml", "VALIDATION-REPORT.yaml", "PRIOR-INTEGRITY.yaml"]
REPORT_FILES = ["CURRENT-STATE-REPORT.yaml", "AGGREGATE-CONFORMANCE-REPORT.yaml", "TEMPORAL-INTEGRITY-REPORT.yaml", "CERTIFICATION-IMPACT-REPORT.yaml"]
DELIVERABLES = [*MACHINE_FILES, *(f"schema/{name}.schema.yaml" for name in SCHEMA_NAMES), *(f"reports/{name}" for name in REPORT_FILES)]
ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]*$")


def load(path: Path) -> Any: return json.loads(path.read_text(encoding="utf-8"))
def canonical(value: Any) -> bytes: return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
def digest(value: Any) -> str: return hashlib.sha256(canonical(value)).hexdigest()
def sha_file(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()
def valid_time(value: Any) -> bool:
    if not isinstance(value, str): return False
    try: return datetime.fromisoformat(value.replace("Z", "+00:00")).tzinfo is not None
    except ValueError: return False


def schema_errors(value: Any, schema: dict[str, Any], schemas: dict[str, Any], current: str, path: str = "$") -> list[str]:
    if "$ref" in schema:
        target = Path(schema["$ref"]).name.replace(".schema.yaml", "")
        return schema_errors(value, schemas[target], schemas, target, path)
    if "oneOf" in schema:
        matches = [schema_errors(value, candidate, schemas, current, path) for candidate in schema["oneOf"]]
        return [] if sum(not result for result in matches) == 1 else [f"{path}: oneOf"]
    errors: list[str] = []; expected = schema.get("type")
    if expected:
        tests = {"object": isinstance(value, dict), "array": isinstance(value, list), "string": isinstance(value, str), "integer": isinstance(value, int) and not isinstance(value, bool), "boolean": isinstance(value, bool), "null": value is None}
        if not tests.get(expected, False): return [f"{path}: type {expected}"]
    if "const" in schema and value != schema["const"]: errors.append(f"{path}: const")
    if "enum" in schema and value not in schema["enum"]: errors.append(f"{path}: enum")
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0): errors.append(f"{path}: minLength")
        if "pattern" in schema and re.fullmatch(schema["pattern"], value) is None: errors.append(f"{path}: pattern")
        if schema.get("format") == "date-time" and not valid_time(value): errors.append(f"{path}: date-time")
    if isinstance(value, int) and not isinstance(value, bool) and value < schema.get("minimum", value): errors.append(f"{path}: minimum")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0): errors.append(f"{path}: minItems")
        if schema.get("uniqueItems") and len({canonical(item) for item in value}) != len(value): errors.append(f"{path}: uniqueItems")
        if "items" in schema:
            for index, item in enumerate(value): errors.extend(schema_errors(item, schema["items"], schemas, current, f"{path}[{index}]"))
    if isinstance(value, dict):
        props = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in value: errors.append(f"{path}: missing {key}")
        if schema.get("additionalProperties") is False:
            for key in value:
                if key not in props: errors.append(f"{path}: additional {key}")
        for key, item in value.items():
            if key in props: errors.extend(schema_errors(item, props[key], schemas, current, f"{path}.{key}"))
    return errors


def legal_maps() -> dict[str, set[tuple[str, str]]]:
    finding = {("DETECTED", "VALIDATED"), ("DETECTED", "REJECTED"), ("VALIDATED", "CLASSIFIED"), ("CLASSIFIED", "OPEN"), ("OPEN", "UNDER_REMEDIATION"), ("OPEN", "WAIVED"), ("OPEN", "SUPERSEDED"), ("UNDER_REMEDIATION", "RESOLVED"), ("UNDER_REMEDIATION", "OPEN"), ("RESOLVED", "CLOSED"), ("RESOLVED", "OPEN")} | {(state, "BLOCKED") for state in ["DETECTED", "VALIDATED", "CLASSIFIED", "OPEN", "UNDER_REMEDIATION", "RESOLVED"]}
    remediation = {("PROPOSED", "ASSESSED"), ("PROPOSED", "REJECTED"), ("ASSESSED", "APPROVED"), ("ASSESSED", "REJECTED"), ("APPROVED", "IN_PROGRESS"), ("IN_PROGRESS", "READY_FOR_VERIFICATION"), ("IN_PROGRESS", "BLOCKED"), ("READY_FOR_VERIFICATION", "REVERIFICATION"), ("REVERIFICATION", "FAILED"), ("REVERIFICATION", "REGRESSION"), ("REGRESSION", "FAILED"), ("REGRESSION", "COMPLETE"), ("FAILED", "IN_PROGRESS")}
    program = {("CREATED", "TRIAGED"), ("TRIAGED", "PLANNED"), ("PLANNED", "ACTIVE"), ("ACTIVE", "EVALUATING"), ("EVALUATING", "COMPLETED"), ("CREATED", "CANCELLED"), ("TRIAGED", "CANCELLED"), ("PLANNED", "CANCELLED"), ("BLOCKED", "FAILED"), ("BLOCKED", "CANCELLED"), ("TRIAGED", "SUPERSEDED"), ("PLANNED", "SUPERSEDED"), ("ACTIVE", "SUPERSEDED"), ("EVALUATING", "SUPERSEDED")} | {(state, "BLOCKED") for state in ["CREATED", "TRIAGED", "PLANNED", "ACTIVE", "EVALUATING"]}
    return {"AUDIT_FINDING": finding, "REMEDIATION": remediation, "REMEDIATION_PROGRAM": program}


def project(events: list[dict[str, Any]], object_type: str, object_id: str) -> tuple[str, dict[str, Any] | None]:
    legal = legal_maps(); ordered = sorted(events, key=lambda item: item.get("sequence", -1)); state = None; previous = None; previous_time = None; return_state = None
    if not ordered or [item.get("sequence") for item in ordered] != list(range(1, len(ordered) + 1)): return "HISTORY_INVALID", None
    for index, event in enumerate(ordered):
        if event.get("object_type") != object_type or event.get("object_id") != object_id: return "HISTORY_INVALID", None
        if event.get("previous_transition") != previous or event.get("from_state") != state: return "HISTORY_INVALID", None
        if not valid_time(event.get("occurred_at")): return "HISTORY_INVALID", None
        event_time = datetime.fromisoformat(event["occurred_at"].replace("Z", "+00:00"))
        if previous_time and event_time < previous_time: return "HISTORY_INVALID", None
        if not event.get("evidence_refs"): return "HISTORY_INVALID", None
        payload = dict(event); supplied = payload.pop("event_hash", None)
        if supplied != digest(payload): return "HISTORY_INVALID", None
        baseline = index == 0 and state is None and event.get("reason", "").startswith("BASELINE_IMPORT:")
        blocked_return = state == "BLOCKED" and event.get("to_state") == return_state and "BLOCK_REMOVED" in event.get("reason", "")
        if not baseline and not blocked_return and (state, event.get("to_state")) not in legal.get(object_type, set()): return "HISTORY_INVALID", None
        if state == "COMPLETED": return "HISTORY_INVALID", None
        if event.get("to_state") == "BLOCKED": return_state = state
        elif state == "BLOCKED": return_state = None
        state = event["to_state"]; previous = event["transition_id"]; previous_time = event_time
    current = {"current_state_id": "CURRENT-" + object_id, "object_type": object_type, "object_id": object_id, "state": state, "state_as_of": ordered[-1]["occurred_at"], "last_transition_id": ordered[-1]["transition_id"], "transition_sequence": ordered[-1]["sequence"]}
    current["projection_hash"] = digest(current)
    return "VALID", current


def project_decisions(records: list[dict[str, Any]]) -> tuple[str, dict[str, Any] | None]:
    if not records: return "NO_DECISION", None
    ordered = sorted(records, key=lambda item: item.get("decided_at", "")); previous = None
    for item in ordered:
        payload = dict(item); supplied = payload.pop("decision_hash", None)
        if supplied != digest(payload) or not valid_time(item.get("decided_at")): return "DECISION_HISTORY_INVALID", None
        if item.get("audit_id") != "TEST-AUDIT" or item.get("requirement_id") != "TEST-REQ" or item.get("implementation_snapshot") != "1" * 64 or item.get("specification_snapshot") != "2" * 64: return "DECISION_HISTORY_INVALID", None
        if item.get("supersedes") != previous: return "DECISION_HISTORY_INVALID", None
        previous = item["decision_id"]
    latest = ordered[-1]
    current = {"current_decision_id": "CURRENT-" + latest["decision_id"], "audit_id": "TEST-AUDIT", "requirement_id": "TEST-REQ", "decision_id": latest["decision_id"], "decision": latest["decision"], "as_of": latest["decided_at"], "implementation_snapshot": "1" * 64, "specification_snapshot": "2" * 64, "decision_history_valid": True}
    current["projection_hash"] = digest(current)
    return "VALID", current


def aggregate(requirements: list[dict[str, Any]], blockers: list[str]) -> tuple[str, dict[str, dict[str, int]]]:
    categories = ["proven_failure", "waived_failure", "blocked", "unresolved", "pass", "excluded"]; counts = {kind: {category: 0 for category in categories} for kind in ["mandatory", "optional"]}; mandatory = []
    for item in requirements:
        kind = "mandatory" if item["mandatory"] else "optional"; decision = item["decision"]
        if not item.get("applicable", True) or decision == "NOT_APPLICABLE": category = "excluded"
        elif decision == "NON_CONFORMANT": category = "waived_failure" if item.get("waiver_effective", False) else "proven_failure"
        elif decision == "BLOCKED" or decision in {"UNASSESSED", "MAPPED", "VERIFIED"}: category = "blocked"
        elif decision in {"PARTIALLY_CONFORMANT", "UNVERIFIED", "UNKNOWN"}: category = "unresolved"
        elif decision == "CONFORMANT": category = "pass"
        else: raise ValueError(decision)
        counts[kind][category] += 1
        if kind == "mandatory" and category != "excluded": mandatory.append(category)
    if "proven_failure" in mandatory: return "NON_COMPLIANT", counts
    if blockers or "blocked" in mandatory: return "BLOCKED", counts
    if "unresolved" in mandatory: return "UNVERIFIED", counts
    if "waived_failure" in mandatory: return "CONDITIONALLY_COMPLIANT", counts
    if not mandatory: return "NO_MANDATORY_REQUIREMENTS", counts
    return "COMPLIANT", counts


def derive_program(states: list[str], values: dict[str, bool]) -> str:
    if values.get("superseded"): return "SUPERSEDED"
    if values.get("cancelled"): return "CANCELLED"
    if states and all(state == "REJECTED" for state in states): return "FAILED"
    if values.get("blocking"): return "BLOCKED"
    if states and all(state == "COMPLETE" for state in states) and values.get("evaluation_complete"): return "COMPLETED"
    if any(state in {"REVERIFICATION", "REGRESSION"} for state in states) or values.get("evaluation_pending") or (states and all(state == "COMPLETE" for state in states)): return "EVALUATING"
    if any(state in {"IN_PROGRESS", "READY_FOR_VERIFICATION"} for state in states): return "ACTIVE"
    if any(state in {"PROPOSED", "ASSESSED", "APPROVED"} for state in states): return "PLANNED"
    if states: return "TRIAGED"
    return "CREATED"


def parseable(path: Path) -> bool:
    try: load(path); return True
    except Exception: return False


def main() -> int:
    checks: list[dict[str, str]] = []
    def check(cid: str, category: str, description: str, ok: bool, detail: str = "") -> None: checks.append({"check_id": cid, "category": category, "description": description, "result": "PASS" if ok else "FAIL", "detail": detail})
    def blocked(cid: str, category: str, description: str, detail: str) -> None: checks.append({"check_id": cid, "category": category, "description": description, "result": "BLOCKED", "detail": detail})

    for index, name in enumerate(DELIVERABLES, 1): check(f"F{index:02d}", "artifacts", f"v13.2 artifact exists: {name}", (DEST / name).is_file())
    if any(item["result"] == "FAIL" for item in checks): return finish(checks, {})
    check("F45", "artifacts", "generator owns exactly 44 unique v13.2 deliverables", len(DELIVERABLES) == len(set(DELIVERABLES)) == 44)
    check("F46", "artifacts", "all generated YAML is JSON-compatible", all(parseable(DEST / name) for name in DELIVERABLES))

    schemas = {name: load(SCHEMA / f"{name}.schema.yaml") for name in SCHEMA_NAMES}
    check("S01", "schemas", "nine dedicated v13.2 schemas are complete", set(schemas) == set(SCHEMA_NAMES))
    unresolved = []
    for name, schema in schemas.items():
        def scan(value: Any) -> None:
            if isinstance(value, dict):
                if "$ref" in value and Path(value["$ref"]).name.replace(".schema.yaml", "") not in schemas: unresolved.append((name, value["$ref"]))
                for child in value.values(): scan(child)
            elif isinstance(value, list):
                for child in value: scan(child)
        scan(schema)
    check("S02", "schemas", "all schema references resolve", not unresolved, str(unresolved))
    check("S03", "schemas", "transition schema requires immutable identity, sequence, evidence, and hash", set(schemas["state-transition"]["required"]) == {"transition_id", "object_type", "object_id", "from_state", "to_state", "reason", "evidence_refs", "actor", "occurred_at", "sequence", "previous_transition", "event_hash"} and schemas["state-transition"]["properties"]["evidence_refs"]["minItems"] == 1)
    check("S04", "schemas", "current state schema is projection-specific", set(schemas["current-state"]["required"]) == {"current_state_id", "object_type", "object_id", "state", "state_as_of", "last_transition_id", "transition_sequence", "projection_hash"})
    check("S05", "schemas", "invalid history can carry null current projection", any(candidate.get("type") == "null" for candidate in schemas["state-history"]["properties"]["current_state"]["oneOf"]))
    check("S06", "schemas", "decision history schema preserves snapshots and supersession", {"implementation_snapshot", "specification_snapshot", "supersedes", "decision_hash"} <= set(schemas["compliance-decision-record"]["required"]) and set(schemas["compliance-decision-record"]["properties"]["decision"]["enum"]) == DECISION_STATES)
    check("S07", "schemas", "aggregate schema includes explicit empty-mandatory result", set(schemas["audit-aggregate"]["properties"]["aggregate_status"]["enum"]) == AGGREGATE_STATES)
    schema_registry = load(DEST / "SCHEMA-REGISTRY.yaml")
    check("S08", "schemas", "schema registry hashes all nine schemas", len(schema_registry["schemas"]) == 9 and all(sha_file(DEST / item["path"]) == item["sha256"] for item in schema_registry["schemas"]))

    histories = load(DEST / "STATE-HISTORIES.yaml")["histories"]; state_schema_errors = {}
    for history in histories:
        errors = schema_errors(history, schemas["state-history"], schemas, "state-history")
        if errors: state_schema_errors[history["history_id"]] = errors
    check("H01", "history", "all six state histories validate against dedicated schemas", len(histories) == 6 and not state_schema_errors, str(state_schema_errors))
    reproject_errors = []
    for history in histories:
        status, current = project(history["transitions"], history["object_type"], history["object_id"])
        if status != "VALID" or current != history["current_state"]: reproject_errors.append(history["history_id"])
    check("H02", "projection", "all six current states independently reproject exactly", not reproject_errors, str(reproject_errors))
    check("H03", "history", "history integrity and hashes validate", all(history["history_integrity"] == {"valid": True, "checked_at": "2026-09-12T17:20:43Z", "error_codes": []} and history["history_hash"] == digest({key: value for key, value in history.items() if key != "history_hash"}) for history in histories))
    events = [event for history in histories for event in history["transitions"]]; currents = [history["current_state"] for history in histories]
    check("H04", "events", "all six baseline events have immutable hashes and contiguous genesis sequence", len(events) == 6 and all(event["sequence"] == 1 and event["from_state"] is None and event["previous_transition"] is None and event["reason"].startswith("BASELINE_IMPORT:") and event["event_hash"] == digest({key: value for key, value in event.items() if key != "event_hash"}) for event in events))
    policy = load(DEST / "BASELINE-IMPORT-POLICY.yaml")
    check("H05", "non-invention", "baseline imports explicitly avoid reconstructing unavailable history", policy["historical_claim"] == "NO_PRE_V13.2_TRANSITION_TIME_OR_SEQUENCE_IS_ASSERTED" and policy["evidence_required"] is True)
    check("H06", "derived-views", "event registry is an exact reproducible history view", load(DEST / "STATE-TRANSITION-REGISTRY.yaml")["events"] == events and load(DEST / "STATE-TRANSITION-REGISTRY.yaml")["reproducible_view"] is True)
    check("H07", "derived-views", "current-state registry is an exact reproducible projection", load(DEST / "CURRENT-STATES.yaml")["objects"] == currents and load(DEST / "CURRENT-STATES.yaml")["reproducible_projection"] is True)
    check("H08", "projection", "finding and program current states remain separately OPEN and CREATED", [item["state"] for item in currents if item["object_type"] == "AUDIT_FINDING"] == ["OPEN"] * 3 and [item["state"] for item in currents if item["object_type"] == "REMEDIATION_PROGRAM"] == ["CREATED"] * 3)
    source_entries = load(OUT / "OBJECT-REGISTRY.yaml")["objects"] + load(V131 / "OBJECT-REGISTRY.yaml")["objects"]
    source_by_id = {identifier: [item for item in source_entries if item["object_id"] == identifier] for identifier in {item["object_id"] for item in source_entries}}
    check("H09", "references", "all baseline evidence references resolve exactly once with matching subject type", all(len(source_by_id.get(reference, [])) == 1 and source_by_id[reference][0]["object_type"] == event["object_type"] and reference == event["object_id"] for event in events for reference in event["evidence_refs"]))
    transition_model = load(DEST / "STATE-TRANSITION-MODEL.yaml")
    check("H10", "validation-order", "all twelve projection validation stages and no-skip failure behavior are explicit", len(transition_model["validation_order"]) == 12 and transition_model["failure_behavior"] == "HISTORY_INVALID_NO_PROJECTION" and transition_model["skip_invalid_transition"] is False)
    vectors = load(DEST / "STATE-PROJECTION-TEST-VECTORS.yaml"); bad_vectors = []
    for item in vectors["vectors"]:
        first = item["events"][0]; status, current = project(item["events"], first["object_type"], first["object_id"])
        if status != item["expected"] or status != item["actual"] or (current["state"] if current else None) != item["projected_state"] or not item["pass"]: bad_vectors.append(item["vector_id"])
    check("H11", "test-vectors", "all twelve history projection vectors reproduce independently", vectors["summary"] == {"total": 12, "passed": 12, "failed": 0} and not bad_vectors, str(bad_vectors))
    check("H12", "terminal", "completed-to-active history is rejected", next(item for item in vectors["vectors"] if item["vector_id"] == "COMPLETED_PROGRAM_TERMINAL")["actual"] == "HISTORY_INVALID")
    check("H13", "block-return", "block return accepts only the previous operational state", next(item for item in vectors["vectors"] if item["vector_id"] == "BLOCK_RETURN_PREVIOUS")["actual"] == "VALID" and next(item for item in vectors["vectors"] if item["vector_id"] == "BLOCK_RETURN_WRONG_STATE")["actual"] == "HISTORY_INVALID")

    decision_model = load(DEST / "DECISION-HISTORY-MODEL.yaml")
    check("D01", "decision-history", "new decision triggers and immutable supersession semantics are exact", set(decision_model["new_decision_triggers"]) == {"NEW_IMPLEMENTATION_STATE", "NEW_EVIDENCE", "CHANGED_REQUIREMENT", "CHANGED_ORACLE"} and decision_model["supersession_deletes_predecessor"] is False)
    check("D02", "decision-projection", "projection key includes audit, requirement, specification, and implementation", decision_model["projection_key"] == ["audit_id", "requirement_id", "specification_snapshot", "implementation_snapshot"])
    check("D03", "decision-projection", "invalid latest decision cannot silently fall back", decision_model["latest_invalid_behavior"] == "DECISION_HISTORY_INVALID_NO_FALLBACK")
    decision_vectors = load(DEST / "DECISION-PROJECTION-TEST-VECTORS.yaml"); decision_errors = []
    decision_schema_errors = []
    for item in decision_vectors["vectors"]:
        status, selected = project_decisions(item["records"]); selected_id = selected["decision_id"] if selected else None
        if status != item["expected"] or status != item["actual"] or selected_id != item["expected_decision_id"] or selected_id != item["actual_decision_id"] or selected != item["current_projection"] or not item["pass"]: decision_errors.append(item["vector_id"])
        for record in item["records"]:
            if schema_errors(record, schemas["compliance-decision-record"], schemas, "compliance-decision-record"): decision_schema_errors.append(item["vector_id"])
        if selected and schema_errors(selected, schemas["current-requirement-decision"], schemas, "current-requirement-decision"): decision_schema_errors.append(item["vector_id"])
    check("D04", "test-vectors", "all six decision projection vectors reproduce independently", decision_vectors["summary"] == {"total": 6, "passed": 6, "failed": 0} and not decision_errors, str(decision_errors))
    check("D05", "schemas", "synthetic decision records and valid current projections exercise both schemas", not decision_schema_errors and sum(item["current_projection"] is not None for item in decision_vectors["vectors"]) == 2, str(decision_schema_errors))
    check("D06", "decision-history", "current package invents no requirement decisions", load(DEST / "COMPLIANCE-DECISION-HISTORIES.yaml")["records"] == [] and load(DEST / "CURRENT-REQUIREMENT-DECISIONS.yaml")["objects"] == [])

    aggregate_function = load(DEST / "AGGREGATE-FUNCTION.yaml")
    check("A01", "aggregate", "canonical precedence is failure, blocked, unresolved, waiver, pass, empty", aggregate_function["precedence"] == ["PROVEN_FAILURE", "BLOCKED", "UNRESOLVED", "WAIVED_FAILURE", "PASS", "NO_MANDATORY_REQUIREMENTS"])
    check("A02", "aggregate", "aggregate excludes lifecycle process states", aggregate_function["process_states_are_inputs"] is False and aggregate_function["deterministic"] is True)
    check("A03", "optional", "optional results are separately reported and cannot alter mandatory aggregate", aggregate_function["optional_reporting"] == {"proven_failure": "OPTIONAL_FAILURE", "unresolved": "OPTIONAL_UNVERIFIED", "blocked": "OPTIONAL_BLOCKED"} and aggregate_function["optional_requirements_change_mandatory_aggregate"] is False)
    aggregate_vectors = load(DEST / "AGGREGATE-TEST-VECTORS.yaml"); aggregate_errors = []
    for item in aggregate_vectors["vectors"]:
        status, counts = aggregate(item["requirements"], item["integrity_blockers"])
        if status != item["expected"] or status != item["actual"] or counts != item["counts"] or not item["pass"]: aggregate_errors.append(item["vector_id"])
    check("A04", "test-vectors", "all twelve aggregate vectors reproduce independently", aggregate_vectors["summary"] == {"total": 12, "passed": 12, "failed": 0} and not aggregate_errors, str(aggregate_errors))
    by_vector = {item["vector_id"]: item["actual"] for item in aggregate_vectors["vectors"]}
    check("A05", "precedence", "proven failure dominates blockers", by_vector["PROVEN_FAILURE_DOMINATES_BLOCKER"] == "NON_COMPLIANT")
    check("A06", "precedence", "blocked dominates unresolved", by_vector["BLOCKED_DOMINATES_UNRESOLVED"] == "BLOCKED")
    check("A07", "precedence", "unresolved dominates waived failure", by_vector["UNRESOLVED_DOMINATES_WAIVER"] == "UNVERIFIED")
    check("A08", "waiver", "waived-only mandatory violation is conditional", by_vector["WAIVED_FAILURE_ONLY"] == "CONDITIONALLY_COMPLIANT")
    check("A09", "empty-set", "valid empty/all-excluded/optional-only mandatory sets are not compliant", {by_vector[key] for key in ["VALID_EMPTY_MANDATORY", "ALL_NOT_APPLICABLE", "OPTIONAL_FAILURE_WITH_NO_MANDATORY"]} == {"NO_MANDATORY_REQUIREMENTS"})
    check("A10", "integrity", "integrity failure blocks empty-set evaluation", by_vector["INTEGRITY_BLOCKS_EMPTY_EVALUATION"] == "BLOCKED")
    check("A11", "optional", "optional failure with mandatory pass remains compliant", by_vector["OPTIONAL_FAILURE_WITH_MANDATORY_PASS"] == "COMPLIANT")

    snapshot = load(DEST / "AUDIT-SNAPSHOT.yaml")["objects"][0]
    check("N01", "snapshot", "audit snapshot validates and hash matches", not schema_errors(snapshot, schemas["audit-snapshot"], schemas, "audit-snapshot") and snapshot["snapshot_hash"] == digest({key: value for key, value in snapshot.items() if key != "snapshot_hash"}))
    check("N02", "snapshot", "snapshot components and typed audit reference match exact immutable inputs", len(source_by_id.get(snapshot["audit_id"], [])) == 1 and source_by_id[snapshot["audit_id"]][0]["object_type"] == "AUDIT" and snapshot["specification_snapshot"] == sha_file(HS / "specification" / "SPECIFICATION-MANIFEST.yaml") and snapshot["implementation_snapshot"] == sha_file(OUT / "IMPLEMENTATION-ARTIFACTS.yaml") and snapshot["waiver_snapshot"] == sha_file(OUT / "WAIVERS.yaml") and snapshot["state_history_snapshot"] == digest(histories))
    current_aggregate = load(DEST / "CURRENT-AGGREGATE.yaml"); aggregate_object = current_aggregate["objects"][0]
    actual_status, actual_counts = aggregate([], aggregate_object["integrity_blockers"])
    check("N03", "current-aggregate", "current aggregate independently recomputes BLOCKED", actual_status == aggregate_object["aggregate_status"] == current_aggregate["aggregate_status_after_integrity"] == "BLOCKED" and actual_counts["mandatory"] == aggregate_object["mandatory_counts"] and actual_counts["optional"] == aggregate_object["optional_counts"])
    check("N04", "current-aggregate", "empty mandatory state is explicit without manufacturing compliance", current_aggregate["mandatory_set_status"] == "NO_MANDATORY_REQUIREMENTS" and aggregate_object["aggregate_status"] != "COMPLIANT")
    check("N05", "current-aggregate", "aggregate validates, identifies snapshot, and has canonical hash", not schema_errors(aggregate_object, schemas["audit-aggregate"], schemas, "audit-aggregate") and aggregate_object["audit_snapshot_id"] == snapshot["snapshot_id"] and aggregate_object["aggregate_hash"] == digest({key: value for key, value in aggregate_object.items() if key != "aggregate_hash"}))
    integrity = load(DEST / "AUDIT-INTEGRITY.yaml")
    check("N06", "integrity", "H/D/R/T/S/E predicates block at invalid specification prerequisite", set(integrity["predicates"]) == {"H_state_history_valid", "D_current_decisions_valid", "R_references_resolve", "T_temporal_integrity", "S_specification_snapshot_valid", "E_required_evidence_integrity", "result"} and integrity["earliest_invalid_prerequisite"] == "SPECIFICATION_SNAPSHOT" and integrity["predicates"]["result"] == "BLOCKED" and integrity["silent_fallback"] is False)
    audit_status = load(DEST / "AUDIT-STATUS.yaml")["objects"][0]
    check("N07", "audit-status", "audit status derives from snapshot aggregate and remains uncertifiable", not schema_errors(audit_status, schemas["audit-status"], schemas, "audit-status") and audit_status["audit_snapshot_id"] == snapshot["snapshot_id"] and audit_status["aggregate_id"] == aggregate_object["aggregate_id"] and audit_status["status"] == "BLOCKED" and audit_status["certification_eligible"] is False and audit_status["status_hash"] == digest({key: value for key, value in audit_status.items() if key != "status_hash"}))

    program_machine = load(DEST / "PROGRAM-STATE-MACHINE.yaml"); transitions = {(item["from"], item["to"]): item["guard"] for item in program_machine["legal_transitions"]}
    check("P01", "program-state", "all ten program states have exact definitions", set(program_machine["states"]) == PROGRAM_STATES and set(program_machine["definitions"]) == PROGRAM_STATES and all(program_machine["definitions"].values()))
    check("P02", "program-state", "canonical operational chain is guarded", all(pair in transitions and transitions[pair] for pair in [("CREATED", "TRIAGED"), ("TRIAGED", "PLANNED"), ("PLANNED", "ACTIVE"), ("ACTIVE", "EVALUATING"), ("EVALUATING", "COMPLETED")]))
    check("P03", "program-state", "block and return rules cover every operational state", all((state, "BLOCKED") in transitions and ("BLOCKED", state) in transitions for state in ["CREATED", "TRIAGED", "PLANNED", "ACTIVE", "EVALUATING"]))
    check("P04", "program-state", "completed is terminal and cannot return active", set(program_machine["terminal_states"]) == {"COMPLETED", "FAILED", "CANCELLED", "SUPERSEDED"} and ("COMPLETED", "ACTIVE") not in transitions and program_machine["completed_to_active"] == "FORBIDDEN")
    check("P05", "separation", "program machine has no conformance effect", program_machine["conformance_effect"] == "NONE")
    derivation_function = load(DEST / "PROGRAM-DERIVATION-FUNCTION.yaml")
    expected_precedence = ["SUPERSEDED", "CANCELLED", "FAILED", "BLOCKED", "COMPLETED", "EVALUATING", "ACTIVE", "PLANNED", "TRIAGED", "CREATED"]
    check("P06", "program-derivation", "program predicate precedence is exact and resolves EVALUATING before ACTIVE", derivation_function["precedence"] == expected_precedence and derivation_function["independent_assertion"] == "FORBIDDEN")
    derivations = load(DEST / "PROGRAM-DERIVATIONS.yaml")["objects"]; derivation_errors = []
    for item in derivations:
        if schema_errors(item, schemas["program-state-derivation"], schemas, "program-state-derivation") or item["derived_state"] != derive_program(item["remediation_states"], {}) or item["derivation_hash"] != digest({key: value for key, value in item.items() if key != "derivation_hash"}): derivation_errors.append(item["derivation_id"])
    check("P07", "program-derivation", "three referenced zero-member programs independently derive CREATED", len(derivations) == 3 and not derivation_errors and all(item["derived_state"] == "CREATED" and item["remediation_ids"] == [] and item["evidence_refs"] == [item["program_id"]] and len(source_by_id.get(item["program_id"], [])) == 1 and source_by_id[item["program_id"]][0]["object_type"] == "REMEDIATION_PROGRAM" for item in derivations), str(derivation_errors))
    program_vectors = load(DEST / "PROGRAM-TEST-VECTORS.yaml"); program_errors = [item["vector_id"] for item in program_vectors["vectors"] if derive_program(item["remediation_states"], item["predicates"]) != item["actual"] or item["actual"] != item["expected"] or not item["pass"]]
    check("P08", "test-vectors", "all ten program derivation vectors reproduce independently", program_vectors["summary"] == {"total": 10, "passed": 10, "failed": 0} and not program_errors, str(program_errors))

    temporal = load(DEST / "TEMPORAL-QUERY-RULES.yaml")
    check("T01", "temporal", "five temporal query classes are supported without wall-clock dependence", set(temporal["supported_queries"]) == {"decision_at(t)", "finding_state_at(t)", "remediation_state_at(t)", "program_state_at(t)", "aggregate_at(t)"} and temporal["wall_clock_dependency"] is False)
    check("T02", "temporal", "baseline temporal queries distinguish before-lineage from current state", len(temporal["queries"]) == 12 and sum(item["result"] == "NO_ACCEPTED_V13.2_STATE" for item in temporal["queries"]) == 6)
    canonical_model = load(DEST / "CANONICAL-MODEL.yaml")
    check("T03", "separation", "canonical flow is forward-only through certificate", canonical_model["forward_flow"] == ["IMMUTABLE_HISTORY", "CURRENT_STATE", "IMPLEMENTATION_CHANGE", "VERIFICATION", "COMPLIANCE_DECISION_HISTORY", "CURRENT_DECISION", "AGGREGATE", "AUDIT_STATUS", "CERTIFICATE"] and canonical_model["reverse_mutation"] is False)
    certificate_policy = load(DEST / "CERTIFICATE-POLICY.yaml"); certificate_status = load(DEST / "CERTIFICATE-REVISION-STATUS.yaml"); prior_certificate = load(OUT / "AUDIT-CERTIFICATE.yaml")["objects"][0]
    check("C01", "certificate", "certificate policy requires snapshot scope and immutable lineage", certificate_policy["certificate_requires_snapshot"] is True and certificate_policy["lineage_immutable"] is True and certificate_policy["universal_truth_claim_forbidden"] is True)
    check("C02", "certificate", "no certificate revision is authorized", certificate_status["status"] == "NOT_AUTHORIZED" and certificate_status["lineage_modified"] is False and certificate_status["prior_certificate_id"] == prior_certificate["object_id"] and certificate_status["prior_certificate_hash"] == prior_certificate["certificate_hash"])

    invariants = load(DEST / "INVARIANTS.yaml")["invariants"]
    check("I01", "invariants", "all twenty canonical v13.2 invariants are mechanically enumerated", len(invariants) == 20 and [item["invariant_id"] for item in invariants] == [f"V132-I{index:02d}" for index in range(1, 21)] and all(item["enforcement"] == "MECHANICAL" for item in invariants))
    registry = load(DEST / "OBJECT-REGISTRY.yaml"); registered_ids = [item["object_id"] for item in registry["objects"]]
    check("I02", "identities", "all twenty-four v13.2 normative IDs are unique and valid", len(registered_ids) == len(set(registered_ids)) == 24 and all(ID_RE.fullmatch(identifier) for identifier in registered_ids))
    expected_registry = {(history["history_id"], "STATE_HISTORY") for history in histories} | {(event["transition_id"], "STATE_TRANSITION") for event in events} | {(current["current_state_id"], "CURRENT_STATE") for current in currents} | {(item["derivation_id"], "PROGRAM_STATE_DERIVATION") for item in derivations} | {(snapshot["snapshot_id"], "AUDIT_SNAPSHOT"), (aggregate_object["aggregate_id"], "AUDIT_AGGREGATE"), (audit_status["audit_status_id"], "AUDIT_STATUS")}
    check("I03", "registry", "object registry contains all and only canonical v13.2 objects", {(item["object_id"], item["object_type"]) for item in registry["objects"]} == expected_registry)
    external_ids = {item["object_id"] for item in load(OUT / "OBJECT-REGISTRY.yaml")["objects"]} | {item["object_id"] for item in load(REM / "OBJECT-REGISTRY.yaml")["objects"]} | {item["object_id"] for item in load(V131 / "OBJECT-REGISTRY.yaml")["objects"]}
    check("I04", "identities", "v13.2 normative IDs are globally unique against predecessor registries", not (set(registered_ids) & external_ids))
    check("I05", "references", "all three predecessor registry hashes resolve exactly", len(registry["external_registries"]) == 3 and all((DEST / item["path"]).is_file() and sha_file(DEST / item["path"]) == item["sha256"] for item in registry["external_registries"]))
    validation_report = load(DEST / "VALIDATION-REPORT.yaml")
    check("I06", "validation", "generated report preserves structural pass and blocked audit", validation_report["overall_status"] == "STRUCTURAL_PASS_AUDIT_BLOCKED" and validation_report["state_histories"] == {"total": 6, "valid": 6, "invalid": 0} and validation_report["current_aggregate"] == validation_report["audit_status"] == "BLOCKED")

    prior = load(DEST / "PRIOR-INTEGRITY.yaml"); prior_errors = [item["path"] for item in prior["artifacts"] if not (OUT / item["path"]).is_file() or sha_file(OUT / item["path"]) != item["sha256"] or (OUT / item["path"]).stat().st_size != item["bytes"]]
    check("R01", "append-only", "all 169 predecessor compliance artifacts remain byte-identical", prior["status"] == "PRESERVED" and prior["protected_artifact_count"] == len(prior["artifacts"]) == 169 and not prior_errors, str(prior_errors))
    check("R02", "append-only", "v13.1 builder contains future-extension refusal", "refusing to erase predecessor artifacts after append-only v13.2 extension" in (HS / "tools/build_state_separation_aggregate_v131.py").read_text())
    reports = [load(DEST / f"reports/{name}") for name in REPORT_FILES]
    check("R03", "reports", "four reports preserve current states, temporal integrity, aggregate, and certification separation", reports[0]["history_invalid"] == 0 and reports[1]["aggregate_status"] == "BLOCKED" and reports[1]["process_states_consumed"] is False and reports[2]["reproducible"] is True and reports[3]["certificate_revision"] is False)

    determinism = load(DEST / "DETERMINISM-VALIDATION.yaml") if (DEST / "DETERMINISM-VALIDATION.yaml").is_file() else {}
    check("Q01", "determinism", "all 44 generator-owned outputs reproduce byte-for-byte", determinism.get("status") == "PASS" and determinism.get("summary") == {"total": 44, "identical": 44, "different": 0} and {item["path"] for item in determinism.get("files", [])} == set(DELIVERABLES) and all(item["byte_identical"] for item in determinism.get("files", [])))
    regression = load(DEST / "REGRESSION-VALIDATION.yaml") if (DEST / "REGRESSION-VALIDATION.yaml").is_file() else {}
    expected_regression = {"13.1": (110, 0, 1), "13.0": (115, 0, 1), "12.1": (194, 0, 1), "12.0": (148, 0, 1), "11.1": (177, 0, 1), "10.1": (143, 0, 1)}
    actual_regression = {item["protocol"]: (item["passed"], item["failed"], item["blocked"]) for item in regression.get("regressions", [])}
    check("Q02", "regression", "v10.1 through v13.1 regressions and append-only guards pass", regression.get("status") == "PASS" and actual_regression == expected_regression and regression.get("append_only_guards") == {"v13": "PASS_REFUSED", "v13.1": "PASS_REFUSED", "v13.2": "PASS_REFUSED"})
    check("Q03", "hygiene", "no Python cache artifacts exist", not any(HS.rglob("__pycache__")) and not any(HS.rglob("*.pyc")))
    check("Q04", "tools", "generic and pinned v13.2 tools exist", all((HS / "tools" / name).is_file() for name in ["build_current_state_projection.py", "build_current_state_projection_v132.py", "validate_current_state_projection.py", "validate_current_state_projection_v132.py"]))
    blocked("GATE-V132", "acceptance", "current audit/certification decision", "History and projection structures validate, but invalid normative scope and missing implementation/evidence prerequisites keep the current audit BLOCKED and prohibit certificate revision.")
    return finish(checks, {"schemas": 9, "state_histories": 6, "state_transitions": 6, "current_states": 6, "decision_records": 0, "current_decisions": 0, "program_derivations": 3, "audit_snapshots": 1, "aggregates": 1, "audit_statuses": 1})


def finish(checks: list[dict[str, str]], counts: dict[str, Any]) -> int:
    passed = sum(item["result"] == "PASS" for item in checks); failed = sum(item["result"] == "FAIL" for item in checks); blocked_count = sum(item["result"] == "BLOCKED" for item in checks)
    report = {"schema_version": VERSION, "validator": "Protocol-v13.2 independent validator", "overall_status": "FAIL" if failed else "STRUCTURAL_PASS_AUDIT_BLOCKED" if blocked_count else "PASS", "acceptance": "VALIDATION_FAILED" if failed else "BLOCKED" if blocked_count else "PASS", "summary": {"total": len(checks), "passed": passed, "failed": failed, "blocked": blocked_count}, "object_counts": counts, "checks": checks}
    (DEST / "VALIDATION.yaml").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    lines = ["# Protocol-v13.2 Independent Validation", "", f"**Overall:** `{report['overall_status']}`", f"**Acceptance:** `{report['acceptance']}`", f"**Checks:** {passed} PASS / {failed} FAIL / {blocked_count} BLOCKED ({len(checks)} total)", "", "Valid history/projection architecture does not alter the blocked requirement and certification truth state.", "", "| ID | Category | Result | Description | Detail |", "|---|---|---|---|---|"]
    for item in checks: lines.append("| %s | %s | %s | %s | %s |" % (item["check_id"], item["category"], item["result"], item["description"].replace("|", "\\|"), item["detail"].replace("|", "\\|")))
    (DEST / "VALIDATION.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{passed} PASS / {failed} FAIL / {blocked_count} BLOCKED ({len(checks)} checks); {report['overall_status']}")
    return 1 if failed else 0


if __name__ == "__main__": sys.exit(main())
