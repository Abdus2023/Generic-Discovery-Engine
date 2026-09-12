#!/usr/bin/env python3
"""Independent validator for Protocol-v13.1 state separation and aggregation."""
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
V13 = OUT / "remediation"
DEST = V13 / "v13.1"
SCHEMA = DEST / "schema"
REPORTS = DEST / "reports"
VERSION = "13.1"
SCHEMA_NAMES = ["audit-finding", "remediation", "remediation-program", "state-transition", "audit-aggregate"]
SCHEMA_BY_TYPE = {"AUDIT_FINDING": "audit-finding", "REMEDIATION": "remediation", "REMEDIATION_PROGRAM": "remediation-program", "STATE_TRANSITION": "state-transition", "AUDIT_AGGREGATE": "audit-aggregate"}
MACHINE_FILES = ["STATE-DOMAINS.yaml", "CONFORMANCE-STATE-MACHINE.yaml", "FINDING-STATE-MACHINE.yaml", "REMEDIATION-STATE-MACHINE.yaml", "PROGRAM-STATE-MACHINE.yaml", "PROGRAM-AGGREGATE-FUNCTION.yaml", "AUDIT-AGGREGATE-FUNCTION.yaml", "AGGREGATE-TEST-VECTORS.yaml", "FINDING-STATE-VIEWS.yaml", "REMEDIATIONS.yaml", "REMEDIATION-PROGRAMS.yaml", "PROGRAM-SUMMARIES.yaml", "FINDING-SUMMARIES.yaml", "STATE-TRANSITIONS.yaml", "CURRENT-AGGREGATE.yaml", "INTEGRITY-CONDITIONS.yaml", "CONFORMANCE-CLASSIFICATION.yaml", "VALIDATION-REPORT.yaml", "PRIOR-V13-INTEGRITY.yaml", "OBJECT-REGISTRY.yaml", "SCHEMA-REGISTRY.yaml", "INVARIANTS.yaml", "CANONICAL-TRANSFORMATION.yaml", "CERTIFICATE-REVISION-STATUS.yaml", "STATE-MIGRATION.yaml"]
REPORT_FILES = ["STATE-SEPARATION-REPORT.yaml", "AGGREGATE-CONFORMANCE-REPORT.yaml", "CLOSURE-IMPACT-REPORT.yaml"]
DELIVERABLES = [*MACHINE_FILES, *(f"schema/{name}.schema.yaml" for name in SCHEMA_NAMES), *(f"reports/{name}" for name in REPORT_FILES)]
FINDING_STATES = {"DETECTED", "VALIDATED", "CLASSIFIED", "OPEN", "UNDER_REMEDIATION", "RESOLVED", "CLOSED", "WAIVED", "SUPERSEDED", "REJECTED", "BLOCKED"}
REMEDIATION_STATES = {"PROPOSED", "ASSESSED", "APPROVED", "IN_PROGRESS", "READY_FOR_VERIFICATION", "REVERIFICATION", "FAILED", "REGRESSION", "COMPLETE", "BLOCKED", "REJECTED", "SUPERSEDED", "CANCELLED"}
PROGRAM_STATES = {"CREATED", "TRIAGED", "PLANNED", "ACTIVE", "BLOCKED", "EVALUATING", "COMPLETED", "CANCELLED", "SUPERSEDED", "FAILED"}
CONFORMANCE_STATES = {"UNASSESSED", "MAPPED", "VERIFIED", "CONFORMANT", "PARTIALLY_CONFORMANT", "NON_CONFORMANT", "UNVERIFIED", "BLOCKED", "UNKNOWN", "NOT_APPLICABLE"}
AUDIT_STATES = {"NON_COMPLIANT", "CONDITIONALLY_COMPLIANT", "BLOCKED", "UNVERIFIED", "COMPLIANT"}
ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]*$")


