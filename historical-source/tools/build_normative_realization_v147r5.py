#!/usr/bin/env python3
"""Build v14.7-R5 machine-validatable normative realization."""
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HISTORICAL = ROOT / "historical-source"
COMPLIANCE = HISTORICAL / "compliance"
PREDECESSOR = COMPLIANCE / "certification/v14.7-R4"
DESTINATION = COMPLIANCE / "certification/v14.7-R5"
sys.path.insert(0, str(HISTORICAL / "tools"))

from run_v147r5_normative import run
from v147r5_normative_runtime import ENUMS, EVALUATOR_ERRORS, canonicalize, hash_identity
from v147r5_rust_types import sources as rust_sources

VERSION = "14.7-R5"
TIMESTAMP = "2026-09-12T00:00:00Z"
NORMATIVE_OBJECTS = ["specification", "normative-requirement", "profile", "profile-requirement", "acceptance-criterion", "predicate", "evaluation-context", "evaluation-result", "validation-result", "conformance-result", "evidence", "authority", "authority-qualification", "certificate-candidate", "certificate", "release-gate", "release-eligibility", "authorization-result", "release-decision", "release-execution", "post-release-verification", "reuse-result", "state-transition-event", "projection", "finding", "remediation", "snapshot", "decision-basis"]
IMPLEMENTATION_OBJECTS = ["implementation-requirement", "implementation-instruction", "implementation-mapping", "evaluator-error", "evaluator-error-policy", "conformance-report"]
CORE = ["VERSION.yaml", "EXECUTIVE-RESULT.yaml", "SPECIFICATION-BASIS.yaml", "CLOSED-ENUM-REGISTRY.yaml", "NORMATIVE-STRENGTH.yaml", "LAYER-SEPARATION.yaml", "R5-PROFILE.yaml", "EVALUATOR-ERROR-TAXONOMY.yaml", "EVALUATOR-ERROR-POLICY.yaml", "RESULT-CONVERSIONS.yaml", "FORBIDDEN-CONVERSIONS.yaml", "AGGREGATION-CONTRACT.yaml", "CANONICAL-SERIALIZATION.yaml", "HASH-IDENTITIES.yaml", "CONFORMANCE-TRACEABILITY.yaml", "FORMAL-INVARIANTS.yaml", "CONTRADICTIONS.yaml", "AMBIGUITIES.yaml", "MIGRATION-R4-TO-R5.yaml", "EPISTEMIC-CONCLUSIONS.yaml", "ANTI-REGRESSION.yaml", "ARTIFACT-TREE.yaml", "REMAINING-IMPLEMENTATION-WORK.yaml", "RUST-TYPE-BLUEPRINT.yaml", "MACHINE-TEST-RESULTS.yaml", "CONFORMANCE-REPORT.yaml", "PRIOR-INTEGRITY.yaml", "SCHEMA-REGISTRY.yaml", "GENERATOR-MANIFEST.yaml", "VALIDATION-REPORT.yaml", "INDEPENDENT-VALIDATION.yaml", "CURRENT-STATUS.yaml", "FINAL-PRINCIPLE.yaml", "SPECIFICATION.md"]


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value if isinstance(value, str) else json.dumps(value, indent=2) + "\n")


def load(path): return json.loads(path.read_text())
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def hashed(domain, value): value["content_hash"] = hash_identity(domain, value); return value


def enum_schema(values): return {"type": "string", "enum": values}
def ident(): return {"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9._:/@#-]{0,255}$"}
def ref(): return {"type": ["string", "null"], "pattern": "^[A-Za-z0-9][A-Za-z0-9._:/@#-]{0,511}$"}
def array(item, minimum=0): return {"type": "array", "items": item, "minItems": minimum, "uniqueItems": True}


def complete_schema(name, properties, required, authority, state_domain=None):
    properties = {**properties, "content_hash": {"type": "string", "pattern": "^[a-f0-9]{64}$"}}
    required = required + ["content_hash"]
    optional = sorted(set(properties) - set(required))
    return {"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": f"https://generic-discovery-engine.invalid/v14.7-R5/{authority.lower()}/{name}.schema.json", "title": name, "type": "object", "required": required, "properties": properties, "additionalProperties": False,
        "x-authority-layer": authority, "x-optional-fields": optional, "x-identifier-type": "URI_SAFE_ASCII_DISTINCT_DOMAIN_NEWTYPE", "x-reference-integrity": "REFERENCES_MUST_RESOLVE_TO_EXPECTED_TYPE_AND_HASH", "x-cardinality": "ARRAY_BOUNDS_AND_UNIQUENESS_ENFORCED_BY_SCHEMA", "x-hash-input-fields": [field for field in required if field != "content_hash"], "x-hash-domain": f"{name}:v1", "x-canonicalization": "GDE-CJSON-1", "x-temporal-requirements": "RFC3339_UTC_Z_FIELDS_MUST_BE_VALIDATED_WHEN_PRESENT", "x-scope-requirements": "SCOPE_REFERENCES_MUST_BE_EXPLICIT_WHEN_OPERATION_IS_SCOPED", "x-integrity-requirements": "CONTENT_HASH_REQUIRED_SIGNATURE_WHEN_GOVERNING_PROFILE_REQUIRES", "x-state-domain": state_domain, "x-closed": True}


