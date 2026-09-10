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
| TEST CHANGES | forbidden; adding verification tooling was authorized as documentation/analysis work (`ANALYSIS_ONLY` + `DOC_REFACTOR`) |
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

## 3. Ownership roles

Exactly six roles. One actor may hold several roles, but the roles stay distinct,
and technical access never implies authorization.

| Role | Holder here | Responsibilities | Constraints |
| --- | --- | --- | --- |
| `REPOSITORY_OWNER` | `Abdus2023` | repository authority, scope authority, architectural ownership, delegation of execution authority | may delegate authorization, but ownership of the repository is never transferred by doing so |
| `ANALYZER` | this analysis | inspection, evidence extraction, interpretation, verification analysis, contradiction and duplication detection, refactoring proposals | must not mutate the target repository merely because it has technical access; may produce analysis artifacts inside it when authorized (here: `ANALYSIS_ONLY`) |
| `REVIEWER` | repository owner / reviewer | reviews evidence, verification conclusions, refactoring proposals, risk and scope | carries no mutation authority by virtue of reviewing |
| `AUTHORIZER` | repository owner, delegating through the user's instruction | grants mutation permission, scoped and explicit | must hold authority delegated by the repository owner; authorization is never inferred from capability or from phrasing such as "clean this up" |
| `EXECUTOR` | the same agent, **explicitly entering the EXECUTOR role** for the authorized change set only | performs the authorized mutations | must follow the approved change set, respect scope and forbidden operations, stop at any boundary violation, and report changes |
| `VERIFIER` | this analysis, re-running the tools after execution | determines whether the result satisfies the requested postconditions | must not silently repair a failed verification; it reports `FAILED`/`PARTIALLY_VERIFIED` instead |

Role-entry statement required by the ownership rule: the analyzer became the
executor **only** for change set `R-001 … R-017` (documentation and analysis
artifacts), under the authorization recorded in §5. For `R-101 … R-112` (code) the
analyzer remained `ANALYZER` and produced proposals only.

## 4. Decision ownership

| Kind | Example from this analysis | Owner |
| --- | --- | --- |
| FACT | "the prototype has seven recognition providers" | established by analysis from evidence; not a decision |
| INTERPRETATION | "the provider abstraction is deliberately pure, which is why it is replaceable" | analysis (labelled as interpretation) |
| DESIGN DECISION | "introduce a protocol-neutral acquisition provider; treat re-proposed work as work rather than candidate state" | repository owner — proposed, not taken |
| EXECUTION DECISION | "modify `queueCandidate()` now" | repository owner authorizes; analysis recommends, and did **not** execute (`R-101`, plan only) |
| DOCUMENTATION DECISION | "split the archive into code + roadmap + history" | analysis executed under the authorization for documentation refactoring |

## 5. Execution authorization model

Authorization is **two separate concepts**, never one word.

| Field | Question it answers | Canonical values |
| --- | --- | --- |
| `authorization.state` | *Has mutation authority actually been granted?* | `NOT_REQUESTED` · `REQUESTED` · `DENIED` · `GRANTED` · `REVOKED` · `EXPIRED` |
| `authorization.level` | *If authorization exists, what operations does it permit?* | `READ_ONLY` · `ANALYSIS_ONLY` · `DOC_REFACTOR` · `TEST_REFACTOR` · `CODE_REFACTOR` · `ARCHITECTURE_CHANGE` · `COMMIT` · `PUSH` |

`state: GRANTED` does not by itself say what may be changed, and
`level: CODE_REFACTOR` does not prove that anything was granted. The default,
with no explicit authorization, is `state: NOT_REQUESTED` with
`level: READ_ONLY` — inspect, search, analyze, verify and propose only.

Valid and invalid combinations (§98):

| Combination | Verdict |
| --- | --- |
| `NOT_REQUESTED` + `READ_ONLY` | valid |
| `DENIED` + `READ_ONLY` | valid |
| `GRANTED` + `DOC_REFACTOR` | valid |
| `GRANTED` + no level | invalid — a grant must state what it permits |
| `REVOKED` + `CODE_REFACTOR` + a later `execution.result: SUCCEEDED` | invalid — revocation prevents subsequent execution |

