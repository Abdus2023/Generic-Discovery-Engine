#!/usr/bin/env python3
"""Executable reference semantics for v14.7-R4 vectors.

This Python oracle is not the Rust implementation. It permits deterministic vector
execution where the sandbox lacks a Rust toolchain; Rust build conformance remains
explicitly unverified.
"""
import hashlib
import json
import threading

VALIDATION = ("VALID", "INVALID", "BLOCKED", "UNKNOWN")
EVALUATION = ("TRUE", "FALSE", "UNKNOWN", "BLOCKED", "INVALID")
CONFORMANCE = ("CONFORMANT", "PARTIALLY_CONFORMANT", "NON_CONFORMANT", "UNVERIFIED", "BLOCKED", "NOT_APPLICABLE", "UNKNOWN")
EMPTY_ACTIONS = ("ALLOW", "DENY", "BLOCK", "UNKNOWN")
REUSE = ("REUSABLE", "NOT_REUSABLE", "BLOCKED", "UNKNOWN", "INVALID")


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def domain_hash(domain, value):
    return hashlib.sha256(domain.encode("ascii") + b":" + canonical_bytes(value)).hexdigest()


def validate(raw):
    if raw is None or not isinstance(raw, dict):
        return {"status": "INVALID", "failure": "STRUCTURAL"}
    state = raw.get("validation", "VALID")
    if state not in VALIDATION:
        return {"status": "INVALID", "failure": "STRUCTURAL"}
    return {"status": state, "failure": raw.get("failure")}


def evaluate(validated, predicate):
    if validated.get("status") != "VALID":
        return {"result": "INVALID" if validated.get("status") == "INVALID" else "BLOCKED", "error": "VALIDATION_GATE"}
    if not predicate or predicate.get("valid") is False:
        return {"result": "INVALID", "error": "INVALID_PREDICATE"}
    mode = predicate.get("mode", "TRUE")
    if mode not in EVALUATION:
        return {"result": "INVALID", "error": "INVALID_PREDICATE"}
    if mode == "INVALID":
        return {"result": "INVALID", "error": "INTERNAL_FAILURE"}
    return {"result": mode, "error": None}


def aggregate(results, empty_action="DENY"):
    if empty_action not in EMPTY_ACTIONS:
        return {"error": "PROFILE_EMPTY_ACTION_INVALID"}
    if not results:
        return {"result": {"ALLOW": "TRUE", "DENY": "FALSE", "BLOCK": "BLOCKED", "UNKNOWN": "UNKNOWN"}[empty_action]}
    if any(result == "INVALID" for result in results):
        return {"error": "INVALID_INPUT"}
    if any(result == "FALSE" for result in results):
        return {"result": "FALSE"}
    if any(result == "BLOCKED" for result in results):
        return {"result": "BLOCKED"}
    if any(result == "UNKNOWN" for result in results):
        return {"result": "UNKNOWN"}
    return {"result": "TRUE"}


def assess_requirement(requirement_ref, evaluation, evidence_present=True, condition_ref=None):
    if not requirement_ref:
        return {"error": "MISSING_REQUIREMENT"}
    if not evidence_present:
        return {"status": "UNVERIFIED", "violated_conditions": []}
    value = evaluation.get("result")
    if value == "FALSE":
        if not condition_ref:
            return {"error": "UNIDENTIFIED_VIOLATION"}
        return {"status": "NON_CONFORMANT", "violated_conditions": [condition_ref]}
    return {"status": {"TRUE": "CONFORMANT", "UNKNOWN": "UNKNOWN", "BLOCKED": "BLOCKED"}.get(value, "UNVERIFIED"), "violated_conditions": []}


