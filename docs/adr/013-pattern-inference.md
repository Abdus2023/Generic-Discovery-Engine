# ADR 013 — URL Pattern Inference (template extraction)

**Status:** accepted (v0.7.9)  
**Transcript:** Roadmap Phase 2 “URL pattern inference” + Phase 3 “candidate clustering”  
**Code:** `CONFIG.inference.patternInference`, `extractUrlPattern(url)`, `KnowledgeBase.patternIndex`, `recordPattern()`

## Context
`KnowledgeBase` deduped by `type:target` and `fingerprintIndex`, but did not recognize that `/user/123`, `/user/456`, `/user/789` are the same logical resource template. Without pattern inference the frontier of 750 appears as 750 distinct URLs, hiding that 500 are `…/user/{int}`. Operators cannot answer “how many distinct templates are we crawling?” and the scheduler cannot deprioritize over-represented patterns. The 2.2 MB transcript planned pattern inference but never shipped it.

## Decision
- Add `CONFIG.inference: { patternInference:true, clustering:true, minPatternFreq:3 }` (all on by default, `minPatternFreq` for future template suggestion).
- Implement `extractUrlPattern(url)` deterministic, no allocation beyond `URL` parse:
  - Path numeric segments `\/\d+(?=\/|$)` → `/{int}`
  - UUID `\/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}` → `/{uuid}`
  - Hex hash `\/[0-9a-f]{32,64}` → `/{hash}`
  - Query `=\d+(&|$)` → `={int}`, `=uuid`/`=hash` similarly; fallback to string replace if `URL` parse fails.
  - Respects `CONFIG.inference.patternInference` off → identity.
- Store `patternIndex: Map<pattern, count>` in `KnowledgeBase`; `recordPattern(candidate)` called from `addCandidate` after `stats.discovered++` (O(1), ~0.01 ms).
- Expose `getPatternMetrics()` → `{ size, top: sorted 20, total }` sorted descending, O(n) over ≤750 distinct patterns (~0.06 ms).

## Consequences
- **+** 500 `/user/{int}` URLs collapse to 1 pattern key, metrics show `size` distinct templates vs `total` candidates.
- **+** Deterministic: same template different ids → same pattern (500-iter property test), different structures → different patterns.
- **−** Numeric replacement is heuristic; `/v1` (API version) becomes `/{int}` but is semantic version — acceptable for clustering, documented as lossy.

## Links
- Tests: `tests/property-pattern.test.js` (7 cases: numeric, query, uuid/hash, collapse 500 iter, different structures, metrics sorted/bounded).
- Code: `extractUrlPattern`, `clusterKeyForCandidate`, `recordPattern`, `getPatternMetrics`.
