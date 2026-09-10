# Prototype Limitations and Failure Modes

Claim state: `CURRENT`. Evidence state: `CORROBORATED` — static analysis plus
executed checks. Verification state: `VERIFIED` for D1, D2, D3, D7, D8 (reproduced
or statically proven); `PARTIALLY_VERIFIED` for D5, D6, D9 and for entries marked
ARGUMENT; `UNVERIFIED` for entries marked OPEN. Nothing here describes a
protection that does not exist.

Evidence tools:

```bash
node tools/verify.mjs      # static: reports D1 and D3 as [DEFECT]
node tools/simulate.mjs    # dynamic: runs the artifact and measures the outcomes
```

## Known defects

| ID | Defect | Evidence | Impact |
| --- | --- | --- | --- |
| **D1** | Re-discovery of an in-flight candidate re-queues it, allowing a second owner | static: `queueCandidate()` refuses only `completed`/`skipped`; dynamic: 2–4 concurrent owners, 12–18 duplicate URL acquisitions per run | duplicate network work, violated ownership invariant, double-counted discoveries |
| **D2** | Workers exit permanently when no candidate is eligible at that instant; the pool is never refilled | dynamic: peak live workers is 1 with an initially empty frontier and 4 only when the frontier is pre-populated | effective concurrency below configured concurrency; long tail of a scan runs single-threaded |
| **D3** | `failed` is a claimable state and `markFailed()` sets no backoff | static: claim eligibility includes `failed`; dynamic: a permanently broken URL is re-fetched repeatedly instead of being retired | request budget consumed by dead targets |
| **D4** | A candidate waiting for retry backoff is abandoned when workers exit, and `running` stays `true` | dynamic: candidate left `queued` with `backoffMs > 0` at quiescence; UI state `running`; `Scan` button becomes a no-op | work silently stops; restart requires a page reload |
| **D5** | Adaptive concurrency updates `currentConcurrency` but never resizes the live pool | static: pool created once in `start()`; `start()` early-returns while running | the adaptive subsystem has no runtime effect; UI shows the adjusted value |
| **D6** | The per-URL acquisition guard is not atomic across the in-flight window | consequence of D1: both owners check `shouldAcquireResource()` before either resource reaches `acquired` | duplicate acquisition |
| **D7** | `stats.acquired` is never incremented | static: no writer for that counter | exported statistics and the UI report a permanently zero value |
| **D8** | Content fingerprints are collected and indexed but never read | static: 4 write/probe sites, 0 read sites for `fingerprintIndex` | content identity cannot influence any decision; the platform for v0.17 identity resolution exists but is dead code |
| **D9** | Every recognition stores a new `Discovery`, even for a URL already discovered | dynamic: 74 discoveries for 27 unique URLs in one harness run | discovery counts overstate the frontier; combined with D1 the same expansion runs repeatedly |

D1, D2, D3 differ in severity: D1 breaks a stated architectural invariant, D2/D4
break scan termination semantics, D3 wastes budget, D5/D7 are reporting and
control-plane errors, D8 is dead capability, D9 inflates discovery counts.

### Why D9 happens

Two independent mechanisms add discovery records for the same URL:

1. `text/html` matches `HtmlProvider` **and** `TextProvider`, so one body is
   interpreted twice — structural extraction plus raw URL extraction (see
   [../architecture/provider-model.md](../architecture/provider-model.md));
2. `emitDiscovery()` always stores a `Discovery` and only *then* deduplicates the
   derived candidate through `addCandidate()`. A URL rediscovered from a page
   that is acquired twice (D1) or from two different pages produces a second,
   third … discovery record.

The candidate store stays deduplicated; the discovery store does not.

## Failure-mode matrix

