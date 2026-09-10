# Change Register — 2026-09-10

Separation of responsibilities required by the analysis controls: **verification
established what is true; this document records what was changed, what is merely
proposed, and how each change was verified afterwards.**

| Phase | State | Boundary |
| --- | --- | --- |
| A — Verification (read-only) | complete | produced the [evidence register](evidence-register.md), [claims](claims.md) and the [analysis](repository-analysis-2026-09-10.md); **no repository state was modified during verification** |
| Authorization | level `DOC_REFACTOR`, plus `ANALYSIS_ONLY`, `COMMIT` and `PUSH` declared separately (no implied hierarchy) | full contract, allowed/forbidden operations and rollback in [scope-and-authorization.md](scope-and-authorization.md) §5; machine-readable in [analysis.json](analysis.json) |
| B — Refactoring plan | complete | every change below has an ID, evidence, category and risk |
| B — Refactoring execution | executed for documentation; **not executed for code** | authorization covered repository documentation restructure; no authorization was given for behavioural code changes, and the review briefs explicitly forbade fixing correctness ahead of establishing it |
| C — Post-refactor verification | complete for executed changes | see §Post-refactor verification |

Nothing in this register silently mixes "what is" with "what should be".

## Executed changes — documentation

| ID | Category | Before | After | Reason | Evidence | Risk | Verification | Result |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R-001 | DOC-SPLIT | one 92,274-line transcript containing implementation, design series and conversation | implementation extracted to `prototype/`, design series summarised in `docs/roadmap/`, transcript archived | three responsibilities in one artifact | DOC-002, DOC-003, DOC-006 | MEDIUM | `node --check`; `tools/verify.mjs` parse + version | PASS |
| R-002 | DOC-REWRITE | README asserted architecture the code did not contain | README describes verified behaviour, labelled scope, DVB boundary | unsupported implementation claims | DOC-001 vs CODE-008, TEST-009 | LOW | `tools/verify.mjs` README checks | PASS |
| R-003 | DOC-SPLIT | DVB analogy, discovery loop, concurrency and scope each repeated in several places | one canonical owner per concept; other documents link | duplication | DOC-007, DOC-011 | LOW | duplication map; link check in `tools/verify.mjs` | PASS |
| R-004 | DOC-MOVE | design series buried in a transcript | `docs/roadmap/future-architecture.md`, every stage labelled DESIGNED/CONJECTURE/OPEN | roadmap mixed with current behaviour | DOC-006 | LOW | `tools/verify.mjs` design-layer symbol scan | PASS |
| R-005 | DOC-MOVE | two transcripts at repository root | `archive/` with an index explaining their non-normative status | research vs specification | DOC-007 | LOW | archive README; analysis §14 | PASS |
| R-006 | DOC-REWRITE | "at most one active owner" stated as a property of the system | claim atomicity (PROVED) separated from the end-to-end invariant (violated, D1) | contradiction | CONC-001, CONC-002, TEST-009 | LOW | `tools/verify.mjs`, `tools/simulate.mjs` | PASS |
| R-007 | DOC-REWRITE | README/provider notes implied `TextProvider` was a fallback | exact matching rules documented; body sniffing and double-match stated | documentation contradicted code | CODE-016, TEST-006 | LOW | `tools/checks.mjs` exact-set cases | PASS |
| R-008 | DOC-REWRITE | provider material implied a `candidates()` method | contract documented as `matches()` + `recognize()`; expansion engine-owned | documentation implied a non-existent interface | CODE-015 | LOW | `tools/verify.mjs` provider-contract check | PASS |
| R-009 | DOC_CLEANUP | no terminology authority | `docs/glossary.md` with definitions, conflicting usages, canonical usage and corrected documents | inconsistent vocabulary | DOC-011 | LOW | consistency review across `docs/` | PASS |
| R-010 | TEST_ADD | no executable verification existed | `tools/verify.mjs`, `tools/checks.mjs`, `tools/simulate.mjs` | claims were assertions | TEST-001 … TEST-013 | LOW | tools run in CI-able form; exit codes defined | PASS |
| R-011 | DOC_CLEANUP | extent of DVB/future material unenforced | scope document + mechanical symbol checks | analogy could drift into compatibility claims | SCOPE-001, SCOPE-002 | LOW | `tools/verify.mjs` symbol scans | PASS |
| R-012 | DOC_CLEANUP | verification and change history undocumented | evidence register + claims + this change register | traceability of conclusions and edits | DOC-012 | LOW | `tools/verify.mjs` evidence lint | PASS |
| R-014 | DOC_REWRITE | status expressed as one collapsed word ("implemented"/"tested") | typed status fields, recorded once per claim: `claim_kind`, `implementation_state`, `test_state`, `evidence_level`, `verification_result` | the fields describe different things and must never be merged or substituted | DOC-011, DOC-012 | LOW | `tools/verify.mjs` vocabulary lint; `tools/validate-analysis.mjs` | PASS |
| R-015 | DOC_CLEANUP | scope, ownership and authorization implicit | [scope-and-authorization.md](scope-and-authorization.md) with the four scope dimensions, ownership matrix, decision ownership, authorization levels and pre/post-execution checks | governs who may decide and mutate | DOC-012 | LOW | `tools/verify.mjs` authorization-record lint | PASS |
| R-016 | DOC_CLEANUP | status existed only as prose tables; no machine-readable record, and no way to tell a stale table from a current one | [analysis.json](analysis.json) as the normative record, plus `tools/validate-analysis.mjs` (schema, enums, authorization/execution rules) and `tools/render-claims.mjs` (claims.md is generated, never hand-edited) | a canonical model that cannot be validated silently drifts | DOC-012 | LOW | `tools/validate-analysis.mjs`: JSON Schema + rules V1–V20 + invariants I-001–I-016; `tools/render-claims.mjs --check` | PASS |
| R-017 | DOC-REWRITE | claim and status statements written before the canonical model, in three-dimension or collapsed form | 41 records regenerated with all five typed fields; evidence register, analysis document, scope document, README and the 11 behaviour documents updated to the same vocabulary | documents must agree with the normative record or be detected | DOC-011, DOC-012 | LOW | `tools/verify.mjs` field-substitution and declaration lints; `node tools/verify.mjs` → 39 PASS / 0 FAIL | PASS |
| R-018 | DOC_CLEANUP | claim validity was structural only, the authorization object used a single level with extra capabilities beside it, and the YAML rendering had no enforced connection to the record | claim-kind and cross-dimension rules (`C-001…C-043`; renumbered to the canonical `CV-001…CV-020` matrix by R-019), canonical authorization fields with explicit operation sets and intersection semantics (`EffectiveOperations = Ops(level) ∩ operations`), no-inheritance enforcement, a second canonical grant for publication, and a YAML mirror checked by `SER-001…SER-012` | structure does not make a claim semantically valid, and a level name must not imply an operation | DOC-013, DOC-014 | LOW | `tools/validate-analysis.mjs` (14 checks); `tools/verify.mjs` (39 PASS / 0 FAIL) | PASS |
| R-020 | DOC_REWRITE | an unqualified `verification` object did not say which object was being verified; capabilities were names in a flat list without their own state or resource class; per-operation authorization decisions were not recorded; and execution verification reused the claim vocabulary | two named domains — `claim_verification` (claims) and `execution_verification` (resulting repository state) — with `VERIFIED` and `CONFORMING` reserved to their own domains; 21 capability objects with `state` and `resource_class`; per-operation `authorization_decision`; rule sets `AC-001…AC-016` and `EVV-001…EVV-009`; capability-restricted grants (three, including the disclosed `R-001` extraction grant) | `docs/analysis/analysis.schema.json`, `docs/analysis/analysis.json`, `docs/analysis/authorization.yaml`, `tools/validate-analysis.mjs`, `docs/analysis/scope-and-authorization.md`, `tools/verify.mjs` |
| R-019 | DOC_REWRITE | the authorization object treated a level as an operation set, and execution and post-verification each carried a single ambiguous result | level profiles with declared `inherits`, capability sets with `allow`/`deny` restriction, operation resolution from capabilities, scope paths, per-operation execution results, and a post-verification lifecycle with its own state, result and check results; claim `confidence` added as a graded dimension | a profile name must not imply a capability, an inherited capability must be removable, and an execution result must not imply a verification result | DOC-013, DOC-014 | MEDIUM | `tools/validate-analysis.mjs` (19 checks); `tools/verify.mjs` (43 PASS / 0 FAIL) | PASS |
| R-013 | RENAME | `Continue Architecture Planning.md` at root implied a normative planning document | archived under `archive/`, indexed | non-normative status unclear | DOC-003, DOC-006 | LOW | link checks | PASS |

