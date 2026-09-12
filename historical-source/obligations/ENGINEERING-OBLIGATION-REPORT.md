# Generic Discovery Engine — Protocol-v10.1 Obligations

> **Input status: INPUT_CONTRACT_FAILED.** Protocol-v1 source integrity fails and required Protocol-v4 through Protocol-v7 artifacts are missing. This is a structurally validated, downgraded source-local corpus—not an accepted complete v10.1 synthesis. Missing evidence is not evidence of absence.

## 1. Scope

Typed, dependency-aware engineering consequences are derived only after input normalization. No future architecture is selected.

## 2. Evidence Boundary

`INPUT-CONTRACT.yaml` records `INPUT_CONTRACT_FAILED`: v1 is unverified/hash-mismatched and v4-v7 are `INPUT_MISSING`. The corpus is downgraded; missing evidence is not evidence of absence.

## 3. Historical Properties

26 normalized evidence records support 144 historical facts and 198 properties. Evidence, property, obligation, class, strength, epistemic status, final category, and lifecycle remain independent.

## 4. Mandatory Preservation Obligations

| ID | Statement | Class | Strength | Category | Epistemic | Lifecycle | Closure |
|---|---|---|---|---|---|---|---|
| OBL-CANDIDATE-IDENTITY | A candidate must retain stable identity or a lossless identity mapping across its lifecycle. | PRESERVE | REQUIRED | PRESERVATION_OBLIGATION | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-ACQ-BEFORE-INTERP | Acquisition must remain semantically distinct and produce evidence before recognition. | PRESERVE | REQUIRED | PRESERVATION_OBLIGATION | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-ACQ-TIMEOUT | Each acquisition must remain under an explicit finite timeout or stronger encompassing deadline, with timeout exposed distinctly. | PRESERVE | REQUIRED | PRESERVATION_OBLIGATION | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-OBS-DISTINCT | Acquisition evidence must remain represented separately from interpreted Discovery records. | PRESERVE | REQUIRED | PRESERVATION_OBLIGATION | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-OBS-SOURCE | Each observation must retain an unambiguous candidate correlation or explicit orphan classification. | PRESERVE | REQUIRED | PRESERVATION_OBLIGATION | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-RECOGNITION-DISTINCT | Recognition must remain semantically separable from acquisition and operate on represented observation evidence. | PRESERVE | REQUIRED | PRESERVATION_OBLIGATION | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-DISCOVERY-RECORD | Discovery kind/data and candidate/observation correlation must be preserved; populated confidence/timestamps require migration or versioning if removed. | PRESERVE | REQUIRED | PRESERVATION_OBLIGATION | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-EXPANSION-RECURSIVE | Discoveries must remain able to yield candidate work that re-enters scheduling under explicit bounds. | PRESERVE | REQUIRED | PRESERVATION_OBLIGATION | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-KNOWLEDGE | Candidate, observation, and discovery outcomes required by scheduling, provenance, and reporting must remain queryable for the applicable scope. | PRESERVE | REQUIRED | PRESERVATION_OBLIGATION | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-BOUNDED-CONCURRENCY | Active work concurrency must have an explicit finite bound. | PRESERVE | REQUIRED | PRESERVATION_OBLIGATION | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-PROVENANCE | Populated Discovery→Observation→Candidate→Parent→Origin associations must be retained; missing edges must stay explicit. | PRESERVE | REQUIRED | PRESERVATION_OBLIGATION | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-RESOURCE | Candidate, request, concurrency, timeout, retry, response/body, parser, and retained-state growth must remain finitely bounded or covered by a stronger bound. | PRESERVE | REQUIRED | PRESERVATION_OBLIGATION | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |

## 5. Compatibility Obligations

| ID | Statement | Class | Strength | Category | Epistemic | Lifecycle | Closure |
|---|---|---|---|---|---|---|---|
| OBL-CANDIDATE-PRIORITY | If priority affects consumers or operations, its ordering semantics must be preserved or versioned; otherwise it must be documented as advisory. | COMPATIBILITY | CONDITIONAL | COMPATIBILITY_OBLIGATION | INFERRED | FORMALIZED | OBLIGATION_UNVERIFIED |
| OBL-PROVIDER-ORDER | Provider ordering must not be promised stable until external dependence and selection semantics are established; if promised, order changes require versioning or equivalence proof. | COMPATIBILITY | CONDITIONAL | COMPATIBILITY_OBLIGATION | UNKNOWN | FORMALIZED | OBLIGATION_UNVERIFIED |
| OBL-PERSIST-COMPAT | If historical state is consumed, schema versions, validation, semantic migration, and explicit rejection of incompatible data are required. | COMPATIBILITY | CONDITIONAL | COMPATIBILITY_OBLIGATION | SUPPORTED | FORMALIZED | OBLIGATION_UNVERIFIED |

