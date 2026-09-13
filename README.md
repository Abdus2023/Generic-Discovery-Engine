# Generic Discovery Engine

> **Current release:** `v1.0.0` — stable (generic discovery loop feature-complete) (src/ → dist/ deterministic) (see [`VERIFICATION_REPORT.md`](VERIFICATION_REPORT.md), [`VERIFICATION_SUPPLEMENT_v0.7.2.md`](VERIFICATION_SUPPLEMENT_v0.7.2.md), [`VERIFICATION_SUPPLEMENT_v0.7.6.md`](VERIFICATION_SUPPLEMENT_v0.7.6.md), [`VERIFICATION_SUPPLEMENT_v0.7.7.md`](VERIFICATION_SUPPLEMENT_v0.7.7.md), [`VERIFICATION_SUPPLEMENT_v0.7.8.md`](VERIFICATION_SUPPLEMENT_v0.7.8.md), [`VERIFICATION_SUPPLEMENT_v0.7.9.md`](VERIFICATION_SUPPLEMENT_v0.7.9.md), [`VERIFICATION_SUPPLEMENT_v0.8.0.md`](VERIFICATION_SUPPLEMENT_v0.8.0.md), [`VERIFICATION_SUPPLEMENT_v0.8.1.md`](VERIFICATION_SUPPLEMENT_v0.8.1.md), [`VERIFICATION_SUPPLEMENT_v0.8.2.md`](VERIFICATION_SUPPLEMENT_v0.8.2.md), [`VERIFICATION_SUPPLEMENT_v0.9.0.md`](VERIFICATION_SUPPLEMENT_v0.9.0.md), [`VERIFICATION_SUPPLEMENT_v0.9.1.md`](VERIFICATION_SUPPLEMENT_v0.9.1.md), [`VERIFICATION_SUPPLEMENT_v1.0.0.md`](VERIFICATION_SUPPLEMENT_v1.0.0.md), [`CHANGELOG.md`](CHANGELOG.md), [`dist/generic-discovery-engine.user.js`](dist/generic-discovery-engine.user.js)). `node --check` PASS · `npm test` 126/126 PASS (incl. 6-test E2E + hardening + 7 fuzz + 8 priority + 13 determinism + 8 lifecycle + 6 concurrency + 7 pattern + 12 robots/headers/change + 6 src/build + 6 export/inference + 5 pattern-guided/revisit) (bundler + adaptive) · `v0.7.1` archived as `dist/generic-discovery-engine.v0.7.1.user.js` · `src/` 7-file mirror (`config`/`utils` extracts) + `verify:build` src gate · new: [`docs/SECURITY_AUDIT.md`](docs/SECURITY_AUDIT.md), [`docs/PERFORMANCE_ANALYSIS.md`](docs/PERFORMANCE_ANALYSIS.md), [`docs/DECISIONS.md`](docs/DECISIONS.md), [`docs/architecture/OVERVIEW.md`](docs/architecture/OVERVIEW.md), [`docs/adr/`](docs/adr/) 23 ADRs, [`docs/analysis/DEEP_DVB_AUDIT_v0.8.2.md`](docs/analysis/DEEP_DVB_AUDIT_v0.8.2.md) (DVB→Generic deep verification), `src/` 7 modules (framework bundler, pattern-guided, 1.0 stable), `tests/pattern-guided-revisit.test.js` + `tests/export-inference.test.js` + `tests/src-build.test.js` + `tsconfig.json` + `scripts/build.js` (`npm run verify:build` sha256 9b2b68… , 5,977 lines) · `eslint.config.js` + `.prettierrc` + `docs/ci/verify.yml.example` (lint+gate+typecheck+build).
 
A browser-based discovery engine inspired by the architecture of **DVB blind scanning**.
 
The project explores whether the fundamental pattern behind blind discovery in digital broadcasting can be generalized to other information-acquisition domains.
 
The prototype applies that pattern to web resources:
 `Candidate     ↓ Probe / Acquisition     ↓ Observation     ↓ Recognition     ↓ Discovery     ↓ Candidate Expansion     ↓ Scheduler     ↺ ` 
## Core Idea
 
A DVB blind scanner does not begin with complete knowledge of the available services.
 
It searches a parameter space, detects potentially interesting signals, attempts acquisition, validates what it receives, extracts metadata, and uses that metadata to discover additional resources.
 
