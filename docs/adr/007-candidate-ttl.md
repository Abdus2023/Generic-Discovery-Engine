# ADR 007 — Candidate TTL (bounded frontier freshness)

**Status:** accepted (v0.7.7)  
**Transcript:** Roadmap Phase 1 “candidate expiration (TTL beyond retry delay — not yet)” + Decision sweep v0.7.7  
**Code:** `CONFIG.candidateTTL`, `KnowledgeBase.claimNextCandidate()` TTL sweep, `markSkipped(...,'ttl-expired')`, `recordDiagnostic('candidate-ttl-expired')`

## Context
`maxCandidates 750 live` prevents unbounded heap, but a stale `queued` candidate can sit forever if the scheduler prefers higher-priority work or if the tab is throttled (150 ms/origin, concurrency 4). Without freshness, the frontier can be clogged by low-value, aged URLs discovered at bootstrap (e.g., 500 links from a SPA shell). Retry already has `nextAttemptAt` + `maxRetries`, but that only governs failed attempts, not successful queuing.

## Decision
- Add `CONFIG.candidateTTL: 0` (disabled by default, ms when >0). When `candidate.createdAt + TTL < now()`, the next `claimNextCandidate()` sweeps the candidate before sorting and marks it `skipped` with `skipReason ttl-expired` (visited-scoped), emitting `candidate-ttl-expired` diagnostic `{id, target, age, ttl}`.
- Sweep happens synchronously inside `claimNextCandidate()` before `eligible.sort(...)`, so liveCount is freed immediately and `addCandidate()` can admit fresh discoveries. No background timer; cost O(n) over ≤750 per claim (~0.05 ms).
- Ledger retains evidence (`skipped` + diagnostic); export still counts `skipped`. Disabled (`0`) preserves exact v0.7.6 behavior.

## Consequences
- **+** Frontier freshness bounded without external cron; tab idle for hours won’t claim day-old `queued` that may be 404.
- **+** Deterministic: TTL check is pure `now()`-`createdAt` comparison, proven by `property-determinism.test.js` (old vs fresh, TTL=0 no expiry, liveCount bound 500 iter).
- **−** Setting TTL too low (e.g., 5 s) would thrash on throttled origins; default 0 leaves choice to caller. Diagnostics make tuning visible.

## Links
- Tests: `tests/property-determinism.test.js` “TTL determinism” (4 cases).
- Static: `tests/verify-p0-fixes.test.js` asserts `candidateTTL/ttl-expired/candidate-ttl-expired` present.
- Perf: `PERFORMANCE_ANALYSIS.md` §8 (TTL sweep ~0.05 ms).
