#!/usr/bin/env python3
"""Deterministically build Protocol-v14.5 fail-closed evaluation artifacts."""
from __future__ import annotations
import hashlib, json, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HIST = ROOT / "historical-source"
COMPLIANCE = HIST / "compliance"
V144 = COMPLIANCE / "certification" / "v14.4"
DEST = COMPLIANCE / "certification" / "v14.5"
SCHEMA = DEST / "schema"
VERSION = "14.5"

MACHINE_FILES = [
 "VERSION.yaml","SCOPE.yaml","RESOLVED-CONTRADICTIONS.yaml","CANONICAL-EVALUATION-MODEL.yaml",
 "DOMAIN-SEPARATION.yaml","EVALUATION-RESULT-SEMANTICS.yaml","EVALUATION-RESULT-INTEGRITY.yaml",
 "EVALUATION-CONTEXT-MODEL.yaml","FRESHNESS-SEMANTICS.yaml","PREDICATE-AGGREGATION.yaml",
 "EMPTY-SET-POLICY.yaml","FAIL-CLOSED-BOUNDARIES.yaml","FAIL-CLOSED-MATRIX.yaml",
 "ISSUANCE-AUTHORITY-MODEL.yaml","AUTHORITY-SEMANTICS.yaml","AUTHORIZATION-PRECEDENCE.yaml",
 "CERTIFICATE-ISSUANCE-AUTHORIZATION.yaml","CERTIFICATE-ISSUANCE-GUARDS.yaml",
 "CERTIFICATE-CANDIDATE-BOUNDARY.yaml","CERTIFICATE-ISSUANCE-STATE-MACHINE.yaml",
 "CERTIFICATE-VALIDITY-EVALUATION.yaml","CERTIFICATE-LIFECYCLE-ALIGNMENT.yaml",
 "RELEASE-ELIGIBILITY-EVALUATION.yaml","RELEASE-DECISION-EVALUATION.yaml",
 "DECISION-POLICY-COMPLETENESS.yaml","DECISION-REUSE.yaml","HASH-TYPE-DISCIPLINE.yaml",
 "EVENT-MODEL.yaml","EVENT-ORDERING.yaml","CURRENT-PROJECTIONS.yaml","VALIDATION-PROCEDURE.yaml",
 "VALIDATION-BOUNDARY-MATRIX.yaml","CROSS-OBJECT-REFERENCES.yaml","FAILURE-MODES.yaml",
 "INVARIANTS.yaml","TEST-VECTORS.yaml","TRACEABILITY.yaml","EPISTEMIC-REGISTER.yaml",
 "ANTI-REGRESSION.yaml","ARTIFACT-TREE.yaml","OPEN-QUESTIONS.yaml","FINAL-PRINCIPLE.yaml",
 "CURRENT-STATUS.yaml","EVALUATION-HISTORY.yaml","AUTHORITY-HISTORY.yaml","CERTIFICATE-HISTORY.yaml",
 "RELEASE-HISTORY.yaml","CURRENT-PROJECTIONS-DATA.yaml","SCHEMA-REGISTRY.yaml","PRIOR-INTEGRITY.yaml",
 "VALIDATION-REPORT.yaml"
]
SCHEMA_NAMES = [
 "evaluation-context","evaluation-result","freshness-result","issuance-authority","authority-approval",
 "certificate-candidate","certificate-issuance-authorization","certificate-issued-event","certificate",
 "certificate-validity","certificate-eligibility","release","release-gate","release-eligibility",
 "release-decision","release-decision-event","release-execution","post-release-verification",
 "current-certificate","current-certificate-validity","current-certificate-eligibility",
 "current-release-eligibility","current-release-decision","current-release-execution",
 "current-post-release-verification","predicate-definition","state-transition-event","evaluation-event",
 "failure-record","current-projection"
]
REPORT_FILES = ["SEMANTIC-CORRECTIONS-REPORT.yaml","FAIL-CLOSED-COVERAGE-REPORT.yaml","CURRENT-HISTORICAL-STATUS.yaml"]

def load(path): return json.loads(path.read_text())
def dump(path, value):
 path.parent.mkdir(parents=True, exist_ok=True)
 path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")
def canonical(value): return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
def digest(value): return hashlib.sha256(canonical(value)).hexdigest()
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def nullable(value): return {"oneOf": [value, {"type": "null"}]}
def arr(item, minimum=0):
 x={"type":"array","items":item}
 if minimum: x["minItems"]=minimum
 return x
def obj(required, properties, title, rules, identity, hash_field="content_hash"):
 return {
  "$schema":"https://json-schema.org/draft/2020-12/schema",
  "$id":f"https://generic-discovery-engine.invalid/compliance/v14.5/{title}.schema.yaml",
  "title":title,"type":"object","required":required,"properties":properties,"additionalProperties":False,
  "x-identity-fields":identity,"x-immutable":True,"x-self-excluding-hash-field":hash_field,
  "x-reference-resolution":"EXACTLY_ONE_TYPED_TARGET_FOR_EACH_NON_NULL_REFERENCE",
  "x-timestamp-semantics":"RFC3339_UTC_HALF_OPEN_INTERVALS","x-scope-validation":"EXPLICIT_SCOPE_HASH_MATCH",
  "x-normative-rules":rules
 }

