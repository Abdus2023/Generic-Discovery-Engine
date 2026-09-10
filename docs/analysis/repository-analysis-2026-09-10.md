# Repository Analysis — 2026-09-10

Deep structural review of `Abdus2023/Generic-Discovery-Engine` at commit
`cc8df73` ("Add files via upload"), performed before and during the
documentation cleanup. Output order follows the review brief (Phases 0–21).

## Analysis control block

| | |
| --- | --- |
| Repository | `Abdus2023/Generic-Discovery-Engine` |
| Resolved commit (analysis target) | `cc8df7357c2dbfe9d149747743e2f5e9ac9c0178` (`main`) |
| Access classification | **FULL ACCESS** — complete tree, no submodules, no external artifacts to inspect |
| Evidence standard | every non-trivial finding cites `[EVID:…]` from the [evidence register](evidence-register.md) |
| State model | six typed fields per claim — `claim_kind`, `implementation_state`, `test_state`, `evidence_level`, `claim_verification.result`, `confidence` — plus independent authority dimensions (`authorization.state`, `authorization.level.profile`, `capabilities`, `operations`, `scope`, `change_ids`) and independent lifecycles (`execution.state` with per-operation `authorization_decision` and `result`, `execution_verification.state` with its own `result` and per-check outcomes). Normative record: [analysis.json](analysis.json) under [analysis.schema.json](analysis.schema.json); readable tables: [claims.md](claims.md) |
| Enforcement | [EVID:TEST-014] `tools/validate-analysis.mjs` runs the brief-11 pipeline — [EVID:DOC-013] schema validity against `analysis.schema.json` (draft 2020-12, closed root), object validity `REQ-001`–`REQ-015`, cross-object semantics (`CV-001`–`CV-020` of section 144, evidence rules `C-030`–`C-034` with the recorded absence procedures, capability rules `CAP-001`–`CAP-016` and `CG-001`–`CG-015`), the section 216 authorization function re-deriving every recorded decision from the effective capability set, execution invariants `EV-001`–`EV-012` with the section 200 transition graph, execution-verification rules `EVV-001`–`EVV-009`, YAML ≡ JSON serialization and invariants `I-001`–`I-016`: no generic status field, no field substitution, executed ⊆ authorized, documentation never proves implementation, `ABSENT` ≠ `INACCESSIBLE`. The vocabulary layer is separate from the schema: [EVID:DOC-015] five versioned registries under `docs/analysis/registries/` own the capability, level-profile, operation, resource-class and claim vocabularies, and the model is specified in [EVID:DOC-016] [validation-model.md](validation-model.md) |
| Scope boundary | repository / artifact / verification / execution — recorded in [scope-and-authorization.md](scope-and-authorization.md) |
| Authorization | one `state: GRANTED` object on profile `PUSH`, 21 capability grants (5 `ENABLED`, 5 `RESTRICTED`, 11 `DENIED`); the tenant is capability-level, not profile-level: `CAP-DOCUMENT-MODIFY` is scoped to `README.md`/`docs/`/`tools/`, `CAP-SOURCE-CREATE` to `prototype/` (the disclosed extraction for `R-001`), and `CAP-SOURCE-MODIFY`, `CAP-TEST-*`, `CAP-ARCHITECTURE-MODIFY`, `CAP-DOCUMENT-DELETE` are `DENIED`; `change_ids: R-001 … R-021`; effective set computed from registry ∩ grants − denies, never stored |
| Phase A — verification | **read-only**; no repository file was created, edited or moved while establishing truth |
| Phase B — refactoring | plan and execution recorded separately in the [change register](change-register-2026-09-10.md) |
| Code changes | **none** — the artifact digest is unchanged since extraction and enforced (`sha256 8f5fc5c5…`); all code findings are `PLAN ONLY` |
| Execution / execution verification | `execution.state: SUCCEEDED` across 23 recorded operations, every one `authorization_decision: ALLOWED` and `result: SUCCEEDED` · `execution_verification.state: PASSED` / `result: CONFORMING` across eight checks, `mutations: []` · `unauthorized_changes: []` |
| Negative evidence | absence is recorded as `ABSENT` only where the declared inspection scope justifies it, with a recorded procedure `AV-001 … AV-007` (rules CV-006, CV-010, CV-020) |

**Record construction.** [analysis.json](analysis.json) is normative; the tables in
[claims.md](claims.md) are rendered from it by `tools/render-claims.mjs` and never
hand-edited, and `tools/validate-analysis.mjs` enforces the schema, the registries
and the rule sets. The schema owns shape; the registries under
[registries/](registries/) own what the identifiers mean; the validator owns
whether the references and relationships hold (brief 11 sections 218–243, specified
in [validation-model.md](validation-model.md)). Verification is recorded: every run
closes with an entry in [validation-runs.json](validation-runs.json) that binds the
verdict to the digests of the document, the schema, the registries and the
validator, carries every error with its phase, and compares the working-tree digest
before and after the run so that "verification modified nothing" is measured rather
than asserted.
Values are taken from repository evidence only: no value is invented to satisfy the
schema, and a rule that cannot be satisfied is reported as a failure rather than
worked around. Timestamps are recorded at date granularity — the work was performed
in one session on that date and per-operation wall-clock times were not captured —
and the six claims-substantive fields of brief 7 are carried per claim, with a
seventh, advisory field, `confidence`, that never replaces them (section 141).


