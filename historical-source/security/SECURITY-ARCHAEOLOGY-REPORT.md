# Historical Generic Discovery Failure, Security & Trust-Boundary Evolution Archaeology Report

## Result and epistemic boundary

This Protocol-v8 corpus reconstructs historical **failure handling, security mechanisms, trust/authority boundaries, resource and concurrency safety, data/provenance integrity, and execution safety** from 12 exact or mechanically composed snapshots. Two partial alternatives remain uncertainty evidence and are not complete semantic models.

`FAILURE ≠ ERROR HANDLING ≠ FAILURE CONTAINMENT ≠ RECOVERY ≠ RESILIENCE`

`SECURITY MECHANISM ≠ SECURITY PROPERTY ≠ SECURITY ASSUMPTION ≠ SECURITY GUARANTEE`

`BOUNDARY ≠ TRUST BOUNDARY ≠ AUTHORITY BOUNDARY`

No historical runtime execution, exploit, incident, or security test result is claimed. “Observed failure” below means a failure representation/detection path observed in recovered source.

Input availability in this checkout at generation time: `{"all_required_verified_inputs_available": false, "v1_v3_present": true, "v1_validation": "FAIL", "v3_validation": "PASS", "v4_present": false, "v5_present": false, "v6_present": false, "v7_present": false}`. Because the complete verified v1–v7 prerequisite set is not physically available and the available v1 validator currently reports failure, this is a **provisional source-derived v8 corpus**, not a claim of full prerequisite acceptance. The generator re-derives every v8 claim directionally from recovered source and never fabricates an absent upstream ledger.

## Central answer

The earliest recovered v0.1 is already a partial safety model: it has URL canonicalization/admission, same-origin-by-default configuration, maximum candidate/request/concurrency/time bounds, privileged and browser acquisition paths, Observation error/status recording, acquisition and persistence catches, provenance fields, and UI/export observability. It is not a verified secure system.

v0.2 adds the earliest recovered synchronous local claim protocol and reusable provider registry. Later competing branches add retry/backoff, AbortController paths, provider-local catches, richer provenance/diagnostics, response/per-origin/retention bounds, and eventually decision-ledger/policy/plan structures. These are path mechanisms. They do not establish whole-system isolation, cancellation, integrity, least authority, or resilience guarantees.

## Failure evolution

Across the recovered snapshots, mechanisms range from generic rejection/failed Observation/local logging to more differentiated parser/provider/scheduler/persistence diagnostics, retry/requeue, and structured records; this comparison does not prove monotonic lineage or superiority. Information preservation remains uneven: generic strings, null/empty fallbacks, and logging-only handlers can discard error type, stack, candidate/provider identity, request/response, or retry context.

Containment is assessed from actual handler control flow. F4–F6 labels apply only to the recovered candidate/provider/operation path. Rethrow/rejection and unresolved caller behavior remain UNKNOWN at the eventual scan boundary.

## Trust and authority

Page DOM, remote network content, providers/parsers, userscript APIs, storage, UI, and export are observable data or authority boundaries from v0.1. Internal scheduler structure is not automatically called a trust boundary. `@connect *` and privileged request APIs grant broad authority even where default policy is same-origin. Granted authority, configured policy, and actual use are tracked separately.

## Remote data and code/data boundary

Acquired HTML, JSON, XML, and text are parsed/extracted as data on located paths. No acquired-content-to-`eval`, `Function`, or dynamic-import path was found. UI `innerHTML` and later static page-bridge script insertion are separately recorded sinks; neither is silently relabelled remote-content execution. Absence of a located path is not a security guarantee.

## Concurrency, resources, and integrity

Synchronous claim mutations before `await` support event-loop-local ownership on selected paths. They do not prove thread safety, processing atomicity across `await`, distributed uniqueness, or complete failure cleanup. Candidate, request, worker, timeout, depth, response, per-origin, graph, diagnostic, and persistence bounds appear over time, but each is tied to its actual enforcement reference and failure behavior. Provenance identifiers support partial reconstruction; mutability and missing referential/immutability enforcement prevent an end-to-end integrity guarantee.

