# Prototype Version Artifacts

> **Status:** CURRENT
>
> **Source:** `Userscript Discovery Prototype.md`; `Continue Architecture Planning.md`
>
> **Purpose:** Index of the complete userscript artifacts preserved verbatim from the planning conversation.

The conversation contains several complete prototype scripts, preserved here in conversation order, each as one file. The conversation revisits some version numbers, so the same version number can appear more than once; the artifacts are **not** merged because the scripts differ (contradiction [C-01](../../REVIEW-NOTES.md#c-01--prototype-version-numbering-is-not-monotonic)).

| # | Artifact | Sections | Status | Contents |
| --- | --- | --- | --- | --- |
| 00 | [`00-v0.1.0-and-v0.2.0-paste.md`](00-v0.1.0-and-v0.2.0-paste.md) | `CAP-001` | UNVERIFIED | The two userscript versions as pasted into the planning conversation (flattened copy; preserved verbatim). |
| 01 | [`01-v0.1.0.md`](01-v0.1.0.md) | `USP-065`, `USP-066` | CURRENT | The first complete userscript: candidate, observation, validation, discovery, scheduler. |
| 02 | [`02-v0.2.0.md`](02-v0.2.0.md) | `USP-069`, `USP-070` | CURRENT | Adds explicit concurrent candidate claiming, HTML/JSON/text providers and an explicit scope. |
| 03 | [`03-v0.3.0.md`](03-v0.3.0.md) | `CAP-003`, `CAP-004` | CURRENT | Corrections to URL resolution, discovery model, timeouts, retries and persistence. |
| 04 | [`04-v0.4.0-plan.md`](04-v0.4.0-plan.md) | `CAP-007`, `CAP-008` | FUTURE | Plan for v0.4.0: network observation, richer candidate types, scheduling and UI. |
| 05 | [`05-v0.4.0.md`](05-v0.4.0.md) | `CAP-009`, `CAP-010` | CURRENT | Adds passive page-network observation, a provenance graph and depth tracking. |
| 06 | [`06-v0.5.0.md`](06-v0.5.0.md) | `CAP-013` | CURRENT | Adds an execution-world-safe network bridge, PerformanceObserver fallback and candidate fingerprints. |
| 07 | [`07-v0.4.0-second-iteration.md`](07-v0.4.0-second-iteration.md) | `CAP-016` | CURRENT | A second complete v0.4.0 produced later in the conversation. |
| 08 | [`08-v0.5.0-plan.md`](08-v0.5.0-plan.md) | `CAP-019` | FUTURE | Plan for v0.5.0: separate observation from acquisition and make resources explicit. |
| 09 | [`09-v0.5.0-second-iteration.md`](09-v0.5.0-second-iteration.md) | `CAP-021` | CURRENT | Canonical resource identity, discovery mechanisms separated from acquisition. |
| 10 | [`10-v0.6.0.md`](10-v0.6.0.md) | `CAP-024` | CURRENT | Candidates separated from the resource database; resource graph and policy layer. |
| 11 | [`11-v0.5.0-third-iteration.md`](11-v0.5.0-third-iteration.md) | `CAP-027` | CURRENT | A third complete v0.5.0 produced later in the conversation. |
| 12 | [`12-v0.6.0-second-iteration.md`](12-v0.6.0-second-iteration.md) | `CAP-030` | CURRENT | Policy/scheduler layer, adaptive concurrency and per-origin budgets. |
| 13 | [`13-v0.6.0-third-iteration.md`](13-v0.6.0-third-iteration.md) | `CAP-033` | CURRENT | A third complete v0.6.0 with acquisition policy and hard request reservation. |
| 14 | [`14-v0.7.1.md`](14-v0.7.1.md) | `CAP-043` | CURRENT | Complete v0.7.1 userscript: deterministic event ledger and replayable acquisition decisions. |

## Notes

- Each artifact keeps the surrounding lead-in text, so it stays traceable to its conversation turn.
- Change notes written after a script are collected in [Userscript Development Narrative](../userscript.md).
- `00-v0.1.0-and-v0.2.0-paste.md` is the flattened paste of the same two scripts that are preserved with full formatting in `01-v0.1.0.md` and `02-v0.2.0.md`; both are kept because they differ character-for-character ([Duplicates](../../REVIEW-NOTES.md#duplicates-and-near-duplicates)).

## Related Documents

- [Prototype Overview](../overview.md)
- [Userscript Development Narrative](../userscript.md)
- [Configuration](../configuration.md)
- [Prototype Scope and Limitations](../limitations.md)
- [Documentation index](../../README.md)

