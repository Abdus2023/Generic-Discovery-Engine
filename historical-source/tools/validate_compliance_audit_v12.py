#!/usr/bin/env python3
"""Independent Protocol-v12 compliance-audit validator."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
HS = ROOT / "historical-source"
SPEC = HS / "specification"
OUT = HS / "compliance"
MACHINE = ["INPUT-CONTRACT.yaml", "AUDIT.yaml", "AUDIT-SCOPE.yaml", "IMPLEMENTATION-ARTIFACTS.yaml", "IMPLEMENTATION-EVIDENCE.yaml", "IMPLEMENTATION-CLAIMS.yaml", "REQUIREMENT-MAPPINGS.yaml", "EVIDENCE-RECORDS.yaml", "VERIFICATION-EXECUTIONS.yaml", "ENVIRONMENTS.yaml", "COMPLIANCE-DECISIONS.yaml", "FINDINGS.yaml", "NONCONFORMANCES.yaml", "WAIVERS.yaml", "REMEDIATIONS.yaml", "REMEDIATION-ACTIONS.yaml", "AUDIT-RUNS.yaml", "AUDIT-CERTIFICATE.yaml", "IMPLEMENTATION-GRAPH.yaml", "CONFORMANCE-GRAPH.yaml", "FINDING-GRAPH.yaml", "AUDIT-EVIDENCE-GRAPH.yaml", "COMPLIANCE-MATRIX.yaml", "COMPLIANCE-AGGREGATION.yaml", "RELEASE-GATE.yaml"]
SCHEMA_NAMES = ["audit", "audit-scope", "implementation-artifact", "implementation-evidence", "implementation-claim", "requirement-mapping", "evidence-record", "verification-execution", "environment", "compliance-decision", "finding", "nonconformance", "waiver", "remediation", "remediation-action", "audit-run", "audit-certificate"]
SCHEMAS = [f"SCHEMA/{x}.schema.yaml" for x in SCHEMA_NAMES]
REPORTS = ["REPORTS/COMPLIANCE-MATRIX.md", "REPORTS/NONCONFORMANCES.md", "REPORTS/FINDINGS.md", "REPORTS/REMEDIATION-PLAN.md", "REPORTS/REGRESSION-REPORT.md", "REPORTS/SECURITY-AUDIT.md", "REPORTS/COMPATIBILITY-AUDIT.md", "REPORTS/TEMPORAL-AUDIT.md", "REPORTS/TRACEABILITY-AUDIT.md", "REPORTS/FINAL-COMPLIANCE-REPORT.md"]
DELIVERABLES = MACHINE + SCHEMAS + REPORTS
FAILURE_CLASSES = {"SPECIFICATION_FAILURE", "IMPLEMENTATION_FAILURE", "MAPPING_FAILURE", "ORACLE_FAILURE", "TEST_FAILURE", "HARNESS_FAILURE", "ENVIRONMENT_FAILURE", "DEPENDENCY_FAILURE", "TRACEABILITY_FAILURE", "TEMPORAL_FAILURE", "CONFIGURATION_FAILURE", "NONDETERMINISM", "RESOURCE_FAILURE", "SECURITY_FAILURE", "UNKNOWN_FAILURE"}
DECISION_STATUSES = {"CONFORMANT", "PARTIALLY_CONFORMANT", "NON_CONFORMANT", "UNVERIFIED", "NOT_APPLICABLE", "BLOCKED", "UNKNOWN"}
FINDING_TYPES = {"NON_CONFORMANCE", "SPECIFICATION_DEFECT", "VERIFICATION_DEFECT", "ORACLE_DEFECT", "MAPPING_DEFECT", "TRACEABILITY_GAP", "SECURITY_RISK", "COMPATIBILITY_RISK", "RESOURCE_RISK", "PROCESS_FAILURE", "UNKNOWN"}
ARTIFACT_TYPES = {"SOURCE_FILE", "FUNCTION", "METHOD", "TYPE", "TRAIT", "MODULE", "CONFIGURATION", "SCHEMA", "TEST", "FIXTURE", "DOCUMENTATION", "BUILD_ARTIFACT", "BINARY", "RUNTIME_TRACE", "LOG", "METRIC", "AUDIT_RECORD"}
LIFECYCLE = {"DISCOVERED", "PLANNED", "RUNNING", "COMPLETED", "BLOCKED", "FAILED", "VERIFIED", "REJECTED", "UNKNOWN"}


def load(name: str, base: Path = OUT) -> Any:
    return json.loads((base / name).read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def object_hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def schema_errors(value: Any, schema: dict[str, Any], path: str = "$") -> list[str]:
    """Validate the JSON-Schema subset emitted by the independent v12 builder."""
    errors: list[str] = []
    expected = schema.get("type")
    type_checks = {"object": lambda: isinstance(value, dict), "array": lambda: isinstance(value, list), "string": lambda: isinstance(value, str), "integer": lambda: isinstance(value, int) and not isinstance(value, bool), "number": lambda: isinstance(value, (int, float)) and not isinstance(value, bool), "boolean": lambda: isinstance(value, bool), "null": lambda: value is None}
    allowed = expected if isinstance(expected, list) else [expected]
    type_ok = expected is None or any(type_checks.get(kind, lambda: True)() for kind in allowed)
    if not type_ok: return [f"{path}: expected {expected}"]
    if "const" in schema and value != schema["const"]: errors.append(f"{path}: value does not match const")
    if "enum" in schema and value not in schema["enum"]: errors.append(f"{path}: value not in enum")
    if isinstance(value, dict):
        props = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in value: errors.append(f"{path}: missing {key}")
        if schema.get("additionalProperties") is False:
            errors.extend(f"{path}: unexpected {key}" for key in value if key not in props)
        for key, child in value.items():
            if key in props: errors.extend(schema_errors(child, props[key], f"{path}.{key}"))
    if isinstance(value, list):
        item_schema = schema.get("items")
        if item_schema:
            for i, child in enumerate(value): errors.extend(schema_errors(child, item_schema, f"{path}[{i}]"))
        if "minItems" in schema and len(value) < schema["minItems"]: errors.append(f"{path}: fewer than minItems")
        if schema.get("uniqueItems") and len({json.dumps(x, sort_keys=True) for x in value}) != len(value): errors.append(f"{path}: duplicate items")
    if isinstance(value, str) and "minLength" in schema and len(value) < schema["minLength"]: errors.append(f"{path}: shorter than minLength")
    if isinstance(value, (int, float)) and not isinstance(value, bool) and "minimum" in schema and value < schema["minimum"]: errors.append(f"{path}: below minimum")
    return errors


def main() -> int:
    checks: list[dict[str, str]] = []
    def check(cid: str, category: str, description: str, ok: bool, detail: str = "") -> None:
        checks.append({"check_id": cid, "category": category, "description": description, "result": "PASS" if ok else "FAIL", "detail": detail})
    def blocked(cid: str, category: str, description: str, detail: str) -> None:
        checks.append({"check_id": cid, "category": category, "description": description, "result": "BLOCKED", "detail": detail})

    for i, name in enumerate(DELIVERABLES, 1):
        check(f"A{i:02d}", "artifacts", f"required v12 artifact exists: {name}", (OUT / name).is_file())
    if any(x["result"] == "FAIL" for x in checks): return finish(checks, {})

    ic = load("INPUT-CONTRACT.yaml"); audit_obj = load("AUDIT.yaml"); scopes = load("AUDIT-SCOPE.yaml")["audit_scopes"]
    impl_art = load("IMPLEMENTATION-ARTIFACTS.yaml"); impl_ev = load("IMPLEMENTATION-EVIDENCE.yaml"); impl_claims = load("IMPLEMENTATION-CLAIMS.yaml"); mappings = load("REQUIREMENT-MAPPINGS.yaml")
    evidence = load("EVIDENCE-RECORDS.yaml")["evidence_records"]; verification_exec_obj = load("VERIFICATION-EXECUTIONS.yaml"); executions = verification_exec_obj["verification_executions"]; environments = load("ENVIRONMENTS.yaml")["environments"]
    decisions = load("COMPLIANCE-DECISIONS.yaml"); findings = load("FINDINGS.yaml")["findings"]; noncon = load("NONCONFORMANCES.yaml")["nonconformances"]; waivers = load("WAIVERS.yaml")["waivers"]
    remediations = load("REMEDIATIONS.yaml")["remediations"]; actions = load("REMEDIATION-ACTIONS.yaml")["remediation_actions"]; runs = load("AUDIT-RUNS.yaml")["audit_runs"]; cert = load("AUDIT-CERTIFICATE.yaml")
    impl_graph = load("IMPLEMENTATION-GRAPH.yaml"); conf_graph = load("CONFORMANCE-GRAPH.yaml"); finding_graph = load("FINDING-GRAPH.yaml"); evidence_graph = load("AUDIT-EVIDENCE-GRAPH.yaml")
    matrix = load("COMPLIANCE-MATRIX.yaml"); aggregation = load("COMPLIANCE-AGGREGATION.yaml"); release = load("RELEASE-GATE.yaml")
    spec_manifest = load("SPECIFICATION-MANIFEST.yaml", SPEC)["specification"]; spec_cert = load("SPECIFICATION-CERTIFICATE.yaml", SPEC); spec_req = load("REQUIREMENTS.yaml", SPEC); spec_validation = load("VALIDATION.yaml", SPEC)
    audits = audit_obj["audits"]; E = {x["evidence_record_id"]: x for x in evidence}; F = {x["finding_id"]: x for x in findings}; REM = {x["remediation_id"]: x for x in remediations}; ACT = {x["action_id"]: x for x in actions}; ENV = {x["environment_id"]: x for x in environments}

    # Input contract and specification validation.
    roles = {"specification_manifest", "requirements", "normative_rules", "acceptance_criteria", "test_oracles", "dependencies", "conflicts", "compatibility", "implementation_boundaries", "verification_records", "implementation_source", "test_source", "runtime_artifacts"}
    check("I01", "input", "all thirteen audit input roles are represented", {x["artifact_type"] for x in ic["required_inputs"]} == roles)
    fields = {"artifact_id", "schema_version", "content_hash", "source_path", "generated_at", "required"}
    check("I02", "input", "every input records required identity fields", all(fields <= set(x) for x in ic["required_inputs"]))
    actual = [x for x in ic["required_inputs"] if x["source_path"] != "UNKNOWN"]
    check("I03", "input", "all available input hashes match", all((ROOT / x["source_path"]).is_file() and sha(ROOT / x["source_path"]) == x["content_hash"] for x in actual))
    missing_required = [x for x in ic["required_inputs"] if x["required"] and x["state"] == "INPUT_MISSING"]
    check("I04", "input", "required implementation source is explicitly missing", len(missing_required) == 1 and missing_required[0]["artifact_type"] == "implementation_source")
    optional_missing = {x["artifact_type"] for x in ic["required_inputs"] if not x["required"] and x["state"] == "OPTIONAL_INPUT_UNAVAILABLE"}
    check("I05", "input", "optional test/runtime absence is not promoted to required failure", optional_missing == {"test_source", "runtime_artifacts"})
    check("I06", "input", "v11.1 specification is validated and rejected", ic["specification_validation"]["manifest_status"] == "FAIL" and ic["specification_validation"]["certificate_status"] == "FAIL" and ic["specification_validation"]["validator_status"] == "STRUCTURAL_PASS_INPUT_REJECTED" and not ic["specification_validation"]["normative_specification_valid"])
    check("I07", "input", "zero normative requirements are detected", ic["specification_validation"]["requirement_count"] == len(spec_req["requirements"]) == 0)
    check("I08", "input", "audit gate is closed", ic["status"] == "AUDIT_BLOCKED" and ic["derivation_gate"] == "CLOSED")
    check("I09", "input", "specification validation remains structurally successful but acceptance-rejected", spec_validation["summary"]["failed"] == 0 and spec_validation["acceptance"] == "REJECTED_INVALID_OBLIGATION_PACKAGE")
    check("I10", "input", "input checks distinguish fail, block, and optional unavailable", {x["result"] for x in ic["checks"]} == {"PASS", "FAIL", "BLOCKED", "UNAVAILABLE"})

    # Audit identity, scope, environment, and reproducibility.
    check("U01", "audit", "one full audit object is present", len(audits) == 1 and audits[0]["audit_id"] == "AUDIT-V12-001" and audits[0]["audit_version"] == "12.0" and audits[0]["mode"] == "FULL")
    check("U02", "audit", "audit planes remain independent", audit_obj["planes"] == ["NORMATIVE", "IMPLEMENTATION", "VERIFICATION", "DECISION"])
    check("U03", "audit", "audit has explicit empty requirement and decision scope", audits[0]["requirements"] == [] and audits[0]["decisions"] == [] and len(scopes) == 1 and scopes[0]["requirements"] == {"include": [], "exclude": []})
    check("U04", "audit", "scope is blocked rather than treated as universal", scopes[0]["status"] == "BLOCKED_NO_VALID_REQUIREMENTS_OR_IMPLEMENTATION" and scopes[0]["exclusions"] == [])
    check("U05", "audit", "audit references scope, findings, and certificate", audits[0]["scope"]["scope_id"] == scopes[0]["scope_id"] and set(audits[0]["findings"]) == set(F) and audits[0]["certificate_id"] == cert["certificate_id"])
    check("U06", "audit", "failure class registry is exact", set(audit_obj["failure_classes"]) == FAILURE_CLASSES)
    check("U07", "audit", "failure attribution order validates observation/oracle/spec/environment before blame", audit_obj["failure_attribution_order"] == ["DETERMINE_OBSERVATION", "DETERMINE_EXPECTED_SEMANTICS", "VALIDATE_ORACLE", "VALIDATE_SPECIFICATION", "VALIDATE_ENVIRONMENT", "ATTRIBUTE_FAILURE"])
    check("U08", "audit", "all twenty audit invariants pass via explicit gating", len(audit_obj["audit_invariants"]) == 20 and [x["invariant_id"] for x in audit_obj["audit_invariants"]] == [f"V12-I{i:02d}" for i in range(1, 21)] and all(x["status"] == "PASS" for x in audit_obj["audit_invariants"]))
    check("U09", "audit", "audit procedure is ordered and complete", [x["order"] for x in audit_obj["audit_procedure"]] == list(range(1, 15)))
    check("U10", "environment", "one explicit audit environment exists", len(ENV) == 1 and "ENV-AUDIT-001" in ENV and scopes[0]["environments"] == ["ENV-AUDIT-001"])
    check("U11", "environment", "environment configuration is hash-bound", len(ENV["ENV-AUDIT-001"]["configuration_hash"]) == 64 and ENV["ENV-AUDIT-001"]["runtime"] == "Python")
    check("U12", "run", "one blocked reproducible run exists", len(runs) == 1 and runs[0]["result"] == "BLOCKED" and runs[0]["audit_id"] == audits[0]["audit_id"])
    check("U13", "run", "run records required repeatability inputs", {"oracle_versions", "environment", "configuration_hash", "input_artifacts", "dependency_versions", "execution_parameters"} <= set(runs[0]["reproducibility"]))
    check("U14", "run", "specification and missing-implementation hashes are deterministic", runs[0]["specification_hash"] == sha(SPEC / "SPECIFICATION-MANIFEST.yaml") and runs[0]["implementation_hash"] == digest("IMPLEMENTATION_SOURCE_MISSING") and runs[0]["implementation_hash_basis"] == "MISSING_IMPLEMENTATION_SENTINEL")
    policies = audit_obj["specialized_audit_policies"]
    check("U15", "audit", "concurrency/resource/security audit domains are explicit", len(policies["concurrency"]) == 7 and len(policies["resource"]) == 6 and len(policies["security"]) == 8)
    check("U16", "audit", "resource evidence classes remain distinct", set(policies["resource_evidence_classes"]) == {"BOUND_ENFORCED", "BOUND_OBSERVED", "BOUND_DOCUMENTED"})
    check("U17", "audit", "temporal contamination classes and retrospective labeling are explicit", set(policies["temporal_failures"]) == {"TEMPORAL_MISMATCH", "FUTURE_REQUIREMENT_APPLIED", "FUTURE_ORACLE_APPLIED", "FUTURE_IMPLEMENTATION_EVIDENCE"} and "RETROSPECTIVE_NONCONFORMANCE" in policies["historical_mode_rule"])
    input_ids = {x["artifact_id"] for x in ic["required_inputs"]}
    check("U18", "references", "audit/scope/run/evidence references resolve", audits[0]["scope"]["scope_id"] in {x["scope_id"] for x in scopes} and set(scopes[0]["environments"]) <= set(ENV) and set(audits[0]["findings"]) <= set(F) and audits[0]["certificate_id"] == cert["certificate_id"] and all(set(x["evidence"]) <= set(E) for x in findings) and all(x in input_ids for x in runs[0]["reproducibility"]["input_artifacts"]) and all(x["source_ref"] in input_ids or (ROOT / x["source_ref"]).exists() for x in evidence))

    # Implementation plane: no historical/planning contamination.
    check("P01", "implementation", "no implementation artifact is fabricated", impl_art["implementation_artifacts"] == [] and impl_art["status"] == "INPUT_MISSING")
    check("P02", "implementation", "historical and planning inputs are explicitly excluded", {x["reason"] for x in impl_art["discovery"]["excluded"]} == {"DOCUMENTATION_NOT_IMPLEMENTATION", "AUTHORITATIVE_HISTORICAL_DOCUMENT_NOT_PRESENT_IMPLEMENTATION", "FUTURE_PLANNING_NOT_PRESENT_IMPLEMENTATION", "HISTORICAL_AND_DERIVED_EVIDENCE_NOT_PRESENT_IMPLEMENTATION"})
    check("P03", "implementation", "artifact type registry is complete", set(impl_art["artifact_types"]) == ARTIFACT_TYPES)
    check("P04", "implementation", "no implementation evidence or claim is invented", impl_ev["implementation_evidence"] == [] and impl_claims["implementation_claims"] == [])
    check("P05", "implementation", "claims remain distinct from decisions", impl_claims["rule"] == "Claims are not compliance decisions.")
    check("P06", "mapping", "no mapping implies conformance", mappings["requirement_mappings"] == [] and mappings["status"] == "BLOCKED" and "No mapping implies" in mappings["rule"])

    # Verification/decision semantics and absence of false nonconformance.
    check("D01", "decision", "no verification execution is fabricated", executions == [])
    check("D02", "decision", "no compliance decision exists without requirement", decisions["compliance_decisions"] == [] and set(decisions["decision_statuses"]) == DECISION_STATUSES)
    check("D03", "decision", "no absence-of-evidence nonconformance is fabricated", noncon == [] and "No violated normative condition" in load("NONCONFORMANCES.yaml")["reason"])
    check("D04", "decision", "UNVERIFIED, UNKNOWN, BLOCKED and NON_CONFORMANT remain distinct", {"UNVERIFIED", "UNKNOWN", "BLOCKED", "NON_CONFORMANT"} <= set(decisions["decision_statuses"]))
    check("D05", "decision", "no NOT_APPLICABLE assertion is fabricated", not any(x["status"] == "NOT_APPLICABLE" for x in decisions["compliance_decisions"]))
    check("D06", "decision", "no waiver rewrites requirements", waivers == [] and "never modifies" in load("WAIVERS.yaml")["rule"])
    state_machine = decisions["conformance_state_machine"]
    check("D07", "decision", "conformance state machine keeps progression and terminal decisions distinct", state_machine["progression"] == ["UNASSESSED", "MAPPED", "VERIFIED"] and set(state_machine["decision_states"]) == {"CONFORMANT", "PARTIALLY_CONFORMANT", "NON_CONFORMANT"} and set(state_machine["alternative_terminal_states"]) == {"BLOCKED", "UNVERIFIED", "NOT_APPLICABLE", "UNKNOWN"})
    check("D08", "decision", "decision rules require evidence and violated semantics", len(decisions["decision_rules"]["CONFORMANT"]) == 7 and "actual violated normative condition" in decisions["decision_rules"]["NON_CONFORMANT"])
    check("D09", "verification", "flaky success cannot establish conformance", verification_exec_obj["flaky_verification_policy"]["classification"] == "FLAKY_VERIFICATION" and verification_exec_obj["flaky_verification_policy"]["intermittent_success_implies_conformance"] is False)
    check("D10", "verification", "deterministic audit input tuple is explicit", verification_exec_obj["deterministic_audit_inputs"] == ["specification", "implementation", "environment", "inputs", "oracle"])

    # Evidence-backed findings and remediation.
    check("F01", "findings", "three appropriately typed findings exist", len(F) == 3 and {x["finding_type"] for x in F.values()} == {"PROCESS_FAILURE", "MAPPING_DEFECT", "TRACEABILITY_GAP"})
    check("F02", "findings", "every finding has resolving evidence", all(x["evidence"] and set(x["evidence"]) <= set(E) for x in F.values()))
    check("F03", "findings", "no finding is mislabeled implementation defect/nonconformance", not any(x["finding_type"] == "NON_CONFORMANCE" for x in F.values()))
    check("F04", "evidence", "three audit evidence records are explicit", len(E) == 3 and {x["result"] for x in E.values()} == {"INVALID", "UNAVAILABLE"})
    check("F05", "evidence", "evidence distinguishes specification, implementation, and requirement absence", {x["evidence_record_id"] for x in evidence} == {"EVIDREC-V12-SPEC", "EVIDREC-V12-IMPL", "EVIDREC-V12-REQ"})
    check("F06", "remediation", "every finding has one remediation", len(REM) == len(F) and {x["finding_id"] for x in REM.values()} == set(F))
    check("F07", "remediation", "every remediation action resolves and remains blocked", set(a for x in REM.values() for a in x["actions"]) == set(ACT) and all(x["status"] == "BLOCKED" and x["verification"]["required"] for x in REM.values()))
    check("F08", "remediation", "no remediation is called complete before reverification", not any(x["status"] in {"COMPLETED", "VERIFIED"} for x in REM.values()))
    check("F09", "remediation", "actions do not invent implementation boundaries/oracles", all(not x["implementation_boundary"] and not x["verification"]["oracle_ids"] for x in ACT.values()))

    # Compliance matrix, aggregation, release, specialized status.
    check("C01", "compliance", "compliance matrix is generated from empty machine decisions", matrix["rows"] == [] and matrix["status"] == "BLOCKED" and matrix["source"] == "machine-readable audit registries")
    expected_aggregation = {"MANDATORY_CONFORMANT", "MANDATORY_PARTIAL", "MANDATORY_NON_CONFORMANT", "MANDATORY_UNVERIFIED", "MANDATORY_BLOCKED", "OPTIONAL_CONFORMANT", "OPTIONAL_NON_CONFORMANT", "NOT_APPLICABLE", "UNKNOWN"}
    check("C02", "compliance", "all aggregation classes are independently represented", set(aggregation["counts"]) == expected_aggregation and set(aggregation["counts"].values()) == {0})
    check("C03", "compliance", "zero counts are not presented as percentage/compliance", aggregation["status"] == "BLOCKED_NO_REQUIREMENTS" and aggregation["percentage_only_summary"] == "FORBIDDEN")
    check("C04", "release", "release gate remains blocked", release["status"] == "BLOCKED" and release["waiver_count"] == 0)
    check("C05", "release", "default compliant rule is retained but not satisfied", "all mandatory requirements CONFORMANT" in release["default_compliant_rule"])

    # Four explicit, distinct graphs.
    check("G01", "graphs", "implementation graph is distinct and empty", impl_graph["graph_type"] == "IMPLEMENTATION_GRAPH" and not impl_graph["nodes"] and not impl_graph["edges"])
    check("G02", "graphs", "conformance graph is distinct and blocked", conf_graph["graph_type"] == "CONFORMANCE_GRAPH" and conf_graph["status"] == "BLOCKED_NO_REQUIREMENTS" and not conf_graph["nodes"])
    check("G03", "graphs", "finding graph links findings, remediation, actions, and re-audit", finding_graph["graph_type"] == "FINDING_GRAPH" and {x["relation"] for x in finding_graph["edges"]} == {"REMEDIATED_BY", "HAS_ACTION", "REQUIRES_REAUDIT"})
    check("G04", "graphs", "audit evidence graph has no fabricated decision/verification node", evidence_graph["graph_type"] == "AUDIT_EVIDENCE_GRAPH" and evidence_graph["decision_nodes"] == [] and evidence_graph["verification_nodes"] == [])
    check("G05", "graphs", "all finding graph references resolve", all(x["node_id"] in {n["node_id"] for n in finding_graph["nodes"]} for edge in finding_graph["edges"] for x in [{"node_id": edge["from"]}, {"node_id": edge["to"]}]))
    check("G06", "graphs", "all evidence graph references resolve", all(edge["from"] in {n["node_id"] for n in evidence_graph["nodes"]} and edge["to"] in {n["node_id"] for n in evidence_graph["nodes"]} for edge in evidence_graph["edges"]))

    # Certificate semantics.
    copy = {k: v for k, v in cert.items() if k != "certificate_hash"}
    check("K01", "certificate", "certificate hash is valid", cert["certificate_hash"] == object_hash(copy))
    check("K02", "certificate", "certificate identifies exact audit and scope", cert["certificate_id"] == audits[0]["certificate_id"] and cert["audit_id"] == audits[0]["audit_id"] and cert["scope_id"] == scopes[0]["scope_id"])
    check("K03", "certificate", "certificate is BLOCKED rather than compliant", cert["status"] == "BLOCKED" and cert["lifecycle_status"] == "BLOCKED")
    check("K04", "certificate", "all decision counts are zero without overclaim", set(cert["counts"]) == {"conformant", "partial", "non_conformant", "unverified", "blocked", "not_applicable", "unknown"} and set(cert["counts"].values()) == {0})
    check("K05", "certificate", "certificate hashes agree with run", cert["specification_hash"] == runs[0]["specification_hash"] and cert["implementation_hash"] == runs[0]["implementation_hash"])
    check("K06", "certificate", "integrity dimensions remain independently blocked/partial", cert["temporal_integrity"] == "BLOCKED_NO_IMPLEMENTATION_VERSION" and cert["traceability_integrity"] == "PARTIAL_TO_OBLIGATION" and cert["verification_integrity"] == "BLOCKED_NO_REQUIREMENTS_OR_ORACLES")
    check("K07", "certificate", "certificate does not imply universal safety", len(cert["limitations"]) == 4 and any("universal safety" in x for x in cert["limitations"]))
    check("K08", "certificate", "generated time is explicit deterministic unknown", cert["generated_at"] == "UNKNOWN_NOT_RECORDED_DETERMINISTIC_BUILD")

    # Complete schema registry and object identity.
    schemas = {x: load(f"SCHEMA/{x}.schema.yaml") for x in SCHEMA_NAMES}
    check("S01", "schemas", "all seventeen dedicated schemas exist", len(schemas) == 17 and set(schemas) == set(SCHEMA_NAMES))
    check("S02", "schemas", "all schemas declare version 1.0", all(x["schema_version"] == "1.0" for x in schemas.values()))
    check("S03", "schemas", "every object schema requires type/version/lifecycle/provenance", all({"object_type", "schema_version", "lifecycle_status", "provenance"} <= set(x["required"]) for x in schemas.values()))
    check("S04", "schemas", "audit certificate status enum is exact", set(schemas["audit-certificate"]["properties"]["status"]["enum"]) == {"COMPLIANT", "CONDITIONALLY_COMPLIANT", "NON_COMPLIANT", "UNVERIFIED", "BLOCKED"})
    check("S05", "schemas", "decision status/confidence axes are independent", set(schemas["compliance-decision"]["properties"]["status"]["enum"]) == DECISION_STATUSES and "confidence" in schemas["compliance-decision"]["properties"])
    instantiated = audits + scopes + environments + evidence + findings + remediations + actions + runs + [cert]
    id_fields = {"AUDIT": "audit_id", "AUDIT_SCOPE": "scope_id", "ENVIRONMENT": "environment_id", "EVIDENCE_RECORD": "evidence_record_id", "AUDIT_FINDING": "finding_id", "REMEDIATION": "remediation_id", "REMEDIATION_ACTION": "action_id", "AUDIT_RUN": "audit_run_id", "AUDIT_CERTIFICATE": "certificate_id"}
    ids = [x[id_fields[x["object_type"]]] for x in instantiated]
    check("S06", "schemas", "all instantiated object identities are globally unique", len(ids) == len(set(ids)))
    check("S07", "schemas", "all instantiated objects carry common metadata", all(x["schema_version"] == "1.0" and x["lifecycle_status"] in LIFECYCLE and x["provenance"] for x in instantiated))
    schema_by_type = {"AUDIT": "audit", "AUDIT_SCOPE": "audit-scope", "IMPLEMENTATION_ARTIFACT": "implementation-artifact", "IMPLEMENTATION_EVIDENCE": "implementation-evidence", "IMPLEMENTATION_CLAIM": "implementation-claim", "REQUIREMENT_MAPPING": "requirement-mapping", "EVIDENCE_RECORD": "evidence-record", "VERIFICATION_EXECUTION": "verification-execution", "ENVIRONMENT": "environment", "COMPLIANCE_DECISION": "compliance-decision", "AUDIT_FINDING": "finding", "NONCONFORMANCE": "nonconformance", "WAIVER": "waiver", "REMEDIATION": "remediation", "REMEDIATION_ACTION": "remediation-action", "AUDIT_RUN": "audit-run", "AUDIT_CERTIFICATE": "audit-certificate"}
    instantiated_errors = [(x[id_fields[x["object_type"]]], schema_errors(x, schemas[schema_by_type[x["object_type"]]])) for x in instantiated]
    check("S08", "schemas", "every instantiated v12 object validates against its dedicated schema", all(not errors for _, errors in instantiated_errors), "; ".join(f"{oid}: {errors[0]}" for oid, errors in instantiated_errors if errors))
    check("S09", "schemas", "all required schema fields have declared definitions", all(set(x["required"]) <= set(x["properties"]) for x in schemas.values()))

    # Reports, determinism, and hygiene.
    for i, name in enumerate(REPORTS, 1):
        check(f"R{i:02d}", "reports", f"report preserves blocked disposition: {name}", "Audit status: BLOCKED" in (OUT / name).read_text(encoding="utf-8"))
    check("H01", "hygiene", "all machine/schema YAML is JSON-compatible", all(parseable(OUT / x) for x in MACHINE + SCHEMAS))
    check("H02", "hygiene", "authoritative documents are not generator outputs", all("Userscript Discovery Prototype.md" not in x and "Continue Architecture Planning.md" not in x for x in DELIVERABLES))
    check("H03", "hygiene", "no Python cache artifacts exist", not any(HS.rglob("__pycache__")) and not any(HS.rglob("*.pyc")))
    det = load("DETERMINISM-VALIDATION.yaml") if (OUT / "DETERMINISM-VALIDATION.yaml").is_file() else {}
    check("H04", "hygiene", "all generator-owned outputs reproduce byte-for-byte", det.get("status") == "PASS" and det.get("summary", {}).get("total") == len(DELIVERABLES) and det.get("summary", {}).get("identical") == len(DELIVERABLES) and {x["path"] for x in det.get("files", [])} == set(DELIVERABLES))
    check("H05", "hygiene", "generator and validator exist", (HS / "tools/build_compliance_audit.py").is_file() and (HS / "tools/validate_compliance_audit.py").is_file())
    blocked("GATE-V12", "acceptance", "v12 compliance/release decision", "No accepted normative specification and no present implementation source are available; audit certificate remains BLOCKED.")
    counts = {"requirements": 0, "implementation_artifacts": 0, "implementation_evidence": 0, "mappings": 0, "executions": 0, "decisions": 0, "findings": len(F), "nonconformances": 0, "waivers": 0, "remediations": len(REM)}
    return finish(checks, counts)


def parseable(path: Path) -> bool:
    try: json.loads(path.read_text(encoding="utf-8")); return True
    except Exception: return False


def finish(checks: list[dict[str, str]], counts: dict[str, int]) -> int:
    passed = sum(x["result"] == "PASS" for x in checks); failed = sum(x["result"] == "FAIL" for x in checks); blocked = sum(x["result"] == "BLOCKED" for x in checks)
    report = {"schema_version": "1.0", "audit_version": "12.0", "overall_status": "FAIL" if failed else "STRUCTURAL_PASS_AUDIT_BLOCKED" if blocked else "PASS", "acceptance": "VALIDATION_FAILED" if failed else "BLOCKED" if blocked else "PASS", "summary": {"total": len(checks), "passed": passed, "failed": failed, "blocked": blocked}, "object_counts": counts, "checks": checks}
    OUT.mkdir(parents=True, exist_ok=True); (OUT / "VALIDATION.yaml").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    lines = ["# Protocol-v12 Validation", "", f"**Overall:** `{report['overall_status']}`", f"**Acceptance:** `{report['acceptance']}`", f"**Checks:** {passed} PASS / {failed} FAIL / {blocked} BLOCKED ({len(checks)} total)", "", "Structural success validates the blocked audit and failure attribution. It does not assert implementation conformance or nonconformance.", "", "| ID | Category | Result | Description | Detail |", "|---|---|---|---|---|"]
    for x in checks: lines.append("| %s | %s | %s | %s | %s |" % (x["check_id"], x["category"], x["result"], x["description"].replace("|", "\\|"), x["detail"].replace("|", "\\|")))
    (OUT / "VALIDATION.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{passed} PASS / {failed} FAIL / {blocked} BLOCKED ({len(checks)} checks); {report['overall_status']}")
    return 1 if failed else 0


if __name__ == "__main__": sys.exit(main())
