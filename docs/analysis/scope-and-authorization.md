# Scope Boundary and Authorization

Governance record for the 2026-09-10 analysis. It states *what was in scope*,
*who owns what decision*, and *what mutation was authorized* — before any claim
or change in this repository is evaluated.

Companion documents: [evidence register](evidence-register.md) (evidence),
[claims](claims.md) (verdicts), [change register](change-register-2026-09-10.md)
(changes), [analysis](repository-analysis-2026-09-10.md) (report).

## 1. Scope boundary

### Repository scope

| Field | Value |
| --- | --- |
| Owner | `Abdus2023` |
| Repository | `Generic-Discovery-Engine` |
| Branch | `main` (verification target); work branch `arena/01a08d14-generic-discovery-engine` |
| Commit | `cc8df7357c2dbfe9d149747743e2f5e9ac9c0178` |
| Tag | none |
| Accessible paths | the entire tree: `README.md`, `Userscript Discovery Prototype.md`, `Continue Architecture Planning.md` at the analysis revision |
| Excluded paths | none |
| Access | FULL ACCESS |

Evidence from different branches, forks, commits or mirrors is **not** combined.
The one artifact extracted from the archive was verified by parse, version and
digest, so it is attributable to a specific revision of a specific file.

### Artifact scope

| Artifact | Classification | Used to establish repository facts |
| --- | --- | --- |
| `prototype/generic-discovery-engine.user.js` | SOURCE | yes — primary evidence |
| `Continue Architecture Planning.md` (embedded userscripts v0.3.0–v0.7.1) | SOURCE (historical revisions) | yes, for history only |
| `Continue Architecture Planning.md` (v0.8–v0.35 prose) | ROADMAP | yes, as evidence that these layers are *planned*, never that they exist |
| `Userscript Discovery Prototype.md` | RESEARCH | as the origin of the analogy; not as behavioural evidence |
| `README.md` (pre-cleanup) | DOCUMENTATION | yes — as a claim to test, not as evidence of behaviour |
| `archive/*` transcripts | HISTORY | context; quoted only with line locators |
| `docs/**` (this analysis) | DOCUMENTATION | derived; cites evidence rather than replacing it |
| `tools/*.mjs` | TEST (verification tooling) | yes — evidence when executed |
| DVB standards, external articles, tutorials | EXTERNAL REFERENCE | **not used**; no external source supports any repository fact here |
| `dist/`, build output, generated artifacts | GENERATED ARTIFACT | none exist |

Distinction enforced throughout: **repository evidence ≠ external evidence ≠
architectural reasoning.** Where reasoning appears (for example, why providers
should not schedule), it is labelled as interpretation, not evidence.

### Verification scope

**Included:** userscript implementation · candidate model and lifecycle ·
scheduler and claiming · concurrency · acquisition · recognition providers ·
persistence · export and UI · provenance records · scope and non-goals ·
prototype documentation · architecture documentation · roadmap labelling.

**Excluded:** external services and live sites · browser behaviour beyond the
shim (real DOM, real CORS, real storage quotas) · unavailable private
dependencies (none exist) · undocumented deployments · hardware (none present) ·
future architecture beyond confirming that it is not implemented · other
repositories, forks and mirrors.

Consequences of exclusion, stated so they cannot later appear as verified:

* browser-compatibility beyond the tested surface is **UNVERIFIED**;
* real-page HTML recognition is verified statically and by matching rules, not
  end-to-end, because the shim stubs `DOMParser`;
* ordering effects under real network jitter are **PARTIALLY_VERIFIED**;
* every v0.8+ layer is excluded from verification by construction.

### Execution scope (as authorized for this work)

| Operation | Status |
| --- | --- |
| READ | allowed |
| ANALYZE | allowed |
| PROPOSE | allowed |
| CREATE | allowed — documentation and verification tooling only |
| MODIFY | allowed — documentation and verification tooling only; **source code forbidden** |
| RENAME | allowed — documentation only (one archive move) |
| MOVE | allowed — documentation only |
| DELETE | forbidden (nothing was deleted) |
| CODE CHANGES | **forbidden** |
| TEST CHANGES | initially forbidden (no tests existed); adding verification tooling was authorized as `A1`/`A2` work |
| DOCUMENTATION CHANGES | allowed |
| COMMIT | allowed |
| PUSH | allowed |

The artifact was never modified; its digest is frozen in the evidence register
and enforced by `tools/verify.mjs`.

## 2. Scope escalation

Two gaps were found during verification. Neither was silently expanded; both are
reported in the required form.