## Final answers

### 1. What could fail in the earliest implementation?

The earliest recovered v0.1 has URL-validation, request/network, timeout, recognition, persistence, export/UI, mutable-state, and worker/scheduler progress failure surfaces. Only some have explicit handlers. These are static paths and potential modes, not observed production incidents.

Evidence: `security-ev-8812129cadb6f280`, `security-ev-cd52827ef732e7d4`, `security-ev-b1fbd072c5e527b7`, `security-ev-5f02dc3748547b35`, `security-ev-f5938550f988fa3e`, `security-ev-92452c8c6a88aa28`, `security-ev-b90fb5bcfffb1a0b`, `security-ev-ee35b3e2616be7b6`, `security-ev-a636b4c2f43931b0`, `security-absence-f247455ad45b5a6c`

### 2. Where did failures terminate?

Termination varies by path: some acquisition errors become failed Observations/caller results; persistence handlers stop locally; later worker handlers can stop at a candidate or worker path. Unknown propagation is retained where control flow does not prove a stopping boundary.

Evidence: `security-ev-8812129cadb6f280`, `security-ev-cd52827ef732e7d4`, `security-ev-b1fbd072c5e527b7`, `security-ev-5f02dc3748547b35`, `security-ev-f5938550f988fa3e`, `security-ev-6b1bd6d142794968`, `security-ev-abd184135de8a5dc`, `security-ev-835a71ba17d2d8a9`, `security-ev-1d21f8fcd42ea7c6`, `security-ev-eaeb4711e4fdb262`

### 3. Which failures were silently discarded?

Empty or fallback-return catch paths are listed as intentional silence, unexplained silence, or error suppression. Logging-only suppression remains observable but does not propagate structured failure.

Evidence: `security-ev-8812129cadb6f280`, `security-ev-cd52827ef732e7d4`, `security-ev-b1fbd072c5e527b7`, `security-ev-5f02dc3748547b35`, `security-ev-6b1bd6d142794968`, `security-ev-abd184135de8a5dc`, `security-ev-835a71ba17d2d8a9`, `security-ev-1d21f8fcd42ea7c6`, `security-ev-02b567c67da4c8b5`, `security-ev-1ba1749f7bb08635`

### 4. When did failures become structured?

Observation error/status fields exist from v0.1; richer structured diagnostics first appear in v0.6.0. Structure does not imply complete preservation or verification.

Evidence: `security-ev-9e1b270cf149261a`, `security-ev-d78cbea44e26812a`, `security-ev-b4c766cbd30df652`, `security-ev-2300ebb00e50e014`, `security-ev-4ee417a3f7b1973a`, `security-ev-0dd9d36d75d2a552`, `security-ev-68d50316d9c0d79f`, `security-ev-60004747f53b0bdc`, `security-ev-1c4949c3b6935b6a`, `security-ev-2f431baa1463725b`

### 5. When did retry semantics appear?

A demonstrable count-plus-requeue retry path first appears in v0.3.0. Configuration-only retry names are not counted as implemented retry.

Evidence: `security-ev-c984040edce91058`, `security-ev-b0995f95c3feefc3`, `security-ev-1132fa88f610b64a`

### 6. When did cancellation appear?

AbortController/abort first appears in v0.3.0 on recovered paths. Earlier/lateral stop flags do not prove underlying request cancellation.

Evidence: `security-ev-f1e56a4ca72ee3e1`

### 7. When did resource bounds appear?

Candidate count, request count, worker concurrency, and request timeout bounds are present from v0.1. Later variants add depth, retries, body-size, per-origin, graph, diagnostic, and persistence-retention bounds.

Evidence: `security-ev-948cf470b5888a69`, `security-ev-2830473f43bce3b7`, `security-ev-c36edd585706ea75`, `security-ev-08cc2e4da8ffe70a`, `security-ev-f9d9b3c207c68249`, `security-ev-c9932dde2d91acff`, `security-ev-530e5c93b3b1af3f`, `security-ev-86efdcfaa2888d90`

