#!/usr/bin/env python3
"""Isolated deterministic regeneration check for v14.7-R3."""
import ast
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


def constant(name):
    tree = ast.parse((HISTORICAL / "tools/build_executable_boundary_contracts_v147r3.py").read_text())
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id == name:
            return ast.literal_eval(node.value)
    raise KeyError(name)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    files = constant("FILES")
    schemas = constant("SCHEMAS")
    owned = files + [f"schema/{name}.schema.yaml" for name in schemas] + ["SPECIFICATION.md"]
    with tempfile.TemporaryDirectory(prefix="gde-r3-det-") as temporary:
        root = Path(temporary)
        destination = root / "historical-source"
        shutil.copytree(HISTORICAL / "tools", destination / "tools")
        shutil.copytree(HISTORICAL / "compliance", destination / "compliance",
                        ignore=lambda path, names: ["v14.7-R3"] if Path(path).name == "certification" else [])
        process = subprocess.run(
            ["python3", str(destination / "tools/build_executable_boundary_contracts_v147r3.py")],
            cwd=root, capture_output=True, text=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        regenerated = destination / "compliance/certification/v14.7-R3"
        rows = []
        for relative in owned:
            source = PACKAGE / relative
            candidate = regenerated / relative
            rows.append({
                "path": relative,
                "source_sha256": sha256(source),
                "regenerated_sha256": sha256(candidate) if candidate.is_file() else None,
                "identical": candidate.is_file() and source.read_bytes() == candidate.read_bytes(),
            })
        ok = process.returncode == 0 and len(rows) == 57 and all(row["identical"] for row in rows)
    output = {
        "realization_version": "14.7-R3", "method": "ISOLATED_CLEAN_REGENERATION",
        "summary": {"total": len(rows), "identical": sum(row["identical"] for row in rows),
                    "different": sum(not row["identical"] for row in rows)},
        "objects": rows, "status": "PASS" if ok else "FAIL",
    }
    (PACKAGE / "DETERMINISM-VALIDATION.yaml").write_text(json.dumps(output, indent=2) + "\n")
    print(f'{output["status"]}: {output["summary"]["identical"]}/{len(rows)} byte-identical')
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
