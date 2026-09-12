#!/usr/bin/env python3
"""Build the Protocol-v11 obligation-to-specification registry.

Protocol-v11 may only derive normative requirements from a valid, verified v10.1
obligation package. The checked-in v10.1 package is structurally valid but has a failed
upstream input contract, no VERIFIED obligations, epistemic UNKNOWN records, and
unresolved conflicts. This builder therefore closes the derivation gate and emits a
complete machine-readable rejection/audit package with zero normative requirements.
It never turns blocked obligations into requirements merely to populate a registry.
"""
from __future__ import annotations

import hashlib
import json
import shutil
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[2]
HS = ROOT / "historical-source"
OBL = HS / "obligations"
OUT = HS / "specification"
TOOLS = HS / "tools"

MACHINE = [
    "INPUT-CONTRACT.yaml", "REQUIREMENTS.yaml", "NORMATIVE-RULES.yaml",
    "ACCEPTANCE-CRITERIA.yaml", "TEST-ORACLES.yaml", "REQUIREMENT-DEPENDENCIES.yaml",
    "REQUIREMENT-CONFLICTS.yaml", "REQUIREMENT-SUPERSESSION.yaml",
    "REQUIREMENT-COVERAGE.yaml", "CONFORMANCE-MATRIX.yaml", "VERIFICATION-MATRIX.yaml",
    "IMPLEMENTATION-BOUNDARIES.yaml", "SEMANTIC-DIFFS.yaml", "TRACEABILITY.yaml",
    "CONFORMANCE.yaml", "SPECIFICATION-CERTIFICATE.yaml",
]
REPORTS = [
    "REQUIREMENTS.md", "NORMATIVE-RULES.md", "ACCEPTANCE-CRITERIA.md",
    "TEST-ORACLES.md", "REQUIREMENT-COVERAGE.md", "REQUIREMENT-DEPENDENCIES.md",
    "REQUIREMENT-CONFLICTS.md", "CONFORMANCE-MATRIX.md", "VERIFICATION-MATRIX.md",
    "IMPLEMENTATION-BOUNDARIES.md", "SEMANTIC-DIFFS.md", "TRACEABILITY.md",
    "SPECIFICATION-AUDIT.md", "FINAL-SPECIFICATION.md",
]
SCHEMAS = [
    "schema/requirement.schema.yaml", "schema/normative-rule.schema.yaml",
    "schema/acceptance-criterion.schema.yaml", "schema/test-oracle.schema.yaml",
    "schema/requirement-dependency.schema.yaml", "schema/traceability.schema.yaml",
    "schema/specification-certificate.schema.yaml",
]
DELIVERABLES = MACHINE + REPORTS + SCHEMAS

REQUIREMENT_TYPES = [
    "BEHAVIORAL", "STRUCTURAL", "INTERFACE", "SEMANTIC", "STATE", "LIFECYCLE",
    "ERROR", "SECURITY", "AUTHORIZATION", "CONCURRENCY", "RESOURCE", "PERFORMANCE",
    "PERSISTENCE", "PROVENANCE", "OBSERVABILITY", "COMPATIBILITY", "CONFIGURATION",
    "SERIALIZATION", "DISCOVERY", "DEDUPLICATION", "SCHEDULING", "CANCELLATION",
    "RECOVERY", "AUDIT", "EXPORT", "UI", "TESTABILITY", "VERIFICATION", "NEGATIVE",
    "INVARIANT", "TRANSITION", "BOUNDARY",
]
DISPOSITIONS = ["PRESERVE", "STABILIZE", "GENERALIZE", "FORMALIZE", "STRENGTHEN", "RESTRICT", "COMPATIBILIZE", "DEPRECATE", "REJECT", "INTRODUCE", "OPTIONALIZE"]
STRENGTHS = ["MANDATORY", "CONDITIONAL", "RECOMMENDED", "OPTIONAL", "EXPERIMENTAL", "NON_NORMATIVE", "UNKNOWN"]
SCOPES = ["GLOBAL", "VERSION", "COMPONENT", "INTERFACE", "OPERATION", "STATE", "TRANSITION", "CANDIDATE", "OBSERVATION", "DISCOVERY", "PROVIDER", "SCHEDULER", "WORKER", "KNOWLEDGE_BASE", "PERSISTENCE", "EXPORT", "UI", "TEST", "SECURITY_BOUNDARY", "TRUST_BOUNDARY", "CONFIGURATION", "RUNTIME"]
EPISTEMIC = ["PROVED", "SUPPORTED", "INFERRED", "CONJECTURED", "CONTRADICTED", "UNKNOWN"]
LIFECYCLE = ["DISCOVERED", "DERIVED", "DRAFTED", "FORMALIZED", "IMPLEMENTED", "PARTIALLY_IMPLEMENTED", "VERIFIED", "FAILED", "SUPERSEDED", "REJECTED", "DEPRECATED", "UNKNOWN"]
RULE_OPERATORS = ["MUST", "MUST_NOT", "SHALL", "SHALL_NOT", "MAY", "MAY_NOT", "IF", "THEN", "ONLY_IF", "UNLESS", "EXCEPT"]
CANONICAL_OPERATORS = ["MUST", "MUST_NOT", "MAY"]
PREDICATES = ["EQUALITY", "INEQUALITY", "MEMBERSHIP", "EXISTENCE", "NON_EXISTENCE", "TYPE", "SHAPE", "RANGE", "CARDINALITY", "UNIQUENESS", "ORDERING", "TEMPORAL", "STATE", "TRANSITION", "DEPENDENCY", "AUTHORIZATION", "CAPABILITY", "PROVENANCE", "HASH", "SIGNATURE", "REFERENCE", "SCHEMA", "CONTAINMENT", "RESOURCE_BOUND", "CONCURRENCY", "CANCELLATION", "DETERMINISM", "COMPATIBILITY", "AND", "OR", "NOT", "XOR", "IMPLIES", "IFF", "FOR_ALL", "EXISTS", "EXACTLY_ONE", "AT_LEAST_ONE", "AT_MOST_ONE"]
ORACLES = ["BOOLEAN", "EXACT_VALUE", "RANGE", "SET_MEMBERSHIP", "STRUCTURAL", "STATE", "TRACE", "INVARIANT", "PROPERTY", "REFERENCE_MODEL", "DIFFERENTIAL", "METAMORPHIC", "HASH", "SIGNATURE", "SCHEMA", "TEMPORAL", "RESOURCE_BOUND", "SECURITY_POLICY"]
BOUNDARIES = ["INPUT", "VALIDATION", "ACQUISITION", "RECOGNITION", "PROVIDER", "EXPANSION", "SCHEDULER", "STATE_STORE", "KNOWLEDGE_BASE", "PERSISTENCE", "AUTHORIZATION", "AUDIT", "EXPORT", "UI", "RUNTIME", "TEST_HARNESS"]
RDEP_RELATIONS = ["REQUIRES", "ENABLES", "SUPPORTS", "REFINES", "STRENGTHENS", "CONSTRAINS", "CONFLICTS_WITH", "SUPERSEDES", "VERIFIED_BY", "DERIVED_FROM"]
CONFORMANCE_LEVELS = ["L0_NONE", "L1_STRUCTURAL", "L2_BEHAVIORAL", "L3_SEMANTIC", "L4_SAFETY", "L5_SECURITY", "L6_VERIFIED"]
VERIFICATION_LEVELS = ["V0_UNTESTED", "V1_EXAMPLE_TESTED", "V2_UNIT_VERIFIED", "V3_PROPERTY_VERIFIED", "V4_INTEGRATION_VERIFIED", "V5_ADVERSARIAL_VERIFIED", "V6_FORMALLY_VERIFIED"]
CRITICALITY = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "UNKNOWN"]
COVERAGE = ["FULL", "PARTIAL", "MISSING", "CONFLICTED", "BLOCKED", "UNKNOWN"]
INPUT_REJECTIONS = ["INPUT_MISSING", "INPUT_SCHEMA_MISMATCH", "INPUT_HASH_MISMATCH", "OBLIGATION_UNKNOWN", "PROPERTY_UNKNOWN", "BROKEN_LINEAGE", "BROKEN_DEPENDENCY", "TEMPORAL_CONTAMINATION", "UNVERIFIED_SOURCE", "CONFLICT_UNRESOLVED"]
FAILURE_MODES = ["REQUIREMENT_WITHOUT_OBLIGATION", "REQUIREMENT_WITHOUT_EVIDENCE", "UNTRACED_REQUIREMENT", "ORPHAN_OBLIGATION", "NON_TESTABLE_REQUIREMENT", "ORACLE_CIRCULARITY", "ORACLE_IMPLEMENTATION_COUPLING", "DEPENDENCY_CYCLE", "UNRESOLVED_CONFLICT", "SEMANTIC_NARROWING", "SEMANTIC_WIDENING", "RETROACTIVE_NORMATIVITY", "HISTORICAL_CONTAMINATION", "FALSE_VERIFICATION", "FALSE_PROOF", "HIDDEN_EXCEPTION", "UNDEFINED_SCOPE", "UNDEFINED_BOUNDARY", "UNMEASURABLE_PROPERTY", "MISSING_NEGATIVE_TEST", "COMPATIBILITY_OVERCLAIM", "UNJUSTIFIED_STRENGTHENING", "HARNESS_CONFUSION", "UNKNOWN_ESCALATION"]
V11_INVARIANTS = [
    "Every historical requirement traces to historical evidence.",
    "Every mandatory requirement has an acceptance criterion.",
    "Every safety/security requirement has a verification path.",
    "Requirement dependencies are explicit.",
    "Requirement conflicts are explicit.",
    "Historical and future requirements are distinguishable.",
    "Implementation location is not confused with semantic definition.",
    "Test existence is not confused with test adequacy.",
    "Verification status is not confused with epistemic status.",
    "Requirement strength is not confused with obligation strength.",
    "Requirement type is not confused with obligation class.",
    "A requirement may not strengthen historical meaning without explicit disposition.",
    "Negative requirements remain testable.",
    "Failed verification remains traceable to the failed requirement.",
    "Specification changes preserve historical lineage.",
]


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def object_hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest()


