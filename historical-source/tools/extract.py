#!/usr/bin/env python3
"""Mechanical extractor for the two historical Markdown source documents.

The extractor never reformats source payloads. Original artifact files are byte
slices of pinned Git blobs. JSON-compatible YAML is used so validation needs no
third-party YAML emitter/parser.
"""

from __future__ import annotations

import bisect
import datetime as dt
import difflib
import hashlib
import json
import re
import shutil
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "historical-source"

# Pinned source revisions discovered from all refs after an unshallow fetch.
REVISIONS = [
    {
        "order": 0,
        "document": "Userscript Discovery Prototype.md",
        "path": "Userscript Discovery Prototype.md",
        "revision": "38bd0fece1136e8beaa6101ce659c35fc17b52af",
        "commit": "cc8df7357c2dbfe9d149747743e2f5e9ac9c0178",
        "parent_revision": None,
        "author": "Abdus2023",
        "timestamp": "2026-09-10T20:36:25+01:00",
        "branch": "main",
        "branches_observed": [
            "arena/01a08fba-generic-discovery-engine",
            "main",
            "origin/arena/01a08cd3-generic-discovery-engine",
            "origin/arena/01a08d14-generic-discovery-engine",
            "origin/arena/01a08f03-generic-discovery-engine",
            "origin/main",
        ],
        "tags": [],
        "occurrences": [
            {"commit": "cc8df7357c2dbfe9d149747743e2f5e9ac9c0178", "path": "Userscript Discovery Prototype.md", "event": "introduced_on_main"},
            {"commit": "400810db93e5bd742d2c1a8ac8ac49a14bc4643b", "path": "archive/Userscript Discovery Prototype.md", "event": "exact_rename_on_origin_arena_01a08d14"},
            {"commit": "48b08f20badbf8e4f19aae73137f9199a9be2ecd", "path": "Userscript Discovery Prototype.md", "event": "unchanged_occurrence_before_bannered_archive_on_origin_arena_01a08f03"},
        ],
        "revision_kind": "original_git_blob",
    },
    {
        "order": 1,
        "document": "Continue Architecture Planning.md",
        "path": "Continue Architecture Planning.md",
        "revision": "1c7b52bb1244677ba22bf25285ba199f9e5f722d",
        "commit": "cc8df7357c2dbfe9d149747743e2f5e9ac9c0178",
        "parent_revision": None,
        "author": "Abdus2023",
        "timestamp": "2026-09-10T20:36:25+01:00",
        "branch": "main",
        "branches_observed": [
            "arena/01a08fba-generic-discovery-engine",
            "main",
            "origin/arena/01a08cd3-generic-discovery-engine",
            "origin/arena/01a08d14-generic-discovery-engine",
            "origin/arena/01a08f03-generic-discovery-engine",
            "origin/main",
        ],
        "tags": [],
        "occurrences": [
            {"commit": "cc8df7357c2dbfe9d149747743e2f5e9ac9c0178", "path": "Continue Architecture Planning.md", "event": "introduced_on_main"},
            {"commit": "400810db93e5bd742d2c1a8ac8ac49a14bc4643b", "path": "archive/Continue Architecture Planning.md", "event": "exact_rename_on_origin_arena_01a08d14"},
            {"commit": "48b08f20badbf8e4f19aae73137f9199a9be2ecd", "path": "Continue Architecture Planning.md", "event": "unchanged_occurrence_before_bannered_archive_on_origin_arena_01a08f03"},
        ],
        "revision_kind": "original_git_blob",
    },
    {
        "order": 2,
        "document": "Userscript Discovery Prototype.md",
        "path": "archive/Userscript Discovery Prototype.md",
        "revision": "844851b9aafa927b7aeef62a59ec143b8765f3ff",
        "commit": "167a245afde8a7863650ec153acfb66ddc714555",
        "parent_revision": "38bd0fece1136e8beaa6101ce659c35fc17b52af",
        "author": "Abdus2023",
        "timestamp": "2026-09-11T06:30:20+00:00",
        "branch": "origin/arena/01a08f03-generic-discovery-engine",
        "branches_observed": ["origin/arena/01a08f03-generic-discovery-engine"],
        "tags": [],
        "occurrences": [
            {"commit": "167a245afde8a7863650ec153acfb66ddc714555", "path": "archive/Userscript Discovery Prototype.md", "event": "archive_banner_added"},
        ],
        "revision_kind": "archived_copy_with_provenance_banner",
    },
    {
        "order": 3,
        "document": "Continue Architecture Planning.md",
        "path": "archive/Continue Architecture Planning.md",
        "revision": "b69aa1964883bec154e7f81dce72f5bc22e7472d",
        "commit": "167a245afde8a7863650ec153acfb66ddc714555",
        "parent_revision": "1c7b52bb1244677ba22bf25285ba199f9e5f722d",
        "author": "Abdus2023",
        "timestamp": "2026-09-11T06:30:20+00:00",
        "branch": "origin/arena/01a08f03-generic-discovery-engine",
        "branches_observed": ["origin/arena/01a08f03-generic-discovery-engine"],
        "tags": [],
        "occurrences": [
            {"commit": "167a245afde8a7863650ec153acfb66ddc714555", "path": "archive/Continue Architecture Planning.md", "event": "archive_banner_added"},
        ],
        "revision_kind": "archived_copy_with_provenance_banner",
    },
]

REVISION_EVENTS = [
    {
        "commit": "cc8df7357c2dbfe9d149747743e2f5e9ac9c0178",
        "timestamp": "2026-09-10T20:36:25+01:00",
        "event": "introduced",
        "paths": ["Userscript Discovery Prototype.md", "Continue Architecture Planning.md"],
        "content_change": True,
    },
    {
        "commit": "400810db93e5bd742d2c1a8ac8ac49a14bc4643b",
        "timestamp": "2026-09-10T20:59:11+00:00",
        "event": "renamed_to_archive",
        "paths": ["archive/Userscript Discovery Prototype.md", "archive/Continue Architecture Planning.md"],
        "content_change": False,
        "branch": "origin/arena/01a08d14-generic-discovery-engine",
    },
    {
        "commit": "167a245afde8a7863650ec153acfb66ddc714555",
        "timestamp": "2026-09-11T06:30:20+00:00",
        "event": "renamed_to_archive_and_prefixed_with_archive_banner",
        "paths": ["archive/Userscript Discovery Prototype.md", "archive/Continue Architecture Planning.md"],
        "content_change": True,
        "branch": "origin/arena/01a08f03-generic-discovery-engine",
    },
]

DEPENDENCY_NAMES = [
    "Candidate", "CandidateQueue", "Scheduler", "Worker", "Observation",
    "Discovery", "KnowledgeBase", "Provider", "ProviderRegistry",
    "ResponseProvider", "Acquisition", "AcquisitionRuntime", "DiscoveryEngine",
    "DiscoveryController", "CandidateSource", "RecognitionRuntime", "EventLedger",
    "ProvenanceGraph", "ResourceRegistry", "NetworkObserver", "FrontierRuntime",
    "FrontierArbitrator", "OriginController", "GM_xmlhttpRequest", "GM_getValue",
    "GM_setValue", "fetch", "XMLHttpRequest", "DOMParser", "MutationObserver",
    "PerformanceObserver", "AbortController", "URL", "Map", "Set", "Promise",
    "document", "window", "localStorage", "IndexedDB", "BroadcastChannel",
]

