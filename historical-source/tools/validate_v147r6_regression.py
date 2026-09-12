#!/usr/bin/env python3
"""R6 append-only predecessor and semantic regression checks."""
import hashlib,json,os,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HIST=ROOT/"historical-source";COMP=HIST/"compliance";TOOLS=HIST/"tools";R6=COMP/"certification/v14.7-R6"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def command(script,cwd=ROOT):
 r=subprocess.run([sys.executable,str(script)],cwd=cwd,capture_output=True,text=True,env={**os.environ,"PYTHONDONTWRITEBYTECODE":"1"});return r.returncode==0,r.stdout[-1000:]
def isolated(script):
 with tempfile.TemporaryDirectory(prefix="v147r6-reg-") as temporary:
  target=Path(temporary)/"repo/historical-source"
  def ignore(src,names):
   omitted={"__pycache__","target"}
   if Path(src).name=="certification":omitted.add("v14.7-R6")
   return omitted&set(names)
  shutil.copytree(HIST,target,ignore=ignore);return command(target/"tools"/script,target.parent)
def main():
 p=json.loads((R6/"PRIOR-INTEGRITY.yaml").read_text());idx={x["path"]:x for x in p["artifacts"]};rows=[]
 rows.append(("PREDECESSOR_BYTES",len(idx)==1249 and all((COMP/k).is_file() and sha(COMP/k)==v["sha256"] and (COMP/k).stat().st_size==v["bytes"] for k,v in idx.items())))
 rows.append(("R5_INDEPENDENT_VALIDATION",isolated("validate_normative_realization_v147r5.py")[0]))
 ok,out=command(TOOLS/"run_v147r5_normative.py");rows.append(("R5_MACHINE_EXECUTION",ok and '"passed": 312' in out))
 ok,out=command(TOOLS/"run_v147r4_conformance.py");rows.append(("R4_VECTOR_EXECUTION",ok and '"passed": 79' in out))
 ok,out=command(TOOLS/"run_v147r6_conformance.py");rows.append(("R6_MACHINE_EXECUTION",ok and '"passed": 549' in out))
 rows.append(("R3_R6_RUST_EXCLUSION",'"v14.7-R6"' in (TOOLS/"validate_executable_boundary_contracts_v147r3.py").read_text()))
 rows.append(("R5_R6_SUCCESSOR_GUARD",'v14.7-R[6-9]' in (TOOLS/"build_normative_realization_v147r5.py").read_text()))
 rows.append(("NO_V14_8_OR_R7",not (COMP/"certification/v14.8").exists() and not (COMP/"certification/v14.7-R7").exists()))
 for name,ok in rows:print(f"{name}: {'PASS' if ok else 'FAIL'}")
 print(f"regression: {sum(x for _,x in rows)}/{len(rows)} PASS");return 1 if not all(x for _,x in rows) else 0
if __name__=="__main__":sys.exit(main())