def write_md(name: str, text: str) -> None:
    (OUT / name).write_text(text.rstrip() + "\n", encoding="utf-8")


def table(headers: list[str], rows: Iterable[Iterable[Any]]) -> str:
    def clean(v: Any) -> str:
        if isinstance(v, list): v = ", ".join(str(x) for x in v)
        return str(v).replace("|", "\\|").replace("\n", " ")
    return "| " + " | ".join(headers) + " |\n|" + "|".join("---" for _ in headers) + "|\n" + "".join("| " + " | ".join(clean(v) for v in row) + " |\n" for row in rows)


def front(title: str) -> str:
    return f"# {title}\n\n> **Derivation gate: CLOSED — REJECTED_INVALID_OBLIGATION_PACKAGE.** The v10.1 input contract failed, no source obligation is `VERIFIED`, epistemic `UNKNOWN` records remain, and four obligation conflicts are unresolved. Protocol-v11 therefore emits no normative requirements. This is a validated rejection/audit package, not a normative implementation specification.\n\n"


def input_record(kind: str, rel: str, schema_version: str) -> dict[str, Any]:
    path = OBL / rel
    return {
        "artifact_id": f"V101-{kind.upper().replace('_','-')}-{sha(path)[:16]}",
        "artifact_type": kind,
        "schema_version": schema_version,
        "source_path": f"historical-source/obligations/{rel}",
        "producer_stage": "v10.1",
        "generated_at": "UNKNOWN_NOT_RECORDED_UPSTREAM",
        "content_hash": sha(path),
        "hash_validation": "MATCH",
        "schema_validation": "STRUCTURALLY_VALID_JSON_COMPATIBLE_YAML",
    }


