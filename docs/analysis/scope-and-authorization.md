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
| `ANALYZER` | this analysis | inspection, evidence extraction, interpretation, verification analysis, contradiction and duplication detection, refactoring proposals | must not mutate the target repository merely because it has technical access; may produce analysis artifacts inside it when authorized (here: `ANALYSIS_ONLY`, reached through `DOC_REFACTOR`) |
| `REVIEWER` | repository owner / reviewer | reviews evidence, verification conclusions, refactoring proposals, risk and scope | carries no mutation authority by virtue of reviewing |
| `AUTHORIZER` | repository owner, delegating through the user's instruction | grants mutation permission, scoped and explicit | must hold authority delegated by the repository owner; authorization is never inferred from capability or from phrasing such as "clean this up" |
| `EXECUTOR` | the same agent, **explicitly entering the EXECUTOR role** for the authorized change set only | performs the authorized mutations | must follow the approved change set, respect scope and forbidden operations, stop at any boundary violation, and report changes |
| `VERIFIER` | this analysis, re-running the tools after execution | determines whether the result satisfies the requested postconditions | must not silently repair a failed verification; it reports `FAILED`/`PARTIALLY_VERIFIED` instead |

Role-entry statement required by the ownership rule: the analyzer became the
executor **only** for change set `R-001 … R-021` (documentation and analysis
artifacts), under the authorization recorded in §5. For `R-101 … R-112` (code) the
analyzer remained `ANALYZER` and produced proposals only.

## 4. Decision ownership

| Kind | Example from this analysis | Owner |
| --- | --- | --- |
| FACT | "the prototype has seven recognition providers" | established by analysis from evidence; not a decision |
| INTERPRETATION | "the provider abstraction is deliberately pure, which is why it is replaceable" | analysis (labelled as interpretation) |
| DESIGN DECISION | "introduce a protocol-neutral acquisition provider; treat re-proposed work as work rather than candidate state" | repository owner — proposed, not taken |
| EXECUTION DECISION | "modify `queueCandidate()` now" | repository owner authorizes; analysis recommends, and did **not** execute (`R-101`, plan only) |
| DOCUMENTATION DECISION | "split the archive into code + roadmap + history" | analysis executed under `DOC_REFACTOR` with `CAP-DOCUMENT-*` capabilities |

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
| Capability declaration | `capability-registry.json` | What may a profile declare? (`DECLARED`, authorizing nothing) |
| Capability grant | `authorization.capability_grants[]` | Which atomic permission, in which state and scope? |
| Operation | `authorization.operations.allow/deny` | Which actions are permitted against a resource class? |
| Scope | `authorization.scope.paths` | Which locations are in play? |
| Change authorization | `authorization.change_ids` | Which change records are covered? |

States: `NOT_REQUESTED` · `REQUESTED` · `GRANTED` · `DENIED` · `REVOKED` ·
`EXPIRED`. **Only `GRANTED` can authorize mutation**, and even then only through a
capability that survives the profile ceiling (section 216). A profile is a reusable
policy definition, not authorization — `PUSH` in `level.profile` says what *could*
be permitted at most, not what the user granted.

### Profile declaration ≠ grant ≠ effective capability

Brief 10 section 202 separates three things that an earlier revision of this
document ran together, and forbids representing them by one state field:

```
PROFILE DECLARATION   "this capability belongs to this reusable profile"
        ↓
AUTHORIZATION GRANT   "this authorization grants this capability for this target and scope"
        ↓
EFFECTIVE CAPABILITY  (profile ∩ grant) − deny, computed, never persisted as input
```

The registry that carries the declarations is
[capability-registry.json](capability-registry.json): a policy file, not a grant.
A capability there is `DECLARED`, which authorizes nothing (section 203).

```jsonc
{ "id": "CAP-DOCUMENT-MODIFY", "resource_class": "DOCUMENT", "operations": ["MODIFY"] }
```

`CAP-DOCUMENT-MODIFY` means **MODIFY against DOCUMENT** — never MODIFY against an
arbitrary repository object (section 176). The grant lives in the authorization and
names the capability by id, adding only a state and, when restricted, a scope:

```yaml
capability_grants:
  - {capability_id: CAP-DOCUMENT-MODIFY, state: RESTRICTED,
     scope: {paths: {include: [README.md, docs/, tools/], exclude: []}}}
```