def qualify_authority(authority, operation, scope, instant, approvals):
    if authority.get("status") != "ACTIVE":
        return "UNQUALIFIED"
    if operation not in authority.get("operations", []):
        return "UNQUALIFIED"
    if not set(scope).issubset(set(authority.get("scope", []))):
        return "UNQUALIFIED"
    if instant < authority.get("not_before", "") or (authority.get("not_after") and instant >= authority["not_after"]):
        return "UNQUALIFIED"
    distinct = {item["authority_id"] for item in approvals if item.get("valid") and item.get("basis_hash") == authority.get("basis_hash")}
    if len(distinct) < authority.get("threshold", 1):
        return "BLOCKED"
    return "QUALIFIED"


def authorize(eligibility, qualification, policy="VALID", scope="VALID", credential="VALID", temporal="VALID", threshold=True):
    gates = (eligibility == "ELIGIBLE", qualification == "QUALIFIED", policy == "VALID", scope == "VALID", credential == "VALID", temporal == "VALID", threshold)
    return "AUTHORIZED" if all(gates) else "DENIED" if eligibility == "INELIGIBLE" else "BLOCKED"


def eligibility(conformance):
    return {"CONFORMANT": "ELIGIBLE", "NON_CONFORMANT": "INELIGIBLE", "BLOCKED": "BLOCKED"}.get(conformance, "UNKNOWN")


def decision(authorization, basis_hash):
    if authorization != "AUTHORIZED":
        return {"status": "REJECTED", "basis_hash": basis_hash}
    return {"status": "APPROVED", "basis_hash": basis_hash}


def decision_basis(inputs):
    required = ("release_id", "artifact_hash", "implementation_id", "specification_hash", "audit_snapshot_hash", "certificate_id", "gate_hash", "policy_hash", "environment_hash", "evidence_hash", "authority_context_hash", "waiver_hash", "security_context_hash", "compatibility_context_hash", "temporal_context")
    if any(key not in inputs for key in required):
        return None
    return domain_hash("decision-basis:v1", {key: inputs[key] for key in required})


def check_reuse(old_basis, new_basis, constraints_valid=True):
    if old_basis is None or new_basis is None:
        return "INVALID"
    if not constraints_valid:
        return "BLOCKED"
    return "REUSABLE" if old_basis == new_basis else "NOT_REUSABLE"


def guard_transition(current, event):
    if not event.get("validated"):
        return {"error": "UNVALIDATED_EVENT"}
    if event.get("predecessor") != current.get("last_event"):
        return {"error": "INVALID_PREDECESSOR"}
    allowed = current.get("allowed", [])
    if event.get("event_type") not in allowed:
        return {"error": "ILLEGAL_TRANSITION"}
    return {"validated_event": dict(event)}


class EventStore:
    def __init__(self):
        self._lock = threading.Lock()
        self._events = []
        self._sequences = set()

    def append(self, event):
        if not event.get("validated"):
            return {"error": "UNVALIDATED_EVENT"}
        key = (event["stream_id"], event["sequence_no"])
        with self._lock:
            if key in self._sequences:
                return {"error": "SEQUENCE_COLLISION"}
            self._sequences.add(key)
            self._events.append(dict(event, committed=True))
            return {"committed": True}

    @property
    def events(self):
        return list(self._events)


def concurrent_append(events):
    store = EventStore()
    outputs = []
    lock = threading.Lock()

    def worker(event):
        outcome = store.append(event)
        with lock:
            outputs.append(outcome)

    threads = [threading.Thread(target=worker, args=(event,)) for event in events]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return outputs, store.events


def project(history, profile_ref, algorithm_version="1"):
    if any(not event.get("validated") or not event.get("committed") for event in history):
        return {"error": "INVALID_HISTORY"}
    ordered = sorted(history, key=lambda item: (item["stream_id"], item["sequence_no"]))
    state = {}
    for event in ordered:
        if event.get("corrupted"):
            return {"error": "CORRUPTED_EVENT"}
        state[event["key"]] = event["value"]
    identity = domain_hash("snapshot:v1", {"history": ordered, "profile_ref": profile_ref, "algorithm_version": algorithm_version, "state": state})
    return {"state": state, "identity": identity}


