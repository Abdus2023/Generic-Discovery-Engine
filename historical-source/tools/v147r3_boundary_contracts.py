#!/usr/bin/env python3
"""Executable v14.7-R3 authority, boundary, conversion, and conformance contracts."""
import hashlib
import json
import re

LAYERS = ("SPECIFICATION", "PROFILE", "IMPLEMENTATION")
CLASSIFICATIONS = (
    "NORMATIVE_REQUIREMENT",
    "ACCEPTANCE_CRITERION",
    "PROFILE_BINDING",
    "IMPLEMENTATION_INSTRUCTION",
    "IMPLEMENTATION_GUIDANCE",
    "OBSERVATION",
    "EVIDENCE",
)
VALIDATION_RESULTS = ("VALID", "INVALID", "BLOCKED", "UNKNOWN")
EVALUATION_RESULTS = ("TRUE", "FALSE", "UNKNOWN", "BLOCKED", "INVALID")
CONFORMANCE_RESULTS = (
    "CONFORMANT",
    "PARTIALLY_CONFORMANT",
    "NON_CONFORMANT",
    "UNVERIFIED",
    "BLOCKED",
    "NOT_APPLICABLE",
    "UNKNOWN",
)
RECOVERABILITY = (
    "RETRYABLE",
    "NON_RETRYABLE",
    "REQUIRES_NEW_EVIDENCE",
    "REQUIRES_AUTHORITY",
    "REQUIRES_PROFILE_CHANGE",
    "REQUIRES_IMPLEMENTATION_CHANGE",
    "REQUIRES_SPECIFICATION_REVIEW",
)
ERROR_DOMAINS = (
    "ValidationError",
    "EvaluationError",
    "ConformanceError",
    "AuthorizationError",
    "TransitionError",
    "EventStoreError",
    "ProjectionError",
    "ExecutionError",
    "VerificationError",
)
CONCRETE_MECHANISMS = (
    "sqlite",
    "postgresql",
    "tokio",
    "sha2 crate",
    "ring crate",
    "rust crate",
    "unique(stream_id, sequence_no)",
)


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def object_hash(domain, value):
    body = {k: v for k, v in value.items() if k != "content_hash"}
    return hashlib.sha256(domain.encode("ascii") + b"\x00" + canonical_bytes(body)).hexdigest()


def result(status, code=None, detail=None, **extra):
    return {"status": status, "code": code, "detail": detail, **extra}


def _contains_mechanism(statement):
    text = statement.lower()
    return any(term in text for term in CONCRETE_MECHANISMS)


def validate_boundary_artifact(artifact, frozen_profile=None):
    """Return ValidationResult and a B001..B012 defect code when applicable."""
    kind = artifact.get("kind")
    if kind == "statement_classification":
        statement = artifact.get("statement", "")
        classification = artifact.get("classification")
        if re.search(r"\bMUST(?:_NOT)?\b", statement) and classification == "IMPLEMENTATION_GUIDANCE":
            return result("INVALID", "B010", "normative statement classified as guidance")
        if _contains_mechanism(statement) and classification == "NORMATIVE_REQUIREMENT":
            return result("INVALID", "B011", "implementation statement classified as normative")
    if kind == "normative_requirement" and _contains_mechanism(artifact.get("statement", "")):
        return result("INVALID", "B001", "requirement contains implementation mechanism")
    if kind == "implementation_instruction" and not artifact.get("authority_ref"):
        return result("INVALID", "B002", "implementation instruction lacks authority")
    if kind == "profile_binding" and not artifact.get("requirement_ref") and not artifact.get("profile_wide"):
        return result("INVALID", "B003", "profile binding lacks requirement reference")
    if kind == "profile" and not artifact.get("specification_ref"):
        return result("INVALID", "B004", "profile lacks specification reference")
    if kind == "implementation" and not artifact.get("profile_ref"):
        return result("INVALID", "B005", "implementation lacks profile reference")
    if kind == "evidence":
        if not artifact.get("subject_ref"):
            return result("INVALID", "B006", "evidence lacks subject reference")
        if artifact.get("redefines_normative_meaning"):
            return result("INVALID", "B013", "evidence attempts normative override")
    if kind == "evaluation" and not artifact.get("predicate_ref"):
        return result("INVALID", "B007", "evaluation lacks predicate reference")
    if kind == "conformance" and not artifact.get("requirement_ref"):
        return result("INVALID", "B008", "conformance lacks requirement reference")
    if kind == "conversion" and not artifact.get("rule_ref"):
        return result("INVALID", "B009", "conversion lacks rule reference")
    if kind == "profile_change" and frozen_profile is not None:
        interpretation_changed = artifact.get("semantic_fingerprint") != frozen_profile.get("semantic_fingerprint")
        version_changed = artifact.get("profile_version") != frozen_profile.get("profile_version")
        if interpretation_changed and not version_changed:
            return result("INVALID", "B012", "frozen semantics changed without profile version")
    return result("VALID")


