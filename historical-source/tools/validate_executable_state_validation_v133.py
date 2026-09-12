#!/usr/bin/env python3
"""Independent validator for Protocol-v13.3 executable state conformance."""
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
V132 = REM / "v13.2"
DEST = REM / "v13.3"
SCHEMA = DEST / "schema"
VERSION = "13.3"
FINDING_STATES = {"DETECTED", "VALIDATED", "CLASSIFIED", "OPEN", "UNDER_REMEDIATION", "RESOLVED", "CLOSED", "REJECTED", "WAIVED", "SUPERSEDED", "BLOCKED"}
REMEDIATION_STATES = {"PROPOSED", "ASSESSED", "APPROVED", "IN_PROGRESS", "READY_FOR_VERIFICATION", "REVERIFICATION", "REGRESSION", "COMPLETE", "FAILED", "BLOCKED", "REJECTED", "SUPERSEDED", "CANCELLED"}
PROGRAM_STATES = {"CREATED", "TRIAGED", "PLANNED", "ACTIVE", "EVALUATING", "COMPLETED", "BLOCKED", "FAILED", "CANCELLED", "SUPERSEDED"}
CONFORMANCE_STATES = {"UNASSESSED", "MAPPED", "VERIFIED", "CONFORMANT", "PARTIALLY_CONFORMANT", "NON_CONFORMANT", "UNVERIFIED", "BLOCKED", "UNKNOWN", "NOT_APPLICABLE"}
AGGREGATE_STATES = {"NON_COMPLIANT", "BLOCKED", "UNVERIFIED", "CONDITIONALLY_COMPLIANT", "COMPLIANT", "NO_MANDATORY_REQUIREMENTS"}
FAILURE_CODES = {"SEQUENCE_GAP", "DUPLICATE_SEQUENCE", "PREDECESSOR_MISMATCH", "STATE_MISMATCH", "ILLEGAL_TRANSITION", "MISSING_EVIDENCE", "INVALID_HASH", "TIMESTAMP_VIOLATION", "UNKNOWN"}
PREDICATES = ["object_exists", "object_type_valid", "state_names_valid", "sequence_valid", "predecessor_valid", "from_state_matches", "transition_is_legal", "guard_satisfied", "evidence_valid", "timestamp_valid", "hash_valid"]
SCHEMA_NAMES = ["finding-state", "remediation-state", "program-state", "conformance-state", "state-transition", "transition-guard-context", "transition-validation", "history-integrity-failure", "current-state", "state-history", "compliance-decision-record", "current-decision", "waiver-record", "waiver-resolution", "audit-snapshot", "aggregate-result", "program-derivation", "pipeline-execution", "audit-status"]
MACHINE_FILES = ["NORMATIVE-VOCABULARY.yaml", "STATE-DOMAINS.yaml", "TRANSITION-VALIDATION-PREDICATES.yaml", "FINDING-TRANSITION-TABLE.yaml", "REMEDIATION-TRANSITION-TABLE.yaml", "PROGRAM-TRANSITION-TABLE.yaml", "TRANSITION-GUARDS.yaml", "BASELINE-IMPORT-POLICY.yaml", "STATE-HISTORIES.yaml", "TRANSITION-GUARD-CONTEXTS.yaml", "TRANSITION-VALIDATIONS.yaml", "CURRENT-STATES.yaml", "HISTORY-INTEGRITY-FAILURES.yaml", "HISTORY-VALIDATION-TEST-VECTORS.yaml", "TRANSITION-VALIDATION-TEST-VECTORS.yaml", "DECISION-PROJECTION-RULES.yaml", "COMPLIANCE-DECISION-HISTORIES.yaml", "CURRENT-DECISIONS.yaml", "DECISION-PROJECTION-TEST-VECTORS.yaml", "WAIVER-RESOLUTION-RULES.yaml", "WAIVERS-V133.yaml", "WAIVER-RESOLUTIONS.yaml", "WAIVER-TEST-VECTORS.yaml", "AGGREGATE-FUNCTION.yaml", "AGGREGATE-INVARIANTS.yaml", "AGGREGATE-TEST-VECTORS.yaml", "CONFORMANCE-SEPARATION-TEST-VECTORS.yaml", "DETERMINISM-PURITY-TEST-VECTORS.yaml", "PROGRAM-DERIVATION-FUNCTION.yaml", "PROGRAM-DERIVATIONS.yaml", "PROGRAM-DERIVATION-TEST-VECTORS.yaml", "AUDIT-SNAPSHOT.yaml", "VALIDATION-PIPELINE.yaml", "FAILURE-BOUNDARIES.yaml", "CURRENT-PIPELINE-EXECUTION.yaml", "CURRENT-AGGREGATE.yaml", "CURRENT-AUDIT-STATUS.yaml", "CERTIFICATE-STATUS.yaml", "COMPLETE-TRANSFORMATION.yaml", "AXIS-SEPARATION.yaml", "OBJECT-REGISTRY.yaml", "SCHEMA-REGISTRY.yaml", "PRIOR-INTEGRITY.yaml", "VALIDATION-REPORT.yaml"]
REPORT_FILES = ["EXECUTABLE-STATE-REPORT.yaml", "AGGREGATE-CONFORMANCE-REPORT.yaml", "FAILURE-BOUNDARY-REPORT.yaml", "CERTIFICATION-IMPACT-REPORT.yaml"]
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
        if body.get("format") == "date-time" and not valid_time(value): errors.append(f"{path}: time")
    if isinstance(value, int) and not isinstance(value, bool) and value < body.get("minimum", value): errors.append(f"{path}: minimum")
    if isinstance(value, list):
        if len(value) < body.get("minItems", 0): errors.append(f"{path}: minItems")
        if body.get("uniqueItems") and len({canonical(item) for item in value}) != len(value): errors.append(f"{path}: unique")
        if "items" in body:
            for index, item in enumerate(value): errors.extend(schema_errors(item, body["items"], schemas, f"{path}[{index}]"))
    if isinstance(value, dict):
        props = body.get("properties", {})
        for key in body.get("required", []):
            if key not in value: errors.append(f"{path}: missing {key}")
        if body.get("additionalProperties") is False:
            for key in value:
                if key not in props: errors.append(f"{path}: additional {key}")
        for key, item in value.items():
            if key in props: errors.extend(schema_errors(item, props[key], schemas, f"{path}.{key}"))
    return errors


