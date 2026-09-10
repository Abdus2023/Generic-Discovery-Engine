# Repository Analysis — 2026-09-10

Deep structural review of `Abdus2023/Generic-Discovery-Engine` at commit
`cc8df73` ("Add files via upload"), performed before and during the
documentation cleanup. Output order follows the review brief (Phases 0–21).

---

## 1. Repository Verification

| | |
| --- | --- |
| Repository | `Abdus2023/Generic-Discovery-Engine` |
| Branch reviewed | `main` @ `cc8df73` (workspace: `arena/01a08d14-generic-discovery-engine`) |
| Files at review time | 3 — `README.md`, `Userscript Discovery Prototype.md`, `Continue Architecture Planning.md` |
| Implementation artifacts | **1** — the v0.7.1 userscript, embedded in the planning transcript (lines 48948–54113) |
| Documentation artifacts | 3 — the README plus two unedited chat transcripts |
| Tests / CI / configuration | none |
| Executable code outside the transcript | none |

### Inventory

| File | Type | Purpose | Status | Dependencies | Disposition |
| --- | --- | --- | --- | --- | --- |
| `README.md` (396 lines) | README / documentation | project pitch, architecture sketch, roadmap, scope list | active, partly aspirational | none | **KEEP**, rewritten against verified behaviour |
| `Userscript Discovery Prototype.md` (4,805 lines) | design exploration + historical reasoning | 41 notes: DVB blind scan as generic algorithm; conceptual pipeline; v0.1.0/v0.2.0 pastes | historical, non-normative; contains broken code | none | **ARCHIVE**, extract DVB analogy into `docs/research/` |
| `Continue Architecture Planning.md` (92,274 lines) | implementation log + design series | 10 fenced userscripts (v0.3.0 … v0.7.1) + prose design series v0.8 … v0.35 | mixed: 1 valid current artifact, 1 invalid artifact, ~1.5 MB prose-only design | none | **SPLIT**: code → `prototype/`, design series → `docs/roadmap/`, remainder → `archive/` |
| v0.7.1 userscript (embedded) | prototype | working discovery engine | **current and verified** | browser + userscript manager | **EXTRACT** to `prototype/generic-discovery-engine.user.js` |

### Classification of the material

* normative architecture: none existed before this cleanup
* implementation specification: partial (transcript sections that describe v0.7.1)
* prototype: v0.7.1 (and v0.3.0 – v0.6.0, superseded)
* experiment: none recorded
* research note: DVB blind-scan analogy (`Userscript Discovery Prototype.md`)
* design exploration: v0.8 … v0.35 (planning transcript)
* historical reasoning: version-by-version "what changed" sections
* roadmap: the "Phase 0–4" list in the README + version series
* obsolete material: v0.1.0/v0.2.0 pastes (invalid), the invalid v0.5.0 paste

### Verification performed

* every fenced userscript block was extracted and parsed with `node --check`:
  **9 of 10 parse**, the v0.5.0 paste at transcript lines 18378–23093 does not
  (`await` outside an async function);
* the v0.7.1 block was extracted verbatim and re-parsed (`vm.Script`) — see
  `tools/verify.mjs`;
* the artifact was executed under a browser shim to observe runtime behaviour —
  see `tools/simulate.mjs`;
* README claims were checked one by one against the artifact; results appear in
  sections 3, 5 and 7.

---

## 2. Executive Findings

1. The repository contained **one real implementation** — the v0.7.1 userscript —
   buried inside a 92k-line chat transcript, and **no repository file that
   described it accurately**.
2. Everything from v0.8 to v0.35 is **design prose with no code**; the README and
   the transcript's conclusion read as if that architecture were the project.
3. The prototype is genuinely layered: candidates, scheduler, acquisition,
   recognition providers, knowledge base, decision ledger, persistence, export.
4. The provider boundary is **clean and verified**: providers perform no I/O,
   never enqueue candidates, never touch scheduling — the strongest part of the
   design.
5. The claim operation is synchronous and marks ownership before any `await`;
   within one execution context two workers cannot claim the same candidate *via
   the claim function*.
