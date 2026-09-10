# ADR 016 — Robots Provider (robots.txt Sitemap extraction)

**Status:** accepted (v0.8.0)  
**Transcript:** Roadmap Phase 2 “robots.txt provider”  
**Code:** `RobotsProvider`, `ProviderRegistry` (9 providers), `CONFIG.typePriority.robots 0.90`

## Context
`robots.txt` is the site-declared crawling contract and often advertises `Sitemap:` URLs that are not linked from HTML. Before v0.8.0 the engine had `XmlProvider` for sitemaps but no provider for `robots.txt` itself; a candidate `https://ex/robots.txt` would be fetched as `text` and its `Sitemap:` lines would be extracted only as generic `text-url` with confidence 0.40, losing the semantic `sitemap` type and priority 0.92. Operators could not distinguish sitemap discoveries from generic text URLs.

## Decision
- Add `RobotsProvider` (order 6 after `JavaScriptProvider`, before `HeadersProvider`):
  - `matches(observation)`: `requestedUrl` ends `robots.txt` (case-insensitive) OR `contentType` `text/plain` and body contains `User-agent:` (distinguishes robots.txt from other text/plain).
  - `recognize`: regex `Sitemap:\s*(https?:\/\/\S+)` global, canonicalize each, emit `Discovery` `kind:sitemap` confidence 0.92 mechanism `robots-sitemap` with provenance.
- Register in `ProviderRegistry` as 6th of 9: `Html, Json, Xml, Css, JavaScript, Robots, Headers, Binary, Text` (Text remains fallback last).
- Keep `typePriority.robots 0.90` for candidate priority; sitemap discoveries get `kind:sitemap` → `typePriority.sitemap 0.92` on next acquisition.

## Consequences
- **+** `https://ex/robots.txt` → `https://ex/sitemap.xml` now discovered with correct `kind:sitemap` and priority, proven by `provider-robots-headers.test.js` (Sitemap extraction 2 URLs).
- **+** No extra network cost: reuses existing `text/plain` fetch; `matches` is O(body) regex once.
- **−** Only `Sitemap:` lines are extracted; `Allow`/`Disallow` are not yet used for policy (future `AcquisitionPolicy` could respect `Disallow` as soft deny) — documented as residual.

## Links
- Tests: `tests/provider-robots-headers.test.js` “RobotsProvider” (4 cases: source contains, matches URL, matches body, Sitemap extraction).
- Code: `RobotsProvider` class, `ProviderRegistry`.