def matrix(path: str) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for item in load(DEST / path)["transitions"]: result.setdefault(item["from"], []).append(item["to"])
    return result


def validate_history_vector(item: dict[str, Any], tables: dict[str, list[dict[str, str]]], guard_defs: dict[str, list[str]]) -> tuple[str, str | None]:
    events = sorted(item["events"], key=lambda event: event.get("sequence", -1)); contexts = {context["transition_id"]: context for context in item["guard_contexts"]}; sequences = [event.get("sequence") for event in events]
    if len(sequences) != len(set(sequences)): return "HISTORY_INVALID", "DUPLICATE_SEQUENCE"
    if sequences != list(range(len(events))): return "HISTORY_INVALID", "SEQUENCE_GAP"
    state = None; previous = None; previous_time = None; previous_operational = None
    states = {"FINDING": FINDING_STATES, "REMEDIATION": REMEDIATION_STATES, "PROGRAM": PROGRAM_STATES, "COMPLIANCE_DECISION": CONFORMANCE_STATES}
    for index, event in enumerate(events):
        if event.get("object_type") not in states or event.get("object_id") != "TEST-FINDING": return "HISTORY_INVALID", "UNKNOWN"
        if event.get("previous_transition") != previous: return "HISTORY_INVALID", "PREDECESSOR_MISMATCH"
        if event.get("from_state") != state: return "HISTORY_INVALID", "STATE_MISMATCH"
        if event.get("to_state") not in states[event["object_type"]]: return "HISTORY_INVALID", "ILLEGAL_TRANSITION"
        entry = None
        if index == 0 and state is None: entry = {"guard_id": "BASELINE_IMPORT_GUARD"}
        else:
            for candidate in tables[event["object_type"]]:
                if candidate["from"] == state and (candidate["to"] == event["to_state"] or candidate["to"] == "$PREVIOUS_OPERATIONAL_STATE" and event["to_state"] == previous_operational): entry = candidate; break
        if not entry: return "HISTORY_INVALID", "ILLEGAL_TRANSITION"
        context = contexts.get(event["transition_id"], {}); required = guard_defs[entry["guard_id"]]
        if context.get("guard_id") != entry["guard_id"] or not all(context.get("facts", {}).get(name) is True for name in required): return "HISTORY_INVALID", "ILLEGAL_TRANSITION"
        if not event.get("evidence_refs") or any(reference != "TEST-EVIDENCE" for reference in event["evidence_refs"]): return "HISTORY_INVALID", "MISSING_EVIDENCE"
        if not valid_time(event.get("occurred_at")): return "HISTORY_INVALID", "TIMESTAMP_VIOLATION"
        instant = datetime.fromisoformat(event["occurred_at"].replace("Z", "+00:00"))
        if previous_time and instant < previous_time: return "HISTORY_INVALID", "TIMESTAMP_VIOLATION"
        payload = dict(event); supplied = payload.pop("event_hash", None)
        if supplied != digest(payload): return "HISTORY_INVALID", "INVALID_HASH"
        if event["to_state"] == "BLOCKED": previous_operational = state
        elif state == "BLOCKED": previous_operational = None
        state = event["to_state"]; previous = event["transition_id"]; previous_time = instant
    return "VALID", None


def project_decision(records: list[dict[str, Any]], arguments: dict[str, Any]) -> tuple[str, dict[str, Any] | None]:
    implementation = arguments.get("implementation", "1" * 64); specification = arguments.get("specification", "2" * 64); scope = set(arguments.get("scope", ["TEST-REQ"]))
    if "TEST-REQ" not in scope: return "DECISION_SNAPSHOT_MISMATCH", None
    if not records: return "NO_DECISION", None
    ordered = sorted(records, key=lambda record: record.get("decided_at", "")); previous = None
    for record in ordered:
        payload = dict(record); supplied = payload.pop("decision_hash", None)
        if supplied != digest(payload) or not valid_time(record.get("decided_at")) or record.get("supersedes") != previous: return "DECISION_HISTORY_INVALID", None
        if record.get("audit_id") != "TEST-AUDIT" or record.get("requirement_id") != "TEST-REQ" or record.get("implementation_snapshot") != implementation or record.get("specification_snapshot") != specification: return "DECISION_SNAPSHOT_MISMATCH", None
        previous = record["decision_id"]
    latest = ordered[-1]; current = {"current_decision_id": "CURRENT-" + latest["decision_id"], "audit_id": "TEST-AUDIT", "requirement_id": "TEST-REQ", "decision_id": latest["decision_id"], "decision": latest["decision"], "as_of": latest["decided_at"], "implementation_snapshot": implementation, "specification_snapshot": specification, "decision_history_valid": True, "schema_version": VERSION}; current["projection_hash"] = digest(current); return "VALID", current


def waiver(record: dict[str, Any]) -> tuple[str, bool]:
    payload = dict(record); supplied = payload.pop("waiver_hash", None)
    if supplied != digest(payload): return "WAIVER_INVALID", False
    if record.get("audit_id") != "TEST-AUDIT" or record.get("requirement_id") != "TEST-REQ" or "TEST-REQ" not in record.get("scope", []) or record.get("implementation_snapshot") != "1" * 64 or record.get("specification_snapshot") != "2" * 64: return "WAIVER_SCOPE_MISMATCH", False
    if record.get("status") != "EFFECTIVE": return "WAIVER_NOT_EFFECTIVE", False
    if not record.get("effective_from") <= "2026-09-12T18:11:09Z" <= record.get("effective_until"): return "WAIVER_OUTSIDE_EFFECTIVE_PERIOD", False
    return "EFFECTIVE", True


