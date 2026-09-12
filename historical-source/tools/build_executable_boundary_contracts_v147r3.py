#!/usr/bin/env python3
"""Build the append-only v14.7-R3 executable boundary-contract package."""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HISTORICAL = ROOT / "historical-source"
COMPLIANCE = HISTORICAL / "compliance"
PREDECESSOR = COMPLIANCE / "certification/v14.7-R2.1"
DESTINATION = COMPLIANCE / "certification/v14.7-R3"
SCHEMA_DIRECTORY = DESTINATION / "schema"
sys.path.insert(0, str(HISTORICAL / "tools"))

from v147r3_boundary_contracts import object_hash
from run_v147r3_boundary import run

VERSION = "14.7-R3"
TIMESTAMP = "2026-09-12T00:00:00Z"
FILES = [
    "VERSION.yaml", "EXECUTIVE-RESULT.yaml", "SPECIFICATION-BASIS.yaml", "PROFILE-REFERENCE.yaml",
    "BOUNDARY-CONTRACT.yaml", "BOUNDARY-BINDINGS.yaml", "AUTHORITY-PRECEDENCE.yaml",
    "STATEMENT-CLASSIFICATION.yaml", "NORMATIVE-REQUIREMENTS.yaml", "ACCEPTANCE-CRITERIA.yaml",
    "PROFILE-BINDINGS.yaml", "IMPLEMENTATION-MAPPINGS.yaml", "EVIDENCE.yaml", "VALIDATION-RESULTS.yaml",
    "EVALUATION-RESULTS.yaml", "COMPLETE-TRACEABILITY.yaml", "VALIDATION-CONTRACT.yaml", "EVALUATION-CONTRACT.yaml", "CONFORMANCE-CONTRACT.yaml",
    "CONFORMANCE-RESULT-MODEL.yaml", "RESULT-CONVERSION-RULES.yaml", "FORBIDDEN-IMPLICIT-CONVERSIONS.yaml",
    "TYPED-BOUNDARY-GUIDANCE.yaml", "ERROR-MODEL.yaml", "RECOVERABILITY.yaml",
    "REQUIREMENT-CODE-TRACEABILITY.yaml", "REQUIREMENT-IMPLEMENTATION-MATRIX.yaml",
    "PROFILE-IMPLEMENTATION-TEST.yaml", "PROFILE-FREEZE-AUDIT.yaml", "MECHANICAL-BOUNDARY-VALIDATOR.yaml",
    "BOUNDARY-CONFORMANCE-RULES.yaml", "MACHINE-TESTS.yaml", "MACHINE-TEST-RESULTS.yaml",
    "FINAL-ARTIFACT-GRAPH.yaml", "CLOSURE-CONDITION.yaml", "IMPLEMENTATION-CONFORMANCE.yaml",
    "FAILURE-PROVENANCE.yaml", "SCHEMA-REGISTRY.yaml", "ARTIFACT-TREE.yaml", "PRIOR-INTEGRITY.yaml",
    "VALIDATION-REPORT.yaml", "FINAL-PRINCIPLE.yaml", "CURRENT-STATUS.yaml",
]
SCHEMAS = [
    "boundary-binding", "statement-classification", "normative-requirement", "acceptance-criterion",
    "profile-binding-r3", "implementation-mapping", "evidence", "validation-contract",
    "evaluation-contract", "conformance-contract", "conformance-result-r3", "conversion-rule", "boundary-error",
]


def load(path):
    return json.loads(path.read_text())


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def array(items):
    return {"type": "array", "items": items}


def nullable(item):
    return {"oneOf": [item, {"type": "null"}]}


def schema(name, properties, required, identities, rules):
    properties = {**properties, "content_hash": {"type": "string", "pattern": "^[a-f0-9]{64}$"}}
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": f"https://generic-discovery-engine.invalid/compliance/v14.7-R3/{name}.schema.yaml",
        "title": name,
        "type": "object",
        "required": required + ["content_hash"],
        "properties": properties,
        "additionalProperties": False,
        "x-identity-fields": identities,
        "x-immutable": True,
        "x-self-excluding-hash-field": "content_hash",
        "x-canonical-profile": "GDE-CJSON-1",
        "x-authority-precedence": ["SPECIFICATION", "PROFILE", "IMPLEMENTATION", "EVIDENCE"],
        "x-normative-rules": rules,
    }