## 6. Algorithmic Obligations

| ID | Statement | Class | Strength | Category | Epistemic | Lifecycle | Closure |
|---|---|---|---|---|---|---|---|
| OBL-EXPANSION-RECURSIVE | Discoveries must remain able to yield candidate work that re-enters scheduling under explicit bounds. | PRESERVE | REQUIRED | PRESERVATION_OBLIGATION | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-EXPANSION-VS-RETRY | New-child expansion and same-candidate retry must remain separate operations with separate provenance and bounds. | STABILIZE | REQUIRED | ENGINEERING_REQUIREMENT | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |

## 7. Candidate Obligations

| ID | Statement | Class | Strength | Category | Epistemic | Lifecycle | Closure |
|---|---|---|---|---|---|---|---|
| OBL-CANDIDATE-IDENTITY | A candidate must retain stable identity or a lossless identity mapping across its lifecycle. | PRESERVE | REQUIRED | PRESERVATION_OBLIGATION | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-CANDIDATE-EQUIVALENCE | Before compatibility is promised, candidate equivalence must explicitly keep target, type, origin, parent, provider, and scope dimensions independent. | FORMALIZE | CONDITIONAL | FUTURE_STRENGTHENING | UNKNOWN | FORMALIZED | OBLIGATION_UNVERIFIED |
| OBL-DEDUP-SCOPES | Queue, claim, processing, discovery, persistence, and export deduplication must be specified and verified independently. | FORMALIZE | REQUIRED | ENGINEERING_REQUIREMENT | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-CANDIDATE-ORIGIN | Populated candidate origin must be retained or migrated to an equivalent provenance reference. | PRESERVE | CONDITIONAL | PRESERVATION_OBLIGATION | SUPPORTED | FORMALIZED | OBLIGATION_UNVERIFIED |
| OBL-CANDIDATE-PARENT | Expanded candidates must retain parentage or an equivalent derivation edge; roots may remain parentless. | PRESERVE | CONDITIONAL | PRESERVATION_OBLIGATION | SUPPORTED | FORMALIZED | OBLIGATION_UNVERIFIED |
| OBL-CANDIDATE-STATE | Legal candidate state transitions, owners, postconditions, terminal outcomes, and retry re-entry must be explicit. | FORMALIZE | REQUIRED | FUTURE_STRENGTHENING | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-CANDIDATE-PRIORITY | If priority affects consumers or operations, its ordering semantics must be preserved or versioned; otherwise it must be documented as advisory. | COMPATIBILITY | CONDITIONAL | COMPATIBILITY_OBLIGATION | INFERRED | FORMALIZED | OBLIGATION_UNVERIFIED |
| OBL-CANDIDATE-ATTEMPTS | Retry-enabled work must advance observable attempt accounting and preserve exhaustion semantics. | PRESERVE | CONDITIONAL | PRESERVATION_OBLIGATION | SUPPORTED | FORMALIZED | OBLIGATION_UNVERIFIED |
| OBL-CANDIDATE-TIMESTAMPS | Operationally retained timestamps must have explicit clock, ordering, and nullability semantics before contractual use. | OBSERVE | CONDITIONAL | FUTURE_STRENGTHENING | SUPPORTED | FORMALIZED | OBLIGATION_UNVERIFIED |
| OBL-CLAIM-EXCLUSIVITY | When workers overlap, exactly one worker may own a candidate within the declared concurrency scope. | PRESERVE | CONDITIONAL | ENGINEERING_REQUIREMENT | SUPPORTED | FORMALIZED | OBLIGATION_UNVERIFIED |
| OBL-TERMINAL-OWNERSHIP | Every claim must receive one attributable completion, failure, expiry, or explicit abandonment outcome. | FORMALIZE | REQUIRED | FUTURE_STRENGTHENING | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-CANDIDATE-ADMISSION | Admission must define identity checking, reject/merge behavior, provenance retention, bounds, and recursive eligibility. | FORMALIZE | REQUIRED | FUTURE_STRENGTHENING | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |

## 8. Acquisition Obligations

| ID | Statement | Class | Strength | Category | Epistemic | Lifecycle | Closure |
|---|---|---|---|---|---|---|---|
| OBL-ACQ-BEFORE-INTERP | Acquisition must remain semantically distinct and produce evidence before recognition. | PRESERVE | REQUIRED | PRESERVATION_OBLIGATION | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-ACQ-OUTCOME | Every attempted acquisition must yield an observation outcome or an explicit attributable failure outcome. | STABILIZE | REQUIRED | ENGINEERING_REQUIREMENT | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-ACQ-METADATA | Observations must retain metadata sufficient for interpretation, attribution, and diagnosis; exact representation may change equivalently. | PRESERVE | CONDITIONAL | PRESERVATION_OBLIGATION | SUPPORTED | FORMALIZED | OBLIGATION_UNVERIFIED |
| OBL-ACQ-TIMEOUT | Each acquisition must remain under an explicit finite timeout or stronger encompassing deadline, with timeout exposed distinctly. | PRESERVE | REQUIRED | PRESERVATION_OBLIGATION | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-ACQ-SCOPE | Requested and redirected targets must be validated against declared network authority and scope. | CONTAIN | REQUIRED | ENGINEERING_REQUIREMENT | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-CANCELLATION | If cancellation is exposed, transport stop, candidate outcome, propagation, state preservation, and scheduler termination must be verified separately. | VERIFY | CONDITIONAL | FUTURE_STRENGTHENING | SUPPORTED | FORMALIZED | OBLIGATION_UNVERIFIED |
| OBL-WEB-GENERALIZE | A generalized acquisition layer may add protocols only while preserving a versioned compatible web behavior envelope. | GENERALIZE | RECOMMENDED | FUTURE_STRENGTHENING | SUPPORTED | FORMALIZED | OBLIGATION_UNVERIFIED |

## 9. Observation Obligations

| ID | Statement | Class | Strength | Category | Epistemic | Lifecycle | Closure |
|---|---|---|---|---|---|---|---|
| OBL-ACQ-METADATA | Observations must retain metadata sufficient for interpretation, attribution, and diagnosis; exact representation may change equivalently. | PRESERVE | CONDITIONAL | PRESERVATION_OBLIGATION | SUPPORTED | FORMALIZED | OBLIGATION_UNVERIFIED |
| OBL-OBS-DISTINCT | Acquisition evidence must remain represented separately from interpreted Discovery records. | PRESERVE | REQUIRED | PRESERVATION_OBLIGATION | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-OBS-SOURCE | Each observation must retain an unambiguous candidate correlation or explicit orphan classification. | PRESERVE | REQUIRED | PRESERVATION_OBLIGATION | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-OBS-OUTCOMES | Success, failure, timeout, cancellation, partial/truncated, and empty outcomes must remain semantically distinct. | STABILIZE | REQUIRED | FUTURE_STRENGTHENING | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |

## 10. Recognition Obligations

| ID | Statement | Class | Strength | Category | Epistemic | Lifecycle | Closure |
|---|---|---|---|---|---|---|---|
| OBL-RECOGNITION-DISTINCT | Recognition must remain semantically separable from acquisition and operate on represented observation evidence. | PRESERVE | REQUIRED | PRESERVATION_OBLIGATION | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-RECOGNITION-OUTCOMES | Non-applicability, applicable-with-no-discovery, provider failure, and partial discovery must be distinct outcomes. | FORMALIZE | REQUIRED | FUTURE_STRENGTHENING | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |

## 11. Discovery Obligations

| ID | Statement | Class | Strength | Category | Epistemic | Lifecycle | Closure |
|---|---|---|---|---|---|---|---|
| OBL-DISCOVERY-RECORD | Discovery kind/data and candidate/observation correlation must be preserved; populated confidence/timestamps require migration or versioning if removed. | PRESERVE | REQUIRED | PRESERVATION_OBLIGATION | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-PROVENANCE | Populated Discovery→Observation→Candidate→Parent→Origin associations must be retained; missing edges must stay explicit. | PRESERVE | REQUIRED | PRESERVATION_OBLIGATION | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |

## 12. Expansion Obligations