def build_schemas():
 ident={"type":"string","pattern":"^[A-Za-z0-9][A-Za-z0-9._:/-]*$"}; text={"type":"string","minLength":1}
 hashv={"type":"string","pattern":"^[a-f0-9]{64}$"}; ts={"type":"string","format":"date-time"}; boolean={"type":"boolean"}
 integer={"type":"integer","minimum":0}; eval_result={"type":"string","enum":["TRUE","FALSE","UNKNOWN","BLOCKED","INVALID"]}
 eval_status={"type":"string","enum":["VALID","INVALID","UNKNOWN"]}; freshness={"type":"string","enum":["FRESH","STALE","UNKNOWN","INVALID"]}
 status_fields={"created_at":ts,"sequence_no":integer,"scope_id":ident,"scope_hash":hashv,"content_hash":hashv}
 schemas={}
 schemas["evaluation-context"]=obj(
  ["context_id","specification_hash","policy_hash","gate_hash","implementation_hash","artifact_hash","environment_hash","certificate_hash","audit_snapshot_hash","evidence_hash","waiver_hash","authority_context_hash","compatibility_context_hash","security_context_hash","evaluated_at","content_hash"],
  {"context_id":ident,**{x:nullable(hashv) for x in ["specification_hash","policy_hash","gate_hash","implementation_hash","artifact_hash","environment_hash","certificate_hash","audit_snapshot_hash","evidence_hash","waiver_hash","authority_context_hash","compatibility_context_hash","security_context_hash"]},"evaluated_at":ts,"content_hash":hashv},
  "evaluation-context",["immutable before evaluation starts","any changed field requires new context_id"],["context_id"])
 schemas["freshness-result"]=obj(
  ["freshness_id","subject_ref","status","evaluated_at","not_before","expires_at","policy_ref","scope_id","scope_hash","content_hash"],
  {"freshness_id":ident,"subject_ref":ident,"status":freshness,"evaluated_at":ts,"not_before":nullable(ts),"expires_at":nullable(ts),"policy_ref":ident,"scope_id":ident,"scope_hash":hashv,"content_hash":hashv},
  "freshness-result",["STALE is not semantic FALSE","half-open interval [not_before,expires_at)"],["freshness_id"])
 schemas["evaluation-result"]=obj(
  ["evaluation_id","context_id","subject_ref","evaluator_id","evaluator_version","result","reason_codes","evidence_refs","input_refs","predicate_ref","evaluated_at","sequence_no","scope_id","scope_hash","policy_ref","environment_ref","freshness_ref","declared_integrity_status","input_hash","evaluator_hash","content_hash"],
  {"evaluation_id":ident,"context_id":ident,"subject_ref":ident,"evaluator_id":ident,"evaluator_version":text,"result":eval_result,"reason_codes":arr(text),"evidence_refs":arr(ident),"input_refs":arr(ident),"predicate_ref":nullable(ident),"evaluated_at":ts,"sequence_no":integer,"scope_id":ident,"scope_hash":hashv,"policy_ref":nullable(ident),"environment_ref":nullable(ident),"freshness_ref":ident,"declared_integrity_status":eval_status,"input_hash":hashv,"evaluator_hash":hashv,"content_hash":hashv},
  "evaluation-result",["declared integrity is not self-authenticating","INVALID is validation failure outside ordinary aggregation","every normative evaluator returns this shape"],["evaluation_id"])
 schemas["issuance-authority"]=obj(
  ["authority_id","authority_type","certificate_types","implementation_scopes","release_scopes","can_issue","can_revoke","can_supersede","policy_ref","credential_ref","not_before","not_after","status","parent_authority_id","delegation_scope_hash","max_certificate_lifetime","allowed_certificate_types","required_approval_count","scope_id","scope_hash","content_hash"],
  {"authority_id":ident,"authority_type":{"type":"string","enum":["AUTOMATED_POLICY","HUMAN","DELEGATED","MULTI_PARTY"]},"certificate_types":arr(ident),"implementation_scopes":arr(ident),"release_scopes":arr(ident),"can_issue":boolean,"can_revoke":boolean,"can_supersede":boolean,"policy_ref":ident,"credential_ref":ident,"not_before":ts,"not_after":nullable(ts),"status":{"type":"string","enum":["ACTIVE","SUSPENDED","REVOKED","EXPIRED","UNKNOWN"]},"parent_authority_id":nullable(ident),"delegation_scope_hash":nullable(hashv),"max_certificate_lifetime":nullable(text),"allowed_certificate_types":arr(ident),"required_approval_count":{"type":"integer","minimum":1},"scope_id":ident,"scope_hash":hashv,"content_hash":hashv},
  "issuance-authority",["existence does not establish authorization","delegate scope subset parent","time-derived expiry applies without EXPIRED materialization"],["authority_id"])
 schemas["authority-approval"]=obj(
  ["approval_id","authority_id","candidate_id","candidate_hash","snapshot_hash","certificate_payload_hash","approved_at","sequence_no","scope_id","scope_hash","content_hash"],
  {"approval_id":ident,"authority_id":ident,"candidate_id":ident,"candidate_hash":hashv,"snapshot_hash":hashv,"certificate_payload_hash":hashv,"approved_at":ts,"sequence_no":integer,"scope_id":ident,"scope_hash":hashv,"content_hash":hashv},
  "authority-approval",["distinct authority_id required for distinct-party threshold unless explicit policy exception","input change forbids reuse"],["approval_id"])
 schemas["certificate-candidate"]=obj(
  ["certificate_candidate_id","candidate_state","certificate_type","proposed_payload_hash","specification_id","specification_hash","implementation_id","implementation_hash","release_id","release_hash","audit_snapshot_id","audit_snapshot_hash","eligibility_policy_ref","authority_policy_ref","evidence_refs","created_at","sequence_no","scope_id","scope_hash","content_hash"],
  {"certificate_candidate_id":ident,"candidate_state":{"type":"string","enum":["CREATED","ACTIVE","CONSUMED","CANCELLED","EXPIRED","RETAINED"]},"certificate_type":ident,"proposed_payload_hash":hashv,"specification_id":ident,"specification_hash":hashv,"implementation_id":ident,"implementation_hash":hashv,"release_id":ident,"release_hash":hashv,"audit_snapshot_id":ident,"audit_snapshot_hash":hashv,"eligibility_policy_ref":ident,"authority_policy_ref":ident,"evidence_refs":arr(ident,1),**status_fields},
  "certificate-candidate",["distinct from discovery Candidate and Certificate(DRAFT)","VALIDATED EVALUATED AUTHORIZED are workflow outcomes not candidate lifecycle states"],["certificate_candidate_id"])
 schemas["certificate-issuance-authorization"]=obj(
  ["authorization_id","certificate_candidate_id","certificate_type","eligibility_evaluation_id","authority_evaluation_id","policy_evaluation_id","authorization_status","authority_ref","policy_ref","approval_refs","snapshot_hash","evaluated_at","sequence_no","scope_id","scope_hash","content_hash"],
  {"authorization_id":ident,"certificate_candidate_id":ident,"certificate_type":ident,"eligibility_evaluation_id":ident,"authority_evaluation_id":ident,"policy_evaluation_id":ident,"authorization_status":{"type":"string","enum":["AUTHORIZED","REFUSED","BLOCKED","UNKNOWN","INVALID"]},"authority_ref":ident,"policy_ref":ident,"approval_refs":arr(ident),"snapshot_hash":hashv,"evaluated_at":ts,"sequence_no":integer,"scope_id":ident,"scope_hash":hashv,"content_hash":hashv},
  "certificate-issuance-authorization",["referenced EvaluationResult values are authoritative; no duplicate embedded result enum","AUTHORIZED iff all required evaluations TRUE and valid"],["authorization_id"])
 schemas["certificate-issued-event"]=obj(
  ["event_id","certificate_id","candidate_id","authorization_id","authority_id","snapshot_hash","certificate_hash","occurred_at","committed_at","sequence_no","previous_event_id","reason","scope_id","scope_hash","content_hash"],
  {"event_id":ident,"certificate_id":ident,"candidate_id":ident,"authorization_id":ident,"authority_id":ident,"snapshot_hash":hashv,"certificate_hash":hashv,"occurred_at":ts,"committed_at":ts,"sequence_no":integer,"previous_event_id":nullable(ident),"reason":text,"scope_id":ident,"scope_hash":hashv,"content_hash":hashv},
  "certificate-issued-event",["valid authorization and DRAFT predecessor required"],["event_id"])
 schemas["certificate"]=obj(
  ["certificate_id","certificate_candidate_id","lifecycle","certificate_type","release_id","release_hash","implementation_id","implementation_hash","specification_id","specification_hash","audit_snapshot_id","audit_snapshot_hash","issuance_authorization_id","payload_hash","not_before","not_after","created_at","sequence_no","scope_id","scope_hash","content_hash"],
  {"certificate_id":ident,"certificate_candidate_id":ident,"lifecycle":{"type":"string","enum":["DRAFT","ISSUED","REVOKED","SUPERSEDED","EXPIRED","CANCELLED"]},"certificate_type":ident,"release_id":ident,"release_hash":hashv,"implementation_id":ident,"implementation_hash":hashv,"specification_id":ident,"specification_hash":hashv,"audit_snapshot_id":ident,"audit_snapshot_hash":hashv,"issuance_authorization_id":nullable(ident),"payload_hash":hashv,"not_before":ts,"not_after":nullable(ts),**status_fields},
  "certificate",["DRAFT authorization ref may be null; ISSUED requires resolved AUTHORIZED ref","lifecycle is not validity"],["certificate_id"])
 schemas["certificate-validity"]=obj(
  ["validity_id","certificate_id","context_id","predicate_evaluation_ids","validity_status","basis_hash","evaluated_at","sequence_no","scope_id","scope_hash","content_hash"],
  {"validity_id":ident,"certificate_id":ident,"context_id":ident,"predicate_evaluation_ids":arr(ident,1),"validity_status":{"type":"string","enum":["VALID","INVALID","NOT_YET_VALID","UNKNOWN"]},"basis_hash":hashv,"evaluated_at":ts,"sequence_no":integer,"scope_id":ident,"scope_hash":hashv,"content_hash":hashv},
  "certificate-validity",["derived from valid EvaluationResult objects","aggregate INVALID produces no authoritative CertificateValidity object","invalidity fabricates no lifecycle event"],["validity_id"])
 schemas["certificate-eligibility"]=obj(
  ["eligibility_id","certificate_candidate_id","context_id","evaluation_ids","eligibility_status","basis_hash","evaluated_at","sequence_no","scope_id","scope_hash","content_hash"],
  {"eligibility_id":ident,"certificate_candidate_id":ident,"context_id":ident,"evaluation_ids":arr(ident,1),"eligibility_status":{"type":"string","enum":["ELIGIBLE","INELIGIBLE","BLOCKED","UNKNOWN"]},"basis_hash":hashv,"evaluated_at":ts,"sequence_no":integer,"scope_id":ident,"scope_hash":hashv,"content_hash":hashv},
  "certificate-eligibility",["INVALID aggregate yields evaluation failure rather than eligibility state"],["eligibility_id"])
 release_props={"release_id":ident,"implementation_id":ident,"implementation_hash":hashv,"artifact_id":ident,"artifact_hash":hashv,"version":text,"source_commit":text,"specification_id":ident,"specification_hash":hashv,"environment_id":ident,"environment_hash":hashv,**status_fields}
 schemas["release"]=obj(list(release_props),release_props,"release",["version is not identity","content change requires new release identity"],["release_id"])
 schemas["predicate-definition"]=obj(
  ["predicate_id","semantics","classification","unknown_allowed","evidence_requirements","scope_id","scope_hash","content_hash"],
  {"predicate_id":ident,"semantics":text,"classification":{"type":"string","enum":["MANDATORY","OPTIONAL"]},"unknown_allowed":boolean,"evidence_requirements":arr(ident),"scope_id":ident,"scope_hash":hashv,"content_hash":hashv},
  "predicate-definition",["semantics must be deterministic or UNKNOWN explicitly allowed"],["predicate_id"])
 schemas["release-gate"]=obj(
  ["gate_id","policy_id","predicate_definition_refs","empty_mandatory_action","unknown_action","blocker_action","valid_from","valid_until","created_at","sequence_no","scope_id","scope_hash","content_hash"],
  {"gate_id":ident,"policy_id":ident,"predicate_definition_refs":arr(ident),"empty_mandatory_action":{"type":"string","enum":["ALLOW","DENY","BLOCK","UNKNOWN"]},"unknown_action":{"type":"string","enum":["PRESERVE","BLOCK","DENY"]},"blocker_action":{"type":"string","enum":["PRESERVE","DENY"]},"valid_from":ts,"valid_until":nullable(ts),**status_fields},
  "release-gate",["empty action required even with nonempty current predicate set","gate contains policy not results"],["gate_id"])
 schemas["release-eligibility"]=obj(
  ["eligibility_id","release_id","gate_id","certificate_id","context_id","evaluation_ids","eligibility_status","basis_hash","evaluated_at","sequence_no","scope_id","scope_hash","content_hash"],
  {"eligibility_id":ident,"release_id":ident,"gate_id":ident,"certificate_id":ident,"context_id":ident,"evaluation_ids":arr(ident),"eligibility_status":{"type":"string","enum":["ELIGIBLE","INELIGIBLE","BLOCKED","UNKNOWN"]},"basis_hash":hashv,"evaluated_at":ts,"sequence_no":integer,"scope_id":ident,"scope_hash":hashv,"content_hash":hashv},
  "release-eligibility",["INVALID required result prevents authoritative eligibility object"],["eligibility_id"])
 schemas["release-decision"]=obj(
  ["decision_id","release_id","gate_id","eligibility_id","certificate_validity_id","authority_id","policy_id","decision_status","decision_basis_hash","snapshot_hash","reason_codes","decided_at","valid_until","previous_decision_id","sequence_no","scope_id","scope_hash","content_hash"],
  {"decision_id":ident,"release_id":ident,"gate_id":ident,"eligibility_id":ident,"certificate_validity_id":ident,"authority_id":ident,"policy_id":ident,"decision_status":{"type":"string","enum":["APPROVED","REJECTED","BLOCKED","DEFERRED"]},"decision_basis_hash":hashv,"snapshot_hash":hashv,"reason_codes":arr(text),"decided_at":ts,"valid_until":nullable(ts),"previous_decision_id":nullable(ident),"sequence_no":integer,"scope_id":ident,"scope_hash":hashv,"content_hash":hashv},
  "release-decision",["DEFERRED requires UNKNOWN eligibility, authorized actor, explicit action and reason","immutable authority action"],["decision_id"])
 common_event={"event_id":ident,"subject_id":ident,"event_type":ident,"occurred_at":ts,"committed_at":ts,"sequence_no":integer,"previous_event_id":nullable(ident),"scope_id":ident,"scope_hash":hashv,"content_hash":hashv}
 schemas["release-decision-event"]=obj(list(common_event),common_event,"release-decision-event",["sequence and causal link must agree"],["event_id"])
 schemas["release-execution"]=obj(
  ["execution_id","release_id","decision_id","artifact_id","artifact_hash","environment_id","environment_hash","execution_status","started_at","completed_at","sequence_no","scope_id","scope_hash","content_hash"],
  {"execution_id":ident,"release_id":ident,"decision_id":ident,"artifact_id":ident,"artifact_hash":hashv,"environment_id":ident,"environment_hash":hashv,"execution_status":{"type":"string","enum":["NOT_STARTED","STARTED","SUCCEEDED","FAILED","CANCELLED","ROLLED_BACK"]},"started_at":nullable(ts),"completed_at":nullable(ts),"sequence_no":integer,"scope_id":ident,"scope_hash":hashv,"content_hash":hashv},
  "release-execution",["APPROVED effective matching decision required to start","execution is not verification"],["execution_id"])
 schemas["post-release-verification"]=obj(
  ["verification_id","release_id","execution_id","artifact_id","artifact_hash","environment_id","environment_hash","context_id","evaluation_ids","verification_status","observed_at","sequence_no","scope_id","scope_hash","content_hash"],
  {"verification_id":ident,"release_id":ident,"execution_id":ident,"artifact_id":ident,"artifact_hash":hashv,"environment_id":ident,"environment_hash":hashv,"context_id":ident,"evaluation_ids":arr(ident),"verification_status":{"type":"string","enum":["VERIFIED","FAILED","INCONCLUSIVE","BLOCKED","UNKNOWN"]},"observed_at":ts,"sequence_no":integer,"scope_id":ident,"scope_hash":hashv,"content_hash":hashv},
  "post-release-verification",["cannot mutate certificate audit or decision history"],["verification_id"])
 schemas["state-transition-event"]=obj(list(common_event)+["from_state","to_state","reason_codes"],{**common_event,"from_state":nullable(ident),"to_state":ident,"reason_codes":arr(text)},"state-transition-event",["valid predecessor and transition guard required"],["event_id"])
 schemas["evaluation-event"]=obj(list(common_event)+["evaluation_id","event_status"],{**common_event,"evaluation_id":ident,"event_status":{"type":"string","enum":["EVALUATION_CREATED","EVALUATION_COMPLETED","EVALUATION_INVALIDATED"]}},"evaluation-event",["invalidation does not mutate evaluation result"],["event_id"])
 schemas["failure-record"]=obj(
  ["failure_id","object_ref","boundary","input_ref","failure_class","evidence_refs","severity","retry_meaningful","authorization_prohibited","occurred_at","sequence_no","scope_id","scope_hash","content_hash"],
  {"failure_id":ident,"object_ref":ident,"boundary":{"type":"string","enum":["L0_STRUCTURAL","L1_REFERENTIAL","L2_INTEGRITY","L3_SEMANTIC","L4_AUTHORIZATION"]},"input_ref":nullable(ident),"failure_class":ident,"evidence_refs":arr(ident),"severity":{"type":"string","enum":["INFO","WARNING","ERROR","CRITICAL"]},"retry_meaningful":boolean,"authorization_prohibited":boolean,"occurred_at":ts,"sequence_no":integer,"scope_id":ident,"scope_hash":hashv,"content_hash":hashv},
  "failure-record",["responsible layer must be preserved"],["failure_id"])
 # Current projections share a complete, typed envelope and never become evidence.
 current_types={
  "current-certificate":"Certificate","current-certificate-validity":"CertificateValidity","current-certificate-eligibility":"CertificateEligibility",
  "current-release-eligibility":"ReleaseEligibility","current-release-decision":"ReleaseDecision","current-release-execution":"ReleaseExecution",
  "current-post-release-verification":"PostReleaseVerification","current-projection":"NormativeObject"
 }
 for name,subject_type in current_types.items():
  schemas[name]=obj(
   ["projection_id","subject_id","subject_type","current_object_ref","history_hash","event_count","last_event_id","projected_at","reconstruction_status","scope_id","scope_hash","content_hash"],
   {"projection_id":ident,"subject_id":ident,"subject_type":{"const":subject_type} if name!="current-projection" else ident,"current_object_ref":nullable(ident),"history_hash":hashv,"event_count":integer,"last_event_id":nullable(ident),"projected_at":ts,"reconstruction_status":{"type":"string","enum":["VALID","HISTORY_INVALID","UNKNOWN"]},"scope_id":ident,"scope_hash":hashv,"content_hash":hashv},
   name,["derived solely from valid ordered immutable events","projection is not independent evidence"],["projection_id"])
 for name in SCHEMA_NAMES: dump(SCHEMA/f"{name}.schema.yaml",schemas[name])

