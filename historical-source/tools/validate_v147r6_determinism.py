#!/usr/bin/env python3
"""Regenerate and independently validate R6 in isolation."""
import json,os,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HIST=ROOT/"historical-source";BASE=HIST/"compliance/certification/v14.7-R6"
def main():
    manifest=json.loads((BASE/"GENERATOR-MANIFEST.yaml").read_text());env={**os.environ,"PYTHONDONTWRITEBYTECODE":"1"}
    with tempfile.TemporaryDirectory(prefix="v147r6-det-") as temporary:
        target=Path(temporary)/"repo/historical-source"
        def ignore(src,names):
            omitted={"__pycache__","target"}
            if Path(src).name=="certification":omitted.add("v14.7-R6")
            return omitted&set(names)
        shutil.copytree(HIST,target,ignore=ignore)
        for script in ["build_machine_domain_realization_v147r6.py","validate_machine_domain_realization_v147r6.py"]:
            result=subprocess.run([sys.executable,str(target/"tools"/script)],cwd=target.parent,capture_output=True,text=True,env=env)
            if result.returncode:print(result.stdout);print(result.stderr,file=sys.stderr);return 1
        made=target/"compliance/certification/v14.7-R6";mismatch=[p for p in manifest["paths"] if not (made/p).is_file() or (made/p).read_bytes()!=(BASE/p).read_bytes()]
        if sorted(str(p.relative_to(made)) for p in made.rglob("*") if p.is_file())!=manifest["paths"]:mismatch.append("<manifest-set>")
    print(f"determinism: {manifest['count']-len(mismatch)}/{manifest['count']} byte-identical")
    for p in mismatch:print("MISMATCH",p)
    return 1 if mismatch else 0
if __name__=="__main__":sys.exit(main())
