# Mechanical Historical Reconstruction Report

## Governing result

A smaller exact snapshot was preferred to a larger fictional one. Snapshot source was copied or composed only from extraction artifacts. Architecture-only material was never converted into source.

## Snapshot inventory

| Snapshot | Historical version | Variant | Reconstruction | Completeness | Executability | SHA-256 |
|---|---|---|---|---|---|---|
| snapshot-0001 | v0.1.0 | mechanically-composed | MECHANICALLY_COMPOSED | 1.0 | LIKELY_EXECUTABLE | `5ae5a2bbeacc88827794c0052a27101bf29d4c9dd3aa4b4c96b53667ca0537cd` |
| snapshot-0002 | v0.1.0 | flattened-alternative | PARTIAL | UNKNOWN | NON_EXECUTABLE | `40409ec314b9062705a8874c327e796d8bb5635a5c7d935edfd6119daf937722` |
| snapshot-0003 | v0.2.0 | mechanically-composed | MECHANICALLY_COMPOSED | 1.0 | LIKELY_EXECUTABLE | `b7586963c62b827291c574118a9f25e22b67f5e9374b72a9fc2b58d4ca4ea28e` |
| snapshot-0004 | v0.2.0 | flattened-alternative | PARTIAL | UNKNOWN | NON_EXECUTABLE | `457fcf715e58cd59dec9157ace098b4d9ae499d9aa079154ca472ff8fdaf57b0` |
| snapshot-0005 | v0.3.0 | only-evidenced-complete-occurrence | EXACT | 1.0 | LIKELY_EXECUTABLE | `f52fccf69f9d89c5d4269de784479657e1c2baaca3d1ff5d7d4b07887ad156e3` |
| snapshot-0006 | v0.4.0 | variant-a | EXACT | 1.0 | LIKELY_EXECUTABLE | `9239a85bf7e040427adf93d4380d9ed28ceaf908b36201c7ca171150f94256b8` |
| snapshot-0007 | v0.5.0 | variant-a | EXACT | 1.0 | LIKELY_EXECUTABLE | `a55a835ef0b1274db71e4019616b8ac8b12f67a3b96d050e42bc3d8eca9ed0ab` |
| snapshot-0008 | v0.4.0 | variant-b | EXACT | 1.0 | LIKELY_EXECUTABLE | `c60c3278d160ed1ba6e8b4254d26cab291a3df64a4e986234cfc1fa7f897b783` |
| snapshot-0009 | v0.5.0 | variant-b | EXACT | 1.0 | NON_EXECUTABLE | `f71b190c334069da6e4ae82a8e8d27383826b5e333de4ca3cb1f72de19d9b1cd` |
| snapshot-0010 | v0.6.0 | variant-a | EXACT | 1.0 | LIKELY_EXECUTABLE | `3a3aa26747ff5105ce52578133e8c8932edb2ec0c54246853ea0b8938ba3118c` |
| snapshot-0011 | v0.5.0 | variant-c | EXACT | 1.0 | LIKELY_EXECUTABLE | `644e9cf006441cf81e407e47f4b37b8ff12d91a65e738595de5eabadee6ec390` |
| snapshot-0012 | v0.6.0 | variant-b | EXACT | 1.0 | LIKELY_EXECUTABLE | `414ad2bfc4df241d85b20367a4c8764187155f9cfdf8daacd5fb7e773477eed1` |
| snapshot-0013 | v0.6.0 | variant-c | EXACT | 1.0 | LIKELY_EXECUTABLE | `8b0987792f6182090942ff5959eb8ae1e5cbf5386c45632c08b1f31742bf14d3` |
| snapshot-0014 | v0.7.1 | only-evidenced-complete-occurrence | EXACT | 1.0 | LIKELY_EXECUTABLE | `00c676fabe2d0b6c0e469e03171e00971a7291c7da404b624751fa86c19d39bb` |

## Questions required by the protocol

### Which versions can be reconstructed exactly?

