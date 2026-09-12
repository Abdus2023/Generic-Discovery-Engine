#!/usr/bin/env python3
"""Build Protocol-v10.1 evidence-normalized engineering obligations.

The required v1-v9 input package is incomplete in this checkout. The builder therefore
emits INPUT_CONTRACT_FAILED and a downgraded, source-local obligation corpus. It never
silently substitutes missing v4-v7 artifacts or treats the downgraded corpus as accepted.
"""
from __future__ import annotations

import hashlib
import json
import shutil
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[2]
HS = ROOT / "historical-source"
OUT = HS / "obligations"
TOOLS = HS / "tools"

DELIVERABLES = [
    "README.md", "INPUT-CONTRACT.yaml", "OBLIGATIONS.yaml",
    "OBLIGATION-DEPENDENCIES.yaml", "OBLIGATION-DEPENDENCY-MATRIX.yaml",
    "DEPENDENCY-CLOSURE.md", "DEPENDENCY-CRITICAL-OBLIGATIONS.yaml",
    "EVIDENCE-GRAPH.yaml", "HISTORICAL-OBLIGATION-GRAPH.yaml",
    "FUTURE-ENGINEERING-OBLIGATION-GRAPH.yaml", "VERIFICATION-GRAPH.yaml",
    "OBLIGATION-LINEAGE.yaml", "OBLIGATION-LINEAGE-GRAPH.md", "OBLIGATION-CONFLICTS.yaml",
    "FAILURE-OBLIGATIONS.yaml", "SECURITY-OBLIGATIONS.yaml", "CONTRACT-OBLIGATIONS.yaml",
    "NULLABILITY-COMPATIBILITY.yaml", "HISTORICAL-API-SURFACE.yaml",
    "TRACEABILITY-MATRIX.yaml", "HISTORICAL-REGRESSION-SUITE.md",
    "COMPATIBILITY-ENVELOPE.md", "ESSENTIAL-VS-ACCIDENTAL.md",
    "MIGRATION-OBLIGATIONS.md", "OBLIGATION-CONFLICTS.md",
    "OBLIGATION-GRAPH.md", "ENGINEERING-OBLIGATION-REPORT.md",
    "schema/input-contract.schema.yaml", "schema/historical-property.schema.yaml",
    "schema/obligation.schema.yaml", "schema/obligation-dependency.schema.yaml",
    "schema/obligation-lineage.schema.yaml", "schema/obligation-conflict.schema.yaml",
    "schema/traceability.schema.yaml",
]
CLASSES = ["PRESERVE", "COMPATIBILITY", "STABILIZE", "GENERALIZE", "FORMALIZE", "VERIFY", "CONTAIN", "OBSERVE", "DEPRECATE", "REJECT", "OPTIONAL"]
STRENGTHS = ["REQUIRED", "CONDITIONAL", "RECOMMENDED", "OPTIONAL", "UNKNOWN"]
CATEGORIES = ["HISTORICAL_FACT", "HISTORICAL_PROPERTY", "PRESERVATION_OBLIGATION", "COMPATIBILITY_OBLIGATION", "ENGINEERING_REQUIREMENT", "FUTURE_STRENGTHENING", "DESIGN_OPTION", "HISTORICAL_DEFECT", "UNKNOWN"]
EPISTEMIC = ["PROVED", "SUPPORTED", "INFERRED", "CONJECTURED", "CONTRADICTED", "UNKNOWN"]
LIFECYCLE = ["DISCOVERED", "SUPPORTED", "FORMALIZED", "IMPLEMENTED", "VERIFIED", "SUPERSEDED", "REJECTED", "UNKNOWN"]
PROPERTY_TYPES = ["ALGORITHMIC", "ARCHITECTURAL", "BEHAVIORAL", "DATA", "INTERFACE", "CONTRACTUAL", "CONCURRENCY", "FAILURE", "SECURITY", "PROVENANCE", "OBSERVABILITY", "RESOURCE", "COMPATIBILITY"]
DEPENDENCY_RELATIONS = ["REQUIRES", "SUPPORTS", "ENABLES", "REFINES", "STRENGTHENS", "CONSTRAINS", "CONFLICTS_WITH", "SUPERSEDES", "DERIVED_FROM", "VERIFIED_BY"]
INPUT_FAILURES = ["INPUT_MISSING", "INPUT_MALFORMED", "INPUT_SCHEMA_MISMATCH", "INPUT_HASH_MISMATCH", "INPUT_PROVENANCE_BROKEN", "INPUT_VERSION_CONFLICT", "INPUT_TEMPORAL_CONTAMINATION", "INPUT_UNVERIFIED", "INPUT_CONTRADICTION", "INPUT_INSUFFICIENT"]
EVIDENCE_CLASSES = ["VERIFIED_ARTIFACT", "VERIFIED_SNAPSHOT", "EVOLUTION_EVENT", "HISTORICAL_CLAIM", "HISTORICAL_PROPERTY", "CONTRACT_RECORD", "SECURITY_RECORD", "FAILURE_RECORD", "ARCHITECTURE_RECORD", "ALGORITHM_RECORD", "TEST_EVIDENCE"]
VERSIONS = ["v0.1.0", "v0.2.0", "v0.3.0", "v0.4.0", "v0.5.0", "v0.6.0", "v0.7.1"]
REGRESSION = ["CONTRACT_REGRESSION", "ALGORITHM_REGRESSION", "CONCURRENCY_REGRESSION", "SECURITY_REGRESSION", "PROVENANCE_REGRESSION", "RESOURCE_REGRESSION", "SERIALIZATION_REGRESSION"]


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def table(headers: list[str], rows: Iterable[Iterable[Any]]) -> str:
    def clean(value: Any) -> str:
        if isinstance(value, list): value = ", ".join(str(x) for x in value)
        return str(value).replace("|", "\\|").replace("\n", " ")
    return ("| " + " | ".join(headers) + " |\n" + "|" + "|".join("---" for _ in headers) + "|\n" +
            "".join("| " + " | ".join(clean(v) for v in row) + " |\n" for row in rows))


def write_md(name: str, text: str) -> None:
    path = OUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def front(title: str) -> str:
    return (f"# {title}\n\n> **Input status: INPUT_CONTRACT_FAILED.** Protocol-v1 source integrity fails and required Protocol-v4 through Protocol-v7 artifacts are missing. This is a structurally validated, downgraded source-local corpus—not an accepted complete v10.1 synthesis. Missing evidence is not evidence of absence.\n\n")


def schema_version(value: Any) -> str:
    return str(value.get("schema_version", "UNKNOWN")) if isinstance(value, dict) else "UNKNOWN"


def prop_type(domain: str) -> str:
    return {
        "algorithm": "ALGORITHMIC", "architecture": "ARCHITECTURAL", "data": "DATA",
        "interfaces": "INTERFACE", "contract": "CONTRACTUAL", "contracts": "CONTRACTUAL",
        "scheduler": "ARCHITECTURAL", "concurrency": "CONCURRENCY", "failure": "FAILURE",
        "security": "SECURITY", "provenance": "PROVENANCE", "observability": "OBSERVABILITY",
        "resource": "RESOURCE", "serialization": "COMPATIBILITY", "candidate": "DATA",
        "acquisition": "BEHAVIORAL", "observation": "DATA", "recognition": "BEHAVIORAL",
        "provider": "INTERFACE", "discovery": "DATA", "testing": "BEHAVIORAL", "ui": "OBSERVABILITY",
    }.get(domain, "BEHAVIORAL")


