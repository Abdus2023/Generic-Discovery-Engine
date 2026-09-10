# Provider Model

Status: **CURRENT** for recognition providers; **DESIGNED** for acquisition and
candidate-source providers.

## Three planes

```
Acquisition        "how do I obtain this?"     CURRENT: one HTTP GET path
Recognition        "what did I obtain?"        CURRENT: seven provider classes
Candidate sources  "what might exist?"         CURRENT: engine methods, not an interface
```

The design series separates all three into replaceable interfaces
(v0.9 acquisition providers, v0.11 recognition providers, v0.12 candidate
sources). Only recognition is an actual interface in the prototype.

## Canonical provider architecture

```
             ┌───────────────┐
             │ Acquisition   │
             └───────┬───────┘
                     │
                     ▼
             ┌───────────────┐
             │  Observation  │
             └───────┬───────┘
                     │
                     ▼
             ┌───────────────┐
             │ Provider      │
             │ Registry      │
             └───────┬───────┘
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
        HTML        JSON       Text   (+ XML, CSS, JS, Binary)
          │          │          │
          └──────────┼──────────┘
                     ▼
                Discovery
                     │
                     ▼
             Candidate Expansion
```

## Contract (as implemented)

```
class Provider {
    matches(observation) → boolean
    async recognize(candidate, observation) → Discovery[]
}
```

* `matches()` must be cheap and must not have side effects. Most providers
  combine a content-type test with a body sniff (`looksLikeHtml`, `looksLikeJson`,
  `looksLikeXml`, `looksLikeCss`, `looksLikeJavaScript`, `looksLikeBinary`).
* `recognize()` receives the candidate and observation and returns discoveries.
  It may throw; the engine catches the error, records a `provider-error`
  diagnostic, and continues with the remaining matching providers.
* **Multiple providers may match one observation.** All matching providers are
  run; there is no router priority or arbitration in v0.7.1.

## Providers

Matching combines a content-type test with a body sniff where the format allows
it, so a mislabelled response can still be recognized.

| Class | Match rule (as implemented) | Emits |
| --- | --- | --- |
| `HtmlProvider` | `text/html`, `application/xhtml+xml`, **or** body starting with `<!doctype html` / `<html` | links, frames, scripts, media, form actions, metadata URLs (`og:`, `twitter:`, meta-refresh) |
| `JsonProvider` | `application/json`, `*+json`, **or** body starting with `[` or `{` | URL-like string values found by a recursive walk |
| `XmlProvider` | `application/xml`, `text/xml`, `*+xml`, **or** body starting with `<?xml` | `loc` values |
| `CssProvider` | `text/css` only | `url(...)` references |
| `JavaScriptProvider` | `application/javascript`, `text/javascript`, `application/x-javascript`, `text/ecmascript`, `application/ecmascript` | string literals that parse as HTTP(S) URLs |
| `TextProvider` | **`text/*` or an empty content type** | HTTP(S) URLs and **relative** URL-shaped paths in the text |
| `BinaryProvider` | `image/*`, `audio/*`, `video/*`, `application/pdf`, `application/zip`, `application/octet-stream` | nothing (recognizes; deliberately emits no candidates) |

Two consequences of this design are worth stating explicitly, because they are
easy to misread:

1. **`TextProvider` is not a universal fallback.** It matches `text/*` and
   unknown/absent content types only. A `application/octet-stream` or
   `application/javascript` response is not passed to it.
2. **Several providers may match one observation.** `text/html` matches both
   `HtmlProvider` and `TextProvider`; `text/css` matches `CssProvider` and
   `TextProvider`; `text/xml` matches `XmlProvider` and `TextProvider`. All
   matching providers run, so one body can be interpreted twice by design —
   structural extraction plus raw URL extraction. There is no router, priority or
   arbitration in v0.7.1 (DESIGNED: v0.11).

Extraction helpers used by the providers:

| Helper | Behaviour |
| --- | --- |
| `extractUrlsFromText(text)` | absolute `http(s)://…` matches **and** relative paths beginning `/`, `./`, `../` |
| `extractCssUrls(text)` | `url(...)`, quoted or unquoted |
| `extractXmlLocs(text)` | `<loc>` values via `DOMParser`, with a regex fallback |

## Boundary rules

| Rule | Status |
| --- | --- |
| Providers must not perform network I/O | **holds** — no provider references `GM_xmlhttpRequest`, `fetch` or `XMLHttpRequest` |
| Providers must not enqueue candidates | **holds** — providers return `Discovery[]`; only `emitDiscovery()` creates candidates |
| Providers must not own scheduling, retry or budget policy | **holds** — all of it is in `KnowledgeBase`/`AcquisitionPolicy`/`Acquisition` |
| Providers must not write persistence | **holds** — persistence is triggered by the engine |
| Providers must not own deduplication | **holds** — dedup happens in `KnowledgeBase.addCandidate()` |
| A provider failure must not fail the scan | **holds** — per-provider `try/catch` plus a ledger diagnostic |

These five rules are the reason the provider layer is genuinely replaceable, and
they are the part of the prototype that most closely matches the design series.

## Acquisition plane (CURRENT, not pluggable)

`Acquisition` performs one HTTP GET through `GM_xmlhttpRequest` when available and
`fetch` otherwise, with an 8 s timeout, origin gating, and body truncation.
There is no acquisition-provider interface, no cache provider, no replay
provider, and no capability negotiation; those are DESIGNED (v0.9, v0.8).

## Candidate-source plane (CURRENT, engine-internal)

Sources exist as engine methods, not as a registry:

| Source | Method | Notes |
| --- | --- | --- |
| Current page | `observeCurrentPage()` | priority 1, depth 0 |
| DOM (initial and mutations) | `observeCurrentDom()` | links, scripts, frames, images, form actions; debounced 250 ms |
| Network bridge | `handleBridgeEvent()` → `observeNetworkGet()` | only `phase === 'response'` events whose method is known to be `GET` |
| Performance entries | `installPerformanceObserver()` | static resources are treated as GET-like; `fetch`/`xhr` entries are **evidence only** because the observer cannot prove the method |

The performance-observer rule is deliberate and is recorded in the artifact's own
comment: *"PerformanceObserver does NOT imply GET."* Do not describe performance
entries as proof of a GET request.

## DESIGNED

| Layer | Version | Content |
| --- | --- | --- |
| Acquisition providers with capability contracts | v0.9, v0.10 | provider selection, admission control, cancellation, timeout owned by runtime |
| Recognition runtime with a response router | v0.11 | provider priority, recognition confidence, failure taxonomy |
| Candidate sources | v0.12, v0.13 | sources propose; a controller prevents uncontrolled proposal generation |
| Classification layer separate from recognition | v0.18 | recognition ≠ semantic classification |

See [../roadmap/future-architecture.md](../roadmap/future-architecture.md).

## Decisions

### D-07 — Providers return discoveries; the engine expands them

* **Decision:** the provider contract is `matches()` + `recognize()`; there is no
  `candidates()` method.
* **Rationale:** expansion is where scope, depth, deduplication and budget policy
  live; letting providers enqueue would give each provider a private crawler.
* **Alternatives considered:** the design brief's `candidates()` shape, and
  providers that fetch their own resources (both rejected: they would make the
  provider layer a scheduler).
* **Consequence:** a new provider cannot bypass dedup or depth limits, and can be
  tested with no network.
* **Status:** IMPLEMENTED, verified by `tools/verify.mjs`.

### D-08 — Multiple providers may match one observation

* **Decision:** every matching provider runs; there is no router or priority.
* **Rationale:** recognition is cheap and deterministic; running all matches
  maximizes recall for a prototype.
* **Alternatives considered:** content-type routing with a single winner
  (deferred to v0.11, which introduces a response router and provider priority).
* **Consequence:** a `text/html` body is interpreted twice (HTML structure plus
  text URL extraction), and confidence values from different providers are not
  comparable.
* **Status:** IMPLEMENTED (D9 is the accounting consequence).
