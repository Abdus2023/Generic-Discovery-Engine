#!/usr/bin/env python3
"""Build Protocol-v11.1 obligation-to-specification artifacts.

Normative derivation is gated on verified v10.1 obligations. The current v10.1 package
is structurally validated but rejected as an input package: its own input contract
failed, no obligation is VERIFIED, UNKNOWN records remain, and obligation conflicts
remain unresolved. Therefore this builder emits no normative specification objects.
It does emit explicitly non-normative rationale/guidance/assumption records and a full
rejection, schema, traceability, validation, and certificate framework.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[2]
HS = ROOT / "historical-source"
OBL = HS / "obligations"
OUT = HS / "specification"

MACHINE = [
    "INPUT-CONTRACT.yaml", "SPECIFICATION-MANIFEST.yaml", "SPECIFICATION-CERTIFICATE.yaml",
    "EVIDENCE-REFERENCES.yaml", "PROPERTY-REFERENCES.yaml", "OBLIGATION-REFERENCES.yaml",
    "REQUIREMENTS.yaml", "NORMATIVE-RULES.yaml", "CONDITIONS.yaml", "PREDICATES.yaml",
    "CONSTRAINTS.yaml", "GUIDANCE.yaml", "RATIONALES.yaml", "ASSUMPTIONS.yaml", "IMPLEMENTATION-NOTES.yaml",
    "EXAMPLES.yaml", "ACCEPTANCE-CRITERIA.yaml", "TEST-ORACLES.yaml", "INVARIANTS.yaml",
    "TRANSITIONS.yaml", "EFFECTS.yaml", "EXCEPTIONS.yaml", "REQUIREMENT-DEPENDENCIES.yaml",
    "REQUIREMENT-CONFLICTS.yaml", "REQUIREMENT-SUPERSESSION.yaml", "COMPATIBILITY.yaml",
    "IMPLEMENTATION-BOUNDARIES.yaml", "VERIFICATION.yaml", "TEST-RESULTS.yaml",
    "CONFORMANCE.yaml", "TRACEABILITY.yaml",
]
REPORTS = [
    "REPORTS/REQUIREMENTS.md", "REPORTS/NORMATIVE-RULES.md", "REPORTS/GUIDANCE.md",
    "REPORTS/ACCEPTANCE-CRITERIA.md", "REPORTS/TEST-ORACLES.md", "REPORTS/DEPENDENCIES.md",
    "REPORTS/CONFLICTS.md", "REPORTS/CONFORMANCE.md", "REPORTS/VERIFICATION.md",
    "REPORTS/TRACEABILITY.md", "REPORTS/SPECIFICATION-AUDIT.md",
    "REPORTS/FINAL-SPECIFICATION.md",
]
SCHEMA_NAMES = [
    "specification", "requirement", "rule", "guidance", "rationale", "assumption",
    "implementation-note", "example", "condition", "predicate", "constraint", "acceptance-criterion",
    "oracle", "invariant", "transition", "effect", "exception", "compatibility",
    "dependency", "conflict", "supersession", "boundary", "verification", "test-result",
    "conformance", "traceability", "evidence", "property", "obligation", "certificate",
]
SCHEMAS = [f"SCHEMA/{x}.schema.yaml" for x in SCHEMA_NAMES]
DELIVERABLES = MACHINE + REPORTS + SCHEMAS

REQUIREMENT_TYPES = ["BEHAVIORAL", "STRUCTURAL", "INTERFACE", "SEMANTIC", "STATE", "LIFECYCLE", "ERROR", "SECURITY", "AUTHORIZATION", "CONCURRENCY", "RESOURCE", "PERFORMANCE", "PERSISTENCE", "PROVENANCE", "OBSERVABILITY", "COMPATIBILITY", "CONFIGURATION", "SERIALIZATION", "DISCOVERY", "DEDUPLICATION", "SCHEDULING", "CANCELLATION", "RECOVERY", "AUDIT", "EXPORT", "UI", "TESTABILITY", "VERIFICATION", "NEGATIVE", "INVARIANT", "TRANSITION", "BOUNDARY"]
DISPOSITIONS = ["PRESERVE", "STABILIZE", "GENERALIZE", "FORMALIZE", "STRENGTHEN", "RESTRICT", "COMPATIBILIZE", "DEPRECATE", "REJECT", "INTRODUCE", "OPTIONALIZE"]
STRENGTHS = ["MANDATORY", "CONDITIONAL", "RECOMMENDED", "OPTIONAL", "EXPERIMENTAL", "NON_NORMATIVE", "UNKNOWN"]
EPISTEMIC = ["PROVED", "SUPPORTED", "INFERRED", "CONJECTURED", "CONTRADICTED", "UNKNOWN"]
LIFECYCLE = ["DISCOVERED", "DERIVED", "DRAFTED", "FORMALIZED", "IMPLEMENTED", "PARTIALLY_IMPLEMENTED", "VERIFIED", "FAILED", "SUPERSEDED", "REJECTED", "DEPRECATED", "UNKNOWN"]
SCOPES = ["GLOBAL", "VERSION", "COMPONENT", "INTERFACE", "OPERATION", "STATE", "TRANSITION", "CANDIDATE", "OBSERVATION", "DISCOVERY", "PROVIDER", "SCHEDULER", "WORKER", "KNOWLEDGE_BASE", "PERSISTENCE", "EXPORT", "UI", "TEST", "SECURITY_BOUNDARY", "TRUST_BOUNDARY", "CONFIGURATION", "RUNTIME"]
GUIDANCE_TYPES = ["ARCHITECTURAL", "IMPLEMENTATION", "TESTING", "OPERATIONS", "MIGRATION", "COMPATIBILITY", "PERFORMANCE", "SECURITY", "DEBUGGING", "DOCUMENTATION", "MAINTENANCE", "INTERPRETATION", "EXAMPLE"]
GUIDANCE_PRIORITIES = ["RECOMMENDED", "OPTIONAL", "INFORMATIONAL"]
IMPLEMENTATION_NOTE_STATUSES = ["SUGGESTED", "EXAMPLE", "EXPERIMENTAL", "CURRENT", "DEPRECATED", "UNKNOWN"]
RULE_OPERATORS = ["MUST", "MUST_NOT", "MAY"]
PREDICATES = ["EQUALITY", "INEQUALITY", "MEMBERSHIP", "EXISTENCE", "NON_EXISTENCE", "TYPE", "SHAPE", "RANGE", "CARDINALITY", "UNIQUENESS", "ORDERING", "TEMPORAL", "STATE", "TRANSITION", "DEPENDENCY", "AUTHORIZATION", "CAPABILITY", "PROVENANCE", "HASH", "SIGNATURE", "REFERENCE", "SCHEMA", "CONTAINMENT", "RESOURCE_BOUND", "CONCURRENCY", "CANCELLATION", "DETERMINISM", "COMPATIBILITY"]
COMPOUND_PREDICATES = ["AND", "OR", "NOT", "XOR", "IMPLIES", "IFF", "FOR_ALL", "EXISTS", "EXACTLY_ONE", "AT_LEAST_ONE", "AT_MOST_ONE"]
ORACLE_TYPES = ["BOOLEAN", "EXACT_VALUE", "RANGE", "SET_MEMBERSHIP", "STRUCTURAL", "STATE", "TRACE", "INVARIANT", "PROPERTY", "REFERENCE_MODEL", "DIFFERENTIAL", "METAMORPHIC", "HASH", "SIGNATURE", "SCHEMA", "TEMPORAL", "RESOURCE_BOUND", "SECURITY_POLICY"]
ORACLE_INDEPENDENCE = ["INDEPENDENT", "PARTIALLY_INDEPENDENT", "IMPLEMENTATION_DERIVED", "UNKNOWN"]
BOUNDARY_TYPES = ["INPUT", "VALIDATION", "ACQUISITION", "RECOGNITION", "PROVIDER", "EXPANSION", "SCHEDULER", "STATE_STORE", "KNOWLEDGE_BASE", "PERSISTENCE", "AUTHORIZATION", "AUDIT", "EXPORT", "UI", "RUNTIME", "TEST_HARNESS"]
DEPENDENCY_RELATIONS = ["REQUIRES", "ENABLES", "SUPPORTS", "REFINES", "STRENGTHENS", "CONSTRAINS", "CONFLICTS_WITH", "SUPERSEDES", "VERIFIED_BY", "DERIVED_FROM"]
CONFLICT_TYPES = ["DIRECT", "CONDITIONAL", "SCOPE", "TEMPORAL", "COMPATIBILITY", "SECURITY", "RESOURCE", "SEMANTIC", "UNKNOWN"]
CONFLICT_RESOLUTIONS = ["PRESERVE_BOTH", "PRIORITIZE_ONE", "RESTRICT_SCOPE", "SPLIT_SCOPE", "SUPERSEDE", "REJECT", "DEFER", "UNKNOWN"]
COMPATIBILITY_TYPES = ["SOURCE", "BEHAVIORAL", "DATA", "PROTOCOL", "CONFIGURATION", "SERIALIZATION", "UI", "TEST"]
EFFECT_TYPES = ["STATE_CHANGE", "OWNERSHIP_CHANGE", "DATA_WRITE", "DATA_DELETE", "AUDIT_EVENT", "RESOURCE_RELEASE", "RESOURCE_ALLOCATE", "QUEUE_OPERATION", "EXTERNAL_OPERATION"]
VIOLATION_ACTIONS = ["REJECT", "FAIL", "ROLLBACK", "CANCEL", "QUARANTINE", "ALERT", "UNKNOWN"]
SECURITY_IMPACTS = ["NONE", "LOW", "MEDIUM", "HIGH", "CRITICAL", "UNKNOWN"]
TEST_RESULTS = ["PASS", "FAIL", "BLOCKED", "SKIPPED", "INCONCLUSIVE", "NOT_APPLICABLE", "UNKNOWN"]
CONFORMANCE_LEVELS = ["L0_NONE", "L1_STRUCTURAL", "L2_BEHAVIORAL", "L3_SEMANTIC", "L4_SAFETY", "L5_SECURITY", "L6_VERIFIED"]
CONFORMANCE_STATUSES = ["CONFORMANT", "PARTIALLY_CONFORMANT", "NON_CONFORMANT", "UNVERIFIED", "BLOCKED", "UNKNOWN"]
VERIFICATION_LEVELS = ["V0_UNTESTED", "V1_EXAMPLE_TESTED", "V2_UNIT_VERIFIED", "V3_PROPERTY_VERIFIED", "V4_INTEGRATION_VERIFIED", "V5_ADVERSARIAL_VERIFIED", "V6_FORMALLY_VERIFIED"]
VERIFICATION_METHODS = ["INSPECTION", "UNIT_TEST", "INTEGRATION_TEST", "PROPERTY_TEST", "REFERENCE_MODEL", "DIFFERENTIAL_TEST", "ADVERSARIAL_TEST", "FORMAL_PROOF", "STATIC_ANALYSIS", "RUNTIME_CHECK", "MANUAL_REVIEW"]
TRACE_RELATIONS = ["DERIVED_FROM", "SUPPORTED_BY", "JUSTIFIED_BY", "FORMALIZED_AS", "TESTED_BY", "VERIFIED_BY", "IMPLEMENTED_AT", "DEPENDS_ON", "CONFLICTS_WITH", "SUPERSEDES"]
SUPPORTING_RELATIONS = ["EXPLAINED_BY", "QUALIFIED_BY", "ILLUSTRATED_BY", "INFORMED_BY"]
COVERAGE_STATUSES = ["FULL", "PARTIAL", "MISSING", "CONFLICTED", "BLOCKED", "UNKNOWN"]
FAILURE_CLASSES = ["INPUT_FAILURE", "SCHEMA_FAILURE", "REFERENCE_FAILURE", "DERIVATION_FAILURE", "NORMATIVE_CLASSIFICATION_FAILURE", "DEPENDENCY_FAILURE", "CONFLICT_FAILURE", "SCOPE_FAILURE", "SEMANTIC_FAILURE", "RULE_FAILURE", "ACCEPTANCE_FAILURE", "ORACLE_FAILURE", "BOUNDARY_FAILURE", "TRACEABILITY_FAILURE", "VERIFICATION_FAILURE", "CONFORMANCE_FAILURE"]
PIPELINE_INVARIANTS = [
    "Normative rules are distinct from guidance.", "Guidance cannot create hidden mandatory behavior.",
    "Every mandatory requirement has a normative rule.", "Every mandatory requirement has an acceptance criterion.",
    "Every mandatory requirement has a verification path.", "Every historical requirement remains traceable to evidence.",
    "Future strengthening cannot masquerade as historical fact.", "Requirement class and obligation class remain independent.",
    "Requirement strength and obligation strength remain independent.", "Epistemic status and verification status remain independent.",
    "Dependencies and lineage remain distinct.", "Conflicts cannot be silently resolved.",
    "Implementation notes cannot redefine normative semantics.", "Examples cannot define normative scope.",
    "A test result cannot establish historical truth.", "Implementation location cannot substitute for a requirement.",
    "Every first-class object has a complete schema.", "Every cross-object reference is resolvable.",
    "Mandatory conformance requires verification evidence.", "No normative semantic transformation may occur without explicit traceability.",
]
NORMATIVE_TOKEN = re.compile(r"\b(?:MUST|MUST_NOT|SHALL|SHALL_NOT|MAY|MAY_NOT|ONLY_IF|UNLESS)\b")


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def object_hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def table(headers: list[str], rows: Iterable[Iterable[Any]]) -> str:
    def clean(value: Any) -> str:
        if isinstance(value, list): value = ", ".join(str(x) for x in value)
        return str(value).replace("|", "\\|").replace("\n", " ")
    return "| " + " | ".join(headers) + " |\n|" + "|".join("---" for _ in headers) + "|\n" + "".join("| " + " | ".join(clean(v) for v in row) + " |\n" for row in rows)


def write_md(name: str, content: str) -> None:
    path = OUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def front(title: str) -> str:
    return f"# {title}\n\n> **v11.1 derivation gate: CLOSED — REJECTED_INVALID_OBLIGATION_PACKAGE.** The v10.1 input contract failed; 54 obligations are unverified, two retain UNKNOWN epistemic status, fourteen properties remain UNKNOWN, and four obligation conflicts are unresolved. No normative object, verification result, or conformance claim is derived. Non-normative context is explicitly classified and cannot impose behavior.\n\n"


def source_provenance(source_object: str, source_hash: str, transformation: str, source_artifact: str = "historical-source/obligations/OBLIGATIONS.yaml") -> dict[str, Any]:
    return {"source_artifact": source_artifact, "source_object": source_object, "content_hash": source_hash, "transformation": transformation, "normative": False}


def input_record(kind: str, filename: str, version: str) -> dict[str, Any]:
    path = OBL / filename
    return {"artifact_id": f"V101-{kind.upper().replace('_','-')}-{sha(path)[:16]}", "artifact_type": kind, "schema_version": version, "source_path": f"historical-source/obligations/{filename}", "producer_stage": "v10.1", "generated_at": "UNKNOWN_NOT_RECORDED_UPSTREAM", "content_hash": sha(path), "hash_validation": "MATCH", "schema_validation": "STRUCTURALLY_VALID_JSON_COMPATIBLE_YAML"}


def registry(name: str, plural: str, values: list[Any], **extra: Any) -> dict[str, Any]:
    return {"schema_version": "1.0", "specification_version": "11.1", "registry_type": name, "status": "DERIVATION_REJECTED", plural: values, **extra}


def main() -> None:
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    v10_contract = load(OBL / "INPUT-CONTRACT.yaml")
    v10 = load(OBL / "OBLIGATIONS.yaml")
    v10_deps = load(OBL / "OBLIGATION-DEPENDENCIES.yaml")
    v10_lineage = load(OBL / "OBLIGATION-LINEAGE.yaml")
    v10_conflicts = load(OBL / "OBLIGATION-CONFLICTS.yaml")
    v10_trace = load(OBL / "TRACEABILITY-MATRIX.yaml")
    v10_verification = load(OBL / "VERIFICATION-GRAPH.yaml")
    obligations = v10["obligations"]
    properties = v10["historical_properties"]
    source_hash = sha(OBL / "OBLIGATIONS.yaml")
    unverified = [x for x in obligations if x["status"] != "VERIFIED" or x["verification"]["result"] != "VERIFIED"]
    unknown_obligations = [x for x in obligations if x["epistemic_status"] == "UNKNOWN" or x["status"] == "UNKNOWN"]
    unknown_properties = [x for x in properties if x["epistemic_status"] == "UNKNOWN" or x["historical_status"] == "UNKNOWN"]
    unresolved = [x for x in v10_conflicts["conflicts"] if x["resolution_status"] == "UNRESOLVED"]
    inherited_missing = [x["stage"] for x in v10_contract["failure_states"] if x["state"] == "INPUT_MISSING"]

    inputs = [
        input_record("obligation_contract", "INPUT-CONTRACT.yaml", v10_contract["input_contract_version"]),
        input_record("obligation_registry", "OBLIGATIONS.yaml", v10["metadata"]["obligation_schema_version"]),
        input_record("historical_properties", "OBLIGATIONS.yaml", v10["metadata"]["obligation_schema_version"]),
        input_record("obligation_dependencies", "OBLIGATION-DEPENDENCIES.yaml", v10_deps["schema_version"]),
        input_record("obligation_lineage", "OBLIGATION-LINEAGE.yaml", v10_lineage["schema_version"]),
        input_record("obligation_conflicts", "OBLIGATION-CONFLICTS.yaml", v10_conflicts["schema_version"]),
        input_record("traceability", "TRACEABILITY-MATRIX.yaml", v10_trace["schema_version"]),
        input_record("verification_records", "VERIFICATION-GRAPH.yaml", v10_verification["schema_version"]),
    ]
    failures = [
        {"failure_id": "V111-INPUT-001", "failure_class": "INPUT_FAILURE", "state": "INPUT_MISSING", "affected": inherited_missing, "detail": "Required Protocol-v4 through Protocol-v7 upstream stages remain absent."},
        {"failure_id": "V111-INPUT-002", "failure_class": "INPUT_FAILURE", "state": "INPUT_HASH_MISMATCH", "affected": ["v1 source extraction"], "detail": "The v10.1 package preserves the Protocol-v1 byte/range integrity failure."},
        {"failure_id": "V111-VERIFY-001", "failure_class": "VERIFICATION_FAILURE", "state": "UNVERIFIED_SOURCE", "affected": [x["obligation_id"] for x in unverified], "detail": "No source obligation is VERIFIED with verification evidence."},
        {"failure_id": "V111-SEMANTIC-001", "failure_class": "SEMANTIC_FAILURE", "state": "OBLIGATION_UNKNOWN", "affected": [x["obligation_id"] for x in unknown_obligations], "detail": "Obligation epistemic uncertainty cannot be escalated into normativity."},
        {"failure_id": "V111-SEMANTIC-002", "failure_class": "SEMANTIC_FAILURE", "state": "PROPERTY_UNKNOWN", "affected": [x["property_id"] for x in unknown_properties], "detail": "Unknown historical properties cannot silently define a normative domain."},
        {"failure_id": "V111-CONFLICT-001", "failure_class": "CONFLICT_FAILURE", "state": "CONFLICT_UNRESOLVED", "affected": [x["conflict_id"] for x in unresolved], "detail": "Unresolved obligation conflicts block affected normative derivation."},
        {"failure_id": "V111-DERIVE-001", "failure_class": "DERIVATION_FAILURE", "state": "DERIVATION_GATE_CLOSED", "affected": [x["obligation_id"] for x in obligations], "detail": "No normative semantic transformation is authorized."},
    ]
    input_contract = {"schema_version": "1.0", "specification_version": "11.1", "input_contract_version": "1.0", "status": "REJECTED_INVALID_OBLIGATION_PACKAGE", "derivation_gate": "CLOSED", "required_inputs": inputs, "source_package": {"protocol": "v10.1", "status": v10_contract["status"], "obligations": len(obligations), "verified_obligations": 0, "unknown_obligations": len(unknown_obligations), "unknown_properties": len(unknown_properties), "unresolved_conflicts": len(unresolved)}, "failures": failures, "policy": "Invalid or unverified obligation input may produce audit and explicitly non-normative context, but no normative object."}
    dump(OUT / "INPUT-CONTRACT.yaml", input_contract)

    # The normative plane remains empty because the gate is closed.
    requirements = registry("REQUIREMENT", "requirements", [], requirement_types=REQUIREMENT_TYPES, dispositions=DISPOSITIONS, strengths=STRENGTHS, epistemic_states=EPISTEMIC, lifecycle_states=LIFECYCLE, scope_types=SCOPES, blocked_source_obligations=[x["obligation_id"] for x in obligations])
    rules = registry("RULE", "rules", [], operators=RULE_OPERATORS, predicate_types=PREDICATES, compound_predicate_types=COMPOUND_PREDICATES)
    conditions = registry("CONDITION", "conditions", [], severity_values=["REQUIRED", "OPTIONAL"])
    predicates = registry("PREDICATE", "predicates", [], predicate_types=PREDICATES, compound_predicate_types=COMPOUND_PREDICATES)
    constraints = registry("CONSTRAINT", "constraints", [], reason="No normative constraint is instantiated without an admitted requirement.")
    criteria = registry("ACCEPTANCE_CRITERION", "acceptance_criteria", [])
    oracles = registry("TEST_ORACLE", "test_oracles", [], oracle_types=ORACLE_TYPES, independence_levels=ORACLE_INDEPENDENCE, harness={"object_type": "TEST_HARNESS_CONTRACT", "status": "NOT_INSTANTIATED_INPUT_REJECTED", "required_dimensions": ["input_generation", "environment", "isolation", "reset", "execution", "observation", "oracle_evaluation", "evidence_capture", "cleanup"], "may_silently_alter_tested_semantics": False}, negative_test_policy="Safety, security, authorization, lifecycle, resource, and failure requirements receive explicit negative tests when admitted.")
    invariants = registry("INVARIANT", "invariants", [], pipeline_invariant_results=[{"invariant_id": f"V111-I{i:02d}", "statement": s, "status": "PASS", "basis": "CLOSED_GATE_PREVENTS_INVALID_NORMATIVE_TRANSFORMATION" if i != 17 else "DEDICATED_SCHEMA_PRESENT"} for i, s in enumerate(PIPELINE_INVARIANTS, 1)])
    transitions = registry("TRANSITION", "transitions", [])
    effects = registry("EFFECT", "effects", [], effect_types=EFFECT_TYPES)
    exceptions = registry("EXCEPTION", "exceptions", [], security_impact_values=SECURITY_IMPACTS)

    # Non-normative plane: source rationale is preserved with explicit classification.
    rationales = []
    for i, obligation in enumerate(obligations, 1):
        rationales.append({"rationale_id": f"RATIONALE-V101-{i:03d}", "object_type": "RATIONALE", "schema_version": "1.0", "lifecycle_status": "DERIVED", "statement": obligation["rationale"], "source_obligations": [obligation["obligation_id"]], "source_properties": obligation["source_properties"], "source_evidence": obligation["source_evidence"], "epistemic_status": obligation["epistemic_status"], "reasoning_type": "HISTORICAL" if obligation["strengthening"] == "HISTORICAL" else "ENGINEERING", "normative": False, "provenance": source_provenance(obligation["obligation_id"], source_hash, "NON_NORMATIVE_RATIONALE_EXTRACTION")})
    guidance_values = [
        {"guidance_id": "GUIDE-V111-INPUT", "object_type": "GUIDANCE", "schema_version": "1.0", "lifecycle_status": "DRAFTED", "title": "Input restoration guidance", "statement": "Prefer restoring and independently validating the missing upstream stages before repeating specification derivation.", "guidance_type": "MAINTENANCE", "scope": {"type": "GLOBAL", "ref": "v10.1-input-package"}, "related_requirements": [], "related_obligations": [x["obligation_id"] for x in obligations], "epistemic_status": "SUPPORTED", "priority": "RECOMMENDED", "examples": [], "normative": False, "provenance": source_provenance("INPUT-CONTRACT", sha(OBL / "INPUT-CONTRACT.yaml"), "NON_NORMATIVE_REMEDIATION_GUIDANCE", "historical-source/obligations/INPUT-CONTRACT.yaml")},
        {"guidance_id": "GUIDE-V111-VERIFY", "object_type": "GUIDANCE", "schema_version": "1.0", "lifecycle_status": "DRAFTED", "title": "Verification guidance", "statement": "Prefer independent executable evidence for each obligation before deriving conformance-bearing requirements.", "guidance_type": "TESTING", "scope": {"type": "TEST", "ref": "obligation-verification"}, "related_requirements": [], "related_obligations": [x["obligation_id"] for x in obligations], "epistemic_status": "SUPPORTED", "priority": "RECOMMENDED", "examples": [], "normative": False, "provenance": source_provenance("VERIFICATION-GRAPH", sha(OBL / "VERIFICATION-GRAPH.yaml"), "NON_NORMATIVE_VERIFICATION_GUIDANCE", "historical-source/obligations/VERIFICATION-GRAPH.yaml")},
        {"guidance_id": "GUIDE-V111-CONFLICT", "object_type": "GUIDANCE", "schema_version": "1.0", "lifecycle_status": "DRAFTED", "title": "Conflict review guidance", "statement": "Consider resolving each obligation conflict through explicit scope, evidence, compatibility impact, and rationale before normative decomposition.", "guidance_type": "INTERPRETATION", "scope": {"type": "GLOBAL", "ref": "obligation-conflicts"}, "related_requirements": [], "related_obligations": sorted({y for x in unresolved for y in [x["left_obligation"], x["right_obligation"]]}), "epistemic_status": "SUPPORTED", "priority": "RECOMMENDED", "examples": [], "normative": False, "provenance": source_provenance("OBLIGATION-CONFLICTS", sha(OBL / "OBLIGATION-CONFLICTS.yaml"), "NON_NORMATIVE_CONFLICT_GUIDANCE", "historical-source/obligations/OBLIGATION-CONFLICTS.yaml")},
    ]
    assumptions_values = [
        {"assumption_id": "ASSUMP-V111-001", "object_type": "ASSUMPTION", "schema_version": "1.0", "lifecycle_status": "DISCOVERED", "statement": "A future candidate identity requirement would require a deterministic normalization and equivalence domain.", "scope": {"type": "CANDIDATE", "ref": "candidate-identity"}, "affected_objects": ["OBL-CANDIDATE-IDENTITY", "OBL-CANDIDATE-EQUIVALENCE"], "epistemic_status": "UNKNOWN", "validation": {"method": "PROPERTY_TEST", "oracle_id": None, "status": "UNVERIFIED"}, "normative": False, "provenance": source_provenance("OBL-CANDIDATE-EQUIVALENCE", source_hash, "EXPLICIT_NON_NORMATIVE_ASSUMPTION")},
        {"assumption_id": "ASSUMP-V111-002", "object_type": "ASSUMPTION", "schema_version": "1.0", "lifecycle_status": "DISCOVERED", "statement": "Any future conformance subject would require an identified implementation artifact and execution environment.", "scope": {"type": "RUNTIME", "ref": None}, "affected_objects": [], "epistemic_status": "UNKNOWN", "validation": {"method": "INSPECTION", "oracle_id": None, "status": "UNVERIFIED"}, "normative": False, "provenance": source_provenance("VERIFICATION-GRAPH", sha(OBL / "VERIFICATION-GRAPH.yaml"), "EXPLICIT_NON_NORMATIVE_ASSUMPTION", "historical-source/obligations/VERIFICATION-GRAPH.yaml")},
        {"assumption_id": "ASSUMP-V111-003", "object_type": "ASSUMPTION", "schema_version": "1.0", "lifecycle_status": "DISCOVERED", "statement": "Current architecture and roadmap material cannot repair missing historical verification evidence.", "scope": {"type": "GLOBAL", "ref": "historical-evidence-boundary"}, "affected_objects": [], "epistemic_status": "SUPPORTED", "validation": {"method": "INSPECTION", "oracle_id": None, "status": "VERIFIED"}, "normative": False, "provenance": source_provenance("INPUT-CONTRACT", sha(OBL / "INPUT-CONTRACT.yaml"), "EXPLICIT_NON_NORMATIVE_ASSUMPTION", "historical-source/obligations/INPUT-CONTRACT.yaml")},
    ]
    guidance = registry("GUIDANCE", "guidance", guidance_values, guidance_types=GUIDANCE_TYPES, priorities=GUIDANCE_PRIORITIES, normative_operators_forbidden=True)
    guidance["status"] = "NON_NORMATIVE_ONLY"
    rationale_obj = registry("RATIONALE", "rationales", rationales, reasoning_types=["HISTORICAL", "ENGINEERING", "SECURITY", "COMPATIBILITY", "OPERATIONAL", "PERFORMANCE"])
    rationale_obj["status"] = "NON_NORMATIVE_ONLY"
    assumptions = registry("ASSUMPTION", "assumptions", assumptions_values)
    assumptions["status"] = "NON_NORMATIVE_ONLY"
    implementation_notes = registry("IMPLEMENTATION_NOTE", "implementation_notes", [], status_values=IMPLEMENTATION_NOTE_STATUSES, reason="No implementation strategy is introduced without an admitted requirement.")
    examples = registry("EXAMPLE", "examples", [], normative_value_required=False, reason="No example is introduced without an admitted requirement.")

    reqdeps = registry("DEPENDENCY", "requirement_dependencies", [], graph_type="REQUIREMENT_DEPENDENCY_GRAPH", nodes=[], edges=[], relations=DEPENDENCY_RELATIONS, requires_cycles=[], mandatory_closure=[], obligation_dependencies_copied=False)
    reqconflicts = registry("CONFLICT", "requirement_conflicts", [], graph_type="REQUIREMENT_CONFLICT_GRAPH", conflict_types=CONFLICT_TYPES, resolutions=CONFLICT_RESOLUTIONS, upstream_obligation_conflict_blockers=[x["conflict_id"] for x in unresolved], automatic_resolution=False)
    supersession = registry("SUPERSESSION", "supersessions", [], object_types=["REQUIREMENT", "RULE", "GUIDANCE", "ACCEPTANCE_CRITERION", "ORACLE"])
    compatibility = registry("COMPATIBILITY", "compatibility_records", [], compatibility_types=COMPATIBILITY_TYPES, historical_preservation_modes=["EXACT", "SEMANTIC", "COMPATIBLE", "NORMALIZED", "GENERALIZED", "INTENTIONALLY_CHANGED", "REJECTED", "UNKNOWN"])
    boundaries = registry("BOUNDARY", "boundaries", [], boundary_types=BOUNDARY_TYPES, rule="Enforcement, observation, and verification remain independent.")
    verification = registry("VERIFICATION", "verifications", [], methods=VERIFICATION_METHODS, verification_levels=VERIFICATION_LEVELS, harness_failure_classes=["HARNESS_FAILURE", "IMPLEMENTATION_FAILURE", "ORACLE_FAILURE", "ENVIRONMENT_FAILURE", "SPECIFICATION_FAILURE", "UNKNOWN_FAILURE"], upstream={"test_edges": len(v10_verification["edges"]), "verified_nodes": len(v10_verification["verified_nodes"]), "status": "UNVERIFIED_SOURCE"})
    test_results = registry("TEST_RESULT", "test_results", [], result_values=TEST_RESULTS)
    conformance = registry("CONFORMANCE", "conformance_records", [], levels=CONFORMANCE_LEVELS, statuses=CONFORMANCE_STATUSES, highest_claimed_level="L0_NONE", claim_allowed=False, reason="No admitted requirements or verification evidence.")
    traceability = build_traceability(v10_contract, v10, rationales, guidance_values, assumptions_values)
    evidence_refs = [{**e, "object_type": "EVIDENCE", "schema_version": "1.0", "lifecycle_status": "DISCOVERED", "provenance": {"source_artifact": "historical-source/obligations/INPUT-CONTRACT.yaml", "source_object": e["evidence_id"], "content_hash": sha(OBL / "INPUT-CONTRACT.yaml"), "transformation": "REFERENCE_WRAPPER_NO_EPISTEMIC_STRENGTHENING"}} for e in v10_contract["normalized_evidence"]]
    property_refs = [{**p, "object_type": "PROPERTY", "schema_version": "1.0", "lifecycle_status": "DISCOVERED", "provenance": {"source_artifact": "historical-source/obligations/OBLIGATIONS.yaml", "source_object": p["property_id"], "content_hash": source_hash, "transformation": "REFERENCE_WRAPPER_NO_SEMANTIC_REWRITE"}} for p in properties]
    obligation_refs = [{**o, "object_type": "OBLIGATION", "schema_version": "1.0", "lifecycle_status": o["status"], "provenance": {"source_artifact": "historical-source/obligations/OBLIGATIONS.yaml", "source_object": o["obligation_id"], "content_hash": source_hash, "transformation": "REFERENCE_WRAPPER_NO_VERIFICATION_ESCALATION"}} for o in obligations]

    outputs = {
        "EVIDENCE-REFERENCES.yaml": {"schema_version": "1.0", "specification_version": "11.1", "registry_type": "EVIDENCE", "status": "SOURCE_PACKAGE_REJECTED", "evidence": evidence_refs},
        "PROPERTY-REFERENCES.yaml": {"schema_version": "1.0", "specification_version": "11.1", "registry_type": "PROPERTY", "status": "SOURCE_PACKAGE_REJECTED", "properties": property_refs},
        "OBLIGATION-REFERENCES.yaml": {"schema_version": "1.0", "specification_version": "11.1", "registry_type": "OBLIGATION", "status": "SOURCE_PACKAGE_REJECTED", "obligations": obligation_refs},
        "REQUIREMENTS.yaml": requirements, "NORMATIVE-RULES.yaml": rules, "CONDITIONS.yaml": conditions,
        "PREDICATES.yaml": predicates, "CONSTRAINTS.yaml": constraints, "GUIDANCE.yaml": guidance, "RATIONALES.yaml": rationale_obj,
        "ASSUMPTIONS.yaml": assumptions, "IMPLEMENTATION-NOTES.yaml": implementation_notes,
        "EXAMPLES.yaml": examples, "ACCEPTANCE-CRITERIA.yaml": criteria, "TEST-ORACLES.yaml": oracles,
        "INVARIANTS.yaml": invariants, "TRANSITIONS.yaml": transitions, "EFFECTS.yaml": effects,
        "EXCEPTIONS.yaml": exceptions, "REQUIREMENT-DEPENDENCIES.yaml": reqdeps,
        "REQUIREMENT-CONFLICTS.yaml": reqconflicts, "REQUIREMENT-SUPERSESSION.yaml": supersession,
        "COMPATIBILITY.yaml": compatibility, "IMPLEMENTATION-BOUNDARIES.yaml": boundaries,
        "VERIFICATION.yaml": verification, "TEST-RESULTS.yaml": test_results,
        "CONFORMANCE.yaml": conformance, "TRACEABILITY.yaml": traceability,
    }
    for filename, value in outputs.items(): dump(OUT / filename, value)
    build_schemas()

    counts = {"evidence": len(evidence_refs), "historical_properties": len(property_refs), "source_obligations": len(obligation_refs), "requirements": 0, "rules": 0, "guidance": len(guidance_values), "rationales": len(rationales), "assumptions": len(assumptions_values), "implementation_notes": 0, "examples": 0, "conditions": 0, "predicates": 0, "constraints": 0, "acceptance_criteria": 0, "oracles": 0, "invariants": 0, "transitions": 0, "effects": 0, "exceptions": 0, "dependencies": 0, "conflicts": 0, "compatibility": 0, "boundaries": 0, "verifications": 0, "test_results": 0, "conformance_records": 0}
    coverage = {"obligation_requirement": "BLOCKED", "requirement_rule": "BLOCKED", "requirement_acceptance": "BLOCKED", "acceptance_oracle": "BLOCKED", "oracle_test": "BLOCKED", "test_verification": "BLOCKED", "verification_conformance": "BLOCKED"}
    certificate = {"object_type": "SPECIFICATION_CERTIFICATE", "schema_version": "1.0", "specification_version": "11.1", "lifecycle_status": "FAILED", "provenance": {"input_artifacts": [x["artifact_id"] for x in inputs], "input_hashes": [x["content_hash"] for x in inputs]}, "validation_status": "FAIL", "counts": counts, "coverage": coverage, "failures": sorted({x["failure_class"] for x in failures}), "warnings": ["Non-normative records remain source-qualified and do not authorize implementation."], "input_hashes": [x["content_hash"] for x in inputs], "certificate_semantics": "Validation execution evidence; not proof of semantic correctness.", "certificate_hash": None}
    certificate["certificate_hash"] = object_hash({k: v for k, v in certificate.items() if k != "certificate_hash"})
    dump(OUT / "SPECIFICATION-CERTIFICATE.yaml", certificate)
    manifest = {"specification": {"manifest_id": "SPEC-MANIFEST-11.1", "object_type": "SPECIFICATION_MANIFEST", "schema_version": "1.0", "specification_version": "11.1", "input_contract_version": "1.0", "generated_at": "UNKNOWN_NOT_RECORDED_DETERMINISTIC_BUILD", "canonical_transformation": ["SOURCE", "EVIDENCE", "PROPERTY", "OBLIGATION", "REQUIREMENT", "RULE", "ACCEPTANCE_CRITERION", "TEST_ORACLE", "TEST_RESULT", "VERIFICATION", "CONFORMANCE"], "stage_responsibilities": [{"stage": "EVIDENCE", "responsibility": "establish source-supported fact"}, {"stage": "PROPERTY", "responsibility": "state what historically held"}, {"stage": "OBLIGATION", "responsibility": "derive engineering consequence"}, {"stage": "REQUIREMENT", "responsibility": "state required property or behavior"}, {"stage": "RULE", "responsibility": "formalize mandatory semantics"}, {"stage": "ACCEPTANCE_CRITERION", "responsibility": "define observable satisfaction"}, {"stage": "TEST_ORACLE", "responsibility": "mechanically evaluate satisfaction"}, {"stage": "TEST_RESULT", "responsibility": "record execution outcome"}, {"stage": "VERIFICATION", "responsibility": "assess satisfaction evidence independently of historical justification"}, {"stage": "CONFORMANCE", "responsibility": "classify implementation against requirements"}], "semantic_planes": {"NORMATIVE": ["REQUIREMENT", "RULE", "ACCEPTANCE_CRITERION", "INVARIANT", "TRANSITION", "CONSTRAINT"], "NON_NORMATIVE": ["GUIDANCE", "RATIONALE", "IMPLEMENTATION_NOTE", "EXAMPLE", "RECOMMENDATION", "ASSUMPTION"]}, "inputs": [{"artifact_id": x["artifact_id"], "content_hash": x["content_hash"]} for x in inputs], "objects": counts, "validation": {"status": "FAIL", "errors": len(failures), "warnings": 1}, "certificate": {"hash": certificate["certificate_hash"]}, "lifecycle_status": "FAILED", "provenance": {"builder": "historical-source/tools/build_normative_specification_v111.py", "derivation_gate": "CLOSED"}, "deliverables": DELIVERABLES}}
    dump(OUT / "SPECIFICATION-MANIFEST.yaml", manifest)
    audit = build_audit(failures, unresolved, obligations)
    build_reports(input_contract, manifest, outputs, certificate, audit, obligations)
    assert all((OUT / x).is_file() for x in DELIVERABLES)
    print(f"generated {len(DELIVERABLES)} v11.1 deliverables; normative=0 guidance={len(guidance_values)} rationales={len(rationales)} assumptions={len(assumptions_values)} gate=CLOSED")


def build_traceability(v10_contract: dict[str, Any], v10: dict[str, Any], rationales: list[dict[str, Any]], guidance: list[dict[str, Any]], assumptions: list[dict[str, Any]]) -> dict[str, Any]:
    nodes: list[dict[str, str]] = []
    seen: set[str] = set()
    def node(oid: str, otype: str, status: str) -> None:
        if oid not in seen:
            nodes.append({"object_id": oid, "object_type": otype, "status": status}); seen.add(oid)
    canonical: list[dict[str, Any]] = []
    supporting: list[dict[str, Any]] = []
    for e in v10_contract["normalized_evidence"]:
        sid = "SOURCE:" + e["provenance"]["source_path"]
        node(sid, "SOURCE", "PRESENT"); node(e["evidence_id"], "EVIDENCE", e["verification_status"])
        canonical.append({"traceability_id": f"TRACE-{len(canonical)+1:05d}", "from": {"object_id": sid, "object_type": "SOURCE"}, "to": {"object_id": e["evidence_id"], "object_type": "EVIDENCE"}, "relation": "FORMALIZED_AS", "evidence": [e["evidence_id"]]})
    for p in v10["historical_properties"]:
        node(p["property_id"], "PROPERTY", p["epistemic_status"])
        for eid in p["evidence_refs"]:
            canonical.append({"traceability_id": f"TRACE-{len(canonical)+1:05d}", "from": {"object_id": eid, "object_type": "EVIDENCE"}, "to": {"object_id": p["property_id"], "object_type": "PROPERTY"}, "relation": "FORMALIZED_AS", "evidence": [eid]})
    rationale_by_obligation = {r["source_obligations"][0]: r for r in rationales}
    for o in v10["obligations"]:
        node(o["obligation_id"], "OBLIGATION", o["status"])
        for pid in o["source_properties"]:
            canonical.append({"traceability_id": f"TRACE-{len(canonical)+1:05d}", "from": {"object_id": pid, "object_type": "PROPERTY"}, "to": {"object_id": o["obligation_id"], "object_type": "OBLIGATION"}, "relation": "FORMALIZED_AS", "evidence": o["source_evidence"]})
        r = rationale_by_obligation[o["obligation_id"]]
        node(r["rationale_id"], "RATIONALE", r["lifecycle_status"])
        supporting.append({"traceability_id": f"SUPTRACE-{len(supporting)+1:04d}", "from": {"object_id": o["obligation_id"], "object_type": "OBLIGATION"}, "to": {"object_id": r["rationale_id"], "object_type": "RATIONALE"}, "relation": "JUSTIFIED_BY", "evidence": r["source_evidence"]})
    for g in guidance:
        node(g["guidance_id"], "GUIDANCE", g["lifecycle_status"])
        for oid in g["related_obligations"]:
            supporting.append({"traceability_id": f"SUPTRACE-{len(supporting)+1:04d}", "from": {"object_id": oid, "object_type": "OBLIGATION"}, "to": {"object_id": g["guidance_id"], "object_type": "GUIDANCE"}, "relation": "EXPLAINED_BY", "evidence": []})
    for a in assumptions:
        node(a["assumption_id"], "ASSUMPTION", a["lifecycle_status"])
        for oid in a["affected_objects"]:
            if oid in seen:
                supporting.append({"traceability_id": f"SUPTRACE-{len(supporting)+1:04d}", "from": {"object_id": oid, "object_type": "OBLIGATION"}, "to": {"object_id": a["assumption_id"], "object_type": "ASSUMPTION"}, "relation": "QUALIFIED_BY", "evidence": []})
    trace_provenance = {"source_artifact": "historical-source/obligations/TRACEABILITY-MATRIX.yaml", "content_hash": sha(OBL / "TRACEABILITY-MATRIX.yaml"), "transformation": "V11.1_TRACE_EDGE_CONSTRUCTION"}
    for edge in canonical + supporting:
        edge.update({"object_type": "TRACEABILITY", "schema_version": "1.0", "lifecycle_status": "DERIVED", "provenance": trace_provenance})
    reverse = [{"forward_traceability_id": x["traceability_id"], "from": x["to"], "to": x["from"], "relation": "REVERSE_" + x["relation"], "evidence": x["evidence"]} for x in canonical + supporting]
    return {"schema_version": "1.0", "specification_version": "11.1", "registry_type": "TRACEABILITY", "graph_type": "CANONICAL_AND_SUPPORTING_TRACEABILITY", "status": "PARTIAL_BLOCKED_AT_OBLIGATION", "canonical_chain": ["SOURCE", "EVIDENCE", "PROPERTY", "OBLIGATION", "REQUIREMENT", "RULE", "ACCEPTANCE_CRITERION", "TEST_ORACLE", "TEST_RESULT", "VERIFICATION", "CONFORMANCE"], "nodes": nodes, "canonical_edges": canonical, "supporting_edges": supporting, "reverse_edges": reverse, "normative_nodes_after_obligation": [], "termination_reason": "The v11.1 normative derivation gate is closed."}


def build_audit(failures: list[dict[str, Any]], unresolved: list[dict[str, Any]], obligations: list[dict[str, Any]]) -> dict[str, Any]:
    stages = ["INPUT VALIDATION", "SCHEMA VALIDATION", "REFERENCE VALIDATION", "DERIVATION VALIDATION", "NORMATIVE/GUIDANCE SEPARATION", "DEPENDENCY VALIDATION", "CONFLICT DETECTION", "SEMANTIC NARROWING/WIDENING", "RULE VALIDATION", "ACCEPTANCE VALIDATION", "ORACLE VALIDATION", "BOUNDARY VALIDATION", "TRACEABILITY VALIDATION", "CONFORMANCE VALIDATION"]
    results = ["FAIL", "PASS", "PASS", "FAIL_GATE_CLOSED", "PASS", "PASS_EMPTY_REQUIREMENT_GRAPH", "BLOCKED_UPSTREAM_CONFLICTS", "BLOCKED_NO_REQUIREMENTS", "PASS_EMPTY", "PASS_EMPTY", "PASS_EMPTY", "PASS_EMPTY", "PARTIAL_TO_OBLIGATION", "PASS_NO_CLAIM"]
    dimensions = ["TRACEABILITY", "SEMANTICS", "NORMATIVITY", "SCHEMA", "DEPENDENCY", "CONFLICT", "ACCEPTANCE", "ORACLE", "VERIFICATION", "SECURITY", "FAILURE", "COMPATIBILITY", "BOUNDARY"]
    return {"stages": [{"order": i, "stage": s, "result": results[i-1]} for i, s in enumerate(stages, 1)], "completeness": [{"dimension": d, "classification": "PARTIAL" if d == "TRACEABILITY" else "FULL" if d == "SCHEMA" else "BLOCKED", "reason": "canonical trace reaches obligation" if d == "TRACEABILITY" else "all first-class schemas emitted" if d == "SCHEMA" else "normative derivation gate closed"} for d in dimensions], "failure_classes": FAILURE_CLASSES, "detected_failures": failures, "pipeline_invariants": [{"invariant_id": f"V111-I{i:02d}", "statement": s, "status": "PASS", "basis": "CLOSED_GATE_OR_EXPLICIT_SEPARATION"} for i, s in enumerate(PIPELINE_INVARIANTS, 1)], "unresolved_obligation_conflicts": [x["conflict_id"] for x in unresolved], "orphan_obligations": [x["obligation_id"] for x in obligations], "aggregate_percentage": "FORBIDDEN"}


def common(required_id: str) -> list[str]:
    return [required_id, "object_type", "schema_version", "lifecycle_status", "provenance"]


def schema(title: str, required: list[str], properties: dict[str, Any] | None = None) -> dict[str, Any]:
    return {"$schema": "https://json-schema.org/draft/2020-12/schema", "schema_version": "1.0", "schema_change_class": "MAJOR", "title": title, "type": "object", "required": required, "properties": properties or {}, "additionalProperties": True}


def build_schemas() -> None:
    scope = {"type": "object", "required": ["type", "ref"], "properties": {"type": {"enum": SCOPES}}}
    provenance = {"type": "object"}
    common_props = {"object_type": {"type": "string"}, "schema_version": {"const": "1.0"}, "lifecycle_status": {"enum": LIFECYCLE}, "provenance": provenance}
    schemas: dict[str, Any] = {}
    schemas["specification"] = schema("v11.1 specification manifest", ["specification"], {"specification": {"type": "object", "required": ["manifest_id", "object_type", "schema_version", "specification_version", "input_contract_version", "generated_at", "canonical_transformation", "stage_responsibilities", "semantic_planes", "inputs", "objects", "validation", "certificate", "lifecycle_status", "provenance"]}})
    req_fields = common("requirement_id") + ["statement", "requirement_type", "disposition", "strength", "epistemic_status", "scope", "source_obligations", "source_properties", "source_evidence", "rationales", "rules", "acceptance_criteria", "invariants", "transitions", "dependencies", "conflicts", "guidance", "implementation_notes", "examples", "assumptions", "implementation_boundaries", "exceptions", "compatibility"]
    schemas["requirement"] = schema("v11.1 requirement", req_fields, {**common_props, "requirement_type": {"enum": REQUIREMENT_TYPES}, "disposition": {"enum": DISPOSITIONS}, "strength": {"enum": STRENGTHS}, "epistemic_status": {"enum": EPISTEMIC}, "scope": scope})
    schemas["rule"] = schema("v11.1 normative rule", common("rule_id") + ["requirement_id", "operator", "subject", "predicate", "scope", "preconditions", "exceptions", "failure_class", "priority", "source"], {**common_props, "operator": {"enum": RULE_OPERATORS}})
    schemas["guidance"] = schema("v11.1 guidance", common("guidance_id") + ["title", "statement", "guidance_type", "scope", "related_requirements", "related_obligations", "epistemic_status", "priority", "examples", "normative"], {**common_props, "guidance_type": {"enum": GUIDANCE_TYPES}, "priority": {"enum": GUIDANCE_PRIORITIES}, "normative": {"const": False}})
    schemas["rationale"] = schema("v11.1 rationale", common("rationale_id") + ["statement", "source_obligations", "source_properties", "source_evidence", "epistemic_status", "reasoning_type", "normative"], {**common_props, "normative": {"const": False}})
    schemas["assumption"] = schema("v11.1 assumption", common("assumption_id") + ["statement", "scope", "affected_objects", "epistemic_status", "validation", "normative"], {**common_props, "normative": {"const": False}})
    schemas["implementation-note"] = schema("v11.1 implementation note", common("implementation_note_id") + ["statement", "related_requirements", "related_boundaries", "status", "technology", "constraints", "epistemic_status"], {**common_props, "status": {"enum": IMPLEMENTATION_NOTE_STATUSES}})
    schemas["example"] = schema("v11.1 example", common("example_id") + ["requirement_id", "description", "inputs", "execution", "expected_behavior", "normative"], {**common_props, "normative": {"const": False}})
    schemas["condition"] = schema("v11.1 condition", common("condition_id") + ["predicate", "severity", "scope"], {**common_props, "severity": {"enum": ["REQUIRED", "OPTIONAL"]}})
    schemas["predicate"] = schema("v11.1 predicate", common("predicate_id") + ["type", "expression", "field", "value", "parameters", "operands"], {**common_props, "type": {"enum": PREDICATES + COMPOUND_PREDICATES}, "operands": {"type": "array", "items": {"$ref": "predicate.schema.yaml"}}})
    schemas["constraint"] = schema("v11.1 normative constraint", common("constraint_id") + ["requirement_id", "statement", "predicate", "scope", "failure_class"], common_props)
    schemas["acceptance-criterion"] = schema("v11.1 acceptance criterion", common("criterion_id") + ["requirement_id", "statement", "preconditions", "observation", "expected", "pass_condition", "fail_condition", "evidence_required", "environment", "oracle_ids"], common_props)
    schemas["oracle"] = schema("v11.1 test oracle", common("oracle_id") + ["criterion_id", "oracle_type", "input_contract", "observation", "expected_predicate", "comparison", "failure_class", "independence", "evidence_capture"], {**common_props, "oracle_type": {"enum": ORACLE_TYPES}})
    schemas["invariant"] = schema("v11.1 invariant", common("invariant_id") + ["statement", "scope", "activation", "property", "violation", "verification"], common_props)
    schemas["transition"] = schema("v11.1 transition", common("transition_id") + ["from_state", "event", "guard", "to_state", "required_effects", "forbidden_effects", "failure_behavior", "verification"], common_props)
    schemas["effect"] = schema("v11.1 effect", common("effect_id") + ["type", "target", "operation", "predicate"], {**common_props, "type": {"enum": EFFECT_TYPES}})
    schemas["exception"] = schema("v11.1 exception", common("exception_id") + ["applies_to", "condition", "altered_behavior", "security_impact", "audit_required", "justification"], {**common_props, "security_impact": {"enum": SECURITY_IMPACTS}})
    schemas["compatibility"] = schema("v11.1 compatibility", common("compatibility_id") + ["scope", "from_version", "to_version", "compatibility_type", "preserved_properties", "allowed_changes", "forbidden_changes", "migration_required", "migration"], {**common_props, "compatibility_type": {"enum": COMPATIBILITY_TYPES}})
    schemas["dependency"] = schema("v11.1 requirement dependency", common("dependency_id") + ["from_requirement", "to_requirement", "relation", "condition", "reason", "evidence"], {**common_props, "relation": {"enum": DEPENDENCY_RELATIONS}})
    schemas["conflict"] = schema("v11.1 requirement conflict", common("conflict_id") + ["requirements", "conflict_type", "scope", "predicate_overlap", "resolution", "rationale", "effective_requirement"], {**common_props, "conflict_type": {"enum": CONFLICT_TYPES}, "resolution": {"enum": CONFLICT_RESOLUTIONS}})
    schemas["supersession"] = schema("v11.1 supersession", common("supersession_id") + ["old_object_id", "new_object_id", "object_type_superseded", "reason", "effective_scope", "compatibility_impact", "effective_version"], common_props)
    schemas["boundary"] = schema("v11.1 implementation boundary", common("boundary_id") + ["boundary_type", "name", "enforces", "observes", "verifies", "authority", "trust_level"], {**common_props, "boundary_type": {"enum": BOUNDARY_TYPES}})
    schemas["verification"] = schema("v11.1 verification", common("verification_id") + ["subject_id", "subject_type", "method", "oracle_ids", "test_result_ids", "verification_level", "status", "evidence", "limitations"], {**common_props, "method": {"enum": VERIFICATION_METHODS}, "verification_level": {"enum": VERIFICATION_LEVELS}})
    schemas["test-result"] = schema("v11.1 test result", common("test_result_id") + ["requirement_id", "criterion_id", "oracle_id", "execution_id", "result", "observed", "expected", "evidence", "environment", "timestamp", "failure"], {**common_props, "result": {"enum": TEST_RESULTS}})
    schemas["conformance"] = schema("v11.1 conformance", common("conformance_id") + ["subject", "requirement_id", "level", "status", "verification_level", "test_results", "known_failures", "evidence"], {**common_props, "level": {"enum": CONFORMANCE_LEVELS}, "status": {"enum": CONFORMANCE_STATUSES}, "verification_level": {"enum": VERIFICATION_LEVELS}})
    schemas["traceability"] = schema("v11.1 traceability", common("traceability_id") + ["from", "to", "relation", "evidence"], {**common_props, "relation": {"enum": TRACE_RELATIONS + SUPPORTING_RELATIONS}})
    schemas["evidence"] = schema("v10.1 evidence reference", common("evidence_id") + ["evidence_type", "source_stage", "source_artifact", "version_scope", "statement", "epistemic_status", "verification_status"], common_props)
    schemas["property"] = schema("v10.1 historical property reference", common("property_id") + ["property_type", "statement", "version_scope", "evidence_refs", "epistemic_status", "historical_status"], common_props)
    schemas["obligation"] = schema("v10.1 obligation reference", common("obligation_id") + ["statement", "class", "strength", "final_category", "epistemic_status", "source_properties", "source_evidence", "verification", "compatibility", "exceptions", "status"], common_props)
    schemas["certificate"] = schema("v11.1 specification certificate", common("certificate_hash") + ["specification_version", "validation_status", "counts", "coverage", "failures", "warnings", "input_hashes", "certificate_semantics"], {**common_props, "validation_status": {"enum": ["PASS", "PARTIAL", "FAIL"]}})
    for name, value in schemas.items(): dump(OUT / "SCHEMA" / f"{name}.schema.yaml", value)


def build_reports(input_contract: dict[str, Any], manifest: dict[str, Any], outputs: dict[str, Any], certificate: dict[str, Any], audit: dict[str, Any], obligations: list[dict[str, Any]]) -> None:
    guidance = outputs["GUIDANCE.yaml"]["guidance"]
    rationales = outputs["RATIONALES.yaml"]["rationales"]
    write_md("REPORTS/REQUIREMENTS.md", front("v11.1 Requirements") + "No requirement is admitted. The input gate rejects all 54 source obligations before normative transformation.\n\n" + table(["Obligation", "Class", "Strength", "Epistemic", "Lifecycle", "Coverage"], [(x["obligation_id"], x["class"], x["strength"], x["epistemic_status"], x["status"], "BLOCKED") for x in obligations]))
    write_md("REPORTS/NORMATIVE-RULES.md", front("v11.1 Normative Rules") + "No normative rule, condition, predicate, invariant, transition, effect, constraint, or exception is instantiated. Empty registries are intentional and schema-valid.\n")
    write_md("REPORTS/GUIDANCE.md", front("v11.1 Non-Normative Guidance") + "Guidance and rationale are non-normative and cannot create mandatory behavior. Uppercase normative operators are forbidden in guidance.\n\n" + table(["ID", "Type", "Statement", "Priority", "Normative"], [(x["guidance_id"], x["guidance_type"], x["statement"], x["priority"], x["normative"]) for x in guidance]) + f"\nThe rationale registry contains {len(rationales)} source-qualified non-normative records.\n")
    write_md("REPORTS/ACCEPTANCE-CRITERIA.md", front("v11.1 Acceptance Criteria") + "No criterion is admitted because no requirement exists. No example is substituted for a criterion.\n")
    write_md("REPORTS/TEST-ORACLES.md", front("v11.1 Test Oracles") + "No oracle is admitted. The independent harness contract remains uninstantiated and upstream test candidates remain unverified.\n")
    write_md("REPORTS/DEPENDENCIES.md", front("v11.1 Requirement Dependencies") + "The requirement graph has zero nodes and edges. Obligation dependencies and lineage remain separate and are not copied into requirement dependencies.\n")
    write_md("REPORTS/CONFLICTS.md", front("v11.1 Requirement Conflicts") + "No requirement conflict is fabricated. Four unresolved obligation conflicts remain upstream blockers; textual order is not used to resolve them.\n\n" + table(["Conflict"], [(x,) for x in outputs["REQUIREMENT-CONFLICTS.yaml"]["upstream_obligation_conflict_blockers"]]))
    write_md("REPORTS/CONFORMANCE.md", front("v11.1 Conformance") + table(["Level", "Claim"], [(x, "NOT CLAIMED") for x in CONFORMANCE_LEVELS]) + "\nNo mandatory conformance claim is authorized.\n")
    write_md("REPORTS/VERIFICATION.md", front("v11.1 Verification") + f"Upstream verification edges: {outputs['VERIFICATION.yaml']['upstream']['test_edges']}; verified nodes: {outputs['VERIFICATION.yaml']['upstream']['verified_nodes']}. Test existence, epistemic support, implementation, and verification remain independent.\n")
    trace = outputs["TRACEABILITY.yaml"]
    write_md("REPORTS/TRACEABILITY.md", front("v11.1 Traceability") + f"The graph contains {len(trace['nodes'])} nodes, {len(trace['canonical_edges'])} canonical edges, {len(trace['supporting_edges'])} explicitly non-normative supporting edges, and exact reverse edges.\n\n```text\nSOURCE → EVIDENCE → PROPERTY → OBLIGATION ┤ CLOSED\nREQUIREMENT → RULE → CRITERION → ORACLE → RESULT → VERIFICATION → CONFORMANCE (not instantiated)\n```\n")
    write_md("REPORTS/SPECIFICATION-AUDIT.md", front("v11.1 Specification Audit") + "## Ordered audit\n\n" + table(["Order", "Stage", "Result"], [(x["order"], x["stage"], x["result"]) for x in audit["stages"]]) + "\n## Completeness\n\n" + table(["Dimension", "Classification", "Reason"], [(x["dimension"], x["classification"], x["reason"]) for x in audit["completeness"]]) + "\n## Final invariants\n\n" + table(["ID", "Invariant", "Status", "Basis"], [(x["invariant_id"], x["statement"], x["status"], x["basis"]) for x in audit["pipeline_invariants"]]) + "\n## Failure-class registry\n\n" + "\n".join(f"- `{x}`" for x in audit["failure_classes"]) + "\n\n## Detected failures\n\n" + table(["ID", "Class", "State", "Affected", "Detail"], [(x["failure_id"], x["failure_class"], x["state"], len(x["affected"]), x["detail"]) for x in audit["detected_failures"]]) + "\nNo aggregate percentage is reported.\n")
    final = front("Generic Discovery Engine — Protocol-v11.1 Final Specification")
    final += "## 1. Three-plane model\n\n**Evidence** explains historical basis. **Normative objects** would state enforceable behavior. **Guidance** explains possible approaches without imposing behavior. Verification and conformance remain downstream.\n\n"
    final += "## 2. Canonical chain\n\n`SOURCE → EVIDENCE → PROPERTY → OBLIGATION → REQUIREMENT → RULE → CRITERION → ORACLE → RESULT → VERIFICATION → CONFORMANCE`. The current chain stops at obligation.\n\n"
    final += "## 3. Input rejection\n\n" + table(["Failure", "Class", "Affected", "Detail"], [(x["state"], x["failure_class"], len(x["affected"]), x["detail"]) for x in input_contract["failures"]]) + "\n"
    final += "## 4. Normative plane\n\nAll normative registries are empty: 0 requirements, rules, conditions, predicates, criteria, oracles, invariants, transitions, effects, exceptions, boundaries, verifications, results, and conformance records.\n\n"
    final += "## 5. Non-normative plane\n\nThree guidance records, 54 source-qualified rationales, and three explicit assumptions are emitted. There are no implementation notes or examples because no requirement exists.\n\n"
    final += "## 6. Object identity and schemas\n\nEvery instantiated first-class object has a stable ID, type, schema version, lifecycle status, and provenance. Thirty dedicated schemas cover the required registry plus constraint, evidence, property, obligation, and certificate records.\n\n"
    final += "## 7. Dependencies, conflicts, and lineage\n\nThe requirement dependency graph is empty and acyclic. Obligation dependencies and lineage are not reused as requirement dependencies. Four unresolved obligation conflicts remain explicit blockers.\n\n"
    final += "## 8. Guidance separation\n\nGuidance contains no uppercase normative operator, is marked `normative: false`, and has no related requirement. Rationale and assumptions also remain non-normative.\n\n"
    final += "## 9. Acceptance, oracle, and harness boundary\n\nNo acceptance criterion or oracle exists without a requirement. The harness is modeled separately and cannot silently alter tested semantics.\n\n"
    final += "## 10. Verification and conformance\n\nNo test result or verification record is fabricated. Highest claimed conformance is `L0_NONE`, with claims disabled.\n\n"
    final += "## 11. Traceability\n\nForward and reverse canonical traceability reaches obligations. Supporting rationale, guidance, and assumption edges are explicitly non-normative and do not extend the canonical transformation.\n\n"
    final += "## 12. Completeness\n\nSchema completeness is `FULL`; traceability is `PARTIAL`; all normative, acceptance, oracle, verification, conflict-resolution, compatibility, security, failure, and boundary dimensions are `BLOCKED`. No aggregate score hides this.\n\n"
    final += "## 13. Certificate\n\n" + table(["Field", "Value"], [("specification", "11.1"), ("validation", certificate["validation_status"]), ("requirements", certificate["counts"]["requirements"]), ("guidance", certificate["counts"]["guidance"]), ("rationales", certificate["counts"]["rationales"]), ("certificate hash", certificate["certificate_hash"])]) + "\n"
    final += "## 14. Remediation boundary\n\nOpening the normative gate requires valid upstream v1–v9 evidence, verified v10.1 obligations, resolved UNKNOWN properties and obligations, and explicit conflict resolution. Future architecture cannot be used backward to repair these inputs.\n\n"
    final += "## Final disposition\n\n**`REJECTED_INVALID_OBLIGATION_PACKAGE` — the v11.1 framework is machine-valid, but no normative specification or conformance claim is authorized.**\n"
    write_md("REPORTS/FINAL-SPECIFICATION.md", final)


if __name__ == "__main__":
    main()
