#!/usr/bin/env python3
"""Independent Protocol-v8 validator; deliberately does not import the generator."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[2]
HS = ROOT / "historical-source"
OUT = HS / "security"
MANIFEST_PATH = OUT / "SECURITY-MANIFEST.yaml"
LEVELS = {"F0", "F1", "F2", "F3", "F4", "F5", "F6", "UNKNOWN"}
FAILURES = {
    "INPUT_FAILURE", "VALIDATION_FAILURE", "CONFIGURATION_FAILURE", "ACQUISITION_FAILURE", "NETWORK_FAILURE", "TIMEOUT",
    "HTTP_FAILURE", "PARSING_FAILURE", "RECOGNITION_FAILURE", "PROVIDER_FAILURE", "DISCOVERY_FAILURE", "EXPANSION_FAILURE",
    "DEDUPLICATION_FAILURE", "SCHEDULER_FAILURE", "CONCURRENCY_FAILURE", "STATE_FAILURE", "PERSISTENCE_FAILURE",
    "EXPORT_FAILURE", "UI_FAILURE", "RESOURCE_EXHAUSTION", "CANCELLATION", "UNKNOWN_FAILURE",
}
STAGES = {"INPUT", "VALIDATION", "ACQUISITION", "OBSERVATION", "RECOGNITION", "DISCOVERY", "EXPANSION", "SCHEDULING", "PERSISTENCE", "EXPORT", "UI", "CROSS_CUTTING"}
CLAIM_TYPES = {"SECURITY_PROPERTY", "SECURITY_MECHANISM", "SECURITY_ASSUMPTION", "SECURITY_GOAL", "SECURITY_GUARANTEE"}
REQUIRED = {
    "README.md", "FAILURE-EVENTS.yaml", "FAILURE-MATRIX.yaml", "FAILURE-PROPAGATION.md", "RETRY-HISTORY.md",
    "TIMEOUT-HISTORY.md", "CANCELLATION-HISTORY.md", "RESOURCE-BOUND-HISTORY.md", "CONCURRENCY-SAFETY-HISTORY.md",
    "DATA-INTEGRITY-HISTORY.md", "PROVENANCE-INTEGRITY-HISTORY.md", "TRUST-BOUNDARIES.yaml", "AUTHORITY-HISTORY.md",
    "USERSCRIPT-PERMISSION-HISTORY.md", "ORIGIN-SCOPE-HISTORY.md", "URL-TRUST-HISTORY.md", "CODE-DATA-BOUNDARY-HISTORY.md",
    "PARSER-SAFETY-HISTORY.md", "RESOURCE-EXHAUSTION-HISTORY.md", "OBSERVABILITY-HISTORY.md", "AUDITABILITY-HISTORY.md",
    "SECURITY-INVARIANT-HISTORY.md", "THREAT-MODEL-HISTORY.md", "SECURITY-REGRESSIONS.md", "SECURITY-IMPROVEMENTS.md",
    "FAILURE-CONTRACT-MAP.md", "SECURITY-ARCHITECTURE-MAP.md", "TRUST-BOUNDARY-MATRIX.yaml",
    "SECURITY-EVOLUTION-GRAPH.md", "SECURITY-ARCHAEOLOGY-REPORT.md", "SECURITY-FUNCTION-TRADEOFFS.md", "PRIVILEGED-API-HISTORY.md",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str:
    return sha(path.read_bytes())


def independently_mask_comments(text: str) -> str:
    chars=list(text); i=0; state="code"; quote=""
    while i<len(chars):
        c=chars[i]; n=chars[i+1] if i+1<len(chars) else ""
        if state=="code":
            if c=="/" and n=="/": chars[i]=chars[i+1]=" "; i+=2; state="line"; continue
            if c=="/" and n=="*": chars[i]=chars[i+1]=" "; i+=2; state="block"; continue
            if c in "'\"`": quote=c; state="string"
            i+=1
        elif state=="line":
            if c=="\n": state="code"
            else: chars[i]=" "
            i+=1
        elif state=="block":
            if c=="*" and n=="/": chars[i]=chars[i+1]=" "; i+=2; state="code"
            else:
                if c not in "\r\n": chars[i]=" "
                i+=1
        else:
            if c=="\\": i+=2
            elif c==quote: state="code"; i+=1
            else: i+=1
    return "".join(chars)

checks: list[dict[str, str]] = []
def check(name: str, test: Callable[[], tuple[bool, str] | bool]) -> None:
    try:
        value = test()
        ok, detail = value if isinstance(value, tuple) else (bool(value), "")
    except Exception as exc:
        ok, detail = False, f"{type(exc).__name__}: {exc}"
    checks.append({"check": name, "result": "PASS" if ok else "FAIL", "detail": detail})

check("security output directory exists", lambda: (OUT.is_dir(), str(OUT)))
check("manifest exists and parses", lambda: (MANIFEST_PATH.is_file() and load(MANIFEST_PATH)["schema_version"] == 8, str(MANIFEST_PATH)))
if not MANIFEST_PATH.exists():
    print(json.dumps({"overall":"FAIL", "checks":checks}, indent=2)); raise SystemExit(1)
manifest = load(MANIFEST_PATH)

check("all required Protocol-v8 deliverables exist", lambda: (not (missing := sorted(REQUIRED - {p.name for p in OUT.iterdir() if p.is_file()})), f"missing={missing}"))
check("all seven per-version reports exist", lambda: (all((OUT/f"v0.{x}.md").exists() for x in ["1.0","2.0","3.0","4.0","5.0","6.0","7.1"]), "v0.1.0 through v0.7.1"))
check("generator and validator are bound", lambda: (manifest["tool_hashes"]["generator"] == sha_file(HS/"tools/build_security_archaeology.py") and manifest["tool_hashes"]["validator"] == sha_file(Path(__file__)), str(manifest["tool_hashes"])))
check("every bound input hash matches", lambda: (not (bad := [p for p,h in manifest["input_hashes"].items() if not (ROOT/p).exists() or sha_file(ROOT/p) != h]), f"bad={bad}"))
check("every generator output hash matches", lambda: (not (bad := [p for p,h in manifest["output_hashes"].items() if not (ROOT/p).exists() or sha_file(ROOT/p) != h]), f"bad={bad}"))
check("manifest output count is exact", lambda: (manifest["counts"]["generator_outputs"] == len(manifest["output_hashes"])+1, f"declared={manifest['counts']['generator_outputs']} hashed={len(manifest['output_hashes'])}"))

recon = load(HS/"RECONSTRUCTION-MANIFEST.yaml")
semantic = [x for x in recon["snapshots"] if x["reconstruction"]["status"] in {"EXACT","MECHANICALLY_COMPOSED"}]
partial = [x for x in recon["snapshots"] if x["reconstruction"]["status"] == "PARTIAL"]
semantic_ids = {x["snapshot_id"] for x in semantic}
partial_ids = {x["snapshot_id"] for x in partial}
check("scope has 12 complete semantic snapshots", lambda: (set(manifest["scope"]["semantic_snapshots"]) == semantic_ids and len(semantic_ids)==12, str(sorted(semantic_ids))))
check("two partial variants remain uncertainty-only", lambda: (set(manifest["scope"]["partial_uncertainty_snapshots"]) == partial_ids and len(partial_ids)==2 and not (partial_ids & set(manifest["scope"]["semantic_snapshots"])), str(sorted(partial_ids))))
def upstream_truth() -> tuple[bool,str]:
    actual={
        "v1_v3_present": all((HS/x).exists() for x in ["SOURCE-MANIFEST.yaml","LINEAGE.yaml","RECONSTRUCTION-MANIFEST.yaml"]),
        "v1_validation": load(HS/"VALIDATION.yaml").get("overall","UNKNOWN") if (HS/"VALIDATION.yaml").exists() else "MISSING",
        "v3_validation": load(HS/"RECONSTRUCTION-VALIDATION.yaml").get("overall","UNKNOWN") if (HS/"RECONSTRUCTION-VALIDATION.yaml").exists() else "MISSING",
        "v4_present":(HS/"verification").exists(), "v5_present":(HS/"algorithm").exists(), "v6_present":(HS/"architecture").exists(), "v7_present":(HS/"contracts").exists(),
    }
    actual["all_required_verified_inputs_available"]=actual["v1_validation"]=="PASS" and actual["v3_validation"]=="PASS" and all(actual[x] for x in ["v4_present","v5_present","v6_present","v7_present"])
    expected_acceptance="ELIGIBLE" if actual["all_required_verified_inputs_available"] else "BLOCKED_MISSING_OR_FAILED_UPSTREAM"
    return manifest["upstream_availability"]==actual and manifest["prerequisite_acceptance"]==expected_acceptance,str(manifest["upstream_availability"])
check("upstream availability and prerequisite acceptance are reported truthfully", upstream_truth)

# Directional evidence verification.
ev_rows = load(OUT/"EVIDENCE.yaml")["evidence"]
ev = {x["evidence_id"]:x for x in ev_rows}
check("evidence IDs are unique", lambda: (len(ev)==len(ev_rows)==manifest["counts"]["evidence"], f"rows={len(ev_rows)} unique={len(ev)}"))
def evidence_valid() -> tuple[bool,str]:
    bad=[]
    for row in ev_rows:
        path=ROOT/row["path"]
        if not path.exists() or sha_file(path)!=row["source_sha256"]:
            bad.append((row["evidence_id"],"source")); continue
        raw=path.read_bytes()
        if row["kind"]=="BOUNDED_ABSENCE_SEARCH":
            try:
                corpus=independently_mask_comments(raw.decode("utf-8")) if row.get("search_scope")=="COMMENT_MASKED_CODE_WITH_STRINGS" else raw.decode("utf-8")
                found=re.search(row["query"],corpus,re.I|re.S) is not None
            except re.error: found=True
            if found: bad.append((row["evidence_id"],"absence-query-found-or-invalid"))
        else:
            a,b=row["byte_start"],row["byte_end"]
            if not (0<=a<=b<=len(raw)) or sha(raw[a:b])!=row["range_sha256"]: bad.append((row["evidence_id"],"range"))
    return not bad,f"bad={bad[:12]} total={len(bad)}"
check("all evidence byte ranges and bounded absences independently verify", evidence_valid)
check("all historical evidence flows source-to-derived", lambda: (all("TO_DERIVED" in x["direction"] or "TO_BOUNDED" in x["direction"] or x["snapshot_id"] is None for x in ev_rows), f"rows={len(ev_rows)}"))
check("no partial snapshot is used as semantic evidence", lambda: (all(x.get("snapshot_id") not in partial_ids for x in ev_rows), "partial evidence count="+str(sum(x.get("snapshot_id") in partial_ids for x in ev_rows))))

# Every evidence reference in outputs must resolve.
def collect_refs(value: Any) -> list[str]:
    out=[]
    if isinstance(value,dict):
        for k,v in value.items():
            if k=="evidence" and isinstance(v,list): out += [x for x in v if isinstance(x,str)]
            else: out += collect_refs(v)
    elif isinstance(value,list):
        for x in value: out += collect_refs(x)
    return out
refs=[]
for p in OUT.glob("*.yaml"):
    if p.name in {"EVIDENCE.yaml","SECURITY-MANIFEST.yaml","VALIDATION.yaml"}: continue
    refs += collect_refs(load(p))
check("all machine-ledger evidence references resolve", lambda: (not (bad:=sorted(set(refs)-set(ev))), f"references={len(refs)} unresolved={bad[:10]}"))

fail_doc=load(OUT/"FAILURE-EVENTS.yaml"); failures=fail_doc["failures"]
check("stable failure taxonomy is exact", lambda: (set(fail_doc["failure_taxonomy"])==FAILURES, str(sorted(fail_doc["failure_taxonomy"]))))
check("failure stages and containment vocabularies are exact", lambda: (set(fail_doc["stage_registry"])==STAGES and set(fail_doc["containment_levels"])==LEVELS, f"stages={fail_doc['stage_registry']} levels={fail_doc['containment_levels'].keys()}"))
required_failure_fields={"failure_id","version","stage","operation","failure_type","trigger","detection","representation","propagation","containment","recovery","logging","provenance_effect","evidence","status"}
check("failure event schema is complete", lambda: (failures and all(required_failure_fields<=set(x) for x in failures), f"events={len(failures)}"))
check("failure events use valid taxonomies", lambda: (all(x["failure_type"] in FAILURES and x["stage"] in STAGES and x["containment_level"] in LEVELS for x in failures), f"events={len(failures)}"))
check("failure event count matches manifest", lambda: (len(failures)==manifest["counts"]["failure_events"], str(len(failures))))
check("static failure events never claim runtime occurrence", lambda: (all(x["runtime_occurrence_proved"] is False for x in failures), f"events={len(failures)}"))
check("containment claims are evidence-backed", lambda: (all(x["evidence"] and x["containment"]==fail_doc["containment_levels"][x["containment_level"]] for x in failures), f"events={len(failures)}"))
check("unknown failure remains available and no category is forced", lambda: ("UNKNOWN_FAILURE" in fail_doc["failure_taxonomy"] and any(x["failure_type"]=="UNKNOWN_FAILURE" for x in failures), "unknown events="+str(sum(x["failure_type"]=="UNKNOWN_FAILURE" for x in failures))))

matrix=load(OUT/"FAILURE-MATRIX.yaml")["matrix"]
check("failure matrix covers every category in every snapshot", lambda: (len(matrix)==len(semantic_ids)*len(FAILURES) and {(x["snapshot_id"],x["failure"]) for x in matrix}=={(s,f) for s in semantic_ids for f in FAILURES}, f"rows={len(matrix)}"))
stage_model=load(OUT/"FAILURE-STAGE-MODEL.yaml")["stages"]
check("failure model covers all eight pipeline stages plus cross-cutting stages in every snapshot", lambda: (len(stage_model)==len(semantic_ids)*len(STAGES)==manifest["counts"]["failure_stage_rows"] and {(x["snapshot_id"],x["stage"]) for x in stage_model}=={(s,t) for s in semantic_ids for t in STAGES} and all(x["failure_sources"] and x["detection_points"] and x["representations"] and x["propagation"] and x["containment"] and x["recovery"] and x["logging"] and x["provenance"] and x["evidence"] for x in stage_model), f"rows={len(stage_model)}"))
check("failure semantics use four-way evidence labels", lambda: (all(x[k] in {"PROVED","SUPPORTED","INFERRED","UNKNOWN"} for x in matrix for k in ["detection","propagation","containment","recovery","observable"]), f"rows={len(matrix)}"))
prop=load(OUT/"FAILURE-PROPAGATION.yaml")["edges"]
check("failure propagation edges resolve and carry evidence", lambda: (prop and all(x["failure_id"] in {f["failure_id"] for f in failures} and x["confidence"] in {"PROVED","SUPPORTED","INFERRED","UNKNOWN"} and x["evidence"] for x in prop), f"edges={len(prop)}"))

silent=load(OUT/"SILENT-FAILURES.yaml")
check("silent failure candidates use exact conservative classes", lambda: (set(silent["classification_registry"])=={"INTENTIONAL_SILENCE","UNEXPLAINED_SILENCE","ERROR_SUPPRESSION","UNKNOWN"} and all(x["classification"] in set(silent["classification_registry"]) and x["bug_claimed"] is False for x in silent["failures"]), f"rows={len(silent['failures'])}"))
info=load(OUT/"FAILURE-INFORMATION.yaml")["handlers"]
check("error information preservation covers required fields", lambda: (info and all(set(x["preserved"])|set(x["not_evidenced"])=={"error_type","message","source","candidate","provider","operation","timestamp","stack","request","response","retry_count"} for x in info), f"handlers={len(info)}"))

retry=load(OUT/"RETRY-HISTORY.yaml")["snapshots"]
timeout=load(OUT/"TIMEOUT-HISTORY.yaml")["snapshots"]
cancel=load(OUT/"CANCELLATION-HISTORY.yaml")["snapshots"]
check("retry history covers snapshots and rejects recursion inference", lambda: (len(retry)==12 and all(x["recursion_is_retry"] is False and x["backoff"] and x["terminal_failure"] for x in retry), f"rows={len(retry)}"))
check("implemented retry requires count/action evidence", lambda: (all(len(x["evidence"])>=2 for x in retry if x["retry"]=="IMPLEMENTED"), "implemented="+str(sum(x["retry"]=="IMPLEMENTED" for x in retry))))
check("timeout scopes remain independently tracked", lambda: (len(timeout)==12 and all(x["candidate_timeout"] and x["worker_timeout"] and x["scan_timeout"] and x["global_timeout"] for x in timeout), f"rows={len(timeout)}"))
check("cancellation does not promote stop controls to operation cancellation", lambda: (len(cancel)==12 and all(x["stop_button_is_not_proof"] is True and x["candidate"]=="NO_PER_CANDIDATE_TOKEN_EVIDENCED" for x in cancel), f"rows={len(cancel)}"))

bounds=load(OUT/"RESOURCE-BOUNDS.yaml")["bounds"]
risks_doc=load(OUT/"RESOURCE-EXHAUSTION.yaml"); risks=risks_doc["risks"]
check("resource bound count and schemas match", lambda: (len(bounds)==manifest["counts"]["resource_bounds"] and all(x["first_appearance"] and x["scope"] and x["enforcement"] and x["failure_behavior"] and x["evidence"] for x in bounds), f"bounds={len(bounds)}"))
check("resource risks distinguish static risk from incidents", lambda: (len(risks)==manifest["counts"]["resource_risks"] and all(x["classification"] in {"OBSERVED_RISK","MITIGATED","UNMITIGATED","UNKNOWN"} and x["actual_exhaustion_or_exploit"]=="NOT_EVIDENCED" for x in risks), f"risks={len(risks)}"))

state=load(OUT/"CONCURRENCY-STATE.yaml")["structures"]
claim=load(OUT/"CLAIM-SAFETY.yaml")["snapshots"]
dup=load(OUT/"DUPLICATE-PROCESSING.yaml")["snapshots"]
races=load(OUT/"RACE-ANALYSIS.yaml")["races"]
check("shared state records writers readers await and ordering", lambda: (len(state)==manifest["counts"]["shared_structures"] and all(x["writers"] is not None and x["readers"] is not None and x["await_boundaries"] is not None and x["ordering_assumptions"] and x["thread_safe_claim"] is False for x in state), f"rows={len(state)}"))
check("claim analysis separates six ownership/safety dimensions", lambda: (len(claim)==12 and all(x["claim_atomicity"] and x["claim_ownership"] and x["processing_exclusivity"] and x["completion_ownership"] and x["failure_ownership"] and x["requeue"] for x in claim), f"rows={len(claim)}"))
check("claim analysis rejects thread/distributed generalization", lambda: (all(x["thread_safety"]=="NOT_ESTABLISHED" and x["distributed_atomicity"]=="NOT_ESTABLISHED" and x["cross_await_atomicity"]=="NOT_CLAIMED" for x in claim), f"rows={len(claim)}"))
check("duplicate processing factors remain separate", lambda: (len(dup)==12 and all(x["global_uniqueness_guarantee"]=="NOT_ESTABLISHED" and x["normalization_mismatch"] for x in dup), f"rows={len(dup)}"))
check("race candidates are theoretical rather than demonstrated", lambda: (len(races)==manifest["counts"]["race_candidates"] and all(x["classification"]=="THEORETICAL_INTERLEAVING_NOT_DEMONSTRATED_FAILURE" and x["observable_consequence"]=="UNKNOWN_NOT_DEMONSTRATED" for x in races), f"rows={len(races)}"))

data=load(OUT/"DATA-INTEGRITY.yaml"); provenance=load(OUT/"PROVENANCE-INTEGRITY.yaml")["snapshots"]
check("data integrity distinguishes possible observed prevented unknown", lambda: (set(data["classification_registry"])=={"POSSIBLE","OBSERVED","PREVENTED","UNKNOWN"} and all(x["classification"] in set(data["classification_registry"]) and x["runtime_failure_observed"] is False for x in data["conditions"]), f"conditions={len(data['conditions'])}"))
check("tampering surfaces are only integrity weaknesses", lambda: (all(x["classification"]=="INTEGRITY_WEAKNESS" and x["malicious_tampering_claimed"] is False for x in data["weaknesses"]), f"weaknesses={len(data['weaknesses'])}"))
check("provenance tracks all four edges independently", lambda: (len(provenance)==12 and all([e["field"] for e in x["edges"]]==["observationId","candidateId","parent","origin"] and x["integrity_guarantee"]=="NOT_ESTABLISHED" for x in provenance), f"rows={len(provenance)}"))

trust=load(OUT/"TRUST-BOUNDARIES.yaml")["boundaries"]
trust_required={"boundary","source","sink","data","validation","authority","sanitization","isolation","evidence"}
check("trust-boundary inventory covers twelve potential boundaries per snapshot", lambda: (len(trust)==12*12==manifest["counts"]["trust_boundaries"] and all(trust_required<=set(x) for x in trust), f"rows={len(trust)}"))
check("internal scheduler boundaries are not auto-promoted to trust boundaries", lambda: (all(x["boundary_status"]=="INTERNAL_AUTHORITY_BOUNDARY_NOT_PROVED_TRUST" for x in trust if x["boundary"]=="SCHEDULER" and x["authority"]!="NOT_EVIDENCED"), "scheduler rows checked"))
check("no trust boundary claims a security guarantee", lambda: (all(x["security_guarantee"]=="NOT_ESTABLISHED" for x in trust), f"rows={len(trust)}"))
matrix2=load(OUT/"TRUST-BOUNDARY-MATRIX.yaml")["matrix"]
check("trust matrix covers five named boundaries per snapshot", lambda: (len(matrix2)==12*5 and {x["boundary"] for x in matrix2}=={"NETWORK","PROVIDER_CODE","SCHEDULER","STORAGE","UI"} and all(x["guarantee"]=="UNKNOWN" for x in matrix2), f"rows={len(matrix2)}"))

auth=load(OUT/"AUTHORITY-HISTORY.yaml")["authorities"]
check("authority required/granted/used/exposure remain distinct", lambda: (len(auth)==manifest["counts"]["authorities"] and all(x["authority_required"] and x["authority_granted"] and x["authority_used"] and x["unnecessarily_exposed"] and x["least_authority"]=="NOT_ESTABLISHED" for x in auth), f"rows={len(auth)}"))
check("capability-like patterns are not formal capability systems", lambda: (all(x["formal_capability_system"] is False for x in auth), f"rows={len(auth)}"))
migrations=load(OUT/"AUTHORITY-MIGRATION.yaml")["migrations"]
check("authority migrations preserve unknown lineage and consequences", lambda: (len(migrations)==manifest["counts"]["authority_migrations"] and all(x["relationship"]=="COMPARATIVE_AUTHORITY_CHANGE_NOT_PROVED_LINEAGE" and x["security_consequence"]=="UNKNOWN" and x["transition_confidence"] in {"PROVED","SUPPORTED","INFERRED","CONTRADICTED","UNKNOWN"} for x in migrations), f"rows={len(migrations)}"))
boundary_migrations=load(OUT/"SECURITY-BOUNDARY-MIGRATION.yaml")["migrations"]
check("security-boundary migrations remain comparative with unknown consequences", lambda: (len(boundary_migrations)==manifest["counts"]["security_boundary_migrations"] and all(x["classification"]=="COMPARATIVE_MOVEMENT_NOT_PROVED_LINEAGE" and x["security_consequence"]=="UNKNOWN" for x in boundary_migrations), f"rows={len(boundary_migrations)}"))
privileged=load(OUT/"PRIVILEGED-API-HISTORY.yaml")["apis"]
check("privileged API rows track permission and both data/error crossings", lambda: (len(privileged)==manifest["counts"]["privileged_apis"] and all(x["caller"] and x["permission"] and x["data_crossing_out"] and x["data_crossing_in"] and x["error_crossing"] and x["platform_semantics_verified"] is False for x in privileged), f"rows={len(privileged)}"))
tradeoffs=load(OUT/"SECURITY-FUNCTION-TRADEOFFS.yaml")["tradeoffs"]
check("security/function tradeoffs avoid measured or superiority claims", lambda: (len(tradeoffs)==manifest["counts"]["tradeoffs"] and all(x["measured_effect"]=="NOT_MEASURED" and x["superiority_claim"] is False for x in tradeoffs), f"rows={len(tradeoffs)}"))
providers=load(OUT/"PROVIDER-SAFETY.yaml")["providers"]
check("HTML JSON and text provider safety separates extraction from execution", lambda: (len(providers)==manifest["counts"]["provider_safety_rows"] and all(x["executes_embedded_content"]=="NOT_EVIDENCED" and x["security_guarantee"]=="NOT_ESTABLISHED" for x in providers), f"rows={len(providers)}"))
memory=load(OUT/"MEMORY-SAFETY.yaml")["snapshots"]
check("JavaScript memory surfaces and cleanup avoid memory-safety guarantee", lambda: (len(memory)==12 and all(x["surfaces"] and x["garbage_collection_behavior"]=="PLATFORM_DEPENDENT_UNKNOWN" and x["memory_safety_guarantee"]=="NOT_ESTABLISHED" for x in memory), f"rows={len(memory)}"))

permissions=load(OUT/"USERSCRIPT-PERMISSION-HISTORY.yaml")["snapshots"]
recon_by={x["snapshot_id"]:x for x in semantic}
def permissions_exact() -> tuple[bool,str]:
    bad=[]
    for row in permissions:
        d=recon_by[row["snapshot_id"]]["static_validation"]["userscript_metadata"]["directives"]
        for key in ["include","match","grant","connect","require","resource"]:
            if row[key]!=d.get(key,[]): bad.append((row["snapshot_id"],key))
    return len(permissions)==12 and not bad,f"rows={len(permissions)} bad={bad}"
check("userscript permissions exactly preserve parsed metadata", permissions_exact)
origin=load(OUT/"ORIGIN-SCOPE-HISTORY.yaml")["snapshots"]
check("origin scope separates metadata authority, policy, and use", lambda: (len(origin)==12 and all(x["metadata_authority"] and x["default_policy"] and x["authority_used"] and x["redirect_detection"]=="NOT_EVIDENCED" for x in origin), f"rows={len(origin)}"))
url=load(OUT/"URL-TRUST-HISTORY.yaml")["snapshots"]
check("URL trust covers scheme origin redirect credentials and local addresses", lambda: (len(url)==12 and all(x["scheme"] and x["origin"] and x["redirect"] and x["credentials"] and x["local_addresses"] and x["url_parser_is_not_policy"] is True for x in url), f"rows={len(url)}"))

code_data=load(OUT/"CODE-DATA-BOUNDARY-HISTORY.yaml")["snapshots"]
check("code/data history distinguishes absence evidence from security", lambda: (len(code_data)==12 and all(x["absence_is_not_security_guarantee"] is True and x["html_extraction_executes_scripts"]=="NOT_EVIDENCED" and x["json_strings_executed"]=="NOT_EVIDENCED" for x in code_data), f"rows={len(code_data)}"))
check("no acquired-content execution path is invented", lambda: (all(x["acquired_content_to_code_path"] in {"NO_EVIDENCE_OF_CODE_EXECUTION","EVIDENCED"} for x in code_data), str({x['acquired_content_to_code_path'] for x in code_data})))
parsers=load(OUT/"PARSER-SAFETY-HISTORY.yaml")
check("parser rows constrain security claims", lambda: (len(parsers["parsers"])==manifest["counts"]["parser_rows"] and all(x["external_entities"]=="UNKNOWN" and x["security_guarantee"]=="NOT_ESTABLISHED" for x in parsers["parsers"]), f"parsers={len(parsers['parsers'])}"))
check("regex risks use theoretical/supported/demonstrated/unknown vocabulary", lambda: (all(x["risk"] in {"THEORETICAL","SUPPORTED","DEMONSTRATED","UNKNOWN"} and x["demonstrated"] is False for x in parsers["regex_risks"]), f"regexes={len(parsers['regex_risks'])}"))

persist=load(OUT/"PERSISTENCE-INTEGRITY.yaml")["snapshots"]
exports=load(OUT/"EXPORT-INTEGRITY.yaml")["snapshots"]
check("persistence integrity does not invent atomicity or crash recovery", lambda: (len(persist)==12 and all(x["write_atomicity"]=="UNKNOWN" and x["crash_recovery"]=="UNKNOWN" for x in persist), f"rows={len(persist)}"))
check("export integrity distinguishes interpretation from compatibility", lambda: (len(exports)==12 and all(x["compatibility_guarantee"]=="NOT_ESTABLISHED" for x in exports), f"rows={len(exports)}"))
obs=load(OUT/"OBSERVABILITY-HISTORY.yaml")["snapshots"]
audit=load(OUT/"AUDITABILITY-HISTORY.yaml")["snapshots"]
check("observability separates detection from visibility", lambda: (len(obs)==12 and all(x["failure_detected_not_same_as_observable"] is True for x in obs), f"rows={len(obs)}"))
check("auditability is never called verified without execution", lambda: (len(audit)==12 and all(x["classification"] in {"NONE","PARTIAL","SUBSTANTIAL","VERIFIED","UNKNOWN"} and x["verified_by_execution"] is False and x["classification"]!="VERIFIED" for x in audit), f"rows={len(audit)}"))

invariants=load(OUT/"SECURITY-INVARIANT-HISTORY.yaml")
check("security claim types are exact and invariants cover seven per snapshot", lambda: (set(invariants["claim_types"])==CLAIM_TYPES and len(invariants["invariants"])==12*7 and all(x["claim_type"] in CLAIM_TYPES and x["mechanism_not_guarantee"] is True for x in invariants["invariants"]), f"rows={len(invariants['invariants'])}"))
threat=load(OUT/"THREAT-MODEL-HISTORY.yaml")
check("threat model preserves explicit implicit retrospective unknown", lambda: (set(threat["classification_registry"])=={"EXPLICIT_THREAT","IMPLICIT_THREAT","RETROSPECTIVE_THREAT","UNKNOWN"} and len(threat["snapshots"])==12 and all(x["complete_threat_model"]=="NOT_EVIDENCED" for x in threat["snapshots"]), f"rows={len(threat['snapshots'])}"))

changes=load(OUT/"SECURITY-CHANGES.yaml")["comparisons"]
check("branch-preserving security comparisons include adjacent and same-version variants", lambda: (len(changes)==29 and {x["relationship"] for x in changes}=={"ADJACENT_RECOVERED_VERSION_COMPARISON_NOT_LINEAGE","SAME_VERSION_VARIANT_COMPARISON_NOT_LINEAGE"} and all(x["motivation"]=="UNKNOWN" for x in changes), f"rows={len(changes)} relationships={sorted({x['relationship'] for x in changes})}"))
check("control disappearance is not auto-labelled regression", lambda: (all(x["regression"]=="NOT_PROVED_WITHOUT_LINEAGE_REQUIREMENT_AND_BEHAVIOR_EVIDENCE" and x["removal_classification"] in {"UNKNOWN","NONE"} for x in changes), f"rows={len(changes)}"))
archmap=load(OUT/"SECURITY-ARCHITECTURE-MAP.yaml")["mappings"]
check("security/architecture mapping rejects chronology as causality", lambda: (all(x["causality"] in {"EXPLICIT","SUPPORTED","CORRELATED","UNKNOWN"} and x["chronology_is_not_causality"] is True for x in archmap), f"rows={len(archmap)}"))
contractmap=load(OUT/"FAILURE-CONTRACT-MAP.yaml")["mappings"]
check("every failure-contract mapping remains test-unverified", lambda: (contractmap and all(x["test"]=="UNVERIFIED_NO_HISTORICAL_TEST_EVIDENCE" for x in contractmap), f"rows={len(contractmap)}"))

questions=load(OUT/"FINAL-QUESTIONS.yaml")["questions"]
check("all 23 final questions are answered and evidenced", lambda: ([x["number"] for x in questions]==list(range(1,24)) and len(questions)==manifest["counts"]["questions"] and all(x["question"] and x["answer"] and x["evidence"] for x in questions), f"rows={len(questions)}"))
ff=load(OUT/"FINAL-FAILURE-CLASSIFICATION.yaml")["classification"]
check("final failure classification has all seven sections", lambda: (set(ff)=={"OBSERVED_FAILURES","HANDLED_FAILURES","CONTAINED_FAILURES","RECOVERABLE_FAILURES","SILENT_FAILURES","POTENTIAL_FAILURE_MODES","UNVERIFIED_FAILURE_MODES"} and len({(x["operation"],x["classification"]) for x in ff["SILENT_FAILURES"]})==len(ff["SILENT_FAILURES"]), str(sorted(ff))))
fs=load(OUT/"FINAL-SECURITY-CLASSIFICATION.yaml")["classification"]
check("final security classification has all six sections", lambda: (set(fs)=={"HISTORICALLY_VERIFIED_SECURITY_MECHANISMS","HISTORICALLY_VERIFIED_SECURITY_PROPERTIES","SECURITY_GOALS_WITHOUT_ENFORCEMENT","RETROSPECTIVE_SECURITY_INTERPRETATIONS","CURRENT_PROPOSED_SECURITY_ARCHITECTURE","UNKNOWN"} and len({x["goal"] for x in fs["SECURITY_GOALS_WITHOUT_ENFORCEMENT"]})==len(fs["SECURITY_GOALS_WITHOUT_ENFORCEMENT"]), str(sorted(fs))))
check("historically verified properties are path-scoped", lambda: (all("scope" in x and x["scope"] for x in fs["HISTORICALLY_VERIFIED_SECURITY_PROPERTIES"]), f"properties={len(fs['HISTORICALLY_VERIFIED_SECURITY_PROPERTIES'])}"))

report=(OUT/"SECURITY-ARCHAEOLOGY-REPORT.md").read_text(encoding="utf-8")
check("final report contains governing distinctions", lambda: (all(x in report for x in ["FAILURE ≠ ERROR HANDLING ≠ FAILURE CONTAINMENT ≠ RECOVERY ≠ RESILIENCE","SECURITY MECHANISM ≠ SECURITY PROPERTY ≠ SECURITY ASSUMPTION ≠ SECURITY GUARANTEE","BOUNDARY ≠ TRUST BOUNDARY ≠ AUTHORITY BOUNDARY"]), "distinctions"))
check("final report contains questions 1 through 23", lambda: (all(f"### {i}." in report for i in range(1,24)), "23 headings"))
check("final report contains all failure classification headings", lambda: (all(x in report for x in ["OBSERVED FAILURES","HANDLED FAILURES","CONTAINED FAILURES","RECOVERABLE FAILURES","SILENT FAILURES","POTENTIAL FAILURE MODES","UNVERIFIED FAILURE MODES"]), "failure headings"))
check("final report contains all security classification headings", lambda: (all(x in report for x in ["HISTORICALLY VERIFIED SECURITY MECHANISMS","HISTORICALLY VERIFIED SECURITY PROPERTIES","SECURITY GOALS WITHOUT ENFORCEMENT","RETROSPECTIVE SECURITY INTERPRETATIONS","CURRENT/PROPOSED SECURITY ARCHITECTURE","UNKNOWN"]), "security headings"))
check("report expressly rejects mechanism-to-guarantee promotions", lambda: (all(x in report for x in ["A catch is not isolation","a Set is not global uniqueness","a worker pool is not a complete resource guarantee","a URL parser is not policy","a provenance field is not provenance integrity","an interface is not a security boundary"]), "guarantee rule"))
check("temporal contamination is expressly prohibited", lambda: (manifest["acceptance_constraints"]["temporal_backfill_forbidden"] is True and all(x["status"]=="CURRENT_OR_PROPOSED_NOT_BACKFILLED" for x in load(OUT/"CURRENT-PROPOSED-SECURITY.yaml")["concepts"]), "current concepts isolated"))
check("all eight acceptance constraints hold", lambda: (len(manifest["acceptance_constraints"])==8 and all(manifest["acceptance_constraints"].values()), str(manifest["acceptance_constraints"])))

# Authoritative root documents and caches.
def git_clean_docs() -> tuple[bool,str]:
    r=subprocess.run(["git","diff","--exit-code","HEAD","--","Userscript Discovery Prototype.md","Continue Architecture Planning.md"],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    return r.returncode==0,f"git-diff-exit={r.returncode}"
check("authoritative source documents remain unchanged", git_clean_docs)
check("no Python cache artifacts exist", lambda: (not (bad:=[str(x.relative_to(ROOT)) for x in HS.rglob("*.pyc")]+[str(x.relative_to(ROOT)) for x in HS.rglob("__pycache__")]), f"bad={bad}"))
check("no unexpected validator-owned files enter generator manifest", lambda: ("historical-source/security/VALIDATION.yaml" not in manifest["output_hashes"] and "historical-source/security/VALIDATION.md" not in manifest["output_hashes"], "validator outputs excluded"))

passed=sum(x["result"]=="PASS" for x in checks); failed=len(checks)-passed
overall="PASS" if failed==0 else "FAIL"
result={
    "schema_version":8, "protocol":"Historical Generic Discovery Failure, Security & Trust-Boundary Evolution Archaeology Protocol v8",
    "overall":overall, "acceptance":("ACCEPTED" if manifest["upstream_availability"]["all_required_verified_inputs_available"] else "PROVISIONAL_ONLY_UPSTREAM_BLOCKED") if overall=="PASS" else "REJECTED", "checks":checks,
    "counts":{"checks":len(checks),"passed":passed,"failed":failed,**{k:manifest["counts"][k] for k in ["evidence","failure_events","silent_failures","resource_bounds","resource_risks","shared_structures","race_candidates","trust_boundaries","authorities","parser_rows","questions"]}},
}
(OUT/"VALIDATION.yaml").write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8",newline="\n")
summary=["# Protocol-v8 Independent Validation","",f"**Overall: {overall}**",f"**Acceptance: {result['acceptance']}**","",f"Passed: {passed}/{len(checks)}",""]
summary += [f"- `{x['result']}` — {x['check']}: {x['detail']}" for x in checks]
(OUT/"VALIDATION.md").write_text("\n".join(summary)+"\n",encoding="utf-8",newline="\n")
print(json.dumps({"overall":overall,"acceptance":result["acceptance"],"checks":len(checks),"passed":passed,"failed":failed,**result["counts"]},indent=2))
raise SystemExit(0 if overall=="PASS" else 1)
