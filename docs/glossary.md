# Glossary

One canonical term per concept. Where the repository formerly used several words
for one concept (or one word for several), the conflict is recorded and the
canonical choice is fixed here. Terms are marked:

| Mark | Meaning |
| --- | --- |
| **CURRENT** | implemented in `prototype/generic-discovery-engine.user.js` (v0.7.1) |
| **DESIGNED** | specified in the design series v0.8 … v0.35, no code |
| **FUTURE** | exploratory; not specified in detail |

## Canonical definitions, usage and conflicts

| Term | Definition | Current usage in the repo | Conflicting usages found | Canonical usage | Documents corrected |
| --- | --- | --- | --- | --- | --- |
| **Candidate** | Hypothesis that a target is worth acquiring | `class Candidate`, `discover()` | "target", "URL", "work item" used loosely | a candidate is a hypothesis, keyed `type:target` | README, architecture/candidate-model |
| **Observation** | Record of what acquisition produced, including failure | `class Observation` | "evidence", "result", "validation" | observation only; never "proof" | provenance, limitations |
| **Recognition** | Interpretation of an observation by a provider | `Provider.recognize()` | "lock", "validation", "detection", "parsing" | recognition (deterministic given the observation) | provider-model, research/DVB |
| **Discovery** | One interpreted result with kind, confidence, data, provenance | `class Discovery`, `emitDiscovery()` | "finding", "resource", "knowledge" | discovery is an interpretation, not a resource | provenance, provider-model |
| **Evidence** | (DESIGNED) support for an assertion, with independence and strength | absent from code | used for observations throughout the old README | reserve for v0.16; today say *observation* | README, glossary |
| **Provenance** | Why a candidate/discovery exists: parent, mechanism, depth, hints | `parent`, `provenance{}`, `graphEdges`, ledger | "lineage", "history" | provenance records derivation; it is not evidence of truth | provenance |
| **Provider** | Recognition unit with `matches()` / `recognize()` | 7 classes + registry | "adapter", "recognizer", "parser", "crawler" | provider = recognition only | provider-model |
| **Acquisition** | Obtaining a candidate's target over a transport | `Acquisition`, `GM_xmlhttpRequest`/`fetch` | "probe", "fetch", "request", "download" | acquisition; *probe* is reserved for DESIGNED capability-aware attempts | README, scheduler |
| **Scheduler** | Decides which candidate is claimed next, under policy and budget | `claimNextCandidate()`, `AcquisitionPolicy` | "queue", "dispatcher", "crawler loop" | scheduler | scheduler |
| **Knowledge Base** | In-memory store of candidates, observations, discoveries, resources, edges, diagnostics | `class KnowledgeBase`, persisted via `serialize()` | "database", "graph", "store" | knowledge base | candidate-model, provenance |
| **Probe** | (DESIGNED) a capability-aware acquisition attempt | absent from code | used as a synonym for acquisition | do not use for current behaviour | README |
| **Expansion** | Turning a discovery into new candidates | `emitDiscovery()` → `discover()` | "generation", "extraction", "crawl" | candidate expansion, engine-owned | discovery-model |
| **Seed** | Initial candidate(s) that start a scan | `observeCurrentPage()`, DOM/network sources | "start URL", "root" | seed is a starting point, not a category of candidate | search-space |
| **Scope** | Boundary of allowed targets | `isAllowedUrl()`, `CONFIG.sameOriginOnly` | "domain" (DESIGNED concept) | scope = current origin today | candidate-model, scope |
| **Coverage** | (DESIGNED) what part of the search space was explored | absent from code | "exhausted", "complete" used for "no eligible candidate" | never claimed today | search-space |
| **Confidence** | Provider-supplied belief in an interpretation (0–1) | `Discovery.confidence`, `hints.confidence` | "score", "strength", "accuracy", "priority" | confidence = belief; priority = scheduling weight | candidate-model, scheduler |

## Core loop terms

