# ADR 005 — Mutation Observer Batch Dedup

**Status:** accepted (v0.7.2 P1-2)  
**Transcript:** §28 + verification supplement §1  
**Code:** `GenericDiscoveryEngine.installMutationObserver()`, `observeCurrentDom()` with `seen Set<type:canonical>`, `tryDiscover()`

## Context
SPA virtualized lists mutate `document` hundreds of times per second, often re-inserting the same `<a href>` nodes. Pre-batch code called `discover()` per element per mutation flush, allocating `Candidate` objects that immediately hit `candidateKeys` dedup. On a feed with 500 identical links, each 250 ms flush created ~500 allocations → GC pressure, `candidate-cap-reached` noise.

## Decision
- Mutations debounced `mutationDebounce 250 ms`, observing `subtree:childList:attributes(href,src,action)`.
- Each `observeCurrentDom()` flush creates a local `seen = Set<string>` of `type:canonicalUrl`.
- `tryDiscover(target, type, ...)` canonicalizes, builds `key`, skips if `seen.has(key)` or `key==null`; otherwise `seen.add(key)` then `discover()`.
- `discover()` still does global `candidateKeys`/`visited` checks; batch is an early micro-optimization, not a correctness gate.

## Consequences
- **+** 500 dup `href` per flush → 1 `discover()` call (~0.3 ms measured).
- **+** No behavior change for unique URLs; still 1:1.
- **−** `seen` is per-flush, not cross-flush; same URL in two separate flushes will still be `discover()`-ed twice then globally deduped (acceptable: flush window is 250 ms).

## Alternatives considered
- No batch, rely on global dedup: rejected (alloc pressure).
- Persistent `seen` across flushes: rejected (would hide legitimate re-appearance after navigation without clearing).

## Links
- Verification: `VERIFICATION_SUPPLEMENT_v0.7.2.md` §1 P1-2, `PERFORMANCE_ANALYSIS.md` §5 (batch 0.3 ms).
- Code: `dist/generic-discovery-engine.user.js` lines ~4200–4250.
