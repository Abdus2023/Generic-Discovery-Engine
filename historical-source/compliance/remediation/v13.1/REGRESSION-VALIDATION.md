# Protocol-v13.1 Regression Validation

**Status:** `PASS`

All independently executed version-correct regressions retained their expected structural result and one expected blocked acceptance gate.

| Protocol | PASS | FAIL | BLOCKED | Overall |
|---|---:|---:|---:|---|
| v13 | 115 | 0 | 1 | `STRUCTURAL_PASS_REMEDIATION_BLOCKED` |
| v12.1 | 194 | 0 | 1 | `STRUCTURAL_PASS_AUDIT_BLOCKED` |
| v12 | 148 | 0 | 1 | `STRUCTURAL_PASS_AUDIT_BLOCKED` |
| v11.1 | 177 | 0 | 1 | `STRUCTURAL_PASS_INPUT_REJECTED` |
| v10.1 | 143 | 0 | 1 | `STRUCTURAL_PASS_INPUT_BLOCKED` |

The v13 builder also refused to erase the append-only `v13.1` extension, as required.
