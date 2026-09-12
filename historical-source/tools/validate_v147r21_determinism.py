#!/usr/bin/env python3
"""Isolated deterministic regeneration check for v14.7-R2.1."""
import hashlib,json,shutil,subprocess,tempfile
from pathlib import Path
R=Path(__file__).resolve().parents[2];H=R/'historical-source';D=H/'compliance/certification/v14.7-R2.1'
FILES=['VERSION.yaml','EXECUTIVE-RESULT.yaml','R2-AUDIT-FINDINGS.yaml','SEMANTIC-CONTRADICTIONS.yaml','REALIZATION-DEFECTS.yaml','SPECIFICATION-BASIS.yaml','PROFILE.yaml','PROFILE-CHOICE-CLASSIFICATION.yaml','PROFILE-CONFORMANCE.yaml','PROFILE-COMPATIBILITY.yaml','VALIDATION-RESULT-MODEL.yaml','EVALUATION-VALIDATION-BOUNDARY.yaml','OUTPUT-TAXONOMY.yaml','REQUIREMENTS.yaml','IMPLEMENTATION-INSTRUCTIONS.yaml','REALIZATION-MAPPING.yaml','IMPLEMENTATION-CONTRACT.yaml','IMPLEMENTATION-CONFORMANCE.yaml','FAILURE-ATTRIBUTION.yaml','COERCION-GUARDS.yaml','BOUNDARY-TESTS.yaml','BOUNDARY-TEST-RESULTS.yaml','ACCEPTANCE-CRITERIA.yaml','INVARIANTS.yaml','ARTIFACT-TREE.yaml','TRACEABILITY.yaml','ANTI-REGRESSION.yaml','OPEN-QUESTIONS.yaml','FINAL-PRINCIPLE.yaml','CURRENT-STATUS.yaml','SCHEMA-REGISTRY.yaml','PRIOR-INTEGRITY.yaml','VALIDATION-REPORT.yaml']
SCHEMAS=['profile','validation-result','evaluation-result','requirement','implementation-instruction','profile-compatibility','conformance-result','profile-binding','implementation-contract','failure-attribution']
OWNED=FILES+[f'schema/{x}.schema.yaml' for x in SCHEMAS]+['SPECIFICATION.md']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 with tempfile.TemporaryDirectory(prefix='gde-r21-det-') as t:
  root=Path(t);dst=root/'historical-source';shutil.copytree(H/'tools',dst/'tools')
  shutil.copytree(H/'compliance',dst/'compliance',ignore=lambda path,names:['v14.7-R2.1'] if Path(path).name=='certification' else [])
  r=subprocess.run(['python3',str(dst/'tools/build_frozen_boundary_realization_v147r21.py')],cwd=root,capture_output=True,text=True,env={'PYTHONDONTWRITEBYTECODE':'1'})
  generated=dst/'compliance/certification/v14.7-R2.1';rows=[]
  for x in OWNED:
   a=D/x;b=generated/x;rows.append({'path':x,'source_sha256':sha(a),'regenerated_sha256':sha(b) if b.is_file() else None,'identical':b.is_file() and a.read_bytes()==b.read_bytes()})
  ok=r.returncode==0 and len(rows)==44 and all(x['identical'] for x in rows)
 out={'profile_version':'14.7-R2.1','method':'ISOLATED_CLEAN_REGENERATION','summary':{'total':len(rows),'identical':sum(x['identical'] for x in rows),'different':sum(not x['identical'] for x in rows)},'objects':rows,'status':'PASS' if ok else 'FAIL'};(D/'DETERMINISM-VALIDATION.yaml').write_text(json.dumps(out,indent=2)+'\n');print(f"{out['status']}: {out['summary']['identical']}/{len(rows)} byte-identical");return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
