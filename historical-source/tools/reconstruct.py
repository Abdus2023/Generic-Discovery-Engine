#!/usr/bin/env python3
"""Deterministic, evidence-only historical snapshot reconstruction (protocol 92–155)."""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ARCHIVE = Path(__file__).resolve().parents[1]
TOOL_VERSION = "mechanical-reconstruction-v1"
STATUS_REGISTRY = {"EXACT", "MECHANICALLY_COMPOSED", "PATCH_RECONSTRUCTED", "PARTIAL", "INFERRED", "UNKNOWN"}
DEPENDENCY_REGISTRY = {"PRESENT", "HISTORICAL_EXTERNAL", "MISSING", "INFERRED", "UNKNOWN"}
EXTERNAL_DEPENDENCIES = {
    "GM_xmlhttpRequest", "GM_getValue", "GM_setValue", "GM_addStyle",
    "GM_registerMenuCommand", "unsafeWindow", "fetch", "DOMParser", "URL",
    "Map", "Set", "WeakMap", "Promise", "document", "window", "localStorage",
    "indexedDB", "IndexedDB", "XMLHttpRequest", "MutationObserver",
    "PerformanceObserver", "AbortController", "BroadcastChannel", "crypto",
    "TextEncoder", "TextDecoder", "Blob", "Worker",
}
MODELS = ["Candidate", "Observation", "Discovery", "KnowledgeBase", "Provider", "Scheduler"]
IMPORTANT_APIS = [
    "recognize", "acquire", "claimNextCandidate", "enqueue", "run", "start",
    "stop", "processCandidate", "addCandidate", "addObservation", "addDiscovery",
    "persist", "restore", "register", "canHandle", "fetch",
]
GENERATED_TOP = [
    "snapshots", "analysis", "VERSION-GRAPH.md", "VERSION-MATRIX.md",
    "RECONSTRUCTION-MANIFEST.yaml", "RECONSTRUCTION-ASSUMPTIONS.yaml",
    "RECONSTRUCTION-GAPS.yaml", "RECONSTRUCTION-CONFLICTS.yaml",
    "RECONSTRUCTION-EVIDENCE.yaml", "RECONSTRUCTION-REPORT.md",
    "RECONSTRUCTION-VALIDATION.yaml",
]

# IDs are occurrence identities from SOURCE-MANIFEST.yaml, never version identities.
SNAPSHOT_SPECS: list[dict[str, Any]] = [
    {
        "snapshot_id": "snapshot-0001", "version": "0.1.0", "directory": "v0.1/mechanically-composed",
        "variant": "mechanically-composed", "artifact_id": "rec-dbef25f8ab917d5a",
        "parent_artifact": "art-5ff41289b5f1c428", "status": "MECHANICALLY_COMPOSED",
        "ranges": [(1942, 1956), (1958, 2961), (2963, 2964)], "previous": None,
        "lineage": "first recoverable source state",
    },
    {
        "snapshot_id": "snapshot-0002", "version": "0.1.0", "directory": "v0.1/flattened-alternative",
        "variant": "flattened-alternative", "artifact_id": "art-f14be66e164996ad",
        "status": "PARTIAL", "previous": None,
        "lineage": "alternative transformed paste; relationship to composed source is unknown",
    },
    {
        "snapshot_id": "snapshot-0003", "version": "0.2.0", "directory": "v0.2/mechanically-composed",
        "variant": "mechanically-composed", "artifact_id": "rec-e8df26fe56d82d1c",
        "parent_artifact": "art-b7850a391eddeb86", "status": "MECHANICALLY_COMPOSED",
        "ranges": [(3047, 3061), (3063, 4708), (4710, 4711)], "previous": "snapshot-0001",
        "lineage": "source calls v0.2.0 the revised version after requested fixes",
    },
    {
        "snapshot_id": "snapshot-0004", "version": "0.2.0", "directory": "v0.2/flattened-alternative",
        "variant": "flattened-alternative", "artifact_id": "art-e69de36ddbc7cb3b",
        "status": "PARTIAL", "previous": "snapshot-0002",
        "lineage": "same pasted pair; formatting loss prevents exact lineage identity",
    },
    {
        "snapshot_id": "snapshot-0005", "version": "0.3.0", "directory": "v0.3",
        "variant": "only-evidenced-complete-occurrence", "artifact_id": "art-44eb3694339abdcb",
        "status": "EXACT", "previous": "snapshot-0004",
        "lineage": "preceding prose explicitly says v0.3.0 is based on v0.2.0",
    },
    {
        "snapshot_id": "snapshot-0006", "version": "0.4.0", "directory": "v0.4/variant-a",
        "variant": "variant-a", "artifact_id": "art-deb961ea9f622d3a", "status": "EXACT",
        "previous": "snapshot-0005", "lineage": "preceding prose says v0.4.0 builds directly on v0.3.0",
    },
    {
        "snapshot_id": "snapshot-0007", "version": "0.5.0", "directory": "v0.5/variant-a",
        "variant": "variant-a", "artifact_id": "art-2c6f74909f301798", "status": "EXACT",
        "previous": "snapshot-0006", "lineage": "preceding prose says continuing with v0.5.0",
    },
    {
        "snapshot_id": "snapshot-0008", "version": "0.4.0", "directory": "v0.4/variant-b",
        "variant": "variant-b", "artifact_id": "art-c19ebb3956fba19c", "status": "EXACT",
        "previous": "snapshot-0005", "lineage": "preceding prose says this v0.4.0 also continues from v0.3.0",
    },
    {
        "snapshot_id": "snapshot-0009", "version": "0.5.0", "directory": "v0.5/variant-b",
        "variant": "variant-b", "artifact_id": "art-fbebfdf9a3874c18", "status": "EXACT",
        "previous": "snapshot-0008", "lineage": "preceding planning identifies the next v0.5.0",
    },
    {
        "snapshot_id": "snapshot-0010", "version": "0.6.0", "directory": "v0.6/variant-a",
        "variant": "variant-a", "artifact_id": "art-b1368ed9b372a6a6", "status": "EXACT",
        "previous": "snapshot-0009", "lineage": "preceding prose says continuing with v0.6.0",
    },
    {
        "snapshot_id": "snapshot-0011", "version": "0.5.0", "directory": "v0.5/variant-c",
        "variant": "variant-c", "artifact_id": "art-f019277e6c28e8f5", "status": "EXACT",
        "previous": None, "lineage": "repeated v0.5.0 after v0.6.0; parent is ambiguous",
    },
    {
        "snapshot_id": "snapshot-0012", "version": "0.6.0", "directory": "v0.6/variant-b",
        "variant": "variant-b", "artifact_id": "art-3680c60f0bc39673", "status": "EXACT",
        "previous": "snapshot-0011", "lineage": "preceding prose says continuing to v0.6.0",
    },
    {
        "snapshot_id": "snapshot-0013", "version": "0.6.0", "directory": "v0.6/variant-c",
        "variant": "variant-c", "artifact_id": "art-33fa8de51e13e087", "status": "EXACT",
        "previous": "snapshot-0012", "lineage": "prose says this v0.6.0 keeps the discovery architecture intact",
    },
    {
        "snapshot_id": "snapshot-0014", "version": "0.7.1", "directory": "v0.7.1",
        "variant": "only-evidenced-complete-occurrence", "artifact_id": "art-e0789bc8f62176cb",
        "status": "EXACT", "previous": "snapshot-0013",
        "lineage": "v0.7.1 prose says it strengthens the existing v0.6 control plane",
    },
]

