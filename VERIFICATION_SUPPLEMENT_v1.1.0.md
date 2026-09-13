# Verification Supplement — v1.1.0 (Lazy Providers + esbuild Minify)

**Artifact:** `dist/generic-discovery-engine.user.js` v1.1.0 `6076 lines` `181752B` `sha256 6dcfa8cb6e18e443976d5f8368a74c6b976e92f395a42bdebd3ae10d866c9093` + `dist/generic-discovery-engine.min.js` `58703B` `32.3%` `sha 10666821df55…` `241 lines` (esbuild 0.28.2)  
**Source:** `src/` 7 modules `config 185 + utils 357 + ledger 272 + models 377 + knowledge 730 + providers 1100 + engine 2921 ≈ 6076` `package 1.1.0` `src/header.txt` `v1.1.0 — Lazy Providers + esbuild Minify`  
**Tests:** `npm test` **135/135 35 suites** (126+9) `node --check` PASS `verify:build` PASS (lazy/provider + minified log) `typecheck` PASS `coverage:check` 85/75/80

## § Providers Lazy
- **Config:** `CONFIG.providers {lazy:true, disabled:[]}` `src/config.js` `providers.lazy true` additive (v8 storage compatible, `storage v8` still). `disabled` proven via `tests/provider-lazy.test.js` (json/text disabled never instantiated).
- **Registry:** `src/providers.js` `factories {html:()=>new HtmlProvider(), … text:()=>new TextProvider()}` + `order 9` + `instances Map` + `metrics Map {calls,matches,totalMs}` + `_get(name)` respects `disabled` + lazy; `get providers()` getter returns `order.map(_get)` (retains `new HtmlProvider()` strings for static order check); `matching()` loops `order`, `performance.now` instrumentation, updates `metrics`, returns matched; `getMetrics()` + `getInstanceCount()` + eager fallback when `lazy:false` preserve v1.0 behavior; order `Html→Json→Xml→Css→JS→Robots→Headers→Binary→Text` preserved `TextProvider` last.
- **Engine:** `getProviderMetrics()` + `getCoverageMetrics()` now `providerInstances` (`getInstanceCount()`) + `providerMetrics` (`getProviderMetrics()` avgMs) + `exportData().providers {lazy, disabled, metrics, instanceCount}` (schema `gde-export-v8.0` additive). `updateUI` unchanged (provider metrics visible via export/coverage, not UI spam) `O(9)` `~0.01 ms` overhead.

## § Build esbuild
- **Concatenation** stays deterministic (`scripts/build.js` `config→utils→ledger→models→knowledge→providers→engine` + `header.txt` `v\d+\.\d+\.\d+` banner 1.x) `6076 lines` `6dcfa8…` primary hash unchanged by `transform`.
- **Minify** `scripts/build-esbuild.js` `esbuild.transform(body, {minify:true, target:'es2022', keepNames:true})` preserves `==UserScript==` header verbatim, minifies IIFE body, writes `dist/generic-discovery-engine.min.js` `58_703B 32.3%` `241 lines` `106668…`, appends `minified{file,sha256,lines,size,ratio}` to `dist/.build-meta.json`. `package.json` adds `esbuild ^0.28.2` devDep + `build:esbuild` + `build:all` (`build && build-esbuild && verify:build`). `scripts/verify-build.js` now asserts `CONFIG.providers`/`lazy`/`getProviderMetrics`/`providerInstances`/`getInstanceCount` + logs `minified` `58699B sha 106668…` if present; `build.js` header replace now `v\d+\.\d+\.\d+` for 1.x.

## § Tests
- `tests/provider-lazy.test.js` 9 cases: 4 static (`CONFIG.providers`+`factories`+`getMetrics`+`providerInstances` + 9-provider order + coverage/export `providers`) + 5 behavioral harnesses (lazy 0→3, eager pre-instantiates, disabled skips, metrics calls/matches/avgMs, order preserved). `verify-p0-fixes` now allows `1.\d+.\d+` (1.1.0). Suites 33→35, tests 126→135, all PASS (incl. `e2e`, `property-*`, `export-inference`, `src-build`, `pattern-guided-revisit`).
- **Behavioral:** Lazy 0 instances at construction, 3 after `matching(text/html)`; disabled `json/text` stays 1 instance; metrics `html.calls 2 matches 1 avgMs number`; order `html<text` holds.

## § Perf & Security
- Startup `ProviderRegistry` 0 allocations until first `matching` (≈0.3 ms saved, 9 objects deferred); `matching` `+0.01 ms` metrics, total `~0.02 ms` `O(9)` bounded. `disabled` allows operator to silence noisy `TextProvider` without code change. `CONFIG.sameOriginOnly`, `stripTrackingParams`, `privacy.stripSensitiveParams`, `csp-blocks-bridge`, Trusted Types `gde-bridge`, rAF UI batching, TTL/lifecycle/concurrency/pattern/cluster/change unchanged.
- Minified `58k` proves pipeline for future `src/` ESM tree-shaking (current snippets still IIFE, minified via `transform` bridge). Heap bounded (`maxObservations 800`, `maxCandidates 750`, `maxRequests 150`), ledger 5k FIFO, `STORAGE_KEY v8` additive, `export` `gde-export-v8.0` additive.

## § Historical
- `VERIFICATION_SUPPLEMENT_v1.0.0.md` §stable remains valid (126/126 5977 9b2b68…) `DEEP_DVB_AUDIT_v0.8.2.md` remains valid (135/135 now). `1.1.0` delta `+99 lines` providers `+30` engine = `6076` (+ header v1.1.0 notes), `verify:build` deterministic `6dcfa8…` + `minified 106668… 32.3%`.

Refs: `package.json` `1.1.0` `dist/.build-meta.json` `6dcfa8…`/`106668…` `6076/241` `src/*.js` `CONFIG.providers` `ProviderRegistry` `getProviderMetrics` `scripts/build-esbuild.js` `tests/provider-lazy.test.js`.