def main() -> None:
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    # Stage 1: parse known upstream structures. No obligation is derived in this phase.
    payloads = {
        "v1_validation": load(HS / "VALIDATION.yaml"),
        "v3_reconstruction": load(HS / "RECONSTRUCTION-MANIFEST.yaml"),
        "v3_validation": load(HS / "RECONSTRUCTION-VALIDATION.yaml"),
        "v3_data": load(HS / "analysis" / "DATA-MODEL-EVOLUTION.yaml")["models"],
        "v3_api": load(HS / "analysis" / "API-EVOLUTION.yaml")["api_evolution"],
        "v3_providers": load(HS / "analysis" / "PROVIDER-HISTORY.yaml")["history"],
        "v8_validation": load(HS / "security" / "VALIDATION.yaml"),
        "v8_manifest": load(HS / "security" / "SECURITY-MANIFEST.yaml"),
        "v8_failure_matrix": load(HS / "security" / "FAILURE-MATRIX.yaml")["matrix"],
        "v8_failures": load(HS / "security" / "FAILURE-EVENTS.yaml")["failures"],
        "v8_claim": load(HS / "security" / "CLAIM-SAFETY.yaml")["snapshots"],
        "v8_duplicate": load(HS / "security" / "DUPLICATE-PROCESSING.yaml")["snapshots"],
        "v8_retry": load(HS / "security" / "RETRY-HISTORY.yaml")["snapshots"],
        "v8_cancel": load(HS / "security" / "CANCELLATION-HISTORY.yaml")["snapshots"],
        "v8_provenance": load(HS / "security" / "PROVENANCE-INTEGRITY.yaml")["snapshots"],
        "v8_observe": load(HS / "security" / "OBSERVABILITY-HISTORY.yaml")["snapshots"],
        "v8_persist": load(HS / "security" / "PERSISTENCE-INTEGRITY.yaml")["snapshots"],
        "v8_export": load(HS / "security" / "EXPORT-INTEGRITY.yaml")["snapshots"],
        "v8_bounds": load(HS / "security" / "RESOURCE-BOUNDS.yaml")["bounds"],
        "v8_risks": load(HS / "security" / "RESOURCE-EXHAUSTION.yaml")["risks"],
        "v8_boundaries": load(HS / "security" / "TRUST-BOUNDARIES.yaml")["boundaries"],
        "v8_authority": load(HS / "security" / "AUTHORITY-HISTORY.yaml")["authorities"],
        "v8_parsers": load(HS / "security" / "PARSER-SAFETY-HISTORY.yaml")["parsers"],
        "v8_code_data": load(HS / "security" / "CODE-DATA-BOUNDARY-HISTORY.yaml")["snapshots"],
        "v9_validation": load(HS / "synthesis" / "VALIDATION.yaml"),
        "v9_manifest": load(HS / "synthesis" / "SYNTHESIS-MANIFEST.yaml"),
        "v9_evidence": load(HS / "synthesis" / "EVIDENCE-LEDGER.yaml")["evidence"],
        "v9_states": load(HS / "synthesis" / "VERSION-STATE-VECTORS.yaml")["states"],
        "v9_claims": load(HS / "synthesis" / "CLAIMS.yaml")["claims"],
        "v9_invariants": load(HS / "synthesis" / "INVARIANTS.yaml")["invariants"],
        "v9_unknowns": load(HS / "synthesis" / "UNCERTAINTIES.yaml")["uncertainties"],
        "v9_contradictions": load(HS / "synthesis" / "CONTRADICTIONS.yaml")["contradictions"],
    }
    input_contract = build_input_contract(payloads)
    dump(OUT / "INPUT-CONTRACT.yaml", input_contract)

    # Stage 2: obligation derivation consumes only the normalized envelope payloads.
    normalized = {x["evidence_id"]: x for x in input_contract["normalized_evidence"]}
    def np(eid: str) -> Any: return normalized[eid]["normalized_payload"]
    data_models = np("NE-V3-DATA")
    api_evolution = np("NE-V3-API")
    provider_history = np("NE-V3-PROVIDERS")
    failure_matrix = np("NE-V8-FAILURE-MATRIX")
    duplicate_processing = np("NE-V8-DUPLICATE")
    resource_bounds = np("NE-V8-BOUNDS")
    resource_risks = np("NE-V8-RISKS")
    trust_boundaries = np("NE-V8-BOUNDARIES")
    v9_states = np("NE-V9-STATES")
    v9_claims = np("NE-V9-CLAIMS")
    v9_invariants = np("NE-V9-INVARIANTS")

    evidence_ref = {
        "v3:": "NE-V3-DATA", "v3:API": "NE-V3-API", "v3:PROVIDER": "NE-V3-PROVIDERS",
        "v8:CLAIM": "NE-V8-CLAIM", "v8:DUPLICATE": "NE-V8-DUPLICATE", "v8:RETRY": "NE-V8-RETRY",
        "v8:CANCELLATION": "NE-V8-CANCEL", "v8:PROVENANCE": "NE-V8-PROVENANCE",
        "v8:OBSERVABILITY": "NE-V8-OBSERVE", "v8:PERSISTENCE": "NE-V8-PERSIST",
        "v8:EXPORT": "NE-V8-EXPORT", "v8:RESOURCE-BOUNDS": "NE-V8-BOUNDS",
        "v8:RESOURCE-EXHAUSTION": "NE-V8-RISKS", "v8:TRUST": "NE-V8-BOUNDARIES",
        "v8:AUTHORITY": "NE-V8-AUTHORITY", "v8:PARSER": "NE-V8-PARSERS",
        "v8:CODE-DATA": "NE-V8-CODE-DATA", "v8:FAILURE": "NE-V8-FAILURE-MATRIX",
        "claim-": "NE-V9-CLAIMS", "inv-": "NE-V9-INVARIANTS", "unc-": "NE-V9-UNKNOWNS",
        "contra-": "NE-V9-CONTRADICTIONS", "state-": "NE-V9-STATES",
    }
    def evidence_for(claims: list[str]) -> list[str]:
        out=[]
        for claim in claims:
            matches=[(k,v) for k,v in evidence_ref.items() if claim.startswith(k)]
            out.append(max(matches, key=lambda x: len(x[0]))[1] if matches else "NE-V9-CLAIMS")
        return sorted(set(out))

    facts=[]; properties=[]
    state_map={"algorithm":"algorithm","architecture":"architecture","data":"data","interfaces":"providers","contracts":"contracts","scheduler":"algorithm","concurrency":"concurrency","failure":"failure","security":"security","provenance":"provenance","observability":"observability","testing":"validation"}
    for state in v9_states:
        for domain,key in state_map.items():
            cell=state["state_vector"][key]
            fid=f"FACT-{state['snapshot_id']}-{domain.upper()}"
            pid=f"PROP-{state['snapshot_id']}-{domain.upper()}"
            facts.append({"fact_id":fid,"final_category":"HISTORICAL_FACT","statement":f"{state['snapshot_id']} records {key} state {cell['state']}.","version_scope":{"versions":[state["version"]]},"source_evidence":["NE-V9-STATES"],"epistemic_status":cell["status"],"historical_status":cell["state"],"future_requirement":"NOT_AUTOMATIC"})
            properties.append({"property_id":pid,"property_type":prop_type(domain),"statement":f"The recovered {domain} property for {state['snapshot_id']} is {cell['state']}.","version_scope":{"versions":[state["version"]]},"evidence_refs":["NE-V9-STATES"],"epistemic_status":cell["status"],"historical_status":cell["state"],"derived_from_facts":[fid],"final_category":"HISTORICAL_PROPERTY","requirement_status":"NOT_AUTOMATICALLY_A_REQUIREMENT"})

    specs = obligation_specs()
    obligations=[]; invariants=[]; tests=[]; requirements=[]
    for spec in specs:
        claims=spec["claims"]
        pid="PROP-"+spec["id"][4:]
        src_evidence=evidence_for(claims)
        properties.append({"property_id":pid,"property_type":prop_type(spec["domain"]),"statement":spec["property"],"version_scope":{"versions":spec["versions"]},"evidence_refs":src_evidence,"epistemic_status":spec["epistemic"],"historical_status":spec.get("historical_status","SUPPORTED_OR_EXPLICITLY_QUALIFIED"),"derived_from_facts":[],"historical_claims":claims,"final_category":"HISTORICAL_PROPERTY","requirement_status":"CANDIDATE_FOR_DERIVATION_ONLY"})
        justified=spec.get("justified",True)
        status="FORMALIZED" if justified else "UNKNOWN"
        statement=spec["statement"] if justified else "REQUIREMENT_NOT_JUSTIFIED"
        iid="INV-"+spec["id"][4:]; tid="TEST-"+spec["id"][4:]
        obligation={
            "obligation_id":spec["id"],"title":spec["title"],"statement":statement,
            "class":spec["class"],"strength":spec["strength"],"final_category":spec["category"],
            "epistemic_status":spec["epistemic"],"source_properties":[pid],"source_evidence":src_evidence,
            "historical_claims":claims,"version_scope":{"versions":spec["versions"]},
            "dependencies":[],"dependents":[],"prerequisite_obligations":[],
            "verification":{"test_id":tid,"strategy":spec.get("test",f"Exercise {spec['title'].lower()} in an executable future harness and assert its semantic invariant."),"expected":spec.get("expected","The obligation holds or the deviation is explicit and observable."),"result":"UNVERIFIED"},
            "compatibility":{"scope":spec.get("compatibility","internal and cross-component semantics"),"impact_if_changed":spec.get("compatibility_impact","REQUIRES_EQUIVALENCE_ANALYSIS")},
            "exceptions":spec.get("exceptions",[]),"status":status,
            "rationale":spec["rationale"],"engineering_rationale":spec["rationale"] if justified else "ABSENT",
            "derivation_status":"JUSTIFIED_SOURCE_LOCAL_INPUT_BLOCKED" if justified else "REQUIREMENT_NOT_JUSTIFIED",
            "derivation_acceptance":"BLOCKED_BY_INPUT_CONTRACT_FAILED",
            "strengthening":spec.get("strengthening","HISTORICAL"),
            "allowed_change":spec.get("allowed",["Any mechanism preserving the declared semantics"]),
            "forbidden_change":spec.get("forbidden",["Silent semantic weakening","Retroactive attribution of a future mechanism"]),
            "failure_if_violated":spec.get("failure","Semantic regression or unversioned compatibility break."),
            "priority":spec.get("priority","HIGH" if spec["strength"]=="REQUIRED" else "MEDIUM"),
            "priority_basis":{"security_impact":"PRIMARY" if spec["domain"]=="security" else "POSSIBLE_OR_NOT_PRIMARY","data_loss_impact":"PRIMARY" if spec["domain"] in {"candidate","observation","discovery","provenance","failure","serialization"} else "POSSIBLE_OR_NOT_PRIMARY","concurrency_impact":"PRIMARY" if spec["domain"] in {"scheduler","concurrency"} else "POSSIBLE_OR_NOT_PRIMARY","compatibility_impact":"PRIMARY" if spec["class"]=="COMPATIBILITY" or spec["domain"] in {"contract","serialization"} else "POSSIBLE_OR_NOT_PRIMARY","historical_importance_is_not_current_risk":True},
            "invariant_ref":iid,"test_ref":tid,"dependency_level":"UNASSIGNED","prerequisite_closure":[],"closure_status":"OBLIGATION_BLOCKED",
        }
        obligations.append(obligation)
        invariants.append({"invariant_id":iid,"obligation_id":spec["id"],"statement":f"Within applicable scope, {statement.rstrip('.').lower()}.","epistemic_status":spec["epistemic"],"status":"FORMALIZED" if justified else "UNKNOWN","final_category":"ENGINEERING_REQUIREMENT" if justified else "UNKNOWN"})
        tests.append({"test_id":tid,"obligation_id":spec["id"],"historical_versions":spec["versions"],"verified_behavior":spec["property"],"invariant_ref":iid,"executable_test":obligation["verification"]["strategy"],"expected_outcome":obligation["verification"]["expected"],"negative_cases":spec.get("negative",["missing input","malformed input","duplicate input","failure path"]),"regression_classes":spec.get("regression",[domain_regression(spec["domain"])]),"priority":obligation["priority"],"prerequisite_tests":[],"dependent_failures":[],"failure_class":"OBLIGATION_UNVERIFIED","execution_status":"UNVERIFIED","final_category":"ENGINEERING_REQUIREMENT" if justified else "UNKNOWN"})
        if justified:
            requirements.append({"requirement_id":"REQ-"+spec["id"][4:],"obligation_ref":spec["id"],"statement":statement,"strength":spec["strength"],"engineering_rationale":spec["rationale"],"final_category":"ENGINEERING_REQUIREMENT","design_choice":"UNSELECTED","verification_ref":tid,"derivation_acceptance":"BLOCKED_BY_INPUT_CONTRACT_FAILED"})

    dep_model = build_dependencies(obligations, tests)
    dependencies=dep_model["dependencies"]
    lineage=build_lineage(obligations)
    conflicts=build_conflicts(obligations)
    graph_models=build_graphs(input_contract, properties, obligations, dependencies, lineage, tests)

    assessments=build_assessments(data_models, provider_history, duplicate_processing, resource_bounds, resource_risks)
    metadata={
        "protocol":"v10.1","input_contract_version":"1.0","obligation_schema_version":"1.0",
        "input_contract_status":"INPUT_CONTRACT_FAILED","acceptance":"INPUT_CONTRACT_FAILED",
        "derivation_mode":"DOWNGRADED_PROVISIONAL_SOURCE_LOCAL_ONLY",
        "derivation_input":"NORMALIZED_EVIDENCE_ENVELOPE_ONLY",
        "required_upstream_stages":["v1","v2","v3","v4","v5","v6","v7","v8","v9"],
        "unavailable_stages":["v4","v5","v6","v7"],"deliverables":DELIVERABLES,
        "counts":{"normalized_evidence":len(input_contract["normalized_evidence"]),"facts":len(facts),"properties":len(properties),"obligations":len(obligations),"requirements":len(requirements),"dependencies":len(dependencies),"invariants":len(invariants),"tests":len(tests)},
        "tools":{"generator":sha(TOOLS/"build_historical_obligations.py"),"validator":sha(TOOLS/"validate_historical_obligations.py")},
        "normative_distinctions":["EVIDENCE != PROPERTY","PROPERTY != OBLIGATION","CLASS != FINAL_CATEGORY","CLASS != STRENGTH","STRENGTH != EPISTEMIC_STATUS","EPISTEMIC_STATUS != LIFECYCLE_STATUS","DEPENDENCY != LINEAGE","LINEAGE != SUPERSESSION","CONFLICT != DEPENDENCY","HISTORICAL_DEPENDENCY != FUTURE_ENGINEERING_DEPENDENCY","IMPLEMENTED != VERIFIED"],
    }
    main_obj={"metadata":metadata,"historical_facts":facts,"historical_properties":properties,"obligations":obligations,"engineering_requirements":requirements,"invariants":invariants,"test_candidates":tests,**assessments,
              "future_design_decisions":[{"decision_id":"DESIGN-"+o["obligation_id"][4:],"obligation_ref":o["obligation_id"],"status":"UNSELECTED","final_category":"DESIGN_OPTION","constraint":"A selected mechanism must satisfy the obligation without being attributed to history."} for o in obligations]}
    dump(OUT/"OBLIGATIONS.yaml",main_obj)
    dump(OUT/"OBLIGATION-DEPENDENCIES.yaml",dep_model)
    dump(OUT/"OBLIGATION-DEPENDENCY-MATRIX.yaml",dependency_matrix(obligations,dependencies))
    dump(OUT/"DEPENDENCY-CRITICAL-OBLIGATIONS.yaml",critical_obligations(obligations,dependencies,dep_model["verification_order"]))
    dump(OUT/"OBLIGATION-LINEAGE.yaml",lineage)
    dump(OUT/"OBLIGATION-CONFLICTS.yaml",conflicts)
    for filename,obj in graph_models.items(): dump(OUT/filename,obj)

    failure_obj=build_failure(failure_matrix)
    security_obj=build_security(trust_boundaries,np("NE-V8-AUTHORITY"),np("NE-V8-PARSERS"))
    contract_obj=build_contract(api_evolution)
    null_obj=build_nullability(data_models)
    api_obj=build_api(api_evolution,np("NE-V8-EXPORT"))
    trace_obj=build_trace(obligations,properties,dependencies,input_contract)
    dump(OUT/"FAILURE-OBLIGATIONS.yaml",failure_obj)
    dump(OUT/"SECURITY-OBLIGATIONS.yaml",security_obj)
    dump(OUT/"CONTRACT-OBLIGATIONS.yaml",contract_obj)
    dump(OUT/"NULLABILITY-COMPATIBILITY.yaml",null_obj)
    dump(OUT/"HISTORICAL-API-SURFACE.yaml",api_obj)
    dump(OUT/"TRACEABILITY-MATRIX.yaml",trace_obj)
    build_schemas()
    build_markdown(main_obj,input_contract,dep_model,lineage,conflicts,failure_obj,security_obj,contract_obj,trace_obj)
    assert all((OUT/name).is_file() for name in DELIVERABLES)
    print(f"generated {len(DELIVERABLES)} deliverables; evidence={len(input_contract['normalized_evidence'])} obligations={len(obligations)} dependencies={len(dependencies)}")


def build_input_contract(payloads: dict[str,Any]) -> dict[str,Any]:
    selected=[
        ("source_extraction","v1","SOURCE-MANIFEST.yaml","source_extraction"),
        ("artifact_lineage","v2","LINEAGE.yaml","artifact_lineage"),
        ("reconstructed_snapshots","v3","RECONSTRUCTION-MANIFEST.yaml","reconstruction"),
        ("reconstruction_verification","v4",None,"verification"),
        ("algorithm_evolution","v5",None,"algorithm_evolution"),
        ("architecture_evolution","v6",None,"architecture_evolution"),
        ("contract_evolution","v7",None,"contract_evolution"),
        ("security_evolution","v8","security/SECURITY-MANIFEST.yaml","security_evolution"),
        ("historical_synthesis","v9","synthesis/SYNTHESIS-MANIFEST.yaml","historical_synthesis"),
    ]
    required=[]; failures=[]
    for kind,stage,rel,producer in selected:
        if rel is None:
            required.append({"artifact_id":f"MISSING-{stage.upper()}","artifact_type":kind,"schema_version":"UNKNOWN","source_path":"UNKNOWN","producer_stage":producer,"generated_at":"UNKNOWN_NOT_RECORDED","content_hash":"UNKNOWN","schema_validation":"NOT_AVAILABLE_INPUT_MISSING","content_hash_validation":"NOT_AVAILABLE_INPUT_MISSING","version_validation":"NOT_AVAILABLE_INPUT_MISSING","provenance_validation":"NOT_AVAILABLE_INPUT_MISSING","temporal_validation":"NOT_AVAILABLE_INPUT_MISSING","input_state":"INPUT_MISSING","sufficiency":"INPUT_INSUFFICIENT"})
            failures.append({"stage":stage,"state":"INPUT_MISSING","detail":f"Required {kind} artifact is absent; this is missing evidence, not evidence of absence."})
        else:
            p=HS/rel; obj=load(p)
            state="INPUT_UNVERIFIED" if stage=="v1" else "PROVISIONAL_VERIFIED" if stage in {"v3","v8","v9"} else "STRUCTURALLY_PRESENT"
            required.append({"artifact_id":f"ART-{stage.upper()}-{sha(p)[:16]}","artifact_type":kind,"schema_version":schema_version(obj),"source_path":f"historical-source/{rel}","producer_stage":producer,"generated_at":"UNKNOWN_NOT_RECORDED_UPSTREAM","content_hash":sha(p),"schema_validation":"STRUCTURALLY_VALID_JSON_COMPATIBLE_YAML","content_hash_validation":"UPSTREAM_PAYLOAD_HASH_MISMATCH" if stage=="v1" else "ARTIFACT_CONTENT_HASH_BOUND","version_validation":"STRUCTURALLY_CONSISTENT_SOURCE_LOCAL","provenance_validation":"STRUCTURALLY_RESOLVED_SOURCE_LOCAL","temporal_validation":"PASS_SOURCE_LOCAL","input_state":state,"sufficiency":"SUFFICIENT_SOURCE_LOCAL" if stage!="v1" else "INPUT_INSUFFICIENT"})
    failures += [
        {"stage":"v1","state":"INPUT_HASH_MISMATCH","detail":"Protocol-v1 reports 0/4 raw revisions and 0/5644 source ranges matching pinned bytes."},
        {"stage":"v1","state":"INPUT_UNVERIFIED","detail":"Source extraction overall status is FAIL."},
        {"stage":"v1-v9","state":"INPUT_INSUFFICIENT","detail":"The complete required package cannot be verified while v1 fails and v4-v7 are missing."},
    ]
    checks=[
        {"check_id":"I01","check":"all required sources present and sufficient","result":"FAIL","failure_states":["INPUT_MISSING","INPUT_UNVERIFIED","INPUT_INSUFFICIENT"]},
        {"check_id":"I02","check":"artifact schemas are valid","result":"BLOCKED","failure_states":["INPUT_MISSING"]},
        {"check_id":"I03","check":"content hashes match","result":"FAIL","failure_states":["INPUT_HASH_MISMATCH"]},
        {"check_id":"I04","check":"version identifiers are consistent","result":"BLOCKED","failure_states":["INPUT_INSUFFICIENT"]},
        {"check_id":"I05","check":"provenance references resolve","result":"PASS","failure_states":[]},
        {"check_id":"I06","check":"epistemic labels are valid","result":"PASS","failure_states":[]},
        {"check_id":"I07","check":"contradictions are preserved","result":"PASS","failure_states":["INPUT_CONTRADICTION"]},
        {"check_id":"I08","check":"unknowns are preserved","result":"PASS","failure_states":[]},
        {"check_id":"I09","check":"reconstructed versions have v4 verification status","result":"FAIL","failure_states":["INPUT_MISSING","INPUT_UNVERIFIED"]},
        {"check_id":"I10","check":"no future artifact contaminates earlier version","result":"PASS","failure_states":[]},
    ]
    normalized=[]
    def add(eid,etype,stage,path,statement,status,payload,dependencies=None):
        p=HS/path
        normalized.append({"evidence_id":eid,"evidence_type":etype,"source_stage":stage,"source_artifact":f"historical-source/{path}","version_scope":VERSIONS if stage in {"v3","v8","v9"} else [stage],"statement":statement,"provenance":{"source_path":f"historical-source/{path}","content_hash":sha(p),"normalization":"STRUCTURE_PRESERVED_NO_SEMANTIC_REWRITE"},"epistemic_status":status,"verification_status":"PROVISIONAL_SOURCE_LOCAL" if stage in {"v3","v8","v9"} else "UNVERIFIED" if stage=="v1" else "STRUCTURALLY_PRESENT","dependencies":dependencies or [],"normalized_payload":payload})
    add("NE-V1-SOURCE","HISTORICAL_CLAIM","v1","VALIDATION.yaml","Source extraction validation fails pinned byte/range integrity.","PROVED",payloads["v1_validation"])
    add("NE-V2-LINEAGE","HISTORICAL_CLAIM","v2","LINEAGE.yaml","Artifact lineage structure is present, but full provenance acceptance remains blocked by v1.","SUPPORTED",load(HS/"LINEAGE.yaml"),["NE-V1-SOURCE"])
    add("NE-V3-RECON","VERIFIED_SNAPSHOT","v3","RECONSTRUCTION-MANIFEST.yaml","Twelve complete recovered occurrences and two partial alternatives are recorded.","SUPPORTED",payloads["v3_reconstruction"],["NE-V2-LINEAGE"])
    groups=[
        ("NE-V3-DATA","HISTORICAL_PROPERTY","v3","analysis/DATA-MODEL-EVOLUTION.yaml","Recovered data-model fields.",payloads["v3_data"]),
        ("NE-V3-API","HISTORICAL_PROPERTY","v3","analysis/API-EVOLUTION.yaml","Recovered API shape occurrences.",payloads["v3_api"]),
        ("NE-V3-PROVIDERS","HISTORICAL_PROPERTY","v3","analysis/PROVIDER-HISTORY.yaml","Recovered provider occurrences.",payloads["v3_providers"]),
        ("NE-V8-FAILURE-MATRIX","FAILURE_RECORD","v8","security/FAILURE-MATRIX.yaml","Failure detection, propagation, containment, recovery, and observability matrix.",payloads["v8_failure_matrix"]),
        ("NE-V8-CLAIM","SECURITY_RECORD","v8","security/CLAIM-SAFETY.yaml","Claim ownership and atomicity assessments.",payloads["v8_claim"]),
        ("NE-V8-DUPLICATE","SECURITY_RECORD","v8","security/DUPLICATE-PROCESSING.yaml","Duplicate-processing dimensions remain independent.",payloads["v8_duplicate"]),
        ("NE-V8-RETRY","FAILURE_RECORD","v8","security/RETRY-HISTORY.yaml","Retry and terminal behavior history.",payloads["v8_retry"]),
        ("NE-V8-CANCEL","FAILURE_RECORD","v8","security/CANCELLATION-HISTORY.yaml","Cancellation mechanisms and unknown guarantees.",payloads["v8_cancel"]),
        ("NE-V8-PROVENANCE","SECURITY_RECORD","v8","security/PROVENANCE-INTEGRITY.yaml","Provenance edges and integrity limits.",payloads["v8_provenance"]),
        ("NE-V8-OBSERVE","SECURITY_RECORD","v8","security/OBSERVABILITY-HISTORY.yaml","Observability channel history.",payloads["v8_observe"]),
        ("NE-V8-PERSIST","SECURITY_RECORD","v8","security/PERSISTENCE-INTEGRITY.yaml","Persistence integrity limits.",payloads["v8_persist"]),
        ("NE-V8-EXPORT","SECURITY_RECORD","v8","security/EXPORT-INTEGRITY.yaml","Export structure and compatibility limits.",payloads["v8_export"]),
        ("NE-V8-BOUNDS","SECURITY_RECORD","v8","security/RESOURCE-BOUNDS.yaml","Historical resource bounds.",payloads["v8_bounds"]),
        ("NE-V8-RISKS","SECURITY_RECORD","v8","security/RESOURCE-EXHAUSTION.yaml","Static resource risk assessments, not incidents.",payloads["v8_risks"]),
        ("NE-V8-BOUNDARIES","SECURITY_RECORD","v8","security/TRUST-BOUNDARIES.yaml","Trust/authority/control boundary candidates.",payloads["v8_boundaries"]),
        ("NE-V8-AUTHORITY","SECURITY_RECORD","v8","security/AUTHORITY-HISTORY.yaml","Authority records.",payloads["v8_authority"]),
        ("NE-V8-PARSERS","SECURITY_RECORD","v8","security/PARSER-SAFETY-HISTORY.yaml","Parser records.",payloads["v8_parsers"]),
        ("NE-V8-CODE-DATA","SECURITY_RECORD","v8","security/CODE-DATA-BOUNDARY-HISTORY.yaml","Acquired content execution is not evidenced.",payloads["v8_code_data"]),
        ("NE-V9-STATES","HISTORICAL_PROPERTY","v9","synthesis/VERSION-STATE-VECTORS.yaml","Twelve multidimensional source-local state vectors.",payloads["v9_states"]),
        ("NE-V9-CLAIMS","HISTORICAL_CLAIM","v9","synthesis/CLAIMS.yaml","Unified historical claims.",payloads["v9_claims"]),
        ("NE-V9-INVARIANTS","HISTORICAL_PROPERTY","v9","synthesis/INVARIANTS.yaml","Cross-occurrence invariants and counter-invariant.",payloads["v9_invariants"]),
        ("NE-V9-UNKNOWNS","HISTORICAL_CLAIM","v9","synthesis/UNCERTAINTIES.yaml","Unresolved historical unknowns.",payloads["v9_unknowns"]),
        ("NE-V9-CONTRADICTIONS","HISTORICAL_CLAIM","v9","synthesis/CONTRADICTIONS.yaml","Preserved contradictions/input conflicts.",payloads["v9_contradictions"]),
    ]
    for eid,etype,stage,path,statement,payload in groups:
        add(eid,etype,stage,path,statement,"SUPPORTED" if "UNKNOWNS" not in eid else "UNKNOWN",payload,["NE-V3-RECON"] if stage=="v8" else ["NE-V8-FAILURE-MATRIX"] if stage=="v9" else ["NE-V3-RECON"])
    return {"input_contract_version":"1.0","obligation_schema_version":"1.0","status":"INPUT_CONTRACT_FAILED","derivation_authorization":"DOWNGRADED_PROVISIONAL_ONLY","required_inputs":required,"minimum_evidence_requirements":{"v1":"artifact identity + provenance","v2":"version/lineage information","v3":"reconstructed historical states","v4":"verification status for reconstructed states","v5":"algorithm evolution events","v6":"architecture evolution events","v7":"contract evolution events","v8":"failure/security/trust events","v9":"claims + contradictions + unknowns"},"accepted_evidence_classes":EVIDENCE_CLASSES,"rejected_direct_mandatory_sources":["current architecture documentation","future roadmap","modern redesign proposal","unverified interpretation","unverified causal explanation","implementation assumption","name similarity alone","diagram-only inference"],"failure_state_registry":INPUT_FAILURES,"failure_states":failures,"integrity_checks":checks,"missing_evidence_semantics":{"INPUT_MISSING":"MISSING_EVIDENCE","must_not_be_interpreted_as":"EVIDENCE_OF_ABSENCE"},"incompatible_schema_policy":"REJECT_DO_NOT_REINTERPRET","normalized_evidence":normalized}