def authority_precedence(actor_layer, target_layer, operation="OVERRIDE"):
    """No lower layer may redefine a higher layer; evidence has no normative layer."""
    if operation != "OVERRIDE":
        return result("VALID")
    rank = {"SPECIFICATION": 3, "PROFILE": 2, "IMPLEMENTATION": 1, "EVIDENCE": 0}
    if actor_layer not in rank or target_layer not in rank:
        return result("INVALID", "AUTHORITY_LAYER_UNKNOWN")
    if rank[actor_layer] < rank[target_layer] or actor_layer == "EVIDENCE":
        return result("REJECTED", "AUTHORITY_PRECEDENCE")
    return result("ALLOWED")


def apply_conversion_rule(source_domain, source_state, target_domain, target_state, rule):
    """Apply one identified cross-domain rule; no unruled generic conversion exists."""
    if not rule or not rule.get("rule_id"):
        return result("REJECTED", "B009")
    expected = (rule.get("source_domain"), rule.get("source_state"), rule.get("target_domain"), rule.get("target_state"))
    requested = (source_domain, source_state, target_domain, target_state)
    if requested != expected:
        return result("REJECTED", "CONVERSION_RULE_MISMATCH")
    if not all(rule.get(key) for key in ("operation", "preconditions", "authority_ref")):
        return result("REJECTED", "INCOMPLETE_CONVERSION_RULE")
    return result("ALLOWED", rule_ref=rule["rule_id"])


def compare_profile_change(old_profile, new_profile):
    interpretation_keys = ("hash_algorithm", "serialization", "time_semantics", "ordering", "predicate_language", "wire_format")
    changed = any(old_profile.get(k) != new_profile.get(k) for k in interpretation_keys)
    if changed and old_profile.get("profile_version") == new_profile.get("profile_version"):
        return result("VERSION_REQUIRED")
    return result("PROFILE_REVISION" if changed else "NO_PROFILE_CHANGE")


def compare_implementation_change(old_implementation, new_implementation):
    profile_changed = old_implementation.get("profile_ref") != new_implementation.get("profile_ref")
    return result("PROFILE_CHANGE_REQUIRED" if profile_changed else "NO_PROFILE_CHANGE")


def distinct_approval_count(approvals, basis_hash):
    return len({a.get("authority_id") for a in approvals if a.get("valid") and a.get("basis_hash") == basis_hash})


def replay_projection(events):
    ordered = sorted(events, key=lambda event: (event["stream_id"], event["sequence_no"]))
    state = {}
    for event in ordered:
        state[event["key"]] = event["value"]
    return hashlib.sha256(canonical_bytes(state)).hexdigest()


def validate_for_evaluation(validation_status, subject_ref, context_ref):
    if validation_status not in VALIDATION_RESULTS:
        return result("INVALID", "VALIDATION_DOMAIN")
    if validation_status != "VALID":
        return result("BLOCKED", "REQUIRED_VALIDATION_NOT_VALID")
    if not subject_ref or not context_ref:
        return result("INVALID", "EVALUATION_INPUT_BINDING")
    return result("ELIGIBLE", validated_input={"subject_ref": subject_ref, "context_ref": context_ref})


