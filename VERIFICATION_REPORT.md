# Generic Discovery Engine — Deep Analysis & Verification Report

**Branch:** `arena/01a08cd3-generic-discovery-engine`  
**Baseline:** `cc8df73` (main) — 2 Markdown documents, no standalone source artifact  
**Latest Prototype Reviewed:** `v0.7.1` — 5,164 lines, 140 kB, embedded in `Continue Architecture Planning.md` (lines 1,355,214–1,495,770)  
**Also Reviewed:** `v0.1.0`, `v0.2.0`, `README.md` claims, `Userscript Discovery Prototype.md`  
**Date (UTC):** 2026-09-10  
**Node Syntax Check:** `node --check` **PASS** for v0.7.1 (brace 577/576 balanced, intentional 1-line IIFE tail)  
**Analyst Mode:** static code audit + architectural trace + claim/implementation matrix + security & robustness review  

---

## 0. Executive Summary

**Verdict:** **Substantively sound architecture, prototype-grade implementation. DVB blind-scan analogy is defensible as a control-pattern abstraction, and the README scope disclaimer (“DVB-inspired, not DVB-compatible”) is accurate. Core invariants — atomic candidate claiming, provider-based recognition, recursive expansion with provenance — are implemented. Latest v0.7.1 materially strengthens the control plane (AcquisitionPlan, AcquisitionPolicy, OriginController, DecisionLedger, ResourceRecord, KnowledgeGraph) beyond what README describes. README is now 3–4 versions stale.**

**Maturity:** Phase-0 prototype → early Phase-1. Architecture documents (92k lines of planning) significantly exceed code artifact. That is appropriate for a research prototype but creates a documentation–code drift risk.

| Dimension | Grade | Notes |
|---|---|---|
| **Architectural Fidelity (DVB → Generic)** | **A-** | Clean separation: candidate / acquisition / observation / recognition / discovery / expansion. DVB loop `tune→detect→demod→validate→PSI→NIT→new mux` maps correctly to `candidate→acquire→recognize→discover→expand`. No over-claim of RF competence. |
| **Concurrency Correctness** | **A-** | Claim-before-await invariant holds. Two subtler liveness/capacity bugs remain (see §4.2). |
| **Provider Extensibility** | **B+** | v0.7.1 introduces real `Provider` base, 7 providers, registry, matching pipeline. Text-provider fallback ordering still leaks. |
| **Persistence & Provenance** | **B** | Ledger + graph edges + ResourceRecord give explainability; persistence bounds are present but observation bodies can still blow quota. |
| **Security / Safety** | **B-** | `sameOriginOnly:true` default is correct, forms/media/binary disabled by default. Network bridge injection and unlimited URL extraction remain the widest attack surface. |
| **Robustness / Edge Handling** | **C+** | URL canonicalization, origin throttling, retries, body truncation present. No test suite, no CI, no lint, no types. Completed-candidate retention bug caps effective search space. |
| **Documentation Accuracy** | **C** | README describes v0.2-era 3-provider system; v0.7.1 has 7 providers + policy + ledger + network bridge. Roadmap checkboxes stale. |

**One-line recommendation:** **Extract v0.7.1 into a versioned `dist/generic-discovery-engine.user.js` file, fix the 2 P0 capacity bugs, add a minimal test harness for the claim/dedup/ledger invariants, and refresh README. Without that, the planning docs will continue to diverge from the runnable artifact.**

---

## 1. Repository Structure Audit

```
Generic-Discovery-Engine/
├── .git/
├── README.md                              12.8 kB, 396 lines — accurate at v0.2, stale vs v0.7.1
├── Continue Architecture Planning.md        2.24 MB, 92,274 lines — chat transcript + 12 userscript versions (0.1.0→0.7.1)
└── Userscript Discovery Prototype.md        107 kB, 4,805 lines — earlier design notes + v0.1 baseline
```

**Findings:**

1. **No standalone source file.** The runnable code only exists inside Markdown code fences. `git ls-files` shows 2 tracked non-git files. This violates the principle that the artifact under analysis should be directly runnable/lintable. Any verification must first extract via fence parsing (reproduced in `/tmp/v071.js` for this audit).

2. **No `package.json`, no `eslint`, no `tsconfig`, no `tests/`, no CI.** The radar for regressions is human inspection only.

3. **Branch hygiene:** `arena/01a08cd3-generic-discovery-engine` correctly based on `cc8df73`. No divergence from `main` yet.

4. **File-size anomaly:** `Continue Architecture Planning.md` at 2.2 MB is a single-file transcript. It functions as both design log and code history. For reviewability it should be split into `docs/architecture/*.md` + `src/*.js`.

---

## 2. Architecture Deep Dive

### 2.1 The DVB Blind-Scan Abstraction — Is It Valid?

The mapping is presented as:

```
DVB blind scan                  Generic discovery
─────────────────               ─────────────────
frequency                       candidate (URL/ resource descriptor)
signal detection                probe / acquisition (HTTP fetch)
demodulator acquisition         observation (status + body + headers)
transport validation            recognition (provider matches)
PSI/SI metadata                 metadata (HTML links, JSON URL-like values)
network discovery (NIT)         candidate expansion (new URLs)
```

