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
| READ | allowed (`REPOSITORY_READ` → READ) |
| ANALYZE | allowed (`ANALYSIS_EXECUTE` → ANALYZE) |
| PROPOSE | allowed (`PROPOSAL_CREATE` → PROPOSE) |
| CREATE | allowed — documentation and verification tooling only (`DOCUMENT_CREATE` → CREATE, documentation) |
| MODIFY | allowed — documentation and verification tooling only (`DOCUMENT_MODIFY`); **source code has no capability** |
| RENAME | allowed — documentation only (`DOCUMENT_RENAME`; one archive move) |
| MOVE | allowed — documentation only (`DOCUMENT_MOVE`) |
| DELETE | denied at both layers (`DOCUMENT_DELETE` in `capabilities.deny`, `DELETE` in `operations.deny`); nothing was deleted — the two transcripts are recorded by git as 100 %-similar renames (`R100`), not as deletions |
| CODE CHANGES | **no capability exists** — `CODE_*` is a withheld class, unreachable through either grant |
| TEST CHANGES | **no capability exists** — `TEST_*` is a withheld class; adding the verification tooling was documentation/analysis work, not test-suite modification |
| DOCUMENTATION CHANGES | allowed up to the capability ceiling, and narrowed by the explicit allow list |
| COMMIT | allowed by the publication grant only (`COMMIT_CREATE`) |
| PUSH | allowed by the publication grant only (`PUSH_EXECUTE`, work branch) |

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
executor **only** for change set `R-001 … R-018` (documentation and analysis
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

## 5. Authorization model

Authorization is resolved in layers. They are different objects, and none of
them may stand in for another:

```
LEVEL PROFILE  →  CAPABILITY SET  →  OPERATION AUTHORIZATION  →  CHANGE
 (policy ceiling)   (atomic permits)     (what may be done)         (to what)
```

| Concept | Field | Question |
| --- | --- | --- |
| Authorization state | `authorization.state` | Has mutation authority actually been granted? |
| Level profile | `authorization.level.profile` | Which named policy ceiling applies? |
| Capability set | `authorization.capabilities` | Which atomic permissions survive that ceiling? |
| Operations | `authorization.operations` | Which execution-level operations do they imply here? |
| Scope | `authorization.scope` | Which paths and resources are in play? |
| Change authorization | `authorization.change_ids` | Which change records are covered? |

States: `NOT_REQUESTED` · `REQUESTED` · `DENIED` · `GRANTED` · `REVOKED` ·
`EXPIRED`. **Only `GRANTED` permits mutation.** A profile is a ceiling, never an
authority: `DOC_REFACTOR` on a grant says what *could* be permitted at most, not
what the user granted.

### Capabilities are atomic; operations are the execution abstraction

| Capability group | Members |
| --- | --- |
| Repository | `REPOSITORY_READ` · `ANALYSIS_EXECUTE` · `PROPOSAL_CREATE` |
| Documentation | `DOCUMENT_CREATE` · `DOCUMENT_MODIFY` · `DOCUMENT_RENAME` · `DOCUMENT_MOVE` · `DOCUMENT_DELETE` |
| Tests | `TEST_CREATE` · `TEST_MODIFY` · `TEST_RENAME` · `TEST_MOVE` · `TEST_DELETE` |
| Source code | `CODE_CREATE` · `CODE_MODIFY` · `CODE_RENAME` · `CODE_MOVE` · `CODE_DELETE` |
| Architecture | `ARCHITECTURE_MODIFY` |
| Publication | `COMMIT_CREATE` · `PUSH_EXECUTE` |

A capability authorizes one operation against one resource class
(`capability_operations` in [analysis.schema.json](analysis.schema.json)). For
example `DOCUMENT_MODIFY` permits `MODIFY` against documentation — not against
arbitrary source code. Capabilities are deliberately finer-grained than profiles,
and profiles never differ only by their names.

### Inheritance is declared, never inferred

```yaml
READ_ONLY:           capabilities: [REPOSITORY_READ]
ANALYSIS_ONLY:       inherits READ_ONLY             + [ANALYSIS_EXECUTE, PROPOSAL_CREATE]
DOC_REFACTOR:        inherits ANALYSIS_ONLY         + [DOCUMENT_*]
TEST_REFACTOR:       inherits ANALYSIS_ONLY         + [TEST_*]
CODE_REFACTOR:       inherits ANALYSIS_ONLY         + [CODE_*]
ARCHITECTURE_CHANGE: inherits CODE_REFACTOR, DOC_REFACTOR, TEST_REFACTOR + [ARCHITECTURE_MODIFY]
COMMIT:              inherits ARCHITECTURE_CHANGE   + [COMMIT_CREATE]
PUSH:                inherits COMMIT                + [PUSH_EXECUTE]
```

```
Capabilities(L) = OwnCapabilities(L) ∪ Capabilities(parent₁) ∪ … ∪ Capabilities(parentₙ)
```

The closure is computed over the declared `inherits` edges in the schema — the
validator walks them and rejects a cycle. **No rule reads the textual ordering of
profile names.** `CODE_REFACTOR` does not imply `COMMIT`; `PUSH` inherits the
content profiles only because the table says so, and that inheritance is exactly
what has to be restricted below.

### Restriction: allow narrows, deny wins

```
EffectiveCapabilities = (Capabilities(level.profile) ∩ capabilities.allow) − capabilities.deny
```

`capabilities.allow` may never introduce a capability the profile does not contain
(`AUTH-006`); it can only narrow. `capabilities.deny` always wins over `allow` and
over the profile (`AUTH-009`). The operation layer repeats the pattern:
`operations.allow` must be implied by an effective capability, and
`operations.deny` wins over it.

### The grants as applied

```yaml
authorization:                        # content grant
  state: GRANTED
  level: {profile: DOC_REFACTOR}      # ceiling: repository + analysis + documentation
  capabilities:
    mode: RESTRICT
    allow: [REPOSITORY_READ, ANALYSIS_EXECUTE, PROPOSAL_CREATE,
            DOCUMENT_CREATE, DOCUMENT_MODIFY, DOCUMENT_RENAME, DOCUMENT_MOVE]
    deny:  [DOCUMENT_DELETE]          # inside the profile, explicitly removed
  operations:
    allow: [READ, ANALYZE, PROPOSE, CREATE, MODIFY, RENAME, MOVE]
    deny:  [DELETE]
  scope: {paths: {include: [README.md, docs/, tools/, prototype/, archive/], exclude: []}}
  change_ids: [R-001 … R-019]
  authority: {type: USER, identifier: "Abdus2023 (repository owner), delegating through the standing session instruction"}
  target:    {repository: "Abdus2023/Generic-Discovery-Engine", revision: "cc8df73… (work branch)"}
  granted_at: "2026-09-10"
  expires_at: null

authorization_grants:                 # publication grant
  - state: GRANTED
    level: {profile: PUSH}            # ceiling: everything, by declared inheritance
    capabilities:
      mode: RESTRICT
      allow: [REPOSITORY_READ, ANALYSIS_EXECUTE, PROPOSAL_CREATE, COMMIT_CREATE, PUSH_EXECUTE]
      deny:  [DOCUMENT_CREATE, DOCUMENT_MODIFY, DOCUMENT_RENAME, DOCUMENT_MOVE, DOCUMENT_DELETE,
              TEST_CREATE, TEST_MODIFY, TEST_RENAME, TEST_MOVE, TEST_DELETE,
              CODE_CREATE, CODE_MODIFY, CODE_RENAME, CODE_MOVE, CODE_DELETE, ARCHITECTURE_MODIFY]
    operations:
      allow: [READ, ANALYZE, PROPOSE, COMMIT, PUSH]
      deny:  [CREATE, MODIFY, RENAME, MOVE, DELETE]
    scope: {paths: {include: [README.md, docs/, tools/, prototype/, archive/], exclude: []}}
    change_ids: [R-001 … R-019]
    authority: {…} · target: {…} · granted_at: "2026-09-10" · expires_at: null
```

This is where the model earns its keep. `PUSH` **does** inherit
`ARCHITECTURE_CHANGE` → `CODE_REFACTOR`/`DOC_REFACTOR`/`TEST_REFACTOR`, so an
unrestricted `PUSH` grant would permit source-code mutation. The publication grant
therefore lists sixteen denied capabilities and five allowed ones: publication
authority without content authority. `capabilities.deny` doing real subtraction is
the mechanism, exactly as §153 intends — the safety boundary is not a naming
convention, it is a computed set.

The content grant likewise denies `DOCUMENT_DELETE`, which *is* inside its
profile. Nothing in this work deleted a file: git records the two archived
transcripts as renames with 100 % similarity (`R100`), which is a `MOVE`/`RENAME`
under the canonical vocabulary, not a `DELETE`. The deny is therefore a statement
about authority that was never exercised — and the operation list is a list of
what was actually done, so `DELETE` appears in `deny` and nowhere in the
execution record.

### The decision function

```
ALLOW(operation, target, change) =
      authorization.state == GRANTED
  AND operation ∈ EffectiveOperations            (∩ operations.allow, − operations.deny)
  AND target ∈ authorization.scope
  AND change.id ∈ authorization.change_ids
  AND authorization is temporally valid (granted_at ≤ now < expires_at)
```

Evaluation follows the resolution order of §151 and §155:

```
requested operation
      ↓
state == GRANTED ?                     ── no ─→ AUTHORIZATION_BLOCKED
      ↓ yes
level.profile valid and known ?        ── no ─→ deny
      ↓ yes
capability closure of the profile
      ↓
∩ capabilities.allow   − capabilities.deny        (deny wins)
      ↓
operation ∈ implied operations            ── no ─→ AUTHORIZATION_DENIED
∩ operations.allow     − operations.deny
      ↓
target path inside scope.paths.include, outside exclude   ── no ─→ deny
      ↓ yes
change.id ∈ change_ids ?               ── no ─→ separate authorization required
      ↓ yes
ALLOW
```

`AUTH-001` … `AUTH-020` encode these steps and `tools/validate-analysis.mjs`
evaluates them against the record; `EV-010`, `EV-011` and `EV-012` require that
every executed operation has a decision, names an authorized change, and that no
unauthorized operation touched the repository.

### Scope paths

`scope.paths.include` names the locations this change set was allowed to touch:
`README.md`, `docs/`, `tools/`, `prototype/`, `archive/`. `exclude` is **empty**,
and that is a recorded fact rather than an omission: every location the change set
touched is inside the include list, so there was nothing to withhold. The
protection in this work is not path-based but capability-based — no grant carries
`CODE_*`, `TEST_*` or `ARCHITECTURE_MODIFY`, and `tools/verify.mjs` re-derives the
capability closure to prove that no withheld capability is reachable through
either grant. The declared include list is additionally checked against git: the
paths changed since the base revision must all lie inside it.

`prototype/` appears in the include list because the extraction step created the
artifact file there (change `R-001`), and `archive/` because the transcripts were
moved into it (`R-005`, `R-013`). Both are frozen afterwards: the artifact digest
is recomputed by the verification tooling and has not changed since it was
extracted.

### The two lifecycles

Execution and post-verification are separate lifecycles with separate vocabularies,
and neither reuses the other's or the claim's:

```
execution.state            NOT_STARTED · AUTHORIZATION_BLOCKED · READY · RUNNING ·
                           SUCCEEDED · PARTIALLY_SUCCEEDED · FAILED · CANCELLED · STOPPED
execution.operations[].result
                           NOT_ATTEMPTED · AUTHORIZATION_DENIED · SKIPPED · SUCCEEDED ·
                           FAILED · CANCELLED · BLOCKED
post_verification.state    NOT_REQUIRED · NOT_STARTED · READY · RUNNING · PASSED ·
                           PARTIALLY_PASSED · FAILED · BLOCKED · INCONCLUSIVE
post_verification.result   CONFORMING · PARTIALLY_CONFORMING · NON_CONFORMING ·
                           INCONCLUSIVE · NOT_APPLICABLE
post_verification.checks[].result
                           NOT_RUN · PASSED · FAILED · BLOCKED · INCONCLUSIVE
```

The per-operation results exist so that `execution.state: PARTIALLY_SUCCEEDED`
cannot hide which operation failed. In this record all 21 operations returned
`SUCCEEDED`, the execution lifecycle is `SUCCEEDED`, and the post-verification
lifecycle is `PASSED` with result `CONFORMING` across eight independent checks —
three separate statements, not one.

`SUCCEEDED ≠ VERIFIED` and `FAILED ≠ UNVERIFIED`: execution success never
produces verification success by itself (`PV-008`), and verification never modifies
the repository to make a check pass (`PV-009`, and `post_verification.mutations`
is empty). Remediation proposed by verification would need its own authorization
(`PV-010`).

### Change-set boundary

Authorization covered `R-001 … R-018`. During execution, twelve further problems
were discovered (`R-101 … R-112`, including the P0 ownership defects). Per the
change-set rule they were **recorded and proposed, not fixed** — even though one
(`R-109`, the dead counter) would have been a two-line edit. They remain
`PLAN ONLY` and outside `change_ids`.

### Discovered-change rule — worked example

```
Approved:      documentation refactor (R-001 … R-018)
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
| Authorization level confirmed | yes — content grant profile `DOC_REFACTOR` (capabilities narrowed, `DOCUMENT_DELETE` denied); publication grant profile `PUSH` (16 inherited content capabilities denied, publication only) |
| Capability closure computed and checked | yes — `allow ⊆ Capabilities(profile)` for both grants; withheld classes unreachable (`AUTH-006`, `AUTH-018`) |
| Change set identified | yes — `R-001 … R-019` in `change_ids` |
| Verification completed | yes — evidence + claims + analysis |
| Evidence references available | yes — the register resolves every cited id |
| Rollback understood | yes — git history on the work branch |

```
EXECUTION STATUS: AUTHORIZED
```

**Post-execution:**

| Check | Result |
| --- | --- |
| Requested changes completed | yes — `R-001 … R-019` |
| No unauthorized changes made | yes — artifact digest identical to extraction; no code or test changes |
| Repository structure valid | yes — matches the proposed structure |
| Links valid | yes — 20+ documents, zero broken relative links |
| References valid | yes — evidence/claim citations resolve |
| Documentation consistent | yes — 43 static checks pass |
| Code unchanged (out of scope) | **yes — SHA-256 unchanged** |
| Tests unchanged (out of scope) | yes — no test suite existed to change |
| Required tests executed | yes — `verify.mjs`, `checks.mjs`, `simulate.mjs` |
| Critical invariants reverified | yes — ownership invariant measured and reported as violated (unchanged, as expected) |
| New contradictions absent | yes — none introduced; seven recorded instead |

```yaml
execution:                          # lifecycle and per-operation results are separate fields
  state: SUCCEEDED
  operations:                       # 21 entries; each names its operation, target, change and result
    - {id: OP-001, change_id: R-001, operation: CREATE, target: prototype/generic-discovery-engine.user.js, result: SUCCEEDED}
    - {id: OP-019, change_id: R-019, operation: MODIFY, target: docs/analysis/analysis.schema.json, result: SUCCEEDED}
    - {id: OP-020, change_id: R-019, operation: COMMIT, target: "repository (change set R-001 … R-019)", result: SUCCEEDED}
    - {id: OP-021, change_id: R-019, operation: PUSH,   target: origin/arena/01a08d14-generic-discovery-engine, result: SUCCEEDED}
  executed_changes: [R-001 .. R-019]
  unauthorized_changes: []
  discovered_not_executed: [R-101 .. R-112]

post_verification:                  # its own lifecycle and its own outcome vocabulary
  state: PASSED
  result: CONFORMING
  checks:
    - {id: VERIFY-001, description: "record passes the validation pipeline", result: PASSED}
    - {id: VERIFY-005, description: "source artifact unchanged (sha256 8f5fc5c5...)", result: PASSED}
    - {id: VERIFY-007, description: "no path outside the declared scope paths changed", result: PASSED}
  findings: []
  remediation_required: false
  mutations: []                     # verification repaired nothing (PV-009)
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
| Modify code | only if authorized (**not** granted — no grant carries `CODE_*`) | yes | yes |
| Delete | only if authorized (not granted; nothing deleted) | yes | yes |
| Commit | only if authorized (yes — `COMMIT_CREATE` on the publication grant only) | yes | yes |
| Push | only if explicitly authorized (yes — `PUSH_EXECUTE`, work branch only) | yes | yes |
| Final verification (`VERIFIER`) | yes | optional | no |

Role identifier per operation, first two columns only — the analyzer and the
executor are the same actor holding different roles, which is why the role
boundary is stated explicitly rather than assumed.

## 8. Master separation invariant

The architecture preserves these distinctions, and the validator checks that the
record keeps them as separate fields:

```
claim_kind ≠ implementation_state ≠ test_state ≠ evidence_level
           ≠ verification_result ≠ confidence

authorization.state ≠ authorization.level.profile ≠ capability
                    ≠ operation ≠ scope ≠ change authorization

execution.state ≠ execution.operations[].result
                ≠ post_verification.state ≠ post_verification.result
```

The purpose is not cleaner terminology. It prevents a specific reasoning error —
the chain

```
"implemented" → "tested" → "verified" → "authorized" → "executed" → "correct"
```

in which every arrow is an assumption. None of those implications is valid without
evidence for the next transition, and the model requires each transition to be
established independently. This repository contains live counter-examples to each
arrow: `CAND-CLAIM-003` is `IMPLEMENTED` and `UNTESTED`; `SCHED-CLAIM-004` is
`TESTED` and `CONTRADICTED`; `SCOPE-CLAIM-001` is `VERIFIED` and
`NOT_IMPLEMENTED`; the publication grant is `GRANTED` while carrying no content
capability; and `execution.state: SUCCEEDED` sits beside a post-verification
lifecycle that had to establish `PASSED` on its own.

## 9. Complete lifecycle, as applied

```
                    CLAIM  (41 records, six typed dimensions)
                      │
                      ▼
              CLAIM VALIDATION          structural schema → CV-001…CV-020
                      │
                      ▼
              EVIDENCE ANALYSIS         register resolution, CV-008, CV-010, C-031
                      │
                      ▼
             VERIFICATION RESULT        what the inspected revision establishes
                      │
                      │
              proposed change
                      ▼
               AUTHORIZATION              AUTH-001…AUTH-020
                      │
           ┌──────────┴──────────┐
           │                     │
        DENIED                 GRANTED
           │                     │
           ▼                     ▼
 AUTHORIZATION_BLOCKED         READY
                                 │
                                 ▼
                               RUNNING                       EV-001…EV-012
                                 │
                  ┌──────────────┼──────────────┐
                  ▼              ▼              ▼
               SUCCEEDED      PARTIAL        FAILED         per-operation results
                  │              │              │
                  └──────────────┼──────────────┘
                                 ▼
                        POST-VERIFICATION                 PV-001…PV-010
                                 │
                  ┌──────────────┼──────────────┐
                  ▼              ▼              ▼
                PASSED        PARTIAL        FAILED
                  │              │              │
                  └──────────────┴──────────────┘
                                 ▼
                          FINAL EVIDENCE
                    (this record, and the tools that reproduce it)
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
VERIFICATION         read-only; 41 claim records with six typed dimensions
     ↓
VERIFIED TRUTH SET   what exists, what is planned, what is absent, what is contradicted
     ↓
REFACTORING PLAN     R-001…R-019 executed; R-101…R-112 plan only
     ↓
AUTHORIZATION CHECK  state GRANTED; profile DOC_REFACTOR restricted by capability; publication by a
                     separate PUSH grant whose inherited content capabilities are denied
     ↓
EXECUTE (docs only)  → POST-VERIFY (independent, I-012) → execution SUCCEEDED,
                        post_verification PASSED / CONFORMING
```

Governing separation, preserved at every step: **evidence → claim → verification
→ proposal → authorization → execution → post-verification**. No stage
impersonates another; repository access is not authorization, authorization is not
a capability, a capability is not an operation, an operation is not an authorized
change, an authorized change is not an executed change, and an executed change is
not a verified change.
