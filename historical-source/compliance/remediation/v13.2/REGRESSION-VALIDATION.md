# Protocol-v13.2 Regression Validation

**Status:** `PASS`

All version-correct predecessor validators retained their expected structural result and expected blocked acceptance gate.

| Protocol | PASS | FAIL | BLOCKED | Overall |
|---|---:|---:|---:|---|
| v13.1 | 110 | 0 | 1 | `STRUCTURAL_PASS_AGGREGATE_BLOCKED` |
| v13 | 115 | 0 | 1 | `STRUCTURAL_PASS_REMEDIATION_BLOCKED` |
| v12.1 | 194 | 0 | 1 | `STRUCTURAL_PASS_AUDIT_BLOCKED` |
| v12 | 148 | 0 | 1 | `STRUCTURAL_PASS_AUDIT_BLOCKED` |
| v11.1 | 177 | 0 | 1 | `STRUCTURAL_PASS_INPUT_REJECTED` |
| v10.1 | 143 | 0 | 1 | `STRUCTURAL_PASS_INPUT_BLOCKED` |

The v13 and v13.1 builders refused to erase their append-only successor extensions, and the v13.2 builder refused to erase appended transition history.
