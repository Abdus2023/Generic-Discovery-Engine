# ADR 002 — Deterministic Decision Ledger (12 typed events, 5k FIFO)

**Status:** accepted (v0.7.1)  
**Transcript:** §§18–24 (lines ~58k–65k)  
**Code:** `DecisionLedger` (dist lines ~530–830), `GenericDiscoveryEngine.ledger`, `exportData().ledger`

## Context
Pre-ledger scheduling (`v0.1`) logged only `console.log`. Debugging why a URL was skipped required re-reading code. The verification report (§4.5) asked for “why was this candidate denied?” to be first-class and replayable.

## Decision
- Ledger records **decisions, not network outcomes**. Network is inherently non-deterministic; ledger replay answers “what policy chose”, not “what bytes arrived”.
- 12 typed `record*` methods: `candidate-discovered/enqueued/claimed`, `acquisition-planned/policy-denied/budget-denied/slot-granted`, `request-started/completed`, `observation-recorded`, `provider-recognized`, `discovery-emitted`, `candidate-completed/skipped/retried`, plus `diagnostic:*`.
- FIFO cap `persistedLedgerEvents 5000`, `sequence` monotonic, `export()/restore()` for `exportData()` and `GM_setValue` persistence.
- Every denial carries `reason` (`url-not-allowed`, `non-get-method`, `max-depth`, `forms-disabled`, …) and is mirrored as `diagnostic:policy-denied`.

## Consequences
- **+** Auditability: `gde-*.json` export contains full `ledger.events` + `diagnostics` + `graphEdges`; a post-mortem can replay the frontier without re-fetching.
- **+** UI compatibility: `updateUI` shows `ledger=N` without traversing the ledger.
- **−** `diagnostic:*` namespace is open-ended; consumers must filter by prefix. P2 recommends a typed enum (not yet).
- **−** Ledger does not snapshot `CONFIG` per event (only `policyVersion`); full reproducibility needs `exportData().config`.

## Alternatives considered
- Log-only: rejected (lost after reload).
- Full HTTP replay: rejected (network not reproducible; violates privacy + quota).

## Links
- Verification: `VERIFICATION_REPORT.md` §§2.2/11, `VERIFICATION_SUPPLEMENT_v0.7.2.md` §3 (behavioral tests for ledger chain).
- E2E: `e2e-discovery-loop.test.js` asserts ledger chain `discovered→claimed→planned→started→completed→recognized→emitted→completed` + `discovery-deduped`.
