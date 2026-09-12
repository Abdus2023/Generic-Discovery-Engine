#!/usr/bin/env python3
"""Isolated predecessor-regression and append-only guard checks for R2.1."""
import json,os,shutil,subprocess,tempfile
from pathlib import Path
R=Path(__file__).resolve().parents[2];H=R/'historical-source';D=H/'compliance/certification/v14.7-R2.1'
def main():
 env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'};rows=[]
 with tempfile.TemporaryDirectory(prefix='gde-r21-reg-') as t:
  root=Path(t);dst=root/'historical-source';shutil.copytree(H/'tools',dst/'tools');shutil.copytree(H/'compliance',dst/'compliance')
  for i,script,expected in [('REG-01','validate_executable_realization_v147r2.py',0),('REG-02','validate_v147_conformance_correction_v1471.py',0),('REG-03','build_executable_realization_v147r2.py','refuse'),('REG-04','build_frozen_boundary_realization_v147r21.py','refuse')]:
   p=subprocess.run(['python3',str(dst/'tools'/script)],cwd=root,capture_output=True,text=True,env=env)
   passed=(p.returncode==expected) if isinstance(expected,int) else (p.returncode!=0 and ('refus' in (p.stdout+p.stderr).lower() or 'immutable' in (p.stdout+p.stderr).lower()))
   rows.append({'check_id':i,'script':script,'returncode':p.returncode,'expected':expected,'passed':passed,'output_tail':(p.stdout+p.stderr)[-500:]})
 prior=json.loads((D/'PRIOR-INTEGRITY.yaml').read_text());preserved=prior['protected_artifact_count']==852 and all((H/'compliance'/x['path']).is_file() for x in prior['artifacts']);rows.append({'check_id':'REG-05','script':'PRIOR-INTEGRITY.yaml','returncode':0 if preserved else 1,'expected':0,'passed':preserved,'output_tail':'852 predecessor records present'})
 ok=all(x['passed'] for x in rows);out={'profile_version':'14.7-R2.1','method':'ISOLATED_PREDECESSOR_VALIDATION_AND_SUCCESSOR_GUARDS','objects':rows,'status':'PASS' if ok else 'FAIL'};(D/'REGRESSION-VALIDATION.yaml').write_text(json.dumps(out,indent=2)+'\n');print(out['status']+': '+str(sum(x['passed'] for x in rows))+'/'+str(len(rows)));return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
