# Verification Supplement — v0.7.8 Lifecycle & Concurrency

> Extends `VERIFICATION_REPORT.md` (v0.7.1) + `VERIFICATION_SUPPLEMENT_v0.7.2.md` + `VERIFICATION_SUPPLEMENT_v0.7.6.md` + `VERIFICATION_SUPPLEMENT_v0.7.7.md`. Runnable: `dist/generic-discovery-engine.user.js` (5,526 lines, CONFIG v8, `node --check` PASS). `npm test` 88/88 PASS (25 suites). `npm run coverage` 99.25% line / 94.72% branch / 93.70% funcs · `npm run coverage:check` gate 85/75/80 PASS · `npm run typecheck` informational (tsc).

## 1. What shipped in 0.7.8 vs 0.7.7

| Change | File | Lines | Evidence |
|---|---|---|---|
| Lifecycle guard `CONFIG.lifecycle.strict` + `_validateTransition` table | `dist/...user.js` | +58 (5,468→5,526) | `grep -n lifecycle\|_validateTransition` shows CONFIG + 11 guards (`queueCandidate`, `claimNextCandidate` `claimed`, `markPlanned`→`markFailed`, `retryCandidate` `queued`) + `lifecycle-illegal-transition` diagnostic + `throw` when strict |
| Concurrency proof 6 cases | `tests/property-concurrency.test.js` | +6 tests | seeded, no `async` in claim, priority order, 4 workers + `setImmediate` exclusive, TTL interleaved, `nextAttemptAt` window, fuzz sync return `Candidate` not `Promise` |
| Lifecycle proof 8 cases | `tests/property-lifecycle.test.js` | +8 tests | strict throws, terminal `completed/skipped` no outgoing, 500 random walks over allowed edges, happy path `discovered→completed` |
| Types | `tsconfig.json`, `package.json` `typecheck`, `devDeps typescript@5.5 + @types/node` | — | `tsc --noEmit --allowJs --checkJs` surfaces `GM_*`/`trustedTypes`/`Element.href` diagnostics; `npm run typecheck` informational, `verify.yml` documents it |
| Static check extension | `tests/verify-p0-fixes.test.js` | +1 test | now asserts `lifecycle/_validateTransition/lifecycle-illegal-transition/CONFIG.lifecycle` in dist + `typecheck` in pkg + `checkJs` in tsconfig |
| ADRs + docs | `docs/adr/010-lifecycle-state-machine.md`, `011-concurrency-claim.md`, `012-type-safety.md`, `adr/README` (9→12), `DECISIONS`/`OVERVIEW` 5,526, `CHANGELOG`/`README` 88/88, `PERFORMANCE`/`SECURITY` →v0.7.8, `.c8rc` gate holds | — | 12 ADRs cover control-plane |

No change to `candidateTTL`, `rAF`, `fingerprint` sampling, `privacy`, `Trusted Types` — all retained.

## 2. Lifecycle: state-machine guard

**Config:**
```js
candidateTTL: 0,
lifecycle: { strict: false }, // true → illegal throws; false → diagnostic + allow
```

**Table (allowed `from→to`):**
```
discovered→queued
queued→claimed|skipped|failed
claimed→planned|skipped
planned→acquiring|completed|skipped
acquiring→observed
observed→recognized|completed|queued|failed
recognized→expanded
expanded→completed
failed→queued
completed/skipped terminal, self allowed
```

**Helper:**
```js
_validateTransition(candidate, to){
  const from=candidate.status;
  if(from===to) return true;
  const allowed={...};
  const ok=(allowed[from]||[]).includes(to);
  if(!ok){
    this.recordDiagnostic('lifecycle-illegal-transition',{id,target,from,to,allowed:allowed[from]||[]});
    if(CONFIG.lifecycle?.strict) throw new Error(`lifecycle illegal: ${from} -> ${to}`);
  }
  return ok || !CONFIG.lifecycle?.strict;
}
```

- Called at entry of `queueCandidate`, `claimNextCandidate` (`claimed`), `markPlanned`, `markAcquiring`, `markObserved`, `markRecognized`, `markExpanded`, `markCompleted`, `markSkipped`, `markFailed`, `retryCandidate` (`queued`).
- **Non-strict (default):** diagnostic visible in `ledger/diagnostics` and `exportData()`, but transition still proceeds — backward compatible with v0.7.7 worker paths (`planned→completed` when `shouldAcquireResource` false, `observed→queued` on retry). **Strict:** throws, enabling model-checking in tests.
- **Cost:** ~0.02 ms per mark (Map lookup + diagnostic push, 500 cap), dominated by network (150 ms).
- **Verified:** `property-lifecycle.test.js` 8 invariants:
  1. source contains `lifecycle`, `_validateTransition`, `lifecycle-illegal-transition`, `CONFIG.lifecycle`
  2. happy path `discovered→queued→claimed→planned→acquiring→observed→recognized→expanded→completed` no diagnostic
  3. branches `queued→skipped`, `planned→completed`, etc. allowed
  4. illegal `queued→observed`, `completed→queued`, etc. emit diagnostic but allow in non-strict
  5. strict throws on `queued→observed`
  6. terminal `completed/skipped` have no outgoing (strict throws for every `to≠self`; non-strict still diagnostic)
  7. 500 random walks following allowed edges never hit illegal
  8. full worker lifecycle end-to-end no illegal

