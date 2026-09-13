# Deep Static Verification — Generic Discovery Engine v1.4.0 (arena/01a08cd3-generic-discovery-engine)

> **Branch:** `arena/01a08cd3-generic-discovery-engine` — 21 commits ahead of `main` (`cc8df73`), not behind  
> **Artifact:** `dist/generic-discovery-engine.user.js` v1.4.0 `6394 lines` `200208B` `sha256 4f2c63fd4723d854c2c0464da090a19c291d25fe7c6b241c7bc39b431902bd54` + `dist/generic-discovery-engine.min.js` `65367B 32.6%` `6c3103…` + `dist/generic-discovery-engine.esm.js` `267B` `792783…`  
> **Source:** `src/` 7 modules (`config` health+concurrent, `engine` getHealthMetrics + Promise.all) + 30 ADRs  
> **Tests:** `npm test` `160/160 42 suites` (`node --check` PASS, `verify:build` PASS)  
> **Date:** 2026-09-13 — deep static verification against primary external docs (ETSI DVB-SI, MDN Fetch/DOMParser/Trusted Types/CORS, c8 coverage, tsc)  
> **Verdict:** **ARCHITECTURALLY STRONG, IMPLEMENTATIONALLY REAL, BUT NOT YET “VERIFIED” in the strong assurance sense**

Extends `VERIFICATION_REPORT.md` (v0.7.1) + supplements `v0.7.2→v1.4.0` + `docs/analysis/DEEP_DVB_AUDIT_v0.8.2.md` + `docs/SECURITY_AUDIT.md` + `docs/PERFORMANCE_ANALYSIS.md` + 30 ADRs.

---

## Verification Verdict (summary matrix)

| Area | Verdict | Confidence |
|------|---------|------------|
| Generic discovery architecture | **PASS** | High |
| DVB → generic control-loop analogy | **PASS** | High |
| Candidate ownership / claim-before-await | **PASS** | High |
| Policy-before-acquisition | **PASS** | High |
| Global request reservation | **PASS** | High |
| Provider architecture | **PASS** | High |
| Provenance / causal graph | **PASS** | High |
| Actual runnable artifact | **PASS** | High |
| Build reproducibility mechanism | **PASS, with limitations** | High |
| Security defaults | **Mostly PASS** | High |
| Same-origin acquisition guarantee | **PARTIAL** | High |
| Memory boundedness | **FAIL** | High |
| Adaptive concurrency claim | **PARTIAL / misleading** | High |
| Health-state verification | **PARTIAL** | High |
| Test coverage claim | **MISLEADING** | High |
| Type-check verification | **WEAK** | High |
| Documentation consistency | **FAIL / drift remains** | High |

> Several issues are **not currently caught** by the repository's own verification reports.

---

## 1. The project has crossed an important architectural threshold

The old v0.7.1 verification report described the project as prototype-grade, with the major architecture already sound. That report is now substantially superseded: the current branch contains a real `src/` implementation, generated `dist/`, package metadata, tests, build scripts, 30 ADRs, security/performance documentation, and v1.4 verification material.

The branch is also 21 commits ahead of main and not behind it, so this is a genuine development line rather than a stale copy.

The current artifact is:

```
v1.4.0
6394 lines
200,208 bytes
13 providers
7 source modules
160 tests claimed
SHA-256: 4f2c63fd4723d854c2c0464da090a19c291d25fe7c6b241c7bc39b431902bd54
```

and the current v1.4 verification supplement reports 160/160 tests, `node --check`, `verify:build`, `typecheck`, coverage gate, minified build and ESM build.

So the project is no longer accurately characterized as “code embedded in planning documents.” That old finding has been fixed.

---

## 2. DVB analogy: verified and defensible

The project explicitly defines:

```
DVB blind scan              Generic Discovery
frequency                   candidate
signal detection            acquisition
demodulation                observation
validation / PSI            recognition
NIT/network discovery       expansion
```

and deliberately states:

> DVB-inspired, not DVB-compatible.

That distinction is correct. ETSI's DVB-SI specification defines the NIT as carrying information about the physical organization of multiplexes/transport streams and the network itself. It can therefore participate in discovering additional network resources.

Your abstraction is **not** claiming `HTTP == RF`, `URL == frequency`, `HTML == MPEG-TS`. Instead it claims:

```
unknown search space → candidate → acquisition → observation → recognition → metadata/discovery → new candidates → scheduler ↺
```

That is a legitimate control-pattern abstraction. The important difference is correctly identified:

- **DVB:** bounded/exhaustive physical search space
- **GDE:** open-world/budgeted search space

DVB coverage can approach exhaustive coverage of a bounded parameter space; web discovery cannot generally make the same claim. So: **DVB analogy = PROVED as an architectural analogy** — not as a universal theory of discovery, but strong enough to justify the project.

---

## 3. Candidate ownership invariant is genuinely implemented

This is one of the strongest parts.

```
worker
  ├── claimNextCandidate() → status = claimed   // synchronous
  └── await executePlan()
```

The claim occurs **synchronously before** the first asynchronous acquisition. `KnowledgeBase.claimNextCandidate()` selects a queued/failed candidate and changes its state to `claimed`; the worker subsequently awaits acquisition. Therefore two workers cannot both obtain the same queued candidate through the normal path.

This is materially different from `peek() → await acquire() → remove()` which would race. The project has `claimNextCandidate(); await executePlan(candidate);` — **PASS**, a real architectural invariant.

---

## 4. Policy-before-acquisition is also real

```
Candidate → AcquisitionPolicy → AcquisitionPlan {allowed, reason, method, origin, expectedType, policyInputs} → budget → origin controller → network
```

`AcquisitionPolicy.plan()` explicitly rejects non-HTTP(S), cross-origin under `sameOriginOnly`, non-GET, excessive depth, forms, media, binary, disabled frames/scripts/stylesheets/network candidates. Decision ≠ side effect and the decision itself is ledgered. This makes the system substantially more auditable than a simple crawler. **PASS.**

---

## 5. The global request-budget invariant is real

```js
reserveRequestSlot() {
  if (this.requestsReserved >= CONFIG.maxRequests) return false;
  this.requestsReserved++;
  return true;
}
```

Reservation happens synchronously before acquisition. Concurrent workers cannot independently observe `149 used` and all decide one more is available. **PASS.**

---

## 6. Provider architecture is now genuinely extensible

13 providers: `HTML, JSON, XML, CSS, JavaScript, Robots, Headers, SitemapIndex, OpenAPI, WellKnown, Manifest, Binary, Text` with factories, lazy instantiation, metrics and deterministic ordering.

```
Observation → ProviderRegistry.matching() → Provider[] → recognize() → Discovery[]
```

Concurrent mode also preserves provider-order processing after `Promise.all`, so completion timing does not determine discovery ordering. **PASS** — solid foundation for independently testable plugins.

---

## 7. Security review: several protections are real

The audit correctly identifies: https/http only, same-origin default, GET only, forms/media/binary disabled, body truncation, `DOMParser`, Trusted Types bridge, network-method verification. URL guard rejects `javascript:`, `data:`, `mailto:`, `ftp:` and cross-origin under default policy. HTML provider uses `DOMParser.parseFromString()` into a separate document where scripts are non-executable (MDN). **No obvious remote-HTML → arbitrary script execution path — justified.**

---

## 8. But there is a real same-origin weakness: redirects (P1)

Code verifies `isAllowedUrl(plan.target)` but fetch fallback uses:

```js
fetch(plan.target, { method: plan.method, credentials: 'same-origin', redirect: 'follow', signal })
```

Policy controls the initial URL, not necessarily the eventual URL. Browser Fetch follows redirects by default; MDN recommends `redirect: 'error'` when redirects are unexpected because checking the final URL after the redirect is too late.