6. However, the stated invariant "a candidate may have at most one active owner"
   is **violated end to end**: re-discovery re-queues an in-flight candidate
   (`queueCandidate()` refuses only `completed`/`skipped`), producing 2–4
   concurrent owners and 12–18 duplicate acquisitions per harness run (**D1**).
7. Workers exit permanently when no candidate is eligible at that instant, so
   effective concurrency collapses toward 1 and work waiting on retry backoff is
   abandoned while `running` stays true and the Scan button becomes a no-op
   (**D2**, **D4**).
8. `failed` is a claimable state with no backoff, so a permanently broken target
   can consume the request budget (**D3**).
9. Adaptive concurrency updates a variable that the already-created worker pool
   never reads, and `stats.acquired` is never incremented (**D5**, **D7**).
10. Terminology drifted badly: *probe*, *acquisition*, *lock*, *validation*,
    *evidence*, *visited*, *database*, *graph*, *coverage* were used
    inconsistently; the canonical glossary now fixes one term per concept.
11. The README mixed implemented, designed and aspirational statements with no
    labels, and its roadmap marked the whole prototype phase as complete.
12. The DVB analogy is legitimate as an explanation of control structure and was
    at risk of being read as a compatibility claim; it is now bounded explicitly.
13. Provenance exists in a usable but partial form (parent, mechanism, depth,
    ledger, graph edges); the design series' evidence/claim layer does not exist.
14. Failure modes were undocumented; 26 are now recorded with detection, current
    behaviour, desired behaviour and status, alongside 7 named defects (D1–D7).
15. The repository now holds the code, the documents, the archive and two
    executable verification tools; static verification exits non-zero when
    documentation and code disagree.

---

## 3. Architecture Truth Table

| Area | Implemented | Designed | Future | Problem |
| --- | --- | --- | --- | --- |
| Candidate representation | yes (`Candidate`, `identityKey`, `effectivePriority`) | fingerprints, requirements | — | priority formula is heuristic, not the documented value/cost model |
| Candidate lifecycle | yes (11 states) | work-item lifecycle | — | `failed` is claimable, no terminal state |
| Candidate claiming | yes (synchronous) | leases, fencing (v0.33) | — | violated end-to-end by the re-queue path (D1) |
| Scheduler | yes (scan + sort, budget, origin limits) | aging, fairness, arbitration | admission scheduling | O(n log n) per claim; no fairness; worker pool not refilled (D2) |
| HTTP acquisition | yes (GM XHR / fetch, 8 s timeout, truncation) | acquisition runtime, capability lattice | replay provider, cache provider | transport is hard-wired; no cancellation |
| Response recognition | yes (7 providers, `matches`/`recognize`) | response router, provider priority, recognition evidence | — | multiple providers may match; confidence not comparable |
| Candidate sources | yes (page, DOM, network bridge, performance) | `CandidateSource` interface, discovery controller | non-HTTP sources | engine-internal; performance entries are evidence-only by design |
| Candidate expansion | yes (engine-owned, depth-bounded) | frontier/arbitration | — | re-queues in-flight candidates (D1) |
| Deduplication | yes (type:target; resource URL guard) | reconciliation, identity resolution | artifact/revision identity | guard is non-atomic across the in-flight window (D6) |
| Persistence | yes (GM storage, caps, debounced) | transactional persistence, crash recovery | cross-context replication | no transactions; `running` latch survives restore |
| Provenance | partial (parent, mechanism, depth, ledger, edges) | evidence graph, claims, conflicts | causal ordering | no evidence layer; observations are mutable |
| Concurrency | single-context claim | multi-worker coordination | distributed consensus | invariant violation (D1); not a lock |
| Coverage / absence / completeness | no | v0.22, v0.23 | goal-constrained coverage | none of it exists; must not be claimed |
| Adaptive strategy | counters only | v0.21 learning | — | no effect on the live pool (D5) |
| DVB/physical layer | no | — | — | non-goal; enforced by a static check |

---

## 4. Terminology Audit

