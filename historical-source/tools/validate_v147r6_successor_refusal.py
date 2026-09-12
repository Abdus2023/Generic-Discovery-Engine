#!/usr/bin/env python3
"""Exercise R5/R6 immutability and R6 successor refusal."""
import os,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HIST=ROOT/"historical-source";TOOLS=HIST/"tools";ENV={**os.environ,"PYTHONDONTWRITEBYTECODE":"1"}
def invoke(p,c):return subprocess.run([sys.executable,str(p)],cwd=c,capture_output=True,text=True,env=ENV)
def main():
 r5=invoke(TOOLS/"build_normative_realization_v147r5.py",ROOT);r6=invoke(TOOLS/"build_machine_domain_realization_v147r6.py",ROOT)
 rows=[("R5_REFUSES_AFTER_R6",r5.returncode!=0 and "successor realization" in r5.stderr),("R6_REFUSES_REGENERATION",r6.returncode!=0 and "immutable v14.7-R6" in r6.stderr)]
 with tempfile.TemporaryDirectory(prefix="v147r6-successor-") as temporary:
  target=Path(temporary)/"repo/historical-source"
  def ignore(src,names):
   omitted={"__pycache__","target"}
   if Path(src).name=="certification":omitted.add("v14.7-R6")
   return omitted&set(names)
  shutil.copytree(HIST,target,ignore=ignore);successor=target/"compliance/certification/v14.7-R7";successor.mkdir();(successor/"MARKER").write_text("successor\n")
  out=invoke(target/"tools/build_machine_domain_realization_v147r6.py",target.parent);rows.append(("R6_REFUSES_AFTER_R7",out.returncode!=0 and "successor realization" in out.stderr))
 for name,ok in rows:print(f"{name}: {'PASS' if ok else 'FAIL'}")
 print(f"successor refusal: {sum(x for _,x in rows)}/{len(rows)} PASS");return 1 if not all(x for _,x in rows) else 0
if __name__=="__main__":sys.exit(main())