def aggregate(requirements: list[dict[str, Any]]) -> dict[str, Any]:
    classes = ["pass", "proven_failure", "blocked", "unresolved", "waived_failure", "excluded"]; counts = {kind: {key: 0 for key in classes} for kind in ["mandatory", "optional"]}; mandatory = []
    for item in requirements:
        kind = "mandatory" if item["mandatory"] else "optional"; decision = item["decision"]
        if not item.get("applicable", True) or decision == "NOT_APPLICABLE": contribution = "excluded"
        elif decision == "CONFORMANT": contribution = "pass"
        elif decision == "NON_CONFORMANT": contribution = "waived_failure" if item.get("waiver_effective") else "proven_failure"
        elif decision == "BLOCKED" or decision in {"UNASSESSED", "MAPPED", "VERIFIED"}: contribution = "blocked"
        elif decision in {"PARTIALLY_CONFORMANT", "UNVERIFIED", "UNKNOWN"}: contribution = "unresolved"
        else: raise ValueError(decision)
        counts[kind][contribution] += 1
        if kind == "mandatory" and contribution != "excluded": mandatory.append(contribution)
    status = "NON_COMPLIANT" if "proven_failure" in mandatory else "BLOCKED" if "blocked" in mandatory else "UNVERIFIED" if "unresolved" in mandatory else "CONDITIONALLY_COMPLIANT" if "waived_failure" in mandatory else "NO_MANDATORY_REQUIREMENTS" if not mandatory else "COMPLIANT"
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


