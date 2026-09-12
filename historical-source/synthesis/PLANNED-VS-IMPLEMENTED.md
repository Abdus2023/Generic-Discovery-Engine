# Planned vs Implemented

> **Acceptance: PROVISIONAL_ONLY_UPSTREAM_BLOCKED.** Protocol-v1 raw/range validation fails and Protocol-v4 through Protocol-v7 outputs are absent. `SUPPORTED` in this report is source-local and does not mean the full v1→v9 chain is verified. Missing dimensions remain `UNKNOWN`.

| Version | Planned | Described | Implemented occurrence | Historically tested | Verified now |
|---|---|---|---|---|---|
| v0.1.0 | UNKNOWN | Comments/names present; not design proof | snapshot-0001:LIKELY_EXECUTABLE | UNKNOWN | Retrospective static source-local only |
| v0.2.0 | UNKNOWN | Comments/names present; not design proof | snapshot-0003:LIKELY_EXECUTABLE | UNKNOWN | Retrospective static source-local only |
| v0.3.0 | UNKNOWN | Comments/names present; not design proof | snapshot-0005:LIKELY_EXECUTABLE | UNKNOWN | Retrospective static source-local only |
| v0.4.0 | UNKNOWN | Comments/names present; not design proof | snapshot-0006:LIKELY_EXECUTABLE; snapshot-0008:LIKELY_EXECUTABLE | UNKNOWN | Retrospective static source-local only |
| v0.5.0 | UNKNOWN | Comments/names present; not design proof | snapshot-0007:LIKELY_EXECUTABLE; snapshot-0009:NON_EXECUTABLE; snapshot-0011:LIKELY_EXECUTABLE | UNKNOWN | Retrospective static source-local only |
| v0.6.0 | UNKNOWN | Comments/names present; not design proof | snapshot-0010:LIKELY_EXECUTABLE; snapshot-0012:LIKELY_EXECUTABLE; snapshot-0013:LIKELY_EXECUTABLE | UNKNOWN | Retrospective static source-local only |
| v0.7.1 | UNKNOWN | Comments/names present; not design proof | snapshot-0014:LIKELY_EXECUTABLE | UNKNOWN | Retrospective static source-local only |

## Divergence rules

- A roadmap or current planning statement is `planned`, not historical code.
- A comment/interface is `described`, not proof of complete semantics.
- Reconstructed code is an occurrence, not proof of historical execution.
- Static parse validation is retrospective verification, not a historical test.
- snapshot-0009 proves the distinction sharply: it is an exact complete occurrence but fails parsing.

## Current-plan gap

Current plans describe protocol independence, capability/security policy, stronger contracts, and integrity validation beyond what recovered snapshots prove. Those gaps are not treated as historical defects unless the historical source itself states the requirement.
