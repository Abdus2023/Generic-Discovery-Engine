# Verification Supplement — v0.8.2 Export Hardening + Inference Metrics

> Extends `VERIFICATION_REPORT.md` (v0.7.1) + `VERIFICATION_SUPPLEMENT_v0.7.2.md` + `VERIFICATION_SUPPLEMENT_v0.7.6.md` + `VERIFICATION_SUPPLEMENT_v0.7.7.md` + `VERIFICATION_SUPPLEMENT_v0.7.8.md` + `VERIFICATION_SUPPLEMENT_v0.7.9.md` + `VERIFICATION_SUPPLEMENT_v0.8.0.md` + `VERIFICATION_SUPPLEMENT_v0.8.1.md`. Runnable: `dist/generic-discovery-engine.user.js` (5,864 lines, CONFIG v8, `node --check` PASS). `npm test` 121/121 PASS (32 suites). `npm run verify:build` sha256 a46d37… lines 5864 deterministic (src 7 + inference gate) · `node --experimental-test-coverage` 99.3%/92%/95% · `npm run typecheck` informational. `src/` mirror 7.

## 1. What shipped in 0.8.2 vs 0.8.1

| Change | File | Lines | Evidence |
|---|---|---|---|
| Coverage determinism + inference | `dist/...user.js` `getCoverageMetrics()` | +~40 (5784→5864, +80 total with export) | `grep -n patternCount dist/...user.js` shows `patternCount`, `clusterCount`, `fingerprintUnique`, `inferenceEnabled`; `grep -n queuedByTypeUnsorted` shows sorted copy `Object.keys(...).sort()` |
| Export inference block | `dist/...user.js` `exportData()` | — | `grep -n inference dist/...user.js` shows `inference = {enabled, patternMetrics, clusterMetrics, fingerprintStats:{unique,total}}` alongside `coverage`, `engine`, `ledger`; schema stays `gde-export-v8.0` |
| Build gate hardening | `scripts/verify-build.js` | — | asserts `patternCount`/`clusterCount`/`fingerprintUnique`/`inferenceEnabled`/`patternMetrics`/`clusterMetrics`/`fingerprintStats` plus `extractUrlPattern`/`RobotsProvider` + `/"builtAt"/` forbidden; `scripts/build.js` already src-aware |
| Tests | `tests/export-inference.test.js` | +6 tests | sorted `queuedByType` alphabetical, export inference block, pattern collapse `{int}`, JSON-stable, static keys, fingerprintUnique via `fingerprintIndex`; `verify-p0-fixes` now allows `0.8.[0-9]` |
| Package | `package.json` `0.8.2` | — | description “export hardening + inference metrics (coverage/export deterministic)” |
| ADRs + docs | `docs/adr/020-export-hardening.md`, `adr/README` (19→20), `DECISIONS`/`OVERVIEW` 5864, `CHANGELOG`/`README` 121/121, `PERFORMANCE`/`SECURITY` →v0.8.2 | — | 20 ADRs cover control-plane through export hardening |

No change to `candidateTTL`, `lifecycle` guard, `rAF`, `pattern/cluster` collection, `fingerprint` sampling, `privacy`, `Trusted Types`, provider semantics — all retained. `CONFIG.version` stays 8. Dist hash changes only because coverage/export logic + header added, not provider regressions.

## 2. Coverage determinism: sorted `queuedByType`

```js
// before (v0.8.1, insertion-order, non-deterministic diff)
const queuedByType = {};
for (const c of queued) queuedByType[c.type] = (queuedByType[c.type]||0)+1;

// after (v0.8.2, alphabetical, JSON-stable)
const queuedByTypeUnsorted = {};
for (const c of queued) queuedByTypeUnsorted[c.type] = (queuedByTypeUnsorted[c.type]||0)+1;
const queuedByType = {};
for (const k of Object.keys(queuedByTypeUnsorted).sort())
  queuedByType[k] = queuedByTypeUnsorted[k];
```