def main() -> int:
    checks: list[dict[str, str]] = []
    def check(cid: str, category: str, description: str, ok: bool, detail: str = "") -> None: checks.append({"check_id": cid, "category": category, "description": description, "result": "PASS" if ok else "FAIL", "detail": detail})
    def blocked(cid: str, category: str, description: str, detail: str) -> None: checks.append({"check_id": cid, "category": category, "description": description, "result": "BLOCKED", "detail": detail})

    for index, name in enumerate(DELIVERABLES, 1): check(f"F{index:02d}", "artifacts", f"v13.3 artifact exists: {name}", (DEST / name).is_file())
    if any(item["result"] == "FAIL" for item in checks): return finish(checks, {})
    check("F68", "artifacts", "generator owns exactly 67 unique deliverables", len(DELIVERABLES) == len(set(DELIVERABLES)) == 67)
    check("F69", "artifacts", "all generated YAML is JSON-compatible", all(parseable(DEST / name) for name in DELIVERABLES))

    vocabulary = load(DEST / "NORMATIVE-VOCABULARY.yaml")
    check("N01", "normative", "MUST/MUST_NOT/SHOULD/SHOULD_NOT/MAY are defined", set(vocabulary["keywords"]) == {"MUST", "MUST_NOT", "SHOULD", "SHOULD_NOT", "MAY"} and vocabulary["guidance_changes_conformance"] is False)
    domains = load(DEST / "STATE-DOMAINS.yaml")["domains"]
    check("N02", "states", "all four state vocabularies are exact", set(domains["finding"]) == FINDING_STATES and set(domains["remediation"]) == REMEDIATION_STATES and set(domains["program"]) == PROGRAM_STATES and set(domains["conformance"]) == CONFORMANCE_STATES)
    check("N03", "separation", "truth/process/time axes cannot substitute", load(DEST / "STATE-DOMAINS.yaml")["substitution"] == "MUST_NOT" and set(load(DEST / "STATE-DOMAINS.yaml")["axes"]) == {"TRUTH", "PROCESS", "TIME"})

    schemas = {name: load(SCHEMA / f"{name}.schema.yaml") for name in SCHEMA_NAMES}
    check("S01", "schemas", "nineteen dedicated schemas exist", len(schemas) == 19 and set(schemas) == set(SCHEMA_NAMES))
    check("S02", "schemas", "four lifecycle enum schemas are exact", set(schemas["finding-state"]["enum"]) == FINDING_STATES and set(schemas["remediation-state"]["enum"]) == REMEDIATION_STATES and set(schemas["program-state"]["enum"]) == PROGRAM_STATES and set(schemas["conformance-state"]["enum"]) == CONFORMANCE_STATES)
    transition_required = {"transition_id", "object_type", "object_id", "from_state", "to_state", "reason", "evidence_refs", "actor", "occurred_at", "sequence", "previous_transition", "event_hash", "schema_version"}
    check("S03", "schemas", "transition schema matches v13.3 record and sequence begins at zero", set(schemas["state-transition"]["required"]) == transition_required and schemas["state-transition"]["properties"]["sequence"]["minimum"] == 0 and set(schemas["state-transition"]["properties"]["object_type"]["enum"]) == {"FINDING", "REMEDIATION", "PROGRAM", "COMPLIANCE_DECISION"})
    unresolved = []
    for owner, body in schemas.items():
        def scan(value: Any) -> None:
            if isinstance(value, dict):
                if "$ref" in value and Path(value["$ref"]).name.replace(".schema.yaml", "") not in schemas: unresolved.append((owner, value["$ref"]))
                for child in value.values(): scan(child)
            elif isinstance(value, list):
                for child in value: scan(child)
        scan(body)
    check("S04", "schemas", "all schema references resolve", not unresolved, str(unresolved))
    registry = load(DEST / "SCHEMA-REGISTRY.yaml")
    check("S05", "schemas", "schema registry hashes all nineteen files", len(registry["schemas"]) == 19 and all(sha_file(DEST / item["path"]) == item["sha256"] for item in registry["schemas"]))
    check("S06", "schemas", "history failures have the exact nine-code vocabulary", set(schemas["history-integrity-failure"]["properties"]["failure_code"]["enum"]) == FAILURE_CODES)
    check("S07", "schemas", "aggregate result includes empty mandatory scope state", set(schemas["aggregate-result"]["properties"]["status"]["enum"]) == AGGREGATE_STATES)

    finding_matrix = matrix("FINDING-TRANSITION-TABLE.yaml"); remediation_matrix = matrix("REMEDIATION-TRANSITION-TABLE.yaml"); program_matrix = matrix("PROGRAM-TRANSITION-TABLE.yaml")
    expected_finding = {"DETECTED": ["VALIDATED", "REJECTED", "BLOCKED"], "VALIDATED": ["CLASSIFIED", "REJECTED", "BLOCKED"], "CLASSIFIED": ["OPEN", "REJECTED", "BLOCKED"], "OPEN": ["UNDER_REMEDIATION", "WAIVED", "SUPERSEDED", "BLOCKED"], "UNDER_REMEDIATION": ["RESOLVED", "OPEN", "BLOCKED"], "RESOLVED": ["CLOSED", "OPEN"], "CLOSED": ["SUPERSEDED"], "BLOCKED": ["$PREVIOUS_OPERATIONAL_STATE", "REJECTED", "SUPERSEDED"], "WAIVED": ["SUPERSEDED"], "REJECTED": ["SUPERSEDED"]}
    expected_remediation = {"PROPOSED": ["ASSESSED", "REJECTED", "CANCELLED"], "ASSESSED": ["APPROVED", "REJECTED", "CANCELLED"], "APPROVED": ["IN_PROGRESS", "CANCELLED"], "IN_PROGRESS": ["READY_FOR_VERIFICATION", "BLOCKED", "FAILED", "CANCELLED"], "READY_FOR_VERIFICATION": ["REVERIFICATION", "BLOCKED", "FAILED"], "REVERIFICATION": ["REGRESSION", "COMPLETE", "IN_PROGRESS", "BLOCKED", "FAILED"], "REGRESSION": ["COMPLETE", "REVERIFICATION", "IN_PROGRESS", "BLOCKED", "FAILED"], "COMPLETE": ["SUPERSEDED"], "FAILED": ["PROPOSED", "SUPERSEDED"], "BLOCKED": ["$PREVIOUS_OPERATIONAL_STATE", "FAILED", "CANCELLED", "SUPERSEDED"], "REJECTED": ["SUPERSEDED"], "CANCELLED": ["SUPERSEDED"]}
    expected_program = {"CREATED": ["TRIAGED", "CANCELLED"], "TRIAGED": ["PLANNED", "CANCELLED", "SUPERSEDED"], "PLANNED": ["ACTIVE", "CANCELLED", "SUPERSEDED"], "ACTIVE": ["EVALUATING", "BLOCKED", "SUPERSEDED", "FAILED"], "EVALUATING": ["COMPLETED", "BLOCKED", "SUPERSEDED", "FAILED"], "BLOCKED": ["ACTIVE", "EVALUATING", "FAILED", "CANCELLED", "SUPERSEDED"]}
    check("T01", "transition-table", "finding transition matrix is exact", finding_matrix == expected_finding)
    check("T02", "transition-table", "remediation transition matrix is exact", remediation_matrix == expected_remediation)
    check("T03", "transition-table", "program transition matrix is exact", program_matrix == expected_program)
    check("T04", "terminal", "forbidden direct and terminal restart transitions are absent", "CLOSED" not in finding_matrix.get("DETECTED", []) and "IN_PROGRESS" not in remediation_matrix.get("COMPLETE", []) and not program_matrix.get("COMPLETED"))
    tables = {domain: load(DEST / f"{domain}-TRANSITION-TABLE.yaml")["transitions"] for domain in ["FINDING", "REMEDIATION", "PROGRAM"]}
    guard_defs = {item["guard_id"]: item["all_of"] for item in load(DEST / "TRANSITION-GUARDS.yaml")["guards"]}
    check("T05", "guards", "every legal transition resolves exactly one non-empty guard", all(entry["guard_id"] in guard_defs and guard_defs[entry["guard_id"]] for entries in tables.values() for entry in entries))
    check("T06", "guards", "five program operational guards contain all specified predicates", guard_defs["PROGRAM_TRIAGE_READY"] == ["program_scope_valid", "target_findings_resolvable"] and len(guard_defs["PROGRAM_COMPLETION_READY"]) == 5 and "blocking_cause_recorded" in guard_defs["BLOCKING_CONDITION_PRESENT"])

    histories = load(DEST / "STATE-HISTORIES.yaml")["histories"]; contexts = load(DEST / "TRANSITION-GUARD-CONTEXTS.yaml")["objects"]; validations = load(DEST / "TRANSITION-VALIDATIONS.yaml")["objects"]; currents = load(DEST / "CURRENT-STATES.yaml")["objects"]
    schema_failures = []
    for history in histories:
        schema_failures += schema_errors(history, schemas["state-history"], schemas, history["history_id"])
    for item, name in [(x, "transition-guard-context") for x in contexts] + [(x, "transition-validation") for x in validations]: schema_failures += schema_errors(item, schemas[name], schemas, name)
    check("H01", "schemas", "all actual histories, transitions, currents, contexts, and validations satisfy schemas", len(histories) == len(contexts) == len(validations) == len(currents) == 6 and not schema_failures, str(schema_failures[:10]))
    events = [history["transitions"][0] for history in histories]
    check("H02", "initial-transition", "all baseline transitions use null predecessor and sequence zero", all(event["from_state"] is None and event["previous_transition"] is None and event["sequence"] == 0 for event in events))
    check("H03", "hashes", "all event/current/history/context/validation hashes validate", all(event["event_hash"] == digest({key: value for key, value in event.items() if key != "event_hash"}) for event in events) and all(current["projection_hash"] == digest({key: value for key, value in current.items() if key != "projection_hash"}) for current in currents) and all(history["history_hash"] == digest({key: value for key, value in history.items() if key != "history_hash"}) for history in histories) and all(item["context_hash"] == digest({key: value for key, value in item.items() if key != "context_hash"}) for item in contexts) and all(item["validation_hash"] == digest({key: value for key, value in item.items() if key != "validation_hash"}) for item in validations))
    check("H04", "validation", "all eleven transition predicates are true for all six current events", all(set(item["predicates"]) == set(PREDICATES) and all(item["predicates"].values()) and item["result"] == "VALID_TRANSITION" for item in validations))
    check("H05", "projection", "three findings project OPEN and three programs project CREATED", [item["state"] for item in currents if item["object_type"] == "FINDING"] == ["OPEN"] * 3 and [item["state"] for item in currents if item["object_type"] == "PROGRAM"] == ["CREATED"] * 3)
    check("H06", "failure-objects", "no current malformed history or fabricated failure exists", load(DEST / "HISTORY-INTEGRITY-FAILURES.yaml")["objects"] == [])
    history_vectors = load(DEST / "HISTORY-VALIDATION-TEST-VECTORS.yaml"); history_errors = []; failure_schema_errors = []
    for item in history_vectors["vectors"]:
        result, code = validate_history_vector(item, tables, guard_defs)
        if result != item["expected_result"] or result != item["actual_result"] or code != item["expected_failure_code"] or code != item["actual_failure_code"] or not item["pass"]: history_errors.append(item["vector_id"])
        if item["failure"]:
            failure_schema_errors += schema_errors(item["failure"], schemas["history-integrity-failure"], schemas, item["vector_id"])
            if item["failure"]["failure_code"] != code or item["failure"]["failure_hash"] != digest({key: value for key, value in item["failure"].items() if key != "failure_hash"}): failure_schema_errors.append(item["vector_id"])
        elif result != "VALID": failure_schema_errors.append(item["vector_id"])
    check("H07", "test-vectors", "all ten history vectors reproduce with exact failure boundaries", history_vectors["summary"] == {"total": 10, "passed": 10, "failed": 0} and not history_errors, str(history_errors))
    check("H07A", "failure-schema", "every invalid vector emits a schema-valid HistoryIntegrityFailure", not failure_schema_errors and sum(item["failure"] is not None for item in history_vectors["vectors"]) == 9, str(failure_schema_errors[:10]))
    transition_vectors = load(DEST / "TRANSITION-VALIDATION-TEST-VECTORS.yaml"); transition_errors = [item["vector_id"] for item in transition_vectors["vectors"] if ("VALID_TRANSITION" if all(item["predicates"].values()) else "TRANSITION_INVALID") != item["actual"] or item["actual"] != item["expected"] or not item["pass"]]
    check("H08", "test-vectors", "all twelve transition conjunction vectors execute independently", transition_vectors["summary"] == {"total": 12, "passed": 12, "failed": 0} and not transition_errors, str(transition_errors))
    check("H09", "non-invention", "baseline policy claims no predecessor chronology", load(DEST / "BASELINE-IMPORT-POLICY.yaml")["historical_claim"] == "NO_PRE_V13.3_CHRONOLOGY_RECONSTRUCTED")

    decision_rules = load(DEST / "DECISION-PROJECTION-RULES.yaml")
    check("D01", "decision", "snapshot mismatch and invalid-latest outcomes are explicit", decision_rules["snapshot_mismatch"] == "DECISION_SNAPSHOT_MISMATCH" and decision_rules["latest_invalid"] == "DECISION_HISTORY_INVALID_NO_FALLBACK" and decision_rules["immutability"] is True)
    decision_vectors = load(DEST / "DECISION-PROJECTION-TEST-VECTORS.yaml"); decision_errors = []; decision_schema_errors = []
    for item in decision_vectors["vectors"]:
        result, current = project_decision(item["records"], item["arguments"]); current_id = current["decision_id"] if current else None
        if result != item["expected"] or result != item["actual"] or current_id != item["expected_decision_id"] or current_id != item["actual_decision_id"] or current != item["current_projection"] or not item["pass"]: decision_errors.append(item["vector_id"])
        for record in item["records"]: decision_schema_errors += schema_errors(record, schemas["compliance-decision-record"], schemas, item["vector_id"])
        if current: decision_schema_errors += schema_errors(current, schemas["current-decision"], schemas, item["vector_id"])
    check("D02", "test-vectors", "all seven decision vectors reproduce, including temporal contamination", decision_vectors["summary"] == {"total": 7, "passed": 7, "failed": 0} and not decision_errors, str(decision_errors))
    check("D03", "schemas", "synthetic decision records and projections exercise both decision schemas", not decision_schema_errors, str(decision_schema_errors[:10]))
    check("D04", "current", "invalid current scope produces no fabricated decision", load(DEST / "COMPLIANCE-DECISION-HISTORIES.yaml")["records"] == [] and load(DEST / "CURRENT-DECISIONS.yaml")["objects"] == [])
    check("D05", "temporal", "superseding decision preserves predecessor in test history", len(next(item for item in decision_vectors["vectors"] if item["vector_id"] == "SUPERSESSION_CURRENT")["records"]) == 2)

    waiver_rules = load(DEST / "WAIVER-RESOLUTION-RULES.yaml")
    check("W01", "waiver", "waiver resolver uses only declared snapshot/as-of inputs and cannot mutate decisions", waiver_rules["mutates_decision"] is False and waiver_rules["wall_clock_input"] is False and waiver_rules["effect"] == "CHANGE_AGGREGATE_CONTRIBUTION_ONLY")
    waiver_vectors = load(DEST / "WAIVER-TEST-VECTORS.yaml"); waiver_errors = []; waiver_schema_errors = []
    for item in waiver_vectors["vectors"]:
        result, effective = waiver(item["waiver"])
        if result != item["expected"] or result != item["actual"] or effective != item["expected_effective"] or effective != item["actual_effective"] or item["underlying_decision_mutated"] or not item["pass"]: waiver_errors.append(item["vector_id"])
        waiver_schema_errors += schema_errors(item["waiver"], schemas["waiver-record"], schemas, item["vector_id"])
        waiver_schema_errors += schema_errors(item["resolution"], schemas["waiver-resolution"], schemas, item["vector_id"])
        if item["resolution"]["result"] != result or item["resolution"]["effective"] != effective or item["resolution"]["resolution_hash"] != digest({key: value for key, value in item["resolution"].items() if key != "resolution_hash"}): waiver_schema_errors.append(item["vector_id"])
    check("W02", "test-vectors", "all five waiver vectors reproduce independently", waiver_vectors["summary"] == {"total": 5, "passed": 5, "failed": 0} and not waiver_errors, str(waiver_errors))
    check("W03", "schemas", "all synthetic waiver records satisfy their schema", not waiver_schema_errors, str(waiver_schema_errors[:10]))
    check("W04", "current", "current package invents no waiver or waiver resolution", load(DEST / "WAIVERS-V133.yaml")["objects"] == [] and load(DEST / "WAIVER-RESOLUTIONS.yaml")["objects"] == [])

    function = load(DEST / "AGGREGATE-FUNCTION.yaml")
    check("A01", "aggregate", "one pure normative aggregate function has no hidden inputs", function["single_normative_function"] is True and function["pure"] is True and function["hidden_mutable_inputs"] == [])
    check("A02", "aggregate", "aggregate input excludes finding/remediation/program lifecycle state", function["inputs"] == ["CURRENT_DECISIONS", "APPLICABILITY", "MANDATORY_CLASSIFICATION", "EFFECTIVE_WAIVERS"])
    aggregate_vectors = load(DEST / "AGGREGATE-TEST-VECTORS.yaml"); aggregate_errors = []; aggregate_schema_errors = []
    for item in aggregate_vectors["vectors"]:
        actual = aggregate(item["requirements"]); result_object = item["aggregate_result"]
        if actual["status"] != item["expected"] or actual["status"] != item["actual"] or actual["mandatory_counts"] != item["mandatory_counts"] or actual["optional_counts"] != item["optional_counts"] or result_object["status"] != actual["status"] or not item["pass"]: aggregate_errors.append(item["vector_id"])
        aggregate_schema_errors += schema_errors(result_object, schemas["aggregate-result"], schemas, item["vector_id"])
        if result_object["aggregate_hash"] != digest({key: value for key, value in result_object.items() if key != "aggregate_hash"}): aggregate_schema_errors.append(item["vector_id"])
    check("A03", "test-vectors", "all twelve canonical aggregate vectors reproduce independently", aggregate_vectors["summary"] == {"total": 12, "passed": 12, "failed": 0} and not aggregate_errors, str(aggregate_errors))
    check("A03A", "schemas", "all synthetic aggregate results validate with canonical hashes", not aggregate_schema_errors, str(aggregate_schema_errors[:10]))
    by_id = {item["vector_id"]: item["actual"] for item in aggregate_vectors["vectors"]}
    check("A04", "precedence", "failure dominates blocker; blocker dominates waiver and unresolved", by_id["TEST-06-FAILURE-PLUS-BLOCKER"] == "NON_COMPLIANT" and by_id["TEST-07-WAIVER-PLUS-BLOCKER"] == "BLOCKED" and by_id["TEST-08-WAIVER-PLUS-UNRESOLVED"] == "UNVERIFIED")
    check("A05", "empty-scope", "all-N/A and empty scope are NO_MANDATORY_REQUIREMENTS", by_id["TEST-10-ALL-NA"] == by_id["TEST-11-EMPTY-SCOPE"] == "NO_MANDATORY_REQUIREMENTS")
    check("A06", "optional", "optional failure is reported but does not change compliance", by_id["TEST-09-OPTIONAL-FAILURE"] == "COMPLIANT" and next(item for item in aggregate_vectors["vectors"] if item["vector_id"] == "TEST-09-OPTIONAL-FAILURE")["optional_counts"]["proven_failure"] == 1)
    invariants = load(DEST / "AGGREGATE-INVARIANTS.yaml")["invariants"]
    check("A07", "invariants", "all fifteen aggregate invariants are machine checked", len(invariants) == 15 and [item["id"] for item in invariants] == [f"AGG-{index:03d}" for index in range(1, 16)] and all(item["machine_checked"] for item in invariants))
    separation = load(DEST / "CONFORMANCE-SEPARATION-TEST-VECTORS.yaml")
    check("A08", "separation", "all four lifecycle/conformance/history independence vectors pass", separation["summary"] == {"total": 4, "passed": 4, "failed": 0} and all(item["pass"] for item in separation["vectors"]))
    purity = load(DEST / "DETERMINISM-PURITY-TEST-VECTORS.yaml")
    check("A09", "purity", "four reordered executions produce identical aggregate and counts", purity["summary"] == {"total": 4, "passed": 4, "failed": 0} and purity["declared_inputs_only"] is True and all(item["pass"] and item["counts_identical"] for item in purity["vectors"]))

    derivation_function = load(DEST / "PROGRAM-DERIVATION-FUNCTION.yaml"); expected_precedence = ["SUPERSEDED", "CANCELLED", "FAILED", "BLOCKED", "COMPLETED", "EVALUATING", "ACTIVE", "PLANNED", "TRIAGED", "CREATED"]
    check("P01", "program", "program derives from history, member states, and predicates with exact precedence", derivation_function["inputs"] == ["PROGRAM_HISTORY", "MEMBER_REMEDIATION_CURRENT_STATES", "PROGRAM_LEVEL_PREDICATES"] and derivation_function["precedence"] == expected_precedence and len(derivation_function["derivation_rules"]) == 10 and derivation_function["manual_completed_flag"] == "FORBIDDEN")
    program_vectors = load(DEST / "PROGRAM-DERIVATION-TEST-VECTORS.yaml"); program_errors = [item["vector_id"] for item in program_vectors["vectors"] if derive_program(item["history_current_state"], item["member_states"], item["predicates"]) != item["actual"] or item["actual"] != item["expected"] or not item["pass"]]
    check("P02", "test-vectors", "all ten program derivation vectors reproduce independently", program_vectors["summary"] == {"total": 10, "passed": 10, "failed": 0} and not program_errors, str(program_errors))
    check("P03", "multi-member", "two complete plus one blocked remediation derives BLOCKED", next(item for item in program_vectors["vectors"] if item["vector_id"] == "TWO-COMPLETE-ONE-BLOCKED")["actual"] == "BLOCKED")
    derivations = load(DEST / "PROGRAM-DERIVATIONS.yaml")["objects"]; derivation_errors = []
    for item in derivations:
        derivation_errors += schema_errors(item, schemas["program-derivation"], schemas, item["derivation_id"])
        if item["derived_state"] != derive_program(item["history_current_state"], item["member_remediation_states"], item["predicates"]) or item["derivation_hash"] != digest({key: value for key, value in item.items() if key != "derivation_hash"}): derivation_errors.append(item["derivation_id"])
    check("P04", "current", "three no-member programs reproducibly remain CREATED", len(derivations) == 3 and not derivation_errors and all(item["member_remediation_ids"] == [] and item["derived_state"] == "CREATED" for item in derivations), str(derivation_errors))

    pipeline = load(DEST / "VALIDATION-PIPELINE.yaml")
    check("B01", "pipeline", "all seventeen ordered validation stages are present", [item["number"] for item in pipeline["stages"]] == list(range(1, 18)) and len(pipeline["stages"]) == 17 and pipeline["upstream_failure_behavior"] == "STOP_DEPENDENT_DOWNSTREAM_CLAIMS")
    boundaries = {item["failure"]: item["result"] for item in load(DEST / "FAILURE-BOUNDARIES.yaml")["boundaries"]}
    check("B02", "boundaries", "seven failure boundaries preserve attribution", boundaries == {"SPEC_INVALID": "AUDIT_BLOCKED", "SCOPE_INVALID": "AUDIT_BLOCKED", "HISTORY_INVALID": "AFFECTED_EVALUATION_BLOCKED", "DECISION_INVALID": "AFFECTED_REQUIREMENT_BLOCKED", "ORACLE_INVALID": "AFFECTED_VERIFICATION_BLOCKED", "VERIFICATION_INVALID": "AFFECTED_REQUIREMENT_UNVERIFIED_OR_BLOCKED", "VALID_PROVEN_FAILURE": "NON_COMPLIANT"})
    snapshot = load(DEST / "AUDIT-SNAPSHOT.yaml")["objects"][0]; execution = load(DEST / "CURRENT-PIPELINE-EXECUTION.yaml")["objects"][0]; audit_status = load(DEST / "CURRENT-AUDIT-STATUS.yaml")["objects"][0]
    object_schema_errors = schema_errors(snapshot, schemas["audit-snapshot"], schemas, "snapshot") + schema_errors(execution, schemas["pipeline-execution"], schemas, "pipeline") + schema_errors(audit_status, schemas["audit-status"], schemas, "status")
    check("B03", "schemas", "snapshot, pipeline execution, and audit status validate", not object_schema_errors, str(object_schema_errors))
    check("B04", "pipeline", "current audit stops at specification validation before aggregate", execution["stopped_at"] == 2 and execution["result"] == "AUDIT_BLOCKED" and execution["stages"][1]["failure"] == "SPEC_INVALID" and all(item["status"] == "NOT_EXECUTED_UPSTREAM_STOP" for item in execution["stages"][2:]))
    current_aggregate = load(DEST / "CURRENT-AGGREGATE.yaml")
    check("B05", "aggregate-boundary", "no aggregate is assigned after upstream specification failure", current_aggregate["objects"] == [] and current_aggregate["execution_status"] == "NOT_EXECUTED_UPSTREAM_FAILURE" and current_aggregate["empty_scope_not_treated_as_compliant"] is True)
    check("B06", "audit-status", "audit status is BLOCKED without an aggregate or certification eligibility", audit_status["status"] == "BLOCKED" and audit_status["aggregate_id"] is None and audit_status["certification_eligible"] is False)
    check("B07", "hashes", "snapshot, pipeline, and audit status hashes validate", snapshot["snapshot_hash"] == digest({key: value for key, value in snapshot.items() if key != "snapshot_hash"}) and execution["execution_hash"] == digest({key: value for key, value in execution.items() if key != "execution_hash"}) and audit_status["status_hash"] == digest({key: value for key, value in audit_status.items() if key != "status_hash"}))
    certificate = load(DEST / "CERTIFICATE-STATUS.yaml"); prior_certificate = load(OUT / "AUDIT-CERTIFICATE.yaml")["objects"][0]
    check("B08", "certificate", "certificate revision remains unauthorized with exact predecessor lineage", certificate["status"] == "NOT_AUTHORIZED" and certificate["aggregate_id"] is None and certificate["lineage_modified"] is False and certificate["prior_certificate_id"] == prior_certificate["object_id"] and certificate["prior_certificate_hash"] == prior_certificate["certificate_hash"])

    transform = load(DEST / "COMPLETE-TRANSFORMATION.yaml"); axes = load(DEST / "AXIS-SEPARATION.yaml")
    check("X01", "transformation", "truth and lifecycle chains remain explicitly parallel", transform["truth_chain"][-3:] == ["CURRENT_DECISION", "AGGREGATE", "CERTIFICATE"] and transform["lifecycle_chain"] == ["EVENTS", "HISTORY_VALIDATION", "CURRENT_STATE"] and transform["conflation"] == "FORBIDDEN")
    check("X02", "axes", "truth/process/time axes and strongest invariants are exact", set(axes["axes"]) == {"TRUTH", "PROCESS", "TIME"} and len(axes["strongest_invariants"]) == 4)
    object_registry = load(DEST / "OBJECT-REGISTRY.yaml"); ids = [item["object_id"] for item in object_registry["objects"]]
    check("X03", "registry", "all thirty-six v13.3 normative object IDs are unique", len(ids) == len(set(ids)) == 36)
    external_ids = {item["object_id"] for path in [OUT / "OBJECT-REGISTRY.yaml", REM / "OBJECT-REGISTRY.yaml", REM / "v13.1" / "OBJECT-REGISTRY.yaml", V132 / "OBJECT-REGISTRY.yaml"] for item in load(path)["objects"]}
    check("X04", "registry", "v13.3 IDs are globally unique from predecessors", not (set(ids) & external_ids))
    check("X05", "references", "all four predecessor registries resolve with exact hashes", len(object_registry["external_registries"]) == 4 and all((DEST / item["path"]).is_file() and sha_file(DEST / item["path"]) == item["sha256"] for item in object_registry["external_registries"]))
    validation_report = load(DEST / "VALIDATION-REPORT.yaml")
    check("X06", "report", "generated validation report preserves blocked boundary and no aggregate", validation_report["overall_status"] == "STRUCTURAL_PASS_AUDIT_BLOCKED" and validation_report["aggregate_execution"] == "NOT_EXECUTED_UPSTREAM_FAILURE" and validation_report["audit_status"] == "BLOCKED")
    reports = [load(DEST / f"reports/{name}") for name in REPORT_FILES]
    check("X07", "reports", "all four reports preserve state, aggregate, boundary, and certificate separation", reports[0]["status"] == "PASS" and reports[1]["single_normative_function"] is True and reports[2]["downstream_aggregate_claim"] is False and reports[3]["certificate_revision"] is False)

    prior = load(DEST / "PRIOR-INTEGRITY.yaml"); prior_errors = [item["path"] for item in prior["artifacts"] if not (OUT / item["path"]).is_file() or sha_file(OUT / item["path"]) != item["sha256"] or (OUT / item["path"]).stat().st_size != item["bytes"]]
    check("R01", "append-only", "all 219 predecessor compliance artifacts remain byte-identical", prior["status"] == "PRESERVED" and prior["protected_artifact_count"] == len(prior["artifacts"]) == 219 and not prior_errors, str(prior_errors))
    check("R02", "append-only", "v13.2 builder refuses to erase v13.3 extension", "refusing to erase predecessor artifacts after append-only v13.3 extension" in (HS / "tools/build_current_state_projection_v132.py").read_text())
    determinism = load(DEST / "DETERMINISM-VALIDATION.yaml") if (DEST / "DETERMINISM-VALIDATION.yaml").is_file() else {}
    check("Q01", "determinism", "all 67 generator outputs reproduce byte-for-byte", determinism.get("status") == "PASS" and determinism.get("summary") == {"total": 67, "identical": 67, "different": 0} and {item["path"] for item in determinism.get("files", [])} == set(DELIVERABLES) and all(item["byte_identical"] for item in determinism.get("files", [])))
    regression = load(DEST / "REGRESSION-VALIDATION.yaml") if (DEST / "REGRESSION-VALIDATION.yaml").is_file() else {}
    expected_regression = {"13.2": (117, 0, 1), "13.1": (110, 0, 1), "13.0": (115, 0, 1), "12.1": (194, 0, 1), "12.0": (148, 0, 1), "11.1": (177, 0, 1), "10.1": (143, 0, 1)}
    actual_regression = {item["protocol"]: (item["passed"], item["failed"], item["blocked"]) for item in regression.get("regressions", [])}
    check("Q02", "regression", "v10.1 through v13.2 regressions and all append guards pass", regression.get("status") == "PASS" and actual_regression == expected_regression and regression.get("append_only_guards") == {"v13": "PASS_REFUSED", "v13.1": "PASS_REFUSED", "v13.2": "PASS_REFUSED", "v13.3": "PASS_REFUSED"})
    check("Q03", "hygiene", "no Python caches exist", not any(HS.rglob("__pycache__")) and not any(HS.rglob("*.pyc")))
    check("Q04", "tools", "generic and pinned v13.3 tools exist", all((HS / "tools" / name).is_file() for name in ["build_executable_state_validation.py", "build_executable_state_validation_v133.py", "validate_executable_state_validation.py", "validate_executable_state_validation_v133.py"]))
    blocked("GATE-V133", "acceptance", "current audit certification", "The executable protocol validates, but current specification validation fails at stage 2; aggregate execution is correctly suppressed, audit status is BLOCKED, and certificate revision is unauthorized.")
    return finish(checks, {"schemas": 19, "transition_tables": 3, "current_transitions": 6, "current_histories": 6, "current_states": 6, "decision_records": 0, "waivers": 0, "program_derivations": 3, "aggregate_results": 0, "audit_statuses": 1})


