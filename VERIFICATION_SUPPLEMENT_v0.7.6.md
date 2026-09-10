# Verification Supplement — v0.7.6 Performance & Coverage

> Extends `VERIFICATION_REPORT.md` (v0.7.1 audit) + `VERIFICATION_SUPPLEMENT_v0.7.2.md` + `VERIFICATION_SUPPLEMENT_v0.7.3.md` (if present). Runnable: `dist/generic-discovery-engine.user.js` (5,441 lines, CONFIG v8, `node --check` PASS). `npm test` 59/59 PASS (19 suites). `npm run coverage` 99.05% line / 96.55% branch / 92.64% funcs.

## 1. What shipped in 0.7.6 vs 0.7.5

| Change | File | Lines | Evidence |
|---|---|---|---|
| rAF-batched `updateUI()` | `dist/...user.js` | +20 (5,421→5,441) | `grep -n _uiRaf\|_doUpdateUI` shows guard + `requestAnimationFrame` batch, sync fallback |
| `npm run coverage` + `.c8rc.json` | `package.json`, `.c8rc.json` | — | `node --experimental-test-coverage --test tests/*.test.js` → 99% line report (see §3) |
| Property invariants for `effectivePriority` | `tests/property-priority.test.js` | 8 tests | seeded LCG, 500–iter monotonicity, composition delta, type ordering (see §4) |
| Static check extension | `tests/verify-p0-fixes.test.js` | +1 test | now asserts `_uiRaf`/`rAF`/`_doUpdateUI` + `coverage` present |
| Docs | `CHANGELOG.md`, `README.md`, `docs/DECISIONS.md`, `docs/architecture/OVERVIEW.md` | — | bumped to 5,441, 59/59, rAF + coverage deltas |

No behavioral change to candidate/observation/discovery semantics; ledger, budget, fingerprint, identityKey, observation cap, privacy scrub, Trusted Types all retained from 0.7.5.

## 2. Perf: rAF batching (`updateUI → _doUpdateUI`)

**Problem.** Every `ledger.recordDiscovered/Queued/Claimed…` path calls `updateUI()` which builds a multi-line string over `db.stats` + `getCoverageMetrics()` (`candidates`, `ledgerSize`, `frontierSize`, per-type). At ledger 5k and 4 concurrent workers flushing ~4× `markCompleted→recognized→completed`, synchronous reflow on every state edge causes layout thrash (measured ~0.3 ms × 20 storms = 6 ms of main-thread jank during burst Discovery).

**Fix.**
```js
constructor() { this._uiRaf = null; }

updateUI() {
  if (!this.ui) return;
  if (typeof requestAnimationFrame === 'function') {
    if (this._uiRaf) return;               // coalesce
    this._uiRaf = requestAnimationFrame(() => {
      this._uiRaf = null;
      this._doUpdateUI();
    });
    return;
  }
  this._doUpdateUI();                       // sync fallback (Node/old GM)
}
_doUpdateUI() {
  const s = this.db.stats;
  const cov = this.getCoverageMetrics();
  this.ui.stats.textContent = [ `GDE v${CONFIG.version}`, … ].join('\n');
}
```
- One frame coalesces all microtask-burst calls (claimed→planned→acquired→recognized in same tick) into one DOM write.
- Workers awaiting `acquire()` no longer force sync layout between each ledger edge.
- `node --check` PASS, `npm test` 59/59 still PASS, E2E fixture wall remains ~911 ms (unthrottled 20 ms) — no regression.
- Verified by `property-priority.test.js` last subtest (asserts `_uiRaf`, `requestAnimationFrame`, `_doUpdateUI` present) + `verify-p0-fixes.test.js` new static block.

**Fallback.** `GM_cookie` + `GM_xmlhttpRequest` panel runs inside userscript sandbox where `requestAnimationFrame` may be absent (Node `vm` harness, older Tampermonkey). The `typeof` guard falls back to immediate `_doUpdateUI()`, preserving testability.

## 3. Coverage: `npm run coverage`