```
Current guarantee: candidate URL ∈ same-origin → fetch → possibly redirected elsewhere
Desired: candidate URL ∈ same-origin → every network hop ∈ same-origin
```

CORS may prevent reading a cross-origin final response, but does not mean the request never happened (simple cross-origin requests can still be sent under CORS).

**Recommendation:** For strict `sameOriginOnly` mode: `redirect: 'error'` or explicit redirect validation. `sameOriginOnly=true → redirect=error` and make following redirects an explicit policy capability. **Severity: P1** — not immediate RCE, but “same-origin acquisition” invariant is stronger in docs than in fetch.

---

## 9. The biggest technical finding: memory is NOT actually bounded

Architecture claims `maxCandidates=750, maxObservations=800, maxGraphEdges=5000, maxDiagnostics=500` but these do not constitute a complete memory bound.

### 9.1 Observations alone can become enormous

```
maxBodyChars = 2,000,000
maxObservationsInMemory = 800
maxRequests = 150

Each Observation retains its complete body in memory.
Serialization removes body (good for persistence), but does nothing for runtime.
Worst-case raw body: 150 × 2M chars ≈ 300M chars ≈ ~600 MB UTF-16
+ DOMParser allocations, normalized strings, regex, discoveries, JSON, fingerprints...
```

Documented `Heap worst-case ≈ 6 MB` is **not credible** for current implementation. Correct model:

```
O(observations × body_size + parsed_provider_state + discoveries + resources + candidates + ledger)
not merely O(750+800+5000)
```

---

## 10. Discoveries and resources are not actually capped in memory

`addDiscovery()` inserts directly into `this.discoveries.set(id, discovery)` with no runtime eviction; `ensureResource()` likewise creates resources without a global cap. Persistence slices `discoveries.slice(-persistedDiscoveries)` — that limits serialization, not memory. So `persistedDiscoveries=1200` ≠ max 1200 discoveries in RAM; it means when serializing, retain last 1200.

A hostile or enormous document can produce `2 MB body → thousands of URLs → thousands of Discovery/ResourceRecord` while candidate cap may prevent only some URLs from becoming candidates. **P1 resource-exhaustion.**

Proper invariant: **runtime collection cap AND persistence cap**, not merely persistence slice.

---

## 11. Candidate memory also grows across long-lived operation

`maxCandidates` was changed to count only live candidates:

```js
const liveCount = [...this.candidates.values()].filter(c => !['completed','skipped'].includes(c.status)).length;
```

That fixes “completed permanently consume capacity” but creates: completed remains in `this.candidates`, not evicted. So `candidates Map, candidateKeys, visited, patternIndex, clusterIndex` grow without long-term eviction. `maxCandidates` is a **frontier bound, not total-memory bound** — useful distinction, but docs treat system as more memory-bounded than it is.

---

## 12. Network-event cap can be bypassed

`recordNetworkEvent()` checks `if (size >= maxNetworkEvents) return;` but `handleBridgeEvent()` directly does `this.engine.networkEvents.set(key, {...})` before `observeNetworkGet()`. Bridge-generated events do not consistently pass through the cap. `networkEvents.size <= 1000` not guaranteed. **Fix:** centralize insertion via `recordNetworkEvent()` and never write directly to `networkEvents`. **P1/P2** depending on deployment duration.

---

## 13. Adaptive concurrency is currently mostly observability, not control

Code starts `for (i=0; i<currentConcurrency; i++) workers.push(worker());` with `currentConcurrency=4` so four workers exist. Later `onFailure()` can reduce `currentConcurrency: 4→3→2→1` but does not stop workers; `onSuccess()` can increase number but does not create additional workers. During a running scan actual active worker count and `currentConcurrency` can diverge (e.g., start 4 workers, threshold reduces to 2, actual still 4). Current feature is better described as **adaptive concurrency target for subsequent launches** rather than dynamically adaptive concurrency. v1.4 supplement calls it adaptive without distinction.