def parseable(path: Path) -> bool:
    try: load(path); return True
    except Exception: return False


def finish(checks: list[dict[str, str]], counts: dict[str, Any]) -> int:
    passed = sum(item["result"] == "PASS" for item in checks); failed = sum(item["result"] == "FAIL" for item in checks); blocked_count = sum(item["result"] == "BLOCKED" for item in checks)
    report = {"schema_version": VERSION, "validator": "Protocol-v13.3 independent executable validator", "overall_status": "FAIL" if failed else "STRUCTURAL_PASS_AUDIT_BLOCKED" if blocked_count else "PASS", "acceptance": "VALIDATION_FAILED" if failed else "BLOCKED" if blocked_count else "PASS", "summary": {"total": len(checks), "passed": passed, "failed": failed, "blocked": blocked_count}, "object_counts": counts, "checks": checks}
    (DEST / "VALIDATION.yaml").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    lines = ["# Protocol-v13.3 Independent Executable Validation", "", f"**Overall:** `{report['overall_status']}`", f"**Acceptance:** `{report['acceptance']}`", f"**Checks:** {passed} PASS / {failed} FAIL / {blocked_count} BLOCKED ({len(checks)} total)", "", "Executable protocol validity does not bypass the upstream invalid-specification boundary or create an aggregate/certificate claim.", "", "| ID | Category | Result | Description | Detail |", "|---|---|---|---|---|"]
    for item in checks: lines.append("| %s | %s | %s | %s | %s |" % (item["check_id"], item["category"], item["result"], item["description"].replace("|", "\\|"), item["detail"].replace("|", "\\|")))
    (DEST / "VALIDATION.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{passed} PASS / {failed} FAIL / {blocked_count} BLOCKED ({len(checks)} checks); {report['overall_status']}")
    return 1 if failed else 0


if __name__ == "__main__": sys.exit(main())
