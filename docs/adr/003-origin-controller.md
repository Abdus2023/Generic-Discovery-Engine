# ADR 003 — Per-Origin Throttle & Budget (2 concurrent / 150 ms / 50 per origin, 150 global)

**Status:** accepted (v0.7.1)  
**Transcript:** §§20–22 (lines ~60k–64k)  
**Code:** `OriginController`, `CONFIG.origin`, `GenericDiscoveryEngine.reserveRequestSlot()`, `Acquisition.execute()`

## Context
Without origin-aware throttling, a burst of 4 workers on the same origin could send concurrent requests that trigger IP bans or distort server logs. Verification (§4.3, §6.1) flagged “no per-origin throttle” as a robustness gap.

## Decision
- `OriginController` maintains `Map<origin, {active, requests, lastRequestAt}>`.
- Guards: `maxConcurrentPerOrigin 2`, `minRequestInterval 150 ms`, `maxRequestsPerOrigin 50`, plus global `maxRequests 150` via synchronous `reserveRequestSlot()` before `acquire()`.
- On `origin-request-budget` exhaustion the candidate is `skipped` (not retried); budget denials are ledgered (`budget-denied`).
- Budget is **per execution**: `restore()` resets `requestsReserved` to 0 each tab load (a new execution gets a fresh budget).

## Consequences
- **+** Same-origin burst is paced: E2E (7 requests, 1 origin, concurrency 2) measures ~911 ms wall (150 ms throttle dominates; 20 ms unthrottled baseline).
- **+** Global vs per-origin caps compose: large crawls cannot exceed IP-level budget even if many distinct origins are queued.
- **−** 150 ms throttle is conservative; link-dense SPA may crawl slower than user expects. Configurable but not exposed in UI yet (P2).

## Alternatives considered
- No throttle, rely on server 429: rejected (by then IP may be blocked).
- Token bucket with refill: deferred (current fixed interval is simpler and easier to verify; heap/stats remain synchronous).

## Links
- Verification: `VERIFICATION_REPORT.md` §4.3, `PERFORMANCE_ANALYSIS.md` §2 (E2E wall breakdown), `SECURITY_AUDIT.md` S-06.
- Code: `dist/generic-discovery-engine.user.js` lines ~1950–2050 (`OriginController.acquire` loop with `sleep(50)` poll).
