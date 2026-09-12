#!/usr/bin/env python3
"""Standard-library reference conformance harness for v14.7-R2."""
from __future__ import annotations
import hashlib,json,threading,unicodedata
from copy import deepcopy
from datetime import datetime,timezone

PROFILE_ID="gde-cjson-1"; HASH_ALGORITHM="sha256"; EVAL_RESULTS=("TRUE","FALSE","UNKNOWN","BLOCKED","INVALID")
def outcome(status, failure_class=None, detail="", value=None):return {"status":status,"failure_class":failure_class,"detail":detail,"value":value}
def _normalize(value):
 if value is None or isinstance(value,(bool,int)):return value
 if isinstance(value,float):raise ValueError("GDE-CJSON-1 forbids floating-point values")
 if isinstance(value,str):return unicodedata.normalize("NFC",value)
 if isinstance(value,list):return [_normalize(x) for x in value]
 if isinstance(value,dict):
  pairs=[(unicodedata.normalize("NFC",str(k)),_normalize(v)) for k,v in value.items()]
  if len({k for k,_ in pairs})!=len(pairs):raise ValueError("normalized key collision")
  return {k:v for k,v in sorted(pairs,key=lambda x:[ord(c) for c in x[0]])}
 raise TypeError(f"unsupported canonical type: {type(value).__name__}")
def canonical_bytes(value):return json.dumps(_normalize(value),ensure_ascii=False,sort_keys=False,separators=(",",":"),allow_nan=False).encode("utf-8")
def content_hash(domain,value,exclude=()):
 if not isinstance(domain,str) or not domain:raise ValueError("typed hash domain required")
 body={k:v for k,v in value.items() if k not in set(exclude)} if isinstance(value,dict) else value
 prefix=f"GDE-HASH-1\n{domain}\n{PROFILE_ID}\n".encode()
 return hashlib.sha256(prefix+canonical_bytes(body)).hexdigest()
def parse_utc(value):
 if not isinstance(value,str) or not value.endswith("Z"):raise ValueError("timestamp must be UTC Z")
 dt=datetime.fromisoformat(value[:-1]+"+00:00")
 if dt.utcoffset()!=timezone.utc.utcoffset(dt):raise ValueError("not UTC")
 return dt

class SchemaValidator:
 def validate(self,obj,schema):
  errors=[]
  if schema.get("type")=="object" and not isinstance(obj,dict):return outcome("INVALID","STRUCTURAL_FAILURE","not object")
  missing=set(schema.get("required",[]))-set(obj)
  if missing:errors.append("missing:"+",".join(sorted(missing)))
  if schema.get("additionalProperties") is False:
   extra=set(obj)-set(schema.get("properties",{}))
   if extra:errors.append("extra:"+",".join(sorted(extra)))
  for k,v in obj.items():
   s=schema.get("properties",{}).get(k,{})
   if "enum" in s and v not in s["enum"]:errors.append(f"enum:{k}")
   if "const" in s and v!=s["const"]:errors.append(f"const:{k}")
   typ=s.get("type");valid={"string":isinstance(v,str),"integer":isinstance(v,int) and not isinstance(v,bool),"boolean":isinstance(v,bool),"array":isinstance(v,list),"object":isinstance(v,dict),"null":v is None}.get(typ,True)
   if not valid:errors.append(f"type:{k}")
  return outcome("VALID" if not errors else "INVALID",None if not errors else "STRUCTURAL_FAILURE",";".join(errors))

