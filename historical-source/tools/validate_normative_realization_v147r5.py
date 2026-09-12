#!/usr/bin/env python3
"""Independent structural and semantic validator for v14.7-R5."""
import hashlib
import json
import re
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HISTORICAL = ROOT / "historical-source"
COMPLIANCE = HISTORICAL / "compliance"
BASE = COMPLIANCE / "certification/v14.7-R5"
TOOLS = HISTORICAL / "tools"
sys.path.insert(0, str(TOOLS))
from run_v147r5_normative import run

EXPECTED_ENUMS = {
    "Evaluation":["TRUE","FALSE","UNKNOWN","BLOCKED","INVALID"],"Validation":["VALID","INVALID","BLOCKED","UNKNOWN"],"Conformance":["CONFORMANT","PARTIALLY_CONFORMANT","NON_CONFORMANT","UNVERIFIED","BLOCKED","NOT_APPLICABLE","UNKNOWN"],"CertificateLifecycle":["DRAFT","ISSUED","REVOKED","SUPERSEDED","EXPIRED","CANCELLED"],"CertificateValidity":["VALID","INVALID","NOT_YET_VALID","UNKNOWN"],"ReleaseEligibility":["ELIGIBLE","INELIGIBLE","BLOCKED","UNKNOWN"],"Authorization":["AUTHORIZED","REFUSED","BLOCKED","UNKNOWN","INVALID"],"ReleaseDecision":["APPROVED","REJECTED","BLOCKED","DEFERRED"],"ReleaseExecution":["NOT_STARTED","STARTED","SUCCEEDED","FAILED","CANCELLED","ROLLED_BACK"],"PostReleaseVerification":["NOT_STARTED","IN_PROGRESS","PASSED","FAILED","INCONCLUSIVE","BLOCKED","INVALID"],"Reuse":["REUSABLE","NOT_REUSABLE","BLOCKED","UNKNOWN","INVALID"],"Authority":["ACTIVE","SUSPENDED","REVOKED","EXPIRED","UNKNOWN"],"AuthorityQualification":["QUALIFIED","NOT_QUALIFIED","BLOCKED","UNKNOWN","INVALID"],"EventValidation":["VALID","INVALID","BLOCKED","UNKNOWN"],"EventCommit":["PENDING","COMMITTED","REJECTED"],"Projection":["CURRENT","REPLAYING","STALE","INVALID","BLOCKED","UNKNOWN"],"RequirementLifecycle":["PROPOSED","DRAFT","ACTIVE","DEPRECATED","SUPERSEDED","RETIRED"],"FindingLifecycle":["OPEN","TRIAGED","ROOT_CAUSE_IDENTIFIED","REMEDIATION_PLANNED","REMEDIATION_IN_PROGRESS","READY_FOR_REVERIFICATION","REVERIFICATION_IN_PROGRESS","RESOLVED","WAIVED","REJECTED","CLOSED"],"Remediation":["PLANNED","APPROVED","IN_PROGRESS","BLOCKED","READY_FOR_VERIFICATION","VERIFIED","FAILED","CANCELLED","SUPERSEDED"],"NormativeStrength":["MUST","MUST_NOT","SHOULD","SHOULD_NOT","MAY"]}
EXPECTED_ERRORS = ["INVALID_PREDICATE","INVALID_SUBJECT","INVALID_CONTEXT","VALIDATION_REQUIRED","VALIDATION_FAILED","UNSUPPORTED_PREDICATE","EVALUATOR_FAILURE","EVALUATOR_TIMEOUT","EVALUATOR_RESOURCE_FAILURE","EVALUATOR_INTERNAL_FAILURE","OUTPUT_INVALID","EVALUATOR_DEPENDENCY_UNAVAILABLE"]
EPISTEMIC = {"PROVED","SUPPORTED","INFERRED","CONJECTURED","CONTRADICTED","UNKNOWN"}


