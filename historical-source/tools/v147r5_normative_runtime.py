#!/usr/bin/env python3
"""Executable enum, evaluator-error, conversion, and aggregation contracts for R5."""
import hashlib
import json
import unicodedata

ENUMS = {
    "Evaluation": ["TRUE", "FALSE", "UNKNOWN", "BLOCKED", "INVALID"],
    "Validation": ["VALID", "INVALID", "BLOCKED", "UNKNOWN"],
    "Conformance": ["CONFORMANT", "PARTIALLY_CONFORMANT", "NON_CONFORMANT", "UNVERIFIED", "BLOCKED", "NOT_APPLICABLE", "UNKNOWN"],
    "CertificateLifecycle": ["DRAFT", "ISSUED", "REVOKED", "SUPERSEDED", "EXPIRED", "CANCELLED"],
    "CertificateValidity": ["VALID", "INVALID", "NOT_YET_VALID", "UNKNOWN"],
    "ReleaseEligibility": ["ELIGIBLE", "INELIGIBLE", "BLOCKED", "UNKNOWN"],
    "Authorization": ["AUTHORIZED", "REFUSED", "BLOCKED", "UNKNOWN", "INVALID"],
    "ReleaseDecision": ["APPROVED", "REJECTED", "BLOCKED", "DEFERRED"],
    "ReleaseExecution": ["NOT_STARTED", "STARTED", "SUCCEEDED", "FAILED", "CANCELLED", "ROLLED_BACK"],
    "PostReleaseVerification": ["NOT_STARTED", "IN_PROGRESS", "PASSED", "FAILED", "INCONCLUSIVE", "BLOCKED", "INVALID"],
    "Reuse": ["REUSABLE", "NOT_REUSABLE", "BLOCKED", "UNKNOWN", "INVALID"],
    "Authority": ["ACTIVE", "SUSPENDED", "REVOKED", "EXPIRED", "UNKNOWN"],
    "AuthorityQualification": ["QUALIFIED", "NOT_QUALIFIED", "BLOCKED", "UNKNOWN", "INVALID"],
    "EventValidation": ["VALID", "INVALID", "BLOCKED", "UNKNOWN"],
    "EventCommit": ["PENDING", "COMMITTED", "REJECTED"],
    "Projection": ["CURRENT", "REPLAYING", "STALE", "INVALID", "BLOCKED", "UNKNOWN"],
    "RequirementLifecycle": ["PROPOSED", "DRAFT", "ACTIVE", "DEPRECATED", "SUPERSEDED", "RETIRED"],
    "FindingLifecycle": ["OPEN", "TRIAGED", "ROOT_CAUSE_IDENTIFIED", "REMEDIATION_PLANNED", "REMEDIATION_IN_PROGRESS", "READY_FOR_REVERIFICATION", "REVERIFICATION_IN_PROGRESS", "RESOLVED", "WAIVED", "REJECTED", "CLOSED"],
    "Remediation": ["PLANNED", "APPROVED", "IN_PROGRESS", "BLOCKED", "READY_FOR_VERIFICATION", "VERIFIED", "FAILED", "CANCELLED", "SUPERSEDED"],
    "NormativeStrength": ["MUST", "MUST_NOT", "SHOULD", "SHOULD_NOT", "MAY"],
}
EVALUATOR_ERRORS = [
    "INVALID_PREDICATE", "INVALID_SUBJECT", "INVALID_CONTEXT", "VALIDATION_REQUIRED", "VALIDATION_FAILED",
    "UNSUPPORTED_PREDICATE", "EVALUATOR_FAILURE", "EVALUATOR_TIMEOUT", "EVALUATOR_RESOURCE_FAILURE",
    "EVALUATOR_INTERNAL_FAILURE", "OUTPUT_INVALID", "EVALUATOR_DEPENDENCY_UNAVAILABLE",
]
ERROR_ALLOWED_MAPPINGS = {
    "INVALID_PREDICATE": {"INVALID"}, "INVALID_SUBJECT": {"INVALID"}, "INVALID_CONTEXT": {"INVALID"},
    "VALIDATION_REQUIRED": {"INVALID"}, "VALIDATION_FAILED": {"INVALID"}, "UNSUPPORTED_PREDICATE": {"BLOCKED"},
    "EVALUATOR_FAILURE": set(), "EVALUATOR_TIMEOUT": {"UNKNOWN", "BLOCKED"},
    "EVALUATOR_RESOURCE_FAILURE": {"BLOCKED"}, "EVALUATOR_INTERNAL_FAILURE": set(), "OUTPUT_INVALID": {"INVALID"},
    "EVALUATOR_DEPENDENCY_UNAVAILABLE": {"UNKNOWN", "BLOCKED"},
}


