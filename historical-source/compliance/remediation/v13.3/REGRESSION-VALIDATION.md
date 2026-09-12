# Protocol-v13.3 Regression Validation

**Status:** `PASS`

| Protocol | PASS | FAIL | BLOCKED | Overall |
|---|---:|---:|---:|---|
| v13.2 | 117 | 0 | 1 | `STRUCTURAL_PASS_AUDIT_BLOCKED` |
| v13.1 | 110 | 0 | 1 | `STRUCTURAL_PASS_AGGREGATE_BLOCKED` |
| v13 | 115 | 0 | 1 | `STRUCTURAL_PASS_REMEDIATION_BLOCKED` |
| v12.1 | 194 | 0 | 1 | `STRUCTURAL_PASS_AUDIT_BLOCKED` |
| v12 | 148 | 0 | 1 | `STRUCTURAL_PASS_AUDIT_BLOCKED` |
| v11.1 | 177 | 0 | 1 | `STRUCTURAL_PASS_INPUT_REJECTED` |
| v10.1 | 143 | 0 | 1 | `STRUCTURAL_PASS_INPUT_BLOCKED` |

All predecessor guards and the v13.3 appended-record guard refused destructive regeneration as required.
