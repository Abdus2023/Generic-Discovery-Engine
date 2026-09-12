#!/usr/bin/env python3
"""Build Protocol-v9's provisional, evidence-bounded historical synthesis.

The builder consumes persisted Protocol-v1-v3 and Protocol-v8 outputs. Protocol-v4-v7
are deliberately never reconstructed here: their absence is represented as UNKNOWN and
blocks full acceptance. JSON is emitted in YAML-named files, as elsewhere in this corpus.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import shutil
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[2]
HS = ROOT / "historical-source"
OUT = HS / "synthesis"
TOOLS = HS / "tools"
STATUS = {"PROVED", "SUPPORTED", "INFERRED", "CONJECTURED", "CONTRADICTED", "UNKNOWN"}
VERSIONS = ["v0.1.0", "v0.2.0", "v0.3.0", "v0.4.0", "v0.5.0", "v0.6.0", "v0.7.1"]
VINDEX = {v: i for i, v in enumerate(VERSIONS)}
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


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_md(name: str, text: str) -> None:
    (OUT / name).write_text(text.rstrip() + "\n", encoding="utf-8")


def table(headers: list[str], rows: Iterable[Iterable[Any]]) -> str:
    h = "| " + " | ".join(headers) + " |\n"
    sep = "|" + "|".join("---" for _ in headers) + "|\n"
    body = "".join("| " + " | ".join(str(v).replace("|", "\\|").replace("\n", " ") for v in row) + " |\n" for row in rows)
    return h + sep + body


def lines_for(text: str, pattern: str) -> list[int]:
    rx = re.compile(pattern, re.I | re.M)
    return sorted({text.count("\n", 0, m.start()) + 1 for m in rx.finditer(text)})


def snapshot_path(snapshot: dict[str, Any]) -> str:
    return snapshot["paths"]["source"]


def snapshot_artifact(snapshot: dict[str, Any]) -> str:
    return snapshot["version_boundary"]["evidence"]["artifact_id"]


def source_text(snapshot: dict[str, Any]) -> str:
    return (HS / snapshot_path(snapshot)).read_text(encoding="utf-8", errors="replace")


def source_evidence(evidence: list[dict[str, Any]], snap: dict[str, Any], pattern: str,
                    claim: str, ceiling: str = "SUPPORTED") -> str:
    text = source_text(snap)
    found = lines_for(text, pattern)
    eid = f"syn-ev-{len(evidence)+1:05d}"
    evidence.append({
        "evidence_id": eid,
        "directional_chain": ["SOURCE", "ARTIFACT", "SNAPSHOT", "VERIFIED_FACT", "EVOLUTION_EVENT", "CAUSAL_HYPOTHESIS", "SYNTHESIS"],
        "source_revision_id": snap["revision"],
        "source_artifact_id": snapshot_artifact(snap),
        "snapshot_id": snap["snapshot_id"],
        "version": snap["historical_version"],
        "variant": snap["variant"],
        "source_path": snapshot_path(snap),
        "line_numbers": found,
        "pattern": pattern,
        "claim": claim,
        "source_presence": "PRESENT" if found else "ABSENT_IN_SCANNED_SNAPSHOT",
        "status": ceiling if found else "UNKNOWN",
        "confidence_ceiling": ceiling if found else "UNKNOWN",
        "v1_integrity_caveat": "RAW_BYTES_AND_RANGES_FAIL_PINNED_VALIDATION",
        "backward_proof_forbidden": True,
    })
    return eid


def upstream_evidence(evidence: list[dict[str, Any]], path: str, record_id: str,
                      claim: str, status: str = "SUPPORTED") -> str:
    eid = f"syn-ev-{len(evidence)+1:05d}"
    evidence.append({
        "evidence_id": eid,
        "directional_chain": ["SOURCE", "ARTIFACT", "SNAPSHOT", "VERIFIED_FACT", "EVOLUTION_EVENT", "CAUSAL_HYPOTHESIS", "SYNTHESIS"],
        "upstream_output": path,
        "upstream_record_id": record_id,
        "claim": claim,
        "status": status,
        "confidence_ceiling": status,
        "v1_integrity_caveat": "RAW_BYTES_AND_RANGES_FAIL_PINNED_VALIDATION",
        "backward_proof_forbidden": True,
    })
    return eid


def md_front(title: str) -> str:
    return f"# {title}\n\n> **Acceptance: PROVISIONAL_ONLY_UPSTREAM_BLOCKED.** Protocol-v1 raw/range validation fails and Protocol-v4 through Protocol-v7 outputs are absent. `SUPPORTED` in this report is source-local and does not mean the full v1→v9 chain is verified. Missing dimensions remain `UNKNOWN`.\n\n"


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    reconstruction = load(HS / "RECONSTRUCTION-MANIFEST.yaml")
    analysis_validation = load(HS / "RECONSTRUCTION-VALIDATION.yaml")
    data_models = {r["snapshot_id"]: r for r in load(HS / "analysis" / "DATA-MODEL-EVOLUTION.yaml")["models"]}
    providers = {r["snapshot_id"]: r for r in load(HS / "analysis" / "PROVIDER-HISTORY.yaml")["history"]}
    security_manifest = load(HS / "security" / "SECURITY-MANIFEST.yaml")
    security_validation = load(HS / "security" / "VALIDATION.yaml")
    failure_events = load(HS / "security" / "FAILURE-EVENTS.yaml")["failures"]
    trust_boundaries = load(HS / "security" / "TRUST-BOUNDARIES.yaml")["boundaries"]
    authority = load(HS / "security" / "AUTHORITY-HISTORY.yaml")["authorities"]
    resource_bounds = load(HS / "security" / "RESOURCE-BOUNDS.yaml")["bounds"]
    parser_rows = load(HS / "security" / "PARSER-SAFETY-HISTORY.yaml")["parsers"]

    snapshots = [s for s in reconstruction["snapshots"] if s["reconstruction"]["status"] != "PARTIAL"]
    snapshots.sort(key=lambda s: (VINDEX[s["historical_version"]], s["snapshot_id"]))
    by_version: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for s in snapshots:
        by_version[s["historical_version"]].append(s)

    evidence: list[dict[str, Any]] = []
    base_patterns = {
        "candidate": r"class\s+Candidate\b|new\s+Candidate\b",
        "observation": r"class\s+Observation\b|new\s+Observation\b",
        "discovery": r"class\s+Discovery\b|emitDiscovery\b|addDiscovery\b",
        "recognition": r"recognize\s*\(|class\s+\w*(?:Provider|Recognizer)\b",
        "scheduler": r"class\s+Scheduler\b|claimNextCandidate\b|nextCandidate\b",
        "acquisition": r"GM_xmlhttpRequest\b|fetch\s*\(|HttpAcquisition\b|acquir(?:e|er)\s*\(",
        "expansion": r"candidate(?:s)?\s*\(|addCandidate\b|emitCandidate\b|CandidateExtractor\b",
        "repetition": r"while\s*\(|run\s*\(|workerLoop\b|pump\s*\(",
        "provider_abstraction": r"class\s+ResponseProvider\b|class\s+Provider\b|ProviderRegistry\b",
        "retry": r"attempts\b|retry\b|backoff\b|requeue\b",
        "cancellation": r"AbortController\b|abort\s*\(|signal\b",
        "provenance": r"provenance\b|lineage\b|edges\b|observationId\b",
        "acquisition_policy": r"AcquisitionPolicy\b",
        "acquisition_plan": r"AcquisitionPlan\b",
        "decision_ledger": r"DecisionLedger\b",
        "claim": r"claimNextCandidate\b|status\s*=\s*[\"']running",
        "recognition_error_containment": r"Promise\.allSettled\b|providerErrors\b|try\s*\{[\s\S]{0,500}recognize",
        "network_observation": r"NetworkObservation\b|performance\.getEntries|PerformanceObserver\b",
        "structured_diagnostics": r"\bDiagnostic\w*\b|\bdiagnostics?\b|\btrace\b|DecisionLedger\b|\bmetrics?\b",
        "validation": r"node\s+--check|test\s*\(|describe\s*\(|assert\s*\(",
    }
    snapshot_feature: dict[str, dict[str, bool]] = {}
    feature_refs: dict[tuple[str, str], str] = {}
    for s in snapshots:
        text = source_text(s)
        snapshot_feature[s["snapshot_id"]] = {}
        for feature, pattern in base_patterns.items():
            present = bool(lines_for(text, pattern))
            snapshot_feature[s["snapshot_id"]][feature] = present
            if present:
                feature_refs[(s["snapshot_id"], feature)] = source_evidence(
                    evidence, s, pattern, f"{feature} syntax occurs in this snapshot"
                )

    # Multidimensional states. Values are intentionally categorical and independent.
    vector_rows: list[dict[str, Any]] = []
    for s in snapshots:
        sid = s["snapshot_id"]
        f = snapshot_feature[sid]
        model = data_models[sid]
        fields = model["fields"]
        fe = [x for x in failure_events if x["snapshot_id"] == sid]
        tb = [x for x in trust_boundaries if x["snapshot_id"] == sid]
        au = [x for x in authority if x["snapshot_id"] == sid]
        rb = [x for x in resource_bounds if x["snapshot_id"] == sid]
        pr = [x for x in parser_rows if x["snapshot_id"] == sid]
        refs = [feature_refs[(sid, k)] for k in f if (sid, k) in feature_refs]
        vector_rows.append({
            "state_id": "state-" + sid,
            "snapshot_id": sid,
            "version": s["historical_version"],
            "variant": s["variant"],
            "source_artifact_id": snapshot_artifact(s),
            "state_vector": {
                "algorithm": {"state": "PRESENT" if all(f[k] for k in ("candidate", "observation", "discovery", "repetition")) else "PARTIAL", "status": "SUPPORTED"},
                "architecture": {"state": "CANDIDATE_CENTRIC_PIPELINE", "status": "SUPPORTED"},
                "contracts": {"state": "UNKNOWN", "status": "UNKNOWN", "reason": "Protocol-v7 contract outputs are absent; source shapes are not upgraded into validated contracts"},
                "data": {"state": "STRUCTURED", "status": "SUPPORTED", "model_count": len(fields), "field_count": sum(len(v) for v in fields.values())},
                "execution": {"state": s["executability"], "status": "SUPPORTED", "historical_runtime": s["historical_execution"]},
                "concurrency": {"state": "EXPLICIT" if re.search(r"concurr|workers|inFlight|Promise\.all", source_text(s), re.I) else "IMPLICIT_OR_UNKNOWN", "status": "SUPPORTED"},
                "providers": {"state": "MULTI_PROVIDER" if len(providers[sid]["providers"]) > 1 else "SINGLE_RECOGNIZER", "status": "SUPPORTED", "count": len(providers[sid]["providers"])},
                "provenance": {"state": "EXPLICIT" if f["provenance"] else "LIMITED_OR_IMPLICIT", "status": "SUPPORTED"},
                "failure": {"state": "EXPLICIT_HANDLING_PRESENT" if fe else "UNKNOWN", "status": "SUPPORTED" if fe else "UNKNOWN", "event_count": len(fe)},
                "security": {"state": "MECHANISMS_NOT_GUARANTEES", "status": "SUPPORTED", "trust_boundary_count": len(tb), "authority_count": len(au)},
                "observability": {"state": ("DECISION_LEDGER_AND_DIAGNOSTICS" if f["decision_ledger"] else
                                                "STRUCTURED_DIAGNOSTICS" if f["structured_diagnostics"] else
                                                "NETWORK_OBSERVATION" if f["network_observation"] else
                                                "OBSERVATION_CENTRIC"), "status": "SUPPORTED"},
                "validation": {"state": "STATIC_ONLY" if s["static_validation"]["syntax_and_ast_parse"]["result"] == "PASS" else "STATIC_PARSE_FAIL", "status": "SUPPORTED", "historical_tests": "UNKNOWN"},
            },
            "resource_bound_count": len(rb),
            "parser_boundary_count": len(pr),
            "evidence_refs": refs,
            "confidence": "SUPPORTED",
            "acceptance_caveat": "V1_FAILED_V4_V7_MISSING",
        })
    dump(OUT / "VERSION-STATE-VECTORS.yaml", {"schema_version": "protocol-v9", "states": vector_rows})

    # Atomic transition events compare adjacent labels only. Variant cross-products are retained.
    events: list[dict[str, Any]] = []
    causal: list[dict[str, Any]] = []
    def add_event(v_from: str, v_to: str, kind: str, dimension: str, subject: str,
                  before: Any, after: Any, refs: list[str], summary: str,
                  status: str = "SUPPORTED", causal_label: str = "UNKNOWN",
                  hypothesis: str = "Chronology establishes succession, not cause.",
                  alternatives: list[str] | None = None) -> None:
        assert status in STATUS and causal_label in STATUS
        eid = f"event-{len(events)+1:04d}"
        cid = f"causal-{len(causal)+1:04d}"
        events.append({
            "event_id": eid, "from_version": v_from, "to_version": v_to,
            "adjacent": VINDEX[v_to] - VINDEX[v_from] == 1,
            "event_type": kind, "dimension": dimension, "subject": subject,
            "before": before, "after": after, "summary": summary,
            "status": status, "evidence_refs": sorted(set(refs)),
            "causal_claim_ref": cid,
        })
        causal.append({
            "causal_claim_id": cid, "event_ref": eid, "hypothesis": hypothesis,
            "causal_confidence": causal_label,
            "alternatives": alternatives or ["Independent design choice", "Unrecorded external requirement", "Branch-specific experimentation"],
            "chronology_alone_is_not_causality": True,
            "evidence_refs": sorted(set(refs)),
        })

    for a, b in zip(VERSIONS, VERSIONS[1:]):
        for feature in base_patterns:
            left = [snapshot_feature[s["snapshot_id"]][feature] for s in by_version[a]]
            right = [snapshot_feature[s["snapshot_id"]][feature] for s in by_version[b]]
            if all(left) == all(right) and any(left) == any(right):
                continue
            refs = [feature_refs[(s["snapshot_id"], feature)] for s in by_version[a] + by_version[b] if (s["snapshot_id"], feature) in feature_refs]
            before = "ALL_VARIANTS" if all(left) else "SOME_VARIANTS" if any(left) else "ABSENT_IN_SCAN"
            after = "ALL_VARIANTS" if all(right) else "SOME_VARIANTS" if any(right) else "ABSENT_IN_SCAN"
            kind = ("ADDITION_OR_GENERALIZATION" if any(right) and not any(left) else
                    "REMOVAL_OR_RELOCATION" if any(left) and not any(right) else
                    "BRANCH_CONVERGENCE_IN_RECOVERED_OCCURRENCES" if not all(left) and all(right) else
                    "BRANCH_DIVERGENCE")
            add_event(a, b, kind, "cross_cutting", feature, before, after, refs,
                      f"Scanned {feature} presence changes from {before} to {after}; identity and motivation are not inferred.",
                      "SUPPORTED", "UNKNOWN")
        # Provider-set deltas are occurrence-level, not lineage proof.
        before_set = sorted({p for s in by_version[a] for p in providers[s["snapshot_id"]]["providers"]})
        after_set = sorted({p for s in by_version[b] for p in providers[s["snapshot_id"]]["providers"]})
        for p in sorted(set(after_set) - set(before_set)):
            refs = [feature_refs[(s["snapshot_id"], "recognition")] for s in by_version[b] if (s["snapshot_id"], "recognition") in feature_refs]
            add_event(a, b, "ADDITION", "providers", p, "NOT_OBSERVED", "OBSERVED", refs,
                      f"Provider/recognizer name {p} first occurs in the recovered adjacent-version sequence; lineage is not proved.")
        for p in sorted(set(before_set) - set(after_set)):
            refs = [feature_refs[(s["snapshot_id"], "recognition")] for s in by_version[a] if (s["snapshot_id"], "recognition") in feature_refs]
            add_event(a, b, "DISAPPEARANCE", "providers", p, "OBSERVED", "NOT_OBSERVED", refs,
                      f"Provider/recognizer name {p} is not observed at the next version; deletion and abandonment remain UNKNOWN.")

    # Explicit source comments support mechanism pressure but not undocumented author intent.
    for v_from, v_to, subj, patt, hyp, alts in [
        ("v0.1.0", "v0.2.0", "atomic_candidate_claim", r"claimNextCandidate\b", "The explicit claim operation addresses duplicate worker selection by atomically moving a pending candidate to running.", ["Queue ownership cleanup", "Status-accounting requirement"]),
        ("v0.2.0", "v0.3.0", "bounded_retry", r"attempts\b|requeue\b|backoff\b", "Attempt and requeue state implements bounded retry pressure rather than silent one-shot loss.", ["Diagnostics bookkeeping", "Scheduling fairness experiment"]),
        ("v0.3.0", "v0.4.0", "provider_failure_isolation", r"allSettled\b|providerErrors\b", "Per-provider error capture isolates recognition failures so one provider need not terminate all recognition.", ["Diagnostic enrichment", "Branch-local coding style"]),
    ]:
        ss = by_version[v_to]
        refs = [source_evidence(evidence, s, patt, hyp) for s in ss if lines_for(source_text(s), patt)]
        if refs:
            add_event(v_from, v_to, "EXPLICIT_MECHANISM_CHANGE", "architecture", subj, "EARLIER_FORM", "EXPLICIT_FORM", refs, hyp,
                      "SUPPORTED", "SUPPORTED", hyp, alts)

    dump(OUT / "EVOLUTION-EVENTS.yaml", {"schema_version": "protocol-v9", "atomic_events": events})
    dump(OUT / "CAUSAL-CLAIMS.yaml", {"schema_version": "protocol-v9", "causal_claims": causal,
                                      "rule": "Chronological succession alone is never causal evidence."})

    with (OUT / "EVOLUTION-MATRIX.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["event_id", "from_version", "to_version", "adjacent", "event_type", "dimension", "subject", "before", "after", "status", "causal_confidence", "evidence_refs"])
        c_by = {c["causal_claim_id"]: c for c in causal}
        for e in events:
            w.writerow([e["event_id"], e["from_version"], e["to_version"], str(e["adjacent"]).lower(), e["event_type"], e["dimension"], e["subject"], e["before"], e["after"], e["status"], c_by[e["causal_claim_ref"]]["causal_confidence"], ";".join(e["evidence_refs"])])

    # Lifecycle and genealogy: coding/use are distinct from historical testing/verification/stability.
    concepts = {
        "Candidate identity": ("candidate", "v0.1.0"), "Observation": ("observation", "v0.1.0"),
        "Discovery": ("discovery", "v0.1.0"), "Revisiting scheduler": ("repetition", "v0.1.0"),
        "Recognition role": ("recognition", "v0.1.0"), "Reusable provider abstraction": ("provider_abstraction", "v0.2.0"),
        "Explicit retry": ("retry", "v0.3.0"), "Cancellation": ("cancellation", "v0.3.0"),
        "Explicit provenance": ("provenance", "v0.1.0"),
        "Acquisition policy": ("acquisition_policy", "v0.6.0"),
        "Acquisition plan": ("acquisition_plan", "v0.7.1"),
        "Decision ledger": ("decision_ledger", "v0.7.1"),
    }
    genealogies = []
    for name, (feature, expected) in concepts.items():
        occurrences = [s for s in snapshots if snapshot_feature[s["snapshot_id"]][feature]]
        first = occurrences[0] if occurrences else None
        ref = feature_refs.get((first["snapshot_id"], feature)) if first else None
        genealogies.append({
            "concept": name,
            "first_mention": {"version": first["historical_version"] if first else "UNKNOWN", "status": "SUPPORTED" if first else "UNKNOWN", "evidence_refs": [ref] if ref else []},
            "first_design": {"version": "UNKNOWN", "status": "UNKNOWN", "reason": "Code occurrence is not silently upgraded to prior design"},
            "first_code": {"version": first["historical_version"] if first else "UNKNOWN", "status": "SUPPORTED" if first else "UNKNOWN", "evidence_refs": [ref] if ref else []},
            "first_use": {"version": first["historical_version"] if first else "UNKNOWN", "status": "SUPPORTED" if first else "UNKNOWN", "evidence_refs": [ref] if ref else []},
            "first_test": {"version": "UNKNOWN", "status": "UNKNOWN", "reason": "No historical test corpus is verified"},
            "first_verification": {"version": "UNKNOWN", "status": "UNKNOWN", "reason": "Retrospective static checks are not historical verification"},
            "stabilization": {"version": "UNKNOWN", "status": "UNKNOWN", "reason": "Branch lineage and contract verification are unavailable"},
            "occurrences": [{"snapshot_id": s["snapshot_id"], "version": s["historical_version"], "variant": s["variant"]} for s in occurrences],
            "identity_across_occurrences": "UNKNOWN",
            "transformations": {
                "renames": [], "splits": [], "merges": [],
                "generalizations": ([{"at_version": "v0.2.0", "status": "INFERRED", "interpretation": "The recovered recognition role broadens from one HtmlRecognizer occurrence to a reusable multi-provider family; implementation lineage remains UNKNOWN.", "evidence_refs": [ref] if ref else []}] if name == "Reusable provider abstraction" else []),
                "abandonments": [], "reintroductions": [],
                "empty_list_meaning": "NOT_PROVED_NOT_NONE_HISTORICALLY",
            },
            "unresolved_transformation_questions": ["rename identity", "split or merge identity", "abandonment versus non-occurrence", "reintroduction versus independent recurrence"],
            "expected_first_version_check": expected,
        })
    dump(OUT / "CONCEPT-GENEALOGY.yaml", {"schema_version": "protocol-v9", "genealogies": genealogies,
        "rename_split_merge_rule": "Same names, similar code, and chronological adjacency do not prove identity, renaming, splits, merges, deletion, or reintroduction."})

    # Complexity uses direct structural counts and independent security dimensions, never one maturity score.
    complexity = []
    for s in snapshots:
        sid = s["snapshot_id"]; text = source_text(s); model = data_models[sid]
        complexity.append({
            "snapshot_id": sid, "version": s["historical_version"], "variant": s["variant"],
            "source_lines": len(text.splitlines()), "class_occurrences": len(re.findall(r"\bclass\s+\w+", text)),
            "async_method_occurrences": len(re.findall(r"\basync\s+\w+\s*\(", text)),
            "model_count": len(model["fields"]), "field_count": sum(len(x) for x in model["fields"].values()),
            "provider_count": len(providers[sid]["providers"]),
            "failure_event_count": sum(x["snapshot_id"] == sid for x in failure_events),
            "trust_boundary_count": sum(x["snapshot_id"] == sid for x in trust_boundaries),
            "authority_count": sum(x["snapshot_id"] == sid for x in authority),
            "resource_bound_count": sum(x["snapshot_id"] == sid for x in resource_bounds),
        })
    with (OUT / "COMPLEXITY-GROWTH.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(complexity[0])); w.writeheader(); w.writerows(complexity)

    # Evidence ledger is written after all evidence-producing sections below; markdown refs already stable.
    build_markdown_outputs(OUT, snapshots, by_version, snapshot_feature, feature_refs, data_models,
                           providers, vector_rows, events, causal, complexity, failure_events,
                           trust_boundaries, authority, resource_bounds, evidence)

    contradictions = [
        {"contradiction_id": "contra-001", "claim_a": "Protocol-v1 raw revisions and extracted ranges are byte-verified", "claim_b": "Active validation reports 0/4 raw revisions and 0/5644 artifact ranges valid", "status": "CONTRADICTED", "resolution": "UNRESOLVED_INPUT_INTEGRITY_FAILURE", "effect": "All later acceptance is provisional", "evidence_refs": [upstream_evidence(evidence, "historical-source/VALIDATION.yaml", "validation_summary", "Protocol-v1 byte validation fails", "PROVED")]},
        {"contradiction_id": "contra-002", "claim_a": "A passing Protocol-v3 report establishes a verified Protocol-v1-through-v3 chain", "claim_b": "Protocol-v1 source/range validation fails even though Protocol-v3's internal validation passes", "status": "CONTRADICTED", "resolution": "V3_INTERNAL_PASS_DOES_NOT_REPAIR_V1_CHAIN", "effect": "Source-local reconstruction facts are capped at SUPPORTED", "evidence_refs": [upstream_evidence(evidence, "historical-source/RECONSTRUCTION-VALIDATION.yaml", "validation_summary", "Protocol-v3 reports 28/28 PASS", "PROVED")]},
        {"contradiction_id": "contra-003", "claim_a": "All exact complete reconstructed occurrences are statically executable", "claim_b": "snapshot-0009 is exact but fails static parsing and is classified NON_EXECUTABLE", "status": "CONTRADICTED", "resolution": "EXACTNESS_IS_NOT_EXECUTABILITY", "effect": "v0.5 has executable and non-executable variants", "evidence_refs": [upstream_evidence(evidence, "historical-source/RECONSTRUCTION-MANIFEST.yaml", "snapshot-0009", "Exact source occurrence has NON_EXECUTABLE static classification", "PROVED")]},
        {"contradiction_id": "contra-004", "claim_a": "Protocol-v9 can consume verified Protocol-v4-v7 outputs", "claim_b": "verification/, algorithm/, architecture/, and contracts/ are absent", "status": "CONTRADICTED", "resolution": "MISSING_INPUTS_REMAIN_UNKNOWN", "effect": "Contract integration and full verified-fact synthesis are blocked", "evidence_refs": [upstream_evidence(evidence, "historical-source/security/SECURITY-MANIFEST.yaml", "upstream_availability", "Protocol-v4 through v7 are absent", "PROVED")]},
    ]
    dump(OUT / "CONTRADICTIONS.yaml", {"schema_version": "protocol-v9", "contradictions": contradictions})

    uncertainties = [
        ("unc-001", "Protocol-v1 pinned-byte integrity", "Raw/range mismatch", "Blocks verified chain", "Do not repair or normalize source"),
        ("unc-002", "Protocol-v4 verified facts", "Directory absent", "Runtime facts unavailable", "UNKNOWN"),
        ("unc-003", "Protocol-v5 algorithm model", "Directory absent", "Algorithm guarantees unavailable", "UNKNOWN"),
        ("unc-004", "Protocol-v6 architecture model", "Directory absent", "Architecture conformance unavailable", "UNKNOWN"),
        ("unc-005", "Protocol-v7 contract model", "Directory absent", "Contract-driven threshold unavailable", "UNKNOWN"),
        ("unc-006", "Historical runtime", "Manifest says UNKNOWN for every occurrence", "Runnable means static likelihood only", "UNKNOWN"),
        ("unc-007", "Historical tests", "No verified tests tied to versions", "First-tested/stabilized unknown", "UNKNOWN"),
        ("unc-008", "Branch lineage", "v0.4-v0.6 have parallel alternatives", "No unique linear predecessor", "UNKNOWN"),
        ("unc-009", "Partial flattened alternatives", "snapshot-0002 and snapshot-0004 are partial", "Excluded from complete state vectors", "Preserved, not promoted"),
        ("unc-010", "Causal intent", "Most deltas lack explicit rationale", "Chronology only", "UNKNOWN with alternatives"),
        ("unc-011", "Current prose temporal scope", "Current proposals are not historical implementations", "No backward proof", "Separated"),
        ("unc-012", "Provider identity", "Names and code similarity do not prove lineage", "Renames/deletions/reintroductions unknown", "Occurrence-level only"),
        ("unc-013", "Security guarantees", "Mechanisms do not prove guarantees", "Boundary/integrity claims limited", "SUPPORTED mechanisms only"),
        ("unc-014", "Protocol independence", "Current design discusses generic protocols; snapshots are web-coupled", "Historical protocol-generic capability unproved", "UNKNOWN"),
        ("unc-015", "Exhaustive closure", "Finite bounds and scheduling do not prove complete search", "No completeness claim", "CONTRADICTED if asserted"),
    ]
    dump(OUT / "UNCERTAINTIES.yaml", {"schema_version": "protocol-v9", "uncertainties": [
        {"uncertainty_id": i, "subject": s, "basis": b, "impact": im, "disposition": d, "status": "UNKNOWN"}
        for i, s, b, im, d in uncertainties]})

    invariants = build_invariants(snapshots, snapshot_feature, feature_refs)
    dump(OUT / "INVARIANTS.yaml", {"schema_version": "protocol-v9", "invariants": invariants})

    claims = build_claims(snapshots, feature_refs, events, contradictions, evidence)
    dump(OUT / "CLAIMS.yaml", {"schema_version": "protocol-v9", "claims": claims})
    nodes = ([{"id": c["claim_id"], "kind": "claim", "status": c["status"]} for c in claims] +
             [{"id": e["evidence_id"], "kind": "evidence", "status": e["status"]} for e in evidence] +
             [{"id": e["event_id"], "kind": "event", "status": e["status"]} for e in events])
    edges = []
    for c in claims:
        edges += [{"from": r, "to": c["claim_id"], "relation": "supports"} for r in c["evidence_refs"]]
        edges += [{"from": d, "to": c["claim_id"], "relation": "claim_dependency"} for d in c.get("depends_on", [])]
    for e in events:
        edges += [{"from": r, "to": e["event_id"], "relation": "supports"} for r in e["evidence_refs"]]
    dump(OUT / "HISTORICAL-CLAIMS-GRAPH.json", {"schema_version": "protocol-v9", "nodes": nodes, "edges": edges,
        "direction": "evidence_to_event_or_claim; dependency_to_claim", "acyclic_claim_dependencies": True})

    dump(OUT / "EVIDENCE-LEDGER.yaml", {"schema_version": "protocol-v9", "acceptance": "PROVISIONAL_ONLY_UPSTREAM_BLOCKED",
        "allowed_statuses": sorted(STATUS), "evidence": evidence})

    # The final report is generated before the manifest so the manifest binds every
    # required deliverable except itself (self-hashing would be recursive).
    build_final_report(OUT, snapshots, events, causal, claims, contradictions, uncertainties,
                       invariants, complexity, security_validation)
    files = []
    for name in (n for n in REQUIRED if n != "SYNTHESIS-MANIFEST.yaml"):
        p = OUT / name
        files.append({"path": f"historical-source/synthesis/{name}", "sha256": sha(p), "size": p.stat().st_size})
    consumed = [
        "VALIDATION.yaml", "RECONSTRUCTION-MANIFEST.yaml", "RECONSTRUCTION-VALIDATION.yaml",
        "analysis/DATA-MODEL-EVOLUTION.yaml", "analysis/PROVIDER-HISTORY.yaml",
        "security/VALIDATION.yaml", "security/SECURITY-MANIFEST.yaml", "security/FAILURE-EVENTS.yaml",
        "security/TRUST-BOUNDARIES.yaml", "security/AUTHORITY-HISTORY.yaml",
        "security/RESOURCE-BOUNDS.yaml", "security/PARSER-SAFETY-HISTORY.yaml",
        "security/CURRENT-PROPOSED-SECURITY.yaml",
    ]
    verified_artifacts = [{
        "path": f"historical-source/{p}", "sha256": sha(HS / p),
        "status": ("FAILED_PREREQUISITE" if p == "VALIDATION.yaml" else
                   "PROVISIONAL_ONLY_UPSTREAM_BLOCKED" if p.startswith("security/") else
                   "INTERNALLY_VALIDATED_SOURCE_LOCAL"),
    } for p in consumed]
    verified_artifacts += [{
        "path": f"historical-source/{snapshot_path(s)}", "sha256": sha(HS / snapshot_path(s)),
        "status": "SNAPSHOT_INPUT_SOURCE_LOCAL",
    } for s in snapshots]
    manifest = {
        "synthesis_version": "protocol-v9", "source_versions": VERSIONS,
        "verified_artifacts": verified_artifacts,
        "evolution_events": len(events), "causal_claims": len(causal),
        "architecture_states": len(vector_rows), "contract_states": len(vector_rows),
        "contract_state_disposition": "ALL_UNKNOWN_BECAUSE_PROTOCOL_V7_IS_ABSENT",
        "security_states": len(vector_rows), "algorithm_states": len(vector_rows),
        "unresolved_questions": len(uncertainties), "contradictions": len(contradictions),
        "confidence": "PROVISIONAL_SOURCE_LOCAL_SUPPORTED",
        "prerequisite_acceptance": "BLOCKED_MISSING_OR_FAILED_UPSTREAM",
        "acceptance": "PROVISIONAL_ONLY_UPSTREAM_BLOCKED",
        "upstream_availability": security_manifest["upstream_availability"],
        "dimensions_unavailable": ["Protocol-v4 verified runtime facts", "Protocol-v5 validated algorithm model", "Protocol-v6 validated architecture model", "Protocol-v7 validated contracts"],
        "generator": "historical-source/tools/build_historical_synthesis.py",
        "tools": {
            "generator": sha(TOOLS / "build_historical_synthesis.py"),
            "validator": sha(TOOLS / "validate_historical_synthesis.py"),
        },
        "required_deliverables": REQUIRED,
        "files": files,
    }
    dump(OUT / "SYNTHESIS-MANIFEST.yaml", manifest)
    assert all((OUT / p).exists() for p in REQUIRED)
    print(f"generated {len(REQUIRED)} deliverables; evidence={len(evidence)} events={len(events)} claims={len(claims)}")


def build_invariants(snapshots, features, refs):
    specs = [
        ("inv-001", "Candidate is the scheduled work identity", "candidate", []),
        ("inv-002", "Acquisition precedes recognition/interpretation in the workflow", "acquisition", []),
        ("inv-003", "Observations preserve acquisition results separately from discoveries", "observation", []),
        ("inv-004", "Discoveries can feed further candidate work", "expansion", []),
        ("inv-005", "The engine repeats over scheduled work", "repetition", []),
        ("inv-006", "Recovered acquisition is web-protocol coupled", "acquisition", ["Current protocol-generic proposals are retrospective/current, not recovered historical implementation"]),
    ]
    out = []
    for iid, statement, feature, exceptions in specs:
        supporting = [s for s in snapshots if features[s["snapshot_id"]][feature]]
        missing = [s for s in snapshots if not features[s["snapshot_id"]][feature]]
        out.append({"invariant_id": iid, "statement": statement,
                    "scope": "all complete recovered occurrences" if not missing else "most complete recovered occurrences",
                    "status": "SUPPORTED" if not missing else "INFERRED",
                    "supporting_snapshots": [s["snapshot_id"] for s in supporting],
                    "exceptions": exceptions + [s["snapshot_id"] for s in missing],
                    "evidence_refs": [refs[(s["snapshot_id"], feature)] for s in supporting if (s["snapshot_id"], feature) in refs]})
    out.append({"invariant_id": "inv-007", "statement": "Provider abstraction and ownership remain unchanged", "scope": "v0.1-v0.7.1", "status": "CONTRADICTED", "supporting_snapshots": [], "exceptions": ["v0.1 uses HtmlRecognizer", "provider sets and signatures vary", "v0.7.1 centralizes policy/ledger and changes provider interaction"], "evidence_refs": [refs[(s["snapshot_id"], "recognition")] for s in snapshots if (s["snapshot_id"], "recognition") in refs]})
    return out


def build_claims(snapshots, refs, events, contradictions, evidence):
    first = snapshots[0]
    def r(feature, sid="snapshot-0001"):
        return [refs[(sid, feature)]] if (sid, feature) in refs else []
    claims = []
    def add(cid, text, status, evrefs, deps=None, boundary="historical"):
        claims.append({"claim_id": cid, "claim": text, "status": status, "evidence_refs": evrefs,
                       "depends_on": deps or [], "interpretation_boundary": boundary,
                       "upstream_blocker": "V1_FAILED_V4_V7_MISSING"})
    # The A-H threshold is conjunctive. Dedicated evidence prevents a class name
    # alone from being mistaken for identity, duplicate control, or an entry path.
    threshold_extra = {
        "A": source_evidence(evidence, first, r"this\.id\s*=\s*makeId\s*\(\s*['\"]candidate|candidateKey\s*\(", "Candidate identity generation/keying occurs in v0.1.0"),
        "G": source_evidence(evidence, first, r"visited\s*=\s*new\s+Set|candidateKey\s*\(|candidates\.has\s*\(", "Duplicate-management state/key checks occur in v0.1.0"),
        "H": source_evidence(evidence, first, r"engine\.run\s*\(|await\s+engine\.run|discoveries\s*:\s*\[", "A bootstrap-to-engine/output-state path occurs in v0.1.0"),
    }
    conditions = [
        ("A", "candidate", "stable discovery identity is represented"),
        ("B", "acquisition", "executable acquisition code is represented in the statically parseable occurrence"),
        ("C", "observation", "structured Observation is represented"),
        ("D", "recognition", "recognition is separable from acquisition"),
        ("E", "expansion", "discoveries can yield new candidates"),
        ("F", "repetition", "scheduled revisiting/repetition is represented"),
        ("G", "scheduler", "duplicate-management and scheduling state are represented"),
        ("H", "discovery", "an entry-to-discovery/output-state path is represented"),
    ]
    for letter, feat, text in conditions:
        evrefs = r(feat)
        if letter in threshold_extra:
            evrefs.append(threshold_extra[letter])
        if letter == "B":
            evrefs.append(upstream_evidence(evidence, "historical-source/RECONSTRUCTION-MANIFEST.yaml", first["snapshot_id"], "v0.1.0 acquisition-bearing occurrence passes static parsing", "PROVED"))
        add(f"claim-generic-{letter.lower()}", f"Strict-generic condition {letter}: {text} in v0.1.0.", "SUPPORTED", evrefs)
    add("claim-earliest-runnable", "v0.1.0 is the earliest recovered complete occurrence classified LIKELY_EXECUTABLE by retrospective static validation; historical execution remains UNKNOWN.", "SUPPORTED", r("candidate") + [upstream_evidence(evidence, "historical-source/RECONSTRUCTION-MANIFEST.yaml", first["snapshot_id"], "v0.1.0 is LIKELY_EXECUTABLE and historical execution UNKNOWN", "PROVED")])
    add("claim-earliest-generic", "v0.1.0 is the earliest recovered architecture satisfying strict conditions A-H at source-local SUPPORTED confidence.", "SUPPORTED", [], [f"claim-generic-{x.lower()}" for x,_,_ in conditions])
    add("claim-earliest-contract", "Earliest contract-driven architecture is UNKNOWN because Protocol-v7 outputs are unavailable; source shapes are not silently promoted to validated contracts.", "UNKNOWN", [upstream_evidence(evidence, "historical-source/security/SECURITY-MANIFEST.yaml", "upstream_availability.v7_present", "Protocol-v7 output is absent", "PROVED")])
    add("claim-closure", "Every complete recovered occurrence represents recursive discovery closure mechanisms, but no occurrence proves exhaustive search completeness.", "SUPPORTED", r("expansion") + r("repetition"))
    add("claim-exhaustive-closure", "Recovered recursive closure guarantees exhaustive search completeness.", "CONTRADICTED", [upstream_evidence(evidence, "historical-source/security/RESOURCE-BOUNDS.yaml", "bounds", "Finite depth, frontier, body, timeout, and retry mechanisms constrain search without proving exhaustive coverage", "SUPPORTED")], ["claim-closure"])
    add("claim-protocol", "Recovered snapshots remain web-protocol coupled; protocol-independent genericity is not proved historically.", "SUPPORTED", r("acquisition"))
    add("claim-acceptance", "Protocol-v9 cannot receive full acceptance in this checkout.", "PROVED", [upstream_evidence(evidence, "historical-source/security/SECURITY-MANIFEST.yaml", "prerequisite_acceptance", "Upstream acceptance is blocked", "PROVED")])
    add("claim-current-separation", "Current architecture proposals are retrospective/current context and are not evidence for missing historical implementation.", "SUPPORTED", [upstream_evidence(evidence, "historical-source/security/CURRENT-PROPOSED-SECURITY.yaml", "temporal_scope", "Current analysis is separated from historical snapshots", "SUPPORTED")], boundary="current-versus-historical")
    add("claim-causal-limit", "Most transition motivations remain UNKNOWN; atomic deltas do not establish authorial cause.", "SUPPORTED", [x for e in events for x in e["evidence_refs"]][:10])

    def rv(version, feature_names):
        return sorted({refs[(s["snapshot_id"], f)] for s in snapshots if s["historical_version"] == version for f in feature_names if (s["snapshot_id"], f) in refs})
    add("claim-version-v010", "v0.1.0 represents the earliest recovered candidate-centric closed web discovery loop.", "SUPPORTED", rv("v0.1.0", ["candidate", "observation", "discovery", "expansion", "repetition"]), ["claim-earliest-generic"])
    add("claim-version-v020", "v0.2.0 represents a reusable multi-provider pipeline with explicit candidate claiming.", "SUPPORTED", rv("v0.2.0", ["provider_abstraction", "recognition", "claim"]))
    add("claim-version-v030", "v0.3.0 retains the claimed provider pipeline, adds explicit bounded retry, and elaborates cancellation with controller-based timeout handling.", "SUPPORTED", rv("v0.3.0", ["claim", "retry", "cancellation"]))
    add("claim-version-v040", "v0.4.0 is preserved as divergent richer-provider/provenance/failure-handling alternatives.", "SUPPORTED", rv("v0.4.0", ["recognition", "provenance", "recognition_error_containment", "network_observation"]))
    add("claim-version-v050", "v0.5.0 preserves three divergent provider/resource/observability occurrences, including one static parse failure.", "SUPPORTED", rv("v0.5.0", ["recognition", "provenance", "retry", "network_observation"]) + [upstream_evidence(evidence, "historical-source/RECONSTRUCTION-MANIFEST.yaml", "snapshot-0009", "v0.5.0 snapshot-0009 fails static parsing while other v0.5.0 variants pass", "PROVED")])
    add("claim-version-v060", "v0.6.0 preserves three broad provider/policy/diagnostic/resource-control experiments.", "SUPPORTED", rv("v0.6.0", ["recognition", "provenance", "retry", "network_observation", "structured_diagnostics", "acquisition_policy"]))
    add("claim-version-v071", "v0.7.1 represents explicit acquisition policy, plan, and decision-ledger structures around the recursive pipeline.", "SUPPORTED", rv("v0.7.1", ["acquisition_policy", "acquisition_plan", "decision_ledger", "recognition", "expansion"]))
    return claims


def build_markdown_outputs(out, snapshots, by_version, features, refs, data_models, providers,
                           vectors, events, causal, complexity, failure_events, trust_boundaries,
                           authority, resource_bounds, evidence):
    # Architecture evolution and historical topologies.
    epochs = [
        ("E1", "v0.1.0", "Candidate-centric closed recognition loop", "The earliest recovered occurrence already contains Candidate, Observation, acquisition, recognition, Discovery, expansion, scheduling, and knowledge state."),
        ("E2", "v0.2.0-v0.3.0", "Providerized claimed pipeline", "Multiple response providers and an explicit claim operation appear; retry/cancellation state becomes more explicit."),
        ("E3", "v0.4.0-v0.6.0", "Branching reliability, provenance, and observability experiments", "Parallel alternatives add provider kinds, error-containment forms, origin/budget structures, and richer diagnostics without proving one linear lineage."),
        ("E4", "v0.7.1", "Policy/plan/ledger recomposition", "Acquisition policy, plans, decisions, and ledger structures become explicit while provider interaction changes."),
    ]
    arch = md_front("Architecture Evolution")
    arch += "## Historical architecture (recovered snapshots)\n\nThe diagrams below are source-local structural interpretations, not source code and not proof of runtime behavior.\n\n"
    for v in ["v0.1.0", "v0.2.0", "v0.3.0", "v0.4.0", "v0.5.0", "v0.6.0", "v0.7.1"]:
        ss = by_version[v]
        arch += f"### {v}\n\n"
        arch += "```text\nSeed/DOM\n  -> Candidate identity -> Scheduler/Knowledge state -> Worker/Engine\n  -> Web acquisition -> Observation -> Recognizer/Provider set\n  -> Discovery/provenance -> Candidate expansion -> Scheduler/Knowledge state\n```\n\n"
        arch += "Occurrences: " + ", ".join(f"`{s['snapshot_id']}` ({s['variant']}; {s['executability']})" for s in ss) + ". "
        arch += "Providers/recognizers: " + "; ".join(f"{s['variant']}: {', '.join(providers[s['snapshot_id']]['providers'])}" for s in ss) + ".\n\n"
        arch += table(["Branch occurrence", "Variant", "Recovered model nodes", "Provider count", "Policy/ledger", "Failure rows", "Bound rows"], [
            (s["snapshot_id"], s["variant"], ", ".join(data_models[s["snapshot_id"]]["fields"].keys()), len(providers[s["snapshot_id"]]["providers"]),
             "present" if any(features[s["snapshot_id"]][x] for x in ["acquisition_policy", "acquisition_plan", "decision_ledger"]) else "not scanned",
             sum(x["snapshot_id"] == s["snapshot_id"] for x in failure_events),
             sum(x["snapshot_id"] == s["snapshot_id"] for x in resource_bounds)) for s in ss]) + "\n"
    arch += "## Retrospective phase model\n\n" + table(["Epoch", "Range", "Interpretive label", "Evidence-bounded meaning"], epochs)
    arch += "\nThese epoch boundaries are `INFERRED` analytical groupings. They do not assert source lineage. The prompt's hypothetical URL-only and structured-observation precursor phases are not recovered: v0.1.0 already has Candidate and Observation structures.\n\n"
    arch += "## Current architecture\n\nCurrent planning adds protocol-independent acquisition, stronger contracts, capability policy, integrity, and security boundaries. Those are current targets, not backward evidence for v0.1-v0.7.1. See `CONTRACT-SECURITY-INTEGRATION.md`.\n"
    write_md("ARCHITECTURE-EVOLUTION.md", arch)

    algo = md_front("Algorithm and Scheduler Evolution")
    algo += "## Workflow by occurrence\n\n" + table(
        ["Snapshot", "Version", "Candidate", "Acquire", "Observe", "Recognize", "Expand", "Repeat", "Retry", "Static execution"],
        [(s["snapshot_id"], s["historical_version"], *("yes" if features[s["snapshot_id"]][k] else "not scanned" for k in ["candidate","acquisition","observation","recognition","expansion","repetition","retry"]), s["executability"]) for s in snapshots])
    algo += "\n## Scheduler state transitions\n\n```text\npending -> running/claimed -> done\n                    \\-> failure -> retry/requeue when represented -> terminal failure\n```\n\n"
    algo += "The diagram is a union interpretation, not a claim that every variant has identical transitions. Candidate status and queue/knowledge state occur from v0.1.0. `claimNextCandidate` is explicit from v0.2.0. Attempts/requeue/backoff become explicit in later occurrences. Cancellation signals appear, but stop guarantees remain unproved.\n\n"
    algo += "## Boundedness and convergence\n\n"
    algo += "Resource mechanisms include worker limits, retry/attempt limits, depth/body/frontier controls, timeouts, and per-origin controls in varying combinations. They bound particular operations; they do not prove global termination, exhaustive coverage, fairness, or convergence. Duplicate suppression is stateful but not proved atomic in every variant.\n\n"
    algo += "## Complexity and stability\n\nProvider and model counts increase, but variants make growth non-monotonic. No composite maturity score is computed: execution, validation, contracts, security, and algorithmic closure remain independent.\n"
    write_md("ALGORITHM-AND-SCHEDULER-EVOLUTION.md", algo)

    provider_md = md_front("Provider and Acquisition Evolution")
    provider_md += table(["Snapshot", "Version", "Variant", "Providers / recognizers", "Acquisition coupling"],
                         [(s["snapshot_id"], s["historical_version"], s["variant"], ", ".join(providers[s["snapshot_id"]]["providers"]), "Web URL + GM/fetch/HTTP-shaped") for s in snapshots])
    provider_md += "\n## Interpretation\n\n- v0.1.0 uses a concrete `HtmlRecognizer`; it demonstrates separable recognition but not the later reusable provider family.\n- v0.2.0 introduces multiple response provider occurrences. Later versions broaden media/protocol recognition names. Names do not prove lineage.\n- v0.4-v0.6 alternatives diverge in provider sets and failure handling; no canonical branch is selected.\n- v0.7.1 makes policy/plan/decision structures explicit. Provider ownership and candidate expansion must be interpreted per occurrence, not assumed stable.\n- Error-containment mechanisms (whole-item catches and, where directly evidenced, narrower catches or settled aggregation) improve continuation behavior, but neither complete provider isolation nor integrity is guaranteed.\n- Historical acquisition remains HTTP/browser/userscript coupled. Current protocol-independent acquisition is a separate target.\n"
    write_md("PROVIDER-AND-ACQUISITION-EVOLUTION.md", provider_md)

    obs = md_front("Observation and Provenance Evolution")
    rows=[]
    for s in snapshots:
        fs=data_models[s["snapshot_id"]]["fields"]
        surfaces = []
        if features[s["snapshot_id"]]["network_observation"]: surfaces.append("network observation")
        if features[s["snapshot_id"]]["structured_diagnostics"]: surfaces.append("diagnostic/trace/metric syntax")
        if features[s["snapshot_id"]]["acquisition_policy"]: surfaces.append("acquisition policy")
        if features[s["snapshot_id"]]["acquisition_plan"]: surfaces.append("acquisition plan")
        if features[s["snapshot_id"]]["decision_ledger"]: surfaces.append("decision ledger")
        rows.append((s["snapshot_id"],s["historical_version"],", ".join(fs.get("Observation",[])) or "none", "yes" if features[s["snapshot_id"]]["provenance"] else "limited/implicit", ", ".join(surfaces) or "none scanned"))
    obs += table(["Snapshot", "Version", "Observation fields", "Explicit provenance syntax", "Additional source surfaces"], rows)
    obs += "\nObservations are structured from the earliest complete occurrence, separating acquisition facts from interpretation. Discovery records carry candidate/observation associations and provenance-shaped fields in many occurrences. Later alternatives add network observations, edges, traces, diagnostics, or decision records. This supports increasing observability surface, not end-to-end provenance integrity: identifiers can be generated or propagated incorrectly, mutable stores can corrupt lineage, and Protocol-v7 contracts are unavailable.\n"
    write_md("OBSERVATION-PROVENANCE-EVOLUTION.md", obs)

    closure = md_front("Discovery Closure Analysis")
    closure += table(["Snapshot", "Version", "Expansion mechanism", "Repeating scheduler", "Closure classification", "Exhaustive?"],
                     [(s["snapshot_id"],s["historical_version"],"present" if features[s["snapshot_id"]]["expansion"] else "unknown","present" if features[s["snapshot_id"]]["repetition"] else "unknown","STATIC_RECURSIVE_CLOSURE_SUPPORTED" if features[s["snapshot_id"]]["expansion"] and features[s["snapshot_id"]]["repetition"] else "UNKNOWN","NO") for s in snapshots])
    closure += "\n**Closure means:** a discovery can yield candidate work that re-enters scheduler/knowledge state. It does not mean exhaustive crawling. Convergence depends on duplicate identity, depth/frontier/body/time/retry budgets, provider behavior, asynchronous additions, and origin policy. Termination remains conditional. Snapshot-0009 is structurally exact but statically non-executable; its represented closure cannot be upgraded to runnable closure.\n"
    write_md("DISCOVERY-CLOSURE-ANALYSIS.md", closure)

    integ = md_front("Contract and Security Integration")
    integ += "## Integration boundary\n\nProtocol-v8 is internally validated (`87/87 PASS`) but explicitly prerequisite-blocked. Protocol-v7 is physically absent, so no historical source shape is relabeled as a verified contract.\n\n"
    integ += table(["Dimension", "Historical source-local result", "Contract result", "Security result", "Confidence"], [
        ("Identity", "Candidate/Observation/Discovery identifiers occur", "UNKNOWN", "Mutable/generated identity is a mechanism, not integrity", "SUPPORTED / UNKNOWN"),
        ("Acquisition", "HTTP/browser acquisition occurs", "UNKNOWN", "External network and parser boundaries are explicit", "SUPPORTED"),
        ("Scheduling", "Queues/status/claims/retries occur", "UNKNOWN", "Race and resource risks remain", "SUPPORTED"),
        ("Provider execution", "Provider/recognizer families occur", "UNKNOWN", "Isolation varies; complete sandboxing not proved", "SUPPORTED"),
        ("Provenance", "Associations/edges/ledger-shaped records occur", "UNKNOWN", "Provenance integrity is not guaranteed", "SUPPORTED"),
        ("Policy", "Explicit in v0.7.1", "UNKNOWN", "Policy objects do not prove enforcement completeness", "SUPPORTED / UNKNOWN"),
    ])
    integ += "\n## Historical, retrospective, current\n\n1. **Historical architecture:** reconstructed snapshot source and direct state.\n2. **Retrospective interpretation:** Protocol-v3 and provisional Protocol-v8 models.\n3. **Current architecture:** current planning documents.\n\nEvidence never flows backward from 2 or 3 to prove 1. Security-shaped code is classified as a mechanism unless runtime and contract evidence proves a guarantee.\n"
    write_md("CONTRACT-SECURITY-INTEGRATION.md", integ)

    plan = md_front("Planned vs Implemented")
    plan += table(["Version", "Planned", "Described", "Implemented occurrence", "Historically tested", "Verified now"],
                  [(v,"UNKNOWN","Comments/names present; not design proof", "; ".join(f"{s['snapshot_id']}:{s['executability']}" for s in by_version[v]),"UNKNOWN","Retrospective static source-local only") for v in by_version])
    plan += "\n## Divergence rules\n\n- A roadmap or current planning statement is `planned`, not historical code.\n- A comment/interface is `described`, not proof of complete semantics.\n- Reconstructed code is an occurrence, not proof of historical execution.\n- Static parse validation is retrospective verification, not a historical test.\n- snapshot-0009 proves the distinction sharply: it is an exact complete occurrence but fails parsing.\n\n## Current-plan gap\n\nCurrent plans describe protocol independence, capability/security policy, stronger contracts, and integrity validation beyond what recovered snapshots prove. Those gaps are not treated as historical defects unless the historical source itself states the requirement.\n"
    write_md("PLANNED-VS-IMPLEMENTED.md", plan)

    epochs_md = md_front("Architecture Epochs") + table(["Epoch","Range","Label","Boundary status"], [(x[0],x[1],x[2],"INFERRED") for x in epochs])
    epochs_md += "\nPhase transitions are useful compression, not a recovered branch graph. The recovered record starts after any hypothetical URL-only or unstructured precursor: no such earlier complete implementation is available.\n"
    write_md("ARCHITECTURE-EPOCHS.md", epochs_md)

    conv = md_front("Convergence and Divergence")
    conv += "## Convergence points\n\n- **v0.1.0:** Candidate, Observation, acquisition, recognition, Discovery, expansion, scheduler, and knowledge state coexist.\n- **v0.2.0:** the same loop coexists with a reusable multi-provider family and explicit claim operation.\n- **v0.7.1:** policy, acquisition plans, decisions/ledger, providers, observations, discoveries, and scheduling coexist in one recovered occurrence.\n\n## Divergence points\n\n- Acquisition already has userscript/GM and fetch/HTTP-shaped alternatives.\n- v0.4.0 through v0.6.0 preserve multiple complete variants with different providers, models, failure handling, and topology.\n- v0.5.0 includes both likely executable and non-executable exact complete variants.\n- Recognition signatures and provider ownership vary; sameness is not assumed.\n\n## Dead ends and reintroduction\n\nNo deletion, abandonment, or reintroduction is `PROVED`. Non-occurrence at a later version is recorded as disappearance only. Recurring names are occurrence similarity with identity `UNKNOWN`.\n"
    write_md("CONVERGENCE-AND-DIVERGENCE.md", conv)

    caps = md_front("Capability Emergence")
    caps += table(["Capability","First mention/code/use","First test","First verification","Stabilization","Confidence"], [
        ("Coherent candidate-centric workflow","v0.1.0","UNKNOWN","Retrospective static only","UNKNOWN","SUPPORTED"),
        ("Recursive discovery closure mechanism","v0.1.0","UNKNOWN","Retrospective static only","UNKNOWN","SUPPORTED"),
        ("Parallel/concurrent workers","v0.1.0","UNKNOWN","Retrospective static only","UNKNOWN","SUPPORTED"),
        ("Reusable multi-provider recognition","v0.2.0","UNKNOWN","Retrospective static only","UNKNOWN","SUPPORTED"),
        ("Timeout cancellation signal","v0.1.0","UNKNOWN","Retrospective static only","UNKNOWN","SUPPORTED"),
        ("Bounded retry and controller-based timeout handling","v0.3.0","UNKNOWN","Retrospective static only","UNKNOWN","SUPPORTED"),
        ("Recognition error containment","v0.2.0; later forms vary","UNKNOWN","Retrospective source-local","UNKNOWN","SUPPORTED"),
        ("Policy/plan/ledger inspectability","v0.7.1","UNKNOWN","Retrospective source-local","UNKNOWN","SUPPORTED"),
        ("Protocol-independent execution","UNKNOWN","UNKNOWN","UNKNOWN","UNKNOWN","UNKNOWN"),
        ("Contract-driven architecture","UNKNOWN","UNKNOWN","UNKNOWN","UNKNOWN","UNKNOWN"),
    ])
    caps += "\nCapability loss is not inferred from disappearance. Snapshot-0009 loses static executability for that occurrence, but does not prove a version-wide historical regression because other v0.5.0 variants parse.\n"
    write_md("CAPABILITY-EMERGENCE.md", caps)

    stability = md_front("Stability Analysis")
    stability += table(["Concept","Role stability","Implementation stability","Contract stability","Evidence-bounded conclusion"], [
        ("Candidate","High across occurrences","Fields/status vary","UNKNOWN","Persistent work identity; no identity-lineage proof"),
        ("Observation","High","Fields and network detail vary","UNKNOWN","Persistent acquisition record"),
        ("Discovery","High","Kinds/provenance vary","UNKNOWN","Persistent interpreted result"),
        ("Scheduler/frontier","Medium-high","Dedicated/embedded forms vary","UNKNOWN","Persistent revisiting role"),
        ("Provider/recognizer","Medium","Families/signatures/ownership vary","UNKNOWN","Extensibility grows but abstraction is unstable"),
        ("Acquisition","High web coupling","GM/fetch/policy forms vary","UNKNOWN","Historically web-bound"),
        ("Provenance","Medium-high","Associations/graphs/ledger vary","UNKNOWN","Visibility increases; integrity unproved"),
        ("Security boundaries","Medium","Counts and enforcement vary","UNKNOWN","Mechanisms present; guarantees limited"),
    ])
    stability += "\nNo aggregate stability or maturity score is used. Variants, unknown lineage, absent Protocol-v7, and no historical tests prevent a stabilization claim.\n"
    write_md("STABILITY-ANALYSIS.md", stability)


def build_final_report(out, snapshots, events, causal, claims, contradictions, uncertainties, invariants, complexity, security_validation):
    by_claim={c["claim_id"]:c for c in claims}
    report=md_front("Final Historical Report — Generic Discovery Engine")
    report += "## Executive conclusion\n\nThe earliest recovered complete architecture, **v0.1.0**, is already a candidate-centric recursive discovery engine rather than a URL-only precursor. At source-local `SUPPORTED` confidence it represents Candidate identity, web acquisition, structured Observation, separable recognition, Discovery, discovery-to-candidate expansion, revisiting scheduling, duplicate-management state, and an entry-to-output workflow. It is also the earliest recovered occurrence classified `LIKELY_EXECUTABLE`, although historical execution is `UNKNOWN`.\n\nThe architecture then becomes multi-provider and explicitly claimed (v0.2), adds bounded retries and controller-based timeout handling (v0.3), branches into richer provider, provenance, error-containment, and observability experiments (v0.4-v0.6), and reaches an explicit policy/plan/decision-ledger recomposition at v0.7.1. This sequence is not asserted to be one linear source lineage.\n\n**Full historical acceptance is impossible here:** Protocol-v1 byte/range validation fails, Protocol-v4-v7 outputs are absent, and Protocol-v8 is provisional. Contract-driven onset therefore remains `UNKNOWN`.\n\n"
    report += "## Strict earliest-generic definition A-H\n\n" + table(["Condition","v0.1.0 result","Confidence","Provenance"],[(x,by_claim[f"claim-generic-{x.lower()}"]["claim"],"SUPPORTED",f"`claim-generic-{x.lower()}`") for x in "ABCDEFGH"])
    report += "\nThe strict result is **v0.1.0 (SUPPORTED, source-local, prerequisite-blocked)**. This is not silently upgraded to `PROVED`; the conjunctive dependency is `claim-earliest-generic`.\n\n"
    report += "## Version-by-version model\n\n" + table(["Version","What it became","Historical caution","Provenance"], [
        ("v0.1.0","Candidate-centric closed web discovery loop with structured observations, recognition, discoveries, expansion, worker scheduling, duplicate state, and knowledge storage","Historical runtime unknown","`claim-version-v010`; `state-snapshot-0001`"),
        ("v0.2.0","Reusable multi-provider interpretation plus explicit candidate claiming","Cause mostly unknown","`claim-version-v020`; `state-snapshot-0003`"),
        ("v0.3.0","Claimed provider pipeline with bounded retries and controller-based timeout handling","No historical tests","`claim-version-v030`; `state-snapshot-0005`"),
        ("v0.4.0","Divergent richer-provider/provenance/error-handling architectures","Two complete alternatives; no canonical branch","`claim-version-v040`; states 0006/0008"),
        ("v0.5.0","Further provider, resource, and observability divergence","Three variants; one exact occurrence is non-executable","`claim-version-v050`; states 0007/0009/0011"),
        ("v0.6.0","Broader provider and policy/diagnostic/resource-control experiments","Three variants; lineage unknown","`claim-version-v060`; states 0010/0012/0013"),
        ("v0.7.1","Policy/plan/decision-ledger recomposition around acquisition and provider execution","Contract validation unavailable","`claim-version-v071`; `state-snapshot-0014`"),
    ])
    report += "\n## Twenty final historical questions\n\n"
    answers=[
        (1,"What is the earliest runnable architecture?","v0.1.0 is earliest `LIKELY_EXECUTABLE`; historical execution is `UNKNOWN`.","SUPPORTED"),
        (2,"What is the earliest generic architecture under A-H?","v0.1.0 satisfies all eight represented-mechanism conditions.","SUPPORTED"),
        (3,"What is the earliest contract-driven architecture?","Unavailable because Protocol-v7 is absent.","UNKNOWN"),
        (4,"What was the first coherent architecture?","v0.1.0, already candidate-centric and recursively closed.","SUPPORTED"),
        (5,"When did reusable provider extensibility emerge?","v0.2.0 is the first recovered multi-provider abstraction occurrence.","SUPPORTED"),
        (6,"When did discovery become recursively closed?","Already represented in v0.1.0 through expansion and revisiting.","SUPPORTED"),
        (7,"Is closure exhaustive?","No exhaustive-completeness proof exists; asserting it is contradicted by bounded, provider-dependent search.","CONTRADICTED"),
        (8,"How did scheduling evolve?","Persistent queue/knowledge revisiting gains explicit claiming, retry/backoff, cancellation, and policy/resource controls in varying variants.","SUPPORTED"),
        (9,"How did acquisition evolve?","Web acquisition persists while implementation varies from userscript/fetch-shaped mechanisms to explicit policy/plan structures.","SUPPORTED"),
        (10,"How did observation evolve?","Structured Observation exists at v0.1; later variants enrich network, diagnostic, trace, and decision context.","SUPPORTED"),
        (11,"How did provenance evolve?","Candidate-observation-discovery links persist and later grow graph/trace/ledger forms; integrity remains unproved.","SUPPORTED"),
        (12,"How did failure handling evolve?","Local catches and status handling expand into retries, cancellation, varying recognition error containment, and structured diagnostics, unevenly by branch.","SUPPORTED"),
        (13,"How did concurrency evolve?","Worker concurrency exists early; explicit atomic claiming and origin/resource controls address additional coordination surfaces.","SUPPORTED"),
        (14,"How did security evolve?","Trust, authority, parser, and resource mechanisms become more explicit, but mechanisms are not guarantees.","SUPPORTED"),
        (15,"Which invariants survived?","Candidate work identity, acquisition-before-interpretation, Observation/Discovery separation, expansion, revisiting, and web coupling recur.","INFERRED"),
        (16,"Where did architectures diverge?","Most visibly across v0.4-v0.6 complete alternatives and acquisition/provider forms.","SUPPORTED"),
        (17,"Which concepts were abandoned or reintroduced?","None can be proved abandoned/reintroduced; disappearance and recurrence preserve identity uncertainty.","UNKNOWN"),
        (18,"What pressures caused transitions?","Duplicate coordination, failure continuation, bounded resources, provider growth, provenance, and inspectability are mechanism-supported pressures; authorial intent is mostly unknown.","SUPPORTED"),
        (19,"What was tested and stabilized historically?","No verified historical test lineage or stabilization point is available.","UNKNOWN"),
        (20,"What did the system ultimately become?","By v0.7.1 it is a web-coupled, candidate-centric, recursive, provider-extensible discovery engine with explicit acquisition policy/plans and decision records—not yet a proved protocol-independent or contract-verified engine.","SUPPORTED"),
    ]
    answer_provenance = [
        "`claim-earliest-runnable`", "`claim-earliest-generic` + A-H dependencies", "`claim-earliest-contract`",
        "`claim-version-v010`", "`claim-version-v020`", "`claim-closure`", "`claim-exhaustive-closure`",
        "`EVOLUTION-EVENTS.yaml` scheduler events", "`PROVIDER-AND-ACQUISITION-EVOLUTION.md` + event records",
        "`OBSERVATION-PROVENANCE-EVOLUTION.md`; state vectors", "`OBSERVATION-PROVENANCE-EVOLUTION.md`; state vectors",
        "`FAILURE-EVENTS.yaml`; event records", "state vectors; claim events", "`CONTRACT-SECURITY-INTEGRATION.md`; Protocol-v8 records",
        "`INVARIANTS.yaml`", "`CONVERGENCE-AND-DIVERGENCE.md`; occurrence states", "`CONCEPT-GENEALOGY.yaml`",
        "`CAUSAL-CLAIMS.yaml`", "`CONCEPT-GENEALOGY.yaml`; `PLANNED-VS-IMPLEMENTED.md`", "`claim-version-v071`",
    ]
    answers = [(*row, answer_provenance[i]) for i, row in enumerate(answers)]
    report += table(["#","Question","Answer","Status","Provenance"],answers)
    report += "\nMachine-resolvable evidence identifiers for claim records are in `CLAIMS.yaml`; every identifier resolves through `HISTORICAL-CLAIMS-GRAPH.json` to `EVIDENCE-LEDGER.yaml`.\n\n## Causal reconstruction\n\n"
    cc=Counter(c["causal_confidence"] for c in causal)
    report += f"The corpus records {len(events)} atomic adjacent-version events and {len(causal)} corresponding causal assessments: " + ", ".join(f"{k}={v}" for k,v in sorted(cc.items())) + ". Most causal labels remain `UNKNOWN`; alternatives are explicit in `CAUSAL-CLAIMS.yaml`.\n\n"
    report += "## Maturity without collapse\n\n" + table(["Axis","Terminal recovered state","Confidence"], [
        ("Architecture","Policy/plan/ledger candidate-centric pipeline","SUPPORTED"),
        ("Algorithm","Recursive bounded work loop; exhaustive convergence unproved","SUPPORTED"),
        ("Contracts","Unavailable Protocol-v7 integration","UNKNOWN"),
        ("Execution","v0.7.1 likely executable; historical runtime unknown","SUPPORTED / UNKNOWN"),
        ("Providers","Broad multi-provider family","SUPPORTED"),
        ("Provenance/observability","Structured records and ledger-shaped visibility","SUPPORTED"),
        ("Security","Mechanisms and boundaries modeled; guarantees limited","SUPPORTED"),
        ("Testing/stability","No verified historical evidence","UNKNOWN"),
    ])
    report += "\n## Contradictions and uncertainty\n\nFour contradictions or input-consistency conflicts are preserved: broken v1 bytes/ranges, v3's internal pass over that broken chain, an exact v0.5 variant that fails parsing, and absent required v4-v7 outputs. Fifteen major uncertainties remain registered. Nothing was repaired or filled.\n\n"
    report += "## Acceptance\n\n- Protocol-v8 validation: `87/87 PASS`, acceptance `PROVISIONAL_ONLY_UPSTREAM_BLOCKED`.\n- Protocol-v9 corpus disposition (even when internal checks pass): `PROVISIONAL_ONLY_UPSTREAM_BLOCKED`; independent results are recorded in `VALIDATION.yaml`.\n- Full acceptance: **BLOCKED** until source integrity and missing Protocol-v4-v7 prerequisites are resolved outside this synthesis.\n"
    write_md("FINAL-HISTORICAL-REPORT.md", report)


if __name__ == "__main__":
    main()