This project generalizes that control pattern:
 `DVB Blind Scan              Generic Discovery  Frequency                   Candidate     ↓                           ↓ Signal detection             Probe     ↓                           ↓ Demodulator acquisition      Observation     ↓                           ↓ Transport validation         Recognition     ↓                           ↓ PSI/SI metadata              Metadata     ↓                           ↓ Network discovery            Candidate expansion ` 
The goal is **not** to implement a DVB receiver in JavaScript.
 
The goal is to investigate the **generic discovery algorithm underlying blind scanning**.
  
## Current Prototype
 
The current implementation is a Tampermonkey/Greasemonkey userscript.
 
It can:
 
 
- generate URL candidates
 
- maintain a priority queue
 
- concurrently acquire candidates
 
- prevent concurrent workers from claiming the same candidate
 
- record observations
 
- recognize different response types
 
- extract new candidates
 
- preserve candidate provenance
 
- deduplicate candidates
 
- persist discovery state
 
- export discovery results
 
- recursively expand the search space
 

 
Current response providers (v1.0.0 — 9 providers, ordered pipeline):
 `HTTP Response      │      ├── HTML Provider (links, scripts, stylesheets, frames, media, forms, meta, embedded URLs)      │      ├── JSON Provider (recursive URL-like string walk)      │      ├── XML Provider (sitemap <loc> via DOMParser + regex fallback)      │      ├── CSS Provider (url() extraction)      │      ├── JavaScript Provider (regex URL extraction)      │      ├── Binary Provider (observed-only: image/audio/video/pdf/zip)      │      └── Text Provider (fallback HTTP(S) URL regex) `  
## Architecture (v1.0.0 — modular prelude, provider-augmented, coverage observable, privacy-opt-in)

 `                     ┌─────────────────────┐                      │   Discovery Engine  │                      └──────────┬──────────┘                                 │                      ┌──────────▼──────────┐                      │      Scheduler      │                      └──────────┬──────────┘                                 │                      ┌──────────▼──────────┐                      │      Candidate      │  (type, target, depth, priority, hints, alternate*)                      └──────────┬──────────┘                                 │                      ┌──────────▼──────────┐                      │  AcquisitionPolicy│  (method, depth, type, binary, origin guards)                      └──────────┬──────────┘                                 │                      ┌──────────▼──────────┐                      │  AcquisitionPlan  │  (allowed + reason, replayable)                      └──────────┬──────────┘                                 │                      ┌──────────▼──────────┐                      │   OriginController│  (per-origin throttle 2 concurrent, 150ms)                      └──────────┬──────────┘                                 │                      ┌──────────▼──────────┐                      │    Acquisition    │  (GM_xhr + fetch fallback, 2M truncate)                      └──────────┬──────────┘                                 │                      ┌──────────▼──────────┐                      │     Observation   │  (status, http, fingerprint fnv1a32)                      └──────────┬──────────┘                                 │                      ┌──────────▼──────────┐                      │  Provider Registry│  (ordered matching → recognition)                      └──────────┬──────────┘                                 │           ┌─────────┼──────────┬──────────┼──────────┐                  ▼         ▼         ▼          ▼          ▼          ▼              HTML      JSON      XML        CSS       JS      Binary      Text                  │         │         │          │          │          │          │                  └─────────┴─────────┴──────────┴──────────┴──────────┴──────────┘                                 ▼                          ┌─────────────┐                          │  Discovery  │  (kind, confidence, mechanism, provenance)                          └──────┬──────┘                                 │                          New Candidates (depth+1, provenance→graphEdges)                                 │                                 └──────────► Scheduler                                 │                                  └────► ResourceRecord / DecisionLedger / Knowledge Graph`