class ReferenceValidator:
 def build_index(self,objects):
  index={}
  for o in objects:
   key=(o["object_type"],o["object_id"])
   if key in index:return outcome("INVALID","REFERENCE_FAILURE","duplicate identity")
   index[key]=o
  return outcome("VALID",value=index)
 def validate(self,references,index,source_scope,allow_cycles=False):
  edges=[]
  for r in references:
   key=(r["target_type"],r["target_id"]);target=index.get(key)
   if target is None:
    if r.get("required",True):return outcome("INVALID","REFERENCE_FAILURE","missing target")
    continue
   if target.get("scope_hash")!=source_scope:return outcome("INVALID","SCOPE_FAILURE","wrong scope")
   if r.get("target_hash") and r["target_hash"]!=target.get("content_hash"):return outcome("INVALID","INTEGRITY_FAILURE","wrong target hash")
   if r.get("schema_id") and r["schema_id"]!=target.get("schema_id"):return outcome("INVALID","REFERENCE_FAILURE","wrong schema/version")
   edges.append((r.get("source_id"),r["target_id"]))
  if not allow_cycles:
   graph={}
   for a,b in edges:
    if a:graph.setdefault(a,[]).append(b)
   visiting=set();done=set()
   def visit(n):
    if n in visiting:return False
    if n in done:return True
    visiting.add(n)
    if not all(visit(x) for x in graph.get(n,[])):return False
    visiting.remove(n);done.add(n);return True
   if not all(visit(n) for n in list(graph)):return outcome("INVALID","REFERENCE_FAILURE","circular reference")
  return outcome("VALID")

class IntegrityValidator:
 def validate_hash(self,domain,obj,field="content_hash",exclude=("content_hash",)):
  expected=content_hash(domain,obj,exclude)
  return outcome("VALID" if obj.get(field)==expected else "INVALID",None if obj.get(field)==expected else "INTEGRITY_FAILURE",value=expected)

class TemporalValidator:
 def validate_interval(self,instant,not_before,not_after,max_future_seconds=0):
  try:t=parse_utc(instant);lo=parse_utc(not_before);hi=parse_utc(not_after) if not_after else None
  except Exception as e:return outcome("INVALID","TEMPORAL_FAILURE",str(e))
  if hi is not None and hi<=lo:return outcome("INVALID","TEMPORAL_FAILURE","contradictory interval")
  if t<lo:return outcome("NOT_YET_VALID")
  if hi is not None and t>=hi:return outcome("EXPIRED")
  return outcome("ACTIVE")

class ScopeValidator:
 def validate(self,requested,granted):return outcome("TRUE" if set(requested)<=set(granted) else "FALSE",None if set(requested)<=set(granted) else "SCOPE_FAILURE")
class PolicyValidator:
 def validate_gate(self,gate):
  required={"ELIGIBLE","INELIGIBLE","BLOCKED","UNKNOWN"}
  if gate.get("empty_mandatory_action") not in {"ALLOW","DENY","BLOCK","UNKNOWN"}:return outcome("INVALID","POLICY_FAILURE","empty action")
  if set(gate.get("decision_mappings",{}))!=required:return outcome("INVALID","POLICY_FAILURE","incomplete mappings")
  return outcome("VALID")
class EvidenceValidator:
 def validate(self,evidence):
  if evidence is None:return outcome("INVALID","REFERENCE_FAILURE","missing required evidence")
  return outcome({"FRESH":"TRUE","STALE":"UNKNOWN","UNKNOWN":"UNKNOWN","UNAVAILABLE":"BLOCKED","INVALID":"INVALID"}.get(evidence.get("freshness"),"INVALID"),"FRESHNESS_FAILURE" if evidence.get("freshness")!="FRESH" else None)

class Evaluator:
 def evaluate(self,subject,predicate,context,evaluator):
  required=("evaluator_id","version","hash")
  if any(not evaluator.get(x) for x in required):return outcome("INVALID","EVALUATION_FAILURE","unbound evaluator")
  if context.get("sealed") is not True:return outcome("INVALID","INTEGRITY_FAILURE","unsealed context")
  op=predicate.get("op")
  if op=="equals":result="TRUE" if subject.get(predicate["field"])==predicate.get("value") else "FALSE"
  elif op=="present":result="TRUE" if predicate["field"] in subject else "FALSE"
  elif op=="unknown":result="UNKNOWN"
  elif op=="blocked":result="BLOCKED"
  else:result="INVALID"
  basis={"subject":subject,"predicate":predicate,"context":context,"evaluator":evaluator,"result":result}
  return outcome(result,None if result!="INVALID" else "EVALUATION_FAILURE",value={"result":result,"evaluation_hash":content_hash("EVALUATION",basis)})