### The authorization object as applied

```yaml
authorization:
  state: GRANTED
  authority:
    type: USER
    identifier: "Abdus2023 (repository owner), delegating through the standing session instruction"
  target:
    repository: "Abdus2023/Generic-Discovery-Engine"
    revision: "cc8df7357c2dbfe9d149747743e2f5e9ac9c0178 (work branch: arena/01a08d14-generic-discovery-engine)"
  level: DOC_REFACTOR              # capability ceiling for content mutation
  additional_levels_declared: [ANALYSIS_ONLY, COMMIT, PUSH]
  hierarchical: false              # nothing is inherited
  change_ids: [R-001 … R-017]
  operations: [READ, ANALYZE, PROPOSE, CREATE, MODIFY, MOVE, RENAME, COMMIT, PUSH]
  forbidden_operations: [MODIFY_SOURCE_CODE, MODIFY_TESTS, DELETE, ARCHITECTURE_CHANGE, PUSH_TO_OTHER_BRANCH]
  expires_at: null
  granted_at: "2026-09-10"
```

This object **is** the mutation boundary: a change is permitted only if it
appears in `change_ids` and the operation it needs appears in `operations`.

### Capability ceiling, not inheritance (§100)

`DOC_REFACTOR` permits documentation operations only. It does **not** imply
`TEST_REFACTOR`, `CODE_REFACTOR`, `ARCHITECTURE_CHANGE`, `COMMIT` or `PUSH`. In
this work `COMMIT` and `PUSH` were granted explicitly and are therefore recorded
in `operations` and in `additional_levels_declared`; because
`hierarchical: false`, no capability is assumed from any other level. The code
changes `R-101 … R-112` sit outside the ceiling entirely and were not executed.

### The check applied before each mutation (§101)

```
requested operation
        ↓
authorization.state == GRANTED ?
        ↓
authorization target matches repository ?
        ↓
operation allowed by authorization.operations ?
        ↓
change ID present in authorization.change_ids ?
        ↓
authorization not expired / revoked ?
        ↓
EXECUTE          otherwise → DO NOT MUTATE
```

Rules `V8`–`V15` encode this mechanically and `tools/validate-analysis.mjs`
evaluates them against the record. Invariants `I-007`/`I-008` keep the state and
the level distinct; `I-010`/`I-011` keep access, authorization and execution
distinct.

### Change-set boundary

Authorization covered `R-001 … R-017`. During execution, twelve further problems
were discovered (`R-101 … R-112`, including the P0 ownership defects). Per the
change-set rule they were **recorded and proposed, not fixed** — even though one
(`R-109`, the dead counter) would have been a two-line edit. They remain
`PLAN ONLY` and outside `change_ids`.

### Discovered-change rule — worked example

```
Approved:      documentation refactor (R-001 … R-017)
Discovered:    candidate re-queue violates the ownership invariant (D1)
Action:        record finding (CONC-CLAIM-002) → classify (BUG, ARCHITECTURAL)
               → add proposed change R-101 → request authorization
Result:        NOT EXECUTED. No scope creep. (I-016)
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
Required decision:   owner decides whether to authorize CODE_REFACTOR /
                     ARCHITECTURE_CHANGE work on the ownership and control-plane defects.
```

## 6. Pre-execution and post-execution checks

**Pre-execution** (recorded before the first documentation change):

| Check | Result |
| --- | --- |
| Repository target confirmed | yes — `Abdus2023/Generic-Discovery-Engine` |
| Revision confirmed | yes — `cc8df73` |
| Scope confirmed | yes — four dimensions above |
| Authorization state confirmed | yes — `GRANTED` |
| Authorization level confirmed | yes — `DOC_REFACTOR` ceiling, with `ANALYSIS_ONLY`, `COMMIT` and `PUSH` declared separately (`hierarchical: false`) |
| Allowed / forbidden operations confirmed | yes |
| Change set identified | yes — `R-001 … R-017` in `change_ids` |
| Verification completed | yes — evidence + claims + analysis |
| Evidence references available | yes — the register resolves every cited id |
| Rollback understood | yes — git history on the work branch |