**Recommendation:** rename to `nextConcurrency` or implement real worker pool/semaphore whose capacity changes dynamically. Preferred: `Scheduler → ConcurrencyController → Permit/Semaphore → Acquisition`.

---

## 14. Health verification contains a logical dead branch

`getHealthMetrics()` computes:

```js
const recentDiagnostics = this.db.diagnostics.slice(-(CONFIG.health?.maxRecentErrors ?? 20));
if (recentDiagnostics.length > CONFIG.health.maxRecentErrors) status = 'unhealthy';
```

This condition cannot normally be true — you already sliced to at most `maxRecentErrors`, so `length <= maxRecentErrors` by construction. The `recentDiagnostics.length > maxRecentErrors` unhealthy transition is **dead**. v1.4 test claims to verify healthy/degraded/unhealthy/disabled, but its “unhealthy” case uses `liveCount=750`, not the recent-error branch.

**Fix:** calculate from underlying count:

```js
const diagnosticCount = this.db.diagnostics.length;
const recentDiagnostics = this.db.diagnostics.slice(-maxRecentErrors);
if (diagnosticCount > maxRecentErrors) degraded/unhealthy...
```

Or define a real rolling error-rate metric.

---

## 15. totalProviders is not necessarily 13

Because providers are lazy (`this.instances = new Map()`), instances are created only when requested. `getHealthMetrics()` obtains `providerMetrics` from instantiated providers. Therefore `totalProviders` can mean providers instantiated so far rather than providers configured. At initialization this can be zero even though registry has 13. Semantics should be separated: `configuredProviders=13, instantiatedProviders=N, activeProviders=M` for observability.

---

## 16. The test suite is much weaker than “160/160” suggests

`npm test = 160/160` is useful evidence, but much of suite is static verification or behavioral mirrors, not direct execution of source modules. E.g., `canonicalize-and-policy.test.js` explicitly says it “mirrors the patched helpers” and reimplements `canonicalizeUrl, isAllowedUrl, AcquisitionPolicy`, and `health-concurrent.test.js` contains “Minimal harness for health logic (mirrors src)” rather than invoking actual implementation. Test implementation can diverge from production without failing.

Exception: **E2E test loads actual dist artifact** (`e2e-discovery-loop.test.js` reads `../dist/generic-discovery-engine.user.js` via `vm.Script`) — genuine artifact-level testing.

Correct assessment: `160 tests = some actual artifact execution + many mirrored/static tests`, not `160 tests directly exercising the implementation`.

---

## 17. The coverage claim is materially misleading

`.c8rc.json`:

```json
{ "include": ["tests/*.test.js"], "exclude": ["dist/**"] }
```

Coverage tool measures test files, not production engine. Repository simultaneously reports `coverage:check 85/75/80` and very high line coverage, but because `dist/` is excluded and only `tests/*.test.js` included, that number cannot be interpreted as “85%+ of GDE runtime code is covered.” It is essentially “test code itself satisfies thresholds.” **Not useful as production-code coverage.** Fix: instrument actual runtime artifact or preferably source modules `src/**/*.js → tests/**/*.test.js → coverage`, excluding tests/scripts/build artifacts from measured production set.

---

## 18. Typecheck is also weaker than advertised

`package.json`:

```json
"typecheck": "tsc ... 2>&1 | head -n 100 || echo ..."
```

Pipeline's final command is `head`, so failing `tsc` can be masked. Without `set -o pipefail` or direct `tsc` invocation, not a reliable CI gate. `typecheck PASS` should currently be interpreted as “typecheck command completed through its wrapper” not “TypeScript checker definitely returned success.” **Verification flaw.**

---

## 19. lint is not actually lint

`package.json`:

```json
"lint": "node --check dist/... && echo \"lint: syntax OK (eslint optional)\""
```

Repository says ESLint is optional, so `npm run lint` currently means **JavaScript syntax check**, not ESLint static analysis. Not a runtime defect, but nomenclature should be corrected.

