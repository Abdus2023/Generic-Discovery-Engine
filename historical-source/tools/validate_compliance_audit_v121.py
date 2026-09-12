#!/usr/bin/env python3
"""Independent deterministic validator for Protocol-v12.1 outputs."""
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
SPEC = HS / "specification"
OUT = HS / "compliance"
SCHEMA_DIR = OUT / "schema"
VERSION = "12.1"
OBJECT_TYPES = {
    "AUDIT", "AUDIT_SCOPE", "INPUT_ARTIFACT", "ENVIRONMENT",
    "IMPLEMENTATION_ARTIFACT", "IMPLEMENTATION_CLAIM", "REQUIREMENT_MAPPING",
    "EVIDENCE_RECORD", "VERIFICATION_EXECUTION", "COMPLIANCE_DECISION",
    "NONCONFORMANCE", "WAIVER", "REMEDIATION", "AUDIT_FINDING",
    "AUDIT_RUN", "AUDIT_CERTIFICATE",
}
SCHEMA_NAMES = [
    "common", "audit", "audit-scope", "input-artifact", "environment",
    "implementation-artifact", "implementation-claim", "requirement-mapping",
    "evidence-record", "verification-execution", "compliance-decision",
    "nonconformance", "waiver", "remediation", "audit-finding", "audit-run",
    "audit-certificate",
]
SCHEMA_BY_TYPE = {name.upper().replace("-", "_"): name for name in SCHEMA_NAMES if name != "common"}
MACHINE = [
    "AGGREGATION.yaml", "AUDIT-CERTIFICATE.yaml", "AUDIT-EVIDENCE-GRAPH.yaml", "AUDIT-RUNS.yaml", "AUDIT-SCOPE.yaml", "AUDIT.yaml",
    "COMPLIANCE-AGGREGATION.yaml", "COMPLIANCE-DECISIONS.yaml", "COMPLIANCE-MATRIX.yaml", "CONFLICT-VALIDATION.yaml", "CONFORMANCE-DECISIONS.yaml", "CONFORMANCE-GRAPH.yaml",
    "CONFORMANCE-INVARIANTS.yaml", "CONFORMANCE-STATE-MACHINE.yaml",
    "DECISION-ALGORITHM.yaml", "DEPENDENCY-VALIDATION.yaml", "ENVIRONMENTS.yaml",
    "EVIDENCE-RECORDS.yaml", "EVIDENCE-VALIDATION.yaml", "FAILURE-BOUNDARIES.yaml", "FINDING-GRAPH.yaml", "FINDINGS.yaml",
    "IMPLEMENTATION-ARTIFACTS.yaml", "IMPLEMENTATION-CLAIMS.yaml", "IMPLEMENTATION-EVIDENCE.yaml", "IMPLEMENTATION-GRAPH.yaml",
    "INPUT-ARTIFACTS.yaml", "INPUT-CONTRACT.yaml", "NONCONFORMANCES.yaml",
    "NORMATIVE-MODEL.yaml", "OBJECT-REGISTRY.yaml", "ORACLE-VALIDATION.yaml",
    "REFERENCE-INTEGRITY.yaml", "RELEASE-GATE.yaml", "REMEDIATION-ACTIONS.yaml", "REMEDIATIONS.yaml", "REQUIREMENT-MAPPINGS.yaml",
    "SCHEMA-REGISTRY.yaml", "SCHEMA-VALIDATION.yaml", "TEMPORAL-INTEGRITY.yaml",
    "VALIDATION-ERRORS.yaml", "VALIDATION-PIPELINE.yaml", "VALIDATION-REPORT.yaml",
    "VERIFICATION-EXECUTIONS.yaml", "VERIFICATION-VALIDATION.yaml", "WAIVERS.yaml",
]
SCHEMAS = [f"schema/{name}.schema.yaml" for name in SCHEMA_NAMES]
REPORTS = [
    "REPORTS/AGGREGATION.md", "REPORTS/COMPATIBILITY-AUDIT.md", "REPORTS/COMPLIANCE-MATRIX.md",
    "REPORTS/FINAL-COMPLIANCE-REPORT.md", "REPORTS/FINDINGS.md", "REPORTS/NONCONFORMANCES.md",
    "REPORTS/REFERENCE-INTEGRITY.md", "REPORTS/REGRESSION-REPORT.md", "REPORTS/REMEDIATION-PLAN.md",
    "REPORTS/SCHEMA-VALIDATION.md", "REPORTS/SECURITY-AUDIT.md", "REPORTS/STATE-TRANSITIONS.md",
    "REPORTS/TEMPORAL-AUDIT.md", "REPORTS/TEMPORAL-INTEGRITY.md", "REPORTS/TRACEABILITY-AUDIT.md",
    "REPORTS/VALIDATION-PIPELINE.md",
]
DELIVERABLES = MACHINE + SCHEMAS + REPORTS
PIPELINE = [
    "LOAD", "STRUCTURAL_VALIDATION", "SCHEMA_VALIDATION", "REFERENCE_VALIDATION",
    "VERSION_TEMPORAL_VALIDATION", "HASH_INTEGRITY_VALIDATION",
    "REQUIREMENT_SEMANTIC_VALIDATION", "DEPENDENCY_VALIDATION",
    "CONFLICT_PRECEDENCE_VALIDATION", "MAPPING_VALIDATION", "EVIDENCE_VALIDATION",
    "ORACLE_VALIDATION", "VERIFICATION_VALIDATION", "CONFORMANCE_EVALUATION",
    "FINDING_GENERATION", "AGGREGATION", "CERTIFICATE_VALIDATION",
]
DECISION_STATES = {"UNASSESSED", "MAPPED", "VERIFIED", "CONFORMANT", "PARTIALLY_CONFORMANT", "NON_CONFORMANT", "UNVERIFIED", "NOT_APPLICABLE", "BLOCKED", "UNKNOWN"}
RELEASE_STATES = {"COMPLIANT", "CONDITIONALLY_COMPLIANT", "NON_COMPLIANT", "UNVERIFIED", "BLOCKED"}
IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]*$")
HEX_PATTERN = re.compile(r"^[A-Fa-f0-9]+$")
HASH_LENGTHS = {"SHA-256": 64, "SHA-384": 96, "SHA-512": 128}


