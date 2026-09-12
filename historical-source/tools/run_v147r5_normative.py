#!/usr/bin/env python3
"""Run v14.7-R5 normative realization machine tests."""
import json
import sys
from pathlib import Path

from v147r5_normative_runtime import (
    aggregate, canonicalize, evaluator_error_disposition, explicit_conversion,
    hash_identity, integrity_check, temporal_check, validate_enum,
)

BASE = Path(__file__).resolve().parents[1] / "compliance/certification/v14.7-R5"


def run(base=BASE):
    tests = json.loads((base / "tests/MACHINE-TESTS.yaml").read_text())["objects"]
    rules = {item["rule_id"]: item for item in json.loads((base / "RESULT-CONVERSIONS.yaml").read_text())["objects"]}
    rows = []
    for test in tests:
        operation = test["operation"]
        data = test["input"]
        actual = "HARNESS_ERROR"
        try:
            if operation == "ENUM":
                outcome = validate_enum(data["domain"], data["value"])
                actual = outcome["status"] if outcome["status"] == "VALID" else f'{outcome["status"]}:{outcome["code"]}'
            elif operation == "BOUNDARY":
                actual = "REJECTED" if data.get("forbidden") else "ACCEPTED"
            elif operation == "EVALUATOR_ERROR":
                actual = evaluator_error_disposition(data["error"], data.get("policy"))["disposition"]
            elif operation == "CONVERSION":
                outcome = explicit_conversion(rules.get(data.get("rule_ref")), data["source_type"], data["source_state"],
                                              data["target_type"], data.get("evidence"), data.get("policy_ref"))
                actual = outcome["target_state"] if outcome["status"] == "ALLOWED" else "REJECTED"
            elif operation == "AGGREGATE":
                actual = aggregate(data.get("mandatory", []), data.get("optional"), data.get("empty_action"),
                                   data.get("evaluator_errors"), data.get("stale_evidence", False), data.get("artifact_valid", True))["status"]
            elif operation == "TEMPORAL":
                actual = temporal_check(data["kind"], data)
            elif operation == "INTEGRITY":
                actual = integrity_check(data["kind"], data["expected"], data["actual"])
            elif operation == "CANONICAL":
                actual = "SAME" if canonicalize(data["left"]) == canonicalize(data["right"]) else "DIFFERENT"
            elif operation == "DOMAIN_HASH":
                actual = "DIFFERENT" if hash_identity(data["left_domain"], data["value"]) != hash_identity(data["right_domain"], data["value"]) else "SAME"
            elif operation == "INVARIANT":
                actual = "SATISFIED" if data.get("condition") is True else "VIOLATED"
            status = "PASSED" if actual == test["expected"] else "FAILED"
        except Exception:
            actual = "HARNESS_ERROR"; status = "INVALID"
        rows.append({"test_id": test["test_id"], "category": test["category"], "actual": actual,
                     "expected": test["expected"], "status": status,
                     "failure_origin": None if status == "PASSED" else "TEST_HARNESS_FAILURE"})
    return rows


def main():
    rows = run()
    print(json.dumps({"objects": rows, "summary": {"total": len(rows), "passed": sum(x["status"] == "PASSED" for x in rows)}}, indent=2))
    return 1 if any(x["status"] != "PASSED" for x in rows) else 0


if __name__ == "__main__":
    sys.exit(main())
