# Verification Supplement — v1.0.0 Stable (generic discovery loop feature-complete)

> Extends `VERIFICATION_REPORT.md` (v0.7.1) + supplements `v0.7.2`→`v0.9.1` + `DEEP_DVB_AUDIT_v0.8.2.md`. Runnable `dist/generic-discovery-engine.user.js` **5,977 lines** (`sha 9b2b68…` `176645B`) built from `src/` 7 modules via bundler (`node --check` PASS). `npm test` **126/126 33 suites** (was 126/126). `verify:build` deterministic (header + src 7 + `9b2b68…`).

## 1. What shipped in 1.0.0 vs 0.9.1

| Change | File | Lines | Evidence |
|---|---|---|---|
| Version stable | `package.json` `1.0.0` + `src/header.txt` `v1.0.0 — Stable` | `5969→5977` (+8 header patch notes) `9b2b68…` | `grep -n "@version" src/header.txt` `1.0.0`, `grep -n "v1.0.0 —" src/header.txt` `Stable`, `cat package.json \| grep version` `1.0.0` |
| No runtime delta | `src/config.js` `CONFIG` v8 unchanged, `src/knowledge.js`/`engine.js` unchanged | — | `diff <(git show HEAD~1:src/config.js) src/config.js` only header version; `npm test` 126/126 unchanged |
| Build | `dist/.build-meta.json` `1.0.0` `9b2b68…` 5977 | — | `npm run verify:build` `9b2b68…` deterministic |
| Tests | `tests/verify-p0-fixes.test.js` now allows `1.0.0` | — | `npm test` 126/126 |
| ADRs+docs | `docs/adr/023-stable-1.0.md`, `adr/README` 22→23, `DECISIONS`/`OVERVIEW` 5977, `CHANGELOG`/`README` 126/126, `SECURITY`/`PERFORMANCE` →1.0.0 | — | 23 ADRs |

## 2. Why 1.0.0 is stable

* **Control-plane closed:** DVB loop `Candidate → AcquisitionPlan → OriginController → Acquisition → Observation → ProviderRegistry (9) → Discovery → KnowledgeBase (pattern/cluster, fingerprint, TTL, lifecycle, change, suggest/changed) → Scheduler (adaptive, priority, revisit/pattern-guided) → Ledger (12 types 5k) → Export (coverage + inference) → Persist → UI (rAF)` — all ADRs accepted, no P0/P1, 126/126.
* **Deterministic:** `src/` 7 modules + `header.txt` → `dist` via `scripts/build.js` `sha 9b2b68…` `5977` `wc -l`, `verify:build` asserts `header @version`, `src 7`, `patternCount`/`inference`/`revisitChanged`/`patternGuided` present, meta hash/version match.
* **Storage compatible:** `CONFIG.version 8`, `STORAGE_KEY v8`, `gde-export-v8.0` + `inference` additive, ledger `export/restore` 5k FIFO — 1.0 restores 0.9.1 state.
* **Deep audit valid:** `DEEP_DVB_AUDIT_v0.8.2.md` (121/121) remains valid for 126/126 (only +5 pattern/revisit tests, both opt-in false by default).
* **Security/perf unchanged:** `sameOriginOnly` default, `trustedTypes gde-bridge`, `DOMParser`, `maxBody 2M`/`fingerprint 1M`, `maxCandidates 750`/`observations 800`/`ledger 5k`, heap ≈6 MB, e2e 911 ms.

## 3. How to reproduce

```bash
npm run check          # node --check both dist files
npm test               # 126/126 33 suites
npm run verify:build   # sha256 9b2b68… lines 5977 src 7 OK deterministic
npm run build          # regenerates dist/.build-meta.json
node --test tests/pattern-guided-revisit.test.js # 5/5
```

## 4. Residual & Next for 1.x

* `src/` still IIFE snippets (no `import`/`export` tree-shaking) — `esbuild` for `v1.1` with `src/` as ES modules.
* `revisitChanged`/`patternGuided` remain opt-in `false` — enable via `CONFIG` before `engine.start()`.
* `STORAGE_KEY v8` not bumped — 1.x will keep additive migration.
* Next 1.x: provider additions (e.g., `Allow/Disallow` soft deny via `Robots`), `export --stable` (`exportedAt:0`), `Allow/Disallow` + `Content-Location` providers.