No content was deleted. Removed text was either contradicted by the
implementation, duplicated in a canonical document, or conversational filler;
each case is recorded in the analysis's duplication map and contradiction report.

## Executed changes — code

**None.** The artifact is byte-identical to the extraction of transcript
L48948–L54113. It was verified, not modified.

| ID | Category | Target | Note |
| --- | --- | --- | --- |
| — | — | `prototype/generic-discovery-engine.user.js` | extraction only; no edit, no reformat, no repair |

```
CHANGE:   (none)
Before:   artifact as extracted from archive L48948-L54113
After:    identical
Reason:   code changes were not authorized (the ceiling is DOC_REFACTOR; CODE_REFACTOR and ARCHITECTURE_CHANGE were never granted)
Evidence: [EVID:CODE-001], frozen digest in the evidence register
Verification: SHA-256 8f5fc5c5…e354c474 unchanged since commit 400810d,
              recomputed and enforced by tools/verify.mjs
```

An earlier note in the transcript claimed both pasted scripts contained stray
backtick delimiters; that was checked and is false for v0.7.1 (the file parses).
Consequently no repair was performed — a change that would otherwise have been
"obviously correct" was skipped because the evidence disproved the premise.

## Proposed changes — code (PLAN ONLY, not executed)

Ordered by priority. Each references verification evidence and carries a risk
class. **None of these has been applied.**