**Verification result: VERIFIED** — the repository state, implementation, and
documentation claims were assessed with full access and are reproducible from the
recorded commit and tool runs.

**Refactoring result: EXECUTED + EXECUTION-VERIFIED** for documentation
(`R-001 … R-021`); **PLAN ONLY** for code (`R-101 … R-112`).

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

### Access contract reference

Full record (branch, commit, accessible scope, unavailable scope, fallback
history): [evidence register, "Repository access contract"](evidence-register.md).
No fallback source was needed: the requested repository, branch and documents
were available locally, and no substituted fork or mirror was used.

### Verification performed

* every fenced userscript block was extracted and parsed with `node --check`:
  **9 of 10 parse**, the v0.5.0 paste at transcript lines 18378–23093 does not
  (`await` outside an async function);
* the v0.7.1 block was extracted verbatim and re-parsed (`vm.Script`) — see
  `tools/verify.mjs`;
* the artifact was executed under a browser shim to observe runtime behaviour —
  see `tools/simulate.mjs` (one long scenario) and `tools/checks.mjs` (isolated
  invariants in fresh contexts) — evidence TEST-004 … TEST-013;
* every finding was assigned an evidence ID with path, locator, type, quality and
  status in the [evidence register](evidence-register.md);
* README claims were checked one by one against the artifact; results appear in
  sections 3, 5 and 7.

---

## 2. Executive Findings

1. The repository contained **one real implementation** — the v0.7.1 userscript — *(evidence: [EVID:DOC-002], [EVID:DOC-003], [EVID:CODE-001])*
   buried inside a 92k-line chat transcript, and **no repository file that
   described it accurately**.
2. Everything from v0.8 to v0.35 is **design prose with no code**; the README and
   the transcript's conclusion read as if that architecture were the project.
3. The prototype is genuinely layered: candidates, scheduler, acquisition,
   recognition providers, knowledge base, decision ledger, persistence, export.
4. The provider boundary is **clean and verified**: providers perform no I/O,
   never enqueue candidates, never touch scheduling — the strongest part of the
   design. The engine (not the provider) owns expansion.
5. The claim operation is synchronous and marks ownership before any `await`; *(evidence: [EVID:CODE-009], [EVID:CODE-018], [EVID:TEST-001])*
   within one execution context two workers cannot claim the same candidate *via
   the claim function*.
6. However, the stated invariant "a candidate may have at most one active owner" *(evidence: [EVID:CODE-008], [EVID:CODE-021], [EVID:TEST-009], [EVID:TEST-011])*
   is **violated end to end** (**D1**): `queueCandidate()` refuses only
   `completed`/`skipped`, so re-discovery re-queues in-flight candidates —
   measured at 2–4 concurrent owners and 12–18 duplicate acquisitions per run.
7. Workers exit permanently when no candidate is eligible at that instant (**D2**), *(evidence: [EVID:CODE-018], [EVID:TEST-010])*
   so effective concurrency collapses toward 1; work waiting on retry backoff is
   abandoned while `running` stays true and the Scan button becomes a no-op (**D4**).
8. `failed` is a claimable state with no backoff (**D3**), so a permanently broken *(evidence: [EVID:CODE-009], [EVID:CODE-010])*
   target can consume the request budget.
9. Adaptive concurrency updates a variable the already-created worker pool never *(evidence: [EVID:CODE-018], [EVID:CODE-029], [EVID:CODE-023], [EVID:CODE-030])*
   reads (**D5**), `stats.acquired` is never incremented (**D7**), and content
   fingerprints are indexed but never consulted (**D8**).
10. Recognition is broader than the documentation implied: HTML, JSON and XML *(evidence: [EVID:CODE-016], [EVID:TEST-006], [EVID:TEST-012])*
    match by **content type or body sniff**, `TextProvider` matches `text/*` (not
    a universal fallback), and several providers match one observation — so a
    `text/html` body is interpreted twice and discovery records are duplicated
    (**D9**).
11. Provenance is partly implemented but partial in a precise sense: candidate, *(evidence: [EVID:CODE-005], [EVID:TEST-007])*
    observation and discovery records link correctly and the chain is
    reconstructible (verified), while evidence, competing interpretations and
    conflict handling do not exist.
12. Persistence is stronger than assumed and weaker than needed: candidates, *(evidence: [EVID:CODE-025], [EVID:TEST-008])*
    observations, discoveries, resources, edges **and the ledger** survive a
    reload (verified), but there is no transaction, no validation, and the run
    state is not restored.
13. Terminology had drifted badly; one canonical term per concept is now fixed in
    a glossary with an explicit conflict table.
