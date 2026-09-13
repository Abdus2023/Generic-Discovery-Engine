# ADR 026 — Bundle Analyze (esbuild metafile + provider size breakdown)

**Status:** accepted (v1.2.0)  
**Transcript:** 1.2 bundle analysis — provider cost visibility  
**Code:** `scripts/analyze-bundle.js`, `package.json` `analyze`+`build:all`, `dist/.build-meta.json` `providerSizes`+`bundleAnalysis`

## Context
v1.1.0 added `esbuild` transform minify (`dist/*.min.js` 58k 32.3% `106668…`) but no visibility into which provider dominates bundle cost. With 9→11 providers (36k 19.1% of dist 188k) and future tree-shaking planned, operators need per-provider line/byte breakdown to decide `disabled` (e.g. `HtmlProvider` 8640 B 326 lines vs `RobotsProvider` 1633 B 41 lines). `esbuild` metafile not yet emitted; manual `wc -l` insufficient. `verify:build` asserts hash/lines but not cost. Need `npm run analyze` for CI size budget.

## Decision
- **Script** `scripts/analyze-bundle.js` — reads `dist/generic-discovery-engine.user.js` + `src/providers.js`, heuristically slices `class XProvider` blocks via regex `class ${name}[\s\S]*?^    \}` or `indexOf` next class fallback, captures `{lines, bytes}` per provider (11), sums `totalProviderBytes/lines`, computes `providerRatio = totalProviderBytes/distBytes`, reads `distBytes/lines`, attempts `import('esbuild')` for metafile note (`esbuild 0.28.2 available, metafile not needed for IIFE concat; transform minifies 32-33%`), prints sorted table `TOTAL providers 36048 B 1149 lines (19.1% of dist)` + `DIST total 188338 B 6214 lines`, writes `dist/.build-meta.json` `providerSizes` (map) + `bundleAnalysis {totalProviders, totalProviderBytes, distBytes, providerRatio, providers, esbuild, timestamp}`.
- **Package** `package.json` adds `scripts.analyze = node scripts/analyze-bundle.js` and updates `build:all = build && build-esbuild && analyze-bundle && verify:build` (was `build && build-esbuild && verify:build`). `analyze` is additive, not gate; `verify:build` remains deterministic (hash + provider presence).
- **Meta** `dist/.build-meta.json` now includes `providerSizes` 11 entries + `bundleAnalysis` (sorted breakdown, ratio 19.1%, timestamp). CI can assert `providerRatio < 25%` or `distBytes < 200k` via `analyze` output.

## Consequences
- **+** `npm run analyze` reports `Html 8640 > Binary 4894 > Json 4368 > OpenApi 3546 > Xml 2334 > JS 2267 > Text 2237 > Headers 2153 > Css 2115 > SitemapIndex 1861 > Robots 1633` — guides `disabled` tuning and future tree-shaking (e.g. disabling `Html` not viable, but `Text`/`Binary` 7k could be  disabled for API-only crawl). `bundleAnalysis` JSON in meta enables `dashboard` visualization.
- **+** Zero runtime cost (build-time only); `analyze` idempotent, runs in `<50 ms`, does not affect `dist` hash. `build:all` now 4 steps keeps `verify:build` deterministic (hash still `344b9c…` primary).
- **−** Heuristic provider slicing via regex fallback may drift if `src/providers.js` formatting changes (e.g. extra indent); fallback `indexOf` mitigates. `esbuild` metafile not yet full `esbuild.build` with `metafile:true` (future ESM entry will emit true metafile); current `note` placeholder suffices.

## Links
- Code: `scripts/analyze-bundle.js` `providerSizes` `bundleAnalysis`, `dist/.build-meta.json` `19.1%`, `package.json` `analyze`.
- Tests: 8 cases in ADR 025 cover provider logic; `analyze` proven via `node scripts/analyze-bundle.js` manual run (1149 lines 36048 B).
- Prior: ADR 024 lazy+esbuild, ADR 025 providers, `VERIFICATION_SUPPLEMENT_v1.1.0.md`.
