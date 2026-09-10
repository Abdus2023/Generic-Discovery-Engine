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
| READ | allowed (`CAP-REPOSITORY-READ`, ENABLED) |
| ANALYZE | allowed (`CAP-REPOSITORY-ANALYZE`, ENABLED) |
| PROPOSE | allowed (`CAP-REPOSITORY-PROPOSE`, ENABLED) |
| CREATE | allowed — documentation and tooling only (`CAP-DOCUMENT-CREATE`, RESTRICTED to `docs/` and `tools/`; source creation only under the disclosed extraction grant, `prototype/`, change `R-001`) |
| MODIFY | allowed — `CAP-DOCUMENT-MODIFY`, RESTRICTED to `README.md`, `docs/`, `tools/`; **no source capability exists in any grant** |
| RENAME | allowed — `CAP-DOCUMENT-RENAME`, RESTRICTED to `archive/` (one archived transcript) |
| MOVE | allowed — `CAP-DOCUMENT-MOVE`, RESTRICTED to `docs/roadmap/` and `archive/` |
| DELETE | denied at every layer (`CAP-DOCUMENT-DELETE` in `denies`, `DELETE` in `operations.deny`); nothing was deleted — git records the two archived transcripts as 100 %-similar renames (`R100`), not deletions |
| CODE CHANGES | one disclosed exception: `CAP-SOURCE-CREATE` under the extraction grant for `R-001`. Every other source capability is withheld and unreachable; no source file was modified, renamed, moved or deleted |
| TEST CHANGES | **no capability exists** — `CAP-TEST-*` is withheld; adding the verification tooling was documentation and analysis tooling, not test-suite modification |
| DOCUMENTATION CHANGES | allowed up to the capability ceiling, and narrowed by the explicit allow list |
| COMMIT | allowed by the publication grant only (`CAP-COMMIT-CREATE`, ENABLED) |
| PUSH | allowed by the publication grant only (`CAP-REMOTE-PUSH`, ENABLED, work branch) |

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

Authorization resolves through distinct objects, and none of them may stand in for
another (sections 167, 178, 179):

```
LEVEL PROFILE   →   CAPABILITY SET   →   OPERATION   →   SCOPE   →   CHANGE
 reusable policy     atomic primitives     actions       paths        records
```

| Concept | Field | Question |
| --- | --- | --- |
| Authorization state | `authorization.state` | Has mutation authority actually been granted? |
| Level profile | `authorization.level.profile` | Which reusable policy ceiling applies? |
| Capability | `authorization.capabilities.grants[]` / `denies[]` | Which atomic permission, in which state? |
| Operation | `authorization.operations.allow/deny` | Which actions are permitted against a resource class? |
| Scope | `authorization.scope.paths` | Which locations are in play? |
| Change authorization | `authorization.change_ids` | Which change records are covered? |

States: `NOT_REQUESTED` · `REQUESTED` · `GRANTED` · `DENIED` · `REVOKED` ·
`EXPIRED`. **Only `GRANTED` can authorize mutation** (AC-001). A profile is a
reusable policy definition, not authorization — `DOC_REFACTOR` on a grant says
what *could* be permitted at most, not what the user granted.

### Capabilities are objects, not names

A capability is an atomic authorization primitive with its own lifecycle
(sections 171, 172, 191):

```yaml
- id: CAP-DOCUMENT-MODIFY        # ^CAP-[A-Z0-9_-]+$
  state: RESTRICTED              # DECLARED · ENABLED · RESTRICTED · DENIED · REVOKED · EXPIRED
  resource_class: DOCUMENT       # REPOSITORY · DOCUMENT · TEST · SOURCE · CONFIGURATION · ARCHITECTURE · COMMIT · REMOTE
  operations: [MODIFY]
  constraints: {paths: {include: [README.md, docs/, tools/], exclude: []}}
```

`CAP-DOCUMENT-MODIFY` means **MODIFY against DOCUMENT** — never MODIFY against an
arbitrary repository object (section 176). The catalogue is embedded in
[analysis.json](analysis.json) as `capabilities` with state `DECLARED`, and
**DECLARED is not ENABLED** (AC-005): a capability existing in a policy registry
proves nothing about a particular authorization. The states that matter for a
decision are carried by the authorization's own `grants` and `denies` entries.

| State | Meaning in this record |
| --- | --- |
| `DECLARED` | the 21 catalogue entries: policy definitions, authorizing nothing |
| `ENABLED` | granted without additional narrowing (`CAP-REPOSITORY-READ`, `CAP-COMMIT-CREATE`, …) |
| `RESTRICTED` | granted but narrowed by constraints (the document and extraction capabilities) |
| `DENIED` | explicitly prohibited (every inherited content capability of the publication grant) |