### 8. When did concurrency safety become explicit?

v0.2 is the earliest recovered named claimNextCandidate path. Its short synchronous mutation sequence supports event-loop-local claim ownership before await, not thread safety or atomic processing across await.

Evidence: `security-ev-2edbfd1d30a21f40`, `security-ev-c420f255e02c9133`, `security-ev-c4ef2d16cfef0d8b`

### 9. When did provenance integrity become explicit?

Provenance representation through Candidate, Observation, and Discovery identifiers/fields is already explicit in v0.1. End-to-end provenance integrity, immutability, and non-loss are never guaranteed.

Evidence: `security-ev-d64c4269c0f700b3`, `security-ev-04a1849bf2b86df6`, `security-ev-58523db917b3633b`, `security-ev-650e0f4f98cc7e85`

### 10. What were the earliest trust boundaries?

v0.1 already crosses page DOM, admitted URLs, privileged/browser network APIs, remote content parsers/providers, storage, UI, and export boundaries. Scheduler structure is an authority boundary but is not automatically a trust boundary.

Evidence: `security-absence-1e3fe556108fa8d6`, `security-ev-6687585eb4e95e9d`, `security-ev-ce39263ea398c095`, `security-ev-99f0e1637bad7bae`, `security-ev-cfdebb9f2dc12d86`, `security-ev-30baf6409a04e8f0`, `security-ev-fdcba3da4e192bbc`, `security-ev-8fa6a5f31eb7c2ae`, `security-ev-2458cce86d2f93d8`, `security-ev-8a45f0571469596e`

### 11. When did network access become a distinct authority?

It is already distinct in v0.1: browser fetch and GM_xmlhttpRequest perform acquisition, while metadata grants GM_xmlhttpRequest and @connect *. Granted authority is distinguished from default same-origin policy and actual use.

Evidence: `security-ev-7baafdf429d732ce`, `security-ev-89fcecd7bf9f766a`

### 12. When did provider code become isolated?

The first recovered provider-local stopping boundary appears in v0.4.0. This proves selected catch paths only, not a provider isolation guarantee.

Evidence: `security-ev-aaa9560381e948a1`

### 13. When did remote data become explicitly treated as untrusted?

Parsing, allow checks, and provider recognition show implicit distrust from v0.1. An explicit complete threat statement that all remote content is untrusted was not recovered; retrospective interpretation remains separate.

Evidence: `security-ev-2224a706f10034c5`, `security-ev-604b0adf0ff4798b`, `security-ev-b37c0806ac4200ad`, `security-ev-cbd8c1d0a7f9b85c`, `security-ev-728b30ffe167a3a6`, `security-ev-335648e073ddb329`

### 14. What code/data boundaries existed?

Acquired HTML/JSON/text is parsed and extracted as data. No eval/new Function/dynamic-import path from acquired content was found. Later static page-bridge script insertion and UI innerHTML are separate sinks and do not prove remote content execution.

Evidence: `security-ev-c2b65f751cd68d51`, `security-ev-7123bf5d8c84d6f4`, `security-ev-05ed0b72a2e40a6d`, `security-ev-4b1f1121ff6d855b`, `security-ev-0400a2f04846ba1d`, `security-ev-dd33e5933d4533d6`, `security-ev-ebed62125f4af7ae`, `security-ev-f9bdf24b86aa2c0c`, `security-ev-d83a4c0b812e1958`, `security-ev-ffda3b844c9a7612`

### 15. What userscript privileges existed historically?

Recovered headers grant GM_getValue, GM_setValue, and GM_xmlhttpRequest throughout; selected branch variants also grant unsafeWindow. @connect * is present. v0.1/v0.2 recovered @match text is preserved literally and flagged as potentially Markdown-affected.

