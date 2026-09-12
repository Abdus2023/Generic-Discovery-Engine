#!/usr/bin/env python3
"""Validate predecessor behavior and R5 append-only regression boundaries."""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
HIST=ROOT/"historical-source";TOOLS=HIST/"tools";COMP=HIST/"compliance";R5=COMP/"certification/v14.7-R5"

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def command(path,cwd=ROOT):
    environment={**os.environ,"PYTHONDONTWRITEBYTECODE":"1"}
    result=subprocess.run([sys.executable,str(path)],cwd=cwd,capture_output=True,text=True,env=environment)
    return result.returncode==0,result.stdout[-1000:]
def isolated(script):
    with tempfile.TemporaryDirectory(prefix="v147r5-regression-") as temporary:
        target=Path(temporary)/"repo/historical-source"
        def ignore(_src,names):return {"__pycache__","target"}&set(names)
        shutil.copytree(HIST,target,ignore=ignore)
        return command(target/"tools"/script,target.parent)
def main():
    rows=[]
    prior=json.loads((R5/"PRIOR-INTEGRITY.yaml").read_text());indexed={x["path"]:x for x in prior["artifacts"]}
    rows.append(("PREDECESSOR_BYTES",len(indexed)==1165 and all((COMP/p).is_file() and sha(COMP/p)==x["sha256"] and (COMP/p).stat().st_size==x["bytes"] for p,x in indexed.items())))
    rows.append(("R3_INDEPENDENT_VALIDATION",isolated("validate_executable_boundary_contracts_v147r3.py")[0]))
    ok,out=command(TOOLS/"run_v147r4_conformance.py");rows.append(("R4_VECTOR_EXECUTION",ok and '"passed": 79' in out))
    rows.append(("R4_INDEPENDENT_VALIDATION",isolated("validate_reference_domain_model_v147r4.py")[0]))
    ok,out=command(TOOLS/"run_v147r5_normative.py");rows.append(("R5_MACHINE_EXECUTION",ok and '"passed": 312' in out))
    r3=(TOOLS/"validate_executable_boundary_contracts_v147r3.py").read_text();rows.append(("R3_SUCCESSOR_RUST_EXCLUSION",'"v14.7-R5"' in r3))
    r4=(TOOLS/"build_reference_domain_model_v147r4.py").read_text();rows.append(("R4_SUCCESSOR_GUARD",'certification/v14.7-R5' in r4))
    rows.append(("NO_V14_8",not (COMP/"certification/v14.8").exists()))
    for name,ok in rows:print(f"{name}: {'PASS' if ok else 'FAIL'}")
    print(f"regression: {sum(ok for _,ok in rows)}/{len(rows)} PASS")
    return 1 if not all(ok for _,ok in rows) else 0
if __name__=="__main__":sys.exit(main())