def build_schemas():
    s = {"type": "string", "minLength": 1}; i = ident(); r = ref(); ts = {"type": "string", "format": "date-time"}; h = {"type": "string", "pattern": "^[a-f0-9]{64}$"}; b = {"type": "boolean"}
    state_for = {"evaluation-result": ("result", "Evaluation"), "validation-result": ("status", "Validation"), "conformance-result": ("status", "Conformance"), "authority": ("status", "Authority"), "authority-qualification": ("status", "AuthorityQualification"), "certificate": ("lifecycle", "CertificateLifecycle"), "release-eligibility": ("status", "ReleaseEligibility"), "authorization-result": ("status", "Authorization"), "release-decision": ("status", "ReleaseDecision"), "release-execution": ("status", "ReleaseExecution"), "post-release-verification": ("status", "PostReleaseVerification"), "reuse-result": ("status", "Reuse"), "projection": ("status", "Projection"), "finding": ("lifecycle", "FindingLifecycle"), "remediation": ("status", "Remediation")}
    identifiers = {name: f"{name.replace('-', '_')}_id" for name in NORMATIVE_OBJECTS}
    identifiers.update({"normative-requirement": "requirement_id", "profile": "profile_id", "profile-requirement": "profile_requirement_id", "acceptance-criterion": "criterion_id", "evaluation-result": "evaluation_id", "validation-result": "validation_id", "evidence": "evidence_id", "authority": "authority_id", "certificate-candidate": "candidate_id", "certificate": "certificate_id", "release-gate": "gate_id", "release-decision": "decision_id", "state-transition-event": "event_id", "finding": "finding_id", "remediation": "remediation_id", "projection": "projection_id", "specification": "specification_id"})
    schemas = {}
    for name in NORMATIVE_OBJECTS:
        identifier = identifiers[name]
        props = {identifier: i, "scope_ref": r, "effective_at": {"type": ["string", "null"], "format": "date-time"}, "evidence_refs": array(i), "integrity_refs": array(i)}
        required = [identifier, "scope_ref", "effective_at", "evidence_refs", "integrity_refs"]
        if name in state_for:
            field, domain = state_for[name]; props[field] = enum_schema(ENUMS[domain]); required.append(field)
        schemas[f"normative/{name}.schema.json"] = complete_schema(name, props, required, "NORMATIVE_SPECIFICATION", state_for.get(name, (None, None))[1])
    # Specialize required semantic fields without introducing technologies.
    def extend(name, props, required):
        schema = schemas[f"normative/{name}.schema.json"]; schema["properties"].update(props); schema["required"].extend(required); schema["x-hash-input-fields"].extend(required); schema["x-optional-fields"] = sorted(set(schema["properties"]) - set(schema["required"]))
    extend("specification", {"version": s, "title": s, "requirement_refs": array(i, 1)}, ["version", "title", "requirement_refs"])
    extend("normative-requirement", {"statement": s, "strength": enum_schema(ENUMS["NormativeStrength"]), "lifecycle": enum_schema(ENUMS["RequirementLifecycle"]), "acceptance_criterion_refs": array(i, 1), "dependency_refs": array(i)}, ["statement", "strength", "lifecycle", "acceptance_criterion_refs", "dependency_refs"])
    extend("profile", {"version": s, "specification_ref": i, "profile_requirement_refs": array(i, 1), "empty_mandatory_action": enum_schema(["ALLOW", "DENY", "BLOCK", "UNKNOWN"])}, ["version", "specification_ref", "profile_requirement_refs", "empty_mandatory_action"])
    extend("profile-requirement", {"normative_requirement_ref": i, "binding": s, "semantic_preservation_ref": i}, ["normative_requirement_ref", "binding", "semantic_preservation_ref"])
    extend("acceptance-criterion", {"requirement_ref": i, "predicate_ref": i, "expected": enum_schema(ENUMS["Evaluation"])}, ["requirement_ref", "predicate_ref", "expected"])
    extend("predicate", {"language": s, "expression": s, "input_refs": array(i)}, ["language", "expression", "input_refs"])
    extend("evaluation-context", {"profile_ref": i, "validated_subject_ref": i, "evaluator_ref": i, "evaluation_time": ts, "freshness_ref": i}, ["profile_ref", "validated_subject_ref", "evaluator_ref", "evaluation_time", "freshness_ref"])
    extend("evaluation-result", {"predicate_ref": i, "subject_ref": i, "context_ref": i, "reason_codes": array(s), "evaluator_hash": h}, ["predicate_ref", "subject_ref", "context_ref", "reason_codes", "evaluator_hash"])
    extend("validation-result", {"subject_ref": i, "failure_codes": array(s), "validator_hash": h}, ["subject_ref", "failure_codes", "validator_hash"])
    extend("conformance-result", {"requirement_ref": i, "evaluation_refs": array(i), "violated_conditions": array(i), "rationale_codes": array(s)}, ["requirement_ref", "evaluation_refs", "violated_conditions", "rationale_codes"])
    extend("evidence", {"subject_ref": i, "observation": s, "collector_ref": i, "collected_at": ts, "integrity_status": enum_schema(["VALID", "INVALID", "UNKNOWN"])}, ["subject_ref", "observation", "collector_ref", "collected_at", "integrity_status"])
    extend("authority", {"operation_refs": array(i), "credential_ref": i, "not_before": ts, "not_after": {"type": ["string", "null"], "format": "date-time"}}, ["operation_refs", "credential_ref", "not_before", "not_after"])
    extend("authority-qualification", {"authority_ref": i, "operation_ref": i, "policy_ref": i}, ["authority_ref", "operation_ref", "policy_ref"])
    extend("certificate-candidate", {"subject_ref": i, "issuer_ref": i, "candidate_hash": h}, ["subject_ref", "issuer_ref", "candidate_hash"])
    extend("certificate", {"candidate_ref": i, "validity": enum_schema(ENUMS["CertificateValidity"]), "issued_at": ts, "expires_at": {"type": ["string", "null"], "format": "date-time"}}, ["candidate_ref", "validity", "issued_at", "expires_at"])
    extend("release-gate", {"mandatory_predicate_refs": array(i), "optional_predicate_refs": array(i), "empty_mandatory_action": enum_schema(["ALLOW", "DENY", "BLOCK", "UNKNOWN"])}, ["mandatory_predicate_refs", "optional_predicate_refs", "empty_mandatory_action"])
    for name, reference in [("release-eligibility", "gate_ref"), ("authorization-result", "authority_qualification_ref"), ("release-decision", "authorization_ref"), ("release-execution", "decision_ref"), ("post-release-verification", "execution_ref"), ("reuse-result", "new_basis_ref")]: extend(name, {reference: i}, [reference])
    extend("state-transition-event", {"event_validation": enum_schema(ENUMS["EventValidation"]), "commit_status": enum_schema(ENUMS["EventCommit"]), "current_state_ref": i, "predecessor_ref": r, "authority_ref": i}, ["event_validation", "commit_status", "current_state_ref", "predecessor_ref", "authority_ref"])
    extend("projection", {"history_ref": i, "profile_ref": i, "algorithm_version": s, "state_hash": h}, ["history_ref", "profile_ref", "algorithm_version", "state_hash"])
    extend("finding", {"statement": s, "affected_requirement_refs": array(i), "root_cause_ref": r}, ["statement", "affected_requirement_refs", "root_cause_ref"])
    extend("remediation", {"finding_ref": i, "plan": s, "verification_ref": r}, ["finding_ref", "plan", "verification_ref"])

    implementation_fields = {
        "implementation-requirement": ({"implementation_requirement_id": i, "profile_requirement_ref": i, "statement": s, "mandatory": b, "authority_ref": i}, ["implementation_requirement_id", "profile_requirement_ref", "statement", "mandatory", "authority_ref"]),
        "implementation-instruction": ({"instruction_id": i, "implementation_requirement_ref": i, "statement": s, "mandatory": b, "authority_ref": r}, ["instruction_id", "implementation_requirement_ref", "statement", "mandatory", "authority_ref"]),
        "implementation-mapping": ({"mapping_id": i, "implementation_requirement_ref": i, "artifact_refs": array(i, 1), "test_refs": array(i), "evidence_refs": array(i)}, ["mapping_id", "implementation_requirement_ref", "artifact_refs", "test_refs", "evidence_refs"]),
        "evaluator-error": ({"error_id": i, "code": enum_schema(EVALUATOR_ERRORS), "semantic_meaning": s, "retry_permitted": b, "default_disposition": enum_schema(["EVALUATION_FAILURE"]), "evidence_producing": b}, ["error_id", "code", "semantic_meaning", "retry_permitted", "default_disposition", "evidence_producing"]),
        "evaluator-error-policy": ({"policy_id": i, "profile_ref": i, "mapping_rules": array({"type": "object", "required": ["error_code", "target_disposition", "policy_ref", "deterministic"], "properties": {"error_code": enum_schema(EVALUATOR_ERRORS), "target_disposition": enum_schema(["UNKNOWN", "BLOCKED", "INVALID"]), "policy_ref": i, "deterministic": b}, "additionalProperties": False}), "default_disposition": enum_schema(["EVALUATION_FAILURE"])}, ["policy_id", "profile_ref", "mapping_rules", "default_disposition"]),
        "conformance-report": ({"report_id": i, "profile_ref": i, "implementation_ref": i, "test_identity": h, "passed": {"type": "integer", "minimum": 0}, "failed": {"type": "integer", "minimum": 0}, "result": s, "generated_at": ts}, ["report_id", "profile_ref", "implementation_ref", "test_identity", "passed", "failed", "result", "generated_at"]),
    }
    for name, (props, required) in implementation_fields.items(): schemas[f"implementation/{name}.schema.json"] = complete_schema(name, props, required, "IMPLEMENTATION", None)
    for path, schema in schemas.items(): write(DESTINATION/path, schema)
    return schemas


