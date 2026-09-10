# ADR — Architectural Decision Records

Format: **Context → Decision → Consequences → Alternatives → Links**.

New ADRs:
1. Copy `docs/adr/000-template.md` (if present) or clone `001`.
2. Number sequentially (`004-…` next).
3. Update `docs/DECISIONS.md` index.

Current ADRs (v0.8.0 — 18 ADRs):

- `001-provider-pipeline.md` — 7 providers, ordered matching, `ProviderRegistry`.
- `002-ledger.md` — 12 typed events, 5k FIFO, replayable `DecisionLedger`.
- `003-origin-controller.md` — per-origin throttle/budget, `OriginController`.
- `004-fingerprint.md` — fnv1a32 1M sample, fingerprintIndex.
- `005-mutation-batch.md` — seen Set, batch dedup.
- `006-export-schema.md` — gde-export-v8.0, ledger + coverage.
- `007-candidate-ttl.md` — candidateTTL 0/off, ttl-expired sweep before sort.
- `008-origin-throttle-invariants.md` — interval / concurrency / isolation proofs.
- `009-coverage-gates.md` — check-coverage true 85/75/80, coverage:check gate.
- `010-lifecycle-state-machine.md` — strict guard + allowed table, lifecycle-illegal-transition.
- `011-concurrency-claim.md` — synchronous claim, 4-worker exclusivity, TTL/retry interleaving.
- `012-type-safety.md` — tsconfig checkJs, typecheck script, @types/node.
- `013-pattern-inference.md` — extractUrlPattern /{int} /{uuid} /{hash}, patternIndex, getPatternMetrics.
- `014-clustering.md` — clusterKey origin::pattern, clusterIndex, getClusterMetrics.
- `015-build-determinism.md` — sha256+lines, dist/.build-meta.json, verify:build.
- `016-robots-provider.md` — robots.txt Sitemap extraction, 9 providers ordered.
- `017-headers-provider.md` — Link/Location header capture, HeadersProvider.
- `018-change-detection.md` — fingerprint diff → resource-changed, changeDetection flag.

Transcript provenance: `Continue Architecture Planning.md` (92,274 lines). Runnable artifact: `dist/generic-discovery-engine.user.js`.
