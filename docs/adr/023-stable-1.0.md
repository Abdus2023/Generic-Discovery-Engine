# ADR 023 — Stable 1.0 (generic discovery loop feature-complete)

**Status:** accepted (v1.0.0)  
**Transcript:** 1.0 stabilisation — control-plane feature-complete  
**Code:** `package.json` `1.0.0`, `src/header.txt` `v1.0.0 — Stable`, `dist` `5977` `9b2b68…`, `CONFIG` v8 unchanged, 22 ADRs + deep audit

## Context
v0.9.1 delivered pattern-guided + revisitChanged (22 ADRs, 126/126, 5969 lines, `src/` bundler). The DVB-inspired generic loop — *Candidate → AcquisitionPlan → OriginController → Acquisition → Observation → ProviderRegistry (9) → Discovery → KnowledgeBase (pattern/cluster, fingerprint, TTL, lifecycle, change) → Scheduler (adaptive, priority) → Ledger → Export (coverage + inference) → Persist/Restore → UI* — is now closed with deterministic build, sorted export, and adaptive re-queue. No P0/P1 remains, heap bounded, security `sameOriginOnly` default.

## Decision
- **Version** `1.0.0` package + header `v1.0.0 — Stable (generic discovery loop feature-complete)` + patch notes vs `0.9.1` (no new runtime code, `CONFIG` v8 storage compatible, `dist` 5969→5977 +8 header lines `9b2b68…`). No `retry`/`origin`/`priority` changes; `revisitChanged`/`patternGuided` stay opt-in.
- **Stability** no new `src/` code for 1.0; `src/` 7 modules remain source of truth (`header.txt` 165 + `config` 172 + `utils` 357 + `ledger` 271 + `models` 377 + `knowledge` 731 + `providers` 985 + `engine` 2913 ≈ 5977), `scripts/build.js` bundler + `verify:build` deterministic retained.
- **Docs** `CHANGELOG` 1.0, `README` 1.0 `126/126` `9b2b68…`, `DECISIONS` 22→23? Actually stays 22 ADRs — 1.0 does not add new ADR beyond this one (23), `OVERVIEW` 1.0, `SECURITY`/`PERFORMANCE` →1.0, `VERIFICATION_SUPPLEMENT_v1.0.0.md`.

## Consequences
- **+** `1.0.0` signals API stability: `exportData` `gde-export-v8.0` + `inference` additive, `CONFIG` v8, `STORAGE_KEY v8` additive migration, ledger 12 types, provider order fixed. Consumers can pin `^1.0.0` with `verify:build` hash `9b2b68…`.
- **+** No runtime delta vs `0.9.1` — `npm test` 126/126 unchanged, `node --check` PASS, deep audit `DEEP_DVB_AUDIT_v0.8.2.md` still valid (126/126). Control-plane considered complete; future `1.x` will be provider additions or `esbuild` tree-shaking, not loop changes.
- **−** `1.0.0` does not yet use `esbuild` tree-shaking — `src/` still IIFE snippets, not true ES modules; `header.txt` not JS (expected). `STORAGE_KEY` `v8` not bumped, so 1.0 state restores 0.9.1 state.

## Links
- Code: `package.json` `1.0.0`, `src/header.txt` `v1.0.0`, `dist` `5977` `9b2b68…`, `dist/.build-meta.json` `1.0.0`.
- Tests: `126/126` 33 suites, `tests/verify-p0-fixes.test.js` now allows `1.0.0`, `verify:build` `9b2b68…` deterministic.
- Prior: ADR 022 pattern-guided/revisit, ADR 021 bundler, ADR 020 export hardening, `DEEP_DVB_AUDIT_v0.8.2.md`.
