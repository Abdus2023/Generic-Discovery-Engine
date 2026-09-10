# ADR 014 — Candidate Clustering (origin + pattern)

**Status:** accepted (v0.7.9)  
**Transcript:** Phase 3 “candidate clustering”  
**Code:** `clusterKeyForCandidate(candidate)`, `KnowledgeBase.clusterIndex: Map<origin::pattern, count>`, `getClusterMetrics()`

## Context
Pattern inference alone gives `https://a.example/user/{int}` but does not separate `https://a.example/user/{int}` from `https://b.example/user/{int}`. Per-origin budget (`OriginController` 50/origin, 2 concurrent, 150 ms) already partitions by origin, but `getCoverageMetrics` only showed `queuedByType` and `frontierSize`. No metric showed “which origin+template is dominating the frontier?” A burst of `html` discoveries from `sitemap.xml` could fill 750 with `https://cdn.example/asset/{hash}` and starve other origins.

## Decision
- Add `clusterKeyForCandidate(candidate)` → `${origin}::${pattern}` where `origin` is `candidate.origin || originOf(target) || 'unknown'` and `pattern` is `extractUrlPattern(target)`. Respects `CONFIG.inference.clustering` off → not recorded.
- Store `clusterIndex: Map<clusterKey, count>` in `KnowledgeBase` alongside `patternIndex`; `recordPattern` increments both atomically when candidate is added (not when `visited` deduped).
- Expose `getClusterMetrics()` → `{ size, top: sorted 20, total }` sorted descending, O(n) over ≤750 clusters (~0.06 ms).
- No scheduler change yet; metrics are observable via `exportData` future and via `getClusterMetrics` for UI/persistence.

## Consequences
- **+** Operators see top clusters e.g., `https://a.example::https://a.example/user/{int} 200` vs `https://b.example::https://b.example/api/{int} 15`, enabling future deprioritization of over-represented clusters.
- **+** Deterministic and bounded: same origin+pattern → same key, different origin → different key (property test).
- **−** `clusterIndex` doubles counting vs `patternIndex` but both are O(750) Maps (~100 B per entry, <100 KB).

## Links
- Tests: `tests/property-pattern.test.js` “clustering groups by origin+pattern” (seeded 200, size ≤2, total 200, sorted).
- Code: `clusterKeyForCandidate`, `recordPattern`, `getClusterMetrics`.