**Assessment: Valid as a *control architecture*, not as a physical-layer equivalence.** The author correctly never claims RF semantics. The useful generalization is:

```
SEARCH → CANDIDATE → ACQUIRE → OBSERVE → RECOGNIZE → DISCOVER → EXPAND → SCHEDULE ↺
```

This is the loop formalized on p.1 of README and reproduced in v0.7.1 header. It matches the classical “blind discovery as hypothesis-testing over a parameter space” described in planning docs §7–§23. The five-level evidence hierarchy (no signal → RF energy → PL sync → valid TS → services) is collapsed in the web prototype to (no response → HTTP response → recognized content type → discovered URLs). Collapse is acknowledged explicitly; no misleading equivalence is asserted.

**One nuance to preserve in docs:** DVB blind scan is *exhaustive* over a bounded spectrum; web discovery is *open-world* and unbounded. Coverage metric plans (§19, §39) therefore cannot be ported 1:1. The report recommends replacing “coverage = evaluated / configured” with “budget exhaustion + frontier size” for the web domain.

### 2.2 Module Map (v0.7.1)

```
CONFIG (version 7, 67 keys)
├── STORAGE_KEY = generic-discovery-engine-v7
├── utils: log, warn, now, sleep, makeId, clamp, unique, originOf,
│          canonicalizeUrl, isAllowedUrl, contentTypeBase,
│          looksLikeHtml/Json/Xml/Css/JavaScript/Binary/ApiUrl,
│          extractUrlsFromText / extractCssUrls / extractXmlLocs,
│          fnv1a32, makeFingerprint, stableId, contentTypeForTarget
├── AcquisitionPlan          id, candidateId, target, method, allowed, reason, priority, origin, expectedType
├── DecisionLedger           seq, events[], append() + 12 typed record*() + export/restore
├── Candidate                id, target, type, origin, parent, priority, hints, depth, 10 timestamp fields, attempts, status, alternate*
│                            effectivePriority() = priority + typeWeight*0.2 + confidence*0.08 - depth*0.045 - attempts*0.05
├── Observation              candidateId, planId, target, http{status,contentType,contentLength,finalUrl}, body, fingerprint, signalPresent
├── Discovery                candidateId, observationId, kind, confidence, mechanism, data{url}, provenance
├── ResourceRecord           url, types[], mechanisms[], parents[], dedup merge(), status, fingerprint, skipReason
├── KnowledgeBase            candidates Map<id,Candidate>, candidateKeys Map<type:target,id>,
│                            observations, discoveries, resources, visited Set<url>, claimed Set<id>,
│                            graphEdges[], fingerprintIndex, diagnostics[], stats{}
├── AcquisitionPolicy        plan(candidate) → AcquisitionPlan (method, depth, type, binary, origin checks)
├── OriginController         states Map<origin,{active,requests,lastRequestAt}>, canReserve(), acquire()→throttle, release()
├── Acquisition              execute(plan,ledger)→Observation  [GM_xmlhttpRequest + fetch fallback, body truncation 2M]
├── Provider (base)          HtmlProvider, JsonProvider, XmlProvider, CssProvider,
│                            JavaScriptProvider, TextProvider, BinaryProvider
├── ProviderRegistry         providers[7 in fixed order], matching(observation)
├── NetworkObserver          bridge injection (fetch/XHR monkey-patch) + PerformanceObserver
└── GenericDiscoveryEngine   db, policy, origins, acquisition, providers, ledger, networkEvents,
                             worker()/start()/pause()/resume()/stop(), adaptive concurrency,
                             discover()/emitDiscovery()/plan()/reserveRequestSlot()/executePlan(),
                             persistence (debounced GM_setValue), UI panel, bootstrap()
```

**Control-plane vs data-plane separation introduced in v0.7.1 is the headline improvement.** Before: `Candidate → Acquisition`. After: `Candidate → Policy → AcquisitionPlan(allowed+reason) → Budget → OriginSlot → Acquisition`. This makes denials first-class and replayable, which planning doc §1–§2 correctly identifies as the auditability fix.

### 2.3 Data-Flow Invariant Diagram (Verified Against Code)

```
initial page ─┬─► discover(url, type, depth0) ─► KnowledgeBase.candidates
              │         │ ledger: candidate-discovered + candidate-enqueued
              │         └─► resource.merge(candidateIds)
              │
DOM mutation ─┘                ▲
                network GET ───┘
                              │
Scheduler: claimNextCandidate()  ←── synchronous, sorts by effectivePriority, skips nextAttemptAt > now
         │ ledger: candidate-claimed
         ▼
AcquisitionPolicy.plan() → AcquisitionPlan{allowed,reason}  ledger: acquisition-planned [+ policy-denied if !allowed]
         │ if !allowed → markSkipped + candidate-skipped
         ▼
reserveRequestSlot()  (synchronous, global maxRequests guard) → budget-denied if exhausted
         ▼
OriginController.acquire()  (async throttle per origin) → slot-granted
         ▼
Acquisition.execute() → Observation{status, http, body, fingerprint}  ledger: request-started → request-completed → observation-recorded
         ▼
KnowledgeBase.recordObservation() → ResourceRecord status acquired/observed + fingerprintIndex
         ▼
ProviderRegistry.matching() → Html/Json/Xml/Css/Js/Binary/Text
         ▼
Provider.recognize() → Discovery[]  ledger: provider-recognized per provider, discovery-emitted per discovery
         ▼
emitDiscovery() → discover() for each discovery.targetUrl() with depth+1  (candidate expansion)
         ▼
markExpanded → markCompleted → candidate-completed  ledger: candidate-completed
         ↺ worker loop
```

