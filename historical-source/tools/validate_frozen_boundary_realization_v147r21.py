#!/usr/bin/env python3
"""Independent validator for v14.7-R2.1 boundary realization."""
import ast,hashlib,json,re,sys
from pathlib import Path
R=Path(__file__).resolve().parents[2];H=R/'historical-source';C=H/'compliance';D=C/'certification/v14.7-R2.1';sys.path.insert(0,str(H/'tools'))
from v147r2_conformance_harness import content_hash
from v147r21_boundary_harness import VALIDATION_STATUSES,CONFORMANCE_STATUSES
from run_v147r21_boundary import run
V='14.7-R2.1'
def ld(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def const(n):
 t=ast.parse((H/'tools/build_frozen_boundary_realization_v147r21.py').read_text())
 for x in t.body:
  if isinstance(x,ast.Assign) and isinstance(x.targets[0],ast.Name) and x.targets[0].id==n:return ast.literal_eval(x.value)
 raise KeyError(n)
def valid_hash(domain,x):return x.get('content_hash')==content_hash(domain,{k:v for k,v in x.items() if k!='content_hash'})
def main():
 z=[]
 def ck(i,c,d,o,x=''):z.append({'check_id':i,'category':c,'result':'PASS' if o else 'FAIL','description':d,'detail':x})
 files=const('FILES');schemas=const('SCHEMAS');owned=files+[f'schema/{x}.schema.yaml' for x in schemas]+['SPECIFICATION.md'];ck('I01','inventory','44 generator-owned artifacts',len(owned)==44 and all((D/x).is_file() for x in owned))
 errs=[]
 for p in D.rglob('*.yaml'):
  try:ld(p)
  except Exception as e:errs.append(f'{p}:{e}')
 ck('I02','parse','all YAML parses',not errs,';'.join(errs));actual={str(p.relative_to(D)) for p in D.rglob('*') if p.is_file()}-{'VALIDATION.yaml','VALIDATION.md','DETERMINISM-VALIDATION.yaml','REGRESSION-VALIDATION.yaml'};ck('I03','inventory','no undeclared generator file',actual==set(owned),str(sorted(actual^set(owned))))
 ver=ld(D/'VERSION.yaml');result=ld(D/'EXECUTIVE-RESULT.yaml');ck('B01','boundary','R2.1 is realization clarification without semantic layer',ver['semantic_version']=='v14.7' and ver['clarifies']=='v14.7-R2' and not ver['new_semantic_layer'] and not result['v14_8'] and ver['version_resolution']=={'supplied_title':'v14.7-R2','supplied_acceptance_reference':'v14.7-R1','published_r2_immutable':True,'interpretation_affecting_profile_change':True,'resolved_profile_version':'14.7-R2.1','rationale':'APPEND_ONLY_PROFILE_VERSION_REQUIRED_NOT_V14_8'})
 ck('B02','boundary','three realization defects and no semantic contradiction',result['realization_defects']==3 and not result['semantic_contradiction'] and ld(D/'SEMANTIC-CONTRADICTIONS.yaml')['objects']==[])
 reg=ld(D/'SCHEMA-REGISTRY.yaml');ck('S01','schema','10 local schemas extend exact 57-schema predecessor set',len(reg['local'])==10 and reg['predecessor']['count']==57 and reg['effective_count']==67 and sha(D/reg['predecessor']['path'])==reg['predecessor']['sha256'])
 meta={'$schema','$id','title','type','required','properties','additionalProperties','x-identity-fields','x-immutable','x-self-excluding-hash-field','x-canonical-profile','x-normative-rules'};ok=True
 for x in reg['local']:
  s=ld(D/x['path']);ok &= sha(D/x['path'])==x['sha256'] and meta<=set(s) and s['type']=='object' and s['additionalProperties'] is False and s['x-immutable'] and set(s['required'])<=set(s['properties']) and set(s['x-identity-fields'])<=set(s['properties']) and 'content_hash' in s['required']
 ck('S02','schema','all boundary schemas complete immutable and hash-bound',ok)
 profile=ld(D/'PROFILE.yaml');basis=ld(D/'SPECIFICATION-BASIS.yaml');ps=ld(D/'schema/profile.schema.yaml');ck('P01','profile','profile object satisfies required top-level shape',set(ps['required'])<=set(profile) and set(profile)<=set(ps['properties']))
 ck('P02','profile','profile content hash valid and exact specification basis bound',valid_hash('PROFILE',profile) and profile['specification']['specification_hash']==basis['content_hash'])
 ck('P03','profile','specification basis binds v14.7 plus append-only correction',basis['specification_version']=='14.7.1' and len(basis['components'])==2 and all(sha(D/x['path'])==x['sha256'] for x in basis['components']))
 choices=profile['choice_classification'];ck('P04','profile','every choice has exactly one of three statuses',len(choices)==18 and {x['status'] for x in choices}=={'FIXED','PROFILE-SELECTABLE','IMPLEMENTATION-DEFINED'})
 ck('P05','profile','all profile-selectable choices selected and implementation-defined choices explicit',all(x['selected'] is not None for x in choices if x['status']=='PROFILE-SELECTABLE') and all('selected' in x for x in choices if x['status']=='IMPLEMENTATION-DEFINED'))
 ck('P06','profile','complete interoperability bindings and limits',profile['hashing']['algorithm']=='SHA-256' and profile['signatures']['algorithm']=='Ed25519' and profile['time']['max_clock_skew']=='PT5S' and profile['events']['atomic_commit'] and profile['policy']['predicate_language']=='GDE-PREDICATE-1' and profile['choice_universe']['closed'] and profile['semantic_preservation']['semantic_states']=='UNCHANGED' and profile['semantic_preservation']['authority']=='UNCHANGED' and all(profile['limits'][x] is not None for x in profile['limits']))
 pc=ld(D/'PROFILE-CONFORMANCE.yaml');ic=ld(D/'IMPLEMENTATION-CONFORMANCE.yaml');ck('P07','profile','profile-to-spec and implementation-to-profile claims separate',pc['claim']=='ProfileConformant(P,S)' and pc['result']=='CONFORMANT' and ic['claim']=='ImplementationSatisfiesProfile(I,P)' and ic['result']=='UNVERIFIED' and not ic['direct_specification_claim'])
 compat=ld(D/'PROFILE-COMPATIBILITY.yaml');ck('P08','profile','compatibility explicit not version-inferred',valid_hash('PROFILE_COMPATIBILITY',compat) and compat['classification']=='CONVERTIBLE' and compat['migration_required'] and compat['semantic_equivalence']=='UNKNOWN' and compat['migration']['operation']=='REVALIDATE_REHASH_RESIGN' and compat['migration']['source_validity']=='NOT_TRANSFERRED')
 vr=ld(D/'VALIDATION-RESULT-MODEL.yaml');er=ld(D/'OUTPUT-TAXONOMY.yaml');vs=ld(D/'schema/validation-result.schema.yaml');es=ld(D/'schema/evaluation-result.schema.yaml');ck('O01','outputs','ValidationResult exactly VALID INVALID BLOCKED UNKNOWN and no truth values',vr['statuses']==['VALID','INVALID','BLOCKED','UNKNOWN'] and vs['properties']['status']['enum']==vr['statuses'] and set(vr['forbidden'])=={'TRUE','FALSE'} and tuple(vr['statuses'])==VALIDATION_STATUSES)
 ck('O02','outputs','EvaluationResult remains exact and distinct',er['EvaluationResult']==['TRUE','FALSE','UNKNOWN','BLOCKED','INVALID'] and es['properties']['status']['enum']==er['EvaluationResult'] and set(er['ValidationResult']).isdisjoint({'TRUE','FALSE'}))
 ck('O03','outputs','ConformanceResult exact and distinct from validation/evaluation',tuple(er['ConformanceResult'])==CONFORMANCE_STATUSES and er['substitution']=='FORBIDDEN')
 boundary=ld(D/'EVALUATION-VALIDATION-BOUNDARY.yaml');ck('O04','outputs','only VALID permits evaluation and validator cannot emit truth',boundary['validation_valid']=='EVALUATION_PERMITTED' and boundary['validation_invalid']=='STOP' and not boundary['validator_may_emit_truth'] and not boundary['evaluator_bypass'])
 req=ld(D/'REQUIREMENTS.yaml')['objects'];rs=ld(D/'schema/requirement.schema.yaml');banned={'Rust','SQLite','PostgreSQL','Tokio'};ck('R01','requirements','12 complete immutable requirements with valid hashes',len(req)==12 and [x['requirement_id'] for x in req]==[f'R-BOUNDARY-{i:03d}' for i in range(1,13)] and all(set(rs['required'])<=set(x) and valid_hash('REQUIREMENT',x) for x in req))
 ck('R02','requirements','normative requirement statements contain no selected implementation technology',all(not any(term in x['statement']['text'] for term in banned) for x in req))
 ins=ld(D/'IMPLEMENTATION-INSTRUCTIONS.yaml')['objects'];ischema=ld(D/'schema/implementation-instruction.schema.yaml');ck('R03','requirements','implementation instructions separately typed and hash-valid',len(ins)==4 and all(set(ischema['required'])<=set(x) and valid_hash('IMPLEMENTATION_INSTRUCTION',x) for x in ins))
 ck('R04','requirements','every mandatory instruction has explicit profile or contract authority',all(not x['mandatory'] or x['authority_ref'] for x in ins))
 mapping=ld(D/'REALIZATION-MAPPING.yaml');pbs=ld(D/'schema/profile-binding.schema.yaml');ck('R05','requirements','all requirements have hash-bound profile bindings and executable mappings',len(mapping['mappings'])==len(mapping['profile_bindings'])==12 and mapping['chain']==['REQUIREMENT','PROFILE_BINDING','IMPLEMENTATION_INSTRUCTION','EXECUTABLE_TEST','EVIDENCE'] and all(set(pbs['required'])<=set(x) and valid_hash('PROFILE_BINDING',x) and x['profile_id']==profile['profile_id'] and x['profile_version']==profile['profile_version'] for x in mapping['profile_bindings']) and {x['requirement_id'] for x in mapping['mappings']}=={x['requirement_id'] for x in req} and {x['test_ref'] for x in mapping['mappings']}=={f'R2B-T-{i:03d}' for i in range(29,41)})
 impl=ld(D/'IMPLEMENTATION-CONTRACT.yaml');impls=ld(D/'schema/implementation-contract.schema.yaml');ck('R06','requirements','implementation contract names exact profile and valid artifact',set(impls['required'])<=set(impl) and valid_hash('IMPLEMENTATION_CONTRACT',impl) and impl['profile_id']==profile['profile_id'] and impl['profile_version']==profile['profile_version'])
 attrs=ld(D/'FAILURE-ATTRIBUTION.yaml');fschema=ld(D/'schema/failure-attribution.schema.yaml');ck('F01','failures','11 exact hash-bound failure origins and no automatic implementation attribution',len(attrs['origins'])==len(set(attrs['origins']))==len(attrs['objects'])==11 and all(set(fschema['required'])<=set(x) and valid_hash('FAILURE_ATTRIBUTION',x) for x in attrs['objects']) and not attrs['automatic_implementation_attribution'])
 coercions=ld(D/'COERCION-GUARDS.yaml')['forbidden'];ck('C01','coercion','all nine forbidden cross-domain conversions explicit',len(coercions)==9 and len({(x['source_domain'],x['source_value'],x['target_domain'],x['target_value']) for x in coercions})==9)
 results=run(D);stored=ld(D/'BOUNDARY-TEST-RESULTS.yaml');ck('T01','tests','40 boundary tests independently rerun and pass',len(results)==40 and results==stored['objects'] and all(x['status']=='PASSED' for x in results))
 tests=ld(D/'BOUNDARY-TESTS.yaml')['objects'];ck('T02','tests','validation tests never expect TRUE or FALSE',all(x['expected'] not in {'TRUE','FALSE'} for x in tests if x['operation'] in {'SCOPE_VALIDATE','EVIDENCE_VALIDATE','TEMPORAL_VALIDATE'}))
 ck('T03','tests','all nine semantic coercions execute as rejected',sum(x['operation']=='COERCION' and x['expected']=='REJECTED' for x in tests)==9)
 ck('T04','tests','validation gate blocks INVALID BLOCKED UNKNOWN before evaluation',all(next(x for x in results if x['test_id']==tid)['actual']==expected for tid,expected in [('R2B-T-002','INVALID'),('R2B-T-003','BLOCKED'),('R2B-T-004','BLOCKED')]))
 ac=ld(D/'ACCEPTANCE-CRITERIA.yaml');test_ids={x['test_id'] for x in tests if x['operation']=='ARTIFACT_ASSERTION'};ck('AC01','acceptance','all 12 supplied acceptance criteria independently execute and pass',ac['count']==12 and [x['id'] for x in ac['objects']]==[f'AC-{i:02d}' for i in range(1,13)] and {r for x in ac['objects'] for r in x['test_refs']}==test_ids and all(x['status']=='PASS' and x['description'] for x in ac['objects']) and sum(x['operation']=='ARTIFACT_ASSERTION' for x in tests)==12)
 inv=ld(D/'INVARIANTS.yaml')['objects'];ck('N01','invariants','13 unique frozen-boundary invariants',len(inv)==len(set(inv))==13)
 trace=ld(D/'TRACEABILITY.yaml');ck('TR01','traceability','full object-to-verification and requirement-to-evidence traces bidirectional',trace['chain']==['OBJECT','VALIDATION','EVALUATION_ELIGIBILITY','EVALUATION','REQUIREMENT_RESULT','CONFORMANCE','ELIGIBILITY','AUTHORIZATION','DECISION','EXECUTION','VERIFICATION'] and len(trace['requirement_chain'])==7 and trace['reverse'])
 current=ld(D/'CURRENT-STATUS.yaml');ck('NI01','non_invention','profile conformant but implementation and target explicitly unverified',current['objects']==[] and current['profile_conformance']=='CONFORMANT' and current['reference_implementation_conformance']=='UNVERIFIED' and current['target_engine']=='UNVERIFIED' and not current['invented'])
 prior=ld(D/'PRIOR-INTEGRITY.yaml');bad=[]
 for x in prior['artifacts']:
  p=C/x['path']
  if not p.is_file() or p.stat().st_size!=x['bytes'] or sha(p)!=x['sha256']:bad.append(x['path'])
 ck('PR01','integrity','all 852 predecessor artifacts preserved',prior['protected_artifact_count']==len(prior['artifacts'])==852 and not bad,str(bad[:10]))
 heads=re.findall(r'^## (\d+)\. ',(D/'SPECIFICATION.md').read_text(),re.M);ck('D01','documentation','26 required boundary deliverable sections',heads==[str(i) for i in range(1,27)])
 det=ld(D/'DETERMINISM-VALIDATION.yaml') if (D/'DETERMINISM-VALIDATION.yaml').is_file() else {};ck('Q01','determinism','44 generator artifacts deterministic',det.get('status')=='PASS' and det.get('summary',{}).get('identical')==44)
 regv=ld(D/'REGRESSION-VALIDATION.yaml') if (D/'REGRESSION-VALIDATION.yaml').is_file() else {};ck('Q02','regression','R2 predecessor and append guards pass',regv.get('status')=='PASS')
 ck('Q03','hygiene','no Python caches',not list(H.rglob('__pycache__')) and not list(H.rglob('*.pyc')))
 z.append({'check_id':'GATE-R21','category':'acceptance','result':'BLOCKED','description':'implementation and target conformance','detail':'Profile conforms; Ed25519 provider, durable store, and target engine remain unverified.'});return finish(z)
def finish(z):
 p=sum(x['result']=='PASS' for x in z);f=sum(x['result']=='FAIL' for x in z);b=sum(x['result']=='BLOCKED' for x in z);s='FAIL' if f else 'PROFILE_CONFORMANT_IMPLEMENTATION_AND_TARGET_UNVERIFIED';out={'profile_version':V,'overall_status':s,'summary':{'total':len(z),'passed':p,'failed':f,'blocked':b},'checks':z};(D/'VALIDATION.yaml').write_text(json.dumps(out,indent=2)+'\n');(D/'VALIDATION.md').write_text(f'# v14.7-R2.1 Validation\n\n{p} PASS / {f} FAIL / {b} BLOCKED ({len(z)} checks)\n\n`{s}`\n');print(f'{p} PASS / {f} FAIL / {b} BLOCKED ({len(z)} checks); {s}');return 1 if f else 0
if __name__=='__main__':sys.exit(main())