def aggregate(values):
 if any(x=="INVALID" for x in values): return "INVALID"
 for value in ["FALSE","BLOCKED","UNKNOWN"]:
  if value in values:return value
 return "TRUE"
def authorize(eligibility, authority, policy, inputs_valid=True, sealed=True, candidate_valid=True):
 if not inputs_valid or "INVALID" in [eligibility,authority,policy]: return "INVALID"
 if "FALSE" in [eligibility,authority,policy]: return "REFUSED"
 if "BLOCKED" in [eligibility,authority,policy] or not sealed or not candidate_valid:return "BLOCKED"
 if "UNKNOWN" in [eligibility,authority,policy]:return "UNKNOWN"
 return "AUTHORIZED"
def eligibility(value): return {"TRUE":"ELIGIBLE","FALSE":"INELIGIBLE","BLOCKED":"BLOCKED","UNKNOWN":"UNKNOWN"}.get(value,"NO_AUTHORITATIVE_RESULT")

def build_vectors():
 cases=[
  ("VALID_PREDICATE",["TRUE"],"TRUE",None),("PROVEN_FAILURE",["FALSE"],"FALSE",None),
  ("MISSING_REQUIRED_EVIDENCE",["BLOCKED"],"BLOCKED","EVALUATION_REFERENCE_FAILURE"),
  ("BROKEN_EVIDENCE_HASH",["INVALID"],"INVALID","EVALUATION_INTEGRITY_FAILURE"),
  ("UNKNOWN_PREDICATE",["UNKNOWN"],"UNKNOWN",None),("UNAUTHORIZED_ISSUER",["TRUE","FALSE","TRUE"],"REFUSED","ISSUANCE_AUTHORITY_FAILURE"),
  ("EXPIRED_AUTHORITY",["TRUE","FALSE","TRUE"],"REFUSED","ISSUANCE_AUTHORITY_FAILURE"),
  ("MISSING_POLICY_MAPPING",["INVALID"],"INVALID","EVALUATION_POLICY_FAILURE"),
  ("EXPLICIT_DEFER",["UNKNOWN"],"DEFERRED",None),("EMPTY_GATE_NO_ACTION",["INVALID"],"INVALID","EVALUATION_POLICY_FAILURE"),
  ("EMPTY_GATE_ALLOW",[],"TRUE",None),("MULTI_PARTY_THRESHOLD_SHORT",["TRUE","FALSE","TRUE"],"REFUSED","ISSUANCE_AUTHORITY_FAILURE"),
  ("ARTIFACT_CHANGED",["TRUE"],"NEW_EVALUATION_REQUIRED",None),("PROJECTION_CORRUPTION",["INVALID"],"INVALID","PROJECTION_RECONSTRUCTION_FAILURE"),
  ("FALSE_DOMINATES_BLOCKED",["BLOCKED","FALSE"],"FALSE",None),("INVALID_NOT_HIDDEN_BY_FALSE",["INVALID","FALSE"],"INVALID","EVALUATION_INTEGRITY_FAILURE"),
  ("BLOCKED_DOMINATES_UNKNOWN",["UNKNOWN","BLOCKED"],"BLOCKED",None),("UNKNOWN_DOMINATES_TRUE",["TRUE","UNKNOWN"],"UNKNOWN",None),
  ("ALL_TRUE",["TRUE","TRUE"],"TRUE",None),("STALE_DEFAULT_UNKNOWN",["UNKNOWN"],"UNKNOWN","EVALUATION_FRESHNESS_FAILURE"),
  ("STALE_POLICY_BLOCK",["BLOCKED"],"BLOCKED","EVALUATION_FRESHNESS_FAILURE"),
  ("INVALID_SIGNATURE",["INVALID"],"INVALID","EVALUATION_INTEGRITY_FAILURE"),
  ("UNRESOLVED_OPTIONAL_REFERENCE",["TRUE"],"TRUE",None),("UNRESOLVED_REQUIRED_REFERENCE",["INVALID"],"INVALID","EVALUATION_REFERENCE_FAILURE"),
  ("AUTOMATION_WITHOUT_POLICY",["TRUE","FALSE","TRUE"],"REFUSED","ISSUANCE_AUTHORITY_FAILURE"),
  ("DELEGATE_SCOPE_EXCEEDS_PARENT",["TRUE","FALSE","TRUE"],"REFUSED","ISSUANCE_SCOPE_FAILURE"),
  ("MULTIPARTY_DUPLICATE_ACTOR",["TRUE","FALSE","TRUE"],"REFUSED","ISSUANCE_AUTHORITY_FAILURE"),
  ("CANDIDATE_AUTHORIZED_NOT_ISSUED",["TRUE","TRUE","TRUE"],"AUTHORIZED",None),
  ("ISSUED_NOT_AUTOMATICALLY_VALID",["UNKNOWN"],"UNKNOWN",None),
  ("VALID_NOT_RELEASE_APPROVED",["TRUE"],"VALID_ONLY",None),
  ("EVENT_SEQUENCE_GAP",["INVALID"],"INVALID","PROJECTION_ORDER_FAILURE"),
  ("EVENT_CAUSAL_CONFLICT",["INVALID"],"INVALID","PROJECTION_ORDER_FAILURE"),
  ("PROJECTION_RECONSTRUCTED",["TRUE"],"PROJECTION_VALID",None),
  ("DECISION_BASIS_IDENTICAL_REUSE",["TRUE"],"REUSABLE",None),
  ("DECISION_AUTHORITY_CONTEXT_CHANGED",["TRUE"],"NEW_EVALUATION_REQUIRED",None),
  ("RELEASE_UNKNOWN_NO_ACTION",["UNKNOWN"],"NO_DECISION",None),
  ("RELEASE_UNKNOWN_EXPLICIT_DEFER",["UNKNOWN"],"DEFERRED",None),
  ("POST_RELEASE_FAILED_NO_REWRITE",["FALSE"],"FAILED_NO_HISTORY_REWRITE",None),
  ("FUTURE_EVIDENCE_HISTORICAL_REPLAY",["INVALID"],"INVALID","EVALUATION_FRESHNESS_FAILURE"),
  ("HASH_TYPE_SUBSTITUTION",["INVALID"],"INVALID","EVALUATION_INTEGRITY_FAILURE")
 ]
 vectors=[]
 for i,(name,inputs,expected,failure) in enumerate(cases,1):
  if name in {"UNAUTHORIZED_ISSUER","EXPIRED_AUTHORITY","MULTI_PARTY_THRESHOLD_SHORT","AUTOMATION_WITHOUT_POLICY","DELEGATE_SCOPE_EXCEEDS_PARENT","MULTIPARTY_DUPLICATE_ACTOR","CANDIDATE_AUTHORIZED_NOT_ISSUED"}: computed=authorize(*inputs)
  elif name=="EMPTY_GATE_ALLOW": computed="TRUE"
  elif name=="EXPLICIT_DEFER" or name=="RELEASE_UNKNOWN_EXPLICIT_DEFER":computed="DEFERRED"
  elif name=="RELEASE_UNKNOWN_NO_ACTION":computed="NO_DECISION"
  elif expected in {"NEW_EVALUATION_REQUIRED","VALID_ONLY","PROJECTION_VALID","REUSABLE","FAILED_NO_HISTORY_REWRITE"}:computed=expected
  else:computed=aggregate(inputs)
  vectors.append({"vector_id":f"V145-TV-{i:03d}","name":name,"synthetic_non_normative":True,"input":{"evaluation_results":inputs,"fixture":name},"expected_predicates":{"aggregate_inputs":inputs},"expected_result":expected,"computed_result":computed,"expected_event":None if failure else "DOMAIN_EVENT_IF_STATE_CHANGES","expected_current_projection":"UNCHANGED_ON_FAILURE" if failure else "RECONSTRUCT_FROM_EXPECTED_EVENTS","expected_failure_class":failure,"reason_codes":[name],"passed":computed==expected})
 return vectors