| Current term(s) | Canonical term | Problem | Action |
| --- | --- | --- | --- |
| probe, acquire, fetch, validate | **Acquisition** | four words for one operation | fixed in `docs/glossary.md`; *probe* reserved for the designed capability-aware attempt |
| lock, validation, detection, recognition | **Recognition** | "lock" imported DVB physics into an HTTP context; "validation" implied truth judgement | recognise only; DVB boundary documented |
| visited / completed / acquired | **status = completed** | "visited" is bookkeeping, not state | lifecycle is canonical |
| evidence (for observations) | **Observation** | design vocabulary used for current behaviour | evidence reserved for the DESIGNED v0.16 layer |
| database, knowledge graph, discovery graph | **Knowledge base** | implied durability and queryability that do not exist | one term, one object |
| priority, confidence, score, strength | **priority** (scheduling), **confidence** (belief) | conflated numeric fields | split and defined |
| coverage, completeness, exhaustion | **Coverage** (DESIGNED), **Exhaustion** (OPEN) | "exhausted" used for "empty eligible set" | terminology separated; claims forbidden today |
| claim (ownership) vs claim (assertion) | **claim** (ownership), **assertion** (designed) | one word, two concepts | naming hazard documented |
| sweep, crawl, scan | **Scan** | "crawl" contradicts a stated non-goal | one term |
| unknown target types | **candidate type** | type list exists but only URL targets are implemented | documented per type |

---

## 5. Contradictions

**CONFLICT 1 — implementation status of the architecture**
*Statement A:* the README roadmap marks "Phase 0 — Prototype" complete for
candidate model, scheduler, concurrency, provenance, providers, persistence, and
the transcript's conclusion describes the prototype as "evidence-driven,
coverage-aware, concurrency-safe, conflict-aware".
*Statement B:* the only code in the repository implements none of the evidence,
coverage, conflict or capability layers, and the last code version is v0.7.1.
*Evidence:* transcript has no userscript after line 54113; `tools/verify.mjs`
confirms the artifact contains none of the later-design symbols.
*Resolution:* implemented/designed/future labels; roadmap rewritten; the
conclusion's framing reclassified as DESIGNED.
*Documents changed:* `README.md`, `docs/roadmap/future-architecture.md`,
`docs/prototype/userscript.md`.

**CONFLICT 2 — "at most one active owner"**
*Statement A:* README and design-series invariants state a candidate has at most
one active owner.
*Statement B:* `queueCandidate()` re-queues candidates in `claimed`, `planned`,
`acquiring` or `observed` states; the harness measured 2–4 concurrent owners and
duplicate acquisitions of the same URL.
*Evidence:* static (claim filter vs re-queue path) and dynamic
(`tools/simulate.mjs`).
*Resolution:* the *claim operation* is atomic; the *end-to-end invariant* is
violated. Both statements are now written precisely and the defect is tracked as
D1.
*Documents changed:* `README.md`, `docs/architecture/concurrency.md`,
`docs/prototype/limitations.md`.

**CONFLICT 3 — "concurrent acquisition"**
*Statement A:* README lists "concurrently acquire candidates" and the UI shows
`concurrency=4`.
*Statement B:* a worker that finds no eligible candidate exits permanently, so
scans often run with one live worker; measured peak live workers is 1 without a
pre-populated frontier.
*Evidence:* harness measurement of `activeWorkers`.
*Resolution:* concurrency is configured, not guaranteed; documented as D2.
*Documents changed:* `docs/architecture/scheduler.md`,
`docs/prototype/limitations.md`.

**CONFLICT 4 — "persistent state"**
*Statement A:* README claims persistent state; the userscript stores state via
`GM_setValue`.
*Statement B:* there is no transaction, no consistency check and no recovery;
candidate statuses in flight are persisted as if they were facts.
*Evidence:* `persist()` serializes current state; no journal or validation.
*Resolution:* "durable-ish snapshot with caps", not persistence with guarantees.
*Documents changed:* `docs/architecture/discovery-model.md` (missing contracts),
`docs/prototype/scope.md`.

**CONFLICT 5 — "protocol-independent / provider architecture"**
*Statement A:* README and design series present the engine as
protocol-independent with replaceable providers.
*Statement B:* only *recognition* is a provider interface; acquisition is
hard-wired to HTTP GET and candidate sources are engine methods.
*Evidence:* no `AcquisitionProvider` or `CandidateSource` symbol exists in the
artifact; `tools/verify.mjs` documents the provider contract as
`matches()` + `recognize()` only.
*Resolution:* scope narrowed to "recognition providers are replaceable";
acquisition and source planes are DESIGNED.
*Documents changed:* `docs/architecture/provider-model.md`,
`docs/prototype/scope.md`.

