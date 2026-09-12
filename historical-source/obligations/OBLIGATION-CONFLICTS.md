# Obligation Conflicts

> **Input status: INPUT_CONTRACT_FAILED.** Protocol-v1 source integrity fails and required Protocol-v4 through Protocol-v7 artifacts are missing. This is a structurally validated, downgraded source-local corpus—not an accepted complete v10.1 synthesis. Missing evidence is not evidence of absence.

| ID | Left | Right | Difference | Status | Possible resolution |
|---|---|---|---|---|---|
| CONF-001 | OBL-CANDIDATE-PRIORITY | OBL-BOUNDED-CONCURRENCY | Potential stable ordering semantics may conflict with unrestricted concurrent scheduling. | UNRESOLVED | Version ordering or prove order-insensitive equivalence. |
| CONF-002 | OBL-DEDUP-SCOPES | OBL-CANDIDATE-PARENT | Aggressive merging may discard alternate parent provenance. | UNRESOLVED | Merge work identity while retaining alternate derivation edges. |
| CONF-003 | OBL-RETRY | OBL-RESOURCE | Continuation through retry is constrained by finite resource bounds. | CONDITIONALLY_RESOLVED | Classify retryability and expose exhaustion under explicit limits. |
| CONF-004 | OBL-PERSIST-COMPAT | OBL-PROVENANCE-INTEGRITY | Schema compatibility may conflict with strengthened provenance fields or protection. | UNRESOLVED | Version and migrate rather than reinterpret old records. |
| CONF-005 | OBL-PROVIDER-ORDER | OBL-PROVIDER-FAILURE | Parallel/isolation changes may alter first-match provider ordering. | UNRESOLVED | Establish ordering dependence, then test or version the change. |
| CONF-006 | OBL-PARSE-DEFECT | OBL-PRIVATE-SHAPE | Byte/source-form preservation is not semantic preservation of a known parse defect. | FALSE_CONFLICT | Preserve defect evidence; reject reproduction as a future requirement. |

Conflicts are not dependency prerequisites and chronology does not resolve them.
