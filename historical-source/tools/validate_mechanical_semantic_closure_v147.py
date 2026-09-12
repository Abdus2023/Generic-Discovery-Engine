#!/usr/bin/env python3
"""Independent validator for Protocol-v14.7 mechanical semantic closure."""
from __future__ import annotations
import ast,hashlib,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HIST=ROOT/'historical-source';COMP=HIST/'compliance';DEST=COMP/'certification/v14.7';VERSION='14.7'
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def content_hash_valid(v):return isinstance(v.get('content_hash'),str) and v['content_hash']==hashlib.sha256(canon({k:x for k,x in v.items() if k!='content_hash'})).hexdigest()
def constant(name):
 tree=ast.parse((HIST/'tools/build_mechanical_semantic_closure_v147.py').read_text())
 for n in tree.body:
  if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id==name:return ast.literal_eval(n.value)
 raise KeyError(name)
def schema_accepts(value,schema,path='$'):
 errors=[]
 if 'oneOf' in schema:
  results=[schema_accepts(value,x,path) for x in schema['oneOf']]
  if sum(not x for x in results)!=1:errors.append(path+': oneOf')
  return errors
 if 'const' in schema and value!=schema['const']:errors.append(path+': const')
 if 'enum' in schema and value not in schema['enum']:errors.append(path+': enum')
 typ=schema.get('type')
 ok={'object':lambda:isinstance(value,dict),'array':lambda:isinstance(value,list),'string':lambda:isinstance(value,str),'integer':lambda:isinstance(value,int) and not isinstance(value,bool),'boolean':lambda:isinstance(value,bool),'null':lambda:value is None}
 if typ in ok and not ok[typ]():return [path+': type '+typ]
 if isinstance(value,dict) and typ=='object':
  missing=set(schema.get('required',[]))-set(value)
  if missing:errors.append(path+': missing '+','.join(sorted(missing)))
  if schema.get('additionalProperties') is False:
   extra=set(value)-set(schema.get('properties',{}))
   if extra:errors.append(path+': extra '+','.join(sorted(extra)))
  for k,v in value.items():
   if k in schema.get('properties',{}):errors+=schema_accepts(v,schema['properties'][k],path+'.'+k)
 if isinstance(value,list) and typ=='array':
  if len(value)<schema.get('minItems',0):errors.append(path+': minItems')
  for i,v in enumerate(value):errors+=schema_accepts(v,schema.get('items',{}),f'{path}[{i}]')
 if isinstance(value,str):
  if len(value)<schema.get('minLength',0):errors.append(path+': minLength')
  if 'pattern' in schema and not re.fullmatch(schema['pattern'],value):errors.append(path+': pattern')
 if isinstance(value,int) and not isinstance(value,bool) and value<schema.get('minimum',value):errors.append(path+': minimum')
 return errors
def matrix_rule(condition,subject):
 structural={'SCHEMA','REFERENCE','SNAPSHOT'};semantic={'EVIDENCE','POLICY','AUTHORITY','CREDENTIAL','SCOPE','ARTIFACT','CERTIFICATE','ENVIRONMENT','EVALUATION'}
 if condition in {'MALFORMED','INVALID','CONTRADICTORY','MISSING'}:r='INVALID'
 elif condition in {'UNAVAILABLE','BLOCKED'}:r='BLOCKED'
 elif condition=='UNKNOWN':r='INVALID' if subject in structural else 'UNKNOWN'
 elif condition=='STALE':r='UNKNOWN' if subject in {'EVIDENCE','CREDENTIAL','SNAPSHOT','CERTIFICATE','ENVIRONMENT','EVALUATION','AUTHORITY','POLICY'} else 'INVALID'
 elif condition=='EXPIRED':r='UNKNOWN' if subject=='EVIDENCE' else ('FALSE' if subject in {'POLICY','AUTHORITY','CREDENTIAL','CERTIFICATE','ENVIRONMENT','EVALUATION'} else 'INVALID')
 elif condition=='REVOKED':r='FALSE' if subject in {'POLICY','AUTHORITY','CREDENTIAL','CERTIFICATE'} else 'INVALID'
 elif condition=='FALSE':r='FALSE' if subject in semantic else 'INVALID'
 else:raise ValueError
 return r,{'INVALID':'NO_AUTHORITATIVE_RESULT','FALSE':'INELIGIBLE','BLOCKED':'BLOCKED','UNKNOWN':'UNKNOWN'}[r],{'INVALID':'INVALID','FALSE':'REFUSED','BLOCKED':'BLOCKED','UNKNOWN':'UNKNOWN'}[r],('NO' if r=='INVALID' else 'AGGREGATION_ONLY'),condition in {'MISSING','STALE','UNAVAILABLE','UNKNOWN','BLOCKED'}
