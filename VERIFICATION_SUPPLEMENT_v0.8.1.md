# Verification Supplement — v0.8.1 Modular Prelude + Export Hardening

> Extends `VERIFICATION_REPORT.md` (v0.7.1) + `VERIFICATION_SUPPLEMENT_v0.7.2.md` + `VERIFICATION_SUPPLEMENT_v0.7.6.md` + `VERIFICATION_SUPPLEMENT_v0.7.7.md` + `VERIFICATION_SUPPLEMENT_v0.7.8.md` + `VERIFICATION_SUPPLEMENT_v0.7.9.md` + `VERIFICATION_SUPPLEMENT_v0.8.0.md`. Runnable: `dist/generic-discovery-engine.user.js` (5,784 lines, CONFIG v8, `node --check` PASS). `npm test` 115/115 PASS (31 suites). `npm run verify:build` sha256 031c3… lines 5784 deterministic (src 7 files) · `npm run coverage:check` gate PASS 85/75/80 · `npm run typecheck` informational. `src/` mirror 7 files.

## 1. What shipped in 0.8.1 vs 0.8.0

| Change | File | Lines | Evidence |
|---|---|---|---|
| Modular prelude `src/` 7 files | `src/config.js` (CONFIG v8 84 keys export), `src/utils.js` (canonicalizeUrl/fnv1a32/makeFingerprint), `src/{models,knowledge,ledger,providers,engine}.js` placeholders, `src/README.md` plan | +7 files | `ls src/` 7, `grep -n version src/config.js` shows `version: 8`, `verify-p0` now allows `0.8.[01]` |
| Dist header bump + patch notes | `dist/...user.js` | +11 (5,773→5,784) | `head -n 25 dist/...user.js` shows `@version 0.8.1` + `v0.8.1 — Modular Prelude + Export Hardening` patch notes |
| Build src gate | `scripts/build.js` | + src check | `grep -n src/ scripts/build.js` shows 7-file exist + non-empty + header `@version` matches pkg before hash |
| Verify src + order | `scripts/verify-build.js` | + src + order | `grep -n src\\|RobotsProvider\\|ProviderRegistry` shows src-mirror 7 OK + ordered `Html→…→Text` 9 check + meta hash/version |
| Build script hardening | `package.json` | `build → build.js && verify:build` | `grep build package.json` shows atomic `&& npm run verify:build` |
| Tests | `tests/src-build.test.js` | +6 tests | src 7 files, CONFIG version, header sync, meta hash/version, 9-provider order, pattern/cluster exports |
| Static check extension | `tests/verify-p0-fixes.test.js` | +2 regex | version regex now `0.8.[01]`, build no longer checks for `0.8.0` only |
| ADRs + docs | `docs/adr/019-modular-prelude.md`, `adr/README` (18→19), `DECISIONS`/`OVERVIEW` 5,784, `CHANGELOG`/`README` 115/115, `PERFORMANCE`/`SECURITY` →v0.8.1 | — | 19 ADRs cover control-plane through Phase 4 prelude |

No change to `candidateTTL`, `lifecycle` guard, `rAF`, `pattern/cluster`, `fingerprint` sampling, `privacy`, `Trusted Types`, provider semantics — all retained. `CONFIG.version` stays 8 (storage compatible). Dist hash changes only because header + patch notes changed, not logic.

## 2. Modular prelude: why a mirror, not a bundler yet

`dist/generic-discovery-engine.user.js` is 5,784 lines with GM_ globals, IIFE, and Userscript header block (`@grant`, `@connect`). A full `src/` → `dist/` bundler (esbuild/rollup) would need to preserve that header verbatim and keep `sha256` deterministic. To avoid invalidating the `verify:build` hash gate mid-flight, v0.8.1 ships the `src/` mirror as **verified placeholders**:

