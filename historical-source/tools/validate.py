#!/usr/bin/env python3
"""Validate the generated historical source archive without changing source."""

from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / "historical-source"


def load(name: str):
    return json.loads((ARCHIVE / name).read_text(encoding="utf-8"))


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def check(condition: bool, category: str, detail: str, warning: bool = False) -> dict:
    return {
        "category": category,
        "result": "PASS" if condition else ("WARN" if warning else "FAIL"),
        "detail": detail,
    }


def main() -> int:
    manifest_doc = load("SOURCE-MANIFEST.yaml")
    artifacts = manifest_doc["artifacts"]
    index = load("ARTIFACT-INDEX.yaml")["artifacts"]
    detections = load("DETECTION-INVENTORY.yaml")["detections"]
    revisions = load("REVISION-INVENTORY.yaml")["revisions"]
    lineage = load("LINEAGE.yaml")
    duplicates = load("DUPLICATES.yaml")["duplicate_groups"]

    checks = []
    ids = [item["artifact_id"] for item in artifacts]
    id_set = set(ids)
    checks.append(check(
        len(ids) == len(id_set), "Artifact identifiers",
        f"{len(ids)} artifacts; {len(ids) - len(id_set)} duplicate identifiers",
    ))
    checks.append(check(
        len(index) == len(artifacts) and {x["artifact_id"] for x in index} == id_set,
        "Manifest/index count", f"manifest={len(artifacts)}, index={len(index)}",
    ))

    expected_files = {item["output_file"] for item in artifacts}
    duplicate_outputs = len(expected_files) != len(artifacts)
    actual_files = {
        str(path.relative_to(ARCHIVE))
        for base in (ARCHIVE / "artifacts", ARCHIVE / "reconstructed")
        if base.exists()
        for path in base.rglob("*") if path.is_file()
    }
    checks.append(check(
        not duplicate_outputs and actual_files == expected_files,
        "Orphan artifacts",
        f"expected={len(expected_files)}, actual={len(actual_files)}, "
        f"missing={len(expected_files - actual_files)}, orphan={len(actual_files - expected_files)}, "
        f"duplicate output references={len(artifacts) - len(expected_files)}",
    ))

    empty = []
    bad_hash = []
    missing_hash = []
    for item in artifacts:
        value = item.get("integrity", {}).get("sha256")
        if not value:
            missing_hash.append(item["artifact_id"])
            continue
        data = (ARCHIVE / item["output_file"]).read_bytes()
        if not data:
            empty.append(item["artifact_id"])
        if digest(data) != value:
            bad_hash.append(item["artifact_id"])
    checks.append(check(
        not missing_hash and not bad_hash, "Hash coverage",
        f"{len(artifacts) - len(missing_hash) - len(bad_hash)}/{len(artifacts)} files have present, matching SHA-256",
    ))
    checks.append(check(not empty, "Empty artifacts", f"{len(empty)} empty artifact files"))

    missing_provenance = []
    bad_chronology = []
    for item in artifacts:
        source = item.get("source", {})
        required = (source.get("document"), source.get("revision"), source.get("position"), source.get("extraction_method"))
        if not all(required):
            missing_provenance.append(item["artifact_id"])
        history = item.get("history", {})
        if history.get("version_status") not in {
            "EXPLICIT", "INFERRED_FROM_HEADING", "INFERRED_FROM_CONTEXT", "UNKNOWN"
        } or not history.get("chronology"):
            bad_chronology.append(item["artifact_id"])
    checks.append(check(
        not missing_provenance, "Provenance coverage",
        f"{len(artifacts) - len(missing_provenance)}/{len(artifacts)} artifacts have document, revision, position, and method",
    ))
    checks.append(check(
        not bad_chronology, "Chronology coverage",
        f"{len(artifacts) - len(bad_chronology)}/{len(artifacts)} artifacts have known/inferred/unknown chronology labels",
    ))

    raw_by_revision = {}
    bad_raw = []
    for revision in revisions:
        raw = (ARCHIVE / revision["raw_file"]).read_bytes()
        raw_by_revision[revision["revision"]] = raw
        if digest(raw) != revision["integrity"]["sha256"]:
            bad_raw.append(revision["revision"])
    checks.append(check(
        not bad_raw, "Raw revision integrity",
        f"{len(revisions) - len(bad_raw)}/{len(revisions)} raw Git-blob copies match recorded SHA-256",
    ))
    attributes_path = ARCHIVE / ".gitattributes"
    attributes_text = attributes_path.read_text(encoding="utf-8") if attributes_path.exists() else ""
    required_attributes = {"raw/** -text", "artifacts/** -text", "reconstructed/** -text"}
    checks.append(check(
        required_attributes <= set(attributes_text.splitlines()),
        "Git byte-preservation attributes",
        "raw, extracted, and reconstructed payload trees are marked -text",
    ))

    source_mismatch = []
    reconstructed_bad = []
    for item in artifacts:
        output = (ARCHIVE / item["output_file"]).read_bytes()
        if item.get("derived"):
            reconstruction = item.get("reconstruction", {})
            if (item.get("artifact_type") != "reconstructed"
                    or reconstruction.get("semantic_inference") is not False
                    or reconstruction.get("authoritative") is not False
                    or not reconstruction.get("source_artifacts")):
                reconstructed_bad.append(item["artifact_id"])
            continue
        source = item["source"]
        blob = raw_by_revision.get(source["revision"])
        start, end = source.get("byte_start"), source.get("byte_end_exclusive")
        if blob is None or start is None or end is None or blob[start:end] != output:
            source_mismatch.append(item["artifact_id"])
    original_count = sum(not item.get("derived") for item in artifacts)
    checks.append(check(
        not source_mismatch, "Semantic preservation",
        f"{original_count - len(source_mismatch)}/{original_count} original files equal their pinned source byte ranges",
    ))
    reconstructed_count = sum(bool(item.get("derived")) for item in artifacts)
    checks.append(check(
        not reconstructed_bad, "Reconstruction labeling",
        f"{reconstructed_count - len(reconstructed_bad)}/{reconstructed_count} reconstructed files are explicit, non-authoritative, and inference-free",
    ))

    detection_ids = [x["detection_id"] for x in detections]
    represented = [
        x["source"]["detection_id"] for x in artifacts
        if not x.get("derived")
        and x["source"].get("detection_id")
        and not x["source"]["detection_id"].startswith("component-")
    ]
    detection_counts = Counter(detection_ids)
    represented_counts = Counter(represented)
    checks.append(check(
        detection_counts == represented_counts, "Source coverage",
        f"{len(represented)}/{len(detection_ids)} detected fences/outside userscripts/inline regions represented exactly once",
    ))

    relation_refs = [
        relation for relation in lineage["relationships"]
        if relation.get("from") not in id_set or relation.get("to") not in id_set
    ]
    node_ids = {x["artifact_id"] for x in lineage["nodes"]}
    checks.append(check(
        not relation_refs and node_ids == id_set, "Lineage consistency",
        f"nodes={len(node_ids)}, relationships={len(lineage['relationships'])}, "
        f"broken references={len(relation_refs)}, node delta={len(node_ids ^ id_set)}",
    ))

    grouped = defaultdict(list)
    by_id = {x["artifact_id"]: x for x in artifacts}
    for item in artifacts:
        if not item.get("derived"):
            grouped[item["integrity"]["sha256"]].append(item["artifact_id"])
    expected_duplicate_sets = {
        digest_value: set(members)
        for digest_value, members in grouped.items() if len(members) > 1
    }
    recorded_duplicate_sets = {
        group["sha256"]: set(group["identical_artifacts"])
        for group in duplicates
    }
    duplicate_canonical_bad = [
        group["id"] for group in duplicates
        if group["canonical_artifact"] not in group["identical_artifacts"]
        or any(by_id[x]["integrity"]["sha256"] != group["sha256"] for x in group["identical_artifacts"])
    ]
    checks.append(check(
        expected_duplicate_sets == recorded_duplicate_sets and not duplicate_canonical_bad,
        "Duplicate consistency",
        f"expected groups={len(expected_duplicate_sets)}, recorded={len(recorded_duplicate_sets)}, "
        f"bad canonical/hash groups={len(duplicate_canonical_bad)}",
    ))

    sidecar_fields_missing = []
    for item in artifacts:
        if not all(key in item for key in (
            "artifact_id", "artifact_type", "language", "classification", "status",
            "source_document", "source_revision", "source_heading", "source_position",
            "sha256", "provenance", "source", "history", "integrity", "context",
            "relationships", "output_file",
        )):
            sidecar_fields_missing.append(item["artifact_id"])
    checks.append(check(
        not sidecar_fields_missing, "Metadata sidecars",
        f"{len(artifacts) - len(sidecar_fields_missing)}/{len(artifacts)} consolidated sidecar records contain required layers",
    ))

    source_map = (ARCHIVE / "SOURCE-MAP.md").read_text(encoding="utf-8")
    unmapped = [item["artifact_id"] for item in artifacts if item["artifact_id"] not in source_map]
    checks.append(check(
        not unmapped, "Source map coverage",
        f"{len(artifacts) - len(unmapped)}/{len(artifacts)} artifact identifiers occur in SOURCE-MAP.md",
    ))

    overall = "FAIL" if any(x["result"] == "FAIL" for x in checks) else (
        "WARN" if any(x["result"] == "WARN" for x in checks) else "PASS"
    )
    result = {
        "schema_version": 1,
        "overall": overall,
        "checks": checks,
        "counts": {
            "artifacts": len(artifacts),
            "manifest_entries": len(artifacts),
            "index_entries": len(index),
            "detections": len(detections),
            "raw_revisions": len(revisions),
            "duplicate_groups": len(duplicates),
            "lineage_nodes": len(lineage["nodes"]),
            "relationships": len(lineage["relationships"]),
            "reconstructed": reconstructed_count,
        },
    }
    serialized = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    (ARCHIVE / "VALIDATION.yaml").write_text(
        serialized, encoding="utf-8", newline="\n"
    )
    print(serialized, end="")
    return 0 if overall != "FAIL" else 1


if __name__ == "__main__":
    sys.exit(main())