---

## 20. The @connect header is inconsistent

Source header contains:

```
@connect self
@connect * — uncomment if CONFIG.sameOriginOnly=false
```

But wildcard line is not commented out; generated v1.4 artifact has same active wildcard. Tampermonkey documents `@connect *` as permitting all domains, whereas `@connect self` restricts to current domain. Runtime policy still prevents cross-origin acquisition under `sameOriginOnly:true`, so not equivalent to “engine freely fetches arbitrary origins,” but from least-privilege:

```
runtime: same-origin
declared capability: all origins  — unnecessarily broad
```

Security audit recognizes wildcard. **Better:** generate `@connect self` for default artifact; build separate cross-origin artifact when explicitly enabled.

---

## 21. The documentation has significant version drift

Project has improved enormously, but some docs still contain historical leftovers. E.g., `OVERVIEW.md` says `Module Map (v1.3.0)` while describing v1.4 features, and contains older `Providers 9` language alongside current 13-provider architecture. README is much better and correctly identifies v1.4. Repository moved from `documentation severely stale` to `documentation mostly current but internally inconsistent` — progress, but for verification-oriented project docs should be treated as executable specifications.

---

## 22. A deeper architectural issue: “bounded” needs to be split into three concepts

Currently system mixes search bound, storage bound, execution bound — they are different.

| Layer | Example bounds |
|-------|----------------|
| **Search Budget** | `maxDepth, maxCandidates, maxRequests, per-origin requests` |
| **Runtime-memory Budget** | Currently incomplete: `observations, discoveries, resources, candidates, visited, patternIndex, clusterIndex, networkEvents, ledger` |
| **Persistence Budget** | Currently better: `persistedDiscoveries, persistedResources, persistedEdges, persistedLedgerEvents` |

Architecture should explicitly define:

```
┌──────────────────┐
│ Search Budget    │
├──────────────────┤
│ candidates       │
│ requests         │
│ depth            │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Runtime Budget   │
├──────────────────┤
│ bodies           │
│ discoveries      │
│ resources        │
│ indexes          │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Persistence      │
├──────────────────┤
│ serialized data  │
│ retention        │
└──────────────────┘
```

That would make system much more rigorous.

---

## 23. What I would classify as the actual invariants today

After audit, freeze these as proven invariants:

- **I-1 — Candidate ownership:** At most one worker can transition a queued candidate to claimed via `claimNextCandidate()`. *PROVED statically.*
- **I-2 — Policy gate:** No candidate reaches `Acquisition.execute()` unless `AcquisitionPolicy.allowed == true`. *PROVED statically.*
- **I-3 — Global reservation:** `requestsReserved <= maxRequests` for engine-managed acquisitions. *PROVED statically.*
- **I-4 — Scheme/origin admission:** `discover()` rejects non-http(s) and cross-origin when `sameOriginOnly=true`. *PROVED.*
- **I-5 — Provider recognition:** `Observation → zero or more providers → discoveries` *PROVED structurally.*
- **I-6 — Per-observation discovery dedup:** same target URL emitted at most once via `processDiscoveries()` *PROVED structurally.*
- **I-7 — Persistence serialization bounds:** persisted discoveries/resources/edges/ledger sliced to retention *PROVED.*

Not yet proven:

- I-8 runtime memory bounded
- I-9 total knowledge graph bounded
- I-10 same-origin across redirects
- I-11 adaptive concurrency actually changes active concurrency
- I-12 health error pressure correctly transitions state
- I-13 production-code coverage ≥ declared threshold
- I-14 typecheck failure cannot be masked
- I-15 networkEvents cap always holds

---

## 24. Verification status matrix