- `src/config.js` is a real extract: `grep CONFIG src/config.js` shows the same 84-key object as dist, now `export const CONFIG = …; export default CONFIG;`.
- `src/utils.js` re-exports canonical helpers (`canonicalizeUrl` with `stripSensitiveParams` guard, `fnv1a32`, `makeFingerprint` with 1M sampling) and `import { CONFIG } from './config.js'` — proven by `grep canonicalizeUrl src/utils.js`.
- Remaining five (`models`/`knowledge`/`ledger`/`providers`/`engine`) are `// placeholder — see src/README.md` with the v0.9.0 plan: they document the intended split but do not yet duplicate logic, so reviewing them cannot hide a drift (build fails if any `src/*.js` is missing or empty).
- `dist/.build-meta.json` now records `src: [config.js,…,engine.js]` alongside `sha256`/`lines`, so any future `src/` edit that is not reflected in `dist` is caught by `verify:build`.

Cost: `src/` adds ~12 kB to repo, zero runtime cost (not loaded by the userscript). Future v0.9.0 will concatenate `src/**/*.js` with header preservation; the current gate guarantees that migration will be explicit (hash will change once and be committed).

## 3. Build determinism hardened (ADR 015 → 019)

```bash
npm run build          # build.js → meta → verify-build atomically
npm run verify:build   # re-hashes dist, checks header, src, order, forbidden builtAt
```

- `scripts/build.js` (v0.8.1): existence + non-empty check for 7 `src/` files, header `@version` == `package.json` `version`, then `sha256` + `wc -l` (newline count) → `dist/.build-meta.json` `{ version:"0.8.1", sha256:"031c3b…", lines:5784, size:167064, src:[…], builtAt, node }`.
- `scripts/verify-build.js` (v0.8.1): re-hashes dist, asserts `@version`/`vX.Y.Z —` banner, forbidden `builtAt`/`__RANDOM__` absent, `extractUrlPattern` + `RobotsProvider` present, `ProviderRegistry` 9 ordered, `src` 7 present, meta `sha256` + `version` match (otherwise `run: npm run build`).
- `package.json` `build` is now `node scripts/build.js && npm run verify:build` — a second invocation cannot leave stale meta.

Proven by `tests/src-build.test.js` (6 cases): missing `src/*.js` → build fails; header/pkg mismatch → verify fails; provider order wrong → verify fails; hash drift → verify fails. Existing `verify-p0-fixes` still checks `liveCount`/`visited`/`maxObservationsInMemory`/`emittedForObservation`/`seen`/`getCoverageMetrics`/`hardening`/`trust`/`rAF`/`TTL`/`lifecycle`/`concurrency`/`pattern`/`robots/headers/change` — none regressed.

## 4. How to reproduce

```bash
npm run check          # node --check both dist files
npm test               # 115/115 PASS 31 suites ~2.0s
npm run coverage       # native 99.2%+/92%+/94%+
npm run coverage:check # c8 99.2%+/92%+/88%+ gate PASS
npm run verify:build   # sha256 031c3baff656… lines 5784 src 7 OK deterministic
npm run build          # regenerates dist/.build-meta.json + re-verifies
npm run typecheck 2>&1 | head -n 50  # informational
node --test tests/src-build.test.js # 6/6
node --test tests/provider-robots-headers.test.js # 12/12
```

`dist/generic-discovery-engine.v0.7.1.user.js` (5,164 lines) retained; `docs/ci/verify.yml.example` is CI source (copy to `.github/workflows/verify.yml` with PAT that has `workflows` scope). `src/README.md` documents the v0.9.0 bundler plan; no new runtime dependency.

## 5. Residual

- `src/` placeholders still contain no engine logic — `dist` remains monolith, and tree-shaking is not yet possible. Explicit in `src/README.md` and ADR 019; the mirror is the gate, not the runtime.
- `HeadersProvider` still only handles `Link` + `Location`; `Content-Location`/`Refresh`/`X-Robots-Tag` deferred (same as 0.8.0).
- `changed` status still informational (no auto-requeue); future `revisitChanged` will use either `candidateTTL` or explicit revisit, now easier to test once `src/knowledge.js` lands.
- Next for v0.9.0: concatenate `src/config.js→utils→models→knowledge→ledger→providers→engine` with header preservation via esbuild-style wrapper, keep `verify:build` hash, move provider/knowledge tests to import from `src/` and test `dist` via E2E only.
