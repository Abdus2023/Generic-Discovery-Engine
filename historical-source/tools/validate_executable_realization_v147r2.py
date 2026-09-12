#!/usr/bin/env python3
"""Independent v14.7-R2 realization/profile validator."""
import ast,hashlib,json,re,sys
from pathlib import Path
R=Path(__file__).resolve().parents[2];H=R/'historical-source';C=H/'compliance';D=C/'certification/v14.7-R2';sys.path.insert(0,str(H/'tools'))
from run_v147r2_conformance import run
from v147r2_conformance_harness import canonical_bytes,content_hash,PROFILE_ID
V='14.7-R2'
def ld(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def const(n):
 t=ast.parse((H/'tools/build_executable_realization_v147r2.py').read_text())
 for x in t.body:
  if isinstance(x,ast.Assign) and isinstance(x.targets[0],ast.Name) and x.targets[0].id==n:return ast.literal_eval(x.value)
 raise KeyError(n)
def main():
 z=[]
 def ck(i,c,d,o,x=''):z.append({'check_id':i,'category':c,'result':'PASS' if o else 'FAIL','description':d,'detail':x})
 files=const('FILES');schemas=const('SCHEMAS');owned=files+[f'schema/{x}.schema.yaml' for x in schemas]+['SPECIFICATION.md'];ck('I01','inventory','45 generator-owned artifacts',len(owned)==45 and all((D/x).is_file() for x in owned))
 errs=[]
 for p in D.rglob('*.yaml'):
  try:ld(p)
  except Exception as e:errs.append(f'{p}:{e}')
 ck('I02','parse','all YAML parses',not errs,';'.join(errs));actual={str(p.relative_to(D)) for p in D.rglob('*') if p.is_file()}-{'VALIDATION.yaml','VALIDATION.md','DETERMINISM-VALIDATION.yaml','REGRESSION-VALIDATION.yaml'};ck('I03','inventory','no undeclared generator artifact',actual==set(owned),str(sorted(actual^set(owned))))
 v=ld(D/'VERSION.yaml');ex=ld(D/'EXECUTIVE-RESULT.yaml');ck('B01','scope','R2 is realization profile not v14.8 semantic revision',v['semantic_version']=='v14.7' and not v['new_semantic_revision'] and not ex['v14_8_created'] and ex['specification']=='FROZEN')
 ck('B02','scope','audit found no semantic contradiction',not ex['semantic_defect_found'] and ld(D/'SEMANTIC-CONTRADICTIONS.yaml')['objects']==[])
 reg=ld(D/'SCHEMA-REGISTRY.yaml');ck('S01','schema','8 profile schemas extend hash-bound effective 49 predecessor schemas',len(reg['local'])==8 and reg['predecessor_effective_registry']['effective_count']==49 and reg['effective_count']==57 and sha(D/reg['predecessor_effective_registry']['path'])==reg['predecessor_effective_registry']['sha256'])
 meta={'$schema','$id','title','type','required','properties','additionalProperties','x-identity-fields','x-immutable','x-self-excluding-hash-field','x-canonical-profile','x-normative-rules'};ok=True
 for x in reg['local']:
  s=ld(D/x['path']);ok &= sha(D/x['path'])==x['sha256'] and meta<=set(s) and s['type']=='object' and s['additionalProperties'] is False and set(s['required'])<=set(s['properties']) and s['x-immutable'] and set(s['x-identity-fields'])<=set(s['properties']) and 'content_hash' in s['required']
 ck('S02','schema','all profile schemas complete, immutable and hash-bound',ok)
 audit=ld(D/'SCHEMA-AUDIT.yaml');ck('S03','schema','all 13 mandatory normative objects resolve without gaps',len(audit['required_objects'])==13 and audit['missing']==[] and audit['inheritance_mechanism'].startswith('R2_LOCAL'))
 profile=ld(D/'CANONICAL-SERIALIZATION-PROFILE.yaml');ck('C01','serialization','profile object matches exact schema vocabulary',set(profile)==set(ld(D/'schema/serialization-profile.schema.yaml')['properties']))
 ck('C02','serialization','canonical profile identity and own typed hash valid',profile['profile_id']==PROFILE_ID and profile['encoding']=='UTF-8' and profile['unicode_normalization'].startswith('NFC') and profile['content_hash']==content_hash('SERIALIZATION_PROFILE',{k:x for k,x in profile.items() if k!='content_hash'}))
 ck('C03','serialization','map order and NFC produce identical bytes',canonical_bytes({'b':2,'a':'e\u0301'})==canonical_bytes({'a':'é','b':2}))
 try:canonical_bytes({'float':1.2});float_rejected=False
 except ValueError:float_rejected=True
 ck('C04','serialization','floating point rejected by constrained number profile',float_rejected)
 hashes=ld(D/'HASH-DOMAIN-SPECIFICATION.yaml')['rows'];ck('H01','hash','seven exact typed hash domains',len(hashes)==7 and {x['field_name'] for x in hashes}=={'artifact_hash','object_hash','snapshot_hash','evaluation_hash','decision_basis_hash','event_hash','certificate_hash'})
 ck('H02','hash','every hash fixes input canonicalization algorithm encoding scope purpose',all({'input_domain','canonicalization','algorithm','encoding','scope','purpose'}<=set(x) and x['algorithm']=='SHA-256' and x['encoding']=='LOWERCASE_HEX_64' for x in hashes))
 ck('H03','hash','domain prefixes prevent cross-domain substitution',content_hash('OBJECT',{'x':1})!=content_hash('EVENT',{'x':1}))
 refs=ld(D/'REFERENCE-RESOLUTION-CONTRACT.yaml');ck('R01','reference','typed reference contract has eight fields and exact-one resolution',len(refs['fields'])==8 and refs['rule']=='EXACTLY_ONE_MATCHING_TARGET' and refs['failure_not_false'])
 ck('R02','reference','all eight reference failure/semantic cases explicit',len(refs['tests'])==8 and {'MISSING','WRONG_TYPE','WRONG_SCOPE','WRONG_VERSION','CIRCULAR_DEFAULT_REJECT','DUPLICATE_ID_REJECT'}<=set(refs['tests']))
 interfaces=ld(D/'VALIDATION-INTERFACE-CONTRACT.yaml');objects=interfaces['objects'];ck('V01','interfaces','all 16 required harness interfaces complete',interfaces['count']==len(objects)==16 and all({'input_contract','output_contract','failure_contract','side_effect_contract','determinism'}<=set(x) for x in objects))
 ck('V02','interfaces','validators side-effect-free except atomic event commit',all(x['side_effect_contract']=='NONE' for x in objects if x['name']!='commit_event') and next(x for x in objects if x['name']=='commit_event')['side_effect_contract']=='ATOMIC_EVENT_APPEND_ONLY')
 expected_names={'validate_structure','validate_references','validate_integrity','validate_temporal_scope','validate_scope','validate_policy','validate_authority','validate_evidence','evaluate','aggregate','guard_transition','commit_event','project','verify_projection','check_reuse','report_conformance'};ck('V03','interfaces','interface names exact',set(x['name'] for x in objects)==expected_names)
 evaluation=ld(D/'EVALUATION-CONTRACT.yaml');ck('E01','evaluation','Evaluate binds seven deterministic inputs',evaluation['function'].startswith('Evaluate(') and evaluation['equal_inputs_equal_result'] and len(evaluation['bound'])==7 and evaluation['external_nondeterminism'].startswith('MUST_BECOME'))
 authority=ld(D/'AUTHORITY-CONTRACT.yaml');ck('A01','authority','qualification signature, set containment and duplicate rejection explicit',authority['function'].startswith('QualifyAuthority(') and authority['set_containment'] and not authority['duplicate_authority_count'] and len(authority['approval_identity'])==5)
 sm=ld(D/'STATE-MACHINE-CONTRACT.yaml');trs=ld(D/'TRANSITIONS.yaml')['objects'];ck('T01','transitions','all 53 frozen transitions have executable tuple definitions',len(trs)==53 and all(set(sm['tuple_fields'])=={'TRANSITION_ID','OBJECT_TYPE','FROM_STATE','EVENT_TYPE','GUARD_EXPRESSION','REQUIRED_EVIDENCE','REQUIRED_AUTHORITY','TO_STATE','SIDE_EFFECTS','FORBIDDEN_SIDE_EFFECTS'} for _ in [0]))
 required_transition={'transition_id','object_type','from_state','event_type','guard_expression','required_evidence','required_authority_operation','required_authority_type','to_state','side_effects','forbidden_side_effects','semantic_override_profile','content_hash'};ck('T02','transitions','every transition complete, guarded, immutable and correction-bound',all(required_transition<=set(x) and x['guard_expression'] and x['forbidden_side_effects'] and x['semantic_override_profile']=='v14.7.1/TRANSITION-CORRECTIONS.yaml' and x['content_hash']==content_hash('TRANSITION_DEFINITION',{k:v for k,v in x.items() if k!='content_hash'}) for x in trs))
 es=ld(D/'EVENT-STORE-CONTRACT.yaml');ck('ES01','event_store','five interfaces and four mandatory guarantees',es['interfaces']==['append_event','read_stream','read_events','read_checkpoint','verify_stream'] and len(es['guarantees'])==4 and es['untrusted_if_missing_guarantee'])
 projection=ld(D/'PROJECTION-CONTRACT.yaml');ck('P01','projection','Project deterministic and fail-closed for eight history faults',projection['function']=='Project(history,profile)' and projection['deterministic'] and len(projection['fail_closed'])==8 and not projection['mutation_of_history'])
 reuse=ld(D/'REUSE-CONTRACT.yaml');ck('U01','reuse','three canonical predicates with invalid missing and changed handling',reuse['predicates']==['CertificateReusable','CertificateIssuanceReusable','DecisionReusable'] and reuse['missing_comparison']=='INVALID' and reuse['changed_comparison']=='NOT_REUSABLE')
 concurrency=ld(D/'CONCURRENCY-CONTRACT.yaml');ck('CC01','concurrency','all seven races and six required behaviors defined',len(concurrency['races'])==7 and concurrency['serialization']=='ATOMIC_COMPARE_AND_APPEND' and concurrency['winner']=='FIRST_DURABLE_COMMIT_INDEX' and not concurrency['process_mutex_sufficient'])
 harness=ld(D/'CONFORMANCE-HARNESS.yaml');classes={'SchemaValidator','ReferenceValidator','IntegrityValidator','TemporalValidator','ScopeValidator','PolicyValidator','AuthorityValidator','EvidenceValidator','Evaluator','Aggregator','TransitionGuard','EventStore','Projector','ProjectionVerifier','ReuseChecker','ConformanceReporter'};ck('CH01','harness','all 16 components executable without human interpretation',set(harness['components'])==classes and not harness['human_interpretation_required'])
 # Independently execute all oracles and generated properties.
 results,props=run(D);stored=ld(D/'TEST-RESULTS.yaml');stored_props=ld(D/'PROPERTY-RESULTS.yaml');ck('O01','oracles','71 machine oracles execute and match stored results',len(results)==71 and results==stored['objects'] and all(x['status']=='PASSED' for x in results))
 oracles=ld(D/'TEST-ORACLES.yaml')['objects'];fields={'oracle_id','operation','input_refs','expected_result','expected_state','expected_event','forbidden_results','determinism','content_hash'};ck('O02','oracles','every oracle fulfills immutable oracle contract and typed hash',len(oracles)==71 and all(fields<=set(x) and x['determinism']['required'] and x['content_hash']==content_hash('TEST_ORACLE',{k:v for k,v in x.items() if k!='content_hash'}) for x in oracles))
 ck('O03','oracles','failure origin vocabulary separates implementation oracle harness environment specification',set(harness['failure_origins'])=={'IMPLEMENTATION_FAILURE','ORACLE_FAILURE','TEST_HARNESS_FAILURE','ENVIRONMENT_FAILURE','SPECIFICATION_FAILURE'})
 ck('PB01','properties','170 generated properties rerun identically with one explicitly unknown durability claim',len(props)==170 and props==stored_props['objects'] and sum(x['status']=='SATISFIED' for x in props)==169 and sum(x['status']=='UNKNOWN' for x in props)==1 and not any(x['status']=='VIOLATED' for x in props))
 pm=ld(D/'PROPERTY-TEST-MODEL.yaml');ck('PB02','properties','finite proof scope and universal correctness limitation explicit',pm['generated_domains']['AGGREGATION']=='5^3_EXHAUSTIVE' and pm['universal_claim_limit'].endswith('SUPPORTED_ONLY'))
 neg=ld(D/'NEGATIVE-SPACE-TESTS.yaml');ck('N01','negative_space','all 11 forbidden transitions rejected',len(neg['attempts'])==11 and all(next(x for x in results if x['oracle_id']=='oracle:'+a)['actual']=='REJECTED' for a in neg['attempts']))
 report=ld(D/'CONFORMANCE-REPORT.yaml');ck('CR01','report','immutable report counts exact and durability remains explicitly unverified',report['result']=='UNVERIFIED' and report['tests']=={'total':71,'passed':71,'failed':0,'blocked':0,'invalid':0,'unknown':0} and report['invariants']=={'total':170,'satisfied':169,'violated':0,'unknown':1})
 ck('CR02','report','report content hash valid and claim scoped to reference harness',report['content_hash']==content_hash('CONFORMANCE_REPORT',{k:v for k,v in report.items() if k!='content_hash'}) and report['implementation']['implementation_id']=='v147r2-python-reference-harness')
 boundary=ld(D/'IMPLEMENTATION-PROFILE-BOUNDARY.yaml');ck('B03','boundary','normative profile and implementation choices separate',set(boundary)=={'profile_version','profile_id','epistemic_status','claim_class','normative','profile','implementation','implementation_choices_not_theorems'} and boundary['implementation_choices_not_theorems'])
 current=ld(D/'CURRENT-STATUS.yaml');ck('NI01','non_invention','target engine remains unverified and no current object invented',current['objects']==[] and current['target_engine_conformance']=='UNVERIFIED' and current['reference_harness_only'] and not current['invented'])
 prior=ld(D/'PRIOR-INTEGRITY.yaml');bad=[]
 for x in prior['artifacts']:
  p=C/x['path']
  if not p.is_file() or p.stat().st_size!=x['bytes'] or sha(p)!=x['sha256']:bad.append(x['path'])
 ck('PR01','integrity','all 803 predecessor artifacts preserved',prior['protected_artifact_count']==len(prior['artifacts'])==803 and not bad,str(bad[:10]))
 heads=re.findall(r'^## (\d+)\. ',(D/'SPECIFICATION.md').read_text(),re.M);ck('DOC01','documentation','all 26 required deliverable sections',heads==[str(i) for i in range(1,27)])
 det=ld(D/'DETERMINISM-VALIDATION.yaml') if (D/'DETERMINISM-VALIDATION.yaml').is_file() else {};ck('Q01','determinism','45 generator artifacts deterministic',det.get('status')=='PASS' and det.get('summary',{}).get('identical')==45)
 regv=ld(D/'REGRESSION-VALIDATION.yaml') if (D/'REGRESSION-VALIDATION.yaml').is_file() else {};ck('Q02','regression','profile predecessor and append guards pass',regv.get('status')=='PASS')
 ck('Q03','hygiene','no Python cache files',not list(H.rglob('__pycache__')) and not list(H.rglob('*.pyc')))
 z.append({'check_id':'GATE-R2','category':'acceptance','result':'BLOCKED','description':'target engine conformance','detail':'Reference harness conforms; target engine remains UNVERIFIED and inherited audit remains SPEC_INVALID_AT_PIPELINE_STAGE_2.'});return finish(z)
def finish(z):
 p=sum(x['result']=='PASS' for x in z);f=sum(x['result']=='FAIL' for x in z);b=sum(x['result']=='BLOCKED' for x in z);s='FAIL' if f else 'REFERENCE_HARNESS_TESTS_PASS_DURABILITY_AND_TARGET_ENGINE_UNVERIFIED';out={'profile_version':V,'overall_status':s,'summary':{'total':len(z),'passed':p,'failed':f,'blocked':b},'checks':z};(D/'VALIDATION.yaml').write_text(json.dumps(out,indent=2)+'\n');(D/'VALIDATION.md').write_text(f'# v14.7-R2 Validation\n\n{p} PASS / {f} FAIL / {b} BLOCKED ({len(z)} checks)\n\n`{s}`\n');print(f'{p} PASS / {f} FAIL / {b} BLOCKED ({len(z)} checks); {s}');return 1 if f else 0
if __name__=='__main__':sys.exit(main())