### Inheritance is declared; restriction only narrows

```
ProfileCapabilitySet(L) = Own(L) ∪ ProfileCapabilitySet(parents)   (AC-003, AC-004)

EffectiveCapabilities  = (ProfileCapabilitySet(profile) ∩ grants) − denies
```

`Capabilities(PUSH)` contains the document, test and code capabilities by declared
inheritance through `COMMIT → ARCHITECTURE_CHANGE`. An authorization may not add a
capability the profile does not contain (AC-007); an explicit deny overrides an
explicit grant (AC-008); operation allow-lists restrict and never expand (AC-009,
AC-010). §153's "deny is preferable to profile mutation" is exactly what the
publication grant does.

### The grants as applied — three, all capability-restricted

```yaml
authorization:                                  # 1. content grant
  state: GRANTED
  level: {profile: DOC_REFACTOR}
  capabilities:
    mode: RESTRICT
    grants:
      - {id: CAP-REPOSITORY-READ,    state: ENABLED,    resource_class: REPOSITORY, operations: [READ]}
      - {id: CAP-REPOSITORY-ANALYZE, state: ENABLED,    resource_class: REPOSITORY, operations: [ANALYZE]}
      - {id: CAP-REPOSITORY-PROPOSE, state: ENABLED,    resource_class: REPOSITORY, operations: [PROPOSE]}
      - {id: CAP-DOCUMENT-CREATE, state: RESTRICTED, resource_class: DOCUMENT, operations: [CREATE],
         constraints: {paths: {include: [docs/, tools/], exclude: []}}}
      - {id: CAP-DOCUMENT-MODIFY, state: RESTRICTED, resource_class: DOCUMENT, operations: [MODIFY],
         constraints: {paths: {include: [README.md, docs/, tools/], exclude: []}}}
      - {id: CAP-DOCUMENT-RENAME, state: RESTRICTED, resource_class: DOCUMENT, operations: [RENAME],
         constraints: {paths: {include: [archive/], exclude: []}}}
      - {id: CAP-DOCUMENT-MOVE,   state: RESTRICTED, resource_class: DOCUMENT, operations: [MOVE],
         constraints: {paths: {include: [docs/roadmap/, archive/], exclude: []}}}
    denies:
      - {id: CAP-DOCUMENT-DELETE, state: DENIED, resource_class: DOCUMENT, operations: [DELETE]}
  operations: {allow: [READ, ANALYZE, PROPOSE, CREATE, MODIFY, RENAME, MOVE], deny: [DELETE]}
  scope: {paths: {include: [README.md, docs/, tools/, prototype/, archive/], exclude: []}}
  change_ids: [R-001 … R-020]
  authority: {type: USER, identifier: "Abdus2023 (repository owner), delegating through the standing session instruction"}
  target:    {repository: "Abdus2023/Generic-Discovery-Engine", revision: "cc8df73… (work branch)"}
  granted_at: "2026-09-10"
  expires_at: null

authorization_grants:
  - # 2. extraction grant — disclosed, narrow, and closed
    state: GRANTED
    level: {profile: CODE_REFACTOR}
    capabilities:
      mode: RESTRICT
      grants:
        - {id: CAP-SOURCE-CREATE, state: RESTRICTED, resource_class: SOURCE, operations: [CREATE],
           constraints: {paths: {include: [prototype/], exclude: []}}}
      denies: []
    operations: {allow: [CREATE], deny: [MODIFY, RENAME, MOVE, DELETE, COMMIT, PUSH]}
    scope: {paths: {include: [prototype/], exclude: []}}
    change_ids: [R-001]

  - # 3. publication grant — publication authority without content authority
    state: GRANTED
    level: {profile: PUSH}
    capabilities:
      mode: RESTRICT
      grants:
        - {id: CAP-REPOSITORY-READ, state: ENABLED, resource_class: REPOSITORY, operations: [READ]}
        - {id: CAP-REPOSITORY-ANALYZE, state: ENABLED, resource_class: REPOSITORY, operations: [ANALYZE]}
        - {id: CAP-REPOSITORY-PROPOSE, state: ENABLED, resource_class: REPOSITORY, operations: [PROPOSE]}
        - {id: CAP-COMMIT-CREATE, state: ENABLED, resource_class: COMMIT, operations: [COMMIT]}
        - {id: CAP-REMOTE-PUSH,   state: ENABLED, resource_class: REMOTE, operations: [PUSH]}
      denies:                     # 16 capabilities PUSH inherits and must not carry
        - {id: CAP-DOCUMENT-CREATE, state: DENIED} … {id: CAP-DOCUMENT-DELETE, state: DENIED}
        - {id: CAP-TEST-CREATE,     state: DENIED} … {id: CAP-TEST-DELETE,     state: DENIED}
        - {id: CAP-SOURCE-CREATE,   state: DENIED} … {id: CAP-SOURCE-DELETE,   state: DENIED}
        - {id: CAP-ARCHITECTURE-MODIFY, state: DENIED}
    operations: {allow: [READ, ANALYZE, PROPOSE, COMMIT, PUSH], deny: [CREATE, MODIFY, RENAME, MOVE, DELETE]}
    change_ids: [R-001 … R-020]
```

