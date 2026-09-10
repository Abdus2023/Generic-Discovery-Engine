# ADR 008 — Origin Throttle Invariants (per-origin budget & interval)

**Status:** accepted (v0.7.7)  
**Transcript:** ADR 003 (origin controller) + verification sweep v0.7.7  
**Code:** `CONFIG.origin {maxRequestsPerOrigin:50, maxConcurrentPerOrigin:2, minRequestInterval:150}`, `OriginController`, `AcquisitionPolicy.plan()` origin guards

## Context
ADR 003 introduced per-origin throttling (2 concurrent, 150 ms interval, 50 per origin, 150 global) but invariants were only exercised via E2E (7-node crawl, mocked 5 ms). No property proof that `minRequestInterval` is monotonic, that concurrency is respected under burst, or that isolation holds per origin. A regression could let a burst of `html→json→xml` discoveries hammer the same origin.

## Decision
- Formalize invariants as `property-determinism.test.js` with mocked `OriginController`:
  - `minRequestInterval` monotonic: after `recordStart(origin)` `canRequest(origin)` is false until `now()-lastAt ≥ 150`.
  - `maxConcurrentPerOrigin 2`: two `recordStart` blocks third; `recordEnd` frees one.
  - Isolation: `a` blocked does not block `b`.
- Keep implementation unchanged (no code delta); invariants are verification-only. `CONFIG.origin` remains the single source of truth, checked in both `plan()` (policy) and `OriginController` (runtime gate).

## Consequences
- **+** Deterministic throttle proven independent of network mock wall (911 ms throttled vs 20 ms unthrottled remain observational, but invariants now run at 0 ms in mocks).
- **+** Documents that throttle is additive safety, not just performance: protects origin + tab + ledger (burst discoveries still coalesce via `emittedForObservation`).
- **−** Mocked controller duplicates real code; divergence risk mitigated by static `grep` for `maxConcurrentPerOrigin`/`minRequestInterval` in `verify-p0`.

## Links
- Tests: `tests/property-determinism.test.js` “Origin throttle invariants” (3 cases).
- ADR 003 remains normative for values; this ADR adds invariants.
- Perf: `PERFORMANCE_ANALYSIS.md` §2 (150 ms wall) and §8 (TTL sweep).
