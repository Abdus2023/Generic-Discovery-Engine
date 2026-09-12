#!/usr/bin/env python3
"""Run v14.7-R3 executable boundary contract tests."""
import json
import sys
from pathlib import Path

from v147r3_boundary_contracts import (
    apply_conversion_rule,
    attach_recoverability,
    authority_precedence,
    compare_implementation_change,
    compare_profile_change,
    derive_conformance,
    distinct_approval_count,
    evaluate,
    replay_projection,
    validate_boundary_artifact,
    validate_boundary_rule,
    validate_for_evaluation,
)

BASE = Path(__file__).resolve().parents[1] / "compliance/certification/v14.7-R3"


def run(base=BASE):
    cases = json.loads((base / "MACHINE-TESTS.yaml").read_text())["objects"]
    rows = []
    for case in cases:
        operation = case["operation"]
        data = case["input"]
        actual = "HARNESS_ERROR"
        try:
            if operation == "BOUNDARY_VALIDATE":
                outcome = validate_boundary_artifact(data["artifact"], data.get("frozen_profile"))
                actual = outcome["status"] if not outcome.get("code") else f'{outcome["status"]}:{outcome["code"]}'
            elif operation == "CONVERSION":
                outcome = apply_conversion_rule(
                    data["source_domain"], data["source_state"], data["target_domain"], data["target_state"], data.get("rule")
                )
                actual = outcome["status"]
            elif operation == "PROFILE_CHANGE":
                actual = compare_profile_change(data["old"], data["new"])["status"]
            elif operation == "IMPLEMENTATION_CHANGE":
                actual = compare_implementation_change(data["old"], data["new"])["status"]
            elif operation == "AUTHORITY_PRECEDENCE":
                actual = authority_precedence(data["actor_layer"], data["target_layer"])["status"]
            elif operation == "APPROVAL_COUNT":
                actual = str(distinct_approval_count(data["approvals"], data["basis_hash"]))
            elif operation == "REPLAY_EQUAL":
                actual = "SAME" if replay_projection(data["left"]) == replay_projection(data["right"]) else "DIFFERENT"
            elif operation == "RULE_ASSERT":
                actual = validate_boundary_rule(data["rule_id"], data["artifact"])["status"]
            elif operation == "EVALUATION_GATE":
                actual = validate_for_evaluation(data["validation"], data["subject_ref"], data["context_ref"])["status"]
            elif operation == "EVALUATE":
                actual = evaluate(
                    data.get("validated_input"), data.get("predicate_ref"), data.get("inputs_ref"),
                    data.get("evaluator"), data.get("evaluation_time"), data.get("evidence_refs"), data.get("scope_ref")
                )["status"]
            elif operation == "CONFORMANCE":
                actual = derive_conformance(
                    data.get("requirement_ref"), data.get("scope_ref"), data.get("acceptance_criteria"),
                    data.get("evaluations", []), data.get("evidence_refs", []),
                    data.get("evidence_validation", "VALID"), data.get("evidence_mandatory", False)
                )["status"]
            elif operation == "RECOVERABILITY":
                actual = attach_recoverability(data["semantic_result"], data["diagnostic"])["status"]
            status = "PASSED" if actual == case["expected"] else "FAILED"
        except Exception as exc:
            actual = "HARNESS_ERROR"
            status = "INVALID"
        rows.append({
            "test_id": case["test_id"],
            "actual": actual,
            "expected": case["expected"],
            "status": status,
            "failure_origin": None if status == "PASSED" else "TEST_HARNESS_FAILURE",
        })
    return rows


def main():
    rows = run()
    output = {"objects": rows, "summary": {"total": len(rows), "passed": sum(x["status"] == "PASSED" for x in rows)}}
    print(json.dumps(output, indent=2))
    return 1 if any(x["status"] != "PASSED" for x in rows) else 0


if __name__ == "__main__":
    sys.exit(main())
