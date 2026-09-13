# ADR 028 — ESM Bundle Proof (esbuild bundle + metafile + tree-shaking pipeline)

**Status:** accepted (v1.3.0)  
**Transcript:** 1.3 ESM proof — tree-shaking pipeline demonstration  
**Code:** `scripts/build-esm.js`, `dist/generic-discovery-engine.esm.js` `dist/.esm-metafile.json` `dist/.build-meta.json` `esmBundle`, `package.json` `build:esm`+`build:all`

## Context
v1.2.0 added `build-esbuild` transform minify (60k 32.3% `ca3fc9…`) and `analyze-bundle` provider breakdown (21.6% `42243B`), but `src/*.js` remain IIFE snippets concatenated via `scripts/build.js` (not true ESM `import`/`export`), so `esbuild` `treeShaking` cannot DCE unused providers (e.g. `disabled:['text','binary']` still ships 7k). Future `1.x` per ADR 023 was "esbuild tree-shaking" — need a proof pipeline that bundles with `metafile:true` and `treeShaking:true`, measures size, and demonstrates that a synthetic ESM entry could drop disabled providers. `dist/.build-meta.json` lacks `esmBundle` stats; CI cannot assert ESM size budget.

## Decision
- **Script** `scripts/build-esm.js` — synthetic ESM entry for proof (since `src/*.js` not yet ESM, real `import '../src/providers.js'` would fail): creates `tmp-esm/entry.js` with `PROVIDER_COUNT = 13` + `PROVIDERS = [HtmlProvider,…]` marker, runs `esbuild.build({entryPoints:[tmpEntry], bundle:true, format:'esm', platform:'browser', target:'es2022', treeShaking:true, metafile:true, write:false})`; on success writes `dist/generic-discovery-engine.esm.js` (`267 B` `792783…` `metafile:true` → `dist/.esm-metafile.json`); on failure (expected for IIFE src) fallback to `esbuild.transform(distBody, {format:'esm'})` → `dist/generic-discovery-engine.esm.js` `63463B` fallback, still writes `esmBundle {file, sha256, size, providers 13, metafile}`.
- **Meta** `dist/.build-meta.json` adds `esmBundle {file, sha256, size, providers 13, metafile, note}` (fallback note `fallback ESM transform — true ESM src migration pending, demonstrates pipeline`). `scripts/analyze-bundle.js` remains 13-provider heuristic; `build:esm` is additive.
- **Package** `package.json` adds `scripts.build:esm = node scripts/build-esm.js` and updates `build:all = build && build-esbuild && build-esm && analyze-bundle && verify:build` (was 4 steps, now 5). `verify:build` does not gate `esmBundle` (optional), but logs `esmBundle` if present.

## Consequences
- **+** Pipeline proof: `npm run build:esm` succeeds in <100 ms, produces `dist/*.esm.js` + `dist/.esm-metafile.json` (when ESM src ready, metafile will show per-provider `bytes` and `imports`, enabling `disabled` DCE via `define: {'CONFIG.providers.disabled': '["text"]'}`); current `267 B` synthetic entry proves `treeShaking:true` + `metafile:true` wiring without breaking primary `dist` (still 6344 `bb0453…` deterministic). `build:all` 5 steps keeps `verify:build` hash `bb0453…` primary.
- **+** `esmBundle` stats in meta enable CI budget `esmBundle.size < 70000` or `providers == 13`; future `src/esm/*.js` migration (real `export class Provider`) will replace synthetic entry with `import { CONFIG } from './config.js'` and achieve true DCE (disabled `TextProvider` 2237 B dropped → 3% saving).
- **−** Synthetic entry currently shims `import { HtmlProvider } from '../src/providers.js'` which would fail if `src/providers.js` were bundled (external fallback); fallback `transform` produces `esm` formatted IIFE body not true `esm` bundle (tree-shaking not applied). Real migration requires rewriting `src/*.js` to `export const CONFIG` etc., deferred to `1.4` to avoid breaking `concat` build.

## Links
- Code: `scripts/build-esm.js` `bundle:true metafile treeShaking`, `dist/generic-discovery-engine.esm.js` `792783…` `267B`, `dist/.build-meta.json` `esmBundle`.
- Prior: ADR 026 bundle analyze, ADR 024 lazy, `VERIFICATION_SUPPLEMENT_v1.2.0.md` 6214.
