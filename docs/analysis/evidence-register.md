# Evidence Register

Audit index for every non-trivial finding in
[repository-analysis-2026-09-10.md](repository-analysis-2026-09-10.md). It is an
index, not a bibliography: each row supports a specific claim, and the claim
should not be asserted anywhere in this repository without its ID.

## Repository access contract

| | |
| --- | --- |
| Repository | `Abdus2023/Generic-Discovery-Engine` |
| Owner / name | `Abdus2023` / `Generic-Discovery-Engine` |
| Requested branch | `main` (as supplied by the user) |
| Resolved branch | local `main` @ `cc8df73`, work branch `arena/01a08d14-generic-discovery-engine` |
| Resolved commit at analysis start | `cc8df7357c2dbfe9d149747743e2f5e9ac9c0178` |
| Access method | local git checkout, full read/write, `git`, `node`, `gh` |
| Accessible scope | the entire repository tree at the resolved commit: all files, no submodules, no LFS, no private dependencies |
| Unavailable scope | none — no test directory, CI configuration, issue tracker content or external artifact exists to inspect |
| Access classification | **FULL ACCESS** (single-repository scope, no remote-only artifacts) |

Access verification:

| Check | Result |
| --- | --- |
| repository exists | yes |
| requested repository is the correct repository | yes — tree contains the two named documents |
| requested branch exists | yes (`main`) |
| repository tree can be inspected | yes — 3 files at the resolved commit |
| source files can be inspected | yes — one implementation artifact, extracted and read in full |
| tests can be inspected | **no tests exist** (ABSENCE_VERIFIED, EVID:SCOPE-005) |
| requested documentation can be inspected | yes — both named documents |
| relevant history can be inspected | yes — single commit; no earlier history to inspect |

Analysis target for every code locator below:
`prototype/generic-discovery-engine.user.js` at the artifact extracted verbatim
from `archive/Continue Architecture Planning.md` L48948–L54113; file identity is
asserted by `tools/verify.mjs` (parse + version + symbol checks).

## Citation format

```
[EVID:CONC-001]
path:      prototype/generic-discovery-engine.user.js
locator:   L1088-L1119 (KnowledgeBase.claimNextCandidate)
type:      code
status:    implemented
```

Locators prefer line ranges of the current artifact; semantic locators
(`Class.method`, `"heading"`) are used where line numbers would be misleading.

## Evidence quality

| Quality | Meaning | Examples in this repository |
| --- | --- | --- |
| DIRECT | executable behaviour or the code that produces it | artifact source, `tools/checks.mjs`, `tools/simulate.mjs` results |
| CORROBORATED | several independent sources agree | code + executed behaviour + documentation |
| INDIRECT | documentation or configuration describing behaviour | README, design series |
| WEAK | historical or conversational material | `archive/Continue Architecture Planning.md` |
| UNVERIFIED | asserted without a source in scope | anything not listed here |

Preferred hierarchy applied throughout: executable behaviour → automated check →
interface → configuration → current documentation → historical documentation →
reasoning.

## Register — code