14. The DVB analogy is legitimate as control-structure inspiration and was at risk *(evidence: [EVID:SCOPE-001], [EVID:TEST-003])*
    of being read as a compatibility claim; it is now bounded, matrixed, and
    enforced by a static symbol check.
15. The repository now holds the code, the normative documents, the non-normative
    archive, and three executable verification tools whose results are recorded
    in this document.

## 3. Architecture Truth Table

The six typed fields are recorded **once**, in
[analysis.json](analysis.json) (machine-readable) and rendered into
[claims.md](claims.md) (readable). This section is an index from architectural
area to the claim that carries its status, so a second copy of the verdicts
cannot drift out of step.

| Area | Owning claim(s) | Field summary |
| --- | --- | --- |
| Candidate identity and dedup | `CLAIM-001` | `CURRENT` · `IMPLEMENTED` · `TESTED` · `CORROBORATED` · `VERIFIED` |
| Candidate as hypothesis | `CLAIM-002` | `CURRENT` · `IMPLEMENTED` · `UNTESTED` · `INDIRECT` · `PARTIALLY_VERIFIED` |
| Bounds (caps, depth, budget) | `CLAIM-003` | `CURRENT` · `IMPLEMENTED` · `UNTESTED` · `DIRECT` · `VERIFIED` |
| Claim atomicity at the claim site | `CLAIM-004` | `CURRENT` · `IMPLEMENTED` · `TESTED` · `CORROBORATED` · `VERIFIED` |
| Single-owner invariant end to end | `CLAIM-005` | `CURRENT` · `PARTIAL` · `TESTED` · `CORROBORATED` · `CONTRADICTED` |
| Retry and backoff | `CLAIM-006` | `CURRENT` · `PARTIAL` · `TESTED` · `DIRECT` · `PARTIALLY_VERIFIED` |
| Terminal failure | `CLAIM-007` | `CURRENT` · `NOT_IMPLEMENTED` · `TESTED` · `DIRECT` · `CONTRADICTED` |
| Worker pool and concurrency | `CLAIM-008` | `CURRENT` · `PARTIAL` · `TESTED` · `CORROBORATED` · `CONTRADICTED` |
| Adaptive concurrency | `CLAIM-009` | `CURRENT` · `NOT_IMPLEMENTED` · `UNTESTED` · `DIRECT` · `CONTRADICTED` |
| Acquisition transport | `CLAIM-010` | `CURRENT` · `IMPLEMENTED` · `TESTED` · `CORROBORATED` · `VERIFIED` |
| Observation on failure | `CLAIM-011` | `CURRENT` · `IMPLEMENTED` · `UNTESTED` · `CORROBORATED` · `VERIFIED` |
| Cancellation | `CLAIM-012` | `CURRENT` · `NOT_IMPLEMENTED` · `UNTESTED` · `DIRECT` · `CONTRADICTED` |
| Discovery linkage | `CLAIM-013` | `CURRENT` · `IMPLEMENTED` · `TESTED` · `DIRECT` · `VERIFIED` |
| Derivation chain | `CLAIM-014` | `CURRENT` · `IMPLEMENTED` · `TESTED` · `CORROBORATED` · `VERIFIED` |
| Content identity (fingerprints) | `CLAIM-015` | `SPECIFIED` · `NOT_IMPLEMENTED` · `UNTESTED` · `DIRECT` · `CONTRADICTED` |
| Observation ≠ discovery | `CLAIM-016` | `CURRENT` · `IMPLEMENTED` · `TESTED` · `DIRECT` · `VERIFIED` |
| Evidence layer | `CLAIM-017` | `SPECIFIED` · `NOT_IMPLEMENTED` · `NOT_APPLICABLE` · `ABSENT` · `UNVERIFIED` |
| Observation immutability | `CLAIM-018` | `CURRENT` · `NOT_IMPLEMENTED` · `UNTESTED` · `DIRECT` · `UNVERIFIED` |
| Provider boundary | `CLAIM-019` | `CURRENT` · `IMPLEMENTED` · `TESTED` · `CORROBORATED` · `VERIFIED` |
| Protocol independence | `CLAIM-020` | `CURRENT` · `NOT_IMPLEMENTED` · `PARTIALLY_TESTED` · `DIRECT` · `CONTRADICTED` |
| Expansion ownership | `CLAIM-021` | `CURRENT` · `IMPLEMENTED` · `TESTED` · `CORROBORATED` · `VERIFIED` |
| Discovery deduplication | `CLAIM-022` | `CURRENT` · `NOT_IMPLEMENTED` · `TESTED` · `CORROBORATED` · `CONTRADICTED` |
| Persistence across reload | `CLAIM-023` | `CURRENT` · `IMPLEMENTED` · `TESTED` · `CORROBORATED` · `VERIFIED` |
| Transactional persistence | `CLAIM-024` | `SPECIFIED` · `NOT_IMPLEMENTED` · `NOT_APPLICABLE` · `ABSENT` · `UNVERIFIED` |
| Request budget | `CLAIM-025` | `CURRENT` · `IMPLEMENTED` · `TESTED` · `CORROBORATED` · `VERIFIED` |
| Cross-context coordination | `CLAIM-026` | `SPECIFIED` · `NOT_IMPLEMENTED` · `NOT_APPLICABLE` · `DIRECT` · `CONTRADICTED` |
| Confidence comparability | `CLAIM-027` | `CURRENT` · `NOT_IMPLEMENTED` · `UNTESTED` · `DIRECT` · `UNVERIFIED` |
| Multiple provider matches | `CLAIM-028` | `CURRENT` · `IMPLEMENTED` · `TESTED` · `CORROBORATED` · `VERIFIED` |
| No DVB/RF implementation | `CLAIM-029` | `CURRENT` · `NOT_IMPLEMENTED` · `NOT_APPLICABLE` · `ABSENT` · `VERIFIED` |
| No v0.8+ layers implemented | `CLAIM-030` | `CURRENT` · `NOT_IMPLEMENTED` · `NOT_APPLICABLE` · `ABSENT` · `VERIFIED` |
| Coverage / absence / completeness | `CLAIM-031` | `CURRENT` · `NOT_IMPLEMENTED` · `NOT_APPLICABLE` · `ABSENT` · `VERIFIED` |
| Non-URL targets | `CLAIM-032` | `CURRENT` · `NOT_IMPLEMENTED` · `NOT_APPLICABLE` · `ABSENT` · `VERIFIED` |
| Repository tooling at the analysis revision | `CLAIM-033` | `HISTORICAL` · `NOT_IMPLEMENTED` · `NOT_APPLICABLE` · `ABSENT` · `VERIFIED` |
| DVB support as a non-goal | `CLAIM-034` | `NON_GOAL` · `NOT_APPLICABLE` · `NOT_APPLICABLE` · `DIRECT` · `VERIFIED` |
| Design series v0.8–v0.35 | `CLAIM-035` | `PLANNED` · `NOT_IMPLEMENTED` · `NOT_APPLICABLE` · `DIRECT` · `VERIFIED` |
| Profile coordination ≠ consensus | `CLAIM-036` | `SPECIFIED` · `NOT_IMPLEMENTED` · `NOT_APPLICABLE` · `DIRECT` · `VERIFIED` |
| Replay separable from acquisition | `CLAIM-037` | `SPECIFIED` · `NOT_IMPLEMENTED` · `NOT_APPLICABLE` · `DIRECT` · `VERIFIED` |
| Historical versions | `CLAIM-038` | `HISTORICAL` · `IMPLEMENTED` · `UNTESTED` · `DIRECT` · `VERIFIED` |
| Invalid v0.5.0 paste | `CLAIM-039` | `HISTORICAL` · `NOT_IMPLEMENTED` · `NOT_APPLICABLE` · `DIRECT` · `VERIFIED` |
| Pre-cleanup README accuracy | `CLAIM-040` | `HISTORICAL` · `NOT_APPLICABLE` · `NOT_APPLICABLE` · `CORROBORATED` · `CONTRADICTED` |
| Value × probability ÷ cost model | `CLAIM-041` | `HYPOTHESIS` · `NOT_APPLICABLE` · `NOT_APPLICABLE` · `INDIRECT` · `UNVERIFIED` |