v0.3.0, v0.4.0, v0.5.0, v0.6.0, v0.7.1 have **10 exact occurrence snapshots**. Repeated v0.4.0, v0.5.0, and v0.6.0 implementations remain separate variants; no canonical winner was selected.

### Which can be mechanically composed?

v0.1.0 and v0.2.0 each have one **MECHANICALLY_COMPOSED** snapshot assembled from explicit, ordered source ranges after removing only Markdown fence delimiters.

### Which are only partial?

v0.1.0 and v0.2.0 each also have one transformed/flattened **PARTIAL** alternative. Their completeness is `UNKNOWN`; explicit non-historical gap markers identify unrecoverable formatting and boundaries.

### Which are impossible to reconstruct as implementation source?

v0.7.0, v0.8, v0.9, v0.10, v0.11, v0.12, v0.13, v0.14, v0.15, v0.16, v0.17, v0.18, v0.19, v0.20, v0.21, v0.22, v0.23, v0.24, v0.25, v0.26, v0.27, v0.28, v0.29, v0.30, v0.31, v0.32, v0.33, v0.34, v0.35. These labels have design, pseudocode, interface, example, or prose evidence but no complete implementation source. No version directory was created for them.

### Which source fragments remain orphaned?

**0 independently implemented root artifacts** are orphaned from the recoverable userscript snapshots. Nested component artifacts are already contained by their parent userscripts. Future pseudocode/design artifacts remain design evidence rather than orphan implementation source. Exact archive copies are duplicate occurrences, not new snapshots.

### Which implementations evolved?

Evidence-backed edges are shown in `VERSION-GRAPH.md`. Detailed source, symbol, API, data-model, capability, provider, acquisition, and concurrency changes are stored per snapshot and under `analysis/`.

### Which implementations were abandoned?

No abandonment intent is proved. `62` symbol disappearances across linked source pairs are recorded as observations with abandonment `UNKNOWN`.

### Which features were designed but never evidenced as implemented?

The traceability ledger leaves the WASM module capability, SQLite persistence adapter, Rust runtime/agent platform, and distributed coordination protocol as **DESIGNED** or **PROPOSED**, not implemented source.

### Which versions contain unresolved conflicts?

v0.1.0, v0.2.0, v0.4.0, v0.5.0, and v0.6.0 contain alternative source representations/implementations. The **5** conflict groups remain unresolved and unmerged.

### Which reconstructions depend on assumptions?

None. There are **0 unresolved assumptions** and no executable snapshot is assumption-dependent.

### Which snapshots are executable?

`node --check` supports **11 LIKELY_EXECUTABLE** classifications. **3** snapshots are `NON_EXECUTABLE` as recovered. This is static parsing only, not browser/userscript runtime verification.

### Which were actually executed historically?

**0 are proved historically executed.** Historical execution remains `UNKNOWN` for all snapshots; runtime validation was not performed.

## Integrity and contamination controls

- Every copied output range maps to an extraction artifact in `source-map.yaml`.
- Every reconstructed source has a SHA-256.
- Exact snapshots are byte-identical to their direct source artifacts.
- Composed snapshots reproduce explicit source ranges and exclude only fence delimiters.
- No source artifact from another/later embedded version was inserted.
- No future architecture artifact was inserted into a historical snapshot.
- No patch reconstruction was attempted because no authoritative historical patch artifact was available.
- Runtime execution was not performed.

## HISTORICAL RECONSTRUCTION STATUS

EXACT:
10

MECHANICALLY_COMPOSED:
2

PATCH_RECONSTRUCTED:
0

PARTIAL:
2

INFERRED:
0

UNKNOWN:
29

TEMPORAL_CONFLICTS:
0

RECONSTRUCTION_CONFLICTS:
5

MISSING_SOURCE_REGIONS:
31

UNRESOLVED_ASSUMPTIONS:
0

No historical source was modified.  
No missing source was silently invented.  
No later implementation was retroactively inserted.  
No architectural proposal was treated as implementation without evidence.
