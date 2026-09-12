# ADR 019 — Modular Prelude + Export Hardening (src/ mirror)

**Status:** accepted (v0.8.1)  
**Transcript:** Phase 4 framework split — modular prelude (next after v0.8.0)  
**Code:** `src/config.js`, `src/utils.js`, `src/models.js`, `src/knowledge.js`, `src/ledger.js`, `src/providers.js`, `src/engine.js`, `scripts/build.js` src check, `verify:build`

## Context
`dist/generic-discovery-engine.user.js` grew to 5,773 lines (v0.8.0) as a monolith. Verifying provider ordering, ledger, or change detection required grepping a single file. The roadmap called for a `src/` split, but a full bundler would invalidate the deterministic hash gate (ADR 015). Verification needed a way to start modularizing without breaking the `@version` + `sha256` + `lines` + `verify:build` contract.

## Decision
- Create `src/` as a **mirror prelude** (7 files) with `src/README.md` as the plan: `src/config.js` is a real extract (`CONFIG` v8, 84 keys, ES module `export const CONFIG`), `src/utils.js` contains the canonical helpers (`canonicalizeUrl`, `fnv1a32`, `makeFingerprint` wired to `CONFIG`), the other five are explicit placeholders for the future bundle (`models`, `knowledge`, `ledger`, `providers`, `engine`).
- Keep `dist/generic-discovery-engine.user.js` as the source of truth; `src/` does not replace it yet — it is verified, not bundled. `scripts/build.js` now checks that all 7 `src/` files exist and are non-empty, and that the dist header `@version` matches `package.json`; `scripts/verify-build.js` additionally checks the ordered 9-provider registry (`Html → … → Text`, with `Robots` + `Headers` sixth/seventh) and that `dist/.build-meta.json` lists `src`.
- Bump `@version`/`package.json` to **0.8.1**, describe package as “modular prelude + export hardening”, and wire `npm run build → build.js && verify:build` so `dist/.build-meta.json` captures the new 5,784-line / 167 kB / `sha256:031c3b…` artifact atomically. Full concatenation via an esbuild-style bundler is deferred to v0.9.0 once the mirror is stable.

## Consequences
- **+** Contributors can now review `src/config.js` / `src/utils.js` in isolation; the build gate guarantees the mirror never drifts from dist (missing `src/` file → build fails).
- **+** No entropy change: dist is still deterministic (same hash for same source; only header/version bump changes hash), and the `lines` count tracks the 11-line patch note.
- **−** `src/` placeholders still contain no logic — the engine still ships as one file, and tree-shaking is not yet possible. Documented in `src/README.md` with the v0.9.0 bundler plan.
- **−** Import paths in `src/` are ESM-only; the userscript still uses IIFE `GM_` globals, so dual-mode testing requires the existing `tests/src-build.test.js` rather than direct `import` of dist.

## Links
- Code: `src/config.js` (CONFIG v8 extract), `src/utils.js`, `src/README.md`, `dist/generic-discovery-engine.user.js` v0.8.1 header, `scripts/build.js` src check, `dist/.build-meta.json` v0.8.1.
- Tests: `tests/src-build.test.js` (7-file existence, config version, header sync, meta hash, 9-provider order, pattern/cluster exports), extended `tests/verify-p0-fixes.test.js` (§static patch presence now allows `0.8.[01]`).
- Prior: ADR 015 build determinism, Phase 4 framework split noted in DECISIONS §Further splits.
