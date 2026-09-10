# ADR 004 — Content Fingerprint (fnv1a32, 1M sample, Resource dedup)

**Status:** accepted (v0.7.1)  
**Transcript:** §§24–26 (lines ~65k–70k)  
**Code:** `fnv1a32()`, `makeFingerprint()`, `KnowledgeBase.fingerprintIndex`, `ResourceRecord.fingerprint`

## Context
Same URL may return different bodies over time (A/B, personalization) and different URLs may return identical bodies (mirrors, CDN). Scheduler needs to avoid re-acquiring *identical content* under different URLs and to detect when a known URL changed.

## Decision
- Fingerprint = `fnv1a32( body.slice(0, fingerprintMaxChars 1M).replace(/\s+/g,' ').trim() )` with length metadata (800 char hash `8-hex`, `length`, `sampledLength`).
- `KnowledgeBase.recordObservation()` indexes `fingerprintIndex: Map<hash, Set<url>>` and `resources` store `fingerprint`.
- `ResourceRecord.merge()` propagates `fingerprint` and `finalUrl`.
- Sampling at 1M bounds hashing cost to ~3 ms per 2M body (vs ~30 ms untruncated); whitespace normalization makes trivial formatting differences not create distinct hashes.

## Consequences
- **+** Deduplicates identical resources across origins without re-fetch.
- **+** Stable under whitespace churn; still distinguishes semantic changes.
- **−** `fnv1a32` is not cryptographic; collision theoretical but acceptable for dedup (not security).
- **−** 1M sample means two 2M bodies differing only after 1M are considered identical (rare, intentional perf trade-off; documented).

## Alternatives considered
- Full body hash: rejected (heap + CPU on 2M × 150 requests).
- Cryptographic SHA-256 via SubtleCrypto: rejected (async, not available in VM tests, slower).

## Links
- E2E: `tests/e2e-discovery-loop.test.js` asserts `fingerprintIndex` size ≥1 after 7 fetches.
- Performance: `docs/PERFORMANCE_ANALYSIS.md` §4 (hash cost).