Evidence: `security-ev-7baafdf429d732ce`, `security-ev-e43b79edd1d1250b`, `security-ev-9d3c8f0fdf922089`, `security-ev-69f43687c3d760ee`, `security-ev-9966c57b646332f7`, `security-ev-dc21477849eb1956`, `security-ev-69ef0e06a748c9e1`, `security-ev-379285dc0f6243fd`, `security-ev-463009a06d8c22f2`, `security-ev-bde0c6ca0373c3f8`

### 16. How did acquisition scope evolve?

Current-page DOM plus active acquisition of admitted discovered resources already coexist in v0.1; a current-page-only predecessor is not recovered. Later versions elaborate policy and per-origin controls without proving protocol independence.

Evidence: `security-ev-7baafdf429d732ce`, `security-ev-89fcecd7bf9f766a`, `security-ev-e43b79edd1d1250b`, `security-ev-b9be3cd89a5960b9`, `security-ev-9d3c8f0fdf922089`, `security-ev-55674071807f3409`, `security-ev-69f43687c3d760ee`, `security-ev-b3763b993a627ad9`, `security-ev-9966c57b646332f7`, `security-ev-cd1cb1ff998f67c3`

### 17. How did authority migrate between components?

Network, candidate admission/claim, provider registration, state mutation, export, and configuration authority move among adapters, KnowledgeBase/scheduler, ProviderRegistry, engine, and UI across variants. Cross-version parentage is unknown, so this is comparative migration, not proved lineage.

Evidence: `security-ev-d9e5058dbe63c966`, `security-ev-979f38feb06f0fec`, `security-ev-b09312afbcf61aa8`, `security-ev-77f11af7029cc2d3`, `security-ev-95ad26395d96d042`, `security-ev-a82b3596633357ce`, `security-ev-efd9838fc7eb304b`, `security-ev-da9ccf7e37394f64`, `security-ev-19649f1287062611`, `security-ev-71decef9ec57ab2e`

### 18. Which security controls affected discovery completeness?

Same-origin checks, maximum candidate/request/depth/fanout/body limits, rate controls, and provider admission can bound work while excluding discoveries or truncating evidence. The tradeoff is structural; completeness loss was not measured.

Evidence: `security-ev-948cf470b5888a69`, `security-ev-2830473f43bce3b7`, `security-ev-c36edd585706ea75`, `security-ev-08cc2e4da8ffe70a`, `security-ev-f9d9b3c207c68249`, `security-ev-c9932dde2d91acff`, `security-ev-530e5c93b3b1af3f`, `security-ev-86efdcfaa2888d90`, `security-ev-9cf987ce4e7e19da`, `security-ev-1e8b1330a3862cc9`

### 19. Which security properties were documented but unenforced?

The clearest recovered example is v0.3's broad ‘Safer DOM/UI handling’ statement, which does not specify a complete enforceable property. Atomic-claim and bounded-work comments have local mechanisms but remain unverified as whole-system guarantees. Complete provider isolation, provenance non-loss, and untrusted-input non-execution are retrospective analytical assumptions unless separately documented.

Evidence: `security-ev-e76896ef295ed96a`, `security-ev-f3da7d05db853cb3`, `security-ev-7f1b04549b616213`, `security-ev-440d9662316f2e81`

### 20. Which security properties were implemented but undocumented?

Candidate key/visited/claimed checks, local catch boundaries, body/frontier bounds, and URL admission are mechanically present even where no security label is attached. They remain mechanisms or path properties, not generic guarantees.

Evidence: `security-ev-db5726c7efee3f8e`, `security-ev-03c88adaa970a421`, `security-ev-c4e774a69340b25f`, `security-ev-80099042171aef8d`, `security-ev-77f266a19fc0f29f`, `security-ev-aca15d5b382bd8ef`, `security-ev-3d8c7ac36a596f78`, `security-ev-19aeba3424a9e136`, `security-ev-f5938550f988fa3e`, `security-ev-92452c8c6a88aa28`

### 21. Which security mechanisms were later removed?

Adjacent-version comparisons contain controls absent in later variants, but no removal is classified as a proved regression because lineage, requirement continuity, and behavioral consequence are unproved.

