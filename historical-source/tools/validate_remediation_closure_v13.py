#!/usr/bin/env python3
"""Independent Protocol-v13 remediation/closure package validator."""
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
SCHEMA = OUT / "schema"
REPORTS = OUT / "reports"
VERSION = "13.0"
OBJECT_TYPES = ["REMEDIATION_PROGRAM", "ROOT_CAUSE", "REMEDIATION_ACTION", "CHANGE_SET", "IMPACT_ASSESSMENT", "REVERIFICATION_PLAN", "REVERIFICATION_EXECUTION", "REGRESSION_SCOPE", "CLOSURE_DECISION", "WAIVER_REVIEW", "CERTIFICATE_REVISION", "RESIDUAL_RISK"]
SCHEMA_NAMES = ["remediation-program", "root-cause", "remediation-action", "change-set", "impact-assessment", "reverification-plan", "reverification-execution", "regression-scope", "closure-decision", "waiver-review", "residual-risk", "certificate-revision"]
SCHEMA_BY_TYPE = {name.upper().replace("-", "_"): name for name in SCHEMA_NAMES}
REGISTRY_FILES = ["REMEDIATION-PROGRAMS.yaml", "ROOT-CAUSES.yaml", "REMEDIATION-ACTIONS.yaml", "CHANGE-SETS.yaml", "IMPACT-ASSESSMENTS.yaml", "REVERIFICATION-PLANS.yaml", "REVERIFICATION-EXECUTIONS.yaml", "REGRESSION-SCOPES.yaml", "CLOSURE-DECISIONS.yaml", "WAIVER-REVIEWS.yaml", "RESIDUAL-RISKS.yaml", "CERTIFICATE-REVISIONS.yaml"]
SUPPORT_FILES = ["REMEDIATION-STATE-MACHINE.yaml", "VALIDATION-PIPELINE.yaml", "VALIDATION-ERRORS.yaml", "VALIDATION-REPORT.yaml", "DECISION-FUNCTION.yaml", "CLOSURE-PREDICATE.yaml", "CLOSURE-INVARIANTS.yaml", "PRIOR-AUDIT-INTEGRITY.yaml", "OBJECT-REGISTRY.yaml", "SCHEMA-REGISTRY.yaml", "IMPACT-RULES.yaml", "REVERIFICATION-RULES.yaml", "CERTIFICATE-LINEAGE.yaml", "REMEDIATION-DEPENDENCY-GRAPH.yaml", "ACCOUNTABILITY-CHAIN.yaml"]
REPORT_FILES = ["REMEDIATION-STATUS.yaml", "REVERIFICATION-REPORT.yaml", "REGRESSION-REPORT.yaml", "CLOSURE-REPORT.yaml"]
DELIVERABLES = [*(f"remediation/{name}" for name in REGISTRY_FILES + SUPPORT_FILES), *(f"schema/{name}.schema.yaml" for name in SCHEMA_NAMES), *(f"reports/{name}" for name in REPORT_FILES)]
PIPELINE = ["LOAD_FINDING", "VALIDATE_FINDING", "VALIDATE_NORMATIVE_BASIS", "CLASSIFY_FAILURE_BOUNDARY", "ESTABLISH_ROOT_CAUSE", "DEFINE_REMEDIATION", "RECORD_CHANGE_SET", "ASSESS_IMPACT", "DETERMINE_REVERIFICATION_SCOPE", "VALIDATE_ORACLE", "EXECUTE_REVERIFICATION", "EXECUTE_REGRESSION", "REEVALUATE_CONFORMANCE", "ASSESS_RESIDUAL_RISK", "DECIDE_CLOSURE", "REVISE_CERTIFICATE"]
FAILURES = {"FINDING_INVALID", "ROOT_CAUSE_INSUFFICIENT", "REMEDIATION_UNDEFINED", "CHANGE_SET_MISSING", "IMPACT_INCOMPLETE", "REVERIFICATION_SCOPE_INCOMPLETE", "ORACLE_INVALID", "REVERIFICATION_BLOCKED", "REVERIFICATION_FAILED", "REGRESSION_FAILED", "REGRESSION_INCOMPLETE", "NEW_NONCONFORMANCE", "TRACEABILITY_BROKEN", "RESIDUAL_RISK_MISSING", "CERTIFICATE_LINEAGE_BROKEN"}
ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]*$")


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def valid_timestamp(value: Any) -> bool:
    if not isinstance(value, str) or not (value.endswith("Z") or re.search(r"[+-]\d{2}:\d{2}$", value)):
        return False
    try: return datetime.fromisoformat(value.replace("Z", "+00:00")).tzinfo is not None
    except ValueError: return False