| Canonical term | Definition | Status |
| --- | --- | --- |
| **Candidate** | A hypothesis that a resource or search point is worth acquiring, identified by `type:target` and carrying priority, depth and provenance. Not a statement that the resource exists. | CURRENT |
| **Acquisition** | The act of obtaining a candidate's target over a transport. In the prototype this is an HTTP GET. | CURRENT |
| **Observation** | The record of what acquisition actually produced: status, HTTP metadata, body, errors, timing. Failures are observations too. | CURRENT |
| **Recognition** | The interpretation of an observation by a provider, producing discoveries. Deterministic given the observation. | CURRENT |
| **Discovery** | A single interpreted result of recognition: a kind, a confidence, data, and provenance linking it to candidate and observation. | CURRENT |
| **Candidate expansion** | Turning a discovery into new candidates. Owned by the engine, not by providers. | CURRENT |
| **Scheduler** | The component that decides which candidate is claimed next: eligibility filter, priority ordering, request budget. | CURRENT |
| **Decision ledger** | The append-only, capped record of scheduling/planning/acquisition/recognition/discovery events with sequence numbers. | CURRENT |
| **Knowledge base** | The in-memory store of candidates, observations, discoveries, resources, graph edges, network events and diagnostics. | CURRENT |
| **Provenance** | The recorded reason a candidate or discovery exists: parent candidate, mechanism, depth, hints. | CURRENT (partial) |
| **Claim** | The ownership transition that makes exactly one worker responsible for a candidate. | CURRENT |
| **Provider** | A recognition unit with `matches(observation)` and `recognize(candidate, observation)`. | CURRENT |
| **Seed** | The initial candidate(s) that start a scan: the current page URL, plus DOM/network-observed URLs. | CURRENT |
| **Search space** | The set of candidates reachable from the seeds through expansion. Implicit in the prototype; explicit in the design series. Owned today by [architecture/search-space.md](architecture/search-space.md). | CURRENT (implicit) / DESIGNED (explicit) |

## Terms that formerly overlapped

| Term seen in the repository | Canonical term | Problem and action |
| --- | --- | --- |
| "probe", "acquire", "fetch" | **Acquisition** | Three words for one operation. Use *acquisition* for the operation, *probe* only for a designed capability-aware attempt (FUTURE). |
| "validation", "lock", "recognition" | **Recognition** | "Lock" is DVB terminology and must not be reused for provider matching; "validation" implied a truth judgement the code does not make. |
| "visited", "completed", "acquired", "consumed" | **status = completed / acquired** | "Visited" is a URL set used for completion bookkeeping, not a state. Candidate lifecycle states are the canonical vocabulary (see below). |
| "evidence", "observation" | **Observation** (CURRENT) / **Evidence** (DESIGNED) | The prototype stores observations; it does not build an evidence graph. Never call an observation "evidence" when describing current behaviour. |
| "knowledge graph", "discovery graph" | **Knowledge base** (CURRENT) / **Discovery graph** (DESIGNED) | The prototype keeps a flat store plus `graphEdges`; there is no queryable graph. |
| "database" | **Knowledge base** | Same object; "database" implied durability guarantees the prototype does not make. |
| "scan", "crawl", "sweep" | **Scan** | Keep *scan* for a bounded run of the loop. Avoid *crawl* (implies unrestricted crawling, a stated non-goal) and *sweep* (implies exhaustive RF-style coverage). |
| "confidence", "score", "strength" | **Confidence** | The prototype carries a per-discovery confidence and a per-candidate hint confidence; use *priority* for scheduling weight and *confidence* for belief. Never call either "accuracy". |
| "coverage", "completeness", "exhaustion" | **Coverage** (DESIGNED) / **Exhaustion** (OPEN) | The prototype has no coverage metric. Log lines saying "exhausted" describe an empty eligible set, not a proven complete search. |
| "priority queue" | **Scheduler** | The prototype sorts a Map on demand; there is no heap or queue object. |
| "status", "state" (one word for a claim) | **the five typed fields** | One word cannot say what kind of statement it is, whether it is implemented, whether it is tested, how strong the evidence is and what verification concluded. Use `claim_kind`, `implementation_state`, `test_state`, `evidence_level`, `verification_result`. |
| "authorized: true" | **`authorization.state`** + **`authorization.level`** | Permission to mutate and the capability it grants are two different questions. `GRANTED` alone does not say what may change; a level alone does not prove anything was granted. |
| "level A4 / A5" | **`CODE_REFACTOR` / `ARCHITECTURE_CHANGE`** | The A-numbered authorization names are retired; the canonical enum is `READ_ONLY` … `PUSH`. |
| "PASS", "FAIL", "clean", "successful" (as a verification verdict) | **`verification_result`** | Verification concludes `VERIFIED`, `PARTIALLY_VERIFIED`, `UNVERIFIED`, `CONTRADICTED` or `NOT_APPLICABLE`. `SUCCEEDED` belongs to `execution.result` only, and never implies verification. |
| "implemented" (as a verdict about a claim) | **`implementation_state`** | `IMPLEMENTED` describes the behaviour named in the claim; it is not a verification conclusion and not a test result. |

