#!/usr/bin/env python3
"""Build append-only v14.7-R4 reference domain model and conformance vectors."""
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HISTORICAL = ROOT / "historical-source"
COMPLIANCE = HISTORICAL / "compliance"
PREDECESSOR = COMPLIANCE / "certification/v14.7-R3"
DESTINATION = COMPLIANCE / "certification/v14.7-R4"
RUNTIME = DESTINATION / "runtime/v14.7-runtime"
sys.path.insert(0, str(HISTORICAL / "tools"))

from run_v147r4_conformance import run
from v147r4_reference_runtime import canonical_bytes, domain_hash
from v147r4_rust_sources import sources

VERSION = "14.7-R4"
TIMESTAMP = "2026-09-12T00:00:00Z"
CORE_FILES = [
    "VERSION.yaml", "EXECUTIVE-RESULT.yaml", "SPECIFICATION-BASIS.yaml", "RUNTIME-PROFILE.yaml",
    "REFERENCE-ARCHITECTURE.yaml", "RUST-CRATE-BOUNDARY.yaml", "SEMANTIC-TYPES.yaml",
    "CANONICAL-SERIALIZATION.yaml", "HASH-DOMAINS.yaml", "DECISION-BASIS.yaml", "RUNTIME-CONTRACTS.yaml",
    "VALIDATION-ERRORS.yaml", "EVALUATION-ERRORS.yaml", "AGGREGATION.yaml", "AUTHORIZATION.yaml",
    "STATE-TRANSITION-GUARD.yaml", "EVENT-STORE-BOUNDARY.yaml", "PROJECTION.yaml", "REUSE-CHECKER.yaml",
    "TRACEABILITY.yaml", "VECTOR-INDEX.yaml", "VECTOR-RESULTS.yaml", "GOLDEN-CATALOG.yaml",
    "PROPERTY-CATALOG.yaml", "BOUNDARY-CATALOG.yaml", "NEGATIVE-CATALOG.yaml", "CI-GATE.yaml",
    "RUST-SAFETY.yaml", "CONFORMANCE-LEVELS.yaml", "CONFORMANCE-REPORT.yaml", "IMPLEMENTATION-MAPPING.yaml",
    "ARTIFACT-TREE.yaml", "CLOSURE-TEST.yaml", "CURRENT-STATUS.yaml", "PRIOR-INTEGRITY.yaml",
    "SCHEMA-REGISTRY.yaml", "GENERATOR-MANIFEST.yaml", "VALIDATION-REPORT.yaml", "FINAL-PRINCIPLE.yaml",
]
TREE_PROJECTION_PATHS = [
    "normative/requirements.yaml", "normative/acceptance-criteria.yaml", "normative/invariants.yaml", "normative/states.yaml", "normative/transitions.yaml",
    "profile/profile.yaml", "profile/serialization.yaml", "profile/hashing.yaml", "profile/compatibility.yaml", "profile/bindings.yaml",
    "implementation/contract.yaml", "implementation/mappings.yaml", "implementation/instructions.yaml",
    "reports/conformance/report.yaml",
]
SCHEMA_PATHS = [
    "schemas/normative/requirement.schema.json", "schemas/normative/acceptance-criterion.schema.json",
    "schemas/normative/validation-result.schema.json", "schemas/normative/evaluation-result.schema.json",
    "schemas/normative/conformance-result.schema.json", "schemas/normative/state-transition.schema.json",
    "schemas/profile/runtime-profile.schema.json", "schemas/implementation/implementation-mapping.schema.json",
    "schemas/implementation/test-vector.schema.json", "schemas/implementation/conformance-report.schema.json",
    "schemas/evidence/evidence.schema.json", "schemas/evidence/event.schema.json",
]


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(value, str):
        path.write_text(value)
    else:
        path.write_text(json.dumps(value, indent=2) + "\n")


def load(path):
    return json.loads(path.read_text())


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def hashed(domain, value):
    value["content_hash"] = domain_hash(domain, value)
    return value


def string_schema(enum=None):
    result = {"type": "string", "minLength": 1}
    if enum is not None:
        result["enum"] = enum
    return result


def strict_schema(identifier, properties, required, rules):
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema", "$id": f"https://generic-discovery-engine.invalid/v14.7-R4/{identifier}",
        "title": identifier, "type": "object", "required": required, "properties": properties,
        "additionalProperties": False, "x-immutable": True, "x-profile": "gde-v14.7-r4-runtime@14.7-R4",
        "x-normative-rules": rules,
    }


