# ADR — Architectural Decision Records

Format: **Context → Decision → Consequences → Alternatives → Links**.

New ADRs:
1. Copy `docs/adr/000-template.md` (if present) or clone `001`.
2. Number sequentially (`004-…` next).
3. Update `docs/DECISIONS.md` index.

Current ADRs (v1.3.0 — 28 ADRs):

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
- `019-modular-prelude.md` — src/ 7-file mirror, config/utils extracts, verify:build src check.
- `020-export-hardening.md` — sorted queuedByType, coverage patternCount/clusterCount, export inference block.
- `021-framework-bundler.md` — src/header.txt + 7 modules → dist bundler, 5875 lines 8c734… deterministic.
- `022-pattern-guided-revisit.md` — suggestPatternCandidates + getChangedResources, revisitChanged/patternGuided adaptive re-queue.
- `023-stable-1.0.md` — 1.0 stable, package 1.0.0 header 1.0.0, 22 ADRs 126/126 5977 9b2b68…
- `024-lazy-providers-esbuild.md` — lazy ProviderRegistry + esbuild minify + provider metrics, 6076 lines 6dcfa8… 135/135
- `025-sitemap-openapi-providers.md` — SitemapIndex + OpenAPI providers, 11-provider pipeline, 6214 lines 344b9c… 143/143
- `026-bundle-analyze.md` — bundle analyze (provider size breakdown + esbuild metafile), 19.1% provider ratio
- `027-wellknown-manifest-providers.md` — WellKnown + Manifest providers, 13-provider pipeline, 6344 lines bb0453… 150/150
- `028-esm-bundle-proof.md` — ESM bundle proof (esbuild bundle+metafile, tree-shaking pipeline)

Transcript provenance: `Continue Architecture Planning.md` (92,274 lines). Runnable artifact: `dist/generic-discovery-engine.user.js` (v1.3.0, 6,344 lines) + `dist/generic-discovery-engine.min.js` (63k 32.5%) + `dist/generic-discovery-engine.esm.js` (267B) + bundle analyze 21.6% built from `src/` 7 modules.
