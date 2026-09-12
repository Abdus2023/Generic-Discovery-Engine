#!/usr/bin/env python3
"""Independent Protocol-v9 validator.

This module intentionally does not import the synthesis builder. It checks the persisted
corpus, evidence links, thresholds, state/delta semantics, prerequisites, and hashes.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[2]
HS = ROOT / "historical-source"
OUT = HS / "synthesis"
ALLOWED = {"PROVED", "SUPPORTED", "INFERRED", "CONJECTURED", "CONTRADICTED", "UNKNOWN"}
VERSIONS = ["v0.1.0", "v0.2.0", "v0.3.0", "v0.4.0", "v0.5.0", "v0.6.0", "v0.7.1"]
VI = {v: i for i, v in enumerate(VERSIONS)}
REQUIRED = [
    "EVIDENCE-LEDGER.yaml", "VERSION-STATE-VECTORS.yaml", "EVOLUTION-EVENTS.yaml",
    "EVOLUTION-MATRIX.csv", "CONCEPT-GENEALOGY.yaml", "ARCHITECTURE-EVOLUTION.md",
    "ALGORITHM-AND-SCHEDULER-EVOLUTION.md", "PROVIDER-AND-ACQUISITION-EVOLUTION.md",
    "OBSERVATION-PROVENANCE-EVOLUTION.md", "DISCOVERY-CLOSURE-ANALYSIS.md",
    "CONTRACT-SECURITY-INTEGRATION.md", "PLANNED-VS-IMPLEMENTED.md",
    "CAUSAL-CLAIMS.yaml", "INVARIANTS.yaml", "ARCHITECTURE-EPOCHS.md",
    "CONVERGENCE-AND-DIVERGENCE.md", "CAPABILITY-EMERGENCE.md", "COMPLEXITY-GROWTH.csv",
    "STABILITY-ANALYSIS.md", "CONTRADICTIONS.yaml", "UNCERTAINTIES.yaml", "CLAIMS.yaml",
    "HISTORICAL-CLAIMS-GRAPH.json", "SYNTHESIS-MANIFEST.yaml", "FINAL-HISTORICAL-REPORT.md",
]


def load(name: str) -> Any:
    return json.loads((OUT / name).read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    checks: list[dict[str, str]] = []

    def check(name: str, condition: bool | Callable[[], bool], detail: Any = "") -> None:
        try:
            ok = condition() if callable(condition) else bool(condition)
            d = detail() if callable(detail) else detail
        except Exception as exc:
            ok, d = False, f"{type(exc).__name__}: {exc}"
        checks.append({"check": name, "result": "PASS" if ok else "FAIL", "detail": str(d)})

    check("synthesis output directory exists", OUT.is_dir(), OUT)
    missing = [x for x in REQUIRED if not (OUT / x).is_file()]
    check("all 25 required Protocol-v9 deliverables exist", not missing, f"missing={missing}")
    if missing:
        write_reports(checks, {})
        return

    # Parse first so subsequent failures remain independently visible.
    parsed: dict[str, Any] = {}
    for n in REQUIRED:
        if n.endswith((".yaml", ".json")):
            try:
                parsed[n] = load(n)
                check(f"{n} parses", True, "JSON-compatible YAML/JSON")
            except Exception as exc:
                check(f"{n} parses", False, exc)
    if any(c["result"] == "FAIL" and c["check"].endswith("parses") for c in checks):
        write_reports(checks, {})
        return

    manifest = parsed["SYNTHESIS-MANIFEST.yaml"]
    ledger = parsed["EVIDENCE-LEDGER.yaml"]; evidence = ledger["evidence"]
    states = parsed["VERSION-STATE-VECTORS.yaml"]["states"]
    events = parsed["EVOLUTION-EVENTS.yaml"]["atomic_events"]
    causal = parsed["CAUSAL-CLAIMS.yaml"]["causal_claims"]
    genealogy = parsed["CONCEPT-GENEALOGY.yaml"]["genealogies"]
    contradictions = parsed["CONTRADICTIONS.yaml"]["contradictions"]
    uncertainties = parsed["UNCERTAINTIES.yaml"]["uncertainties"]
    claims = parsed["CLAIMS.yaml"]["claims"]
    invariants = parsed["INVARIANTS.yaml"]["invariants"]
    graph = parsed["HISTORICAL-CLAIMS-GRAPH.json"]

    # Prerequisite truth (never inferred from the synthesis itself).
    v1 = json.loads((HS / "VALIDATION.yaml").read_text())
    v3 = json.loads((HS / "RECONSTRUCTION-VALIDATION.yaml").read_text())
    v8 = json.loads((HS / "security" / "VALIDATION.yaml").read_text())
    sm = json.loads((HS / "security" / "SECURITY-MANIFEST.yaml").read_text())
    check("Protocol-v1 failure is preserved", v1["overall"] == "FAIL", v1["overall"])
    check("Protocol-v3 internal pass is preserved", v3["overall"] == "PASS", v3["overall"])
    check("Protocol-v8 provisional pass is preserved", v8["overall"] == "PASS" and v8["acceptance"] == "PROVISIONAL_ONLY_UPSTREAM_BLOCKED", v8["acceptance"])
    check("Protocol-v4 through v7 remain physically absent", all(not (HS / x).exists() for x in ["verification", "algorithm", "architecture", "contracts"]), "all absent")
    expected_up = {"v1_v3_present": True, "v1_validation": "FAIL", "v3_validation": "PASS", "v4_present": False, "v5_present": False, "v6_present": False, "v7_present": False, "all_required_verified_inputs_available": False}
    check("manifest upstream availability is exact", manifest["upstream_availability"] == expected_up, manifest["upstream_availability"])
    check("manifest prerequisite acceptance is blocked", manifest["prerequisite_acceptance"] == "BLOCKED_MISSING_OR_FAILED_UPSTREAM", manifest["prerequisite_acceptance"])
    check("manifest final acceptance is provisional only", manifest["acceptance"] == "PROVISIONAL_ONLY_UPSTREAM_BLOCKED", manifest["acceptance"])

    # Integrity check 1: source/input integrity.
    bad_inputs = []
    for r in manifest["verified_artifacts"]:
        p = ROOT / r["path"]
        if not p.is_file() or sha(p) != r["sha256"]:
            bad_inputs.append(r["path"])
    check("integrity 1/10: every consumed input hash matches", not bad_inputs, f"inputs={len(manifest['verified_artifacts'])} bad={bad_inputs}")
    diff = subprocess.run(["git", "diff", "--quiet", "--", "Userscript Discovery Prototype.md", "Continue Architecture Planning.md"], cwd=ROOT)
    check("authoritative root documents remain unchanged", diff.returncode == 0, f"git-diff-exit={diff.returncode}")

    # Manifest/output hash checks. Self is excluded by construction.
    declared = {Path(x["path"]).name: x for x in manifest["files"]}
    check("manifest binds all required outputs except itself", set(declared) == set(REQUIRED) - {"SYNTHESIS-MANIFEST.yaml"}, f"bound={len(declared)}")
    bad_outputs = [n for n, r in declared.items() if not (OUT / n).is_file() or sha(OUT / n) != r["sha256"] or (OUT / n).stat().st_size != r["size"]]
    check("all declared output hashes and sizes match", not bad_outputs, f"bad={bad_outputs}")
    check("manifest required list is exact and ordered", manifest["required_deliverables"] == REQUIRED, f"count={len(manifest['required_deliverables'])}")
    expected_tools = {
        "generator": sha(HS / "tools" / "build_historical_synthesis.py"),
        "validator": sha(HS / "tools" / "validate_historical_synthesis.py"),
    }
    check("generator and independent validator hashes are bound", manifest["tools"] == expected_tools, manifest["tools"])
    det_path = OUT / "DETERMINISM-VALIDATION.yaml"
    check("isolated randomized-hash determinism report exists", det_path.is_file(), det_path)
    try:
        det = json.loads(det_path.read_text())
    except Exception:
        det = {}
    check("all 25 required outputs regenerated byte-identically", det.get("result") == "PASS" and det.get("required_outputs") == 25 and det.get("byte_identical_outputs") == 25 and not det.get("differences"), f"seed={det.get('pythonhashseed')} matching={det.get('byte_identical_outputs')}/{det.get('required_outputs')}")
    det_by_name = {Path(x["path"]).name: x for x in det.get("files", [])}
    check("determinism report primary hashes match current outputs", set(det_by_name) == set(REQUIRED) and all(det_by_name[n]["primary_sha256"] == sha(OUT / n) for n in REQUIRED), f"records={len(det_by_name)}")

    # Integrity check 2: evidence integrity.
    eids = [x["evidence_id"] for x in evidence]
    check("integrity 2/10: evidence identifiers are unique", len(eids) == len(set(eids)), f"rows={len(eids)}")
    chain = ["SOURCE", "ARTIFACT", "SNAPSHOT", "VERIFIED_FACT", "EVOLUTION_EVENT", "CAUSAL_HYPOTHESIS", "SYNTHESIS"]
    check("every evidence row preserves the directional chain", all(x["directional_chain"] == chain for x in evidence), f"rows={len(evidence)}")
    check("evidence statuses use only allowed vocabulary", all(x["status"] in ALLOWED and x["confidence_ceiling"] in ALLOWED for x in evidence), str(Counter(x["status"] for x in evidence)))
    check("every evidence row keeps the v1 caveat", all(x["v1_integrity_caveat"] == "RAW_BYTES_AND_RANGES_FAIL_PINNED_VALIDATION" for x in evidence), f"rows={len(evidence)}")
    check("every evidence row forbids backward proof", all(x["backward_proof_forbidden"] is True for x in evidence), f"rows={len(evidence)}")
    bad_source = []
    for x in evidence:
        if "source_path" not in x:
            continue
        p = HS / x["source_path"]
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
            found = sorted({text.count("\n", 0, m.start()) + 1 for m in re.finditer(x["pattern"], text, re.I | re.M)})
            if not found or found != x["line_numbers"] or x["source_presence"] != "PRESENT":
                bad_source.append(x["evidence_id"])
        except Exception:
            bad_source.append(x["evidence_id"])
    check("direct source evidence reproduces exact line occurrences", not bad_source, f"direct={sum('source_path' in x for x in evidence)} bad={bad_source}")
    bad_up = [x["evidence_id"] for x in evidence if "upstream_output" in x and not (ROOT / x["upstream_output"]).is_file()]
    check("upstream evidence references present persisted outputs", not bad_up, f"bad={bad_up}")

    # Reconstruction completeness and branch preservation.
    reconstruction = json.loads((HS / "RECONSTRUCTION-MANIFEST.yaml").read_text())
    complete = [x for x in reconstruction["snapshots"] if x["reconstruction"]["status"] != "PARTIAL"]
    expected_sids = {x["snapshot_id"] for x in complete}
    check("twelve complete reconstructed occurrences are modeled", len(states) == 12 and {x["snapshot_id"] for x in states} == expected_sids, f"states={len(states)}")
    check("all seven recovered version labels are covered", {x["version"] for x in states} == set(VERSIONS), sorted({x["version"] for x in states}))
    expected_pairs = {(x["snapshot_id"], x["variant"]) for x in complete}
    check("same-version alternatives are preserved independently", {(x["snapshot_id"], x["variant"]) for x in states} == expected_pairs, f"pairs={len(expected_pairs)}")
    check("partial alternatives remain excluded from complete state vectors", not {"snapshot-0002", "snapshot-0004"} & {x["snapshot_id"] for x in states}, "partial uncertainty-only")

    dimensions = {"algorithm", "architecture", "contracts", "data", "execution", "concurrency", "providers", "provenance", "failure", "security", "observability", "validation"}
    check("state vectors keep all maturity dimensions independent", all(set(x["state_vector"]) == dimensions for x in states), sorted(dimensions))
    check("integrity 3/10: version/state coverage is complete", len(states) == 12 and all(x["version"] in VERSIONS for x in states), f"states={len(states)}")
    check("absent Protocol-v7 leaves every contract state UNKNOWN", all(x["state_vector"]["contracts"]["state"] == "UNKNOWN" and x["state_vector"]["contracts"]["status"] == "UNKNOWN" for x in states), "12/12 UNKNOWN")
    check("historical runtime is never silently claimed", all(x["state_vector"]["execution"]["historical_runtime"] == "UNKNOWN" for x in states), "12/12 UNKNOWN")
    check("snapshot-0009 parse failure is preserved", next(x for x in states if x["snapshot_id"] == "snapshot-0009")["state_vector"]["validation"]["state"] == "STATIC_PARSE_FAIL", "snapshot-0009")
    check("state confidence remains source-local SUPPORTED", all(x["confidence"] == "SUPPORTED" and x["acceptance_caveat"] == "V1_FAILED_V4_V7_MISSING" for x in states), f"rows={len(states)}")

    # Integrity check 4: atomic adjacent deltas.
    check("integrity 4/10: every event is adjacent-version atomic", all(x["adjacent"] is True and VI[x["to_version"]] - VI[x["from_version"]] == 1 for x in events), f"events={len(events)}")
    event_ids = [x["event_id"] for x in events]
    check("event identifiers are unique", len(event_ids) == len(set(event_ids)), f"events={len(events)}")
    check("events preserve before and after states", all("before" in x and "after" in x and x["before"] != x["after"] for x in events), f"events={len(events)}")
    check("event statuses use allowed vocabulary", all(x["status"] in ALLOWED for x in events), str(Counter(x["status"] for x in events)))
    check("event evidence references resolve", all(set(x["evidence_refs"]) <= set(eids) for x in events), f"events={len(events)}")
    with (OUT / "EVOLUTION-MATRIX.csv").open(newline="", encoding="utf-8") as f:
        matrix = list(csv.DictReader(f))
    check("evolution matrix is one row per atomic event", len(matrix) == len(events) and {x["event_id"] for x in matrix} == set(event_ids), f"rows={len(matrix)}")
    check("evolution matrix uses adjacent transitions only", all(x["adjacent"] == "true" for x in matrix), f"rows={len(matrix)}")

    # Integrity check 5: causal claims and alternatives.
    cids = [x["causal_claim_id"] for x in causal]
    check("integrity 5/10: every event has exactly one causal assessment", len(causal) == len(events) and {x["event_ref"] for x in causal} == set(event_ids), f"causal={len(causal)} events={len(events)}")
    check("causal identifiers are unique", len(cids) == len(set(cids)), f"rows={len(cids)}")
    check("causal confidence uses allowed vocabulary", all(x["causal_confidence"] in ALLOWED for x in causal), str(Counter(x["causal_confidence"] for x in causal)))
    check("every causal claim rejects chronology-only cause", all(x["chronology_alone_is_not_causality"] is True for x in causal), f"rows={len(causal)}")
    check("causal UNKNOWN/INFERRED claims retain alternatives", all(len(x["alternatives"]) >= 2 for x in causal if x["causal_confidence"] in {"UNKNOWN", "INFERRED"}), f"rows={len(causal)}")
    check("causal evidence references resolve", all(set(x["evidence_refs"]) <= set(eids) for x in causal), f"rows={len(causal)}")

    # Integrity check 6: uncertainty and contradiction preservation.
    check("integrity 6/10: registered uncertainties remain UNKNOWN", len(uncertainties) >= 10 and all(x["status"] == "UNKNOWN" for x in uncertainties), f"rows={len(uncertainties)}")
    check("uncertainty identifiers are unique", len({x["uncertainty_id"] for x in uncertainties}) == len(uncertainties), f"rows={len(uncertainties)}")
    check("all four prerequisite/execution contradictions are retained", len(contradictions) == 4 and all(x["status"] == "CONTRADICTED" for x in contradictions), f"rows={len(contradictions)}")
    check("contradictions retain both claims, effect, and resolution", all(all(k in x and x[k] for k in ["claim_a", "claim_b", "effect", "resolution"]) for x in contradictions), f"rows={len(contradictions)}")
    check("contradiction evidence references resolve", all(set(x["evidence_refs"]) <= set(eids) for x in contradictions), f"rows={len(contradictions)}")

    # Integrity check 7: architecture separation and branch coverage.
    arch = (OUT / "ARCHITECTURE-EVOLUTION.md").read_text()
    check("integrity 7/10: historical retrospective and current architecture are separated", all(x in arch for x in ["## Historical architecture", "## Retrospective phase model", "## Current architecture"]), "three temporal sections")
    check("architecture evolution names all versions", all(v in arch for v in VERSIONS), "seven versions")
    check("architecture evolution names all complete snapshots", all(x in arch for x in expected_sids), "twelve snapshots")
    epochs = (OUT / "ARCHITECTURE-EPOCHS.md").read_text()
    check("epochs are explicitly interpretive rather than lineage", "INFERRED" in epochs and "not a recovered branch graph" in epochs, "epoch caveat")
    convergence = (OUT / "CONVERGENCE-AND-DIVERGENCE.md").read_text()
    check("dead-end and reintroduction claims remain unproved", "No deletion, abandonment, or reintroduction is `PROVED`" in convergence, "identity uncertainty")

    # Integrity check 8: lifecycle/capability distinctions.
    lifecycle = {"first_mention", "first_design", "first_code", "first_use", "first_test", "first_verification", "stabilization"}
    check("integrity 8/10: every genealogy separates all lifecycle moments", all(lifecycle <= set(x) for x in genealogy), f"concepts={len(genealogy)}")
    check("genealogies do not silently invent historical tests", all(x["first_test"]["status"] == "UNKNOWN" for x in genealogy), f"concepts={len(genealogy)}")
    check("genealogies do not silently invent stabilization", all(x["stabilization"]["status"] == "UNKNOWN" for x in genealogy), f"concepts={len(genealogy)}")
    transformations = {"renames", "splits", "merges", "generalizations", "abandonments", "reintroductions", "empty_list_meaning"}
    check("genealogies account separately for rename split merge generalization abandonment and reintroduction", all(set(x["transformations"]) == transformations for x in genealogy), f"concepts={len(genealogy)}")
    check("empty transformation lists mean not proved rather than absent historically", all(x["transformations"]["empty_list_meaning"] == "NOT_PROVED_NOT_NONE_HISTORICALLY" for x in genealogy), f"concepts={len(genealogy)}")
    cap = (OUT / "CAPABILITY-EMERGENCE.md").read_text()
    check("capability report separates mention test verification stabilization", all(x in cap for x in ["First mention/code/use", "First test", "First verification", "Stabilization"]), "lifecycle columns")
    plan = (OUT / "PLANNED-VS-IMPLEMENTED.md").read_text()
    check("planned described implemented tested verified states are separate", all(x in plan for x in ["Planned", "Described", "Implemented occurrence", "Historically tested", "Verified now"]), "five states")

    # Integrity check 9: graph and cross-file consistency.
    claim_ids = [x["claim_id"] for x in claims]
    check("integrity 9/10: claim identifiers are unique", len(claim_ids) == len(set(claim_ids)), f"claims={len(claims)}")
    check("claim statuses use allowed vocabulary", all(x["status"] in ALLOWED for x in claims), str(Counter(x["status"] for x in claims)))
    check("claim evidence and dependencies resolve", all(set(x["evidence_refs"]) <= set(eids) and set(x["depends_on"]) <= set(claim_ids) for x in claims), f"claims={len(claims)}")
    evidence_by_id = {x["evidence_id"]: x for x in evidence}
    proved_claims = [x for x in claims if x["status"] == "PROVED"]
    check("no claim is silently upgraded to PROVED", all(any(evidence_by_id[r]["status"] == "PROVED" for r in x["evidence_refs"]) or (x["depends_on"] and all(next(c for c in claims if c["claim_id"] == d)["status"] == "PROVED" for d in x["depends_on"])) for x in proved_claims), f"proved_claims={len(proved_claims)}")
    node_ids = [x["id"] for x in graph["nodes"]]
    check("claims graph node identifiers are unique", len(node_ids) == len(set(node_ids)), f"nodes={len(node_ids)}")
    check("claims graph contains every claim evidence and event", set(claim_ids) | set(eids) | set(event_ids) <= set(node_ids), f"nodes={len(node_ids)}")
    check("claims graph edges resolve", all(x["from"] in set(node_ids) and x["to"] in set(node_ids) for x in graph["edges"]), f"edges={len(graph['edges'])}")
    # Dependency acyclicity, recomputed independently.
    dep = {x["claim_id"]: x["depends_on"] for x in claims}; visiting=set(); done=set()
    def visit(n):
        if n in visiting: return False
        if n in done: return True
        visiting.add(n)
        if not all(visit(d) for d in dep[n]): return False
        visiting.remove(n); done.add(n); return True
    acyclic = all(visit(n) for n in dep)
    check("claim dependency graph is acyclic", acyclic, f"claims={len(dep)}")
    check("manifest counts agree with persisted models", manifest["evolution_events"] == len(events) and manifest["causal_claims"] == len(causal) and manifest["architecture_states"] == len(states) and manifest["algorithm_states"] == len(states) and manifest["security_states"] == len(states) and manifest["contract_states"] == len(states), "all model counts")
    check("complexity matrix has one row per state", len(list(csv.DictReader((OUT / "COMPLEXITY-GROWTH.csv").open()))) == len(states), f"states={len(states)}")
    check("invariant statuses use allowed vocabulary", all(x["status"] in ALLOWED for x in invariants), str(Counter(x["status"] for x in invariants)))
    check("false stable-provider invariant is contradicted", any(x["invariant_id"] == "inv-007" and x["status"] == "CONTRADICTED" for x in invariants), "inv-007")

    # Integrity check 10: strict thresholds and final reconstruction completeness.
    by_claim = {x["claim_id"]: x for x in claims}
    generic_ids = [f"claim-generic-{x}" for x in "abcdefgh"]
    check("integrity 10/10: strict generic conditions A-H all exist", all(x in by_claim for x in generic_ids), generic_ids)
    check("all A-H conditions are source-local SUPPORTED", all(by_claim[x]["status"] == "SUPPORTED" and by_claim[x]["evidence_refs"] for x in generic_ids), "8/8")
    check("earliest-generic conclusion depends on every A-H condition", set(by_claim["claim-earliest-generic"]["depends_on"]) == set(generic_ids), by_claim["claim-earliest-generic"]["depends_on"])
    check("earliest runnable remains static-likelihood qualified", by_claim["claim-earliest-runnable"]["status"] == "SUPPORTED" and "historical execution remains UNKNOWN" in by_claim["claim-earliest-runnable"]["claim"], "v0.1.0")
    check("earliest contract-driven threshold remains UNKNOWN", by_claim["claim-earliest-contract"]["status"] == "UNKNOWN", by_claim["claim-earliest-contract"]["claim"])
    report = (OUT / "FINAL-HISTORICAL-REPORT.md").read_text()
    check("final report answers exactly numbered questions 1 through 20", all(f"| {i} |" in report for i in range(1, 21)) and "| 21 |" not in report, "20 questions")
    check("final report applies strict A-H labels", all(f"| {x} |" in report for x in "ABCDEFGH"), "8 conditions")
    check("final report states provisional acceptance prominently", "PROVISIONAL_ONLY_UPSTREAM_BLOCKED" in report and "Full historical acceptance is impossible" in report, "blocked")
    check("final report separates runnable generic and contract thresholds", all(x in report for x in ["earliest runnable architecture", "earliest generic architecture", "earliest contract-driven architecture"]), "three thresholds")
    check("closure analysis rejects exhaustive completeness", "does not mean exhaustive crawling" in (OUT / "DISCOVERY-CLOSURE-ANALYSIS.md").read_text(), "closure bounded")
    check("contract/security integration leaves contracts unknown", "Protocol-v7 is physically absent" in (OUT / "CONTRACT-SECURITY-INTEGRATION.md").read_text(), "v7 absent")
    check("provider/acquisition report preserves protocol coupling", "Historical acquisition remains HTTP/browser/userscript coupled" in (OUT / "PROVIDER-AND-ACQUISITION-EVOLUTION.md").read_text(), "web coupled")
    check("observation/provenance report rejects integrity promotion", "not end-to-end provenance integrity" in (OUT / "OBSERVATION-PROVENANCE-EVOLUTION.md").read_text(), "mechanism not guarantee")
    check("stability report rejects aggregate maturity scoring", "No aggregate stability or maturity score" in (OUT / "STABILITY-ANALYSIS.md").read_text(), "independent axes")
    check("no Python cache artifacts exist", not list(HS.rglob("__pycache__")) and not list(HS.rglob("*.pyc")), "clean")

    counts = {
        "checks": len(checks), "passed": sum(x["result"] == "PASS" for x in checks),
        "failed": sum(x["result"] == "FAIL" for x in checks), "evidence": len(evidence),
        "states": len(states), "events": len(events), "causal_claims": len(causal),
        "claims": len(claims), "contradictions": len(contradictions), "uncertainties": len(uncertainties),
    }
    write_reports(checks, counts)
    print(f"{counts['passed']}/{counts['checks']} PASS; acceptance=PROVISIONAL_ONLY_UPSTREAM_BLOCKED")
    if counts["failed"]:
        raise SystemExit(1)


def write_reports(checks: list[dict[str, str]], counts: dict[str, Any]) -> None:
    passed = sum(x["result"] == "PASS" for x in checks); failed = len(checks) - passed
    obj = {
        "schema_version": "protocol-v9-validation", "protocol": "Protocol-v9",
        "overall": "PASS" if not failed else "FAIL",
        "acceptance": "PROVISIONAL_ONLY_UPSTREAM_BLOCKED" if not failed else "REJECTED_INTERNAL_VALIDATION_FAILURE",
        "checks": checks,
        "counts": counts or {"checks": len(checks), "passed": passed, "failed": failed},
    }
    (OUT / "VALIDATION.yaml").write_text(json.dumps(obj, indent=2) + "\n")
    rows = "\n".join(f"| {i} | {x['check']} | {x['result']} | {x['detail'].replace('|', '/')} |" for i, x in enumerate(checks, 1))
    text = f"# Protocol-v9 Validation\n\n**Overall:** {obj['overall']}  \n**Acceptance:** {obj['acceptance']}  \n**Checks:** {passed}/{len(checks)} PASS\n\n| # | Check | Result | Detail |\n|---:|---|---|---|\n{rows}\n"
    (OUT / "VALIDATION.md").write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
