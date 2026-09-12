#!/usr/bin/env python3
"""Isolated deterministic regeneration check for v14.7-R4."""
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HISTORICAL = ROOT / "historical-source"
PACKAGE = HISTORICAL / "compliance/certification/v14.7-R4"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    manifest = json.loads((PACKAGE / "GENERATOR-MANIFEST.yaml").read_text())
    paths = manifest["paths"]
    with tempfile.TemporaryDirectory(prefix="gde-r4-det-") as temporary:
        root = Path(temporary)
        destination = root / "historical-source"
        shutil.copytree(HISTORICAL / "tools", destination / "tools")
        shutil.copytree(HISTORICAL / "compliance", destination / "compliance",
                        ignore=lambda path, names: ["v14.7-R4"] if Path(path).name == "certification" else [])
        process = subprocess.run(["python3", str(destination / "tools/build_reference_domain_model_v147r4.py")], cwd=root,
                                 capture_output=True, text=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
        regenerated = destination / "compliance/certification/v14.7-R4"
        rows = []
        for relative in paths:
            source = PACKAGE / relative
            candidate = regenerated / relative
            rows.append({"path": relative, "source_sha256": sha256(source),
                         "regenerated_sha256": sha256(candidate) if candidate.is_file() else None,
                         "identical": candidate.is_file() and source.read_bytes() == candidate.read_bytes()})
        ok = process.returncode == 0 and len(rows) == 200 and all(row["identical"] for row in rows)
    output = {"realization_version": "14.7-R4", "method": "ISOLATED_CLEAN_REGENERATION",
              "summary": {"total": len(rows), "identical": sum(row["identical"] for row in rows),
                          "different": sum(not row["identical"] for row in rows)},
              "objects": rows, "status": "PASS" if ok else "FAIL"}
    (PACKAGE / "DETERMINISM-VALIDATION.yaml").write_text(json.dumps(output, indent=2) + "\n")
    print(f'{output["status"]}: {output["summary"]["identical"]}/{len(rows)} byte-identical')
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