| ID | Statement | Class | Strength | Category | Epistemic | Lifecycle | Closure |
|---|---|---|---|---|---|---|---|
| OBL-EXPANSION-RECURSIVE | Discoveries must remain able to yield candidate work that re-enters scheduling under explicit bounds. | PRESERVE | REQUIRED | PRESERVATION_OBLIGATION | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-EXPANSION-VS-RETRY | New-child expansion and same-candidate retry must remain separate operations with separate provenance and bounds. | STABILIZE | REQUIRED | ENGINEERING_REQUIREMENT | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-CANDIDATE-ADMISSION | Admission must define identity checking, reject/merge behavior, provenance retention, bounds, and recursive eligibility. | FORMALIZE | REQUIRED | FUTURE_STRENGTHENING | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-RESOURCE | Candidate, request, concurrency, timeout, retry, response/body, parser, and retained-state growth must remain finitely bounded or covered by a stronger bound. | PRESERVE | REQUIRED | PRESERVATION_OBLIGATION | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |

## 13. Scheduler Obligations

| ID | Statement | Class | Strength | Category | Epistemic | Lifecycle | Closure |
|---|---|---|---|---|---|---|---|
| OBL-CANDIDATE-STATE | Legal candidate state transitions, owners, postconditions, terminal outcomes, and retry re-entry must be explicit. | FORMALIZE | REQUIRED | FUTURE_STRENGTHENING | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-CANDIDATE-PRIORITY | If priority affects consumers or operations, its ordering semantics must be preserved or versioned; otherwise it must be documented as advisory. | COMPATIBILITY | CONDITIONAL | COMPATIBILITY_OBLIGATION | INFERRED | FORMALIZED | OBLIGATION_UNVERIFIED |
| OBL-CLAIM-EXCLUSIVITY | When workers overlap, exactly one worker may own a candidate within the declared concurrency scope. | PRESERVE | CONDITIONAL | ENGINEERING_REQUIREMENT | SUPPORTED | FORMALIZED | OBLIGATION_UNVERIFIED |
| OBL-TERMINAL-OWNERSHIP | Every claim must receive one attributable completion, failure, expiry, or explicit abandonment outcome. | FORMALIZE | REQUIRED | FUTURE_STRENGTHENING | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-CANCELLATION | If cancellation is exposed, transport stop, candidate outcome, propagation, state preservation, and scheduler termination must be verified separately. | VERIFY | CONDITIONAL | FUTURE_STRENGTHENING | SUPPORTED | FORMALIZED | OBLIGATION_UNVERIFIED |
| OBL-CANDIDATE-ADMISSION | Admission must define identity checking, reject/merge behavior, provenance retention, bounds, and recursive eligibility. | FORMALIZE | REQUIRED | FUTURE_STRENGTHENING | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-KNOWLEDGE | Candidate, observation, and discovery outcomes required by scheduling, provenance, and reporting must remain queryable for the applicable scope. | PRESERVE | REQUIRED | PRESERVATION_OBLIGATION | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-BOUNDED-CONCURRENCY | Active work concurrency must have an explicit finite bound. | PRESERVE | REQUIRED | PRESERVATION_OBLIGATION | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-SCHEDULER-TERMINATION | Completion may be reported only when no admissible queued or in-flight work can add candidates, or explicit stop policy accounts for it. | FORMALIZE | REQUIRED | FUTURE_STRENGTHENING | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-WORKER-FAILURE | Worker failure must leave owned work in one explicit recoverable or terminal state without corrupting unrelated frontier state. | CONTAIN | REQUIRED | FUTURE_STRENGTHENING | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-PRIVATE-SHAPE | Private names, class/module grouping, language, and Map/Set layout may be deprecated or refactored with semantic equivalence. | DEPRECATE | RECOMMENDED | DESIGN_OPTION | INFERRED | FORMALIZED | OBLIGATION_UNVERIFIED |

## 14. Concurrency Obligations

