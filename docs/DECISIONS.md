# Architecture Decisions — Index

> Source transcript: [`Continue Architecture Planning.md`](../Continue%20Architecture%20Planning.md) (2.2 MB, 92,274 lines, 12 userscript iterations v0.1.0→v0.7.1).  This index is the **P2-10 hygiene split** (v0.7.4) that extracts the durable decisions into ADRs without deleting the transcript.

## How to use this file
- Each ADR is a one-page record: **Context → Decision → Consequences → Alternatives → Links**.
- The transcript remains the provenance; ADRs are the normative summary.
- New decisions get a new `docs/adr/NNN-title.md` and are linked here.

## Decisions extracted (v0.7.4)

| ADR | Title | Status | Transcript range | Code |
|-----|-------|--------|------------------|------|
| [001](adr/001-provider-pipeline.md) | Provider pipeline (7 providers, ordered matching) | ✅ accepted | §§7–23, lines ~45k–58k | `Provider`, `ProviderRegistry`, `Html/Json/Xml/Css/JS/Binary/Text` |
| [002](adr/002-ledger.md) | Deterministic Decision Ledger (12 typed events, 5k FIFO) | ✅ accepted | §§18–24, lines ~58k–65k | `DecisionLedger`, `exportData().ledger` |
| [003](adr/003-origin-controller.md) | Per-origin throttle & budget (2 concurrent / 150 ms / 50 per origin, 150 global) | ✅ accepted | §§20–22, lines ~60k–64k | `OriginController`, `CONFIG.origin`, `reserveRequestSlot` |
| — | Coverage frontier metric (planned §19, shipped v0.7.3) | ✅ accepted | §19, §39 → v0.7.3 patch | `getCoverageMetrics()` |
| — | Privacy scrub opt-in (v0.7.4) | ✅ accepted | SECURITY_AUDIT S-07 → v0.7.4 | `CONFIG.privacy` |

## Decisions still in transcript (not yet ADR-ified)

- DVB analogy scope (web is open-world, DVB is bounded spectrum) — see `VERIFICATION_REPORT.md` §2.1.
- Adaptive concurrency (thresholds 4/2) — `GenericDiscoveryEngine.onSuccess/onFailure`.
- Persistence migration v6→v8 additive — `KnowledgeBase.restore` + `STORAGE_KEY v8`.
- Network bridge vs PerformanceObserver separation (GET-trust rule) — `NetworkObserver` header comment.

## Process
1. ChatGPT proposes; user selects v0.2.0 as base.
2. Each iteration adds one control-plane concern (claim-before-await, policy-before-acquisition, ledger-for-explainability).
3. Verification (v0.7.1 audit) files P0/P1; patches landed v0.7.2/v0.7.3/v0.7.4.

## Further splits
- The 2.2 MB file also contains 12 full code fences. The runnable artifact is now `dist/generic-discovery-engine.user.js` (v0.7.4, 5,3k lines). The fences are retained for diff archaeology but are no longer the source of truth.
- Suggested future ADR: `004-fingerprint-index`, `005-mutation-batch`, `006-export-schema`.