Reading rule: `PLANNED` + `NOT_IMPLEMENTED` + `VERIFIED` means *the fact that it
is planned is verified*; it never implies implementation.

## 4. Terminology Audit

The canonical table — definition, current usage, conflicting usages, canonical
usage and the documents corrected — is owned by
[../glossary.md](../glossary.md). Summary:

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

**CONFLICT 9 — "deduplicated discovery"**
*Statement A:* the architecture presents the engine as deduplicating what it
finds (one candidate per identity, one resource per URL).
*Statement B:* the discovery store is not deduplicated: `emitDiscovery()` always
stores a `Discovery` before the derived candidate is deduplicated, and
`text/html` bodies are interpreted by two providers, so the same URL is recorded
as several discoveries (74 discoveries for 27 unique URLs in one harness run).
*Evidence:* dynamic (`tools/simulate.mjs`), static (`emitDiscovery()` ordering,
provider matching rules).
*Resolution:* candidate identity is deduplicated; discovery identity is not.
Tracked as D9, with the two mechanisms documented.
*Documents changed:* `docs/prototype/limitations.md`,
`docs/architecture/provider-model.md`, `docs/architecture/provenance.md`.

**CONFLICT 10 — content identity exists but is unused**
*Statement A:* the prototype computes content fingerprints and maintains a
hash → URL index, which reads like content-identity resolution.
*Statement B:* no code reads that index; identical bytes behind different URLs are
never related.
*Evidence:* static (4 write/probe sites, 0 read sites).
*Resolution:* fingerprinting is an observation feature, not an identity feature.
Tracked as D8.
*Documents changed:* `docs/architecture/provenance.md`,
`docs/prototype/limitations.md`.

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

Scope is now expressed in three tiers — Implemented, Partially implemented,
Not implemented (designed and non-goal) — owned by
[../prototype/scope.md](../prototype/scope.md). Summary:

`claim_kind: CURRENT` · `implementation_state: IMPLEMENTED` · `test_state: TESTED` ·
`evidence_level: CORROBORATED` · `claim_verification.result: VERIFIED` — present and
demonstrated (see [claims.md](claims.md)): seed generation; candidate
normalization; identity deduplication; resource-level acquisition guard;
synchronous candidate claiming; worker pool; HTTP GET acquisition with timeout;
content-type handling and sniffing; HTML/JSON/XML/CSS/JS/text/binary
recognition; URL and resource extraction; candidate expansion with depth and
candidate caps; persistence with caps; JSON export; control panel; per-provider
error isolation; request budget; origin rate limiting; retry with backoff;
decision ledger; graph edges; policy gating (GET-only, depth, disabled classes,
scope).

`claim_kind: CURRENT` with `claim_verification.result: PARTIALLY_VERIFIED` or
`CONTRADICTED` — real function with a named limitation: concurrency
(pool not refilled, D2), adaptive concurrency (no effect, D5), persistence (no
transaction or reconciliation), retry (`failed` bypasses backoff, D3),
termination (no completion criterion, D4), cancellation (cooperative only),
content identity (fingerprints unused, D8), discovery accounting (duplicates
not merged, D9), statistics (`acquired` dead, D7).

`claim_kind: SPECIFIED` / `PLANNED` · `implementation_state: NOT_IMPLEMENTED` ·
`evidence_level: INDIRECT` — documented, not implemented: capability lattice, acquisition runtime, recognition runtime,
candidate sources and controller, discovery domain and sessions, work items and
frontier arbitration, evidence graph, resource identity resolution,
classification axes, representations/artifacts/revisions, partitioning,
adaptive strategies, coverage, absence, goal-constrained discovery, query
planner, tactics, enumeration, reconciliation, cost ledger, transactional
persistence, multi-worker coordination, conflict resolution, replication.

`claim_kind: HYPOTHESIS`: learned priority, cross-domain discovery, non-HTTP transports,
completeness claims.

`claim_kind: NON_GOAL` · `evidence_level: ABSENT` (inspected scope covered), seen in
`CLAIM-029`/`CLAIM-034`: RF spectrum scanning; SDR and tuner control; DVB-S/S2, DVB-T/T2,
DVB-C demodulation; carrier synchronization; symbol-rate estimation; FEC
decoding; MPEG-TS decoding; PSI/SI parsing; NIT-based discovery; general-purpose
or unrestricted crawling; browser automation; replacing DVB tooling; claiming
completeness of the open web.

The non-goals are enforced mechanically: `tools/verify.mjs` fails if a DVB/RF
symbol appears in the artifact.

**Negative-evidence discipline:** absences inside the single implementation file
are recorded as ABSENCE_VERIFIED (full read + mechanical scan); absences of
repository artifacts that never existed are recorded as NOT_FOUND. No absence is
asserted from a partial search (see the register's negative-evidence table,
[EVID:SCOPE-001 … SCOPE-007]).

---

## 8. Concurrency Verification

Required invariant: **a candidate may have at most one active owner.**

| Property | Verdict | Evidence |
| --- | --- | --- |
| `claimNextCandidate()` performs the ownership transition synchronously | evidence CORROBORATED, verification VERIFIED — `CLAIM-004` [EVID:CODE-009, TEST-001] | no `await` in the method; sets `status='claimed'` before returning |
| Worker claims before its first suspension point | PROVED | `worker()` calls the claim, then `plan()`, then `markAcquiring()` synchronously before `await executePlan()` |
| Two workers can obtain the same candidate via the claim function | no (single context) | eligibility filter excludes `claimed`/`planned`/`acquiring`/`observed` |
| Two workers can obtain the same candidate at all | **yes — defect D1** [EVID:CONC-002, TEST-009] | `addCandidate()` returns the existing candidate on re-discovery; `queueCandidate()` re-queues it for any non-terminal state; measured 2–4 concurrent owners |
| Duplicate acquisition of the same URL | **yes — defect D1/D6** | the resource guard is checked before the request completes, so both owners pass it |
| Safe because JavaScript is synchronous between awaits | yes | stated explicitly; not a general lock |
| Safe across tabs, workers or devices | **no** [EVID:SCOPE-004] | no shared claim state, no leases, no fencing; profile coordination ≠ distributed consensus |
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
| `HtmlProvider` | `text/html`, `application/xhtml+xml`, or body starting with `<!doctype html`/`<html` | links, frames, scripts, media, forms, metadata | no | no |
| `JsonProvider` | `application/json`, `*+json`, or body starting with `[`/`{` | URL-like values (recursive walk) | no | no |
| `XmlProvider` | `application/xml`, `text/xml`, `*+xml`, or body starting with `<?xml` | `loc` values | no | no |
| `CssProvider` | `text/css` (content type only) | `url(...)` references | no | no |
| `JavaScriptProvider` | javascript/ecmascript media types | URL-shaped string literals | no | no |
| `TextProvider` | **`text/*` or empty content type** — not a fallback | absolute and relative URLs in text | no | no |
| `BinaryProvider` | image/audio/video/pdf/zip/octet-stream | none, by design | no | no |

