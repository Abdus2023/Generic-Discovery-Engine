#!/usr/bin/env python3
"""Executable machine-contract oracle for v14.7-R6."""
import hashlib
import json
import unicodedata

ENUMS = {
    "ValidationStatus": ["VALID", "INVALID", "BLOCKED", "UNKNOWN"],
    "EvaluationValue": ["TRUE", "FALSE", "UNKNOWN", "BLOCKED", "INVALID"],
    "ConformanceStatus": ["CONFORMANT", "PARTIALLY_CONFORMANT", "NON_CONFORMANT", "UNVERIFIED", "BLOCKED", "NOT_APPLICABLE", "UNKNOWN"],
    "CertificateLifecycle": ["DRAFT", "ISSUED", "REVOKED", "SUPERSEDED", "EXPIRED", "CANCELLED"],
    "CertificateValidity": ["VALID", "INVALID", "NOT_YET_VALID", "UNKNOWN"],
    "ReleaseEligibility": ["ELIGIBLE", "INELIGIBLE", "BLOCKED", "UNKNOWN"],
    "AuthorizationStatus": ["AUTHORIZED", "REFUSED", "BLOCKED", "UNKNOWN", "INVALID"],
    "ReleaseDecisionStatus": ["APPROVED", "REJECTED", "BLOCKED", "DEFERRED"],
    "ReleaseExecutionStatus": ["NOT_STARTED", "STARTED", "SUCCEEDED", "FAILED", "CANCELLED", "ROLLED_BACK"],
    "PostReleaseVerificationStatus": ["NOT_STARTED", "IN_PROGRESS", "PASSED", "FAILED", "INCONCLUSIVE", "BLOCKED", "INVALID"],
    "ReuseStatus": ["REUSABLE", "NOT_REUSABLE", "BLOCKED", "UNKNOWN", "INVALID"],
    "AuthorityStatus": ["ACTIVE", "SUSPENDED", "REVOKED", "EXPIRED", "UNKNOWN"],
    "AuthorityQualificationStatus": ["QUALIFIED", "NOT_QUALIFIED", "BLOCKED", "UNKNOWN", "INVALID"],
    "RequirementLifecycle": ["PROPOSED", "DRAFT", "ACTIVE", "DEPRECATED", "SUPERSEDED", "RETIRED"],
    "FindingStatus": ["OPEN", "TRIAGED", "ROOT_CAUSE_IDENTIFIED", "REMEDIATION_PLANNED", "REMEDIATION_IN_PROGRESS", "READY_FOR_REVERIFICATION", "REVERIFICATION_IN_PROGRESS", "RESOLVED", "WAIVED", "REJECTED", "CLOSED"],
    "RemediationStatus": ["PLANNED", "APPROVED", "IN_PROGRESS", "BLOCKED", "READY_FOR_VERIFICATION", "VERIFIED", "FAILED", "CANCELLED", "SUPERSEDED"],
    # Frozen R5 domains omitted by the supplied R6 abbreviated registry remain inherited.
    "EventValidationStatus": ["VALID", "INVALID", "BLOCKED", "UNKNOWN"],
    "EventCommitStatus": ["PENDING", "COMMITTED", "REJECTED"],
    "ProjectionStatus": ["CURRENT", "REPLAYING", "STALE", "INVALID", "BLOCKED", "UNKNOWN"],
    "NormativeStrength": ["MUST", "MUST_NOT", "SHOULD", "SHOULD_NOT", "MAY"],
}
ERRORS = ["INVALID_PREDICATE", "INVALID_SUBJECT", "INVALID_CONTEXT", "VALIDATION_REQUIRED", "VALIDATION_FAILED", "UNSUPPORTED_PREDICATE", "EVALUATOR_FAILURE", "EVALUATOR_TIMEOUT", "EVALUATOR_RESOURCE_FAILURE", "EVALUATOR_INTERNAL_FAILURE", "OUTPUT_INVALID", "EVALUATOR_DEPENDENCY_UNAVAILABLE"]
ERROR_ALLOWED = {
    "INVALID_PREDICATE": {"INVALID"}, "INVALID_SUBJECT": {"INVALID"}, "INVALID_CONTEXT": {"INVALID"},
    "VALIDATION_REQUIRED": {"INVALID"}, "VALIDATION_FAILED": {"INVALID"}, "UNSUPPORTED_PREDICATE": {"BLOCKED"},
    "EVALUATOR_FAILURE": set(), "EVALUATOR_TIMEOUT": {"UNKNOWN", "BLOCKED"}, "EVALUATOR_RESOURCE_FAILURE": {"BLOCKED"},
    "EVALUATOR_INTERNAL_FAILURE": set(), "OUTPUT_INVALID": {"INVALID"}, "EVALUATOR_DEPENDENCY_UNAVAILABLE": {"UNKNOWN", "BLOCKED"},
}
CERTIFICATE_TRANSITIONS = {("DRAFT", "ISSUED"), ("DRAFT", "CANCELLED"), ("ISSUED", "REVOKED"), ("ISSUED", "SUPERSEDED"), ("ISSUED", "EXPIRED")}
EXECUTION_TRANSITIONS = {("NOT_STARTED", "STARTED"), ("STARTED", "SUCCEEDED"), ("STARTED", "FAILED"), ("STARTED", "CANCELLED"), ("FAILED", "ROLLED_BACK"), ("SUCCEEDED", "ROLLED_BACK")}