Evidence: `security-ev-090755281bfac436`, `security-ev-4f52959e02632633`, `security-ev-7f3ca1a078f11d0d`, `security-ev-f95ce5b983873d9c`, `security-ev-3b16625e2da1e7c4`, `security-ev-ac26860e55542dc5`, `security-ev-59f895da4881668b`, `security-ev-3ab7c8dd550118e6`, `security-ev-bb12cc012cb2177b`, `security-ev-5d02ea92972c557a`

### 22. Which security concepts appeared only in later architecture?

Capability-oriented boundaries, WASM extension/execution, explicit policy architecture, and run isolation appear in later/current prose where located; they are not imported into earlier snapshots.

Evidence: `security-prose-bd024c40087b4836`, `security-prose-712ba4dd9551284c`, `security-prose-1734b4e2e4d2ed16`, `security-prose-179f24337f97b51c`

### 23. What is the earliest historically defensible security model?

v0.1 is already a bounded, same-origin-by-default web discovery userscript with privileged network/storage authority, URL admission, remote-data parsing, local error handling, persistence, provenance fields, and a worker pool. It is a partial path-based safety model—not a verified secure system. v0.2 adds the earliest explicit local claim protocol and reusable provider boundary.

Evidence: `security-absence-1e3fe556108fa8d6`, `security-ev-6687585eb4e95e9d`, `security-ev-ce39263ea398c095`, `security-ev-99f0e1637bad7bae`, `security-ev-cfdebb9f2dc12d86`, `security-ev-30baf6409a04e8f0`, `security-ev-fdcba3da4e192bbc`, `security-ev-8fa6a5f31eb7c2ae`, `security-ev-2458cce86d2f93d8`, `security-ev-8a45f0571469596e`, `security-ev-2edbfd1d30a21f40`, `security-ev-c420f255e02c9133`, `security-ev-c4ef2d16cfef0d8b`

## Final failure classification

OBSERVED FAILURES
─────────────────

Static failure detection/representation paths observed; runtime occurrence is not proved.
- DISCOVERY_FAILURE
- HTTP_FAILURE
- NETWORK_FAILURE
- PARSING_FAILURE
- PERSISTENCE_FAILURE
- PROVIDER_FAILURE
- RECOGNITION_FAILURE
- SCHEDULER_FAILURE
- TIMEOUT
- UI_FAILURE
- UNKNOWN_FAILURE
- VALIDATION_FAILURE

HANDLED FAILURES
────────────────

- DISCOVERY_FAILURE
- NETWORK_FAILURE
- PARSING_FAILURE
- PERSISTENCE_FAILURE
- PROVIDER_FAILURE
- RECOGNITION_FAILURE
- SCHEDULER_FAILURE
- TIMEOUT
- UI_FAILURE
- UNKNOWN_FAILURE
- VALIDATION_FAILURE

CONTAINED FAILURES
──────────────────

- DISCOVERY_FAILURE
- NETWORK_FAILURE
- PARSING_FAILURE
- PERSISTENCE_FAILURE
- PROVIDER_FAILURE
- RECOGNITION_FAILURE
- SCHEDULER_FAILURE
- TIMEOUT
- UI_FAILURE
- UNKNOWN_FAILURE
- VALIDATION_FAILURE

RECOVERABLE FAILURES
────────────────────

- DISCOVERY_FAILURE
- NETWORK_FAILURE
- PARSING_FAILURE
- PERSISTENCE_FAILURE
- PROVIDER_FAILURE
- RECOGNITION_FAILURE
- SCHEDULER_FAILURE
- TIMEOUT
- UNKNOWN_FAILURE
- VALIDATION_FAILURE

SILENT FAILURES
───────────────