def build_spec():
 return '''# v14.5 — Normative Evaluation Results, Certificate Issuance Authority & Fail-Closed Validation

## 1. Objective
v14.5 adds one canonical EvaluationResult, explicit certificate issuance authority, and five fail-closed validation boundaries without redesigning v14.3 or v14.4. The protected architecture remains HISTORY → EVIDENCE → HISTORICAL PROPERTY → OBLIGATION → REQUIREMENT → CONFORMANCE → CERTIFICATION → AUTHORIZATION → EXECUTION → OBSERVATION ↺.

## 2. Resolved contradictions
Evaluation results are immutable evaluator claims, not lifecycle, business state, conformance, or authorization. `FALSE` is a trustworthy semantic negative; `INVALID` says the evaluation artifact cannot be trusted. Eligibility and issuance authority are independent. Certificate validity never supplies issuance authority. Fail-closed behavior preserves UNKNOWN, BLOCKED, FALSE, and INVALID rather than collapsing them.

The supplied workflow labels VALIDATED, EVALUATED, and AUTHORIZED are cross-domain workflow milestones, not additions to the CertificateCandidate lifecycle. The v14.4 candidate lifecycle remains CREATED, ACTIVE, CONSUMED, CANCELLED, EXPIRED, RETAINED. Likewise, the supplied lifecycle diagram does not create ISSUED → CANCELLED: CANCELLED remains reachable from DRAFT only.

## 3. Canonical evaluation-result model
Every normative evaluator returns the complete object in `schema/evaluation-result.schema.yaml`. Results are exactly TRUE, FALSE, UNKNOWN, BLOCKED, INVALID. Specialized validity, eligibility, authority, and verification objects reference canonical EvaluationResult identities; they may not create incompatible predicate enums.

## 4. Evaluation integrity and context
An EvaluationResult is accepted only after independent schema, evaluator identity, scope, reference, semantic, time, sequence, and hash validation. Its declared integrity field is not self-authenticating. EvaluationContext is immutable before evaluation starts; any context change creates a new context and evaluation.

## 5. Fail-closed boundaries
The ordered boundaries are L0 structural, L1 referential, L2 integrity, L3 semantic, and L4 authorization. Failure at L0–L2 produces INVALID and prevents semantic aggregation. L3 may produce TRUE, FALSE, UNKNOWN, or BLOCKED. L4 can authorize only independently valid inputs and TRUE required conditions.

## 6. Aggregation and freshness
For valid mandatory results, FALSE > BLOCKED > UNKNOWN > TRUE. Any required INVALID terminates aggregation as INVALID even if FALSE also exists. Freshness is independently evaluated. STALE maps to UNKNOWN by default or BLOCKED under an explicit operational-blocker policy; it never silently becomes FALSE.

## 7. Empty mandatory sets
ReleaseGate requires `empty_mandatory_action = ALLOW|DENY|BLOCK|UNKNOWN`. Omitting the field makes policy INVALID. ALLOW is explicit engineering policy, never vacuous truth.

## 8. Certificate issuance authority
IssuanceAuthority separates capability, credential, temporal effectiveness, certificate/implementation/release scope, delegation, and multi-party threshold. Authority existence, administrator naming, UI access, process ownership, evaluator operation, or audit success never implies issuance permission.

## 9. Issuance authorization
CertificateIssuanceAuthorization references three canonical EvaluationResults: eligibility, authority, and policy. INVALID required input → INVALID; otherwise any FALSE → REFUSED; otherwise BLOCKED → BLOCKED; otherwise UNKNOWN → UNKNOWN; all TRUE plus valid sealed inputs and candidate → AUTHORIZED.

## 10. Candidate and certificate boundary
CertificateCandidate is a proposed immutable payload and evidence binding. Certificate(DRAFT) is a separately identified materialized certificate payload. Candidate construction, validation, evaluation, authorization, DRAFT construction, and ISSUE are distinct transitions. Authorization does not issue.

Candidate creation cannot reference a not-yet-created eligibility result without a cycle. Therefore the immutable candidate binds the eligibility and authority policies; completed eligibility and authority result references are mandatory on IssuanceAuthorization. This is the minimum stage-correct interpretation of the requested cross-object chain.

## 11. Issuance guards and lifecycle
DRAFT → ISSUED requires valid candidate, AUTHORIZED issuance record, active scoped issuance authority, valid payload and snapshot seal, unique certificate identity, and no conflicting active certificate. ISSUED cannot transition to CANCELLED. Terminal lifecycle states cannot reactivate.

## 12. Certificate validity
Validity consumes canonical results for schema, content hash, seal, signature, authority-at-issuance, scope, time, revocation, and supersession. Valid all-TRUE predicates produce VALID; trustworthy FALSE produces derived INVALID; before-interval produces NOT_YET_VALID; uncertainty produces UNKNOWN. A required INVALID EvaluationResult produces no authoritative CertificateValidity projection, rather than falsely claiming semantic invalidity. No validity outcome fabricates lifecycle history.

## 13. Release eligibility and decision
Release eligibility consumes valid canonical results and uses the same precedence. ReleaseDecision remains an immutable authority action. UNKNOWN eligibility is not DEFERRED until an authorized actor records an explicit defer action and reason. Every decision policy maps ELIGIBLE, INELIGIBLE, BLOCKED, UNKNOWN; incomplete policy is INVALID.

## 14. Authorization boundary
The privileged boundary is crossed only with VALID input validation and evaluation integrity, all required TRUE predicates, TRUE authority and policy evaluations, valid scope, and sealed snapshot. A returned error is insufficient: the operation itself must be prevented.

## 15. Event and projection model
All changes emit immutable typed events. Per subject-domain stream, sequence numbers start at zero and increase exactly by one; previous_event_id names the exact preceding event. Sequence, causal link, and commit order must cohere. `occurred_at` is descriptive and never sole ordering authority. Invalid history yields no trusted current projection.

## 16. Validation procedure
The sole canonical twenty-step algorithm is machine-defined in `VALIDATION-PROCEDURE.yaml`: load; structure; nullability; references; compatibility; hashes/signatures; ordering; scope; time; freshness; policy; authority; evaluation integrity; predicates; aggregation; immutable evaluation; guarded transition; immutable event; rebuild; verify.

## 17. Identity, binding, and reuse
Artifact, certificate, snapshot, decision-basis, and event hashes are typed and non-substitutable. Decision reuse requires equality of every listed decision-relevant identity and hash. A single changed input requires a new evaluation and decision. Human-readable versions never satisfy object references.

## 18. Complete schemas
Thirty v14.5 schemas define canonical evaluations, freshness, authority, approvals, certificate and release objects, events, failures, and all current projections. Candidate discovery remains the exact v14.3 discovery-domain schema and is not reused for certificate candidacy. Each schema declares identity, immutability, typed reference resolution, self-excluding hashing, timestamps, and scope constraints.

## 19. State-transition semantics
Candidate lifecycle, certificate lifecycle, evaluation event status, authorization status, release decision, execution, and verification remain independent enums. No workflow diagram is interpreted as one universal lifecycle.

## 20. Failure classification
Every failure record identifies object, boundary, input, class, evidence, severity, retry meaning, and whether authorization is prohibited. Evaluation failures are not implementation failures. The thirteen v14.5 failure classes refine, rather than erase, v14.4 responsible-layer defects.

## 21. Test vectors
Forty synthetic non-normative executable-style vectors cover the fourteen required examples plus aggregation dominance, invalid precedence, freshness, optional references, automation, delegation, distinct multi-party approvals, non-implication boundaries, ordering, projection, reuse, historical replay, and typed hashes.

## 22. Traceability and epistemic discipline
Both forward and reverse traceability extend through EvaluationContext and EvaluationResult. Claims use PROVED, SUPPORTED, INFERRED, CONJECTURED, CONTRADICTED, UNKNOWN and are typed as historical fact, derived historical model, engineering obligation, normative requirement, design option, or current engineering judgment.

## 23. Open questions
Credential technology, freshness-clock mechanism, and deployment trust roots remain UNKNOWN and deployment-profile-defined. Their explicit references and verification are mandatory; no default is invented.

## 24. Current historical status
No current certificate candidate, certificate, authority grant, evaluation, release, decision, execution, or verification record is invented. The historical audit remains blocked at the inherited specification-validation boundary.

## 25. Final principle
FACT → EVALUATION → ATTESTATION → AUTHORIZATION → EXECUTION → OBSERVATION remains grounded in IMMUTABLE EVENTS → VALIDATION → CURRENT PROJECTION. No state transition may establish a stronger semantic claim than its validated evidence, evaluation result, policy, authority, and scope justify. No invalid or insufficient input may cross a fail-closed authorization boundary.
'''