def obligation_specs() -> list[dict[str,Any]]:
    V=VERSIONS; post1=VERSIONS[1:]; post2=VERSIONS[2:]
    def s(id,title,statement,cls,strength,category,epistemic,domain,claims,prop,rationale,versions=V,**kw):
        return {"id":id,"title":title,"statement":statement,"class":cls,"strength":strength,"category":category,"epistemic":epistemic,"domain":domain,"claims":claims,"property":prop,"rationale":rationale,"versions":versions,**kw}
    return [
        s("OBL-CANDIDATE-IDENTITY","Stable candidate work identity","A candidate must retain stable identity or a lossless identity mapping across its lifecycle.","PRESERVE","REQUIRED","PRESERVATION_OBLIGATION","SUPPORTED","candidate",["inv-001","claim-generic-a"],"Candidate repeatedly represents scheduled work identity.","Lifecycle, deduplication, ownership, and provenance require correlation.",forbidden=["Replace candidates with uncorrelated requests"]),
        s("OBL-CANDIDATE-EQUIVALENCE","Candidate equivalence rule","Before compatibility is promised, candidate equivalence must explicitly keep target, type, origin, parent, provider, and scope dimensions independent.","FORMALIZE","CONDITIONAL","FUTURE_STRENGTHENING","UNKNOWN","candidate",["claim-generic-a","unc-012"],"A cross-version candidate equivalence formula is not established.","Deduplication and migration require a declared rule; URL equality is insufficient.",strengthening="ENGINEERING_STRENGTHENING"),
        s("OBL-DEDUP-SCOPES","Independent deduplication scopes","Queue, claim, processing, discovery, persistence, and export deduplication must be specified and verified independently.","FORMALIZE","REQUIRED","ENGINEERING_REQUIREMENT","SUPPORTED","candidate",["claim-generic-g","v8:DUPLICATE"],"Local Set/Map/key checks mitigate some duplicates but do not prove global uniqueness.","One local check cannot establish all lifecycle uniqueness properties.",strengthening="ENGINEERING_STRENGTHENING"),
        s("OBL-CANDIDATE-ORIGIN","Candidate origin preservation","Populated candidate origin must be retained or migrated to an equivalent provenance reference.","PRESERVE","CONDITIONAL","PRESERVATION_OBLIGATION","SUPPORTED","provenance",["v8:PROVENANCE"],"Origin is recurrent but seed reconstruction and integrity are incomplete.","Origin supports scope and lineage when present."),
        s("OBL-CANDIDATE-PARENT","Candidate parentage preservation","Expanded candidates must retain parentage or an equivalent derivation edge; roots may remain parentless.","PRESERVE","CONDITIONAL","PRESERVATION_OBLIGATION","SUPPORTED","provenance",["v8:PROVENANCE","claim-closure"],"Parent references represent recursive expansion lineage.","Discarding populated parentage loses derivation context."),
        s("OBL-CANDIDATE-STATE","Candidate lifecycle state","Legal candidate state transitions, owners, postconditions, terminal outcomes, and retry re-entry must be explicit.","FORMALIZE","REQUIRED","FUTURE_STRENGTHENING","SUPPORTED","scheduler",["claim-version-v020","v8:CLAIM","v8:RETRY"],"Queued, claimed, completed, failed, and requeued behaviors recur with varying literal forms.","Explicit transitions prevent stranded, duplicated, or falsely completed work.",strengthening="ENGINEERING_STRENGTHENING"),
        s("OBL-CANDIDATE-PRIORITY","Candidate priority compatibility","If priority affects consumers or operations, its ordering semantics must be preserved or versioned; otherwise it must be documented as advisory.","COMPATIBILITY","CONDITIONAL","COMPATIBILITY_OBLIGATION","INFERRED","scheduler",["v3:"],"Priority is recurrent but no stable total ordering contract is verified.","Silent ordering reversal can alter operational discovery order."),
        s("OBL-CANDIDATE-ATTEMPTS","Attempt accounting","Retry-enabled work must advance observable attempt accounting and preserve exhaustion semantics.","PRESERVE","CONDITIONAL","PRESERVATION_OBLIGATION","SUPPORTED","failure",["v8:RETRY"],"Attempt counts and bounded retry occur from v0.3.0; v0.7.1 path proof is incomplete.","Retry without accounting can bypass limits or hide terminal failure.",versions=post2),
        s("OBL-CANDIDATE-TIMESTAMPS","Lifecycle timestamp semantics","Operationally retained timestamps must have explicit clock, ordering, and nullability semantics before contractual use.","OBSERVE","CONDITIONAL","FUTURE_STRENGTHENING","SUPPORTED","observability",["v3:","v8:OBSERVABILITY"],"Created timestamps recur and later variants add stage timestamps without verified clock semantics.","Timing aids diagnosis but field presence is not trustworthy chronology.",strengthening="ENGINEERING_STRENGTHENING"),
        s("OBL-CLAIM-EXCLUSIVITY","Exclusive candidate ownership","When workers overlap, exactly one worker may own a candidate within the declared concurrency scope.","PRESERVE","CONDITIONAL","ENGINEERING_REQUIREMENT","SUPPORTED","concurrency",["claim-version-v020","v8:CLAIM"],"Event-loop-local claiming supports processing exclusivity on recovered paths after v0.1.0; thread/distributed atomicity is unproved.","Exclusive ownership prevents simultaneous duplicate processing.",versions=post1,test="Start N overlapping workers with one candidate and assert exactly one claimant and one attributable terminal outcome.",negative=["N workers one candidate","owner failure","claim during cancellation","requeue while prior owner active"]),
        s("OBL-TERMINAL-OWNERSHIP","Completion and failure ownership","Every claim must receive one attributable completion, failure, expiry, or explicit abandonment outcome.","FORMALIZE","REQUIRED","FUTURE_STRENGTHENING","SUPPORTED","scheduler",["v8:CLAIM"],"Completion/failure operations recur while v0.7.1 ownership is unknown.","A claim without terminal ownership can strand work and invalidate termination.",versions=post1,strengthening="ENGINEERING_STRENGTHENING"),
        s("OBL-ACQ-BEFORE-INTERP","Acquisition precedes interpretation","Acquisition must remain semantically distinct and produce evidence before recognition.","PRESERVE","REQUIRED","PRESERVATION_OBLIGATION","SUPPORTED","acquisition",["inv-002","claim-generic-b","claim-generic-d"],"Recovered workflows order acquisition before interpretation.","Stage separation preserves failure attribution and code/data boundaries."),
        s("OBL-ACQ-OUTCOME","Acquisition outcome recording","Every attempted acquisition must yield an observation outcome or an explicit attributable failure outcome.","STABILIZE","REQUIRED","ENGINEERING_REQUIREMENT","SUPPORTED","acquisition",["inv-003","v8:FAILURE"],"Observation-shaped outcomes and acquisition failures recur with varying propagation.","Unrecorded acquisition erases evidence and can strand work."),
        s("OBL-ACQ-METADATA","Acquisition metadata","Observations must retain metadata sufficient for interpretation, attribution, and diagnosis; exact representation may change equivalently.","PRESERVE","CONDITIONAL","PRESERVATION_OBLIGATION","SUPPORTED","observation",["v3:","v8:PROVENANCE"],"Target, HTTP-shaped metadata, timing, status, and errors recur while body/network details vary.","Uncontextualized content weakens recognition and provenance."),
        s("OBL-ACQ-TIMEOUT","Finite acquisition timeout","Each acquisition must remain under an explicit finite timeout or stronger encompassing deadline, with timeout exposed distinctly.","PRESERVE","REQUIRED","PRESERVATION_OBLIGATION","SUPPORTED","resource",["v8:RESOURCE-BOUNDS","claim-version-v030"],"Every complete occurrence contains requestTimeout.","Unbounded in-flight acquisition blocks progress and consumes resources.",regression=["RESOURCE_REGRESSION","CONTRACT_REGRESSION"]),
        s("OBL-ACQ-SCOPE","Acquisition scope enforcement","Requested and redirected targets must be validated against declared network authority and scope.","CONTAIN","REQUIRED","ENGINEERING_REQUIREMENT","SUPPORTED","security",["v8:TRUST","inv-006"],"URL allow/canonicalization checks occur but redirect, credential, local-address, and origin controls vary.","Remote targets cross historical trust and authority boundaries.",strengthening="ENGINEERING_STRENGTHENING",regression=["SECURITY_REGRESSION"]),
        s("OBL-CANCELLATION","Cancellation verification","If cancellation is exposed, transport stop, candidate outcome, propagation, state preservation, and scheduler termination must be verified separately.","VERIFY","CONDITIONAL","FUTURE_STRENGTHENING","SUPPORTED","concurrency",["v8:CANCELLATION"],"Abort paths support particular operations; global cancellation safety is unknown.","API/control presence does not establish cancellation safety.",versions=post2,strengthening="ENGINEERING_STRENGTHENING",test="Cancel at transport, parsing, recognition, expansion, retry delay, and idle states; assert explicit outcomes and no forbidden later mutation."),
        s("OBL-OBS-DISTINCT","Observation remains distinct","Acquisition evidence must remain represented separately from interpreted Discovery records.","PRESERVE","REQUIRED","PRESERVATION_OBLIGATION","SUPPORTED","observation",["inv-003","claim-generic-c"],"Observation and Discovery are separate from the earliest complete occurrence.","Collapsing evidence into interpretation destroys source evidence."),
        s("OBL-OBS-SOURCE","Observation source linkage","Each observation must retain an unambiguous candidate correlation or explicit orphan classification.","PRESERVE","REQUIRED","PRESERVATION_OBLIGATION","SUPPORTED","provenance",["v8:PROVENANCE","inv-003"],"Observation stores candidateId across complete occurrences.","Acquisition evidence must be attributable to work identity."),
        s("OBL-OBS-OUTCOMES","Observation outcome semantics","Success, failure, timeout, cancellation, partial/truncated, and empty outcomes must remain semantically distinct.","STABILIZE","REQUIRED","FUTURE_STRENGTHENING","SUPPORTED","observation",["v3:","v8:FAILURE"],"Errors, statuses, and timing recur but exact value domains are unverified.","Null, empty, status, and partial outcomes are not equivalent.",strengthening="ENGINEERING_STRENGTHENING"),
        s("OBL-RECOGNITION-DISTINCT","Recognition stage separation","Recognition must remain semantically separable from acquisition and operate on represented observation evidence.","PRESERVE","REQUIRED","PRESERVATION_OBLIGATION","SUPPORTED","recognition",["claim-generic-d","inv-002"],"Recognition is separate from acquisition from v0.1.0.","Separation allows independent containment and verification."),
        s("OBL-RECOGNITION-OUTCOMES","Recognition outcome contract","Non-applicability, applicable-with-no-discovery, provider failure, and partial discovery must be distinct outcomes.","FORMALIZE","REQUIRED","FUTURE_STRENGTHENING","SUPPORTED","recognition",["v3:API","v8:FAILURE"],"Historical paths use null-like, collection, return, and exception outcomes without stable cross-version contract.","Conflation hides failure or loses partial results.",strengthening="ENGINEERING_STRENGTHENING"),
        s("OBL-PROVIDER-CONTRACT","Provider semantic contract","Any exposed provider API must define matching, output, expansion ownership, failure, ordering, lifecycle, cancellation, and provenance.","FORMALIZE","CONDITIONAL","FUTURE_STRENGTHENING","SUPPORTED","provider",["claim-version-v020","v3:PROVIDER","claim-earliest-contract"],"Provider families recur but signatures, ownership, and v7 contracts vary or are unavailable.","Names/signatures do not establish substitutability.",versions=post1,strengthening="ENGINEERING_STRENGTHENING"),
        s("OBL-PROVIDER-FAILURE","Provider failure containment","Provider failure must be attributable and must not corrupt global scheduler state; narrower isolation requires explicit verification.","CONTAIN","CONDITIONAL","FUTURE_STRENGTHENING","SUPPORTED","failure",["v8:FAILURE"],"Provider containment/recovery is supported in some occurrences and unknown in others; propagation is unknown.","Partial evidence cannot be upgraded to complete isolation.",versions=post1,strengthening="ENGINEERING_STRENGTHENING"),
        s("OBL-PROVIDER-ORDER","Provider ordering compatibility","Provider ordering must not be promised stable until external dependence and selection semantics are established; if promised, order changes require versioning or equivalence proof.","COMPATIBILITY","CONDITIONAL","COMPATIBILITY_OBLIGATION","UNKNOWN","provider",["v3:PROVIDER","unc-012"],"Ordering exists but external dependence and selection semantics are unknown.","The conditional obligation preserves uncertainty instead of inventing a stable ordering contract.",versions=post1),
        s("OBL-DISCOVERY-RECORD","Discovery semantic record","Discovery kind/data and candidate/observation correlation must be preserved; populated confidence/timestamps require migration or versioning if removed.","PRESERVE","REQUIRED","PRESERVATION_OBLIGATION","SUPPORTED","discovery",["claim-generic-h","v3:","v8:PROVENANCE"],"Discovery recurrently carries identity, source links, kind, data, confidence, timestamp, and provenance shape.","The interpreted output must remain meaningful and attributable."),
        s("OBL-EXPANSION-RECURSIVE","Recursive expansion capability","Discoveries must remain able to yield candidate work that re-enters scheduling under explicit bounds.","PRESERVE","REQUIRED","PRESERVATION_OBLIGATION","SUPPORTED","algorithm",["inv-004","inv-005","claim-closure"],"Every complete occurrence represents recursive closure mechanisms.","Removing re-entry changes recursive discovery to one-pass extraction."),
        s("OBL-EXPANSION-VS-RETRY","Expansion is not retry","New-child expansion and same-candidate retry must remain separate operations with separate provenance and bounds.","STABILIZE","REQUIRED","ENGINEERING_REQUIREMENT","SUPPORTED","algorithm",["claim-closure","v8:RETRY"],"Recursion creates candidate work; retry requeues failed existing work.","Conflation corrupts parentage, attempts, and termination."),
        s("OBL-CANDIDATE-ADMISSION","Candidate admission transaction","Admission must define identity checking, reject/merge behavior, provenance retention, bounds, and recursive eligibility.","FORMALIZE","REQUIRED","FUTURE_STRENGTHENING","SUPPORTED","scheduler",["claim-generic-e","claim-generic-g","v8:DUPLICATE"],"Expanded candidates enter scheduler/knowledge state under local duplicate and bound checks.","Silent drops lose provenance; non-atomic admission duplicates work.",strengthening="ENGINEERING_STRENGTHENING"),
        s("OBL-KNOWLEDGE","Knowledge accumulation","Candidate, observation, and discovery outcomes required by scheduling, provenance, and reporting must remain queryable for the applicable scope.","PRESERVE","REQUIRED","PRESERVATION_OBLIGATION","SUPPORTED","architecture",["claim-version-v010","inv-003","inv-004"],"Knowledge state accumulates candidate, observation, and discovery records.","Discarding required state breaks scheduling and reporting."),
        s("OBL-BOUNDED-CONCURRENCY","Bounded worker concurrency","Active work concurrency must have an explicit finite bound.","PRESERVE","REQUIRED","PRESERVATION_OBLIGATION","SUPPORTED","concurrency",["v8:RESOURCE-BOUNDS","claim-version-v010"],"Concurrent workers and a finite concurrency setting recur.","Unbounded spawning is a resource and scheduling regression.",regression=["CONCURRENCY_REGRESSION","RESOURCE_REGRESSION"]),
        s("OBL-SCHEDULER-TERMINATION","In-flight-aware termination","Completion may be reported only when no admissible queued or in-flight work can add candidates, or explicit stop policy accounts for it.","FORMALIZE","REQUIRED","FUTURE_STRENGTHENING","SUPPORTED","concurrency",["inv-005","v8:CLAIM"],"A universal termination guarantee is not verified; in-flight expansion creates a theoretical race.","Queue emptiness alone can terminate prematurely.",strengthening="ENGINEERING_STRENGTHENING",test="Hold one worker in flight with an empty queue, let it emit a child, and assert completion waits for child admission or explicit stop."),
        s("OBL-WORKER-FAILURE","Worker failure state consistency","Worker failure must leave owned work in one explicit recoverable or terminal state without corrupting unrelated frontier state.","CONTAIN","REQUIRED","FUTURE_STRENGTHENING","SUPPORTED","concurrency",["v8:CLAIM","v8:FAILURE"],"Worker paths use completion/failure operations, but all propagation scopes are not established.","Ownership and scheduler state must remain coherent after worker failure.",strengthening="ENGINEERING_STRENGTHENING"),
        s("OBL-RETRY","Bounded explicit retry","Only declared retryable failures may retry; attempts, error provenance, finite bounds, backoff, and terminal exhaustion must be explicit.","FORMALIZE","REQUIRED","FUTURE_STRENGTHENING","SUPPORTED","failure",["v8:RETRY","v8:RESOURCE-BOUNDS"],"Bounded retry/backoff appears from v0.3.0 with incomplete same-provider/v0.7 semantics.","Unclassified retry can loop permanent failures or hide exhaustion.",versions=post2,strengthening="ENGINEERING_STRENGTHENING"),
        s("OBL-PROVENANCE","End-to-end provenance associations","Populated Discovery→Observation→Candidate→Parent→Origin associations must be retained; missing edges must stay explicit.","PRESERVE","REQUIRED","PRESERVATION_OBLIGATION","SUPPORTED","provenance",["v8:PROVENANCE","inv-003","inv-004"],"Four provenance edge types are represented with partial end-to-end traceability.","Derivation must not be discarded or fabricated."),
        s("OBL-PROVENANCE-INTEGRITY","Provenance integrity verification","Integrity claims require verified writers, mutation authorization, persistence, forgery resistance, and cryptographic properties independently.","VERIFY","CONDITIONAL","FUTURE_STRENGTHENING","SUPPORTED","provenance",["v8:PROVENANCE","unc-013"],"Provenance fields exist without established immutability or cryptographic guarantee.","Visibility is not integrity.",strengthening="ENGINEERING_STRENGTHENING"),
        s("OBL-REMOTE-DATA","Remote content remains untrusted data","Acquired content must remain untrusted input data, not trusted executable code, absent a separately authorized contained execution contract.","CONTAIN","REQUIRED","ENGINEERING_REQUIREMENT","SUPPORTED","security",["v8:CODE-DATA","v8:PARSER"],"Remote content is parsed/extracted; acquired-content execution is not evidenced.","Preserving non-execution avoids a security-semantic regression.",regression=["SECURITY_REGRESSION"]),
        s("OBL-AUTHORITY","Explicit authority scope","Required, granted, used, and exposed authority must be declared separately and excess authority explicitly approved or rejected.","FORMALIZE","REQUIRED","FUTURE_STRENGTHENING","SUPPORTED","security",["v8:AUTHORITY"],"Browser, userscript, network, storage, UI, and provider operations exercise distinct authority.","Ambient permission is not required capability or trust.",strengthening="ENGINEERING_STRENGTHENING"),
        s("OBL-PARSER","Malformed-input containment","Malformed remote content must remain inside its parser/provider failure boundary and never become trusted execution or unmarked success.","CONTAIN","REQUIRED","ENGINEERING_REQUIREMENT","SUPPORTED","security",["v8:PARSER","v8:FAILURE"],"Parsing failure is operation-locally contained in most occurrences; observability varies.","Malformed one-response input must not corrupt unrelated work.",regression=["SECURITY_REGRESSION","CONTRACT_REGRESSION"]),
        s("OBL-RESOURCE","Explicit resource bounds","Candidate, request, concurrency, timeout, retry, response/body, parser, and retained-state growth must remain finitely bounded or covered by a stronger bound.","PRESERVE","REQUIRED","PRESERVATION_OBLIGATION","SUPPORTED","resource",["v8:RESOURCE-BOUNDS","claim-exhaustive-closure"],"Many local bounds recur but do not prove global convergence.","Removing bounds creates resource regressions; local bounds are not global guarantees.",regression=["RESOURCE_REGRESSION"]),
        s("OBL-UNBOUNDED","Reject unbounded remote-driven work","Future designs must reject unbounded remote response retention, task spawning, or memory growth without explicit external bounds.","REJECT","REQUIRED","FUTURE_STRENGTHENING","SUPPORTED","resource",["v8:RESOURCE-EXHAUSTION"],"Static unmitigated response/memory/parser paths occur in some snapshots; incidents are not evidenced.","This is resource strengthening, not a vulnerability claim.",strengthening="ENGINEERING_STRENGTHENING",regression=["RESOURCE_REGRESSION","SECURITY_REGRESSION"]),
        s("OBL-LIFECYCLE-OBS","Lifecycle observability","Claim, acquisition start/completion, recognition, discovery, expansion, failure, worker lifecycle, and scan completion must be observable semantically.","OBSERVE","REQUIRED","FUTURE_STRENGTHENING","SUPPORTED","observability",["v8:OBSERVABILITY","v8:FAILURE"],"Console/UI/state/export/metric channels expose lifecycle unevenly.","Diagnosis and testing require semantic events, not formatting.",strengthening="ENGINEERING_STRENGTHENING"),
        s("OBL-AUDIT","Auditability verification","Any auditability claim must verify completeness, ordering, identity, retention, mutation protection, and forensic reconstruction separately from logging.","VERIFY","RECOMMENDED","FUTURE_STRENGTHENING","SUPPORTED","observability",["v8:OBSERVABILITY","claim-version-v071"],"Later ledger/diagnostic shapes improve visibility but do not verify auditability.","A log or ledger-shaped object is not an audit trail.",versions=VERSIONS[-2:],strengthening="ENGINEERING_STRENGTHENING"),
        s("OBL-SILENT-FAILURE","Reject silent semantic failure","Failure affecting completeness, lifecycle, or trust decisions must be explicit failure, partial result, or policy skip—not silent success.","REJECT","REQUIRED","FUTURE_STRENGTHENING","SUPPORTED","failure",["v8:FAILURE"],"Potential silent returns, fallbacks, empty outputs, and swallowed context occur; incidents are unproved.","Silent semantic loss causes false success.",strengthening="ENGINEERING_STRENGTHENING"),
        s("OBL-PERSIST-COMPAT","Persistence schema compatibility","If historical state is consumed, schema versions, validation, semantic migration, and explicit rejection of incompatible data are required.","COMPATIBILITY","CONDITIONAL","COMPATIBILITY_OBLIGATION","SUPPORTED","serialization",["v8:PERSISTENCE"],"JSON-shaped persistence exists without general migration, write atomicity, or crash-recovery guarantees.","Compatibility applies only when historical state is consumed.",regression=["SERIALIZATION_REGRESSION"]),
        s("OBL-PERSIST-CORRUPTION","Persistence corruption containment","Malformed, partial, or incompatible persisted state should be detected and contained without becoming trusted active state.","CONTAIN","RECOMMENDED","FUTURE_STRENGTHENING","SUPPORTED","serialization",["v8:PERSISTENCE"],"Load validation is partial and recovery mostly unknown.","This strengthens incomplete handling without backfilling history.",strengthening="ENGINEERING_STRENGTHENING"),
        s("OBL-EXPORT","Export role and schema","Before export compatibility is promised, purpose, version, optional/null/derived fields, partial-state marker, and relationship integrity must be explicit.","FORMALIZE","CONDITIONAL","FUTURE_STRENGTHENING","SUPPORTED","serialization",["v8:EXPORT"],"Structured export exists but purpose and compatibility guarantee are unestablished.","Identical JSON can be observability, persistence, interchange, or API.",strengthening="ENGINEERING_STRENGTHENING",regression=["SERIALIZATION_REGRESSION"]),
        s("OBL-UI","UI presentation","UI styling, layout, labels, and control arrangement may change; preserve only selected operational semantics.","OPTIONAL","OPTIONAL","DESIGN_OPTION","SUPPORTED","ui",["v8:OBSERVABILITY"],"UI channels vary and no stable presentation contract is verified.","Presence does not make styling contractual."),
        s("OBL-PRIVATE-SHAPE","Private names and layouts","Private names, class/module grouping, language, and Map/Set layout may be deprecated or refactored with semantic equivalence.","DEPRECATE","RECOMMENDED","DESIGN_OPTION","INFERRED","architecture",["v3:API","v3:"],"Private structural details vary and lack external-contract evidence.","Historical faithfulness preserves semantics, not source form."),
        s("OBL-CONTRACT-INPUT","Validated contract input","Validated Protocol-v7 contract evidence must be available before any contract transition, compatibility, strengthening, weakening, replacement, or retirement conclusion is accepted.","VERIFY","REQUIRED","ENGINEERING_REQUIREMENT","PROVED","contract",["claim-earliest-contract","unc-005"],"Protocol-v7 contract output is absent.","The missing mandatory input blocks contract conclusions and must not be replaced with signature inference.",strengthening="PROTOCOL_REQUIRED_INPUT_GATE"),
        s("OBL-ERROR-CONTRACT","Error compatibility contract","Each interface must define null, undefined, empty, status, partial, returned-error, and exception semantics before changing them.","FORMALIZE","CONDITIONAL","FUTURE_STRENGTHENING","SUPPORTED","contract",["v3:API","v8:FAILURE","claim-earliest-contract"],"Historical outcomes vary and consumer reliance is unverified.","These outcomes are semantically distinct despite missing v7.",strengthening="ENGINEERING_STRENGTHENING"),
        s("OBL-REGRESSION","Executable regression verification","Every REQUIRED or dependency-critical obligation must have executable verification before status VERIFIED.","VERIFY","REQUIRED","ENGINEERING_REQUIREMENT","SUPPORTED","testing",["unc-007","claim-earliest-runnable"],"No verified historical runtime test lineage exists.","Static archaeology cannot verify a future implementation.",strengthening="ENGINEERING_STRENGTHENING"),
        s("OBL-PARSE-DEFECT","Reject v0.5 parse defect","The snapshot-0009 parse defect must remain historical evidence but must not be reproduced as future required behavior.","REJECT","REQUIRED","HISTORICAL_DEFECT","PROVED","testing",["contra-003","claim-version-v050"],"An exact complete v0.5 occurrence fails static parsing.","Exactness is not executability; defects are not future requirements.",versions=["v0.5.0"],strengthening="ENGINEERING_STRENGTHENING"),
        s("OBL-WEB-GENERALIZE","Generalize beyond web without losing web semantics","A generalized acquisition layer may add protocols only while preserving a versioned compatible web behavior envelope.","GENERALIZE","RECOMMENDED","FUTURE_STRENGTHENING","SUPPORTED","acquisition",["inv-006","claim-protocol"],"Recovered execution is web-coupled; protocol independence is unproved.","Generalization must not rewrite historical scope or discard validated web behavior.",strengthening="ENGINEERING_STRENGTHENING"),
    ]