**CONFLICT 6 — "generic discovery" vs URL-only behaviour**
*Statement A:* the project is a *generic* discovery architecture.
*Statement B:* every implemented candidate target is a URL; classification,
relevance and non-HTTP transports do not exist.
*Evidence:* `Candidate.target` is always a URL; scope gate is origin-based.
*Resolution:* "generic in control structure, URL-only in implementation",
stated explicitly.
*Documents changed:* `README.md`, `docs/architecture/candidate-model.md`.

**CONFLICT 7 — confidence**
*Statement A:* the README describes a discovery confidence model and the design
series treats confidence as an architectural primitive.
*Statement B:* confidence is a provider-local constant propagated into a
scheduling weight; there is no calibration, aggregation or comparison rule.
*Evidence:* `HtmlProvider` emits 0.7, network observations 0.70, page seed 1.0.
*Resolution:* marked as OPEN; confidence is not comparable across providers.

**CONFLICT 8 — DVB compatibility risk**
*Statement A:* the repository is "DVB-blind-scan-inspired".
*Statement B:* no DVB symbol, table or physical-layer concept exists in the code.
*Evidence:* static symbol check passes.
*Resolution:* "inspiration only", with a canonical analogy matrix and explicit
non-claim statements.
*Documents changed:* `docs/research/dvb-blind-scan-inspiration.md`,
`README.md`, `docs/prototype/scope.md`.

---

## 6. Duplication Map

| Concept | Occurrences before cleanup | Canonical location now |
| --- | --- | --- |
| DVB analogy | README (4 sections), transcript (repeated per version) | `docs/research/dvb-blind-scan-inspiration.md` |
| generic discovery loop | README (3 diagrams), each design version, transcript conclusion | `docs/architecture/discovery-model.md` (one diagram) |
| candidate lifecycle | README, transcript v0.7, v0.15, v0.33 | `docs/glossary.md` + `docs/architecture/candidate-model.md` |
| provider architecture | README, transcript v0.9/v0.11 | `docs/architecture/provider-model.md` |
| concurrency explanation | README, transcript v0.33/v0.34 | `docs/architecture/concurrency.md` |
| scope limitations | README, transcript conclusion | `docs/prototype/scope.md` |
| roadmap | README "Phase 0–4", transcript v0.8…v0.35, conclusion | `docs/roadmap/future-architecture.md` |
| provenance | README, transcript v0.16, v0.28 | `docs/architecture/provenance.md` |
| scheduler behaviour | README, transcript v0.10/v0.15/v0.30 | `docs/architecture/scheduler.md` |

Rule applied: each concept is explained once; other documents link to it.

---

## 7. Scope Verification

**CURRENT** (verified against the artifact): seed generation; candidate
normalization; identity deduplication; resource-level acquisition guard;
synchronous candidate claiming; worker pool; HTTP GET acquisition with timeout;
content-type handling and sniffing; HTML/JSON/XML/CSS/JS/text/binary
recognition; URL and resource extraction; candidate expansion with depth and
candidate caps; persistence with caps; JSON export; control panel; per-provider
error isolation; request budget; origin rate limiting; retry with backoff;
decision ledger; graph edges; policy gating (GET-only, depth, disabled classes,
scope).

**DESIGNED**: capability lattice, acquisition runtime, recognition runtime,
candidate sources and controller, discovery domain and sessions, work items and
frontier arbitration, evidence graph, resource identity resolution,
classification axes, representations/artifacts/revisions, partitioning,
adaptive strategies, coverage, absence, goal-constrained discovery, query
planner, tactics, enumeration, reconciliation, cost ledger, transactional
persistence, multi-worker coordination, conflict resolution, replication.

**FUTURE**: learned priority, cross-domain discovery, non-HTTP transports,
completeness claims.

**NON-GOAL**: RF spectrum scanning; SDR and tuner control; DVB-S/S2, DVB-T/T2,
DVB-C demodulation; carrier synchronization; symbol-rate estimation; FEC
decoding; MPEG-TS decoding; PSI/SI parsing; NIT-based discovery; general-purpose
or unrestricted crawling; browser automation; replacing DVB tooling; claiming
completeness of the open web.