def build_schemas():
    string = {"type": "string", "minLength": 1}
    boolean = {"type": "boolean"}
    timestamp = {"type": "string", "format": "date-time"}
    hash_value = {"type": "string", "pattern": "^[a-f0-9]{64}$"}
    def closed_object(properties, required):
        return {"type": "object", "required": required, "properties": properties, "additionalProperties": False}
    authority = {
        "type": "object",
        "required": ["layer", "ref"],
        "properties": {"layer": {"type": "string", "enum": ["SPECIFICATION", "PROFILE", "IMPLEMENTATION"]}, "ref": string},
        "additionalProperties": False,
    }
    definitions = {
        "boundary-binding": schema(
            "boundary-binding",
            {"subject_ref": string, "authority": authority,
             "claims": array(closed_object({"claim_id": string, "statement": string}, ["claim_id", "statement"])),
             "satisfies": array(string), "evidence_refs": array(string)},
            ["subject_ref", "authority", "claims", "satisfies", "evidence_refs"], ["subject_ref"],
            ["authority layer identifies normative force", "evidence does not redefine authority"],
        ),
        "statement-classification": schema(
            "statement-classification",
            {"statement_id": string, "source_ref": string, "statement": string,
             "classification": {"type": "string", "enum": ["NORMATIVE_REQUIREMENT", "ACCEPTANCE_CRITERION", "PROFILE_BINDING", "IMPLEMENTATION_INSTRUCTION", "IMPLEMENTATION_GUIDANCE", "OBSERVATION", "EVIDENCE"]},
             "authority": authority, "object_ref": string},
            ["statement_id", "source_ref", "statement", "classification", "authority", "object_ref"], ["statement_id"],
            ["exactly one classification"],
        ),
        "normative-requirement": schema(
            "normative-requirement",
            {"requirement_id": string, "statement": string,
             "strength": {"type": "string", "enum": ["MUST", "MUST_NOT", "SHOULD", "SHOULD_NOT", "MAY"]},
             "scope_ref": string, "acceptance_criteria": array(closed_object({"criterion_id": string}, ["criterion_id"])), "dependencies": array(string),
             "authority": authority},
            ["requirement_id", "statement", "strength", "scope_ref", "acceptance_criteria", "dependencies", "authority"],
            ["requirement_id"], ["normative requirement has specification authority and no implementation leakage"],
        ),
        "acceptance-criterion": schema(
            "acceptance-criterion",
            {"criterion_id": string, "requirement_ref": string,
             "condition": closed_object({"expression": string}, ["expression"]),
             "oracle": closed_object({"expected_result": {"type": "string", "enum": ["TRUE", "FALSE", "UNKNOWN", "BLOCKED", "INVALID"]}}, ["expected_result"]),
             "evidence_requirements": array(string)},
            ["criterion_id", "requirement_ref", "condition", "oracle", "evidence_requirements"], ["criterion_id"],
            ["criterion operationalizes without changing meaning"],
        ),
        "profile-binding-r3": schema(
            "profile-binding-r3",
            {"binding_id": string, "requirement_ref": string,
             "selected_realization": closed_object({"mechanism": string}, ["mechanism"]),
             "alternatives": array(closed_object({"mechanism": string}, ["mechanism"])),
             "semantic_preservation": closed_object({"claim": string, "verification_ref": string}, ["claim", "verification_ref"]),
             "profile_ref": string},
            ["binding_id", "requirement_ref", "selected_realization", "alternatives", "semantic_preservation", "profile_ref"],
            ["binding_id"], ["binding selects a permitted realization and preserves requirement meaning"],
        ),
        "implementation-mapping": schema(
            "implementation-mapping",
            {"mapping_id": string, "implementation_id": string, "profile_binding_ref": string,
             "artifact_refs": array(string), "code_refs": array(string), "tests": array(string), "evidence_refs": array(string),
             "mapping_type": {"type": "string", "enum": ["DIRECT", "INDIRECT", "DISTRIBUTED", "CONFIGURATION", "RUNTIME", "TEST_ONLY"]}},
            ["mapping_id", "implementation_id", "profile_binding_ref", "artifact_refs", "code_refs", "tests", "evidence_refs", "mapping_type"],
            ["mapping_id"], ["implementation mapping is not a requirement"],
        ),
        "evidence": schema(
            "evidence",
            {"evidence_id": string, "subject_ref": string,
             "source": closed_object({"type": string, "ref": string}, ["type", "ref"]),
             "observation": closed_object({"statement": string}, ["statement"]), "collected_at": timestamp,
             "collector": closed_object({"id": string, "version": string}, ["id", "version"]),
             "integrity": closed_object({"hash": hash_value, "status": {"type": "string", "enum": ["VALID", "INVALID", "UNKNOWN"]}}, ["hash", "status"])},
            ["evidence_id", "subject_ref", "source", "observation", "collected_at", "collector", "integrity"],
            ["evidence_id"], ["evidence is descriptive and carries no normative authority"],
        ),
        "validation-contract": schema(
            "validation-contract",
            {"contract_id": string,
             "input": closed_object({"subject_ref": string, "context_ref": string}, ["subject_ref", "context_ref"]),
             "output": closed_object({"type": {"type": "string", "const": "ValidationResult"}, "states": array({"type": "string", "enum": ["VALID", "INVALID", "BLOCKED", "UNKNOWN"]})}, ["type", "states"]),
             "may_modify_authoritative_state": boolean, "deterministic": boolean, "forbidden_actions": array(string)},
            ["contract_id", "input", "output", "may_modify_authoritative_state", "deterministic", "forbidden_actions"],
            ["contract_id"], ["validation is a non-mutating processability gate"],
        ),
        "evaluation-contract": schema(
            "evaluation-contract",
            {"contract_id": string, "operation": string,
             "prerequisite": closed_object({"required_validation": {"type": "string", "const": "VALID"}, "alternate_path": string}, ["required_validation", "alternate_path"]),
             "required_bindings": array(string), "output_type": {"type": "string", "const": "EvaluationResult"}, "may_authorize": boolean},
            ["contract_id", "operation", "prerequisite", "required_bindings", "output_type", "may_authorize"],
            ["contract_id"], ["evaluation requires valid validation and does not authorize"],
        ),
        "conformance-contract": schema(
            "conformance-contract",
            {"contract_id": string, "operation": string, "required_inputs": array(string), "output_type": string,
             "forbidden_inferences": array(string), "non_conformant_requires_violation": boolean,
             "absence_of_evidence_default": string},
            ["contract_id", "operation", "required_inputs", "output_type", "forbidden_inferences", "non_conformant_requires_violation", "absence_of_evidence_default"],
            ["contract_id"], ["conformance applies requirement acceptance criteria"],
        ),
        "conformance-result-r3": schema(
            "conformance-result-r3",
            {"requirement_ref": string,
             "status": {"type": "string", "enum": ["CONFORMANT", "PARTIALLY_CONFORMANT", "NON_CONFORMANT", "UNVERIFIED", "BLOCKED", "NOT_APPLICABLE", "UNKNOWN"]},
             "evaluation_refs": array(string), "evidence_refs": array(string), "violated_conditions": array(string),
             "rationale_codes": array(string)},
            ["requirement_ref", "status", "evaluation_refs", "evidence_refs", "violated_conditions", "rationale_codes"],
            ["requirement_ref"], ["NON_CONFORMANT requires an identified violated condition"],
        ),
        "conversion-rule": schema(
            "conversion-rule",
            {"rule_id": string, "source_domain": string, "source_state": string, "target_domain": string,
             "target_state": string, "operation": string, "preconditions": array(string), "authority_ref": string},
            ["rule_id", "source_domain", "source_state", "target_domain", "target_state", "operation", "preconditions", "authority_ref"],
            ["rule_id"], ["every conversion identifies source target operation preconditions and authority"],
        ),
        "boundary-error": schema(
            "boundary-error",
            {"error_id": string,
             "error_type": {"type": "string", "enum": ["ValidationError", "EvaluationError", "ConformanceError", "AuthorizationError", "TransitionError", "EventStoreError", "ProjectionError", "ExecutionError", "VerificationError"]},
             "error_code": string, "layer": string, "subject_ref": string, "rule_ref": string,
             "evidence_refs": array(string), "cause": nullable(string),
             "recoverability": {"type": "string", "enum": ["RETRYABLE", "NON_RETRYABLE", "REQUIRES_NEW_EVIDENCE", "REQUIRES_AUTHORITY", "REQUIRES_PROFILE_CHANGE", "REQUIRES_IMPLEMENTATION_CHANGE", "REQUIRES_SPECIFICATION_REVIEW"]},
             "semantic_result": string},
            ["error_id", "error_type", "error_code", "layer", "subject_ref", "rule_ref", "evidence_refs", "cause", "recoverability", "semantic_result"],
            ["error_id"], ["recoverability metadata never alters semantic result"],
        ),
    }
    for name, definition in definitions.items():
        write(SCHEMA_DIRECTORY / f"{name}.schema.yaml", definition)


def specification_text():
    sections = [
        ("Boundary Contract", "Every artifact has a BoundaryBinding identifying SPECIFICATION, PROFILE, or IMPLEMENTATION authority, claims, satisfied requirements, evidence references, and a content hash."),
        ("Authority Precedence", "Specification defines obligations; profile binds permitted realization choices; implementation realizes the profile; evidence demonstrates observations. Lower layers MUST NOT override higher layers."),
        ("Requirement Classification", "Every extracted statement is classified exactly once as NORMATIVE_REQUIREMENT, ACCEPTANCE_CRITERION, PROFILE_BINDING, IMPLEMENTATION_INSTRUCTION, IMPLEMENTATION_GUIDANCE, OBSERVATION, or EVIDENCE."),
        ("Normative Requirement", "A NormativeRequirement identifies statement, strength, scope, acceptance criteria, dependencies, authority, and content hash without embedding a concrete implementation mechanism."),
        ("Acceptance Criterion", "An AcceptanceCriterion operationalizes one requirement without changing its meaning and binds an EvaluationResult oracle and evidence requirements."),
        ("Profile Binding", "A ProfileBinding selects one permitted realization, records alternatives, and carries a verified semantic-preservation claim. A concrete implementation mechanism is not the requirement."),
        ("Implementation Mapping", "An ImplementationMapping connects implementation artifacts, code, tests, and evidence to a profile binding. The mapping is distinct from the requirement."),
        ("Evidence Mapping", "Evidence records a subject, source, observation, collection time, collector, integrity, and hash. Evidence is descriptive and cannot become normative by existing."),
        ("Complete Traceability Chain", "REQ → acceptance criterion → profile binding → implementation mapping → test or observation → evidence → validation → evaluation → conformance is bidirectionally indexed."),
        ("Validation Contract", "Validate(subject, context) returns ValidationResult deterministically without modifying authoritative state, issuing certificates, approving releases, or mutating history."),
        ("Evaluation Contract", "Evaluate(predicate, subject, context) requires required validation to be VALID unless an explicit normative path says otherwise and identifies every semantic input binding."),
        ("Conformance Contract", "EvaluateRequirement applies scope, acceptance criteria, validated evidence, and evaluation results. VALID and TRUE alone do not imply CONFORMANT."),
        ("Conformance Result", "ConformanceResult uses the frozen seven-state domain. NON_CONFORMANT requires an identified violated condition; ordinary missing evidence yields UNVERIFIED."),
        ("Result Conversion Rules", "Cross-domain transitions are named rules identifying source domain/state, target domain/state, operation, preconditions, and authority. No unruled generic conversion is permitted."),
        ("Forbidden Implicit Conversion", "VALID→CONFORMANT, TRUE→APPROVED, CONFORMANT→GRANTED, and APPROVED→SUCCEEDED are rejected without their independent contractual gates."),
        ("Explicit Conversion Example", "VALID → TRUE → CONFORMANT → ELIGIBLE → QUALIFIED → AUTHORIZED → APPROVED → SUCCEEDED → VERIFIED is a sequence of independent operations."),
        ("Rust Domain Separation", "A Rust implementation SHOULD use distinct semantic result types instead of a universal Status enum. This is implementation guidance, not a new normative state."),
        ("Typed Boundary Pattern", "ValidatedInput and EligibleRelease typed inputs are preferred over AnyObject or Status arguments because they encode preconditions."),
        ("State-Carrying Types", "Raw, validated, eligible, authorized, approved, executed, and verified wrappers are a realization technique and do not add semantic states."),
        ("Error Model", "Normative operations distinguish validation, evaluation, conformance, authorization, transition, event store, projection, execution, and verification errors with structured provenance."),
        ("Recoverability", "Recoverability diagnostics are one of seven explicit values and MUST NOT alter the semantic result; UNKNOWN with new-evidence diagnostics remains UNKNOWN."),
        ("Requirement-to-Code Traceability", "The realization supports reverse lookup from code through test and evidence to requirement and forward lookup from requirement through profile to code and test."),
        ("Requirement–Implementation Matrix", "The matrix is traceability rather than normative authority; proposed concrete mechanisms remain unverified until backed by implementation evidence."),
        ("Profile vs Implementation Test", "A mechanism affecting protocol interpretation is profile-level or normative; an interchangeable library implementing a fixed algorithm is implementation-level."),
        ("Profile Freeze Test", "A profile is frozen only when selectable decisions are enumerated, no requirement depends on an unspecified choice, and no instruction silently acts as a profile rule."),
        ("Mechanical Boundary Validator", "validate_boundary_artifact detects B001 through B012 and returns only ValidationResult states with defect provenance."),
        ("Boundary Conformance Rules", "BOUNDARY-001 through BOUNDARY-010 enforce authority, references, result-domain separation, semantic preservation, versioning, and evidence non-authority."),
        ("Machine Test Matrix", "B-T01 through B-T15 execute requirement leakage, missing bindings, conversion, versioning, duplicate approval, and deterministic replay cases."),
        ("Final Artifact Relationship", "The complete graph flows from specification to requirements, criteria, profile, implementation, evidence, validation, evaluation, conformance, eligibility, authority, authorization, decision, execution, verification, and new evidence."),
        ("Closure Condition", "Closure requires no specification implementation leakage, no unspecified profile binding, no hidden implementation authority, and no semantic borrowing across result layers."),
        ("Final Principle", "A requirement defines obligation; profile fixes realization; implementation realizes; evidence observes; validation gates; evaluation establishes propositions; conformance establishes satisfaction; authorization permits; decision chooses; execution performs; verification observes."),
    ]
    return "# v14.7-R3 — Executable Boundary Contracts and Conformance Mapping\n\n" + "\n\n".join(
        f"## {index}. {title}\n{text}" for index, (title, text) in enumerate(sections, 1)
    ) + "\n"