def evaluate(validated_input, predicate_ref, inputs_ref, evaluator, evaluation_time, evidence_refs, scope_ref):
    required_validated = isinstance(validated_input, dict) and validated_input.get("subject_ref") and validated_input.get("context_ref")
    required_evaluator = isinstance(evaluator, dict) and evaluator.get("id") and evaluator.get("version")
    if not all((required_validated, predicate_ref, inputs_ref, required_evaluator, evaluation_time, scope_ref)):
        return result("INVALID", "EVALUATION_BINDING")
    if not isinstance(evidence_refs, list):
        return result("INVALID", "EVIDENCE_BINDING")
    return result("TRUE", predicate_ref=predicate_ref)


def derive_conformance(requirement_ref, scope_ref, acceptance_criteria, evaluations, evidence_refs,
                       evidence_validation="VALID", evidence_mandatory=False):
    if not requirement_ref:
        return result("NO_CONFORMANCE_RESULT", "B008")
    if not scope_ref or not acceptance_criteria:
        return result("NO_CONFORMANCE_RESULT", "CONFORMANCE_BINDING")
    if scope_ref == "NOT_APPLICABLE":
        return result("NOT_APPLICABLE")
    if not evidence_refs:
        if evidence_mandatory:
            return result("NON_CONFORMANT", violated_conditions=["MANDATORY_EVIDENCE_ABSENT"])
        return result("UNVERIFIED", violated_conditions=[])
    if evidence_validation != "VALID":
        return result("BLOCKED" if evidence_validation in {"BLOCKED", "UNKNOWN"} else "NO_CONFORMANCE_RESULT", "EVIDENCE_VALIDATION")
    if any(e.get("status") == "INVALID" for e in evaluations):
        return result("NO_CONFORMANCE_RESULT", "INVALID_EVALUATION")
    violated = [e.get("condition_ref") for e in evaluations if e.get("status") == "FALSE" and e.get("condition_ref")]
    false_without_condition = any(e.get("status") == "FALSE" and not e.get("condition_ref") for e in evaluations)
    if false_without_condition:
        return result("NO_CONFORMANCE_RESULT", "UNIDENTIFIED_VIOLATION")
    if violated:
        return result("NON_CONFORMANT", violated_conditions=violated)
    if any(e.get("status") == "BLOCKED" for e in evaluations):
        return result("BLOCKED", violated_conditions=[])
    if any(e.get("status") == "UNKNOWN" for e in evaluations):
        return result("UNKNOWN", violated_conditions=[])
    return result("CONFORMANT", violated_conditions=[])


def attach_recoverability(semantic_result, diagnostic):
    if diagnostic not in RECOVERABILITY:
        return result("INVALID", "RECOVERABILITY_DOMAIN")
    return {"status": semantic_result, "recoverability": diagnostic}


def validate_boundary_rule(rule_id, artifact):
    checks = {
        "BOUNDARY-001": artifact.get("kind") != "normative_requirement" or artifact.get("authority_layer") == "SPECIFICATION",
        "BOUNDARY-002": artifact.get("kind") != "profile_binding" or bool(artifact.get("requirement_ref") or artifact.get("profile_wide")),
        "BOUNDARY-003": artifact.get("kind") != "implementation_mapping" or bool(artifact.get("profile_binding_ref") or artifact.get("implementation_contract_ref")),
        "BOUNDARY-004": artifact.get("kind") != "evaluation" or bool(artifact.get("predicate_ref")),
        "BOUNDARY-005": artifact.get("kind") != "conformance" or bool(artifact.get("requirement_ref")),
        "BOUNDARY-006": artifact.get("kind") != "authorization" or all(artifact.get(x) for x in ("operation_ref", "authority_ref", "scope_ref", "policy_ref")),
        "BOUNDARY-007": artifact.get("kind") != "conversion" or bool(artifact.get("rule_ref")),
        "BOUNDARY-008": not artifact.get("weakens_requirement", False),
        "BOUNDARY-009": not artifact.get("interpretation_changed", False) or artifact.get("profile_version_changed", False),
        "BOUNDARY-010": not artifact.get("evidence_redefines_meaning", False),
    }
    return result("PASS" if checks.get(rule_id, False) else "FAIL", rule_ref=rule_id)