The non-goals are enforced mechanically: `tools/verify.mjs` fails if a DVB/RF
symbol appears in the artifact.

---

## 8. Concurrency Verification

Required invariant: **a candidate may have at most one active owner.**

| Property | Verdict | Evidence |
| --- | --- | --- |
| `claimNextCandidate()` performs the ownership transition synchronously | PROVED | no `await` in the method; sets `status='claimed'` before returning |
| Worker claims before its first suspension point | PROVED | `worker()` calls the claim, then `plan()`, then `markAcquiring()` synchronously before `await executePlan()` |
| Two workers can obtain the same candidate via the claim function | no (single context) | eligibility filter excludes `claimed`/`planned`/`acquiring`/`observed` |
| Two workers can obtain the same candidate at all | **yes — defect D1** | `addCandidate()` returns the existing candidate on re-discovery; `queueCandidate()` re-queues it for any non-terminal state; measured 2–4 concurrent owners |
| Duplicate acquisition of the same URL | **yes — defect D1/D6** | the resource guard is checked before the request completes, so both owners pass it |
| Safe because JavaScript is synchronous between awaits | yes | stated explicitly; not a general lock |
| Safe across tabs, workers or devices | **no** | no shared claim state, no leases, no fencing |
| Retry behaviour | partial | backoff written to `nextAttemptAt`; ignored for `failed` (D3) |
| Worker termination | defect D2 | permanent exit on an empty eligible set |
| Queue exhaustion | defect D4 | `running` stays true; restart requires reload |
| Cancellation | partial | cooperative `stopRequested`; in-flight request not aborted |
| Dynamically generated candidates | handled | expansion enqueues during the loop; any live worker can claim them |
| Duplicate candidates generated concurrently | partial | identity dedup is keyed on `type:target`; concurrent re-discovery triggers D1 |

Model comparison required by the brief:

```
SAFE (shipped claim function)          UNSAFE (inspect → await → acquire)
Worker A ─ claim(X) → owns X           Worker A ─ inspect X ─ await
Worker B ─ claim(X) → REJECT           Worker B ─ inspect X ─ await
   reason: synchronous transition        Worker A ─ acquire X
                                          Worker B ─ acquire X
```

The unsafe shape is preserved in `tools/simulate.mjs --unsafe-control`, where
the harness detects concurrent owners, proving the measurement is sensitive.

---

## 9. Provider Verification

Boundary: `Acquisition → Observation → ProviderRegistry → Provider → Discovery →
Candidate Expansion`. Verified in code:

| Provider | `matches()` | `recognize()` | Performs I/O | Enqueues candidates |
| --- | --- | --- | --- | --- |
| `HtmlProvider` | content type / body sniff | links, frames, scripts, media, forms, metadata | no | no |
| `JsonProvider` | content type / body sniff | URL-like values (recursive walk) | no | no |
| `XmlProvider` | content type / body sniff | `loc` values | no | no |
| `CssProvider` | CSS content type | `url(...)` references | no | no |
| `JavaScriptProvider` | script content type | URL-shaped string literals | no | no |
| `TextProvider` | fallback | HTTP(S) URLs in text | no | no |
| `BinaryProvider` | binary content type | none, by design | no | no |

* `Provider` declares only `matches()` and `recognize()` — there is **no**
  `candidates()` method, and none is needed: expansion belongs to the engine.
* All seven providers are registered in `ProviderRegistry`.
* Provider errors are caught per provider and recorded as `provider-error`
  diagnostics; they cannot fail the scan.
* No provider references network, storage, scheduler or policy APIs.

Violations found: none in the provider layer. The acquisition plane is *not*
pluggable (single hard-wired HTTP path), and candidate sources are engine methods
rather than an interface — both are scope reductions relative to the design
series and are labelled DESIGNED.

---

## 10. Provenance Verification

