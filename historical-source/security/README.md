# Historical Failure, Security & Trust-Boundary Archaeology

Protocol-v8 derived corpus. Historical source is never modified.

## Scope

- Semantic snapshots: 12
- Partial variants retained only as uncertainty: 2
- Versions: v0.1.0, v0.2.0, v0.3.0, v0.4.0, v0.5.0, v0.6.0, v0.7.1
- Runtime/security tests recovered by this protocol: none
- Failure events are static source paths, not production incidents.
- Prerequisite status: BLOCKED: one or more required v1–v7 inputs missing/failed; corpus is provisional.

## Trust rules

1. Mechanism never silently becomes guarantee.
2. Actual control flow determines path-local containment.
3. Synchronous JavaScript claim sequences are not generalized across `await`.
4. Potential resource/race/integrity modes are not called demonstrated failures.
5. Same-version variants remain alternatives; adjacent versions are comparisons, not lineage.
6. Current/proposed security concepts are temporally isolated.

The main report is `SECURITY-ARCHAEOLOGY-REPORT.md`. Machine ledgers retain exact source evidence IDs; `EVIDENCE.yaml` resolves them to byte/line ranges and hashes.
