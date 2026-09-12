# Historical Source Archive

This archive is the mechanical, provenance-first extraction of code and code-like material embedded in `Userscript Discovery Prototype.md` and `Continue Architecture Planning.md` across all unique source-document blobs found in fetched Git refs.

## Layer separation

1. **Raw historical source:** `raw/` contains byte-exact pinned Git blobs, including BOM and CRLF.
2. **Provenance:** `SOURCE-MANIFEST.yaml`, `SOURCE-MAP.md`, `REVISION-INVENTORY.yaml`, and `DETECTION-INVENTORY.yaml`.
3. **Derived analysis:** indexes, duplicates, near-duplicates, lineage, changes, field history, contradictions, uncertainties, report, and validation.
4. **Extraction-level reconstruction:** `reconstructed/`; always derived and non-authoritative.
5. **Historical snapshots:** `snapshots/`; exact copies, mechanical compositions, and explicitly partial alternatives remain externally labeled and range-mapped.
6. **Reconstruction analysis:** `analysis/`, the version graph/matrix, and `RECONSTRUCTION-*.yaml`/`.md` ledgers.

Every file under `artifacts/` is an exact contiguous byte slice of a raw Git blob. Fenced-artifact files contain the bytes *inside* the Markdown fence; fence labels and source positions remain in metadata. Source-split userscript containers are also retained as exact contiguous intervals, including their historical formatting anomalies. No formatter or linter was run. The local `.gitattributes` marks raw, extracted, and reconstructed payloads `-text` so Git checkout cannot rewrite their historical line endings.

## Metadata sidecars

To stay below repository file-count limits while retaining one metadata record per artifact, `SOURCE-MANIFEST.yaml` is the consolidated logical sidecar store. Its JSON serialization is valid YAML 1.2 and can be parsed with standard JSON tools. There is no artifact without a manifest record.

## Key files

- `SOURCE-MANIFEST.yaml` — complete per-artifact metadata, provenance, context, integrity, dependencies, and concurrency observations
- `SOURCE-MAP.md` — bidirectional source/artifact map
- `ARTIFACT-INDEX.yaml` — concise deterministic index
- `REVISION-INVENTORY.yaml` — blobs, every observed unchanged path occurrence, refs, rename events, and raw hashes
- `DETECTION-INVENTORY.yaml` — every fence/outside userscript/independent inline region
- `DUPLICATES.yaml` / `NEAR-DUPLICATES.yaml` — retained exact copies and mechanical similarity
- `LINEAGE.yaml` / `CHANGES.yaml` — conservative evidence-backed lineage and mechanical comparisons
- `FIELD-HISTORY.yaml` — mechanically observed model field-set changes
- `CONTRADICTIONS.md` / `UNCERTAINTIES.md` — unresolved evidence registers
- `VALIDATION.yaml` — automated integrity checks
- `EXTRACTION-REPORT.md` — final historical evolution report
- `snapshots/` — 14 evidence-supported snapshot variants, each with source, external metadata, source map, and report
- `RECONSTRUCTION-MANIFEST.yaml` — snapshot identities, classes, input hashes, evidence, dependencies, static checks, and contamination tests
- `VERSION-GRAPH.md` / `VERSION-MATRIX.md` — non-linear history and evidence-backed capability matrix
- `RECONSTRUCTION-ASSUMPTIONS.yaml`, `RECONSTRUCTION-GAPS.yaml`, `RECONSTRUCTION-CONFLICTS.yaml` — visible uncertainty accounting
- `RECONSTRUCTION-REPORT.md` / `RECONSTRUCTION-VALIDATION.yaml` — final answers and independent protocol 92–155 validation

## Reproduce and validate extraction

```sh
python3 historical-source/tools/extract.py
python3 historical-source/tools/validate.py
```

## Reproduce and validate reconstruction

```sh
python3 historical-source/tools/reconstruct.py
python3 historical-source/tools/validate_reconstruction.py
```

The reconstruction tool performs two complete in-memory/temp-directory runs and rejects byte-level nondeterminism. Static `node --check` parsing is read-only; no userscript runtime execution is performed.

The extractor is pinned to the four unique document blob revisions inventoried on 2026-09-11T13:21:04+00:00. Earlier pre-Git chat revisions are not available and are never guessed.
