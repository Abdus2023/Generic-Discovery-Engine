# ADR 010 — Lifecycle State-Machine Guard

**Status:** accepted (v0.7.8)  
**Transcript:** Roadmap Phase 1 “candidate expiration” + worker lifecycle audit v0.7.8  
**Code:** `CONFIG.lifecycle.strict`, `KnowledgeBase._validateTransition()`, all `mark*` / `queueCandidate` / `claimNextCandidate` / `retryCandidate` guards, diagnostic `lifecycle-illegal-transition`

## Context
Candidates traverse `discovered→queued→claimed→planned→acquiring→observed→recognized→expanded→completed` with branches to `skipped` (ttl/policy/budget) and `failed→queued` (retry). Before v0.7.8 the `mark*` methods set `candidate.status` without validation; a buggy caller could transition `completed→queued` or `queued→observed`, corrupting `visited`, `stats`, and `graphEdges` and violating the “at most one active owner” invariant. No test proved the allowed graph.

## Decision
- Add `CONFIG.lifecycle: { strict:false }`. When `strict:true` illegal transitions throw; when `false` they emit `lifecycle-illegal-transition` diagnostic `{id,target,from,to,allowed}` and return `true` (allow) — preserving backward behavior while making misuse observable.
- Define `allowed` table strict:
  ```
  discovered→queued, queued→claimed|skipped|failed, claimed→planned|skipped,
  planned→acquiring|completed|skipped, acquiring→observed,
  observed→recognized|completed|queued|failed, recognized→expanded,
  expanded→completed, failed→queued, completed/skipped terminal, self allowed
  ```
- Call `_validateTransition(candidate, to)` at entry of `queueCandidate`, `claimNextCandidate` (`claimed`), `markPlanned`, `markAcquiring`, `markObserved`, `markRecognized`, `markExpanded`, `markCompleted`, `markSkipped`, `markFailed`, `retryCandidate` (`queued`). Cost ~0.02 ms per mark, dominated by network.

## Consequences
- **+** Illegal `queued→observed` or `completed→queued` no longer silent; visible in `ledger/diagnostics` and in `exportData()`.
- **+** Strict mode enables model-checking in `property-lifecycle.test.js` (500 random walks over allowed edges never hit illegal).
- **−** Table is permissive for branch `planned→completed` and `observed→queued` (retry) to allow existing worker paths; future tightening to `planned→acquiring` only would require worker refactor.

## Links
- Tests: `tests/property-lifecycle.test.js` (8 invariants, strict throw, terminal, walks, happy path).
- Static: `tests/verify-p0-fixes.test.js` asserts `lifecycle/_validateTransition/lifecycle-illegal-transition/CONFIG.lifecycle` present.
- Perf: `PERFORMANCE_ANALYSIS.md` §8 (0.02 ms).