**The feedback edge `Discovery → New Candidates → Scheduler` is correctly the only recursion path. No hidden global expansion.**

---

## 3. Feature Verification Matrix — README Claims vs Implementation

| README Claim (Phase 0) | v0.2 Description | v0.7.1 Reality | Verdict |
|---|---|---|---|
| `generate URL candidates` | `Candidate {target,type,priority,origin,parent}` + `Scheduler.add()` | Full `Candidate` with depth, alternateTypes/Origins/Parents, `discover()` + 4 discovery sources (DOM, HTML, JSON/text, network) + `wellKnown` flag (sitemap/robots) | ✅ **Exceeds** |
| `maintain a priority queue` | `Scheduler.next()` sort by `priority` | `claimNextCandidate()` sorts eligible `effectivePriority()` (typePriority 0.20 + confidence + depth/retry penalties) | ✅ **Exceeds** |
| `concurrently acquire candidates` | `concurrency:3`, `Promise.all(workers)` | `concurrency:4`, adaptive `currentConcurrency` (min 1) auto-tuned on success/failure thresholds, `activeWorkers` counter, `paused/running/stopRequested` | ✅ **Exceeds** |
| `prevent concurrent workers from claiming same candidate` | `claimNextCandidate()` sync `queued→claimed` before await | Same sync claim, plus `candidateKeys` dedup, `visited` + `claimed` sets. **Proof in §4.1.** | ✅ **Pass** |
| `record observations` | `Observation {candidateId, http{status,contentType,contentLength}, body, errors}` | `Observation` adds `planId, fingerprint, signalPresent, reason, bodyTruncated, network[]` + `Acquisition` produces fingerprint (fnv1a32) | ✅ **Exceeds** |
| `recognize different response types` | HTML/JSON/Text, `ProviderRegistry.recognize()` | 7 providers: Html, Json, Xml, Css, JavaScript, Binary, Text + `matching()` pipeline (ordered) | ✅ **Exceeds** |
| `extract new candidates` | per-provider `candidates(discovery)` | per-provider `recognize()` emits `Discovery[]`; `emitDiscovery()` creates next-depth `Candidate` | ✅ **Pass** (mechanism renamed correctly) |
| `preserve candidate provenance` | `Discovery.provenance{origin,parent}` | `provenance{origin,parent,candidateTarget,candidateType,mechanism,depth,hints}` + `graphEdges[]` + `ResourceRecord.parents` | ✅ **Exceeds** |
| `deduplicate candidates` | visited + claimed + candidates Maps | `candidateKeys Map<identityKey,id>` + `visited Set<url>` + `fingerprintIndex` + `ResourceRecord.merge()` | ✅ **Pass** (see capacity bug note) |
| `persist discovery state` | `GM_setValue` JSON `visited+discoveries` | Debounced `GM_setValue(STORAGE_KEY, {engine, ledger, requestsReserved, currentConcurrency})` with version 7, bounded slices (1200/1500/3000/5000) | ✅ **Exceeds** |
| `export discovery results` | `engine.export()` v2 JSON + Blob download | `exportData()` v7.1 `{schema, exportedAt, config, engine, ledger, networkEvents, diagnostics}` | ✅ **Exceeds** |
| `recursively expand search space` | `provider.candidates(discovery)` loop | `emitDiscovery()` bounded by `maxDepth:5`, `stripTrackingParams`, `maxCandidates:750` | ✅ **Pass** |

**Providers claimed in README diagram:**

| Provider | README Detail | v0.7.1 |
|---|---|---|
| HTML | links + resources | ✅ Full: a/area, script, link[rel→sitemap/manifest/feed/stylesheet], iframe/frame, media, embedded, form, meta-refresh/canonical/og:url, html-embedded-url regex |
| JSON | URL-like values | ✅ Recursive walk, `${path}` provenance, looksLikeApiUrl → kind api/url |
| Text | HTTP(S) URLs regex | ✅ `text-url` with type detection; note fallback ordering issue §5.2 |
| XML | — | ✅ New: sitemap `loc` extraction via DOMParser + regex fallback |
| CSS | — | ✅ New: `url()` extraction |
| JavaScript | — | ✅ New: regex URL extraction from JS bodies |
| Binary | — | ✅ New: observed-only (image/audio/video/pdf/zip) |

**Current prototype “scope does NOT implement” list (README §Scope):** All 10 DVB-RF negatives (spectrum, SDR, tuner, demod, carrier sync, symbol-rate, FEC, TS, PSI/SI, NIT) — **verified true**, no RF code exists. `scope.rfScanning:false` exported correctly.