**SCOPE GAP 1 — behaviour of `HtmlProvider` under a real DOM**

```
SCOPE GAP:            end-to-end HTML extraction behaviour
WHY REQUIRED:         the harness stub returns no nodes, so HTML discoveries were
                      verified by matching rules and by code, not by execution
PROPOSED EXPANSION:   run the artifact in a real browser (or a DOM implementation)
AUTHORIZATION:        required — not granted
STATUS:               OPEN (excluded from verification scope, and recorded as such)
```

**SCOPE GAP 2 — behaviour of `GM_xmlhttpRequest` in a real userscript manager**

```
SCOPE GAP:            real userscript-manager semantics (redirects, CORS, grants,
                      storage quotas, cross-tab storage)
WHY REQUIRED:         these determine whether the persistence and scope claims hold
                      outside the shim
PROPOSED EXPANSION:   manual test protocol in Tampermonkey/Violentmonkey
AUTHORIZATION:        required — not granted
STATUS:               OPEN
```

Both gaps are recorded as exclusions in the verification scope and in the
residual limitations of the change register. No claim depends on them.

## 3. Ownership boundary

| Responsibility | Owner |
| --- | --- |
| Repository contents | repository owner (`Abdus2023`) |
| Interpretation of evidence | analysis (this document set) |
| Verification conclusions | analysis |
| Acceptance or rejection of conclusions | repository owner / reviewer |
| Refactoring proposal | analysis |
| Authorization to mutate | repository owner / authorized user |
| Repository mutation (executed) | the agent acting under the authorization record below |
| Post-change verification | analysis (tools rerun; results recorded) |
| Commit and push authority | delegated by the user's instruction to work in this repository and branch |

The analysis does not treat technical capability as ownership. Every executed
change is listed in the change register with its authorization basis; every code
change is `PLAN ONLY`.

## 4. Decision ownership

| Kind | Example from this analysis | Owner |
| --- | --- | --- |
| FACT | "the prototype has seven recognition providers" | established by analysis from evidence; not a decision |
| INTERPRETATION | "the provider abstraction is deliberately pure, which is why it is replaceable" | analysis (labelled as interpretation) |
| DESIGN DECISION | "introduce a protocol-neutral acquisition provider; treat re-proposed work as work rather than candidate state" | repository owner — proposed, not taken |
| EXECUTION DECISION | "modify `queueCandidate()` now" | repository owner authorizes; analysis recommends, and did **not** execute (`R-101`, plan only) |
| DOCUMENTATION DECISION | "split the archive into code + roadmap + history" | analysis executed under the authorization for documentation refactoring |

## 5. Execution authorization contract

```
EXECUTION AUTHORIZATION

Target:                 Abdus2023/Generic-Discovery-Engine
Revision:               branch arena/01a08d14-generic-discovery-engine,
                        based on main @ cc8df73
Authorization level:    A0 (read/analyze)
                        + A1 (analysis artifacts: registers, analysis, tools)
                        + A2 (documentation refactor)
                        + A6/A7 (commit and push to the work branch, per the
                          user's standing instruction)
NOT granted:            A3 (test changes to an existing suite — none exists),
                        A4 (code refactor),
                        A5 (architectural change)

Allowed operations:     read · analyze · propose · create docs · create tools ·
                        move/rename docs · commit · push (work branch only)
Forbidden operations:   modify source code · modify behaviour · delete anything ·
                        alter the design series · push to `main` or any branch
                        other than the work branch

Change set (executed):  R-001 … R-013   (documentation, verification tooling)
Change set (plan only): R-101 … R-112   (code / architecture — NOT authorized)
Out-of-scope:           any runtime behaviour change, any test change to an
                        existing suite, any modification of archive contents

Precondition:           verification phase completed (read-only)
Postcondition:          post-refactor verification completed and recorded
Rollback:               documentation changes are ordinary git history on the
                        work branch; the artifact digest pins code state, so a
                        revert of commits 400810d/e8b9aec restores the prior
                        documentation without touching code
Authorization status:   AUTHORIZED for documentation and tooling;
                        NOT AUTHORIZED for code
```

### Change-set boundary

Authorization covered `R-001 … R-013` only. During execution, twelve further
problems were discovered (`R-101 … R-112`, including the P0 ownership defects).
Per the change-set rule they were **recorded and proposed, not fixed** — even
though several are trivially explained and one (`R-109`, the dead counter) would
have been a two-line edit. They remain `PLAN ONLY`.

### Discovered-change rule — worked example