def resolve_pointer(document: Any, pointer: str) -> Any:
    node = document
    for part in pointer.lstrip("/").split("/") if pointer else []:
        key = part.replace("~1", "/").replace("~0", "~")
        node = node[int(key)] if isinstance(node, list) else node[key]
    return node


def schema_errors(value: Any, schema: dict[str, Any], schemas: dict[str, Any], current: str, path: str = "$") -> list[str]:
    errors: list[str] = []
    if "$ref" in schema:
        file_part, _, pointer = schema["$ref"].partition("#")
        target = Path(file_part).name.replace(".schema.yaml", "") if file_part else current
        try: resolved = resolve_pointer(schemas[target], pointer)
        except (KeyError, IndexError, TypeError, ValueError): return [f"{path}: unresolved $ref {schema['$ref']}"]
        return schema_errors(value, resolved, schemas, target, path)
    if "oneOf" in schema:
        results = [schema_errors(value, item, schemas, current, path) for item in schema["oneOf"]]
        return [] if sum(not item for item in results) == 1 else [f"{path}: oneOf"]
    expected = schema.get("type")
    if expected is not None:
        types = expected if isinstance(expected, list) else [expected]
        tests = {"object": lambda: isinstance(value, dict), "array": lambda: isinstance(value, list), "string": lambda: isinstance(value, str), "integer": lambda: isinstance(value, int) and not isinstance(value, bool), "boolean": lambda: isinstance(value, bool), "null": lambda: value is None}
        if not any(tests.get(item, lambda: False)() for item in types): return [f"{path}: type {expected}"]
    if "const" in schema and value != schema["const"]: errors.append(f"{path}: const")
    if "enum" in schema and value not in schema["enum"]: errors.append(f"{path}: enum")
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0): errors.append(f"{path}: minLength")
        if "maxLength" in schema and len(value) > schema["maxLength"]: errors.append(f"{path}: maxLength")
        if "pattern" in schema and re.fullmatch(schema["pattern"], value) is None: errors.append(f"{path}: pattern")
        if schema.get("format") == "date-time" and not valid_timestamp(value): errors.append(f"{path}: date-time")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0): errors.append(f"{path}: minItems")
        if schema.get("uniqueItems") and len({canonical(item) for item in value}) != len(value): errors.append(f"{path}: uniqueItems")
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


def registry(name: str) -> list[dict[str, Any]]:
    return load(REM / name)["objects"]