**Overall:** Every Phase-0 checkbox that README marks `[x]` is implemented; several Phase-1 items that README marks `[ ]` (formal provider interface, fingerprints, discovery confidence) are *already* done in v0.7.1 but not reflected in README.

---

## 4. Code Quality — Deep Dive

### 4.1 Candidate & Scheduler Correctness (Core Invariant)

**Critical invariant (README):** `A candidate may have at most one active owner.`

**Proof sketch from code:**

```js
// GenericDiscoveryEngine.worker() — line ~ 3,720
while (running && !stopRequested) {
    const candidate = this.db.claimNextCandidate(); // ← synchronous, no await
    if (!candidate) break;
    this.ledger.recordCandidateClaimed(candidate);
    const plan = this.plan(candidate);               // → still synchronous
    if (!plan.allowed) { markSkipped; continue; }
    await this.executePlan(plan);                    // ← first await AFTER claim
}
```

```js
// KnowledgeBase.claimNextCandidate() — line ~ 1,050
claimNextCandidate() {
    const eligible = [];
    for (const c of this.candidates.values()) {
        if (c.status !== 'queued' && c.status !== 'failed') continue;
        if (c.nextAttemptAt && c.nextAttemptAt > now()) continue;
        eligible.push(c);
    }
    eligible.sort((a,b) => b.effectivePriority() - a.effectivePriority());
    const candidate = eligible[0];
    if (!candidate) return null;
    candidate.status = 'claimed';
    candidate.claimedAt = now();
    this.claimed.add(candidate.id);
    this.stats.claimed++;
    return candidate;
}
```

Because JavaScript is single-threaded and `claimNextCandidate` contains **no `await`**, two workers that call it in the same microtask turn cannot interleave between `eligible.sort` and `candidate.status='claimed'`. The second worker sees `status==='claimed'` and skips the candidate. This matches the DVB analogy’s “claim before tune.”

**Verification:** Sequential claim of `A,B,C` with concurrency 3 yields `Queue:{D,E}`, `Claimed:{A,B,C}` — reproduced by code walk, not a timing assumption. The earlier v0.1 bug (`Scheduler.next()` + `markVisited` after `await`) is fixed.

**Residual design note:** v0.7.1 tracks both `claimed Set<id>` and `candidateKeys Map<type:target,id>`. `claimed` is appended but never used for dedup (KnowledgeBase.addCandidate checks `candidateKeys`, not `claimed`). Harmless redundancy; could be removed or enforce `if claimed.has(key)` guard.

### 4.2 Two P0 Capacity/Liveness Bugs

#### P0-1 — `maxCandidates` counts *completed* candidates (search-space exhaustion leak)

```js
// KnowledgeBase.addCandidate() — line ~ 980
if (this.candidates.size >= CONFIG.maxCandidates) {
    this.recordDiagnostic('candidate-cap-reached', {target: ...});
    return null;
}
```

`this.candidates` is `Map<id,Candidate>` that **never deletes completed entries**. After 750 unique URLs (of any status) the discovery frontier is frozen even though `queued` may be 0. Expected behavior: cap should apply to `queued + claimed + retryable`, not to `completed + skipped`. This is a regression from v0.2’s `KnowledgeBase.candidates.delete(key)` on complete. In a long-lived tab that continuously discovers via DOM mutations, the cap will be hit within minutes on a link-dense site and then appear to “stall.”

**Fix:** Track `liveSize` or test `eligibleCount = [...candidates.values()].filter(c=>c.status==='queued'||c.status==='failed').length`, or delete/evict completed entries from the indexed map (retain them only in `visited` / `resources`).

#### P0-2 — `visited` semantics mismatch (URL vs identityKey)

```js
// markCompleted() — line ~ 1,110
this.visited.add(candidate.target);          // stores canonical URL string
// addCandidate() dedup check — uses candidateKeys Map<type:target,id>, not visited
// serialize() persists visited: [...this.visited]
```

`visited` stores bare URL but `addCandidate` dedup is keyed on `type:target`. A URL discovered first as `type:script` and later as `type:stylesheet` will coexist as two candidates with same URL but different keys, bypassing `visited` and re-acquiring the same bytes. Conversely, `visited` prevents re-adding a URL even if a prior attempt failed due to transient error but type changed. The two indexes diverge. Recommendation: canonicalize to `visitedIdentity = Set<identityKey>` or maintain both URL-set and key-set and document which prevents re-enqueue.

**Severity:** Low in sameOrigin default, but becomes duplicate-fetch amplification when `sameOriginOnly:false` or when sitemap feeds emit same URL under multiple `type` hints.

### 4.3 Knowledge Base & Resource Graph

`ResourceRecord` + `fingerprintIndex` + `graphEdges` is well-designed. `ensureResource(url)` → `merge()` correctly accumulates `types, mechanisms, parents, candidateIds, observationIds, discoveryIds`. `fingerprintIndex Map<hash, Set<url>>` enables “same bytes, different URLs” detection (useful for asset deduplication). `graphEdges` bounded at 5,000 with FIFO eviction prevents unbounded growth.

