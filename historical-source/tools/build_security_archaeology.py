#!/usr/bin/env python3
"""Build Protocol-v8 failure, security, and trust-boundary archaeology.

This is a deterministic static archaeology generator.  It extracts mechanisms from
recovered snapshots before applying the stable analytical vocabulary.  It does not
execute historical code and never turns a mechanism into a system-wide guarantee.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[2]
HS = ROOT / "historical-source"
OUT = HS / "security"
MANIFEST = HS / "RECONSTRUCTION-MANIFEST.yaml"
BUILDER = "security-archaeology-builder-v8"
SCHEMA = 8

FAILURE_TYPES = [
    "INPUT_FAILURE", "VALIDATION_FAILURE", "CONFIGURATION_FAILURE", "ACQUISITION_FAILURE",
    "NETWORK_FAILURE", "TIMEOUT", "HTTP_FAILURE", "PARSING_FAILURE", "RECOGNITION_FAILURE",
    "PROVIDER_FAILURE", "DISCOVERY_FAILURE", "EXPANSION_FAILURE", "DEDUPLICATION_FAILURE",
    "SCHEDULER_FAILURE", "CONCURRENCY_FAILURE", "STATE_FAILURE", "PERSISTENCE_FAILURE",
    "EXPORT_FAILURE", "UI_FAILURE", "RESOURCE_EXHAUSTION", "CANCELLATION", "UNKNOWN_FAILURE",
]
STAGES = ["INPUT", "VALIDATION", "ACQUISITION", "OBSERVATION", "RECOGNITION", "DISCOVERY", "EXPANSION", "SCHEDULING", "PERSISTENCE", "EXPORT", "UI", "CROSS_CUTTING"]
FAILURE_LEVELS = {
    "F0": "CATASTROPHIC_OR_PROCESS_WIDE", "F1": "ENGINE_WIDE", "F2": "SCAN_WIDE",
    "F3": "WORKER_WIDE", "F4": "CANDIDATE_WIDE", "F5": "PROVIDER_WIDE", "F6": "OPERATION_LOCAL",
    "UNKNOWN": "STOP_BOUNDARY_NOT_PROVED",
}
EVIDENCE_LABELS = {"PROVED", "SUPPORTED", "INFERRED", "UNKNOWN"}
SILENCE_CLASSES = {"INTENTIONAL_SILENCE", "UNEXPLAINED_SILENCE", "ERROR_SUPPRESSION", "UNKNOWN"}
RISK_CLASSES = {"OBSERVED_RISK", "MITIGATED", "UNMITIGATED", "UNKNOWN"}
INTEGRITY_CLASSES = {"POSSIBLE", "OBSERVED", "PREVENTED", "UNKNOWN"}
SECURITY_CLAIM_TYPES = {"SECURITY_PROPERTY", "SECURITY_MECHANISM", "SECURITY_ASSUMPTION", "SECURITY_GOAL", "SECURITY_GUARANTEE"}
THREAT_CLASSES = {"EXPLICIT_THREAT", "IMPLICIT_THREAT", "RETROSPECTIVE_THREAT", "UNKNOWN"}
TRANSITION_CONFIDENCE = {"PROVED", "SUPPORTED", "INFERRED", "CONTRADICTED", "UNKNOWN"}
CHANGE_CLASSES = {"REGRESSION", "SIMPLIFICATION", "REQUIREMENT_CHANGE", "EXPERIMENT", "UNKNOWN"}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def stable_id(prefix: str, *parts: Any) -> str:
    payload = "\x1f".join(str(x) for x in parts).encode("utf-8")
    return f"{prefix}-{hashlib.sha256(payload).hexdigest()[:16]}"


def uniq(values: Iterable[Any]) -> list[Any]:
    out: list[Any] = []
    seen: set[str] = set()
    for value in values:
        key = json.dumps(value, sort_keys=True, ensure_ascii=False)
        if key not in seen:
            seen.add(key)
            out.append(value)
    return out


def version_key(version: str) -> tuple[int, ...]:
    return tuple(int(x) for x in re.findall(r"\d+", version))


def line_at(text: str, offset: int) -> int:
    return text.count("\n", 0, max(0, offset)) + 1


def byte_at(text: str, offset: int) -> int:
    return len(text[:max(0, offset)].encode("utf-8"))


def brief(value: Any, limit: int = 180) -> str:
    text = re.sub(r"\s+", " ", str(value)).strip()
    return text if len(text) <= limit else text[:limit-1] + "…"


def mask_js(text: str, *, strings: bool = True, comments: bool = True) -> str:
    """Preserve offsets/newlines while masking comments and optionally strings."""
    chars = list(text)
    i = 0
    state = "code"
    quote = ""
    while i < len(chars):
        c = chars[i]
        n = chars[i + 1] if i + 1 < len(chars) else ""
        if state == "code":
            if comments and c == "/" and n == "/":
                chars[i] = chars[i + 1] = " "
                i += 2
                state = "line"
                continue
            if comments and c == "/" and n == "*":
                chars[i] = chars[i + 1] = " "
                i += 2
                state = "block"
                continue
            if strings and c == "/" and n not in "/*":
                j = i - 1
                while j >= 0 and chars[j].isspace(): j -= 1
                previous = chars[j] if j >= 0 else ""
                if previous in "=(:,![{;?" or previous == "":
                    chars[i] = " "; i += 1; state = "regex"; continue
            if strings and c in "'\"`":
                quote = c
                chars[i] = " "
                i += 1
                state = "string"
                continue
            i += 1
        elif state == "line":
            if c == "\n":
                state = "code"
            else:
                chars[i] = " "
            i += 1
        elif state == "block":
            if c == "*" and n == "/":
                chars[i] = chars[i + 1] = " "
                i += 2
                state = "code"
            else:
                if c not in "\r\n": chars[i] = " "
                i += 1
        elif state == "regex":
            if c == "\\":
                chars[i] = " "
                if i + 1 < len(chars): chars[i + 1] = " "
                i += 2
            elif c == "[":
                chars[i] = " "; i += 1; state = "regex_class"
            elif c == "/":
                chars[i] = " "; i += 1
                while i < len(chars) and chars[i].isalpha(): chars[i] = " "; i += 1
                state = "code"
            else:
                if c not in "\r\n": chars[i] = " "
                i += 1
        elif state == "regex_class":
            if c == "\\":
                chars[i] = " "
                if i + 1 < len(chars): chars[i + 1] = " "
                i += 2
            elif c == "]":
                chars[i] = " "; i += 1; state = "regex"
            else:
                if c not in "\r\n": chars[i] = " "
                i += 1
        else:
            if c == "\\":
                chars[i] = " "
                if i + 1 < len(chars) and chars[i + 1] not in "\r\n": chars[i + 1] = " "
                i += 2
            elif c == quote:
                chars[i] = " "
                i += 1
                state = "code"
            else:
                if c not in "\r\n": chars[i] = " "
                i += 1
    return "".join(chars)


def brace_end(masked: str, open_pos: int) -> int | None:
    if open_pos < 0 or open_pos >= len(masked) or masked[open_pos] != "{": return None
    depth = 0
    for i in range(open_pos, len(masked)):
        if masked[i] == "{": depth += 1
        elif masked[i] == "}":
            depth -= 1
            if depth == 0: return i + 1
    return None


def extract_classes(text: str, syntax: str) -> list[dict[str, Any]]:
    out = []
    for m in re.finditer(r"\bclass\s+([A-Za-z_$][\w$]*)(?:\s+extends\s+([A-Za-z_$][\w$]*))?\s*\{", syntax):
        end = brace_end(syntax, m.end() - 1)
        if end:
            out.append({"name": m.group(1), "base": m.group(2), "start": m.start(), "body_start": m.end(), "end": end})
    return out


def extract_methods(text: str, syntax: str, classes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    pattern = re.compile(r"(?m)^\s*(?:(async)\s+)?(?:static\s+)?(?:get\s+|set\s+)?([A-Za-z_$][\w$]*)\s*\(([^)]*)\)\s*\{")
    for cls in classes:
        for m in pattern.finditer(syntax, cls["body_start"], cls["end"] - 1):
            # only direct class methods, not nested function declarations
            prefix = syntax[cls["body_start"]:m.start()]
            if prefix.count("{") != prefix.count("}"): continue
            end = brace_end(syntax, m.end() - 1)
            if not end or end > cls["end"]: continue
            out.append({
                "class": cls["name"], "name": m.group(2), "async": bool(m.group(1)), "params": brief(m.group(3), 500),
                "start": m.start(), "body_start": m.end(), "end": end, "body": text[m.end():end - 1],
            })
    # Top-level named functions are useful security owners.
    occupied = [(x["start"], x["end"]) for x in classes]
    fp = re.compile(r"(?m)^\s*(?:(async)\s+)?function\s+([A-Za-z_$][\w$]*)\s*\(([^)]*)\)\s*\{")
    for m in fp.finditer(syntax):
        if any(a <= m.start() < b for a, b in occupied): continue
        end = brace_end(syntax, m.end() - 1)
        if end:
            out.append({"class": "TOP_LEVEL", "name": m.group(2), "async": bool(m.group(1)), "params": brief(m.group(3), 500), "start": m.start(), "body_start": m.end(), "end": end, "body": text[m.end():end - 1]})
    return sorted(out, key=lambda x: (x["start"], x["end"], x["class"], x["name"]))


reconstruction = load(MANIFEST)
all_snapshots = reconstruction["snapshots"]
snapshots = sorted([x for x in all_snapshots if x["reconstruction"]["status"] in {"EXACT", "MECHANICALLY_COMPOSED"}], key=lambda x: (version_key(x["historical_version"]), x["snapshot_id"]))
partial_snapshots = [x for x in all_snapshots if x["reconstruction"]["status"] == "PARTIAL"]
versions = sorted({x["historical_version"] for x in snapshots}, key=version_key)
by_id = {x["snapshot_id"]: x for x in snapshots}
paths = {x["snapshot_id"]: HS / x["paths"]["source"] for x in snapshots}
raws = {k: p.read_bytes() for k, p in paths.items()}
texts = {k: b.decode("utf-8") for k, b in raws.items()}
syntax_masks = {k: mask_js(v, strings=True, comments=True) for k, v in texts.items()}
comment_masks = {k: mask_js(v, strings=False, comments=True) for k, v in texts.items()}
classes = {k: extract_classes(texts[k], syntax_masks[k]) for k in texts}
methods = {k: extract_methods(texts[k], syntax_masks[k], classes[k]) for k in texts}

# Evidence is directional: exact recovered source/root prose -> analytical record.
evidence: dict[str, dict[str, Any]] = {}

def source_ev(snapshot_id: str, start: int, end: int, claim: str, kind: str = "HISTORICAL_CODE") -> str:
    text = texts[snapshot_id]
    start = max(0, min(start, len(text)))
    end = max(start, min(end, len(text)))
    rel = str(paths[snapshot_id].relative_to(ROOT))
    eid = stable_id("security-ev", rel, byte_at(text, start), byte_at(text, end), claim)
    evidence[eid] = {
        "evidence_id": eid, "kind": kind, "snapshot_id": snapshot_id,
        "version": by_id[snapshot_id]["historical_version"], "variant": by_id[snapshot_id]["variant"],
        "path": rel, "line_start": line_at(text, start), "line_end": line_at(text, max(start, end - 1)),
        "byte_start": byte_at(text, start), "byte_end": byte_at(text, end),
        "range_sha256": sha_bytes(text[start:end].encode("utf-8")), "source_sha256": sha_bytes(raws[snapshot_id]),
        "claim": claim, "direction": "HISTORICAL_SOURCE_TO_DERIVED_SECURITY_CLAIM",
    }
    return eid


def match_ev(snapshot_id: str, match: re.Match[str], claim: str, kind: str = "HISTORICAL_CODE") -> str:
    return source_ev(snapshot_id, match.start(), match.end(), claim, kind)


def method_ev(snapshot_id: str, method: dict[str, Any], claim: str) -> str:
    return source_ev(snapshot_id, method["start"], method["end"], claim, "HISTORICAL_METHOD")


def class_ev(snapshot_id: str, name: str, claim: str) -> str | None:
    row = next((x for x in classes[snapshot_id] if x["name"] == name), None)
    return source_ev(snapshot_id, row["start"], row["end"], claim, "HISTORICAL_CLASS") if row else None


def absence_ev(snapshot_id: str, query: str, claim: str) -> str:
    # A composite property can be unproved even when one token is present.  In
    # that case retain the token as context; never emit a false source-absence.
    try:
        present = re.search(query, comment_masks[snapshot_id], re.I | re.S)
    except re.error:
        present = None
    if present:
        return source_ev(snapshot_id, present.start(), present.end(), claim + " (context token present; composite property still unproved)", "CONTEXT_ONLY_NOT_POSITIVE_PROOF")
    rel = str(paths[snapshot_id].relative_to(ROOT))
    eid = stable_id("security-absence", rel, query, claim)
    evidence[eid] = {
        "evidence_id": eid, "kind": "BOUNDED_ABSENCE_SEARCH", "snapshot_id": snapshot_id,
        "version": by_id[snapshot_id]["historical_version"], "variant": by_id[snapshot_id]["variant"],
        "path": rel, "query": query, "flags": "IGNORECASE", "search_scope": "COMMENT_MASKED_CODE_WITH_STRINGS",
        "source_sha256": sha_bytes(raws[snapshot_id]),
        "claim": claim, "direction": "HISTORICAL_SOURCE_ABSENCE_TO_BOUNDED_NEGATIVE_CLAIM",
    }
    return eid


def root_ev(path: Path, match: re.Match[str], claim: str) -> str:
    raw = path.read_bytes(); text = raw.decode("utf-8")
    rel = str(path.relative_to(ROOT))
    eid = stable_id("security-prose", rel, byte_at(text, match.start()), byte_at(text, match.end()), claim)
    evidence[eid] = {
        "evidence_id": eid, "kind": "CURRENT_OR_HISTORICAL_PROSE", "snapshot_id": None, "version": "CURRENT_PROSE",
        "path": rel, "line_start": line_at(text, match.start()), "line_end": line_at(text, max(match.start(), match.end()-1)),
        "byte_start": byte_at(text, match.start()), "byte_end": byte_at(text, match.end()),
        "range_sha256": sha_bytes(text[match.start():match.end()].encode()), "source_sha256": sha_bytes(raw),
        "claim": claim, "direction": "PROSE_TO_PROSE_SCOPED_SECURITY_CLAIM",
    }
    return eid


def owner_at(snapshot_id: str, offset: int) -> tuple[str, str, dict[str, Any] | None]:
    containing = [m for m in methods[snapshot_id] if m["start"] <= offset < m["end"]]
    if containing:
        m = min(containing, key=lambda x: x["end"] - x["start"])
        return m["class"], m["name"], m
    cls = next((c for c in classes[snapshot_id] if c["start"] <= offset < c["end"]), None)
    if cls:
        return cls["name"], "TOP_LEVEL", None
    # Regex literals can contain braces and defeat a coarse class scan.  Recover
    # a bounded lexical owner for nearby historical method syntax; this remains
    # an occurrence label, not a call/containment inference.
    start = max(0, offset - 7000)
    prefix = syntax_masks[snapshot_id][start:offset]
    candidates = [m for m in re.finditer(r"(?m)^\s*(?:async\s+)?([A-Za-z_$][\w$]*)\s*\([^;{}]*\)\s*\{", prefix) if m.group(1) not in {"if", "for", "while", "switch", "catch", "with"}]
    if candidates:
        mm = candidates[-1]
        absolute = start + mm.start()
        owner_candidates = [x for x in re.finditer(r"\bclass\s+([A-Za-z_$][\w$]*)[^\{]*\{", syntax_masks[snapshot_id][:absolute])]
        owner = owner_candidates[-1].group(1) if owner_candidates else "TOP_LEVEL"
        pseudo = {"class": owner, "name": mm.group(1), "start": absolute, "end": offset + 1,
                  "body": texts[snapshot_id][absolute:min(len(texts[snapshot_id]), offset + 1200)]}
        return owner, mm.group(1), pseudo
    return "TOP_LEVEL", "TOP_LEVEL", None


def first_match(snapshot_id: str, pattern: str, flags: int = re.I | re.S, *, commentless: bool = True) -> re.Match[str] | None:
    return re.search(pattern, comment_masks[snapshot_id] if commentless else texts[snapshot_id], flags)


def all_matches(snapshot_id: str, pattern: str, flags: int = re.I | re.S, *, commentless: bool = True) -> list[re.Match[str]]:
    return list(re.finditer(pattern, comment_masks[snapshot_id] if commentless else texts[snapshot_id], flags))


def evidence_for_match(snapshot_id: str, pattern: str, claim: str, *, required: bool = False, flags: int = re.I | re.S) -> list[str]:
    m = first_match(snapshot_id, pattern, flags)
    if m: return [match_ev(snapshot_id, m, claim)]
    return [absence_ev(snapshot_id, pattern, claim)] if required else []


def stage_for(owner: str, operation: str, body: str = "") -> str:
    label = f"{owner}.{operation}".lower()
    if re.search(r"persist|restore|storage|\.load", label): return "PERSISTENCE"
    if re.search(r"export|download", label): return "EXPORT"
    if re.search(r"(?:^|\.)(?:ui|engineui|render|renderui|installui|initializeui|panel|button)(?:\.|$)", label): return "UI"
    if re.search(r"schedul|worker|claim|queue|run|origincontroller", label): return "SCHEDULING"
    if re.search(r"acqui|request|http|fetch|response", label): return "ACQUISITION"
    if "observation" in label: return "OBSERVATION"
    if re.search(r"provider|recogn|parse|extract", label): return "RECOGNITION"
    if "discover" in label: return "DISCOVERY"
    if re.search(r"candidate|expand", label): return "EXPANSION"
    if re.search(r"canonical|allow|valid|seed|url", label): return "VALIDATION"
    value = body[:400].lower()
    if re.search(r"acqui|request|http|fetch|response", value): return "ACQUISITION"
    if "observation" in value: return "OBSERVATION"
    if re.search(r"provider|recogn|parse|extract", value): return "RECOGNITION"
    if "discover" in value: return "DISCOVERY"
    if re.search(r"candidate|expand", value): return "EXPANSION"
    return "CROSS_CUTTING"


def classify_context(owner: str, operation: str, body: str, excerpt: str = "") -> str:
    label = f"{owner}.{operation}".lower()
    value = f"{label} {body[:800]} {excerpt}".lower()
    if "timeout" in excerpt.lower() or "ontimeout" in value: return "TIMEOUT"
    if re.search(r"persist|restore|storage|load", label): return "PERSISTENCE_FAILURE"
    if "providerregistry" in label: return "PROVIDER_FAILURE"
    if re.search(r"worker|schedul|claim|queue|origincontroller", label): return "SCHEDULER_FAILURE"
    if re.search(r"acqui|request|fetch|xmlhttprequest|network", label): return "NETWORK_FAILURE"
    if re.search(r"export|download", label): return "EXPORT_FAILURE"
    if re.search(r"(?:^|\.)(?:ui|engineui|render|renderui|installui|initializeui|panel|button)(?:\.|$)", label): return "UI_FAILURE"
    if "provider" in label and re.search(r"json\.parse|domparser|parsererror|parse", value): return "PARSING_FAILURE"
    if "provider" in label: return "RECOGNITION_FAILURE"
    if "recogn" in label: return "RECOGNITION_FAILURE"
    if "discover" in label: return "DISCOVERY_FAILURE"
    if re.search(r"candidate|expand", label): return "EXPANSION_FAILURE"
    if re.search(r"canonical|allowed|valid|url", label): return "VALIDATION_FAILURE"
    # Body-only clues are weaker and used only after the owner did not classify.
    if re.search(r"persist|restore|gm_setvalue|gm_getvalue|localstorage", value): return "PERSISTENCE_FAILURE"
    if re.search(r"json\.parse|domparser|parsererror", value): return "PARSING_FAILURE"
    return "UNKNOWN_FAILURE"


def catch_block(snapshot_id: str, m: re.Match[str]) -> tuple[str, int, int]:
    syntax = syntax_masks[snapshot_id]
    open_pos = syntax.find("{", m.start(), min(len(syntax), m.end() + 80))
    end = brace_end(syntax, open_pos) if open_pos >= 0 else None
    if end: return texts[snapshot_id][open_pos + 1:end - 1], open_pos + 1, end - 1
    return "", m.end(), m.end()


# --- Failure event extraction -------------------------------------------------
failure_events: list[dict[str, Any]] = []
silent_failures: list[dict[str, Any]] = []
failure_information: list[dict[str, Any]] = []


def add_failure(snapshot_id: str, offset: int, end: int, failure_type: str, trigger: str,
                detection: str, representation: str, propagation: str, containment: str,
                recovery: str, logging: list[str], provenance_effect: str, status: str,
                refs: list[str], operation_override: str | None = None) -> None:
    owner, operation, method = owner_at(snapshot_id, offset)
    if operation_override: operation = operation_override
    stage = stage_for(owner, operation, method["body"] if method else "")
    fid = stable_id("failure", snapshot_id, offset, failure_type, detection)
    failure_events.append({
        "failure_id": fid, "snapshot_id": snapshot_id, "version": by_id[snapshot_id]["historical_version"],
        "variant": by_id[snapshot_id]["variant"], "stage": stage, "operation": f"{owner}.{operation}",
        "failure_type": failure_type, "trigger": trigger, "detection": detection,
        "representation": representation, "propagation": propagation, "containment": containment,
        "containment_level": next((k for k, v in FAILURE_LEVELS.items() if v == containment), "UNKNOWN"),
        "recovery": recovery, "logging": logging or ["NOT_EVIDENCED"],
        "provenance_effect": provenance_effect, "evidence": uniq(refs), "status": status,
        "runtime_occurrence_proved": False,
    })

for snapshot in snapshots:
    sid = snapshot["snapshot_id"]
    code = comment_masks[sid]
    # Network callback detection paths.
    for pattern, ftype, detection, trigger in [
        (r"\bonerror\s*(?::|=)", "NETWORK_FAILURE", "ERROR_CALLBACK", "network/userscript request error callback"),
        (r"\bontimeout\s*(?::|=)", "TIMEOUT", "TIMEOUT_CALLBACK", "request timeout callback"),
    ]:
        for m in re.finditer(pattern, syntax_masks[sid], re.I):
            owner, op, method = owner_at(sid, m.start())
            body = method["body"] if method else code[max(0, m.start()-200):m.start()+500]
            representation = "PROMISE_REJECTION" if re.search(r"\breject\s*\(", body) else ("FAILED_OBSERVATION_OR_STATE" if re.search(r"failed|errors?\.push", body, re.I) else "CALLBACK_CONTROL_FLOW")
            propagation = "PROPAGATES_AS_REJECTION" if representation == "PROMISE_REJECTION" else "RECORDED_OR_RETURNED_ON_LOCAL_PATH"
            add_failure(sid, m.start(), m.end(), ftype, trigger, detection, representation, propagation,
                        FAILURE_LEVELS["UNKNOWN"], "CALLER_OR_WORKER_MAY_HANDLE" if "REJECTION" in representation else "LOCAL_FAILURE_PATH",
                        ["NOT_EVIDENCED_AT_CALLBACK"], "CANDIDATE_OR_REQUEST_LINKAGE_UNKNOWN_AT_CALLBACK", "IMPLEMENTED_DETECTION_PATH",
                        [match_ev(sid, m, f"{ftype} callback")])
    # HTTP status failure checks.
    for m in re.finditer(r"(?:status|response\.status)\s*(?:>=\s*400|<\s*200|>\s*299|!==?\s*200)", syntax_masks[sid], re.I):
        owner, op, method = owner_at(sid, m.start()); body = method["body"] if method else ""
        representation = "THROWN_ERROR" if re.search(r"throw\s+new\s+Error", body, re.I) else ("FAILED_STATUS_OR_RESULT" if re.search(r"fail|error|status", body, re.I) else "BOOLEAN_BRANCH")
        add_failure(sid, m.start(), m.end(), "HTTP_FAILURE", "HTTP status outside accepted range", "STATUS_BRANCH", representation,
                    "PROPAGATES" if representation == "THROWN_ERROR" else "LOCAL_BRANCH_OR_CALLER_RESULT", FAILURE_LEVELS["UNKNOWN"],
                    "NONE_OR_CALLER_DECIDES", ["NOT_EVIDENCED"], "RESPONSE_STATUS_MAY_BE_RETAINED", "IMPLEMENTED_DETECTION_PATH",
                    [match_ev(sid, m, "HTTP failure status detection")])
    # Parser-error markers are explicit parse failure detections.
    for m in re.finditer(r"parsererror|parseError", code, re.I):
        owner, op, method = owner_at(sid, m.start()); body = method["body"] if method else ""
        add_failure(sid, m.start(), m.end(), "PARSING_FAILURE", "parser-specific failure marker", "PARSER_RESULT_CHECK", brief(texts[sid][m.start():m.end()]),
                    "LOCAL_FALLBACK_OR_PROVIDER_RESULT", FAILURE_LEVELS["F6"], "RETURN_NULL_FALSE_OR_ERROR_DISCOVERY" if re.search(r"return\s+(?:null|false|\[\])", body) else "LOCAL_CLASSIFICATION",
                    ["NOT_EVIDENCED"], "PROVIDER_OR_OBSERVATION_LINKAGE_VARIES", "IMPLEMENTED_DETECTION_PATH", [match_ev(sid, m, "parse failure marker")])
    # Catch blocks expose concrete historical handling paths, not runtime failures.
    for m in re.finditer(r"\bcatch\s*(?:\(([^)]*)\))?\s*\{", syntax_masks[sid], re.I):
        block, bstart, bend = catch_block(sid, m)
        owner, op, method = owner_at(sid, m.start()); method_body = method["body"] if method else block
        ftype = classify_context(owner, op, method_body, block)
        empty = not re.sub(r"[\s;]", "", mask_js(block, strings=False, comments=True))
        rethrows = bool(re.search(r"\bthrow\b", mask_js(block, strings=False, comments=True)))
        rejection = bool(re.search(r"\breject\s*\(", block))
        fallback = re.search(r"\breturn(?:\s+(null|false|true|\[\]|\{\}))?\s*;", block, re.I)
        continues = bool(re.search(r"\bcontinue\b", block))
        records = bool(re.search(r"errors?\.push|fail(?:Candidate)?\s*\(|status\s*=|record|diagnostic|ledger", block, re.I))
        logs = []
        if re.search(r"console\.(?:error|warn|log)", block): logs.append("CONSOLE")
        if re.search(r"\b(?:warn|log)\s*\(", block): logs.append("LOG_WRAPPER")
        if re.search(r"diagnostic|ledger|record", block, re.I): logs.append("STRUCTURED_RECORD")
        if re.search(r"observation\.errors|observation\.complete", block, re.I): logs.append("OBSERVATION")
        if re.search(r"failCandidate|scheduler\.fail|addObservation", block, re.I): logs.append("KNOWLEDGE_BASE_OR_SCHEDULER_STATE")
        if re.search(r"textContent|render|updateUI", block, re.I): logs.append("UI")
        if rethrows: propagation = "RETHROW"
        elif rejection: propagation = "PROMISE_REJECTION"
        elif continues: propagation = "CONTINUE_LOOP"
        elif fallback: propagation = "FALLBACK_RETURN"
        elif records: propagation = "STATE_OR_DIAGNOSTIC_RECORD"
        else: propagation = "SUPPRESSED_OR_LOCAL_UNKNOWN"
        if owner == "ProviderRegistry" and not rethrows: level = "F5"
        elif re.search(r"processCandidate|worker", op, re.I) and records: level = "F4" if re.search(r"candidate", block, re.I) else "F3"
        elif not rethrows and (fallback or records or logs or empty): level = "F6"
        else: level = "UNKNOWN"
        if continues: recovery = "CONTINUE_NEXT_ITERATION"
        elif owner == "ProviderRegistry" and not rethrows and re.search(r"\bfor\s*\(", method_body): recovery = "CONTINUE_PROVIDER_LOOP_OR_METHOD_FALLBACK"
        elif re.search(r"retry|requeue|queueCandidate|addCandidate", block, re.I): recovery = "RETRY_OR_REQUEUE_PATH"
        elif fallback: recovery = "FALLBACK_VALUE"
        elif records: recovery = "RECORD_AND_RETURN_OR_CONTINUE"
        elif rethrows or rejection: recovery = "DELEGATED_TO_CALLER"
        else: recovery = "NONE_EVIDENCED"
        if re.search(r"candidate(?:Id|\.id)|observationId|provider", block, re.I): prov = "CONTEXT_PARTIALLY_RETAINED"
        else: prov = "FAILURE_CONTEXT_NOT_EVIDENCED_IN_HANDLER"
        ref = match_ev(sid, m, "catch handling path")
        add_failure(sid, m.start(), bend, ftype, "exception reaching catch", "CATCH", "EXCEPTION_VARIABLE" if m.group(1) else "UNBOUND_EXCEPTION",
                    propagation, FAILURE_LEVELS[level], recovery, logs, prov, "IMPLEMENTED_HANDLING_PATH", [ref])
        # Information preservation at this exact handler.
        preserved = []
        fields = {
            "error_type": r"(?:error|err)\.(?:name|constructor)", "message": r"(?:error|err)(?:\.message|\b)", "source": r"source|origin",
            "candidate": r"candidate(?:Id|\.id|\b)", "provider": r"provider(?:Id|\.name|\b)", "operation": r"operation|phase|stage",
            "timestamp": r"timestamp|createdAt|Date\.now", "stack": r"(?:error|err)\.stack", "request": r"request(?:Id|\b)",
            "response": r"response(?:Id|\b)", "retry_count": r"attempts|maxRetries|retryCount",
        }
        for field, pat in fields.items():
            if re.search(pat, block, re.I): preserved.append(field)
        failure_information.append({
            "failure_id": stable_id("failure", sid, m.start(), ftype, "CATCH"), "snapshot_id": sid,
            "preserved": preserved, "not_evidenced": [x for x in fields if x not in preserved],
            "information_loss": "GENERIC_STRING_OR_FALLBACK_LOSES_STRUCTURE" if re.search(r"String\s*\(\s*(?:error|err)|return\s+(?:null|false|\[\])", block, re.I) else "UNKNOWN",
            "evidence": [ref],
        })
        if empty:
            silence = "UNEXPLAINED_SILENCE"
        elif not rethrows and not rejection and not records and not logs:
            silence = "ERROR_SUPPRESSION"
        elif not rethrows and not rejection and logs and not records:
            silence = "ERROR_SUPPRESSION"
        else:
            silence = "UNKNOWN"
        if silence != "UNKNOWN":
            nearby = texts[sid][max(0, m.start()-180):min(len(texts[sid]), bend+180)]
            if re.search(r"optional|best effort|ignore|non-fatal", nearby, re.I): silence = "INTENTIONAL_SILENCE"
            silent_failures.append({
                "silence_id": stable_id("silence", sid, m.start()), "snapshot_id": sid,
                "version": snapshot["historical_version"], "variant": snapshot["variant"],
                "operation": f"{owner}.{op}", "classification": silence,
                "observable": bool(logs), "state_recorded": records, "rethrows": rethrows,
                "bug_claimed": False, "evidence": [ref],
            })
    # Explicit throws/rejections not already represented as catch paths.
    for pattern, detection in [(r"\bthrow\s+new\s+Error\s*\(", "THROW"), (r"\breject\s*\(\s*new\s+Error\s*\(", "PROMISE_REJECT")]:
        for m in re.finditer(pattern, syntax_masks[sid], re.I):
            owner, op, method = owner_at(sid, m.start()); body = method["body"] if method else ""
            ftype = classify_context(owner, op, body, texts[sid][m.start():m.start()+160])
            add_failure(sid, m.start(), m.end(), ftype, "explicit error branch", detection, "ERROR_OBJECT",
                        "PROPAGATES_TO_CALLER", FAILURE_LEVELS["UNKNOWN"], "CALLER_DECIDES", ["NOT_EVIDENCED_AT_THROW"],
                        "MESSAGE_PRESERVED_CANDIDATE_PROVIDER_CONTEXT_VARIES", "IMPLEMENTED_PROPAGATION_PATH", [match_ev(sid, m, "explicit error propagation")])

failure_events.sort(key=lambda x: (version_key(x["version"]), x["snapshot_id"], evidence[x["evidence"][0]].get("byte_start", -1), x["failure_id"]))

# Propagation graph is event-scoped; shared evidence never becomes cross-event causality.
propagation_edges: list[dict[str, Any]] = []
for event in failure_events:
    chain = [("FAILURE_SOURCE", "DETECTION", "TRIGGERS")]
    if event["propagation"] in {"RETHROW", "PROMISE_REJECTION", "PROPAGATES_TO_CALLER", "PROPAGATES_AS_REJECTION"}:
        chain += [("DETECTION", "CALLER", "PROPAGATES_TO")]
    else:
        chain += [("DETECTION", event["containment"], "HANDLED_AT")]
    if event["recovery"] not in {"NONE_EVIDENCED", "CALLER_DECIDES", "DELEGATED_TO_CALLER"}:
        chain += [(event["containment"], "RECOVERY_PATH", "ENABLES_PATH")]
    for index, (src, dst, kind) in enumerate(chain):
        propagation_edges.append({
            "edge_id": stable_id("failure-edge", event["failure_id"], index), "failure_id": event["failure_id"],
            "snapshot_id": event["snapshot_id"], "source": src, "target": dst, "type": kind,
            "confidence": "PROVED" if index == 0 else "SUPPORTED", "evidence": event["evidence"],
        })

# Per-category matrix retains absence/unknown rather than manufacturing events.
failure_matrix: list[dict[str, Any]] = []
for snapshot in snapshots:
    sid = snapshot["snapshot_id"]
    for failure_type in FAILURE_TYPES:
        rows = [x for x in failure_events if x["snapshot_id"] == sid and x["failure_type"] == failure_type]
        failure_matrix.append({
            "snapshot_id": sid, "version": snapshot["historical_version"], "variant": snapshot["variant"], "failure": failure_type,
            "detection": "PROVED" if rows else "UNKNOWN", "propagation": "SUPPORTED" if rows and all(x["propagation"] != "SUPPRESSED_OR_LOCAL_UNKNOWN" for x in rows) else "UNKNOWN",
            "containment": "SUPPORTED" if rows and any(x["containment_level"] != "UNKNOWN" for x in rows) else "UNKNOWN",
            "recovery": "SUPPORTED" if rows and any(x["recovery"] not in {"NONE_EVIDENCED", "CALLER_DECIDES"} for x in rows) else "UNKNOWN",
            "observable": "SUPPORTED" if rows and any(x["logging"] != ["NOT_EVIDENCED"] for x in rows) else "UNKNOWN",
            "event_ids": [x["failure_id"] for x in rows], "evidence": uniq(ev for x in rows for ev in x["evidence"]),
        })

failure_stage_model: list[dict[str, Any]] = []
stage_queries = {
    "INPUT": r"seed|prompt|location\.href", "VALIDATION": r"canonicalizeUrl|isAllowedUrl|new\s+URL",
    "ACQUISITION": r"GM_xmlhttpRequest|\bfetch\s*\(", "OBSERVATION": r"class\s+Observation|addObservation",
    "RECOGNITION": r"recognize|ProviderRegistry", "DISCOVERY": r"class\s+Discovery|addDiscovery",
    "EXPANSION": r"candidates\s*\(|CandidateExtractor|emitDiscovery", "SCHEDULING": r"Scheduler|claimNextCandidate|worker",
    "PERSISTENCE": r"persist|restore|GM_setValue|localStorage", "EXPORT": r"\bexport\s*\(|createObjectURL",
    "UI": r"installUI|innerHTML|addEventListener", "CROSS_CUTTING": r"try\s*\{|catch\s*\(",
}
for snapshot in snapshots:
    sid = snapshot["snapshot_id"]
    for stage in STAGES:
        rows = [x for x in failure_events if x["snapshot_id"] == sid and x["stage"] == stage]
        stage_match = first_match(sid, stage_queries[stage])
        refs = uniq(ev for x in rows for ev in x["evidence"])
        if not refs:
            refs = [match_ev(sid, stage_match, f"{stage} stage boundary")] if stage_match else [absence_ev(sid, stage_queries[stage], f"{stage} stage not evidenced")]
        failure_stage_model.append({
            "snapshot_id": sid, "version": snapshot["historical_version"], "variant": snapshot["variant"], "stage": stage,
            "failure_sources": sorted({x["failure_type"] for x in rows}) or ["UNKNOWN_FAILURE"],
            "detection_points": sorted({x["detection"] for x in rows}) or ["UNKNOWN"],
            "representations": sorted({x["representation"] for x in rows}) or ["UNKNOWN"],
            "propagation": sorted({x["propagation"] for x in rows}) or ["UNKNOWN"],
            "containment": sorted({x["containment"] for x in rows}) or ["UNKNOWN"],
            "recovery": sorted({x["recovery"] for x in rows}) or ["UNKNOWN"],
            "logging": sorted({v for x in rows for v in x["logging"]}) or ["UNKNOWN"],
            "provenance": sorted({x["provenance_effect"] for x in rows}) or ["UNKNOWN"],
            "evidence": refs,
        })

# --- Retry, timeout, cancellation -------------------------------------------
def config_object(snapshot_id: str) -> tuple[dict[str, dict[str, Any]], int | None]:
    syntax = syntax_masks[snapshot_id]; text = texts[snapshot_id]
    m = re.search(r"\b(?:const|let|var)\s+CONFIG\s*=\s*\{", syntax)
    if not m: return {}, None
    end = brace_end(syntax, m.end()-1)
    if not end: return {}, None
    values: dict[str, dict[str, Any]] = {}
    body_start = m.end()
    # nested keys are retained with lexical path unknown; exact occurrence identity is primary.
    for km in re.finditer(r"(?m)^\s*([A-Za-z_$][\w$]*)\s*:\s*([^,\r\n}]+)", text[body_start:end-1]):
        start = body_start + km.start(1)
        name = km.group(1)
        values.setdefault(name, {"value": brief(km.group(2)), "offset": start, "evidence": source_ev(snapshot_id, start, body_start + km.end(2), f"CONFIG.{name} occurrence")})
    return values, end

configs: dict[str, dict[str, dict[str, Any]]] = {}
config_ends: dict[str, int | None] = {}
for s in snapshots:
    configs[s["snapshot_id"]], config_ends[s["snapshot_id"]] = config_object(s["snapshot_id"])

retry_history = []
timeout_history = []
cancellation_history = []
for snapshot in snapshots:
    sid = snapshot["snapshot_id"]; code = comment_masks[sid]; cfg = configs[sid]
    max_retry = cfg.get("maxRetries")
    enforcement = first_match(sid, r"(?:attempts?|retryCount)\s*(?:<|<=)\s*(?:CONFIG\.)?(?:retry\.)?maxRetries|(?:CONFIG\.)?(?:retry\.)?maxRetries\s*(?:>|>=)\s*(?:attempts?|retryCount)")
    retry_action = first_match(sid, r"(?:queueCandidate|addCandidate|scheduler\.add|\.queue\.push)\s*\([^)]*(?:candidate|item)|\bretry\s*\(")
    delay_match = first_match(sid, r"(?:retryBaseDelay|baseDelay)[\s\S]{0,180}(?:Math\.pow\s*\(\s*2|2\s*\*\*|attempts?)|setTimeout\s*\([^,]+,\s*[^)]*(?:retry|delay|backoff)")
    if delay_match and re.search(r"Math\.random", code[max(0, delay_match.start()-300):delay_match.end()+300], re.I): backoff = "RANDOMIZED"
    elif delay_match and re.search(r"Math\.pow\s*\(\s*2|2\s*\*\*", delay_match.group(0), re.I): backoff = "EXPONENTIAL"
    elif delay_match and re.search(r"attempt", delay_match.group(0), re.I): backoff = "LINEAR_OR_EXPONENTIAL_EXPRESSION_REQUIRES_LOCAL_READING"
    elif cfg.get("retryBaseDelay") or cfg.get("baseDelay"): backoff = "CONFIGURED_DELAY_ENFORCEMENT_UNKNOWN" if not delay_match else "FIXED"
    else: backoff = "NONE_EVIDENCED"
    retry_exists = bool(enforcement and retry_action)
    refs = []
    if max_retry: refs.append(max_retry["evidence"])
    if enforcement: refs.append(match_ev(sid, enforcement, "retry count enforcement"))
    if retry_action: refs.append(match_ev(sid, retry_action, "retry/requeue action"))
    if delay_match: refs.append(match_ev(sid, delay_match, "retry delay/backoff"))
    if not refs: refs.append(absence_ev(sid, "maxRetries|retryCount|requeue", "retry not evidenced"))
    retry_history.append({
        "snapshot_id": sid, "version": snapshot["historical_version"], "variant": snapshot["variant"],
        "retry": "IMPLEMENTED" if retry_exists else ("CONFIGURED_WITHOUT_COMPLETE_PATH_PROOF" if max_retry else "NOT_EVIDENCED"),
        "trigger": "HANDLED_CANDIDATE_OR_ACQUISITION_FAILURE" if retry_exists else "UNKNOWN", "count": max_retry["value"] if max_retry else "UNKNOWN",
        "backoff": backoff, "same_candidate": "SUPPORTED" if retry_exists and retry_action and re.search(r"candidate|item", retry_action.group(0), re.I) else "UNKNOWN",
        "same_provider": "UNKNOWN", "new_acquisition": "SUPPORTED_BY_REQUEUED_PROCESSING_PATH" if retry_exists else "UNKNOWN",
        "terminal_failure": "SUPPORTED" if enforcement and re.search(r"fail|failed|terminal", code[enforcement.start():enforcement.start()+1000], re.I) else "UNKNOWN",
        "recursion_is_retry": False, "evidence": uniq(refs),
    })
    request_timeout = cfg.get("requestTimeout")
    timeout_callback = first_match(sid, r"\bontimeout\s*(?::|=)")
    controller = first_match(sid, r"new\s+AbortController\s*\(")
    timer_abort = first_match(sid, r"setTimeout\s*\([\s\S]{0,240}\.abort\s*\(")
    refs = ([request_timeout["evidence"]] if request_timeout else [])
    for mm, claim in [(timeout_callback, "timeout callback"), (controller, "AbortController timeout/cancellation mechanism"), (timer_abort, "timer-triggered abort")]:
        if mm: refs.append(match_ev(sid, mm, claim))
    timeout_history.append({
        "snapshot_id": sid, "version": snapshot["historical_version"], "variant": snapshot["variant"],
        "timeout_scope": "REQUEST_TIMEOUT" if request_timeout else "ABSENT_OR_UNKNOWN",
        "configured_value": request_timeout["value"] if request_timeout else None,
        "detection": "TIMEOUT_CALLBACK" if timeout_callback else ("TIMER_ABORT" if timer_abort else "UNKNOWN"),
        "cancellation": "ABORTCONTROLLER_PATH" if timer_abort and controller else ("USERSCRIPT_API_TIMEOUT_PLATFORM_BEHAVIOR" if timeout_callback else "UNKNOWN"),
        "cleanup": "SUPPORTED_TIMER_CLEAR" if first_match(sid, r"clearTimeout\s*\(") else "UNKNOWN",
        "retry": next(x["retry"] for x in retry_history if x["snapshot_id"] == sid),
        "failure_recording": "SUPPORTED" if any(x["snapshot_id"] == sid and x["failure_type"] == "TIMEOUT" for x in failure_events) else "UNKNOWN",
        "candidate_timeout": "NOT_EVIDENCED", "worker_timeout": "NOT_EVIDENCED", "scan_timeout": "NOT_EVIDENCED", "global_timeout": "NOT_EVIDENCED",
        "evidence": uniq(refs) or [absence_ev(sid, "requestTimeout|ontimeout|AbortController", "timeout not evidenced")],
    })
    stop_flag = first_match(sid, r"(?:stopRequested|\bstop\s*\(\s*\)\s*\{)")
    abort_call = first_match(sid, r"\.abort\s*\(")
    ui_stop = first_match(sid, r"(?:gd-stop|data-action=[\"']stop|>\s*Stop\s*<)")
    refs = []
    for mm, claim in [(stop_flag, "manual stop/flag"), (abort_call, "abort call"), (ui_stop, "UI stop control")]:
        if mm: refs.append(match_ev(sid, mm, claim))
    cancellation_history.append({
        "snapshot_id": sid, "version": snapshot["historical_version"], "variant": snapshot["variant"],
        "mechanism": "ABORTCONTROLLER" if abort_call else ("MANUAL_STOP_FLAG" if stop_flag else "NONE_EVIDENCED"),
        "ui": "CONTROL_PRESENT" if ui_stop else "NOT_EVIDENCED", "scheduler": "FLAG_OR_RUNNING_STATE" if stop_flag else "NOT_EVIDENCED",
        "worker": "LOOP_OBSERVES_FLAG" if stop_flag and first_match(sid, r"while\s*\([^)]*(?:running|stopRequested)") else "UNKNOWN",
        "candidate": "NO_PER_CANDIDATE_TOKEN_EVIDENCED", "acquisition": "ABORT_CALL_PRESENT" if abort_call else "NOT_EVIDENCED",
        "provider": "NOT_EVIDENCED", "underlying_operation_cancelled": "SUPPORTED_ON_ABORT_PATH_ONLY" if abort_call else "UNKNOWN",
        "stop_button_is_not_proof": True, "evidence": uniq(refs) or [absence_ev(sid, r"AbortController|stopRequested|\.abort\s*\(", "cancellation mechanism not evidenced")],
    })

# --- Resource bounds and exhaustion -----------------------------------------
BOUND_SPECS = {
    "maxCandidates": "CANDIDATE_FRONTIER", "maxRequests": "SCAN_REQUEST_COUNT", "concurrency": "WORKER_COUNT",
    "requestTimeout": "REQUEST_DURATION", "maxResponseBytes": "RESPONSE_BODY", "maxBodyChars": "RESPONSE_BODY",
    "maxDepth": "EXPANSION_DEPTH", "maxRetries": "RETRY_COUNT", "retryMaxDelay": "RETRY_DELAY",
    "maxRequestsPerOrigin": "ORIGIN_REQUEST_COUNT", "maxConcurrentPerOrigin": "ORIGIN_CONCURRENCY",
    "minRequestInterval": "ORIGIN_RATE", "maxPersistedDiscoveries": "PERSISTED_DISCOVERIES",
    "persistedDiscoveries": "PERSISTED_DISCOVERIES", "maxPersistedResources": "PERSISTED_RESOURCES",
    "persistedResources": "PERSISTED_RESOURCES", "maxPersistedEdges": "PERSISTED_EDGES", "persistedEdges": "PERSISTED_EDGES",
    "maxNetworkEvents": "NETWORK_EVENT_RETENTION", "maxGraphEdges": "GRAPH_EDGE_RETENTION",
    "maxDiagnostics": "DIAGNOSTIC_RETENTION", "maxUrlsPerDiscovery": "EXPANSION_FANOUT",
    "maxTextPreview": "TEXT_RETENTION", "maxStoredTextPreview": "TEXT_RETENTION", "fingerprintMaxChars": "FINGERPRINT_INPUT",
}
resource_bounds = []
for snapshot in snapshots:
    sid = snapshot["snapshot_id"]; cfg = configs[sid]; code = comment_masks[sid]; cfg_end = config_ends[sid] or 0
    for key, scope in BOUND_SPECS.items():
        if key not in cfg: continue
        uses = list(re.finditer(rf"(?:CONFIG\.)?(?:[A-Za-z_$][\w$]*\.)?{re.escape(key)}\b", code[cfg_end:], re.I))
        use = uses[0] if uses else None
        abs_start = cfg_end + use.start() if use else None
        owner, operation, method = owner_at(sid, abs_start) if abs_start is not None else ("CONFIG", "declaration", None)
        context = texts[sid][max(cfg_end, (abs_start or cfg_end)-180):min(len(texts[sid]), (abs_start or cfg_end)+420)]
        if re.search(r"slice\s*\(|substring\s*\(", context, re.I): behavior = "TRUNCATE"
        elif re.search(r"return\s+(?:false|null)|continue|break", context, re.I): behavior = "REJECT_DROP_OR_STOP"
        elif re.search(r"abort\s*\(", context, re.I): behavior = "ABORT"
        elif use: behavior = "ENFORCEMENT_EXPRESSION_PRESENT_OUTCOME_NEEDS_PATH_ANALYSIS"
        else: behavior = "CONFIGURED_ENFORCEMENT_NOT_EVIDENCED"
        refs = [cfg[key]["evidence"]]
        if abs_start is not None: refs.append(source_ev(sid, abs_start, abs_start + len(use.group(0)), f"{key} use/enforcement point"))
        resource_bounds.append({
            "bound_id": stable_id("bound", sid, key), "snapshot_id": sid, "version": snapshot["historical_version"], "variant": snapshot["variant"],
            "bound": key, "value": cfg[key]["value"], "scope": scope, "first_appearance": None,
            "enforcement_point": f"{owner}.{operation}" if use else "NOT_EVIDENCED",
            "enforcement": "PROVED_REFERENCE" if use else "UNKNOWN", "failure_behavior": behavior, "evidence": uniq(refs),
        })
for key in BOUND_SPECS:
    rows = [x for x in resource_bounds if x["bound"] == key]
    if rows:
        first = min((x["version"] for x in rows), key=version_key)
        for x in rows: x["first_appearance"] = first

resource_risks = []
for snapshot in snapshots:
    sid = snapshot["snapshot_id"]
    scopes = {x["scope"]: x for x in resource_bounds if x["snapshot_id"] == sid and x["enforcement"] == "PROVED_REFERENCE"}
    risk_specs = [
        ("unbounded candidate growth", "CANDIDATE_FRONTIER", r"candidates|queue"),
        ("unbounded response body", "RESPONSE_BODY", r"responseText|\.text\s*\("),
        ("unbounded concurrency", "WORKER_COUNT", r"Promise\.all|concurrency"),
        ("recursive/unbounded expansion", "EXPANSION_DEPTH", r"candidates\s*\(|expand|discover"),
        ("memory-retained observations", "SCAN_REQUEST_COUNT", r"observations\s*=\s*new\s+Map"),
        ("large DOM or JSON parse", "RESPONSE_BODY", r"DOMParser|JSON\.parse"),
    ]
    for name, bound_scope, indicator in risk_specs:
        ind = first_match(sid, indicator)
        if not ind: continue
        mitigated = bound_scope in scopes
        resource_risks.append({
            "risk_id": stable_id("resource-risk", sid, name), "snapshot_id": sid, "version": snapshot["historical_version"], "variant": snapshot["variant"],
            "risk": name, "classification": "MITIGATED" if mitigated else "UNMITIGATED",
            "risk_basis": "STATIC_GROWTH_OR_INPUT_PATH_PRESENT", "actual_exhaustion_or_exploit": "NOT_EVIDENCED",
            "mitigation": scopes[bound_scope]["bound"] if mitigated else "NONE_EVIDENCED_FOR_SCOPE",
            "mitigation_limit": "PATH_LOCAL_NOT_SYSTEM_WIDE_GUARANTEE" if mitigated else "UNKNOWN",
            "evidence": [match_ev(sid, ind, f"resource risk indicator: {name}")] + (scopes[bound_scope]["evidence"] if mitigated else []),
        })

# --- Concurrency safety, duplicate processing, and race candidates -----------
STATE_NAMES = ["queue", "claimed", "visited", "candidates", "observations", "discoveries", "providers", "registry"]
concurrency_state = []
claim_safety = []
duplicate_processing = []
race_analysis = []
for snapshot in snapshots:
    sid = snapshot["snapshot_id"]; text = texts[sid]; code = comment_masks[sid]
    for state in STATE_NAMES:
        occurrence = first_match(sid, rf"this\.{state}\s*=|this\.{state}\.(?:set|add|push|delete|clear)|this\.{state}\b")
        if not occurrence: continue
        relevant = [m for m in methods[sid] if re.search(rf"this\.{state}\b|(?:database|knowledgeBase)\.{state}\b", m["body"])]
        writers, readers, await_methods = [], [], []
        refs = [match_ev(sid, occurrence, f"shared state {state}")]
        for method in relevant:
            body = method["body"]
            label = f"{method['class']}.{method['name']}"
            if re.search(rf"(?:this\.{state}|(?:database|knowledgeBase)\.{state})\.(?:set|add|push|delete|clear|shift|splice)\s*\(|this\.{state}\s*=", body): writers.append(label)
            if re.search(rf"(?:this\.{state}|(?:database|knowledgeBase)\.{state})\.(?:has|get|values|size|find|filter)|\.\.\.this\.{state}", body): readers.append(label)
            if "await" in body: await_methods.append(label)
        concurrency_state.append({
            "state_id": stable_id("shared-state", sid, state), "snapshot_id": sid, "version": snapshot["historical_version"], "variant": snapshot["variant"],
            "structure": state, "writers": sorted(set(writers)), "readers": sorted(set(readers)),
            "mutation_timing": "SYNCHRONOUS_METHOD_BODY" if writers else "MUTATION_NOT_LOCATED",
            "await_boundaries": sorted(set(await_methods)), "synchronization": "NO_LOCK_PRIMITIVE_EVIDENCED",
            "ordering_assumptions": "EVENT_LOOP_TASK_ORDER_AND_LOCAL_CALL_ORDER_ONLY",
            "thread_safe_claim": False, "evidence": uniq(refs + [method_ev(sid, m, f"{state} access") for m in relevant[:3]]),
        })
    claim_method = next((m for m in methods[sid] if m["name"] == "claimNextCandidate"), None)
    if not claim_method:
        claim_method = next((m for m in methods[sid] if re.search(r"claimed\.add\s*\(", m["body"]) and re.search(r"candidates\.(?:delete|get|values)", m["body"])), None)
    refs = []
    if claim_method: refs.append(method_ev(sid, claim_method, "candidate claim sequence"))
    claim_body = claim_method["body"] if claim_method else ""
    claim_before_await = bool(claim_method and ("await" not in claim_body or claim_body.find("claimed.add") < claim_body.find("await")))
    checks_claimed = bool(re.search(r"claimed\.(?:has|add)", claim_body))
    removes_queue = bool(re.search(r"candidates\.delete|queue\.(?:shift|splice)", claim_body))
    complete = next((m for m in methods[sid] if m["name"] in {"completeCandidate", "complete"} and re.search(r"claimed|visited", m["body"])), None)
    fail = next((m for m in methods[sid] if m["name"] in {"failCandidate", "fail"} and re.search(r"claimed|retry|attempt", m["body"], re.I)), None)
    for m, label in [(complete, "claim completion ownership"), (fail, "claim failure ownership")]:
        if m: refs.append(method_ev(sid, m, label))
    claim_safety.append({
        "snapshot_id": sid, "version": snapshot["historical_version"], "variant": snapshot["variant"],
        "claim_operation": f"{claim_method['class']}.{claim_method['name']}" if claim_method else "NOT_EVIDENCED",
        "claim_atomicity": "SYNCHRONOUS_EVENT_LOOP_LOCAL_SEQUENCE" if claim_before_await and (checks_claimed or removes_queue) else "UNKNOWN",
        "claim_ownership": "SUPPORTED_LOCAL_CLAIM_SET_OR_QUEUE_REMOVAL" if checks_claimed or removes_queue else "UNKNOWN",
        "processing_exclusivity": "SUPPORTED_FOR_RECOVERED_WORKER_PATH" if claim_before_await and checks_claimed else "UNKNOWN",
        "completion_ownership": f"{complete['class']}.{complete['name']}" if complete else "UNKNOWN",
        "failure_ownership": f"{fail['class']}.{fail['name']}" if fail else "UNKNOWN",
        "requeue": next(x["retry"] for x in retry_history if x["snapshot_id"] == sid),
        "cross_await_atomicity": "NOT_CLAIMED", "thread_safety": "NOT_ESTABLISHED", "distributed_atomicity": "NOT_ESTABLISHED",
        "evidence": uniq(refs) or [absence_ev(sid, "claimNextCandidate|claimed.add", "claim operation not evidenced")],
    })
    identity = first_match(sid, r"candidateKey\s*\(|\.key\s*\(\)|canonicalizeUrl\s*\(")
    visited = first_match(sid, r"visited\.(?:has|add)\s*\(")
    dup_refs = []
    for mm, claim in [(identity, "candidate identity/dedup key"), (visited, "visited duplicate prevention"), (first_match(sid, r"claimed\.(?:has|add)\s*\("), "claimed duplicate prevention")]:
        if mm: dup_refs.append(match_ev(sid, mm, claim))
    duplicate_processing.append({
        "snapshot_id": sid, "version": snapshot["historical_version"], "variant": snapshot["variant"],
        "duplicate_seeds": "LOCALLY_MITIGATED" if identity else "UNKNOWN", "duplicate_discoveries": "LOCALLY_MITIGATED" if identity else "UNKNOWN",
        "multiple_workers": "LOCALLY_MITIGATED" if claim_before_await and checks_claimed else "POSSIBLE",
        "retry_requeue": "POSSIBLE_BY_DESIGN" if next(x["retry"] for x in retry_history if x["snapshot_id"] == sid) == "IMPLEMENTED" else "UNKNOWN",
        "normalization_mismatch": "POSSIBLE_NOT_DEMONSTRATED", "claim_timing": "MITIGATED_ON_RECOVERED_PATH" if claim_before_await else "UNKNOWN",
        "global_uniqueness_guarantee": "NOT_ESTABLISHED", "evidence": uniq(dup_refs),
    })
    # Await-bearing state mutators are potential interleavings, never demonstrated races here.
    for method in methods[sid]:
        if "await" not in method["body"]: continue
        touched = [state for state in STATE_NAMES if re.search(rf"(?:this|database|knowledgeBase)\.{state}\b", method["body"])]
        for state in touched[:3]:
            before, after = method["body"].split("await", 1)
            if re.search(rf"\.{state}\b", before) or re.search(rf"\.{state}\b", after):
                race_analysis.append({
                    "race_id": stable_id("race", sid, method["class"], method["name"], state), "snapshot_id": sid,
                    "version": snapshot["historical_version"], "shared_state": state,
                    "operation_a": f"{method['class']}.{method['name']} before await", "operation_b": "another event-loop continuation touching shared state",
                    "interleaving": "POSSIBLE_AT_AWAIT_BOUNDARY", "observable_consequence": "UNKNOWN_NOT_DEMONSTRATED",
                    "mitigation": "claim-before-await" if claim_before_await and state in {"queue", "claimed", "candidates"} else "UNKNOWN",
                    "classification": "THEORETICAL_INTERLEAVING_NOT_DEMONSTRATED_FAILURE", "evidence": [method_ev(sid, method, f"await boundary with {state} state")],
                })

# --- Data and provenance integrity -------------------------------------------
data_integrity = []
provenance_integrity = []
integrity_weaknesses = []
for snapshot in snapshots:
    sid = snapshot["snapshot_id"]
    field_matches = {name: first_match(sid, rf"this\.{name}\s*=", re.I) for name in ["candidateId", "observationId", "parent", "provenance", "status"]}
    fields = {name: bool(value) for name, value in field_matches.items()}
    has_claim = next(x for x in claim_safety if x["snapshot_id"] == sid)
    has_dedup = next(x for x in duplicate_processing if x["snapshot_id"] == sid)
    base_ref = class_ev(sid, "KnowledgeBase", "data integrity state owner") or source_ev(sid, 0, min(1, len(texts[sid])), "snapshot scope")
    conditions = [
        ("orphaned observations", "POSSIBLE" if fields["candidateId"] else "UNKNOWN", "No foreign-key enforcement is evidenced.", [match_ev(sid, field_matches["candidateId"], "Observation candidate reference") ] if field_matches["candidateId"] else [base_ref]),
        ("orphaned discoveries", "POSSIBLE" if fields["observationId"] else "UNKNOWN", "Identifiers are stored but referential enforcement is not proved.", [match_ev(sid, field_matches["observationId"], "Discovery observation reference")] if field_matches["observationId"] else [base_ref]),
        ("duplicate candidates", "PREVENTED" if has_dedup["duplicate_seeds"] == "LOCALLY_MITIGATED" else "POSSIBLE", "Local key/visited path only.", has_dedup["evidence"] or [base_ref]),
        ("lost provenance", "POSSIBLE" if fields["provenance"] or fields["parent"] else "UNKNOWN", "Presence of fields does not guarantee preservation at every boundary.", [match_ev(sid, field_matches[name], f"{name} provenance field") for name in ["provenance", "parent"] if field_matches[name]] or [base_ref]),
        ("partial records", "POSSIBLE", "Incremental mutable object construction and persistence are present.", [base_ref]),
        ("inconsistent status", "POSSIBLE" if fields["status"] else "UNKNOWN", "Multiple mutation paths; no exhaustive state machine verification.", [match_ev(sid, field_matches["status"], "mutable status field")] if field_matches["status"] else [base_ref]),
        ("stale claims", "PREVENTED" if has_claim["completion_ownership"] != "UNKNOWN" and has_claim["failure_ownership"] != "UNKNOWN" else "POSSIBLE", "Only handled completion/failure paths are covered.", has_claim["evidence"]),
    ]
    for condition, status, caveat, condition_refs in conditions:
        data_integrity.append({
            "integrity_id": stable_id("integrity", sid, condition), "snapshot_id": sid, "version": snapshot["historical_version"],
            "variant": snapshot["variant"], "condition": condition, "classification": status,
            "scope": "RECOVERED_STATIC_PATHS", "caveat": caveat, "runtime_failure_observed": False, "evidence": uniq(condition_refs),
        })
    edge_specs = [
        ("Discovery", "Observation", "observationId", "EXPLICIT_STORED_IDENTIFIER"),
        ("Observation", "Candidate", "candidateId", "EXPLICIT_STORED_IDENTIFIER"),
        ("Candidate", "Parent Candidate", "parent", "STORED_REFERENCE"),
        ("Parent Candidate", "Seed", "origin", "STORED_ORIGIN_LABEL_SEED_RECONSTRUCTION_UNKNOWN"),
    ]
    edges = []
    refs = []
    for src, dst, field, present_status in edge_specs:
        m = first_match(sid, rf"(?:this\.)?{field}\s*=")
        if m:
            status = present_status; ev = match_ev(sid, m, f"provenance edge {src} to {dst}")
            refs.append(ev)
        else:
            status = "MISSING_OR_NOT_EVIDENCED"; ev = absence_ev(sid, rf"{field}\s*=", f"provenance edge {src} to {dst} absent")
        edges.append({"from": src, "to": dst, "field": field, "status": status, "evidence": [ev]})
    provenance_integrity.append({
        "snapshot_id": sid, "version": snapshot["historical_version"], "variant": snapshot["variant"], "edges": edges,
        "end_to_end_traceability": "PARTIAL" if any(x["status"].startswith("EXPLICIT_STORED") or x["status"] == "STORED_REFERENCE" for x in edges) else "UNKNOWN",
        "integrity_guarantee": "NOT_ESTABLISHED", "evidence": uniq(refs + [e for x in edges for e in x["evidence"]]),
    })
    for surface, pattern in [
        ("provenance overwrite", r"(?:candidate|discovery|observation)\.provenance\s*="),
        ("parent reassignment", r"(?:candidate|discovery)\.parent\s*="),
        ("observation replacement", r"observations\.set\s*\("),
        ("timestamp modification", r"(?:createdAt|completedAt|startedAt)\s*="),
    ]:
        m = first_match(sid, pattern)
        if m:
            integrity_weaknesses.append({
                "weakness_id": stable_id("integrity-weakness", sid, surface), "snapshot_id": sid, "version": snapshot["historical_version"],
                "surface": surface, "classification": "INTEGRITY_WEAKNESS", "malicious_tampering_claimed": False,
                "authority": owner_at(sid, m.start())[0], "evidence": [match_ev(sid, m, f"mutable integrity surface: {surface}")],
            })

# --- Trust boundaries, authority, permissions, URL trust ---------------------
def metadata_directives(snapshot: dict[str, Any]) -> dict[str, list[str]]:
    return snapshot.get("static_validation", {}).get("userscript_metadata", {}).get("directives", {})

permission_history = []
trust_boundaries = []
authority_history = []
origin_scope = []
url_trust = []

for snapshot in snapshots:
    sid = snapshot["snapshot_id"]; directives = metadata_directives(snapshot); code = comment_masks[sid]
    header_match = first_match(sid, r"//\s*==UserScript==[\s\S]*?//\s*==/UserScript==", flags=re.I, commentless=False)
    header_ref = match_ev(sid, header_match, "userscript metadata permissions") if header_match else absence_ev(sid, "==UserScript==", "userscript header absent")
    permission_history.append({
        "snapshot_id": sid, "version": snapshot["historical_version"], "variant": snapshot["variant"],
        "include": directives.get("include", []), "match": directives.get("match", []), "grant": directives.get("grant", []),
        "connect": directives.get("connect", []), "require": directives.get("require", []), "resource": directives.get("resource", []),
        "metadata_scope_interpretation": "LITERAL_DIRECTIVES_ONLY", "malformed_or_markdown_affected": any("_" in x for x in directives.get("match", [])),
        "evidence": [header_ref],
    })
    mechanisms = {
        "DOM": first_match(sid, r"document\.(?:querySelector|querySelectorAll|documentElement|body)|DOMParser"),
        "NETWORK": first_match(sid, r"GM_xmlhttpRequest|\bfetch\s*\("),
        "REMOTE_CONTENT": first_match(sid, r"responseText|response\.text\s*\(|observation\.(?:features\.)?body"),
        "PROVIDER": first_match(sid, r"class\s+(?:\w*Provider|\w*Recognizer)\b|ProviderRegistry"),
        "SCHEDULER": first_match(sid, r"class\s+(?:\w*Scheduler|OriginController)|claimNextCandidate"),
        "STORAGE": first_match(sid, r"GM_(?:get|set)Value|localStorage"),
        "EXPORT": first_match(sid, r"\bexport\s*\(|JSON\.stringify|createObjectURL"),
        "UI": first_match(sid, r"createElement\s*\(\s*['\"](?:div|button)|innerHTML|addEventListener\s*\(\s*['\"]click"),
        "BROWSER_API": first_match(sid, r"\b(?:fetch|DOMParser|URL|PerformanceObserver|MutationObserver)\b"),
        "USERSCRIPT_API": first_match(sid, r"\bGM_[A-Za-z_$]+"),
        "USER_INPUT": first_match(sid, r"prompt\s*\(|<input|\.value\b"),
        "THIRD_PARTY_LIBRARY": first_match(sid, r"@require\b|\bimport\s+[^(']|require\s*\("),
    }
    specs = {
        "USER_INPUT": ("user/UI event", "validation/engine", "seed or control value", "UI event authority"),
        "PAGE_DOM": ("page DOM", "candidate extraction", "links/forms/resources/metadata", "browser DOM read"),
        "NETWORK": ("remote server", "acquisition", "request/response", "GM/fetch network authority"),
        "REMOTE_CONTENT": ("acquisition response", "provider/parser", "HTML/JSON/text/headers", "parse and extraction authority"),
        "PROVIDER_CODE": ("provider implementation", "registry/engine", "recognition and discovery results", "provider method execution"),
        "SCHEDULER": ("candidate frontier", "worker", "claim/work state", "work admission authority"),
        "STORAGE": ("in-memory state", "GM/local storage", "serialized state", "storage read/write authority"),
        "EXPORT": ("engine state", "download/consumer", "JSON/blob", "state disclosure authority"),
        "UI": ("engine state", "page DOM/user", "status/results/controls", "DOM mutation authority"),
        "BROWSER_APIS": ("engine", "browser API", "DOM/network/timers", "ambient browser authority"),
        "USERSCRIPT_APIS": ("engine", "userscript manager", "privileged network/storage", "metadata-granted authority"),
        "THIRD_PARTY_LIBRARIES": ("external library", "engine", "code/data", "dependency execution authority"),
    }
    map_key = {"PAGE_DOM":"DOM", "PROVIDER_CODE":"PROVIDER", "BROWSER_APIS":"BROWSER_API", "USERSCRIPT_APIS":"USERSCRIPT_API", "THIRD_PARTY_LIBRARIES":"THIRD_PARTY_LIBRARY"}
    for boundary, (source, sink, data, authority) in specs.items():
        key = map_key.get(boundary, boundary)
        m = mechanisms.get(key)
        present = bool(m)
        if boundary in {"SCHEDULER"}: kind = "INTERNAL_AUTHORITY_BOUNDARY_NOT_PROVED_TRUST"
        elif boundary in {"NETWORK", "REMOTE_CONTENT", "USERSCRIPT_APIS", "PAGE_DOM", "STORAGE"} and present: kind = "HISTORICAL_TRUST_OR_AUTHORITY_BOUNDARY"
        elif present: kind = "DATA_OR_AUTHORITY_BOUNDARY"
        else: kind = "NOT_PRESENT_OR_NOT_EVIDENCED"
        if m:
            ref = match_ev(sid, m, f"{boundary} boundary")
        else:
            query = {"USER_INPUT":r"prompt|input\.value", "THIRD_PARTY_LIBRARIES":r"@require|\bimport\b|require\s*\("}.get(boundary, key)
            ref = absence_ev(sid, query, f"{boundary} boundary not evidenced")
        validation = "URL_CANONICALIZATION_OR_ALLOW_CHECK" if boundary in {"PAGE_DOM", "NETWORK"} and first_match(sid, r"canonicalizeUrl|isAllowedUrl") else ("PARSER_OR_PROVIDER_HEURISTIC" if boundary == "REMOTE_CONTENT" and present else "UNKNOWN")
        isolation = "CATCH_PATHS_PRESENT_NOT_GUARANTEE" if boundary == "PROVIDER_CODE" and first_match(sid, r"class\s+ProviderRegistry[\s\S]{0,5000}\bcatch\b") else "UNKNOWN"
        sanitization = "EXTRACTION_OR_NORMALIZATION_ONLY" if boundary in {"PAGE_DOM", "REMOTE_CONTENT"} and present else "UNKNOWN"
        trust_boundaries.append({
            "boundary_id": stable_id("trust-boundary", sid, boundary), "snapshot_id": sid, "version": snapshot["historical_version"], "variant": snapshot["variant"],
            "boundary": boundary, "source": source, "sink": sink, "data": data, "validation": validation,
            "authority": authority if present else "NOT_EVIDENCED", "sanitization": sanitization, "isolation": isolation,
            "boundary_status": kind, "security_guarantee": "NOT_ESTABLISHED", "evidence": [ref],
        })
    authority_specs = [
        ("network request", r"GM_xmlhttpRequest|\bfetch\s*\(", "Acquisition/adapter or engine"),
        ("candidate insertion", r"addCandidate\s*\(|queueCandidate\s*\(", "KnowledgeBase/scheduler/engine"),
        ("candidate claim", r"claimNextCandidate\s*\(|claimed\.add\s*\(", "KnowledgeBase/scheduler"),
        ("provider registration", r"new\s+\w*Provider\s*\(", "ProviderRegistry/composition root"),
        ("state mutation", r"(?:candidates|observations|discoveries)\.(?:set|delete|clear)\s*\(", "KnowledgeBase/engine"),
        ("export", r"\bexport\s*\(|createObjectURL", "Engine/UI"),
        ("configuration", r"\bCONFIG\b", "global userscript scope"),
    ]
    for operation, pattern, expected in authority_specs:
        m = first_match(sid, pattern)
        if not m: continue
        owner, method, _ = owner_at(sid, m.start())
        authority_history.append({
            "authority_id": stable_id("authority", sid, operation), "snapshot_id": sid, "version": snapshot["historical_version"],
            "variant": snapshot["variant"], "operation": operation, "authority_required": expected,
            "authority_granted": "GLOBAL_OR_AMBIENT" if operation in {"network request", "configuration"} else f"{owner}.{method}",
            "authority_used": f"{owner}.{method}", "unnecessarily_exposed": "POSSIBLE" if operation == "configuration" or (operation == "network request" and "*" in directives.get("connect", [])) else "UNKNOWN",
            "least_authority": "NOT_ESTABLISHED", "capability_like_pattern": "CAPABILITY_LIKE_PATTERN" if owner not in {"TOP_LEVEL", "CONFIG"} and operation in {"network request", "candidate insertion", "candidate claim"} else "NOT_EVIDENCED",
            "formal_capability_system": False, "evidence": [match_ev(sid, m, f"authority for {operation}")],
        })
    canonical = first_match(sid, r"function\s+canonicalizeUrl|canonicalizeUrl\s*\(")
    allowed = first_match(sid, r"function\s+isAllowedUrl|isAllowedUrl\s*\(")
    scheme = first_match(sid, r"protocol\s*(?:===|!==|==|!=)|https?:")
    origin = first_match(sid, r"sameOriginOnly|\.origin\s*(?:===|!==)")
    credentials = first_match(sid, r"\.username|\.password|credentials\s*:")
    refs = []
    for mm, claim in [(canonical, "URL canonicalization"), (allowed, "URL admission"), (scheme, "URL scheme check"), (origin, "origin check"), (credentials, "credential handling")]:
        if mm: refs.append(match_ev(sid, mm, claim))
    url_trust.append({
        "snapshot_id": sid, "version": snapshot["historical_version"], "variant": snapshot["variant"],
        "discovered_to_candidate": "CANONICALIZED" if canonical else "UNKNOWN", "candidate_to_acquisition": "ALLOW_CHECK_PRESENT" if allowed else "DIRECT_OR_UNKNOWN",
        "scheme": "EXPLICIT_CHECK" if scheme else "NOT_EVIDENCED", "origin": "CONFIGURABLE_ORIGIN_CHECK" if origin else "NOT_EVIDENCED",
        "host": "URL_ORIGIN_ONLY" if origin else "NOT_EVIDENCED", "port": "NOT_SEPARATELY_VALIDATED", "redirect": "UNKNOWN",
        "credentials": "EXPLICIT_HANDLING" if credentials else "UNKNOWN", "local_addresses": "NOT_EVIDENCED",
        "javascript_scheme": "EXPLICITLY_BLOCKED_ONLY_IF_SCHEME_CHECK" if scheme else "UNKNOWN", "data_scheme": "EXPLICITLY_BLOCKED_ONLY_IF_SCHEME_CHECK" if scheme else "UNKNOWN",
        "file_scheme": "EXPLICITLY_BLOCKED_ONLY_IF_SCHEME_CHECK" if scheme else "UNKNOWN", "blob_scheme": "EXPLICITLY_BLOCKED_ONLY_IF_SCHEME_CHECK" if scheme else "UNKNOWN",
        "url_parser_is_not_policy": True, "evidence": uniq(refs) or [absence_ev(sid, "canonicalizeUrl|isAllowedUrl|URL.protocol", "URL validation not evidenced")],
    })
    gm = bool(first_match(sid, r"GM_xmlhttpRequest")); fetch = bool(first_match(sid, r"\bfetch\s*\(")); dom = bool(first_match(sid, r"document\."))
    scope = []
    if dom: scope.append("CURRENT_PAGE_DOM")
    if fetch: scope.append("BROWSER_FETCH_TO_ADMITTED_URL")
    if gm: scope.append("GM_PRIVILEGED_REQUEST_TO_ADMITTED_URL")
    origin_scope.append({
        "snapshot_id": sid, "version": snapshot["historical_version"], "variant": snapshot["variant"], "historical_scope": scope,
        "default_policy": "SAME_ORIGIN_CONFIG_PRESENT" if "sameOriginOnly" in configs[sid] else "UNKNOWN",
        "metadata_authority": "ARBITRARY_CONNECT_TARGETS" if "*" in directives.get("connect", []) else directives.get("connect", []) or "UNKNOWN",
        "authority_used": "DISCOVERED_RESOURCES_PASSING_RECOVERED_POLICY", "current_page_to_arbitrary_evolution": "ALREADY_BOTH_PRESENT" if dom and (gm or fetch) else "UNKNOWN",
        "redirect_detection": "NOT_EVIDENCED", "redirect_destination_validation": "UNKNOWN", "credential_forwarding": "UNKNOWN",
        "evidence": uniq([header_ref] + evidence_for_match(sid, r"GM_xmlhttpRequest|\bfetch\s*\(", "acquisition authority")),
    })

# --- Code/data boundary and parser safety ------------------------------------
code_data_history = []
parser_history = []
regex_risks = []
for snapshot in snapshots:
    sid = snapshot["snapshot_id"]; code = comment_masks[sid]
    eval_m = first_match(sid, r"\beval\s*\(")
    func_m = first_match(sid, r"\bnew\s+Function\s*\(")
    inner = first_match(sid, r"\.innerHTML\s*=")
    script = first_match(sid, r"createElement\s*\(\s*['\"]script['\"]")
    dynamic_import = first_match(sid, r"\bimport\s*\(")
    sinks = []
    refs = []
    for name, mm in [("eval", eval_m), ("Function", func_m), ("innerHTML", inner), ("script insertion", script), ("dynamic import", dynamic_import)]:
        if mm:
            sinks.append(name); refs.append(match_ev(sid, mm, f"code/data sink {name}"))
    acquired_exec = bool((eval_m or func_m or dynamic_import) and first_match(sid, r"responseText|observation\.(?:features\.)?body"))
    static_bridge = bool(script and first_match(sid, r"script\.textContent\s*=\s*`[\s\S]{0,3000}(?:fetch|XMLHttpRequest)"))
    code_data_history.append({
        "snapshot_id": sid, "version": snapshot["historical_version"], "variant": snapshot["variant"], "sinks": sinks,
        "acquired_content_to_code_path": "EVIDENCED" if acquired_exec else "NO_EVIDENCE_OF_CODE_EXECUTION",
        "inner_html": "PRESENT_UI_OR_TEMPLATE_SINK_REMOTE_TAINT_NOT_PROVED" if inner else "ABSENT",
        "script_insertion": "STATIC_PAGE_BRIDGE_CODE" if static_bridge else ("PRESENT_SOURCE_UNKNOWN" if script else "ABSENT"),
        "html_extraction_executes_scripts": "NOT_EVIDENCED", "json_strings_executed": "NOT_EVIDENCED",
        "absence_is_not_security_guarantee": True,
        "evidence": uniq(refs) or [absence_ev(sid, r"eval\s*\(|new Function|innerHTML|createElement\(['\"]script|import\s*\(", "code/data sinks absent")],
    })
    parser_specs = [
        ("HTML", r"new\s+DOMParser|parseFromString\s*\([^,]+,\s*['\"]text/html", "DOM_CONSTRUCTION"),
        ("XML", r"parseFromString\s*\([^,]+,\s*['\"](?:application|text)/xml|parsererror", "DOM_CONSTRUCTION"),
        ("JSON", r"JSON\.parse\s*\(", "JSON_PARSE"),
        ("TEXT", r"matchAll\s*\(|\.match\s*\(|URL_REGEX|https\?:", "REGEX_OR_TOKEN_EXTRACTION"),
    ]
    for parser, pattern, mechanism in parser_specs:
        mm = first_match(sid, pattern)
        if not mm: continue
        owner, operation, method = owner_at(sid, mm.start()); body = method["body"] if method else ""
        size_bound = next((x for x in resource_bounds if x["snapshot_id"] == sid and x["scope"] in {"RESPONSE_BODY", "TEXT_RETENTION"} and x["enforcement"] == "PROVED_REFERENCE"), None)
        catches = bool(re.search(r"\btry\b|\bcatch\b|parsererror", body, re.I))
        parser_history.append({
            "parser_id": stable_id("parser", sid, parser, mm.start()), "snapshot_id": sid, "version": snapshot["historical_version"], "variant": snapshot["variant"],
            "parser": parser, "owner": f"{owner}.{operation}", "mechanism": mechanism,
            "input_size": size_bound["bound"] if size_bound else "UNBOUNDED_OR_UNKNOWN_AT_PARSER",
            "recursion": "PRESENT" if re.search(r"\b(?:walk|visit|recurse|extract)[A-Za-z]*\s*\(", body) else "NOT_EVIDENCED",
            "dom_construction": parser in {"HTML", "XML"}, "json_parsing": parser == "JSON", "regex_extraction": parser == "TEXT",
            "external_entities": "UNKNOWN", "script_execution": "NO_EVIDENCE_OF_PARSER_SCRIPT_EXECUTION",
            "error_handling": "LOCAL_CHECK_OR_CATCH" if catches else "UNKNOWN", "security_guarantee": "NOT_ESTABLISHED",
            "evidence": [match_ev(sid, mm, f"{parser} parser")],
        })
    # Regex literal inventory: only supported cost risks are elevated; no fabricated ReDoS.
    for rm in re.finditer(r"/(?![/*])(?:\\.|\[(?:\\.|[^\]])*\]|[^/\r\n])+/[dgimsuvy]*", syntax_masks[sid]):
        literal = rm.group(0)
        nested = bool(re.search(r"\([^)]*[+*][^)]*\)[+*]|(?:\.\*|\.\+).*(?:\.\*|\.\+)", literal))
        broad = bool(re.search(r"https\?|\.\*|\\S[+*]", literal, re.I))
        if not (nested or broad): continue
        owner, operation, _ = owner_at(sid, rm.start())
        regex_risks.append({
            "regex_id": stable_id("regex", sid, rm.start()), "snapshot_id": sid, "version": snapshot["historical_version"],
            "owner": f"{owner}.{operation}", "pattern": brief(literal, 240),
            "risk": "SUPPORTED" if nested else "THEORETICAL", "catastrophic_backtracking": "POSSIBLE_PATTERN_SHAPE_NOT_BENCHMARKED" if nested else "NOT_ESTABLISHED",
            "input_bound": "UNKNOWN", "demonstrated": False, "evidence": [match_ev(sid, rm, "regex cost-risk candidate")],
        })

# --- Persistence/export integrity, observability and auditability ------------
persistence_integrity = []
export_integrity = []
observability = []
auditability = []
for snapshot in snapshots:
    sid = snapshot["snapshot_id"]
    storage = first_match(sid, r"GM_setValue|localStorage\.setItem")
    load_m = first_match(sid, r"GM_getValue|localStorage\.getItem")
    serialize = first_match(sid, r"JSON\.stringify")
    parse_m = first_match(sid, r"JSON\.parse")
    persist_refs = []
    for mm, claim in [(storage, "persistence write"), (load_m, "persistence read"), (serialize, "persistence serialization"), (parse_m, "persistence parse")]:
        if mm: persist_refs.append(match_ev(sid, mm, claim))
    persistence_integrity.append({
        "snapshot_id": sid, "version": snapshot["historical_version"], "variant": snapshot["variant"],
        "presence": "PRESENT" if storage or load_m else "NOT_PRESENT", "write_atomicity": "UNKNOWN",
        "partial_writes": "POSSIBLE_PLATFORM_DEPENDENT" if storage else "NOT_PRESENT", "schema_migration": "NOT_EVIDENCED",
        "duplicate_records": "MAP_KEYED_LOCAL_MITIGATION" if first_match(sid, r"new\s+Map\s*\(") else "UNKNOWN",
        "crash_recovery": "UNKNOWN", "serialization": "JSON" if serialize else "UNKNOWN", "load_validation": "PARTIAL_TRY_CATCH" if parse_m else "UNKNOWN",
        "evidence": uniq(persist_refs) or [absence_ev(sid, "GM_setValue|localStorage.setItem", "persistence not present")],
    })
    exp = next((m for m in methods[sid] if m["name"] == "export"), None)
    exp_body = exp["body"] if exp else ""
    fields = []
    for field in ["version", "timestamp", "identity", "provenance", "observations", "discoveries", "errors", "statistics", "graph", "ledger"]:
        if re.search(rf"\b{field}\b", exp_body, re.I): fields.append(field)
    export_integrity.append({
        "snapshot_id": sid, "version": snapshot["historical_version"], "variant": snapshot["variant"], "present": bool(exp),
        "schema": "STRUCTURED_OBJECT" if exp else "UNKNOWN", "fields": fields,
        "independently_interpretable": "PARTIAL" if exp and ("version" in fields or "timestamp" in fields) else "UNKNOWN",
        "relationship_integrity": "PARTIAL" if any(x in fields for x in ["provenance", "graph"]) else "UNKNOWN",
        "errors_exported": "errors" in fields, "partial_state_marked": "NOT_EVIDENCED", "compatibility_guarantee": "NOT_ESTABLISHED",
        "evidence": [method_ev(sid, exp, "export integrity boundary")] if exp else [absence_ev(sid, r"\bexport\s*\(", "export method not evidenced")],
    })
    channels = []
    channel_patterns = [
        ("CONSOLE", r"console\.(?:log|warn|error|table|group)"), ("UI", r"textContent\s*=|render\s*\(|updateUI"),
        ("STRUCTURED_LOG", r"recordDiagnostic|DecisionLedger|diagnostics\.(?:push|set)"), ("OBSERVATION", r"observation\.errors|Observation"),
        ("KNOWLEDGE_BASE", r"addObservation|addDiscovery"), ("EXPORT", r"\bexport\s*\("),
        ("METRICS", r"statistics|stats\.|metrics"), ("TRACE", r"\btrace(?:Id|\s*\()"),
    ]
    refs = []
    for channel, pattern in channel_patterns:
        mm = first_match(sid, pattern)
        if mm:
            channels.append(channel); refs.append(match_ev(sid, mm, f"observability channel {channel}"))
    progression = [x for x in ["CONSOLE" if "CONSOLE" in channels else None, "STRUCTURED_LOG" if "STRUCTURED_LOG" in channels else None,
                                  "STATUS_TRACKING" if "UI" in channels or "OBSERVATION" in channels else None,
                                  "METRICS" if "METRICS" in channels else None, "TRACING" if "TRACE" in channels else None,
                                  "AUDIT_LEDGER" if first_match(sid, r"DecisionLedger") else None] if x]
    observability.append({
        "snapshot_id": sid, "version": snapshot["historical_version"], "variant": snapshot["variant"],
        "channels": channels, "progression_stages_evidenced": progression,
        "failure_detected_not_same_as_observable": True, "evidence": uniq(refs),
    })
    dimensions = {
        "what": bool(channels), "when": bool(first_match(sid, r"timestamp|createdAt|Date\.now")),
        "candidate": bool(first_match(sid, r"candidateId|candidate\.id")), "why": bool(first_match(sid, r"reason|error|diagnostic")),
        "provider": bool(first_match(sid, r"provider(?:Id|Name|\.name)|provider-error")), "observation": bool(first_match(sid, r"observationId|observation\.id")),
        "discovery": bool(first_match(sid, r"discoveryId|discovery\.id")), "failure": bool(first_match(sid, r"errors?|failed|failure")),
    }
    count = sum(dimensions.values())
    auditability.append({
        "snapshot_id": sid, "version": snapshot["historical_version"], "variant": snapshot["variant"], "questions": dimensions,
        "classification": "SUBSTANTIAL" if count >= 7 else ("PARTIAL" if count else "NONE"),
        "verified_by_execution": False, "replay": "EVENT_RECORDS_NOT_REPLAY_GUARANTEE" if first_match(sid, r"DecisionLedger|ledger") else "NOT_EVIDENCED",
        "evidence": uniq(refs[:4] + evidence_for_match(sid, r"candidateId|observationId|provider|error", "audit context")),
    })

# --- Invariants, threats, trust matrix, and evolution -------------------------
security_invariants = []
threat_models = []
for snapshot in snapshots:
    sid = snapshot["snapshot_id"]
    code_data = next(x for x in code_data_history if x["snapshot_id"] == sid)
    claim = next(x for x in claim_safety if x["snapshot_id"] == sid)
    prov = next(x for x in provenance_integrity if x["snapshot_id"] == sid)
    invariant_specs = [
        ("remote content is data", "SUPPORTED" if code_data["acquired_content_to_code_path"] == "NO_EVIDENCE_OF_CODE_EXECUTION" else "UNKNOWN", "SECURITY_PROPERTY", code_data["evidence"]),
        ("provider failure cannot corrupt global state", "UNKNOWN", "SECURITY_ASSUMPTION", evidence_for_match(sid, r"ProviderRegistry", "provider boundary", required=True)),
        ("candidate identity remains stable", "UNKNOWN", "SECURITY_ASSUMPTION", evidence_for_match(sid, r"candidateKey|\.key\s*\(", "candidate identity", required=True)),
        ("provenance cannot be silently lost", "UNKNOWN", "SECURITY_ASSUMPTION", prov["evidence"][:2]),
        ("workers cannot double-claim candidates", "SUPPORTED" if claim["processing_exclusivity"].startswith("SUPPORTED") else "UNKNOWN", "SECURITY_PROPERTY", claim["evidence"]),
        ("bounded concurrency is preserved", "SUPPORTED" if any(x["snapshot_id"] == sid and x["scope"] == "WORKER_COUNT" and x["enforcement"] == "PROVED_REFERENCE" for x in resource_bounds) else "UNKNOWN", "SECURITY_PROPERTY", [x["evidence"][0] for x in resource_bounds if x["snapshot_id"] == sid and x["scope"] == "WORKER_COUNT"][:1] or evidence_for_match(sid, r"concurrency", "concurrency bound", required=True)),
        ("untrusted input cannot execute as code", "UNKNOWN", "SECURITY_ASSUMPTION", code_data["evidence"]),
    ]
    for name, status, ctype, refs in invariant_specs:
        security_invariants.append({
            "invariant_id": stable_id("security-invariant", sid, name), "snapshot_id": sid, "version": snapshot["historical_version"],
            "variant": snapshot["variant"], "invariant": name, "status": status, "claim_type": ctype,
            "mechanism_not_guarantee": True, "historical_test": "NOT_FOUND", "evidence": uniq(refs),
        })
    threat_specs = [
        ("remote content", r"responseText|DOMParser|JSON\.parse", "IMPLICIT_THREAT"),
        ("arbitrary URLs", r"isAllowedUrl|sameOriginOnly", "IMPLICIT_THREAT"),
        ("cross-origin access", r"@connect\s+\*|sameOriginOnly", "IMPLICIT_THREAT"),
        ("resource exhaustion", r"maxCandidates|maxRequests|maxResponseBytes|maxBodyChars", "IMPLICIT_THREAT"),
        ("duplicate processing", r"visited\.has|claimed\.has", "IMPLICIT_THREAT"),
        ("provider failures", r"ProviderRegistry[\s\S]{0,4000}catch", "IMPLICIT_THREAT"),
        ("state corruption", r"persist|restore|failCandidate", "RETROSPECTIVE_THREAT"),
    ]
    threats = []
    for threat, pattern, classification in threat_specs:
        mm = first_match(sid, pattern, flags=re.I|re.S)
        if mm:
            # Only explicit threat/security prose can elevate to EXPLICIT_THREAT.
            nearby = texts[sid][max(0, mm.start()-250):min(len(texts[sid]), mm.end()+250)]
            cls = "EXPLICIT_THREAT" if re.search(r"threat|untrusted|security risk|attack", nearby, re.I) else classification
            threats.append({"threat": threat, "classification": cls, "evidence": [match_ev(sid, mm, f"threat-model evidence: {threat}")]})
    threat_models.append({
        "snapshot_id": sid, "version": snapshot["historical_version"], "variant": snapshot["variant"],
        "threats": threats, "complete_threat_model": "NOT_EVIDENCED", "retrospective_items_do_not_become_historical": True,
        "evidence": uniq(ev for x in threats for ev in x["evidence"]),
    })

trust_matrix = []
for snapshot in snapshots:
    sid = snapshot["snapshot_id"]
    for boundary in ["NETWORK", "PROVIDER_CODE", "SCHEDULER", "STORAGE", "UI"]:
        row = next(x for x in trust_boundaries if x["snapshot_id"] == sid and x["boundary"] == boundary)
        prov = next(x for x in provenance_integrity if x["snapshot_id"] == sid)
        trust_matrix.append({
            "snapshot_id": sid, "version": snapshot["historical_version"], "variant": snapshot["variant"], "boundary": boundary,
            "historical_scope": row["boundary_status"], "validation": "SUPPORTED" if row["validation"] != "UNKNOWN" else "UNKNOWN",
            "isolation": "SUPPORTED" if row["isolation"] != "UNKNOWN" else "UNKNOWN",
            "provenance": "SUPPORTED" if prov["end_to_end_traceability"] == "PARTIAL" else "UNKNOWN",
            "enforcement": "SUPPORTED" if row["boundary_status"] in {"HISTORICAL_TRUST_OR_AUTHORITY_BOUNDARY", "DATA_OR_AUTHORITY_BOUNDARY"} else "UNKNOWN",
            "guarantee": "UNKNOWN", "evidence": uniq(row["evidence"] + prov["evidence"][:1]),
        })

# Branch-preserving adjacent-version comparisons; chronology is not lineage.
version_groups = {v: [x for x in snapshots if x["historical_version"] == v] for v in versions}
def controls_for(sid: str) -> set[str]:
    controls = set()
    if first_match(sid, r"canonicalizeUrl|isAllowedUrl"): controls.add("URL_VALIDATION")
    if first_match(sid, r"ProviderRegistry[\s\S]{0,5000}catch", flags=re.I|re.S): controls.add("PROVIDER_CATCH_PATH")
    if first_match(sid, r"claimNextCandidate|claimed\.add"): controls.add("CANDIDATE_CLAIM")
    if first_match(sid, r"AbortController|\.abort\s*\("): controls.add("ABORT_PATH")
    for x in resource_bounds:
        if x["snapshot_id"] == sid and x["enforcement"] == "PROVED_REFERENCE": controls.add("BOUND:" + x["scope"])
    if first_match(sid, r"provenance|observationId|candidateId"): controls.add("PROVENANCE_FIELDS")
    if first_match(sid, r"DecisionLedger|recordDiagnostic"): controls.add("STRUCTURED_AUDIT")
    return controls

security_changes = []
for before_v, after_v in zip(versions, versions[1:]):
    for before, after in itertools.product(version_groups[before_v], version_groups[after_v]):
        left, right = controls_for(before["snapshot_id"]), controls_for(after["snapshot_id"])
        refs = []
        for sid in [before["snapshot_id"], after["snapshot_id"]]:
            refs += evidence_for_match(sid, r"canonicalizeUrl|ProviderRegistry|claimNextCandidate|AbortController|maxCandidates|provenance|DecisionLedger", "security control comparison", required=True)
        security_changes.append({
            "change_id": stable_id("security-change", before["snapshot_id"], after["snapshot_id"]),
            "before_snapshot": before["snapshot_id"], "after_snapshot": after["snapshot_id"],
            "relationship": "ADJACENT_RECOVERED_VERSION_COMPARISON_NOT_LINEAGE",
            "controls_added": sorted(right-left), "controls_absent_after": sorted(left-right), "controls_shared": sorted(left&right),
            "improvement": "MECHANISM_ADDITION_NOT_GENERIC_SECURITY_SCORE" if right-left else "NONE_EVIDENCED",
            "removal_classification": "UNKNOWN" if left-right else "NONE",
            "regression": "NOT_PROVED_WITHOUT_LINEAGE_REQUIREMENT_AND_BEHAVIOR_EVIDENCE",
            "scope_expansion": "POSSIBLE" if len(next(x["historical_scope"] for x in origin_scope if x["snapshot_id"] == after["snapshot_id"])) > len(next(x["historical_scope"] for x in origin_scope if x["snapshot_id"] == before["snapshot_id"])) else "NOT_ESTABLISHED",
            "transition_confidence": "SUPPORTED", "motivation": "UNKNOWN", "evidence": uniq(refs),
        })
for version in versions:
    for left_snapshot, right_snapshot in itertools.combinations(version_groups[version], 2):
        left, right = controls_for(left_snapshot["snapshot_id"]), controls_for(right_snapshot["snapshot_id"])
        refs = []
        for sid in [left_snapshot["snapshot_id"], right_snapshot["snapshot_id"]]:
            refs += evidence_for_match(sid, r"canonicalizeUrl|ProviderRegistry|claimNextCandidate|AbortController|maxCandidates|provenance|DecisionLedger", "same-version security control comparison", required=True)
        security_changes.append({
            "change_id": stable_id("security-change", left_snapshot["snapshot_id"], right_snapshot["snapshot_id"]),
            "before_snapshot": left_snapshot["snapshot_id"], "after_snapshot": right_snapshot["snapshot_id"],
            "relationship": "SAME_VERSION_VARIANT_COMPARISON_NOT_LINEAGE",
            "controls_added": sorted(right-left), "controls_absent_after": sorted(left-right), "controls_shared": sorted(left&right),
            "improvement": "MECHANISM_ADDITION_NOT_GENERIC_SECURITY_SCORE" if right-left else "NONE_EVIDENCED",
            "removal_classification": "UNKNOWN" if left-right else "NONE", "regression": "NOT_PROVED_WITHOUT_LINEAGE_REQUIREMENT_AND_BEHAVIOR_EVIDENCE",
            "scope_expansion": "UNKNOWN_WITHOUT_VARIANT_LINEAGE", "transition_confidence": "SUPPORTED", "motivation": "UNKNOWN", "evidence": uniq(refs),
        })

# Failure -> contract and architecture mappings remain non-causal unless prose says otherwise.
failure_contract_map = []
for ftype in FAILURE_TYPES:
    rows = [x for x in failure_events if x["failure_type"] == ftype]
    if not rows: continue
    requirement = {
        "PROVIDER_FAILURE": "provider failure isolation", "NETWORK_FAILURE": "acquisition error semantics", "TIMEOUT": "timeout/cancellation semantics",
        "PERSISTENCE_FAILURE": "persistence integrity and observability", "SCHEDULER_FAILURE": "candidate failure ownership and progress",
        "PARSING_FAILURE": "parser failure representation", "HTTP_FAILURE": "HTTP result-state semantics",
    }.get(ftype, f"{ftype.lower()} handling semantics")
    failure_contract_map.append({
        "failure": ftype, "contract_requirement": requirement,
        "enforcement": sorted({x["detection"] for x in rows}), "test": "UNVERIFIED_NO_HISTORICAL_TEST_EVIDENCE",
        "evidence": uniq(ev for x in rows for ev in x["evidence"])[:12],
    })

security_architecture_map = []
for name, mechanism, boundary in [
    ("provider failures", "ProviderRegistry catch path", "provider boundary"),
    ("resource exhaustion", "configured/enforced limits", "scheduler/acquisition boundary"),
    ("duplicate processing", "key/visited/claimed state", "KnowledgeBase/scheduler boundary"),
    ("untrusted remote data", "acquisition then parser/provider", "acquisition/provider data boundary"),
    ("persistence failure", "local persistence catch", "storage boundary"),
]:
    rows = []
    for snapshot in snapshots:
        sid = snapshot["snapshot_id"]
        mm = first_match(sid, {"provider failures":r"ProviderRegistry", "resource exhaustion":r"maxCandidates|maxRequests|maxBodyChars|maxResponseBytes", "duplicate processing":r"visited|claimed", "untrusted remote data":r"responseText|DOMParser|JSON\.parse", "persistence failure":r"GM_setValue|localStorage"}[name])
        if mm: rows.append((sid, match_ev(sid, mm, f"security/architecture correlation: {name}")))
    security_architecture_map.append({
        "security_concern": name, "mechanism": mechanism, "architectural_boundary": boundary,
        "causality": "CORRELATED", "explicit_motivation": "NOT_EVIDENCED", "chronology_is_not_causality": True,
        "snapshots": [x[0] for x in rows], "evidence": [x[1] for x in rows],
    })

# Security/function tradeoffs, authority migration, privileged APIs, and memory/parser surfaces.
security_tradeoffs = []
tradeoff_meanings = {
    "CANDIDATE_FRONTIER": ("bounded candidate memory/work", "candidate discoveries beyond the cap may be rejected"),
    "SCAN_REQUEST_COUNT": ("bounded acquisition work", "scan completeness is capped"),
    "WORKER_COUNT": ("bounded concurrent workers", "lower parallelism can increase completion time"),
    "REQUEST_DURATION": ("bounded request wait", "slow resources may be classified as failure"),
    "RESPONSE_BODY": ("bounded response retention/parsing", "truncation can hide late content"),
    "EXPANSION_DEPTH": ("bounded recursive expansion", "deeper discoveries can be omitted"),
    "EXPANSION_FANOUT": ("bounded per-discovery fanout", "additional URLs can be omitted"),
    "ORIGIN_REQUEST_COUNT": ("bounded per-origin authority/use", "origin coverage can be capped"),
    "ORIGIN_RATE": ("reduced request pressure", "scan takes longer"),
}
for row in resource_bounds:
    if row["scope"] not in tradeoff_meanings: continue
    control, completeness = tradeoff_meanings[row["scope"]]
    security_tradeoffs.append({
        "tradeoff_id": stable_id("tradeoff", row["bound_id"]), "snapshot_id": row["snapshot_id"], "version": row["version"],
        "control": row["bound"], "security_or_safety_effect": control, "discovery_effect": completeness,
        "measured_effect": "NOT_MEASURED", "superiority_claim": False, "evidence": row["evidence"],
    })
for snapshot in snapshots:
    sid = snapshot["snapshot_id"]
    if "sameOriginOnly" in configs[sid]:
        row = configs[sid]["sameOriginOnly"]
        security_tradeoffs.append({
            "tradeoff_id": stable_id("tradeoff", sid, "sameOriginOnly"), "snapshot_id": sid, "version": snapshot["historical_version"],
            "control": "sameOriginOnly", "security_or_safety_effect": "restricts default cross-origin acquisition scope",
            "discovery_effect": "cross-origin discoveries may not be acquired", "measured_effect": "NOT_MEASURED",
            "superiority_claim": False, "evidence": [row["evidence"]],
        })

authority_migrations = []
for operation in sorted({x["operation"] for x in authority_history}):
    by_snapshot_authority = {(x["snapshot_id"]): x for x in authority_history if x["operation"] == operation}
    for before_v, after_v in zip(versions, versions[1:]):
        for before, after in itertools.product(version_groups[before_v], version_groups[after_v]):
            left = by_snapshot_authority.get(before["snapshot_id"]); right = by_snapshot_authority.get(after["snapshot_id"])
            if not left or not right or left["authority_used"] == right["authority_used"]: continue
            authority_migrations.append({
                "migration_id": stable_id("authority-migration", operation, before["snapshot_id"], after["snapshot_id"]),
                "operation": operation, "before_snapshot": before["snapshot_id"], "after_snapshot": after["snapshot_id"],
                "before_authority": left["authority_used"], "after_authority": right["authority_used"],
                "relationship": "COMPARATIVE_AUTHORITY_CHANGE_NOT_PROVED_LINEAGE", "security_consequence": "UNKNOWN",
                "transition_confidence": "SUPPORTED", "evidence": uniq(left["evidence"] + right["evidence"]),
            })

security_boundary_migrations = [{
    "migration_id": stable_id("security-boundary-migration", x["migration_id"]),
    "operation": x["operation"], "before_snapshot": x["before_snapshot"], "after_snapshot": x["after_snapshot"],
    "before_boundary": x["before_authority"], "after_boundary": x["after_authority"],
    "security_consequence": "UNKNOWN", "classification": "COMPARATIVE_MOVEMENT_NOT_PROVED_LINEAGE",
    "evidence": x["evidence"],
} for x in authority_migrations if x["operation"] in {"network request", "candidate insertion", "candidate claim", "provider registration"}]

privileged_apis = []
api_specs = {
    "GM_xmlhttpRequest": ("GM_xmlhttpRequest", "network request metadata/body", "response/status/headers/body", "callback or rejection"),
    "GM_getValue": ("GM_getValue", "storage key/default", "persisted value", "throw/catch path"),
    "GM_setValue": ("GM_setValue", "storage key/serialized state", "storage side effect", "throw/catch path"),
    "unsafeWindow": ("unsafeWindow", "page-world object access", "page-world state", "UNKNOWN"),
    "fetch": ("fetch", "URL/request options", "Response object/body", "Promise rejection"),
    "localStorage": ("localStorage", "storage key/value", "persisted value", "throw/catch path"),
}
for snapshot in snapshots:
    sid = snapshot["snapshot_id"]; grants = set(metadata_directives(snapshot).get("grant", []))
    for api, (pattern, outbound, inbound, error_crossing) in api_specs.items():
        mm = first_match(sid, rf"\b{pattern}\b")
        if not mm: continue
        owner, operation, _ = owner_at(sid, mm.start())
        privileged_apis.append({
            "api_id": stable_id("privileged-api", sid, api), "snapshot_id": sid, "version": snapshot["historical_version"],
            "api": api, "caller": f"{owner}.{operation}",
            "permission": "EXPLICIT_GRANT" if api in grants else ("BROWSER_AMBIENT" if api in {"fetch", "localStorage"} else "NOT_EXPLICITLY_GRANTED"),
            "data_crossing_out": outbound, "data_crossing_in": inbound, "error_crossing": error_crossing,
            "platform_semantics_verified": False, "evidence": [match_ev(sid, mm, f"privileged/browser API boundary: {api}")],
        })

provider_safety = []
for snapshot in snapshots:
    sid = snapshot["snapshot_id"]
    for parser, owner_pattern in [("HTML", r"Html(?:Provider|Recognizer)"), ("JSON", r"JsonProvider"), ("TEXT", r"TextProvider")]:
        cls = next((x for x in classes[sid] if re.search(owner_pattern, x["name"], re.I)), None)
        if not cls: continue
        body = texts[sid][cls["start"]:cls["end"]]
        provider_safety.append({
            "snapshot_id": sid, "version": snapshot["historical_version"], "provider_kind": parser, "provider": cls["name"],
            "reads_links": bool(re.search(r"a\[href\]|links?", body, re.I)), "reads_scripts": bool(re.search(r"script\[|scripts?", body, re.I)),
            "reads_forms": bool(re.search(r"form\b|forms?", body, re.I)), "reads_resources": bool(re.search(r"img\[|link\[|resources?", body, re.I)),
            "parses": bool(re.search(r"JSON\.parse|DOMParser|parseFromString", body)), "recurses": bool(re.search(r"\b(?:walk|visit|extract)[A-Za-z]*\s*\(", body)),
            "extracts_strings_or_urls": bool(re.search(r"https?|URL|strings?|links?", body, re.I)),
            "injects_html": bool(re.search(r"innerHTML\s*=|insertAdjacentHTML", body)), "evaluates_expressions": bool(re.search(r"\beval\s*\(|new\s+Function", body)),
            "executes_embedded_content": "NOT_EVIDENCED", "security_guarantee": "NOT_ESTABLISHED",
            "evidence": [source_ev(sid, cls["start"], cls["end"], f"{parser} provider safety surface", "HISTORICAL_CLASS")],
        })

memory_safety = []
for snapshot in snapshots:
    sid = snapshot["snapshot_id"]
    fields = {
        "arrays": len(all_matches(sid, r"=\s*\[")), "maps": len(all_matches(sid, r"new\s+Map\s*\(")),
        "sets": len(all_matches(sid, r"new\s+Set\s*\(")), "response_bodies": len(all_matches(sid, r"responseText|\.text\s*\(")),
        "dom_references": len(all_matches(sid, r"document\.|querySelector|DOMParser")), "event_listeners": len(all_matches(sid, r"addEventListener\s*\(")),
        "recursive_calls": len(all_matches(sid, r"\b(?:walk|visit|extract)[A-Za-z]*\s*\(")),
    }
    cleanup = first_match(sid, r"removeEventListener|disconnect\s*\(|\.clear\s*\(|revokeObjectURL")
    basis = first_match(sid, r"new\s+(?:Map|Set)\s*\(|responseText|addEventListener|DOMParser")
    memory_safety.append({
        "snapshot_id": sid, "version": snapshot["historical_version"], "surfaces": fields,
        "cleanup": "PARTIAL_CLEANUP_PATHS" if cleanup else "NOT_EVIDENCED", "garbage_collection_behavior": "PLATFORM_DEPENDENT_UNKNOWN",
        "memory_safety_guarantee": "NOT_ESTABLISHED", "evidence": ([match_ev(sid, basis, "JavaScript memory-retention surface")] if basis else []) + ([match_ev(sid, cleanup, "cleanup path")] if cleanup else []),
    })

# Current/proposed security concepts are isolated from historical snapshots.
current_doc = ROOT / "Continue Architecture Planning.md"
current_text = current_doc.read_bytes().decode("utf-8")
current_security = []
for name, pattern in [
    ("capability-oriented extension boundaries", r"capabilit(?:y|ies)[\s\S]{0,160}(?:provider|module|adapter)"),
    ("WASM extension/execution proposal", r"(?:WASM module|WASM/plugin ecosystem|WASM execution units)"),
    ("explicit policy architecture", r"Cross-cutting:[\s\S]{0,120}\bPolicy\b"),
    ("run isolation", r"Run isolation[\s*]+so stale asynchronous workers cannot mutate a later run"),
]:
    mm = re.search(pattern, current_text, re.I)
    if mm:
        current_security.append({"concept": name, "status": "CURRENT_OR_PROPOSED_NOT_BACKFILLED", "evidence": [root_ev(current_doc, mm, f"current/proposed security concept: {name}")]})

# Final classifications distinguish static path evidence from runtime occurrence evidence.
observed_failures = sorted({x["failure_type"] for x in failure_events})
handled_failures = sorted({x["failure_type"] for x in failure_events if x["status"] == "IMPLEMENTED_HANDLING_PATH"})
contained_failures = sorted({x["failure_type"] for x in failure_events if x["containment_level"] in {"F4", "F5", "F6"}})
explicit_recovery_paths = {"CONTINUE_NEXT_ITERATION", "CONTINUE_PROVIDER_LOOP_OR_METHOD_FALLBACK", "RETRY_OR_REQUEUE_PATH", "FALLBACK_VALUE", "RECORD_AND_RETURN_OR_CONTINUE", "LOCAL_FAILURE_PATH", "LOCAL_CLASSIFICATION"}
recoverable_failures = sorted({x["failure_type"] for x in failure_events if x["recovery"] in explicit_recovery_paths})
silent_summary = []
for (operation, classification), group in itertools.groupby(sorted(silent_failures, key=lambda x: (x["operation"], x["classification"], x["snapshot_id"])), key=lambda x: (x["operation"], x["classification"])):
    rows = list(group)
    silent_summary.append({"operation": operation, "classification": classification, "occurrences": [x["snapshot_id"] for x in rows], "evidence": uniq(ev for x in rows for ev in x["evidence"])})
final_failure_classification = {
    "OBSERVED_FAILURES": {"items": observed_failures, "meaning": "Static failure detection/representation paths observed; runtime occurrence is not proved."},
    "HANDLED_FAILURES": handled_failures,
    "CONTAINED_FAILURES": contained_failures,
    "RECOVERABLE_FAILURES": recoverable_failures,
    "SILENT_FAILURES": silent_summary,
    "POTENTIAL_FAILURE_MODES": sorted({x["condition"] for x in data_integrity if x["classification"] == "POSSIBLE"} | {x["risk"] for x in resource_risks if x["classification"] == "UNMITIGATED"}),
    "UNVERIFIED_FAILURE_MODES": FAILURE_TYPES,
}

verified_mechanisms = [
    {"mechanism": "URL parsing/canonicalization and admission checks", "scope": "path-local", "evidence": uniq(ev for x in url_trust for ev in x["evidence"])[:8]},
    {"mechanism": "request error and timeout callbacks", "scope": "selected acquisition paths", "evidence": uniq(ev for x in failure_events if x["failure_type"] in {"NETWORK_FAILURE", "TIMEOUT"} for ev in x["evidence"])[:8]},
    {"mechanism": "provider/worker/persistence catch paths", "scope": "individual recovered handlers", "evidence": uniq(ev for x in failure_events if x["detection"] == "CATCH" for ev in x["evidence"])[:8]},
    {"mechanism": "candidate key, visited, and claimed structures", "scope": "event-loop-local recovered paths", "evidence": uniq(ev for x in duplicate_processing for ev in x["evidence"])[:8]},
    {"mechanism": "configured and referenced resource bounds", "scope": "recorded enforcement points", "evidence": uniq(ev for x in resource_bounds if x["enforcement"] == "PROVED_REFERENCE" for ev in x["evidence"])[:8]},
]
verified_properties = [
    {"property": "selected claim mutations execute synchronously before the first await", "scope": "claim method path only", "evidence": uniq(ev for x in claim_safety if x["claim_atomicity"] == "SYNCHRONOUS_EVENT_LOOP_LOCAL_SEQUENCE" for ev in x["evidence"])[:8]},
    {"property": "selected provider exceptions are caught at registry/provider paths", "scope": "handlers with F5 classification only", "evidence": uniq(ev for x in failure_events if x["containment_level"] == "F5" for ev in x["evidence"])[:8]},
]
goal_summary = []
for snapshot in snapshots:
    sid = snapshot["snapshot_id"]
    vague_goal = re.search(r"Safer DOM/UI handling", texts[sid], re.I)
    if vague_goal:
        goal_summary.append({
            "goal": "Safer DOM/UI handling", "occurrences": [sid], "enforcement": "UNDERSPECIFIED_GOAL_NO_COMPLETE_PROPERTY",
            "evidence": [match_ev(sid, vague_goal, "documented but underspecified security/safety goal")],
        })
final_security_classification = {
    "HISTORICALLY_VERIFIED_SECURITY_MECHANISMS": verified_mechanisms,
    "HISTORICALLY_VERIFIED_SECURITY_PROPERTIES": verified_properties,
    "SECURITY_GOALS_WITHOUT_ENFORCEMENT": goal_summary,
    "RETROSPECTIVE_SECURITY_INTERPRETATIONS": [
        {"interpretation": "Remote parsing and retained state form a resource-exhaustion surface; no exploit or incident is claimed.", "evidence": uniq(ev for x in resource_risks for ev in x["evidence"])[:8]},
        {"interpretation": "Ambient GM/browser authority is broader than narrow capability-like object passing; least authority is not established.", "evidence": uniq(ev for x in authority_history if x["operation"] == "network request" for ev in x["evidence"])[:8]},
    ],
    "CURRENT_PROPOSED_SECURITY_ARCHITECTURE": current_security,
    "UNKNOWN": ["whole-system provider isolation", "global uniqueness", "cross-thread/distributed safety", "redirect trust", "persistence crash atomicity", "absence of all code-execution paths"],
}

# Final 23 answers, each evidence-backed and conservative.
def refs_where(rows: list[dict[str, Any]], predicate=lambda x: True, limit: int = 10) -> list[str]:
    return uniq(ev for x in rows if predicate(x) for ev in x.get("evidence", []))[:limit]

earliest = snapshots[0]["snapshot_id"]
first_retry = next((x for x in retry_history if x["retry"] == "IMPLEMENTED"), None)
first_abort = next((x for x in cancellation_history if x["mechanism"] == "ABORTCONTROLLER"), None)
first_structured = next((x for x in observability if "STRUCTURED_LOG" in x["channels"]), None)
first_provider_contain = next((x for x in failure_events if x["containment_level"] == "F5"), None)
answers = [
    (1, "What could fail in the earliest implementation?", "The earliest recovered v0.1 has URL-validation, request/network, timeout, recognition, persistence, export/UI, mutable-state, and worker/scheduler progress failure surfaces. Only some have explicit handlers. These are static paths and potential modes, not observed production incidents.", refs_where(failure_events, lambda x: x["snapshot_id"] == earliest) + refs_where(claim_safety, lambda x: x["snapshot_id"] == earliest)),
    (2, "Where did failures terminate?", "Termination varies by path: some acquisition errors become failed Observations/caller results; persistence handlers stop locally; later worker handlers can stop at a candidate or worker path. Unknown propagation is retained where control flow does not prove a stopping boundary.", refs_where(failure_events, lambda x: x["containment_level"] in {"F4", "F5", "F6"})),
    (3, "Which failures were silently discarded?", "Empty or fallback-return catch paths are listed as intentional silence, unexplained silence, or error suppression. Logging-only suppression remains observable but does not propagate structured failure.", refs_where(silent_failures)),
    (4, "When did failures become structured?", f"Observation error/status fields exist from v0.1; richer structured diagnostics first appear in {first_structured['version'] if first_structured else 'no recovered version'}. Structure does not imply complete preservation or verification.", refs_where(observability)),
    (5, "When did retry semantics appear?", f"A demonstrable count-plus-requeue retry path first appears in {first_retry['version'] if first_retry else 'no recovered version'}. Configuration-only retry names are not counted as implemented retry.", first_retry["evidence"] if first_retry else refs_where(retry_history)),
    (6, "When did cancellation appear?", f"AbortController/abort first appears in {first_abort['version'] if first_abort else 'no recovered version'} on recovered paths. Earlier/lateral stop flags do not prove underlying request cancellation.", first_abort["evidence"] if first_abort else refs_where(cancellation_history)),
    (7, "When did resource bounds appear?", "Candidate count, request count, worker concurrency, and request timeout bounds are present from v0.1. Later variants add depth, retries, body-size, per-origin, graph, diagnostic, and persistence-retention bounds.", refs_where(resource_bounds, lambda x: x["snapshot_id"] == earliest)),
    (8, "When did concurrency safety become explicit?", "v0.2 is the earliest recovered named claimNextCandidate path. Its short synchronous mutation sequence supports event-loop-local claim ownership before await, not thread safety or atomic processing across await.", refs_where(claim_safety, lambda x: x["version"] == "v0.2.0")),
    (9, "When did provenance integrity become explicit?", "Provenance representation through Candidate, Observation, and Discovery identifiers/fields is already explicit in v0.1. End-to-end provenance integrity, immutability, and non-loss are never guaranteed.", refs_where(provenance_integrity, lambda x: x["snapshot_id"] == earliest)),
    (10, "What were the earliest trust boundaries?", "v0.1 already crosses page DOM, admitted URLs, privileged/browser network APIs, remote content parsers/providers, storage, UI, and export boundaries. Scheduler structure is an authority boundary but is not automatically a trust boundary.", refs_where(trust_boundaries, lambda x: x["snapshot_id"] == earliest)),
    (11, "When did network access become a distinct authority?", "It is already distinct in v0.1: browser fetch and GM_xmlhttpRequest perform acquisition, while metadata grants GM_xmlhttpRequest and @connect *. Granted authority is distinguished from default same-origin policy and actual use.", refs_where(origin_scope, lambda x: x["snapshot_id"] == earliest)),
    (12, "When did provider code become isolated?", f"The first recovered provider-local stopping boundary appears in {first_provider_contain['version'] if first_provider_contain else 'no version'}. This proves selected catch paths only, not a provider isolation guarantee.", first_provider_contain["evidence"] if first_provider_contain else refs_where(failure_events, lambda x: x["failure_type"] == "PROVIDER_FAILURE")),
    (13, "When did remote data become explicitly treated as untrusted?", "Parsing, allow checks, and provider recognition show implicit distrust from v0.1. An explicit complete threat statement that all remote content is untrusted was not recovered; retrospective interpretation remains separate.", refs_where(threat_models, lambda x: x["snapshot_id"] == earliest)),
    (14, "What code/data boundaries existed?", "Acquired HTML/JSON/text is parsed and extracted as data. No eval/new Function/dynamic-import path from acquired content was found. Later static page-bridge script insertion and UI innerHTML are separate sinks and do not prove remote content execution.", refs_where(code_data_history)),
    (15, "What userscript privileges existed historically?", "Recovered headers grant GM_getValue, GM_setValue, and GM_xmlhttpRequest throughout; selected branch variants also grant unsafeWindow. @connect * is present. v0.1/v0.2 recovered @match text is preserved literally and flagged as potentially Markdown-affected.", refs_where(permission_history)),
    (16, "How did acquisition scope evolve?", "Current-page DOM plus active acquisition of admitted discovered resources already coexist in v0.1; a current-page-only predecessor is not recovered. Later versions elaborate policy and per-origin controls without proving protocol independence.", refs_where(origin_scope)),
    (17, "How did authority migrate between components?", "Network, candidate admission/claim, provider registration, state mutation, export, and configuration authority move among adapters, KnowledgeBase/scheduler, ProviderRegistry, engine, and UI across variants. Cross-version parentage is unknown, so this is comparative migration, not proved lineage.", refs_where(authority_history)),
    (18, "Which security controls affected discovery completeness?", "Same-origin checks, maximum candidate/request/depth/fanout/body limits, rate controls, and provider admission can bound work while excluding discoveries or truncating evidence. The tradeoff is structural; completeness loss was not measured.", refs_where(resource_bounds)),
    (19, "Which security properties were documented but unenforced?", "The clearest recovered example is v0.3's broad ‘Safer DOM/UI handling’ statement, which does not specify a complete enforceable property. Atomic-claim and bounded-work comments have local mechanisms but remain unverified as whole-system guarantees. Complete provider isolation, provenance non-loss, and untrusted-input non-execution are retrospective analytical assumptions unless separately documented.", refs_where(goal_summary) + refs_where(claim_safety, lambda x: x["version"] == "v0.3.0")),
    (20, "Which security properties were implemented but undocumented?", "Candidate key/visited/claimed checks, local catch boundaries, body/frontier bounds, and URL admission are mechanically present even where no security label is attached. They remain mechanisms or path properties, not generic guarantees.", refs_where(verified_mechanisms)),
    (21, "Which security mechanisms were later removed?", "Adjacent-version comparisons contain controls absent in later variants, but no removal is classified as a proved regression because lineage, requirement continuity, and behavioral consequence are unproved.", refs_where(security_changes, lambda x: bool(x["controls_absent_after"]))),
    (22, "Which security concepts appeared only in later architecture?", "Capability-oriented boundaries, WASM extension/execution, explicit policy architecture, and run isolation appear in later/current prose where located; they are not imported into earlier snapshots.", refs_where(current_security)),
    (23, "What is the earliest historically defensible security model?", "v0.1 is already a bounded, same-origin-by-default web discovery userscript with privileged network/storage authority, URL admission, remote-data parsing, local error handling, persistence, provenance fields, and a worker pool. It is a partial path-based safety model—not a verified secure system. v0.2 adds the earliest explicit local claim protocol and reusable provider boundary.", refs_where(trust_boundaries, lambda x: x["snapshot_id"] == earliest) + refs_where(claim_safety, lambda x: x["version"] == "v0.2.0")),
]

# Guarantee every answer has directional evidence without inventing positive claims.
for i, row in enumerate(answers):
    if not row[3]:
        answers[i] = (row[0], row[1], row[2], [source_ev(earliest, 0, min(1, len(texts[earliest])), "bounded historical snapshot scope")])

# --- Serialization and Markdown ---------------------------------------------
def envelope(key: str, value: Any, kind: str = "DERIVED_SECURITY_ARCHAEOLOGY_NOT_SOURCE") -> dict[str, Any]:
    return {"schema_version": SCHEMA, "builder": BUILDER, "model_kind": kind, key: value}

machine_outputs: dict[str, Any] = {
    "EVIDENCE.yaml": envelope("evidence", sorted(evidence.values(), key=lambda x: x["evidence_id"]), "SECURITY_EVIDENCE_INDEX"),
    "FAILURE-EVENTS.yaml": {**envelope("failures", failure_events), "failure_taxonomy": FAILURE_TYPES, "stage_registry": STAGES, "containment_levels": FAILURE_LEVELS},
    "FAILURE-MATRIX.yaml": {**envelope("matrix", failure_matrix), "evidence_labels": sorted(EVIDENCE_LABELS)},
    "FAILURE-STAGE-MODEL.yaml": envelope("stages", failure_stage_model),
    "FAILURE-PROPAGATION.yaml": envelope("edges", propagation_edges),
    "FAILURE-INFORMATION.yaml": envelope("handlers", failure_information),
    "SILENT-FAILURES.yaml": {**envelope("failures", silent_failures), "classification_registry": sorted(SILENCE_CLASSES)},
    "RETRY-HISTORY.yaml": envelope("snapshots", retry_history),
    "TIMEOUT-HISTORY.yaml": envelope("snapshots", timeout_history),
    "CANCELLATION-HISTORY.yaml": envelope("snapshots", cancellation_history),
    "RESOURCE-BOUNDS.yaml": envelope("bounds", resource_bounds),
    "RESOURCE-EXHAUSTION.yaml": {**envelope("risks", resource_risks), "classification_registry": sorted(RISK_CLASSES)},
    "CONCURRENCY-STATE.yaml": envelope("structures", concurrency_state),
    "CLAIM-SAFETY.yaml": envelope("snapshots", claim_safety),
    "DUPLICATE-PROCESSING.yaml": envelope("snapshots", duplicate_processing),
    "RACE-ANALYSIS.yaml": envelope("races", race_analysis),
    "DATA-INTEGRITY.yaml": {**envelope("conditions", data_integrity), "classification_registry": sorted(INTEGRITY_CLASSES), "weaknesses": integrity_weaknesses},
    "PROVENANCE-INTEGRITY.yaml": envelope("snapshots", provenance_integrity),
    "TRUST-BOUNDARIES.yaml": envelope("boundaries", trust_boundaries),
    "AUTHORITY-HISTORY.yaml": envelope("authorities", authority_history),
    "USERSCRIPT-PERMISSION-HISTORY.yaml": envelope("snapshots", permission_history),
    "ORIGIN-SCOPE-HISTORY.yaml": envelope("snapshots", origin_scope),
    "URL-TRUST-HISTORY.yaml": envelope("snapshots", url_trust),
    "CODE-DATA-BOUNDARY-HISTORY.yaml": envelope("snapshots", code_data_history),
    "PARSER-SAFETY-HISTORY.yaml": {**envelope("parsers", parser_history), "regex_risks": regex_risks},
    "PERSISTENCE-INTEGRITY.yaml": envelope("snapshots", persistence_integrity),
    "EXPORT-INTEGRITY.yaml": envelope("snapshots", export_integrity),
    "OBSERVABILITY-HISTORY.yaml": envelope("snapshots", observability),
    "AUDITABILITY-HISTORY.yaml": envelope("snapshots", auditability),
    "SECURITY-INVARIANT-HISTORY.yaml": {**envelope("invariants", security_invariants), "claim_types": sorted(SECURITY_CLAIM_TYPES)},
    "THREAT-MODEL-HISTORY.yaml": {**envelope("snapshots", threat_models), "classification_registry": sorted(THREAT_CLASSES)},
    "SECURITY-CHANGES.yaml": {**envelope("comparisons", security_changes), "change_registry": sorted(CHANGE_CLASSES)},
    "TRUST-BOUNDARY-MATRIX.yaml": envelope("matrix", trust_matrix),
    "FAILURE-CONTRACT-MAP.yaml": envelope("mappings", failure_contract_map),
    "SECURITY-ARCHITECTURE-MAP.yaml": envelope("mappings", security_architecture_map),
    "SECURITY-FUNCTION-TRADEOFFS.yaml": envelope("tradeoffs", security_tradeoffs),
    "AUTHORITY-MIGRATION.yaml": envelope("migrations", authority_migrations),
    "SECURITY-BOUNDARY-MIGRATION.yaml": envelope("migrations", security_boundary_migrations),
    "PRIVILEGED-API-HISTORY.yaml": envelope("apis", privileged_apis),
    "PROVIDER-SAFETY.yaml": envelope("providers", provider_safety),
    "MEMORY-SAFETY.yaml": envelope("snapshots", memory_safety),
    "CURRENT-PROPOSED-SECURITY.yaml": envelope("concepts", current_security),
    "FINAL-QUESTIONS.yaml": envelope("questions", [{"number": n, "question": q, "answer": a, "evidence": uniq(e)} for n, q, a, e in answers]),
    "FINAL-FAILURE-CLASSIFICATION.yaml": envelope("classification", final_failure_classification),
    "FINAL-SECURITY-CLASSIFICATION.yaml": envelope("classification", final_security_classification),
}

OUT.mkdir(parents=True, exist_ok=True)
for name, value in machine_outputs.items(): dump(OUT / name, value)

def esc(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def table(headers: list[str], rows: list[list[Any]]) -> str:
    return "\n".join(["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"] + ["| " + " | ".join(esc(x) for x in row) + " |" for row in rows])

failure_prop_md = ["# Failure Propagation Evolution", "", "`DERIVED SECURITY MODEL — NOT HISTORICAL SOURCE`", "", "Every graph edge is event-scoped. A catch path is not promoted to a fault-isolation guarantee.", "", "```text", "Failure Source → Detection → Local Handling or Propagation → Scheduler/Caller → Scan Result", "```", "", "## Containment levels", ""]
for level, meaning in FAILURE_LEVELS.items(): failure_prop_md.append(f"- **{level}** — {meaning}")
failure_prop_md += ["", "## Per-version summary", "", table(["Snapshot", "Events", "Local F4–F6", "Propagating", "Unknown stop"], [[s["snapshot_id"], sum(x["snapshot_id"]==s["snapshot_id"] for x in failure_events), sum(x["snapshot_id"]==s["snapshot_id"] and x["containment_level"] in {"F4","F5","F6"} for x in failure_events), sum(x["snapshot_id"]==s["snapshot_id"] and "PROPAGAT" in x["propagation"] or x["snapshot_id"]==s["snapshot_id"] and x["propagation"] in {"RETHROW","PROMISE_REJECTION"} for x in failure_events), sum(x["snapshot_id"]==s["snapshot_id"] and x["containment_level"]=="UNKNOWN" for x in failure_events)] for s in snapshots])]
(OUT / "FAILURE-PROPAGATION.md").write_text("\n".join(failure_prop_md)+"\n", encoding="utf-8", newline="\n")

md_specs = [
    ("RETRY-HISTORY.md", "Retry Archaeology", retry_history, ["Snapshot","Retry","Trigger","Count","Backoff","Same candidate","Terminal"], lambda x:[x["snapshot_id"],x["retry"],x["trigger"],x["count"],x["backoff"],x["same_candidate"],x["terminal_failure"]], "Recursion is never counted as retry without a demonstrable same-operation path."),
    ("TIMEOUT-HISTORY.md", "Timeout Archaeology", timeout_history, ["Snapshot","Scope","Value","Detection","Cancellation","Cleanup","Retry"], lambda x:[x["snapshot_id"],x["timeout_scope"],x["configured_value"],x["detection"],x["cancellation"],x["cleanup"],x["retry"]], "A configured request timeout does not establish candidate, worker, scan, or global timeout."),
    ("CANCELLATION-HISTORY.md", "Cancellation Archaeology", cancellation_history, ["Snapshot","Mechanism","UI","Scheduler","Worker","Acquisition","Underlying operation"], lambda x:[x["snapshot_id"],x["mechanism"],x["ui"],x["scheduler"],x["worker"],x["acquisition"],x["underlying_operation_cancelled"]], "A Stop control or running flag is not proof that in-flight acquisition/provider work is cancelled."),
    ("RESOURCE-BOUND-HISTORY.md", "Resource-Bound Evolution", resource_bounds, ["Snapshot","Bound","Value","Scope","Enforcement","Point","Failure behavior"], lambda x:[x["snapshot_id"],x["bound"],x["value"],x["scope"],x["enforcement"],x["enforcement_point"],x["failure_behavior"]], "Configuration is recorded separately from its enforcement point."),
    ("RESOURCE-EXHAUSTION-HISTORY.md", "Resource Exhaustion History", resource_risks, ["Snapshot","Risk","Classification","Mitigation","Limit"], lambda x:[x["snapshot_id"],x["risk"],x["classification"],x["mitigation"],x["mitigation_limit"]], "OBSERVED_RISK means a static growth/input surface was observed, not an exploit or incident."),
    ("CONCURRENCY-SAFETY-HISTORY.md", "Concurrency Safety History", claim_safety, ["Snapshot","Claim","Atomicity","Ownership","Processing","Completion","Failure","Requeue"], lambda x:[x["snapshot_id"],x["claim_operation"],x["claim_atomicity"],x["claim_ownership"],x["processing_exclusivity"],x["completion_ownership"],x["failure_ownership"],x["requeue"]], "Synchronous JavaScript claim mutation is event-loop-local. Await boundaries, callbacks, threads, processes, and distributed workers are not covered."),
    ("DATA-INTEGRITY-HISTORY.md", "Data Integrity History", data_integrity, ["Snapshot","Condition","Classification","Scope","Caveat"], lambda x:[x["snapshot_id"],x["condition"],x["classification"],x["scope"],x["caveat"]], "POSSIBLE is not OBSERVED; PREVENTED is path-local unless stated otherwise. Persistence integrity is included in PERSISTENCE-INTEGRITY.yaml."),
    ("PROVENANCE-INTEGRITY-HISTORY.md", "Provenance Integrity History", provenance_integrity, ["Snapshot","Discovery→Observation","Observation→Candidate","Candidate→Parent","Parent→Seed","End-to-end"], lambda x:[x["snapshot_id"]]+[e["status"] for e in x["edges"]]+[x["end_to_end_traceability"]], "A provenance field is not a provenance-integrity guarantee."),
    ("AUTHORITY-HISTORY.md", "Authority History", authority_history, ["Snapshot","Operation","Required","Granted","Used","Extra exposure","Capability-like"], lambda x:[x["snapshot_id"],x["operation"],x["authority_required"],x["authority_granted"],x["authority_used"],x["unnecessarily_exposed"],x["capability_like_pattern"]], "Narrow object passing may be capability-like; no formal capability system is inferred."),
    ("USERSCRIPT-PERMISSION-HISTORY.md", "Userscript Permission History", permission_history, ["Snapshot","@match","@include","@grant","@connect","@require","@resource"], lambda x:[x["snapshot_id"],", ".join(x["match"]),", ".join(x["include"]),", ".join(x["grant"]),", ".join(x["connect"]),", ".join(x["require"]),", ".join(x["resource"])], "Directives are preserved literally. Markdown-affected early @match values are not silently repaired."),
    ("ORIGIN-SCOPE-HISTORY.md", "Origin and Acquisition Scope History", origin_scope, ["Snapshot","Historical scope","Default policy","Metadata authority","Redirect","Current→arbitrary"], lambda x:[x["snapshot_id"],", ".join(x["historical_scope"]),x["default_policy"],x["metadata_authority"],x["redirect_detection"],x["current_page_to_arbitrary_evolution"]], "Granted authority, configured policy, and actual use are distinct."),
    ("URL-TRUST-HISTORY.md", "URL Trust History", url_trust, ["Snapshot","Canonicalization","Admission","Scheme","Origin","Redirect","Local addresses","Credentials"], lambda x:[x["snapshot_id"],x["discovered_to_candidate"],x["candidate_to_acquisition"],x["scheme"],x["origin"],x["redirect"],x["local_addresses"],x["credentials"]], "URL parsing is not a URL security policy. Redirect behavior remains UNKNOWN without code evidence."),
    ("CODE-DATA-BOUNDARY-HISTORY.md", "Code/Data Boundary History", code_data_history, ["Snapshot","Sinks","Acquired content→code","innerHTML","Script insertion"], lambda x:[x["snapshot_id"],", ".join(x["sinks"]) or "none",x["acquired_content_to_code_path"],x["inner_html"],x["script_insertion"]], "NO_EVIDENCE_OF_CODE_EXECUTION is a bounded negative finding, not a claim that the system is secure."),
    ("PARSER-SAFETY-HISTORY.md", "Parser Safety History", parser_history, ["Snapshot","Parser","Owner","Input size","Recursion","Error handling","Script execution"], lambda x:[x["snapshot_id"],x["parser"],x["owner"],x["input_size"],x["recursion"],x["error_handling"],x["script_execution"]], "HTML extraction, JSON parsing, and text regex processing are data operations unless an execution sink is evidenced. Regex candidates are in PARSER-SAFETY-HISTORY.yaml."),
    ("OBSERVABILITY-HISTORY.md", "Observability History", observability, ["Snapshot","Channels","Progression stages"], lambda x:[x["snapshot_id"],", ".join(x["channels"])," → ".join(x["progression_stages_evidenced"])], "Detection and observability are independent."),
    ("AUDITABILITY-HISTORY.md", "Auditability History", auditability, ["Snapshot","Classification","What","When","Candidate","Why","Provider","Observation","Discovery","Failure","Replay"], lambda x:[x["snapshot_id"],x["classification"]]+["yes" if x["questions"][k] else "no" for k in ["what","when","candidate","why","provider","observation","discovery","failure"]]+[x["replay"]], "Static fields/channels support audit questions; no historical execution replay was verified."),
]
for filename, title, rows, headers, mapper, note in md_specs:
    content = [f"# {title}", "", "`DERIVED SECURITY MODEL — NOT HISTORICAL SOURCE`", "", note, "", table(headers, [mapper(x) for x in rows]), ""]
    (OUT / filename).write_text("\n".join(content), encoding="utf-8", newline="\n")

# Extend authority history with branch-preserving comparative migrations.
authority_path = OUT / "AUTHORITY-HISTORY.md"
authority_path.write_text(authority_path.read_text(encoding="utf-8") + "\n## Comparative authority migrations\n\n" + table(["Operation","Before","After","Authority before","Authority after","Consequence"], [[x["operation"],x["before_snapshot"],x["after_snapshot"],x["before_authority"],x["after_authority"],x["security_consequence"]] for x in authority_migrations]) + "\n", encoding="utf-8", newline="\n")
tradeoff_md = ["# Security / Function Tradeoffs", "", "Controls can bound authority or work while reducing discovery completeness. No effect was measured and no generic superiority score is assigned.", "", table(["Snapshot","Control","Safety effect","Discovery effect","Measured"], [[x["snapshot_id"],x["control"],x["security_or_safety_effect"],x["discovery_effect"],x["measured_effect"]] for x in security_tradeoffs])]
(OUT / "SECURITY-FUNCTION-TRADEOFFS.md").write_text("\n".join(tradeoff_md)+"\n", encoding="utf-8", newline="\n")
priv_md = ["# Privileged API Boundary History", "", "Permissions, callers, outbound data, inbound data, and error crossings are separate. Platform semantics were not historically executed.", "", table(["Snapshot","API","Caller","Permission","Outbound","Inbound","Errors"], [[x["snapshot_id"],x["api"],x["caller"],x["permission"],x["data_crossing_out"],x["data_crossing_in"],x["error_crossing"]] for x in privileged_apis])]
(OUT / "PRIVILEGED-API-HISTORY.md").write_text("\n".join(priv_md)+"\n", encoding="utf-8", newline="\n")

inv_md = ["# Security Invariant History", "", "`DERIVED SECURITY MODEL — NOT HISTORICAL SOURCE`", "", "SECURITY_PROPERTY, SECURITY_MECHANISM, SECURITY_ASSUMPTION, SECURITY_GOAL, and SECURITY_GUARANTEE remain distinct.", "", table(["Snapshot","Invariant","Status","Claim type","Historical test"], [[x["snapshot_id"],x["invariant"],x["status"],x["claim_type"],x["historical_test"]] for x in security_invariants])]
(OUT / "SECURITY-INVARIANT-HISTORY.md").write_text("\n".join(inv_md)+"\n", encoding="utf-8", newline="\n")
threat_md = ["# Threat Model History", "", "`DERIVED SECURITY MODEL — NOT HISTORICAL SOURCE`", "", "Implicit mechanisms and retrospective concerns are not rewritten as explicit historical threats.", ""]
for row in threat_models:
    threat_md += [f"## {row['version']} / `{row['snapshot_id']}`", ""] + [f"- **{x['classification']}** — {x['threat']}" for x in row["threats"]] + ["- Complete threat model: NOT_EVIDENCED", ""]
(OUT / "THREAT-MODEL-HISTORY.md").write_text("\n".join(threat_md), encoding="utf-8", newline="\n")

reg_md = ["# Security Regressions", "", "No generic security score is used. Absence-after is not a regression without lineage, a continuing requirement, and behavioral consequence.", "", table(["Before","After","Controls absent after","Classification","Regression"], [[x["before_snapshot"],x["after_snapshot"],", ".join(x["controls_absent_after"]) or "none",x["removal_classification"],x["regression"]] for x in security_changes if x["controls_absent_after"]])]
(OUT / "SECURITY-REGRESSIONS.md").write_text("\n".join(reg_md)+"\n", encoding="utf-8", newline="\n")
imp_md = ["# Security Improvements", "", "Control additions are recorded as mechanism changes, not proof that a whole version is ‘more secure’.", "", table(["Before","After","Controls added","Finding","Motivation"], [[x["before_snapshot"],x["after_snapshot"],", ".join(x["controls_added"]) or "none",x["improvement"],x["motivation"]] for x in security_changes if x["controls_added"]])]
(OUT / "SECURITY-IMPROVEMENTS.md").write_text("\n".join(imp_md)+"\n", encoding="utf-8", newline="\n")

fc_md = ["# Failure → Contract Map", "", "A failure path maps to a contract requirement and local enforcement; every test column remains UNVERIFIED where no historical test evidence exists.", "", table(["Failure","Contract requirement","Enforcement","Test"], [[x["failure"],x["contract_requirement"],", ".join(x["enforcement"]),x["test"]] for x in failure_contract_map])]
(OUT / "FAILURE-CONTRACT-MAP.md").write_text("\n".join(fc_md)+"\n", encoding="utf-8", newline="\n")
sa_md = ["# Security → Architecture Map", "", "Chronological correlation is not causality. No boundary is claimed to have been caused by a concern unless explicit motivation evidence exists.", "", table(["Concern","Mechanism","Boundary","Causality","Explicit motivation"], [[x["security_concern"],x["mechanism"],x["architectural_boundary"],x["causality"],x["explicit_motivation"]] for x in security_architecture_map]), "", "## Comparative security-boundary migration", "", "Movement is comparative; parentage and security consequence remain UNKNOWN.", "", table(["Operation","Before","After","Boundary before","Boundary after","Classification"], [[x["operation"],x["before_snapshot"],x["after_snapshot"],x["before_boundary"],x["after_boundary"],x["classification"]] for x in security_boundary_migrations])]
(OUT / "SECURITY-ARCHITECTURE-MAP.md").write_text("\n".join(sa_md)+"\n", encoding="utf-8", newline="\n")

graph_md = ["# Security Evolution Graph", "", "Only source-supported nodes are connected. The graph is comparative and does not establish design causality or superiority.", "", "```text", "v0.1 URL admission + bounded work + local failure handling", "  ├── v0.1 privileged network/storage and remote-data parser boundaries", "  └── v0.2 named provider registry + synchronous local candidate claim", "        ├── later branch variants: retries/backoff + AbortController", "        ├── later branch variants: provider catch paths + richer provenance", "        ├── later branch variants: body/per-origin/retention bounds", "        └── v0.7.1 structured decision ledger and explicit acquisition policy/plan forms", "```", "", "No functions-only, current-page-only, or implicit-trust-only predecessor is recovered. Whole-system explicit trust policy remains incomplete."]
(OUT / "SECURITY-EVOLUTION-GRAPH.md").write_text("\n".join(graph_md)+"\n", encoding="utf-8", newline="\n")

# Per-version state reports preserve same-version variants.
for version in versions:
    group = version_groups[version]
    lines = [f"# Historical Security State — {version}", "", "`DERIVED SECURITY MODEL — NOT HISTORICAL SOURCE`", ""]
    for snapshot in group:
        sid = snapshot["snapshot_id"]
        lines += [f"## `{sid}` — {snapshot['variant']}", "",
                  f"- Trust boundaries: {sum(x['snapshot_id']==sid and x['boundary_status']!='NOT_PRESENT_OR_NOT_EVIDENCED' for x in trust_boundaries)} observed data/authority/trust boundaries.",
                  f"- Authority: {', '.join(sorted({x['operation'] for x in authority_history if x['snapshot_id']==sid})) or 'UNKNOWN'}.",
                  f"- Failure containment: {sum(x['snapshot_id']==sid and x['containment_level'] in {'F4','F5','F6'} for x in failure_events)} local candidate/provider/operation paths; mechanism ≠ guarantee.",
                  f"- Resource bounds: {', '.join(sorted({x['bound'] for x in resource_bounds if x['snapshot_id']==sid})) or 'none evidenced'}.",
                  f"- Input validation: {next(x['candidate_to_acquisition'] for x in url_trust if x['snapshot_id']==sid)}.",
                  f"- Provenance integrity: {next(x['end_to_end_traceability'] for x in provenance_integrity if x['snapshot_id']==sid)}; guarantee NOT_ESTABLISHED.",
                  f"- Concurrency safety: {next(x['claim_atomicity'] for x in claim_safety if x['snapshot_id']==sid)}; no thread/distributed claim.",
                  f"- Code/data boundary: {next(x['acquired_content_to_code_path'] for x in code_data_history if x['snapshot_id']==sid)}.",
                  f"- Observability: {', '.join(next(x['channels'] for x in observability if x['snapshot_id']==sid)) or 'none'}.",
                  f"- Known gaps: redirect trust, complete cancellation, parser/resource safety, crash atomicity, end-to-end provenance, and historical execution verification remain UNKNOWN unless a row says otherwise.", ""]
    (OUT / f"{version}.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")

failure_headings = ["OBSERVED FAILURES", "HANDLED FAILURES", "CONTAINED FAILURES", "RECOVERABLE FAILURES", "SILENT FAILURES", "POTENTIAL FAILURE MODES", "UNVERIFIED FAILURE MODES"]
security_headings = ["HISTORICALLY VERIFIED SECURITY MECHANISMS", "HISTORICALLY VERIFIED SECURITY PROPERTIES", "SECURITY GOALS WITHOUT ENFORCEMENT", "RETROSPECTIVE SECURITY INTERPRETATIONS", "CURRENT/PROPOSED SECURITY ARCHITECTURE", "UNKNOWN"]

def render_failure_classification() -> list[str]:
    out = []
    for heading, (key, value) in zip(failure_headings, final_failure_classification.items()):
        out += [heading, "─" * len(heading), ""]
        items = value["items"] if isinstance(value, dict) else value
        if isinstance(value, dict) and value.get("meaning"): out.append(value["meaning"])
        if not items: out.append("None proved.")
        for item in items:
            out.append("- " + (item if isinstance(item, str) else f"{item['operation']}: {item['classification']} ({len(item['occurrences'])} recovered occurrence(s))"))
        out.append("")
    return out

def render_security_classification() -> list[str]:
    key_order = ["HISTORICALLY_VERIFIED_SECURITY_MECHANISMS", "HISTORICALLY_VERIFIED_SECURITY_PROPERTIES", "SECURITY_GOALS_WITHOUT_ENFORCEMENT", "RETROSPECTIVE_SECURITY_INTERPRETATIONS", "CURRENT_PROPOSED_SECURITY_ARCHITECTURE", "UNKNOWN"]
    out = []
    for heading, key in zip(security_headings, key_order):
        out += [heading, "─" * len(heading), ""]
        items = final_security_classification[key]
        if not items: out.append("None proved.")
        for item in items:
            if isinstance(item, str): label = item
            else: label = item.get("mechanism", item.get("property", item.get("goal", item.get("interpretation", item.get("concept", str(item))))))
            out.append(f"- {label}")
        out.append("")
    return out

answers_md = []
for n, q, a, refs in answers:
    answers_md += [f"### {n}. {q}", "", a, "", "Evidence: " + ", ".join(f"`{x}`" for x in uniq(refs)), ""]

upstream = {
    "v1_v3_present": all((HS / x).exists() for x in ["SOURCE-MANIFEST.yaml", "LINEAGE.yaml", "RECONSTRUCTION-MANIFEST.yaml"]),
    "v1_validation": load(HS / "VALIDATION.yaml").get("overall", "UNKNOWN") if (HS / "VALIDATION.yaml").exists() else "MISSING",
    "v3_validation": load(HS / "RECONSTRUCTION-VALIDATION.yaml").get("overall", "UNKNOWN") if (HS / "RECONSTRUCTION-VALIDATION.yaml").exists() else "MISSING",
    "v4_present": (HS / "verification").exists(), "v5_present": (HS / "algorithm").exists(),
    "v6_present": (HS / "architecture").exists(), "v7_present": (HS / "contracts").exists(),
}
upstream["all_required_verified_inputs_available"] = upstream["v1_validation"] == "PASS" and upstream["v3_validation"] == "PASS" and all(upstream[x] for x in ["v4_present", "v5_present", "v6_present", "v7_present"])

report = f"""# Historical Generic Discovery Failure, Security & Trust-Boundary Evolution Archaeology Report

