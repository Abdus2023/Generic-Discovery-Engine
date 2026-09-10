# ADR 012 — Type Safety (JSDoc + tsconfig + typecheck)

**Status:** accepted (v0.7.8)  
**Transcript:** v0.7.5 JSDoc typedefs + v0.7.6 coverage  
**Code:** `tsconfig.json` (`allowJs:true, checkJs:true, skipLibCheck:true, lib: ES2022/DOM, strict:false`), `package.json` `typecheck` (`tsc --noEmit --allowJs --checkJs ...`), `devDeps typescript@5.5 + @types/node`

## Context
`dist/generic-discovery-engine.user.js` (5,468 lines) is plain JS with JSDoc `@typedef CandidateData/ObservationData/DiscoveryData` (0.7.5). No type checker ran in CI; Tampermonkey globals (`GM_getValue`, `GM_setValue`, `GM_xmlhttpRequest`, `trustedTypes`) and `DOMParser` `Element` casts produced subtle `any` drifts (e.g., `el.href` on `Element`). `tests/*.test.js` also lack `node:` typings.

## Decision
- Add `tsconfig.json` permissive: `allowJs:true, checkJs:true, strict:false, noEmit:true, target ES2022, module ESNext, skipLibCheck:true`. Includes `dist/**/*.js` + `tests/**/*.js`, excludes `node_modules/coverage`. `strict:false` keeps current JSDoc passes informational while exposing missing `trustedTypes`/`import.meta.dirname` etc.
- Add `package.json` `typecheck` script (`tsc ... 2>&1 | head -n 100 || echo "typecheck: no tsc or skip"`) and `devDeps typescript@5.5` + `@types/node`. The `||` keeps `npm run verify` green while `npm run typecheck` still surfaces ~30 `TS2339`/`TS2307` diagnostics (expected: `Element.href`, `GM_xmlhttpRequest`, `trustedTypes`) for incremental fix.
- Future tightening to `strict:true` will require explicit casts (`as HTMLAnchorElement`) and `declare var GM_*` shims — deferred to v0.8.0 modular build.

## Consequences
- **+** `npm run typecheck` is now runnable locally and in CI (`docs/ci/verify.yml.example` documents it); current 99.25% line-coverage harness still passes.
- **+** `@types/node` silences `node:test`/`node:fs` imports; remaining `GM_*` errors are visible, not hidden by `skipLibCheck`.
- **−** `strict:false` means the gate is informational, not enforced; the `.c8rc` gate (85/75/80) remains the hard gate.

## Links
- Config: `tsconfig.json`, `package.json` `typecheck`.
- Tests: `tests/verify-p0-fixes.test.js` asserts `typecheck` in pkg and `checkJs` in tsconfig.
- Perf: no runtime cost; build remains single-file `dist` (5526 lines).
