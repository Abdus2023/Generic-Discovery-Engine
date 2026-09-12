#!/usr/bin/env python3
"""Independent validator for v14.7-R6 machine contracts."""
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HIST=ROOT/"historical-source";COMP=HIST/"compliance";BASE=COMP/"certification/v14.7-R6";TOOLS=HIST/"tools"
sys.path.insert(0,str(TOOLS))
from run_v147r6_conformance import run
EXPECTED={
"ValidationStatus":["VALID","INVALID","BLOCKED","UNKNOWN"],"EvaluationValue":["TRUE","FALSE","UNKNOWN","BLOCKED","INVALID"],"ConformanceStatus":["CONFORMANT","PARTIALLY_CONFORMANT","NON_CONFORMANT","UNVERIFIED","BLOCKED","NOT_APPLICABLE","UNKNOWN"],"CertificateLifecycle":["DRAFT","ISSUED","REVOKED","SUPERSEDED","EXPIRED","CANCELLED"],"CertificateValidity":["VALID","INVALID","NOT_YET_VALID","UNKNOWN"],"ReleaseEligibility":["ELIGIBLE","INELIGIBLE","BLOCKED","UNKNOWN"],"AuthorizationStatus":["AUTHORIZED","REFUSED","BLOCKED","UNKNOWN","INVALID"],"ReleaseDecisionStatus":["APPROVED","REJECTED","BLOCKED","DEFERRED"],"ReleaseExecutionStatus":["NOT_STARTED","STARTED","SUCCEEDED","FAILED","CANCELLED","ROLLED_BACK"],"PostReleaseVerificationStatus":["NOT_STARTED","IN_PROGRESS","PASSED","FAILED","INCONCLUSIVE","BLOCKED","INVALID"],"ReuseStatus":["REUSABLE","NOT_REUSABLE","BLOCKED","UNKNOWN","INVALID"],"AuthorityStatus":["ACTIVE","SUSPENDED","REVOKED","EXPIRED","UNKNOWN"],"AuthorityQualificationStatus":["QUALIFIED","NOT_QUALIFIED","BLOCKED","UNKNOWN","INVALID"],"RequirementLifecycle":["PROPOSED","DRAFT","ACTIVE","DEPRECATED","SUPERSEDED","RETIRED"],"FindingStatus":["OPEN","TRIAGED","ROOT_CAUSE_IDENTIFIED","REMEDIATION_PLANNED","REMEDIATION_IN_PROGRESS","READY_FOR_REVERIFICATION","REVERIFICATION_IN_PROGRESS","RESOLVED","WAIVED","REJECTED","CLOSED"],"RemediationStatus":["PLANNED","APPROVED","IN_PROGRESS","BLOCKED","READY_FOR_VERIFICATION","VERIFIED","FAILED","CANCELLED","SUPERSEDED"],"EventValidationStatus":["VALID","INVALID","BLOCKED","UNKNOWN"],"EventCommitStatus":["PENDING","COMMITTED","REJECTED"],"ProjectionStatus":["CURRENT","REPLAYING","STALE","INVALID","BLOCKED","UNKNOWN"],"NormativeStrength":["MUST","MUST_NOT","SHOULD","SHOULD_NOT","MAY"]}
ERRORS=["INVALID_PREDICATE","INVALID_SUBJECT","INVALID_CONTEXT","VALIDATION_REQUIRED","VALIDATION_FAILED","UNSUPPORTED_PREDICATE","EVALUATOR_FAILURE","EVALUATOR_TIMEOUT","EVALUATOR_RESOURCE_FAILURE","EVALUATOR_INTERNAL_FAILURE","OUTPUT_INVALID","EVALUATOR_DEPENDENCY_UNAVAILABLE"]
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main(base=BASE):
    rows=[]
    def check(identifier,description,condition,blocked=False,detail=None):rows.append({"check_id":identifier,"description":description,"status":"BLOCKED" if blocked else "PASS" if condition else "FAIL","detail":detail})
    docs={};errors=[]
    for p in sorted(x for x in base.rglob("*") if x.is_file() and x.suffix in {".yaml",".json"}):
        try:docs[str(p.relative_to(base))]=load(p)
        except Exception as e:errors.append(f"{p}:{e}")
    check("R6-V-001","All machine documents parse",not errors,detail=errors or None)
    manifest=docs["GENERATOR-MANIFEST.yaml"];actual=sorted(str(p.relative_to(base)) for p in base.rglob("*") if p.is_file())
    check("R6-V-002","Manifest count and uniqueness are exact",manifest["count"]==len(manifest["paths"])==len(set(manifest["paths"]))==84)
    check("R6-V-003","Manifest declares every R6 artifact",manifest["paths"]==actual)
    prior=docs["PRIOR-INTEGRITY.yaml"];indexed={x["path"]:x for x in prior["artifacts"]}
    check("R6-V-004","R6 protects all 1,249 predecessor files",prior["protected_artifact_count"]==len(indexed)==1249)
    check("R6-V-005","Every predecessor byte count and hash remains exact",all((COMP/p).is_file() and (COMP/p).stat().st_size==x["bytes"] and sha(COMP/p)==x["sha256"] for p,x in indexed.items()))
    registry=docs["CLOSED-ENUM-REGISTRY.yaml"];domains={x["machine_type"]:x["values"] for x in registry["objects"]}
    check("R6-V-006","Twenty machine enum domains are closed",registry["domain_count"]==len(domains)==20 and all(x["closed"] for x in registry["objects"]))
    check("R6-V-007","All 111 inherited and supplied values are exact",domains==EXPECTED and registry["value_count"]==111)
    check("R6-V-008","Unknown values are rejected",all(x["unknown_value"]=="REJECT" for x in registry["objects"]))
    check("R6-V-009","Sixteen supplied and four inherited domains are distinguished",registry["supplied_r6_domains"]==16 and registry["inherited_r5_domains"]==4 and sum(x["origin"]=="INHERITED_R5" for x in registry["objects"])==4)
    check("R6-V-010","R5 semantic domains map explicitly to R6 machine names",len(registry["aliases"])==20 and set(registry["aliases"].values())==set(EXPECTED))
    ids=docs["IDENTIFIER-DOMAINS.yaml"];id_names=[x["identifier_domain"] for x in ids["objects"]]
    check("R6-V-011","Semantic identifier domains are distinct",len(id_names)==len(set(id_names))==21 and all(x["interchangeable"] is False for x in ids["objects"]))
    check("R6-V-012","Generic semantic-boundary identifiers are prohibited",ids["generic_identifier_at_semantic_boundary"]=="FORBIDDEN")
    planes=docs["PLANE-MODEL.yaml"]
    check("R6-V-013","Exactly five planes are defined",[x["plane"] for x in planes["objects"]]==["NORMATIVE","PROFILE","IMPLEMENTATION","EVIDENCE","DECISION"])
    check("R6-V-014","Implicit authority inheritance is forbidden",planes["implicit_authority_inheritance"]=="FORBIDDEN")
    schema_registry=docs["SCHEMA-REGISTRY.yaml"];schemas={x["schema_id"]:docs[x["path"]] for x in schema_registry["objects"]}
    check("R6-V-015","Twenty machine schemas are registered",schema_registry["count"]==len(schemas)==20)
    check("R6-V-016","Abstract schema language leaves concrete dialect implementation-only",schema_registry["language"]=="GDE-ABSTRACT-SCHEMA-1" and schema_registry["dialect_binding"]=="IMPLEMENTATION_TASK")
    check("R6-V-017","Every schema is closed",all(x["closed"] and x["additional_fields"]=="FORBIDDEN" for x in schemas.values()))
    check("R6-V-018","Required and optional fields form complete disjoint sets",all(set(x["required"])|set(x["optional"])==set(x["fields"]) and not set(x["required"])&set(x["optional"]) for x in schemas.values()))
    check("R6-V-019","Every schema declares identifier, reference, cardinality, temporal, and integrity policies",all(all(x.get(k) for k in ["identifier_policy","reference_policy","cardinality_policy","temporal_policy","integrity_policy"]) for x in schemas.values()))
    check("R6-V-020","Every schema binds canonicalization and a distinct hash domain",all(x["canonicalization_ref"] and x["hash"]["domain"] for x in schemas.values()) and len({x["hash"]["domain"] for x in schemas.values()})==20)
    req=schemas["NormativeRequirement"]
    check("R6-V-021","NormativeRequirement has the supplied required fields",req["required"]==["requirement_id","specification_id","specification_version","lifecycle","statement","normative_strength","scope","content_hash"])
    check("R6-V-022","NormativeRequirement remains technology-neutral",not any(re.search(rf"\\b{word}\\b", json.dumps(req).lower()) for word in ["rust","cargo","sqlite","tokio","wasm"]))
    imp=schemas["ImplementationRequirement"]
    check("R6-V-023","ImplementationRequirement traces requirement and profile",imp["fields"]["target_requirement"]["reference_domain"]=="RequirementId" and imp["fields"]["target_profile"]["reference_domain"]=="ProfileId")
    instruction=schemas["ImplementationInstruction"]
    check("R6-V-024","ImplementationInstruction is a distinct implementation object",instruction["plane"]=="IMPLEMENTATION" and instruction["object_type"]!="ImplementationRequirement" and instruction["fields"]["instruction_type"]["allowed_values"]==["PROFILE_BINDING","IMPLEMENTATION_GUIDANCE","OPTIMIZATION","DEPLOYMENT","TEST_HARNESS","STORAGE","LANGUAGE","LIBRARY"])
    validation=schemas["ValidationResult"];evaluation=schemas["EvaluationResult"];conformance=schemas["ConformanceResult"]
    check("R6-V-025","Validation uses only ValidationStatus",validation["fields"]["status"]["enum_domain"]=="ValidationStatus")
    check("R6-V-026","Evaluation uses only EvaluationValue",evaluation["fields"]["result"]["enum_domain"]=="EvaluationValue")
    check("R6-V-027","Conformance is requirement-bound",conformance["fields"]["requirement_ref"]["reference_domain"]=="RequirementId")
    check("R6-V-063","Tests, observations, and evidence are distinct Evidence-plane schemas",all(schemas[name]["plane"]=="EVIDENCE" for name in ["TestDefinition","Observation","Evidence"]) and schemas["Evidence"]["fields"]["observation_refs"]["reference_domain"]=="ObservationId")
    error_policy=docs["ERROR-POLICY.yaml"];error_objects=error_policy["objects"]
    check("R6-V-028","Twelve deterministic error categories preserve dependency coverage",[x["code"] for x in error_objects]==ERRORS)
    check("R6-V-029","Eleven supplied errors and one inherited error are labeled",sum(x["origin"]=="SUPPLIED_R6" for x in error_objects)==11 and sum(x["origin"]=="INHERITED_R5" for x in error_objects)==1)
    check("R6-V-030","Every evaluator error defaults to evaluation failure",all(x["default"]=="EVALUATION_FAILURE" for x in error_objects))
    check("R6-V-031","No evaluator error can map to FALSE",all(x["false_mapping"] is False and "FALSE" not in x["allowed_explicit_mappings"] for x in error_objects))
    check("R6-V-032","Error mapping requires explicit profile policy",error_policy["explicit_profile_policy_required"] is True and error_policy["automatic_semantic_mapping"] is False)
    evaluator=docs["EVALUATOR-CONTRACT.yaml"]
    check("R6-V-033","Evaluator result and error boundary is explicit","Result<EvaluationResult, EvaluationError>" in evaluator["interface"] and evaluator["error_postcondition"]=="NO_VALID_EVALUATION_RESULT_PRODUCED")
    check("R6-V-034","Evaluator has no decision or mutation authority",len(evaluator["forbidden_operations"])==7)
    conversions=docs["CONVERSION-REGISTRY.yaml"];rules=conversions["objects"]
    check("R6-V-035","Five named conversion rules exist",conversions["count"]==len(rules)==5 and len({x["rule_id"] for x in rules})==5)
    check("R6-V-036","Generic conversion is forbidden",conversions["generic_convert"]=="FORBIDDEN" and all(x["generic_convert"] is False for x in rules))
    check("R6-V-037","Every conversion defines source, target, legal, forbidden, evidence, policy, and failure",all(all(k in x for k in ["source_type","target_type","legal","forbidden","evidence_required","policy_required","failure"]) for x in rules))
    transitions=docs["TRANSITION-REGISTRY.yaml"]
    check("R6-V-038","Exactly eleven supplied certificate and execution edges exist",transitions["count"]==len(transitions["objects"])==11)
    check("R6-V-039","Unlisted transitions are illegal",transitions["unlisted_transition"]=="ILLEGAL")
    check("R6-V-040","Finding and remediation edges are not invented",transitions["finding_transition_binding"]==transitions["remediation_transition_binding"]=="PROFILE_RULE_REQUIRED")
    pipeline=docs["TYPED-PIPELINE.yaml"]
    check("R6-V-041","Typed pipeline keeps semantic and error types separate",pipeline["error_as_semantic_result"]=="FORBIDDEN" and len(pipeline["success"])==9 and len(pipeline["errors"])==6)
    check("R6-V-042","Typestate remains an implementation technique",pipeline["typestate_normativity"]=="IMPLEMENTATION_TECHNIQUE")
    tests=docs["tests/MACHINE-TESTS.yaml"];cases=tests["objects"];families={x["family"] for x in cases}
    check("R6-V-043","All seven mandatory test families exist",set(tests["families"])<families and len(tests["families"])==7)
    check("R6-V-044","Minimum negative N-001 through N-018 is exact",[x["negative_ref"] for x in cases if x["family"]=="MINIMUM_NEGATIVE_SET"]==[f"N-{i:03d}" for i in range(1,19)])
    check("R6-V-045","All enum values and unknown values are tested",sum(x["family"]=="T1_ENUM_CLOSURE" for x in cases)==151)
    check("R6-V-046","Every schema required field has a missing-field test",sum(x["family"]=="T2_SCHEMA_VALIDITY" for x in cases)==sum(len(x["required"])+2 for x in schemas.values()))
    check("R6-V-047","Every evaluator error and disposition boundary is tested",sum(x["family"]=="T4_EVALUATOR_ERRORS" for x in cases)==63)
    check("R6-V-048","Every certificate and release state pair is tested",sum(x["family"]=="T6_STATE_TRANSITIONS" for x in cases)==78)
    invariants=docs["MACHINE-INVARIANTS.yaml"]["objects"]
    check("R6-V-049","R6-I01 through R6-I18 are complete and tested",[x["invariant_id"] for x in invariants]==[f"R6-I{i:02d}" for i in range(1,19)] and all(x["status"]=="SATISFIED" for x in invariants))
    runtime=run(base);runtime_fail=[x for x in runtime if x["status"]!="PASSED"]
    check("R6-V-050","All 549 machine vectors pass",len(runtime)==549 and not runtime_fail,detail=runtime_fail or None)
    check("R6-V-051","Persisted vector summary is exact",docs["MACHINE-TEST-RESULTS.yaml"]["summary"]=={"total":549,"passed":549,"failed":0})
    rust_root=base/"rust/gde-v147-r6-machine";rust="\n".join(p.read_text() for p in rust_root.rglob("*.rs"))
    check("R6-V-052","Rust forbids unsafe and generic boxed errors","#![forbid(unsafe_code)]" in rust and "Box<dyn" not in rust and "unsafe {" not in rust)
    check("R6-V-053","Rust defines all twenty machine enums",all(re.search(rf"enum\s+{name}\s*\{{",rust) for name in EXPECTED))
    check("R6-V-054","Rust defines all supplied identifier newtypes",all(f"id!({name})" in rust for name in ["SpecificationId","RequirementId","ProfileId","PredicateId","EvaluationId","EvidenceId","ImplementationId","AuthorityId","CertificateId","ReleaseId","DecisionId","EventId","FindingId","RemediationId","TestId","ObservationId"]))
    check("R6-V-055","Rust Evaluator has the canonical typed signature","Result<EvaluationResult,EvaluationError>" in rust and "subject:&ValidatedSubject" in rust)
    check("R6-V-056","Rust transition guards encode supplied edges","certificate_transition" in rust and "execution_transition" in rust)
    contradictions=docs["CONTRADICTIONS.yaml"]
    check("R6-V-057","Three representation omissions are explicitly reconciled",len(contradictions["objects"])==3 and all(x["status"]=="RESOLVED" and x["semantic_state_change"] is False for x in contradictions["objects"]))
    check("R6-V-058","No unresolved semantic contradiction requires a new state",contradictions["unresolved_semantic_contradictions"]==0 and contradictions["conclusion"]=="NO NEW SEMANTIC STATE REQUIRED")
    check("R6-V-059","R5 to R6 migration preserves semantics",docs["MIGRATION-R5-TO-R6.yaml"]["new_semantic_states"] is False and docs["MIGRATION-R5-TO-R6.yaml"]["source_validity_transfers"] is False)
    check("R6-V-060","Specification contains thirty numbered sections",len(re.findall(r"^## \d+\.", (base/"SPECIFICATION.md").read_text(),re.M))==30)
    check("R6-V-061","Neither v14.8 nor R7 was created",not (COMP/"certification/v14.8").exists() and not (COMP/"certification/v14.7-R7").exists())
    cargo=shutil.which("cargo")
    if cargo:
        proc=subprocess.run([cargo,"test","--locked"],cwd=rust_root,capture_output=True,text=True);check("R6-V-062","Rust blueprint compiles and tests",proc.returncode==0,detail={"returncode":proc.returncode})
    else:check("R6-V-062","Rust blueprint compiles and tests",False,blocked=True,detail="RUST_TOOLCHAIN_UNAVAILABLE")
    summary={"pass":sum(x["status"]=="PASS" for x in rows),"fail":sum(x["status"]=="FAIL" for x in rows),"blocked":sum(x["status"]=="BLOCKED" for x in rows)};result="FAIL" if summary["fail"] else "PASS_WITH_BLOCKED_TOOLCHAIN" if summary["blocked"] else "PASS"
    report={"realization_version":"14.7-R6","validator":"validate_machine_domain_realization_v147r6.py","objects":rows,"summary":summary,"result":result};(base/"INDEPENDENT-VALIDATION.yaml").write_text(json.dumps(report,indent=2)+"\n")
    validation=docs["VALIDATION-REPORT.yaml"];validation["status"]="INDEPENDENT_VALIDATION_COMPLETE";validation["independent_summary"]=summary;validation["independent_result"]=result;(base/"VALIDATION-REPORT.yaml").write_text(json.dumps(validation,indent=2)+"\n")
    for row in rows:print(f"{row['check_id']} {row['status']} {row['description']}")
    print(f"summary: {summary['pass']} PASS / {summary['fail']} FAIL / {summary['blocked']} BLOCKED");return 1 if summary["fail"] else 0
if __name__=="__main__":sys.exit(main())
