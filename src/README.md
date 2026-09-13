# src — Modular Prelude (v1.4.0 — Health + Concurrent Providers)

This directory is the **modular prelude** for the Generic Discovery Engine.

`dist/generic-discovery-engine.user.js` (6,394 lines, sha256 4f2c63… + `dist/generic-discovery-engine.min.js` 65k 32.6% 6c3103… + `dist/generic-discovery-engine.esm.js` 267B + bundle 21.1%) is the runnable artifact, logical sections mirrored here as ES modules:

- `config.js` — `CONFIG` (v8, 84 keys, `export const CONFIG`)
- `utils.js` — `canonicalizeUrl`, `isAllowedUrl`, `fnv1a32`, `makeFingerprint`, `originOf`, `extractUrlPattern`, `clusterKeyForCandidate`, `extractUrlsFromText`/`Css`/`Xml` (wired to `CONFIG`)
- `models.js` — `Candidate`, `Observation`, `Discovery`, `ResourceRecord` (planned)
- `knowledge.js` — `KnowledgeBase` (planned)
- `ledger.js` — `DecisionLedger` (planned)
- `providers.js` — `ProviderRegistry` + 13 providers ordered `Html→…→Text` (planned)
- `engine.js` — `GenericDiscoveryEngine` (planned)

`scripts/build.js` now verifies that all 7 `src/*.js` exist and are non-empty and that `dist` header `@version` matches `package.json` before capturing `sha256`/`lines`/`size` → `dist/.build-meta.json`. `scripts/verify-build.js` additionally checks the 13-provider order and `extractUrlPattern` + `getHealthMetrics` presence. v0.8.2 export hardening adds `getCoverageMetrics()` inference + `exportData().inference` (see ADR 020). Future `v0.9.0` will make `scripts/build.js` a true bundler (`src/` → `dist/` with header preservation).

Verification: `npm run verify:build` deterministic (src 7 OK, 4f2c63… 6394 lines + min 6c3103… + esm 792783… + analyze 21.1%); `npm test` 160/160 PASS (incl. `tests/src-build.test.js` 6 cases + `tests/provider-lazy.test.js` 9 cases + `tests/provider-sitemap-openapi.test.js` 8 cases + `tests/provider-wellknown-manifest.test.js` 7 cases + `tests/health-concurrent.test.js` 10 cases); `npm run coverage:check` 85/75/80.

Health+concurrent (v1.4): `CONFIG.health {enabled,maxRecentErrors,slowProviderMs}` + `getHealthMetrics()` + `providers.concurrent` + `Promise.all` parallel with dedup `processDiscoveries` + `exportData().health` (see ADR 029/030). `npm run build:all` 5 steps deterministic.

Providers 13 (v1.3): `WellKnownProvider` wellKnown 0.80/0.70 + `ManifestProvider` manifest 0.85/0.80 + 13-order pipeline, `build-esm.js` ESM bundle proof 267B + `analyze-bundle.js` 21.6% (see ADR 027/028). `npm run build:all` 5 steps deterministic.

Providers 11 (v1.2): `SitemapIndexProvider` sitemapindex 0.90 + `OpenApiProvider` openapi 0.95 + 11-order pipeline, `analyze-bundle.js` 19.1% (see ADR 025/026). `npm run build:all` 4 steps deterministic.

Lazy providers (v1.1): `CONFIG.providers {lazy:true, disabled:[], concurrent:false}` → `ProviderRegistry` factories + `getMetrics` + `getInstanceCount` + `getProviderMetrics` + `export.providers` (see ADR 024). `npm run build:all` produces deterministic concat + esbuild minify.