| ID | Statement | Class | Strength | Category | Epistemic | Lifecycle | Closure |
|---|---|---|---|---|---|---|---|
| OBL-CLAIM-EXCLUSIVITY | When workers overlap, exactly one worker may own a candidate within the declared concurrency scope. | PRESERVE | CONDITIONAL | ENGINEERING_REQUIREMENT | SUPPORTED | FORMALIZED | OBLIGATION_UNVERIFIED |
| OBL-CANCELLATION | If cancellation is exposed, transport stop, candidate outcome, propagation, state preservation, and scheduler termination must be verified separately. | VERIFY | CONDITIONAL | FUTURE_STRENGTHENING | SUPPORTED | FORMALIZED | OBLIGATION_UNVERIFIED |
| OBL-BOUNDED-CONCURRENCY | Active work concurrency must have an explicit finite bound. | PRESERVE | REQUIRED | PRESERVATION_OBLIGATION | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-SCHEDULER-TERMINATION | Completion may be reported only when no admissible queued or in-flight work can add candidates, or explicit stop policy accounts for it. | FORMALIZE | REQUIRED | FUTURE_STRENGTHENING | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-WORKER-FAILURE | Worker failure must leave owned work in one explicit recoverable or terminal state without corrupting unrelated frontier state. | CONTAIN | REQUIRED | FUTURE_STRENGTHENING | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |

## 15. Provider Obligations

| ID | Statement | Class | Strength | Category | Epistemic | Lifecycle | Closure |
|---|---|---|---|---|---|---|---|
| OBL-PROVIDER-CONTRACT | Any exposed provider API must define matching, output, expansion ownership, failure, ordering, lifecycle, cancellation, and provenance. | FORMALIZE | CONDITIONAL | FUTURE_STRENGTHENING | SUPPORTED | FORMALIZED | OBLIGATION_UNVERIFIED |
| OBL-PROVIDER-ORDER | Provider ordering must not be promised stable until external dependence and selection semantics are established; if promised, order changes require versioning or equivalence proof. | COMPATIBILITY | CONDITIONAL | COMPATIBILITY_OBLIGATION | UNKNOWN | FORMALIZED | OBLIGATION_UNVERIFIED |

## 16. Provenance Obligations

| ID | Statement | Class | Strength | Category | Epistemic | Lifecycle | Closure |
|---|---|---|---|---|---|---|---|
| OBL-CANDIDATE-ORIGIN | Populated candidate origin must be retained or migrated to an equivalent provenance reference. | PRESERVE | CONDITIONAL | PRESERVATION_OBLIGATION | SUPPORTED | FORMALIZED | OBLIGATION_UNVERIFIED |
| OBL-CANDIDATE-PARENT | Expanded candidates must retain parentage or an equivalent derivation edge; roots may remain parentless. | PRESERVE | CONDITIONAL | PRESERVATION_OBLIGATION | SUPPORTED | FORMALIZED | OBLIGATION_UNVERIFIED |
| OBL-OBS-SOURCE | Each observation must retain an unambiguous candidate correlation or explicit orphan classification. | PRESERVE | REQUIRED | PRESERVATION_OBLIGATION | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-PROVENANCE | Populated Discovery→Observation→Candidate→Parent→Origin associations must be retained; missing edges must stay explicit. | PRESERVE | REQUIRED | PRESERVATION_OBLIGATION | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-PROVENANCE-INTEGRITY | Integrity claims require verified writers, mutation authorization, persistence, forgery resistance, and cryptographic properties independently. | VERIFY | CONDITIONAL | FUTURE_STRENGTHENING | SUPPORTED | FORMALIZED | OBLIGATION_UNVERIFIED |

## 17. Failure Obligations

| ID | Statement | Class | Strength | Category | Epistemic | Lifecycle | Closure |
|---|---|---|---|---|---|---|---|
| OBL-CANDIDATE-ATTEMPTS | Retry-enabled work must advance observable attempt accounting and preserve exhaustion semantics. | PRESERVE | CONDITIONAL | PRESERVATION_OBLIGATION | SUPPORTED | FORMALIZED | OBLIGATION_UNVERIFIED |
| OBL-PROVIDER-FAILURE | Provider failure must be attributable and must not corrupt global scheduler state; narrower isolation requires explicit verification. | CONTAIN | CONDITIONAL | FUTURE_STRENGTHENING | SUPPORTED | FORMALIZED | OBLIGATION_UNVERIFIED |
| OBL-RETRY | Only declared retryable failures may retry; attempts, error provenance, finite bounds, backoff, and terminal exhaustion must be explicit. | FORMALIZE | REQUIRED | FUTURE_STRENGTHENING | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-SILENT-FAILURE | Failure affecting completeness, lifecycle, or trust decisions must be explicit failure, partial result, or policy skip—not silent success. | REJECT | REQUIRED | FUTURE_STRENGTHENING | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |

