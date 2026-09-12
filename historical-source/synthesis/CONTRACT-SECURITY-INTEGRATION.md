# Contract and Security Integration

> **Acceptance: PROVISIONAL_ONLY_UPSTREAM_BLOCKED.** Protocol-v1 raw/range validation fails and Protocol-v4 through Protocol-v7 outputs are absent. `SUPPORTED` in this report is source-local and does not mean the full v1→v9 chain is verified. Missing dimensions remain `UNKNOWN`.

## Integration boundary

Protocol-v8 is internally validated (`87/87 PASS`) but explicitly prerequisite-blocked. Protocol-v7 is physically absent, so no historical source shape is relabeled as a verified contract.

| Dimension | Historical source-local result | Contract result | Security result | Confidence |
|---|---|---|---|---|
| Identity | Candidate/Observation/Discovery identifiers occur | UNKNOWN | Mutable/generated identity is a mechanism, not integrity | SUPPORTED / UNKNOWN |
| Acquisition | HTTP/browser acquisition occurs | UNKNOWN | External network and parser boundaries are explicit | SUPPORTED |
| Scheduling | Queues/status/claims/retries occur | UNKNOWN | Race and resource risks remain | SUPPORTED |
| Provider execution | Provider/recognizer families occur | UNKNOWN | Isolation varies; complete sandboxing not proved | SUPPORTED |
| Provenance | Associations/edges/ledger-shaped records occur | UNKNOWN | Provenance integrity is not guaranteed | SUPPORTED |
| Policy | Explicit in v0.7.1 | UNKNOWN | Policy objects do not prove enforcement completeness | SUPPORTED / UNKNOWN |

## Historical, retrospective, current

1. **Historical architecture:** reconstructed snapshot source and direct state.
2. **Retrospective interpretation:** Protocol-v3 and provisional Protocol-v8 models.
3. **Current architecture:** current planning documents.

Evidence never flows backward from 2 or 3 to prove 1. Security-shaped code is classified as a mechanism unless runtime and contract evidence proves a guarantee.
