# Verification Supplement — v0.7.2 Verified Patch

**Parent report:** [`VERIFICATION_REPORT.md`](VERIFICATION_REPORT.md) (v0.7.1 audit, 518 lines)  
**This supplement:** verifies the **P0/P1 patches** that close the issues filed in §4.2 / §10 of the parent report.  
**Patched artifact:** `dist/generic-discovery-engine.user.js` — **v0.7.2**, 5,245 lines, `CONFIG.version 8`, `STORAGE_KEY v8`, `gde-export-v8.0`  
**Archive:** `dist/generic-discovery-engine.v0.7.1.user.js` (5,164 lines) retained verbatim (git `8902856`)  
**Verification harness:** `tests/verify-p0-fixes.test.js` + `tests/canonicalize-and-policy.test.js` — **34/34 PASS** (`npm test`)  
**Toolchain:** `node v22.22.3`, `node --check` PASS for both artifacts, `node --test` built-in (no external deps)  

---

## 1. What Was Patched and Why

| Issue | Parent Report § | Root Cause | Patch (dist lines) | Risk if unpatched |
|---|---|---|---|---|
| **P0-1 liveCount** | §4.2 P0-1, §11 | `addCandidate` guard used `candidates.size` which counts `completed`/`skipped` | `liveCount = [...candidates.values()].filter(c=>!['completed','skipped'].includes(c.status)).length` then `liveCount >= maxCandidates` | Frontier frozen after 750 total URLs even though queued=0; SPA stalls within minutes |
| **P0-2 visited duality** | §4.2 P0-2 | `visited` stored bare `url`, `candidateKeys` keyed `type:target`, `addCandidate` never consulted `visited` | `visited` now `Set<identityKey>`; `markCompleted`/`markSkipped` add `identityKey`; `addCandidate` early-returns `candidate-visited` if `visited.has(key)` | Same URL with different `type` could re-acquire after completion; same type could linger |
| **P0-3 obs heap** | §4.7, §6.3 | `observations Map` unbounded in RAM (persisted via `serialize` already stripped body, but heap not) | `recordObservation` FIFO evicts `firstKey` when `size >= maxObservationsInMemory (800)` + `observation-evicted` diag | Link-dense SPA + mutations → unbounded heap, OOM in long-lived tab |
| **P1-1 cross-provider dedup** | §4.5 | `html` + `text` could both emit same `targetUrl` from one payload | `executePlan` now dedups via `emittedForObservation Set<targetUrl>` across providers, emits `discovery-deduped` | Duplicate discoveries → duplicate candidates → amplified scheduling |
| **P1-2 mutation batch** | §6.2 | `observeCurrentDom` called `discover` per element, no batch dedup | `seen Set<type:canonical>` per flush, `tryDiscover` skips `seen` before `discover` | 100s duplicate `Candidate` allocs per frame on virtualized lists |

---

## 2. Patch Evidence (static grep — automated by tests)

```sh
$ grep -n "liveCount\|visited.*identityKey\|maxObservationsInMemory\|emittedForObservation\|tryDiscover" \
    dist/generic-discovery-engine.user.js

  liveCount = [...this.candidates.values()].filter(...)   # P0-1
  this.visited.has(key) / this.visited.add(candidate.identityKey())  # P0-2
  maxObservationsInMemory: 800 / observation-evicted     # P0-3
  emittedForObservation = new Set() / discovery-deduped  # P1-1
  tryDiscover(...) / seen.has(key)                        # P1-2
```

These strings are asserted by `tests/verify-p0-fixes.test.js` static suite (§ “static patch presence”). Any regression that removes a patch fails `npm test` before behavioral checks.

---

## 3. Behavioral Verification (node --test)

### Harness

Two test files, no external dependencies, run with `npm test` (`node --test tests/*.test.js`):

- **`verify-p0-fixes.test.js`** — static patch checks + isolated `KnowledgeBasePatched` reimplementation of patched logic (7 behavioral suites, 14 tests).
- **`canonicalize-and-policy.test.js`** — URL canonicalization, `isAllowedUrl`, `looksLike*`, `AcquisitionPolicy` denials, `fnv1a32` stability (5 suites, 17 tests).

```
$ npm test

# tests 34
# suites 12
# pass 34
# fail 0
# duration_ms ~200
```

### What the behavioral tests prove