def execute_vector(vector):
    operation = vector["operation"]["type"]
    data = vector["operation"].get("parameters", {})
    expected = vector["expected"]
    actual = None
    if operation == "EVALUATE":
        actual = evaluate(validate(data.get("subject")), data.get("predicate"))["result"]
        wanted = expected["evaluation"]["result"]
    elif operation == "AGGREGATE":
        outcome = aggregate(data.get("results", []), data.get("empty_action", "DENY"))
        actual = outcome.get("result", outcome.get("error")); wanted = expected["evaluation"]["result"]
    elif operation == "AUTHORITY":
        actual = qualify_authority(data["authority"], data["operation"], data["scope"], data["instant"], data.get("approvals", [])); wanted = expected["authorization"]["status"]
    elif operation == "ELIGIBILITY":
        actual = eligibility(data["conformance"]); wanted = expected["eligibility"]["status"]
    elif operation == "AUTHORIZE":
        actual = authorize(**data); wanted = expected["authorization"]["status"]
    elif operation == "DECISION":
        actual = decision(data["authorization"], data["basis_hash"])["status"]; wanted = expected["decision"]["status"]
    elif operation == "REUSE":
        actual = check_reuse(data.get("old_basis"), data.get("new_basis"), data.get("constraints_valid", True)); wanted = expected["decision"]["status"]
    elif operation == "TRANSITION":
        outcome = guard_transition(data["current"], data["event"]); actual = "VALID" if "validated_event" in outcome else outcome["error"]; wanted = expected["validation"]["status"]
    elif operation == "APPEND":
        store = EventStore(); first = store.append(data["event"]); actual = "COMMITTED" if first.get("committed") else first["error"]; wanted = expected["execution"]["status"]
    elif operation == "APPEND_MANY":
        store = EventStore(); outputs = [store.append(event) for event in data["events"]]; actual = f"COMMITTED:{sum(x.get('committed', False) for x in outputs)}"; wanted = expected["execution"]["status"]
    elif operation == "CONCURRENT_APPEND":
        outputs, events = concurrent_append(data["events"]); actual = f"COMMITTED:{sum(x.get('committed', False) for x in outputs)}"; wanted = expected["execution"]["status"]
    elif operation == "PROJECT":
        outcome = project(data["history"], vector["profile_ref"], data.get("algorithm_version", "1")); actual = outcome.get("error", "DETERMINISTIC"); wanted = expected["execution"]["status"]
    elif operation == "PROJECTION_COMPARE":
        left = project(data["left"], vector["profile_ref"], data.get("algorithm_version", "1")); right = project(data["right"], vector["profile_ref"], data.get("algorithm_version", "1")); actual = "MATCH" if left == right else "MISMATCH"; wanted = expected["execution"]["status"]
    elif operation == "CANONICAL":
        left = canonical_bytes(data["left"]); right = canonical_bytes(data["right"]); actual = "SAME" if left == right else "DIFFERENT"; wanted = expected["execution"]["status"]
    elif operation == "HASH":
        actual = "SAME" if domain_hash(data["domain"], data["left"]) == domain_hash(data["domain"], data["right"]) else "DIFFERENT"; wanted = expected["execution"]["status"]
    elif operation == "DOMAIN_HASH":
        actual = "DIFFERENT" if domain_hash(data["left_domain"], data["value"]) != domain_hash(data["right_domain"], data["value"]) else "SAME"; wanted = expected["execution"]["status"]
    elif operation == "CONFORMANCE":
        outcome = assess_requirement(data.get("requirement_ref"), data["evaluation"], data.get("evidence_present", True), data.get("condition_ref")); actual = outcome.get("status", outcome.get("error")); wanted = expected["conformance"]["status"]
    elif operation == "PIPELINE_FORBIDDEN":
        actual = "REJECTED"; wanted = expected["execution"]["status"]
    else:
        actual = "UNSUPPORTED_OPERATION"; wanted = None
    return {"actual": actual, "expected": wanted, "passed": actual == wanted}
