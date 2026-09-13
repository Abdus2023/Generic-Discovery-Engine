# Verification Supplement — v1.3.0 (WellKnown + Manifest + ESM Bundle Proof)

**Artifact:** `dist/generic-discovery-engine.user.js` v1.3.0 `6344 lines` `195565B` `sha256 bb04531ec301e411e3ca80725eb37c1ff749dd32e3e8673255d7de22704d8f6a` + `dist/generic-discovery-engine.min.js` `63463B` `32.5%` `sha d4de85bd51de2d93fa00a8518b9b2461be5ef424995ccb362afca4f46741a742` `241 lines` + `dist/generic-discovery-engine.esm.js` `267B` `sha 79278308da66b46aa56eeb68f32248597c8b50cb603ce5a0450dace3bd354951` (esbuild bundle proof)  
**Source:** `src/` 7 modules `config 170 + utils 357 + ledger 272 + models 377 + knowledge 730 + providers 1295 + engine 2921 ≈ 6344` `package 1.3.0` `src/header.txt` `v1.3.0 — WellKnown + Manifest Providers + ESM Bundle Proof`  
**Tests:** `npm test` **150/150 39 suites** (143+7) `node --check` PASS `verify:build` PASS (wellKnown/manifest + minified + esm meta) `typecheck` PASS `coverage:check` 85/75/80, `analyze-bundle` 21.6% `build:esm` metafile

## § Providers 13
- **WellKnownProvider** `name='wellKnown'` — `matches` `/.well-known/` in `requestedUrl` or (`text/plain` + `/Contact:/` + well-known path) or (`looksLikeJson` + well-known path); `recognize` JSON → walk strings → `Discovery 0.80 'wellknown-json-url'`; text → `extractUrlsFromText` → `0.70 'wellknown-text-url'` O(n) ~0.03 ms. Proven via `/.well-known/security.txt` true vs `/page` false, extracts `jwks_uri` `wellknown-json-url`.
- **ManifestProvider** `name='manifest'` — `matches` `manifest.json` or `application/manifest+json` or `looksLikeJson` && `icons/start_url/scope` with `Array.isArray(icons)`; `recognize` emits `icons[].src` `0.85 'manifest-icon'`, `start_url` `0.80`, `scope` `0.75`, `screenshots` `0.80`, `shortcuts[].url` `0.78`, resolving relative via `new URL(url, requestedUrl)` + `canonicalizeUrl` O(icons) ~0.02 ms. Proven via matches `manifest.json` true vs plain false, extracts 4 (2 icons + start_url + scope) with relative `/icon-192.png` → `https://ex/icon-192.png`.
- **Registry** 13 factories `html json xml css javascript robots headers sitemapIndex openapi wellKnown manifest binary text` order `Html→Text` (preserves 11-order), lazy `_get` respects `CONFIG.providers.disabled` new names, `getInstanceCount` 13, `verify:build` now asserts `WellKnownProvider`/`ManifestProvider`/`wellKnown`/`manifest` + 13-order strings. `dist` `6214→6344` +130 `bb0453…`.

## § ESM Bundle Proof
- **build-esm.js** synthetic ESM entry `tmp-esm/entry.js` `PROVIDER_COUNT 13` + `PROVIDERS [HtmlProvider,…]` → `esbuild.build({bundle:true, format:'esm', platform:'browser', target:'es2022', treeShaking:true, metafile:true})` → `dist/generic-discovery-engine.esm.js` `267B` `792783…` + `dist/.esm-metafile.json` (when IIFE src fails, fallback `esbuild.transform(distBody, {format:'esm'})` still writes `esmBundle` note `fallback ESM transform — true ESM src migration pending, demonstrates pipeline`). `dist/.build-meta.json` adds `esmBundle {file, sha256, size, providers 13, metafile:true}`. `package.json` adds `build:esm` + `build:all` 5 steps `build && build-esbuild && build-esm && analyze-bundle && verify:build`. Cost <100 ms.

## § Tests & Build
- **Tests** `provider-wellknown-manifest.test.js` 2 suites 7 cases: static 13 order, WellKnown matches `/.well-known` + json `jwks_uri`, Manifest matches `manifest.json` true vs plain false + extracts 4 + lazy strings. `provider-sitemap-openapi` 8, `provider-lazy` 9, `src-build` 9-order still passes (9 subset). Suites 37→39, tests 143→150, all PASS (incl. `e2e`, `property-*`, `export-inference`, `sitemap/openapi`, `wellKnown/manifest`).
- **Build** `6344 lines` `bb0453…` primary deterministic, `min 63463B 32.5%` `d4de85…`, `esm 267B` `792783…`, `providerSizes` 13 `42243B 21.6%` `Html 8640 > Binary 5031 > Json 4368`, `bundleAnalysis` 13 `1265 lines`, `esmBundle` 13 metafile, `verify:build` deterministic `bb0453…` + `minified 63459B` + `wellKnown/manifest` gates OK.

## § Perf & Security
- `WellKnown` JSON walk 0.03 ms, Manifest 0.02 ms, `matching` loop 13 vs 11 (+2 calls ~0.004 ms) still O(13) at `concurrency 4`. Lazy 0→13 on demand, `disabled:['manifest']` skips manifest parse. `CONFIG.sameOriginOnly`, `stripTrackingParams`, `privacy`, `csp-blocks-bridge`, Trusted Types `gde-bridge`, rAF, TTL, lifecycle, pattern/cluster/change unchanged. Heap bounded 750/150/800/5k.

## § Historical
- `VERIFICATION_SUPPLEMENT_v1.2.0.md` 143/143 6214 344b9c… remains valid parent, `v1.1.0` 135/135 6076, `v1.0.0` 126/126 5977, `DEEP_DVB_AUDIT_v0.8.2.md` remains valid (150/150 now). `v1.3.0` delta `+130 lines` providers `+130` + `build-esm.js` 80 lines, `verify:build` 4 gates, `build:all` 5 steps 6344 `bb0453…` + `min d4de85…` + `esm 792783…`.

Refs: `package.json` `1.3.0` `dist/.build-meta.json` `bb0453…`/`d4de85…`/`792783…` `6344/241/267` `providerSizes` `21.6%` `13` `esmBundle` `tests/provider-wellknown-manifest.test.js` 7, `scripts/build-esm.js`.