*Several providers may match one observation:* `text/html` matches HTML **and**
text, `text/css` matches CSS **and** text, `text/xml` matches XML **and** text.
All matches run; there is no router or priority in v0.7.1 (DESIGNED: v0.11).
This is the first of the two mechanisms behind D9.

* `Provider` declares only `matches()` and `recognize()` — there is **no**
  `candidates()` method, and none is needed: expansion belongs to the engine.
* All seven providers are registered in `ProviderRegistry`.
* Provider errors are caught per provider and recorded as `provider-error`
  diagnostics; they cannot fail the scan.
* No provider references network, storage, scheduler or policy APIs.

Violations found: none in the provider layer — `CLAIM-019`, evidence CORROBORATED, verification VERIFIED [EVID:CODE-014, CODE-015, TEST-002]. The acquisition plane is *not*
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
| Content fingerprint per observation/resource | yes (fnv1a32 over a normalized sample) | stored as `{ algorithm, hash, length, sampledLength }` |
| Content-identity index (`hash → URLs`) | populated, **never read** | D8 — dead evidence |

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
| content fingersprints collected but unused | index written, never read | **defect D8** |
| duplicate discovery of one URL | separate records from provider double-match and repeated expansion | **defect D9** |

No protection is claimed that is not implemented.

---

## 12. Search-Space Analysis

Canonical owner: [../architecture/search-space.md](../architecture/search-space.md).
Fields: `claim_kind` · `implementation_state` · `test_state` · `evidence_level` ·
`claim_verification.result`.

| Question | Answer (v0.7.1) | Claim state | Evidence state | Verification state |
| --- | --- | --- | --- | --- |
| Finite space? | Not enumerable; bounded by caps (750 candidates, depth 5, same origin) and budget (150 requests) | CURRENT | DIRECT | VERIFIED |
| Dynamically expanding? | Yes — recognition emits discoveries that emit candidates while workers run | CURRENT | DIRECT | VERIFIED |
| Growth control | Hard cap with silent drops; no rate control or throttle | CURRENT | DIRECT | VERIFIED |
| Duplicate suppression | Candidate identity `type:target`, resource guard, `visited` | CURRENT | CORROBORATED | PARTIALLY_VERIFIED — defeated in flight (D1) and at discovery level (D9) |
| Priority | Static heuristic over type, confidence, depth, attempts; no aging | CURRENT | DIRECT | VERIFIED |
| Termination | Empty eligible set, budget exhaustion or `stop()`; no completion criterion | CURRENT | CORROBORATED | PARTIALLY_VERIFIED — work can be stranded (D4) |
| Negative evidence | Not modelled; a failed acquisition is an observation | SPECIFIED | ABSENT | VERIFIED (as absent) — designed v0.23 |
| Coverage | Not measured; "exhausted" means "nothing eligible right now" | SPECIFIED | ABSENT | VERIFIED (as absent) — designed v0.22 |
| Revisiting | While `queued`; after `failed` without bound (D3); never after `completed`/`skipped` | CURRENT | DIRECT | VERIFIED |
| Staleness | No TTL, expiry or revalidation | SPECIFIED | ABSENT | VERIFIED (as absent) |
| Historical knowledge | Persisted across reloads, never used for scoring | CURRENT | CORROBORATED | VERIFIED (persistence) / UNVERIFIED (influence) |
| Exhaustive or opportunistic? | Opportunistic within bounds | CURRENT | INDIRECT | VERIFIED (as characterisation) |

The prototype must never claim coverage, absence or completeness. The strongest
accurate statements remain those in [claims.md](claims.md), "Claims deliberately
not made".