| ID | Path | Locator | Supports | Quality | Status |
| --- | --- | --- | --- | --- | --- |
| CODE-001 | `prototype/generic-discovery-engine.user.js` | header, L1–L17 (`@version 0.7.1`, grants) | artifact identity and version; userscript runtime surface | DIRECT | implemented |
| CODE-002 | same | L49–L135 (`CONFIG`, including `maxCandidates`, `maxRequests`, `maxDepth`, `adaptive`, `retry`) | limits, budget, adaptive and retry configuration | DIRECT | implemented |
| CODE-003 | same | L686–L788 (`Candidate`) | candidate fields; `identityKey()` L750; `effectivePriority()` L753 | DIRECT | implemented |
| CODE-004 | same | L789–L853 (`Observation`) | observation fields incl. status, HTTP metadata, truncation | DIRECT | implemented |
| CODE-005 | same | L854–L893 (`Discovery`) | discovery fields: candidateId, observationId, kind, confidence, mechanism, provenance | DIRECT | implemented |
| CODE-006 | same | L975–L1417 (`KnowledgeBase`) | stores, caps, graph edges, diagnostics, statistics | DIRECT | implemented |
| CODE-007 | same | L1002–L1073 (`KnowledgeBase.addCandidate`) | dedup by `identityKey`, merge of `alternate*`, max priority, candidate cap | DIRECT | implemented |
| CODE-008 | same | L1074–L1087 (`KnowledgeBase.queueCandidate`) | **only `completed`/`skipped` are refused** | DIRECT | contradicted (see CONC-003) |
| CODE-009 | same | L1088–L1119 (`KnowledgeBase.claimNextCandidate`) | synchronous claim; marks `claimed` before returning; accepts `queued` and `failed` | DIRECT | implemented |
| CODE-010 | same | L1143–L1148 / L1149–L1160 / L1161–L1165 (`markCompleted` / `markSkipped` / `markFailed`) | terminal states; `markFailed` sets no backoff | DIRECT | implemented |
| CODE-011 | same | L1166–L1190 (`KnowledgeBase.retryCandidate`) | retry budget, exponential backoff into `nextAttemptAt` | DIRECT | implemented |
| CODE-012 | same | L1303–L1310 (`shouldAcquireResource`) | per-URL acquisition guard keyed on canonical URL + resource status | DIRECT | implemented |
| CODE-013 | same | L1621–L1968 (`Acquisition`), incl. `execute` L1626, `request` L1666 | HTTP GET via `GM_xmlhttpRequest`, `fetch` fallback, 8 s timeout, body truncation | DIRECT | implemented |
| CODE-014 | same | L1969–L1984 (`Provider`), L1985–L2669 (seven providers), L2670–L2703 (`ProviderRegistry`) | provider contract `matches()`/`recognize()`; registry completeness | DIRECT | implemented |
| CODE-015 | same | L1973–L1981 (`Provider.matches`/`recognize` stubs) | there is **no** `candidates()` method: expansion is engine-owned | DIRECT | implemented |
| CODE-016 | same | L214–L281 (`looksLikeHtml`/`looksLikeJson`/`looksLikeXml`), L2450–L2578 (CSS/JS providers), L2579–L2645 (`TextProvider.matches`) | content-type **and body-sniff** matching; `TextProvider` = `text/*` or empty | DIRECT | implemented |
| CODE-017 | same | L284–L341 (`extractUrlsFromText`, `extractCssUrls`, `extractXmlLocs`) | absolute **and relative** URL extraction rules | DIRECT | implemented |
| CODE-018 | same | L3114–L4291 (`GenericDiscoveryEngine`), incl. `worker()` L3540, `start()` L3594 | worker pool creation, claim-before-await ordering, `Promise.all` | DIRECT | implemented |
| CODE-019 | same | L3354–L3610 (`executePlan` L3362 onward) | policy denial, budget reservation, observation, retry, recognition, expansion, completion | DIRECT | implemented |
| CODE-020 | same | L3347–L3353 (`reserveRequestSlot`) | global request budget, slot never released | DIRECT | implemented |
| CODE-021 | same | L3262–L3330 (`emitDiscovery`) | a `Discovery` is stored **before** the derived candidate is deduplicated | DIRECT | implemented |
| CODE-022 | same | L344–L356 (`makeFingerprint`), L986 (`fingerprintIndex`) | content fingerprints computed and indexed | DIRECT | implemented |
| CODE-023 | same | L986, L1216–L1227, L1397–L1408 (`fingerprintIndex` sites) | the index is written/probed, **never read** → D8 | DIRECT | contradicted |
| CODE-024 | same | L441–L685 (`DecisionLedger`) incl. `append` cap, `export`/`restore` | sequenced append-only ledger, capped at 5000, persisted | DIRECT | implemented |
| CODE-025 | same | L3975–L4002 (`persist`), L4003–L4067 (`restore`) | persistence payload, v6→v7 migration, ledger restore, budget reset | DIRECT | implemented |
| CODE-026 | same | L4068–L4090 (`exportData`) | export schema `gde-export-v7.1` | DIRECT | implemented |
| CODE-027 | same | L3838–L3893 (`observeCurrentPage`), L3895–L3950 (`observeCurrentDom`), L3792–L3836 (`observeNetworkGet`) | seed generation and its mechanisms | DIRECT | implemented |
| CODE-028 | same | L2704–L3113 (`NetworkObserver`), incl. `installBridge` L2724, `installPerformanceObserver` L3016 | page fetch/XHR bridge; performance entries treated as evidence only | DIRECT | implemented |
| CODE-029 | same | L4241–L4285 (`updateUI`) | UI exposes `currentConcurrency`, `activeWorkers`, dead `acquired` counter | DIRECT | implemented |
| CODE-030 | same | `stat = { …, acquired: 0 }` L1006–L1018 and no assignment anywhere | `stats.acquired` is never incremented → D7 | DIRECT | contradicted |
| CODE-031 | same | L1419–L1420 (`plan(candidate)` in `AcquisitionPolicy` and engine) | policy decides GET-only, depth, disabled classes, scope | DIRECT | implemented |
| CODE-032 | same | L191–L213 (`isAllowedUrl`, `sameOriginOnly`) | scope gate is the current origin | DIRECT | implemented |

