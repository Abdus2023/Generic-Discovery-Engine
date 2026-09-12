# Observation and Provenance Evolution

> **Acceptance: PROVISIONAL_ONLY_UPSTREAM_BLOCKED.** Protocol-v1 raw/range validation fails and Protocol-v4 through Protocol-v7 outputs are absent. `SUPPORTED` in this report is source-local and does not mean the full v1→v9 chain is verified. Missing dimensions remain `UNKNOWN`.

| Snapshot | Version | Observation fields | Explicit provenance syntax | Additional source surfaces |
|---|---|---|---|---|
| snapshot-0001 | v0.1.0 | candidateId, completedAt, errors, features, http, id, signalPresent, startedAt, status, target | yes | none scanned |
| snapshot-0003 | v0.2.0 | body, candidateId, completedAt, errors, http, id, signalPresent, startedAt, status, target | yes | none scanned |
| snapshot-0005 | v0.3.0 | body, candidateId, completedAt, errors, http, id, signalPresent, startedAt, status, target | yes | none scanned |
| snapshot-0006 | v0.4.0 | body, candidateId, completedAt, errors, http, id, signalPresent, startedAt, status, target | yes | none scanned |
| snapshot-0008 | v0.4.0 | body, candidateId, completedAt, errors, http, id, network, signalPresent, startedAt, status, target | yes | network observation |
| snapshot-0007 | v0.5.0 | body, bodyTruncated, candidateId, completedAt, errors, http, id, signalPresent, startedAt, status, target | yes | network observation |
| snapshot-0009 | v0.5.0 | body, candidateId, completedAt, errors, fingerprint, http, id, signalPresent, startedAt, status, target | yes | network observation |
| snapshot-0011 | v0.5.0 | body, candidateId, completedAt, errors, fingerprint, http, id, network, signalPresent, startedAt, status, target | yes | network observation |
| snapshot-0010 | v0.6.0 | body, candidateId, completedAt, errors, fingerprint, http, id, signalPresent, startedAt, status, target | yes | network observation |
| snapshot-0012 | v0.6.0 | body, candidateId, completedAt, errors, fingerprint, http, id, network, reason, signalPresent, startedAt, status, target | yes | network observation, diagnostic/trace/metric syntax, acquisition policy |
| snapshot-0013 | v0.6.0 | body, candidateId, completedAt, errors, fingerprint, http, id, network, reason, requestedUrl, signalPresent, startedAt, status, target | yes | network observation, diagnostic/trace/metric syntax, acquisition policy |
| snapshot-0014 | v0.7.1 | body, bodyTruncated, candidateId, completedAt, errors, fingerprint, http, id, network, planId, reason, requestedUrl, signalPresent, startedAt, status, target | yes | network observation, diagnostic/trace/metric syntax, acquisition policy, acquisition plan, decision ledger |

Observations are structured from the earliest complete occurrence, separating acquisition facts from interpretation. Discovery records carry candidate/observation associations and provenance-shaped fields in many occurrences. Later alternatives add network observations, edges, traces, diagnostics, or decision records. This supports increasing observability surface, not end-to-end provenance integrity: identifiers can be generated or propagated incorrectly, mutable stores can corrupt lineage, and Protocol-v7 contracts are unavailable.
