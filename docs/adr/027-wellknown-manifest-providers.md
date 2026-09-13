# ADR 027 — WellKnown + Manifest Providers (13-provider pipeline)

**Status:** accepted (v1.3.0)  
**Transcript:** 1.3 provider expansion — well-known + manifest discovery  
**Code:** `src/providers.js` `WellKnownProvider` `ManifestProvider` `ProviderRegistry` 13, `tests/provider-wellknown-manifest.test.js` 7 cases

## Context
v1.2.0 expanded to 11 providers (`SitemapIndex`/`OpenApi`) with bundle analyze 19.1% (143/143, 6214 lines `344b9c…`). Remaining high-value well-known seeds: `/.well-known/` (IETF `security.txt` `Contact:` `openid-configuration` `jwks_uri`, `assetlinks.json` `relation`, `apple-app-site-association`) and Web App `manifest.json` (`icons[].src`, `start_url`, `scope`, `screenshots`) — both expose origin-scoped URLs with provenance `wellknown-*`/`manifest-*` and confidence 0.70–0.85, missed by generic `Json`/`Text` (0.40–0.75). `HtmlProvider` extracts `<link rel="manifest">` but not `manifest.json` body itself; `TextProvider` extracts URLs from `security.txt` but without `/.well-known/` guard.

## Decision
- **WellKnownProvider** `src/providers.js` `class WellKnownProvider extends Provider` `name='wellKnown'` — `matches` true if `requestedUrl` contains `/.well-known/` (IETF) or (`contentType text/plain` + `/Contact:/` + well-known path) or (`looksLikeJson` + well-known path); `recognize` branches: JSON → `JSON.parse` walk string values → `Discovery kind url/api confidence 0.80 mechanism 'wellknown-json-url'`; text → `extractUrlsFromText` → `0.70 'wellknown-text-url'`. Cost JSON walk O(n) ~0.03 ms, text regex ~0.02 ms.
- **ManifestProvider** `class ManifestProvider extends Provider` `name='manifest'` — `matches` if `manifest.json` in URL or `contentType application/manifest+json` or `looksLikeJson` && `JSON.parse` has `icons`/`start_url`/`scope` with `Array.isArray(icons)` or `start_url`; `recognize` parses JSON, emits `icons[].src` as `resource` `0.85 'manifest-icon'`, `start_url` `0.80`, `scope` `0.75`, `screenshots[].src` `0.80`, `shortcuts[].url` `0.78`, resolving relative via `new URL(url, requestedUrl)` + `canonicalizeUrl`. Cost parse + emit O(icons+screenshots) ~0.02 ms.
- **Registry** `ProviderRegistry` `factories` adds `wellKnown:()=>new WellKnownProvider()` `manifest:()=>new ManifestProvider()` + `order` inserts `'wellKnown','manifest'` before `binary` (preserves 11-order): `['html','json','xml','css','javascript','robots','headers','sitemapIndex','openapi','wellKnown','manifest','binary','text']` (13 lazy, `disabled` respects new, `getInstanceCount` 13). Static strings `new WellKnownProvider()`/`new ManifestProvider()` for `verify:build` 13-order check.
- **Tests** `tests/provider-wellknown-manifest.test.js` 2 suites 7 cases: static 13 order, WellKnown matches `/.well-known/security.txt` true vs `/page` false, extracts `jwks_uri` `wellknown-json-url`, Manifest matches `manifest.json` true vs plain `app.json` false, extracts icons `2` + `start_url` + `scope` =4 (relative `+https://cdn`), lazy `disabled` strings present. `npm test` 150/150 39 suites (143+7) vs 143/143.

## Consequences
- **+** Well-known discovery now specialized: `/.well-known/openid-configuration` yields `jwks_uri` as `api` without generic JSON noise (0.80 vs 0.75), `security.txt` yields `Contact` URL 0.70. Manifest yields `icons` as `resource` high confidence 0.85 for PWA pre-caching, provenance `manifest-icon` filterable in ledger.
- **+** Lazy 0→13 on demand; `disabled:['manifest']` skips manifest parse on non-PWA crawls; metrics expose new (`wellKnown` low, `manifest` rare). Bundle `6214→6344` +130 `195565B` `bb0453…`, min `63463B 32.5%` `d4de85…`, provider payload 42243 21.6% (Html 8640 > Binary 5031 > Json 4368).
- **−** 13-provider `matching` loop +2 calls ~0.004 ms, still O(13) at `concurrency 4` negligible. Manifest relative `icon.png` resolution via `new URL` may produce `https://ex/icon.png` even if `sameOriginOnly` false — still gated by `isAllowedUrl` and `policy`.

## Links
- Code: `src/providers.js` `WellKnownProvider`/`ManifestProvider`, `ProviderRegistry` 13, `tests/provider-wellknown-manifest.test.js`.
- Prior: ADR 025/026 sitemap/openapi/bundle, ADR 024 lazy, `VERIFICATION_SUPPLEMENT_v1.2.0.md`.