def main() -> int:
    checks: list[dict[str, str]] = []
    def check(cid: str, category: str, description: str, ok: bool, detail: str = "") -> None:
        checks.append({"check_id": cid, "category": category, "description": description, "result": "PASS" if ok else "FAIL", "detail": detail})
    def blocked(cid: str, category: str, description: str, detail: str) -> None:
        checks.append({"check_id": cid, "category": category, "description": description, "result": "BLOCKED", "detail": detail})

    for index, path in enumerate(DELIVERABLES, 1): check(f"A{index:02d}", "artifacts", f"v13 artifact exists: {path}", (OUT / path).is_file())
    if any(x["result"] == "FAIL" for x in checks): return finish(checks, {})
    check("A44", "artifacts", "v13 generator-owned artifact set has 43 unique paths", len(DELIVERABLES) == len(set(DELIVERABLES)) == 43)
    check("A45", "artifacts", "all v13 YAML is JSON-compatible", all(parseable(OUT / path) for path in DELIVERABLES))
    check("A46", "layout", "all twelve normative registries use remediation directory", all((REM / name).is_file() for name in REGISTRY_FILES))
    check("A47", "layout", "all four required reports use lowercase reports directory", all((REPORTS / name).is_file() for name in REPORT_FILES))

    schemas = {"common": load(SCHEMA / "common.schema.yaml")} | {name: load(SCHEMA / f"{name}.schema.yaml") for name in SCHEMA_NAMES}
    check("S01", "schemas", "all twelve v13 object schemas exist", len(SCHEMA_NAMES) == 12 and all((SCHEMA / f"{name}.schema.yaml").is_file() for name in SCHEMA_NAMES))
    check("S02", "schemas", "every v13 object type has exactly one explicit schema", set(SCHEMA_BY_TYPE) == set(OBJECT_TYPES) and len(SCHEMA_BY_TYPE) == 12)
    common_required = {"object_type", "schema_version", "object_id", "created_at"}
    check("S03", "schemas", "every v13 schema requires the common object contract", all(common_required <= set(schemas[name]["required"]) for name in SCHEMA_NAMES))
    check("S04", "schemas", "every required field has a declared schema", all(set(schemas[name]["required"]) <= set(schemas[name]["properties"]) for name in SCHEMA_NAMES))
    check("S05", "schemas", "v13 schemas reject undocumented implicit fields", all(schemas[name]["additionalProperties"] is False for name in SCHEMA_NAMES))
    check("S06", "schemas", "all v13 schema references resolve", all(resolve_schema_ref(ref, current, schemas) for current in SCHEMA_NAMES for ref in extract_refs(schemas[current])))
    schema_registry = load(REM / "SCHEMA-REGISTRY.yaml")
    check("S07", "schemas", "v13 schema registry records all twelve exact hashes", len(schema_registry["schemas"]) == 12 and all(sha_file(REM / item["path"]) == item["sha256"] for item in schema_registry["schemas"]))
    check("S08", "schemas", "schema registry reuses the hash-bound v12.1 common schema", sha_file(REM / schema_registry["common_schema"]["path"]) == schema_registry["common_schema"]["sha256"])
    check("S09", "schemas", "reverification plans require nonempty requirements, oracles, and criteria", all(schemas["reverification-plan"]["properties"][field]["minItems"] == 1 for field in ["requirement_ids", "oracle_ids", "acceptance_criteria"]))
    check("S10", "schemas", "closure evidence and root-cause evidence cannot be empty", schemas["closure-decision"]["properties"]["evidence"]["minItems"] == 1 and schemas["root-cause"]["properties"]["evidence"]["minItems"] == 1)
    check("S11", "schemas", "specification change is explicitly separated from implementation remediation", any("SPECIFICATION_CHANGE" in item for item in schemas["remediation-action"]["x-v13-constraints"]))
    check("S12", "schemas", "certificate revisions require new evidence, verification, decisions, and aggregate", {"new_evidence", "new_verifications", "new_decisions", "new_aggregate_status"} <= set(schemas["certificate-revision"]["required"]))
    check("S13", "schemas", "root-cause schema requires failure, cause, normative condition, evidence, and epistemic status", {"what_failed", "why_failed", "normative_condition", "evidence", "cause_status", "confidence"} <= set(schemas["root-cause"]["required"]) and set(schemas["root-cause"]["properties"]["cause_status"]["enum"]) == {"ESTABLISHED", "HYPOTHETICAL", "UNKNOWN"})
    check("S14", "schemas", "reverification execution must link its plan and change set", {"plan_id", "change_set_id", "evidence"} <= set(schemas["reverification-execution"]["required"]))

    local_objects = [(obj, name) for name in REGISTRY_FILES for obj in registry(name)]
    ids = [obj["object_id"] for obj, _ in local_objects]
    check("O01", "objects", "all local v13 object IDs are unique and syntactically valid", len(ids) == len(set(ids)) and all(ID_PATTERN.fullmatch(item) and len(item) <= 256 for item in ids))
    check("O02", "objects", "every local object has v13 common fields and timezone timestamp", all(obj["schema_version"] == VERSION and obj["object_type"] in OBJECT_TYPES and valid_timestamp(obj["created_at"]) for obj, _ in local_objects))
    object_errors = {obj["object_id"]: schema_errors(obj, schemas[SCHEMA_BY_TYPE[obj["object_type"]]], schemas, SCHEMA_BY_TYPE[obj["object_type"]]) for obj, _ in local_objects}
    check("O03", "objects", "every instantiated v13 object validates against its schema", not any(object_errors.values()), str({k: v for k, v in object_errors.items() if v}))
    local_registry = load(REM / "OBJECT-REGISTRY.yaml")
    check("O04", "objects", "local object registry indexes all and only instantiated objects", {(x["object_type"], x["object_id"], x["source_file"]) for x in local_registry["objects"]} == {(obj["object_type"], obj["object_id"], name) for obj, name in local_objects})
    external = load(OUT / "OBJECT-REGISTRY.yaml"); external_ids = {x["object_id"] for x in external["objects"]}
    check("O05", "objects", "local IDs are globally unique against v12.1 objects", not (set(ids) & external_ids) and local_registry["global_uniqueness_checked"] is True)
    check("O06", "objects", "external object registry reference and hash resolve", sha_file(REM / local_registry["external_registry"]["path"]) == local_registry["external_registry"]["sha256"])

    programs = registry("REMEDIATION-PROGRAMS.yaml"); risks = registry("RESIDUAL-RISKS.yaml"); findings = load(OUT / "FINDINGS.yaml")["objects"]; finding_ids = {x["object_id"] for x in findings}
    check("P01", "programs", "one blocked program exists for each finding", len(programs) == len(findings) == 3 and {x for p in programs for x in p["finding_ids"]} == finding_ids and all(p["status"] == "BLOCKED" for p in programs))
    check("P02", "programs", "blocked programs are not represented as closed", all(p["closed_at"] is None for p in programs))
    check("P03", "risk", "every finding retains one unresolved residual risk", len(risks) == 3 and {x["source_finding_id"] for x in risks} == finding_ids and all(x["disposition"] == "UNRESOLVED" for x in risks))
    downstream = ["ROOT-CAUSES.yaml", "REMEDIATION-ACTIONS.yaml", "CHANGE-SETS.yaml", "IMPACT-ASSESSMENTS.yaml", "REVERIFICATION-PLANS.yaml", "REVERIFICATION-EXECUTIONS.yaml", "REGRESSION-SCOPES.yaml", "CLOSURE-DECISIONS.yaml", "WAIVER-REVIEWS.yaml", "CERTIFICATE-REVISIONS.yaml"]
    check("P04", "gating", "no downstream object is fabricated after R2 stop", all(registry(name) == [] for name in downstream))
    check("P05", "distinctions", "root cause, action, change, execution, closure, and waiver remain distinct empty registries", len({load(REM / name)["object_type"] for name in downstream}) == len(downstream))
    check("P06", "integrity", "no code/specification/oracle/test change is claimed", registry("REMEDIATION-ACTIONS.yaml") == [] and registry("CHANGE-SETS.yaml") == [])

    pipeline = load(REM / "VALIDATION-PIPELINE.yaml"); report = load(REM / "VALIDATION-REPORT.yaml"); errors = load(REM / "VALIDATION-ERRORS.yaml")
    check("V01", "pipeline", "canonical remediation pipeline is exact R0-R15", [x["stage_id"] for x in pipeline["stages"]] == [f"R{i}" for i in range(16)] and [x["stage"] for x in pipeline["stages"]] == PIPELINE)
    check("V02", "pipeline", "R0 and R1 pass before R2 blocks/stops", [x["status"] for x in pipeline["stages"][:3]] == ["PASS", "PASS", "BLOCKED_STOP"] and pipeline["stop_stage"] == "R2")
    check("V03", "pipeline", "R3-R15 are not executed past invalid normative basis", all(x["status"] == "NOT_EXECUTED_EARLY_STOP" for x in pipeline["stages"][3:]))
    check("V04", "pipeline", "validation report counts pipeline outcomes", report["summary"] == {"stages": 16, "executed": 3, "passed": 2, "blocked": 1, "not_executed": 13})
    check("V05", "pipeline", "closure and certificate revision are unauthorized", report["closure_authorized"] is False and report["certificate_revision_authorized"] is False)
    check("V06", "failures", "all fifteen remediation validation failures are registered", set(errors["failure_codes"]) == FAILURES)
    check("V07", "failures", "current process failure is not implementation nonconformance", len(errors["errors"]) == 1 and errors["errors"][0]["code"] == "TRACEABILITY_BROKEN" and errors["errors"][0]["stage"] == "R2" and errors["errors"][0]["implementation_nonconformance"] is False)
    check("V08", "gating", "invalid v11.1 normative basis remains the blocker", load(OUT / "VALIDATION-REPORT.yaml")["overall_status"] == "BLOCKED_SCHEMA_INVALID_INPUT" and load(OUT / "INPUT-CONTRACT.yaml")["v11_1"]["requirement_count"] == 0)

    machine = load(REM / "REMEDIATION-STATE-MACHINE.yaml")
    check("T01", "state-machine", "normal path is exact OPEN through CLOSED", machine["normal_path"] == ["OPEN", "TRIAGED", "ROOT_CAUSED", "PLANNED", "IN_PROGRESS", "READY_FOR_VERIFICATION", "VERIFIED", "CLOSED"])
    transitions = {(x["from"], x["to"]) for x in machine["legal_transitions"]}
    check("T02", "state-machine", "seventeen guarded legal transition patterns are unique", len(transitions) == len(machine["legal_transitions"]) == 17 and all(x["guard"] for x in machine["legal_transitions"]))
    check("T03", "state-machine", "every active state can block and blocked returns only to previous state", all((state, "BLOCKED") in transitions for state in machine["normal_path"][:-1]) and ("BLOCKED", "$PREVIOUS_ACTIVE_STATE") in transitions)
    expected_forbidden = {"OPEN", "TRIAGED", "ROOT_CAUSED", "PLANNED", "IN_PROGRESS", "READY_FOR_VERIFICATION", "BLOCKED", "WAIVED"}
    check("T04", "state-machine", "all eight direct closure paths are forbidden", {x["from"] for x in machine["forbidden_direct_closure"]} == expected_forbidden and all(x["to"] == "CLOSED" for x in machine["forbidden_direct_closure"]))
    check("T05", "waiver", "waiver changes disposition without changing normative truth", machine["waiver_disposition"]["disposition"] == "WAIVED" and machine["waiver_disposition"]["underlying_normative_truth_changed"] is False)
    legal_pairs = transitions
    histories_ok = all(history["current"] == "BLOCKED" and all((step["from"], step["to"]) in legal_pairs for step in history["transitions"]) for history in machine["state_histories"])
    check("T06", "state-machine", "all three actual program histories use legal transitions", histories_ok and {x["program_id"] for x in machine["state_histories"]} == {x["object_id"] for x in programs})

    closure = load(REM / "CLOSURE-PREDICATE.yaml"); decision = load(REM / "DECISION-FUNCTION.yaml")
    check("C01", "closure", "closure predicate contains all eleven mandatory conjuncts", closure["operator"] == "AND" and len(closure["predicates"]) == 11 and closure["closed_iff_all_true"] is True)
    check("C02", "closure", "current closure predicates are all false and result blocked", set(closure["current"]) == set(closure["predicates"]) and not any(closure["current"].values()) and closure["current_result"] == "BLOCKED")
    check("C03", "closure", "decision function distinguishes all seven closure outcomes", set(decision["function"]) == {"CLOSED", "PARTIALLY_RESOLVED", "REMAINS_OPEN", "WAIVED", "BLOCKED", "SUPERSEDED", "REJECTED"} and decision["precedence"] == ["REJECTED", "SUPERSEDED", "WAIVED", "BLOCKED", "REMAINS_OPEN", "PARTIALLY_RESOLVED", "CLOSED"] and decision["deterministic_for_identical_normalized_inputs"] is True)
    invariants = load(REM / "CLOSURE-INVARIANTS.yaml")["invariants"]
    check("C04", "invariants", "all twenty closure invariants are mechanically registered", len(invariants) == 20 and [x["invariant_id"] for x in invariants] == [f"V13-I{i:02d}" for i in range(1, 21)] and all(x["enforcement"] == "MECHANICAL" for x in invariants))
    reverification = load(REM / "REVERIFICATION-RULES.yaml")
    check("C05", "reverification", "reverification preserves original failure-to-new-evidence chain", reverification["required_chain"] == ["ORIGINAL_VIOLATION", "ORIGINAL_NORMATIVE_CONDITION", "ORIGINAL_ACCEPTANCE_CRITERION", "VALIDATED_ORACLE", "NEW_EXECUTION", "NEW_EVIDENCE"])
    check("C06", "reverification", "flaky verification is inconclusive and cannot close", reverification["flaky_result"] == "INCONCLUSIVE" and set(reverification["flaky_closure"]) == {"REMAINS_OPEN", "BLOCKED"})
    check("C07", "regression", "regression scope includes original, direct, and transitive requirements", reverification["regression_scope"] == ["ORIGINAL_FAILING_REQUIREMENT", "DIRECTLY_AFFECTED_REQUIREMENTS", "TRANSITIVE_DEPENDENT_REQUIREMENTS"])
    check("C07A", "regression", "security, concurrency, persistence, and resource coverage are explicit", set(reverification["recommended_explicit_regression_coverage"]) == {"SECURITY", "CONCURRENCY", "PERSISTENCE", "RESOURCE_BOUNDARIES"})
    check("C07B", "reassessment", "post-remediation decisions are invalidated, reevaluated, propagated, and reaggregated", reverification["post_remediation_recalculation"] == ["INVALIDATE_AFFECTED_DECISION", "REEVALUATE_AFFECTED_REQUIREMENT", "PROPAGATE_DEPENDENCY_GRAPH", "RECALCULATE_AUDIT_AGGREGATE"] and "impact evidence" in reverification["decision_reuse_policy"])
    impact = load(REM / "IMPACT-RULES.yaml")
    check("C08", "impact", "impact analysis has all eleven minimum dimensions", len(impact["minimum_dimensions"]) == 11 and impact["unknown_impact_is_zero"] is False and impact["incomplete_dependency_policy"] == "CONSERVATIVE")
    check("C09", "impact", "generic discovery pipeline trigger set is complete", impact["discovery_pipeline_triggers"] == ["Candidate", "Acquisition", "Observation", "Recognition", "Discovery", "Candidate Expansion", "Scheduler"])
    dependency_graph = load(REM / "REMEDIATION-DEPENDENCY-GRAPH.yaml")
    check("C10", "dependencies", "remediation dependency graph is separate and nothing is ready", dependency_graph["graph_type"] == "REMEDIATION_DEPENDENCY_GRAPH" and dependency_graph["ready_for_verification"] == [])
    chain = load(REM / "ACCOUNTABILITY-CHAIN.yaml")
    check("C11", "traceability", "v10-v13 accountability chain terminates honestly at finding", len(chain["chain"]) == 19 and chain["current_terminal_stage"] == "FINDING" and chain["blocked_next_stage"] == "ROOT_CAUSE")
    check("C12", "history", "historical remediation preserves old decisions and requires new version/decision", chain["historical_remediation_policy"] == {"historical_decision_immutable": True, "later_remediation_requires_new_implementation_version": True, "later_conformance_requires_new_decision": True, "retrospective_audit_must_be_explicit": True})
    check("C13", "findings", "remediation-introduced violations require separate findings", "separate finding" in chain["new_finding_policy"] and "never overwrites" in chain["new_finding_policy"])

    prior = load(REM / "PRIOR-AUDIT-INTEGRITY.yaml")
    prior_errors = [item["path"] for item in prior["artifacts"] if not (OUT / item["path"]).is_file() or sha_file(OUT / item["path"]) != item["sha256"] or (OUT / item["path"]).stat().st_size != item["bytes"]]
    check("I01", "immutability", "all protected v12/v12.1 artifacts remain byte-identical", prior["status"] == "PRESERVED" and prior["protected_artifact_count"] == len(prior["artifacts"]) == 83 and not prior_errors, str(prior_errors))
    protected_paths = {x["path"] for x in prior["artifacts"]}
    check("I02", "immutability", "prior findings, evidence, decisions, requirements, and certificate are protected", {"FINDINGS.yaml", "EVIDENCE-RECORDS.yaml", "CONFORMANCE-DECISIONS.yaml", "AUDIT-CERTIFICATE.yaml", "../specification/REQUIREMENTS.yaml"} - {"../specification/REQUIREMENTS.yaml"} <= protected_paths and sha_file(HS / "specification/REQUIREMENTS.yaml") == load(OUT / "INPUT-ARTIFACTS.yaml")["objects"][1]["metadata"]["source_content_hash"]["value"])
    lineage = load(REM / "CERTIFICATE-LINEAGE.yaml"); prior_cert = load(OUT / "AUDIT-CERTIFICATE.yaml")["objects"][0]
    check("I03", "certificate", "certificate lineage retains immutable v12.1 predecessor", lineage["lineage"] == [prior_cert["object_id"]] and lineage["previous_certificate_hash"] == prior_cert["certificate_hash"] and lineage["revisions"] == [])
    check("I04", "certificate", "no certificate revision exists without changed decisions", registry("CERTIFICATE-REVISIONS.yaml") == [] and lineage["status"] == "UNCHANGED_NO_DECISION_REVISION")
    check("I05", "history", "historical record is append-only while current conformance remains iterative", chain["append_only_history"] is True and chain["iterative_conformance"] is True)

    remediation_status = load(REPORTS / "REMEDIATION-STATUS.yaml"); reverify_report = load(REPORTS / "REVERIFICATION-REPORT.yaml"); regression_report = load(REPORTS / "REGRESSION-REPORT.yaml"); closure_report = load(REPORTS / "CLOSURE-REPORT.yaml")
    check("P07", "reports", "remediation report is blocked with no fabricated changes", remediation_status["status"] == "BLOCKED" and remediation_status["changes_recorded"] == 0)
    check("P08", "reports", "reverification report is not executed and not passed", reverify_report["status"] == "NOT_EXECUTED" and reverify_report["pass"] == 0 and reverify_report["executions"] == 0)
    check("P09", "reports", "regression report is not executed and zero is not a pass", regression_report["status"] == "NOT_EXECUTED" and regression_report["executions"] == 0)
    check("P10", "reports", "closure report closes nothing and preserves prior certificate", closure_report["status"] == "BLOCKED" and closure_report["closed"] == 0 and closure_report["blocked_without_decision"] == 3 and closure_report["prior_certificate_immutable"] is True)

    det = load(REM / "DETERMINISM-VALIDATION.yaml") if (REM / "DETERMINISM-VALIDATION.yaml").is_file() else {}
    check("Q01", "determinism", "all 43 v13 generator outputs reproduce byte-for-byte", det.get("status") == "PASS" and det.get("summary") == {"total": 43, "identical": 43, "different": 0} and {x["path"] for x in det.get("files", [])} == set(DELIVERABLES) and all(x["byte_identical"] for x in det.get("files", [])))
    check("Q02", "hygiene", "authoritative historical/planning documents remain outside generator outputs", all(not path.startswith("Userscript Discovery Prototype.md") and not path.startswith("Continue Architecture Planning.md") for path in DELIVERABLES))
    check("Q03", "hygiene", "no Python cache artifacts exist", not any(HS.rglob("__pycache__")) and not any(HS.rglob("*.pyc")))
    check("Q04", "tools", "generic and version-pinned v13 builders/validators exist", all((HS / "tools" / name).is_file() for name in ["build_remediation_closure.py", "build_remediation_closure_v13.py", "validate_remediation_closure.py", "validate_remediation_closure_v13.py"]))
    blocked("GATE-V13", "acceptance", "Protocol-v13 remediation closure gate", "R2 blocks because no accepted normative requirements exist. No root cause, change, re-verification, regression, closure, conformance recalculation, or certificate revision is authorized.")
    counts = {"schemas": 12, "programs": 3, "residual_risks": 3, "root_causes": 0, "actions": 0, "change_sets": 0, "impact_assessments": 0, "reverification_plans": 0, "reverification_executions": 0, "regression_scopes": 0, "closure_decisions": 0, "certificate_revisions": 0}
    return finish(checks, counts)


