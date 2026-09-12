#!/usr/bin/env python3
"""Independent structural/semantic validator for Protocol-v10.1 outputs.

A truthful INPUT_CONTRACT_FAILED gate is a blocked acceptance gate, not a validator bug.
The validator exits nonzero only for structural or semantic misrepresentation.
"""
from __future__ import annotations
import hashlib, json, sys
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[2]; HS=ROOT/"historical-source"; OUT=HS/"obligations"
DELIVERABLES=[
 "README.md","INPUT-CONTRACT.yaml","OBLIGATIONS.yaml","OBLIGATION-DEPENDENCIES.yaml","OBLIGATION-DEPENDENCY-MATRIX.yaml","DEPENDENCY-CLOSURE.md","DEPENDENCY-CRITICAL-OBLIGATIONS.yaml","EVIDENCE-GRAPH.yaml","HISTORICAL-OBLIGATION-GRAPH.yaml","FUTURE-ENGINEERING-OBLIGATION-GRAPH.yaml","VERIFICATION-GRAPH.yaml","OBLIGATION-LINEAGE.yaml","OBLIGATION-LINEAGE-GRAPH.md","OBLIGATION-CONFLICTS.yaml","FAILURE-OBLIGATIONS.yaml","SECURITY-OBLIGATIONS.yaml","CONTRACT-OBLIGATIONS.yaml","NULLABILITY-COMPATIBILITY.yaml","HISTORICAL-API-SURFACE.yaml","TRACEABILITY-MATRIX.yaml","HISTORICAL-REGRESSION-SUITE.md","COMPATIBILITY-ENVELOPE.md","ESSENTIAL-VS-ACCIDENTAL.md","MIGRATION-OBLIGATIONS.md","OBLIGATION-CONFLICTS.md","OBLIGATION-GRAPH.md","ENGINEERING-OBLIGATION-REPORT.md","schema/input-contract.schema.yaml","schema/historical-property.schema.yaml","schema/obligation.schema.yaml","schema/obligation-dependency.schema.yaml","schema/obligation-lineage.schema.yaml","schema/obligation-conflict.schema.yaml","schema/traceability.schema.yaml"]
CLASSES={"PRESERVE","COMPATIBILITY","STABILIZE","GENERALIZE","FORMALIZE","VERIFY","CONTAIN","OBSERVE","DEPRECATE","REJECT","OPTIONAL"}
STRENGTHS={"REQUIRED","CONDITIONAL","RECOMMENDED","OPTIONAL","UNKNOWN"}
CATEGORIES={"HISTORICAL_FACT","HISTORICAL_PROPERTY","PRESERVATION_OBLIGATION","COMPATIBILITY_OBLIGATION","ENGINEERING_REQUIREMENT","FUTURE_STRENGTHENING","DESIGN_OPTION","HISTORICAL_DEFECT","UNKNOWN"}
EPISTEMIC={"PROVED","SUPPORTED","INFERRED","CONJECTURED","CONTRADICTED","UNKNOWN"}
LIFECYCLE={"DISCOVERED","SUPPORTED","FORMALIZED","IMPLEMENTED","VERIFIED","SUPERSEDED","REJECTED","UNKNOWN"}
PROPERTY_TYPES={"ALGORITHMIC","ARCHITECTURAL","BEHAVIORAL","DATA","INTERFACE","CONTRACTUAL","CONCURRENCY","FAILURE","SECURITY","PROVENANCE","OBSERVABILITY","RESOURCE","COMPATIBILITY"}
RELATIONS={"REQUIRES","SUPPORTS","ENABLES","REFINES","STRENGTHENS","CONSTRAINS","CONFLICTS_WITH","SUPERSEDES","DERIVED_FROM","VERIFIED_BY"}
FAILURE_STATES={"INPUT_MISSING","INPUT_MALFORMED","INPUT_SCHEMA_MISMATCH","INPUT_HASH_MISMATCH","INPUT_PROVENANCE_BROKEN","INPUT_VERSION_CONFLICT","INPUT_TEMPORAL_CONTAMINATION","INPUT_UNVERIFIED","INPUT_CONTRADICTION","INPUT_INSUFFICIENT"}