**The state has a semantic owner** (section 203): a profile declares
(`DECLARED`), an authorization decides (`ENABLED`, `RESTRICTED`, `DENIED`,
`REVOKED`, `EXPIRED`). The same word in the wrong object is a modelling error, and
the validator reports the registry's states and the grant states separately.

When several rules bear on one capability, precedence is fixed (section 206):

```
DENIED > REVOKED > EXPIRED > RESTRICTED > ENABLED > DECLARED
```

`DECLARED` alone never authorizes execution, and the terminal states
(`DENIED`, `REVOKED`, `EXPIRED`) cannot be promoted by adding an `ENABLED` grant
(CG-007, CG-008, CG-009, CAP-009, CAP-010, CAP-011).

| State | Meaning in this record | Count |
| --- | --- | --- |
| `DECLARED` | the registry: 21 policy declarations, authorizing nothing | 21 |
| `ENABLED` | granted without narrowing (`CAP-REPOSITORY-READ\|ANALYZE\|PROPOSE`, `CAP-COMMIT-CREATE`, `CAP-REMOTE-PUSH`) | 5 |
| `RESTRICTED` | granted, narrowed by a scope (`CAP-DOCUMENT-CREATE\|MODIFY\|RENAME\|MOVE`, `CAP-SOURCE-CREATE`) | 5 |
| `DENIED` | explicitly prohibited (document deletion, every test and source mutation, architecture change) | 11 |

### Inheritance is declared; restriction is intersection

```
ProfileCapabilitySet(L) = Own(L) ∪ ProfileCapabilitySet(parents)      (section 212)

EffectiveCapabilities   = (ProfileCapabilitySet(level.profile) ∩ grants) − denies
EffectiveScope          = profile scope ∩ authorization scope ∩ capability restriction   (section 207)
EffectiveOperations     = capability operations ∩ operations.allow − operations.deny      (section 208)
```

`Capabilities(PUSH)` contains the document, test and code capabilities by declared
inheritance through `COMMIT → ARCHITECTURE_CHANGE`; inheritance exists only where
`inherits` says so, is acyclic, and is never inferred from ordering. A grant may not
introduce a capability the resolved profile does not contain (CG-002, CG-003,
CG-014, CAP-014) — the authorization cannot escalate itself. Every layer is an
**intersection**: a restriction narrows authority, it never widens it, and the
operation list is a restriction layer rather than a privilege-granting one.

Because restriction is intersection, the withheld classes do not need to be listed
as denies to be unreachable: `CAP-SOURCE-MODIFY|RENAME|MOVE|DELETE`, every
`CAP-TEST-*` and `CAP-ARCHITECTURE-MODIFY` are `DENIED` explicitly *and* absent from
the granted set, so two independent rules keep them out.

### The authorization as applied — one object, twenty-one explicit grants

Brief 10 replaced the multi-object grant model: there is exactly one
`authorization` object, and every capability it does not grant is either absent
from the profile or explicitly denied. The profile is the **ceiling**; the grant
states decide what is actual.

```yaml
authorization:
  state: GRANTED
  level: {profile: PUSH}          # ceiling, not authority (section 202.1)
  capability_grants:              # section 204: an explicit grant object per capability
    - {capability_id: CAP-REPOSITORY-READ,    state: ENABLED}
    - {capability_id: CAP-REPOSITORY-ANALYZE, state: ENABLED}
    - {capability_id: CAP-REPOSITORY-PROPOSE, state: ENABLED}
    - {capability_id: CAP-COMMIT-CREATE,      state: ENABLED}
    - {capability_id: CAP-REMOTE-PUSH,        state: ENABLED}
    - {capability_id: CAP-DOCUMENT-CREATE, state: RESTRICTED,
       scope: {paths: {include: [docs/, tools/], exclude: []}}}
    - {capability_id: CAP-DOCUMENT-MODIFY, state: RESTRICTED,
       scope: {paths: {include: [README.md, docs/, tools/], exclude: []}}}
    - {capability_id: CAP-DOCUMENT-RENAME, state: RESTRICTED,
       scope: {paths: {include: [archive/], exclude: []}}}
    - {capability_id: CAP-DOCUMENT-MOVE, state: RESTRICTED,
       scope: {paths: {include: [docs/roadmap/, archive/], exclude: []}}}
    - {capability_id: CAP-SOURCE-CREATE, state: RESTRICTED,          # the disclosed extraction, R-001
       scope: {paths: {include: [prototype/], exclude: []}}}
    - {capability_id: CAP-DOCUMENT-DELETE, state: DENIED}
    - {capability_id: CAP-TEST-CREATE,    state: DENIED}  {capability_id: CAP-TEST-MODIFY, state: DENIED}
    - {capability_id: CAP-TEST-RENAME,    state: DENIED}  {capability_id: CAP-TEST-MOVE,   state: DENIED}
    - {capability_id: CAP-TEST-DELETE,    state: DENIED}
    - {capability_id: CAP-SOURCE-MODIFY,  state: DENIED}  {capability_id: CAP-SOURCE-RENAME, state: DENIED}
    - {capability_id: CAP-SOURCE-MOVE,    state: DENIED}  {capability_id: CAP-SOURCE-DELETE, state: DENIED}
    - {capability_id: CAP-ARCHITECTURE-MODIFY, state: DENIED}
  operations: {allow: [READ, ANALYZE, PROPOSE, CREATE, MODIFY, RENAME, MOVE, COMMIT, PUSH], deny: [DELETE]}
  scope: {paths: {include: [README.md, docs/, tools/, prototype/, archive/], exclude: []}}
  change_ids: [R-001 … R-021]
  authority: {type: USER, identifier: "Abdus2023 (repository owner), delegating through the standing session instruction"}
  target: {repository: "Abdus2023/Generic-Discovery-Engine", revision: "cc8df735…"}
  granted_at: "2026-09-10T00:00:00Z"
  expires_at: null
```