```
EXECUTION STATUS: AUTHORIZED
```

**Post-execution:**

| Check | Result |
| --- | --- |
| Requested changes completed | yes — `R-001 … R-017` |
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

```yaml
execution:
  result: SUCCEEDED                 # from the canonical enum
  executed_changes: [R-001 .. R-017]
  unauthorized_changes: []
  discovered_not_executed: [R-101 .. R-112]

post_verification:
  result: VERIFIED                  # reuses the verification enum; no separate PASS/FAIL vocabulary
  evidence:
    - tools/verify.mjs: 38 passed, 0 failed, 4 documented defects
    - tools/checks.mjs: 4 passed, 0 failed
    - tools/validate-analysis.mjs: 10 checks (JSON Schema, rules V1-V20, invariants I-001-I-016, restated fields)
    - artifact digest unchanged (sha256 8f5fc5c5...)
  not_verified:
    - end-to-end HtmlProvider behaviour under a real DOM (SCOPE-GAP-1, OPEN)
    - real userscript-manager semantics (SCOPE-GAP-2, OPEN)
```

## 7. Ownership and authorization matrix

| Operation | Analysis | User / owner | Execution agent |
| --- | --- | --- | --- |
| Inspect | yes | yes | yes |
| Analyze | yes | yes | optional |
| Recommend | yes | yes | no |
| Approve | no | **yes** | no |
| Modify documentation | only if authorized (was: yes, `DOC_REFACTOR`) | yes | yes |
| Modify code | only if authorized (**not** granted) | yes | yes |
| Delete | only if authorized (not granted; nothing deleted) | yes | yes |
| Commit | only if authorized (yes, `COMMIT` declared separately) | yes | yes |
| Push | only if explicitly authorized (yes, `PUSH` on the work branch) | yes | yes |
| Final verification (`VERIFIER`) | yes | optional | no |

Role identifier per operation, first two columns only — the analyzer and the
executor are the same actor holding different roles, which is why the role
boundary is stated explicitly rather than assumed.

## 8. Final governance model as applied

The **claim** side and the **execution authority** side are independent; no
field appears in both.

```
CLAIM                                  AUTHORIZATION
  │                                       │
  ├── claim_kind                   ┌──────┴───────┐
  ├── implementation_state         ▼              ▼
  ├── test_state            authorization    authorization
  │                            state            level
  ├── evidence_level               │              │
  │                                └──────┬───────┘
  └── verification_result                 ▼
                                    change_ids / operations
                                          │
                                          ▼
                                      EXECUTION
                                          │
                                          ▼
                                   execution_result
                                          │
                                          ▼
                                   POST-VERIFICATION
                                    (reuses verification_result)
```

Applied end to end:

```
REPOSITORY  (full access, resolved revision cc8df73)
     ↓
ACCESS BOUNDARY      FULL ACCESS; no fallback source used (I-010)
     ↓
SCOPE BOUNDARY       repository / artifact / verification / execution
     ↓
EVIDENCE EXTRACTION  the register resolves every cited id; evidence objects carry path + locator
     ↓
VERIFICATION         read-only; 41 claim records with five typed fields
     ↓
VERIFIED TRUTH SET   what exists, what is planned, what is absent, what is contradicted
     ↓
REFACTORING PLAN     R-001…R-017 executed; R-101…R-112 plan only
     ↓
AUTHORIZATION CHECK  state GRANTED; level DOC_REFACTOR; COMMIT/PUSH declared separately (I-011)
     ↓
EXECUTE (docs only)  → POST-VERIFY (independent, I-012) → execution_result SUCCEEDED,
                        post_verification VERIFIED
```

Governing separation, preserved at every step: **evidence → claim → verification
→ proposal → authorization → execution → post-verification**. No stage
impersonates another; in particular, the documentation work never silently
acquired authority over runtime behaviour, and execution success was never
treated as post-verification success.
