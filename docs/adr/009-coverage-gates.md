# ADR 009 — Coverage Gates (enforced thresholds via c8)

**Status:** accepted (v0.7.7)  
**Transcript:** v0.7.6 coverage proof (99% line) → residual “check-coverage false”  
**Code:** `.c8rc.json` (`check-coverage:true, lines:85 branches:75 funcs:80`), `package.json` `coverage:check`, `docs/ci/verify.yml.example` lint+check

## Context
v0.7.6 introduced `npm run coverage` (experimental) + `npm run coverage:html` (c8) but `.c8rc.json` had `check-coverage:false` at 70/60/70. Gates were informational, not enforced; a regression that dropped coverage to 65% would still pass CI. Verification supplement showed 99.05% line but no mechanism to block a low-coverage contribution.

## Decision
- Enable `check-coverage:true` in `.c8rc.json` at `lines:85 branches:75 funcs:80` (per-file false, all-files true). Values chosen 14 points below current 99/96/92 to allow legitimate small dips but to fail gross regressions. Thresholds apply to `tests/*.test.js` (dist excluded) under `c8`.
- Add `package.json` `coverage:check` (`c8 --check-coverage --reporter=text node --test tests/*.test.js`) as the enforced command; `coverage:html` remains for local HTML (`coverage/index.html`). `verify.yml.example` documents lint (`node --check`) + `npm run coverage:check` as the CI quality gate.
- Keep `node --experimental-test-coverage` for fast local `npm run coverage` (Node-native, no c8) — both reporters agree within ~1%.

## Consequences
- **+** CI will fail PRs that introduce uncovered branches (e.g., remove TTL sweep but not test).
- **+** Explicit gate makes the 99% claim in `VERIFICATION_SUPPLEMENT_v0.7.6.md` actionable, not just documentary.
- **−** Very small test files (<20 lines) would be subject to aggregate, not per-file, to avoid noisy per-file failures (hence `per-file:false`).

## Links
- Tests: `tests/verify-p0-fixes.test.js` asserts `coverage:check` in `package.json` and `"check-coverage": true` in `.c8rc.json`.
- Coverage: `VERIFICATION_SUPPLEMENT_v0.7.6.md` §3 (99% report) + `VERIFICATION_SUPPLEMENT_v0.7.7.md` §3 (gate).