| Relationship | Implemented | Notes |
| --- | --- | --- |
| Candidate → why it exists | yes | `parent`, `hints`, `mechanism`, `depth`; `alternateParents` merges later origins |
| Observation → what was observed | yes | status, HTTP metadata, body/truncation flag, timing, `finalUrl` |
| Discovery → which candidate + observation | yes | `candidateId`, `observationId` |
| Discovery → interpretation provenance | yes | `provenance { origin, parent, candidateTarget, candidateType, mechanism, depth, hints }` |
| Candidate graph | yes | `graphEdges { from, to, relation }`, capped |
| Causal trace of decisions | yes | append-only ledger with `seq`, capped at 5000 |
| Evidence, competing interpretations, conflicts | no | DESIGNED (v0.16, v0.34) |
| Immutability of observations | no | stored in a mutable map, serialized on persistence |

Collapse risk identified and documented: the phrase "evidence" was used for plain
observations; the glossary now separates observation (CURRENT) from evidence
(DESIGNED).

---

## 11. Failure-Mode Matrix

See `docs/prototype/limitations.md` for the full matrix with detection, current
behaviour, desired behaviour and status for 26 failure modes, plus the seven defects D1–D7. Highlights:

| Failure | Current behaviour | Status |
| --- | --- | --- |
| duplicate candidate in flight | re-queued; 2–4 owners; duplicate acquisitions | **defect D1** |
| worker exits on empty frontier | pool never refilled; concurrency collapses | **defect D2** |
| HTTP 5xx | retried twice, then `failed`, then claimable again | **defect D3** |
| candidate awaiting backoff at quiescence | abandoned; `running` stays true; Scan becomes a no-op | **defect D4** |
| adaptive concurrency | counters change, pool does not | **defect D5** |
| non-atomic resource guard | both in-flight owners pass it | **defect D6** |
| `stats.acquired` | never incremented | **defect D7** |
| cross-origin target | rejected at creation and planning | handled |
| unsupported content type | binary provider matches, emits nothing | handled |
| malformed body | provider aborts, diagnostic recorded, scan continues | handled |
| persistence corruption | restore skipped, scan continues | handled |
| worker crash (unexpected throw) | worker dies; `start()` may reject (ARGUMENT) | OPEN |

No protection is claimed that is not implemented.

---

## 12. Proposed Repository Structure

Smallest structure that separates responsibilities (implemented):

```
README.md                                   concept, status, architecture, scope, index
prototype/generic-discovery-engine.user.js  the implementation (v0.7.1, verbatim)
docs/glossary.md                            canonical terminology
docs/architecture/discovery-model.md        loop + stage contracts
docs/architecture/candidate-model.md        candidate identity, lifecycle, bounds
docs/architecture/scheduler.md              claiming, budget, retry, termination
docs/architecture/provider-model.md         three planes, provider contract
docs/architecture/provenance.md             what is recorded, what is missing
docs/architecture/concurrency.md            ownership invariant and its violation
docs/prototype/userscript.md                artifact guide, versions, config, UI
docs/prototype/scope.md                     CURRENT / DESIGNED / FUTURE / NON-GOAL
docs/prototype/limitations.md               defects and failure-mode matrix
docs/research/dvb-blind-scan-inspiration.md analogy matrix and boundary
docs/roadmap/future-architecture.md         v0.8 … v0.35, labelled
docs/analysis/repository-analysis-2026-09-10.md  this review
archive/*.md                                unedited transcripts (non-normative)
archive/README.md                           why the archive exists
tools/verify.mjs                            static verification
tools/simulate.mjs                          dynamic harness
```

No file was created that has no distinct responsibility, and no document
duplicates another's canonical explanation.

---

## 13. Document-by-Document Rewrite Plan