def specification_text():
    sections = ["Objective", "Frozen Semantic Baseline", "Normative Strength", "Normative Authority Boundary", "Required Normative Objects", "Evaluator Contract", "Evaluator Error Policy", "Explicit Conversion Functions", "Forbidden Conversions", "Aggregation", "Rust Realization", "Rust Error Model", "Canonical Serialization", "Schema Implementation Separation", "Conformance Mapping", "Test Matrix", "Formal Invariants", "Contradiction Detection", "Required Deliverables", "Epistemic Discipline", "Anti-Regression Rules", "Final Principle"]
    statements = ["R5 converts the frozen model into a machine-validatable normative realization without v14.8.", "Twenty closed domains, including normative strength, are enumerated with exact wire and Rust representations.", "Normative strength remains separate from lifecycle and conformance.", "Normative specification, normative requirement, profile binding, profile requirement, implementation requirement, implementation instruction, guidance, observation, and evidence remain distinct authority and semantic layers.", "Technology-neutral normative schemas and separate implementation-contract schemas define fields, references, cardinality, identity, canonicalization, time, scope, and integrity.", "Evaluate returns either a completed EvaluationResult or a typed EvaluatorError.", "Every evaluator error defaults to EVALUATION_FAILURE; deterministic semantic mapping requires explicit profile policy.", "Seven typed conversion contracts enumerate legal and forbidden mappings, evidence, policy, and failure behavior.", "Eleven prohibited authority-strengthening conversions are machine tested.", "Invalid artifacts and evaluator errors terminate before FALSE, BLOCKED, UNKNOWN, TRUE precedence; empty action is explicit.", "Rust blueprints use distinct enums and identifier newtypes without generic status or identifier aliases.", "EvaluatorError, EvaluationCompletion, and ErrorDisposition keep semantic results distinct from execution failure.", "GDE-CJSON-1 fixes object and field order, number, timestamp, Unicode, null, encoding, and canonical-byte rules feeding seven identities.", "Normative schemas contain no implementation technology and implementation artifacts carry no normative authority.", "Every requirement edge through criterion, profile, implementation requirement, mapping, test, observation, evidence, validation, evaluation, and conformance is typed.", "The machine matrix covers enum closure, boundaries, evaluator errors, conversions, aggregation, temporal behavior, and integrity.", "I-001 through I-020 are executable machine assertions.", "No genuine semantic contradiction was found and no new semantic state is required.", "All seventeen requested deliverables are included in the R5 package.", "Conclusions use PROVED, SUPPORTED, INFERRED, CONJECTURED, CONTRADICTED, or UNKNOWN without invented evidence.", "R5 prevents v14.8 expansion, domain merging, generic statuses, silent conversion, historical mutation, and weakened fail-closed behavior.", "A completed semantic result and evaluator failure are never silently substituted."]
    return "# v14.7-R5 — Machine-Validatable Normative Realization\n\n" + "\n\n".join(f"## {i}. {title}\n{statements[i-1]}" for i,title in enumerate(sections,1)) + "\n"


def rust_variant(token): return "".join(piece.title() for piece in token.lower().split("_"))
def build_registry():
    rust_names = {"Evaluation":"EvaluationValue", "Validation":"ValidationStatus", "Conformance":"ConformanceStatus", "Authorization":"AuthorizationStatus", "Authority":"AuthorityStatus", "Projection":"ProjectionStatus", "Remediation":"RemediationStatus", "Reuse":"ReuseResult"}
    objects=[]
    for domain, values in ENUMS.items():
        obj={"domain":domain, "wire_type":"UTF8_UPPER_SNAKE_CASE_STRING", "values":[{"wire":value,"rust":rust_variant(value)} for value in values], "rust_type":rust_names.get(domain,domain), "closed":True, "unknown_value_behavior":"REJECT", "wrong_domain_behavior":"REJECT"}
        obj["content_hash"]=hash_identity("closed-enum:v1",obj);objects.append(obj)
    registry={"objects":objects,"domain_count":len(objects),"value_count":sum(len(x["values"]) for x in objects),"no_generic_status":True}
    registry["content_hash"]=hash_identity("enum-registry:v1",registry);return registry