class Aggregator:
 def aggregate(self,results,empty_action=None):
  if not results:
   return outcome({"ALLOW":"ELIGIBLE","DENY":"INELIGIBLE","BLOCK":"BLOCKED","UNKNOWN":"UNKNOWN"}.get(empty_action,"INVALID"),None if empty_action in {"ALLOW","DENY","BLOCK","UNKNOWN"} else "POLICY_FAILURE")
  if "INVALID" in results:return outcome("INVALID","EVALUATION_FAILURE")
  for r,s in [("FALSE","INELIGIBLE"),("BLOCKED","BLOCKED"),("UNKNOWN","UNKNOWN")]:
   if r in results:return outcome(s)
  return outcome("ELIGIBLE")

class AuthorityValidator:
 def qualify(self,authority,credential,operation,requested_scope,policy,instant,approvals=()):
  if not credential or not credential.get("valid"):return outcome("INVALID","AUTHORITY_FAILURE","credential")
  if authority.get("status")!="ACTIVE":return outcome("UNQUALIFIED","AUTHORITY_FAILURE","inactive")
  if operation not in authority.get("operations",[]):return outcome("UNQUALIFIED","AUTHORITY_FAILURE","operation")
  if not set(requested_scope)<=set(authority.get("scope",[])):return outcome("UNQUALIFIED","SCOPE_FAILURE")
  temporal=TemporalValidator().validate_interval(instant,authority["not_before"],authority.get("not_after"))
  if temporal["status"]!="ACTIVE":return outcome("UNQUALIFIED","AUTHORITY_FAILURE",temporal["status"])
  if authority.get("parent_scope") is not None and not set(authority.get("scope",[]))<=set(authority["parent_scope"]):return outcome("INVALID","AUTHORITY_FAILURE","delegation exceeds parent")
  threshold=policy.get("threshold",1)
  if threshold<1:return outcome("INVALID","POLICY_FAILURE","zero threshold")
  distinct={a["authority_id"] for a in approvals if a.get("valid") and a.get("basis_hash")==policy.get("basis_hash")}
  if authority.get("type")=="MULTI_PARTY" and len(distinct)<threshold:return outcome("BLOCKED","AUTHORITY_FAILURE","threshold")
  return outcome("QUALIFIED")

class TransitionGuard:
 def validate(self,current,event,rule):
  if current!=rule["from_state"]:return outcome("INVALID","STATE_TRANSITION_FAILURE","wrong predecessor")
  if event.get("event_type")!=rule["event_type"]:return outcome("INVALID","STATE_TRANSITION_FAILURE","illegal event")
  if rule.get("authority_required") and not event.get("authority_valid"):return outcome("INVALID","AUTHORIZATION_FAILURE","authority")
  if set(rule.get("required_evidence",[]))-set(event.get("evidence_refs",[])):return outcome("INVALID","EVIDENCE_FAILURE","evidence")
  if not event.get("scope_valid",False):return outcome("INVALID","SCOPE_FAILURE")
  return outcome("VALID",value=rule["to_state"])