## Result and epistemic boundary

This Protocol-v8 corpus reconstructs historical **failure handling, security mechanisms, trust/authority boundaries, resource and concurrency safety, data/provenance integrity, and execution safety** from {len(snapshots)} exact or mechanically composed snapshots. Two partial alternatives remain uncertainty evidence and are not complete semantic models.

`FAILURE ≠ ERROR HANDLING ≠ FAILURE CONTAINMENT ≠ RECOVERY ≠ RESILIENCE`

`SECURITY MECHANISM ≠ SECURITY PROPERTY ≠ SECURITY ASSUMPTION ≠ SECURITY GUARANTEE`

`BOUNDARY ≠ TRUST BOUNDARY ≠ AUTHORITY BOUNDARY`

No historical runtime execution, exploit, incident, or security test result is claimed. “Observed failure” below means a failure representation/detection path observed in recovered source.

Input availability in this checkout at generation time: `{json.dumps(upstream, sort_keys=True)}`. Because the complete verified v1–v7 prerequisite set is not physically available and the available v1 validator currently reports failure, this is a **provisional source-derived v8 corpus**, not a claim of full prerequisite acceptance. The generator re-derives every v8 claim directionally from recovered source and never fabricates an absent upstream ledger.

## Central answer

The earliest recovered v0.1 is already a partial safety model: it has URL canonicalization/admission, same-origin-by-default configuration, maximum candidate/request/concurrency/time bounds, privileged and browser acquisition paths, Observation error/status recording, acquisition and persistence catches, provenance fields, and UI/export observability. It is not a verified secure system.

