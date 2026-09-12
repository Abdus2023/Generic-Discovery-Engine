#!/usr/bin/env python3
"""v14.7-R2.1 boundary-correct realization interfaces."""
from v147r2_conformance_harness import *
from v147r2_conformance_harness import TemporalValidator as R2TemporalValidator
VALIDATION_STATUSES=("VALID","INVALID","BLOCKED","UNKNOWN")
CONFORMANCE_STATUSES=("CONFORMANT","PARTIALLY_CONFORMANT","NON_CONFORMANT","UNVERIFIED","BLOCKED","NOT_APPLICABLE","UNKNOWN")
class ScopeValidator:
 def validate(self,requested,granted):return outcome("VALID" if set(requested)<=set(granted) else "INVALID",None if set(requested)<=set(granted) else "SCOPE_FAILURE")
class EvidenceValidator:
 def validate(self,evidence):
  if evidence is None:return outcome("INVALID","REFERENCE_FAILURE","missing required evidence")
  return outcome({"FRESH":"VALID","STALE":"UNKNOWN","UNKNOWN":"UNKNOWN","UNAVAILABLE":"BLOCKED","INVALID":"INVALID"}.get(evidence.get("freshness"),"INVALID"),None if evidence.get("freshness")=="FRESH" else "EVIDENCE_FAILURE")
class TemporalValidator(R2TemporalValidator):
 def validate_interval(self,instant,not_before,not_after):
  raw=super().validate_interval(instant,not_before,not_after)
  if raw["status"]=="ACTIVE":return outcome("VALID",value="ACTIVE")
  if raw["status"] in {"NOT_YET_VALID","EXPIRED"}:return outcome("VALID",value=raw["status"])
  return raw
class AuthorityValidator:
 def qualify(self,authority,credential,operation,requested_scope,policy,instant,approvals=()):
  if not credential or not credential.get("valid"):return outcome("INVALID","AUTHORITY_FAILURE","credential")
  if authority.get("status")!="ACTIVE":return outcome("UNQUALIFIED","AUTHORITY_FAILURE","inactive")
  if operation not in authority.get("operations",[]):return outcome("UNQUALIFIED","AUTHORITY_FAILURE","operation")
  if ScopeValidator().validate(requested_scope,authority.get("scope",[]))["status"]!="VALID":return outcome("UNQUALIFIED","SCOPE_FAILURE")
  temporal=TemporalValidator().validate_interval(instant,authority["not_before"],authority.get("not_after"))
  if temporal["status"]!="VALID" or temporal["value"]!="ACTIVE":return outcome("UNQUALIFIED","AUTHORITY_FAILURE",str(temporal.get("value")))
  if authority.get("parent_scope") is not None and not set(authority.get("scope",[]))<=set(authority["parent_scope"]):return outcome("INVALID","AUTHORITY_FAILURE","delegation")
  threshold=policy.get("threshold",1)
  if threshold<1:return outcome("INVALID","POLICY_FAILURE","threshold")
  distinct={a["authority_id"] for a in approvals if a.get("valid") and a.get("basis_hash")==policy.get("basis_hash")}
  if authority.get("type")=="MULTI_PARTY" and len(distinct)<threshold:return outcome("BLOCKED","AUTHORITY_FAILURE","threshold")
  return outcome("QUALIFIED")
class ValidatedEvaluator:
 def evaluate(self,validation_result,subject,predicate,context,evaluator):
  if validation_result not in VALIDATION_STATUSES:return outcome("INVALID","VALIDATION_FAILURE","invalid validation output")
  if validation_result!="VALID":return outcome("BLOCKED" if validation_result in {"BLOCKED","UNKNOWN"} else "INVALID","VALIDATION_FAILURE","evaluation not permitted")
  return Evaluator().evaluate(subject,predicate,context,evaluator)
class ConformanceEvaluator:
 def derive(self,applicable,mandatory_results,optional_results=()):
  if not applicable:return outcome("NOT_APPLICABLE")
  if any(x=="INVALID" for x in mandatory_results):return outcome("NO_RESULT","EVALUATION_FAILURE")
  if "FALSE" in mandatory_results:return outcome("NON_CONFORMANT")
  if "BLOCKED" in mandatory_results:return outcome("BLOCKED")
  if "UNKNOWN" in mandatory_results:return outcome("UNVERIFIED")
  if all(x=="TRUE" for x in mandatory_results):return outcome("PARTIALLY_CONFORMANT" if "FALSE" in optional_results else "CONFORMANT")
  return outcome("UNKNOWN")
class ProfileConformanceChecker:
 def check(self,profile,specification):
  required={"profile_id","profile_version","specification","serialization","hashing","signatures","time","events","policy","limits","compatibility","choice_universe","semantic_preservation","choice_classification"}
  if not required<=set(profile):return outcome("NON_CONFORMANT","PROFILE_FAILURE","incomplete profile")
  if profile["specification"]["specification_hash"]!=specification["content_hash"]:return outcome("NON_CONFORMANT","PROFILE_FAILURE")
  statuses={x["status"] for x in profile["choice_classification"]}
  if not statuses<={"FIXED","PROFILE-SELECTABLE","IMPLEMENTATION-DEFINED"}:return outcome("INVALID","PROFILE_FAILURE")
  choices=[x["choice"] for x in profile["choice_classification"]]
  if not profile["choice_universe"].get("closed") or choices!=profile["choice_universe"].get("choices") or len(choices)!=len(set(choices)):return outcome("NON_CONFORMANT","PROFILE_FAILURE","choice universe")
  if any(x["status"]=="PROFILE-SELECTABLE" and x.get("selected") is None for x in profile["choice_classification"]):return outcome("NON_CONFORMANT","PROFILE_FAILURE")
  preservation=profile["semantic_preservation"]
  if any(preservation.get(k)!=v for k,v in {"semantic_states":"UNCHANGED","state_meanings":"UNCHANGED","authority":"UNCHANGED","invariants":"PRESERVED","validation_boundaries":"PRESERVED","uncertainty":"PRESERVED"}.items()):return outcome("NON_CONFORMANT","PROFILE_FAILURE","semantic weakening")
  return outcome("CONFORMANT")
class ImplementationConformanceChecker:
 def check(self,implementation,profile,checks):
  if implementation.get("profile_id")!=profile["profile_id"] or implementation.get("profile_version")!=profile["profile_version"]:return outcome("NON_CONFORMANT","IMPLEMENTATION_FAILURE")
  if any(x=="VIOLATED" for x in checks):return outcome("NON_CONFORMANT","IMPLEMENTATION_FAILURE")
  if any(x in {"UNKNOWN","BLOCKED"} for x in checks):return outcome("UNVERIFIED")
  return outcome("CONFORMANT")
def forbidden_coercion(source_domain,source_value,target_domain,target_value,rule_ref=None):
 forbidden={("ValidationResult","INVALID","EvaluationResult","FALSE"),("ValidationResult","UNKNOWN","EvaluationResult","TRUE"),("EvaluationResult","UNKNOWN","EvaluationResult","TRUE"),("EvaluationResult","BLOCKED","EvaluationResult","TRUE"),("EvaluationResult","INVALID","EvaluationResult","FALSE"),("ConformanceResult","UNVERIFIED","ConformanceResult","CONFORMANT"),("EligibilityResult","UNKNOWN","Decision","APPROVED"),("EligibilityResult","BLOCKED","Decision","APPROVED"),("Decision","APPROVED","Execution","EXECUTED")}
 return outcome("REJECTED" if (source_domain,source_value,target_domain,target_value) in forbidden and not rule_ref else "ALLOWED")