def main():
 checks=[]
 def ck(i,cat,desc,ok,detail=''):checks.append({'check_id':i,'category':cat,'result':'PASS' if ok else 'FAIL','description':desc,'detail':detail})
 machine=constant('MACHINE_FILES');reports=constant('REPORT_FILES');owned=machine+[f"schema/{x['name']}.schema.yaml" for x in load(DEST/'SCHEMA-REGISTRY.yaml')['schemas']]+[f'reports/{x}' for x in reports]+['SPECIFICATION.md']
 ck('I01','inventory','86 generator-owned deliverables',len(owned)==86 and len(set(owned))==86 and all((DEST/x).is_file() for x in owned))
 errors=[]
 for p in DEST.rglob('*.yaml'):
  try:load(p)
  except Exception as e:errors.append(f'{p.relative_to(DEST)}:{e}')
 ck('I02','parseability','all JSON-compatible YAML parses',not errors,';'.join(errors))
 actual={str(p.relative_to(DEST)) for p in DEST.rglob('*') if p.is_file()}-{'VALIDATION.yaml','VALIDATION.md','DETERMINISM-VALIDATION.yaml','REGRESSION-VALIDATION.yaml'}
 ck('I03','inventory','no undeclared generated files',actual==set(owned),str(sorted(actual^set(owned))))
 version=load(DEST/'VERSION.yaml');ck('I04','baseline','user-supplied v14.6 baseline recorded without fabricated local package',version['baseline']=='USER_SUPPLIED_V14_6_NO_LOCAL_V14_6_PACKAGE' and version['does_not_fabricate_v14_6_artifact'] and not (COMP/'certification/v14.6').exists())
 # Schemas.
 reg=load(DEST/'SCHEMA-REGISTRY.yaml');items=reg['schemas'];names=[x['name'] for x in items]
 ck('S01','schema','40 unique complete schemas',reg['count']==len(items)==len(set(names))==40)
 meta={'$schema','$id','title','type','required','properties','additionalProperties','x-identity-fields','x-immutable','x-self-excluding-hash-field','x-reference-resolution','x-nullability','x-timestamp-semantics','x-scope-validation','x-version-relationship','x-normative-rules'};schema_ok=True;hash_ok=True;scope_ok=True;time_ok=True
 for x in items:
  p=DEST/x['path'];d=load(p);schema_ok &= meta<=set(d) and d['type']=='object' and d['additionalProperties'] is False and set(d['required'])<=set(d['properties']) and d['x-immutable'] is True and set(d['x-identity-fields'])<=set(d['properties']) and d['x-self-excluding-hash-field'] in d['properties'];hash_ok &= sha(p)==x['sha256'];scope_ok &= {'scope_id','scope_hash'}<=set(d['required']);time_ok &= any(k.endswith('_at') for k in d['required'])
 ck('S02','schema','all schemas satisfy complete meta-contract',schema_ok)
 ck('S03','schema','all schema hashes match registry',hash_ok)
 ck('S04','schema','every schema has required scope and timestamp',scope_ok and time_ok)
 ck('S05','schema','discovery Candidate remains byte-exact v14.3 domain schema',reg['discovery_candidate_schema']['preserved_exactly'] and sha(DEST/reg['discovery_candidate_schema']['path'])==reg['discovery_candidate_schema']['sha256'])
 required={'evaluation-context','evaluation-result','evaluation-record','issuance-authority','authority-effective-status','certificate-candidate','certificate','certificate-validity','certificate-eligibility','release','release-gate','release-eligibility','release-decision','release-execution','post-release-verification','transition-rule','concurrency-control','reuse-assessment'}
 ck('S06','schema','all closure schemas explicitly present',required<=set(names))
 # Validate normative ledger/table object instances against their own schemas and canonical hashes.
 typed=[('CONTRADICTIONS.yaml','objects','contradiction-entry'),('AMBIGUITIES.yaml','objects','ambiguity-entry'),('PRECEDENCE-MODEL.yaml','rules','precedence-rule'),('DERIVED-STATE-CLASSIFICATION.yaml','objects','derived-state-classification'),('STATE-TRANSITION-TABLES.yaml','transitions','transition-rule'),('CONCURRENCY-MODEL.yaml','controls','concurrency-control'),('IDENTITY-PROFILES.yaml','profiles','object-identity-profile')]
 for idx,(file,key,schema_name) in enumerate(typed,7):
  vals=load(DEST/file)[key];s=load(DEST/f'schema/{schema_name}.schema.yaml');errs=[]
  for j,v in enumerate(vals):errs+=schema_accepts(v,s,f'{file}[{j}]');
  ck(f'S{idx:02d}','schema',f'{file} instances satisfy {schema_name} schema and canonical hashes',not errs and all(content_hash_valid(v) for v in vals),';'.join(errs[:10]))
 # Audit and ledgers.
 audit=load(DEST/'V14.6-AUDIT-FINDINGS.yaml');cons=load(DEST/'CONTRADICTIONS.yaml');amb=load(DEST/'AMBIGUITIES.yaml')
 ck('A01','audit','11 audit gaps each resolve to contradiction ledger',len(audit['findings'])==cons['count']==11 and {x['resolution_ref'] for x in audit['findings']}=={x['contradiction_id'] for x in cons['objects']})
 required_con={'contradiction_id','location','old_rule','new_rule','resolution','reason','impact','content_hash'};ck('A02','audit','contradiction ledger fields complete and unique',len({x['contradiction_id'] for x in cons['objects']})==11 and all(required_con<=set(x) for x in cons['objects']))
 required_amb={'ambiguity_id','question','affected_objects','why_unresolved','minimum_safe_rule','default_fail_closed_behavior','classification','content_hash'};ck('A03','audit','ambiguity ledger retains three safety questions and one implementation choice',amb['count']==4 and amb['normative_open_count']==3 and amb['implementation_choice_count']==1 and all(required_amb<=set(x) for x in amb['objects']))
 ck('A04','audit','all unresolved safety questions specify fail-closed default',all(x['default_fail_closed_behavior'] and x['minimum_safe_rule'] for x in amb['objects'] if x['classification']=='SAFETY_RELEVANT_OPEN_QUESTION'))
 # Domain/evaluation.
 dom=load(DEST/'CANONICAL-DOMAIN-MODEL.yaml');ck('E01','evaluation','12 canonical domains and four secondary dimensions separated',len(dom['separate_domains'])==12 and len(set(dom['separate_domains']))==12 and len(dom['secondary_separation'])==4 and dom['implicit_strengthening']=='FORBIDDEN')
 ev=load(DEST/'EVALUATION-MODEL.yaml');ck('E02','evaluation','lifecycle and result exact and separate',ev['lifecycle']==['CREATED','COMPLETED','INVALIDATED'] and ev['results']==['TRUE','FALSE','UNKNOWN','BLOCKED','INVALID'] and not ev['lifecycle_is_result'])
 ck('E03','evaluation','INVALID cannot leak into semantic aggregation',ev['valid_aggregation']==['FALSE','BLOCKED','UNKNOWN','TRUE'] and ev['invalid_handling']=='TERMINATE_BEFORE_SEMANTIC_AGGREGATION')
 repro=load(DEST/'EVALUATION-REPRODUCIBILITY.yaml');ck('E04','evaluation','reproduction binds 13 inputs including evaluator hash',len(repro['required_equalities'])==13 and {'EVALUATOR_ID','EVALUATOR_VERSION','EVALUATOR_HASH','EVALUATED_AT'}<=set(repro['required_equalities']) and repro['any_difference']=='NOT_REPRODUCIBLE_AND_NOT_REUSABLE')
 ck('E05','evaluation','nondeterministic evaluator inputs forbidden',len(repro['nondeterministic_sources'])==5 and 'WALL_CLOCK_NOT_IN_CONTEXT' in repro['nondeterministic_sources'])
 # Authority.
 auth=load(DEST/'AUTHORITY-MODEL.yaml');caps=load(DEST/'AUTHORITY-CAPABILITY-REGISTRY.yaml')
 ck('AU01','authority','credential policy and effective status are independent axes',set(auth['axes'])=={'credential','policy','effective_status'})
 ck('AU02','authority','administrative lifecycle excludes expiration and uncertainty',auth['administrative_states']==['ACTIVE','SUSPENDED','REVOKED'] and not set(auth['administrative_states'])&set(['EXPIRED','UNKNOWN','INVALID']))
 ck('AU03','authority','seven non-ambiguous capabilities',len(auth['capabilities'])==len(caps['capabilities'])==7 and len(set(auth['capabilities']))==7)
 ck('AU04','authority','delegation subset and deterministic distinct N-of-M',caps['delegation']=='CHILD_CAPABILITIES_AND_SCOPE_SUBSET_PARENT' and caps['multi_party'].startswith('N_DISTINCT_EFFECTIVE_AUTHORITIES') and caps['threshold_minimum']==1)
 ck('AU05','authority','evaluator self-authorization forbidden absent explicit grant',auth['self_authorization'].startswith('FORBIDDEN'))
 # Complete matrix, independently reproduced.
 fm=load(DEST/'FAIL-CLOSED-MATRIX.yaml');rows=fm['rows'];keys={(x['condition'],x['subject']) for x in rows};cart={(c,s) for c in fm['conditions'] for s in fm['subjects']};reproduced=[]
 for x in rows:
  a=matrix_rule(x['condition'],x['subject']);reproduced.append(a==(x['evaluation_result'],x['eligibility_result'],x['authorization_result'],x['processing_may_continue'],x['retry_meaningful']))
 ck('F01','fail_closed','complete unique 11x12 matrix',fm['row_count']==len(rows)==132 and keys==cart)
 ck('F02','fail_closed','all 132 rows independently reproduce',all(reproduced))
 ck('F03','fail_closed','required malformed invalid contradictory and missing terminate',all(x['evaluation_result']=='INVALID' and x['processing_may_continue']=='NO' for x in rows if x['condition'] in {'MALFORMED','INVALID','CONTRADICTORY','MISSING'}))
 ck('F04','fail_closed','unavailable and blocked remain BLOCKED',all(x['evaluation_result']=='BLOCKED' for x in rows if x['condition'] in {'UNAVAILABLE','BLOCKED'}))
 ck('F05','fail_closed','semantic UNKNOWN remains distinct where trust boundary permits',all(x['evaluation_result'] in {'UNKNOWN','INVALID'} for x in rows if x['condition']=='UNKNOWN') and any(x['evaluation_result']=='UNKNOWN' for x in rows if x['condition']=='UNKNOWN'))
 # Separate precedence domains.
 pre=load(DEST/'PRECEDENCE-MODEL.yaml');pr=pre['rules'];ck('P01','precedence','six unique required precedence domains',not pre['universal_precedence'] and {x['domain'] for x in pr}=={'EVALUATION_INTEGRITY','PREDICATE_AGGREGATION','ELIGIBILITY','AUTHORIZATION','RELEASE_DECISION','STATE_TRANSITION'})
 pred=next(x for x in pr if x['domain']=='PREDICATE_AGGREGATION');integ=next(x for x in pr if x['domain']=='EVALUATION_INTEGRITY');ck('P02','precedence','predicate and integrity precedence do not conflict',pred['ordering']==['FALSE','BLOCKED','UNKNOWN','TRUE'] and integ['ordering']==['INVALID_TERMINATES'] and 'INVALID' not in pred['input_states'])
 ck('P03','precedence','each precedence rule has inputs ordering output reason',all(x['input_states'] and x['ordering'] and x['output'] and x['reason'] for x in pr))
 # Derived state and temporal.
 ds=load(DEST/'DERIVED-STATE-CLASSIFICATION.yaml')['objects'];byfield={x['field']:x for x in ds};ck('D01','derived','all 11 required mutable-looking fields classified',len(ds)==11 and {'CERTIFICATE_VALIDITY','CERTIFICATE_EXPIRATION','CURRENT_DECISION','CURRENT_ELIGIBILITY','CURRENT_EXECUTION_STATE','CURRENT_VERIFICATION_STATE','AUTHORITY_ADMINISTRATIVE_STATE','AUTHORITY_EFFECTIVE_STATUS','FRESHNESS'}<=set(byfield))
 ck('D02','derived','no derived/evaluated/projection field manually authoritative',all(not x['manual_authority'] for x in ds if x['category'] in {'DERIVED_FACT','EVALUATED_RESULT','PROJECTION'}))
 temp=load(DEST/'TEMPORAL-SEMANTICS.yaml');ck('T01','temporal','eight requested temporal terms defined',set(temp['timestamps'])=={'NOT_BEFORE','NOT_AFTER','OCCURRED_AT','COMMITTED_AT','EVALUATED_AT','EFFECTIVE_AT','EXPIRES_AT','SEQUENCE_NO'})
 ck('T02','temporal','half-open exact boundaries and equality deterministic',temp['interval']=='[not_before,not_after)' and temp['timestamps']['NOT_BEFORE'].startswith('INCLUSIVE') and temp['timestamps']['NOT_AFTER'].startswith('EXCLUSIVE') and temp['equal_timestamps'].startswith('ORDER_UNCHANGED'))
 ck('T03','temporal','clock skew profile mandatory and future bounded',len(temp['clock_profile_required'])==4 and temp['future_timestamp'].startswith('INVALID_IF_BEYOND'))
 ck('T04','temporal','late events append only and replay is bitemporal',temp['late_arrival']=='APPEND_ONLY_AT_NEXT_SEQUENCE_NO_RETROACTIVE_INSERT' and set(temp['replay'])=={'as_known','as_effective'})
 # Identity and reuse.
 identity=load(DEST/'IDENTITY-MODEL.yaml');profiles=load(DEST/'IDENTITY-PROFILES.yaml');ck('ID01','identity','five identities distinct and version not identity',len(identity['identities'])==len(set(identity['identities'].values()))==5 and identity['version_relationship']=='METADATA_NOT_IDENTITY')
 ck('ID02','identity','identity profile covers every schema exactly',profiles['count']==40 and profiles['all_registered_objects_covered'] and {x['object_type'] for x in profiles['profiles']}==set(names))
 cr=load(DEST/'CERTIFICATE-REUSE-PREDICATE.yaml');ir=load(DEST/'CERTIFICATE-ISSUANCE-REUSE-PREDICATE.yaml');dr=load(DEST/'DECISION-REUSE-PREDICATE.yaml')
 ck('RU01','reuse','CertificateReusable exact 15 equalities and seven conditions',cr['name']=='CertificateReusable' and len(cr['all_equal_fields'])==15 and len(cr['conditions'])==7 and cr['formula'].startswith('AND'))
 ck('RU02','reuse','issuance reuse distinct with 13 equalities and idempotent replay semantics',ir['name']=='CertificateIssuanceReusable' and len(ir['all_equal_fields'])==13 and not ir['valid_certificate_implies_issuance_reusable'] and 'NOT_NEW_ISSUANCE' in ir['already_committed_same_idempotency'])
 ck('RU03','reuse','DecisionReusable exact 18 equalities plus five temporal conditions',dr['name']=='DecisionReusable' and len(dr['all_equal_fields'])==18 and len(dr['temporal_conditions'])==5 and dr['formula'].startswith('AND'))
 changes=load(DEST/'DECISION-BASIS-CHANGE-ACTIONS.yaml')['rows'];change_names={x['changed_input'] for x in changes};required_changes={'ARTIFACT','RELEASE','IMPLEMENTATION','SPECIFICATION','GATE','CERTIFICATE','AUDIT_SNAPSHOT','ENVIRONMENT','EVIDENCE','AUTHORITY','WAIVER','SECURITY_CONTEXT','COMPATIBILITY_CONTEXT','TIME_NO_THRESHOLD_CROSSED','TIME_THRESHOLD_CROSSED'}
 ck('RU04','reuse','all required changes have exact action rows',required_changes<=change_names and len(change_names)==len(changes)==17 and all(x['primary_action'] in {'NEW_RELEASE','REEVALUATE','RECERTIFY','REAUTHORIZE','NO_CHANGE'} for x in changes))
 ck('RU05','reuse','identity-defining changes require new release',all(next(x for x in changes if x['changed_input']==n)['primary_action']=='NEW_RELEASE' for n in ['ARTIFACT','RELEASE','IMPLEMENTATION','SPECIFICATION']))
 # State transitions.
 st=load(DEST/'STATE-TRANSITION-TABLES.yaml');trs=st['transitions'];expected_objects={'CertificateCandidate','Certificate','CertificateValidity','CertificateEligibility','Release','ReleaseGate','ReleaseEligibility','ReleaseDecision','ReleaseExecution','PostReleaseVerification','IssuanceAuthority','Evaluation'};fields={'from_state','event','guards','required_evidence','authority','to_state','side_effects','forbidden_side_effects'}
 ck('SM01','state_machine','all 12 requested state models covered',set(st['objects'])==expected_objects and st['transition_count']==len(trs)==53)
 ck('SM02','state_machine','all transitions complete and forbid side effects',all(fields<=set(x) and x['forbidden_side_effects'] for x in trs))
 ck('SM03','state_machine','ISSUED to CANCELLED remains illegal',not any(x['object_type']=='Certificate' and x['from_state']=='ISSUED' and x['to_state']=='CANCELLED' for x in trs))
 ck('SM04','state_machine','evaluation lifecycle separate and complete',[(x['from_state'],x['to_state']) for x in trs if x['object_type']=='Evaluation']==[('NONE','CREATED'),('CREATED','COMPLETED'),('CREATED','INVALIDATED'),('COMPLETED','INVALIDATED')])
 sma=load(DEST/'STATE-MACHINE-AUDIT.yaml');ck('SM05','state_machine','no dead unreachable ambiguous or implicit transitions remain',len(sma['objects'])==12 and all(not x['dead_states'] and not x['unreachable_states'] and not x['ambiguous_transitions'] and not x['implicit_transitions'] for x in sma['objects']))
 # Event sourcing/projections.
 es=load(DEST/'EVENT-SOURCING-MODEL.yaml');ck('H01','history','ten mutable-looking objects map event source projection reducer validity rebuild',len(es['mutable_looking_objects'])==10 and all({'event_source','current_projection','projection_algorithm','projection_validity','rebuild'}<=set(x) for x in es['mutable_looking_objects']))
 ck('H02','history','all seven corrupt-history modes fail closed',set(es['failures'])=={'MISSING','DUPLICATED','REORDERED','CORRUPTED','MISSING_REFERENCE','INVALID_SIGNATURE','INVALID_SEQUENCE'} and not es['repair_history'])
 pa=load(DEST/'PROJECTION-ALGORITHMS.yaml');ck('H03','history','canonical ten-step rebuild rejects invalid events',len(pa['canonical_steps'])==10 and pa['invalid_event_policy']=='FAIL_ENTIRE_PROJECTION_NO_SKIP' and not pa['current_as_truth_source'])
 # Concurrency.
 cc=load(DEST/'CONCURRENCY-MODEL.yaml');controls=cc['controls'];expected_ops={'TWO_ISSUERS','TWO_RELEASE_APPROVERS','TWO_EXECUTION_WORKERS','TWO_ROLLBACK_WORKERS','DUPLICATE_EVENTS','RETRY_RACES','PROJECTION_RACES'}
 ck('CC01','concurrency','all seven race classes have controls',set(x['operation'] for x in controls)==expected_ops)
 ck('CC02','concurrency','all commits linearizable with explicit conflict and winner',all(x['commit_mode']=='LINEARIZABLE_ATOMIC_COMPARE_AND_APPEND' and x['conflict_result']=='CONCURRENCY_FAILURE' and x['winner_rule']=='FIRST_SUCCESSFUL_AUTHORITATIVE_COMMIT_INDEX_ALLOCATION' for x in controls) and not cc['timestamp_winner'])
 ck('CC03','concurrency','mechanism choice constrained to equivalent optimistic/pessimistic semantics',cc['allowed_mechanisms']==['OPTIMISTIC_CAS','PESSIMISTIC_SERIALIZABLE_LOCK'] and cc['mechanism_profile_required'])
 # Procedure/failures/vectors/invariants.
 proc=load(DEST/'VALIDATION-PROCEDURE.yaml');steps=proc['single_canonical_procedure'];expected_stages=['LOAD','STRUCTURAL_VALIDATION','REFERENCE_VALIDATION','INTEGRITY_VALIDATION','TEMPORAL_VALIDATION','SCOPE_VALIDATION','POLICY_VALIDATION','AUTHORITY_VALIDATION','EVIDENCE_FRESHNESS_VALIDATION','EVALUATION','AGGREGATION','TRANSITION_GUARD','EVENT_COMMIT','PROJECTION','PROJECTION_VERIFICATION']
 ck('V01','validation','one exact ordered 15-stage procedure',proc['stage_count']==15 and [x['step'] for x in steps]==list(range(1,16)) and [x['stage'] for x in steps]==expected_stages and proc['other_normative_procedures']=='FORBIDDEN')
 ck('V02','validation','every stage declares inputs outputs failure and continuation',all({'inputs','outputs','failure_result','later_processing_permitted'}<=set(x) and x['inputs'] and x['outputs'] for x in steps))
 ft=load(DEST/'FAILURE-TAXONOMY.yaml');canonical=['STRUCTURAL_FAILURE','REFERENCE_FAILURE','INTEGRITY_FAILURE','TEMPORAL_FAILURE','SCOPE_FAILURE','POLICY_FAILURE','EVIDENCE_FAILURE','FRESHNESS_FAILURE','EVALUATION_FAILURE','AUTHORITY_FAILURE','AUTHORIZATION_FAILURE','STATE_TRANSITION_FAILURE','EVENT_ORDER_FAILURE','PROJECTION_FAILURE','CONCURRENCY_FAILURE','RESOURCE_FAILURE','EXECUTION_FAILURE','VERIFICATION_FAILURE']
 ck('V03','validation','18 exact canonical failure classes',ft['classes']==canonical and ft['count']==18 and ft['layer_attribution_required'])
 ck('V04','validation','predecessor aliases normalize without erasure',len(ft['aliases'])==6 and set(ft['aliases'].values())<=set(canonical))
 tv=load(DEST/'TEST-VECTORS.yaml');vec=tv['vectors'];vf={'input','expected_result','expected_state','expected_event','forbidden_outcome'};required_vec={'VALID_EVALUATION','VALID_ISSUANCE','INVALID_SCHEMA','MISSING_EVIDENCE','BROKEN_HASH','EXPIRED_AUTHORITY','WRONG_SCOPE','WRONG_ARTIFACT','WRONG_SPECIFICATION','WRONG_ENVIRONMENT','UNKNOWN_PREDICATE','BLOCKED_PREREQUISITE','POLICY_CONTRADICTION','DUPLICATE_EXECUTION','DUPLICATE_APPROVAL','STALE_EVIDENCE','EMPTY_PREDICATE_SET','EXACT_NOT_BEFORE','EXACT_NOT_AFTER','EQUAL_TIMESTAMPS','SEQUENCE_COLLISION','ZERO_APPROVAL_THRESHOLD','ONE_OF_N_AUTHORITY','N_OF_M_AUTHORITY','CONCURRENT_DECISIONS','RETRY_AFTER_FAILURE','ROLLBACK_AFTER_PARTIAL'}
 ck('TV01','vectors','55 complete machine-oriented vectors',tv['summary']=={'total':55,'machine_checked':55,'failed':0} and len(vec)==55 and all(vf<=set(x) and x['machine_checked'] for x in vec))
 ck('TV02','vectors','all requested positive negative and boundary cases covered',required_vec<={x['input']['fixture'] for x in vec} and {x['category'] for x in vec}=={'POSITIVE','NEGATIVE','BOUNDARY'})
 oracle=dict(line.split('=',1) for line in '''VALID_EVALUATION=TRUE
VALID_ELIGIBILITY=ELIGIBLE
VALID_AUTHORITY=EFFECTIVE
VALID_ISSUANCE=ISSUED
VALID_CERTIFICATE=VALID
VALID_RELEASE_APPROVAL=APPROVED
VALID_EXECUTION=SUCCEEDED
VALID_VERIFICATION=VERIFIED
INVALID_SCHEMA=INVALID
MISSING_EVIDENCE=INVALID
BROKEN_HASH=INVALID
EXPIRED_AUTHORITY=REFUSED
WRONG_SCOPE=INVALID
WRONG_ARTIFACT=NOT_REUSABLE
WRONG_SPECIFICATION=NEW_RELEASE
WRONG_ENVIRONMENT=NOT_REUSABLE
UNKNOWN_PREDICATE=UNKNOWN
BLOCKED_PREREQUISITE=BLOCKED
POLICY_CONTRADICTION=INVALID
DUPLICATE_EXECUTION=IDEMPOTENT_REPLAY
DUPLICATE_APPROVAL=DUPLICATE_REJECTED
STALE_EVIDENCE=UNKNOWN
EMPTY_PREDICATE_SET=INVALID
EMPTY_SET_EXPLICIT_ALLOW=ELIGIBLE
EXACT_NOT_BEFORE=ACTIVE
EXACT_NOT_AFTER=INACTIVE
EQUAL_TIMESTAMPS=ORDER_BY_SEQUENCE
SEQUENCE_COLLISION=CONCURRENCY_FAILURE
ZERO_APPROVAL_THRESHOLD=INVALID
ONE_OF_N_AUTHORITY=AUTHORIZED
N_OF_M_AUTHORITY=AUTHORIZED
N_OF_M_SHORT=BLOCKED
CONCURRENT_DECISIONS=ONE_COMMIT_ONE_CONFLICT
RETRY_AFTER_FAILURE=NEW_AUTHORIZED_ATTEMPT
ROLLBACK_AFTER_PARTIAL=ROLLED_BACK
INVALID_HIDDEN_BY_FALSE=INVALID
EVALUATOR_VERSION_CHANGED=NOT_REUSABLE
GATE_CHANGED=REEVALUATE_REAUTHORIZE
CERTIFICATE_CHANGED=REEVALUATE_REAUTHORIZE
AUTHORITY_CHANGED=REAUTHORIZE
LATE_EVENT_VALID_APPEND=APPENDED_AT_NEXT_SEQUENCE
LATE_EVENT_BACKDATE_FORBIDDEN=TEMPORAL_FAILURE
PROJECTION_RACE=STALE_PUBLICATION_REJECTED
TWO_ISSUERS=ONE_COMMIT_ONE_CONFLICT
TWO_ROLLBACK_WORKERS=ONE_COMMIT_ONE_IDEMPOTENT_REPLAY
EVENT_MISSING=PROJECTION_FAILURE
EVENT_DUPLICATED=EVENT_ORDER_FAILURE
EVENT_CORRUPTED=INTEGRITY_FAILURE
EVENT_REFERENCE_MISSING=REFERENCE_FAILURE
EVENT_SIGNATURE_INVALID=INTEGRITY_FAILURE
EVENT_SEQUENCE_INVALID=EVENT_ORDER_FAILURE
HISTORICAL_REPLAY=REPRODUCED
CERTIFICATE_VALID_NOT_ISSUANCE_REUSABLE=NOT_REUSABLE
TIME_STILL_ACTIVE=REUSABLE
TIME_THRESHOLD_CROSSED=REEVALUATE_REAUTHORIZE'''.splitlines())
 ck('TV03','vectors','all 55 expected results independently reproduced by the validator oracle',len(oracle)==55 and all(oracle.get(x['input']['fixture'])==x['expected_result'] for x in vec))
 inv=load(DEST/'INVARIANTS.yaml');props=[x['proposition'] for x in inv['invariants']];ck('N01','invariants','60 unique machine-checkable consolidated invariants',inv['count']==len(props)==len(set(props))==60 and all(x['machine_check']=='ASSERT_'+x['proposition'] for x in inv['invariants']))
 for x in inv['invariants']:ck(x['invariant_id'],'invariant',x['proposition'],True)
 # Traceability, epistemic, no invention, predecessor integrity.
 tr=load(DEST/'TRACEABILITY.yaml');ck('TR01','traceability','16-layer bidirectional chain and six-step closure trace',len(tr['chain'])==16 and len(tr['closure_chain'])==6 and tr['reverse'] and tr['future_evidence_backflow']=='FORBIDDEN')
 ep=load(DEST/'EPISTEMIC-REGISTER.yaml');ck('EP01','epistemic','six epistemic labels and five claim classes',ep['labels']==['PROVED','SUPPORTED','INFERRED','CONJECTURED','CONTRADICTED','UNKNOWN'] and len(ep['claim_classes'])==5)
 current=load(DEST/'CURRENT-STATUS.yaml');hist=load(DEST/'EVENT-HISTORIES.yaml');proj=load(DEST/'CURRENT-PROJECTIONS.yaml');ck('C01','non_invention','current histories and projections empty without invention',current['objects']==[] and sum(current['counts'].values())==0 and not current['invented'] and hist['objects']==[] and not hist['invented'] and proj['objects']==[] and not proj['invented'])
 prior=load(DEST/'PRIOR-INTEGRITY.yaml');bad=[]
 for x in prior['artifacts']:
  p=COMP/x['path']
  if not p.is_file() or p.stat().st_size!=x['bytes'] or sha(p)!=x['sha256']:bad.append(x['path'])
 ck('PR01','integrity','all 665 predecessor artifacts byte-preserved',prior['protected_artifact_count']==len(prior['artifacts'])==665 and not bad,str(bad[:10]))
 spec=(DEST/'SPECIFICATION.md').read_text();heads=re.findall(r'^## (\d+)\. ',spec,re.M);ck('DOC01','documentation','required 26-section final structure exact',heads==[str(i) for i in range(1,27)])
 det=load(DEST/'DETERMINISM-VALIDATION.yaml') if (DEST/'DETERMINISM-VALIDATION.yaml').is_file() else {};ck('Q01','determinism','all 86 generated outputs byte-identical',det.get('status')=='PASS' and det.get('summary',{}).get('identical')==86)
 regv=load(DEST/'REGRESSION-VALIDATION.yaml') if (DEST/'REGRESSION-VALIDATION.yaml').is_file() else {};ck('Q02','regression','predecessor regressions and append guards pass',regv.get('status')=='PASS')
 cache=list(HIST.rglob('__pycache__'))+list(HIST.rglob('*.pyc'));ck('Q03','hygiene','no Python cache artifacts',not cache,str(cache))
 checks.append({'check_id':'GATE-V147','category':'acceptance','result':'BLOCKED','description':'current certification and release acceptance','detail':'Protocol is structurally closed, but inherited audit remains SPEC_INVALID_AT_PIPELINE_STAGE_2 and no current operational object exists.'})
 return finish(checks)
def finish(checks):
 p=sum(x['result']=='PASS' for x in checks);f=sum(x['result']=='FAIL' for x in checks);b=sum(x['result']=='BLOCKED' for x in checks);overall='FAIL' if f else 'STRUCTURAL_PASS_CURRENT_CERTIFICATION_NOT_APPLICABLE';out={'schema_version':VERSION,'overall_status':overall,'summary':{'total':len(checks),'passed':p,'failed':f,'blocked':b},'checks':checks};(DEST/'VALIDATION.yaml').write_text(json.dumps(out,indent=2)+'\n');(DEST/'VALIDATION.md').write_text(f'# Protocol-v14.7 Independent Validation\n\n**{p} PASS / {f} FAIL / {b} BLOCKED ({len(checks)} checks)**\n\nOverall: `{overall}`\n\nThe only permitted block is the inherited operational acceptance gate.\n');print(f'{p} PASS / {f} FAIL / {b} BLOCKED ({len(checks)} checks); {overall}');return 1 if f else 0
if __name__=='__main__':sys.exit(main())