## 18. Security Obligations

| ID | Statement | Class | Strength | Category | Epistemic | Lifecycle | Closure |
|---|---|---|---|---|---|---|---|
| OBL-ACQ-SCOPE | Requested and redirected targets must be validated against declared network authority and scope. | CONTAIN | REQUIRED | ENGINEERING_REQUIREMENT | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-REMOTE-DATA | Acquired content must remain untrusted input data, not trusted executable code, absent a separately authorized contained execution contract. | CONTAIN | REQUIRED | ENGINEERING_REQUIREMENT | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-AUTHORITY | Required, granted, used, and exposed authority must be declared separately and excess authority explicitly approved or rejected. | FORMALIZE | REQUIRED | FUTURE_STRENGTHENING | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-PARSER | Malformed remote content must remain inside its parser/provider failure boundary and never become trusted execution or unmarked success. | CONTAIN | REQUIRED | ENGINEERING_REQUIREMENT | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |

## 19. Resource Obligations

| ID | Statement | Class | Strength | Category | Epistemic | Lifecycle | Closure |
|---|---|---|---|---|---|---|---|
| OBL-ACQ-TIMEOUT | Each acquisition must remain under an explicit finite timeout or stronger encompassing deadline, with timeout exposed distinctly. | PRESERVE | REQUIRED | PRESERVATION_OBLIGATION | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-RESOURCE | Candidate, request, concurrency, timeout, retry, response/body, parser, and retained-state growth must remain finitely bounded or covered by a stronger bound. | PRESERVE | REQUIRED | PRESERVATION_OBLIGATION | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-UNBOUNDED | Future designs must reject unbounded remote response retention, task spawning, or memory growth without explicit external bounds. | REJECT | REQUIRED | FUTURE_STRENGTHENING | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |

## 20. Contract Obligations

| ID | Statement | Class | Strength | Category | Epistemic | Lifecycle | Closure |
|---|---|---|---|---|---|---|---|
| OBL-CONTRACT-INPUT | Validated Protocol-v7 contract evidence must be available before any contract transition, compatibility, strengthening, weakening, replacement, or retirement conclusion is accepted. | VERIFY | REQUIRED | ENGINEERING_REQUIREMENT | PROVED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-ERROR-CONTRACT | Each interface must define null, undefined, empty, status, partial, returned-error, and exception semantics before changing them. | FORMALIZE | CONDITIONAL | FUTURE_STRENGTHENING | SUPPORTED | FORMALIZED | OBLIGATION_UNVERIFIED |

## 21. Serialization Obligations

| ID | Statement | Class | Strength | Category | Epistemic | Lifecycle | Closure |
|---|---|---|---|---|---|---|---|
| OBL-PERSIST-COMPAT | If historical state is consumed, schema versions, validation, semantic migration, and explicit rejection of incompatible data are required. | COMPATIBILITY | CONDITIONAL | COMPATIBILITY_OBLIGATION | SUPPORTED | FORMALIZED | OBLIGATION_UNVERIFIED |
| OBL-PERSIST-CORRUPTION | Malformed, partial, or incompatible persisted state should be detected and contained without becoming trusted active state. | CONTAIN | RECOMMENDED | FUTURE_STRENGTHENING | SUPPORTED | FORMALIZED | OBLIGATION_UNVERIFIED |
| OBL-EXPORT | Before export compatibility is promised, purpose, version, optional/null/derived fields, partial-state marker, and relationship integrity must be explicit. | FORMALIZE | CONDITIONAL | FUTURE_STRENGTHENING | SUPPORTED | FORMALIZED | OBLIGATION_UNVERIFIED |

## 22. Observability Obligations

| ID | Statement | Class | Strength | Category | Epistemic | Lifecycle | Closure |
|---|---|---|---|---|---|---|---|
| OBL-CANDIDATE-TIMESTAMPS | Operationally retained timestamps must have explicit clock, ordering, and nullability semantics before contractual use. | OBSERVE | CONDITIONAL | FUTURE_STRENGTHENING | SUPPORTED | FORMALIZED | OBLIGATION_UNVERIFIED |
| OBL-LIFECYCLE-OBS | Claim, acquisition start/completion, recognition, discovery, expansion, failure, worker lifecycle, and scan completion must be observable semantically. | OBSERVE | REQUIRED | FUTURE_STRENGTHENING | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-AUDIT | Any auditability claim must verify completeness, ordering, identity, retention, mutation protection, and forensic reconstruction separately from logging. | VERIFY | RECOMMENDED | FUTURE_STRENGTHENING | SUPPORTED | FORMALIZED | OBLIGATION_UNVERIFIED |
| OBL-UI | UI styling, layout, labels, and control arrangement may change; preserve only selected operational semantics. | OPTIONAL | OPTIONAL | DESIGN_OPTION | SUPPORTED | FORMALIZED | OBLIGATION_UNVERIFIED |