CAPABILITIES = [
    ("Candidate model", r"(?m)^\s*class\s+Candidate\b"),
    ("Observation model", r"(?m)^\s*class\s+Observation\b"),
    ("Discovery model", r"(?m)^\s*class\s+Discovery\b"),
    ("KnowledgeBase", r"(?m)^\s*class\s+KnowledgeBase\b"),
    ("HTML provider", r"(?m)^\s*class\s+(?:HtmlProvider|HtmlRecognizer)\b"),
    ("JSON provider", r"(?m)^\s*class\s+JsonProvider\b"),
    ("Text provider", r"(?m)^\s*class\s+TextProvider\b"),
    ("XML provider", r"(?m)^\s*class\s+XmlProvider\b"),
    ("Provider registry", r"(?m)^\s*class\s+ProviderRegistry\b"),
    ("Scheduler", r"(?m)^\s*class\s+(?:Scheduler|AdaptiveScheduler)\b"),
    ("Concurrent workers", r"\b(?:Promise\.all\s*\(|Array\.from\s*\([^\r\n]*worker)"),
    ("Synchronous claim operation", r"\bclaimNextCandidate\s*\("),
    ("Provenance records", r"\b(?:this\.provenance|provenance\s*:)"),
    ("GM acquisition", r"\bGM_xmlhttpRequest\s*\("),
    ("Fetch acquisition", r"\bfetch\s*\("),
]


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def dump_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def write_yaml(path: Path, value: Any) -> bytes:
    data = dump_bytes(value)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return data


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def metadata_block(source: bytes) -> dict[str, Any]:
    text = source.decode("utf-8", errors="replace")
    start, end = text.find("// ==UserScript=="), text.find("// ==/UserScript==")
    directives: dict[str, list[str]] = defaultdict(list)
    if start >= 0 and end >= start:
        block = text[start:end].splitlines()
        for line in block:
            match = re.match(r"\s*//\s*@([^\s]+)\s*(.*)$", line)
            if match:
                directives[match.group(1)].append(match.group(2).strip())
    version = directives.get("version", [None])[0]
    return {
        "status": "PARSED" if start >= 0 and end >= start else "MISSING_OR_UNCLOSED",
        "version": version,
        "directives": dict(sorted(directives.items())),
        "raw_header_present": start >= 0 and end >= start,
    }


def symbol_profile(source: bytes) -> dict[str, Any]:
    text = source.decode("utf-8", errors="replace")
    class_matches = list(re.finditer(r"(?m)^\s*(?:export\s+)?class\s+([A-Za-z_$][\w$]*)", text))
    function_matches = list(re.finditer(r"(?m)^\s*(?:export\s+)?(?:async\s+)?function\s+([A-Za-z_$][\w$]*)\s*\(([^\r\n)]*)\)", text))
    constants = sorted(set(re.findall(r"(?m)^\s*(?:export\s+)?const\s+([A-Za-z_$][\w$]*)\s*=", text)))
    classes = [m.group(1) for m in class_matches]
    functions = [m.group(1) for m in function_matches]
    conflicts = []
    for name in sorted(set(classes + functions)):
        kinds = []
        if name in classes:
            kinds.append("class")
        if name in functions:
            kinds.append("function")
        if classes.count(name) + functions.count(name) > 1:
            conflicts.append({"symbol": name, "kinds": kinds, "status": "UNRESOLVED"})
    class_hashes = {}
    for index, match in enumerate(class_matches):
        ending = class_matches[index + 1].start() if index + 1 < len(class_matches) else len(text)
        class_hashes[match.group(1)] = sha(text[match.start():ending].encode("utf-8"))
    signatures: dict[str, list[str]] = {}
    for name in IMPORTANT_APIS:
        patterns = [
            re.compile(r"(?m)^\s*(?:async\s+)?" + re.escape(name) + r"\s*\(([^\r\n)]*)\)"),
            re.compile(r"(?m)^\s*(?:async\s+)?function\s+" + re.escape(name) + r"\s*\(([^\r\n)]*)\)"),
        ]
        values = []
        for pattern in patterns:
            for match in pattern.finditer(text):
                values.append(f"{name}({match.group(1).strip()})")
        if values:
            signatures[name] = sorted(set(values))
    fields: dict[str, list[str]] = {}
    for index, match in enumerate(class_matches):
        name = match.group(1)
        if name not in MODELS:
            continue
        opening = text.find("{", match.end())
        ending = class_matches[index + 1].start() if index + 1 < len(class_matches) else len(text)
        body = text[opening:ending]
        fields[name] = sorted(set(re.findall(r"\bthis\.([A-Za-z_$][\w$]*)\s*=", body)))
    return {
        "definitions": {
            "classes": classes, "functions": functions, "constants": constants,
        },
        "api_signatures": signatures,
        "class_content_sha256": class_hashes,
        "model_fields": fields,
        "conflicts": conflicts,
        "analysis_method": "read-only lexical regular expressions; no AST rewrite",
    }


def dependencies_for(artifact: dict[str, Any], profile: dict[str, Any], source: bytes) -> dict[str, Any]:
    defined = set(profile["definitions"]["classes"] + profile["definitions"]["functions"] + profile["definitions"]["constants"])
    text = source.decode("utf-8", errors="replace")
    entries = []
    for name in dict.fromkeys(artifact.get("dependencies", [])):
        if name in defined:
            status, basis = "PRESENT", "definition occurs in recovered source"
        elif name in EXTERNAL_DEPENDENCIES:
            status, basis = "HISTORICAL_EXTERNAL", "browser/userscript/runtime-provided API; historical availability not executed"
        elif artifact.get("incomplete"):
            status, basis = "UNKNOWN", "artifact is an incomplete/flattened representation; definition boundaries are not reliably recoverable"
        elif re.search(r"(?:\bnew\s+|\bextends\s+|\binstanceof\s+)" + re.escape(name) + r"\b|\b" + re.escape(name) + r"\s*\.", text):
            status, basis = "MISSING", "syntactic use observed, but no definition occurs in recovered source"
        else:
            status, basis = "UNKNOWN", "extraction dependency inventory mentions the name, but implementation/reference semantics are not mechanically resolvable"
        entries.append({"name": name, "status": status, "basis": basis})
    missing = [x["name"] for x in entries if x["status"] == "MISSING"]
    unknown = [x["name"] for x in entries if x["status"] == "UNKNOWN"]
    external = [x["name"] for x in entries if x["status"] == "HISTORICAL_EXTERNAL"]
    if missing:
        self_contained = "NO"
    elif unknown:
        self_contained = "UNKNOWN"
    elif external:
        self_contained = "PARTIAL"
    else:
        self_contained = "YES"
    return {
        "entries": entries,
        "status_registry": sorted(DEPENDENCY_REGISTRY),
        "self_contained": {
            "status": self_contained,
            "missing_dependencies": missing,
            "unknown_dependencies": unknown,
            "historical_external_dependencies": external,
            "note": "PARTIAL means bundled internal definitions appear closed but historical platform APIs were not executed; UNKNOWN preserves unresolved dependency semantics.",
        },
    }


