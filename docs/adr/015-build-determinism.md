# ADR 015 — Build Determinism (hash + line count + verify)

**Status:** accepted (v0.7.9)  
**Transcript:** Hygiene split 2.2 MB → dist source of truth, residual “dist is not built”  
**Code:** `scripts/build.js`, `scripts/verify-build.js`, `dist/.build-meta.json`, `package.json` `build`/`verify:build`, `docs/ci/verify.yml.example` build step

## Context
`dist/generic-discovery-engine.user.js` (5,526 lines→5,597 lines) is the runnable artifact but is still hand-edited (no `src/` split). No mechanism proved that the committed `dist` equals a deterministic build; a manual edit that changed `candidateTTL` or `lifecycle` without bumping `package.json` version would pass `node --check` but be semantically drifted. Prior `verify.yml` only checked `size` via `fs.statSync`, not hash.

## Decision
- Add `scripts/build.js` (deterministic): reads `dist/generic-discovery-engine.user.js`, computes `sha256`, `lines` (`split('\n').length`), `size`, reads `package.json` version, writes `dist/.build-meta.json` `{ version, file, sha256, lines, size, builtAt, node }`. No random, no timestamp in `dist` itself (forbidden patterns `builtAt`, `__RANDOM__` in `verify-build`).
- Add `scripts/verify-build.js`: recomputes `sha256`/`lines`/`size`, asserts no forbidden patterns, asserts `dist` header `@version` and `v${version} —` banner match `package.json` version, asserts `extractUrlPattern` present (new feature), and if `dist/.build-meta.json` exists, asserts `sha256` and `version` match (must run `npm run build` after `dist` edit).
- Add `package.json` scripts `build` (`node scripts/build.js && npm run verify:build`) and `verify:build` (`node scripts/verify-build.js`), and `docs/ci/verify.yml.example` step `Build determinism` (`npm run verify:build`). `.gitignore` keeps `node_modules`/`coverage` but `dist/.build-meta.json` is committed (small, deterministic).

## Consequences
- **+** `npm run verify:build` fails if `dist` drifted from `package.json` version or from `dist/.build-meta.json` (must `npm run build`); catches version/header mismatch without `src/` split.
- **+** `dist/.build-meta.json` is reproducible: same `dist` content → same `sha256`/`lines`/`size` regardless of `builtAt`/`node` (those are meta only).
- **−** Until `src/` split, `build.js` is a stub (captures hash, does not rebuild from `src/`). Future v0.8.0 will replace stub with `src/` → `dist` bundler; `verify-build` already enforces hash, so transition is non-breaking.

## Links
- Scripts: `scripts/build.js`, `scripts/verify-build.js`, `dist/.build-meta.json`.
- Tests: `tests/verify-p0-fixes.test.js` asserts `verify:build` in `package.json` and `scripts/verify-build.js` exists.
- CI: `docs/ci/verify.yml.example` build step.
