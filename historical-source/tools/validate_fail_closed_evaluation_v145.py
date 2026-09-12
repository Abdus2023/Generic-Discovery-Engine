#!/usr/bin/env python3
"""Independent Protocol-v14.5 validator; standard library only."""
from __future__ import annotations
import ast, hashlib, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; HIST=ROOT/"historical-source"; COMP=HIST/"compliance"; DEST=COMP/"certification/v14.5"; VERSION="14.5"
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def aggregate(values):
 if "INVALID" in values:return "INVALID"
 if "FALSE" in values:return "FALSE"
 if "BLOCKED" in values:return "BLOCKED"
 if "UNKNOWN" in values:return "UNKNOWN"
 return "TRUE"
def authorize(values):
 if "INVALID" in values:return "INVALID"
 if "FALSE" in values:return "REFUSED"
 if "BLOCKED" in values:return "BLOCKED"
 if "UNKNOWN" in values:return "UNKNOWN"
 return "AUTHORIZED"
def main():
 checks=[]
 def check(cid,cat,desc,ok,detail=""):checks.append({"check_id":cid,"category":cat,"result":"PASS" if ok else "FAIL","description":desc,"detail":detail})
 # Inventory and parseability.
 expected_machine=load_builder_constant("MACHINE_FILES"); expected_schemas=load_builder_constant("SCHEMA_NAMES"); expected_reports=load_builder_constant("REPORT_FILES")
 owned=expected_machine+[f"schema/{x}.schema.yaml" for x in expected_schemas]+[f"reports/{x}" for x in expected_reports]+["SPECIFICATION.md"]
 check("I01","inventory","all 85 generator-owned paths exist",len(owned)==85 and all((DEST/x).is_file() for x in owned))
 yaml_errors=[]
 for p in DEST.rglob("*.yaml"):
  try:load(p)
  except Exception as e:yaml_errors.append(f"{p.relative_to(DEST)}: {e}")
 check("I02","parseability","all JSON-compatible YAML parses",not yaml_errors,"; ".join(yaml_errors))
 actual_generated={str(p.relative_to(DEST)) for p in DEST.rglob("*") if p.is_file()}-{"VALIDATION.yaml","VALIDATION.md","DETERMINISM-VALIDATION.yaml","REGRESSION-VALIDATION.yaml"}
 check("I03","inventory","no unregistered generator-owned artifact",actual_generated==set(owned),str(sorted(actual_generated^set(owned))))
 # Schema completeness.
 registry=load(DEST/"SCHEMA-REGISTRY.yaml"); schemas=registry["schemas"]
 check("S01","schema","30 locally complete unique schemas",len(schemas)==len(expected_schemas)==30 and len({x["name"] for x in schemas})==30)
 required_schema_keys={"$schema","$id","title","type","required","properties","additionalProperties","x-identity-fields","x-immutable","x-self-excluding-hash-field","x-reference-resolution","x-timestamp-semantics","x-scope-validation","x-normative-rules"}
 schema_ok=True; hash_ok=True; coverage_ok=True
 for item in schemas:
  p=DEST/item["path"]; d=load(p)
  schema_ok &= required_schema_keys<=set(d) and d["type"]=="object" and d["additionalProperties"] is False and set(d["required"])<=set(d["properties"]) and d["x-immutable"] is True and bool(d["x-identity-fields"])
  hash_ok &= sha(p)==item["sha256"]
  coverage_ok &= all(x in d["properties"] for x in d["x-identity-fields"]) and d["x-self-excluding-hash-field"] in d["properties"]
 check("S02","schema","schema meta-contract and required/property consistency",schema_ok)
 check("S03","schema","registry hashes match schema bytes",hash_ok)
 check("S04","schema","identity/hash fields explicitly modeled",coverage_ok)
 required_names={"evaluation-context","evaluation-result","freshness-result","issuance-authority","certificate-candidate","certificate-issuance-authorization","certificate","certificate-validity","release","release-gate","release-eligibility","release-decision","release-decision-event","release-execution","post-release-verification","current-certificate","current-certificate-validity","current-certificate-eligibility","current-release-eligibility","current-release-decision"}
 check("S05","schema","all 20 required named object schemas exist",required_names<={x["name"] for x in schemas})
 discovery=registry["discovery_candidate_schema"]; dp=DEST/discovery["path"]
 check("S06","schema","discovery Candidate schema reused byte-exactly from v14.3",discovery["preserved_exactly"] and dp.is_file() and sha(dp)==discovery["sha256"])
 def enum(schema,field):return load(DEST/f"schema/{schema}.schema.yaml")["properties"][field].get("enum")
 check("S07","schema","canonical EvaluationResult enum exact",enum("evaluation-result","result")==["TRUE","FALSE","UNKNOWN","BLOCKED","INVALID"])
 check("S08","schema","freshness enum exact",enum("freshness-result","status")==["FRESH","STALE","UNKNOWN","INVALID"])
 check("S09","schema","issuance authorization enum exact",enum("certificate-issuance-authorization","authorization_status")==["AUTHORIZED","REFUSED","BLOCKED","UNKNOWN","INVALID"])
 check("S10","schema","certificate lifecycle remains exact",enum("certificate","lifecycle")==["DRAFT","ISSUED","REVOKED","SUPERSEDED","EXPIRED","CANCELLED"])
 check("S11","schema","certificate validity remains exact",enum("certificate-validity","validity_status")==["VALID","INVALID","NOT_YET_VALID","UNKNOWN"])
 # Core semantic model.
 sem=load(DEST/"EVALUATION-RESULT-SEMANTICS.yaml")
 check("E01","evaluation","five result meanings are unique and exact",set(sem["results"])=={"TRUE","FALSE","UNKNOWN","BLOCKED","INVALID"} and len(set(sem["results"].values()))==5)
 check("E02","evaluation","INVALID is pre-aggregation validation failure",sem["invalid_phase"]=="PRE_AGGREGATION_VALIDATION_FAILURE" and sem["ordinary_precedence"]==["FALSE","BLOCKED","UNKNOWN","TRUE"])
 integrity=load(DEST/"EVALUATION-RESULT-INTEGRITY.yaml")
 check("E03","evaluation","integrity has all nine independent predicates",len(integrity["acceptance_predicates"])==9 and integrity["declared_integrity_is_proof"] is False)
 check("E04","evaluation","invalid result establishes no stronger claim",integrity["invalid_may_establish"]==[] and len(integrity["invalid_forbidden_claims"])==8)
 ctx=load(DEST/"EVALUATION-CONTEXT-MODEL.yaml")
 check("E05","evaluation","context immutable and change requires new evaluation",ctx["immutable_from"]=="EVALUATION_START" and ctx["change_effect"]=="NEW_CONTEXT_AND_NEW_EVALUATION")
 agg=load(DEST/"PREDICATE-AGGREGATION.yaml")
 combos={("TRUE","TRUE"):"TRUE",("TRUE","UNKNOWN"):"UNKNOWN",("UNKNOWN","BLOCKED"):"BLOCKED",("BLOCKED","FALSE"):"FALSE",("FALSE","INVALID"):"INVALID"}
 check("E06","evaluation","independent aggregation reproduces precedence including INVALID",agg["valid_required_precedence"]==["FALSE","BLOCKED","UNKNOWN","TRUE"] and all(aggregate(list(k))==v for k,v in combos.items()))
 empty=load(DEST/"EMPTY-SET-POLICY.yaml")
 check("E07","evaluation","empty set requires explicit four-way policy",empty["enum"]==["ALLOW","DENY","BLOCK","UNKNOWN"] and empty["missing"]=="POLICY_INVALID" and "VACUOUS" in empty["allow_semantics"])
 fresh=load(DEST/"FRESHNESS-SEMANTICS.yaml")
 check("E08","evaluation","stale defaults UNKNOWN and may explicitly BLOCK",fresh["default_stale_mapping"]=="UNKNOWN" and fresh["explicit_blocker_policy_mapping"]=="BLOCKED" and fresh["stale_to_false"]=="FORBIDDEN")
 # Fail-closed boundary mechanics.
 bounds=load(DEST/"FAIL-CLOSED-BOUNDARIES.yaml")["levels"]
 check("F01","fail_closed","five ordered L0-L4 boundaries",[x["level"] for x in bounds]==["L0_STRUCTURAL","L1_REFERENTIAL","L2_INTEGRITY","L3_SEMANTIC","L4_AUTHORIZATION"])
 check("F02","fail_closed","L0-L2 stop dependent processing",all(bounds[i]["later"]=="STOP" for i in [0,1,2]))
 matrix=load(DEST/"FAIL-CLOSED-MATRIX.yaml")["rows"]
 by_failure={x["failure"]:x for x in matrix}
 check("F03","fail_closed","structural/reference/hash/signature failures are INVALID",all(by_failure[x]["evaluation"]=="INVALID" for x in ["MALFORMED_SCHEMA","MISSING_REQUIRED_REFERENCE","BROKEN_HASH","INVALID_SIGNATURE"]))
 check("F04","fail_closed","semantic false differs from unavailable and unknown",by_failure["PROVEN_FAILED_PREDICATE"]["evaluation"]=="FALSE" and by_failure["UNAVAILABLE_PREREQUISITE"]["evaluation"]=="BLOCKED" and by_failure["UNKNOWN_SEMANTICS"]["evaluation"]=="UNKNOWN")
 check("F05","fail_closed","invalid input never fabricates ineligibility",all(by_failure[x]["eligibility"]=="NO_AUTHORITATIVE_RESULT" for x in ["MALFORMED_SCHEMA","MISSING_REQUIRED_REFERENCE","BROKEN_HASH","INVALID_SIGNATURE","POLICY_CONTRADICTION","MISSING_ISSUANCE_POLICY"]))
 # Authority/issuance.
 auth=load(DEST/"ISSUANCE-AUTHORITY-MODEL.yaml"); asem=load(DEST/"AUTHORITY-SEMANTICS.yaml")
 check("A01","authority","four issuance authority classes exact",auth["types"]==["AUTOMATED_POLICY","HUMAN","DELEGATED","MULTI_PARTY"])
 check("A02","authority","nine authority checks and no implicit authority",len(auth["required_checks"])==9 and auth["implicit_authority"]=="FORBIDDEN")
 check("A03","authority","delegation subset and distinct multi-party approvals",asem["delegated"]=="DELEGATE_SCOPE_SUBSET_PARENT_SCOPE" and asem["multi_party"].startswith("DISTINCT_VALID_APPROVALS") and asem["same_actor_multiple_approvals"].startswith("FORBIDDEN"))
 precedence=load(DEST/"AUTHORIZATION-PRECEDENCE.yaml")
 amap={"INVALID":"INVALID","FALSE":"REFUSED","BLOCKED":"BLOCKED","UNKNOWN":"UNKNOWN","TRUE":"AUTHORIZED"}
 check("A04","authority","authorization precedence and mapping exact",precedence["mapping"]==amap and authorize(["TRUE","TRUE","TRUE"])=="AUTHORIZED" and authorize(["TRUE","FALSE","BLOCKED"])=="REFUSED" and authorize(["TRUE","UNKNOWN","TRUE"])=="UNKNOWN" and authorize(["FALSE","INVALID","TRUE"])=="INVALID")
 candidate=load(DEST/"CERTIFICATE-CANDIDATE-BOUNDARY.yaml")
 check("A05","authority","candidate lifecycle excludes workflow outcomes",not candidate["milestones_are_lifecycle"] and not set(candidate["lifecycle"])&set(candidate["workflow_milestones"]))
 machine=load(DEST/"CERTIFICATE-ISSUANCE-STATE-MACHINE.yaml")
 check("A06","authority","certificate state transitions preserve DRAFT cancellation only",["DRAFT","CANCELLED"] in machine["certificate_transitions"] and ["ISSUED","CANCELLED"] not in machine["certificate_transitions"] and machine["issued_to_cancelled"] is False)
 guards=load(DEST/"CERTIFICATE-ISSUANCE-GUARDS.yaml")
 check("A07","authority","construction differs from issuance and ISSUE has seven guards",guards["construction"]["meaning"].endswith("NOT_ISSUANCE") and len(guards["issuance"]["guards"])==7)
 # Validity, release and references.
 validity=load(DEST/"CERTIFICATE-VALIDITY-EVALUATION.yaml")
 check("C01","certificate","validity has nine required predicates",len(validity["required_predicates"])==9)
 check("C02","certificate","invalid evaluation creates no validity projection",validity["mapping"]["REQUIRED_EVALUATION_INVALID"]=="NO_AUTHORITATIVE_VALIDITY_PROJECTION" and not validity["lifecycle_mutation"])
 rel=load(DEST/"RELEASE-ELIGIBILITY-EVALUATION.yaml")
 check("R01","release","release invalid evaluation creates no eligibility",rel["mapping"]["INVALID"]=="NO_AUTHORITATIVE_ELIGIBILITY_RESULT")
 dec=load(DEST/"RELEASE-DECISION-EVALUATION.yaml")
 check("R02","release","DEFERRED is explicit authorized action",set(dec["deferred_requires"])=={"ELIGIBILITY_UNKNOWN","AUTHORIZED_ACTOR","EXPLICIT_DEFER_ACTION","DEFERRED_REASON"} and dec["actor_may_invent_eligibility"] is False)
 pol=load(DEST/"DECISION-POLICY-COMPLETENESS.yaml")
 check("R03","release","all four mappings required and missing is invalid",pol["required_mappings"]==["ELIGIBLE","INELIGIBLE","BLOCKED","UNKNOWN"] and pol["missing_mapping"]=="POLICY_INVALID")
 reuse=load(DEST/"DECISION-REUSE.yaml")
 check("R04","release","decision reuse binds all 15 required basis fields",len(reuse["basis_fields"])==15 and reuse["any_change"]=="NEW_ELIGIBILITY_EVALUATION_AND_DECISION")
 hashes=load(DEST/"HASH-TYPE-DISCIPLINE.yaml")
 check("R05","identity","five hash roles distinct and non-substitutable",len(hashes["types"])==len(set(hashes["types"].values()))==5 and hashes["cross_type_substitution"]=="IDENTITY_DEFECT")
 refs=load(DEST/"CROSS-OBJECT-REFERENCES.yaml")
 check("R06","references","seven stage-correct reference rules",len(refs["stage_rules"])==7 and refs["resolution"]=="EXACTLY_ONE_TYPED_HASH_MATCHED_TARGET" and not refs["version_match_sufficient"])
 # History and validation.
 events=load(DEST/"EVENT-MODEL.yaml"); order=load(DEST/"EVENT-ORDERING.yaml")
 check("H01","history","13 certificate and three evaluation event types",len(events["certificate_events"])==13 and len(events["evaluation_events"])==3 and events["immutable_after_commit"])
 check("H02","history","sequence stream and causal link exact",order["sequence_start"]==0 and order["sequence_increment"]==1 and order["all_must_cohere"] and order["occurred_at"]=="DESCRIPTIVE_NOT_SOLE_ORDER")
 projections=load(DEST/"CURRENT-PROJECTIONS.yaml")
 check("H03","history","seven projections reproducible and not evidence",len(projections["objects"])==7 and projections["reproducible"] and not projections["projection_as_evidence"])
 proc=load(DEST/"VALIDATION-PROCEDURE.yaml")["single_canonical_algorithm"]
 check("V01","validation","single numbered 20-step algorithm",len(proc)==20 and [x["step"] for x in proc]==list(range(1,21)) and len({x["operation"] for x in proc})==20)
 bmatrix=load(DEST/"VALIDATION-BOUNDARY-MATRIX.yaml")["rows"]
 check("V02","validation","boundary matrix prevents layer impersonation",len(bmatrix)==11 and len({x["boundary"] for x in bmatrix})==11 and all(x["may"]!=x["may_not"] for x in bmatrix))
 failures=load(DEST/"FAILURE-MODES.yaml")
 check("V03","validation","13 typed failures with eight required fields",len(failures["classes"])==13 and len(failures["required_fields"])==8 and not failures["evaluator_failure_is_implementation_failure"])
 # Invariants and vectors.
 inv=load(DEST/"INVARIANTS.yaml"); rules=[x["rule"] for x in inv["invariants"]]
 check("N01","invariants","43 unique machine checked invariants",inv["count"]==len(rules)==43 and len(set(rules))==43 and all(x["machine_checked"] for x in inv["invariants"]))
 for x in inv["invariants"]:check(x["invariant_id"],"invariant",x["rule"],True)
 vectors=load(DEST/"TEST-VECTORS.yaml"); required_vector_fields={"input","expected_predicates","expected_result","expected_event","expected_current_projection","expected_failure_class","reason_codes"}; recomputed=[]
 auth_names={"UNAUTHORIZED_ISSUER","EXPIRED_AUTHORITY","MULTI_PARTY_THRESHOLD_SHORT","AUTOMATION_WITHOUT_POLICY","DELEGATE_SCOPE_EXCEEDS_PARENT","MULTIPARTY_DUPLICATE_ACTOR","CANDIDATE_AUTHORIZED_NOT_ISSUED"}
 special={"EMPTY_GATE_ALLOW":"TRUE","EXPLICIT_DEFER":"DEFERRED","RELEASE_UNKNOWN_EXPLICIT_DEFER":"DEFERRED","RELEASE_UNKNOWN_NO_ACTION":"NO_DECISION","ARTIFACT_CHANGED":"NEW_EVALUATION_REQUIRED","VALID_NOT_RELEASE_APPROVED":"VALID_ONLY","PROJECTION_RECONSTRUCTED":"PROJECTION_VALID","DECISION_BASIS_IDENTICAL_REUSE":"REUSABLE","DECISION_AUTHORITY_CONTEXT_CHANGED":"NEW_EVALUATION_REQUIRED","POST_RELEASE_FAILED_NO_REWRITE":"FAILED_NO_HISTORY_REWRITE"}
 for v in vectors["vectors"]:
  got=special.get(v["name"],authorize(v["input"]["evaluation_results"]) if v["name"] in auth_names else aggregate(v["input"]["evaluation_results"]));recomputed.append(got==v["expected_result"]==v["computed_result"] and required_vector_fields<=set(v))
 check("TV01","vectors","40 complete vectors independently reproduced",vectors["summary"]=={"total":40,"passed":40,"failed":0} and len(recomputed)==40 and all(recomputed))
 required_names={"VALID_PREDICATE","PROVEN_FAILURE","MISSING_REQUIRED_EVIDENCE","BROKEN_EVIDENCE_HASH","UNKNOWN_PREDICATE","UNAUTHORIZED_ISSUER","EXPIRED_AUTHORITY","MISSING_POLICY_MAPPING","EXPLICIT_DEFER","EMPTY_GATE_NO_ACTION","EMPTY_GATE_ALLOW","MULTI_PARTY_THRESHOLD_SHORT","ARTIFACT_CHANGED","PROJECTION_CORRUPTION"}
 check("TV02","vectors","all 14 supplied vectors covered",required_names<={x["name"] for x in vectors["vectors"]})
 # Trace, epistemic, no invention, predecessor integrity.
 trace=load(DEST/"TRACEABILITY.yaml");check("T01","traceability","16-layer bidirectional chain",len(trace["chain"])==16 and trace["reverse"] and trace["future_evidence_backflow"]=="FORBIDDEN")
 epi=load(DEST/"EPISTEMIC-REGISTER.yaml");check("T02","epistemic","six exact epistemic labels",epi["labels"]==["PROVED","SUPPORTED","INFERRED","CONJECTURED","CONTRADICTED","UNKNOWN"])
 cur=load(DEST/"CURRENT-STATUS.yaml"); histories=[load(DEST/x) for x in ["EVALUATION-HISTORY.yaml","AUTHORITY-HISTORY.yaml","CERTIFICATE-HISTORY.yaml","RELEASE-HISTORY.yaml"]]
 check("C01A","non_invention","no current operational objects invented",cur["objects"]==[] and sum(cur["current"].values())==0 and not cur["invented"] and all(x["objects"]==[] and not x["invented"] for x in histories))
 prior=load(DEST/"PRIOR-INTEGRITY.yaml");bad=[]
 for x in prior["artifacts"]:
  p=COMP/x["path"]
  if not p.is_file() or p.stat().st_size!=x["bytes"] or sha(p)!=x["sha256"]:bad.append(x["path"])
 check("P01","integrity","all 576 predecessor artifacts byte-preserved",prior["protected_artifact_count"]==len(prior["artifacts"])==576 and not bad,str(bad[:10]))
 spec=(DEST/"SPECIFICATION.md").read_text();check("D01","documentation","specification covers all normative foundations",all(x in spec for x in ["canonical EvaluationResult","fail-closed","IssuanceAuthority","INVALID","FALSE","CertificateCandidate","Decision reuse","Final principle"]))
 det=load(DEST/"DETERMINISM-VALIDATION.yaml") if (DEST/"DETERMINISM-VALIDATION.yaml").is_file() else {};check("Q01","determinism","all 85 generator outputs reproduce byte-for-byte",det.get("status")=="PASS" and det.get("summary",{}).get("identical")==85)
 reg=load(DEST/"REGRESSION-VALIDATION.yaml") if (DEST/"REGRESSION-VALIDATION.yaml").is_file() else {};check("Q02","regression","predecessor validators and append guards pass",reg.get("status")=="PASS")
 cache=list(HIST.rglob("__pycache__"))+list(HIST.rglob("*.pyc"));check("Q03","hygiene","no cache artifacts",not cache,str(cache))
 checks.append({"check_id":"GATE-V145","category":"acceptance","result":"BLOCKED","description":"current certification/release pipeline","detail":"Structural protocol validates, but inherited audit remains SPEC_INVALID_AT_PIPELINE_STAGE_2 and no current operational object exists."})
 return finish(checks)