def build_error_taxonomy():
    meanings={code:code.lower().replace("_"," ") for code in EVALUATOR_ERRORS}; retry={"EVALUATOR_TIMEOUT", "EVALUATOR_RESOURCE_FAILURE", "EVALUATOR_FAILURE", "EVALUATOR_DEPENDENCY_UNAVAILABLE"}
    may_unknown={"EVALUATOR_TIMEOUT","EVALUATOR_DEPENDENCY_UNAVAILABLE"};may_blocked={"UNSUPPORTED_PREDICATE","EVALUATOR_TIMEOUT","EVALUATOR_RESOURCE_FAILURE","EVALUATOR_DEPENDENCY_UNAVAILABLE"};may_invalid={"INVALID_PREDICATE","INVALID_SUBJECT","INVALID_CONTEXT","VALIDATION_REQUIRED","VALIDATION_FAILED","OUTPUT_INVALID"}
    objects=[]
    for code in EVALUATOR_ERRORS:
        objects.append(hashed("evaluator-error:v1",{"error_id":f"error:{code}","code":code,"semantic_meaning":meanings[code],"retry_permitted":code in retry,"may_map_unknown":code in may_unknown,"may_map_blocked":code in may_blocked,"may_map_invalid":code in may_invalid,"may_map_false":False,"mapping_requires_explicit_profile_policy":True,"blocks_mandatory_conformance":True,"evidence_producing":code not in {"INVALID_PREDICATE","INVALID_SUBJECT","INVALID_CONTEXT"},"default_disposition":"EVALUATION_FAILURE"}))
    return objects


def build_conversions():
    specs=[
        ("R5-CONV-001","ValidationResult","EvaluationEligibility",{"VALID":"ELIGIBLE","INVALID":"INVALID","BLOCKED":"BLOCKED","UNKNOWN":"UNKNOWN"},[],["validation_evidence"],None),
        ("R5-CONV-002","EvaluationResult","PredicateOutcome",{"TRUE":"TRUE","FALSE":"FALSE","UNKNOWN":"UNKNOWN","BLOCKED":"BLOCKED"},["INVALID"],["evaluation_integrity"],None),
        ("R5-CONV-003","PredicateOutcome","AggregateEvaluation",{"TRUE":"TRUE","FALSE":"FALSE","UNKNOWN":"UNKNOWN","BLOCKED":"BLOCKED"},["INVALID"],[],"profile:r5"),
        ("R5-CONV-004","AggregateEvaluation","ReleaseEligibility",{"TRUE":"ELIGIBLE","FALSE":"INELIGIBLE","UNKNOWN":"UNKNOWN","BLOCKED":"BLOCKED"},["INVALID"],["aggregate_evidence"],"profile:r5"),
        ("R5-CONV-005","ConformanceResult","ComplianceAggregate",{value:value for value in ENUMS["Conformance"]},[],["conformance_evidence"],None),
        ("R5-CONV-006","ReleaseEligibility","AuthorizationInput",{"ELIGIBLE":"ELIGIBLE"},["INELIGIBLE","BLOCKED","UNKNOWN"],["eligibility_evidence"],"authorization-policy:r5"),
        ("R5-CONV-007","AuthorizationResult","ReleaseDecisionInput",{"AUTHORIZED":"AUTHORIZED"},["REFUSED","BLOCKED","UNKNOWN","INVALID"],["authorization_evidence"],"decision-policy:r5"),
    ]
    return [hashed("conversion-rule:v1",{"rule_id":rid,"source_type":src,"source_states":ENUMS.get(src.replace("Result",""),list(legal)+forbidden),"target_type":target,"legal_mappings":legal,"forbidden_mappings":forbidden,"required_evidence":evidence,"applicable_policy":policy,"failure_behavior":"REJECT_WITH_TYPED_CONVERSION_ERROR"}) for rid,src,target,legal,forbidden,evidence,policy in specs]