v0.2 adds the earliest recovered synchronous local claim protocol and reusable provider registry. Later competing branches add retry/backoff, AbortController paths, provider-local catches, richer provenance/diagnostics, response/per-origin/retention bounds, and eventually decision-ledger/policy/plan structures. These are path mechanisms. They do not establish whole-system isolation, cancellation, integrity, least authority, or resilience guarantees.

## Failure evolution

Across the recovered snapshots, mechanisms range from generic rejection/failed Observation/local logging to more differentiated parser/provider/scheduler/persistence diagnostics, retry/requeue, and structured records; this comparison does not prove monotonic lineage or superiority. Information preservation remains uneven: generic strings, null/empty fallbacks, and logging-only handlers can discard error type, stack, candidate/provider identity, request/response, or retry context.

Containment is assessed from actual handler control flow. F4–F6 labels apply only to the recovered candidate/provider/operation path. Rethrow/rejection and unresolved caller behavior remain UNKNOWN at the eventual scan boundary.

## Trust and authority

Page DOM, remote network content, providers/parsers, userscript APIs, storage, UI, and export are observable data or authority boundaries from v0.1. Internal scheduler structure is not automatically called a trust boundary. `@connect *` and privileged request APIs grant broad authority even where default policy is same-origin. Granted authority, configured policy, and actual use are tracked separately.