def canonical(value):
    def normalize(item):
        if isinstance(item, float): raise ValueError("float requires an explicit profile rule")
        if isinstance(item, str): return unicodedata.normalize("NFC", item)
        if isinstance(item, list): return [normalize(value) for value in item]
        if isinstance(item, dict): return {unicodedata.normalize("NFC", key): normalize(value) for key, value in item.items()}
        return item
    return json.dumps(normalize(value), sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def identity(domain, value): return hashlib.sha256(domain.encode("ascii") + b":" + canonical(value)).hexdigest()


def enum_validate(domain, value):
    if domain not in ENUMS: return "UNKNOWN_DOMAIN"
    if value in ENUMS[domain]: return "VALID"
    if any(value in values for name, values in ENUMS.items() if name != domain): return "WRONG_DOMAIN"
    return "UNKNOWN_VALUE"


def schema_validate(schema, value):
    if not isinstance(value, dict): return "TYPE_INVALID"
    fields = schema["fields"]
    missing = [field for field in schema["required"] if field not in value]
    if missing: return "MISSING_REQUIRED"
    if schema["additional_fields"] == "FORBIDDEN" and set(value) - set(fields): return "UNKNOWN_FIELD"
    for name, spec in fields.items():
        if name not in value: continue
        item = value[name]
        if item is None:
            if not spec.get("nullable", False): return "NULL_FORBIDDEN"
            continue
        kind = spec["type"]
        if kind == "string" and not isinstance(item, str): return "TYPE_INVALID"
        if kind == "integer" and (not isinstance(item, int) or isinstance(item, bool)): return "TYPE_INVALID"
        if kind == "boolean" and not isinstance(item, bool): return "TYPE_INVALID"
        if kind == "array" and not isinstance(item, list): return "TYPE_INVALID"
        if kind == "object" and not isinstance(item, dict): return "TYPE_INVALID"
        if spec.get("enum_domain") and enum_validate(spec["enum_domain"], item) != "VALID": return "ENUM_INVALID"
        if spec.get("allowed_values") and item not in spec["allowed_values"]: return "ENUM_INVALID"
        if kind == "object" and spec.get("shape"):
            shape = spec["shape"]
            if any(name not in item for name in shape["required"]): return "MISSING_REQUIRED"
            if shape.get("additional_fields") == "FORBIDDEN" and set(item) - set(shape["fields"]): return "UNKNOWN_FIELD"
            if any(not isinstance(item[name], str) for name in shape["required"]): return "TYPE_INVALID"
        if kind == "array" and spec.get("unique") and len({canonical(x) for x in item}) != len(item): return "DUPLICATE_ITEM"
    return "VALID"


def error_disposition(code, policy=None):
    if code not in ERRORS: return "EVALUATION_FAILURE"
    if policy is None: return "EVALUATION_FAILURE"
    target = policy.get("mapping")
    if not policy.get("explicit") or not policy.get("profile_ref") or target not in ERROR_ALLOWED[code]: return "EVALUATION_FAILURE"
    return target


def convert(rule, source_type, source_value, target_type, evidence=None, policy=None):
    if not rule or rule["source_type"] != source_type or rule["target_type"] != target_type: return "REJECTED"
    if source_value not in rule["legal"]: return "REJECTED"
    if rule.get("evidence_required") and not evidence: return "REJECTED"
    if rule.get("policy_required") and not policy: return "REJECTED"
    return rule["legal"][source_value]


def guard_transition(domain, source, target, context):
    if not all(context.get(key) for key in ["structural", "reference", "integrity", "temporal", "scope", "authority"]): return "TRANSITION_ERROR"
    transitions = CERTIFICATE_TRANSITIONS if domain == "CertificateLifecycle" else EXECUTION_TRANSITIONS if domain == "ReleaseExecutionStatus" else set()
    return "VALIDATED" if (source, target) in transitions else "ILLEGAL_TRANSITION"


def project(history, profile_ref, algorithm):
    if any(not event.get("validated") or not event.get("committed") for event in history): return {"status": "INVALID_HISTORY"}
    sequences = [event["sequence_no"] for event in history]
    if sequences != sorted(sequences) or len(sequences) != len(set(sequences)): return {"status": "INVALID_HISTORY"}
    expected = list(range(sequences[0], sequences[0] + len(sequences))) if sequences else []
    if sequences != expected: return {"status": "MISSING_EVENT"}
    return {"status": "CURRENT", "state_hash": identity("projection-state:v1", {"history": history, "profile": profile_ref, "algorithm": algorithm})}


def reuse(old_basis, new_basis, compatible=False):
    if old_basis is None or new_basis is None: return "INVALID"
    if canonical(old_basis) == canonical(new_basis): return "REUSABLE"
    return "REUSABLE" if compatible else "NOT_REUSABLE"
