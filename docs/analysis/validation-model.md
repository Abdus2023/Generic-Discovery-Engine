# Validation model

Canonical owner of how this repository's analysis record is validated. Brief 11
(sections 218–243) is normative here; where an earlier brief said something
different about validation, this document supersedes it and says so.

Three concerns are separated, and the separation is the point of the model:

```
                       INPUT DOCUMENT
                             │
                             ▼
                    ┌─────────────────┐
                    │ STRUCTURAL      │  docs/analysis/analysis.schema.json
                    │ SCHEMA          │  object structure, protocol enums,
                    └────────┬────────┘  local required fields, nullability,
                             │           identifier syntax
                             ▼
                    ┌─────────────────┐
                    │ SEMANTIC        │  docs/analysis/registries/*.json
                    │ REGISTRIES      │  externally governed vocabularies
                    └────────┬────────┘  and policy
                             │
                ┌────────────┴────────────┐
                ▼                         ▼
        POLICY REGISTRIES          REPOSITORY STATE
                │                         │
                └────────────┬────────────┘
                             ▼
                    ┌─────────────────┐
                    │ SEMANTIC        │  tools/validate-analysis.mjs
                    │ VALIDATOR       │  references and relationships
                    └────────┬────────┘
                             ▼
                    ┌─────────────────┐
                    │ AUTHORIZATION   │  the section 216 function
                    │ ENGINE          │
                    └────────┬────────┘
                             ▼
                         EXECUTION  →  EXECUTION VERIFICATION
```

**Schema says what shape is legal. Registry says what identifiers mean. Semantic
validation says whether references and relationships are legal. Authorization says
whether this actor may act. Execution records what actually happened. Verification
determines whether the result conforms.** No layer promotes information into
another: a string that satisfies a pattern is not thereby a capability, and a
capability that exists in a registry is not thereby granted.

## 1. What each layer owns

### Structural schema — `analysis.schema.json`

Owns object structure, property names, primitive types, arrays, the enums that are
**intrinsic to the protocol**, local required fields, local nullability, formats,
identifier syntax and `additionalProperties`.

Enums that remain in the schema, with the reason they are protocol rather than
inventory:

| Enum | Why it is structural |
| --- | --- |
| `claim_kind`, `implementation_state`, `test_state`, `evidence_level`, `claim_verification.result`, `confidence` | the claim model itself (briefs 5–9); a claim has exactly these dimensions |
| `authorization.state` | the authorization lifecycle (section 203) |
| `capability_grant.state` | the grant lifecycle: `ENABLED`, `RESTRICTED`, `DENIED`, `REVOKED`, `EXPIRED` |
| `execution.state`, `operation.result`, `operation.authorization_decision` | the execution protocol |
| `execution_verification.state`, `.result`, `checks[].result` | the verification protocol |
| `change.category`, `change.risk`, `repository.access_level`, `evidence.kind`, `authority.type` | classifiers of a single object, fixed by the briefs |

Enums that are **not** in the schema, because the vocabulary is expected to evolve
(sections 218.3, 219, 225):

| Field | Schema says | Registry decides |
| --- | --- | --- |
| `authorization.capability_grants[].capability_id` | `string`, `^CAP-[A-Z0-9_-]+$` | `capability` — resource class, operations, scope model, grantability |
| `authorization.level.profile` | `string`, `^[A-Z][A-Z0-9_]*$` | `level_profile` — inheritance and declared capabilities |
| `authorization.operations.allow/deny[]`, `execution.operations[].operation` | `string`, `^[A-Z][A-Z0-9_]*$` | `operation` — recognized, and whether it mutates |
| `execution.operations[].target.resource_class` | `string`, `^[A-Z][A-Z0-9_]*$` | `resource_class` |
| `claims[].id` | `string`, `^CLAIM-[0-9]{3,}$` | `claim` — the identifier and its analysis domain |

A capability identifier is therefore *syntactically* valid on its own and
*semantically* meaningless until the registry resolves it (X-010).

### Semantic registries — `docs/analysis/registries/`

Five registries, each a versioned object with the required fields
`schema_version`, `registry_id`, `registry_version`, `entries` (section 220):

| Registry | Entries | Owns |
| --- | --- | --- |
| `capability-registry.json` | 21 | resource class, operations, `constraints.scope_model` (`PATH`/`NONE`), `lifecycle.grantable` |
| `level-profile-registry.json` | 8 | `inherits`, `capabilities` |
| `operation-registry.json` | 10 | `mutating` |
| `resource-class-registry.json` | 8 | the class vocabulary |
| `claim-registry.json` | 41 | claim identifier to analysis domain |

`registry.schema.json` is the structural contract of the envelope and of the five
entry shapes; which entry shape applies is selected by `registry_id`.

Registry revisions are independent of the analysis schema version — currently
registries `2026.09.1`, envelope format `1.0`, analysis schema `1.0`. A registry
revision **must be bumped whenever an entry is added, removed or redefined**; the
validator can check the form of the version but not that the bump happened, so the
rule is stated here rather than implied.

### Semantic validator — `tools/validate-analysis.mjs`

