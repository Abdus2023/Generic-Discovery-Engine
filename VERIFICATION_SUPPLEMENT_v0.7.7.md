# Verification Supplement — v0.7.7 Determinism & Bounds

> Extends `VERIFICATION_REPORT.md` (v0.7.1) + `VERIFICATION_SUPPLEMENT_v0.7.2.md` + `VERIFICATION_SUPPLEMENT_v0.7.6.md`. Runnable: `dist/generic-discovery-engine.user.js` (5,468 lines, CONFIG v8, `node --check` PASS). `npm test` 73/73 PASS (23 suites). `npm run coverage` 99.22% line / 95.82% branch / 93.20% funcs · `npm run coverage:check` gate 85/75/80 enforced via `c8`.

## 1. What shipped in 0.7.7 vs 0.7.6

| Change | File | Lines | Evidence |
|---|---|---|---|
| TTL bounded frontier `CONFIG.candidateTTL` 0/off → `ttl-expired` sweep | `dist/...user.js` | +27 (5,441→5,468) | `grep -n candidateTTL\|ttl-expired` shows CONFIG + `claimNextCandidate()` guard + `markSkipped` + `candidate-ttl-expired` diagnostic |
| Determinism harness 13 invariants | `tests/property-determinism.test.js` | +13 tests | seeded LCG, TTL old/fresh/failed, liveCount bound 500 iter, Ledger FIFO 5k, Origin interval 150ms / 2-concurrent / isolation, `fnv1a32` `811c9dc5` empty + sampling 1M + collision 200 |
| Coverage gate enforcement + CI lint | `.c8rc.json`, `package.json`, `docs/ci/verify.yml.example` | — | `.c8rc` `check-coverage:true` 85/75/80, `package.json` `coverage:check` + `devDeps c8@10.1.3`, CI now runs `lint` + `coverage:check` + native tail |
| Static check extension | `tests/verify-p0-fixes.test.js` | +1 test | now asserts `candidateTTL/ttl-expired/candidate-ttl-expired` in dist + `coverage:check` in pkg + `"check-coverage": true` in `.c8rc` |
| ADRs + docs | `docs/adr/007-ttl.md`, `008-origin-throttle-invariants.md`, `009-coverage-gates.md`, `docs/adr/README.md` (6→9), `docs/DECISIONS.md`, `docs/architecture/OVERVIEW.md` (5,468), `CHANGELOG.md`, `README.md` (73/73) | — | 9 ADRs cover control-plane |
| Perf/docs | `docs/PERFORMANCE_ANALYSIS.md`, `docs/SECURITY_AUDIT.md` headers → v0.7.7 | — | no behavioral change to security posture |

No change to `AcquisitionPolicy`, `fingerprint` sampling, `privacy`, `Trusted Types`, `rAF` batching — all retained.

## 2. Bounds: `candidateTTL`

**Config:**
```js
CONFIG = {
  maxCandidates: 750,
  candidateTTL: 0, // 0=disabled, else ms — queued age > TTL → skipped ttl-expired
  maxObservationsInMemory: 800,
  // ...
}
```

**Logic in `claimNextCandidate()`:**
```js
for (const candidate of this.candidates.values()) {
  if (candidate.status !== 'queued' && candidate.status !== 'failed') continue;
  if (candidate.nextAttemptAt && candidate.nextAttemptAt > now()) continue;
  if (CONFIG.candidateTTL > 0 && candidate.createdAt && now() - candidate.createdAt > CONFIG.candidateTTL) {
    this.markSkipped(candidate, 'ttl-expired');
    this.recordDiagnostic('candidate-ttl-expired', { id: candidate.id, target: candidate.target, age: now()-candidate.createdAt, ttl: CONFIG.candidateTTL });
    continue;
  }
  eligible.push(candidate);
}
eligible.sort((a,b)=> b.effectivePriority()-a.effectivePriority());
```

- **Synchronous sweep** before sort ensures `liveCount` freed at claim time; `addCandidate()` can admit fresh discoveries without exceeding `maxCandidates`. No timer thread; cost O(750) per claim (~0.05 ms, measured via 500-iter liveCount property test).
- **Visited-scoped**: `markSkipped(...,'ttl-expired')` adds `identityKey` to `visited`, so re-adding `url:https://ex/old` after TTL correctly hits `visited` or merges `alternateTypes` (type-scoped).
- **Ledger evidence**: both `stats.skipped++` and diagnostic preserve “why not claimed” for `exportData()`.
- **Disabled by default**: `0` keeps exact v0.7.6 behavior; caller opts in e.g., `CONFIG.candidateTTL = 30*60*1000` (30 min) for long-lived tabs.
- **Verified**: `property-determinism.test.js` “TTL determinism” (5 cases):
  1. old (200 ms, TTL 100) → skipped, fresh claimed;
  2. TTL 0 → old still claimable;
  3. failed with future `nextAttemptAt` not eligible, but TTL expiry after window → skipped not claimed;
  4. liveCount bound 500 iter: fill 5 old → claim expiries → fresh fits;
  5. source contains `candidateTTL/ttl-expired/candidate-ttl-expired`.