## Register — behaviour (executed)

| ID | Path | Locator | Supports | Quality | Status |
| --- | --- | --- | --- | --- | --- |
| TEST-001 | `tools/verify.mjs` | checks `claimNextCandidate() is synchronous`, `ownership is handed straight to execution` | claim-before-await atomicity | DIRECT | tested |
| TEST-002 | `tools/verify.mjs` | checks `providers perform no network I/O`, registry completeness, `TextProvider scope` | provider boundary and matching rules | DIRECT | tested |
| TEST-003 | `tools/verify.mjs` | checks `no DVB/RF implementation symbols`, `no later-design layers present` | non-goals and design/implementation separation | DIRECT | tested |
| TEST-004 | `tools/checks.mjs` | case 1 (duplicate insertion) | candidate identity dedup by `type:target` | DIRECT | tested |
| TEST-005 | `tools/checks.mjs` | case 2 (type disambiguation) | same URL with different type ⇒ distinct candidates | DIRECT | tested |
| TEST-006 | `tools/checks.mjs` | case 3 (11 content-type/body cases, exact sets) | provider selection incl. double-match and body sniffing | DIRECT | tested |
| TEST-007 | `tools/checks.mjs` | case 4 (chain reconstruction) | seed → candidate → observation → discovery → child candidate | DIRECT | tested |
| TEST-008 | `tools/checks.mjs` | case 5 (round-trip) | candidates, discoveries, resources **and ledger** survive restore; budget resets | DIRECT | tested |
| TEST-009 | `tools/simulate.mjs` | checks `single owner per candidate`, `no duplicate acquisition` | **violation of the single-owner invariant** (D1) | DIRECT | contradicted |
| TEST-010 | `tools/simulate.mjs` | `peakActiveWorkers`, `pendingWorkAtQuiescence` | pool never refilled (D2); work stranded on backoff (D4) | DIRECT | contradicted |
| TEST-011 | `tools/simulate.mjs` | anomaly stream `CONCURRENT_OWNER` | two workers acquiring one candidate at the same time | DIRECT | contradicted |
| TEST-012 | `tools/simulate.mjs` | metrics `discoveries` vs `uniqueUrls` (74 / 27) | discovery records are not deduplicated (D9) | DIRECT | contradicted |
| TEST-013 | `tools/simulate.mjs` | `--unsafe-control` run | the harness detects an ownership violation (detector sensitivity) | DIRECT | tested |

## Register — documentation