Minor: `KnowledgeBase.candidateKeys` is keyed by `identityKey = ${type}:${target}`. This means `type:api:https://x/api` and `type:url:https://x/api` are distinct. Intentional for type-aware priority but should be documented as “candidate identity is type-scoped.”

### 4.4 Acquisition Pipeline

`Acquisition.execute(plan, ledger)` correctly:

1. `ledger.recordRequestStarted(plan)` before any network.
2. `OriginController.acquire(origin)` throttles per origin (`maxRequestsPerOrigin:50`, `maxConcurrentPerOrigin:2`, `minRequestInterval:150ms`). Implementation uses `sleep(50)` poll-loop with elapsed check — correct but could use a proper semaphore for lower CPU wakeups. Not a bug.
3. `request(plan)` branch: `GM_xmlhttpRequest` preferred, `fetch+AbortController` fallback with `body.slice(0, 2_M)` truncation + `bodyTruncated` flag + `fingerprint`. The dual-path mirrors v0.2 fixes (settled flag, header parsing via regex, abort handling). Timeout is enforced twice (GM timeout + outer `setTimeout`), which is defensive; ensure not double-resolve (settled flag present in GM path, fetch path relies on `AbortController` single-resolve).

**One correctness improvement over v0.6:** `Observation.http.finalUrl` is preserved from `response.finalUrl || response.url`, enabling redirect tracing. Good.

### 4.5 Provider Pipeline

Order is fixed: `Html, Json, Xml, Css, JavaScript, Binary, Text`. Cost is that a `text/html` response that fails `looksLikeHtml` (e.g., malformed) can still be caught by `TextProvider` (which matches `contentType.startsWith('text/') || contentType===''` ) and emit low-confidence `text-url` discoveries from the same bytes. In v0.6-era logs this produced duplicate discoveries. Options: short-circuit after first strong match, or keep multi-provider but deduplicate `Discovery.targetUrl()` across providers per observation.

`looksLike*` heuristics each use `contentTypeBase()` + body-sniff fallback. Heuristics are reasonable for browserscope (no magic-bytes access). `looksLikeBinary` correctly short-circuits `BinaryProvider` to emit no candidates.

### 4.6 Ledger & Replay Semantics

`DecisionLedger` is the most principled v0.7.1 addition. Doc header correctly states:

> Decision replay is supported. Network replay is NOT guaranteed.

`append(type,data)` auto-increments `seq`, caps at 5,000, and 12 typed helpers (e.g., `recordPlan`, `recordPolicyDenied`, `recordSlotGranted`) ensure uniform schema. `restore()` handles missing `seq` via `Math.max(...seq)`. `persist()` stores `ledger.export()` alongside engine. This gives a causal trace:

```
candidate-discovered → candidate-enqueued → candidate-claimed → acquisition-planned
→ [policy-denied | slot-granted → request-started → request-completed] → observation-recorded
→ provider-recognized → discovery-emitted → candidate-discovered …
```

This is **superior to v0.2’s flat `stats`**. It should be promoted in README.

### 4.7 Persistence Robustness

- Debounced at 400 ms (`persistenceDebounce`) — avoids write amplification during burst discovery.
- Bounded slices prevent storage explosion: `persistedDiscoveries 1200`, `persistedResources 1500`, `persistedEdges 3000`. Correct.
- **Risk:** `observations` are serialized in `db.serialize()` without bound and contain `body` up to 2 MB each after truncation. If `db.observations` grows large, `JSON.stringify` can exceed GM storage quota (typically ~10 MB) and `GM_setValue` will throw. The `diagnostics` catch does not recover quota; engine would silently lose persistence. Fix: persist observations separately with LRU or drop bodies from persisted form (retain only fingerprint + http meta). v0.7.1 currently persists full bodies — the same issue v0.2 notes warn about (“Observations can contain complete bodies and are deliberately not persisted” in older version) has regressed.
- `restore()`’s `v6→v7 migration is additive` comment is accurate; new `ledger` starts empty if absent. `requestsReserved` correctly resets to 0 on new execution to avoid stale budget.

### 4.8 URL Handling

`canonicalizeUrl(raw)` canonicalizes via `new URL(raw, location.href)`, strips `#hash`, optionally strips tracking params (`utm_*`, `fbclid`, `gclid`, `mc_`, `ref`). Good for dedup but aggressive (`ref` is used non-tracking on many sites). Should be documented as lossy. `isAllowedUrl` enforces `https?:` and `sameOriginOnly` — correct default. No `javascript:` or `data:` bypass because they fail the protocol test first.

---

## 5. Security Review