## 13. Proposed Repository Structure

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
docs/architecture/search-space.md           what is searched, bounds, termination
docs/prototype/userscript.md                artifact guide, versions, config, UI
docs/prototype/scope.md                     CURRENT / DESIGNED / FUTURE / NON-GOAL
docs/prototype/limitations.md               defects and failure-mode matrix
docs/research/dvb-blind-scan-inspiration.md analogy matrix and boundary
docs/roadmap/future-architecture.md         v0.8 … v0.35, labelled
docs/analysis/repository-analysis-2026-09-10.md  this review
archive/*.md                                unedited transcripts (non-normative)
archive/README.md                           why the archive exists
tools/verify.mjs                            static verification
tools/checks.mjs                            behavioural invariants (dedup, providers, provenance, persistence)
tools/simulate.mjs                          dynamic harness
```

No file was created that has no distinct responsibility, and no document
duplicates another's canonical explanation.

---

## 14. Document-by-Document Rewrite Plan

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

Executed changes and plan-only code changes, with categories, risk classes,
before/after states and post-refactor verification results, are recorded in the
[change register](change-register-2026-09-10.md) as `R-001 … R-021` (executed
documentation) and `R-101 … R-112` (code, PLAN ONLY).

---

## 15. Clean Canonical Architecture

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

## 16. Implementation Gaps

Classified as required: BUG, MISSING TEST, DOCUMENTATION GAP, ARCHITECTURAL GAP,
FUTURE FEATURE, RESEARCH QUESTION. A missing future feature is never a bug.

| # | Gap | Class | Architectural importance | Current state | Required work | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Re-discovery re-queues in-flight candidates (D1) | BUG | **critical** — breaks the stated ownership invariant and causes duplicate acquisition | reproduced in `tools/simulate.mjs` (2–4 owners, 12–18 duplicate URLs) | refuse re-queue for any non-terminal state, or model re-proposed work as work | P0 |
| 2 | `failed` stays claimable with no backoff (D3) | BUG | high — budget is consumed by dead targets | `claimNextCandidate()` includes `failed`; `markFailed()` sets no `nextAttemptAt` | give `failed` terminal or backoff-gated semantics | P0 |
| 3 | Worker pool is never refilled; workers exit on an empty frontier (D2) | BUG | high — a scan silently degrades to single-threaded and can strand work | measured peak workers 1 (empty start) vs 4 (pre-seeded) | keep workers alive until a scan-level stop condition, or respawn on new work | P0 |
| 4 | Retry backoff can leave work stranded and `running` stuck true (D4) | BUG | high — control plane lies about state | candidate observed `queued` with pending backoff at quiescence | explicit scan states: running / quiescent / exhausted / stopped | P1 |
| 5 | Per-URL acquisition guard is not atomic with ownership (D6) | BUG | high — duplicate acquisition | consequence of D1 | tie the guard to the ownership transition | P0 (with #1) |
| 6 | Discovery records are never deduplicated (D9) | BUG | medium — inflated counts, repeated expansion | 74 discoveries / 27 URLs measured | deduplicate, or store corroboration as provenance | P1 |
| 7 | Content fingerprint index is written but never read (D8) | BUG (dead capability) | medium — blocks any identity work | 4 write sites, 0 read sites | either consult it (identity) or remove it | P1 |
| 8 | `stats.acquired` never incremented (D7) | BUG | low — reporting | static | maintain or remove the counter | P2 |
| 9 | Adaptive concurrency has no effect (D5) | BUG (control plane) | low today, high if relied upon | counters update, pool fixed | drive the pool from the counter, or delete the feature | P2 |
| 10 | No test for the single-owner invariant after its fix | MISSING TEST | high — regression risk | the harness detects the violation but is not a pass/fail gate | add an assertion that fails on any concurrent owner | P0 |
| 11 | No deterministic replay fixture | MISSING TEST | medium | harness responses are randomized in delay only | fixed responses + fake clock for reproducible runs | P1 |
| 12 | No persistence-failure path test | MISSING TEST | medium | only the happy path is exercised | corrupt payload, quota exceeded, schema mismatch | P2 |
| 13 | Coverage/absence semantics | DOCUMENTATION GAP (resolved) + ARCHITECTURAL GAP | medium | now documented as absent; no object exists | design review of v0.22/v0.23 before implementation | P2 |
| 14 | Cancellation does not abort in-flight requests | ARCHITECTURAL GAP | medium | `stop()` sets a flag; the request continues | runtime-owned cancellation (v0.10 design) | P2 |
| 15 | No scan-level termination evaluator | ARCHITECTURAL GAP | high for any future coverage work | "idle" and "finished" are indistinguishable | define states and persist them | P1 |
| 16 | Acquisition transport is not an interface | ARCHITECTURAL GAP | medium | HTTP GET hard-wired | acquisition provider boundary (v0.9/v0.10 design) | P3 |
| 17 | Capabilities, work items, evidence graph, leases, coverage | FUTURE FEATURE | high long-term | DESIGNED only | do not start before P0 items are fixed | P3 |
| 18 | Is the search space finite in any useful sense? | RESEARCH QUESTION | high | unanswerable today | define what could be enumerated and what cannot | P2 |
| 19 | How should confidence be produced and compared? | RESEARCH QUESTION | medium | provider-local constants | calibration study across providers | P3 |
| 20 | How much coordination is safe inside one browser profile? | RESEARCH QUESTION | medium | unaddressed | storage-atomicity study before v0.33 work | P3 |

Anything not listed here was either not found or is already correct.

## 17. Verification Plan

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

### Executed procedures

| # | Procedure | Tool | Covers |
| --- | --- | --- | --- |
| 1 | static claim atomicity and ordering | `tools/verify.mjs` | claim before await, no suspension in the claim |
| 2 | provider contract and registry completeness | `tools/verify.mjs` | methods, registration, no I/O in providers |
| 3 | scope enforcement | `tools/verify.mjs` | DVB symbols, design-only symbols, doc links, README claims |
| 4 | candidate uniqueness | `tools/checks.mjs` | same `type:target` inserted twice → one logical candidate |
| 5 | type disambiguation | `tools/checks.mjs` | same URL, different type → two candidates |
| 6 | provider selection | `tools/checks.mjs` | 11 content-type/body cases, exact matching sets |
| 7 | provenance chain | `tools/checks.mjs` | seed → candidate → observation → discovery → child candidate |
| 8 | persistence round-trip | `tools/checks.mjs` | candidates, discoveries, resources and ledger survive reload; budget resets |
| 9 | ownership under load | `tools/simulate.mjs` | concurrent owners, duplicate acquisitions (D1) |
| 10 | scheduler sensitivity | `tools/simulate.mjs --unsafe-control` | proves the harness detects an ownership violation |

Reproduction:

```bash
node tools/verify.mjs               # static; exits non-zero on documentation drift
node tools/checks.mjs               # behavioural invariants; exits non-zero on drift
node tools/simulate.mjs             # dynamics; reports the defects it observes
node tools/simulate.mjs --unsafe-control   # negative control
```

Still missing and required before feature work: a pass/fail regression gate for
the single-owner invariant (after D1 is fixed), a deterministic replay fixture,
and a persistence-failure path test.

---

## 18. Recommended Execution Order

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
12. **Fix the accounting defects (D7, D9)** — counters and discovery records that
    misstate what happened will corrupt any later coverage reasoning.
13. **Decide the fate of the fingerprint index (D8)** — consult it or delete it;
    leaving dead evidence invites false assumptions about identity resolution.
14. **Add the missing regression gate** — a pass/fail assertion for the
    single-owner invariant, plus a deterministic replay fixture.
15. **Only then** consider the v0.10/v0.11 runtime boundaries, which are the
    smallest useful next architectural step.

---

## Final Quality Gate

| Criterion | Status |
| --- | --- |
| Current implementation distinguishable from planned architecture | yes — labels throughout |
| DVB analogy bounded | yes — matrix + explicit non-claims + static enforcement |
| Candidate lifecycle unambiguous | yes — one state list, one diagram |
| Candidate claiming race-safe | **no — D1 documented and reproduced**; claim function itself is atomic within one execution context |
| Candidate identity distinct from lifecycle | yes — `type:target` vs the state machine |
| Acquisition distinct from recognition | yes — enforced by the no-I/O provider rule |
| Retry behaviour documented | yes — backoff, and the `failed` exception (D3) |
| Candidate growth bounded or marked open | yes — caps, depth, budget, silent drops |
| Duplicate discoveries addressed | yes — measured, mechanism explained, tracked as D9 |
| Persistence semantics documented | yes — what round-trips (verified), what deliberately resets, what is missing |
| Diagrams canonicalized | yes — one loop, one provider graph, one concurrency model |
| No contradiction silently resolved | yes — 10 conflicts recorded with evidence and resolution |
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

---

## Governance Record

| Requirement | Where |
| --- | --- |
| Scope boundary (repository / artifact / verification / execution) | [scope-and-authorization.md](scope-and-authorization.md) §1 |
| Scope escalations (two, both OPEN, neither silently expanded) | same, §2 |
| Ownership and authorization matrix | same, §3, §7 |
| Decision ownership (fact / interpretation / design / execution) | same, §4 |
| Execution authorization contract (state, profile, capabilities, operations, scope, change set, rollback) | same, §5 |
| Change-set boundary and discovered-change rule | same, §5 |
| Pre-execution and post-execution checks, execution result | same, §6 |
| Canonical status vocabulary and claim records | [claims.md](claims.md) |
| Validation model: schema, registries, phases, error model | [validation-model.md](validation-model.md) |
| Vocabulary registries (capability, level profile, operation, resource class, claim) | [registries/](registries/) |
| Recorded verification runs, with phases, errors and tree digests | [validation-runs.json](validation-runs.json) |
| Evidence items, access contract, negative evidence | [evidence-register.md](evidence-register.md) |
| Executed and proposed changes | [change-register-2026-09-10.md](change-register-2026-09-10.md) |

## Final Audit Question

> Can another engineer trace every important architectural conclusion back to
> repository evidence, distinguish current reality from proposed future state, and
> determine exactly which changes were verified versus merely recommended?

| Requirement | Answer | Mechanism |
| --- | --- | --- |
| traceable to repository evidence | yes | every finding cites `[EVID:…]`; the register gives path, locator, source type, quality and status; `tools/verify.mjs` fails on a citation that does not resolve |
| current reality vs proposed future state | yes | `VERIFIED CURRENT STATE` and `PROPOSED TARGET STATE` are recorded side by side in the change register and never merged without labels; every roadmap item is labelled DESIGNED / CONJECTURE / OPEN |
| which changes were verified vs recommended | yes | executed documentation changes `R-001 … R-020` with execution-verification results; code changes `R-101 … R-112` marked **PLAN ONLY** with risk classes and priorities |
| which conclusions are limited by access | yes | access classification FULL; two scope escalations and three residual verification limitations are recorded and marked OPEN in the governance record |
| who authorized the changes | yes | authorization object with `state`, `level.profile`, `capabilities`, `operations`, `scope`, `change_ids`, rollback strategy, and the explicit statement that `CODE_REFACTOR` / `ARCHITECTURE_CHANGE` were never granted |