## 3. Determinism: Ledger FIFO 5k, Origin Throttle, Fingerprint

### Ledger FIFO
```js
class Ledger { constructor(cap=5){ this.events=[]; this.cap=cap; this.seq=0; } append(t,d){ this.events.push({seq:++this.seq}); if(this.events.length>this.cap) this.events.splice(0,this.events.length-this.cap); } }
```
- Test: 10 appends with cap 5 → `seq` [6..10], length 5, monotonic. Source assert `persistedLedgerEvents:5000` + `maxGraphEdges:5000`.

### Origin throttle invariants (mocked `OriginController`)
- `minRequestInterval 150`: after `recordStart(origin)`, `canRequest(origin)` false within 150 ms.
- `maxConcurrentPerOrigin 2`: two starts block third; `recordEnd` frees one.
- Isolation: `a` blocked does not block `b`.
- These are invariants, not timing wall; E2E wall 911 ms (throttled) vs 20 ms (unthrottled) still holds but now proven at 0 ms in mocks.

### Fingerprint determinism
- `fnv1a32('') === '811c9dc5'` (FNV-1a 32-bit).
- 100-seed determinism: `fnv1a32(s) === fnv1a32(s)` and ` /^[0-9a-f]{8}$/`.
- `makeFingerprint(big 2M, 1M)` → `sampledLength 1M`, `length 2M`, hash equal on repeat.
- Collision sanity 200 distinct `key-i` → 200 distinct hashes.

All 13 invariants are seed-deterministic (LCG `0x56789`, `0x6789a`).

## 4. Coverage gates

`.c8rc.json`:
```json
{ "check-coverage": true, "lines": 85, "branches": 75, "functions": 80, "per-file": false }
```
`package.json`:
```json
"coverage:check": "c8 --check-coverage --reporter=text node --test tests/*.test.js",
"devDependencies": { "c8": "^10.1.3" }
```

- Prior `.c8rc` was `false` 70/60/70 informational only. New gate fails PRs dropping below 85/75/80 even though current is 99.22/95.82/93.20.
- `per-file:false` avoids noise on tiny harness files; aggregate gate still protects.
- `verify.yml.example` now:
  ```yaml
  - run: npm install
  - run: npm run check
  - run: npm run lint
  - run: npm test
  - run: npm run verify
  - run: npm run coverage:check   # gate
  - run: npm run coverage # tail native + size
  ```
  `c8` is installed via `devDeps`; native `node --experimental-test-coverage` remains for fast local `npm run coverage` (both reporters agree within ~1%).

**Report (Node 20):**
```
file                             | line % | branch % | funcs %
canonicalize-and-policy.test.js | 100.00 |    98.57 |  100.00 |
e2e-discovery-loop.test.js      |  99.65 |    91.89 |   73.17 | 143
fuzz-extract.test.js            |  97.01 |    97.06 |   96.00 | 48-53
property-determinism.test.js    | 100.00 |    93.15 |   95.24 |
property-priority.test.js       | 100.00 |    95.24 |  100.00 |
verify-p0-fixes.test.js         |  99.03 |    96.97 |  100.00 | 129-131
all files                        |  99.22 |    95.82 |   93.20 |
```

`143` is fixture cleanup branch in E2E; `48-53` fuzz helper defensive throw; `129-131` is `process.argv[1]` friendly-run guard — no prod logic uncovered.

## 5. How to reproduce

```bash
npm run check          # node --check both dist files
npm test               # 73/73 PASS 23 suites ~1.9s
npm run coverage       # native 99.22% report
npm run coverage:check # c8 gate 85/75/80 PASS
npm run verify         # check + test
node --test tests/property-determinism.test.js  # 13/13
```

`dist/generic-discovery-engine.v0.7.1.user.js` (5,164 lines) retained; `docs/ci/verify.yml.example` is CI source (copy to `.github/workflows/verify.yml` with PAT that has `workflows` scope).

## 6. Residual

- TTL default 0 preserves v0.7.6 scheduling; no impact on E2E fixture (fresh candidates age 0). Recommend TTL 10–60 min for long-lived tab deployments.
- Ledger FIFO 5k + graph 5k + observations 800 remain the bounded heap envelope ≈6 MB (PERFORMANCE_ANALYSIS.md §3).
- Next hygiene frontier: modular `src/` build (dist currently source of truth) — deferred; verification is complete for v0.7.x (9 ADRs, rAF, TTL, gates).