def load(path: Path) -> Any: return json.loads(path.read_text(encoding="utf-8"))
def sha_file(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()
def canonical(value: Any) -> bytes: return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()

def valid_timestamp(value: Any) -> bool:
    if not isinstance(value, str) or not (value.endswith("Z") or re.search(r"[+-]\d{2}:\d{2}$", value)): return False
    try: return datetime.fromisoformat(value.replace("Z", "+00:00")).tzinfo is not None
    except ValueError: return False


def resolve_pointer(value: Any, pointer: str) -> Any:
    node = value
    for part in pointer.lstrip("/").split("/") if pointer else []:
        key = part.replace("~1", "/").replace("~0", "~"); node = node[int(key)] if isinstance(node, list) else node[key]
    return node


def schema_errors(value: Any, schema: dict[str, Any], schemas: dict[str, Any], current: str, path: str = "$") -> list[str]:
    errors: list[str] = []
    if "$ref" in schema:
        file_part, _, pointer = schema["$ref"].partition("#"); target = Path(file_part).name.replace(".schema.yaml", "") if file_part else current
        try: resolved = resolve_pointer(schemas[target], pointer)
        except (KeyError, IndexError, TypeError, ValueError): return [f"{path}: unresolved ref"]
        return schema_errors(value, resolved, schemas, target, path)
    if "oneOf" in schema:
        results = [schema_errors(value, item, schemas, current, path) for item in schema["oneOf"]]
        return [] if sum(not item for item in results) == 1 else [f"{path}: oneOf"]
    expected = schema.get("type")
    if expected is not None:
        kinds = expected if isinstance(expected, list) else [expected]
        tests = {"object": lambda: isinstance(value, dict), "array": lambda: isinstance(value, list), "string": lambda: isinstance(value, str), "integer": lambda: isinstance(value, int) and not isinstance(value, bool), "boolean": lambda: isinstance(value, bool), "null": lambda: value is None}
        if not any(tests.get(kind, lambda: False)() for kind in kinds): return [f"{path}: type"]
    if "const" in schema and value != schema["const"]: errors.append(f"{path}: const")
    if "enum" in schema and value not in schema["enum"]: errors.append(f"{path}: enum")
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0): errors.append(f"{path}: minLength")
        if "maxLength" in schema and len(value) > schema["maxLength"]: errors.append(f"{path}: maxLength")
        if "pattern" in schema and re.fullmatch(schema["pattern"], value) is None: errors.append(f"{path}: pattern")
        if schema.get("format") == "date-time" and not valid_timestamp(value): errors.append(f"{path}: timestamp")
    if isinstance(value, (int, float)) and not isinstance(value, bool) and value < schema.get("minimum", value): errors.append(f"{path}: minimum")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0): errors.append(f"{path}: minItems")
        if schema.get("uniqueItems") and len({canonical(item) for item in value}) != len(value): errors.append(f"{path}: unique")
        if "items" in schema:
            for index, item in enumerate(value): errors.extend(schema_errors(item, schema["items"], schemas, current, f"{path}[{index}]"))
    if isinstance(value, dict):
        props = schema.get("properties", {})
        for field in schema.get("required", []):
            if field not in value: errors.append(f"{path}: missing {field}")
        if schema.get("additionalProperties") is False:
            for field in value:
                if field not in props: errors.append(f"{path}: additional {field}")
        for field, item in value.items():
            if field in props: errors.extend(schema_errors(item, props[field], schemas, current, f"{path}.{field}"))
    return errors


def extract_refs(value: Any) -> list[str]:
    refs: list[str] = []
    if isinstance(value, dict):
        if "$ref" in value: refs.append(value["$ref"])
        for item in value.values(): refs.extend(extract_refs(item))
    elif isinstance(value, list):
        for item in value: refs.extend(extract_refs(item))
    return refs


def classify(decision: str, waived: bool) -> str:
    if decision == "CONFORMANT": return "pass"
    if decision == "NON_CONFORMANT": return "waived_failure" if waived else "fail"
    if decision in {"PARTIALLY_CONFORMANT", "UNVERIFIED", "UNKNOWN"}: return "unresolved"
    if decision == "BLOCKED": return "blocked"
    if decision == "NOT_APPLICABLE": return "excluded"
    if decision in {"UNASSESSED", "MAPPED", "VERIFIED"}: return "intermediate"
    raise ValueError(decision)


def aggregate(requirements: list[dict[str, Any]], blockers: list[str], integrity: bool, completed: bool = True) -> tuple[str, dict[str, dict[str, int]]]:
    keys = ["pass", "fail", "waived_failure", "unresolved", "blocked", "excluded", "intermediate"]
    counts = {kind: {key: 0 for key in keys} for kind in ["mandatory", "optional"]}; applicable = []
    for item in requirements:
        kind = "mandatory" if item["mandatory"] else "optional"; decision = item["decision"]
        category = "excluded" if not item["applicable"] or decision == "NOT_APPLICABLE" else classify(decision, item.get("waiver_effective", False)); counts[kind][category] += 1
        if category != "excluded": applicable.append(item)
    mandatory = [item for item in applicable if item["mandatory"]]
    if any(x["decision"] == "NON_CONFORMANT" and not x.get("waiver_effective", False) for x in mandatory): return "NON_COMPLIANT", counts
    if blockers or not integrity or (completed and any(x["decision"] in {"UNASSESSED", "MAPPED", "VERIFIED"} for x in mandatory)) or any(x["decision"] == "BLOCKED" for x in mandatory): return "BLOCKED", counts
    if any(x["decision"] in {"PARTIALLY_CONFORMANT", "UNVERIFIED", "UNKNOWN"} for x in mandatory): return "UNVERIFIED", counts
    if any(x["decision"] == "NON_CONFORMANT" and x.get("waiver_effective", False) for x in mandatory): return "CONDITIONALLY_COMPLIANT", counts
    return "COMPLIANT", counts


def program_state(states: list[str], event: str | None = None) -> str:
    if event in {"CANCELLED", "SUPERSEDED"}: return event
    if not states: return "CREATED"
    if all(x == "REJECTED" for x in states): return "FAILED"
    if all(x == "COMPLETE" for x in states): return "COMPLETED"
    active = {"IN_PROGRESS", "READY_FOR_VERIFICATION", "REVERIFICATION", "REGRESSION"}
    if any(x in active for x in states): return "ACTIVE"
    if any(x == "BLOCKED" for x in states) and not any(x in active for x in states): return "BLOCKED"
    if all(x in {"PROPOSED", "ASSESSED"} for x in states): return "PLANNED"
    return "TRIAGED"