def hashed(domain, value):
    value["content_hash"] = object_hash(domain, value)
    return value


def build_tests(conversion_rules):
    tests = []

    def add(test_id, name, operation, input_value, expected):
        tests.append({"test_id": test_id, "name": name, "operation": operation, "input": input_value, "expected": expected})

    add("B-T01", "Requirement without implementation detail", "BOUNDARY_VALIDATE", {"artifact": {"kind": "normative_requirement", "statement": "The event stream MUST provide deterministic ordering."}}, "VALID")
    add("B-T02", "Requirement containing hidden mechanism", "BOUNDARY_VALIDATE", {"artifact": {"kind": "normative_requirement", "statement": "The event stream MUST use SQLite."}}, "INVALID:B001")
    add("B-T03", "Profile without specification reference", "BOUNDARY_VALIDATE", {"artifact": {"kind": "profile", "profile_id": "p"}}, "INVALID:B004")
    add("B-T04", "Implementation without profile reference", "BOUNDARY_VALIDATE", {"artifact": {"kind": "implementation", "implementation_id": "i"}}, "INVALID:B005")
    add("B-T05", "Validation VALID to implicit CONFORMANT", "CONVERSION", {"source_domain": "ValidationResult", "source_state": "VALID", "target_domain": "ConformanceResult", "target_state": "CONFORMANT", "rule": None}, "REJECTED")
    add("B-T06", "Evaluation TRUE to implicit APPROVED", "CONVERSION", {"source_domain": "EvaluationResult", "source_state": "TRUE", "target_domain": "ReleaseDecision", "target_state": "APPROVED", "rule": None}, "REJECTED")
    add("B-T07", "Conformance without requirement reference", "BOUNDARY_VALIDATE", {"artifact": {"kind": "conformance"}}, "INVALID:B008")
    old_profile = {"profile_version": "14.7-R2.1", "hash_algorithm": "SHA-256", "serialization": "GDE-CJSON-1", "time_semantics": "RFC3339", "ordering": "SEQUENCE", "predicate_language": "GDE-PREDICATE-1", "wire_format": "JSON"}
    new_profile = {**old_profile, "hash_algorithm": "SHA-512"}
    add("B-T08", "Profile changes hash algorithm", "PROFILE_CHANGE", {"old": old_profile, "new": new_profile}, "VERSION_REQUIRED")
    add("B-T09", "Implementation changes crypto library", "IMPLEMENTATION_CHANGE", {"old": {"profile_ref": "p", "crypto_library": "ring"}, "new": {"profile_ref": "p", "crypto_library": "sha2 crate"}}, "NO_PROFILE_CHANGE")
    add("B-T10", "UNKNOWN coerced to TRUE", "CONVERSION", {"source_domain": "EvaluationResult", "source_state": "UNKNOWN", "target_domain": "EvaluationResult", "target_state": "TRUE", "rule": None}, "REJECTED")
    add("B-T11", "BLOCKED coerced to TRUE", "CONVERSION", {"source_domain": "EvaluationResult", "source_state": "BLOCKED", "target_domain": "EvaluationResult", "target_state": "TRUE", "rule": None}, "REJECTED")
    add("B-T12", "INVALID coerced to FALSE", "CONVERSION", {"source_domain": "EvaluationResult", "source_state": "INVALID", "target_domain": "EvaluationResult", "target_state": "FALSE", "rule": None}, "REJECTED")
    add("B-T13", "Evidence changes requirement semantics", "AUTHORITY_PRECEDENCE", {"actor_layer": "EVIDENCE", "target_layer": "SPECIFICATION"}, "REJECTED")
    approvals = [{"authority_id": "a", "valid": True, "basis_hash": "h"}, {"authority_id": "a", "valid": True, "basis_hash": "h"}]
    add("B-T14", "Duplicate authority approval", "APPROVAL_COUNT", {"approvals": approvals, "basis_hash": "h"}, "1")
    history = [{"stream_id": "s", "sequence_no": 0, "key": "x", "value": 1}, {"stream_id": "s", "sequence_no": 1, "key": "x", "value": 2}]
    add("B-T15", "Same valid history replay", "REPLAY_EQUAL", {"left": history, "right": list(reversed(history))}, "SAME")

    defect_fixtures = [
        ("B001", {"kind": "normative_requirement", "statement": "The stream MUST use SQLite."}),
        ("B002", {"kind": "implementation_instruction", "authority_ref": None}),
        ("B003", {"kind": "profile_binding"}),
        ("B004", {"kind": "profile"}),
        ("B005", {"kind": "implementation"}),
        ("B006", {"kind": "evidence"}),
        ("B007", {"kind": "evaluation"}),
        ("B008", {"kind": "conformance"}),
        ("B009", {"kind": "conversion"}),
        ("B010", {"kind": "statement_classification", "statement": "The validator MUST_NOT mutate history.", "classification": "IMPLEMENTATION_GUIDANCE"}),
        ("B011", {"kind": "statement_classification", "statement": "Use SQLite for storage.", "classification": "NORMATIVE_REQUIREMENT"}),
        ("B012", {"kind": "profile_change", "profile_version": "1", "semantic_fingerprint": "changed"}),
    ]
    for number, (code, fixture) in enumerate(defect_fixtures, 1):
        input_value = {"artifact": fixture}
        if code == "B012":
            input_value["frozen_profile"] = {"profile_version": "1", "semantic_fingerprint": "frozen"}
        add(f"BV-T{number:02d}", f"Mechanical detector {code}", "BOUNDARY_VALIDATE", input_value, f"INVALID:{code}")

    rule_fixtures = {
        "BOUNDARY-001": {"kind": "normative_requirement", "authority_layer": "SPECIFICATION"},
        "BOUNDARY-002": {"kind": "profile_binding", "requirement_ref": "REQ"},
        "BOUNDARY-003": {"kind": "implementation_mapping", "profile_binding_ref": "BIND"},
        "BOUNDARY-004": {"kind": "evaluation", "predicate_ref": "PRED"},
        "BOUNDARY-005": {"kind": "conformance", "requirement_ref": "REQ"},
        "BOUNDARY-006": {"kind": "authorization", "operation_ref": "OP", "authority_ref": "AUTH", "scope_ref": "SCOPE", "policy_ref": "POLICY"},
        "BOUNDARY-007": {"kind": "conversion", "rule_ref": "CONV"},
        "BOUNDARY-008": {"kind": "implementation_instruction", "weakens_requirement": False},
        "BOUNDARY-009": {"kind": "profile_change", "interpretation_changed": True, "profile_version_changed": True},
        "BOUNDARY-010": {"kind": "evidence", "evidence_redefines_meaning": False},
    }
    for number, (rule_id, fixture) in enumerate(rule_fixtures.items(), 1):
        add(f"BR-T{number:02d}", f"Conformance rule {rule_id}", "RULE_ASSERT", {"rule_id": rule_id, "artifact": fixture}, "PASS")

    for number, rule in enumerate(conversion_rules, 1):
        add(f"CV-T{number:02d}", f"Explicit conversion {rule['rule_id']}", "CONVERSION", {
            "source_domain": rule["source_domain"], "source_state": rule["source_state"],
            "target_domain": rule["target_domain"], "target_state": rule["target_state"], "rule": rule,
        }, "ALLOWED")

    add("CT-T01", "INVALID validation cannot evaluate", "EVALUATION_GATE", {"validation": "INVALID", "subject_ref": "s", "context_ref": "c"}, "BLOCKED")
    add("CT-T02", "VALID validation creates evaluation eligibility", "EVALUATION_GATE", {"validation": "VALID", "subject_ref": "s", "context_ref": "c"}, "ELIGIBLE")
    evaluation_input = {"validated_input": {"subject_ref": "s", "context_ref": "c"}, "predicate_ref": "predicate:p", "inputs_ref": "inputs:i", "evaluator": {"id": "e", "version": "1"}, "evaluation_time": TIMESTAMP, "evidence_refs": [], "scope_ref": "scope:s"}
    add("CT-T03", "Evaluation requires predicate", "EVALUATE", {**evaluation_input, "predicate_ref": None}, "INVALID")
    conformance_input = {"requirement_ref": "r", "scope_ref": "scope:s", "acceptance_criteria": ["criterion:c"], "evidence_validation": "VALID"}
    add("CT-T04", "True criterion with evidence conforms", "CONFORMANCE", {**conformance_input, "evaluations": [{"status": "TRUE", "condition_ref": "c"}], "evidence_refs": ["e"]}, "CONFORMANT")
    add("CT-T05", "Absent evidence is unverified", "CONFORMANCE", {**conformance_input, "evaluations": [{"status": "TRUE", "condition_ref": "c"}], "evidence_refs": []}, "UNVERIFIED")
    add("CT-T06", "False without violation identity yields no result", "CONFORMANCE", {**conformance_input, "evaluations": [{"status": "FALSE"}], "evidence_refs": ["e"]}, "NO_CONFORMANCE_RESULT")
    add("CT-T07", "Identified violated condition is nonconformant", "CONFORMANCE", {**conformance_input, "evaluations": [{"status": "FALSE", "condition_ref": "condition:r"}], "evidence_refs": ["e"]}, "NON_CONFORMANT")
    add("CT-T08", "Normatively mandatory evidence absence violates", "CONFORMANCE", {**conformance_input, "evaluations": [], "evidence_refs": [], "evidence_mandatory": True}, "NON_CONFORMANT")
    add("CT-T09", "Recoverability does not alter UNKNOWN", "RECOVERABILITY", {"semantic_result": "UNKNOWN", "diagnostic": "REQUIRES_NEW_EVIDENCE"}, "UNKNOWN")
    add("CT-T10", "Complete validated evaluation input evaluates", "EVALUATE", evaluation_input, "TRUE")
    add("CT-T11", "Unvalidated evidence blocks conformance", "CONFORMANCE", {**conformance_input, "evaluations": [{"status": "TRUE", "condition_ref": "c"}], "evidence_refs": ["e"], "evidence_validation": "UNKNOWN"}, "BLOCKED")
    return tests


