#!/usr/bin/env python3
"""Isolated predecessor regression and append-only guard checks for v14.7-R3."""
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HISTORICAL = ROOT / "historical-source"
PACKAGE = HISTORICAL / "compliance/certification/v14.7-R3"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    environment = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    rows = []
    with tempfile.TemporaryDirectory(prefix="gde-r3-reg-") as temporary:
        root = Path(temporary)
        destination = root / "historical-source"
        shutil.copytree(HISTORICAL / "tools", destination / "tools")
        shutil.copytree(HISTORICAL / "compliance", destination / "compliance")
        cases = [
            ("REG-01", "validate_frozen_boundary_realization_v147r21.py", 0),
            ("REG-02", "validate_executable_realization_v147r2.py", 0),
            ("REG-03", "validate_v147_conformance_correction_v1471.py", 0),
            ("REG-04", "build_frozen_boundary_realization_v147r21.py", "REFUSE"),
            ("REG-05", "build_executable_realization_v147r2.py", "REFUSE"),
            ("REG-06", "build_executable_boundary_contracts_v147r3.py", "REFUSE"),
        ]
        for identifier, script, expected in cases:
            process = subprocess.run(["python3", str(destination / "tools" / script)], cwd=root,
                                     capture_output=True, text=True, env=environment)
            output = process.stdout + process.stderr
            passed = process.returncode == expected if isinstance(expected, int) else (
                process.returncode != 0 and ("refus" in output.lower() or "immutable" in output.lower())
            )
            rows.append({"check_id": identifier, "script": script, "returncode": process.returncode,
                         "expected": expected, "passed": passed, "output_tail": output[-500:]})
    prior = json.loads((PACKAGE / "PRIOR-INTEGRITY.yaml").read_text())
    mismatches = []
    for item in prior["artifacts"]:
        path = HISTORICAL / "compliance" / item["path"]
        if not path.is_file() or path.stat().st_size != item["bytes"] or sha256(path) != item["sha256"]:
            mismatches.append(item["path"])
    preserved = prior["protected_artifact_count"] == len(prior["artifacts"]) == 900 and not mismatches
    rows.append({"check_id": "REG-07", "script": "PRIOR-INTEGRITY.yaml", "returncode": 0 if preserved else 1,
                 "expected": 0, "passed": preserved, "output_tail": f"mismatches={mismatches[:10]}"})
    ok = all(row["passed"] for row in rows)
    output = {"realization_version": "14.7-R3", "method": "ISOLATED_PREDECESSOR_VALIDATION_AND_SUCCESSOR_GUARDS",
              "objects": rows, "status": "PASS" if ok else "FAIL"}
    (PACKAGE / "REGRESSION-VALIDATION.yaml").write_text(json.dumps(output, indent=2) + "\n")
    print(f'{output["status"]}: {sum(row["passed"] for row in rows)}/{len(rows)}')
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