> **v1.0.0 delta:** `package 1.0.0` + `header 1.0.0` + `CONFIG v8` unchanged — no runtime code, 22 ADRs 126/126 5977 lines 9b2b68… marks stable 1.0 (deep audit valid). **v0.9.1 delta:** `CONFIG.revisitChanged` + `CONFIG.patternGuided` + `KnowledgeBase.suggestPatternCandidates()`/`getChangedResources()` + `Engine` revisit (`revisit-queued`) + pattern-guided (`pattern-guided-queued`, 5 bounded, deterministic) + `tests/pattern-guided-revisit.test.js` (5 cases) + ADR 022. **v0.9.0 delta:** `src/` 7 modules → `dist` via `scripts/build.js` bundler (header.txt + config→utils→ledger→models→knowledge→providers→engine, 5875 lines 8c734…, deterministic), `src/` source of truth. **v0.8.2 delta:** `getCoverageMetrics()` sorted `queuedByType` + `patternCount`/`clusterCount`/`fingerprintUnique`/`inferenceEnabled` + `exportData().inference` (`patternMetrics`/`clusterMetrics`/`fingerprintStats`) + `verify:build` inference gate + `tests/export-inference.test.js` (6 cases) + ADR 020. **v0.8.1 delta:** `src/` 7-file mirror (`config.js`/`utils.js` extracts, 5 placeholders, `src/README.md` plan) + `scripts/build.js` `verify:build` src gate + header `@version 0.8.1` (5,784 lines, sha256 031c3…) + `tests/src-build.test.js` (6 cases) + ADR 019. **v0.8.0 delta:** `RobotsProvider`/`HeadersProvider` (Sitemap 0.92, Link 0.88/Location 0.90, 9 providers) + `http.headers` captured (fetch/GM_xhr) + `CONFIG.changeDetection` → `resource-changed` via `provider-robots-headers.test.js` (12 cases) + 3 ADRs (016-018) + `VERIFICATION_SUPPLEMENT_v0.8.0.md`. **v0.7.9 delta:** `CONFIG.inference` + `extractUrlPattern` + `patternIndex`/`clusterIndex` (7 cases) + `scripts/build.js` deterministic + 3 ADRs (013-015). **v0.7.8 delta:** `CONFIG.lifecycle` + `_validateTransition` + 4-worker `claim` exclusivity (6 cases) + `tsconfig`/`typecheck` + 3 ADRs (010-012). **v0.7.7 delta:** `CONFIG.candidateTTL` + `ttl-expired` + Ledger FIFO/Origin invariants (13 cases) + gate 85/75/80 + 3 ADRs (007-009). **v0.7.6 delta:** rAF-batched `updateUI` + `npm run coverage` 99% + 8 invariants. **v0.7.5 delta:** Trusted Types `gde-bridge` + JSDoc + `tests/fuzz-extract.test.js` + 3 ADRs + CI `docs/ci/verify.yml.example`. **v0.7.4 delta:** `CONFIG.privacy` scrub + `@connect self` + `csp-blocks-bridge` + ADR split 3 →6. **v0.7.3 delta:** `getCoverageMetrics()` frontier + `export.coverage`. See `VERIFICATION_REPORT.md` §2.2 and `CHANGELOG.md`.  
## Candidate Lifecycle
 
Candidates move through explicit ownership states:
 `QUEUED    │    ▼ CLAIMED    │    ├───────────────┐    ▼               ▼ COMPLETED        FAILED ` 
The critical invariant is:
 `A candidate may have at most one active owner. ` 
Candidate claiming is performed synchronously before asynchronous network acquisition:
 `worker   │   ├── claim candidate   │   └── await HTTP request ` 
This prevents multiple concurrent workers from selecting the same candidate.
  
## Discovery Model
 
The system distinguishes several concepts that are often incorrectly collapsed into one object.
 
### Candidate
 
Something the engine intends to investigate.
 `Candidate {     target     type     priority     origin     parent } ` 
### Observation
 
What acquisition actually produced.
 `Observation {     candidate     HTTP status     content type     body     errors } ` 
### Discovery
 
A validated interpretation of an observation.
 `Discovery {     kind     confidence     data     provenance } ` 
This separation allows the same candidate to have different observations over time and allows discoveries to retain evidence about how they were obtained.
  
## Provenance
 
Candidate generation is recorded.
 
For example:
 `initial page      │      ▼ HTML document      │      ├── link A      ├── link B      └── resource C              │              ▼         JSON response              │              └── URL D ` 
The resulting discovery graph can therefore answer:
 
 
Why did the engine investigate this resource?
 
 
rather than merely reporting:
 
 
This resource was found.
 
  
## Search Strategy
 
The prototype currently uses priority-based scheduling.
 
Conceptually:
 `priority(candidate) =     estimated_value     × estimated_probability     ÷ acquisition_cost ` 
