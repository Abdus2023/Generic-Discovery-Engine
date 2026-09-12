#!/usr/bin/env python3
"""Independent validator for v14.7-R3 executable boundary contracts."""
import ast
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HISTORICAL = ROOT / "historical-source"
COMPLIANCE = HISTORICAL / "compliance"
DESTINATION = COMPLIANCE / "certification/v14.7-R3"
sys.path.insert(0, str(HISTORICAL / "tools"))

from run_v147r3_boundary import run
from v147r3_boundary_contracts import (
    CLASSIFICATIONS,
    CONFORMANCE_RESULTS,
    ERROR_DOMAINS,
    LAYERS,
    RECOVERABILITY,
    VALIDATION_RESULTS,
    object_hash,
)

VERSION = "14.7-R3"


def load(path):
    return json.loads(path.read_text())


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def constant(name):
    tree = ast.parse((HISTORICAL / "tools/build_executable_boundary_contracts_v147r3.py").read_text())
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id == name:
            return ast.literal_eval(node.value)
    raise KeyError(name)


def valid_hash(domain, value):
    return value.get("content_hash") == object_hash(domain, value)


def exact_shape(schema, value):
    return set(value) == set(schema["properties"]) and set(schema["required"]) <= set(value)


def main():
    checks = []

    def check(identifier, category, description, condition, detail=""):
        checks.append({
            "check_id": identifier,
            "category": category,
            "result": "PASS" if condition else "FAIL",
            "description": description,
            "detail": detail,
        })

    files = constant("FILES")
    schemas = constant("SCHEMAS")
    owned = files + [f"schema/{name}.schema.yaml" for name in schemas] + ["SPECIFICATION.md"]
    check("I01", "inventory", "57 generator-owned artifacts exist", len(owned) == 57 and all((DESTINATION / path).is_file() for path in owned))
    parse_errors = []
    for path in DESTINATION.rglob("*.yaml"):
        try:
            load(path)
        except Exception as error:
            parse_errors.append(f"{path}:{error}")
    check("I02", "inventory", "all JSON-compatible YAML parses", not parse_errors, ";".join(parse_errors))
    validation_extras = {"VALIDATION.yaml", "VALIDATION.md", "DETERMINISM-VALIDATION.yaml", "REGRESSION-VALIDATION.yaml"}
    actual = {str(path.relative_to(DESTINATION)) for path in DESTINATION.rglob("*") if path.is_file()} - validation_extras
    check("I03", "inventory", "no undeclared generator artifact", actual == set(owned), str(sorted(actual ^ set(owned))))

    version = load(DESTINATION / "VERSION.yaml")
    executive = load(DESTINATION / "EXECUTIVE-RESULT.yaml")
    check("V01", "version", "R3 is an implementation-realization refinement, not a semantic revision",
          version["realization_version"] == VERSION and version["semantic_version"] == "v14.7" and
          version["refines"] == ["v14.7-R2", "v14.7-R2.1"] and not version["new_normative_states"] and
          not version["renamed_semantic_states"] and not version["weakened_requirement_semantics"] and
          not version["new_semantic_layer"] and not executive["semantic_revision"])
    check("V02", "version", "reference boundary and target implementation claims remain separate",
          executive["reference_boundary_conformance"] == "CONFORMANT" and executive["target_implementation_conformance"] == "UNVERIFIED")

    basis = load(DESTINATION / "SPECIFICATION-BASIS.yaml")
    check("B01", "basis", "specification basis is self-hashed and binds all exact components",
          valid_hash("R3_SPECIFICATION_BASIS", basis) and len(basis["components"]) == 3 and
          all(sha256(DESTINATION / item["path"]) == item["sha256"] for item in basis["components"]))
    check("B02", "basis", "basis explicitly preserves semantic states and requirement strength",
          not basis["new_normative_states"] and not basis["renamed_semantic_states"] and not basis["weakened_requirements"])
    profile = load(DESTINATION / "PROFILE-REFERENCE.yaml")
    predecessor_profile = load(DESTINATION / profile["artifact_path"])
    check("B03", "basis", "R3 binds the immutable R2.1 profile without profile changes",
          valid_hash("R3_PROFILE_REFERENCE", profile) and profile["profile_id"] == predecessor_profile["profile_id"] and
          profile["profile_version"] == predecessor_profile["profile_version"] and
          profile["profile_content_hash"] == predecessor_profile["content_hash"] and
          profile["artifact_sha256"] == sha256(DESTINATION / profile["artifact_path"]) and profile["profile_changes"] == "NONE" and
          profile["compatibility_with_r2_1_profile"] == "IDENTICAL")

    registry = load(DESTINATION / "SCHEMA-REGISTRY.yaml")
    check("S01", "schema", "13 local schemas extend the exact 67-schema predecessor registry",
          len(registry["local"]) == 13 and registry["predecessor"]["count"] == 67 and registry["effective_count"] == 80 and
          sha256(DESTINATION / registry["predecessor"]["path"]) == registry["predecessor"]["sha256"])
    metadata = {"$schema", "$id", "title", "type", "required", "properties", "additionalProperties",
                "x-identity-fields", "x-immutable", "x-self-excluding-hash-field", "x-canonical-profile",
                "x-authority-precedence", "x-normative-rules"}
    schema_ok = True
    for entry in registry["local"]:
        schema = load(DESTINATION / entry["path"])
        schema_ok &= (sha256(DESTINATION / entry["path"]) == entry["sha256"] and metadata <= set(schema) and
                      schema["type"] == "object" and schema["additionalProperties"] is False and schema["x-immutable"] and
                      schema["x-authority-precedence"] == ["SPECIFICATION", "PROFILE", "IMPLEMENTATION", "EVIDENCE"] and
                      set(schema["required"]) <= set(schema["properties"]) and "content_hash" in schema["required"])
    check("S02", "schema", "all schemas are strict, immutable, authority-aware, and hash-bound", schema_ok)
    boundary_schema = load(DESTINATION / "schema/boundary-binding.schema.yaml")
    criterion_contract_schema = load(DESTINATION / "schema/acceptance-criterion.schema.yaml")
    evidence_contract_schema = load(DESTINATION / "schema/evidence.schema.yaml")
    validation_contract_schema = load(DESTINATION / "schema/validation-contract.schema.yaml")
    check("S03", "schema", "nested claim, oracle, evidence-integrity, and validation domains are closed and exact",
          boundary_schema["properties"]["claims"]["items"]["additionalProperties"] is False and
          criterion_contract_schema["properties"]["oracle"]["properties"]["expected_result"]["enum"] == ["TRUE", "FALSE", "UNKNOWN", "BLOCKED", "INVALID"] and
          evidence_contract_schema["properties"]["integrity"]["properties"]["status"]["enum"] == ["VALID", "INVALID", "UNKNOWN"] and
          validation_contract_schema["properties"]["output"]["properties"]["states"]["items"]["enum"] == ["VALID", "INVALID", "BLOCKED", "UNKNOWN"])

    binding_document = load(DESTINATION / "BOUNDARY-BINDINGS.yaml")
    bindings = binding_document["objects"]
    declared_with_validation = set(owned) | validation_extras
    binding_schema = load(DESTINATION / "schema/boundary-binding.schema.yaml")
    check("A01", "authority", "every declared artifact has exactly one BoundaryBinding",
          binding_document["covers_declared_artifacts"] and len(bindings) == len(declared_with_validation) and
          {item["subject_ref"] for item in bindings} == declared_with_validation and
          len({item["subject_ref"] for item in bindings}) == len(bindings))
    check("A02", "authority", "every BoundaryBinding is exact, hash-valid, and names one authority layer",
          all(exact_shape(binding_schema, item) and valid_hash("BOUNDARY_BINDING", item) and
              item["authority"]["layer"] in LAYERS and item["authority"]["ref"] and item["claims"] and item["satisfies"]
              for item in bindings))
    precedence = load(DESTINATION / "AUTHORITY-PRECEDENCE.yaml")
    check("A03", "authority", "authority precedence is strict and evidence has no normative authority",
          precedence["order"] == ["SPECIFICATION", "PROFILE", "IMPLEMENTATION", "EVIDENCE"] and
          precedence["lower_layer_override"] == "FORBIDDEN" and precedence["evidence_normative_authority"] is False)

    classifications = load(DESTINATION / "STATEMENT-CLASSIFICATION.yaml")
    classification_schema = load(DESTINATION / "schema/statement-classification.schema.yaml")
    specification_lines = (DESTINATION / "SPECIFICATION.md").read_text().splitlines()
    extracted = [specification_lines[index + 1] for index, line in enumerate(specification_lines) if line.startswith("## ")]
    check("C01", "classification", "all 31 extracted section statements have exactly one permitted classification",
          classifications["classification_cardinality"] == "EXACTLY_ONE" and classifications["source_sections"] == list(range(1, 32)) and
          len(classifications["objects"]) == 31 and [item["statement"] for item in classifications["objects"]] == extracted and
          all(item["classification"] in CLASSIFICATIONS for item in classifications["objects"]))
    check("C02", "classification", "classification inventory uses every required category and has valid hashes",
          {item["classification"] for item in classifications["objects"]} == set(CLASSIFICATIONS) and
          all(exact_shape(classification_schema, item) and valid_hash("STATEMENT_CLASSIFICATION", item) for item in classifications["objects"]))

    requirements = load(DESTINATION / "NORMATIVE-REQUIREMENTS.yaml")["objects"]
    requirement_schema = load(DESTINATION / "schema/normative-requirement.schema.yaml")
    concrete = re.compile(r"\b(SQLite|PostgreSQL|Tokio|Rust crate|sha2 crate|ring crate)\b", re.I)
    check("R01", "requirements", "24 exact, hash-bound normative requirements have specification authority",
          len(requirements) == 24 and [item["requirement_id"] for item in requirements] == [f"R3-REQ-{i:03d}" for i in range(1, 25)] and
          all(exact_shape(requirement_schema, item) and valid_hash("NORMATIVE_REQUIREMENT", item) and
              item["authority"]["layer"] == "SPECIFICATION" for item in requirements))
    check("R02", "requirements", "normative requirement statements contain no concrete implementation mechanism",
          all(not concrete.search(item["statement"]) for item in requirements))
    criteria = load(DESTINATION / "ACCEPTANCE-CRITERIA.yaml")["objects"]
    criterion_schema = load(DESTINATION / "schema/acceptance-criterion.schema.yaml")
    check("R03", "requirements", "every requirement has one exact criterion with a frozen evaluation oracle",
          len(criteria) == 24 and {item["requirement_ref"] for item in criteria} == {item["requirement_id"] for item in requirements} and
          all(exact_shape(criterion_schema, item) and valid_hash("ACCEPTANCE_CRITERION", item) and
              item["oracle"]["expected_result"] in ["TRUE", "FALSE", "UNKNOWN", "BLOCKED", "INVALID"]
              for item in criteria))

    profile_bindings = load(DESTINATION / "PROFILE-BINDINGS.yaml")["objects"]
    profile_binding_schema = load(DESTINATION / "schema/profile-binding-r3.schema.yaml")
    check("P01", "profile", "every requirement has exactly one semantic-preserving profile binding",
          len(profile_bindings) == 24 and {item["requirement_ref"] for item in profile_bindings} == {item["requirement_id"] for item in requirements} and
          all(exact_shape(profile_binding_schema, item) and valid_hash("PROFILE_BINDING_R3", item) and
              item["semantic_preservation"]["claim"] == "NO_STATE_ADDED_RENAMED_OR_WEAKENED" and
              item["profile_ref"] == f'{profile["profile_id"]}@{profile["profile_version"]}' for item in profile_bindings))
    freeze = load(DESTINATION / "PROFILE-FREEZE-AUDIT.yaml")
    check("P02", "profile", "freeze audit detects no implicit defaults, leakage, or unstated binding",
          freeze["result"] == "FROZEN" and all(value is True for key, value in freeze["checks"].items() if isinstance(value, bool)) and
          all(value == 0 for key, value in freeze["checks"].items() if isinstance(value, int) and not isinstance(value, bool)))
    separation = load(DESTINATION / "PROFILE-IMPLEMENTATION-TEST.yaml")
    check("P03", "profile", "profile-changing mechanisms and interchangeable libraries are distinguished",
          separation["yes"] == "PROFILE_OR_SPECIFICATION" and separation["no"] == "IMPLEMENTATION_DETAIL" and
          separation["examples"][0]["version_required"] and not separation["examples"][1]["version_required"])

    mappings = load(DESTINATION / "IMPLEMENTATION-MAPPINGS.yaml")["objects"]
    mapping_schema = load(DESTINATION / "schema/implementation-mapping.schema.yaml")
    check("M01", "mapping", "every profile binding has one typed implementation mapping distinct from its requirement",
          len(mappings) == 24 and {item["profile_binding_ref"] for item in mappings} == {item["binding_id"] for item in profile_bindings} and
          all(exact_shape(mapping_schema, item) and valid_hash("IMPLEMENTATION_MAPPING", item) and item["mapping_type"] in
              ["DIRECT", "INDIRECT", "DISTRIBUTED", "CONFIGURATION", "RUNTIME", "TEST_ONLY"] for item in mappings) and
          not load(DESTINATION / "IMPLEMENTATION-MAPPINGS.yaml")["mapping_is_requirement"])
    matrix = load(DESTINATION / "REQUIREMENT-IMPLEMENTATION-MATRIX.yaml")
    check("M02", "mapping", "five-row matrix is explicitly non-normative and not production conformance",
          len(matrix["rows"]) == 5 and matrix["normative_authority"] is False and
          matrix["status"] == "TRACEABILITY_EXAMPLE_NOT_PRODUCTION_CONFORMANCE")

    evidence = load(DESTINATION / "EVIDENCE.yaml")["objects"]
    evidence_schema = load(DESTINATION / "schema/evidence.schema.yaml")
    evidence_ok = True
    for item in evidence:
        source_test = item["source"]["ref"].split("#", 1)[1]
        observed = next(row for row in load(DESTINATION / "MACHINE-TEST-RESULTS.yaml")["objects"] if row["test_id"] == source_test)
        body = {"test_id": source_test, "actual": observed["actual"], "status": observed["status"]}
        expected_integrity = hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()
        evidence_ok &= (exact_shape(evidence_schema, item) and valid_hash("EVIDENCE", item) and item["subject_ref"] and
                        item["integrity"] == {"hash": expected_integrity, "status": "VALID"})
    check("E01", "evidence", "24 descriptive evidence objects bind exact observed test results and valid integrity", len(evidence) == 24 and evidence_ok)
    check("E02", "evidence", "evidence is explicitly descriptive and non-normative",
          load(DESTINATION / "EVIDENCE.yaml")["normative_authority"] is False and
          load(DESTINATION / "AUTHORITY-PRECEDENCE.yaml")["evidence_normative_authority"] is False)
    validation_results_document = load(DESTINATION / "VALIDATION-RESULTS.yaml")
    evaluation_results_document = load(DESTINATION / "EVALUATION-RESULTS.yaml")
    validation_results = validation_results_document["objects"]
    evaluation_results = evaluation_results_document["objects"]
    predecessor_validation_schema = load(DESTINATION / "../v14.7-R2.1/schema/validation-result.schema.yaml")
    predecessor_evaluation_schema = load(DESTINATION / "../v14.7-R2.1/schema/evaluation-result.schema.yaml")
    check("E03", "evidence", "24 hash-bound ValidationResults use only the validation domain and do not claim semantic truth",
          len(validation_results) == 24 and not validation_results_document["semantic_truth_claim"] and
          all(exact_shape(predecessor_validation_schema, item) and valid_hash("R3_VALIDATION_RESULT", item) and
              item["status"] == "VALID" and item["subject_ref"] in {e["evidence_id"] for e in evidence}
              for item in validation_results))
    check("E04", "evidence", "24 hash-bound EvaluationResults reference criteria and do not claim conformance",
          len(evaluation_results) == 24 and not evaluation_results_document["conformance_claim"] and
          all(exact_shape(predecessor_evaluation_schema, item) and valid_hash("R3_EVALUATION_RESULT", item) and
              item["status"] == "TRUE" and item["proposition_ref"] in {c["criterion_id"] for c in criteria}
              for item in evaluation_results))

    trace = load(DESTINATION / "COMPLETE-TRACEABILITY.yaml")
    trace_rows = trace["objects"]
    check("T01", "traceability", "complete nine-stage executable chain and extended result flow are explicit",
          trace["chain"] == ["REQUIREMENT", "ACCEPTANCE_CRITERION", "PROFILE_BINDING", "IMPLEMENTATION_MAPPING", "TEST_OR_OBSERVATION", "EVIDENCE", "VALIDATION", "EVALUATION", "CONFORMANCE"] and
          trace["extended_result_flow"] == ["VALIDATION", "EVALUATION", "CONFORMANCE", "ELIGIBILITY", "AUTHORITY", "AUTHORIZATION", "DECISION", "EXECUTION", "VERIFICATION", "NEW_EVIDENCE"] and trace["bidirectional"])
    check("T02", "traceability", "24 one-to-one rows provide forward and reverse requirement/code/evidence lookup",
          len(trace_rows) == 24 and len({row["requirement_ref"] for row in trace_rows}) == 24 and
          len({row["implementation_mapping_ref"] for row in trace_rows}) == 24 and len({row["evidence_ref"] for row in trace_rows}) == 24 and
          {row["validation_ref"] for row in trace_rows} == {item["validation_id"] for item in validation_results} and
          {row["evaluation_ref"] for row in trace_rows} == {item["evaluation_id"] for item in evaluation_results} and
          all(row["conformance_ref"] for row in trace_rows))

    validation_contract = load(DESTINATION / "VALIDATION-CONTRACT.yaml")
    validation_schema = load(DESTINATION / "schema/validation-contract.schema.yaml")
    check("K01", "contracts", "validation contract is deterministic, non-mutating, and validation-only",
          exact_shape(validation_schema, validation_contract) and valid_hash("VALIDATION_CONTRACT", validation_contract) and
          validation_contract["output"]["states"] == list(VALIDATION_RESULTS) and not validation_contract["may_modify_authoritative_state"] and
          validation_contract["deterministic"] and {"ISSUE_CERTIFICATE", "APPROVE_RELEASE", "MUTATE_AUTHORITATIVE_HISTORY", "EVALUATE_PREDICATE"} <= set(validation_contract["forbidden_actions"]))
    evaluation_contract = load(DESTINATION / "EVALUATION-CONTRACT.yaml")
    evaluation_schema = load(DESTINATION / "schema/evaluation-contract.schema.yaml")
    check("K02", "contracts", "evaluation contract requires VALID and all nine semantic bindings",
          exact_shape(evaluation_schema, evaluation_contract) and valid_hash("EVALUATION_CONTRACT", evaluation_contract) and
          evaluation_contract["prerequisite"]["required_validation"] == "VALID" and len(evaluation_contract["required_bindings"]) == 9 and
          evaluation_contract["output_type"] == "EvaluationResult" and not evaluation_contract["may_authorize"])
    conformance_contract = load(DESTINATION / "CONFORMANCE-CONTRACT.yaml")
    conformance_schema = load(DESTINATION / "schema/conformance-contract.schema.yaml")
    check("K03", "contracts", "conformance contract applies requirements and forbids VALID/TRUE shortcuts",
          exact_shape(conformance_schema, conformance_contract) and valid_hash("CONFORMANCE_CONTRACT", conformance_contract) and
          len(conformance_contract["required_inputs"]) == 5 and set(conformance_contract["forbidden_inferences"]) ==
          {"VALIDATION_EQUALS_CONFORMANT", "TRUE_EQUALS_CONFORMANT"} and conformance_contract["non_conformant_requires_violation"] and
          conformance_contract["absence_of_evidence_default"] == "UNVERIFIED")

    conformance_document = load(DESTINATION / "CONFORMANCE-RESULT-MODEL.yaml")
    conformance_schema_r3 = load(DESTINATION / "schema/conformance-result-r3.schema.yaml")
    conformance_objects = conformance_document["objects"]
    check("K04", "contracts", "conformance result domain is exact and every reference result is hash-bound",
          conformance_document["states"] == list(CONFORMANCE_RESULTS) and len(conformance_objects) == 24 and
          all(exact_shape(conformance_schema_r3, item) and valid_hash("CONFORMANCE_RESULT_R3", item) and
              item["requirement_ref"] in {requirement["requirement_id"] for requirement in requirements} and
              set(item["evaluation_refs"]) <= {evaluation["evaluation_id"] for evaluation in evaluation_results} and
              (item["status"] != "NON_CONFORMANT" or item["violated_conditions"]) for item in conformance_objects))

    conversion_document = load(DESTINATION / "RESULT-CONVERSION-RULES.yaml")
    conversion_schema = load(DESTINATION / "schema/conversion-rule.schema.yaml")
    conversion_rules = conversion_document["objects"]
    check("X01", "conversion", "nine explicit, named, hash-bound conversion functions form the complete result flow",
          conversion_document["generic_convert_operation"] == "FORBIDDEN" and len(conversion_rules) == 9 and
          len({item["rule_id"] for item in conversion_rules}) == 9 and
          all(exact_shape(conversion_schema, item) and valid_hash("CONVERSION_RULE", item) and item["preconditions"] and item["authority_ref"] for item in conversion_rules))
    forbidden = load(DESTINATION / "FORBIDDEN-IMPLICIT-CONVERSIONS.yaml")
    check("X02", "conversion", "all four supplied implicit conversions and uncertainty coercions are forbidden",
          forbidden["unruled_conversion"] == "INVALID" and len(forbidden["objects"]) == 7 and
          {("ValidationResult.VALID", "ConformanceResult.CONFORMANT"), ("EvaluationResult.TRUE", "ReleaseDecision.APPROVED"),
           ("ConformanceResult.CONFORMANT", "Authorization.GRANTED"), ("ReleaseDecision.APPROVED", "ReleaseExecution.SUCCEEDED")} <=
          {(item["source"], item["target"]) for item in forbidden["objects"]})

    guidance = load(DESTINATION / "TYPED-BOUNDARY-GUIDANCE.yaml")
    rust_files = list(ROOT.rglob("*.rs"))
    check("G01", "guidance", "Rust type separation remains implementation guidance, not invented evidence",
          guidance["classification"] == "IMPLEMENTATION_GUIDANCE" and guidance["language"] == "Rust" and
          guidance["repository_has_rust_target"] is False and guidance["implementation_evidence"] == "UNAVAILABLE" and
          not guidance["creates_normative_states"] and not rust_files)
    errors = load(DESTINATION / "ERROR-MODEL.yaml")["objects"]
    error_schema = load(DESTINATION / "schema/boundary-error.schema.yaml")
    check("G02", "errors", "nine exact structured error domains preserve rule and evidence provenance",
          len(errors) == 9 and {item["error_type"] for item in errors} == set(ERROR_DOMAINS) and
          all(exact_shape(error_schema, item) and valid_hash("BOUNDARY_ERROR", item) and item["rule_ref"] for item in errors))
    recovery = load(DESTINATION / "RECOVERABILITY.yaml")
    check("G03", "errors", "seven recoverability values are diagnostic and do not alter UNKNOWN",
          recovery["states"] == list(RECOVERABILITY) and recovery["semantic_effect"] == "NONE" and
          recovery["example"]["result"] == recovery["example"]["effective_result"] == "UNKNOWN")

    validator_model = load(DESTINATION / "MECHANICAL-BOUNDARY-VALIDATOR.yaml")
    check("D01", "detector", "mechanical validator publishes exactly B001 through B012",
          validator_model["entrypoint"] == "validate_boundary_artifact" and validator_model["output_type"] == "ValidationResult" and
          list(validator_model["defects"]) == [f"B{i:03d}" for i in range(1, 13)])
    rules = load(DESTINATION / "BOUNDARY-CONFORMANCE-RULES.yaml")["objects"]
    check("D02", "detector", "BOUNDARY-001 through BOUNDARY-010 are complete and unique",
          [item["id"] for item in rules] == [f"BOUNDARY-{i:03d}" for i in range(1, 11)])

    tests = load(DESTINATION / "MACHINE-TESTS.yaml")["objects"]
    rerun = run(DESTINATION)
    stored_results = load(DESTINATION / "MACHINE-TEST-RESULTS.yaml")
    check("Q01", "tests", "all 57 executable tests independently rerun byte-for-value and pass",
          len(tests) == len(rerun) == 57 and rerun == stored_results["objects"] and all(item["status"] == "PASSED" for item in rerun))
    check("Q02", "tests", "B-T01 through B-T15 machine matrix is complete",
          [item["test_id"] for item in tests[:15]] == [f"B-T{i:02d}" for i in range(1, 16)])
    check("Q03", "tests", "all B001 through B012 negative fixtures reject with exact provenance",
          all(next(item for item in rerun if item["test_id"] == f"BV-T{i:02d}")["actual"] == f"INVALID:B{i:03d}" for i in range(1, 13)))
    check("Q04", "tests", "all ten boundary conformance rules execute successfully",
          all(next(item for item in rerun if item["test_id"] == f"BR-T{i:02d}")["actual"] == "PASS" for i in range(1, 11)))
    check("Q05", "tests", "all nine explicit cross-domain conversions require and accept their exact rules",
          all(next(item for item in rerun if item["test_id"] == f"CV-T{i:02d}")["actual"] == "ALLOWED" for i in range(1, 10)))
    check("Q06", "tests", "contract tests enforce complete bindings and preserve absence, violation, and evidence-validation semantics",
          [next(item for item in rerun if item["test_id"] == f"CT-T{i:02d}")["actual"] for i in range(1, 12)] ==
          ["BLOCKED", "ELIGIBLE", "INVALID", "CONFORMANT", "UNVERIFIED", "NO_CONFORMANCE_RESULT", "NON_CONFORMANT", "NON_CONFORMANT", "UNKNOWN", "TRUE", "BLOCKED"])

    graph = load(DESTINATION / "FINAL-ARTIFACT-GRAPH.yaml")
    closure = load(DESTINATION / "CLOSURE-CONDITION.yaml")
    check("CL01", "closure", "final graph reaches verification and feeds only new evidence",
          graph["nodes"][-2:] == ["VERIFICATION", "NEW_EVIDENCE"] and graph["new_evidence_feedback_only"] and not graph["history_rewrite"])
    check("CL02", "closure", "all eight closure conditions hold without cross-layer borrowing",
          closure["result"] == "BOUNDARY_FROZEN" and len(closure["checks"]) == 8 and all(closure["checks"].values()) and
          load(DESTINATION / "FINAL-PRINCIPLE.yaml")["no_layer_may_borrow_semantic_authority"])
    implementation = load(DESTINATION / "IMPLEMENTATION-CONFORMANCE.yaml")
    current = load(DESTINATION / "CURRENT-STATUS.yaml")
    check("NI01", "non_invention", "reference harness conformance does not manufacture target or Rust conformance",
          implementation["reference_boundary_harness"] == "CONFORMANT" and implementation["target_engine"] == "UNVERIFIED" and
          implementation["rust_typed_domain_implementation"] == "UNVERIFIED" and not implementation["finite_tests_prove_all_implementations"] and
          current["objects"] == [] and current["target_implementation"] == "UNVERIFIED" and not current["invented_production_evidence"])

    prior = load(DESTINATION / "PRIOR-INTEGRITY.yaml")
    mismatches = []
    for item in prior["artifacts"]:
        path = COMPLIANCE / item["path"]
        if not path.is_file() or path.stat().st_size != item["bytes"] or sha256(path) != item["sha256"]:
            mismatches.append(item["path"])
    check("PR01", "integrity", "all 900 predecessor artifacts remain byte-identical",
          prior["protected_artifact_count"] == len(prior["artifacts"]) == 900 and not mismatches, str(mismatches[:10]))
    headings = re.findall(r"^## (\d+)\. ", (DESTINATION / "SPECIFICATION.md").read_text(), re.M)
    check("DOC01", "documentation", "all 31 requested R3 sections are represented in order", headings == [str(i) for i in range(1, 32)])

    determinism = load(DESTINATION / "DETERMINISM-VALIDATION.yaml") if (DESTINATION / "DETERMINISM-VALIDATION.yaml").is_file() else {}
    regression = load(DESTINATION / "REGRESSION-VALIDATION.yaml") if (DESTINATION / "REGRESSION-VALIDATION.yaml").is_file() else {}
    check("DET01", "determinism", "57 generator artifacts regenerate byte-identically",
          determinism.get("status") == "PASS" and determinism.get("summary", {}).get("identical") == 57)
    check("REG01", "regression", "R2.1, R2, and v14.7.1 regressions plus append-only guards pass", regression.get("status") == "PASS")
    check("HY01", "hygiene", "no Python bytecode caches exist", not list(HISTORICAL.rglob("__pycache__")) and not list(HISTORICAL.rglob("*.pyc")))

    checks.append({
        "check_id": "GATE-R3", "category": "acceptance", "result": "BLOCKED",
        "description": "target implementation, Rust domain types, durability, and production crypto",
        "detail": "Boundary reference contracts conform; no target implementation or production evidence is present.",
    })
    return finish(checks)


def finish(checks):
    passed = sum(item["result"] == "PASS" for item in checks)
    failed = sum(item["result"] == "FAIL" for item in checks)
    blocked = sum(item["result"] == "BLOCKED" for item in checks)
    overall = "FAIL" if failed else "BOUNDARY_CONFORMANT_TARGET_IMPLEMENTATION_UNVERIFIED"
    output = {"realization_version": VERSION, "overall_status": overall,
              "summary": {"total": len(checks), "passed": passed, "failed": failed, "blocked": blocked}, "checks": checks}
    (DESTINATION / "VALIDATION.yaml").write_text(json.dumps(output, indent=2) + "\n")
    (DESTINATION / "VALIDATION.md").write_text(
        f"# v14.7-R3 Validation\n\n{passed} PASS / {failed} FAIL / {blocked} BLOCKED ({len(checks)} checks)\n\n`{overall}`\n"
    )
    print(f"{passed} PASS / {failed} FAIL / {blocked} BLOCKED ({len(checks)} checks); {overall}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