| ID | Category | Current | Proposed | Reason | Evidence | Risk | Priority |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R-101 | CODE-FIX | `queueCandidate()` re-queues candidates in `claimed`/`planned`/`acquiring`/`observed` | refuse re-queue for any non-terminal state, or model re-proposed work as work | breaks the stated ownership invariant; duplicate acquisition | CONC-002, TEST-009, TEST-011 | **ARCHITECTURAL** | P0 |
| R-102 | CODE-FIX | `shouldAcquireResource()` is checked before the request completes | bind the guard to the ownership transition (single decision point) | both in-flight owners pass the guard | TEST-011 | **ARCHITECTURAL** | P0 |
| R-103 | CODE-FIX | `failed` is claimable and carries no backoff | terminal or backoff-gated failure | budget consumed by dead targets | CONC-004, FAIL-001 | HIGH | P0 |
| R-104 | CODE-FIX | worker exits permanently when no candidate is eligible | keep workers alive until a scan-level stop condition, or respawn on new work | effective concurrency collapses; work stranded | CONC-003, TEST-010 | HIGH | P0 |
| R-105 | TEST-ADD | no pass/fail gate for the single-owner invariant | assert "at most one concurrent owner" and fail on violation | regression protection for R-101/R-102 | TEST-009 | LOW | P0 |
| R-106 | CODE-FIX | `running` stays true after a scan drains; `Scan` becomes a no-op | explicit scan states (idle / running / quiescent / exhausted / stopped) | control plane misreports state | TEST-010 | MEDIUM | P1 |
| R-107 | CODE-FIX | every recognition stores a `Discovery`, even for known URLs | deduplicate, or store corroboration as provenance | discovery counts overstate the frontier | PROV-003, TEST-012 | MEDIUM | P1 |
| R-108 | CODE-FIX | `fingerprintIndex` is written but never read | consult it for content identity, or delete it | dead evidence invites false assumptions | PROV-002, CODE-023 | MEDIUM | P1 |
| R-109 | CODE-FIX | `stats.acquired` never incremented | maintain or remove the counter | reporting accuracy | CODE-030 | LOW | P2 |
| R-110 | CODE-REFACTOR | adaptive counters never resize the pool | drive the pool from the counter, or delete the feature | inert control plane | CODE-018, CODE-029 | MEDIUM | P2 |
| R-111 | CODE-REFACTOR | acquisition transport hard-wired to HTTP GET | introduce an acquisition-provider boundary | enables v0.9/v0.10 designs | SCOPE-003, ARCH-002 | **ARCHITECTURAL** | P3 |
| R-112 | ARCHITECTURE-CHANGE | no scan-level termination evaluator | define and persist scan states with a termination criterion | prerequisite for any coverage claim | DOC-006, SCOPE-006 | **ARCHITECTURAL** | P3 |

