#!/usr/bin/env python3
"""Execute v14.7-R6 machine contract vectors."""
import json
import sys
from pathlib import Path
from v147r6_machine_runtime import canonical, convert, enum_validate, error_disposition, guard_transition, identity, project, reuse, schema_validate
BASE=Path(__file__).resolve().parents[1]/"compliance/certification/v14.7-R6"

def run(base=BASE):
    tests=json.loads((base/"tests/MACHINE-TESTS.yaml").read_text())["objects"]
    schemas={x["schema_id"]:json.loads((base/x["path"]).read_text()) for x in json.loads((base/"SCHEMA-REGISTRY.yaml").read_text())["objects"]}
    conversions={x["rule_id"]:x for x in json.loads((base/"CONVERSION-REGISTRY.yaml").read_text())["objects"]}
    rows=[]
    for test in tests:
        data=test["input"];actual="HARNESS_ERROR"
        try:
            op=test["operation"]
            if op=="ENUM":actual=enum_validate(data["domain"],data["value"])
            elif op=="SCHEMA":actual=schema_validate(schemas[data["schema_id"]],data["value"])
            elif op=="BOUNDARY":actual="REJECTED" if data["forbidden"] else "ACCEPTED"
            elif op=="ERROR":actual=error_disposition(data["code"],data.get("policy"))
            elif op=="CONVERT":actual=convert(conversions.get(data.get("rule_id")),data["source_type"],data["source_value"],data["target_type"],data.get("evidence"),data.get("policy"))
            elif op=="TRANSITION":actual=guard_transition(data["domain"],data["source"],data["target"],data["context"])
            elif op=="PROJECT":actual=project(data["history"],data["profile_ref"],data["algorithm"])["status"]
            elif op=="PROJECTION_COMPARE":actual="SAME" if project(data["left"],data["profile_ref"],data["algorithm"])==project(data["right"],data["profile_ref"],data["algorithm"]) else "DIFFERENT"
            elif op=="REUSE":actual=reuse(data.get("old_basis"),data.get("new_basis"),data.get("compatible",False))
            elif op=="CANONICAL":actual="SAME" if canonical(data["left"])==canonical(data["right"]) else "DIFFERENT"
            elif op=="HASH":actual="DIFFERENT" if identity(data["left_domain"],data["value"])!=identity(data["right_domain"],data["value"]) else "SAME"
            elif op=="INVARIANT":actual="SATISFIED" if data.get("condition") is True else "VIOLATED"
            status="PASSED" if actual==test["expected"] else "FAILED"
        except Exception:
            actual="HARNESS_ERROR";status="INVALID"
        rows.append({"test_id":test["test_id"],"family":test["family"],"expected":test["expected"],"actual":actual,"status":status,"failure_origin":None if status=="PASSED" else "TEST_HARNESS_FAILURE"})
    return rows

def main():
    rows=run();summary={"total":len(rows),"passed":sum(x["status"]=="PASSED" for x in rows),"failed":sum(x["status"]!="PASSED" for x in rows)}
    print(json.dumps({"objects":rows,"summary":summary},indent=2));return 1 if summary["failed"] else 0
if __name__=="__main__":sys.exit(main())