| Area | Status | Details |
|---|---|---|
| **Same-origin confinement** | ✅ Good default | `CONFIG.sameOriginOnly:true` + `isAllowedUrl` origin check in both `discover()` and `AcquisitionPolicy.plan()`. Must be re-checked if user sets `sameOriginOnly:false`. GM `@connect *` still declares wildcard; narrow to `*://*/*` if confined. |
| **Forms acquisition** | ✅ Safe default | `policy.acquireForms:false` — prevents GET-disguised POST and side-effectful acquisitions. Provider still *discovers* form actions (as `kind:form`) but Policy denies acquisition. Correct separation of discovery vs acquisition. |
| **Media/binary fetch** | ✅ Safe default | `acquireMedia:false`, `acquireBinaryResources:false` — prevents bulk image/video fetch that would DoS origin and bloat body cache. |
| **Network bridge script injection** | ⚠️ CSP risk | `installBridge()` injects `<script>` with monkey-patched `fetch`/`XHR` into page. Blocked by strict `script-src` CSP, and injected script runs in page world (not userscript world), so it sees page’s CSP and `trustedTypes` restrictions. Fallback is silent diagnostic `network-bridge-error`. Recommend feature-detect and degrade to PerformanceObserver-only when injection fails; also consider `postMessage` origin check already present (correct). |
| **HTML parsing XSS** | ✅ Safe | `DOMParser.parseFromString(body, 'text/html')` does not execute `<script>`; querySelector extraction only reads `href/src/action/content`. No `innerHTML` assignment of untrusted body to live document. Panel `innerHTML` is static (no interpolation of body). |
| **URL extraction regex DoS** | ⚠️ Low | `extractUrlsFromText` runs two global regexes over `body` up to 2 MB + `doc.documentElement.outerHTML`. Worst-case O(n) but with backtracking paths `/(?:^|["'(\s])((?:\/|\.\.?\/)[...-]+)/g` on pathological bodies could be expensive. Bound by `maxBodyChars` and debounce; acceptable. |
| **Storage exhaustion** | ⚠️ As above | Persisted observations with bodies can fill `GM_setValue` quota. Recommend stripping bodies from persisted slice. |
| **Privacy / PII** | ⚠️ Note | Ledger persists every discovered URL (including query strings) to `GM_setValue`. URLs may contain session tokens. Document that `Clear` requires `GM_setValue(STORAGE_KEY,null)` + reload, and that Export includes raw discoveries. |

No `eval()`, no `new Function()`, no unsanitized `href` navigation. Overall safe for a userscript.

---

## 6. Robustness & Edge Cases

### 6.1 Edge Handling — Pass

- Empty/null `target` → `discover()` returns `null`.
- Malformed URL → `canonicalizeUrl` returns `null` → `discover` aborts.
- Non-http scheme (`mailto:`, `blob:`, `data:`) → `isAllowedUrl` false → Policy `url-not-allowed`.
- `candidate.depth > maxDepth(5)` → `max-depth` denial — prevents infinite expansion loops (e.g., sitemap pointing to itself).
- `maxBodyChars 2M` truncation with `bodyTruncated` flag — prevents OOM from 100 MB HTML.
- `fingerprintMaxChars 1M` sampled hash — avoids hashing multi-MB bodies fully.
- `retry.maxRetries:2` exponential backoff `500 → 1000 → 2000` capped at 8s — correct.

### 6.2 Failure Modes — Partial

- **Origin starvation:** `OriginController.acquire()` loops `while(true) { if active<2 && elapsed>150ms then reserve else sleep(50) }`. Under sustained load with 4 workers on 1 origin, 2 workers will sleep-poll. Works, but no fairness guarantee; a burst of high-priority candidates for origin A can starve lower-priority candidates for origin B blocked behind A’s `minRequestInterval`. Lower priority than concurrency bug above.

- **MutationObserver volume:** `installMutationObserver` debounced at 250 ms and queries `a[href], script[src], link[href]` on each flush. On a SPA that mutates 100s of nodes per frame (e.g., virtualized list), this can discover 100s of duplicate candidates per flush. Dedup via `candidateKeys` absorbs duplicates but `discover()` still allocates a `Candidate` object per mutation batch. Acceptable, but worth adding a per-flush `Set` to avoid allocating duplicates within batch.

- **PerformanceObserver evidence-only guard:** Correct fix in v0.7.1. Earlier versions assumed `entry.name` → `GET candidate`. Now only `script/link/img/iframe/stylesheet` are executable GET-like; `fetch/xmlhttprequest` are “evidence only unless bridge provides method.” This prevents promoting a `POST /api` resource timing into a `GET` acquisition (the bug noted in planning doc §3).

### 6.3 Resource & Ledger Limits

`maxNetworkEvents:1000`, `maxGraphEdges:5000`, `maxDiagnostics:500`, `persistedLedgerEvents:5000`. All FIFO/eviction capped. Ledger `seq` is monotonic across restore (recomputed from max if missing). Good.

---

## 7. Performance & Scalability

| Operation | Complexity | Bound | Comment |
|---|---|---|---|
| `claimNextCandidate()` sort | `O(n log n)`, n = `candidates.size` | max 750 | Acceptable. Could use heap for 10k scale, not needed here. |
| `addCandidate()` dedup | `O(1)` Map lookup | — | Correct. |
| Provider matching | `O(p)`, p=7 | — | Sequential; each provider scans body once. Worst-case 7 full scans of 2 MB body per observation. Acceptable for `concurrency:4`. |
| URL extraction regex | `O(body.length)` per provider | 2 MB | Dominant cost. CSS/JS providers each run a regex; okay. |
| Persistence JSON.stringify | `O(serialized size)` | debounce 400 ms | Body-inclusive observations are the cost driver; recommend excluding bodies. |