| Document | Action | Reason |
| --- | --- | --- |
| `README.md` | **KEEP (rewritten)** | contained aspirational claims; now answers the five README questions with verified state and links |
| `Userscript Discovery Prototype.md` | **ARCHIVE** | historical research note; its DVB analogy was extracted to `docs/research/`, its generic principles merged into `docs/architecture/`, its broken v0.1.0/v0.2.0 pastes remain only as history |
| `Continue Architecture Planning.md` | **SPLIT + ARCHIVE** | three different things in one file: the implementation (extracted to `prototype/`), the design series (summarised in `docs/roadmap/`), and the conversation itself (archived) |
| embedded v0.7.1 userscript | **EXTRACT → KEEP** | it is the project's only working artifact and must be versioned as code, not as prose |
| embedded v0.3.0 – v0.6.0 userscripts | **ARCHIVE (in transcript)** | superseded; preserved for audit, not maintained |
| v0.1.0 / v0.2.0 pastes | **ARCHIVE** | syntactically invalid; no code value, historical value only |
| invalid v0.5.0 paste (lines 18378–23093) | **ARCHIVE** | does not parse; superseded by v0.6.0 |
| design series v0.8 … v0.35 | **SUMMARISE** in `docs/roadmap/future-architecture.md` | the detail is not reproducible in a normative document without inventing code; the summary preserves every boundary decision with labels |
| README roadmap "Phase 0–4" | **MERGE** into the roadmap document | duplicates the version series with different (and inaccurate) completion marks |
| last-formulation section | **MERGE** into roadmap + scope | states the design intent; must not be read as implemented behaviour |

Nothing was deleted. Text removed from the README was either contradicted by the
code (obsolete implementation claims), duplicated in a canonical document, or
conversational filler.

---

## 14. Clean Canonical Architecture

```
                       ┌──────────────────────────────┐
   seeds              │        Discovery Engine      │
   page / DOM /  ───► │  (orchestration, expansion,  │
   network            │   persistence, ledger, UI)   │
                       └───────────────┬──────────────┘
                                       │
                              ┌────────▼────────┐
                              │    Scheduler    │  claim: synchronous ownership
                              │  + policy/budget│  policy: GET, depth, classes
                              └────────┬────────┘
                                       │
                              ┌────────▼────────┐
                              │   Acquisition   │  transport, timeout,
                              │  (+ origins)    │  origin limits, budget
                              └────────┬────────┘
                                       │
                              ┌────────▼────────┐
                              │   Observation   │  always produced, incl. failures
                              └────────┬────────┘
                                       │
                              ┌────────▼────────┐
                              │ ProviderRegistry│  matches() / recognize()
                              └────────┬────────┘
                                       │
      ┌────────┬────────┬────────┬─────┴────┬────────┬────────┐
      ▼        ▼        ▼        ▼          ▼        ▼        ▼
    HTML     JSON      XML      CSS        JS      Text    Binary
      └────────┴────────┴────────┴──────────┴────────┴────────┘
                                       │
                                 Discovery[]
                                       │
                            ┌──────────▼──────────┐
                            │ Candidate Expansion │  engine-owned, depth/budget
                            └──────────┬──────────┘
                                       │
                                   Scheduler ↺
```

Knowledge base and decision ledger sit alongside the loop and record
candidates, observations, discoveries, resources, edges and events.

Labelled status of each element: everything drawn here is CURRENT except the
capability, work-item, evidence, coverage and coordination layers, which are not
drawn because they do not exist.

---

## 15. Implementation Gaps

Only gaps that matter for the next implementation step:

1. **Ownership transition vs re-discovery (D1).** Decide whether re-discovery may
   re-queue at all; if work must be re-proposed, model it as work, not as
   candidate state.
2. **Terminal failure (D3).** Give `failed` a terminal or backoff-gated meaning.
3. **Worker lifecycle (D2, D4).** A pool that never refills and a `running` flag
   that never clears make scan control dishonest; fix the control plane before
   adding features.
4. **Atomic acquisition guard (D6).** The resource guard must be decided at the
   same instant as ownership, or derived from it.
5. **Cancellation (v0.10 design).** `stop()` cannot abort in-flight work; without
   it, budget accounting is approximate.
6. **Termination semantics (v0.14 design).** "Idle", "budget-exhausted" and
   "stop-requested" need distinct, persisted meanings before any coverage claim
   is meaningful.
7. **Reporting truth (D5, D7).** Statistics that are structurally wrong (adaptive
   concurrency, `acquired`) must be corrected or removed before they are used in
   design review.

Not in scope for the next step: capabilities, evidence graphs, leases, coverage
claims — implementing them on top of an unsound ownership baseline would
reproduce the defect at a larger scale.

---

## 16. Verification Plan