- Acquisition.request: ERROR_SUPPRESSION (1 recovered occurrence(s))
- ApiDescriptionProvider.recognize: ERROR_SUPPRESSION (1 recovered occurrence(s))
- DiscoveryEngine.clear: ERROR_SUPPRESSION (2 recovered occurrence(s))
- DiscoveryEngine.expand: ERROR_SUPPRESSION (1 recovered occurrence(s))
- DiscoveryEngine.inspectDomNode: ERROR_SUPPRESSION (1 recovered occurrence(s))
- DiscoveryEngine.recordNetwork: ERROR_SUPPRESSION (1 recovered occurrence(s))
- DiscoveryEngine.seed: UNEXPLAINED_SILENCE (1 recovered occurrence(s))
- DiscoveryEngine.seedWellKnown: ERROR_SUPPRESSION (2 recovered occurrence(s))
- DiscoveryEngine.worker: ERROR_SUPPRESSION (5 recovered occurrence(s))
- EngineUI.downloadExport: ERROR_SUPPRESSION (4 recovered occurrence(s))
- GenericDiscoveryEngine.processCandidate: ERROR_SUPPRESSION (1 recovered occurrence(s))
- GenericDiscoveryEngine.restore: ERROR_SUPPRESSION (1 recovered occurrence(s))
- HtmlProvider.recognize: ERROR_SUPPRESSION (1 recovered occurrence(s))
- HttpAcquisitionAdapter.acquireGM: ERROR_SUPPRESSION (2 recovered occurrence(s))
- JsonProvider.discover: ERROR_SUPPRESSION (1 recovered occurrence(s))
- JsonProvider.recognize: ERROR_SUPPRESSION (10 recovered occurrence(s))
- KnowledgeBase.clear: ERROR_SUPPRESSION (2 recovered occurrence(s))
- KnowledgeBase.clear: INTENTIONAL_SILENCE (1 recovered occurrence(s))
- KnowledgeBase.load: ERROR_SUPPRESSION (11 recovered occurrence(s))
- KnowledgeBase.persist: ERROR_SUPPRESSION (8 recovered occurrence(s))
- KnowledgeBase.persistNow: ERROR_SUPPRESSION (2 recovered occurrence(s))
- KnowledgeBase.persistSoon: ERROR_SUPPRESSION (1 recovered occurrence(s))
- ManifestProvider.recognize: ERROR_SUPPRESSION (2 recovered occurrence(s))
- NetworkBridge.install: ERROR_SUPPRESSION (2 recovered occurrence(s))
- NetworkObserver.dispose: UNEXPLAINED_SILENCE (1 recovered occurrence(s))
- NetworkObserver.installFetchObserver: ERROR_SUPPRESSION (1 recovered occurrence(s))
- NetworkObserver.installPageBridge: ERROR_SUPPRESSION (4 recovered occurrence(s))
- NetworkObserver.installPerformanceObserver: ERROR_SUPPRESSION (7 recovered occurrence(s))
- NetworkObserver.installPerformanceObserver: INTENTIONAL_SILENCE (1 recovered occurrence(s))
- NetworkObserver.installXhrObserver: ERROR_SUPPRESSION (1 recovered occurrence(s))
- PerformanceNetworkObserver.install: INTENTIONAL_SILENCE (2 recovered occurrence(s))
- PerformanceObserverAdapter.install: INTENTIONAL_SILENCE (2 recovered occurrence(s))
- ProviderRegistry.candidatesFor: ERROR_SUPPRESSION (2 recovered occurrence(s))
- ProviderRegistry.discover: ERROR_SUPPRESSION (1 recovered occurrence(s))
- ProviderRegistry.recognize: ERROR_SUPPRESSION (5 recovered occurrence(s))
- ProviderRegistry.recognizeAll: ERROR_SUPPRESSION (4 recovered occurrence(s))
- RobotsProvider.matches: ERROR_SUPPRESSION (2 recovered occurrence(s))
- TOP_LEVEL.allowed: ERROR_SUPPRESSION (2 recovered occurrence(s))
- TOP_LEVEL.canonicalizeUrl: ERROR_SUPPRESSION (12 recovered occurrence(s))
- TOP_LEVEL.contentTypeForTarget: ERROR_SUPPRESSION (1 recovered occurrence(s))
- TOP_LEVEL.extractXmlLocs: UNEXPLAINED_SILENCE (3 recovered occurrence(s))
- TOP_LEVEL.getOrigin: ERROR_SUPPRESSION (1 recovered occurrence(s))
- TOP_LEVEL.gmRequest: ERROR_SUPPRESSION (1 recovered occurrence(s))
- TOP_LEVEL.hashText: UNEXPLAINED_SILENCE (1 recovered occurrence(s))
- TOP_LEVEL.initializeUi: ERROR_SUPPRESSION (4 recovered occurrence(s))
- TOP_LEVEL.installUi: ERROR_SUPPRESSION (4 recovered occurrence(s))
- TOP_LEVEL.isAllowedUrl: ERROR_SUPPRESSION (9 recovered occurrence(s))
- TOP_LEVEL.looksLikeApiUrl: ERROR_SUPPRESSION (3 recovered occurrence(s))
- TOP_LEVEL.originOf: ERROR_SUPPRESSION (2 recovered occurrence(s))
- TOP_LEVEL.sha256: UNEXPLAINED_SILENCE (1 recovered occurrence(s))
- TextProvider.matches: INTENTIONAL_SILENCE (2 recovered occurrence(s))