| Failure | Detection | Current behaviour | Desired behaviour | Status |
| --- | --- | --- | --- | --- |
| Duplicate candidate proposed | `identityKey()` lookup | merged into the existing candidate (`alternateTypes`, `alternateParents`, max priority) | unchanged | handled |
| Duplicate candidate *in flight* | none | re-queued, second owner, duplicate acquisition (D1) | refuse re-queue for any non-terminal state | **defect** |
| Duplicate discovery of the same URL | none | a second `Discovery` record is stored for the same URL (two mechanisms: provider double-match, repeated expansion) — **D9** | deduplicate, or count as corroboration with provenance | **defect** |
| Candidate starvation (low priority) | none | possible; no aging, no fairness term | aging or fairness policy | OPEN (DESIGNED v0.15) |
| Unbounded candidate growth | `maxCandidates` | new candidates dropped silently; diagnostic recorded | unchanged, but surface the drop to the user | handled (silent) |
| Provider misclassification | multiple providers may match | all matching providers run; text provider acts as a fallback and can emit URL-shaped noise | provider priority / arbitration | OPEN (DESIGNED v0.11) |
| Malformed response body | provider `try/catch` | provider aborts, `provider-error` diagnostic, scan continues | unchanged | handled |
| Unsupported content type | `looksLike*` chain | `BinaryProvider` matches and emits nothing; resource is still recorded | unchanged | handled |
| Timeout | 8 s timer | `Observation{status:'timeout'}` → retry with backoff | unchanged | handled |
| Network error | `onerror` handler | `Observation{status:'error'}` → retry with backoff | unchanged | handled |
| HTTP 4xx/5xx | status check (`200 ≤ s < 400`) | `Observation{status:'http-error'}` → retry → `failed` → claimable again (D3) | terminal failure with backoff | **defect** |
| Redirect loop | none | delegated to the userscript host; only `finalUrl` is recorded | bounded redirect handling | OPEN |
| Cross-origin target | `isAllowedUrl()` | rejected at creation and at planning (`url-not-allowed`) | unchanged | handled |
| Repeated expansion of one URL | identity dedup + `shouldAcquireResource()` | after completion the URL is not acquired again; discoveries may still be re-recorded | unchanged | handled (post-completion) |
| Persistence corruption | `try/catch` around `JSON.parse` | restore is skipped, scan continues with empty state | unchanged | handled |
| Persistence growth | caps (750/1200/1500/3000/5000) | oldest entries trimmed | unchanged | handled |
| Worker cancellation | `stopRequested` | current candidate finishes, worker exits | cancel in-flight request (runtime-owned cancel) | partial (DESIGNED v0.10) |
| Worker crash (unexpected exception) | none — `worker()` has `try/finally` but no `catch` | that worker dies; `start()`'s `Promise.all` may reject, skipping final persistence/UI update (ARGUMENT, static) | catch, record diagnostic, keep the pool alive | OPEN |
| Partial observation | `bodyTruncated` flag | body truncated at 2 MB; recognition runs on the truncated body | unchanged, but record recognition-time truncation effects | handled (flagged) |
| False-positive recognition | none | plausible: any URL-shaped string in text/JS becomes a candidate | confidence-thresholded acceptance | OPEN |
| False-negative recognition | none | plausible: binary bodies, truncated HTML, unrecognized encodings | coverage/diagnostics for unparsed bodies | OPEN |
| Retry storm | backoff gate | bounded for `queued` retries; **unbounded for `failed`** (D3) | terminal state respected | **defect** |
| Scan never finishes | wall-clock observation | budget (150 requests) bounds the run in practice; without budget exhaustion it ends at empty eligible set | explicit termination evaluator | OPEN (DESIGNED v0.14) |
| Ledger growth | cap 5000 | oldest events dropped, so early causal history is lost on long scans | durable append-only log | handled by cap, information loss accepted |
| Cross-context duplication | none | two tabs each run their own engine with their own state | shared claim/lease records | DESIGNED (v0.33), not implemented |
| Content-type trust | `contentTypeBase()` | providers combine header and body sniffing; header alone is not trusted | unchanged | handled |

## What the prototype cannot claim

The prototype can state, at best:

* which candidates existed, and why (parent, mechanism);
* what was observed for each attempted candidate;
* what was interpreted from those observations;
* what budget was consumed and what remains unclaimable at that moment.

It cannot state that a search is **complete**, that a URL does **not** exist, or
that its results are **exhaustive**. The design series proposes coverage,
absence and completeness objects (v0.22 – v0.23) precisely because those claims
require explicit accounting that this code does not perform.
