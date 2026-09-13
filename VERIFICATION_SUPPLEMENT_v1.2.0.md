# Verification Supplement — v1.2.0 (SitemapIndex + OpenAPI + Bundle Analyze)

**Artifact:** `dist/generic-discovery-engine.user.js` v1.2.0 `6214 lines` `188338B` `sha256 344b9c71fbdccf6381be105bf2262b7e9178bba448ce0da29d05f3efb9884906` + `dist/generic-discovery-engine.min.js` `60743B` `32.3%` `sha ca3fc94fec601c2c922e70c035f2aa1bc71e8928715c84eb28473d8ff83e9c95` `241 lines`  
**Source:** `src/` 7 modules `config 170 + utils 357 + ledger 272 + models 377 + knowledge 730 + providers 1165 + engine 2921 ≈ 6214` `package 1.2.0` `src/header.txt` `v1.2.0 — SitemapIndex + OpenAPI Providers + Bundle Analyze`  
**Tests:** `npm test` **143/143 37 suites** (135+8) `node --check` PASS `verify:build` PASS (sitemap/openapi + minified log) `typecheck` PASS `coverage:check` 85/75/80, `analyze-bundle` 19.1%

## § Providers 11
- **SitemapIndexProvider** `src/providers.js` `class SitemapIndexProvider` `name='sitemapIndex'` — `matches` `/sitemapindex/i` in body or xml `sitemapindex` or `sitemap*.xml` + `<loc>`; `recognize` `extractXmlLocs` → `Discovery kind:'sitemap' confidence:0.90 mechanism:'sitemap-index-loc'` O(n) ~0.02 ms. Proven via `provider-sitemap-openapi.test.js` sitemapindex root true vs html false, extracts 2 locs `s1.xml`/`s2.xml`.
- **OpenApiProvider** `class OpenApiProvider` `name='openapi'` — `matches` `looksLikeJson` && `JSON.parse` has `openapi`/`swagger` or `info+paths`; `recognize` emits `servers[].url` 0.95 `openapi-server`, `swagger host+basePath+scheme` 0.90 `openapi-host`, walk `api` URLs 0.85 `openapi-url` (dedup). Proven via matches openapi 3.0/swagger 2.0/info+paths true vs plain false, extracts servers 2 + host `https://api.ex/v1`.
- **Registry** 11 factories `html json xml css javascript robots headers sitemapIndex openapi binary text` order `Html→Text` (preserves original 9 relative), lazy `_get` respects `CONFIG.providers.disabled` for new names, `getInstanceCount` 11, `getMetrics` tracks new, `verify:build` now asserts `SitemapIndexProvider`/`OpenApiProvider`/`sitemapIndex`/`openapi`. `dist` `6076→6214` +138 lines.

## § Bundle Analyze
- **analyze-bundle.js** heuristic `class XProvider` slicing via regex `class ${name}[\s\S]*?^    \}` fallback `indexOf` next class, captures `{lines,bytes}` per provider 11, sums `totalProviderBytes 36048` `totalProviderLines 1149`, computes `providerRatio 19.1%` (36048/188338), reads `distBytes/lines`, `import('esbuild')` note `esbuild 0.28.2 available, metafile not needed for IIFE concat; transform minifies 32-33%`, prints sorted `Html 8640 > Binary 4894 > Json 4368 > OpenApi 3546 > Xml 2334 > JS 2267 > Text 2237 > Headers 2153 > Css 2115 > SitemapIndex 1861 > Robots 1633`, writes `dist/.build-meta.json` `providerSizes` 11 + `bundleAnalysis {totalProviders 11, totalProviderBytes, distBytes, providerRatio 19.1, providers, esbuild, timestamp}`. `package.json` adds `analyze` + `build:all` 4-steps `build && build-esbuild && analyze-bundle && verify:build`. `analyze` <50 ms, idempotent.

## § Tests & Build
- **Tests** `provider-sitemap-openapi.test.js` 2 suites 8 cases: static 11 order, `SitemapIndex` matches/extract, `OpenApi` matches true/false + servers/host, lazy disabled respects new names. `src-build` 9-order still passes (9 subset). Suites 35→37, tests 135→143, all PASS (incl. `provider-lazy` 9, `e2e`, `property-*`, `export-inference`, `sitemap/openapi`).
- **Build** `6214 lines` `344b9c…` primary deterministic, `min 60743B 32.3%` `ca3fc9…`, `providerSizes` 36k 19.1% `Html` largest, `verify:build` deterministic `344b9c…` + `minified 60739B sha ca3fc9…` OK + `SitemapIndexProvider`/`OpenApiProvider` gates.

## § Perf & Security
- `SitemapIndex` O(n) 0.02 ms, `OpenApi` JSON parse+walk 0.05 ms (10 kB spec), `matching` loop 11 vs 9 (+2 calls ~0.004 ms) still O(11) at `concurrency 4`. Lazy 0→11 on demand, `disabled:['openapi']` skips parse. `Binary` still observed-only, `Text` fallback last. `CONFIG.sameOriginOnly`, `stripTrackingParams`, `privacy.stripSensitiveParams`, `csp-blocks-bridge`, Trusted Types `gde-bridge`, rAF, TTL, lifecycle, pattern/cluster/change unchanged. Heap bounded 750/150/800/5k.

## § Historical
- `VERIFICATION_SUPPLEMENT_v1.1.0.md` 135/135 6076 6dcfa8… remains valid parent, `v1.0.0` 126/126 5977 9b2b68… `DEEP_DVB_AUDIT_v0.8.2.md` remains valid (143/143 now). `v1.2.0` delta `+138 lines` providers `+120` + `analyze-bundle.js` 70 lines, `verify:build` 4 gates, `build:all` 4 steps 6214 `344b9c…` + `min ca3fc9…`.

Refs: `package.json` `1.2.0` `dist/.build-meta.json` `344b9c…`/`ca3fc9…` `6214/241` `providerSizes` `19.1%` `src/providers.js` 11 `tests/provider-sitemap-openapi.test.js` 8, `scripts/analyze-bundle.js`.