def load(name): return json.loads((OUT/name).read_text(encoding="utf-8"))
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    checks=[]
    def check(cid,category,desc,ok,detail=""):
        checks.append({"check_id":cid,"category":category,"description":desc,"result":"PASS" if ok else "FAIL","detail":detail})
    def blocked(cid,category,desc,detail): checks.append({"check_id":cid,"category":category,"description":desc,"result":"BLOCKED","detail":detail})
    for i,name in enumerate(DELIVERABLES,1):check(f"A{i:02d}","deliverables",f"required deliverable exists: {name}",(OUT/name).is_file())
    if any(x["result"]=="FAIL" for x in checks): return finish(checks,{})
    data=load("OBLIGATIONS.yaml"); ic=load("INPUT-CONTRACT.yaml"); dm=load("OBLIGATION-DEPENDENCIES.yaml"); matrix=load("OBLIGATION-DEPENDENCY-MATRIX.yaml"); critical=load("DEPENDENCY-CRITICAL-OBLIGATIONS.yaml"); lineage=load("OBLIGATION-LINEAGE.yaml"); conflicts=load("OBLIGATION-CONFLICTS.yaml"); trace=load("TRACEABILITY-MATRIX.yaml"); fail=load("FAILURE-OBLIGATIONS.yaml"); security=load("SECURITY-OBLIGATIONS.yaml"); contract=load("CONTRACT-OBLIGATIONS.yaml"); nulls=load("NULLABILITY-COMPATIBILITY.yaml"); api=load("HISTORICAL-API-SURFACE.yaml"); evidence_graph=load("EVIDENCE-GRAPH.yaml"); hist_graph=load("HISTORICAL-OBLIGATION-GRAPH.yaml"); future_graph=load("FUTURE-ENGINEERING-OBLIGATION-GRAPH.yaml"); verify_graph=load("VERIFICATION-GRAPH.yaml")
    meta=data["metadata"]; facts=data["historical_facts"]; props=data["historical_properties"]; obs=data["obligations"]; reqs=data["engineering_requirements"]; invs=data["invariants"]; tests=data["test_candidates"]
    O={x["obligation_id"]:x for x in obs}; P={x["property_id"]:x for x in props}; E={x["evidence_id"]:x for x in ic["normalized_evidence"]}; T={x["test_id"]:x for x in tests}; D={x["dependency_id"]:x for x in dm["dependencies"]}

    # Contract identity and truthful failed-input model.
    check("I00","input","input contract and obligation schema versions are 1.0",ic.get("input_contract_version")=="1.0" and ic.get("obligation_schema_version")=="1.0" and meta.get("input_contract_version")=="1.0" and meta.get("obligation_schema_version")=="1.0")
    required_types={"source_extraction","artifact_lineage","reconstructed_snapshots","reconstruction_verification","algorithm_evolution","architecture_evolution","contract_evolution","security_evolution","historical_synthesis"}
    check("I01","input","all nine required input kinds are represented",{x["artifact_type"] for x in ic["required_inputs"]}==required_types)
    check("I02","input","schemas are checked and missing schema inputs remain blocked",find_ic(ic,"I02")=="BLOCKED" and all(x["schema_version"]=="UNKNOWN" for x in ic["required_inputs"] if x["input_state"]=="INPUT_MISSING"))
    check("I03","input","content hashes and v1 mismatch are distinguished",find_ic(ic,"I03")=="FAIL" and "INPUT_HASH_MISMATCH" in emitted_failures(ic) and all(len(x["content_hash"])==64 for x in ic["required_inputs"] if x["source_path"]!="UNKNOWN"))
    check("I04","input","version consistency gate is blocked, not falsely passed",find_ic(ic,"I04")=="BLOCKED")
    check("I05","input","provenance references structurally resolve",find_ic(ic,"I05")=="PASS" and all((ROOT/e["provenance"]["source_path"]).is_file() for e in E.values()))
    check("I06","input","normalized evidence epistemic labels are valid",find_ic(ic,"I06")=="PASS" and all(e["epistemic_status"] in EPISTEMIC for e in E.values()))
    check("I07","input","contradictions are preserved",find_ic(ic,"I07")=="PASS" and "NE-V9-CONTRADICTIONS" in E and len(E["NE-V9-CONTRADICTIONS"]["normalized_payload"])>0)
    check("I08","input","unknowns are preserved",find_ic(ic,"I08")=="PASS" and "NE-V9-UNKNOWNS" in E and E["NE-V9-UNKNOWNS"]["epistemic_status"]=="UNKNOWN")
    check("I09","input","missing v4 reconstruction verification fails explicitly",find_ic(ic,"I09")=="FAIL" and any(x["artifact_type"]=="reconstruction_verification" and x["input_state"]=="INPUT_MISSING" for x in ic["required_inputs"]))
    check("I10","input","temporal isolation gate is explicit",find_ic(ic,"I10")=="PASS" and "INPUT_TEMPORAL_CONTAMINATION" in ic["failure_state_registry"])
    check("I11","input","v4-v7 remain missing, not synthesized",{x["producer_stage"] for x in ic["required_inputs"] if x["input_state"]=="INPUT_MISSING"}=={"verification","algorithm_evolution","architecture_evolution","contract_evolution"})
    check("I12","input","overall failed status and downgrade authorization are explicit",ic["status"]=="INPUT_CONTRACT_FAILED" and ic["derivation_authorization"]=="DOWNGRADED_PROVISIONAL_ONLY" and meta["input_contract_status"]=="INPUT_CONTRACT_FAILED")
    check("I13","input","missing evidence is not evidence of absence",ic["missing_evidence_semantics"]["must_not_be_interpreted_as"]=="EVIDENCE_OF_ABSENCE")
    check("I14","input","every failure state belongs to normative registry",set(ic["failure_state_registry"])==FAILURE_STATES and emitted_failures(ic)<=FAILURE_STATES)
    check("I15","input","normalization envelope has exact core fields",all(set(["evidence_id","evidence_type","source_stage","source_artifact","version_scope","statement","provenance","epistemic_status","verification_status","dependencies","normalized_payload"])<=set(e) for e in E.values()))
    check("I16","input","derivation declares normalized-evidence-only consumption",meta["derivation_input"]=="NORMALIZED_EVIDENCE_ENVELOPE_ONLY" and all(x in E for p in props for x in p["evidence_refs"]))
    check("I17","input","direct mandatory-source rejection policy is present",all(x in ic["rejected_direct_mandatory_sources"] for x in ["current architecture documentation","future roadmap","modern redesign proposal","unverified interpretation"]))
    check("I18","input","normalized content hashes bind existing source paths",all(e["provenance"]["content_hash"]==sha(ROOT/e["provenance"]["source_path"]) for e in E.values()))
    check("I19","input","normalized evidence uses only accepted evidence classes",all(e["evidence_type"] in ic["accepted_evidence_classes"] for e in E.values()))

    # Property and obligation schemas.
    check("P01","properties","facts remain distinct from properties and obligations",all(f["final_category"]=="HISTORICAL_FACT" and f["future_requirement"]=="NOT_AUTOMATIC" for f in facts))
    check("P02","properties","all properties use prescribed uppercase property types",all(p["property_type"] in PROPERTY_TYPES for p in props))
    check("P03","properties","all properties include minimum v10.1 model fields",all(set(["property_id","property_type","statement","version_scope","evidence_refs","epistemic_status","historical_status"])<=set(p) for p in props))
    check("P04","properties","every property resolves normalized evidence",all(p["evidence_refs"] and set(p["evidence_refs"])<=set(E) for p in props))
    check("P05","properties","property is not automatically a requirement",all("requirement_status" in p for p in props) and any(p["requirement_status"]=="NOT_AUTOMATICALLY_A_REQUIREMENT" for p in props))
    check("P06","properties","state properties preserve epistemic labels",all(p["epistemic_status"] in EPISTEMIC for p in props))
    required_ob_fields={"obligation_id","statement","class","strength","final_category","epistemic_status","source_properties","source_evidence","version_scope","dependencies","dependents","verification","compatibility","exceptions","status"}
    check("O01","obligations","every obligation includes the minimum schema",all(required_ob_fields<=set(o) for o in obs))
    check("O02","obligations","class enum excludes UNKNOWN",all(o["class"] in CLASSES and o["class"]!="UNKNOWN" for o in obs))
    check("O03","obligations","strength, category, epistemic, and lifecycle enums are independent and valid",all(o["strength"] in STRENGTHS and o["final_category"] in CATEGORIES and o["epistemic_status"] in EPISTEMIC and o["status"] in LIFECYCLE for o in obs))
    check("O04","obligations","obligation IDs are unique",len(O)==len(obs))
    check("O05","obligations","all source properties/evidence resolve",all(set(o["source_properties"])<=set(P) and set(o["source_evidence"])<=set(E) and o["source_properties"] and o["source_evidence"] for o in obs))
    check("O06","obligations","all obligations expose version scope",all(o["version_scope"].get("versions") for o in obs))
    check("O07","obligations","no obligation is marked VERIFIED or IMPLEMENTED",not any(o["status"] in {"VERIFIED","IMPLEMENTED"} for o in obs))
    check("O08","obligations","verified status is distinct from implementation and test result",all(o["verification"]["result"]=="UNVERIFIED" for o in obs) and all(t["execution_status"]=="UNVERIFIED" for t in tests))
    check("O09","obligations","classes, strengths and categories are not mechanically identical",len({(o["class"],o["strength"],o["final_category"],o["epistemic_status"],o["status"]) for o in obs})>15)
    check("O10","obligations","historical defects are explicitly rejected",any(o["class"]=="REJECT" and o["final_category"]=="HISTORICAL_DEFECT" for o in obs))
    check("O11","obligations","future strengthenings remain labeled",all(o["strengthening"]!="HISTORICAL" for o in obs if o["final_category"]=="FUTURE_STRENGTHENING"))
    check("O12","obligations","requirements retain source-local blocked acceptance",len(reqs)==len(obs) and all(r["derivation_acceptance"]=="BLOCKED_BY_INPUT_CONTRACT_FAILED" for r in reqs))
    check("O13","obligations","one invariant and test resolves for every obligation",len(invs)==len(obs)==len(tests) and all(o["invariant_ref"] in {x["invariant_id"] for x in invs} and o["test_ref"] in T for o in obs))
    check("O14","obligations","priority basis is risk-based rather than chronological",all(o["priority_basis"]["historical_importance_is_not_current_risk"] is True for o in obs))

    # Dependencies V02-V10 and separation rules.
    check("V02","dependencies","dependency direction and relation are valid",all(d["from_obligation"] in O and d["to_obligation"] in O and d["relation"] in RELATIONS and d["from_obligation"]!=d["to_obligation"] for d in D.values()))
    check("V03","dependencies","every dependency has semantic justification and provenance",all(d["reason"].strip() and d["evidence"] and set(d["evidence"])<=set(E) and set(["condition","dependency_type","scope","valid_from","valid_until"])<=set(d) for d in D.values()))
    check("V04","dependencies","verification edges resolve actual test evidence without false verification",all(e["to"] in T and e["verification_result"]=="UNVERIFIED" for e in verify_graph["edges"]) and not verify_graph["verified_nodes"])
    cycles=find_cycles(O,{k:[d["to_obligation"] for d in D.values() if d["from_obligation"]==k and d["relation"]=="REQUIRES"] for k in O})
    check("V05","dependencies","REQUIRES cycles are detected and none are silently linearized",cycles==[] and dm["cycle_status"]=="ACYCLIC" and dm["requires_cycles"]==[])
    req_closure={x["obligation_id"]:x for x in dm["required_closure"]}
    check("V06","dependencies","every REQUIRED obligation exposes complete dependency closure",all(o["obligation_id"] in req_closure and req_closure[o["obligation_id"]]["transitive_prerequisites"]==o["prerequisite_closure"] for o in obs if o["strength"]=="REQUIRED"))
    check("V07","dependencies","no obligation is VERIFIED while required dependencies are unverified",not any(o["status"]=="VERIFIED" and any(O[p]["status"]!="VERIFIED" for p in o["prerequisite_closure"]) for o in obs))
    check("V08","dependencies","centrality and change impact cover every obligation",{x["obligation_id"] for x in critical["records"]}==set(O) and all(isinstance(x["centrality"],int) and set(["revisit_dependents","revisit_invariants","revisit_regression_tests","revisit_migration","revisit_conflicts"])<=set(x["change_impact"]) for x in critical["records"]))
    order=dm["verification_order"]; pos={x:i for i,x in enumerate(order)}
    check("V09","dependencies","topological verification order puts REQUIRES targets first",len(order)==len(O)==len(set(order)) and all(pos[d["to_obligation"]]<pos[d["from_obligation"]] for d in D.values() if d["relation"]=="REQUIRES"))
    check("V10","dependencies","failure propagation reaches dependent tests",all(set(t["prerequisite_tests"])=={O[p]["test_ref"] for p in O[t["obligation_id"]]["prerequisite_closure"]} and t["failure_class"] in fail["failure_classes"] and t["prerequisite_failure_result"]=="OBLIGATION_DEPENDENCY_FAILURE" and t["self_failure_result"]=="OBLIGATION_VIOLATED" for t in tests) and any(x["dependent_result"]=="OBLIGATION_DEPENDENCY_FAILURE" and x["may_pass"] is False for x in dm["failure_propagation_rules"] if "may_pass" in x))
    check("V11","dependencies","historical and future dependency types are explicit",{d["dependency_type"] for d in D.values()}=={"HISTORICAL_DEPENDENCY","FUTURE_ENGINEERING_DEPENDENCY"})
    check("V12","dependencies","conflicts do not enter dependency graph",not any(d["relation"]=="CONFLICTS_WITH" for d in D.values()) and all(c["dependency"] is False for c in conflicts["conflicts"]))
    check("V13","dependencies","lineage and supersession remain separate",not lineage["supersessions"] and all(x["dependency"] is False for x in lineage["lineage"]) and not any(d["relation"] in {"SUPERSEDES","DERIVED_FROM"} for d in D.values()))
    check("V14","dependencies","matrix covers all obligation pairs",matrix["columns"]==list(O) and len(matrix["rows"])==len(O) and all(set(r["cells"])==set(O) for r in matrix["rows"]))
    check("V15","dependencies","dependency IDs resolve in obligation adjacency",all(set(o["dependencies"]+o["dependents"])<=set(D) for o in obs))
    check("V16","dependencies","required closures are blocked rather than falsely verified",all(x["closure_status"]=="OBLIGATION_BLOCKED" for x in dm["required_closure"]))
    levels={o["obligation_id"]:int(o["dependency_level"][1:]) for o in obs}
    check("V17","dependencies","dependency layers do not place dependents below prerequisites",all(levels[d["from_obligation"]]>=levels[d["to_obligation"]] for d in D.values() if d["relation"]=="REQUIRES") and {x["layer"].split()[0] for x in dm["dependency_layers"]}=={"L1","L2","L3","L4","L5","L6"})

    # Four graph models and specialized matrices.
    check("G01","graphs","evidence graph is distinct and typed",evidence_graph["graph_type"]=="EVIDENCE_GRAPH" and all(e["relation"]=="SUPPORTS_PROPERTY" for e in evidence_graph["edges"]))
    check("G02","graphs","historical dependency graph excludes future edges",hist_graph["graph_type"]=="HISTORICAL_OBLIGATION_GRAPH" and hist_graph["future_edges_excluded"])
    check("G03","graphs","future engineering dependency graph does not relabel history",future_graph["graph_type"]=="FUTURE_ENGINEERING_OBLIGATION_GRAPH" and future_graph["historical_edges_not_relabelled"])
    check("G04","graphs","verification graph remains distinct",verify_graph["graph_type"]=="VERIFICATION_GRAPH" and all(e["relation"]=="VERIFIED_BY" for e in verify_graph["edges"]))
    check("G05","graphs","lineage graph has explicit version/status fields",lineage["graph_type"]=="OBLIGATION_LINEAGE_GRAPH" and all(set(["valid_from","valid_until","epistemic_status"])<=set(x) for x in lineage["lineage"]))
    check("G06","graphs","conflict graph carries semantic differences and resolution status",conflicts["graph_type"]=="OBLIGATION_CONFLICT_GRAPH" and all(c["semantic_difference"] and c["resolution_status"] in {"CONDITIONALLY_RESOLVED","UNRESOLVED","FALSE_CONFLICT"} for c in conflicts["conflicts"]))
    check("G07","graphs","dependency graph has distinct typed nodes and edges",dm["graph_type"]=="OBLIGATION_DEPENDENCY_GRAPH" and set(dm["nodes"])==set(O) and len(dm["edges"])==len(D))
    check("S01","specialized","failure classes separate obligation propagation states",set(["OBLIGATION_VIOLATED","OBLIGATION_UNVERIFIED","OBLIGATION_BLOCKED","OBLIGATION_SUPERSEDED","OBLIGATION_CONTRADICTED","OBLIGATION_DEPENDENCY_FAILURE"])<=set(fail["failure_classes"]))
    check("S02","specialized","security treats remote content as untrusted data",security["remote_content_rule"]["classification"]=="UNTRUSTED_INPUT_DATA" and security["remote_content_rule"]["trusted_execution"]=="NOT_EVIDENCED")
    check("S03","specialized","contract conclusions remain unknown under missing v7",contract["v7_contract_inventory"]["status"]=="INPUT_MISSING" and all(x["status"]=="UNKNOWN" for x in contract["contract_obligations"]))
    check("S04","specialized","nullability remains unknown without v7",all(x["current_value_domain"]=="UNKNOWN_NO_V7_CONTRACT" for x in nulls["fields"]))
    check("S05","specialized","API signatures do not prove semantics",all(set(x["semantic_contract"].values())<={"UNKNOWN_FROM_SIGNATURE","STRUCTURED_OBJECT","VARIES","UNKNOWN","PARTIAL"} for x in api["surfaces"]))
    check("S06","specialized","traceability resolves obligations, properties and tests",all(x["obligation"] in O and x["historical_property"] in P and x["test"] in T for x in trace["rows"]))
    check("S07","specialized","traceability includes dependency and verification result",all("dependency" in x and x["verification_result"]=="UNVERIFIED" for x in trace["rows"]))

    # Validate schema enum contracts against runtime registry.
    schemas={name:load("schema/"+name) for name in ["input-contract.schema.yaml","historical-property.schema.yaml","obligation.schema.yaml","obligation-dependency.schema.yaml","obligation-lineage.schema.yaml","obligation-conflict.schema.yaml","traceability.schema.yaml"]}
    check("C01","schemas","seven schemas are versioned 1.0",len(schemas)==7 and all(x["schema_version"]=="1.0" for x in schemas.values()))
    check("C02","schemas","obligation schema class enum excludes UNKNOWN",set(schemas["obligation.schema.yaml"]["properties"]["class"]["enum"])==CLASSES)
    check("C03","schemas","property schema uses required type enum",set(schemas["historical-property.schema.yaml"]["properties"]["property_type"]["enum"])==PROPERTY_TYPES)
    check("C04","schemas","dependency schema permits normative REQUIRES",set(schemas["obligation-dependency.schema.yaml"]["properties"]["relation"]["enum"])==RELATIONS)
    check("C05","schemas","traceability schema requires dependency and verification",{"dependency","verification_result"}<=set(schemas["traceability.schema.yaml"]["required"]))

    # Content coverage guards for the core historical model.
    ids=set(O)
    expected_ids={"OBL-CANDIDATE-IDENTITY","OBL-DEDUP-SCOPES","OBL-ACQ-BEFORE-INTERP","OBL-OBS-DISTINCT","OBL-RECOGNITION-DISTINCT","OBL-DISCOVERY-RECORD","OBL-EXPANSION-RECURSIVE","OBL-BOUNDED-CONCURRENCY","OBL-SCHEDULER-TERMINATION","OBL-PROVENANCE","OBL-REMOTE-DATA","OBL-RESOURCE","OBL-LIFECYCLE-OBS","OBL-CONTRACT-INPUT","OBL-PARSE-DEFECT"}
    check("M01","model","core obligation coverage is present",expected_ids<=ids)
    check("M02","model","candidate identity dimensions remain independent",set(data["candidate_identity"]["dimensions_kept_independent"])=={"normalized_target","type","origin","parent","provider","scope"})
    check("M03","model","deduplication scopes remain independent",{x["scope"] for x in data["deduplication_assessments"]}=={"queue","claim","processing","discovery","persistence","export"})
    check("M04","model","claim scope does not overstate thread/distributed atomicity",data["candidate_state_machine"]["thread_safety"]=="NOT_ESTABLISHED" and data["candidate_state_machine"]["distributed_atomicity"]=="NOT_ESTABLISHED")
    check("M05","model","termination remains an engineering strengthening",O["OBL-SCHEDULER-TERMINATION"]["strengthening"]=="ENGINEERING_STRENGTHENING")
    check("M06","model","cancellation API does not imply safety",O["OBL-CANCELLATION"]["class"]=="VERIFY" and O["OBL-CANCELLATION"]["epistemic_status"]=="SUPPORTED")
    check("M07","model","auditability is not inferred from logs",O["OBL-AUDIT"]["class"]=="VERIFY" and "not an audit trail" in O["OBL-AUDIT"]["rationale"].lower())
    check("M08","model","provenance visibility and integrity stay separate",O["OBL-PROVENANCE"]["class"]=="PRESERVE" and O["OBL-PROVENANCE-INTEGRITY"]["class"]=="VERIFY")
    check("M09","model","resource findings are static risk not incidents",all(x["vulnerability"]=="NOT_AUTOMATICALLY_A_VULNERABILITY" for x in data["resource_assessments"]["unbounded_findings"]))
    check("M10","model","future mechanisms remain unselected",all(x["status"]=="UNSELECTED" for x in data["future_design_decisions"]))
    check("M11","model","no externally visible API is invented",all(x["external_consumability"] in {"UNKNOWN","POSSIBLE_USER_FACING"} for x in api["surfaces"]))
    check("M12","model","historical parse defect is not future behavior",O["OBL-PARSE-DEFECT"]["class"]=="REJECT" and O["OBL-PARSE-DEFECT"]["epistemic_status"]=="PROVED")
    check("M13","model","provider ordering uncertainty remains explicit",O["OBL-PROVIDER-ORDER"]["epistemic_status"]=="UNKNOWN" and O["OBL-PROVIDER-ORDER"]["strength"]=="CONDITIONAL")
    check("M14","model","v7 gate is required without inventing contract conclusions",O["OBL-CONTRACT-INPUT"]["class"]=="VERIFY" and O["OBL-CONTRACT-INPUT"]["strength"]=="REQUIRED" and contract["v7_contract_inventory"]["contracts_consumed"]==0)

    # Q01-Q16 final quality gates. Q01 is intentionally blocked by the real package.
    blocked("Q01","quality","all required inputs exist, are valid, verified and temporally clean","Protocol-v1 validation fails and Protocol-v4-v7 required artifacts are missing; acceptance cannot proceed.")
    check("Q02","quality","every historical property traces to normalized evidence",all(p["evidence_refs"] and set(p["evidence_refs"])<=set(E) for p in props))
    check("Q03","quality","every obligation has historical property/evidence justification",all(o["source_properties"] and o["source_evidence"] and o["rationale"] for o in obs))
    check("Q04","quality","class strength category epistemic and lifecycle are separately declared",all(all(k in o for k in ["class","strength","final_category","epistemic_status","status"]) for o in obs))
    check("Q05","quality","every dependency has direction, condition, reason, provenance and scope",all(all(k in d for k in ["from_obligation","to_obligation","condition","reason","evidence","scope","valid_from","valid_until"]) for d in D.values()))
    check("Q06","quality","REQUIRES graph is acyclic or cycles would be reported",cycles==[] and dm["cycle_status"]=="ACYCLIC")
    check("Q07","quality","every REQUIRED obligation exposes closure",all(o["obligation_id"] in req_closure for o in obs if o["strength"]=="REQUIRED"))
    check("Q08","quality","dependency criticality and ordering are reproducible",len(critical["records"])==len(O) and len(order)==len(O))
    check("Q09","quality","dependency failure propagation is encoded",all("dependent_failures" in t and t["failure_class"] in fail["failure_classes"] for t in tests))
    check("Q10","quality","historical and future dependency models remain distinct",hist_graph["graph_type"]!=future_graph["graph_type"])
    check("Q11","quality","dependency, lineage, conflict and verification semantics remain distinct",not any(d["relation"] in {"CONFLICTS_WITH","SUPERSEDES","VERIFIED_BY"} for d in D.values()) and all(x["relation"]=="CONFLICTS_WITH" for x in conflicts["conflicts"]) and all(x["relation"]=="VERIFIED_BY" for x in verify_graph["edges"]))
    check("Q12","quality","IMPLEMENTED never implies VERIFIED",not any(o["status"] in {"IMPLEMENTED","VERIFIED"} for o in obs))
    check("Q13","quality","future strengthenings are explicit and not historical claims",all(o["strengthening"]!="HISTORICAL" for o in obs if o["final_category"]=="FUTURE_STRENGTHENING"))
    check("Q14","quality","unknowns and contradictions remain preserved",len(E["NE-V9-UNKNOWNS"]["normalized_payload"])>0 and len(E["NE-V9-CONTRADICTIONS"]["normalized_payload"])>0)
    check("Q15","quality","all reports carry failed-input disposition",all("INPUT_CONTRACT_FAILED" in (OUT/n).read_text(encoding="utf-8") for n in ["README.md","DEPENDENCY-CLOSURE.md","OBLIGATION-LINEAGE-GRAPH.md","HISTORICAL-REGRESSION-SUITE.md","COMPATIBILITY-ENVELOPE.md","ENGINEERING-OBLIGATION-REPORT.md"]))
    det_path=OUT/"DETERMINISM-VALIDATION.yaml"
    det=load("DETERMINISM-VALIDATION.yaml") if det_path.is_file() else {}
    check("Q16","quality","all generator-owned outputs reproduce byte-for-byte",meta["deliverables"]==DELIVERABLES and set(meta["counts"])=={"normalized_evidence","facts","properties","obligations","requirements","dependencies","invariants","tests"} and det.get("status")=="PASS" and det.get("summary",{}).get("total")==len(DELIVERABLES) and det.get("summary",{}).get("identical")==len(DELIVERABLES) and {x["path"] for x in det.get("files",[])}==set(DELIVERABLES))

    # Authoritative documents and generation hygiene.
    check("H01","hygiene","authoritative documents remain outside generated corpus",all("Userscript Discovery Prototype.md" not in x and "Continue Architecture Planning.md" not in x for x in DELIVERABLES))
    check("H02","hygiene","no Python cache artifacts exist",not any(HS.rglob("__pycache__")) and not any(HS.rglob("*.pyc")))
    check("H03","hygiene","tool hashes are current",meta["tools"]["generator"]==sha(HS/"tools/build_historical_obligations.py") and meta["tools"]["validator"]==sha(HS/"tools/validate_historical_obligations.py"))
    check("H04","hygiene","all machine artifacts are JSON-compatible YAML",all(parseable(OUT/n) for n in DELIVERABLES if n.endswith(".yaml")))
    check("H05","hygiene","no rejected current/future documents enter normalized evidence",not any(e["provenance"]["source_path"] in {"Userscript Discovery Prototype.md","Continue Architecture Planning.md"} for e in E.values()))
    return finish(checks,data)