## 23. Testing Obligations

| ID | Statement | Class | Strength | Category | Epistemic | Lifecycle | Closure |
|---|---|---|---|---|---|---|---|
| OBL-REGRESSION | Every REQUIRED or dependency-critical obligation must have executable verification before status VERIFIED. | VERIFY | REQUIRED | ENGINEERING_REQUIREMENT | SUPPORTED | FORMALIZED | OBLIGATION_BLOCKED |
| OBL-PARSE-DEFECT | The snapshot-0009 parse defect must remain historical evidence but must not be reproduced as future required behavior. | REJECT | REQUIRED | HISTORICAL_DEFECT | PROVED | FORMALIZED | OBLIGATION_BLOCKED |

## 24. Essential vs Accidental Architecture

Candidate/Observation/Discovery semantics, scheduler lifecycle, recursive expansion, knowledge, and provenance associations are semantic. Source names, private grouping, language, UI presentation, logs, and containers are accidental absent contracts.

## 25. Compatibility Envelope

Preserve justified semantics; change representations only with equivalence proof; redesign accidental details freely. The failed input contract prevents full compatibility acceptance.

## 26. Migration Obligations

Identity, state, persistence, export, provider, error, and nullability changes require conditional versioning/migration when actual consumers exist.

## 27. Obligation Conflicts

6 conflicts are separate from prerequisites and retain explicit resolution status.

## 28. Verification Gaps

All tests are `UNVERIFIED`; every REQUIRED closure is `OBLIGATION_BLOCKED`. The topological order is analytical and cannot override failed input or unexecuted prerequisites.

## 29. Historical Defects

The v1 byte/range break, missing v4-v7 evidence, snapshot-0009 parse defect, possible silent failures, local-only deduplication, partial provenance, and static resource risks remain explicit.

## 30. Future Engineering Strengthenings