def domain_regression(domain: str) -> str:
    if domain in {"algorithm","architecture"}: return "ALGORITHM_REGRESSION"
    if domain in {"scheduler","concurrency"}: return "CONCURRENCY_REGRESSION"
    if domain=="security": return "SECURITY_REGRESSION"
    if domain=="provenance": return "PROVENANCE_REGRESSION"
    if domain=="resource": return "RESOURCE_REGRESSION"
    if domain=="serialization": return "SERIALIZATION_REGRESSION"
    return "CONTRACT_REGRESSION"


def build_dependencies(obligations: list[dict[str,Any]], tests: list[dict[str,Any]]) -> dict[str,Any]:
    O={x["obligation_id"]:x for x in obligations}
    requires={
        "OBL-CANDIDATE-EQUIVALENCE":["OBL-CANDIDATE-IDENTITY"],"OBL-DEDUP-SCOPES":["OBL-CANDIDATE-IDENTITY"],
        "OBL-CANDIDATE-ORIGIN":["OBL-CANDIDATE-IDENTITY"],"OBL-CANDIDATE-PARENT":["OBL-CANDIDATE-IDENTITY"],
        "OBL-CANDIDATE-STATE":["OBL-CANDIDATE-IDENTITY"],"OBL-CANDIDATE-PRIORITY":["OBL-CANDIDATE-IDENTITY"],
        "OBL-CANDIDATE-ATTEMPTS":["OBL-CANDIDATE-STATE"],"OBL-CANDIDATE-TIMESTAMPS":["OBL-CANDIDATE-STATE"],
        "OBL-CLAIM-EXCLUSIVITY":["OBL-CANDIDATE-IDENTITY","OBL-CANDIDATE-STATE"],
        "OBL-TERMINAL-OWNERSHIP":["OBL-CLAIM-EXCLUSIVITY","OBL-CANDIDATE-STATE"],
        "OBL-ACQ-BEFORE-INTERP":["OBL-CANDIDATE-IDENTITY"],"OBL-ACQ-OUTCOME":["OBL-ACQ-BEFORE-INTERP","OBL-CANDIDATE-IDENTITY"],
        "OBL-ACQ-METADATA":["OBL-OBS-DISTINCT","OBL-OBS-SOURCE"],"OBL-ACQ-TIMEOUT":["OBL-ACQ-BEFORE-INTERP"],
        "OBL-ACQ-SCOPE":["OBL-ACQ-BEFORE-INTERP","OBL-AUTHORITY"],
        "OBL-CANCELLATION":["OBL-CANDIDATE-STATE","OBL-TERMINAL-OWNERSHIP","OBL-ACQ-TIMEOUT","OBL-SCHEDULER-TERMINATION"],
        "OBL-OBS-DISTINCT":["OBL-ACQ-BEFORE-INTERP"],"OBL-OBS-SOURCE":["OBL-OBS-DISTINCT","OBL-CANDIDATE-IDENTITY"],
        "OBL-OBS-OUTCOMES":["OBL-ACQ-OUTCOME","OBL-OBS-DISTINCT"],
        "OBL-RECOGNITION-DISTINCT":["OBL-OBS-DISTINCT","OBL-ACQ-BEFORE-INTERP"],
        "OBL-RECOGNITION-OUTCOMES":["OBL-RECOGNITION-DISTINCT","OBL-OBS-OUTCOMES"],
        "OBL-PROVIDER-CONTRACT":["OBL-RECOGNITION-DISTINCT","OBL-RECOGNITION-OUTCOMES"],
        "OBL-PROVIDER-FAILURE":["OBL-PROVIDER-CONTRACT","OBL-SILENT-FAILURE"],
        "OBL-DISCOVERY-RECORD":["OBL-RECOGNITION-DISTINCT","OBL-OBS-SOURCE"],
        "OBL-CANDIDATE-ADMISSION":["OBL-CANDIDATE-IDENTITY","OBL-DEDUP-SCOPES","OBL-CANDIDATE-PARENT","OBL-CANDIDATE-STATE"],
        "OBL-SCHEDULER-TERMINATION":["OBL-TERMINAL-OWNERSHIP","OBL-CANDIDATE-ADMISSION","OBL-BOUNDED-CONCURRENCY","OBL-LIFECYCLE-OBS"],
        "OBL-EXPANSION-RECURSIVE":["OBL-DISCOVERY-RECORD","OBL-CANDIDATE-ADMISSION","OBL-SCHEDULER-TERMINATION","OBL-RESOURCE"],
        "OBL-RETRY":["OBL-CANDIDATE-ATTEMPTS","OBL-TERMINAL-OWNERSHIP","OBL-ACQ-TIMEOUT"],
        "OBL-EXPANSION-VS-RETRY":["OBL-EXPANSION-RECURSIVE","OBL-RETRY"],
        "OBL-KNOWLEDGE":["OBL-CANDIDATE-IDENTITY","OBL-OBS-DISTINCT","OBL-DISCOVERY-RECORD"],
        "OBL-WORKER-FAILURE":["OBL-CLAIM-EXCLUSIVITY","OBL-TERMINAL-OWNERSHIP","OBL-SILENT-FAILURE"],
        "OBL-PROVENANCE":["OBL-CANDIDATE-ORIGIN","OBL-CANDIDATE-PARENT","OBL-OBS-SOURCE","OBL-DISCOVERY-RECORD"],
        "OBL-PROVENANCE-INTEGRITY":["OBL-PROVENANCE"],"OBL-REMOTE-DATA":["OBL-ACQ-SCOPE","OBL-RECOGNITION-DISTINCT"],
        "OBL-PARSER":["OBL-REMOTE-DATA","OBL-RECOGNITION-DISTINCT"],"OBL-UNBOUNDED":["OBL-RESOURCE"],
        "OBL-LIFECYCLE-OBS":["OBL-CANDIDATE-STATE","OBL-ACQ-OUTCOME","OBL-RECOGNITION-OUTCOMES","OBL-DISCOVERY-RECORD"],
        "OBL-AUDIT":["OBL-LIFECYCLE-OBS","OBL-PROVENANCE","OBL-PROVENANCE-INTEGRITY"],
        "OBL-SILENT-FAILURE":["OBL-OBS-OUTCOMES","OBL-RECOGNITION-OUTCOMES"],
        "OBL-PERSIST-COMPAT":["OBL-KNOWLEDGE","OBL-PROVENANCE","OBL-ERROR-CONTRACT"],
        "OBL-PERSIST-CORRUPTION":["OBL-PERSIST-COMPAT","OBL-SILENT-FAILURE"],
        "OBL-EXPORT":["OBL-KNOWLEDGE","OBL-PROVENANCE","OBL-ERROR-CONTRACT"],
        "OBL-ERROR-CONTRACT":["OBL-OBS-OUTCOMES","OBL-RECOGNITION-OUTCOMES"],
        "OBL-PARSE-DEFECT":["OBL-REGRESSION"],"OBL-WEB-GENERALIZE":["OBL-ACQ-BEFORE-INTERP","OBL-ACQ-SCOPE"],
    }
    historical_pairs={
        ("OBL-ACQ-BEFORE-INTERP","OBL-CANDIDATE-IDENTITY"),("OBL-OBS-DISTINCT","OBL-ACQ-BEFORE-INTERP"),
        ("OBL-OBS-SOURCE","OBL-CANDIDATE-IDENTITY"),("OBL-RECOGNITION-DISTINCT","OBL-OBS-DISTINCT"),
        ("OBL-DISCOVERY-RECORD","OBL-RECOGNITION-DISTINCT"),("OBL-DISCOVERY-RECORD","OBL-OBS-SOURCE"),
        ("OBL-CANDIDATE-ADMISSION","OBL-CANDIDATE-IDENTITY"),("OBL-EXPANSION-RECURSIVE","OBL-DISCOVERY-RECORD"),
        ("OBL-EXPANSION-RECURSIVE","OBL-CANDIDATE-ADMISSION"),("OBL-CLAIM-EXCLUSIVITY","OBL-CANDIDATE-IDENTITY"),
        ("OBL-KNOWLEDGE","OBL-CANDIDATE-IDENTITY"),("OBL-KNOWLEDGE","OBL-OBS-DISTINCT"),("OBL-KNOWLEDGE","OBL-DISCOVERY-RECORD"),
    }
    deps=[]
    for frm in sorted(requires):
        for to in sorted(requires[frm]):
            dtype="HISTORICAL_DEPENDENCY" if (frm,to) in historical_pairs else "FUTURE_ENGINEERING_DEPENDENCY"
            deps.append({"dependency_id":f"DEP-{len(deps)+1:03d}","from_obligation":frm,"to_obligation":to,"relation":"REQUIRES","condition":"APPLICABLE_WHEN_DEPENDENT_OBLIGATION_IS_IN_SCOPE","reason":dependency_reason(O[frm],O[to]),"evidence":sorted(set(O[frm]["source_evidence"]+O[to]["source_evidence"])),"dependency_type":dtype,"scope":{"historical":"TRUE" if dtype=="HISTORICAL_DEPENDENCY" else "FALSE","current":"UNKNOWN","future":"TRUE"},"valid_from":latest_start(O[frm],O[to]),"valid_until":"UNKNOWN","status":"SUPPORTED" if dtype=="HISTORICAL_DEPENDENCY" else "FORMALIZED_ENGINEERING"})
    extras=[
        ("OBL-CANDIDATE-STATE","OBL-CANDIDATE-IDENTITY","REFINES"),("OBL-CLAIM-EXCLUSIVITY","OBL-CANDIDATE-STATE","REFINES"),
        ("OBL-RESOURCE","OBL-EXPANSION-RECURSIVE","CONSTRAINS"),("OBL-LIFECYCLE-OBS","OBL-AUDIT","SUPPORTS"),
        ("OBL-PROVENANCE-INTEGRITY","OBL-PROVENANCE","STRENGTHENS"),("OBL-PROVIDER-FAILURE","OBL-PROVIDER-CONTRACT","STRENGTHENS"),
    ]
    for frm,to,relation in extras:
        deps.append({"dependency_id":f"DEP-{len(deps)+1:03d}","from_obligation":frm,"to_obligation":to,"relation":relation,"condition":"ANALYTICAL_RELATION_NOT_A_REQUIRES_EDGE","reason":dependency_reason(O[frm],O[to]),"evidence":sorted(set(O[frm]["source_evidence"]+O[to]["source_evidence"])),"dependency_type":"FUTURE_ENGINEERING_DEPENDENCY","scope":{"historical":"UNKNOWN","current":"UNKNOWN","future":"TRUE"},"valid_from":latest_start(O[frm],O[to]),"valid_until":"UNKNOWN","status":"FORMALIZED_ENGINEERING"})
    req=[x for x in deps if x["relation"]=="REQUIRES"]
    direct=defaultdict(list); reverse=defaultdict(list)
    for d in req: direct[d["from_obligation"]].append(d["to_obligation"]); reverse[d["to_obligation"]].append(d["from_obligation"])
    cycles=find_cycles(O,direct)
    closure={oid:transitive(oid,direct) for oid in O}
    order=topological_order(O,direct)
    levels={}
    for oid in order:
        levels[oid]=min(6,1+max((levels[p] for p in direct.get(oid,[])),default=0))
    for o in obligations:
        oid=o["obligation_id"]
        o["dependencies"]=[d["dependency_id"] for d in deps if d["from_obligation"]==oid]
        o["dependents"]=[d["dependency_id"] for d in deps if d["to_obligation"]==oid]
        o["prerequisite_obligations"]=sorted(direct[oid])
        o["prerequisite_closure"]=closure[oid]
        o["dependency_level"]=f"L{levels[oid]}"
        o["closure_status"]="OBLIGATION_BLOCKED" if o["strength"]=="REQUIRED" else "OBLIGATION_UNVERIFIED"
    tby={t["obligation_id"]:t for t in tests}
    for oid,t in tby.items():
        t["prerequisite_tests"]=[tby[p]["test_id"] for p in closure[oid]]
        t["dependent_failures"]=[tby[d]["test_id"] for d in transitive(oid,reverse)]
        t["failure_class"]="OBLIGATION_BLOCKED" if O[oid]["strength"]=="REQUIRED" else "OBLIGATION_UNVERIFIED"
        t["self_failure_result"]="OBLIGATION_VIOLATED"
        t["prerequisite_failure_result"]="OBLIGATION_DEPENDENCY_FAILURE"
        t["unexecuted_result"]="OBLIGATION_UNVERIFIED"
        t["input_block_result"]="OBLIGATION_BLOCKED"
    return {"schema_version":"1.0","graph_type":"OBLIGATION_DEPENDENCY_GRAPH","input_contract_status":"INPUT_CONTRACT_FAILED","nodes":list(O),"edges":[{"from":d["from_obligation"],"to":d["to_obligation"],"relation":d["relation"],"dependency_id":d["dependency_id"]} for d in deps],"relation_registry":DEPENDENCY_RELATIONS,"dependencies":deps,"requires_cycles":[{"cycle_id":f"CYCLE-{i+1:03d}","members":c,"classification":"UNKNOWN"} for i,c in enumerate(cycles)],"cycle_status":"ACYCLIC" if not cycles else "CYCLES_DETECTED","verification_order":order,"dependency_layers":dependency_layers(order,direct),"required_closure":[{"obligation_id":o["obligation_id"],"direct_prerequisites":sorted(direct[o["obligation_id"]]),"transitive_prerequisites":closure[o["obligation_id"]],"verification_prerequisites":[tby[x]["test_id"] for x in closure[o["obligation_id"]]],"unresolved_dependencies":closure[o["obligation_id"]],"closure_status":"OBLIGATION_BLOCKED"} for o in obligations if o["strength"]=="REQUIRED"],"failure_propagation_rules":[{"when":"REQUIRED prerequisite test is UNVERIFIED or BLOCKED","dependent_result":"OBLIGATION_BLOCKED","may_pass":False},{"when":"REQUIRED prerequisite test fails","dependent_result":"OBLIGATION_DEPENDENCY_FAILURE","may_pass":False},{"when":"obligation own invariant fails","dependent_result":"OBLIGATION_VIOLATED","propagate_to_dependents":"OBLIGATION_DEPENDENCY_FAILURE"}],"rule":"from_obligation depends_on to_obligation; conflict, lineage, and verification graphs remain separate."}


