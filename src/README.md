# src — Modular Prelude (v0.8.1)

This directory is the **modular prelude** for the Generic Discovery Engine.

`dist/generic-discovery-engine.user.js` (5,977 lines, sha256 9b2b68…) is still the runnable artifact, but its logical sections are now mirrored here as ES modules:

- `config.js` — `CONFIG` (v8, 84 keys, `export const CONFIG`)
- `utils.js` — `canonicalizeUrl`, `isAllowedUrl`, `fnv1a32`, `makeFingerprint`, `originOf`, `extractUrlPattern`, `clusterKeyForCandidate`, `extractUrlsFromText`/`Css`/`Xml` (wired to `CONFIG`)
- `models.js` — `Candidate`, `Observation`, `Discovery`, `ResourceRecord` (planned)
- `knowledge.js` — `KnowledgeBase` (planned)
- `ledger.js` — `DecisionLedger` (planned)
- `providers.js` — `ProviderRegistry` + 9 providers ordered `Html→…→Text` (planned)
- `engine.js` — `GenericDiscoveryEngine` (planned)

`scripts/build.js` now verifies that all 7 `src/*.js` exist and are non-empty and that `dist` header `@version` matches `package.json` before capturing `sha256`/`lines`/`size` → `dist/.build-meta.json`. `scripts/verify-build.js` additionally checks the 9-provider order and `extractUrlPattern` presence. v0.8.2 export hardening adds `getCoverageMetrics()` inference + `exportData().inference` (see ADR 020). Future `v0.9.0` will make `scripts/build.js` a true bundler (`src/` → `dist/` with header preservation).

Verification: `npm run verify:build` deterministic (src 7 OK, 031c3… 5784 lines); `npm test` 115/115 PASS (incl. `tests/src-build.test.js` 6 cases); `npm run coverage:check` 85/75/80.