POTENTIAL FAILURE MODES
───────────────────────

- inconsistent status
- large DOM or JSON parse
- lost provenance
- orphaned discoveries
- orphaned observations
- partial records
- recursive/unbounded expansion
- stale claims
- unbounded response body

UNVERIFIED FAILURE MODES
────────────────────────

- INPUT_FAILURE
- VALIDATION_FAILURE
- CONFIGURATION_FAILURE
- ACQUISITION_FAILURE
- NETWORK_FAILURE
- TIMEOUT
- HTTP_FAILURE
- PARSING_FAILURE
- RECOGNITION_FAILURE
- PROVIDER_FAILURE
- DISCOVERY_FAILURE
- EXPANSION_FAILURE
- DEDUPLICATION_FAILURE
- SCHEDULER_FAILURE
- CONCURRENCY_FAILURE
- STATE_FAILURE
- PERSISTENCE_FAILURE
- EXPORT_FAILURE
- UI_FAILURE
- RESOURCE_EXHAUSTION
- CANCELLATION
- UNKNOWN_FAILURE

## Final security classification

HISTORICALLY VERIFIED SECURITY MECHANISMS
─────────────────────────────────────────

- URL parsing/canonicalization and admission checks
- request error and timeout callbacks
- provider/worker/persistence catch paths
- candidate key, visited, and claimed structures
- configured and referenced resource bounds

HISTORICALLY VERIFIED SECURITY PROPERTIES
─────────────────────────────────────────

- selected claim mutations execute synchronously before the first await
- selected provider exceptions are caught at registry/provider paths

SECURITY GOALS WITHOUT ENFORCEMENT
──────────────────────────────────

- Safer DOM/UI handling

RETROSPECTIVE SECURITY INTERPRETATIONS
──────────────────────────────────────

- Remote parsing and retained state form a resource-exhaustion surface; no exploit or incident is claimed.
- Ambient GM/browser authority is broader than narrow capability-like object passing; least authority is not established.

CURRENT/PROPOSED SECURITY ARCHITECTURE
──────────────────────────────────────

- capability-oriented extension boundaries
- WASM extension/execution proposal
- explicit policy architecture
- run isolation

UNKNOWN
───────

- whole-system provider isolation
- global uniqueness
- cross-thread/distributed safety
- redirect trust
- persistence crash atomicity
- absence of all code-execution paths

## Governing conclusion

The strongest defensible historical model is path-specific: later recovered forms contain additional failure kinds, context records, local stopping/retry/cancellation paths, and resource controls, while branch comparisons remain non-lineage. It never becomes historically verified as secure or resilient. A catch is not isolation; a Set is not global uniqueness; a worker pool is not a complete resource guarantee; a URL parser is not policy; a provenance field is not provenance integrity; and an interface is not a security boundary.