FENCE_RE = re.compile(br"^(?P<indent>[ \t]*)```(?P<label>[^`\r\n]*)\r?\n?$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
VERSION_RE = re.compile(r"\bv(\d+(?:\.\d+){0,2})\b", re.I)
EXPLICIT_VERSION_RE = re.compile(br"(?m)^\s*//\s*@version\s+([^\r\n]+?)\s*$")


_FETCH_ATTEMPTED = False


def git_blob(oid: str) -> bytes:
    """Read a pinned blob, fetching all historical refs once if clone is shallow."""
    global _FETCH_ATTEMPTED
    try:
        return subprocess.check_output(
            ["git", "cat-file", "blob", oid], cwd=ROOT,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        if _FETCH_ATTEMPTED:
            raise
        _FETCH_ATTEMPTED = True
        shallow = subprocess.check_output(
            ["git", "rev-parse", "--is-shallow-repository"], cwd=ROOT, text=True,
        ).strip() == "true"
        command = ["git", "fetch"]
        if shallow:
            command.append("--unshallow")
        command += [
            "origin",
            "+refs/heads/*:refs/remotes/origin/*",
            "+refs/tags/*:refs/tags/*",
        ]
        subprocess.run(command, cwd=ROOT, check=True)
        return subprocess.check_output(["git", "cat-file", "blob", oid], cwd=ROOT)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def slug(value: str, limit: int = 64) -> str:
    value = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", value)
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return (value or "unnamed")[:limit].rstrip("-")


def line_ending(data: bytes) -> str:
    crlf = data.count(b"\r\n")
    lf = data.count(b"\n")
    if lf and crlf == lf:
        return "CRLF"
    if lf and crlf == 0:
        return "LF"
    if lf:
        return "MIXED"
    return "NONE"


def decode(data: bytes) -> str:
    return data.decode("utf-8-sig", errors="replace")


def cap_context(data: bytes, keep_tail: bool) -> str:
    if len(data) > 4000:
        data = data[-4000:] if keep_tail else data[:4000]
    text = data.decode("utf-8-sig", errors="replace")
    return text


def source_structure(data: bytes) -> dict[str, Any]:
    lines = data.splitlines(keepends=True)
    starts: list[int] = []
    offset = 0
    for line in lines:
        starts.append(offset)
        offset += len(line)
    starts.append(offset)

    fences: list[dict[str, Any]] = []
    outside = [True] * len(lines)
    active: tuple[int, bytes, bytes] | None = None
    for i, line in enumerate(lines):
        match = FENCE_RE.match(line)
        if match:
            if active is None:
                active = (i, match.group("indent"), match.group("label"))
                outside[i] = False
            else:
                open_i, indent, label = active
                outside[i] = False
                fences.append({
                    "open_i": open_i,
                    "close_i": i,
                    "indent": indent,
                    "label": label.decode("utf-8", errors="replace").strip(),
                    "start": starts[open_i + 1],
                    "end": starts[i],
                    "content": data[starts[open_i + 1]:starts[i]],
                })
                active = None
            continue
        if active is not None:
            outside[i] = False
    unclosed = None
    if active is not None:
        unclosed = active[0] + 1

    headings: list[dict[str, Any]] = []
    turns: list[dict[str, Any]] = []
    version_context: list[str | None] = [None] * len(lines)
    current_version = None
    for i, line in enumerate(lines):
        text = line.decode("utf-8-sig", errors="replace").rstrip("\r\n")
        if outside[i]:
            if text in ("**You:**", "**ChatGPT:**"):
                turns.append({"i": i, "speaker": text.strip("*:")})
                current_version = None
            heading = HEADING_RE.match(text)
            if heading:
                headings.append({"i": i, "level": len(heading.group(1)), "title": heading.group(2)})
                versions = VERSION_RE.findall(heading.group(2))
                if versions:
                    current_version = versions[-1]
            version_context[i] = current_version
        elif i:
            version_context[i] = version_context[i - 1]
        if i and version_context[i] is None and not (outside[i] and text in ("**You:**", "**ChatGPT:**")):
            version_context[i] = version_context[i - 1]

    boundaries = {0, len(lines)}
    for fence in fences:
        boundaries.add(fence["open_i"])
        boundaries.add(fence["close_i"])
    boundaries.update(x["i"] for x in headings)
    boundaries.update(x["i"] for x in turns)
    boundaries_sorted = sorted(boundaries)

    return {
        "lines": lines,
        "starts": starts,
        "fences": fences,
        "outside": outside,
        "headings": headings,
        "turns": turns,
        "version_context": version_context,
        "boundaries": boundaries_sorted,
        "unclosed_fence": unclosed,
    }


def line_for_offset(starts: list[int], offset: int) -> int:
    return bisect.bisect_right(starts, offset)  # 1-based line for ordinary offsets


def nearest_heading(struct: dict[str, Any], line_i: int) -> tuple[str, int | None]:
    # A heading from a previous chat turn is not the heading of the current
    # source section. Conversation markers therefore bound heading lookup.
    turn_floor = -1
    for turn in struct["turns"]:
        if turn["i"] < line_i:
            turn_floor = turn["i"]
        else:
            break
    found = None
    for heading in struct["headings"]:
        if turn_floor < heading["i"] < line_i:
            found = heading
        elif heading["i"] >= line_i:
            break
    return (found["title"], found["i"] + 1) if found else ("", None)


def nearest_turn(struct: dict[str, Any], line_i: int) -> tuple[str, int | None]:
    found = None
    for turn in struct["turns"]:
        if turn["i"] < line_i:
            found = turn
        else:
            break
    return (found["speaker"], found["i"] + 1) if found else ("UNKNOWN", None)


def context_for(struct: dict[str, Any], start_i: int, end_i: int) -> dict[str, Any]:
    boundaries = struct["boundaries"]
    lines = struct["lines"]

    # For a fenced region start_i is its first content line and end_i is its
    # closing-fence index. Skip those two delimiter boundaries so BEFORE and
    # AFTER retain the explanatory prose surrounding the fence.
    before_limit = start_i
    if start_i > 0 and FENCE_RE.match(lines[start_i - 1]):
        before_limit = start_i - 1
    previous = max((x for x in boundaries if x < before_limit), default=-1)
    before = b"".join(lines[previous + 1:before_limit])

    after_start = end_i
    if end_i < len(lines) and FENCE_RE.match(lines[end_i]):
        after_start = end_i + 1
    following = min((x for x in boundaries if x >= after_start), default=len(lines))
    if following == after_start and following < len(lines):
        following = min((x for x in boundaries if x > after_start), default=len(lines))
    following_heading = ""
    if following < len(lines):
        candidate = lines[following].decode("utf-8-sig", errors="replace").rstrip("\r\n")
        heading_match = HEADING_RE.match(candidate)
        if heading_match:
            following_heading = heading_match.group(2)
            # A post-code "What changed"/next-section heading is immediate
            # explanatory context. Include it and its prose up to the next
            # structural boundary, rather than retaining only a blank line.
            following = min((x for x in boundaries if x > following), default=len(lines))
    after = b"".join(lines[after_start:following])

    heading, heading_line = nearest_heading(struct, start_i)
    speaker, turn_line = nearest_turn(struct, start_i)
    return {
        "preceding_text": cap_context(before, True),
        "following_text": cap_context(after, False),
        "section_title": heading,
        "heading_line": heading_line,
        "following_section_title": following_heading,
        "conversation_speaker": speaker,
        "conversation_turn_line": turn_line,
    }


def explicit_version(content: bytes) -> str | None:
    match = EXPLICIT_VERSION_RE.search(content)
    if match:
        return match.group(1).decode("utf-8", errors="replace").strip()
    # Flattened paste has all metadata on one line.
    match = re.search(br"//\s*@version\s+([0-9]+(?:\.[0-9]+){0,2})", content)
    return match.group(1).decode() if match else None


def infer_version(struct: dict[str, Any], start_i: int, context: dict[str, Any]) -> tuple[str | None, str]:
    if start_i < len(struct["version_context"]) and struct["version_context"][start_i]:
        return struct["version_context"][start_i], "INFERRED_FROM_HEADING"
    combined = context["preceding_text"][-1600:] + "\n" + context["section_title"]
    versions = VERSION_RE.findall(combined)
    if versions:
        return versions[-1], "INFERRED_FROM_CONTEXT"
    return None, "UNKNOWN"


def primary_symbol(content: bytes) -> tuple[str | None, str | None]:
    text = decode(content)
    patterns = [
        (r"(?m)^\s*class\s+([A-Za-z_$][\w$]*)", "class"),
        (r"(?m)^\s*interface\s+([A-Za-z_$][\w$]*)", "interface"),
        (r"(?m)^\s*(?:async\s+)?function\s+([A-Za-z_$][\w$]*)", "function"),
        (r"(?m)^\s*const\s+([A-Za-z_$][\w$]*)\s*=", "constant"),
        (r"(?m)^\s*type\s+([A-Za-z_$][\w$]*)\s*=", "type"),
    ]
    for pattern, kind in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1), kind
    return None, None


def infer_language(label: str, content: bytes) -> str:
    normalized = label.strip().lower()
    mapping = {
        "javascript": "javascript", "js": "javascript", "typescript": "typescript",
        "ts": "typescript", "json": "json", "yaml": "yaml", "yml": "yaml",
        "bash": "shell", "sh": "shell", "rust": "rust", "html": "html",
        "xml": "xml", "http": "http", "diff": "diff", "patch": "diff",
        "mermaid": "mermaid",
    }
    if normalized in mapping:
        return mapping[normalized]
    sample = decode(content[:5000])
    if re.search(r"(?m)^\s*(?:class|const|let|var|function|async\s+function)\b", sample):
        return "javascript"
    if "=>" in sample and ("{" in sample or ";" in sample):
        return "javascript"
    if re.search(r"(?m)^\s*(?:interface|type)\s+[A-Za-z_$]", sample):
        return "typescript"
    return "text"


def detect_diff(content: bytes, label: str) -> bool:
    if label.lower() in ("diff", "patch"):
        return True
    lines = decode(content).splitlines()
    markers = sum(1 for x in lines if x.startswith(("@@ ", "diff ", "--- ", "+++ ", "+ ", "- ")))
    return markers >= 2


def classify(content: bytes, label: str, context: dict[str, Any], method: str,
             complete_userscript: bool = False, nested_kind: str | None = None,
             nested_symbol: str | None = None) -> dict[str, Any]:
    text = decode(content)
    lower = text.lower()
    heading = context.get("section_title", "").lower()
    surrounding = (context.get("preceding_text", "") + " " + context.get("following_text", "")).lower()
    language = infer_language(label, content)
    symbol, symbol_kind = primary_symbol(content)
    if nested_symbol:
        symbol, symbol_kind = nested_symbol, nested_kind

    if complete_userscript or "==userscript==" in lower:
        artifact_type = "userscript"
        secondary = "USERSCRIPT"
        if method == "outside_userscript":
            classification = "PARTIAL_IMPLEMENTATION"
            status = "PARTIAL_IMPLEMENTATION"
            incomplete = True
        else:
            classification = "IMPLEMENTED"
            status = "HISTORICAL_IMPLEMENTATION"
            incomplete = False
        short = "generic-discovery" + (("-v" + explicit_version(content).replace(".", "-")) if explicit_version(content) else "")
    else:
        key = (symbol or "") + " " + heading
        key_lower = key.lower()
        if detect_diff(content, label):
            artifact_type, secondary = "patch", "UTILITY"
            classification, status = "DIFF", "UNVERIFIED"
        elif method == "inline_fragment":
            artifact_type, secondary = "fragment", "UTILITY"
            classification = "EXAMPLE" if "→" in text else "PSEUDOCODE"
            status = "EXAMPLE_ONLY" if classification == "EXAMPLE" else "PSEUDOCODE"
        elif nested_kind == "ui_section":
            artifact_type, secondary = "ui", "UI"
            classification, status = "IMPLEMENTED", "HISTORICAL_IMPLEMENTATION"
        elif nested_kind == "configuration":
            artifact_type, secondary = "configuration", "UTILITY"
            classification, status = "CONFIGURATION", "HISTORICAL_IMPLEMENTATION"
        elif "test" in heading and re.search(r"\b(assert|expect|test|describe|it)\s*\(", text):
            artifact_type, secondary = "test", "UTILITY"
            classification, status = "TEST", "UNVERIFIED"
        elif language == "json" and ("schema" in heading or '"$schema"' in lower):
            artifact_type, secondary = "schema", "STORAGE"
            classification, status = "SCHEMA", "PSEUDOCODE"
        elif "configuration" in heading or (symbol and symbol.upper() in {"CONFIG", "CONFIGURATION", "DEFAULTS", "LIMITS"}):
            artifact_type, secondary = "configuration", "UTILITY"
            classification, status = "CONFIGURATION", "PSEUDOCODE"
        elif "provider" in key_lower or "recognizer" in key_lower or "candidatesource" in key_lower:
            artifact_type, secondary = "provider", "PROVIDER"
            if any(x in heading for x in ("contract", "interface")) or "not implemented" in lower:
                classification = "INTERFACE"
            else:
                classification = "IMPLEMENTED" if nested_kind == "class" else "PSEUDOCODE"
            status = "HISTORICAL_IMPLEMENTATION" if nested_kind == "class" else "PSEUDOCODE"
        elif any(x in key_lower for x in ("acquisition", "httpacquisition", "gm-xhr", "gmxhr")):
            artifact_type, secondary = "acquisition", "ACQUISITION"
            classification = "IMPLEMENTED" if nested_kind == "class" else "PSEUDOCODE"
            status = "HISTORICAL_IMPLEMENTATION" if nested_kind == "class" else "PSEUDOCODE"
        elif any(x in key_lower for x in ("scheduler", "candidatequeue", "worker", "frontierarbitrator", "leasemanager")):
            artifact_type, secondary = "scheduler", "SCHEDULER"
            classification = "IMPLEMENTED" if nested_kind == "class" else "PSEUDOCODE"
            status = "HISTORICAL_IMPLEMENTATION" if nested_kind == "class" else "PSEUDOCODE"
        elif symbol and not any(x in symbol.lower() for x in ("engine", "controller", "runtime", "registry")) and any(x in symbol.lower() for x in ("candidate", "observation", "discovery", "knowledge", "record", "event", "result", "provenance", "resource", "claim", "budget", "plan", "policy", "state", "evidence", "goal", "query", "partition", "coverage", "session", "domain", "artifact", "conflict")):
            artifact_type, secondary = "model", "CANDIDATE" if "candidate" in symbol.lower() else "OBSERVATION" if "observation" in symbol.lower() else "DISCOVERY"
            classification = "IMPLEMENTED" if nested_kind == "class" else ("INTERFACE" if "contract" in heading else "PSEUDOCODE")
            status = "HISTORICAL_IMPLEMENTATION" if nested_kind == "class" else "PSEUDOCODE"
        elif symbol and any(x in symbol.lower() for x in ("engine", "controller", "runtime", "registry")):
            artifact_type, secondary = "engine", "ENGINE"
            classification = "IMPLEMENTED" if nested_kind == "class" else "PSEUDOCODE"
            status = "HISTORICAL_IMPLEMENTATION" if nested_kind == "class" else "PSEUDOCODE"
        elif language in ("json", "yaml"):
            artifact_type, secondary = "configuration", "UTILITY"
            classification, status = "EXAMPLE", "EXAMPLE_ONLY"
        else:
            artifact_type, secondary = "pseudocode", "UTILITY"
            if "example" in heading or "for example" in surrounding[-500:]:
                classification, status = "EXAMPLE", "EXAMPLE_ONLY"
            elif symbol_kind == "interface" or "contract" in heading:
                classification, status = "INTERFACE", "PSEUDOCODE"
            else:
                classification, status = "PSEUDOCODE", "PSEUDOCODE"
        incomplete = bool(re.search(r"\b(?:remaining implementation omitted|not implemented|todo)\b", lower))
        short = symbol or context.get("section_title") or next((x.strip() for x in text.splitlines() if x.strip()), "fragment")

    return {
        "artifact_type": artifact_type,
        "secondary_classification": secondary,
        "classification": classification,
        "status": status,
        "verification": "UNVERIFIED",
        "language": language,
        "short_name": slug(short),
        "symbol": symbol,
        "symbol_kind": symbol_kind,
        "incomplete": incomplete,
    }


def dependencies(content: bytes, own_symbol: str | None) -> list[str]:
    text = decode(content)
    found = []
    for name in DEPENDENCY_NAMES:
        if name != own_symbol and re.search(r"(?<![\w$])" + re.escape(name) + r"(?![\w$])", text):
            found.append(name)
    extends = re.search(r"\bextends\s+([A-Za-z_$][\w$]*)", text)
    if extends and extends.group(1) != own_symbol and extends.group(1) not in found:
        found.insert(0, extends.group(1))
    return found


def concurrency_record(content: bytes, context: dict[str, Any]) -> dict[str, Any] | None:
    text = decode(content)
    lower = text.lower()
    terms = ("concurrency", "worker", "claimnextcandidate", "claimed", "semaphore", "mutex", "promise.all", "lease")
    if not any(term in lower for term in terms):
        return None
    worker_count = None
    for pattern in (
        r"\bconcurrency\s*:\s*(\d+)", r"\bworkerCount\s*[:=]\s*(\d+)",
        r"\bmaxWorkers\s*[:=]\s*(\d+)",
    ):
        match = re.search(pattern, text, re.I)
        if match:
            worker_count = int(match.group(1))
            break
    mechanisms = []
    for literal, label in (
        ("claimNextCandidate", "claimNextCandidate"), ("claimed", "claimed state/set"),
        ("visited", "visited state/set"), ("lease", "lease"), ("fencing", "fencing token"),
        ("semaphore", "semaphore"), ("mutex", "mutex"),
    ):
        if literal.lower() in lower:
            mechanisms.append(label)
    models = []
    if "promise.all" in lower or re.search(r"\bworkers?\b", lower):
        models.append("async worker pool")
    if "queue" in lower or "frontier" in lower:
        models.append("shared queue/frontier")
    if "lease" in lower:
        models.append("lease-based ownership")
    if not models:
        models.append("unspecified concurrency discussion")
    awaits = [i + 1 for i, line in enumerate(text.splitlines()) if re.search(r"\bawait\b", line)]
    asserted = any(x in (context.get("preceding_text", "") + context.get("following_text", "")).lower() for x in ("atomic", "safe", "exclusive"))
    return {
        "model": models,
        "worker_count": worker_count if worker_count is not None else "UNKNOWN",
        "ownership_mechanism": mechanisms or ["UNKNOWN"],
        "claim_point": "claimNextCandidate" if "claimnextcandidate" in lower else "UNKNOWN",
        "async_boundary": f"first await at artifact line {awaits[0]}" if awaits else "NONE_OBSERVED",
        "duplicate_prevention": [x for x in mechanisms if x in ("claimed state/set", "visited state/set", "lease", "fencing token")] or ["UNKNOWN"],
        "cancellation": [x for x in ("AbortController", "stop", "pause", "cancel") if x.lower() in lower] or ["UNKNOWN"],
        "error_isolation": "try/catch observed" if "try" in lower and "catch" in lower else "UNKNOWN",
        "asserted_safety": asserted,
        "mechanical_safety_observations": mechanisms,
        "verification_status": "UNVERIFIED",
        "safety_conclusion": "UNKNOWN",
    }


def brace_end(data: bytes, opening: int) -> int | None:
    """Return the byte offset just after the balancing brace.

    This lexical scanner ignores comments and string/template/regex literals.
    It is used only to select bytes; failure produces an uncertainty rather
    than guessed source.
    """
    depth = 0
    i = opening
    state = "normal"
    escaped = False
    regex_class = False
    previous_sig = b""
    while i < len(data):
        c = data[i:i + 1]
        n = data[i + 1:i + 2]
        if state == "line_comment":
            if c in (b"\r", b"\n"):
                state = "normal"
            i += 1
            continue
        if state == "block_comment":
            if c == b"*" and n == b"/":
                state = "normal"; i += 2; continue
            i += 1; continue
        if state in ("single", "double", "template"):
            quote = {"single": b"'", "double": b'"', "template": b"`"}[state]
            if escaped:
                escaped = False
            elif c == b"\\":
                escaped = True
            elif c == quote:
                state = "normal"
            i += 1; continue
        if state == "regex":
            if escaped:
                escaped = False
            elif c == b"\\":
                escaped = True
            elif c == b"[":
                regex_class = True
            elif c == b"]":
                regex_class = False
            elif c == b"/" and not regex_class:
                state = "normal"
            i += 1; continue
        if c == b"/" and n == b"/":
            state = "line_comment"; i += 2; continue
        if c == b"/" and n == b"*":
            state = "block_comment"; i += 2; continue
        if c == b"'": state = "single"; i += 1; continue
        if c == b'"': state = "double"; i += 1; continue
        if c == b"`": state = "template"; i += 1; continue
        if c == b"/" and (not previous_sig or previous_sig[-1:] in b"=(:,![{;?&|" or previous_sig.endswith((b"return", b"case", b"=>"))):
            state = "regex"; regex_class = False; i += 1; continue
        if c == b"{":
            depth += 1
        elif c == b"}":
            depth -= 1
            if depth == 0:
                return i + 1
        if c not in b" \t\r\n":
            previous_sig = (previous_sig + c)[-12:]
        i += 1
    return None


def line_end_after(data: bytes, offset: int) -> int:
    newline = data.find(b"\n", offset)
    return len(data) if newline < 0 else newline + 1


def component_ranges(content: bytes) -> tuple[list[dict[str, Any]], list[str]]:
    components: list[dict[str, Any]] = []
    failures: list[str] = []
    class_pattern = re.compile(br"(?m)^[ \t]*class[ \t]+([A-Za-z_$][\w$]*)(?:[ \t\r\n]+extends[ \t\r\n]+[A-Za-z_$][\w$]*)?[ \t\r\n]*\{")
    for match in class_pattern.finditer(content):
        opening = content.find(b"{", match.start(), match.end())
        end = brace_end(content, opening)
        name = match.group(1).decode()
        if end is None:
            failures.append(f"class {name}: balancing brace not recoverable")
            continue
        components.append({"start": match.start(), "end": line_end_after(content, end), "kind": "class", "symbol": name})

    config_pattern = re.compile(br"(?m)^[ \t]*const[ \t]+(CONFIG|CONFIGURATION|DEFAULTS|LIMITS)[ \t]*=[ \t]*\{")
    for match in config_pattern.finditer(content):
        opening = content.find(b"{", match.start(), match.end())
        end = brace_end(content, opening)
        name = match.group(1).decode()
        if end is None:
            failures.append(f"configuration {name}: balancing brace not recoverable")
            continue
        components.append({"start": match.start(), "end": line_end_after(content, end), "kind": "configuration", "symbol": name})

    # UI is source-delimited by a section heading comment. Extract only when a
    # clear heading and a mechanically determinable next section/end exist.
    ui_pattern = re.compile(br"(?mi)^[ \t]*//[ \t]*(?:USER[ \t]+INTERFACE|UI)(?:[ \t]*/[^\r\n]*)?[ \t]*\r?$", re.M)
    section_pattern = re.compile(br"(?mi)^[ \t]*//[ \t]*([A-Z][A-Z0-9 /&_-]{1,60})[ \t]*\r?$", re.M)
    for match in ui_pattern.finditer(content):
        start = match.start()
        # Include an immediately preceding separator line.
        prior_line_start = content.rfind(b"\n", 0, max(0, start - 1)) + 1
        prior_prior = content.rfind(b"\n", 0, max(0, prior_line_start - 1)) + 1
        prior = content[prior_prior:prior_line_start].strip()
        if prior and set(prior.replace(b"//", b"").strip()) <= {ord("=")}:
            start = prior_prior
        candidates = [x.start() for x in section_pattern.finditer(content, match.end())]
        end = candidates[0] if candidates else len(content)
        if end > start:
            components.append({"start": start, "end": end, "kind": "ui_section", "symbol": "UI"})

    # Prevent duplicate component ranges caused by permissive patterns.
    unique = {}
    for item in components:
        unique[(item["start"], item["end"], item["kind"], item["symbol"])] = item
    return sorted(unique.values(), key=lambda x: (x["start"], x["end"])), failures


def artifact_id(revision: str, start: int | None, end: int | None, method: str, extra: str = "") -> str:
    material = f"{revision}:{start}:{end}:{method}:{extra}".encode()
    return "art-" + sha256(material)[:16]


def make_source_record(rev: dict[str, Any], struct: dict[str, Any], start: int, end: int,
                       start_i: int, end_i: int, method: str, label: str,
                       detection_id: str, complete_userscript: bool = False,
                       parent: str | None = None, nested_kind: str | None = None,
                       nested_symbol: str | None = None, content: bytes | None = None) -> dict[str, Any]:
    if content is None:
        content = rev["data"][start:end]
    context = context_for(struct, start_i, end_i)
    info = classify(content, label, context, method, complete_userscript, nested_kind, nested_symbol)
    version = explicit_version(content)
    version_status = "EXPLICIT" if version else None
    if not version:
        version, version_status = infer_version(struct, start_i, context)
    aid = artifact_id(rev["revision"], start, end, method, nested_symbol or "")
    source_line_start = line_for_offset(struct["starts"], start)
    source_line_end = line_for_offset(struct["starts"], max(start, end - 1))
    record = {
        "artifact_id": aid,
        "artifact_type": info["artifact_type"],
        "short_name": info["short_name"],
        "language": info["language"],
        "classification": info["classification"],
        "secondary_classification": info["secondary_classification"],
        "status": info["status"],
        "verification": info["verification"],
        "derived": False,
        "incomplete": info["incomplete"],
        "symbol": info["symbol"],
        "symbol_kind": info["symbol_kind"],
        "source": {
            "document": rev["document"],
            "path": rev["path"],
            "revision": rev["revision"],
            "commit": rev["commit"],
            "branch": rev["branch"],
            "branches_observed": rev["branches_observed"],
            "occurrences": rev["occurrences"],
            "tag": None,
            "author": rev["author"],
            "timestamp": rev["timestamp"],
            "parent_revision": rev["parent_revision"],
            "heading": context["section_title"],
            "position": f"lines {source_line_start}-{source_line_end}; bytes {start}-{end - 1}",
            "line_start": source_line_start,
            "line_end": source_line_end,
            "byte_start": start,
            "byte_end_exclusive": end,
            "fence_label": label,
            "extraction_method": method,
            "detection_id": detection_id,
        },
        "history": {
            "version": version if version else "UNKNOWN",
            "version_status": version_status,
            "chronology": "KNOWN_COMMIT; EMBEDDED_ORDER_INFERRED" if version_status != "UNKNOWN" else "KNOWN_COMMIT; ARTIFACT_VERSION_UNKNOWN",
        },
        "integrity": {
            "encoding": "UTF-8",
            "bom": content.startswith(b"\xef\xbb\xbf"),
            "newline_style": line_ending(content),
            "size_bytes": len(content),
            "sha256": sha256(content),
        },
        "context": context,
        "dependencies": dependencies(content, info["symbol"]),
        "relationships": [],
        "parent_artifact": parent,
        "logical_key": ("userscript:generic-discovery" if info["artifact_type"] == "userscript" else f"{info['symbol_kind']}:{info['symbol']}" if info["symbol"] else None),
        "concurrency": concurrency_record(content, context),
        "_content": content,
        "_revision_order": rev["order"],
    }
    if parent:
        record["relationships"].append({"type": "partial_of", "target": parent, "evidence": "mechanically nested source range"})
    return record


def provider_subdir(record: dict[str, Any]) -> str:
    value = ((record.get("symbol") or "") + " " + record.get("short_name", "")).lower()
    if "html" in value: return "html"
    if "json" in value: return "json"
    if "text" in value: return "text"
    return "other"


def output_category(record: dict[str, Any]) -> str:
    kind = record["artifact_type"]
    mapping = {
        "userscript": "userscript", "engine": "engine", "model": "models",
        "scheduler": "scheduler", "acquisition": "acquisition", "ui": "ui",
        "test": "tests", "configuration": "configuration", "schema": "configuration/schema",
        "patch": "patches", "pseudocode": "pseudocode", "fragment": "fragments",
    }
    if kind == "provider":
        return "providers/" + provider_subdir(record)
    return mapping.get(kind, "fragments")


def extension(record: dict[str, Any]) -> str:
    return {
        "javascript": "js", "typescript": "ts", "json": "json", "yaml": "yaml",
        "shell": "sh", "rust": "rs", "html": "html", "xml": "xml",
        "http": "http", "diff": "diff", "mermaid": "mmd", "text": "txt",
    }.get(record["language"], "txt")


def add_relationship(records_by_id: dict[str, dict[str, Any]], relationships: list[dict[str, Any]],
                     source: str, relation_type: str, target: str, evidence: str) -> None:
    relation = {"from": source, "type": relation_type, "to": target, "evidence": evidence}
    if relation not in relationships:
        relationships.append(relation)
    local = {"type": relation_type, "target": target, "evidence": evidence}
    if local not in records_by_id[source]["relationships"]:
        records_by_id[source]["relationships"].append(local)


def symbol_set(content: bytes) -> set[str]:
    text = decode(content)
    return set(re.findall(r"(?m)^\s*(?:class|function|const|let|var)\s+([A-Za-z_$][\w$]*)", text))


def token_counts(text: str, tokens: list[str]) -> dict[str, int]:
    return {token: len(re.findall(r"(?<![\w$])" + re.escape(token) + r"(?![\w$])", text, re.I)) for token in tokens}


def configuration_literals(text: str) -> dict[str, str]:
    """Observe simple key/literal pairs without evaluating JavaScript."""
    values: dict[str, str] = {}
    for match in re.finditer(
        r"(?m)^\s*([A-Za-z_$][\w$]*)\s*:\s*"
        r"(true|false|null|-?\d+(?:\.\d+)?|'[^'\r\n]*'|\"[^\"\r\n]*\")\s*,?\s*$",
        text,
    ):
        values.setdefault(match.group(1), match.group(2))
    return values


def configuration_profile(content: bytes) -> dict[str, str]:
    """Read simple literals only from mechanically bounded CONFIG objects."""
    values: dict[str, str] = {}
    pattern = re.compile(br"(?m)^[ \t]*const[ \t]+(?:CONFIG|CONFIGURATION)[ \t]*=[ \t]*\{")
    for match in pattern.finditer(content):
        opening = content.find(b"{", match.start(), match.end())
        end = brace_end(content, opening)
        if end is not None:
            values.update(configuration_literals(decode(content[opening:end])))
    return values


def mechanical_profile(content: bytes) -> dict[str, Any]:
    text = decode(content)
    symbols = symbol_set(content)
    return {
        "api_symbols": sorted(symbols),
        "data_fields": sorted(set(re.findall(r"\bthis\.([A-Za-z_$][\w$]*)\s*=", text))),
        "control_flow_tokens": token_counts(text, ["if", "for", "while", "switch", "await", "return"]),
        "scheduler_tokens": token_counts(text, ["Scheduler", "queue", "priority", "claimNextCandidate", "frontier"]),
        "concurrency_tokens": token_counts(text, ["worker", "claimed", "Promise", "await", "lease", "fencing"]),
        "acquisition_tokens": token_counts(text, ["Acquisition", "GM_xmlhttpRequest", "fetch", "XMLHttpRequest", "response"]),
        "provider_symbols": sorted(x for x in symbols if re.search(r"(?:Provider|Recognizer|CandidateSource)$", x)),
        "discovery_tokens": token_counts(text, ["Candidate", "Observation", "Discovery", "KnowledgeBase", "recognize", "expand"]),
        "ui_tokens": token_counts(text, ["document.createElement", "innerHTML", "addEventListener", "updateUI"]),
        "storage_tokens": token_counts(text, ["GM_getValue", "GM_setValue", "localStorage", "IndexedDB"]),
        "error_tokens": token_counts(text, ["try", "catch", "throw", "error", "timeout"]),
        "security_tokens": token_counts(text, ["sameOrigin", "allowedOrigin", "canonicalUrl", "protocol", "authorization"]),
        "configuration_literals": configuration_profile(content),
    }


def profile_delta(old: dict[str, Any], new: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key in ("api_symbols", "data_fields", "provider_symbols"):
        before, after = set(old[key]), set(new[key])
        result[key] = {"added": sorted(after - before), "removed": sorted(before - after)}
    for key in (
        "control_flow_tokens", "scheduler_tokens", "concurrency_tokens",
        "acquisition_tokens", "discovery_tokens", "ui_tokens", "storage_tokens",
        "error_tokens", "security_tokens",
    ):
        keys = sorted(set(old[key]) | set(new[key]))
        result[key] = {
            token: {"from": old[key].get(token, 0), "to": new[key].get(token, 0)}
            for token in keys if old[key].get(token, 0) != new[key].get(token, 0)
        }
    old_config, new_config = old["configuration_literals"], new["configuration_literals"]
    result["configuration_literals"] = {
        "added": {k: new_config[k] for k in sorted(set(new_config) - set(old_config))},
        "removed": {k: old_config[k] for k in sorted(set(old_config) - set(new_config))},
        "modified": {
            k: {"from": old_config[k], "to": new_config[k]}
            for k in sorted(set(old_config) & set(new_config))
            if old_config[k] != new_config[k]
        },
    }
    result["interpretation"] = "MECHANICAL_TOKEN_AND_LITERAL_COMPARISON_ONLY"
    return result


def change_record(parent: dict[str, Any], child: dict[str, Any]) -> dict[str, Any]:
    a = decode(parent["_content"]).splitlines()
    b = decode(child["_content"]).splitlines()
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    added = removed = replaced = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "insert": added += j2 - j1
        elif tag == "delete": removed += i2 - i1
        elif tag == "replace":
            removed += i2 - i1; added += j2 - j1; replaced += 1
    old_symbols, new_symbols = symbol_set(parent["_content"]), symbol_set(child["_content"])
    modifications = []
    if parent["integrity"]["sha256"] != child["integrity"]["sha256"]:
        modifications.append("artifact bytes changed")
    if parent["history"]["version"] != child["history"]["version"]:
        modifications.append(f"explicit/inferred version {parent['history']['version']} -> {child['history']['version']}")
    return {
        "from": parent["artifact_id"],
        "to": child["artifact_id"],
        "additions": sorted(new_symbols - old_symbols),
        "removals": sorted(old_symbols - new_symbols),
        "modifications": modifications,
        "renamed_symbols": [],
        "behavior_changes": [],
        "uncertain_changes": ["Behavior was not executed or semantically verified."],
        "mechanical_line_diff": {
            "added_lines": added, "removed_lines": removed,
            "replace_hunks": replaced, "sequence_similarity": round(sm.ratio(), 6),
        },
        "cross_version_dimensions": profile_delta(
            mechanical_profile(parent["_content"]),
            mechanical_profile(child["_content"]),
        ),
    }


def fields_for_model(content: bytes) -> list[str]:
    return sorted(set(re.findall(r"\bthis\.([A-Za-z_$][\w$]*)\s*=", decode(content))))


def clean_generated() -> None:
    for name in ("raw", "artifacts", "reconstructed"):
        path = OUT / name
        if path.exists(): shutil.rmtree(path)
    for name in (
        "README.md", "SOURCE-MANIFEST.yaml", "SOURCE-MAP.md", "ARTIFACT-INDEX.yaml",
        "LINEAGE.yaml", "DUPLICATES.yaml", "NEAR-DUPLICATES.yaml", "CHANGES.yaml",
        "FIELD-HISTORY.yaml", "REVISION-INVENTORY.yaml", "DETECTION-INVENTORY.yaml",
        "CONTRADICTIONS.md", "UNCERTAINTIES.md", "EXTRACTION-REPORT.md", "VALIDATION.yaml",
    ):
        path = OUT / name
        if path.exists(): path.unlink()


def write_json_yaml(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    clean_generated()
    generated_at = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    artifacts: list[dict[str, Any]] = []
    detections: list[dict[str, Any]] = []
    revision_inventory = []
    structures: dict[str, dict[str, Any]] = {}
    extraction_uncertainties: list[dict[str, Any]] = []

    # PHASES 1-3: pin revisions, preserve raw blobs, parse structure/detections.
    for spec in REVISIONS:
        rev = dict(spec)
        data = git_blob(rev["revision"])
        rev["data"] = data
        struct = source_structure(data)
        structures[rev["revision"]] = struct
        raw_slug = slug(rev["document"].removesuffix(".md"))
        raw_name = f"{rev['timestamp'][:10].replace('-', '')}__{rev['revision'][:12]}__{Path(rev['path']).name}"
        raw_rel = Path("raw") / raw_slug / raw_name
        raw_path = OUT / raw_rel
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        raw_path.write_bytes(data)
        revision_inventory.append({
            **{k: v for k, v in rev.items() if k != "data"},
            "raw_file": str(raw_rel),
            "integrity": {
                "encoding": "UTF-8", "bom": data.startswith(b"\xef\xbb\xbf"),
                "newline_style": line_ending(data), "size_bytes": len(data), "sha256": sha256(data),
            },
            "structure": {
                "line_count": len(struct["lines"]), "fenced_regions": len(struct["fences"]),
                "unclosed_fence": struct["unclosed_fence"],
            },
        })
        if struct["unclosed_fence"]:
            extraction_uncertainties.append({"label": "UNCERTAIN", "revision": rev["revision"], "issue": f"unclosed fence at line {struct['unclosed_fence']}"})

        # Explicit fenced regions.
        for number, fence in enumerate(struct["fences"], 1):
            did = "det-" + sha256(f"{rev['revision']}:fence:{fence['open_i']}".encode())[:16]
            parent = None
            record = make_source_record(
                rev, struct, fence["start"], fence["end"], fence["open_i"] + 1,
                fence["close_i"], "fenced_block", fence["label"], did,
                complete_userscript=b"==UserScript==" in fence["content"], parent=parent,
            )
            artifacts.append(record)
            detections.append({
                "detection_id": did, "source_revision": rev["revision"], "kind": "fenced_block",
                "position": f"opening line {fence['open_i'] + 1}, content lines {fence['open_i'] + 2}-{fence['close_i']}",
                "artifact_id": record["artifact_id"], "status": "extracted",
            })

        # Complete userscripts whose metadata header lies outside a fence.
        outside_scripts: list[tuple[int, int]] = []
        lines, starts = struct["lines"], struct["starts"]
        i = 0
        while i < len(lines):
            if struct["outside"][i] and b"// ==UserScript==" in lines[i]:
                start_i = i
                end_i = None
                j = i
                while j < len(lines):
                    if j > i and struct["outside"][j] and b"// ==UserScript==" in lines[j]:
                        break
                    if struct["outside"][j] and b"})();" in lines[j]:
                        end_i = j + 1
                        break
                    if j > i and struct["outside"][j] and lines[j].decode("utf-8", errors="replace").rstrip("\r\n") in ("**You:**", "**ChatGPT:**"):
                        break
                    j += 1
                if end_i is None:
                    extraction_uncertainties.append({"label": "UNCERTAIN", "revision": rev["revision"], "issue": f"outside userscript at line {i + 1} has no mechanically recoverable closure"})
                else:
                    start, end = starts[start_i], starts[end_i]
                    did = "det-" + sha256(f"{rev['revision']}:outside-userscript:{start}".encode())[:16]
                    record = make_source_record(rev, struct, start, end, start_i, end_i,
                                                "outside_userscript", "", did, True)
                    record["format_anomalies"] = [
                        "userscript crosses Markdown fence boundaries or is flattened in source",
                        "preserved exactly; not repaired",
                    ]
                    artifacts.append(record)
                    detections.append({
                        "detection_id": did, "source_revision": rev["revision"], "kind": "outside_userscript",
                        "position": f"lines {start_i + 1}-{end_i}", "artifact_id": record["artifact_id"], "status": "extracted",
                    })
                    outside_scripts.append((start, end))
                    i = end_i
                    continue
            i += 1

        # Independently meaningful lines consisting solely of one inline span.
        inline_re = re.compile(br"^[ \t]*`([^`\r\n]+)`[,.;:]?[ \t]*\r?\n?$")
        for line_i, line in enumerate(lines):
            if not struct["outside"][line_i]:
                continue
            match = inline_re.match(line)
            if not match:
                continue
            content = match.group(1)
            start = starts[line_i] + match.start(1)
            end = starts[line_i] + match.end(1)
            did = "det-" + sha256(f"{rev['revision']}:inline:{start}".encode())[:16]
            record = make_source_record(rev, struct, start, end, line_i, line_i + 1,
                                        "inline_fragment", "inline", did, content=content)
            artifacts.append(record)
            detections.append({
                "detection_id": did, "source_revision": rev["revision"], "kind": "inline_fragment",
                "position": f"line {line_i + 1}, byte columns {match.start(1) + 1}-{match.end(1)}",
                "artifact_id": record["artifact_id"], "status": "extracted",
            })

    # Parent fenced bodies that sit inside outside-userscript source ranges.
    by_revision = defaultdict(list)
    for record in artifacts:
        by_revision[record["source"]["revision"]].append(record)
    for records in by_revision.values():
        outside = [x for x in records if x["source"]["extraction_method"] == "outside_userscript"]
        fenced = [x for x in records if x["source"]["extraction_method"] == "fenced_block"]
        for child in fenced:
            for parent in outside:
                if parent["source"]["byte_start"] < child["source"]["byte_start"] and child["source"]["byte_end_exclusive"] < parent["source"]["byte_end_exclusive"]:
                    child["parent_artifact"] = parent["artifact_id"]
                    child["relationships"].append({"type": "partial_of", "target": parent["artifact_id"], "evidence": "fenced implementation body lies inside userscript source interval"})
                    child["classification"] = "PARTIAL_IMPLEMENTATION"
                    child["status"] = "PARTIAL_IMPLEMENTATION"
                    break

    # PHASES 4-6: exact nested class/config/UI slices from complete userscripts.
    complete_userscripts = [x for x in artifacts if x["artifact_type"] == "userscript"]
    for parent in list(complete_userscripts):
        rev = next(x for x in REVISIONS if x["revision"] == parent["source"]["revision"])
        rev = {**rev, "data": git_blob(rev["revision"])}
        struct = structures[rev["revision"]]
        ranges, failures = component_ranges(parent["_content"])
        for failure in failures:
            extraction_uncertainties.append({"label": "UNCERTAIN", "artifact_id": parent["artifact_id"], "issue": failure})
        for component in ranges:
            start = parent["source"]["byte_start"] + component["start"]
            end = parent["source"]["byte_start"] + component["end"]
            start_i = line_for_offset(struct["starts"], start) - 1
            end_i = line_for_offset(struct["starts"], max(start, end - 1))
            method = "nested_" + component["kind"]
            did = "component-" + sha256(f"{rev['revision']}:{start}:{end}:{component['kind']}".encode())[:16]
            record = make_source_record(
                rev, struct, start, end, start_i, end_i, method, "JavaScript", did,
                parent=parent["artifact_id"], nested_kind=component["kind"],
                nested_symbol=component["symbol"], content=parent["_content"][component["start"]:component["end"]],
            )
            record["history"] = dict(parent["history"])
            record["logical_key"] = f"{component['kind']}:{component['symbol']}"
            record["context"]["parent_explanatory_context"] = {
                "preceding_text": parent["context"]["preceding_text"],
                "following_text": parent["context"]["following_text"],
                "section_title": parent["context"]["section_title"],
                "parent_artifact": parent["artifact_id"],
            }
            artifacts.append(record)

    # Mechanical reconstructions for two source-split scripts. No guessed text.
    reconstructed: list[dict[str, Any]] = []
    base_rev = next(x for x in REVISIONS if x["order"] == 0)
    base_data = git_blob(base_rev["revision"])
    base_struct = structures[base_rev["revision"]]
    reconstruction_specs = [
        {"version": "0.1.0", "ranges": [(1942, 1956), (1958, 1961 + (2961 - 1958 + 1)), (2963, 2964)]},
        {"version": "0.2.0", "ranges": [(3047, 3061), (3063, 4708), (4710, 4711)]},
    ]
    # Correct the intentionally explicit line ranges (inclusive).
    reconstruction_specs[0]["ranges"] = [(1942, 1956), (1958, 2961), (2963, 2964)]
    for spec in reconstruction_specs:
        parts = []
        part_positions = []
        for first, last in spec["ranges"]:
            start, end = base_struct["starts"][first - 1], base_struct["starts"][last]
            parts.append(base_data[start:end])
            part_positions.append(f"lines {first}-{last}")
        content = b"".join(parts)
        parent = next(x for x in artifacts if x["source"]["revision"] == base_rev["revision"] and x["artifact_type"] == "userscript" and x["history"]["version"] == spec["version"])
        aid = "rec-" + sha256((parent["artifact_id"] + ":mechanical-fence-removal").encode())[:16]
        record = {
            "artifact_id": aid, "artifact_type": "reconstructed",
            "short_name": f"generic-discovery-v{spec['version'].replace('.', '-')}",
            "language": "javascript", "classification": "PARTIAL_IMPLEMENTATION",
            "secondary_classification": "USERSCRIPT", "status": "UNVERIFIED",
            "verification": "UNVERIFIED", "derived": True, "incomplete": False,
            "symbol": None, "symbol_kind": None,
            "source": {
                "document": base_rev["document"], "path": base_rev["path"],
                "revision": base_rev["revision"], "commit": base_rev["commit"],
                "branch": base_rev["branch"], "branches_observed": base_rev["branches_observed"],
                "occurrences": base_rev["occurrences"],
                "tag": None, "author": base_rev["author"], "timestamp": base_rev["timestamp"],
                "parent_revision": None, "heading": parent["source"]["heading"],
                "position": "composite: " + ", ".join(part_positions),
                "line_start": None, "line_end": None, "byte_start": None,
                "byte_end_exclusive": None, "fence_label": None,
                "extraction_method": "mechanical_reconstruction",
                "detection_id": None,
            },
            "history": dict(parent["history"]),
            "integrity": {"encoding": "UTF-8", "bom": False, "newline_style": line_ending(content), "size_bytes": len(content), "sha256": sha256(content)},
            "context": dict(parent["context"]), "dependencies": dependencies(content, None),
            "relationships": [{"type": "reconstructed_from", "target": parent["artifact_id"], "evidence": "listed source ranges concatenated in source order"}],
            "parent_artifact": None, "logical_key": "reconstructed:generic-discovery",
            "concurrency": concurrency_record(content, parent["context"]),
            "reconstruction": {
                "source_artifacts": [parent["artifact_id"]],
                "source_ranges": part_positions,
                "reconstruction_method": "mechanical concatenation after excluding Markdown fence delimiter lines",
                "semantic_inference": False,
                "authoritative": False,
            },
            "_content": content, "_revision_order": 99,
        }
        reconstructed.append(record)
    artifacts.extend(reconstructed)

    # Assign stable chronology and deterministic output paths.
    method_rank = {"outside_userscript": 0, "fenced_block": 1, "nested_class": 2, "nested_configuration": 2, "nested_ui_section": 2, "inline_fragment": 3, "mechanical_reconstruction": 9}
    artifacts.sort(key=lambda x: (
        x["_revision_order"],
        x["source"]["byte_start"] if x["source"]["byte_start"] is not None else 10**12,
        method_rank.get(x["source"]["extraction_method"], 5),
        x["artifact_id"],
    ))
    for index, record in enumerate(artifacts, 1):
        record["chronology_index"] = index
        if record["derived"]:
            rel = Path("reconstructed") / f"{index:06d}__reconstructed__{record['short_name']}__{record['artifact_id']}.js"
        else:
            rel = Path("artifacts") / output_category(record) / f"{index:06d}__{record['artifact_type']}__{record['short_name']}__{record['artifact_id']}.{extension(record)}"
        record["output_file"] = str(rel)
        destination = OUT / rel
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(record["_content"])

    records_by_id = {x["artifact_id"]: x for x in artifacts}
    relationships: list[dict[str, Any]] = []
    for record in artifacts:
        for relation in record["relationships"]:
            relationships.append({"from": record["artifact_id"], "type": relation["type"], "to": relation["target"], "evidence": relation["evidence"]})

    # PHASE 8: exact duplicates, retained rather than removed.
    hash_groups = defaultdict(list)
    for record in artifacts:
        if not record["derived"]:
            hash_groups[record["integrity"]["sha256"]].append(record)
    duplicate_groups = []
    for digest, group in sorted(hash_groups.items()):
        if len(group) < 2:
            continue
        group.sort(key=lambda x: x["chronology_index"])
        canonical = group[0]
        gid = "dup-" + digest[:16]
        group_record = {
            "id": gid, "sha256": digest,
            "canonical_artifact": canonical["artifact_id"],
            "selection_basis": "earliest chronology/provenance index",
            "identical_artifacts": [x["artifact_id"] for x in group],
        }
        duplicate_groups.append(group_record)
        for member in group:
            member["duplicate_group"] = {
                "id": gid,
                "canonical_artifact": canonical["artifact_id"],
                "identical_artifacts": group_record["identical_artifacts"],
            }
        for duplicate in group[1:]:
            add_relationship(records_by_id, relationships, duplicate["artifact_id"], "duplicate_of", canonical["artifact_id"], f"identical SHA-256; {gid}")

    # PHASES 9-11: conservative userscript/component lineage and comparisons.
    original_userscripts = [x for x in artifacts if not x["derived"] and x["artifact_type"] == "userscript" and x["_revision_order"] in (0, 1)]
    user_by_doc_line = {(x["source"]["document"], x["source"]["line_start"]): x for x in original_userscripts}
    lineage_specs = [
        ("Userscript Discovery Prototype.md", 3047, 1942, "evolved_from", "source calls v0.2.0 the revised version after requested fixes"),
        ("Continue Architecture Planning.md", 11, 3, "unknown_relation", "same pasted pair; formatting loss prevents exact identity claim"),
        # Fenced artifact positions begin on the first content line (one line
        # after the opening fence), which is the line stored in provenance.
        ("Continue Architecture Planning.md", 53, 11, "evolved_from", "preceding prose explicitly says v0.3.0 is based on v0.2.0"),
        ("Continue Architecture Planning.md", 2792, 53, "evolved_from", "preceding prose explicitly says v0.4.0 builds directly on v0.3.0"),
        ("Continue Architecture Planning.md", 7178, 2792, "evolved_from", "preceding prose says continuing with v0.5.0"),
        ("Continue Architecture Planning.md", 13487, 53, "evolved_from", "preceding prose says v0.4.0 continues from v0.3.0"),
        ("Continue Architecture Planning.md", 18379, 13487, "evolved_from", "preceding planning and continuation identify the next v0.5.0"),
        ("Continue Architecture Planning.md", 23141, 18379, "evolved_from", "preceding prose says continuing with v0.6.0"),
        ("Continue Architecture Planning.md", 29439, 18379, "unknown_relation", "repeated v0.5.0 appears after v0.6.0; parent is ambiguous"),
        ("Continue Architecture Planning.md", 34755, 29439, "evolved_from", "preceding prose says continuing to v0.6.0"),
        ("Continue Architecture Planning.md", 43196, 34755, "evolved_from", "preceding prose says this v0.6.0 keeps the discovery architecture intact"),
        ("Continue Architecture Planning.md", 48949, 43196, "evolved_from", "v0.7.1 prose says it strengthens the existing v0.6 control plane"),
    ]
    evolved_edges: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for document, child_line, parent_line, relation_type, evidence in lineage_specs:
        child = user_by_doc_line.get((document, child_line))
        parent = user_by_doc_line.get((document, parent_line))
        if child and parent:
            add_relationship(records_by_id, relationships, child["artifact_id"], relation_type, parent["artifact_id"], evidence)
            if relation_type == "evolved_from": evolved_edges.append((parent, child))

    # Cross-document transformed copies are conservatively unknown.
    for version, user_line, continue_line in (("0.1.0", 1942, 3), ("0.2.0", 3047, 11)):
        source = user_by_doc_line.get(("Userscript Discovery Prototype.md", user_line))
        copied = user_by_doc_line.get(("Continue Architecture Planning.md", continue_line))
        if source and copied:
            add_relationship(records_by_id, relationships, copied["artifact_id"], "unknown_relation", source["artifact_id"], f"appears to be transformed paste of v{version}; bytes differ and whitespace was lost")

    # Propagate proved parent-script evolution to same-named nested components.
    children_by_parent = defaultdict(list)
    for record in artifacts:
        if record.get("parent_artifact"):
            children_by_parent[record["parent_artifact"]].append(record)
    for parent_script, child_script in list(evolved_edges):
        old = {x["logical_key"]: x for x in children_by_parent[parent_script["artifact_id"]] if x["logical_key"]}
        new = {x["logical_key"]: x for x in children_by_parent[child_script["artifact_id"]] if x["logical_key"]}
        for key in sorted(set(old) & set(new)):
            if old[key]["integrity"]["sha256"] == new[key]["integrity"]["sha256"]:
                continue
            add_relationship(records_by_id, relationships, new[key]["artifact_id"], "evolved_from", old[key]["artifact_id"], f"same mechanically extracted component in userscript lineage: {key}")
            evolved_edges.append((old[key], new[key]))

    # Near duplicates are similarity observations only; no unsupported lineage.
    families = defaultdict(list)
    for record in artifacts:
        if record["derived"] or record["_revision_order"] not in (0, 1) or not record["logical_key"]:
            continue
        families[record["logical_key"]].append(record)
    near_duplicates = []
    for key, family in sorted(families.items()):
        unique = []
        seen_hashes = set()
        for record in sorted(family, key=lambda x: x["chronology_index"]):
            if record["integrity"]["sha256"] not in seen_hashes:
                unique.append(record); seen_hashes.add(record["integrity"]["sha256"])
        for old, new in zip(unique, unique[1:]):
            a, b = decode(old["_content"]).splitlines(), decode(new["_content"]).splitlines()
            length_ratio = min(len(a), len(b)) / max(1, max(len(a), len(b)))
            if length_ratio < 0.35:
                continue
            ratio = difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()
            if ratio >= 0.45:
                near_duplicates.append({
                    "family": key, "artifact_a": old["artifact_id"], "artifact_b": new["artifact_id"],
                    "line_similarity": round(ratio, 6), "relationship": "unknown_relation",
                    "note": "mechanical similarity only; source artifacts remain separate",
                })

    changes = [change_record(parent, child) for parent, child in evolved_edges]

    evolution_groups = []
    grouped_edges = defaultdict(list)
    for parent, child in evolved_edges:
        key = child["logical_key"] or child["artifact_type"]
        grouped_edges[key].append({"from": parent["artifact_id"], "to": child["artifact_id"]})
    for key, edges in sorted(grouped_edges.items()):
        evolution_groups.append({"id": "evo-" + sha256(key.encode())[:12], "family": key, "edges": edges})

    # Field evolution is purely assignment-set comparison along proved model edges.
    field_histories = []
    for parent, child in evolved_edges:
        if parent["artifact_type"] != "model" or child["artifact_type"] != "model":
            continue
        old_fields, new_fields = set(fields_for_model(parent["_content"])), set(fields_for_model(child["_content"]))
        field_histories.append({
            "model": child["symbol"], "from": parent["artifact_id"], "to": child["artifact_id"],
            "introduced_fields": sorted(new_fields - old_fields), "removed_fields": sorted(old_fields - new_fields),
            "retained_fields": sorted(old_fields & new_fields), "renamed_fields": [],
            "type_changes": [], "note": "renames and type changes are UNKNOWN unless explicit; none inferred",
        })

    # Assign format anomaly/incompleteness notes and update parent relation list in lineage.
    for record in artifacts:
        if record.get("format_anomalies"):
            record["incomplete"] = True

    # Contradictions and uncertainties: evidence registers, not repairs.
    def aid(document: str, line: int) -> str:
        item = user_by_doc_line.get((document, line))
        return item["artifact_id"] if item else "NOT_AVAILABLE"

    contradictions = [
        {
            "id": "CONTRADICTION-001", "label": "SUPPORTED",
            "summary": "The source calls the early userscripts self-contained/revised, but Markdown fence delimiters split their implementation bodies.",
            "evidence": [f"Userscript Discovery Prototype.md:1940-2964 ({aid('Userscript Discovery Prototype.md', 1942)})", f"Userscript Discovery Prototype.md:3045-4711 ({aid('Userscript Discovery Prototype.md', 3047)})", "Continue Architecture Planning.md:36 explicitly calls stray backticks invalid JavaScript"],
            "resolution": "NOT_RESOLVED",
        },
        {
            "id": "CONTRADICTION-002", "label": "PROVED",
            "summary": "Document order regresses from a complete v0.5.0 userscript to another complete v0.4.0 userscript.",
            "evidence": [f"Continue Architecture Planning.md:7177-7178 ({aid('Continue Architecture Planning.md', 7178)})", f"Continue Architecture Planning.md:13486-13487 ({aid('Continue Architecture Planning.md', 13487)})"],
            "resolution": "NOT_RESOLVED",
        },
        {
            "id": "CONTRADICTION-003", "label": "PROVED",
            "summary": "Document order regresses from a complete v0.6.0 userscript to another complete v0.5.0 userscript.",
            "evidence": [f"Continue Architecture Planning.md:23140-23141 ({aid('Continue Architecture Planning.md', 23141)})", f"Continue Architecture Planning.md:29438-29439 ({aid('Continue Architecture Planning.md', 29439)})"],
            "resolution": "NOT_RESOLVED",
        },
        {
            "id": "CONTRADICTION-004", "label": "PROVED",
            "summary": "The same explicit version labels identify byte-distinct complete userscripts.",
            "evidence": ["v0.4.0 at lines 2791 and 13486", "v0.5.0 at lines 7177, 18378, and 29438", "v0.6.0 at lines 23140, 34754, and 43195"],
            "resolution": "NOT_RESOLVED; all variants retained",
        },
    ]
    uncertainties = [
        {"id": "UNCERTAINTY-001", "label": "UNKNOWN", "issue": "Pre-Git creation dates, authorship per chat turn, and revisions before the initial upload are not available.", "effect": "Embedded chronology has no date finer than its containing Git revision."},
        {"id": "UNCERTAINTY-002", "label": "PROVED", "issue": "No Git tags exist in the fetched repository.", "effect": "No artifact can be assigned a tag."},
        {"id": "UNCERTAINTY-003", "label": "SUPPORTED", "issue": "The first two scripts in Continue Architecture Planning.md are flattened across extremely long lines.", "effect": "Component boundaries and original whitespace are NOT_RECOVERABLE; only the represented bytes were extracted."},
        {"id": "UNCERTAINTY-004", "label": "PROVED", "issue": "Most fences are unlabeled.", "effect": "Language classifications for unlabeled blocks are mechanical inferences; raw bytes are unaffected."},
        {"id": "UNCERTAINTY-005", "label": "UNKNOWN", "issue": "No historical artifact has execution evidence in the two source documents sufficient for this extraction.", "effect": "Verification remains UNVERIFIED even when prose calls a userscript complete."},
        {"id": "UNCERTAINTY-006", "label": "UNCERTAIN", "issue": "Repeated and regressing explicit versions make a single linear implementation lineage impossible.", "effect": "Only text-supported edges are evolved_from; ambiguous links are unknown_relation."},
        {"id": "UNCERTAINTY-007", "label": "SUPPORTED", "issue": "Derived split-document trees on remote branches postdate and rewrite/split the source documents.", "effect": "They were inventoried as derivative copies but not treated as independent pre-existing source revisions."},
        {"id": "UNCERTAINTY-008", "label": "UNKNOWN", "issue": "Concurrency safety is not established by source prose or token observation alone.", "effect": "Every concurrency safety conclusion is UNKNOWN and verification is UNVERIFIED."},
    ] + extraction_uncertainties

    # PHASE 12: consolidated metadata (logical sidecars) and indexes.
    manifest_records = []
    for record in artifacts:
        clean = {k: v for k, v in record.items() if not k.startswith("_") and k != "logical_key"}
        # SOURCE-MANIFEST's required flat tracing fields coexist with the
        # richer layered source/provenance records.
        clean.update({
            "source_document": record["source"]["document"],
            "source_revision": record["source"]["revision"],
            "source_heading": record["source"]["heading"],
            "source_position": record["source"]["position"],
            "sha256": record["integrity"]["sha256"],
            "provenance": {
                "source_document": record["source"]["document"],
                "source_revision": record["source"]["revision"],
                "source_path": record["source"]["path"],
                "source_heading": record["source"]["heading"],
                "source_position": record["source"]["position"],
                "extraction_method": record["source"]["extraction_method"],
                "commit_sha": record["source"]["commit"],
                "branch": record["source"]["branch"],
                "occurrences": record["source"]["occurrences"],
                "tag": record["source"]["tag"],
                "author": record["source"]["author"],
                "timestamp": record["source"]["timestamp"],
                "parent_revision": record["source"]["parent_revision"],
            },
        })
        manifest_records.append(clean)
    manifest = {
        "schema_version": 1,
        "format_note": "JSON serialization; valid YAML 1.2. Each record is the artifact's consolidated metadata sidecar.",
        "generated_at": generated_at,
        "artifacts": manifest_records,
    }
    write_json_yaml(OUT / "SOURCE-MANIFEST.yaml", manifest)
    write_json_yaml(OUT / "ARTIFACT-INDEX.yaml", {
        "schema_version": 1,
        "artifacts": [{
            "artifact_id": x["artifact_id"], "chronology": x["chronology_index"],
            "artifact_type": x["artifact_type"], "classification": x["classification"],
            "status": x["status"], "version": x["history"]["version"],
            "source_revision": x["source"]["revision"], "source_position": x["source"]["position"],
            "output_file": x["output_file"], "sha256": x["integrity"]["sha256"],
        } for x in artifacts],
    })
    write_json_yaml(OUT / "REVISION-INVENTORY.yaml", {
        "schema_version": 1, "history_scope": {
            "repository_was_unshallowed": True,
            "refs_examined": ["main", "origin/main", "origin/arena/01a08cd3-generic-discovery-engine", "origin/arena/01a08d14-generic-discovery-engine", "origin/arena/01a08f03-generic-discovery-engine"],
            "tags_examined": [], "unique_document_blob_revisions": len(revision_inventory),
            "revision_events": REVISION_EVENTS,
        },
        "revisions": revision_inventory,
    })
    write_json_yaml(OUT / "DETECTION-INVENTORY.yaml", {"schema_version": 1, "detections": detections})
    write_json_yaml(OUT / "DUPLICATES.yaml", {"schema_version": 1, "duplicate_groups": duplicate_groups})
    write_json_yaml(OUT / "NEAR-DUPLICATES.yaml", {"schema_version": 1, "method": "successive same-symbol/family line SequenceMatcher; threshold 0.45; no semantic identity implied", "groups": near_duplicates})
    write_json_yaml(OUT / "CHANGES.yaml", {"schema_version": 1, "changes": changes})
    write_json_yaml(OUT / "FIELD-HISTORY.yaml", {"schema_version": 1, "field_histories": field_histories})
    write_json_yaml(OUT / "LINEAGE.yaml", {
        "schema_version": 1,
        "nodes": [{"artifact_id": x["artifact_id"], "artifact_type": x["artifact_type"], "version": x["history"]["version"], "source_revision": x["source"]["revision"]} for x in artifacts],
        "relationships": relationships,
        "evolution_groups": evolution_groups,
    })

    # Full bidirectional source map: one row per artifact.
    map_lines = [
        "# Source Map", "", "Every artifact row provides source → artifact and artifact → source tracing.", "",
        "| Source | Revision | Section | Position | Artifact | Output |",
        "|---|---|---|---|---|---|",
    ]
    esc = lambda value: str(value).replace("|", "\\|").replace("\r", " ").replace("\n", " ")
    for x in artifacts:
        source_paths = list(dict.fromkeys(
            [x["source"]["path"]] + [item["path"] for item in x["source"].get("occurrences", [])]
        ))
        map_lines.append(f"| {esc(', '.join(source_paths))} | `{x['source']['revision']}` | {esc(x['source']['heading'] or '(no heading)')} | {esc(x['source']['position'])} | `{x['artifact_id']}` | `{x['output_file']}` |")
    (OUT / "SOURCE-MAP.md").write_text("\n".join(map_lines) + "\n", encoding="utf-8", newline="\n")

    def finding_markdown(title: str, entries: list[dict[str, Any]], key: str) -> str:
        result = [f"# {title}", "", "These are derived evidence records. Historical source is not changed or resolved here.", ""]
        for item in entries:
            result += [f"## {item.get('id', item.get('label', 'Finding'))}", "", f"**Evidence label:** `{item['label']}`", "", item[key], ""]
            if "evidence" in item:
                result.append("Evidence:")
                result.extend(f"- {value}" for value in item["evidence"])
                result.append("")
            if "effect" in item:
                result += [f"Effect: {item['effect']}", ""]
            if "resolution" in item:
                result += [f"Resolution: `{item['resolution']}`", ""]
        return "\n".join(result)
    (OUT / "CONTRADICTIONS.md").write_text(finding_markdown("Contradiction Register", contradictions, "summary") + "\n", encoding="utf-8")
    (OUT / "UNCERTAINTIES.md").write_text(finding_markdown("Uncertainty Register", uncertainties, "issue") + "\n", encoding="utf-8")

    # PHASES 13-14: validation data and extraction report.
    valid_ids = set(records_by_id)
    validation_checks = []
    detection_ids = {x["detection_id"] for x in detections}
    represented = {x["source"]["detection_id"] for x in artifacts if x["source"]["detection_id"] and not x["source"]["detection_id"].startswith("component-")}
    validation_checks.append({"category": "Source coverage", "result": "PASS" if detection_ids == represented else "FAIL", "detail": f"{len(represented)}/{len(detection_ids)} detected source regions represented"})
    missing_prov = [x["artifact_id"] for x in artifacts if not x["derived"] and (not x["source"]["revision"] or x["source"]["byte_start"] is None)]
    validation_checks.append({"category": "Provenance coverage", "result": "PASS" if not missing_prov else "FAIL", "detail": f"{len(artifacts) - len(missing_prov)}/{len(artifacts)} artifacts have required provenance; reconstructed artifacts use composite provenance"})
    bad_hash = [x["artifact_id"] for x in artifacts if sha256((OUT / x["output_file"]).read_bytes()) != x["integrity"]["sha256"]]
    validation_checks.append({"category": "Hash coverage", "result": "PASS" if not bad_hash else "FAIL", "detail": f"{len(artifacts) - len(bad_hash)}/{len(artifacts)} artifact files match SHA-256"})
    bad_refs = [r for r in relationships if r["from"] not in valid_ids or r["to"] not in valid_ids]
    validation_checks.append({"category": "Lineage consistency", "result": "PASS" if not bad_refs else "FAIL", "detail": f"{len(relationships)} relationships; {len(bad_refs)} broken references"})
    bad_recon = [x["artifact_id"] for x in artifacts if x["derived"] and (x["artifact_type"] != "reconstructed" or not x.get("reconstruction") or x["reconstruction"].get("authoritative") is not False)]
    validation_checks.append({"category": "Reconstruction labeling", "result": "PASS" if not bad_recon else "FAIL", "detail": f"{len(reconstructed)} reconstructed artifacts explicitly non-authoritative"})
    semantic_mismatch = []
    blob_cache = {x["revision"]: git_blob(x["revision"]) for x in REVISIONS}
    for x in artifacts:
        if x["derived"]: continue
        source_bytes = blob_cache[x["source"]["revision"]][x["source"]["byte_start"]:x["source"]["byte_end_exclusive"]]
        if source_bytes != x["_content"]:
            semantic_mismatch.append(x["artifact_id"])
    validation_checks.append({"category": "Semantic preservation", "result": "PASS" if not semantic_mismatch else "FAIL", "detail": f"{len(artifacts) - len(reconstructed) - len(semantic_mismatch)}/{len(artifacts) - len(reconstructed)} original artifacts equal their source byte ranges"})
    empty = [x["artifact_id"] for x in artifacts if not x["_content"]]
    validation_checks.append({"category": "Empty artifacts", "result": "PASS" if not empty else "FAIL", "detail": f"{len(empty)} empty artifacts"})
    validation = {
        "schema_version": 1, "generated_at": generated_at,
        "overall": "PASS" if all(x["result"] == "PASS" for x in validation_checks) else "FAIL",
        "checks": validation_checks,
        "counts": {"artifacts": len(artifacts), "manifest_entries": len(manifest_records), "detections": len(detections), "duplicate_groups": len(duplicate_groups), "relationships": len(relationships)},
    }
    write_json_yaml(OUT / "VALIDATION.yaml", validation)

    counts = Counter(x["artifact_type"] for x in artifacts if not x["derived"])
    class_counts = Counter(x["classification"] for x in artifacts if not x["derived"])
    concurrency_count = sum(1 for x in artifacts if not x["derived"] and x["concurrency"])
    versions = defaultdict(set)
    for x in original_userscripts:
        versions[x["history"]["version"]].add(x["integrity"]["sha256"])
    provider_symbols = sorted({x["symbol"] for x in artifacts if x["artifact_type"] == "provider" and x["symbol"]})

    # Compact, artifact-addressed evolution tables for the report. These do
    # not copy or rewrite source; they summarize manifest observations.
    canonical_scripts = sorted(original_userscripts, key=lambda x: x["chronology_index"])

    def md(value: Any) -> str:
        return str(value).replace("|", "\\|").replace("\r", " ").replace("\n", " ")

    def source_label(script: dict[str, Any]) -> str:
        return f"{script['source']['document']}:{script['source']['line_start']}"

    def component_list(script: dict[str, Any], predicate) -> list[dict[str, Any]]:
        return sorted(
            [
                x for x in children_by_parent.get(script["artifact_id"], [])
                if x["source"]["extraction_method"].startswith("nested_") and predicate(x)
            ],
            key=lambda x: x["source"]["byte_start"] or 0,
        )

    userscript_rows = [
        "| Order | Version | Source | Artifact | Classification | Bytes | SHA-256 |",
        "|---:|---|---|---|---|---:|---|",
    ]
    for script in canonical_scripts:
        userscript_rows.append(
            f"| {script['chronology_index']} | `{script['history']['version']}` | {md(source_label(script))} | "
            f"`{script['artifact_id']}` | `{script['classification']}` | {script['integrity']['size_bytes']} | "
            f"`{script['integrity']['sha256']}` |"
        )

    def model_table(symbol: str) -> str:
        rows = [
            "| Version | Source | Artifact | Mechanically observed fields |",
            "|---|---|---|---|",
        ]
        for script in canonical_scripts:
            matches = component_list(script, lambda x: x.get("symbol") == symbol and x.get("symbol_kind") == "class")
            if matches:
                item = matches[0]
                fields = fields_for_model(item["_content"])
                field_text = ", ".join(f"`{field}`" for field in fields) if fields else "(none matched)"
                rows.append(f"| `{script['history']['version']}` | {md(source_label(script))} | `{item['artifact_id']}` | {field_text} |")
            else:
                reason = "NOT_RECOVERABLE_FROM_FLATTENED_REPRESENTATION" if script["source"]["line_start"] in (3, 11) else "NOT_PRESENT_AS_SEPARATE_CLASS"
                rows.append(f"| `{script['history']['version']}` | {md(source_label(script))} | `{reason}` | — |")
        return "\n".join(rows)

    scheduler_rows = [
        "| Version | Source | Scheduler artifacts |",
        "|---|---|---|",
    ]
    provider_rows = [
        "| Version | Source | Provider artifacts/symbols |",
        "|---|---|---|",
    ]
    acquisition_rows = [
        "| Version | Source | Acquisition artifacts/symbols |",
        "|---|---|---|",
    ]
    configuration_rows = [
        "| Version | Source | Configuration artifact | Worker count observation |",
        "|---|---|---|---|",
    ]
    concurrency_rows = [
        "| Version | Source | Model | Worker count | Ownership/duplicate-prevention observation |",
        "|---|---|---|---|---|",
    ]
    ui_rows = [
        "| Version | Source | UI artifacts |",
        "|---|---|---|",
    ]
    engine_rows = [
        "| Version | Source | Engine artifacts |",
        "|---|---|---|",
    ]
    for script in canonical_scripts:
        version = script["history"]["version"]
        source = md(source_label(script))
        schedulers = component_list(script, lambda x: x["artifact_type"] == "scheduler")
        providers = component_list(script, lambda x: x["artifact_type"] == "provider")
        acquisitions = component_list(script, lambda x: x["artifact_type"] == "acquisition")
        configurations = component_list(script, lambda x: x["artifact_type"] == "configuration")
        uis = component_list(script, lambda x: x["artifact_type"] == "ui")
        engines = component_list(script, lambda x: x["artifact_type"] == "engine")

        def refs(items: list[dict[str, Any]], with_symbol: bool = False) -> str:
            if not items:
                return "`NOT_SEPARATELY_RECOVERABLE_OR_NOT_PRESENT`"
            values = []
            for item in items:
                prefix = f"{item.get('symbol')}: " if with_symbol and item.get("symbol") else ""
                values.append(f"{prefix}`{item['artifact_id']}`")
            return "<br>".join(values)

        scheduler_rows.append(f"| `{version}` | {source} | {refs(schedulers, True)} |")
        provider_rows.append(f"| `{version}` | {source} | {refs(providers, True)} |")
        acquisition_rows.append(f"| `{version}` | {source} | {refs(acquisitions, True)} |")
        ui_rows.append(f"| `{version}` | {source} | {refs(uis, True)} |")
        engine_rows.append(f"| `{version}` | {source} | {refs(engines, True)} |")
        config_ref = refs(configurations, True)
        worker_count = script["concurrency"]["worker_count"] if script.get("concurrency") else "UNKNOWN"
        configuration_rows.append(f"| `{version}` | {source} | {config_ref} | `{worker_count}` |")
        if script.get("concurrency"):
            concurrency = script["concurrency"]
            concurrency_rows.append(
                f"| `{version}` | {source} | {md(', '.join(concurrency['model']))} | `{concurrency['worker_count']}` | "
                f"{md(', '.join(concurrency['ownership_mechanism']))}; duplicate prevention: "
                f"{md(', '.join(concurrency['duplicate_prevention']))} |"
            )
        else:
            concurrency_rows.append(f"| `{version}` | {source} | `NO_CONCURRENCY_TOKENS_OBSERVED` | `UNKNOWN` | `UNKNOWN` |")

    report = f"""# Historical Source Extraction Report

## Completion

**HISTORICAL SOURCE EXTRACTION COMPLETE**

This is an evidence-preserving extraction. It does not modernize, repair, merge, or execute historical source.

## Documents examined

- `Userscript Discovery Prototype.md`
- `Continue Architecture Planning.md`
- Exact renamed archive copies and archive-banner revisions on fetched remote branches

Historical document blob revisions examined: **{len(REVISIONS)}**  
Code-bearing revisions: **{len(REVISIONS)}**  
Git revision events affecting these documents: **{len(REVISION_EVENTS)}**  
Tags found: **0**

Unchanged commit/path occurrences (including an exact rename to `archive/` on another branch) are mapped to their content-addressed blob revision. They are not miscounted as new byte revisions; their paths and commits remain in provenance.

## Artifacts

Original extracted artifacts: **{len(artifacts) - len(reconstructed)}**  
Reconstructed artifacts: **{len(reconstructed)}**

- Userscripts: **{counts['userscript']}**
- Engines: **{counts['engine']}**
- Models: **{counts['model']}**
- Providers: **{counts['provider']}**
- Schedulers: **{counts['scheduler']}**
- Acquisition: **{counts['acquisition']}**
- Concurrency-bearing artifacts (overlapping category): **{concurrency_count}**
- UI: **{counts['ui']}**
- Tests: **{counts['test']}**
- Configurations: **{counts['configuration']}**
- Schemas: **{counts['schema']}**
- Patches/diffs: **{counts['patch']}**
- Pseudocode-classified: **{class_counts['PSEUDOCODE']}**
- Fragments: **{counts['fragment']}**

## Userscript versions

The original (non-banner) document revisions contain 14 userscript representations. Archive-banner revisions retain another 14 exact code copies. Explicit version labels and distinct represented-byte variants in the original revisions:

{chr(10).join(f'- `v{version}`: {len(hashes)} byte-distinct representation(s)' for version, hashes in sorted(versions.items()))}

The v0.4.0, v0.5.0, and v0.6.0 labels each occur on multiple byte-distinct scripts. They are not merged.

### Chronological source-position index

{chr(10).join(userscript_rows)}

## Major implementation families

- Early source-split v0.1.0 and v0.2.0 userscripts
- Flattened v0.1.0/v0.2.0 paste representations
- Complete fenced v0.3.0 through v0.7.1 userscript family, including repeated-version branches
- Post-v0.7.1 architecture contracts and pseudocode through v0.35
- Exact archive-banner revision copies

## Discovery-engine evolution

{chr(10).join(engine_rows)}

Rows report exact nested engine-class slices where boundaries were mechanically recoverable. Absence in this table does not mean the concept is absent from a flattened whole-script artifact.

## Scheduler evolution

{chr(10).join(scheduler_rows)}

Scheduler classes and scheduler-oriented code blocks remain independent artifacts. No scheduler implementation was merged into a later representation.

## Candidate model evolution

{model_table('Candidate')}

## Observation model evolution

{model_table('Observation')}

## Discovery model evolution

{model_table('Discovery')}

`FIELD-HISTORY.yaml` compares `this.<field> =` assignment sets only along source-supported userscript lineage edges. It does not infer field renames, types, or semantic equivalence. KnowledgeBase, provenance, resource, budget, session, domain, claim, and related definitions remain separately indexed.

## Provider evolution

{chr(10).join(provider_rows)}

Provider symbols mechanically identified across all artifacts include:

{chr(10).join(f'- `{name}`' for name in provider_symbols) if provider_symbols else '- None mechanically identified'}

Provider dependencies are token observations, not runtime verification.

## Acquisition evolution

{chr(10).join(acquisition_rows)}

Acquisition classes and contracts are separately classified where source boundaries permit. Historical `fetch`, XHR, and `GM_xmlhttpRequest` implementations remain independent.

## Concurrency evolution

{chr(10).join(concurrency_rows)}

Manifest `concurrency` records also retain claim points, async boundaries, cancellation tokens, and error-isolation syntax. These observations do **not** establish concurrency safety; every safety conclusion remains `UNKNOWN` and verification remains `UNVERIFIED`.

## Configuration evolution

{chr(10).join(configuration_rows)}

Configuration files preserve exact historical literals. `CHANGES.yaml` compares mechanically observed simple literals without evaluating JavaScript.

## Storage evolution

{model_table('KnowledgeBase')}

Storage API token deltas (`GM_getValue`, `GM_setValue`, `localStorage`, and `IndexedDB`) are recorded under `cross_version_dimensions.storage_tokens` in `CHANGES.yaml`; no persistence behavior is inferred.

## UI evolution

{chr(10).join(ui_rows)}

Clearly marked UI source sections inside complete userscripts are extracted as exact nested byte ranges. Flattened scripts were not split because their original component whitespace/boundaries are not recoverable.

## Tests and validation code

No fenced block met the conservative test criterion (a test-labeled section with assertion/test calls). Validation/invariant architecture snippets remain pseudocode rather than being relabeled as executed tests.

## Duplication and lineage

Exact duplicate groups: **{len(duplicate_groups)}**  
Near-duplicate observations: **{len(near_duplicates)}**  
Evolution groups: **{len(evolution_groups)}**  
Change records: **{len(changes)}**

Duplicates are retained. `DUPLICATES.yaml` chooses a canonical identifier solely by earliest chronology/provenance index. `NEAR-DUPLICATES.yaml` records mechanical line similarity without asserting semantic identity. `evolved_from` is used only where source prose supports the transition; ambiguous edges are `unknown_relation`.

Every `CHANGES.yaml` record contains mechanical comparisons for API symbols, assigned data fields, control-flow tokens, scheduler/concurrency/acquisition/discovery tokens, provider symbols, UI/storage/error/security tokens, and simple configuration literals. `behavior_changes` remains empty because no execution or semantic verification was performed.

## Superseded implementations

Artifacts explicitly classified `SUPERSEDED_IMPLEMENTATION`: **{sum(1 for x in artifacts if x['status'] == 'SUPERSEDED_IMPLEMENTATION')}**.

The documents use revised/continuing language that supports selected `evolved_from` edges, but they do not reliably establish one current winner among repeated v0.4.0, v0.5.0, or v0.6.0 scripts. The extraction therefore does not silently mark those variants superseded.

## Missing/incomplete source

Incomplete/anomalous original artifacts: **{sum(1 for x in artifacts if not x['derived'] and x['incomplete'])}**

The early split/flattened scripts are preserved exactly. Missing original whitespace in flattened lines is `NOT_RECOVERABLE`; it was not inferred. There were **0** extraction failures. Lexical component-boundary uncertainties, if any, are listed in `UNCERTAINTIES.md`.

## Contradictions and uncertainties

Contradictions: **{len(contradictions)}**  
Uncertainties: **{len(uncertainties)}**

Repeated/regressing versions and source formatting conflicts are registered, not resolved.

## Reconstruction candidates and results

Two optional v0.1.0/v0.2.0 reconstructions mechanically concatenate explicit source ranges after removing Markdown fence delimiter lines. They remain under `reconstructed/`, are marked `derived: true`, `semantic_inference: false`, and `authoritative: false`. They are **not** authentic raw artifacts. Flattened paste representations were not reconstructed.

## Validation

{chr(10).join(f"- {x['category']}: **{x['result']}** — {x['detail']}" for x in validation_checks)}

Overall: **{validation['overall']}**

## Final distinction

- **EXTRACTED:** exact bytes selected from pinned historical Git blobs; authoritative for what those Markdown revisions contain.
- **RECONSTRUCTED:** separately labeled mechanical concatenations; non-authoritative derivatives.
- **INFERRED:** language, role, context version, similarity, and some chronology metadata only; never presented as authentic source bytes.
"""
    (OUT / "EXTRACTION-REPORT.md").write_text(report, encoding="utf-8", newline="\n")

    readme = f"""# Historical Source Archive

This archive is the mechanical, provenance-first extraction of code and code-like material embedded in `Userscript Discovery Prototype.md` and `Continue Architecture Planning.md` across all unique source-document blobs found in fetched Git refs.

## Layer separation

1. **Raw historical source:** `raw/` contains byte-exact pinned Git blobs, including BOM and CRLF.
2. **Provenance:** `SOURCE-MANIFEST.yaml`, `SOURCE-MAP.md`, `REVISION-INVENTORY.yaml`, and `DETECTION-INVENTORY.yaml`.
3. **Derived analysis:** indexes, duplicates, near-duplicates, lineage, changes, field history, contradictions, uncertainties, report, and validation.
4. **Reconstruction:** `reconstructed/`; always derived and non-authoritative.

Every file under `artifacts/` is an exact contiguous byte slice of a raw Git blob. Fenced-artifact files contain the bytes *inside* the Markdown fence; fence labels and source positions remain in metadata. Source-split userscript containers are also retained as exact contiguous intervals, including their historical formatting anomalies. No formatter or linter was run. The local `.gitattributes` marks raw, extracted, and reconstructed payloads `-text` so Git checkout cannot rewrite their historical line endings.

## Metadata sidecars

To stay below repository file-count limits while retaining one metadata record per artifact, `SOURCE-MANIFEST.yaml` is the consolidated logical sidecar store. Its JSON serialization is valid YAML 1.2 and can be parsed with standard JSON tools. There is no artifact without a manifest record.

## Key files

- `SOURCE-MANIFEST.yaml` — complete per-artifact metadata, provenance, context, integrity, dependencies, and concurrency observations
- `SOURCE-MAP.md` — bidirectional source/artifact map
- `ARTIFACT-INDEX.yaml` — concise deterministic index
- `REVISION-INVENTORY.yaml` — blobs, every observed unchanged path occurrence, refs, rename events, and raw hashes
- `DETECTION-INVENTORY.yaml` — every fence/outside userscript/independent inline region
- `DUPLICATES.yaml` / `NEAR-DUPLICATES.yaml` — retained exact copies and mechanical similarity
- `LINEAGE.yaml` / `CHANGES.yaml` — conservative evidence-backed lineage and mechanical comparisons
- `FIELD-HISTORY.yaml` — mechanically observed model field-set changes
- `CONTRADICTIONS.md` / `UNCERTAINTIES.md` — unresolved evidence registers
- `VALIDATION.yaml` — automated integrity checks
- `EXTRACTION-REPORT.md` — final historical evolution report

## Reproduce and validate

```sh
python3 historical-source/tools/extract.py
python3 historical-source/tools/validate.py
```

The extractor is pinned to the four unique document blob revisions inventoried on {generated_at}. Earlier pre-Git chat revisions are not available and are never guessed.
"""
    (OUT / "README.md").write_text(readme, encoding="utf-8", newline="\n")

    # Run the independent validator last; it replaces VALIDATION.yaml with the
    # broader orphan/raw/duplicate/index checks in addition to core checks.
    subprocess.run(
        ["python3", str(OUT / "tools" / "validate.py")],
        cwd=ROOT, check=True, stdout=subprocess.DEVNULL,
    )

    print(json.dumps({
        "artifacts": len(artifacts), "extracted": len(artifacts) - len(reconstructed),
        "reconstructed": len(reconstructed), "detections": len(detections),
        "duplicates": len(duplicate_groups), "near_duplicates": len(near_duplicates),
        "evolution_groups": len(evolution_groups), "validation": validation["overall"],
    }, indent=2))


if __name__ == "__main__":
    main()