| ID | Statement | Reason |
|---|---|---|
| OBL-CANDIDATE-EQUIVALENCE | Before compatibility is promised, candidate equivalence must explicitly keep target, type, origin, parent, provider, and scope dimensions independent. | Deduplication and migration require a declared rule; URL equality is insufficient. |
| OBL-DEDUP-SCOPES | Queue, claim, processing, discovery, persistence, and export deduplication must be specified and verified independently. | One local check cannot establish all lifecycle uniqueness properties. |
| OBL-CANDIDATE-STATE | Legal candidate state transitions, owners, postconditions, terminal outcomes, and retry re-entry must be explicit. | Explicit transitions prevent stranded, duplicated, or falsely completed work. |
| OBL-CANDIDATE-TIMESTAMPS | Operationally retained timestamps must have explicit clock, ordering, and nullability semantics before contractual use. | Timing aids diagnosis but field presence is not trustworthy chronology. |
| OBL-TERMINAL-OWNERSHIP | Every claim must receive one attributable completion, failure, expiry, or explicit abandonment outcome. | A claim without terminal ownership can strand work and invalidate termination. |
| OBL-ACQ-SCOPE | Requested and redirected targets must be validated against declared network authority and scope. | Remote targets cross historical trust and authority boundaries. |
| OBL-CANCELLATION | If cancellation is exposed, transport stop, candidate outcome, propagation, state preservation, and scheduler termination must be verified separately. | API/control presence does not establish cancellation safety. |
| OBL-OBS-OUTCOMES | Success, failure, timeout, cancellation, partial/truncated, and empty outcomes must remain semantically distinct. | Null, empty, status, and partial outcomes are not equivalent. |
| OBL-RECOGNITION-OUTCOMES | Non-applicability, applicable-with-no-discovery, provider failure, and partial discovery must be distinct outcomes. | Conflation hides failure or loses partial results. |
| OBL-PROVIDER-CONTRACT | Any exposed provider API must define matching, output, expansion ownership, failure, ordering, lifecycle, cancellation, and provenance. | Names/signatures do not establish substitutability. |
| OBL-PROVIDER-FAILURE | Provider failure must be attributable and must not corrupt global scheduler state; narrower isolation requires explicit verification. | Partial evidence cannot be upgraded to complete isolation. |
| OBL-CANDIDATE-ADMISSION | Admission must define identity checking, reject/merge behavior, provenance retention, bounds, and recursive eligibility. | Silent drops lose provenance; non-atomic admission duplicates work. |
| OBL-SCHEDULER-TERMINATION | Completion may be reported only when no admissible queued or in-flight work can add candidates, or explicit stop policy accounts for it. | Queue emptiness alone can terminate prematurely. |
| OBL-WORKER-FAILURE | Worker failure must leave owned work in one explicit recoverable or terminal state without corrupting unrelated frontier state. | Ownership and scheduler state must remain coherent after worker failure. |
| OBL-RETRY | Only declared retryable failures may retry; attempts, error provenance, finite bounds, backoff, and terminal exhaustion must be explicit. | Unclassified retry can loop permanent failures or hide exhaustion. |
| OBL-PROVENANCE-INTEGRITY | Integrity claims require verified writers, mutation authorization, persistence, forgery resistance, and cryptographic properties independently. | Visibility is not integrity. |
| OBL-AUTHORITY | Required, granted, used, and exposed authority must be declared separately and excess authority explicitly approved or rejected. | Ambient permission is not required capability or trust. |
| OBL-UNBOUNDED | Future designs must reject unbounded remote response retention, task spawning, or memory growth without explicit external bounds. | This is resource strengthening, not a vulnerability claim. |
| OBL-LIFECYCLE-OBS | Claim, acquisition start/completion, recognition, discovery, expansion, failure, worker lifecycle, and scan completion must be observable semantically. | Diagnosis and testing require semantic events, not formatting. |
| OBL-AUDIT | Any auditability claim must verify completeness, ordering, identity, retention, mutation protection, and forensic reconstruction separately from logging. | A log or ledger-shaped object is not an audit trail. |
| OBL-SILENT-FAILURE | Failure affecting completeness, lifecycle, or trust decisions must be explicit failure, partial result, or policy skip—not silent success. | Silent semantic loss causes false success. |
| OBL-PERSIST-CORRUPTION | Malformed, partial, or incompatible persisted state should be detected and contained without becoming trusted active state. | This strengthens incomplete handling without backfilling history. |
| OBL-EXPORT | Before export compatibility is promised, purpose, version, optional/null/derived fields, partial-state marker, and relationship integrity must be explicit. | Identical JSON can be observability, persistence, interchange, or API. |
| OBL-ERROR-CONTRACT | Each interface must define null, undefined, empty, status, partial, returned-error, and exception semantics before changing them. | These outcomes are semantically distinct despite missing v7. |
| OBL-REGRESSION | Every REQUIRED or dependency-critical obligation must have executable verification before status VERIFIED. | Static archaeology cannot verify a future implementation. |
| OBL-PARSE-DEFECT | The snapshot-0009 parse defect must remain historical evidence but must not be reproduced as future required behavior. | Exactness is not executability; defects are not future requirements. |
| OBL-WEB-GENERALIZE | A generalized acquisition layer may add protocols only while preserving a versioned compatible web behavior envelope. | Generalization must not rewrite historical scope or discard validated web behavior. |

## 31. Final Obligation Set

| Class | Count |
|---|---|
| COMPATIBILITY | 3 |
| CONTAIN | 6 |
| DEPRECATE | 1 |
| FORMALIZE | 12 |
| GENERALIZE | 1 |
| OBSERVE | 2 |
| OPTIONAL | 1 |
| PRESERVE | 17 |
| REJECT | 3 |
| STABILIZE | 3 |
| VERIFY | 5 |

| Strength | Count |
|---|---|
| CONDITIONAL | 16 |
| OPTIONAL | 1 |
| RECOMMENDED | 4 |
| REQUIRED | 33 |

| Dependency | Count |
|---|---|
| REQUIRES | 94 |
| non-REQUIRES analytical | 6 |
| cycles | 0 |

**Final disposition: `INPUT_CONTRACT_FAILED`; structural synthesis is downgraded and not accepted as complete.**