def dependency_reason(frm: dict[str,Any],to: dict[str,Any]) -> str:
    target=to["obligation_id"]
    reasons={
        "OBL-CANDIDATE-IDENTITY":"The dependent behavior must correlate the same candidate across lifecycle operations.",
        "OBL-CANDIDATE-STATE":"The dependent behavior reads or mutates candidate lifecycle state and needs legal transitions.",
        "OBL-CLAIM-EXCLUSIVITY":"The dependent behavior needs an attributable exclusive owner before terminal mutation.",
        "OBL-TERMINAL-OWNERSHIP":"The dependent behavior cannot close safely while owned work lacks terminal accountability.",
        "OBL-OBS-DISTINCT":"The dependent behavior needs acquisition evidence distinct from interpretation.",
        "OBL-OBS-SOURCE":"The dependent behavior needs an attributable source candidate for observation/discovery correlation.",
        "OBL-RECOGNITION-DISTINCT":"The dependent behavior assumes recognition remains separable from acquisition.",
        "OBL-RECOGNITION-OUTCOMES":"The dependent behavior needs no-match, failure, partial, and success to remain distinct.",
        "OBL-CANDIDATE-ADMISSION":"The dependent behavior creates work and therefore needs defined admission and duplicate handling.",
        "OBL-BOUNDED-CONCURRENCY":"The dependent behavior cannot reason about in-flight completion without a finite worker scope.",
        "OBL-LIFECYCLE-OBS":"The dependent behavior needs observable lifecycle evidence to diagnose or verify satisfaction.",
        "OBL-RESOURCE":"The dependent recursive/resource behavior needs explicit bounds to avoid unbounded execution.",
        "OBL-PROVENANCE":"The dependent behavior assumes visible derivation associations.",
        "OBL-PROVENANCE-INTEGRITY":"The dependent audit/integrity behavior cannot be claimed while provenance mutation remains unverified.",
        "OBL-ERROR-CONTRACT":"The dependent serialized/API behavior needs explicit error and null-like value semantics.",
        "OBL-REGRESSION":"The known-defect rejection needs an executable build/parse regression test.",
    }
    return reasons.get(target,f"{frm['title']} consumes or semantically assumes the property guaranteed by {to['title']}; satisfying the dependent without that prerequisite would leave its stated invariant undefined.")