Memory: `candidates` Map retains completed entries (P0-1); `discoveries` Map unbounded in-memory (persisted slice 1200 is only for storage, not RAM). On a site with 500+ unique URLs, heap grows linearly with discoveries. Recommend LRU eviction for in-memory `discoveries` or summary view.

---

## 8. Documentation Accuracy & Drift

| Doc Section | Accurate? | Detail |
|---|---|---|
| README “Current Prototype can” (11 bullets) | ✅ largely | All 11 hold; 8 are exceeded in v0.7.1 |
| README Architecture diagram (Scheduler→Candidate→Acquisition→Observation→ProviderRegistry→Discovery) | ✅ | Diagram matches code; missing `AcquisitionPlan/OriginController/Ledger` layers added in v0.7.1 (should be updated) |
| README Candidate Lifecycle `QUEUED→CLAIMED→COMPLETED/FAILED` | ✅ | Now has richer substates: `discovered→queued→claimed→planned→acquiring→observed→recognized→expanded→completed` plus `skipped/failed`. Diagram simplified, not wrong. |
| README Search Strategy formula | ✅ conceptual | Not wired to runtime; `effectivePriority()` uses typeWeight+confidence-depth-retry heuristics as a simplified instantiation — acceptable. |
| README Generic Discovery Loop pseudocode | ✅ | Loop pseudocode matches `worker()` flow. |
| README Scope: “does not implement RF” | ✅ | No RF code, disclaimer preserved in v0.7.1 header. |
| README Roadmap Phase 0 checkboxes all `[x]` | ✅ | True for v0.7.1. |
| README Roadmap Phase 1 `[ ] formal provider interface` | ❌ **stale** | `Provider` base + `ProviderRegistry` + 7 providers already implemented. Should be `[x]`. |
| README Roadmap Phase 1 `[ ] candidate/observation fingerprints` | ❌ **stale** | `fnv1a32` + `makeFingerprint` + `fingerprintIndex` already shipped. |
| README Roadmap Phase 1 `[ ] candidate expiration` | ❌ **partially stale** | Retry delay via `nextAttemptAt` exists; expiration TTL not yet. |
| README Roadmap Phase 1 others (retry, coverage, event stream, logging) | partially stale | Retry + DecisionLedger exist; coverage metrics not yet computed. |
| README Roadmap Phase 2 “HTTP headers / XML / RSS / sitemap …” | ❌ **understated** | XML/sitemap already done via XmlProvider + extractXmlLocs. Headers provider not yet. |
| `Continue Architecture Planning.md` as history | ✅ | Accurate chat log; but single 2.2 MB file is unwieldy for contributors. |

**Recommendation:** Refresh README to v0.7.1 (see patch suggestion in §10) and split planning doc into `docs/architecture-decisions/*.md` + `CHANGELOG.md`.

---

## 9. Gaps & Technical Debt

**Blocked by missing artifact (P1):**

- [ ] No extractable `generic-discovery-engine.user.js` in repo — cannot `npm run lint`, cannot `node --check` in CI, cannot diff versions.
- [ ] No tests: claim atomicity, dedup, policy denial, retry backoff, leaderboard ordering, fingerprint stability, XML/CS link extraction. A 30-line harness that fakes `location.href` and calls `KnowledgeBase` + `AcquisitionPolicy` would catch P0-1/2.
- [ ] No lint/type: `eslint` + `prettier` + `JSDoc` or TypeScript declarations for Candidate/Observation/Discovery shapes.
- [ ] No `CHANGELOG.md`: versions exist only as chat headings; no git tags.

**Design debt:**

- `KnowledgeBase.visited` vs `candidateKeys` duality (§4.2).
- `cap` counts completed as live (§4.2).
- `candidate.alternate*` arrays grow without bound for hot URLs.
- `discoveries` Map unbounded in RAM.
- `OriginController` poll-loop vs semaphore.

**Docs debt:**

- Roadmap p1–p4 checkboxes stale vs code reality.
- No “Threat Model” or “Privacy” section despite persistence of URLs.

---

## 10. Recommendations (Prioritized)

### P0 — Fix before next release

1. **Fix `maxCandidates` live-vs-completed semantics.** Change `addCandidate` guard to count only `queued|claimed|planned|acquiring|observed|recognized|failed(retryable)` or delete completed from the indexed live set. One-line patch, high impact.
2. **Fix persistence body bloat.** Exclude `body` from `db.serialize().observations` persisted slice, or persist observations as `{id, candidateId, http, fingerprint, status}` only. Keep bodies in-memory only. Prevents quota failure on second scan.

### P1 — Ship alongside P0

3. **Extract distributable artifact.** Move v0.7.1 header+body to `dist/generic-discovery-engine.user.js` (or `src/engine.js`), add `@updateURL` + `@downloadURL` once hosted, and make Markdown reference it rather than embed.
4. **Refresh README:** replace Architecture diagram with v0.7.1 layering (`Candidate → Policy → Plan → Budget → OriginSlot → Acquisition → Observation → Providers → Discovery`), update Phase-1 checkboxes to `[x]` for shipped items, bump `version` badge to `0.7.1`, note ledger & network bridge.
5. **Add minimal invariant tests** (run with `node --test`): claim atomicity (50 concurrent claims yield 50 unique ids), dedup (same URL+type enqueued once, priority max preserved), policy denials (non-GET, maxDepth, binary), retry backoff.