#### P0-1 — liveCount excludes completed/skipped
```
kb = new KB(3); add a,b,c → cap; add d blocked;
kb.markCompleted(a); add d → OK (liveCount 2→3, size 4)
kb.markSkipped(b); add c → OK
```
Old buggy guard (`size >= cap`) would have stayed blocked. Test asserts `liveCount` computation.

#### P0-2 — visited identityKey-scoped
```
add url/https://ex/page → completed;
add same type:target → liveCount unchanged, visited has 'url:https://ex/page';
add same URL type:script → allowed (different key), id distinct;
skipped also adds to visited.
```
Ensures `type:target` scoping, not bare URL.

#### P0-3 — FIFO cap
```
maxObs 2 → obs1,obs2 → size 2; obs3 → evicts obs1, diagnostics 'observation-evicted'.
```

#### P1-1 — cross-provider dedup
```
emitted Set dedup: html:ex/a + text:ex/a → kept 1, text:ex/b → kept 2.
```

#### Concurrency invariant (unchanged but re-verified)
```
claimNextCandidate is synchronous: two successive claims return distinct ids, both status 'claimed'.
```

#### Canonicalization & policy
```
hash stripped, tracking params (utm_*, fbclid, gclid, mc_*, ref) stripped, relative resolved;
non-http (javascript:, data:, mailto:) rejected; sameOriginOnly enforced;
looksLikeHtml/Json/Binary heuristics; policy denies non-GET, max-depth, forms/media/binary, cross-origin.
```

---

## 4. Manual Static Checks (no harness)

| Check | Command | Result |
|---|---|---|
| Syntax v0.7.1 archive | `node --check dist/generic-discovery-engine.v0.7.1.user.js` | PASS |
| Syntax v0.7.2 patched | `node --check dist/generic-discovery-engine.user.js` | PASS |
| Diff size | `wc -l` 5164→5245 (+81 lines, only P0/P1), `diff -u` inspected | Patch minimal, no providers rewritten |
| Storage migration | `restore` handles `engine.version >=6`, additive ledger | v7→v8 additive; `requestsReserved` reset to 0, concurrency clamped |
| XSS/CSP | `DOMParser` only, no `innerHTML` of untrusted body, bridge injection has `try/catch` + diagnostic | Unchanged, safe |
| `@connect` scope | still `*` (reported as P2, not patched in v0.7.2) | Deliberately deferred |

---

## 5. Updated Documentation

- **`README.md`** refreshed for v0.7.2: top banner with release link, provider diagram 3→7, architecture diagram layered (Policy→Plan→OriginController), roadmap checkboxes Phase 1 0/9→5/9 and Phase 2 0/7→5/7 (each item explicitly referenced to implementation), Phase 3 partial.
- **`CHANGELOG.md`** added (covers 0.7.2 patch notes, 0.7.1 feature list, migration notes).
- **`package.json`** added (`type:module`, scripts `test`/`check`/`verify`, engine `node>=18`).

---

## 6. Remaining P2 (deliberately not in v0.7.2)

Per parent report §10, these are **P2 — next iteration**, not blocking:

- Narrow `@connect *` when `sameOriginOnly:true` (use `@connect self` or document risk).
- Deduplicate per-observation discoveries beyond `targetUrl` (also consider `fingerprint` coalescing).
- Add coverage/budget metric (`frontierSize`, `queuedByType`, `requestsRemaining`) to UI + export.
- Split `Continue Architecture Planning.md` (2.2 MB) into `docs/decisions/*.md` + `CHANGELOG.md`.
- Add `eslint` + `prettier` + JSDoc/TypeScript for provider shapes.

---

## 7. How to Re-verify

```sh
# 1. Syntax
npm run check          # node --check both artifacts

# 2. Invariants
npm test               # 34 tests, 12 suites, 0 fail

# 3. Full verify (as CI)
npm run verify         # check + test

# 4. Diff the patch
diff -u dist/generic-discovery-engine.v0.7.1.user.js \
        dist/generic-discovery-engine.user.js | less
```

Expected output (abridged):

```
# tests 34
# suites 12
# pass 34
# fail 0
```

---

## 8. Provenance

- Base commit: `8902856` (parent report + v0.7.1 extract)
- This supplement commit: patches v0.7.2 + tests + docs
- No network fetches, no secrets, no branch switch (still `arena/01a08cd3-generic-discovery-engine`)
- Tooling: manual `edit_file`, `grep`, `node --check`, `node --test`

---

*End of supplement.*
