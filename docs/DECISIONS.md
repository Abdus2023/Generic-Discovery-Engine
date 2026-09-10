# Architecture Decisions — Index

> Source transcript: [`Continue Architecture Planning.md`](../Continue%20Architecture%20Planning.md) (2.2 MB, 92,274 lines, 12 userscript iterations v0.1.0→v0.7.1).  This index is the **P2-10 hygiene split** (v0.7.4) that extracts the durable decisions into ADRs without deleting the transcript.

## How to use this file
- Each ADR is a one-page record: **Context → Decision → Consequences → Alternatives → Links**.
- The transcript remains the provenance; ADRs are the normative summary.
- New decisions get a new `docs/adr/NNN-title.md` and are linked here.

## Decisions extracted (v0.7.5 — 6 ADRs)

| ADR | Title | Status | Transcript range | Code |
|-----|-------|--------|------------------|------|
| [001](adr/001-provider-pipeline.md) | Provider pipeline (7 providers, ordered matching) | ✅ accepted | §§7–23, lines ~45k–58k | `Provider`, `ProviderRegistry`, `Html/Json/Xml/Css/JS/Binary/Text` |
| [002](adr/002-ledger.md) | Deterministic Decision Ledger (12 typed events, 5k FIFO) | ✅ accepted | §§18–24, lines ~58k–65k | `DecisionLedger`, `exportData().ledger` |
| [003](adr/003-origin-controller.md) | Per-origin throttle & budget (2 concurrent / 150 ms / 50 per origin, 150 global) | ✅ accepted | §§20–22, lines ~60k–64k | `OriginController`, `CONFIG.origin`, `reserveRequestSlot` |
| [004](adr/004-fingerprint.md) | Content fingerprint (fnv1a32, 1M sample, Resource dedup) | ✅ accepted | §§24–26, lines ~65k–70k | `fnv1a32`, `makeFingerprint`, `fingerprintIndex` |
| [005](adr/005-mutation-batch.md) | Mutation observer batch dedup | ✅ accepted | §28 → v0.7.2 P1-2 | `installMutationObserver`, `seen Set` |
| [006](adr/006-export-schema.md) | Export schema (gde-export-v8.0, ledger + coverage) | ✅ accepted | §§26–30 → v0.7.2–v0.7.3 | `exportData()`, `serialize`, `getCoverageMetrics` |
| — | Coverage frontier metric (planned §19, shipped v0.7.3) | ✅ accepted | §19, §39 → v0.7.3 patch | `getCoverageMetrics()` |
| — | Privacy scrub opt-in (v0.7.4) | ✅ accepted | SECURITY_AUDIT S-07 → v0.7.4 | `CONFIG.privacy` |
| — | Trusted Types bridge (v0.7.5) | ✅ accepted | SECURITY_AUDIT S-02 → v0.7.5 | `trustedTypes.createPolicy('gde-bridge')` |
| — | Fuzz harness (v0.7.5) | ✅ accepted | PERFORMANCE + SECURITY → v0.7.5 | `tests/fuzz-extract.test.js` |

## Decisions still in transcript (not yet ADR-ified)

- DVB analogy scope (web is open-world, DVB is bounded spectrum) — see `VERIFICATION_REPORT.md` §2.1.
- Adaptive concurrency (thresholds 4/2) — `GenericDiscoveryEngine.onSuccess/onFailure`.
- Persistence migration v6→v8 additive — `KnowledgeBase.restore` + `STORAGE_KEY v8`.
- Network bridge vs PerformanceObserver separation (GET-trust rule) — `NetworkObserver` header comment.

## Process
1. ChatGPT proposes; user selects v0.2.0 as base.
2. Each iteration adds one control-plane concern (claim-before-await, policy-before-acquisition, ledger-for-explainability).
3. Verification (v0.7.1 audit) files P0/P1; patches landed v0.7.2/v0.7.3/v0.7.4/v0.7.5.

## Further splits
- The 2.2 MB file also contains 12 full code fences. The runnable artifact is now `dist/generic-discovery-engine.user.js` (v0.7.5, 5,421 lines). The fences are retained for diff archaeology but are no longer the source of truth.
- With 6 ADRs the control-plane split is considered **complete** for v0.7.x; remaining transcript is chat history, not architecture.
