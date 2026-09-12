# Migration Obligations

> **Input status: INPUT_CONTRACT_FAILED.** Protocol-v1 source integrity fails and required Protocol-v4 through Protocol-v7 artifacts are missing. This is a structurally validated, downgraded source-local corpus—not an accepted complete v10.1 synthesis. Missing evidence is not evidence of absence.

| Area | Required when changed | State |
|---|---|---|
| candidate identity | versioning, compatibility layer, data/test migration | CONDITIONAL |
| candidate state | state mapping, documentation, tests | CONDITIONAL |
| persistence | schema version, validated migration/rejection, recovery | CONDITIONAL |
| export | versioned envelope, adapter, partial marker | CONDITIONAL |
| provider/error/nullability | deprecation, adapter, semantic negative tests | CONDITIONAL |
| v0.5 parse defect | retain evidence; no compatibility reproduction by default | REQUIRED_FIX |