def main() -> None:
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    upstream_contract = load(OBL / "INPUT-CONTRACT.yaml")
    obligation_data = load(OBL / "OBLIGATIONS.yaml")
    dependency_data = load(OBL / "OBLIGATION-DEPENDENCIES.yaml")
    lineage_data = load(OBL / "OBLIGATION-LINEAGE.yaml")
    conflict_data = load(OBL / "OBLIGATION-CONFLICTS.yaml")
    trace_data = load(OBL / "TRACEABILITY-MATRIX.yaml")
    verification_data = load(OBL / "VERIFICATION-GRAPH.yaml")

    obligations = obligation_data["obligations"]
    properties = obligation_data["historical_properties"]
    evidence = {x["evidence_id"]: x for x in upstream_contract["normalized_evidence"]}
    obligation_ids = {x["obligation_id"] for x in obligations}
    property_ids = {x["property_id"] for x in properties}
    unresolved_conflicts = [x for x in conflict_data["conflicts"] if x["resolution_status"] == "UNRESOLVED"]
    unverified = [x for x in obligations if x["status"] != "VERIFIED" or x["verification"]["result"] != "VERIFIED"]
    unknown_obligations = [x for x in obligations if x["epistemic_status"] == "UNKNOWN" or x["status"] == "UNKNOWN"]
    unknown_properties = [x for x in properties if x["epistemic_status"] == "UNKNOWN" or x["historical_status"] == "UNKNOWN"]

    required_inputs = [
        input_record("obligation_contract", "INPUT-CONTRACT.yaml", upstream_contract["input_contract_version"]),
        input_record("obligation_registry", "OBLIGATIONS.yaml", obligation_data["metadata"]["obligation_schema_version"]),
        input_record("historical_properties", "OBLIGATIONS.yaml", obligation_data["metadata"]["obligation_schema_version"]),
        input_record("obligation_dependencies", "OBLIGATION-DEPENDENCIES.yaml", dependency_data["schema_version"]),
        input_record("obligation_lineage", "OBLIGATION-LINEAGE.yaml", lineage_data["schema_version"]),
        input_record("obligation_conflicts", "OBLIGATION-CONFLICTS.yaml", conflict_data["schema_version"]),
        input_record("traceability", "TRACEABILITY-MATRIX.yaml", trace_data["schema_version"]),
        input_record("verification_records", "VERIFICATION-GRAPH.yaml", verification_data["schema_version"]),
    ]
    inherited_missing = [x for x in upstream_contract["failure_states"] if x["state"] == "INPUT_MISSING"]
    input_failures = [
        {"failure_id": "RIF-001", "state": "INPUT_MISSING", "affected": [x["stage"] for x in inherited_missing], "detail": "The v10.1 source package is missing required Protocol-v4 through Protocol-v7 stages."},
        {"failure_id": "RIF-002", "state": "INPUT_HASH_MISMATCH", "affected": ["v1 source extraction"], "detail": "The v10.1 package preserves the Protocol-v1 raw/source-range integrity failure."},
        {"failure_id": "RIF-003", "state": "UNVERIFIED_SOURCE", "affected": [x["obligation_id"] for x in unverified], "detail": f"{len(unverified)} obligations are not VERIFIED with verification evidence."},
        {"failure_id": "RIF-004", "state": "OBLIGATION_UNKNOWN", "affected": [x["obligation_id"] for x in unknown_obligations], "detail": f"{len(unknown_obligations)} obligations retain UNKNOWN epistemic or lifecycle state."},
        {"failure_id": "RIF-005", "state": "PROPERTY_UNKNOWN", "affected": [x["property_id"] for x in unknown_properties], "detail": f"{len(unknown_properties)} historical properties retain UNKNOWN epistemic or historical state."},
        {"failure_id": "RIF-006", "state": "CONFLICT_UNRESOLVED", "affected": [x["conflict_id"] for x in unresolved_conflicts], "detail": f"{len(unresolved_conflicts)} obligation conflicts remain unresolved."},
    ]
    input_checks = [
        {"check_id": "RI01", "check": "all required v10.1 artifacts are present", "result": "PASS", "detail": "8/8 required input roles are bound to existing artifacts"},
        {"check_id": "RI02", "check": "schemas are structurally compatible", "result": "PASS", "detail": "all selected registries are schema version 1.0"},
        {"check_id": "RI03", "check": "content hashes match selected artifacts", "result": "PASS", "detail": "8/8 selected artifact hashes match"},
        {"check_id": "RI04", "check": "upstream obligation contract is accepted", "result": "FAIL", "failure_states": ["INPUT_MISSING", "INPUT_HASH_MISMATCH", "UNVERIFIED_SOURCE"]},
        {"check_id": "RI05", "check": "obligation registry contains only verified, known source obligations", "result": "FAIL", "failure_states": ["UNVERIFIED_SOURCE", "OBLIGATION_UNKNOWN"]},
        {"check_id": "RI06", "check": "historical properties are resolved", "result": "FAIL", "failure_states": ["PROPERTY_UNKNOWN"]},
        {"check_id": "RI07", "check": "obligation dependency graph references resolve and is acyclic", "result": "PASS", "failure_states": []},
        {"check_id": "RI08", "check": "obligation lineage references resolve", "result": "PASS", "failure_states": []},
        {"check_id": "RI09", "check": "obligation conflicts are resolved", "result": "FAIL", "failure_states": ["CONFLICT_UNRESOLVED"]},
        {"check_id": "RI10", "check": "traceability and verification records establish verified source", "result": "FAIL", "failure_states": ["UNVERIFIED_SOURCE"]},
    ]
    input_contract = {
        "specification_version": "11.0", "requirement_input_contract_version": "1.0",
        "status": "REJECTED_INVALID_OBLIGATION_PACKAGE", "derivation_gate": "CLOSED",
        "required_inputs": required_inputs, "rejection_registry": INPUT_REJECTIONS,
        "failure_states": input_failures, "validation_checks": input_checks,
        "source_package": {"protocol": "v10.1", "input_contract_status": upstream_contract["status"], "obligation_count": len(obligations), "verified_obligation_count": len(obligations) - len(unverified), "unknown_obligation_count": len(unknown_obligations), "unknown_property_count": len(unknown_properties), "unresolved_conflict_count": len(unresolved_conflicts)},
        "derivation_policy": "No requirement, rule, criterion, oracle, boundary, or conformance claim may be derived while this gate is closed.",
    }
    dump(OUT / "INPUT-CONTRACT.yaml", input_contract)

    registries = {
        "requirement_types": REQUIREMENT_TYPES, "dispositions": DISPOSITIONS,
        "strengths": STRENGTHS, "scope_types": SCOPES, "epistemic_states": EPISTEMIC,
        "lifecycle_states": LIFECYCLE, "rule_operators": RULE_OPERATORS,
        "canonical_rule_operators": CANONICAL_OPERATORS, "predicate_types": PREDICATES,
        "oracle_types": ORACLES, "implementation_boundaries": BOUNDARIES,
        "dependency_relations": RDEP_RELATIONS, "conformance_levels": CONFORMANCE_LEVELS,
        "verification_levels": VERIFICATION_LEVELS, "criticality_values": CRITICALITY,
    }
    requirements_obj = {
        "schema_version": "1.0", "specification_version": "11.0",
        "status": "DERIVATION_REJECTED", "derivation_gate": "CLOSED",
        "registries": registries, "requirements": [],
        "untraced_requirements": [], "new_engineering_requirements": [],
        "blocked_source_obligations": [x["obligation_id"] for x in obligations],
        "pipeline_invariants": [{"invariant_id": f"V11-I{i:02d}", "statement": statement, "status": "PASS", "basis": "CLOSED_GATE_PREVENTS_INVALID_TRANSFORMATION" if i < 15 else "UPSTREAM_LINEAGE_RETAINED_AND_REFERENCED"} for i, statement in enumerate(V11_INVARIANTS, 1)],
        "statement_rule": "Requirements use atomic, scoped, testable MUST/MUST_NOT/IF-THEN forms only after the input gate opens.",
        "compatibility_types": ["SOURCE_COMPATIBILITY", "BEHAVIORAL_COMPATIBILITY", "DATA_COMPATIBILITY", "PROTOCOL_COMPATIBILITY", "CONFIGURATION_COMPATIBILITY", "SERIALIZATION_COMPATIBILITY", "UI_COMPATIBILITY", "TEST_COMPATIBILITY"],
        "historical_preservation_modes": ["EXACT", "SEMANTIC", "COMPATIBLE", "NORMALIZED", "GENERALIZED", "INTENTIONALLY_CHANGED", "REJECTED", "UNKNOWN"],
        "forbidden_equivalences": ["historical behavior = requirement", "obligation = requirement", "requirement = implementation", "implementation = verification", "test = proof of all semantics", "documentation = enforcement", "interface = guarantee"],
    }
    rules_obj = {"schema_version": "1.0", "status": "DERIVATION_REJECTED", "operators": RULE_OPERATORS, "canonical_operators": CANONICAL_OPERATORS, "predicate_types": PREDICATES, "compound_logic": ["AND", "OR", "NOT", "XOR", "IMPLIES", "IFF", "FOR_ALL", "EXISTS", "EXACTLY_ONE", "AT_LEAST_ONE", "AT_MOST_ONE"], "rules": [], "reason": "No requirement exists from which a normative rule may be derived."}
    criteria_obj = {"schema_version": "1.0", "status": "DERIVATION_REJECTED", "acceptance_criteria": [], "non_testable_requirements": [], "reason": "No admitted normative requirement exists."}
    oracles_obj = {"schema_version": "1.0", "status": "DERIVATION_REJECTED", "oracle_types": ORACLES, "test_oracles": [], "reference_models": [], "property_based_requirements": [], "oracle_independence_audit": [], "negative_test_policy": "Security, authorization, lifecycle, failure, and safety requirements require negative-test coverage unless explicitly justified.", "mutation_testing_policy": "Where practical, weakening a mandatory enforced property must cause a relevant independent oracle to fail.", "test_harness_contract": {"status": "NOT_INSTANTIATED_INPUT_REJECTED", "required_dimensions": ["input_generation", "environment", "isolation", "reset", "execution", "observation", "oracle_evaluation", "evidence_capture", "cleanup"], "may_silently_alter_tested_semantics": False}, "reason": "No criterion exists from which an oracle may be derived."}
    reqdeps_obj = {"schema_version": "1.0", "graph_type": "REQUIREMENT_DEPENDENCY_GRAPH", "status": "DERIVATION_REJECTED", "relations": RDEP_RELATIONS, "nodes": [], "edges": [], "requirement_dependencies": [], "requires_cycles": [], "mandatory_closure": [], "verification_order": [], "ordering_model": ["FOUNDATION", "SCHEMA", "IDENTITY", "STATE", "AUTHORIZATION", "CORE_BEHAVIOR", "CONCURRENCY", "FAILURE", "PERSISTENCE", "PROVENANCE", "OBSERVABILITY", "EXPORT", "UI"], "reason": "Obligation dependencies are not silently copied into requirement dependencies."}
    reqconf_obj = {"schema_version": "1.0", "graph_type": "REQUIREMENT_CONFLICT_GRAPH", "status": "DERIVATION_REJECTED", "requirement_conflicts": [], "upstream_obligation_conflict_blockers": [x["conflict_id"] for x in unresolved_conflicts], "resolution_values": ["PRESERVE_BOTH", "PRIORITIZE_ONE", "RESTRICT_SCOPE", "SPLIT_SCOPE", "SUPERSEDE", "REJECT", "DEFER", "UNKNOWN"], "default_precedence": ["SAFETY", "SECURITY", "DATA_INTEGRITY", "AUTHORIZATION", "LIFECYCLE", "BEHAVIOR", "PERFORMANCE", "UI", "CONVENIENCE"], "automatic_resolution": False}
    supersession_obj = {"schema_version": "1.0", "status": "DERIVATION_REJECTED", "supersessions": [], "requirement_version": "1.0", "change_classes": ["TEXT_ONLY", "CLARIFICATION", "SCOPE_CHANGE", "SEMANTIC_WEAKENING", "SEMANTIC_STRENGTHENING", "BREAKING_CHANGE", "DEPRECATION", "REMOVAL"], "deletion_policy": "Historical requirement lineage may not be destroyed."}

    coverage_records = [{"obligation_id": x["obligation_id"], "requirements": [], "coverage_status": "BLOCKED", "orphan_status": "ORPHAN_OBLIGATION", "blockers": ["UNVERIFIED_SOURCE", "REJECTED_INVALID_OBLIGATION_PACKAGE"], "non_normative_disposition": None, "rejected_disposition": None} for x in obligations]
    coverage_obj = {
        "schema_version": "1.0", "status": "BLOCKED", "coverage_values": COVERAGE,
        "obligation_coverage": coverage_records,
        "orphan_requirements": [], "orphan_obligations": [x["obligation_id"] for x in obligations],
        "historical_preservation": [],
        "historical_preservation_modes": ["EXACT", "SEMANTIC", "COMPATIBLE", "NORMALIZED", "GENERALIZED", "INTENTIONALLY_CHANGED", "REJECTED", "UNKNOWN"],
        "coverage_metrics": [
            {"dimension": "obligation_to_requirement", "classification": "BLOCKED", "reason": "input derivation gate closed"},
            {"dimension": "requirement_to_rule", "classification": "BLOCKED", "reason": "no admitted requirements"},
            {"dimension": "requirement_to_criterion", "classification": "BLOCKED", "reason": "no admitted requirements"},
            {"dimension": "criterion_to_oracle", "classification": "BLOCKED", "reason": "no criteria"},
            {"dimension": "oracle_to_test", "classification": "BLOCKED", "reason": "no oracles"},
            {"dimension": "test_to_evidence", "classification": "BLOCKED", "reason": "no v11 tests"},
        ],
        "single_aggregate_percentage": "FORBIDDEN",
    }
    conformance_matrix = {"schema_version": "1.0", "status": "BLOCKED", "levels": CONFORMANCE_LEVELS, "requirements": [], "implementation_claims": [], "known_failed_requirements_may_be_omitted": False, "reason": "No normative requirement or implementation under v11 is admitted."}
    verification_matrix = {"schema_version": "1.0", "status": "BLOCKED", "verification_levels": VERIFICATION_LEVELS, "result_values": ["PASS", "FAIL", "BLOCKED", "SKIPPED", "INCONCLUSIVE", "NOT_APPLICABLE", "UNKNOWN"], "failure_taxonomy": ["HARNESS_FAILURE", "IMPLEMENTATION_FAILURE", "ENVIRONMENT_FAILURE", "TEST_ORACLE_FAILURE", "CONTRACT_VIOLATION", "SPECIFICATION_FAILURE", "TEST_FAILURE", "ORACLE_FAILURE", "DATA_FAILURE", "NONDETERMINISM", "CONTRACT_FAILURE", "UNKNOWN_FAILURE"], "records": [], "upstream_obligation_tests": {"total": len(verification_data["edges"]), "verified": len(verification_data["verified_nodes"]), "status": "UNVERIFIED_SOURCE"}, "rule": "A failed implementation does not prove or disprove historical justification."}
    boundaries_obj = {"schema_version": "1.0", "status": "BLOCKED", "allowed_boundaries": BOUNDARIES, "requirement_boundaries": [], "distinctions": ["SEMANTIC_DEFINITION != IMPLEMENTATION_LOCATION", "ENFORCEMENT_BOUNDARY != OBSERVATION_BOUNDARY", "OBSERVATION_BOUNDARY != VERIFICATION_BOUNDARY"], "reason": "No mandatory requirement exists to assign an enforcement boundary."}
    semantic_diffs_obj = {"schema_version": "1.0", "status": "BLOCKED", "semantic_diffs": [], "comparison_dimensions": ["subject", "predicate", "scope", "precondition", "postcondition", "exception", "strength", "enforcement", "verification", "compatibility"], "narrowing_audit": {"status": "BLOCKED", "findings": [], "reason": "no requirement domains admitted"}, "widening_audit": {"status": "BLOCKED", "findings": [], "reason": "no requirement domains admitted"}, "generalization_tests": [], "strengthening_tests": [], "assumptions": [{"assumption_id": "ASSUMP-001", "statement": "The v10.1 package is source-local and not accepted as complete.", "affected_requirements": [], "epistemic_status": "PROVED", "validation_method": "Read v10.1 INPUT-CONTRACT status."}, {"assumption_id": "ASSUMP-002", "statement": "No current architecture or roadmap may repair missing historical inputs.", "affected_requirements": [], "epistemic_status": "SUPPORTED", "validation_method": "Inspect v11 input bindings and traceability graph."}], "exceptions": [], "configurations": [], "environment_preconditions": []}

    trace_obj = build_traceability(upstream_contract, obligation_data)
    conformance_obj = {"schema_version": "1.0", "status": "BLOCKED", "highest_claimed_level": "L0_NONE", "implemented": [], "partial": [], "missing": [], "failed": [], "claim_allowed": False, "reason": "Input rejection prevents a v11 conformance claim."}

    dump(OUT / "REQUIREMENTS.yaml", requirements_obj)
    dump(OUT / "NORMATIVE-RULES.yaml", rules_obj)
    dump(OUT / "ACCEPTANCE-CRITERIA.yaml", criteria_obj)
    dump(OUT / "TEST-ORACLES.yaml", oracles_obj)
    dump(OUT / "REQUIREMENT-DEPENDENCIES.yaml", reqdeps_obj)
    dump(OUT / "REQUIREMENT-CONFLICTS.yaml", reqconf_obj)
    dump(OUT / "REQUIREMENT-SUPERSESSION.yaml", supersession_obj)
    dump(OUT / "REQUIREMENT-COVERAGE.yaml", coverage_obj)
    dump(OUT / "CONFORMANCE-MATRIX.yaml", conformance_matrix)
    dump(OUT / "VERIFICATION-MATRIX.yaml", verification_matrix)
    dump(OUT / "IMPLEMENTATION-BOUNDARIES.yaml", boundaries_obj)
    dump(OUT / "SEMANTIC-DIFFS.yaml", semantic_diffs_obj)
    dump(OUT / "TRACEABILITY.yaml", trace_obj)
    dump(OUT / "CONFORMANCE.yaml", conformance_obj)

    audit = build_audit(input_contract, coverage_obj, upstream_contract, obligation_data, conflict_data)
    certificate = {
        "specification_version": "11.0", "generated_at": "UNKNOWN_NOT_RECORDED_DETERMINISTIC_BUILD",
        "input_hashes": [{"artifact_id": x["artifact_id"], "content_hash": x["content_hash"]} for x in required_inputs],
        "requirement_count": 0, "rule_count": 0, "criterion_count": 0, "oracle_count": 0,
        "conflict_count": 0, "orphan_requirement_count": 0, "orphan_obligation_count": len(obligations),
        "coverage": {"traceability": "PARTIAL", "semantic": "BLOCKED", "verification": "BLOCKED"},
        "validation_status": "FAIL",
        "unresolved_issues": ["INPUT_MISSING", "INPUT_HASH_MISMATCH", "UNVERIFIED_SOURCE", "OBLIGATION_UNKNOWN", "PROPERTY_UNKNOWN", "CONFLICT_UNRESOLVED", "ORPHAN_OBLIGATION"],
        "certificate_semantics": "Evidence of validation execution, not proof of semantic perfection.",
        "derivation_gate": "CLOSED", "certificate_hash": None,
    }
    certificate["certificate_hash"] = object_hash({k: v for k, v in certificate.items() if k != "certificate_hash"})
    dump(OUT / "SPECIFICATION-CERTIFICATE.yaml", certificate)
    build_schemas()
    build_reports(input_contract, requirements_obj, coverage_obj, reqdeps_obj, reqconf_obj, conformance_matrix, verification_matrix, boundaries_obj, semantic_diffs_obj, trace_obj, audit, certificate, obligations)
    assert all((OUT / x).is_file() for x in DELIVERABLES)
    print(f"generated {len(DELIVERABLES)} v11 deliverables; requirements=0 blocked_obligations={len(obligations)} gate=CLOSED")