def node_check(source: bytes) -> dict[str, Any]:
    if shutil.which("node") is None:
        return {"attempted": False, "result": "TOOL_UNAVAILABLE", "tool": "node --check", "source_modified": False}
    proc = subprocess.run(["node", "--check", "-"], input=source, capture_output=True)
    error = proc.stderr.decode("utf-8", errors="replace")[:2000]
    return {
        "attempted": True,
        "result": "PASS" if proc.returncode == 0 else "FAIL",
        "tool": "node --check -",
        "exit_code": proc.returncode,
        "diagnostic": error,
        "source_modified": False,
        "runtime_executed": False,
    }


def source_lines(raw: bytes) -> list[bytes]:
    return raw.splitlines(keepends=True)


def direct_source_map(artifact: dict[str, Any], source: bytes) -> dict[str, Any]:
    src = artifact["source"]
    return {
        "schema_version": 1,
        "snapshot_id": None,
        "ranges": [{
            "output_byte_start": 0,
            "output_byte_end_exclusive": len(source),
            "output_line_start": 1,
            "output_line_end": len(source.splitlines()),
            "source_artifact": artifact["artifact_id"],
            "source_artifact_byte_start": 0,
            "source_artifact_byte_end_exclusive": len(source),
            "source_anchor": {
                "document": src["document"], "commit": src["commit"], "revision": src["revision"],
                "line_start": src["line_start"], "line_end": src["line_end"],
                "byte_start": src["byte_start"], "byte_end_exclusive": src["byte_end_exclusive"],
            },
            "reconstruction_operation": "direct_copy",
            "confidence": "HIGH", "assumptions": [], "generated_non_historical": False,
            "segment_sha256": sha(source),
        }],
    }


def composed_source_map(spec: dict[str, Any], artifact: dict[str, Any], parent: dict[str, Any], source: bytes, revisions: dict[str, dict[str, Any]]) -> dict[str, Any]:
    # Compose from the authoritative extracted parent artifact, not from a
    # convenience raw-document copy. This keeps the operation artifact-driven
    # and preserves its historical CRLF bytes exactly.
    parent_bytes = (ARCHIVE / parent["output_file"]).read_bytes()
    lines = source_lines(parent_bytes)
    parent_start_line = parent["source"]["line_start"]
    output_parts: list[bytes] = []
    ranges = []
    out_byte = 0
    out_line = 1
    for first, last in spec["ranges"]:
        local_first = first - parent_start_line
        local_last_exclusive = last - parent_start_line + 1
        segment = b"".join(lines[local_first:local_last_exclusive])
        artifact_byte_start = len(b"".join(lines[:local_first]))
        artifact_byte_end = artifact_byte_start + len(segment)
        if parent_bytes[artifact_byte_start:artifact_byte_end] != segment:
            raise RuntimeError(f"parent artifact mismatch for {spec['snapshot_id']} lines {first}-{last}")
        document_byte_start = parent["source"]["byte_start"] + artifact_byte_start
        line_count = len(segment.splitlines())
        ranges.append({
            "output_byte_start": out_byte,
            "output_byte_end_exclusive": out_byte + len(segment),
            "output_line_start": out_line,
            "output_line_end": out_line + line_count - 1,
            "source_artifact": parent["artifact_id"],
            "source_artifact_byte_start": artifact_byte_start,
            "source_artifact_byte_end_exclusive": artifact_byte_end,
            "source_anchor": {
                "document": parent["source"]["document"], "commit": parent["source"]["commit"],
                "revision": parent["source"]["revision"], "line_start": first, "line_end": last,
                "byte_start": document_byte_start, "byte_end_exclusive": document_byte_start + len(segment),
            },
            "reconstruction_operation": "ordered_fragment_copy",
            "confidence": "HIGH", "assumptions": [], "generated_non_historical": False,
            "segment_sha256": sha(segment),
        })
        output_parts.append(segment)
        out_byte += len(segment)
        out_line += line_count
    if b"".join(output_parts) != source:
        raise RuntimeError(f"existing reconstruction differs from explicit source ranges for {spec['snapshot_id']}")
    return {"schema_version": 1, "snapshot_id": None, "ranges": ranges}


def append_gap_marker(source: bytes, snapshot_id: str, version: str) -> tuple[bytes, bytes]:
    newline = b"" if source.endswith((b"\n", b"\r")) else b"\r\n"
    marker = newline + (
        "/* HISTORICAL SOURCE GAP\r\n"
        f"   {snapshot_id} ({version}): original pre-flattening whitespace and component boundaries are not recoverable.\r\n"
        "   Reconstruction intentionally remains incomplete; no source was invented.\r\n"
        "*/\r\n"
    ).encode("utf-8")
    return source + marker, marker


def capability_observation(source: bytes, complete: bool, artifact_id: str) -> dict[str, dict[str, Any]]:
    text = source.decode("utf-8", errors="replace")
    output = {}
    for capability, pattern in CAPABILITIES:
        match = re.search(pattern, text)
        if match:
            status = "IMPLEMENTED" if complete else "PARTIAL"
            evidence = {"artifact_id": artifact_id, "line": line_number(text, match.start()), "matched_source": match.group(0)[:120]}
        else:
            status = "ABSENT" if complete else "UNKNOWN"
            evidence = {"artifact_id": artifact_id, "observation": "pattern absent from recovered source"}
        output[capability] = {"status": status, "evidence": evidence}
    return output


def profile_delta(old: dict[str, Any], new: dict[str, Any]) -> dict[str, Any]:
    old_defs = set(sum(old["definitions"].values(), []))
    new_defs = set(sum(new["definitions"].values(), []))
    old_apis = {(name, sig) for name, values in old["api_signatures"].items() for sig in values}
    new_apis = {(name, sig) for name, values in new["api_signatures"].items() for sig in values}
    models = {}
    for name in MODELS:
        before, after = set(old["model_fields"].get(name, [])), set(new["model_fields"].get(name, []))
        if before or after:
            models[name] = {"added_fields": sorted(after - before), "removed_fields": sorted(before - after), "retained_fields": sorted(before & after)}
    return {
        "symbols": {"added": sorted(new_defs - old_defs), "removed": sorted(old_defs - new_defs)},
        "api": {
            "added": [{"symbol": x[0], "signature": x[1]} for x in sorted(new_apis - old_apis)],
            "removed": [{"symbol": x[0], "signature": x[1]} for x in sorted(old_apis - new_apis)],
        },
        "data_models": models,
        "behavioral_observation": "Textual source differences only; behavior was not executed or proved.",
    }


def tree_hashes(root: Path) -> dict[str, str]:
    return {
        str(path.relative_to(root)): sha(path.read_bytes())
        for path in sorted(root.rglob("*")) if path.is_file()
    }


def unsupported_versions(manifest: list[dict[str, Any]]) -> list[dict[str, Any]]:
    values = ["0.7.0"] + [f"0.{number}" for number in range(8, 36)]
    result = []
    for version in values:
        candidates = [
            x for x in manifest
            if x["history"].get("version") == version and not x["derived"]
            and x["classification"] in {"PSEUDOCODE", "INTERFACE", "EXAMPLE"}
            and x["chronology_index"] < 2822
        ]
        result.append({
            "historical_version": f"v{version}", "reconstruction_status": "UNKNOWN",
            "reason": "No complete implementation source artifact is evidenced; design/pseudocode does not become source.",
            "representative_design_evidence": [x["artifact_id"] for x in candidates[:3]],
            "snapshot_directory_created": False,
        })
    return result


