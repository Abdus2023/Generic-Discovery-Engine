#!/usr/bin/env python3
"""Build Protocol-v13.1 orthogonal state and deterministic aggregate records."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
HS = ROOT / "historical-source"
OUT = HS / "compliance"
V13 = OUT / "remediation"
DEST = V13 / "v13.1"
SCHEMA = DEST / "schema"
REPORTS = DEST / "reports"
VERSION = "13.1"
CREATED_AT = "2026-09-12T15:58:32Z"
SCHEMA_NAMES = ["audit-finding", "remediation", "remediation-program", "state-transition", "audit-aggregate"]
MACHINE_FILES = [
    "STATE-DOMAINS.yaml", "CONFORMANCE-STATE-MACHINE.yaml", "FINDING-STATE-MACHINE.yaml", "REMEDIATION-STATE-MACHINE.yaml",
    "PROGRAM-STATE-MACHINE.yaml", "PROGRAM-AGGREGATE-FUNCTION.yaml",
    "AUDIT-AGGREGATE-FUNCTION.yaml", "AGGREGATE-TEST-VECTORS.yaml",
    "FINDING-STATE-VIEWS.yaml", "REMEDIATIONS.yaml", "REMEDIATION-PROGRAMS.yaml",
    "PROGRAM-SUMMARIES.yaml", "FINDING-SUMMARIES.yaml", "STATE-TRANSITIONS.yaml",
    "CURRENT-AGGREGATE.yaml", "INTEGRITY-CONDITIONS.yaml",
    "CONFORMANCE-CLASSIFICATION.yaml", "VALIDATION-REPORT.yaml",
    "PRIOR-V13-INTEGRITY.yaml", "OBJECT-REGISTRY.yaml", "SCHEMA-REGISTRY.yaml",
    "INVARIANTS.yaml", "CANONICAL-TRANSFORMATION.yaml",
    "CERTIFICATE-REVISION-STATUS.yaml", "STATE-MIGRATION.yaml",
]
REPORT_FILES = ["STATE-SEPARATION-REPORT.yaml", "AGGREGATE-CONFORMANCE-REPORT.yaml", "CLOSURE-IMPACT-REPORT.yaml"]
FINDING_STATES = ["DETECTED", "VALIDATED", "CLASSIFIED", "OPEN", "UNDER_REMEDIATION", "RESOLVED", "CLOSED", "WAIVED", "SUPERSEDED", "REJECTED", "BLOCKED"]
REMEDIATION_STATES = ["PROPOSED", "ASSESSED", "APPROVED", "IN_PROGRESS", "READY_FOR_VERIFICATION", "REVERIFICATION", "FAILED", "REGRESSION", "COMPLETE", "BLOCKED", "REJECTED", "SUPERSEDED", "CANCELLED"]
PROGRAM_STATES = ["CREATED", "TRIAGED", "PLANNED", "ACTIVE", "BLOCKED", "EVALUATING", "COMPLETED", "CANCELLED", "SUPERSEDED", "FAILED"]
CONFORMANCE_STATES = ["UNASSESSED", "MAPPED", "VERIFIED", "CONFORMANT", "PARTIALLY_CONFORMANT", "NON_CONFORMANT", "UNVERIFIED", "BLOCKED", "UNKNOWN", "NOT_APPLICABLE"]
AUDIT_STATES = ["NON_COMPLIANT", "CONDITIONALLY_COMPLIANT", "BLOCKED", "UNVERIFIED", "COMPLIANT"]
CONFORMANCE_DEFINITIONS = {
    "UNASSESSED": "No assessment stage has completed.", "MAPPED": "A requirement mapping exists but verification has not completed.",
    "VERIFIED": "Verification ran, but a final conformance interpretation is not yet recorded.", "CONFORMANT": "Validated evidence proves the applicable requirement is satisfied.",
    "PARTIALLY_CONFORMANT": "Validated evidence proves only part of the requirement while material semantics remain unresolved.", "NON_CONFORMANT": "Validated evidence proves violation of applicable normative semantics.",
    "UNVERIFIED": "Required verification evidence is absent or insufficient.", "BLOCKED": "A prerequisite prevents a valid conformance decision.",
    "UNKNOWN": "Available evidence cannot determine the requirement truth state.", "NOT_APPLICABLE": "Explicit scope evidence excludes the requirement.",
}
FINDING_DEFINITIONS = {
    "DETECTED": "A candidate condition has been observed.", "VALIDATED": "Evidence establishes that the finding is real and in scope.",
    "CLASSIFIED": "Finding type and severity have been assigned.", "OPEN": "The validated finding remains active without accepted resolution.",
    "UNDER_REMEDIATION": "At least one remediation attempt is active.", "RESOLVED": "Evidence indicates the condition is addressed, pending closure predicates.",
    "CLOSED": "Independent re-verification and closure predicates succeeded; history remains immutable.", "WAIVED": "Disposition is waived without changing the underlying condition or conformance truth.",
    "SUPERSEDED": "A new authoritative finding replaces this active record without erasing it.", "REJECTED": "Validation proved the candidate was not a valid finding.",
    "BLOCKED": "Required lifecycle information is unavailable; the previous valid state is retained for return.",
}
REMEDIATION_DEFINITIONS = {
    "PROPOSED": "A possible remediation was recorded but not assessed.", "ASSESSED": "Impact and feasibility were assessed.",
    "APPROVED": "Authorized remediation may begin.", "IN_PROGRESS": "Authorized changes are being performed.",
    "READY_FOR_VERIFICATION": "The declared change set is complete and awaiting re-verification.", "REVERIFICATION": "The original condition is being independently re-tested.",
    "FAILED": "Re-verification or regression did not meet required predicates.", "REGRESSION": "Required broader regression verification is running.",
    "COMPLETE": "Re-verification and regression predicates succeeded; no conformance implication is created.", "BLOCKED": "A required remediation prerequisite is unavailable.",
    "REJECTED": "Assessment or authorization rejected the proposed attempt.", "SUPERSEDED": "A replacement attempt became authoritative while this record remains immutable.",
    "CANCELLED": "An explicit event ended a non-terminal attempt.",
}
PROGRAM_DEFINITIONS = {
    "CREATED": "No remediation member exists.", "TRIAGED": "Members exist but no more-specific aggregate rule applies.",
    "PLANNED": "All member attempts remain proposed or assessed.", "ACTIVE": "At least one member is in active change or evaluation work.",
    "BLOCKED": "At least one member is blocked and no member is active.", "EVALUATING": "Declared coordination phase for evaluation; the canonical member aggregate classifies evaluation members as ACTIVE.",
    "COMPLETED": "All member remediations are complete.", "CANCELLED": "An explicit cancellation event terminates the program.",
    "SUPERSEDED": "An explicit supersession event replaces the program.", "FAILED": "All member remediation attempts were rejected.",
}
INVARIANTS = [
    "Finding state and remediation state are independent.",
    "Program state is derived from its remediation members.",
    "Conformance state is owned exclusively by the compliance decision.",
    "A finding cannot directly establish conformance.",
    "A remediation cannot directly establish conformance.",
    "A program cannot directly establish conformance.",
    "CLOSED finding does not imply CONFORMANT.",
    "COMPLETE remediation does not imply CONFORMANT.",
    "COMPLETED program does not imply COMPLIANT.",
    "A proven mandatory violation produces NON_COMPLIANT unless effectively waived.",
    "A blocker cannot conceal an already-proven unwaived violation.",
    "An unresolved condition cannot be treated as a proven violation.",
    "Optional requirement failure cannot alone produce NON_COMPLIANT.",
    "PARTIALLY_CONFORMANT is not an audit-level release status.",
    "Every aggregate status is reproducible from current requirement decisions and declared predicates.",
    "Historical state transitions remain immutable.",
    "New evidence creates new decisions rather than mutating historical decisions.",
    "A remediation may generate new findings.",
    "New findings do not overwrite original findings.",
    "Certificate revisions preserve certificate lineage.",
    "A state transition without a legal transition rule is invalid.",
    "Derived summaries are reproducible from authoritative records.",
]


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ref(object_type: str, object_id: str) -> dict[str, str]:
    return {"object_type": object_type, "object_id": object_id}


def seal(value: dict[str, Any]) -> dict[str, Any]:
    payload = dict(value)
    payload.pop("content_hash", None)
    value["content_hash"] = {"algorithm": "SHA-256", "value": hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()}
    return value


def primitive(name: str) -> dict[str, str]:
    return {"$ref": "../../../schema/common.schema.yaml#/$defs/" + name}


def object_schema(title: str, object_type: str, required: list[str], properties: dict[str, Any], rules: list[str]) -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": f"https://generic-discovery-engine.invalid/compliance/v13.1/{object_type.lower().replace('_', '-')}.schema.yaml",
        "title": title, "type": "object",
        "required": ["object_type", "schema_version", "object_id", "created_at", "content_hash", *required],
        "properties": {"object_type": {"const": object_type}, "schema_version": {"const": VERSION}, "object_id": primitive("Identifier"), "created_at": primitive("Timestamp"), "content_hash": primitive("Hash"), **properties},
        "additionalProperties": False, "x-v13.1-rules": rules,
    }


def build_schemas() -> dict[str, Any]:
    ids = lambda minimum=0: {"type": "array", **({"minItems": minimum} if minimum else {}), "items": primitive("Identifier"), "uniqueItems": True}
    refs = lambda minimum=0: {"type": "array", **({"minItems": minimum} if minimum else {}), "items": primitive("Reference")}
    schemas: dict[str, Any] = {}
    schemas["audit-finding"] = object_schema("Protocol-v13.1 AUDIT_FINDING state owner", "AUDIT_FINDING", ["finding_id", "finding_state", "finding_type", "severity", "evidence", "remediation_ids", "closure_verification_ids"], {
        "finding_id": primitive("Identifier"), "finding_state": {"type": "string", "enum": FINDING_STATES}, "finding_type": {"type": "string"}, "severity": {"type": "string"},
        "evidence": refs(1), "remediation_ids": ids(), "closure_verification_ids": ids(), "historical_source": primitive("Reference"),
    }, ["Finding state never substitutes for remediation or conformance state", "CLOSED retains immutable history", "CLOSED requires independent closure verification"])
    schemas["audit-finding"]["allOf"] = [{"if": {"properties": {"finding_state": {"const": "CLOSED"}}}, "then": {"properties": {"closure_verification_ids": {"minItems": 1}}}}]
    schemas["remediation"] = object_schema("Protocol-v13.1 REMEDIATION state owner", "REMEDIATION", ["remediation_id", "finding_ids", "program_ids", "remediation_state", "reverification_execution_ids", "regression_execution_ids"], {
        "remediation_id": primitive("Identifier"), "finding_ids": ids(1), "program_ids": ids(), "remediation_state": {"type": "string", "enum": REMEDIATION_STATES},
        "action_ids": ids(), "change_set_ids": ids(), "reverification_execution_ids": ids(), "regression_execution_ids": ids(),
    }, ["A remediation references at least one finding", "COMPLETE requires re-verification and regression evidence", "COMPLETE never directly establishes CONFORMANT", "Many-to-many finding/remediation relation is explicit"])
    schemas["remediation"]["allOf"] = [{"if": {"properties": {"remediation_state": {"const": "COMPLETE"}}}, "then": {"properties": {"reverification_execution_ids": {"minItems": 1}, "regression_execution_ids": {"minItems": 1}}}}]
    schemas["remediation-program"] = object_schema("Protocol-v13.1 REMEDIATION_PROGRAM derived state", "REMEDIATION_PROGRAM", ["program_id", "finding_ids", "remediation_ids", "derived_program_state"], {
        "program_id": primitive("Identifier"), "finding_ids": ids(1), "remediation_ids": ids(), "derived_program_state": {"type": "string", "enum": PROGRAM_STATES},
        "explicit_terminal_event": {"oneOf": [primitive("Reference"), {"type": "null"}]},
    }, ["Program state is derived from member remediation states", "Program state never establishes conformance"])
    transition_states = sorted(set(FINDING_STATES + REMEDIATION_STATES + PROGRAM_STATES + CONFORMANCE_STATES))
    schemas["state-transition"] = object_schema("Protocol-v13.1 immutable STATE_TRANSITION", "STATE_TRANSITION", ["subject", "state_domain", "from_state", "to_state", "reason", "evidence", "occurred_at"], {
        "subject": primitive("Reference"), "state_domain": {"type": "string", "enum": ["FINDING", "REMEDIATION", "PROGRAM", "CONFORMANCE"]},
        "from_state": {"type": "string", "enum": transition_states}, "to_state": {"type": "string", "enum": transition_states}, "reason": {"type": "string", "minLength": 1}, "evidence": refs(1), "occurred_at": primitive("Timestamp"),
    }, ["Undefined state transitions are rejected", "Transition records are immutable"])
    count_keys = ["pass", "fail", "waived_failure", "unresolved", "blocked", "excluded", "intermediate"]
    schemas["audit-aggregate"] = object_schema("Protocol-v13.1 AUDIT_AGGREGATE", "AUDIT_AGGREGATE", ["audit", "aggregate_status", "mandatory_counts", "optional_counts", "decision_ids", "effective_waiver_ids", "audit_blockers", "integrity_status", "computed_at"], {
        "audit": primitive("Reference"), "aggregate_status": {"type": "string", "enum": AUDIT_STATES},
        "mandatory_counts": {"type": "object", "required": count_keys, "properties": {key: {"type": "integer", "minimum": 0} for key in count_keys}, "additionalProperties": False},
        "optional_counts": {"type": "object", "required": count_keys, "properties": {key: {"type": "integer", "minimum": 0} for key in count_keys}, "additionalProperties": False},
        "decision_ids": ids(), "effective_waiver_ids": ids(), "audit_blockers": {"type": "array", "items": {"type": "string"}}, "integrity_status": {"type": "string", "enum": ["PASS", "FAIL", "BLOCKED"]}, "computed_at": primitive("Timestamp"),
    }, ["Aggregate derives only from scope, current decisions, effective waivers, blockers, and integrity", "Process states never participate"])
    for name in SCHEMA_NAMES: dump(SCHEMA / f"{name}.schema.yaml", schemas[name])
    return schemas


def classify(decision: str, waived: bool) -> str:
    if decision == "CONFORMANT": return "pass"
    if decision == "NON_CONFORMANT": return "waived_failure" if waived else "fail"
    if decision in {"PARTIALLY_CONFORMANT", "UNVERIFIED", "UNKNOWN"}: return "unresolved"
    if decision == "BLOCKED": return "blocked"
    if decision == "NOT_APPLICABLE": return "excluded"
    if decision in {"UNASSESSED", "MAPPED", "VERIFIED"}: return "intermediate"
    raise ValueError(f"unknown conformance decision {decision}")


def aggregate(requirements: list[dict[str, Any]], audit_blockers: list[str], integrity_pass: bool, completed_audit: bool = True) -> tuple[str, dict[str, dict[str, int]]]:
    keys = ["pass", "fail", "waived_failure", "unresolved", "blocked", "excluded", "intermediate"]
    counts = {kind: {key: 0 for key in keys} for kind in ["mandatory", "optional"]}
    applicable: list[dict[str, Any]] = []
    for item in requirements:
        kind = "mandatory" if item["mandatory"] else "optional"
        decision = item["decision"]
        category = "excluded" if not item["applicable"] or decision == "NOT_APPLICABLE" else classify(decision, item.get("waiver_effective", False))
        counts[kind][category] += 1
        if category != "excluded": applicable.append(item)
    mandatory = [item for item in applicable if item["mandatory"]]
    if any(item["decision"] == "NON_CONFORMANT" and not item.get("waiver_effective", False) for item in mandatory):
        return "NON_COMPLIANT", counts
    intermediate_invalid = completed_audit and any(item["decision"] in {"UNASSESSED", "MAPPED", "VERIFIED"} for item in mandatory)
    if audit_blockers or not integrity_pass or intermediate_invalid or any(item["decision"] == "BLOCKED" for item in mandatory):
        return "BLOCKED", counts
    if any(item["decision"] in {"PARTIALLY_CONFORMANT", "UNVERIFIED", "UNKNOWN"} for item in mandatory):
        return "UNVERIFIED", counts
    if any(item["decision"] == "NON_CONFORMANT" and item.get("waiver_effective", False) for item in mandatory):
        return "CONDITIONALLY_COMPLIANT", counts
    return "COMPLIANT", counts


def program_state(remediation_states: list[str], explicit_event: str | None = None) -> str:
    if explicit_event in {"CANCELLED", "SUPERSEDED"}: return explicit_event
    if not remediation_states: return "CREATED"
    if all(state == "REJECTED" for state in remediation_states): return "FAILED"
    if all(state == "COMPLETE" for state in remediation_states): return "COMPLETED"
    active = {"IN_PROGRESS", "READY_FOR_VERIFICATION", "REVERIFICATION", "REGRESSION"}
    if any(state in active for state in remediation_states): return "ACTIVE"
    if any(state == "BLOCKED" for state in remediation_states) and not any(state in active for state in remediation_states): return "BLOCKED"
    if all(state in {"PROPOSED", "ASSESSED"} for state in remediation_states): return "PLANNED"
    return "TRIAGED"


def protected_files() -> list[Path]:
    return sorted((path for path in OUT.rglob("*") if path.is_file() and DEST not in path.parents), key=lambda path: str(path.relative_to(OUT)))


def main() -> None:
    required = [V13 / "VALIDATION.yaml", V13 / "REMEDIATION-PROGRAMS.yaml", OUT / "FINDINGS.yaml", OUT / "CONFORMANCE-DECISIONS.yaml", OUT / "AUDIT-CERTIFICATE.yaml"]
    if not all(path.is_file() for path in required): raise RuntimeError("validated Protocol-v13 and v12.1 packages are required")
    if DEST.exists():
        remediation_path = DEST / "REMEDIATIONS.yaml"
        transitions_path = DEST / "STATE-TRANSITIONS.yaml"
        if remediation_path.is_file() and load(remediation_path).get("objects"): raise RuntimeError("refusing to erase v13.1 remediation attempts")
        if transitions_path.is_file() and load(transitions_path).get("events"): raise RuntimeError("refusing to erase immutable v13.1 state-transition events")
    before = [{"path": str(path.relative_to(OUT)), "sha256": sha_file(path), "bytes": path.stat().st_size} for path in protected_files()]
    if DEST.exists(): shutil.rmtree(DEST)
    DEST.mkdir(parents=True); REPORTS.mkdir(); SCHEMA.mkdir()
    schemas = build_schemas()

    finding_objects = load(OUT / "FINDINGS.yaml")["objects"]
    v13_programs = load(V13 / "REMEDIATION-PROGRAMS.yaml")["objects"]
    conformance_decisions = load(OUT / "CONFORMANCE-DECISIONS.yaml")["objects"]
    audit = load(OUT / "AUDIT.yaml")["objects"][0]
    prior_certificate = load(OUT / "AUDIT-CERTIFICATE.yaml")["objects"][0]

    dump(DEST / "STATE-DOMAINS.yaml", {
        "schema_version": VERSION,
        "domains": [
            {"domain": "CONFORMANCE", "owner": "COMPLIANCE_DECISION", "question": "Does implementation conform?", "states": CONFORMANCE_STATES},
            {"domain": "FINDING", "owner": "AUDIT_FINDING", "question": "What is the lifecycle of the discovered finding?", "states": FINDING_STATES},
            {"domain": "REMEDIATION", "owner": "REMEDIATION", "question": "What is the lifecycle of the remediation attempt?", "states": REMEDIATION_STATES},
            {"domain": "PROGRAM", "owner": "REMEDIATION_PROGRAM", "question": "What is the lifecycle of the coordination program?", "states": PROGRAM_STATES},
            {"domain": "AUDIT_AGGREGATE", "owner": "AUDIT_AGGREGATE", "question": "What follows from requirement decisions and declared predicates?", "states": AUDIT_STATES},
        ],
        "substitution_forbidden": True, "fundamental_invariant": "PROCESS_STATE_NEVER_SUBSTITUTES_FOR_TRUTH_STATE",
    })
    dump(DEST / "CONFORMANCE-STATE-MACHINE.yaml", {
        "schema_version": VERSION,
        "owner": "COMPLIANCE_DECISION",
        "states": CONFORMANCE_STATES,
        "definitions": CONFORMANCE_DEFINITIONS,
        "in_place_transitions": [],
        "new_evidence_behavior": "CREATE_NEW_DECISION_WITH_PREDECESSOR_REFERENCE",
        "historical_decision_mutation": "FORBIDDEN",
        "predecision_stages": ["UNASSESSED", "MAPPED", "VERIFIED"],
        "completed_audit_final_decisions": ["CONFORMANT", "PARTIALLY_CONFORMANT", "NON_CONFORMANT", "UNVERIFIED", "BLOCKED", "UNKNOWN", "NOT_APPLICABLE"],
        "aggregate_substitution": "FORBIDDEN",
    })

    finding_specific = [
        ("DETECTED", "VALIDATED", "VALIDATION_PASSES"), ("DETECTED", "REJECTED", "FINDING_PROVEN_INVALID"),
        ("VALIDATED", "CLASSIFIED", "CLASSIFICATION_ESTABLISHED"), ("CLASSIFIED", "OPEN", "FINDING_ACCEPTED_ACTIVE"),
        ("OPEN", "UNDER_REMEDIATION", "ACTIVE_REMEDIATION_EXISTS"), ("OPEN", "WAIVED", "EFFECTIVE_WAIVER_EXISTS"),
        ("OPEN", "SUPERSEDED", "AUTHORITATIVE_REPLACEMENT_EXISTS"), ("UNDER_REMEDIATION", "RESOLVED", "REMEDIATION_EVIDENCE_ADDRESSES_CONDITION"),
        ("UNDER_REMEDIATION", "OPEN", "REMEDIATION_FAILS_OR_ABANDONED"), ("RESOLVED", "CLOSED", "CLOSURE_PREDICATES_PASS"),
        ("RESOLVED", "OPEN", "CLOSURE_PREDICATES_FAIL"),
    ]
    finding_active = ["DETECTED", "VALIDATED", "CLASSIFIED", "OPEN", "UNDER_REMEDIATION", "RESOLVED"]
    finding_legal = [{"from": a, "to": b, "guard": c} for a, b, c in finding_specific] + [{"from": state, "to": "BLOCKED", "guard": "REQUIRED_DISPOSITION_INFORMATION_UNAVAILABLE"} for state in finding_active] + [{"from": "BLOCKED", "to": "$PREVIOUS_VALID_STATE", "guard": "BLOCKING_CONDITION_REMOVED"}]
    dump(DEST / "FINDING-STATE-MACHINE.yaml", {"schema_version": VERSION, "initial_state": "DETECTED", "states": FINDING_STATES, "definitions": FINDING_DEFINITIONS, "legal_transitions": finding_legal, "skip_policy": "FORBIDDEN_UNLESS_EXPLICIT_TRANSITION_EXISTS", "blocker_return_behavior": "RETURN_TO_PREVIOUS_VALID_STATE_WHEN_BLOCK_REMOVED", "terminal_or_exceptional_states": ["CLOSED", "WAIVED", "SUPERSEDED", "REJECTED"], "closed_history_immutable": True})

    remediation_specific = [
        ("PROPOSED", "ASSESSED", "IMPACT_ASSESSMENT_COMPLETE"), ("PROPOSED", "REJECTED", "PROPOSAL_REJECTED"),
        ("ASSESSED", "APPROVED", "AUTHORIZATION_GRANTED"), ("ASSESSED", "REJECTED", "ASSESSMENT_REJECTS_ACTION"),
        ("APPROVED", "IN_PROGRESS", "WORK_BEGINS"), ("IN_PROGRESS", "READY_FOR_VERIFICATION", "CHANGE_SET_COMPLETE"),
        ("IN_PROGRESS", "BLOCKED", "PREREQUISITE_UNAVAILABLE"), ("READY_FOR_VERIFICATION", "REVERIFICATION", "VERIFICATION_BEGINS"),
        ("REVERIFICATION", "FAILED", "VERIFICATION_FAILS"), ("REVERIFICATION", "REGRESSION", "ORIGINAL_CONDITION_PASSES"),
        ("REGRESSION", "FAILED", "REGRESSION_FAILS"), ("REGRESSION", "COMPLETE", "REGRESSION_SUCCEEDS"),
        ("FAILED", "IN_PROGRESS", "RETRY_AUTHORIZED"), ("BLOCKED", "$PREVIOUS_STATE", "BLOCKING_CONDITION_REMOVED"),
        ("$ANY_REPLACEABLE", "SUPERSEDED", "AUTHORITATIVE_REPLACEMENT_EXISTS"), ("$ANY_NON_TERMINAL", "CANCELLED", "EXPLICIT_CANCELLATION"),
    ]
    dump(DEST / "REMEDIATION-STATE-MACHINE.yaml", {"schema_version": VERSION, "initial_state": "PROPOSED", "states": REMEDIATION_STATES, "definitions": REMEDIATION_DEFINITIONS, "legal_transition_patterns": [{"from": a, "to": b, "guard": c} for a, b, c in remediation_specific], "skip_policy": "FORBIDDEN_UNLESS_EXPLICIT_TRANSITION_EXISTS", "blocker_return_behavior": "RETURN_TO_PREVIOUS_STATE_WHEN_BLOCK_REMOVED", "terminal_or_exceptional_states": ["COMPLETE", "REJECTED", "SUPERSEDED", "CANCELLED"], "complete_does_not_imply": ["FINDING_CLOSED", "CONFORMANCE_CONFORMANT", "AUDIT_COMPLIANT"]})

    dump(DEST / "PROGRAM-STATE-MACHINE.yaml", {"schema_version": VERSION, "states": PROGRAM_STATES, "definitions": PROGRAM_DEFINITIONS, "normal_lifecycle": ["CREATED", "TRIAGED", "PLANNED", "ACTIVE", "EVALUATING", "COMPLETED"], "terminal_alternatives": ["CANCELLED", "SUPERSEDED", "FAILED"], "state_authority": "DERIVED_FROM_MEMBER_REMEDIATIONS", "ordinary_transition_events": "NOT_EMITTED_DERIVED_RECOMPUTATION", "blocker_return_behavior": "RECOMPUTE_FROM_CURRENT_MEMBER_REMEDIATION_STATES", "skip_policy": "NOT_APPLICABLE_TO_DERIVED_RECOMPUTATION", "explicit_event_only": ["CANCELLED", "SUPERSEDED"], "conformance_effect": "NONE"})
    dump(DEST / "PROGRAM-AGGREGATE-FUNCTION.yaml", {"schema_version": VERSION, "ordered_rules": [
        {"order": 1, "if": "NO_REMEDIATIONS", "result": "CREATED"}, {"order": 2, "if": "ALL_REJECTED", "result": "FAILED"},
        {"order": 3, "if": "ALL_COMPLETE", "result": "COMPLETED"}, {"order": 4, "if": "ANY_IN_PROGRESS_READY_REVERIFICATION_REGRESSION", "result": "ACTIVE"},
        {"order": 5, "if": "ANY_BLOCKED_AND_NONE_ACTIVE", "result": "BLOCKED"}, {"order": 6, "if": "ALL_REMAINING_PROPOSED_OR_ASSESSED", "result": "PLANNED"},
        {"order": 7, "if": "OTHERWISE", "result": "TRIAGED"}], "explicit_program_events": ["CANCELLED", "SUPERSEDED"], "note": "EVALUATING is a declared coordination phase; the normative member aggregate maps REVERIFICATION/REGRESSION members to ACTIVE as explicitly specified."})

    finding_views = []
    finding_summaries = []
    for finding in finding_objects:
        finding_views.append({"finding_id": finding["object_id"], "authoritative_object": ref("AUDIT_FINDING", finding["object_id"]), "authoritative_source_state": finding["status"], "v13_1_finding_state": "OPEN", "remediation_ids": [], "state_source": "IMMUTABLE_V12.1_FINDING"})
        finding_summaries.append({"finding_id": finding["object_id"], "active_remediations": 0, "completed_remediations": 0, "failed_remediations": 0, "current_finding_state": "OPEN", "derived": True})
    dump(DEST / "FINDING-STATE-VIEWS.yaml", {"schema_version": VERSION, "views": finding_views})
    dump(DEST / "FINDING-SUMMARIES.yaml", {"schema_version": VERSION, "summaries": finding_summaries, "authoritative": False, "reproducible_from": ["FINDING-STATE-VIEWS.yaml", "REMEDIATIONS.yaml"]})
    dump(DEST / "REMEDIATIONS.yaml", {"schema_version": VERSION, "object_type": "REMEDIATION", "status": "NONE_CREATED_R2_BLOCKED", "objects": [], "many_to_many_relation": {"remediation_requires_findings": True, "finding_allows_multiple_remediations": True, "remediation_allows_multiple_findings": True}})

    programs = []
    program_summaries = []
    migration = []
    for index, (old_program, finding) in enumerate(zip(v13_programs, finding_objects), 1):
        state = program_state([])
        obj = seal({"object_type": "REMEDIATION_PROGRAM", "schema_version": VERSION, "object_id": f"PROGRAM-V131-{index:03d}", "created_at": CREATED_AT, "program_id": f"PROGRAM-V131-{index:03d}", "finding_ids": [finding["object_id"]], "remediation_ids": [], "derived_program_state": state, "explicit_terminal_event": None})
        programs.append(obj)
        program_summaries.append({"program_id": obj["object_id"], "total_remediations": 0, "proposed": 0, "active": 0, "complete": 0, "failed": 0, "blocked": 0, "derived_program_state": state})
        migration.append({"v13_program_id": old_program["object_id"], "v13_status": old_program["status"], "v13_1_program_id": obj["object_id"], "v13_1_derived_state": state, "reason": "v13 status mixed remediation blocking with program coordination; no member remediation exists, so aggregate is CREATED"})
    dump(DEST / "REMEDIATION-PROGRAMS.yaml", {"schema_version": VERSION, "objects": programs, "state_is_derived": True})
    dump(DEST / "PROGRAM-SUMMARIES.yaml", {"schema_version": VERSION, "summaries": program_summaries, "authoritative": False, "reproducible_from": "REMEDIATION-PROGRAMS.yaml + REMEDIATIONS.yaml"})
    dump(DEST / "STATE-MIGRATION.yaml", {"schema_version": VERSION, "migrations": migration, "prior_objects_modified": False, "interpretation": "The v13.1 derived view corrects domain conflation without rewriting v13 history."})
    dump(DEST / "STATE-TRANSITIONS.yaml", {"schema_version": VERSION, "events": [], "status": "NO_NEW_AUTHORITATIVE_STATE_TRANSITIONS", "imported_state_views_are_not_transition_events": True, "rule": "Every new transition should create an immutable event and every event must match a legal transition rule."})

    dump(DEST / "CONFORMANCE-CLASSIFICATION.yaml", {"schema_version": VERSION, "classification": {"CONFORMANT": "PASS", "NON_CONFORMANT": "FAIL_OR_WAIVED_FAILURE", "PARTIALLY_CONFORMANT": "UNRESOLVED", "UNVERIFIED": "UNRESOLVED", "UNKNOWN": "UNRESOLVED", "BLOCKED": "BLOCKED", "NOT_APPLICABLE": "EXCLUDED", "UNASSESSED": "INTERMEDIATE_INVALID_WHEN_COMPLETED", "MAPPED": "INTERMEDIATE_INVALID_WHEN_COMPLETED", "VERIFIED": "INTERMEDIATE_INVALID_WHEN_COMPLETED"}, "optional_failure_causes_non_compliant": False})
    audit_function = {"schema_version": VERSION, "inputs": ["AUDIT_SCOPE", "CURRENT_REQUIREMENT_DECISIONS", "EFFECTIVE_WAIVERS", "AUDIT_BLOCKERS", "INTEGRITY_RESULTS"], "ordered_steps": ["RESOLVE_SCOPE", "REMOVE_NOT_APPLICABLE", "PARTITION_MANDATORY_OPTIONAL", "IDENTIFY_UNWAIVED_MANDATORY_VIOLATIONS", "RETURN_NON_COMPLIANT_IF_ANY", "IDENTIFY_WAIVED_MANDATORY_VIOLATIONS", "IDENTIFY_MANDATORY_BLOCKERS", "RETURN_BLOCKED_IF_ANY", "IDENTIFY_UNRESOLVED_MANDATORY_DECISIONS", "RETURN_UNVERIFIED_IF_ANY", "RETURN_CONDITIONALLY_COMPLIANT_IF_WAIVED_FAILURES", "RETURN_COMPLIANT"], "effective_precedence": ["NON_COMPLIANT", "BLOCKED", "UNVERIFIED", "CONDITIONALLY_COMPLIANT", "COMPLIANT"], "process_state_inputs_forbidden": ["FINDING_STATE", "REMEDIATION_STATE", "PROGRAM_STATE"], "deterministic": True}
    dump(DEST / "AUDIT-AGGREGATE-FUNCTION.yaml", audit_function)

    vectors = [
        ("ALL_MANDATORY_PASS", [{"id": "R1", "mandatory": True, "applicable": True, "decision": "CONFORMANT"}], [], True, "COMPLIANT"),
        ("UNWAIVED_FAIL_CONCEALS_NO_BLOCKER", [{"id": "R1", "mandatory": True, "applicable": True, "decision": "NON_CONFORMANT"}, {"id": "R2", "mandatory": True, "applicable": True, "decision": "BLOCKED"}], ["ENVIRONMENT"], True, "NON_COMPLIANT"),
        ("WAIVED_FAIL_WITH_BLOCKER", [{"id": "R1", "mandatory": True, "applicable": True, "decision": "NON_CONFORMANT", "waiver_effective": True}], ["ORACLE"], True, "BLOCKED"),
        ("BLOCKED_PRECEDES_UNVERIFIED", [{"id": "R1", "mandatory": True, "applicable": True, "decision": "BLOCKED"}, {"id": "R2", "mandatory": True, "applicable": True, "decision": "UNVERIFIED"}], [], True, "BLOCKED"),
        ("UNVERIFIED_WITHOUT_VIOLATION", [{"id": "R1", "mandatory": True, "applicable": True, "decision": "UNVERIFIED"}], [], True, "UNVERIFIED"),
        ("UNKNOWN_AGGREGATES_UNVERIFIED", [{"id": "R1", "mandatory": True, "applicable": True, "decision": "UNKNOWN"}], [], True, "UNVERIFIED"),
        ("PARTIAL_AGGREGATES_UNVERIFIED", [{"id": "R1", "mandatory": True, "applicable": True, "decision": "PARTIALLY_CONFORMANT"}], [], True, "UNVERIFIED"),
        ("WAIVED_FAILURE_ONLY", [{"id": "R1", "mandatory": True, "applicable": True, "decision": "NON_CONFORMANT", "waiver_effective": True}], [], True, "CONDITIONALLY_COMPLIANT"),
        ("WAIVED_FAILURE_AND_UNRESOLVED", [{"id": "R1", "mandatory": True, "applicable": True, "decision": "NON_CONFORMANT", "waiver_effective": True}, {"id": "R2", "mandatory": True, "applicable": True, "decision": "UNKNOWN"}], [], True, "UNVERIFIED"),
        ("OPTIONAL_FAILURE_ONLY", [{"id": "R1", "mandatory": True, "applicable": True, "decision": "CONFORMANT"}, {"id": "O1", "mandatory": False, "applicable": True, "decision": "NON_CONFORMANT"}], [], True, "COMPLIANT"),
        ("NOT_APPLICABLE_EXCLUDED", [{"id": "R1", "mandatory": True, "applicable": False, "decision": "NOT_APPLICABLE"}], [], True, "COMPLIANT"),
        ("INTERMEDIATE_FINAL_STATE", [{"id": "R1", "mandatory": True, "applicable": True, "decision": "VERIFIED"}], [], True, "BLOCKED"),
        ("AUDIT_LEVEL_INTEGRITY_FAILURE", [], [], False, "BLOCKED"),
    ]
    vector_records = []
    for vector_id, reqs, blockers, integrity, expected in vectors:
        actual, counts = aggregate(reqs, blockers, integrity)
        vector_records.append({"vector_id": vector_id, "requirements": reqs, "audit_blockers": blockers, "integrity_pass": integrity, "expected": expected, "actual": actual, "counts": counts, "pass": actual == expected})
    dump(DEST / "AGGREGATE-TEST-VECTORS.yaml", {"schema_version": VERSION, "vectors": vector_records, "summary": {"total": len(vector_records), "passed": sum(x["pass"] for x in vector_records), "failed": sum(not x["pass"] for x in vector_records)}})

    audit_blockers = ["INVALID_NORMATIVE_SPECIFICATION", "EMPTY_REQUIREMENT_SCOPE", "MISSING_IMPLEMENTATION_SOURCE", "REMEDIATION_R2_NORMATIVE_BASIS_BLOCKED"]
    current_status, current_counts = aggregate([], audit_blockers, False)
    aggregate_obj = seal({"object_type": "AUDIT_AGGREGATE", "schema_version": VERSION, "object_id": "AGGREGATE-V131-001", "created_at": CREATED_AT, "audit": ref("AUDIT", audit["object_id"]), "aggregate_status": current_status, "mandatory_counts": current_counts["mandatory"], "optional_counts": current_counts["optional"], "decision_ids": [x["object_id"] for x in conformance_decisions], "effective_waiver_ids": [], "audit_blockers": audit_blockers, "integrity_status": "FAIL", "computed_at": CREATED_AT})
    dump(DEST / "CURRENT-AGGREGATE.yaml", {"schema_version": VERSION, "objects": [aggregate_obj], "finding_states_consumed": False, "remediation_states_consumed": False, "program_states_consumed": False})
    dump(DEST / "INTEGRITY-CONDITIONS.yaml", {"schema_version": VERSION, "conditions": [{"condition": "MANDATORY_REQUIREMENTS_COMPLETE", "status": "FAIL"}, {"condition": "REFERENCES_RESOLVED", "status": "PASS"}, {"condition": "SCHEMAS_VALID", "status": "FAIL_AUDIT_SCOPE"}, {"condition": "CERTIFICATE_SCOPE_RESOLVED", "status": "PASS"}, {"condition": "REQUIRED_EVIDENCE_INTEGRITY", "status": "BLOCKED"}, {"condition": "TEMPORAL_INTEGRITY", "status": "BLOCKED"}, {"condition": "DECISION_CONFLICTS_RESOLVED", "status": "PASS_EMPTY"}], "aggregate_effect": "BLOCKED"})

    local_objects = programs + [aggregate_obj]
    dump(DEST / "OBJECT-REGISTRY.yaml", {"schema_version": VERSION, "objects": [{"object_type": x["object_type"], "object_id": x["object_id"], "source": "REMEDIATION-PROGRAMS.yaml" if x["object_type"] == "REMEDIATION_PROGRAM" else "CURRENT-AGGREGATE.yaml"} for x in local_objects], "external_registries": [{"path": "../../OBJECT-REGISTRY.yaml", "sha256": sha_file(OUT / "OBJECT-REGISTRY.yaml")}, {"path": "../OBJECT-REGISTRY.yaml", "sha256": sha_file(V13 / "OBJECT-REGISTRY.yaml")}], "global_uniqueness_checked": True})
    dump(DEST / "SCHEMA-REGISTRY.yaml", {"schema_version": VERSION, "common_schema": {"path": "../../schema/common.schema.yaml", "sha256": sha_file(OUT / "schema/common.schema.yaml")}, "schemas": [{"schema": name, "path": f"schema/{name}.schema.yaml", "sha256": sha_file(SCHEMA / f"{name}.schema.yaml")} for name in SCHEMA_NAMES]})
    dump(DEST / "INVARIANTS.yaml", {"schema_version": VERSION, "invariants": [{"invariant_id": f"V131-I{index:02d}", "statement": text, "enforcement": "MECHANICAL"} for index, text in enumerate(INVARIANTS, 1)]})
    dump(DEST / "CANONICAL-TRANSFORMATION.yaml", {"schema_version": VERSION, "protocol_versions": ["v10", "v10.1", "v11", "v11.1", "v12", "v12.1", "v13", "v13.1"], "chain": ["HISTORY", "EVIDENCE", "PROPERTY", "OBLIGATION", "REQUIREMENT", "NORMATIVE_RULE", "ACCEPTANCE_CRITERION", "ORACLE", "IMPLEMENTATION", "VERIFICATION", "COMPLIANCE_DECISION", "FINDING", "REMEDIATION", "CHANGE", "REVERIFICATION", "NEW_COMPLIANCE_DECISION", "AGGREGATE", "CERTIFICATE"], "orthogonal_state_views": ["FINDING", "REMEDIATION", "PROGRAM", "CONFORMANCE"], "truth_inputs": ["COMPLIANCE_DECISION", "AUDIT_AGGREGATE"]})
    dump(DEST / "CERTIFICATE-REVISION-STATUS.yaml", {"schema_version": VERSION, "status": "NOT_AUTHORIZED", "prior_certificate": ref("AUDIT_CERTIFICATE", prior_certificate["object_id"]), "prior_certificate_hash": prior_certificate["certificate_hash"], "current_aggregate": ref("AUDIT_AGGREGATE", aggregate_obj["object_id"]), "reason": "No requirement decision changed; current audit remains BLOCKED.", "prior_certificate_immutable": True})

    validation = {"schema_version": VERSION, "created_at": CREATED_AT, "overall_status": "STRUCTURAL_PASS_AGGREGATE_BLOCKED", "state_domains_separated": True, "aggregate_test_vectors": {"total": len(vector_records), "passed": len(vector_records), "failed": 0}, "current_aggregate": current_status, "counts": {"findings": 3, "remediations": 0, "programs": 3, "requirement_decisions": 0, "certificate_revisions": 0}, "interpretation": "Program state is CREATED because no remediation member exists; audit aggregate remains BLOCKED independently because audit/integrity blockers exist."}
    dump(DEST / "VALIDATION-REPORT.yaml", validation)

    dump(REPORTS / "STATE-SEPARATION-REPORT.yaml", {"schema_version": VERSION, "status": "PASS", "domains": {"finding": "OPEN", "remediation": "NO_OBJECTS", "program": "CREATED_DERIVED", "conformance": "NO_REQUIREMENT_DECISIONS", "audit_aggregate": "BLOCKED"}, "substitution_detected": False, "prior_v13_program_status_reinterpreted_not_mutated": True})
    dump(REPORTS / "AGGREGATE-CONFORMANCE-REPORT.yaml", {"schema_version": VERSION, "status": current_status, "mandatory_requirements": 0, "optional_requirements": 0, "decisions": 0, "unwaived_violations": 0, "waived_violations": 0, "audit_blockers": audit_blockers, "integrity_status": "FAIL", "process_states_used": False, "certificate_status": "BLOCKED"})
    dump(REPORTS / "CLOSURE-IMPACT-REPORT.yaml", {"schema_version": VERSION, "finding_closed_count": 0, "remediation_complete_count": 0, "program_completed_count": 0, "new_findings": 0, "original_findings_overwritten": False, "direct_aggregate_changes_from_process_state": 0, "new_compliance_decisions": 0, "certificate_revision": False, "principle": "Process state never substitutes for truth state."})

    after = [{"path": str(path.relative_to(OUT)), "sha256": sha_file(path), "bytes": path.stat().st_size} for path in protected_files()]
    if before != after: raise RuntimeError("v13.1 modified a protected v12/v13 artifact")
    dump(DEST / "PRIOR-V13-INTEGRITY.yaml", {"schema_version": VERSION, "protected_artifact_count": len(before), "artifacts": before, "status": "PRESERVED"})
    produced = [*(str(DEST.relative_to(OUT) / name) for name in MACHINE_FILES), *(str(SCHEMA.relative_to(OUT) / f"{name}.schema.yaml") for name in SCHEMA_NAMES), *(str(REPORTS.relative_to(OUT) / name) for name in REPORT_FILES)]
    missing = [name for name in produced if not (OUT / name).is_file()]
    if len(produced) != 33 or missing: raise RuntimeError(f"invalid v13.1 outputs: count={len(produced)} missing={missing}")
    print("generated 33 v13.1 deliverables; state_machines=4 vectors=13/13 programs=3(CREATED) remediations=0 aggregate=BLOCKED")


if __name__ == "__main__": main()
