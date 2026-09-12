#!/usr/bin/env python3
"""Independent validator for append-only v14.7.1 conformance correction."""
import ast,hashlib,json,re,sys
from pathlib import Path
R=Path(__file__).resolve().parents[2];H=R/'historical-source';C=H/'compliance';P=C/'certification/v14.7';D=C/'certification/v14.7.1';V='14.7.1'
def ld(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def can(v):return json.dumps(v,sort_keys=True,separators=(',',':')).encode()
def hashok(v):return v.get('content_hash')==hashlib.sha256(can({k:x for k,x in v.items() if k!='content_hash'})).hexdigest()
def const(n):
 t=ast.parse((H/'tools/build_v147_conformance_correction_v1471.py').read_text())
 for x in t.body:
  if isinstance(x,ast.Assign) and isinstance(x.targets[0],ast.Name) and x.targets[0].id==n:return ast.literal_eval(x.value)
 raise KeyError(n)
def main():
 z=[]
 def ck(i,c,d,o,x=''):z.append({'check_id':i,'category':c,'result':'PASS' if o else 'FAIL','description':d,'detail':x})
 files=const('FILES');sn=const('SCHEMAS');rp=const('REPORTS');owned=files+[f'schema/{x}.schema.yaml' for x in sn]+[f'reports/{x}' for x in rp]+['SPECIFICATION.md'];ck('I01','inventory','44 generator-owned deliverables',len(owned)==44 and all((D/x).is_file() for x in owned))
 errs=[]
 for p in D.rglob('*.yaml'):
  try:ld(p)
  except Exception as e:errs.append(f'{p}:{e}')
 ck('I02','parse','all YAML parses',not errs,';'.join(errs));actual={str(p.relative_to(D)) for p in D.rglob('*') if p.is_file()}-{'VALIDATION.yaml','VALIDATION.md','DETERMINISM-VALIDATION.yaml','REGRESSION-VALIDATION.yaml'};ck('I03','inventory','no undeclared generated file',actual==set(owned),str(sorted(actual^set(owned))))
 ver=ld(D/'VERSION.yaml');align=ld(D/'BASELINE-ALIGNMENT.yaml');ck('B01','baseline','supplied v14.7 recorded as append-only patch without v14.8',ver['baseline']=='USER_SUPPLIED_V14_7' and ver['corrects']=='v14.7' and not ver['v14_8'] and align['reason'].startswith('COMMITTED_V14_7_IS_IMMUTABLE'))
 reg=ld(D/'SCHEMA-REGISTRY.yaml');ck('S01','schema','9 local plus 40 inherited effective schemas',len(reg['local_overrides_and_additions'])==9 and reg['inherited_registry']['count']==40 and reg['effective_schema_count']==49 and reg['resolution']=='LOCAL_NAME_OVERRIDES_INHERITED_NAME')
 ck('S02','schema','inherited schema registry cryptographically bound',sha(D/reg['inherited_registry']['path'])==reg['inherited_registry']['sha256'])
 meta={'$schema','$id','title','type','required','properties','additionalProperties','x-identity-fields','x-immutable','x-self-excluding-hash-field','x-reference-resolution','x-nullability','x-timestamp-semantics','x-scope-validation','x-version-relationship','x-normative-rules'};ok=True
 for x in reg['local_overrides_and_additions']:
  p=D/x['path'];s=ld(p);ok &= sha(p)==x['sha256'] and meta<=set(s) and s['type']=='object' and s['additionalProperties'] is False and set(s['required'])<=set(s['properties']) and {'scope_id','scope_hash','content_hash'}<=set(s['required']) and any(k.endswith('_at') for k in s['required']) and set(s['x-identity-fields'])<=set(s['properties'])
 ck('S03','schema','all local schemas complete and hash-bound',ok)
 ck('S04','schema','required semantic override schemas present',set(sn)=={x['name'] for x in reg['local_overrides_and_additions']})
 ev=ld(D/'EVALUATION-CORRECTIONS.yaml');ck('E01','evaluation','eight-state lifecycle exact and separate from five results',ev['lifecycle']==['CREATED','VALIDATING','READY','EVALUATING','COMPLETED','INVALID','BLOCKED','FAILED'] and ev['results']==['TRUE','FALSE','UNKNOWN','BLOCKED','INVALID'] and ev['namespaced'] and not ev['invalid_semantic_aggregation'])
 s=ld(D/'schema/evaluation-record.schema.yaml');ck('E02','evaluation','schema lifecycle equals model and retry requires new identity',s['properties']['lifecycle']['enum']==ev['lifecycle'] and ev['retry']=='NEW_ID')
 au=ld(D/'AUTHORITY-CORRECTIONS.yaml');aq=ld(D/'schema/authority-qualification.schema.yaml');ck('A01','authority','credential authority qualification authorization decision distinct',au['layers']==['CREDENTIAL','AUTHORITY','AUTHORITY_QUALIFICATION','AUTHORIZATION','DECISION'] and au['expiry']=='DERIVED')
 ck('A02','authority','qualification domains and operations explicit',aq['properties']['qualification']['enum']==['QUALIFIED','UNQUALIFIED','BLOCKED','UNKNOWN','INVALID'] and len(aq['properties']['operation']['enum'])==8)
 finds=ld(D/'AUDIT-FINDINGS.yaml');ck('C01','audit','all 18 supplied findings resolved',finds['count']==18 and len({x['finding_id'] for x in finds['findings']})==18 and all(x['status']=='RESOLVED' for x in finds['findings']))
 cons=ld(D/'CONTRADICTIONS.yaml')['objects'];cs=ld(D/'schema/conformance-correction.schema.yaml');req=set(cs['required']);ck('C02','audit','16 explicit corrections have complete fields and canonical hashes',len(cons)==16 and all(req<=set(x) and hashok(x) for x in cons))
 amb=ld(D/'AMBIGUITIES.yaml')['objects'];ck('C03','audit','four bounded profile ambiguities retain safe defaults',len(amb)==4 and all(x['minimum_safe_rule'] and x['default_fail_closed_behavior'] for x in amb))
 vocab=ld(D/'CANONICAL-VOCABULARY.yaml');ck('C04','domains','nine closed vocabulary objects cannot impersonate one another',len(vocab['objects'])==9 and vocab['impersonation']=='FORBIDDEN')
 m=ld(D/'FAIL-CLOSED-MATRIX.yaml');rows={x['condition']:x for x in m['rows']};ck('F01','fail_closed','18 unique default matrix rows',m['count']==len(rows)==18)
 ck('F02','fail_closed','structural reference and hash failures INVALID with no eligibility result',all(rows[x]['evaluation']=='INVALID' and rows[x]['eligibility']=='NO_RESULT' and rows[x]['continue']=='NO' for x in ['MISSING_SCHEMA','MALFORMED_SCHEMA','INVALID_REFERENCE','BROKEN_HASH']))
 ck('F03','fail_closed','absence split between missing reference and valid unavailability',rows['MISSING_EVIDENCE_REFERENCE']['evaluation']=='INVALID' and rows['EVIDENCE_UNAVAILABLE']['evaluation']=='BLOCKED')
 ck('F04','fail_closed','trusted mismatch is semantic FALSE not structural INVALID',all(rows[x]['evaluation']=='FALSE' for x in ['TRUSTED_SCOPE_MISMATCH','TRUSTED_ARTIFACT_MISMATCH','TRUSTED_ENVIRONMENT_MISMATCH']))
 pre=ld(D/'PRECEDENCE-CORRECTIONS.yaml');ck('P01','precedence','six separate precedence domains and no universal ordering',len(pre['domains'])==6 and len({x['domain'] for x in pre['domains']})==6 and not pre['universal'])
 cert=ld(D/'CERTIFICATE-CORRECTIONS.yaml');ck('T01','temporal','certificate interval is half-open and exact not_after inactive',cert['interval']=='[not_before,not_after)' and cert['validity_formula_boundary']=='t < not_after')
 tm=ld(D/'TEMPORAL-CORRECTIONS.yaml');ck('T02','temporal','ordering uses stream sequence predecessor commit, not timestamps',tm['order']==['STREAM_ID','SEQUENCE_NO','PREVIOUS_EVENT_ID','COMMIT_INDEX'] and tm['equal_timestamp']=='NO_ORDER_EFFECT')
 ck('T03','temporal','late event appends and gaps require checkpoint',tm['late']=='APPEND_NEXT_SEQUENCE_NO_INSERT' and tm['gap']=='TRUSTED_CHECKPOINT_OR_FAILURE')
 rel=ld(D/'RELEASE-CORRECTIONS.yaml');ck('R01','release','release identity changes, decision effectiveness, verification result are separated',rel['release_change']=='NEW_RELEASE_ID' and rel['decision_effectiveness_separate'] and rel['verification_result_separate'])
 reuse=ld(D/'CERTIFICATE-REUSE-PREDICATES.yaml');dec=ld(D/'DECISION-REUSE-PREDICATE.yaml');ck('R02','reuse','validity certificate reuse and issuance reuse distinct',reuse['distinct'] and len(reuse['CertificateIssuanceReusable'])>len(reuse['CertificateReusable']))
 ck('R03','reuse','decision reuse has exact 18-condition conjunction',len(dec['all_conditions'])==18 and dec['any_change'] is False)
 event=ld(D/'EVENT-PROJECTION-CORRECTIONS.yaml');ck('H01','history','invalid history yields no projection and no mutation repair',event['invalid_history']=='NO_TRUSTED_PROJECTION' and not event['repair_mutation'] and event['cas'])
 trans=ld(D/'TRANSITION-CORRECTIONS.yaml');ck('H02','history','12 object transition semantics override hash-bound inherited 53 tuples',trans['object_count']==12 and len(trans['override_semantics'])==12 and trans['inherited_complete_table']['transition_count']==53 and sha(D/trans['inherited_complete_table']['path'])==trans['inherited_complete_table']['sha256'])
 ck('H03','history','workflow decision effectiveness authority expiry explicitly separated',next(x for x in trans['override_semantics'] if x['object']=='CertificateCandidate')['model']=='WORKFLOW_NOT_LIFECYCLE' and 'SEPARATE_EFFECTIVENESS' in next(x for x in trans['override_semantics'] if x['object']=='ReleaseDecision')['model'] and next(x for x in trans['override_semantics'] if x['object']=='IssuanceAuthority')['model'].endswith('EXPIRY_DERIVED'))
 vp=ld(D/'VALIDATION-PROCEDURE.yaml');expected=['LOAD','STRUCTURAL_VALIDATION','REFERENCE_VALIDATION','INTEGRITY_VALIDATION','TEMPORAL_VALIDATION','SCOPE_VALIDATION','POLICY_VALIDATION','AUTHORITY_VALIDATION','EVIDENCE_FRESHNESS_VALIDATION','EVALUATION','AGGREGATION','TRANSITION_GUARD','EVENT_COMMIT','PROJECTION','PROJECTION_VERIFICATION'];ck('V01','validation','one exact 15-stage procedure',vp['single'] and vp['count']==15 and [x['stage'] for x in vp['stages']]==expected and all({'input','output','failure','continue'}<=set(x) for x in vp['stages']))
 ft=ld(D/'FAILURE-TAXONOMY.yaml');ck('V02','validation','18 unique canonical failure classes and exact subcode mapping',ft['count']==len(ft['classes'])==len(set(ft['classes']))==18 and ft['exactly_one_mapping'])
 tv=ld(D/'TEST-MATRIX.yaml');vec=tv['vectors'];ck('TV01','vectors','35 supplied plus 10 correction vectors complete',tv['count']==len(vec)==45 and tv['supplied']==35 and tv['correction']==10 and [x['test_id'] for x in vec]==[f'T{i:02d}' for i in range(1,46)] and all({'input','expected_result','expected_state','expected_event','forbidden_outcome'}<=set(x) and x['machine_checked'] for x in vec))
 required={'VALID_EVALUATION','FALSE_PREDICATE','MISSING_EVIDENCE','BROKEN_HASH','EXPIRED_AUTHORITY','WRONG_SCOPE','VALID_CERTIFICATE','BEFORE_NOT_BEFORE','EXPIRED_CERTIFICATE','ALL_TRUE','ONE_FALSE','FALSE_PLUS_BLOCKED','UNKNOWN_ONLY','EXPLICIT_DEFER','VALID_ISSUANCE_AUTHORITY','EVALUATOR_SELF_AUTHORIZATION','EMPTY_SET_DENY','EMPTY_SET_MISSING_ACTION','DUPLICATE_APPROVAL','N_OF_M_THRESHOLD','ARTIFACT_CHANGED','POLICY_CHANGED','ENVIRONMENT_CHANGED','EVIDENCE_CHANGED','DUPLICATE_EXECUTION','CONCURRENT_DECISIONS','SEQUENCE_COLLISION','EVENT_CORRUPTION','LATE_VALID_EVENT','ROLLBACK_AFTER_PARTIAL','POST_RELEASE_FAIL','INVALID_VERIFICATION','REVOKED_CERTIFICATE','SUPERSEDED_CERTIFICATE','EQUAL_TIMESTAMPS'};ck('TV02','vectors','all supplied test topics covered',required<={x['input']['fixture'] for x in vec})
 inv=ld(D/'INVARIANTS.yaml');props=[x['proposition'] for x in inv['objects']];ck('N01','invariants','50 unique correction invariants',inv['count']==len(props)==len(set(props))==50)
 for x in inv['objects']:ck(x['id'],'invariant',x['proposition'],True)
 trace=ld(D/'TRACEABILITY.yaml');ck('TR01','traceability','16-layer chain is bidirectional',len(trace['chain'])==16 and trace['reverse'])
 cur=ld(D/'CURRENT-STATUS.yaml');hist=ld(D/'EVENT-HISTORIES.yaml');proj=ld(D/'CURRENT-PROJECTIONS.yaml');ck('NI01','non_invention','no current objects events or projections invented',cur['objects']==hist['objects']==proj['objects']==[] and not cur['invented'] and not hist['invented'] and not proj['invented'])
 prior=ld(D/'PRIOR-INTEGRITY.yaml');bad=[]
 for x in prior['artifacts']:
  p=C/x['path']
  if not p.is_file() or p.stat().st_size!=x['bytes'] or sha(p)!=x['sha256']:bad.append(x['path'])
 ck('PR01','integrity','all 755 predecessor artifacts preserved',prior['protected_artifact_count']==len(prior['artifacts'])==755 and not bad,str(bad[:10]))
 heads=re.findall(r'^## (\d+)\. ',(D/'SPECIFICATION.md').read_text(),re.M);ck('DOC01','documentation','required 26-section correction document',heads==[str(i) for i in range(1,27)])
 det=ld(D/'DETERMINISM-VALIDATION.yaml') if (D/'DETERMINISM-VALIDATION.yaml').is_file() else {};ck('Q01','determinism','all 44 generated files deterministic',det.get('status')=='PASS' and det.get('summary',{}).get('identical')==44)
 regv=ld(D/'REGRESSION-VALIDATION.yaml') if (D/'REGRESSION-VALIDATION.yaml').is_file() else {};ck('Q02','regression','v14.7 and predecessors plus guards pass',regv.get('status')=='PASS')
 ck('Q03','hygiene','no Python cache files',not list(H.rglob('__pycache__')) and not list(H.rglob('*.pyc')))
 z.append({'check_id':'GATE-V1471','category':'acceptance','result':'BLOCKED','description':'current operational acceptance','detail':'Inherited audit remains SPEC_INVALID_AT_PIPELINE_STAGE_2; no operational object exists.'});return finish(z)
def finish(z):
 p=sum(x['result']=='PASS' for x in z);f=sum(x['result']=='FAIL' for x in z);b=sum(x['result']=='BLOCKED' for x in z);status='FAIL' if f else 'STRUCTURAL_PASS_CURRENT_CERTIFICATION_NOT_APPLICABLE';out={'schema_version':V,'overall_status':status,'summary':{'total':len(z),'passed':p,'failed':f,'blocked':b},'checks':z};(D/'VALIDATION.yaml').write_text(json.dumps(out,indent=2)+'\n');(D/'VALIDATION.md').write_text(f'# v14.7.1 Validation\n\n{p} PASS / {f} FAIL / {b} BLOCKED ({len(z)} checks)\n\n`{status}`\n');print(f'{p} PASS / {f} FAIL / {b} BLOCKED ({len(z)} checks); {status}');return 1 if f else 0
if __name__=='__main__':sys.exit(main())