Gate required before executing any of R-101 … R-112:

```
proposal → evidence → impact → user-approved execution boundary → change → post-verify
```

No code change should be attempted while R-101 … R-104 are open, because the
later architectural layers (leases, work items, coverage) would inherit an
unsound ownership baseline.

## Change-set boundary and discovered changes

Authorization covered `R-001 … R-020` (`change_ids` in the authorization object;
`R-014 … R-017` extended the set within the same `DOC_REFACTOR` ceiling — all
documentation/analysis artifacts). While executing,
twelve further problems were discovered (`R-101 … R-112`). Under the
discovered-change rule they were recorded, classified and proposed, **not
fixed** — including `R-109`, a two-line counter fix, because code mutation was
outside the authorized scope.

One proposed change was dropped after evidence contradicted its premise: the
archive claimed the pasted scripts contained stray backtick delimiters, which is
false for v0.7.1. No repair was made.

## Post-refactor verification

Applied to the executed documentation changes. Procedure: `node tools/verify.mjs`,
`node tools/checks.mjs`, `node tools/simulate.mjs`, plus the checklist below.

| Check | Result | Evidence |
| --- | --- | --- |
| original invariant still holds (code untouched) | PASS — artifact byte-identical to extraction | `node --check`; `tools/verify.mjs` parse + version |
| references remain valid | PASS — every `[EVID:…]` citation resolves to a register row | evidence lint in `tools/verify.mjs` |
| links remain valid | PASS — 16 documents scanned, 0 broken relative links | `tools/verify.mjs` |
| documentation matches implementation | PASS — 19 static checks pass; 4 defects are documented, not hidden | `tools/verify.mjs` |
| moved content was not lost | PASS — archive retained; design series summarised with version map | `archive/README.md`; roadmap document |
| duplicated content actually removed | PASS — one canonical owner per concept (analysis §6) | duplication map |
| terminology remains consistent | PASS — glossary is the single authority; conflicts tabulated | `docs/glossary.md` |
| tests still pass where applicable | PASS — `checks.mjs` 4/4; `simulate.mjs` reproduces D1/D2/D4/D9 by design | tool output |
| structure matches the proposed structure | PASS — analysis §13 matches the tree | `find` output |
| no new contradictions introduced | PASS — contradictions are recorded as CONFLICT 1–10 and CONC/FAIL/ARCH entries | analysis §5, evidence register |
| claims are traceable to evidence | PASS — every conclusion in the analysis cites register IDs | analysis §2, §3, §8–§12 |

Known limitations of this verification:

* the harness shim is not a browser: DOM parsing is stubbed, so `HtmlProvider`
  behaviour is verified statically (code) and by matching rules, not end-to-end;
* randomness exists only in response delays; ordering effects are therefore
  representative but not exhaustive;
* `tools/simulate.mjs` deliberately reports failing invariant checks — that is a
  measurement of the prototype, not of the tooling.

## Refactoring result

```yaml
execution:                          # what happened, per operation
  state: SUCCEEDED
  operations: 21 recorded, every authorization_decision ALLOWED, every result SUCCEEDED
  executed_changes: [R-001 .. R-020]
  unauthorized_changes: []
execution_verification:             # whether the resulting state conforms
  state: PASSED
  result: CONFORMING
  checks: 8, every result PASSED
  mutations: []
```

**EXECUTED + EXECUTION-VERIFIED**: documentation and analysis artifacts
`R-001 … R-020`.

**PLAN ONLY**: code changes `R-101 … R-112` — no authorization was given to
change runtime behaviour (`CAP-SOURCE-MODIFY|RENAME|MOVE|DELETE`, every
`CAP-TEST-*` and `CAP-ARCHITECTURE-MODIFY` are withheld capability classes,
unreachable through any grant), and correctness must be established before the
prototype is modified.