Resolves references and checks relationships (section 218.3). It is a **pure
function of its inputs**: it reads the document, the schema, the registries, the
evidence register, the YAML mirror and two restating documents, and it writes
nothing (section 241). `--json` prints the machine-readable report;
`--root <dir>` validates a snapshot of another revision without checking it out.

### Authorization engine

The section 216 function, evaluated over the *computed* effective capability set
(`profile ∩ grants − denies`, precedence `DENIED > REVOKED > EXPIRED > RESTRICTED >
ENABLED > DECLARED`). Effective capabilities are never read from the document; a
persisted effective set fails the structural phase.

## 2. Nullability: absent, null, empty

Three different states, never collapsed (section 226):

| State | Meaning | Example |
| --- | --- | --- |
| **absent** | the property does not exist: no value was supplied | an omitted `started_at` while the execution has not started |
| **null** | the property exists and is intentionally unknown, not applicable, or unset by contract | `expires_at: null` — this authorization does not expire |
| **empty** | the property exists and is known to contain no members | `change_ids: []` — there are definitely no authorized changes |

A required field may be nullable (section 227): `expires_at` is required and may be
`null`, so *omitting* it is invalid while `null` is valid. The canonical table:

| Field | Required | Nullable | Empty allowed |
| --- | --- | --- | --- |
| `schema_version` | yes | no | no |
| `repository.owner` / `.name` / `.requested_revision` / `.resolved_revision` | yes | no | no |
| `repository.included_paths` / `.excluded_paths` | yes | no | yes |
| `claim.statement` | yes | no | no |
| `claim.evidence` | yes | no | yes |
| `authorization.state` | yes | no | no |
| `authorization.level.profile` | yes | no | no |
| `authorization.capability_grants` | yes | no | yes |
| `authorization.change_ids` | yes | no | yes |
| `authorization.granted_at` | conditional — required and non-null when `state = GRANTED` | no | n/a |
| `authorization.expires_at` | yes (materialized authorization) | yes | n/a |
| `execution.started_at` | conditional — required and non-null once started | yes | n/a |
| `execution.completed_at` | conditional — required and non-null when terminal | yes | n/a |
| `execution.executed_changes` / `.unauthorized_changes` | yes | no | yes |
| `execution_verification.checks` / `.findings` | yes | no | yes |
| `execution_verification.remediation_required` | yes | no | no |

## 3. Timestamps

| Rule | Contract |
| --- | --- |
| `granted_at` | required and non-null when `authorization.state == GRANTED`; `expires_at != null` requires it |
| `expires_at` | always present; `null` means no expiry; if non-null then `expires_at >= granted_at` (TS-007) |
| `started_at` | required and non-null when the execution is `RUNNING`, `SUCCEEDED`, `PARTIALLY_SUCCEEDED`, `FAILED`, `CANCELLED` or `STOPPED`; `null` only while not started |
| `completed_at` | required and non-null for terminal states; `null` for `NOT_STARTED`, `AUTHORIZATION_BLOCKED`, `READY` and `RUNNING` |

`TS-001` `completed_at != null` ⇒ `started_at != null` · `TS-002`
`completed_at >= started_at` · `TS-003` `RUNNING` ⇒ `completed_at == null` ·
`TS-004` terminal ⇒ `completed_at != null` · `TS-005` `NOT_STARTED` ⇒
`started_at == null` · `TS-006` `AUTHORIZATION_BLOCKED` ⇒ `started_at == null` ·
`TS-007` `expires_at != null` ⇒ `expires_at >= granted_at`.

These are semantic constraints, not type constraints, and the schema does not
express them. Where two recorded timestamps are equal, that is one session
captured at a single instant, not a zero-duration execution: `TS-002` is satisfied
as an equality, and the granularity is stated where the run is recorded.

## 4. Cross-object rules (section 232)

The schema can require that `change_id` is a string; only a semantic rule can
establish that the change exists.

| Rule | Requirement |
| --- | --- |
| `X-001` | every claim and check evidence id resolves to an evidence object (and to an evidence-register row) |
| `X-002` | every change evidence id resolves |
| `X-003` … `X-006` | every `authorization.change_ids`, operation `change_id`, `executed_changes` and `unauthorized_changes` id resolves to a change in the same document |
| `X-007` / `X-008` | `authorization.target.repository` equals the repository identity; `.revision` equals `repository.resolved_revision` |
| `X-009` | `authorization.level.profile` resolves in the profile registry |
| `X-010` | every capability grant resolves in the capability registry |
| `X-011` | every granted capability is available from the resolved profile — the anti-escalation invariant |
| `X-012` / `X-014` | every authorization, execution and capability operation resolves in the operation registry |
| `X-013` / `X-015` | every operation target and capability resource class resolves in the resource-class registry |
| `X-016` | every recorded `authorization_decision` is re-derived by the section 216 function; a successful operation always carries an `ALLOWED` decision |
| `X-017` | every mutating operation references an authorized `change_id` |
| `X-018` | no successful mutation is reported while the authorization is `DENIED`, `REVOKED`, `EXPIRED` or not yet `GRANTED` |
| `X-019` | `execution_verification.execution_id` names the execution in the same document |
| `X-020` | verification checks authorize nothing: a finding may not name an authorized or executed change |