def load(name: str, base: Path = OUT) -> Any:
    return json.loads((base / name).read_text(encoding="utf-8"))


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha_file(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def valid_timestamp(value: str) -> bool:
    if not isinstance(value, str) or not (value.endswith("Z") or re.search(r"[+-]\d{2}:\d{2}$", value)):
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed.tzinfo is not None
    except ValueError:
        return False


def valid_hash(value: Any) -> bool:
    return isinstance(value, dict) and set(value) == {"algorithm", "value"} and value.get("algorithm") in HASH_LENGTHS and isinstance(value.get("value"), str) and HEX_PATTERN.fullmatch(value["value"]) is not None and len(value["value"]) == HASH_LENGTHS[value["algorithm"]]


def valid_version_scope(value: Any) -> bool:
    if not isinstance(value, dict) or not isinstance(value.get("specification_version"), str):
        return False
    start = value.get("valid_from"); end = value.get("valid_until")
    if start is not None and not valid_timestamp(start): return False
    if end is not None and not valid_timestamp(end): return False
    if start is not None and end is not None:
        return datetime.fromisoformat(end.replace("Z", "+00:00")) >= datetime.fromisoformat(start.replace("Z", "+00:00"))
    return True


def resolve_pointer(document: Any, pointer: str) -> Any:
    node = document
    if not pointer:
        return node
    for part in pointer.lstrip("/").split("/"):
        key = part.replace("~1", "/").replace("~0", "~")
        node = node[int(key)] if isinstance(node, list) else node[key]
    return node


def schema_errors(value: Any, schema: dict[str, Any], schemas: dict[str, Any], current: str, path: str = "$") -> list[str]:
    errors: list[str] = []
    for clause in schema.get("allOf", []):
        errors.extend(schema_errors(value, clause, schemas, current, path))
    if "if" in schema and not schema_errors(value, schema["if"], schemas, current, path) and "then" in schema:
        errors.extend(schema_errors(value, schema["then"], schemas, current, path))
    if "$ref" in schema:
        target = schema["$ref"]
        file_part, _, pointer = target.partition("#")
        target_name = Path(file_part).name.replace(".schema.yaml", "") if file_part else current
        if target_name not in schemas:
            return [f"{path}: unresolved schema reference {target}"]
        try:
            resolved = resolve_pointer(schemas[target_name], pointer)
        except (KeyError, IndexError, ValueError, TypeError):
            return [f"{path}: unresolved schema pointer {target}"]
        return schema_errors(value, resolved, schemas, target_name, path)
    if "oneOf" in schema:
        results = [schema_errors(value, candidate, schemas, current, path) for candidate in schema["oneOf"]]
        if sum(not result for result in results) != 1:
            errors.append(f"{path}: expected exactly one oneOf match")
        return errors
    expected = schema.get("type")
    if expected is not None:
        expected_types = expected if isinstance(expected, list) else [expected]
        type_checks = {
            "object": lambda: isinstance(value, dict), "array": lambda: isinstance(value, list),
            "string": lambda: isinstance(value, str),
            "integer": lambda: isinstance(value, int) and not isinstance(value, bool),
            "number": lambda: isinstance(value, (int, float)) and not isinstance(value, bool),
            "boolean": lambda: isinstance(value, bool), "null": lambda: value is None,
        }
        if not any(type_checks.get(kind, lambda: False)() for kind in expected_types):
            return [f"{path}: expected type {expected}"]
    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: const mismatch")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: enum mismatch")
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0): errors.append(f"{path}: minLength")
        if "maxLength" in schema and len(value) > schema["maxLength"]: errors.append(f"{path}: maxLength")
        if "pattern" in schema and re.fullmatch(schema["pattern"], value) is None: errors.append(f"{path}: pattern")
        if schema.get("format") == "date-time" and not valid_timestamp(value): errors.append(f"{path}: date-time")
    if isinstance(value, (int, float)) and not isinstance(value, bool) and "minimum" in schema and value < schema["minimum"]:
        errors.append(f"{path}: minimum")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0): errors.append(f"{path}: minItems")
        if schema.get("uniqueItems") and len({canonical_bytes(x) for x in value}) != len(value): errors.append(f"{path}: uniqueItems")
        for index, item in enumerate(value):
            if "items" in schema: errors.extend(schema_errors(item, schema["items"], schemas, current, f"{path}[{index}]"))
    if isinstance(value, dict):
        properties = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in value: errors.append(f"{path}: missing {key}")
        if schema.get("additionalProperties") is False:
            for key in value:
                if key not in properties: errors.append(f"{path}: additional property {key}")
        for key, item in value.items():
            if key in properties: errors.extend(schema_errors(item, properties[key], schemas, current, f"{path}.{key}"))
    return errors


def collect_objects() -> list[tuple[dict[str, Any], str, str]]:
    objects: list[tuple[dict[str, Any], str, str]] = []
    audit = load("AUDIT.yaml")["objects"][0]
    objects.append((audit, "AUDIT.yaml", "/objects/0"))
    objects.append((audit["scope"], "AUDIT.yaml", "/objects/0/scope"))
    for filename in ["INPUT-ARTIFACTS.yaml", "ENVIRONMENTS.yaml", "EVIDENCE-RECORDS.yaml", "FINDINGS.yaml", "REMEDIATIONS.yaml", "AUDIT-RUNS.yaml", "AUDIT-CERTIFICATE.yaml"]:
        for index, obj in enumerate(load(filename)["objects"]):
            objects.append((obj, filename, f"/objects/{index}"))
    for filename in ["IMPLEMENTATION-ARTIFACTS.yaml", "IMPLEMENTATION-CLAIMS.yaml", "REQUIREMENT-MAPPINGS.yaml", "VERIFICATION-EXECUTIONS.yaml", "CONFORMANCE-DECISIONS.yaml", "NONCONFORMANCES.yaml", "WAIVERS.yaml"]:
        for index, obj in enumerate(load(filename)["objects"]):
            objects.append((obj, filename, f"/objects/{index}"))
    return objects