| ID | Path | Locator | Supports | Quality | Status |
| --- | --- | --- | --- | --- | --- |
| DOC-001 | `README.md` (pre-cleanup, at `cc8df73`) | "Current Prototype", "Candidate Lifecycle" | historical README claims: atomic claiming, concurrency, persistence | WEAK | historical (superseded) |
| DOC-002 | `archive/Continue Architecture Planning.md` | L48914–L48944 ("1. New invariant", "Complete v0.7.1") | design intent for the decision boundary and ledger | INDIRECT | specified |
| DOC-003 | `archive/Continue Architecture Planning.md` | L54117–L54580 ("What v0.7.1 actually changes" … "Architecture after v0.7.1") | v0.7.1 contract: candidate ≠ acquisition plan, provider separation | INDIRECT | specified |
| DOC-004 | `archive/Continue Architecture Planning.md` | L54418–L54472 ("6. One remaining architectural limitation") | replay vs acquisition distinction | INDIRECT | specified |
| DOC-005 | `archive/Continue Architecture Planning.md` | L90113–L90153, L91859–L91906 ("What the browser prototype can guarantee", "Prototype Boundary") | profile coordination ≠ distributed consensus | INDIRECT | specified |
| DOC-006 | `archive/Continue Architecture Planning.md` | v0.8 … v0.35 headings (L54631 onwards) | design-only layers with no implementation | INDIRECT | planned |
| DOC-007 | `archive/Userscript Discovery Prototype.md` | notes 1–41 | origin of the DVB analogy and the coarse-to-fine/confidence ideas | WEAK | historical |
| DOC-008 | `docs/prototype/limitations.md` | "Known defects" table | D1–D9 definitions with evidence pointers | DIRECT | implemented (index) |
| DOC-009 | `docs/prototype/scope.md` | "Implemented / Partially implemented / Not implemented" | scope tiers and their verification | DIRECT | implemented (index) |
| DOC-010 | `docs/architecture/search-space.md` | whole document | bounds, termination, coverage, staleness | DIRECT | implemented (index) |
| DOC-011 | `docs/glossary.md` | "Canonical definitions" | one term per concept; conflict table | DIRECT | implemented (index) |
| DOC-012 | `docs/analysis/change-register-2026-09-10.md` | change IDs R-001… | what was changed, why, and how it was verified | DIRECT | implemented (index) |

## Register — negative evidence

Absence is recorded only where the inspection scope justifies it. The
implementation is a **single 4,290-line file** that was read in full and scanned
mechanically, so absence claims inside it are `ABSENCE_VERIFIED`; absence claims
about artifacts that do not exist in the repository are `NOT_FOUND`.

| ID | Claim | Method | Verdict | Evidence |
| --- | --- | --- | --- | --- |
| SCOPE-001 | No DVB/RF implementation (spectrum, tuner, demodulator, FEC, transport stream, PSI/SI) | full read + symbol scan (`tools/verify.mjs`) | **ABSENCE_VERIFIED** | TEST-003, CODE-001, CODE-002 |
| SCOPE-002 | No v0.8+ design layer is implemented (capabilities, work items, evidence graph, leases, coverage, fencing) | symbol scan over the whole artifact | **ABSENCE_VERIFIED** | TEST-003, DOC-006 |
| SCOPE-003 | Acquisition transport is HTTP-only | provider/transport interfaces inspected; only `GM_xmlhttpRequest` and `fetch` appear | **ABSENCE_VERIFIED** | CODE-013, CODE-015 |
| SCOPE-004 | No cross-context claim or lease mechanism | ownership state is per-engine-instance (`KnowledgeBase.claimed`, candidate status) | **ABSENCE_VERIFIED** | CODE-009, CODE-025, DOC-005 |
| SCOPE-005 | No tests, CI configuration or build tooling existed in the repository | tree inspection at the resolved commit | **ABSENCE_VERIFIED** | access contract above |
| SCOPE-006 | No coverage, absence or completeness object exists | no such symbol; termination is an empty eligible set | **ABSENCE_VERIFIED** | CODE-009, DOC-010 |
| SCOPE-007 | No non-URL candidate target is implemented | every `discover()` call passes a URL; target type list is URL-oriented | **ABSENCE_VERIFIED** | CODE-003, CODE-027 |

