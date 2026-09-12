# Data Integrity History

`DERIVED SECURITY MODEL — NOT HISTORICAL SOURCE`

POSSIBLE is not OBSERVED; PREVENTED is path-local unless stated otherwise. Persistence integrity is included in PERSISTENCE-INTEGRITY.yaml.

| Snapshot | Condition | Classification | Scope | Caveat |
|---|---|---|---|---|
| snapshot-0001 | orphaned observations | POSSIBLE | RECOVERED_STATIC_PATHS | No foreign-key enforcement is evidenced. |
| snapshot-0001 | orphaned discoveries | POSSIBLE | RECOVERED_STATIC_PATHS | Identifiers are stored but referential enforcement is not proved. |
| snapshot-0001 | duplicate candidates | PREVENTED | RECOVERED_STATIC_PATHS | Local key/visited path only. |
| snapshot-0001 | lost provenance | POSSIBLE | RECOVERED_STATIC_PATHS | Presence of fields does not guarantee preservation at every boundary. |
| snapshot-0001 | partial records | POSSIBLE | RECOVERED_STATIC_PATHS | Incremental mutable object construction and persistence are present. |
| snapshot-0001 | inconsistent status | POSSIBLE | RECOVERED_STATIC_PATHS | Multiple mutation paths; no exhaustive state machine verification. |
| snapshot-0001 | stale claims | POSSIBLE | RECOVERED_STATIC_PATHS | Only handled completion/failure paths are covered. |
| snapshot-0003 | orphaned observations | POSSIBLE | RECOVERED_STATIC_PATHS | No foreign-key enforcement is evidenced. |
| snapshot-0003 | orphaned discoveries | POSSIBLE | RECOVERED_STATIC_PATHS | Identifiers are stored but referential enforcement is not proved. |
| snapshot-0003 | duplicate candidates | PREVENTED | RECOVERED_STATIC_PATHS | Local key/visited path only. |
| snapshot-0003 | lost provenance | POSSIBLE | RECOVERED_STATIC_PATHS | Presence of fields does not guarantee preservation at every boundary. |
| snapshot-0003 | partial records | POSSIBLE | RECOVERED_STATIC_PATHS | Incremental mutable object construction and persistence are present. |
| snapshot-0003 | inconsistent status | POSSIBLE | RECOVERED_STATIC_PATHS | Multiple mutation paths; no exhaustive state machine verification. |
| snapshot-0003 | stale claims | PREVENTED | RECOVERED_STATIC_PATHS | Only handled completion/failure paths are covered. |
| snapshot-0005 | orphaned observations | POSSIBLE | RECOVERED_STATIC_PATHS | No foreign-key enforcement is evidenced. |
| snapshot-0005 | orphaned discoveries | POSSIBLE | RECOVERED_STATIC_PATHS | Identifiers are stored but referential enforcement is not proved. |
| snapshot-0005 | duplicate candidates | PREVENTED | RECOVERED_STATIC_PATHS | Local key/visited path only. |
| snapshot-0005 | lost provenance | POSSIBLE | RECOVERED_STATIC_PATHS | Presence of fields does not guarantee preservation at every boundary. |
| snapshot-0005 | partial records | POSSIBLE | RECOVERED_STATIC_PATHS | Incremental mutable object construction and persistence are present. |
| snapshot-0005 | inconsistent status | POSSIBLE | RECOVERED_STATIC_PATHS | Multiple mutation paths; no exhaustive state machine verification. |
| snapshot-0005 | stale claims | PREVENTED | RECOVERED_STATIC_PATHS | Only handled completion/failure paths are covered. |
| snapshot-0006 | orphaned observations | POSSIBLE | RECOVERED_STATIC_PATHS | No foreign-key enforcement is evidenced. |
| snapshot-0006 | orphaned discoveries | POSSIBLE | RECOVERED_STATIC_PATHS | Identifiers are stored but referential enforcement is not proved. |
| snapshot-0006 | duplicate candidates | PREVENTED | RECOVERED_STATIC_PATHS | Local key/visited path only. |
| snapshot-0006 | lost provenance | POSSIBLE | RECOVERED_STATIC_PATHS | Presence of fields does not guarantee preservation at every boundary. |
| snapshot-0006 | partial records | POSSIBLE | RECOVERED_STATIC_PATHS | Incremental mutable object construction and persistence are present. |
| snapshot-0006 | inconsistent status | POSSIBLE | RECOVERED_STATIC_PATHS | Multiple mutation paths; no exhaustive state machine verification. |
| snapshot-0006 | stale claims | PREVENTED | RECOVERED_STATIC_PATHS | Only handled completion/failure paths are covered. |
| snapshot-0008 | orphaned observations | POSSIBLE | RECOVERED_STATIC_PATHS | No foreign-key enforcement is evidenced. |
| snapshot-0008 | orphaned discoveries | POSSIBLE | RECOVERED_STATIC_PATHS | Identifiers are stored but referential enforcement is not proved. |
| snapshot-0008 | duplicate candidates | PREVENTED | RECOVERED_STATIC_PATHS | Local key/visited path only. |
| snapshot-0008 | lost provenance | POSSIBLE | RECOVERED_STATIC_PATHS | Presence of fields does not guarantee preservation at every boundary. |
| snapshot-0008 | partial records | POSSIBLE | RECOVERED_STATIC_PATHS | Incremental mutable object construction and persistence are present. |
| snapshot-0008 | inconsistent status | POSSIBLE | RECOVERED_STATIC_PATHS | Multiple mutation paths; no exhaustive state machine verification. |
| snapshot-0008 | stale claims | PREVENTED | RECOVERED_STATIC_PATHS | Only handled completion/failure paths are covered. |
| snapshot-0007 | orphaned observations | POSSIBLE | RECOVERED_STATIC_PATHS | No foreign-key enforcement is evidenced. |
| snapshot-0007 | orphaned discoveries | POSSIBLE | RECOVERED_STATIC_PATHS | Identifiers are stored but referential enforcement is not proved. |
| snapshot-0007 | duplicate candidates | PREVENTED | RECOVERED_STATIC_PATHS | Local key/visited path only. |
| snapshot-0007 | lost provenance | POSSIBLE | RECOVERED_STATIC_PATHS | Presence of fields does not guarantee preservation at every boundary. |
| snapshot-0007 | partial records | POSSIBLE | RECOVERED_STATIC_PATHS | Incremental mutable object construction and persistence are present. |
| snapshot-0007 | inconsistent status | POSSIBLE | RECOVERED_STATIC_PATHS | Multiple mutation paths; no exhaustive state machine verification. |
| snapshot-0007 | stale claims | PREVENTED | RECOVERED_STATIC_PATHS | Only handled completion/failure paths are covered. |
| snapshot-0009 | orphaned observations | POSSIBLE | RECOVERED_STATIC_PATHS | No foreign-key enforcement is evidenced. |
| snapshot-0009 | orphaned discoveries | POSSIBLE | RECOVERED_STATIC_PATHS | Identifiers are stored but referential enforcement is not proved. |
| snapshot-0009 | duplicate candidates | PREVENTED | RECOVERED_STATIC_PATHS | Local key/visited path only. |
| snapshot-0009 | lost provenance | POSSIBLE | RECOVERED_STATIC_PATHS | Presence of fields does not guarantee preservation at every boundary. |
| snapshot-0009 | partial records | POSSIBLE | RECOVERED_STATIC_PATHS | Incremental mutable object construction and persistence are present. |
| snapshot-0009 | inconsistent status | POSSIBLE | RECOVERED_STATIC_PATHS | Multiple mutation paths; no exhaustive state machine verification. |
| snapshot-0009 | stale claims | PREVENTED | RECOVERED_STATIC_PATHS | Only handled completion/failure paths are covered. |
| snapshot-0011 | orphaned observations | POSSIBLE | RECOVERED_STATIC_PATHS | No foreign-key enforcement is evidenced. |
| snapshot-0011 | orphaned discoveries | POSSIBLE | RECOVERED_STATIC_PATHS | Identifiers are stored but referential enforcement is not proved. |
| snapshot-0011 | duplicate candidates | PREVENTED | RECOVERED_STATIC_PATHS | Local key/visited path only. |
| snapshot-0011 | lost provenance | POSSIBLE | RECOVERED_STATIC_PATHS | Presence of fields does not guarantee preservation at every boundary. |
| snapshot-0011 | partial records | POSSIBLE | RECOVERED_STATIC_PATHS | Incremental mutable object construction and persistence are present. |
| snapshot-0011 | inconsistent status | POSSIBLE | RECOVERED_STATIC_PATHS | Multiple mutation paths; no exhaustive state machine verification. |
| snapshot-0011 | stale claims | PREVENTED | RECOVERED_STATIC_PATHS | Only handled completion/failure paths are covered. |
| snapshot-0010 | orphaned observations | POSSIBLE | RECOVERED_STATIC_PATHS | No foreign-key enforcement is evidenced. |
| snapshot-0010 | orphaned discoveries | POSSIBLE | RECOVERED_STATIC_PATHS | Identifiers are stored but referential enforcement is not proved. |
| snapshot-0010 | duplicate candidates | PREVENTED | RECOVERED_STATIC_PATHS | Local key/visited path only. |
| snapshot-0010 | lost provenance | POSSIBLE | RECOVERED_STATIC_PATHS | Presence of fields does not guarantee preservation at every boundary. |
| snapshot-0010 | partial records | POSSIBLE | RECOVERED_STATIC_PATHS | Incremental mutable object construction and persistence are present. |
| snapshot-0010 | inconsistent status | POSSIBLE | RECOVERED_STATIC_PATHS | Multiple mutation paths; no exhaustive state machine verification. |
| snapshot-0010 | stale claims | PREVENTED | RECOVERED_STATIC_PATHS | Only handled completion/failure paths are covered. |
| snapshot-0012 | orphaned observations | POSSIBLE | RECOVERED_STATIC_PATHS | No foreign-key enforcement is evidenced. |
| snapshot-0012 | orphaned discoveries | POSSIBLE | RECOVERED_STATIC_PATHS | Identifiers are stored but referential enforcement is not proved. |
| snapshot-0012 | duplicate candidates | PREVENTED | RECOVERED_STATIC_PATHS | Local key/visited path only. |
| snapshot-0012 | lost provenance | POSSIBLE | RECOVERED_STATIC_PATHS | Presence of fields does not guarantee preservation at every boundary. |
| snapshot-0012 | partial records | POSSIBLE | RECOVERED_STATIC_PATHS | Incremental mutable object construction and persistence are present. |
| snapshot-0012 | inconsistent status | POSSIBLE | RECOVERED_STATIC_PATHS | Multiple mutation paths; no exhaustive state machine verification. |
| snapshot-0012 | stale claims | PREVENTED | RECOVERED_STATIC_PATHS | Only handled completion/failure paths are covered. |
| snapshot-0013 | orphaned observations | POSSIBLE | RECOVERED_STATIC_PATHS | No foreign-key enforcement is evidenced. |
| snapshot-0013 | orphaned discoveries | POSSIBLE | RECOVERED_STATIC_PATHS | Identifiers are stored but referential enforcement is not proved. |
| snapshot-0013 | duplicate candidates | PREVENTED | RECOVERED_STATIC_PATHS | Local key/visited path only. |
| snapshot-0013 | lost provenance | POSSIBLE | RECOVERED_STATIC_PATHS | Presence of fields does not guarantee preservation at every boundary. |
| snapshot-0013 | partial records | POSSIBLE | RECOVERED_STATIC_PATHS | Incremental mutable object construction and persistence are present. |
| snapshot-0013 | inconsistent status | POSSIBLE | RECOVERED_STATIC_PATHS | Multiple mutation paths; no exhaustive state machine verification. |
| snapshot-0013 | stale claims | PREVENTED | RECOVERED_STATIC_PATHS | Only handled completion/failure paths are covered. |
| snapshot-0014 | orphaned observations | POSSIBLE | RECOVERED_STATIC_PATHS | No foreign-key enforcement is evidenced. |
| snapshot-0014 | orphaned discoveries | POSSIBLE | RECOVERED_STATIC_PATHS | Identifiers are stored but referential enforcement is not proved. |
| snapshot-0014 | duplicate candidates | PREVENTED | RECOVERED_STATIC_PATHS | Local key/visited path only. |
| snapshot-0014 | lost provenance | POSSIBLE | RECOVERED_STATIC_PATHS | Presence of fields does not guarantee preservation at every boundary. |
| snapshot-0014 | partial records | POSSIBLE | RECOVERED_STATIC_PATHS | Incremental mutable object construction and persistence are present. |
| snapshot-0014 | inconsistent status | POSSIBLE | RECOVERED_STATIC_PATHS | Multiple mutation paths; no exhaustive state machine verification. |
| snapshot-0014 | stale claims | POSSIBLE | RECOVERED_STATIC_PATHS | Only handled completion/failure paths are covered. |
