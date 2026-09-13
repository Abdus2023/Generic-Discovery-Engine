# src — Modular Prelude (v1.2.0 — SitemapIndex/OpenAPI)

This directory is the **modular prelude** for the Generic Discovery Engine.

`dist/generic-discovery-engine.user.js` (6,214 lines, sha256 344b9c… + `dist/generic-discovery-engine.min.js` 60k 32.3% ca3fc9… + bundle 19.1%) is the runnable artifact, logical sections mirrored here as ES modules:

- `config.js` — `CONFIG` (v8, 84 keys, `export const CONFIG`)
- `utils.js` — `canonicalizeUrl`, `isAllowedUrl`, `fnv1a32`, `makeFingerprint`, `originOf`, `extractUrlPattern`, `clusterKeyForCandidate`, `extractUrlsFromText`/`Css`/`Xml` (wired to `CONFIG`)
- `models.js` — `Candidate`, `Observation`, `Discovery`, `ResourceRecord` (planned)
- `knowledge.js` — `KnowledgeBase` (planned)
- `ledger.js` — `DecisionLedger` (planned)
- `providers.js` — `ProviderRegistry` + 11 providers ordered `Html→…→Text` (planned)
- `engine.js` — `GenericDiscoveryEngine` (planned)

`scripts/build.js` now verifies that all 7 `src/*.js` exist and are non-empty and that `dist` header `@version` matches `package.json` before capturing `sha256`/`lines`/`size` → `dist/.build-meta.json`. `scripts/verify-build.js` additionally checks the 11-provider order and `extractUrlPattern` presence. v0.8.2 export hardening adds `getCoverageMetrics()` inference + `exportData().inference` (see ADR 020). Future `v0.9.0` will make `scripts/build.js` a true bundler (`src/` → `dist/` with header preservation).

Verification: `npm run verify:build` deterministic (src 7 OK, 344b9c… 6214 lines + min ca3fc9… + analyze 19.1%); `npm test` 143/143 PASS (incl. `tests/src-build.test.js` 6 cases + `tests/provider-lazy.test.js` 9 cases + `tests/provider-sitemap-openapi.test.js` 8 cases); `npm run coverage:check` 85/75/80.

Lazy providers (v1.1): `CONFIG.providers {lazy:true, disabled:[]}` → `ProviderRegistry` factories + `getMetrics` + `getInstanceCount` + `getProviderMetrics` + `export.providers` (see ADR 024). `npm run build:all` produces deterministic concat + esbuild minify.

Providers 11 (v1.2): `SitemapIndexProvider` sitemapindex 0.90 + `OpenApiProvider` openapi 0.95 + 11-order pipeline, `analyze-bundle.js` 19.1% (see ADR 025/026). `npm run build:all` 4 steps deterministic.
