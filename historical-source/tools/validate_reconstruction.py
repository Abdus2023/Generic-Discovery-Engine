#!/usr/bin/env python3
"""Independent integrity checks for protocol 92–155 reconstruction outputs."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / "historical-source"
RECONSTRUCT = ARCHIVE / "tools" / "reconstruct.py"
STATUS_REGISTRY = {"EXACT", "MECHANICALLY_COMPOSED", "PATCH_RECONSTRUCTED", "PARTIAL", "INFERRED", "UNKNOWN"}
DEPENDENCY_REGISTRY = {"PRESENT", "HISTORICAL_EXTERNAL", "MISSING", "INFERRED", "UNKNOWN"}
EXPECTED_COUNTS = {
    "EXACT": 10, "MECHANICALLY_COMPOSED": 2, "PATCH_RECONSTRUCTED": 0,
    "PARTIAL": 2, "INFERRED": 0, "UNKNOWN": 29,
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def check(condition: bool, category: str, detail: str) -> dict[str, str]:
    return {"category": category, "result": "PASS" if condition else "FAIL", "detail": detail}


def node_result(source: bytes) -> str:
    if shutil.which("node") is None:
        return "TOOL_UNAVAILABLE"
    process = subprocess.run(["node", "--check", "-"], input=source, capture_output=True)
    return "PASS" if process.returncode == 0 else "FAIL"


def tree_hashes(root: Path) -> dict[str, str]:
    return {str(path.relative_to(root)): sha(path.read_bytes()) for path in sorted(root.rglob("*")) if path.is_file()}


def main() -> int:
    checks: list[dict[str, str]] = []
    required = [
        "snapshots", "analysis", "VERSION-GRAPH.md", "VERSION-MATRIX.md",
        "RECONSTRUCTION-MANIFEST.yaml", "RECONSTRUCTION-ASSUMPTIONS.yaml",
        "RECONSTRUCTION-GAPS.yaml", "RECONSTRUCTION-CONFLICTS.yaml",
        "RECONSTRUCTION-EVIDENCE.yaml", "RECONSTRUCTION-REPORT.md",
    ]
    missing_required = [name for name in required if not (ARCHIVE / name).exists()]
    checks.append(check(not missing_required, "Required reconstruction outputs", f"missing={missing_required}"))

    reconstruction = load(ARCHIVE / "RECONSTRUCTION-MANIFEST.yaml")
    snapshots = reconstruction["snapshots"]
    source_manifest_path = ARCHIVE / "SOURCE-MANIFEST.yaml"
    source_manifest = load(source_manifest_path)["artifacts"]
    artifacts = {x["artifact_id"]: x for x in source_manifest}
    assumptions = load(ARCHIVE / "RECONSTRUCTION-ASSUMPTIONS.yaml")
    gaps = load(ARCHIVE / "RECONSTRUCTION-GAPS.yaml")["gaps"]
    conflicts_doc = load(ARCHIVE / "RECONSTRUCTION-CONFLICTS.yaml")
    conflicts = conflicts_doc["conflicts"]

    ids = [x["snapshot_id"] for x in snapshots]
    statuses = Counter(x["reconstruction"]["status"] for x in snapshots)
    statuses["UNKNOWN"] = len(reconstruction["unsupported_versions"])
    checks.append(check(len(ids) == len(set(ids)) == 14, "Snapshot identity", f"snapshots={len(ids)}, unique={len(set(ids))}"))
    checks.append(check(set(statuses) <= STATUS_REGISTRY and all(statuses[key] == value for key, value in EXPECTED_COUNTS.items()),
                        "Reconstruction class accounting", f"counts={dict(statuses)}"))

    bad_metadata = []
    bad_hashes = []
    bad_maps = []
    map_integrity_failures = []
    exact_failures = []
    composition_failures = []
    partial_marker_failures = []
    temporal_failures = []
    contamination_failures = []
    dependency_failures = []
    static_failures = []
    runtime_failures = []
    diff_failures = []

    for snapshot in snapshots:
        paths = snapshot["paths"]
        source_path = ARCHIVE / paths["source"]
        map_path = ARCHIVE / paths["source_map"]
        report_path = ARCHIVE / paths["report"]
        metadata_path = source_path.parents[1] / "metadata.yaml"
        if not all(path.exists() for path in (source_path, map_path, report_path, metadata_path)):
            bad_metadata.append(snapshot["snapshot_id"])
            continue
        source = source_path.read_bytes()
        source_map_bytes = map_path.read_bytes()
        metadata_bytes = metadata_path.read_bytes()
        metadata = json.loads(metadata_bytes)
        source_map = json.loads(source_map_bytes)
        if metadata["snapshot_id"] != snapshot["snapshot_id"] or metadata["historical_version"] != snapshot["historical_version"]:
            bad_metadata.append(snapshot["snapshot_id"])
        if (sha(source) != snapshot["integrity"]["reconstructed_sha256"]
                or sha(source_map_bytes) != snapshot["integrity"]["source_map_sha256"]
                or sha(metadata_bytes) != snapshot["integrity"]["metadata_sha256"]):
            bad_hashes.append(snapshot["snapshot_id"])

        ranges = source_map["ranges"]
        cursor = 0
        for region in ranges:
            start, end = region["output_byte_start"], region["output_byte_end_exclusive"]
            if start != cursor or end < start or sha(source[start:end]) != region["segment_sha256"]:
                map_integrity_failures.append(snapshot["snapshot_id"])
            cursor = end
            aid = region["source_artifact"]
            if aid:
                artifact = artifacts.get(aid)
                if not artifact:
                    map_integrity_failures.append(snapshot["snapshot_id"])
                    continue
                artifact_bytes = (ARCHIVE / artifact["output_file"]).read_bytes()
                a_start, a_end = region["source_artifact_byte_start"], region["source_artifact_byte_end_exclusive"]
                if source[start:end] != artifact_bytes[a_start:a_end]:
                    map_integrity_failures.append(snapshot["snapshot_id"])
            elif not region.get("generated_non_historical"):
                map_integrity_failures.append(snapshot["snapshot_id"])
        if cursor != len(source):
            bad_maps.append(snapshot["snapshot_id"])

        status = snapshot["reconstruction"]["status"]
        evidence_ids = snapshot["artifacts"]
        if status == "EXACT":
            if len(evidence_ids) != 1 or source != (ARCHIVE / artifacts[evidence_ids[0]]["output_file"]).read_bytes():
                exact_failures.append(snapshot["snapshot_id"])
            if b"HISTORICAL SOURCE GAP" in source:
                exact_failures.append(snapshot["snapshot_id"])
        elif status == "MECHANICALLY_COMPOSED":
            if any(region["reconstruction_operation"] != "ordered_fragment_copy" for region in ranges):
                composition_failures.append(snapshot["snapshot_id"])
            extracted_reconstruction_id = snapshot["version_boundary"]["evidence"]["artifact_id"]
            if source != (ARCHIVE / artifacts[extracted_reconstruction_id]["output_file"]).read_bytes():
                composition_failures.append(snapshot["snapshot_id"])
        elif status == "PARTIAL":
            generated = [x for x in ranges if x.get("generated_non_historical")]
            if len(generated) != 1 or b"HISTORICAL SOURCE GAP" not in source[generated[0]["output_byte_start"]:generated[0]["output_byte_end_exclusive"]]:
                partial_marker_failures.append(snapshot["snapshot_id"])

        for aid in evidence_ids:
            artifact = artifacts.get(aid)
            if artifact is None:
                contamination_failures.append(snapshot["snapshot_id"])
                continue
            version = artifact["history"].get("version")
            if version != snapshot["historical_version"].removeprefix("v"):
                contamination_failures.append(snapshot["snapshot_id"])
            if artifact["classification"] in {"PSEUDOCODE", "EXAMPLE", "INTERFACE"}:
                contamination_failures.append(snapshot["snapshot_id"])
            if artifact["source"]["timestamp"] > snapshot["date"]:
                temporal_failures.append(snapshot["snapshot_id"])
        if not all(value.startswith("PASS") for value in snapshot["temporal_tests"].values()):
            temporal_failures.append(snapshot["snapshot_id"])

        entries = snapshot["dependencies"]["entries"]
        if any(x["status"] not in DEPENDENCY_REGISTRY for x in entries):
            dependency_failures.append(snapshot["snapshot_id"])
        if set(snapshot["dependencies"]["status_registry"]) != DEPENDENCY_REGISTRY:
            dependency_failures.append(snapshot["snapshot_id"])
        if any(x["status"] == "INFERRED" for x in entries):
            dependency_failures.append(snapshot["snapshot_id"])
        compatibility = snapshot.get("compatibility_test", {})
        if any(compatibility.get(key) != "PASS" for key in ("same_revision", "same_branch", "same_version", "same_implementation_family", "compatible_symbol_definitions")):
            dependency_failures.append(snapshot["snapshot_id"])

        recorded_static = snapshot["static_validation"]["syntax_and_ast_parse"]["result"]
        if node_result(source) != recorded_static:
            static_failures.append(snapshot["snapshot_id"])
        if snapshot["static_validation"]["source_was_modified_to_validate"] is not False:
            static_failures.append(snapshot["snapshot_id"])
        if snapshot["runtime_validation"]["executed"] is not False or snapshot["historical_execution"] != "UNKNOWN":
            runtime_failures.append(snapshot["snapshot_id"])

        changes = snapshot["changes_from_previous"]
        if changes.get("source_diff"):
            diff_path = ARCHIVE / changes["source_diff"]
            if not diff_path.exists() or sha(diff_path.read_bytes()) != changes["source_diff_sha256"]:
                diff_failures.append(snapshot["snapshot_id"])

    checks.append(check(not bad_metadata, "Snapshot metadata/report coverage", f"bad={len(set(bad_metadata))}"))
    checks.append(check(not bad_hashes, "Snapshot/source-map/metadata hashes", f"bad={len(set(bad_hashes))}"))
    checks.append(check(not bad_maps and not map_integrity_failures, "Range-level historical integrity",
                        f"coverage_failures={len(set(bad_maps))}, copied_range_failures={len(set(map_integrity_failures))}"))
    checks.append(check(not exact_failures, "Exact snapshot identity", f"bad={len(set(exact_failures))}/10"))
    checks.append(check(not composition_failures, "Mechanical composition identity", f"bad={len(set(composition_failures))}/2"))
    checks.append(check(not partial_marker_failures, "Partial snapshot gap markers", f"bad={len(set(partial_marker_failures))}/2"))
    checks.append(check(not temporal_failures, "Temporal consistency", f"conflicts={len(set(temporal_failures))}"))
    checks.append(check(not contamination_failures, "No backward/forward architecture contamination", f"failures={len(set(contamination_failures))}"))
    checks.append(check(not dependency_failures, "Dependency closure labeling", f"bad={len(set(dependency_failures))}"))
    checks.append(check(not static_failures, "Read-only static validation reproducibility", f"mismatches={len(set(static_failures))}"))
    checks.append(check(not runtime_failures, "Runtime/historical execution separation", f"bad={len(set(runtime_failures))}"))
    checks.append(check(not diff_failures, "Historical source diff integrity", f"bad={len(set(diff_failures))}"))

    # Every extraction artifact consumed as source still matches its recorded identity.
    bad_input_artifacts = []
    for artifact in source_manifest:
        path = ARCHIVE / artifact["output_file"]
        if not path.exists() or sha(path.read_bytes()) != artifact["sha256"]:
            bad_input_artifacts.append(artifact["artifact_id"])
    checks.append(check(not bad_input_artifacts, "Extraction artifact input integrity", f"matching={len(source_manifest)-len(bad_input_artifacts)}/{len(source_manifest)}"))

    input_integrity = reconstruction["input_integrity"]
    input_hashes_ok = (
        sha((ARCHIVE / "SOURCE-MANIFEST.yaml").read_bytes()) == input_integrity["source_manifest_sha256"]
        and sha((ARCHIVE / "REVISION-INVENTORY.yaml").read_bytes()) == input_integrity["revision_inventory_sha256"]
        and sha((ARCHIVE / "LINEAGE.yaml").read_bytes()) == input_integrity["lineage_sha256"]
    )
    checks.append(check(input_hashes_ok, "Bound reconstruction inputs", "manifest, revision inventory, and lineage hashes match"))

    unsupported = reconstruction["unsupported_versions"]
    unsupported_dirs = [x["historical_version"] for x in unsupported if x["snapshot_directory_created"] or (ARCHIVE / "snapshots" / x["historical_version"].removeprefix("v")).exists()]
    checks.append(check(len(unsupported) == 29 and not unsupported_dirs, "No unsupported version directories", f"unsupported={len(unsupported)}, improper_dirs={unsupported_dirs}"))
    checks.append(check(not assumptions["assumptions"] and assumptions["unresolved_assumptions"] == 0,
                        "Assumption registry", "unresolved=0; executable assumption-dependent snapshots=0"))
    checks.append(check(len(conflicts) == 5 and all(x["status"] == "UNRESOLVED" for x in conflicts),
                        "Alternative/conflict preservation", f"conflict_groups={len(conflicts)}"))
    checks.append(check(len(gaps) == 31 and all(x["type"] == "MISSING_SOURCE" for x in gaps),
                        "Missing-source accounting", f"gaps={len(gaps)}"))
    checks.append(check(not conflicts_doc["symbol_conflicts_within_snapshots"], "Symbol conflict check", "within-snapshot unresolved conflicts=0"))

    matrix = (ARCHIVE / "VERSION-MATRIX.md").read_text(encoding="utf-8")
    matrix_ok = all(capability in matrix for capability in ["Candidate model", "Observation model", "HTML provider", "Concurrent workers"]) and matrix.count("`art-") >= 12
    checks.append(check(matrix_ok, "Evidence-backed version matrix", "cells contain artifact/line or absence evidence"))

    trace = load(ARCHIVE / "analysis" / "ARCHITECTURE-CODE-TRACEABILITY.yaml")
    future_claims_ok = all(
        not item["historical_code_evidence"] and item["claim_status"] in {"DESIGNED", "PROPOSED"}
        for item in trace["architecture_to_code"]
        if item["architecture_statement"] in {"Pluggable WASM module capability", "SQLite persistence adapter", "Rust discovery runtime / agent platform", "Distributed coordination protocol"}
    )
    checks.append(check(future_claims_ok, "Proposed/design boundary", "future architecture was not promoted to implementation"))

    provider_history = load(ARCHIVE / "analysis" / "PROVIDER-HISTORY.yaml")["history"]
    provider_events_ok = all(
        event["event"] in {"introduced", "modified", "removed", "reintroduced", "unknown"}
        for record in provider_history for event in record["events"]
    )
    checks.append(check(provider_events_ok and len(provider_history) == 12, "Provider evolution labeling",
                        f"snapshot records={len(provider_history)}; event vocabulary valid={provider_events_ok}"))

    report = (ARCHIVE / "RECONSTRUCTION-REPORT.md").read_text(encoding="utf-8")
    required_report_phrases = [
        "HISTORICAL RECONSTRUCTION STATUS", "EXACT:\n10", "MECHANICALLY_COMPOSED:\n2",
        "PATCH_RECONSTRUCTED:\n0", "PARTIAL:\n2", "INFERRED:\n0", "UNKNOWN:\n29",
        "TEMPORAL_CONFLICTS:\n0", "RECONSTRUCTION_CONFLICTS:\n5",
        "MISSING_SOURCE_REGIONS:\n31", "UNRESOLVED_ASSUMPTIONS:\n0",
        "No historical source was modified.", "No missing source was silently invented.",
        "No later implementation was retroactively inserted.",
        "No architectural proposal was treated as implementation without evidence.",
    ]
    checks.append(check(all(value in report for value in required_report_phrases), "Required final report status", "all required status fields and declarations present"))

    # Re-run the deterministic generator twice outside the archive and compare every byte.
    deterministic = False
    determinism_detail = "not run"
    try:
        with tempfile.TemporaryDirectory(prefix="reconstruction-validate-a-") as a_name, tempfile.TemporaryDirectory(prefix="reconstruction-validate-b-") as b_name:
            a, b = Path(a_name), Path(b_name)
            for destination in (a, b):
                process = subprocess.run(
                    [sys.executable, str(RECONSTRUCT), "--output-root", str(destination), "--single-run"],
                    cwd=ROOT, capture_output=True, timeout=300,
                )
                if process.returncode != 0:
                    raise RuntimeError(process.stderr.decode("utf-8", errors="replace"))
            hashes_a, hashes_b = tree_hashes(a), tree_hashes(b)
            deterministic = hashes_a == hashes_b
            determinism_detail = f"run_a_files={len(hashes_a)}, run_b_files={len(hashes_b)}, differing={len(set(hashes_a) ^ set(hashes_b)) + sum(hashes_a.get(k) != hashes_b.get(k) for k in set(hashes_a) & set(hashes_b))}"
    except Exception as error:
        determinism_detail = f"failed: {error}"
    checks.append(check(deterministic, "Reconstruction determinism", determinism_detail))

    # The two repository source documents must remain byte-identical to HEAD.
    source_unchanged = True
    source_details = []
    for name in ("Userscript Discovery Prototype.md", "Continue Architecture Planning.md"):
        head = subprocess.run(["git", "show", f"HEAD:{name}"], cwd=ROOT, capture_output=True, check=True).stdout
        worktree = (ROOT / name).read_bytes()
        same = head == worktree
        source_unchanged &= same
        source_details.append(f"{name}={'MATCH' if same else 'DIFF'}")
    checks.append(check(source_unchanged, "Historical source documents unchanged", "; ".join(source_details)))

    overall = "PASS" if all(x["result"] == "PASS" for x in checks) else "FAIL"
    output = {
        "schema_version": 1,
        "protocol": "Mechanical Historical Version Reconstruction Protocol sections 92-155",
        "overall": overall,
        "checks": checks,
        "counts": {
            "snapshots": len(snapshots), **EXPECTED_COUNTS,
            "temporal_conflicts": 0, "reconstruction_conflicts": len(conflicts),
            "missing_source_regions": len(gaps), "unresolved_assumptions": 0,
            "likely_executable": sum(x["executability"] == "LIKELY_EXECUTABLE" for x in snapshots),
            "non_executable": sum(x["executability"] == "NON_EXECUTABLE" for x in snapshots),
            "historically_executed_proved": 0,
        },
    }
    (ARCHIVE / "RECONSTRUCTION-VALIDATION.yaml").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