The current implementation uses simpler heuristic priorities, but the architecture leaves room for more sophisticated search strategies.
 
Potential future strategies include:
 `Exhaustive Energy/Signal-inspired Priority-first Historical Metadata-guided Breadth-first Depth-first Adaptive Hybrid `  
## Generic Discovery Loop
 
The fundamental algorithm is:
 `initialize search space  while candidates remain:      candidate ← scheduler.claim()      observation ← acquire(candidate)      provider ← recognize(observation)      if provider accepts observation:          discovery ← provider.discover(observation)          store discovery          candidates ← provider.expand(discovery)          enqueue candidates      mark candidate complete ` 
The important operation is the feedback loop:
 `Observation     ↓ Discovery     ↓ New knowledge     ↓ New candidates ` 
This transforms discovery from a static list traversal into an **adaptive search process**.
  
## Scope
 
### This repository currently implements
 
 
- browser-side discovery
 
- URL candidate generation
 
- concurrent HTTP acquisition
 
- candidate ownership
 
- response recognition
 
- HTML discovery
 
- JSON discovery
 
- text discovery
 
- recursive candidate expansion
 
- provenance
 
- deduplication
 
- persistent state
 
- JSON export
 

 
### This repository does not currently implement
 
 
- RF spectrum scanning
 
- SDR hardware access
 
- DVB tuner control
 
- DVB-S/S2 demodulation
 
- DVB-T/T2 demodulation
 
- DVB-C demodulation
 
- carrier synchronization
 
- symbol-rate estimation
 
- FEC decoding
 
- MPEG transport-stream decoding
 
- DVB PSI/SI parsing
 
- NIT-based DVB discovery
 

 
Therefore:
 
 
**This is DVB-inspired, not DVB-compatible.**
 
 
The analogy concerns the **discovery architecture**, not the physical-layer implementation.
  
## Why DVB Blind Scan?
 
DVB blind scanning provides a useful model because the receiver begins with incomplete information.
 
It must:
 
 
1. search an unknown space
 
2. detect candidates
 
3. test hypotheses
 
4. validate observations
 
5. extract structured information
 
6. discover additional candidates
 
7. avoid duplicate work
 
8. continue until the search space is sufficiently covered
 

 
That pattern appears in many other domains.
 
Possible applications include:
 `Web discovery Document discovery Repository discovery API discovery Service discovery Network resource discovery Device discovery Knowledge-base acquisition Digital archive discovery ` 
The project investigates whether these can share a common discovery substrate.
  
## Design Principles
 
### 1. Discovery is not acquisition
 `Acquisition → produces observations  Recognition → interprets observations  Discovery → creates knowledge ` 
### 2. Candidates are hypotheses
 
A candidate means:
 
 
"This is worth investigating."
 
 
It does not mean:
 
 
"This resource exists."
 
 
### 3. Observations are evidence
 
A failed acquisition is still an observation.
 
### 4. Metadata expands the search space
 
Discovery is recursive.
 
### 5. Provenance matters
 
Every discovery should retain its origin.
 
### 6. Concurrency requires explicit ownership
 
Workers must claim work before performing asynchronous operations.
 
### 7. Providers should be replaceable
 
HTML, JSON, text, APIs, documents, and other protocols should not require rewriting the scheduler.
 
### 8. The search engine should remain protocol-independent
 
Protocol-specific knowledge belongs in providers/adapters.
  
## Roadmap
 
### Phase 0 — Prototype
 
 
- [x] candidate model
 
- [x] scheduler
 
- [x] concurrent acquisition
 
- [x] atomic candidate claiming
 
- [x] observation model
 
- [x] discovery model
 
- [x] provenance
 
- [x] HTML provider
 
- [x] JSON provider
 
- [x] text provider
 
- [x] persistent state
 
- [x] export
 

 
### Phase 1 — Discovery Core
 
> **Status in v0.7.4:** P2-6 (header/privacy/CSP) + P2-10 (ADR split) + tooling shipped; see `VERIFICATION_REPORT.md` §8 and `CHANGELOG.md`. P2-3 (coverage) shipped in 0.7.3.
 
- [x] formal provider interface (`Provider` base class + `ProviderRegistry` + 7 providers, ordered pipeline)
 