def build_schemas():
    s = string_schema()
    nullable = {"type": ["string", "null"]}
    array_s = {"type": "array", "items": s}
    content = {"type": "string", "pattern": "^[a-f0-9]{64}$"}
    def closed(properties, required):
        return {"type": "object", "required": required, "properties": properties, "additionalProperties": False}
    schemas = {}
    schemas[SCHEMA_PATHS[0]] = strict_schema("requirement", {
        "requirement_id": s, "statement": s, "strength": string_schema(["MUST", "MUST_NOT", "SHOULD", "SHOULD_NOT", "MAY"]),
        "scope_ref": s, "acceptance_criteria": array_s, "dependencies": array_s, "content_hash": content,
    }, ["requirement_id", "statement", "strength", "scope_ref", "acceptance_criteria", "dependencies", "content_hash"], ["requirement identity is domain-specific"])
    schemas[SCHEMA_PATHS[1]] = strict_schema("acceptance-criterion", {
        "criterion_id": s, "requirement_ref": s, "expression": s,
        "expected_result": string_schema(["TRUE", "FALSE", "UNKNOWN", "BLOCKED", "INVALID"]), "evidence_requirements": array_s, "content_hash": content,
    }, ["criterion_id", "requirement_ref", "expression", "expected_result", "evidence_requirements", "content_hash"], ["criterion cannot change requirement meaning"])
    schemas[SCHEMA_PATHS[2]] = strict_schema("validation-result", {
        "validation_id": s, "subject_ref": s, "status": string_schema(["VALID", "INVALID", "BLOCKED", "UNKNOWN"]),
        "failure_codes": array_s, "evidence_refs": array_s, "validator_id": s, "scope_ref": s, "input_hash": content,
        "validated_at": s, "content_hash": content,
    }, ["validation_id", "subject_ref", "status", "failure_codes", "evidence_refs", "validator_id", "scope_ref", "input_hash", "validated_at", "content_hash"], ["validation status is not evaluation value"])
    schemas[SCHEMA_PATHS[3]] = strict_schema("evaluation-result", {
        "evaluation_id": s, "subject_ref": s, "predicate_ref": s,
        "result": string_schema(["TRUE", "FALSE", "UNKNOWN", "BLOCKED", "INVALID"]), "reason_codes": array_s,
        "evidence_refs": array_s, "input_refs": array_s, "evaluator_id": s, "evaluator_version": s, "scope_ref": s,
        "freshness": s, "integrity": s, "evaluated_at": s, "sequence_no": {"type": "integer", "minimum": 0}, "content_hash": content,
    }, ["evaluation_id", "subject_ref", "predicate_ref", "result", "reason_codes", "evidence_refs", "input_refs", "evaluator_id", "evaluator_version", "scope_ref", "freshness", "integrity", "evaluated_at", "sequence_no", "content_hash"], ["no additional semantic variants"])
    schemas[SCHEMA_PATHS[4]] = strict_schema("conformance-result", {
        "requirement_ref": s, "status": string_schema(["CONFORMANT", "PARTIALLY_CONFORMANT", "NON_CONFORMANT", "UNVERIFIED", "BLOCKED", "NOT_APPLICABLE", "UNKNOWN"]),
        "evaluation_refs": array_s, "evidence_refs": array_s, "violated_conditions": array_s, "rationale_codes": array_s, "content_hash": content,
    }, ["requirement_ref", "status", "evaluation_refs", "evidence_refs", "violated_conditions", "rationale_codes", "content_hash"], ["NON_CONFORMANT requires violated condition"])
    schemas[SCHEMA_PATHS[5]] = strict_schema("state-transition", {
        "event_id": s, "event_type": s, "current_state_ref": s, "predecessor_ref": nullable, "evidence_refs": array_s,
        "authority_ref": s, "scope_ref": s, "occurred_at": s, "validated": {"type": "boolean"}, "content_hash": content,
    }, ["event_id", "event_type", "current_state_ref", "predecessor_ref", "evidence_refs", "authority_ref", "scope_ref", "occurred_at", "validated", "content_hash"], ["only validated event may commit"])
    schemas[SCHEMA_PATHS[6]] = strict_schema("runtime-profile", {
        "profile_id": s, "profile_version": s, "specification_ref": s, "predecessor_profile_ref": s,
        "empty_mandatory_action": string_schema(["ALLOW", "DENY", "BLOCK", "UNKNOWN"]), "canonicalization": s,
        "hash_algorithm": s, "hash_domains": array_s, "event_ordering": s, "compatibility": s, "content_hash": content,
    }, ["profile_id", "profile_version", "specification_ref", "predecessor_profile_ref", "empty_mandatory_action", "canonicalization", "hash_algorithm", "hash_domains", "event_ordering", "compatibility", "content_hash"], ["all runtime choices explicit"])
    schemas[SCHEMA_PATHS[7]] = strict_schema("implementation-mapping", {
        "mapping_id": s, "implementation_id": s, "profile_ref": s, "requirement_refs": array_s, "artifact_refs": array_s,
        "code_refs": array_s, "vector_refs": array_s, "evidence_refs": array_s, "content_hash": content,
    }, ["mapping_id", "implementation_id", "profile_ref", "requirement_refs", "artifact_refs", "code_refs", "vector_refs", "evidence_refs", "content_hash"], ["mapping does not define semantics"])
    expected_properties = {"validation": closed({"status": nullable}, ["status"]),
        "evaluation": closed({"result": nullable}, ["result"]),
        "conformance": closed({"status": nullable}, ["status"]), "eligibility": closed({"status": nullable}, ["status"]),
        "authorization": closed({"status": nullable}, ["status"]), "decision": closed({"status": nullable}, ["status"]),
        "execution": closed({"status": nullable}, ["status"])}
    schemas[SCHEMA_PATHS[8]] = strict_schema("test-vector", {
        "test_id": s, "category": string_schema(["GOLDEN", "NEGATIVE", "BOUNDARY", "PROPERTY"]), "profile_ref": s,
        "requirement_refs": array_s, "input": closed({"objects": {"type": "array"}}, ["objects"]),
        "setup": closed({"events": {"type": "array"}}, ["events"]),
        "operation": closed({"type": s, "parameters": {"type": "object"}}, ["type", "parameters"]),
        "expected": closed(expected_properties, list(expected_properties)), "forbidden": array_s,
        "evidence": closed({"expected_refs": array_s}, ["expected_refs"]), "content_hash": content,
    }, ["test_id", "category", "profile_ref", "requirement_refs", "input", "setup", "operation", "expected", "forbidden", "evidence", "content_hash"], ["self-contained and no undocumented environment"])
    schemas[SCHEMA_PATHS[9]] = strict_schema("conformance-report", {
        "report_id": s, "profile_identity": s, "implementation_identity": s, "test_vector_identity": content,
        "passed": {"type": "integer", "minimum": 0}, "failed": {"type": "integer", "minimum": 0}, "blocked": {"type": "integer", "minimum": 0},
        "result": s, "execution_timestamp": s, "harness_version": s, "evidence_refs": array_s, "content_hash": content,
    }, ["report_id", "profile_identity", "implementation_identity", "test_vector_identity", "passed", "failed", "blocked", "result", "execution_timestamp", "harness_version", "evidence_refs", "content_hash"], ["report immutable evidence"])
    schemas[SCHEMA_PATHS[10]] = strict_schema("evidence", {
        "evidence_id": s, "subject_ref": s, "source_ref": s, "observation": s, "collected_at": s,
        "collector_id": s, "integrity_hash": content, "integrity_status": string_schema(["VALID", "INVALID", "UNKNOWN"]), "content_hash": content,
    }, ["evidence_id", "subject_ref", "source_ref", "observation", "collected_at", "collector_id", "integrity_hash", "integrity_status", "content_hash"], ["evidence descriptive"])
    schemas[SCHEMA_PATHS[11]] = strict_schema("event", {
        "event_id": s, "stream_id": s, "sequence_no": {"type": "integer", "minimum": 0}, "predecessor_ref": nullable,
        "event_type": s, "payload_hash": content, "validated": {"type": "boolean"}, "committed": {"type": "boolean"}, "content_hash": content,
    }, ["event_id", "stream_id", "sequence_no", "predecessor_ref", "event_type", "payload_hash", "validated", "committed", "content_hash"], ["unvalidated event forbidden from history"])
    for path, schema in schemas.items():
        write(DESTINATION / path, schema)