def find_references(value: Any, path: str = "$") -> list[tuple[dict[str, str], str]]:
    refs: list[tuple[dict[str, str], str]] = []
    if isinstance(value, dict):
        if set(value) == {"object_type", "object_id"} and isinstance(value.get("object_type"), str) and isinstance(value.get("object_id"), str):
            refs.append((value, path))
        else:
            for key, child in value.items(): refs.extend(find_references(child, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value): refs.extend(find_references(child, f"{path}[{index}]"))
    return refs


def main() -> int:
    checks: list[dict[str, str]] = []
    def check(cid: str, category: str, description: str, ok: bool, detail: str = "") -> None:
        checks.append({"check_id": cid, "category": category, "description": description, "result": "PASS" if ok else "FAIL", "detail": detail})
    def blocked(cid: str, category: str, description: str, detail: str) -> None:
        checks.append({"check_id": cid, "category": category, "description": description, "result": "BLOCKED", "detail": detail})

    for index, name in enumerate(DELIVERABLES, 1):
        check(f"A{index:02d}", "artifacts", f"required generator-owned artifact exists: {name}", (OUT / name).is_file())
    if any(x["result"] == "FAIL" for x in checks): return finish(checks, {})
    extension_schema_names = {"certificate-revision", "change-set", "closure-decision", "impact-assessment", "regression-scope", "remediation-action", "remediation-program", "residual-risk", "reverification-execution", "reverification-plan", "root-cause", "waiver-review"}
    visible_files = {str(p.relative_to(OUT)) for p in OUT.rglob("*") if p.is_file() and p.name not in {"VALIDATION.yaml", "VALIDATION.md", "DETERMINISM-VALIDATION.yaml", "DETERMINISM-VALIDATION.md"} and not str(p.relative_to(OUT)).startswith(("remediation/", "reports/")) and str(p.relative_to(OUT)) not in {f"schema/{name}.schema.yaml" for name in extension_schema_names}}
    check("A80", "artifacts", "generator-owned file set is exact", visible_files == set(DELIVERABLES))
    check("A81", "artifacts", "all YAML files are JSON-compatible", all(parseable(OUT / name) for name in MACHINE + SCHEMAS))

    schemas = {name: load(f"schema/{name}.schema.yaml") for name in SCHEMA_NAMES}
    common = schemas["common"]
    check("S01", "schemas", "normative schema directory is lowercase exact path", SCHEMA_DIR.name == "schema" and SCHEMA_DIR.is_dir())
    check("S02", "schemas", "one common and sixteen object schemas exist", set(schemas) == set(SCHEMA_NAMES) and len(schemas) == 17)
    check("S03", "schemas", "common schema defines all five primitives", set(common["$defs"]) == {"Identifier", "Timestamp", "Hash", "VersionScope", "Reference"})
    identifier = common["$defs"]["Identifier"]; timestamp = common["$defs"]["Timestamp"]; hash_schema = common["$defs"]["Hash"]; version_scope = common["$defs"]["VersionScope"]; reference = common["$defs"]["Reference"]
    check("S04", "schemas", "Identifier bounds and pattern are exact", identifier["minLength"] == 1 and identifier["maxLength"] == 256 and identifier["pattern"] == "^[A-Za-z0-9][A-Za-z0-9._:/-]*$")
    check("S05", "schemas", "Timestamp requires date-time and explicit timezone pattern", timestamp["format"] == "date-time" and "Z" in timestamp["pattern"] and "+-" in timestamp["pattern"])
    check("S06", "schemas", "Hash algorithms are exact", set(hash_schema["properties"]["algorithm"]["enum"]) == {"SHA-256", "SHA-384", "SHA-512"})
    check("S07", "schemas", "VersionScope requires specification version and temporal ordering", version_scope["required"] == ["specification_version"] and "valid_until MUST NOT precede valid_from" in version_scope["x-v12.1-constraint"])
    check("S08", "schemas", "Reference requires unrestricted string object type and Identifier object id", set(reference["required"]) == {"object_type", "object_id"} and reference["properties"]["object_type"] == {"type": "string"} and reference["properties"]["object_id"] == {"$ref": "common.schema.yaml#/$defs/Identifier"})
    common_fields = {"object_type", "schema_version", "object_id", "created_at"}
    check("S09", "schemas", "every normative object schema requires common fields", all(common_fields <= set(schemas[name]["required"]) for name in SCHEMA_NAMES if name != "common"))
    check("S10", "schemas", "every object schema has complete declared required properties", all(set(schemas[name]["required"]) <= set(schemas[name]["properties"]) for name in SCHEMA_NAMES if name != "common"))
    check("S11", "schemas", "every object schema forbids undocumented fields", all(schemas[name].get("additionalProperties") is False for name in SCHEMA_NAMES if name != "common"))
    check("S12", "schemas", "every object type has exactly one schema", set(SCHEMA_BY_TYPE) == OBJECT_TYPES and len(SCHEMA_BY_TYPE) == len(OBJECT_TYPES))
    all_schema_refs = [(name, target) for name, doc in schemas.items() for target in extract_schema_refs(doc)]
    unresolved_schema_refs = []
    for current, target in all_schema_refs:
        file_part, _, pointer = target.partition("#"); target_name = Path(file_part).name.replace(".schema.yaml", "") if file_part else current
        try: resolve_pointer(schemas[target_name], pointer)
        except (KeyError, IndexError, ValueError, TypeError): unresolved_schema_refs.append((current, target))
    check("S13", "schemas", "all schema references resolve", not unresolved_schema_refs, str(unresolved_schema_refs))
    registry = load("SCHEMA-REGISTRY.yaml")
    check("S14", "schemas", "schema registry has exact paths and content hashes", len(registry["schemas"]) == 17 and all(sha_file(OUT / x["path"]) == x["sha256"] for x in registry["schemas"]))
    check("S15", "schemas", "audit-scope requires a nonempty requirement array", schemas["audit-scope"]["properties"]["requirements"]["minItems"] == 1)
    check("S16", "schemas", "certificate requires specification and implementation hashes", {"specification_hash", "implementation_hash", "certificate_hash"} <= set(schemas["audit-certificate"]["required"]))
    check("S17", "schemas", "historical temporal policy is a machine condition on AUDIT", "allOf" in schemas["audit"] and "HISTORICAL audit" in schemas["audit"]["x-v12.1-temporal-rule"])

    objects = collect_objects()
    ids = [obj["object_id"] for obj, _, _ in objects]
    object_index: dict[str, list[dict[str, Any]]] = {}
    for obj, _, _ in objects: object_index.setdefault(obj["object_id"], []).append(obj)
    check("O01", "objects", "all object identifiers are globally unique", len(ids) == len(set(ids)))
    check("O02", "objects", "all object identifiers satisfy Identifier", all(isinstance(x, str) and 1 <= len(x) <= 256 and IDENTIFIER_PATTERN.fullmatch(x) for x in ids))
    check("O03", "objects", "all objects declare v12.1 and explicit timezone timestamps", all(obj["schema_version"] == VERSION and valid_timestamp(obj["created_at"]) for obj, _, _ in objects))
    check("O04", "objects", "all object types belong to the normative universe", {obj["object_type"] for obj, _, _ in objects} <= OBJECT_TYPES)
    check("O05", "objects", "object registry exactly indexes every object once", load("OBJECT-REGISTRY.yaml")["object_count"] == len(objects) and {(x["object_type"], x["object_id"], x["source_file"], x["json_pointer"]) for x in load("OBJECT-REGISTRY.yaml")["objects"]} == {(obj["object_type"], obj["object_id"], filename, pointer) for obj, filename, pointer in objects})

    validation_by_id: dict[str, list[str]] = {}
    for obj, _, _ in objects:
        validation_by_id[obj["object_id"]] = schema_errors(obj, schemas[SCHEMA_BY_TYPE[obj["object_type"]]], schemas, SCHEMA_BY_TYPE[obj["object_type"]])
    expected_invalid = {"SCOPE-V121-001", "AUDIT-OBJECT-V121-001"}
    actual_invalid = {oid for oid, errors in validation_by_id.items() if errors}
    check("O06", "objects", "only audit and nested scope are schema-invalid", actual_invalid == expected_invalid, str({k: v for k, v in validation_by_id.items() if v}))
    check("O07", "objects", "scope invalidity is exactly empty requirements", any("requirements: minItems" in x or "scope.requirements: minItems" in x for errors in validation_by_id.values() for x in errors) and all("minItems" in x for oid in expected_invalid for x in validation_by_id[oid]))
    check("O08", "objects", "no synthetic requirement repairs the rejected scope", load("AUDIT.yaml")["objects"][0]["scope"]["requirements"] == [])
    schema_validation_output = load("SCHEMA-VALIDATION.yaml")
    check("O09", "objects", "schema-validation output declares the V2 stop", schema_validation_output["status"] == "FAIL_STOP" and schema_validation_output["schema_count"] == 17)
    check("O10", "objects", "objects after the invalid audit/scope are explicitly not reached", set(schema_validation_output["objects_not_reached_due_stop"]) == set(ids) - expected_invalid)
    audit_candidate = next(obj for obj, _, _ in objects if obj["object_type"] == "AUDIT")
    historical_candidate = json.loads(json.dumps(audit_candidate)); historical_candidate["mode"] = "HISTORICAL"; historical_candidate["scope"]["requirements"] = [{"object_type": "REQUIREMENT", "object_id": "SYNTHETIC-SCHEMA-TEST"}]
    historical_candidate["scope"]["temporal_policy"] = "CURRENT"
    historical_errors = schema_errors(historical_candidate, schemas["audit"], schemas, "audit")
    historical_candidate["scope"]["temporal_policy"] = "RETROSPECTIVE"
    retrospective_errors = schema_errors(historical_candidate, schemas["audit"], schemas, "audit")
    check("O11", "objects", "historical mode rejects CURRENT and permits explicit RETROSPECTIVE policy", any("temporal_policy" in x and "enum" in x for x in historical_errors) and not retrospective_errors)
    version_scopes = [scope_value for obj, _, _ in objects for scope_value in collect_version_scopes(obj)]
    check("O12", "objects", "all emitted VersionScope values are decidable and temporal ordering rejects reversal", version_scopes and all(valid_version_scope(x) for x in version_scopes) and valid_version_scope({"specification_version": "11.1", "valid_from": "2026-01-01T00:00:00Z", "valid_until": "2026-01-02T00:00:00Z"}) and not valid_version_scope({"specification_version": "11.1", "valid_from": "2026-01-02T00:00:00Z", "valid_until": "2026-01-01T00:00:00Z"}))

    references = [(source["object_id"], target, path) for source, _, _ in objects for target, path in find_references(source)]
    unresolved = [(source, target, path) for source, target, path in references if len(object_index.get(target["object_id"], [])) != 1]
    mismatches = [(source, target, path) for source, target, path in references if len(object_index.get(target["object_id"], [])) == 1 and object_index[target["object_id"]][0]["object_type"] != target["object_type"]]
    check("R01", "references", "every Reference resolves exactly once", not unresolved, str(unresolved))
    check("R02", "references", "every Reference resolves to the declared type", not mismatches, str(mismatches))
    check("R03", "references", "reference integrity distinguishes construction from stopped V3", load("REFERENCE-INTEGRITY.yaml")["construction_integrity"] == "PASS" and load("REFERENCE-INTEGRITY.yaml")["canonical_stage_status"] == "NOT_EXECUTED_EARLY_STOP")
    audit = load("AUDIT.yaml")["objects"][0]; run = load("AUDIT-RUNS.yaml")["objects"][0]; cert = load("AUDIT-CERTIFICATE.yaml")["objects"][0]
    findings = load("FINDINGS.yaml")["objects"]; remediations = load("REMEDIATIONS.yaml")["objects"]; evidence = load("EVIDENCE-RECORDS.yaml")["objects"]
    check("R04", "references", "audit-run audit_id resolves to the declared audit", run["audit_id"] == audit["audit_id"])
    check("R05", "references", "certificate audit_id and scope resolve", cert["audit_id"] == audit["audit_id"] and cert["scope"]["object_id"] == audit["scope"]["object_id"])
    check("R06", "references", "each remediation finding_id resolves", {x["finding_id"] for x in remediations} == {x["object_id"] for x in findings})
    check("R07", "references", "every finding has resolving evidence", all(x["evidence"] and all(r["object_id"] in object_index for r in x["evidence"]) for x in findings))

    input_artifacts = load("INPUT-ARTIFACTS.yaml")["objects"]
    input_hash_errors = []
    for obj in input_artifacts:
        declared = obj["content_hash"]; unhashed = {k: v for k, v in obj.items() if k != "content_hash"}
        if not valid_hash(declared) or declared["algorithm"] != "SHA-256" or declared["value"] != sha_bytes(canonical_bytes(unhashed)):
            input_hash_errors.append(obj["object_id"])
    check("H01", "hashes", "all input object content_hash values cover canonical objects excluding the hash field", not input_hash_errors, str(input_hash_errors))
    source_errors = []
    for obj in input_artifacts:
        if obj["source_path"] == ".": continue
        source_path = ROOT / obj["source_path"]
        if not source_path.is_file() or obj["metadata"]["source_content_hash"]["value"] != sha_file(source_path): source_errors.append(obj["object_id"])
    check("H02", "hashes", "every source artifact hash matches exact source bytes", not source_errors, str(source_errors))
    cert_unhashed = {k: v for k, v in cert.items() if k != "certificate_hash"}
    check("H03", "hashes", "certificate hash covers canonical certificate excluding certificate_hash", valid_hash(cert["certificate_hash"]) and cert["certificate_hash"]["value"] == sha_bytes(canonical_bytes(cert_unhashed)))
    check("H04", "hashes", "certificate specification hash matches manifest bytes", cert["specification_hash"]["value"] == sha_file(SPEC / "SPECIFICATION-MANIFEST.yaml"))
    check("H05", "hashes", "missing implementation uses explicit deterministic sentinel hash", cert["implementation_hash"]["value"] == sha_bytes(canonical_bytes("IMPLEMENTATION_SOURCE_UNAVAILABLE")) and cert["metadata"]["implementation_hash_basis"] == "MISSING_IMPLEMENTATION_SENTINEL")
    check("H06", "hashes", "every declared Hash has legal algorithm, hex, and length", all(valid_hash(value) for obj, _, _ in objects for value in collect_hashes(obj)))

    contract = load("INPUT-CONTRACT.yaml"); report = load("VALIDATION-REPORT.yaml"); errors = load("VALIDATION-ERRORS.yaml"); pipeline = load("VALIDATION-PIPELINE.yaml")
    check("V01", "pipeline", "v11.1 rejection is validated before audit evaluation", contract["v11_1"]["manifest_status"] == "FAIL" and contract["v11_1"]["certificate_status"] == "FAIL" and contract["v11_1"]["requirement_count"] == 0)
    check("V02", "pipeline", "required implementation input is explicitly INPUT_MISSING", contract["missing_inputs"] == [{"artifact_type": "IMPLEMENTATION_SOURCE", "required": True, "failure": "INPUT_MISSING"}])
    check("V03", "pipeline", "canonical pipeline has exact V0-V16 order", [x["stage_id"] for x in pipeline["stages"]] == [f"V{i}" for i in range(17)] and [x["stage"] for x in pipeline["stages"]] == PIPELINE)
    check("V04", "pipeline", "V0 blocks conformance while permitting structural diagnostics", pipeline["stages"][0]["status"] == "BLOCKED_CONTINUE_STRUCTURAL_DIAGNOSTICS")
    check("V05", "pipeline", "V1 passes and V2 fails/stops", pipeline["stages"][1]["status"] == "PASS" and pipeline["stages"][2]["status"] == "FAIL_STOP" and pipeline["stop_stage"] == "V2")
    check("V06", "pipeline", "V3-V16 are not executed after invalid schema", all(x["status"] == "NOT_EXECUTED_EARLY_STOP" for x in pipeline["stages"][3:]))
    check("V07", "pipeline", "conformance evaluation is explicitly not performed", pipeline["conformance_evaluation_performed"] is False and run["metadata"]["conformance_evaluation_performed"] is False)
    check("V08", "pipeline", "validation report counts pipeline outcomes exactly", report["summary"] == {"pipeline_stages": 17, "executed": 3, "passed": 1, "failed": 1, "blocked": 1, "not_executed": 14, "errors": 3})
    check("V09", "pipeline", "validation errors preserve failure boundaries without implementation blame", {x["code"] for x in errors["errors"]} == {"INPUT_MISSING", "SCHEMA_VIOLATION", "SPECIFICATION_DEFECT"} and not any(x["implementation_blame"] for x in errors["errors"]))
    check("V10", "pipeline", "overall validation and release statuses are BLOCKED", report["overall_status"] == "BLOCKED_SCHEMA_INVALID_INPUT" and report["release_status"] == "BLOCKED")
    check("V11", "pipeline", "all mandatory validation outputs exist", all((OUT / name).is_file() for name in ["VALIDATION-REPORT.yaml", "VALIDATION-ERRORS.yaml", "REFERENCE-INTEGRITY.yaml", "TEMPORAL-INTEGRITY.yaml", "SCHEMA-VALIDATION.yaml", "DEPENDENCY-VALIDATION.yaml", "CONFLICT-VALIDATION.yaml", "EVIDENCE-VALIDATION.yaml", "ORACLE-VALIDATION.yaml", "VERIFICATION-VALIDATION.yaml", "CONFORMANCE-DECISIONS.yaml", "FINDINGS.yaml"]))
    domain_outputs = {name: load(name) for name in ["DEPENDENCY-VALIDATION.yaml", "CONFLICT-VALIDATION.yaml", "ORACLE-VALIDATION.yaml", "VERIFICATION-VALIDATION.yaml"]}
    check("V12", "pipeline", "dependency/conflict/oracle/verification outputs do not claim evaluation", all(x["canonical_stage_status"] == "NOT_EXECUTED_EARLY_STOP" and x["objects_evaluated"] == 0 for x in domain_outputs.values()))
    check("V12A", "pipeline", "dependency validation encodes existence, acyclicity, ordering, and constraint rules", set(domain_outputs["DEPENDENCY-VALIDATION.yaml"]["rules"]) == {"ALL_REFERENCED_REQUIREMENTS_EXIST", "REQUIRES_GRAPH_ACYCLIC", "DEPENDENCIES_EVALUATED_BEFORE_DEPENDENTS", "UNSATISFIED_MANDATORY_DEPENDENCY_CONSTRAINS_DEPENDENT"})
    check("V12B", "pipeline", "conflict validation forbids automatic nonconformance", "UNRESOLVED_CONFLICT_IS_SPECIFICATION_DEFECT_NOT_AUTOMATIC_NONCONFORMANCE" in domain_outputs["CONFLICT-VALIDATION.yaml"]["rules"])
    check("V12C", "pipeline", "oracle validation requires five validity predicates before attribution", set(domain_outputs["ORACLE-VALIDATION.yaml"]["rules"][:5]) == {"WELL_FORMED", "VERSION_COMPATIBLE", "APPLICABLE", "DECIDABLE", "TRACEABLE_TO_REQUIREMENT"})
    check("V12D", "pipeline", "verification validation rejects claim/test/coverage/interface/documentation substitutes", len(domain_outputs["VERIFICATION-VALIDATION.yaml"]["rules"]) == 7 and all("NOT_CONFORMANCE" in x for x in domain_outputs["VERIFICATION-VALIDATION.yaml"]["rules"][1:]))
    check("V12E", "pipeline", "evidence validity requires all five predicates", set(load("EVIDENCE-VALIDATION.yaml")["validity_predicates"]) == {"SOURCE_RESOLVES", "INTEGRITY_VALID", "VERSION_SCOPE_COMPATIBLE", "EVIDENCE_TYPE_APPROPRIATE", "CAPTURE_METADATA_SUFFICIENT"})
    temporal = load("TEMPORAL-INTEGRITY.yaml")
    check("V13", "temporal", "temporal audit is blocked without contamination", temporal["result"] == "BLOCKED_NO_IMPLEMENTATION_VERSION" and not temporal["future_requirement_applied"] and not temporal["future_oracle_applied"] and not temporal["future_implementation_evidence"])
    boundaries = load("FAILURE-BOUNDARIES.yaml")
    expected_effects = {"MALFORMED_INPUT": "STOP", "INVALID_SCHEMA": "STOP", "BROKEN_REFERENCE": "BLOCK_AFFECTED_OBJECTS", "TEMPORAL_CONTAMINATION": "BLOCK_AFFECTED_HISTORICAL_DECISIONS", "INVALID_REQUIREMENT": "BLOCK_CONFORMANCE_DECISION", "INVALID_ORACLE": "BLOCK_VERIFICATION_DEPENDENT_DECISION", "INVALID_EVIDENCE": "UNVERIFIED", "PROVEN_NORMATIVE_VIOLATION": "NON_CONFORMANT"}
    check("V14", "boundaries", "all eight earliest-invalid-boundary effects are exact", boundaries["earliest_invalid_boundary_rule"] is True and {x["condition"]: x["effect"] for x in boundaries["boundaries"]} == expected_effects)
    check("V15", "boundaries", "only proven normative violation supports implementation nonconformance", [x["condition"] for x in boundaries["boundaries"] if x["implementation_nonconformance_supported"]] == ["PROVEN_NORMATIVE_VIOLATION"])
    check("V16", "attribution", "six failure attribution classes remain independent", set(boundaries["attribution_classes"]) == {"SPECIFICATION_DEFECT", "VERIFICATION_DEFECT", "ORACLE_DEFECT", "MAPPING_DEFECT", "IMPLEMENTATION_DEFECT", "ENVIRONMENT_DEFECT"})

    machine = load("CONFORMANCE-STATE-MACHINE.yaml")
    transition_pairs = {(x["from"], x["to"]) for x in machine["legal_transitions"]}
    check("T01", "state-machine", "state model contains exact ten decision states", set(machine["decision_states"]) == DECISION_STATES)
    check("T02", "state-machine", "UNASSESSED is initial and MAPPED/VERIFIED are intermediate", machine["initial_state"] == "UNASSESSED" and machine["intermediate_states"] == ["MAPPED", "VERIFIED"])
    check("T03", "state-machine", "all legal transitions use defined conformance states", all(x["from"] in DECISION_STATES and x["to"] in DECISION_STATES for x in machine["legal_transitions"]))
    expected_legal = {
        ("UNASSESSED", "MAPPED"), ("UNASSESSED", "NOT_APPLICABLE"), ("UNASSESSED", "BLOCKED"), ("UNASSESSED", "UNKNOWN"),
        ("MAPPED", "VERIFIED"), ("MAPPED", "UNVERIFIED"), ("MAPPED", "BLOCKED"), ("MAPPED", "UNKNOWN"),
        ("VERIFIED", "CONFORMANT"), ("VERIFIED", "PARTIALLY_CONFORMANT"), ("VERIFIED", "NON_CONFORMANT"), ("VERIFIED", "UNVERIFIED"), ("VERIFIED", "BLOCKED"),
        ("PARTIALLY_CONFORMANT", "CONFORMANT"), ("PARTIALLY_CONFORMANT", "NON_CONFORMANT"), ("PARTIALLY_CONFORMANT", "UNVERIFIED"), ("PARTIALLY_CONFORMANT", "BLOCKED"),
        ("NON_CONFORMANT", "CONFORMANT"), ("NON_CONFORMANT", "PARTIALLY_CONFORMANT"),
        ("UNVERIFIED", "MAPPED"), ("UNVERIFIED", "VERIFIED"), ("UNVERIFIED", "BLOCKED"),
        ("BLOCKED", "UNASSESSED"), ("BLOCKED", "MAPPED"), ("BLOCKED", "VERIFIED"),
        ("UNKNOWN", "UNASSESSED"), ("UNKNOWN", "MAPPED"), ("UNKNOWN", "VERIFIED"), ("NOT_APPLICABLE", "UNASSESSED"),
    }
    check("T04", "state-machine", "legal transition relation is exact and duplicate-free", transition_pairs == expected_legal and len(transition_pairs) == len(machine["legal_transitions"]) == 29 and all(x["guard"] for x in machine["legal_transitions"]))
    expected_forbidden = {("UNVERIFIED", "CONFORMANT"), ("UNKNOWN", "CONFORMANT"), ("BLOCKED", "CONFORMANT"), ("MAPPED", "CONFORMANT"), ("UNVERIFIED", "NON_CONFORMANT"), ("UNKNOWN", "NON_CONFORMANT"), ("BLOCKED", "NON_CONFORMANT")}
    check("T05", "state-machine", "all seven direct forbidden transitions are explicit", {(x["from"], x["to"]) for x in machine["forbidden_transitions"]} == expected_forbidden)
    check("T06", "state-machine", "claims/tests/documentation cannot substitute for state transitions", set(machine["forbidden_substitutions"]) == {"IMPLEMENTED_CLAIM_TO_CONFORMANT", "TEST_PASS_TO_CONFORMANT", "DOCUMENTATION_TO_CONFORMANT"})
    waiver = machine["waiver_disposition"]
    check("T07", "state-machine", "WAIVED is disposition-only and preserves NON_CONFORMANT truth", waiver["transition_kind"] == "DISPOSITION_ONLY" and waiver["underlying_state_before"] == waiver["underlying_state_after"] == "NON_CONFORMANT" and "WAIVED" not in DECISION_STATES)
    check("T08", "state-machine", "implementation change forces impact analysis/remap/reverify/redecide", machine["reverification_rule"] == ["IMPLEMENTATION_CHANGE", "IMPACT_ANALYSIS", "INVALIDATE_AFFECTED_DECISIONS", "REMAP", "REVERIFY", "REDECIDE"])
    decision_algorithm = load("DECISION-ALGORITHM.yaml")
    check("T09", "decision", "decision precedence is exact", decision_algorithm["precedence"] == ["INVALID_INPUT", "NOT_APPLICABLE", "BLOCKED", "PROVEN_VIOLATION", "PROVEN_SATISFACTION", "PARTIAL_SATISFACTION", "UNVERIFIED", "UNKNOWN"])
    check("T10", "decision", "decision function remains deterministic", decision_algorithm["deterministic_for_identical_normalized_inputs"] is True and set(decision_algorithm["function"]) == {"NOT_APPLICABLE", "BLOCKED", "NON_CONFORMANT", "CONFORMANT", "PARTIALLY_CONFORMANT", "UNVERIFIED", "UNKNOWN"})
    invariants = load("CONFORMANCE-INVARIANTS.yaml")["invariants"]
    check("T11", "invariants", "all twenty-five normative invariants have mechanical enforcement", len(invariants) == 25 and [x["invariant_id"] for x in invariants] == [f"V121-I{i:02d}" for i in range(1, 26)] and all(x["enforcement"] == "MECHANICAL" for x in invariants))

    decisions = load("CONFORMANCE-DECISIONS.yaml")["objects"]; noncon = load("NONCONFORMANCES.yaml")["objects"]; mappings = load("REQUIREMENT-MAPPINGS.yaml")["objects"]; executions = load("VERIFICATION-EXECUTIONS.yaml")["objects"]
    check("C01", "conformance", "no decision exists without an admitted requirement", decisions == [] and report["requirements"] == 0)
    check("C02", "conformance", "no mapping or verification execution is fabricated", mappings == [] and executions == [])
    check("C03", "conformance", "absence of evidence does not fabricate nonconformance", noncon == [] and load("NONCONFORMANCES.yaml")["status"] == "NONE_PROVEN")
    check("C04", "evidence", "three evidence records retain invalid/unavailable distinctions", len(evidence) == 3 and {x["result"] for x in evidence} == {"INVALID", "UNAVAILABLE"})
    check("C05", "findings", "three failures are attributed outside implementation nonconformance", len(findings) == 3 and {x["finding_type"] for x in findings} == {"SPECIFICATION_DEFECT", "MAPPING_DEFECT", "TRACEABILITY_GAP"})
    check("C06", "remediation", "each finding has one blocked remediation requiring reverification", len(remediations) == len(findings) and all(x["status"] == "BLOCKED" and x["metadata"]["reverification_required"] for x in remediations))
    counts = load("AGGREGATION.yaml")["counts"]
    check("C07", "aggregation", "complete decision distribution is retained", set(counts) == {"conformant", "partially_conformant", "non_conformant", "unverified", "blocked", "unknown", "not_applicable"} and set(counts.values()) == {0})
    check("C08", "aggregation", "zero decisions cannot become a percentage or compliance", load("AGGREGATION.yaml")["percentage_summary"] == "FORBIDDEN" and load("AGGREGATION.yaml")["release_status"] == "BLOCKED")
    check("C08A", "aggregation", "all five audit-level release rules are explicit and PARTIALLY_COMPLIANT is forbidden", set(load("AGGREGATION.yaml")["release_rules"]) == RELEASE_STATES and "PARTIALLY_COMPLIANT" in load("AGGREGATION.yaml")["rule"])
    check("C09", "aggregation", "matrix is generated from machine decisions and remains empty-blocked", load("COMPLIANCE-MATRIX.yaml")["rows"] == [] and load("COMPLIANCE-MATRIX.yaml")["source"] == "CONFORMANCE-DECISIONS.yaml" and load("COMPLIANCE-MATRIX.yaml")["status"] == "BLOCKED")
    check("C10", "certificate", "certificate is scoped and blocked", cert["release_status"] == "BLOCKED" and cert["scope"] == {"object_type": "AUDIT_SCOPE", "object_id": "SCOPE-V121-001"})
    check("C11", "certificate", "certificate has zero requirement decisions and no waiver", cert["counts"] == counts and cert["waivers"] == [] and cert["critical_findings"] == [])
    check("C12", "certificate", "certificate limitations deny universal and future claims", any("universal" in x.lower() for x in cert["metadata"]["limitations"]) and any("future" in x.lower() for x in cert["metadata"]["limitations"]))
    check("C13", "v12-compatibility", "v12 scope view points to the one embedded normative scope", load("AUDIT-SCOPE.yaml")["scope"] == {"object_type": "AUDIT_SCOPE", "object_id": "SCOPE-V121-001"} and load("AUDIT-SCOPE.yaml")["canonical_location"] == "AUDIT.yaml#/objects/0/scope")
    check("C14", "v12-compatibility", "v12 decision and aggregation views have canonical v12.1 sources", load("COMPLIANCE-DECISIONS.yaml")["canonical_source"] == "CONFORMANCE-DECISIONS.yaml" and load("COMPLIANCE-AGGREGATION.yaml")["canonical_source"] == "AGGREGATION.yaml")
    graph_names = ["IMPLEMENTATION-GRAPH.yaml", "CONFORMANCE-GRAPH.yaml", "FINDING-GRAPH.yaml", "AUDIT-EVIDENCE-GRAPH.yaml"]
    check("C15", "v12-compatibility", "all four distinct v12 graph planes remain emitted", {load(name)["graph_type"] for name in graph_names} == {"IMPLEMENTATION_GRAPH", "CONFORMANCE_GRAPH", "FINDING_GRAPH", "AUDIT_EVIDENCE_GRAPH"})
    check("C16", "v12-compatibility", "compatibility graphs contain no decision or verification fabrication", load("CONFORMANCE-GRAPH.yaml")["nodes"] == [] and load("AUDIT-EVIDENCE-GRAPH.yaml")["decision_nodes"] == [] and load("AUDIT-EVIDENCE-GRAPH.yaml")["verification_nodes"] == [])
    check("C17", "v12-compatibility", "release gate and separate implementation-evidence plane remain blocked", load("RELEASE-GATE.yaml")["status"] == "BLOCKED" and load("IMPLEMENTATION-EVIDENCE.yaml")["status"] == "UNAVAILABLE" and load("IMPLEMENTATION-EVIDENCE.yaml")["objects"] == [])
    graph_refs_ok = True
    for name in ["FINDING-GRAPH.yaml", "AUDIT-EVIDENCE-GRAPH.yaml"]:
        graph = load(name); node_ids = {x["node_id"] for x in graph["nodes"]}; graph_refs_ok = graph_refs_ok and all(x["from"] in node_ids and x["to"] in node_ids for x in graph["edges"])
    check("C18", "v12-compatibility", "all compatibility graph edge endpoints resolve", graph_refs_ok)

    for index, name in enumerate(REPORTS, 1):
        text = (OUT / name).read_text(encoding="utf-8")
        check(f"P{index:02d}", "reports", f"report declares blocked v12.1 disposition: {name}", "v12.1" in text and "BLOCKED" in text)
    check("Q01", "hygiene", "authoritative historical/planning documents are not generator outputs", all(name not in DELIVERABLES for name in ["Userscript Discovery Prototype.md", "Continue Architecture Planning.md"]))
    check("Q02", "hygiene", "no Python caches exist", not any(HS.rglob("__pycache__")) and not any(HS.rglob("*.pyc")))
    det = load("DETERMINISM-VALIDATION.yaml") if (OUT / "DETERMINISM-VALIDATION.yaml").is_file() else {}
    check("Q03", "determinism", "all 79 generator-owned outputs regenerate byte-identically", det.get("status") == "PASS" and det.get("summary") == {"total": 79, "identical": 79, "different": 0} and {x["path"] for x in det.get("files", [])} == set(DELIVERABLES) and all(x["byte_identical"] for x in det.get("files", [])))
    check("Q04", "tools", "generic and version-pinned v12.1 entrypoints exist", all((HS / "tools" / name).is_file() for name in ["build_compliance_audit.py", "build_compliance_audit_v121.py", "validate_compliance_audit.py", "validate_compliance_audit_v121.py"]))
    blocked("GATE-V121", "acceptance", "Protocol-v12.1 compliance gate", "V2 rejects the empty audit requirement scope; v11.1 is rejected and required implementation source is missing. No requirement conformance state is authorized.")
    counts_out = {"schemas": 17, "objects": len(objects), "requirements": 0, "mappings": 0, "executions": 0, "decisions": 0, "nonconformances": 0, "findings": 3, "remediations": 3}
    return finish(checks, counts_out)


def collect_version_scopes(value: Any) -> list[dict[str, Any]]:
    scopes: list[dict[str, Any]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key in {"version_scope", "temporal_scope"} and isinstance(child, dict): scopes.append(child)
            else: scopes.extend(collect_version_scopes(child))
    elif isinstance(value, list):
        for child in value: scopes.extend(collect_version_scopes(child))
    return scopes


def collect_hashes(value: Any) -> list[dict[str, str]]:
    hashes: list[dict[str, str]] = []
    if isinstance(value, dict):
        if set(value) == {"algorithm", "value"} and value.get("algorithm") in HASH_LENGTHS:
            hashes.append(value)
        else:
            for child in value.values(): hashes.extend(collect_hashes(child))
    elif isinstance(value, list):
        for child in value: hashes.extend(collect_hashes(child))
    return hashes


def extract_schema_refs(value: Any) -> list[str]:
    refs: list[str] = []
    if isinstance(value, dict):
        if "$ref" in value: refs.append(value["$ref"])
        for child in value.values(): refs.extend(extract_schema_refs(child))
    elif isinstance(value, list):
        for child in value: refs.extend(extract_schema_refs(child))
    return refs


def parseable(path: Path) -> bool:
    try:
        json.loads(path.read_text(encoding="utf-8")); return True
    except Exception:
        return False


def finish(checks: list[dict[str, str]], counts: dict[str, int]) -> int:
    passed = sum(x["result"] == "PASS" for x in checks); failed = sum(x["result"] == "FAIL" for x in checks); blocked_count = sum(x["result"] == "BLOCKED" for x in checks)
    report = {"schema_version": VERSION, "validator": "Protocol-v12.1 independent validator", "overall_status": "FAIL" if failed else "STRUCTURAL_PASS_AUDIT_BLOCKED" if blocked_count else "PASS", "acceptance": "VALIDATION_FAILED" if failed else "BLOCKED" if blocked_count else "PASS", "summary": {"total": len(checks), "passed": passed, "failed": failed, "blocked": blocked_count}, "object_counts": counts, "checks": checks}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "VALIDATION.yaml").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    lines = ["# Protocol-v12.1 Independent Validation", "", f"**Overall:** `{report['overall_status']}`", f"**Acceptance:** `{report['acceptance']}`", f"**Checks:** {passed} PASS / {failed} FAIL / {blocked_count} BLOCKED ({len(checks)} total)", "", "Structural success validates deterministic stopping and blocked attribution; it establishes no requirement conformance or nonconformance.", "", "| ID | Category | Result | Description | Detail |", "|---|---|---|---|---|"]
    for item in checks:
        lines.append("| %s | %s | %s | %s | %s |" % (item["check_id"], item["category"], item["result"], item["description"].replace("|", "\\|"), item["detail"].replace("|", "\\|")))
    (OUT / "VALIDATION.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{passed} PASS / {failed} FAIL / {blocked_count} BLOCKED ({len(checks)} checks); {report['overall_status']}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
