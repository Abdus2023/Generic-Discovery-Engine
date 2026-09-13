# ADR 025 — SitemapIndex + OpenAPI Providers (11-provider pipeline)

**Status:** accepted (v1.2.0)  
**Transcript:** 1.2 provider expansion — sitemap index + OpenAPI discovery  
**Code:** `src/providers.js` `SitemapIndexProvider` `OpenApiProvider` `ProviderRegistry` 11, `src/config.js` `providers` unchanged, `tests/provider-sitemap-openapi.test.js` 8 cases

## Context
v1.1.0 delivered lazy 9-provider pipeline (`Html/Json/Xml/Css/JavaScript/Robots/Headers/Binary/Text`) with `CONFIG.providers` lazy/disabled + metrics (135/135, 6076 lines `6dcfa8…`). Future 1.x per ADR 023 was "provider additions or esbuild tree-shaking". Real-world sites expose `<sitemapindex>` (parent sitemaps listing child `sitemap.xml` with `<loc>`) and OpenAPI/Swagger (`openapi: 3.x` / `swagger: 2.0` with `servers[].url` or `host+basePath`) — high-value discovery seeds not yet specialized: `XmlProvider` extracts `<loc>` generically (kind `xml` 0.70) but does not distinguish `sitemapindex` (should be `sitemap` 0.90), `JsonProvider` extracts URLs generically (0.75) but does not recognize OpenAPI `servers` (should be `api` 0.95). Tenants disabling `TextProvider` still pay `Xml`/`Json` generic cost; specialized providers allow higher confidence + provenance `sitemap-index-loc`/`openapi-server`.

## Decision
- **SitemapIndexProvider** `src/providers.js` `class SitemapIndexProvider extends Provider` `name='sitemapIndex'` — `matches` true if `body` contains `/sitemapindex/i` or (`contentType xml` + `<sitemap` + `looksLikeXml`) or (`requestedUrl` `sitemap*.xml` + `<loc>`); `recognize` `extractXmlLocs(body)` → `Discovery kind:'sitemap' confidence:0.90 mechanism:'sitemap-index-loc'`. Cost O(n) `extractXmlLocs` ~0.02 ms, same as `XmlProvider`.
- **OpenApiProvider** `class OpenApiProvider extends Provider` `name='openapi'` — `matches` if `looksLikeJson` && `JSON.parse` has `openapi` or `swagger` or (`info` && `paths`); `recognize` parses JSON, emits `servers[].url` as `kind` `api`/`url` `confidence 0.95` `mechanism 'openapi-server'`, `swagger host+basePath+scheme` as `0.90 'openapi-host'`, then walks remaining JSON for `looksLikeApiUrl` strings as `0.85 'openapi-url'` (dedup via `discoveries.some`). Cost JSON parse + walk O(n) ~0.05 ms for typical 10 kB spec.
- **Registry** `ProviderRegistry` `factories` adds `sitemapIndex:()=>new SitemapIndexProvider()` `openapi:()=>new OpenApiProvider()` + `order` inserts `'sitemapIndex','openapi'` before `binary` (preserves original 9 relative order, adds 2): `['html','json','xml','css','javascript','robots','headers','sitemapIndex','openapi','binary','text']` (11 lazy factories, `disabled` respects new names, `getInstanceCount` now 11, `getMetrics` tracks new). Static `new SitemapIndexProvider()`/`new OpenApiProvider()` strings remain for `verify:build` order check.
- **Tests** `tests/provider-sitemap-openapi.test.js` 2 suites 8 cases: static `dist contains SitemapIndexProvider/OpenApiProvider` + order 11, `SitemapIndex` matches `sitemapindex` root + extracts 2 `loc`s as `sitemap`, `OpenApi` matches `openapi`/`swagger`/`info+paths` true vs plain json false, extracts `servers` 2 urls, swagger `host+basePath` → `https://api.ex/v1`, lazy `disabled` respects new names. `npm test` 143/143 37 suites (135+8) vs 135/135.

## Consequences
- **+** Sitemap index crawling now specialized: parent sitemap yields child sitemaps with higher confidence (0.90 vs generic Xml 0.70) and provenance `sitemap-index-loc` for ledger filtering. OpenAPI specs yield `servers` as `api` seeds without generic JSON walk noise (0.95 vs 0.75), enables `api` prioritization `typePriority api 1.00`.
- **+** Lazy still 0→11 on demand; `disabled:['openapi']` skips OpenAPI parse cost; metrics expose new providers (`sitemapIndex` low matches, `openapi` rare 0.95). Bundle +138 lines (6076→6214) `+659…` `344b9c…` `188338B`, min `60743B 32.3%` `ca3fc9…` (19.1% provider payload 36k), analyze shows `Html` 8640 B > `Binary` 4894 B > `Json` 4368 B.
- **−** 11-provider `matching` loop now 11 vs 9 (+2 `matches` calls, ~0.004 ms), still O(11) negligible at `concurrency 4`. Duplicate `sitemap` `<loc>` from both `XmlProvider` and `SitemapIndexProvider` deduped via `emittedForObservation Set` (same `targetUrl`).

## Links
- Code: `src/providers.js` `SitemapIndexProvider`/`OpenApiProvider`, `ProviderRegistry` `11` `order`, `tests/provider-sitemap-openapi.test.js`.
- Prior: ADR 024 lazy+esbuild, ADR 016/017 robots/headers, `VERIFICATION_SUPPLEMENT_v1.1.0.md` 135/135.