**Why three and not two.** When operations gained a resource class, one already
executed operation became visible that the first two grants could not cover:
`OP-001` created `prototype/generic-discovery-engine.user.js`, and creating a
source file is `CREATE` against `SOURCE`. The extraction was part of the original
mandate, so the honest response is to disclose it as its own grant — the narrowest
one that covers it: profile `CODE_REFACTOR`, a single `RESTRICTED` capability
constrained to `prototype/`, a single change (`R-001`), and `MODIFY`/`RENAME`/
`MOVE`/`DELETE` explicitly denied. The alternative — leaving an executed operation
that no grant covers — is precisely what AC-011 and AC-012 forbid. Nothing about
that grant authorizes further work, and the withheld capability classes
(`CAP-SOURCE-MODIFY|RENAME|MOVE|DELETE`, all `CAP-TEST-*`,
`CAP-ARCHITECTURE-MODIFY`) remain unreachable through every grant, which
`tools/verify.mjs` re-derives from the closure.

The publication grant is the model's clearest demonstration. `PUSH` inherits
`ARCHITECTURE_CHANGE` → `CODE_REFACTOR`/`DOC_REFACTOR`/`TEST_REFACTOR`, so an
unrestricted `PUSH` grant would permit source-code mutation. Sixteen inherited
content capabilities are therefore `DENIED` and only five are enabled:
publication authority without content authority, enforced as a computed set rather
than a naming convention.

### The decision function (section 179)

```
ALLOW(operation) =
      authorization.state == GRANTED
  AND ∃ capability in the grant:
        capability.state ∈ {ENABLED, RESTRICTED}
        AND capability ∈ ProfileCapabilitySet(level.profile)
        AND capability not in denies
        AND operation ∈ capability.operations
        AND target.resource_class == capability.resource_class
        AND constraints pass (for RESTRICTED capabilities)
  AND target ∈ authorization.scope
  AND change_id ∈ authorization.change_ids
  AND authorization is temporally valid (AC-013)
```

Resolution order (§201):

```
AUTHORIZATION → state == GRANTED → LEVEL PROFILE → INHERITANCE RESOLUTION
      → PROFILE CAPABILITIES → AUTHORIZATION RESTRICTIONS → EFFECTIVE CAPABILITIES
      → OPERATION EVALUATION → DENY | ALLOW → SCOPE → CHANGE ID → EXECUTION
      → EXECUTION VERIFICATION
```

`AC-001` … `AC-016` encode these rules, `AUTH-017`…`AUTH-020` add what the section
does not name (a `GRANTED` authorization must state its authority and target,
discovered work stays unauthorized, withheld classes stay unreachable, and every
recorded `authorization_decision` must match what the resolver computes).
`tools/validate-analysis.mjs` evaluates all of them; the record's own decisions
are re-derived rather than trusted. Mutating operations in this record resolve to
`DOC_REFACTOR: 18`, `CODE_REFACTOR: 1`, `PUSH: 2`.

### Scope paths

`scope.paths.include` names the locations this change set was allowed to touch:
`README.md`, `docs/`, `tools/`, `prototype/`, `archive/`. `exclude` is **empty**,
and that is a recorded fact rather than an omission: nothing inside the tree was
withheld from the change set. The protection here is capability-based — no grant
carries `CAP-SOURCE-MODIFY`, `CAP-TEST-*` or `CAP-ARCHITECTURE-MODIFY` — and
`tools/verify.mjs` re-derives the capability closure to prove it. The declared
include list is additionally checked against git: every path changed since the base
revision must lie inside it.

