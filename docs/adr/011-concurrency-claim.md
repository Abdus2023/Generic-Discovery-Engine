# ADR 011 — Concurrency Claim Exclusivity

**Status:** accepted (v0.7.8)  
**Transcript:** Scheduler claim-before-await + TTL sweep v0.7.7  
**Code:** `KnowledgeBase.claimNextCandidate()` synchronous `sort → _validateTransition → status='claimed'`, `tests/property-concurrency.test.js`

## Context
`GenericDiscoveryEngine` runs `concurrency:4` workers each looping `claim → plan → acquire → observe → recognize`. The invariant “candidate has at most one active owner” depends on `claimNextCandidate()` being synchronous (claim before any `await`). No test interleaved workers with `setImmediate` to prove exclusivity under burst, nor with TTL expiries and `nextAttemptAt` windows. A regression that made `claim` async would silently duplicate acquisition.

## Decision
- Keep `claimNextCandidate()` synchronous: filter `queued|failed` + `nextAttemptAt` + `candidateTTL` sweep, sort by `effectivePriority`, mark `claimed` with `claimedAt`, add to `claimed` Set, `stats.claimed++`, return. No `await`, no `Promise`.
- Prove via `property-concurrency.test.js` (6 cases, seeded):
  1. source chunk has no `async` before `candidate.status='claimed'`
  2. 10 candidates sequential claims respect priority order, no duplicates
  3. 4 workers × `Promise.all` + `setImmediate` yield 12 distinct claims
  4. TTL expiries (old 200 ms, TTL 100) are skipped, not claimed, still exclusive
  5. `nextAttemptAt` future blocks, past allows (100 iter)
  6. 500 fuzz returns `Candidate` not `Promise`
- `verify-p0` asserts `candidate.status='claimed'` and `effectivePriority` still present.

## Consequences
- **+** Model covers burst `discovered→queued` storms (4 workers flushing) and `rAF` UI batching (0.7.6) does not affect claim.
- **+** Deterministic without real network: `setImmediate` interleaving is 0 ms, seeded LCG ensures no flake.
- **−** Mock `KBClaim` duplicates real `KB` logic; divergence risk mitigated by static grep for `claimed` + `effectivePriority`.

## Links
- Tests: `tests/property-concurrency.test.js` (6 cases).
- ADR 007 (TTL) and 010 (lifecycle) are prerequisites (TTL sweep inside claim).