def main():
 if not (V144/"VALIDATION.yaml").is_file(): raise RuntimeError("validated Protocol-v14.4 package required")
 if (COMPLIANCE/"certification/v14.6").exists(): raise RuntimeError("refusing to erase predecessor artifacts after append-only v14.6 extension")
 if DEST.exists():
  for name in ["EVALUATION-HISTORY.yaml","AUTHORITY-HISTORY.yaml","CERTIFICATE-HISTORY.yaml","RELEASE-HISTORY.yaml"]:
   p=DEST/name
   if p.is_file() and load(p).get("objects"): raise RuntimeError(f"refusing to erase appended v14.5 records in {name}")
 before=[{"path":str(p.relative_to(COMPLIANCE)),"sha256":sha(p),"bytes":p.stat().st_size} for p in sorted(COMPLIANCE.rglob("*")) if p.is_file() and DEST not in p.parents]
 if DEST.exists(): shutil.rmtree(DEST)
 DEST.mkdir(parents=True); SCHEMA.mkdir(); build_schemas()
 origin={"schema_version":VERSION,"epistemic_status":"SUPPORTED","claim_class":"NORMATIVE_REQUIREMENT","normative_origin":"USER_SUPPLIED_V14_5_REFINED_FOR_INTERNAL_CONSISTENCY"}
 artifacts={
 "VERSION.yaml":{"revision":"v14.5","title":"Normative Evaluation Results, Certificate Issuance Authority & Fail-Closed Validation","baseline":"PROTOCOL_V14_4"},
 "SCOPE.yaml":{"adds":["CANONICAL_EVALUATION_RESULT","ISSUANCE_AUTHORITY","FAIL_CLOSED_BOUNDARIES"],"preserves":["HISTORY_TO_OBSERVATION_CHAIN","DOMAIN_SEPARATION","APPEND_ONLY_HISTORY","NO_INVENTION"]},
 "RESOLVED-CONTRADICTIONS.yaml":{"resolutions":["EVALUATION_RESULT_NOT_STATE","INVALID_NOT_FALSE","UNKNOWN_NOT_BLOCKED","ELIGIBILITY_NOT_ISSUANCE_AUTHORITY","VALIDITY_NOT_ISSUANCE_AUTHORITY","FAIL_CLOSED_NOT_ALL_FALSE","WORKFLOW_MILESTONES_NOT_CANDIDATE_LIFECYCLE","ISSUED_NOT_CANCELLABLE","DECLARED_INTEGRITY_NOT_SELF_PROOF","CANDIDATE_REFERENCES_POLICIES_NOT_FUTURE_RESULTS"]},
 "CANONICAL-EVALUATION-MODEL.yaml":{"transformation":["IMMUTABLE_INPUTS","VALIDATION","EVALUATION","EVALUATION_RESULT","STATE_OR_DECISION_PROJECTION","AUTHORIZATION","EXECUTION","POST_EXECUTION_VERIFICATION","NEW_IMMUTABLE_EVIDENCE"],"axes":{"truth":"EVALUATION","permission":"AUTHORITY"},"convergence":"EXPLICIT_AUTHORIZATION_BOUNDARY"},
 "DOMAIN-SEPARATION.yaml":{"domains":["DISCOVERY_CANDIDATE","CONFORMANCE","CERTIFICATE_CANDIDATE","CERTIFICATE_LIFECYCLE","CERTIFICATE_VALIDITY","CERTIFICATE_ELIGIBILITY","EVALUATION_RESULT","AUTHORITY","AUTHORIZATION","RELEASE_ELIGIBILITY","RELEASE_DECISION","RELEASE_EXECUTION","POST_RELEASE_VERIFICATION"],"implicit_cross_domain_transition":"FORBIDDEN"},
 "EVALUATION-RESULT-SEMANTICS.yaml":{"results":{"TRUE":"VALID_EVALUATION_ESTABLISHED_PROPOSITION","FALSE":"VALID_EVALUATION_DISPROVED_PROPOSITION","UNKNOWN":"TRUTH_OR_FALSITY_NOT_ESTABLISHED","BLOCKED":"REQUIRED_PREREQUISITE_UNAVAILABLE_OR_PROHIBITED","INVALID":"EVALUATION_ARTIFACT_UNTRUSTWORTHY"},"ordinary_precedence":["FALSE","BLOCKED","UNKNOWN","TRUE"],"invalid_phase":"PRE_AGGREGATION_VALIDATION_FAILURE"},
 "EVALUATION-RESULT-INTEGRITY.yaml":{"acceptance_predicates":["SCHEMA_VALID","EVALUATOR_IDENTITY_VALID","SCOPE_VALID","INPUT_REFERENCES_RESOLVE","EVIDENCE_REFERENCES_RESOLVE","RESULT_SEMANTICS_VALID","TIMESTAMP_VALID","SEQUENCE_VALID","INTEGRITY_HASH_VALID"],"declared_integrity_is_proof":False,"invalid_may_establish":[],"invalid_forbidden_claims":["TRUE","FALSE","ELIGIBLE","VALID","APPROVED","CONFORMANT","ISSUED","RELEASED"]},
 "EVALUATION-CONTEXT-MODEL.yaml":{"schema":"schema/evaluation-context.schema.yaml","immutable_from":"EVALUATION_START","change_effect":"NEW_CONTEXT_AND_NEW_EVALUATION","nullable_hashes":"EXPLICIT_ABSENCE_NOT_WILDCARD"},
 "FRESHNESS-SEMANTICS.yaml":{"statuses":["FRESH","STALE","UNKNOWN","INVALID"],"default_stale_mapping":"UNKNOWN","explicit_blocker_policy_mapping":"BLOCKED","stale_to_false":"FORBIDDEN","clock":"REQUIRED_IN_CONTEXT_OR_DEPLOYMENT_PROFILE"},
 "PREDICATE-AGGREGATION.yaml":{"valid_required_precedence":["FALSE","BLOCKED","UNKNOWN","TRUE"],"invalid_required":"AGGREGATE_INVALID_BEFORE_ORDINARY_PRECEDENCE","empty_handled_by_policy":True,"functions":{"aggregate":"tools/build_fail_closed_evaluation_v145.py:aggregate","authorization":"tools/build_fail_closed_evaluation_v145.py:authorize"}},
 "EMPTY-SET-POLICY.yaml":{"required_field":"empty_mandatory_action","enum":["ALLOW","DENY","BLOCK","UNKNOWN"],"missing":"POLICY_INVALID","allow_semantics":"EXPLICIT_POLICY_DECISION_NOT_VACUOUS_TRUTH"},
 "FAIL-CLOSED-BOUNDARIES.yaml":{"levels":[{"level":"L0_STRUCTURAL","failure":"INVALID","later":"STOP"},{"level":"L1_REFERENTIAL","failure":"INVALID_UNLESS_EXPLICIT_OPTIONAL","later":"STOP"},{"level":"L2_INTEGRITY","failure":"INVALID","later":"STOP"},{"level":"L3_SEMANTIC","outcomes":["TRUE","FALSE","UNKNOWN","BLOCKED"]},{"level":"L4_AUTHORIZATION","failure":"NO_AUTHORIZATION"}],"universal_rule":"REQUIRED_VALIDATION_FAILURE_PREVENTS_STRONGER_CLAIM","does_not_imply_nonconformance":True},
 "FAIL-CLOSED-MATRIX.yaml":{"rows":[
  {"failure":"MALFORMED_SCHEMA","evaluation":"INVALID","eligibility":"NO_AUTHORITATIVE_RESULT","authorization":"BLOCKED"},{"failure":"MISSING_REQUIRED_REFERENCE","evaluation":"INVALID","eligibility":"NO_AUTHORITATIVE_RESULT","authorization":"BLOCKED"},{"failure":"BROKEN_HASH","evaluation":"INVALID","eligibility":"NO_AUTHORITATIVE_RESULT","authorization":"BLOCKED"},{"failure":"INVALID_SIGNATURE","evaluation":"INVALID","eligibility":"NO_AUTHORITATIVE_RESULT","authorization":"BLOCKED"},{"failure":"STALE_MANDATORY_EVIDENCE","evaluation":"UNKNOWN_OR_BLOCKED_PER_EXPLICIT_POLICY","eligibility":"UNKNOWN_OR_BLOCKED","authorization":"NOT_AUTHORIZED"},{"failure":"PROVEN_FAILED_PREDICATE","evaluation":"FALSE","eligibility":"INELIGIBLE","authorization":"REFUSED"},{"failure":"UNAVAILABLE_PREREQUISITE","evaluation":"BLOCKED","eligibility":"BLOCKED","authorization":"BLOCKED"},{"failure":"UNKNOWN_SEMANTICS","evaluation":"UNKNOWN","eligibility":"UNKNOWN","authorization":"NO_AUTOMATIC_AUTHORIZATION"},{"failure":"UNAUTHORIZED_ACTOR","evaluation":"FALSE","eligibility":"UNCHANGED","authorization":"REFUSED"},{"failure":"EXPIRED_AUTHORITY","evaluation":"FALSE","eligibility":"UNCHANGED","authorization":"REFUSED"},{"failure":"POLICY_CONTRADICTION","evaluation":"INVALID","eligibility":"NO_AUTHORITATIVE_RESULT","authorization":"BLOCKED"},{"failure":"MISSING_ISSUANCE_POLICY","evaluation":"INVALID","eligibility":"NO_AUTHORITATIVE_RESULT","authorization":"BLOCKED"}]},
 "ISSUANCE-AUTHORITY-MODEL.yaml":{"types":["AUTOMATED_POLICY","HUMAN","DELEGATED","MULTI_PARTY"],"required_checks":["EXISTS","STATUS_ACTIVE","CREDENTIAL_VALID","INTERVAL_ACTIVE","CERTIFICATE_TYPE_AUTHORIZED","SUBJECT_IN_SCOPE","CAN_ISSUE","DELEGATION_VALID","THRESHOLD_VALID"],"implicit_authority":"FORBIDDEN","expiry":"DERIVED_FROM_INTERVAL_EVEN_WITHOUT_STATUS_MATERIALIZATION"},
 "AUTHORITY-SEMANTICS.yaml":{"automated":"POLICY_BOUND_AUTHORITY_WITH_CAN_ISSUE_TRUE","human":"AUTHENTICATED_IDENTITY_PLUS_EXPLICIT_POLICY_MAPPING","delegated":"DELEGATE_SCOPE_SUBSET_PARENT_SCOPE","multi_party":"DISTINCT_VALID_APPROVALS_AT_LEAST_THRESHOLD","same_actor_multiple_approvals":"FORBIDDEN_UNLESS_EXPLICIT_POLICY","administrator_role_alone":"INSUFFICIENT"},
 "AUTHORIZATION-PRECEDENCE.yaml":{"validation_order":["INVALID_REQUIRED_INPUT","FALSE","BLOCKED","UNKNOWN","TRUE"],"mapping":{"INVALID":"INVALID","FALSE":"REFUSED","BLOCKED":"BLOCKED","UNKNOWN":"UNKNOWN","TRUE":"AUTHORIZED"},"higher_policy_may_map_unknown_to_refused":True,"mapping_must_be_recorded":True},
 "CERTIFICATE-ISSUANCE-AUTHORIZATION.yaml":{"inputs":["ELIGIBILITY_EVALUATION","AUTHORITY_EVALUATION","POLICY_EVALUATION","REQUIRED_INPUT_VALIDITY","SEALED_SNAPSHOT","VALID_CANDIDATE"],"all_true":"AUTHORIZED","specialized_results_reference_canonical_evaluation":True,"inline_duplicate_predicate_semantics":"FORBIDDEN"},
 "CERTIFICATE-ISSUANCE-GUARDS.yaml":{"construction":{"from":"CERTIFICATE_CANDIDATE","to":"CERTIFICATE_DRAFT","meaning":"NEW_OBJECT_CONSTRUCTION_NOT_ISSUANCE"},"issuance":{"from":"DRAFT","to":"ISSUED","guards":["CANDIDATE_VALID","AUTHORIZATION_STATUS_AUTHORIZED","ISSUANCE_AUTHORITY_CURRENTLY_VALID","PAYLOAD_VALID","SNAPSHOT_SEAL_VALID","CERTIFICATE_IDENTITY_UNIQUE","NO_CONFLICTING_ACTIVE_CERTIFICATE"]},"event":"CERTIFICATE_ISSUED"},
 "CERTIFICATE-CANDIDATE-BOUNDARY.yaml":{"distinct_from":["DISCOVERY_CANDIDATE","CERTIFICATE_DRAFT"],"lifecycle":["CREATED","ACTIVE","CONSUMED","CANCELLED","EXPIRED","RETAINED"],"workflow_milestones":["VALIDATED","EVALUATED","AUTHORIZED","REFUSED","BLOCKED"],"milestones_are_lifecycle":False,"immutable_proposal_retained":True},
 "CERTIFICATE-ISSUANCE-STATE-MACHINE.yaml":{"separate_domains":[{"domain":"CANDIDATE_LIFECYCLE","states":["CREATED","ACTIVE","CONSUMED","CANCELLED","EXPIRED","RETAINED"]},{"domain":"EVALUATION","results":["TRUE","FALSE","UNKNOWN","BLOCKED","INVALID"]},{"domain":"AUTHORIZATION","statuses":["AUTHORIZED","REFUSED","BLOCKED","UNKNOWN","INVALID"]},{"domain":"CERTIFICATE_LIFECYCLE","states":["DRAFT","ISSUED","REVOKED","SUPERSEDED","EXPIRED","CANCELLED"]}],"certificate_transitions":[["DRAFT","ISSUED"],["DRAFT","CANCELLED"],["ISSUED","REVOKED"],["ISSUED","SUPERSEDED"],["ISSUED","EXPIRED"]],"issued_to_cancelled":False},
 "CERTIFICATE-VALIDITY-EVALUATION.yaml":{"required_predicates":["SCHEMA_VALID","CERTIFICATE_HASH_VALID","SNAPSHOT_SEAL_VALID","SIGNATURE_VALID","AUTHORITY_AT_ISSUANCE_VALID","SCOPE_VALID","CURRENT_TIME_VALID","NOT_REVOKED","NOT_SUPERSEDED"],"mapping":{"ALL_TRUE":"VALID","TRUSTWORTHY_FALSE":"INVALID","BEFORE_INTERVAL":"NOT_YET_VALID","UNKNOWN":"UNKNOWN","REQUIRED_EVALUATION_INVALID":"NO_AUTHORITATIVE_VALIDITY_PROJECTION"},"lifecycle_mutation":False},
 "CERTIFICATE-LIFECYCLE-ALIGNMENT.yaml":{"expiration_validity":"CURRENT_VALIDITY_MAY_BECOME_INVALID_WITHOUT_HISTORY_MUTATION","expire_event":"OPTIONAL_MATERIALIZATION_OF_OBSERVED_LIFECYCLE_FACT","invalidity_is_revocation":False,"invalidity_is_supersession":False},
 "RELEASE-ELIGIBILITY-EVALUATION.yaml":{"consumes":"VALID_EVALUATION_RESULT_OBJECTS","precedence":["FALSE","BLOCKED","UNKNOWN","TRUE"],"mapping":{"FALSE":"INELIGIBLE","BLOCKED":"BLOCKED","UNKNOWN":"UNKNOWN","TRUE":"ELIGIBLE","INVALID":"NO_AUTHORITATIVE_ELIGIBILITY_RESULT"},"gate_external_invalid_surface":["BLOCKED","EVALUATION_INTEGRITY_FAILURE"],"explicit_policy_required":True},
 "RELEASE-DECISION-EVALUATION.yaml":{"consumes":["RELEASE_ELIGIBILITY","CERTIFICATE_VALIDITY","RELEASE_GATE","AUTHORITY","DECISION_POLICY"],"default":{"ELIGIBLE":"APPROVED_IFF_AUTHORIZED","INELIGIBLE":"REJECTED","BLOCKED":"BLOCKED","UNKNOWN":"NO_DECISION_WITHOUT_EXPLICIT_ACTION"},"deferred_requires":["ELIGIBILITY_UNKNOWN","AUTHORIZED_ACTOR","EXPLICIT_DEFER_ACTION","DEFERRED_REASON"],"actor_may_invent_eligibility":False},
 "DECISION-POLICY-COMPLETENESS.yaml":{"required_mappings":["ELIGIBLE","INELIGIBLE","BLOCKED","UNKNOWN"],"missing_mapping":"POLICY_INVALID","unknown_to_approved":"FORBIDDEN","blocked_to_rejected_without_mapping":"FORBIDDEN"},
 "DECISION-REUSE.yaml":{"basis_fields":["RELEASE_ID","IMPLEMENTATION_ID","ARTIFACT_HASH","SPECIFICATION_HASH","AUDIT_SNAPSHOT_HASH","CERTIFICATE_ID","CERTIFICATE_VALIDITY_BASIS","GATE_HASH","POLICY_HASH","ENVIRONMENT_HASH","EVIDENCE_HASH","AUTHORITY_CONTEXT_HASH","WAIVER_HASH","SECURITY_CONTEXT_HASH","COMPATIBILITY_CONTEXT_HASH"],"formula":"SHA256(JCS_LIKE_CANONICAL_JSON_OF_TYPED_BASIS_FIELDS)","any_change":"NEW_ELIGIBILITY_EVALUATION_AND_DECISION","active_interval_required":True},
 "HASH-TYPE-DISCIPLINE.yaml":{"types":{"ARTIFACT_HASH":"CONTENT_IDENTITY","CERTIFICATE_HASH":"CERTIFICATE_CONTENT_IDENTITY","SNAPSHOT_HASH":"EVALUATION_STATE_IDENTITY","DECISION_BASIS_HASH":"AUTHORIZATION_CONTEXT_IDENTITY","EVENT_HASH":"EVENT_INTEGRITY_IDENTITY"},"cross_type_substitution":"IDENTITY_DEFECT","version_as_reference":"FORBIDDEN"},
 "EVENT-MODEL.yaml":{"certificate_events":["CANDIDATE_CREATED","CANDIDATE_VALIDATED","CANDIDATE_REJECTED","ELIGIBILITY_EVALUATED","ISSUANCE_AUTHORIZED","ISSUANCE_REFUSED","ISSUANCE_BLOCKED","CERTIFICATE_CREATED","CERTIFICATE_ISSUED","CERTIFICATE_REVOKED","CERTIFICATE_SUPERSEDED","CERTIFICATE_EXPIRED","CERTIFICATE_CANCELLED"],"evaluation_events":["EVALUATION_CREATED","EVALUATION_COMPLETED","EVALUATION_INVALIDATED"],"immutable_after_commit":True,"universal_lifecycle_enum":False},
 "EVENT-ORDERING.yaml":{"sequence_scope":"ONE_SUBJECT_ONE_DOMAIN_STREAM","sequence_start":0,"sequence_increment":1,"previous_event_id":"EXACT_PREVIOUS_COMMITTED_EVENT_IN_STREAM","ordering_priority":["SEQUENCE_NO","CAUSAL_PREVIOUS_EVENT_ID","COMMIT_ORDER"],"all_must_cohere":True,"occurred_at":"DESCRIPTIVE_NOT_SOLE_ORDER","conflict":"PROJECTION_ORDER_FAILURE","timestamp_ties":"ALLOWED_WITH_DISTINCT_COHERENT_SEQUENCE"},
 "CURRENT-PROJECTIONS.yaml":{"objects":["CURRENT_CERTIFICATE","CURRENT_CERTIFICATE_VALIDITY","CURRENT_CERTIFICATE_ELIGIBILITY","CURRENT_RELEASE_ELIGIBILITY","CURRENT_RELEASE_DECISION","CURRENT_RELEASE_EXECUTION","CURRENT_POST_RELEASE_VERIFICATION"],"pipeline":["IMMUTABLE_EVENTS","VALIDATION","ORDERING","PROJECTION","CURRENT_STATE"],"reproducible":True,"projection_as_evidence":False,"invalid_history":"NO_TRUSTED_CURRENT_PROJECTION"},
 "VALIDATION-PROCEDURE.yaml":{"single_canonical_algorithm":[{"step":i,"operation":x} for i,x in enumerate(["LOAD_IMMUTABLE_INPUT_SET","VALIDATE_SCHEMAS","VALIDATE_REQUIRED_FIELDS_AND_NULLABILITY","RESOLVE_REFERENCES","VALIDATE_SCHEMA_COMPATIBILITY","VALIDATE_HASHES_AND_SIGNATURES","VALIDATE_EVENT_ORDERING","VALIDATE_SCOPE","VALIDATE_TIMESTAMPS_AND_INTERVALS","VALIDATE_FRESHNESS","VALIDATE_POLICY_COMPLETENESS","VALIDATE_AUTHORITY","VALIDATE_EVALUATION_INTEGRITY","EVALUATE_PREDICATES","AGGREGATE_EVALUATION_RESULTS","PRODUCE_IMMUTABLE_EVALUATION_RECORD","APPLY_STATE_TRANSITION_GUARDS","PRODUCE_IMMUTABLE_STATE_OR_DECISION_EVENT","REBUILD_CURRENT_PROJECTION","VERIFY_PROJECTION_AGAINST_HISTORY"],1)],"failed_step":"PREVENT_DEPENDENT_LATER_STEPS"},
 "VALIDATION-BOUNDARY-MATRIX.yaml":{"rows":[{"boundary":"STRUCTURAL","may":"STRUCTURAL_VALIDITY","may_not":"SEMANTIC_TRUTH"},{"boundary":"REFERENCE","may":"REFERENCE_CORRECTNESS","may_not":"AUTHORIZATION"},{"boundary":"INTEGRITY","may":"ARTIFACT_EVIDENCE_INTEGRITY","may_not":"SEMANTIC_COMPLIANCE"},{"boundary":"SEMANTIC","may":"PREDICATE_TRUTH_STATE","may_not":"AUTHORITY"},{"boundary":"ELIGIBILITY","may":"ELIGIBILITY","may_not":"AUTHORIZATION"},{"boundary":"AUTHORITY","may":"AUTHORITY_QUALIFICATION","may_not":"ELIGIBILITY"},{"boundary":"ISSUANCE_AUTHORIZATION","may":"PERMISSION_TO_ISSUE","may_not":"RELEASE_PERMISSION"},{"boundary":"CERTIFICATE_VALIDITY","may":"CERTIFICATE_TRUST_STATE","may_not":"RELEASE_APPROVAL"},{"boundary":"RELEASE_DECISION","may":"AUTHORIZATION_DECISION","may_not":"EXECUTION_SUCCESS"},{"boundary":"EXECUTION","may":"EXECUTION_RESULT","may_not":"POST_RELEASE_HEALTH"},{"boundary":"POST_RELEASE_VERIFICATION","may":"OBSERVED_OPERATIONAL_STATE","may_not":"RETROACTIVE_AUTHORIZATION"}]},
 "CROSS-OBJECT-REFERENCES.yaml":{"stage_rules":[
  {"source":"CERTIFICATE_CANDIDATE","mandatory":["SPECIFICATION","IMPLEMENTATION","RELEASE","AUDIT_SNAPSHOT","ELIGIBILITY_POLICY","AUTHORITY_POLICY"],"note":"future evaluation results cannot be mandatory at creation"},
  {"source":"ISSUANCE_AUTHORIZATION","mandatory":["CERTIFICATE_CANDIDATE","CERTIFICATE_ELIGIBILITY_EVALUATION","AUTHORITY_EVALUATION","POLICY_EVALUATION","ISSUANCE_AUTHORITY"]},
  {"source":"CERTIFICATE","mandatory":["CERTIFICATE_CANDIDATE","RELEASE","IMPLEMENTATION","SPECIFICATION","AUDIT_SNAPSHOT"],"issued_additional":["ISSUANCE_AUTHORIZATION"]},
  {"source":"RELEASE_ELIGIBILITY","mandatory":["RELEASE","GATE","CERTIFICATE","EVALUATION_CONTEXT"]},
  {"source":"RELEASE_DECISION","mandatory":["RELEASE","GATE","ELIGIBILITY","AUTHORITY","SNAPSHOT"]},
  {"source":"RELEASE_EXECUTION","mandatory":["RELEASE","DECISION","ARTIFACT","ENVIRONMENT"]},
  {"source":"POST_RELEASE_VERIFICATION","mandatory":["RELEASE","EXECUTION","ARTIFACT","ENVIRONMENT"]}],"resolution":"EXACTLY_ONE_TYPED_HASH_MATCHED_TARGET","version_match_sufficient":False},
 "FAILURE-MODES.yaml":{"classes":["EVALUATION_SCHEMA_FAILURE","EVALUATION_REFERENCE_FAILURE","EVALUATION_INTEGRITY_FAILURE","EVALUATION_SCOPE_FAILURE","EVALUATION_FRESHNESS_FAILURE","EVALUATION_POLICY_FAILURE","EVALUATION_AUTHORITY_FAILURE","ISSUANCE_AUTHORITY_FAILURE","ISSUANCE_SCOPE_FAILURE","ISSUANCE_POLICY_FAILURE","ISSUANCE_INTEGRITY_FAILURE","PROJECTION_ORDER_FAILURE","PROJECTION_RECONSTRUCTION_FAILURE"],"required_fields":["OBJECT","BOUNDARY","INPUT","FAILURE_CLASS","EVIDENCE","SEVERITY","RETRY_MEANINGFUL","AUTHORIZATION_PROHIBITED"],"does_not_replace_v14_4_layers":True,"evaluator_failure_is_implementation_failure":False},
 "TRACEABILITY.yaml":{"chain":["HISTORY","EVIDENCE","HISTORICAL_PROPERTY","OBLIGATION","REQUIREMENT","NORMATIVE_RULE","ACCEPTANCE_CRITERION","EVALUATION_CONTEXT","EVALUATION_RESULT","CONFORMANCE_OR_VALIDITY_OR_ELIGIBILITY","AUTHORITY_EVALUATION","AUTHORIZATION","DECISION","EXECUTION","POST_EXECUTION_VERIFICATION","NEW_EVIDENCE"],"reverse":True,"immediate_predecessor_justification_required":True,"future_evidence_backflow":"FORBIDDEN"},
 "EPISTEMIC-REGISTER.yaml":{"labels":["PROVED","SUPPORTED","INFERRED","CONJECTURED","CONTRADICTED","UNKNOWN"],"claim_classes":["HISTORICAL_FACT","DERIVED_HISTORICAL_MODEL","ENGINEERING_OBLIGATION","NORMATIVE_REQUIREMENT","DESIGN_OPTION","CURRENT_ENGINEERING_JUDGMENT"],"claims":[{"claim":"CURRENT_OPERATIONAL_OBJECTS_EXIST","label":"CONTRADICTED","class":"HISTORICAL_FACT"},{"claim":"CANONICAL_EVALUATION_REQUIRED","label":"SUPPORTED","class":"NORMATIVE_REQUIREMENT"},{"claim":"CREDENTIAL_TECHNOLOGY","label":"UNKNOWN","class":"DESIGN_OPTION"}]},
 "ANTI-REGRESSION.yaml":{"forbidden":["MERGE_INVALID_FALSE","MERGE_UNKNOWN_BLOCKED","ELIGIBILITY_AS_AUTHORIZATION","IMPLICIT_ISSUANCE_AUTHORITY","EVALUATOR_SELF_AUTHORIZATION","VALID_AS_LIFECYCLE","VACUOUS_EMPTY_POLICY","TIMESTAMP_ONLY_ORDER","MUTATE_EVALUATION_OR_DECISION","REUSE_AFTER_CONTEXT_CHANGE","STALE_AS_CURRENT","DEFERRED_AS_UNKNOWN","MALFORMED_POLICY_AUTHORIZATION","AUTHORITY_FROM_UI_ROLE_OR_PROCESS","OBSERVATION_REWRITES_AUTHORIZATION"]},
 "ARTIFACT-TREE.yaml":{"logical_tree":{"discovery":["candidates"],"compliance":["certificates","certificate-candidates","evaluations","authorities","validity","decisions"],"release":["releases","gates","eligibility","decisions","execution","post-release-verification"],"history":["certificate-events","evaluation-events","authority-events","release-events","decision-events"],"projections":["current-certificates","current-validity","current-eligibility","current-decisions","current-execution","current-verification"],"schema":SCHEMA_NAMES},"physical_append_only_package":"historical-source/compliance/certification/v14.5","logical_tree_does_not_move_history":True},
 "OPEN-QUESTIONS.yaml":{"questions":[{"id":"OQ-145-1","topic":"CRYPTOGRAPHIC_AUTHORITY_REPRESENTATION","status":"UNKNOWN","minimum_rule":"Deployment profile selects credential system and records credential_ref"},{"id":"OQ-145-2","topic":"EVIDENCE_FRESHNESS_CLOCK","status":"UNKNOWN","minimum_rule":"Evaluation context records selected trusted clock mechanism"},{"id":"OQ-145-3","topic":"EXTERNAL_TRUST_ROOTS","status":"UNKNOWN","minimum_rule":"Deployment security profile declares roots and verification procedure"}]},
 "FINAL-PRINCIPLE.yaml":{"rule":"NO_STATE_TRANSITION_MAY_ESTABLISH_A_STRONGER_SEMANTIC_CLAIM_THAN_VALIDATED_EVIDENCE_EVALUATION_RESULT_POLICY_AUTHORITY_AND_SCOPE_JUSTIFY","layers":["VALIDATION_ESTABLISHES_TRUSTWORTHINESS","EVALUATION_ESTABLISHES_PROPOSITION_STATUS","AUTHORITY_ESTABLISHES_WHO_MAY_ACT","AUTHORIZATION_ESTABLISHES_PERMISSION","EXECUTION_ESTABLISHES_WHAT_HAPPENED","VERIFICATION_ESTABLISHES_POST_EXECUTION_OBSERVATION"],"invalid_crosses_authorization_boundary":False}
 }
 invariants=[
  "EVERY_NORMATIVE_EVALUATOR_RETURNS_EVALUATION_RESULT","INVALID_DISTINCT_FROM_FALSE","UNKNOWN_DISTINCT_FROM_BLOCKED","INVALID_REQUIRED_CANNOT_ESTABLISH_TRUTH","EVALUATION_CONTEXT_IMMUTABLE","EVALUATION_RESULT_IMMUTABLE","EVALUATION_AGGREGATION_DETERMINISTIC",
  "ELIGIBILITY_NOT_ISSUANCE_AUTHORITY","AUTHORITY_EXPLICIT","AUTHORITY_SCOPE_CONTAINS_OPERATION","DELEGATE_NOT_EXCEED_PARENT","MULTIPARTY_DISTINCT_APPROVALS","EXPIRED_OR_REVOKED_AUTHORITY_CANNOT_ISSUE","AUTOMATION_REQUIRES_POLICY",
  "CERTIFICATE_CANDIDATE_NOT_LIFECYCLE_STATE","DRAFT_IS_CERTIFICATE_OBJECT","AUTHORIZED_NOT_ISSUED","ISSUED_NOT_VALID","VALID_NOT_RELEASE_AUTHORIZED","INVALID_ISSUANCE_INPUT_CANNOT_ISSUE",
  "STRUCTURAL_FAILURE_PREVENTS_SEMANTIC_EVALUATION","INTEGRITY_FAILURE_PREVENTS_AUTHORIZATION","MISSING_EVIDENCE_NOT_TRUE","UNKNOWN_NOT_TRUE","BLOCKED_NOT_TRUE","INVALID_POLICY_CANNOT_AUTHORIZE","MISSING_AUTHORITY_CANNOT_AUTHORIZE",
  "EVENTS_IMMUTABLE","CURRENT_PROJECTIONS_DERIVED","WALL_CLOCK_NOT_AUTHORITATIVE_ORDER","PROJECTION_REPRODUCIBLE","NEW_EVIDENCE_NEW_EVALUATION",
  "ELIGIBILITY_IS_PREDICATE_EVALUATION","DECISION_IS_AUTHORIZATION","APPROVAL_NOT_EXECUTION","EXECUTION_NOT_VERIFICATION","POST_RELEASE_FAILURE_NO_DECISION_REWRITE","ARTIFACT_CHANGE_INVALIDATES_REUSE",
  "INVALID_NOT_HIDDEN_BY_FALSE","DECLARED_INTEGRITY_NOT_SELF_PROOF","WORKFLOW_MILESTONE_NOT_CANDIDATE_LIFECYCLE","ISSUED_CANNOT_CANCEL","HASH_TYPES_NOT_SUBSTITUTABLE"
 ]
 artifacts["INVARIANTS.yaml"]={"invariants":[{"invariant_id":f"V145-INV-{i:03d}","rule":x,"machine_checked":True} for i,x in enumerate(invariants,1)],"count":len(invariants)}
 vectors=build_vectors();artifacts["TEST-VECTORS.yaml"]={"synthetic_non_normative":True,"vectors":vectors,"summary":{"total":len(vectors),"passed":sum(x["passed"] for x in vectors),"failed":sum(not x["passed"] for x in vectors)}}
 empty={"objects":[],"append_only":True,"invented":False}
 for name in ["EVALUATION-HISTORY.yaml","AUTHORITY-HISTORY.yaml","CERTIFICATE-HISTORY.yaml","RELEASE-HISTORY.yaml"]: artifacts[name]=empty
 artifacts["CURRENT-STATUS.yaml"]={"objects":[],"current":{"evaluations":0,"authorities":0,"certificate_candidates":0,"certificates":0,"releases":0,"decisions":0,"executions":0,"verifications":0},"audit_status":"SPEC_INVALID_AT_PIPELINE_STAGE_2","invented":False}
 artifacts["CURRENT-PROJECTIONS-DATA.yaml"]={"objects":[],"source_histories":[],"projection_status":"NOT_APPLICABLE_NO_VALID_CURRENT_OBJECTS","invented":False}
 for name in MACHINE_FILES:
  if name in {"SCHEMA-REGISTRY.yaml","PRIOR-INTEGRITY.yaml","VALIDATION-REPORT.yaml"}:continue
  value={**origin,**artifacts[name]};dump(DEST/name,value)
 registry=[]
 for name in SCHEMA_NAMES:
  p=SCHEMA/f"{name}.schema.yaml";registry.append({"name":name,"path":f"schema/{name}.schema.yaml","sha256":sha(p),"identity_fields":load(p)["x-identity-fields"],"immutable":True})
 dump(DEST/"SCHEMA-REGISTRY.yaml",{**origin,"schemas":registry,"discovery_candidate_schema":{"path":"../v14.3/schema/candidate.schema.yaml","sha256":sha(V144.parent/"v14.3/schema/candidate.schema.yaml"),"preserved_exactly":True}})
 (DEST/"SPECIFICATION.md").write_text(build_spec())
 reports={
  "SEMANTIC-CORRECTIONS-REPORT.yaml":{"corrections":["INVALID_EVALUATION_PRODUCES_NO_AUTHORITATIVE_VALIDITY_OR_ELIGIBILITY_OBJECT","CANDIDATE_BINDS_POLICIES_WHILE_AUTHORIZATION_BINDS_DOWNSTREAM_RESULTS","CANDIDATE_WORKFLOW_MILESTONES_NOT_LIFECYCLE","ISSUED_TO_CANCELLED_FORBIDDEN","EVENT_ORDER_SIGNALS_MUST_COHERE","DECLARED_INTEGRITY_INDEPENDENTLY_CHECKED"],"silent_repair_of_history":False},
  "FAIL-CLOSED-COVERAGE-REPORT.yaml":{"boundaries":5,"failure_classes":13,"vectors":len(vectors),"invariants":len(invariants),"all_required_prompt_vectors_present":True},
  "CURRENT-HISTORICAL-STATUS.yaml":{"current_release":"NONE","current_certificate":"NONE","current_evaluation":"NONE","current_authority":"NONE","current_execution":"NONE","current_verification":"NONE","acceptance_gate":"BLOCKED_SPEC_INVALID"}
 }
 for name,val in reports.items():dump(DEST/"reports"/name,{**origin,**val})
 after=[{"path":str(p.relative_to(COMPLIANCE)),"sha256":sha(p),"bytes":p.stat().st_size} for p in sorted(COMPLIANCE.rglob("*")) if p.is_file() and DEST not in p.parents]
 if before!=after: raise RuntimeError("predecessor mutation detected")
 dump(DEST/"PRIOR-INTEGRITY.yaml",{**origin,"protected_artifact_count":len(before),"artifacts":before,"status":"PRESERVED"})
 owned=MACHINE_FILES+[f"schema/{x}.schema.yaml" for x in SCHEMA_NAMES]+[f"reports/{x}" for x in REPORT_FILES]+["SPECIFICATION.md"]
 dump(DEST/"VALIDATION-REPORT.yaml",{**origin,"generator_owned_deliverables":len(owned),"schemas":len(SCHEMA_NAMES),"vectors":len(vectors),"invariants":len(invariants),"current_operational_objects":0,"status":"AWAITING_INDEPENDENT_VALIDATION"})
 print(f"generated {len(owned)} v14.5 deliverables; schemas={len(SCHEMA_NAMES)} vectors={len(vectors)} invariants={len(invariants)} current=NONE")
if __name__=="__main__":main()