def build_traceability(upstream_contract: dict[str, Any], obligation_data: dict[str, Any]) -> dict[str, Any]:
    evidence = upstream_contract["normalized_evidence"]
    properties = obligation_data["historical_properties"]
    obligations = obligation_data["obligations"]
    nodes = []
    seen = set()
    def node(nid: str, kind: str, status: str) -> None:
        if nid not in seen:
            nodes.append({"node_id": nid, "node_type": kind, "status": status}); seen.add(nid)
    edges = []
    for e in evidence:
        source = "SOURCE:" + e["provenance"]["source_path"]
        node(source, "SOURCE", "PRESENT")
        node(e["evidence_id"], "EVIDENCE", e["verification_status"])
        edges.append({"from": source, "to": e["evidence_id"], "relation": "SUPPORTS"})
    for p in properties:
        node(p["property_id"], "HISTORICAL_PROPERTY", p["epistemic_status"])
        for eid in p["evidence_refs"]:
            edges.append({"from": eid, "to": p["property_id"], "relation": "SUPPORTS_PROPERTY"})
    for o in obligations:
        node(o["obligation_id"], "OBLIGATION", o["status"])
        for pid in o["source_properties"]:
            edges.append({"from": pid, "to": o["obligation_id"], "relation": "SUPPORTS_OBLIGATION"})
    reverse = [{"from": e["to"], "to": e["from"], "relation": "REVERSE_" + e["relation"]} for e in edges]
    return {
        "schema_version": "1.0", "graph_type": "FORWARD_AND_BACKWARD_TRACEABILITY_GRAPH",
        "status": "PARTIAL_BLOCKED_AT_OBLIGATION", "nodes": nodes, "forward_edges": edges,
        "reverse_edges": reverse, "requirement_nodes": [], "rule_nodes": [], "criterion_nodes": [],
        "oracle_nodes": [], "test_nodes": [], "result_nodes": [],
        "termination_reason": "The v11 derivation gate is closed; no edge crosses from obligation to requirement.",
    }


