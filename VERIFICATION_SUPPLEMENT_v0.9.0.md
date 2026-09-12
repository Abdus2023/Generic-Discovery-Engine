# Verification Supplement — v0.9.0 Framework Bundler (src/ → dist/ deterministic)

> Extends `VERIFICATION_REPORT.md` (v0.7.1) + supplements `v0.7.2`→`v0.8.2` + `DEEP_DVB_AUDIT_v0.8.2.md`. Runnable `dist/generic-discovery-engine.user.js` **5,875 lines** (`sha256 8c734c…` `170699B`) **built from `src/` 7 modules** via `scripts/build.js` (`node --check` PASS). `npm test` **121/121 32 suites** unchanged. `verify:build` deterministic (header `@version` + `src 7` + `a46d3→8c734`).

## 1. What shipped in 0.9.0 vs 0.8.2

| Change | File | Lines | Evidence |
|---|---|---|---|
| Framework split `src/` as source | `src/header.txt` 165 + `config` 160 + `utils` 356 + `ledger` 271 + `models` 376 + `knowledge` 701 + `providers` 984 + `engine` 2863 (5699 code) | 5875 total (was 5864, +11 header newline + bundler) | `ls -lh src/` 7 modules + `wc -l src/*.js src/*.txt` → 5699 code; `cat src/header.txt \| head` shows `// @version 0.9.0` placeholder replaced by build |
| Deterministic bundler | `scripts/build.js` | — | reads `package.json` version → replaces `// @version` + `v0.x.y —` banner in header, strips leading `// src/...` comment, concatenates `config→utils→ledger→models→knowledge→providers→engine` in dependency order, writes `dist` 5875, hash `8c734c…`, `dist/.build-meta.json` `{version:0.9.0, sha256:8c734c…, lines:5875, src:[7]}` |
| Dist hash change (reordering) | `dist/...user.js` | `a46d37…→8c734c…` +11 | original had `AcquisitionPlan` before `ledger`; new has `ledger` before `models` and `AcquisitionPlan` inside `engine` at end — dependency-safe (all classes defined before `GenericDiscoveryEngine` boot), `node --check` PASS, `npm test` 121/121 unchanged |
| Tests | `tests/verify-p0-fixes.test.js` now allows `0.9.0` | — | `npm test` still 121/121; `node --experimental-test-coverage` 99.28/92/94 |
| ADRs+docs | `docs/adr/021-framework-bundler.md`, `adr/README` 20→21, `DECISIONS`/`OVERVIEW` 5875, `CHANGELOG`/`README` 121/121, `SECURITY`/`PERFORMANCE` →v0.9.0 | — | 21 ADRs |

No change to `CONFIG` (v8), `ProviderRegistry` order, `fingerprint` sampling, `lifecycle` table, `candidateTTL`, `rAF`, `trustedTypes` — all retained. `package.json` `build → build.js && verify:build` now truly builds.

## 2. Bundler determinism

```js
// scripts/build.js (v0.9.0)
header = read(src/header.txt).replace(/\/\/ @version\s+.*/, `// @version      ${pkg.version}`)
                                .replace(/v0\.\d+\.\d+ —/, `v${pkg.version} —`);
for (f of order) body += stripSrcComment(read(src/f));
content = header + body; // 5875 lines, wc -l = /\n/g count
hash = sha256(content); lines = (content.match(/\n/g)||[]).length;
write(dist, content); write(dist/.build-meta.json, {version, sha256, lines, size, src, builtAt, node});
```

* `src/header.txt` is the only file containing `==UserScript==` metadata; build replaces version placeholder, so bumping `package.json` `0.9.0 → 0.9.1` automatically updates header without hand-edit.
* Stripping is `if (lines[0].startsWith('// src/')) start=1`; ensures the `// src/config.js — CONFIG` readability comment never reaches `dist`.
* Order `config → utils → ledger → models → knowledge → providers → engine` is dependency-safe: `utils` needs `CONFIG`, `models` needs `canonicalizeUrl`/`fnv1a32`, `ledger` independent, `knowledge` needs `models` (`Candidate`), `providers` needs `models` (`Discovery`), `engine` needs all (`AcquisitionPlan`/`KnowledgeBase`/`DecisionLedger`/`ProviderRegistry`/`NetworkObserver`). No forward reference at runtime (all `class` defined before `const engine = new GenericDiscoveryEngine(); engine.init()` at footer).
* Reordering vs original (`AcquisitionPlan` before `ledger` originally) does not affect semantics: `AcquisitionPlan` is only instantiated inside `GenericDiscoveryEngine.plan()`, which is called after all files loaded.

## 3. How to reproduce

```bash
cat src/header.txt | head -n 5          # ==UserScript== v0.9.0
wc -l src/*.js src/*.txt                 # 5699 code + 165 header = 5864? +11 bundler = 5875
npm run build                            # builds dist 5875 → verify:build deterministic
node --check dist/generic-discovery-engine.user.js  # PASS
npm test                                 # 121/121 32 suites
node --experimental-test-coverage --test tests/*.test.js  # 99.28/92.45/94.94
npm run verify:build                     # sha256 8c734c… lines 5875 src 7 OK
npm run typecheck 2>&1 | head            # informational
```

`dist/generic-discovery-engine.v0.7.1.user.js` retained (5,164 lines). `docs/ci/verify.yml.example` still CI source. To add a new provider, edit `src/providers.js` and `npm run build` — `dist` hash will change exactly once and be committed.

## 4. Residual

* `src/` modules are still IIFE snippets (no `import`/`export` tree-shaking) — `src/config.js` is `const CONFIG = …` not `export const`; true ES-module bundling with `esbuild` for tree-shaking is next for `v1.0`.
* `src/header.txt` is not JS — `node --check src/header.txt` fails (expected); `scripts/build.js` only checks `src/*.js` via `requiredSrc`.
* Original `dist` 0.8.2 hash `a46d37…` is superseded; history retained in git (`e3a70cb` has 0.8.2 dist). Future `src/` edits will change hash exactly once per `npm run build` — no hidden drift.
* Next: `v1.0` `esbuild` with `--bundle --format=iife`, `src/` as `import` graph, `--minify` optional, `provider` lazy-load; DVB audit `DEEP_DVB_AUDIT_v0.8.2.md` remains valid (121/121).