Local extensions of that set, marked as such because the brief does not name them:

| Rule | Requirement |
| --- | --- |
| `RG-001` … `RG-003` | the five registries load, validate against `registry.schema.json`, use independent versions and unique entry ids |
| `RG-004` | the claim registry and the document agree on the claim identifiers, exactly |
| `RG-005` | a capability's `scope_model` matches its resource class; only path-bearing capabilities may be restricted |
| `RG-006` | profile inheritance is acyclic and every referenced profile and capability exists |
| `RG-007` | a granted capability is `grantable` in its registry entry |
| `RG-008` | absence procedures and contradiction rows in the evidence register cover the claims that need them |
| `ST-001` / `ST-002` | schema validity; no forbidden field name (`status`, `verification`, `effective_capabilities`) |

The example cases of sections 234–240 (unknown change, capability escalation,
operation escalation, restriction, execution mismatch, verification mismatch,
nullability) are reproduced as fixtures in `tools/validation-fixtures.mjs`: each
fixture is the minimal mutation that one rule forbids, and
`node tools/validate-analysis.mjs --self-test` fails unless the validator rejects it
in the expected phase with the expected code. A rule that no fixture exercises is
not treated as enforced, and the scope model's `lifecycle.grantable` flag is
currently uniform (`true`) — the rule is executed by a fixture rather than
demonstrated by the record.

## 5. Phases and the error model (section 242)

Validation phases, with no relationship to object lifecycles:

| Phase | Contains |
| --- | --- |
| `STRUCTURAL` | schema validity (`ST-001`), forbidden field names (`ST-002`), object validity (`REQ-001`…`REQ-014`) |
| `REGISTRY` | registry loading and envelope/entry validity (`RG-001`…`RG-003`, `RG-005`), profile resolution (`X-009`, `RG-006`), vocabulary references (`X-010`, `X-012`…`X-015`) |
| `SEMANTIC` | cross-object rules `X-001`…`X-008`, `X-011`, `X-016`…`X-020`, timestamps `TS-001`…`TS-007`, claim rules `CV-001`…`CV-020`, invariants `I-001`…`I-016`, serialization, restated fields |
| `AUTHORIZATION` | `CAP-001`…`CAP-016`, `CG-001`…`CG-015` and the effective-capability computation |
| `EXECUTION` | `EV-001`…`EV-012`, coverage, the section 200 transition graph |
| `VERIFICATION` | `EVV-001`…`EVV-009` and the verification scope |

Every finding carries a machine-readable shape. When the validator fails it names
the phase, the rule and the object, so a failure can be tracked across runs:

```yaml
error:
  code: X-011
  phase: SEMANTIC
  object: authorization.capability_grants[20]
  message: capability CAP-ORBIT-CHANGE is not available from profile PUSH
  actual: [CAP-ORBIT-CHANGE]
  rules: [X-011, CAP-004, CAP-014, CG-002, CG-003, RG-007]
```

`node tools/validate-analysis.mjs --json` prints the whole report in that shape,
including the per-phase summary and the digests of every input.

## 6. Verification runs

`tools/validation-run.mjs` is the recorder, kept separate from the validator
precisely because the validator must not write:

```
before digest ──► tools/validate-analysis.mjs --json ──► after digest
      │                                                     │
      └────────────── append one entry ─────────────────────┘
                    docs/analysis/validation-runs.json
```

For every run the ledger records the mode (`WORKTREE` or `SNAPSHOT`), the
revision, the start and end timestamps, the verdict, the digest of the validator
and of every input (document, schema, registries), the per-phase state, **every
error with its code, phase, object and message**, and the tree digest before and
after with the single excluded path (`docs/analysis/validation-runs.json` — the
recorder's own output).

The ledger is append-only: an existing run id is never rewritten. `verify.mjs`
fails the repository when the newest entry does not match the current record
digest, so "the record has been validated in its current form" is a checked
statement rather than an assumption.

Recorded runs:

| Run | Mode | Verdict | What it shows |
| --- | --- | --- | --- |
| `RUN-001` | `SNAPSHOT` at `27b5977` | `INVALID` | the pre-brief-11 artifacts under the brief-11 model: no registries exist to load (`REGISTRY · LOAD-001`) — the "before" state |
| `RUN-002` | `WORKTREE` | `VALID` | the same model over the migrated artifacts, with every phase passing |

## 7. What this model does not claim

* The validator checks the *document*, not the repository's files: a scope path
  that no file uses is not detected, and `verify.mjs` is what compares the declared
  scope with `git diff`.
* `EVV-008` (verification must not mutate the repository) is procedural: it is
  measured by the run recorder's before/after tree digest, not by a schema rule.
* Registry revisions are author-maintained labels; the validator checks their form
  and their independence from the analysis schema version, not that a change
  bumped them.
* `X-020` reads verification findings as text and rejects any that names an
  authorized or executed change; it does not parse remediation prose.
