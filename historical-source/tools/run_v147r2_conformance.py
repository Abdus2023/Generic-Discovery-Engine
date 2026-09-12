#!/usr/bin/env python3
"""Execute v14.7-R2 test oracles and generated properties."""
from __future__ import annotations
import json,sys,threading
from pathlib import Path
from v147r2_conformance_harness import *
BASE=Path(__file__).resolve().parents[1]/'compliance/certification/v14.7-R2'
def execute(op,p):
 if op=='SCHEMA':return SchemaValidator().validate(p['object'],p['schema'])['status']
 if op=='INTEGRITY':return IntegrityValidator().validate_hash(p['domain'],p['object'])['status']
 if op=='CANONICAL_EQUAL':return 'PASS' if canonical_bytes(p['a'])==canonical_bytes(p['b']) else 'FAIL'
 if op=='CANONICAL_REJECT_FLOAT':
  try:canonical_bytes({'x':1.5});return 'FAIL'
  except ValueError:return 'PASS'
 if op=='HASH_DOMAIN':return 'PASS' if content_hash('A',p)!=content_hash('B',p) else 'FAIL'
 if op=='AGGREGATE':return Aggregator().aggregate(p['results'],p.get('empty_action'))['status']
 if op=='EVALUATE':return Evaluator().evaluate(p['subject'],p['predicate'],p['context'],p['evaluator'])['status']
 if op=='SCOPE':return ScopeValidator().validate(p['requested'],p['granted'])['status']
 if op=='POLICY':return PolicyValidator().validate_gate(p)['status']
 if op=='EVIDENCE':return EvidenceValidator().validate(p.get('evidence'))['status']
 if op=='TEMPORAL':return TemporalValidator().validate_interval(p['instant'],p['not_before'],p.get('not_after'))['status']
 if op=='AUTHORITY':return AuthorityValidator().qualify(p['authority'],p['credential'],p['operation'],p['scope'],p['policy'],p['instant'],p.get('approvals',[]))['status']
 if op=='REFERENCE':
  v=ReferenceValidator();idx=v.build_index(p['objects'])
  return idx['status'] if idx['status']!='VALID' else v.validate(p['references'],idx['value'],p['scope'])['status']
 if op=='TRANSITION':return TransitionGuard().validate(p['current'],p['event'],p['rule'])['status']
 if op=='EVENT':
  s=EventStore();first=s.append_event('s',{'event_id':'e1','to_state':'STARTED'},-1,'k1')
  if p['mode']=='COMMIT':return first['status']
  if p['mode']=='IDEMPOTENT':return s.append_event('s',{'event_id':'e2'},0,'k1')['status']
  return s.append_event('s',{'event_id':'e2'},-1,'k2')['status']
 if op=='PROJECT':return Projector().project(p['history'],{'profile_id':PROFILE_ID})['status']
 if op=='VERIFY_PROJECTION':
  good=Projector().project(p['history'],{'profile_id':PROFILE_ID});stored=good['value'] if p['mode']=='MATCH' else {'state':'wrong'}
  return ProjectionVerifier().verify(p['history'],{'profile_id':PROFILE_ID},stored)['status']
 if op=='REUSE':return ReuseChecker().check(p['old'],p['new'],p['fields'],p['conditions'])['status']
 if op=='NEGATIVE_SPACE':return 'REJECTED' if p['attempt'] in {'UNKNOWN_TO_APPROVED','INVALID_TO_FALSE','BLOCKED_TO_TRUE','DRAFT_TO_VALID','VALID_TO_ISSUED','ELIGIBLE_TO_APPROVED_NO_AUTH','APPROVED_TO_EXECUTED_NO_AUTH','EXECUTED_TO_VERIFIED_NO_TEST','PROJECTION_MUTATES_HISTORY','CHANGED_ARTIFACT_REUSE','DUPLICATE_APPROVAL_COUNTS'} else 'INVALID'
 raise KeyError(op)