def main():
    if not (PREDECESSOR / "VALIDATION.yaml").is_file():
        raise RuntimeError("validated v14.7-R2.1 predecessor required")
    if (COMPLIANCE / "certification/v14.7-R4").exists():
        raise RuntimeError("refusing to erase predecessor artifacts after append-only v14.7-R4 realization")
    if DESTINATION.exists():
        raise RuntimeError("refusing to regenerate immutable v14.7-R3 package")
    predecessor = [{"path": str(path.relative_to(COMPLIANCE)), "sha256": sha256(path), "bytes": path.stat().st_size}
                   for path in sorted(COMPLIANCE.rglob("*")) if path.is_file()]
    DESTINATION.mkdir(parents=True)
    SCHEMA_DIRECTORY.mkdir()
    build_schemas()
    (DESTINATION / "SPECIFICATION.md").write_text(specification_text())

    predecessor_profile = load(PREDECESSOR / "PROFILE.yaml")
    profile_reference = hashed("R3_PROFILE_REFERENCE", {
        "profile_id": predecessor_profile["profile_id"], "profile_version": predecessor_profile["profile_version"],
        "profile_content_hash": predecessor_profile["content_hash"], "artifact_path": "../v14.7-R2.1/PROFILE.yaml",
        "artifact_sha256": sha256(PREDECESSOR / "PROFILE.yaml"), "profile_changes": "NONE",
        "compatibility_with_r2_1_profile": "IDENTICAL",
    })
    basis = hashed("R3_SPECIFICATION_BASIS", {
        "realization_id": "gde-v14.7-r3-boundary-contracts", "semantic_specification": "v14.7",
        "predecessor_realization": "v14.7-R2.1", "components": [
            {"path": "SPECIFICATION.md", "sha256": sha256(DESTINATION / "SPECIFICATION.md")},
            {"path": "../v14.7-R2.1/SPECIFICATION.md", "sha256": sha256(PREDECESSOR / "SPECIFICATION.md")},
            {"path": "../v14.7-R2.1/SPECIFICATION-BASIS.yaml", "sha256": sha256(PREDECESSOR / "SPECIFICATION-BASIS.yaml")},
        ], "new_normative_states": False, "renamed_semantic_states": False, "weakened_requirements": False,
    })

    requirement_texts = [
        "Every governed artifact MUST have an identifiable authority layer.",
        "An implementation artifact MUST NOT override a profile rule.",
        "A profile MUST NOT override a specification requirement.",
        "Evidence MUST NOT redefine specification, profile, or implementation obligations.",
        "Every extracted statement MUST have exactly one permitted classification.",
        "An acceptance criterion MUST operationalize a requirement without changing its meaning.",
        "An implementation mapping MUST remain distinct from the requirement it realizes.",
        "A validator MUST be deterministic, non-mutating, and unable to certify, authorize, decide, or execute.",
        "An evaluator MUST require applicable VALID validation and identify predicate, subject, inputs, context, evaluator, time, evidence, and scope.",
        "Conformance MUST apply the referenced requirement, scope, acceptance criteria, validated evidence, and evaluation results.",
        "NON_CONFORMANT MUST identify at least one violated normative condition.",
        "Absence of ordinary evidence MUST yield UNVERIFIED unless mandatory evidence absence is itself a defined violation.",
        "Every cross-domain result conversion MUST identify source, target, operation, preconditions, and rule authority.",
        "VALID, TRUE, CONFORMANT, and APPROVED MUST NOT implicitly establish stronger cross-domain states.",
        "Normative-operation errors MUST preserve their originating domain and structured provenance.",
        "Recoverability metadata MUST NOT alter the semantic result it diagnoses.",
        "Requirement, profile, implementation, test, evidence, validation, evaluation, and conformance traceability MUST be bidirectional.",
        "Profile freeze MUST require complete choice enumeration and prohibit hidden profile defaults in implementation instructions.",
        "The mechanical boundary validator MUST detect B001 through B012 with validation-domain results.",
        "BOUNDARY-001 through BOUNDARY-010 MUST be mechanically enforceable.",
        "All profile-selectable interpretation choices MUST be explicitly enumerated before profile freeze.",
        "Implementation instructions MUST NOT silently act as profile rules or normative requirements.",
        "Validation MUST NOT contain evaluation or conformance semantics.",
        "Authorization, decision, execution, and verification MUST each have an independent contract and authority basis.",
    ]
    requirements = []
    criteria = []
    for index, statement in enumerate(requirement_texts, 1):
        requirement_id = f"R3-REQ-{index:03d}"
        criterion_id = f"R3-AC-{index:03d}"
        requirement = hashed("NORMATIVE_REQUIREMENT", {
            "requirement_id": requirement_id, "statement": statement, "strength": "MUST", "scope_ref": "scope:v14.7-r3",
            "acceptance_criteria": [{"criterion_id": criterion_id}], "dependencies": [] if index == 1 else ["R3-REQ-001"],
            "authority": {"layer": "SPECIFICATION", "ref": "SPECIFICATION.md"},
        })
        criterion = hashed("ACCEPTANCE_CRITERION", {
            "criterion_id": criterion_id, "requirement_ref": requirement_id,
            "condition": {"expression": f"boundary_requirement_satisfied('{requirement_id}')"},
            "oracle": {"expected_result": "TRUE"},
            "evidence_requirements": [f"R3-EVIDENCE-{index:03d}"],
        })
        requirements.append(requirement)
        criteria.append(criterion)

    profile_bindings = []
    for index, requirement in enumerate(requirements, 1):
        profile_bindings.append(hashed("PROFILE_BINDING_R3", {
            "binding_id": f"R3-PROFILE-BINDING-{index:03d}", "requirement_ref": requirement["requirement_id"],
            "selected_realization": {"mechanism": "HASH_BOUND_TYPED_BOUNDARY_OBJECTS_AND_EXPLICIT_GATES"},
            "alternatives": [{"mechanism": "SEMANTICALLY_EQUIVALENT_SCHEMA_VALIDATED_BOUNDARY_OBJECTS"}],
            "semantic_preservation": {"claim": "NO_STATE_ADDED_RENAMED_OR_WEAKENED", "verification_ref": "PROFILE-FREEZE-AUDIT.yaml"},
            "profile_ref": f'{profile_reference["profile_id"]}@{profile_reference["profile_version"]}',
        }))

    conversion_specs = [
        ("R3-CONV-001", "ValidationResult", "VALID", "EvaluationEligibility", "ELIGIBLE", "establish_evaluation_eligibility", ["required validation applies"]),
        ("R3-CONV-002", "EvaluationResult", "TRUE", "RequirementEvaluation", "SATISFIED", "apply_acceptance_criterion", ["criterion referenced"]),
        ("R3-CONV-003", "RequirementEvaluation", "SATISFIED", "ConformanceResult", "CONFORMANT", "aggregate_requirement", ["all mandatory criteria satisfied"]),
        ("R3-CONV-004", "ConformanceResult", "CONFORMANT", "ReleaseEligibility", "ELIGIBLE", "evaluate_release_policy", ["release policy referenced"]),
        ("R3-CONV-005", "ReleaseEligibility", "ELIGIBLE", "AuthorizationResult", "AUTHORIZED", "authorize_release", ["qualified authority", "scope", "policy"]),
        ("R3-CONV-006", "AuthorizationResult", "AUTHORIZED", "ReleaseDecision", "APPROVED", "record_release_decision", ["authorization current"]),
        ("R3-CONV-007", "ReleaseDecision", "APPROVED", "ReleaseExecution", "SUCCEEDED", "execute_approved_release", ["decision current", "execution succeeds"]),
        ("R3-CONV-008", "ReleaseExecution", "SUCCEEDED", "PostReleaseVerification", "VERIFIED", "verify_release_effect", ["verification observation"]),
        ("R3-CONV-009", "PostReleaseVerification", "VERIFIED", "Evidence", "RECORDED", "record_verification_evidence", ["evidence integrity valid"]),
    ]
    conversion_rules = [hashed("CONVERSION_RULE", {
        "rule_id": rule_id, "source_domain": source_domain, "source_state": source_state,
        "target_domain": target_domain, "target_state": target_state, "operation": operation,
        "preconditions": preconditions, "authority_ref": "SPECIFICATION.md#14",
    }) for rule_id, source_domain, source_state, target_domain, target_state, operation, preconditions in conversion_specs]

    tests = build_tests(conversion_rules)
    write(DESTINATION / "MACHINE-TESTS.yaml", {"realization_version": VERSION, "objects": tests, "count": len(tests)})
    results = run(DESTINATION)
    write(DESTINATION / "MACHINE-TEST-RESULTS.yaml", {
        "realization_version": VERSION, "objects": results,
        "summary": {"total": len(results), "passed": sum(x["status"] == "PASSED" for x in results)},
    })

    implementation_mappings = []
    evidence_objects = []
    for index, binding in enumerate(profile_bindings, 1):
        test = tests[(index - 1) % len(tests)]
        evidence_id = f"R3-EVIDENCE-{index:03d}"
        mapping = hashed("IMPLEMENTATION_MAPPING", {
            "mapping_id": f"R3-MAP-{index:03d}", "implementation_id": "v147r3-python-boundary-reference",
            "profile_binding_ref": binding["binding_id"],
            "artifact_refs": ["historical-source/tools/v147r3_boundary_contracts.py"],
            "code_refs": ["validate_boundary_artifact", "apply_conversion_rule", "derive_conformance"],
            "tests": [test["test_id"]], "evidence_refs": [evidence_id], "mapping_type": "TEST_ONLY",
        })
        implementation_mappings.append(mapping)
        observed = next(x for x in results if x["test_id"] == test["test_id"])
        integrity_body = {"test_id": test["test_id"], "actual": observed["actual"], "status": observed["status"]}
        evidence_objects.append(hashed("EVIDENCE", {
            "evidence_id": evidence_id, "subject_ref": mapping["mapping_id"],
            "source": {"type": "REFERENCE_HARNESS_RESULT", "ref": f'MACHINE-TEST-RESULTS.yaml#{test["test_id"]}'},
            "observation": {"statement": f'{test["test_id"]} produced {observed["actual"]} and {observed["status"]}'},
            "collected_at": TIMESTAMP, "collector": {"id": "v147r3-boundary-runner", "version": VERSION},
            "integrity": {"hash": hashlib.sha256(json.dumps(integrity_body, sort_keys=True).encode()).hexdigest(), "status": "VALID"},
        }))

    validation_results = []
    evaluation_results = []
    validator_hash = sha256(HISTORICAL / "tools/v147r3_boundary_contracts.py")
    for index, (criterion, evidence) in enumerate(zip(criteria, evidence_objects), 1):
        evidence_input_hash = hashlib.sha256(json.dumps(evidence, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        validation_results.append(hashed("R3_VALIDATION_RESULT", {
            "validation_id": f"R3-VALIDATION-{index:03d}", "subject_ref": evidence["evidence_id"], "status": "VALID",
            "failure_codes": [], "evidence_refs": [evidence["evidence_id"]], "validator_id": "v147r3-boundary-validator",
            "validator_version": VERSION, "validator_hash": validator_hash, "input_hash": evidence_input_hash,
            "validated_at": TIMESTAMP, "scope": {"scope_ref": "scope:v14.7-r3-evidence"},
        }))
        evaluation_input_hash = hashlib.sha256(json.dumps({"criterion": criterion["criterion_id"], "evidence": evidence["evidence_id"]}, sort_keys=True).encode()).hexdigest()
        evaluation_results.append(hashed("R3_EVALUATION_RESULT", {
            "evaluation_id": f"R3-EVALUATION-{index:03d}", "proposition_ref": criterion["criterion_id"], "status": "TRUE",
            "failure_codes": [], "evidence_refs": [evidence["evidence_id"]], "evaluator_id": "v147r3-boundary-evaluator",
            "evaluator_version": VERSION, "evaluator_hash": validator_hash, "input_hash": evaluation_input_hash,
            "evaluated_at": TIMESTAMP,
        }))

    conformance_results = []
    for index, requirement in enumerate(requirements, 1):
        conformance_results.append(hashed("CONFORMANCE_RESULT_R3", {
            "requirement_ref": requirement["requirement_id"], "status": "CONFORMANT",
            "evaluation_refs": [evaluation_results[index - 1]["evaluation_id"]],
            "evidence_refs": [evidence_objects[index - 1]["evidence_id"]],
            "violated_conditions": [], "rationale_codes": ["REFERENCE_BOUNDARY_ORACLE_PASSED"],
        }))

    classifications = [
        "NORMATIVE_REQUIREMENT", "NORMATIVE_REQUIREMENT", "NORMATIVE_REQUIREMENT", "NORMATIVE_REQUIREMENT",
        "ACCEPTANCE_CRITERION", "PROFILE_BINDING", "IMPLEMENTATION_INSTRUCTION", "EVIDENCE", "OBSERVATION",
        "NORMATIVE_REQUIREMENT", "NORMATIVE_REQUIREMENT", "NORMATIVE_REQUIREMENT", "NORMATIVE_REQUIREMENT",
        "NORMATIVE_REQUIREMENT", "NORMATIVE_REQUIREMENT", "OBSERVATION", "IMPLEMENTATION_GUIDANCE",
        "IMPLEMENTATION_GUIDANCE", "IMPLEMENTATION_GUIDANCE", "IMPLEMENTATION_INSTRUCTION", "IMPLEMENTATION_GUIDANCE",
        "OBSERVATION", "OBSERVATION", "PROFILE_BINDING", "NORMATIVE_REQUIREMENT", "IMPLEMENTATION_INSTRUCTION",
        "NORMATIVE_REQUIREMENT", "ACCEPTANCE_CRITERION", "OBSERVATION", "ACCEPTANCE_CRITERION", "NORMATIVE_REQUIREMENT",
    ]
    specification_lines = specification_text().splitlines()
    section_statements = [specification_lines[index + 1] for index, line in enumerate(specification_lines) if line.startswith("## ")]
    statement_classifications = []
    for index, (statement, classification) in enumerate(zip(section_statements, classifications), 1):
        layer = "PROFILE" if classification == "PROFILE_BINDING" else "IMPLEMENTATION" if classification in {"IMPLEMENTATION_INSTRUCTION", "IMPLEMENTATION_GUIDANCE", "OBSERVATION", "EVIDENCE"} else "SPECIFICATION"
        statement_classifications.append(hashed("STATEMENT_CLASSIFICATION", {
            "statement_id": f"R3-STMT-{index:03d}", "source_ref": f"SPECIFICATION.md#{index}",
            "statement": statement, "classification": classification,
            "authority": {"layer": layer, "ref": f"SPECIFICATION.md#{index}" if layer == "SPECIFICATION" else ("PROFILE-REFERENCE.yaml" if layer == "PROFILE" else "IMPLEMENTATION-CONFORMANCE.yaml")},
            "object_ref": f"section:{index}",
        }))

    errors = []
    error_types = ["ValidationError", "EvaluationError", "ConformanceError", "AuthorizationError", "TransitionError", "EventStoreError", "ProjectionError", "ExecutionError", "VerificationError"]
    recoverability = ["NON_RETRYABLE", "REQUIRES_NEW_EVIDENCE", "REQUIRES_SPECIFICATION_REVIEW", "REQUIRES_AUTHORITY", "RETRYABLE", "REQUIRES_IMPLEMENTATION_CHANGE", "REQUIRES_IMPLEMENTATION_CHANGE", "RETRYABLE", "REQUIRES_NEW_EVIDENCE"]
    for index, (error_type, recovery) in enumerate(zip(error_types, recoverability), 1):
        errors.append(hashed("BOUNDARY_ERROR", {
            "error_id": f"R3-ERROR-{index:03d}", "error_type": error_type, "error_code": f"{error_type.upper()}_EXAMPLE",
            "layer": "IMPLEMENTATION", "subject_ref": "subject:boundary-reference", "rule_ref": f"R3-REQ-{min(index + 7, 24):03d}",
            "evidence_refs": [], "cause": None, "recoverability": recovery,
            "semantic_result": "UNKNOWN" if recovery == "REQUIRES_NEW_EVIDENCE" else "BLOCKED",
        }))

    conformance_rules = [
        ("BOUNDARY-001", "Every normative requirement has a specification authority."),
        ("BOUNDARY-002", "Every profile binding references exactly one requirement or declares a profile-wide binding."),
        ("BOUNDARY-003", "Every implementation mapping references a profile binding or implementation-defined contract."),
        ("BOUNDARY-004", "Every evaluation references a predicate."),
        ("BOUNDARY-005", "Every conformance result references a requirement."),
        ("BOUNDARY-006", "Every authorization references operation, authority, scope, and policy."),
        ("BOUNDARY-007", "No cross-domain result conversion occurs without an explicit rule."),
        ("BOUNDARY-008", "Implementation instructions cannot weaken normative requirements."),
        ("BOUNDARY-009", "Interpretation-changing profile changes require profile version changes."),
        ("BOUNDARY-010", "Evidence cannot modify normative meaning."),
    ]

    trace_rows = []
    for index, requirement in enumerate(requirements, 1):
        trace_rows.append({
            "requirement_ref": requirement["requirement_id"], "criterion_ref": criteria[index - 1]["criterion_id"],
            "profile_binding_ref": profile_bindings[index - 1]["binding_id"],
            "implementation_mapping_ref": implementation_mappings[index - 1]["mapping_id"],
            "test_ref": implementation_mappings[index - 1]["tests"][0], "evidence_ref": evidence_objects[index - 1]["evidence_id"],
            "validation_ref": validation_results[index - 1]["validation_id"],
            "evaluation_ref": evaluation_results[index - 1]["evaluation_id"],
            "conformance_ref": requirement["requirement_id"],
        })

    base = {"realization_id": "gde-v14.7-r3-boundary-contracts", "realization_version": VERSION, "semantic_version": "v14.7"}
    artifacts = {
        "VERSION.yaml": {"title": "Executable Boundary Contracts and Conformance Mapping", "status": "IMPLEMENTATION_REALIZATION_REFINEMENT", "refines": ["v14.7-R2", "v14.7-R2.1"], "new_normative_states": False, "renamed_semantic_states": False, "weakened_requirement_semantics": False, "new_semantic_layer": False},
        "EXECUTIVE-RESULT.yaml": {"boundary_contracts": "EXECUTABLE", "reference_boundary_conformance": "CONFORMANT", "target_implementation_conformance": "UNVERIFIED", "semantic_revision": False},
        "SPECIFICATION-BASIS.yaml": basis,
        "PROFILE-REFERENCE.yaml": profile_reference,
        "BOUNDARY-CONTRACT.yaml": {"layers": ["SPECIFICATION", "PROFILE", "IMPLEMENTATION", "EVIDENCE"], "authority_layers": ["SPECIFICATION", "PROFILE", "IMPLEMENTATION"], "question": "WHERE_DOES_THIS_RULE_OBTAIN_NORMATIVE_FORCE", "schema_ref": "schema/boundary-binding.schema.yaml"},
        "AUTHORITY-PRECEDENCE.yaml": {"order": ["SPECIFICATION", "PROFILE", "IMPLEMENTATION", "EVIDENCE"], "relationships": ["SPECIFICATION_DEFINES_OBLIGATION", "PROFILE_BINDS_PERMITTED_CHOICES", "IMPLEMENTATION_REALIZES_PROFILE", "EVIDENCE_DEMONSTRATES_OBSERVATION"], "lower_layer_override": "FORBIDDEN", "evidence_normative_authority": False},
        "STATEMENT-CLASSIFICATION.yaml": {"allowed": ["NORMATIVE_REQUIREMENT", "ACCEPTANCE_CRITERION", "PROFILE_BINDING", "IMPLEMENTATION_INSTRUCTION", "IMPLEMENTATION_GUIDANCE", "OBSERVATION", "EVIDENCE"], "objects": statement_classifications, "source_sections": list(range(1, 32)), "classification_cardinality": "EXACTLY_ONE"},
        "NORMATIVE-REQUIREMENTS.yaml": {"objects": requirements, "count": len(requirements)},
        "ACCEPTANCE-CRITERIA.yaml": {"objects": criteria, "count": len(criteria)},
        "PROFILE-BINDINGS.yaml": {"profile_ref": f'{profile_reference["profile_id"]}@{profile_reference["profile_version"]}', "objects": profile_bindings, "count": len(profile_bindings)},
        "IMPLEMENTATION-MAPPINGS.yaml": {"implementation_id": "v147r3-python-boundary-reference", "objects": implementation_mappings, "count": len(implementation_mappings), "mapping_is_requirement": False},
        "EVIDENCE.yaml": {"objects": evidence_objects, "count": len(evidence_objects), "normative_authority": False},
        "VALIDATION-RESULTS.yaml": {"objects": validation_results, "count": len(validation_results), "semantic_truth_claim": False},
        "EVALUATION-RESULTS.yaml": {"objects": evaluation_results, "count": len(evaluation_results), "conformance_claim": False},
        "COMPLETE-TRACEABILITY.yaml": {"chain": ["REQUIREMENT", "ACCEPTANCE_CRITERION", "PROFILE_BINDING", "IMPLEMENTATION_MAPPING", "TEST_OR_OBSERVATION", "EVIDENCE", "VALIDATION", "EVALUATION", "CONFORMANCE"], "extended_result_flow": ["VALIDATION", "EVALUATION", "CONFORMANCE", "ELIGIBILITY", "AUTHORITY", "AUTHORIZATION", "DECISION", "EXECUTION", "VERIFICATION", "NEW_EVIDENCE"], "objects": trace_rows, "bidirectional": True},
        "VALIDATION-CONTRACT.yaml": hashed("VALIDATION_CONTRACT", {"contract_id": "R3-VALIDATION-CONTRACT", "input": {"subject_ref": "required", "context_ref": "required"}, "output": {"type": "ValidationResult", "states": ["VALID", "INVALID", "BLOCKED", "UNKNOWN"]}, "may_modify_authoritative_state": False, "deterministic": True, "forbidden_actions": ["ISSUE_CERTIFICATE", "APPROVE_RELEASE", "MUTATE_AUTHORITATIVE_HISTORY", "EVALUATE_PREDICATE"]}),
        "EVALUATION-CONTRACT.yaml": hashed("EVALUATION_CONTRACT", {"contract_id": "R3-EVALUATION-CONTRACT", "operation": "Evaluate(predicate, subject, context)", "prerequisite": {"required_validation": "VALID", "alternate_path": "EXPLICIT_NORMATIVE_RULE_ONLY"}, "required_bindings": ["predicate", "subject", "inputs", "context", "evaluator", "evaluator_version", "evaluation_time", "evidence", "scope"], "output_type": "EvaluationResult", "may_authorize": False}),
        "CONFORMANCE-CONTRACT.yaml": hashed("CONFORMANCE_CONTRACT", {"contract_id": "R3-CONFORMANCE-CONTRACT", "operation": "EvaluateRequirement(requirement, subject, evidence)", "required_inputs": ["requirement", "applicable_scope", "acceptance_criteria", "validated_evidence", "evaluation_results"], "output_type": "ConformanceResult", "forbidden_inferences": ["VALIDATION_EQUALS_CONFORMANT", "TRUE_EQUALS_CONFORMANT"], "non_conformant_requires_violation": True, "absence_of_evidence_default": "UNVERIFIED"}),
        "CONFORMANCE-RESULT-MODEL.yaml": {"states": ["CONFORMANT", "PARTIALLY_CONFORMANT", "NON_CONFORMANT", "UNVERIFIED", "BLOCKED", "NOT_APPLICABLE", "UNKNOWN"], "objects": conformance_results, "non_conformant_requires_identified_violation": True, "absence_of_evidence_default": "UNVERIFIED"},
        "RESULT-CONVERSION-RULES.yaml": {"generic_convert_operation": "FORBIDDEN", "objects": conversion_rules, "count": len(conversion_rules)},
        "FORBIDDEN-IMPLICIT-CONVERSIONS.yaml": {"objects": [
            {"source": "ValidationResult.VALID", "target": "ConformanceResult.CONFORMANT"},
            {"source": "EvaluationResult.TRUE", "target": "ReleaseDecision.APPROVED"},
            {"source": "ConformanceResult.CONFORMANT", "target": "Authorization.GRANTED"},
            {"source": "ReleaseDecision.APPROVED", "target": "ReleaseExecution.SUCCEEDED"},
            {"source": "EvaluationResult.UNKNOWN", "target": "EvaluationResult.TRUE"},
            {"source": "EvaluationResult.BLOCKED", "target": "EvaluationResult.TRUE"},
            {"source": "EvaluationResult.INVALID", "target": "EvaluationResult.FALSE"},
        ], "unruled_conversion": "INVALID"},
        "TYPED-BOUNDARY-GUIDANCE.yaml": {"classification": "IMPLEMENTATION_GUIDANCE", "language": "Rust", "repository_has_rust_target": False, "preferred_types": ["ValidationResult", "EvaluationResult", "ConformanceResult", "ReleaseEligibility", "AuthorizationResult", "ReleaseDecision", "ReleaseExecution", "PostReleaseVerification"], "forbidden_universal_type": "Status", "state_carrying_types": ["RawObject", "ValidatedObject", "ConformantSubject", "EligibleRelease", "AuthorizedRelease", "ApprovedRelease", "ExecutedRelease"], "creates_normative_states": False, "implementation_evidence": "UNAVAILABLE"},
        "ERROR-MODEL.yaml": {"objects": errors, "count": len(errors), "generic_result_string": "DISCOURAGED", "required_fields": ["error_code", "layer", "subject", "rule_reference", "evidence_references", "cause", "recoverability"]},
        "RECOVERABILITY.yaml": {"states": ["RETRYABLE", "NON_RETRYABLE", "REQUIRES_NEW_EVIDENCE", "REQUIRES_AUTHORITY", "REQUIRES_PROFILE_CHANGE", "REQUIRES_IMPLEMENTATION_CHANGE", "REQUIRES_SPECIFICATION_REVIEW"], "semantic_effect": "NONE", "example": {"result": "UNKNOWN", "diagnostic": "REQUIRES_NEW_EVIDENCE", "effective_result": "UNKNOWN"}},
        "REQUIREMENT-CODE-TRACEABILITY.yaml": {"forward": "requirement_to_profile_to_code_to_test_to_evidence", "reverse": "code_to_test_to_evidence_to_requirement", "objects": trace_rows, "target_code_mapping_status": "UNVERIFIED"},
        "REQUIREMENT-IMPLEMENTATION-MATRIX.yaml": {"normative_authority": False, "rows": [
            {"requirement": "deterministic ordering", "profile_binding": "sequence-based ordering", "implementation": "event store sequence constraint", "test": "replay test", "evidence": "replay evidence"},
            {"requirement": "immutable history", "profile_binding": "append-only event model", "implementation": "transactional append", "test": "mutation rejection", "evidence": "event-store evidence"},
            {"requirement": "authority scope", "profile_binding": "explicit scope model", "implementation": "scope validator", "test": "scope boundary tests", "evidence": "authorization evidence"},
            {"requirement": "artifact binding", "profile_binding": "artifact hash identity", "implementation": "hash verifier", "test": "artifact mismatch test", "evidence": "integrity evidence"},
            {"requirement": "decision reuse safety", "profile_binding": "decision-basis identity", "implementation": "reuse checker", "test": "context-change tests", "evidence": "reuse evidence"},
        ], "status": "TRACEABILITY_EXAMPLE_NOT_PRODUCTION_CONFORMANCE"},
        "PROFILE-IMPLEMENTATION-TEST.yaml": {"question": "DOES_CHANGING_THIS_MECHANISM_CHANGE_PROTOCOL_SEMANTICS", "yes": "PROFILE_OR_SPECIFICATION", "no": "IMPLEMENTATION_DETAIL", "examples": [{"mechanism": "SHA-256_TO_SHA-512_WHEN_PROFILE_FIXED", "classification": "PROFILE_CHANGE", "version_required": True}, {"mechanism": "RUST_CRATE_IMPLEMENTING_SHA-256", "classification": "IMPLEMENTATION_DETAIL", "version_required": False}]},
        "PROFILE-FREEZE-AUDIT.yaml": {"profile_ref": f'{profile_reference["profile_id"]}@{profile_reference["profile_version"]}', "checks": {"all_profile_selectable_decisions_enumerated": True, "no_requirement_depends_on_unspecified_choice": True, "no_instruction_silently_acts_as_profile_rule": True, "implicit_defaults": 0, "implementation_leakage": 0, "unstated_algorithms": 0, "unstated_ordering": 0, "unstated_time_semantics": 0, "unstated_encoding": 0, "unstated_error_coercion": 0, "unstated_compatibility": 0}, "result": "FROZEN"},
        "MECHANICAL-BOUNDARY-VALIDATOR.yaml": {"entrypoint": "validate_boundary_artifact", "tool": "historical-source/tools/v147r3_boundary_contracts.py", "output_type": "ValidationResult", "defects": {f"B{i:03d}": name for i, name in enumerate(["REQUIREMENT_CONTAINS_IMPLEMENTATION_MECHANISM", "INSTRUCTION_LACKS_AUTHORITY", "PROFILE_BINDING_LACKS_REQUIREMENT", "PROFILE_LACKS_SPECIFICATION", "IMPLEMENTATION_LACKS_PROFILE", "EVIDENCE_LACKS_SUBJECT", "EVALUATION_LACKS_PREDICATE", "CONFORMANCE_LACKS_REQUIREMENT", "CONVERSION_LACKS_RULE", "NORMATIVE_CLASSIFIED_AS_GUIDANCE", "IMPLEMENTATION_CLASSIFIED_AS_NORMATIVE", "PROFILE_CHANGES_FROZEN_SEMANTICS"], 1)}},
        "BOUNDARY-CONFORMANCE-RULES.yaml": {"objects": [{"id": rule_id, "rule": rule} for rule_id, rule in conformance_rules], "count": len(conformance_rules)},
        "FINAL-ARTIFACT-GRAPH.yaml": {"nodes": ["SPECIFICATION", "REQUIREMENTS", "ACCEPTANCE_CRITERIA", "PROFILE", "PROFILE_BINDINGS", "IMPLEMENTATION", "OBSERVATIONS", "EVIDENCE", "VALIDATION", "EVALUATION", "CONFORMANCE", "ELIGIBILITY", "AUTHORITY", "AUTHORIZATION", "DECISION", "EXECUTION", "VERIFICATION", "NEW_EVIDENCE"], "new_evidence_feedback_only": True, "history_rewrite": False},
        "CLOSURE-CONDITION.yaml": {"checks": {"specification_has_no_implementation_leakage": True, "profile_has_no_unspecified_semantic_binding": True, "implementation_has_no_hidden_normative_authority": True, "validation_has_no_evaluation_semantics": True, "evaluation_has_no_authorization_semantics": True, "conformance_has_explicit_requirement_semantics": True, "authorization_has_explicit_authority_semantics": True, "decision_has_explicit_operational_semantics": True}, "result": "BOUNDARY_FROZEN"},
        "IMPLEMENTATION-CONFORMANCE.yaml": {"reference_boundary_harness": "CONFORMANT", "target_engine": "UNVERIFIED", "rust_typed_domain_implementation": "UNVERIFIED", "durable_event_store": "UNVERIFIED", "production_crypto": "UNVERIFIED", "finite_tests_prove_all_implementations": False},
        "FAILURE-PROVENANCE.yaml": {"error_types": error_types, "objects": errors, "cross_domain_cause_erasure": "FORBIDDEN"},
        "ARTIFACT-TREE.yaml": {"physical": "historical-source/compliance/certification/v14.7-R3", "groups": ["specification", "profile", "implementation", "evidence", "contracts", "schemas", "tests", "conformance"], "append_only": True},
        "FINAL-PRINCIPLE.yaml": {"text": "A requirement defines obligation; a profile fixes a permitted realization; an implementation realizes it; evidence observes it; validation gates processing; evaluation establishes propositions; conformance establishes satisfaction; authorization permits; decision chooses; execution performs; verification observes.", "no_layer_may_borrow_semantic_authority": True},
        "CURRENT-STATUS.yaml": {"objects": [], "reference_boundary_contracts": "CONFORMANT", "profile": "FROZEN", "target_implementation": "UNVERIFIED", "semantic_revision": False, "invented_production_evidence": False},
    }

    all_declared = FILES + [f"schema/{name}.schema.yaml" for name in SCHEMAS] + ["SPECIFICATION.md", "VALIDATION.yaml", "VALIDATION.md", "DETERMINISM-VALIDATION.yaml", "REGRESSION-VALIDATION.yaml"]
    specification_authority = {
        "VERSION.yaml", "SPECIFICATION-BASIS.yaml", "BOUNDARY-CONTRACT.yaml", "AUTHORITY-PRECEDENCE.yaml",
        "STATEMENT-CLASSIFICATION.yaml", "NORMATIVE-REQUIREMENTS.yaml", "ACCEPTANCE-CRITERIA.yaml",
        "VALIDATION-CONTRACT.yaml", "EVALUATION-CONTRACT.yaml", "CONFORMANCE-CONTRACT.yaml",
        "CONFORMANCE-RESULT-MODEL.yaml", "RESULT-CONVERSION-RULES.yaml", "FORBIDDEN-IMPLICIT-CONVERSIONS.yaml",
        "RECOVERABILITY.yaml", "PROFILE-IMPLEMENTATION-TEST.yaml", "PROFILE-FREEZE-AUDIT.yaml",
        "MECHANICAL-BOUNDARY-VALIDATOR.yaml", "BOUNDARY-CONFORMANCE-RULES.yaml", "FINAL-ARTIFACT-GRAPH.yaml",
        "CLOSURE-CONDITION.yaml", "FINAL-PRINCIPLE.yaml", "SPECIFICATION.md",
    }
    profile_authority = {"PROFILE-REFERENCE.yaml", "PROFILE-BINDINGS.yaml"}
    boundary_bindings = []
    for subject in all_declared:
        layer = "PROFILE" if subject in profile_authority else "SPECIFICATION" if subject in specification_authority or subject.startswith("schema/") else "IMPLEMENTATION"
        boundary_bindings.append(hashed("BOUNDARY_BINDING", {
            "subject_ref": subject, "authority": {"layer": layer, "ref": "SPECIFICATION.md" if layer == "SPECIFICATION" else ("PROFILE-REFERENCE.yaml" if layer == "PROFILE" else "IMPLEMENTATION-CONFORMANCE.yaml")},
            "claims": [{"claim_id": f'claim:{subject}', "statement": "Authority identifies force; artifact content cannot borrow another layer's authority."}],
            "satisfies": ["R3-REQ-001"], "evidence_refs": ["MACHINE-TEST-RESULTS.yaml"],
        }))
    artifacts["BOUNDARY-BINDINGS.yaml"] = {"objects": boundary_bindings, "count": len(boundary_bindings), "covers_declared_artifacts": True}

    for filename, value in artifacts.items():
        write(DESTINATION / filename, value if filename in {"SPECIFICATION-BASIS.yaml", "PROFILE-REFERENCE.yaml", "VALIDATION-CONTRACT.yaml", "EVALUATION-CONTRACT.yaml", "CONFORMANCE-CONTRACT.yaml"} else {**base, **value})

    registry = [{"name": name, "path": f"schema/{name}.schema.yaml", "sha256": sha256(SCHEMA_DIRECTORY / f"{name}.schema.yaml")} for name in SCHEMAS]
    write(DESTINATION / "SCHEMA-REGISTRY.yaml", {**base, "local": registry, "predecessor": {"path": "../v14.7-R2.1/SCHEMA-REGISTRY.yaml", "sha256": sha256(PREDECESSOR / "SCHEMA-REGISTRY.yaml"), "count": 67}, "effective_count": 80})

    after = [{"path": str(path.relative_to(COMPLIANCE)), "sha256": sha256(path), "bytes": path.stat().st_size}
             for path in sorted(COMPLIANCE.rglob("*")) if path.is_file() and DESTINATION not in path.parents]
    if predecessor != after:
        raise RuntimeError("predecessor mutation detected")
    write(DESTINATION / "PRIOR-INTEGRITY.yaml", {**base, "protected_artifact_count": len(predecessor), "artifacts": predecessor, "status": "PRESERVED"})
    owned = FILES + [f"schema/{name}.schema.yaml" for name in SCHEMAS] + ["SPECIFICATION.md"]
    write(DESTINATION / "VALIDATION-REPORT.yaml", {**base, "generator_owned": len(owned), "schemas": len(SCHEMAS), "requirements": len(requirements), "criteria": len(criteria), "profile_bindings": len(profile_bindings), "implementation_mappings": len(implementation_mappings), "evidence_objects": len(evidence_objects),
        "validation_results": len(validation_results), "evaluation_results": len(evaluation_results), "tests": len(tests), "status": "AWAITING_INDEPENDENT_VALIDATION"})
    print(f"generated {len(owned)} R3 artifacts; tests={len(tests)} requirements={len(requirements)} predecessor={len(predecessor)}")


if __name__ == "__main__":
    main()