`prototype/` appears because the extraction created the artifact file there
(`R-001`), and `archive/` because the transcripts were moved into it (`R-005`,
`R-013`). Both are frozen afterwards: the artifact digest is recomputed by the
verification tooling and has not changed since extraction.

### The two verification domains, and execution

Three different objects, three different vocabularies (sections 168, 180–184):

```
claim_verification.result      VERIFIED · PARTIALLY_VERIFIED · UNVERIFIED · CONTRADICTED · NOT_APPLICABLE
                               → the proposition and its evidence

execution.state                NOT_STARTED · AUTHORIZATION_BLOCKED · READY · RUNNING · SUCCEEDED ·
                               PARTIALLY_SUCCEEDED · FAILED · CANCELLED · STOPPED
execution.operations[].result  NOT_ATTEMPTED · AUTHORIZATION_DENIED · SKIPPED · SUCCEEDED · FAILED ·
                               CANCELLED · BLOCKED
                               → what actually happened, per operation

execution_verification.state   NOT_REQUIRED · NOT_STARTED · READY · RUNNING · PASSED ·
                               PARTIALLY_PASSED · FAILED · BLOCKED · INCONCLUSIVE
execution_verification.result  CONFORMING · PARTIALLY_CONFORMING · NON_CONFORMING · INCONCLUSIVE ·
                               NOT_APPLICABLE
checks[].result                NOT_RUN · PASSED · FAILED · BLOCKED · INCONCLUSIVE
                               → whether the resulting repository satisfies its invariants
```

**VERIFIED belongs to claims; CONFORMING belongs to execution verification.** An
unqualified `verification` object would be ambiguous about which object is being
verified, so it is forbidden (section 168.3) and the validator rejects the field
name outright.

Per-operation results exist so that `execution.state: PARTIALLY_SUCCEEDED` cannot
hide which operation failed; each operation also carries the
`authorization_decision` that permitted it. In this record all 21 operations are
`ALLOWED` and `SUCCEEDED`, and the execution verification is `PASSED` /
`CONFORMING` across eight checks — three separate statements, not one.

`SUCCEEDED ≠ VERIFIED` and `FAILED ≠ UNVERIFIED`: execution success never produces
verification success by itself (EVV-001, EVV-002), and verification never modifies
the repository to make a check pass (EVV-008 — `execution_verification.mutations`
is empty). A remediation finding would propose a new change and would not
authorize it (EVV-009).

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
| Authorization level confirmed | yes — three grants: content (`DOC_REFACTOR`, mutating capabilities RESTRICTED, `CAP-DOCUMENT-DELETE` DENIED), extraction (`CODE_REFACTOR`, `CAP-SOURCE-CREATE` only, change `R-001`), publication (`PUSH`, 16 inherited content capabilities DENIED) |
| Capability closure computed and checked | yes — every grant ⊆ `ProfileCapabilitySet(profile)` (AC-007); explicit denies override grants (AC-008); withheld classes unreachable (`AUTH-019`) |
| Change set identified | yes — `R-001 … R-020` in `change_ids` |
| Verification completed | yes — evidence + claims + analysis |
| Evidence references available | yes — the register resolves every cited id |
| Rollback understood | yes — git history on the work branch |

```
EXECUTION STATUS: AUTHORIZED
```

**Post-execution:**

| Check | Result |
| --- | --- |
| Requested changes completed | yes — `R-001 … R-020` |
| No unauthorized changes made | yes — artifact digest identical to extraction; no code or test changes |
| Repository structure valid | yes — matches the proposed structure |
| Links valid | yes — 20+ documents, zero broken relative links |
| References valid | yes — evidence/claim citations resolve |
| Documentation consistent | yes — 47 static checks pass |
| Code unchanged (out of scope) | **yes — SHA-256 unchanged** |
| Tests unchanged (out of scope) | yes — no test suite existed to change |
| Required tests executed | yes — `verify.mjs`, `checks.mjs`, `simulate.mjs` |
| Critical invariants reverified | yes — ownership invariant measured and reported as violated (unchanged, as expected) |
| New contradictions absent | yes — none introduced; seven recorded instead |