## Remote data and code/data boundary

Acquired HTML, JSON, XML, and text are parsed/extracted as data on located paths. No acquired-content-to-`eval`, `Function`, or dynamic-import path was found. UI `innerHTML` and later static page-bridge script insertion are separately recorded sinks; neither is silently relabelled remote-content execution. Absence of a located path is not a security guarantee.

## Concurrency, resources, and integrity

Synchronous claim mutations before `await` support event-loop-local ownership on selected paths. They do not prove thread safety, processing atomicity across `await`, distributed uniqueness, or complete failure cleanup. Candidate, request, worker, timeout, depth, response, per-origin, graph, diagnostic, and persistence bounds appear over time, but each is tied to its actual enforcement reference and failure behavior. Provenance identifiers support partial reconstruction; mutability and missing referential/immutability enforcement prevent an end-to-end integrity guarantee.

## Final answers

{chr(10).join(answers_md)}
## Final failure classification

{chr(10).join(render_failure_classification())}
## Final security classification

{chr(10).join(render_security_classification())}
## Governing conclusion

The strongest defensible historical model is path-specific: later recovered forms contain additional failure kinds, context records, local stopping/retry/cancellation paths, and resource controls, while branch comparisons remain non-lineage. It never becomes historically verified as secure or resilient. A catch is not isolation; a Set is not global uniqueness; a worker pool is not a complete resource guarantee; a URL parser is not policy; a provenance field is not provenance integrity; and an interface is not a security boundary.
"""
(OUT / "SECURITY-ARCHAEOLOGY-REPORT.md").write_text(report, encoding="utf-8", newline="\n")

readme = f"""# Historical Failure, Security & Trust-Boundary Archaeology

