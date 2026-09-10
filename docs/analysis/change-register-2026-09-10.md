# Change Register — 2026-09-10

Separation of responsibilities required by the analysis controls: **verification
established what is true; this document records what was changed, what is merely
proposed, and how each change was verified afterwards.**

| Phase | State | Boundary |
| --- | --- | --- |
| A — Verification (read-only) | complete | produced the [evidence register](evidence-register.md) and the [analysis](repository-analysis-2026-09-10.md); **no repository state was modified during verification** |
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
| R-009 | DOC-ADD | no terminology authority | `docs/glossary.md` with definitions, conflicting usages, canonical usage and corrected documents | inconsistent vocabulary | DOC-011 | LOW | consistency review across `docs/` | PASS |
| R-010 | DOC-ADD | no executable verification existed | `tools/verify.mjs`, `tools/checks.mjs`, `tools/simulate.mjs` | claims were assertions | TEST-001 … TEST-013 | LOW | tools run in CI-able form; exit codes defined | PASS |
| R-011 | DOC-ADD | extent of DVB/future material unenforced | scope document + mechanical symbol checks | analogy could drift into compatibility claims | SCOPE-001, SCOPE-002 | LOW | `tools/verify.mjs` symbol scans | PASS |
| R-012 | DOC-ADD | verification and change history undocumented | evidence register + this change register | traceability of conclusions and edits | DOC-012 | LOW | `tools/verify.mjs` evidence lint | PASS |
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

**EXECUTED + POST-VERIFIED** for documentation changes R-001 … R-013.

**PLAN ONLY** for code changes R-101 … R-112: no authorization was given to
change runtime behaviour, and correctness must be established before the
prototype is modified.

## Two-state architecture record

| | VERIFIED CURRENT STATE | PROPOSED TARGET STATE |
| --- | --- | --- |
| Candidate ownership | atomic claim, violated end to end (D1) | single owner end to end, enforced by tests (R-101, R-102, R-105) |
| Failure semantics | `failed` claimable without backoff (D3) | terminal or backoff-gated failure (R-103) |
| Worker pool | created once, never refilled (D2) | alive until a scan-level stop condition (R-104, R-112) |
| Run state | `running` latch, no completion criterion (D4) | explicit states incl. quiescence and exhaustion (R-106) |
| Discovery accounting | one record per recognition (D9) | deduplicated or provenance-backed corroboration (R-107) |
| Content identity | fingerprints indexed, unused (D8) | consulted or removed (R-108) |
| Acquisition | HTTP GET hard-wired | acquisition-provider boundary (R-111) — v0.9/v0.10 design |
| Coverage/absence | not represented | DESIGNED v0.22/v0.23, not scheduled until ownership is fixed |

The two columns are never to be merged into a single architecture diagram
without labels; the verified column is what `README.md` describes today.