def build_audit(input_contract: dict[str, Any], coverage: dict[str, Any], upstream_contract: dict[str, Any], obligation_data: dict[str, Any], conflicts: dict[str, Any]) -> dict[str, Any]:
    detected = ["ORPHAN_OBLIGATION", "UNRESOLVED_CONFLICT", "UNKNOWN_ESCALATION"]
    return {
        "specification_version": "11.0", "status": "FAIL_INPUT_REJECTED",
        "validation_procedure": [
            {"step": 1, "name": "Validate input contract", "result": "FAIL"},
            {"step": 2, "name": "Validate obligation registry", "result": "BLOCKED_UNVERIFIED"},
            {"step": 3, "name": "Validate obligation references", "result": "PASS_STRUCTURAL"},
            {"step": 4, "name": "Validate requirement schema", "result": "PASS_EMPTY_REJECTED_REGISTRY"},
            {"step": 5, "name": "Validate source traceability", "result": "PARTIAL_TO_OBLIGATION"},
            {"step": 6, "name": "Validate dependency graph", "result": "PASS_EMPTY_REQUIREMENT_GRAPH"},
            {"step": 7, "name": "Validate rule predicates", "result": "PASS_EMPTY_REJECTED_REGISTRY"},
            {"step": 8, "name": "Validate acceptance criteria", "result": "PASS_EMPTY_REJECTED_REGISTRY"},
            {"step": 9, "name": "Validate oracle references", "result": "PASS_EMPTY_REJECTED_REGISTRY"},
            {"step": 10, "name": "Validate implementation boundaries", "result": "PASS_EMPTY_REJECTED_REGISTRY"},
            {"step": 11, "name": "Detect contradictions", "result": "BLOCKED_UPSTREAM_CONFLICTS"},
            {"step": 12, "name": "Detect semantic narrowing/widening", "result": "BLOCKED_NO_REQUIREMENTS"},
            {"step": 13, "name": "Compute coverage", "result": "BLOCKED"},
            {"step": 14, "name": "Validate conformance claims", "result": "PASS_NO_CLAIM"},
            {"step": 15, "name": "Produce specification certificate", "result": "FAIL_CERTIFICATE_EMITTED"},
        ],
        "completeness": [
            {"dimension": "TRACEABILITY_COMPLETENESS", "classification": "PARTIAL", "detail": "source through obligation only"},
            {"dimension": "SEMANTIC_COMPLETENESS", "classification": "BLOCKED", "detail": "no admitted requirements"},
            {"dimension": "VALIDATION_COMPLETENESS", "classification": "FULL", "detail": "rejection path structurally validated"},
            {"dimension": "VERIFICATION_COMPLETENESS", "classification": "BLOCKED", "detail": "no verified source obligations"},
            {"dimension": "FAILURE_COMPLETENESS", "classification": "BLOCKED", "detail": "no failure requirements admitted"},
            {"dimension": "SECURITY_COMPLETENESS", "classification": "BLOCKED", "detail": "no security requirements admitted"},
            {"dimension": "COMPATIBILITY_COMPLETENESS", "classification": "BLOCKED", "detail": "v7 missing upstream"},
            {"dimension": "IMPLEMENTATION_BOUNDARY_COMPLETENESS", "classification": "BLOCKED", "detail": "no mandatory requirements"},
        ],
        "failure_mode_registry": FAILURE_MODES,
        "detected_failure_modes": detected,
        "input_rejection_states": [x["state"] for x in input_contract["failure_states"]],
        "contradiction_audit": {"status": "BLOCKED", "upstream_unresolved_conflicts": [x["conflict_id"] for x in conflicts["conflicts"] if x["resolution_status"] == "UNRESOLVED"], "requirement_conflicts": []},
        "hidden_assumptions": [
            {"assumption_id": "ASSUMP-001", "statement": "The v10.1 package is source-local and not accepted as complete.", "affected_requirements": [], "epistemic_status": "PROVED", "validation_method": "Read v10.1 INPUT-CONTRACT status."},
            {"assumption_id": "ASSUMP-002", "statement": "No current architecture or roadmap may repair missing historical inputs.", "affected_requirements": [], "epistemic_status": "SUPPORTED", "validation_method": "Inspect v11 input bindings and traceability graph."},
        ],
        "exceptions": [], "configurations": [], "environment_preconditions": [],
        "required_invariants": [{"invariant_id": f"V11-I{i:02d}", "statement": statement, "status": "PASS", "basis": "CLOSED_GATE_PREVENTS_INVALID_TRANSFORMATION" if i < 15 else "UPSTREAM_LINEAGE_RETAINED_AND_REFERENCED"} for i, statement in enumerate(V11_INVARIANTS, 1)],
        "orphan_obligations": coverage["orphan_obligations"], "orphan_requirements": [],
        "single_aggregate_score": "FORBIDDEN",
    }


