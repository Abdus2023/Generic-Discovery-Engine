#!/usr/bin/env python3
"""Execute all v14.7-R4 golden, negative, boundary, and property vectors."""
import json
import sys
from pathlib import Path

from v147r4_reference_runtime import execute_vector

BASE = Path(__file__).resolve().parents[1] / "compliance/certification/v14.7-R4"


def run(base=BASE):
    vectors = []
    for category in ("golden", "negative", "boundary", "property"):
        for path in sorted((base / "vectors" / category).glob("*.yaml")):
            vector = json.loads(path.read_text())
            vector["_path"] = str(path.relative_to(base))
            vectors.append(vector)
    rows = []
    for vector in vectors:
        try:
            outcome = execute_vector(vector)
            rows.append({"test_id": vector["test_id"], "category": vector["category"], "vector_path": vector["_path"],
                         "actual": outcome["actual"], "expected": outcome["expected"],
                         "status": "PASSED" if outcome["passed"] else "FAILED", "failure_category": None if outcome["passed"] else "ORACLE_FAILURE"})
        except Exception as error:
            rows.append({"test_id": vector["test_id"], "category": vector["category"], "vector_path": vector["_path"],
                         "actual": "HARNESS_ERROR", "expected": None, "status": "INVALID", "failure_category": "HARNESS_FAILURE"})
    return rows


def main():
    rows = run()
    output = {"objects": rows, "summary": {"total": len(rows), "passed": sum(row["status"] == "PASSED" for row in rows)}}
    print(json.dumps(output, indent=2))
    return 1 if any(row["status"] != "PASSED" for row in rows) else 0


if __name__ == "__main__":
    sys.exit(main())