def main() -> int:
    checks: list[dict[str, str]] = []
    def check(cid: str, category: str, description: str, ok: bool, detail: str = "") -> None: checks.append({"check_id": cid, "category": category, "description": description, "result": "PASS" if ok else "FAIL", "detail": detail})
    def blocked(cid: str, category: str, description: str, detail: str) -> None: checks.append({"check_id": cid, "category": category, "description": description, "result": "BLOCKED", "detail": detail})

    for index, name in enumerate(DELIVERABLES, 1): check(f"A{index:02d}", "artifacts", f"v13.1 artifact exists: {name}", (DEST / name).is_file())
    if any(x["result"] == "FAIL" for x in checks): return finish(checks, {})
    check("A34", "artifacts", "generator-owned v13.1 set has exactly 33 unique files", len(DELIVERABLES) == len(set(DELIVERABLES)) == 33)
    check("A35", "artifacts", "all machine/schema/report files are JSON-compatible YAML", all(parseable(DEST / name) for name in DELIVERABLES))

    schemas = {name: load(SCHEMA / f"{name}.schema.yaml") for name in SCHEMA_NAMES}; schemas["common"] = load(OUT / "schema/common.schema.yaml")
    check("S01", "schemas", "five v13.1 schemas explicitly cover all new/updated state objects", set(schemas) == set(SCHEMA_NAMES) | {"common"} and set(SCHEMA_BY_TYPE) == {"AUDIT_FINDING", "REMEDIATION", "REMEDIATION_PROGRAM", "STATE_TRANSITION", "AUDIT_AGGREGATE"})
    common_fields = {"object_type", "schema_version", "object_id", "created_at", "content_hash"}
    check("S02", "schemas", "every v13.1 object schema requires common identity and content hash", all(common_fields <= set(schemas[name]["required"]) for name in SCHEMA_NAMES))
    check("S03", "schemas", "every required schema field is declared and extras forbidden", all(set(schemas[name]["required"]) <= set(schemas[name]["properties"]) and schemas[name]["additionalProperties"] is False for name in SCHEMA_NAMES))
    unresolved_schema_refs = []
    for current in SCHEMA_NAMES:
        for reference in extract_refs(schemas[current]):
            target_name = "common" if Path(reference.partition("#")[0]).name == "common.schema.yaml" else Path(reference.partition("#")[0]).name.replace(".schema.yaml", "")
            try: resolve_pointer(schemas[target_name], reference.partition("#")[2])
            except Exception: unresolved_schema_refs.append((current, reference))
    check("S04", "schemas", "every schema reference resolves", not unresolved_schema_refs, str(unresolved_schema_refs))
    check("S05", "schemas", "finding, remediation, and program state enums are disjointly owned", set(schemas["audit-finding"]["properties"]["finding_state"]["enum"]) == FINDING_STATES and set(schemas["remediation"]["properties"]["remediation_state"]["enum"]) == REMEDIATION_STATES and set(schemas["remediation-program"]["properties"]["derived_program_state"]["enum"]) == PROGRAM_STATES)
    check("S06", "schemas", "many-to-many remediation schema requires at least one finding", schemas["remediation"]["properties"]["finding_ids"]["minItems"] == 1 and "program_ids" in schemas["remediation"]["properties"])
    check("S07", "schemas", "audit aggregate schema accepts only audit-level vocabulary", set(schemas["audit-aggregate"]["properties"]["aggregate_status"]["enum"]) == AUDIT_STATES)
    registry = load(DEST / "SCHEMA-REGISTRY.yaml")
    check("S08", "schemas", "schema registry hashes five local schemas and prior common schema", len(registry["schemas"]) == 5 and all(sha_file(DEST / item["path"]) == item["sha256"] for item in registry["schemas"]) and sha_file(DEST / registry["common_schema"]["path"]) == registry["common_schema"]["sha256"])
    transition_vocab = FINDING_STATES | REMEDIATION_STATES | PROGRAM_STATES | CONFORMANCE_STATES
    check("S09", "schemas", "transition endpoints are restricted to the declared state vocabularies", set(schemas["state-transition"]["properties"]["from_state"]["enum"]) == transition_vocab and set(schemas["state-transition"]["properties"]["to_state"]["enum"]) == transition_vocab)
    finding_close_rule = schemas["audit-finding"]["allOf"][0]
    remediation_complete_rule = schemas["remediation"]["allOf"][0]
    check("S10", "schemas", "CLOSED/COMPLETE objects and transitions require verification evidence", finding_close_rule["if"]["properties"]["finding_state"]["const"] == "CLOSED" and finding_close_rule["then"]["properties"]["closure_verification_ids"]["minItems"] == 1 and remediation_complete_rule["if"]["properties"]["remediation_state"]["const"] == "COMPLETE" and all(remediation_complete_rule["then"]["properties"][field]["minItems"] == 1 for field in ["reverification_execution_ids", "regression_execution_ids"]) and schemas["state-transition"]["properties"]["evidence"]["minItems"] == 1)

    programs = load(DEST / "REMEDIATION-PROGRAMS.yaml")["objects"]; remediations = load(DEST / "REMEDIATIONS.yaml")["objects"]; aggregate_obj = load(DEST / "CURRENT-AGGREGATE.yaml")["objects"][0]
    objects = programs + remediations + [aggregate_obj]; object_errors = {x["object_id"]: schema_errors(x, schemas[SCHEMA_BY_TYPE[x["object_type"]]], schemas, SCHEMA_BY_TYPE[x["object_type"]]) for x in objects}
    check("O01", "objects", "all instantiated v13.1 objects validate", not any(object_errors.values()), str({k: v for k, v in object_errors.items() if v}))
    ids = [x["object_id"] for x in objects]
    check("O02", "objects", "all local identities are unique and syntactically valid", len(ids) == len(set(ids)) and all(ID_PATTERN.fullmatch(x) and len(x) <= 256 for x in ids))
    check("O03", "objects", "all objects use explicit timezone timestamps", all(valid_timestamp(x["created_at"]) for x in objects) and valid_timestamp(aggregate_obj["computed_at"]))
    external_ids = {x["object_id"] for x in load(OUT / "OBJECT-REGISTRY.yaml")["objects"]} | {x["object_id"] for x in load(V13 / "OBJECT-REGISTRY.yaml")["objects"]}
    check("O04", "objects", "v13.1 object IDs are globally unique against v12/v13", not (set(ids) & external_ids))
    local_registry = load(DEST / "OBJECT-REGISTRY.yaml")
    check("O05", "objects", "object registry contains all and only local objects", {(x["object_type"], x["object_id"]) for x in local_registry["objects"]} == {(x["object_type"], x["object_id"]) for x in objects})
    check("O06", "objects", "both external registries resolve with exact hashes", all((DEST / x["path"]).is_file() and sha_file(DEST / x["path"]) == x["sha256"] for x in local_registry["external_registries"]))
    content_hashes_valid = True
    for obj in objects:
        payload = dict(obj); expected_hash = payload.pop("content_hash", None)
        content_hashes_valid &= expected_hash == {"algorithm": "SHA-256", "value": hashlib.sha256(canonical(payload)).hexdigest()}
    check("O07", "objects", "mandatory content hashes match canonical serialization excluding themselves", content_hashes_valid)
    root_registry_objects = load(OUT / "OBJECT-REGISTRY.yaml")["objects"]
    root_by_id = {item["object_id"]: [entry for entry in root_registry_objects if entry["object_id"] == item["object_id"]] for item in root_registry_objects}
    program_finding_ids = [finding_id for program in programs for finding_id in program["finding_ids"]]
    check("O08", "references", "every program finding ID resolves exactly once with AUDIT_FINDING type", all(len(root_by_id.get(fid, [])) == 1 and root_by_id[fid][0]["object_type"] == "AUDIT_FINDING" for fid in program_finding_ids))
    audit_ref = aggregate_obj["audit"]
    check("O09", "references", "aggregate audit reference resolves exactly once with matching type", len(root_by_id.get(audit_ref["object_id"], [])) == 1 and root_by_id[audit_ref["object_id"]][0]["object_type"] == audit_ref["object_type"] == "AUDIT")

    domains = {x["domain"]: x for x in load(DEST / "STATE-DOMAINS.yaml")["domains"]}
    check("D01", "domains", "five state domains have exclusive authoritative owners", {k: v["owner"] for k, v in domains.items()} == {"CONFORMANCE": "COMPLIANCE_DECISION", "FINDING": "AUDIT_FINDING", "REMEDIATION": "REMEDIATION", "PROGRAM": "REMEDIATION_PROGRAM", "AUDIT_AGGREGATE": "AUDIT_AGGREGATE"})
    check("D02", "domains", "domain vocabularies are exact", set(domains["CONFORMANCE"]["states"]) == CONFORMANCE_STATES and set(domains["FINDING"]["states"]) == FINDING_STATES and set(domains["REMEDIATION"]["states"]) == REMEDIATION_STATES and set(domains["PROGRAM"]["states"]) == PROGRAM_STATES and set(domains["AUDIT_AGGREGATE"]["states"]) == AUDIT_STATES)
    check("D03", "domains", "state substitution is categorically forbidden", load(DEST / "STATE-DOMAINS.yaml")["substitution_forbidden"] is True and load(DEST / "STATE-DOMAINS.yaml")["fundamental_invariant"] == "PROCESS_STATE_NEVER_SUBSTITUTES_FOR_TRUTH_STATE")
    conformance_machine = load(DEST / "CONFORMANCE-STATE-MACHINE.yaml")
    check("D04", "conformance-state", "conformance decisions are defined, immutable, and new evidence creates a new decision", set(conformance_machine["states"]) == CONFORMANCE_STATES and set(conformance_machine["definitions"]) == CONFORMANCE_STATES and all(conformance_machine["definitions"].values()) and conformance_machine["in_place_transitions"] == [] and conformance_machine["historical_decision_mutation"] == "FORBIDDEN" and conformance_machine["new_evidence_behavior"] == "CREATE_NEW_DECISION_WITH_PREDECESSOR_REFERENCE")
    check("D05", "conformance-state", "intermediate states are excluded from completed-audit finals", set(conformance_machine["predecision_stages"]) == {"UNASSESSED", "MAPPED", "VERIFIED"} and not set(conformance_machine["predecision_stages"]) & set(conformance_machine["completed_audit_final_decisions"]) and conformance_machine["aggregate_substitution"] == "FORBIDDEN")

    finding_machine = load(DEST / "FINDING-STATE-MACHINE.yaml"); finding_pairs = {(x["from"], x["to"]) for x in finding_machine["legal_transitions"]}
    finding_core = {("DETECTED", "VALIDATED"), ("DETECTED", "REJECTED"), ("VALIDATED", "CLASSIFIED"), ("CLASSIFIED", "OPEN"), ("OPEN", "UNDER_REMEDIATION"), ("OPEN", "WAIVED"), ("OPEN", "SUPERSEDED"), ("UNDER_REMEDIATION", "RESOLVED"), ("UNDER_REMEDIATION", "OPEN"), ("RESOLVED", "CLOSED"), ("RESOLVED", "OPEN")}
    check("F01", "finding-state", "all eleven specific finding transitions are exact", finding_core <= finding_pairs)
    check("F02", "finding-state", "all six active finding states can block and resume previous", all((state, "BLOCKED") in finding_pairs for state in ["DETECTED", "VALIDATED", "CLASSIFIED", "OPEN", "UNDER_REMEDIATION", "RESOLVED"]) and ("BLOCKED", "$PREVIOUS_VALID_STATE") in finding_pairs and len(finding_pairs) == 18)
    check("F03", "finding-state", "all finding states are defined; skipping and historical erasure are forbidden", set(finding_machine["definitions"]) == FINDING_STATES and all(finding_machine["definitions"].values()) and finding_machine["skip_policy"] == "FORBIDDEN_UNLESS_EXPLICIT_TRANSITION_EXISTS" and finding_machine["blocker_return_behavior"] == "RETURN_TO_PREVIOUS_VALID_STATE_WHEN_BLOCK_REMOVED" and finding_machine["closed_history_immutable"] is True)
    views = load(DEST / "FINDING-STATE-VIEWS.yaml")["views"]; source_findings = load(OUT / "FINDINGS.yaml")["objects"]
    check("F04", "finding-state", "three immutable source findings map to independent OPEN views", len(views) == len(source_findings) == 3 and {x["finding_id"] for x in views} == {x["object_id"] for x in source_findings} and all(x["v13_1_finding_state"] == "OPEN" and x["remediation_ids"] == [] for x in views))
    finding_summaries = load(DEST / "FINDING-SUMMARIES.yaml")
    check("F05", "derived", "finding summaries are non-authoritative and reproducible", finding_summaries["authoritative"] is False and all(x["active_remediations"] == x["completed_remediations"] == x["failed_remediations"] == 0 for x in finding_summaries["summaries"]))
    check("F06", "evidence", "every authoritative finding retains evidence and each state view has a matching typed reference", all(x.get("evidence") for x in source_findings) and all(x["authoritative_object"] == {"object_type": "AUDIT_FINDING", "object_id": x["finding_id"]} for x in views))

    remediation_machine = load(DEST / "REMEDIATION-STATE-MACHINE.yaml"); remediation_patterns = {(x["from"], x["to"]) for x in remediation_machine["legal_transition_patterns"]}
    required_patterns = {("PROPOSED", "ASSESSED"), ("PROPOSED", "REJECTED"), ("ASSESSED", "APPROVED"), ("ASSESSED", "REJECTED"), ("APPROVED", "IN_PROGRESS"), ("IN_PROGRESS", "READY_FOR_VERIFICATION"), ("IN_PROGRESS", "BLOCKED"), ("READY_FOR_VERIFICATION", "REVERIFICATION"), ("REVERIFICATION", "FAILED"), ("REVERIFICATION", "REGRESSION"), ("REGRESSION", "FAILED"), ("REGRESSION", "COMPLETE"), ("FAILED", "IN_PROGRESS"), ("BLOCKED", "$PREVIOUS_STATE"), ("$ANY_REPLACEABLE", "SUPERSEDED"), ("$ANY_NON_TERMINAL", "CANCELLED")}
    check("M01", "remediation-state", "all sixteen remediation transition patterns are exact", remediation_patterns == required_patterns and len(remediation_machine["legal_transition_patterns"]) == 16)
    check("M02", "remediation-state", "all remediation states are defined and COMPLETE has no direct truth effect", set(remediation_machine["definitions"]) == REMEDIATION_STATES and all(remediation_machine["definitions"].values()) and remediation_machine["skip_policy"] == "FORBIDDEN_UNLESS_EXPLICIT_TRANSITION_EXISTS" and remediation_machine["blocker_return_behavior"] == "RETURN_TO_PREVIOUS_STATE_WHEN_BLOCK_REMOVED" and set(remediation_machine["complete_does_not_imply"]) == {"FINDING_CLOSED", "CONFORMANCE_CONFORMANT", "AUDIT_COMPLIANT"})
    check("M03", "remediation-state", "no remediation object is fabricated past v13 R2 blocker", remediations == [] and load(DEST / "REMEDIATIONS.yaml")["status"] == "NONE_CREATED_R2_BLOCKED")
    relation = load(DEST / "REMEDIATIONS.yaml")["many_to_many_relation"]
    check("M04", "relationships", "many-to-many finding/remediation relation is explicit", relation == {"remediation_requires_findings": True, "finding_allows_multiple_remediations": True, "remediation_allows_multiple_findings": True})

    program_machine = load(DEST / "PROGRAM-STATE-MACHINE.yaml"); program_rules = load(DEST / "PROGRAM-AGGREGATE-FUNCTION.yaml")["ordered_rules"]
    check("P01", "program-state", "program definitions, lifecycle, and explicit-event alternatives are exact", set(program_machine["states"]) == PROGRAM_STATES and set(program_machine["definitions"]) == PROGRAM_STATES and all(program_machine["definitions"].values()) and program_machine["normal_lifecycle"] == ["CREATED", "TRIAGED", "PLANNED", "ACTIVE", "EVALUATING", "COMPLETED"] and set(program_machine["explicit_event_only"]) == {"CANCELLED", "SUPERSEDED"} and program_machine["blocker_return_behavior"] == "RECOMPUTE_FROM_CURRENT_MEMBER_REMEDIATION_STATES")
    check("P02", "program-state", "program state authority is member-derived and has no conformance effect", program_machine["state_authority"] == "DERIVED_FROM_MEMBER_REMEDIATIONS" and program_machine["conformance_effect"] == "NONE")
    check("P03", "program-state", "seven aggregate rules use deterministic order", [x["order"] for x in program_rules] == list(range(1, 8)) and [x["result"] for x in program_rules] == ["CREATED", "FAILED", "COMPLETED", "ACTIVE", "BLOCKED", "PLANNED", "TRIAGED"])
    program_cases = [([], None, "CREATED"), (["REJECTED"], None, "FAILED"), (["COMPLETE", "COMPLETE"], None, "COMPLETED"), (["IN_PROGRESS", "BLOCKED"], None, "ACTIVE"), (["BLOCKED"], None, "BLOCKED"), (["PROPOSED", "ASSESSED"], None, "PLANNED"), (["APPROVED"], None, "TRIAGED"), (["COMPLETE"], "CANCELLED", "CANCELLED"), (["BLOCKED"], "SUPERSEDED", "SUPERSEDED")]
    check("P04", "program-state", "independent program aggregate implementation passes nine cases", all(program_state(states, event) == expected for states, event, expected in program_cases))
    check("P05", "program-state", "three programs with no remediation derive CREATED", len(programs) == 3 and all(x["remediation_ids"] == [] and x["derived_program_state"] == program_state([]) == "CREATED" for x in programs))
    summaries = load(DEST / "PROGRAM-SUMMARIES.yaml")
    check("P06", "derived", "program summaries are derived and reproduce zero-member programs", summaries["authoritative"] is False and all(x["total_remediations"] == 0 and x["derived_program_state"] == "CREATED" for x in summaries["summaries"]))
    migration = load(DEST / "STATE-MIGRATION.yaml")
    check("P07", "migration", "v13 BLOCKED programs become new CREATED derived views without mutation", migration["prior_objects_modified"] is False and len(migration["migrations"]) == 3 and all(x["v13_status"] == "BLOCKED" and x["v13_1_derived_state"] == "CREATED" for x in migration["migrations"]))

    function = load(DEST / "AUDIT-AGGREGATE-FUNCTION.yaml")
    check("A01X", "aggregate", "aggregate inputs exclude all process states", function["inputs"] == ["AUDIT_SCOPE", "CURRENT_REQUIREMENT_DECISIONS", "EFFECTIVE_WAIVERS", "AUDIT_BLOCKERS", "INTEGRITY_RESULTS"] and set(function["process_state_inputs_forbidden"]) == {"FINDING_STATE", "REMEDIATION_STATE", "PROGRAM_STATE"})
    check("A02X", "aggregate", "deterministic precedence is violation, blocker, unresolved, waiver, pass", function["effective_precedence"] == ["NON_COMPLIANT", "BLOCKED", "UNVERIFIED", "CONDITIONALLY_COMPLIANT", "COMPLIANT"] and function["deterministic"] is True)
    expected_steps = ["RESOLVE_SCOPE", "REMOVE_NOT_APPLICABLE", "PARTITION_MANDATORY_OPTIONAL", "IDENTIFY_UNWAIVED_MANDATORY_VIOLATIONS", "RETURN_NON_COMPLIANT_IF_ANY", "IDENTIFY_WAIVED_MANDATORY_VIOLATIONS", "IDENTIFY_MANDATORY_BLOCKERS", "RETURN_BLOCKED_IF_ANY", "IDENTIFY_UNRESOLVED_MANDATORY_DECISIONS", "RETURN_UNVERIFIED_IF_ANY", "RETURN_CONDITIONALLY_COMPLIANT_IF_WAIVED_FAILURES", "RETURN_COMPLIANT"]
    check("A03X", "aggregate", "all twelve aggregate steps are exact", function["ordered_steps"] == expected_steps)
    vectors = load(DEST / "AGGREGATE-TEST-VECTORS.yaml"); vector_errors = []
    for item in vectors["vectors"]:
        actual, counts = aggregate(item["requirements"], item["audit_blockers"], item["integrity_pass"])
        if actual != item["expected"] or actual != item["actual"] or counts != item["counts"] or not item["pass"]: vector_errors.append(item["vector_id"])
    check("A04X", "aggregate", "all thirteen published vectors reproduce independently", vectors["summary"] == {"total": 13, "passed": 13, "failed": 0} and not vector_errors, str(vector_errors))
    by_id = {x["vector_id"]: x["actual"] for x in vectors["vectors"]}
    check("A05X", "precedence", "unwaived violation precedes blocker", by_id["UNWAIVED_FAIL_CONCEALS_NO_BLOCKER"] == "NON_COMPLIANT")
    check("A06X", "precedence", "blocker precedes waived failure and unresolved uncertainty", by_id["WAIVED_FAIL_WITH_BLOCKER"] == by_id["BLOCKED_PRECEDES_UNVERIFIED"] == "BLOCKED")
    check("A07X", "uncertainty", "UNVERIFIED, UNKNOWN, and PARTIAL aggregate to UNVERIFIED", {by_id[x] for x in ["UNVERIFIED_WITHOUT_VIOLATION", "UNKNOWN_AGGREGATES_UNVERIFIED", "PARTIAL_AGGREGATES_UNVERIFIED"]} == {"UNVERIFIED"})
    check("A08X", "waiver", "waived violation remains conditional unless blocker/unresolved dominates", by_id["WAIVED_FAILURE_ONLY"] == "CONDITIONALLY_COMPLIANT" and by_id["WAIVED_FAILURE_AND_UNRESOLVED"] == "UNVERIFIED")
    check("A09X", "optional", "optional failure cannot produce NON_COMPLIANT", by_id["OPTIONAL_FAILURE_ONLY"] == "COMPLIANT")
    check("A10X", "integrity", "intermediate completed decision and integrity failure block", by_id["INTERMEDIATE_FINAL_STATE"] == by_id["AUDIT_LEVEL_INTEGRITY_FAILURE"] == "BLOCKED")
    classification = load(DEST / "CONFORMANCE-CLASSIFICATION.yaml")
    check("A11X", "classification", "MAPPED, VERIFIED, UNASSESSED remain invalid final states", all(classification["classification"][x] == "INTERMEDIATE_INVALID_WHEN_COMPLETED" for x in ["MAPPED", "VERIFIED", "UNASSESSED"]))
    check("A12X", "classification", "optional failure exclusion is explicit", classification["optional_failure_causes_non_compliant"] is False)

    blockers = aggregate_obj["audit_blockers"]; current_actual, current_counts = aggregate([], blockers, False)
    check("C01", "current", "current aggregate independently recomputes BLOCKED", current_actual == aggregate_obj["aggregate_status"] == "BLOCKED" and current_counts["mandatory"] == aggregate_obj["mandatory_counts"] and current_counts["optional"] == aggregate_obj["optional_counts"])
    current_file = load(DEST / "CURRENT-AGGREGATE.yaml")
    check("C02", "separation", "current aggregate consumes no finding/remediation/program state", not current_file["finding_states_consumed"] and not current_file["remediation_states_consumed"] and not current_file["program_states_consumed"])
    check("C03", "current", "zero decisions remain zero without becoming compliance", aggregate_obj["decision_ids"] == [] and len(blockers) == 4 and aggregate_obj["integrity_status"] == "FAIL")
    integrity = load(DEST / "INTEGRITY-CONDITIONS.yaml")
    check("C04", "integrity", "mandatory/schema/evidence/temporal integrity failures block certification", integrity["aggregate_effect"] == "BLOCKED" and {x["condition"] for x in integrity["conditions"]} == {"MANDATORY_REQUIREMENTS_COMPLETE", "REFERENCES_RESOLVED", "SCHEMAS_VALID", "CERTIFICATE_SCOPE_RESOLVED", "REQUIRED_EVIDENCE_INTEGRITY", "TEMPORAL_INTEGRITY", "DECISION_CONFLICTS_RESOLVED"})
    certificate = load(DEST / "CERTIFICATE-REVISION-STATUS.yaml"); prior_cert = load(OUT / "AUDIT-CERTIFICATE.yaml")["objects"][0]
    check("C05", "certificate", "no process state causes certificate revision", certificate["status"] == "NOT_AUTHORIZED" and certificate["current_aggregate"]["object_id"] == aggregate_obj["object_id"] and certificate["prior_certificate_immutable"] is True)
    check("C06", "certificate", "prior certificate identity and hash remain exact", certificate["prior_certificate"]["object_id"] == prior_cert["object_id"] and certificate["prior_certificate_hash"] == prior_cert["certificate_hash"])
    prior_ref = certificate["prior_certificate"]; current_ref = certificate["current_aggregate"]
    check("C07", "references", "certificate status references resolve exactly once with matching types", len(root_by_id.get(prior_ref["object_id"], [])) == 1 and root_by_id[prior_ref["object_id"]][0]["object_type"] == prior_ref["object_type"] == "AUDIT_CERTIFICATE" and sum(obj["object_id"] == current_ref["object_id"] and obj["object_type"] == current_ref["object_type"] == "AUDIT_AGGREGATE" for obj in objects) == 1)

    transitions = load(DEST / "STATE-TRANSITIONS.yaml")
    check("E01", "events", "no historical transition event is fabricated", transitions["events"] == [] and transitions["imported_state_views_are_not_transition_events"] is True)
    check("E02", "events", "undefined transitions are mechanically rejected by rule", "legal transition rule" in transitions["rule"])
    invariants = load(DEST / "INVARIANTS.yaml")["invariants"]
    check("I01", "invariants", "all twenty-two state-separation invariants are mechanical", len(invariants) == 22 and [x["invariant_id"] for x in invariants] == [f"V131-I{i:02d}" for i in range(1, 23)] and all(x["enforcement"] == "MECHANICAL" for x in invariants))
    chain = load(DEST / "CANONICAL-TRANSFORMATION.yaml")
    check("I02", "traceability", "canonical v10-v13.1 transformation has new decision before aggregate", chain["protocol_versions"] == ["v10", "v10.1", "v11", "v11.1", "v12", "v12.1", "v13", "v13.1"] and chain["chain"].index("NEW_COMPLIANCE_DECISION") < chain["chain"].index("AGGREGATE") < chain["chain"].index("CERTIFICATE") and set(chain["truth_inputs"]) == {"COMPLIANCE_DECISION", "AUDIT_AGGREGATE"})
    report = load(DEST / "VALIDATION-REPORT.yaml")
    check("I03", "validation", "validation reports separated states and blocked aggregate", report["state_domains_separated"] is True and report["aggregate_test_vectors"] == {"total": 13, "passed": 13, "failed": 0} and report["current_aggregate"] == "BLOCKED")

    prior = load(DEST / "PRIOR-V13-INTEGRITY.yaml"); prior_errors = [x["path"] for x in prior["artifacts"] if not (OUT / x["path"]).is_file() or sha_file(OUT / x["path"]) != x["sha256"] or (OUT / x["path"]).stat().st_size != x["bytes"]]
    check("H01", "history", "all 130 prior v12/v13 artifacts remain byte-identical", prior["status"] == "PRESERVED" and prior["protected_artifact_count"] == len(prior["artifacts"]) == 130 and not prior_errors, str(prior_errors))
    check("H02", "history", "v13 programs remain immutable while v13.1 creates new derived views", sha_file(V13 / "REMEDIATION-PROGRAMS.yaml") == next(x["sha256"] for x in prior["artifacts"] if x["path"] == "remediation/REMEDIATION-PROGRAMS.yaml") and load(DEST / "STATE-MIGRATION.yaml")["prior_objects_modified"] is False)
    check("H03", "history", "v13 validation remains structurally successful and blocked", load(V13 / "VALIDATION.yaml")["overall_status"] == "STRUCTURAL_PASS_REMEDIATION_BLOCKED")

    state_report = load(REPORTS / "STATE-SEPARATION-REPORT.yaml"); aggregate_report = load(REPORTS / "AGGREGATE-CONFORMANCE-REPORT.yaml"); closure_report = load(REPORTS / "CLOSURE-IMPACT-REPORT.yaml")
    check("R01", "reports", "state report passes with no substitution", state_report["status"] == "PASS" and state_report["substitution_detected"] is False)
    check("R02", "reports", "aggregate report is blocked without process-state input", aggregate_report["status"] == "BLOCKED" and aggregate_report["process_states_used"] is False)
    check("R03", "reports", "closure report preserves findings and records zero direct process effects", closure_report["new_findings"] == 0 and closure_report["original_findings_overwritten"] is False and closure_report["direct_aggregate_changes_from_process_state"] == 0 and closure_report["new_compliance_decisions"] == 0 and closure_report["certificate_revision"] is False)

    det = load(DEST / "DETERMINISM-VALIDATION.yaml") if (DEST / "DETERMINISM-VALIDATION.yaml").is_file() else {}
    check("Q01", "determinism", "all 33 generator-owned v13.1 outputs reproduce byte-for-byte", det.get("status") == "PASS" and det.get("summary") == {"total": 33, "identical": 33, "different": 0} and {x["path"] for x in det.get("files", [])} == set(DELIVERABLES) and all(x["byte_identical"] for x in det.get("files", [])))
    check("Q02", "hygiene", "no Python caches exist", not any(HS.rglob("__pycache__")) and not any(HS.rglob("*.pyc")))
    check("Q03", "tools", "generic and pinned v13.1 tools exist", all((HS / "tools" / name).is_file() for name in ["build_state_separation_aggregate.py", "build_state_separation_aggregate_v131.py", "validate_state_separation_aggregate.py", "validate_state_separation_aggregate_v131.py"]))
    regression = load(DEST / "REGRESSION-VALIDATION.yaml") if (DEST / "REGRESSION-VALIDATION.yaml").is_file() else {}
    expected_regressions = {"13.0": (115, 0, 1), "12.1": (194, 0, 1), "12.0": (148, 0, 1), "11.1": (177, 0, 1), "10.1": (143, 0, 1)}
    actual_regressions = {x["protocol"]: (x["passed"], x["failed"], x["blocked"]) for x in regression.get("regressions", [])}
    check("Q04", "regression", "v10.1 through v13 regressions and append-only guard pass", regression.get("status") == "PASS" and actual_regressions == expected_regressions and regression.get("append_only_guard", {}).get("result") == "PASS_REFUSED")
    blocked("GATE-V131", "acceptance", "current audit aggregate", "The state architecture validates and aggregate vectors pass, but current audit status remains BLOCKED due invalid normative scope, missing implementation, and failed integrity prerequisites.")
    return finish(checks, {"schemas": 5, "findings": 3, "remediations": 0, "programs": 3, "requirement_decisions": 0, "aggregate_test_vectors": 13, "current_aggregate": 1})