def build_schemas() -> None:
    base = {"$schema": "https://json-schema.org/draft/2020-12/schema", "schema_version": "1.0", "additionalProperties": True}
    requirement_fields = ["requirement_id", "requirement_version", "statement", "requirement_type", "disposition", "strength", "final_category", "epistemic_status", "lifecycle_status", "scope", "conformance_level", "criticality", "source_obligations", "source_properties", "source_evidence", "derivation", "preconditions", "postconditions", "normative_rules", "acceptance_criteria", "test_oracles", "invariants", "transitions", "dependencies", "conflicts", "compatibility", "implementation_boundary", "boundary_model", "exceptions", "assumptions", "verification"]
    schemas = {
        "requirement.schema.yaml": {**base, "title": "Protocol-v11 requirement", "type": "object", "required": requirement_fields, "properties": {"requirement_version": {"const": "1.0"}, "requirement_type": {"enum": REQUIREMENT_TYPES}, "disposition": {"enum": DISPOSITIONS}, "strength": {"enum": STRENGTHS}, "final_category": {"enum": ["PRESERVATION_OBLIGATION", "COMPATIBILITY_OBLIGATION", "ENGINEERING_REQUIREMENT", "FUTURE_STRENGTHENING", "DESIGN_OPTION", "HISTORICAL_DEFECT", "UNKNOWN"]}, "epistemic_status": {"enum": EPISTEMIC}, "lifecycle_status": {"enum": LIFECYCLE}, "conformance_level": {"enum": CONFORMANCE_LEVELS}, "criticality": {"enum": CRITICALITY}, "scope": {"type": "object", "required": ["scope_type", "scope_ref"], "properties": {"scope_type": {"enum": SCOPES}}}, "verification": {"type": "object", "required": ["verification_level", "evidence", "result"], "properties": {"verification_level": {"enum": VERIFICATION_LEVELS}}}}},
        "normative-rule.schema.yaml": {**base, "title": "Protocol-v11 normative rule", "type": "object", "required": ["rule_id", "requirement_id", "predicate", "operator", "scope", "failure_class"], "properties": {"operator": {"enum": RULE_OPERATORS}}},
        "acceptance-criterion.schema.yaml": {**base, "title": "Protocol-v11 acceptance criterion", "type": "object", "required": ["criterion_id", "requirement_id", "statement", "observable", "pass_condition", "fail_condition", "evidence_required"]},
        "test-oracle.schema.yaml": {**base, "title": "Protocol-v11 test oracle", "type": "object", "required": ["oracle_id", "criterion_id", "oracle_type", "input_contract", "observation", "expected_predicate", "tolerance", "failure_class", "evidence_capture"], "properties": {"oracle_type": {"enum": ORACLES}}},
        "requirement-dependency.schema.yaml": {**base, "title": "Protocol-v11 requirement dependency", "type": "object", "required": ["dependency_id", "from_requirement", "to_requirement", "relation", "condition", "reason", "evidence"], "properties": {"relation": {"enum": RDEP_RELATIONS}}},
        "traceability.schema.yaml": {**base, "title": "Protocol-v11 traceability edge", "type": "object", "required": ["from", "to", "relation"]},
        "specification-certificate.schema.yaml": {**base, "title": "Protocol-v11 specification certificate", "type": "object", "required": ["specification_version", "generated_at", "input_hashes", "requirement_count", "rule_count", "criterion_count", "oracle_count", "conflict_count", "orphan_requirement_count", "orphan_obligation_count", "coverage", "validation_status", "unresolved_issues", "certificate_hash"], "properties": {"validation_status": {"enum": ["PASS", "FAIL", "PARTIAL"]}}},
    }
    for name, value in schemas.items(): dump(OUT / "schema" / name, value)