- Keys now `"api","url","xml"` not `insertion["url","api"]`; `JSON.stringify(coverage.queuedByType)` identical across runs with same frontier, proven by `export-inference` case “JSON-stable” (two `exportData()` calls `stringify` equal).
- Inference fields added to `coverage` without extra traversal: `patternCount = patternMetrics.size`, `clusterCount = clusterMetrics.size`, `fingerprintUnique = fingerprintIndex.size`, `inferenceEnabled = !!CONFIG.inference.patternInference` — all O(1) or O(n≤750) via already-maintained indexes (~0.06 ms).

## 3. Export hardening: `inference` block

```js
exportData() {
  const coverage = this.getCoverageMetrics();
  const inference = {
    enabled: !!CONFIG.inference.patternInference,
    patternMetrics: this.db.getPatternMetrics(), // {size, total, top[20]}
    clusterMetrics: this.db.getClusterMetrics(),
    fingerprintStats: {
      unique: this.db.fingerprintIndex.size,
      total: [...this.db.fingerprintIndex.values()].reduce((a,s)=>a+s.size,0)
    }
  };
  return { schema:'gde-export-v8.0', exportedAt:new Date().toISOString(),
           config:{...CONFIG}, coverage, inference,
           engine:this.db.serialize(), ledger:this.ledger.export(),
           networkEvents:[...this.networkEvents.values()], diagnostics:this.db.diagnostics.slice() };
}
```

- Additive: old consumers that read `schema` + `coverage` + `ledger` ignore `inference`; new operators see `export.inference.patternMetrics.top[0] = ["https://a.ex/user/{int}",200]` and `fingerprintStats.unique 12` without reaching into `engine.db`.
- Bounded: `top` already sliced to 20 in `getPatternMetrics`/`getClusterMetrics`; `fingerprintStats.total` sums Set sizes, not bodies (≤750). Export grows ~2 kB worst-case.
- Ledger still `seq`-ordered 5 k FIFO (`ledger.export()`), `graphEdges` 5 k, `diagnostics` 500 — no new caps. `exportedAt` remains ISO string (non-deterministic, but not used for diff; `verify:build` checks only `hash` of dist, not export timestamp).

## 4. How to reproduce

```bash
npm run check          # node --check both dist files
npm test               # 121/121 PASS 32 suites ~2.5s
node --experimental-test-coverage --test tests/*.test.js  # 99.28/92.45/94.94
npm run verify:build   # sha256 a46d375a84c3… lines 5864 src 7 + inference gate deterministic
npm run build          # regenerates dist/.build-meta.json + re-verifies
npm run typecheck 2>&1 | head -n 50  # informational (no tsc)
node --test tests/export-inference.test.js # 6/6
node --test tests/provider-robots-headers.test.js # 12/12
```

`dist/generic-discovery-engine.v0.7.1.user.js` (5,164 lines) retained; `docs/ci/verify.yml.example` is CI source.

## 5. Residual

- `exportedAt` still non-deterministic per export (by design — captures wall time); `verify:build` does not hash export, only dist. Future `export --stable` could inject deterministic `exportedAt:0` for snapshot testing.
- `queuedByType` sorting is alphabetical, not by count descending — `patternMetrics.top` is by count, `coverage.queuedByType` is by key; both are now documented.
- `fingerprintStats.total` counts indexed URLs per hash, not distinct bodies — if two URLs share hash (collision, ~1/2³²), total may undercount bodies; acceptable for fingerprint dedup metric, noted in ADR 020.
- Next for v0.9.0: concatenate `src/config→utils→models→knowledge→ledger→providers→engine` with header preservation via bundler, keep `verify:build` hash, move provider/knowledge tests to import from `src/` and test `dist` via E2E only; DVB-loop audit doc (`VERIFICATION_DEEP`) to map each blind-scan phase to engine module with invariant proof.