All twenty-one registry capabilities carry an explicit state, so nothing is left
implicit: ten are effective (five `ENABLED`, five `RESTRICTED`), eleven are
`DENIED`, and the registry's `DECLARED` state remains what the policy says before
any authorization exists. `tools/validate-analysis.mjs` computes the effective set
from the registry and the grants (CG-014, CAP-012) and re-derives every recorded
authorization decision with the section 216 function.

**Why the profile is `PUSH`.** The authority being recorded spans documentation
and publication, and no narrower profile contains publication capabilities. The
ceiling is therefore the widest one, and the *grant list* is what keeps it narrow —
which is precisely the split section 202.1/202.2 requires: a profile may declare,
only a grant may authorize. An earlier revision split this into three separate
authorization objects; the closed schema of brief 10 section 209 admits one, so the
restriction now lives in the grant states, where it is computed rather than named.

**The one capability that needed justification.** When operations gained a resource
class, an already executed operation became visible that no documentation
capability could cover: `OP-001` created `prototype/generic-discovery-engine.user.js`,
and creating a source file is `CREATE` against `SOURCE`. The extraction was part of
the mandate, so the honest response is to disclose it: `CAP-SOURCE-CREATE` is
granted `RESTRICTED` to `prototype/`, and `CAP-SOURCE-MODIFY|RENAME|MOVE|DELETE`
are `DENIED`. Leaving the operation uncovered instead would violate the rule that
every mutation needs a matching grant (section 216) — the alternative to disclosing
authority here is not "no authority", it is an unauthorized operation in the
record. The artifact digest is re-checked on every run, and it has not changed
since extraction.

### The authorization function (section 216)

```
authorize(authorization, profile_registry, capability_registry, requested_operation, target, change)

1. state == GRANTED                      6. apply capability restrictions
2. resolve level profile                 7. apply operation restrictions
3. resolve inherited capabilities        8. validate temporal constraints
4. resolve capability grants             9. validate target scope
5. apply capability denies              10. validate change_id
                                        11. return ALLOW or DENY

ALLOW iff
      authorization.state == GRANTED
  AND profile resolves, capability exists, and the capability is effectively ENABLED or RESTRICTED
  AND the requested operation is authorized by that capability's operation set
  AND the target satisfies the capability's resource class and restriction
  AND the target satisfies the authorization scope
  AND change_id ∈ authorization.change_ids
  AND the authorization is temporally valid
  AND no deny rule applies
```

`tools/validate-analysis.mjs` implements exactly this function and applies it to
every recorded operation, comparing its own verdict with the record's
`authorization_decision` rather than trusting it. In this record all 23 operations
re-derive as `ALLOWED`, resolved through `CAP-SOURCE-CREATE` (1),
`CAP-DOCUMENT-CREATE` (7), `CAP-DOCUMENT-MODIFY` (10), `CAP-DOCUMENT-MOVE` (2),
`CAP-DOCUMENT-RENAME` (1), `CAP-COMMIT-CREATE` (1) and `CAP-REMOTE-PUSH` (1).