class EventStore:
 def __init__(self):self._streams={};self._event_ids={};self._keys={};self._lock=threading.Lock();self._commit=0
 def append_event(self,stream_id,event,expected_version,idempotency_key):
  with self._lock:
   k=(stream_id,idempotency_key)
   if k in self._keys:return outcome("IDEMPOTENT_REPLAY",value=deepcopy(self._keys[k]))
   if event["event_id"] in self._event_ids:return outcome("CONFLICT","CONCURRENCY_FAILURE","duplicate event")
   stream=self._streams.setdefault(stream_id,[]);actual=len(stream)-1
   if expected_version!=actual:return outcome("CONFLICT","CONCURRENCY_FAILURE","version")
   e=deepcopy(event);e.update({"stream_id":stream_id,"sequence_no":actual+1,"previous_event_id":stream[-1]["event_id"] if stream else None,"commit_index":self._commit,"idempotency_key":idempotency_key});self._commit+=1;stream.append(e);self._event_ids[e["event_id"]]=e;self._keys[k]=e
   return outcome("COMMITTED",value=deepcopy(e))
 def read_stream(self,stream_id):return deepcopy(self._streams.get(stream_id,[]))
 def read_events(self):return deepcopy(sorted(self._event_ids.values(),key=lambda x:x["commit_index"]))
 def read_checkpoint(self,stream_id):return None
 def verify_stream(self,stream_id):
  s=self._streams.get(stream_id,[])
  for n,e in enumerate(s):
   if e["sequence_no"]!=n or e["previous_event_id"]!=(s[n-1]["event_id"] if n else None):return outcome("INVALID","EVENT_ORDER_FAILURE")
  return outcome("VALID")

class Projector:
 def project(self,history,profile):
  if profile.get("profile_id")!=PROFILE_ID:return outcome("INVALID","PROJECTION_FAILURE","profile")
  seen=set();state=None
  for n,e in enumerate(history):
   if e.get("event_id") in seen or e.get("sequence_no")!=n or e.get("previous_event_id")!=(history[n-1]["event_id"] if n else None):return outcome("INVALID","EVENT_ORDER_FAILURE")
   if not e.get("valid",True):return outcome("INVALID","PROJECTION_FAILURE","invalid event")
   seen.add(e["event_id"]);state=e.get("to_state",state)
  result={"state":state,"event_count":len(history),"history_hash":content_hash("HISTORY",history)}
  return outcome("VALID",value=result)
class ProjectionVerifier:
 def verify(self,history,profile,stored):
  rebuilt=Projector().project(history,profile)
  return outcome("VALID" if rebuilt["status"]=="VALID" and rebuilt["value"]==stored else "INVALID",None if rebuilt["status"]=="VALID" and rebuilt["value"]==stored else "PROJECTION_FAILURE")
class ReuseChecker:
 def check(self,old,new,fields,conditions=()):
  if any(k not in old or k not in new for k in fields):return outcome("INVALID","REFERENCE_FAILURE")
  if any(old[k]!=new[k] for k in fields):return outcome("NOT_REUSABLE")
  if not all(conditions):return outcome("NOT_REUSABLE")
  return outcome("REUSABLE")
class ConformanceReporter:
 def create(self,profile,implementation,results,invariants,evaluated_at):
  counts={x:sum(r["status"]==x for r in results) for x in ["PASSED","FAILED","BLOCKED","INVALID","UNKNOWN"]};ic={x:sum(r==x for r in invariants) for x in ["SATISFIED","VIOLATED","UNKNOWN"]}
  if counts["INVALID"]:final="INVALID"
  elif counts["FAILED"] or ic["VIOLATED"]:final="NON_CONFORMANT"
  elif counts["BLOCKED"]:final="BLOCKED"
  elif counts["UNKNOWN"] or ic["UNKNOWN"]:final="UNVERIFIED"
  else:final="CONFORMANT"
  report={"report_id":"v147r2-reference-harness","profile_id":profile["profile_id"],"profile_version":profile["version"],"implementation":implementation,"evaluated_at":evaluated_at,"tests":{"total":len(results),"passed":counts["PASSED"],"failed":counts["FAILED"],"blocked":counts["BLOCKED"],"invalid":counts["INVALID"],"unknown":counts["UNKNOWN"]},"invariants":{"total":len(invariants),"satisfied":ic["SATISFIED"],"violated":ic["VIOLATED"],"unknown":ic["UNKNOWN"]},"result":final,"evidence_refs":["TEST-RESULTS.yaml","PROPERTY-RESULTS.yaml"]}
  report["content_hash"]=content_hash("CONFORMANCE_REPORT",report)
  return report
