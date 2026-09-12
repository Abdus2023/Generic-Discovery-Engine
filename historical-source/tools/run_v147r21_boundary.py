#!/usr/bin/env python3
"""Execute R2.1 boundary and coercion tests."""
import json,sys
from pathlib import Path
from v147r21_boundary_harness import *
BASE=Path(__file__).resolve().parents[1]/'compliance/certification/v14.7-R2.1'
def artifact_assertion(base,name):
 def ld(n):return json.loads((base/n).read_text())
 p=ld('PROFILE.yaml');v=ld('VALIDATION-RESULT-MODEL.yaml');o=ld('OUTPUT-TAXONOMY.yaml');b=ld('EVALUATION-VALIDATION-BOUNDARY.yaml');pc=ld('PROFILE-CONFORMANCE.yaml');ic=ld('IMPLEMENTATION-CONFORMANCE.yaml');impl=ld('IMPLEMENTATION-CONTRACT.yaml');req=ld('REQUIREMENTS.yaml')['objects'];ins=ld('IMPLEMENTATION-INSTRUCTIONS.yaml')['objects'];trace=ld('TRACEABILITY.yaml');compat=ld('PROFILE-COMPATIBILITY.yaml');fail=ld('FAILURE-ATTRIBUTION.yaml');coerce=ld('COERCION-GUARDS.yaml')['forbidden'];ver=ld('VERSION.yaml');tree=ld('ARTIFACT-TREE.yaml')
 checks={
  'AC-01':set(('specification','serialization','hashing','signatures','time','events','policy','limits','compatibility','choice_universe','semantic_preservation','choice_classification'))<=set(p) and p['choice_universe']['closed'] and p['semantic_preservation']['semantic_states']=='UNCHANGED' and {x['status'] for x in p['choice_classification']}=={'FIXED','PROFILE-SELECTABLE','IMPLEMENTATION-DEFINED'},
  'AC-02':v['statuses']==['VALID','INVALID','BLOCKED','UNKNOWN'] and set(v['forbidden'])=={'TRUE','FALSE'},
  'AC-03':o['EvaluationResult']==['TRUE','FALSE','UNKNOWN','BLOCKED','INVALID'] and b['validation_valid']=='EVALUATION_PERMITTED' and not b['evaluator_bypass'],
  'AC-04':pc['claim']=='ProfileConformant(P,S)' and ic['claim']=='ImplementationSatisfiesProfile(I,P)' and pc['result']=='CONFORMANT',
  'AC-05':impl['profile_id']==p['profile_id'] and impl['profile_version']==p['profile_version'] and ic['result']=='UNVERIFIED',
  'AC-06':len(req)==12 and len(ins)>0 and all(not x['mandatory'] or x['authority_ref'] for x in ins),
  'AC-07':trace['chain']==['OBJECT','VALIDATION','EVALUATION_ELIGIBILITY','EVALUATION','REQUIREMENT_RESULT','CONFORMANCE','ELIGIBILITY','AUTHORIZATION','DECISION','EXECUTION','VERIFICATION'] and trace['reverse'],
  'AC-08':compat['classification']=='CONVERTIBLE' and compat['migration_required'] and compat['semantic_equivalence']=='UNKNOWN',
  'AC-09':len(fail['origins'])==11 and not fail['automatic_implementation_attribution'],
  'AC-10':len(coerce)==9,
  'AC-11':[x['requirement_id'] for x in req]==[f'R-BOUNDARY-{i:03d}' for i in range(1,13)],
  'AC-12':ver['semantic_version']=='v14.7' and not ver['new_semantic_layer'] and not tree['moves_history'] and len(tree['groups'])==6,
 }
 return 'PASS' if checks.get(name,False) else 'FAIL'
def run(base=BASE):
 cases=json.loads((base/'BOUNDARY-TESTS.yaml').read_text())['objects'];out=[]
 for c in cases:
  op=c['operation'];p=c['input'];actual='HARNESS_ERROR'
  try:
   if op=='SCOPE_VALIDATE':actual=ScopeValidator().validate(p['requested'],p['granted'])['status']
   elif op=='EVIDENCE_VALIDATE':actual=EvidenceValidator().validate(p.get('evidence'))['status']
   elif op=='TEMPORAL_VALIDATE':actual=TemporalValidator().validate_interval(p['instant'],p['not_before'],p.get('not_after'))['status']
   elif op=='VALIDATED_EVALUATE':actual=ValidatedEvaluator().evaluate(p['validation'],p.get('subject',{'x':1}),p.get('predicate',{'op':'equals','field':'x','value':1}),{'sealed':True},{'evaluator_id':'e','version':'1','hash':'h'})['status']
   elif op=='CONFORMANCE':actual=ConformanceEvaluator().derive(p['applicable'],p['mandatory'],p.get('optional',[]))['status']
   elif op=='COERCION':actual=forbidden_coercion(*p['conversion'])['status']
   elif op=='PROFILE':actual=ProfileConformanceChecker().check(p['profile'],p['specification'])['status']
   elif op=='IMPLEMENTATION':actual=ImplementationConformanceChecker().check(p['implementation'],p['profile'],p['checks'])['status']
   elif op=='ARTIFACT_ASSERTION':actual=artifact_assertion(base,p['acceptance_criterion'])
   status='PASSED' if actual==c['expected'] else 'FAILED'
  except Exception as e:status='INVALID';actual='HARNESS_ERROR'
  out.append({'test_id':c['test_id'],'actual':actual,'expected':c['expected'],'status':status,'failure_origin':None if status=='PASSED' else 'TEST_HARNESS_FAILURE'})
 return out
def main():
 x=run();print(json.dumps({'objects':x,'summary':{'total':len(x),'passed':sum(y['status']=='PASSED' for y in x)}},indent=2));return 1 if any(y['status']!='PASSED' for y in x) else 0
if __name__=='__main__':sys.exit(main())