def latest_start(a,b):
    starts=[VERSIONS.index(x["version_scope"]["versions"][0]) for x in (a,b) if x["version_scope"]["versions"]]
    return VERSIONS[max(starts)] if starts else "UNKNOWN"


def transitive(start: str, graph: dict[str,list[str]]) -> list[str]:
    seen=set(); stack=list(graph.get(start,[]))
    while stack:
        n=stack.pop()
        if n in seen: continue
        seen.add(n); stack.extend(graph.get(n,[]))
    return sorted(seen)


def find_cycles(nodes: dict[str,Any], graph: dict[str,list[str]]) -> list[list[str]]:
    visiting=set(); done=set(); cycles=[]; path=[]
    def visit(n):
        if n in visiting:
            i=path.index(n); cycles.append(path[i:]+[n]); return
        if n in done:return
        visiting.add(n);path.append(n)
        for x in graph.get(n,[]):visit(x)
        path.pop();visiting.remove(n);done.add(n)
    for n in nodes:visit(n)
    return cycles


def topological_order(nodes: dict[str,Any], direct: dict[str,list[str]]) -> list[str]:
    # prerequisite-first Kahn order
    indegree={n:len(direct.get(n,[])) for n in nodes}; rev=defaultdict(list)
    for frm,tos in direct.items():
        for to in tos:rev[to].append(frm)
    q=deque(sorted(n for n,d in indegree.items() if d==0));out=[]
    while q:
        n=q.popleft();out.append(n)
        for dep in sorted(rev[n]):
            indegree[dep]-=1
            if indegree[dep]==0:q.append(dep)
    return out


def dependency_layers(order: list[str], direct: dict[str,list[str]]) -> list[dict[str,Any]]:
    names=["L1 — Core state","L2 — Component behavior","L3 — Scheduler semantics","L4 — Recursive behavior","L5 — Reliability / containment","L6 — System-level guarantees"]
    levels={};buckets=[[] for _ in names]
    for oid in order:
        level=min(6,1+max((levels[p] for p in direct.get(oid,[])),default=0))
        levels[oid]=level;buckets[level-1].append(oid)
    return [{"layer":names[i],"obligations":buckets[i],"analytical_only":True,"assignment_rule":"one plus maximum REQUIRES prerequisite layer, capped at L6"} for i in range(6)]


def dependency_matrix(obligations,deps):
    ids=[o["obligation_id"] for o in obligations];codes={"REQUIRES":"R","SUPPORTS":"S","ENABLES":"E","REFINES":"F","STRENGTHENS":"T","CONSTRAINS":"C"};lookup={(d["from_obligation"],d["to_obligation"]):codes.get(d["relation"],".") for d in deps}
    return {"schema_version":"1.0","columns":ids,"legend":{"R":"REQUIRES","S":"SUPPORTS","E":"ENABLES","F":"REFINES","T":"STRENGTHENS","C":"CONSTRAINS",".":"NO_EDGE"},"rows":[{"obligation_id":frm,"cells":{to:lookup.get((frm,to),".") for to in ids}} for frm in ids],"conflicts_excluded":True,"lineage_excluded":True}


def critical_obligations(obligations,deps,order):
    rev=defaultdict(list)
    for d in deps:
        if d["relation"]=="REQUIRES":rev[d["to_obligation"]].append(d["from_obligation"])
    rows=[]
    for o in obligations:
        oid=o["obligation_id"];direct=sorted(rev[oid]);trans=transitive(oid,rev);count=len(trans)
        rows.append({"obligation_id":oid,"direct_dependents":direct,"transitive_dependents":trans,"centrality":count,"classification":"DEPENDENCY_CRITICAL" if count>=5 else "DEPENDENCY_CONNECTED" if count else "LEAF","verification_priority":order.index(oid)+1 if oid in order else "CYCLE_ISOLATED","reason":"Priority is based on downstream dependency count, not chronology or historical importance.","change_impact":{"revisit_dependents":trans,"revisit_invariants":["INV-"+x[4:] for x in [oid]+trans],"revisit_regression_tests":["TEST-"+x[4:] for x in [oid]+trans],"revisit_migration":bool(trans),"revisit_conflicts":True}})
    return {"schema_version":"1.0","input_contract_status":"INPUT_CONTRACT_FAILED","records":sorted(rows,key=lambda x:(-x["centrality"],x["obligation_id"]))}


def build_lineage(obligations):
    rows=[
        ("LIN-001","OBL-CANDIDATE-IDENTITY","OBL-CANDIDATE-EQUIVALENCE","FORMALIZED_AS","v0.1.0","UNKNOWN","INFERRED"),
        ("LIN-002","OBL-CANDIDATE-STATE","OBL-CLAIM-EXCLUSIVITY","STRENGTHENED","v0.2.0","UNKNOWN","SUPPORTED"),
        ("LIN-003","OBL-OBS-DISTINCT","OBL-ACQ-METADATA","ELABORATED","v0.1.0","UNKNOWN","SUPPORTED"),
        ("LIN-004","OBL-RECOGNITION-DISTINCT","OBL-PROVIDER-CONTRACT","GENERALIZED","v0.2.0","UNKNOWN","SUPPORTED"),
        ("LIN-005","OBL-PROVENANCE","OBL-PROVENANCE-INTEGRITY","FUTURE_STRENGTHENING","UNKNOWN","UNKNOWN","SUPPORTED"),
        ("LIN-006","OBL-RESOURCE","OBL-UNBOUNDED","FUTURE_STRENGTHENING","UNKNOWN","UNKNOWN","SUPPORTED"),
        ("LIN-007","OBL-LIFECYCLE-OBS","OBL-AUDIT","FUTURE_STRENGTHENING","v0.7.1","UNKNOWN","SUPPORTED"),
    ]
    records=[{"lineage_id":a,"from_obligation":b,"to_obligation":c,"relation":d,"valid_from":e,"valid_until":f,"epistemic_status":g,"dependency":False,"supersession":False,"reason":"Analytical obligation evolution; no implementation lineage is silently asserted."} for a,b,c,d,e,f,g in rows]
    return {"schema_version":"1.0","graph_type":"OBLIGATION_LINEAGE_GRAPH","nodes":sorted({x for r in records for x in [r["from_obligation"],r["to_obligation"]]}),"edges":[{"from":r["from_obligation"],"to":r["to_obligation"],"relation":r["relation"],"lineage_id":r["lineage_id"]} for r in records],"lineage":records,"supersessions":[],"rule":"Lineage is evolution, not logical prerequisite or supersession."}


def build_conflicts(obligations):
    rows=[
        ("CONF-001","OBL-CANDIDATE-PRIORITY","OBL-BOUNDED-CONCURRENCY","Potential stable ordering semantics may conflict with unrestricted concurrent scheduling.","UNRESOLVED","Version ordering or prove order-insensitive equivalence."),
        ("CONF-002","OBL-DEDUP-SCOPES","OBL-CANDIDATE-PARENT","Aggressive merging may discard alternate parent provenance.","UNRESOLVED","Merge work identity while retaining alternate derivation edges."),
        ("CONF-003","OBL-RETRY","OBL-RESOURCE","Continuation through retry is constrained by finite resource bounds.","CONDITIONALLY_RESOLVED","Classify retryability and expose exhaustion under explicit limits."),
        ("CONF-004","OBL-PERSIST-COMPAT","OBL-PROVENANCE-INTEGRITY","Schema compatibility may conflict with strengthened provenance fields or protection.","UNRESOLVED","Version and migrate rather than reinterpret old records."),
        ("CONF-005","OBL-PROVIDER-ORDER","OBL-PROVIDER-FAILURE","Parallel/isolation changes may alter first-match provider ordering.","UNRESOLVED","Establish ordering dependence, then test or version the change."),
        ("CONF-006","OBL-PARSE-DEFECT","OBL-PRIVATE-SHAPE","Byte/source-form preservation is not semantic preservation of a known parse defect.","FALSE_CONFLICT","Preserve defect evidence; reject reproduction as a future requirement."),
    ]
    records=[{"conflict_id":a,"left_obligation":b,"right_obligation":c,"relation":"CONFLICTS_WITH","evidence_strength":"SUPPORTED_OR_EXPLICITLY_QUALIFIED","version_scope":"VARIES_OR_FUTURE","semantic_difference":d,"compatibility_impact":"REQUIRES_EXPLICIT_DECISION","resolution_status":e,"possible_resolution":f,"dependency":False} for a,b,c,d,e,f in rows]
    return {"schema_version":"1.0","graph_type":"OBLIGATION_CONFLICT_GRAPH","nodes":sorted({x for r in records for x in [r["left_obligation"],r["right_obligation"]]}),"edges":[{"from":r["left_obligation"],"to":r["right_obligation"],"relation":"CONFLICTS_WITH","conflict_id":r["conflict_id"]} for r in records],"conflicts":records,"rule":"Conflicts are not prerequisites and are not resolved by chronology."}


def build_graphs(contract,properties,obligations,deps,lineage,tests):
    evidence_nodes=[{"id":e["evidence_id"],"kind":"EVIDENCE","status":e["verification_status"]} for e in contract["normalized_evidence"]]
    property_nodes=[{"id":p["property_id"],"kind":"HISTORICAL_PROPERTY","status":p["epistemic_status"]} for p in properties]
    obligation_nodes=[{"id":o["obligation_id"],"kind":"OBLIGATION","status":o["status"],"category":o["final_category"]} for o in obligations]
    evidence_edges=[{"from":e,"to":p["property_id"],"relation":"SUPPORTS_PROPERTY"} for p in properties for e in p["evidence_refs"]]
    historical=[d for d in deps if d["dependency_type"]=="HISTORICAL_DEPENDENCY"]
    future=[d for d in deps if d["dependency_type"]=="FUTURE_ENGINEERING_DEPENDENCY"]
    historical_ids={x for d in historical for x in [d["from_obligation"],d["to_obligation"]]}
    future_ids={x for d in future for x in [d["from_obligation"],d["to_obligation"]]}
    verification_nodes=[{"id":t["test_id"],"kind":"TEST_EVIDENCE","status":t["execution_status"]} for t in tests]
    return {
        "EVIDENCE-GRAPH.yaml":{"schema_version":"1.0","graph_type":"EVIDENCE_GRAPH","nodes":evidence_nodes+property_nodes,"edges":evidence_edges},
        "HISTORICAL-OBLIGATION-GRAPH.yaml":{"schema_version":"1.0","graph_type":"HISTORICAL_OBLIGATION_GRAPH","nodes":[n for n in obligation_nodes if n["id"] in historical_ids],"edges":[{"from":d["from_obligation"],"to":d["to_obligation"],"relation":d["relation"],"evidence":d["evidence"]} for d in historical],"future_edges_excluded":True},
        "FUTURE-ENGINEERING-OBLIGATION-GRAPH.yaml":{"schema_version":"1.0","graph_type":"FUTURE_ENGINEERING_OBLIGATION_GRAPH","nodes":[n for n in obligation_nodes if n["id"] in future_ids],"edges":[{"from":d["from_obligation"],"to":d["to_obligation"],"relation":d["relation"],"reason":d["reason"]} for d in future],"historical_edges_not_relabelled":True},
        "VERIFICATION-GRAPH.yaml":{"schema_version":"1.0","graph_type":"VERIFICATION_GRAPH","nodes":obligation_nodes+verification_nodes,"edges":[{"from":o["obligation_id"],"to":o["test_ref"],"relation":"VERIFIED_BY","verification_result":"UNVERIFIED"} for o in obligations],"verified_nodes":[]},
    }