## Register — contradictions

| ID | Claim A | Claim B | Evidence | Status |
| --- | --- | --- | --- | --- |
| CONC-001 | claim operation is atomic | — | CODE-009, TEST-001 | implemented |
| CONC-002 | "a candidate may have at most one active owner" | re-discovery re-queues in-flight candidates | CODE-008, CODE-021, TEST-009, TEST-011 | **contradicted (D1)** |
| CONC-003 | worker pool provides configured concurrency | workers exit permanently on an empty frontier | CODE-018, TEST-010 | **contradicted (D2)** |
| CONC-004 | retry is bounded by backoff | `failed` is claimable with no backoff | CODE-009, CODE-010, CODE-011 | **contradicted (D3)** |
| PROV-001 | derivation chain seed → candidate → observation → discovery | — | CODE-005, TEST-007 | implemented |
| PROV-002 | content identity is modelled by fingerprints | index is never read | CODE-022, CODE-023 | **contradicted (D8)** |
| PROV-003 | discoveries represent distinct findings | records are not deduplicated | CODE-021, TEST-012 | **contradicted (D9)** |
| FAIL-001 | HTTP failure ends a candidate's life | `failed` returns to the claimable pool | CODE-010, CODE-011 | **contradicted (D3)** |
| ARCH-001 | "persistent state" | no transaction, validation or in-flight reconciliation | CODE-025, TEST-008 | partially supported |
| ARCH-002 | "protocol-independent providers" | only recognition is an interface | CODE-015, SCOPE-003 | partially supported |

## Register — configuration

| ID | Path | Locator | Supports | Quality | Status |
| --- | --- | --- | --- | --- | --- |
| CFG-001 | artifact | L49–L135 (`CONFIG` limits and policy switches) | budget, caps, depth, origin and adaptive settings | DIRECT | implemented |
| CFG-002 | artifact | L134 (`STORAGE_KEY = 'generic-discovery-engine-v7'`) | persistence key and schema generation | DIRECT | implemented |

## Multi-source evidence summary

| Claim | Sources | Relationship |
| --- | --- | --- |
| Claiming is synchronous and precedes any `await` | CODE-009, CODE-018, TEST-001 | **CONFIRMED** |
| Provider boundary is clean | CODE-014, CODE-015, TEST-002 | **CONFIRMED** |
| The single-owner invariant is violated end to end | CODE-008, CODE-021, TEST-009, TEST-011 | **CORROBORATED** (static + dynamic) |
| Content fingerprints are dead evidence | CODE-022, CODE-023 | **CONFIRMED** (static) |
| Discovery records are not deduplicated | CODE-021, TEST-012 | **CORROBORATED** |
| Persistence round-trips state and ledger | CODE-025, TEST-008 | **CONFIRMED** |
| No DVB/RF implementation exists | SCOPE-001, TEST-003 | **ABSENCE_VERIFIED** |
| Worker pool never refills | CODE-018, TEST-010 | **CORROBORATED** |
| Adaptive concurrency has no live effect | CODE-018, CODE-029 | **CONFIRMED** (static) |
| Retrospective documentation claims (pre-cleanup README) describe the system accurately | DOC-001 vs CODE-008, TEST-009 | **CONTRADICTED** — documentation evidence was overridden by direct implementation evidence, as required |

## How to use this register

1. Any claim added to `docs/` must cite at least one ID from this file.
2. A claim whose citation is `WEAK` or `INDIRECT` must be labelled
   SPECIFIED/PLANNED/HISTORICAL, never IMPLEMENTED.
3. New evidence gets a new ID; IDs are never reused for unrelated evidence.
4. `tools/verify.mjs` fails if a document cites an ID that does not exist here,
   or if a register row points at a path that is not in the repository.