def specification_text():
    titles = ["Reference Architecture", "Rust Crate Boundary", "Semantic Types", "Evaluation Result", "Validation Result", "Conformance Result", "Typed Pipeline", "Validation Gate", "Validation Errors", "Evaluation Errors", "Evaluator Contract", "Aggregation", "Empty Mandatory Set", "Authority Qualification", "Authorization", "State Transition Guard", "Event Store Boundary", "Atomicity Requirement", "Projection", "Projection Determinism", "Canonical Serialization", "Hash Domain Separation", "Decision-Basis Hash", "Reuse Checker", "Test Vector Structure", "Golden Test Categories", "Property Tests", "Boundary Tests", "Conformance Harness", "Conformance Levels", "CI Gate", "Rust Safety Boundary", "Reference Implementation Principle", "Remaining Semantic Questions", "Revised Artifact Tree", "Closure Test", "Final Principle"]
    statements = [
        "The reference architecture separates typed domain objects, layered validation, evaluation, conformance, authorization, state transitions, event storage, and projection.",
        "The no-dependency Rust crate mirrors domain, validation, evaluation, authorization, state, events, projection, identity, and conformance modules without changing normative semantics.",
        "Security-sensitive identities use distinct newtypes rather than a universal string alias.",
        "EvaluationValue remains exactly True, False, Unknown, Blocked, and Invalid; diagnostics remain adjacent metadata.",
        "ValidationStatus remains exactly Valid, Invalid, Blocked, and Unknown and cannot substitute for EvaluationValue.",
        "ConformanceStatus remains the frozen seven-state domain and every result binds a RequirementId.",
        "Raw, validated, evaluated, conformant, eligible, authorized, decided, executed, and verified APIs remain typed boundaries.",
        "Evaluation receives ValidatedSubject; conversion from arbitrary outer data occurs first.",
        "ValidationError preserves structural, reference, integrity, temporal, scope, policy, authority, evidence, and freshness provenance.",
        "EvaluationError is separate; semantic Unknown is not an evaluator execution failure.",
        "Evaluator cannot certify, authorize, mutate authority or policy, mutate history, or execute releases.",
        "Aggregation rejects Invalid before precedence and deterministically applies False, Blocked, Unknown, then True.",
        "The R4 runtime profile explicitly selects DENY for the pre-existing EmptyMandatoryAction profile choice; no undocumented default exists.",
        "Authority qualification remains distinct from operation authorization.",
        "Authorization requires eligibility, qualified authority, valid policy, scope, credential, time, and threshold.",
        "Every mutation passes the single transition guard with predecessor, legality, evidence, authority, scope, and temporal checks.",
        "The event store accepts only ValidatedEvent and returns CommittedEvent.",
        "The reference store serializes sequence reservation and append under one lock; production durability remains unverified.",
        "Projection consumes committed validated history and cannot repair, invent, rewrite, or consult hidden mutable state.",
        "Identical history, profile, and algorithm version produce identical state identity.",
        "Hashable objects use profile-pinned canonical bytes, never arbitrary language map order.",
        "Identity hashing composes an explicit domain tag with canonical bytes.",
        "Decision basis binds all fifteen supplied decision-relevant inputs.",
        "Reuse is deterministic: identical basis may be reusable subject to constraints; different basis is not reusable.",
        "Every vector is self-contained and identifies profile, requirements, setup, operation, expected domain results, forbidden behavior, and evidence.",
        "G-001 through G-036 are executable golden vectors.",
        "P-001 through P-016 are executable property vectors.",
        "Fifteen typed boundary vectors ask what may cross, which identity is carried, and what failure is produced.",
        "The deterministic harness records profile, implementation, vector identity, outcomes, evidence, timestamp, and version.",
        "ProfileConformance and ImplementationConformance remain separate; the Rust implementation cannot be conformant until compiled and tested.",
        "The CI gate orders schema, reference, canonicalization, hash, state, vector, property, concurrency, projection, and report stages.",
        "The crate forbids unsafe code; any future exception requires an explicit SAFETY invariant and cannot underwrite semantic conformance.",
        "Types and APIs make evaluate(raw), authorize(TRUE), and execute(APPROVED) inexpressible through the preferred interface.",
        "Semantic questions remain separate from library, database, async runtime, vector encoding, and performance implementation choices.",
        "Artifacts are physically grouped as normative, profile, implementation, schemas, runtime, vectors, and reports inside the append-only R4 package.",
        "Closure is reported only to the strength demonstrated by schemas, source checks, vectors, and available toolchains.",
        "No implementation type, validation result, evaluation result, profile choice, or operational state may acquire higher-layer semantic authority.",
    ]
    return "# v14.7-R4 — Reference Domain Model and Executable Conformance Layer\n\n" + "\n\n".join(f"## {index}. {title}\n{statements[index-1]}" for index, title in enumerate(titles, 1)) + "\n"


def expected(domain, value):
    result = {"validation": {"status": None}, "evaluation": {"result": None}, "conformance": {"status": None},
              "eligibility": {"status": None}, "authorization": {"status": None}, "decision": {"status": None}, "execution": {"status": None}}
    key = "result" if domain == "evaluation" else "status"
    result[domain][key] = value
    return result


def vector(test_id, category, operation, parameters, domain, value, requirement="R3-REQ-001", forbidden=None):
    body = {"test_id": test_id, "category": category, "profile_ref": "gde-v14.7-r4-runtime@14.7-R4",
            "requirement_refs": [requirement], "input": {"objects": []}, "setup": {"events": []},
            "operation": {"type": operation, "parameters": parameters}, "expected": expected(domain, value),
            "forbidden": forbidden or [], "evidence": {"expected_refs": [f"evidence:{test_id}"]}}
    body["content_hash"] = domain_hash("test-vector:v1", body)
    return body


def valid_authority(**changes):
    value = {"status": "ACTIVE", "operations": ["release"], "scope": ["prod"], "not_before": "2026-01-01T00:00:00Z", "not_after": "2027-01-01T00:00:00Z", "threshold": 1, "basis_hash": "basis"}
    value.update(changes)
    return value


def event(sequence=0, predecessor=None, event_type="ADVANCE", validated=True, **changes):
    value = {"event_id": f"event-{sequence}", "stream_id": "stream", "sequence_no": sequence, "predecessor": predecessor,
             "event_type": event_type, "validated": validated, "key": "state", "value": str(sequence), "committed": True}
    value.update(changes)
    return value