def load(path): return json.loads(path.read_text())
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def canonical(value):
    def n(x):
        if isinstance(x,float): raise ValueError
        if isinstance(x,str): return unicodedata.normalize("NFC",x)
        if isinstance(x,list): return [n(v) for v in x]
        if isinstance(x,dict): return {unicodedata.normalize("NFC",k):n(v) for k,v in x.items()}
        return x
    return json.dumps(n(value),sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
def domain_hash(domain,value): return hashlib.sha256(domain.encode("ascii")+b":"+canonical(value)).hexdigest()


def main(base=BASE):
    rows=[]
    def check(identifier, description, condition, blocked=False, detail=None):
        status="BLOCKED" if blocked else ("PASS" if condition else "FAIL")
        rows.append({"check_id":identifier,"description":description,"status":status,"detail":detail})
    documents={}
    parse_errors=[]
    for path in sorted(p for p in base.rglob("*") if p.is_file() and p.suffix in {".yaml", ".json"}):
        try:documents[str(path.relative_to(base))]=load(path)
        except Exception as error:parse_errors.append(f"{path}:{error}")
    check("R5-V-001","All JSON-compatible YAML parses",not parse_errors,detail=parse_errors or None)
    manifest=documents.get("GENERATOR-MANIFEST.yaml",{});declared=manifest.get("paths",[]);actual=sorted(str(p.relative_to(base)) for p in base.rglob("*") if p.is_file())
    check("R5-V-002","Generator manifest count is exact",manifest.get("count")==len(declared)==len(set(declared)))
    check("R5-V-003","Manifest declares every file",set(declared)==set(actual))
    check("R5-V-004","Expected generator-owned artifact count",len(actual)==84,detail={"actual":len(actual)})
    prior=documents.get("PRIOR-INTEGRITY.yaml",{});current_prior=[p for p in COMPLIANCE.rglob("*") if p.is_file() and base not in p.parents]
    check("R5-V-005","Prior integrity count preserves 1,165 files",prior.get("protected_artifact_count")==len(current_prior)==1165)
    indexed={x["path"]:x for x in prior.get("artifacts",[])}
    check("R5-V-006","Every predecessor hash and byte count remains exact",len(indexed)==1165 and all(x in indexed and indexed[x]["sha256"]==sha(COMPLIANCE/x) and indexed[x]["bytes"]==(COMPLIANCE/x).stat().st_size for x in indexed))
    registry=documents.get("CLOSED-ENUM-REGISTRY.yaml",{});domains={x["domain"]:[v["wire"] for v in x["values"]] for x in registry.get("objects",[])}
    check("R5-V-007","Exactly 20 closed domains are registered",registry.get("domain_count")==len(domains)==20)
    check("R5-V-008","All 111 supplied wire states are exact",domains==EXPECTED_ENUMS and registry.get("value_count")==111)
    check("R5-V-009","Every enum has explicit Rust representation",all(x.get("rust_type") and all(v.get("rust") for v in x.get("values",[])) for x in registry.get("objects",[])))
    check("R5-V-010","Every enum rejects extension and wrong-domain values",all(x.get("closed") and x.get("unknown_value_behavior")=="REJECT" and x.get("wrong_domain_behavior")=="REJECT" for x in registry.get("objects",[])))
    check("R5-V-011","Normative strength remains separate",documents.get("NORMATIVE-STRENGTH.yaml",{}).get("values")==EXPECTED_ENUMS["NormativeStrength"] and set(documents["NORMATIVE-STRENGTH.yaml"].get("separate_from",[]))=={"LIFECYCLE","CONFORMANCE"})
    check("R5-V-012","Enum content hashes are valid",all(x.get("content_hash")==domain_hash("closed-enum:v1",{k:v for k,v in x.items() if k!="content_hash"}) for x in registry.get("objects",[])))
    schemas={path:doc for path,doc in documents.items() if path.endswith(".schema.json")}
    normative={p:d for p,d in schemas.items() if p.startswith("normative/")};implementation={p:d for p,d in schemas.items() if p.startswith("implementation/")}
    check("R5-V-013","Exactly 28 normative object schemas exist",len(normative)==28)
    check("R5-V-014","Exactly 6 implementation schemas exist",len(implementation)==6)
    check("R5-V-015","Schema families are physically separated",len(schemas)==34 and not (set(normative)&set(implementation)))
    def recursively_strict(node):
        if isinstance(node, dict):
            if node.get("type") == "object" and (node.get("additionalProperties") is not False or set(node.get("required", [])) - set(node.get("properties", {}))): return False
            return all(recursively_strict(value) for value in node.values())
        if isinstance(node, list): return all(recursively_strict(value) for value in node)
        return True
    check("R5-V-016","Every schema is strict",all(x.get("type")=="object" and recursively_strict(x) for x in schemas.values()))
    check("R5-V-017","Every schema explicitly defines nullability and optional fields",all(set(x.get("x-optional-fields",[]))==set(x["properties"])-set(x["required"]) for x in schemas.values()))
    check("R5-V-018","Every schema defines typed identity/reference behavior",all(x.get("x-identifier-type")=="URI_SAFE_ASCII_DISTINCT_DOMAIN_NEWTYPE" and x.get("x-reference-integrity") for x in schemas.values()))
    check("R5-V-019","Every schema defines cardinality and uniqueness behavior",all(x.get("x-cardinality") and all(not (v.get("type")=="array") or "uniqueItems" in v for v in x["properties"].values()) for x in schemas.values()))
    check("R5-V-020","Every schema defines hash inputs and domain",all(x.get("x-hash-domain") and "content_hash" not in x.get("x-hash-input-fields",[]) and set(x.get("x-hash-input-fields",[]))<=set(x["properties"]) for x in schemas.values()))
    check("R5-V-021","Every schema defines canonical, temporal, scope, integrity rules",all(all(x.get(k) for k in ["x-canonicalization","x-temporal-requirements","x-scope-requirements","x-integrity-requirements"]) for x in schemas.values()))
    check("R5-V-022","Normative schemas carry only normative authority",all(x.get("x-authority-layer")=="NORMATIVE_SPECIFICATION" for x in normative.values()))
    check("R5-V-023","Implementation schemas carry only implementation authority",all(x.get("x-authority-layer")=="IMPLEMENTATION" for x in implementation.values()))
    normative_text="\n".join(json.dumps(x).lower() for x in normative.values());forbidden_tech=[w for w in ["rust","cargo","tokio","sqlite","wasm"] if w in normative_text]
    check("R5-V-024","Normative schemas are technology-neutral",not forbidden_tech,detail=forbidden_tech or None)
    error_doc=documents.get("EVALUATOR-ERROR-TAXONOMY.yaml",{});errors=error_doc.get("objects",[])
    check("R5-V-025","Evaluator-error taxonomy is exact and complete",[x.get("code") for x in errors]==EXPECTED_ERRORS and error_doc.get("count")==12)
    check("R5-V-026","Every error defines retry and mapping metadata",all(all(k in x for k in ["retry_permitted","may_map_unknown","may_map_blocked","may_map_invalid","mapping_requires_explicit_profile_policy"]) for x in errors))
    check("R5-V-027","Every error defines conformance and evidence metadata",all("blocks_mandatory_conformance" in x and "evidence_producing" in x for x in errors))
    check("R5-V-028","Every evaluator error defaults to EVALUATION_FAILURE",all(x.get("default_disposition")=="EVALUATION_FAILURE" for x in errors))
    check("R5-V-029","No evaluator error permits FALSE mapping",all(x.get("may_map_false") is False for x in errors))
    policy=documents.get("EVALUATOR-ERROR-POLICY.yaml",{})
    check("R5-V-030","Error policy forbids silent mapping",policy.get("silent_mapping") is False and policy.get("mapping_requires_explicit_profile_policy") is True and policy.get("false_mapping_permitted") is False)
    conversions=documents.get("RESULT-CONVERSIONS.yaml",{}).get("objects",[])
    check("R5-V-031","Exactly seven named conversion functions exist",len(conversions)==7 and len({x["rule_id"] for x in conversions})==7)
    check("R5-V-032","Generic convert is forbidden",documents.get("RESULT-CONVERSIONS.yaml",{}).get("generic_convert")=="FORBIDDEN")
    check("R5-V-033","Conversions name source, target, evidence, policy, and failure",all(all(k in x for k in ["source_type","source_states","target_type","legal_mappings","forbidden_mappings","required_evidence","applicable_policy","failure_behavior"]) for x in conversions))
    check("R5-V-034","All conversion source states are legal or forbidden",all(set(x["source_states"])==set(x["legal_mappings"])|set(x["forbidden_mappings"]) for x in conversions))
    tests=documents.get("tests/MACHINE-TESTS.yaml",{}).get("objects",[]);testids={x["test_id"] for x in tests}
    conversion_tests=[x for x in tests if x["category"].startswith("CONVERSION")]
    expected_conversion_cases=sum(len(x["legal_mappings"])+len(x["forbidden_mappings"]) for x in conversions)
    check("R5-V-035","Every legal and forbidden conversion mapping is tested",len(conversion_tests)==expected_conversion_cases)
    forbidden=documents.get("FORBIDDEN-CONVERSIONS.yaml",{}).get("objects",[])
    check("R5-V-036","Eleven authority-strengthening conversions are forbidden and tested",len(forbidden)==11 and all(x.get("test_ref") in testids for x in forbidden))
    aggregate=documents.get("AGGREGATION-CONTRACT.yaml",{})
    check("R5-V-037","Aggregation precedence remains FALSE > BLOCKED > UNKNOWN > TRUE",aggregate.get("precedence")==["FALSE","BLOCKED","UNKNOWN","TRUE"])
    check("R5-V-038","Aggregation handles every precondition explicitly",all(aggregate.get(k) for k in ["invalid_before_aggregation","empty_mandatory_action","missing_configuration","optional_predicates","duplicate_same","duplicate_conflict","evaluator_error","stale_evidence","invalid_artifact"]))
    profile=documents.get("R5-PROFILE.yaml",{})
    check("R5-V-039","R5 profile has an explicit allowed empty action",profile.get("empty_mandatory_action") in {"ALLOW","DENY","BLOCK","UNKNOWN"})
    canonical_doc=documents.get("CANONICAL-SERIALIZATION.yaml",{})
    check("R5-V-040","Canonicalization freezes all requested dimensions",all(canonical_doc.get(k) for k in ["field_order","map_order","array_order","numbers","timestamps","unicode","null","encoding","canonical_bytes"]))
    check("R5-V-041","Independent canonicalization normalizes map order and Unicode",canonical({"b":2,"a":"e\u0301"})==canonical({"a":"é","b":2}))
    identities=documents.get("HASH-IDENTITIES.yaml",{}).get("identities",{})
    check("R5-V-042","Seven distinct hash identities are defined",len(identities)==len(set(identities.values()))==7)
    check("R5-V-043","Domain separation changes identity",domain_hash("artifact:v1",{"x":1})!=domain_hash("object:v1",{"x":1}))
    trace=documents.get("CONFORMANCE-TRACEABILITY.yaml",{})
    check("R5-V-044","All conformance edges are typed",len(trace.get("objects",[]))>0 and all(len(x.get("edge_types",[]))==10 and all(x.get(k) for k in ["requirement_ref","acceptance_criterion_ref","profile_binding_ref","implementation_requirement_ref","implementation_mapping_ref","test_ref","observation_ref","evidence_ref","validation_ref","evaluation_ref","conformance_ref"]) for x in trace["objects"]))
    check("R5-V-045","Untyped implements is forbidden",trace.get("untyped_implements")=="FORBIDDEN")
    invariants=documents.get("FORMAL-INVARIANTS.yaml",{}).get("objects",[])
    check("R5-V-046","Invariants I-001 through I-020 are complete and tested",[x["invariant_id"] for x in invariants]==[f"I-{i:03d}" for i in range(1,21)] and all(x.get("test_ref") in testids and x.get("status")=="SATISFIED" for x in invariants))
    contradictions=documents.get("CONTRADICTIONS.yaml",{})
    check("R5-V-047","Contradiction inspection covers required distinctions",contradictions.get("status")=="NO_GENUINE_CONTRADICTION" and len(contradictions.get("inspected",[]))>=12)
    check("R5-V-048","No-new-state conclusion is tied to zero contradictions",contradictions.get("objects")==[] and contradictions.get("conclusion")=="NO NEW SEMANTIC STATE REQUIRED")
    migration=documents.get("MIGRATION-R4-TO-R5.yaml",{})
    check("R5-V-049","R4 to R5 migration requires revalidation and rehashing",migration.get("classification")=="CONVERTIBLE" and {"REVALIDATE_EVALUATOR_ERROR_POLICY","REHASH_WITH_TYPED_DOMAIN"}<=set(migration.get("requires",[])) and migration.get("source_validity_transfers") is False)
    epistemic=documents.get("EPISTEMIC-CONCLUSIONS.yaml",{}).get("objects",[])
    check("R5-V-050","All conclusions use closed epistemic labels",len(epistemic)>0 and all(x.get("status") in EPISTEMIC for x in epistemic))
    rust_root=base/"implementation/rust-types/gde-v147-r5-types";rust_text="\n".join(p.read_text() for p in rust_root.rglob("*.rs"))
    check("R5-V-051","Rust blueprint forbids unsafe and boxed generic errors","#![forbid(unsafe_code)]" in rust_text and "Box<dyn Error>" not in rust_text and "unsafe {" not in rust_text)
    check("R5-V-052","Rust defines every frozen semantic domain distinctly",all(re.search(rf"enum\s+{re.escape(x['rust_type'])}\s*\{{",rust_text) for x in registry.get("objects",[])))
    ids=["RequirementId","ProfileId","PredicateId","EvaluationId","ValidationId","EvidenceId","CertificateId","ReleaseId","DecisionId","EventId","ImplementationId","AuthorityId","SnapshotId","DecisionBasisId"]
    check("R5-V-053","Semantic identifiers are distinct Rust newtypes",all(f"identifier!({x});" in rust_text for x in ids) and "type Id" not in rust_text)
    check("R5-V-054","Rust evaluator boundary returns result or typed error","EvaluationCompletion" in rust_text and "Result(EvaluationResult)" in rust_text and "Error(EvaluatorError)" in rust_text and "pub value: EvaluationValue" in rust_text)
    check("R5-V-055","Rust exposes only named typed conversions","pub fn convert(" not in rust_text and all(name in rust_text for name in ["validation_to_evaluation_eligibility","evaluation_to_predicate_outcome","predicate_outcome_to_aggregate","aggregate_to_release_eligibility","conformance_to_compliance","release_eligibility_to_authorization_input","authorization_to_decision_input"]))
    runtime_rows=run(base);failed_runtime=[x for x in runtime_rows if x["status"]!="PASSED"]
    check("R5-V-056","All 312 self-contained machine tests pass",len(runtime_rows)==312 and not failed_runtime,detail=failed_runtime or None)
    categories={x["category"] for x in tests}
    check("R5-V-057","Test matrix spans all required categories",{"ENUM_LEGAL","ENUM_UNKNOWN","ENUM_WRONG_DOMAIN","BOUNDARY","EVALUATOR_ERROR_DEFAULT","EVALUATOR_ERROR_EXPLICIT","EVALUATOR_ERROR_FORBIDDEN","EVALUATOR_ERROR_POLICY","CONVERSION_LEGAL","CONVERSION_FORBIDDEN","FORBIDDEN_CONVERSION","AGGREGATION","TEMPORAL","INTEGRITY","CANONICAL","INVARIANT"}<=categories)
    error_tests=[x for x in tests if x["category"].startswith("EVALUATOR_ERROR")]
    mapping_cases={(x["input"]["error"],next(iter(x["input"]["policy"]["mappings"].values()))) for x in error_tests if x["category"] in {"EVALUATOR_ERROR_EXPLICIT","EVALUATOR_ERROR_FORBIDDEN"}}
    check("R5-V-058","Every evaluator error and every legal or forbidden disposition is tested",len(error_tests)==63 and mapping_cases=={(error,target) for error in EXPECTED_ERRORS for target in ["UNKNOWN","BLOCKED","INVALID","FALSE"]})
    machine_results=documents.get("MACHINE-TEST-RESULTS.yaml",{}).get("summary",{})
    check("R5-V-059","Persisted machine result summary is exact",machine_results=={"total":312,"passed":312,"failed":0})
    separation=documents.get("LAYER-SEPARATION.yaml",{})
    required_distinct={"NormativeSpecification","NormativeRequirement","ProfileBinding","ProfileRequirement","ImplementationRequirement","ImplementationInstruction","Guidance","Observation","Evidence","ValidationResult","EvaluationResult","EvaluatorError","ConformanceResult","AuthorityQualification","AuthorizationResult","ReleaseExecution","PostReleaseVerification","DerivedTruth"}
    check("R5-V-060","Authority and semantic object layers remain pairwise distinct",separation.get("pairwise_distinct") is True and required_distinct<=set(separation.get("distinct_types",[])) and separation.get("guidance_authority")=="NON_NORMATIVE" and separation.get("observation_authority")=="DESCRIPTIVE_ONLY")
    final=documents.get("FINAL-PRINCIPLE.yaml",{})
    check("R5-V-061","Final principle preserves result/error separation","NO_SILENT_SUBSTITUTION" in final.get("rule",""))
    cargo=shutil.which("cargo")
    if cargo:
        process=subprocess.run([cargo,"test","--locked"],cwd=rust_root,capture_output=True,text=True)
        check("R5-V-062","Rust source compiles and tests",process.returncode==0,detail={"returncode":process.returncode})
    else:
        check("R5-V-062","Rust source compiles and tests",False,blocked=True,detail="RUST_TOOLCHAIN_UNAVAILABLE")
    summary={"pass":sum(x["status"]=="PASS" for x in rows),"fail":sum(x["status"]=="FAIL" for x in rows),"blocked":sum(x["status"]=="BLOCKED" for x in rows)}
    report={"realization_version":"14.7-R5","validator":"validate_normative_realization_v147r5.py","objects":rows,"summary":summary,"result":"FAIL" if summary["fail"] else ("PASS_WITH_BLOCKED_TOOLCHAIN" if summary["blocked"] else "PASS")}
    (base/"INDEPENDENT-VALIDATION.yaml").write_text(json.dumps(report,indent=2)+"\n")
    validation=documents.get("VALIDATION-REPORT.yaml",{})
    validation["status"]="INDEPENDENT_VALIDATION_COMPLETE"
    validation["independent_summary"]=summary
    validation["independent_result"]=report["result"]
    (base/"VALIDATION-REPORT.yaml").write_text(json.dumps(validation,indent=2)+"\n")
    for row in rows: print(f"{row['check_id']} {row['status']} {row['description']}")
    print(f"summary: {summary['pass']} PASS / {summary['fail']} FAIL / {summary['blocked']} BLOCKED")
    return 1 if summary["fail"] else 0

if __name__=="__main__":sys.exit(main())