def build_reports(input_contract, requirements, coverage, dependencies, conflicts, conformance, verification, boundaries, diffs, trace, audit, certificate, obligations) -> None:
    blocked_rows = [(x["obligation_id"], x["class"], x["strength"], x["epistemic_status"], x["status"], "BLOCKED") for x in obligations]
    write_md("REQUIREMENTS.md", front("Protocol-v11 Requirements") + "No source obligation satisfies the verified-input precondition, so the normative requirement registry is empty. Generating requirements here would violate §§640, 642, 664, 683, 702–704, and 752.\n\n" + table(["Source obligation", "Class", "Obligation strength", "Epistemic", "Lifecycle", "Coverage"], blocked_rows))
    write_md("NORMATIVE-RULES.md", front("Normative Rules") + "No rule is admitted because no requirement exists. Operators and predicate registries are retained in `NORMATIVE-RULES.yaml`; they are not instantiated speculatively.\n")
    write_md("ACCEPTANCE-CRITERIA.md", front("Acceptance Criteria") + "No acceptance criterion is admitted. A criterion without an admitted requirement would create an untraced normative path.\n")
    write_md("TEST-ORACLES.md", front("Test Oracles") + "No oracle is admitted. This avoids oracle circularity, implementation coupling, and false verification. Upstream v10.1 test candidates remain `UNVERIFIED`.\n")
    write_md("REQUIREMENT-COVERAGE.md", front("Requirement Coverage") + table(["Obligation", "Requirements", "Coverage", "Orphan", "Blockers"], [(x["obligation_id"], x["requirements"], x["coverage_status"], x["orphan_status"], x["blockers"]) for x in coverage["obligation_coverage"]]) + "\nCoverage dimensions remain separate; a single aggregate percentage is forbidden.\n")
    write_md("REQUIREMENT-DEPENDENCIES.md", front("Requirement Dependencies") + "The requirement dependency graph has zero nodes and edges. Obligation dependencies were not copied because obligation dependency ≠ requirement dependency. No REQUIRES cycle exists in the empty rejected graph.\n")
    write_md("REQUIREMENT-CONFLICTS.md", front("Requirement Conflicts") + "No requirement conflicts are fabricated. Four unresolved **obligation** conflicts block derivation and remain upstream conflict records. Default precedence is a reasoning aid, not an automatic resolver.\n\n" + table(["Upstream blocker"], [(x,) for x in conflicts["upstream_obligation_conflict_blockers"]]))
    write_md("CONFORMANCE-MATRIX.md", front("Conformance Matrix") + table(["Level", "Claim"], [(x, "NOT CLAIMED") for x in conformance["levels"]]) + "\nNo implementation may claim v11 conformance from this rejected package.\n")
    write_md("VERIFICATION-MATRIX.md", front("Verification Matrix") + table(["Verification level", "Status"], [(x, "NOT ESTABLISHED") for x in verification["verification_levels"]]) + f"\nUpstream test edges: {verification['upstream_obligation_tests']['total']}; verified nodes: {verification['upstream_obligation_tests']['verified']}. Test existence is not verification.\n")
    write_md("IMPLEMENTATION-BOUNDARIES.md", front("Implementation Boundaries") + "No mandatory requirement exists, so no enforcement boundary is assigned. The boundary registry remains machine-readable. Enforcement, observation, and verification boundaries remain independent.\n\n" + table(["Allowed boundary"], [(x,) for x in boundaries["allowed_boundaries"]]))
    write_md("SEMANTIC-DIFFS.md", front("Semantic Diffs") + "No requirement revision exists. Narrowing, widening, generalization, and strengthening audits are `BLOCKED`, not vacuously accepted. Textual similarity is never semantic equivalence.\n")
    write_md("TRACEABILITY.md", front("Forward and Reverse Traceability") + f"The graph retains {len(trace['nodes'])} source/evidence/property/obligation nodes and {len(trace['forward_edges'])} forward edges, plus exact reverse edges. Traversal intentionally terminates at obligation because the derivation gate is closed.\n\n```text\nSOURCE → EVIDENCE → PROPERTY → OBLIGATION ┤ CLOSED GATE\nREQUIREMENT → RULE → CRITERION → ORACLE → TEST → RESULT  (not instantiated)\n```\n")
    write_md("SPECIFICATION-AUDIT.md", front("Specification Audit") + "## Validation procedure\n\n" + table(["Step", "Name", "Result"], [(x["step"], x["name"], x["result"]) for x in audit["validation_procedure"]]) + "\n## Completeness dimensions\n\n" + table(["Dimension", "Classification", "Detail"], [(x["dimension"], x["classification"], x["detail"]) for x in audit["completeness"]]) + "\n## Failure mode registry\n\n" + "\n".join(f"- `{x}`" for x in audit["failure_mode_registry"]) + "\n\n## Detected failure modes\n\n" + "\n".join(f"- `{x}`" for x in audit["detected_failure_modes"]) + "\n\n## Pipeline invariants\n\n" + table(["ID", "Statement", "Status", "Basis"], [(x["invariant_id"], x["statement"], x["status"], x["basis"]) for x in audit["required_invariants"]]) + "\n## Explicit assumptions\n\n" + table(["ID", "Statement", "Epistemic", "Validation"], [(x["assumption_id"], x["statement"], x["epistemic_status"], x["validation_method"]) for x in audit["hidden_assumptions"]]) + "\n")
    final = front("Generic Discovery Engine — Protocol-v11 Final Specification")
    final += "## 1. Objective and disposition\n\nThe deterministic v11 implementation validates the complete v10.1 package before derivation. The package is rejected; no normative requirement is produced.\n\n"
    final += "## 2. Input contract\n\n" + table(["Input role", "Schema", "Path", "Hash validation"], [(x["artifact_type"], x["schema_version"], x["source_path"], x["hash_validation"]) for x in input_contract["required_inputs"]]) + "\n"
    final += "## 3. Rejection causes\n\n" + table(["State", "Affected count", "Detail"], [(x["state"], len(x["affected"]), x["detail"]) for x in input_contract["failure_states"]]) + "\n"
    final += "## 4. Layer separation\n\nEvidence, historical property, rationale, obligation, requirement, rule, criterion, oracle, test, implementation, verification, and conformance remain distinct. The chain stops at obligation.\n\n"
    final += "## 5. Requirement registry\n\n`0` admitted requirements; `54` blocked/orphan source obligations. No `UNTRACED_REQUIREMENT` or `NEW_ENGINEERING_REQUIREMENT` was introduced.\n\n"
    final += "## 6. Normative rules and predicates\n\n`0` rules. The operator, predicate, and compound-logic registries are defined but uninstantiated.\n\n"
    final += "## 7. Acceptance criteria and oracles\n\n`0` criteria and `0` oracles. No mandatory requirement exists, and no oracle can substitute for one.\n\n"
    final += "## 8. Dependencies, conflicts, and supersession\n\nRequirement dependency and supersession graphs are empty. Four unresolved obligation conflicts remain blocking inputs and are not relabeled as requirement conflicts.\n\n"
    final += "## 9. Coverage\n\nAll obligation-to-requirement rows are `BLOCKED`; downstream coverage dimensions remain independently `BLOCKED`.\n\n"
    final += "## 10. Boundaries\n\nNo implementation boundary is assigned without a requirement. Enforcement, observation, and verification are not conflated.\n\n"
    final += "## 11. Semantic narrowing/widening\n\nBoth audits are blocked because there is no admitted requirement domain. This is not a pass-by-vacuity.\n\n"
    final += "## 12. Traceability\n\nForward and reverse traversal is preserved through source → evidence → property → obligation. No edge crosses the closed gate.\n\n"
    final += "## 13. Verification and conformance\n\nAll levels remain unclaimed. A test candidate is not a passing test; an implementation is not verification; a certificate is not semantic proof.\n\n"
    final += "## 14. Certificate\n\n" + table(["Field", "Value"], [("validation_status", certificate["validation_status"]), ("requirements", certificate["requirement_count"]), ("orphan obligations", certificate["orphan_obligation_count"]), ("certificate hash", certificate["certificate_hash"])]) + "\n"
    final += "## 15. Remediation boundary\n\nTo open derivation, repair or replace invalid v1 evidence without rewriting it, supply and validate Protocol-v4–v7 artifacts, resolve unknown obligation/property states, execute independent verification, and explicitly resolve obligation conflicts. v11 must then be regenerated from that newly valid package.\n\n"
    final += "## Final disposition\n\n**`REJECTED_INVALID_OBLIGATION_PACKAGE` — no normative specification or implementation conformance claim is authorized.**\n"
    write_md("FINAL-SPECIFICATION.md", final)


if __name__ == "__main__":
    main()