```yaml
AUTHORIZATION (as applied)  # five separate objects, each with its own field
  content grant:
    state: GRANTED
    level: {profile: DOC_REFACTOR}     # policy ceiling only
    capabilities:
      mode: RESTRICT
      grants:                        # capability objects, each with a state
        - {id: CAP-REPOSITORY-READ, state: ENABLED, resource_class: REPOSITORY, operations: [READ]}
        - {id: CAP-REPOSITORY-ANALYZE, state: ENABLED, resource_class: REPOSITORY, operations: [ANALYZE]}
        - {id: CAP-REPOSITORY-PROPOSE, state: ENABLED, resource_class: REPOSITORY, operations: [PROPOSE]}
        - {id: CAP-DOCUMENT-CREATE, state: RESTRICTED, constraints: {paths: {include: [docs/, tools/]}}}
        - {id: CAP-DOCUMENT-MODIFY, state: RESTRICTED, constraints: {paths: {include: [README.md, docs/, tools/]}}}
        - {id: CAP-DOCUMENT-RENAME, state: RESTRICTED, constraints: {paths: {include: [archive/]}}}
        - {id: CAP-DOCUMENT-MOVE, state: RESTRICTED, constraints: {paths: {include: [docs/roadmap/, archive/]}}}
      denies:
        - {id: CAP-DOCUMENT-DELETE, state: DENIED, resource_class: DOCUMENT, operations: [DELETE]}
    operations: {allow: [READ, ANALYZE, PROPOSE, CREATE, MODIFY, RENAME, MOVE], deny: [DELETE]}
  extraction grant:                    # disclosed: OP-001 created the artifact file
    state: GRANTED
    level: {profile: CODE_REFACTOR}
    capabilities: {mode: RESTRICT, grants: [{id: CAP-SOURCE-CREATE, state: RESTRICTED,
                    constraints: {paths: {include: [prototype/]}}}], denies: []}
    operations: {allow: [CREATE], deny: [MODIFY, RENAME, MOVE, DELETE, COMMIT, PUSH]}
    change_ids: [R-001]
  publication grant:
    state: GRANTED
    level: {profile: PUSH}
    capabilities:
      mode: RESTRICT
      grants: [CAP-REPOSITORY-READ, CAP-REPOSITORY-ANALYZE, CAP-REPOSITORY-PROPOSE,
               CAP-COMMIT-CREATE, CAP-REMOTE-PUSH]
      denies: 16 inherited content capabilities
    operations: {allow: [READ, ANALYZE, PROPOSE, COMMIT, PUSH], deny: [CREATE, MODIFY, RENAME, MOVE, DELETE]}
```

Category vocabulary: the change categories follow the canonical enum
(`DOC_CLEANUP`, `DOC_MOVE`, `DOC_MERGE`, `DOC_SPLIT`, `DOC_REWRITE`,
`CODE_REFACTOR`, `CODE_FIX`, `TEST_ADD`, `TEST_UPDATE`, `ARCHITECTURE_CHANGE`,
`REMOVAL`, `RENAME`). The earlier `DOC_ADD` label is not part of that enum, so
those rows were reclassified by their effect — consolidation (`R-003`),
terminology and governance cleanup (`R-009`, `R-011`, `R-012`, `R-015`, `R-016`),
verification tooling (`R-010`) and status-vocabulary replacement (`R-014`,
`R-017`) — with no change to what was actually done.

## Two-state architecture record

| | VERIFIED CURRENT STATE | PROPOSED TARGET STATE |
| --- | --- | --- |
| Candidate ownership | atomic claim, violated end to end (D1) | single owner end to end, enforced by tests (R-101, R-102, R-105) |
| Failure semantics | `failed` claimable without backoff (D3) | terminal or backoff-gated failure (R-103) |
| Worker pool | created once, never refilled (D2) | alive until a scan-level stop condition (R-104, R-112) |
| Run state | `running` latch, no completion criterion (D4) | explicit states incl. quiescence and exhaustion (R-106) |
| Discovery accounting | one record per recognition (D9) | deduplicated or provenance-backed corroboration (R-107) |
| Status vocabulary | one word per verdict ("implemented", "tested") | six typed claim fields, recorded once in analysis.json and rendered into claims.md (R-014) |
| Governance | implicit scope and ownership | explicit scope boundary, authorization contract, pre/post-execution checks (R-015) |
| Content identity | fingerprints indexed, unused (D8) | consulted or removed (R-108) |
| Acquisition | HTTP GET hard-wired | acquisition-provider boundary (R-111) — v0.9/v0.10 design |
| Coverage/absence | not represented | DESIGNED v0.22/v0.23, not scheduled until ownership is fixed |

The two columns are never to be merged into a single architecture diagram
without labels; the verified column is what `README.md` describes today.
