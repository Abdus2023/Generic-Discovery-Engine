#!/usr/bin/env python3
"""Regenerate R5 in isolation and compare all generator-owned bytes."""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
HIST=ROOT/"historical-source"
BASE=HIST/"compliance/certification/v14.7-R5"


def main():
    manifest=json.loads((BASE/"GENERATOR-MANIFEST.yaml").read_text())
    with tempfile.TemporaryDirectory(prefix="v147r5-determinism-") as temporary:
        target=Path(temporary)/"repo/historical-source"
        def ignore(src,names):
            omitted={"__pycache__"}
            if Path(src).name=="certification": omitted.add("v14.7-R5")
            return omitted & set(names)
        shutil.copytree(HIST,target,ignore=ignore)
        builder=target/"tools/build_normative_realization_v147r5.py"
        validator=target/"tools/validate_normative_realization_v147r5.py"
        for command in ([sys.executable,str(builder)],[sys.executable,str(validator)]):
            result=subprocess.run(command,cwd=target.parent,capture_output=True,text=True)
            if result.returncode:
                print(result.stdout);print(result.stderr,file=sys.stderr);return 1
        generated=target/"compliance/certification/v14.7-R5"
        mismatches=[]
        for relative in manifest["paths"]:
            if not (generated/relative).is_file() or (BASE/relative).read_bytes()!=(generated/relative).read_bytes():mismatches.append(relative)
        actual=sorted(str(p.relative_to(generated)) for p in generated.rglob("*") if p.is_file())
        if actual!=manifest["paths"]:mismatches.append("<manifest-set>")
    print(f"determinism: {manifest['count']-len(mismatches)}/{manifest['count']} byte-identical")
    for path in mismatches:print(f"MISMATCH {path}")
    return 1 if mismatches else 0
if __name__=="__main__":sys.exit(main())
