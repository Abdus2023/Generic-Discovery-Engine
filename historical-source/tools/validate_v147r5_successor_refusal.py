#!/usr/bin/env python3
"""Exercise R4/R5 immutability and R5 successor refusal."""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];HIST=ROOT/"historical-source";TOOLS=HIST/"tools"
def invoke(path,cwd):return subprocess.run([sys.executable,str(path)],cwd=cwd,capture_output=True,text=True)
def main():
    r4=invoke(TOOLS/"build_reference_domain_model_v147r4.py",ROOT)
    r5=invoke(TOOLS/"build_normative_realization_v147r5.py",ROOT)
    rows=[("R4_REFUSES_AFTER_R5",r4.returncode!=0 and "v14.7-R5" in r4.stderr),
          ("R5_REFUSES_REGENERATION",r5.returncode!=0 and "immutable v14.7-R5" in r5.stderr)]
    with tempfile.TemporaryDirectory(prefix="v147r5-successor-") as temporary:
        target=Path(temporary)/"repo/historical-source"
        def ignore(src,names):
            omitted={"__pycache__"}
            if Path(src).name=="certification":omitted.add("v14.7-R5")
            return omitted & set(names)
        shutil.copytree(HIST,target,ignore=ignore)
        successor=target/"compliance/certification/v14.7-R6";successor.mkdir();(successor/"MARKER").write_text("append-only successor\n")
        outcome=invoke(target/"tools/build_normative_realization_v147r5.py",target.parent)
        rows.append(("R5_REFUSES_AFTER_SUCCESSOR",outcome.returncode!=0 and "successor realization" in outcome.stderr))
    for name,ok in rows:print(f"{name}: {'PASS' if ok else 'FAIL'}")
    print(f"successor refusal: {sum(ok for _,ok in rows)}/{len(rows)} PASS")
    return 1 if not all(ok for _,ok in rows) else 0
if __name__=="__main__":sys.exit(main())
