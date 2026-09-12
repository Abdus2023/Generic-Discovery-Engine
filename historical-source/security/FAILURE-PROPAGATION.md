# Failure Propagation Evolution

`DERIVED SECURITY MODEL — NOT HISTORICAL SOURCE`

Every graph edge is event-scoped. A catch path is not promoted to a fault-isolation guarantee.

```text
Failure Source → Detection → Local Handling or Propagation → Scheduler/Caller → Scan Result
```

## Containment levels

- **F0** — CATASTROPHIC_OR_PROCESS_WIDE
- **F1** — ENGINE_WIDE
- **F2** — SCAN_WIDE
- **F3** — WORKER_WIDE
- **F4** — CANDIDATE_WIDE
- **F5** — PROVIDER_WIDE
- **F6** — OPERATION_LOCAL
- **UNKNOWN** — STOP_BOUNDARY_NOT_PROVED

## Per-version summary

| Snapshot | Events | Local F4–F6 | Propagating | Unknown stop |
|---|---|---|---|---|
| snapshot-0001 | 9 | 5 | 4 | 4 |
| snapshot-0003 | 11 | 7 | 4 | 4 |
| snapshot-0005 | 12 | 8 | 4 | 4 |
| snapshot-0006 | 18 | 12 | 4 | 6 |
| snapshot-0008 | 22 | 18 | 4 | 4 |
| snapshot-0007 | 28 | 20 | 7 | 8 |
| snapshot-0009 | 19 | 16 | 0 | 3 |
| snapshot-0011 | 23 | 19 | 1 | 4 |
| snapshot-0010 | 15 | 12 | 0 | 3 |
| snapshot-0012 | 24 | 20 | 1 | 4 |
| snapshot-0013 | 14 | 9 | 0 | 5 |
| snapshot-0014 | 16 | 10 | 0 | 6 |