The rule sets are machine-checked: `REQ-001`…`REQ-015` (required fields),
`CAP-001`…`CAP-016` and `CG-001`…`CG-015` (capability grants), `CV-001`…`CV-020`
(claims), `EV-001`…`EV-012` with the section 200 transition graph (execution),
`EVV-001`…`EVV-009` (execution verification) and `I-001`…`I-016` (separation
invariants).

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
`authorization_decision` that permitted it. In this record all 23 operations are
`ALLOWED` and `SUCCEEDED`, and the execution verification is `PASSED` /
`CONFORMING` across eight checks — three separate statements, not one.

`SUCCEEDED ≠ VERIFIED` and `FAILED ≠ UNVERIFIED`: execution success never produces
verification success by itself (EVV-001, EVV-002), and verification never modifies
the repository to make a check pass (EVV-008 — `execution_verification.mutations`
is empty). A remediation finding would propose a new change and would not
authorize it (EVV-009).

### Change-set boundary

Authorization covered `R-001 … R-021`. During execution, twelve further problems
were discovered (`R-101 … R-112`, including the P0 ownership defects). Per the
change-set rule they were **recorded and proposed, not fixed** — even though one
(`R-109`, the dead counter) would have been a two-line edit. They remain
`PLAN ONLY` and outside `change_ids`.

### Discovered-change rule — worked example

```
Approved:      documentation refactor (R-001 … R-021)
Discovered:    candidate re-queue violates the ownership invariant (D1)
Action:        record finding (CLAIM-005) → classify (BUG, ARCHITECTURAL)
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
| Authorization level confirmed | yes — one object, profile `PUSH`; 21 capability grants (5 `ENABLED`, 5 `RESTRICTED`, 11 `DENIED`) |
| Capability closure computed and checked | yes — every grant names a capability the profile declares (CG-002/CG-003); `DENIED` grants override authorizing ones (CG-007…CG-009); withheld classes unreachable twice over |
| Change set identified | yes — `R-001 … R-021` in `change_ids` |
| Verification completed | yes — evidence + claims + analysis |
| Evidence references available | yes — the register resolves every cited id |
| Rollback understood | yes — git history on the work branch |

```
EXECUTION STATUS: AUTHORIZED
```

**Post-execution:**

| Check | Result |
| --- | --- |
| Requested changes completed | yes — `R-001 … R-021` |
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
  operations:                       # 23 entries; each names its operation, resource-classed target, change, decision and result
    - {id: OP-001, change_id: R-001, operation: CREATE,   # the disclosed extraction
       target: {resource_class: SOURCE, path: prototype/generic-discovery-engine.user.js},
       authorization_decision: ALLOWED, result: SUCCEEDED}
    - {id: OP-020, change_id: R-020, operation: MODIFY,
       target: {resource_class: DOCUMENT, path: docs/analysis/analysis.json},
       authorization_decision: ALLOWED, result: SUCCEEDED}
    - {id: OP-022, change_id: R-021, operation: COMMIT,
       target: {resource_class: COMMIT, path: "repository (change set R-001 … R-021)"},
       authorization_decision: ALLOWED, result: SUCCEEDED}
    - {id: OP-023, change_id: R-021, operation: PUSH,
       target: {resource_class: REMOTE, path: origin/arena/01a08d14-generic-discovery-engine},
       authorization_decision: ALLOWED, result: SUCCEEDED}
  executed_changes: [R-001 .. R-021]
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
arrow: `CLAIM-003` is `IMPLEMENTED` and `UNTESTED`; `CLAIM-007` is
`TESTED` and `CONTRADICTED`; `CLAIM-029` is `VERIFIED` and
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
               AUTHORIZATION              REQ-001…REQ-015, CAP-001…CAP-016, CG-001…CG-015
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
REFACTORING PLAN     R-001…R-021 executed; R-101…R-112 plan only
     ↓
AUTHORIZATION CHECK  state GRANTED; profile PUSH; 21 grants, 10 effective; section 216 re-derives
                        every decision rather than trusting the record
     ↓
EXECUTE (docs only)  → EXECUTION VERIFICATION (independent, I-012) → execution SUCCEEDED with
                        23 ALLOWED decisions, execution_verification PASSED / CONFORMING
```

Governing separation, preserved at every step: **evidence → claim → claim
verification → proposal → authorization → capability → operation → execution →
execution verification**. No stage impersonates another; repository access is not
authorization, authorization is not a capability, a capability is not an
operation, an operation is not an authorized change, an authorized change is not
an executed change, an executed change is not a conforming repository, and
`VERIFIED` is not `CONFORMING`.