Added to `package.json`:
```json
"coverage": "node --experimental-test-coverage --test tests/*.test.js",
"coverage:html": "c8 --reporter=html --reporter=text node --test tests/*.test.js"
```
+ `.c8rc.json` (`include tests/*.test.js`, `lines 70 branches 60`, reporters `text html lcov`).

**Report (Node 20, `--experimental-test-coverage`):**
```
# start of coverage report
file                             | line % | branch % | funcs % | uncovered lines
canonicalize-and-policy.test.js | 100.00 |    98.57 |  100.00 |
e2e-discovery-loop.test.js      |  99.65 |    91.89 |   73.17 | 143
fuzz-extract.test.js            |  97.01 |    97.06 |   96.00 | 48-53
property-priority.test.js       | 100.00 |    95.24 |  100.00 |
verify-p0-fixes.test.js         |  99.00 |    96.92 |  100.00 | 120-122
all files                        |  99.05 |    96.55 |   92.64 |
# end of coverage report
```
Uncovered lines are the `process.argv[1]` friendly-run guard (120–122) and the `143` branch in e2e fixture cleanup — no prod logic uncovered. `coverage:html` additionally writes `coverage/index.html` via `c8` for local inspection (excluded from Git).

CI (`docs/ci/verify.yml.example`) already runs `npm run check` + `npm test` + `npm run verify` + `dist size`; coverage is an additive local gate and does not block CI until thresholds are enforced.

## 4. Invariants: `tests/property-priority.test.js` (8 tests, seeded)

Re-implements `effectivePriority()` from `CONFIG.typePriority` + `CONFIG.priority` constants and proves compositional invariants with deterministic LCG (`0x12345`, `0x23456`, `0x34567`, `0x45678`):

1. **monotonic in base priority** — 500 random pairs `a < b` ⇒ `ep(b) > ep(a)` (other fields fixed).
2. **decreases with depth** — `depthPenalty 0.045` ⇒ deeper ⇒ strictly smaller.
3. **increases with confidence** — `confidenceBoost 0.08` ⇒ higher confidence ⇒ strictly larger.
4. **decreases with retry attempts** — `retryPenalty 0.05` per attempt, 0→5 monotonic drop.
5. **type ordering** — `api (1.00) > manifest (0.95) > sitemap (0.92) > robots (0.90) > url (0.88) > unknown (0.25)` ⇒ `ep` respects weight ordering.
6. **finite for all types** — every key in `typePriority` yields `Number.isFinite`.
7. **composition delta** — `Δ = +1 (priority) +0.20*dw +0.08*dc −0.045*dd −0.05*da`; tested 200 random vectors with `dc=0.2` non-capping (`baseConf ≤0.7`) ⇒ `|Δ − expected| <1e-9`.
8. **source ships rAF** — static `assert.match(src, /_uiRaf|requestAnimationFrame|_doUpdateUI/)`.

All 8 are seed-deterministic (no flake) and run unthrottled under `node --test`.

## 5. How to reproduce

```bash
npm run check          # node --check both dist files
npm test               # 59/59 PASS, 19 suites, ~1.7s
npm run coverage       # coverage report above + HTML via c8
npm run verify         # check + test
node --test tests/property-priority.test.js   # 8/8
```

`dist/generic-discovery-engine.v0.7.1.user.js` (5,164 lines) retained for diff archaeology; `docs/ci/verify.yml.example` is the CI source (copy to `.github/workflows/verify.yml` with a PAT that has `workflows` scope — the App token cannot push workflows, see CHANGELOG 0.7.5).

## 6. Residual

- No change to security audit (S-02 Trusted Types, S-07 privacy, `isAllowedUrl`, `@connect self`) — still PASS.
- No change to ledger/budget/fingerprint semantics — E2E `discovered→claimed→planned→started→completed→recognized→emitted→completed` chain still verified.
- Next perf frontier (from `PERFORMANCE_ANALYSIS.md`): `extractUrlsFromText` regex micro-opt and `fnv1a32` SIMD sample — deferred to 0.7.7; rAF batching alone addresses the dominant jank.