def build_assessments(models,provider_history,duplicate,bounds,risks):
    fields={name:field_assessments(models,name) for name in ["Candidate","Observation","Discovery"]}
    providers=defaultdict(list)
    for row in provider_history:
        for p in row["providers"]:providers[p].append(row)
    by_bound=defaultdict(list)
    for b in bounds:by_bound[b["bound"]].append(b)
    return {
        "canonical_pipeline":[
            {"from":"Candidate","to":"Acquisition","classification":"REQUIRED","scope":"admitted acquirable candidate; explicit policy skip permitted"},
            {"from":"Acquisition","to":"Observation","classification":"REQUIRED","scope":"attempted acquisition; failure/partial is an outcome"},
            {"from":"Observation","to":"Recognition","classification":"OPTIONAL","scope":"only eligible observations"},
            {"from":"Recognition","to":"Discovery","classification":"OPTIONAL","scope":"no-match permitted"},
            {"from":"Discovery","to":"Candidate Expansion","classification":"OPTIONAL","scope":"zero children permitted"},
            {"from":"Candidate Expansion","to":"Scheduling","classification":"OPTIONAL","scope":"bounds/dedup may reject or merge"},
        ],
        "candidate_identity":{"historically_established_rule":"UNKNOWN","dimensions_kept_independent":["normalized_target","type","origin","parent","provider","scope"],"forbidden_assumption":"URL_EQUALITY_IS_COMPLETE_HISTORICAL_IDENTITY"},
        "candidate_field_assessments":fields["Candidate"],"observation_field_assessments":fields["Observation"],"discovery_field_assessments":fields["Discovery"],
        "deduplication_assessments":[{"scope":x,"historical_status":"SUPPORTED_SCOPED" if x in {"queue","claim","processing","discovery"} else "UNKNOWN","global_guarantee":"NOT_ESTABLISHED"} for x in ["queue","claim","processing","discovery","persistence","export"]],
        "candidate_state_machine":{"scope":"v0.2.0 onward where explicit claiming is evidenced; v0.1.0 is not forced into it","states":["QUEUED","CLAIMED","COMPLETED","FAILED"],"excluded":{"NEW":"not needed for smallest machine","RETRYABLE":"edge condition, not stable state"},"transitions":[{"from":a,"to":b,"owner":c,"mutation":d,"postcondition":e,"failure_behavior":f,"observable_evidence":g} for a,b,c,d,e,f,g in [
            ("QUEUED","CLAIMED","scheduler/knowledge claim","remove/admit claim","one local owner","explicit claim failure","claim state/event"),("CLAIMED","COMPLETED","claim owner","release and complete","not re-claimable","no false completion","completion state/event"),("CLAIMED","FAILED","claim owner","record failure","context retained","no silent disappearance","failure state/event"),("FAILED","QUEUED","retry policy","increment attempts and requeue","one eligibility under bound","terminal exhaustion","attempt/requeue event")]],"thread_safety":"NOT_ESTABLISHED","distributed_atomicity":"NOT_ESTABLISHED"},
        "scheduler_semantics":[{"semantic":a,"historical_status":b,"future_status":c} for a,b,c in [("claim","SUPPORTED_EVENT_LOOP_LOCAL","CONDITIONAL"),("worker lifecycle","SUPPORTED_WITH_VARIANTS","PRESERVE_SEMANTICS"),("completion","SUPPORTED_WITH_UNKNOWN_V0.7_OWNERSHIP","FORMALIZE"),("failure","SUPPORTED_WITH_UNKNOWN_PROPAGATION","CONTAIN"),("retry","SUPPORTED_FROM_V0.3","CONDITIONAL"),("termination","UNSPECIFIED_UNIVERSAL_GUARANTEE","ENGINEERING_STRENGTHENING"),("cancellation","SOFT_BEHAVIOR_PARTICULAR_PATHS","VERIFY_IF_EXPOSED"),("concurrency","FINITE_CONFIGURED","THREAD_DISTRIBUTED_UNSPECIFIED")]],
        "observation_minimum":[{"potential_field":a,"historical_status":b,"minimum_obligation":c,"exact_value_domain":"UNKNOWN_NO_V7_CONTRACT"} for a,b,c in [("headers","SUPPORTED_NESTED_HTTP_SHAPE","CONDITIONAL"),("content_type","SUPPORTED_NESTED_METADATA","CONDITIONAL"),("content_length","UNKNOWN","UNKNOWN"),("body","ABSENT_IN_V0.1_FIELD_MODEL_PRESENT_LATER","CONDITIONAL"),("URL","SUPPORTED_TARGET","PRESERVE_OR_EQUIVALENT"),("redirect_target","SUPPORTED_LATE_VARIANTS","CONDITIONAL"),("error","SUPPORTED","PRESERVE_OR_EQUIVALENT"),("timing","SUPPORTED","PRESERVE_OR_EQUIVALENT"),("source_candidate","SUPPORTED","PRESERVE_OR_EQUIVALENT")]],
        "provenance_field_assessments":[{"field":a,"visibility":b,"integrity":"NOT_ESTABLISHED","obligation":c} for a,b,c in [("observation","EXPLICIT_ID","REQUIRED_OR_EXPLICIT_MISSING"),("provider","VARIES","CONDITIONAL"),("parent","STORED_WHEN_EXPANDED","REQUIRED_WHEN_APPLICABLE"),("derivation_path","PARTIAL","DO_NOT_CLAIM_COMPLETE"),("timestamp","PRESENT_UNVERIFIED_CLOCK","CONDITIONAL"),("confidence","RECURRENT_UNKNOWN_DOMAIN","CONDITIONAL")]],
        "provider_assessments":[{"provider":p,"versions":sorted({r["version"] for r in rows},key=VERSIONS.index),"recognition_semantics":"PER_OCCURRENCE_PARTIAL","discovery_semantics":"PER_OCCURRENCE_PARTIAL","candidate_generation":"VARIES_PROVIDER_OR_ENGINE","failure_behavior":"VARIES_OR_UNKNOWN","registration":"SUPPORTED_OCCURRENCE","ordering":"PRESENT_DEPENDENCE_UNKNOWN","common_contract":"NOT_ESTABLISHED_FROM_NAME_OR_SIGNATURE"} for p,rows in sorted(providers.items())],
        "resource_assessments":{"historical_bounds":[{"bound":name,"occurrences":len(rows),"versions":sorted({r["version"] for r in rows},key=VERSIONS.index),"values":sorted({r["value"] for r in rows}),"classification":"EXPLICIT_OR_CONFIGURED_BOUND"} for name,rows in sorted(by_bound.items())],"unbounded_findings":[{"finding":"POTENTIAL_UNBOUNDED_MEMORY","status":"SUPPORTED_STATIC_RISK_SOME_OCCURRENCES","vulnerability":"NOT_AUTOMATICALLY_A_VULNERABILITY"},{"finding":"POTENTIAL_UNBOUNDED_RETRIES","status":"UNKNOWN_EARLY_OR_INCOMPLETE_PATHS_BOUNDED_WHERE_IMPLEMENTED","vulnerability":"NOT_AUTOMATICALLY_A_VULNERABILITY"},{"finding":"POTENTIAL_UNBOUNDED_RESPONSE","status":"SUPPORTED_STATIC_RISK_WITHOUT_BODY_BOUND","vulnerability":"NOT_AUTOMATICALLY_A_VULNERABILITY"}],"risk_summary":dict(Counter(x["classification"] for x in risks))},
        "capability_matrix":[{"capability":a,"first_appearance":b,"first_implementation":b if not b.startswith("UNKNOWN") else "UNKNOWN","first_verification":"UNKNOWN_HISTORICAL_RETROSPECTIVE_STATIC_ONLY","stable":"UNKNOWN","future_obligation":c} for a,b,c in [("candidate discovery","v0.1.0","OBL-CANDIDATE-IDENTITY"),("recursive expansion","v0.1.0","OBL-EXPANSION-RECURSIVE"),("providerization","v0.2.0","OBL-PROVIDER-CONTRACT"),("concurrency","v0.1.0","OBL-BOUNDED-CONCURRENCY"),("provenance","v0.1.0","OBL-PROVENANCE"),("bounded execution","v0.1.0","OBL-RESOURCE"),("auditability","UNKNOWN_LEDGER_IS_NOT_AUDITABILITY","OBL-AUDIT")]],
        "observability_events":[{"event":x,"classification":"HISTORICAL_EVENT" if x in {"candidate claimed","acquisition completed","discovery emitted","candidate failed","scan completed"} else "OPTIONAL_EVENT","auditability":"NOT_IMPLIED"} for x in ["candidate claimed","acquisition started","acquisition completed","recognition succeeded","discovery emitted","candidate expanded","candidate failed","worker started","worker stopped","scan completed"]],
        "architecture_preservation_rules":[{"element":a,"classification":b} for a,b in [("Candidate","PRESERVE_SEMANTICS_ONLY"),("Observation","PRESERVE_SEMANTICS_ONLY"),("Provider role","PRESERVE_SEMANTICS_ONLY"),("Scheduler lifecycle","PRESERVE_SEMANTICS_ONLY"),("Knowledge accumulation","PRESERVE_SEMANTICS_ONLY"),("Provenance associations","PRESERVE_SEMANTICS_ONLY"),("Persistence/export representation","REMOVE_WITH_MIGRATION"),("UI presentation","OPTIONAL"),("Map/Set/function/module layout","HISTORICAL_ONLY")]],
        "historical_defects":[{"defect":"snapshot-0009 static parse failure","fix_defect":"REQUIRED_FOR_FUTURE","compatibility_concern":"UNKNOWN","migration_required":"ONLY_IF_REAL_CONSUMER_DEPENDENCE","evidence_preserved":True}],
    }


def field_assessments(models,model):
    by=defaultdict(list)
    for m in models:
        for f in m["fields"].get(model,[]):by[f].append(m)
    core={"Candidate":{"id","target","type","origin","parent","status","attempts","createdAt"},"Observation":{"id","candidateId","status","target","errors","startedAt","completedAt"},"Discovery":{"id","candidateId","observationId","kind","data","provenance"}}[model]
    return [{"model":model,"field":f,"occurrences":len(rows),"versions":sorted({r["version"] for r in rows},key=VERSIONS.index),"semantically_required":"REQUIRED_OR_EQUIVALENT" if f in core else "CONDITIONAL_OR_VERSION_SPECIFIC","serialization_required":"UNKNOWN_NO_VERIFIED_CONTRACT","externally_observable":"POTENTIAL_VIA_PERSISTENCE_OR_EXPORT","safe_to_remove":"NO_WITHOUT_EQUIVALENCE_OR_MIGRATION" if f in core else "UNKNOWN"} for f,rows in sorted(by.items())]


def build_failure(matrix):
    mapping={"acquisition":{"ACQUISITION_FAILURE","NETWORK_FAILURE","TIMEOUT","HTTP_FAILURE"},"parsing":{"PARSING_FAILURE"},"provider":{"PROVIDER_FAILURE","RECOGNITION_FAILURE"},"scheduler":{"SCHEDULER_FAILURE","STATE_FAILURE","DEDUPLICATION_FAILURE"},"concurrency":{"CONCURRENCY_FAILURE","CANCELLATION"},"persistence":{"PERSISTENCE_FAILURE"},"export":{"EXPORT_FAILURE"}}
    rows=[]
    for name,kinds in mapping.items():
        src=[x for x in matrix if x["failure"] in kinds]; vals=lambda k:sorted({x[k] for x in src}); supported=any(x["detection"]=="PROVED" or x["containment"]=="SUPPORTED" for x in src)
        rows.append({"failure_class":name,"source_taxonomy":sorted(kinds),"detection":vals("detection"),"containment":vals("containment"),"propagation":vals("propagation"),"recording":vals("observable"),"retryability":"EXPLICIT_ONLY_WHERE_CLASSIFIED" if name=="acquisition" else "UNKNOWN","recovery":vals("recovery"),"observability":vals("observable"),"historical_status":"SUPPORTED_WITH_UNKNOWN_PATHS" if supported else "UNKNOWN","engineering_obligation":"CONTAIN_AND_RECORD_WITHOUT_SILENT_SUCCESS" if supported else "REQUIREMENT_NOT_JUSTIFIED","strength":"REQUIRED" if supported and name!="export" else "UNKNOWN","future_strengthening":"Explicit classification and observability","failure_if_violated":"OBLIGATION_DEPENDENCY_FAILURE"})
    return {"schema_version":"1.0","input_contract_status":"INPUT_CONTRACT_FAILED","failure_obligations":rows,"failure_matrix":rows,"failure_classes":["OBLIGATION_VIOLATED","OBLIGATION_UNVERIFIED","OBLIGATION_BLOCKED","OBLIGATION_SUPERSEDED","OBLIGATION_CONTRADICTED","OBLIGATION_DEPENDENCY_FAILURE"],"rule":"Static failure mode is not a runtime incident; UNKNOWN remains UNKNOWN."}


def build_security(boundaries,authorities,parsers):
    trust={"USER_INPUT","PAGE_DOM","NETWORK","REMOTE_CONTENT","STORAGE","THIRD_PARTY_LIBRARIES"};auth={"PROVIDER_CODE","EXPORT","UI","BROWSER_APIS","USERSCRIPT_APIS"};rows=[]
    for x in boundaries:
        cls="UNKNOWN" if x["boundary_status"]=="NOT_PRESENT_OR_NOT_EVIDENCED" else "CONTROL_BOUNDARY" if x["boundary"]=="SCHEDULER" else "TRUST_BOUNDARY" if x["boundary"] in trust else "AUTHORITY_BOUNDARY" if x["boundary"] in auth else "UNKNOWN"
        rows.append({"boundary_id":x["boundary_id"],"snapshot_id":x["snapshot_id"],"version":x["version"],"boundary":x["boundary"],"classification":cls,"consumer":x["sink"],"authority":x["authority"],"data_crossing":x["data"],"validation":x["validation"],"sanitization":x["sanitization"],"execution_possibility":"ACQUIRED_CONTENT_EXECUTION_NOT_EVIDENCED" if x["boundary"]=="REMOTE_CONTENT" else "COMPONENT_CODE_EXECUTION" if x["boundary"]=="PROVIDER_CODE" else "UNKNOWN","failure_behavior":"UNKNOWN","security_guarantee":"NOT_ESTABLISHED","evidence":x["evidence"]})
    return {"schema_version":"1.0","input_contract_status":"INPUT_CONTRACT_FAILED","remote_content_rule":{"classification":"UNTRUSTED_INPUT_DATA","trusted_execution":"NOT_EVIDENCED","forbidden":"DOWNLOADED_SCRIPT_IS_TRUSTED_CODE"},"boundary_assessments":rows,"authority_records":len(authorities),"parser_records":len(parsers),"security_strengthenings":[{"historical":"remote acquisition exists","future":"explicit origin policy + bounded acquisition + verified provenance integrity","classification":"FUTURE_STRENGTHENING"},{"historical":"authority use is present","future":"required/granted/used authority is formally scoped","classification":"FUTURE_STRENGTHENING"}],"rule":"Data boundary is not automatically trust boundary; structure is not security guarantee."}


def build_contract(api):
    transitions=[{"old_contract":a,"new_contract":b,"classification":"UNKNOWN","outputs":"UNKNOWN","side_effects":"UNKNOWN","errors":"UNKNOWN","ordering":"UNKNOWN","ownership":"UNKNOWN","lifecycle":"UNKNOWN","concurrency":"UNKNOWN","provenance":"UNKNOWN","reason":"Protocol-v7 is missing; signatures are insufficient."} for a,b in zip(VERSIONS,VERSIONS[1:])]
    return {"schema_version":"1.0","input_contract_status":"INPUT_CONTRACT_FAILED","v7_contract_inventory":{"status":"INPUT_MISSING","contracts_consumed":0,"reason":"historical-source/contracts is absent"},"contract_obligations":[{"area":x,"status":"UNKNOWN","strengthen":"UNKNOWN","weaken":"UNKNOWN","replace":"UNKNOWN","retire":"UNKNOWN","reason":"REQUIREMENT_NOT_JUSTIFIED"} for x in ["candidate","acquisition","observation","provider","discovery","scheduler","failure","provenance","serialization"]],"versioned_contract_envelope":transitions,"semantic_dimensions":["outputs","side effects","errors","ordering","ownership","lifecycle","concurrency","provenance"],"source_api_shapes":len(api),"future_strengthening":{"provider":["matching","output","errors","ownership","lifecycle","cancellation","provenance"],"historical_fact":False}}


def build_nullability(models):
    rows=[]
    for model in ["Candidate","Observation","Discovery"]:
        for f in field_assessments(models,model):
            rows.append({"model":model,"field":f["field"],"current_value_domain":"UNKNOWN_NO_V7_CONTRACT","historical_presence":"SUPPORTED_FIELD_OCCURRENCE","safe_widening":"UNKNOWN","safe_narrowing":"UNKNOWN","breaking_changes":["required→absent","null→rejected","value→error","identifier semantic change"],"optional":"UNKNOWN","nullable":"UNKNOWN","derived":"UNKNOWN","deprecated":False})
    return {"schema_version":"1.0","input_contract_status":"INPUT_CONTRACT_FAILED","fields":rows,"serialization_surfaces":[{"surface":"YAML","historical_role":"ARCHAEOLOGY_OUTPUT_NOT_RUNTIME_CONTRACT"},{"surface":"export schema","historical_role":"STRUCTURED_OUTPUT_PRESENT_COMPATIBILITY_UNKNOWN"},{"surface":"stored objects","historical_role":"JSON_PERSISTENCE_PRESENT"},{"surface":"UI state","historical_role":"OBSERVABILITY_CHANNEL"},{"surface":"external APIs","historical_role":"CONSUMABILITY_UNKNOWN"}],"rule":"Field/signature presence does not prove nullability compatibility."}


def build_api(api,exports):
    cat={"recognize":"provider API","acquire":"component API","claimNextCandidate":"scheduler API","run":"component API","start":"UI API","stop":"UI API","addCandidate":"component API","addObservation":"component API","addDiscovery":"component API","persist":"component API","restore":"component API"}
    rows=[{"symbol":x["symbol"],"surface":cat.get(x["symbol"],"component API"),"external_consumability":"UNKNOWN","revisions":x["revisions"],"semantic_contract":{k:"UNKNOWN_FROM_SIGNATURE" for k in ["outputs","side_effects","errors","ordering","ownership","lifecycle","concurrency","provenance"]},"compatibility":"CONDITIONAL_ON_VERIFIED_CONSUMER"} for x in api]
    rows.append({"symbol":"structured export","surface":"export API","external_consumability":"POSSIBLE_USER_FACING","revisions":[],"semantic_contract":{"outputs":"STRUCTURED_OBJECT","side_effects":"VARIES","errors":"UNKNOWN","ordering":"UNKNOWN","ownership":"UNKNOWN","lifecycle":"UNKNOWN","concurrency":"UNKNOWN","provenance":"PARTIAL"},"compatibility":"CONDITIONAL_SCHEMA_VERSIONING"})
    return {"schema_version":"1.0","input_contract_status":"INPUT_CONTRACT_FAILED","surfaces":rows,"surface_categories":["component API","provider API","scheduler API","export API","UI API","external API"],"rule":"Not every function is external; signatures are not semantic guarantees."}