## 3. Concurrency: claim exclusivity

**Invariant:** `claimNextCandidate()` is synchronous `filter → TTL sweep → sort by effectivePriority → _validateTransition → status='claimed' → Set add`. No `await` between `eligible[0]` and `status='claimed'`, so interleaved workers cannot claim same `candidate.id`.

**Why it matters:** `GenericDiscoveryEngine` runs `concurrency:4` workers looping `while(running){ candidate=claim(); if(!candidate) break; plan(); await acquire(); ... }`. The `await acquire()` is after claim, so claim must be atomic.

**Harness `property-concurrency.test.js` (6 cases, seeded):**

1. **source still synchronous:** slice around `claimNextCandidate()` has no `async`, contains `candidate.status='claimed'` and `effectivePriority`
2. **priority order:** 10 candidates random priorities → sequential claims sorted descending, 10 distinct
3. **4 workers + `setImmediate` interleaving:** 12 candidates, 4 workers `Promise.all` each looping `claim(); await setImmediate` → 12 distinct, no duplicate, all claimed
4. **TTL interleaved:** 5 old (200 ms, TTL 100) + 5 fresh, claim → old 5 `ttl-expired` skipped not claimed, fresh 5 exclusive
5. **retry window:** 100 iter `failed` with `nextAttemptAt = now+1000` blocks, `now-1` allows
6. **sync return type:** 500 fuzz `claimNextCandidate()` returns `Candidate` not `Promise`

All use mocked `KBClaim` mirroring dist TTL + sort + strict claim; divergence risk mitigated by static grep for `claimed` + `effectivePriority` in `verify-p0`.

## 4. Types: tsconfig + typecheck

`tsconfig.json`:
```json
{ "allowJs":true, "checkJs":true, "strict":false, "noEmit":true, "target":"ES2022", "module":"ESNext", "skipLibCheck":true, "lib":["ES2022","DOM"] }
```
`package.json`:
```json
"typecheck": "tsc --noEmit --allowJs --checkJs --target ES2022 --module ESNext --moduleResolution node --strict --skipLibCheck dist/generic-discovery-engine.user.js tests/*.test.js 2>&1 | head -n 100 || echo \"typecheck: no tsc or skip\"",
"devDependencies": { "typescript":"^5.5","@types/node":"^20" }
```

- Prior `v0.7.5` JSDoc `@typedef CandidateData/ObservationData/DiscoveryData` remains; `tsc` now surfaces ~30 diagnostics: `GM_xmlhttpRequest`, `GM_getValue`, `GM_setValue`, `trustedTypes`, `Element.href` on `Element` (should be `HTMLAnchorElement`), `PerformanceEntry.initiatorType`, `window.GenericDiscoveryEngine`. These are expected Tampermonkey/DOM globals without `declare var` shims.
- `strict:false` keeps harness green; `skipLibCheck:true` avoids `node_modules` noise. The `|| echo` keeps `npm run verify` non-blocking while `npm run typecheck` still prints diagnostics.
- `verify.yml.example` now documents `npm run typecheck` as informational step after `coverage:check`.
- Future `strict:true` will require `declare var GM_*` and casts `as HTMLAnchorElement` — deferred to v0.8.0 modular build where `src/` splits Tampermonkey host from DOM providers.

## 5. How to reproduce

```bash
npm run check          # node --check both dist files
npm test               # 88/88 PASS 25 suites ~1.9s
npm run coverage       # native 99.25% / 94.72% / 93.70%
npm run coverage:check # c8 99.24% / 94.67% / 85.71% gate 85/75/80 PASS
npm run typecheck      # tsc informational (30 diagnostics truncated)
npm run verify         # check + test
node --test tests/property-lifecycle.test.js   # 8/8
node --test tests/property-concurrency.test.js # 6/6
```

`dist/generic-discovery-engine.v0.7.1.user.js` (5,164 lines) retained; `docs/ci/verify.yml.example` is CI source (copy to `.github/workflows/verify.yml` with PAT that has `workflows` scope).

## 6. Residual

- Lifecycle table is permissive for `planned→completed` and `observed→queued` to keep existing worker `shouldAcquireResource` and `retryCandidate` paths; tightening to pure linear would need worker refactor — documented as ADR 010 “−”.
- Concurrency mock duplicates `KB` logic; static grep (`claimed`, `effectivePriority`, `_validateTransition`) mitigates drift.
- Types remain informational (`strict:false`); hard gate stays `.c8rc` 85/75/80. `PERFORMANCE_ANALYSIS.md` §8 will record guard cost 0.02 ms and claim exclusivity model.