## State and authority vocabulary

Canonical model, enforced by `tools/validate-analysis.mjs` against
[analysis/analysis.schema.json](analysis/analysis.schema.json). Record:
[analysis/analysis.json](analysis/analysis.json).

| Field | Question | Values |
| --- | --- | --- |
| `claim_kind` | What kind of statement is this? | `CURRENT`, `SPECIFIED`, `PLANNED`, `HISTORICAL`, `HYPOTHESIS`, `NON_GOAL` |
| `implementation_state` | Is the named behaviour implemented? | `IMPLEMENTED`, `PARTIAL`, `NOT_IMPLEMENTED`, `NOT_APPLICABLE`, `UNKNOWN` |
| `test_state` | Is it exercised? | `TESTED`, `PARTIALLY_TESTED`, `UNTESTED`, `NOT_APPLICABLE`, `UNKNOWN` |
| `evidence_level` | How strong / available is the evidence? | `DIRECT`, `CORROBORATED`, `INDIRECT`, `ABSENT`, `INACCESSIBLE` |
| `verification_result` | What did verification conclude? | `VERIFIED`, `PARTIALLY_VERIFIED`, `UNVERIFIED`, `CONTRADICTED`, `NOT_APPLICABLE` |
| `authorization.state` | Has mutation authority been granted? | `NOT_REQUESTED`, `REQUESTED`, `DENIED`, `GRANTED`, `REVOKED`, `EXPIRED` |
| `authorization.level` | What does the grant permit? (capability ceiling) | `READ_ONLY`, `ANALYSIS_ONLY`, `DOC_REFACTOR`, `TEST_REFACTOR`, `CODE_REFACTOR`, `ARCHITECTURE_CHANGE`, `COMMIT`, `PUSH` |
| `execution.result` | What actually happened? | `NOT_EXECUTED`, `SUCCEEDED`, `PARTIALLY_SUCCEEDED`, `FAILED`, `STOPPED` |
| `post_verification.result` | What did the independent re-run establish? | the `verification_result` values only |
| `access_level` | How much of the repository could be inspected? | `FULL`, `PARTIAL`, `DOCUMENT_ONLY`, `SEARCH_ONLY`, `NONE` |

Terms that must not be confused: **`ABSENT`** (inspected, not found) is not
**`INACCESSIBLE`** (could not inspect); **`TESTED`** is not **`IMPLEMENTED`**;
**`PLANNED`** is not **`MISSING`**; **`DOCUMENTED`** is not **`IMPLEMENTED`**;
**`ANALOGY`** is not **`IMPLEMENTATION`**.

## Candidate lifecycle vocabulary

Canonical states as implemented, in transition order:

```
discovered → queued → claimed → planned → acquiring → observed
                                                     │
                        recognized → expanded → completed
                        (else) skipped | failed → (retry) → queued
```

| State | Meaning |
| --- | --- |
| `discovered` | constructed, not yet enqueued |
| `queued` | eligible for claiming (subject to `nextAttemptAt` backoff) |
| `claimed` | owned by exactly one worker (invariant intended, see limitations) |
| `planned` / `acquiring` | policy allowed the attempt; network work in progress |
| `observed` | an observation exists for this candidate |
| `recognized` / `expanded` | providers ran; expansion was attempted |
| `completed` | terminal success for the candidate |
| `skipped` | deliberately not acquired (policy, budget, depth) |
| `failed` | retries exhausted — but still claimable in v0.7.1 (defect D3) |

## Designed-only vocabulary

These terms appear only in the design series. They must not be used to describe
the prototype:

`Capability`, `WorkItem`, `Frontier`, `DiscoveryDomain`, `ScanSession`,
`Evidence`, `Claim` (as an assertion of truth — distinct from candidate
claiming), `Classification`, `Locator`, `Artifact`, `Revision`, `Coverage`,
`Absence`, `Completeness`, `Lease`, `Fencing token`, `Conflict record`.

**Naming hazard:** *claim* means two different things in this repository —
ownership of work (CURRENT) and an assertion about the world (DESIGNED). Keep
"claim a candidate" for ownership; write "assertion" or "evidence-backed claim"
for the designed sense.
