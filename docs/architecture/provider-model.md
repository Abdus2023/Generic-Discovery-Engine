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

| Class | Match signal | Emits | Mechanism tags |
| --- | --- | --- | --- |
| `HtmlProvider` | HTML content type or body sniff | links, frames, scripts, media, form actions, metadata URLs (og/twitter, meta-refresh) | `html-link`, `html-frame`, `html-script`, `html-media`, `html-form-action`, `metadata-url` |
| `JsonProvider` | JSON content type or body sniff | URL-like string values found by recursive walk | `json-url` |
| `XmlProvider` | XML content type or body sniff | `loc`/location values | `xml-loc` |
| `CssProvider` | CSS content type | `url(...)` references | `css-url` |
| `JavaScriptProvider` | script content type | string literals that parse as HTTP(S) URLs | `javascript-url` |
| `TextProvider` | anything not matching the above | HTTP(S) URLs in the text | `text-url` |
| `BinaryProvider` | binary content types | nothing (recognizes, deliberately emits no candidates) | — |

The registry order matters only for `TextProvider`/`BinaryProvider`, which act as
fallbacks; all matching providers run.

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