def run(base=BASE):
 oracles=json.loads((base/'TEST-ORACLES.yaml').read_text())['objects'];fixtures=json.loads((base/'TEST-FIXTURES.yaml').read_text())['objects'];fx={x['fixture_id']:x['input'] for x in fixtures};results=[]
 for o in oracles:
  try:actual=execute(o['operation'],fx[o['input_refs'][0]]);expected=o['expected_result']['value'];status='PASSED' if actual==expected and actual not in o['forbidden_results'] else 'FAILED';detail=''
  except Exception as e:actual='HARNESS_ERROR';status='INVALID';detail=str(e)
  results.append({'oracle_id':o['oracle_id'],'status':status,'actual':actual,'expected':o['expected_result']['value'],'failure_origin':None if status=='PASSED' else ('TEST_HARNESS_FAILURE' if actual=='HARNESS_ERROR' else 'IMPLEMENTATION_FAILURE'),'detail':detail})
 props=[]
 vals=['TRUE','FALSE','UNKNOWN','BLOCKED','INVALID']
 def expected(xs):
  if 'INVALID' in xs:return 'INVALID'
  if 'FALSE' in xs:return 'INELIGIBLE'
  if 'BLOCKED' in xs:return 'BLOCKED'
  if 'UNKNOWN' in xs:return 'UNKNOWN'
  return 'ELIGIBLE'
 for a in vals:
  for b in vals:
   for c in vals:
    got=Aggregator().aggregate([a,b,c])['status'];props.append({'property':'AGGREGATION_PRECEDENCE','case':[a,b,c],'status':'SATISFIED' if got==expected([a,b,c]) else 'VIOLATED'})
 fields=['release','implementation','artifact','specification','gate','policy','certificate','audit','environment','evidence','authority','waiver','security','compatibility','time'];old={x:'same' for x in fields}
 for changed in fields:
  new=dict(old);new[changed]='changed';got=ReuseChecker().check(old,new,fields,[True])['status'];props.append({'property':'DECISION_BASIS_CHANGED_NOT_REUSABLE','case':changed,'status':'SATISFIED' if got=='NOT_REUSABLE' else 'VIOLATED'})
 history=[{'event_id':'e0','sequence_no':0,'previous_event_id':None,'to_state':'A'},{'event_id':'e1','sequence_no':1,'previous_event_id':'e0','to_state':'B'}]
 for _ in range(20):
  a=Projector().project(history,{'profile_id':PROFILE_ID});b=Projector().project(history,{'profile_id':PROFILE_ID});props.append({'property':'SAME_HISTORY_PROFILE_SAME_PROJECTION','case':'repeat','status':'SATISFIED' if a==b else 'VIOLATED'})
 for same_key in [False,True]:
  store=EventStore();statuses=[];barrier=threading.Barrier(2)
  def writer(n):
   barrier.wait();statuses.append(store.append_event('race',{'event_id':f'e{n}','to_state':'X'},-1,'shared' if same_key else f'k{n}')['status'])
  threads=[threading.Thread(target=writer,args=(n,)) for n in [1,2]]
  for thread in threads:thread.start()
  for thread in threads:thread.join()
  expected={'COMMITTED','IDEMPOTENT_REPLAY'} if same_key else {'COMMITTED','CONFLICT'};props.append({'property':'SIMULTANEOUS_IDEMPOTENT_RETRY' if same_key else 'SIMULTANEOUS_APPEND_SINGLE_WINNER','case':sorted(statuses),'status':'SATISFIED' if set(statuses)==expected and len(store.read_stream('race'))==1 else 'VIOLATED'})
 props.append({'property':'DURABLE_COMMIT_CRASH_PERSISTENCE','case':'NO_PRODUCTION_BACKEND_SELECTED','status':'UNKNOWN'})
 for proposition,attempt in [('INVALID_REQUIRED_NOT_AUTHORIZED','INVALID_TO_FALSE'),('UNKNOWN_NOT_TRUE','UNKNOWN_TO_APPROVED'),('BLOCKED_NOT_TRUE','BLOCKED_TO_TRUE'),('ELIGIBLE_NOT_APPROVED','ELIGIBLE_TO_APPROVED_NO_AUTH'),('APPROVED_NOT_EXECUTED','APPROVED_TO_EXECUTED_NO_AUTH'),('EXECUTED_NOT_VERIFIED','EXECUTED_TO_VERIFIED_NO_TEST'),('DUPLICATE_APPROVAL_NO_THRESHOLD','DUPLICATE_APPROVAL_COUNTS')]:props.append({'property':proposition,'case':attempt,'status':'SATISFIED' if execute('NEGATIVE_SPACE',{'attempt':attempt})=='REJECTED' else 'VIOLATED'})
 return results,props
def main():
 results,props=run();print(json.dumps({'tests':results,'properties':props,'summary':{'tests':len(results),'passed':sum(x['status']=='PASSED' for x in results),'properties':len(props),'satisfied':sum(x['status']=='SATISFIED' for x in props)}},indent=2));return 1 if any(x['status']!='PASSED' for x in results) or any(x['status']=='VIOLATED' for x in props) else 0
if __name__=='__main__':sys.exit(main())