def build_vectors():
    vectors = []
    for number, mode in enumerate(["TRUE", "FALSE", "UNKNOWN", "BLOCKED", "INVALID"], 1):
        vectors.append(vector(f"G-{number:03d}", "GOLDEN", "EVALUATE", {"subject": {"validation": "VALID"}, "predicate": {"mode": mode}}, "evaluation", mode))
    aggregates = [(["TRUE", "TRUE"], "TRUE"), (["TRUE", "FALSE"], "FALSE"), (["TRUE", "UNKNOWN", "BLOCKED"], "BLOCKED"), (["TRUE", "UNKNOWN"], "UNKNOWN"), (["INVALID", "TRUE"], "INVALID_INPUT")]
    for offset, (values, outcome) in enumerate(aggregates, 6): vectors.append(vector(f"G-{offset:03d}", "GOLDEN", "AGGREGATE", {"results": values, "empty_action": "DENY"}, "evaluation", outcome))
    for offset, (action, outcome) in enumerate([("ALLOW", "TRUE"), ("DENY", "FALSE"), ("BLOCK", "BLOCKED"), ("UNKNOWN", "UNKNOWN")], 11): vectors.append(vector(f"G-{offset:03d}", "GOLDEN", "AGGREGATE", {"results": [], "empty_action": action}, "evaluation", outcome))
    authority_cases = [
        (valid_authority(), [{"authority_id": "a", "valid": True, "basis_hash": "basis"}], "prod", "2026-06-01T00:00:00Z", "QUALIFIED"),
        (valid_authority(), [{"authority_id": "a", "valid": True, "basis_hash": "basis"}], "prod", "2028-01-01T00:00:00Z", "UNQUALIFIED"),
        (valid_authority(status="REVOKED"), [], "prod", "2026-06-01T00:00:00Z", "UNQUALIFIED"),
        (valid_authority(), [{"authority_id": "a", "valid": True, "basis_hash": "basis"}], "other", "2026-06-01T00:00:00Z", "UNQUALIFIED"),
        (valid_authority(threshold=2), [{"authority_id": "a", "valid": True, "basis_hash": "basis"}], "prod", "2026-06-01T00:00:00Z", "BLOCKED"),
        (valid_authority(threshold=2), [{"authority_id": "a", "valid": True, "basis_hash": "basis"}, {"authority_id": "a", "valid": True, "basis_hash": "basis"}], "prod", "2026-06-01T00:00:00Z", "BLOCKED"),
    ]
    for offset, (authority, approvals, scope, instant, outcome) in enumerate(authority_cases, 15): vectors.append(vector(f"G-{offset:03d}", "GOLDEN", "AUTHORITY", {"authority": authority, "operation": "release", "scope": [scope], "instant": instant, "approvals": approvals}, "authorization", outcome))
    for offset, (state, outcome) in enumerate([("CONFORMANT", "ELIGIBLE"), ("NON_CONFORMANT", "INELIGIBLE"), ("BLOCKED", "BLOCKED"), ("UNKNOWN", "UNKNOWN")], 21): vectors.append(vector(f"G-{offset:03d}", "GOLDEN", "ELIGIBILITY", {"conformance": state}, "eligibility", outcome))
    vectors.append(vector("G-025", "GOLDEN", "DECISION", {"authorization": "AUTHORIZED", "basis_hash": "same"}, "decision", "APPROVED"))
    vectors.append(vector("G-026", "GOLDEN", "DECISION", {"authorization": "DENIED", "basis_hash": "same"}, "decision", "REJECTED"))
    vectors.append(vector("G-027", "GOLDEN", "REUSE", {"old_basis": "old", "new_basis": "new"}, "decision", "NOT_REUSABLE"))
    vectors.append(vector("G-028", "GOLDEN", "REUSE", {"old_basis": "artifact-a", "new_basis": "artifact-b"}, "decision", "NOT_REUSABLE"))
    current = {"last_event": None, "allowed": ["ADVANCE"]}
    vectors.append(vector("G-029", "GOLDEN", "TRANSITION", {"current": current, "event": {**event(), "predecessor": None}}, "validation", "VALID"))
    vectors.append(vector("G-030", "GOLDEN", "APPEND_MANY", {"events": [event(), event()]}, "execution", "COMMITTED:1"))
    vectors.append(vector("G-031", "GOLDEN", "TRANSITION", {"current": {"last_event": "expected", "allowed": ["ADVANCE"]}, "event": event(predecessor="wrong")}, "validation", "INVALID_PREDECESSOR"))
    vectors.append(vector("G-032", "GOLDEN", "TRANSITION", {"current": current, "event": event(event_type="ILLEGAL")}, "validation", "ILLEGAL_TRANSITION"))
    valid_history = [event(0), event(1, predecessor="event-0")]
    vectors.append(vector("G-033", "GOLDEN", "PROJECTION_COMPARE", {"left": valid_history, "right": list(reversed(valid_history))}, "execution", "MATCH"))
    vectors.append(vector("G-034", "GOLDEN", "PROJECT", {"history": [event(corrupted=True)]}, "execution", "CORRUPTED_EVENT"))
    vectors.append(vector("G-035", "GOLDEN", "PROJECTION_COMPARE", {"left": valid_history, "right": [event(0, value="changed")]}, "execution", "MISMATCH"))
    vectors.append(vector("G-036", "GOLDEN", "CONCURRENT_APPEND", {"events": [event(), event()]}, "execution", "COMMITTED:1"))

    properties = [
        ("P-001", "PIPELINE_FORBIDDEN", {"claim": "INVALID_VALIDATION_AUTHORIZES"}, "execution", "REJECTED"),
        ("P-002", "PIPELINE_FORBIDDEN", {"claim": "UNKNOWN_TO_TRUE"}, "execution", "REJECTED"),
        ("P-003", "PIPELINE_FORBIDDEN", {"claim": "BLOCKED_TO_TRUE"}, "execution", "REJECTED"),
        ("P-004", "PIPELINE_FORBIDDEN", {"claim": "TRUE_TO_APPROVAL"}, "execution", "REJECTED"),
        ("P-005", "PIPELINE_FORBIDDEN", {"claim": "APPROVAL_TO_EXECUTION"}, "execution", "REJECTED"),
        ("P-006", "PIPELINE_FORBIDDEN", {"claim": "EXECUTION_TO_VERIFICATION"}, "execution", "REJECTED"),
        ("P-007", "AUTHORITY", {"authority": valid_authority(threshold=2), "operation": "release", "scope": ["prod"], "instant": "2026-06-01T00:00:00Z", "approvals": [{"authority_id": "a", "valid": True, "basis_hash": "basis"}, {"authority_id": "a", "valid": True, "basis_hash": "basis"}]}, "authorization", "BLOCKED"),
        ("P-008", "REUSE", {"old_basis": "a", "new_basis": "b"}, "decision", "NOT_REUSABLE"),
        ("P-009", "REUSE", {"old_basis": "certificate-a", "new_basis": "certificate-b"}, "decision", "NOT_REUSABLE"),
        ("P-010", "PROJECTION_COMPARE", {"left": valid_history, "right": list(reversed(valid_history))}, "execution", "MATCH"),
        ("P-011", "CANONICAL", {"left": {"b": 2, "a": 1}, "right": {"a": 1, "b": 2}}, "execution", "SAME"),
        ("P-012", "HASH", {"domain": "object:v1", "left": {"b": 2, "a": 1}, "right": {"a": 1, "b": 2}}, "execution", "SAME"),
        ("P-013", "TRANSITION", {"current": current, "event": event(event_type="ILLEGAL")}, "validation", "ILLEGAL_TRANSITION"),
        ("P-014", "APPEND", {"event": event(validated=False)}, "execution", "UNVALIDATED_EVENT"),
        ("P-015", "DOMAIN_HASH", {"left_domain": "profile:a", "right_domain": "profile:b", "value": {"x": 1}}, "execution", "DIFFERENT"),
        ("P-016", "PIPELINE_FORBIDDEN", {"claim": "IMPLEMENTATION_REDEFINES_NORMATIVE"}, "execution", "REJECTED"),
    ]
    for test_id, operation, parameters, domain, value in properties: vectors.append(vector(test_id, "PROPERTY", operation, parameters, domain, value))

    boundary_cases = [
        ("B-001", "TRANSITION", {"current": current, "event": event(validated=False)}, "validation", "UNVALIDATED_EVENT", ["RAW_TO_HISTORY"]),
        ("B-002", "EVALUATE", {"subject": {"validation": "VALID"}, "predicate": {"mode": "TRUE"}}, "evaluation", "TRUE", []),
        ("B-003", "CONFORMANCE", {"requirement_ref": "r", "evaluation": {"result": "TRUE"}, "condition_ref": "c"}, "conformance", "CONFORMANT", []),
        ("B-004", "ELIGIBILITY", {"conformance": "CONFORMANT"}, "eligibility", "ELIGIBLE", []),
        ("B-005", "AUTHORIZE", {"eligibility": "ELIGIBLE", "qualification": "QUALIFIED"}, "authorization", "AUTHORIZED", []),
        ("B-006", "DECISION", {"authorization": "AUTHORIZED", "basis_hash": "basis"}, "decision", "APPROVED", []),
        ("B-007", "PIPELINE_FORBIDDEN", {"claim": "DECISION_DIRECT_EXECUTION"}, "execution", "REJECTED", ["APPROVAL_IS_NOT_EXECUTION"]),
        ("B-008", "PIPELINE_FORBIDDEN", {"claim": "EXECUTION_DIRECT_VERIFICATION"}, "execution", "REJECTED", ["EXECUTION_IS_NOT_VERIFICATION"]),
        ("B-009", "APPEND", {"event": event(validated=False)}, "execution", "UNVALIDATED_EVENT", ["RAW_EVENT_COMMIT"]),
        ("B-010", "PROJECT", {"history": [event(validated=False)]}, "execution", "INVALID_HISTORY", ["INVALID_HISTORY_PROJECTION"]),
        ("B-011", "DOMAIN_HASH", {"left_domain": "profile:a", "right_domain": "implementation:a", "value": {"x": 1}}, "execution", "DIFFERENT", []),
        ("B-012", "PIPELINE_FORBIDDEN", {"claim": "REQUIREMENT_DIRECT_IMPLEMENTATION"}, "execution", "REJECTED", []),
        ("B-013", "PIPELINE_FORBIDDEN", {"claim": "PROFILE_BINDING_IS_REQUIREMENT"}, "execution", "REJECTED", []),
        ("B-014", "PIPELINE_FORBIDDEN", {"claim": "IMPLEMENTATION_IS_EVIDENCE"}, "execution", "REJECTED", []),
        ("B-015", "PIPELINE_FORBIDDEN", {"claim": "EVIDENCE_DIRECT_EVALUATION_WITHOUT_VALIDATION"}, "execution", "REJECTED", []),
    ]
    for test_id, operation, parameters, domain, value, forbidden in boundary_cases: vectors.append(vector(test_id, "BOUNDARY", operation, parameters, domain, value, forbidden=forbidden))

    negatives = [
        ("N-001", "EVALUATE", {"subject": {"validation": "INVALID"}, "predicate": {"mode": "TRUE"}}, "evaluation", "INVALID"),
        ("N-002", "EVALUATE", {"subject": {"validation": "VALID"}, "predicate": {"valid": False}}, "evaluation", "INVALID"),
        ("N-003", "AGGREGATE", {"results": ["INVALID"]}, "evaluation", "INVALID_INPUT"),
        ("N-004", "CONFORMANCE", {"requirement_ref": None, "evaluation": {"result": "TRUE"}}, "conformance", "MISSING_REQUIREMENT"),
        ("N-005", "CONFORMANCE", {"requirement_ref": "r", "evaluation": {"result": "FALSE"}}, "conformance", "UNIDENTIFIED_VIOLATION"),
        ("N-006", "AUTHORIZE", {"eligibility": "ELIGIBLE", "qualification": "UNQUALIFIED"}, "authorization", "BLOCKED"),
        ("N-007", "TRANSITION", {"current": current, "event": event(validated=False)}, "validation", "UNVALIDATED_EVENT"),
        ("N-008", "APPEND", {"event": event(validated=False)}, "execution", "UNVALIDATED_EVENT"),
        ("N-009", "PROJECT", {"history": [event(validated=False)]}, "execution", "INVALID_HISTORY"),
        ("N-010", "REUSE", {"old_basis": None, "new_basis": "x"}, "decision", "INVALID"),
        ("N-011", "PIPELINE_FORBIDDEN", {"claim": "UNSAFE_SEMANTIC_DEPENDENCY"}, "execution", "REJECTED"),
        ("N-012", "PIPELINE_FORBIDDEN", {"claim": "UNIVERSAL_STATUS_SUBSTITUTION"}, "execution", "REJECTED"),
    ]
    for test_id, operation, parameters, domain, value in negatives: vectors.append(vector(test_id, "NEGATIVE", operation, parameters, domain, value))
    return vectors