def canonicalize(value):
    def normalize(item):
        if isinstance(item, float):
            raise ValueError("floating point requires an explicit schema rule")
        if isinstance(item, str):
            return unicodedata.normalize("NFC", item)
        if isinstance(item, list):
            return [normalize(value) for value in item]
        if isinstance(item, dict):
            return {unicodedata.normalize("NFC", key): normalize(value) for key, value in item.items()}
        return item
    return json.dumps(normalize(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def hash_identity(domain, value):
    return hashlib.sha256(domain.encode("ascii") + b":" + canonicalize(value)).hexdigest()


def validate_enum(domain, value):
    if domain not in ENUMS:
        return {"status": "INVALID", "code": "UNKNOWN_ENUM_DOMAIN"}
    if value not in ENUMS[domain]:
        wrong_domain = any(value in values for name, values in ENUMS.items() if name != domain)
        return {"status": "INVALID", "code": "WRONG_ENUM_DOMAIN" if wrong_domain else "UNKNOWN_ENUM_VALUE"}
    return {"status": "VALID", "code": None}


def evaluator_error_disposition(error, policy=None):
    if error not in EVALUATOR_ERRORS:
        return {"disposition": "EVALUATION_FAILURE", "code": "UNKNOWN_EVALUATOR_ERROR"}
    if policy is None:
        return {"disposition": "EVALUATION_FAILURE", "code": error}
    mapping = policy.get("mappings", {}).get(error)
    if mapping not in ERROR_ALLOWED_MAPPINGS[error]:
        return {"disposition": "EVALUATION_FAILURE", "code": error}
    if not policy.get("profile_policy_ref") or not policy.get("deterministic"):
        return {"disposition": "EVALUATION_FAILURE", "code": "UNAUTHORIZED_ERROR_MAPPING"}
    return {"disposition": mapping, "code": error}


def explicit_conversion(rule, source_type, source_state, target_type, evidence=None, policy_ref=None):
    if not rule or rule.get("source_type") != source_type or rule.get("target_type") != target_type:
        return {"status": "REJECTED", "code": "RULE_TYPE_MISMATCH"}
    mapping = rule.get("legal_mappings", {}).get(source_state)
    if mapping is None:
        return {"status": "REJECTED", "code": "FORBIDDEN_MAPPING"}
    if rule.get("required_evidence") and not evidence:
        return {"status": "REJECTED", "code": "REQUIRED_EVIDENCE_MISSING"}
    if rule.get("applicable_policy") and policy_ref != rule["applicable_policy"]:
        return {"status": "REJECTED", "code": "POLICY_MISMATCH"}
    return {"status": "ALLOWED", "target_state": mapping, "rule_ref": rule["rule_id"]}


def aggregate(mandatory, optional=None, empty_action=None, evaluator_errors=None, stale_evidence=False, artifact_valid=True):
    optional = optional or []
    evaluator_errors = evaluator_errors or []
    if empty_action not in {"ALLOW", "DENY", "BLOCK", "UNKNOWN"}:
        return {"status": "PROFILE_VALIDATION_FAILURE"}
    if evaluator_errors:
        return {"status": "EVALUATION_FAILURE"}
    if not artifact_valid:
        return {"status": "INVALID_INPUT"}
    if stale_evidence:
        return {"status": "STALE_EVIDENCE"}
    grouped = {}
    for item in mandatory:
        predicate = item["predicate_ref"]
        value = item["result"]
        if value == "INVALID":
            return {"status": "INVALID_INPUT"}
        if predicate in grouped and grouped[predicate] != value:
            return {"status": "CONFLICTING_EVALUATIONS"}
        grouped[predicate] = value
    if not grouped:
        return {"status": {"ALLOW": "TRUE", "DENY": "FALSE", "BLOCK": "BLOCKED", "UNKNOWN": "UNKNOWN"}[empty_action], "optional": optional}
    values = list(grouped.values())
    if "FALSE" in values:
        return {"status": "FALSE", "optional": optional}
    if "BLOCKED" in values:
        return {"status": "BLOCKED", "optional": optional}
    if "UNKNOWN" in values:
        return {"status": "UNKNOWN", "optional": optional}
    return {"status": "TRUE", "optional": optional}


def temporal_check(kind, data):
    if kind == "EQUAL_TIMESTAMPS":
        return "VALID" if data["left"] == data["right"] else "INVALID"
    if kind == "CLOCK_SKEW":
        return "VALID" if abs(data["observed"] - data["trusted"]) <= data["maximum"] else "INVALID"
    if kind == "EXPIRED_AUTHORITY":
        return "EXPIRED" if data["instant"] >= data["not_after"] else "ACTIVE"
    if kind == "STALE_EVIDENCE":
        return "STALE" if data["age"] > data["maximum_age"] else "FRESH"
    if kind == "FUTURE_EVIDENCE":
        return "INVALID" if data["collected_at"] > data["trusted_now"] + data["maximum_skew"] else "VALID"
    if kind == "SEQUENCE_CONFLICT":
        return "CONFLICT" if len(data["sequences"]) != len(set(data["sequences"])) else "VALID"
    return "INVALID"


def integrity_check(kind, expected, actual):
    if kind not in {"HASH", "SIGNATURE", "EVALUATOR_HASH", "PROFILE_HASH", "DECISION_BASIS_HASH"}:
        return "INVALID_CHECK"
    return "VALID" if expected == actual else "INVALID"
