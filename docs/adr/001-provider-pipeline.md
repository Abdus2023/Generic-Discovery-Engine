# ADR 001 — Provider Pipeline (7 providers, ordered matching)

**Status:** accepted (v0.7.1)  
**Transcript:** `Continue Architecture Planning.md` §§7–23 (lines ~45k–58k)  
**Code:** `Provider` base, `Html/Json/Xml/Css/JavaScript/Binary/TextProvider`, `ProviderRegistry` (dist lines ~1.9k–3k)

## Context
Early v0.1.0 had a single ad-hoc HTML URL extractor. v0.2.0 introduced a `Provider` abstraction but only 3 providers (Html, Json, Text). Verification (§2.2, §4.5) found that mixed content (sitemap XML, CSS `url()`, JS URL literals, binary resources) was either ignored or extracted via a single regex, causing misses and false positives.

## Decision
- Define a `Provider` base with `matches(observation) → boolean` and `recognize(candidate, observation) → Discovery[]`.
- Register **7 providers in fixed order**: `Html (dom links) → Json (recursive string walk) → Xml (sitemap <loc>) → Css (url()) → JavaScript (regex) → Binary (observed-only) → Text (fallback regex)`.
- `ProviderRegistry.matching(observation)` filters to the providers whose `matches` predicate passes (content-type + body prefix). Execution is ordered; discoveries are unioned then deduped per-observation via `emittedForObservation Set<targetUrl>` (v0.7.2 P1-1).

## Consequences
- **+** Content-type-specific extraction: `looksLikeHtml/Json/Xml/Css/JavaScript/Binary` gates avoid running 7 regexes on every body; cost is `O(body)` bounded at `maxBodyChars 2M`.
- **+** Extensibility: adding a new type (e.g., PDF manifest) is a new subclass + registry entry, no changes to `GenericDiscoveryEngine`.
- **+** Explainability: each `Discovery` carries `mechanism` (e.g., `html-link`, `xml-loc`, `json-url`) and is ledgered (`provider-recognized`).
- **−** Order matters: `Html` before `Text` avoids double-emitting links that also match the generic URL regex; ordering must be documented.

## Alternatives considered
- Single regex over all bodies: rejected (misses DOM semantics, e.g., `<link rel=stylesheet>` type).
- Content negotiation via header only: rejected (many resources served as `text/plain` with JSON body; `looksLikeJson` also checks `^{`).

## Links
- Verification: `VERIFICATION_REPORT.md` §2.2, `VERIFICATION_SUPPLEMENT_v0.7.2.md` P1-1.
- Tests: `e2e-discovery-loop.test.js` fixtures cover html/json/xml/js/text providers.
