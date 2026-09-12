# Compatibility Envelope

> **Input status: INPUT_CONTRACT_FAILED.** Protocol-v1 source integrity fails and required Protocol-v4 through Protocol-v7 artifacts are missing. This is a structurally validated, downgraded source-local corpus—not an accepted complete v10.1 synthesis. Missing evidence is not evidence of absence.

```text
MUST PRESERVE
MAY CHANGE WITH EQUIVALENCE PROOF
FREE TO REDESIGN
```

## Must preserve
| Obligation | Statement |
|---|---|
| OBL-CANDIDATE-IDENTITY | A candidate must retain stable identity or a lossless identity mapping across its lifecycle. |
| OBL-DEDUP-SCOPES | Queue, claim, processing, discovery, persistence, and export deduplication must be specified and verified independently. |
| OBL-ACQ-BEFORE-INTERP | Acquisition must remain semantically distinct and produce evidence before recognition. |
| OBL-ACQ-OUTCOME | Every attempted acquisition must yield an observation outcome or an explicit attributable failure outcome. |
| OBL-ACQ-TIMEOUT | Each acquisition must remain under an explicit finite timeout or stronger encompassing deadline, with timeout exposed distinctly. |
| OBL-ACQ-SCOPE | Requested and redirected targets must be validated against declared network authority and scope. |
| OBL-OBS-DISTINCT | Acquisition evidence must remain represented separately from interpreted Discovery records. |
| OBL-OBS-SOURCE | Each observation must retain an unambiguous candidate correlation or explicit orphan classification. |
| OBL-RECOGNITION-DISTINCT | Recognition must remain semantically separable from acquisition and operate on represented observation evidence. |
| OBL-DISCOVERY-RECORD | Discovery kind/data and candidate/observation correlation must be preserved; populated confidence/timestamps require migration or versioning if removed. |
| OBL-EXPANSION-RECURSIVE | Discoveries must remain able to yield candidate work that re-enters scheduling under explicit bounds. |
| OBL-EXPANSION-VS-RETRY | New-child expansion and same-candidate retry must remain separate operations with separate provenance and bounds. |
| OBL-KNOWLEDGE | Candidate, observation, and discovery outcomes required by scheduling, provenance, and reporting must remain queryable for the applicable scope. |
| OBL-BOUNDED-CONCURRENCY | Active work concurrency must have an explicit finite bound. |
| OBL-PROVENANCE | Populated Discovery→Observation→Candidate→Parent→Origin associations must be retained; missing edges must stay explicit. |
| OBL-REMOTE-DATA | Acquired content must remain untrusted input data, not trusted executable code, absent a separately authorized contained execution contract. |
| OBL-PARSER | Malformed remote content must remain inside its parser/provider failure boundary and never become trusted execution or unmarked success. |
| OBL-RESOURCE | Candidate, request, concurrency, timeout, retry, response/body, parser, and retained-state growth must remain finitely bounded or covered by a stronger bound. |
| OBL-CONTRACT-INPUT | Validated Protocol-v7 contract evidence must be available before any contract transition, compatibility, strengthening, weakening, replacement, or retirement conclusion is accepted. |
| OBL-REGRESSION | Every REQUIRED or dependency-critical obligation must have executable verification before status VERIFIED. |

## May change with equivalence proof
| Obligation | Allowed |
|---|---|
| OBL-CANDIDATE-EQUIVALENCE | Any mechanism preserving the declared semantics |
| OBL-CANDIDATE-ORIGIN | Any mechanism preserving the declared semantics |
| OBL-CANDIDATE-PARENT | Any mechanism preserving the declared semantics |
| OBL-CANDIDATE-STATE | Any mechanism preserving the declared semantics |
| OBL-CANDIDATE-PRIORITY | Any mechanism preserving the declared semantics |
| OBL-CANDIDATE-ATTEMPTS | Any mechanism preserving the declared semantics |
| OBL-CANDIDATE-TIMESTAMPS | Any mechanism preserving the declared semantics |
| OBL-CLAIM-EXCLUSIVITY | Any mechanism preserving the declared semantics |
| OBL-TERMINAL-OWNERSHIP | Any mechanism preserving the declared semantics |
| OBL-ACQ-METADATA | Any mechanism preserving the declared semantics |
| OBL-CANCELLATION | Any mechanism preserving the declared semantics |
| OBL-OBS-OUTCOMES | Any mechanism preserving the declared semantics |
| OBL-RECOGNITION-OUTCOMES | Any mechanism preserving the declared semantics |
| OBL-PROVIDER-CONTRACT | Any mechanism preserving the declared semantics |
| OBL-PROVIDER-FAILURE | Any mechanism preserving the declared semantics |
| OBL-PROVIDER-ORDER | Any mechanism preserving the declared semantics |
| OBL-CANDIDATE-ADMISSION | Any mechanism preserving the declared semantics |
| OBL-SCHEDULER-TERMINATION | Any mechanism preserving the declared semantics |
| OBL-WORKER-FAILURE | Any mechanism preserving the declared semantics |
| OBL-RETRY | Any mechanism preserving the declared semantics |
| OBL-PROVENANCE-INTEGRITY | Any mechanism preserving the declared semantics |
| OBL-AUTHORITY | Any mechanism preserving the declared semantics |
| OBL-UNBOUNDED | Any mechanism preserving the declared semantics |
| OBL-LIFECYCLE-OBS | Any mechanism preserving the declared semantics |
| OBL-AUDIT | Any mechanism preserving the declared semantics |
| OBL-SILENT-FAILURE | Any mechanism preserving the declared semantics |
| OBL-PERSIST-COMPAT | Any mechanism preserving the declared semantics |
| OBL-PERSIST-CORRUPTION | Any mechanism preserving the declared semantics |
| OBL-EXPORT | Any mechanism preserving the declared semantics |
| OBL-UI | Any mechanism preserving the declared semantics |
| OBL-PRIVATE-SHAPE | Any mechanism preserving the declared semantics |
| OBL-ERROR-CONTRACT | Any mechanism preserving the declared semantics |
| OBL-PARSE-DEFECT | Any mechanism preserving the declared semantics |
| OBL-WEB-GENERALIZE | Any mechanism preserving the declared semantics |

## Free to redesign
Function/class names, private modules, language, UI styling, log formatting, concrete containers, and worker mechanics. Semantic equivalence—not source identity—governs refactoring.