def find_ic(ic,cid): return next(x["result"] for x in ic["integrity_checks"] if x["check_id"]==cid)
def emitted_failures(ic): return {x["state"] for x in ic["failure_states"]}
def parseable(path):
    try: json.loads(path.read_text(encoding="utf-8")); return True
    except Exception:return False

def find_cycles(nodes,graph):
    visiting=set();done=set();path=[];cycles=[]
    def v(n):
        if n in visiting:
            cycles.append(path[path.index(n):]+[n]);return
        if n in done:return
        visiting.add(n);path.append(n)
        for x in graph.get(n,[]):v(x)
        path.pop();visiting.remove(n);done.add(n)
    for n in nodes:v(n)
    return cycles

def finish(checks,data):
    passed=sum(x["result"]=="PASS" for x in checks);failed=sum(x["result"]=="FAIL" for x in checks);blocked=sum(x["result"]=="BLOCKED" for x in checks)
    counts=(data or {}).get("metadata",{}).get("counts",{})
    report={"schema_version":"1.0","protocol":"v10.1","overall_status":"FAIL" if failed else "STRUCTURAL_PASS_INPUT_BLOCKED" if blocked else "PASS","acceptance":"INPUT_CONTRACT_FAILED" if not failed else "VALIDATION_FAILED","summary":{"total":len(checks),"passed":passed,"failed":failed,"blocked":blocked},"corpus_counts":counts,"checks":checks}
    (OUT/"VALIDATION.yaml").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    lines=["# Protocol-v10.1 Validation","",f"**Overall:** `{report['overall_status']}`",f"**Acceptance:** `{report['acceptance']}`",f"**Checks:** {passed} PASS / {failed} FAIL / {blocked} BLOCKED ({len(checks)} total)","","Q01 is intentionally blocked by the actual upstream package; structural success does not convert missing or invalid inputs into acceptance.","","| ID | Category | Result | Description | Detail |","|---|---|---|---|---|" ]
    for c in checks:lines.append("| %s | %s | %s | %s | %s |"%(c["check_id"],c["category"],c["result"],c["description"].replace("|","\\|"),c["detail"].replace("|","\\|")))
    (OUT/"VALIDATION.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(f"{passed} PASS / {failed} FAIL / {blocked} BLOCKED ({len(checks)} checks); {report['overall_status']}")
    return 1 if failed else 0
if __name__=="__main__":sys.exit(main())