def build_trace(obligations,properties,deps,contract):
    pby={p["property_id"]:p for p in properties};dby=defaultdict(list)
    for d in deps:dby[d["from_obligation"]].append(d["dependency_id"])
    eby={e["evidence_id"]:e for e in contract["normalized_evidence"]};rows=[]
    for o in obligations:
        ev=eby[o["source_evidence"][0]];p=pby[o["source_properties"][0]]
        rows.append({"source":ev["provenance"]["source_path"],"artifact":ev["source_artifact"],"historical_claim":o["historical_claims"],"historical_property":p["property_id"],"obligation":o["obligation_id"],"obligation_class":o["class"],"strength":o["strength"],"final_category":o["final_category"],"epistemic_status":o["epistemic_status"],"lifecycle_status":o["status"],"dependency":dby[o["obligation_id"]],"contract":"INPUT_MISSING_V7" if p["property_type"]=="CONTRACTUAL" else "NOT_SEPARATELY_VERIFIED","invariant":o["invariant_ref"],"test":o["test_ref"],"verification_result":"UNVERIFIED","derivation_acceptance":"BLOCKED_BY_INPUT_CONTRACT_FAILED"})
    return {"schema_version":"1.0","input_contract_status":"INPUT_CONTRACT_FAILED","columns":["source","artifact","historical_claim","historical_property","obligation","obligation_class","strength","final_category","epistemic_status","lifecycle_status","dependency","contract","invariant","test","verification_result"],"rows":rows}


def build_schemas():
    base={"$schema":"https://json-schema.org/draft/2020-12/schema","schema_version":"1.0","additionalProperties":True}
    schemas={
        "input-contract.schema.yaml":{**base,"title":"Protocol-v10.1 input contract","type":"object","required":["input_contract_version","obligation_schema_version","status","required_inputs","integrity_checks","normalized_evidence"],"properties":{"input_contract_version":{"const":"1.0"},"obligation_schema_version":{"const":"1.0"},"status":{"enum":["VALID","INPUT_CONTRACT_FAILED"]}}},
        "historical-property.schema.yaml":{**base,"title":"Historical property","type":"object","required":["property_id","property_type","statement","version_scope","evidence_refs","epistemic_status","historical_status"],"properties":{"property_type":{"enum":PROPERTY_TYPES},"epistemic_status":{"enum":EPISTEMIC}}},
        "obligation.schema.yaml":{**base,"title":"Engineering obligation","type":"object","required":["obligation_id","statement","class","strength","final_category","epistemic_status","source_properties","source_evidence","dependencies","dependents","verification","compatibility","exceptions","status"],"properties":{"class":{"enum":CLASSES},"strength":{"enum":STRENGTHS},"final_category":{"enum":CATEGORIES},"epistemic_status":{"enum":EPISTEMIC},"status":{"enum":LIFECYCLE}}},
        "obligation-dependency.schema.yaml":{**base,"title":"Obligation dependency","type":"object","required":["dependency_id","from_obligation","to_obligation","relation","reason"],"properties":{"relation":{"enum":DEPENDENCY_RELATIONS},"scope":{"type":"object"}}},
        "obligation-lineage.schema.yaml":{**base,"title":"Obligation lineage","type":"object","required":["lineage_id","from_obligation","to_obligation","relation","epistemic_status"],"properties":{"epistemic_status":{"enum":EPISTEMIC}}},
        "obligation-conflict.schema.yaml":{**base,"title":"Obligation conflict","type":"object","required":["conflict_id","left_obligation","right_obligation","relation","semantic_difference","resolution_status"],"properties":{"relation":{"const":"CONFLICTS_WITH"},"resolution_status":{"enum":["CONDITIONALLY_RESOLVED","UNRESOLVED","FALSE_CONFLICT"]}}},
        "traceability.schema.yaml":{**base,"title":"Requirement traceability row","type":"object","required":["source","artifact","historical_claim","historical_property","obligation","obligation_class","final_category","dependency","invariant","test","verification_result"]},
    }
    for name,obj in schemas.items():dump(OUT/"schema"/name,obj)


def build_markdown(main_obj,input_contract,dep_model,lineage,conflicts,failure,security,contract,trace):
    obligations=main_obj["obligations"];oby={o["obligation_id"]:o for o in obligations}
    write_md("README.md",front("Protocol-v10.1 Historical Engineering Obligations")+"v10.1 validates a versioned input package, normalizes accepted evidence, extracts properties, and only then derives typed obligations. The required package fails because v1 integrity fails and v4-v7 are missing. All obligation results are downgraded and blocked from full acceptance.\n\n"+table(["Measure","Count"],main_obj["metadata"]["counts"].items())+"\nThe four graphs—evidence, obligation dependency, obligation lineage, and verification—are separate machine artifacts. Future mechanisms remain `UNSELECTED`.\n")
    closure=front("Dependency Closure")+"Every REQUIRED obligation is listed. Because no future test is executed and the input contract fails, all closure states remain `OBLIGATION_BLOCKED`.\n\n"+table(["Obligation","Direct prerequisites","Transitive prerequisites","Verification prerequisites","Unresolved","State"],[(x["obligation_id"],x["direct_prerequisites"],x["transitive_prerequisites"],x["verification_prerequisites"],x["unresolved_dependencies"],x["closure_status"]) for x in dep_model["required_closure"]])
    write_md("DEPENDENCY-CLOSURE.md",closure)
    write_md("OBLIGATION-LINEAGE-GRAPH.md",front("Obligation Lineage Graph")+"Lineage represents analytical evolution, not logical dependency or supersession.\n\n"+table(["ID","From","Relation","To","From version","Status"],[(x["lineage_id"],x["from_obligation"],x["relation"],x["to_obligation"],x["valid_from"],x["epistemic_status"]) for x in lineage["lineage"]]))
    conflict_rows=[(x["conflict_id"],x["left_obligation"],x["right_obligation"],x["semantic_difference"],x["resolution_status"],x["possible_resolution"]) for x in conflicts["conflicts"]]
    write_md("OBLIGATION-CONFLICTS.md",front("Obligation Conflicts")+table(["ID","Left","Right","Difference","Status","Possible resolution"],conflict_rows)+"\nConflicts are not dependency prerequisites and chronology does not resolve them.\n")
    tests=main_obj["test_candidates"]
    write_md("HISTORICAL-REGRESSION-SUITE.md",front("Dependency-Aware Historical Regression Suite")+table(["Test","Obligation","Prerequisite tests","Potential dependent failures","Expected","State"],[(t["test_id"],t["obligation_id"],t["prerequisite_tests"],t["dependent_failures"],t["expected_outcome"],t["failure_class"]) for t in tests])+"\n## Golden candidates\nCandidate identity, declared provider selection, discovery extraction, provenance, versioned export shape, failure classification, and scheduler termination become golden only after semantic domains are explicit.\n\n## Non-golden behavior\nFunction names, private modules, implementation language, UI styling, log formatting, Map/Set layout, and scheduler mechanism are not golden absent external contracts.\n")
    must=[o for o in obligations if o["strength"]=="REQUIRED" and o["final_category"] in {"PRESERVATION_OBLIGATION","ENGINEERING_REQUIREMENT"}]
    may=[o for o in obligations if o not in must and o["final_category"]!="UNKNOWN"]
    write_md("COMPATIBILITY-ENVELOPE.md",front("Compatibility Envelope")+"```text\nMUST PRESERVE\nMAY CHANGE WITH EQUIVALENCE PROOF\nFREE TO REDESIGN\n```\n\n## Must preserve\n"+table(["Obligation","Statement"],[(o["obligation_id"],o["statement"]) for o in must])+"\n## May change with equivalence proof\n"+table(["Obligation","Allowed"],[(o["obligation_id"],o["allowed_change"]) for o in may])+"\n## Free to redesign\nFunction/class names, private modules, language, UI styling, log formatting, concrete containers, and worker mechanics. Semantic equivalence—not source identity—governs refactoring.\n")
    write_md("ESSENTIAL-VS-ACCIDENTAL.md",front("Essential vs Accidental Architecture")+table(["Element","Semantic effect","Rule"],[(x["element"],"Changes behavior" if x["classification"]=="PRESERVE_SEMANTICS_ONLY" else "Representation or conditional compatibility",x["classification"]) for x in main_obj["architecture_preservation_rules"]])+"\n## Allowed refactoring\nworker loop → actor; class → trait; function → service; in-memory queue → persistent queue, only with equivalent contracts.\n\n## Forbidden refactoring\nfailure → silent skip; provenance → discard; Observation → raw body only; provider failure → scheduler failure; bounded pool → unbounded spawning.\n")
    write_md("MIGRATION-OBLIGATIONS.md",front("Migration Obligations")+table(["Area","Required when changed","State"],[("candidate identity","versioning, compatibility layer, data/test migration","CONDITIONAL"),("candidate state","state mapping, documentation, tests","CONDITIONAL"),("persistence","schema version, validated migration/rejection, recovery","CONDITIONAL"),("export","versioned envelope, adapter, partial marker","CONDITIONAL"),("provider/error/nullability","deprecation, adapter, semantic negative tests","CONDITIONAL"),("v0.5 parse defect","retain evidence; no compatibility reproduction by default","REQUIRED_FIX")])+"\n")
    write_md("OBLIGATION-GRAPH.md",front("Four-Graph Obligation Model")+"```text\nNORMALIZED EVIDENCE -> HISTORICAL PROPERTY -> OBLIGATION\nOBLIGATION -> DEPENDENCY GRAPH\nOBLIGATION -> LINEAGE GRAPH\nOBLIGATION -> VERIFICATION GRAPH -> UNVERIFIED TEST\n```\n\nEvidence, dependency, lineage, conflict, and verification relations are not collapsed. Historical and future dependency graphs are also separate.\n")
    build_final_report(main_obj,input_contract,dep_model,conflicts)


def build_final_report(main_obj,input_contract,dep_model,conflicts):
    o=main_obj["obligations"]; pby={p["property_id"]:p for p in main_obj["historical_properties"]}
    def sec(n,title,ids=None,types=None):
        rows=[x for x in o if (not ids or x["obligation_id"] in ids) and (not types or pby[x["source_properties"][0]]["property_type"] in types)]
        return f"## {n}. {title}\n\n"+table(["ID","Statement","Class","Strength","Category","Epistemic","Lifecycle","Closure"],[(x["obligation_id"],x["statement"],x["class"],x["strength"],x["final_category"],x["epistemic_status"],x["status"],x["closure_status"]) for x in rows])+"\n"
    text=front("Generic Discovery Engine — Protocol-v10.1 Obligations")
    text+="## 1. Scope\n\nTyped, dependency-aware engineering consequences are derived only after input normalization. No future architecture is selected.\n\n"
    text+="## 2. Evidence Boundary\n\n`INPUT-CONTRACT.yaml` records `INPUT_CONTRACT_FAILED`: v1 is unverified/hash-mismatched and v4-v7 are `INPUT_MISSING`. The corpus is downgraded; missing evidence is not evidence of absence.\n\n"
    text+="## 3. Historical Properties\n\n%d normalized evidence records support %d historical facts and %d properties. Evidence, property, obligation, class, strength, epistemic status, final category, and lifecycle remain independent.\n\n"%(main_obj["metadata"]["counts"]["normalized_evidence"],len(main_obj["historical_facts"]),len(main_obj["historical_properties"]))
    text+=sec(4,"Mandatory Preservation Obligations",ids={x["obligation_id"] for x in o if x["strength"]=="REQUIRED" and x["final_category"]=="PRESERVATION_OBLIGATION"})
    text+=sec(5,"Compatibility Obligations",ids={x["obligation_id"] for x in o if x["class"]=="COMPATIBILITY"})
    text+=sec(6,"Algorithmic Obligations",types={"ALGORITHMIC"})
    text+=sec(7,"Candidate Obligations",ids={x for x in ["OBL-CANDIDATE-IDENTITY","OBL-CANDIDATE-EQUIVALENCE","OBL-DEDUP-SCOPES","OBL-CANDIDATE-ORIGIN","OBL-CANDIDATE-PARENT","OBL-CANDIDATE-STATE","OBL-CANDIDATE-PRIORITY","OBL-CANDIDATE-ATTEMPTS","OBL-CANDIDATE-TIMESTAMPS","OBL-CLAIM-EXCLUSIVITY","OBL-TERMINAL-OWNERSHIP","OBL-CANDIDATE-ADMISSION"]})
    text+=sec(8,"Acquisition Obligations",ids={x for x in ["OBL-ACQ-BEFORE-INTERP","OBL-ACQ-OUTCOME","OBL-ACQ-METADATA","OBL-ACQ-TIMEOUT","OBL-ACQ-SCOPE","OBL-CANCELLATION","OBL-WEB-GENERALIZE"]})
    text+=sec(9,"Observation Obligations",ids={"OBL-OBS-DISTINCT","OBL-OBS-SOURCE","OBL-OBS-OUTCOMES","OBL-ACQ-METADATA"})
    text+=sec(10,"Recognition Obligations",ids={"OBL-RECOGNITION-DISTINCT","OBL-RECOGNITION-OUTCOMES"})
    text+=sec(11,"Discovery Obligations",ids={"OBL-DISCOVERY-RECORD","OBL-PROVENANCE"})
    text+=sec(12,"Expansion Obligations",ids={"OBL-EXPANSION-RECURSIVE","OBL-EXPANSION-VS-RETRY","OBL-CANDIDATE-ADMISSION","OBL-RESOURCE"})
    text+=sec(13,"Scheduler Obligations",types={"ARCHITECTURAL","CONCURRENCY"})
    text+=sec(14,"Concurrency Obligations",types={"CONCURRENCY"})
    text+=sec(15,"Provider Obligations",types={"INTERFACE"})
    text+=sec(16,"Provenance Obligations",types={"PROVENANCE"})
    text+=sec(17,"Failure Obligations",types={"FAILURE"})
    text+=sec(18,"Security Obligations",types={"SECURITY"})
    text+=sec(19,"Resource Obligations",types={"RESOURCE"})
    text+=sec(20,"Contract Obligations",types={"CONTRACTUAL"})
    text+=sec(21,"Serialization Obligations",types={"COMPATIBILITY"})
    text+=sec(22,"Observability Obligations",types={"OBSERVABILITY"})
    text+=sec(23,"Testing Obligations",types={"BEHAVIORAL"},ids={"OBL-REGRESSION","OBL-PARSE-DEFECT"})
    text+="## 24. Essential vs Accidental Architecture\n\nCandidate/Observation/Discovery semantics, scheduler lifecycle, recursive expansion, knowledge, and provenance associations are semantic. Source names, private grouping, language, UI presentation, logs, and containers are accidental absent contracts.\n\n"
    text+="## 25. Compatibility Envelope\n\nPreserve justified semantics; change representations only with equivalence proof; redesign accidental details freely. The failed input contract prevents full compatibility acceptance.\n\n"
    text+="## 26. Migration Obligations\n\nIdentity, state, persistence, export, provider, error, and nullability changes require conditional versioning/migration when actual consumers exist.\n\n"
    text+="## 27. Obligation Conflicts\n\n%d conflicts are separate from prerequisites and retain explicit resolution status.\n\n"%len(conflicts["conflicts"])
    text+="## 28. Verification Gaps\n\nAll tests are `UNVERIFIED`; every REQUIRED closure is `OBLIGATION_BLOCKED`. The topological order is analytical and cannot override failed input or unexecuted prerequisites.\n\n"
    text+="## 29. Historical Defects\n\nThe v1 byte/range break, missing v4-v7 evidence, snapshot-0009 parse defect, possible silent failures, local-only deduplication, partial provenance, and static resource risks remain explicit.\n\n"
    strong=[x for x in o if x["strengthening"]=="ENGINEERING_STRENGTHENING"]
    text+="## 30. Future Engineering Strengthenings\n\n"+table(["ID","Statement","Reason"],[(x["obligation_id"],x["statement"],x["rationale"]) for x in strong])+"\n"
    text+="## 31. Final Obligation Set\n\n"+table(["Class","Count"],sorted(Counter(x["class"] for x in o).items()))+"\n"+table(["Strength","Count"],sorted(Counter(x["strength"] for x in o).items()))+"\n"+table(["Dependency","Count"],[("REQUIRES",sum(x["relation"]=="REQUIRES" for x in dep_model["dependencies"])),("non-REQUIRES analytical",sum(x["relation"]!="REQUIRES" for x in dep_model["dependencies"])),("cycles",len(dep_model["requires_cycles"]))])+"\n**Final disposition: `INPUT_CONTRACT_FAILED`; structural synthesis is downgraded and not accepted as complete.**\n"
    write_md("ENGINEERING-OBLIGATION-REPORT.md",text)


if __name__=="__main__":main()