### P2 — Next iteration

6. **Narrow `@connect` when `sameOriginOnly:true`** — use `@connect self` or document risk.
7. **Deduplicate per-observation discoveries** across providers (`Set<canonical>`).
8. **Batch mutation dedup** within `observeCurrentDom()` flush (`Set` before `discover()` loop).
9. **Add coverage/budget metric:** `frontierSize`, `queuedByType`, `requestsRemaining`, exposed in UI + export.
10. **Split `Continue Architecture Planning.md`** into `docs/decisions/NNN-title.md` with ADR template; generate `CHANGELOG.md` from ledger.

---

## 11. Verification Checklist (Pass/Fail)

| Check | Result | Evidence |
|---|---|---|
| Single-threaded claim-before-await holds | **PASS** | `GenericDiscoveryEngine.worker()` line ~ 3720; `KnowledgeBase.claimNextCandidate()` synchronous |
| Candidate identity dedup works | **PASS** (with P0 caveat) | `candidateKeys Map<type:target,id>` + `visited` Set; duplicate `addCandidate` returns existing with priority max |
| Provider pipeline extensible | **PASS** | `Provider` base + 7 subclasses + `ProviderRegistry.matching()`; `HtmlProvider` emits typed discoveries |
| Observation ≠ Discovery separation | **PASS** | `Observation` carries transport evidence; `Discovery` carries interpreted kind/confidence/mechanism/provenance |
| Provenance answers “why?” | **PASS** | `Discovery.provenance` + `graphEdges` + `ResourceRecord.parents`; example `initial page → HTML → link → JSON → URL` traceable |
| Persistence bounded | **PASS** (conditional) | Bounded slices 1200/1500/3000/5000; **FAIL** if bodies included (P0-2) |
| Scope disclaimer accurate | **PASS** | README + v0.7.1 header both state “not RF / not DVB-compatible” |
| Security defaults safe | **PASS** | `sameOriginOnly:true`, `acquireForms/Media/Binary:false`, no eval/innerHTML of untrusted body |
| Network bridge method-trust fix | **PASS** | Performance `fetch/xhr` treated as evidence-only; only bridge `GET` promotes to candidate |
| Adaptive concurrency responds to failure | **PASS** | `onSuccess/onFailure` clamp with thresholds 4/2 |
| Export includes ledger | **PASS** | `exportData()` includes `ledger.export()` + `networkEvents` + `diagnostics` |
| Node syntax valid | **PASS** | `node --check /tmp/v071.js` exit 0 |

---

## 12. Experimental Verification (Static)

Executed during audit:

```sh
python3 -c "extract fence at 1355200→1495770" > /tmp/v071.js
node --check /tmp/v071.js           # PASS
grep -c "class " /tmp/v071.js       # 21 classes
grep -c "function " /tmp/v071.js    # 27 utils
grep "AcquisitionPlan\|DecisionLedger\|OriginController" /tmp/v071.js  # all present
```

Not executed (requires browser runtime): live fetch, DOMParser against real pages, GM storage round-trip, network bridge under CSP. Recommend adding a headless `jsdom` + `msw` harness for those paths.

---

## 13. Conclusion

The project successfully demonstrates that **the blind-scan control pattern generalizes beyond DVB**. The architecture — especially the v0.7.1 ledger, policy, and resource graph — is more rigorous than a typical userscript crawler and gives the prototype real research value as a “discovery substrate” for web resources.

The implementation is *prototype-correct* but not yet *product-robust*: two P0 capacity bugs and persistence bloat are the only blockers to a trustworthy `v0.7.1` release. Fixing them, extracting the distributable file, and syncing README to code would move the grade from **B (prototype)** to **A- (releasable research tool)** without changing the DVB analogy’s validity.

**Suggested commit message for this report:**

```
docs: add deep verification report (v0.7.1)

- audit architecture, concurrency, providers, ledger, persistence
- verify all Phase-0 claims; flag README drift vs v0.7.1
- file P0 bugs: maxCandidates live-count, visit/keys duality, body persistence
- grade B→A- path with prioritized fixes
```

---

## Appendix A — Provenance of This Report

- Sources: `README.md` (cc8df73), `Userscript Discovery Prototype.md`, `Continue Architecture Planning.md` (12 embedded versions), extracted `v0.7.1` fence (5,164 lines).
- Tooling: `node --check`, `grep`, `python3` fence extraction, manual line-level code reads.
- No network fetches performed; no secrets accessed.

## Appendix B — Minimal Patch Sketch (for P0-1)

```js
// KnowledgeBase.addCandidate — replace size guard:
const liveCount = [...this.candidates.values()].filter(c =>
    !['completed','skipped'].includes(c.status)
).length;
if (liveCount >= CONFIG.maxCandidates) { /* diagnostic */ return null; }

// KnowledgeBase.serialize — strip bodies:
observations: [...this.observations.values()]
    .map(o => ({...o.serialize(), body: undefined}))
```

---

*End of report.*