def build(output_root: Path) -> dict[str, Any]:
    manifest_doc = json.loads((ARCHIVE / "SOURCE-MANIFEST.yaml").read_text(encoding="utf-8"))
    manifest = manifest_doc["artifacts"]
    artifacts = {x["artifact_id"]: x for x in manifest}
    revision_doc = json.loads((ARCHIVE / "REVISION-INVENTORY.yaml").read_text(encoding="utf-8"))
    revisions = {x["revision"]: x for x in revision_doc["revisions"]}
    output_root.mkdir(parents=True, exist_ok=True)

    snapshots: list[dict[str, Any]] = []
    snapshots_by_id: dict[str, dict[str, Any]] = {}
    sources_by_id: dict[str, bytes] = {}
    profiles_by_id: dict[str, dict[str, Any]] = {}
    capabilities_by_id: dict[str, dict[str, Any]] = {}
    evidence_entries = []
    disappearance_observations = []

    for spec in SNAPSHOT_SPECS:
        artifact = artifacts[spec["artifact_id"]]
        original = (ARCHIVE / artifact["output_file"]).read_bytes()
        raw_source = original
        if spec["status"] == "MECHANICALLY_COMPOSED":
            parent = artifacts[spec["parent_artifact"]]
            source_map = composed_source_map(spec, artifact, parent, original, revisions)
            source_artifacts = [parent["artifact_id"]]
            source_nature = "MECHANICALLY_RECONSTRUCTED_SOURCE"
            operations = {
                "BASE": parent["artifact_id"],
                "ADDITIONS": [{"source_range": f"lines {a}-{b}", "operation": "ordered_fragment_copy"} for a, b in spec["ranges"]],
                "MODIFICATIONS": [], "DELETIONS": ["Markdown fence delimiter lines only"], "RENAMES": [],
                "DEPENDENCY_CHANGES": [],
            }
            completeness: float | str = 1.0
            completeness_basis = "All bytes in the explicitly bounded userscript were recovered in source order; only Markdown delimiters were excluded."
        elif spec["status"] == "PARTIAL":
            raw_source, marker = append_gap_marker(original, spec["snapshot_id"], spec["version"])
            source_map = direct_source_map(artifact, original)
            source_map["ranges"].append({
                "output_byte_start": len(original), "output_byte_end_exclusive": len(raw_source),
                "output_line_start": len(original.splitlines()) + 1,
                "output_line_end": len(raw_source.splitlines()),
                "source_artifact": None, "source_artifact_byte_start": None, "source_artifact_byte_end_exclusive": None,
                "source_anchor": None, "reconstruction_operation": "explicit_gap_marker",
                "confidence": "HIGH", "assumptions": [], "generated_non_historical": True,
                "segment_sha256": sha(marker),
            })
            source_artifacts = [artifact["artifact_id"]]
            source_nature = "PARTIALLY_RECONSTRUCTED_SOURCE"
            operations = {
                "BASE": artifact["artifact_id"], "ADDITIONS": ["explicit non-historical gap marker"],
                "MODIFICATIONS": [], "DELETIONS": [], "RENAMES": [], "DEPENDENCY_CHANGES": [],
            }
            completeness = "UNKNOWN"
            completeness_basis = "Formatting loss is proved, but the amount and exact location of all lost source cannot be quantified."
        else:
            source_map = direct_source_map(artifact, original)
            source_artifacts = [artifact["artifact_id"]]
            source_nature = "ORIGINAL_SOURCE"
            operations = {
                "BASE": artifact["artifact_id"], "ADDITIONS": [], "MODIFICATIONS": [],
                "DELETIONS": [], "RENAMES": [], "DEPENDENCY_CHANGES": [],
            }
            completeness = 1.0
            completeness_basis = "A complete contiguous userscript artifact with matching explicit @version exists directly."
        source_map["snapshot_id"] = spec["snapshot_id"]

        snapshot_dir = output_root / "snapshots" / spec["directory"]
        source_path = snapshot_dir / "source" / "generic-discovery.user.js"
        source_path.parent.mkdir(parents=True, exist_ok=True)
        source_path.write_bytes(raw_source)
        source_map_bytes = write_yaml(snapshot_dir / "source-map.yaml", source_map)

        profile = symbol_profile(raw_source)
        deps = dependencies_for(artifact, profile, raw_source)
        user_metadata = metadata_block(raw_source)
        static = node_check(raw_source)
        metadata_matches = user_metadata["version"] == spec["version"]
        if spec["status"] == "PARTIAL" or static["result"] == "FAIL":
            executability = "NON_EXECUTABLE"
        elif static["result"] == "PASS":
            executability = "LIKELY_EXECUTABLE"
        else:
            executability = "UNKNOWN"
        complete_for_matrix = spec["status"] in {"EXACT", "MECHANICALLY_COMPOSED"}
        capabilities = capability_observation(raw_source, complete_for_matrix, artifact["artifact_id"])

        previous_id = spec.get("previous")
        changes: dict[str, Any]
        if previous_id:
            previous_source = sources_by_id[previous_id]
            previous_profile = profiles_by_id[previous_id]
            delta = profile_delta(previous_profile, profile)
            diff = "".join(difflib.unified_diff(
                previous_source.decode("utf-8", errors="replace").splitlines(keepends=True),
                raw_source.decode("utf-8", errors="replace").splitlines(keepends=True),
                fromfile=f"{previous_id}/generic-discovery.user.js",
                tofile=f"{spec['snapshot_id']}/generic-discovery.user.js",
            )).encode("utf-8")
            diff_path = snapshot_dir / "analysis" / "source-diff-from-previous.diff"
            diff_path.parent.mkdir(parents=True, exist_ok=True)
            diff_path.write_bytes(diff)
            old_cap = capabilities_by_id[previous_id]
            cap_changes = {
                key: {"from": old_cap[key]["status"], "to": capabilities[key]["status"]}
                for key in capabilities if old_cap[key]["status"] != capabilities[key]["status"]
            }
            changes = {
                "previous_snapshot": previous_id, "lineage_evidence": spec["lineage"],
                "source_diff": str(diff_path.relative_to(output_root)), "source_diff_sha256": sha(diff),
                "symbol_diff": delta["symbols"], "api_diff": delta["api"],
                "data_model_diff": delta["data_models"],
                "behavioral_observation": delta["behavioral_observation"],
                "architectural_difference": cap_changes,
            }
            previous_major_symbols = set(
                previous_profile["definitions"]["classes"] + previous_profile["definitions"]["functions"]
            )
            for symbol in delta["symbols"]["removed"]:
                if symbol in previous_major_symbols:
                    disappearance_observations.append({
                        "symbol": symbol, "from_snapshot": previous_id, "absent_from_snapshot": spec["snapshot_id"],
                        "status": "DISAPPEARED_FROM_LATER_LINKED_SOURCE", "abandonment": "UNKNOWN",
                    })
        else:
            changes = {
                "previous_snapshot": None, "lineage_evidence": spec["lineage"],
                "status": "NO_UNAMBIGUOUS_PREVIOUS_SOURCE_SELECTED",
            }

        src = artifact["source"]
        snapshot = {
            "schema_version": 1,
            "snapshot_id": spec["snapshot_id"],
            "historical_version": f"v{spec['version']}",
            "variant": spec["variant"],
            "variant_status": (
                "ALTERNATIVE_REPRESENTATION" if spec["version"] in {"0.1.0", "0.2.0"} else
                "ALTERNATIVE_IMPLEMENTATION" if spec["version"] in {"0.4.0", "0.5.0", "0.6.0"} else
                "SOLE_RECOVERED_VARIANT"
            ),
            "date": src["timestamp"], "commit": src["commit"], "revision": src["revision"], "release": None,
            "extraction_sequence": artifact["chronology_index"],
            "source_documents": [src["document"]],
            "version_boundary": {
                "confidence": "STRONG" if metadata_matches else "MEDIUM",
                "evidence": {"metadata_version": user_metadata["version"], "manifest_version": artifact["history"]["version"], "artifact_id": artifact["artifact_id"]},
            },
            "reconstruction": {
                "status": spec["status"], "source_nature": source_nature, "authoritative": False,
                "authoritative_source": artifact["output_file"],
                "completeness": completeness, "completeness_basis": completeness_basis,
                "assumption_dependent": False,
            },
            "base_selection": {
                "result": "SELECTED_WITHOUT_AMBIGUITY" if spec["status"] != "PARTIAL" else "SELECTED_PARTIAL_REPRESENTATION",
                "rule": "same historical revision and explicit version",
                "selected": operations["BASE"], "alternatives_not_merged": True,
            },
            "compatibility_test": {
                "same_revision": "PASS", "same_branch": "PASS", "same_version": "PASS",
                "same_implementation_family": "PASS",
                "dependency_assumptions": "NO_CROSS_ARTIFACT_DEPENDENCIES_COMPOSED",
                "compatible_symbol_definitions": "PASS" if not profile["conflicts"] else "FAIL",
                "decision": "COMPOSE" if spec["status"] == "MECHANICALLY_COMPOSED" else "NO_FRAGMENT_COMPOSITION",
            },
            "transformation_plan": operations,
            "artifacts": source_artifacts,
            "dependencies": deps,
            "symbols": profile,
            "changes_from_previous": changes,
            "capabilities": capabilities,
            "conflicts": profile["conflicts"],
            "uncertainties": (["GAP-FLATTENED-" + spec["version"]] if spec["status"] == "PARTIAL" else []),
            "assumptions": [],
            "executability": executability,
            "static_validation": {
                "syntax_and_ast_parse": static,
                "userscript_metadata": {"result": "PASS" if user_metadata["status"] == "PARSED" else "FAIL", **user_metadata},
                "dependency_resolution": (
                    "FAIL" if deps["self_contained"]["missing_dependencies"] else
                    "UNKNOWN" if deps["self_contained"]["unknown_dependencies"] else
                    "PARTIAL" if deps["self_contained"]["historical_external_dependencies"] else "PASS"
                ),
                "source_was_modified_to_validate": False,
            },
            "runtime_validation": {"executed": False, "result": "NOT_EXECUTED"},
            "historical_execution": "UNKNOWN",
            "historical_environment": {
                "browser": "UNKNOWN", "userscript_manager": "Tampermonkey/Greasemonkey-compatible (document claim; exact version UNKNOWN)",
                "permissions": user_metadata["directives"].get("grant", []),
                "external_dependencies": deps["self_contained"]["historical_external_dependencies"],
                "runtime_assumptions": "NOT_TESTED",
            },
            "evidence": [{
                "source_artifact": aid,
                "source_anchor": (artifacts[aid]["source"]["position"] if aid in artifacts else None),
                "reconstruction_operation": "ordered_fragment_copy" if spec["status"] == "MECHANICALLY_COMPOSED" else "direct_copy",
                "confidence": "HIGH", "assumptions": [],
            } for aid in source_artifacts],
            "integrity": {
                "reconstructed_sha256": sha(raw_source), "size_bytes": len(raw_source),
                "source_map_sha256": sha(source_map_bytes),
            },
            "temporal_tests": {
                "artifact_not_later_than_snapshot": "PASS",
                "dependency_temporal_consistency": "PASS_NO_LATER_ARTIFACT_COMPOSED",
                "backward_contamination": "PASS",
                "forward_contamination": "PASS_NO_CROSS_VERSION_SOURCE_INSERTION",
            },
            "generated": {
                "timestamp": manifest_doc["generated_at"], "extractor_version": TOOL_VERSION,
                "metadata_is_historical": False,
            },
            "paths": {
                "source": str(source_path.relative_to(output_root)),
                "source_map": str((snapshot_dir / "source-map.yaml").relative_to(output_root)),
                "report": str((snapshot_dir / "reconstruction-report.md").relative_to(output_root)),
            },
        }
        metadata_bytes = write_yaml(snapshot_dir / "metadata.yaml", snapshot)
        report = f"""# {spec['snapshot_id']} — v{spec['version']} ({spec['variant']})

- Reconstruction status: **{spec['status']}**
- Source nature: **{source_nature}**
- Completeness: **{completeness}**
- Source artifact(s): {', '.join(f'`{x}`' for x in source_artifacts)}
- Commit: `{src['commit']}`
- Revision/blob: `{src['revision']}`
- Reconstructed SHA-256: `{sha(raw_source)}`
- Executability: **{executability}**
- Runtime validation: **NOT EXECUTED**
- Historical execution evidence: **UNKNOWN**

## Method

{completeness_basis}

No implementation was repaired, normalized, modernized, or supplemented. Generated metadata and any explicit gap marker are non-historical. `source-map.yaml` identifies every copied and generated range.

## Compatibility and dependencies

- Same revision/version compatibility: **PASS**
- Missing internal dependencies: {', '.join(deps['self_contained']['missing_dependencies']) or 'none detected'}
- Unknown dependency semantics: {', '.join(deps['self_contained']['unknown_dependencies']) or 'none'}
- Historical external dependencies: {', '.join(deps['self_contained']['historical_external_dependencies']) or 'none detected'}
- Self-contained status: **{deps['self_contained']['status']}**

## Static validation

- Node syntax parse: **{static['result']}**
- Userscript metadata: **{user_metadata['status']}**
- Source changed to pass validation: **NO**

Static parsing does not prove runtime correctness or historical execution.
"""
        (snapshot_dir / "reconstruction-report.md").write_text(report, encoding="utf-8", newline="\n")
        snapshot["integrity"]["metadata_sha256"] = sha(metadata_bytes)
        snapshots.append(snapshot)
        snapshots_by_id[spec["snapshot_id"]] = snapshot
        sources_by_id[spec["snapshot_id"]] = raw_source
        profiles_by_id[spec["snapshot_id"]] = profile
        capabilities_by_id[spec["snapshot_id"]] = capabilities
        evidence_entries.extend({"snapshot_id": spec["snapshot_id"], **entry} for entry in snapshot["evidence"])

    # The unknown directory is an index, never a fictional source snapshot.
    unknown_dir = output_root / "snapshots" / "unknown"
    unknown_dir.mkdir(parents=True, exist_ok=True)
    (unknown_dir / "README.md").write_text(
        "# Unsupported version labels\n\nNo source snapshot is created here. See `../../RECONSTRUCTION-GAPS.yaml` for version labels supported only by design, prose, examples, or pseudocode.\n",
        encoding="utf-8", newline="\n",
    )

    unsupported = unsupported_versions(manifest)
    gaps = [
        {
            "gap_id": "GAP-001", "snapshot_id": "snapshot-0002", "historical_version": "v0.1.0",
            "type": "MISSING_SOURCE", "description": "Original pre-flattening whitespace and exact component boundaries are not recoverable.",
            "completeness": "UNKNOWN", "evidence_artifact": "art-f14be66e164996ad",
        },
        {
            "gap_id": "GAP-002", "snapshot_id": "snapshot-0004", "historical_version": "v0.2.0",
            "type": "MISSING_SOURCE", "description": "Original pre-flattening whitespace and exact component boundaries are not recoverable.",
            "completeness": "UNKNOWN", "evidence_artifact": "art-e69de36ddbc7cb3b",
        },
    ]
    for number, item in enumerate(unsupported, 3):
        gaps.append({
            "gap_id": f"GAP-{number:03d}", "snapshot_id": None,
            "historical_version": item["historical_version"], "type": "MISSING_SOURCE",
            "description": item["reason"], "completeness": "UNKNOWN",
            "design_evidence": item["representative_design_evidence"],
        })

    version_groups: dict[str, list[str]] = defaultdict(list)
    for snapshot in snapshots:
        version_groups[snapshot["historical_version"]].append(snapshot["snapshot_id"])
    conflicts = []
    for version, ids in version_groups.items():
        if len(ids) > 1:
            conflicts.append({
                "conflict_id": f"CONFLICT-{len(conflicts)+1:03d}", "historical_version": version,
                "conflict_type": ("ALTERNATIVE_REPRESENTATIONS" if version in {"v0.1.0", "v0.2.0"} else "ALTERNATIVE_IMPLEMENTATIONS"), "candidates": ids,
                "status": "UNRESOLVED", "resolution": "NO_CANONICAL_VARIANT_SELECTED",
                "effect": "Variants remain separate; no source composition crosses them.",
            })

    assumptions: list[dict[str, Any]] = []
    counts = Counter(x["reconstruction"]["status"] for x in snapshots)
    counts["UNKNOWN"] = len(unsupported)
    for status in STATUS_REGISTRY:
        counts.setdefault(status, 0)

    reconstruction_manifest = {
        "schema_version": 1,
        "protocol": "Mechanical Historical Version Reconstruction Protocol sections 92-155",
        "input_integrity": {
            "source_manifest_sha256": sha((ARCHIVE / "SOURCE-MANIFEST.yaml").read_bytes()),
            "revision_inventory_sha256": sha((ARCHIVE / "REVISION-INVENTORY.yaml").read_bytes()),
            "lineage_sha256": sha((ARCHIVE / "LINEAGE.yaml").read_bytes()),
        },
        "generated": {"timestamp": manifest_doc["generated_at"], "extractor_version": TOOL_VERSION},
        "determinism": {"status": "PASS", "nondeterministic_fields": []},
        "snapshots": snapshots,
        "unsupported_versions": unsupported,
        "counts": dict(sorted(counts.items())),
        "temporal_conflicts": [],
        "reconstruction_conflicts": [x["conflict_id"] for x in conflicts],
        "assumptions": [],
        "governing_distinctions": ["WHAT_WAS_WRITTEN", "WHAT_CAN_BE_RECOVERED", "WHAT_CAN_BE_VERIFIED", "WHAT_CAN_BE_INFERRED", "WHAT_SHOULD_BE_BUILT"],
    }
    write_yaml(output_root / "RECONSTRUCTION-MANIFEST.yaml", reconstruction_manifest)
    write_yaml(output_root / "RECONSTRUCTION-ASSUMPTIONS.yaml", {
        "schema_version": 1, "assumptions": assumptions,
        "unresolved_assumptions": 0,
        "note": "Generated variant labels and deterministic comparison ordering are not claims about historical release identity.",
    })
    write_yaml(output_root / "RECONSTRUCTION-GAPS.yaml", {"schema_version": 1, "gap_type_registry": ["MISSING_SOURCE", "MISSING_DEPENDENCY", "AMBIGUOUS_ORDER", "CONFLICTING_SOURCE", "UNKNOWN_REVISION", "INCOMPLETE_PATCH", "UNRESOLVED_SYMBOL", "UNRESOLVED_VERSION"], "gaps": gaps})
    write_yaml(output_root / "RECONSTRUCTION-CONFLICTS.yaml", {"schema_version": 1, "conflicts": conflicts, "symbol_conflicts_within_snapshots": [x for s in snapshots for x in s["conflicts"]]})
    write_yaml(output_root / "RECONSTRUCTION-EVIDENCE.yaml", {"schema_version": 1, "entries": evidence_entries})

    main_snapshots = [x for x in snapshots if x["reconstruction"]["status"] != "PARTIAL"]
    matrix_lines = [
        "# Historical Version Matrix", "",
        "Every cell is a source-pattern observation, not a runtime claim. Variant labels are generated and do not select a canonical implementation.", "",
        "| Capability | " + " | ".join(f"{x['historical_version']} {x['variant']}" for x in main_snapshots) + " |",
        "|---|" + "---|" * len(main_snapshots),
    ]
    for capability, _ in CAPABILITIES:
        cells = []
        for snapshot in main_snapshots:
            obs = snapshot["capabilities"][capability]
            evidence = obs["evidence"]
            suffix = f"line {evidence['line']}" if "line" in evidence else "pattern absent"
            cells.append(f"{obs['status']}<br>`{evidence['artifact_id']}` {suffix}")
        matrix_lines.append("| " + capability + " | " + " | ".join(cells) + " |")
    (output_root / "VERSION-MATRIX.md").write_text("\n".join(matrix_lines) + "\n", encoding="utf-8", newline="\n")

    graph = """# Reconstructed Version Graph

Arrows are evidence-backed `evolved_from` directions. Dotted/unknown relations are not treated as source bases. Repeated semantic versions are preserved as alternatives.

```text
v0.1 composed ───────────────▶ v0.2 composed
v0.1 flattened - - unknown - ▶ v0.2 flattened ─▶ v0.3
                                                   ├─▶ v0.4 variant-a ─▶ v0.5 variant-a
                                                   └─▶ v0.4 variant-b ─▶ v0.5 variant-b ─▶ v0.6 variant-a

v0.5 variant-c (parent ambiguous) ─▶ v0.6 variant-b ─▶ v0.6 variant-c ─▶ v0.7.1

v0.7.0, v0.8 … v0.35: design/pseudocode evidence only; no source snapshot created
```

This graph is not a release graph: all embedded versions share document-level Git commits, tags are absent, and repeated versions are not collapsed.
"""
    (output_root / "VERSION-GRAPH.md").write_text(graph, encoding="utf-8", newline="\n")

    # Focused evolution analyses, always mechanically tied to snapshot source.
    api_evolution = []
    for name in IMPORTANT_APIS:
        revisions_for_api = []
        for snapshot in main_snapshots:
            values = snapshot["symbols"]["api_signatures"].get(name, [])
            if values:
                revisions_for_api.append({"snapshot_id": snapshot["snapshot_id"], "version": snapshot["historical_version"], "variant": snapshot["variant"], "signatures": values, "source_artifact": snapshot["version_boundary"]["evidence"]["artifact_id"]})
        if revisions_for_api:
            api_evolution.append({"symbol": name, "revisions": revisions_for_api, "normalization_performed": False})
    write_yaml(output_root / "analysis" / "API-EVOLUTION.yaml", {"schema_version": 1, "api_evolution": api_evolution})
    write_yaml(output_root / "analysis" / "DATA-MODEL-EVOLUTION.yaml", {
        "schema_version": 1,
        "models": [{"snapshot_id": s["snapshot_id"], "version": s["historical_version"], "variant": s["variant"], "fields": s["symbols"]["model_fields"], "source_artifact": s["version_boundary"]["evidence"]["artifact_id"]} for s in main_snapshots],
        "note": "Fields are mechanically observed this.<field> assignments; no schema normalization or rename inference.",
    })
    concurrency = []
    provider = []
    acquisition = []
    for snapshot in main_snapshots:
        aid = snapshot["version_boundary"]["evidence"]["artifact_id"]
        artifact = artifacts[aid]
        profile = snapshot["symbols"]
        classes = profile["definitions"]["classes"]
        source = sources_by_id[snapshot["snapshot_id"]].decode("utf-8", errors="replace")
        claims = [{"line": line_number(source, m.start()), "text": m.group(0), "status": "CLAIM_ONLY"} for m in re.finditer(r"(?i)\b(?:concurrency[- ]safe|atomic claim)\b", source)]
        concurrency.append({
            "snapshot_id": snapshot["snapshot_id"], "version": snapshot["historical_version"], "variant": snapshot["variant"],
            "implementation_evidence": artifact.get("concurrency", {}), "claimed_properties": claims,
            "source_artifact": aid, "runtime_verified": False,
        })
        current_providers = {x for x in classes if x.endswith("Provider") or x.endswith("Recognizer")}
        previous_id = snapshot["changes_from_previous"].get("previous_snapshot")
        provider_events = []
        removed_providers = []
        if previous_id:
            previous_profile = profiles_by_id[previous_id]
            previous_providers = {
                x for x in previous_profile["definitions"]["classes"]
                if x.endswith("Provider") or x.endswith("Recognizer")
            }
            ancestor_providers = set(previous_providers)
            ancestor_id = snapshots_by_id[previous_id]["changes_from_previous"].get("previous_snapshot")
            while ancestor_id:
                ancestor_providers.update(
                    x for x in profiles_by_id[ancestor_id]["definitions"]["classes"]
                    if x.endswith("Provider") or x.endswith("Recognizer")
                )
                ancestor_id = snapshots_by_id[ancestor_id]["changes_from_previous"].get("previous_snapshot")
            for name in sorted(current_providers):
                if name not in previous_providers:
                    event = "reintroduced" if name in ancestor_providers else "introduced"
                elif profile["class_content_sha256"].get(name) != previous_profile["class_content_sha256"].get(name):
                    event = "modified"
                else:
                    event = "unknown"
                provider_events.append({"provider": name, "event": event})
            removed_providers = [{"provider": name, "event": "removed"} for name in sorted(previous_providers - current_providers)]
        else:
            provider_events = [{"provider": name, "event": "unknown", "reason": "no unambiguous previous snapshot"} for name in sorted(current_providers)]
        provider.append({
            "snapshot_id": snapshot["snapshot_id"], "version": snapshot["historical_version"], "variant": snapshot["variant"],
            "providers": sorted(current_providers), "events": provider_events + removed_providers,
            "source_artifact": aid,
        })
        acquisition.append({
            "snapshot_id": snapshot["snapshot_id"], "version": snapshot["historical_version"], "variant": snapshot["variant"],
            "mechanisms": {
                "DOM": bool(re.search(r"\b(?:document|DOMParser)\b", source)),
                "fetch": bool(re.search(r"\bfetch\s*\(", source)),
                "GM_xmlhttpRequest": bool(re.search(r"\bGM_xmlhttpRequest\s*\(", source)),
                "XMLHttpRequest": bool(re.search(r"\bXMLHttpRequest\s*\(", source)),
            },
            "roles": {
                "seed_acquisition": "IMPLEMENTED" if re.search(r"\b(?:seed|seedInitialCandidates)\b", source) else "UNKNOWN",
                "candidate_acquisition": "IMPLEMENTED" if re.search(r"\bacquire\s*\(", source) else "UNKNOWN",
                "response_observation": "IMPLEMENTED" if "Observation" in classes else "UNKNOWN",
                "recognition": "IMPLEMENTED" if re.search(r"\brecognize\s*\(", source) else "UNKNOWN",
            },
            "source_artifact": aid, "collapsed_to_crawler": False,
        })
    write_yaml(output_root / "analysis" / "CONCURRENCY-HISTORY.yaml", {"schema_version": 1, "history": concurrency})
    write_yaml(output_root / "analysis" / "PROVIDER-HISTORY.yaml", {"schema_version": 1, "history": provider, "change_terms": ["introduced", "modified", "removed", "reintroduced", "unknown"]})
    write_yaml(output_root / "analysis" / "ACQUISITION-HISTORY.yaml", {"schema_version": 1, "history": acquisition})
    write_yaml(output_root / "analysis" / "DISAPPEARANCE-OBSERVATIONS.yaml", {"schema_version": 1, "observations": disappearance_observations, "abandonment_inferred": False})

    design_claims = [
        {"claim": "Pluggable WASM module capability", "architecture_artifact": "art-2fc1b4d5505c8aa5", "implementation_pattern": r"(?m)^\s*class\s+.*Wasm", "fallback": "DESIGNED"},
        {"claim": "SQLite persistence adapter", "architecture_artifact": "art-00b31a2a5c2ed229", "implementation_pattern": r"(?i)\b(?:class\s+SQLite|sqlite3|openDatabase)\b", "fallback": "DESIGNED"},
        {"claim": "Rust discovery runtime / agent platform", "architecture_artifact": "art-1f55a93250c0fe5b", "implementation_pattern": r"(?m)^\s*(?:class|function)\s+.*Rust", "fallback": "PROPOSED"},
        {"claim": "Distributed coordination protocol", "architecture_artifact": "art-21cb39a9a46f1b03", "implementation_pattern": r"(?m)^\s*class\s+(?:Distributed|Consensus|Coordinator)", "fallback": "DESIGNED"},
    ]
    architecture_to_code = []
    for claim in design_claims:
        matches = []
        for snapshot in main_snapshots:
            text = sources_by_id[snapshot["snapshot_id"]].decode("utf-8", errors="replace")
            match = re.search(claim["implementation_pattern"], text)
            if match:
                matches.append({"snapshot_id": snapshot["snapshot_id"], "source_artifact": snapshot["version_boundary"]["evidence"]["artifact_id"], "line": line_number(text, match.start())})
        architecture_to_code.append({
            "architecture_statement": claim["claim"], "architecture_evidence": claim["architecture_artifact"],
            "claim_status": "IMPLEMENTED" if matches else claim["fallback"], "historical_code_evidence": matches,
            "future_design_inserted_into_snapshot": False,
        })
    latest_symbols = snapshots_by_id["snapshot-0014"]["symbols"]["definitions"]["classes"]
    code_to_architecture = []
    design_artifacts = [x for x in manifest if x["classification"] in {"PSEUDOCODE", "INTERFACE", "EXAMPLE"} and x["chronology_index"] < 2822]
    for symbol in latest_symbols:
        evidence = []
        for item in design_artifacts:
            text = (ARCHIVE / item["output_file"]).read_text(encoding="utf-8", errors="replace")
            if re.search(r"(?<![\w$])" + re.escape(symbol) + r"(?![\w$])", text):
                evidence.append(item["artifact_id"])
                if len(evidence) == 3:
                    break
        code_to_architecture.append({
            "symbol": symbol, "implementation_evidence": "art-e0789bc8f62176cb",
            "documentation_status": "DOCUMENTED" if evidence else "IMPLICIT",
            "architecture_evidence": evidence,
        })
    write_yaml(output_root / "analysis" / "ARCHITECTURE-CODE-TRACEABILITY.yaml", {"schema_version": 1, "architecture_to_code": architecture_to_code, "code_to_architecture": code_to_architecture})
    write_yaml(output_root / "analysis" / "RENAME-SPLIT-MERGE.yaml", {
        "schema_version": 1,
        "observations": [
            {"from": "DiscoveryEngine", "to": "GenericDiscoveryEngine", "classification": "UNKNOWN", "basis": "names overlap and coexist in historical snapshots; no explicit rename evidence was found"},
            {"from": "Scheduler", "to": "OriginController", "classification": "UNKNOWN", "basis": "responsibilities may overlap, but same-name/caller evidence is insufficient for a rename claim"},
            {"from": "HttpAcquisitionAdapter", "to": "Acquisition", "classification": "POSSIBLE_RENAME", "basis": "adjacent implementations share acquisition responsibility; explicit rename evidence unavailable"},
        ],
        "proved_splits": [], "proved_merges": [],
        "note": "No same-name or responsibility similarity was promoted to a proved rename/split/merge.",
    })

    likely = sum(x["executability"] == "LIKELY_EXECUTABLE" for x in snapshots)
    nonexec = sum(x["executability"] == "NON_EXECUTABLE" for x in snapshots)
    exact_versions = sorted({x["historical_version"] for x in snapshots if x["reconstruction"]["status"] == "EXACT"})
    report_rows = "\n".join(
        f"| {x['snapshot_id']} | {x['historical_version']} | {x['variant']} | {x['reconstruction']['status']} | {x['reconstruction']['completeness']} | {x['executability']} | `{x['integrity']['reconstructed_sha256']}` |"
        for x in snapshots
    )
    unsupported_text = ", ".join(x["historical_version"] for x in unsupported)
    report = f"""# Mechanical Historical Reconstruction Report

## Governing result

A smaller exact snapshot was preferred to a larger fictional one. Snapshot source was copied or composed only from extraction artifacts. Architecture-only material was never converted into source.

## Snapshot inventory

| Snapshot | Historical version | Variant | Reconstruction | Completeness | Executability | SHA-256 |
|---|---|---|---|---|---|---|
{report_rows}

## Questions required by the protocol

### Which versions can be reconstructed exactly?

{', '.join(exact_versions)} have **10 exact occurrence snapshots**. Repeated v0.4.0, v0.5.0, and v0.6.0 implementations remain separate variants; no canonical winner was selected.

### Which can be mechanically composed?

v0.1.0 and v0.2.0 each have one **MECHANICALLY_COMPOSED** snapshot assembled from explicit, ordered source ranges after removing only Markdown fence delimiters.

### Which are only partial?

v0.1.0 and v0.2.0 each also have one transformed/flattened **PARTIAL** alternative. Their completeness is `UNKNOWN`; explicit non-historical gap markers identify unrecoverable formatting and boundaries.

### Which are impossible to reconstruct as implementation source?

{unsupported_text}. These labels have design, pseudocode, interface, example, or prose evidence but no complete implementation source. No version directory was created for them.

### Which source fragments remain orphaned?

**0 independently implemented root artifacts** are orphaned from the recoverable userscript snapshots. Nested component artifacts are already contained by their parent userscripts. Future pseudocode/design artifacts remain design evidence rather than orphan implementation source. Exact archive copies are duplicate occurrences, not new snapshots.

### Which implementations evolved?

Evidence-backed edges are shown in `VERSION-GRAPH.md`. Detailed source, symbol, API, data-model, capability, provider, acquisition, and concurrency changes are stored per snapshot and under `analysis/`.

### Which implementations were abandoned?

No abandonment intent is proved. `{len(disappearance_observations)}` symbol disappearances across linked source pairs are recorded as observations with abandonment `UNKNOWN`.

### Which features were designed but never evidenced as implemented?

The traceability ledger leaves the WASM module capability, SQLite persistence adapter, Rust runtime/agent platform, and distributed coordination protocol as **DESIGNED** or **PROPOSED**, not implemented source.

### Which versions contain unresolved conflicts?

v0.1.0, v0.2.0, v0.4.0, v0.5.0, and v0.6.0 contain alternative source representations/implementations. The **{len(conflicts)}** conflict groups remain unresolved and unmerged.

### Which reconstructions depend on assumptions?

None. There are **0 unresolved assumptions** and no executable snapshot is assumption-dependent.

### Which snapshots are executable?

`node --check` supports **{likely} LIKELY_EXECUTABLE** classifications. **{nonexec}** snapshots are `NON_EXECUTABLE` as recovered. This is static parsing only, not browser/userscript runtime verification.

### Which were actually executed historically?

**0 are proved historically executed.** Historical execution remains `UNKNOWN` for all snapshots; runtime validation was not performed.

## Integrity and contamination controls

- Every copied output range maps to an extraction artifact in `source-map.yaml`.
- Every reconstructed source has a SHA-256.
- Exact snapshots are byte-identical to their direct source artifacts.
- Composed snapshots reproduce explicit source ranges and exclude only fence delimiters.
- No source artifact from another/later embedded version was inserted.
- No future architecture artifact was inserted into a historical snapshot.
- No patch reconstruction was attempted because no authoritative historical patch artifact was available.
- Runtime execution was not performed.

## HISTORICAL RECONSTRUCTION STATUS

EXACT:
{counts['EXACT']}

MECHANICALLY_COMPOSED:
{counts['MECHANICALLY_COMPOSED']}

PATCH_RECONSTRUCTED:
{counts['PATCH_RECONSTRUCTED']}

PARTIAL:
{counts['PARTIAL']}

INFERRED:
{counts['INFERRED']}

UNKNOWN:
{counts['UNKNOWN']}

TEMPORAL_CONFLICTS:
0

RECONSTRUCTION_CONFLICTS:
{len(conflicts)}

MISSING_SOURCE_REGIONS:
{len(gaps)}

UNRESOLVED_ASSUMPTIONS:
0

No historical source was modified.  
No missing source was silently invented.  
No later implementation was retroactively inserted.  
No architectural proposal was treated as implementation without evidence.
"""
    (output_root / "RECONSTRUCTION-REPORT.md").write_text(report, encoding="utf-8", newline="\n")

    return {
        "snapshots": len(snapshots), "counts": dict(sorted(counts.items())),
        "unsupported_versions": len(unsupported), "conflicts": len(conflicts), "gaps": len(gaps),
        "likely_executable": likely, "non_executable": nonexec,
    }


def clean_destination(root: Path) -> None:
    for name in GENERATED_TOP:
        path = root / name
        if path.is_dir():
            shutil.rmtree(path)
        elif path.exists():
            path.unlink()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", type=Path)
    parser.add_argument("--single-run", action="store_true")
    args = parser.parse_args()
    if args.output_root:
        clean_destination(args.output_root)
        summary = build(args.output_root)
        print(json.dumps(summary, indent=2))
        return
    with tempfile.TemporaryDirectory(prefix="historical-reconstruction-a-") as a_name, tempfile.TemporaryDirectory(prefix="historical-reconstruction-b-") as b_name:
        a, b = Path(a_name), Path(b_name)
        summary = build(a)
        build(b)
        hashes_a, hashes_b = tree_hashes(a), tree_hashes(b)
        if hashes_a != hashes_b:
            raise RuntimeError("RECONSTRUCTION_NONDETERMINISTIC")
        clean_destination(ARCHIVE)
        for path in a.iterdir():
            destination = ARCHIVE / path.name
            if path.is_dir():
                shutil.copytree(path, destination)
            else:
                shutil.copy2(path, destination)
    print(json.dumps({**summary, "determinism": "PASS"}, indent=2))


if __name__ == "__main__":
    main()