def resolve_schema_ref(reference: str, current: str, schemas: dict[str, Any]) -> bool:
    file_part, _, pointer = reference.partition("#")
    target = Path(file_part).name.replace(".schema.yaml", "") if file_part else current
    try: resolve_pointer(schemas[target], pointer); return True
    except (KeyError, IndexError, TypeError, ValueError): return False


def parseable(path: Path) -> bool:
    try: json.loads(path.read_text(encoding="utf-8")); return True
    except Exception: return False


def finish(checks: list[dict[str, str]], counts: dict[str, int]) -> int:
    passed = sum(x["result"] == "PASS" for x in checks); failed = sum(x["result"] == "FAIL" for x in checks); blocked_count = sum(x["result"] == "BLOCKED" for x in checks)
    report = {"schema_version": VERSION, "validator": "Protocol-v13 independent validator", "overall_status": "FAIL" if failed else "STRUCTURAL_PASS_REMEDIATION_BLOCKED" if blocked_count else "PASS", "acceptance": "VALIDATION_FAILED" if failed else "BLOCKED" if blocked_count else "PASS", "summary": {"total": len(checks), "passed": passed, "failed": failed, "blocked": blocked_count}, "object_counts": counts, "checks": checks}
    (REM / "VALIDATION.yaml").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    lines = ["# Protocol-v13 Independent Validation", "", f"**Overall:** `{report['overall_status']}`", f"**Acceptance:** `{report['acceptance']}`", f"**Checks:** {passed} PASS / {failed} FAIL / {blocked_count} BLOCKED ({len(checks)} total)", "", "Structural success validates deterministic blocked remediation. It does not establish a fix, verification, conformance, closure, or revised certificate.", "", "| ID | Category | Result | Description | Detail |", "|---|---|---|---|---|"]
    for item in checks: lines.append("| %s | %s | %s | %s | %s |" % (item["check_id"], item["category"], item["result"], item["description"].replace("|", "\\|"), item["detail"].replace("|", "\\|")))
    (REM / "VALIDATION.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{passed} PASS / {failed} FAIL / {blocked_count} BLOCKED ({len(checks)} checks); {report['overall_status']}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