```
Architecture
 ├── DVB abstraction             PASS
 ├── discovery loop              PASS
 ├── provenance                  PASS
 ├── provider model              PASS
 └── policy/control plane        PASS

Concurrency
 ├── claim exclusivity           PASS
 ├── request reservation         PASS
 ├── origin throttle             PASS
 └── adaptive concurrency       PARTIAL

Security
 ├── scheme filtering            PASS
 ├── same-origin initial URL     PASS
 ├── redirect boundary           FAIL
 ├── DOMParser isolation         PASS
 ├── network bridge isolation    PARTIAL
 └── least-privilege @connect   FAIL

Resource safety
 ├── request budget              PASS
 ├── body truncation             PASS
 ├── observation eviction        PASS
 ├── discovery eviction          FAIL
 ├── resource eviction          FAIL
 ├── candidate history bound    FAIL
 └── network event bound        FAIL

Verification infrastructure
 ├── actual artifact E2E         PASS
 ├── static tests                PASS
 ├── mirrored tests              WEAK
 ├── production coverage        FAIL
 ├── typecheck gate              WEAK
 ├── lint gate                  WEAK
 └── deterministic build        PASS
```

---

## 25. Priority order I recommend

Would not add another provider yet — architecture has enough provider coverage. Instead:

**P0 — Verification integrity** — Fix (1) c8 production coverage, (2) typecheck exit-code masking, (3) real ESLint gate. Otherwise “verified” status is overstated.

**P1 — Runtime safety** — Fix (4) runtime discovery/resource eviction, (5) observation/body memory strategy, (6) candidate/index historical retention, (7) networkEvents cap bypass.

**P1 — Security boundary** — Fix (8) redirect policy, (9) @connect self vs wildcard.

**P1 — Control semantics** — Fix (10) real adaptive concurrency, (11) health error-pressure logic, (12) configured vs instantiated provider metrics.

**P2 — Documentation** — Synchronize README, OVERVIEW, SECURITY_AUDIT, PERFORMANCE_ANALYSIS, v1.4 supplement, ADRs against actual v1.4 code.

---

## 26. The next architectural step

The project is ready for transition beyond v1.5 — from Generic Discovery Engine to **Discovery Kernel**:

```
Generic Discovery Engine
          ▼
   Discovery Kernel
   ┌──────┼────────┐
   ▼      ▼        ▼
Search  Resource  Evidence
Budget   Budget    Ledger
   │      │        │
   └──────┼────────┘
          ▼
     Control Loop
```

Introduce explicit contracts: `SearchBudget, RuntimeBudget, PersistenceBudget, AcquisitionPolicy, EvidencePolicy, ResourceRetentionPolicy, ConcurrencyController`. Then the system can make stronger claim:

> Every externally observable action is admitted by policy, consumes an explicit budget, produces evidence, and has bounded retention.

That would be significant conceptual upgrade.

---

## Bottom line

The deep audit **strengthens the thesis, rather than breaking it**. Central architecture is real (`Candidate → Policy → Plan → Budget → Acquire → Observation → Recognition → Discovery → Provenance → Candidate expansion ↺`), DVB abstraction is defensible and technically meaningful (ETSI NIT model supports analogy).

But project currently makes stronger verification claim than evidence warrants:

> The engine has bounded search, but it does not yet have bounded runtime state.

And:

> 160/160 is evidence that test suite passes; it is not yet evidence that production implementation has 85%+ verified coverage.

Three things to fix before calling architecture v1.5 / verification-grade:

1. **Real production-code coverage**
2. **Hard runtime-memory/knowledge retention bounds**
3. **Hard acquisition-boundary semantics including redirects**

After those, project moves from “well-tested research prototype” toward “auditable discovery runtime.”

---

*Source: deep static verification of `arena/01a08cd3-generic-discovery-engine` (v1.4.0, 6394 lines, 4f2c63…, 13 providers, 160 tests claimed) — 1m 30s analysis of repo structure, src/, dist/, tests, build/verification scripts, security audit, architecture docs, v1.4 supplement, cross-checked against ETSI DVB-SI, MDN Fetch/DOMParser/Trusted Types/CORS, c8, tsc.*  
*Generated: 2026-09-13 — saved as markdown per request.*