```yaml
execution:                          # what happened; per-operation results are separate fields
  state: SUCCEEDED
  operations:                       # 21 entries; each names its operation, resource-classed target, change, decision and result
    - {id: OP-001, change_id: R-001, operation: CREATE,
       target: {resource_class: SOURCE, path: prototype/generic-discovery-engine.user.js},
       authorization_decision: ALLOWED, result: SUCCEEDED}
    - {id: OP-017, change_id: R-017, operation: MODIFY,
       target: {resource_class: DOCUMENT, path: docs/analysis/claims.md},
       authorization_decision: ALLOWED, result: SUCCEEDED}
    - {id: OP-020, change_id: R-020, operation: COMMIT,
       target: {resource_class: COMMIT, path: "repository (change set R-001 … R-020)"},
       authorization_decision: ALLOWED, result: SUCCEEDED}
    - {id: OP-021, change_id: R-020, operation: PUSH,
       target: {resource_class: REMOTE, path: origin/arena/01a08d14-generic-discovery-engine},
       authorization_decision: ALLOWED, result: SUCCEEDED}
  executed_changes: [R-001 .. R-020]
  unauthorized_changes: []
  discovered_not_executed: [R-101 .. R-112]

execution_verification:             # whether the resulting state conforms — a different domain
  state: PASSED
  result: CONFORMING
  checks:                           # one outcome per invariant, no lifecycle on a check
    - {id: VERIFY-001, description: "record passes the validation pipeline", result: PASSED}
    - {id: VERIFY-005, description: "source artifact unchanged (sha256 8f5fc5c5...)", result: PASSED}
    - {id: VERIFY-007, description: "no path outside the declared scope paths changed", result: PASSED}
  findings: []
  remediation_required: false
  mutations: []                     # verification repaired nothing (EVV-008)
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
| Modify code | only if authorized (**not** granted — no grant carries `CAP-SOURCE-MODIFY`) | yes | yes |
| Delete | only if authorized (not granted; nothing deleted) | yes | yes |
| Commit | only if authorized (yes — `CAP-COMMIT-CREATE`, publication grant only) | yes | yes |
| Push | only if explicitly authorized (yes — `CAP-REMOTE-PUSH`, work branch only) | yes | yes |
| Final verification (`VERIFIER`) | yes | optional | no |

Role identifier per operation, first two columns only — the analyzer and the
executor are the same actor holding different roles, which is why the role
boundary is stated explicitly rather than assumed.

## 8. Master separation invariant

The architecture preserves these distinctions, and the validator checks that the
record keeps them as separate fields:

```
claim_kind ≠ implementation_state ≠ test_state ≠ evidence_level
           ≠ claim_verification.result ≠ confidence

authorization.state ≠ authorization.level.profile ≠ capability.state
                    ≠ operation ≠ scope ≠ change authorization

execution.state ≠ execution.operations[].result ≠ execution.operations[].authorization_decision
                ≠ execution_verification.state ≠ execution_verification.result
                ≠ execution_verification.checks[].result
```

The purpose is not cleaner terminology. It prevents a specific reasoning error —
the chain

```
"implemented" → "tested" → "verified" → "authorized" → "executed" → "correct"
```

in which every arrow is an assumption. None of those implications is valid without
evidence for the next transition, and the model requires each transition to be
established independently. Section 200 adds the same discipline to lifecycle
states: a state may only be reached through a declared transition, and the
validator checks that every recorded state is reachable in the declared graph. This repository contains live counter-examples to each
arrow: `CAND-CLAIM-003` is `IMPLEMENTED` and `UNTESTED`; `SCHED-CLAIM-004` is
`TESTED` and `CONTRADICTED`; `SCOPE-CLAIM-001` is `VERIFIED` and
`NOT_IMPLEMENTED`; the publication grant is `GRANTED` while carrying no content
capability; and `execution.state: SUCCEEDED` sits beside an execution-verification
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
          CLAIM_VERIFICATION.RESULT     what the inspected revision establishes
                      │
                      │
              proposed change
                      ▼
               AUTHORIZATION              AC-001…AC-016 + AUTH-017…AUTH-020
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
                    EXECUTION_VERIFICATION                EVV-001…EVV-009
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
REFACTORING PLAN     R-001…R-020 executed; R-101…R-112 plan only
     ↓
AUTHORIZATION CHECK  state GRANTED; three capability-restricted grants; AC-001…AC-016 evaluated
     ↓
EXECUTE (docs only)  → EXECUTION VERIFICATION (independent, I-012) → execution SUCCEEDED with
                        21 ALLOWED decisions, execution_verification PASSED / CONFORMING
```

Governing separation, preserved at every step: **evidence → claim → claim
verification → proposal → authorization → capability → operation → execution →
execution verification**. No stage impersonates another; repository access is not
authorization, authorization is not a capability, a capability is not an
operation, an operation is not an authorized change, an authorized change is not
an executed change, an executed change is not a conforming repository, and
`VERIFIED` is not `CONFORMING`.