```
Approved:      documentation refactor (R-001 … R-013)
Discovered:    candidate re-queue violates the ownership invariant (D1)
Action:        record finding (CONC-CLAIM-002) → classify (BUG, ARCHITECTURAL)
               → add proposed change R-101 → request authorization
Result:        NOT EXECUTED. No scope creep.
```

A second case shows the rule protecting against an *unnecessary* change: the
archive claimed the pasted scripts contained stray backtick delimiters. The
"obviously correct" repair was checked first, the premise proved false for
v0.7.1, and no edit was made.

### Stop conditions

```
STOP CONDITION
Observed:            none triggered.
Affected invariant:  single-owner invariant — known violated (D1) BEFORE execution,
                     recorded as a defect rather than "fixed" inside a
                     documentation change set.
Changes applied:     documentation only; artifact digest unchanged.
Remaining:           R-101 … R-112 (code), requiring separate authorization.
Required decision:   owner decides whether to authorize A4/A5 work on the
                     ownership and control-plane defects.
```

## 6. Pre-execution and post-execution checks

**Pre-execution** (recorded before the first documentation change):

| Check | Result |
| --- | --- |
| Repository target confirmed | yes — `Abdus2023/Generic-Discovery-Engine` |
| Revision confirmed | yes — `cc8df73` |
| Scope confirmed | yes — four dimensions above |
| Authorization level confirmed | yes — A1/A2 + A6/A7 on the work branch |
| Allowed / forbidden operations confirmed | yes |
| Change set identified | yes — `R-001 … R-013` |
| Verification completed | yes — evidence + claims + analysis |
| Evidence references available | yes — 66 evidence rows |
| Rollback understood | yes — git history on the work branch |

```
EXECUTION STATUS: AUTHORIZED
```

**Post-execution:**

| Check | Result |
| --- | --- |
| Requested changes completed | yes — `R-001 … R-013` |
| No unauthorized changes made | yes — artifact digest identical to extraction; no code or test changes |
| Repository structure valid | yes — matches the proposed structure |
| Links valid | yes — 20+ documents, zero broken relative links |
| References valid | yes — evidence/claim citations resolve |
| Documentation consistent | yes — 22 static checks pass |
| Code unchanged (out of scope) | **yes — SHA-256 unchanged** |
| Tests unchanged (out of scope) | yes — no test suite existed to change |
| Required tests executed | yes — `verify.mjs`, `checks.mjs`, `simulate.mjs` |
| Critical invariants reverified | yes — ownership invariant measured and reported as violated (unchanged, as expected) |
| New contradictions absent | yes — none introduced; ten recorded instead |

```
EXECUTION RESULT:  SUCCESS (documentation scope)
POST-VERIFICATION: VERIFIED (documentation) / code findings UNCHANGED by design
```

## 7. Ownership and authorization matrix

| Operation | Analysis | User / owner | Execution agent |
| --- | --- | --- | --- |
| Inspect | yes | yes | yes |
| Analyze | yes | yes | optional |
| Recommend | yes | yes | no |
| Approve | no | **yes** | no |
| Modify documentation | only if authorized (was: yes, A2) | yes | yes |
| Modify code | only if authorized (**not** granted) | yes | yes |
| Delete | only if authorized (not granted; nothing deleted) | yes | yes |
| Commit | only if authorized (yes, A6) | yes | yes |
| Push | only if explicitly authorized (yes, work branch) | yes | yes |
| Final verification | yes | optional | no |

## 8. Final governance model as applied

```
REPOSITORY  (full access, main @ cc8df73)
     ↓
ACCESS BOUNDARY      FULL ACCESS; no fallback source used
     ↓
SCOPE BOUNDARY       repository / artifact / verification / execution
     ↓
EVIDENCE EXTRACTION  66 evidence rows with locators and evidence states
     ↓
VERIFICATION         read-only; claims table with three status dimensions
     ↓
VERIFIED TRUTH SET   what exists, what is planned, what is absent, what is contradicted
     ↓
REFACTORING PLAN     R-001…R-013 executed; R-101…R-112 plan only
     ↓
AUTHORIZATION CHECK  A1/A2 + A6/A7 granted; A4/A5 NOT granted
     ↓
EXECUTE (docs only)  → POST-VERIFY → RESULT: SUCCESS / VERIFIED
```

Governing separation, preserved at every step: **evidence → claim → verification
→ proposal → authorization → execution → post-verification**. No stage
impersonates another; in particular, the documentation work never silently
acquired authority over runtime behaviour.