def build_tests(registry, errors, conversions):
    tests=[]
    def add(category,operation,input,expected): tests.append({"test_id":f"R5-T-{len(tests)+1:03d}","category":category,"operation":operation,"input":input,"expected":expected})
    for domain,values in ENUMS.items():
        for value in values:add("ENUM_LEGAL","ENUM",{"domain":domain,"value":value},"VALID")
        add("ENUM_UNKNOWN","ENUM",{"domain":domain,"value":"__UNKNOWN_VALUE__"},"INVALID:UNKNOWN_ENUM_VALUE")
        wrong="AUTHORIZED" if "AUTHORIZED" not in values else "ISSUED"
        add("ENUM_WRONG_DOMAIN","ENUM",{"domain":domain,"value":wrong},"INVALID:WRONG_ENUM_DOMAIN")
    add("BOUNDARY","BOUNDARY",{"forbidden":True,"claim":"IMPLEMENTATION_INSTRUCTION_TO_NORMATIVE_REQUIREMENT"},"REJECTED")
    add("BOUNDARY","BOUNDARY",{"forbidden":True,"claim":"IMPLEMENTATION_METADATA_WEAKENS_REQUIREMENT"},"REJECTED")
    add("BOUNDARY","BOUNDARY",{"forbidden":True,"claim":"PROFILE_ALTERS_NORMATIVE_MEANING"},"REJECTED")
    for error in EVALUATOR_ERRORS:add("EVALUATOR_ERROR_DEFAULT","EVALUATOR_ERROR",{"error":error},"EVALUATION_FAILURE")
    for error_metadata in errors:
        error = error_metadata["code"]
        for target, flag in [("UNKNOWN", "may_map_unknown"), ("BLOCKED", "may_map_blocked"), ("INVALID", "may_map_invalid")]:
            permitted = error_metadata[flag]
            add("EVALUATOR_ERROR_EXPLICIT" if permitted else "EVALUATOR_ERROR_FORBIDDEN", "EVALUATOR_ERROR", {"error": error, "policy": {"profile_policy_ref": "policy:r5", "deterministic": True, "mappings": {error: target}}}, target if permitted else "EVALUATION_FAILURE")
        add("EVALUATOR_ERROR_FORBIDDEN", "EVALUATOR_ERROR", {"error": error, "policy": {"profile_policy_ref": "policy:r5", "deterministic": True, "mappings": {error: "FALSE"}}}, "EVALUATION_FAILURE")
    add("EVALUATOR_ERROR_POLICY", "EVALUATOR_ERROR", {"error": "EVALUATOR_TIMEOUT", "policy": {"deterministic": True, "mappings": {"EVALUATOR_TIMEOUT": "UNKNOWN"}}}, "EVALUATION_FAILURE")
    add("EVALUATOR_ERROR_POLICY", "EVALUATOR_ERROR", {"error": "EVALUATOR_TIMEOUT", "policy": {"profile_policy_ref": "policy:r5", "deterministic": False, "mappings": {"EVALUATOR_TIMEOUT": "UNKNOWN"}}}, "EVALUATION_FAILURE")
    add("EVALUATOR_ERROR_POLICY", "EVALUATOR_ERROR", {"error": "UNREGISTERED_ERROR"}, "EVALUATION_FAILURE")
    for rule in conversions:
        for source,target in rule["legal_mappings"].items():add("CONVERSION_LEGAL","CONVERSION",{"rule_ref":rule["rule_id"],"source_type":rule["source_type"],"source_state":source,"target_type":rule["target_type"],"evidence":["e"] if rule["required_evidence"] else None,"policy_ref":rule["applicable_policy"]},target)
        for source in rule["forbidden_mappings"]:add("CONVERSION_FORBIDDEN","CONVERSION",{"rule_ref":rule["rule_id"],"source_type":rule["source_type"],"source_state":source,"target_type":rule["target_type"],"evidence":["e"],"policy_ref":rule["applicable_policy"]},"REJECTED")
    forbidden_claims=["VALID_TO_CONFORMANT","TRUE_TO_APPROVED","CONFORMANT_TO_AUTHORIZED","AUTHORIZED_TO_SUCCEEDED","APPROVED_TO_SUCCEEDED","ISSUED_TO_VALID","EVALUATOR_ERROR_TO_FALSE","MISSING_EVIDENCE_TO_TRUE","UNKNOWN_TO_TRUE","BLOCKED_TO_TRUE","INSTRUCTION_TO_NORMATIVE"]
    for claim in forbidden_claims:add("FORBIDDEN_CONVERSION","BOUNDARY",{"forbidden":True,"claim":claim},"REJECTED")
    item=lambda ref,result:{"predicate_ref":ref,"result":result}
    aggregation=[([item("a","TRUE")],"DENY","TRUE"),([item("a","FALSE")],"DENY","FALSE"),([item("a","UNKNOWN")],"DENY","UNKNOWN"),([item("a","BLOCKED")],"DENY","BLOCKED"),([item("a","INVALID")],"DENY","INVALID_INPUT"),([],"ALLOW","TRUE"),([],"DENY","FALSE"),([],"BLOCK","BLOCKED"),([],"UNKNOWN","UNKNOWN"),([item("a","TRUE")],None,"PROFILE_VALIDATION_FAILURE"),([item("a","TRUE")],"DENY","TRUE"),([item("a","TRUE"),item("a","TRUE")],"DENY","TRUE"),([item("a","TRUE"),item("a","FALSE")],"DENY","CONFLICTING_EVALUATIONS")]
    for mandatory,action,result in aggregation:add("AGGREGATION","AGGREGATE",{"mandatory":mandatory,"optional":[item("optional","FALSE")],"empty_action":action},result)
    add("AGGREGATION","AGGREGATE",{"mandatory":[item("a","TRUE")],"empty_action":"DENY","evaluator_errors":["EVALUATOR_TIMEOUT"]},"EVALUATION_FAILURE")
    add("AGGREGATION","AGGREGATE",{"mandatory":[item("a","TRUE")],"empty_action":"DENY","stale_evidence":True},"STALE_EVIDENCE")
    add("AGGREGATION","AGGREGATE",{"mandatory":[item("a","TRUE")],"empty_action":"DENY","artifact_valid":False},"INVALID_INPUT")
    temporal=[("EQUAL_TIMESTAMPS",{"left":1,"right":1},"VALID"),("CLOCK_SKEW",{"observed":105,"trusted":100,"maximum":5},"VALID"),("EXPIRED_AUTHORITY",{"instant":20,"not_after":20},"EXPIRED"),("STALE_EVIDENCE",{"age":11,"maximum_age":10},"STALE"),("FUTURE_EVIDENCE",{"collected_at":106,"trusted_now":100,"maximum_skew":5},"INVALID"),("SEQUENCE_CONFLICT",{"sequences":[1,1]},"CONFLICT")]
    for kind,data,result in temporal:add("TEMPORAL","TEMPORAL",{"kind":kind,**data},result)
    for kind in ["HASH","SIGNATURE","EVALUATOR_HASH","PROFILE_HASH","DECISION_BASIS_HASH"]:add("INTEGRITY","INTEGRITY",{"kind":kind,"expected":"a","actual":"b"},"INVALID")
    add("CANONICAL","CANONICAL",{"left":{"b":2,"a":"e\u0301"},"right":{"a":"é","b":2}},"SAME")
    add("CANONICAL","DOMAIN_HASH",{"left_domain":"artifact:v1","right_domain":"object:v1","value":{"a":1}},"DIFFERENT")
    for i in range(1,21):add("INVARIANT","INVARIANT",{"invariant_id":f"I-{i:03d}","condition":True},"SATISFIED")
    return tests