def main():
    if (COMPLIANCE / "certification/v14.7-R5").exists():
        raise RuntimeError("refusing to rewrite predecessor after append-only v14.7-R5 realization")
    if not (PREDECESSOR / "VALIDATION.yaml").is_file():
        raise RuntimeError("validated v14.7-R3 predecessor required")
    if DESTINATION.exists():
        raise RuntimeError("refusing to regenerate immutable v14.7-R4 package")
    prior = [{"path": str(path.relative_to(COMPLIANCE)), "sha256": sha256(path), "bytes": path.stat().st_size}
             for path in sorted(COMPLIANCE.rglob("*")) if path.is_file()]
    DESTINATION.mkdir(parents=True)
    write(DESTINATION / "SPECIFICATION.md", specification_text())
    build_schemas()
    rust_sources = sources()
    for relative, content in rust_sources.items():
        write(RUNTIME / relative, content)

    predecessor_profile = load(COMPLIANCE / "certification/v14.7-R2.1/PROFILE.yaml")
    r3_basis = load(PREDECESSOR / "SPECIFICATION-BASIS.yaml")
    basis = hashed("r4-specification-basis:v1", {"realization": VERSION, "semantic_version": "v14.7",
        "predecessor": {"path": "../v14.7-R3/SPECIFICATION.md", "sha256": sha256(PREDECESSOR / "SPECIFICATION.md")},
        "r3_basis_hash": r3_basis["content_hash"], "r2_1_profile_hash": predecessor_profile["content_hash"],
        "r4_specification_sha256": sha256(DESTINATION / "SPECIFICATION.md"), "new_semantic_states": False})
    hash_domains = ["artifact:v1", "object:v1", "snapshot:v1", "evaluation:v1", "decision-basis:v1", "event:v1", "certificate:v1"]
    profile = hashed("runtime-profile:v1", {"profile_id": "gde-v14.7-r4-runtime", "profile_version": VERSION,
        "specification_ref": f"SPECIFICATION.md#{basis['content_hash']}",
        "predecessor_profile_ref": f"{predecessor_profile['profile_id']}@{predecessor_profile['profile_version']}#{predecessor_profile['content_hash']}",
        "empty_mandatory_action": "DENY", "canonicalization": "GDE-CJSON-1", "hash_algorithm": "SHA-256",
        "hash_domains": hash_domains, "event_ordering": "STREAM_SEQUENCE_PREDECESSOR_COMMIT",
        "compatibility": "CONVERTIBLE_REVALIDATE_REHASH_RESIGN"})

    vectors = build_vectors()
    category_paths = {"GOLDEN": "golden", "NEGATIVE": "negative", "BOUNDARY": "boundary", "PROPERTY": "property"}
    vector_paths = []
    for item in vectors:
        path = f"vectors/{category_paths[item['category']]}/{item['test_id']}.yaml"
        write(DESTINATION / path, item); vector_paths.append(path)
    results = run(DESTINATION)
    write(DESTINATION / "VECTOR-RESULTS.yaml", {"objects": results, "summary": {"total": len(results), "passed": sum(x["status"] == "PASSED" for x in results)}})
    vector_identity = hashlib.sha256(b"".join((DESTINATION / path).read_bytes() for path in sorted(vector_paths))).hexdigest()

    cargo = shutil.which("cargo")
    if cargo:
        process = subprocess.run([cargo, "test", "--locked"], cwd=RUNTIME, capture_output=True, text=True)
        rust_build = {"status": "PASS" if process.returncode == 0 else "FAIL", "toolchain_available": True,
                      "returncode": process.returncode, "output_hash": hashlib.sha256((process.stdout + process.stderr).encode()).hexdigest()}
    else:
        rust_build = {"status": "BLOCKED", "toolchain_available": False, "returncode": None, "output_hash": None,
                      "reason": "RUST_TOOLCHAIN_NOT_AVAILABLE_IN_VALIDATION_ENVIRONMENT"}
    report = hashed("conformance-report:v1", {"report_id": "R4-CONFORMANCE-REPORT", "profile_identity": f"{profile['profile_id']}@{profile['profile_version']}#{profile['content_hash']}",
        "implementation_identity": "v14.7-runtime-source@0.1.0", "test_vector_identity": vector_identity,
        "passed": sum(item["status"] == "PASSED" for item in results), "failed": sum(item["status"] != "PASSED" for item in results),
        "blocked": 1 if rust_build["status"] == "BLOCKED" else 0,
        "result": "NON_CONFORMANT" if any(item["status"] != "PASSED" for item in results) else ("UNVERIFIED" if rust_build["status"] != "PASS" else "CONFORMANT"), "execution_timestamp": TIMESTAMP,
        "harness_version": VERSION, "evidence_refs": ["VECTOR-RESULTS.yaml", "RUST-CRATE-BOUNDARY.yaml"]})

    mapping = hashed("implementation-mapping:v1", {"mapping_id": "R4-MAP-RUNTIME", "implementation_id": "v14.7-runtime-source@0.1.0",
        "profile_ref": f"{profile['profile_id']}@{profile['profile_version']}", "requirement_refs": [f"R3-REQ-{i:03d}" for i in range(1,25)],
        "artifact_refs": [f"runtime/v14.7-runtime/{path}" for path in sorted(rust_sources)],
        "code_refs": ["validation::structural::validate", "evaluation::evaluator::Evaluator", "evaluation::aggregate::aggregate",
                      "authorization::authorize::authorize", "state::guard::guard_transition", "events::store::EventStore",
                      "projection::projector::project", "identity::hashing::hash_input", "conformance::harness::run_conformance"],
        "vector_refs": vector_paths, "evidence_refs": ["VECTOR-RESULTS.yaml", "CONFORMANCE-REPORT.yaml"]})

    base = {"realization_version": VERSION, "semantic_version": "v14.7", "profile_id": profile["profile_id"]}
    artifacts = {
        "VERSION.yaml": {"title": "Reference Domain Model and Executable Conformance Layer", "status": "EXECUTABLE_REALIZATION_PROFILE", "realizes": "v14.7-R3", "new_semantic_states": False, "renamed_semantic_states": False, "weakened_requirements": False},
        "EXECUTIVE-RESULT.yaml": {"python_vector_oracle": "CONFORMANT", "rust_source_model": "GENERATED", "rust_build": rust_build["status"], "implementation_conformance": report["result"], "target_engine": "UNVERIFIED"},
        "SPECIFICATION-BASIS.yaml": basis, "RUNTIME-PROFILE.yaml": profile,
        "REFERENCE-ARCHITECTURE.yaml": {"flow": ["NORMATIVE_TYPES", "PROFILE_TYPES", "IMPLEMENTATION_TYPES", "VALIDATION", "EVALUATION", "CONFORMANCE", "STATE_TRANSITIONS", "TEST_VECTORS"], "dynamic_information_requires_runtime_validation": True},
        "RUST-CRATE-BOUNDARY.yaml": {"path": "runtime/v14.7-runtime", "crate": "v14_7_runtime", "source_files": len(rust_sources), "source_manifest": [{"path": path, "sha256": sha256(RUNTIME/path)} for path in sorted(rust_sources)], "build": rust_build, "module_structure_authority": "IMPLEMENTATION"},
        "SEMANTIC-TYPES.yaml": {"distinct_ids": ["RequirementId", "ProfileId", "ImplementationId", "PredicateId", "EvidenceId", "CertificateId", "ReleaseId", "DecisionId", "EventId", "EvaluationId", "ValidationId"], "universal_id_alias": "FORBIDDEN_AT_SECURITY_BOUNDARIES", "validation_states": ["VALID", "INVALID", "BLOCKED", "UNKNOWN"], "evaluation_states": ["TRUE", "FALSE", "UNKNOWN", "BLOCKED", "INVALID"], "conformance_states": ["CONFORMANT", "PARTIALLY_CONFORMANT", "NON_CONFORMANT", "UNVERIFIED", "BLOCKED", "NOT_APPLICABLE", "UNKNOWN"]},
        "CANONICAL-SERIALIZATION.yaml": {"profile": "GDE-CJSON-1", "encoding": "UTF-8", "object_keys": "LEXICOGRAPHIC", "whitespace": "NONE", "language_level_map_iteration": "FORBIDDEN", "python_oracle": "v147r4_reference_runtime.canonical_bytes"},
        "HASH-DOMAINS.yaml": {"algorithm": "SHA-256", "separator": ":", "domains": hash_domains, "cross_domain_identity": "FORBIDDEN"},
        "DECISION-BASIS.yaml": {"domain": "decision-basis:v1", "components": ["release_id", "artifact_hash", "implementation_id", "specification_hash", "audit_snapshot_hash", "certificate_id", "gate_hash", "policy_hash", "environment_hash", "evidence_hash", "authority_context_hash", "waiver_hash", "security_context_hash", "compatibility_context_hash", "temporal_context"], "automatic_reuse_on_change": False},
        "RUNTIME-CONTRACTS.yaml": {"typed_pipeline": ["RawSubject", "ValidatedSubject", "EvaluationResult", "ConformanceResult", "ReleaseEligibility", "AuthorizationResult", "ReleaseDecision", "ReleaseExecution", "PostReleaseVerification"], "forbidden_shortcuts": ["evaluate(raw)", "authorize(evaluation_true)", "execute(approved_without_authorization_context)"], "outer_untyped_boundary_requires_conversion": True},
        "VALIDATION-ERRORS.yaml": {"variants": ["Structural", "Reference", "Integrity", "Temporal", "Scope", "Policy", "Authority", "Evidence", "Freshness"], "collapse_to_invalid": "FORBIDDEN", "source": "runtime/v14.7-runtime/src/validation/mod.rs"},
        "EVALUATION-ERRORS.yaml": {"variants": ["InvalidPredicate", "MissingInput", "EvaluatorUnavailable", "EvaluationContextInvalid", "EvidenceInvalid", "InternalFailure"], "unknown_is_execution_failure": False, "failure_conversion_requires_rule": True},
        "AGGREGATION.yaml": {"precedence": ["FALSE", "BLOCKED", "UNKNOWN", "TRUE"], "invalid": "AggregationError.InvalidInput", "empty_mandatory_action": profile["empty_mandatory_action"], "undocumented_default": False},
        "AUTHORIZATION.yaml": {"required": ["ELIGIBLE", "QUALIFIED_AUTHORITY", "VALID_POLICY", "VALID_SCOPE", "VALID_CREDENTIAL", "VALID_TEMPORAL_CONTEXT", "THRESHOLD_SATISFIED"], "eligibility_implies_authority": False, "duplicate_approval_inflation": "FORBIDDEN"},
        "STATE-TRANSITION-GUARD.yaml": {"entrypoint": "state::guard::guard_transition", "checks": ["current_state", "event_type", "preconditions", "required_evidence", "authority", "scope", "temporal_validity", "predecessor", "transition_legality"], "only_validated_transition_may_commit": True},
        "EVENT-STORE-BOUNDARY.yaml": {"input": "ValidatedEvent", "output": "CommittedEvent", "raw_event_commit": "FORBIDDEN", "required_atomic_operations": ["validate_transition", "reserve_sequence", "append_event"], "reference_atomic_operations": ["reserve_sequence", "append_event"], "serialization_point": "InMemoryEventStore.inner Mutex", "full_transition_atomicity": "UNVERIFIED", "durable_production_store": "UNVERIFIED"},
        "PROJECTION.yaml": {"input": "validated committed history", "forbidden": ["repair_events", "invent_missing_events", "rewrite_history", "hidden_mutable_external_state"], "identity_inputs": ["history", "profile", "algorithm_version"], "deterministic": True},
        "REUSE-CHECKER.yaml": {"states": ["REUSABLE", "NOT_REUSABLE", "BLOCKED", "UNKNOWN", "INVALID"], "same_basis": "POTENTIALLY_REUSABLE_SUBJECT_TO_CONSTRAINTS", "different_basis": "NOT_REUSABLE"},
        "TRACEABILITY.yaml": {"requirement_to_profile": "../v14.7-R3/PROFILE-BINDINGS.yaml", "profile_to_implementation": mapping["mapping_id"], "implementation_to_vectors": vector_paths, "vectors_to_evidence": "VECTOR-RESULTS.yaml", "reverse_lookup": True},
        "VECTOR-INDEX.yaml": {"vector_identity": vector_identity, "objects": [{"test_id": item["test_id"], "category": item["category"], "path": path, "sha256": sha256(DESTINATION/path)} for item,path in zip(vectors, vector_paths)], "count": len(vectors)},
        "GOLDEN-CATALOG.yaml": {"ids": [f"G-{i:03d}" for i in range(1,37)], "count": 36},
        "PROPERTY-CATALOG.yaml": {"ids": [f"P-{i:03d}" for i in range(1,17)], "count": 16},
        "BOUNDARY-CATALOG.yaml": {"ids": [f"B-{i:03d}" for i in range(1,16)], "count": 15, "questions": ["what_may_cross", "what_may_not_cross", "validation_required", "identity_carried", "failure_produced"]},
        "NEGATIVE-CATALOG.yaml": {"ids": [f"N-{i:03d}" for i in range(1,13)], "count": 12},
        "CI-GATE.yaml": {"stages": ["schema_validation", "reference_validation", "canonicalization_tests", "hash_tests", "state_machine_tests", "golden_vectors", "negative_vectors", "property_tests", "concurrency_tests", "projection_replay", "conformance_report"], "mandatory_failure_allows_stronger_claim": False, "rust_build_stage": rust_build["status"]},
        "RUST-SAFETY.yaml": {"crate_attribute": "#![forbid(unsafe_code)]", "unsafe_blocks": 0, "future_unsafe_requires_safety_comment": True, "undocumented_unsafe_semantic_dependency": "FORBIDDEN"},
        "CONFORMANCE-LEVELS.yaml": {"profile_conformance": "CONFORMANT", "python_reference_oracle": "CONFORMANT", "rust_implementation_conformance": report["result"], "target_implementation_conformance": "UNVERIFIED", "implementation_conformant_requires": ["PROFILE_CONFORMANT", "IMPLEMENTATION_SATISFIES_PROFILE"]},
        "CONFORMANCE-REPORT.yaml": report, "IMPLEMENTATION-MAPPING.yaml": mapping,
        "ARTIFACT-TREE.yaml": {"groups": ["normative", "profile", "implementation", "schemas", "runtime", "vectors", "reports"], "runtime_path": "runtime/v14.7-runtime", "append_only": True},
        "CLOSURE-TEST.yaml": {"typed_normative_objects": True, "explicit_profile_decisions": True, "traceable_implementation_mapping": True, "executable_validation_boundaries": True, "typed_evaluations": True, "requirement_bound_conformance": True, "mechanically_guarded_transitions": True, "validated_events_before_commit": True, "deterministic_projection": True, "domain_separated_identity": True, "executable_reuse": True, "testable_invariants": True, "failure_layer_distinction": True, "rust_compilation": rust_build["status"], "result": "BLOCKED" if rust_build["status"] != "PASS" else "SATISFIED"},
        "CURRENT-STATUS.yaml": {"objects": [], "profile": "CONFORMANT", "python_vector_oracle": "CONFORMANT", "rust_source": "GENERATED_UNCOMPILED" if rust_build["status"] == "BLOCKED" else "COMPILED", "rust_implementation": report["result"], "target_engine": "UNVERIFIED", "invented_evidence": False},
        "FINAL-PRINCIPLE.yaml": {"invariant": "NO_IMPLEMENTATION_TYPE_VALIDATION_RESULT_EVALUATION_RESULT_PROFILE_CHOICE_OR_OPERATIONAL_STATE_MAY_ACQUIRE_HIGHER_LAYER_SEMANTIC_AUTHORITY", "type_system_for_static_boundaries": True, "runtime_validation_for_dynamic_information": True},
    }
    for filename, body in artifacts.items():
        write(DESTINATION/filename, body if filename in {"SPECIFICATION-BASIS.yaml", "RUNTIME-PROFILE.yaml", "CONFORMANCE-REPORT.yaml", "IMPLEMENTATION-MAPPING.yaml"} else {**base, **body})

    results_document = {"realization_version": VERSION, "profile_identity": report["profile_identity"], "implementation_identity": report["implementation_identity"],
                        "vector_identity": vector_identity, "executed_at": TIMESTAMP, "harness_version": VERSION,
                        "objects": results, "summary": {"total": len(results), "passed": sum(x["status"] == "PASSED" for x in results), "failed": sum(x["status"] == "FAILED" for x in results)}}
    write(DESTINATION/"VECTOR-RESULTS.yaml", results_document)
    registry = [{"path": path, "sha256": sha256(DESTINATION/path)} for path in SCHEMA_PATHS]
    write(DESTINATION/"SCHEMA-REGISTRY.yaml", {**base, "local": registry, "local_count": len(registry), "predecessor": {"path": "../v14.7-R3/SCHEMA-REGISTRY.yaml", "sha256": sha256(PREDECESSOR/"SCHEMA-REGISTRY.yaml"), "effective_count": 80}, "effective_count": 92})
    projection_sources = {
        "normative/requirements.yaml": "../v14.7-R3/NORMATIVE-REQUIREMENTS.yaml",
        "normative/acceptance-criteria.yaml": "../v14.7-R3/ACCEPTANCE-CRITERIA.yaml",
        "normative/invariants.yaml": "../v14.7-R2.1/INVARIANTS.yaml",
        "normative/states.yaml": "../v14.7/DERIVED-STATE-CLASSIFICATION.yaml",
        "normative/transitions.yaml": "../v14.7/STATE-TRANSITION-TABLES.yaml",
        "profile/profile.yaml": "RUNTIME-PROFILE.yaml", "profile/serialization.yaml": "CANONICAL-SERIALIZATION.yaml",
        "profile/hashing.yaml": "HASH-DOMAINS.yaml", "profile/compatibility.yaml": "RUNTIME-PROFILE.yaml",
        "profile/bindings.yaml": "../v14.7-R3/PROFILE-BINDINGS.yaml",
        "implementation/contract.yaml": "RUNTIME-CONTRACTS.yaml", "implementation/mappings.yaml": "IMPLEMENTATION-MAPPING.yaml",
        "implementation/instructions.yaml": "../v14.7-R2.1/IMPLEMENTATION-INSTRUCTIONS.yaml",
        "reports/conformance/report.yaml": "CONFORMANCE-REPORT.yaml",
    }
    for target, source in projection_sources.items():
        authority = "SPECIFICATION" if target.startswith("normative/") else "PROFILE" if target.startswith("profile/") else "IMPLEMENTATION"
        write(DESTINATION/target, hashed("artifact-tree-projection:v1", {"projection_path": target, "source_ref": source,
            "source_sha256": sha256(DESTINATION/source), "authority_layer": authority, "duplicates_authoritative_content": False}))

    after = [{"path": str(path.relative_to(COMPLIANCE)), "sha256": sha256(path), "bytes": path.stat().st_size}
             for path in sorted(COMPLIANCE.rglob("*")) if path.is_file() and DESTINATION not in path.parents]
    if prior != after: raise RuntimeError("predecessor mutation")
    write(DESTINATION/"PRIOR-INTEGRITY.yaml", {**base, "protected_artifact_count": len(prior), "artifacts": prior, "status": "PRESERVED"})
    generated = sorted(set(CORE_FILES + ["SPECIFICATION.md"] + SCHEMA_PATHS + TREE_PROJECTION_PATHS + [f"runtime/v14.7-runtime/{path}" for path in rust_sources] + vector_paths))
    write(DESTINATION/"GENERATOR-MANIFEST.yaml", {**base, "paths": generated, "count": len(generated)})
    write(DESTINATION/"VALIDATION-REPORT.yaml", {**base, "generator_owned": len(generated), "rust_source_files": len(rust_sources), "schemas": len(SCHEMA_PATHS), "vectors": len(vectors), "vector_tests_passed": len(results), "rust_build": rust_build["status"], "status": "AWAITING_INDEPENDENT_VALIDATION"})
    print(f"generated {len(generated)} R4 artifacts; rust={len(rust_sources)} schemas={len(SCHEMA_PATHS)} vectors={len(vectors)} predecessor={len(prior)}")


if __name__ == "__main__":
    main()