- [x] candidate fingerprints (`fnv1a32`, `makeFingerprint`, `fingerprintIndex` Map<hash,Set<url>>)
 
- [x] observation fingerprints (same, attached to `Observation.fingerprint`, indexed per `ResourceRecord`)
 
- [x] configurable retry policy (`CONFIG.retry {maxRetries:2, baseDelay:500, maxDelay:8000}` + exponential backoff, `nextAttemptAt`)
 
- [ ] candidate expiration (TTL beyond retry delay — not yet)
 
- [x] discovery confidence model (`Discovery.confidence` 0.40–0.95 per provider/mechanism + `effectivePriority` boost `confidence*0.08`)
 
- [ ] search-space coverage metrics (frontier size / coverage ratio not yet exposed)
 
- [x] event stream (`DecisionLedger` — 12 typed events, seq, FIFO 5,000, export/restore, replayable decisions)
 
- [x] structured logging (`ledger.recordDiagnostic`, `db.diagnostics` 500 cap, `network-observed`/`policy-denied`/`adaptive-*`)
 

 
### Phase 2 — Web Intelligence
 
- [ ] HTTP headers provider
 
- [x] XML provider (`XmlProvider` — `extractXmlLocs` DOMParser + regex fallback, sitemap-aware confidence 0.90)
 
- [x] RSS/Atom provider (covered via `XmlProvider` + `feed` type heuristic; `rel=alternate` → `feed`)
 
- [x] JavaScript resource provider (`JavaScriptProvider` — regex URL extraction)
 
- [x] sitemap provider (`XmlProvider` + `sitemap` type, `rel=sitemap` detection)
 
- [ ] robots.txt provider
 
- [x] API/JSON-LD provider (`JsonProvider` + `looksLikeApiUrl` → `kind:api` priority 1.00)
 
- [x] document-link provider (HTML `link[rel=canonical|manifest]` + `meta og:url` → `metadata-url` 0.90)
 
- [ ] URL pattern inference
 

 
### Phase 3 — Adaptive Search
 `Blind discovery       ↓ Observation       ↓ Inference       ↓ Candidate ranking       ↓ Guided discovery       ↓ New observations ` 
Status in v0.7.4 — partial:
 
- [x] adaptive priority (`effectivePriority = priority + typeWeight*0.20 + confidence*0.08 − depth*0.045 − attempts*0.05` + typePriority map + adaptive concurrency on success/failure thresholds)
 
- [ ] search-space partitioning
 
- [x] negative evidence (`Observation.status !== 'success'` → `retryCandidate` → `markFailed`, `markSkipped` with reason `resource-already-acquired`/`global-request-budget`)
 
- [ ] candidate clustering
 
- [x] historical knowledge (persistence `GM_setValue` v8, `visited` identityKey set, `fingerprintIndex`, `ResourceRecord` status)
 
- [ ] change detection
 
- [x] active exploration (`observeNetworkGet` + `PerformanceObserver` GET-like guard + DOM mutation observer with batch dedup)
 

 
### Phase 4 — Generic Acquisition Framework
 
Separate the browser implementation into:
 `Discovery Core      │      ├── Candidate Store      ├── Scheduler      ├── Evidence Store      ├── Provenance Graph      └── Discovery Graph  Acquisition Adapters      │      ├── HTTP      ├── Browser DOM      ├── Browser APIs      └── External sources  Recognition Providers      │      ├── HTML      ├── JSON      ├── XML      ├── Documents      └── Domain-specific protocols `  
## Non-Goals
 
This project is not intended to become:
 
 
- a general-purpose web crawler clone
 
- a browser automation framework
 
- an RF scanner implemented in JavaScript
 
- an unrestricted Internet crawler
 
- a replacement for specialized DVB software
 

 
The purpose is to investigate a **general discovery architecture**.
  
## Conceptual Formula
 
The project can be summarized as:
 
[ \boxed{ Candidate \rightarrow Observation \rightarrow Evidence \rightarrow Discovery \rightarrow Candidate\ Expansion } ]
 
Or more compactly:
 `SEARCH   ↓ PROBE   ↓ OBSERVE   ↓ RECOGNIZE   ↓ DISCOVER   ↓ EXPAND   ↺ ` 
DVB blind scanning is the motivating example.
 
The intended destination is a **generic, adaptive discovery engine**.