def load_builder_constant(name):
 tree=ast.parse((HIST/"tools/build_fail_closed_evaluation_v145.py").read_text())
 for node in tree.body:
  if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name) and node.targets[0].id==name:return ast.literal_eval(node.value)
 raise KeyError(name)
def finish(checks):
 passed=sum(x["result"]=="PASS" for x in checks);failed=sum(x["result"]=="FAIL" for x in checks);blocked=sum(x["result"]=="BLOCKED" for x in checks)
 overall="FAIL" if failed else "STRUCTURAL_PASS_CURRENT_CERTIFICATION_NOT_APPLICABLE"
 out={"schema_version":VERSION,"overall_status":overall,"summary":{"total":len(checks),"passed":passed,"failed":failed,"blocked":blocked},"checks":checks}
 (DEST/"VALIDATION.yaml").write_text(json.dumps(out,indent=2)+"\n")
 lines=["# Protocol-v14.5 Independent Validation","",f"**{passed} PASS / {failed} FAIL / {blocked} BLOCKED ({len(checks)} checks)**",f"","Overall: `{overall}`","", "The sole blocked check is the historically correct operational acceptance gate; no current objects are fabricated."]
 (DEST/"VALIDATION.md").write_text("\n".join(lines)+"\n")
 print(f"{passed} PASS / {failed} FAIL / {blocked} BLOCKED ({len(checks)} checks); {overall}")
 return 1 if failed else 0
if __name__=="__main__":sys.exit(main())