| Claim | Current status | Test that changes it | Result |
| --- | --- | --- | --- |
| Claim operation is atomic in one context | ARGUMENT → **PROVED** | static check that the claim is synchronous and transitions before returning (`tools/verify.mjs`) | passing |
| Provider contract holds | ARGUMENT → **PROVED (static)** | static checks: methods exist, registry complete, no I/O in providers | passing |
| No DVB/RF implementation | claim → **PROVED (static)** | symbol scan over the artifact | passing |
| No later-design layers present | claim → **PROVED (static)** | symbol scan for work items, evidence graph, leases, coverage | passing |
| Single-owner invariant end to end | claim → **DISPROVED** | execute the artifact with 4 workers and a re-discovering workload; measure concurrent owners and duplicate acquisitions (`tools/simulate.mjs`) | defect D1 reproduced |
| Claiming is safe under an unsafe scheduler | — | negative control with an ownership-free claim function; harness must detect violations (`--unsafe-control`) | detected |
| Deterministic expansion/dedup | ARGUMENT | dry-run harness with fixed responses asserts each URL is acquired once | fails while D1 exists |
| Persistence round-trip | ARGUMENT → OPEN | export → restore → compare candidate/observation/discovery counts | not implemented |
| Timeout and retry semantics | ARGUMENT → PROVED (dynamic, partial) | harness returns 5xx/timeouts and asserts backoff and terminal behaviour | retry observable; terminal behaviour is D3 |
| Worker-pool behaviour | ARGUMENT → PROVED (dynamic) | measure peak live workers with empty vs pre-populated frontier | D2 confirmed |

Reproduction:

```bash
node tools/verify.mjs               # static; exits non-zero on documentation drift
node tools/simulate.mjs             # dynamics; reports the defects it observes
node tools/simulate.mjs --unsafe-control   # negative control
```

Not yet implemented and required before feature work: a deterministic replay
harness (fixed responses, fixed delays), persistence round-trip test, and a
regression test that asserts the single-owner invariant after D1 is fixed.

---

## 17. Recommended Execution Order

1. **Freeze terminology** — `docs/glossary.md` is the reference for all further
   writing. *(done)*
2. **Establish implementation truth** — extract the artifact, verify it, state
   what exists. *(done)*
3. **Separate prototype from architecture** — CURRENT / DESIGNED / FUTURE labels
   everywhere. *(done)*
4. **Extract canonical architecture** — one loop diagram, one provider diagram,
   one concurrency diagram. *(done)*
5. **Split documents by responsibility** — `docs/` tree, archive the transcripts.
   *(done)*
6. **Remove duplication** — one canonical location per concept (section 6).
   *(done)*
7. **Resolve contradictions** — resolved or marked OPEN, never guessed away
   (section 5). *(done)*
8. **Add missing invariants** — ownership, provider purity, expansion ownership,
   failure-as-observation. *(done; ownership marked violated)*
9. **Update the README** — five questions, reality not aspiration. *(done)*
10. **Verify implementation against documentation** — `tools/verify.mjs` +
    `tools/simulate.mjs`. *(done; defects D1–D7 recorded)*
11. **Fix the ownership and control-plane defects (D1, D2, D3, D4, D6)** before
    adding any designed layer.
12. **Only then** consider the v0.10/v0.11 runtime boundaries, which are the
    smallest useful next architectural step.

---

## Final Quality Gate

| Criterion | Status |
| --- | --- |
| Current implementation distinguishable from planned architecture | yes — labels throughout |
| DVB analogy bounded | yes — matrix + explicit non-claims + static enforcement |
| Candidate lifecycle unambiguous | yes — one state list, one diagram |
| Candidate claiming race-safe | **no — D1 documented and reproduced**; claim function itself is atomic |
| Provider/acquisition boundary explicit | yes — verified rule table |
| Observation and discovery distinct | yes — separate records, separate documents |
| Provenance explicit | yes — recorded fields, limits and missing layers |
| Failure modes documented | yes — 26 entries + 7 defects |
| Duplicate explanations have canonical locations | yes — duplication map |
| Contradictions resolved or marked OPEN | yes — 8 conflicts closed, OPEN items listed |
| README describes reality, not aspiration | yes |
| Future architecture clearly labelled | yes — roadmap with DESIGNED/CONJECTURE/OPEN |
| No unsupported implementation claims remain | yes — each claim checked or labelled |
| No important architectural decision silently lost | yes — archive retained; summaries cite versions |
