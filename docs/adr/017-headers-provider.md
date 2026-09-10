# ADR 017 — Headers Provider (Link & Location)

**Status:** accepted (v0.8.0)  
**Transcript:** Phase 2 “HTTP headers provider”  
**Code:** `HeadersProvider`, `Observation.http.headers`, `Acquisition` fetch + `GM_xmlhttpRequest` header capture

## Context
`Acquisition` stored `http: {status, contentType, contentLength, finalUrl}` but discarded `Link`, `Location`, and other response headers. The engine therefore missed `Link: <https://ex/next>; rel="next"` pagination and `Location:` redirects that are not in body. `HtmlProvider` extracts `<a href>` but not header links. The 2.2 MB transcript planned an HTTP headers provider but never shipped it.

## Decision
- Capture `http.headers` in `Acquisition`:
  - Fetch fallback: `headers: Object.fromEntries([...response.headers.entries()].map(([k,v])=>[k.toLowerCase(),v]))`
  - `GM_xmlhttpRequest`: parse `response.responseHeaders` string (`\r?\n` split, `:` index, lowercased keys) into same shape.
  - Stored in `Observation.http.headers` alongside `status`/`contentType`/`contentLength`/`finalUrl`; `Observation` class unchanged (stores `data.http` as provided).
- Add `HeadersProvider` (order 7 after `RobotsProvider`, before `BinaryProvider`):
  - `matches`: `http.headers` exists and `headers['link']` contains `<https://…>` OR `headers['location']` is allowed URL.
  - `recognize`: parse `Link` header via `/<([^>]+)>/g` (extracts `<url>`), emit `kind:url` `mechanism:headers-link` 0.88; parse `Location` emit `mechanism:headers-location` 0.90.

## Consequences
- **+** Pagination `Link` and redirect `Location` now discovered with correct provenance, independent of body parsers; `matches` is O(headers) ~0.01 ms.
- **+** `http.headers` also enables future `S-02` CSP header inspection and `changeDetection` via `ETag`/`Last-Modified` (not yet used).
- **−** Header names lowercased for case-insensitivity, but original case lost — acceptable for discovery.

## Links
- Tests: `tests/provider-robots-headers.test.js` “HeadersProvider” (4 cases: source contains, matches Link, matches Location, extracts 3 URLs).
- Code: `HeadersProvider`, `Acquisition` header capture, `Observation.http.headers`.
