# ADR — Architectural Decision Records

Format: **Context → Decision → Consequences → Alternatives → Links**.

New ADRs:
1. Copy `docs/adr/000-template.md` (if present) or clone `001`.
2. Number sequentially (`004-…` next).
3. Update `docs/DECISIONS.md` index.

Current ADRs (v0.7.5 — 6 ADRs):

- `001-provider-pipeline.md` — 7 providers, ordered matching, `ProviderRegistry`.
- `002-ledger.md` — 12 typed events, 5k FIFO, replayable `DecisionLedger`.
- `003-origin-controller.md` — per-origin throttle/budget, `OriginController`.
- `004-fingerprint.md` — fnv1a32 1M sample, fingerprintIndex.
- `005-mutation-batch.md` — seen Set, batch dedup.
- `006-export-schema.md` — gde-export-v8.0, ledger + coverage.

Transcript provenance: `Continue Architecture Planning.md` (92,274 lines). Runnable artifact: `dist/generic-discovery-engine.user.js`.