Protocol-v8 derived corpus. Historical source is never modified.

## Scope

- Semantic snapshots: {len(snapshots)}
- Partial variants retained only as uncertainty: {len(partial_snapshots)}
- Versions: {', '.join(versions)}
- Runtime/security tests recovered by this protocol: none
- Failure events are static source paths, not production incidents.
- Prerequisite status: {upstream['all_required_verified_inputs_available'] and 'all required v1–v7 inputs available' or 'BLOCKED: one or more required v1–v7 inputs missing/failed; corpus is provisional'}.

## Trust rules

1. Mechanism never silently becomes guarantee.
2. Actual control flow determines path-local containment.
3. Synchronous JavaScript claim sequences are not generalized across `await`.
4. Potential resource/race/integrity modes are not called demonstrated failures.
5. Same-version variants remain alternatives; adjacent versions are comparisons, not lineage.
6. Current/proposed security concepts are temporally isolated.

The main report is `SECURITY-ARCHAEOLOGY-REPORT.md`. Machine ledgers retain exact source evidence IDs; `EVIDENCE.yaml` resolves them to byte/line ranges and hashes.
"""
(OUT / "README.md").write_text(readme, encoding="utf-8", newline="\n")

# Manifest binds tools, source, upstream inputs, and all generator-owned outputs.
generator_names = sorted(list(machine_outputs) + [
    "README.md", "FAILURE-PROPAGATION.md", "RETRY-HISTORY.md", "TIMEOUT-HISTORY.md", "CANCELLATION-HISTORY.md",
    "RESOURCE-BOUND-HISTORY.md", "CONCURRENCY-SAFETY-HISTORY.md", "DATA-INTEGRITY-HISTORY.md", "PROVENANCE-INTEGRITY-HISTORY.md",
    "AUTHORITY-HISTORY.md", "USERSCRIPT-PERMISSION-HISTORY.md", "ORIGIN-SCOPE-HISTORY.md", "URL-TRUST-HISTORY.md",
    "CODE-DATA-BOUNDARY-HISTORY.md", "PARSER-SAFETY-HISTORY.md", "RESOURCE-EXHAUSTION-HISTORY.md", "OBSERVABILITY-HISTORY.md",
    "AUDITABILITY-HISTORY.md", "SECURITY-INVARIANT-HISTORY.md", "THREAT-MODEL-HISTORY.md", "SECURITY-REGRESSIONS.md",
    "SECURITY-IMPROVEMENTS.md", "FAILURE-CONTRACT-MAP.md", "SECURITY-ARCHITECTURE-MAP.md", "SECURITY-EVOLUTION-GRAPH.md",
    "SECURITY-ARCHAEOLOGY-REPORT.md", "SECURITY-FUNCTION-TRADEOFFS.md", "PRIVILEGED-API-HISTORY.md",
] + [f"{v}.md" for v in versions])
generator_names = sorted(set(generator_names))
input_paths = [MANIFEST, HS/"SOURCE-MANIFEST.yaml", HS/"LINEAGE.yaml", HS/"VALIDATION.yaml", HS/"RECONSTRUCTION-VALIDATION.yaml", HS/"analysis/CONCURRENCY-HISTORY.yaml", HS/"analysis/ACQUISITION-HISTORY.yaml", ROOT/"Userscript Discovery Prototype.md", ROOT/"Continue Architecture Planning.md"] + [paths[x["snapshot_id"]] for x in snapshots]
manifest = {
    "schema_version": SCHEMA, "protocol": "Historical Generic Discovery Failure, Security & Trust-Boundary Evolution Archaeology Protocol v8",
    "builder": BUILDER, "status": "GENERATED_NOT_HISTORICAL_SOURCE", "prerequisite_acceptance": "ELIGIBLE" if upstream["all_required_verified_inputs_available"] else "BLOCKED_MISSING_OR_FAILED_UPSTREAM", "tool_hashes": {
        "generator": sha_file(Path(__file__)),
        "validator": sha_file(HS/"tools/validate_security_archaeology.py") if (HS/"tools/validate_security_archaeology.py").exists() else None,
    },
    "upstream_availability": upstream,
    "scope": {"semantic_snapshots": [x["snapshot_id"] for x in snapshots], "partial_uncertainty_snapshots": [x["snapshot_id"] for x in partial_snapshots], "versions": versions},
    "counts": {"evidence": len(evidence), "failure_events": len(failure_events), "silent_failures": len(silent_failures), "failure_matrix_rows": len(failure_matrix), "failure_stage_rows": len(failure_stage_model), "resource_bounds": len(resource_bounds), "resource_risks": len(resource_risks), "shared_structures": len(concurrency_state), "race_candidates": len(race_analysis), "trust_boundaries": len(trust_boundaries), "authorities": len(authority_history), "authority_migrations": len(authority_migrations), "security_boundary_migrations": len(security_boundary_migrations), "privileged_apis": len(privileged_apis), "tradeoffs": len(security_tradeoffs), "provider_safety_rows": len(provider_safety), "parser_rows": len(parser_history), "questions": len(answers), "generator_outputs": len(generator_names)+1},
    "registries": {"failure_types": FAILURE_TYPES, "containment_levels": FAILURE_LEVELS, "security_claim_types": sorted(SECURITY_CLAIM_TYPES)},
    "input_hashes": {str(p.relative_to(ROOT)): sha_file(p) for p in sorted(set(input_paths), key=str) if p.exists()},
    "output_hashes": {f"historical-source/security/{name}": sha_file(OUT/name) for name in generator_names},
    "acceptance_constraints": {
        "mechanism_is_not_guarantee": True, "failure_event_is_not_runtime_incident": True, "no_thread_safe_generalization": True,
        "no_vulnerability_without_execution_path": True, "no_security_score": True, "no_chronology_as_causality": True,
        "same_version_variants_preserved": True, "temporal_backfill_forbidden": True,
    },
}
dump(OUT / "SECURITY-MANIFEST.yaml", manifest)

print(json.dumps({"status":"GENERATED", **manifest["counts"]}, indent=2))