def parseable(path: Path) -> bool:
    try: json.loads(path.read_text()); return True
    except Exception: return False


def finish(checks: list[dict[str, str]], counts: dict[str, Any]) -> int:
    passed = sum(x["result"] == "PASS" for x in checks); failed = sum(x["result"] == "FAIL" for x in checks); blocked_count = sum(x["result"] == "BLOCKED" for x in checks)
    report = {"schema_version": VERSION, "validator": "Protocol-v13.1 independent validator", "overall_status": "FAIL" if failed else "STRUCTURAL_PASS_AGGREGATE_BLOCKED" if blocked_count else "PASS", "acceptance": "VALIDATION_FAILED" if failed else "BLOCKED" if blocked_count else "PASS", "summary": {"total": len(checks), "passed": passed, "failed": failed, "blocked": blocked_count}, "object_counts": counts, "checks": checks}
    (DEST / "VALIDATION.yaml").write_text(json.dumps(report, indent=2) + "\n")
    lines = ["# Protocol-v13.1 Independent Validation", "", f"**Overall:** `{report['overall_status']}`", f"**Acceptance:** `{report['acceptance']}`", f"**Checks:** {passed} PASS / {failed} FAIL / {blocked_count} BLOCKED ({len(checks)} total)", "", "State-separation validity does not alter the current blocked requirement/audit truth state.", "", "| ID | Category | Result | Description | Detail |", "|---|---|---|---|---|"]
    for x in checks: lines.append("| %s | %s | %s | %s | %s |" % (x["check_id"], x["category"], x["result"], x["description"].replace("|", "\\|"), x["detail"].replace("|", "\\|")))
    (DEST / "VALIDATION.md").write_text("\n".join(lines) + "\n")
    print(f"{passed} PASS / {failed} FAIL / {blocked_count} BLOCKED ({len(checks)} checks); {report['overall_status']}")
    return 1 if failed else 0


if __name__ == "__main__": sys.exit(main())