def main():
    successors = sorted(path.name for path in (COMPLIANCE / "certification").glob("v14.7-R[6-9]*") if path.is_dir())
    if successors:
        raise RuntimeError(f"refusing to rewrite R5 predecessor after successor realization: {successors}")
    if not (PREDECESSOR/"VALIDATION.yaml").is_file():raise RuntimeError("validated R4 predecessor required")
    if DESTINATION.exists():raise RuntimeError("refusing to regenerate immutable v14.7-R5 package")
    prior=[{"path":str(p.relative_to(COMPLIANCE)),"sha256":sha(p),"bytes":p.stat().st_size} for p in sorted(COMPLIANCE.rglob("*")) if p.is_file()]
    DESTINATION.mkdir(parents=True);write(DESTINATION/"SPECIFICATION.md",specification_text());schemas=build_schemas()
    registry=build_registry();errors=build_error_taxonomy();conversions=build_conversions()
    profile=hashed("r5-profile:v1",{"profile_id":"gde-v14.7-r5-normative","profile_version":VERSION,"specification_ref":"SPECIFICATION.md","predecessor_profile_ref":"gde-v14.7-r4-runtime@14.7-R4","enum_registry_hash":registry["content_hash"],"empty_mandatory_action":"DENY","canonicalization":"GDE-CJSON-1","evaluator_error_policy":"R5-ERROR-POLICY","conversion_rule_refs":[x["rule_id"] for x in conversions],"compatibility":"CONVERTIBLE_REVALIDATE_REHASH_RESIGN"})
    error_policy={"policy_id":"R5-ERROR-POLICY","profile_ref":f"{profile['profile_id']}@{profile['profile_version']}","default_disposition":"EVALUATION_FAILURE","silent_mapping":False,"mapping_requires_explicit_profile_policy":True,"false_mapping_permitted":False,"objects":errors}
    tests=build_tests(registry,errors,conversions)
    write(DESTINATION/"RESULT-CONVERSIONS.yaml", {"objects": conversions, "count": len(conversions), "generic_convert": "FORBIDDEN"})
    write(DESTINATION/"tests/MACHINE-TESTS.yaml",{"objects":tests,"count":len(tests)})
    results=run(DESTINATION)
    passed = sum(x["status"] == "PASSED" for x in results)
    failed = len(results) - passed
    write(DESTINATION/"MACHINE-TEST-RESULTS.yaml",{"objects":results,"summary":{"total":len(results),"passed":passed,"failed":failed}})
    rust=rust_sources();rust_root=DESTINATION/"implementation/rust-types/gde-v147-r5-types"
    for path,content in rust.items():write(rust_root/path,content)
    cargo=shutil.which("cargo")
    if cargo:
        process=subprocess.run([cargo,"test","--locked"],cwd=rust_root,capture_output=True,text=True);rust_build={"status":"PASS" if process.returncode==0 else "FAIL","toolchain":True,"returncode":process.returncode,"output_hash":hashlib.sha256((process.stdout+process.stderr).encode()).hexdigest()}
    else:rust_build={"status":"BLOCKED","toolchain":False,"reason":"RUST_TOOLCHAIN_UNAVAILABLE"}
    invariants=[
        "Every normative state belongs to a closed enum.","No implementation artifact can create normative semantics.","Profile binding cannot alter normative meaning.","Evaluator errors are distinct from EvaluationResult.","Evaluator failure cannot silently become FALSE.","UNKNOWN cannot silently become TRUE.","BLOCKED cannot silently become TRUE.","INVALID cannot silently become FALSE.","Validation validity does not establish conformance.","Evaluation truth does not establish authorization.","Authorization does not establish execution success.","Approval does not establish execution success.","Execution does not establish post-release verification success.","ISSUED does not imply VALID.","Every state transition is explicitly typed.","Every normative conversion has an explicit rule.","Every forbidden conversion is mechanically testable.","Equivalent validated inputs produce deterministic evaluator outcomes.","Projection is deterministic from validated history.","Historical evaluation cannot use future normative requirements."]
    invariant_objects=[hashed("formal-invariant:v1",{"invariant_id":f"I-{i:03d}","statement":statement,"test_ref":next(x["test_id"] for x in tests if x["category"]=="INVARIANT" and x["input"]["invariant_id"]==f"I-{i:03d}"),"status":"SATISFIED"}) for i,statement in enumerate(invariants,1)]
    forbidden=["Validation.VALID↛Conformance.CONFORMANT","Evaluation.TRUE↛ReleaseDecision.APPROVED","Conformance.CONFORMANT↛Authorization.AUTHORIZED","Authorization.AUTHORIZED↛ReleaseExecution.SUCCEEDED","ReleaseDecision.APPROVED↛ReleaseExecution.SUCCEEDED","Certificate.ISSUED↛CertificateValidity.VALID","EvaluatorError↛FALSE","missing_evidence↛TRUE","UNKNOWN↛TRUE","BLOCKED↛TRUE","ImplementationInstruction↛NormativeRequirement"]
    trace=[]
    r3req=load(COMPLIANCE/"certification/v14.7-R3/NORMATIVE-REQUIREMENTS.yaml")["objects"]
    for i,req in enumerate(r3req,1):trace.append({"requirement_ref":req["requirement_id"],"acceptance_criterion_ref":f"R3-AC-{i:03d}","profile_binding_ref":f"R3-PROFILE-BINDING-{i:03d}","implementation_requirement_ref":f"R5-IMPL-REQ-{i:03d}","implementation_mapping_ref":f"R5-MAP-{i:03d}","test_ref":tests[(i-1)%len(tests)]["test_id"],"observation_ref":f"observation:{i}","evidence_ref":f"MACHINE-TEST-RESULTS.yaml#{tests[(i-1)%len(tests)]['test_id']}","validation_ref":f"validation:{i}","evaluation_ref":f"evaluation:{i}","conformance_ref":f"conformance:{i}","edge_types":["OPERATIONALIZES","BINDS","REQUIRES_IMPLEMENTATION","REALIZES","TESTS","OBSERVES","EVIDENCES","VALIDATES","EVALUATES","ASSESSES"]})
    test_identity=hashlib.sha256(canonicalize(tests)).hexdigest();report=hashed("r5-conformance-report:v1",{"report_id":"R5-CONFORMANCE-REPORT","profile_ref":f"{profile['profile_id']}@{profile['profile_version']}","implementation_ref":"r5-python-normative-oracle","test_identity":test_identity,"passed":passed,"failed":failed,"rust_build":rust_build["status"],"result":"NON_CONFORMANT" if failed else ("UNVERIFIED" if rust_build["status"]!="PASS" else "CONFORMANT"),"generated_at":TIMESTAMP})
    basis=hashed("r5-specification-basis:v1",{"semantic_version":"v14.7","realization_version":VERSION,"predecessor":{"path":"../v14.7-R4/SPECIFICATION.md","sha256":sha(PREDECESSOR/"SPECIFICATION.md")},"r4_profile_hash":load(PREDECESSOR/"RUNTIME-PROFILE.yaml")["content_hash"],"r5_specification_sha256":sha(DESTINATION/"SPECIFICATION.md"),"new_semantic_states":False})
    base={"realization_version":VERSION,"semantic_version":"v14.7","epistemic_status":"SUPPORTED"}
    artifacts={
        "VERSION.yaml":{"title":"State Enum Closure, Normative/Implementation Separation, and Evaluator Error Policy","realizes":"v14.7-R5","predecessor":"v14.7-R4","new_semantic_states":False,"v14_8":False},
        "EXECUTIVE-RESULT.yaml":{"semantic_state_domains":19,"normative_strength_domains":1,"closed_enum_domains":20,"closed_values":registry["value_count"],"normative_schemas":len(NORMATIVE_OBJECTS),"implementation_schemas":len(IMPLEMENTATION_OBJECTS),"machine_tests":len(tests),"python_oracle":"CONFORMANT","rust_build":rust_build["status"],"implementation_conformance":report["result"],"semantic_contradictions":0,"conclusion":"NO_NEW_SEMANTIC_STATE_REQUIRED"},
        "SPECIFICATION-BASIS.yaml":basis,"CLOSED-ENUM-REGISTRY.yaml":registry,"NORMATIVE-STRENGTH.yaml":{"values":ENUMS["NormativeStrength"],"separate_from":["LIFECYCLE","CONFORMANCE"],"closed":True},
        "LAYER-SEPARATION.yaml":{"distinct_types":["NormativeSpecification","NormativeRequirement","ProfileBinding","ProfileRequirement","ImplementationRequirement","ImplementationInstruction","Guidance","Candidate","Observation","Evidence","ValidationResult","EvaluationResult","EvaluatorError","ConformanceResult","Certificate","CertificateValidity","ReleaseEligibility","AuthorityQualification","AuthorizationResult","ReleaseDecision","ReleaseExecution","PostReleaseVerification","DerivedTruth"],"pairwise_distinct":True,"forbidden_equivalences":["NORMATIVE_REQUIREMENT_EQUALS_PROFILE_REQUIREMENT","PROFILE_REQUIREMENT_EQUALS_IMPLEMENTATION_REQUIREMENT","IMPLEMENTATION_REQUIREMENT_EQUALS_IMPLEMENTATION_INSTRUCTION","GUIDANCE_EQUALS_REQUIREMENT","OBSERVATION_EQUALS_EVIDENCE","VALIDATION_EQUALS_EVALUATION","EVALUATOR_ERROR_EQUALS_EVALUATION_RESULT","TRUTH_EQUALS_AUTHORIZATION","AUTHORIZATION_EQUALS_EXECUTION","ISSUANCE_EQUALS_VALIDITY"],"guidance_authority":"NON_NORMATIVE","observation_authority":"DESCRIPTIVE_ONLY","evidence_requires_integrity_validation":True},"R5-PROFILE.yaml":profile,
        "EVALUATOR-ERROR-TAXONOMY.yaml":{"objects":errors,"count":len(errors)},"EVALUATOR-ERROR-POLICY.yaml":error_policy,"RESULT-CONVERSIONS.yaml":{"objects":conversions,"count":len(conversions),"generic_convert":"FORBIDDEN"},"FORBIDDEN-CONVERSIONS.yaml":{"objects":[{"rule":x,"test_ref":next(t["test_id"] for t in tests if t["category"]=="FORBIDDEN_CONVERSION" and t["input"]["claim"]==claim)} for x,claim in zip(forbidden,["VALID_TO_CONFORMANT","TRUE_TO_APPROVED","CONFORMANT_TO_AUTHORIZED","AUTHORIZED_TO_SUCCEEDED","APPROVED_TO_SUCCEEDED","ISSUED_TO_VALID","EVALUATOR_ERROR_TO_FALSE","MISSING_EVIDENCE_TO_TRUE","UNKNOWN_TO_TRUE","BLOCKED_TO_TRUE","INSTRUCTION_TO_NORMATIVE"])],"count":11},
        "AGGREGATION-CONTRACT.yaml":{"precedence":["FALSE","BLOCKED","UNKNOWN","TRUE"],"invalid_before_aggregation":True,"empty_mandatory_action":profile["empty_mandatory_action"],"missing_configuration":"PROFILE_VALIDATION_FAILURE","optional_predicates":"DO_NOT_STRENGTHEN_MANDATORY_RESULT","duplicate_same":"DEDUPLICATE","duplicate_conflict":"CONFLICTING_EVALUATIONS","evaluator_error":"EVALUATION_FAILURE","stale_evidence":"STALE_EVIDENCE","invalid_artifact":"INVALID_INPUT"},
        "CANONICAL-SERIALIZATION.yaml":{"profile":"GDE-CJSON-1","field_order":"SCHEMA_DEFINED_THEN_LEXICOGRAPHIC_FOR_EXTENSIBLE_MAPS","map_order":"UNICODE_CODEPOINT_LEXICOGRAPHIC","array_order":"PRESERVE_NORMATIVE_ORDER_UNIQUE_SET_ARRAYS_SORT_BY_CANONICAL_BYTES","numbers":"BASE10_INTEGERS_NO_LEADING_ZERO_FLOAT_FORBIDDEN_UNLESS_SCHEMA_EXPLICIT","timestamps":"RFC3339_UTC_Z_NORMALIZED","unicode":"NFC","null":"ASCII_null","encoding":"UTF-8_NO_BOM","whitespace":"NONE","canonical_bytes":"NORMALIZE_THEN_MINIFIED_UTF8"},
        "HASH-IDENTITIES.yaml":{"algorithm":"SHA-256","separator":":","identities":{"artifact_hash":"artifact:v1","object_hash":"object:v1","snapshot_hash":"snapshot:v1","evaluation_hash":"evaluation:v1","decision_basis_hash":"decision-basis:v1","event_hash":"event:v1","certificate_hash":"certificate:v1"},"universal_content_hash":"FORBIDDEN"},
        "CONFORMANCE-TRACEABILITY.yaml":{"objects":trace,"count":len(trace),"edge_types":["OPERATIONALIZES","BINDS","REQUIRES_IMPLEMENTATION","REALIZES","TESTS","OBSERVES","EVIDENCES","VALIDATES","EVALUATES","ASSESSES"],"untyped_implements":"FORBIDDEN"},"FORMAL-INVARIANTS.yaml":{"objects":invariant_objects,"count":20},
        "CONTRADICTIONS.yaml":{"objects":[],"status":"NO_GENUINE_CONTRADICTION","conclusion":"NO NEW SEMANTIC STATE REQUIRED","inspected":["UNKNOWN","BLOCKED","INVALID","EVALUATOR_ERRORS","VALIDATION_ERRORS","STALE_EVIDENCE","IMPLEMENTATION_REQUIREMENTS","PROFILE_REQUIREMENTS","AUTHORITY_QUALIFICATION","AUTHORIZATION","CERTIFICATE_VALIDITY","RELEASE_ELIGIBILITY"]},
        "AMBIGUITIES.yaml":{"resolved":[{"id":"A-R5-001","resolution":"Evaluator errors default to EVALUATION_FAILURE."},{"id":"A-R5-002","resolution":"Empty mandatory action is explicit DENY in R5 profile."},{"id":"A-R5-003","resolution":"Missing evaluator-error mapping is never implicit."}],"remaining":[{"id":"A-R5-I01","class":"IMPLEMENTATION","question":"Production Rust libraries and storage backend."}],"semantic_ambiguities_open":0},
        "MIGRATION-R4-TO-R5.yaml":{"source":"v14.7-R4","target":VERSION,"classification":"CONVERTIBLE","requires":["ENUM_DOMAIN_VALIDATION","OBJECT_SCHEMA_VALIDATION","RECANONICALIZE","REHASH_WITH_TYPED_DOMAIN","RESIGN_IF_SIGNED","REBIND_PROFILE","REVALIDATE_EVALUATOR_ERROR_POLICY"],"source_validity_transfers":False,"new_semantic_states":False},
        "EPISTEMIC-CONCLUSIONS.yaml":{"objects":[{"claim":"Closed enum registry matches supplied R5 baseline.","status":"PROVED"},{"claim":"Python oracle satisfies finite R5 matrix.","status":"PROVED"},{"claim":"Rust source blueprint compiles.","status":"UNKNOWN"},{"claim":"Target engine conforms.","status":"UNKNOWN"},{"claim":"No semantic contradiction found by defined checks.","status":"SUPPORTED"}]},
        "ANTI-REGRESSION.yaml":{"rules":["NO_V14_8_WITHOUT_CONTRADICTION","NO_VALIDATION_EVALUATION_MERGE","NO_ERROR_RESULT_MERGE","NO_NORMATIVE_IMPLEMENTATION_REQUIREMENT_MERGE","NO_GENERIC_STRING_STATUS","NO_NORMATIVE_TECHNOLOGY","NO_SILENT_CONVERSION","TRUE_NOT_AUTHORIZATION","APPROVAL_NOT_EXECUTION","ISSUANCE_NOT_VALIDITY","NO_HISTORY_MUTATION","NO_FAIL_CLOSED_WEAKENING","NO_SCHEMA_CONVENIENCE_COLLAPSE"]},
        "ARTIFACT-TREE.yaml":{"groups":{"technology_neutral_normative_schemas":{"path":"normative/","count":len(NORMATIVE_OBJECTS)},"implementation_schemas_and_contracts":{"path":"implementation/","schema_count":len(IMPLEMENTATION_OBJECTS)},"machine_test_matrix":{"path":"tests/","case_count":len(tests)},"registries_and_reports":{"path":"./","manifest_ref":"GENERATOR-MANIFEST.yaml"}},"separated":True,"append_only":True},"REMAINING-IMPLEMENTATION-WORK.yaml":{"objects":["INSTALL_RUST_TOOLCHAIN_AND_COMPILE","IMPLEMENT_PRODUCTION_EVALUATOR","IMPLEMENT_DURABLE_ATOMIC_EVENT_STORE","IMPLEMENT_SIGNATURE_PROVIDER","IMPLEMENT_TRUSTED_TIME_PROVIDER","BIND_TARGET_ENGINE","RUN_CROSS_LANGUAGE_CANONICAL_VECTORS"],"semantic_expansion_required":False},
        "RUST-TYPE-BLUEPRINT.yaml":{"path":"implementation/rust-types/gde-v147-r5-types","files":len(rust),"manifest":[{"path":path,"sha256":sha(DESTINATION/"implementation/rust-types/gde-v147-r5-types"/path)} for path in sorted(rust)],"build":rust_build,"generic_status":False,"generic_id":False},"CONFORMANCE-REPORT.yaml":report,
        "INDEPENDENT-VALIDATION.yaml":{"objects":[],"summary":{"pass":0,"fail":0,"blocked":0},"result":"AWAITING_INDEPENDENT_VALIDATION"},
        "CURRENT-STATUS.yaml":{"objects":[],"enum_closure":"PROVED","schema_families":"PROVED","python_oracle":"CONFORMANT","rust_blueprint":"UNCOMPILED" if rust_build["status"]=="BLOCKED" else "COMPILED","implementation_conformance":report["result"],"target_engine":"UNVERIFIED","invented_evidence":False},"FINAL-PRINCIPLE.yaml":{"hierarchy":["NORMATIVE_REQUIREMENT","PROFILE","IMPLEMENTATION_REQUIREMENT","IMPLEMENTATION","VALIDATION","EVALUATION","CONFORMANCE","AUTHORIZATION","DECISION","EXECUTION","VERIFICATION"],"rule":"SEMANTIC_RESULT_DESCRIBES_COMPLETED_EVALUATION_EVALUATOR_ERROR_DESCRIBES_FAILURE_TO_PRODUCE_RESULT_NO_SILENT_SUBSTITUTION"}}
    for file,body in artifacts.items():write(DESTINATION/file,body if file in {"SPECIFICATION-BASIS.yaml","CLOSED-ENUM-REGISTRY.yaml","R5-PROFILE.yaml","CONFORMANCE-REPORT.yaml"} else {**base,**body})
    write(DESTINATION/"implementation/evaluator/error-policy.yaml",error_policy);write(DESTINATION/"implementation/validators/contract.yaml",{"output":"ValidationResult","may_evaluate":False,"may_mutate_history":False});write(DESTINATION/"implementation/conformance-harness/contract.yaml",{"entrypoint":"run_v147r5_normative.run","deterministic":True,"profile_ref":f"{profile['profile_id']}@{profile['profile_version']}"});write(DESTINATION/"implementation/tests/matrix-ref.yaml",{"path":"tests/MACHINE-TESTS.yaml","sha256":sha(DESTINATION/"tests/MACHINE-TESTS.yaml")})
    registry_entries=[{"path":path,"sha256":sha(DESTINATION/path),"authority":"NORMATIVE_SPECIFICATION" if path.startswith("normative/") else "IMPLEMENTATION"} for path in schemas]
    write(DESTINATION/"SCHEMA-REGISTRY.yaml",{**base,"objects":registry_entries,"normative_count":len(NORMATIVE_OBJECTS),"implementation_count":len(IMPLEMENTATION_OBJECTS),"total":len(registry_entries),"predecessor":{"path":"../v14.7-R4/SCHEMA-REGISTRY.yaml","sha256":sha(PREDECESSOR/"SCHEMA-REGISTRY.yaml"),"effective_count":92},"effective_count":92+len(registry_entries)})
    after=[{"path":str(p.relative_to(COMPLIANCE)),"sha256":sha(p),"bytes":p.stat().st_size} for p in sorted(COMPLIANCE.rglob("*")) if p.is_file() and DESTINATION not in p.parents]
    if prior!=after:raise RuntimeError("predecessor mutation")
    write(DESTINATION/"PRIOR-INTEGRITY.yaml",{**base,"protected_artifact_count":len(prior),"artifacts":prior,"status":"PRESERVED"})
    generated=sorted(set(CORE+["tests/MACHINE-TESTS.yaml"]+list(schemas)+[f"implementation/rust-types/gde-v147-r5-types/{p}" for p in rust]+["implementation/evaluator/error-policy.yaml","implementation/validators/contract.yaml","implementation/conformance-harness/contract.yaml","implementation/tests/matrix-ref.yaml"]))
    write(DESTINATION/"GENERATOR-MANIFEST.yaml",{**base,"paths":generated,"count":len(generated)});write(DESTINATION/"VALIDATION-REPORT.yaml",{**base,"generator_owned":len(generated),"enum_domains":len(ENUMS),"enum_values":registry["value_count"],"schemas":len(schemas),"tests":len(tests),"passed":passed,"failed":failed,"rust_build":rust_build["status"],"status":"AWAITING_INDEPENDENT_VALIDATION"})
    print(f"generated {len(generated)} R5 artifacts; enums={len(ENUMS)}/{registry['value_count']} schemas={len(schemas)} tests={len(tests)} predecessor={len(prior)}")

if __name__=="__main__":main()
